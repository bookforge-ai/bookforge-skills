---
name: object-relational-structural-mapping-guide
description: "Object-relational mapping structural patterns guide. Use when designing or auditing how domain objects map to relational tables — identity fields, foreign key mapping, association table mapping for many-to-many relationships, dependent mapping for child objects with cascade delete, embedded value for value object mapping, and serialized LOB for JSON column or blob storage. Applies when choosing ORM associations (Hibernate, SQLAlchemy, EF Core, ActiveRecord, Django ORM), deciding between a join table and nested foreign keys, mapping address or money value objects as inline columns, or detecting serialized LOB overuse on queryable data. Covers the six PEAA structural patterns: Identity Field (surrogate key vs meaningful key), Foreign Key Mapping (single-valued reference), Association Table Mapping (many-to-many via join table), Dependent Mapping (child lifecycle owned by parent), Embedded Value (value object as columns), Serialized LOB (graph serialized to JSON/BLOB column)."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/object-relational-structural-mapping-guide
metadata: {"openclaw":{"emoji":"🗂️","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [3, 12]
domain: persistence
tags:
  - object-relational-mapping
  - persistence
  - orm
  - database-design
  - design-patterns
  - associations
  - value-objects
  - cascade-delete
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Domain model classes, existing ORM mappings, schema SQL/migrations, and build files (to detect ORM in use)"
    - type: user description
      description: "Domain model relationships to map, current pain points (N+1, cascade failures, unmappable queries), and ORM stack"
  tools-required:
    - Read
    - Glob
    - Grep
    - Edit
    - Write
  tools-optional:
    - Bash
  mcps-required: []
  environment: "Enterprise application codebase with OO domain model and relational database. ORM stack detectable from build files or imports. Schema available as .sql, migrations, or ORM model definitions."
discovery:
  goal: "Map every relationship and value structure in a domain model to the correct PEAA structural pattern, producing a structural mapping design document with schema sketches and ORM config for each."
  tasks:
    - "Classify each domain class relationship by structural type (identity / 1:1 / 1:N / N:M / dependent / embedded / graph)"
    - "Route each to the correct structural pattern using the decision table"
    - "Generate schema sketch (table columns, FK constraints, join tables)"
    - "Provide idiomatic ORM configuration for the detected stack"
    - "Flag anti-patterns: meaningful keys, Serialized LOB on queryable data, nested FK attempts at N:M, dependent with external FK references"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
      - framework-designer
    experience: intermediate
  when_to_use:
    triggers:
      - "Designing a new domain model's persistence layer from scratch"
      - "Auditing an existing ORM configuration for structural anti-patterns"
      - "Deciding between a join table and a FK column for a new relationship"
      - "Mapping a value object (Address, Money, DateRange) — should it be its own table or inline columns?"
      - "Evaluating whether to use a JSON/JSONB column for nested data"
      - "N+1 or cascade-delete bug traced to wrong mapping choice"
      - "ORM config uses meaningful primary keys and team wants to refactor"
    prerequisites: []
    not_for:
      - "Inheritance mapping decisions (use inheritance-mapping-selector for Single/Class/Concrete Table Inheritance)"
      - "Choosing between Table Data Gateway, Active Record, or Data Mapper (use data-source-pattern-selector)"
      - "Concurrency and locking design (use offline-concurrency-strategy-selector)"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: "{filled by tester}"
      baseline: "{filled by tester}"
      delta: "{filled by tester}"
    tested_at: "{filled by tester}"
    eval_count: "{filled by tester}"
    assertion_count: 13
    iterations_needed: "{filled by tester}"
---

# Object-Relational Structural Mapping Guide

Six PEAA patterns that bridge between OO domain objects and relational tables: Identity Field, Foreign Key Mapping, Association Table Mapping, Dependent Mapping, Embedded Value, and Serialized LOB.

## When to Use

Use this skill when you are:

- Designing how a domain model maps to a relational schema for the first time
- Auditing an existing ORM configuration and schema for structural problems
- Deciding how to map a specific relationship type (1:1, 1:N, N:M, value object, child graph)
- Evaluating whether a JSON/BLOB column is the right choice for nested data
- Debugging N+1 queries, cascade failures, or query-impossible data buried in a LOB

**Not for:**
- Inheritance hierarchies → use `inheritance-mapping-selector`
- Data-source gateway selection (Active Record vs Data Mapper) → use `data-source-pattern-selector`

## Context & Input Gathering

Gather before proceeding:

**Required:**
- List of domain classes with their relationships and cardinalities (1:1, 1:N, N:M)
- Which objects are value objects (no identity, owned by another object) vs. entities (independent identity)
- ORM stack in use (Hibernate/JPA, EF Core, SQLAlchemy, Django, ActiveRecord, TypeORM, or hand-rolled)

**Observable from codebase:**
- Existing ORM annotations / model definitions (detect from `@Entity`, `models.Model`, `Column`, etc.)
- Schema migrations or DDL files (detect FK patterns, join tables, LOB columns)
- Build files (`pom.xml`, `requirements.txt`, `*.csproj`, `Gemfile`) to confirm ORM version

**Ask if absent:**
- "Which classes have independent lifecycles (can be loaded/deleted on their own)?"
- "Are there many-to-many relationships? Do the associations carry their own attributes (e.g., a role or start date)?"
- "Is there any data currently stored as XML, JSON, or binary blob? What SQL queries run against it?"

**Sufficiency check:** Proceed once you have the domain class list, relationship cardinalities, and a yes/no on value object identity. ORM stack helps with the output but is not blocking.

## Process

### Step 1 — Identify all domain structures

For each domain class and relationship, classify it into one of these structural types:

| Type | Signal |
|------|--------|
| **Entity with identity** | Can be loaded/deleted independently; has a unique ID |
| **Value object** | No independent identity; always belongs to one owner (Money, Address, DateRange) |
| **Single-valued reference** | One object holds a reference to exactly one other entity |
| **Collection reference (1:N)** | One object holds a collection of other entities; each child knows its parent |
| **Many-to-many reference** | Both sides hold collections pointing at each other |
| **Dependent child** | Child exists only in the context of an owner; no external references to child |
| **Complex nested graph** | Hierarchical or graph structure that would require many joins relationally |

*WHY:* Each structural type maps to exactly one pattern. Misclassifying here leads to wrong pattern choice (e.g., treating a Value Object as an entity creates an unnecessary table and Identity Map entry).

### Step 2 — Apply the pattern routing table

| Structure | Pattern | Key rule |
|-----------|---------|----------|
| Every persistable entity | **Identity Field** | Use surrogate (auto-assigned) key — never meaningful keys |
| Single-valued reference (1:1, N:1) | **Foreign Key Mapping** | FK lives in the "many" or "child" table |
| 1:N collection (entity children) | **Foreign Key Mapping** | FK lives in child table; parent has collection in memory, not in the table |
| N:M relationship | **Association Table Mapping** | Always use a join table — even if no attributes today |
| Child with no independent identity | **Dependent Mapping** | No Identity Field on child; owner mapper handles all persistence |
| Value object (DDD Value Object) | **Embedded Value** | Map value's fields as columns on the owner's table |
| Non-queryable complex subgraph | **Serialized LOB** | Only when SQL queries will NEVER need to filter by content |

*WHY:* This routing table encodes the core insight that objects and relations have fundamentally different link representations. Without this explicit classification, teams default to wrong choices: adding FK columns for N:M (violates first normal form), creating tables for value objects (unnecessary complexity), or Serialized LOB for data later needing SQL queries (queryability trap).

### Step 3 — Apply Identity Field to all entities

For every entity class (not value objects, not dependents):

1. **Always prefer a surrogate key** (auto-assigned integer or UUID). Meaningful keys (email, SSN, order number) appear stable but fail in practice: human input errors break both uniqueness and immutability.
2. **Prefer simple (single-column) keys.** They enable a Layer Supertype with uniform key handling. Compound keys require per-class handling and carry implicit meaning that tends to leak.
3. **Key type:** 64-bit integer (`BIGINT`) is the best default — fast equality check, fast increment, effectively unlimited range. UUIDs/GUIDs provide database-wide uniqueness at the cost of larger index size and slower inserts (random insertion order).
4. **Inheritance caveat:** With Class Table or Concrete Table Inheritance, keys must be unique across the hierarchy, not just per-table, to avoid Identity Map collisions.

*WHY:* The Identity Field is the bridge between the object graph and the relational schema. Without it, you cannot map FK references back to in-memory objects. Without surrogate keys, you inherit the fragility of the real world into your database contract.

### Step 4 — Map relationships

**Foreign Key Mapping (1:1 and N:1):**
- The FK column lives in the table of the class that holds the reference in memory.
- For a collection (1:N), the FK lives in the child table (structural inversion: the parent holds a collection in OO, but the child table holds the FK in SQL).
- Write order: insert parent first, then children, to satisfy FK constraints.

**Association Table Mapping (N:M):**
- Create a link table with two FK columns (one per side).
- The link table has no corresponding domain object and no Identity Field of its own.
- Its PK is the compound of both FKs.
- Treat the link table like a Dependent Mapping — delete all links for one side and re-insert on update.
- If the association acquires its own attributes (role, start_date), promote the link table to a first-class entity with its own Identity Field and Foreign Key Mappings on both sides.

*WHY for Association Table:* There is no alternative for N:M in relational databases. Attempts to model N:M with a list-of-IDs column violate first normal form and make queries and updates extremely painful. Even if the association has no attributes today, using a join table preserves schema flexibility for when attributes appear.

### Step 5 — Map child structures

**Dependent Mapping:**
- Apply when: child object has no independent identity, is always loaded with its owner, and is never referenced by foreign keys from other tables.
- The child class has no Identity Field, no Identity Map entry, and no independent finder methods.
- The owner's mapper (or ORM cascade config) handles all inserts, updates, and deletes.
- On update: delete all dependents for the owner, then re-insert (safe because no external FK references exist).
- If another table needs a direct FK to the child, the child is not truly dependent — give it an Identity Field and use Foreign Key Mapping instead.

**Embedded Value:**
- Apply to all DDD Value Objects (Money, Address, DateRange, GeoPoint, etc.).
- Map each value field as a column on the owner's table (e.g., `employment.salary_amount`, `employment.salary_currency`).
- The value class has no persistence methods of its own; the owner saves/loads it.
- Do NOT use Embedded Value if: (a) the value is shared across multiple owners, (b) there can be a variable number of values per owner, or (c) you need to sort/filter on the value's fields via SQL independently of the owner.

*WHY for Embedded Value:* Value Objects have no identity and should never have their own table — a table of Money values or Address values is meaningless without context. Embedding them preserves the OO semantics (the value is part of the owner, not related to it) while avoiding extra joins and unnecessary tables.

### Step 6 — Evaluate any graph / LOB candidates

For complex hierarchical or graph structures:

1. Can the structure be represented with a self-referencing FK (e.g., `parent_id` on an organization table)? If yes, prefer this — it keeps data queryable.
2. If the structure is truly too complex to normalize, and **you are certain SQL will never need to filter or join on the internal fields**, consider Serialized LOB.
3. Choose format: JSON/JSONB (PostgreSQL, MySQL 5.7+) is preferred over XML for readability and tooling; binary BLOB is compact but opaque and fragile to class changes.
4. Verify the anti-pattern checklist for Serialized LOB (see Key Principles).

*WHY:* Serialized LOB sacrifices SQL queryability for schema simplicity. This trade-off is acceptable for truly private, complex, non-queryable subgraphs. It is a trap when applied to data that reporting queries, search, or business logic will need to inspect.

### Step 7 — Produce the structural mapping design document

For each entity and relationship, output:

```
[ClassName / Relationship]
  Pattern: <pattern name>
  Schema: <table/columns/constraints sketch>
  ORM config: <annotation or model field>
  Rationale: <why this pattern fits>
  Anti-pattern warning: <if applicable>
```

Review cross-cutting concerns:
- Write ordering for inserts (parent before child for all FK relationships)
- Cascade delete configuration (Dependent Mapping → cascade all; FK Mapping → decide per relationship)
- Identity Map interaction (only entities with Identity Field enter the Identity Map; dependents and value objects do not)

## Inputs

- Domain model class list with relationships and cardinalities
- Value object identification (which classes lack independent identity)
- ORM stack and version
- Existing schema (if mapping to a pre-existing database)
- Any current LOB/JSON columns and the SQL queries that run against them

## Outputs

A **structural mapping design document** containing:

1. **Pattern assignment table** — every entity, value object, and relationship mapped to a pattern with rationale
2. **Schema sketch** — table definitions (columns, types, FK constraints, join tables)
3. **ORM configuration** — idiomatic annotations/model fields for the detected stack
4. **Write-order dependency graph** — insert/update ordering to satisfy FK constraints
5. **Anti-pattern flags** — any meaningful keys, LOB-queryability risks, or orphaned FK references identified

**Output template (per structure):**

```markdown
## [Structure Name]
**Pattern:** [Pattern Name]
**Schema:**
  [table_name]([pk] BIGINT PK, [fk] BIGINT FK → [other_table.pk], [field] TYPE, ...)
**ORM:**
  [stack-specific annotation/field declaration]
**Rationale:** [1-2 sentences on why this pattern fits]
**Warning:** [if anti-pattern risk exists]
```

## Key Principles

**1. Surrogate keys over meaningful keys — always.**
Meaningful keys (SSN, email, order number) require uniqueness AND immutability from the real world, which human error and business rule changes routinely violate. Surrogate auto-assigned keys give you control over both. Fowler's framing: "take a rare stand on the side of meaninglessness."

**2. Association Table Mapping is the only correct answer for N:M.**
Any attempt to encode a many-to-many with a list-of-IDs column violates first normal form and will make future queries impossible. Use a join table, even if the association has no attributes today — you will thank yourself when it acquires them.

**3. Dependent Mapping requires no-external-FK discipline.**
A child object only qualifies as a dependent if no other table holds a FK reference to its table. The moment another entity needs a direct reference to the child, the child needs its own Identity Field and becomes a standalone entity mapped via Foreign Key Mapping.

**4. All Value Objects should use Embedded Value.**
DDD Value Objects (Money, Address, DateRange) have no independent identity. Giving them their own table and Identity Field is wrong — it implies identity they don't have and adds joins where none are needed. The owner table absorbs their columns.

**5. Serialized LOB is a trap for queryable data.**
The check is binary: will SQL ever need to filter, sort, or join on data inside the column? If yes, normalize it. PostgreSQL JSONB operators and XPath do not change this calculus — they are not portable and do not perform at scale like indexed normalized columns.

**6. The structural inversion rule for 1:N.**
In OO, the parent holds the collection (album has tracks). In the relational model, the FK is on the child (track.album_id). This inversion is the source of most ORM confusion. The rule: **the FK always lives on the "many" side of the relationship**, regardless of which direction the OO association points.

**7. When a join table acquires attributes, promote it to an entity.**
The moment a link table needs its own data (start_date, end_date, role, weight), it should become a first-class entity with its own Identity Field and explicit Foreign Key Mappings on both sides. This is a DDD relationship-as-entity promotion.

## Examples

### Example 1: E-Commerce Order Domain

**Trigger:** Team is designing the persistence layer for an order management system. Domain classes: Customer, Order, LineItem, Address (value object for shipping and billing).

**Process:**
- Customer: entity → Identity Field (surrogate `customer_id BIGINT`)
- Order: entity → Identity Field; references Customer → Foreign Key Mapping (`order.customer_id FK → customers.customer_id`)
- LineItem: child with no independent identity, only exists within Order → Dependent Mapping (`order_id, sequence` composite PK or surrogate; cascade all)
- ShippingAddress / BillingAddress: Value Objects → Embedded Value (columns `shipping_street`, `shipping_city`, `shipping_zip`, `billing_street`, etc. on the `orders` table)
- Order ↔ Promotion (a customer's Order can use multiple Promotions, and a Promotion applies to multiple Orders): N:M → Association Table Mapping (`order_promotions(order_id, promotion_id)`)

**Output:**
```sql
customers(customer_id BIGINT PK, name VARCHAR)
orders(order_id BIGINT PK, customer_id BIGINT FK, 
       shipping_street VARCHAR, shipping_city VARCHAR, shipping_zip VARCHAR,
       billing_street VARCHAR, billing_city VARCHAR, billing_zip VARCHAR)
line_items(line_item_id BIGINT PK, order_id BIGINT FK, product_id BIGINT FK, 
           quantity INT, unit_price DECIMAL)
order_promotions(order_id BIGINT FK, promotion_id BIGINT FK, PRIMARY KEY(order_id, promotion_id))
```

LineItem uses cascade-delete. ShippingAddress and BillingAddress are Embedded Value — no join needed to load them. Order↔Promotion uses a join table with no attributes (yet).

---

### Example 2: Music Library with Dependent Tracks

**Trigger:** Mapping the Artist/Album/Track domain from PEAA Chapter 12.

**Process:**
- Artist: entity → Identity Field (`artist_id BIGINT`)
- Album: entity, references Artist → Identity Field + Foreign Key Mapping (`album.artist_id FK → artists.artist_id`)
- Track: child of Album with no identity outside Album context; no other table references Track directly → Dependent Mapping. Album mapper loads/saves/deletes all Tracks. Track has no independent finder.
- Track has no Identity Field; Album mapper deletes-and-reinserts all Tracks when Album is saved.

**Output schema:**
```sql
artists(artist_id BIGINT PK, name VARCHAR)
albums(album_id BIGINT PK, artist_id BIGINT FK, title VARCHAR)
tracks(album_id BIGINT FK, sequence INT, title VARCHAR, duration INT,
       PRIMARY KEY(album_id, sequence))
```

ORM (Hibernate): `@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)` on Album → tracks. Tracks loaded when Album is loaded.

---

### Example 3: Legacy LOB Anti-Pattern Detection

**Trigger:** Existing system stores customer contact preferences as XML CLOB in the `customers` table. Support team needs to query "all customers who prefer email contact." Currently impossible via SQL.

**Process:**
- Identify: `customers.preferences_xml CLOB` — a Serialized LOB.
- Apply check: Do SQL queries need to filter on data inside the LOB? Yes — `preferred_channel = 'email'` must be queryable.
- Verdict: Anti-pattern. Serialized LOB used for queryable data.
- Recommendation: Normalize to a `customer_preferences` table: `(customer_id BIGINT FK, preference_key VARCHAR, preference_value VARCHAR)` or `(customer_id, channel ENUM, enabled BOOLEAN)`. Apply Foreign Key Mapping.
- Exception path: If the preference structure is complex and evolving AND a reporting-only database handles the queries, Serialized LOB with JSONB can remain in the operational DB while the reporting DB normalizes the structure.

## References

- [Pattern Decision Table](references/pattern-decision-table.md) — Full routing table with edge cases
- [ORM Mapping Cheatsheet](references/orm-mapping-cheatsheet.md) — Per-pattern ORM config for Hibernate/JPA, EF Core, SQLAlchemy, Django, Rails, TypeORM
- [Anti-Pattern Checklist](references/anti-pattern-checklist.md) — Detection signals for all 5 structural anti-patterns

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-inheritance-mapping-selector`
- `clawhub install bookforge-data-access-anti-pattern-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
