# Trade-off Analysis: E-Commerce Order Processing — Monolith vs Microservices vs Modular Monolith

## Decision

How should we restructure the order processing module of a 3-year-old Django monolith (200k LOC, 12 developers) to handle 30x traffic spikes during flash sales (Black Friday), given that the team has zero microservices operational experience and a hard deadline of next Black Friday (~9 months)?

## Options Considered

1. **Full Microservices Extraction** — Extract order processing (and related services like inventory, payments, notifications) into independently deployable microservices with separate databases and inter-service communication.
2. **Modular Monolith with Selective Scaling** — Refactor the Django monolith into well-defined modules with strict boundaries, then deploy the order processing module as a separately scalable process behind a shared database, without going full microservices.
3. **Strangler Fig with Order Processing Service** — Extract ONLY the order processing module as a single independent service while leaving the rest of the monolith intact. Route order traffic through the new service; everything else stays in Django.

## Driving Quality Attributes

Based on the stated context (flash sale scaling, team inexperience with distributed systems, hard deadline), the top 3 driving attributes are:

1. **Elasticity** — The core problem: 30x traffic spikes during flash sales brought the entire site down. The order processing module must scale independently and handle sudden bursts.
2. **Time-to-market** — Hard deadline of next Black Friday. There is no room for a multi-year migration. Whatever is chosen must be production-ready within ~9 months.
3. **Simplicity (Operational)** — The team has never operated microservices. Introducing too much operational complexity could cause MORE outages, not fewer. The solution must be operable by this team.

Supporting attributes also considered: availability, cost, maintainability, deployability.

## Analysis of Each Option

### Option 1: Full Microservices Extraction

**Advantages:**
- **Elasticity (+):** Each service scales independently. Order processing can auto-scale to 30x while user browsing stays at normal capacity. This is the gold standard for independent scaling.
- **Deployability (+):** Each service can be deployed independently. Order processing changes don't risk breaking the product catalog.
- **Fault isolation (+):** If order processing crashes under load, the rest of the site stays up (with proper bulkheading).

**Disadvantages:**
- **Time-to-market (---):** Extracting multiple services from a 200k LOC monolith in 9 months with a team that has never done it is extremely high risk. Service boundaries, data decomposition, inter-service communication, distributed transactions — each is a multi-month effort. Teams experienced with microservices typically take 12-18 months for a migration of this scale.
- **Simplicity (---):** The team needs to learn: container orchestration (Kubernetes or equivalent), service mesh or API gateway, distributed tracing, circuit breakers, eventual consistency patterns, independent CI/CD pipelines per service, database-per-service migration. This is a massive operational learning curve.
- **Reliability (-):** Distributed transactions across services (e.g., order placed → inventory decremented → payment captured) are fundamentally harder than local database transactions. Saga patterns or two-phase commits introduce failure modes the team has never dealt with.
- **Cost (-):** Multiple services = multiple databases, multiple container clusters, monitoring per service, potential cloud spend increase of 2-5x for infrastructure alone.
- **Observability (-):** Debugging a failed order now requires correlating logs across 4-5 services instead of reading one Django traceback.

### Option 2: Modular Monolith with Selective Scaling

**Advantages:**
- **Simplicity (+):** The team stays in Django-land. No new languages, no new deployment infrastructure, no distributed systems patterns to learn. The mental model remains "it's one application with clear internal boundaries."
- **Time-to-market (+):** Refactoring internal module boundaries is faster than extracting services. Can be done incrementally alongside feature work. Realistic in 4-6 months.
- **Cost (+):** No new infrastructure. Can scale by running multiple instances of the monolith behind a load balancer (horizontal scaling). Django handles this well with stateless request handling + shared database.
- **Maintainability (+):** Clean module boundaries improve code quality regardless of deployment model. The refactoring work pays off even if you later extract services.

**Disadvantages:**
- **Elasticity (-):** You can scale the entire monolith horizontally, but you cannot scale ONLY order processing independently. During a 30x flash sale, you're scaling everything — user profiles, product catalog, admin panel — just to handle order spikes. This is wasteful and may hit database connection limits.
- **Scalability (-):** The shared database becomes the bottleneck. 30x order processing load means 30x database write pressure, which also affects product browsing queries. Read replicas help reads, but write contention on inventory and order tables remains.
- **Deployability (=):** Still a single deployment unit. A bug in the product catalog module still requires redeploying the order processing module.
- **Fault isolation (-):** An OOM error or CPU spike in one module still takes down the whole process.

### Option 3: Strangler Fig — Extract Order Processing Only

**Advantages:**
- **Elasticity (+):** The order processing service scales independently. During flash sales, you auto-scale just the order service to 30x while the rest of the monolith handles normal browsing traffic. This directly solves the Black Friday problem.
- **Time-to-market (+):** Extracting ONE service is dramatically simpler than extracting many. The team focuses on a single, well-understood bounded context. Realistic in 5-7 months with buffer.
- **Simplicity (moderate):** The team learns distributed systems concepts on ONE boundary, not five. One new service to operate, one API contract to maintain, one new CI/CD pipeline. The learning curve is steep but bounded.
- **Fault isolation (+):** If the order service has issues, the main site (browsing, search, account management) stays up. If the monolith has issues, orders in-flight can be queued.
- **Availability (+):** The order processing service can be deployed with higher redundancy (multi-AZ, more replicas) independently of the monolith.

