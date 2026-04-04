# Consensus Equivalence Checklist

## What Consensus Means

Consensus means getting several nodes to agree on a single value, such that:
- **Uniform agreement**: No two nodes decide differently
- **Integrity**: No node decides twice
- **Validity**: The decided value was proposed by some node (not invented)
- **Termination**: Every non-crashed node eventually decides

The key challenge is termination under faults. 2PC satisfies the first three properties but fails termination (in-doubt participants block indefinitely when the coordinator crashes). True consensus algorithms (Raft, Zab, Paxos) satisfy all four.

## The 6 Consensus-Equivalent Problems

These problems are all reducible to each other. If you can solve one in a fault-tolerant way, you can transform that solution to solve any of the others. All require a consensus algorithm for a correct fault-tolerant implementation.

### 1. Linearizable Compare-and-Set Registers
**Problem**: Atomically read a value, compare it to an expected value, and set it to a new value only if the comparison succeeds — and have all nodes agree on whether the operation succeeded.  
**Why it needs consensus**: The "compare" and "set" must be atomic across replicas. Without consensus, two nodes can each see the old value and both succeed their CAS, producing split state.  
**Implementation**: ZooKeeper's `setData` with version check, etcd's transactional `compare-and-swap`.  
**Practical use**: Username uniqueness, lock acquisition, leader election tokens, optimistic concurrency control.

### 2. Atomic Transaction Commit
**Problem**: A transaction spans multiple nodes. Either all nodes commit, or all abort — no partial commits.  
**Why it needs consensus**: Nodes must agree on the commit/abort decision despite failures. 2PC approximates this but fails the termination property when the coordinator crashes.  
**Implementation**: Two-phase commit (approximate, not full consensus), or database-internal consensus (VoltDB, CockroachDB).  
**Practical use**: Cross-shard transactions, multi-table atomic updates in partitioned databases.

### 3. Total Order Broadcast
**Problem**: All nodes must receive messages in exactly the same order, with no messages lost.  
**Why it needs consensus**: Deciding the position of each message in the total order requires agreement among nodes. A single leader can serialize messages, but choosing that leader — and handling leader failures — requires consensus.  
**Implementation**: ZooKeeper (Zab), etcd (Raft), Kafka (KRaft or ZooKeeper-based).  
**Practical use**: Database replication log, serializable transactions via stored procedures, event sourcing with global ordering.

### 4. Distributed Locks and Leases
**Problem**: Multiple clients race to acquire a lock. Exactly one must succeed. The lock must be released on client failure (leases with expiry).  
**Why it needs consensus**: The decision of "which client holds the lock" must be agreed upon by all nodes. Without consensus, a network partition can cause two clients to each believe they hold the lock (split-brain).  
**Implementation**: ZooKeeper ephemeral nodes, etcd leases. Always use fencing tokens to handle slow lock holders.  
**Practical use**: Single-active-instance patterns (job schedulers, cron, leader-only tasks).

**Fencing token requirement**: A distributed lock is not sufficient on its own. If the lock holder is paused (garbage collection, slow network) after acquiring the lock, it may act on the lock after a new holder has been elected. Fencing tokens — a monotonically increasing number attached to every request that uses the lock — allow the resource being protected to reject stale requests from the previous lock holder. ZooKeeper provides this via `zxid`.

### 5. Membership and Coordination Service
**Problem**: Nodes must agree on which other nodes are currently alive and part of the cluster. A failed node should be removed from membership; a recovered node should be re-admitted.  
**Why it needs consensus**: Without agreement on membership, different nodes have divergent views of the cluster. Operations that depend on "the current member set" (partition assignment, quorum calculation) become inconsistent.  
**Implementation**: ZooKeeper (failure detection via session timeouts + ephemeral nodes), etcd (similar model).  
**Practical use**: Service discovery, partition assignment, quorum determination, failover coordination.

### 6. Uniqueness Constraints
**Problem**: Multiple concurrent operations attempt to create records with the same unique key (same username, same email, same seat). Exactly one must succeed; the rest must fail with a constraint violation.  
**Why it needs consensus**: The decision of "which request won" must be agreed upon by all nodes before any of them responds to the client. Lamport timestamps can define a total order after the fact, but a node receiving a request cannot know in real time whether another node is concurrently processing a conflicting request with a lower timestamp.  
**Implementation**: Single-leader database with a unique index, or a linearizable compare-and-set register (which itself requires consensus).  
**Practical use**: Username registration, email uniqueness, seat booking, inventory reservation.

## Quick Checklist: Do I Need Consensus?

Answer yes to any of the following → consensus is required:

- [ ] Two concurrent operations could both believe they succeeded but only one should
- [ ] I need to enforce a uniqueness constraint as data is written (not just detect violations after the fact)
- [ ] I need a distributed lock that prevents any form of split-brain
- [ ] I need to elect a single leader and all nodes must agree who it is
- [ ] A transaction spans multiple nodes or databases and must be atomic
- [ ] Messages must be delivered to all nodes in the same order for correctness
- [ ] I need to know which nodes are live members of a cluster with agreement

## How to Use the Equivalence

If you already have ZooKeeper or etcd (which implement total order broadcast = consensus):
- You can build all 6 primitives on top of it — linearizable CAS, atomic commit coordination, distributed locks, membership, uniqueness constraints, and message ordering
- You do not need to implement a separate consensus mechanism for each problem

If you do not have a consensus service:
- Do not build your own consensus algorithm (very high failure rate)
- Deploy ZooKeeper or etcd as infrastructure and use it for all consensus-equivalent operations
- Alternatively, use a database that internally implements consensus (CockroachDB, TiKV, Spanner, VoltDB)
