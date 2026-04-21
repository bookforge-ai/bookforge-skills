---
name: transaction-isolation-level-auditor
description: "Use when auditing database transaction configuration for concurrency safety — checking isolation level settings, diagnosing lost update bugs, non-repeatable read vulnerabilities, phantom read risks, or ACID compliance gaps. Applies Fowler's Table 5.1 (the explicit isolation-level × anomaly matrix from Patterns of Enterprise Application Architecture Chapter 5) to map READ UNCOMMITTED / READ COMMITTED / REPEATABLE READ / SERIALIZABLE to permitted anomaly classes: dirty read, non-repeatable read (inconsistent read), phantom read, and lost update. Produces a structured isolation audit report covering: current isolation level, permitted anomalies, code locations with read-modify-write without optimistic check (lost update vulnerability), SELECT FOR UPDATE correctness, long-transaction risks, ACID compliance at system-transaction level, and ACID gaps at business-transaction level across multiple requests. Covers: transaction isolation, database concurrency, optimistic locking, pessimistic locking, version column, READ COMMITTED default risks, REPEATABLE READ upgrade decisions, SERIALIZABLE overhead, immutability as concurrency escape hatch, Spring @Transactional isolation settings, Hibernate session isolation, SQLAlchemy transaction config, EF Core transaction isolation, business transaction ACID, saga atomicity, offline lock isolation. Triggers: 'we have a lost update bug', 'two users editing the same record', 'is our isolation level correct', 'should we use SERIALIZABLE', 'transaction audit', 'ACID compliance review'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/transaction-isolation-level-auditor
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors:
      - Martin Fowler
      - David Rice
      - Matthew Foemmel
      - Edward Hieatt
      - Robert Mee
      - Randy Stafford
    chapters: [5]
domain: enterprise-application-architecture
tags:
  - transactions
  - concurrency
  - acid
  - database
  - data-integrity
  - auditing
  - design-patterns
  - isolation-levels
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Enterprise application source code — transaction boundaries (@Transactional, begin/commit, BEGIN TRANSACTION, session.begin_nested), database config (isolation level per connection/session/global), update patterns (read-modify-write, SELECT FOR UPDATE)"
    - type: user-description
      description: "Description of the system, its transaction config, and the concurrency concern (lost update report, audit request, isolation level selection question)"
  tools-required:
    - Read
    - Grep
  tools-optional:
    - Glob
    - Write
  mcps-required: []
  environment: "Enterprise application with a relational database. Codebase access strongly preferred; user description of transaction config and update patterns is a workable fallback."
discovery:
  goal: "Produce an isolation audit report that maps the current isolation level to permitted anomaly classes, finds code-level vulnerabilities, assesses system-transaction ACID compliance, and flags business-transaction ACID gaps."
  tasks:
    - "Identify the current database isolation level from config/code"
    - "Apply Table 5.1 to determine which anomaly types are permitted"
    - "Scan transaction code for lost update vulnerabilities (read-modify-write without optimistic check)"
    - "Flag non-repeatable read and phantom read exposure per transaction"
    - "Check system-transaction ACID compliance signals"
    - "Identify business-transaction ACID gaps (multi-request workflows with no offline lock)"
    - "Produce per-vulnerability fix recommendations"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
    experience: intermediate
  when_to_use:
    triggers:
      - "Reports of lost updates — one user's save silently overwrites another's"
      - "Auditing transaction configuration before a production incident"
      - "Selecting an isolation level for a new service or subsystem"
      - "Reviewing @Transactional or begin/commit usage in a codebase"
      - "ACID compliance review for a financial, inventory, or healthcare system"
      - "Performance complaints about too much locking / deadlocks suggesting over-isolation"
      - "Diagnosing whether READ COMMITTED is safe for a specific workflow"
    prerequisites: []
    not_for:
      - "Multi-request business transaction concurrency (user edits spanning multiple HTTP requests) — use offline-concurrency-strategy-selector instead for lock pattern selection"
      - "Thread-level concurrency within a single process (use language-level synchronization primitives)"
      - "Distributed consensus across services (use saga, two-phase commit, or Raft)"
      - "NoSQL systems without SQL isolation level semantics"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 13
    iterations_needed: null
---

# Transaction Isolation Level Auditor

