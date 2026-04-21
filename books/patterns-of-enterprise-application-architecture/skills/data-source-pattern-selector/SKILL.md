---
name: data-source-pattern-selector
description: |
  Choose the right data access pattern — Table Data Gateway, Row Data Gateway, Active Record, or Data Mapper — for a persistence layer. Use when asked "should I use Active Record or Data Mapper?", "which ORM pattern fits my app?", "when does Hibernate-style mapping make sense vs. Rails ActiveRecord?", "how do I structure my database access layer?", "data mapper or active record for my domain model?", "Row Data Gateway vs Active Record", "Table Data Gateway vs Data Mapper", "Fowler data source patterns", "persistence layer design", "ORM pattern selection", "choose ORM pattern", "database access layer architecture", "Hibernate vs Rails persistence style". Applies when designing a new persistence layer or refactoring an existing one. Routes each domain-logic pattern (Table Module, Transaction Script, Domain Model) to its natural data-source counterpart. Identifies the Active Record / Data Mapper mismatch anti-pattern (AR when schema is not isomorphic with objects; DM when AR would suffice). Maps each pattern to modern framework idioms: Rails ActiveRecord → AR pattern; Hibernate / Spring Data JPA / EF Core → DM; Django ORM → AR-leaning; SQLAlchemy Core → TDG-style; SQLAlchemy ORM → DM; Laravel Eloquent → AR. Warns against business logic creeping into Gateway classes. Produces a pattern decision record with rationale, framework notes, and migration path. If the domain-logic pattern has not yet been chosen, invoke `domain-logic-pattern-selector` first.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/data-source-pattern-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [3, 10]
tags: ["data-access", "persistence", "orm", "database", "design-patterns", "software-architecture", "active-record", "data-mapper", "table-data-gateway", "row-data-gateway", "fowler-peaa", "object-relational-mapping", "enterprise-patterns"]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "System description including: the chosen (or candidate) domain-logic pattern, schema shape, language and ORM framework, whether the schema is owned by this team or external, team sophistication, and any current pain points with data access."
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with codebase analysis, architecture documents, schema files, or a written project description."
discovery:
  goal: "Produce a concrete data-source pattern recommendation with rationale, framework mapping, anti-pattern warnings, and migration path."
  tasks:
    - "Determine the already-chosen or candidate domain-logic pattern (Table Module, Transaction Script, Domain Model)"
    - "Assess schema isomorphism with domain objects (high = AR-friendly; low = DM)"
    - "Assess business logic weight on domain objects (none = TDG/RDG; moderate-to-heavy = AR or DM)"
    - "Apply the routing matrix to produce a primary pattern recommendation"
    - "Map the recommendation to the team's language/framework idiom"
    - "Identify applicable anti-patterns and warn against them"
    - "Output a pattern decision record with rationale and migration path"
  audience:
    roles: ["software-architect", "senior-backend-engineer", "tech-lead", "framework-designer"]
    experience: "intermediate-to-advanced"
  when_to_use:
    triggers:
      - "Starting a new service and choosing how to structure database access"
      - "Refactoring a persistence layer that has grown messy or tightly coupled to the schema"
      - "Evaluating whether to adopt an ORM and which style (AR-style vs. DM-style)"
      - "Noticing Active Record classes that have become fat with complex domain logic and inheritance"
      - "Noticing a full Data Mapper layer that feels over-engineered for simple CRUD"
      - "Choosing between Rails-style ORM and Hibernate-style ORM for a new stack"
      - "Documenting an architecture decision about persistence-layer design"
    prerequisites:
      - "Some clarity about domain-logic approach (even a guess). If unknown, run `domain-logic-pattern-selector` first."
    not_for:
      - "Choosing a specific database product (PostgreSQL vs. MySQL) — this skill selects the access pattern, not the product"
      - "Concurrency control patterns (optimistic/pessimistic locking) — see `unit-of-work-implementer` or `optimistic-lock-advisor`"
      - "Query optimization or index design — this is an architectural pattern selection, not a performance tuning skill"
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
    assertion_count: 14
    iterations_needed: "{filled by tester}"
