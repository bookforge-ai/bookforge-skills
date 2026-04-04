# Quorum Edge Cases

The quorum condition w + r > n is designed to guarantee that the read node set and the write node set overlap, ensuring at least one node in every read has the latest value. In practice, six scenarios break this guarantee even when the condition is mathematically satisfied.

Applies to leaderless (Dynamo-style) replication: Cassandra, Riak, Voldemort, DynamoDB, and custom Dynamo-inspired implementations.

---

## The Quorum Baseline

For n replicas:
- Every write must be confirmed by w nodes to be considered successful.
- Every read must query r nodes and return the most recent value seen.
- As long as w + r > n, at least one node in the r-node read set must have seen the w-node write set.

Example: n=3, w=2, r=2. Any two nodes overlap in at least one member. If the write was confirmed by nodes {A, B}, any read contacting {A, C} or {B, C} or {A, B} will include at least one node that has the latest value.

This guarantee holds under the assumptions: strict quorums, no concurrent writes, no partial failures, no node recovery from stale state, and no clock skew in conflict resolution. The six edge cases each violate one of these assumptions.

---

## Edge Case 1: Sloppy Quorum / Hinted Handoff in Progress

**Condition:** A network interruption isolated the client from the n "home" nodes for a key. The database accepted the write on w "non-home" nodes (sloppy quorum) to maintain write availability. After the partition heals, hinted handoff is replaying those writes to the home nodes — but the process is not yet complete.

**Why the guarantee breaks:** The w writes are on non-home nodes. The r reads go to the home nodes. Even though w + r > n is satisfied in terms of counts, there is no overlap between the write set (non-home nodes) and the read set (home nodes) until hinted handoff completes.

**Detection signal:** Recent network partition or node outage. Hinted handoff queue non-empty. Reads returning pre-partition values.

**Mitigation:**
- Wait for hinted handoff to complete before serving reads. Monitor `HintsService` metrics (Cassandra: `nodetool tpstats`; Riak: hints queue length).
- Force read repair: issue a `CONSISTENCY QUORUM` read or run `nodetool repair`.
- Long-term: for keyspaces requiring freshness guarantees, disable sloppy quorums. For Cassandra: set `durable_writes = true`. For Riak: configure per-bucket quorum settings with `pw` (primary write quorum) rather than relying on sloppy handoff.

**Key distinction:** A sloppy quorum is a durability guarantee — "w nodes somewhere in the cluster hold this write." It is not a freshness guarantee. Treating sloppy quorum confirmations as equivalent to strict quorum confirmations is the error.

---

## Edge Case 2: Concurrent Writes with Last-Write-Wins Resolution

**Condition:** Two clients write to the same key at approximately the same time. Last-write-wins (LWW) is the conflict resolution strategy. Clocks between nodes have skew.

**Why the guarantee breaks:** The quorum condition says nothing about which write wins when two writes are concurrent. The only safe solution is to merge concurrent writes (using version vectors or application-level conflict resolution). LWW picks a winner based on timestamp — but timestamps come from node clocks, which have skew. The write with the higher timestamp wins, even if it was causally earlier. The causally later write — which the application intended to be the final value — is silently discarded. No error is reported.

**Detection signal:** Concurrent writes to the same key. LWW conflict resolution enabled (Cassandra default). Clock skew present between nodes. Missing writes with no error in the application.

**Mitigation:**
- Replace LWW with version vectors (Riak: dotted version vectors; custom systems: per-replica version numbers). Version vectors detect concurrent writes and preserve both versions as siblings, allowing application-level or CRDT-based merge.
- If LWW must be retained: use UUIDs as keys so each write has a unique key and concurrent writes to the same key cannot occur. This is the recommended Cassandra pattern for LWW safety.
- Monitor inter-node clock skew. Alert when skew exceeds the acceptable loss threshold (even 3ms skew can cause LWW data loss under high write concurrency).

**Key distinction:** LWW achieves eventual convergence at the cost of durability. All w writes were durably stored; LWW then deliberately discards some of them. This is a design choice, not a quorum failure — but it violates the application's intuition that "confirmed writes survive."

---

## Edge Case 3: Write Concurrent with Read

**Condition:** A write is in-flight when a read is issued. The write has been applied to some replicas but not others. The read contacts r replicas.

**Why the guarantee breaks:** If some of the r replicas have the new value and some have the old value, the read may return either value. If the read takes the old value and the write subsequently completes on all nodes, a later read might return the new value — but another later read (contacting a different replica subset) might still return the old value if that subset did not all receive the write in time. The system is in a transient inconsistent state during the in-flight write window.

**Detection signal:** Very high write concurrency. Intermittent stale reads on keys that are actively being written. Reads sometimes returning new values and sometimes old values non-deterministically.

**Mitigation:**
- For strong consistency requirements: use a consensus protocol (Raft, Paxos) rather than quorums. Consensus protocols serialize reads and writes and provide linearizability.
- For eventual consistency workloads: this edge case is inherent and expected. Ensure the application can tolerate reading either the old or new value during the write window.
- Read repair helps: if a read returns conflicting versions from different replicas, it writes the latest version back to the stale replicas, accelerating convergence.

---

## Edge Case 4: Partial Write Success, No Rollback

