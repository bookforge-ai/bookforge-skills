# Serializability Implementation Comparison

Reference for Step 4 of the transaction-isolation-selector process. Use when serializable isolation is required and you need to select among the three implementations.

---

## The Three Implementations

| Dimension | Serial Execution | Two-Phase Locking (2PL) | Serializable Snapshot Isolation (SSI) |
|-----------|:----------------:|:----------------------:|:-------------------------------------:|
| **Concurrency model** | None — single thread | Pessimistic — block on conflict | Optimistic — proceed, detect, abort |
| **Throughput ceiling** | Single CPU core / partition | Limited by lock contention | Near-snapshot-isolation throughput |
| **Latency profile** | Very low, very predictable | Unpredictable at high percentiles | Predictable (aborts, not waits) |
| **Read blocking** | All reads serialized | Readers block writers; writers block readers | Readers never block writers |
| **Write blocking** | All writes serialized | Writers block readers and writers | Writers never block readers |
| **Deadlocks** | None (no concurrency) | Common; database auto-detects and aborts | None (optimistic; no locks held) |
| **Abort type** | None | On deadlock detection; requires retry | On serialization violation; requires retry |
| **Long-running reads** | Block all writes on that partition | Block all writes on locked rows | Safe — reads from consistent snapshot |
| **Cross-partition transactions** | ~10–1000x slower | Standard behavior | Standard behavior |
| **Dataset constraint** | Must fit in memory | No constraint | No constraint |
| **Transaction length** | Must be very short (ms) | Short preferred; long causes lock pile-ups | Short preferred; long increases abort risk |
| **Implementation complexity** | Simple (stored procedures required) | Moderate (lock management automatic) | Moderate (retry logic required in app) |
| **Database support** | VoltDB, Redis, Datomic | MySQL InnoDB, SQL Server, DB2 | PostgreSQL >= 9.1, FoundationDB |

---

## When to Use Each

### Serial Execution

Use when:
- The entire active dataset fits in RAM (disk access inside a serial transaction stalls the single thread)
- All transactions are milliseconds-fast (one slow transaction stalls every other transaction)
- Write throughput fits on a single CPU core, OR the data can be cleanly partitioned so most transactions are single-partition
- The application can express transactions as stored procedures submitted as a unit (no interactive client-server round-trips mid-transaction)

Do not use when:
- Transactions involve user interaction (a human deciding mid-transaction)
- Transactions access data not in memory
- Throughput requirements exceed a single core and data cannot be partitioned cleanly
- Transactions span many partitions

**Performance note from Kleppmann:** VoltDB reports single-partition throughput that scales linearly with CPU cores (each core gets its own partition). Cross-partition transactions are "orders of magnitude" slower — approximately 1,000 cross-partition writes/sec regardless of node count.

---

### Two-Phase Locking (2PL)

Use when:
- SSI is not available in the target database (MySQL InnoDB, SQL Server, DB2)
- Workload has moderate concurrency and short transactions
- Read/write contention on the same rows is low to moderate

Do not use when:
- Strict latency SLA (p99 < 10ms) AND high contention — lock wait queues make tail latency unbounded
- Workload has long-running transactions coexisting with short OLTP transactions — one slow transaction's locks stall all others
- Deadlock rate becomes operationally significant — each deadlock requires aborting and retrying a transaction

**Performance characterization from Kleppmann:** 2PL has "significantly worse" throughput and response times than weak isolation. Unstable latencies at high percentiles. Deadlocks frequent under 2PL (more so than under read committed). A slow transaction can cause the "rest of the system to grind to a halt."

**2PL lock mechanics:**
- Shared lock (read): multiple transactions can hold simultaneously; exclusive lock by any transaction blocks all
- Exclusive lock (write): blocks all readers and all writers
- Upgrade: transaction that reads then writes upgrades shared → exclusive
- Lock held until: commit or abort (both phases — acquire throughout, release at end)
- Predicate locks: prevent phantoms by locking a search condition (e.g., "all bookings for room 123 between noon and 1pm"), not just specific rows
- Index-range locks: practical approximation of predicate locks; attaches shared lock to an index range; slightly over-locks but much lower overhead

---

### Serializable Snapshot Isolation (SSI)

