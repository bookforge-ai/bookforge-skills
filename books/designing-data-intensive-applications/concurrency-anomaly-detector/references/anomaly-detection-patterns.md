# Anomaly Detection Patterns

Reference for Step 2 of the concurrency-anomaly-detector process. SQL and ORM grep patterns for all 6 concurrency anomaly types, with per-language examples and false positive filters.

---

## How to Use This Reference

Run the grep patterns below in the codebase to find candidate code locations. Each pattern produces a list of files and line numbers. For each hit, apply the false positive filter to determine whether it is an actual exposure. Then classify into a finding using Step 3 of the skill.

---

## Pattern 1: Lost Update Detection

### What to find
A transaction that reads a value, computes a new value in application code, and writes it back. The key marker is application-layer arithmetic between read and write — the new value depends on the old value.

### SQL grep patterns
```
SELECT.*FROM.*\n.*UPDATE
UPDATE.*SET.*=.*\+
UPDATE.*SET.*=.*-
SELECT.*FOR UPDATE.*\n.*UPDATE    ← explicit lock present; lower risk but verify
```

### ORM grep patterns (Python/SQLAlchemy)
```python
# High risk: find then modify in loop or immediate scope
session.query(Model).filter(...).one()
session.query(Model).filter(...).first()
# Followed by: obj.field += or obj.field -= or obj.field = obj.field +
```

### ORM grep patterns (Java/Hibernate)
```java
em.find(Entity.class, id)
repository.findById(id)
// Followed by: entity.setField(entity.getField() + delta)
//              or entity.setCount(entity.getCount() + 1)
```

### ORM grep patterns (Ruby/ActiveRecord)
```ruby
record = Model.find(id)
record = Model.find_by(...)
# Followed by: record.field += delta, record.save
# Also: Model.increment(:column, ...)  ← atomic — NOT a lost update
```

### ORM grep patterns (Go/sqlx or GORM)
```go
db.First(&entity, id)
db.Where(...).First(&entity)
// Followed by: entity.Field = entity.Field + delta
//              db.Save(&entity)
```

### ORM grep patterns (Node.js/Sequelize)
```javascript
await Model.findOne({ where: ... })
await Model.findByPk(id)
// Followed by: instance.field += delta, instance.save()
```

### False positives (NOT lost updates)
```sql
-- Pure SQL atomic expression: no application-layer read needed
UPDATE counters SET value = value + 1 WHERE key = 'x';
UPDATE accounts SET balance = balance - :amount WHERE id = :id AND balance >= :amount;
```
```python
# SQLAlchemy atomic update: no Python-layer arithmetic
session.execute(update(Counter).where(...).values(value=Counter.value + 1))
```
```ruby
# ActiveRecord atomic: no Ruby-layer arithmetic
Account.where(id: id).update_all("balance = balance - #{amount}")
Model.increment_counter(:count, id)
```

These are safe — the arithmetic happens inside the database atomically, with no window for a concurrent read to see the old value.

---

## Pattern 2: Write Skew Detection

### What to find
A transaction that reads an aggregate or existence condition (COUNT, SUM, EXISTS, MAX, MIN), makes an application-level decision based on the result, then performs a write that changes the state of the condition.

This is the single most commonly missed pattern. It looks like safe code — each transaction is individually correct. The race condition only appears when two transactions run simultaneously.

### SQL grep patterns
```sql
SELECT COUNT(*)                -- check count, then write based on result
SELECT SUM(                    -- check aggregate, then insert/update
SELECT EXISTS(                 -- check existence, then write
SELECT MAX(                    -- check bound, then write
```
All followed (in the same transaction scope) by INSERT, UPDATE, or DELETE.

### ORM grep patterns
```python
# Python/SQLAlchemy
session.query(Model).filter(...).count()      # check count
session.query(func.sum(Model.field)).scalar() # check sum
session.query(Model).filter(...).first()      # check existence
# All followed by session.add(...) or session.execute(update(...))
```

```java
// Java/Hibernate
repository.countBy...()
repository.existsBy...()
entityManager.createQuery("SELECT SUM(...)").getSingleResult()
// Followed by: entityManager.persist(new Entity(...)) or repository.save(new Entity(...))
```

```ruby
# Ruby/ActiveRecord
Model.where(...).count
Model.where(...).exists?
Model.where(...).sum(:field)
# Followed by: Model.create(...) or record.update(...)
```

```javascript
// Node.js/Sequelize
await Model.count({ where: ... })
await Model.sum('field', { where: ... })
await Model.findOne({ where: ... })  // guard for uniqueness
// Followed by: await Model.create(...)
```

### The 5 write skew patterns — specific code signatures

**At-least-one constraint (doctor on-call):**
```sql
SELECT COUNT(*) FROM resources WHERE status = 'active' AND group_id = $1;
-- app: if count >= 2, proceed
UPDATE resources SET status = 'inactive' WHERE id = $2;
```
Signal: COUNT check with threshold, followed by UPDATE on a different row than was counted.

