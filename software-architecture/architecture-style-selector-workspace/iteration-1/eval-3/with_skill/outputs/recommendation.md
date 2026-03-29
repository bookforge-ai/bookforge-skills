# Architecture Style Selection: E-Commerce Platform

## Decision Context
**System:** E-commerce platform processing 50k orders/day, currently a monolith. Payment module failures cascade to the entire site during flash sales. 4-hour deployments, twice weekly.
**Driving characteristics:** (1) Fault tolerance, (2) Deployability, (3) Scalability
**Architecture quanta:** Multiple quanta. The payment module has fundamentally different quality attribute needs (high fault tolerance, high elasticity during flash sales) than the core catalog/browsing experience (high availability, moderate scalability) and the order management workflow (reliability, consistency). These components cannot share the same deployment and scaling profile — payment needs independent scaling and isolation so it stops taking down the entire site.
**Team context:** 35 developers across 4 teams. Basic CI/CD (Jenkins) and monitoring (Datadog) but no distributed tracing. Currently operating a monolith — no distributed architecture experience in production.

## Step 1: Monolith vs Distributed

**Decision:** Distributed

**Reasoning:** Multiple quanta are clearly present. The defining symptom is stated directly: the payment module brings down the entire site during flash sales. This means payment needs different fault tolerance and elasticity characteristics than the rest of the system, but the monolith forces them into a single deployment unit where one module's failure cascades everywhere. Additionally, 35 developers across 4 teams stepping on each other's code is a classic signal that the single deployment quantum has become a bottleneck for team autonomy and deployability. The 4-hour, twice-weekly deployment cycle confirms that the monolith's single quantum cannot support the deployability needs of 4 independent teams.

## Candidate Evaluation

Given the distributed decision, evaluate the four distributed styles: Service-Based, Event-Driven, Space-Based, and Microservices.

| Criterion | Service-Based | Event-Driven | Microservices |
|-----------|:---:|:---:|:---:|
| Fault tolerance (priority 1) | 4/5 | 5/5 | 4/5 |
| Deployability (priority 2) | 4/5 | 3/5 | 4/5 |
| Scalability (priority 3) | 3/5 | 5/5 | 5/5 |
| **Characteristic total** | **11** | **13** | **13** |
| Organizational fit | **Good** | **Fair** | **Poor** |
| Domain isomorphism | Yes | No | Partial |
| Anti-pattern risk | Low | Broker/mediator mismatch | Distributed monolith, too-fine-grained services |

**Space-based was eliminated early:** The load pattern (50k orders/day with flash sale spikes) is high but not at the "extreme and unpredictable" level that justifies space-based architecture's enormous cost (rated 2/5) and complexity (simplicity 1/5). Flash sale spikes like Black Friday are predictable events, not random viral surges. Space-based is over-engineering for this scenario.

### Organizational Fit Detail

**Service-Based (Good):**
- 35 developers / 4 teams maps well to 4-8 coarse-grained domain services (one or two per team)
- Team can transition from monolith incrementally — no "big bang" rewrite
- Shared database preserves ACID transactions where needed (orders, payments)
- Existing Jenkins CI/CD can be extended to handle a small number of service pipelines
- No distributed tracing needed initially (fewer inter-service calls than microservices)

**Event-Driven (Fair):**
- Scores highest on characteristics, but team has no async/event debugging experience
- Testability rated 2/5 — significant gap given current team experience
- Simplicity rated 1/5 — steep learning curve from monolith
- Would require new tooling (message broker, distributed tracing) before delivering value
- Organizational fit modifier: -2 (no async experience, no distributed tracing)

**Microservices (Poor):**
- Scores well on characteristics, but team has no distributed systems experience
- 35 developers is technically in the viable range (30+), but DevOps maturity is a prerequisite the team does not meet
- No distributed tracing, basic CI/CD — operating fine-grained microservices would produce a distributed monolith
- The most common anti-pattern: teams adopt microservices without the operational foundation, resulting in services that share a database and deploy in lockstep — the worst of both worlds
- Organizational fit modifier: -3 (immature CI/CD, no distributed tracing, no distributed experience)

### Adjusted Scores (with organizational modifiers)

| | Service-Based | Event-Driven | Microservices |
|---|:---:|:---:|:---:|
| Characteristic total | 11 | 13 | 13 |
| Organizational modifier | 0 | -2 | -3 |
| Isomorphism bonus | +1 | 0 | 0 |
| **Final score** | **12** | **11** | **10** |

## Data Architecture

**Data location:** Shared database initially, with logical partitioning by domain (separate schemas for payment, orders, catalog, user accounts). This preserves ACID transactions where needed (payment + order creation) while establishing the domain boundaries that could become physical separation later.
**Communication:** Hybrid. Synchronous (REST) for request-reply flows (browsing, checkout). Asynchronous (message queue) for payment processing and order confirmation — this is the first place to introduce async because payment isolation is the primary driver.
**Consistency model:** Mixed. ACID within each domain service (enabled by shared database). Introduce eventual consistency only where it naturally fits (inventory counts, analytics, recommendation updates).

## Recommendation

**Selected style: Service-Based Architecture**

