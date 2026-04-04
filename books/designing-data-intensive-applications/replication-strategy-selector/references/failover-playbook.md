# Failover Playbook

Use this reference when planning or executing a leader failover in a single-leader or multi-leader replication setup. Failover is the process of promoting a follower to become the new leader after the current leader fails. It is the most operationally risky event in a leader-based replication system.

## The Three-Step Failover Process

### Step 1: Determine that the leader has failed

There is no foolproof way to detect leader failure. The standard approach is a timeout:
- If the leader does not respond within a configured period (commonly 30 seconds), assume it is dead.
- If it has not responded within that period, initiate failover.

**The timeout calibration problem:**
- Too short (< 10 seconds): A temporary load spike or network hiccup causes false positives. The system performs an unnecessary failover while the leader is still alive — creating split-brain risk.
- Too long (> 60 seconds): The cluster is unavailable for writes for longer than necessary after a real failure.
- Starting point: 30 seconds. Adjust upward if your system operates under sustained high load (response times naturally higher). Adjust downward only after observing false-positive rate in production.

### Step 2: Choose a new leader

**By election:** The remaining replicas vote; the replica with the most up-to-date data is elected. This requires consensus (a notoriously hard distributed systems problem — see Raft, Paxos, Zab in Chapter 9 of DDIA).

**By appointment:** A previously elected controller node (e.g., ZooKeeper) appoints the new leader. The controller is itself a replicated consensus system.

**Heuristic for the best candidate:** The replica that is most up-to-date with the old leader (fewest unreplicated writes) should become the new leader, to minimize data loss.

### Step 3: Reconfigure the system to use the new leader

- All clients must send write requests to the new leader.
- All followers must consume the replication log from the new leader, not the old one.
- If the old leader comes back online, it must recognize the new leader and demote itself to follower. Without this, it may still accept writes as leader — creating split brain.

## Automatic vs. Manual Failover

| | Automatic failover | Manual failover |
|---|---|---|
| Recovery time | ~30s (timeout + election) | Minutes to hours (human response time) |
| Risk | Split brain, premature election, stale leader confusion | Human error during high-stress incident |
| Recommended for | Systems with high availability SLA, well-tested failover path | Systems where the failover code is untested or where human judgment is critical |

**Recommendation:** Use automatic failover with a conservative timeout (30-60 seconds). Test the failover path regularly (chaos engineering — kill the leader in staging, observe behavior). Do not rely on automatic failover as a substitute for testing.

## Failover Pitfalls

### Pitfall 1: Data loss from async replication

When the old leader fails, the new leader is chosen as the most up-to-date replica. But "most up-to-date" does not mean "identical to the old leader." Any writes the old leader applied but had not yet replicated are lost.

**How much data can be lost?** Determined by the replication lag at the moment of failure. With semi-synchronous replication (one synchronous follower), the loss is bounded: the synchronous follower was always up-to-date, so it becomes the new leader with no data loss. With fully asynchronous replication, the lag can be seconds to minutes.

**Mitigation:** Use semi-synchronous replication so at least one follower is always current.

### Pitfall 2: The old leader's unreplicated writes cause conflict when it rejoins

When the old leader comes back online, it has writes that the new leader does not have. The most common solution is to discard those writes — the old leader becomes a follower and its unreplicated writes are thrown away.

**Why discarding is dangerous:** The client received a success acknowledgment for those writes. The database silently breaks the durability guarantee. If those writes were coordinated with other systems (e.g., a Redis counter was incremented based on the DB write), the external system is now inconsistent with the database.

**Example:** At GitHub in 2012, a MySQL follower that was behind the leader was promoted to leader during a failover. The lagging new leader had missed some writes, including auto-incrementing primary keys. Those primary key values had already been used by the old leader's rows (which were stored in a Redis cache). The reuse of primary keys caused data from different users to be returned to the wrong users.

### Pitfall 3: Split brain — two nodes both believe they are the leader

In certain network partition scenarios, the old leader is partitioned from the cluster but not actually dead. The cluster elects a new leader. Now two nodes believe they are the leader and both accept writes.

**Defense — fencing (STONITH):** The system shuts down one node when it detects two leaders. "Shoot The Other Node In The Head" — the node that loses the election is forcibly terminated. 

**The fencing catch:** If the fencing mechanism is improperly designed, it can shut down both nodes. A split-brain situation where both nodes are shut down is worse than a split-brain where both nodes are alive (at least the system is running in the latter case, even if inconsistently). Design fencing carefully and test it explicitly.

### Pitfall 4: Premature failover during load spikes

High system load causes response times to increase. If the leader is under sustained high load, it may not respond to heartbeats within the timeout — even though it is alive and processing writes. This triggers an unnecessary failover.

**Symptoms:** Failovers that happen during high-traffic periods (not hardware failures). Post-failover analysis shows the old leader was still running and had no hardware failure.

**Mitigation:** Increase the timeout during known high-load windows. Monitor the leader's response time trend — if p99 response times are approaching the failover timeout, alert before a failover is triggered. Separate heartbeat traffic from write traffic so write backpressure does not cause heartbeat failures.

## Failover Configuration by Database

### PostgreSQL

- **pg_auto_failover:** Automated failover with a monitor node. Monitor detects primary failure, promotes standby.
- **Patroni:** ZooKeeper or etcd-backed leader election. The current leader must hold a lock; if it cannot renew the lock, it demotes itself.
- **Repmgr:** Simpler failover automation; relies on monitoring script, not consensus.
- Key config: `synchronous_standby_names` (for semi-sync); `wal_level = replica` (for streaming replication).

### MySQL

- **Orchestrator (GitHub):** Detects leader failure, elects most up-to-date replica, reconfigures replication topology automatically.
- **MHA (MySQL High Availability):** Similar to Orchestrator; widely used.
- Key config: `rpl_semi_sync_master_enabled` (semi-synchronous); `GTID_MODE = ON` (for easier failover topology reconfiguration).

### Kafka

- Kafka uses an ISR (In-Sync Replicas) list managed by ZooKeeper (older) or KRaft (newer, built-in consensus). Leader election happens automatically among ISR members.
- Key config: `acks=all` (write must be acknowledged by all ISR replicas before success); `min.insync.replicas` (minimum ISR size for writes to be accepted).

## Post-Failover Checklist

After every failover (automatic or manual), verify:

- [ ] Old leader has fully demoted itself to follower (not accepting writes)
- [ ] All clients are writing to the new leader
- [ ] New leader's replication lag to its followers is decreasing (not growing)
- [ ] Any data loss is documented (how many writes were discarded? Were they coordinated with external systems?)
- [ ] External systems that relied on the old leader's data (caches, search indexes) are invalidated or refreshed
- [ ] The root cause of the failover is identified (hardware failure, network partition, timeout misconfiguration, load spike)
- [ ] The failover timeout setting is re-evaluated based on the root cause
