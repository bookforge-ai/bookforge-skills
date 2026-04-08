---
name: transaction-isolation-selector
description: |
  Choose the correct transaction isolation level and serializability implementation for an application's concurrency patterns. Use when: selecting an isolation level for a new system; evaluating whether read committed or snapshot isolation is safe for your access patterns; deciding whether to upgrade to serializable and choosing between two-phase locking (2PL) vs. serializable snapshot isolation (SSI); producing an architecture decision record for isolation level choice; or explaining to a team why the database default is insufficient. Distinct from concurrency-anomaly-detector (which scans code for exposed anomalies) — this skill selects the level, not the bugs. Covers PostgreSQL, MySQL InnoDB, Oracle, SQL Server, and distributed databases. Applies a 6-anomaly × 4-isolation-level mapping matrix (dirty read, dirty write, read skew, lost update, write skew, phantom read vs. read uncommitted, read committed, snapshot isolation, serializable) to produce a concrete recommendation with implementation trade-off analysis. Works on any codebase, schema, or workload description.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/transaction-isolation-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [7]
tags: [transactions, isolation-levels, serializability, snapshot-isolation, read-committed, write-skew, phantom-reads, lost-updates, dirty-reads, mvcc, two-phase-locking, serializable-snapshot-isolation, concurrency, race-conditions, postgresql, mysql, oracle, sql-server, acid, database-selection]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application codebase, schema files, docker-compose, or architecture description — any artifact that reveals data access patterns and transaction boundaries"
    - type: document
      description: "Workload description or requirements document if no codebase is available"
  tools-required: [Read, Write, Grep]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory where codebase or configuration files exist. Falls back to document/description input if no codebase."
discovery:
  goal: "Identify the minimum safe isolation level for the application's concurrency patterns and produce a concrete recommendation with implementation trade-off analysis"
  tasks:
    - "Identify which of the 6 concurrency anomalies the application is exposed to"
    - "Map those anomalies to the minimum isolation level that prevents them"
    - "Assess performance requirements to select among serializability implementations if serializable is indicated"
    - "Identify the database in use and its actual default isolation level"
    - "Flag write skew exposure — the most commonly missed anomaly"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "tech-lead", "site-reliability-engineer"]
    experience: "intermediate-to-advanced — assumes experience with relational databases and SQL transactions"
  triggers:
    - "User is choosing an isolation level for a new service or database"
    - "User has a concurrency bug and suspects a race condition in their transactions"
    - "User wants to understand whether their database's default is safe for their workload"
    - "User is migrating from one database to another and needs to verify isolation equivalence"
    - "User needs to justify an isolation choice in an architecture decision record"
    - "User suspects write skew but isn't sure how to detect or prevent it"
    - "User wants to evaluate serializable snapshot isolation vs two-phase locking"
  not_for:
    - "Distributed transaction coordination across multiple databases — use two-phase commit analysis (Ch 9)"
    - "Choosing between replication consistency models (eventual vs linearizable) — use consistency-model-selector"
    - "Selecting a storage engine — use storage-engine-selector"
---

# Transaction Isolation Selector

## When to Use

You have a database with concurrent transaction access and need to choose the right isolation level — or you suspect an existing isolation level is inadequate for your concurrency patterns.

This skill applies when any of the following are true:
- You are building a new service and need to decide what isolation level to configure
- You have a bug that appears nondeterministically and involves concurrent reads and writes
- You are migrating to a new database and need to verify the isolation guarantees are equivalent
- Your application touches multiple rows or tables within a single transaction
- Your business logic reads a value and then conditionally writes based on it (the write skew pattern)

