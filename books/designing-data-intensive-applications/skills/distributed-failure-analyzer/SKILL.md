---
name: distributed-failure-analyzer
description: |
  Diagnose distributed system failures caused by network faults, unreliable clocks, or process pauses — and map each to its correct mitigation. Use when: a node is intermittently timing out with no clear network outage; a lock-holder or leader keeps acting after being declared dead (zombie leader / split brain via distributed locking, not replication topology — use replication-failure-analyzer for replica split brain); stale reads persist beyond expected replication lag; wall-clock-based lease checks or last-write-wins conflict resolution is producing data loss under clock skew; or cascading node-death declarations are occurring under load. Also use proactively to audit timing assumptions in new system designs (absence of fencing tokens, NTP drift exposure, GC pause risk). Distinct from replication-failure-analyzer (replication lag anomalies, failover pitfalls, quorum edge cases). Produces a structured failure report: symptom → fault category → mechanism → mitigation. Covers: asynchronous network behavior, timeout tuning and cascade risk, NTP drift and clock jump mechanics, process pause causes (GC, VM migration, paging, SIGSTOP), fencing tokens with ZooKeeper zxid/cversion, Byzantine fault scoping, and system model selection (crash-stop vs. crash-recovery vs. Byzantine; synchronous vs. partially synchronous vs. asynchronous).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/distributed-failure-analyzer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - replication-strategy-selector
  - consistency-model-selector
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [8]
tags:
  - distributed-systems
  - failure-analysis
  - network-faults
  - unreliable-clocks
  - process-pauses
  - fencing-tokens
  - zombie-leader
  - split-brain
  - distributed-locking
  - last-write-wins
  - clock-skew
  - ntp-drift
  - garbage-collection
  - partial-failure
  - timeout-tuning
  - byzantine-faults
  - system-model
  - crash-recovery
  - quorum
  - zookeeper
  - lease-expiry
  - partial-synchrony
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application source code, infrastructure configs (docker-compose, k8s manifests), or architecture description revealing timing assumptions, locking patterns, and clock usage"
    - type: document
      description: "Incident report, runbook, or architecture description if no codebase is available"
    - type: description
      description: "User-described symptoms: what failed, when, topology, observed behavior vs. expected behavior"
  tools-required: [Read, Write, Grep]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory with codebase or configuration files, or accept a verbal description of the failure. Produces a written failure analysis report."
discovery:
  goal: "Produce a structured failure analysis report: classify each symptom into its fault category, identify the specific mechanism, and recommend concrete mitigations"
  tasks:
    - "Gather failure symptoms, system topology, and observed vs. expected behavior"
    - "Classify each symptom into network fault, clock unreliability, or process pause"
    - "Identify the specific failure mechanism within the category"
    - "Scan codebase for anti-patterns (clock-based ordering, unguarded lease checks, missing fencing tokens)"
    - "Recommend mitigations matched to the root cause"
    - "Assess Byzantine fault risk and whether it is relevant to this context"
    - "Select appropriate system model assumptions for the architecture"
  audience:
    roles: ["backend-engineer", "software-architect", "site-reliability-engineer", "tech-lead", "data-engineer"]
    experience: "intermediate-to-advanced — assumes familiarity with distributed systems concepts"
  triggers:
    - "Intermittent timeouts with no clear network cause"
    - "Data disappearing or being silently overwritten after concurrent writes"
    - "A node or leader that continues acting after being declared dead"
    - "Stale reads that persist longer than replication lag explains"
    - "Cascading node-death declarations under load"
    - "Distributed lock / lease behavior that appears correct but causes corruption under failure"
    - "Designing a system and wanting to audit timing and locking assumptions before shipping"
  not_for:
    - "Choosing a replication topology — use replication-strategy-selector"
    - "Selecting consistency and isolation levels — use consistency-model-selector"
    - "Diagnosing replication lag anomalies specifically — use replication-failure-analyzer"
---

## When to Use

You are diagnosing or preventing a failure in a distributed system and the root cause is not immediately obvious. The symptom could be: a timeout that might mean the remote node is dead, or might mean the network is congested, or might mean the node is alive but paused. A write that appeared to succeed but whose data is now missing. A leader that is still writing after another leader was elected. A lock that was held correctly but still allowed two writers simultaneously.

