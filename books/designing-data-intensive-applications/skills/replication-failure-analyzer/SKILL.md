---
name: replication-failure-analyzer
description: |
  Diagnose active replication failures by mapping symptoms to leader failover pitfalls, replication lag anomalies, or quorum edge cases — and produce a structured remediation plan. Use when: data just written disappears or shows stale on re-read (read-after-write violation); records appear and vanish on refresh (monotonic reads violation); causally related events appear in impossible order (consistent prefix reads violation); a failover produces duplicate primary keys, write rejections, or incorrect routing; two replica nodes are both accepting writes (split brain in replication topology — for split brain via distributed locking, use distributed-failure-analyzer); quorum reads return stale values despite w + r > n; or a sloppy quorum with incomplete hinted handoff is serving old data. Applies to PostgreSQL, MySQL (single-leader), Cassandra, Riak, Voldemort, DynamoDB (leaderless). Use replication-strategy-selector first if the topology has not yet been chosen. Produces: symptom → failure class → mechanism → mitigation report, leader failover checklist, replication lag anomaly guide, and quorum edge case catalog (six ways w + r > n still fails).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/replication-failure-analyzer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - replication-strategy-selector
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [5]
tags:
  - replication
  - failover
  - split-brain
  - replication-lag
  - read-after-write
  - monotonic-reads
  - consistent-prefix-reads
  - quorum
  - sloppy-quorum
  - hinted-handoff
  - leaderless
  - single-leader
  - cassandra
  - riak
  - postgresql
  - mysql
  - primary-key-conflict
  - data-loss
  - stale-reads
  - anti-entropy
  - version-vectors
  - last-write-wins
  - concurrent-writes
  - failure-analysis
execution:
  tier: 2
  mode: full
  inputs:
    - type: description
      description: "Current replication topology (single-leader, multi-leader, or leaderless), observed symptoms, and whether a failover recently occurred"
    - type: codebase
      description: "Application source code, docker-compose, or database configuration files that reveal quorum settings, read routing, conflict resolution strategy, and primary key generation"
    - type: document
      description: "Incident report, runbook, or architecture description if no codebase is available"
  tools-required: [Read, Write, Grep]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory with codebase or configuration files, or accept a verbal description of the failure. Produces a written replication failure analysis report."
discovery:
  goal: "Produce a structured replication failure analysis report: classify each symptom into its failure class, identify the specific mechanism, and recommend concrete mitigations"
  tasks:
    - "Gather symptom description, replication topology, and recent operational events (failover, partition, node restart)"
    - "Classify each symptom into leader failover failure, replication lag anomaly, or quorum edge case"
    - "Identify the specific mechanism within the class"
    - "Scan configuration and codebase for anti-patterns (timeout values, read routing, quorum parameters, primary key generation)"
    - "Recommend mitigations matched to root cause"
    - "Produce the failure analysis report"
  audience:
    roles: ["backend-engineer", "software-architect", "site-reliability-engineer", "data-engineer", "tech-lead"]
    experience: "intermediate-to-advanced — assumes basic replication familiarity (what a leader is, what a follower is, what a quorum is)"
  triggers:
    - "User's submitted data disappeared or shows stale immediately after a write"
    - "Data appears then vanishes on refresh — time appears to move backward"
    - "Causally related records appear out of causal order (answer before question)"
    - "Failover completed but writes are rejected, misrouted, or creating duplicate key conflicts"
    - "Two nodes are both accepting writes simultaneously"
    - "Quorum reads returning stale values despite w + r > n"
    - "Hinted handoff in progress and fresh reads returning old data"
    - "Infrequently-read keys diverging silently across replicas"
    - "Proactive review of replication config before shipping to production"
  not_for:
    - "Choosing a replication topology — use replication-strategy-selector"
    - "Diagnosing network faults, zombie leaders, or clock unreliability — use distributed-failure-analyzer"
    - "Selecting consistency and isolation guarantees at the transaction level — use consistency-model-selector or transaction-isolation-selector"
---

## When to Use

You have a replication failure in progress or an anomaly you cannot explain. The symptom is one of: data that was written cannot be read back; data that was visible has disappeared; records arrive in causally impossible order; two nodes are writing simultaneously; a quorum read is stale despite the math being correct.

This skill imposes a diagnostic framework: every replication failure traces to one of three classes — **leader failover pitfalls**, **replication lag anomalies**, or **quorum edge cases**. Each class has a bounded set of mechanisms with known mitigations. The skill maps your symptoms to a class, narrows to the mechanism, and produces a remediation plan.