---

# Data Source Pattern Selector

## When to Use

You are designing or refactoring the persistence layer of an enterprise application and need to choose *how* objects talk to the database. The four canonical options — Table Data Gateway, Row Data Gateway, Active Record, Data Mapper — differ not just in complexity but in what they assume about domain object structure and business logic placement.

This skill applies when:
- You are choosing a data-access approach before — or alongside — selecting an ORM framework
- Your Active Record classes have started accumulating complex inheritance, collections, or non-trivial business logic and things feel messy
- You suspect your full Data Mapper layer is overkill for a largely CRUD application
- You want to document a persistence architecture decision with clear rationale

**If the domain-logic pattern (Table Module, Transaction Script, Domain Model) has not yet been chosen, the data-source pattern cannot be selected reliably.** Invoke `domain-logic-pattern-selector` first, or ask the user to describe their domain-logic approach before proceeding.

---

## Context & Input Gathering

### Required
- **Domain-logic pattern in use or planned:** Table Module / Transaction Script / Domain Model — this is the primary routing axis.
- **Schema shape:** Is the database schema closely aligned with how you model objects in code, or does it differ significantly? Are there inheritance hierarchies, embedded collections, or many-to-many associations that don't map neatly to tables?
- **Business logic weight:** Do domain objects carry significant behavior (validation, calculations, policies), or is the application largely CRUD?
- **Language and framework:** What language and ORM/database library are in use or being evaluated? (Rails, Hibernate, Django, SQLAlchemy, EF Core, Laravel, etc.)

### Helpful
- **Schema ownership:** Does your team control the schema, or is it a legacy/external schema you must conform to? (External schemas often push toward Data Mapper for isolation.)
- **Team sophistication:** Larger or more complex mapping layers (Data Mapper) require more experience to implement and maintain.
- **Existing code artifacts:** Any domain classes, repository interfaces, or gateway classes already in the codebase signal where the current approach sits.

### Defaults if not specified
- Unknown domain-logic pattern → ask before proceeding (this is a hard prerequisite)
- Unknown schema shape → assume moderate complexity; flag isomorphism check as required
- Unknown framework → provide pattern-level recommendation; offer framework mapping as a separate step

---

## Process

**Step 1 — Identify the domain-logic pattern.**

WHY: The domain-logic pattern is the primary determinant of which data-source pattern fits. Fowler is explicit: Table Module pairs with Table Data Gateway; Domain Model pairs with Active Record or Data Mapper. Choosing a data-source pattern independently from domain-logic pattern creates structural mismatches that compound over time.

- Table Module → go directly to **Table Data Gateway** (Step 5). No further analysis needed.
- Transaction Script → go to Step 2 to pick TDG vs RDG.
- Domain Model → go to Step 3 to pick AR vs DM.
- Unknown → invoke `domain-logic-pattern-selector` or ask the user to describe domain-logic approach.

**Step 2 — Transaction Script: choose TDG vs RDG.**

WHY: Both Gateway patterns separate SQL from application logic, but they differ in their result shape. The choice is about what is more convenient for the Transaction Script to work with — a result set / record set, or a per-row object.

- Prefer **Table Data Gateway** when: the environment has good Record Set support (.NET ADO.NET DataSet, JDBC ResultSet consumed directly), when scripts prefer to iterate over result sets rather than object collections, or when stored procedures are the access mechanism (stored procs naturally map to TDG).
- Prefer **Row Data Gateway** when: the environment favors per-row objects, when you want object-oriented field access in scripts, or when you anticipate logic accumulating on the gateway and want a natural refactoring path toward Active Record.
- Note: If you observe business logic creeping into either gateway class, that is the signal to refactor toward Active Record (Step 5a).

**Step 3 — Domain Model: assess schema isomorphism.**

WHY: Active Record works well only when the schema is isomorphic with domain objects — one table per class, fields map one-to-one to columns. The moment inheritance hierarchies, embedded value objects, rich collections, or divergent naming appear, Active Record mapping becomes patchwork. Isomorphism is the primary AR/DM split criterion.

