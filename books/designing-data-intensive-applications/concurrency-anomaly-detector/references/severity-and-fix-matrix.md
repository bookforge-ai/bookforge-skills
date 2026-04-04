# Severity and Fix Matrix

Reference for Step 3 of the concurrency-anomaly-detector process. Severity per anomaly type per isolation level, fix decision tree, and fix applicability conditions.

---

## Severity by Anomaly and Effective Isolation Level

A finding's severity depends on both the anomaly type and the isolation level currently in effect. The same code pattern that is CRITICAL at read committed may be NOT PRESENT at serializable.

| Anomaly | Read Uncommitted | Read Committed | Snapshot Isolation | Serializable |
|---------|:----------------:|:--------------:|:-----------------:|:------------:|
| Dirty read | HIGH | NOT PRESENT | NOT PRESENT | NOT PRESENT |
| Dirty write | HIGH | NOT PRESENT | NOT PRESENT | NOT PRESENT |
| Read skew | MEDIUM | MEDIUM | NOT PRESENT | NOT PRESENT |
| Lost update (PostgreSQL/Oracle SI) | HIGH | HIGH | MEDIUM* | NOT PRESENT |
| Lost update (MySQL InnoDB RR) | HIGH | HIGH | HIGH** | NOT PRESENT |
| Write skew | CRITICAL | CRITICAL | CRITICAL | NOT PRESENT |
| Phantom (write skew variant) | CRITICAL | CRITICAL | CRITICAL | NOT PRESENT |

*PostgreSQL and Oracle automatically detect and abort one of the conflicting transactions at snapshot isolation. The anomaly does not silently corrupt data, but the application must handle the abort and retry. Severity is MEDIUM because it requires application-level retry handling that is often missing.

**MySQL InnoDB repeatable read does NOT automatically detect lost updates. Two concurrent read-modify-write cycles silently lose one update. This is HIGH severity, not MEDIUM — the data corruption is silent.

---

## Severity Definitions

| Severity | Meaning | Action required |
|----------|---------|-----------------|
| CRITICAL | Invariant violation that cannot be prevented without serializable isolation (or specific mitigation). Business logic constraints can be violated silently with no database error. Examples: double-booking, zero staff on shift, negative balance. | Fix before next production deployment. |
| HIGH | Silent data corruption or reads of data that never existed. Direct integrity violation. Examples: lost counter increment, overwritten balance update. | Fix in current sprint. |
| MEDIUM | Transaction sees internally inconsistent state. Dangerous for analytics, backups, integrity checks. May produce incorrect results without error. | Assess impact; fix if long-running reads are involved. |
| LOW | Possible exposure but requires unusual timing or very high conturrency to trigger. Or: the anomaly is possible in theory but the affected data has compensating constraints. | Note in code review; monitor. |
| NOT PRESENT | The effective isolation level prevents this anomaly. No code change required for this specific finding. | No action required. |

---

## Fix Decision Tree

For each finding, select the fix using this tree:

```
Is the effective isolation level already sufficient to prevent this anomaly?
  YES → NOT PRESENT; skip this finding
  NO  → Continue

Is the anomaly a lost update?
  YES →
    Is the write value computed purely in SQL (no application-layer arithmetic)?
      YES → Already safe (atomic SQL operation). Mark as false positive.
      NO  →
        Can the write be expressed as a pure SQL expression? (e.g., value = value + ?)
          YES → Fix A: Replace read-modify-write with atomic SQL UPDATE
          NO  →
            Is the database PostgreSQL or Oracle at snapshot isolation?
              YES → Aborts automatically; add retry logic (Fix B)
              NO  → Fix C: Add SELECT FOR UPDATE before the read, OR
                    Fix D: Upgrade to serializable isolation
  NO  → Continue (not a lost update)

Is the anomaly write skew (non-phantom variant)?
  YES →
    Does the precondition SELECT return existing rows?
      YES → Fix E: Add SELECT FOR UPDATE to the precondition query
      NO  → Fix F: Upgrade to serializable isolation
             (or Fix G: Materialize conflicts — last resort)
  NO  → Continue

Is the anomaly a phantom (check-for-absence then insert)?
  YES →
    Is a UNIQUE database constraint sufficient to enforce the invariant?
      YES → Fix H: Add UNIQUE constraint (no application change needed)
      NO  → Fix F: Upgrade to serializable isolation
             (or Fix G: Materialize conflicts — last resort)
  NO  → Continue

Is the anomaly read skew?
  YES → Fix I: Upgrade the transaction to snapshot isolation (REPEATABLE READ or higher)
  NO  → Continue

Is the anomaly a dirty read or dirty write?
  YES → Fix J: Enable read committed isolation (the database default for most systems)
```

