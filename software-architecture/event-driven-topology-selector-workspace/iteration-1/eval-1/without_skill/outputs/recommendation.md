# Order Fulfillment System — Event-Driven Architecture Recommendation

## Overview

For your order fulfillment system, I recommend using a **mediator (orchestration) pattern** rather than a broker (choreography) pattern. Here's why.

## Why Mediator?

The key requirement is that "if payment fails, we need to rollback the inventory reservation." This implies a coordinated workflow where:

1. Steps have dependencies on each other
2. Failure in one step must trigger compensating actions in other steps
3. The system needs to know the overall state of the order process

A mediator (orchestrator) is the right choice because it can:
- Coordinate the sequence of steps
- Handle errors by triggering compensating transactions
- Track the state of the overall workflow
- Restart failed workflows

## Suggested Architecture

Use an orchestration service (e.g., a Saga orchestrator) that manages the order workflow:

1. **Order Service** receives the order request
2. **Orchestrator** manages the workflow:
   - Calls Inventory Service to reserve inventory
   - Calls Payment Service to charge payment
   - If payment fails, calls Inventory Service to release reservation
   - Calls Notification Service to send confirmation
   - Calls Warehouse Service to update inventory
   - Calls Shipping Service to initiate shipping

## Technology Suggestions

- **Message Broker:** RabbitMQ or Apache Kafka
- **Orchestration:** Use the Saga pattern with a saga orchestrator
- **Framework:** Consider using a workflow engine like Temporal or Camunda

## Error Handling

- Implement the **Saga pattern** with compensating transactions
- Each step has a corresponding compensation action:
  - Reserve inventory ↔ Release inventory
  - Charge payment ↔ Refund payment
  - Create shipment ↔ Cancel shipment
- Use dead letter queues for messages that fail repeatedly

## Trade-offs

**Advantages of this approach:**
- Clear workflow control
- Error handling and rollback capabilities
- Easier to debug and monitor

**Disadvantages:**
- The orchestrator is a single point of failure
- Slightly lower performance due to coordination overhead
- More complex to implement initially

## Alternative: Choreography

If your requirements were simpler (all steps independent, no rollback needed), a choreography/broker pattern would be better for scalability and loose coupling. But given your rollback requirements, orchestration is the clear choice.