**Critical default:** Most databases do NOT default to serializable isolation. Oracle 11g does not implement true serializable at all — its "serializable" level is actually snapshot isolation. PostgreSQL defaults to read committed. MySQL InnoDB defaults to repeatable read (which is snapshot isolation in MySQL's implementation). If you have not explicitly set your isolation level, you are running at a weaker level than serializable, and some anomalies are possible.

**Related skills:**
- `concurrency-anomaly-detector` — if you already have a bug and need to identify the anomaly type
- `consistency-model-selector` — for distributed system consistency guarantees (linearizability, eventual consistency)

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Database in use and its version.** Why: The same isolation level name means different things in different databases. Oracle's "serializable" is snapshot isolation. PostgreSQL's "repeatable read" is snapshot isolation. MySQL's "repeatable read" does not detect lost updates automatically. Without knowing the database, the isolation level name alone is meaningless.
  - Check environment for: `docker-compose.yml` (database service images), `requirements.txt` / `pom.xml` / `package.json` (database driver), schema files (database-specific syntax)
  - If still missing, ask: "What database are you using, and what version?"

- **Transaction boundaries and what they read/write.** Why: Isolation level requirements are determined by what transactions do — specifically whether they read a value and then write based on what they read. A transaction that only does blind writes (INSERT without a preceding SELECT) has different requirements than one that does SELECT then UPDATE.
  - Check environment for: application code (look for BEGIN TRANSACTION / BEGIN / with transaction context managers); ORM code (look for @Transactional, session.begin()); look for read-then-write patterns (SELECT followed by UPDATE or INSERT in the same function)
  - If still missing, ask: "Can you describe a typical transaction your application performs? For example: 'we read an account balance, check if it's positive, then deduct an amount.'"

- **Concurrency pattern — how many concurrent users or processes access the same data.** Why: Anomalies only occur under concurrent access. A single-user system with no concurrency has no isolation requirements beyond atomicity. A high-concurrency system where many transactions access the same rows needs strong isolation.
  - Check environment for: architecture descriptions (number of instances/workers), load testing configs, queue worker counts
  - If still missing, ask: "Is this data accessed by a single process at a time, or by multiple concurrent users or worker processes?"

- **Performance requirements.** Why: Serializable isolation is the safest choice but has a performance cost. The choice between serializability implementations (serial execution, two-phase locking, serializable snapshot isolation) depends heavily on transaction throughput requirements and whether workloads are read-heavy or write-heavy.
  - Check environment for: SLA definitions (requirements.md, architecture.md), load test results, existing query timeout configurations
  - If still missing, ask: "Are there throughput or latency requirements? For example, transactions per second, or p99 latency SLA?"

### Observable Context (gather from environment)

- **Existing isolation level configuration.** Look for `SET TRANSACTION ISOLATION LEVEL`, `transaction_isolation` config vars, ORM transaction settings, or database configuration files. If already set, assess whether it is sufficient.
- **Read-then-write patterns.** Grep for: SELECT followed by UPDATE/INSERT/DELETE in the same transaction scope; ORM patterns like `find_then_update`; check-and-set patterns; aggregate queries (COUNT, SUM) used as a guard before a write.
- **Multi-object transactions.** Look for transactions that touch more than one table or row. Single-object transactions have simpler isolation requirements than multi-object ones.
- **Long-running transactions.** Look for background jobs, batch jobs, or backup processes that hold transactions open for minutes. These are particularly sensitive to read skew.

### Default Assumptions

When context cannot be observed and asking would be excessive:
- Database isolation level unknown → assume read committed (PostgreSQL/Oracle/SQL Server default); note this assumption explicitly
- Transaction length unknown → assume short OLTP transactions (< 1 second)
- Throughput requirements unknown → assume moderate concurrency; do not pre-optimize away serializable
- Write pattern unknown → assume read-then-write patterns exist (conservative); flag for user confirmation

---

## Process

### Step 1: Identify the Database Default and Current Isolation Level

**ACTION:** Determine what isolation level the database is actually operating at — not what is assumed.

**WHY:** The most common root cause of concurrency bugs is assuming the database provides stronger guarantees than it does. "We use PostgreSQL so we're ACID-compliant" is true for atomicity and durability but does not mean serializable isolation. PostgreSQL defaults to read committed, which allows read skew and does not prevent write skew or phantom reads. Establishing the actual current level — not the desired level — is the necessary starting point.

Check and record:

```
Database:            [PostgreSQL | MySQL InnoDB | Oracle | SQL Server | other]
Actual default:      [read uncommitted | read committed | snapshot isolation | serializable]
Current setting:     [check docker-compose, app config, ORM settings, database session config]
```

**Default isolation levels by database (as of Kleppmann's analysis):**

| Database | Default Isolation Level | Notes |
|----------|------------------------|-------|
| PostgreSQL | Read committed | "Repeatable read" = snapshot isolation. "Serializable" = true SSI (since v9.1). |
| MySQL InnoDB | Repeatable read | MySQL's repeatable read does NOT automatically detect lost updates. Not the same as PostgreSQL's snapshot isolation. |
| Oracle 11g | Read committed | "Serializable" = snapshot isolation. True serializable is not available. |
| SQL Server | Read committed | Snapshot isolation available with READ_COMMITTED_SNAPSHOT=ON. |
| DB2 | Cursor stability (≈ read committed) | "Repeatable read" = serializable in IBM's terminology — opposite of everyone else. |

---

### Step 2: Map the Application's Transaction Patterns to Anomaly Exposure

**ACTION:** For each significant transaction type in the application, identify which of the 6 concurrency anomalies it is exposed to.

**WHY:** Not every application needs serializable isolation. The 6 anomalies exist on a spectrum of severity and commonality. Dirty reads and dirty writes are rare and catastrophic; write skew is subtle and frequently missed; phantom reads matter only in specific patterns. Identifying which anomalies are actually possible in your access patterns lets you select the minimum sufficient isolation level rather than defaulting to either "use serializable always" (overly conservative) or "read committed is fine" (frequently wrong). The minimum sufficient level is the correct engineering answer.

**The 6 anomalies and what they require to occur:**

| Anomaly | What must be true for it to occur | What it looks like |
|---------|----------------------------------|--------------------|
| **Dirty read** | Transaction A reads uncommitted writes from transaction B, then B aborts | Application sees data that was never actually committed — "phantom" changes that disappear |
| **Dirty write** | Transaction A overwrites uncommitted writes from transaction B | Two concurrent writes to the same object mix their results; for example, car sale listing shows one buyer but invoice shows another |
| **Read skew (nonrepeatable read)** | Transaction reads same data twice; a concurrent write commits between the two reads | Bank transfer example: Alice reads account 1 ($500) before transfer, account 2 ($400) after transfer — total appears as $900 not $1000 |
| **Lost update** | Two transactions do read-modify-write cycles concurrently; one's write overwrites the other's | Counter increment race: both read 42, both write 43, result is 43 instead of 44 |
| **Write skew** | Two transactions read overlapping data, each makes a decision based on the read, each writes to disjoint objects | Doctor on-call: both doctors see 2 on-call, both go off-call, result is 0 doctors on call |
| **Phantom read** | Transaction reads a set of objects matching a condition; concurrent transaction inserts/deletes a row matching that condition | Booking system: check shows no conflicts, insert succeeds; concurrent check also shows no conflicts, concurrent insert also succeeds — double-booking |

**Write skew detection checklist** (the most commonly missed anomaly):

A transaction is vulnerable to write skew if ALL of the following are true:
1. It reads one or more rows matching some condition
2. It makes a decision based on the result of that read
3. It writes to the database (INSERT, UPDATE, or DELETE) based on that decision
4. The write changes the precondition that was checked in step 1
5. Another transaction could do the same thing concurrently

**Common write skew patterns by domain:**

| Pattern | Example | Risk |
|---------|---------|------|
| At-least-one constraint | Doctor on-call: check count >= 1, then remove self | Two concurrent removals both pass the check, both remove |
| No-overlap constraint | Meeting room booking: check no conflicts, then insert booking | Two concurrent bookings both pass the check, both insert |
| Unique-per-user constraint | Username claim: check username not taken, then insert user | Two concurrent registrations both pass, both insert |
| Budget constraint | Spending check: verify sum remains positive, then insert spend | Two concurrent spends both see positive sum, both insert — total goes negative |
| Game state validity | Chess: check move is valid, then update position | Two concurrent moves to the same position both pass validity |

---

### Step 3: Apply the Anomaly-to-Isolation Mapping Matrix

**ACTION:** For each identified anomaly exposure, determine the minimum isolation level that prevents it.

**WHY:** Isolation levels exist on a spectrum where each level prevents some anomalies and allows others. The correct level is the minimum one that prevents all anomalies the application is actually exposed to. Choosing a weaker level than necessary risks data corruption; choosing a stronger level than necessary incurs unnecessary performance cost. The mapping matrix makes this selection systematic rather than intuitive.

**The anomaly-to-isolation mapping matrix:**

| Anomaly | Read Uncommitted | Read Committed | Snapshot Isolation | Serializable |
|---------|:----------------:|:--------------:|:-----------------:|:------------:|
| Dirty reads | allowed | **prevented** | prevented | prevented |
| Dirty writes | prevented | prevented | prevented | prevented |
| Read skew | allowed | allowed | **prevented** | prevented |
| Lost updates | allowed | allowed | sometimes* | **prevented** |
| Write skew | allowed | allowed | allowed | **prevented** |
| Phantom reads | allowed | allowed | partially** | **prevented** |

*PostgreSQL and Oracle automatically detect lost updates in snapshot isolation. MySQL InnoDB does NOT.

**Snapshot isolation prevents straightforward phantom reads but NOT phantoms that cause write skew.** A phantom in a read-only query (e.g., a backup scan) is prevented by snapshot isolation. A phantom in a read-write transaction where the phantom affects a write decision (the write skew pattern) is NOT prevented by snapshot isolation — serializable isolation is required.

**Reading the matrix:**
- Find the highest-severity anomaly your application is exposed to (rows are ordered from least to most severe in terms of "hardest to prevent")
- The minimum isolation level is the column where that anomaly is first marked "prevented"
- If multiple anomalies are present, take the maximum (most restrictive) required level

**Decision summary:**

```
Exposed to dirty reads only          → Read committed is sufficient
Exposed to read skew                 → Snapshot isolation is the minimum
Exposed to lost updates              → Snapshot isolation (PostgreSQL/Oracle) or
                                       explicit locking (MySQL); verify database behavior
Exposed to write skew or phantoms    → Serializable is required; no weaker level prevents these
```

---

### Step 4: If Serializable Is Required — Select an Implementation

**ACTION:** If Step 3 indicates serializable isolation is required, select among the three implementation approaches using the table and decision tree below.

**WHY:** Serializable isolation has a reputation for being unusably slow — this comes from two-phase locking (2PL), the only option for decades. Two newer approaches (serial execution and SSI) have very different profiles. The choice between them is the difference between "blocking all reads when a write is in progress" and "reads and writes never block each other." Selecting the wrong implementation is the primary reason teams unnecessarily abandon correctness for performance.

| Implementation | Key property | Use when | Do not use when |
|----------------|-------------|----------|-----------------|
| **Serial Execution** | No concurrency — one thread, serial order | Dataset in memory; transactions < 10ms; throughput fits a single core; stored procedures only | Long transactions; disk I/O in transactions; cross-partition coordination at scale |
| **Two-Phase Locking (2PL)** | Pessimistic — readers block writers, writers block readers | SSI unavailable (MySQL, SQL Server, DB2); moderate concurrency; low contention | Strict latency SLA with high contention; long + short transactions coexist |
| **Serializable Snapshot Isolation (SSI)** | Optimistic — proceed, detect conflicts at commit, abort if needed | Read-heavy; low-to-moderate contention; PostgreSQL >= 9.1 or FoundationDB | High contention (abort rate dominates); app cannot implement retry logic |

**Decision tree:**
```
Dataset in memory + transactions < 10ms + stored procedures?
  → Yes: Serial Execution (VoltDB, Redis, Datomic)

Database supports SSI + workload read-heavy + low-moderate contention?
  → Yes: SSI (PostgreSQL SERIALIZABLE, FoundationDB)
  → No: Two-Phase Locking (MySQL SERIALIZABLE, SQL Server SERIALIZABLE)
```

**SSI requirement:** Application must implement retry logic. SSI aborts transactions at commit time with SQLSTATE 40001. The entire transaction must be re-executed from scratch. ORM frameworks do not retry by default.

See `references/serializability-implementation-comparison.md` for full per-implementation detail, performance profiles, and retry patterns.

---

### Step 5: Check for the Naming Trap

**ACTION:** Verify that the isolation level name used in the database matches the actual guarantee, not just the name.

**WHY:** The SQL standard's isolation level definitions are ambiguous and inconsistently implemented. Different databases use the same names to mean different things. A team that sets `SERIALIZABLE` in Oracle 11g believes they have full serializability but actually has snapshot isolation — write skew is still possible. A team using `REPEATABLE READ` in MySQL believes they have the same guarantee as PostgreSQL's repeatable read but MySQL's implementation does not automatically detect lost updates. This naming confusion has caused real financial losses and data corruption.

**Critical naming mismatches to check:**

| Database | Name Used | What It Actually Provides |
|----------|-----------|--------------------------|
| Oracle 11g | SERIALIZABLE | Snapshot isolation (write skew still possible) |
| PostgreSQL | REPEATABLE READ | Snapshot isolation (does detect lost updates) |
| MySQL InnoDB | REPEATABLE READ | Snapshot isolation WITHOUT automatic lost update detection |
| MySQL InnoDB | SERIALIZABLE | Two-phase locking — true serializable |
| DB2 | REPEATABLE READ | Serializable (opposite of everyone else) |
| PostgreSQL | SERIALIZABLE | True serializable via SSI (since v9.1) |

**Action:** After selecting the required isolation level, verify the database's actual behavior against this table. If the database name does not provide the required guarantee, select the next stronger level or apply compensating measures.

---

### Step 6: Produce the Recommendation

**ACTION:** Write a structured recommendation with: the anomaly exposure, the minimum required isolation level, the implementation choice (if serializable), the database-specific setting, and compensating measures if the database cannot provide the required level.

**WHY:** The recommendation must be actionable by an engineer configuring a database session or making a pull request. An abstract statement ("use serializable") is insufficient — the team needs the specific database configuration, any compensating measures, and the trade-offs being accepted.

**Output format:**

```
## Transaction Isolation Recommendation

### Current State
Database: [database + version]
Default isolation level: [what the database defaults to]
Current configured level: [what is actually set, if observable]

### Anomaly Exposure Analysis
[For each significant transaction pattern:]
Pattern: [description]
Exposed to: [list of anomalies from Step 2]
Minimum level required: [from Step 3 mapping]

### Recommendation
Isolation Level: [read committed | snapshot isolation | serializable]
Database Setting: [exact configuration statement for the specific database]
Implementation: [serial execution | 2PL | SSI | N/A]

### Trade-offs Accepted
[What anomalies are still possible at the chosen level, if below serializable]
[Performance cost if serializable is chosen]

### Compensating Measures
[If the database cannot provide the required level, or if a weaker level is
chosen deliberately, list the application-level compensations needed:]
- SELECT FOR UPDATE for write skew patterns (if staying below serializable)
- Retry logic for SSI aborts
- Explicit constraint checks at the application layer

### What to Monitor
[Deadlock rate (2PL), abort/retry rate (SSI), or lock contention metrics]
```

---

## What Can Go Wrong

Each of the 6 concurrency anomalies has a distinct detection signature and a specific minimum isolation level. The table below is a quick reference; full per-anomaly detail with worked examples is in `references/anomaly-isolation-matrix.md`.

| Anomaly | Detection signature | Prevented by | Level required |
|---------|--------------------|-----------|----|
| **Dirty read** | App acts on data that was never committed (in-flight write later rolled back) | Read committed + | Read committed |
| **Dirty write** | Two concurrent writes to the same object produce a mixed result (car sale: listing says Bob, invoice says Alice) | All practical levels | Read committed |
| **Read skew** | Long-running read sees different states at different points in time (Alice's $1000 appears as $900 during a transfer) | Snapshot isolation + | Snapshot isolation |
| **Lost update** | Concurrent read-modify-write cycles: both read 42, both write 43, result is 43 not 44 | Snapshot isolation (PG/Oracle auto-detect); explicit locks (MySQL) | Snapshot isolation* |
| **Write skew** | Two concurrent transactions both read a valid precondition, both write to disjoint objects, combined result violates invariant (doctor on-call count goes to 0) | Serializable only | Serializable |
| **Phantom read** | Check-then-insert: both transactions see zero conflicts, both insert, double-booking occurs | Serializable (write skew variant); snapshot isolation (read-only variant) | Serializable |

*MySQL InnoDB snapshot isolation does NOT automatically detect lost updates. Use `SELECT ... FOR UPDATE` or upgrade to SERIALIZABLE.

**The most dangerous gap:** Snapshot isolation does not prevent write skew. Oracle's "serializable" is snapshot isolation. If you are on Oracle and have any write skew pattern, you have no database-level protection. Use explicit `SELECT FOR UPDATE` on the precondition query (when rows exist) or add serializable-level protection at the application boundary.

---

## Key Principles

**The naming trap is the most dangerous pitfall.** Database isolation level names are not standardized in practice. Two databases can both claim to implement "serializable" while providing fundamentally different guarantees. Before configuring an isolation level, look up what that specific database's implementation actually provides, not what the name suggests. Oracle's "serializable" is snapshot isolation; IBM DB2's "repeatable read" is serializable. Trust the behavior, not the label.

**Write skew is the most commonly missed anomaly.** Dirty reads are well-known. Lost updates are familiar. Write skew — where two transactions read the same precondition and update disjoint objects — is subtle enough that it frequently goes undetected until a production incident. Any time application logic follows the pattern "check condition, make decision, write result," write skew is a possibility if two such transactions can run concurrently. The doctor on-call pattern appears in: inventory management, appointment booking, financial spending limits, membership count checks, and game state validation.

**Snapshot isolation is not serializable, despite what Oracle calls it.** Snapshot isolation prevents dirty reads, dirty writes, read skew, and (in some databases) lost updates. It does not prevent write skew or write skew phantoms. The "readers never block writers, writers never block readers" guarantee that makes snapshot isolation attractive is precisely what allows write skew: two transactions can both read the same precondition simultaneously and proceed to write.

**Serializable snapshot isolation (SSI) makes serializable practical.** The historical association of serializable isolation with heavy performance penalties comes from two-phase locking. SSI provides full serializability with much lower overhead — close to snapshot isolation performance at low-to-moderate contention. PostgreSQL has offered SSI since version 9.1. Teams that reject serializable isolation for performance reasons should evaluate whether SSI in their specific database actually has unacceptable overhead for their workload, rather than accepting that overhead as given.

**Explicit locking is the escape hatch, not the solution.** `SELECT FOR UPDATE` and other explicit locks can compensate for weaker isolation levels in specific cases. They work when the rows to lock are known in advance (you can lock the specific rows the precondition query returns). They fail when the write skew involves inserting a new row that matches a condition — there is no existing row to lock. Explicit locking also requires careful code discipline: forgetting one lock somewhere creates a race condition. Serializable isolation is more robust because it applies automatically.

**Application retry logic is not optional for SSI.** SSI aborts transactions that would violate serializability. Unlike 2PL where the transaction blocks waiting for a lock (and succeeds after the lock is released), SSI aborts at commit time. The application must detect the abort and retry the entire transaction from the beginning. ORM frameworks that silently swallow exceptions (like Rails' ActiveRecord with default error handling) will not retry — the error reaches the user and the operation is lost. SSI adoption requires explicit retry handling in the application layer.

---

## Examples

### Example 1: Financial Transfer Service (Write Skew Exposure)

**Scenario:** A fintech service performs fund transfers between accounts. A transfer transaction reads both account balances, verifies the source account has sufficient funds, then decrements the source and increments the destination. The service processes ~500 concurrent requests per second. The database is PostgreSQL (default isolation: read committed).

**Trigger:** "We have a bug where accounts occasionally go negative, but only under load. Our transaction checks the balance before debiting."

**Process:**
- Step 1: PostgreSQL defaults to read committed. The transaction is: SELECT balance, verify > 0, UPDATE source balance, UPDATE destination balance.
- Step 2: The read-then-write pattern (check balance, then debit) is exposed to write skew if multiple transfers from the same source account run concurrently. Two concurrent transfers both read the balance as $100, both decide it's sufficient for a $60 debit, both debit — result is -$20.
- Step 3: Write skew requires serializable isolation. Snapshot isolation would not help here because both transactions update different rows (source and destination balances are different objects).
- Step 4: SSI evaluation: PostgreSQL supports SSI via SERIALIZABLE. Contention is moderate (multiple concurrent transfers from popular accounts). SSI is appropriate; retry logic required.
- Step 5: Naming check: PostgreSQL's SERIALIZABLE actually uses SSI — true serializable.

**Output:**
```
## Transaction Isolation Recommendation

Database: PostgreSQL 15
Default: Read committed
Current: Read committed (bug: insufficient for this workload)

Anomaly Exposure:
Pattern: Read balance → verify sufficient → debit source → credit destination
Exposed to: Write skew (concurrent transfers from same source account)
Minimum level required: Serializable

Recommendation:
Isolation Level: Serializable
Database Setting: SET default_transaction_isolation = 'serializable';
  (or per-transaction: BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE)
Implementation: SSI (PostgreSQL default for SERIALIZABLE since v9.1)

Trade-offs Accepted:
  - SSI may abort transactions under high contention on the same account
  - Application must implement retry logic for serialization failures (SQLSTATE 40001)

Compensating Measure (if serializable is not adopted):
  - Add SELECT balance FROM accounts WHERE id = $1 FOR UPDATE in the transfer
    transaction — locks the source account row before checking the balance
  - This prevents concurrent transfers from the same source from passing the
    balance check simultaneously

Monitor: pg_stat_activity for serialization failures; track retry rate
```

---

### Example 2: Doctor On-Call Scheduling (Classic Write Skew)

**Scenario:** A hospital scheduling app allows doctors to release their on-call shift if at least one other doctor remains on call. The check is: `SELECT COUNT(*) FROM doctors WHERE on_call = true AND shift_id = $1`. If count >= 2, the requesting doctor is marked off-call. The database is MySQL InnoDB (default: repeatable read).

**Trigger:** "We had an incident where all doctors went off-call simultaneously. Our code checks that at least one other doctor is on call before allowing the change."

**Process:**
- Step 1: MySQL InnoDB defaults to repeatable read. MySQL's repeatable read does not automatically detect lost updates and does not prevent write skew.
- Step 2: Classic write skew — two concurrent off-call requests both pass the count check (both see count = 2), both update their own row (disjoint objects — Alice's record and Bob's record), result is count = 0.
- Step 3: Write skew requires serializable. Snapshot isolation alone does not prevent this.
- Step 4: MySQL InnoDB SERIALIZABLE uses two-phase locking (not SSI). At ~50 concurrent scheduling requests, contention on the doctors table is low — 2PL is acceptable.
- Step 5: Naming check: MySQL's REPEATABLE READ does NOT prevent write skew. MySQL's SERIALIZABLE uses 2PL — true serializable.

**Output:**
```
## Transaction Isolation Recommendation

Database: MySQL InnoDB
Default: Repeatable read (does not prevent write skew)
Current: Repeatable read (insufficient — confirmed root cause of incident)

Anomaly Exposure:
Pattern: COUNT doctors on-call → if >= 2 → update own record to off-call
Exposed to: Write skew (concurrent off-call requests)
Minimum level required: Serializable

Recommendation:
Isolation Level: Serializable
Database Setting: SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  (or SET GLOBAL if appropriate)
Implementation: 2PL (MySQL InnoDB SERIALIZABLE uses 2PL, not SSI)

Trade-offs Accepted:
  - 2PL will block concurrent transactions that conflict — scheduling requests may queue
  - Deadlocks possible; application must handle and retry

Compensating Measure (if serializable not adopted):
  - Upgrade the COUNT query to: SELECT COUNT(*) FROM doctors
    WHERE on_call = true AND shift_id = $1 FOR UPDATE
  - This locks all on-call rows for the shift, preventing concurrent reads of
    the same precondition. Works because the rows being checked exist.
  - This is application-level mitigation, not a substitute for serializable isolation.

Monitor: Deadlock rate (SHOW ENGINE INNODB STATUS); lock wait timeouts
```

---

### Example 3: Meeting Room Booking System (Phantom Causing Write Skew)

**Scenario:** A booking system checks for conflicting reservations before inserting a new booking. The check: `SELECT COUNT(*) FROM bookings WHERE room_id = $1 AND end_time > $2 AND start_time < $3`. If count = 0, insert the booking. Database is PostgreSQL with snapshot isolation (REPEATABLE READ).

**Trigger:** "We occasionally get double-booked rooms. The conflict check runs inside a transaction, so we thought it was safe."

**Process:**
- Step 1: PostgreSQL REPEATABLE READ = snapshot isolation. Not true serializable.
- Step 2: This is a write skew phantom — the transaction checks for the absence of rows, then inserts a new row matching the same condition. Two concurrent bookings both see count = 0, both proceed to insert. Neither transaction modified an existing row — they both inserted new rows that didn't exist when the check ran. Snapshot isolation does not prevent this.
- Step 3: Write skew phantom requires serializable. Snapshot isolation explicitly does NOT prevent phantoms in read-write transactions.
- Step 4: SSI evaluation: PostgreSQL SERIALIZABLE uses SSI. Booking conflicts are low-frequency per room (users don't typically book the same room simultaneously in high volume). SSI is appropriate.
- Step 5: Naming check: PostgreSQL SERIALIZABLE = SSI = true serializable. Correct.

**Output:**
```
## Transaction Isolation Recommendation

Database: PostgreSQL
Default / Current: Repeatable read (snapshot isolation) — insufficient for this pattern

Anomaly Exposure:
Pattern: SELECT count of conflicts → if zero → INSERT booking
Exposed to: Write skew phantom (two concurrent inserts both pass the zero-conflict check)
Minimum level required: Serializable

Recommendation:
Isolation Level: Serializable
Database Setting: BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE
  (applied to all booking transactions)
Implementation: SSI (PostgreSQL default for SERIALIZABLE)

Trade-offs Accepted:
  - High-contention booking windows (popular rooms, peak hours) will see SSI aborts
  - Application must retry on serialization failure (SQLSTATE 40001)

Compensating Measure (if serializable not adopted):
  - Materializing conflicts: create a table of room/time-slot locks populated
    ahead of time. Use SELECT FOR UPDATE on the relevant time slots before
    checking for conflicts. This is complex and couples concurrency logic
    into the data model — use as last resort only.
  - A unique constraint on (room_id, time_slot) works for discrete time slots
    but not for arbitrary time ranges.

Monitor: SSI abort rate per booking endpoint; alert if retry rate > 5%
```

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/anomaly-isolation-matrix.md` | Full 6×4 anomaly-to-isolation mapping matrix with per-cell explanations; database-specific implementation notes; examples for each anomaly type | When working through Step 3 or explaining anomaly coverage to a team |
| `references/serializability-implementation-comparison.md` | Side-by-side comparison of serial execution, two-phase locking, and SSI across 8 dimensions (throughput, latency, abort rate, contention behavior, deadlock risk, implementation complexity, database support, operational overhead); decision tree for selecting among them | When Step 4 selection is needed or when justifying implementation choice to a team |
| `references/write-skew-patterns.md` | Detailed catalog of 5 write skew patterns (at-least-one constraint, no-overlap, unique claim, budget enforcement, game state validity); detection checklist; SQL patterns for explicit locking mitigation per pattern | When diagnosing whether a specific transaction pattern is vulnerable to write skew |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
