---
name: concurrency-anomaly-detector
description: |
  Scan application code, SQL queries, or ORM code for exposure to the 6 database concurrency anomalies and produce a findings report with severity, affected locations, and fix recommendations. Use when: debugging a nondeterministic data corruption or race condition bug under concurrent load; auditing transaction code before deployment or after switching databases (isolation defaults differ across engines); a read-modify-write cycle or check-then-act pattern may be exposed to lost updates or write skew; an aggregate query (COUNT, SUM) guards an INSERT or UPDATE (phantom read exposure); or multiple tables are updated in one transaction without serializable isolation. Distinct from transaction-isolation-selector (which chooses the isolation level) — this skill scans code to find which anomalies existing code is already exposed to. Covers Python, Java, Go, JavaScript, Ruby; raw SQL; ORM code (SQLAlchemy, Hibernate, ActiveRecord, GORM); PostgreSQL, MySQL InnoDB, Oracle, SQL Server, and distributed databases. Maps code patterns (read-modify-write, SELECT/INSERT pairs, cross-table boundaries, snapshot boundary reads) to anomaly type, trigger conditions, and minimum fix (isolation upgrade vs. application-level mitigation).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/concurrency-anomaly-detector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - transaction-isolation-selector
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [7]
tags: [transactions, concurrency, race-conditions, dirty-read, dirty-write, read-skew, lost-update, write-skew, phantom-read, isolation-levels, snapshot-isolation, serializable, mvcc, postgresql, mysql, oracle, sql-server, code-review, audit]
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "Application source code containing transaction logic, SQL queries, or ORM calls — the primary input"
    - type: document
      description: "Transaction description or architecture summary if no codebase is available"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Grepping for SQL keywords and transaction patterns is the primary analysis method."
discovery:
  goal: "Identify all code locations exposed to at least one of the 6 concurrency anomalies; classify each finding by anomaly type and severity; produce actionable fix recommendations"
  tasks:
    - "Determine the database in use and its default isolation level"
    - "Grep for transaction boundaries and SQL patterns that indicate anomaly exposure"
    - "Classify each finding into one of the 6 anomaly types"
    - "Assign severity based on the anomaly type and its business impact"
    - "Produce fix recommendations — isolation upgrade or application-level mitigation — per finding"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "tech-lead", "site-reliability-engineer"]
    experience: "intermediate-to-advanced — assumes familiarity with relational databases and SQL transactions"
  triggers:
    - "A data corruption or inconsistency bug is suspected but hard to reproduce"
    - "Code review for a new service or feature that uses database transactions"
    - "Migration to a database with a different default isolation level"
    - "Audit of existing codebase for concurrency safety"
    - "Post-incident analysis of a race condition"
  not_for:
    - "Choosing an isolation level from scratch without existing code — use transaction-isolation-selector instead"
    - "Distributed transaction coordination across multiple databases — use distributed-failure-analyzer"
    - "Replication-level consistency issues — use replication-strategy-selector"
---

# Concurrency Anomaly Detector

## When to Use

You have existing application code that interacts with a database and you need to know whether it is safe under concurrent execution.

This skill applies when:
- A bug only manifests under concurrent load and is hard to reproduce in tests
- Code is being reviewed before deployment to a high-concurrency environment
- The application recently migrated to a database with a different default isolation level
- The codebase accesses multiple tables in a single transaction
- Any code follows the pattern: read a value, make a decision, write a result

**The core insight from Kleppmann:** Concurrency bugs caused by weak transaction isolation are not just theoretical. They cause real financial losses and data corruption. They are triggered only by unfortunate timing, making them nearly impossible to catch by testing. The only reliable approach is to analyze the code structure — not the test results — and identify which patterns are structurally vulnerable.

**Companion skill:** `transaction-isolation-selector` — once anomalies are identified, that skill selects the minimum safe isolation level. This skill identifies what anomalies exist in current code; the companion skill recommends what to do about them.

---

## Context and Input Gathering

### Required Context (must have — ask if missing)

- **Database in use and version.** Why: the same isolation level name has different behaviors across databases. MySQL's "repeatable read" does not automatically detect lost updates; PostgreSQL's does. Oracle's "serializable" is actually snapshot isolation. Without knowing the database, severity assessments cannot be calibrated to actual risk.
  - Check: `docker-compose.yml`, `requirements.txt` / `pom.xml` / `go.mod` / `package.json` for database drivers, schema file syntax
  - If missing, ask: "What database are you using, and what version?"

