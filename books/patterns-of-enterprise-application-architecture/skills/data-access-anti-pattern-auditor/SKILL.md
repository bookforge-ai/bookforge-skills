---
name: data-access-anti-pattern-auditor
description: "Audit a persistence layer and schema for data access anti-patterns: N+1 query
  (SELECT N+1), ripple loading, lazy loading anti-pattern, ghost/proxy identity trap (missing
  Identity Map), Active Record anti-pattern on non-isomorphic schema, Active Record / Data Mapper
  mismatch, Serialized LOB overuse (queryable data stored in BLOB/JSONB/TEXT), meaningful primary
  key leakage, business logic in Gateway classes. Given a codebase and schema, produces a
  prioritized anti-pattern inventory with code location, evidence snippet, consequence, and
  remediation that cross-references pattern-selector skills. Use this for ORM performance audit,
  ORM anti-pattern detection, persistence anti-pattern inventory, database access anti-pattern
  review, persistence layer review, data access review, audit persistence layer."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/data-access-anti-pattern-auditor
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [3, 11, 12]
domain: software-architecture
tags:
  - anti-patterns
  - persistence
  - orm
  - auditing
  - data-access
  - code-review
  - performance
  - database
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Persistence layer source files (models, repositories, gateways, mappers) plus schema (SQL DDL or ORM model definitions). The fuller the snapshot, the more precise the findings."
    - type: description
      description: "ORM / framework in use (Rails/ActiveRecord, Hibernate/JPA, SQLAlchemy, EF Core, TypeORM, etc.) and language. Inferred from build files if not stated."
  tools-required:
    - Grep
    - Read
    - Glob
  tools-optional:
    - Bash
  mcps-required: []
  environment: "Enterprise application codebase with persistence layer accessible. Minimum: schema DDL + one sample model/repository file. Optimal: full src/persistence/, src/domain/, schema.sql, and ORM config."
discovery:
  goal: "Produce a prioritized anti-pattern inventory for a persistence layer, with code location, evidence, consequence, and remediation for each finding."
  tasks:
    - "Identify N+1 / ripple loading: loop + per-iteration DB access"
    - "Identify ghost/proxy identity trap: missing or bypassed Identity Map"
    - "Identify Active Record / Data Mapper mismatch: schema-isomorphism failure"
    - "Identify Serialized LOB overuse: queryable data buried in BLOB/JSONB/TEXT"
    - "Identify meaningful primary key leakage: business values as PKs"
    - "Identify business logic in Gateway classes: non-CRUD methods in TDG/RDG"
    - "Prioritize findings by severity (data-integrity > performance > maintainability)"
    - "Produce remediation recommendations cross-referencing selector skills"
  audience:
    roles:
      - senior-backend-engineer
      - software-architect
      - tech-lead
      - code-reviewer
    experience: intermediate
  when_to_use:
    triggers:
      - "Suspecting N+1 query performance problems in an ORM-backed app"
      - "Pre-refactoring audit of persistence layer before introducing a new ORM or framework"
      - "Code review of a persistence layer or data access object set"
      - "Diagnosing slow pages or endpoints where the bottleneck is database round-trips"
      - "Migrating from ActiveRecord to Data Mapper (or vice versa) and need to assess fit"
      - "Greenfield design review: confirming the chosen data-source pattern matches domain complexity"
      - "Legacy system audit: identifying structural persistence debt before modernization"
    prerequisites: []
    not_for:
      - "Concurrency/locking anti-patterns (use transaction-isolation-level-auditor)"
      - "Web presentation anti-patterns (fat controller, template scriptlets)"
      - "Distribution anti-patterns (chatty remote calls)"
      - "Choosing the correct data-source pattern from scratch (use data-source-pattern-selector)"
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

# Data Access Anti-Pattern Auditor

An end-to-end persistence-layer audit that detects six classes of data access anti-pattern,
grades each finding by severity, and produces remediation recommendations grounded in
Fowler's Patterns of Enterprise Application Architecture.

## When to Use

Run this audit when:
- Pages or endpoints are inexplicably slow and the bottleneck is query count, not query duration.
- A code review reveals ORM model files that feel "too smart" or "too tangled with schema concerns."
- A migration is planned (new ORM, schema refactor, framework upgrade) and you need a
  baseline of structural debt.