This is the companion to `replication-strategy-selector`. That skill helps you choose. This skill helps you diagnose. Use this one when something is already wrong, or when you want to audit a configuration for latent failure before it manifests.

Cross-references:
- `replication-strategy-selector` — for choosing topology, sync mode, quorum values, and conflict resolution strategy from scratch
- `distributed-failure-analyzer` — for failures whose root cause is a network fault, clock unreliability, or process pause (zombie leaders, LWW data loss via clock skew, cascading timeouts)
- `consistency-model-selector` — for selecting the right consistency and isolation guarantees to prevent a class of anomalies at the application layer

---

## Context and Input Gathering

Before analysis, collect the following. Ask the user for any that are missing.

**Required:**
1. **Symptom description** — what was observed vs. what was expected. Be specific: "a user submitted a comment and immediately reloaded the page but did not see their comment" is better than "stale reads."
2. **Replication topology** — single-leader, multi-leader, or leaderless (Dynamo-style). If leaderless: number of replicas (n), write quorum (w), read quorum (r). If single-leader: synchronous, semi-synchronous, or asynchronous?
3. **Recent operational events** — did a failover happen recently? Was a node restarted? Was there a network partition? Was a follower promoted? Any configuration changes in the past 48 hours?

**Useful:**
4. **Read routing strategy** — do reads go to the leader only, to any replica, or to a specific replica? Is there a load balancer routing reads randomly?
5. **Primary key / ID generation strategy** — autoincrement, UUID, application-generated? Is any external system (cache, secondary store) keyed on these IDs?
6. **Quorum configuration** — for leaderless systems: exact w, r, n values; whether sloppy quorums are enabled; whether an anti-entropy background process is configured.
7. **Replication log metrics** — replication lag in seconds or write offset delta, if available.

**If no codebase or configuration is available:** accept a verbal description and produce an analysis. The report will note which findings are confirmed vs. inferred.

---

## Process

### Step 1 — Classify the failure

WHY: The three failure classes have different root causes and completely different mitigations. Treating a replication lag anomaly as a failover problem (or vice versa) leads to wasted effort and leaves the actual failure in place. Classification first prevents this.

**Class A: Leader failover pitfalls**

Applies to single-leader replication. A failover is the process of promoting a follower to be the new leader when the current leader fails. Automatic failover typically follows three steps: (1) detect the leader has failed via timeout, (2) elect a new leader (usually the most up-to-date replica, chosen by election or by a previously elected controller node), (3) reconfigure clients to route writes to the new leader and ensure the old leader becomes a follower if it recovers.

Failover is "fraught with things that can go wrong." The four documented failure modes are:

| Failure mode | Mechanism | Signal |
|---|---|---|
| **Async data loss** | New leader was an async follower — had not received all writes from old leader before failure. Old leader's unreplicated writes are discarded. | Writes confirmed to client are missing after failover |
| **Primary key conflict** | New leader's autoincrement counter lagged behind old leader's. New leader reissues keys already assigned by the old leader. Any system keyed on these IDs (Redis cache, secondary DB, audit log) develops cross-system inconsistency. | Duplicate key errors or wrong data returned for existing IDs in external systems |
| **Split brain** | Old leader recovers and does not recognize the new leader. Both nodes accept writes simultaneously. Without a process to resolve conflicts, data is lost or corrupted. Some systems "shut down one node if two leaders are detected" — but if this mechanism is misconfigured, both nodes may shut down. | Two nodes both reporting as leader; writes going to both; diverging replica state |
| **Timeout miscalibration** | Timeout too short: unnecessary failovers under load spike or network glitch, making the situation worse. Timeout too long: prolonged unavailability during genuine failures. A temporary load spike can cause response time to exceed the timeout, triggering a failover that increases load further. | Repeated failovers during traffic spikes; or prolonged unavailability before failover triggers |

**Class B: Replication lag anomalies**

Applies to single-leader asynchronous replication with read-scaling (reads routed to followers). The replication lag — the delay between a write being applied on the leader and being reflected on a follower — may be milliseconds under normal conditions, but can grow to seconds or minutes under load or network issues. Three named anomaly patterns arise:

