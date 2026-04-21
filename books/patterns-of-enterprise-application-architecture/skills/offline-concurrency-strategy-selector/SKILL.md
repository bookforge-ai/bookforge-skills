---
name: offline-concurrency-strategy-selector
description: "Use when designing concurrency control for long-running edits where a business transaction spans multiple system transactions — user opens a record, edits for minutes or hours, then saves. Selects between optimistic locking (version column, collision detection at commit) vs pessimistic locking (record check-out, conflict prevention at load time) and decides whether to add Coarse-Grained Lock (aggregate-root lock for multi-object edits) and Implicit Lock (framework-enforced locking to prevent gaps). Handles: lost update prevention, concurrent edit collision detection, offline lock strategy, long-running transaction concurrency, version column design, lock table design, lock timeout policy, aggregate lock, editing concurrency, lock type selection (exclusive-read vs exclusive-write vs read-write). Diagnoses mis-configurations: DB-level locks held across user think-time, implicit-lock gaps, optimistic/pessimistic mixing on overlapping data, timestamp-based versioning pitfalls."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/offline-concurrency-strategy-selector
metadata: {"openclaw":{"emoji":"🔒","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
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
    chapters: [5, 16]
domain: enterprise-application-architecture
tags:
  - concurrency
  - locking
  - transactions
  - design-patterns
  - data-integrity
  - offline-lock
  - optimistic-concurrency
  - pessimistic-concurrency
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Enterprise application codebase (domain, persistence, web layers) or description of the system and its editing workflows"
    - type: user-description
      description: "Description of the business transaction: what the user edits, how long, how many concurrent users, how often they edit the same records, cost of discarding in-progress work"
  tools-required:
    - Read
    - Grep
    - Edit
    - Write
  tools-optional:
    - Glob
  mcps-required: []
  environment: "Enterprise application with at least one multi-step editing workflow (record opened in one request, saved in a later request). Relational database with ORM or hand-rolled persistence layer. Stack-agnostic: Java, C#, Python, TypeScript, Ruby all apply."
discovery:
  goal: "Select the right offline concurrency strategy for each editing workflow and produce a concurrency decision record with infrastructure specifications."
  tasks:
    - "Identify whether the system has genuine offline concurrency (business transaction spans multiple system transactions)"
    - "Apply the collision-frequency × rework-cost framework to choose Optimistic vs Pessimistic Offline Lock"
    - "Within Pessimistic: select lock type (exclusive-write, exclusive-read, or read/write)"
    - "Determine whether Coarse-Grained Lock is needed for aggregate editing"
    - "Determine whether Implicit Lock is needed as a safety net"
    - "Flag anti-patterns: DB-level long locks, implicit-lock gaps, optimistic/pessimistic mis-mix, timestamp versioning"
    - "Produce a concurrency decision record with infrastructure requirements and UX specification"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
    experience: intermediate
  when_to_use:
    triggers:
      - "Designing or auditing any feature where a user opens a record in one HTTP request and saves it in a later one"
      - "Reports of 'lost updates' — one user's changes silently overwriting another's"
      - "Choosing between optimistic and pessimistic locking for a new entity"
      - "Adding concurrency control to a system that currently has none"
      - "Deciding whether to lock at the aggregate root vs individual entity level"
      - "Evaluating whether SELECT FOR UPDATE is safe for long-running user workflows"
      - "Designing collision-detection UX (error message, merge UI, force-reload)"
    prerequisites: []
    not_for:
      - "Single-request workflows where the entire business transaction fits in one system transaction — use database isolation levels instead"
      - "Thread-level concurrency within a single request (use Java synchronization, Go mutexes, etc.)"
      - "Distributed systems consensus (use Raft, Paxos, saga patterns)"
      - "Read-only query concurrency (no writes, no concurrency control needed)"
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

# Offline Concurrency Strategy Selector

## When to Use

This skill applies whenever a **business transaction spans multiple system transactions** — the user loads a record in one HTTP request, works with it (seconds to hours), and saves in a later request. During that gap, the database cannot protect against another user modifying the same data. You need application-level concurrency control.

Use this skill when designing new editing workflows, diagnosing "lost update" bugs, or auditing existing lock strategies. It selects among four patterns from Fowler's *Patterns of Enterprise Application Architecture* Ch 16 and routes to child implementation skills when needed.

**Do not use** if the entire user workflow fits in a single request/transaction — standard database isolation levels are sufficient and far simpler.

## Context & Input Gathering

Gather the following before proceeding. If working from a codebase, grep for session state, version columns, and lock tables. Otherwise, ask the user directly.

**Required:**
1. **Edit duration** — How long does a typical editing session last? (seconds, minutes, hours)
2. **Concurrent user count** — How many users work with the same records simultaneously?
3. **Collision frequency estimate** — How often do two users edit the same record within the same time window? (rare / occasional / frequent)
4. **Rework cost** — If a user's save is rejected due to a conflict, how painful is it to redo? (low: a few fields; high: 30-minute insurance form, complex calculations)
5. **Aggregate structure** — Are records edited in groups? (e.g., Order + LineItems, Customer + Addresses, Lease + Assets)
6. **Infrastructure readiness** — Does a version column or lock table already exist?

**Observable from codebase:**
- Version/timestamp columns in schema files → Optimistic may already be partially in place
- `SELECT FOR UPDATE` or similar → potential long-lock anti-pattern to flag
- Session state storage → helps identify business transaction boundaries

**Sufficiency check:** If collision frequency and rework cost are both unknown, use the heuristic: small internal team + low data overlap → default Optimistic. High-value financial/legal records with multiple editors → investigate Pessimistic.

## Process

### Step 1 — Confirm offline concurrency applies

Check: does the editing workflow span multiple system transactions?

- User loads record in Request A → edits → saves in Request B → YES, offline concurrency applies
- Entire workflow in one request (e.g., API endpoint with no user think-time) → NO, use database isolation levels

**WHY:** All four patterns add complexity and infrastructure. If a single system transaction suffices, the added complexity is pure overhead. The book is explicit: "If you can make all your business transactions fit into a system transaction … then do that."

If offline concurrency applies, proceed. If not, recommend appropriate isolation level and stop.

---

### Step 2 — Apply the primary fork: Optimistic vs Pessimistic

Evaluate:

| Signal | Toward Optimistic | Toward Pessimistic |
|--------|------------------|--------------------|
| Collision frequency | Rare | Frequent |
| Rework cost if conflict | Low (few fields, quick redo) | High (hours of work, complex re-entry) |
| Edit duration | Short (seconds to a few minutes) | Long (30+ minutes, multi-step forms) |
| Concurrency need | High (many users, maximize throughput) | Lower (can accept serialized access) |
| Implementation budget | Lower | Higher (lock manager, timeouts, protocol) |

**Decision:**

- **Low collision × low rework cost → Optimistic Offline Lock** (version-based optimistic concurrency): Add a `version` integer column. On save, include `WHERE version = :loaded_version` in UPDATE/DELETE. If row count = 0 → collision → rollback and surface error with who-modified-and-when.
- **High collision OR high rework cost → Pessimistic Offline Lock** (application-managed pessimistic lock): Acquire a durable application-level lock when the user opens the record. Other users see "locked by Alice" and cannot proceed. Lock released on save or session timeout.
- **Mixed (most records low-risk, some critical) → both** as complements: Optimistic as the default, Pessimistic only for identified high-contention/high-value record types.

**WHY:** Optimistic concurrency trades late failure (discovered at commit) for better throughput and simpler implementation. Pessimistic concurrency trades reduced concurrency for early failure (user knows immediately the record is locked). The correct choice is a UX and domain decision as much as a technical one — it shapes the entire user experience.

**Fowler's default:** "Consider [Optimistic] as the default approach to business transaction conflict management in any system you build. The pessimistic version works well as a complement."

---

### Step 3 — Within Pessimistic: select lock type

If Pessimistic was chosen in Step 2, pick the lock type:

- **Exclusive write lock:** Business transaction must hold a lock to EDIT. Reading is unrestricted. Multiple users can read concurrently; only the editor holds a lock. Best concurrency, simplest. Use when: stale reads are acceptable (viewing slightly out-of-date data is OK).
- **Exclusive read lock:** Business transaction must hold a lock to READ OR EDIT. Only one user accesses the record at a time. Use when: the business transaction's correctness depends on having the latest data even for reads (e.g., an insurance underwriter who builds calculations on what they loaded).
- **Read/write lock:** Read locks are shared (multiple concurrent readers); write lock is exclusive (blocks all read and write locks). Most powerful, most complex. Use when: high concurrent read activity AND occasional editing AND read freshness matters.

**WHY:** The lock type directly controls system concurrency. Exclusive read locks are severe — they serialize ALL access. Most enterprise systems need only exclusive write locks. Read/write locks are a compromise but require careful implementation and are harder for domain experts to reason about.

---

### Step 4 — Check aggregate integrity

Examine the editing workflow:

- Are multiple related objects edited together as a unit? (Order + LineItems, Customer + Addresses, Policy + Coverages)
- Would editing just one member of the group while another session edits a different member cause data integrity problems?

If YES → add **Coarse-Grained Lock** (aggregate-root-level lock / cluster lock):

- **For Optimistic:** Create a shared `Version` object/row that all aggregate members point to (same instance, not equal value). Incrementing the shared version locks the entire group atomically.
- **For Pessimistic:** Use the shared version's ID as the lockable token in the lock table. Locking any member locks all members.
- Alternative: **root lock** — navigate child-to-parent to the aggregate root and lock it; acquiring a root lock locks all descendants by definition.

If NO (objects are independently lockable) → skip Coarse-Grained Lock.

**WHY:** Without Coarse-Grained Lock, per-object locking requires all code paths to know and enumerate every member of the group. This breaks down as the group grows and introduces subtle bugs when a developer forgets to lock one member. Fowler: "locking either the asset or the lease ought to result in the lease and all of its assets being locked."

---

### Step 5 — Check implicit lock safety

Examine the codebase (or planned architecture):

- Are there multiple code paths that access locked records? (different repository methods, admin commands, background jobs, raw SQL paths)
- Could a new developer add a feature without knowing to acquire/release the lock?

If YES → add **Implicit Lock** (framework-enforced lock):

- Move mandatory locking into the abstract Data Mapper / repository base class / ORM lifecycle hooks so it cannot be omitted
- For Optimistic: base mapper supertype handles version storage on load, version check on UPDATE/DELETE
- For Pessimistic: a `LockingMapper` decorator wraps `find()` to always acquire read lock before loading; validates write lock is held before `update()`/`delete()`
- Lock release: register a session lifecycle listener (HTTP session invalidation hook) to call `releaseAllLocks(sessionId)` automatically

If the codebase is tiny or the locking scheme is minimal → may skip, but Fowler: "the risk of a single forgotten lock is too great" in most enterprise applications.

**WHY:** Offline concurrency bugs are extremely hard to reproduce and test. A single missed `acquireLock()` call defeats the entire scheme. "Generally, if an item might be locked anywhere it must be locked everywhere."

---

### Step 6 — Flag anti-patterns

Check for these failure modes in the current or proposed design:

1. **DB-level locks held across user think-time:** `SELECT FOR UPDATE` held open for the duration of a multi-request editing session → DB connection held for minutes/hours, destroys scalability. Flag and replace with application-level lock table.
2. **Timestamp versioning:** Using `modified_at` timestamp as the version marker → unreliable across servers, clock skew causes false-positives and missed conflicts. Replace with an integer `version` counter.
3. **Optimistic/Pessimistic mis-mix on overlapping data:** If the same record is accessed by some sessions using Optimistic and others using Pessimistic, the Pessimistic lock is invisible to the Optimistic sessions — they can read/modify without acquiring the lock. Ensure lock strategy is consistent per record type.
4. **Implicit-lock gaps:** Any code path (admin tool, background job, raw SQL, new command object) that accesses locked records without acquiring the lock. Fix with Implicit Lock.
5. **In-memory lock table in clustered deployment:** Locks on node A are invisible to node B. Fix with database-backed lock table.
6. **Unreleased locks on abandoned sessions:** Users close browsers mid-edit. Locks must expire via timeout policy or session invalidation listener.

**WHY:** Each anti-pattern either silently defeats the locking scheme (invisible gaps) or creates a different operational disaster (DB bottleneck, deadlock in clustered nodes). These are the most common failure modes in production concurrency implementations.

---

### Step 7 — Produce concurrency decision record

Output the artifact (see Outputs section).

## Inputs

- Business transaction description (edit duration, concurrent users, collision frequency, rework cost)
- Domain model / schema (to identify aggregates, existing version columns, lock tables)
- Codebase access (optional, helps detect anti-patterns and existing infrastructure)
- Deployment topology (single-server vs clustered, for lock table implementation choice)

## Outputs

### Concurrency Decision Record (markdown)

```markdown
## Concurrency Decision Record: [Feature/Entity Name]

**Decision date:** YYYY-MM-DD
**Applicable entities:** [list]

### 1. Primary Strategy
**Choice:** Optimistic Offline Lock / Pessimistic Offline Lock / Both (hybrid)
**Rationale:** [collision frequency assessment] × [rework cost assessment] → [reasoning]

### 2. Lock Type (if Pessimistic)
**Choice:** Exclusive write / Exclusive read / Read-write
**Rationale:** [why this lock type fits the access pattern]

### 3. Aggregate Locking
**Coarse-Grained Lock:** Required / Not required
**Scope:** [which objects share the lock]
**Implementation:** Shared version object / Root lock

### 4. Framework Enforcement
**Implicit Lock:** Required / Not required
**Integration point:** Abstract mapper supertype / Mapper decorator / ORM hook / Session listener

### 5. Infrastructure Requirements
- [ ] Version column: `ALTER TABLE <table> ADD COLUMN version INTEGER NOT NULL DEFAULT 0`
- [ ] Lock table: `CREATE TABLE app_lock (lockable_id BIGINT PRIMARY KEY, owner_id VARCHAR(255), acquired_at TIMESTAMP)`
- [ ] Lock timeout policy: [N minutes; auto-release on session invalidation]
- [ ] modifiedBy + modified columns for error messages

### 6. UX Specification
- **On Optimistic collision:** [show error with "Modified by [user] at [time]. Please reload and re-apply your changes."]
- **On Pessimistic lock unavailable:** [show "This record is currently being edited by [user]. Please try again later."]
- **On lock timeout:** [show "Your editing session has expired. Please reload the record."]

### 7. Anti-Pattern Warnings
[List any flagged issues from Step 6]

### 8. Child Implementation Skills Needed
- [ ] optimistic-offline-lock-implementer (version column + mapper mechanics)
- [ ] pessimistic-offline-lock-implementer (lock manager + protocol)
```

## Key Principles

**1. The offline concurrency problem is a domain problem, not just a technical one.**
Collision frequency, rework cost, and lock granularity require domain expert input — not just a DBA. Which records are high-contention? How much time does a user typically spend on a workflow? What's the cost of losing 30 minutes of insurance underwriting? These answers drive the technical choice.

**2. Optimistic is the default; Pessimistic is the exception.**
Optimistic Offline Lock is easier to implement, has no lock infrastructure to maintain, and gives better concurrency. Pessimistic introduces lock managers, timeout policies, session listeners, and deadlock-avoidance concerns. Only adopt Pessimistic when the Optimistic failure mode (late collision discovery) is genuinely unacceptable.

**3. The version counter must be an integer, not a timestamp.**
System clocks are unreliable, especially across multiple servers. A monotonically incrementing integer column provides deterministic conflict detection. Including `modifiedBy` and `modified` columns alongside the version enables user-facing error messages ("Modified by Alice at 2:34pm") but should not replace the integer version in the WHERE clause.

**4. Never hold a database lock across user think-time.**
`SELECT FOR UPDATE` and similar database-native locks hold a DB connection open for the duration. A business transaction that takes 20 minutes would hold that DB resource for 20 minutes, serializing all other access and destroying scalability. Application-level lock tables are the correct tool for cross-request locking.

**5. Coarse-Grained Lock preserves aggregate integrity atomically.**
When an aggregate spans multiple rows/objects (Order + LineItems), locking each object independently creates a window where two sessions lock different members concurrently — neither knows about the other's intent on the group. A shared version object makes this impossible: a single version increment blocks all concurrent attempts on the entire aggregate.

**6. Implicit Lock prevents the #1 failure mode: the forgotten lock call.**
One developer writing one new method without a lock call defeats the entire scheme — and because concurrency bugs are hard to reproduce, it may not be caught in testing. Implicit Lock at the framework level means the developer cannot forget: the base mapper always acquires the lock before loading.

**7. Pessimistic lock managers must never block — always throw immediately.**
When a lock is unavailable, throw an exception instantly. Never wait for the lock to become available. Business transactions that span multiple system transactions cannot reasonably wait: the current holder might be gone for coffee. Immediate failure + early abort is the only practical design; it also eliminates the possibility of deadlock.

## Examples

### Example 1: CMS Article Editor (low collision, low rework cost)

**Scenario:** A content management system where editors write articles. Typical edit session: 10–30 minutes. Team of 5 editors; each article usually has one assigned editor. Collisions rare but possible.

**Trigger:** "We sometimes lose edits when two people accidentally open the same draft. Should we add locking?"

**Process:**
- Step 1: Multi-request workflow (open draft → write → publish) → offline concurrency applies.
- Step 2: Collision frequency = rare; rework cost = moderate (losing 20 min is painful but recoverable) → **Optimistic Offline Lock**.
- Step 3: N/A (Pessimistic not chosen).
- Step 4: Article is a standalone entity; no aggregate integrity concern → no Coarse-Grained Lock.
- Step 5: Single article mapper; small team → **Implicit Lock in abstract mapper** for safety.
- Step 6: No anti-patterns identified if schema is new.

**Output:** Add `version INTEGER NOT NULL DEFAULT 0` + `modified_by` + `modified_at` to articles table. Abstract article mapper includes version in UPDATE WHERE clause. On row count 0 → show "This article was modified by [user] at [time]. Please copy your changes, reload, and re-apply." No lock table needed.

---

### Example 2: Insurance Policy Underwriting (high rework cost)

**Scenario:** Underwriters edit complex insurance policies. Editing a policy takes 45–90 minutes (data gathering, actuarial calculations, document review). Two underwriters might be assigned the same policy. If an underwriter finishes after 90 minutes and their save is rejected, the work is genuinely lost — not a minor inconvenience.

**Trigger:** "Underwriters are furious about rejected saves. Is there a better approach?"

**Process:**
- Step 1: Multi-request, 45-90 min sessions → offline concurrency applies.
- Step 2: Collision rate: low (same policy rarely assigned twice) BUT rework cost: very high → **Pessimistic Offline Lock**.
- Step 3: Underwriters need latest data (coverage amounts, actuarial tables) → **Exclusive read lock** (other underwriters cannot even load the policy while one holds it).
- Step 4: Policy includes Coverages, Endorsements, Named Insureds → these form an aggregate → **Coarse-Grained Lock** with shared version on the Policy root.
- Step 5: Multiple command objects (EditBasicInfo, AddCoverage, RemoveEndorsement) → **Implicit Lock** via LockingMapper decorator.
- Step 6: Flag if existing code uses `SELECT FOR UPDATE` on policy table.

**Output:** Database lock table + shared version on Policy aggregate + LockingMapper + HTTP session expiration listener. UX: "Policy 12345 is currently being edited by Bob Smith. It will be available after his session ends or at [timeout time]."

---

### Example 3: E-commerce Order Management (aggregate integrity)

**Scenario:** Customer service agents edit orders. An order has LineItems, ShippingAddress, and PromoCodes. One agent might add a LineItem while another changes the ShippingAddress at the same time. Each object in isolation is low-risk, but the order must be consistent as a whole.

**Trigger:** "We have a bug where the order total is wrong — looks like two people edited it at the same time."

**Process:**
- Step 1: Multi-request order editing → offline concurrency applies.
- Step 2: Collision frequency: occasional (busy customer service team); rework cost: low → **Optimistic Offline Lock**.
- Step 3: N/A.
- Step 4: Order + LineItems + ShippingAddress + PromoCodes = one aggregate → **Coarse-Grained Lock** with shared version on Order root. Any change to any member increments the shared version, blocking any concurrent session's commit.
- Step 5: Order service has multiple command handlers → **Implicit Lock** in abstract repository.
- Step 6: Verify no per-entity version columns (would create inconsistent locking if mixed with shared version).

**Output:** Single `version` table row per order, referenced by all members. Abstract mapper `update()` calls `order.getVersion().increment()` before any member update. Conflict error: "Order 8834 was modified by [user] at [time]. Please reload to see current state."

## References

- [Offline Concurrency Pattern Details](references/offline-concurrency-patterns.md) — per-pattern mechanics, version column SQL, lock table schema, session listener code sketches
- [Anti-Pattern Catalog](references/concurrency-anti-patterns.md) — detailed detection criteria and remediation for each of the 6 anti-patterns
- [Lock Type Decision Matrix](references/lock-type-matrix.md) — trade-off table for exclusive-write vs exclusive-read vs read-write locks with implementation complexity notes

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-optimistic-offline-lock-implementer`
- `clawhub install bookforge-pessimistic-offline-lock-implementer`
- `clawhub install bookforge-transaction-isolation-level-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
