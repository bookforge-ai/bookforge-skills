# Trade-off Analysis: Scaling Order Processing in a Django E-Commerce Monolith

## Decision

How should we restructure the order processing module of a 3-year-old Django monolith (200k LOC, 12 developers) to handle 30x traffic spikes during flash sales (Black Friday), given that the team has zero microservices operational experience and a hard deadline of next Black Friday (~9 months)?

## Options Considered

1. **Full Microservices Extraction** -- Extract order processing (and related services like inventory, payments) into independently deployable microservices communicating over APIs and message queues.
2. **Modular Monolith with Targeted Scaling** -- Refactor the monolith into well-defined modules with explicit boundaries, then deploy the order processing module as a separately scalable process behind a shared database, using Django's existing ecosystem.
3. **Strangler Fig: Extract Only the Order Processing Hot Path** -- Keep the monolith intact but extract *only* the order-write path (place order, payment initiation, inventory reservation) into a single new service, routing flash-sale traffic to it while everything else stays in the monolith.

## Driving Quality Attributes

Based on the stated constraints (30x flash-sale spikes, team inexperience with distributed systems, hard 9-month deadline), the top 3 driving quality attributes are:

1. **Elasticity** -- The system must handle sudden 30x traffic bursts during flash sales without downtime. This is the non-negotiable business requirement.
2. **Simplicity (Operational)** -- The team has never operated microservices. Operational complexity directly translates to outage risk. The simpler the production operations, the lower the probability of a catastrophic failure during Black Friday itself.
3. **Time-to-market** -- There is a hard deadline. Whatever option is chosen must be production-ready and battle-tested before next Black Friday, with time for load testing.

---

## Step 3: Advantages of Each Option

### Option 1: Full Microservices Extraction

- **Elasticity (+):** Each service scales independently. Order processing can auto-scale to 30x while user profiles stays at 1x. This is the gold standard for targeted scaling.
- **Deployability (+):** Independent deployment pipelines. Order processing team can ship without coordinating with the catalog team.
- **Fault isolation (+):** A crash in the recommendation engine does not take down checkout. Blast radius is contained per service.
- **Long-term scalability (+):** Sets the architecture up for future growth beyond the immediate flash-sale problem.

### Option 2: Modular Monolith with Targeted Scaling

- **Simplicity (+):** Single deployment unit. No network calls between modules. No distributed transactions. Django ORM, single database, existing tooling all still work.
- **Time-to-market (+):** Refactoring module boundaries within a monolith is far less risky than extracting services. Can be done incrementally with existing Django expertise.
- **Cost (+):** No new infrastructure (no service mesh, no container orchestration, no message broker). Scale the monolith horizontally behind a load balancer with read replicas.
- **Testability (+):** Integration tests stay simple -- no contract testing, no service virtualization needed.
- **Maintainability (+):** One codebase, one repo, one CI pipeline. Easier for a 12-person team to reason about.

### Option 3: Strangler Fig (Extract Order Hot Path Only)

- **Elasticity (+):** The extracted order-write service can scale independently for flash sales. The monolith handles everything else at normal scale.
- **Simplicity (partial +):** Only one new service to operate, not five or ten. The operational surface area increase is bounded.
- **Time-to-market (+):** Extracting one bounded context is dramatically faster than a full microservices migration. Realistic in 9 months with load-testing time.
- **Risk containment (+):** The monolith continues to serve all non-flash-sale traffic. Fallback is straightforward: route traffic back to monolith if the new service fails.
- **Learning opportunity (+):** The team gains operational experience with exactly one distributed system before committing to more.

---

## Step 4: Disadvantages and Hidden Costs

### Option 1: Full Microservices Extraction

