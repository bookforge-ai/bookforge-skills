# Trade-off Analysis: Message Broker for Real-Time Analytics Pipeline

## Decision

Which message broker should we use for ingesting and processing mobile app analytics events at ~50k events/sec peak load, running on AWS with a team of 4 engineers and startup-level budget?

## Options Considered

1. **Apache Kafka (via Amazon MSK or self-managed)** — Distributed commit log designed for high-throughput, durable event streaming with replay capability.
2. **RabbitMQ (self-managed on EC2 or Amazon MQ)** — Traditional message broker with flexible routing, mature protocol support (AMQP), and strong delivery guarantees per message.
3. **Amazon Kinesis Data Streams** — AWS-native managed streaming service with Kafka-like semantics but no infrastructure to manage. Included as a managed alternative given the team size and AWS context.

## Driving Quality Attributes

1. **Scalability / Throughput** — The system must reliably handle 50k events/sec at peak, with headroom for growth as the mobile app user base increases.
2. **Simplicity / Operability** — A team of 4 cannot spend significant time operating infrastructure. The broker must be manageable without a dedicated platform team.
3. **Cost** — Startup budget means total cost of ownership (infrastructure + engineering time + operational overhead) must stay low.

## Analysis of Advantages

### Kafka (MSK)

- **Throughput:** Kafka is purpose-built for high-throughput event streaming. 50k events/sec is well within its comfort zone; it handles millions of events/sec at organizations like LinkedIn and Uber. Append-only commit log with sequential disk I/O and batched writes are architecturally optimized for this workload.
- **Durability and replay:** Events are persisted to disk with configurable retention (days/weeks). Analytics pipelines benefit enormously from replay — if a downstream consumer (e.g., a new dashboard or ML model) is added later, it can reprocess the full event history without re-emitting from the mobile app.
- **Consumer scalability:** Kafka's partition-based consumer group model allows adding consumers independently. Multiple analytics systems (real-time dashboards, batch aggregation, alerting) can each consume the same stream without duplicating messages.
- **Ecosystem:** Native integration with Kafka Connect (for sinking to S3, Redshift, ClickHouse), Kafka Streams, and Flink. The analytics pipeline can grow without replacing the broker.
- **AWS managed option (MSK):** Amazon MSK removes most operational burden — provisioning, patching, broker replacement, and ZooKeeper management are handled by AWS. MSK Serverless further reduces operational overhead.

### RabbitMQ

- **Team familiarity:** The team already knows RabbitMQ. This is a genuine advantage — reduced ramp-up time, faster debugging, fewer operational surprises in the first months.
- **Flexible routing:** RabbitMQ's exchange/binding model allows sophisticated per-message routing (topic exchanges, headers-based routing, dead-letter queues). Useful if different event types need radically different processing paths.
- **Simpler mental model for task queues:** For traditional work distribution (process-and-acknowledge), RabbitMQ's model is more intuitive.
- **Lower entry cost:** A single RabbitMQ node or small cluster is cheaper to run than a Kafka cluster for low-to-moderate throughput.
- **Mature tooling:** The management UI, built-in monitoring, and extensive plugin ecosystem make day-to-day operations straightforward at moderate scale.

### Amazon Kinesis Data Streams

- **Fully managed:** Zero broker infrastructure to manage. No patching, no disk monitoring, no rebalancing.
- **AWS-native integration:** Direct integration with Lambda, Firehose (to S3/Redshift), and Kinesis Data Analytics. For an AWS-based analytics pipeline, this creates the shortest path to a working system.
- **On-demand capacity mode:** Automatically scales throughput without pre-provisioning, which matches startup unpredictability.
- **Event replay:** Like Kafka, supports replay via shard iterators with up to 365 days of retention.

## Analysis of Disadvantages (Hunting the Negatives)

### Kafka (MSK)

