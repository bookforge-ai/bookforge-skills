# Failure Taxonomy: Network, Clock, Process

Full reference for Step 1 and Step 2 of the distributed-failure-analyzer skill.

---

## Category A: Network Faults

### Background
The distributed systems discussed in this context are **shared-nothing systems**: nodes have their own memory and disk; communication happens only via messages over a network. Most internal datacenter networks (Ethernet) and the internet are **asynchronous packet networks**: there is no upper bound on delivery time, and no delivery guarantee.

### The Six Network Failure Modes (for a single request/response)

When a client sends a request and receives no response, any of these may have occurred:

| # | What failed | Distinguishable? | Notes |
|---|---|---|---|
| 1 | Request lost in transit | No | Cable unplugged, queue drop, routing failure |
| 2 | Request queued, not yet delivered | No | Network congestion, switch buffer full |
| 3 | Remote node crashed | No | Indistinguishable from 1, 5, 6 via timeout alone |
| 4 | Remote node temporarily unresponsive | No | GC pause, high load — node will recover |
| 5 | Response lost in transit | No | Misconfigured switch, asymmetric fault |
| 6 | Response delayed | No | Overloaded network or receiver node |

**Critical implication:** A timeout tells you that you stopped waiting. It does not tell you whether the remote node executed your request. If you retry after a timeout, the operation may execute twice.

### Network Fault Detection Signals

- **TCP RST or FIN**: the OS on the remote machine closed the port (process crashed, port not listening). Does not tell you how much work the process completed before crashing.
- **ICMP Destination Unreachable**: the router believes the IP is unreachable. Subject to the same limitations as other participants.
- **Management interface query**: for switches you control, can confirm link-level failure at hardware level. Not available in shared/cloud environments.
- **Application-level acknowledgment**: the only reliable confirmation that a request was processed correctly. TCP acknowledgment confirms delivery to the OS, not to the application.

### Network Fault Statistics (real-world)
- One study of a medium-sized datacenter: ~12 network faults per month. Half disconnected a single machine; half disconnected an entire rack.
- Adding redundant networking gear does not proportionally reduce faults — human error (misconfiguration) is a primary cause.
- Public clouds (e.g., EC2): frequent transient network glitches are documented.
- Asymmetric faults observed in practice: a network interface that drops all inbound packets but sends outbound packets successfully.

### Timeout Calibration

**Problem:** A long timeout delays failure detection. A short timeout causes false positives — declaring a live-but-slow node dead.

**Cascade failure mechanism:** Node declared dead → load redistributed to remaining nodes → remaining nodes become slower → their health checks time out → more nodes declared dead → cluster collapses.

**Calibration approach:**
1. Measure round-trip time distribution over an extended period, across many machines.
2. Set timeout at p99 or p99.9 latency under expected peak load, not median.
3. Add jitter to prevent synchronized timeout storms.
4. Consider adaptive failure detectors: **Phi Accrual** (used in Akka, Cassandra, and in TCP retransmission) dynamically adjusts the failure threshold based on observed jitter.

**Formula for a theoretical synchronous network:** If max packet delay is `d` and max processing time is `r`, timeout = `2d + r`. In asynchronous networks there is no `d`, so there is no correct value — only empirical calibration.

---

## Category B: Clock Unreliability

### Background
Each node has its own hardware clock — typically a quartz crystal oscillator. Clocks drift (run faster or slower than real time). Distributed systems cannot share a clock.

### Clock Types

| Type | Purpose | Cross-node comparison | Jump risk |
|---|---|---|---|
| Time-of-day (wall-clock) | Points in time (timestamps, event ordering) | Not safe | Yes — can jump backward on NTP reset |
| Monotonic | Elapsed time (durations, timeouts) | Never safe | No — guaranteed always forward |

**Rule of thumb:** Use monotonic clocks for timeouts and measuring durations on a single node. Never use time-of-day clocks to order events across nodes.

### Sources of Clock Error

