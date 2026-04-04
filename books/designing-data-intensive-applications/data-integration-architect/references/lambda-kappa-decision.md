# Lambda vs. Kappa Architecture Decision Guide

## The Problem Both Architectures Solve

When batch processing is used to reprocess historical data (producing accurate, complete views) and stream processing is used to handle recent events (producing low-latency, approximate views), you need to decide how to combine them. Lambda and Kappa are the two main architectural patterns for this decision.

The underlying principle they share: **incoming data should be recorded as an immutable append-only log of events. Read-optimized views are derived from this log.** The difference is in how many systems derive those views.

## Lambda Architecture

### Structure

```
Incoming events
     │
     ├──► [Batch Layer]  ──────────────────────────────────────────────►  Batch views (accurate)
     │     Hadoop MapReduce / Spark                                              │
     │     Reprocesses all historical data                                       │
     │     Produces corrected, complete views                                    ▼
     │                                                               [Serving Layer]  ──► Query response
     └──► [Speed Layer]  ──────────────────────────────────────────►  Real-time views
          Apache Storm / Kafka Streams                                 (approximate)
          Processes recent events quickly
          Produces approximate, low-latency views
```

### Core Idea

- The batch layer is authoritative and simple: it reprocesses everything, so there is no state to manage, no fault tolerance to implement beyond restarting the job, and no incremental complexity.
- The speed layer is fast but imprecise: it handles the lag between the last batch run and now, accepting that its output may have small errors.
- Queries merge results from both layers at read time.

### When Lambda Makes Sense

- The batch processing logic is significantly simpler and less bug-prone than the equivalent stream processing logic.
- The team's stream processing infrastructure is less mature or reliable than their batch infrastructure.
- The workload uses approximate algorithms in the speed layer (e.g., HyperLogLog cardinality estimates, sketches) that are fast but slightly inaccurate, while the batch layer computes exact results.

### Practical Problems with Lambda

1. **Dual codebase burden.** The same business logic must be implemented in two different frameworks — the batch framework (Spark, MapReduce) and the streaming framework (Storm, Flink, Kafka Streams). These frameworks have very different APIs, semantics, and operational models. Any change to the logic requires updating both implementations.

   Libraries like Apache Beam or Summingbird attempt to abstract this by providing a single API that compiles to both batch and streaming backends, but debugging, tuning, and operational behavior still differ between the two runtimes.

2. **Merging batch and stream outputs is non-trivial.** Merging a simple aggregation (sum, count) over a tumbling window is straightforward. Merging session-based aggregations, joins, or stateful computations is much harder. The serving layer must implement query-time merge logic that mirrors the derivation logic — a third implementation of the same business logic.

3. **Batch layer ends up doing incremental processing.** Reprocessing all historical data from scratch on every batch run is expensive at scale. The batch layer is usually configured to process only recent data (e.g., the last hour), which means it faces the same windowing and late-data problems as the stream layer — negating its simplicity advantage.

4. **Two systems to operate.** Maintaining two independent distributed systems (a batch cluster and a streaming cluster) doubles infrastructure and operational complexity.

## Kappa Architecture

### Structure

```
Incoming events (immutable log, long retention)
     │
     └──► [Stream Processing Layer]  ──────────────────────────────────► Views
          Apache Flink / Apache Beam / Kafka Streams
          Processes both historical (replay) and recent events
          Produces accurate views via exactly-once semantics
```

### Core Idea

Unify batch and stream processing in a single system by treating batch jobs as a special case of stream processing: a job over a bounded (finite) stream. The stream processor reads from the beginning of the log for historical reprocessing, and from the current offset for ongoing processing. No separate batch layer is needed.

### Required Capabilities for Kappa

For Kappa to work correctly, three capabilities are needed:

1. **Log-based broker with configurable retention and replay.** The message broker must retain events long enough to replay all history needed for reprocessing. Kafka's configurable log retention (time-based or size-based) satisfies this. The stream processor reads from offset 0 to reprocess history, then continues from the current offset.

2. **Exactly-once semantics in the stream processor.** The output of a reprocessing run must be the same as if no faults had occurred. This requires: (a) exactly-once message delivery within the processor, (b) idempotent output writes, or (c) transactional output commits. Apache Flink's checkpointing with transactional sinks achieves this.

3. **Event-time windowing.** When reprocessing historical data, processing-time timestamps are meaningless (the job runs now, but the events are from the past). The stream processor must window on the event's original timestamp, not on when the processor handles it. Apache Beam and Flink both support event-time windowing with watermarks for handling late-arriving events.

### When Kappa Wins

- A mature stream processor with the three required capabilities (replay, exactly-once, event-time) is available and the team can operate it.
- Business logic is complex enough that maintaining two implementations is a significant burden.
- Schema evolution or business logic changes are frequent (each change requires reprocessing the log; with Kappa, this is one reprocessing job, not a coordinated update to two systems).

### When Lambda May Still Be Preferred

- The stream processor available to the team lacks replay capability or exactly-once semantics.
- The batch computation is a genuinely simpler algorithm than the equivalent streaming computation (e.g., sorting a bounded dataset vs. approximate sorting in a stream).
- The team has significantly more operational expertise in batch systems than streaming systems.

## The Convergence Trend

Modern processing engines are converging toward the Kappa model:

- **Apache Spark:** Originally batch-only (MapReduce replacement). Added Structured Streaming as a micro-batch stream processor. Spark can read Kafka topics as a stream or as a bounded dataset for batch — same API.
- **Apache Flink:** Originally a stream processor. Added DataSet API for batch processing. Flink 1.12+ unified both under a single streaming model: batch is a bounded stream.
- **Apache Beam:** Provides a single portable API for both batch and streaming. Backends include Flink, Dataflow, and Spark.

The practical consequence: if the team uses Flink or Beam, the Lambda vs. Kappa choice largely dissolves — the same code runs in both modes.

## Decision Matrix

| Criterion | Lambda | Kappa |
|-----------|--------|-------|
| Separate batch and stream codebases | Required | Not needed |
| Exactly-once stream semantics required | No (batch corrects errors) | Yes |
| Log replay capability required | No | Yes (long retention) |
| Query-time merge of batch + stream outputs | Required | Not needed |
| Appropriate when stream processor is immature | Yes | No |
| Appropriate when team has high streaming maturity | Less relevant | Yes |
| Schema evolution / logic change cost | High (update 2 codebases + reprocess) | Lower (one reprocessing job) |
| Operational complexity | High (2 clusters) | Medium (1 cluster) |

## Recommendation

**Default to Kappa** if the team can operate a stream processor with replay, exactly-once, and event-time capabilities (Flink, Beam on Dataflow, or Kafka Streams with Kafka log retention).

**Use Lambda** only if the stream processing capability is genuinely immature relative to the batch capability, or if the batch algorithms being used are fundamentally simpler than their streaming equivalents (which is increasingly rare).

**Use a unified batch/stream system** (Flink, Spark with Structured Streaming, Beam) to make the choice irrelevant.