Evaluate isomorphism:
- HIGH (AR-friendly): Each domain class corresponds to one table. No inheritance in the domain. Field names map cleanly to column names. No complex associations beyond simple foreign keys.
- LOW (DM territory): Inheritance hierarchies in the domain. Collections mapped across multiple tables. Domain objects named and shaped for business concepts, schema named for normalization. External/legacy schema that the domain must adapt to.

**Step 4 — Domain Model: assess business logic weight.**

WHY: Data Mapper is justified by domain model complexity. If the domain model is simple (validations, derivations, single-record logic), Active Record carries that complexity at low cost with no extra layer. If the domain model has complex policies, multi-object calculations, or needs to be testable without a database, Data Mapper's isolation pays off.

- Simple business logic (CRUD + validations + single-record derivations) → lean toward **Active Record**.
- Complex business logic (multi-entity rules, domain events, complex state machines, aggregate roots, test isolation needed) → lean toward **Data Mapper**.

**Step 5 — Apply the routing matrix and select pattern.**

WHY: Combines Steps 1–4 into a single recommendation. Mixing patterns at the primary persistence level is a known anti-pattern — it creates confusion about where persistence logic lives and where domain logic lives.

| Domain-Logic Pattern | Schema Isomorphism | Business Logic Weight | → Data-Source Pattern |
|---|---|---|---|
| Table Module | — | — | **Table Data Gateway** |
| Transaction Script | — | — | TDG (result-set style) or RDG (object style) |
| Domain Model | High | Low | **Active Record** |
| Domain Model | High | Growing / complex | **Active Record** → plan migration to DM |
| Domain Model | Low | Any | **Data Mapper** |
| Domain Model | Any | Heavy / test-isolated | **Data Mapper** |

**Step 6 — Map to framework idiom.**

WHY: Pattern selection is only useful if it connects to the team's actual tooling. Each major ORM embodies one of the four patterns; choosing the pattern misaligned with the framework requires fighting the framework's defaults.

- **Active Record pattern:** Rails ActiveRecord (naming intentional), Django ORM model classes, Laravel Eloquent, Grails GORM.
- **Data Mapper pattern:** Hibernate (Java), Spring Data JPA (via Hibernate), Entity Framework Core (especially with separate repository layer), SQLAlchemy ORM (with `Session` and mapped classes), TypeORM (repository mode), Doctrine ORM (PHP).
- **Table Data Gateway:** ADO.NET DataSet/TableAdapter (.NET classic), stored-procedure wrappers, SQLAlchemy Core (execute + handle result sets directly), JDBC direct usage.
- **Row Data Gateway:** Less common in modern frameworks; often hand-rolled or generated from metadata. Appears in legacy Java/C# codebases before frameworks matured.

**Step 7 — Check for anti-patterns.**

WHY: Even the correct pattern recommendation fails if common misuses are not flagged upfront. These are the most frequent failure modes Fowler identifies.

Check each:
- [ ] **AR with non-isomorphic schema**: Using Active Record when the domain has inheritance hierarchies, value object collections, or complex associations that don't map 1:1 to tables. Symptom: lots of `has_many :through`, STI workarounds, or manual column overrides. Fix: migrate to Data Mapper.
- [ ] **Premature Data Mapper**: Full mapping layer (Hibernate, hand-rolled mappers) for a largely CRUD application with simple domain. Symptom: enormous mapper configuration, trivial domain classes. Fix: evaluate whether Active Record would suffice.
- [ ] **Business logic in Gateway classes**: TDG or RDG methods that contain validation, calculation, or domain rules. This is Active Record by another name — but without intent. Fix: either commit to Active Record or strip the logic out.
- [ ] **Mixed primary persistence patterns**: Using both Active Record and Data Mapper for different parts of the same domain model. Fowler: "you don't want to mix them because that ends up getting very messy."

**Step 8 — Produce the decision record.**

WHY: Pattern selection without documented rationale gets revisited and second-guessed. A one-page decision record captures the reasoning, making future refactoring decisions faster.

Output: See Outputs section below.

---

## Inputs

