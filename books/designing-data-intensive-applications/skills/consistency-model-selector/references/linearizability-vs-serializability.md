# Linearizability vs. Serializability

These two terms are among the most commonly confused in distributed systems. They sound similar and both involve ordering, but they are orthogonal guarantees about different things.

## The Core Distinction

| Property | Serializability | Linearizability |
|---|---|---|
| What it applies to | *Transactions* (multi-object operations) | *Individual objects* (single registers/keys) |
| What it guarantees | Transactions behave as if they ran in *some* serial order | Reads always return the most recently written value |
| Recency guarantee? | No — the serial order can differ from real time | Yes — once a write completes, all reads see it |
| Concurrent operations? | Concurrent transactions allowed; conflicts prevented or serialized | No concurrent operations: one global timeline |
| Prevents write skew? | Yes (serializable transactions prevent write skew) | No — write skew requires multi-object transactions |
| Prevents stale reads? | No — serializable reads may come from a snapshot | Yes — no stale reads from any replica |

## Serializability

Serializability is a property of a *transaction execution schedule*. It guarantees that the result of executing a set of concurrent transactions is the same as if they had been executed one at a time, in *some* serial order — but that serial order need not match the wall-clock order in which the transactions actually ran.

**What serializability does NOT prevent**:
- Stale reads from a replica that hasn't received the latest write
- A read seeing data that is "in the past" relative to real time

**What serializability DOES prevent**:
- Write skew (two transactions reading overlapping data and each making a write that is only safe based on what the other hasn't written yet)
- Lost updates, dirty reads (with sufficient isolation level)

**Implementations**:
- Two-phase locking (2PL): serializable, and typically also linearizable for individual objects
- Actual serial execution: serializable, linearizable for individual objects
- Serializable snapshot isolation (SSI): serializable, but **NOT linearizable**

**SSI and non-linearizability**: SSI deliberately reads from a consistent snapshot taken at transaction start. Writes that happen after that snapshot is taken are not visible to the transaction. This means a read within an SSI transaction may not see the latest committed write — this is the definition of non-linearizability.

## Linearizability

Linearizability is a property of a *single-object execution history*. It guarantees that the system behaves as if there is only one copy of the data, and every operation takes effect atomically at a single point in time between its start and completion.

**What linearizability does NOT prevent**:
- Write skew across multiple objects (because it applies per-object, not per-transaction)
- Dirty reads in multi-object transactions (no transaction concept)

**What linearizability DOES prevent**:
- Stale reads: once a write completes, no subsequent read from any client on any replica may return the old value
- Time-travel reads: reads cannot go "backward" in the value sequence

**Implementations**:
- Single-leader with reads from leader: potentially linearizable (depends on implementation)
- Consensus algorithms (Raft, Zab): linearizable writes; linearizable reads require quorum reads or sync()
- Multi-leader, leaderless: NOT linearizable

## Combining Both: Strict Serializability

When a system provides both serializability and linearizability, it is called *strict serializability* or *strong one-copy serializability (strong-1SR)*. This is the strongest practical guarantee:
- Multi-object transactions behave as if executed serially (serializability)
- That serial order is consistent with real time (linearizability)

**Implementations**: 2PL + single-leader replication, actual serial execution on a single leader.

## Decision Guide

Use this to select which guarantee you need:

**Do you need multi-object atomicity (atomic read-modify-write across multiple keys or tables)?**
- Yes → You need serializability (or at minimum, a weaker isolation level that prevents the specific anomaly you care about — see `transaction-isolation-selector`)
- No → Serializability is not needed

**Do you need recency: once a write completes, every subsequent read must see it, from any replica?**
- Yes → You need linearizability
- No → A weaker model (causal or eventual) may suffice

**Combining both needs → strict serializability**. Be aware this has the highest latency and availability cost.

## Practical Examples

| System / Config | Serializable? | Linearizable? |
|---|---|---|
| PostgreSQL with SERIALIZABLE isolation | Yes (SSI) | No (snapshot reads) |
| PostgreSQL with SERIALIZABLE + synchronous replication, reads from leader | Yes | Yes (for single objects) |
| MySQL with 2PL (SERIALIZABLE isolation) | Yes (2PL) | Yes (single objects) |
| Cassandra (default) | No | No |
| ZooKeeper writes | N/A (single-object) | Yes |
| ZooKeeper reads (without sync()) | N/A | No (may be stale) |
| etcd writes | N/A | Yes |
| etcd linearizable reads (default) | N/A | Yes |
| CockroachDB | Yes (SSI variant) | Yes |
| Spanner | Yes | Yes |
