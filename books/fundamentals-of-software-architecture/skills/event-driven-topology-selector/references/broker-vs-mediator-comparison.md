# Broker vs Mediator Topology — Detailed Comparison

Read this reference when you need the full trade-off details for broker and mediator topologies, including architecture characteristics ratings, implementation guidance, and anti-pattern warnings.

## Topology Overview

### Broker Topology

**Architecture components:** Initiating event, event broker (message broker), event processors, processing events.

**How it works:**
1. An initiating event enters the system (e.g., PlaceOrder)
2. The event is sent to an event channel in the event broker
3. A single event processor picks up the initiating event and processes it
4. That processor advertises what it did by publishing a processing event
5. Other processors react to the processing event, do their work, and publish their own processing events
6. This chain continues until no processor is interested in the latest processing event

**Key metaphor:** A relay race. Each runner (processor) takes the baton, runs their leg, and hands off. Once they hand off, they're done. No coach (mediator) tells them what to do.

**Event broker implementation:** Usually federated (multiple domain-based clustered instances). Uses topics (publish-subscribe) for the fire-and-forget broadcasting model. Technologies: RabbitMQ, ActiveMQ, HornetQ, Kafka.

**Best practice:** Every event processor should advertise what it did, even if no other processor currently cares. This provides architectural extensibility — new processors can tap into existing event streams without modifying the producers.

### Mediator Topology

**Architecture components:** Initiating event, event queue, event mediator, event channels, event processors.

**How it works:**
1. An initiating event enters the system and is placed on an event queue
2. The event mediator picks up the event from the queue
3. The mediator knows the workflow steps required to process this event
4. The mediator generates processing events (commands) sent to dedicated event channels (point-to-point queues)
5. Event processors listen on their dedicated channels, process the command, and respond back to the mediator
6. The mediator waits for acknowledgment before proceeding to the next step
7. Steps within a workflow group execute concurrently; steps across groups execute serially

**Key metaphor:** An orchestra conductor. The conductor (mediator) knows the score (workflow), directs each section (processors) when to play, and coordinates the overall performance.

**Processing event semantics:** In the mediator topology, processing events are COMMANDS — things that NEED to happen (place-order, send-email, apply-payment). In broker topology, they are EVENTS — things that HAVE happened (order-created, email-sent, payment-applied). This semantic difference is fundamental.

## Trade-Off Comparison Table

### Broker Topology

| Advantage | Detail |
|-----------|--------|
| Highly decoupled event processors | Processors don't know about each other. Adding/removing processors requires no changes to others. |
| High scalability | Each processor scales independently. No bottleneck from a central coordinator. |
| High responsiveness | Events are processed as they arrive. No waiting for a coordinator to schedule. |
| High performance | No intermediary adds latency. Direct event-channel-to-processor communication. |
| High fault tolerance | One processor failing doesn't affect others. The broker provides back-pressure. |

| Disadvantage | Detail |
|-------------|--------|
| Workflow control | No component knows the overall workflow state. No one knows when a business transaction is "complete." |
| Error handling | If a processor crashes mid-processing, no component is aware. The business process gets stuck with no automatic recovery. Other processors continue as if everything is fine. |
| Recoverability | Because no component owns the workflow state, there's no way to recover to a known good state. |
| Restart capabilities | Cannot restart from point of failure. The initiating event has already been consumed and processed. Re-submitting it would duplicate work. |
| Data inconsistency | With no coordination, processors can get out of sync. Inventory may be decremented even when payment failed. |

### Mediator Topology

| Advantage | Detail |
|-----------|--------|
| Workflow control | The mediator knows the complete workflow. It knows which steps are done, which are pending, and what comes next. |
| Error handling | The mediator receives error responses from processors. It can stop the workflow, trigger compensation, or retry. |
| Recoverability | The mediator persists workflow state. If the mediator crashes, it can recover and resume from its persisted state. |
| Restart capabilities | Workflows can restart from the point of failure. The mediator knows exactly where the workflow stopped. |
| Better data consistency | The mediator coordinates steps, ensuring downstream steps don't execute until upstream steps succeed. |