- **Current isolation level.** Why: the same code pattern has different severity depending on the isolation level in effect. A lost update pattern is high severity at read committed but handled automatically at PostgreSQL's repeatable read. If the isolation level is unknown, assume the database default (usually read committed).
  - Check: ORM configuration, database session setup, application config files, environment variables
  - If missing, assume the database's default and note the assumption explicitly

- **Application code or transaction descriptions.** Why: this is the primary input. The scan requires reading transaction logic to identify patterns.
  - Gather: entry points for significant transactions, files containing SQL or ORM calls, service layer code

### Observable Context (gather from environment)

Before asking anything, scan the environment:

```
Grep targets:
  - Transaction boundaries:  BEGIN, START TRANSACTION, @Transactional, with_transaction,
                              session.begin(), db.transaction(), conn.cursor()
  - Read-modify-write:       SELECT ... followed by UPDATE in same function scope
  - Check-then-act:          SELECT COUNT(*), SELECT SUM(), SELECT EXISTS() followed by INSERT/UPDATE
  - Explicit locking:        FOR UPDATE, FOR SHARE, LOCK TABLE, SELECT ... WITH (UPDLOCK)
  - Isolation settings:      ISOLATION LEVEL, transaction_isolation, SET SESSION
  - ORM patterns:            find_by, where().first(), session.query(), Model.where()
                              followed by .save(), .update(), .create() in the same scope
```

### Default Assumptions

When context cannot be observed and asking would be excessive:
- Isolation level unknown → assume read committed (PostgreSQL/Oracle/SQL Server default)
- Transaction boundaries unknown → look for natural HTTP request/response boundaries
- Concurrency level unknown → assume multiple concurrent users access the same data (conservative)

---

## Process

### Step 1: Identify the Database and Its Actual Isolation Guarantees

**ACTION:** Determine the database, its default isolation level, and any overrides in the codebase.

**WHY:** Every subsequent severity assessment depends on what the database actually prevents at its current isolation level. "We use PostgreSQL so we're fine" is a common and dangerous assumption. PostgreSQL's default is read committed — it does not prevent read skew, lost updates, write skew, or phantom reads. Establishing the ground truth of what the database currently prevents is the prerequisite for everything else.

Record:

```
Database:                  [PostgreSQL | MySQL InnoDB | Oracle | SQL Server | other]
Default isolation level:   [read committed | repeatable read | serializable]
Configured isolation:      [from code scan or config — override if found]
Effective isolation:       [the level actually in use]
```

**Isolation level defaults (critical to get right):**

| Database | Default | What it prevents | What it allows |
|----------|---------|-----------------|----------------|
| PostgreSQL | Read committed | Dirty reads, dirty writes | Read skew, lost updates, write skew, phantoms |
| MySQL InnoDB | Repeatable read | Dirty reads, dirty writes, read skew | Lost updates (silently!), write skew, phantoms |
| Oracle 11g | Read committed | Dirty reads, dirty writes | Everything else. Oracle "SERIALIZABLE" = snapshot isolation — write skew still possible |
| SQL Server | Read committed | Dirty reads, dirty writes | Read skew, lost updates, write skew, phantoms |

---

### Step 2: Grep for Anomaly-Indicating Code Patterns

**ACTION:** Search the codebase systematically for the structural patterns that expose each of the 6 anomaly types.

**WHY:** Concurrency anomalies cannot be found by running the code — the bugs only manifest when multiple transactions interleave at precisely the wrong time. What can be found reliably is the code structure that makes the anomaly possible. Each anomaly type has a distinct structural fingerprint. Grepping for these patterns is more reliable than reading every file manually and is the same approach a static analysis tool would take.

**Pattern catalog — what to grep for and what it indicates:**

**Dirty reads and dirty writes — Pattern: missing transaction boundary or read uncommitted**
```
Signal: Explicit SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED, or autocommit enabled
        across multi-step write operations with no BEGIN/COMMIT wrapper.
Grep:   READ UNCOMMITTED, autocommit=1 (MySQL) with multi-step writes
Note:   Read committed and above prevent dirty reads automatically at all practical
        databases. Flag only if read uncommitted is explicitly configured.
```

**Read skew — Pattern: multi-read transaction without snapshot isolation**
```
Signal: Multiple SELECTs in the same transaction over related tables where combined
        results must be consistent (balance totals, integrity checks, backup scans).
Grep:   Multiple SELECT statements in the same transaction scope accessing related
        tables (e.g., accounts + transfers, orders + order_items)
Risk:   At read committed, each SELECT reads a fresh snapshot. Concurrent commits
        between reads produce internally inconsistent results.
```

