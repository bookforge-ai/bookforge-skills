---
name: stream-processing-designer
description: |
  Design a stream processing system for unbounded, continuously arriving data. Use when choosing a message broker (Kafka vs RabbitMQ), implementing change data capture (CDC) from PostgreSQL, MySQL, or MongoDB via Debezium or Maxwell, selecting window types for aggregation (tumbling, hopping, sliding, session), joining event streams or enriching events from a table, or configuring exactly-once fault tolerance. Trigger phrases: "should I use Kafka or RabbitMQ?", "how do I sync my database to Elasticsearch in real time?", "how do I implement CDC for Postgres?", "how do I get exactly-once semantics in Flink or Kafka Streams?", "should I use Lambda or Kappa architecture?", "how do I keep derived data systems in sync without dual writes?", "how do I join two event streams?". Covers log-based vs. traditional broker selection, four window types, three join types (stream-stream, stream-table, table-table), CDC bootstrap strategy, and microbatching vs. checkpointing trade-offs. Does not apply to bounded offline datasets (see batch-pipeline-designer) or multi-store integration architecture (see data-integration-architect).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/stream-processing-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: [encoding-format-advisor]
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [11]
tags: [stream-processing, kafka, message-broker, log-based-broker, change-data-capture, cdc, event-sourcing, windowing, tumbling-window, hopping-window, sliding-window, session-window, stream-join, stream-table-join, fault-tolerance, microbatching, checkpointing, idempotent, exactly-once, lambda-architecture, kappa-architecture, debezium, maxwell, flink, spark-streaming, kafka-streams, event-time, processing-time]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Event stream description, system architecture document (architecture.md), docker-compose.yml showing current infrastructure, or requirements document describing latency/throughput targets"
    - type: code
      description: "Application source files showing current data access patterns, existing pipeline code, or schema definitions for events"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with pasted system descriptions, architecture.md, docker-compose.yml, or codebase analysis. Codebase helps identify existing databases and their types."
discovery:
  goal: "Produce a concrete stream processing architecture recommendation: broker type, CDC tool (if applicable), window type(s), join type(s), fault tolerance strategy — with trade-offs documented"
  tasks:
    - "Classify the event source (user activity, database changes, sensors, application events) to determine entry point"
    - "Select broker type (log-based vs. traditional) based on replay, ordering, and throughput requirements"
    - "If syncing from a database, select CDC tool per database type and design the bootstrap strategy"
    - "Select window type(s) for aggregation requirements using the four-type framework"
    - "Select join type(s) for enrichment/correlation requirements using the three-type framework"
    - "Choose fault tolerance strategy based on latency requirements and output side-effect profile"
    - "Apply the end-to-end exactly-once argument to the full pipeline, not just the stream processor"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "tech-lead", "site-reliability-engineer"]
    experience: "intermediate-to-advanced — assumes familiarity with databases, message queues, and building data pipelines"
  triggers:
    - "Team is building a real-time data pipeline and needs to choose between message broker options"
    - "Application writes to a primary database and needs derived systems (search index, cache, data warehouse) kept in sync without dual writes"
    - "Engineer needs to add windowed aggregations (hourly counts, rolling averages) to a stream processor"
    - "Pipeline needs to join a stream of events with a reference dataset that changes over time"
    - "Team is experiencing inconsistency between the primary database and a derived data store"
    - "System needs to tolerate stream processor failures without reprocessing all historical data from the start"
    - "Team is debating Lambda vs. Kappa architecture for a new data platform"
    - "Application needs event sourcing and the team must design the event store and projection strategy"
  not_for:
    - "Batch pipeline design for bounded datasets — use batch-pipeline-designer"
    - "Choosing the data model for event storage (relational vs. document) — use data-model-selector first"
    - "Encoding format for events on the wire — use encoding-format-advisor"
    - "Replication strategy for the source database itself — use replication-strategy-selector"
---

# Stream Processing Designer

## When to Use

You are building or evaluating a system that processes data continuously as it arrives — not in periodic batch runs — and need to make concrete decisions about message transport, windowed aggregation, stream joins, and fault tolerance.

