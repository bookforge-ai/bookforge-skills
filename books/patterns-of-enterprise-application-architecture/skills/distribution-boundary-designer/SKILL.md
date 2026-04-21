---
name: distribution-boundary-designer
description: "Distribution design for enterprise systems: decide whether to distribute, where to draw the service boundary, and how to implement it with Remote Facade and Data Transfer Object (DTO). Use when deciding microservices vs monolith, evaluating process boundaries, extracting services, designing remote APIs, choosing coarse-grained API shape, preventing distribution-by-class anti-pattern, applying Fowler's First Law of Distributed Object Design, designing service extraction strategy, determining when distribution is warranted vs cargo-culting microservices, implementing Remote Facade pattern, designing DTOs independent from domain objects, choosing between gRPC vs REST vs message queue vs GraphQL for service boundary, monolith decomposition, service boundary design, remote API design, distribution strategy, when to distribute, process boundary decision, coarse-grained interface design."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/distribution-boundary-designer
metadata: {"openclaw":{"emoji":"🔀","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [7, 15]
domain: software-architecture
tags:
  - distributed-systems
  - microservices
  - api-design
  - software-architecture
  - design-patterns
  - remote-facade
  - service-boundaries
  - enterprise-architecture
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: description
      description: "System topology description: current architecture (monolith / modular monolith / cluster / microservices), motivation for distribution, team structure, deployment independence needs, scaling needs, and any security zone or vendor integration requirements."
    - type: codebase
      description: "Optional: existing codebase or architecture diagrams to identify existing remote boundaries, chatty interfaces, or domain logic in remote shells."
  tools-required:
    - Read
    - Write
  tools-optional:
    - Grep
    - Glob
  mcps-required: []
  environment: "Architecture design or refactor session. Works offline. Codebase helpful for detecting existing anti-patterns but not required — skill operates on description alone."
discovery:
  goal: "Decide whether to distribute a system (or parts of it), identify legitimate boundaries if distribution is warranted, and design Remote Facade + DTO contracts at each boundary."
  tasks:
    - "Apply the First Law filter: check each legitimate distribution reason; recommend against distributing if none apply"
    - "Identify coarse-grained boundary candidates (per subsystem, not per class)"
    - "Design Remote Facade methods as use-case-shaped coarse calls (not CRUD wrappers)"
    - "Design DTOs per interaction — independent from domain objects, shaped for client needs"
    - "Audit for anti-patterns: distribution-by-class, domain logic in facade, chatty interfaces, DTO-domain coupling"
    - "Select interface style (gRPC / REST / message queue / GraphQL) based on coupling tolerance and async needs"
    - "Produce a distribution design record"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
      - staff-engineer
    experience: intermediate
  when_to_use:
    triggers:
      - "Team considering a microservices migration or service extraction"
      - "Existing system with distribution-by-class (one remote component per domain class)"
      - "Remote API is chatty — many fine-grained calls per user interaction"
      - "Domain logic has leaked into remote service shells or API controllers"
      - "Planning a new system with multiple client types (browser, mobile, desktop) or security zones"
      - "Evaluating whether to extract a scaling hot-spot (payments, search, notifications) as a separate service"
      - "Designing DTOs or gRPC protos for a service boundary"
      - "Reviewing whether a microservices architecture is justified for the team size and scaling needs"
    prerequisites: []
    not_for:
      - "Choosing domain-logic pattern (Transaction Script vs Domain Model) — invoke domain-logic-pattern-selector"
      - "Selecting data-source patterns (ORM, Active Record, Data Mapper) — invoke data-source-pattern-selector"
      - "Concurrency control within a service — invoke offline-concurrency-strategy-selector"
      - "Systems already committed to a specific distribution topology with no flexibility"
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

# Distribution Boundary Designer

Guides you through the decision of whether to distribute a system across processes or machines, where to draw the boundary if distribution is needed, and how to implement the boundary using the Remote Facade and Data Transfer Object patterns. Grounded in Fowler's First Law of Distributed Object Design and the pattern pair that makes distribution workable when it cannot be avoided.

## When to Use

Use this skill when your team is considering breaking a monolith into services, extracting a subsystem as a remote service, reviewing whether a microservices architecture is appropriate, or designing the interface at an existing remote boundary. Also use it when an existing remote API shows signs of the distribution-by-class anti-pattern (too many fine-grained calls per operation), or when domain logic has leaked into remote shells.

Prerequisites: a description of the system's purpose, team structure, deployment needs, and any known scaling or security zone requirements. A codebase or architecture diagram is helpful for detecting existing boundary problems.

## Context & Input Gathering

Gather these before proceeding:

**Required:**
- What does the system do? What are its major subsystems?
- What is the stated motivation for distribution? ("scalability," "team independence," "vendor integration," "security zones," etc.)
- Are there currently separate deployment units? If yes, which ones and why?

**Helpful:**
- How many teams? Do different teams need to deploy independently?
- Are there subsystems with dramatically different scaling needs (e.g., search scales 100x vs catalog)?
- Are there security zone requirements (DMZ vs internal network)?
- Are there vendor package integrations that run in their own process?
- Is the codebase available? Grep for remote stubs, service clients, or proto/schema files to detect existing boundary shape.

**Defaults if not provided:**
- Assume a single team if not stated — leans toward not distributing
- Assume uniform scaling if not stated — leans toward not distributing
- Assume no security zone requirement if not stated

**Sufficiency check:** If the only stated motivation is "we want microservices," "clean architecture," or "team size," the filter step will almost certainly return "do not distribute." Be explicit about this.

## Process

### Step 1 — Apply the First Law Filter

WHY: The single most common architecture mistake is distributing a system that does not need it. Fowler names this explicitly: "Don't distribute your objects." Distribution incurs latency, partial failure, marshaling cost, and interface rigidity — costs that are paid on every call, forever. Every process boundary is a tax.

Check each of Fowler's seven legitimate distribution reasons. The system should distribute ONLY if at least one applies:

| Reason | Check |
|--------|-------|
| Different client machines (desktop vs server, browser vs app server) | Does the client run on a different physical machine? |
| Application server ↔ database process boundary | Standard; SQL is designed for this. |
| Web server and app server must be separate processes | Vendor constraint, security zone, or scaling forces? |
| Independent scaling requirements | Does a hot subsystem need to scale at a dramatically different rate? |
| External vendor / purchased package software | Does a package run in its own process with a coarse-grained interface? |
| Security zone boundary (DMZ, internal network) | Is a firewall or network zone required between subsystems? |
| Different hardware or OS requirements | Does a subsystem require specialized hardware or a different OS? |

IF none apply → **Recommend modular monolith**: keep the application in one process, divide it into packages/modules with clear interfaces. Name this explicitly. Do not proceed to boundary design.

IF one or more apply → Identify only the subsystem pairs that cross a legitimate boundary. Every other subsystem pair should remain in-process.

### Step 2 — Identify Coarse-Grained Boundaries (per subsystem, not per class)

WHY: The distribution-by-class anti-pattern (one remote component per domain class) multiplies call counts and destroys performance. A remote boundary should span a subsystem — a coherent cluster of domain classes that collaborates internally and exposes a small number of use-case-shaped operations externally.

For each legitimate boundary identified in Step 1:
- Name the subsystem on each side (e.g., "order processing" and "payment processor")
- Identify the operations that cross the boundary — framed as user-intent operations ("place order," "authorize payment"), not as CRUD methods on individual entities
- Estimate call frequency: how many times is this boundary crossed per user interaction? If more than ~5, the boundary may be too fine-grained.

Signal that a boundary is too fine-grained: "GetCustomer() then GetOrders() then GetLineItems() then GetProducts()..." — four separate calls to display a single order screen. This should be one call: `GetOrderSummary(orderId)`.

### Step 3 — Design Remote Facade Methods

WHY: A Remote Facade is a thin coordination shell — its only job is to translate coarse-grained remote calls into sequences of fine-grained domain object calls. All domain logic lives in the fine-grained domain objects, not in the facade. A facade with domain logic becomes a second domain layer that is harder to test, harder to evolve, and violates the principle that the application should be runnable entirely in-process without the remote shells.

For each boundary, design the Remote Facade:
1. **Methods are use-case-shaped**: `GetOrderSummary(orderId)`, `SubmitPaymentAuthorization(authDTO)`, not `GetOrder()`, `GetCustomer()`, `UpdateOrderStatus()`
2. **Each method does one useful unit of work**: A single remote call should accomplish a meaningful operation, not just fetch one property
3. **Facade has no conditional domain logic**: No `if (order.status == SHIPPED) applyLateCharge()` in the facade. That belongs in domain objects.
4. **Facade can have multiple methods corresponding to different client use cases**: Different screens may call different facade methods that ultimately touch the same domain objects — this is correct
5. **Facade granularity**: Prefer fewer, larger facades over many small ones. A moderate application might have one; a large application, half a dozen.
6. **Security and transactions are appropriate in the facade**: The facade is a natural boundary for access control and transaction demarcation (start transaction → call domain objects → commit). This is not domain logic.

### Step 4 — Design DTOs Per Use Case

WHY: A DTO is a data carrier designed for the wire, not for the domain. Auto-deriving DTOs from domain classes couples the wire format to the domain model — any domain refactoring forces a wire format change, which may require client updates. DTOs designed around use cases are stable because use cases change less often than domain internals.

For each Remote Facade method, design the corresponding DTO(s):
1. **Shape the DTO around what the client interaction needs** — not around the domain class structure. Collapse related objects: embed artist name in AlbumDTO rather than passing a separate ArtistDTO with a separate call.
2. **Fields are primitives, strings, dates, or nested DTOs** — no domain object references. The DTO must be serializable independently of the domain model.
3. **Use a separate Assembler** to move data between domain objects and DTOs. The assembler keeps the domain model independent of wire format.
4. **Consider separate request and response DTOs** if the shapes diverge significantly. Use a single DTO if they are similar.
5. **Err on the side of sending too much data** rather than requiring a second call: "it's better to err on the side of sending too much data than have to make multiple calls."
6. **Modern naming**: Fowler's DTO = what the J2EE community called "Value Object." Today: gRPC proto messages, JSON response schemas, GraphQL types, OpenAPI schemas, Avro records.

### Step 5 — Audit for Anti-Patterns

WHY: The three most common mistakes at distribution boundaries are predictable and detectable in advance.

Check each boundary against these anti-patterns:

| Anti-Pattern | Signal | Remedy |
|--------------|--------|--------|
| Distribution by class | One remote component per domain class; dozens of remote calls per user interaction | Consolidate to subsystem-level Remote Facades with use-case methods |
| Domain logic in Remote Facade | Conditional logic, business rules, or workflow coordination in the facade | Move logic to domain objects or a non-remote Service Layer; reduce facade to thin delegation |
| Chatty fine-grained remote interface | N calls per screen/operation where N > ~3; individual property getters exposed remotely | Redesign as coarse-grained bulk accessor / command method |
| DTO-domain coupling | DTO fields map 1:1 to domain class fields; DTO imports domain classes | Introduce Assembler; redesign DTOs around use-case needs |
| Distribution without legitimate reason | Motivation is trend, architecture taste, or "clean code" | Recommend modular monolith; document the test that should be passed before re-evaluating |

### Step 6 — Select Interface Style

WHY: The interface style determines coupling tolerance, latency profile, and async capability. Fowler's 2002 guidance was RPC vs XML/HTTP; the modern decision space is richer.

| Style | Best for | Trade-offs |
|-------|----------|------------|
| gRPC (binary, proto) | Internal service-to-service, high throughput, same-platform | Tight schema coupling; not browser-native |
| REST / JSON | External APIs, browser clients, cross-platform, public APIs | Looser coupling; HTTP overhead; no streaming by default |
| Message queue (Kafka, SQS, RabbitMQ) | Fire-and-forget, event-driven, high latency tolerance, decoupled producers/consumers | Async only; harder to test; eventual consistency |
| GraphQL | Multi-client (mobile + web) with varying field needs; avoiding over-fetch | Query complexity; N+1 risk server-side; schema governance overhead |

Fowler's principle still holds: use the simplest mechanism that works. If both sides share a platform, use gRPC or its modern equivalent. Use REST/JSON when interoperability across platforms or external access matters. Use message queues when decoupling and async throughput matter more than latency.

### Step 7 — Produce Distribution Design Record

WHY: The decision must be documented so future architects understand WHY the boundary exists and what test should be passed before adding more. Distribution decisions are expensive to reverse.

Produce a distribution design record containing:
- **Current topology**: monolith / modular monolith / partial services
- **Legitimate distribution reasons identified** (Step 1) and which subsystem pair each applies to
- **Non-distribution alternatives considered** (modular monolith, package separation)
- **Proposed boundaries**: subsystem pair, direction of calls, call frequency estimate
- **Remote Facade spec**: for each facade — class name, method signatures, WHY each method is shaped this way
- **DTO spec**: for each DTO — fields, which domain objects it aggregates, assembler location
- **Interface style selected** with rationale
- **Anti-pattern audit result**: pass / fail per anti-pattern, with remediation notes if any failed

## Inputs

- System description (purpose, subsystems, team structure, deployment needs)
- Stated motivation for distribution
- Optional: codebase, architecture diagrams, existing proto/schema files
- Optional: scaling metrics or capacity constraints

## Outputs

**Distribution Design Record** (`distribution-design-record.md`) containing:

```
# Distribution Design Record: [System Name]

## Summary Decision
[Distribute / Do Not Distribute — one sentence]

## First Law Filter Results
| Reason | Applies? | Notes |
|--------|----------|-------|
| ...    | Yes/No   | ...   |

## Recommended Topology
[Modular monolith / specific service boundaries]

## Boundaries (if distributing)
### Boundary: [Subsystem A] ↔ [Subsystem B]
- Legitimate reason: [reason from filter]
- Interface style: [gRPC / REST / queue / GraphQL]
- Remote Facade: [FacadeClass]
  - [method(params) → ReturnDTO] — [WHY this use-case shape]
- DTOs:
  - [DTOName]: fields=[...], aggregates=[domain objects], assembled by=[AssemblerClass]

## Anti-Pattern Audit
| Anti-Pattern | Result | Notes |
|--------------|--------|-------|
| Distribution by class | Pass/Fail | ... |
| Domain logic in facade | Pass/Fail | ... |
| Chatty interface | Pass/Fail | ... |
| DTO-domain coupling | Pass/Fail | ... |
| Distribution without reason | Pass/Fail | ... |

## Non-Distribution Alternatives Considered
[What modular monolith structure was evaluated and why distribution was preferred]
```

## Key Principles

**1. The First Law is a default, not a suggestion.**
Distribute only when you have a concrete, operational reason from Fowler's list. "We want microservices" is not a reason. "The payment processor must be PCI-compliant in a separate security zone" is a reason. The default is always in-process.

WHY: Remote calls are orders of magnitude slower than in-process calls. Every process boundary is a permanent tax on every call that crosses it. The cumulative cost of unjustified distribution dwarfs the cost of an in-process module boundary.

**2. Boundaries are per subsystem, not per class.**
A Remote Facade corresponds to a subsystem (a cluster of collaborating domain objects), not to an individual class. If every domain class has a remote interface, the boundary design is broken.

WHY: Each fine-grained call to a remote class pays the full inter-process latency cost. A subsystem-level facade batches those calls into one network round-trip per use case.

**3. Facades contain no domain logic — none.**
A Remote Facade is a translation layer: coarse-grained interface → fine-grained domain object calls. Any conditional logic, business rules, or workflow coordination in the facade must be moved to domain objects or a non-remote Service Layer.

WHY: A facade with domain logic becomes a hidden second domain layer. The application can no longer be tested or run in-process without the remote shell, because the logic lives there. This creates a testing and evolution trap.

**4. DTOs are designed for the interaction, not the domain.**
Each DTO is shaped around a specific client use case — what data that client needs to display or send in a single interaction. DTOs are not auto-generated mirrors of domain classes.

WHY: Domain classes change frequently as business rules evolve. DTOs change when the client interaction changes. Coupling these two change rates together means every domain refactoring potentially breaks clients across the wire.

**5. The modular monolith is always on the table.**
When a team says "we need microservices for separation of concerns," the correct counter-offer is: separate your packages/modules/bounded contexts within a single process. You get team ownership, clear interfaces, and independent evolution without network cost.

WHY: The costs of distribution (latency, partial failure, operational complexity, debugging difficulty) are real and ongoing. The benefits of a modular monolith (same testability, same team ownership, same interface discipline) are available without those costs.

**6. Send more data per call rather than fewer.**
When designing DTOs and facade methods, err toward aggregating more data in one call rather than planning a second call. Over-fetching slightly is far cheaper than a second round-trip.

WHY: Remote call latency is fixed overhead per call. Bandwidth is cheap. If a client might need the order's line items after getting the order header, include the line items in the initial DTO.

## Examples

### Example 1 — Reject Distribution for a Two-Team LOB App

**Scenario:** A 12-person engineering team across two squads is building an internal CRM. Engineering lead proposes microservices "for clean boundaries between the sales squad (contacts, deals) and the support squad (tickets, SLAs)."

**Trigger:** "Should we use microservices for our two-squad CRM?"

**Process:**
1. Apply First Law Filter:
   - Client-server divide: Yes (browser client + server). But this is the standard web-app boundary, not an argument for internal microservices.
   - Independent scaling: No — contacts/deals and tickets/SLAs have similar load profiles.
   - Different security zones: No.
   - Vendor package: No.
   - Independent deployment: "Nice to have" but not operationally required.
   - Result: No legitimate reason for internal service distribution.
2. Recommend modular monolith: define a `contacts-deals` package and a `tickets-slas` package with explicit module boundaries, shared domain types, and clear internal APIs. Each squad owns their package.
3. Note: the existing web-app boundary (browser ↔ app server) is the natural Remote Facade. A single `CRMService` facade handles screen-level operations for both squads.
4. Anti-pattern audit: distribution-by-class risk = not applicable (not distributing). Domain logic in facade = not applicable.

**Output:** Distribution Design Record stating "Do not distribute internally." Modular monolith with squad-owned packages. One Remote Facade for the browser-server boundary.

---

### Example 2 — Extract Payments as a Distributed Boundary

**Scenario:** E-commerce platform. Payments team requires PCI-DSS compliance in an isolated network zone. The search subsystem handles 50x the load of the product catalog at peak.

**Trigger:** "We need to separate payments for PCI compliance and search for scaling. How do we design those boundaries?"

**Process:**
1. Apply First Law Filter:
   - Security zone (PCI): Yes — payments must live in an isolated environment. Legitimate.
   - Independent scaling (search): Yes — 50x load differential is a real scaling reason.
   - All other subsystems: No legitimate reason.
2. Two boundaries identified: Catalog ↔ Payments, Catalog ↔ Search. Everything else (orders, inventory, user) stays in the monolith.
3. Design Payments Remote Facade (`PaymentService`):
   - `AuthorizePayment(orderId, paymentMethodDTO) → PaymentResultDTO`
   - `CapturePayment(authorizationId) → CaptureResultDTO`
   - `RefundPayment(paymentId, amount) → RefundResultDTO`
   - NOT: `GetCard()`, `UpdateCard()`, `GetAuthorization()` — these are fine-grained domain calls
4. Design DTOs: `PaymentMethodDTO` (cardToken, billingAddress, amount), `PaymentResultDTO` (authorizationId, status, errorCode). Assembled from domain card/billing objects. Not coupled to domain class structure.
5. Design Search Remote Facade (`SearchService`):
   - `SearchProducts(query, filters, pagination) → ProductSearchResultDTO`
   - `SuggestProducts(partialQuery) → SuggestionDTO[]`
6. Interface style: Payments = gRPC (internal, same platform, high reliability needed). Search = REST/JSON (browser clients query search directly; must be cross-platform).
7. Anti-pattern audit: no distribution-by-class, facades are thin, DTOs are use-case-shaped.

**Output:** Distribution Design Record with two boundaries (PCI, scaling), facade specs, DTO specs, interface styles.

---

### Example 3 — Fix Legacy Chatty Distributed Objects

**Scenario:** Legacy J2EE system from 2005. Every entity bean (Customer, Order, OrderLine, Product, Address) is a separate remote EJB. Displaying an order summary screen makes 15-20 remote calls. Performance is unacceptable.

**Trigger:** "Our EJB app is painfully slow. Each screen makes dozens of remote calls. How do we fix this?"

**Process:**
1. First Law Filter: Application server is separate from DB (legitimate). The internal EJB-to-EJB calls are the problem — distribution by class applied to the domain model.
2. Diagnosis: Classic distribution-by-class anti-pattern. The EJBs mirror the domain class structure. Every property getter is a remote call.
3. Remediation:
   - Keep domain objects as plain in-process Java objects (POJOs) — remove remote interfaces from Customer, Order, OrderLine, Product.
   - Introduce a single `OrderService` Remote Facade with use-case methods: `GetOrderSummary(orderId) → OrderSummaryDTO`, `UpdateOrderStatus(orderId, statusDTO)`.
   - `OrderSummaryDTO` aggregates order header + customer name + line items + product names in one call.
   - Assembler populates the DTO from the fine-grained domain objects.
4. Interface style: Keep as EJB session bean Remote Facade (same platform) or migrate to gRPC for modern replacement.
5. Expected result: 15-20 calls → 1-2 calls per screen interaction.

**Output:** Refactoring plan with identified chatty calls, new facade spec, DTO design, migration sequence.

## References

- [`references/distribution-reasons-checklist.md`](references/distribution-reasons-checklist.md) — Fowler's seven legitimate distribution reasons as a quick-reference filter
- [`references/remote-facade-design-guide.md`](references/remote-facade-design-guide.md) — detailed guidance on Remote Facade granularity, method design, session facade vs remote facade distinction
- [`references/dto-design-guide.md`](references/dto-design-guide.md) — DTO design patterns, assembler pattern, serialization format trade-offs, modern parallels (proto, JSON schema, GraphQL types)
- [`references/interface-style-selector.md`](references/interface-style-selector.md) — gRPC vs REST vs message queue vs GraphQL selection criteria

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-enterprise-architecture-pattern-stack-selector`
- `clawhub install bookforge-domain-logic-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
