# Granularity Disintegrators and Integrators -- Deep Reference

> Source: Chapter 17, Fundamentals of Software Architecture (Richards & Ford)
> Read this file when you need detailed trade-off analysis for specific disintegrator/integrator combinations.

## Disintegrators (Forces Pushing Toward Smaller Services)

Disintegrators are reasons to break a service into smaller pieces. Each has a specific test and threshold. A service should only be split when at least one disintegrator clearly applies with concrete evidence.

### 1. Service Scope and Function

**What it tests:** Is the service responsible for too many unrelated business capabilities?

**How to evaluate:**
- Can you describe the service in one sentence without "and"?
- Does the service span multiple bounded contexts?
- Would different teams naturally own different parts of this service?

**Split threshold:** The service handles 3+ distinct business capabilities that could operate independently.

**Example:**
- BAD (too broad): "CustomerService handles registration, preferences, authentication, notification settings, and analytics tracking"
- GOOD (split): CustomerProfile (registration, preferences), AuthService (authentication), NotificationService (settings + delivery), AnalyticsService (tracking)

**Counter-check with integrators:** Before splitting, verify that the proposed sub-services don't have strong transaction or workflow integrators between them.

### 2. Code Volatility

**What it tests:** Do different parts of the service change at significantly different rates?

**How to evaluate:**
- Look at git history: which directories/packages change most frequently?
- Over 6 months, does one component change weekly while another hasn't changed?
- Do deployments of stable components happen only because an unrelated component changed?

**Split threshold:** One component changes 5x+ more frequently than another, causing unnecessary redeployments of stable code.

**Example:**
- A ReportingService contains both report generation (stable, changes quarterly) and report template management (volatile, changes weekly for new template types). Split: ReportEngine (stable) + ReportTemplates (volatile).

**Counter-check:** If the volatile and stable components share significant business logic (shared code integrator), splitting may force you to maintain that logic in two places.

### 3. Scalability

**What it tests:** Do different parts of the service need different numbers of instances or different resource profiles?

**How to evaluate:**
- Does one component need 10 instances while another needs 1?
- Does one component need GPUs while another needs only CPU?
- Do traffic patterns differ (one spikes during events, another is steady)?

**Split threshold:** One component needs 3x+ more instances or fundamentally different resources than another component in the same service.

**Example:**
- A ProductService handles both product catalog browsing (high traffic, needs 20 instances) and product data import (low traffic, needs 1 instance, runs nightly). Split: ProductCatalog (scales horizontally) + ProductImport (single instance, batch).

**Counter-check:** If both components read/write the same database tables, splitting creates data coupling that may negate the scaling benefit.

### 4. Fault Tolerance

**What it tests:** Should a failure in one part of the service NOT affect another part?

**How to evaluate:**
- If Component A fails, must Component B keep working?
- Are there different availability SLAs for different parts?
- Does a non-critical feature bring down a critical one when it fails?

**Split threshold:** A non-critical component's failure has caused (or could cause) downtime in a critical component.

**Example:**
- An OrderService handles both order placement (critical, must be 99.99% available) and order recommendations (nice-to-have, can degrade). If the recommendation engine has a memory leak, it shouldn't crash order placement. Split: OrderProcessing (critical) + OrderRecommendations (degradable).

**Counter-check:** If order processing needs recommendation data to function (data relationship integrator), the split may not achieve true fault isolation.

### 5. Security

**What it tests:** Do different parts require different security levels, access controls, or compliance boundaries?

**How to evaluate:**
- Does one component handle PCI/PII/HIPAA data while another handles public data?
- Do different components need different network zones or encryption levels?
- Would a security audit scope be smaller if the component were isolated?

**Split threshold:** The entire service must run at the highest security level because one component requires it, forcing unnecessary security overhead on other components.

**Example:**
- A UserService handles both user profiles (moderate security) and payment methods (PCI DSS scope). Keeping them together puts the entire service in PCI scope. Split: UserProfile (standard security) + PaymentMethods (PCI-isolated).

### 6. Extensibility

**What it tests:** Is one part of the service likely to grow significantly while other parts remain stable?

**How to evaluate:**
- Are new features concentrated in one component?
- Is one component's API surface growing while another is stable?
- Would adding new functionality to one component benefit from independent deployment?

**Split threshold:** One component is receiving 5x+ more feature requests than others, and the shared deployment pipeline slows down delivery.

---

## Integrators (Forces Pushing Toward Larger Services)

Integrators are reasons to keep services together (or merge services that were split). They represent costs that are incurred when services are separated. Integrators generally win over disintegrators when they apply strongly.

### 1. Database Transactions

**Strength: VERY HIGH** -- This is the most powerful integrator.

**What it tests:** Do operations across these services need ACID guarantees?

**How to evaluate:**
- Must Operation A and Operation B either both succeed or both fail?
- Would eventual consistency cause business-visible problems (double charges, phantom inventory, inconsistent records)?
- Are you building SAGA patterns for operations that were simple database transactions before splitting?

**Merge threshold:** If you need ACID transactions between two services, they almost certainly should be one service. "Don't do transactions in microservices -- fix granularity instead!"

**When to override:** Only when a strong disintegrator (usually security or extreme scalability difference) makes merging impractical AND the business can tolerate eventual consistency with compensating transactions.

**The saga alternative (last resort):**
If services genuinely cannot be merged despite transaction needs, implement the saga pattern:

| Aspect | Choreographed Saga | Orchestrated Saga |
|--------|-------------------|-------------------|
| Coordination | Each service triggers the next | Central mediator coordinates |
| Coupling | Lower | Higher (through mediator) |
| Error handling | Distributed across services | Centralized in mediator |
| Visibility | Low (requires distributed tracing) | High (mediator has full state) |
| Complexity | Higher for complex workflows | Higher for simple workflows |
| Best for | 2-3 service sagas | 4+ service sagas |

