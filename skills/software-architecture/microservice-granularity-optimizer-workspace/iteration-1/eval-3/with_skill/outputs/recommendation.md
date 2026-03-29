# Microservice Granularity Report: E-Commerce Order Transaction Design

## Context
**Scenario:** New e-commerce platform with microservices. Order placement requires: reserve inventory, charge payment, create shipment. If payment fails after inventory is reserved, inventory must be released.

## Step 1: Evaluate Whether Separate Services Are Justified

Before designing a distributed transaction, the first question is: should these be separate services at all? Applying the transaction integrator rule: "Don't do transactions in microservices -- fix granularity instead!"

### Integrator Analysis: Inventory + Payment + Shipping

| Integrator | Inventory-Payment | Inventory-Shipping | Payment-Shipping |
|-----------|:-:|:-:|:-:|
| Database transactions | YES (reserve must be atomic with charge) | NO (shipping is post-confirmation) | NO (independent) |
| Workflow coupling | MODERATE (payment triggers reservation confirmation) | LOW (async post-order) | LOW (independent) |
| Shared code | NO | NO | NO |
| Data relationships | LOW (payment needs order amount, not inventory data) | LOW (shipping needs item dimensions) | NO |

### Disintegrator Analysis

| Disintegrator | Inventory | Payment | Shipping |
|--------------|:-:|:-:|:-:|
| Scope/function | Stock management (browse + checkout) | Payment processing | Shipment creation + tracking |
| Code volatility | Low | Low | Medium (new carriers) |
| Scalability | HIGH -- inventory checks at browse-time need 10x+ more instances than checkout | Moderate | Low |
| Fault tolerance | Critical for orders | Critical for orders | Non-critical (can retry) |
| Security | Standard | HIGH (PCI DSS scope) | Standard |
| Extensibility | Stable | Stable | Growing (new carriers, methods) |

### Decision: Keep Separate

**Reasoning:**
1. **Scalability disintegrator (Inventory):** Inventory checks happen both at browse-time (high volume) and checkout-time (low volume). If merged with Payment, the combined service must scale to browse-time levels even though payment logic is only needed at checkout.
2. **Security disintegrator (Payment):** Payment handles PCI-scoped data. Merging with Inventory would put all inventory code in PCI scope, increasing audit surface and compliance cost.
3. **These disintegrators override the transaction integrator** because (a) the scalability difference is significant (10x+) and (b) PCI scope reduction has concrete cost benefits.

**Consequence:** We accept the need for a distributed transaction (saga) for the order placement workflow. This is one of the legitimate exceptions.

## Step 2: Saga Design -- Order Placement

### Saga: Place Order (Orchestrated)

**Why orchestration over choreography:**
- 3 services with compensating transactions = complex error handling
- Need full visibility into transaction state for customer support
- Compensating actions have ordering dependencies (must release inventory before canceling shipment)

**Mediator:** OrderService (dedicated orchestrator for order lifecycle)

| Step | Service | Do operation | Undo operation | Pending state |
|:----:|---------|-------------|----------------|:-------------:|
| 1 | InventoryService | `reserve_items(items, order_id)` -> returns `reservation_id` | `release_reservation(reservation_id)` | INVENTORY_PENDING -> INVENTORY_RESERVED |
| 2 | PaymentService | `charge_payment(amount, payment_method, order_id)` -> returns `transaction_id` | `refund_payment(transaction_id)` | PAYMENT_PENDING -> PAYMENT_CHARGED |
| 3 | ShippingService | `create_shipment(order_id, items, address)` -> returns `shipment_id` | `cancel_shipment(shipment_id)` | SHIPPING_PENDING -> SHIPPING_CREATED |

### Saga State Machine