This skill imposes a diagnostic framework: every unexplained distributed system failure traces to one of three root fault categories — **network faults**, **clock unreliability**, or **process pauses** — and each category has a bounded set of mechanisms and well-understood mitigations. The skill maps symptoms to categories, categories to mechanisms, and mechanisms to concrete fixes.

Use it reactively (incident post-mortem, production debugging) or proactively (design review, codebase audit for timing anti-patterns).

Cross-references:
- `replication-failure-analyzer` — for failures specific to replication lag, failover, and quorum behavior
- `consistency-model-selector` — for selecting isolation and consistency guarantees that prevent a class of failures at the application layer

---

## Context and Input Gathering

Before analysis, collect the following. Ask the user for any that are missing.

**Required:**
1. **Symptom description** — what was observed vs. what was expected. Be concrete: "node A sent a write that was confirmed, but the data is now absent on node B" is better than "data loss."
2. **System topology** — number of nodes, roles (leader/follower, lock-holder/client, partitioned shards), deployment environment (bare metal, VMs, cloud, containers).
3. **Failure timeline** — when did it start, is it reproducible, does it correlate with load spikes, deploys, or maintenance events?

**Useful:**
4. **Infrastructure configuration** — timeout values, NTP setup, GC settings (heap size, collector type), VM migration policies.
5. **Relevant code** — any section that checks wall-clock time, holds a lease or lock, does conflict resolution (especially last-write-wins), or makes assumptions about execution timing.
6. **Logs or metrics** — round-trip time distributions, GC pause logs, NTP offset metrics, CPU steal time.

**If no codebase is available:** accept a verbal architecture description and produce an analysis based on stated behavior patterns. The output will note which findings are speculative vs. confirmed.

---

## Process

### Step 1 — Map symptoms to the fault taxonomy

WHY: Distributed failures are non-deterministic and the same symptom can arise from multiple root causes. The three-category taxonomy forces explicit elimination: you cannot address "network issues" without first determining which of the six network failure modes is actually occurring, or whether it is a process pause mimicking a network failure.

For each reported symptom, classify it against this taxonomy:

**Category A: Network faults**
The network is an asynchronous packet network with unbounded delays. When a request is sent and no response arrives, it is impossible to distinguish which of these occurred:
1. Request lost in transit (cable, queue drop)
2. Request queued, not yet delivered (network congestion, switch buffer overflow)
3. Remote node crashed or was powered down
4. Remote node temporarily unresponsive (GC pause — overlaps Category C)
5. Response lost in transit (misconfigured switch, asymmetric fault)
6. Response delayed (network or receiver overloaded)

Key diagnostic signal: **timeouts tell you nothing about whether the remote node executed your request.** A timeout means you gave up waiting; it does not mean the request failed.

