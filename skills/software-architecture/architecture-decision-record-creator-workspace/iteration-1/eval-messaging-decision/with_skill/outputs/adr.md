# ADR 1: Use Kafka for Order-to-Payment Service Communication

## Status
Accepted

## Context
Our e-commerce platform's order service communicates with the payment service using synchronous REST calls. During Black Friday sales events, payment processing latency increases significantly due to load spikes, causing HTTP request timeouts in the order service. These timeouts result in failed orders, lost revenue, and degraded customer experience during our highest-traffic period.

The order service does not need an immediate, synchronous response from the payment service to confirm the order to the user. It needs to reliably hand off a payment request and eventually receive confirmation that payment succeeded or failed.

We are a team of 6 running on AWS. The following alternatives were considered:

1. **Keep REST with increased timeouts and retries** -- Extend HTTP timeout thresholds and add retry logic with exponential backoff.
2. **Use Amazon SQS** -- Replace REST with a managed message queue for point-to-point asynchronous communication.
3. **Use Apache Kafka (Amazon MSK)** -- Replace REST with Kafka as an event streaming platform for asynchronous, event-driven communication.

## Decision
We will replace the synchronous REST communication between the order service and payment service with asynchronous event-driven messaging using Apache Kafka, deployed via Amazon MSK (Managed Streaming for Apache Kafka).

**WHY this decision, technically:** The core problem is that synchronous REST creates temporal coupling -- the order service is blocked while the payment service processes the request. Under peak load (Black Friday), payment processing latency spikes beyond REST timeout thresholds, causing cascading failures. Kafka eliminates this temporal coupling entirely. The order service publishes an `OrderCreated` event and moves on immediately. The payment service consumes events at its own pace, processing the backlog without any upstream timeout pressure. Kafka's partitioned log also provides natural load leveling -- traffic spikes are absorbed into the log rather than overwhelming the payment service.

**WHY Kafka over SQS:** While SQS would solve the immediate timeout problem, Kafka provides durable, replayable event logs and supports multiple consumers on the same event stream. As we grow, other services (inventory, notifications, analytics) can subscribe to `OrderCreated` events without modifying the order service. This fan-out capability positions us for future event-driven patterns without re-architecting. Kafka also provides ordering guarantees within partitions, which matters for payment processing where event sequence is important.

**WHY not just increase REST timeouts:** Raising timeouts is a band-aid. It would still leave the order service blocked and unresponsive during payment processing, degrading user experience. Under extreme load, even generous timeouts would eventually be breached, and the synchronous coupling would continue to make the order service's availability dependent on the payment service's performance.

**Business justification:** Black Friday is our highest-revenue period. Order failures during peak traffic directly translate to lost sales and damaged customer trust. Decoupling these services ensures that payment processing delays do not block order acceptance, preserving revenue during traffic spikes. Amazon MSK is a managed service, keeping operational overhead manageable for our team of 6.

## Consequences

### Positive
- **Eliminates timeout failures during peak load.** The order service publishes events in single-digit milliseconds regardless of payment service load, removing the Black Friday failure mode entirely.
- **Decouples service availability.** The order service no longer depends on the payment service being healthy and responsive at the moment of order placement. If the payment service is temporarily down, events queue in Kafka and are processed when it recovers.
- **Natural load leveling.** Traffic spikes are absorbed by Kafka's durable log. The payment service processes events at a sustainable rate rather than being overwhelmed by burst traffic.
- **Fan-out capability.** Other services can subscribe to order events without modifying the order service, enabling future features (real-time analytics, inventory reservation, notification triggers) with minimal coupling.
- **Event replay.** Kafka's retained log allows replaying events for debugging, recovery, or onboarding new consumers.

### Negative
- **Increased operational complexity.** Kafka (even managed via MSK) introduces a new infrastructure component that the team must monitor, configure, and understand. This is a nontrivial learning curve for a team of 6.
- **Eventual consistency.** The order service can no longer return a synchronous "payment confirmed" response. The user experience must be redesigned to handle an intermediate "order received, payment processing" state, which adds front-end and UX complexity.
- **Complex error handling.** Payment failures (insufficient funds, fraud detection) now arrive asynchronously. The system needs a dead-letter queue strategy, compensation logic (e.g., order cancellation on payment failure), and monitoring for stuck or failed events.
- **Debugging difficulty.** Tracing a request across an asynchronous boundary is harder than following a synchronous REST call chain. Correlation IDs and distributed tracing become essential.

### Trade-offs
- We are trading **simplicity of synchronous request-response** for **resilience and scalability under load**. The system becomes more complex to build and debug, but it no longer fails under the exact conditions (peak traffic) where reliability matters most.
- We are trading **immediate consistency** (synchronous payment confirmation) for **availability** (orders are always accepted, payment confirmation follows asynchronously). This is an explicit CAP theorem trade-off favoring availability.
- We are accepting **higher infrastructure cost** (MSK cluster) in exchange for **preserved revenue** during peak sales events.

## Compliance
- **Type:** Automated fitness function + Manual review
- **Mechanism:**
  - **Automated:** Integration test in CI pipeline that verifies the order service publishes to the `order-events` Kafka topic and does NOT make direct REST calls to the payment service endpoint. This can be implemented as a test that spins up an embedded Kafka (or uses Testcontainers) and asserts event publication, combined with a static analysis check (or architecture test) ensuring no HTTP client calls to the payment service URL exist in the order service codebase.
  - **Automated:** CloudWatch alarm on the `order-events` topic consumer lag. If the payment service falls behind by more than a configured threshold (e.g., 10,000 messages), alert the team.
  - **Manual:** Quarterly review of Kafka topic configuration (retention, partitions, replication factor) and consumer group health as part of architecture review.
- **Frequency:** Automated tests run on every pull request. Consumer lag monitoring is continuous. Manual review is quarterly.

## Notes
- **Author:** Team (6-person e-commerce team)
- **Date:** 2026-03-27
- **Approved by:** Team consensus
- **Last modified:** 2026-03-27
- **Supersedes:** N/A (no prior ADR for order-payment communication; REST was the implicit default)
- **Superseded by:** N/A
- **Implementation notes:** Evaluate Amazon MSK Serverless vs. Provisioned for cost optimization given the team size. Start with a single `order-events` topic with 6 partitions (one per team member for parallel development, adjustable based on throughput needs). Implement correlation IDs from day one to support distributed tracing across the async boundary.
