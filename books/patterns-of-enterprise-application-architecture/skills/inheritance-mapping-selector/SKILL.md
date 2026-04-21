---
name: inheritance-mapping-selector
description: |
  Select the correct ORM inheritance strategy — Single Table Inheritance (STI), Class Table Inheritance (joined table / Multi-Table Inheritance), or Concrete Table Inheritance (table per class) — for any OO inheritance hierarchy that needs to be persisted in a relational database. Use when asked: "which inheritance mapping should I use?", "single table vs joined table inheritance", "STI vs CTI vs table per class", "Hibernate inheritance strategy SINGLE_TABLE vs JOINED vs TABLE_PER_CLASS", "@Inheritance JPA", "Rails STI vs multi-table inheritance", "Django model inheritance type", "how to map inheritance in database", "inheritance in database design", "discriminator column inheritance", "ORM polymorphic query performance", "polymorphic table design", "table per class inheritance trade-offs", "joined inheritance vs single table", "inheritance schema design". Applies at greenfield schema design, ORM configuration, or legacy schema refactoring. Routes to the right strategy on six trade-off dimensions: joins on polymorphic read, wasted column space, FK-constraint enforceability, ad-hoc query readability, refactoring impact, and polymorphism-query cost. Identifies when mixing strategies via Inheritance Mappers is warranted (hierarchy branches with divergent trade-offs). Maps each strategy to idiomatic ORM config: Hibernate/JPA `@Inheritance(SINGLE_TABLE/JOINED/TABLE_PER_CLASS)`, Rails STI type column, Django Multi-Table Inheritance vs abstract base. Produces an inheritance mapping decision record with schema sketch and ORM config snippet.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/inheritance-mapping-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [3, 12]
domain: software-architecture
tags: ["inheritance-mapping", "orm", "persistence", "database-design", "design-patterns", "single-table-inheritance", "class-table-inheritance", "concrete-table-inheritance", "polymorphic-query", "object-relational-mapping", "fowler-peaa", "hibernate", "joined-table-inheritance"]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Description of the OO inheritance hierarchy (class names, field placement, depth), the ORM/framework in use, whether polymorphic reads are frequent, and any schema constraints (FK enforcement, external consumers, existing legacy schema)."
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works from architecture docs, ORM model files, schema files, or a written domain description. Codebase access improves precision but is not required."
discovery:
  goal: "Produce a concrete inheritance mapping recommendation with ORM config, SQL schema sketch, and migration path."
  tasks:
    - "Gather the inheritance hierarchy structure (depth, field distribution, abstract vs concrete classes)"
    - "Identify polymorphic query frequency and whether supertype-level finds are common"
    - "Assess subclass-specific field divergence (similar fields → STI; divergent fields → CTI or Concrete)"
    - "Determine FK constraint requirements and external consumer needs"
    - "Score on six trade-off dimensions to select the primary strategy"
    - "Check if hierarchy branches differ enough to warrant mixing strategies"
    - "Map the recommendation to the team's ORM idiom (Hibernate, Rails, Django, etc.)"
    - "Produce an inheritance mapping decision record with schema sketch and ORM config snippet"
  audience:
    roles: ["software-architect", "senior-backend-engineer", "tech-lead", "database-designer"]
    experience: "intermediate"
  when_to_use:
    triggers:
      - "Designing schema for a new OO domain model with inheritance"
      - "Choosing the `@Inheritance` strategy annotation in Hibernate/JPA"
      - "Deciding whether to use Rails STI or a manual multi-table approach"
      - "Noticing that STI tables are becoming excessively wide with many NULLs"
      - "Noticing that CTI joins are causing performance problems on high-read endpoints"
      - "Refactoring a legacy schema where inheritance was not intentionally designed"
      - "Documenting an architecture decision about how inheritance is persisted"
    prerequisites: []
    not_for:
      - "Choosing which data-source access pattern (Active Record vs Data Mapper) — see `data-source-pattern-selector`"
      - "Full structural mapping patterns (associations, collections, embedded values) — see `object-relational-structural-mapping-guide`"
      - "Query optimization or index tuning — this is a structural design decision, not query-level performance work"
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