---

## Fix Catalog

### Fix A: Replace Read-Modify-Write with Atomic SQL UPDATE

**Applies to:** Lost update — when the new value can be expressed as a SQL expression.

**What to change:** Remove the SELECT that reads the old value. Replace the application-layer arithmetic with a SQL expression in the UPDATE statement. Add a WHERE guard to check preconditions.

**Before:**
```python
# Python — read-modify-write cycle (vulnerable)
item = session.query(InventoryItem).filter_by(id=item_id).one()
if item.quantity < requested:
    raise InsufficientStock()
item.quantity -= requested
session.commit()
```

**After:**
```python
# Atomic SQL update with guard — safe
result = session.execute(
    update(InventoryItem)
    .where(InventoryItem.id == item_id)
    .where(InventoryItem.quantity >= requested)
    .values(quantity=InventoryItem.quantity - requested)
    .returning(InventoryItem.quantity)
)
if result.rowcount == 0:
    raise InsufficientStock()
session.commit()
```

**SQL equivalent:**
```sql
UPDATE inventory_items
  SET quantity = quantity - :requested
  WHERE id = :item_id AND quantity >= :requested;
-- Check rows_affected == 1; if 0, insufficient stock
```

**Why it works:** The arithmetic happens atomically inside the database. No window exists for a concurrent read to see the old value and compute the same update.

**Limitation:** Requires that the new value can be expressed as a function of the current value in SQL. Not applicable when the update logic requires complex application code (e.g., parsing a JSON document, applying business rules, calling an external service).

---

### Fix B: Add Retry Logic for Snapshot Isolation Aborts (PostgreSQL/Oracle)

**Applies to:** Lost update — PostgreSQL or Oracle at snapshot isolation (automatic detection aborts the transaction; application must retry).

**What to change:** Wrap the transaction in a retry loop. Catch the serialization failure exception and retry from scratch.

```python
# Python / psycopg2
import psycopg2
from psycopg2 import errors

def execute_with_retry(conn, transaction_fn, max_retries=5):
    for attempt in range(max_retries):
        try:
            with conn.cursor() as cur:
                cur.execute("BEGIN")
                result = transaction_fn(cur)
                conn.commit()
                return result
        except errors.SerializationFailure:
            conn.rollback()
            if attempt == max_retries - 1:
                raise
            continue
        except Exception:
            conn.rollback()
            raise
```

```java
// Java / Spring — retry template
@Retryable(value = {DataAccessException.class}, maxAttempts = 5)
@Transactional(isolation = Isolation.REPEATABLE_READ)
public void performUpdate(...) {
    // transaction body
}
```

