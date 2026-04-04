# Leader Failover Checklist

Use this checklist when performing or recovering from a leader failover in a single-leader replication setup (PostgreSQL, MySQL, or any leader-follower topology).

---

## Pre-Failover Verification (Planned Failover)

Before initiating a planned failover (e.g., maintenance, upgrade):

1. **Identify the most up-to-date follower.**
   - Check replication lag for each follower. Choose the one with the smallest lag.
   - Ideal: zero lag (follower is fully caught up). If no follower is at zero lag, accept the one with the lowest lag and document the expected data loss window.
   - PostgreSQL: `SELECT * FROM pg_stat_replication;` (on leader). Check `write_lag`, `flush_lag`, `replay_lag`.
   - MySQL: `SHOW SLAVE STATUS\G` on each follower. Check `Seconds_Behind_Master`.

2. **Check the autoincrement / sequence counter on the old leader.**
   - MySQL: `SHOW TABLE STATUS LIKE 'tablename'` → `Auto_increment` column.
   - PostgreSQL: `SELECT last_value FROM tablename_id_seq;`
   - Record this value. It will be needed to advance the new leader's counter after promotion.

3. **Check for any external systems keyed on primary IDs.**
   - Identify Redis caches, Elasticsearch indices, audit logs, or secondary databases that store records keyed on the same IDs.
   - List them. You will need to reconcile or invalidate these after failover.

4. **Verify fencing mechanism is operational.**
   - Confirm that STONITH (Shoot The Other Node In The Head), power fencing, or network-level fencing is configured and can fire.
   - Test: if this is a staging environment, trigger the fencing mechanism manually to confirm it works before you need it in production.

---

## During Failover

5. **Stop writes to the old leader** (planned failover only).
   - Gracefully drain connections.
   - Wait for replication lag to reach zero on the chosen follower.

6. **Promote the follower.**
   - PostgreSQL: `pg_promote()` or `touch /tmp/postgresql.trigger`.
   - MySQL: `STOP SLAVE; RESET SLAVE ALL;` on the new leader.
   - Patroni, MHA, Orchestrator: use their promotion commands rather than manual promotion.

7. **Reconfigure clients.**
   - Update the write endpoint (connection string, load balancer, service discovery record) to point to the new leader.
   - Existing connections to the old leader will fail. Applications must handle reconnection.

8. **Ensure the old leader becomes a follower** (if it recovers).
   - Configure the old leader to replicate from the new leader when it comes back online.
   - Do not allow the old leader to resume accepting writes.

---

## Post-Failover Validation

9. **Advance the new leader's autoincrement counter.**
   - MySQL: `ALTER TABLE tablename AUTO_INCREMENT = <value above old leader's max>;`
   - PostgreSQL: `SELECT setval('tablename_id_seq', <value above old leader's max>);`
   - WHY: If the old leader had issued IDs that were not replicated, the new leader's counter may be behind the old leader's maximum. The new leader will reissue those IDs, causing conflicts in any external system that has already indexed them.

10. **Reconcile or invalidate external systems.**
    - For each external system identified in step 3: invalidate any cached entries in the ID range between (new leader's starting counter) and (old leader's last known max).
    - If the old leader is available: query it for the exact set of IDs it issued that were not replicated. Compare with the new leader.

11. **Verify write traffic is routing to the new leader only.**
    - Check application logs. Look for write attempts to the old leader's address.
    - Check the old leader's write count metric — it should be zero.

12. **Confirm no split brain.**
    - Verify that the old leader (if it recovered) is in follower mode.
    - Check its replication status — it should be replicating from the new leader, not accepting independent writes.
    - If the old leader is accepting writes: immediately fence it (trigger STONITH or revoke its network write access). Then reconcile diverged writes.

---

## The Four Failure Modes: Quick Reference

| Mode | Signal | Immediate action |
|---|---|---|
| Async data loss | Writes confirmed before failover are missing on new leader | Accept loss; roll back downstream effects; advance autoincrement; notify affected users |
| Primary key conflict | Duplicate key errors in application; cross-user data leakage in external systems | Take service offline; advance autoincrement counter past old leader's max; invalidate external system ID range |
| Split brain | Two nodes both reporting as leader; write divergence | Fence old leader immediately; reconcile diverged writes; audit data integrity |
| Timeout miscalibration | Repeated unnecessary failovers under load; or excessive unavailability before failover fires | Measure p99 latency under load; recalibrate timeout; add load-sensitive trigger guard |

---

## Rollback Procedure

If the failover cannot be completed cleanly (e.g., the promoted follower has corruption or the new leader cannot accept connections):

1. Fence the new leader (prevent it from accepting writes).
2. Restore the old leader to primary status.
3. Re-establish replication from the old leader to all followers.
4. Investigate the root cause before attempting another failover.

Do not attempt a second failover while the first failover's state is unresolved. You can accumulate two concurrent leaders if the fencing from the first failover was not confirmed.
