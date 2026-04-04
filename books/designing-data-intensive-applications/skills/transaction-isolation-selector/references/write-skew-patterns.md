# Write Skew Patterns

Reference for Step 2 of the transaction-isolation-selector process. Use when diagnosing whether a specific transaction pattern is vulnerable to write skew.

---

## Write Skew Detection Checklist

A transaction is vulnerable to write skew if ALL of the following are true:

- [ ] The transaction executes a SELECT query that checks a condition (count, existence, sum, aggregate)
- [ ] Application code makes a decision based on the result of that query
- [ ] The transaction executes a write (INSERT, UPDATE, or DELETE) based on that decision
- [ ] The write changes data that affects the condition checked in the SELECT
- [ ] Another transaction could execute the same pattern concurrently

**If all five are true:** The transaction is vulnerable to write skew. Snapshot isolation will not prevent it. Serializable isolation is required, or explicit `SELECT FOR UPDATE` can be used as a mitigation when the rows being checked exist in advance.

**The phantom variant:** If the write is an INSERT (adding a new row that matches the checked condition), there are no rows to lock with `SELECT FOR UPDATE`. Only serializable isolation prevents this form.

---

## The 5 Write Skew Patterns

### Pattern 1: At-Least-One Constraint

**Description:** A resource requires at least one unit to remain active. Concurrent transactions each verify the count is >= 2 (safe to remove one), then each remove one.

**Domain examples:**
- Hospital: at least one doctor on call per shift
- Customer support: at least one agent assigned to a support queue
- Infrastructure: at least one replica must remain running

**Transaction structure:**
```sql
BEGIN;
SELECT COUNT(*) FROM doctors
  WHERE on_call = true AND shift_id = $shift_id;
-- Application checks: if count >= 2, proceed
UPDATE doctors SET on_call = false
  WHERE name = $doctor AND shift_id = $shift_id;
COMMIT;
```

**Race condition:** Two concurrent transactions both read count = 2. Both proceed. Both update their own row. Count becomes 0.

**Under snapshot isolation:** Both transactions read from their own consistent snapshot showing count = 2. Both see a valid precondition. Both commit. The combined result violates the constraint.

**Mitigation (without serializable):**
```sql
SELECT COUNT(*) FROM doctors
  WHERE on_call = true AND shift_id = $shift_id
  FOR UPDATE;
```
This locks all on-call rows for the shift. A second concurrent transaction must wait for the first to commit before it can read the count. After the first commits (count = 1), the second reads count = 1 and aborts.

**Mitigation limitation:** `FOR UPDATE` on a COUNT query locks every row returned. If the shift has 50 doctors on call, this locks all 50 rows for the duration of the transaction. Consider whether this lock scope is acceptable.

---

### Pattern 2: No-Overlap Constraint

**Description:** Resources must not overlap in some dimension (time, space, ID range). A transaction checks for absence of overlap, then inserts a non-overlapping resource.

**Domain examples:**
- Meeting room booking: no two bookings for the same room in the same time window
- Flight seat assignment: no two passengers assigned the same seat
- IP address allocation: no two servers assigned the same IP

**Transaction structure:**
```sql
BEGIN;
SELECT COUNT(*) FROM bookings
  WHERE room_id = $room AND
        end_time > $start AND start_time < $end;
-- Application checks: if count = 0, proceed
INSERT INTO bookings (room_id, start_time, end_time, user_id)
  VALUES ($room, $start, $end, $user);
COMMIT;
```

**Race condition:** Two transactions both query count = 0 for the same room and time range. Both insert a booking. Result: double-booked room.

**Under snapshot isolation:** Both transactions read from consistent snapshots that do not include each other's in-flight insert. Both see count = 0. Both insert. Both commit.

**Why `FOR UPDATE` does not help:** The SELECT returns zero rows (no conflicts found). `FOR UPDATE` on an empty result set locks nothing — there are no rows to lock. This is the phantom variant of write skew.

**Mitigation (without serializable):**
- **Materializing conflicts:** Create a table of time slots ahead of time (e.g., 15-minute slots for each room for the next 6 months). Lock the relevant slots with `SELECT FOR UPDATE` before checking for conflicts. Ugly but functional.
- **Unique constraint:** If bookings can be modeled as discrete units (e.g., seat numbers), a UNIQUE constraint on (room_id, seat_number) allows the database to enforce no-overlap with a constraint violation rather than application logic.
- **Serializable isolation:** The clean solution.

---

### Pattern 3: Unique Claim

**Description:** A user claims a unique resource (username, identifier, role). The transaction checks for non-existence, then creates the claim.

**Domain examples:**
- Username registration: check username not taken, then create account
- Document lock: check document not locked, then lock it
- Prize claim: check prize not claimed, then record claim

**Transaction structure:**
```sql
BEGIN;
SELECT COUNT(*) FROM users WHERE username = $name;
-- Application checks: if count = 0, proceed
INSERT INTO users (username, email, ...) VALUES ($name, $email, ...);
COMMIT;
```

**Race condition:** Two concurrent registrations for the same username both see count = 0 and both insert. Result: two accounts with the same username.

**Mitigation:** A UNIQUE constraint on the `username` column is the correct solution here. The second INSERT will fail with a constraint violation. This is one case where a database constraint can enforce the invariant without requiring serializable isolation.