- A new subsystem is being designed and you want to confirm the data-source pattern choice
  before coding begins.
- You have inherited a legacy codebase and need to map persistence risks before touching it.

Not for: concurrency/locking problems, web controller bloat, remote-call overhead, or
choosing a pattern from scratch (those have dedicated skills).

## Context and Input Gathering

**Required:**
- Persistence layer source files: model classes, repository/gateway/mapper files, ORM config.
- Schema: SQL DDL, migration files, or ORM model definitions that define table structure.

**Observable / inferred:**
- ORM and language: detected from `import`/`require` statements, `pom.xml`, `Gemfile`,
  `requirements.txt`, `package.json`. Ask if not determinable.
- Application domain: inferred from table/class names. A brief description helps scope findings.

**Defaults if not provided:**
- Assume modern ORM with lazy loading enabled by default (the common case in Hibernate,
  Rails, SQLAlchemy, EF Core).
- Assume new system unless file timestamps or comments indicate otherwise.

**Sufficiency check:** You need at least one model/entity file and the schema to produce
findings. Without both, produce a "what to look for" checklist and ask for the missing piece.

## Process

### Step 1 — Discover the persistence layer

WHY: Anti-patterns live in specific file types. Locating them before analysis avoids
missing findings buried in unusual directory structures.

1a. Glob for ORM model/entity/gateway files:
```
src/persistence/**   src/models/**   src/domain/**
**/models.py         **/*.entity.ts  **/*Gateway.*  **/*Mapper.*  **/*Repository.*
schema.sql           db/schema.rb     migrations/
```
1b. Read the build file (pom.xml, Gemfile, requirements.txt, package.json) to confirm ORM.
1c. Read `config/database.yml` or equivalent for connection pool and isolation level context.

### Step 2 — Scan for N+1 / ripple loading

WHY: Fowler warns that "ripple loading" — filling a collection with individually lazy-loaded
objects then examining them one at a time — is the most common ORM performance killer. Each
object triggers a separate SQL round-trip, making N parent entities produce 1+N queries.

2a. Grep for loop constructs: `forEach`, `each`, `for...in`, `for...of`, `.map(`, `.stream(`.
2b. Inside each loop body, check whether a navigation property or finder is accessed:
  `.line_items`, `.getRelated()`, `.find(`, `.query(`.
2c. Confirm no eager-load option at the query site: Rails `.includes`, JPA `JOIN FETCH`,
  SQLAlchemy `joinedload`, EF Core `.Include`, Prisma `include`.
2d. Check ORM model definitions for `lazy=True`, `FetchType.LAZY`, `virtual ICollection` —
  these are the seed of N+1 when accessed in a loop.

Record: file path, line range, loop shape, the lazy field accessed, evidence snippet.

### Step 3 — Scan for ghost / proxy identity trap

WHY: Virtual proxies for lazy loading carry a different object identity than the real object.
Two proxies for the same DB row compare as unequal. Fowler calls this "a nasty identity
problem." Without an Identity Map, the same row can produce multiple conflicting instances
in one transaction — causing double-writes and broken version checks.

3a. Check if the ORM is configured to use a session / Unit of Work / first-level cache.
3b. Grep for multiple session/context creation within one request:
  `new Session(`, `new DbContext(`, `sessionFactory.openSession()`.
3c. Check entity `equals()` / `__eq__` — if not overridden, comparison is reference equality,
  which will fail for proxies of the same row.
3d. Look for detached entity access after session close (JPA `LazyInitializationException`
  stack traces in logs; SQLAlchemy `DetachedInstanceError`).

Record: whether single-session discipline is enforced, any violations found.

### Step 4 — Scan for Active Record / Data Mapper mismatch

WHY: Fowler states Active Record "works well only if the objects correspond directly to the
database tables: an isomorphic schema." When the domain has inheritance hierarchies, value
objects, or systematic naming divergence, AR fights the ORM constantly — every method
involves manual conversion. Conversely, a full Data Mapper for a simple CRUD app adds
ceremony without benefit.

4a. Identify the data-source pattern in use: ActiveRecord base class, explicit mapper classes,
  or repository classes that load domain objects.
