# Service-Based Architecture Design: Food Delivery Platform

## Design Context
**System:** Food delivery platform covering order management, restaurant integration, delivery tracking, notifications, and payments
**Team:** 8 developers, no microservices experience
**Key drivers:** Team is small and inexperienced with distributed systems; need distribution benefits (independent deployment, fault isolation) without microservices complexity; service-based is the ideal "first distributed architecture"

## Is Service-Based Right?

**Yes.** Here's why:

| Factor | Assessment |
|--------|-----------|
| Team size (8) | Too small for microservices (need 20+ for proper DevOps). Service-based sweet spot. |
| Distributed experience (none) | Service-based is the simplest distributed style (simplicity=3, cost=4). Start here. |
| Domain decomposition | 5 clear business domains map naturally to 5 coarse-grained services |
| Transaction needs | Order + Payment must be atomic — service-based preserves this with shared DB |
| Scalability needs | Moderate — dinner rush is predictable, not extreme elasticity (elasticity=2 is acceptable) |

**Why not microservices:** Team of 8 with no distributed experience would produce a distributed monolith — tightly coupled services that must deploy in lockstep, with none of the benefits and all of the complexity. Service-based gives you independent deployability (4 stars) and fault tolerance (4 stars) at a fraction of the operational cost.

**Why not monolith:** Deployment coupling is a real problem for delivery platforms — a bug in notifications shouldn't block deploying a payment fix. Independent deployability matters here.

## Domain Services (5 services)

| # | Service | Domain | Key Components | Instances |
|---|---------|--------|---------------|:---------:|
| 1 | OrderService | Order lifecycle management | Order Creation, Order Validation, Cart Management, Order Status, Order History | 2 (dinner rush) |
| 2 | RestaurantService | Restaurant integration & menus | Restaurant Profiles, Menu Management, Availability, Restaurant Onboarding, Prep Time Estimation | 1 |
| 3 | DeliveryService | Delivery logistics & tracking | Driver Assignment, Route Optimization, Real-time Tracking, Delivery Confirmation, Driver Management | 2 (dinner rush) |
| 4 | NotificationService | All platform notifications | Push Notifications, SMS, Email, In-app Messages, Notification Preferences | 1 |
| 5 | PaymentService | All financial transactions | Payment Processing, Refunds, Restaurant Payouts, Driver Payouts, Transaction History | 1 |

### Service Detail: OrderService
**Domain:** Complete order lifecycle from cart to completion
**Internal design:** Domain-partitioned (API facade + sub-domain components)
**Components:**
- Cart Manager: Shopping cart, item selection, customization
- Order Validator: Checks restaurant availability, delivery zone, minimum order
- Order Orchestrator: The API facade that coordinates the full checkout flow — validates order, processes payment (via shared DB), updates restaurant queue, assigns delivery
- Order Status Manager: Tracks order through stages (placed, preparing, picked up, delivered)
- Order History: Past orders, reorder functionality

**Critical design decision:** The OrderService handles the entire checkout orchestration INTERNALLY. When a customer places an order, the OrderService's API facade:
1. Validates the order (internal component call)
2. Processes payment by writing to payment tables in shared DB (ACID transaction)
3. Updates restaurant queue by writing to restaurant tables in shared DB (same ACID transaction)
4. Initiates delivery assignment by writing to delivery tables in shared DB (same ACID transaction)

This all happens in ONE database transaction. In microservices, this would be 4 separate service calls requiring SAGA. With service-based architecture and a shared DB, it's a single ACID commit.

### Service Detail: DeliveryService
**Domain:** Everything related to getting food from restaurant to customer
**Internal design:** Layered (API facade -> business logic -> persistence)
**Components:**
- Driver Manager: Driver profiles, availability, shift management
- Assignment Engine: Matches available drivers to orders based on proximity and load
- Route Optimizer: Calculates optimal delivery routes
- Tracking Engine: Real-time GPS tracking and ETA updates
- Confirmation Handler: Delivery confirmation, photo proof

## Database Topology
**Strategy:** Logically partitioned shared database
**Reasoning:** Order placement MUST atomically update order records, payment records, and restaurant queue. This is the core business workflow and it spans 3 domains. A shared database makes this a single ACID transaction. Splitting the database would force SAGA pattern for the most critical business operation — unacceptable risk for a team with no distributed systems experience.

**Logical partitions:**

| Partition | Key Tables | Used by services |
|-----------|-----------|-----------------|
| order | orders, order_items, order_status, cart | OrderService |
| restaurant | restaurants, menus, menu_items, availability, prep_queue | RestaurantService, OrderService |
| delivery | drivers, delivery_assignments, routes, tracking_events | DeliveryService, OrderService |
| payment | transactions, refunds, payouts, payment_methods | PaymentService, OrderService |
| notification | notification_queue, templates, preferences, delivery_log | NotificationService |
| common | users, addresses, zones, audit_log | All services |

