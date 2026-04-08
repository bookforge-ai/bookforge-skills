---
name: consistency-model-selector
description: |
  Choose the correct consistency model (linearizability, causal consistency, or eventual consistency) for each operation in a distributed system, and select the matching implementation mechanism. Use when designing a new distributed data system, deciding whether ZooKeeper or etcd is needed for coordination, evaluating whether two-phase commit is appropriate for cross-node transactions, debugging correctness violations (stale reads, split-brain, uniqueness constraint failures), or distinguishing linearizability from serializability. Also use when applying the CAP theorem correctly (beyond the "pick 2 of 3" oversimplification), selecting total order broadcast as a consensus primitive, evaluating 2PC failure modes and lock-holding cost, or assessing whether causal consistency is sufficient in place of linearizability. Produces a per-operation consistency recommendation with replication mechanism, ordering guarantee, and — when consensus is needed — protocol selection (Raft, Zab, Paxos) with documented failure modes. Does not cover replication topology or failure recovery strategy (see replication-strategy-selector, distributed-failure-analyzer).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/consistency-model-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - replication-strategy-selector
  - distributed-failure-analyzer
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [9]
tags:
  - consistency
  - linearizability
  - causal-consistency
  - eventual-consistency
  - consensus
  - total-order-broadcast
  - two-phase-commit
  - cap-theorem
  - zookeeper
  - etcd
  - raft
  - paxos
  - lamport-timestamps
  - distributed-transactions
  - atomic-commit
  - serializability
  - ordering-guarantees
  - leader-election
  - uniqueness-constraints
  - distributed-locks
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application codebase, docker-compose, database config, or architecture description revealing operations and their correctness requirements"
    - type: document
      description: "System requirements document, architecture diagram, or written description of operations if no codebase is available"
  tools-required: [Read, Write]
  tools-optional: [Grep, Bash]
  mcps-required: []
  environment: "Run inside a project directory with codebase or architecture artifacts. Falls back to interactive document/description input."
discovery:
  goal: "Produce a per-operation consistency recommendation: model selection + replication mechanism + ordering guarantee + consensus protocol if needed"
  tasks:
    - "Classify each operation by its consistency requirement"
    - "Select the minimum sufficient consistency model per operation (eventual / causal / linearizable)"
    - "Identify which operations require consensus and match them to the 6-problem checklist"
    - "Select a replication mechanism compatible with the chosen model"
    - "Evaluate 2PC applicability and document failure modes if selected"
    - "Recommend ZooKeeper/etcd for consensus-dependent coordination tasks"
    - "Document the CAP trade-off in force for each linearizable operation"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "site-reliability-engineer", "tech-lead"]
    experience: "intermediate-to-advanced — assumes familiarity with distributed systems, replication, and transactions"
  triggers:
    - "Choosing consistency guarantees for a new distributed data system"
    - "Deciding whether to use ZooKeeper, etcd, or a custom leader election mechanism"
    - "Evaluating whether two-phase commit is appropriate for cross-service transactions"
    - "Debugging stale reads, causality violations, or uniqueness constraint failures"
    - "Assessing whether leaderless replication is strong enough for an operation"
    - "Distinguishing when serializability is sufficient vs. when linearizability is required"
    - "Designing distributed lock or leader election infrastructure"
  not_for:
    - "Selecting isolation levels for single-node transactions — use transaction-isolation-selector"
    - "Diagnosing replication lag and failover failures — use replication-failure-analyzer"
    - "Choosing a replication topology — use replication-strategy-selector"
---

## When to Use

Use this skill when you need to decide **how strongly consistent** a distributed operation must be, and what mechanism enforces that guarantee.

Invoke it for:
- Any operation where two nodes could disagree on the current value (leader election, uniqueness check, account balance enforcement, distributed lock)
- Cross-service or cross-database transactions where atomic commit is required
- Systems where stale reads cause incorrect application behavior (not just stale UI)
- Designing coordination infrastructure (service registry, job scheduler, partition assignment)
- Evaluating whether a Dynamo-style leaderless database is strong enough for a given workload

Do not invoke it for single-node transaction isolation tuning — that is the domain of `transaction-isolation-selector`.

---

## Context and Input Gathering

