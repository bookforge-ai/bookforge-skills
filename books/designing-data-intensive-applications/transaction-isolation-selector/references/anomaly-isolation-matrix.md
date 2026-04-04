# Anomaly-to-Isolation Mapping Matrix

Full reference for Step 3 of the transaction-isolation-selector process.

---

## The Matrix

| Anomaly | Read Uncommitted | Read Committed | Snapshot Isolation | Serializable |
|---------|:----------------:|:--------------:|:-----------------:|:------------:|
| Dirty reads | allowed | **prevented** | prevented | prevented |
| Dirty writes | prevented | prevented | prevented | prevented |
| Read skew | allowed | allowed | **prevented** | prevented |
| Lost updates | allowed | allowed | sometimes* | **prevented** |
| Write skew | allowed | allowed | allowed | **prevented** |
| Phantom reads (read-only) | allowed | allowed | **prevented** | prevented |
| Phantom reads (write skew) | allowed | allowed | allowed | **prevented** |

*Snapshot isolation detects lost updates automatically in PostgreSQL and Oracle. MySQL InnoDB does NOT detect them automatically.

**Read this matrix:** Find your worst anomaly exposure. The column where it is first marked "prevented" is your minimum required isolation level.

---

## Per-Cell Explanations

### Dirty Reads

**Read Uncommitted:** Allowed. A transaction can read uncommitted writes from other transactions. If the writing transaction aborts, the reading transaction has acted on data that never existed. Uncommon in production — almost no database defaults to this level.

**Read Committed and above:** Prevented. The database keeps the previously committed value available to readers while a write transaction is in progress. Only when the write commits do readers see the new value. Implementation: most databases use multi-version storage (keeping both old and new values) rather than requiring a read lock on every read.

---

### Dirty Writes

**All levels including Read Uncommitted:** Dirty writes are prevented at every practical isolation level. When transaction A is writing to an object, transaction B must wait until A commits or aborts before writing to the same object. Implementation: row-level write locks held until commit. This is the one anomaly that isolation levels universally prevent.

---

### Read Skew (Nonrepeatable Read)

**Read Committed:** Allowed. A transaction may see different values for the same object across two reads within the same transaction, because a concurrent transaction committed a write between the two reads. Each read is of committed data (no dirty reads), but the data is from different points in time.

**Snapshot Isolation and above:** Prevented. The transaction reads from a consistent snapshot taken at the start of the transaction. All reads within the transaction see the database as it was at that point in time, even if concurrent transactions commit writes in the interim. Implementation: multi-version concurrency control (MVCC) — the database retains multiple versions of each row, tagged with the transaction ID that created them.

**Critically affected operations:**
- Long-running backup processes (reading from multiple tables over minutes or hours)
- Integrity checks and aggregate queries that scan large portions of the database
- Multi-step reads where an early result influences a later query

---

### Lost Updates

**Read Committed:** Allowed unless the application explicitly prevents it. Two concurrent read-modify-write cycles can each read the same value, compute updates independently, and write back — the second write overwrites the first without incorporating it.

**Snapshot Isolation:** Database-dependent.
- **PostgreSQL:** Automatically detects lost updates and aborts the conflicting transaction. The transaction must be retried.
- **Oracle:** Automatically detects lost updates.
- **MySQL InnoDB:** Does NOT automatically detect lost updates. Two concurrent `UPDATE` statements where both read the old value can lose one update silently.
- **SQL Server:** With SNAPSHOT isolation (READ_COMMITTED_SNAPSHOT=ON), detects lost updates.

**Prevention methods below serializable:**
1. Atomic operations: `UPDATE t SET v = v + 1 WHERE k = $1` — no application-layer read-modify-write; the database executes the increment atomically.
2. Explicit locking: `SELECT ... FOR UPDATE` — locks the row on read, blocking concurrent reads until the transaction completes.
3. Compare-and-set: `UPDATE t SET v = $new WHERE k = $1 AND v = $old` — only updates if the value hasn't changed. Caution: may not be safe if the database reads from a snapshot that doesn't reflect the latest committed value.

