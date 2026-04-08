---
name: event-driven-topology-selector
description: Choose between broker and mediator event-driven topologies based on workflow control needs, error handling requirements, and performance trade-offs. Use this skill whenever the user is designing an event-driven system, choosing between choreography and orchestration, deciding how events should flow between processors, debating broker vs mediator, building async workflows, evaluating event-driven error handling strategies, or comparing request-based vs event-based communication models — even if they don't use the terms "broker" or "mediator."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/event-driven-topology-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [14]
tags: [software-architecture, architecture, event-driven, broker, mediator, choreography, orchestration, async, messaging, error-handling]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "System description and event processing requirements — the skill guides topology selection"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment."
---

# Event-Driven Topology Selector

## When to Use

You are designing or evaluating an event-driven architecture and need to choose between broker topology (decentralized event chains) and mediator topology (centralized event orchestration). Typical situations:

- Building a new event-driven system and need to decide how events flow
- Evaluating whether existing event workflows need central coordination
- Debugging error handling problems in an async system — events are being lost or workflows get stuck
- Comparing choreography vs orchestration for inter-service communication
- Deciding whether a use case is better served by request-based or event-based processing
- System has a mix of simple and complex workflows — need to choose the right topology for each

Before starting, verify:
- Has the team already decided on event-driven architecture? If not, this skill selects the TOPOLOGY within event-driven, not whether to use event-driven at all.
- Does the system have async processing needs? If everything is synchronous request-reply, event-driven may not be the right style — consider request-based model first.

## Context & Input Gathering

### Input Sufficiency Check

This skill depends on understanding the WORKFLOW characteristics, not just the system description. The same system may need different topologies for different workflows.

### Required Context (must have — ask if missing)

- **System description and use cases:** What does the system do? What events need to be processed?
  - Check prompt for: system purpose, event types, processing steps, workflow descriptions
  - If missing, ask: "What does your system do, and what events or workflows need to be processed asynchronously?"

- **Workflow dependencies:** Are processing steps independent or do they depend on each other?
  - Check prompt for: step ordering, conditional logic, rollback needs, parallel vs sequential
  - If missing, ask: "When an event occurs, do the processing steps depend on each other (step B needs step A's result), or can they all happen independently in parallel?"

- **Error handling requirements:** What happens when a processing step fails?
  - Check prompt for: rollback, compensation, retry, notification, data consistency needs
  - If missing, ask: "When a processing step fails (e.g., payment declined), do you need to (a) roll back previous steps, (b) retry automatically, (c) just log and continue, or (d) halt everything until resolved?"
  - **WHY this is critical:** Error handling is the single biggest differentiator between broker and mediator. Broker topology has no built-in error handling — failed events are silently lost unless you build custom recovery.

### Observable Context (gather from environment)

- **Existing messaging infrastructure:** What message brokers or event systems are in place?
  - Look for: RabbitMQ, Kafka, ActiveMQ, AWS SQS/SNS configs, event bus implementations
  - Reveals: whether infrastructure already favors one topology
- **Current event patterns:** Are there existing event handlers or processors?
  - Look for: event handler classes, message consumers, saga implementations
  - Reveals: current topology direction and complexity level

### Default Assumptions

- If error handling requirements unknown, assume they ARE important (safer to recommend mediator and simplify than to recommend broker and discover you need coordination later)
- If workflow complexity unknown, assume moderate complexity (some dependencies between steps)
- If performance requirements unspecified, assume standard (not sub-millisecond)

### Sufficiency Threshold

```
SUFFICIENT: system description + workflow dependencies + error handling needs are known
MUST ASK: error handling requirements are unknown (this drives the entire topology decision)
PROCEED WITH DEFAULTS: workflow dependencies partially known but error handling is clear
```

## Process

### Step 1: Determine If Event-Based Model Is Appropriate

**ACTION:** Evaluate whether the use case is better served by a request-based or event-based processing model.

**WHY:** Not everything should be event-driven. Request-based models are better when processing is data-driven, deterministic, and needs a direct response. Event-based models are better when processing is reactive, requires high responsiveness, and the system must adapt to situations as they arise. Choosing the wrong model wastes the entire topology analysis.