# Inheritance Mapping Selector

## When to Use

Relational databases have no native concept of inheritance. Every time an OO hierarchy needs to be persisted, a structural decision must be made: how does the class tree become table(s)? This skill routes that decision.

Apply this skill when:
- You have an OO inheritance hierarchy and need to choose a database schema strategy
- You are configuring `@Inheritance` in Hibernate/JPA or equivalent ORM annotation
- Your current STI table has grown so wide that NULLs dominate most rows
- Your current CTI (joined) queries are slow because every polymorphic read needs a multi-table join
- You are refactoring a legacy schema where inheritance was never explicitly designed

Prerequisites: none. If the domain-logic pattern (Transaction Script / Domain Model) is not yet settled, clarify that first — it affects whether you need inheritance mapping at all.

---

## Context & Input Gathering

Before scoring, collect:

| Input | Why it matters |
|-------|---------------|
| Class hierarchy diagram or description | Reveals depth, abstract vs concrete classes, field placement |
| Subclass-specific field count | High divergence → CTI or Concrete; low divergence → STI |
| Polymorphic read frequency | Frequent supertype queries penalize Concrete Table (UNION) |
| FK constraint requirements | STI cannot enforce FK/NOT NULL on subclass-only columns |
| External DB consumers | Other apps reading the schema favor Concrete (self-contained tables) |
| ORM/framework | Determines which strategies are idiomatically supported |
| Existing schema (if refactoring) | Legacy constraints may limit options |

**Sufficiency check:** You need at minimum the class hierarchy shape and an estimate of polymorphic read frequency. Everything else refines the recommendation.

---

## Process

### Step 1 — Map the hierarchy structure

List all classes: which are abstract, which are concrete, how deep the tree is, and where fields cluster.

*Why:* STI and CTI (joined) require a clear understanding of which classes share common fields. Concrete Table requires knowing all concrete classes, since each gets its own table. Deep hierarchies with many levels favor CTI; shallow hierarchies with low field divergence favor STI.

### Step 2 — Score on six trade-off dimensions

For each of the three candidate strategies, score the trade-offs given this specific hierarchy:

| Dimension | Single Table (STI) | Class Table (CTI) | Concrete Table |
|-----------|-------------------|-------------------|----------------|
| **Joins on polymorphic read** | None — single table query | 1 join per hierarchy level | UNION across all concrete tables |
| **Wasted column space** | High — NULLs for irrelevant subclass columns | None — each row fully relevant | None — each table is self-contained |
| **FK constraint enforcement** | Cannot enforce on subclass-only columns | Full enforcement possible | Per-table only; no FK to abstract supertypes |
| **Ad-hoc query readability** | Poor — sparse rows, mixed types in one table | Good — normalized, clear schema | Good — each table is standalone and readable |
| **Refactoring impact (field moves)** | None — push/pull fields up or down freely | Schema change required per move | Schema change must propagate to all concrete tables |
| **Polymorphism support** | Excellent — single query for any type | Good — join required per level | Poor — UNION or multi-query required |

*Why:* These six dimensions are the primary axes Fowler identifies for distinguishing the three patterns. Scoring them forces an explicit trade-off rather than defaulting to whichever the ORM does by default.

### Step 3 — Apply the primary routing rule

Use the dominant signals to select a strategy:

**→ Single Table Inheritance** when:
- Few subclass-specific columns (most fields live on the superclass)
- Polymorphic reads are frequent and join cost is a concern
- Refactoring the hierarchy is likely (field promotions/demotions should not require schema migration)
- Constraints on subclass columns are not needed

**→ Class Table Inheritance (Joined)** when:
- Subclasses have substantially divergent fields (many NULL columns in STI would be a problem)
- FK integrity on subclass-specific columns is required
- Domain model clarity matters to DBAs or reporting tools
- Polymorphic read frequency is moderate (joins are acceptable)

**→ Concrete Table Inheritance** when:
- Subclasses are largely independent (rarely queried polymorphically)
- Other applications or reporting tools read the database directly and benefit from standalone tables
- Each concrete class stands alone with a full, self-contained schema

