---
name: microservice-granularity-optimizer
description: >
  Right-size microservice boundaries using granularity disintegrators (forces to split: service scope, code volatility, scalability, fault tolerance, security, extensibility) and integrators (forces to combine: database transactions, workflow/choreography coupling, shared code, data relationships). Includes choreography vs orchestration selection and the saga pattern for distributed transactions. Use this skill whenever the user is splitting a monolith into microservices, deciding how fine-grained services should be, experiencing too many inter-service calls or latency from over-splitting, dealing with distributed transaction problems across microservices, choosing between choreography and orchestration for service communication, implementing the saga pattern, debugging a distributed monolith, or evaluating whether services should be merged or split further -- even if they don't use the exact phrase "microservice granularity."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/microservice-granularity-optimizer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - component-identifier
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [17]
tags: [software-architecture, architecture, microservices, granularity, bounded-context, disintegrators, integrators, choreography, orchestration, saga, distributed-transactions]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: none
      description: "System description with current or proposed service boundaries, inter-service communication patterns, and transaction requirements -- the skill guides the granularity optimization process"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can analyze current service structure."
---

# Microservice Granularity Optimizer

## When to Use

You need to determine the right size for microservice boundaries, evaluate whether existing services should be split or merged, or select communication patterns (choreography vs orchestration) for inter-service coordination. The most common mistake in microservices is making services too small -- as Martin Fowler noted, "microservice" is a label, not a description. Typical situations:

- Splitting a monolith -- "we want to decompose into microservices, but how small should each service be?"
- Over-splitting diagnosis -- "we split too fine and now every request requires 5+ inter-service calls"
- Distributed transaction pain -- "we need atomic operations across services but SAGA is killing us"
- Communication design -- "should our services use choreography or orchestration?"
- Granularity evaluation -- "we have 30 microservices for a system that could be 8 -- did we over-decompose?"
- Merge vs split decision -- "these two services always change together and share data -- should we merge them?"

Before starting, verify:
- Has microservices been confirmed as the architecture style? If the user hasn't decided yet, consider using `architecture-style-selector` first.
- Are components identified? If not, use `component-identifier` to establish initial service candidates.
- If the user has existing microservices and is troubleshooting granularity, proceed directly.

## Context & Input Gathering

### Input Sufficiency Check

This skill optimizes microservice granularity. You can proceed with partial information, but certain inputs directly determine the quality of the recommendation.

### Required Context (must have -- ask if missing)

- **Current or proposed service boundaries:** What services exist (or are planned) and what does each one do?
  -> Check prompt for: service names, service responsibilities, API descriptions, domain descriptions
  -> If missing, ask: "What are your current (or proposed) microservices and what does each one handle?"

- **Inter-service communication pain points:** Which services call each other frequently? Where is latency or complexity highest?
  -> Check prompt for: mentions of "too many calls," latency, coupling, distributed transactions, data consistency
  -> If missing, ask: "Which services communicate with each other most frequently, and are there pain points (latency, failed transactions, tight coupling)?"

### Important Context (strongly recommended -- ask if easy to obtain)

- **Transaction requirements:** Which operations must be atomic across service boundaries?
  -> Check prompt for: ACID mentions, consistency requirements, "must be atomic" language, order/payment/inventory workflows
  -> If missing, ask: "Are there business operations that need to be all-or-nothing across multiple services? For example, does placing an order need to atomically update inventory and charge payment?"

- **Scalability differences:** Do different parts of the system need to scale independently?
  -> Check prompt for: traffic patterns, peak load descriptions, "X gets 100x more traffic than Y"
  -> If missing and relevant, ask: "Do any parts of your system need to scale independently? For example, does search need to handle 100x more traffic than checkout?"

### Observable Context (gather from environment)

- **Existing service structure:** If a codebase exists, scan for service boundaries
  -> Look for: Docker/Kubernetes configs, API gateway routes, service directories, inter-service client libraries
  -> Reveals: actual granularity, communication patterns, shared dependencies

### Default Assumptions