**Lost updates — Pattern: read-modify-write cycle**
```
Signal: A transaction reads a value, computes a new value in application code,
        then writes the new value back.
Grep:   SELECT followed by UPDATE in the same transaction scope where the UPDATE
        value depends on the SELECT result (look for the variable being used in both)
        ORM: find() / find_by() followed by .update() or .save()
        Python: result = session.query(...).one() ... result.field += delta ... session.commit()
        Java:   Entity e = em.find(...) ... e.setCount(e.getCount() + 1) ... em.merge(e)
Risk:   Two concurrent read-modify-write cycles both read the old value, both compute
        an update, and the second write overwrites the first without incorporating it.
        At read committed: always vulnerable.
        At PostgreSQL/Oracle snapshot isolation: automatically detected and aborted.
        At MySQL InnoDB repeatable read: NOT detected — second write silently overwrites first.
Severity: HIGH at read committed or MySQL repeatable read. MEDIUM at PostgreSQL/Oracle
          snapshot isolation (aborts, requires retry). NOT PRESENT at serializable.
```

**Write skew — Pattern: check-then-act (the most commonly missed anomaly)**
```
Signal: A transaction reads an aggregate or existence condition, makes a decision
        based on the result, then writes to the database. The write changes the
        state that the condition was checking.
Grep:   SELECT COUNT(*) / SELECT SUM() / SELECT EXISTS() / SELECT MAX() followed by
        INSERT, UPDATE, or DELETE in the same transaction scope.
        Also: any SELECT that is used as a guard condition ("if the query returns X,
        proceed with the write")
ORM:    Model.where(...).count > 0 followed by Model.create() or model.update()
        Model.where(...).exists? followed by record.save()
Risk:   Two concurrent transactions both pass the guard check because each reads
        from its own snapshot. Both write. The combined state violates the invariant
        the guard was enforcing.
Critical: Write skew is NOT prevented by snapshot isolation. Oracle's "serializable"
          is snapshot isolation. If the database is at any level below true serializable,
          ALL check-then-act patterns are vulnerable.
Severity: CRITICAL at read committed, snapshot isolation, or Oracle "serializable".
          NOT PRESENT at true serializable (PostgreSQL SERIALIZABLE, MySQL SERIALIZABLE).
```

**Phantom reads — Pattern: check-for-absence then insert**
```
Signal: SELECT COUNT(*) = 0 or empty-result check, followed by INSERT into the
        same table. Booking conflict checks, username existence checks.
Grep:   COUNT.*= 0 / .count() == 0 followed by INSERT or .create() in same scope
Risk:   Both transactions see zero matching rows. Both insert. Constraint violated.
        FOR UPDATE does not help — no rows exist to lock when SELECT returns empty.
Severity: CRITICAL at any level below serializable (including snapshot isolation).
Note:   Phantom variant of write skew. Fix: serializable isolation or materializing
        conflicts. UNIQUE constraint sufficient only for single-column uniqueness.
```

---

### Step 3: Classify Each Finding

**ACTION:** For each code location identified in Step 2, produce a structured finding entry.

**WHY:** Unclassified findings — "there might be a race condition somewhere" — do not produce action. A structured finding with anomaly type, trigger conditions, severity, and a concrete fix recommendation is actionable. The classification also determines severity precisely: the same read-modify-write pattern is critical at read committed but harmless at serializable.

**Finding structure:**

```
Finding #N
  File:            [path/to/file.py, line N]
  Anomaly type:    [dirty read | dirty write | read skew | lost update | write skew | phantom]
  Code pattern:    [brief description of what the code does]
  Trigger:         [concurrency condition required to produce the anomaly]
  Severity:        [CRITICAL | HIGH | MEDIUM | LOW] (see severity table below)
  Affected data:   [which tables/entities are involved]
  Fix:             [isolation upgrade | SELECT FOR UPDATE | atomic operation | unique constraint | materializing conflicts]
  Fix detail:      [specific change to make]
```

**Severity classification:**

