# Grading: service-based-architecture-designer — Iteration 1

## Assertions

### Structural Assertions
| ID | Assertion | Description |
|----|-----------|-------------|
| S1 | identifies-domain-services | Identifies specific domain services (4-12 range) with clear business capability boundaries |
| S2 | specifies-database-topology | Makes an explicit database topology decision (shared/partitioned/per-service) with reasoning |
| S3 | maps-transaction-boundaries | Maps business workflows to transaction types (ACID vs BASE) based on service and database boundaries |
| S4 | specifies-ui-topology | Specifies user interface topology variant (single/domain-based/service-based) |
| S5 | addresses-api-layer | Makes an explicit decision about whether to include an API layer with reasoning |

### Value Assertions
| ID | Assertion | Description |
|----|-----------|-------------|
| V1 | service-count-4-12 | Recommends 4-12 coarse-grained services (not dozens of fine-grained microservices), with clear domain scope per service |
| V2 | uses-logical-partitioning | Recommends or evaluates logical database partitioning with federated domain-scoped entity libraries rather than a single shared entity library |
| V3 | preserves-acid-through-granularity | Explains how coarse service granularity preserves ACID transactions by keeping related operations within a single service |
| V4 | no-inter-service-calls | States or enforces that domain services should not call each other directly — orchestration is internal or through UI/API layer |
| V5 | warns-premature-db-split | Warns against premature database splitting and recommends starting with shared DB, splitting only when proven necessary |
| V6 | checks-anti-patterns | Checks for service-based anti-patterns: too many services (>12), too few (<3), premature DB splitting, inter-service communication, single shared entity library |
| V7 | uses-star-ratings | References specific characteristic ratings (Deploy=4, Elast=2, FaultTol=4, etc.) to validate the design against the style's known strengths and weaknesses |

---

## Eval 1: Healthcare Patient Management System

**Prompt:** "We're a team of 15 developers building a healthcare patient management system. We need patient registration, appointment scheduling, medical records, billing, and lab results. Deployment takes 3 hours. We need ACID transactions between billing and medical records. Design a service-based architecture for us."

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | 5 services identified: PatientService, SchedulingService, ClinicalService, BillingService, LabService — all with components listed |
| S2 | PASS | Logically partitioned shared database with 6 domain partitions + common; includes entity library breakdown |
| S3 | PASS | 7 workflows mapped with ACID/BASE designation; billing-clinical ACID explicitly addressed |
| S4 | PASS | Single monolithic UI chosen with reasoning (single user group) |
| S5 | PASS | API layer included with reasoning (HIPAA compliance, external integrations) |
| V1 | PASS | 5 services in 4-12 range; each represents complete domain |
| V2 | PASS | Federated entity libraries: 6 domain-scoped + common; explicitly warns against single shared library |
| V3 | PASS | Explains billing-clinical ACID is preserved because both use shared DB; contrasts with microservices needing SAGA |
| V4 | PASS | States "all coordination through shared DB or UI" in anti-pattern check |
| V5 | PASS | Shared DB chosen explicitly to preserve billing-clinical ACID; no premature splitting |
| V6 | PASS | Anti-pattern checklist: service count, inter-service calls, DB topology, federated libraries, no premature split |
| V7 | PASS | Characteristic ratings table with Deploy=4, Elast=2, FaultTol=4, etc.; maps to system needs |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | FAIL | 12 services listed — too fine-grained (Clinical Notes, Claims, Payment, Lab Order, Lab Results are separate). This is microservices, not service-based |
| S2 | FAIL | "Each service should have its own database" — recommends per-service DBs without reasoning about ACID implications |
| S3 | FAIL | Proposes SAGA for billing-medical records despite user explicitly requesting ACID. SAGA adds complexity and only provides eventual consistency |
| S4 | FAIL | No UI topology discussed |
| S5 | PARTIAL | Mentions API Gateway but doesn't reason about whether to include one |
| V1 | FAIL | 12 services — at the boundary and several are too fine-grained (separate Claims, Payment, Lab Order, Lab Results) |
| V2 | FAIL | Per-service databases; no mention of logical partitioning or entity libraries |
| V3 | FAIL | Does not explain ACID preservation through granularity; instead proposes SAGA which sacrifices ACID |
| V4 | FAIL | Implies inter-service communication ("Saga orchestrator sends charge capture event to Billing Service") |
| V5 | FAIL | Recommends per-service databases from the start — the opposite of starting shared |
| V6 | FAIL | No anti-pattern checks |
| V7 | FAIL | No characteristic ratings |