- **Operational complexity:** Even with MSK, Kafka has a steep learning curve. Partition management, consumer group rebalancing, offset management, and retention tuning require Kafka-specific expertise the team does not currently have. MSK reduces but does not eliminate this burden.
- **Cost at small scale:** MSK minimum cost is roughly $350-500/month for a 3-broker cluster (kafka.t3.small). For a startup, this is a meaningful fixed cost before you process a single event. MSK Serverless helps but has per-throughput pricing that can surprise.
- **Over-engineering risk:** 50k events/sec is achievable with simpler systems. Kafka is designed for orders-of-magnitude higher throughput. Adopting Kafka for "future scale" means paying the complexity tax now for scale you may not reach.
- **Consumer complexity:** Kafka consumers are more complex to write correctly than RabbitMQ consumers. Offset management, partition assignment, and exactly-once semantics require careful implementation.
- **Cold start for team:** The team knows RabbitMQ, not Kafka. Retraining 4 engineers on Kafka concepts (partitions, consumer groups, offsets, compaction) has a real cost in weeks of reduced velocity.

### RabbitMQ

- **Throughput ceiling:** RabbitMQ was not designed for sustained high-throughput streaming. At 50k events/sec, a RabbitMQ cluster will be under significant stress. Achieving this requires careful tuning: lazy queues, pre-fetch limits, multiple queues with sharding, and disabling publisher confirms. This is operating RabbitMQ at the edge of its design envelope.
- **No native replay:** RabbitMQ follows the traditional "consume and acknowledge" model. Once a message is consumed, it is gone. For an analytics pipeline, this means: no reprocessing historical data, no adding a new consumer that catches up, no replaying events after a bug fix. This is a fundamental architectural limitation, not a configuration issue.
- **Scaling requires re-architecture:** RabbitMQ scales vertically first (bigger nodes) and horizontally through federation or shovel plugins, which add significant complexity. Scaling from 50k to 200k events/sec would likely require a broker replacement rather than adding capacity.
- **Memory pressure:** RabbitMQ holds messages in memory by default. At 50k events/sec, even small message sizes create substantial memory pressure, leading to flow control (backpressure that blocks publishers) or disk paging that degrades throughput.
- **Amazon MQ limitations:** Amazon MQ for RabbitMQ has throughput limits and does not support all RabbitMQ features (e.g., no shovel plugin, limited clustering). Self-managing RabbitMQ on EC2 puts the full operational burden on the team.

### Amazon Kinesis Data Streams

- **Shard management (provisioned mode):** Each shard handles 1 MB/sec in or 1,000 records/sec. At 50k events/sec, you need ~50 shards minimum, which costs ~$750/month for shards alone plus data retention and GET costs. On-demand mode auto-scales but at a price premium.
- **Consumer limitations:** Each shard supports max 5 reads/sec across all consumers. With multiple downstream consumers (dashboard, batch, alerting), you hit this limit quickly and need enhanced fan-out ($$$).
- **Vendor lock-in:** Kinesis is AWS-proprietary. If you ever need to run locally, move to another cloud, or use open-source tooling, Kinesis provides no migration path. Kafka's open protocol has broad cross-platform support.
- **7-day default retention:** Extended retention (up to 365 days) costs extra. Kafka's disk-based retention is cheaper per GB.
- **Less ecosystem:** Fewer connectors, fewer community tools, and less community knowledge compared to Kafka.

## Trade-off Matrix

