# Topology Variants — Service-Based Architecture

Service-based architecture is one of the most flexible architecture styles because multiple topology dimensions can be independently varied: user interface deployment, database partitioning, API layer inclusion, and service granularity. This reference covers the decision space for each dimension.

## User Interface Variants

### Single Monolithic UI

```
┌─────────────────────────────────┐
│         User Interface          │
└──┬──────┬──────┬──────┬─────────┘
   │      │      │      │
┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐
│Svc A││Svc B││Svc C││Svc D│
└──┬──┘└──┬──┘└──┬──┘└──┬──┘
   │      │      │      │
┌──▼──────▼──────▼──────▼──┐
│         Database          │
└───────────────────────────┘
```

**When to use:**
- Single user group with uniform needs
- Small team maintaining one frontend
- Simplest deployment model

**Architecture quanta:** 1 (if shared DB) — all services share the same deployment and characteristic profile.

**Trade-offs:**
- (+) Simplest to build and deploy
- (+) Consistent UX across all domains
- (-) UI deployment blocks all domains
- (-) Cannot scale or secure frontend sections independently

### Domain-Based UIs

```
┌───────────────┐ ┌───────────────┐
│  UI: Customer │ │ UI: Internal  │
└──┬─────┬──────┘ └──┬──────┬─────┘
   │     │           │      │
┌──▼──┐┌─▼──┐  ┌────▼─┐┌───▼──┐┌────────┐
│Svc A││Svc B│  │Svc C ││Svc D ││Svc E   │
└──┬──┘└──┬──┘  └──┬───┘└──┬───┘└──┬─────┘
   │      │        │       │       │
┌──▼──────▼────────▼───────▼───────▼──┐
│             Database                 │
└──────────────────────────────────────┘
```

**When to use:**
- Different user groups (customers vs internal staff vs partners)
- Different security requirements per user group
- Different availability/scalability needs per user group

**Architecture quanta:** Can be >1 — each UI + its services can form a separate quantum, especially if databases are also split.

**Trade-offs:**
- (+) Independent deployment per user group
- (+) Different security zones (customer-facing behind DMZ)
- (+) Can scale customer-facing independently
- (-) More deployment units to manage
- (-) Potential code duplication in shared UI components

### Service-Based UIs (Micro-Frontends)

```
┌───────┐┌───────┐┌───────┐┌───────┐
│  UI A ││  UI B ││  UI C ││  UI D │
└──┬────┘└──┬────┘└──┬────┘└──┬────┘
   │        │        │        │
┌──▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐
│Svc A│  │Svc B│  │Svc C│  │Svc D│
└──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
   │        │        │        │
┌──▼────────▼────────▼────────▼──┐
│           Database              │
└─────────────────────────────────┘
```

**When to use:**
- Maximum frontend independence
- Teams organized around domain services
- Each domain needs different frontend technology or release cadence

**Architecture quanta:** Multiple — each UI-service pair is a potential quantum.

**Trade-offs:**
- (+) Maximum team autonomy per domain
- (+) Independent deployment and technology per UI
- (-) Most complex frontend orchestration
- (-) Consistent UX across domains is harder
- (-) Requires micro-frontend framework/approach

### UI Decision Matrix

| Factor | Single UI | Domain-Based | Service-Based |
|--------|:---------:|:------------:|:-------------:|
| Deployment simplicity | Best | Moderate | Most complex |
| Team autonomy | Low | Moderate | High |
| Security zoning | None | Good | Good |
| Independent scaling | No | Per-group | Per-service |
| UX consistency | Easiest | Moderate | Hardest |
| Recommended team size | <15 | 10-30 | 20+ |

## Database Variants

### Single Shared Database (Default)

```
┌──────┐┌──────┐┌──────┐┌──────┐
│Svc A ││Svc B ││Svc C ││Svc D │
└──┬───┘└──┬───┘└──┬───┘└──┬───┘
   │       │       │       │
   │  single_shared_lib    │
   │  (all entity objects) │
   │       │       │       │
┌──▼───────▼───────▼───────▼──┐
│         Database             │
│  (all tables, one schema)   │
└──────────────────────────────┘
```

**When to use:** Starting point. Multiple services need SQL joins. ACID transactions span services.

**Risk:** A table change forces a shared library update -> redeployment of ALL services, even those that don't use the changed table. This is the **single shared entity library anti-pattern**.

### Logically Partitioned Database (Recommended)

```
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│  Svc A   ││  Svc B   ││  Svc C   ││  Svc D   │
│          ││          ││          ││          │
│ a_ent_lib││ b_ent_lib││ c_ent_lib││ d_ent_lib│
│ common   ││ common   ││ a_ent_lib││ common   │
│          ││          ││ common   ││          │
└──┬───────┘└──┬───────┘└──┬───────┘└──┬───────┘
   │           │           │           │
┌──▼───────────▼───────────▼───────────▼──┐
│              Database                    │
│ ┌───────┐┌───────┐┌───────┐┌──────────┐│
│ │ dom_a ││ dom_b ││ dom_c ││  common  ││
│ └───────┘└───────┘└───────┘└──────────┘│
└──────────────────────────────────────────┘
```

**When to use:** Shared database benefits needed + want to control change blast radius.

**How it works:**
1. Database tables are logically grouped into domain partitions
2. Each domain partition has its own entity library (e.g., `invoicing_entities_lib`)
3. A `common_entities_lib` contains shared tables used by all services
4. Services include only the entity libraries they need
5. When a table changes, only the corresponding entity library is updated -> only services using that library need redeployment

**Common table management:** Lock common entity objects in version control. Restrict change access to the database team. Changes to common tables require coordination across all services.

