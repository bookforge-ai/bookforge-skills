# Join Type Reference

Reference for Step 4 of `stream-processing-designer`.

---

## Why Joins Are Different on Streams

In batch processing, both sides of a join are bounded datasets loaded at a point in time. The join reads both sides fully, matches on the key, and produces output. The datasets do not change during the join.

On streams, both sides are unbounded and continuously changing. New events can arrive at any time on either side. The stream processor must maintain state — buffered events or a local copy of a reference table — to match events from different inputs. This state grows over time unless it is bounded by a window.

Three join types cover the common patterns. Each has different state requirements, ordering sensitivity, and time-dependence.

---

## Stream-Stream Join (Window Join)

**What it does:** Correlates events from two event streams where related events occur close in time, joined by a shared key.

**State required:** A buffer of recent events from both streams within a configurable time window, indexed by the join key.

**How it works:**
1. When an event from stream A arrives, add it to the A-side buffer indexed by join key
2. Check the B-side buffer for matching events (same join key, within the time window)
3. For each match, emit a joined output event
4. When an event from stream B arrives, same process in reverse
5. Evict events from both buffers when they fall outside the time window

**Time-dependence:** Results are time-dependent. If a user updates their profile between two correlated events, the join may pair them with different profile versions depending on the order of arrival. If events on different streams arrive in different orders on reruns, the join results differ.

**Ordering across streams:** There is typically no guaranteed ordering across different streams or partitions. Events on stream A and stream B may arrive in any interleaving order at the stream processor, even if they were produced in a clear causal order at the source.

**Use cases:**
- Click-through rate: join search query events with click events by session ID within 1 hour
- Advertising attribution: join ad impression events with conversion events by user ID within 24 hours
- Fraud detection: correlate transaction events with location events by user ID within 5 minutes
- Request-response matching: join request events with response events by request ID within a timeout

**Example — search click-through:**
```
Stream A: {session_id: "s1", query: "laptop", timestamp: 10:00}
Stream B: {session_id: "s1", url: "example.com/laptop", timestamp: 10:00:30}

Join key: session_id
Window: 1 hour

Output: {session_id: "s1", query: "laptop", clicked_url: "example.com/laptop", latency_sec: 30}
```

If no click arrives within the window, emit a "no click" event for the search.

**Configuration considerations:**
- Window size: Must be large enough to capture the natural delay between related events. Too small — misses real correlations. Too large — retains excessive state and joins unrelated events.
- State size: `buffer_size = event_rate * window_duration * avg_event_size`. For high-volume streams with large windows, this can be gigabytes. Choose checkpointing for recovery.

---

## Stream-Table Join (Stream Enrichment)

**What it does:** Enriches each event from an event stream with data from a reference table that is continuously updated via a changelog stream (typically CDC from a source database).

**State required:** A local copy of the reference table (or the relevant partition of it), maintained in the stream processor's local storage (in-memory hash map for small tables, RocksDB index for large tables).

**How it works:**
1. The stream processor subscribes to both the event stream and a CDC changelog of the reference table
2. When a table change event arrives, update the local copy
3. When an event from the main stream arrives, look up the join key in the local table copy and enrich the event
4. Emit the enriched event

**Key difference from batch:** In a batch job, the reference table is a point-in-time snapshot. In a stream-table join, the local copy is continuously updated — the processor joins each event against the version of the table that exists at the time the event is processed.

**Time-dependence:** This is a form of time-dependence. An activity event processed before a profile update is enriched with the old profile. An event processed after the update is enriched with the new profile. This is usually the desired behavior (reflect the state at the time of activity), but it must be documented.

**For historical correctness:** If reprocessing historical events, the local table copy will reflect the current state, not the historical state at the time of the original events. This can produce different results than the original processing run. Use slowly changing dimension (SCD) versioning if historical correctness is required:
- Assign a version ID to each table record when it changes
- Include the version ID in the event at processing time
- On reprocessing, join against the versioned table using the stored version ID

**Use cases:**
- Enrich user activity events with user profile (name, subscription tier, region)
- Enrich order events with product metadata (category, price tier, weight class)
- Enrich IoT sensor readings with device metadata (location, calibration factors)
- Enrich log events with service metadata (owner, SLA tier, dependency graph)

