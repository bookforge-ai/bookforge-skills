# Fault Tolerance Comparison

Reference for Step 5 of `stream-processing-designer`.

---

## The Core Problem

Batch jobs tolerate failures by restarting failed tasks from their immutable input. The output of failed tasks is discarded. Because input is immutable and output is only made visible when a task completes successfully, the result is the same as if no failure occurred — exactly-once semantics without any special mechanism.

Stream jobs cannot use this approach because the stream never ends. You cannot "wait until the job finishes" to make output visible — the job runs indefinitely. And restarting from the beginning of the stream means reprocessing potentially years of events.

Three strategies handle this problem, each with different trade-offs.

---

## Strategy 1: Microbatching

**Mechanism:** Break the stream into small fixed-size blocks, typically ~1 second. Treat each block as a miniature batch job. Process the block, produce output, commit the output, advance the offset. Failed blocks are retried from the start of the block.

**Used by:** Apache Spark Streaming, Spark Structured Streaming

**Latency floor:** The batch interval. Cannot produce output more frequently than once per batch. Minimum practical batch interval: ~500ms–1s.

**Implicit window:** Microbatching implicitly creates a tumbling window at the batch size, windowed by processing time (not event time). Jobs that require windows larger than the batch interval must explicitly carry state forward across microbatches.

**Exactly-once guarantee:** Within the framework — each input record contributes to exactly one output batch in steady state. On failure, the failed microbatch is retried; the previous microbatch's output was already committed.

**State management:** State that spans microbatch boundaries (e.g., session state, running totals) must be explicitly persisted between batches. Spark handles this via stateful transformations (e.g., `updateStateByKey`, `mapGroupsWithState`).

**Overhead:** Each microbatch incurs scheduling and coordination overhead. Smaller batches (lower latency) = higher overhead. Performance tuning requires balancing batch size against acceptable latency.

**Choose microbatching when:**
- Latency of 1-5 seconds is acceptable
- Team is familiar with batch processing (Spark) semantics
- Existing Spark infrastructure is already operated
- Workload consists of high-throughput, low-state operations (filtering, simple aggregations)

---

## Strategy 2: Checkpointing

**Mechanism:** Periodically snapshot all operator state (window buffers, join state, aggregation accumulators) and write snapshots to durable storage (HDFS, S3, GCS). On failure, restart from the most recent checkpoint and discard any output generated between the checkpoint and the crash.

**Used by:** Apache Flink (barrier-based checkpointing), Apache Samza (changelog-based state recovery)

**Latency floor:** Sub-second. Checkpointing is asynchronous — normal processing continues while snapshots are written. The latency floor is the processing time per event, typically milliseconds.

**No implicit window:** Window size is entirely independent of checkpoint interval. A 1-hour window with 30-second checkpoints is entirely valid.

**Exactly-once guarantee:** Within the framework. Flink uses checkpoint barriers: special markers injected into the event stream. When all operators have processed events up to the barrier, state is snapshotted. On recovery, all operators restore from the snapshot and replay only the events after the last barrier.

**State management:** Flink manages operator state automatically. Large state (e.g., a local copy of a reference table for stream-table joins) is stored in RocksDB on local disk and checkpointed to durable storage. Recovery reads from the checkpoint rather than reloading from the source database.

**Checkpoint interval trade-off:** More frequent checkpoints = less reprocessing after failure, but more I/O overhead. Typical production checkpoints: every 30 seconds to 5 minutes.

**Choose checkpointing when:**
- Sub-second latency is required
- Large operator state must survive restarts efficiently (stream-table joins with large reference tables, session windows across millions of users)
- Large windows are needed (hours or days) without per-window carry-over overhead
- The team operates or is willing to operate Flink or Samza

---

## Strategy 3: Idempotent Processing

**Mechanism:** Design every output operation so that applying it multiple times produces the same result as applying it once. On failure, replay input messages from the broker offset and reapply. If the output was already applied, the duplicate application has no effect.

**Not a framework feature:** Idempotence is a property of the output operation, not of the stream processor. It can be used with any stream processor (or even without one).

**Exactly-once guarantee:** Achievable without distributed transactions, provided:
1. All output operations are idempotent
2. The broker supports offset replay (log-based broker — the consumer can reset its offset)
3. Processing is deterministic (replaying the same input produces the same output)
4. No other concurrent process writes to the same output keys

**Examples of naturally idempotent operations:**
- Setting a key in a key-value store to a fixed value: `SET user:42:tier premium` — applying twice sets it to the same value
- Upserting a database row by primary key: if the row already exists with the same value, no change
- Writing a file at a fixed path with fixed content: idempotent if the content is deterministic