| Anomaly | Description | Mechanism | Named guarantee required |
|---|---|---|---|
| **Read-after-write violation** | User submits data; immediately reads it back; does not see it. From the user's perspective, the submission was lost. | Read was routed to a follower that had not yet received the write. | Read-after-write consistency (also called read-your-writes) |
| **Monotonic reads violation** | User reads data (e.g., a comment); reloads the page; the data is gone. Time appears to move backward. | Sequential reads were routed to different replicas with different lag. The second read went to a more-lagged replica that had not yet received the write the first read saw. | Monotonic reads |
| **Consistent prefix reads violation** | User sees causally related records in an impossible order — an answer appearing before the question it answers. | In a partitioned database where partitions operate independently, partition A (carrying the reply) had low lag and partition B (carrying the question) had high lag. The observer read partition A first. | Consistent prefix reads |

**Class C: Quorum edge cases**

Applies to leaderless (Dynamo-style) replication: Cassandra, Riak, Voldemort, DynamoDB. The quorum condition w + r > n is designed to ensure that at least one node in every read set has seen every acknowledged write. However, six scenarios break this guarantee in practice even when the condition is mathematically satisfied:

| Edge case | Mechanism |
|---|---|
| **Sloppy quorum active** | A network interruption isolated the client from the n "home" nodes for a value. Writes were accepted by w nodes outside the home set (sloppy quorum). Even though w + r > n, the r read nodes are the home nodes — they have not seen the writes yet. Hinted handoff has not completed. |
| **Concurrent writes, no clear ordering** | Two writes to the same key occurred simultaneously. The quorum condition does not determine which write happened first. If last-write-wins is the conflict resolution strategy, the write with the lower timestamp (possibly the causally later write, if clocks are skewed) is silently discarded. |
| **Write concurrent with read** | A write was in-flight when a read was issued. The write was reflected on some of the r replicas but not others. The read may return the old value, the new value, or — in the worst case — the read returns the old value and the write is subsequently applied, but a future read may still return the old value from a different replica subset. |
| **Partial write success, no rollback** | A write succeeded on some replicas but failed on others (e.g., disk full) and was reported as failed overall (fewer than w acknowledgements). The replicas that did succeed are not rolled back. Subsequent reads may or may not see the partially-written value. |
| **Node restored from stale replica** | A node carrying a new value fails and its data is restored from a replica carrying an old value. The number of replicas storing the new value falls below w, breaking the quorum condition retrospectively. |
| **Timing edge cases at linearizability boundary** | Even with w + r > n fully satisfied, quorum reads are not linearizable — there are race conditions where unlucky timing can produce stale reads. Quorums provide eventual consistency, not linearizability. |

---

### Step 2 — Identify the specific mechanism

WHY: The class narrows the diagnostic space; the specific mechanism determines which mitigation is effective. "Replication lag anomaly" does not tell you whether you need sticky routing, a timestamp-based threshold, or causal consistency at the partition level — only identifying the exact anomaly pattern does.

**For Class A (leader failover):**

Confirm which of the four failure modes is active by asking:
- Are writes that were confirmed missing after failover? → Async data loss. Check whether the promoted follower was in synchronous or asynchronous mode with the old leader.
- Are duplicate key errors or cross-system inconsistencies appearing after failover? → Primary key conflict. Check whether the new leader's autoincrement counter was reset or is behind the old leader's. Check for any external systems keyed on the same IDs.
- Are two nodes both accepting writes? → Split brain. Check each node's leader status. Check whether fencing / STONITH (Shoot The Other Node In The Head) is configured and whether it fired correctly.
- Are failovers happening repeatedly or under load? → Timeout miscalibration. Check the configured timeout value against observed p99 latency under load.

**For Class B (replication lag anomalies):**

Confirm which anomaly pattern is active by asking:
- Does the stale read affect only the user who just wrote, immediately after a write? → Read-after-write violation.
- Does a previously visible record disappear on refresh? → Monotonic reads violation.
- Does a reply appear before its question, or an effect appear before its cause? → Consistent prefix reads violation.

For each anomaly, identify whether the read routing layer can be changed (application-level) or whether the database must be configured to provide the guarantee (database-level).

**For Class C (quorum edge cases):**

Confirm which edge case applies:
- Was there a network partition recently? Is hinted handoff in progress? → Sloppy quorum edge case.
- Were concurrent writes made to the same key? Is LWW the conflict resolution strategy? → LWW + concurrent write data loss. Check clock skew between nodes.
- Is the write partially applied (error reported on write, but no rollback)? → Partial write success.
- Was a node recently restored from backup or from a replica? → Stale node restoration.
- Is the failure intermittent under high concurrency? → Timing edge case at linearizability boundary.

