# Window Type Selection Reference

Reference for Step 3 of `stream-processing-designer`.

---

## Why Windows Exist

A stream is infinite. Aggregations (count, sum, average, percentile) require a bounded dataset. Windows bound the stream by time (or event count, but time-based windows dominate in practice), making aggregations computable.

Windows are also the mechanism by which stream processing achieves the equivalent of `GROUP BY time_bucket(...)` in SQL — except the "table" is unbounded and rows arrive continuously.

---

## Event Time vs. Processing Time

**Event time:** The timestamp embedded in the event itself — the time the event actually occurred. Correct for analytics and any computation where the result should reflect when things happened.

**Processing time:** The wall-clock time on the stream processor machine when the event is being processed. Simpler (no timestamp parsing), but produces artifacts when:
- The processor restarts and processes a backlog: all backlog events are assigned the current processing time, producing a false spike
- Events are delayed by network, queue backlog, or client buffering: delayed events appear in the wrong window
- The processor is redeployed and reprocesses historical events: results differ from the original run

**Rule:** Use event time for any computation where correctness matters. Use processing time only for monitoring-of-the-monitor (e.g., measuring stream processor lag itself) or when delays are negligibly small and approximation is acceptable.

**Implementation note:** Using event time requires that the stream processor read the timestamp from each event and route the event to the correct window based on that timestamp, not the current clock. This is how Flink's EventTime processing mode works.

---

## The Four Window Types

### Tumbling Window

**Shape:** Fixed length, non-overlapping. Every event belongs to exactly one window.

**Visualization:**
```
Time:   |---window1---|---window2---|---window3---|
Events: A  B  C  D  E  F  G  H  I  J  K  L  M
```

**Properties:**
- Each event belongs to exactly one window
- Contiguous — no gaps between windows
- Simplest to implement and reason about

**Implementation:** `window_id = floor(event_timestamp / window_size) * window_size`

**Use when:**
- Periodic reporting (hourly totals, daily summaries, per-minute request counts)
- Business metrics that align to calendar periods (hourly SLAs, daily revenue)
- Any aggregation where "which window does this event belong to" has a single clear answer

**Example:** Count HTTP requests per minute for a rate dashboard.

---

### Hopping Window

**Shape:** Fixed length with overlap. Hop size < window size. Each event belongs to `window_size / hop_size` windows.

**Visualization (5-min window, 1-min hop):**
```
W1: |--10:00 to 10:05--|
W2:     |--10:01 to 10:06--|
W3:         |--10:02 to 10:07--|
```

**Properties:**
- Smoothing effect: the window advances in small steps, so abrupt changes at window boundaries are reduced
- Higher computation cost than tumbling: each event is processed multiple times
- Multiple windows overlap at any point in time

**Implementation:** Compute tumbling windows at the hop size, then aggregate over `window_size / hop_size` adjacent tumbling windows.

**Use when:**
- Rolling averages: "average over the last 5 minutes, updated every 1 minute"
- Trend detection where abrupt metric changes at tumbling window boundaries would create false alarms
- Smoothed metrics for dashboards

**Example:** 5-minute rolling 99th percentile response time, updated every 30 seconds.

---

### Sliding Window

**Shape:** Variable-length based on event proximity. Groups all events within a fixed time interval of each other, regardless of fixed boundaries.

**Visualization (5-min sliding):**
```
Events at: 10:03:39, 10:08:12 → same window (8m12s - 3m39s = 4m33s < 5min)
Events at: 10:03:39, 10:09:00 → different windows (9m00s - 3m39s = 5m21s > 5min)
```

**Properties:**
- No fixed boundaries — window is defined by proximity between events
- Correctly captures co-occurrence regardless of which "period" the events fall in
- Higher memory cost: requires buffering all recent events sorted by time

**Implementation:** Maintain a buffer of recent events sorted by timestamp. When a new event arrives, include all events within `[now - window_size, now]`. Evict events older than `window_size`.

**Use when:**
- Detecting events that co-occur within a time proximity (rapid successive failures, correlated errors)
- Computing "events within N minutes of each other" where fixed boundaries would split natural pairs
- Proximity-based detection in monitoring, fraud detection, anomaly detection

**Example:** Detect 5 failed login attempts within any 10-minute window, regardless of clock-aligned boundaries.

---

### Session Window

**Shape:** No fixed duration. Groups events from the same entity (user, device, session) that occur close together, with a gap closing the window when no events arrive for a timeout period.

**Visualization (30-min timeout):**
```
User A: [click, click, click]---30min gap---[click, click]
         |--- session 1 ---|               |-- session 2 --|
```

**Properties:**
- Window duration is data-driven — active users have long sessions, inactive users have short ones
- Windows are per-entity (keyed by user ID, device ID, session ID)
- Complex state management: sessions must be merged if new events arrive that bridge a gap

**Implementation:** For each entity key, maintain the session start time and last-event time. On new event: if `event_time - last_event_time < gap_timeout`, extend session; otherwise, close current session and start new one.

**Use when:**
- Website or app session analytics (session duration, page views per session)
- User engagement measurement (time spent in app between inactivity periods)
- Any "activity burst" pattern where the natural unit is a continuous period of activity

**Example:** E-commerce session analytics — group all page views and clicks per user into sessions with a 30-minute inactivity timeout.

---

## Decision Table

| Requirement | Window Type |
|---|---|
| Periodic reports aligned to calendar periods | Tumbling |
| Smoothed metrics without abrupt boundaries | Hopping |
| Events co-occurring within a time proximity, regardless of period | Sliding |
| User activity grouped into natural activity bursts | Session |
| Multiple aggregation periods simultaneously | Multiple tumbling windows |
| Rolling percentiles updated frequently | Hopping |
| Fraud pattern: N events within any N-minute period | Sliding |
| Session duration and depth analytics | Session |

---

## Straggler Event Handling

When using event-time windows, some events arrive after the window has been declared complete. Causes:
- Mobile clients buffering events offline and sending them when connectivity resumes (hours or days of delay)
- Network delays or queue backlog causing modest delays (seconds to minutes)
- Clock skew on the producing device

**Option 1 — Ignore stragglers:**
Declare the window complete after a configurable watermark (e.g., close window when processing time has advanced 5 minutes past the window end). Emit the result. Track straggler count as a metric. Alert if straggler rate exceeds a threshold.

Appropriate when: Straggler rate is low; downstream users understand results are approximate; correction is operationally costly.

**Option 2 — Publish corrections:**
Emit a preliminary result when the watermark is reached. Emit a corrected result if stragglers arrive within a further allowance period. The downstream system must handle retraction and replacement of the earlier result.

Appropriate when: Results are used for billing, compliance, SLA reporting, or any context where downstream users act on results and need corrections.

**Watermark:** A signal from the stream processor indicating "all events with timestamps earlier than T have been processed." Watermarks advance as event timestamps advance. A watermark can be generated from the minimum observed event timestamp across all partitions, minus a configurable lateness allowance.

---

## Clock Skew on Producing Devices

For events produced by mobile devices or IoT sensors, the device clock may be wrong. Strategy: record three timestamps per event:
1. Event occurrence time (device clock) — the semantic timestamp
2. Event send time (device clock) — when the device attempted to send
3. Event receive time (server clock) — when the server received it

Estimate clock offset: `receive_time - send_time` (assuming negligible network delay). Apply this offset to the event occurrence timestamp to approximate the true event time.

This does not eliminate clock skew, but reduces systematic errors. Document the approach in the pipeline — downstream users need to know that event timestamps are estimates with bounded error.