**Entity libraries:**
- `order_entities_lib` — OrderService
- `restaurant_entities_lib` — RestaurantService, OrderService (read for validation/queue updates)
- `delivery_entities_lib` — DeliveryService, OrderService (write for assignment initiation)
- `payment_entities_lib` — PaymentService, OrderService (write for payment processing)
- `notification_entities_lib` — NotificationService
- `common_entities_lib` — all services

## User Interface Topology
**Strategy:** Domain-based UIs (2 UIs)
**Reasoning:** Two distinct user groups with very different needs: (1) Customer-facing app (mobile + web) for ordering and tracking, (2) Operations dashboard (web) for restaurant management, driver management, and reporting. These have different availability requirements — the customer app needs 99.9% uptime during meal times, while the ops dashboard can tolerate brief outages.

**UI breakdown:**
- **Customer App** (mobile + web): Order placement, delivery tracking, payment, order history -> Consumes OrderService, DeliveryService, PaymentService
- **Operations Dashboard** (web): Restaurant onboarding, menu management, driver management, order monitoring, reports -> Consumes all 5 services

## API Layer
**Decision:** Include
**Reasoning:** The customer-facing mobile app and web app both consume the same services. An API layer (API gateway) centralizes authentication, rate limiting, and provides a stable contract for the mobile app (mobile apps can't be updated as easily as web frontends). Also needed for restaurant partner API access.

## Transaction Boundaries

| Workflow | Domains involved | Services | Transaction type | Notes |
|----------|-----------------|----------|:----------------:|-------|
| Place order | order, payment, restaurant, delivery | OrderService (orchestrates internally) | ACID | **Core transaction.** OrderService writes to order + payment + restaurant + delivery tables atomically via shared DB |
| Cancel order + refund | order, payment | OrderService, PaymentService | ACID | Shared DB: atomic order cancellation + refund creation |
| Update menu | restaurant | RestaurantService | ACID | Self-contained |
| Assign driver | delivery | DeliveryService | ACID | Self-contained |
| Update tracking | delivery | DeliveryService | ACID | Self-contained |
| Send notification | notification | NotificationService | ACID | Self-contained; can be eventually consistent (fire-and-forget from other services via DB queue table) |
| Process restaurant payout | payment, restaurant | PaymentService | ACID | Shared DB enables atomic payout + reconciliation |

## Architecture Quanta
**Count:** 2
**Reasoning:**
- **Quantum 1 — Customer-facing:** Customer App UI + OrderService + DeliveryService + PaymentService + shared DB. Needs high availability during meal times, scales for dinner rush.
- **Quantum 2 — Operations:** Ops Dashboard UI + RestaurantService + NotificationService + shared DB. Lower availability requirements, doesn't need rush-hour scaling.

Note: Both quanta share the same database, so the quantum separation is driven by UI and service instance differences rather than data separation.

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | Yes — fix a payment bug without redeploying order tracking |
| Elasticity | 2 | Acceptable — dinner rush is predictable; scale OrderService + DeliveryService to 2 instances |
| Fault tolerance | 4 | Yes — NotificationService outage doesn't block order placement |
| Modularity | 4 | Yes — restaurant integration changes don't affect payment processing |
| Overall cost | 4 | Yes — 8-person team can't afford microservices infrastructure |
| Performance | 3 | Acceptable — food delivery latency tolerance is seconds, not milliseconds |
| Reliability | 4 | Yes — fewer network calls than microservices = fewer failure points |
| Simplicity | 3 | Best distributed option for a team with no distributed experience |
| Testability | 4 | Yes — test PaymentService independently with mock order data |

## Anti-Pattern Check
- [x] Service count in 4-12 range (5 services)
- [x] No inter-service direct calls (OrderService orchestrates by writing to shared DB tables, not by calling PaymentService API)
- [x] Database topology supports required ACID transactions (shared DB preserves order-payment-restaurant atomicity)
- [x] Federated entity libraries (6 domain-scoped + common)
- [x] No premature database splitting (team is inexperienced; shared DB is the safe choice)

## Getting Started
1. Define the 6 logical database partitions and create the federated entity libraries — establish clean domain boundaries from day one
2. Implement OrderService first — it's the core business value and the most complex service; proving the checkout ACID transaction works validates the entire architecture
3. Set up 2 deployment pipelines: one for customer-facing services (OrderService, DeliveryService, PaymentService) and one for operations services (RestaurantService, NotificationService, ReportingService) — this maps to the 2 architecture quanta

## Evolution Path

As the team gains distributed experience and the platform grows:
- **Phase 1 (now):** 5 services, shared DB, team of 8
- **Phase 2 (12-18 months):** If delivery tracking needs real-time WebSocket scaling, DeliveryService can be extracted into its own quantum with a separate tracking database. NotificationService can get its own DB (fire-and-forget pattern, no ACID needed with other services).
- **Phase 3 (future):** If the platform reaches millions of users and the team grows to 30+, evaluate migrating to microservices for the highest-traffic services (orders, tracking). The domain boundaries established in Phase 1 become the microservice boundaries.