---

### Step 3 — Apply the mitigation

WHY: Each mechanism has a specific mitigation. Applying the wrong mitigation (e.g., increasing quorum for a read-after-write problem in a single-leader system) wastes effort and may introduce new problems. This step matches mechanism to fix precisely.

#### Class A mitigations: leader failover

**Async data loss:**
- Short-term: accept that unreplicated writes from the old leader are lost. Inform users; roll back any downstream effects (cache entries, external system records).
- Long-term: configure at least one synchronous follower (semi-synchronous replication). PostgreSQL's `synchronous_standby_names`, MySQL's semi-sync replication. Accept the latency cost on writes. Alternatively: use a consensus-based replication protocol (Group Replication, Galera) where a write is not confirmed until a majority has applied it.

**Primary key conflict:**
- Immediate: reset the new leader's autoincrement counter to a value above the old leader's highest known key. Query the old leader's `AUTO_INCREMENT` status before decommissioning it; if the old leader is unavailable, query all external systems for the highest key they have seen.
- Invalidate or reconcile any external system (Redis, cache, secondary DB) keyed on the affected ID range.
- Long-term: switch to UUIDs or application-generated IDs that are globally unique and do not depend on a per-node counter. This eliminates the class of failure entirely.

**Split brain:**
- Immediate: manually fence the old leader — force it offline, revoke its write permissions at the network or storage layer, or trigger STONITH if configured.
- Reconcile diverged writes: identify writes accepted by both nodes during the split brain window. Resolve conflicts using the conflict resolution strategy appropriate to the data (last-write-wins if losing some writes is acceptable; application-level merge otherwise).
- Long-term: configure a fencing mechanism. Ensure the fencing path is tested periodically. Consider whether a consensus protocol (Raft, Paxos) for leader election would prevent the situation — these protocols guarantee that only one leader is active at a time.

**Timeout miscalibration:**
- Measure round-trip time distribution empirically under peak load. Set the failure-detection timeout at p99 or p99.9 latency plus a safety margin.
- If repeated unnecessary failovers are occurring: increase the timeout. If the timeout is too long and genuine failures are causing excessive unavailability: decrease it — but only after measuring the latency distribution.
- Consider a Phi Accrual failure detector (used in Cassandra, Akka) that adapts its failure threshold based on observed heartbeat jitter, rather than a fixed timeout.
- Some operations teams prefer manual failover even when automatic failover is available, specifically to avoid miscalibrated-timeout failures during load spikes.

#### Class B mitigations: replication lag anomalies

**Read-after-write violation:**

Multiple techniques can implement read-after-write consistency:

1. **Route the user's own data reads to the leader.** For data that only the user themselves can modify (e.g., a user profile), always read from the leader. Read other users' data from followers. This requires knowing, at read time, which data belongs to the current user.

2. **Time-window leader reads.** For one minute (or some configurable interval) after the user's last write, route all that user's reads to the leader. This covers the case where most things in the application are potentially editable by the user.

3. **Client-side write timestamp, replica lag threshold.** The client records the timestamp of its last write (or, better, the replication log position / log sequence number returned by the write). When reading, route to any replica that has advanced past that position. If no such replica is available, either wait or route to the leader.

4. **Cross-device consistency (additional complexity).** If the user accesses your service from multiple devices, the write timestamp must be stored centrally (not just in local storage on the device that made the write). All reads from all of that user's devices must be routed according to that centralized timestamp.

**Monotonic reads violation:**

Ensure that a given user's sequential reads always go to the same replica. The replica can be chosen based on a hash of the user ID rather than randomly. This ensures the user's observed state only moves forward in time.

Caveat: if the assigned replica fails, the user's reads must be rerouted to another replica. At that moment, monotonic reads may be violated for the duration until the new replica catches up. This is generally acceptable — the guarantee is "best effort" in the face of replica failure.

**Consistent prefix reads violation:**

Ensure that writes with causal dependencies are written to the same partition. This prevents the ordering inversion — if the question and answer go to the same partition, the follower will always apply them in the correct order.

If causally related writes cannot always be co-located on the same partition (because the data model makes this impractical): use a database or middleware layer that tracks causal dependencies explicitly (causal consistency via version vectors) and ensures that a read does not return a causally later write without also returning its causal prerequisites.

