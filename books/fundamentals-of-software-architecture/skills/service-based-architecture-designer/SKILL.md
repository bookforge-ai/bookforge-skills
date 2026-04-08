---
name: service-based-architecture-designer
description: Design a service-based architecture with 4-12 coarse-grained domain services, including service decomposition, database partitioning strategy (shared vs domain-partitioned vs per-service), API layer design, and ACID vs BASE transaction decisions. Use this skill whenever the user is designing a service-based system, decomposing a monolith into coarse-grained services, deciding how many services to create, choosing a database topology for distributed services, deciding between shared database and per-service databases, evaluating whether to add an API layer, determining ACID vs eventual consistency needs, or comparing service-based architecture against microservices — even if they don't use the exact phrase "service-based architecture."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/service-based-architecture-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - architecture-characteristics-identifier
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [13]
tags: [software-architecture, architecture, service-based, distributed, domain-services, database-partitioning, ACID, coarse-grained]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "System description, domain requirements, team context, and data consistency needs — the skill guides the entire service-based architecture design process"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can analyze current architecture."
---

# Service-Based Architecture Designer

## When to Use

You need to design a service-based architecture or evaluate whether service-based is the right distributed style for a system. Service-based architecture is a hybrid of microservices — it uses coarse-grained domain services (typically 4-12, averaging ~7) rather than fine-grained single-purpose services. It is considered the most pragmatic distributed architecture style. Typical situations:

- New distributed system — "we need something beyond a monolith but microservices feels like overkill"
- Monolith decomposition — "our deployments take hours and we want independent deployability"
- Architecture comparison — "should we use service-based or microservices?"
- Database topology — "should our services share a database or have separate ones?"
- Transaction design — "we need ACID transactions across some of these workflows"

Before starting, verify:
- Has an architecture style already been selected? If the user hasn't decided on service-based yet, consider using `architecture-style-selector` first.
- Are driving architecture characteristics known? If not, use `architecture-characteristics-identifier` — you need to know what quality attributes drive the design.
- If the user explicitly asks for service-based design, proceed directly.

## Context & Input Gathering

### Input Sufficiency Check

This skill designs a complete service-based architecture. You can proceed with partial information and fill gaps during the process, but certain inputs directly determine the quality of the architecture.

### Required Context (must have — ask if missing)

- **System purpose and domain:** What business capabilities does this system provide?
  -> Check prompt for: domain description, list of features/modules, business workflows
  -> If missing, ask: "What does your system do? What are the main business capabilities or modules?"

- **Business workflows that cross domain boundaries:** Which operations span multiple domains?
  -> Check prompt for: transaction descriptions, workflow dependencies, mentions of "X needs to update Y"
  -> If missing, ask: "Which business operations need to coordinate across multiple areas? For example, does placing an order also need to update inventory and billing atomically?"

### Important Context (strongly recommended — ask if easy to obtain)

- **Team size and distributed experience:** How many developers? Have they built distributed systems before?
  -> Check prompt for: team mentions, experience level, current architecture
  -> If missing, ask: "How large is your development team, and have they built distributed systems before?"

- **Current deployment pain:** What deployment problems are you trying to solve?
  -> Check prompt for: deployment frequency, deployment duration, risk mentions
  -> If missing and relevant, ask: "How long do deployments take and how often do you deploy?"

- **Data consistency requirements:** Which operations require strict transactional guarantees?
  -> Check prompt for: ACID mentions, consistency requirements, "must be atomic" language
  -> If missing, ask: "Which operations require strict transactional consistency (all-or-nothing), and which can tolerate eventual consistency?"

### Observable Context (gather from environment)

- **Existing architecture:** If refactoring, scan for current structure
  -> Look for: package structure, module boundaries, database schemas, existing service definitions
  -> Reveals: natural domain boundaries, current coupling patterns

### Default Assumptions

- If team experience unknown -> assume moderate (can handle service-based but not full microservices)
- If database strategy not specified -> default to shared database (the most common and simplest starting point)
- If service count not specified -> target ~7 services (the average for service-based)
- If API layer not discussed -> recommend adding one if external consumers exist

### Sufficiency Threshold