| Disadvantage | Detail |
|-------------|--------|
| More coupling of event processors | Processors are coupled to the mediator's command structure. Adding a new step means changing the mediator. |
| Lower scalability | The mediator is a potential bottleneck. Although you can have multiple mediators per domain, each mediator instance is a single point of coordination. |
| Lower performance | The mediator adds an intermediary hop. Processing events go: processor -> mediator -> next processor, rather than processor -> broker -> next processor directly. |
| Lower fault tolerance | If the mediator goes down, all workflows it manages are halted. This is a single point of failure per domain. |
| Modeling complex workflows | Declaratively modeling dynamic, conditional processing in a mediator (especially BPEL) is difficult. Many workflows end up as hybrid (mediator for general flow, broker for dynamic parts). |

## 7-Dimension Direct Comparison

| Dimension | Broker | Mediator | Notes |
|-----------|:---:|:---:|-------|
| Workflow control | Low | High | The defining trade-off. Broker has NO workflow awareness. |
| Error handling | Low | High | Broker: errors are silent. Mediator: errors are caught and managed. |
| Recoverability | Low | High | Broker: no state to recover. Mediator: persists workflow state. |
| Restart | Low | High | Broker: can't restart. Mediator: restarts from point of failure. |
| Scalability | High | Moderate | Broker: no bottleneck. Mediator: coordinator can bottleneck. |
| Performance | High | Moderate | Broker: direct communication. Mediator: extra hop through coordinator. |
| Fault tolerance | High | Low | Broker: isolated failures. Mediator: coordinator is SPOF. |

## Architecture Characteristics Ratings (Event-Driven Overall)

| Characteristic | Rating | Notes |
|---------------|:---:|-------|
| Partitioning type | Technical | Events and processors organized by processing type |
| Number of quanta | 1 to many | Depends on topology and processor isolation |
| Deployability | 2/5 | Complex deployment due to event contracts and processor dependencies |
| Elasticity | 3/5 | Processors can scale independently (better in broker) |
| Evolutionary | 5/5 | Excellent — new processors added without changing existing ones |
| Fault tolerance | 5/5 | Processor isolation prevents cascading failures (better in broker) |
| Modularity | 4/5 | Good separation of processing concerns |
| Overall cost | 3/5 | Moderate — messaging infrastructure adds cost |
| Performance | 5/5 | Async processing eliminates blocking (better in broker) |
| Reliability | 3/5 | Moderate — async complexity can reduce reliability |
| Scalability | 5/5 | Excellent processor-level scaling (better in broker) |
| Simplicity | 1/5 | Low — async event flows are inherently complex to reason about |
| Testability | 2/5 | Low — testing async event chains is difficult |

## Mediator Complexity Levels — Detailed Guide

### Simple Mediator (Source Code)

**When to use:**
- Events require simple error handling and orchestration
- Workflows are mostly linear with basic conditional branching
- No long-running transactions or human intervention points