**Disadvantages:**
- **Simplicity (-):** The team still needs to learn SOME distributed systems concepts: API gateway or routing layer, async communication (message queue for order events), health checks, separate deployment pipeline. Not zero learning, but bounded.
- **Reliability (-):** The order-to-payment-to-inventory flow now crosses a service boundary. If the order service places an order but the monolith fails to decrement inventory, you have an inconsistency. Needs careful design: either a synchronous call back to the monolith, or an event-driven approach with compensating transactions.
- **Cost (moderate -):** One additional service means some extra infrastructure, but far less than full microservices. Estimated 30-50% infrastructure cost increase vs. 200-500% for full microservices.
- **Maintainability (-):** Now there are two codebases. Feature work that touches orders AND other modules requires coordinated changes. Integration testing becomes harder.
- **Observability (-):** Debugging order flows now spans two systems. Need distributed tracing for the order path (but only one boundary to trace across, not five).

## Trade-off Matrix

| Quality Attribute | Option 1: Full Microservices | Option 2: Modular Monolith | Option 3: Strangler Fig (Order Svc) |
|---|---|---|---|
| **Elasticity** | + Fully independent scaling per service | - Can only scale entire monolith; wasteful | + Order processing scales independently |
| **Time-to-market** | --- 12-18 months realistic; 9 months is reckless | + 4-6 months achievable | + 5-7 months achievable with buffer |
| **Simplicity (Operational)** | --- Massive learning curve across all services | + Team stays in familiar Django territory | = One new service to learn; bounded complexity |
| **Availability** | + Per-service redundancy | = Standard monolith availability | + Order service gets independent redundancy |
| **Cost** | - 2-5x infrastructure increase | + Minimal additional cost | = 30-50% infrastructure increase |
| **Reliability** | - Distributed transactions across many boundaries | + Local ACID transactions | - One service boundary to manage carefully |
| **Maintainability** | - Multiple codebases, teams need to reorganize | + Clean modules improve code quality | = Two codebases; manageable with 12 devs |
| **Deployability** | + Independent deployments | = Single deployment unit | + Order service deploys independently |
| **Observability** | - Distributed tracing across many services | + Single application logs/traces | = One boundary to trace across |
| **Fault Isolation** | + Full isolation between services | - One module can crash the whole app | + Order processing isolated from monolith |

## Synergies and Conflicts

**Option 1 (Full Microservices):**
- **Synergy:** Elasticity + Deployability + Fault Isolation all reinforce each other — independent services naturally provide all three.
- **Conflict:** Elasticity CONFLICTS with Simplicity and Time-to-market. The very thing that gives you perfect scaling (many independent services) is what makes this impossible to deliver safely in 9 months with an inexperienced team.

**Option 2 (Modular Monolith):**
- **Synergy:** Simplicity + Time-to-market + Cost all reinforce each other — staying in one codebase minimizes everything that takes time and money.
- **Conflict:** Simplicity CONFLICTS with Elasticity. The single deployment unit that keeps things simple is exactly what prevents independent scaling. This is the core tension: the option that's fastest to deliver doesn't solve the actual problem (30x order scaling).

**Option 3 (Strangler Fig):**
- **Synergy:** Elasticity + Time-to-market are partially aligned — extracting one service gives you the scaling you need in a timeframe you can hit.
- **Conflict:** Elasticity CONFLICTS with Reliability at the service boundary. The order-to-inventory transaction that was previously ACID now crosses a network boundary. This is manageable with careful design but cannot be ignored.

## Recommendation

**Option 3: Strangler Fig — Extract Order Processing Service** — the least worst choice for this context because:

1. **It solves the actual problem.** The site went down on Black Friday because order processing couldn't scale independently. This option directly enables independent scaling of orders. Option 2 does not solve this problem — horizontally scaling the entire monolith is wasteful and hits database limits before reaching 30x.

2. **It's achievable in the timeline.** A single service extraction is realistic in 5-7 months for a 12-person team, leaving buffer before Black Friday. Full microservices in 9 months is not realistic for a team with no distributed systems experience — that path leads to a half-migrated system that's WORSE than the current monolith (distributed monolith anti-pattern).

3. **The learning curve is bounded.** The team learns distributed systems concepts on ONE boundary. They operate ONE new service. This builds the muscle memory and operational tooling that could enable further extraction later, without betting the entire platform on skills they don't have yet.

4. **Acknowledged downsides and why they're acceptable:**
   - The order-to-inventory transaction boundary introduces distributed consistency risk. **Acceptable because:** this can be mitigated with a transactional outbox pattern or synchronous callback to the monolith for inventory decrements. It's one boundary to get right, not ten.
   - There's still operational learning required (containerizing the order service, setting up a message queue, adding distributed tracing). **Acceptable because:** 12 developers is enough to dedicate 2-3 people to infrastructure while others continue feature work.
   - Two codebases means coordinated releases for cross-cutting features. **Acceptable because:** the order processing module likely has a relatively stable API surface (place order, check status, cancel order). The interface won't change frequently.