Use when:
- The database supports SSI (PostgreSQL >= 9.1, FoundationDB)
- Workload is read-heavy — SSI's "readers never block writers" property makes read throughput nearly identical to snapshot isolation
- Contention between transactions is low to moderate — high contention causes high abort rates and retry overhead
- Transactions are short — long-running transactions accumulate more read/write tracking overhead and conflict with more concurrent transactions

Do not use when:
- The database does not support SSI
- The application cannot implement retry logic — SSI aborts at commit time with a serialization failure error (SQLSTATE 40001); the transaction must be retried from scratch
- Workload has very high contention (many concurrent writes to the same rows) — abort rate becomes high enough to dominate throughput

**SSI mechanics from Kleppmann:**
SSI detects two patterns that indicate a serialization conflict:

1. **Detecting stale MVCC reads:** When transaction B commits, SSI checks whether any in-flight transaction read data that B modified (a write that was uncommitted when the read occurred). If so, the reading transaction's premise may be outdated, and it is aborted at commit time.

2. **Detecting writes that affect prior reads:** SSI tracks which transactions have read which key ranges (similar to index-range locks but non-blocking — they act as tripwires). When transaction B writes, it checks the tripwires to see if any concurrent transaction read the affected data. If so, SSI notifies those transactions that their read may be outdated. If the conflicting write commits before the reading transaction, the reader must abort.

**SSI vs 2PL key difference:** 2PL blocks — a transaction waits for a lock. SSI notifies and aborts — a transaction proceeds and is checked at commit time. Under SSI, read-only transactions never need to abort (they do not write; no serialization violation is possible). This makes SSI particularly attractive for mixed read-write and analytics workloads.

**PostgreSQL SSI since v9.1:** PostgreSQL uses theory from Michael Cahill's PhD thesis (2008) to reduce unnecessary aborts — it can sometimes prove that a conflict would not actually violate serializability and allow the transaction to commit. This reduces the abort rate below what a naive SSI implementation would produce.

---

## Abort / Retry Requirements

Both 2PL (on deadlock) and SSI (on serialization conflict) require the application to retry transactions. This is not automatic in most frameworks.

**Conditions that require retry (OK to retry):**
- Deadlock detected (2PL): retry the aborted transaction
- Serialization failure (SSI, SQLSTATE 40001): retry the entire transaction from the beginning
- Transient network errors

**Conditions that do NOT warrant retry:**
- Constraint violations (duplicate key, foreign key failure): a retry without changing the data will fail again
- Business logic errors (insufficient balance): a retry will produce the same result
- Permanent errors

**ORM framework warning:** Rails' ActiveRecord and Django's ORM do not retry aborted transactions by default. A serialization failure typically bubbles up as an exception to the user. Applications that adopt SSI must implement explicit retry loops around transaction boundaries. The retry must re-execute the entire transaction (re-read all data, not reuse cached reads from the first attempt).

**Retry pattern:**

```python
MAX_RETRIES = 5
for attempt in range(MAX_RETRIES):
    try:
        with connection.transaction(isolation="serializable"):
            # All reads and writes here
            result = perform_transaction()
        break  # Success — exit retry loop
    except SerializationFailure:
        if attempt == MAX_RETRIES - 1:
            raise  # Give up after MAX_RETRIES
        continue  # Retry from scratch
```

---

## Decision Tree

```
Serializable isolation is required.

Q1: Does the database support SSI?
    (PostgreSQL >= 9.1, FoundationDB)
    → No: Go to Q3

Q2: Is the workload read-heavy with low-to-moderate contention?
    → Yes: Use SSI
    → No (high contention, many aborts expected): Go to Q3

Q3: Is the dataset in memory, throughput fits a single core,
    and transactions are short stored procedures?
    → Yes: Use Serial Execution
    → No: Use Two-Phase Locking (2PL)

Q4 (after selecting 2PL): Is there a strict latency SLA with high contention?
    → Yes: Consider partitioning the data to enable per-partition serial execution,
      OR accept SSI with retry overhead as the lesser of two evils,
      OR narrow the serializable scope to specific high-risk transactions only
      and use explicit SELECT FOR UPDATE elsewhere
```
