---
name: unit-of-work-implementer
description: |
  Implement Unit of Work (UoW) — the object that tracks new, dirty, clean, and removed entities
  during a business operation and commits all database changes together in the correct order.
  Use when asked: "how do I implement Unit of Work?", "how does Hibernate Session work under the
  hood?", "how do I avoid N+1 writes?", "how should I structure DbContext scoping?",
  "SQLAlchemy session management best practices", "EntityManager lifecycle", "ORM session
  management", "how to track entity changes in a Data Mapper layer?", "first-level cache",
  "identity map implementation", "object change tracking", "persistence coordination",
  "commit ordering with foreign keys", "how does EF Core SaveChanges work?", "dirty tracking",
  "how to batch database writes?", "UoW pattern implementation", "Hibernate Session vs
  EntityManager", "SQLAlchemy Session scope", "DbContext per-request", "entity state tracking".
  Applies when a Data Mapper pattern is in place (or being introduced) and the team needs
  disciplined change tracking, ordered commits, and first-level caching across a business
  operation. Integrates with Identity Map for cache and identity consistency. Integrates with
  Optimistic Offline Lock via version-conditioned UPDATE. Prerequisite: Data Mapper must be the
  chosen data-source pattern; UoW does not apply cleanly to Active Record (AR handles
  per-object persistence without a coordinator). If the data-source pattern has not been
  chosen, invoke `data-source-pattern-selector` first.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/unit-of-work-implementer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [3, 11]
tags: ["unit-of-work", "persistence", "orm", "data-access", "design-patterns", "object-relational-mapping", "identity-map", "change-tracking", "entity-state", "hibernate", "ef-core", "sqlalchemy", "fowler-peaa"]
depends-on:
  - data-source-pattern-selector
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Persistence layer using Data Mapper pattern (or being refactored to it). Language, ORM framework, and transaction boundary conventions."
    - type: document
      description: "Description of the business operation scope, FK dependencies between entities, and any existing session or context management code."
  tools-required: [Read, Write, Grep]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with access to the codebase. Codebase access is required to identify entity classes, mapper classes, and transaction boundaries."
discovery:
  goal: "Produce a Unit of Work implementation (or ORM-native equivalent) with entity state tracking, ordered commit, Identity Map integration, and lifecycle policy."
  tasks:
    - "Confirm Data Mapper is the chosen data-source pattern (prerequisite check)"
    - "Choose the registration strategy: caller registration, object registration, or UoW-controlled"
    - "Design the UoW API: register methods, commit, rollback, and clear"
    - "Implement four-state tracking: new, dirty, clean, removed"
    - "Implement ordered commit procedure: INSERT (parents first), UPDATE, DELETE (children first), DB COMMIT"
    - "Wire Identity Map integration: all reads through UoW; identity by primary key"
    - "Establish lifecycle management: per-request or per-business-operation scope"
    - "Integrate with Optimistic Offline Lock and Lazy Load collaborators"
    - "Produce implementation sketch + stack-native mapping"
  audience:
    roles: ["senior-backend-engineer", "software-architect", "tech-lead", "framework-designer"]
    experience: "intermediate-to-advanced"
  when_to_use:
    triggers:
      - "Implementing a Data Mapper layer without an ORM and needing change tracking"
      - "Diagnosing too many round trips to the database from a business operation"
      - "Debugging duplicate entity bugs (two objects for the same DB row)"
      - "Scoping ORM sessions or DbContext incorrectly across requests"
      - "Adding optimistic concurrency control and needing a place to execute version-conditioned commits"
      - "Building a Domain Model that needs test isolation from the database"
      - "Retrofitting disciplined transaction management into a persistence layer"
    prerequisites:
      - "Data Mapper selected as the data-source pattern. If not yet chosen, run `data-source-pattern-selector` first."
    not_for:
      - "Active Record codebases — AR handles per-object persistence; a UoW coordinator adds complexity without benefit"
      - "Simple Transaction Script + Table Data Gateway apps — explicit save calls suffice"
      - "Choosing a database product or query optimization"
      - "Distributed transaction coordination (two-phase commit)"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: "{filled by tester}"
      baseline: "{filled by tester}"
      delta: "{filled by tester}"
    tested_at: "{filled by tester}"
    eval_count: "{filled by tester}"
    assertion_count: 14
    iterations_needed: "{filled by tester}"