**Score: 0.5/12 (4%)**

---

## Eval 2: HR Platform

**Prompt:** "We have an HR platform with employee management, payroll, benefits, time tracking, and reporting. Payroll needs high availability during pay periods. We want a shared database but might split later. How should we design the services and database topology?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | 5 services: EmployeeService, PayrollService, BenefitsService, TimeTrackingService, ReportingService |
| S2 | PASS | Logically partitioned shared DB; includes future split migration path with specific candidates and order |
| S3 | PASS | 7 workflows mapped; payroll-time-benefits ACID preserved through shared DB |
| S4 | PASS | Single monolithic UI with role-based access reasoning |
| S5 | PASS | API layer included for external integrations (payroll providers, benefits carriers) |
| V1 | PASS | 5 services, each covers a complete business domain |
| V2 | PASS | 6 domain-scoped entity libraries + common; detailed partition table |
| V3 | PASS | "Pay run processing" ACID: PayrollService reads time/benefits data via shared DB joins, writes pay records atomically |
| V4 | PASS | Explicitly: "PayrollService reads time/benefits through shared DB, not by calling TimeTrackingService" |
| V5 | PASS | "No premature database splitting"; provides migration path with specific split order and reasoning |
| V6 | PASS | Anti-pattern checklist completed |
| V7 | PASS | Characteristic ratings table with specific star values and "meets needs" assessment |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | 5 services identified matching the domains |
| S2 | PARTIAL | Mentions shared database with schema prefixes, but doesn't detail logical partitioning structure or entity libraries |
| S3 | FAIL | Says "Use database transactions for pay calculations" but doesn't map specific workflows to ACID/BASE |
| S4 | FAIL | No UI topology discussed |
| S5 | FAIL | No API layer discussion |
| V1 | PASS | 5 services in range |
| V2 | FAIL | Mentions "schema prefixes" but no federated entity libraries; suggests "database views to abstract table access" which is not the book's approach |
| V3 | FAIL | No explanation of how coarse granularity preserves ACID |
| V4 | FAIL | Data flow diagram shows bidirectional arrows between services (Employee ←→ Payroll, Benefits ←→ Time Tracking), implying inter-service communication |
| V5 | PARTIAL | Starts with shared DB (good), but doesn't warn against premature splitting — presents splitting as a straightforward migration |
| V6 | FAIL | No anti-pattern checks |
| V7 | FAIL | No characteristic ratings |

**Score: 2.5/12 (21%)**

---

## Eval 3: Food Delivery Platform

