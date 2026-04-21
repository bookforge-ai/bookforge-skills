---
name: pessimistic-offline-lock-implementer
description: "Use when offline-concurrency-strategy-selector (or your team) has chosen Pessimistic Offline Lock and you need to implement it correctly end-to-end. Handles: pessimistic locking, pessimistic offline lock, record locking, exclusive lock, lock manager design, lock timeout policy, acquire and release lock, stale lock cleanup, force release of abandoned locks, editing session lock, concurrent edit lock, edit lock implementation, record check-out pattern, lock table schema, durable lock storage (database-backed vs Redis vs in-memory), lock owner identity (user+session), coarse-grained lock at aggregate root (shared-version token vs root lock), implicit lock via base-class mapper / LockingMapper decorator / ORM interceptor / AOP aspect. Three-phase implementation: (1) choose lock type (exclusive-write vs exclusive-read vs read-write), (2) build durable lock manager (acquire/release/releaseAll/timeout), (3) define lock protocol (when to acquire, scope, release triggers, force-release, deadlock avoidance). Anti-pattern audit: SELECT FOR UPDATE across user think-time, in-memory lock table in clustered deployment, missing timeout policy, no owner identity, implicit-lock gaps, mixing optimistic with pessimistic carelessly. Produces a Pessimistic Offline Lock implementation plan covering lock type, storage choice, manager API, protocol spec, Coarse-Grained Lock integration, Implicit Lock wiring, UX spec (who holds lock + force-release), and test plan."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/pessimistic-offline-lock-implementer
metadata: {"openclaw":{"emoji":"🔐","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
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
  - pessimistic-locking
  - concurrency
  - locking
  - transactions
  - design-patterns
  - data-integrity
  - offline-lock
  - record-locking
depends-on:
  - offline-concurrency-strategy-selector
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Persistence layer (mapper, repository, ORM entities), session management code, and schema files for the entities requiring concurrent-edit protection"
    - type: user-description
      description: "Stack and ORM, which entities need locking, deployment topology (single-server vs clustered), aggregate boundaries, expected edit duration, and whether schema changes are possible"
  tools-required:
    - Read
    - Grep
    - Edit
    - Write
  tools-optional:
    - Glob
  mcps-required: []
  environment: "Application with multi-step editing workflows (record opened in one HTTP request, saved in a later one) where conflict cost is high. Relational database with ORM or hand-rolled persistence. Stack-agnostic: Java/Spring, C#/.NET, Python/Django, Node.js, Ruby on Rails all apply."
discovery:
  goal: "Implement Pessimistic Offline Lock with correct lock type, durable lock manager, protocol, Coarse-Grained Lock for aggregates, and Implicit Lock for safety."
  tasks:
    - "Confirm offline-concurrency-strategy-selector chose Pessimistic (or confirm from context)"
    - "Choose lock type: exclusive-write (most common), exclusive-read, or read-write"
    - "Design durable lock table schema with owner identity, acquired_at, and optional expires_at"
    - "Implement atomic acquire (INSERT with uniqueness enforcement) and release (DELETE) operations"
    - "Define timeout policy: absolute timeout + session-invalidation-triggered release"
    - "Define the protocol: acquire before load, scope per entity-ID, abort immediately on unavailability"
    - "Add Coarse-Grained Lock if aggregate integrity matters (shared-version token or root lock)"
    - "Add Implicit Lock via LockingMapper decorator or base-class repository to prevent gaps"
    - "Specify force-release authorization and lock-owner display UX"
    - "Audit anti-patterns: SELECT FOR UPDATE long-held, in-memory lock in cluster, no timeout, no owner"
    - "Write concurrent-acquire test and timeout test"
    - "Produce Pessimistic Offline Lock implementation plan"
  audience:
    roles:
      - backend-engineer
      - software-architect
      - tech-lead
    experience: intermediate
  when_to_use:
    triggers:
      - "offline-concurrency-strategy-selector output specifies Pessimistic Offline Lock"
      - "Users lose significant work when a save is rejected at commit time (high rework cost)"
      - "Implementing record check-out / edit-lock to prevent concurrent editing"
      - "Designing a lock manager with acquire, release, and timeout for long-running edits"
      - "Auditing an existing pessimistic locking implementation for correctness"
      - "Adding aggregate-level (Coarse-Grained) locking so all members lock together"
      - "Preventing implicit-lock gaps by moving lock acquisition into the framework layer"
      - "Designing the 'locked by Alice' UX and force-release admin flow"
    prerequisites:
      - "offline-concurrency-strategy-selector has been run (or Pessimistic is confirmed appropriate)"
    not_for:
      - "Systems where all business transactions fit in a single DB transaction — use isolation levels instead"
      - "Low-collision, low-rework-cost workflows — use optimistic-offline-lock-implementer"
      - "Thread-level concurrency within a single request (use language-level synchronization)"
      - "Distributed consensus problems (Raft, Paxos, saga patterns)"
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
    assertion_count: 14
    iterations_needed: null
---

# Pessimistic Offline Lock Implementer

## When to Use

This skill implements the Pessimistic Offline Lock pattern after `offline-concurrency-strategy-selector` (or your team) has confirmed it is the right concurrency strategy. The pattern applies when a business transaction spans multiple HTTP requests — user opens a record, edits for minutes or hours, then saves — AND the rework cost of a late collision rejection is unacceptably high.

The core trade-off: Optimistic Offline Lock detects conflicts at commit time (user loses work already done). Pessimistic Offline Lock prevents conflicts at load time (user sees "locked by Alice" immediately, before doing any work). Use Pessimistic when late failure is genuinely unacceptable — insurance policy underwriting, complex order editing, legal document authoring.

**Do not use** if collisions are rare and rework cost is low (use optimistic instead). **Do not use** if the entire workflow fits in a single DB transaction (use isolation levels).

## Context & Input Gathering

Gather the following before proceeding. Grep the codebase or ask the user directly.

**Required:**
1. **Lock type decision** — does the business transaction need to lock on READ, on WRITE, or both? (see Phase 1)
2. **Entities requiring locking** — which tables/domain classes must be locked during editing?
3. **Aggregate boundaries** — are multiple objects edited together as a unit (Order + LineItems, Policy + Coverages)?
4. **Deployment topology** — single-server or clustered? (determines lock storage choice)
5. **Session management** — HTTP sessions, JWT tokens, or custom session IDs? (determines owner identity)
6. **Schema mutability** — can a lock table and a version table be added?

**Observable from codebase:**
- `SELECT FOR UPDATE` or database-native lock hints → likely held across user think-time (anti-pattern — flag it)
- Existing `app_lock` or `lock_table` → partial implementation; audit for missing timeout, owner identity
- Session management code → determines how to register release-on-session-end listener
- Aggregate relationships in domain objects → identifies Coarse-Grained Lock candidates

**Sufficiency:** Proceed when lock type, entity list, and deployment topology are known.

---

## Process

### Phase 1 — Choose Lock Type

Choose the lock type before writing any code. This is a domain decision that must be validated with domain experts, not a purely technical one.

**Step 1 — Evaluate the three options:**

**Exclusive write lock (most common — default unless a specific need requires otherwise):**
A business transaction must acquire a lock only to EDIT a record. Multiple sessions may read concurrently; only the editor holds a lock. If stale reads are acceptable (a reader seeing slightly out-of-date data is tolerable), use this. Most enterprise systems need only this level.

**Exclusive read lock (most restrictive):**
A business transaction must acquire a lock to READ OR EDIT. Only one session accesses the record at a time. Use when the correctness of the business transaction depends on having the most recent data even for reads — for example, an insurance underwriter whose calculations are based on the values they loaded. Warning: this severely limits concurrency (all readers serialize behind each other).

**Read/write lock (most complex):**
Multiple shared read locks may coexist. An exclusive write lock blocks all read and write locks. No write lock can be granted while any read lock exists. Use when: read activity is heavy, editing is occasional, and read freshness matters for readers. More complex to implement (requires counting read lock holders) and harder for domain experts to reason about.

**WHY:** The lock type controls who can proceed concurrently and who gets blocked. An exclusive read lock applied system-wide makes the system behave like a single-user system. A wrong lock type cannot be rescued by a correct technical implementation — it will either create unacceptable data contention or fail to prevent conflicts. Fowler: "the wrong lock type can't be saved by a proper technical implementation."

**Decision rule:**
- DEFAULT → Exclusive write lock
- Readers must always see latest data → Exclusive read lock
- High concurrent read traffic + occasional editing + read freshness → Read/write lock

---

### Phase 2 — Build the Lock Manager

**Step 2 — Choose lock storage**

The lock table must be durable and visible to all application nodes. Choose one:

| Storage | Best for | Caution |
|---------|----------|---------|
| Same relational DB (dedicated table) | Most enterprise apps; reuses existing DB; leverages DB uniqueness constraints for atomicity | Adds load to primary DB; acceptable at normal scale |
| Redis with persistence (AOF/RDB) | Systems already using Redis; built-in TTL simplifies timeout | Must configure persistence (eviction policies); Redis failure = all locks lost |
| Dedicated lock service (Zookeeper, etcd) | Large distributed systems with strict consistency requirements | Heavy infrastructure; rarely justified for typical enterprise apps |
| In-process memory (Singleton map) | Only on single-server deployments with no restart concern | Locks lost on restart; invisible to other nodes — NEVER use in clustered deployments |

**WHY:** Lock durability is not optional. A server restart or process crash must not silently release all locks and allow concurrent editing to proceed unchecked. If the lock store is in-process memory and the application is clustered, node A's locks are invisible to node B — the entire scheme fails silently.

**Step 3 — Design the lock table schema**

```sql
CREATE TABLE app_lock (
  lockable_id   BIGINT       NOT NULL,   -- primary key of the locked entity
  owner_id      VARCHAR(255) NOT NULL,   -- session ID or user+session composite
  lock_type     VARCHAR(20)  NOT NULL,   -- 'exclusive_write', 'exclusive_read', 'read', 'write'
  acquired_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
  expires_at    TIMESTAMP,               -- NULL = no absolute expiry (rely on session listener)
  PRIMARY KEY (lockable_id, owner_id, lock_type)
);
CREATE INDEX idx_app_lock_owner ON app_lock(owner_id);
CREATE INDEX idx_app_lock_expires ON app_lock(expires_at);
```

See [Lock Table Reference](references/lock-table-reference.md) for per-storage-backend DDL and Redis key structures.

**Step 4 — Implement the lock manager API**

The lock manager exposes exactly four operations. Business transactions interact only with the lock manager — never with the lock table directly.

```
acquireLock(lockableId, ownerId, lockType) → void | throws ConcurrencyException
releaseLock(lockableId, ownerId)           → void
releaseAllLocksFor(ownerId)                → void   (session-end cleanup)
getLockOwner(lockableId)                   → ownerId | null
```

**Atomic acquire (database-backed implementation):**
```sql
-- Exclusive write: succeeds if no row exists for this lockableId
INSERT INTO app_lock (lockable_id, owner_id, lock_type, acquired_at)
VALUES (?, ?, 'exclusive_write', NOW())
-- ON CONFLICT / duplicate key exception → lock held by another session → throw ConcurrencyException
```

**Read/write lock acquire requires a read of the lock table inside a serializable transaction** — the lock table must not have conflicting reads. Prefer exclusive write or exclusive read unless read/write semantics are required; do not implement read/write if the added complexity is unnecessary. See [Lock Manager Reference](references/lock-manager-reference.md) for the full read/write implementation.

**WHY:** The `INSERT` approach uses the database's uniqueness constraint as the atomic "compare-and-set." A separate SELECT + conditional INSERT has a race condition. Throwing immediately (rather than waiting) eliminates deadlock — a business transaction that cannot acquire a lock aborts at the start, before the user has done any work.

**Owner identity:** Use the HTTP session ID as the owner identifier for web applications. For applications without HTTP sessions, use a composite of `userId + businessTransactionId`. The owner identifier must be retrievable from any request within the same business transaction. See Fowler's `AppSession` pattern: store the owner ID in a thread-local or request-scoped container bound to the HTTP session.

**Step 5 — Implement timeout and release mechanisms**

Three release triggers must ALL be wired:

1. **Explicit release on save or cancel:** the command that completes the business transaction calls `releaseLock()` (or `releaseAllLocksFor()`) before returning.

2. **Session-invalidation listener (most critical for web apps):**
   ```java
   // Register on HTTP session creation
   httpSession.setAttribute("lockRemover", new LockRemover(sessionId));

   class LockRemover implements HttpSessionBindingListener {
       public void valueUnbound(HttpSessionBindingEvent e) {
           lockManager.releaseAllLocksFor(sessionId);
       }
   }
   ```
   This fires when the HTTP session expires OR when the user's browser is closed (server-side session timeout). If you omit this, a user closing their browser mid-edit holds the lock until an admin intervenes.

3. **Timestamp-based expiry sweep (defensive backstop):**
   Set `expires_at = NOW() + N_minutes` on acquire. A background job (or lazy check on acquire) cleans up expired locks:
   ```sql
   DELETE FROM app_lock WHERE expires_at < NOW();
   ```
   This backstop handles crashed application nodes where the session listener never fired.

**WHY:** Session abandonment is the most common real-world failure mode. Users close browser tabs, network connections drop, laptops sleep. Without a session-end listener and expiry sweep, a single abandoned session locks a record indefinitely. Fowler: "This is a big deal for a web application where sessions are regularly abandoned by users."

**Timeout duration:** Consult domain experts. A typical policy: absolute lock timeout of 60–120 minutes for long business transactions + idle-detection via heartbeat if the UI supports it (client pings `/session/heartbeat` every 30s; if absent for N minutes, session expires).

---

### Phase 3 — Define the Lock Protocol

**Step 6 — When to acquire**

Acquire the lock BEFORE loading the data, within the same system transaction as the load:

```
1. Begin system transaction
2. acquireLock(entityId, sessionId, lockType)   ← if fails: throw ConcurrencyException, rollback
3. Load entity from DB                           ← guaranteed fresh (lock acquired first)
4. Commit system transaction
5. Present data to user (business transaction now in progress)
```

**WHY:** Acquiring after load creates a window where another session may have modified the record between your load and your lock acquisition. Loading after lock acquisition guarantees you see the most recent committed state. Fowler: "Generally, the business transaction should acquire a lock before loading the data, as there's not much point in acquiring a lock without a guarantee that you'll have the latest version of the locked item."

**Step 7 — Scope and granularity**

Lock on the entity's primary key (the ID, not the in-memory object). This allows acquiring the lock before loading, and ensures the lock can be checked by any code path without requiring the object to be in memory.

For entities that form aggregates, see Phase 4 (Coarse-Grained Lock).

**Step 8 — How to act when a lock is unavailable**

Throw an exception immediately. Never wait for the lock to become available.

```java
public void acquireLock(Long lockableId, String ownerId) throws ConcurrencyException {
    if (hasLock(lockableId, ownerId)) return;  // idempotent: already own it
    try {
        execute("INSERT INTO app_lock (lockable_id, owner_id, ...) VALUES (?, ?, ...)", lockableId, ownerId);
    } catch (DuplicateKeyException e) {
        String currentOwner = getLockOwner(lockableId);
        throw new ConcurrencyException("Record is currently being edited by " + currentOwner);
    }
}
```

**WHY:** Waiting for a lock is only sensible if the wait duration is bounded and short (seconds). A business transaction might take 20 minutes. No user will wait 20 minutes for a lock to become available. Waiting also enables deadlock: user A holds lock on record X and waits for Y; user B holds lock on Y and waits for X — both block forever. "Simply have your lock manager throw an exception as soon as a lock is unavailable. This removes the burden of coping with deadlock" (Fowler).

**Step 9 — Deadlock prevention for multi-record locking**

If a business transaction must acquire locks on multiple records (or multiple aggregate roots), enforce a consistent acquisition order across all business transactions:

- Order by entity type, then by primary key within the type.
- Acquire all locks before presenting any data to the user.

**WHY:** Deadlock arises when transaction A holds lock on entity 1 and needs entity 2, while transaction B holds lock on entity 2 and needs entity 1. With immediate-throw (Step 8), deadlock produces a fast ConcurrencyException for one party rather than an indefinite hang. Consistent ordering further reduces the frequency.

---

### Phase 4 — Add Coarse-Grained Lock for Aggregates

**Step 10 — Determine if aggregate locking applies**

An aggregate is a cluster of related objects treated as a unit for data changes (for example, a Lease and its Assets, an Order and its LineItems, a Policy and its Coverages). If editing any member of the group without locking the others could produce inconsistent data, a Coarse-Grained Lock is needed.

IF aggregate exists → add Coarse-Grained Lock. IF objects are independently lockable → skip this phase.

**Step 11 — Choose Coarse-Grained Lock implementation**

**Option A — Shared version token (preferred when also using Optimistic as a complement):**
Create a single `version` table row per aggregate. Every entity in the aggregate references the same version row by ID. To lock the aggregate, lock the version row's ID in the lock table. Acquiring this one lock effectively locks all members.

```sql
CREATE TABLE version (id BIGINT PRIMARY KEY, value BIGINT, modified_by VARCHAR, modified TIMESTAMP);
-- Each aggregate member stores: version_id BIGINT REFERENCES version(id)
```

Lock acquisition: `acquireLock(version.id, sessionId)` — one lock covers the entire aggregate.

**Option B — Root lock (navigate to aggregate root):**
Designate the aggregate root (the entity that provides the single access point to the group). Lock the root's ID. Any code path locking any member must navigate to the root first and lock that instead. Fowler: "locking either the asset or the lease ought to result in the lease and all of its assets being locked."

Navigation tip: use Lazy Load when traversing to the root to avoid loading the entire object graph. Cache the root ID in each member (direct reference) to avoid recursive traversal performance costs.

**WHY:** Without Coarse-Grained Lock, locking individual members requires every code path to enumerate all members of the group. As the group grows, this becomes error-prone. "Having a separate lock for individual objects presents a number of challenges. First, anyone manipulating them has to write code that can find them all in order to lock them" (Fowler). A single lock point eliminates this complexity and prevents the scenario where two sessions lock different members concurrently, neither aware of the other's intent.

---

### Phase 5 — Add Implicit Lock Safety Net

**Step 12 — Identify the mandatory lock tasks**

Compile the list of tasks that must happen for the locking scheme to be correct:

- **For exclusive read lock:** acquire lock before any `find()` call; release all locks on session end.
- **For exclusive write lock:** acquire lock before any `update()` or `delete()` call; verify write lock is held at commit.
- **For read/write lock:** acquire read lock before `find()`; acquire write lock before `update()`/`delete()`.

**Step 13 — Move mandatory tasks into the framework layer**

The goal: a developer writing a new repository method or command object cannot accidentally skip the lock call.

**LockingMapper decorator (Fowler's approach):**
```java
class LockingMapper implements Mapper {
    private final Mapper impl;
    private final LockManager locks;

    public DomainObject find(Long id) {
        locks.acquireLock(id, AppSessionManager.getSession().getId());
        return impl.find(id);   // acquireLock is idempotent if already held
    }
    public void update(DomainObject obj) {
        // For write lock: verify lock is held; throw assertion if not
        if (!locks.hasLock(obj.getId(), currentSessionId())) {
            throw new ConcurrencyException("Write attempted without acquiring lock first");
        }
        impl.update(obj);
    }
}

// Wire in the mapper registry:
class LockingMapperRegistry {
    public Mapper getMapper(Class cls) {
        return new LockingMapper(rawMappers.get(cls), lockManager);
    }
}
```

**Alternative integration points:**
- **Abstract repository base class:** `AbstractRepository.findForEdit(id)` always acquires; concrete repos inherit.
- **ORM lifecycle hooks:** Hibernate `@PostLoad` event, EF Core `ChangeTracker.Tracked` event, SQLAlchemy `after_bulk_update` event.
- **AOP aspect / interceptor:** annotate editing methods `@RequiresLock`; an aspect acquires the lock transparently.

**WHY:** "The key to any locking scheme is that there are no gaps in its use. Forgetting to write a single line of code that acquires a lock can render an entire offline locking scheme useless" (Fowler). "If an item might be locked anywhere it must be locked everywhere." Implicit Lock moves the lock call out of the developer's hands for mandatory operations; for write locks (which require a user-facing decision point), the framework validates that the lock is already held rather than acquiring it implicitly.

**Write lock limitation:** Do not implicitly ACQUIRE write locks — only verify they were acquired. Acquiring a write lock implicitly (e.g., in `update()`) presents the user with a failure mid-work if the lock is unavailable. The intent of Pessimistic Offline Lock is to fail early (at edit start), not mid-work.

---

### Phase 6 — Anti-Pattern Audit

**Step 14 — Check for these failure modes:**

- [ ] **`SELECT FOR UPDATE` held across user think-time:** A DB-native lock held for 20 minutes ties up a DB connection for 20 minutes, serializing all other DB access. Replace with the application-level lock table.
- [ ] **In-memory lock table in clustered deployment:** Locks visible only on node A. Node B has no knowledge of them. Fix with DB-backed or Redis-backed lock store.
- [ ] **No timeout policy:** User closes browser; lock held forever. Fix with session-invalidation listener + expiry sweep.
- [ ] **No owner identity:** Cannot display "locked by X" in the UI. Cannot force-release someone else's stale lock. Fix by recording `owner_id` (user+session) with every lock row.
- [ ] **Implicit-lock gap:** A new code path (admin endpoint, background job, raw SQL) accesses a locked entity without acquiring the lock. Fix with the LockingMapper or framework hook.
- [ ] **Mixing optimistic and pessimistic on the same record:** Sessions using Optimistic version checks do not see Pessimistic locks — they read and modify records that appear "free" while another session holds a pessimistic lock on them. Pick one strategy per record type and apply it consistently.
- [ ] **Waiting for locks instead of throwing immediately:** Lock wait → deadlock risk + long blocking UI. Always throw `ConcurrencyException` immediately on lock unavailability.
- [ ] **Multi-lock acquisition without consistent ordering:** Two sessions locking (A, B) and (B, A) respectively → deadlock. Enforce canonical ordering.

---

### Step 15 — Define Lock-Owner UX and Force-Release

**Lock-owner display (required):**
When a user attempts to load a locked record and gets a `ConcurrencyException`, the error must tell them:
- WHO holds the lock (display name, not just session ID)
- SINCE WHEN the lock was acquired
- WHEN it will expire (if timeout policy is configured)
- How to request force-release (if admin override exists)

Example: "Policy 12345 is currently being edited by Bob Smith (since 10:47 AM). It will be available after his session ends or at 12:47 PM. [Request force-release] [Try again]"

**Force-release authorization:** Admin users call `lockManager.releaseLock(lockableId, currentOwner)` without being the owner (implement `/admin/locks/{id}/release`). The original owner releases via save or cancel. The expiry sweep releases stale locks automatically.

**WHY:** Without the "locked by X" display, users experience opaque failures. Without force-release, an administrator cannot recover from a crashed session before timeout fires.

---

### Step 16 — Write Concurrency Tests

Four required tests (see [Lock Manager Reference](references/lock-manager-reference.md) for full code):

1. **Concurrent acquire:** two sessions attempt `acquireLock(same_id)` — exactly one succeeds, one gets `ConcurrencyException`.
2. **Idempotent re-acquire:** same session acquires twice — must not throw (hasLock check fires).
3. **Release + re-acquire:** after release, a new session can acquire the same lock.
4. **Timeout/expiry:** lock with short `expires_at`; after expiry, a new session can acquire (sweep cleaned up stale lock).

---

### Step 17 — Produce the Implementation Plan Artifact

Output the Pessimistic Offline Lock Implementation Plan (see Outputs section). A written plan makes all decisions reviewable before code is written and serves as the checklist for implementation review.

---

## Inputs

- Entity/table list requiring concurrent-edit protection
- Stack, ORM, language, and deployment topology (single-server vs clustered)
- Aggregate boundaries (determines Coarse-Grained Lock need)
- Session management mechanism (determines owner identity and release listener)
- Existing persistence code (mapper, repository, or ORM entities)

## Outputs

### Pessimistic Offline Lock Implementation Plan

```markdown
## Pessimistic Offline Lock Implementation Plan: [Feature/Entity Name]

**Date:** YYYY-MM-DD | **Stack:** [ORM / language] | **Entities:** [list]

### 1. Lock Type
**Choice:** Exclusive write / Exclusive read / Read-write
**Rationale:** [why this type fits the access pattern and domain need]

### 2. Lock Storage
**Choice:** Database table / Redis / other
**Rationale:** [single-server vs cluster, existing infrastructure]
**DDL / config:** [schema or Redis key structure]

### 3. Lock Manager API
- acquireLock(lockableId, ownerId [, lockType]) → void | ConcurrencyException
- releaseLock(lockableId, ownerId) → void
- releaseAllLocksFor(ownerId) → void
- getLockOwner(lockableId) → ownerId | null

### 4. Protocol
- **Acquire point:** [on edit-view entry / on EditCommand.init()]
- **Release point:** [on SaveCommand / CancelCommand / session invalidation listener]
- **Timeout policy:** [absolute N minutes; expires_at stored in lock table]
- **Session-end listener:** [HttpSessionBindingListener / session lifecycle hook]
- **Force-release:** [admin endpoint; sweep job for expired locks]

### 5. Coarse-Grained Lock
**Required:** Yes / No
**Scope:** [aggregate root + all members]
**Implementation:** Shared version token / Root lock
**Lock point:** [version.id or root entity ID in lock table]

### 6. Implicit Lock Integration
**Required:** Yes / No
**Integration point:** LockingMapper decorator / abstract repo base class / ORM hook / AOP aspect
**Mandatory tasks automated:** [acquire on find() / verify on update() and delete()]

### 7. UX Specification
- **On lock unavailable:** "Record is currently being edited by [name] (since [time]). Try again or [request force-release]."
- **On session timeout:** "Your editing session has expired. Please reload the record."
- **Force-release flow:** [admin UI / endpoint]

### 8. Anti-Pattern Checklist
- [ ] No SELECT FOR UPDATE held across user think-time
- [ ] Lock store is durable and cluster-visible
- [ ] Timeout policy configured (session listener + expiry sweep)
- [ ] Owner identity stored (display name + session ID)
- [ ] All code paths go through LockingMapper / Implicit Lock
- [ ] No optimistic/pessimistic mixing on the same record type
- [ ] Lock unavailability throws immediately (no wait)
- [ ] Multi-lock ordering enforced

### 9. Test Plan
- [ ] Concurrent acquire: only one session succeeds
- [ ] Idempotent re-acquire by same session
- [ ] Release + re-acquire by new session
- [ ] Timeout/expiry: expired lock is cleaned up and available
- [ ] Session-end listener fires: releaseAllLocksFor called on session invalidation
- [ ] Implicit Lock: find() without prior lock → verifies lock acquired; update() without lock → throws assertion
```

## Key Principles

**1. Pessimistic fails EARLY — that is its entire value proposition.**
The purpose of Pessimistic Offline Lock is to prevent a user from investing 45 minutes in a business transaction only to have it rejected at commit time. Acquiring the lock at edit start means the user knows immediately that the record is locked, before doing any work. Any design that delays lock acquisition diminishes this benefit.

**2. Three phases, in order: lock type → lock manager → protocol.**
Fowler's three-phase implementation is non-negotiable. Choosing the wrong lock type produces either unacceptable contention (exclusive read applied everywhere) or insufficient protection (exclusive write where reads must also be fresh). The lock manager must exist before the protocol can be defined. Protocol defines discipline, not mechanism.

**3. The lock manager must throw immediately — never wait.**
Lock contention in an offline (multi-request) context cannot be resolved by waiting. The holder might be at lunch. A lock wait degrades into a timeout + error anyway — but a late timeout defeats the "fail early" goal and introduces deadlock risk. Throw `ConcurrencyException` on first unavailability, every time.

**4. Durable, cluster-visible lock storage is non-negotiable.**
An in-memory lock table fails silently in three ways: locks lost on restart, locks invisible across cluster nodes, and no audit trail for stale locks. A database lock table costs one extra table and one extra row per active edit session — a trivial overhead compared to the correctness guarantee.

**5. Release must be wired to session end, not only to explicit save/cancel.**
Users abandon sessions constantly: browser closes, laptop sleeps, network drops. If release depends only on explicit save or cancel, every abandoned session holds a lock indefinitely. The session-invalidation listener (HTTP session binding event or equivalent) is the most important release trigger — it fires even when the user does nothing explicit.

**6. Coarse-Grained Lock is required when aggregate integrity matters.**
Locking an Order without locking its LineItems allows another session to modify a LineItem while the Order is held — the aggregate is inconsistent from the first session's perspective. One lock on the aggregate root or shared version token eliminates this class of bug entirely with a single lock acquisition instead of one lock per member.

**7. Implicit Lock is not optional in non-trivial systems.**
A single developer adding a new command object or admin endpoint that bypasses the lock call defeats the entire scheme. The scheme's security is proportional to the thoroughness of its enforcement, and thoroughness requires framework-level enforcement. "The risk of a single forgotten lock is too great" (Fowler).

## Examples

### Example 1: Java/Spring — Insurance Underwriting System

**Scenario:** Underwriters edit complex insurance policies. Sessions last 45–90 minutes. Policies have Coverages, Endorsements, and Named Insureds. Two underwriters occasionally assigned the same policy. Work loss cost: very high.

**Trigger:** "Underwriters are furious about 409 errors after 90 minutes of work. Need to lock policies at edit start."

**Process:**
- Phase 1: Correctness depends on reading fresh data (actuarial tables) → **Exclusive read lock**.
- Phase 2: Single DB, existing Postgres → **DB lock table**. Schema: `app_lock(lockable_id BIGINT PK, owner_id VARCHAR, lock_type VARCHAR, acquired_at TIMESTAMP, expires_at TIMESTAMP)`.
- Phase 3: Protocol — `EditPolicyCommand` acquires lock before `policyMapper.find(id)`. `SavePolicyCommand` releases after commit. `LockRemover` registered on HTTP session as `HttpSessionBindingListener`. Expiry: 120 minutes.
- Phase 4: Policy + Coverages + Endorsements + Named Insureds = aggregate → **Shared version token** (one `version` row per Policy; all members reference it). Lock on `version.id`.
- Phase 5: Multiple command objects in the application → **LockingMapper decorator** wraps all policy-family mappers. `find()` acquires; `update()` verifies lock held.
- UX: "Policy 12345 is being edited by Bob Smith (since 10:47 AM). Available after 12:47 PM. [Request force-release]"

**Output:** DB lock table, 120-minute expiry, LockingMapper, shared version token for Policy aggregate, admin `/admin/locks/policy/{id}/release` endpoint, `LockRemover` session listener.

---

### Example 2: Node.js CMS — Article Editing with Redis

**Scenario:** CMS where editors write and edit published articles. Sessions typically 20–30 minutes. Articles consist of Article + Sections + Tags + Metadata. Node.js, no JVM session management.

**Trigger:** "Add edit locking to prevent two editors opening the same article simultaneously."

**Process:**
- Phase 1: Stale reads acceptable (viewing out-of-date draft is OK) → **Exclusive write lock**.
- Phase 2: Redis already in stack → **Redis lock** with TTL. Key: `lock:article:{id}`, value: `{ ownerId, ownerName, acquiredAt }`, TTL: 2400s (40 min).
- Phase 3: `GET /articles/:id/edit` acquires Redis lock before loading. `PUT /articles/:id` releases after save. Express middleware registers session-end cleanup via `req.session.on('destroy', releaseAllLocksFor(sessionId))`. Heartbeat: client pings `/session/ping` every 30s; absence for 5 minutes triggers server-side expiry.
- Phase 4: Article + Sections + Tags + Metadata → use **root lock** on Article ID (all children navigate to Article as root). One Redis key per article covers the aggregate.
- Phase 5: All article repository methods go through `ArticleRepository` base class. `findForEdit(id)` acquires lock; `update(article)` asserts lock is held.
- UX: "This article is currently being edited by Jane (since 2:10 PM). Try again in ~25 minutes or ask Jane to release the lock."

**Output:** Redis lock with TTL + heartbeat, root lock on Article (aggregate), `ArticleRepository.findForEdit()` acquires implicitly, session-destroy listener.

---

### Example 3: Python/Django — Order-Picking System

**Scenario:** Warehouse pickers claim orders from a queue. Once a picker opens an order, it must be locked so two pickers don't pick the same items. Sessions are short (5–15 min, order completion). DB: PostgreSQL.

**Trigger:** "Two pickers sometimes pick the same order. Add a 'picked by X' locking mechanism with visible status."

**Process:**
- Phase 1: Only pickers who intend to edit (pick) need a lock; browsing the queue is read-only → **Exclusive write lock**.
- Phase 2: Single Postgres DB → **DB lock table**. Include `expires_at` for 30-minute absolute timeout.
- Phase 3: `POST /orders/{id}/claim` acquires lock before loading. `POST /orders/{id}/complete` releases. Django signal `request_started` + session middleware for release-on-session-end. Picker's name stored as `owner_id` (human-readable for UI).
- Phase 4: Order + LineItems + Inventory Reservations = aggregate. Use **root lock** on Order ID. All members navigable from Order. Lock the Order ID only.
- Phase 5: `OrderRepository.claim_for_picking(order_id, picker_id)` is the single entry point; implicit lock built in. No LockingMapper needed (single access path).
- UX: Order card in queue shows "PICKED BY: John D. (since 9:05 AM)" badge. Admin dashboard shows all active locks. Auto-released after 30 minutes if order not completed.

**Output:** `app_lock` table with `expires_at`, expiry sweep task, Order root lock, `claim_for_picking()` as single locked access point, UI "PICKED BY" badge, admin lock dashboard.

## References

- [Lock Table Schema and Storage Backends](references/lock-table-reference.md) — DDL for Postgres/MySQL/SQLite lock table; Redis key structure + TTL config; Zookeeper/etcd notes
- [Lock Manager Implementation Reference](references/lock-manager-reference.md) — Java, Python, and Node.js lock manager implementations; read/write lock state machine; atomic acquire patterns
- [Coarse-Grained Lock Reference](references/coarse-grained-lock-reference.md) — Shared version token implementation (Java example from Fowler); root lock navigation patterns; trade-offs between the two approaches
- [Anti-Pattern Detection Checklist](references/anti-pattern-checklist.md) — Grep patterns and code audit queries for each of the 8 anti-patterns with example buggy code and correct fix

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-offline-concurrency-strategy-selector`
- `clawhub install bookforge-transaction-isolation-level-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