**Saga implementation pattern:**
```
For each service operation in the saga:
  1. Define the "do" operation (forward action)
  2. Define the "undo" operation (compensating action)
  3. Define the "pending" state (in-flight marker)

On success: all services commit, clear pending state
On failure at step N:
  1. Record failure
  2. Call undo on steps N-1, N-2, ..., 1 (reverse order)
  3. Report failure to caller
  4. If undo itself fails: alert + manual resolution queue
```

### 2. Workflow and Choreography Coupling

**Strength: HIGH**

**What it tests:** Do these services require extensive back-and-forth communication to complete business operations?

**How to evaluate:**
- Count the inter-service calls for common workflows. If a single business operation requires 4+ synchronous calls between two specific services, they are tightly coupled.
- Does Service A frequently wait for Service B's response before it can continue? (Synchronous dependency)
- If Service B is down, can Service A do anything useful?

**Merge threshold:** If Service A calls Service B on every request, and neither can function without the other, they are one service pretending to be two.

**The front controller anti-pattern:**
In choreography, one service often becomes the "first service called" for complex workflows. This service ends up coordinating other services while also maintaining its own domain logic, making it an accidental mediator. If a choreographed service is spending more than ~30% of its logic on coordination, consider either:
- Merging the coordinated services back together, OR
- Extracting the coordination into an explicit orchestrator service (removing it from the domain service)

### 3. Shared Code

**Strength: MODERATE**

**What it tests:** Do these services share significant business logic?

**How to evaluate:**
- Is the same business rule implemented in multiple services?
- When a business rule changes, how many services need updating?
- Is there a shared library containing business logic (not just utilities)?

**Important distinction:**
- **Shared infrastructure code** (logging, monitoring, circuit breakers) -> This is fine. Use the sidecar pattern. Don't merge services because they share operational concerns.
- **Shared business logic** (pricing rules, validation logic, domain calculations) -> This indicates the services may belong together. The shared business logic represents a single bounded context that was split across services.

**Merge threshold:** If changing a business rule requires coordinated updates to 3+ services, the rule likely belongs in a single service that owns that business logic.

### 4. Data Relationships

**Strength: MODERATE**

**What it tests:** Do these services constantly need each other's data?

**How to evaluate:**
- Does Service A frequently query Service B just to get reference data?
- Could Service A cache Service B's data, or does it always need the latest?
- What percentage of Service A's requests require data from Service B?

**Merge threshold:** If >50% of Service A's operations require real-time data from Service B, they have a data relationship that suggests they should be one service.

**Alternatives to merging:**
- **Data replication:** Service B publishes events when its data changes; Service A maintains a read-only copy. Works for reference data that doesn't change frequently.
- **Shared data service:** Extract the shared data into its own service that both consume. Works when the data is a clear domain concept (e.g., "configuration" used by many services).

---

## Disintegrator vs. Integrator Conflict Resolution

When both forces apply to the same service, use this priority framework:

| Conflict | Typical resolution |
|----------|-------------------|
| Scalability disintegrator + Transaction integrator | Keep together. Scale the combined service. Transactions trump scalability unless the scalability difference is extreme (100x+). |
| Security disintegrator + Transaction integrator | Split. Security isolation is hard to compromise. Use saga pattern for the transaction. Accept the complexity cost. |
| Code volatility disintegrator + Shared code integrator | Keep together. Deploy more frequently. The cost of maintaining shared business logic across services usually exceeds the cost of redeploying stable code. |
| Fault tolerance disintegrator + Workflow coupling integrator | Split, but use async communication. The faulting service can degrade gracefully while the critical service continues. Use circuit breakers. |
| Scope disintegrator + Data relationship integrator | Evaluate: can the data relationship be handled by replication or events? If yes, split. If the data must be real-time consistent, keep together. |

## Choreography vs. Orchestration Decision Matrix

| Decision factor | Favors Choreography | Favors Orchestration |
|----------------|:---:|:---:|
| Number of services in workflow | 2-3 | 4+ |
| Error handling complexity | Simple (retry/fail) | Complex (compensating transactions) |
| Workflow visibility needs | Low | High (audit trail, monitoring) |
| Decoupling priority | High | Moderate |
| Domain/architecture isomorphism | Microservices (natural fit) | Structured workflows (better fit) |
| Performance sensitivity | Higher (no mediator bottleneck) | Lower (mediator adds latency) |
| Team autonomy | Teams work independently | Teams coordinate through mediator contract |

**Default recommendation:** Start with choreography. Introduce orchestration only when choreography complexity becomes unmanageable (typically when a single workflow spans 4+ services with compensating transactions).

## The Sidecar Pattern and Service Mesh

**Problem:** Microservices duplicates infrastructure concerns (logging, monitoring, circuit breakers) across services. Each team implementing these independently leads to inconsistency.

**Solution:** The sidecar pattern extracts operational concerns into a separate component that deploys alongside each service. The sidecar handles logging, monitoring, circuit breakers, and other cross-cutting concerns. A shared infrastructure team maintains the sidecar; when they upgrade the monitoring tool, every service gets the upgrade automatically.

**Service mesh:** When all sidecars connect to a shared service plane, the result is a service mesh -- a consistent operational interface across all microservices. The service mesh provides:
- Unified logging and monitoring
- Consistent circuit breaker behavior
- Service discovery
- mTLS between services
- Traffic management and routing

**Key principle:** The sidecar pattern is the correct way to handle operational reuse in microservices. Domain logic is duplicated (each service has its own Address class). Operational logic is shared (via sidecar). This is the opposite of SOA, which tried to share everything.