**Prompt:** "We're building a food delivery platform with order management, restaurant integration, delivery tracking, notifications, and payments. Team of 8, never done microservices. Is service-based right, and how should we design it?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | PASS | 5 services: OrderService, RestaurantService, DeliveryService, NotificationService, PaymentService — all with detailed components |
| S2 | PASS | Logically partitioned shared DB; 6 partitions detailed with which services use which |
| S3 | PASS | 7 workflows mapped; order placement ACID transaction explained in detail (order + payment + restaurant + delivery in one commit) |
| S4 | PASS | Domain-based UIs: Customer App + Operations Dashboard with reasoning |
| S5 | PASS | API layer included for mobile app stability and restaurant partner access |
| V1 | PASS | 5 services; explicit "why not microservices" analysis (team of 8, no experience → distributed monolith risk) |
| V2 | PASS | 6 domain-scoped entity libraries + common |
| V3 | PASS | Detailed explanation: OrderService handles checkout INTERNALLY — "validates order, processes payment by writing to payment tables in shared DB (ACID transaction)... In microservices, this would be 4 separate service calls requiring SAGA" |
| V4 | PASS | "OrderService orchestrates by writing to shared DB tables, not by calling PaymentService API" |
| V5 | PASS | "team is inexperienced; shared DB is the safe choice"; evolution path shows when splitting becomes appropriate |
| V6 | PASS | Anti-pattern checklist + evolution path showing how to avoid drifting into premature splitting |
| V7 | PASS | Full characteristic ratings table with star values and fit assessment |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|----------|
| S1 | FAIL | 13 services — explicitly over the 12 service-based maximum. Recommends microservices despite being asked about service-based |
| S2 | FAIL | Per-service databases (PostgreSQL, MongoDB, Redis, Elasticsearch) — opposite of service-based approach |
| S3 | FAIL | Proposes SAGA for order-payment consistency; doesn't map workflows systematically |
| S4 | FAIL | No UI topology discussion |
| S5 | PARTIAL | Mentions Kong API Gateway but doesn't reason about the decision |
| V1 | FAIL | 13 services, fine-grained (separate Cart, Search, Promotion, Rating, Analytics services) — this is microservices |
| V2 | FAIL | Per-service databases with different DB technologies; no logical partitioning |
| V3 | FAIL | Does not preserve ACID — explicitly proposes SAGA (eventual consistency) for order-payment |
| V4 | FAIL | Event-driven communication between services via Kafka — the opposite of self-contained services |
| V5 | FAIL | Recommends per-service databases from the start |
| V6 | FAIL | No anti-pattern checks; actually exhibits the "too many services" anti-pattern |
| V7 | FAIL | No characteristic ratings |

**Score: 0.5/12 (4%)**

---

## Summary

| Eval | Prompt | With Skill | Without Skill | Delta |
|:----:|--------|:----------:|:-------------:|:-----:|
| 1 | Healthcare (ACID + 15 devs) | **12/12 (100%)** | 0.5/12 (4%) | +96% |
| 2 | HR Platform (shared DB + HA payroll) | **12/12 (100%)** | 2.5/12 (21%) | +79% |
| 3 | Food Delivery (team of 8, no experience) | **12/12 (100%)** | 0.5/12 (4%) | +96% |
| **Average** | | **12/12 (100%)** | **1.17/12 (10%)** | **+90%** |

## Key Findings

### What the skill consistently adds:

1. **Correct service granularity:** With-skill outputs always recommend 4-12 coarse-grained domain services. Without-skill outputs drift toward microservices (12-13 fine-grained services) even when the user explicitly asks for service-based architecture.

2. **Database partitioning sophistication:** With-skill outputs use the logically-partitioned shared database with federated entity libraries — a specific technique from Chapter 13 that general agents don't know. Without-skill outputs either recommend per-service databases (microservices pattern) or vaguely mention "schema prefixes."

3. **ACID preservation through granularity:** With-skill outputs explain HOW coarse-grained services preserve ACID by keeping related operations within one service. Without-skill outputs default to SAGA/eventual consistency even when the user explicitly needs ACID — actively working against the user's stated requirement.

4. **No inter-service communication rule:** With-skill outputs enforce that domain services don't call each other. Without-skill outputs consistently show inter-service communication (events, REST calls, bidirectional arrows), which defeats the purpose of service-based architecture.

5. **Anti-pattern awareness:** With-skill outputs check for all known anti-patterns. Without-skill outputs sometimes exhibit the anti-patterns they should be preventing (too many services, premature DB splitting).

### Without-skill failure patterns:

- **Defaults to microservices:** In 2 of 3 evals, the without-skill output recommended microservices architecture (or event-driven microservices) instead of service-based, even when the user explicitly asked for service-based.
- **Ignores team constraints:** Recommends Kubernetes, Kafka, service mesh, distributed tracing to a team of 8 with no distributed experience.
- **No topology variant awareness:** Never discusses UI topology options, database partitioning strategies, or API layer as explicit decisions.
- **No quantitative validation:** Never references characteristic star ratings to validate the design.
