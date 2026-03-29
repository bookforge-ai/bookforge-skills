## Significance Assessment

| Dimension | Affected? | How |
|-----------|:---------:|-----|
| Structure | Yes | Shifts the communication pattern between order and payment services from synchronous request/response (REST) to asynchronous event-driven messaging (Kafka). This is a fundamental change in architectural style for this interaction. |
| Nonfunctional characteristics | Yes | Directly addresses performance and scalability — REST calls are timing out under Black Friday peak load because the payment service cannot respond within acceptable latency windows. Kafka decouples processing time from the caller's wait time, improving resilience under load. |
| Dependencies | Yes | Changes the coupling model between the two services. REST creates runtime coupling (order service blocks until payment responds). Kafka introduces temporal decoupling — the order service publishes an event and continues, removing the direct runtime dependency on payment service availability and response time. |
| Interfaces | Yes | Replaces a synchronous REST API contract (HTTP request/response with endpoints, status codes, timeouts) with an asynchronous event contract (Kafka topics, event schemas, consumer groups). The interaction model between these services fundamentally changes. |
| Construction techniques | No | The team is already on AWS, which natively supports both patterns. Kafka (via Amazon MSK or self-managed) is an infrastructure addition but does not change the core development platform, language, or framework. |

**Verdict:** Architecturally significant — affects 4 of 5 dimensions.

---

# ADR 1: Use Kafka for Order-to-Payment Service Communication

## Status

Accepted

## Context

Our e-commerce platform's order service communicates with the payment service via synchronous REST calls. During Black Friday sales events, payment processing latency increases significantly due to traffic volume, causing HTTP timeouts in the order service. This results in failed orders, degraded user experience, and lost revenue during the highest-traffic period of the year.

The core problem is temporal coupling: the order service blocks while waiting for the payment service to complete processing. Under normal load this is acceptable, but under peak load the payment service response time exceeds the order service's timeout threshold, creating cascading failures.

We are a team of 6 engineers operating on AWS.

**Alternatives considered:**

1. **Increase REST timeout thresholds and scale payment service horizontally.** This would preserve the synchronous model but only delays the problem — higher timeouts tie up order service threads longer, reducing its own capacity under load. Horizontal scaling helps but has diminishing returns when the bottleneck is per-request processing time (e.g., payment gateway latency).

2. **Use asynchronous messaging via Kafka.** The order service publishes a payment-requested event to a Kafka topic. The payment service consumes events at its own pace, processes payments, and publishes a payment-completed (or payment-failed) event. The order service no longer blocks on payment processing.

3. **Use a simpler message queue (e.g., Amazon SQS).** Would achieve decoupling but lacks Kafka's event log durability, replay capability, and throughput characteristics. Given that payment events are business-critical and we may need event replay for reconciliation, Kafka's log-based architecture is better suited.

## Decision

We will replace the synchronous REST communication between the order service and payment service with asynchronous event-driven messaging using Apache Kafka (via Amazon MSK on AWS).

**WHY this solves the problem:** The root cause of Black Friday failures is temporal coupling — the order service's fate is tied to the payment service's response time. Kafka eliminates this coupling entirely. The order service publishes a `payment-requested` event and immediately returns a "payment pending" acknowledgment to the user. The payment service processes the event independently, at whatever pace it can sustain, and publishes the result. Even if payment processing takes 30 seconds under peak load, the order service is unaffected.

**WHY Kafka over simpler alternatives:** Scaling REST does not address the fundamental coupling problem — it treats the symptom (slow responses) rather than the cause (blocking dependency). SQS would decouple the services but Kafka provides durable event logs that enable replay for payment reconciliation, better throughput for Black Friday-scale bursts (partitioned consumption), and a foundation for future event-driven patterns as the platform grows.

**Business justification:** Black Friday is our highest-revenue period. Every failed order due to a timeout is direct revenue loss. Asynchronous processing ensures order capture is resilient to downstream latency, protecting revenue during peak traffic. The investment in Kafka also positions us for future event-driven capabilities (order tracking, analytics, notifications) without additional architectural changes.

## Consequences

### Positive

- **Eliminates Black Friday timeout failures.** The order service no longer blocks on payment processing, so payment latency spikes cannot cause order failures.
- **Improved scalability.** Kafka partitions allow the payment service to scale consumers independently based on queue depth, handling traffic bursts more gracefully than synchronous scaling.
- **Service decoupling.** The order service and payment service can be deployed, scaled, and maintained independently. A payment service outage no longer immediately cascades to the order service.
- **Event replay and auditability.** Kafka's durable log provides a replayable history of all payment events, valuable for reconciliation, debugging, and compliance.
- **Foundation for future event-driven patterns.** Other services (notifications, analytics, inventory) can subscribe to the same events without modifying the order or payment services.

### Negative

- **Eventual consistency.** Orders will temporarily exist in a "payment pending" state. The UI must handle this gracefully, and customers accustomed to immediate payment confirmation may find the slight delay unfamiliar.
- **More complex error handling.** Failed payments must be handled asynchronously (dead letter topics, retry policies, compensation logic) rather than with a simple HTTP error response. The team must design and implement a robust error/retry strategy.
- **Operational complexity.** Kafka (even as managed Amazon MSK) introduces a new infrastructure component to monitor, tune, and maintain. The team of 6 must absorb this operational overhead.
- **Debugging difficulty.** Tracing a request across asynchronous boundaries is harder than following a synchronous REST call. Distributed tracing (correlation IDs) becomes essential.

### Trade-offs

- We accept eventual consistency and UI complexity in exchange for resilience and scalability under peak load. The order experience shifts from "instant confirmation" to "confirmation within seconds" — an acceptable trade-off given that the alternative is order failures during high-traffic events.
- We accept increased infrastructure and operational complexity (Kafka cluster management, consumer group tuning, dead letter topic handling) in exchange for eliminating the temporal coupling that causes Black Friday outages.

## Compliance

- **Type:** Automated fitness function + manual review
- **Mechanism:**
  - **Automated:** A CI integration test or architecture test that verifies no direct synchronous REST calls exist from the order service to the payment service. This can be implemented as a test that scans the order service codebase for HTTP client calls targeting payment service endpoints, failing the build if any are found. Additionally, a contract test verifying the Kafka event schema (`payment-requested`, `payment-completed`, `payment-failed`) between producer and consumer.
  - **Manual:** During quarterly architecture review, verify that no new synchronous coupling has been introduced between these services and that Kafka consumer lag metrics are within acceptable thresholds.
- **Frequency:** Automated tests run on every pull request. Manual review quarterly and before major traffic events (e.g., pre-Black Friday readiness check).

## Notes

- **Author:** Team (6-person e-commerce engineering team)
- **Date:** 2026-03-27
- **Approved by:** Team consensus (small team, self-approved)
- **Last modified:** 2026-03-27
- **Supersedes:** N/A (no prior ADR — this is the first formal architecture decision record)
- **Superseded by:** N/A