**Rule of thumb:** If the write skew pattern involves inserting a single "canonical" value that must be globally unique, a UNIQUE constraint is the right tool. If the constraint is more complex (involving multiple rows or aggregates), serializable isolation is needed.

---

### Pattern 4: Budget / Sum Constraint

**Description:** The sum of some values must remain within a bound (positive, below a limit). A transaction reads the current sum, verifies the constraint is not violated, then adds a new value.

**Domain examples:**
- Spending limit: verify total spending + new purchase <= credit limit
- Inventory allocation: verify allocated units + new allocation <= available stock
- Double-spend prevention: verify account balance + new spend >= 0

**Transaction structure:**
```sql
BEGIN;
SELECT SUM(amount) FROM spending WHERE user_id = $user;
-- Application checks: if sum + new_amount <= limit, proceed
INSERT INTO spending (user_id, amount, description)
  VALUES ($user, $new_amount, $desc);
COMMIT;
```

**Race condition:** Two concurrent purchases both read sum = $900 against a $1000 limit. Both see $900 + $150 = $1050 > $1000 would fail, but $900 + $80 = $980 is fine. Wait — both try to spend $80. Both read $900. Both see $900 + $80 = $980 <= $1000. Both insert. Total spending becomes $1060 — over the limit.

**Under snapshot isolation:** Both read from snapshots that predate each other's insert. Both see $900. Both pass the constraint check. Both insert.

**Mitigation (without serializable):**
```sql
SELECT SUM(amount) FROM spending
  WHERE user_id = $user FOR UPDATE;
```
Locks all spending rows for the user. A second concurrent transaction must wait. After the first commits, the second reads the updated sum. This works because the rows being aggregated exist (they're the user's existing spending records). The new INSERT is what creates the problem — the aggregate includes existing rows, which can be locked.

**Note:** This is the case where `FOR UPDATE` works on a write skew pattern because the read is over existing rows (not checking for absence of rows).

---

### Pattern 5: Game / Validity State

**Description:** A transition is valid only if the current state satisfies some condition. Multiple transactions each verify validity and each apply a transition to different parts of the state.

**Domain examples:**
- Chess: verify a move is valid (piece at correct position, move is legal), then update piece position
- Workflow: verify a document is in the correct state (e.g., "draft"), then transition it to "review"
- Two-player resource allocation: verify total allocations <= capacity, then add one allocation each

**Transaction structure:**
```sql
BEGIN;
SELECT position FROM figures
  WHERE name = $piece AND game_id = $game;
-- Application validates move legality based on position
UPDATE figures SET position = $new_position
  WHERE name = $piece AND game_id = $game;
COMMIT;
```

**Race condition:** Two concurrent moves to different pieces both pass validity checks based on the game state at the time of their read. One move makes another move's precondition invalid, but neither transaction sees the other's write.

**Mitigation (without serializable):**
```sql
SELECT * FROM figures
  WHERE name = $piece AND game_id = $game
  FOR UPDATE;
```
Locks the specific piece being moved. If validity depends on other pieces' positions, those must also be locked with `FOR UPDATE`. This works when the rows being checked exist. The chess example in Kleppmann uses this approach for the specific piece being moved — but two players moving different pieces to the same square requires serializable isolation or a unique constraint on (game_id, position).

---

## SQL Pattern Reference

### When SELECT FOR UPDATE Works

`FOR UPDATE` is effective when:
- The rows checked in the precondition SELECT exist in the database
- The write updates those same rows (or rows locked by the same query)
- The transaction is not checking for the absence of rows

```sql
-- WORKS: Lock specific rows that exist
SELECT * FROM doctors WHERE on_call = true AND shift_id = $shift FOR UPDATE;
UPDATE doctors SET on_call = false WHERE name = $name;

-- WORKS: Lock an aggregate over existing rows
SELECT SUM(amount) FROM spending WHERE user_id = $user FOR UPDATE;
INSERT INTO spending (user_id, amount) VALUES ($user, $amount);
```

### When SELECT FOR UPDATE Does NOT Work

`FOR UPDATE` does not prevent write skew when:
- The SELECT returns no rows (checking for absence)
- The write is an INSERT that creates a new row matching the checked condition

```sql
-- DOES NOT WORK: Checking for absence, inserting if absent
SELECT COUNT(*) FROM bookings
  WHERE room_id = $room AND overlap($start, $end) FOR UPDATE;
-- If count = 0, there are no rows to lock
INSERT INTO bookings (...) VALUES (...);
```

### Serializable Setting by Database

```sql
-- PostgreSQL
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- or: SET default_transaction_isolation = 'serializable';

-- MySQL
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- or: SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- SQL Server
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Oracle: not available as true serializable — use application-level locking
-- Oracle's SERIALIZABLE = snapshot isolation (write skew still possible)
```

### Application Retry for SSI Aborts (PostgreSQL)

```python
import psycopg2
from psycopg2 import errors

def execute_with_retry(conn, transaction_fn, max_retries=5):
    for attempt in range(max_retries):
        try:
            with conn.cursor() as cur:
                cur.execute("BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE")
                result = transaction_fn(cur)
                conn.commit()
                return result
        except errors.SerializationFailure:
            conn.rollback()
            if attempt == max_retries - 1:
                raise RuntimeError("Transaction failed after max retries")
            continue
        except Exception:
            conn.rollback()
            raise
```
