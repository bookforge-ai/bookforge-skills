# Grading: microservice-granularity-optimizer -- Iteration 1

## Assertions

### Structural Assertions
| ID | Assertion | Description |
|----|-----------|-------------|
| S1 | applies-disintegrators | Evaluates services against the 6 granularity disintegrators (scope, volatility, scalability, fault tolerance, security, extensibility) with specific evidence |
| S2 | applies-integrators | Evaluates service pairs against the 4 granularity integrators (transactions, workflow coupling, shared code, data relationships) with specific evidence |
| S3 | selects-communication-pattern | Makes an explicit choreography vs orchestration decision per workflow with reasoning |
| S4 | designs-saga-correctly | For distributed transactions, designs saga with do/undo operations, pending state management, and error handling for failed compensations |
| S5 | validates-against-ratings | Validates design against microservices characteristic ratings (Deploy=4, Elast=5, Evol=5, FaultTol=4, Mod=5, Cost=1, Perf=2, Rel=4, Scale=5, Simple=1, Test=4) |

### Value Assertions
| ID | Assertion | Description |
|----|-----------|-------------|
| V1 | fix-granularity-not-transactions | Applies the principle "Don't do transactions in microservices -- fix granularity instead!" -- evaluates whether separate services are justified before designing distributed transactions |
| V2 | detects-over-splitting | Identifies when services are too fine-grained based on excessive inter-service calls, unnecessary sagas, or services that can't function independently |
| V3 | detects-distributed-monolith | Checks for shared databases, coordinated deployments, or services that can't operate independently |
| V4 | bounded-context-awareness | Models services as bounded contexts (domain/workflow) rather than entities -- avoids the entity trap |
| V5 | data-isolation-enforced | Each service owns its data exclusively -- no shared databases, schemas, or tables |
| V6 | integrators-win-conflicts | When disintegrators and integrators conflict, properly weighs integrators (generally stronger) unless a very strong disintegrator overrides with explicit justification |
| V7 | saga-used-sparingly | SAGAs are used only when genuinely necessary, with a warning that >30% of workflows needing sagas indicates wrong granularity |

---

## Eval 1: Monolithic Order Service Decomposition

**Prompt:** "We have a monolithic Order service that handles: order creation, inventory checks, payment processing, shipping label generation, and email notifications. It's becoming too large. How should we split it into microservices?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | All 6 disintegrators evaluated for the monolithic service with specific evidence per factor. Score: 6/6. |
| S2 | PASS | 4 service pairs analyzed: Order+Inventory (1.5/4), Order+Payment (2.5/4), Order+Shipping (0/4), Order+Notification (0/4). Each integrator scored with evidence. |
| S3 | PASS | 5 workflows mapped: order placement (orchestration), browse stock (N/A), shipping (choreography), notifications (choreography), refund (orchestration). Reasoning for each. |
| S4 | PASS | Two sagas designed: Place Order (3-step with do/undo/pending state) and Process Refund (2-step). Error handling for failed undos documented. Alert + manual resolution for failed payment refund. |
| S5 | PASS | Full 11-characteristic table with ratings and "meets needs" assessment. Notes Performance (2) and Simplicity (1) as risks with mitigations. |
| V1 | PASS | Explicitly evaluates integrators before splitting. Order+Payment integrator score is 2.5/4 (normally would merge), but PCI security disintegrator overrides with explicit justification. |
| V2 | PASS | Recommends 5 services (not 9 entity-based services). Avoids splitting OrderCreation/OrderValidation/OrderPricing. |
| V3 | PASS | Anti-pattern checklist includes distributed monolith check. Each service deploys independently and owns its data. |
| V4 | PASS | Services model workflows: "OrderService handles order lifecycle" not "orders entity." Inventory handles "stock management" not "inventory table." |
| V5 | PASS | Each service has its own database. Payment has PCI-isolated DB. No shared tables. |
| V6 | PASS | Order+Payment: integrators (2.5/4) normally win, but security disintegrator overrides with explicit justification (PCI scope reduction). Key trade-off acknowledged at bottom. |
| V7 | PASS | Notes 2 of 5 workflows need saga (40%), acknowledges this is slightly above 30% threshold, justifies with "strong PCI security disintegrator." |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | FAIL | No disintegrator analysis. Services split by entity/function without evaluating forces. |
| S2 | FAIL | No integrator analysis. No evaluation of which services should stay together. |
| S3 | FAIL | Communication described as a fixed flow (step 1-8) mixing REST and RabbitMQ without reasoning about choreography vs orchestration per workflow. |
| S4 | FAIL | Saga mentioned but not designed. No do/undo operations specified. No pending state management. No error handling for failed compensations. |
| S5 | FAIL | No characteristic ratings validation. |
| V1 | FAIL | Jumps directly to splitting without evaluating whether services need to be separate. Proposes saga without asking "should these be one service?" |
| V2 | FAIL | Creates 9 services including separate OrderCreation, OrderValidation, OrderStatus, ShippingLabel, ShippingTracking, EmailNotification, SMSNotification. Textbook over-splitting. |
| V3 | FAIL | No distributed monolith check. Some services likely share data patterns. |
| V4 | FAIL | Entity trap: ShippingLabelService and ShippingTrackingService are not bounded contexts. They are components of a Shipping bounded context. |
| V5 | PARTIAL | States "each service gets its own PostgreSQL database" but doesn't address data isolation or the consequences for shared data needs. |
| V6 | FAIL | No integrator analysis, so no conflict resolution. |
| V7 | FAIL | Saga applied without questioning whether it's necessary. No threshold or warning about overuse. |

