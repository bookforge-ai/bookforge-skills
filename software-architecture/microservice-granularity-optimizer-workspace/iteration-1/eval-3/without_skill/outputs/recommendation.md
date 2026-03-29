# Distributed Transaction Design: E-Commerce Order Placement

## Architecture Overview

For handling distributed transactions across inventory, payment, and shipping services, I recommend the Saga pattern with an event-driven approach.

## Services

1. **OrderService** - Manages order lifecycle
2. **InventoryService** - Manages stock
3. **PaymentService** - Processes payments
4. **ShippingService** - Creates shipments

## Saga Implementation

Use an event-driven choreographed saga with a message broker (Kafka):

### Happy Path:
1. OrderService creates order, publishes `OrderCreated` event
2. InventoryService receives event, reserves items, publishes `InventoryReserved` event
3. PaymentService receives event, charges payment, publishes `PaymentCompleted` event
4. ShippingService receives event, creates shipment, publishes `ShipmentCreated` event
5. OrderService receives event, marks order as confirmed

### Failure Path (Payment fails):
1. PaymentService publishes `PaymentFailed` event
2. InventoryService receives event, releases reservation
3. OrderService receives event, marks order as failed

## Technology Stack

- **Message Broker:** Apache Kafka for event streaming
- **Event Store:** MongoDB for saga state
- **Service Framework:** Spring Boot with Spring Cloud Stream
- **Databases:** PostgreSQL per service

## Code Example (Spring Boot)

```java
@Service
public class OrderSagaManager {

    @KafkaListener(topics = "payment-events")
    public void handlePaymentEvent(PaymentEvent event) {
        if (event.getStatus() == PaymentStatus.FAILED) {
            // Publish compensation event
            kafkaTemplate.send("inventory-commands",
                new ReleaseInventoryCommand(event.getOrderId()));
            orderRepository.updateStatus(event.getOrderId(), OrderStatus.FAILED);
        }
    }
}
```

## Idempotency

Ensure all operations are idempotent:
- Use unique transaction IDs for payment processing
- Use reservation IDs for inventory operations
- Implement deduplication in Kafka consumers

## Monitoring

- Use Kafka consumer group lag monitoring
- Implement a saga dashboard showing pending/completed/failed sagas
- Set up alerts for sagas stuck in pending state > 5 minutes

## Considerations

- Eventual consistency: users may briefly see reserved inventory that's being charged
- Handle duplicate events through idempotency keys
- Consider using Temporal.io or Camunda for more complex saga orchestration
- Implement a dead letter queue for failed compensations