4b. If AR: check for isomorphism failure signals —
  - `to_domain` / `from_record` / `to_entity` methods inside the AR class.
  - Inheritance hierarchy in domain mapped to a flat AR class (STI or manual type column).
  - Value objects (Money, Address) stored as AR fields with multi-column mapping.
  - Systematic column/field name mismatch beyond convention (e.g., `bill_addr_l1` ↔ `billing_address_line1`).
4c. If Data Mapper: check for over-engineering signals —
  - Mapper classes that are pure field-for-field copies with no structural transformation.
  - Domain objects with no behavior (all data, no methods) — anemic domain model.

Record: pattern identified, isomorphism verdict, specific mismatch evidence.

### Step 5 — Scan for Serialized LOB overuse

WHY: Fowler warns that the primary disadvantage of Serialized LOB is "you can't query the
structure using SQL." When teams query inside a LOB using LIKE, JSON operators, or secondary
indexes, they have chosen the wrong pattern — the data needed real columns from the start.
The versioning risk is equally serious: changing the serialized class definition can break
deserialization of old rows.

5a. Grep schema for TEXT/BLOB/JSONB/CLOB/XML columns: `BLOB|CLOB|JSONB|JSON\b|TEXT`.
5b. For each LOB column found: check whether it appears in a WHERE, ORDER BY, or JOIN
  in SQL queries or ORM filter expressions.
5c. Grep application code for deserialization + post-filtering:
  `json.loads(`, `JSON.parse(`, `deserialize(` followed by list comprehension / filter.
5d. Check for GIN indexes or expression indexes on LOB columns.
5e. Grep migration history for changes to LOB content structure (adding/renaming JSON fields
  via UPDATE queries or migration helpers).

Record: column name, query-pattern found, whether content is ever filtered/joined.

### Step 6 — Scan for meaningful primary key leakage

WHY: Fowler states "meaningful keys should be distrusted." Business values used as PKs
are supposed to be unique and immutable, but human error makes them neither. A PK cascade
required by a business-rule change (new order number format, SSN correction) touches every
child table — expensive and error-prone.

6a. Inspect schema PKs: flag any that are VARCHAR, CHAR, or named after business concepts
  (`email`, `ssn`, `order_number`, `sku`, `username`, `code`).
6b. Flag composite PKs where both columns carry business meaning.
6c. Check FK references: if child tables reference a meaningful PK, the cascade risk is live.
6d. Check domain objects: if the PK field is exposed as a stable business identifier (`getId()`
  used as `orderNumber` in UI or external API), the business key is leaking.

Record: table, PK definition, FK references, cascade risk assessment.

### Step 7 — Scan for business logic in Gateway classes

WHY: A Table Data Gateway (DAO returning result sets / recordsets) or Row Data Gateway
(per-row accessor) has a single contract: data access — find, insert, update, delete.
When validation, calculation, or workflow logic accumulates in Gateway methods, the Gateway
has drifted toward Active Record without the design intent. Testing requires a live DB even
for logic that has nothing to do with persistence.

7a. Identify Gateway / DAO classes from naming: `*Gateway`, `*DAO`, `*Dao`, `*DataAccess`.
7b. Enumerate public methods. Flag any that are not CRUD verbs:
  `find*`, `insert`, `update`, `delete`, `save`, `get*`.
7c. For non-CRUD methods: read the body — is it a business rule, calculation, or validation?
7d. Check for SQL WHERE clauses that encode business policy (discount eligibility, status
  transitions) rather than just structural filtering.

Record: class, method name, evidence of non-CRUD logic, suggested move-to target.

### Step 8 — Prioritize and produce the audit report

WHY: Not all findings are equal. Data-integrity risks (double-writes, lost updates from
missing Identity Map) must be fixed before performance issues, which must be fixed before
maintainability issues. Prioritizing prevents "fixing smells while the building is on fire."

8a. Rank all findings by severity tier:
  1. **Critical** — Missing Identity Map / proxy identity trap (data integrity)
  2. **High** — N+1 / ripple loading (performance), AR/DM mismatch (correctness)
  3. **Medium-High** — Serialized LOB overuse (query loss + versioning)
  4. **Medium** — Meaningful key leakage (stability), Business logic in Gateway (maintainability)