**No-overlap constraint (booking system):**
```sql
SELECT COUNT(*) FROM bookings
  WHERE resource_id = $1 AND end_time > $2 AND start_time < $3;
-- app: if count = 0, proceed
INSERT INTO bookings (resource_id, start_time, end_time, user_id)
  VALUES ($1, $2, $3, $4);
```
Signal: Time-range overlap check followed by INSERT into same table.

**Unique claim (username registration):**
```sql
SELECT COUNT(*) FROM users WHERE username = $1;
-- app: if count = 0, proceed
INSERT INTO users (username, ...) VALUES ($1, ...);
```
Signal: Existence check followed by INSERT with the checked value.
Note: A UNIQUE constraint on `username` is sufficient here — no serializable isolation needed.

**Budget / sum constraint (spending limit):**
```sql
SELECT SUM(amount) FROM spending WHERE account_id = $1;
-- app: if sum + new_amount <= limit, proceed
INSERT INTO spending (account_id, amount, ...) VALUES ($1, $2, ...);
```
Signal: SUM aggregate check followed by INSERT that would increase the sum.

**Game state validity:**
```sql
SELECT position FROM game_pieces WHERE piece_id = $1 AND game_id = $2;
-- app: validate move legality based on position
UPDATE game_pieces SET position = $3 WHERE piece_id = $1;
```
Signal: State read for validity check, followed by UPDATE that changes other game state.

### False positives (NOT write skew)
- Read-only queries with no subsequent write in the same transaction
- Writes that do not change the condition checked by the SELECT (e.g., SELECT from table A, write to unrelated table B with no logical dependency)
- Cases where a UNIQUE database constraint catches the conflict at the insert level (duplicate username pattern)

---

## Pattern 3: Phantom Read Detection

### What to find
A transaction checks for zero matching rows, then inserts a row that matches the same condition. This is the phantom variant of write skew. Unlike write skew over existing rows, `SELECT FOR UPDATE` cannot help — there are no rows to lock when the SELECT returns empty.

### Key distinguishing marker
The SELECT returns zero rows (or checks for absence), and the INSERT creates a row that would match the SELECT's WHERE condition.

### SQL grep patterns
```sql
-- Absence check followed by insert
SELECT COUNT(*) FROM table WHERE condition = $1  -- returning 0
INSERT INTO table WHERE ...                       -- values match condition

-- Or: SELECT returns empty, INSERT follows
SELECT id FROM table WHERE unique_key = $1;
-- if no rows: INSERT INTO table (unique_key, ...) VALUES ($1, ...);
```

### ORM grep patterns
```python
# Booking conflict check
existing = session.query(Booking).filter(
    Booking.room_id == room_id,
    Booking.end_time > start_time,
    Booking.start_time < end_time
).count()
if existing == 0:
    session.add(Booking(room_id=room_id, ...))
```

```java
// Room booking
long conflicts = bookingRepo.countConflicting(roomId, startTime, endTime);
if (conflicts == 0) {
    bookingRepo.save(new Booking(roomId, startTime, endTime, userId));
}
```

### Differentiation from general write skew
Write skew over existing rows: SELECT returns rows → FOR UPDATE possible as mitigation
Phantom write skew: SELECT returns no rows → FOR UPDATE does nothing → serializable required

---

## Pattern 4: Read Skew Detection

### What to find
A long-running transaction that reads from multiple tables or reads the same data multiple times, where the combined result must be internally consistent.

### Code signals
- Long-running batch or background jobs inside a transaction
- Multiple SELECT queries over related tables in one transaction scope
- Backup or export operations that read the entire database or large subsets
- Integrity check queries that join or compare multiple tables

### SQL grep patterns
```sql
-- Two or more SELECTs from related tables in the same transaction
BEGIN;
SELECT ... FROM table_a WHERE ...;
-- other processing
SELECT ... FROM table_b WHERE ...;  -- related to table_a result
COMMIT;
```

### ORM grep patterns (Python)
```python
with db.session.begin():
    accounts = session.query(Account).filter(...).all()
    # ... some processing ...
    transfers = session.query(Transfer).filter(...).all()
    # If accounts and transfers must balance, this is read skew exposure
```

### False positives
- Single-table reads (no cross-table consistency requirement)
- Read committed isolation is acceptable when the query is idempotent (re-running gives a useful result even if slightly stale)
- Short transactions where the window for a concurrent write to commit between reads is negligible

---

## Pattern 5: Dirty Read and Dirty Write Detection

### Dirty reads
Only possible at isolation level `READ UNCOMMITTED`. Rare in production — almost no database defaults to this level.

### SQL grep patterns
```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
isolation_level='READ UNCOMMITTED'
```