| Quality Attribute | Kafka (MSK) | RabbitMQ | Kinesis |
|-------------------|-------------|----------|---------|
| **Scalability / Throughput** | + Designed for millions/sec; 50k is comfortable. Partitions scale horizontally. | - 50k/sec pushes its design limits. Requires aggressive tuning. No clear path to 10x. | + Auto-scales in on-demand mode. Shard-based horizontal scaling. |
| **Simplicity / Operability** | - Steep learning curve. MSK helps but partition/offset management still complex. Team has no Kafka experience. | + Team already knows it. Simpler mental model for basic use. Management UI built in. | + Fully managed. Least operational burden of all three options. |
| **Cost** | = MSK ~$400-700/mo for a starter cluster. Reasonable but not cheap. Scales predictably. | + Cheapest to start. A 3-node EC2 cluster ~$150-300/mo. But hidden cost of tuning effort at 50k/sec. | - Most expensive at scale. 50 shards + enhanced fan-out + retention adds up fast. $800-1500+/mo easily. |
| **Event replay / Reprocessing** | + Native. Configurable retention. Multiple consumer groups replay independently. Core to the architecture. | - Not supported. Consumed messages are deleted. Fundamental design limitation for analytics. | + Supported via shard iterators. Up to 365 days retention (at cost). |
| **Ecosystem / Extensibility** | + Kafka Connect, Streams, Flink, ksqlDB. Massive open-source ecosystem for analytics. | = Plugins available but analytics ecosystem is limited. Not designed for stream processing. | = AWS-native integrations (Lambda, Firehose) are good. But locked to AWS ecosystem. |
| **Team velocity (short-term)** | - 2-4 weeks ramp-up for the team. Slower initial delivery. | + Immediate productivity. Team ships faster in month 1-2. | = Some AWS-specific learning but simpler than Kafka. Moderate ramp-up. |

## Synergies and Conflicts

**Kafka (MSK):**
- **Synergy:** Scalability reinforces extensibility — the same partition model that handles 50k/sec also enables adding new consumer groups (new analytics use cases) without impacting existing ones.
- **Synergy:** Event replay reinforces reliability — bugs in downstream processing can be fixed and events replayed, reducing data loss risk.
- **Conflict:** Scalability conflicts with simplicity — the partitioned log model that enables throughput is exactly what makes Kafka harder to operate and learn.
- **Conflict:** Long-term cost efficiency conflicts with short-term team velocity — investing in Kafka pays off at scale but costs engineering time upfront.

**RabbitMQ:**
- **Synergy:** Simplicity reinforces team velocity — the team's existing knowledge means faster debugging, faster feature delivery, and fewer operational incidents initially.
- **Conflict:** Simplicity conflicts with scalability — the same simple model that makes RabbitMQ easy to use is what limits its throughput ceiling. You cannot tune your way past an architectural ceiling.
- **Conflict:** Cost (low entry) conflicts with cost (long-term) — cheap to start, but if you hit scale limits and must migrate to Kafka later, the total cost (migration + downtime risk + re-engineering) far exceeds starting with Kafka.

**Kinesis:**
- **Synergy:** Operability reinforces team velocity — no infrastructure to manage means engineers spend time on analytics logic, not broker babysitting.
- **Conflict:** Cost conflicts with scalability — Kinesis's per-shard and per-GET pricing means costs grow faster than linearly with throughput. At startup budget, this is the riskiest cost profile.
- **Conflict:** Vendor lock-in conflicts with extensibility — if you outgrow Kinesis or need cross-cloud, migration is a full rewrite of the integration layer.

## Recommendation

**Apache Kafka via Amazon MSK Serverless** — the least worst choice for this context because:

1. **The throughput requirement is the non-negotiable constraint.** At 50k events/sec peak with expected growth, you need a broker that is comfortable at this scale, not struggling. RabbitMQ at 50k/sec is operating at its edge — one traffic spike above peak and you face backpressure, message loss, or cascading failures. Kafka treats 50k/sec as a light workload.

2. **Event replay is architecturally critical for analytics.** An analytics pipeline without replay capability is an analytics pipeline that loses data permanently when bugs occur. The team WILL ship a consumer bug in the first 3 months. With Kafka, they replay and recover. With RabbitMQ, the data is gone. This is not a feature — it is a safety net for the core business function.

3. **MSK Serverless mitigates the operability disadvantage.** MSK Serverless eliminates cluster sizing, partition rebalancing, and capacity planning. The team manages topics and consumer groups, not brokers. This narrows the Kafka vs RabbitMQ simplicity gap significantly.