**Condition:** A write succeeded on some replicas but failed on others (e.g., a replica's disk is full, or it was temporarily unreachable). The overall write returned an error to the client (fewer than w acknowledgements). The replicas that did succeed are not rolled back.

**Why the guarantee breaks:** The write was reported as failed, so the client may retry it. But the replicas that succeeded already have the new value. On the next read, those replicas may return the partially-written value. The state is now: some replicas at new value, some at old value, and the client does not know which is "correct."

**Detection signal:** Write errors under disk pressure or replica unavailability. Subsequent reads intermittently returning values the client believes were never written.

**Mitigation:**
- Design operations to be idempotent. A safe retry of a partially-applied write must produce the same result as a full write.
- If atomicity across all replicas is required: use a database that provides transactional writes with rollback, not an eventually consistent leaderless store.
- Use conditional writes (compare-and-swap) where available to make partial writes detectable: the write includes a precondition (expected version), and only succeeds if the precondition is met. If the write partially applied, the replicas that got it are at a new version; replicas that did not are at the old version. The next attempt can detect the split by checking versions.

---

## Edge Case 5: Node Restored from Stale Replica

**Condition:** A node that held the latest value for a key fails. Its data is restored from a backup or from another replica that held an older value. After restoration, the number of replicas storing the latest value for that key falls below w.

**Why the guarantee breaks:** The quorum condition was satisfied when the write was made (w nodes confirmed). But the quorum is a snapshot in time — it is not a permanent guarantee. If nodes fail and are restored with stale data, the count of replicas holding the latest value can shrink below w, retroactively breaking the quorum guarantee for that write.

**Detection signal:** Node failure followed by restoration from backup. Reads intermittently returning values that should have been superseded. `nodetool repair` showing large amounts of data being resynchronized.

**Mitigation:**
- Before restoring a node from backup: run `nodetool repair` on the affected keyspace across all remaining healthy replicas first. This ensures the latest values are fully propagated before the restored node's stale data can contaminate reads.
- After restoring a node: do not route reads to it until a repair completes. Mark it as not eligible for read quorum until it has been resynchronized.
- Schedule regular anti-entropy runs (see below) to prevent silent value drift that makes restoration events worse.

---

## Edge Case 6: Timing Edge Cases at the Linearizability Boundary

**Condition:** No specific failure event has occurred. The system is operating normally with w + r > n fully satisfied. Yet under certain timing conditions, a read returns a stale value.

**Why the guarantee breaks:** Quorum reads provide eventual consistency by default — they are not linearizable. Linearizability requires that every read reflects the most recently completed write as of the moment the read is issued. Quorum reads do not guarantee this: the r replicas contacted may all have received the write, but the read request may have been issued before all r replies were collected. There are race conditions where unlucky timing causes stale reads even when the quorum condition is met.

**Detection signal:** Intermittent stale reads under high concurrency with no concurrent writes or node failures. Reads appearing stale by only milliseconds. The anomaly is not reproducible consistently.

**Mitigation:**
- Accept that quorum reads provide eventual consistency, not linearizability. Design the application to tolerate occasional stale reads.
- If linearizability is genuinely required: route reads through a single leader (leaderless systems can designate one replica as the read coordinator for linearizable reads), or use a consensus protocol (Raft, Paxos). Stronger guarantees require transactions or consensus — see `transaction-isolation-selector` and `consistency-model-selector`.

---

## Anti-Entropy: The Missing Piece

All six edge cases are worsened by the absence of an anti-entropy background process.

**Read repair** (the default in most Dynamo-style databases): when a read detects that some replicas returned a stale value, the reading client writes the latest value back to the stale replicas. This only runs when a value is actually read. Infrequently-read keys can diverge permanently.

**Anti-entropy process**: a background process that continuously compares replicas and propagates missing writes. Unlike read repair, it does not depend on reads being issued. Cassandra: `nodetool repair`. Riak: background anti-entropy (enabled by default). Voldemort: does not implement anti-entropy — relies solely on read repair.

**Without anti-entropy:** values that are rarely read may be missing from some replicas indefinitely. This reduces the effective durability below the theoretical guarantee (if only 1 of n replicas has a value for an infrequently-read key, that single replica's failure causes permanent data loss).

**Anti-entropy schedule recommendation:**
- Run `nodetool repair` on a schedule shorter than the gc_grace_seconds period (Cassandra default: 10 days).
- If gc_grace_seconds expires before repair runs, tombstones (deletion markers) are garbage-collected. If a replica that was offline during the original deletion comes back online after tombstone GC, it will "resurrect" the deleted data — deleted rows will reappear.
- Recommended: weekly repair at minimum. Daily repair for high-write workloads or large clusters.

---

## Quick Reference: Quorum Edge Cases

| Edge case | w + r > n satisfied? | Root cause | Mitigation |
|---|---|---|---|
| Sloppy quorum / hinted handoff | Yes (count-wise) | Write and read node sets don't overlap | Wait for hinted handoff; force read repair; consider strict quorums |
| LWW + concurrent writes | Yes | Conflict resolution discards valid writes | Use version vectors; use UUID keys; monitor clock skew |
| Write concurrent with read | Yes | Transient in-flight state | Design for eventual consistency; use consensus for linearizability |
| Partial write, no rollback | No (write failed) | Partial state left on some replicas | Idempotent operations; conditional writes; transactional DB if atomicity needed |
| Stale node restoration | Was yes, now no | Node count with latest value fell below w | Repair before routing reads to restored node; schedule regular anti-entropy |
| Timing at linearizability boundary | Yes | Quorums are not linearizable | Accept eventual consistency; use consensus for linearizable reads |
