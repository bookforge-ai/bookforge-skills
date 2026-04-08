---
name: replication-strategy-selector
description: |
  Choose a replication topology (single-leader, multi-leader, or leaderless) and configure it correctly — including sync vs. async mode, quorum parameters (w + r > n), and consistency guarantees. Use when designing replication for a new system, configuring quorum values for Cassandra/Riak/DynamoDB, deciding how to handle multi-leader write conflicts, or comparing PostgreSQL/MySQL streaming replication vs. CouchDB multi-leader vs. Cassandra leaderless for your architecture. Also use for: selecting a conflict resolution strategy (last-write-wins vs. version vectors); designing multi-datacenter replication; choosing between WAL shipping, logical replication, and statement-based replication log formats.
  For diagnosing an existing replication failure (failover gone wrong, lag spike, quorum misconfiguration, split brain), use replication-failure-analyzer instead. For consistency model selection (eventual vs. causal vs. linearizable), use consistency-model-selector instead. For partitioning strategy, use partitioning-strategy-advisor instead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/replication-strategy-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - consistency-model-selector
  - replication-failure-analyzer
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [5]
tags:
  - replication
  - single-leader
  - multi-leader
  - leaderless
  - quorum
  - consistency
  - failover
  - replication-lag
  - read-after-write
  - monotonic-reads
  - consistent-prefix-reads
  - cassandra
  - riak
  - postgresql
  - kafka
  - dynamo
  - conflict-resolution
  - last-write-wins
  - version-vectors
  - split-brain
  - sloppy-quorum
  - hinted-handoff
  - wal-shipping
  - logical-replication
  - multi-datacenter
  - availability
  - durability
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application codebase, docker-compose, database config files, or architecture description that reveals data access patterns and consistency requirements"
    - type: document
      description: "System requirements document or architecture description if no codebase is available"
  tools-required: [Read, Write, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Run inside a project directory with codebase or configuration files. Falls back to document/description input."
discovery:
  goal: "Produce a concrete replication strategy recommendation: topology + sync mode + quorum config + consistency guarantees + conflict resolution"
  tasks:
    - "Classify the system's availability vs. consistency priority"
    - "Select the replication topology (single-leader, multi-leader, leaderless)"
    - "Select synchronous, asynchronous, or semi-synchronous replication mode"
    - "Configure quorum parameters (n, w, r) if leaderless"
    - "Select consistency guarantees required by the application"
    - "Select a conflict resolution strategy if multi-leader or leaderless"
    - "Document failover risks and replication lag anomalies"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "site-reliability-engineer", "tech-lead"]
    experience: "intermediate-to-advanced — assumes experience with distributed systems and databases"
  triggers:
    - "User is choosing between replication strategies for a new database deployment"
    - "User is configuring Cassandra, Riak, or DynamoDB quorum parameters"
    - "User wants to add multi-datacenter replication to an existing system"
    - "User is debugging stale reads, inconsistencies, or read-after-write failures"
    - "User is assessing failover risk in a single-leader setup"
    - "User is evaluating whether to use multi-leader replication for offline or multi-datacenter operation"
    - "User is choosing a conflict resolution strategy for concurrent writes"
  not_for:
    - "Diagnosing replication failures in production — use replication-failure-analyzer"
    - "Selecting consistency and isolation levels for transactions — use consistency-model-selector"
    - "Choosing a partitioning/sharding scheme — use partitioning-strategy-advisor"
---

# Replication Strategy Selector

## When to Use

You are designing or evaluating a data system that replicates data across multiple nodes and need to select a replication topology, configure how data is propagated, and define what consistency guarantees the application requires.

This skill applies when the replication architecture is open (new system), contested (existing system with lag or consistency problems), or needs documented justification (team alignment, architecture decision record). It produces a concrete recommendation covering topology, sync mode, quorum configuration, consistency guarantees, and conflict resolution strategy.

**Prerequisite check:**
- If you need to understand what consistency model (linearizability, causal, eventual) the application requires before selecting a topology, run `consistency-model-selector` first.
- If you are diagnosing an active replication failure or anomaly in production, run `replication-failure-analyzer` instead.
- This skill does not cover partitioning/sharding — if the dataset is too large for a single machine, run `partitioning-strategy-advisor` after this skill.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Availability vs. consistency priority:**
  Why: This is the primary axis. Single-leader replication is the most consistent topology (all writes go through one node, so ordering is defined). Leaderless replication is the most available (writes are accepted even when nodes are down). Multi-leader sits between them but introduces conflict risk. You cannot choose a topology without knowing which trade-off matters more.
  - Check prompt for: "high availability", "must not go down", "consistency is critical", "ACID", "always online", "offline-capable", "multi-region"
  - Check environment for: docker-compose (replication factor configs, consistency-level settings), database config files (sync_commit, consistency_level), requirements.md
  - If still missing, ask: "If a network partition separates some of your database nodes, which is more important: (a) all nodes continue accepting writes even if they may diverge temporarily, or (b) writes are rejected until you can confirm consistency across nodes?"

