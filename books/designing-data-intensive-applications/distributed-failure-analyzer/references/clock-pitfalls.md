# Clock Pitfalls in Distributed Systems

Full reference for Step 2 (clock unreliability) of the distributed-failure-analyzer skill.

---

## The Core Problem

Each node in a distributed system has its own hardware clock. Clocks are not perfectly accurate and cannot be perfectly synchronized. Software that assumes clock accuracy across nodes will behave incorrectly in ways that are subtle, silent, and difficult to reproduce.

"Synchronized" does not mean "accurate." Even with NTP running correctly, clocks across nodes may differ by tens of milliseconds. Under network congestion, errors can exceed 100 ms. In virtualized environments, clocks can jump forward by arbitrary amounts.

---

## Time-of-Day vs. Monotonic Clocks

### Time-of-day clock (wall-clock time)
- **API examples:** `clock_gettime(CLOCK_REALTIME)` (Linux), `System.currentTimeMillis()` (Java), `time.time()` (Python), `Date.now()` (JavaScript)
- **Returns:** seconds (or milliseconds) since the Unix epoch (midnight UTC, January 1, 1970)
- **Synchronized via:** NTP
- **Jump risk:** YES — if the local clock is ahead of the NTP server, it may be forcibly reset backward. Applications observing time before and after this reset see time go backward or jump forward.
- **Use for:** timestamps of events for human display, expiry dates, calendar scheduling.
- **Do NOT use for:** measuring elapsed time (can jump), ordering events across nodes (skew causes incorrect orderings).

### Monotonic clock
- **API examples:** `clock_gettime(CLOCK_MONOTONIC)` (Linux), `System.nanoTime()` (Java), `time.monotonic()` (Python)
- **Returns:** nanoseconds since an arbitrary point (usually system boot). The absolute value is meaningless.
- **Synchronized via:** not synchronized — does not need to be, because it is only used to measure duration on a single node.
- **Jump risk:** NO — guaranteed to always move forward. NTP may *slew* (speed up or slow down) the monotonic clock by up to 0.05%, but it cannot jump.
- **Use for:** timeouts, measuring response latency, measuring elapsed time on a single node.
- **Do NOT use for:** comparing times across different nodes (absolute values are incomparable).

**Rule:** Use monotonic clocks for timeouts and durations. Use time-of-day clocks only where you need a point in calendar time, and never for cross-node ordering.

---

## Sources of Clock Error

### 1. Quartz drift
- Quartz crystal oscillators run faster or slower depending on temperature.
- Google's assumption for server hardware: 200 ppm drift.
- 200 ppm = 6 ms drift for a clock resynchronized every 30 seconds; 17 ms/day for a clock synced once daily.
- Even with NTP, clock drift between syncs accumulates.

### 2. NTP accuracy limits
- NTP accuracy is bounded by network round-trip time to the NTP server.
- Minimum achievable error (local network, well-behaved): ~35 ms.
- Under network congestion: errors spike to over 100 ms.
- On public internet NTP servers: accuracy is limited further by variable internet latency.

### 3. NTP misconfiguration and blocking
- If a firewall blocks NTP traffic (UDP port 123), the NTP client cannot sync.
- The misconfiguration is silent — the clock keeps running and drifting.
- Anecdotal evidence: this happens in practice and goes unnoticed for extended periods.
- If the NTP client detects it is too far from the server's time, it may refuse to sync (to avoid destabilizing the system with a large jump).

### 4. Wrong or misconfigured NTP servers
- Some public NTP servers report incorrect times (hours off).
- NTP clients query multiple servers and reject outliers, but this protection is not perfect.

### 5. Leap seconds
- A leap second inserts an extra second (23:59:60) or deletes a second, making a minute 61 or 59 seconds.
- Systems not designed with leap seconds in mind have crashed.
- Best practice: configure NTP servers to "smear" the leap second — spread the adjustment gradually over the course of a day, so clocks see a slightly slower/faster rate of advance rather than a discontinuity.
- NTP server behavior on leap seconds varies in practice.

### 6. VM clock virtualization
- When a VM is paused (CPU time given to another VM), the VM's hardware clock is frozen.
- When the VM resumes, the hypervisor updates the VM's clock to the current time.
- From the application's perspective, the clock suddenly jumps forward by the pause duration.
- Pause durations for live migration: seconds to minutes, depending on memory write rate.
- This manifests as a time-of-day clock jump on resume.

---