| Dimension | Request-Based | Event-Based |
|-----------|:---:|:---:|
| Communication style | Synchronous | Asynchronous |
| Data access | Request-reply (ask for data) | Fire-and-forget (react to events) |
| Determinism | High — same request gives same path | Lower — event chains are dynamic |
| Responsiveness | Moderate (bound by slowest step) | High (immediate acknowledgment) |
| Typical use case | "Get me the order history" | "A bid was placed, react to it" |
| Workflow control | Easy (caller controls the flow) | Hard (no single controller in broker) |
| Error handling | Straightforward (caller gets error) | Complex (no caller waiting) |

**IF** the use case is purely data-retrieval with synchronous needs, recommend request-based model. Stop here.
**ELSE** proceed to Step 2.

### Step 2: Map the Workflow Characteristics

**ACTION:** For each identified workflow/use case, map its characteristics across the 7 comparison dimensions.

**WHY:** Broker and mediator topologies have opposite strengths. Mapping the workflow against these dimensions prevents gut-feel decisions and reveals which trade-offs matter most for THIS specific system.

For each workflow, evaluate:

| Dimension | Favors Broker | Favors Mediator |
|-----------|:---:|:---:|
| **Workflow control** | No coordination needed — events flow freely | Steps must execute in specific order with conditions |
| **Error handling** | Errors are tolerable or self-healing | Failures require rollback, compensation, or retry coordination |
| **Recoverability** | System can recover organically | Must be able to recover to a known state |
| **Restart capability** | No need to restart a failed workflow | Must restart workflows from point of failure |
| **Scalability need** | Maximum throughput is critical | Moderate throughput is acceptable |
| **Performance need** | Sub-millisecond or very high performance | Standard latency is acceptable |
| **Fault tolerance** | Individual processor failure is acceptable | Single processor failure must not break the chain |

### Step 3: Select the Topology

**ACTION:** Based on the dimension mapping, recommend broker, mediator, or hybrid topology.

**WHY:** The choice is fundamentally a trade-off between workflow control and error handling capability (mediator) versus high performance and scalability (broker). Neither is inherently better — it depends entirely on which dimensions the system prioritizes.

**Decision logic:**

**IF** workflow steps are independent AND error handling is not critical AND performance/scalability are top priorities:
- **Recommend BROKER topology**
- Processors are self-contained, events chain through channels
- No central coordinator — maximum decoupling and performance
- Each processor advertises what it did; other processors react

**IF** workflow steps have dependencies AND error handling/recoverability are important AND workflow must be coordinated:
- **Recommend MEDIATOR topology**
- Central mediator orchestrates the processing steps
- Mediator knows the workflow, manages state, handles errors
- Processing events are commands (things to do) not events (things that happened)

**IF** system has BOTH types of workflows:
- **Recommend HYBRID topology**
- Use mediator for complex workflows requiring coordination
- Use broker for simple, independent event chains
- Route through a simple mediator that classifies events and delegates

### Step 4: Determine Mediator Complexity Level (If Mediator Selected)

**ACTION:** If mediator topology was selected, determine the appropriate mediator implementation complexity.

**WHY:** Mediators range from simple source-code routers to full BPM engines. Over-engineering the mediator wastes months; under-engineering it creates a bottleneck that can't handle the workflow complexity. Matching mediator complexity to workflow complexity is critical.

| Mediator Type | Use When | Implementation |
|---------------|----------|----------------|
| **Simple mediator** | Linear workflows, basic error handling, routing logic | Source code (e.g., Apache Camel, Spring Integration, custom code) |
| **Hardcoded mediator** | Complex conditional workflows, multiple dynamic paths, structured error handling | BPEL engine (e.g., Apache ODE, Oracle BPEL Process Manager) |
| **Complex mediator (BPM)** | Long-running transactions, human intervention points, complex state machines | BPM engine (e.g., jBPM, Camunda) |

**Classify each event type:** Determine if it's simple, hard, or complex. Route through the simple mediator first — it classifies and delegates to the appropriate mediator type. This delegation model handles mixed-complexity events efficiently.

### Step 5: Address Error Handling and Data Loss Prevention

**ACTION:** Design the error handling strategy based on the selected topology.