#### Class C mitigations: quorum edge cases

**Sloppy quorum / hinted handoff in progress:**
- Wait for hinted handoff to complete before serving reads that require up-to-date data. Monitor the hinted handoff queue to determine when it is empty.
- If waiting is not acceptable: disable sloppy quorums (`durable_writes = true` in Cassandra, `allow_offline_hnodes = false` in Riak) to get strict quorum behavior at the cost of lower availability during network partitions.
- Do not treat sloppy quorums as equivalent to strict quorums. They are a durability guarantee only — "w nodes somewhere accepted the write" — not a freshness guarantee.

**LWW + concurrent writes:**
- If data loss is not acceptable: do not use last-write-wins as the conflict resolution strategy. Switch to version vectors (Riak supports these natively as "dotted version vectors") which allow conflicting writes to be detected and merged rather than silently discarded.
- If LWW must be retained: use a UUID as the key so each write operation gets a unique key, making concurrent writes to the same key impossible. This is the recommended Cassandra pattern for LWW safety.
- Monitor clock skew between nodes. Alert when skew exceeds the acceptable data-loss threshold.

**Partial write success:**
- Accept that a reported-failed write may have partially applied. Applications that require strict atomicity across all replicas must use a database with transaction support, not an eventually consistent leaderless store.
- Design operations to be idempotent where possible so they can be safely retried or re-applied during read repair.

**Stale node restoration:**
- Before restoring a node from backup or from another replica, assess how many replicas currently hold the latest value for affected keys. If restoring would drop the count below w, delay the restoration until a full-cluster repair can be run first.
- After restoring a node, run a full repair (Cassandra: `nodetool repair`; Riak: `riak-admin repair`) before routing reads to it.

**Linearizability requirement:**
- If the application genuinely needs linearizable reads (not just eventual consistency), quorums alone are insufficient. Options: (1) route all reads and writes through the single-leader (leaderless systems can designate a read-repair coordinator), (2) use a consensus protocol (Raft, Paxos) which provides linearizability, or (3) upgrade to a database with linearizable transaction support (refer to `transaction-isolation-selector`).

---

### Step 4 — Scan configuration and codebase for anti-patterns

WHY: Latent replication failures exist in configuration and code before they manifest in production. Proactive scanning finds them at low cost. These are the specific patterns to search for.

**Anti-pattern 1: Reads always routed to any random follower**
```
# Look for: round-robin read balancing, random replica selection
# or: load balancer distributing reads across all replicas without session affinity
```
Risk: Read-after-write and monotonic reads violations under any replication lag. Any write may be invisible to a read that lands on a different, more-lagged follower.
Fix: Implement user-session sticky reads or timestamp-gated replica selection.

**Anti-pattern 2: Autoincrement primary keys with asynchronous replication and external systems**
```
# Look for: AUTO_INCREMENT columns, SERIAL columns, sequences
# combined with: external system (Redis, Elasticsearch, audit log) using the same IDs
# combined with: asynchronous replication with manual or automatic failover
```
Risk: After failover, the new leader reissues IDs that were already assigned by the old leader but not yet replicated. The external system retains entries for the old IDs; the new leader's records point to different data.
Fix: Use UUIDs or application-generated globally unique IDs. Or, ensure the autoincrement sequence is advanced past the old leader's maximum before the new leader begins accepting writes.

**Anti-pattern 3: No fencing / STONITH configured for leader failover**
```
# Look for: automatic failover configuration without a fencing mechanism
# e.g., Patroni without fencing, MHA without power fencing, manual failover runbooks
```
Risk: The old leader recovers and does not know it has been demoted. Both nodes accept writes. Split brain.
Fix: Configure a fencing mechanism. Test it periodically. See `distributed-failure-analyzer` for fencing token implementation details.

**Anti-pattern 4: Sloppy quorums enabled in a system requiring read freshness**
```
# Cassandra: read_repair_chance and dclocal_read_repair_chance < 1.0
#             with no anti-entropy (nodetool repair) schedule
# Riak: allow_mult = false (no sibling handling) with sloppy quorums
# Voldemort: default config enables sloppy quorums
```
Risk: During and after network partitions, reads return stale data despite w + r > n being satisfied, because the w writes went to non-home nodes.
Fix: Either disable sloppy quorums (strict quorum mode) or implement application-layer awareness of hinted handoff status.