**Score: 0.5/12 (4%)**

---

## Eval 2: Over-Split User Service

**Prompt:** "We split our User service into 5 microservices: UserProfile, UserPreferences, UserAuth, UserNotifications, and UserAnalytics. Now every API call requires 3-4 inter-service calls and our latency tripled. Did we over-split? How do we fix this?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | Disintegrators evaluated for all 5 services in a comparison table. Identifies that only Notifications (scalability, fault tolerance, extensibility) and Analytics (code volatility, extensibility) have legitimate disintegrators. |
| S2 | PASS | Two service pairs analyzed in detail: Profile+Preferences (4/4 integrators), Profile+Auth (4/4 integrators). Both scored maximum, triggering merge. |
| S3 | PASS | Post-merge communication: UserService->Notification (choreography, fire-and-forget), UserService->Analytics (choreography, async events). |
| S4 | PASS | Notes that the user registration saga is ELIMINATED by merging -- now a single ACID transaction. This is the skill's core principle in action. |
| S5 | PASS | Characteristic table included with Performance improvement noted. |
| V1 | PASS | Core diagnosis: "A saga for user registration is absurd -- this was a simple database transaction before the split." Directly applies "fix granularity instead." |
| V2 | PASS | Primary finding: services are over-granular. 5 services reduced to 3. Inter-service calls reduced from 3-4 to 0 for core operations. Latency improvement quantified (16x for registration, 5x for profile view). |
| V3 | PASS | Identifies that the 5-service User architecture was a distributed monolith: services couldn't function independently. |
| V4 | PASS | Root cause identified as entity trap: "User" domain was split along entity/function lines within a single bounded context. UserPreferences is "an attribute of the UserProfile bounded context." |
| V5 | PASS | After merge, each of 3 services owns its data exclusively. |
| V6 | PASS | Auth security disintegrator evaluated but integrators (4/4) win. "Security concern can be addressed within a merged service through encryption, access controls, and internal modularization." |
| V7 | PASS | Post-merge: 0 of 3 workflows need saga (0%). Eliminated the only saga that existed. |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | FAIL | No disintegrator analysis. Doesn't evaluate which services have legitimate reasons to be separate. |
| S2 | FAIL | No integrator analysis. Doesn't evaluate which services should be merged based on transaction, coupling, or data relationship forces. |
| S3 | FAIL | No communication pattern selection. Doesn't discuss choreography vs orchestration. |
| S4 | FAIL | No saga analysis (positive or negative). Doesn't identify the existing registration saga as a granularity indicator. |
| S5 | FAIL | No characteristic ratings. |
| V1 | FAIL | Does not apply "fix granularity" principle. Instead of evaluating whether services should be merged, proposes adding MORE infrastructure (BFF, Redis, GraphQL) to work around the wrong granularity. |
| V2 | FAIL | Only suggests merging Profile+Preferences as a "last resort" (Option 4), keeping the architecture at 4 services. Does not identify Auth as part of the same bounded context. |
| V3 | FAIL | Does not identify the distributed monolith. The 5-service architecture with 3-4 inter-service calls per request IS a distributed monolith. |
| V4 | FAIL | Does not identify the entity trap. Treats each service as a legitimate bounded context. |
| V5 | PARTIAL | Doesn't change data ownership. Suggests Redis caching of cross-service data, which adds complexity without fixing the root cause. |
| V6 | FAIL | No integrator/disintegrator conflict resolution. |
| V7 | FAIL | Does not address sagas at all. |

**Score: 0.5/12 (4%)**

---

## Eval 3: E-Commerce Distributed Transaction Design