```
SUFFICIENT: system purpose + business capabilities + cross-domain workflows are known
PROCEED WITH DEFAULTS: system purpose + capabilities are known, cross-domain workflows unclear
MUST ASK: system purpose OR business capabilities are missing
```

## Process

### Step 1: Identify Domain Services

**ACTION:** Decompose the system into 4-12 coarse-grained domain services based on business capabilities.

**WHY:** Service-based architecture uses "domain services" — coarse-grained portions of an application that encapsulate an entire business domain (like OrderService, PaymentService), NOT fine-grained single-purpose services (like OrderPlacement, OrderValidation). The coarse granularity is the defining characteristic that differentiates service-based from microservices, and it is what preserves ACID transactions and simplifies orchestration. Each domain service internally orchestrates its own sub-operations through class-level calls rather than remote service calls.

**Process:**
1. List all business capabilities the system must support
2. Group related capabilities into cohesive domains (aim for 4-12 groups, ~7 average)
3. Each group becomes a domain service — name it after the domain, not the technical function
4. Verify each service is coarse enough: it should contain multiple related sub-operations, not just one

**Granularity checks:**
- **Too many services (>12):** You are drifting toward microservices. Merge related services. More services = more network calls, more distributed transaction complexity, less ACID safety.
- **Too few services (<3):** You haven't decomposed enough. The benefits of independent deployability and fault isolation are negligible with 2-3 services.
- **Right size (4-12):** Each service represents a complete business domain with multiple internal components.

**IF** a service only does one thing -> merge it with a related service
**IF** a service does unrelated things -> split it into separate domain services

### Step 2: Design Internal Service Structure

**ACTION:** Define the internal architecture of each domain service.

**WHY:** Each domain service is itself a mini-application with its own internal structure. Two design approaches exist: layered (technical partitioning with API facade, business logic, persistence layers) and domain-partitioned (API facade with internal sub-domain components, similar to modular monolith). The choice affects how easily the service can evolve. Domain-partitioned internal design is preferred when the service is complex enough to warrant sub-domain separation, because it makes future decomposition easier if a service eventually needs to be split.

**For each service, define:**
1. **API facade layer:** Every domain service must have an API access facade that orchestrates business requests from the UI. This facade is responsible for receiving a single business request and breaking it into internal sub-operations.
2. **Internal structure:** Choose layered (API facade -> business logic -> persistence) for simpler services, or domain-partitioned (API facade -> sub-domain components) for complex services.
3. **Internal components:** List the key components within each service.

### Step 3: Select Database Topology

**ACTION:** Choose the database partitioning strategy for the system.

**WHY:** Database topology is the most consequential infrastructure decision in service-based architecture. A shared database preserves SQL joins and ACID transactions across all services — this is the primary structural advantage of service-based over microservices. However, a shared database creates coupling through schema changes: modifying a table can force redeployment of all services that use it. The database topology directly determines whether you get ACID transactions (shared) or must implement distributed transactions like SAGA (per-service). Choosing per-service databases prematurely eliminates the ACID advantage that makes service-based architecture attractive in the first place.

**Decision tree:**

| Strategy | When to use | Trade-offs |
|----------|------------|------------|
| **Single shared database** | Default choice. Multiple services need joins across domains. ACID transactions span service boundaries. Team is small. | Simple. Preserves ACID. But: schema changes can impact all services. Mitigate with logical partitioning. |
| **Logically partitioned (shared DB, domain-scoped schemas)** | Want shared DB benefits but need to control schema change impact. Multiple services exist. | Best of both worlds. Services own their logical partition. Federated shared libraries match partitions. Common tables still need coordination. |
| **Domain-partitioned databases** | 2-3 domain groups have clearly separate data with no cross-domain joins needed. | Partial isolation. Some services share a DB, others are separate. Moderate complexity. |
| **Per-service databases** | Each service's data is truly independent. No cross-service joins needed. Team is ready for eventual consistency. | Maximum isolation. But: lose ACID across services. Need SAGA pattern for distributed transactions. Avoid unless necessary. |

**IF** shared database -> implement logical partitioning through federated shared libraries (one entity library per logical domain + one common library)
**IF** per-service databases -> document which workflows now require distributed transactions and plan SAGA implementation