| Anomaly | Severity | Rationale |
|---------|----------|-----------|
| Dirty read | HIGH | Reads data that may never have existed (rolled-back write). Direct data integrity violation. |
| Dirty write | HIGH | Mixes writes from concurrent transactions into a single object. Produces corrupted state. |
| Read skew | MEDIUM | Transaction sees internally inconsistent state. Dangerous for analytics, backups, multi-step reads. |
| Lost update | HIGH | Silent data loss — one write disappears without error. Counter increments, balance updates. |
| Write skew | CRITICAL | Invariant violation that no weaker isolation level prevents. Often produces constraint violations in business logic (zero doctors on call, double-booked rooms, negative balances). |
| Phantom (write skew variant) | CRITICAL | Same as write skew but additionally cannot be mitigated by SELECT FOR UPDATE — only serializable isolation or materializing conflicts works. |

**Downgrade severity if:**
- The anomaly is prevented by the effective isolation level (e.g., lost update at PostgreSQL repeatable read → NOT PRESENT)
- The code path is read-only and cannot cause the write side of the pattern
- The affected data has a compensating unique constraint in the schema

---

### Step 4: Produce the Findings Report

**ACTION:** Write a structured anomaly findings report with all classified findings, a summary table, and prioritized fix recommendations.

**WHY:** The findings report is the deliverable. It must be readable by an engineer without re-reading this skill, actionable as a review ticket or backlog item, and precise enough to be used as evidence in an incident post-mortem. The summary table gives a quick severity overview; the detailed findings give the information needed to implement a fix.

**Output format:**

```markdown
# Concurrency Anomaly Scan — [Project Name]

## Scan Context

Database:            [database + version]
Effective isolation: [actual isolation level in use]
Files scanned:       [count or list]
Findings:            [N total — X CRITICAL, Y HIGH, Z MEDIUM, W LOW]

---

## Summary Table

| # | File | Anomaly Type | Severity | Fix Type |
|---|------|-------------|----------|----------|
| 1 | payments/transfer.py:47 | Write skew | CRITICAL | Upgrade to serializable |
| 2 | scheduling/shift.py:112 | Write skew | CRITICAL | SELECT FOR UPDATE or serializable |
| 3 | accounts/balance.py:33 | Lost update | HIGH | Atomic operation or serializable |
...

---

## Findings

### Finding #1 — [Anomaly Type] — [Severity]
**File:** [path:line]
**Pattern:** [what the code does]
**Trigger:** [concurrency scenario that produces the anomaly]
**Affected data:** [tables/entities]

**Code excerpt:**
[relevant code snippet]

**Fix:** [fix type]
[specific change description]

---

[repeat for each finding]

---

## Recommendations

### Immediate (CRITICAL findings)
[List of changes required before the next production deployment]

### Short-term (HIGH findings)
[List of changes to address in the current sprint]

### For review (MEDIUM findings)
[List of changes to assess — may depend on workload characteristics]

### Related skills
- `transaction-isolation-selector` — select the minimum safe isolation level for this codebase
- `replication-failure-analyzer` — if findings include distributed transaction concerns
```

---

## The 6 Anomalies — Quick Reference

| Anomaly | What happens | Code signal | Minimum fix |
|---------|-------------|-------------|-------------|
| **Dirty read** | Transaction reads uncommitted data that later rolls back — decision based on data that never existed | Read uncommitted isolation explicitly set | Enable read committed (database default) |
| **Dirty write** | Two uncommitted writes to the same object mix results — listing shows one buyer, invoice shows another | Multi-step writes with no transaction boundary; autocommit enabled | Wrap in transaction (read committed prevents) |
| **Read skew** | Long-running read sees two tables at different points in time — Alice's $1000 appears as $900 mid-transfer | Multiple SELECTs over related tables in one transaction | Upgrade to snapshot isolation (REPEATABLE READ) |
| **Lost update** | Read-modify-write cycle: both transactions read 42, both write 43, result is 43 not 44 — one update silently lost | SELECT followed by UPDATE where new value computed in app code | Atomic SQL (`value = value + 1`) or SELECT FOR UPDATE |
| **Write skew** | Check-then-act: two transactions both pass a guard check (count >= 2), both write to different rows, combined result violates the invariant (count = 0). The 5 forms: at-least-one, no-overlap, unique claim, budget, game state | SELECT COUNT/SUM/EXISTS followed by INSERT/UPDATE/DELETE in same transaction | SELECT FOR UPDATE (rows exist) or serializable isolation |
| **Phantom (write skew)** | Check-for-absence then insert: both see zero conflicts, both insert — double-booking, duplicate username | COUNT = 0 check followed by INSERT matching same condition | Serializable isolation; UNIQUE constraint for single-column uniqueness; materializing conflicts as last resort |

Full detail with SQL and ORM patterns per language is in `references/anomaly-detection-patterns.md`.