**Examples of non-idempotent operations that can be made idempotent:**
- Incrementing a counter: non-idempotent. Make idempotent by writing the absolute value instead, or by deduplicating by message offset before incrementing.
- Sending an email: non-idempotent. Make idempotent by maintaining a "sent" set keyed by event ID. Check before sending.
- Publishing a message to another broker: non-idempotent. Make idempotent by including a unique event ID in the message and deduplicating at the consumer.

**Technique — offset in the write:**
When writing to an external database from a Kafka consumer, include the Kafka partition + offset in the write. Before writing, check if that offset has already been applied. If yes, skip. This makes the write idempotent even for counter increments.

```python
# Non-idempotent:
db.execute("UPDATE counters SET count = count + 1 WHERE key = ?", key)

# Made idempotent with offset tracking:
db.execute("""
  INSERT INTO processed_offsets (partition, offset) VALUES (?, ?)
  ON CONFLICT DO NOTHING
""", partition, offset)
if db.rowcount > 0:  # Not a duplicate
    db.execute("UPDATE counters SET count = count + 1 WHERE key = ?", key)
```

**Fencing:** When failing over from one consumer node to another, the old node may not know it has been replaced. If it sends a stale write after the new node has already written a newer value, it could overwrite the newer value with an older one. Use fencing tokens (monotonically increasing version numbers) to reject stale writes.

**Choose idempotent processing when:**
- Output goes to a system with natural upsert or set semantics (key-value store, document database with upsert)
- You want exactly-once without the overhead of distributed transactions or complex framework configuration
- The stream processor is simple (stateless filter + enrich, no large aggregation state)
- You can enforce determinism and sequential ordering via a log-based broker

---

## Comparison Table

| Dimension | Microbatching | Checkpointing | Idempotent Processing |
|---|---|---|---|
| Minimum latency | ~1 second | Sub-second | Depends on output system |
| Framework | Spark Streaming | Flink, Samza | Any |
| State recovery | Reprocess failed batch | Restore from checkpoint snapshot | Replay + reapply (no state to restore) |
| Large state efficiency | Poor (must carry state across batches) | Good (RocksDB + checkpoint) | Good (no framework state) |
| Window independence | No (implicit window = batch interval) | Yes | Yes |
| Exactly-once scope | Within framework | Within framework | End-to-end if all outputs are idempotent |
| Setup complexity | Low (batch semantics) | Medium | Medium (design each output for idempotence) |

---

## The End-to-End Exactly-Once Argument

This is the most important point in this reference and the most commonly misunderstood.

**Framework-level exactly-once is not end-to-end exactly-once.**

Microbatching and checkpointing guarantee that each input record contributes to exactly one output within the stream processing framework. But as soon as output leaves the framework — a write to an external database, a message published to another broker, an email sent, a payment charged — the framework cannot discard that side effect on failure.

Scenario:
1. Stream processor processes a batch/checkpoint period
2. The batch produces an email notification and writes to an external database
3. The processor crashes after sending the email but before committing the offset
4. On restart, the processor reprocesses the same events
5. The email is sent again, and the database write is applied again

The framework reports "exactly-once" — each input record was counted once in the framework's accounting. But the external world saw two emails and two database writes.

**True end-to-end exactly-once requires that all output side effects are either:**

1. **Idempotent** — applying twice produces the same result (safe to reprocess)

2. **Atomically committed** with the consumer offset — all side effects of a batch are committed in a single atomic transaction that also advances the consumer offset. If the transaction fails, neither the side effects nor the offset advance. On retry, the same events are reprocessed and the same (idempotent) side effects are applied.

Atomic commit is available in:
- Google Cloud Dataflow (managed atomic commit facility)
- VoltDB (continuous export with transactional guarantees)
- Kafka Transactions (atomic offset commit + producer publish in a single transaction, available within the Kafka ecosystem)

For side effects that go outside these systems (email, external payment APIs), idempotence is the practical path.

**Practical guidance:**
- For writes to a database or key-value store: design upserts, use offset-keyed deduplication
- For messages published to another Kafka topic: use Kafka Transactions (exactly-once within Kafka)
- For emails, SMS, or external API calls: maintain a "sent" deduplication log keyed by event ID; check before sending
- For payment charges: use idempotency keys (all major payment APIs support them)
- For webhook calls: include the event ID; build the receiver to deduplicate by event ID