**Anti-pattern 5: No anti-entropy process, relying solely on read repair**
```
# Cassandra: nodetool repair not scheduled
# Voldemort: no anti-entropy configured
# Custom leaderless system: no background reconciliation
```
Risk: Values that are rarely read will diverge permanently across replicas. Read repair only runs when a value is actually read. Infrequently-read keys can remain stale indefinitely, violating durability guarantees.
Fix: Schedule regular anti-entropy runs. For Cassandra: `nodetool repair` on a weekly schedule (or more frequently for high-write workloads). Ensure the interval is shorter than the gc_grace_seconds (tombstone expiry period) to prevent deleted data from "coming back."

---

### Step 5 — Produce the failure analysis report

Output a structured report with:

1. **Executive summary** — what failed, which failure class, operational impact.
2. **Symptom-to-mechanism mapping** — for each symptom: class, specific mechanism, confidence level (confirmed / inferred / possible).
3. **Immediate remediation** — ordered list of steps to stop the active failure.
4. **Anti-patterns found** — code or configuration locations (if available), description, risk.
5. **Long-term fixes** — architectural changes to prevent recurrence.
6. **Open questions** — what additional information (metrics, config values, code) would increase diagnostic confidence.

---

## Common Misdiagnoses

**"The read is stale — this must be a replication bug."**
Stale reads in asynchronous replication are expected behavior, not a bug. The replication lag is working as designed. The issue is that the application assumed synchronous replication behavior but is running in asynchronous mode. The fix is application-level read routing, not replication reconfiguration.

**"We set w + r > n so our reads must be consistent."**
The quorum condition ensures overlap between write and read node sets under normal conditions. It does not guarantee freshness when: a sloppy quorum was used (writes went to non-home nodes), concurrent writes occurred with LWW resolution and clock skew, or a write partially succeeded. Quorums provide eventual consistency by default, not linearizability.

**"The failover succeeded — why are there duplicate key errors?"**
The promoted follower's autoincrement counter reflects the writes it received before failover. If the old leader had advanced its counter further (on writes not yet replicated), the new leader's counter is behind. When the new leader issues new IDs, it reuses IDs the old leader already assigned. This is especially dangerous when an external system (Redis, Elasticsearch) is keyed on these IDs — the external system retains entries for the old IDs, and the new leader's records now point to different data in the external system.

**"We have two leaders — one of them must be wrong."**
Both leaders may believe they are legitimate. The old leader did not receive the demotion message (it may have been partitioned when the new leader was elected, or the fencing mechanism failed to fire). The solution is not to query which one is "right" but to forcibly fence the old leader and then reconcile the writes it accepted during the split brain window.

**"Monotonic reads just means we need stronger consistency."**
Monotonic reads is a weaker guarantee than strong consistency. It only requires that a single user's reads do not observe an older state after having observed a newer state. It does not require that all users see the same state at the same time. Implementing it with sticky replica routing is significantly cheaper than requiring strong consistency across the cluster.

**"The quorum write failed, so the data wasn't written."**
A failed quorum write means fewer than w nodes acknowledged. But the nodes that did acknowledge are not rolled back. The write may be partially applied across some replicas. Subsequent reads may or may not return the partially-written value, depending on which replicas the read contacts. Applications that retry a failed write without making it idempotent can create inconsistencies.

---

## Examples

### Example 1: GitHub-style primary key conflict after MySQL failover

**Scenario:** A team runs MySQL with a single-leader replication topology. During maintenance, a follower is promoted to leader. Shortly after, users start seeing other users' private data — profile photos and messages belonging to a different account.

**Trigger:** Security incident report. Immediate investigation required.

**Process:**
1. Classify: failover occurred recently + cross-user data leakage → Class A, primary key conflict mechanism.
2. Mechanism: The old leader had issued autoincrement IDs for rows not yet replicated to the promoted follower. The new leader's `AUTO_INCREMENT` counter started below the old leader's maximum. The new leader reissued IDs already assigned by the old leader. A Redis cache was storing user profile data keyed on MySQL row IDs. Redis entries for the old IDs now returned different users' profile data because the new leader's rows with those IDs belong to different users.
3. Immediate remediation: (a) Take the service offline. (b) Query Redis for the highest user ID present. (c) Advance the new leader's `AUTO_INCREMENT` past that value. (d) Invalidate all Redis entries in the affected ID range. (e) Audit which users were served incorrect data and notify them.
4. Long-term fix: (a) Switch to UUID primary keys. (b) Decouple external system keys from database autoincrement IDs. (c) Add a post-failover checklist that explicitly includes advancing the autoincrement counter before opening traffic.

