# Isolation Anomaly Matrix Reference

Source: Patterns of Enterprise Application Architecture, Chapter 5 (Fowler et al., 2002)

---

## Table 5.1 — Isolation Levels and the Anomalies They Allow

| Isolation Level | Dirty Read | Unrepeatable Read | Phantom Read |
|---|---|---|---|
| Read Uncommitted | Possible | Possible | Possible |
| Read Committed | Prevented | Possible | Possible |
| Repeatable Read | Prevented | Prevented | Possible |
| Serializable | Prevented | Prevented | Prevented |

**Note:** Lost Update is not an anomaly class in the SQL standard (it is a write-write conflict, not a read anomaly), but it is the most common application-layer bug. It can occur at any isolation level when a read-modify-write pattern is used without an explicit optimistic or pessimistic check. Read Committed does not prevent Lost Update by itself — the application must use a version check (Optimistic Offline Lock) or SELECT FOR UPDATE / NOWAIT.

---

## Anomaly Definitions

### Dirty Read
A transaction reads data written by another transaction that has NOT yet committed. Two failure modes:
1. Read mid-update state — the in-flight transaction has partially modified the data.
2. Read rolled-back data — the in-flight transaction later rolls back, so the data read was never "real."

**Prevented at:** Read Committed, Repeatable Read, Serializable.
**Permitted at:** Read Uncommitted only.

**Practical impact:** Only relevant if you explicitly configure Read Uncommitted. Most databases default to Read Committed or higher.

---

### Unrepeatable Read (Non-Repeatable Read / Inconsistent Read)
Within a single transaction, reading the same row twice returns different values because another transaction committed an update between the two reads.

**Permitted at:** Read Committed, Read Uncommitted.
**Prevented at:** Repeatable Read, Serializable.

**Practical impact:** Default setting in PostgreSQL (READ COMMITTED) allows this. A transaction that reads a customer's address at the start of a long computation and relies on that value not changing can get a different value if it re-reads after another session edits the customer.

**Application-level fix options:**
- Raise isolation to Repeatable Read or Serializable for transactions that need stable reads.
- Use Optimistic Offline Lock (version check) across the whole business transaction.
- Read the value once and pass it through the computation without re-reading.

---

### Phantom Read
Within a single transaction, executing the same range query (WHERE clause over multiple rows) twice returns different row sets because another transaction inserted or deleted matching rows between the two queries.

**Permitted at:** Repeatable Read, Read Committed, Read Uncommitted.
**Prevented at:** Serializable only.

**Practical impact:** Financial aggregate reports, inventory counts, or range-based validation rules run inside a transaction can produce phantom-affected totals if another transaction inserts or deletes matching rows concurrently.

**Application-level fix options:**
- Raise isolation to Serializable for the specific transaction that needs range consistency.
- Use Snapshot Isolation (available in PostgreSQL, SQL Server) as a practical approximation of Serializable with better throughput.
- Execute the range query once, hold results in application memory, avoid re-querying.

---

### Lost Update (Write-Write Conflict)
Two transactions each read the same record, compute changes based on the stale read, and then write back. The second writer overwrites the first writer's changes. The first writer's update is silently discarded.

**Not in the SQL standard anomaly table.** Occurs at any isolation level without write-conflict detection.

**Detection patterns in code:**
```
# Pattern 1: read-then-write with no version check
item = db.query("SELECT * FROM inventory WHERE id=?", id)
item.quantity -= ordered
db.execute("UPDATE inventory SET quantity=? WHERE id=?", item.quantity, id)
# ^ Lost Update if another transaction reads the same row before this writes
```

**Prevented by:**
- `SELECT FOR UPDATE` — acquires a row-level exclusive lock at read time (pessimistic).
- Version column optimistic check:
  ```sql
  UPDATE inventory SET quantity=?, version=version+1
  WHERE id=? AND version=?   -- fails if another writer committed first
  ```
- Application-level Optimistic Offline Lock (version column per entity).
- Serializable isolation with database-enforced write conflict detection.

---

## Isolation Level Default by Database

| Database | Default Isolation Level |
|---|---|
| PostgreSQL | Read Committed |
| MySQL (InnoDB) | Repeatable Read |
| SQL Server | Read Committed (or Read Committed Snapshot if RCSI is on) |
| Oracle | Read Committed |
| SQLite | Serializable (exclusive writes) |

Most production enterprise applications run on a database defaulting to **Read Committed**, which permits Unrepeatable Reads, Phantoms, and Lost Updates.

---

## Isolation vs Immutability

Fowler explicitly names immutability as an alternative concurrency-control strategy: "You only get concurrency problems if the data you're sharing can be modified." If a dataset is read-only (or write-once), any isolation level is safe for readers. Read replicas, event-sourced event logs, and CQRS read models exploit this: the read side has no concurrency problems because it only reads from an immutable-once-projected view.

**Practical rule:** Before raising isolation level, ask: "Can I make this data immutable or read from a snapshot?" That eliminates the problem rather than managing it.

---

## Business Transaction vs System Transaction ACID

A **system transaction** is a BEGIN/COMMIT block managed by the database. It provides ACID natively.

A **business transaction** spans multiple user interactions (multiple HTTP requests, multiple system transactions). The database provides no ACID guarantee across requests.

| ACID Property | System Transaction | Business Transaction (application responsibility) |
|---|---|---|
| Atomicity | DB rollback on error | Saga / compensation / undo workflow |
| Consistency | Schema constraints + triggers | Business-rule invariant checks at each commit |
| Isolation | Isolation level setting | Optimistic Offline Lock / Pessimistic Offline Lock |
| Durability | WAL + fsync + replication | Inherited from system transactions (all steps must commit) |

See: `offline-concurrency-strategy-selector` for selecting between Optimistic and Pessimistic Offline Lock for business-transaction isolation.

---

## Long-Transaction Risks at High Isolation Levels

Running a long-running computation under Repeatable Read or Serializable does not just affect throughput — it holds row-level locks (or a read snapshot) that can:
1. Block concurrent writers (Repeatable Read with locking).
2. Accumulate snapshot overhead until commit (MVCC-based Serializable).
3. Trigger lock escalation to table-level if many rows are locked simultaneously.

**Fowler's warning on lock escalation:** Avoid tables that are shared by many objects (e.g., a Layer Supertype object table). These become lock escalation candidates under high-isolation long transactions, shutting all writers out.

**Recommended practice:** Use the minimum isolation level that prevents the specific anomaly you're protecting against. Use Serializable only for transactions that truly need serializability (range scans with correctness requirements). Keep all long computations outside the transaction boundary where possible.