---

# Unit of Work Implementer

## When to Use

A Unit of Work (UoW) is the coordinator object that tracks every entity touched during a
business operation — newly created, loaded and modified, or deleted — and then flushes all
changes to the database together in the correct order inside a single system transaction.

Use this skill when:
- You have a Data Mapper layer and need change tracking discipline across a business operation
- Your code makes too many database round trips (one UPDATE per field change, not one per commit)
- You are scoping an ORM session (Hibernate `Session`, EF `DbContext`, SQLAlchemy `Session`) and want to understand the underlying contract
- You are implementing a custom Data Mapper layer without a framework and need to track dirty objects
- You are wiring optimistic locking and need a single commit point to run version-conditioned updates

**Prerequisite:** Data Mapper must be the chosen data-source pattern. If it has not been selected, invoke `data-source-pattern-selector` first, or ask the user to confirm their persistence approach before proceeding. UoW adds a coordination layer that Active Record codebases do not need.

---

## Context & Input Gathering

### Required
- **Data-source pattern confirmation:** Verify Data Mapper is in use or being introduced. If Active Record: stop, explain UoW is not applicable, offer `data-source-pattern-selector`.
- **Language and framework:** Which language and ORM (if any)? This determines whether UoW is already built-in (Hibernate, EF Core, SQLAlchemy) or must be hand-rolled.
- **Entity classes:** What are the domain objects (e.g., `Order`, `LineItem`, `Product`)?
- **FK dependency graph:** Which entities reference which? This determines INSERT and DELETE ordering.
- **Transaction boundary:** Where does one business operation begin and end (per-HTTP-request, per-command, per-service call)?

### Helpful
- Existing mapper or repository classes — their `find()` / `insert()` / `update()` / `delete()` methods will be called by the UoW on commit.
- Any existing dirty-tracking or session management code.
- Whether Optimistic Offline Lock (version columns) or Lazy Load (proxy collections) is in use — both require UoW integration.

### Defaults if not specified
- Unknown ORM → ask before generating stack-specific code; provide pseudocode in the interim.
- Unknown FK graph → assume single-level parent/child; flag ordering analysis as required.
- Unknown transaction boundary → default to per-request scope; warn about cross-request sharing.

---

## Process

**Step 1 — Confirm Data Mapper prerequisite.**

WHY: Unit of Work is designed to work with Data Mapper's separation of domain objects from SQL. Active Record embeds persistence in the entity itself; adding a UoW coordinator duplicates responsibility and creates confusion about who owns the save call. Confirming the prerequisite prevents a misapplication that will complicate the codebase.

- Data Mapper confirmed → continue.
- Active Record found → stop. Explain that AR handles persistence per-object; suggest `data-source-pattern-selector` if the team wants to reassess.
- Unknown → invoke `data-source-pattern-selector` or ask user directly.

**Step 2 — Choose the registration strategy.**

WHY: The UoW must know which objects have changed. There are three strategies, each with a different trade-off between transparency and coupling. Choosing the wrong one for the stack and team leads to missed registrations (caller registration) or domain-layer coupling (object registration).

Evaluate each option:

| Strategy | How it works | Best for | Risk |
|---|---|---|---|
| **Caller registration** | Application code calls `uow.registerDirty(entity)` explicitly | Simple custom layers, greenfield | Easy to forget; silent data loss |
| **Object registration** | Entity setters call `UoW.getCurrent().registerDirty(this)` | Custom frameworks; Java/C# domain objects | Couples domain to UoW; requires access to current UoW |
| **UoW-controlled (copy-on-load)** | UoW registers clean objects on load; detects changes at commit via snapshot comparison | ORM-provided (Hibernate, EF, SQLAlchemy) | Higher memory overhead; infrastructure-heavy |