**Output:** Failure analysis report identifying primary key conflict as root cause. Immediate remediation steps. UUID migration plan. Updated failover runbook with autoincrement counter validation step.

---

### Example 2: Read-after-write and monotonic reads violations in a social feed

**Scenario:** A social application uses a single-leader MySQL setup with five followers. Reads are distributed across all followers via a round-robin load balancer. Users regularly report that comments they just posted do not appear when they reload the page. Occasionally, a comment that was visible disappears and then reappears.

**Trigger:** Support ticket volume on "my posts disappear" exceeds threshold. Product team requests investigation.

**Process:**
1. Classify: user's own writes not visible on reload → Class B, read-after-write violation. Comments appearing and disappearing → Class B, monotonic reads violation.
2. Mechanism for read-after-write: Round-robin routing sends the reload request to a different follower than the one that received the previous read (or to any follower, including heavily lagged ones). The follower has not yet received the write.
3. Mechanism for monotonic reads: The first read lands on a follower with low lag (comment visible). The reload lands on a follower with higher lag (comment not yet present). The user observes time moving backward.
4. Mitigation: (a) For the user's own content: route reads to the leader for one minute after any write from that user. Implement by storing `last_write_at` in the user session. After one minute, route to followers. (b) For monotonic reads: hash user ID to always route to the same follower. If that follower fails, reroute — accepting a brief monotonic reads violation during failover. (c) Scan the load balancer configuration to confirm round-robin routing is what is actually configured (vs. session-sticky or latency-aware routing).

**Output:** Failure analysis report. Read routing change specification. Session-layer implementation plan for `last_write_at` tracking. Load balancer reconfiguration recommendation.

---

### Example 3: Stale quorum reads after network partition in Cassandra

**Scenario:** A team runs Cassandra with n=3, w=2, r=2 (satisfying w + r > n). After a 20-minute network partition between two datacenters, quorum reads are returning values that are several minutes old. The partition healed 10 minutes ago.

**Trigger:** Monitoring alert showing read staleness exceeding acceptable threshold after a network event.

**Process:**
1. Classify: quorum reads stale after partition healing, despite w + r > n → Class C, sloppy quorum edge case.
2. Mechanism: During the partition, the datacenter-1 nodes were isolated from the three "home" nodes for affected keys. Cassandra's sloppy quorums (enabled by default in many configurations) allowed writes to be accepted by datacenter-1 nodes that are not in the home node set. After partition healing, hinted handoff is replaying those writes to the home nodes — but the process is not yet complete. Reads contacting the home nodes return the pre-partition values. w + r > n is satisfied in terms of node counts, but the r read nodes are not the same nodes that received the w sloppy-quorum writes.
3. Check: confirm that `nodetool tpstats` shows a non-empty hints queue. Monitor the queue draining rate.
4. Mitigation: (a) Wait for hinted handoff to complete (monitor `HintsService` metrics). (b) For values that must be current: force a read repair by issuing a `CONSISTENCY QUORUM` read or running `nodetool repair` on the affected keyspace. (c) Long-term: evaluate whether sloppy quorums provide acceptable trade-offs for this keyspace. For data requiring freshness guarantees, configure `LOCAL_QUORUM` with `durable_writes = true` and disable sloppy quorums. For data tolerating eventual consistency, sloppy quorums increase availability and are appropriate.

**Output:** Failure analysis report. Hinted handoff monitoring procedure. Decision framework for which keyspaces should use strict vs. sloppy quorums. Updated runbook for post-partition recovery validation.

---

## References

- `references/failover-checklist.md` — step-by-step leader failover checklist: pre-failover verification, the four failure modes and their per-mode checks, post-failover validation steps, and rollback procedure
- `references/lag-anomaly-patterns.md` — complete replication lag anomaly reference: read-after-write, monotonic reads, and consistent prefix reads — each with formal definition, concrete example, implementation techniques, and cross-device complexity considerations
- `references/quorum-edge-cases.md` — the six quorum edge cases in detail: conditions that trigger each, detection signals, mitigation options, and the distinction between sloppy quorums (durability guarantee) and strict quorums (freshness guarantee)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-replication-strategy-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