- **Geographic distribution:**
  Why: Multi-datacenter operation strongly favors multi-leader or leaderless replication. In a single-leader setup with multiple datacenters, all writes must route to the datacenter containing the leader, adding cross-datacenter latency to every write. If users are geographically distributed and write latency matters, multi-leader or leaderless is necessary.
  - Check prompt for: "multi-region", "multiple datacenters", "users in Europe and US", "global", "CDN", "geographic proximity"
  - Check environment for: deployment configs (Kubernetes regions, terraform provider regions), docker-compose (multi-DC labels), architecture.md
  - If still missing, ask: "Are your database nodes in a single datacenter, or are they spread across multiple geographic regions?"

- **Write conflict probability:**
  Why: Multi-leader and leaderless replication can produce write conflicts — two nodes concurrently accepting writes to the same key. If writes to the same record from different clients or regions are likely, conflict resolution must be planned. If conflicts are unlikely (e.g., each user only writes to their own data), multi-leader is more tractable.
  - Check prompt for: "concurrent writes", "multiple clients updating the same record", "collaborative editing", "last-write-wins is fine", "offline sync", "shopping cart"
  - Check environment for: application code (multi-writer patterns), schema (shared mutable records, counters, aggregates)
  - If still missing, ask: "Is it possible for two different clients or datacenters to write to the same record at approximately the same time? For example, two users editing the same document, or two datacenters updating the same account balance?"

- **Read/write ratio and latency requirements:**
  Why: Affects whether asynchronous replication and read scaling are appropriate. Single-leader with many asynchronous followers enables horizontal read scaling. Leaderless quorums let you tune r and w to bias toward read or write performance. If write latency is critical, synchronous replication to all nodes is disqualifying.
  - Check prompt for: throughput numbers, "read-heavy", "write-heavy", latency SLA (ms), "real-time", "user-facing"
  - Check environment for: requirements.md, architecture.md (SLA definitions), application code (read/write ratios)
  - If still missing, ask: "What is the approximate read-to-write ratio and your latency requirement? For example: 90% reads with p99 < 50ms, or mostly writes with best-effort latency?"

### Observable Context (gather from environment)

- **Existing database and replication config:** Look for `docker-compose.yml`, `postgresql.conf` (synchronous_standby_names, wal_level), `cassandra.yaml` (replication_factor, consistency_level), `my.cnf` (binlog_format, rpl_semi_sync_master_enabled). Reveals current topology and whether this is a greenfield or migration decision.
- **Number of replicas/nodes:** Look for replica count configurations. Affects quorum math (n must be odd for majority quorums to work cleanly; n=3 tolerates 1 failure, n=5 tolerates 2).
- **Durability configuration:** Look for fsync settings, WAL configuration, backup policies. Signals how much data loss risk is currently accepted.
- **Application consistency patterns:** Grep codebase for session tokens, user-ID-based routing, "read from primary" comments, timestamp-based staleness checks — signals that the team is already working around replication lag.

### Default Assumptions

- Replication factor unknown → assume n=3 (standard minimum for fault tolerance; tolerates 1 node failure)
- Geographic distribution unknown → assume single-datacenter
- Write conflict probability unknown → assume low (most applications have per-user or per-entity write ownership)
- Latency SLA unknown → assume best-effort; synchronous replication to all replicas is not required

---

## Process

### Step 1: Classify the System Profile

**ACTION:** Determine the system profile across three axes: (a) availability vs. consistency priority, (b) geographic distribution, (c) write conflict probability.

**WHY:** The replication topology selection is determined almost entirely by these three axes. Geographic distribution eliminates single-leader as a low-latency option. High conflict probability makes leaderless difficult to use safely. Strict consistency requirements eliminate fully asynchronous leaderless replication. Getting the profile right prevents the most common mistake: choosing Cassandra (leaderless, eventual) for a system that actually needs read-after-write guarantees, or using single-leader in a multi-datacenter deployment where the cross-datacenter write path adds unacceptable latency.

Produce a one-line profile:

```
Profile: [consistency-priority | availability-priority | balanced]
         [single-datacenter | multi-datacenter]
         [low-conflict | high-conflict | conflict-acceptable]
```

**IF** the user describes offline-first mobile clients → note that multi-leader (or leaderless) is structurally required; each device is effectively a leader.
**IF** the user describes collaborative editing (multiple users editing the same document) → flag that conflict resolution complexity is high; consider whether single-leader with leader-per-document is feasible.