**Prompt:** "We're designing a new e-commerce platform with microservices. When a customer places an order, we need to: reserve inventory, charge payment, and create a shipment. If payment fails after inventory is reserved, we need to release it. How do we handle this transaction across services?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | All 6 disintegrators evaluated for Inventory, Payment, and Shipping. Scalability (10x for browse-time inventory) and Security (PCI for payment) identified as driving forces. |
| S2 | PASS | Integrators evaluated in a matrix format for all 3 service pairs. Inventory-Payment has transaction integrator but disintegrators override. |
| S3 | PASS | 4 workflows mapped: place order (orchestration), browse inventory (N/A), track shipment (choreography), refund (orchestration). Clear reasoning for each. |
| S4 | PASS | Complete saga design: 3-step do/undo table, state machine diagram, error handling matrix covering all failure points including "undo itself fails." Pending state table structure shown. TTL/timeout per step. |
| S5 | PASS | Full ratings table. Notes Performance (2) as risk with quantification: "saga adds ~200ms to order placement." |
| V1 | PASS | First evaluates whether services should be separate at all: "Before designing a distributed transaction, the first question is: should these be separate services at all?" Then justifies separation with specific disintegrators. |
| V2 | PASS | Keeps architecture at 4 services (not splitting inventory into browse/checkout, not splitting shipping into label/tracking). Notes 25% workflows need saga, under 30% threshold. |
| V3 | PASS | Anti-pattern checklist completed. Each service owns its data, deploys independently. |
| V4 | PASS | Services model business capabilities: "Stock management" not "inventory table." |
| V5 | PASS | Explicit data isolation. No shared databases. |
| V6 | PASS | Transaction integrator (Inventory-Payment) overridden by security disintegrator with quantified justification: "PCI audit cost savings ($50k-100k/year) justify the saga implementation cost." |
| V7 | PASS | Notes 1 of 4 workflows needs saga (25%). Includes critical warning: "if the team finds themselves adding more sagas for additional workflows, this is a signal that the granularity should be re-evaluated." |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | FAIL | No disintegrator analysis. Assumes services are separate without evaluating why. |
| S2 | FAIL | No integrator analysis. Doesn't evaluate whether the transaction need suggests services should be merged. |
| S3 | PARTIAL | Chooses "event-driven choreographed saga" but doesn't compare with orchestration or reason about the trade-offs. Choreography is actually a poor fit here (3 services with compensating transactions = complex distributed error handling). |
| S4 | PARTIAL | Describes the saga flow (happy path and failure path) but: no explicit do/undo table, no pending state management design, no error handling for failed compensations, no timeout/TTL specification. Mentions "dead letter queue" without designing it. |
| S5 | FAIL | No characteristic ratings. |
| V1 | FAIL | Never asks "should these be separate services?" Jumps directly to saga implementation without evaluating granularity. |
| V2 | PASS | Keeps services at a reasonable count (4). |
| V3 | FAIL | No distributed monolith check. |
| V4 | PASS | Services are named by business capability (OrderService, InventoryService, PaymentService, ShippingService). |
| V5 | PASS | States "PostgreSQL per service." |
| V6 | FAIL | No integrator/disintegrator analysis to resolve. |
| V7 | FAIL | Saga used without questioning whether it's the right approach. No sparingness check. |

**Score: 4/12 (33%)**

---

## Summary

| Eval | Prompt | With Skill | Without Skill | Delta |
|:----:|--------|:----------:|:-------------:|:-----:|
| 1 | Monolith decomposition (Order service) | **12/12 (100%)** | 0.5/12 (4%) | +96% |
| 2 | Over-split diagnosis (User service) | **12/12 (100%)** | 0.5/12 (4%) | +96% |
| 3 | Distributed transaction design (e-commerce) | **12/12 (100%)** | 4/12 (33%) | +67% |
| **Average** | | **12/12 (100%)** | **1.67/12 (14%)** | **+86%** |

## Key Findings

### What the skill consistently adds:

1. **Systematic disintegrator/integrator analysis:** With-skill outputs evaluate every service against 6 disintegrators and every service pair against 4 integrators with specific evidence and scores. Without-skill outputs split services based on entity names or arbitrary conventions without structured evaluation.

2. **"Fix granularity, not transactions" principle:** With-skill outputs always ask "should these be separate services?" BEFORE designing distributed transactions. In Eval 2, this principle directly led to merging 5 services into 3, eliminating a saga entirely. Without-skill outputs never question whether the service boundaries are correct.

3. **Over-splitting detection and correction:** With-skill outputs identified over-splitting in Eval 2 and recommended merging (5 -> 3 services), quantifying the performance improvement (16x faster registration, 5x faster profile views). Without-skill output recommended adding MORE infrastructure (BFF, Redis, GraphQL) to work around the wrong granularity rather than fixing the root cause.

4. **Complete saga design:** When sagas are genuinely necessary, with-skill outputs produce complete designs with do/undo tables, state machines, error handling for failed compensations, TTLs, and pending state management. Without-skill outputs describe saga flows at a high level without the implementation details needed for production systems.

5. **Bounded context awareness:** With-skill outputs model services as bounded contexts (workflows/capabilities), not entities. Without-skill outputs fall into the entity trap (separate ShippingLabel vs ShippingTracking services, separate OrderCreation vs OrderValidation services).

### Without-skill failure patterns:

- **Never questions granularity:** In all 3 evals, without-skill outputs accepted the service boundaries as given and never asked whether they were correct. This is the fundamental failure -- granularity optimization requires questioning boundaries.
- **Adds infrastructure instead of fixing architecture:** When services are over-split (Eval 2), without-skill adds caching, BFF, and GraphQL layers rather than merging services. This adds complexity without addressing the root cause.
- **Incomplete saga designs:** Without-skill describes saga flows but omits critical implementation details: compensating operations, pending state, failed-undo handling, timeout management.
- **No characteristic validation:** Never validates the design against the architecture style's known strengths and weaknesses.
