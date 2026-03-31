# Event-Driven Topology Recommendation: Social Media Content Processing

## Request-Based vs Event-Based Assessment
**Model selected:** Event-based
**Rationale:** Content posting is a reactive event — when a user creates a post, multiple subsystems must react to that occurrence. This is not a data retrieval request; it's a situation the system must respond to. The processing is fire-and-forget from the user's perspective (they don't wait for all 5 downstream systems to complete). Classic event-based model.

## Workflow Analysis

| Workflow | Steps | Dependencies | Error Handling Need | Topology |
|----------|-------|:---:|:---:|:---:|
| Post-created processing | Update feeds, notify followers, content moderation, update search index, generate analytics | Independent — none depends on the others | Low — each processor handles its own errors independently | Broker |

### Step Dependencies Mapped

The user explicitly stated: "These are all independent — none depends on the others." This is a critical input. Let's verify:

- **Update user's feed** — standalone, reads post data, updates feed store
- **Notify followers** — standalone, reads post data + follower list, sends notifications
- **Content moderation** — standalone, analyzes post content, flags if needed
- **Update search index** — standalone, indexes post content
- **Generate analytics events** — standalone, records metrics

**Confirmed: all 5 steps are independent.** No step requires the output of another. No ordering constraints. If content moderation flags the post, that's a separate subsequent workflow — it doesn't block or affect the other 4 processors in this event chain.

## Topology Decision

### Selected: Broker

**Primary driver:** All processing steps are independent. No workflow coordination is needed. Maximum scalability and performance with no mediator overhead.

### 7-Dimension Trade-off Assessment

| Dimension | This System's Need | Broker | Mediator | Fit |
|-----------|-------------------|:---:|:---:|:---:|
| Workflow control | LOW — no coordination needed, all steps independent | Low | High | Broker (no need to pay for coordination) |
| Error handling | LOW — each processor handles its own errors | Low | High | Broker (independent error handling is fine) |
| Recoverability | LOW — individual processor recovery, not workflow-level | Low | High | Broker (per-processor recovery is sufficient) |
| Restart capability | LOW — retry individual events, not workflow | Low | High | Broker |
| Scalability | HIGH — viral posts can trigger millions of notifications | High | Moderate | Broker |
| Performance | HIGH — real-time feed updates expected | High | Moderate | Broker |
| Fault tolerance | HIGH — one processor down shouldn't affect others | High | Low | Broker |

**Score: 7/7 dimensions favor broker.** Unambiguous broker selection.

### Why NOT mediator?

Adding a mediator here would:
- Introduce a coordinator that adds latency to every event
- Create a single point of failure (mediator down = all processing stops)
- Couple processors to the mediator's workflow definition
- Add complexity with zero benefit — there's nothing to coordinate

A mediator is overhead without value when steps are independent.

## Event Flow Design

```
Initiating Event: post-created
├── [post-created topic] ──→ FeedUpdater processor ──→ publishes [feed-updated]
├── [post-created topic] ──→ FollowerNotifier processor ──→ publishes [followers-notified]
├── [post-created topic] ──→ ContentModerator processor ──→ publishes [content-moderated]
├── [post-created topic] ──→ SearchIndexer processor ──→ publishes [search-indexed]
└── [post-created topic] ──→ AnalyticsRecorder processor ──→ publishes [analytics-recorded]
```

All 5 processors subscribe to the `post-created` topic. They process the event in parallel. Each publishes its own processing event advertising what it did — even if no one currently listens. This provides architectural extensibility:

- Future: a "post-reach estimator" could subscribe to `followers-notified`
- Future: a "content appeal handler" could subscribe to `content-moderated`
- Future: a "trending detector" could subscribe to `analytics-recorded`

Note: processing events use past tense (things that HAPPENED), not imperative commands. This is the correct semantic for broker topology.

## Error Handling Strategy

**Per-processor error handling (no central coordination needed):**

Each processor handles its own errors independently:

| Processor | Error Scenario | Handling |
|-----------|---------------|----------|
| FeedUpdater | Feed store unavailable | Retry with exponential backoff; dead letter queue after 3 failures |
| FollowerNotifier | Notification service throttled | Queue backpressure; process in batches |
| ContentModerator | ML model timeout | Retry; flag for manual review if persistent |
| SearchIndexer | Index service down | Retry; search will be eventually consistent |
| AnalyticsRecorder | Analytics store full | Buffer locally; batch write when available |

**Data loss prevention across all three links:**

| Link | Failure Mode | Mitigation |
|------|-------------|------------|
| **Link 1: Message send** | Post service publishes post-created but message doesn't reach broker | Synchronous send with broker acknowledgment. Post service confirms the message was persisted before returning success to the user. |
| **Link 2: Message processing** | Processor dequeues post-created but crashes mid-processing | Client acknowledge mode. Message stays on the topic/queue until consumer explicitly acks. On crash, message is redelivered (ensure idempotent processing). |
| **Link 3: Post-processing** | Processor completes work but database/store write fails | Last participant support where applicable. For analytics and search indexing, eventual consistency with retry is acceptable. For feed updates, use transactional outbox pattern. |

**Dead letter queues:** Each processor has its own DLQ. Failed events are routed to the processor-specific DLQ for monitoring and manual intervention. This is critical for content moderation — a post that can't be moderated should be flagged, not silently passed through.

## Scaling Considerations

Broker topology shines here because each processor scales independently:

| Processor | Scaling Pattern | Rationale |
|-----------|----------------|-----------|
| FeedUpdater | Scale with write throughput | Feed writes are the hot path |
| FollowerNotifier | Scale with follower count | Viral posts with millions of followers need burst capacity |
| ContentModerator | Scale with ML inference capacity | Moderation throughput is bounded by model inference speed |
| SearchIndexer | Scale with index write throughput | Moderate scaling needs |
| AnalyticsRecorder | Scale with event volume | High volume but low-priority — can lag behind |

The FollowerNotifier is likely the processor that needs the most elastic scaling — a post from a user with 10 million followers generates 10 million notification events. Broker topology handles this naturally: add more FollowerNotifier instances behind the topic, and the broker distributes the load.

## Architecture Characteristics Impact

| Characteristic | Rating | Notes |
|---------------|:---:|-------|
| Performance | 5/5 | No mediator overhead; direct event-to-processor |
| Scalability | 5/5 | Each processor scales independently; critical for viral content |
| Fault tolerance | 5/5 | One processor down doesn't affect the other four |
| Evolutionary | 5/5 | New processors added by subscribing to existing topics |
| Testability | 2/5 | Testing 5 parallel async processors is inherently complex |