---

### Step 2: Select the Replication Topology

**ACTION:** Choose between single-leader, multi-leader, and leaderless replication based on the Step 1 profile. Apply disqualifying filters first.

**WHY:** Each topology has a different fundamental design: who can accept writes, in what order writes are applied, and what happens when nodes disagree. These are architectural commitments — changing from single-leader to leaderless after data is in production requires schema redesign, operational migration, and application changes. The topology decision must be made with full awareness of what each option cannot do.

**Disqualifying filters:**

| Condition | Disqualifies |
|-----------|-------------|
| Users distributed across 2+ geographic regions AND write latency < 100ms required | Single-leader (all writes must cross datacenter to reach the leader) |
| Strict ACID transactions required across multiple records | Leaderless (no defined write ordering; transactions require coordination layers) |
| Writes must never be lost (zero data loss on failure) | Fully asynchronous single-leader (async follower may lag behind when leader fails) |
| Application cannot tolerate write conflicts (financial transactions, inventory reservation) | Multi-leader and leaderless (concurrent writes to same record may produce conflicts) |
| Clients must work offline and sync later | Single-leader (requires connectivity to the leader for writes) |

**Three-way topology comparison:**

| Dimension | Single-leader | Multi-leader | Leaderless |
|-----------|--------------|-------------|-----------|
| **Write ordering** | Total order (leader serializes all writes) | Partial order (writes within a leader are ordered; cross-leader conflicts possible) | No global order (concurrent writes to same key are possible) |
| **Write availability during leader failure** | Unavailable until failover completes (~30s typical) | Available (other datacenters continue accepting writes) | Available (quorum of remaining nodes accepts writes) |
| **Write latency in multi-datacenter** | High (all writes route to leader's datacenter) | Low (writes go to local datacenter's leader) | Low (writes go to any available replica; quorum locally) |
| **Conflict risk** | None (only one writer) | High (two datacenters can write to same record concurrently) | Medium (concurrent writes possible; quorum overlap reduces risk) |
| **Operational complexity** | Low (well-understood; all major DBs support it) | High (conflict resolution logic required; retrofitted in many DBs) | Medium (quorum config requires care; read repair needed) |
| **Consistency guarantees available** | Read-after-write, monotonic reads, consistent prefix (achievable with techniques) | Eventual at minimum; stronger guarantees require cross-leader coordination | Tunable via quorum config; does not naturally provide the session guarantees above |
| **Representative systems** | PostgreSQL, MySQL, MongoDB (default), Kafka | Tungsten (MySQL), BDR (PostgreSQL), CouchDB, multi-DC Cassandra with multi-leader config | Cassandra, Riak, Voldemort, DynamoDB |

**Selection rules:**

```
IF single-datacenter AND consistency-priority → Single-leader
IF single-datacenter AND availability-priority AND low-conflict → Leaderless
IF multi-datacenter AND write-latency-critical → Multi-leader OR Leaderless
IF offline-clients OR multi-datacenter-availability → Multi-leader
IF high-conflict AND no-conflict-resolution-capacity → Single-leader (simplest)
IF consistency-priority AND ACID-required → Single-leader (only safe choice)
```

**WHY the selection rules are structured this way:** Single-leader is the simplest and most consistent option — there is only one writer, so write ordering is total and conflicts are impossible. The cost is write availability during failover and cross-datacenter write latency. Multi-leader trades conflict risk for write availability across datacenters. Leaderless trades global ordering for the ability to tune availability and consistency independently via quorum parameters. Most systems should default to single-leader unless there is a concrete reason (multi-datacenter write latency, offline operation) that requires one of the more complex options.

**Record the selected topology and the primary disqualifiers applied.**

---

### Step 3: Select Synchronous vs. Asynchronous Replication Mode

**ACTION:** For the selected topology, determine whether replication to followers/replicas should be synchronous, asynchronous, or semi-synchronous.

**WHY:** Synchronous and asynchronous replication represent a direct trade-off between durability and write availability. Synchronous replication guarantees that a write is on at least two nodes before confirming to the client — if the leader fails immediately after acknowledging the write, the data is not lost. Asynchronous replication confirms the write to the client as soon as the leader applies it locally — if the leader fails before replicating, the write is lost even though the client was told it succeeded. This is not a subtle theoretical concern; it is the primary cause of data loss in leader-based database failures.

**For single-leader and multi-leader:**

