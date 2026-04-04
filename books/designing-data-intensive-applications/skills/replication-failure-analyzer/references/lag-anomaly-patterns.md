# Replication Lag Anomaly Patterns

Three named anomaly patterns arise when single-leader asynchronous replication is combined with read-scaling (reads routed to followers). Each has a formal definition, a concrete example, implementation techniques for the mitigation, and additional complexity notes for multi-device scenarios.

---

## Pattern 1: Read-After-Write Violation

**Also known as:** read-your-writes consistency violation.

**Formal definition:** A user makes a write, then issues a read. The read does not reflect the write. The user observes their own submission as "lost."

**Why it happens:** The write goes to the leader. The read is routed to a follower. If the follower has not yet received and applied the write (replication lag is nonzero), the follower returns the pre-write value. The user sees no data.

**Concrete example:** A user edits their profile bio and clicks Save. They reload their profile page. Their new bio is not shown — the old bio is still displayed. From the user's perspective, the edit failed silently.

**Distinguishing characteristic:** The anomaly affects only the user who made the write, and only their own data. Other users' reads are unaffected (they never had the new value, so they are not surprised by its absence).

**Mitigation techniques:**

*Technique 1: Selective leader reads for own data.*
Route reads for data that the user themselves can modify directly to the leader. Route reads for other users' data to followers. This requires knowing at read time which data belongs to the requesting user.
- Example: user profile pages always read the current user's profile from the leader; other users' profiles are read from followers.
- Drawback: if the application is highly personalized and most data is potentially modifiable by the user, most reads must go to the leader, negating the read-scaling benefit.

*Technique 2: Time-window leader reads.*
For a fixed interval after the user's last write (e.g., one minute), route all reads from that user to the leader. After the interval, resume reading from followers.
- Requires storing `last_write_at` per user in session state.
- The interval should be longer than the expected maximum replication lag. If lag occasionally exceeds the interval, violations can still occur — this is a heuristic, not a guarantee.

*Technique 3: Replication position tracking.*
The write returns the replication log position (PostgreSQL: LSN; MySQL: binlog coordinates) at which the write was applied on the leader. The client stores this position. On subsequent reads, route to any follower whose replication position is at or beyond the stored position. If no such follower is available: either wait for one to catch up, or route to the leader.
- This provides a hard guarantee rather than a heuristic.
- Requires the load balancer or client driver to query each follower's current replication position before routing.
- Supported by some drivers: Vitess supports this via `@primary` and position-aware routing. PgBouncer can be configured for this with custom routing logic.

**Cross-device complexity:** If the user submits data on one device (desktop) and reads it on another (mobile), technique 1 and 2 may fail because the `last_write_at` is stored in the desktop session, which the mobile device does not have access to. Centralizing the write timestamp in the user record (database or server-side session store) is required for correct cross-device read-after-write consistency.

---

## Pattern 2: Monotonic Reads Violation

**Formal definition:** A user makes multiple sequential reads. The second read returns a state that is older than the state returned by the first read. Time appears to move backward.

**Why it happens:** Sequential reads from the same user are routed to different replicas (e.g., random or round-robin routing). Replica A has low lag and returns the new value. Replica B has higher lag and has not yet received the write. The second read goes to Replica B and returns the old value.

**Concrete example:** A user refreshes a social media feed. The first refresh shows a comment posted by another user. The second refresh does not show the comment — the second request was routed to a more-lagged replica. The comment appears to have been deleted (but it was never deleted).

**Distinguishing characteristic:** The anomaly manifests as disappearing data on successive reads by the same user. It does not require the user to have made any writes. It is caused entirely by read routing hitting replicas with different lag.

**Mitigation technique:**

*Sticky replica routing:* Route all reads from a given user to the same replica. Choose the replica based on a hash of the user ID (or session ID) rather than randomly. This ensures that as long as the user's reads land on the same replica, the replica's state only moves forward — even if that replica is behind the leader, its local state is monotonically advancing.