## Clock-Based Anti-Patterns

### Anti-pattern 1: Last-write-wins with wall-clock timestamps

**How it fails:**
- In a multi-leader or leaderless database, concurrent writes to the same key from different nodes are resolved by keeping the write with the higher timestamp.
- If Node A's clock is 5 ms ahead of Node B's, a causally later write from Node B (timestamp = Node B's time) may have a lower timestamp than an earlier write from Node A (timestamp = Node A's time).
- Node B's write is discarded. No error is logged. The application has no idea.
- Example: Cassandra and Riak use LWW as a conflict resolution option.

**Concrete illustration (from the book, Figure 8-3):**
- Client A writes `x=1` on Node 1 at timestamp `42.004`.
- Client B increments `x` on Node 3, producing `x=2` at timestamp `42.003` (Node 3 is 1 ms behind).
- After replication, Node 2 receives both. LWW picks `x=1` (higher timestamp). Client B's increment is lost.
- Clock skew of 1 ms is sufficient to cause data loss. Typical inter-datacenter skew is much larger.

**Fix:**
- Replace LWW timestamp-based resolution with logical clocks (version vectors) for causal ordering.
- If LWW is required by the storage system, monitor clock offsets between nodes and alert when skew exceeds an acceptable threshold. Nodes with excessive drift should be removed.

### Anti-pattern 2: Using clock timestamps as transaction IDs for ordering

**How it fails:**
- Generating monotonically increasing transaction IDs from wall-clock time in a distributed system requires that clocks are synchronized well enough that a later transaction on any node always gets a higher timestamp than earlier transactions.
- This is not achievable with NTP alone. Two transactions on different nodes within the same millisecond may receive the same timestamp.
- Transaction ID ordering breaks; snapshot isolation semantics are violated.

**Partial solution (Google Spanner's TrueTime):**
- Spanner's TrueTime API returns `[earliest, latest]` for the current time.
- Spanner waits out the uncertainty interval before committing a transaction — ensuring that any future transaction's earliest possible timestamp is after the current transaction's latest possible timestamp.
- This provides correct ordering at the cost of commit latency proportional to the uncertainty interval (~7 ms with GPS/atomic clocks in each datacenter).
- Not practical without GPS/atomic clock infrastructure.

**Alternative:** Use logical clocks (Lamport timestamps, vector clocks) or a centralized sequence number generator for transaction IDs. Twitter's Snowflake generates approximately monotonically increasing IDs in a distributed way (but cannot guarantee consistency with causality).

### Anti-pattern 3: Clock-based lease validity check before a protected operation

Documented separately in `fencing-token-pattern.md`. In brief: checking `System.currentTimeMillis() < leaseExpiryTime` before acting on the lease is not atomic with the action. A process pause between the check and the action can cause the lease to have expired by the time the action executes.

---

## Clock Monitoring

Incorrect clocks are insidious because most things continue to work. The system does not crash or throw errors — it silently produces wrong results or drops data. This is why explicit monitoring is essential.

**Recommended monitoring:**
1. **NTP offset metrics**: track the offset between each node's clock and the NTP server. Alert when offset exceeds your acceptable threshold (typically 50–100 ms for most applications; much tighter for financial or high-precision systems).
2. **Inter-node clock skew**: for systems using timestamp-based conflict resolution, directly measure clock differences between nodes. Alert when skew approaches the granularity of your timestamps.
3. **Node removal on excessive drift**: any node whose clock drifts too far from the others should be declared dead and removed from the cluster. The node's incorrect timestamps can corrupt data or cause incorrect ordering.

**Tools:** `ntpq -p` (NTP status), `chronyc tracking` (chrony), Prometheus `node_timex_offset_seconds` metric, AWS CloudWatch `ClockErrorBound` for Spanner-equivalent services.

---

## When Clock Accuracy Really Matters

For most server-side data systems, the mitigations above are sufficient. But some domains require sub-millisecond clock accuracy:

- **High-frequency trading:** MiFID II (European regulation) requires financial institutions to synchronize clocks to within 100 microseconds of UTC.
- **Distributed tracing and log correlation:** millisecond-accurate clocks are usually sufficient; sub-millisecond is rarely needed.
- **Distributed snapshot isolation (Spanner-style):** requires GPS receivers or atomic clocks per datacenter.

For these use cases, the Precision Time Protocol (PTP, IEEE 1588) and GPS/atomic clock hardware are the relevant tools, not NTP.