| Mode | Behavior | When to use |
|------|----------|-------------|
| **Fully synchronous** | All followers must confirm before leader reports success. Write is durable on all nodes. | Never recommended for all followers — any single follower failure blocks all writes. |
| **Semi-synchronous (recommended default)** | One follower is synchronous; all others are asynchronous. If the synchronous follower fails, an async follower is promoted to synchronous. | When you need at least 2 durable copies of every write, while keeping write availability when some followers lag. This is PostgreSQL's `synchronous_commit` behavior. |
| **Fully asynchronous** | Leader confirms immediately; followers catch up in background. Replication lag may be milliseconds to minutes depending on load. | When write throughput is the primary constraint and some data loss on leader failure is acceptable (e.g., log aggregation, analytics events, non-critical telemetry). |

**Configuration implications:**
- PostgreSQL: `synchronous_commit = on` (synchronous to named standby) or `remote_write` (semi-sync). Controlled by `synchronous_standby_names`.
- MySQL: `rpl_semi_sync_master_enabled = 1` enables semi-synchronous. At least one slave must acknowledge before leader reports success.
- Kafka: `acks=all` is synchronous to all in-sync replicas (ISR). `acks=1` is semi-sync (leader only). `acks=0` is fire-and-forget.

**WHY semi-synchronous is the recommended default:** Fully synchronous (all followers) means any follower slowdown or failure stalls all writes — one network blip kills write availability for the entire cluster. Fully asynchronous means leader failure always risks losing writes that were confirmed to the client, which violates most durability expectations. Semi-synchronous gives you at least 2 durable copies (leader + 1 synchronous follower) while keeping write availability when some nodes are slow or down.

**For leaderless:**
Synchronous vs. asynchronous is expressed as quorum configuration (Step 4). Skip to Step 4.

---

### Step 4: Configure Quorum Parameters (Leaderless Only)

**ACTION:** If leaderless replication is selected, determine the values of n (replication factor), w (write quorum), and r (read quorum) using the formula w + r > n.

**WHY:** The quorum formula w + r > n guarantees that at least one node in every read set has seen the most recent write. This is because the w write nodes and r read nodes must overlap by at least one node (by the pigeonhole principle). Without this overlap, a read could hit only stale nodes and return an outdated value without knowing it. Quorum configuration is the primary lever for trading off availability vs. consistency in a leaderless system.

**Common configurations:**

| n | w | r | w+r>n? | Fault tolerance | Bias |
|---|---|---|--------|----------------|------|
| 3 | 2 | 2 | 4>3 ✓ | 1 node failure | Balanced (standard) |
| 3 | 3 | 1 | 4>3 ✓ | 0 for writes | Write-consistent, read-fast |
| 3 | 1 | 3 | 4>3 ✓ | 0 for reads | Write-fast, read-consistent |
| 5 | 3 | 3 | 6>5 ✓ | 2 node failures | Balanced |
| 5 | 5 | 1 | 6>5 ✓ | 0 for writes | Write durable, read-fast |
| 3 | 1 | 1 | 2>3 ✗ | N/A | High availability, stale reads possible |

**Quorum selection rules:**

```
High availability priority → lower w and r (set w+r ≤ n for sloppy quorum behavior)
Read-heavy workload → lower r (r=1 if stale reads acceptable); higher w to keep writes durable
Write-heavy workload → lower w; higher r to compensate for write distribution
Strong consistency needed → w = n or w+r > n strictly (strict quorum)
Multi-datacenter → configure per-datacenter quorum in Cassandra LOCAL_QUORUM
```

**WHY the common default is n=3, w=2, r=2:** This is the minimum configuration that provides both fault tolerance (1 node can fail) and quorum overlap (the 2 write nodes and 2 read nodes must share at least 1 node). Lowering to w=1 or r=1 increases availability but risks returning stale data — the read may miss the node that has the latest write.

**Sloppy quorums and hinted handoff:**
During a network partition that cuts a client off from enough nodes to reach quorum, the database faces a choice: reject all writes (strict quorum) or accept writes on any available nodes even if they are not the designated "home" nodes for a key (sloppy quorum). Sloppy quorums improve write availability during partitions but break the quorum consistency guarantee — a read of r nodes is no longer guaranteed to overlap with the w write nodes. After the partition heals, hinted handoff sends the temporarily-routed writes to their home nodes. Sloppy quorums are appropriate for use cases that can tolerate occasional stale reads (Riak enables by default; Cassandra and Voldemort disable by default).

**WHY sloppy quorums break the consistency guarantee:** With a strict quorum, w + r > n ensures the read and write node sets overlap. With a sloppy quorum, writes may land on "neighbor" nodes not in the normal n-node set. When you read from r nodes in the normal set, those nodes may not include the neighbor nodes that received the write — so w + r > n no longer guarantees overlap. Sloppy quorum is a write-availability mechanism, not a consistency mechanism.

---

### Step 5: Select Consistency Guarantees

**ACTION:** Determine which consistency guarantees the application requires and verify that the selected topology and sync mode can provide them.