Before selecting a model, collect the following per operation or component:

1. **Operation type**: read, write, read-modify-write, uniqueness check, lock acquisition, leader election, atomic commit across nodes
2. **Correctness requirement**: Can stale data cause incorrect behavior? Can two nodes diverge temporarily? Is the worst-case outcome data loss, a user-visible error, or a constraint violation?
3. **Availability requirement**: Must this operation succeed during a network partition, or is it acceptable to return an error?
4. **Cross-channel timing dependencies**: Does any other system or user observe an out-of-band signal about the write (e.g., a webhook, message queue, user notification) before reading back?
5. **Replication topology in use**: single-leader, multi-leader, or leaderless (see `replication-strategy-selector`)
6. **Throughput and latency constraints**: Are response times acceptable with a synchronous round-trip to a leader or quorum?

If a codebase is available, search for:
- Database client configuration (isolation level, quorum parameters `w`, `r`, `n`)
- Distributed lock acquisition code
- Uniqueness constraint enforcement logic
- Leader election or service discovery configuration
- Cross-service transaction boundaries

---

## Process

### Step 1 — Identify the Required Guarantee for Each Operation

**WHY**: Different operations have fundamentally different correctness requirements. Over-provisioning consistency wastes latency and availability; under-provisioning introduces bugs that only appear under concurrency or network faults — the hardest class of bugs to detect in testing.

Apply this decision table per operation:

| Scenario | Minimum Required Model |
|---|---|
| Display a user's own recent writes to that same user | Read-your-writes (causal) |
| Show a feed where replies never appear before questions | Causal consistency |
| Enforce a hard uniqueness constraint (username, seat, stock limit) | Linearizability |
| Acquire a distributed lock that prevents split-brain | Linearizability |
| Elect a single leader across nodes | Linearizability (via consensus) |
| Atomically commit a transaction across multiple nodes | Atomic commit (consensus-equivalent) |
| Show analytics dashboard (staleness of seconds acceptable) | Eventual consistency |
| Show a social feed where ordering is approximate | Eventual consistency |
| Replicate writes across datacenters for disaster recovery | Eventual consistency (async replication) |

**Key distinction — linearizability vs. serializability** (commonly confused):
- **Serializability** is an isolation property of *transactions*: multi-object operations behave as if they executed in some serial order. It says nothing about recency.
- **Linearizability** is a recency guarantee on *individual objects*: once a write completes, all subsequent reads see that value — no stale reads from any replica.
- A system can have one without the other. Serializable snapshot isolation (SSI) is explicitly *not* linearizable by design — reads come from a consistent snapshot, which may not include the latest write.
- When you need both: use strict serializability (strong one-copy serializability), implemented by systems that combine 2-phase locking with single-leader replication, or by actual serial execution.

### Step 2 — Select the Minimum Sufficient Consistency Model

**WHY**: Causal consistency is the strongest model that does not slow down under network delays and remains available during network failures. Linearizability is strictly stronger but imposes real latency costs proportional to network uncertainty. Always use the weakest model that is correct.

**Eventual consistency** — use when:
- Staleness is acceptable or expected (analytics, social feeds, DNS lookups)
- High availability during partitions is the primary requirement
- Conflict resolution is application-managed or last-write-wins is acceptable
- Systems: Cassandra (default), Riak, DynamoDB (eventual mode), CouchDB

**Causal consistency** — use when:
- Operations have cause-and-effect ordering that users would notice if violated (reply before question, update before its acknowledgment)
- Multiple communication channels exist (e.g., message queue + file storage), and race conditions between them would cause incorrect behavior
- You need read-your-writes, monotonic reads, and consistent prefix reads across replicas
- Linearizability overhead is too high but eventual is too weak
- Implementation: single-leader replication with reads from leader or synchronously updated follower; causal dependency tracking via version vectors or Lamport timestamps
- Note: causal consistency is not a standard off-the-shelf setting in most databases — it requires careful design of how reads are routed and how dependency information is propagated

