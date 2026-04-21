---
name: enterprise-architecture-pattern-stack-selector
description: "Select the right enterprise application architecture patterns for every layer of your system using Fowler's PEAA decision framework. Use this skill when designing or refactoring an enterprise app and asking: which domain-logic pattern should I use (Transaction Script, Domain Model, Table Module)? Which persistence pattern fits my stack (Active Record, Data Mapper, Table Data Gateway, Row Data Gateway)? Which web-presentation pattern applies (Front Controller, Page Controller, Template View)? How do I combine these into a coherent full-stack architecture? Triggers include: 'help me choose architecture patterns', 'which Fowler pattern for my app', 'enterprise application architecture', 'PEAA pattern selection', 'layer pattern selection', 'domain logic pattern vs persistence pattern', 'refactor enterprise app to patterns', 'how to structure a Spring/Django/Rails/ASP.NET app', 'what persistence pattern should I use', 'enterprise architecture decision', 'full-stack pattern stack', 'patterns of enterprise application architecture'. This is the hub skill — it maps your subsystem context to per-layer family selector skills and produces a consolidated Pattern Stack Decision Record."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/enterprise-architecture-pattern-stack-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [introduction, 1, 8]
domain: software-architecture
tags: ["enterprise-architecture", "software-architecture", "design-patterns", "persistence", "web-application", "domain-logic", "layered-architecture", "pattern-selection"]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "The enterprise application codebase (domain, persistence, web layers) or a description of the subsystem under discussion."
    - type: user-description
      description: "Stack (language, ORM, web framework), subsystem scope, pain points, and any existing architectural commitments."
  tools-required: [Read, Grep, Glob, Write]
  tools-optional: []
  mcps-required: []
  environment: "An enterprise application codebase (OO language + SQL database + web layer), or a description of one. Works offline from description alone. Output: a Pattern Stack Decision Record markdown document."
discovery:
  goal: "Produce a per-layer pattern stack recommendation for an enterprise application subsystem, routing each architectural layer to the right pattern family and documenting the rationale."
  tasks:
    - "Gather stack, subsystem scope, domain complexity, and existing commitments from the user or codebase"
    - "Route the domain-logic layer to the appropriate pattern family (Transaction Script / Domain Model / Table Module)"
    - "Route the data-source layer based on the domain-logic choice"
    - "Route the web-presentation layer to controller and view patterns"
    - "Apply the First Law of Distributed Object Design and route session-state and concurrency concerns"
    - "Produce a consolidated Pattern Stack Decision Record with per-layer rationale"
  audience:
    roles: ["software-architect", "senior-backend-engineer", "tech-lead", "staff-engineer"]
    experience: "intermediate"
  when_to_use:
    triggers:
      - "Starting greenfield enterprise application design"
      - "Evaluating architectural patterns for a new subsystem in an existing app"
      - "Refactoring a legacy enterprise app and needing a pattern vocabulary"
      - "Team alignment: getting everyone to agree on which patterns apply to each layer"
      - "Architecture review: auditing whether the current pattern stack is appropriate for the domain complexity"
    prerequisites: []
    not_for:
      - "Micro-service topology decisions (this skill addresses in-process layering, not service decomposition)"
      - "Pure front-end or mobile applications with no server-side persistence"
      - "Implementation details of a single pattern (use the family selector skill for that)"
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

# Enterprise Architecture Pattern Stack Selector

## When to Use

Use this skill at the **start of enterprise application design or major refactoring**, when a team needs to select consistent patterns across the domain-logic, data-source, web-presentation, concurrency, and session-state layers of an OO enterprise application backed by a relational database.

This is a **router skill**: it collects your context, routes each architectural layer to the appropriate pattern family, and produces a consolidated Pattern Stack Decision Record. If you have a specific layer question (e.g., only data-source patterns), use the targeted family selector skill instead.