**WHY:** Replication lag is not theoretical — in asynchronous systems, followers can lag by milliseconds to minutes. Applications that read from followers without accounting for this lag expose users to anomalies: seeing a write they just made disappear (violating read-after-write), watching data appear to move backward in time (violating monotonic reads), or seeing an answer before the question that caused it (violating consistent prefix reads). Each anomaly requires a specific mitigation technique. Choosing the right mitigation depends on knowing which anomaly is unacceptable for your application's users.

**The three replication lag anomalies and their mitigations:**

**1. Read-after-write consistency (read-your-writes)**
- Anomaly: User submits data, immediately reads it back from a stale follower, sees the old value. Appears to the user as if their write was lost.
- When it matters: Any application where users write and immediately view their own data (profile updates, comment submission, form submission confirmation).
- Mitigations (apply one):
  - Read the user's own data from the leader; read other users' data from followers. (Requires knowing which data the user can have modified.)
  - For one minute after any write, route all that user's reads to the leader (or prevent reads from followers lagging > 1 minute).
  - Track the timestamp of each user's most recent write as a logical timestamp (log sequence number). On read, only serve from replicas that have applied up to that timestamp.
  - For multi-device access (user writes on phone, reads on laptop): centralize the timestamp metadata and route all devices to the same datacenter.

**2. Monotonic reads**
- Anomaly: User makes two successive reads; the second read returns data older than the first (because it hit a more-lagged replica). Data appears to move backward in time.
- When it matters: Any application where users make multiple reads of the same data in a session (social feeds, dashboards, chat messages).
- Mitigation: Route each user's reads to the same replica (e.g., hash the user ID to a replica). If that replica fails, reroute — but accept that the user may briefly see data go backward.

**3. Consistent prefix reads**
- Anomaly: Observer reads writes in a different order than they were written, violating causality. An answer is visible before the question that prompted it.
- When it matters: Any application where the order of writes is semantically meaningful (conversation threads, audit logs, event sourcing, financial transaction history).
- Mitigation: Ensure causally related writes go to the same partition (so they are applied in the same order at all replicas). Alternatively, track causal dependencies with version vectors.

**Consistency guarantee availability by topology:**

| Guarantee | Single-leader | Multi-leader | Leaderless |
|-----------|-------------|-------------|-----------|
| Read-after-write | Achievable (read from leader; timestamp-based routing) | Complex (requires routing to the same leader that processed the write) | Not guaranteed by quorum alone; application must implement timestamp tracking |
| Monotonic reads | Achievable (sticky-session replica routing) | Complex (requires routing to same datacenter that processed the write) | Not guaranteed by quorum; implement user-to-replica affinity |
| Consistent prefix reads | Natural for single-partition data; requires causal tracking for partitioned data | Very hard (cross-datacenter write ordering is not defined) | Not guaranteed; requires version vectors and causal tracking |

**WHY leaderless quorums do not automatically provide session guarantees:** Even with w + r > n, the overlap node is not guaranteed to be the node you actually read from — quorum reads are sent to r nodes, and the freshest value is returned, but if two concurrent writes happened, the "freshest" determination uses version numbers or timestamps that can be unreliable (especially with clock skew). The session guarantees (read-after-write, monotonic reads, consistent prefix) require the application or database to track causal dependencies explicitly — a capability that is present in single-leader systems by construction (because the leader serializes all writes) but must be built explicitly in leaderless systems.

---

### Step 6: Select a Conflict Resolution Strategy (Multi-leader or Leaderless)

**ACTION:** If the topology is multi-leader or leaderless, select a conflict resolution strategy for concurrent writes to the same key.

**WHY:** In multi-leader and leaderless systems, two nodes can concurrently accept writes to the same key. When replication converges, the system must decide what the final value of that key should be. There is no "correct" answer — the right resolution depends on the application semantics. Making this choice explicit now prevents silent data loss from the default strategy (usually last-write-wins, which discards writes) surprising the team later.