**Linearizability** — use when:
- A uniqueness constraint must be enforced as data is written (username, email, seat booking, stock level)
- A distributed lock must be held by exactly one node at a time (split-brain prevention)
- A leader election must produce exactly one agreed-upon leader
- A cross-channel timing dependency exists and cannot be controlled (an external system reads after an out-of-band signal)
- The operation is a compare-and-set that must be atomic across replicas
- Systems: single-leader replication with reads from leader (potentially), consensus algorithms (ZooKeeper, etcd — linearizable writes, quorum reads for linearizable reads), 2-phase locking + single-leader, actual serial execution
- **Not provided by**: multi-leader replication (concurrent writes to different leaders), leaderless/Dynamo-style replication (last-write-wins with clock skew is not linearizable; even strict quorums with variable network delays are not linearizable — see reference)

### Step 3 — Check If the Operation Requires Consensus

**WHY**: Consensus is harder than it looks. Many operations that appear simple are actually reducible to consensus, meaning they require a consensus algorithm to implement correctly in a fault-tolerant way. Identifying this early prevents building brittle custom solutions.

The following 6 problems are all equivalent to consensus — if you need to solve any one of them in a fault-tolerant distributed system, you need a consensus algorithm:

1. **Linearizable compare-and-set registers** — atomically decide whether to set a value based on its current state
2. **Atomic transaction commit** — decide whether to commit or abort a distributed transaction (all nodes must agree)
3. **Total order broadcast** — decide the order in which messages are delivered to all nodes
4. **Distributed locks and leases** — decide which client successfully acquired the lock
5. **Membership/coordination service** — decide which nodes are alive and should be considered current members
6. **Uniqueness constraints** — decide which of concurrent conflicting writes wins

If your operation matches any of the above, evaluate whether to:
- Use an existing consensus service (ZooKeeper, etcd — preferred, see Step 5)
- Use a database that internally implements consensus (VoltDB, CockroachDB, Spanner)
- Implement two-phase commit for atomic cross-node transactions (see Step 4 for failure modes)

### Step 4 — Evaluate Two-Phase Commit (2PC) If Cross-Node Atomic Commit Is Required

**WHY**: 2PC is the standard algorithm for atomic commit across multiple nodes. It solves a real problem but introduces a single point of failure (the coordinator) and can block indefinitely — understanding its failure modes is essential before choosing it.

**How 2PC works**:
1. Coordinator sends `prepare` to all participant nodes
2. Each participant votes `yes` (promises it can commit) or `no` (aborts)
3. If all vote `yes`, coordinator writes commit decision to its log (the commit point), then sends `commit` to all participants
4. If any vote `no`, coordinator sends `abort` to all participants

**The critical failure mode — coordinator crash after prepare**:
- Once a participant has voted `yes`, it cannot unilaterally abort or commit — it must wait for the coordinator's decision
- If the coordinator crashes after receiving `yes` votes but before sending the commit/abort: participants are **in-doubt** and blocked indefinitely
- In-doubt participants hold row-level locks on all modified rows — no other transaction can proceed on those rows
- The only resolution is coordinator recovery (reads its log) or manual administrator intervention
- Orphaned in-doubt transactions (coordinator log lost or corrupted) may hold locks permanently until manual rollback

**2PC failure mode catalog**:

| Failure | Outcome |
|---|---|
| Coordinator crashes before prepare | Safe: participants can abort |
| Participant crashes before voting | Coordinator aborts on timeout |
| Network partitions participant from coordinator | Coordinator aborts on timeout (before commit point) |
| Coordinator crashes after commit point, before all `commit` sent | Remaining participants are in-doubt; blocked until coordinator recovers |
| Coordinator log lost after crash | Orphaned transactions; manual intervention required |
| Long coordinator restart (e.g., 20 minutes) | All participant locks held for that duration; application may be largely unavailable |

**2PC performance cost**: Disk fsyncs at each phase, additional network round-trips, lock-holding during coordination. MySQL distributed transactions reported at 10x slower than single-node.

**When 2PC is appropriate**:
- Database-internal distributed transactions (all nodes run the same software — e.g., VoltDB, MySQL Cluster NDB) — failure modes are more manageable
- Heterogeneous systems that all support XA transactions (PostgreSQL, MySQL, Oracle + JTA-compatible message brokers)