**WHY:** Asynchronous event-driven architectures have THREE points where data loss can occur in the async communication chain. Protecting only one point still leaves the system vulnerable at the other two. Most architects only think about the message queue and forget about the send and acknowledgment links.

**The three data loss points:**

1. **Message send (producer to queue):** Event is created but never reaches the queue
   - **Mitigation:** Synchronous send with broker acknowledgment. Use persistent message queues. The producer waits for confirmation that the message was persisted before proceeding.

2. **Message processing (queue to consumer):** Event is dequeued but consumer crashes before processing
   - **Mitigation:** Client acknowledge mode (not auto-acknowledge). The message stays on the queue until the consumer explicitly acknowledges successful processing. If the consumer crashes, the message is re-delivered.

3. **Post-processing (consumer to database):** Event is processed but the database write fails
   - **Mitigation:** Use the last participant support pattern — the database commit and the message acknowledgment happen in the same transaction scope. If the DB fails, the message is not acknowledged and will be redelivered.

**For broker topology error handling:**
- Implement the **workflow event pattern**: a dedicated error-handling event processor monitors for failures and can trigger compensating actions
- Use **dead letter queues** for events that fail repeatedly — prevents infinite retry loops and allows manual inspection

**For mediator topology error handling:**
- The mediator itself manages error state — it knows which step failed and can stop the workflow
- Mediator persists workflow state, enabling restart from point of failure
- Compensating transactions can be orchestrated by the mediator (e.g., reverse payment if shipping fails)

### Step 6: Produce the Topology Recommendation

**ACTION:** Compile the complete topology recommendation with rationale.

**WHY:** The recommendation must be specific enough to implement. A vague "use mediator" without explaining the error handling strategy, data loss prevention, and mediator complexity level leaves the team to figure out the hard parts on their own.

## Inputs

- System description and event processing use cases
- Workflow dependencies and ordering requirements
- Error handling and data consistency requirements
- Performance and scalability targets (if known)

## Outputs

### Event-Driven Topology Recommendation

```markdown
# Event-Driven Topology Recommendation: {System Name}

## Request-Based vs Event-Based Assessment
**Model selected:** {Request-based / Event-based / Mixed}
**Rationale:** {why this model fits}

## Workflow Analysis

| Workflow | Steps | Dependencies | Error Handling Need | Topology |
|----------|-------|:---:|:---:|:---:|
| {workflow 1} | {step list} | Independent / Dependent | Low / Medium / High | Broker / Mediator |
| {workflow 2} | ... | ... | ... | ... |

## Topology Decision

### Selected: {Broker / Mediator / Hybrid}

**Primary driver:** {the dimension that tipped the decision}

### 7-Dimension Trade-off Assessment

| Dimension | This System's Need | Broker | Mediator | Fit |
|-----------|-------------------|:---:|:---:|:---:|
| Workflow control | {need level} | Low | High | {which fits} |
| Error handling | {need level} | Low | High | {which fits} |
| Recoverability | {need level} | Low | High | {which fits} |
| Restart capability | {need level} | Low | High | {which fits} |
| Scalability | {need level} | High | Moderate | {which fits} |
| Performance | {need level} | High | Moderate | {which fits} |
| Fault tolerance | {need level} | High | Low | {which fits} |

## Mediator Complexity (if applicable)
**Level:** {Simple / Hardcoded / Complex (BPM)}
**Implementation suggestion:** {specific technology recommendation}
**Rationale:** {why this complexity level}

## Error Handling Strategy
**Data loss prevention:**
- Message send: {mitigation}
- Message processing: {mitigation}
- Post-processing: {mitigation}

**Error recovery pattern:** {workflow event pattern / dead letter queue / mediator-managed / combination}

## Architecture Characteristics Impact
- Performance: {stars}/5
- Scalability: {stars}/5
- Fault tolerance: {stars}/5
- Evolutionary: {stars}/5
- Testability: {stars}/5
```

## Key Principles

- **The choice is workflow control vs performance** — Broker topology maximizes performance, scalability, and decoupling. Mediator topology maximizes workflow control, error handling, and recoverability. Neither is inherently better. The decision hinges on which of these your system values more.