- **Operational complexity (---):** The team has ZERO microservices experience. They need to learn: container orchestration (Kubernetes or ECS), service discovery, distributed tracing, circuit breakers, API gateways, message broker operations, secret management, per-service CI/CD, per-service monitoring. This is not a 9-month learning curve on top of the migration work -- it is a multi-year organizational transformation.
- **Time-to-market (---):** A full extraction of a 200k LOC monolith into microservices takes 18-36 months for experienced teams. For an inexperienced team with a 9-month deadline, this is not achievable. Attempting it guarantees a half-finished migration that is worse than the original monolith (the "distributed monolith" anti-pattern).
- **Data consistency (--):** Distributed transactions across order, inventory, and payment services require sagas or eventual consistency. This is a fundamentally different programming model that the team must learn, and bugs in saga implementations cause lost orders or double charges -- exactly the worst failure mode for e-commerce during Black Friday.
- **Cost (--):** Kubernetes cluster, message broker (RabbitMQ/Kafka), API gateway, distributed tracing (Datadog/Jaeger), container registry -- infrastructure costs increase 3-5x or more.
- **Testing complexity (--):** End-to-end testing across services requires contract tests, service virtualization, and a staging environment that mirrors production topology. The existing Django test suite becomes inadequate.
- **Debugging difficulty (--):** A failed order now involves tracing requests across 3-5 services, correlating logs, and understanding async message flows. During a Black Friday outage, this complexity directly increases mean time to recovery (MTTR).

### Option 2: Modular Monolith with Targeted Scaling

- **Elasticity (--):** The entire monolith must scale together. If order processing needs 30x capacity, you're also scaling 30x of catalog browsing, user management, and admin tools. This is wasteful and may hit database bottlenecks before the application tier saturates.
- **Database bottleneck (--):** The single PostgreSQL database becomes the chokepoint. 30x write load on the orders table will cause lock contention, connection pool exhaustion, and query latency spikes regardless of how many application instances you run. Read replicas help for reads but not for the write-heavy order creation path.
- **Shared failure domain (--):** A memory leak in the product recommendation code still takes down checkout. Module boundaries are logical, not physical -- they share a process.
- **False sense of security (-):** "We refactored the modules" does not solve the scaling problem. The team may invest 6 months in clean module boundaries only to discover the database is still the bottleneck during load testing, leaving insufficient time to address it.
- **Scaling ceiling (-):** Horizontal scaling of a Django monolith has practical limits (database connections, shared state, session management). 30x is at the outer edge of what's achievable without architectural changes.

### Option 3: Strangler Fig (Extract Order Hot Path Only)

- **Data synchronization (--):** The extracted order service and the monolith both need access to product catalog, user accounts, and inventory data. You must decide: shared database (creates coupling), API calls back to monolith (creates a runtime dependency that can fail under load), or data replication (creates consistency lag).
- **Partial complexity (-):** You still need SOME distributed systems infrastructure: a message queue or API gateway for routing, health checks, deployment pipeline for the new service, monitoring for the new service. It's less than full microservices but more than zero.
- **Boundary definition difficulty (-):** Order processing in a 3-year-old monolith is unlikely to be cleanly separable. There will be deeply entangled dependencies: orders reference products, users, shipping rules, discount logic, tax calculation. Defining the cut line is the hardest part and will uncover unexpected coupling.
- **Two systems to debug (-):** During an incident, the team must determine whether the problem is in the monolith, the new service, or the interaction between them. This is harder than debugging one system (monolith) but easier than debugging five (full microservices).
- **Temporary architecture (-):** This is explicitly transitional. The team is maintaining two deployment targets. If the long-term plan is further extraction, this is a stepping stone. If not, it becomes an awkward split that accumulates its own technical debt.

---

## Trade-off Matrix

