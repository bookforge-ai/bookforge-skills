# Quantum Analysis: Online Auction System ("Going Going Gone")

## Step 1: Components Identified

Scanned the codebase at `test-env/`. Found 4 services defined in `docker-compose.yml`, each with its own Dockerfile, source code, and `requirements.txt`.

| Component | Responsibility | Deployment Unit | Port | Replicas |
|-----------|---------------|-----------------|------|----------|
| **Bidder Service** | Accepts bid placement requests from users; validates and forwards to Auction Service | Docker container (`./bidder_service`), 3 replicas, `bidding_net` network | 8001 | 3 |
| **Auction Service** | Manages auction lifecycle (create, accept bids, close); publishes events on close | Docker container (`./auction_service`), 3 replicas, `bidding_net` + `backend_net` networks | 8002 | 3 |
| **Payment Service** | Processes payments after auction close; idempotent, audit-trail-focused | Docker container (`./payment_service`), 1 replica, `backend_net` network | 8003 | 1 |
| **Notification Service** | Sends email/SMS notifications to auction winners | Docker container (`./notification_service`), 2 replicas, `backend_net` network | 8004 | 2 |

**Infrastructure:** RabbitMQ message broker on `backend_net`, used for asynchronous event routing.

### Evidence from codebase

- `bidder_service/app.py` imports `httpx` and makes synchronous HTTP calls to `http://auction:8002` -- confirms tight REST coupling.
- `auction_service/events.py` imports `pika` and publishes to `payment_queue` and `notification_queue` via RabbitMQ -- confirms async event publishing.
- `payment_service/worker.py` and `notification_service/worker.py` are pure RabbitMQ consumers with no outbound HTTP calls -- confirms they are independent async consumers.
- `docker-compose.yml` places Bidder and Auction on a shared `bidding_net` with matching replica counts (3 each), while Payment and Notification are on `backend_net` only.

---

## Step 2: Communication Map

| From | To | Type | Mechanism | Latency Req | Fate-Sharing? |
|------|----|------|-----------|-------------|:---:|
| Bidder Service | Auction Service | **Synchronous** | REST/HTTP via `httpx` (timeout: 2.0s) | <100ms | **Yes** |
| Auction Service | Payment Service | **Asynchronous** | AMQP/RabbitMQ (`payment_queue`, durable, persistent messages) | N/A | No |
| Auction Service | Notification Service | **Asynchronous** | AMQP/RabbitMQ (`notification_queue`, durable) | N/A | No |

### Connascence analysis