**Critical rule:** Make the logical partitioning in the database as fine-grained as possible while still maintaining well-defined data domains to better control database changes within a service-based architecture.

### Step 4: Determine UI Topology

**ACTION:** Select the user interface deployment strategy.

**WHY:** Service-based architecture supports three UI variants, and the choice affects the number of architecture quanta (independently deployable units with distinct characteristics). A single monolithic UI means the entire frontend shares one deployment and one set of architecture characteristics. Domain-based or service-based UIs enable independent frontend deployments, which matters when different parts of the application face different user groups with different availability, scalability, or security needs.

**Options:**

| UI Topology | When to use | Quanta impact |
|------------|------------|---------------|
| **Single monolithic UI** | One user group, simple frontend, single deployment pipeline | All services + UI = 1 quantum (if shared DB) |
| **Domain-based UIs** | Different user groups (e.g., customer-facing vs internal operations) | Multiple quanta possible — each UI + its services can be a separate quantum |
| **Service-based UIs** | Maximum frontend independence, micro-frontend approach | Multiple quanta — each UI is coupled only to its service |

### Step 5: Decide on API Layer

**ACTION:** Determine whether to add an API layer (reverse proxy or gateway) between the UI and services.

**WHY:** An API layer is optional in service-based architecture but valuable in specific scenarios. Without an API layer, the UI accesses services directly using a service locator pattern, API gateway, or proxy embedded in the UI. Adding a separate API layer creates a centralized place for cross-cutting concerns (security, metrics, auditing, rate limiting, service discovery) and is particularly important when exposing services to external consumers. However, it adds another deployment unit, network hop, and potential single point of failure.

**Add an API layer when:**
- External systems or third parties will consume the services
- You need centralized security, auditing, or rate limiting
- Service discovery is needed (services move across infrastructure)
- Cross-cutting concerns are duplicated across the UI and multiple services

**Skip the API layer when:**
- Only internal UIs consume the services
- The team is small and wants to minimize deployment units
- Cross-cutting concerns are handled within each service

### Step 6: Map Transaction Boundaries

**ACTION:** For each cross-domain workflow, determine whether ACID or BASE transactions are needed, and ensure the database topology supports them.

**WHY:** This is where service-based architecture's core advantage materializes. Because services are coarse-grained and typically share a database, most business operations that span sub-operations (like "place order + apply payment + update inventory") happen WITHIN a single domain service using regular ACID database transactions. In microservices, this same operation would span 3 separate services requiring distributed transactions (SAGA pattern), compensating transactions, and eventual consistency. The moment you split services too fine or split the database too aggressively, you lose this advantage and must deal with all the distributed transaction complexity that service-based architecture was designed to avoid.

**For each cross-domain workflow:**
1. List the domains involved
2. If all domains are within ONE service -> ACID transaction (simple, preferred)
3. If domains span MULTIPLE services with SHARED database -> ACID transaction still possible via shared DB
4. If domains span services with SEPARATE databases -> BASE transaction required (SAGA pattern needed)

**IF** many workflows require cross-service ACID transactions -> reconsider service boundaries. Services that frequently transact together may belong in the same domain service.
**IF** BASE transactions are unavoidable -> document the SAGA choreography/orchestration and compensating actions for each workflow.

### Step 7: Validate and Score

**ACTION:** Validate the design against service-based architecture characteristic ratings and check for anti-patterns.

**WHY:** Every architecture style has known strengths and weaknesses. Service-based architecture has no five-star ratings but achieves four stars in many vital areas. Validating against the ratings ensures you are not expecting the architecture to excel where it structurally cannot (like extreme elasticity at 2 stars), and checking for anti-patterns catches the most common design mistakes before they become entrenched.

**Service-based architecture ratings:**