- If communication pattern unknown -> assume choreography-first (aligns with microservices philosophy)
- If transaction requirements unknown -> assume most operations are eventually consistent, flag any that look like they need atomicity
- If team size unknown -> assume moderate (can handle 5-15 services)

### Sufficiency Threshold

```
SUFFICIENT: service boundaries (current or proposed) + communication pain points + transaction requirements are known
PROCEED WITH DEFAULTS: service boundaries are known, pain points and transactions unclear
MUST ASK: service boundaries are missing entirely
```

## Process

### Step 1: Map Current Service Boundaries

**ACTION:** Document each service's scope, responsibilities, and data ownership.

**WHY:** You cannot optimize granularity without understanding the current state. Each microservice should model a bounded context -- a domain or workflow that includes everything necessary to operate: classes, subcomponents, and database schemas. The bounded context concept from domain-driven design is the philosophical foundation of microservices. Services that share databases, classes, or schemas are not truly bounded and will suffer from coupling that defeats the purpose of microservices.

**For each service, document:**
1. Name and domain purpose
2. Key entities and data it owns
3. Which other services it calls (and why)
4. Which other services call it (and why)
5. Database(s) it uses -- shared or dedicated

**IF** services share a database -> flag as coupling risk (violates data isolation principle)
**IF** multiple services need the same entity class (e.g., Address) -> this is expected; microservices prefer duplication over coupling

### Step 2: Apply Granularity Disintegrators

**ACTION:** Evaluate each service against the six disintegrator forces. Each force that applies pushes toward splitting the service into smaller ones.

**WHY:** Disintegrators are the forces that justify making services smaller. Without a structured evaluation, architects split services based on gut feeling, which usually leads to either over-splitting (too many tiny services) or under-splitting (hidden monolith). Each disintegrator has a specific, testable reason for splitting -- if none apply, the service is the right size.

**The six disintegrators:**

1. **Service scope and function** -- Is the service doing too many unrelated things?
   -> Test: Can you describe the service's purpose in one sentence without using "and"?
   -> If the service handles "order management AND inventory tracking AND shipping," it may be doing too much.
   -> Split when: the service contains multiple distinct business domains that could operate independently.

2. **Code volatility** -- Do different parts of the service change at very different rates?
   -> Test: Over the last 6 months, did some components change weekly while others haven't changed in months?
   -> Split when: a frequently-changing component is locked into a service with stable components, forcing unnecessary redeployments.

3. **Scalability** -- Do different parts need different scaling profiles?
   -> Test: Does one component need 10 instances while another needs only 1?
   -> Split when: scaling the service up also scales components that don't need it, wasting resources.

4. **Fault tolerance** -- Should a failure in one part NOT bring down another part?
   -> Test: If the recommendation engine fails, should order processing still work?
   -> Split when: a non-critical component's failure takes down a critical component.

5. **Security** -- Do different parts require different security levels or access controls?
   -> Test: Does one component handle PCI/PII data while another handles public data?
   -> Split when: the entire service must run at the highest security level because one component requires it.

6. **Extensibility** -- Is one part of the service likely to grow in directions that don't affect the rest?
   -> Test: Are new features being added to one component while others remain stable?
   -> Split when: extension points are concentrated in one area and coupling to the rest slows development.

**Score each service:** For each disintegrator, mark whether it applies (YES/NO) with specific evidence. A service with 3+ disintegrators applying is a strong candidate for splitting.

### Step 3: Apply Granularity Integrators

**ACTION:** Evaluate whether services that seem like they should be separate actually need to stay together (or be merged).

**WHY:** Integrators are the counter-forces to disintegrators -- they are reasons NOT to split (or reasons to merge services that were split too aggressively). The most common microservices mistake is ignoring integrators: splitting services that need ACID transactions, that always change together, or that share critical code. The result is a distributed monolith -- all the complexity of microservices with none of the benefits.

**The four integrators:**