### Dirty writes
Prevented by all practical isolation levels (read committed and above) through row-level write locks. Flag only if:
- Autocommit is enabled per-statement and transactions are not used
- The application manually manages locking and a lock is missing

### SQL grep patterns for missing transaction boundaries
```sql
-- INSERTs, UPDATEs, DELETEs outside any transaction context
-- Autocommit enabled with no explicit transaction wrapping multi-step operations
SET autocommit = 1   -- MySQL
-- Followed by multi-step write operations with no BEGIN/COMMIT
```

---

## Per-Database Notes on What Is and Is Not Automatically Prevented

### PostgreSQL

| Anomaly | At READ COMMITTED (default) | At REPEATABLE READ | At SERIALIZABLE |
|---------|--------------------------|---------------------|-----------------|
| Dirty read | Prevented | Prevented | Prevented |
| Dirty write | Prevented | Prevented | Prevented |
| Read skew | **EXPOSED** | Prevented | Prevented |
| Lost update | **EXPOSED** | Auto-detected, aborts | Prevented |
| Write skew | **EXPOSED** | **EXPOSED** | Prevented |
| Phantom (write skew) | **EXPOSED** | **EXPOSED** | Prevented |

**PostgreSQL SERIALIZABLE uses SSI (serializable snapshot isolation)** — true serializable with optimistic concurrency. Aborts transactions rather than blocking. Application must implement retry on SQLSTATE 40001.

### MySQL InnoDB

| Anomaly | At READ COMMITTED | At REPEATABLE READ (default) | At SERIALIZABLE |
|---------|------------------|------------------------------|-----------------|
| Dirty read | Prevented | Prevented | Prevented |
| Dirty write | Prevented | Prevented | Prevented |
| Read skew | **EXPOSED** | Prevented | Prevented |
| Lost update | **EXPOSED** | **EXPOSED (NOT auto-detected!)** | Prevented |
| Write skew | **EXPOSED** | **EXPOSED** | Prevented |
| Phantom (write skew) | **EXPOSED** | **EXPOSED** | Prevented |

**Critical MySQL difference:** MySQL InnoDB at REPEATABLE READ does NOT automatically detect lost updates. PostgreSQL does. Two concurrent read-modify-write cycles will silently lose one update in MySQL. PostgreSQL will abort one and require a retry.

**MySQL SERIALIZABLE uses two-phase locking (2PL)** — pessimistic. Readers block writers; writers block readers. No abort/retry needed but lock contention higher.

### Oracle 11g

| Anomaly | At READ COMMITTED (default) | At "SERIALIZABLE" (= snapshot isolation) |
|---------|-----------------------------|------------------------------------------|
| Dirty read | Prevented | Prevented |
| Dirty write | Prevented | Prevented |
| Read skew | **EXPOSED** | Prevented |
| Lost update | **EXPOSED** | Auto-detected |
| Write skew | **EXPOSED** | **EXPOSED** |
| Phantom (write skew) | **EXPOSED** | **EXPOSED** |

**Oracle's SERIALIZABLE is snapshot isolation, not true serializable.** Write skew is still possible. There is no true serializable isolation available in Oracle 11g.

---

## Quick Grep Commands

### Find read-modify-write cycles (lost update candidates)
```bash
# Python: find() followed by attribute modification
grep -n "session.query\|db.session.get\|Model.get\|Model.find" -A 5 \
  $(find . -name "*.py") | grep -B 3 "+="

# Java: find followed by setter
grep -rn "findById\|em.find\|repository.find" --include="*.java" -A 5 | \
  grep -B 3 "\.set[A-Z]"
```

### Find check-then-act write skew candidates
```bash
# SQL files: COUNT or SUM followed by INSERT/UPDATE in same file
grep -n "SELECT COUNT\|SELECT SUM\|SELECT EXISTS" **/*.sql

# Python: count() or exists() in transaction context
grep -rn "\.count()\|\.exists()" --include="*.py" -B 2 -A 5 | \
  grep -B 5 "session.add\|\.save()\|\.create("

# Java: countBy or existsBy followed by save/persist
grep -rn "countBy\|existsBy\|\.count()\|\.exists()" --include="*.java" -A 10 | \
  grep -B 8 "\.save\|\.persist\|\.create"
```

### Find phantom-variant candidates (absence check + insert)
```bash
# SQL: COUNT = 0 check followed by INSERT
grep -n "COUNT.*= 0\|count.*== 0\|count.*=== 0" **/*.{py,java,go,js,rb} -A 5 | \
  grep -B 3 "INSERT\|\.create\|\.add\|\.save"
```

### Find isolation level configuration
```bash
grep -rn "ISOLATION LEVEL\|isolation_level\|transaction_isolation\|@Transactional" \
  --include="*.{py,java,go,js,rb,yml,yaml,properties,xml}"
```
