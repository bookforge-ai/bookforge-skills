# Social Media Platform — Event-Driven Architecture Recommendation

## Recommendation: Broker (Choreography) Pattern

Since all your processing steps are independent, the **broker/choreography pattern** is the best fit.

## Why Broker?

- **Independence:** Each processor (feed update, notifications, moderation, search, analytics) works independently
- **Scalability:** Each processor can scale independently based on its own load
- **Loose coupling:** Processors don't need to know about each other
- **Performance:** No central coordinator adding latency

## Architecture

When a post is created:
1. Publish a `post.created` event to a message broker (e.g., Kafka or RabbitMQ)
2. Each processor subscribes to this event and processes it independently:
   - Feed Service: Updates user's feed
   - Notification Service: Notifies followers
   - Moderation Service: Runs content moderation
   - Search Service: Updates search index
   - Analytics Service: Generates analytics events

## Technology Recommendations

- **Apache Kafka** is ideal here because:
  - High throughput for large volumes of events
  - Multiple consumer groups can read the same events independently
  - Built-in partitioning for scalability
  - Event replay capability for reprocessing

## Error Handling

Since processors are independent:
- Each processor handles its own errors
- Use retry mechanisms with exponential backoff
- Dead letter queues for failed messages
- Each processor can fail and recover without affecting others

## Considerations

- **Content moderation timing:** If moderation needs to happen BEFORE the post appears in feeds, you'd need to rethink this — that would introduce a dependency
- **Eventual consistency:** Feed updates, search indexing, and analytics will be eventually consistent
- **Idempotency:** Make sure each processor can handle duplicate events safely

## When You'd Need Orchestration Instead

If in the future you need:
- Moderation to block posts before they appear in feeds
- A specific ordering of processing steps
- Compensating transactions

Then you'd want to add orchestration for that specific workflow.
