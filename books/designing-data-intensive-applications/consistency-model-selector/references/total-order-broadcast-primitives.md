# Total Order Broadcast as a Practical Consensus Primitive

## What Total Order Broadcast Provides

Total order broadcast (also called atomic broadcast) is a messaging protocol with two safety properties that must hold even during faults:

1. **Reliable delivery**: No messages are lost — if a message is delivered to one node, it is delivered to all nodes
2. **Totally ordered delivery**: Messages are delivered to every node in exactly the same order

These two properties, together, are equivalent to repeated rounds of consensus — each delivery decision is one consensus round. This is why fault-tolerant consensus algorithms (Raft, Zab, Multi-Paxos) implement total order broadcast directly.

## Relationship to Consensus

Total order broadcast and consensus are equivalent in expressive power:
- **Total order broadcast → consensus**: To reach consensus on a value, broadcast it; the first message in the total order is the consensus decision
- **Consensus → total order broadcast**: Use repeated consensus rounds to decide the next message in the sequence

This equivalence means: if you have ZooKeeper or etcd (which implement total order broadcast), you already have consensus, and all 6 consensus-equivalent problems can be solved using it.

## Relationship to Linearizability

Total order broadcast and linearizability are related but not identical:
- Total order broadcast is **asynchronous**: messages are delivered in a fixed order, but there is no guarantee about *when* a message will be delivered (one node may lag behind)
- Linearizability is a **recency guarantee**: a read is guaranteed to return the most recently written value

**From total order broadcast → linearizable storage**:
You can build linearizable read-write storage on top of total order broadcast. Example — linearizable username uniqueness:
1. Append a message to the log: "I want to claim username X"
2. Wait for the message to be delivered back to you (it's now in the global order)
3. Scan all preceding log entries for any claim on username X
4. If your entry is first: claim succeeds. If another claim appears before yours: abort.

This ensures that because all nodes receive log entries in the same order, they will all agree on who claimed the username first. Writes are linearizable by this procedure.

**Making reads linearizable** (choose one):
- Sequence reads through the log: append a read message, perform the read when the message is delivered back (used by etcd quorum reads)
- Fetch the latest log position in a linearizable way, wait for all entries up to that position, then read (ZooKeeper `sync()`)
- Read from a replica that is synchronously updated on every write (chain replication)

**From linearizable storage → total order broadcast**:
If you have a linearizable register with an atomic increment-and-get operation, you can assign monotonically increasing sequence numbers to messages and implement total order broadcast. This is why linearizable sequence number generators inevitably lead to consensus algorithms when you think about fault tolerance.

## Total Order Broadcast as a Replication Log

Total order broadcast is exactly what is needed for database replication:
- Each message represents a write to the database
- Every replica processes the same writes in the same order
- Replicas remain consistent with each other (aside from temporary replication lag)

This principle is called *state machine replication* — if you start from the same initial state and apply the same sequence of deterministic operations, you arrive at the same final state.

**Kafka** uses this model: producers append messages to a partition log; consumers process messages in partition order. Kafka's ordering guarantee is per-partition total order (not global total order across partitions).

**ZooKeeper** uses Zab to implement total order broadcast for its own replication, making ZooKeeper itself a strongly consistent, fault-tolerant data store.

## Building Linearizable Operations from Total Order Broadcast

### Linearizable Compare-and-Set (CAS)
1. Append a CAS proposal to the log: `CAS(key, expected_value, new_value)`
2. Wait for delivery back to yourself
3. Apply all preceding log entries
4. Check if the key's current value matches `expected_value`
5. If yes: apply the CAS (commit it with another log entry or inline in step 4)
6. If no: reject the CAS

All nodes apply the same log in the same order, so all agree on the CAS outcome.

### Atomic Transaction Coordination
Total order broadcast can coordinate the commit/abort decision that 2PC's coordinator holds:
- Broadcast the "prepare" outcome (yes/no votes from all participants) via total order broadcast
- All nodes see the same votes in the same order; all can independently determine the commit/abort outcome
- Eliminates the coordinator as a single point of failure

### Serializable Multi-Object Transactions
If every message represents a deterministic stored procedure, and every node processes those procedures in the same order, the result is serializable multi-object transactions — this is the model used by VoltDB and H-Store (actual serial execution).

## Fault-Tolerant Consensus Algorithm Summary

| Algorithm | Key Systems | Notes |
|---|---|---|
| Raft | etcd, CockroachDB, TiKV, Consul | Well-documented; leader-based; strong safety |
| Zab | ZooKeeper | Total order broadcast natively; basis of Hadoop/Kafka/HBase coordination |
| Multi-Paxos | Google Chubby, Spanner, some Cassandra configs | Highly proven; complex to implement correctly; "nobody really understands Paxos" |
| Viewstamped Replication (VSR) | Research, some production | Theoretically important; similar structure to Raft |

**Epoch numbers and quorums**: All these algorithms use some form of epoch (term, ballot, view) numbering. Each epoch has a unique leader. If a conflict arises between leaders from different epochs, the higher epoch wins. Leaders must collect a quorum of votes before making a decision, and the quorum for leader election must overlap with the quorum for proposals — ensuring that any new leader knows about all committed decisions from previous epochs.

**Key difference from 2PC**: Fault-tolerant consensus requires votes from a *majority* of nodes. 2PC requires a `yes` from *every* participant. This means:
- A single slow or failed participant can block 2PC indefinitely
- A minority of failures does not block Raft/Zab/Paxos

## When to Use ZooKeeper / etcd vs. Database-Internal Consensus

**Use ZooKeeper or etcd** for:
- Distributed locks and leases (with fencing tokens)
- Leader election for application components
- Service discovery and membership tracking
- Configuration that must be consistent across all nodes
- Partition assignment coordination (Kafka, HBase, YARN)

**Use database-internal consensus** (CockroachDB, Spanner, TiKV) for:
- Linearizable data storage at scale
- Cross-shard transactions with linearizability
- When you want the database to handle consensus transparently

**Do not use** ZooKeeper/etcd for:
- High-throughput application data storage — it is designed for small, slow-changing coordination data
- Per-request state — the overhead of consensus is not worth it for data that can be eventually consistent