Applies Fowler's Table 5.1 isolation-level matrix to audit a system's transaction configuration, map the current isolation level to its permitted anomaly classes, locate code-level vulnerabilities, and produce a structured fix plan with ACID compliance assessment at both system-transaction and business-transaction levels.

---

## When to Use

Use this skill when you need to answer any of:
- "Are we exposed to lost updates with our current isolation level?"
- "Should we upgrade from READ COMMITTED to REPEATABLE READ or SERIALIZABLE?"
- "Is this codebase ACID-compliant at the system-transaction level? At the business-transaction level?"
- "We have a concurrency bug — which anomaly class is it and what fixes it?"

This skill targets **single-request, database-managed system transactions**. If the concern is multi-request business transactions (user edits over minutes), invoke `offline-concurrency-strategy-selector` for lock pattern selection after completing this audit.

**Prerequisites:** None. Codebase access improves coverage; a description of the transaction config is sufficient for a high-level audit.

---

## Context and Input Gathering

Gather the following before auditing. Ask the user if not inferable from the codebase.

**Required:**
- **Current isolation level:** Check in this order — (1) `config/database.yml`, `application.properties`, `appsettings.json`; (2) ORM/framework config (`@Transactional(isolation=...)`, `connection.set_isolation_level(...)`, `DbContextOptionsBuilder`); (3) database-level default (`SHOW TRANSACTION ISOLATION LEVEL`, `SELECT @@transaction_isolation`).
- **Transaction boundary pattern:** How transactions are opened and closed — declarative (`@Transactional`), programmatic (`session.begin()`, `BEGIN TRANSACTION`), or request-scoped middleware.

**Observable from codebase (Grep for):**
- `@Transactional`, `begin_transaction`, `BEGIN TRANSACTION`, `session.begin`, `session.begin_nested`, `getTransaction().begin()`, `SaveChanges()`
- `SELECT.*FOR UPDATE`, `LOCK IN SHARE MODE`, `WITH (UPDLOCK)`
- Read-modify-write patterns: load → mutate → save without a version/optimistic check
- Version/ETag columns: `version`, `optimistic_lock`, `row_version`, `etag`

**Defaults (when not found):**
- PostgreSQL, Oracle, SQL Server: default to READ COMMITTED
- MySQL InnoDB: defaults to REPEATABLE READ
- No `SELECT FOR UPDATE` or version column = no lost-update protection beyond isolation level

**Sufficiency check:** If isolation level and at least one transaction boundary are known, proceed. Flag any gaps in coverage.

---

## Process

### Step 1 — Read the Current Isolation Level

Search config files and ORM annotations for explicit isolation level settings. If not found, assume the database vendor default (READ COMMITTED for most production databases).

_WHY: The isolation level is the single configuration value that determines which anomaly classes the database prevents. Everything downstream depends on it._

**Grep commands:**
```
Grep "@Transactional" — find Spring/Java annotation-based transaction demarcation
Grep "isolation" — find explicit isolation level overrides
Grep "BEGIN\|begin_transaction\|session.begin" — find programmatic boundaries
Grep "SELECT.*FOR UPDATE\|NOWAIT\|SKIP LOCKED" — find pessimistic read locks
Grep "version\|optimistic_lock\|row_version\|etag" in schema/models — find optimistic check columns
```

### Step 2 — Apply Table 5.1 to Map Permitted Anomalies

Look up the current isolation level in the matrix below and record which anomalies are **permitted** (not prevented):

| Isolation Level | Dirty Read | Unrepeatable Read | Phantom Read |
|---|---|---|---|
| Read Uncommitted | Permitted | Permitted | Permitted |
| Read Committed | Prevented | **Permitted** | **Permitted** |
| Repeatable Read | Prevented | Prevented | **Permitted** |
| Serializable | Prevented | Prevented | Prevented |

_WHY: This is Fowler's Table 5.1 — the authoritative SQL standard mapping. It tells you exactly what the database guarantees and what it does not. Anomaly classes not in this table (specifically Lost Update) require an additional application-level check regardless of isolation level._

**Add Lost Update assessment separately:**
- Lost Update is a write-write conflict, not covered by the SQL anomaly table.
- It occurs at **any isolation level** when read-modify-write is used without an optimistic version check or SELECT FOR UPDATE.
- Flag this independently of isolation level.

### Step 3 — Scan for Code-Level Vulnerabilities