**When to avoid 2PC**:
- High-availability requirements: a coordinator crash can make the application unavailable
- Heterogeneous systems where not all participants support XA or 2PC
- When the coordinator is not replicated (single point of failure for the entire transaction system)
- Stateless application server deployments where coordinator logs can be lost on restart

**Alternatives to 2PC for cross-service correctness**:
- Sagas (compensating transactions) — eventual consistency with explicit rollback logic
- Outbox pattern — atomic local write + reliable event relay (see `distributed-failure-analyzer`)
- Total order broadcast + idempotent consumers — exactly-once processing without 2PC

### Step 5 — Select the Consensus Implementation

**WHY**: Implementing consensus from scratch has a very poor success record. Well-tested consensus systems exist and should be used as building blocks. The key insight is that total order broadcast (the core of Raft, Zab, Paxos) is the practical primitive that enables all 6 consensus-equivalent problems to be solved safely.

**Total order broadcast** (also called atomic broadcast) provides:
- **Reliable delivery**: if a message is delivered to one node, it is delivered to all
- **Totally ordered delivery**: all nodes receive messages in exactly the same order
- This is equivalent to repeated rounds of consensus — and it is what ZooKeeper, etcd, and Kafka (with ZooKeeper or KRaft) implement

**Consensus algorithm selection**:

| Algorithm | Implemented by | Notes |
|---|---|---|
| Raft | etcd, CockroachDB, TiKV, Consul | Well-specified, good documentation, widely adopted |
| Zab | ZooKeeper | Total order broadcast directly; basis of Hadoop/HBase/Kafka coordination |
| Multi-Paxos | Google Chubby, Spanner | Highly proven, complex to implement correctly |
| Viewstamped Replication | Basis for VR-based systems | Theoretically important, less common in production |

**Do not implement your own consensus algorithm.** Use one of the above systems.

**ZooKeeper / etcd as outsourced consensus** — prefer this model when:
- You need distributed locks, leader election, service discovery, or membership tracking
- Your application should not embed consensus logic
- You need the combination: linearizable atomic operations + total ordering + failure detection + change notifications
- Note: ZooKeeper writes are linearizable by default; reads may be stale unless you request a linearizable read (quorum read in etcd, `sync()` call in ZooKeeper)

**Fault-tolerant consensus limitations**:
- Requires a strict majority: tolerate 1 failure → need 3 nodes; tolerate 2 failures → need 5 nodes
- Safety properties (agreement, integrity, validity) are always maintained even if a majority fails
- Liveness (termination) requires fewer than half the nodes to be failed or unreachable
- Performance degrades with high network variance (frequent false leader timeouts trigger leader elections, reducing throughput)
- Fixed membership by default — dynamic membership extensions exist but are less well-understood

### Step 6 — Document the CAP Trade-Off Per Linearizable Operation

**WHY**: CAP is widely misunderstood. The correct framing is: when a network partition occurs, a linearizable system must choose between staying consistent (refusing requests) or becoming available (serving potentially stale data). This is not a design choice you make once — it is a per-operation consequence of requiring linearizability.

**What CAP actually says**:
- If an application *requires* linearizability: when a replica is disconnected from others, it must wait or return an error — it becomes *unavailable*
- If an application *does not require* linearizability: replicas can process requests independently during a partition — it remains *available* but behavior is not linearizable
- The "pick 2 of 3" framing is misleading: network partitions are not optional. A better framing: *either Consistent or Available when Partitioned*
- CAP is narrow in scope — it only addresses linearizability and network partition faults, says nothing about latency, node crashes, or other faults. It has been superseded by more precise results for system design purposes

**Practical consequence**: For each operation you mark as requiring linearizability, document the expected behavior during a partition: error returned, request queued, or application component unavailable. Stakeholders should understand this before the system is deployed.

---

## Examples

### Example 1 — Seat Booking Service

**Scenario**: An event ticketing platform lets users book the last seat in a venue. Two users submit requests concurrently.

**Trigger**: "We're seeing double-bookings in our seat reservation system."