```
replica_index = hash(user_id) % number_of_replicas
route_to = replicas[replica_index]
```

**Important caveat:** If the assigned replica fails, the user's reads must be rerouted. At the moment of rerouting, the new replica may be in a different lag state (possibly behind the failed replica's last-seen state). A brief monotonic reads violation is acceptable at this point — the failure case is typically handled by logging in the user out and back in (resetting their read state), or simply accepting the anomaly as a known rare occurrence.

**Interaction with read-after-write:** If sticky routing assigns the user to a follower that has not yet received their own write, a read-after-write violation can occur even with sticky routing in place. Sticky routing solves monotonic reads but does not solve read-after-write. Both mitigations may be needed simultaneously. The read-after-write mitigation (leader reads after a write) overrides sticky routing for the relevant time window.

---

## Pattern 3: Consistent Prefix Reads Violation

**Formal definition:** A user reads a sequence of writes. The writes were causally ordered (write B depends on write A). The user sees write B but not write A — they see the effect before the cause.

**Why it happens:** In a partitioned (sharded) database, different partitions operate independently with no global write ordering. Write A goes to partition 1; write B (which depends on A) goes to partition 2. Partition 2 has low replication lag; partition 1 has high replication lag. The user's read contacts both partitions and sees partition 2's current state (write B present) but partition 1's stale state (write A not yet applied).

**Concrete example (from Kleppmann):** Mr. Poons asks: "How far into the future can you see?" Mrs. Cake replies: "About ten seconds usually." These are written to different partitions. An observer reads Mrs. Cake's reply (partition 2, low lag) before Mr. Poons' question (partition 1, high lag). The observer sees: "About ten seconds usually" followed by "How far into the future can you see?" — the answer precedes the question.

**Distinguishing characteristic:** The anomaly involves causally related writes that are written to different partitions. It is a problem of ordering, not of lag per se — even small lag differences can cause it if partitions diverge for even a moment.

**Mitigation techniques:**

*Technique 1: Causal co-location.*
Ensure that writes with causal dependencies go to the same partition. If the question and answer are always written to the same user's partition, they will always be applied in order by that partition's follower.
- Practical implementation: use a consistent routing key for causally related writes (e.g., a conversation ID, a user ID, an entity ID). All writes for the same conversation go to the same partition.
- Limitation: does not work when causally related writes must span different users' data or different entity types.

*Technique 2: Causal dependency tracking.*
Track causal dependencies explicitly using version vectors or logical clocks. A read does not return a causally later value without also verifying that all its causal prerequisites are present.
- More complex to implement and requires database or middleware support.
- Some databases provide this as a built-in feature (causal consistency in MongoDB, some Cassandra consistency levels).
- References: version vectors (Riak), Lamport timestamps, hybrid logical clocks (CockroachDB).

*Technique 3: Single-partition writes for related data.*
Redesign the data model so that causally related data lives in the same partition by default. For the conversation example: store both the question and answer as records within the same conversation partition, rather than in different user partitions.

---

## Replication Lag Monitoring

Regardless of which anomaly mitigation is implemented, monitoring replication lag is essential:

- **Leader-based replication:** The database exposes per-replica lag metrics. PostgreSQL: `pg_stat_replication.replay_lag`. MySQL: `Seconds_Behind_Master` in `SHOW SLAVE STATUS`. These can be fed into a monitoring system (Prometheus, Datadog, CloudWatch).

- **Leaderless replication:** There is no single leader to compare against. Staleness must be inferred from version numbers or timestamps returned by reads. Some databases expose node-level metrics (Cassandra: `nodetool netstats`, `nodetool tpstats`), but a unified lag figure is not available the same way it is in leader-based systems.

Alert thresholds:
- Warning: lag > 5 seconds (investigate whether the follower is falling behind)
- Critical: lag > 60 seconds (all read-after-write time-window mitigations assume lag is short; long lag makes them unsafe)
- Emergency: lag growing continuously (follower cannot keep up; consider removing it from the read pool)