---

### Write Skew

**Read Committed and Snapshot Isolation:** Allowed. This is the key gap in snapshot isolation. Two transactions each read the same precondition (a count, an existence check, an aggregate), make independent decisions, and write to different objects. Each write is individually valid; together they violate a constraint that neither transaction was aware of being violated.

**Serializable:** Prevented. Serializable isolation detects that the two transactions' reads and writes form a dependency cycle and aborts one of them.

**Why snapshot isolation cannot prevent write skew:**
Snapshot isolation's guarantee is "readers never block writers, writers never block readers." This property is exactly what allows write skew — two readers can observe the same state simultaneously and proceed to write independently. Preventing write skew requires that concurrent writers who read the same precondition be forced into a serial order, which requires either blocking (2PL) or detection-and-abort (SSI).

**Database-specific behavior:**
- Oracle 11g "SERIALIZABLE" = snapshot isolation. Write skew is possible despite the name.
- PostgreSQL REPEATABLE READ = snapshot isolation. Write skew is possible.
- PostgreSQL SERIALIZABLE = SSI = true serializable. Write skew is prevented.
- MySQL InnoDB SERIALIZABLE = 2PL = true serializable. Write skew is prevented.

---

### Phantom Reads

**Two forms with different prevention requirements:**

**Read-only phantom (prevented by snapshot isolation):** A transaction reads a set of rows matching a condition. A concurrent transaction inserts rows matching the same condition. Under read committed, if the first transaction re-executes the query, it sees the new rows. Under snapshot isolation, the first transaction reads from a frozen snapshot — new rows inserted after the snapshot was taken are invisible.

**Write skew phantom (NOT prevented by snapshot isolation):** A transaction reads a set of rows matching a condition (may return empty set), then inserts a row matching that same condition. A concurrent transaction does the same. Both transactions see no conflict; both insert. The concurrent inserts violate a constraint (no double-booking, no duplicate username, etc.).

Snapshot isolation cannot prevent this because:
1. The transactions are reading an empty set — there are no rows to lock with `FOR UPDATE`
2. The writes are inserts — they create new rows that didn't exist when the check ran
3. Snapshot isolation has no mechanism to detect that one transaction's write invalidates another transaction's read premise when the read found nothing

Prevention requires serializable isolation with predicate locks (2PL) or SSI's write-tracking mechanism.

---

## Database Default Isolation Levels

| Database | Default Level | "Repeatable Read" means | "Serializable" means |
|----------|--------------|------------------------|---------------------|
| PostgreSQL | Read committed | Snapshot isolation (MVCC; detects lost updates) | True serializable via SSI (since v9.1) |
| MySQL InnoDB | Repeatable read | Snapshot isolation (MVCC; does NOT detect lost updates automatically) | 2PL (true serializable) |
| Oracle 11g | Read committed | Snapshot isolation (Oracle calls this "serializable") | Not available — "serializable" = snapshot |
| SQL Server | Read committed | Snapshot isolation (if READ_COMMITTED_SNAPSHOT=ON) | 2PL (true serializable) |
| IBM DB2 | Cursor stability (≈ read committed) | Serializable (IBM inverts the term) | Serializable |
| CockroachDB | Serializable | N/A (only level offered) | SSI |
| FoundationDB | Serializable | N/A (only level offered) | SSI |

---

## Minimum Level Required — Decision Table

| Worst anomaly exposure | Minimum required level |
|------------------------|----------------------|
| None (single-user system or no shared data) | None (atomicity sufficient) |
| Dirty reads possible | Read committed |
| Read skew in long-running reads (backups, analytics) | Snapshot isolation |
| Lost updates in read-modify-write cycles | Snapshot isolation (PostgreSQL/Oracle) OR explicit locking (MySQL) |
| Write skew in any transaction | Serializable |
| Write skew phantoms (check-then-insert pattern) | Serializable |