This skill applies when:
- You need to keep derived data systems (search index, cache, data warehouse, analytics) in sync with a primary database in near-real time
- You are processing a stream of events with time-based aggregations (counts per minute, rolling averages, session analytics)
- You need to join two or more event streams, or enrich a stream with data from a reference table
- You are choosing between Kafka and a traditional message broker (RabbitMQ, ActiveMQ, Amazon SQS)
- You need to implement change data capture for PostgreSQL, MySQL, MongoDB, or Oracle
- You are designing event sourcing and need to understand how it differs from CDC
- You need to reason about exactly-once semantics end-to-end, not just within the stream processor

**This skill produces architecture decisions, not code.** For encoding format selection (Avro vs. Protobuf for event schemas), use `encoding-format-advisor` first. For batch pipeline design, use `batch-pipeline-designer`. For overall data integration across multiple systems, use `data-integration-architect`.

---

## Context and Input Gathering

Before applying the frameworks, collect:

### Required
- **Event source type:** Where do events come from? User actions (clicks, purchases), database writes, sensor readings, or application state changes?
- **Processing requirements:** What transformation is needed? Filtering, aggregation, enrichment (joining with reference data), pattern detection, or materialized view maintenance?
- **Latency requirements:** How stale can the output be? Sub-second, seconds, minutes, or hours?
- **Exactly-once requirement:** Does incorrect duplicate processing cause visible harm (double-charging a customer, double-counting inventory)? Or is it tolerable (approximate metrics)?

### Important
- **Consumer count and patterns:** How many downstream consumers read the same stream? Do they need to read independently, at their own pace, or replay past data?
- **Message ordering requirements:** Must messages be processed in the order they were produced? Per-key ordering, or global ordering?
- **Output side effects:** Does processing write to external systems (databases, email services, payment APIs)? This determines whether framework-level exactly-once is sufficient.
- **Existing infrastructure:** What databases, brokers, and stream processors already exist in the environment?

### Useful but Optional
- **Event volume:** Events per second at peak — this affects partitioning and consumer parallelism decisions
- **Message size distribution:** Mostly small events, or large payloads? Affects broker memory configuration
- **Retention requirement:** How long must past events be replayable? Affects log-based broker configuration

---

## Process

### Step 1 — Select Broker Type

**WHY:** The choice between a log-based and traditional message broker determines whether consumers can replay events, whether multiple consumers can read independently, and what happens when a consumer falls behind. Getting this wrong forces an expensive migration later.

Use the broker selection framework in `references/broker-selection-framework.md`. Key decision signals:

**Choose a log-based broker (Kafka, Amazon Kinesis, Apache Pulsar) when:**
- Multiple independent consumers need to read the same events (fan-out without coupling)
- Consumers may need to replay past events — for debugging, reprocessing after a bug fix, or bootstrapping a new derived data system
- Message ordering within a partition is important (log-based brokers give total order within a partition)
- High throughput with many small messages (log-based brokers write every message to disk regardless; throughput is constant and predictable)
- The stream processor may restart and needs to resume from where it left off (consumer offsets)

**Choose a traditional broker (RabbitMQ, ActiveMQ, Amazon SQS, Azure Service Bus) when:**
- Each message should be processed by exactly one consumer, and load balancing across consumers is the primary concern
- Messages are expensive to process individually and need fine-grained per-message acknowledgment with arbitrary redelivery
- Message ordering is not critical and you want per-message parallelism (traditional brokers assign individual messages to consumers; log-based brokers assign whole partitions)
- The team already operates one and the system does not need replay or fan-out

**Critical difference in replay behavior:** In a log-based broker, consuming a message is a read-only operation — the consumer's offset advances, but the log is unchanged. You can reprocess by resetting the offset. In a traditional broker, acknowledgment deletes the message — reprocessing is impossible unless you saved it elsewhere.

### Step 2 — Design the Event Source (CDC or Direct Production)