| Characteristic | Rating | Notes |
|---------------|:------:|-------|
| Deployability | 4 | Independent service deployment without full system release |
| Elasticity | 2 | Coarse services replicate more functionality than needed to scale |
| Evolutionary | 3 | Good domain isolation, moderate coupling through shared DB |
| Fault tolerance | 4 | One service failing does not take down others |
| Modularity | 4 | Domain-partitioned, changes scoped to single service |
| Overall cost | 4 | Much cheaper than microservices, event-driven, or space-based |
| Performance | 3 | Fewer network calls than microservices, but still distributed |
| Reliability | 4 | Less network traffic, fewer distributed transactions |
| Scalability | 3 | Can scale individual services, but coarse granularity limits efficiency |
| Simplicity | 3 | Simpler than other distributed styles, but still distributed |
| Testability | 4 | Smaller test scope per service than monolith |

**Anti-pattern checks:**
- **Too many services (>12):** You have drifted into microservices territory without the operational infrastructure to support it. Merge services.
- **Too few services (<3):** Not enough decomposition to gain independent deployability benefits. Consider whether service-based is the right style.
- **Premature database splitting:** Splitting databases without implementing SAGA creates data inconsistency risks. Keep shared DB until you have proven you don't need cross-service ACID.
- **Inter-service communication:** Domain services in service-based architecture should NOT call each other. If Service A needs to call Service B, either merge them or route through the UI/API layer. Direct inter-service calls create the coupling that service-based architecture is designed to avoid.
- **Single shared entity library:** Using one monolithic shared library for all database entity objects means a table change forces redeployment of every service. Use federated domain-scoped libraries instead.

## Inputs

- System description with business capabilities
- Business workflows, especially those crossing domain boundaries
- Team size and distributed systems experience
- Data consistency requirements (which workflows need ACID)
- Current architecture (if migrating from monolith)
- Scalability and availability requirements per domain

## Outputs

### Service-Based Architecture Design

```markdown
# Service-Based Architecture Design: {System Name}

## Design Context
**System:** {what it does}
**Team:** {size and experience}
**Key drivers:** {why service-based was chosen}

## Domain Services ({count} services)

| # | Service | Domain | Key Components | Instances |
|---|---------|--------|---------------|:---------:|
| 1 | {ServiceName} | {domain} | {component list} | {1 or N} |
| ... | ... | ... | ... | ... |

### Service Detail: {ServiceName}
**Domain:** {what business capability this covers}
**Internal design:** {layered or domain-partitioned}
**Components:**
- {Component 1}: {responsibility}
- {Component 2}: {responsibility}

## Database Topology
**Strategy:** {shared / logically partitioned / domain-partitioned / per-service}
**Reasoning:** {why this strategy was chosen}

{If logically partitioned:}
**Logical partitions:**
| Partition | Tables | Used by services |
|-----------|--------|-----------------|
| {domain} | {tables} | {services} |
| common | {shared tables} | all services |

## User Interface Topology
**Strategy:** {single monolithic / domain-based / service-based}
**Reasoning:** {why this topology was chosen}

## API Layer
**Decision:** {include / omit}
**Reasoning:** {why}

## Transaction Boundaries

| Workflow | Domains involved | Services | Transaction type | Notes |
|----------|-----------------|----------|:----------------:|-------|
| {workflow} | {domains} | {services} | ACID / BASE | {notes} |

## Architecture Quanta
**Count:** {number}
**Reasoning:** {what determines the quantum boundaries}

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | {Yes/No} |
| Fault tolerance | 4 | {Yes/No} |
| ... | ... | ... |

## Anti-Pattern Check
- [ ] Service count in 4-12 range
- [ ] No inter-service direct calls
- [ ] Database topology supports required ACID transactions
- [ ] Federated entity libraries (not single shared library)
- [ ] No premature database splitting

## Getting Started
1. {First step}
2. {Second step}
3. {Third step}
```

## Key Principles

- **Coarse-grained is the point** — Service-based architecture uses 4-12 domain services averaging ~7, NOT dozens of fine-grained microservices. The coarse granularity is what preserves ACID transactions, simplifies orchestration (internal class calls vs remote service calls), and keeps operational cost low. If you find yourself creating more than 12 services, you are building microservices without the infrastructure to support them.

- **Shared database is a feature, not a compromise** — The shared database is what enables SQL joins and ACID transactions across domains. This is the primary structural advantage over microservices. Don't split the database unless you have a proven, specific reason. Premature database splitting eliminates the core benefit of choosing service-based architecture in the first place.