*Why:* Fowler offers no single universal recommendation — the decision is genuinely context-dependent. But each strategy has dominant use cases where it wins cleanly.

### Step 4 — Check for mixing

Evaluate whether different branches of the hierarchy have significantly different trade-off profiles.

IF the hierarchy has a stable branch with few subclass fields (STI-favorable) AND a divergent branch with many subclass-specific fields and constraint needs (CTI-favorable):
→ Use Inheritance Mappers as the coordinator layer and apply different strategies per branch.

Fowler explicitly permits this: "The trio of inheritance patterns can coexist in a single hierarchy."

*Why:* Mixing avoids forcing the entire hierarchy into the strategy that fits only the worst-case branch. The Inheritance Mappers pattern provides the implementation scaffold — an abstract mapper per class plus a separate coordinator mapper for the supertype — that makes mixed strategies workable without duplicating load/save logic.

### Step 5 — Map to ORM idiom

Translate the chosen strategy to the team's ORM:

| ORM | STI | CTI (Joined) | Concrete Table |
|-----|-----|-------------|----------------|
| **Hibernate/JPA** | `@Inheritance(strategy = InheritanceType.SINGLE_TABLE)` + `@DiscriminatorColumn` | `@Inheritance(strategy = InheritanceType.JOINED)` | `@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)` |
| **Rails ActiveRecord** | Built-in: add `type:string` column; subclass AR class | Not natively supported (requires manual joins or gems) | Not natively supported |
| **Django ORM** | Abstract base (no shared table, no polymorphism) | Multi-Table Inheritance (default model inheritance) | Proxy models (no new table, same table) |
| **SQLAlchemy** | `polymorphic_on=type_col`, `single_table_inheritance` | `joined_table_inheritance` | `concrete_table_inheritance` |
| **Doctrine (PHP)** | `@InheritanceType("SINGLE_TABLE")` | `@InheritanceType("JOINED")` | `@InheritanceType("TABLE_PER_CLASS")` |

Note: Hibernate's `TABLE_PER_CLASS` (Concrete) generates UNION queries automatically for polymorphic finds. This convenience hides the performance cost — monitor actual query plans.

*Why:* The choice must translate to idiomatic ORM configuration. Choosing CTI and then fighting the ORM defaults erodes the benefit.

### Step 6 — Produce the decision record

Write the inheritance mapping decision record (see Outputs).

---

## Inputs

- **Required:** OO inheritance hierarchy (class names, field locations, depth, abstract vs. concrete)
- **Required:** Polymorphic read frequency estimate (high / medium / low)
- **Helpful:** ORM/framework in use
- **Helpful:** FK constraint and data integrity requirements
- **Helpful:** Whether other systems read the database directly
- **Helpful:** Existing schema (if refactoring)

---

## Outputs

**Inheritance Mapping Decision Record** containing:

```
## Inheritance Mapping Decision — [Hierarchy Name]

### Hierarchy Summary
[Superclass] → [Subclasses list]
Abstract classes: [list]
Concrete classes: [list]
Field distribution: [X fields on superclass, Y per subclass avg]

### Six-Dimension Score
| Dimension           | STI | CTI | Concrete |
|---------------------|-----|-----|----------|
| Joins               | ✅  | ⚠️  | ❌       |
| Wasted space        | ⚠️  | ✅  | ✅       |
| FK enforcement      | ❌  | ✅  | ⚠️       |
| Ad-hoc readability  | ⚠️  | ✅  | ✅       |
| Refactoring impact  | ✅  | ⚠️  | ⚠️       |
| Polymorphism cost   | ✅  | ⚠️  | ❌       |

### Recommendation
**Primary strategy:** [STI / CTI / Concrete / Mixed]
**Rationale:** [2-3 sentences]

### SQL Schema Sketch
[simplified CREATE TABLE statements]

### ORM Configuration
[annotated class snippet for the team's ORM]

### Mixing Note
[IF mixing: which branches use which strategy, and why]

### Migration Path
[steps to get from current state to chosen strategy]
```

---

## Key Principles