Decision:
- Using Hibernate / EF Core / SQLAlchemy → use the built-in Session/DbContext (UoW-controlled). The skill maps your usage to the UoW contract (see Step 9).
- Custom framework → prefer object registration; use caller registration only for simple scripts.
- Testing-heavy codebase → consider a no-op UoW for unit tests (does not write to DB on commit).

**Step 3 — Design the UoW API.**

WHY: The interface is the contract between domain code and the persistence coordinator. Keeping it minimal and explicit prevents the UoW from becoming a god object.

Minimum API:
```
registerNew(entity)    — entity will be INSERTed on commit
registerDirty(entity)  — entity will be UPDATEd on commit
registerClean(entity)  — entity is known, no action on commit; populates Identity Map
registerRemoved(entity) — entity will be DELETEd on commit
commit()               — flush all changes in order, then DB COMMIT
rollback()             — discard change sets; no DB writes
clear()                — reset UoW state (call after commit or on request teardown)
```

Invariant assertions (enforce at registration time):
- `registerNew`: entity must have a non-null ID; must not be in dirty or removed list.
- `registerDirty`: must not be in removed list; no-op if already in new list.
- `registerRemoved`: if in new list → just remove from new (no DB write needed); remove from dirty.

**Step 4 — Implement four-state tracking.**

WHY: The four states map directly to the four SQL operations. Tracking state precisely prevents redundant SQL (e.g., updating an entity that was just inserted) and missed SQL (e.g., forgetting to delete an entity that was removed mid-operation).

Internal storage — three collections (clean objects are tracked only in Identity Map):
```
newObjects: List<DomainObject>      → INSERT on commit
dirtyObjects: List<DomainObject>    → UPDATE on commit
removedObjects: List<DomainObject>  → DELETE on commit
identityMap: Map<(Class, Id), DomainObject>  → first-level cache
```

State transition rules:
- Load from DB → `registerClean` → add to `identityMap`.
- Mutate a clean object → `registerDirty` → move to `dirtyObjects`.
- Create new → `registerNew` → add to `newObjects` AND `identityMap`.
- Delete → `registerRemoved` → move to `removedObjects`; remove from `dirtyObjects`.
- Delete a `new` object (not yet in DB) → remove from `newObjects`; no DB action needed.

For detailed per-transition code examples see `references/entity-state-transitions.md`.

**Step 5 — Implement the ordered commit procedure.**

WHY: Database referential integrity requires that parent rows exist before child rows are inserted, and child rows are deleted before parent rows. Committing in arbitrary order produces FK violation errors. The UoW is the natural place to enforce this ordering because it holds the full change set.

Commit sequence:
1. **INSERT** `newObjects` in FK dependency order (parents before children). Use a topological sort of the FK graph for complex schemas; use explicit ordering for small schemas.
2. **UPDATE** `dirtyObjects` (order within this set is usually safe; touch each exactly once).
3. **DELETE** `removedObjects` in reverse FK dependency order (children before parents).
4. **DB COMMIT** — issue `COMMIT` on the system transaction.
5. **Clear** UoW state — discard all lists and Identity Map entries, or discard the UoW entirely.

For the topological sort algorithm and ordering metadata approach see `references/commit-ordering.md`.

**Step 6 — Wire Identity Map integration.**

WHY: Without an Identity Map, loading the same entity twice produces two separate in-memory objects for the same database row. Updating both produces conflicting writes and undefined behavior. The Identity Map, co-located in the UoW, prevents this by ensuring every load returns the same instance.

Implementation:
- Key: `(entityClass, primaryKey)` tuple.
- On `find(class, id)`: check Identity Map first. If found → return cached instance. If not → load from DB, call `registerClean`, add to map, return.
- On `registerNew`: add to map immediately (the new ID must be assigned before registration).
- On `registerRemoved`: remove from map.
- The Identity Map also serves as a performance cache (avoids redundant DB reads), but its primary purpose is identity consistency, not performance.