---

## What Can Go Wrong

**The most dangerous gap:** Write skew is the anomaly teams most commonly miss. It looks like safe code — each transaction individually is correct. The invariant violation only appears in the combined outcome of two concurrent transactions. At any isolation level below true serializable (including PostgreSQL's snapshot isolation, Oracle's "serializable"), write skew is possible.

**The naming trap:** Oracle's `SERIALIZABLE` is snapshot isolation. Teams that set Oracle isolation to SERIALIZABLE and assume they have full protection against write skew do not. MySQL's `REPEATABLE READ` does not detect lost updates. These naming mismatches have caused real production data corruption.

**Testing cannot catch these:** Concurrency anomalies only manifest when two transactions interleave at precisely the wrong time. This is nondeterministic and depends on load. Unit tests run single-threaded. Load tests may not hit the exact timing window. The only reliable method is structural code analysis — which is what this skill does.

---

## Examples

### Example 1: E-Commerce Inventory Deduction (Lost Update)

**Scenario:** A Python Flask service handles concurrent purchase requests. When an order is placed, the code reads inventory, checks if stock > 0, deducts the quantity, and saves.

**Trigger:** "We occasionally oversell products — orders go through for items that are actually out of stock. It only happens during flash sales."

**Process:**

Step 1: Database is PostgreSQL, default isolation is read committed. No isolation override found in the codebase.

Step 2: Grep finds this pattern in `orders/inventory.py`:
```python
# orders/inventory.py:34
with db.session.begin():
    item = db.session.query(InventoryItem).filter_by(sku=sku).one()
    if item.quantity < requested_qty:
        raise InsufficientStock()
    item.quantity -= requested_qty
    db.session.commit()
```

This is a read-modify-write cycle: read `item.quantity`, compute `item.quantity - requested_qty` in application code, write back.

Step 3 classification:
```
Finding #1
  File:         orders/inventory.py:34
  Anomaly type: Lost update
  Code pattern: Read quantity → check > 0 → deduct in application code → save
  Trigger:      Two concurrent purchase requests for the same SKU both read quantity=5,
                both check 5 >= 2 (requested), both compute 5-2=3, both write 3.
                Result: quantity=3 instead of quantity=1. One purchase's deduction is lost.
  Severity:     HIGH
  Affected data: InventoryItem.quantity
  Fix:          Atomic SQL operation (no read-modify-write cycle needed)
  Fix detail:   Replace with:
                UPDATE inventory_items
                  SET quantity = quantity - :requested_qty
                  WHERE sku = :sku AND quantity >= :requested_qty
                Check rows_affected == 1 to detect insufficient stock.
                This removes the application-layer read-modify-write cycle entirely.
```

**Output excerpt:**
```markdown
# Concurrency Anomaly Scan — E-Commerce Service

Database:            PostgreSQL 14
Effective isolation: Read committed (default, no override found)
Files scanned:       47
Findings:            1 total — 0 CRITICAL, 1 HIGH, 0 MEDIUM, 0 LOW

## Summary Table
| # | File | Anomaly Type | Severity | Fix Type |
|---|------|-------------|----------|----------|
| 1 | orders/inventory.py:34 | Lost update | HIGH | Atomic SQL operation |

## Finding #1 — Lost Update — HIGH
...
Fix: Replace Python read-modify-write with atomic SQL UPDATE with WHERE guard.
The atomic UPDATE eliminates the window for concurrent reads of the same value.
No isolation level change required for this fix.
```

---

### Example 2: Scheduling Service (Write Skew — Classic Pattern)

**Scenario:** A Java Spring Boot service manages staff shift assignments. Staff can voluntarily release a shift if at least two others are assigned to cover it.

**Trigger:** "A shift ended up with zero assigned staff after two people simultaneously clicked 'release' on the app. Both got a confirmation that their release was accepted."

**Process:**

Step 1: Database is MySQL InnoDB, isolation is repeatable read (default). No override configured.

Step 2: Grep finds this pattern in `ShiftService.java`:
```java
// ShiftService.java:87
@Transactional
public void releaseShift(long staffId, long shiftId) {
    long coverCount = shiftRepository.countAssigned(shiftId);  // SELECT COUNT(*)
    if (coverCount < 2) {
        throw new InsufficientCoverageException();
    }
    staffShiftRepository.markReleased(staffId, shiftId);       // UPDATE staff_shifts
}
```