## Risks of This Choice

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Team underestimates distributed systems complexity at the service boundary | High | High | Allocate 2 senior devs to own the integration layer. Invest in integration tests that simulate the monolith-to-order-service failure modes. Run a chaos engineering session before Black Friday. |
| Database becomes the bottleneck even with order service extracted (shared DB initially) | Medium | High | Start with a shared database for pragmatism, but isolate order tables. Use read replicas for the monolith's queries. Plan to extract the order database in Phase 2 if write contention appears in load tests. |
| 9-month timeline slips due to unexpected refactoring in the monolith to clean up order processing boundaries | Medium | Medium | Start with a thorough domain analysis (2-3 weeks) to map order processing dependencies before writing code. Identify the "hairiest" coupling early. Timebox the extraction to 5 months with a 2-month buffer. |
| Flash sale traffic exceeds 30x or has unexpected patterns (e.g., inventory check storms) | Low | High | Load test the extracted order service at 50x (not just 30x). Implement circuit breakers on the order-to-monolith boundary. Add a queue-based buffer so order submissions are accepted and processed asynchronously during extreme spikes. |
| Team splits focus between extraction work and feature delivery, neither gets done well | Medium | High | Dedicate a "platform squad" (3-4 devs) to the extraction full-time. Remaining 8-9 devs continue feature work on the monolith. Do NOT try to have everyone context-switch between both. |

## Context Sensitivity

This recommendation assumes: the team has zero microservices experience, the deadline is hard (next Black Friday, ~9 months), the order processing module has relatively clear boundaries within the monolith, and the team size is 12 developers.

- **If the team had 2+ years of microservices operational experience** → Option 1 (Full Microservices) becomes viable. The timeline risk drops dramatically when the team already knows Kubernetes, distributed tracing, saga patterns, and CI/CD per service. With experienced teams, 9 months for extracting 3-4 services from a 200k LOC monolith is aggressive but feasible.

- **If the deadline were 18-24 months instead of 9** → Option 1 (Full Microservices) would be the stronger choice. The extra time allows the team to learn distributed systems properly, extract services incrementally with the Strangler Fig pattern (but multiple services, not just one), and run multiple Black Friday rehearsals.

- **If the traffic spike were 3-5x instead of 30x** → Option 2 (Modular Monolith) would likely suffice. Horizontal scaling of the monolith with database read replicas and caching can handle moderate traffic increases. The complexity of service extraction wouldn't be justified.

- **If the team were 4-5 developers instead of 12** → Option 2 (Modular Monolith) would be recommended regardless of the traffic spike. A team of 4-5 cannot sustain two codebases, two deployment pipelines, and the operational overhead of a separate service. They'd need to solve the scaling problem with infrastructure (larger instances, aggressive caching, queue-based order buffering) rather than architecture.

- **If budget were severely constrained** → Option 2 (Modular Monolith) with aggressive caching and queue-based order buffering. The infrastructure cost of running a separate service (even one) is real. For budget-constrained teams, horizontal auto-scaling of the monolith with a message queue in front of order processing might be the pragmatic choice.

- **If the monolith's order processing module is deeply entangled with other modules (shared models, circular imports, no clear boundaries)** → The timeline for Option 3 increases significantly. Budget 2-3 months for untangling before extraction begins. If the entanglement is extreme, Option 2 (Modular Monolith) may be the only realistic choice within 9 months, and the scaling problem would need to be solved with infrastructure (oversized instances + queue buffering) rather than architecture.

## Architecture Decision Record

- **Status:** Proposed
- **Context:** Our Django e-commerce monolith (200k LOC, 12 developers, 3 years old) experienced a complete site outage during Black Friday due to 30x traffic on order processing. The entire site went down because order processing could not scale independently — the monolith is a single deployment unit where all modules share compute and database resources. The CEO has mandated a fix before next Black Friday (~9 months). Our team has no prior experience operating microservices or distributed systems. We need an architecture that enables independent scaling of order processing while remaining achievable within the timeline and operational capabilities of the team.
- **Decision:** We will extract the order processing module into an independently deployable service using the Strangler Fig pattern, while keeping the remainder of the application as a Django monolith. Order submissions during flash sales will be accepted via the new service and buffered through a message queue. The order service will communicate with the monolith via a well-defined API for inventory and payment operations. We chose this over full microservices extraction (unacceptable timeline and operational risk for an inexperienced team) and over a modular monolith (does not solve the independent scaling requirement for 30x spikes).
- **Consequences:**
  - *Positive:* Order processing scales independently during flash sales. Fault isolation prevents order spikes from crashing the browsing experience. Team learns distributed systems on a single, bounded service boundary. Path is open for further extraction in future phases.
  - *Negative:* One distributed transaction boundary (order→inventory) introduces consistency complexity that must be carefully designed (transactional outbox or synchronous callback). Two codebases require coordinated releases for cross-cutting changes. Infrastructure cost increases ~30-50%. Team must learn containerization, message queues, and distributed tracing for the order service.
