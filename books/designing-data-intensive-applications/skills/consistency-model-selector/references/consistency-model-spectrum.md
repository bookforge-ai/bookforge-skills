# Consistency Model Spectrum

Consistency models form a hierarchy from weakest to strongest. Stronger models are easier to reason about but impose higher latency and availability costs.

## The Spectrum (Weakest to Strongest)

```
Eventual Consistency
      |
  Causal Consistency          ← strongest model with no network-delay slowdown
      |
  Sequential Consistency
      |
  Linearizability             ← strongest common model; recency guarantee
      |
  Strict Serializability      ← linearizability + serializability combined
```

## Definitions

### Eventual Consistency (Convergence)
**Guarantee**: If you stop writing, all replicas will eventually converge to the same value.  
**What it does NOT guarantee**: When convergence happens. Until convergence, reads may return anything — including stale values, missing values, or different values from different replicas.  
**Ordering**: None. Operations are not ordered relative to each other.  
**Examples**: Cassandra (default), Riak, DynamoDB (eventual mode), CouchDB, DNS.  
**Best for**: High-availability workloads where staleness is acceptable.

### Causal Consistency
**Guarantee**: Operations that are causally related (cause → effect) are seen in that order by all nodes. Operations with no causal relationship may be seen in any order (they are concurrent).  
**Ordering**: Partial order. Causal dependencies define a directed acyclic graph; concurrent operations are incomparable.  
**Key property**: Causal consistency is the *strongest* model that does not slow down due to network delays and remains available during network failures. CAP theorem does not apply to causal consistency.  
**Subsumes**: Read-your-writes, monotonic reads, consistent prefix reads.  
**Implementation**: Version vectors (per-key causal tracking), Lamport timestamps (total order consistent with causality), or single-leader replication with reads from the leader.  
**Examples**: Snapshot isolation provides causal consistency. COPS, Eiger, Occult (research systems).

### Sequential Consistency
**Guarantee**: All nodes see operations in the same total order, and that order is consistent with the program order on each individual node.  
**What it does NOT guarantee**: That the total order reflects real time. A write may be "seen" after a long delay, but once seen, it appears to have happened at a consistent point relative to other operations.  
**Note**: Less common in distributed databases; more common in CPU memory models.

### Linearizability (Atomic Consistency, Strong Consistency, Immediate Consistency, External Consistency)
**Guarantee**: The system behaves as if there is a single copy of the data, and all operations are atomic. Once a write completes, all subsequent reads — from any replica — see that write. This is a *recency guarantee*.  
**Ordering**: Total order. There is one global timeline; no operation is concurrent with another in the observable history.  
**Key property**: After any one read returns a new value, all following reads (on the same or any other client) must also return the new value.  
**Cost**: Response time is proportional to the uncertainty of network delays — linearizability is inherently slow in high-latency networks.  
**Examples**: ZooKeeper (writes), etcd (writes + linearizable reads), single-leader replication with reads from leader (potentially), Spanner, CockroachDB.

### Strict Serializability (Strong One-Copy Serializability)
**Guarantee**: Transactions behave as if they executed serially on a single copy of the data, AND that serial order is consistent with real time (linearizable).  
**Implementation**: Two-phase locking (2PL) + single-leader replication, or actual serial execution.  
**Examples**: FaunaDB, older VoltDB configurations.  
**Note**: Serializable snapshot isolation (SSI) is serializable but NOT linearizable — reads come from a snapshot that may not include the most recent writes.

## Ordering Properties Compared

| Model | Total Order? | Recency Guarantee? | Available During Partition? | Network-delay-free? |
|---|---|---|---|---|
| Eventual | No | No | Yes | Yes |
| Causal | Partial | No | Yes | Yes |
| Sequential | Total (program-order-consistent) | No | No | No |
| Linearizable | Total (real-time-consistent) | Yes | No | No |
| Strict Serializable | Total (real-time-consistent, multi-object) | Yes | No | No |

## Replication Method Compatibility

| Replication Method | Linearizable? | Notes |
|---|---|---|
| Single-leader, reads from leader | Potentially | Not every single-leader DB is linearizable; snapshot isolation breaks it |
| Single-leader, reads from follower | No | Followers may lag |
| Consensus algorithm (Raft/Zab) | Yes | This is how ZooKeeper/etcd achieve it |
| Multi-leader | No | Concurrent writes to different leaders; conflicts must be resolved |
| Leaderless (Dynamo-style) | Probably not | Quorums with variable network delays are not linearizable; LWW with clock skew is definitely not |
| Leaderless with synchronous read repair | Possible for reads/writes, not CAS | Cassandra does not do this by default; CAS requires consensus |
