# Broker Selection Framework

Reference for Step 1 of `stream-processing-designer`.

---

## Taxonomy

### Traditional message brokers (JMS/AMQP style)

Examples: RabbitMQ, ActiveMQ, HornetQ, IBM MQ, Azure Service Bus, Amazon SQS, Google Cloud Pub/Sub (JMS mode)

Standard: JMS (Java Message Service) and AMQP define the interface. Behavior varies by implementation.

Key characteristics:
- Messages are deleted from the broker once successfully delivered and acknowledged
- Consumers register; the broker assigns individual messages to consumers (load balancing)
- Fan-out via topic subscriptions or exchange bindings (AMQP), but the default model is queue-per-consumer
- Broker maintains very little history — working assumption is the queue is short
- Secondary indexes not supported; topic subscriptions provide some filtering
- Clients are notified when new messages arrive (push model)

Operational implication: If a consumer is shut down, its queue must be explicitly deleted. Otherwise it accumulates messages and consumes broker memory. Contrast with log-based brokers where a stopped consumer simply pauses its offset with no broker-side state.

### Log-based message brokers

Examples: Apache Kafka, Amazon Kinesis Streams, Apache Pulsar, Twitter DistributedLog

Core mechanism: An append-only log on disk, partitioned across machines. Each partition is a separate, independently readable log. Producers append; consumers read sequentially and record their offset.

Key characteristics:
- Messages are NOT deleted on delivery — reading is a read-only operation
- Consumer offset is maintained by the consumer (or a consumer group registry); the broker does not track per-message delivery
- Fan-out is trivial: multiple consumers read the same partition independently
- Partition assignment: the broker assigns entire partitions to consumer group members (coarse-grained load balancing)
- Sequential reads from disk are fast; total-order within a partition is guaranteed
- Log compaction: the broker retains only the most recent value per key, enabling reconstruction of full database state without unbounded storage

Storage model: Log is divided into segments. Old segments are deleted or moved to archive when a configurable retention period (time or size) is reached. This creates a large but bounded circular buffer. At 150 MB/s sequential write speed on a 6 TB disk, the buffer holds ~11 hours of data at maximum write rate — in practice, days to weeks.

---

## Comparison Table

| Dimension | Traditional Broker | Log-Based Broker |
|---|---|---|
| Message replay | Not possible (deleted on ack) | Yes — reset consumer offset |
| Fan-out to N consumers | Via topic subscriptions | Trivially — each consumer reads independently |
| Load balancing | Per-message (round-robin or work queue) | Per-partition (coarse-grained) |
| Max consumers per topic | Unlimited | Limited to partition count (one consumer per partition per group) |
| Head-of-line blocking | No — each consumer gets a different message | Yes — one slow message blocks its partition |
| Message ordering | Best-effort; redelivery can reorder | Total order within partition |
| Throughput behavior | Degrades as queue grows (disk spills) | Constant (always writes to disk) |
| Slow consumer effect | Memory pressure on broker | Consumer falls behind; does not affect others |
| Operational overhead | Must delete queues for stopped consumers | Consumers stop reading; offset remains |
| History / audit | No | Yes — up to retention period |
| Monitoring | Queue depth | Consumer lag (offset delta) |

---

## Decision Signals

**Choose log-based when any of the following are true:**
1. Multiple independent consumers need to read the same events
2. A consumer may need to replay events (debugging, bug fix reprocessing, bootstrapping a new derived system)
3. Message ordering within a key is important
4. High throughput with many small messages (log-based throughput is constant; traditional degrades under queue depth)
5. You want to replay historical events with a different processing version (Kappa architecture)
6. You are implementing CDC or event sourcing — immutability of the event log is a feature, not a side effect

**Choose traditional when all of the following are true:**
1. Each message is consumed by exactly one consumer (no fan-out)
2. Messages may be expensive to process and require per-message retry logic with arbitrary backoff
3. Message ordering does not matter
4. The team already operates a traditional broker and the system does not need replay

**Hybrid:** Most teams building serious data infrastructure end up with a log-based broker as the central spine and traditional queues for specific work queue patterns (job queues, email dispatch) where replay is not needed.

---

## Load Balancing vs. Fan-Out

Two consumer patterns (Figure 11-1 in source):

**Load balancing:** Each message is delivered to one consumer. Consumers share the work. In log-based brokers, implemented by assigning partitions to consumer group members. Maximum parallelism = partition count.

**Fan-out:** Each message is delivered to all consumers. Independent consumers each process every message. In log-based brokers, this is the default — each consumer group reads the full log independently.

**Combined:** Multiple consumer groups each receive all messages (fan-out between groups); within each group, partitions are divided for load balancing.

---

## Consumer Offsets and Fault Tolerance

In a log-based broker, each consumer or consumer group records its current offset per partition. On consumer restart, it resumes from the last committed offset.

If a consumer fails after processing messages but before committing its offset, those messages are processed again. This is at-least-once delivery by default. To achieve exactly-once, the consumer must make its downstream writes idempotent, or atomically commit the offset with the downstream write.

The consumer offset is analogous to the log sequence number (LSN) in database replication — the same principle that allows a replica to reconnect to a leader after a disconnect and resume replication without missing any writes.

---

## Disk Space and Retention

If the consumer falls so far behind that its offset points to a deleted segment, it will miss messages. The log-based broker effectively drops old messages when it fills. This is a large bounded buffer (days to weeks in practice), not unlimited storage.

Monitor consumer lag continuously. Alert when lag grows significantly. The large buffer gives the operations team time to intervene before messages are lost.