**Category B: Clock unreliability**
Each node has its own hardware clock (quartz oscillator). Clocks drift and can jump:
- **Time-of-day clock** (wall-clock time): synchronized via NTP, but NTP accuracy is limited by network round-trip time. On a congested network, NTP error can be 35ms to over 100ms. Clocks may jump backward if they are ahead of the NTP server.
- **Monotonic clock**: suitable for measuring elapsed time (durations, timeouts) on a single node. Cannot be compared across nodes — the absolute value is meaningless.
- **Sources of clock error**: quartz drift (up to 200 ppm = 17 seconds/day without sync), NTP misconfiguration (firewall blocking NTP traffic), NTP server errors (some servers are wrong or misconfigured), leap seconds (a minute can be 59 or 61 seconds), VM virtualization (CPU time-sharing pauses the VM; from the application's view, the clock jumps forward).

**Category C: Process pauses**
A thread can be preempted at any point in its execution and paused for an arbitrary duration without being notified. Pause causes:
- **Stop-the-world GC**: JVM, .NET, Ruby, and others pause all threads during major GC. Pauses of several seconds are possible even with "concurrent" collectors like CMS (which still has stop-the-world phases).
- **VM suspension**: a hypervisor may suspend a VM (save memory to disk) and resume it seconds or minutes later — live migration between hosts does this.
- **OS context switches / CPU steal**: in multi-tenant environments, another VM consuming a shared CPU core creates "steal time" — the paused VM's threads wait with no awareness that real time is passing.
- **Disk I/O**: synchronous disk access pauses the thread. In Java, class loading can trigger disk I/O unexpectedly. On network-attached storage (EBS, NFS), I/O latency inherits network variability.
- **Memory paging (thrashing)**: if the OS swaps pages to disk under memory pressure, a thread can be paused waiting for page-in. In extreme cases the system spends most of its time paging.
- **SIGSTOP**: a Unix signal that immediately halts a process until SIGCONT. Sent accidentally by operators (Ctrl-Z in a shell), or by tooling.

After categorizing, state the most probable category per symptom and note any ambiguity.

---

### Step 2 — Identify the specific failure mechanism

WHY: The category narrows the space; the mechanism identifies the specific causal chain and determines which mitigation is effective. A "clock unreliability" failure caused by NTP being blocked at the firewall needs a different fix than one caused by VM time virtualization.

**For network faults:**
- Distinguish between node death (crash-stop) and node pause (crash-recovery or process pause). If the node later recovers, it is likely a pause, not a crash.
- Check for asymmetric faults: a node can receive messages but its outgoing messages are dropped. This node will appear dead to the rest of the cluster despite being healthy. Symptom: the "dead" node does not know it has been declared dead.
- Check for timeout calibration: is the timeout shorter than the 99th percentile round-trip time under load? Premature timeouts under load cause cascading failures — a node declared dead transfers its load to other nodes, which increases their load, which makes them slower, which causes more timeouts, which declares more nodes dead.

**For clock unreliability:**
- Identify whether the code uses wall-clock time for **ordering events across nodes** (anti-pattern) or for **measuring elapsed time on a single node** (acceptable with monotonic clock).
- Last-write-wins (LWW) conflict resolution using wall-clock timestamps is the canonical clock anti-pattern: a node with a lagging clock will silently discard writes from a node with a fast clock, because the lagging node's writes appear "more recent." Data is lost with no error reported to the application.
- Lease checks using wall-clock time are unsafe if the clock can jump or if a process pause occurs between the check and the protected operation (see Step 4).

**For process pauses:**
- GC pause: correlate with GC logs. Look for stop-the-world events. Check heap size and object allocation rate. Long-lived objects accumulate and force full GC.
- VM migration: check hypervisor or cloud provider logs for live migration events.
- Thrashing: check system swap metrics and page fault rates.
- The defining characteristic: **the paused node does not know it was paused.** When it resumes, it checks its clock and finds that very little time has passed (from its perspective). It has no awareness that the rest of the cluster has moved on, elected a new leader, or acquired a new lock.

---

### Step 3 — Scan the codebase for anti-patterns (if codebase is available)

WHY: Many distributed system bugs are latent — they exist in the code but only manifest under specific timing conditions (high load, GC pressure, VM migration). Proactive scanning finds them before they trigger in production.

Search for:

**Anti-pattern 1: Wall-clock time used for cross-node event ordering**
```
# Look for: System.currentTimeMillis(), time.time(), Date.now(), new Date()
# used to timestamp events that are replicated or compared across nodes
```
Risk: If last-write-wins is the conflict resolution strategy and timestamps come from node clocks, any clock skew causes silent data loss.
Fix: Use logical clocks (version vectors, Lamport timestamps) for causal ordering. Use physical clocks only for duration measurement (monotonic clock).

**Anti-pattern 2: Client-side lease/lock validity check before a protected operation**
```
# Look for: if (lease.isValid()) { ... do protected operation ... }
# or: if (System.currentTimeMillis() < leaseExpiryTime) { ... }
```
Risk: A process pause between the check and the operation can cause the lease to expire. The node proceeds, believing it still holds the lock, while another node has already acquired it.
Fix: The resource itself must enforce the fencing token (see Step 4). Client-side checks are defense-in-depth only, not a correctness guarantee.

**Anti-pattern 3: Timeout values hard-coded without accounting for load variability**
```
# Look for: timeout = 5000 (fixed constant), no jitter, no adaptive adjustment
```
Risk: Timeouts calibrated for p50 latency will fire on p99 latency spikes, causing false node-death declarations.
Fix: Measure round-trip time distribution empirically. Set timeout at p99 + safety margin. Consider adaptive failure detectors (Phi Accrual, used in Akka and Cassandra) that adjust based on observed jitter.

**Anti-pattern 4: Distributed locking without fencing tokens**
```
# Look for: acquire lock → use resource → release lock
# without any monotonically-increasing token passed to the resource
```
Risk: A zombie lock-holder (paused during lock hold, revived after expiry) will corrupt shared state by writing concurrently with the legitimate new lock-holder.
Fix: See Step 4.

---

### Step 4 — Apply the fencing token pattern (for zombie leader / zombie lock-holder failures)

WHY: Any lease or lock system that relies on the lock-holder checking its own lease status is vulnerable to process pauses. The lock-holder cannot detect that it was paused; the check passes because, from the holder's perspective, no time has elapsed. The only correct solution puts enforcement in the resource, not the client.

**The fencing token pattern:**

Every time the lock service grants a lock or lease, it returns a **fencing token** — a monotonically increasing integer (each new grant increments the counter). The lock-holder includes its token in every request to the protected resource. The resource tracks the highest token it has seen and rejects any request with a lower token.

Concrete mechanics:
1. Client 1 acquires lock → receives token 33.
2. Client 1 goes into a stop-the-world GC pause for 15 seconds.
3. Client 1's lock expires. Client 2 acquires lock → receives token 34.
4. Client 2 writes to the resource with token 34. Resource records "highest seen: 34."
5. Client 1 resumes. It believes it still holds the lock (lease check passes — its clock says almost no time has elapsed). It sends a write with token 33.
6. Resource rejects Client 1's write: token 33 < 34. Corruption prevented.

**ZooKeeper integration:** If ZooKeeper is used as the lock service, the transaction ID `zxid` or the node version `cversion` serve as fencing tokens. They are guaranteed to be monotonically increasing.

**When the resource does not support fencing tokens natively:** For a file storage service, encode the fencing token in the filename or as a conditional write (compare-and-swap on a version field). Some kind of server-side enforcement is required — client-side enforcement alone is not sufficient for correctness.

**Important:** Fencing tokens protect against *inadvertent* zombie behavior (a node that does not know it has been declared dead). They do not protect against *deliberate* misbehavior — that requires Byzantine fault tolerance (see Step 5).

---

### Step 5 — Assess Byzantine fault risk

WHY: Byzantine fault tolerance is expensive and complex. For most datacenter systems it is unnecessary. The analysis must be explicit about whether Byzantine faults are in scope, so engineering effort is not misallocated.

**Byzantine faults are relevant when:**
- Nodes may send arbitrary, incorrect, or malicious messages (not just slow or silent).
- The system spans multiple organizations where participants may have conflicting incentives (blockchain, inter-bank settlement).
- Hardware operates in high-radiation environments (aerospace, embedded safety systems) where memory or CPU registers may be silently corrupted.

**Byzantine faults are NOT relevant for most server-side data systems when:**
- All nodes are controlled by your organization.
- The threat model is accidental failure, not adversarial behavior.
- Radiation levels are low enough that memory corruption is not a realistic concern.

For typical datacenter systems: assume crash-recovery faults (nodes may fail and restart, stable storage survives crashes, in-memory state is lost on crash), not Byzantine faults. Standard authentication, checksums in the application protocol, and NTP with multiple servers cover the "weak lying" cases (corrupted packets, misconfigured servers) without the overhead of full Byzantine fault-tolerant protocols.

---

### Step 6 — Select the appropriate system model

WHY: Distributed algorithms are designed for specific system model assumptions. Running an algorithm in a system whose actual behavior violates its model assumptions causes correctness failures. This step makes the model explicit so algorithm selection is grounded.

**Timing models:**

| Model | Assumption | Reality fit |
|---|---|---|
| Synchronous | Bounded network delay, bounded process pauses, bounded clock error | Not realistic for most packet networks and commodity hardware |
| Partially synchronous | Usually synchronous, occasionally exceeds bounds | Realistic for most production systems |
| Asynchronous | No timing assumptions, no timeouts | Very restrictive; few practical algorithms can operate without timeouts |

**Node failure models:**

| Model | Assumption | When to use |
|---|---|---|
| Crash-stop | Node fails by stopping; never recovers | Simplest; safe assumption for algorithm design even if nodes do recover |
| Crash-recovery | Nodes may crash and restart; stable storage survives; in-memory state is lost | Realistic for server-side systems with durable storage |
| Byzantine | Nodes may do anything, including sending false messages | Only for multi-party untrusted environments or high-radiation hardware |

**Recommended default for most server-side data systems:** partially synchronous model + crash-recovery faults.

State the chosen model explicitly in the analysis report. Any algorithm the team adopts (leader election, distributed locking, consensus) must be evaluated against this model.

---

### Step 7 — Produce the failure analysis report

Output a structured report with:

1. **Executive summary** — one paragraph: what failed, root fault category, severity.
2. **Symptom-to-mechanism mapping** — for each symptom: category, mechanism, confidence level.
3. **Anti-patterns found** — code locations (if codebase available), description, risk.
4. **Mitigations** — prioritized list, matched to root cause, with implementation notes.
5. **System model recommendation** — which timing model and node failure model the system should be designed against.
6. **Open questions** — what additional information (logs, metrics, code) would increase diagnostic confidence.

---

## Common Misdiagnoses

These are the mistakes most frequently made when reasoning about distributed failures. Treat each as an active risk to check.

**"The network is reliable inside our datacenter — this must be a software bug."**
Network faults occur inside datacenters. One study found ~12 network faults per month in a medium-sized datacenter, half disconnecting an entire rack. Redundant networking gear does not reduce faults proportionally because human error (misconfiguration) is a primary cause.

**"The timeout fired, so the node must be dead."**
A timeout means you stopped waiting. The remote node may have received your request and processed it, with only the response being lost or delayed. Acting on a false timeout (e.g., promoting a new leader) can create two leaders simultaneously.

**"We use NTP so our clocks are synchronized."**
NTP accuracy is limited by network round-trip time. On a congested network, NTP error can exceed 100ms. VMs are paused by the hypervisor and see their clock jump forward when resumed. Clocks behind a firewall that blocks NTP silently drift. "Synchronized" does not mean "accurate to the millisecond."

**"The node checked its lease and it was valid, so it was safe to proceed."**
A check-then-act sequence is not atomic in a distributed system. A GC pause, VM migration, or OS context switch between the check and the act can make the lease expire. Only server-side enforcement (fencing tokens) provides correctness.

**"Last-write-wins is fine because our timestamps are accurate enough."**
LWW silently discards writes when a node with a lagging clock overwrites values from a node with a fast clock. Clock skew between nodes under 3ms can cause this. The application receives no error. The data is simply gone.

**"The node is dead — it stopped responding."**
The node may be in a stop-the-world GC pause. It will resume, discover that it was declared dead, and attempt to continue its previous role. Without fencing tokens, this zombie behavior can corrupt state.

**"We need Byzantine fault tolerance because we can't trust all nodes."**
In a datacenter where your organization controls all nodes, Byzantine fault tolerance is almost certainly not needed and its cost (algorithmic complexity, performance overhead) is not justified. Standard authentication and checksums handle the realistic "lying" cases.

---

## Examples

### Example 1: Silent data loss in a multi-leader database

**Scenario:** A team runs Cassandra with multi-datacenter replication. After a network partition heals, some writes from one datacenter appear to be silently overwritten or lost. No errors were logged.

**Trigger:** Post-incident investigation after user complaints about missing data. Developer wonders if there is a replication bug.

**Process:**
1. Symptom classification: data loss with no error, after concurrent writes during a partition → Category B (clock unreliability) combined with conflict resolution policy.
2. Mechanism: Cassandra uses last-write-wins by default. During the partition, both datacenters accepted writes to the same key. On reconciliation, the write with the higher timestamp wins. If the losing datacenter's clock was ahead, its writes had higher timestamps and survived — but those writes occurred causally *before* the winning datacenter's writes. The causally later write is silently discarded.
3. Anti-pattern confirmed: timestamp-based conflict resolution with wall-clock time.
4. Mitigation: Replace LWW with application-level conflict resolution using version vectors (CRDTs for counters/sets, explicit merge logic for other data types). If LWW is retained, monitor clock offsets between datacenters and alert when skew exceeds acceptable threshold. Declare nodes with excessive clock drift dead and remove them from the cluster.

**Output:** Failure analysis report identifying LWW + clock skew as root cause. Migration plan to version-vector-based conflict resolution. Alert thresholds for inter-datacenter clock offset monitoring.

---

### Example 2: Zombie leader corrupts shared file storage

**Scenario:** A service uses a ZooKeeper-based distributed lock before writing to shared object storage. Occasionally, two clients write to the same object simultaneously, corrupting it. The team has confirmed the locking code "looks correct."

**Trigger:** Data corruption incident. Developer audits the locking implementation.

**Process:**
1. Symptom classification: two concurrent writers despite a mutual exclusion lock → Category C (process pause) causing zombie lock-holder behavior.
2. Mechanism: Client 1 acquires the lock and begins writing. A stop-the-world GC pause of 18 seconds occurs. The lock expires. Client 2 acquires the lock and begins writing. Client 1 resumes, checks `lease.isValid()`, finds the clock says only milliseconds have elapsed, concludes it still holds the lock, and continues writing. Two writers are now active simultaneously.
3. Anti-pattern confirmed: client-side lease validity check without server-side fencing token enforcement.
4. Mitigation: Implement fencing tokens. ZooKeeper's `zxid` is a suitable fencing token — it is monotonically increasing and returned with each lock grant. Pass the `zxid` with every write to the storage service. The storage service rejects writes with a `zxid` lower than the highest it has seen. Alternatively: use conditional writes (compare-and-swap on an object version field) at the storage layer to detect and reject stale writes.

**Output:** Failure analysis report. Code diff showing where to extract the `zxid` from ZooKeeper and pass it to storage writes. Storage service modification to track and enforce the fencing token.

---

### Example 3: Cascading node-death declarations under load spike

**Scenario:** During a traffic spike, a distributed database cluster declares multiple nodes dead in rapid succession. The cluster degrades severely. When traffic drops, all nodes recover and show healthy, but the cluster has partially lost quorum and requires manual intervention.

**Trigger:** Post-incident review. SRE team wants to understand why nodes were declared dead when they were actually alive.

**Process:**
1. Symptom classification: multiple simultaneous timeout-triggered node-death declarations under load → Category A (network fault) + timeout calibration error.
2. Mechanism: Timeouts were configured at 2 seconds — calibrated for p50 latency. During the load spike, p99 latency jumped to 4–6 seconds due to network congestion and CPU queueing. Health-check RPCs timed out. Nodes were declared dead. Their load was redistributed to remaining nodes, increasing their latency further, causing more timeouts, triggering more declarations — a cascading failure.
3. Anti-pattern: static timeout value calibrated for median, not tail, latency.
4. Mitigation: (a) Recalibrate timeout to p99.9 latency under expected peak load. (b) Add jitter to timeout values to prevent synchronized timeout storms. (c) Implement backpressure: before declaring a node dead, check whether the local node is itself under load (a proxy for network congestion). (d) Consider a Phi Accrual failure detector (used in Akka, Cassandra) that adapts to observed jitter. (e) Tune load shedding to shed excess traffic rather than redistributing it to already-loaded nodes.

**Output:** Failure analysis report. Timeout recalibration recommendation with p99.9 measurement methodology. Configuration changes. Recommendation to evaluate Phi Accrual failure detector.

---

## References

- `references/failure-taxonomy.md` — complete taxonomy: network fault modes, clock error sources, process pause causes, with detection signals and mitigation options
- `references/fencing-token-pattern.md` — fencing token mechanics, ZooKeeper integration, implementation for storage services without native fencing support
- `references/system-models.md` — timing models (synchronous, partially synchronous, asynchronous), node failure models (crash-stop, crash-recovery, Byzantine), safety vs. liveness properties
- `references/clock-pitfalls.md` — NTP accuracy limits, LWW data loss mechanics, clock confidence intervals, Google Spanner TrueTime approach

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-replication-strategy-selector`
- `clawhub install bookforge-consistency-model-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
