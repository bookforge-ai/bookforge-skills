# Replication Lag Monitoring

Use this reference when setting up monitoring for replication lag, or when diagnosing replication lag anomalies. Replication lag is the delay between when a write is applied on the leader and when it is visible on a follower/replica. Unmonitored lag is the primary cause of read-after-write, monotonic reads, and consistent prefix reads violations in production.

## Why Monitoring Lag Is Critical

Replication lag is not constant. In normal operation it may be milliseconds — imperceptible. But during:
- High write load
- Follower recovery after a crash or restart
- Network congestion between leader and follower
- Compaction or heavy disk I/O on the follower

...lag can increase to seconds or minutes. An application that reads from followers without accounting for lag will silently return stale data to users. This is not a theoretical concern — it is a common production incident.

Monitoring must alert before lag reaches the threshold where user-visible anomalies occur.

## PostgreSQL Lag Monitoring

### View current replication state

```sql
-- On the primary: see each standby's lag
SELECT
  client_addr,
  state,
  sent_lsn,
  write_lsn,
  flush_lsn,
  replay_lsn,
  write_lag,
  flush_lag,
  replay_lag,
  sync_state
FROM pg_stat_replication;
```

- `replay_lag`: Time between the primary writing a WAL record and the standby applying it. This is the most meaningful lag metric for data visibility.
- `sync_state`: `sync` (synchronous standby), `async` (asynchronous), `potential` (can become synchronous).

### Check lag from the standby

```sql
-- On the standby: how far behind is this replica?
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;
```

Returns a time interval. Alert if this exceeds your staleness threshold (e.g., 30 seconds for user-facing reads, 5 minutes for analytics).

### Check bytes of lag

```sql
-- On the primary: bytes of WAL not yet replicated
SELECT
  client_addr,
  pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

Large lag in bytes (> 1GB) indicates the replica is significantly behind and may take a long time to catch up even after load normalizes.

### Replication slot lag (prevents WAL recycling)

```sql
-- Check replication slot lag — can prevent WAL cleanup if lag is large
SELECT
  slot_name,
  active,
  restart_lsn,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots;
```

Alert if a replication slot has lag > 10GB — WAL is accumulating and can fill the disk.

### Recommended alerts

| Metric | Warning threshold | Critical threshold |
|--------|------------------|-------------------|
| `replay_lag` (time) | 30 seconds | 5 minutes |
| Lag bytes | 500 MB | 5 GB |
| Replication slot lag bytes | 5 GB | 20 GB |
| `pg_stat_replication` row missing | Immediately | N/A (standby disconnected) |

---

## MySQL Lag Monitoring

### Check lag from the replica

```sql
SHOW REPLICA STATUS\G
```

Key fields:
- `Seconds_Behind_Master`: Approximate lag in seconds. Warning: this metric can be misleading — it shows 0 when the replica SQL thread has caught up but the IO thread is lagging.
- `Replica_IO_Running`: Must be `Yes`. If `No`, the replica cannot receive new writes from the primary.
- `Replica_SQL_Running`: Must be `Yes`. If `No`, the replica is not applying received writes.
- `Last_SQL_Error`: Error message if replica SQL thread stopped. Common cause: a write that succeeded on the primary fails on the replica (schema divergence, constraint violation, duplicate key).

### GTID-based lag (more accurate)

```sql
-- On the primary
SELECT @@global.gtid_executed;

-- On the replica
SELECT @@global.gtid_executed;
-- Compare the two GTID sets to find unapplied transactions
```

GTID (Global Transaction ID) tracking gives a precise count of transactions not yet applied, rather than a time estimate.

### Recommended alerts

| Metric | Warning threshold | Critical threshold |
|--------|------------------|-------------------|
| `Seconds_Behind_Master` | 30 seconds | 5 minutes |
| `Replica_IO_Running` = No | Immediately | N/A |
| `Replica_SQL_Running` = No | Immediately | N/A |
| `Last_SQL_Error` non-empty | Immediately | N/A |

---

## Cassandra Lag Monitoring

Cassandra uses leaderless replication, so there is no single "leader lag" metric. Instead, monitor:

### Repair status

Cassandra's anti-entropy repair process ensures all replicas have all data. If repair is not running regularly, stale data can persist indefinitely on replicas that missed writes.

```bash
nodetool repair --full <keyspace>       # Force a full repair
nodetool compactionstats                # Check compaction backlog
nodetool tpstats                        # Thread pool stats including repair threads
```

Key metrics:
- `AntiEntropyStage` pending tasks: if this grows, repair is not keeping up
- `RepairStage` pending tasks: repair jobs queued but not yet executed

### Hinted handoff

When a node is down and writes are directed to it via hinted handoff, the hints are stored on other nodes. Check hint delivery:

```bash
nodetool tpstats | grep HintedHandoff
```

If hints are accumulating and not being delivered, the target node may not have come back online, or the hinted handoff timeout has expired (hints are discarded after `max_hint_window_in_ms`, default 3 hours).

### Read repair monitoring

Track `ReadRepair` metrics in Cassandra's JMX interface. Low read repair rates in a read-heavy system mean replicas are diverging without correction.

### Recommended alerts

| Metric | Warning threshold | Critical threshold |
|--------|------------------|-------------------|
| AntiEntropyStage pending tasks | > 100 | > 500 |
| HintedHandoffManager active hints | > 10,000 | Growing unbounded |
| Node status (nodetool status) | Any node DN (down) | Multiple nodes DN |
| Dropped messages (nodetool tpstats) | Any | Growing (indicates overload) |

---

## General Monitoring Principles

**Measure actual staleness, not just lag time.** Time-based lag metrics (`Seconds_Behind_Master`) measure when the replica last applied a write, not how stale a specific read is. A replica that hasn't received any writes in the last 10 seconds may show a 10-second lag but is actually fully up-to-date — no writes have happened. For user-facing staleness, track the timestamp of the most recently applied write per key, not just replication lag.

**Set a staleness budget based on your application's guarantees.** If your application provides read-after-write consistency by routing reads to the leader for 1 minute after a write, your lag alert threshold should be much lower than 1 minute — alerting at 30 seconds gives you time to route reads back to the leader before the user notices.

**Monitor the trend, not just the current value.** Lag that is at 10 seconds and growing is more dangerous than lag at 30 seconds and stable. Configure lag rate-of-change alerts in addition to threshold alerts.

**Lag monitoring for leaderless systems requires different approaches.** Without a single replication log, there is no single lag metric. Instead, monitor: (1) anti-entropy repair completion rate, (2) hinted handoff delivery, (3) read repair frequency, and (4) node availability (a node that is down will accumulate lag invisibly until it rejoins).
