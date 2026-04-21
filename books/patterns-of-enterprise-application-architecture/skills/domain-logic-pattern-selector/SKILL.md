---
name: domain-logic-pattern-selector
description: "Choose domain logic pattern for enterprise application subsystems: Transaction Script vs Domain Model vs Table Module, and decide Service Layer thickness. Use when organizing business logic, choosing between procedural service methods and rich domain models, selecting enterprise app architecture, routing domain logic to the right pattern, deciding anemic domain model vs rich domain model, applying Fowler's complexity-vs-effort curve, determining when to use Domain Model, when to use Transaction Script for simple CRUD, when Table Module fits .NET RecordSet environments, deciding Service Layer facade vs operation script vs controller-entity, avoiding transaction-script-sprawl, avoiding anemic-domain-model anti-pattern, preventing stored-procedure logic leakage, structuring enterprise app business logic, domain logic organization, choose domain pattern, enterprise app business logic design."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/domain-logic-pattern-selector
metadata: {"openclaw":{"emoji":"🗂️","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [2, 9]
domain: software-architecture
tags:
  - domain-logic
  - enterprise-architecture
  - software-architecture
  - design-patterns
  - business-logic
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: description
      description: "Subsystem description: what the module does, the nature of the business rules (simple CRUD, rule-heavy, algorithmic), team OO experience, language and stack (Java, C#, Python, .NET, JVM), any existing patterns in place, and whether multiple client types or transactional resources are involved."
    - type: codebase
      description: "Optional: existing domain and service code to diagnose current pattern and detect anti-patterns."
  tools-required:
    - Read
    - Grep
    - Write
  tools-optional:
    - Glob
  mcps-required: []
  environment: "Enterprise application codebase or architecture discussion. Works offline. Codebase helpful but not required — skill operates on description alone."
discovery:
  goal: "Route a subsystem to Transaction Script, Domain Model, or Table Module, decide Service Layer thickness, and produce a domain-logic pattern decision record."
  tasks:
    - "Classify the subsystem's domain complexity (simple CRUD → rule-heavy → rich invariant-laden domain)"
    - "Apply complexity × team × platform routing matrix to select primary pattern"
    - "Decide whether a Service Layer is warranted and, if so, what thickness"
    - "Check for anti-pattern risk (Transaction Script sprawl, anemic domain model, stored-procedure logic leakage)"
    - "Produce a domain-logic pattern decision record with rationale, migration path, and implementation sketch"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
    experience: intermediate
  when_to_use:
    triggers:
      - "Starting a new subsystem or module and need to decide how to organize domain logic"
      - "Existing code shows Transaction Script sprawl (god-class service with duplicated conditional logic)"
      - "Existing code has an anemic domain model (data-only classes with all behavior in services)"
      - "Team debating whether to use Domain Model or keep procedural Transaction Scripts"
      - "Evaluating whether a Service Layer is needed and how thick it should be"
      - ".NET project with ADO.NET RecordSets and uncertainty about Table Module applicability"
      - "Legacy codebase migrating from stored procedures and need a domain-logic pattern to migrate toward"
      - "Complex business rules growing unmanageable in Transaction Scripts"
    prerequisites: []
    not_for:
      - "Choosing data-source patterns (ORM, Active Record, Data Mapper) — invoke data-source-pattern-selector for those"
      - "Choosing presentation-layer patterns (MVC, Front Controller, Template View)"
      - "Concurrency or session-state decisions"
      - "Systems with no domain logic at all (pure data passthrough APIs)"
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

# Domain Logic Pattern Selector

Choose between Transaction Script, Domain Model, and Table Module for a subsystem, then decide how thick to make the Service Layer. Based on Fowler's Patterns of Enterprise Application Architecture (Ch 2 + Ch 9).

## When to Use

Use this skill when starting or refactoring a subsystem and the central question is: _how should business logic be organized?_ This is distinct from _where_ that logic persists (data-source patterns) or _how_ it is presented.

Typical triggers: greenfield module design, Transaction Script code growing unmanageable, a team debate about "should we use DDD?", evaluating whether to add a service layer, diagnosing anemic domain model or script sprawl in legacy code.

Prerequisites: none. Works from a verbal description of the subsystem; codebase access improves diagnosis.

## Context & Input Gathering

Ask the user (or read from codebase) in this order:

**Required:**
1. **What does the subsystem do?** One paragraph — the nouns (entities), the operations (use cases), and the outputs.
2. **How complex is the business logic?** Pick the best match:
   - Simple: mostly CRUD, a few validations, no conditional algorithms
   - Moderate: validations + multi-step calculations + some conditional rules
   - Complex: many rules that interact, vary by product/customer/time, change frequently
3. **What is the team's OO experience?** Low (procedural background), moderate (OO-familiar but not DDD-trained), high (experienced with rich domain models, strategy/composite patterns).
4. **What is the language and stack?** Java/JVM, C#/.NET, Python, TypeScript, Ruby, etc. If .NET, is ADO.NET / RecordSet usage widespread?

**Observable from codebase (if provided):**
- Service classes with many long methods containing `if/else` chains → Transaction Script
- Classes with fields but no methods (getters/setters only) → anemic domain model signal
- Behavior scattered across utility/helper classes → Transaction Script sprawl
- SQL or stored-procedure calls embedded directly in business-logic code → stored-procedure leakage
- Dataset/DataTable types flowing through business logic (.NET) → Table Module context

**Defaults if not specified:**
- Team OO experience: moderate
- Stack: JVM (Java/Kotlin) unless .NET signals are present

**Sufficiency test:** Proceed once complexity level and team experience are known. Stack is tie-breaker for moderate complexity.

## Process

### Step 1 — Classify Domain Complexity

WHY: Fowler's core insight is that the cost curves for the three patterns cross at different complexity points. Choosing the wrong pattern for the complexity level locks the team into a wall of effort as logic grows.

Map the subsystem to one of three complexity bands:

| Band | Signals | Cost Curve Behavior |
|------|---------|---------------------|
| **Low** | Pure CRUD, few validations, minimal branching | All three patterns are cheap. Transaction Script wins on simplicity. |
| **Moderate** | Multi-step calculations, conditional rules, some shared logic | Transaction Script starts showing duplication. Domain Model pays off if team is OO-comfortable. Table Module is viable if RecordSet tooling is strong. |
| **High** | Rules vary by product/customer/time, complex invariants, frequent changes, algorithmic variation | Transaction Script hits exponential complexity wall. Domain Model is the only pattern that manages growth gracefully. |

If the codebase is available: grep for service methods longer than ~50 lines with nested conditionals. That is a high-complexity signal even if the requirement description sounds simple.

### Step 2 — Apply the Routing Matrix

WHY: Complexity alone does not determine the best pattern. Team OO experience shifts the cost curve for Domain Model (familiar teams pay the ramp-up cost once; unfamiliar teams pay it every sprint). Platform shifts the appeal of Table Module (RecordSet tooling makes it a natural fit in .NET; without that tooling it is pointless friction).

```
ROUTING MATRIX
─────────────────────────────────────────────────────────────────────
Complexity   Team OO Exp    Platform         → Recommended Pattern
─────────────────────────────────────────────────────────────────────
Low          any            any              → Transaction Script
Moderate     low            any              → Transaction Script (with extraction discipline)
Moderate     moderate/high  .NET + RecordSet → Table Module
Moderate     moderate/high  Java/Python/TS   → Domain Model (simple variant)
High         low            any              → Domain Model + coaching (or Table Module in .NET as interim)
High         moderate/high  any              → Domain Model
─────────────────────────────────────────────────────────────────────
```

**Platform defaults (Fowler's explicit guidance):**
- **.NET with ADO.NET / DataSet**: Table Module is the natural fit. Fowler says "I don't see a reason to use Transaction Script in a .NET environment" once RecordSet tooling is present.
- **Java / JVM**: Domain Model is the natural target for moderate-to-high complexity. POJOs (plain old Java objects) with Data Mapper is the recommended implementation — avoid entity beans for rich domain models.
- **Python / Ruby / TypeScript**: Domain Model with Active Record is viable for simple-to-moderate domains; Data Mapper for rich ones.

**Refactoring direction rule:** If starting fresh or refactoring up — Transaction Script → Domain Model is a well-worn path. Going the other direction (Domain Model → Transaction Script) is rarely worthwhile unless you can also simplify the data-source layer. Start simple; refactor up when complexity demands.

**Mixed patterns are allowed.** Transaction Script for some use cases, Domain Model for the core rules — Fowler explicitly calls this common.

### Step 3 — Decide Service Layer

WHY: A Service Layer defines the application boundary — where transaction control and security live, and what coarse-grained API client layers (UI, APIs, messaging consumers) call into. Adding it unnecessarily layers overhead; omitting it when multiple client types exist causes cross-cutting logic to scatter.

**Add a Service Layer when ANY of these are true:**
- More than one kind of client (UI + REST API, UI + message consumer, UI + batch job)
- A use case response must be transacted atomically across multiple resources (database + message queue + email)
- Need a distinct, stable API boundary (versioning, remote access, access control)

**Skip the Service Layer when:**
- Single client type (a UI), simple use cases, single transactional resource
- Page Controllers can control transactions directly by delegating to the domain or data-source layer

**Thickness — three variants:**

| Variant | Description | When to Use | Fowler's Verdict |
|---------|-------------|------------|-----------------|
| **Domain Facade** (thin) | Service layer methods are one-liner delegations to the Domain Model. No business logic here. | When Domain Model is rich and self-contained. | Preferred by Fowler when using Domain Model. |
| **Operation Script** (thick) | Service methods contain application logic (notifications, workflow coordination, cross-resource transactions), delegating domain logic to domain objects. | When application logic (workflow, integration, notifications) must be coordinated. | Fowler's pick for applications with application-logic responsibilities. |
| **Controller-Entity** (mid) | Use-case-specific logic in service/controller scripts; shared logic on entities. | Common but risky — tend to produce duplication. | Fowler warns against this as a starting point; useful only when refactoring from Transaction Script. |

**Avoid stored procedures for domain logic.** Reserve stored procedures for batch jobs and extreme performance requirements only. Placing business rules in stored procedures creates logic you cannot test, version, or refactor as a domain model.

### Step 4 — Check Anti-Pattern Risk

WHY: Pattern choices create pressure toward specific failure modes. Flagging the risk up front lets the team establish guards before the anti-pattern takes hold.

| Chosen Pattern | Primary Anti-Pattern Risk | Early Warning Signs | Guard |
|---------------|--------------------------|--------------------|----|
| Transaction Script | **Transaction Script Sprawl**: logic duplicated across scripts; one god-class service | Methods >50 lines; copy-pasted validation blocks; service class >500 lines | Extract shared logic into domain objects; set line-count budget |
| Domain Model | **Anemic Domain Model**: classes with only getters/setters; all behavior in service layer | Domain class has zero methods beyond accessors; service layer orchestrates every operation | Move behavior onto entities; services handle only application logic |
| Domain Model | **Bloated Domain Model**: domain objects absorbing use-case-specific UI behavior | Domain class imports UI or HTTP types | Move use-case-specific logic to service layer or presentation; keep domain pure |
| Table Module | **Stored-Procedure Logic Leakage**: rules drift into the database | Business conditionals in SQL; procedures called from Table Module | Keep calculation logic in Table Module C# / VB class, not in SQL |

**Anemic Domain Model** is Fowler's most prominent warning: a system that uses Domain Model classes but has stripped behavior out into service classes reduces the pattern to an expensive object-relational mapping exercise with none of the encapsulation benefit. If your "domain model" has no methods beyond getters and setters, it is a data transfer layer, not a domain model.

### Step 5 — Produce the Decision Record

WHY: A written record anchors the decision, gives future maintainers the context to maintain pattern consistency, and becomes a checklist for code review.

Produce a **Domain-Logic Pattern Decision Record** containing:

```
## Domain-Logic Pattern Decision Record: [Subsystem Name]

### Classification
- Complexity band: [low / moderate / high]
- Team OO experience: [low / moderate / high]
- Stack / platform: [Java / .NET / Python / ...]

### Primary Pattern: [Transaction Script | Domain Model | Table Module]
**Rationale:** [1-2 sentences applying the routing matrix]

### Service Layer: [None | Domain Facade | Operation Script | Controller-Entity]
**Rationale:** [Why needed / not needed; thickness reasoning]

### Anti-Pattern Watch
- Risk: [name]  Warning sign: [observable symptom]

### Migration Path (if refactoring)
[Starting point → recommended direction → end state]

### Implementation Sketch
[5-10 lines of pseudocode or language-idiomatic code showing the structural skeleton]

### Pair With Data-Source Pattern
[Brief note on which data-source pattern pairs with the chosen domain pattern]
```

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Subsystem description | Yes | What it does, the entities, the use cases |
| Complexity level | Yes | Low / moderate / high (or description to classify) |
| Team OO experience | Yes | Low / moderate / high |
| Language / stack | Yes (for tie-breaking) | JVM, .NET, Python, etc. |
| Existing codebase | No | Helps diagnose current pattern and anti-patterns |
| Multiple client types? | No | Defaults to single client (no Service Layer) |

## Outputs

- **Domain-Logic Pattern Decision Record** (markdown) — primary output
- **Routing rationale** — explicit complexity × team × platform reasoning
- **Anti-pattern risk flags** — with early warning signs and guards
- **Implementation skeleton** — language-idiomatic structural sketch
- **Service Layer decision** — thickness recommendation with rationale
- **Data-source pairing note** — which data-source pattern to combine with the chosen domain pattern

## Key Principles

1. **Complexity determines the crossover point, not personal preference.** Fowler's complexity-vs-effort graph shows that Domain Model costs more upfront but grows sub-linearly while Transaction Script cost grows super-linearly. The crossover is real but cannot be measured precisely — use experienced judgment on domain complexity signals.

2. **Team experience shifts the curve but does not override complexity.** A team unfamiliar with OO domain models lowers the break-even point (they pay ramp-up cost longer), but high-complexity domains still demand Domain Model eventually. The alternative is unbounded Transaction Script sprawl.

3. **Platform preference is Fowler's explicit tie-breaker.** .NET RecordSet tooling makes Table Module the natural mid-complexity choice. Without that tooling, Table Module adds no value over a simple Domain Model with Active Record.

4. **Refactor up, rarely down.** If you start with Transaction Script and complexity grows: refactor toward Domain Model. If you start with Domain Model and want simplicity: going back to Transaction Script is rarely worth it unless you simultaneously simplify the data-source layer.

5. **The anemic domain model is a pattern failure, not a design choice.** Stripping behavior from domain classes into services defeats the purpose of Domain Model. If your domain classes have no methods, you are paying ORM complexity without the encapsulation benefit.

6. **Service Layer thickness should match application-logic responsibility.** Thin facade when the Domain Model carries all logic. Operation script when use cases require coordinating notifications, messaging, and multi-resource transactions. Avoid controller-entity as an architectural style — it tends to replicate Transaction Script duplication inside the service layer.

7. **Mixed patterns are legitimate.** Simple subsystems within a Domain Model application can use Transaction Script. The patterns are not mutually exclusive — the key is conscious, documented choice.

## Examples

### Scenario A — Revenue Recognition Engine (Complex Rules → Domain Model)

**Trigger:** A team building a SaaS billing system. Revenue recognition rules vary by product type: word processors recognize 100% immediately; spreadsheets spread recognition over three dates; databases over two; and the CFO adds new product categories quarterly.

**Process:**
- Classify: High complexity — rules vary by product, change frequently, involve calculations and date logic.
- Route: Domain Model (complexity high → Domain Model regardless of team experience).
- Service Layer: Operation Script — use case requires updating the database and notifying contract administrators atomically.
- Anti-pattern check: Risk of anemic domain model if the recognition strategy is placed in the service layer. Guard: `RevenueRecognition` objects should carry the `isRecognizableBy(date)` method; strategy subclasses should carry `calculateRevenueRecognitions()`. The service layer only coordinates the transaction and sends notifications.

**Output:** Domain Model with `Contract`, `Product`, `RevenueRecognition`, and a strategy hierarchy (`CompleteRecognitionStrategy`, `ThreeWayRecognitionStrategy`). `RecognitionService` is an Operation Script service layer that delegates domain logic to domain objects and handles email/integration notifications.

---

### Scenario B — Simple Order Management (.NET CRUD → Table Module)

**Trigger:** A .NET team building internal order management. Rules are mostly: validate fields, calculate totals, apply standard discounts. All UI is data-grid based. ADO.NET DataSets flow through every layer.

**Process:**
- Classify: Low-to-moderate complexity. No complex invariants, no algorithmic variation.
- Route: Table Module. .NET RecordSet tooling is present; the calculation logic fits naturally in table-oriented classes.
- Service Layer: None needed — single client (a Windows Forms UI), single transactional resource.
- Anti-pattern check: Watch for stored-procedure logic drift. Keep discount calculation in the `Order` Table Module, not in a SQL stored procedure.

**Output:** `Contract` Table Module, `Product` Table Module, `RevenueRecognition` Table Module operating on a shared `DataSet`. No domain object identity — every operation takes a primary key parameter.

---

### Scenario C — Legacy Transaction Scripts Hitting Complexity Wall → Refactor to Domain Model

**Trigger:** A Java team's billing service has grown to a 2,000-line `BillingService` class. Discount logic is copy-pasted across five methods. Adding a new rule requires touching seven places.

**Process:**
- Classify: Transaction Script sprawl — the complexity has exceeded the pattern's capacity.
- Route: Refactor toward Domain Model. Direction: up, not down.
- Service Layer: Keep `BillingService` as an Operation Script service layer; move business rules onto `Contract`, `LineItem`, and `Discount` domain objects.
- Migration path: Extract duplicate validation into domain object methods first; introduce `Data Mapper` to decouple persistence; migrate rule-specific conditional branches into strategy classes.
- Anti-pattern check: Do not introduce an anemic domain model by moving methods from `BillingService` to new classes that only hold data. Behavior must move too.

**Output:** Decision record documenting the refactor direction, a domain object skeleton (`Contract`, `LineItem`, `Discount`), `BillingService` reduced to coordinating transactions and notifications, and a Data Mapper recommendation for persistence.

## References

- `references/complexity-vs-effort-graph.md` — Fowler's unquantified-but-instructive chart described textually with decision thresholds
- `references/revenue-recognition-four-ways.md` — the three-table schema (products / contracts / revenueRecognitions) implemented as Transaction Script (Java), Domain Model (Java), Table Module (C#), and Service Layer (Java)
- `references/service-layer-thickness-guide.md` — detailed comparison of domain facade, operation script, and controller-entity with code sketches

If unclear which data-source pattern to pair with the chosen domain pattern → invoke `data-source-pattern-selector`. If unclear whether a distribution boundary (Remote Facade, DTO) is needed → invoke `distribution-boundary-designer`. If unsure which overall layering approach fits the application → invoke `enterprise-architecture-pattern-stack-selector`.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler et al. (Addison-Wesley, 2002).

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-enterprise-architecture-pattern-stack-selector`
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-distribution-boundary-designer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