**Conflict detection:** Two writes are concurrent if neither operation knew about the other when it was sent. Version vectors track which version each write was based on. If client A's write is based on version v1 and client B's write is also based on v1 (not knowing about A's write), both writes are concurrent — they must be resolved. If B's write is based on v2 (which incorporated A's write), B's write happens-after A's, and the later write wins without conflict.

**Resolution strategies:**

| Strategy | How it works | Data loss? | When to use |
|----------|-------------|-----------|------------|
| **Last write wins (LWW)** | Each write is timestamped; the write with the highest timestamp wins. Other writes are silently discarded. | Yes — concurrent writes are lost | Only when data loss is acceptable (caches, analytics events, idempotent operations). Cassandra's default. |
| **Conflict avoidance** | Route all writes for a given record through the same leader. Conflicts cannot occur if one leader "owns" each record. | No | When write locality is predictable (user X always writes to datacenter A). Breaks down if user location changes. |
| **Merge / union** | Merge all concurrent versions into a combined value. For sets/lists: take the union. | No (but requires tombstones for deletes) | Collaborative data structures (shopping carts, sets, counters). Riak siblings; CRDTs. |
| **Application-level resolution on read** | Store all conflicting versions; return them all to the application on the next read. Application code resolves and writes back the merged value. | No | When only the application has the semantic context to resolve (CouchDB model). Requires application code changes. |
| **Application-level resolution on write** | Conflict handler executes immediately when conflict is detected in the replication log. Must execute quickly (no user prompts). | Depends on handler | When automated resolution is possible (Bucardo for PostgreSQL). |

**WHY LWW is dangerous and widely misused:** LWW requires a reliable total ordering of writes. In distributed systems, clocks cannot be trusted to provide this — two nodes' system clocks can differ by milliseconds or more (see clock skew), meaning a write with an earlier local timestamp may have actually occurred later in causal time. LWW silently discards writes that are reported as successful to the client. The only safe use of LWW is when each key is written exactly once and then treated as immutable — for example, using a UUID as the key so concurrent updates cannot happen.

**WHY conflict avoidance is often the best strategy:** Most multi-leader deployments can be designed so that a given record has a "home" leader — the user's nearest datacenter, for example. If routing ensures that user X always writes to leader A, concurrent writes to the same record from two leaders cannot happen. Conflict avoidance is effectively making multi-leader behave like single-leader on a per-record basis. The limitation is that if the home leader changes (datacenter failure, user relocation), conflicts become possible again.

---

### Step 7: Produce the Recommendation

**ACTION:** Write a structured recommendation document covering all decisions made in Steps 1–6.

**WHY:** A concrete documented recommendation enables team alignment, prevents relitigating the decision, and creates an artifact for the architecture decision record. The "What Can Go Wrong" section is essential — it prevents future surprise when production behavior diverges from the expected replication model.

**Output format:**

Write the following to a file named `replication-strategy-recommendation.md` in the project root (or in `docs/architecture/` if that directory exists):

```markdown
## Replication Strategy Recommendation

### System Profile
[One-line profile from Step 1]

### Recommendation

**Topology:** [Single-leader | Multi-leader | Leaderless]
**Sync Mode:** [Synchronous | Semi-synchronous | Asynchronous | N/A (leaderless)]
**Quorum (if leaderless):** n=[x], w=[x], r=[x] (w+r=[x] > n=[x] ✓)
**Sloppy Quorum:** [Enabled | Disabled | Not applicable]

### Primary Database Products
| Role | Product | Configuration |
|------|---------|--------------|
| [Leader / All replicas] | [PostgreSQL / Cassandra / etc.] | [key config settings] |
| [Follower / Replica] | [as above] | [sync mode setting] |

### Consistency Guarantees Provided
| Guarantee | Provided? | Implementation |
|-----------|----------|----------------|
| Read-after-write | [Yes / No / Application-layer] | [Technique from Step 5] |
| Monotonic reads | [Yes / No / Application-layer] | [Technique from Step 5] |
| Consistent prefix reads | [Yes / No / Application-layer] | [Technique from Step 5] |

### Conflict Resolution (if multi-leader or leaderless)
**Strategy:** [LWW | Conflict avoidance | Merge | Application-level]
**Rationale:** [Why this strategy fits the application semantics]

### Why [Topology]
[2-3 sentences connecting the system profile to the topology choice]

### What We're Giving Up
[1-2 sentences on the primary trade-off and how to mitigate it]

### Disqualifiers Applied
[If any topology was disqualified, state the condition and why]

### What Can Go Wrong
[See "What Can Go Wrong" section below — include the relevant items for this topology]
```

---

## What Can Go Wrong

**Failover data loss (single-leader, async replication).** When an asynchronous leader fails, the new leader is the replica with the most up-to-date data — but "most up-to-date" does not mean "fully up-to-date." Any writes the old leader processed but had not yet replicated are lost when the new leader takes over, even though the client received an acknowledgment. This is the fundamental cost of asynchronous replication. If the old leader later comes back online, it may still have those writes — the system must ensure it discards them and follows the new leader, or data inconsistency results permanently.

**Split brain (single-leader and multi-leader).** In certain network partition scenarios, two nodes can each believe they are the leader. If both accept writes, and there is no mechanism to resolve conflicts, data diverges permanently. The standard defense is fencing: the system shuts down one of the two nodes when it detects two leaders. If the fencing mechanism itself has a bug (or is not implemented), the system can end up with both nodes shut down — a worse outcome than split brain. This is described as "shoot the other node in the head" (STONITH) in the operations literature.

**Replication lag spikes during leader failure or high load.** Asynchronous followers can fall behind by seconds or minutes when the system is under load or recovering from a failure. If the application reads from followers assuming the lag is negligible, users see stale data. The lag can increase to several minutes during follower recovery, maintenance, or network problems. Monitor the replication lag metric on every follower (PostgreSQL: `pg_replication_slots`, `pg_stat_replication`; MySQL: `Seconds_Behind_Master`). Alert when lag exceeds your acceptable staleness threshold.

**Timeout misconfiguration in failover.** Automatic leader election uses a timeout to detect leader failure. If the timeout is too short, a temporarily slow network causes an unnecessary failover — the old leader is still alive but is now competing with the new leader (split brain risk). If the timeout is too long, the cluster is unavailable for writes for longer than necessary after a real failure. There is no universally correct timeout. Start with 30 seconds and calibrate based on observed network behavior. High-load systems should use longer timeouts because response times are naturally higher.

**Old leader rejoining after failover.** When the old leader comes back online after a failover, it may still believe it is the leader — particularly if the old leader was partitioned (slow, not dead). It will try to accept writes. The system must force the old leader to recognize the new leader and demote itself to follower. Without this mechanism, writes go to two nodes simultaneously. This is a known problem in many open-source databases and is a primary reason some operations teams prefer manual failovers even when software supports automatic failover.

**LWW silently discards acknowledged writes.** Last-write-wins conflict resolution is the default in Cassandra and other Dynamo-style databases. If two clients write to the same key concurrently, LWW picks one value and discards the other — even though both clients received a success acknowledgment. The client whose write was discarded has no way to know this happened. For any data where losing a write is unacceptable (financial records, reservations, inventory counts), LWW is a correctness bug, not just a performance trade-off. Use conflict avoidance, application-level resolution, or CRDTs instead.

**Quorum does not guarantee strong consistency.** Even with w + r > n, stale reads can occur in edge cases: (a) if two writes happen concurrently, the ordering between them is not defined and LWW may pick the wrong winner; (b) if a sloppy quorum is enabled, the write nodes and read nodes may not overlap; (c) if a write fails on some replicas but succeeds on others (partial write), and the write is reported as failed to the client but applied to w nodes, subsequent reads may return that "failed" write's value. Quorum is a probabilistic durability guarantee, not a linearizability guarantee. For linearizability, use a consensus protocol (Raft, Paxos — as in etcd, ZooKeeper, CockroachDB).

**Multi-leader conflict resolution logic is hard to get right.** Amazon's early DynamoDB implementation had a conflict resolution handler for shopping carts that merged adds but not removes — items removed from the cart would reappear after a conflict merge. The bug went undetected because conflicts are infrequent and the test suite did not cover the concurrent write case. Conflict resolution code must be explicitly tested with concurrent write scenarios; it cannot be reasoned about by inspecting the code alone. Build a test harness that simulates concurrent writes to the same key before deploying multi-leader.

---

## Key Principles

**Default to single-leader unless there is a concrete requirement for multi-leader or leaderless.** Single-leader replication is the simplest topology — it provides total write ordering, makes consistency guarantees achievable, and is well-supported by every major database. Multi-leader and leaderless replication solve real problems (multi-datacenter write latency, offline operation, high write availability), but they introduce conflict risk and operational complexity that is routinely underestimated. The right default is single-leader with semi-synchronous replication.

**Replication mode is a durability commitment, not a performance setting.** Choosing asynchronous replication to improve write latency means accepting that some acknowledged writes will be lost if the leader fails before replication completes. This is a business and correctness decision, not purely a performance optimization. Make this trade-off explicitly with the team, document it, and build monitoring that alerts when replication lag reaches a level where data loss would be significant.

**The replication lag anomalies (read-after-write, monotonic reads, consistent prefix) are application bugs, not database bugs.** When an application reads from an asynchronous follower and returns stale data to the user, the database is behaving correctly — it told you it uses eventual consistency. The application is the layer responsible for implementing the session guarantees that mask this behavior. Either implement the mitigation techniques in Step 5 or use a database that provides these guarantees at the database layer (PostgreSQL with synchronous_commit, or a database with sessions backed by the leader).

**Quorum configuration is not set-and-forget — it must be re-evaluated as load and node count change.** A system that starts with n=3, w=2, r=2 and later grows to n=5 may have stale quorum configuration. Adding replicas without updating quorum parameters means the quorum overlap guarantee may be weaker or stronger than intended. Revisit quorum configuration whenever the replication factor changes or when the availability vs. consistency balance of the system changes.

**Conflict avoidance is almost always better than conflict resolution.** Every conflict resolution strategy (LWW, merge, application-level) is either lossy, complex, or application-specific. The cleanest approach is to avoid conflicts entirely by routing all writes for a given record through a single leader. If the system allows it, design the data model and routing rules so that conflicts cannot happen — then multi-leader or leaderless replication behaves like single-leader on a per-record basis, with the added benefit of datacenter-local write acceptance for other records.

---

## Examples

**Scenario: Global e-commerce platform with regional datacenters**
Trigger: "We have users in the US, EU, and Asia. Right now all writes go to our US leader. EU and Asia users complain about high write latency. We're considering multi-leader replication."
Process:
- Step 1: Multi-datacenter, write-latency-critical, low-conflict (each user writes to their own orders/cart)
- Step 2: Single-leader disqualified (cross-datacenter write latency). Multi-leader selected. Low conflict probability → conflict avoidance feasible.
- Step 3: Semi-synchronous within each datacenter; asynchronous between datacenters (inter-DC link is less reliable).
- Step 5: Read-after-write: route reads to the user's home datacenter's leader (same datacenter that accepted the write). Monotonic reads: user session pinned to home datacenter.
- Step 6: Conflict avoidance — each user's records are owned by their home datacenter. If home datacenter changes, implement a brief lock during migration.
Output: Multi-leader with one leader per datacenter, semi-sync within datacenter, async cross-datacenter, conflict avoidance via user-to-datacenter affinity. Read-after-write provided by datacenter-local routing.

**Scenario: Real-time leaderboard for a mobile game**
Trigger: "We need a leaderboard that survives node failures without going down. Players' scores update constantly. Occasional stale reads are acceptable — seeing a score a few seconds old is fine."
Process:
- Step 1: Availability-priority, single-datacenter, high-write, stale-reads-acceptable
- Step 2: Single-leader would work but creates write bottleneck for high-frequency score updates. Leaderless selected — high write throughput with tunable availability.
- Step 4: n=3, w=2, r=1. w+r=3, not > n=3. This is intentionally a sloppy configuration for high read availability at the cost of occasional staleness. For scores where exact order matters, increase r=2.
- Step 5: Consistent prefix not required (leaderboard order is eventually consistent by design). Read-after-write not required (seeing a slightly old score is acceptable).
- Step 6: LWW acceptable — score updates are monotonically increasing; overwriting with an older score is unlikely because score writes are always increments, not overwrites. Use version vectors to detect if older value would overwrite newer.
Output: Leaderless (Cassandra), n=3, w=2, r=1. Sloppy quorum enabled for maximum availability. LWW with version tracking. Monitoring alert if replication lag exceeds 5 seconds.

**Scenario: Financial transaction ledger**
Trigger: "We're building an account balance system. Every debit and credit must be consistent. We cannot lose writes. We're using PostgreSQL and considering adding read replicas for reporting."
Process:
- Step 1: Consistency-priority, single-datacenter, write-conflict-unacceptable (double-debit catastrophic)
- Step 2: Multi-leader disqualified (write conflicts are unacceptable; two DCs could both debit the same account). Leaderless disqualified (no strong ordering; quorum does not prevent double-debit). Single-leader selected.
- Step 3: Semi-synchronous. At least one standby must acknowledge before the leader confirms. Fully async is disqualified — data loss on leader failure is not acceptable for financial records.
- Step 5: Read-after-write: all balance reads for the user's own account come from the leader. Reporting queries (dashboards, audit logs) can use async followers with acceptable staleness.
- Step 6: N/A — single-leader, no conflicts possible.
Output: PostgreSQL single-leader, `synchronous_commit = remote_write` (semi-synchronous), one sync standby, multiple async replicas for reporting. All balance reads routed to leader. Replication lag monitoring alert at 10 seconds.

---

## References

For topology-specific deep dives, failure mode details, and quorum calculators, see the references directory:

- For quorum parameter calculations and availability modeling, see [quorum-calculator.md](references/quorum-calculator.md)
- For replication log format comparison (WAL shipping vs. logical/row-based vs. statement-based), see [replication-log-formats.md](references/replication-log-formats.md)
- For conflict resolution strategy comparison and implementation patterns, see [conflict-resolution-strategies.md](references/conflict-resolution-strategies.md)
- For failover procedure and the 3-step leader election process, see [failover-playbook.md](references/failover-playbook.md)
- For replication lag monitoring metrics by database (PostgreSQL, MySQL, Cassandra), see [replication-lag-monitoring.md](references/replication-lag-monitoring.md)
- Cross-reference: `replication-failure-analyzer` — for diagnosing active replication anomalies in production
- Cross-reference: `consistency-model-selector` — for selecting the right consistency model before this skill
- Cross-reference: `partitioning-strategy-advisor` — for sharding strategy after replication topology is decided

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-consistency-model-selector`
- `clawhub install bookforge-replication-failure-analyzer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