**Process**:
1. Gather: the seat availability check + reservation write is a uniqueness constraint — exactly one booking must win
2. Model selection: linearizability required. Both concurrent reads see availability = 1; without a linearizable compare-and-set, both can commit.
3. Consensus check: uniqueness constraint → problem 6 in the consensus-equivalent list → requires consensus
4. Implementation: use a single-leader database with a serializable transaction (or at minimum a linearizable compare-and-set on the seat record). A Dynamo-style leaderless database with last-write-wins is not safe here.
5. 2PC: only needed if the seat record and the payment record live in different databases. If so, use a saga with compensation (refund) instead of 2PC to avoid coordinator-failure blocking.

**Output**: Linearizability required for the reservation write. Use a single-leader database with serializable isolation for the seat-payment transaction. If cross-database: saga pattern with idempotent payment reversal.

### Example 2 — Multi-Region Comment Feed

**Scenario**: A social platform shows threaded comments. Replies should never appear before the question being replied to. Comments can be up to 2 seconds stale. The system uses multi-leader replication across 3 regions.

**Trigger**: "Users in Asia see replies to questions that haven't appeared yet."

**Process**:
1. Gather: the anomaly is a causal ordering violation — replies appearing before their parent
2. Model selection: causal consistency is sufficient. Linearizability is not required (no uniqueness constraint, no lock, stale display is acceptable within 2 seconds).
3. Multi-leader replication is not causally consistent by default — writes on different leaders can be applied in any order on followers.
4. Options: (a) route all reads and writes for a given thread to a single-leader per partition; (b) propagate causal dependency metadata (version vectors) with writes and delay delivery of writes whose dependencies haven't arrived yet; (c) use a single-leader database and accept the write-latency increase for cross-region authors.
5. Total order broadcast is overkill — causal ordering per thread is sufficient.

**Output**: Causal consistency required for comment ordering. Recommended: single-leader-per-partition with reads from leader. Multi-leader without dependency tracking is not safe for this workload.

### Example 3 — Leader Election for a Job Scheduler

**Scenario**: A distributed job scheduler must have exactly one active scheduler node at a time. If two nodes believe they are the leader, jobs execute twice.

**Trigger**: "We have a split-brain problem — two scheduler instances both claim leadership and jobs are running twice."

**Process**:
1. Gather: leader election is problem 5 in the consensus-equivalent list (membership/coordination) and requires a linearizable lock
2. Model selection: linearizability required. The lock must be held by exactly one node at a time — all nodes must agree who holds it.
3. Consensus check: leader election → consensus required
4. Implementation: use ZooKeeper or etcd for leader election. Acquire an ephemeral node (ZooKeeper) or a lease (etcd). Use fencing tokens (the monotonically increasing `zxid` in ZooKeeper) to prevent a slow previous leader from acting on a stale lock after a new leader is elected.
5. 2PC is not relevant — this is a lock acquisition, not a cross-node transaction.
6. Do not implement with a custom distributed lock using a regular database row — it will not handle coordinator failure correctly.

**Output**: Linearizability required. Use etcd or ZooKeeper for leader election with ephemeral leases and fencing tokens. Never use a custom distributed lock without a consensus-backed service.

---

## References

- [consistency-model-spectrum.md](references/consistency-model-spectrum.md) — Formal definitions of all consistency models with ordering properties
- [linearizability-vs-serializability.md](references/linearizability-vs-serializability.md) — Side-by-side distinction with examples of systems that provide each
- [cap-theorem-analysis.md](references/cap-theorem-analysis.md) — What CAP actually says, its limitations, and how to apply it correctly
- [consensus-equivalence-checklist.md](references/consensus-equivalence-checklist.md) — The 6 consensus-equivalent problems with implementation guidance
- [2pc-failure-modes.md](references/2pc-failure-modes.md) — Complete 2PC failure catalog, in-doubt recovery, XA limitations, alternatives
- [total-order-broadcast-primitives.md](references/total-order-broadcast-primitives.md) — How to build linearizable storage and uniqueness constraints from total order broadcast

Cross-references:
- `replication-strategy-selector` — replication topology must be compatible with the selected consistency model
- `distributed-failure-analyzer` — for failure mode diagnosis when consistency violations appear in production
- `transaction-isolation-selector` — for isolation level selection within a single-node or single-leader transaction context

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-replication-strategy-selector`
- `clawhub install bookforge-distributed-failure-analyzer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