For each transaction in scope, check for the patterns below. Flag each finding with file location.

**3a. Lost Update vulnerability — read-modify-write without optimistic check:**
Look for: entity is loaded → a field is modified → entity is saved, with no version comparison between read and write.

```python
# Vulnerable pattern (Python/SQLAlchemy example)
item = session.query(Item).filter_by(id=item_id).one()
item.stock -= quantity   # based on stale read
session.commit()         # second concurrent writer overwrites first

# Safe pattern — version column checked
session.execute(
    "UPDATE items SET stock=:s, version=version+1 WHERE id=:id AND version=:v",
    {"s": item.stock - quantity, "id": item_id, "v": item.version}
)
```

**3b. Unrepeatable Read vulnerability (if isolation < Repeatable Read):**
Look for: the same row is read twice within one transaction, and correctness depends on the values being stable. Flag when isolation level is READ COMMITTED.

**3c. Phantom Read vulnerability (if isolation < Serializable):**
Look for: range queries (COUNT, SUM, WHERE date BETWEEN, WHERE status = 'pending') executed inside a transaction that also writes rows matching the same range. Flag when isolation < Serializable.

**3d. Long transaction at high isolation:**
Look for: transactions that span user think-time, file I/O, or remote calls. These hold locks (Repeatable Read/Serializable) or accumulate snapshot overhead (MVCC), degrading throughput and risking deadlocks.

_WHY: Code-level patterns determine actual exposure. The isolation level sets the floor, but read-modify-write without a guard lets Lost Update through at any level. Step 3 finds the specific call sites to fix._

### Step 4 — Check System-Transaction ACID Compliance

For each ACID property, look for its implementation signal:

| Property | Implementation Signal | Green | Red |
|---|---|---|---|
| Atomicity | Exception handler rolls back | All writes inside one try/catch with rollback | Multiple transactions for one logical operation; partial commit on error |
| Consistency | Schema constraints + post-write validation | FK constraints, NOT NULL, CHECK constraints; business invariants validated pre-commit | Deferred validation; invariants checked after commit |
| Isolation | Isolation level + optimistic/pessimistic guards | Level adequate for use case; version checks present | READ COMMITTED + read-modify-write with no version check |
| Durability | DB config | Sync commit ON; WAL enabled; replication | `synchronous_commit=off` without understanding the tradeoff |

_WHY: Each ACID property has a concrete implementation shape. Identifying the absence of that shape (no rollback on error, no version column) gives actionable fixes, not just warnings._

### Step 5 — Identify Business-Transaction ACID Gaps

A business transaction spans multiple HTTP requests and multiple system transactions. Ask:
- Does the system have any multi-step workflows (user opens record → edits across multiple screens → saves)?
- If YES: the database provides no isolation between the user's reads and final commit. Lost updates and inconsistent reads are possible regardless of system-transaction isolation level.
- IF the workflow has no Optimistic Offline Lock (version column) or Pessimistic Offline Lock (record checkout) → flag as a business-transaction isolation gap.

_WHY: Fowler explicitly distinguishes system transactions (RDBMS-managed) from business transactions (application-managed). Most ACID discussions focus on system transactions and miss the multi-request gap entirely. This is where the most severe real-world lost update bugs live._

For business-transaction gaps, cross-reference `offline-concurrency-strategy-selector` for pattern selection.

### Step 6 — Produce Fix Recommendations

For each vulnerability found in Steps 3-5, assign one of:

| Fix | When to Apply |
|---|---|
| Add version column + optimistic check | Lost Update in read-modify-write; use as default first choice |
| Add `SELECT FOR UPDATE` | Lost Update in high-contention, short-transaction context |
| Raise isolation to Repeatable Read | Unrepeatable Read in a single transaction that reads same row twice |
| Raise isolation to Serializable | Phantom Read in correctness-critical range queries |
| Refactor to immutability / snapshots | Read-heavy computation; consider read replica or snapshot isolation |
| Shorten transaction / extract reads | Long-transaction at high isolation; move non-DB work outside BEGIN/COMMIT |
| Invoke offline-concurrency-strategy-selector | Business-transaction isolation gap across multiple requests |

_WHY: Not every vulnerability needs the highest isolation fix. Recommending per-vulnerability fixes (rather than "always use Serializable") preserves throughput and minimizes lock contention._