8b. Write the audit report (see Outputs section).
8c. For each finding, cross-reference the family skill that handles the fix:
  - N+1 → `lazy-load-strategy-implementer`
  - AR/DM mismatch → `data-source-pattern-selector`
  - Serialized LOB / meaningful key → `object-relational-structural-mapping-guide`
  - Business logic in Gateway → `data-source-pattern-selector`

## Inputs

| Input | Required | Description |
|---|---|---|
| Persistence layer source | Yes | Model, gateway, mapper, repository files |
| Schema / DDL | Yes | SQL CREATE TABLE statements or ORM model definitions |
| ORM / framework | Inferred | Detected from imports/build files; ask if ambiguous |
| Domain description | Optional | Helps scope findings; inferred from naming if absent |

## Outputs

**Primary artifact: Anti-Pattern Audit Report**

```markdown
# Data Access Anti-Pattern Audit — [System / Subsystem Name]

**Stack:** [language, ORM, database]
**Date:** [date]
**Scope:** [files reviewed]

---

## Critical Findings

### [AP-ID]: [Anti-Pattern Name]
- **Location:** `path/to/file.py`, line XX–YY
- **Evidence:**
  ```
  [code snippet showing the problem]
  ```
- **Consequence:** [what goes wrong, how badly]
- **Remediation:** [specific fix; cross-ref skill if pattern choice is involved]

---

## High Findings
[same structure]

## Medium-High Findings
[same structure]

## Medium Findings
[same structure]

---

## Summary Table

| Finding | Anti-Pattern | Severity | File | Remediation Skill |
|---|---|---|---|---|
| AP-01 | N+1: Order.line_items | High | orders_controller.rb:42 | lazy-load-strategy-implementer |
| ... | | | | |

---

## Recommended Action Order

1. [Critical findings first, with rationale]
2. [High findings]
3. [Medium findings]
```

## Key Principles

**1. Ripple loading is detectable statically — it doesn't require profiling.**
The shape is always a loop over N entities with an inner DB access. Grep finds it before
the system is ever under load. Do not wait for slow-query logs; find it in the code.

**2. The proxy identity trap is silent until it causes data loss.**
Two proxies for the same row compare as not-equal. There's no exception, no log message —
just incorrect equality checks, phantom dirty-tracking, and version-check failures. An
Identity Map check (single-session discipline, equals() override) is a correctness audit,
not a performance audit.

**3. "Isomorphic schema" is the only condition under which Active Record is correct.**
Active Record works when every domain field maps 1:1 to a column, every domain class maps
1:1 to a table, and the domain has no inheritance or value objects. Any deviation from this
— even a single `to_domain()` helper — signals that Data Mapper is the correct pattern.

**4. A Serialized LOB is correct only when the content will never be queried independently.**
Fowler's test: "Think of a LOB as a way to take a bunch of objects that aren't likely to be
queried from any SQL route outside the application." If a WHERE clause or application-side
filter ever touches the content, the content needs real columns.

**5. Meaningful keys should be distrusted by default.**
Keys need to be unique AND immutable to function correctly. Business values fail both
properties under human error. The cost of a PK cascade far exceeds the cost of adding a
surrogate column early.

**6. Prioritize by data-integrity risk, not by visibility.**
N+1 queries are loud and visible in slow query logs. Missing Identity Map bugs are silent
and only surface as "phantom data" in production. Audit for the silent killers first.

**7. Gateway classes have a single contract: data access.**
A method on a Gateway that is not `find`, `insert`, `update`, or `delete` is a smell.
Business logic in a Gateway is hidden domain behavior that cannot be tested without a
live database — a compound failure of the persistence/domain separation.

## Examples

### Scenario A: Rails E-Commerce App with N+1 on Order Items

**Trigger:** Engineer reports that the orders index page takes 3–8 seconds for 100+ orders.

**Process:**
1. Glob `app/controllers/orders_controller.rb` and `app/views/orders/index.html.erb`.
2. Grep for `.each` in the view; find `order.line_items.count` inside the loop.
3. Confirm `Order.all` in the controller has no `.includes(:line_items)`.
4. Grep `app/models/order.rb` for `has_many :line_items` — default lazy.
5. Severity: High (performance; 1+100 queries for 100 orders).