4. **The team knowledge gap is a temporary cost; the architecture ceiling is permanent.** Learning Kafka takes 2-4 weeks. Migrating from RabbitMQ to Kafka after hitting scale limits takes 2-4 months and carries data loss risk. Pay the smaller cost now.

**Acknowledged downsides and why they are acceptable:**
- The team will be slower for the first month. This is acceptable because analytics pipelines are typically iterated on over weeks, not shipped in a single sprint. The ramp-up period overlaps with initial pipeline development.
- MSK Serverless costs more than self-managed RabbitMQ. The cost difference (~$200-400/mo) is small relative to the engineering time saved from not tuning RabbitMQ at its limits and not executing a future migration.
- Kafka's consumer model is more complex than RabbitMQ's. Mitigate by using a high-level consumer library (e.g., `confluent-kafka-python` or `aiokafka`) and establishing team conventions for offset management from day one.

**Why not Kinesis?** Despite being the simplest operationally, Kinesis is the most expensive at this throughput and creates hard vendor lock-in. For a startup that may need to optimize costs aggressively or pivot infrastructure, Kafka's open protocol provides more optionality.

## Risks of This Choice

- **Risk: Team ramp-up takes longer than expected.** Mitigation: Timebox Kafka learning to 2 weeks. Use MSK Serverless to reduce operational surface. Start with a single topic and consumer group before adding complexity. Assign one engineer as the "Kafka lead" to go deep and mentor the others.

- **Risk: MSK Serverless costs exceed budget.** Mitigation: Monitor MSK costs weekly in the first month. MSK Serverless charges per throughput — if costs spike, the team can switch to provisioned MSK with right-sized instances. Set a CloudWatch billing alarm at $500/mo.

- **Risk: Over-engineering the initial pipeline.** Mitigation: Start with 1 topic, 1 consumer group, and direct S3 sink via Kafka Connect. Resist the urge to use Kafka Streams, ksqlDB, or complex multi-topic topologies until the basic pipeline is stable.

- **Risk: Kafka concepts confuse the team and introduce bugs (e.g., offset mismanagement, rebalancing storms).** Mitigation: Use the `confluent-kafka-python` library which handles most offset management automatically. Write integration tests that verify consumer group behavior. Document the team's Kafka conventions in an ADR.

## Architecture Decision Record

- **Status:** Proposed
- **Context:** We are building a real-time analytics pipeline for mobile app events at ~50k events/sec peak. The team (4 engineers) has RabbitMQ experience but no Kafka experience. We are on AWS with startup-level budget. The pipeline needs to support multiple downstream consumers (real-time dashboards, batch aggregation, alerting) and must handle data reprocessing when consumer bugs occur. The mobile app user base is expected to grow, so throughput requirements will increase.
- **Decision:** Use Apache Kafka via Amazon MSK Serverless as the message broker for the analytics event pipeline. We choose Kafka over RabbitMQ because RabbitMQ's throughput ceiling and lack of event replay make it architecturally unsuitable for a high-volume analytics pipeline, even though the team is familiar with it. We choose MSK Serverless over self-managed Kafka to minimize operational burden for a small team. We choose Kafka over Kinesis to avoid vendor lock-in and higher costs at scale. We accept the 2-4 week team ramp-up cost because it is smaller than the cost of a future broker migration.
- **Consequences:**
  - **Positive:** Comfortable throughput headroom for 10x growth. Event replay enables data reprocessing and new consumer onboarding. Rich ecosystem (Kafka Connect, Streams) supports future analytics use cases without broker replacement. Open protocol avoids vendor lock-in.
  - **Negative:** Team velocity is reduced for the first 2-4 weeks during Kafka learning. MSK Serverless costs more than self-managed RabbitMQ (~$200-400/mo premium). Consumer code is more complex than equivalent RabbitMQ code. The team is adopting technology they have not operated in production before, increasing incident risk in the first quarter.
