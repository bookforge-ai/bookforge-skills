# Component Design: E-Commerce Platform

## Input Sufficiency Assessment

- **System purpose:** E-commerce platform (clear)
- **Actors/users:** Not explicitly listed but inferable from services: customers, admins, payment system
- **Key workflows:** Checkout workflow explicitly mentioned (spans 4 services); CRUD operations described per service
- **Existing structure:** Yes -- 5 services with 1:1 database table mapping

**Verdict:** PROCEED WITH DEFAULTS. Purpose is clear, workflows are inferable, existing structure reveals the problem.

---

## Partitioning Style

**Current:** Technical/Entity-based -- each service mirrors a database entity with CRUD operations.

**Recommended:** Domain partitioning -- organized around business workflows rather than data entities.

**Reasoning:** The current design organizes around *what the system stores* (Users, Products, Orders, Payments, Notifications). The team should organize around *what the system does* (checkout, catalog browsing, fulfillment). Domain partitioning aligns with how the business thinks, produces higher functional cohesion, and directly addresses the reported problem: a single user action (checkout) requiring 4 sequential service calls.

---

## Actors and Actions

| Actor | Actions |
|-------|---------|
| **Customer** | Browse products, search catalog, view product details, add to cart, checkout, track order, view order history, manage account, receive notifications |
| **Store Admin** | Manage product catalog (add/edit/remove products, manage categories), view sales reports, manage inventory, process refunds |
| **Payment Provider** | Process payment, confirm payment, issue refund, send payment webhook |
| **Notification System** | Send order confirmation email, send shipping update, send promotional push notification |

---

## Entity Trap Check

**DETECTED -- All 5 indicators present.**

| Indicator | Status | Evidence |
|-----------|--------|----------|
| Components named `[Entity]Service` | YES | UserService, ProductService, OrderService, PaymentService |
| Primarily CRUD operations | YES | "CRUD for users", "CRUD for products", "CRUD for orders" explicitly stated |
| 1:1 mapping to database tables | YES | "Each service has its own database table it manages" |
| No workflow logic captured | YES | No service represents a business workflow -- checkout spans 4 services |
| Single user action spans 4+ services | YES | "checkout requires calling 4 services in sequence" |