- Domain-logic pattern name (Table Module / Transaction Script / Domain Model)
- Schema shape description (isomorphic vs. divergent, presence of inheritance/collections)
- Business logic weight (CRUD-only vs. complex policies)
- Language and ORM framework
- Optional: existing codebase, schema files, architecture docs

---

## Outputs

**Pattern Decision Record** (written to a markdown file or returned inline):

```
# Data Source Pattern Decision Record

## Context
- Domain-logic pattern: [Table Module | Transaction Script | Domain Model]
- Schema isomorphism: [High | Medium | Low]
- Business logic weight: [Low | Moderate | Heavy]
- Language / framework: [e.g., Java / Hibernate]

## Recommended Pattern
**[Table Data Gateway | Row Data Gateway | Active Record | Data Mapper]**

## Rationale
[2-4 sentences connecting domain-logic pattern + isomorphism + logic weight to the recommendation]

## Framework Mapping
- This project uses [framework], which implements the [pattern] style natively.
- [Any idiomatic notes or configuration guidance]

## Migration Path (if applicable)
[e.g., "Currently using RDG; as business logic accumulates on row objects, refactor to AR by
moving Transaction Script logic into the gateway class, renaming to domain classes."]

## Anti-Patterns to Watch
- [AR/DM mismatch warning if applicable]
- [Business-logic-in-gateway warning if applicable]

## Related Patterns Triggered
- Unit of Work: [needed / not needed] — [reason]
- Identity Map: [needed / not needed]
- Lazy Load: [consider / not applicable]
```

---

## Key Principles

**1. Domain-logic pattern is the primary routing axis, not a preference.**
The data-source pattern is constrained by domain-logic choice, not independent of it. Table Module cannot work without Table Data Gateway. Domain Model with complex logic cannot sustain Active Record cleanly. This is why `domain-logic-pattern-selector` must run first.

**2. Schema isomorphism is the Active Record / Data Mapper split criterion.**
Active Record requires one-to-one correspondence between class and table structure. When domain objects diverge from the schema — through inheritance, value objects, or separate evolution — Data Mapper becomes necessary. Trying to force AR onto a non-isomorphic schema produces layered hacks.

**3. The four patterns form a progression, not a menu.**
TDG → RDG → AR → DM is a progression of increasing capability and increasing complexity. The appropriate pattern is the simplest one that handles the domain-logic complexity. Over-engineering (premature DM) is as damaging as under-engineering (AR for complex domain).

**4. Business logic in a Gateway class is a smell, not a feature.**
If logic accumulates in a TDG or RDG, the class is evolving into an Active Record. That evolution is fine if intentional; it is an anti-pattern if unintentional, because it violates the Gateway's contract of pure data access.

**5. Data Mapper buys independent evolution, at a cost.**
DM lets the database schema and object model evolve independently — you can rename a table without touching domain code, or add a collection without altering the schema. The cost is the mapping layer itself: more code, more configuration, more tooling. Only justified when that independence is actually needed.

**6. Framework choice reflects pattern choice — fight the framework at your peril.**
Rails assumes Active Record pattern. Hibernate assumes Data Mapper. Using Hibernate like Active Record (loading everything into rich entities for simple CRUD) is as problematic as using Rails AR for a rich domain with complex inheritance. Choose the framework whose default pattern matches the one this skill recommends.

**7. Do not mix primary persistence patterns in the same domain.**
Mixing AR and DM for different domain classes creates two parallel mental models for how persistence works. Fowler is explicit: pick one primary pattern and apply it consistently. DM can call TDG internally (as a layering technique), but that is a deliberate architectural choice, not mixing.

---

## Examples

### Scenario A: Ruby on Rails e-commerce app with standard domain

**Trigger:** "We're building an online store with Rails. Products, Orders, Users — standard stuff. Should we use ActiveRecord or something like Trailblazer's Data Mapper approach?"