- **Events vs commands reveal the topology** — In broker topology, processing events describe what HAPPENED (order-created, payment-applied). In mediator topology, processing events are COMMANDS telling processors what to DO (place-order, apply-payment). If your events are naturally commands with expected outcomes, you need a mediator.

- **Error handling is the deal-breaker** — If a processing step can fail and the failure requires coordinated recovery (rollback, compensation, retry), broker topology cannot handle this without significant custom infrastructure. The mediator exists precisely for this scenario. When in doubt about error handling needs, lean toward mediator.

- **Protect all three links in the async chain** — Data loss can occur at message send, message processing, and post-processing. Most architects only protect the message queue itself (persistence) but forget about the send confirmation and the consumer acknowledgment. All three must be addressed.

- **Hybrid is often the right answer** — Real systems rarely have uniformly simple or uniformly complex workflows. A simple mediator that classifies incoming events and delegates simple ones to broker-style processing while routing complex ones through a full mediator gives the best of both worlds.

- **Match mediator complexity to workflow complexity** — Using a BPM engine for simple routing wastes months of effort. Using source-code routing for complex workflows with human intervention points creates unmaintainable spaghetti. Classify your events (simple/hard/complex) and pick the mediator type accordingly.

## Examples

**Scenario: Order fulfillment with payment rollback**
Trigger: "We're building an order fulfillment system. When a customer places an order, we need to validate inventory, charge payment, send confirmation email, update warehouse, and notify shipping. If payment fails, we need to rollback the inventory reservation."
Process: Mapped workflow — steps have dependencies (payment must succeed before fulfillment). Error handling is critical (payment failure requires inventory rollback). This is a coordinated workflow with compensation requirements. Evaluated 7 dimensions: workflow control = high need, error handling = high need, recoverability = high need. Performance and scalability are standard. All three critical dimensions favor mediator.
Output: **Mediator topology.** Simple mediator implementation (source code, e.g., custom orchestrator or Apache Camel). 5-step workflow: (1) create order, (2) process order (email + payment + inventory in parallel), (3) fulfill order, (4) ship order, (5) notify customer. Mediator waits for acknowledgment from parallel step 2 processors before proceeding. If payment fails at step 2, mediator triggers inventory rollback and halts workflow. Data loss prevention: persistent queues with synchronous send, client-acknowledge mode, last-participant-support for DB writes.

**Scenario: Social media fan-out with independent processors**
Trigger: "Users post content that needs to: update feeds, notify followers, run content moderation, update search index, and generate analytics. These are all independent."
Process: Mapped workflow — all steps are independent (no ordering, no dependencies). Error handling is low priority (if search indexing fails, it can retry independently without affecting other steps). Evaluated 7 dimensions: workflow control = not needed, error handling = low (each processor handles its own), scalability = high (viral posts need fan-out), performance = high (real-time feed updates). All critical dimensions favor broker.
Output: **Broker topology.** Post-created initiating event fans out to 5 independent event processors. Each processor publishes its own processing event (feed-updated, followers-notified, etc.) for extensibility. No mediator needed — processors are self-contained. Dead letter queues for each processor to catch persistent failures. Per-processor scaling based on load.

**Scenario: Mixed workloads — trading platform with compliance**
Trigger: "Trade events need sub-millisecond processing. We also have compliance reporting that aggregates trades daily with complex rules."
Process: Identified two distinct workflows. Trade execution: independent, performance-critical, fault-tolerant — classic broker. Compliance reporting: complex rules, conditional paths, must complete all steps, needs audit trail — classic mediator. Recommended hybrid topology.
Output: **Hybrid topology.** Trade execution path uses broker topology for maximum performance — trade-executed events fan out to position tracking, risk calculation, and P&L processors independently. Compliance reporting path uses mediator topology — daily compliance mediator orchestrates trade aggregation, rule evaluation, exception flagging, and report generation in sequence. Simple event router at entry point classifies events by type and delegates to the appropriate topology. Trade path uses Kafka for high-throughput; compliance path uses RabbitMQ with a lightweight orchestrator.

## References

- For the detailed broker vs mediator comparison table with full trade-off analysis, see [references/broker-vs-mediator-comparison.md](references/broker-vs-mediator-comparison.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