Step 3 classification:
```
Finding #1
  File:         ShiftService.java:87
  Anomaly type: Write skew
  Code pattern: COUNT assigned staff → if >= 2 → mark self as released
  Trigger:      Alice and Bob are both assigned, both click Release simultaneously.
                Both transactions read COUNT = 2 (their own snapshot). Both pass the
                check. Alice's UPDATE sets her record to released. Bob's UPDATE sets
                his record to released. Result: COUNT = 0. Zero staff on shift.
  Severity:     CRITICAL
  Affected data: staff_shifts table
  Fix:          SELECT FOR UPDATE on the precondition query, or upgrade to SERIALIZABLE
  Fix detail:
    Option A — SELECT FOR UPDATE:
      Replace countAssigned() with a locking query:
        SELECT COUNT(*) FROM staff_shifts
          WHERE shift_id = ? AND status = 'assigned'
          FOR UPDATE
      This locks all assigned rows for the shift. Bob's transaction must wait
      for Alice's to commit. After Alice commits (count becomes 1), Bob reads
      count = 1 and throws InsufficientCoverageException. Correct behavior.
    Option B — Serializable isolation:
      Add @Transactional(isolation = Isolation.SERIALIZABLE) to the method.
      MySQL SERIALIZABLE uses two-phase locking — true serializable.
      Note: adds lock contention overhead on the staff_shifts table.
```

---

### Example 3: Multi-Tenant SaaS Subscription Billing (Read Skew + Write Skew)

**Scenario:** A Node.js billing service runs a monthly billing job. The job reads each account's subscription plan and usage, computes the invoice total, and inserts an invoice record. The job runs while normal usage continues.

**Trigger:** "Our monthly billing report shows totals that don't match usage records. Some invoices have usage figures that don't correspond to any committed state we can find."

**Process:**

Step 1: Database is PostgreSQL, isolation is read committed (default). The billing job uses a long-running transaction.

Step 2: Grep finds two issues:

Issue A — `billing/job.js:23`: The billing job reads usage in a loop over accounts. Each loop iteration issues a new SELECT. Between iterations, usage records for already-billed accounts may be updated by concurrent write transactions. The job reads accounts at different points in time.

Issue B — `billing/proration.js:67`: A proration credit calculation reads the current plan price and the days remaining, computes a credit, then inserts a credit record. A concurrent plan upgrade transaction can commit between the two reads, leaving the proration based on the old plan price while the new plan is active.

Step 3 classification:
```
Finding #1
  File:         billing/job.js:23
  Anomaly type: Read skew
  Code pattern: Long-running job reads multiple tables across loop iterations with
                separate SELECT queries per account — no consistent snapshot
  Trigger:      Concurrent write transactions commit usage updates between account reads.
                Job sees Account A's usage before the update and Account B's usage after.
  Severity:     MEDIUM
  Affected data: usage_records, subscriptions, accounts tables
  Fix:          Set transaction isolation to REPEATABLE READ or SERIALIZABLE for the
                billing job transaction. PostgreSQL REPEATABLE READ = snapshot isolation.
                All reads within the transaction see the database at the transaction's
                start time. Concurrent writes are invisible until the transaction commits.

Finding #2
  File:         billing/proration.js:67
  Anomaly type: Write skew
  Code pattern: Read current plan price → read days remaining → compute credit →
                insert credit record. Write changes the precondition (plan price).
  Trigger:      Plan upgrade commits between the two reads. Credit is computed at
                old plan price but inserted while new plan is active.
  Severity:     CRITICAL
  Fix:          SELECT plan_price FROM subscriptions WHERE id = ? FOR UPDATE before
                reading days remaining. This locks the subscription row for the
                duration of the transaction. A concurrent plan upgrade must wait.
```

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/anomaly-detection-patterns.md` | SQL and ORM grep patterns for all 6 anomaly types; per-language examples (Python/SQLAlchemy, Java/Hibernate, Go/sqlx, Ruby/ActiveRecord, Node.js/Sequelize); false positive filters | Step 2 — systematic grep sweep |
| `references/severity-and-fix-matrix.md` | Full severity table per anomaly type per isolation level; fix decision tree (isolation upgrade vs FOR UPDATE vs atomic op vs unique constraint vs materializing conflicts); fix applicability conditions | Step 3 — classifying each finding and selecting a fix |

**Cross-reference:** `transaction-isolation-selector` — use after this skill produces its findings report. That skill takes the anomaly exposure as input and produces the minimum safe isolation level recommendation with database-specific configuration.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-transaction-isolation-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