**Diagnosis:** This is a textbook Entity Trap. The current design is an ORM layer masquerading as an architecture. Each service is essentially a thin wrapper around a database table with CRUD operations. The smoking gun: a checkout (a single, atomic business action from the customer's perspective) requires orchestrating UserService -> ProductService -> OrderService -> PaymentService -> NotificationService in sequence. This means the *real* workflow logic lives nowhere -- it's either in a controller, a script, or in the developers' heads.

---

## Restructured Components

Applying Actor/Actions discovery, grouping by workflow cohesion:

| Component | Responsibility | Key Actions | Architecture Characteristics |
|-----------|---------------|-------------|----------------------------|
| **Catalog** | Product browsing, search, category management | Browse products, search, view details, manage categories, manage inventory | Performance (high read traffic), availability |
| **Checkout** | End-to-end purchase workflow: cart -> payment -> confirmation | Add to cart, apply discount, submit order, coordinate payment, generate confirmation | Reliability, data integrity, fault tolerance |
| **Payment Processing** | Payment gateway integration, refund handling | Charge card, process refund, handle payment webhooks, reconcile transactions | Security, reliability, auditability |
| **Order Management** | Post-purchase order lifecycle | Track order status, view order history, manage fulfillment state, cancel order | Availability, data consistency |
| **Customer Identity** | Authentication, profile, preferences | Register, login, manage profile, reset password, manage preferences | Security, availability |
| **Notification Dispatch** | Cross-cutting notification delivery | Send transactional emails, push notifications, notification preferences | Elasticity (burst during sales), eventual consistency |

### Why This Is Different From the Original

| Original (Entity Trap) | Restructured (Workflow-Based) | What Changed |
|------------------------|-------------------------------|-------------|
| UserService (CRUD users) | Customer Identity (auth + profile workflow) | Focused on *what users do with their identity*, not the user table |
| ProductService (CRUD products) | Catalog (browsing + search + inventory) | Focused on the *product discovery workflow*, not the product table |
| OrderService (CRUD orders) | Checkout + Order Management (two distinct workflows) | Split because placing an order and managing an existing order are different workflows with different characteristics |
| PaymentService (process payments) | Payment Processing (retained but scoped to gateway integration) | Similar scope, but now called by Checkout as a step, not orchestrated externally |
| NotificationService (send emails) | Notification Dispatch (event-driven, not sequentially called) | Now reacts to domain events rather than being called as step 5 of checkout |

---

## Requirement Mapping

| Requirement / User Story | Component(s) | Notes |
|--------------------------|-------------|-------|
| Customer browses and searches products | Catalog | Single component, no cross-cutting |
| Customer checks out (the problem scenario) | **Checkout** (orchestrates), Payment Processing | Down from 4 services to 1 orchestrator + 1 collaborator. Checkout owns the workflow. |
| Customer tracks an existing order | Order Management | Single component |
| Admin manages product catalog | Catalog | Same component, different actor permissions |
| Admin processes a refund | Order Management -> Payment Processing | 2 components, reasonable for a cross-concern action |
| System sends order confirmation | Notification Dispatch (triggered by Checkout event) | Event-driven, not sequential call |
| Customer registers/logs in | Customer Identity | Single component |

**Key improvement:** The checkout workflow -- the team's main pain point -- now lives inside the Checkout component. It coordinates internally rather than requiring an external orchestrator to call 4 services in sequence.

---

## Granularity Assessment

| Check | Result |
|-------|--------|
| Single user action requiring 5+ components? | NO -- checkout now requires Checkout + Payment Processing (2 components). Previously required 4-5. |
| Single component with 10+ unrelated responsibilities? | NO -- largest component (Checkout) has ~5 related actions all in the purchase workflow. |
| Each component handles 2-5 related actions? | YES -- all components fall in the 3-5 action range. |
| Cross-component calls per workflow | Acceptable: most workflows stay within 1-2 components. |

**Verdict:** Granularity looks right. Six components for a team of 8 means roughly 1-2 developers per component, which is manageable. No component is so large it needs its own sub-team, and none is so small it's trivial.

---

## Characteristic Variance

| Component | Primary Characteristic | Differs From Others? |
|-----------|----------------------|:---:|
| Catalog | Performance (high read volume) | Yes |
| Checkout | Reliability, data integrity | Yes |
| Payment Processing | Security, reliability | Yes |
| Order Management | Availability, consistency | No |
| Customer Identity | Security, availability | No |
| Notification Dispatch | Elasticity (burst) | Yes |

**Variance detected:** Catalog (read-optimized), Checkout (transactional integrity), Payment Processing (security-critical), and Notification Dispatch (burst elasticity) each have distinct characteristic profiles. This suggests they may benefit from being separate deployment units (quanta) if the team moves to a distributed architecture. For now as a modular monolith, they should at minimum be separate modules with clear interfaces.

**Recommendation:** Flag for quantum analysis if the team considers moving beyond a monolith. The characteristic variance supports a distributed approach, but a well-modularized monolith is a reasonable starting point for a team of 8.

---

## Component Relationship Map

```
                    +-----------------------+
                    |   Customer Identity   |
                    |  (auth, profile)      |
                    +-----------+-----------+
                                |
                         authenticates
                                |
              +-----------------+------------------+
              |                                    |
   +----------v----------+            +-----------v-----------+
   |      Catalog         |            |   Order Management    |
   | (browse, search,     |            | (track, history,      |
   |  inventory)          |            |  fulfillment)         |
   +----------+-----------+            +-----------------------+
              |                                    ^
        product info                          order created
              |                                    |
   +----------v-----------+                        |
   |      Checkout         +------------------------+
   | (cart, purchase       |
   |  orchestration)       |
   +----------+------------+
              |
        payment request
              |
   +----------v-----------+
   | Payment Processing    |
   | (charge, refund,      |
   |  reconciliation)      |
   +----------------------+

   All state-changing components emit domain events to:
   +---------------------------+
   |  Notification Dispatch    |
   |  (email, push, async)    |
   +---------------------------+
```

**Communication pattern:** Checkout is the orchestrator for the purchase workflow. It reads product info from Catalog, creates orders in Order Management, and delegates payment to Payment Processing. Notification Dispatch is event-driven -- it subscribes to domain events (order placed, payment confirmed, order shipped) rather than being called synchronously. This eliminates the sequential 5-service chain the team currently suffers from.

---

## Summary of Recommendations

1. **You have the Entity Trap.** Your current services mirror database tables, not business workflows. This is the single biggest structural problem and the direct cause of the "4 services in sequence for checkout" pain.

2. **Restructure around 6 workflow-based components:** Catalog, Checkout, Payment Processing, Order Management, Customer Identity, Notification Dispatch.

3. **The checkout workflow should live inside the Checkout component**, not be orchestrated externally across 4 services. Checkout calls Payment Processing for the payment step; everything else (cart, validation, order creation, confirmation) is internal.

4. **Make Notification Dispatch event-driven.** It should react to domain events, not be called as the last step of every workflow. This decouples it from all other components.

5. **Start with a modular monolith.** For a team of 8 at 3 months in, a well-modularized monolith with clear component boundaries is the right move. The characteristic variance supports an eventual move to distributed architecture, but that should be driven by scaling needs, not ambition.

6. **Iterate.** This design is a hypothesis. Map your actual user stories to these components, find the mismatches, and adjust. The chance of getting it perfect on the first pass is near zero -- and that's expected.
