---
name: optimistic-offline-lock-implementer
description: "Use when offline-concurrency-strategy-selector (or your team) has chosen Optimistic Offline Lock and you need to implement it correctly end-to-end. Handles: adding a version column (integer, not timestamp), version-conditioned UPDATE and DELETE SQL (WHERE id=? AND version=?), row-count-zero collision detection, ConcurrencyException with modifiedBy+modified context, stale-version prevention, version round-tripping from server to client and back, Unit of Work commit integration (checkConsistentReads → insertNew → deleteRemoved → updateDirty with rollback on exception), ORM-native version support (@Version annotation JPA/Hibernate, [ConcurrencyCheck] or [Timestamp] EF Core, version_id_col SQLAlchemy, lock_version Rails, django-concurrency), and collision UX design (merge / force-save / abandon — not just a 409 error). Also handles: optimistic locking, optimistic offline lock, concurrent edit collision detection, lost update prevention, conditional update, concurrency version check, OptimisticLockException, DbUpdateConcurrencyException, StaleObjectError, inconsistent read protection, checkCurrent early-failure, anti-pattern audit (missing WHERE clause, non-incremented version, stale in-memory object retry, timestamp versioning). Produces an implementation plan covering schema, ORM config, version round-trip path, collision UX spec, test plan, and anti-pattern checklist."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/optimistic-offline-lock-implementer
metadata: {"openclaw":{"emoji":"🔢","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
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
  - optimistic-locking
  - concurrency
  - transactions
  - design-patterns
  - data-integrity
  - offline-lock
  - lost-update-prevention
  - version-column
depends-on:
  - offline-concurrency-strategy-selector
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Persistence layer source code (mapper, repository, or ORM entity classes), database schema files, and any existing concurrency mechanism"
    - type: user-description
      description: "Stack and ORM in use, entities that need concurrent-edit protection, whether schema changes are possible, and whether client (web/mobile) must round-trip the version"
  tools-required:
    - Read
    - Grep
    - Edit
    - Write
  tools-optional:
    - Glob
  mcps-required: []
  environment: "Application with at least one multi-request editing workflow (record loaded in one HTTP request, saved in a later one). Relational database with ORM or hand-rolled persistence. Stack-agnostic: Java/Spring, C#/.NET, Python, Ruby on Rails, Node.js all apply."
discovery:
  goal: "Implement Optimistic Offline Lock with correct version-conditioned writes, collision detection, UX, and Unit of Work integration."
  tasks:
    - "Confirm offline-concurrency-strategy-selector chose Optimistic (or confirm directly from context)"
    - "Identify all entities and tables requiring concurrent-edit protection"
    - "Design or audit the version column (integer preferred; check ORM annotation requirements)"
    - "Plumb version capture on read: domain object carries version; API/DTO includes version; client round-trips it"
    - "Implement version-conditioned UPDATE and DELETE (WHERE id=? AND version=?); increment version on success"
    - "Implement collision detection: check row count; on 0, re-query for modifiedBy+modified; throw ConcurrencyException with context"
    - "Design collision UX: error message, merge view, force-save, or abandon options"
    - "Integrate with Unit of Work commit sequence; ensure rollback on ConcurrencyException"
    - "Audit for common anti-patterns: missing WHERE, non-incremented version, stale retry, timestamp versioning"
    - "Write two-writer concurrency test"
    - "Produce Optimistic Offline Lock implementation plan"
  audience:
    roles:
      - backend-engineer
      - software-architect
      - tech-lead
    experience: intermediate
  when_to_use:
    triggers:
      - "offline-concurrency-strategy-selector output specifies Optimistic Offline Lock"
      - "Implementing version-based concurrency control for the first time"
      - "Auditing an existing optimistic lock implementation for correctness"
      - "Getting 'lost update' bugs where one user's save overwrites another's silently"
      - "Need to add @Version annotation, lock_version, or version_id_col to entities"
      - "Designing the collision UX: what happens when two users edit the same record"
      - "Integrating optimistic version checks into a Unit of Work commit"
      - "Adding ORM-native optimistic locking to Hibernate, EF Core, SQLAlchemy, or Rails"
    prerequisites:
      - "offline-concurrency-strategy-selector has been run (or Optimistic is confirmed appropriate)"
    not_for:
      - "Systems where all business transactions fit in a single DB transaction — use isolation levels instead"
      - "High-collision, high-rework-cost workflows — use pessimistic-offline-lock-implementer"
      - "Thread-level concurrency within a single request (use language-level synchronization)"
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

# Optimistic Offline Lock Implementer

## When to Use

This skill implements the Optimistic Offline Lock pattern after `offline-concurrency-strategy-selector` (or your team) has confirmed it is the right concurrency strategy. The pattern applies when a business transaction spans multiple HTTP requests — user loads a record, edits for seconds or minutes, then saves — and the collision frequency is low enough that detecting conflicts at commit time is acceptable.

**Do not use** if conflicts are frequent or rework cost is unacceptably high (use pessimistic locking instead). **Do not use** if the entire workflow fits in a single request/transaction (use database isolation levels).

## Context & Input Gathering

Collect this before proceeding. Grep the codebase or ask the user directly.

**Required:**
1. **Stack and ORM** — Java/Hibernate, C#/EF Core, Python/SQLAlchemy, Ruby on Rails, Node.js/Knex, or hand-rolled SQL?
2. **Entities needing protection** — which tables/domain classes have concurrent-edit risk?
3. **Schema mutability** — can version columns be added, or is the schema frozen (legacy)?
4. **Client round-trip** — does a web/mobile client need to hold the version between GET and PUT/POST?
5. **Unit of Work present?** — is there an explicit UoW or does each repository method own its transaction?
6. **Inconsistent read risk?** — are there reads whose correctness the commit depends on (not just writes)?

**Observable from codebase:**
- Existing `version` or `lock_version` columns → implementation may be partially in place; audit for correctness
- `@Version`, `[ConcurrencyCheck]`, `version_id_col` annotations → ORM-native path
- UPDATE statements without WHERE version clause → lost-update vulnerability
- API response DTOs → check whether `version` field is included

**Sufficiency:** If ORM and entity list are known, proceed. If schema is frozen, plan the all-fields-WHERE fallback (see References).

---

## Process

### Step 1 — Confirm strategy selection

Verify that `offline-concurrency-strategy-selector` chose Optimistic Offline Lock for this workflow.

- IF the selector skill was not run → invoke `offline-concurrency-strategy-selector` first, OR ask: "Is collision frequency low AND is rework cost acceptable if a save is rejected?" If yes, Optimistic applies.
- IF Pessimistic was chosen → use `pessimistic-offline-lock-implementer` instead.

**WHY:** This skill implements Optimistic-specific mechanics. Applying it to a high-collision, high-rework-cost workflow produces a poor user experience — users lose significant work on every collision.

---

### Step 2 — Identify entities and design the version column

List every entity (table) that participates in concurrent-edit business transactions.

For each entity:

**Integer version column (primary approach):**
```sql
ALTER TABLE {table} ADD COLUMN version INTEGER NOT NULL DEFAULT 0;
ALTER TABLE {table} ADD COLUMN modified_by VARCHAR(255);
ALTER TABLE {table} ADD COLUMN modified_at TIMESTAMP;
```

**ORM-native equivalents (preferred when ORM is in use):**

| ORM | Annotation / Config | Exception thrown |
|-----|---------------------|-----------------|
| Hibernate / JPA | `@Version` on `int version` field | `OptimisticLockException` |
| EF Core (.NET) | `[ConcurrencyCheck]` on field, or `[Timestamp]` (rowversion) | `DbUpdateConcurrencyException` |
| SQLAlchemy | `__mapper_args__ = {"version_id_col": version_col}` | `StaleDataError` |
| Rails ActiveRecord | `lock_version INTEGER DEFAULT 0` column (auto-detected) | `ActiveRecord::StaleObjectError` |
| Django (no built-in) | Manual: filter on version + check `updated_count`, or `django-concurrency` package | Custom exception |

**WHY:** Using an integer version is deterministic and monotonically increasing. Timestamps are "simply too unreliable, especially if you're coordinating across multiple servers" (Fowler) — clock skew causes missed conflicts and false collisions. The `modified_by` and `modified_at` columns are not used in the WHERE clause; they provide context for the error message shown to the user.

If the schema cannot be changed → fall back to the all-fields WHERE clause approach (see References).

---

### Step 3 — Plumb version capture on read

Every place the entity is loaded must capture and carry the version.

**Domain object / entity:** The version field must be part of the object, not a separate variable. This ensures the Identity Map returns the same version consistently within a business transaction.

```java
// Java domain object base class
class DomainObject {
    private int version;
    private String modifiedBy;
    private Timestamp modifiedAt;
    // setSystemFields() called by mapper after load — NOT constructor
}
```

**API/DTO round-trip (for web/mobile clients):** If a client loads the record in one HTTP request and saves in another, the version must travel to the client and back.

```json
// GET /customers/42
{ "id": 42, "name": "Smith", "version": 7, ... }

// PUT /customers/42
{ "id": 42, "name": "Smythe", "version": 7, ... }
```

The server extracts `version` from the request body and uses it in the WHERE clause.

**WHY:** If the version is not round-tripped, the server has no way to know what version the client read. It would either have to reject all saves (too strict) or skip the check (defeats the pattern). The client must be a faithful carrier of the version it received.

**Identity Map check:** In the persistence layer, `find(id)` must check the Identity Map before querying the DB. Loading the same record twice at different version values within one business transaction produces undefined behavior in version checks.

---

### Step 4 — Implement version-conditioned writes

**UPDATE (modify):**
```sql
UPDATE customer
SET name = ?, modified_by = ?, modified_at = ?, version = ?
WHERE id = ? AND version = ?
-- Parameters: (newName, currentUser, now, oldVersion+1, id, oldVersion)
```

**DELETE:**
```sql
DELETE FROM customer WHERE id = ? AND version = ?
-- Parameters: (id, oldVersion)
```

**Check row count immediately:**
```java
int rowCount = stmt.executeUpdate();
if (rowCount == 0) {
    throwConcurrencyException(object);  // see Step 5
}
```

**For ORM stacks:** Enable the built-in version field (Step 2 annotation). The ORM generates version-conditioned SQL automatically and throws its native exception. Catch that exception at the service/controller boundary (Step 5).

**WHY:** The WHERE clause atomically validates the version AND applies the data change in a single SQL statement. This is the only reliable way to ensure "nobody changed this between my read and my write" without holding a database lock across user think-time. A separate SELECT + UPDATE pair has a TOCTOU race condition.

The version increment (`version = oldVersion + 1`) is essential: it marks the row as changed so any concurrent session holding the old version will see row count 0 on their save.

---

### Step 5 — Implement collision detection and error context

When row count = 0, determine WHY before throwing:

```java
protected void throwConcurrencyException(DomainObject obj) {
    // Re-query to differentiate "modified" from "deleted"
    ResultSet rs = execute("SELECT version, modified_by, modified_at FROM customer WHERE id=?", obj.getId());
    if (rs.next()) {
        int dbVersion = rs.getInt("version");
        String who = rs.getString("modified_by");
        Timestamp when = rs.getTimestamp("modified_at");
        throw new ConcurrencyException(
            "Customer " + obj.getId() + " was modified by " + who +
            " at " + format(when) + ". Please reload and re-apply your changes."
        );
    } else {
        throw new ConcurrencyException(
            "Customer " + obj.getId() + " was deleted by another session."
        );
    }
}
```

**WHY:** A bare "concurrency error" leaves the user confused and helpless. Informing them WHO changed the record and WHEN lets them make an informed decision: was it a conflicting edit or just a background sync? The re-query is safe here because it runs inside the same system transaction that is about to be rolled back — it reads the committed DB state.

---

### Step 6 — Design collision handling UX

Catching the exception at the controller/service boundary is not enough — the user must understand what happened and have a meaningful path forward.

**Minimum acceptable UX (abort + inform):**
> "This record was modified by Alice at 2:34 PM. Your changes could not be saved. Please reload the record and re-apply your changes."
> [Reload] [Cancel]

**Better UX (show conflict):**
Show the user's proposed changes alongside the current DB state side by side. Let them choose which values to keep field by field.

**Advanced UX (merge or force-save):**
- **Merge:** auto-merge non-overlapping field changes (works when two users edited different fields — similar to how source control merges non-conflicting lines).
- **Force-save:** user explicitly accepts that their version will overwrite the current DB state. Requires a deliberate action (not the default). Load the latest version, then re-apply the user's changes on top.

**API semantics:** Return HTTP 409 Conflict with a body that includes `currentVersion`, `modifiedBy`, `modifiedAt`, and the conflicting field values.

**WHY:** "A proper application will tell when the record was altered and by whom" (Fowler). Silent failure or a bare error code is the most common implementation mistake — users lose work and don't know why. The quality of the collision UX often determines whether Optimistic Locking is tolerable in practice.

---

### Step 7 — Integrate with Unit of Work commit

If the system uses a Unit of Work pattern, the commit sequence must:

```
checkConsistentReads()   ← version-check read-set objects (if inconsistent read protection needed)
insertNew()
deleteRemoved()
updateDirty()            ← version-conditioned UPDATEs live here
```

On ANY `ConcurrencyException` during commit: **rollback the system transaction before re-throwing.**

```java
public void commit() {
    try {
        checkConsistentReads();
        insertNew();
        deleteRemoved();
        updateDirty();
    } catch (ConcurrencyException e) {
        rollbackSystemTransaction();  // CRITICAL — do not forget
        throw e;
    }
}
```

**Inconsistent read protection** (optional but recommended): if the commit's correctness depends on a value that was READ but not WRITTEN (e.g., customer address used for tax calculation), register that object in a read-set and version-check it at commit:

```java
public void registerRead(DomainObject obj) { reads.add(obj); }

public void checkConsistentReads() {
    for (DomainObject obj : reads) {
        obj.getVersion().increment();  // forces version check even for read-only objects
    }
}
```

**WHY:** Without rollback, partial writes enter the database — some records updated, others not — leaving data in an inconsistent state. The UoW is the natural integration point because it already owns the system transaction boundary and the commit sequence.

If the Unit of Work skill (`unit-of-work-implementer`) is available, reference its commit sequence and add version-conditioned writes in the `updateDirty()` and `deleteRemoved()` stages. If that skill has not been run, implement the commit loop directly in the repository or service class.

---

### Step 8 — Audit for common anti-patterns

Run this checklist against the codebase before marking implementation complete:

- [ ] **Every UPDATE and DELETE on versioned tables includes `AND version=?`** — grep for `UPDATE {table}` and verify WHERE clause
- [ ] **Version is incremented on every successful save** — verify `version = version+1` (or ORM equivalent), not `version = version`
- [ ] **Row count is checked after every UPDATE/DELETE** — no unchecked `executeUpdate()` calls
- [ ] **Collision error message includes who and when** — not just "concurrency error"
- [ ] **Version is included in API responses and request bodies** (for web clients) — check DTO classes and OpenAPI spec
- [ ] **No timestamp used as version substitute** — search for `modified_at` or `updated_at` in WHERE clauses
- [ ] **Retry logic (if any) reloads the object first** — stale in-memory object with old version must not be reused directly
- [ ] **No raw SQL UPDATE paths that bypass ORM version mechanism** — grep for raw SQL on ORM-managed tables
- [ ] **System transaction is rolled back on ConcurrencyException** — not just re-thrown

**WHY:** Each of these is a known failure mode. Missing the WHERE clause is the most dangerous — it silently permits Lost Updates, the exact problem this pattern exists to prevent. Non-incremented version means subsequent writers see no new version and can overwrite without conflict. Stale retry immediately throws another collision without making progress.

---

### Step 9 — Write the two-writer concurrency test

A test that exercises the actual collision scenario:

```python
# Pseudocode — adapt to your framework's test infrastructure
def test_optimistic_lock_collision():
    record = create_record(name="original", version=0)

    # Session A loads at version 0
    session_a_record = load(record.id)  # version=0

    # Session B loads at version 0, edits, saves first
    session_b_record = load(record.id)  # version=0
    session_b_record.name = "session_b_edit"
    save(session_b_record)  # succeeds, version becomes 1

    # Session A tries to save — version 0 no longer matches DB version 1
    session_a_record.name = "session_a_edit"
    with raises(ConcurrencyException):
        save(session_a_record)  # must raise — row count = 0

    # Verify DB holds session B's value, not session A's
    current = load(record.id)
    assert current.name == "session_b_edit"
    assert current.version == 1
```

**WHY:** Unit tests on individual UPDATE SQL are insufficient. The collision scenario requires two independent sessions reading the same version and one writing first. Without this test, it is easy to ship an implementation that increments correctly in isolation but fails to detect collisions in practice (e.g., version not in WHERE clause but version correctly incremented).

---

### Step 10 — Produce the implementation plan artifact

Output the Optimistic Offline Lock Implementation Plan (see Outputs section).

**WHY:** A written plan consolidates all decisions made in Steps 1–9 into a reviewable artifact. It serves as the spec for implementation (or review checklist for existing code), makes the anti-pattern audit explicit, and gives the team a shared reference for schema changes, ORM config, and UX behavior.

## Inputs

- Entity/table list requiring concurrent-edit protection
- Stack, ORM, and language (determines implementation path)
- Schema mutability (can version columns be added?)
- API contract (does client need to round-trip version?)
- Existing persistence code (mapper, repository, or ORM entities)
- Unit of Work implementation (if present)

## Outputs

### Optimistic Offline Lock Implementation Plan

```markdown
## Optimistic Offline Lock Implementation Plan: [Feature/Entity Name]

**Date:** YYYY-MM-DD | **Stack:** [ORM / language] | **Entities:** [list]

### 1. Schema Changes
- [ ] ALTER TABLE {table} ADD COLUMN version INTEGER NOT NULL DEFAULT 0;
- [ ] ALTER TABLE {table} ADD COLUMN modified_by VARCHAR(255);
- [ ] ALTER TABLE {table} ADD COLUMN modified_at TIMESTAMP;

### 2. ORM Config
[@Version / [ConcurrencyCheck] / version_id_col / lock_version]

### 3. Version Round-Trip Path
- GET /resource/{id} → includes "version" in response
- PUT /resource/{id} → client sends "version" back in body
- Server extracts version from: [request.body.version / session state]

### 4. Write Implementation
- UPDATE: WHERE id=? AND version=? with version=oldVersion+1
- DELETE: WHERE id=? AND version=?
- Row-count check: rowCount == 0 → throwConcurrencyException()

### 5. Collision Handling
- Exception: [ConcurrencyException / OptimisticLockException / custom]
- Re-query: SELECT version, modified_by, modified_at WHERE id=?
- UX: [error+reload / diff view / force-save] | API: 409 Conflict

### 6. Unit of Work Integration
- Commit: checkConsistentReads → insertNew → deleteRemoved → updateDirty
- Rollback on ConcurrencyException: [yes / repository-per-request N/A]

### 7. Anti-Pattern Checklist
[Completed from Step 8]

### 8. Test Plan
- [ ] Two-writer test: session B saves first → session A gets ConcurrencyException
- [ ] Delete collision: record deleted → "deleted" message
- [ ] Retry: reload + re-save succeeds after collision
```

## Key Principles

**1. The version WHERE clause is the lock — it must be in every UPDATE and DELETE.**
A version column stored and incremented but absent from the WHERE clause provides zero protection. The atomic "validate + write" in a single SQL statement is what makes the pattern work without holding a DB connection across user think-time. Any write path missing the version WHERE clause silently permits Lost Updates.

**2. Integer version, not timestamp — always.**
System clocks are unreliable across servers. Sub-millisecond updates can share a timestamp. An integer version is monotonically increasing and immune to clock skew. Fowler: "system clocks are simply too unreliable, especially if you're coordinating across multiple servers."

**3. Round-trip the version — client must carry it faithfully.**
The version must travel from the GET response to the PUT/POST request body. A server that re-reads the version from DB at save time defeats the pattern — it always gets the latest version and never detects conflicts.

**4. The collision message must name who and when.**
"Your save failed" is not acceptable. Users need to know WHO changed the record and WHEN. Store `modified_by` and `modified_at` and re-query on collision. Implementing only the technical check without actionable UX is a half-implementation.

**5. Roll back the system transaction on collision — without exception.**
If any write fails the version check, roll back the system transaction before re-throwing. Partial commits leave data inconsistent (some records written, others not). Fowler: "Do not forget this step!"

**6. Stale retry fails again — always reload before retry.**
Catching ConcurrencyException and re-saving the same domain object immediately fails again (it still holds the old version). Reload the object from DB first, re-apply changes, then save.

**7. Move version mechanics into the abstract mapper — Implicit Lock prevents gaps.**
One developer omitting a version check on one entity silently breaks the scheme for that entity. The abstract `AbstractMapper` supertype (or ORM base config) makes version-conditioned writes mandatory — concrete mappers cannot accidentally skip them.

## Examples

### Example 1: Java/Spring Data JPA — CRM Customer Entity

**Scenario:** CRM where 15 sales reps edit customer records, 2–5 min sessions, low collision rate. Optimistic chosen.

**Trigger:** "Lost updates on customer records when two reps edit the same customer."

**Process:**
- Step 2: Add `@Version private int version;` to `Customer` entity. Hibernate auto-generates version-conditioned SQL.
- Step 3: Include `"version": 7` in `CustomerDTO`. Controller extracts it from PUT body.
- Step 4: `customerRepository.save(customer)` → Hibernate issues `UPDATE customer SET ... WHERE id=? AND version=?`.
- Step 5: Catch `OptimisticLockException` in `@ExceptionHandler`. Re-query for `modifiedBy`/`modifiedAt`. Return HTTP 409.
- Step 6: UI shows: "This customer was updated by Bob at 3:12 PM. Please reload and re-apply your changes."
- Step 7: `@Transactional` handles rollback automatically.

**Output:** `@Version` on Customer entity, DTO round-trips version, 409 handler with who/when, two-writer test.

---

### Example 2: Ruby on Rails — Inventory Management

**Scenario:** Warehouse staff edit product records via Rails admin. 1–3 min sessions.

**Trigger:** "Two staff sometimes update the same product simultaneously — add optimistic locking."

**Process:**
- Step 2: `rails generate migration AddLockVersionToProducts lock_version:integer`. Rails auto-detects `lock_version`.
- Step 3: Hidden field in form: `<%= f.hidden_field :lock_version %>`. Permit in strong params.
- Step 4: `product.update!(params)` → Rails: `UPDATE products SET ... WHERE id=? AND lock_version=?`.
- Step 5: `rescue ActiveRecord::StaleObjectError` in controller. Re-query for `updated_by`/`updated_at`.
- Step 6: Flash: "Someone else updated this product. Here's what changed — please review and re-submit."

**Output:** Migration, hidden field, `rescue StaleObjectError`, diff-style conflict display.

---

### Example 3: Node.js + Knex — Custom Repository

**Scenario:** Node.js SaaS, hand-rolled Knex repositories, no ORM. Entities: `contracts`, `line_items`.

**Trigger:** "Add version-based optimistic locking to our contract editing API — no concurrency protection today."

**Process:**
- Step 2: `ALTER TABLE contracts ADD COLUMN version INTEGER NOT NULL DEFAULT 0`, `modified_by`, `modified_at`.
- Step 3: GET response includes `version`. PUT body sends it back. Repository receives `claimedVersion`.
- Step 4: `knex('contracts').where({ id, version: claimedVersion }).update({ ...fields, version: claimedVersion+1 })` → check `count === 0`.
- Step 5: `ConcurrentModificationError` re-queries `modified_by`/`modified_at` and attaches to error.
- Step 6: Express error handler returns 409 `{ error: "Conflict", modifiedBy, modifiedAt }`.
- Step 7: Multi-table commits use `knex.transaction()` with rollback on `ConcurrentModificationError`.

**Output:** Migration, version-conditioned repository, `ConcurrentModificationError`, 409 handler, two-writer test.

## References

- [Version Column SQL and ORM Config Reference](references/version-column-reference.md) — SQL DDL for version columns, ORM-specific annotations and config, all-fields WHERE fallback for frozen schemas
- [Collision UX Patterns](references/collision-ux-patterns.md) — abort+inform, diff view, merge, force-save — with UI copy templates and API 409 response schema
- [Anti-Pattern Detection Checklist](references/anti-pattern-checklist.md) — grep patterns and code audit queries for each of the 9 anti-patterns, with example buggy code and correct fix
- [Unit of Work Integration Guide](references/unit-of-work-integration.md) — commit sequence, read-set registration, rollback wiring, and Java example from the book

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-offline-concurrency-strategy-selector`
- `clawhub install bookforge-unit-of-work-implementer`
- `clawhub install bookforge-transaction-isolation-level-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