**1. Single Table is Fowler's default for simple hierarchies — with explicit caveats.**
STI wins on query simplicity and refactoring tolerance. Its costs (NULLs, no constraints) are real but manageable for hierarchies with few subclass-specific fields. Fowler's own Player/Footballer/Cricketer example uses it as the primary illustration. The caveat: once subclass-specific field count grows substantially, the NULL bloat and constraint inability become genuine liabilities.

**2. Class Table (Joined) buys normalization at the cost of joins — and joins compound with depth.**
CTI is the most "object-aligned" strategy: one table per class mirrors the class hierarchy. Its cost is that loading any object requires touching multiple tables. For a two-level hierarchy (parent + one child table), one join is tolerable. For a four-level hierarchy, you may be joining four tables per load. Monitor query plans; the supertype table also becomes a bottleneck since every query touches it.

**3. Concrete Table's UNION penalty is the silent killer.**
Concrete Table looks attractive in isolation: no joins, no NULLs, self-contained tables. The danger emerges when someone queries at the supertype level. The ORM (or developer) must UNION all concrete tables. As the hierarchy grows, this query becomes increasingly expensive. Concrete Table is appropriate only when polymorphic supertype queries are rare or absent.

**4. FK constraints are incompatible with STI for subclass-specific columns.**
If a Footballer must have a `club` and that column must be NOT NULL and FK-constrained, STI cannot enforce this — the column exists on all rows, including Cricketers who have no club. CTI (or Concrete) is required when FK integrity on subclass fields is non-negotiable.

**5. Mixing is the escape hatch — use it deliberately, not ad-hoc.**
Fowler explicitly endorses mixing strategies within one hierarchy. The right way to implement mixing is the Inheritance Mappers pattern: each class has its own mapper (abstract or concrete), and a separate coordinator mapper handles supertype-level operations. Do not mix strategies without this scaffolding — the result is tangled load/save logic that is difficult to maintain.

**6. Keys must be unique across all tables in Concrete Table — the database won't enforce this for you.**
When using Concrete Table, the database's primary key constraint only guarantees uniqueness within one table. A Footballer with id=42 and a Cricketer with id=42 are valid in the database — but they will collide on any polymorphic Identity Field lookup. You need a cross-table key allocation strategy (e.g., a shared sequence, UUID keys, or application-level key tracking).

---

## Examples

### Example 1: Sports Player Hierarchy (STI recommended)

**Scenario:** SportsDB system models Player (name, dateOfBirth) with three subclasses: Footballer (club, position), Cricketer (battingAverage), Bowler (bowlingSpeed, bowlingStyle). The application frequently loads "all active Players" for reporting and roster views. Hierarchy is unlikely to deepen further.

**Trigger:** "Should we use STI or separate tables for Player/Footballer/Cricketer? We need to query all players at once frequently."

**Process:**
1. Hierarchy: 3 concrete classes, 1 abstract base. Subclass-specific fields: 1–2 per subclass. Field divergence is low.
2. Dimension score: STI wins on joins (none), refactoring tolerance (none), polymorphism (single query). Cost: wasted columns for ~2–3 nullable columns per row — tolerable. No FK constraint requirement on club or battingAverage.
3. Routing: STI. Fowler uses this exact example to demonstrate Single Table Inheritance.
4. Mixing: Not needed — all branches are similar in shape.
5. ORM config: Hibernate `@Inheritance(SINGLE_TABLE)` with `@DiscriminatorColumn(name="type")` on Player; `@DiscriminatorValue("F")` on Footballer.

**Output (schema sketch):**
```sql
CREATE TABLE players (
  id         BIGINT PRIMARY KEY,
  type       VARCHAR(1) NOT NULL,      -- discriminator: F, C, B
  name       VARCHAR(100) NOT NULL,
  club       VARCHAR(100),             -- Footballer only
  batting_avg DECIMAL(5,2),            -- Cricketer only
  bowling_speed INT,                   -- Bowler only
  bowling_style VARCHAR(50)            -- Bowler only
);
```

---

### Example 2: Organization Hierarchy with Strict Constraints (CTI recommended)