**Best practice:** Make logical partitions as fine-grained as possible while maintaining well-defined data domains.

### Domain-Partitioned Databases

```
┌──────┐┌──────┐  ┌──────┐┌──────┐
│Svc A ││Svc B │  │Svc C ││Svc D │
└──┬───┘└──┬───┘  └──┬───┘└──┬───┘
   │       │         │       │
┌──▼───────▼──┐   ┌──▼───────▼──┐
│  Database 1 │   │  Database 2 │
│ (domain AB) │   │ (domain CD) │
└─────────────┘   └─────────────┘
```

**When to use:**
- Clear domain groups with no cross-group joins needed
- Security boundaries require separate databases (e.g., customer-facing vs internal)
- Different backup/recovery requirements per domain group

**Critical check before splitting:** Verify that NO business workflows require ACID transactions across the database boundary. If they do, you need SAGA pattern for those workflows.

### Per-Service Databases

```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Svc A │  │Svc B │  │Svc C │  │Svc D │
└──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
   │         │         │         │
┌──▼──┐   ┌──▼──┐   ┌──▼──┐   ┌──▼──┐
│DB A │   │DB B │   │DB C │   │DB D │
└─────┘   └─────┘   └─────┘   └─────┘
```

**When to use:** Each service's data is truly independent. No cross-service queries. Team is ready for eventual consistency and SAGA pattern.

**Warning:** This approaches microservices territory. If you need per-service databases, evaluate whether you should be doing microservices instead (with the full operational investment that requires).

### Database Decision Matrix

| Factor | Single shared | Logically partitioned | Domain-partitioned | Per-service |
|--------|:------------:|:--------------------:|:------------------:|:-----------:|
| ACID across services | Yes | Yes | Partial | No |
| SQL joins across domains | Yes | Yes | Within group only | No |
| Schema change blast radius | All services | Domain-scoped | Group-scoped | Single service |
| Operational complexity | Lowest | Low | Moderate | Highest |
| Data isolation | None | Logical | Physical (partial) | Physical (full) |
| SAGA required | No | No | For cross-group ops | For cross-service ops |

## API Layer Variant

### Without API Layer (Direct Access)

```
┌─────────────────────────────┐
│       User Interface        │
│  (service locator / proxy)  │
└──┬──────┬──────┬──────┬─────┘
   │      │      │      │
┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐
│Svc A││Svc B││Svc C││Svc D│
└─────┘└─────┘└─────┘└─────┘
```

UI embeds a service locator pattern, API gateway, or proxy to route requests to services.

### With API Layer

```
┌─────────────────────────────┐
│       User Interface        │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│   API Layer (Proxy/Gateway) │
│  (security, metrics, audit) │
└──┬──────┬──────┬──────┬─────┘
   │      │      │      │
┌──▼──┐┌──▼──┐┌──▼──┐┌──▼──┐
│Svc A││Svc B││Svc C││Svc D│
└─────┘└─────┘└─────┘└─────┘
```

**Benefits of API layer:**
- Centralized cross-cutting concerns (security, metrics, auditing, rate limiting)
- Service discovery and routing
- External consumer access management
- API versioning and transformation

**Cost of API layer:**
- Additional deployment unit
- Additional network hop (latency)
- Potential single point of failure
- More infrastructure to maintain

## ACID vs BASE Transaction Decision

### ACID (Within Service or Shared Database)

Use ACID when the business operation must be all-or-nothing and the database topology supports it.

**Example — Order Checkout (single service with shared DB):**
1. OrderService receives checkout request
2. Within a single database transaction:
   - Create order record
   - Apply payment
   - Update inventory
   - Generate invoice
3. If payment fails -> automatic rollback of all changes
4. Customer sees consistent state immediately

This is the service-based architecture advantage: the coarse-grained OrderService handles the entire workflow internally.

### BASE (Across Separate Databases)

Required when business operations cross database boundaries. Uses SAGA pattern.

**Example — Same Order Checkout if databases were split:**
1. OrderService creates order (commits to Order DB)
2. OrderService sends message to PaymentService
3. PaymentService attempts payment (commits to Payment DB)
4. If payment fails:
   - PaymentService sends "payment failed" event
   - OrderService must execute compensating transaction (delete order)
   - InventoryService must execute compensating transaction (restore inventory)
5. Customer may see temporarily inconsistent state

**Key insight:** If you find yourself implementing SAGA for many core business workflows in a service-based architecture, your services may be too fine-grained or your databases may be split prematurely. Consider merging services or consolidating databases to restore ACID.

## Service Granularity Guidelines

| Service count | Assessment | Action |
|:------------:|-----------|--------|
| 1-2 | Not service-based | Too few services; consider modular monolith instead |
| 3 | Borderline | Barely enough decomposition; validate benefits outweigh distribution costs |
| 4-7 | Sweet spot | Good balance of independence and simplicity |
| 8-12 | Acceptable upper range | Verify each service represents a distinct domain; watch for drift toward microservices |
| 13-20 | Warning zone | You may be building microservices without the infrastructure; consider merging related services |
| 20+ | Not service-based | This is microservices; invest in full microservices operational infrastructure |

## Communication Protocols

Service-based architecture typically uses synchronous communication from the UI to services:

| Protocol | When to use |
|----------|------------|
| **REST** | Default choice. Simple, well-understood, good tooling |
| **gRPC** | High-throughput internal communication, binary efficiency needed |
| **Messaging** | Asynchronous operations, event notifications between UI and services |
| **SOAP** | Legacy integration, WS-* standards required |

**Important:** Communication is UI-to-service or API-layer-to-service. Services should NOT communicate directly with each other in service-based architecture.
