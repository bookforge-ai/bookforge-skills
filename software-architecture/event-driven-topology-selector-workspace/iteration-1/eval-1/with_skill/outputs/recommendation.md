# Event-Driven Topology Recommendation: Order Fulfillment System

## Request-Based vs Event-Based Assessment
**Model selected:** Event-based
**Rationale:** Order placement is a reactive event (customer places order, system must react). Multiple downstream processes need to be triggered. The system benefits from asynchronous processing — the customer doesn't need to wait for warehouse notification or shipping setup to complete. This is clearly an event-based use case, not a data retrieval request.

## Workflow Analysis

| Workflow | Steps | Dependencies | Error Handling Need | Topology |
|----------|-------|:---:|:---:|:---:|
| Order fulfillment | Validate inventory, charge payment, send confirmation, update warehouse, notify shipping | Dependent — payment must succeed before fulfillment proceeds; inventory must be validated before payment | High — payment failure requires inventory rollback | Mediator |

### Step Dependencies Mapped

The steps are NOT independent. The explicit requirement "if payment fails, we need to rollback the inventory reservation" reveals a critical ordering dependency:

1. **Validate inventory** (must succeed before payment)
2. **Charge payment** (must succeed before fulfillment; failure triggers rollback of step 1)
3. **Send confirmation email** (only after payment succeeds)
4. **Update warehouse system** (only after payment succeeds)
5. **Notify shipping** (only after warehouse is updated)

Steps 3 and 4 can run concurrently after payment succeeds. Step 5 depends on step 4.

## Topology Decision

### Selected: Mediator

**Primary driver:** Error handling with compensation. The requirement "if payment fails, rollback inventory reservation" is a compensation pattern that requires coordinated awareness of the workflow state — exactly what a mediator provides.

### 7-Dimension Trade-off Assessment

| Dimension | This System's Need | Broker | Mediator | Fit |
|-----------|-------------------|:---:|:---:|:---:|
| Workflow control | HIGH — steps have ordering dependencies | Low | High | Mediator |
| Error handling | HIGH — payment failure requires inventory rollback | Low | High | Mediator |
| Recoverability | HIGH — must recover to known state on failure | Low | High | Mediator |
| Restart capability | MEDIUM — should restart from point of failure | Low | High | Mediator |
| Scalability | MEDIUM — standard e-commerce scale | High | Moderate | Either |
| Performance | MEDIUM — standard response time acceptable | High | Moderate | Either |
| Fault tolerance | MEDIUM — individual processor failure should not corrupt order state | High | Low | Broker (but mediator's error handling compensates) |

**Score: 4 dimensions favor mediator, 1 favors broker, 2 are neutral.** Clear mediator selection.

### Why NOT broker?

With broker topology, when payment fails:
- The Inventory processor has already received the order-created event and decremented stock
- No component is aware that payment failed
- No component knows it needs to reverse the inventory reservation
- The customer's inventory is "reserved" for an order that will never be fulfilled

You could build a workflow event pattern to detect this, but that essentially recreates mediator coordination on top of broker infrastructure — added complexity with no benefit over just using a mediator.

## Mediator Complexity

**Level:** Simple mediator (source code)
**Implementation suggestion:** Custom orchestrator in your application framework (e.g., Spring Integration, NestJS saga, or a custom state machine). Apache Camel if you want a lightweight integration framework.
**Rationale:** The workflow is linear with one conditional branch (payment success/failure). No human intervention points. No long-running transactions requiring BPM. A source-code mediator with explicit steps handles this well without the overhead of BPEL or BPM engines.

### Mediator Workflow Design

```
Step 1: Create Order
  - Send create-order command to OrderPlacement processor
  - Wait for acknowledgment with order ID
  - Mediator may return order ID to customer at this point

Step 2: Process Order (concurrent within step)
  - Send validate-inventory command to Inventory processor
  - Wait for acknowledgment (inventory reserved)
  - Send apply-payment command to Payment processor
  - Wait for acknowledgment
  - IF payment fails:
      → Send rollback-inventory command to Inventory processor
      → Send payment-failed notification to Notification processor
      → HALT workflow, record failure state
  - Send email-customer command to Notification processor (confirmation)

Step 3: Fulfill Order (concurrent within step)
  - Send fulfill-order command to OrderFulfillment processor
  - Send update-warehouse command to Warehouse processor
  - Wait for both acknowledgments

Step 4: Ship Order
  - Send ship-order command to Shipping processor
  - Wait for acknowledgment

Step 5: Notify Customer
  - Send email-customer (shipped) command to Notification processor
```

Note the semantic distinction: these are COMMANDS (things to do), not events (things that happened). The mediator tells processors WHAT to do; processors don't advertise what they did.

## Error Handling Strategy

**Data loss prevention across all three links:**

| Link | Failure Mode | Mitigation |
|------|-------------|------------|
| **Link 1: Message send** | Mediator sends command but it doesn't reach the processor's queue | Synchronous send with broker acknowledgment. Mediator blocks until the message broker confirms the command message was persisted to the queue. |
| **Link 2: Message processing** | Processor dequeues command but crashes before completing | Client acknowledge mode. The command message stays on the queue until the processor explicitly acknowledges completion. If processor crashes, message is redelivered to another instance. |
| **Link 3: Post-processing** | Processor completes work but database write fails | Last participant support. Database commit and message acknowledgment happen in the same transaction scope. If DB write fails, message is not acknowledged and will be redelivered. |

**Compensation pattern for payment failure:**
1. Mediator sends validate-inventory command, receives acknowledgment (inventory reserved)
2. Mediator sends apply-payment command, receives error (payment declined)
3. Mediator sends rollback-inventory command to release the reservation
4. Mediator sends payment-failed notification to customer
5. Mediator records the order as failed with reason, persists state for potential retry

**Dead letter queue:** Configure a dead letter queue for commands that fail processing after 3 retry attempts. Monitor for manual resolution.

## Architecture Characteristics Impact

| Characteristic | Rating | Notes |
|---------------|:---:|-------|
| Performance | 3/5 | Mediator adds coordination overhead, but acceptable for e-commerce |
| Scalability | 3/5 | Mediator is potential bottleneck; mitigate with per-domain mediators |
| Fault tolerance | 4/5 | Mediator manages failures; mediator itself needs HA deployment |
| Evolutionary | 5/5 | New steps added to mediator workflow without changing processors |
| Testability | 3/5 | Mediator workflow is testable; async processing adds complexity |
