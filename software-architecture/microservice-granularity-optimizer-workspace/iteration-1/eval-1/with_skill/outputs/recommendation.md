# Microservice Granularity Report: Order Processing System

## Current State
**Services:** 1 (monolithic Order service)
**Key pain points:** Service is too large, handles too many concerns, deployment risk is high

## Disintegrator/Integrator Analysis

### Service: OrderService (monolith)
**Current scope:** Order creation, inventory checks, payment processing, shipping label generation, email notifications

| Disintegrator | Applies? | Evidence |
|--------------|:--------:|----------|
| Service scope/function | YES | Service handles 5 distinct business capabilities: orders, inventory, payments, shipping, notifications. Cannot describe in one sentence without "and." |
| Code volatility | YES | Email templates and notification rules change weekly. Order creation logic changes monthly. Shipping label format is stable (changes quarterly). |
| Scalability | YES | Payment processing needs 2x instances during sales events. Email notifications need 10x instances for batch sends. Inventory checks need consistent low-latency. |
| Fault tolerance | YES | If email notifications fail, order processing should continue. If shipping label generation has an error, the order should still be placed. |
| Security | YES | Payment processing handles PCI-scoped data (card numbers, CVV). Order creation handles PII but not payment card data. Notifications handle email addresses only. |
| Extensibility | YES | Notifications are growing rapidly (SMS, push, in-app) while order creation is stable. |
| **Disintegrator score** | **6/6** | Strong candidate for splitting |

### Proposed Split Analysis

**Candidate services after disintegrator analysis:** OrderProcessing, InventoryService, PaymentService, ShippingService, NotificationService

Now applying integrators to test whether any should stay together:

### Service Pair: OrderProcessing + InventoryService

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | YES | Placing an order must atomically reserve inventory. If order creation succeeds but inventory reservation fails, we have phantom orders. |
| Workflow coupling | MODERATE | Every order creation checks inventory, but inventory is also checked during browsing (independent use case). |
| Shared code | NO | Different business logic. |
| Data relationships | MODERATE | Order needs current stock count, but inventory has independent lifecycle. |
| **Integrator score** | **1.5/4** | |

**Decision:** SPLIT, but carefully. The transaction integrator is present but inventory also serves independent use cases (browse-time stock checks). The scalability disintegrator (inventory checks at browse-time need more instances than order processing) outweighs the transaction integrator. Use an orchestrated saga for the order placement workflow.

### Service Pair: OrderProcessing + PaymentService

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | YES | Payment must be atomic with order -- charge must succeed or order must not be created. |
| Workflow coupling | YES | Every order requires payment. Payment never happens without an order. |
| Shared code | NO | Different business logic, different SDKs. |
| Data relationships | MODERATE | Order needs payment confirmation, payment needs order amount. |
| **Integrator score** | **2.5/4** | |

**Decision:** Normally the integrators would favor merging, but the security disintegrator is very strong (PCI scope). Keeping payment separate reduces PCI audit scope to one service instead of the entire order system. **Accept the saga complexity to gain security isolation.** This is one of the valid exceptions to "don't do transactions in microservices."

### Service Pair: OrderProcessing + ShippingService

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | NO | Shipping label can be generated after order is confirmed. Eventual consistency is acceptable. |
| Workflow coupling | LOW | Shipping is triggered after order completion, not during. |
| Shared code | NO | Different business logic. |
| Data relationships | LOW | Shipping needs order address and items, but only once per order. |
| **Integrator score** | **0/4** | |

**Decision:** SPLIT. No integrators apply. Shipping can be triggered asynchronously after order confirmation.

### Service Pair: OrderProcessing + NotificationService

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | NO | Notifications are fire-and-forget. |
| Workflow coupling | NO | Notifications are triggered by events, not synchronous calls. |
| Shared code | NO | Different logic entirely. |
| Data relationships | LOW | Needs order details, but can receive via event payload. |
| **Integrator score** | **0/4** | |

**Decision:** SPLIT. Zero integrators. Different scalability and fault tolerance profiles. This is the clearest split candidate.

## Recommended Service Boundaries