**Why this style:**
- It directly solves the primary problem: isolating payment into its own independently deployable service prevents it from cascading failures to the rest of the site. Fault tolerance rated 4/5 — sufficient for this use case.
- It matches the organizational reality: 4 teams map naturally to 4-6 domain services (Payment, Order Management, Catalog/Search, User/Account, and optionally Promotions and Notifications). Each team owns one or two services.
- Deployability (4/5) enables teams to deploy their services independently, breaking the 4-hour monolithic deployment and eliminating the "stepping on each other's code" problem.
- The shared database preserves ACID transactions for the payment-to-order workflow, which is critical for financial correctness, without requiring eventual consistency patterns the team has never implemented.
- It is the safest migration path from a monolith — extract services incrementally rather than rewriting.

**Trade-offs accepted:**
- Scalability is limited (3/5) compared to microservices or event-driven (5/5). For 50k orders/day with periodic spikes, this is adequate. If order volume grows 10x, the architecture may need to evolve.
- Elasticity is limited (2/5). Payment service can be scaled independently (separate deployment unit), but not with the fine-grained per-function elasticity of microservices.
- Less evolutionary flexibility (3/5) than microservices (5/5) — technology diversity across services is possible but not the norm.

**Trade-offs rejected (why alternatives were not chosen):**
- **Event-Driven:** Scores highest on raw characteristics (13/15) but the team has no experience with asynchronous event flows, no distributed tracing for debugging, and the testability (2/5) and simplicity (1/5) ratings represent real operational risk. Moving from a monolith directly to event-driven architecture is a common failure pattern. The organizational fit penalty outweighs the characteristic advantage.
- **Microservices:** Also scores 13/15 on characteristics, but requires mature DevOps that this team does not have. Without distributed tracing, per-service CI/CD pipelines, and experience with distributed data management, the most likely outcome is a distributed monolith — the worst possible architecture. The book is explicit: microservices require mature DevOps as a prerequisite, not as something you learn along the way.
- **Space-Based:** Massive over-engineering. The cost (2/5) and complexity (simplicity 1/5) are not justified by the load pattern. Flash sale spikes are predictable and can be handled by scaling the payment service horizontally.

## Step 4: Anti-Pattern Check

| Anti-pattern | Risk | Mitigation |
|---|---|---|
| **Too many services** | Medium — temptation to create 15+ services | Cap at 4-8 domain services. "Service-based" means coarse-grained. If you have more services than teams, you've gone too far. |
| **Distributed monolith** | Low (shared DB helps) | Maintain clear domain boundaries in database schemas. Services should own their tables. |
| **Transactions across boundaries** | Low (shared DB preserves ACID) | Keep payment and order creation in the same transaction scope initially. Only split when you have saga/eventual consistency experience. |
| **Reuse coupling** | Medium — temptation to create shared "utility" services | Prefer code duplication over runtime coupling. Shared libraries are fine; shared services create coupling. |

## Getting Started

1. **Extract the Payment service first.** This is the highest-value extraction because it directly solves the primary pain point (cascading failures during flash sales). Define a clear API boundary between the payment domain and the rest of the system. Deploy it as a separate process/container behind the same database (separate schema). This single extraction should eliminate the "payment brings down the whole site" problem.

2. **Set up per-service CI/CD pipelines.** Modify Jenkins (or migrate to GitHub Actions) to support independent build/deploy for the payment service and the remaining monolith. Target: payment service can deploy independently in under 30 minutes. This proves the deployability benefit before extracting more services.

3. **Add distributed tracing (Jaeger or similar) integrated with Datadog.** Before extracting additional services, you need observability across service boundaries. This is a prerequisite for operating any distributed architecture and should be in place before service count grows beyond 2.

4. **Extract remaining services incrementally based on team ownership.** Order Management, Catalog/Search, User/Account — one per quarter. Each extraction should map to a team boundary (Conway's Law). Do not extract a service unless a team will own it end-to-end.

5. **Introduce async messaging for the payment notification flow.** Once the team is comfortable operating 2-3 services, add a message queue (RabbitMQ or SQS) for payment confirmation events. This is the first step toward event-driven patterns and builds the team's async experience safely.

## Migration Path

```
Phase 1 (Months 1-3): Extract Payment Service
├── Define payment API boundary (REST)
├── Separate payment tables into own schema
├── Deploy payment as independent service
├── Set up independent CI/CD pipeline for payment
├── Result: Payment failures no longer cascade to the site
│
Phase 2 (Months 3-6): Observability + Second Extraction
├── Add distributed tracing (Jaeger + Datadog integration)
├── Extract Order Management service
├── Introduce async messaging for payment→order notifications
├── Result: Two independent deployment units, teams deploying daily
│
Phase 3 (Months 6-12): Complete Domain Separation
├── Extract Catalog/Search service
├── Extract User/Account service
├── Logically partition database schemas (still shared DB instance)
├── Result: 4-5 domain services, each owned by a team, independent deploy cycles
│
Phase 4 (12+ months): Evaluate Next Evolution
├── Assess: Is scalability still sufficient? (revisit if order volume 5-10x)
├── Assess: Is the team ready for event-driven patterns? (distributed tracing working, async messaging stable)
├── If yes: Introduce event-driven patterns for high-throughput flows (order processing, inventory)
├── If no: Stay with service-based — it may be sufficient for years
```

**Key principle for migration:** Each phase should deliver measurable value before starting the next. Phase 1 alone solves the primary business problem (flash sale outages). Do not proceed to Phase 2 until Phase 1 is stable in production. The monolith was not built in a day, and it should not be decomposed in a day.