- **Services should NOT call each other** — In service-based architecture, domain services are self-contained and do not communicate with each other directly. All orchestration happens either within a single service (internal) or through the UI/API layer. If two services need to coordinate frequently, they probably belong together as one service.

- **Internal orchestration over external orchestration** — A business request like "place an order" is received by the OrderService's API facade, which internally orchestrates all sub-operations (create order, apply payment, update inventory) through class-level calls within that single service. In microservices, this same operation would require external orchestration across multiple remote services. This internal orchestration is what makes service-based simpler and more reliable.

- **Logical partitioning controls blast radius** — Even with a shared database, use federated domain-scoped entity libraries rather than a single monolithic shared library. When a table in the "invoicing" domain changes, only the invoicing entity library and the services that use it need updating — not every service in the system. This is the pragmatic middle ground between monolithic coupling and full database separation.

- **Start shared, split only when proven necessary** — Begin with a shared database and logical partitioning. Only split into separate databases when you have concrete evidence that shared schema changes are causing deployment coordination problems, AND you have a plan for distributed transactions (SAGA) for any workflows that cross the split boundary.

## Examples

**Scenario: Electronic device recycling system**
Trigger: "We process old electronics (phones, tablets). Customers get quotes online, mail devices in, we assess them, pay the customer, then recycle or resell. We also have internal reporting."
Process: Identified 7 domain services from the business flow: Quoting, Item Status, Receiving, Assessment, Accounting, Recycling, Reporting. Split UI into two quanta: customer-facing (Quoting, Item Status) and internal operations (Receiving, Assessment, Accounting, Recycling, Reporting). Used two separate databases — one for customer-facing operations (higher security, separate network zone) and one for internal operations. Only Quoting and Item Status services need to scale (customer traffic), others run as single instances.
Output: **7 domain services, 2 architecture quanta, domain-partitioned databases** (2 databases split by security boundary, not by service). Customer-facing services behind a firewall separation from internal services. ACID transactions preserved within each database boundary. Assessment service changes frequently (new device rules) but is isolated, enabling high deployability.

**Scenario: Insurance claims processing platform**
Trigger: "We need claims intake, adjudication, payment, fraud detection, and policy verification. Team of 20 developers, currently a monolith with 4-hour deployments."
Process: Identified 6 domain services: Claims Intake, Adjudication, Payment, Fraud Detection, Policy Verification, Reporting. Kept shared database because claims workflows require ACID: a claim submission must atomically create the claim record, initiate fraud check, and verify policy status. Logically partitioned the database into 6 domains + common. Added API layer because external partners (repair shops, medical providers) submit claims via API. Single monolithic UI (all internal users share the same portal). Fraud Detection needs higher throughput, so it runs multiple instances with load balancing.
Output: **6 domain services, shared logically-partitioned database, API layer included.** Key win: deployment time drops from 4 hours to ~30 minutes per service. ACID preserved for claims workflows. Federated entity libraries prevent cascading redeployments from schema changes.

**Scenario: E-learning platform**
Trigger: "Building a learning management system with course catalog, enrollment, content delivery, progress tracking, assessments, and certificates. Team of 10, first distributed system."
Process: Identified 6 domain services: Course Catalog, Enrollment, Content Delivery, Progress Tracking, Assessment, Certification. Shared database — enrollment needs ACID with progress tracking (enrolling a student must atomically create progress records). No API layer needed (internal platform only). Single UI. Default single instances per service since traffic is predictable (students access during class hours). Kept Assessment and Certification in separate services despite being related because assessment rules change frequently (high deployability need) while certification is stable.
Output: **6 domain services, single shared database with logical partitioning, no API layer.** Team's first distributed system — service-based is ideal because it's the simplest distributed style (simplicity 3, cost 4) while still gaining independent deployability (4) and fault tolerance (4). If Content Delivery later needs CDN-level scaling, it can be extracted into a separate quantum.

## References

- For topology variant details and decision matrices, see [references/topology-variants.md](references/topology-variants.md)
- For architecture style comparison (service-based vs alternatives), use `architecture-style-selector`
- For identifying driving quality attributes, use `architecture-characteristics-identifier`
- For documenting the architecture decision, use `architecture-decision-record-creator`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-characteristics-identifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