| # | Service | Domain | Owns Data | Scales to |
|---|---------|--------|-----------|:---------:|
| 1 | OrderService | Order lifecycle (creation, validation, status, fulfillment tracking) | orders, order_items, order_status | 3-5 instances |
| 2 | InventoryService | Stock management, reservation, replenishment | inventory, reservations, warehouse_stock | 5-10 instances (browse-time checks) |
| 3 | PaymentService | Payment processing, refunds, payment methods | payments, refunds, payment_methods (PCI-isolated DB) | 2-4 instances |
| 4 | ShippingService | Label generation, carrier integration, tracking | shipments, tracking_events, carrier_configs | 1-2 instances |
| 5 | NotificationService | Email, SMS, push notifications | notification_templates, notification_log, preferences | 5-15 instances (batch sends) |

## Communication Design

| Workflow | Services involved | Pattern | Reasoning |
|----------|------------------|---------|-----------|
| Place order | Order -> Inventory -> Payment | Orchestration | Complex 3-service workflow with compensating transactions needed. OrderService acts as saga mediator. |
| Browse catalog (stock check) | Inventory only | N/A | Single service, no coordination needed. |
| Generate shipping label | Order -> Shipping | Choreography | Simple 2-service flow, async, no transaction needed. Order publishes "OrderConfirmed" event, Shipping subscribes. |
| Send notifications | Order/Shipping -> Notification | Choreography | Fire-and-forget. Multiple services publish events, Notification subscribes. |
| Process refund | Order -> Payment -> Inventory | Orchestration | Compensating transaction: must refund payment AND release reserved inventory. OrderService mediates. |

## Saga Patterns

### Saga: Place Order
| Step | Service | Do operation | Undo operation |
|:----:|---------|-------------|----------------|
| 1 | InventoryService | reserve_items(order_items) | release_reservation(reservation_id) |
| 2 | PaymentService | charge_payment(amount, method) | refund_payment(transaction_id) |
| 3 | OrderService | confirm_order(order_id) | cancel_order(order_id) |

**Coordination:** Orchestrated -- OrderService mediates
**Pending state:** OrderService tracks saga state in `order_saga_state` table: INITIATED -> INVENTORY_RESERVED -> PAYMENT_CHARGED -> CONFIRMED (or FAILED + compensations)
**Error handling:**
- If Step 2 fails: call InventoryService.release_reservation()
- If Step 2 undo fails: alert operations team + add to manual resolution queue
- If Step 1 fails: no compensation needed, return error immediately

### Saga: Process Refund
| Step | Service | Do operation | Undo operation |
|:----:|---------|-------------|----------------|
| 1 | PaymentService | refund_payment(transaction_id) | re_charge_payment(transaction_id) |
| 2 | InventoryService | release_reservation(reservation_id) | re_reserve_items(order_items) |

**Coordination:** Orchestrated -- OrderService mediates
**Pending state:** `refund_saga_state` table
**Error handling:** If payment refund succeeds but inventory release fails, proceed anyway (inventory will reconcile). Do not reverse the refund.

## Anti-Pattern Check
- [x] No shared databases between services (PaymentService has PCI-isolated DB)
- [x] No distributed monolith (each service deploys independently, owns its data)
- [x] Not over-granular (2 of 5 workflows need saga -- 40%, slightly above 30% threshold but justified by strong PCI security disintegrator)
- [x] No entity trap (services model workflows: OrderService handles order lifecycle, not just "orders" entity)
- [x] No accidental front controllers (OrderService is an explicit saga mediator, not an accidental one)
- [x] Each service can function with degradation if others fail (Notifications can queue, Shipping can retry)

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | Yes -- independent service deployment |
| Elasticity | 5 | Yes -- NotificationService scales to 15x during batch |
| Evolutionary | 5 | Yes -- notification types can evolve independently |
| Fault tolerance | 4 | Yes -- notification failure doesn't affect orders |
| Modularity | 5 | Yes -- each service is a bounded context |
| Overall cost | 1 | Acceptable -- team is prepared for infrastructure cost |
| Performance | 2 | Risk -- saga adds latency to order placement. Mitigate: timeout budgets per step |
| Reliability | 4 | Yes -- service redundancy via discovery |
| Scalability | 5 | Yes -- inventory and notifications scale independently |
| Simplicity | 1 | Risk -- team must handle saga complexity, distributed tracing |
| Testability | 4 | Yes -- small test scope per service |

## Key Trade-off Acknowledged
The Order-Payment saga is the highest-risk design element. If PCI compliance could be achieved within a combined OrderPayment service (e.g., via encryption-at-rest and column-level access controls), merging them would eliminate the saga and simplify the architecture significantly. This should be evaluated with the security team.