**Step 7 — Establish lifecycle management.**

WHY: A UoW that spans multiple requests accumulates stale data, grows without bound, and causes race conditions when shared across threads. The lifecycle must be bounded.

Standard lifecycles:
- **Per-request** (most common for web apps): create UoW at request start, commit (or rollback on error) at request end, discard. Never share a UoW across threads.
- **Per-business-operation**: create UoW at the start of a command/service call, commit at end. Useful for non-HTTP contexts (CLI, batch).
- **Explicit begin/end**: for long business transactions that span multiple system transactions, pair with Optimistic Offline Lock patterns (UoW is recreated per system transaction; lock ensures consistency across them).

Anti-pattern: **never share a UoW across requests or threads.** A shared UoW accumulates dirty objects from multiple users, produces incorrect commits, and leaks memory.

**Step 8 — Integrate with collaborators.**

WHY: UoW is rarely used in isolation. Two patterns depend on UoW for correct behavior; wiring them explicitly prevents integration bugs.

**Optimistic Offline Lock integration:**
- Each entity tracked by UoW has a `version` field (integer or timestamp).
- On `updateDirty`, the UPDATE SQL becomes: `UPDATE ... SET ..., version = version+1 WHERE id=? AND version=?`
- If `rowsAffected == 0` → collision detected → raise `ConcurrencyException`, roll back transaction.
- The UoW is the correct place to run this check (it owns all UPDATE calls). See `optimistic-offline-lock-implementer` for the full version-management workflow.

**Lazy Load integration:**
- Lazy proxy collections are populated on first access via a callback into the current UoW/session.
- The Identity Map ensures that the populated entity is the same instance that UoW is already tracking — preventing a duplicate-entity trap where a loaded proxy yields a different object than the one already in the dirty list.

**Step 9 — Map to your stack's native UoW.**

WHY: Most modern stacks include a built-in Unit of Work. Using it directly is far preferable to hand-rolling; the skill's value is understanding the contract so you configure and scope the built-in correctly.

| Stack | UoW Object | Registration strategy | Commit call |
|---|---|---|---|
| Hibernate (Java) | `Session` | UoW-controlled (snapshot) | `session.flush()` + `tx.commit()` |
| Spring Data JPA | `EntityManager` via `@Transactional` | UoW-controlled | transaction commit |
| EF Core (.NET) | `DbContext` | UoW-controlled (change tracker) | `dbContext.SaveChanges()` |
| SQLAlchemy (Python) | `Session` | UoW-controlled + explicit `session.add()` | `session.commit()` |
| TypeORM (TS/JS) | `EntityManager` / `QueryRunner` | UoW-controlled | `queryRunner.commitTransaction()` |
| Django ORM | No first-class UoW | Per-save explicit | `transaction.atomic()` wrapper |

For Django: use `transaction.atomic()` to batch saves, but note there is no central dirty tracker — `bulk_update` / `bulk_create` provides partial batching.

For stack-specific scoping patterns (request-scoped DbContext in ASP.NET, scoped Session in FastAPI, EntityManager lifecycle in Jakarta EE) see `references/stack-native-uow-guide.md`.

---

## Inputs

- Confirmed data-source pattern: Data Mapper
- Entity class list and FK dependency graph
- Language and ORM framework (or "none — hand-rolling")
- Transaction boundary convention (per-request / per-command / explicit)
- Whether Optimistic Offline Lock and/or Lazy Load are in scope

---

## Outputs

**UoW Implementation Artifact** (written to the codebase or returned inline):