1. **Database transactions** -- Do these services need ACID transactions between them?
   -> Test: Must operations across these services be all-or-nothing? If payment fails, must the order be rolled back atomically?
   -> Merge when: you find yourself building SAGA patterns for operations that were trivial database transactions before splitting. The best advice for distributed transactions is: DON'T. Fix the granularity instead.
   -> **Critical rule:** "Don't do transactions in microservices -- fix granularity instead!" Transaction boundaries are one of the strongest indicators of incorrect granularity.

2. **Workflow and choreography** -- Do these services require extensive back-and-forth communication?
   -> Test: Does completing one business operation require 4+ synchronous calls between services?
   -> Merge when: the inter-service communication overhead exceeds the benefit of separation. If Service A cannot do anything useful without calling Service B, they may belong together.

3. **Shared code** -- Do these services share significant business logic (not just utilities)?
   -> Test: Is the same business rule implemented in multiple services? When the rule changes, do multiple services need updating?
   -> Merge when: shared code represents shared business logic that changes together. (Shared infrastructure code like logging is fine to duplicate -- it's shared domain logic that indicates coupling.)

4. **Data relationships** -- Do these services constantly need each other's data?
   -> Test: Does Service A frequently query Service B just to get reference data it needs for every operation?
   -> Merge when: the data dependency is so frequent that every request to A triggers a call to B, effectively creating a runtime monolith.

**For each pair of closely-related services:** Evaluate all four integrators. If 2+ integrators apply strongly, the services should likely be merged.

### Step 4: Resolve Conflicts and Decide

**ACTION:** When disintegrators say "split" but integrators say "keep together," make a judgment call based on the trade-offs.

**WHY:** Almost every granularity decision involves tension between splitting forces and combining forces. There is no formula -- this is where architectural judgment matters. The key insight is that integrators generally win over disintegrators when they apply, because the cost of fighting integrators (distributed transactions, excessive communication, duplicated business logic) is usually higher than the cost of a slightly-too-large service.

**Decision framework:**
- **Strong disintegrators + weak integrators** -> Split the service
- **Weak disintegrators + strong integrators** -> Keep together (or merge)
- **Strong disintegrators + strong integrators** -> This is the hard case. Consider:
  - Can the transaction boundary be redesigned to avoid the ACID need?
  - Can an event-driven approach replace synchronous coupling?
  - Would the saga pattern be acceptable for this specific workflow?
  - Is the operational cost of SAGA worth the deployment/scaling independence?

**IF** transaction integrator is the blocker -> strongly favor keeping services together. Distributed transactions are the #1 source of microservices complexity.
**IF** choreography integrator is the blocker -> consider whether orchestration could reduce the coupling enough to justify the split.

### Step 5: Select Communication Pattern

**ACTION:** For each inter-service communication path, choose between choreography and orchestration.

**WHY:** Choreography (broker-style, no central coordinator) and orchestration (mediator-style, central coordinator) represent fundamentally different trade-offs. Choreography preserves the decoupled philosophy of microservices and is the natural default. Orchestration creates coupling but simplifies complex multi-step workflows. The choice directly affects how well the architecture handles errors, maintains decoupling, and manages workflow complexity.

**Choreography (default for microservices):**
- Each service calls other services as needed, no central coordinator
- Resembles the broker pattern in event-driven architecture
- Preserves bounded context philosophy -- each service is autonomous
- Trade-off: error handling and coordination are distributed across services
- Best for: simple workflows, high decoupling needs, services that can operate independently
- Risk: complex workflows become "front controller" patterns where one service becomes an accidental mediator

**Orchestration:**
- A dedicated mediator service coordinates the workflow across other services
- Creates coupling through the mediator, but centralizes coordination logic
- Trade-off: coupling through mediator vs. distributed complexity without one
- Best for: complex multi-step business processes (e.g., "place order" involving payment, inventory, shipping)
- Risk: mediator becomes a bottleneck or single point of failure

**Decision criteria:**

| Factor | Choreography | Orchestration |
|--------|:---:|:---:|
| Workflow complexity | Simple (2-3 services) | Complex (4+ services) |
| Error handling | Distributed, each service handles its own | Centralized in mediator |
| Decoupling | Maximum | Moderate (mediator creates coupling) |
| Visibility | Low (tracing across services needed) | High (mediator has full view) |
| Performance | Fewer bottlenecks | Mediator can bottleneck |
| Domain isomorphism | Natural fit for microservices | Better for structured workflows |

### Step 6: Design Saga Pattern (if needed)

**ACTION:** For any remaining cross-service transactions that cannot be eliminated by adjusting granularity, design the saga (compensating transaction) pattern.

**WHY:** Even with optimal granularity, some distributed transactions are unavoidable -- for example, when two services genuinely need different architecture characteristics (one needs extreme scalability, the other needs strict security isolation) yet must participate in a business transaction. The saga pattern coordinates these transactions through a do/undo mechanism: each service operation has a compensating "undo" operation. A mediator service tracks the transaction state and triggers compensating actions if any step fails. This is significantly more complex than ACID transactions and should be used sparingly.

**For each saga:**
1. List the participating services and their operations
2. Define the "do" operation for each service
3. Define the "undo" (compensating) operation for each service
4. Choose: choreographed saga (each service triggers the next) or orchestrated saga (mediator coordinates)
5. Define the pending state management (how do you track which steps completed?)
6. Define error handling: what happens if the undo operation itself fails?

**Critical warnings:**
- A few transactions across services is sometimes necessary; if it's the dominant feature of the architecture, mistakes were made
- If you find yourself designing SAGAs for most of your workflows, your services are too granular -- go back to Step 2-4 and merge services
- The undo operations are often significantly more complex than the do operations
- Asynchronous SAGAs with contingent requests create race conditions that are extremely difficult to debug

### Step 7: Validate and Score

**ACTION:** Validate the final granularity against microservices architecture characteristic ratings and check for anti-patterns.

**WHY:** Every architecture style has known strengths and weaknesses. Validating against the ratings ensures you are leveraging the architecture's strengths (scalability, elasticity, evolutionary, modularity) and not fighting its weaknesses (performance, cost, simplicity). Checking for anti-patterns catches the most common design mistakes.

**Microservices architecture ratings:**

| Characteristic | Rating | Notes |
|---------------|:------:|-------|
| Deployability | 4 | Small, independent deployment units |
| Elasticity | 5 | Fine-grained scaling per service |
| Evolutionary | 5 | High decoupling enables incremental change |
| Fault tolerance | 4 | Independent services fail independently |
| Modularity | 5 | Each service is a bounded context |
| Overall cost | 1 | Expensive: infrastructure, orchestration, monitoring |
| Performance | 2 | Network calls replace method calls |
| Reliability | 4 | Redundancy via service discovery |
| Scalability | 5 | Each service scales independently |
| Simplicity | 1 | Most complex distributed architecture |
| Testability | 4 | Small test scope per service |

**Anti-pattern checks:**
- **Distributed monolith:** Services share databases, deploy together, or can't function independently. You have all the complexity of microservices with none of the benefits.
- **Over-granular services:** Every API call requires 3+ inter-service hops. Latency is unacceptable. Most workflows need SAGAs. Services can't do anything useful alone.
- **Entity trap:** Services modeled after database entities (UserService, OrderService, ProductService) rather than business capabilities/workflows.
- **Shared database:** Multiple services read/write the same database tables, creating hidden coupling through schema changes.
- **Front controller:** One "choreographed" service has become an accidental orchestrator, handling coordination for most workflows while also maintaining its own domain logic.
- **Transaction spaghetti:** More than 30% of workflows require SAGA patterns -- indicates granularity is wrong.

## Inputs

- Current or proposed service boundaries with responsibilities
- Inter-service communication patterns and pain points
- Transaction requirements (which operations must be atomic)
- Scalability and fault tolerance differences between services
- Existing codebase structure (if migrating from monolith)

## Outputs

### Granularity Optimization Report

```markdown
# Microservice Granularity Report: {System Name}

## Current State
**Services:** {count}
**Key pain points:** {latency, transactions, coupling, etc.}

## Disintegrator/Integrator Analysis

### Service: {ServiceName}
**Current scope:** {what it does}

| Disintegrator | Applies? | Evidence |
|--------------|:--------:|----------|
| Service scope/function | {Y/N} | {evidence} |
| Code volatility | {Y/N} | {evidence} |
| Scalability | {Y/N} | {evidence} |
| Fault tolerance | {Y/N} | {evidence} |
| Security | {Y/N} | {evidence} |
| Extensibility | {Y/N} | {evidence} |
| **Disintegrator score** | **{count}/6** | |

### Service Pair: {ServiceA} + {ServiceB}

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | {Y/N} | {evidence} |
| Workflow coupling | {Y/N} | {evidence} |
| Shared code | {Y/N} | {evidence} |
| Data relationships | {Y/N} | {evidence} |
| **Integrator score** | **{count}/4** | |

**Decision:** {split / merge / keep as-is}
**Reasoning:** {why}

## Recommended Service Boundaries

| # | Service | Domain | Owns Data | Scales to |
|---|---------|--------|-----------|:---------:|
| 1 | {name} | {domain} | {entities} | {instances} |

## Communication Design

| Workflow | Services involved | Pattern | Reasoning |
|----------|------------------|---------|-----------|
| {workflow} | {services} | Choreography / Orchestration | {why} |

## Saga Patterns (if any)

### Saga: {WorkflowName}
| Step | Service | Do operation | Undo operation |
|:----:|---------|-------------|----------------|
| 1 | {service} | {do} | {undo} |
| 2 | {service} | {do} | {undo} |
**Coordination:** {choreographed / orchestrated}
**Pending state:** {how tracked}

## Anti-Pattern Check
- [ ] No shared databases between services
- [ ] No distributed monolith (services deploy independently)
- [ ] Not over-granular (<30% of workflows need SAGA)
- [ ] No entity trap (services model workflows, not entities)
- [ ] No accidental front controllers
- [ ] Each service can function with limited degradation if others fail

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | {Yes/No} |
| Elasticity | 5 | {Yes/No} |
| ... | ... | ... |
```

## Key Principles

- **"Microservice" is a label, not a description** -- The originators chose the name to contrast with "gigantic services" (SOA), not to prescribe size. Many developers treat "micro" as a commandment and create services that are too fine-grained. The purpose of service boundaries is to capture a domain or workflow, and those boundaries might be large for some parts of the system.

- **Don't do transactions in microservices -- fix granularity instead** -- This is the single most important guideline. Architects who build microservices and then find themselves wiring transactions across service boundaries have almost certainly made their services too granular. Transaction boundaries are one of the strongest indicators of incorrect granularity. Merge the services that transact together.

- **Bounded context is the architectural unit** -- Each microservice should model a complete bounded context: its own classes, subcomponents, and database schemas. Nothing is shared with other services. Duplication (e.g., an Address class in multiple services) is preferred over coupling. This is the opposite of traditional enterprise thinking where reuse was paramount.

- **Data isolation is non-negotiable** -- Each service must own its data exclusively. No shared databases, no shared schemas, no shared tables. When services need each other's data, they communicate through well-defined APIs or events, never through direct database access. Shared databases are integration points that create hidden coupling.

- **Choreography is the natural default** -- Because microservices favors decoupling, choreography (no central coordinator) is the natural fit. Orchestration should only be introduced for complex multi-step workflows where distributed error handling would be too complex. Even then, the orchestrator should be a thin coordination service, not a place for business logic.

- **Integrators generally win over disintegrators** -- When splitting forces conflict with combining forces, the combining forces usually carry more weight. The cost of fighting integrators (SAGA complexity, excessive communication, duplicated business logic) almost always exceeds the cost of a slightly-too-large service.

- **Iterate on granularity** -- Architects rarely discover the correct granularity, data dependencies, and communication styles on their first pass. Expect to iterate. Start with slightly larger services and split only when a specific disintegrator provides clear justification.

## Examples

**Scenario: Over-split order processing system**
Trigger: "We split our Order service into OrderCreation, OrderValidation, OrderPricing, OrderFulfillment, and OrderNotification. Now placing a single order requires 5 synchronous calls in sequence, latency tripled, and we need distributed transactions between OrderCreation and OrderPricing. How do we fix this?"
Process: Applied disintegrator analysis to each sub-service. Only OrderNotification had independent scalability needs (disintegrator: scalability). All others shared the same code volatility, security level, and fault tolerance requirements. Applied integrator analysis: OrderCreation + OrderPricing had strong database transaction integrator (pricing must be atomic with order creation). OrderCreation + OrderValidation + OrderFulfillment had strong workflow coupling integrator (always called in sequence, never independently). Recommendation: merge OrderCreation, OrderValidation, OrderPricing, and OrderFulfillment back into a single OrderService. Keep OrderNotification separate (different scalability profile, can be async, fault tolerant to delays).
Output: **Reduced from 5 services to 2 (OrderService + NotificationService).** Eliminated 4 synchronous inter-service calls per order. Eliminated distributed transaction between creation and pricing (now a single ACID transaction). OrderNotification communicates via async events (choreography). Latency dropped by ~60%.

**Scenario: Monolith decomposition with mixed granularity needs**
Trigger: "We have a monolithic e-commerce application. We want to move to microservices. The system handles: product catalog, search, user accounts, shopping cart, order processing, payment, inventory management, shipping, reviews, and analytics."
Process: Applied disintegrators systematically. Product Catalog and Search have different scalability needs (search gets 100x more traffic) -- split. Payment has unique security requirements (PCI compliance) -- split. Analytics has different code volatility (changes daily vs monthly for core) -- split. Reviews and Ratings are extensible independently -- split. Applied integrators: Order Processing + Payment have a strong transaction integrator (payment must be atomic with order), but the security disintegrator for Payment is stronger -- keep separate, use orchestrated saga. Shopping Cart + Order Processing have weak integrator (cart is pre-order, separate lifecycle). Inventory + Shipping have moderate data relationship integrator but different scalability needs.
Output: **8 services:** ProductCatalog, Search, UserAccounts, ShoppingCart, OrderProcessing, Payment, InventoryShipping (merged due to data integrator), ReviewsRatings, Analytics. One saga pattern for Order-Payment. Choreography for most communication; orchestration for the order placement workflow (OrderProcessing orchestrates Payment and InventoryShipping).

**Scenario: Distributed transaction redesign**
Trigger: "We're designing a new e-commerce platform with microservices. When a customer places an order, we need to: reserve inventory, charge payment, and create a shipment. If payment fails after inventory is reserved, we need to release it. How do we handle this?"
Process: First evaluated whether these truly need to be separate services (integrator analysis). Inventory and Shipping have different scalability needs (inventory checks happen at browse-time too, not just checkout). Payment has PCI security isolation requirements. These disintegrators justify keeping them separate despite the transaction integrator. Designed an orchestrated saga: OrderService acts as the saga mediator. Step 1: Reserve inventory (do: reserve, undo: release). Step 2: Charge payment (do: charge, undo: refund). Step 3: Create shipment (do: create, undo: cancel). If Step 2 fails, OrderService calls inventory.release(). Each service enters "pending" state until the saga completes. Chose orchestration over choreography because the error handling for compensating transactions is too complex to distribute.
Output: **Orchestrated saga with 3 participants.** OrderService mediates. Each service implements do/undo operations. Pending state tracked in OrderService database. Explicit error handling: if undo itself fails, alert + manual resolution queue. Warning noted: if more than ~30% of workflows need sagas, the granularity should be reconsidered.

## References

- For detailed disintegrator/integrator decision matrices and trade-off tables, see [references/disintegrators-integrators.md](references/disintegrators-integrators.md)
- For identifying initial service candidates, use `component-identifier`
- For choosing between microservices and service-based architecture, use `architecture-style-selector`
- For documenting granularity decisions, use `architecture-decision-record-creator`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-component-identifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