**SQLSTATE to catch:**
- PostgreSQL: `40001` (serialization_failure)
- Oracle: `ORA-08177` (can't serialize access)

**Why it works:** The database detects the lost update conflict at commit time and aborts one transaction. The retry re-executes the transaction from the beginning, at which point it reads the updated value and proceeds correctly.

---

### Fix C: SELECT FOR UPDATE (Read Lock)

**Applies to:** Lost update — when Fix A is not applicable (complex application logic between read and write).

**What to change:** Add `FOR UPDATE` to the SELECT that reads the value being modified. This acquires an exclusive lock on the row, blocking any concurrent transaction that tries to read the same row with FOR UPDATE.

**Before:**
```sql
SELECT balance FROM accounts WHERE id = $1;
-- application computes new balance
UPDATE accounts SET balance = $new_balance WHERE id = $1;
```

**After:**
```sql
SELECT balance FROM accounts WHERE id = $1 FOR UPDATE;
-- application computes new balance
UPDATE accounts SET balance = $new_balance WHERE id = $1;
```

**Why it works:** The FOR UPDATE lock prevents a concurrent transaction from reading the same row in its own FOR UPDATE SELECT until the first transaction commits. The second transaction reads the updated value rather than the stale value.

**Limitation:** Requires remembering to add FOR UPDATE everywhere the row is read for modification. Missing one lock anywhere in the codebase creates the vulnerability. Serializable isolation is more robust because it applies automatically.

---

### Fix D: Upgrade Isolation Level

**Applies to:** Lost update — when Fix A, B, and C are not applicable or not sufficient.

Per-database settings:

```sql
-- PostgreSQL
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- or: SET default_transaction_isolation = 'repeatable read';

-- MySQL InnoDB (REPEATABLE READ does NOT detect lost updates)
-- Must upgrade to SERIALIZABLE
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- SQL Server
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
-- Requires READ_COMMITTED_SNAPSHOT=ON at database level

-- Oracle
-- No true serializable available; use SELECT FOR UPDATE (Fix C)
```

---

### Fix E: SELECT FOR UPDATE on Precondition Query (Write Skew over Existing Rows)

**Applies to:** Write skew — where the precondition SELECT returns existing rows that can be locked.

**Applicable when:** The check-then-act pattern reads rows that exist in the database (not checking for absence).

**Not applicable when:** The SELECT returns zero rows (checking for absence) — no rows exist to lock.

**Before:**
```sql
BEGIN;
SELECT COUNT(*) FROM doctors
  WHERE on_call = true AND shift_id = $1;
-- if count >= 2, proceed
UPDATE doctors SET on_call = false WHERE name = $2 AND shift_id = $1;
COMMIT;
```

**After:**
```sql
BEGIN;
SELECT COUNT(*) FROM doctors
  WHERE on_call = true AND shift_id = $1
  FOR UPDATE;                                    -- lock all on-call rows
-- concurrent transactions must wait until this one commits
UPDATE doctors SET on_call = false WHERE name = $2 AND shift_id = $1;
COMMIT;
```

**Why it works:** FOR UPDATE locks every row returned by the SELECT. A second concurrent transaction's FOR UPDATE SELECT must wait until the first transaction commits. After the first commits (count = 1), the second reads count = 1 and fails the check.

**Limitation:** If the shift has many on-call doctors, this locks all of them for the duration of the transaction. Assess whether this lock scope is acceptable for the workload.

**ORM equivalents:**
```python
# SQLAlchemy
session.query(Doctor).filter_by(on_call=True, shift_id=shift_id).with_for_update().count()
```
```java
// Spring Data JPA
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT COUNT(d) FROM Doctor d WHERE d.onCall = true AND d.shiftId = :shiftId")
long countOnCallForUpdate(@Param("shiftId") long shiftId);
```
```ruby
# ActiveRecord
Doctor.where(on_call: true, shift_id: shift_id).lock("FOR UPDATE").count
```

---

### Fix F: Upgrade to Serializable Isolation

**Applies to:** Write skew (phantom variant, or where FOR UPDATE is insufficient or impractical).

**Per-database settings:**

```sql
-- PostgreSQL: SSI (optimistic; aborts conflicting transactions at commit)
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- or: SET default_transaction_isolation = 'serializable';

-- MySQL InnoDB: 2PL (pessimistic; blocks conflicting transactions)
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- SQL Server: 2PL
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Oracle: not available as true serializable.
-- Oracle "SERIALIZABLE" = snapshot isolation. Write skew still possible.
-- Use Fix E (FOR UPDATE) or Fix G (materializing conflicts) for Oracle.
```

**Application requirements for PostgreSQL SSI:**
- Implement retry logic for SQLSTATE 40001 (serialization_failure)
- The entire transaction must be re-executed on abort — ORM frameworks do not retry by default
- See fix B code patterns for retry implementation

---

### Fix G: Materialize Conflicts (Last Resort)

**Applies to:** Phantom write skew — where the SELECT returns no rows, FOR UPDATE cannot be used, and upgrading to serializable isolation is not possible (e.g., Oracle).

**What to change:** Create a table of "lock rows" that represent the space of possible conflicts. Lock the appropriate rows before checking for conflicts and inserting.

**Example — booking system:**
```sql
-- Create a time slot lock table ahead of time (all rooms × all 15-minute slots for next 6 months)
CREATE TABLE booking_locks (
    room_id INT,
    slot_start TIMESTAMP,
    PRIMARY KEY (room_id, slot_start)
);

-- In the booking transaction:
BEGIN;
-- Lock all slots that overlap the requested time range
SELECT * FROM booking_locks
  WHERE room_id = $1
    AND slot_start >= $2
    AND slot_start < $3
  FOR UPDATE;

-- Now check for conflicting bookings
SELECT COUNT(*) FROM bookings
  WHERE room_id = $1 AND end_time > $2 AND start_time < $3;

-- If count = 0, insert
INSERT INTO bookings (...) VALUES (...);
COMMIT;
```

**Why it works:** Now there are rows to lock with FOR UPDATE — the lock rows. Two concurrent booking transactions for the same room and time range both try to lock the same lock rows. One must wait. After the first commits, the second reads the count and finds the conflict.

**Why this is a last resort:**
- Requires creating and maintaining an additional table
- Lock rows must be populated ahead of time (cron job or migration)
- Coupling concurrency control mechanics into the data model is ugly
- Harder to reason about correctness than serializable isolation
- Only use when serializable isolation is genuinely unavailable or has unacceptable overhead

---

### Fix H: UNIQUE Database Constraint

**Applies to:** Phantom write skew where the uniqueness can be enforced at the single-row level (username, single-column unique values).

**What to change:** Add a UNIQUE constraint to the table. Let the database enforce the invariant at the storage level rather than at the application level.

```sql
-- Username uniqueness: UNIQUE constraint is the right tool
ALTER TABLE users ADD CONSTRAINT unique_username UNIQUE (username);

-- Seat assignment: UNIQUE constraint on (flight_id, seat_number)
ALTER TABLE seat_assignments ADD CONSTRAINT unique_seat UNIQUE (flight_id, seat_number);
```

**Application change:** Catch the unique constraint violation exception and return the appropriate application error.

```python
try:
    db.session.add(User(username=username, ...))
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    raise UsernameAlreadyTakenError()
```

**Why it works:** The UNIQUE constraint is enforced by the database at the storage layer, regardless of isolation level. Two concurrent inserts for the same username — one will succeed, one will fail with a constraint violation. No race condition possible.

**Limitation:** Only works when the invariant can be expressed as a uniqueness constraint on a single row. Does not apply to multi-row invariants (e.g., "at most one booking per room per overlapping time range" requires range comparison, not row uniqueness).

---

### Fix I: Upgrade to Snapshot Isolation for Long-Running Reads

**Applies to:** Read skew — long-running transactions that read multiple related tables.

**What to change:** Set the transaction isolation to REPEATABLE READ (snapshot isolation) for transactions that perform long-running reads across multiple tables.

```python
# Python: per-transaction isolation
with engine.connect() as conn:
    conn.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
    # All reads within this transaction see a consistent snapshot
    accounts = conn.execute(select(accounts_table)).fetchall()
    transfers = conn.execute(select(transfers_table)).fetchall()
    conn.commit()
```

```java
// Java Spring: per-method isolation
@Transactional(isolation = Isolation.REPEATABLE_READ)
public BillingReport generateBillingReport() {
    // All reads see the database state at transaction start
}
```

**Why it works:** Snapshot isolation takes a consistent snapshot of the entire database at the start of the transaction. All reads within the transaction — regardless of how many there are or how long the transaction runs — see the same point-in-time state. Concurrent writes by other transactions are invisible.

---

### Fix J: Enable Read Committed (Baseline Fix)

**Applies to:** Dirty reads — when the database is at read uncommitted.

**What to change:** Set the isolation level to read committed (the default for most production databases).

```sql
-- PostgreSQL
SET default_transaction_isolation = 'read committed';

-- MySQL
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Application-level: remove any explicit READ UNCOMMITTED settings
```

**Note:** Dirty writes are prevented at read committed and above through row-level write locks — no additional change needed beyond ensuring read uncommitted is not in use.

---

## Fix Applicability Summary

| Anomaly | Fix A | Fix B | Fix C | Fix D | Fix E | Fix F | Fix G | Fix H | Fix I |
|---------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| Dirty read / dirty write | | | | | | | | | Fix J |
| Read skew | | | | | | | | | ✓ |
| Lost update (expressible as SQL) | ✓ | | | | | | | | |
| Lost update (complex logic, PG/Oracle) | | ✓ | ✓ | | | | | | |
| Lost update (complex logic, MySQL) | | | ✓ | ✓ | | | | | |
| Write skew (rows exist to lock) | | | | | ✓ | ✓ | | | |
| Write skew (phantom, unique claim) | | | | | | ✓ | | ✓ | |
| Write skew (phantom, range/overlap) | | | | | | ✓ | ✓ | | |
| Write skew (Oracle — no true serial.) | | | | | ✓ | — | ✓ | | |