```
## Unit of Work Implementation Record

### Registration Strategy
[Caller | Object | UoW-controlled] — [rationale]

### API
registerNew(entity) / registerDirty(entity) / registerClean(entity) / registerRemoved(entity)
commit() / rollback() / clear()

### State Tracking
- newObjects: [List<Entity>]
- dirtyObjects: [List<Entity>]
- removedObjects: [List<Entity>]
- identityMap: Map<(Class, Id), Entity>

### Commit Sequence
1. INSERT newObjects in order: [entity order based on FK graph]
2. UPDATE dirtyObjects
3. DELETE removedObjects in reverse order: [reverse FK order]
4. DB COMMIT
5. Clear UoW state

### Lifecycle
[Per-request | Per-command] — [where UoW is created and where it is discarded]

### Stack-Native Equivalent
[If using Hibernate/EF/SQLAlchemy: the built-in Session/DbContext IS the UoW.
Map register/commit calls to the framework's API.]

### Integration Notes
- Optimistic Offline Lock: [version column present / not applicable]
- Lazy Load: [proxy collections wired through session / not applicable]

### Anti-Patterns to Watch
- [ ] Cross-request UoW sharing
- [ ] Missing registerDirty calls (caller registration risk)
- [ ] FK ordering violations on commit
- [ ] UoW not cleared between requests → memory leak + stale data
```

---

## Key Principles

**1. UoW is the database change controller — not individual domain objects.**
Without a UoW, each domain object decides when to write to the database. This produces excessive round trips, inconsistent ordering, and no natural rollback point. The UoW centralizes that control: domain code mutates objects freely; the UoW decides *when* and *in what order* those mutations reach the database.

**2. The four states (new, dirty, clean, removed) map exactly to the four SQL operations.**
Every entity in a business operation is in exactly one of these states. Understanding the state machine prevents double-writes, missed writes, and cascade ordering errors. The UoW enforces the state machine at registration time via assertions.

**3. INSERT/DELETE order is determined by FK dependencies, not by the order changes were made.**
If `LineItem` references `Order`, then `Order` must be inserted before `LineItem`, and `LineItem` must be deleted before `Order`. The UoW must encode or compute this graph. Ignoring it works until it doesn't — a single FK violation on commit surfaces the missing ordering logic.

**4. Identity Map is not optional — it is required for correctness.**
Loading the same row twice into two objects is a correctness bug, not a performance issue. The Identity Map prevents this by making the UoW the single source of truth for in-memory entity identity. Performance caching is a beneficial side-effect, not the purpose.

**5. UoW lifecycle must be bounded to one business operation.**
A UoW that outlives its business operation accumulates stale state and grows unboundedly. Cross-request sharing is especially dangerous in web apps because it causes different users' changes to be committed together. Enforce a clear begin/end boundary and discard the UoW after commit.

**6. On modern stacks, use the built-in Session/DbContext — understand its contract, don't fight it.**
Hibernate `Session`, EF Core `DbContext`, and SQLAlchemy `Session` implement the full UoW + Identity Map contract. The skill's purpose is to understand *what* they do (so you scope, flush, and clear them correctly) — not to replace them with a hand-rolled alternative.

---

## Examples

### Scenario A: Java e-commerce — custom Data Mapper, hand-rolled UoW

**Trigger:** "We have a Java e-commerce service with Order, LineItem, and Product. We're using hand-rolled Data Mappers (no ORM). After a business operation touches 12 objects, we're making 12 separate UPDATE calls. How do we introduce a Unit of Work?"

**Process:**
1. Confirm Data Mapper in place. FK graph: LineItem references Order and Product.
2. Registration strategy: object registration — setters on `Order` and `LineItem` call `UoW.getCurrent().registerDirty(this)`.
3. UoW API: `registerNew / registerDirty / registerClean / registerRemoved / commit()`.
4. Identity Map keyed by `(Class, Long id)`; populated on `OrderMapper.find(id)`.
5. Commit sequence: INSERT Order → INSERT LineItem (Product pre-exists) → UPDATE dirty Orders → UPDATE dirty LineItems → DELETE removed LineItems → DELETE removed Orders → COMMIT.
6. Lifecycle: per-HTTP-request via servlet filter — `UnitOfWork.newCurrent()` on request start; `UnitOfWork.getCurrent().commit()` + `setCurrent(null)` on request end (in `finally` block).