| Quality Attribute | Option 1: Full Microservices | Option 2: Modular Monolith | Option 3: Strangler Fig (Order Hot Path) |
|---|---|---|---|
| **Elasticity** | + Independent scaling per service | - Must scale entire monolith; DB bottleneck likely at 30x | + Order service scales independently; monolith stays at 1x |
| **Simplicity (Operational)** | --- Requires K8s, service mesh, distributed tracing, sagas -- team has zero experience | + Single deployment, existing tooling, Django ecosystem | - One new service to operate; bounded complexity increase |
| **Time-to-market** | --- 18-36 months for experienced teams; impossible in 9 months | + Fastest to implement; incremental refactoring | = Achievable in 9 months but tight; must define clean boundary |
| **Cost** | -- 3-5x infrastructure increase; significant training investment | + Minimal new infrastructure | - Moderate new infrastructure (one new service + routing) |
| **Fault isolation** | + Per-service blast radius | - Shared process; any module can crash the whole app | = Order service isolated; monolith still shared |
| **Maintainability** | - 12 devs across multiple repos, services, and pipelines | + Single codebase, familiar patterns | - Two systems but bounded scope |
| **Reliability** | - Distributed transactions, network failures, partial outages | + Single transaction boundary, ACID guarantees | - Must handle order service <-> monolith interaction failures |
| **Testability** | - Contract tests, service virtualization, complex E2E | + Existing test suite works | - Must test integration between two systems |

---

## Synergies and Conflicts

### Option 1: Full Microservices
- **Conflict:** Elasticity and deployability gains are *directly opposed* by the team's lack of operational simplicity. The architecture solves the scaling problem but creates an operational competence problem that is equally likely to cause a Black Friday outage.
- **Conflict:** Time-to-market is incompatible with the scope of work. Attempting this under deadline pressure virtually guarantees a "distributed monolith" -- the worst of both worlds.

### Option 2: Modular Monolith
- **Synergy:** Simplicity, time-to-market, and cost all reinforce each other. This is the cheapest, fastest, easiest option.
- **Conflict:** Simplicity directly conflicts with elasticity. The database bottleneck at 30x write load is a hard technical ceiling that module boundaries cannot solve. The synergy of this option's strengths creates a dangerous false confidence.

### Option 3: Strangler Fig
- **Synergy:** Elasticity for the critical path + bounded operational complexity. The team learns distributed systems on exactly one service boundary, which is a manageable learning scope in 9 months.
- **Synergy:** Time-to-market and risk containment reinforce each other. The monolith is the fallback. If the extraction isn't ready, the team can apply the modular monolith scaling tactics (more instances, read replicas, caching) as a degraded-mode backup.
- **Conflict:** Simplicity takes a hit -- two systems are always harder than one. But the hit is bounded and proportional to the criticality of the problem being solved.

---

## Recommendation

**Option 3: Strangler Fig (Extract Order Hot Path Only)** -- the least worst choice for this context.

### Primary justification (Elasticity)

The business-critical requirement is surviving 30x traffic during Black Friday. Option 3 directly addresses this by allowing the order-write path to scale independently. Unlike Option 2 (modular monolith), it avoids the database write bottleneck by giving the order service its own data store for order creation, with async replication to the monolith's database for reporting and fulfillment.

### Secondary justification (Operational simplicity + Time-to-market)

Unlike Option 1 (full microservices), Option 3 limits the operational complexity increase to exactly one new service. A team of 12 can realistically learn to operate one additional service in 9 months. They need: one container (Docker on ECS or a simple Kubernetes deployment), one message queue (SQS or RabbitMQ) for order events, one monitoring dashboard, and one deployment pipeline. This is learnable. Operating 5-10 microservices with a service mesh, distributed tracing, and saga orchestration is not learnable in the same timeframe.

### Acknowledged downsides and why they're acceptable

- **Data synchronization complexity:** The order service will need product and user data. Recommended approach: the order service calls the monolith's internal API for reads (acceptable latency for order placement) and publishes order events to a queue that the monolith consumes. This is simpler than a shared database and avoids tight coupling. During Black Friday, product catalog data can be cached aggressively (it doesn't change during a flash sale).
- **Two systems to maintain:** Yes, this is more complex than one. But the alternative is either (a) a monolith that falls over at 30x or (b) a microservices architecture the team can't operate. Two systems is the proportional response.
- **Temporary architecture:** This is a stepping stone, not a final state. If the business continues to grow, further extraction can follow. If not, the split stabilizes. Either way, the team gains the operational experience needed to make future decisions from a position of knowledge rather than theory.