```
INITIATED
    |
    v
INVENTORY_RESERVED  ----[inventory fails]----> FAILED (no compensation needed)
    |
    v
PAYMENT_CHARGED     ----[payment fails]------> COMPENSATING
    |                                               |
    v                                               v
SHIPPING_CREATED    ----[shipping fails]----> COMPENSATING
    |                                               |
    v                                               v
CONFIRMED                                    release_reservation()
                                                    |
                                                    v
                                              FAILED (compensated)
```

### Error Handling Matrix

| Failure point | Compensation needed | Actions |
|--------------|:---:|---------|
| Step 1 (Inventory) fails | None | Return error: "Out of stock" |
| Step 2 (Payment) fails | Release inventory | Call `release_reservation(reservation_id)`. Return error: "Payment declined" |
| Step 3 (Shipping) fails | Refund payment + release inventory | Call `refund_payment(transaction_id)`, then `release_reservation(reservation_id)`. Return error: "Cannot ship to this address" |
| Step 2 undo (refund) fails | CRITICAL | Log alert, add to manual resolution queue. Do NOT release inventory until refund is confirmed (customer was charged). Retry refund with exponential backoff. |
| Step 1 undo (release) fails | Moderate | Retry release. Inventory will auto-expire reservation after TTL (30 min). Log warning. |

### Pending State Management

OrderService maintains a `saga_state` table:

```
order_id | step | status | external_id | created_at | updated_at
---------|------|--------|-------------|-----------|----------
ORD-123  | 1    | COMPLETED | RES-456  | ...       | ...
ORD-123  | 2    | COMPLETED | TXN-789  | ...       | ...
ORD-123  | 3    | PENDING   | null     | ...       | ...
```

**TTL/timeout per step:**
- Inventory reservation: 30s timeout, auto-release after 15 min
- Payment charge: 45s timeout, requires explicit undo
- Shipping creation: 30s timeout, can retry

## Step 3: Communication Design

| Workflow | Pattern | Reasoning |
|----------|---------|-----------|
| Place order | **Orchestration** (saga) | Complex 3-service workflow with compensating transactions. OrderService mediates. |
| Browse inventory | **No inter-service comm** | InventoryService handles directly. |
| Track shipment | **Choreography** | ShippingService publishes tracking events, NotificationService subscribes. |
| Refund order | **Orchestration** (saga) | Reverse saga: refund payment, release inventory, cancel shipment. |

## Step 4: Anti-Pattern Check

- [x] No shared databases -- each service owns its data
- [x] Not over-granular -- 1 of 4 workflows needs saga (25%, under 30% threshold)
- [x] No entity trap -- services model business capabilities, not entities
- [x] Data isolation maintained -- InventoryService doesn't read PaymentService's DB
- [x] Saga used sparingly -- only for the order placement/refund workflows where separate services are justified by strong disintegrators

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | Yes |
| Elasticity | 5 | Yes -- InventoryService scales independently for browse-time |
| Fault tolerance | 4 | Yes -- shipping failure doesn't block orders |
| Scalability | 5 | Yes -- key driver for keeping Inventory separate |
| Performance | 2 | Risk -- saga adds ~200ms to order placement. Acceptable for checkout flow (not real-time). |
| Overall cost | 1 | Accepted -- saga infrastructure is the price of PCI isolation + scaling |
| Simplicity | 1 | Risk -- saga is the most complex element. Well-documented state machine mitigates. |

## Key Trade-offs Documented

1. **Saga complexity vs PCI scope reduction:** Accepted. PCI audit cost savings ($50k-100k/year) justify the saga implementation cost.
2. **Eventual consistency vs scalability:** Accepted. Inventory checks at browse-time need 10x scaling independent of payment processing.
3. **Orchestration coupling vs distributed error handling:** Chose orchestration. Centralized error handling for compensating transactions is worth the mediator coupling.

## Critical Warning
If the team finds themselves adding more sagas for additional workflows (e.g., "apply coupon + charge payment + update loyalty points"), this is a signal that the granularity should be re-evaluated. The saga for order placement is justified by strong disintegrators. Additional sagas should trigger a revisit of service boundaries.