**WHY:** Two patterns exist for getting events into the stream: direct event production (application code writes to the broker) and change data capture (CDC, where the database's replication log is tapped). Each has different consistency guarantees, and the wrong choice causes the dual-write race condition — a form of data loss where two systems permanently diverge.

**Avoid dual writes:** Writing to both the database and the broker in application code creates a race condition. Two concurrent writers can reach the database and broker in opposite orders, leaving the systems permanently inconsistent — with no error and no detection. See the race condition in the "Keeping Systems in Sync" section of the source chapter (page 452).

**When to use CDC:**
- The application already uses a mutable relational database (PostgreSQL, MySQL, Oracle) as the system of record
- You need to sync derived systems (search index, cache, data warehouse) from the database
- You cannot change the application code to produce events directly
- You need strong ordering guarantees (CDC preserves the database's write order)

**Per-database CDC tool mapping:**

| Database | Tool | Mechanism | Notes |
|---|---|---|---|
| PostgreSQL | Debezium, Bottled Water | WAL (write-ahead log) parsing | Debezium uses logical replication slots; Bottled Water uses a dedicated API |
| MySQL | Debezium, Maxwell | binlog parsing | Both parse the MySQL binary log; Maxwell is simpler, Debezium has broader ecosystem |
| MongoDB | Debezium, Mongoriver | oplog tailing | MongoDB oplog is a capped collection; must be large enough to survive processing delays |
| Oracle | GoldenGate | LogMiner / proprietary | Requires Oracle licensing; GoldenGate is the standard production choice |
| Any | Kafka Connect | Plugin-based | Kafka Connect wraps CDC tools; use when events need to land in Kafka topics |

**CDC bootstrap strategy (initial snapshot):**
A CDC pipeline that taps the replication log only captures changes from the time it starts. For rebuilding a derived system from scratch, you need the full historical state.

1. Take a consistent snapshot of the database (e.g., `pg_dump` with a known log sequence number, or a tool-integrated snapshot)
2. Record the log offset at snapshot time
3. Load the snapshot into the derived system
4. Start the CDC consumer from that recorded offset — this ensures no changes are missed between snapshot and live CDC

Some CDC tools (Debezium) handle this bootstrap automatically. For others, it is a manual operation. Confirm before assuming automation.

**Log compaction as an alternative to periodic snapshots:** If using a log-based broker with log compaction enabled, the compacted topic always contains the most recent value for every key. A new derived system can bootstrap by reading the compacted topic from offset 0, then switch to live CDC without taking a database snapshot.

**When to use event sourcing instead of CDC:**
- The application is being designed from scratch and domain events are first-class
- Business events ("order cancelled", "seat reserved") are more meaningful than database row changes
- You need the full event history for audit, compliance, or behavioral analytics — not just the current state
- CDC applies at the infrastructure level (database internals). Event sourcing applies at the application level (explicit business facts)

**Key difference:** In CDC, the application writes to a mutable database and the log is extracted afterward. In event sourcing, the application writes immutable events to an event log first, and current state is derived from the log. The event log is the system of record.

**Commands vs. events in event sourcing:** A command is a request that may fail (validation, constraint checks). When accepted, it becomes an immutable event. Validate commands synchronously before committing them as events — once an event is written to the log, downstream consumers cannot reject it.

### Step 3 — Select Window Type(s)

**WHY:** Windows bound an otherwise infinite stream so aggregations are computable. The wrong window type either produces results that don't match business intent (tumbling where smoothing is needed), consumes excessive memory (sliding on high-volume streams), or fails to capture session behavior (any fixed window for user activity).

Use the window type reference in `references/window-type-selection.md`. Decision framework:

**Tumbling window** — Fixed-length, non-overlapping. Every event belongs to exactly one window.
- Use when: Producing periodic reports (hourly totals, daily counts, per-minute error rates)
- Implement: Round event timestamp down to nearest window boundary
- Example: Count requests per minute → 1-minute tumbling window on event timestamps

**Hopping window** — Fixed-length with overlap (hop size < window size). Events appear in multiple windows.
- Use when: Producing smoothed metrics where abrupt transitions between windows are undesirable
- Implement: Compute tumbling windows at the hop size, then aggregate over multiple adjacent tumbling windows
- Example: 5-minute rolling average updated every 1 minute → 5-minute window, 1-minute hop

**Sliding window** — Variable-length. Groups all events within a fixed time interval of each other.
- Use when: Detecting events that co-occur within a time proximity (two events within 5 minutes of each other), regardless of fixed boundaries
- Implement: Buffer sorted by timestamp, evict events that expire from the window
- Example: Detect rapid successive login failures within 10 minutes for fraud detection

**Session window** — No fixed duration. Groups events from the same user/entity with gaps smaller than a timeout.
- Use when: Measuring user engagement, session duration, or any activity that has natural periods of inactivity
- Implement: Merge events into the same session if less than the gap threshold apart; close session on timeout
- Example: Website session analytics — group clicks within 30-minute inactivity window per user

**Event time vs. processing time:** Always use event timestamps (event time) for window boundaries when event correctness matters. Processing time (the wall clock of the stream processor) produces artifacts when the processor restarts — a backlog of old events appears as a sudden spike when consumed, producing false anomalies. Use processing time only when event delay is negligibly small and approximate results are acceptable.

**Straggler events:** When using event-time windows, events can arrive after the window has closed (delayed by network, buffering, or offline clients). Two options:
1. Ignore stragglers and track them as a metric — acceptable when straggler rate is low
2. Publish a corrected result when stragglers arrive — required for billing, compliance, or any system where downstream users act on window results

### Step 4 — Select Join Type(s)

**WHY:** Stream joins require the processor to maintain state — buffered events or a local copy of a table — to match events from different inputs. Each join type has different state requirements, ordering sensitivity, and time-dependence. Choosing the wrong type produces nondeterministic results or excessive memory consumption.

See `references/join-type-reference.md` for detailed implementation patterns.

**Stream-stream join (window join):**
- What: Correlate two event streams where related events occur close in time, joined by a shared key
- State: Buffer of recent events from both streams within the window, indexed by join key
- Use when: Correlating user actions across sessions (search query + subsequent click), matching request with response events, detecting cause-effect patterns within a time window
- Example: Join search events with click events by session ID within 1 hour to compute click-through rate
- Time-dependence: Results are nondeterministic if ordering across streams is undetermined. If the same job is rerun, events may interleave differently.

**Stream-table join (stream enrichment):**
- What: Enrich each event from a stream with data from a reference table that changes over time
- State: Local copy of the entire reference table (or relevant partition), updated via a CDC stream from the source database
- Use when: Adding user profile data to activity events, looking up product metadata for order events, applying country-specific configuration to events
- Example: Enrich user activity stream with user profile (name, tier, preferences) from user database
- Key difference from batch: The reference table is not a static snapshot — it is updated via a separate CDC stream. The stream processor joins against the version of the table that exists at the time each event arrives.
- Time-dependence: The result depends on when the profile update arrives relative to activity events. Use slowly changing dimension (SCD) versioning if historical correctness is required.

**Table-table join (materialized view maintenance):**
- What: Maintain a continuously updated materialized view of the join between two tables, both represented as changelog streams
- State: Both tables maintained in local storage; recompute the join when either changes
- Use when: Maintaining a denormalized read model (like a user timeline cache) that combines data from multiple source tables
- Example: Maintain a per-user timeline by joining tweet events with follow-relationship events (equivalent to continuously refreshing `SELECT follows.follower_id, array_agg(tweets.*) FROM tweets JOIN follows ON follows.followee_id = tweets.sender_id GROUP BY follows.follower_id`)
- This pattern is how Twitter's home timeline cache works: each new tweet fans out to all followers' cached timelines

**Selecting the right join type:**

| Situation | Join Type |
|---|---|
| Two event streams, correlate events within a time window | Stream-stream |
| One event stream + one reference dataset | Stream-table |
| Maintaining a combined read model from two source tables | Table-table |
| Enriching events with slowly changing data | Stream-table with SCD versioning |

### Step 5 — Choose Fault Tolerance Strategy

**WHY:** A stream processor runs indefinitely. Unlike a batch job that can be fully restarted from its immutable input, restarting a stream job from scratch means reprocessing potentially years of events. The fault tolerance strategy determines how much reprocessing happens after a failure and whether outputs are produced multiple times.

See `references/fault-tolerance-comparison.md` for a full comparison.

**Microbatching (Spark Streaming, Spark Structured Streaming):**
- Mechanism: Break the stream into small fixed-size blocks (typically ~1 second). Treat each block as a miniature batch job. Failed blocks are retried; successful blocks are committed.
- Exactly-once guarantee: Within the framework — each input record contributes to exactly one output record in steady state
- Implicit window: Microbatching implicitly creates a tumbling window at the batch size. Larger windows require explicit state carry-over between microbatches.
- Latency floor: Cannot be lower than the batch interval (~1 second minimum)
- Choose when: Latency of 1-5 seconds is acceptable; team is familiar with batch processing semantics; existing Spark infrastructure

**Checkpointing (Apache Flink, Apache Samza):**
- Mechanism: Periodically snapshot all operator state and write it to durable storage. On failure, restart from the last checkpoint and discard any output produced between the checkpoint and the crash.
- Exactly-once guarantee: Within the framework, using barrier-based checkpointing (Flink) or changelog-based recovery (Samza)
- No implicit window: Window size is independent of checkpoint interval
- Latency floor: Sub-second (checkpoints happen asynchronously; normal processing is not interrupted)
- Choose when: Sub-second latency is required; large operator state (joins, aggregations) needs efficient recovery; you need large windows without per-window state carry-over overhead

**Idempotent processing:**
- Mechanism: Design every output operation to be safe to apply multiple times. On failure, replay input messages from the broker offset and re-apply. If an output was already applied, re-applying has no effect.
- Examples: Writing to a key-value store where the write sets a fixed value (not an increment), including the message offset in the write to detect duplicates, using database upserts keyed by event ID
- Exactly-once guarantee: Achieved without distributed transactions if all output operations are idempotent and the broker supports offset replay (log-based brokers)
- Constraints: The processing must be deterministic. Replay must produce the same messages in the same order (log-based brokers guarantee this within a partition). No other concurrent writer may update the same keys.
- Choose when: Output goes to a key-value store or a database with natural upsert semantics; you want exactly-once without the overhead of distributed transactions

**The end-to-end exactly-once argument:**
Framework-level exactly-once (microbatching or checkpointing) only governs what happens inside the stream processor. As soon as output leaves the processor — a write to an external database, an email sent, a message published to another broker — the framework cannot discard that output on failure. If the processor restarts, the side effect happens again.

True end-to-end exactly-once requires that all output side effects are either:
1. **Idempotent** — safe to apply twice with the same result, or
2. **Atomically committed** — tied to advancing the consumer offset in a single atomic operation (available in some frameworks, e.g., Google Cloud Dataflow's atomic commit facility, Kafka transactions)

Practically: if you send emails or charge payments from a stream processor, microbatching and checkpointing alone are not sufficient. Design the output operation to be idempotent (e.g., deduplicate email sends by event ID), or use atomic commits if available.

### Step 6 — Evaluate Lambda vs. Kappa Architecture

**WHY:** Lambda architecture (separate batch and speed layers with a merge layer) was designed to get the correctness of batch processing with the low latency of stream processing. Kappa architecture challenges whether this complexity is necessary.

**Lambda architecture:**
- Batch layer: Reprocesses all historical data periodically; produces correct, complete output
- Speed layer: Processes recent data in real time; produces approximate or recent-only output
- Serving layer: Merges batch and speed outputs for queries
- Problem: Two separate code paths for the same computation. Business logic must be kept in sync across both. When the batch layer produces new results, it must replace the speed layer output atomically.

**Kappa architecture:**
- Single stream processing layer handles both historical reprocessing and live data
- Reprocessing is done by replaying the event log from offset 0 with a new version of the code, writing output to a new location, then switching consumers to the new output
- Requires: A log-based broker that retains the full event history (or long enough history)
- Advantage: One code path, no synchronization between batch and speed layers
- Limitation: Reprocessing large history is slower than batch processing on a distributed file system. For very large historical datasets, Kappa may not complete reprocessing quickly enough.

**Choose Lambda when:** You have very large historical datasets (petabytes) where stream reprocessing is too slow; you need the batch layer's correctness guarantees independently; the team already operates separate batch and stream infrastructure.

**Choose Kappa when:** Your log-based broker retains sufficient history; reprocessing speed is acceptable; you want operational simplicity; the stream processing framework can handle both historical and live data at acceptable throughput.

---

## Examples

### Example 1 — Real-Time Search Index Sync

**Scenario:** An e-commerce application uses PostgreSQL as its primary database. Product search is powered by Elasticsearch. Currently, the application writes to both PostgreSQL and Elasticsearch directly (dual write). The search index is frequently stale or inconsistent with the database.

**Trigger:** "How do I keep Elasticsearch in sync with PostgreSQL without dual writes?"

**Process:**
1. **Broker:** Log-based (Kafka). Multiple consumers needed: Elasticsearch sink, analytics warehouse, audit log. Replay is needed when Elasticsearch is rebuilt.
2. **Event source:** CDC with Debezium on PostgreSQL WAL. Debezium captures the database's write order, eliminating the race condition in dual writes. The database is the only writer; Debezium observes.
3. **Bootstrap:** Use Debezium's snapshot mode (automatically takes a consistent snapshot + records the WAL offset). Elasticsearch is populated from the snapshot, then Debezium switches to live CDC from that offset.
4. **Window/join:** Not applicable — this is a materialized view maintenance pipeline. No aggregation windows. The Kafka Connect Elasticsearch sink connector writes each change event as a document update.
5. **Fault tolerance:** Idempotent writes to Elasticsearch (document ID = primary key). If Debezium restarts and replays a change, Elasticsearch simply overwrites the same document to the same value.

**Output:** PostgreSQL → Debezium → Kafka topic (log-compacted) → Elasticsearch Sink Connector → Elasticsearch. No dual writes. Consistent ordering. Replay-safe.

### Example 2 — Fraud Detection with Session Windows

**Scenario:** A payments platform needs to detect when a user makes more than 5 failed payment attempts within 30 minutes (a pattern suggesting card testing fraud). Events arrive from multiple microservices with occasional delays of up to 2 minutes.

**Trigger:** "How do I detect rapid failed payment attempts in a stream processor?"

**Process:**
1. **Broker:** Kafka (log-based). Replay needed for reprocessing after rule changes; multiple consumers (fraud engine, analytics, compliance).
2. **Event source:** Application publishes `payment.attempt` events directly to Kafka when processing payments. Event sourcing pattern: the event is the record of what happened.
3. **Window type:** Session window with 30-minute inactivity timeout, keyed by user ID. A session closes if no payment attempt arrives for 30 minutes. Counts failed attempts within each session.
4. **Event time:** Use event timestamp (when the payment was attempted), not processing time. The processor may restart and consume a backlog; processing-time windows would produce false spikes.
5. **Fault tolerance:** Checkpointing (Flink). Session state must survive restarts. Checkpointing writes session state to durable storage; on restart, sessions resume from the last checkpoint without losing partial counts.
6. **Exactly-once:** Fraud alerts go to a downstream Kafka topic (not email). The alert sink is idempotent (alert ID = session ID + window start). On reprocessing, duplicate alerts are deduplicated by the downstream alert router.

**Output:** Flink job with session window (30-minute gap) on `payment.attempt` stream → emits `fraud.alert` event when session count exceeds threshold → downstream alert router deduplicates and notifies.

### Example 3 — Activity Stream Enrichment (Stream-Table Join)

**Scenario:** A SaaS analytics platform processes a high-volume stream of user activity events (page views, feature usage). Each event contains a user ID but not user metadata (subscription tier, company, region). Analytics queries always segment by these dimensions. Currently, a nightly batch job denormalizes the data into a data warehouse. The 24-hour delay makes same-day analytics impossible.

**Trigger:** "How do I enrich activity events with user profile data in real time?"

**Process:**
1. **Broker:** Kafka. Fan-out to multiple analytics consumers; replay needed when enrichment logic changes.
2. **Event source:** Application produces activity events directly. User profile changes are captured via CDC (Debezium on the user PostgreSQL database) into a separate Kafka topic.
3. **Join type:** Stream-table join. Activity event stream joined with the user profile changelog stream. The stream processor loads the user profile table into local state (in-memory hash map or local RocksDB index), updated continuously via CDC events.
4. **Time-dependence:** A user that upgrades their subscription tier will have subsequent activity events enriched with the new tier. Activity events before the upgrade retain the old tier. This is correct — it reflects the tier at the time of activity. Document this behavior explicitly for downstream users.
5. **Fault tolerance:** Checkpointing. The local user profile state (potentially millions of records) must survive restarts without reloading from the source database each time.
6. **Output:** Enriched events written to a new Kafka topic, consumed by the data warehouse (Snowflake, BigQuery) and a real-time dashboard.

**Output:** Activity stream + User profile CDC stream → stream-table join in Flink → enriched event stream → warehouse and dashboard consumers. Latency reduced from 24 hours to seconds.

---

## References

- `references/broker-selection-framework.md` — Detailed comparison of log-based vs. traditional brokers with scoring criteria
- `references/window-type-selection.md` — Window type decision table, implementation notes, and straggler handling patterns
- `references/join-type-reference.md` — Join type patterns, state management requirements, and time-dependence analysis
- `references/fault-tolerance-comparison.md` — Microbatching vs. checkpointing vs. idempotent writes comparison, with exactly-once end-to-end argument

**Related skills:**
- `encoding-format-advisor` — Choose encoding format (Avro, Protobuf) for events on the broker (dependency)
- `batch-pipeline-designer` — For bounded dataset processing; compare Lambda vs. Kappa decisions
- `data-integration-architect` — Cross-system integration decisions when stream processing is one component of a larger data architecture

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-encoding-format-advisor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