| Source | Typical magnitude | Notes |
|---|---|---|
| Quartz drift | Up to 200 ppm (Google's server assumption) | 200 ppm = 6 ms drift if synced every 30s; 17 ms/day if synced once a day |
| NTP sync error | ~35 ms minimum on congested networks; spikes to >100 ms | Limited by network round-trip time |
| NTP firewall block | Unbounded — grows without bound | Goes unnoticed until clock is severely wrong |
| Wrong/misconfigured NTP servers | Hours off | Some public NTP servers are misconfigured |
| Leap seconds | ±1 second | A minute may be 59 or 61 seconds; has crashed production systems |
| VM time virtualization | Tens of milliseconds per pause | When a VM is paused (CPU given to another VM), the clock jumps forward on resume |
| User-controlled clocks | Arbitrary | On user devices (mobile, embedded); users may set clocks to incorrect values intentionally |

### Clock Confidence Interval
A clock reading is not a point in time — it is a range. `clock_gettime()` returns a single value but does not expose its uncertainty. The actual time may be anywhere within a confidence interval.

Google's **TrueTime API** (used in Spanner) explicitly returns `[earliest, latest]` — the earliest and latest possible current time. Spanner waits out the confidence interval before committing read-write transactions to ensure causal ordering. This requires GPS receivers or atomic clocks in each datacenter (uncertainty: ~7 ms).

For most systems without TrueTime: assume clock uncertainty of tens of milliseconds on a LAN, and design accordingly.

### Last-Write-Wins (LWW) Data Loss Mechanism

1. Client A writes `x=1` on Node 1 at wall-clock time `t=42.004`.
2. Client B increments `x` on Node 3, resulting in `x=2` at wall-clock time `t=42.003` (Node 3's clock is 1 ms behind Node 1's).
3. Both writes replicate to Node 2.
4. Node 2 applies LWW: `t=42.004 > t=42.003`, so `x=1` wins.
5. Client B's increment (`x=2`) is silently discarded. No error is reported.

**Detection:** Monitor inter-node clock offset. Alert when skew exceeds the acceptable threshold for your LWW use case. Nodes with excessive drift should be removed from the cluster before they cause data loss.

**Fix:** Replace LWW timestamp-based conflict resolution with **logical clocks** (version vectors, Lamport timestamps) for causal ordering. Logical clocks do not measure wall-clock time — they track only causal happens-before relationships, which are correct regardless of clock skew.

---

## Category C: Process Pauses

### Background
A thread can be preempted at any arbitrary point in its execution and paused for an arbitrary duration. The thread has no awareness that it was paused — when it resumes, it continues from where it left off, with no knowledge that real time has passed.

### Pause Causes

| Cause | Typical duration | Notes |
|---|---|---|
| Stop-the-world GC | Milliseconds to several seconds | JVM, .NET, Ruby. "Concurrent" collectors (CMS) still have stop-the-world phases. |
| VM suspension / live migration | Seconds to minutes | Hypervisor saves VM memory to disk; restores on another host. Cloud providers do this without notice. |
| OS context switch | Microseconds to milliseconds | Normal, but under CPU steal (multi-tenant) the paused thread may wait much longer. |
| CPU steal time | Variable | Another VM is using the shared CPU core. The paused VM's threads wait with no awareness. |
| Synchronous disk I/O | Milliseconds to seconds | Worse on network-attached storage (EBS, NFS). Java class loading can trigger this unexpectedly. |
| Memory paging (thrashing) | Seconds | OS swaps pages to disk under memory pressure. Extreme: system spends most time swapping. |
| SIGSTOP signal | Arbitrary — until SIGCONT | Sent by Ctrl-Z in a shell, or accidentally by operations tooling. |

### The Zombie Problem
When a paused node resumes:
1. It does not know it was paused.
2. Its wall-clock time jumps forward (in virtualized environments).
3. It checks its state (e.g., lease validity) and finds it appears valid.
4. It continues its previous role — even though the rest of the cluster has declared it dead, elected a new leader, or granted a new lock.
5. Result: two nodes acting as leader simultaneously, or two lock-holders writing to the same resource.

### GC Pause Mitigation (without real-time systems)
- **Treat GC pauses as planned node outages**: drain requests from the node before GC, let other nodes handle traffic during GC, resume the node after collection.
- **Use short-lived object patterns**: restart processes periodically before long-lived objects accumulate enough to trigger a full GC. This works like a rolling restart.
- **Tune GC settings**: increase heap size (delays GC), tune allocation patterns. Reduces frequency but does not eliminate pauses.
- **Monitor**: track GC pause durations. Alert on pauses that exceed your timeout budget.

---

## Summary: Symptom-to-Category Quick Reference

| Symptom | Most likely category | Secondary category |
|---|---|---|
| Intermittent timeout, node recovers | A (network) or C (process pause) | — |
| Node declared dead, then recovers with no awareness of downtime | C (process pause) | A (asymmetric network fault) |
| Two leaders active simultaneously | C (pause caused zombie) or A (split brain) | — |
| Silent data loss after concurrent writes | B (clock / LWW) | — |
| Lock corruption despite mutual exclusion code | C (pause caused zombie) | — |
| Stale reads longer than replication lag | A (delayed response) or B (clock) | — |
| Cascading node-death declarations under load | A (timeout miscalibration) | — |
| Clock-ordered events appear out of causal order | B (clock skew) | — |