**Prerequisite check before starting:**
- Do you know the target language and framework? (Java/Spring, Python/Django, Ruby/Rails, C#/.NET, TypeScript/Node, etc.)
- Can you describe the domain-logic complexity? (simple CRUD, moderate business rules, complex domain with many variations)
- Are there existing architectural commitments you cannot change? (existing ORM, existing schema, existing framework)

---

## Context and Input Gathering

### Required Context

- **Stack:** language, web framework, ORM or persistence tooling (e.g., Spring Boot + Hibernate, Rails + ActiveRecord, Django + ORM, ASP.NET Core + EF Core, Express + TypeORM).
- **Subsystem scope:** which part of the application are we designing? (all layers, domain only, persistence only, web layer only)
- **Domain-logic complexity:** simple procedural (CRUD, basic calculations) vs moderate (multi-step rules, validations) vs complex (many domain variations, behavior that belongs on entities, revenue recognition style calculations).
- **Existing commitments:** existing schema, team's ORM familiarity, existing framework, whether distribution across processes is already required.

### Observable Context (if codebase is present)

Scan the codebase for:
- `pom.xml`, `Gemfile`, `requirements.txt`, `package.json`, `*.csproj` — detect stack and ORM.
- `src/domain/` or `src/models/` — are there rich entity classes with behavior, or thin data-holder classes?
- `src/persistence/` or `src/repositories/` — hand-rolled SQL vs ORM-mapped classes.
- `src/web/` or `src/controllers/` — one class per route vs a single dispatcher.
- Schema files (`schema.sql`, `migrations/`) — how closely does the schema match the domain model?

### Sufficiency Gate

If domain-logic complexity is unclear, ask: "If I describe two business rules — are they mostly independent procedural steps, or do they interact through shared domain objects with their own behavior?" This distinguishes Transaction Script from Domain Model territory.

---

## Process

### Step 1 — Identify the layers in scope

List which layers the user's question touches: domain logic, data source (persistence), web presentation, concurrency, session state, distribution. If the user said "full stack" or "design my enterprise app", all layers are in scope.

**WHY:** The hub-and-spoke routing only produces value if it's scoped correctly. Selecting data-source patterns without knowing the domain-logic pattern already chosen leads to mismatched recommendations.

---

### Step 2 — Start with the domain-logic layer (the central decision)

Fowler's "Putting It All Together" (Ch 8) is explicit: **the domain-logic choice shapes every downstream layer decision**. The three candidates are:

| Pattern | When to choose |
|---|---|
| **Transaction Script** (procedural service per use-case) | Simple domain logic; team comfortable with procedural style; scripts don't grow complex; low rule-variation count |
| **Domain Model** (rich OO entity graph / DDD-style) | Complex business logic; many domain variations; team has OO modeling skill; willing to invest in O/R mapping |
| **Table Module** (one class per table, record-set oriented) | Moderate complexity; environment with strong record-set tooling (e.g., .NET DataSet, COM+); good middle ground for .NET stacks |

Signals pointing toward Domain Model: duplicate logic spreading across Transaction Scripts; rules that depend on object state (not just database state); complex inheritance in the domain.

If the user's question covers domain logic in detail → invoke `domain-logic-pattern-selector` for deeper decision analysis. If unavailable → ask: "Are your business rules mostly independent per-use-case scripts, or do they involve domain objects with shared state and behavior?"

**WHY:** Getting the domain-logic choice wrong is the most expensive mistake. Choosing Transaction Script when domain complexity demands Domain Model leads to exponential duplication. Choosing Domain Model prematurely for CRUD-only systems adds O/R mapping overhead with no benefit.

---

### Step 3 — Route the data-source layer based on the domain-logic choice

The data-source pattern is **not an independent choice**; it follows from Step 2:

**If Transaction Script was chosen:**
- Prefer **Table Data Gateway** (one class per table, returns record sets) when the platform has strong record-set tooling (DataTable, ResultSet wrappers).
- Prefer **Row Data Gateway** (one object per database row) when you want an explicit typed interface per record.
- Skip Unit of Work and Data Mapper — the script usually wraps its own transaction.
- For the multi-request edit → save pattern, add **Optimistic Offline Lock** (version column). It is almost always the right choice here.

**If Table Module was chosen:**
- **Table Data Gateway** is the natural partner. Table Module + Table Data Gateway "fit together as if it were a match made in heaven" (Fowler, Ch 8).
- No other O/R mapping patterns are typically needed.

**If Domain Model was chosen:**
- Simple Domain Model (schema close to model, few dozen classes) → **Active Record** (each object persists itself) is sufficient.
- Complex Domain Model → **Data Mapper** (separate mapping layer keeps the domain independent of persistence). Adds complexity; use an O/R mapping tool (Hibernate, SQLAlchemy, EF Core, TypeORM) rather than hand-rolling.
- With Data Mapper, add **Unit of Work** (change-tracking session) and **Identity Map** (first-level cache) to avoid stale reads and duplicate-entity bugs. Modern ORMs provide these automatically.

If the user's question is primarily about persistence pattern selection → invoke `data-source-pattern-selector` for full analysis including structural mapping (inheritance, associations). If unavailable → ask: "What is the domain-logic pattern already chosen, and how closely does your class model match your database schema?"

**WHY:** Pairing incompatible domain-logic and data-source patterns is the most common enterprise architecture mistake. Using Data Mapper overhead on a Transaction Script system wastes complexity. Using Active Record on a complex Domain Model creates tight coupling between the domain and the schema.

---

### Step 4 — Route the web-presentation layer

Web-presentation pattern selection is **relatively independent of domain-logic and data-source choices**, but depends on UI complexity and tooling.

**Controller pattern:**
- **Page Controller** (one controller per page or action) — simpler, fits document-oriented sites with few dynamic pages.
- **Front Controller** (single dispatching controller + command objects) — better for complex navigation, many conditional flows, or when shared pre/post-processing is needed (Spring DispatcherServlet, Rails Router, Django URL dispatcher are Front Controllers).
- Add **Application Controller** (workflow/state-machine layer) when navigation logic is complex and involves multi-step workflows. It sits between the web controller and the domain.

**View pattern:**
- **Template View** (JSP, ERB, Jinja2, Razor, Blade) — most common; team uses server-side templates; choose this unless there's a specific reason not to.
- **Transform View** (XSLT-style) — better testability but requires XSLT expertise; uncommon in modern stacks.
- **Two Step View** (logical→physical pipeline) — choose when the same content must render in multiple "skins" or device-specific layouts.

**Recommendation for most stacks:** Front Controller + Template View is the safe default (and what most modern web frameworks implement by default).

If the user's question is primarily about web-presentation → invoke `web-presentation-pattern-selector` for deeper analysis. If unavailable → ask about navigation complexity and whether the application is document-oriented or workflow-oriented.

**WHY:** Choosing Page Controller for a complex, workflow-heavy application creates duplicated pre/post-processing logic across every controller. Choosing Transform View for a team with no XSLT experience creates a skills mismatch.

---

### Step 5 — Apply the First Law of Distributed Object Design

**First Law: Do not distribute.** Run everything in a single process unless you have a hard requirement to separate processes (different security boundary, different deployment cadence, separate team ownership, hardware constraint).

If distribution is required:
- Wrap the domain layer with a **Remote Facade** (coarse-grained service boundary) backed by **Data Transfer Objects** (DTOs) to minimize remote call overhead.
- Never expose fine-grained domain objects directly across a process boundary.
- SQL between application server and database is designed as a remote interface — minimize round-trips with coarse-grained queries.

For session state across requests:
- **Client Session State** (cookie/token-carried state) — stateless server, best scalability; works for small state payloads.
- **Server Session State** (server-memory session) — simpler to implement; creates server affinity; use when state is large or sensitive.
- **Database Session State** — durable, survives server restart; adds DB load; use when session must survive failures.

If the user's question focuses on distribution or session state → invoke `distribution-boundary-designer` or `session-state-location-selector` respectively.

**WHY:** Premature distribution is Fowler's most-cited enterprise architecture anti-pattern. Distributing by domain object class (one process per entity type) makes every business operation a cascade of slow remote calls. The First Law exists because this mistake is pervasive and expensive.

---

### Step 6 — Handle concurrency across requests

For long business transactions that span multiple HTTP requests:
- **Optimistic Offline Lock** (version column / ETag) — default choice; low conflict rate; late detection is acceptable; fits most user-editing workflows.
- **Pessimistic Offline Lock** (application-managed record lock / check-out) — only when conflict rate is high AND the cost of late failure (optimistic collision) is unacceptable to users.
- **Coarse-Grained Lock** — when a business transaction must lock an aggregate (parent + children) atomically; use with either optimistic or pessimistic strategy.
- **Implicit Lock** — enforce locking through framework machinery so callers cannot forget to acquire a lock; the safety net for pessimistic locks.

If the user's question focuses on concurrency → invoke `offline-concurrency-strategy-selector`.

**WHY:** Skipping offline concurrency design leads to lost updates — a persistent source of data corruption in enterprise applications that is hard to diagnose retrospectively.

---

### Step 7 — Produce the Pattern Stack Decision Record

Write a markdown artifact with:
1. **Subsystem:** name and scope.
2. **Stack:** language, framework, ORM.
3. **Domain Logic Layer:** chosen pattern + rationale + forces considered + alternatives rejected.
4. **Data Source Layer:** chosen pattern(s) + rationale + behavioral patterns needed (Unit of Work, Identity Map, Lazy Load).
5. **Web Presentation Layer:** controller pattern + view pattern + rationale.
6. **Concurrency Strategy:** chosen pattern + trigger condition.
7. **Session State Strategy:** chosen pattern + scalability implication.
8. **Distribution:** in-process or Remote Facade + DTO; rationale.
9. **Known Risks:** what to watch for as the system grows (e.g., Transaction Script growing into complex domain logic → upgrade to Domain Model).
10. **Next Steps:** which family selector skills to invoke for detailed implementation guidance.

**WHY:** Without a documented decision record, architectural decisions are re-litigated in every code review. The artifact creates shared vocabulary and makes the forces-and-resolution reasoning visible to the whole team.

---

## Inputs

- **Stack description** (required): language, web framework, ORM/persistence tooling.
- **Domain complexity description** (required): simplicity spectrum from CRUD to complex business rules.
- **Subsystem scope** (required): which layers are in question.
- **Existing commitments** (optional but important): schema, ORM, framework already in use.
- **Codebase** (optional): read `src/`, `schema.sql`, build files to infer stack and patterns in use.
- **Pain points** (optional): N+1 queries, god-object controllers, lost updates, tangled session state — these trigger targeted layer analysis.

---

## Outputs

- **Pattern Stack Decision Record** — a markdown document covering per-layer choices, rationale, forces, and alternatives.
- **Layer routing summary** — which family selector skills to invoke next for implementation depth.
- **Anti-pattern warnings** — if the current stack exhibits known mis-matches (e.g., complex Domain Model with Active Record, Transaction Scripts with no separation from DB logic).

**Output template:**

```markdown
# Pattern Stack Decision Record — [Subsystem Name]

## Stack
- Language / Framework: [e.g., Java 21 / Spring Boot 3]
- ORM / Persistence: [e.g., Hibernate 6 / JPA]
- Web Layer: [e.g., Spring MVC / Thymeleaf]

## Domain Logic Layer
- **Pattern:** [Transaction Script | Domain Model | Table Module]
- **Rationale:** [forces that drove the choice]
- **Alternatives rejected:** [why the others were ruled out]

## Data Source Layer
- **Pattern:** [Table Data Gateway | Row Data Gateway | Active Record | Data Mapper]
- **Behavioral patterns:** [Unit of Work | Identity Map | Lazy Load — as needed]
- **Rationale:** [follows from domain-logic choice + schema complexity]

## Web Presentation Layer
- **Controller:** [Page Controller | Front Controller + Application Controller]
- **View:** [Template View | Transform View | Two Step View]
- **Rationale:** [navigation complexity + team tooling]

## Concurrency Strategy
- **Pattern:** [Optimistic Offline Lock | Pessimistic Offline Lock | Coarse-Grained Lock | Implicit Lock]
- **Trigger:** [when this applies]

## Session State
- **Strategy:** [Client | Server | Database Session State]
- **Scalability implication:** [stateless vs server-affinity vs DB load]

## Distribution
- [Single process — preferred] OR [Remote Facade + DTO — required because: ...]

## Known Risks
- [Growth risks: when to re-evaluate the domain-logic choice]

## Next Steps
- [ ] Invoke `domain-logic-pattern-selector` for implementation depth on domain layer
- [ ] Invoke `data-source-pattern-selector` for persistence pattern detail
- [ ] Invoke `inheritance-mapping-selector` if the schema has inheritance hierarchies
```

---

## Key Principles

**1. Domain-logic choice is the central decision — make it first.**
Every other layer decision is shaped by whether you chose Transaction Script, Domain Model, or Table Module. Reversing this decision later is expensive. Invest time here before designing the persistence or web layers.

**2. The First Law of Distributed Object Design: minimize distribution.**
Every process boundary is a performance tax. Run as much as possible in a single process. Introduce Remote Facade + DTO only where a hard requirement forces a boundary. Do not distribute for the sake of perceived scalability — measure first.

**3. Active Record fits simple Domain Models; Data Mapper fits complex ones.**
Choosing Data Mapper when Active Record would suffice adds unnecessary mapping complexity. Choosing Active Record for a complex Domain Model creates tight coupling that constrains future refactoring. The tipping point is when the schema and the object model begin to diverge significantly.

**4. O/R mapping tools over hand-rolled mappers.**
When Data Mapper is required, use an established mapping tool (Hibernate, SQLAlchemy, EF Core, TypeORM). Hand-rolling a Data Mapper is a significant engineering undertaking — only justified if the tooling is truly unavailable or inappropriate.

**5. Web-presentation patterns are platform defaults — work with them.**
Most modern frameworks have already made the controller choice for you (Spring DispatcherServlet = Front Controller; Rails Router = Front Controller; classic ASP.NET Web Forms ≈ Page Controller). Override the default only when you have a specific reason; fighting the framework's grain is rarely worth the cost.

**6. Optimistic Offline Lock is the right default for multi-request editing.**
Pessimistic locking is harder to implement correctly, creates hanging-lock failure modes, and adds server-affinity pressure. Default to Optimistic Offline Lock (version column) and move to Pessimistic only when you have measured high conflict rates and confirmed that late-failure is unacceptable to users.

**7. Document the pattern stack and keep it visible.**
Architecture decisions fade from team memory. The Pattern Stack Decision Record is a living document — update it when the system grows and a layer's pattern needs to change (e.g., Transaction Scripts outgrowing into Domain Model).

---

## Examples

### Scenario A — Java/Spring Boot + Hibernate enterprise ordering system

**Trigger:** "We're building an order-management system for a B2B wholesaler. Complex pricing rules (tiered discounts, contract pricing, surcharges), multi-step order-approval workflow, 30 developers on multiple teams, Spring Boot + Hibernate stack."

**Process:**
- Step 2 (Domain logic): Complex pricing rules + approval workflow → Domain Model. Transaction Script would produce exponential duplication across pricing rules. Domain Model with Service Layer entry points is the right choice for the approval workflow.
- Step 3 (Data source): Domain Model chosen + complex domain → Data Mapper (Hibernate). Unit of Work (Hibernate Session) + Identity Map (Hibernate L1 cache) + Lazy Load (Hibernate proxy) are provided by the ORM automatically.
- Step 4 (Web): 30 developers + complex navigation → Front Controller (Spring DispatcherServlet, already the default) + Template View (Thymeleaf). Application Controller for the multi-step approval workflow state machine.
- Step 5 (Distribution): Single process preferred. If the order-management system must integrate with an external inventory service → Remote Facade + DTO at that boundary only.
- Step 6 (Concurrency): Multi-request order editing → Optimistic Offline Lock (version column on order entity, enforced by Hibernate `@Version`).
- Step 7 (Session state): Server Session State for the multi-step approval workflow state; Client Session State (JWT) for authentication context.

**Output:** Pattern Stack Decision Record with Domain Model + Data Mapper (Hibernate) + Front Controller + Template View + Optimistic Offline Lock + Server Session State for workflow.

---

### Scenario B — Ruby on Rails / Django application (framework defaults)

**Trigger:** "We're building a SaaS project-management tool. Standard CRUD with some business rules. Small team (5 engineers). Rails (or Django)."

**Process:**
- Step 2 (Domain logic): Moderate complexity — standard project/task CRUD with some validation rules. Table Module or lightweight Domain Model. Rails convention defaults to Active Record pattern at the domain layer (Active Record objects have both data and behavior). Django ORM models follow the same Active Record shape.
- Step 3 (Data source): Active Record is both the domain-logic pattern and the data-source pattern in Rails/Django — the framework has already made this choice. For moderate complexity this is appropriate. Watch for the signal: if business logic starts accumulating in the controller or in callbacks, extract to service objects (Service Layer pattern).
- Step 4 (Web): Front Controller is the default (Rails Router, Django URL dispatcher). Template View is the default (ERB, Django templates). Accept the framework defaults.
- Step 5 (Distribution): Single process. No Remote Facade needed — run Sidekiq/Celery workers in a separate process only for background jobs, not for synchronous domain logic.
- Step 6 (Concurrency): Optimistic Offline Lock — Rails provides `lock_version` column convention; Django provides `select_for_update` or `F` object compare-and-set.
- Step 7 (Session state): Client Session State (signed cookie session — framework default) for most scenarios.

**Output:** Accept framework defaults (Active Record + Front Controller + Template View + Optimistic Offline Lock + Client Session State). Revisit domain-logic pattern if complexity grows.

---

### Scenario C — ASP.NET Core enterprise application (.NET stack)

**Trigger:** "We're migrating a legacy ASP.NET WebForms app to ASP.NET Core + EF Core. Complex lease-calculation logic, 15-person team, SQL Server."

**Process:**
- Step 2 (Domain logic): Complex lease-calculation logic with many rule variations. Fowler explicitly recommends Table Module as the default for .NET (tool ecosystem centered on DataSet/Record Set). However, EF Core enables a proper Domain Model just as easily. Decision: if the team has OO modeling experience and the lease rules are truly complex (not just many fields), Domain Model. If the team is stronger on data-centric thinking, Table Module.
- Step 3 (Data source): Domain Model chosen → Data Mapper (EF Core DbContext is a Unit of Work + Identity Map). Structural mapping (inheritance, associations) configured via EF Core fluent API or data annotations.
- Step 4 (Web): ASP.NET Core MVC is a Front Controller (the framework's default). Template View (Razor). Accept defaults.
- Step 5 (Distribution): Single process (Web + Domain + EF Core in one ASP.NET Core app). Remote Facade only if exposing an API to external consumers (then use a thin API controller as Remote Facade returning DTOs).
- Step 6 (Concurrency): EF Core concurrency tokens (`[Timestamp]` / `rowversion`) → Optimistic Offline Lock by default.
- Step 7 (Session state): Consider Database Session State for lease workflow state (durable across server restarts); Client Session State (JWT) for authentication.

**Output:** Domain Model (or Table Module) + Data Mapper (EF Core) + Front Controller (ASP.NET Core MVC) + Template View (Razor) + Optimistic Offline Lock + Database Session State for durable workflow.

---

## References

- `references/pattern-stack-decision-table.md` — quick-reference routing table: domain-logic pattern → data-source patterns → behavioral patterns needed.
- `references/layer-anti-patterns.md` — common mis-pairings and how to recognize them in a codebase.
- Source: Fowler et al., *Patterns of Enterprise Application Architecture*, Ch. 1 (Layering), Ch. 8 (Putting It All Together), Introduction.

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Patterns of Enterprise Application Architecture* by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-domain-logic-pattern-selector`
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-inheritance-mapping-selector`
- `clawhub install bookforge-object-relational-structural-mapping-guide`
- `clawhub install bookforge-web-presentation-pattern-selector`
- `clawhub install bookforge-offline-concurrency-strategy-selector`
- `clawhub install bookforge-session-state-location-selector`
- `clawhub install bookforge-distribution-boundary-designer`
- `clawhub install bookforge-enterprise-base-pattern-catalog`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