**Process:**
1. Domain-logic pattern: Transaction Script evolving toward Domain Model — validation and simple calculation on models. Standard Rails.
2. Schema isomorphism: HIGH — each model maps to one table, no unusual inheritance.
3. Business logic weight: LOW to MODERATE — discount calculations, order state transitions, nothing requiring test isolation from DB.
4. Routing matrix: Domain Model (simple) + High isomorphism + Low-moderate logic → **Active Record**.
5. Framework mapping: Rails ActiveRecord implements this natively.
6. Anti-pattern check: Flag that AR will strain if the domain grows to include complex pricing rules, product hierarchies, or external pricing APIs. Plan for that threshold and document it.

**Output:** Recommend Active Record. Use Rails ActiveRecord natively. Add a note: "When Product becomes a polymorphic hierarchy with >3 types and complex pricing rules, reassess toward Data Mapper using a separate service/repository layer."

---

### Scenario B: Java enterprise app with complex domain, legacy schema

**Trigger:** "We have a Java application with a complex insurance policy domain — policies, coverages, endorsements, riders, pricing rules. Legacy Oracle schema from 2003 that doesn't match how we model policies in code. Team of 20, using Spring."

**Process:**
1. Domain-logic pattern: Domain Model — clear from the description (policies, endorsements, pricing rules).
2. Schema isomorphism: LOW — legacy schema with 2003 naming, coverage modeled differently than in code, likely separate pricing tables.
3. Business logic weight: HEAVY — pricing rules, endorsements, riders all suggest complex domain behavior.
4. Routing matrix: Domain Model + Low isomorphism + Heavy logic → **Data Mapper**.
5. Framework mapping: Spring + Hibernate = Data Mapper pattern implemented. Use JPA `@Entity` with `@Column` mapping to isolate domain names from schema names. Repository interfaces provide finder behavior.
6. Anti-pattern check: Warn against "anemic domain model" — putting all logic in service classes while entities are DTOs. That removes DM's benefit. Domain logic should live in domain classes, not in Spring `@Service` beans.

**Output:** Recommend Data Mapper via Hibernate/JPA. Domain classes in `src/domain/`, repository interfaces in `src/persistence/`. Isolate schema column names in `@Column(name="POLICY_COVG_AMT")` mappings. Plan Unit of Work via JPA `EntityManager` + transaction boundaries.

---

### Scenario C: .NET WinForms reporting app with data grids

**Trigger:** "We're building an internal reporting tool in C# .NET. Lots of data grids, editable tables, CRUD screens that mirror database tables. Using DataSets and DataGridViews."

**Process:**
1. Domain-logic pattern: Table Module — screens correspond to tables, data grids bind to record sets.
2. No need to assess isomorphism or business logic weight — Table Module mandates TDG.
3. Framework mapping: ADO.NET DataSet + DataAdapter + DataGridView is the canonical .NET Table Data Gateway implementation. TableAdapter in the Visual Studio dataset designer IS a TDG.
4. Anti-pattern check: Do not add business logic to gateway classes. Validation that spans multiple tables belongs in a separate validation layer, not in the TableAdapter.

**Output:** Confirm Table Data Gateway. Use ADO.NET DataAdapter/DataSet pattern or TableAdapter. Return DataSet from gateway methods to bind to DataGridView controls. Keep gateway classes free of business logic.

---

## References

- `references/pattern-routing-matrix.md` — Complete routing table with all branching conditions
- `references/anti-pattern-catalog.md` — Detailed descriptions of each anti-pattern with detection criteria and remediation steps
- `references/framework-pattern-map.md` — Extended framework mapping (20+ ORM frameworks) organized by pattern
- `references/migration-paths.md` — Step-by-step migration guides: TDG→RDG, RDG→AR, AR→DM

**Downstream skills triggered by this skill's output:**
- If Data Mapper selected → `unit-of-work-implementer` (commit sequencing, dirty tracking)
- If Lazy Load needed → `lazy-load-strategy-implementer`
- If audit of existing persistence code → `data-access-anti-pattern-auditor`

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler et al.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-domain-logic-pattern-selector`
- `clawhub install bookforge-unit-of-work-implementer`
- `clawhub install bookforge-lazy-load-strategy-implementer`
- `clawhub install bookforge-data-access-anti-pattern-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