**Implementation options:** Apache Camel, Mule ESB, Spring Integration, custom source code (Java, C#, etc.)

**How it works:** Message flows and routes are written in programming code. The mediator intercepts events, classifies them (simple/hard/complex), and either processes them directly or delegates to more capable mediators.

**Advantages:** Easy to write and maintain. Fast to develop. Good for 80% of events.

### Hardcoded Mediator (BPEL)

**When to use:**
- Complex conditional processing with multiple dynamic paths
- Structured error handling with redirection and multicasting
- Workflows that are well-defined but have many branches

**Implementation options:** Apache ODE, Oracle BPEL Process Manager

**How it works:** Uses Business Process Execution Language (BPEL), an XML-like structure describing processing steps, error handling, redirection, and multicasting. Usually created via graphical interface tools.

**Advantages:** Declarative workflow definition. Good tooling for visualization. Handles complex branching well.

**Limitations:** Does NOT handle long-running transactions with human intervention. BPEL is powerful but relatively complex to learn.

### Complex Mediator (BPM)

**When to use:**
- Long-running transactions requiring human intervention
- Workflows that pause and wait for external actions (approvals, manual reviews)
- Complex state machines with many possible states

**Implementation options:** jBPM, Camunda, Activiti

**How it works:** Uses Business Process Management engines that support human task management, timers, complex state transitions, and long-running process instances.

**Example:** A stock trade where the mediator must pause processing, notify a senior trader for manual approval (because the trade exceeds a threshold), and wait for the approval before continuing.

**Advantages:** Handles human-in-the-loop workflows. Persistent process state. Resume from any point.

**Limitations:** Heavy infrastructure. Overkill for simple event routing.

### Mediator Delegation Model

Given that real systems have a MIX of simple, hard, and complex events, the recommended approach is:

1. ALL events enter through a **Simple Event Mediator** (source code)
2. The simple mediator classifies each event as simple, hard, or complex
3. Simple events are processed directly by the simple mediator
4. Hard events are forwarded to the **BPEL mediator**
5. Complex events are forwarded to the **BPM mediator**

This delegation model ensures each event type is processed by the mediator with the appropriate capability level, without over-engineering simple cases or under-engineering complex ones.

## Error Handling Patterns

### Workflow Event Pattern (Broker Topology)

Since broker topology has no central coordinator for error handling, the **workflow event pattern** provides a mechanism:

1. A dedicated **workflow processor** monitors the event flow
2. When it detects a failure (processor doesn't emit expected processing event within timeout), it generates a corrective workflow event
3. Other processors react to the corrective event (e.g., reverse inventory, issue refund)

**Limitation:** This effectively rebuilds mediator-like coordination on top of broker topology. If you need extensive use of this pattern, you probably need a mediator.

### Dead Letter Queues

For events that fail processing repeatedly:

1. After N retry attempts, move the failed event to a **dead letter queue**
2. Dead letter queues are monitored for manual inspection and resolution
3. Prevents infinite retry loops that waste resources
4. Provides an audit trail of failed events

### Data Loss Prevention — The Three-Link Chain

Every asynchronous message exchange has three potential failure points:

```
[Producer] ---(Link 1)---> [Message Queue] ---(Link 2)---> [Consumer] ---(Link 3)---> [Database]
```

| Link | Failure Mode | Prevention |
|------|-------------|------------|
| **Link 1: Send** | Producer sends message but it doesn't reach the queue (network failure, broker down) | Use **synchronous send** with broker acknowledgment. Producer blocks until broker confirms message persistence. |
| **Link 2: Processing** | Message is dequeued but consumer crashes before completing processing | Use **client acknowledge mode** (not auto-acknowledge). Message stays on queue until consumer explicitly acknowledges. On crash, message is redelivered to another consumer instance. |
| **Link 3: Post-processing** | Consumer processes message but database write fails | Use **last participant support** pattern. Database commit and message acknowledgment are in the same transaction scope. If DB fails, message is not acknowledged and will be redelivered. |

**Critical insight:** Most architects protect only Link 2 (persistent message queues). This still leaves data loss at Link 1 (fire-and-forget sends) and Link 3 (process-then-ack without DB transaction). ALL THREE links must be protected for reliable event processing.

## Request-Based vs Event-Based Model Comparison

Use this table when deciding whether a use case should be event-driven at all, before selecting broker vs mediator.

| Dimension | Request-Based | Event-Based |
|-----------|:---:|:---:|
| **Communication** | Synchronous request-reply | Asynchronous fire-and-forget |
| **Coupling** | Higher (caller knows the callee) | Lower (publisher doesn't know subscribers) |
| **Data pattern** | Pull: ask for data | Push: react to occurrences |
| **Determinism** | High: same request, same processing path | Lower: event chains are dynamic |
| **Responsiveness** | Bound by total processing time | Immediate acknowledgment |
| **Scalability** | Limited by synchronous chain | High: processors scale independently |
| **Error handling** | Simple: caller gets error response | Complex: no caller waiting for response |
| **Workflow visibility** | Clear: follow the request path | Opaque: follow event chains across processors |

**Use request-based when:** Retrieving data, synchronous operations, well-defined request-response patterns, when the caller needs an immediate answer.

**Use event-based when:** Reacting to situations, high responsiveness needed, fire-and-forget operations, multiple independent processors need to react to the same occurrence.