**Example — activity enrichment:**
```
Activity stream: {user_id: "u42", action: "checkout", amount: 199.00, ts: 10:05}
Profile CDC stream: {user_id: "u42", tier: "premium", region: "us-east", updated: 09:50}

Local table state at 10:05: user "u42" → {tier: "premium", region: "us-east"}

Output: {user_id: "u42", action: "checkout", amount: 199.00, tier: "premium", region: "us-east", ts: 10:05}
```

**Similarity to stream-stream join:** A stream-table join is a stream-stream join where the table-side join uses a conceptually infinite window (back to the beginning of time), with newer records overwriting older ones. The event-side join uses no window.

---

## Table-Table Join (Materialized View Maintenance)

**What it does:** Maintains a continuously updated materialized view of the join between two tables, both represented as changelog streams. When either table changes, the materialized view is recomputed.

**State required:** Both tables maintained in full in local storage. When either table changes, the affected portion of the join result is recomputed and emitted as a change event.

**How it works:**
1. Subscribe to changelog streams for both tables (Table A and Table B)
2. Maintain local copies of both tables
3. When a record in Table A changes, look up all matching records in Table B and emit updated join results
4. When a record in Table B changes, look up all matching records in Table A and emit updated join results
5. The output is a changelog stream of the materialized view

**Use cases:**
- Maintaining a per-user timeline cache (tweets table joined with follows table)
- Maintaining a denormalized product catalog view (products table joined with inventory table)
- Keeping a search index current (events table joined with metadata table)

**Twitter timeline example (canonical table-table join):**
```sql
-- The materialized view being maintained:
SELECT follows.follower_id AS timeline_id,
       array_agg(tweets.* ORDER BY tweets.timestamp DESC)
FROM tweets
JOIN follows ON follows.followee_id = tweets.sender_id
GROUP BY follows.follower_id
```

Event processing rules:
- New tweet by user U → add tweet to timeline of every follower of U
- Tweet deleted → remove from all followers' timelines
- User A follows user B → add B's recent tweets to A's timeline
- User A unfollows user B → remove B's tweets from A's timeline

The stream processor maintains the follower list for each user as a local table, updated via the follows changelog.

**Scale consideration:** Table-table joins can produce large fan-out: one tweet from a user with 10M followers triggers 10M timeline updates. At scale, this fan-out may require rate limiting, batching, or selective materialization (only materialize timelines for active users).

---

## Summary Table

| Dimension | Stream-Stream | Stream-Table | Table-Table |
|---|---|---|---|
| State | Both-sided event buffer (bounded by window) | Full reference table (or partition) | Both tables in full |
| Time scope | Bounded window on both sides | Infinite window on table side; no window on event side | Infinite on both sides |
| Trigger | Matching event arrives on either side | Event arrives on the stream side | Change arrives on either side |
| Typical latency sensitivity | High (correlating near-simultaneous events) | Medium (enrichment per event) | Medium (view updates on table changes) |
| Memory cost | Window size × event rate | Table size | Both table sizes |
| Nondeterminism risk | High (ordering across streams) | Medium (table version at processing time) | Medium (ordering of table changes) |
| Reprocessing behavior | May differ (different interleaving) | Will differ if table has changed | Will differ if tables have changed |

---

## Time-Dependence in Joins: The Slowly Changing Dimension Problem

All three join types share a common challenge: the joined data changes over time. If you rerun the same job on the same input, and the reference data has changed since the original run, you get different output. This is nondeterminism from state mutation.

**In data warehouses**, this is called the slowly changing dimension (SCD) problem. Standard solutions:

**SCD Type 1 — Overwrite:** Keep only the current value. Simple. Reprocessing produces results based on current data, not historical data. Acceptable when historical correctness is not required.

**SCD Type 2 — Versioning:** Create a new record for each version, with validity dates. Join against the version valid at the time of the event. Preserves historical correctness. Prevents log compaction (all versions must be retained).

Apply SCD Type 2 in stream joins when: billing, compliance, or audit requires that reprocessed results match original results exactly; the reference data changes frequently and the join result is sensitive to which version is used.