---

## Risks of This Choice

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Boundary definition takes longer than expected** due to entangled order/product/discount logic | High | Medium -- delays the extraction timeline | Start with a 2-week spike to map all order processing dependencies. Define the boundary before committing to the extraction. If the boundary is too tangled, fall back to Option 2 + aggressive caching as an interim measure. |
| **Data consistency issues** between order service and monolith (e.g., order created but inventory not decremented) | Medium | High -- lost inventory accuracy, overselling | Use an outbox pattern: order service writes to its own DB and publishes an event. Monolith consumes the event and decrements inventory. If the event fails, a reconciliation job catches it. Run chaos testing before Black Friday. |
| **Team underestimates operational learning curve** for the new service | Medium | High -- incident during Black Friday due to unfamiliar system | Run at least 3 load tests at 30x scale before Black Friday. Conduct game-day exercises where the team practices debugging cross-system failures. Have a runbook for "route all traffic back to monolith" as an emergency fallback. |
| **Monolith itself can't handle 30x of non-order traffic** (browsing, search, cart) | Medium | Medium -- site slow even if orders work | Apply standard monolith scaling tactics: horizontal scaling behind a load balancer, read replicas for the database, CDN for static assets, Redis caching for product catalog. These are well-understood Django patterns and don't require architectural change. |
| **Flash sale traffic pattern has changed** and the order path isn't the actual bottleneck | Low | High -- solved the wrong problem | Instrument the monolith NOW to identify actual bottlenecks. Run a load test simulating 30x traffic against the current system to identify where it actually breaks. Don't assume -- measure. |

---

## Implementation Roadmap (High-Level)

| Phase | Timeline | Activities |
|---|---|---|
| **1. Measure and Map** | Months 1-2 | Instrument current monolith. Run 30x load test to identify actual bottlenecks. Map all order processing dependencies. Define the service boundary. |
| **2. Prepare the Monolith** | Months 2-4 | Refactor order processing code into a clean module within the monolith (modular monolith step). Create internal API boundaries. This is valuable regardless of extraction. |
| **3. Extract and Build** | Months 4-7 | Build the order-write service. Implement the outbox pattern for events. Set up deployment pipeline, monitoring, and alerting. |
| **4. Shadow and Test** | Months 7-8 | Run the new service in shadow mode (process orders but don't commit). Compare results with monolith. Load test at 30x. Fix discrepancies. |
| **5. Cutover and Harden** | Months 8-9 | Route production order traffic to new service. Monitor closely. Conduct game-day exercises. Prepare fallback runbook. |

---

## Architecture Decision Record

- **Status:** Proposed
- **Context:** Our Django e-commerce monolith (200k LOC, 12 developers, 3 years old) cannot handle 30x traffic spikes during flash sales. The entire site went down on Black Friday. The order processing module is the primary bottleneck. The team has no microservices operational experience. We have approximately 9 months until next Black Friday.
- **Decision:** We will extract the order-write hot path (order placement, payment initiation, inventory reservation) into a single independently scalable service using the Strangler Fig pattern. The monolith continues to serve all other traffic. Communication between the new service and monolith uses synchronous API calls for reads and asynchronous events (outbox pattern) for writes. We chose this over full microservices (impossible timeline, team lacks operational experience) and modular monolith alone (doesn't solve the database write bottleneck at 30x). We chose the Strangler Fig specifically because it provides the targeted elasticity we need while bounding the operational complexity increase to exactly one new service -- a learnable scope for the team in the available timeframe.
- **Consequences:**
  - **Positive:** Order processing scales independently during flash sales. Team gains distributed systems experience on a bounded scope. Monolith is the fallback if extraction fails. The modular monolith refactoring (Phase 2) is valuable regardless.
  - **Negative:** Two systems to operate and debug. Data synchronization between order service and monolith adds complexity. This is a transitional architecture that may need further evolution. The team must invest in new operational skills (containers, message queues, distributed monitoring) within a tight timeline.