- **Bidder <-> Auction:** Connascence of Name (endpoint paths `/auctions/{id}/bids`), Connascence of Type (shared `BidRequest`/`IncomingBid` schemas via Pydantic), and critically, **Connascence of Execution** (synchronous call -- Bidder blocks waiting for Auction's response). This dynamic connascence means they share operational fate: if Auction is slow or down, Bidder fails too.
- **Auction -> Payment:** Only Connascence of Meaning (agreed-on event schema `{"event": "auction_closed", ...}`). No dynamic connascence -- fire-and-forget via message queue. Payment uses `basic_ack`/`basic_nack` for reliability, independently of Auction's state.
- **Auction -> Notification:** Same as above -- Connascence of Meaning only. Fire-and-forget. Notification never blocks Auction.

### Communication diagram

```
Bidder ──[sync REST, <100ms]──> Auction ──[async MQ, durable]──> Payment
                                   |
                                   └──[async MQ, durable]──> Notification
```

---

## Step 3: Architecture Characteristics Per Component

Sourced from `architecture-characteristics.yaml` and confirmed by code patterns:

| Characteristic | Bidder Service | Auction Service | Payment Service | Notification Service |
|---------------|:-:|:-:|:-:|:-:|
| **Elasticity** | 5 (burst traffic during live auctions) | 4 (inherits from Bidder coupling) | 1 | 1 |
| **Performance** | 5 (sub-100ms bid latency) | 4 (must keep up with bid throughput) | 2 (batch is fine) | 1 (latency not critical) |
| **Scalability** | 4 (horizontal for peaks) | 4 | 1 | 2 |
| **Availability** | 3 | 3 | 3 | **5** (always reachable) |
| **Reliability** | 2 | 3 | **5** (payments must never be lost) | 3 |
| **Security** | 2 | 2 | **5** (PCI compliance) | 1 |

**Key observation:** The characteristics are clearly **non-uniform**. Bidder/Auction are dominated by elasticity and performance. Payment is dominated by reliability and security. Notification is dominated by availability. These are fundamentally different optimization targets.

### Code-level evidence of characteristic priorities

- **Bidder:** `httpx.AsyncClient(timeout=2.0)` -- tight timeout to preserve low-latency user experience. 3 replicas for elasticity.
- **Payment:** `basic_qos(prefetch_count=1)` -- processes one message at a time for reliability. Idempotency check in `processor.py` (`processed_auctions` set). `basic_nack(requeue=True)` on failure -- never drops a payment. Pydantic validation with `field_validator` on amount. 1 replica (reliability over scale).
- **Notification:** Fire-and-forget pattern in `sender.py` -- "failures are logged but never block the pipeline." 2 replicas for availability.

---

## Step 4: Quantum Grouping

Applying the three-criteria AND test:

### Quantum 1: Bidding Quantum (Bidder + Auction)

| Criterion | Satisfied? | Evidence |
|-----------|:-:|---------|
| Deploy together | **Yes** | Same `bidding_net` network, matching replica count (3 each), `depends_on: [auction]` in docker-compose |
| High functional cohesion | **Yes** | Both serve the unified purpose of "real-time bid processing during live auctions" |
| Synchronous connascence | **Yes** | Bidder makes blocking REST calls to Auction via `httpx`; Bidder cannot function without Auction |

All three criteria met. These form a single quantum.

### Quantum 2: Payment Quantum (Payment Service)

| Criterion | Satisfied? | Evidence |
|-----------|:-:|---------|
| Independent deployment | **Yes** | Own network scope (`backend_net` only), own replica count (1), no `depends_on` to bidding services |
| Distinct business purpose | **Yes** | Financial transaction processing -- unrelated to real-time bidding |
| Asynchronous boundary | **Yes** | Consumes from `payment_queue` via RabbitMQ; no synchronous coupling to any other service |

Separated from Bidding Quantum by asynchronous boundary. Independent quantum.

### Quantum 3: Notification Quantum (Notification Service)

| Criterion | Satisfied? | Evidence |
|-----------|:-:|---------|
| Independent deployment | **Yes** | Own network scope (`backend_net` only), own replica count (2), no `depends_on` to bidding services |
| Distinct business purpose | **Yes** | User communication (email/SMS) -- unrelated to bidding or payments |
| Asynchronous boundary | **Yes** | Consumes from `notification_queue` via RabbitMQ; no synchronous coupling to any other service |

Separated from Bidding Quantum by asynchronous boundary. Independent quantum.

### Database analysis

No shared database detected. Each service uses in-memory storage (Auction uses a Python dict, Payment uses a Python set for idempotency). In production, each quantum would have its own datastore -- no database coupling forces quanta together.

---

## Step 5: Quantum Characteristics Comparison

| Quantum | Components | Driving Characteristics (Top 3) | Internal Communication |
|---------|-----------|--------------------------------|:---:|
| **Bidding** | Bidder, Auction | Elasticity, Performance, Scalability | Synchronous REST |
| **Payment** | Payment | Reliability, Security, Availability | N/A (single service) |
| **Notification** | Notification | Availability, Reliability, Scalability | N/A (single service) |

### Cross-quantum characteristic comparison

| Characteristic | Bidding Quantum | Payment Quantum | Notification Quantum | Uniform? |
|---------------|:-:|:-:|:-:|:-:|
| Elasticity | **High** (5) | Low (1) | Low (1) | **No** |
| Performance | **High** (5) | Low (2) | Low (1) | **No** |
| Scalability | **High** (4) | Low (1) | Low (2) | **No** |
| Reliability | Low (2) | **High** (5) | Moderate (3) | **No** |
| Security | Low (2) | **High** (5) | Low (1) | **No** |
| Availability | Moderate (3) | Moderate (3) | **High** (5) | **No** |

**Every single characteristic is non-uniform across quanta.** Each quantum has a completely different optimization profile.

---

## Step 6: Architecture Direction

**Quantum count:** 3

**Characteristic uniformity:** Non-uniform (all six measured characteristics differ significantly across quanta)

**Recommendation: Distributed architecture required.**

### Reasoning

The quantum analysis reveals three independently deployable units with fundamentally different quality attribute needs:

1. **The Bidding Quantum** must optimize for **elasticity and performance**. During live auctions, bid traffic bursts unpredictably. The Bidder and Auction services need to scale horizontally together (3 replicas each, 1 CPU / 512MB per container) and maintain sub-100ms latency. A monolith containing Payment and Notification would force these burst-scaling resources onto services that do not need them.

2. **The Payment Quantum** must optimize for **reliability and security**. Payments must never be lost (idempotent processing, message acknowledgment with requeue on failure, Pydantic validation). It runs at 1 replica with conservative resources (0.5 CPU / 256MB) because throughput is not the priority -- correctness is. If this were part of the Bidding monolith, the elasticity-driven scaling would create unnecessary replicas of payment logic, complicating PCI compliance and introducing reliability risks.

3. **The Notification Quantum** must optimize for **availability**. Notifications should always be deliverable but can tolerate delays. It runs at 2 replicas with minimal resources (0.25 CPU / 128MB). Its failure characteristics are fundamentally different: a failed notification is logged and retried, while a failed payment is a critical incident.

A monolith cannot simultaneously optimize for elasticity (Bidding), reliability (Payment), and availability (Notification). The asynchronous message queue boundaries (RabbitMQ) already provide the architectural seams between quanta, allowing each to scale, deploy, and fail independently.

### Recommended architecture style

Given 3 quanta with event-driven communication between them, this system is well-suited for an **event-driven architecture** (or service-based architecture if the team prefers fewer, coarser services). The existing RabbitMQ infrastructure already implements the inter-quantum communication pattern correctly.

---

## Warnings

1. **No persistent datastores detected.** All services use in-memory storage. In production, each quantum should have its own database to maintain deployment independence. If a shared database is introduced, it would collapse the quanta -- Payment and Bidding sharing a database would force them into the same quantum regardless of async messaging.

2. **RabbitMQ is a shared infrastructure dependency.** While it enables async boundaries between quanta, RabbitMQ itself is a single point of failure. Consider clustering or a managed message broker for production to avoid undermining the independence of the Payment and Notification quanta.

3. **No circuit breaker on the synchronous boundary.** The Bidder Service calls Auction with a 2-second `httpx` timeout but has no circuit breaker or fallback. If Auction becomes unresponsive, Bidder will accumulate waiting connections. Since they share a quantum this is partially mitigated (they scale together), but a circuit breaker would improve resilience during partial failures.

4. **Notification worker has no error handling on `send_notification`.** Unlike Payment (which uses `basic_nack` with requeue on failure), the Notification worker always ACKs after calling `send_notification`, even if sending fails silently. For the availability characteristic to hold, add explicit retry logic or dead-letter queue handling.