### Step 7 — Produce the Isolation Audit Report

Assemble findings into the output format.

---

## Inputs

- Current isolation level (from config, code annotations, or database default)
- Transaction boundary locations (grep results or user description)
- Read-modify-write patterns found in code
- Presence or absence of version columns / SELECT FOR UPDATE
- Multi-request workflow description (for business-transaction check)

---

## Outputs

Produce a markdown isolation audit report with these sections:

```markdown
# Isolation Audit Report — [System Name]
Date: [date]

## Configuration
- Database: [vendor + version]
- Isolation Level: [level name]
- Transaction Demarcation: [declarative @Transactional / programmatic / request-scoped]

## Permitted Anomalies (Table 5.1 Mapping)
- Dirty Read: Prevented / Permitted
- Unrepeatable Read: Prevented / Permitted
- Phantom Read: Prevented / Permitted
- Lost Update (application-layer): Protected / VULNERABLE

## Vulnerabilities Found

### [VULN-01] Lost Update — [file:line]
Pattern: read-modify-write without version check
Risk: [describe the business consequence]
Fix: Add version column + optimistic check (see references/isolation-anomaly-matrix.md)

### [VULN-02] ...

## System-Transaction ACID Assessment
- Atomicity: [Green/Red] — [evidence]
- Consistency: [Green/Red] — [evidence]
- Isolation: [Green/Red] — [evidence]
- Durability: [Green/Red] — [evidence]

## Business-Transaction ACID Gaps
[List multi-request workflows with no offline lock; cross-reference offline-concurrency-strategy-selector]

## Recommended Actions (Prioritized)
1. [Highest risk fix]
2. ...

## Immutability Opportunities
[List read-heavy computations that could use snapshots or read replicas to sidestep concurrency entirely]
```

---

## Key Principles

**1. Table 5.1 is your baseline, not your complete answer.**
The SQL anomaly table covers Dirty Read, Unrepeatable Read, and Phantom. Lost Update — the most common application bug — is not in it. Treat the two separately: isolation level for read anomalies, application-level version check for write conflicts.

_Why this matters: Engineers who only consult the isolation level often miss Lost Update entirely because "we're on READ COMMITTED" sounds safe._

**2. READ COMMITTED + read-modify-write = Lost Update waiting to happen.**
The majority of enterprise databases default to READ COMMITTED. READ COMMITTED prevents dirty reads but allows Unrepeatable Reads, Phantoms, and Lost Updates. A read-modify-write without a version column is vulnerable at READ COMMITTED regardless of how short the transaction is.

_Why this matters: Fowler frames Lost Update as the simplest concurrency problem to understand but the easiest to miss in production because the bug appears as "someone's changes just disappeared."_

**3. Raising isolation level trades liveness for correctness — do it per-transaction.**
Fowler: "You don't have to use the same isolation level for all transactions." Serializable on every transaction in a high-throughput system causes contention and deadlocks. Apply Serializable or Repeatable Read only to the specific transactions that need it (range-scan reports, correctness-critical reads).

_Why this matters: A blanket "upgrade everything to Serializable" fix often causes worse production problems than the original bug._

**4. Immutability eliminates the problem rather than managing it.**
Fowler identifies immutability as a concurrency-control strategy: data that cannot be modified needs no concurrency control. Read replicas, event log projections, CQRS read models, and cached snapshots exploit this. Before raising isolation level, ask whether the read path can be made immutable.

_Why this matters: Immutability removes the tradeoff entirely — no liveness cost, no lock overhead, correct by construction._

**5. Business-transaction ACID requires application-level enforcement.**
The RDBMS provides ACID within a single BEGIN/COMMIT block. Across multiple HTTP requests, the database provides nothing. Multi-step user workflows need Optimistic Offline Lock (version column check at commit) or Pessimistic Offline Lock (record checkout before first read).

_Why this matters: The most severe lost update bugs in enterprise systems live in multi-step workflows, not in individual database transactions._

**6. Long transactions at high isolation are a double-edged fix.**
Running a long computation inside Serializable or Repeatable Read prevents anomalies inside that computation, but holds locks (or accumulates MVCC overhead) for the duration. This blocks concurrent writers and risks deadlocks. Prefer shorter transactions: read data first, perform computation, open transaction only for the write window.