**Output snippet:**
```markdown
### AP-01: N+1 — Order.line_items in orders#index
- **Location:** `app/views/orders/index.html.erb`, line 14
- **Evidence:** `<%= order.line_items.count %>` inside `orders.each` loop;
  controller: `@orders = Order.all` (no `.includes`).
- **Consequence:** 1 + N SQL queries (1 for orders + 1 per order for line_items).
  With 200 orders: 201 queries per page load.
- **Remediation:** `Order.includes(:line_items)` in controller. Or `.eager_load(:line_items)`.
  Cross-ref: `lazy-load-strategy-implementer`.
```

### Scenario B: Hibernate App — Domain Has Inheritance, AR-Style Mapping

**Trigger:** "Our User entity has a `to_domain()` method and the mapper is constantly wrong."

**Process:**
1. Read `User.java` — finds `User extends BaseEntity` (AR style) with `toUserDomain()` method.
2. Read schema — `users` table has a `type` discriminator column; subtypes `AdminUser`,
   `GuestUser` have different behavior.
3. Confirm `@Entity` on `User` with `@Inheritance(strategy = SINGLE_TABLE)` — STI, not AR.
4. The `toUserDomain()` method converts `User` to a separate `UserDomain` POJO — isomorphism broken.
5. Severity: High (mismatch: domain has inheritance + behavior; AR fighting the ORM).

**Output snippet:**
```markdown
### AP-02: AR/DM Mismatch — User domain inheritance vs flat ActiveRecord
- **Location:** `src/persistence/User.java`, `toUserDomain()` at line 87
- **Evidence:** `User` uses AR-style `@Entity` but contains `toUserDomain()` conversion;
  schema has `type` discriminator for AdminUser/GuestUser subtypes.
- **Consequence:** Every domain operation requires manual conversion; schema changes force
  dual updates to entity and domain class; tests require DB for all domain logic.
- **Remediation:** Replace with proper Data Mapper (JPA Mapper or manual Mapper class) that
  maps User table → AdminUser/GuestUser domain objects. Cross-ref: `data-source-pattern-selector`.
```

### Scenario C: PostgreSQL System — Customer Preferences in JSONB, Queried Frequently

**Trigger:** "We're adding a filter UI for customer preferences and it's slow."

**Process:**
1. Read schema — `customers.preferences` column is `JSONB`.
2. Grep SQL files — find `WHERE preferences->>'theme' = 'dark'` and `WHERE preferences->>'notifications' = 'email'`.
3. Grep migrations — find a migration that renames a JSON key inside `preferences`.
4. Severity: Medium-High (query-loss: querying inside LOB; versioning trap evident).

**Output snippet:**
```markdown
### AP-03: Serialized LOB Overuse — customers.preferences
- **Location:** `db/migrations/20240301_create_customers.sql` (column def),
  `src/queries/customer_filters.sql` (WHERE clause at line 12)
- **Evidence:** `customers.preferences JSONB` column filtered via `->>'theme'` and
  `->>'notifications'` operators; migration 20240512 renames `notif_type` → `notifications`.
- **Consequence:** SQL cannot efficiently filter JSONB without expression index; adding
  expression indexes is schema-within-schema churn; past migration renamed a JSON key
  (versioning trap confirmed).
- **Remediation:** Extract `theme VARCHAR(20)`, `notifications_channel VARCHAR(20)` as
  real columns; retain `preferences JSONB` only for content never filtered directly.
  Cross-ref: `object-relational-structural-mapping-guide`.
```

## References

- `references/anti-pattern-detection-cheatsheets.md` — Per-stack grep patterns, evidence
  classification tables, and diagnostic tests for all six anti-pattern types.
- Fowler, *PEAA* Chapter 3: "Reading in Data" — N+1 avoidance rules; finder method placement.
- Fowler, *PEAA* Chapter 11: "Lazy Load" — Ripple loading definition; proxy identity trap.
- Fowler, *PEAA* Chapter 11: "Identity Map" — Single-instance guarantee; first-level cache.
- Fowler, *PEAA* Chapter 10: "Active Record", "Data Mapper" — Isomorphism requirement;
  When to Use It sections.
- Fowler, *PEAA* Chapter 12: "Identity Field" — Meaningful vs meaningless keys.
- Fowler, *PEAA* Chapter 12: "Serialized LOB" — Queryability loss; versioning trap.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise
Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt,
Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-lazy-load-strategy-implementer`
- `clawhub install bookforge-object-relational-structural-mapping-guide`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