**Output:** Hand-rolled `UnitOfWork` class with three lists (new/dirty/removed), `ThreadLocal` storage for current UoW, `DomainObject` base class with `markDirty()` / `markNew()` / `markRemoved()`, and per-request lifecycle managed by a servlet filter. See `references/entity-state-transitions.md` for full Java sketch.

---

### Scenario B: Python + SQLAlchemy — scoping the built-in Session

**Trigger:** "We use SQLAlchemy with a FastAPI app. We're seeing stale data and occasional DetachedInstanceError. How should we scope the Session?"

**Process:**
1. Data Mapper confirmed: SQLAlchemy ORM's mapped classes + `Session` is the UoW.
2. Registration strategy: UoW-controlled — SQLAlchemy tracks changes automatically; `session.add(entity)` registers new objects.
3. Problem diagnosis: `Session` is likely being shared across requests (application-scoped singleton) rather than per-request.
4. Fix: use a dependency-injected `Session` per FastAPI request via `Depends(get_db)`, where `get_db` yields a session and closes it after the request.
5. Commit sequence: handled by `session.commit()` — SQLAlchemy resolves INSERT ordering via mapper relationships; `session.flush()` pushes SQL without committing for mid-operation ID resolution.
6. Lazy Load: SQLAlchemy lazy proxies use the session for population; closed or detached sessions trigger `DetachedInstanceError`. Fix: load eagerly for data needed after session close, or keep session open for the request lifetime.

**Output:** `get_db` generator dependency, per-request session scope, `session.add` for new entities, `session.delete` for removed, `session.commit()` at end of each request handler (or in a middleware). Anti-pattern warning: never use a module-level `Session` instance.

---

### Scenario C: .NET + EF Core — DbContext per-request scoping

**Trigger:** "We have an ASP.NET Core app with EF Core. We're trying to understand when to call SaveChanges and how to avoid detached entity errors."

**Process:**
1. Data Mapper confirmed: EF Core `DbContext` is the UoW; entities tracked by the change tracker.
2. Registration strategy: UoW-controlled — EF Core detects changes on tracked entities automatically.
3. DbContext is registered as `Scoped` in ASP.NET Core DI → one instance per HTTP request. This is correct.
4. Commit: `await dbContext.SaveChanges()` at the end of the service method (or in a controller action). Avoid calling it multiple times per request unless intentional.
5. Optimistic Offline Lock: add a `[Timestamp]` or `[ConcurrencyToken]` property; EF Core adds `WHERE version=?` automatically and throws `DbUpdateConcurrencyException` on collision.
6. Anti-pattern: passing a `DbContext` from a scoped service into a singleton service → context outlives the request, accumulates stale data.

**Output:** Confirm `Scoped` lifetime, single `SaveChanges()` call per business operation, `[ConcurrencyToken]` on entities needing optimistic locking, and warning against singleton-scoped `DbContext`.

---

## References

- `references/entity-state-transitions.md` — Full state machine with Java pseudocode for four entity states and registration assertions
- `references/commit-ordering.md` — Topological sort algorithm for FK-ordered INSERT/DELETE + ordering for Order/LineItem/Product example
- `references/stack-native-uow-guide.md` — Per-stack session scoping patterns (FastAPI, ASP.NET Core, Spring Boot, Jakarta EE, TypeORM)
- `references/identity-map-implementation.md` — Key design choices (explicit vs generic map, one map per class vs per session, inheritance handling)

**Related patterns triggered by this skill's output:**
- If Optimistic Offline Lock needed → `optimistic-offline-lock-implementer`
- If Lazy Load proxies in scope → `lazy-load-strategy-implementer`
- If data-source pattern not yet chosen → `data-source-pattern-selector`

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler et al.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-lazy-load-strategy-implementer`
- `clawhub install bookforge-optimistic-offline-lock-implementer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