---

## Examples

### Scenario 1 — Spring Boot service with @Transactional defaults

**Trigger:** Team reports intermittent "lost updates" on inventory records during high load. Stack: Spring Boot + PostgreSQL (READ COMMITTED default). No version columns.

**Process:**
1. Grep finds `@Transactional` on service methods with no isolation override → READ COMMITTED confirmed.
2. Table 5.1 mapping: Dirty Read prevented; Unrepeatable Read permitted; Phantom permitted.
3. Scan finds `itemRepo.findById(id)` → `item.setStock(item.getStock() - qty)` → `itemRepo.save(item)` with no version check in 3 locations.
4. No `SELECT FOR UPDATE` anywhere in the persistence layer.
5. ACID check: Atomicity — @Transactional handles rollback (green); Isolation — READ COMMITTED + no version column (red).
6. No multi-request business transaction detected (all operations complete in one request).

**Output excerpt:**
```
Permitted Anomalies: Unrepeatable Read (permitted), Phantom (permitted),
Lost Update (VULNERABLE — 3 locations)

VULN-01: ItemService.java:87 — read-modify-write without version check
Fix: Add version column to items table; use optimistic lock in UPDATE statement

Recommended: Add @Version column (JPA) to Item entity. PostgreSQL READ COMMITTED
default is adequate once lost-update protection is added at the application layer.
No isolation level upgrade needed.
```

---

### Scenario 2 — Financial posting service needing range-scan consistency

**Trigger:** Audit requirement: nightly balance report must reflect a consistent snapshot of all postings. Stack: Python + SQLAlchemy + PostgreSQL. Report runs a SUM across millions of rows.

**Process:**
1. Config shows `isolation_level="READ_COMMITTED"` on the session factory.
2. Table 5.1: Phantom Read permitted at READ COMMITTED — range scans can return different totals if concurrent inserts occur mid-query.
3. Report query is a single large SELECT SUM … GROUP BY — no write path, no version check needed.
4. Phantom risk: concurrent posting inserts can change the aggregate mid-report.
5. ACID check: Durability — WAL enabled (green); Isolation for reports — READ COMMITTED insufficient (red for correctness requirement).
6. Immutability opportunity: Consider running the report against a read replica or using `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ` only for this session.

**Output excerpt:**
```
VULN-01: balance_report.py — Phantom Read exposure on SUM aggregates
Fix Option A: SET TRANSACTION ISOLATION LEVEL REPEATABLE READ for this session only
Fix Option B: Run report against a read replica after a logical checkpoint (immutability escape hatch)

No Lost Update risk (report is read-only). No business-transaction ACID gap.
```

---

### Scenario 3 — Multi-step checkout workflow with no offline lock

**Trigger:** E-commerce platform where users add items to cart over multiple pages before placing an order. Engineers ask whether the system is ACID-compliant.

**Process:**
1. Isolation level: MySQL InnoDB REPEATABLE READ (default).
2. Table 5.1 at Repeatable Read: Dirty Read prevented, Unrepeatable Read prevented, Phantom permitted.
3. No Lost Update vulnerability within individual system transactions (version columns present on Order entity).
4. Business-transaction check: checkout spans 4 HTTP requests (address → payment → review → confirm). No Optimistic Offline Lock or Pessimistic Offline Lock between session start and final confirm.
5. Between session start and confirm, inventory levels can change. No version check on inventory at confirm time → business-transaction Lost Update possible.

**Output excerpt:**
```
System-Transaction ACID: Green across all four properties.

Business-Transaction ACID Gap:
- Isolation: VULNERABLE — inventory levels not version-checked at order confirm.
  Two concurrent checkouts for the last item can both succeed.
- Fix: Add Optimistic Offline Lock on inventory.quantity. Check version at confirm step.
  See: offline-concurrency-strategy-selector for full lock pattern selection.
```

---

## References

- `references/isolation-anomaly-matrix.md` — Full Table 5.1, anomaly definitions, default isolation levels by database vendor, business vs system transaction ACID breakdown, long-transaction risk guidance
- Source: PEAA Chapter 5 "Concurrency" — sections: Concurrency Problems, Isolation and Immutability, Transactions (pp. 81–94)

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-offline-concurrency-strategy-selector`
- `clawhub install bookforge-data-access-anti-pattern-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
