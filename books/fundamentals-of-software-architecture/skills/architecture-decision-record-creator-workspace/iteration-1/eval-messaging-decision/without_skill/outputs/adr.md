# ADR-001: Switch Order-to-Payment Communication from REST to Kafka

**Date:** 2026-03-27

**Status:** Accepted

## Context

Our e-commerce platform currently uses synchronous REST calls for communication between the Order Service and the Payment Service. During high-traffic events such as Black Friday sales, payment processing latency increases significantly, causing HTTP request timeouts in the Order Service. This leads to failed orders, poor customer experience, and lost revenue during our highest-volume sales periods.

Our team consists of 6 engineers, and our infrastructure runs on AWS.

### Key problems with the current approach

- **Timeout failures under load:** When payment processing takes longer than the configured HTTP timeout (due to downstream bank/processor latency or volume), the order request fails entirely.
- **Tight coupling:** The Order Service is directly dependent on the Payment Service's availability. If Payment is down or slow, Order is directly impacted.
- **No built-in retry or buffering:** REST offers no native mechanism to queue requests during spikes. Failed requests require custom retry logic in application code.
- **Cascading failures:** Under heavy load, retries from the Order Service compound the problem, further overloading the Payment Service.

## Decision

We will replace the synchronous REST communication between the Order Service and the Payment Service with asynchronous, event-driven messaging using **Apache Kafka**, managed via **Amazon MSK** (Managed Streaming for Apache Kafka) on AWS.

The Order Service will publish an `OrderCreated` event to a Kafka topic. The Payment Service will consume from that topic, process the payment, and publish a `PaymentCompleted` or `PaymentFailed` event back to a separate topic that the Order Service consumes to update order status.

## Alternatives Considered

### 1. Keep REST with increased timeouts and retry logic

- Simple to implement; no new infrastructure.
- Does not solve the fundamental problem: under extreme load, the Payment Service still becomes a bottleneck and retries amplify the issue.
- Rejected because it treats symptoms rather than the root cause.

### 2. Amazon SQS

- Fully managed, simpler operationally than Kafka.
- Provides message buffering and decoupling.
- However, SQS is a point-to-point queue. If we later need multiple consumers for the same event (e.g., analytics, notifications, fraud detection), we would need to add SNS fan-out or duplicate messages.
- Lacks built-in message ordering guarantees (standard queues) or has lower throughput (FIFO queues, 300 msg/s per group).
- Rejected in favor of Kafka's stronger ordering, replay, and multi-consumer capabilities, which better fit our growth trajectory.

### 3. Amazon SNS + SQS (fan-out)

- Good for simple pub/sub with multiple subscribers.
- Adds operational complexity managing both SNS topics and SQS queues.
- No message replay capability; once consumed, messages are gone.
- Rejected because Kafka provides fan-out natively via consumer groups with the added benefit of message retention and replay.

### 4. RabbitMQ

- Mature message broker, good for task queuing.
- Would require self-management on AWS (or use Amazon MQ, which has throughput limits).
- Less suited for high-throughput event streaming at Black Friday scale.
- Rejected because Amazon MSK provides a managed Kafka solution that better handles our peak-traffic requirements.

## Consequences

### Positive

- **Eliminates timeout failures:** The Order Service publishes an event and moves on immediately. Payment processing time no longer blocks order creation.
- **Natural backpressure handling:** Kafka buffers messages during traffic spikes. The Payment Service consumes at its own pace without being overwhelmed.
- **Decoupled services:** Order and Payment services can be deployed, scaled, and maintained independently.
- **Message durability and replay:** Kafka retains messages for a configurable period. If the Payment Service goes down, it can catch up when it recovers. We can also replay events for debugging or reprocessing.
- **Future extensibility:** Other services (inventory, notifications, analytics, fraud detection) can subscribe to the same topics via separate consumer groups without modifying existing producers.
- **Ordering guarantees:** By using the order ID as the partition key, we ensure all events for a given order are processed in sequence.

### Negative

- **Increased infrastructure complexity:** Kafka (even managed via MSK) is significantly more complex than REST. The team needs to understand topics, partitions, consumer groups, offsets, and retention policies.
- **Eventual consistency:** The system moves from synchronous request-response to eventual consistency. The Order Service will not know the payment result immediately; it must handle an intermediate "payment pending" state and update asynchronously.
- **New failure modes:** We must handle scenarios like message serialization errors, consumer lag, partition rebalancing, and poison-pill messages (dead letter queues).
- **Monitoring and observability:** We need new tooling to monitor consumer lag, broker health, and message throughput. AWS CloudWatch with MSK metrics, plus potentially a tool like Conduktor or Kafka UI.
- **Learning curve:** With a team of 6, at least 2-3 engineers will need to develop proficiency with Kafka concepts and MSK operations. This is a meaningful investment.
- **Cost:** Amazon MSK has a baseline cost for broker instances regardless of traffic. For our scale this is manageable, but it is higher than the zero-infrastructure-cost of REST.

### Operational changes required

- **Order Service changes:** Replace REST client call with Kafka producer. Implement an event handler to consume payment result events and update order status.
- **Payment Service changes:** Replace REST endpoint with Kafka consumer. Publish payment result events after processing.
- **New "pending" order state:** The Order Service needs a `PAYMENT_PENDING` status in its state machine, with timeout handling if no payment result arrives within a threshold.
- **Dead letter topic:** Configure a DLT for messages that fail processing after a set number of retries.
- **Schema management:** Adopt a schema registry (e.g., AWS Glue Schema Registry) to manage event schemas and ensure backward compatibility as events evolve.
- **Infrastructure provisioning:** Set up Amazon MSK cluster (recommend starting with 3 brokers, `kafka.m5.large`), configure topics, and set up monitoring dashboards.

## Implementation Notes

- **Rollout strategy:** Implement the Kafka path alongside the existing REST path. Use a feature flag to gradually shift traffic from REST to Kafka. Monitor for issues before fully cutting over.
- **Target topics:** `orders.created`, `payments.completed`, `payments.failed`
- **Partition strategy:** Use order ID as the partition key to maintain per-order event ordering.
- **Retention:** 7-day retention for operational topics; adjust based on replay and debugging needs.
- **Estimated timeline:** 3-4 weeks for core implementation and testing, with an additional 1-2 weeks for production rollout and monitoring stabilization.