**Scenario:** HR system with LegalEntity (taxId, registeredAddress) as abstract base, Corporation (stockExchange, tickerSymbol), Partnership (partnerCount), SoleTrader (tradingName) as concrete subclasses. Every Corporation must have a non-null stockExchange. The compliance team requires FK integrity on all subtype-specific columns. Polymorphic reads ("load any LegalEntity by id") occur at application startup only; most queries are type-specific.

**Trigger:** "We need strict FK constraints on Corporation fields. Can we still use inheritance?"

**Process:**
1. Hierarchy depth: 2 levels. Subclass fields: 3–5 per subclass, highly divergent.
2. Dimension score: FK enforcement → CTI required (STI cannot enforce NOT NULL on stockExchange for Corporations). Refactoring impact acceptable (hierarchy is stable by design). Polymorphic reads are infrequent → join cost acceptable.
3. Routing: Class Table Inheritance (Joined). Hibernate `@Inheritance(JOINED)`.
4. Mixing: Not needed.

**Output (schema sketch):**
```sql
CREATE TABLE legal_entities (id BIGINT PRIMARY KEY, tax_id VARCHAR(20), address TEXT, type VARCHAR(20));
CREATE TABLE corporations (id BIGINT REFERENCES legal_entities(id), stock_exchange VARCHAR(10) NOT NULL, ticker VARCHAR(10) NOT NULL);
CREATE TABLE partnerships (id BIGINT REFERENCES legal_entities(id), partner_count INT NOT NULL);
CREATE TABLE sole_traders (id BIGINT REFERENCES legal_entities(id), trading_name VARCHAR(100) NOT NULL);
```

---

### Example 3: Independent Product Types, Rarely Queried Polymorphically (Concrete recommended)

**Scenario:** E-commerce catalog with Product as abstract base and three highly divergent concrete types: PhysicalProduct (weight, dimensions, shippingClass), DigitalProduct (fileSize, downloadUrl, licenseType), SubscriptionProduct (billingCycle, trialDays, renewalPolicy). Each has 8–12 unique fields. The reporting team queries each type independently ("all digital downloads this month"). Polymorphic "all products" queries exist only in one admin view.

**Trigger:** "Our Product table is a mess — 40 columns, half NULL on any given row. What's the alternative?"

**Process:**
1. Subclass fields: 8–12 per subclass, highly divergent. Only 3 shared fields on Product (id, name, price).
2. Dimension score: Current STI is the problem (wasted space). Concrete Table wins on no NULLs, self-contained tables, per-class query performance. Cost: polymorphic "all products" query → UNION. But this query is rare (one admin view).
3. Routing: Concrete Table Inheritance. Cross-table key uniqueness → use UUID primary keys.
4. Key uniqueness: UUIDs eliminate the cross-table collision problem.
5. Polymorphic admin view: Accept a UNION query here — document the performance expectation; cache if needed.

**Output (schema sketch):**
```sql
CREATE TABLE physical_products (id UUID PRIMARY KEY, name VARCHAR, price DECIMAL, weight_kg DECIMAL, dim_cm VARCHAR, shipping_class VARCHAR);
CREATE TABLE digital_products (id UUID PRIMARY KEY, name VARCHAR, price DECIMAL, file_size_mb INT, download_url TEXT, license_type VARCHAR);
CREATE TABLE subscription_products (id UUID PRIMARY KEY, name VARCHAR, price DECIMAL, billing_cycle VARCHAR, trial_days INT, renewal_policy VARCHAR);
-- Polymorphic admin query:
SELECT id, name, price, 'physical' AS type FROM physical_products
UNION ALL SELECT id, name, price, 'digital' FROM digital_products
UNION ALL SELECT id, name, price, 'subscription' FROM subscription_products;
```

---

## References

- `references/six-dimension-trade-off-matrix.md` — Full trade-off matrix with rationale per cell and worked examples
- `references/inheritance-mappers-scaffold.md` — Inheritance Mappers implementation pattern for mixed-strategy hierarchies
- `references/orm-config-reference.md` — ORM configuration snippets for Hibernate, Rails, Django, SQLAlchemy, Doctrine

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-object-relational-structural-mapping-guide`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
