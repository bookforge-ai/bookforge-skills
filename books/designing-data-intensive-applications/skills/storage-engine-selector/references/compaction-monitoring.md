# Compaction Monitoring Reference

This reference provides operational guidance for monitoring and managing compaction in LSM-tree storage engines. Read this when LSM-tree is selected as the storage engine and you need to define production alerting, tune compaction, or diagnose a compaction problem.

---

## Why Compaction Monitoring Is Non-Optional

LSM-tree engines (Cassandra, RocksDB, LevelDB, HBase) do not throttle incoming writes when compaction falls behind. If write throughput exceeds the compaction thread's capacity to merge SSTable files:

1. **SSTable file count grows** — each uncompacted write creates or expands an SSTable file
2. **Read performance degrades** — each read must check more SSTable files (more Bloom filter checks, more potential disk reads)
3. **Disk space grows unboundedly** — old versions of keys accumulate in uncompacted SSTables; space is not reclaimed
4. **Eventually: disk full** — the system stops accepting writes or crashes

This failure mode is insidious because it degrades gradually. A workload that ran fine for months can suddenly become critical as data volume crosses a threshold.

**Rule:** When selecting an LSM-tree engine, define compaction monitoring before the system goes to production.

---

## Cassandra Compaction Metrics

### Key metrics (via `nodetool`)

```bash
# Show pending compaction tasks
nodetool tpstats | grep -A5 "CompactionExecutor"

# Show per-table SSTable count and size
nodetool cfstats <keyspace>.<table>

# Show compaction history
nodetool compactionhistory

# Show active compaction operations
nodetool compactionstats
```

### Interpreting nodetool tpstats output

```
Pool Name                    Active   Pending      Completed   Blocked  All time blocked
CompactionExecutor               0         3          85432         0             0
```

| Field | Healthy range | Warning threshold | Critical threshold |
|-------|--------------|------------------|--------------------|
| Active | ≤ configured compaction threads | — | — |
| Pending | < 5 | 5-20 | > 20 |
| Blocked | 0 | > 0 briefly | Sustained > 0 |

### SSTable count per table (cfstats)

```
Table: events
SSTable count: 12           ← target < 20 for size-tiered; < 5 for leveled
Space used (live): 45GB
Space used (total): 67GB    ← difference = space waiting for compaction reclaim
```

**Target SSTable counts:**
- Size-tiered compaction: < 20 SSTables per table is normal; 20-50 is elevated; > 50 is a warning
- Leveled compaction: Level 0 should have < 4 SSTables (triggers compaction at 4); if Level 0 > 8, compaction is lagging

### Alert thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Pending compaction tasks | > 15 | > 50 | Increase compaction thread count (compaction_throughput_mb_per_sec) |
| SSTable count (size-tiered) | > 30 | > 60 | Check write rate vs compaction rate; reduce write throughput or add nodes |
| SSTable count (leveled, L0) | > 6 | > 12 | Compaction is behind; check disk I/O saturation |
| Disk space used / disk space total | > 60% | > 80% | Add disk capacity; compaction needs headroom |
| Space used (total) vs (live) ratio | > 1.5x | > 2.5x | Tombstones or stale versions not being collected; trigger manual compaction |

### Tuning compaction throughput (Cassandra)

```yaml
# cassandra.yaml
compaction_throughput_mb_per_sec: 64   # default; increase to 256+ for high-write workloads
concurrent_compactors: 2               # default; increase to 4-8 on nodes with > 8 CPU cores
```

Note: Increasing compaction throughput competes with read/write I/O. On disk-bound systems, more compaction throughput means less available for foreground queries. Test under production-representative load before increasing.

---

## RocksDB Compaction Metrics

### Key statistics (via RocksDB stats API or LOG file)

RocksDB writes compaction statistics to a LOG file and exposes them via `GetProperty`.

```bash
# From the RocksDB LOG file (location: /path/to/db/LOG)
grep "Compaction" /path/to/rocksdb/LOG | tail -50
```

### Key RocksDB properties

```cpp
// In application code or via rocksdb-cli
db->GetProperty("rocksdb.stats", &stats);
db->GetProperty("rocksdb.compaction-pending", &pending);
db->GetProperty("rocksdb.estimate-pending-compaction-bytes", &pending_bytes);
```

| Property | Meaning | Alert threshold |
|----------|---------|-----------------|
| `rocksdb.compaction-pending` | 1 if compaction is pending | Not a direct alert; use pending bytes |
| `rocksdb.estimate-pending-compaction-bytes` | Estimated bytes awaiting compaction | > 10GB: elevated; > 50GB: warning; > 100GB: critical |
| `rocksdb.num-files-at-level0` | Level 0 SSTable file count | > 20: warning; > 40: compaction cannot keep up |
| `rocksdb.total-sst-files-size` | Total SSTable files on disk | Compare to raw data size to measure space amplification |

### Write stall detection

RocksDB introduces write stalls and write stops when compaction cannot keep up. These are logged and can be monitored:

```
# In rocksdb LOG:
[WARN] Stalling writes because we have X level-0 files

# Write stop (engine refuses writes entirely):
[WARN] Stopping writes because we have X level-0 files
```

Write stall thresholds (configurable):
- Default write stall: 20 Level-0 files
- Default write stop: 36 Level-0 files

If write stalls are occurring, reduce write throughput, add compaction threads, or increase Level-0 file count thresholds (short-term mitigation only).

---

## HBase Compaction Metrics

HBase exposes compaction metrics via the HBase Master web UI (default: port 16010) and JMX.

### Key JMX metrics

| Metric | Path | Alert threshold |
|--------|------|-----------------|
| Compaction queue size | `Hadoop:service=HBase,name=RegionServer,sub=Server` → `compactionQueueLength` | > 10: elevated; > 50: warning |
| Store file count | HMaster UI → Tables → per-region store file count | > 10 per store: elevated |
| Write request rate | JMX → `writeRequestCount` | Compare to compaction throughput |

### Trigger manual major compaction (use sparingly)

```bash
# HBase shell
hbase shell
> major_compact 'tablename'
```

Major compaction rewrites all SSTables for a table into a single SSTable per region, reclaiming all tombstone space. It is I/O-intensive — run during off-peak hours only.

---

## Disk Headroom Rules

Insufficient disk headroom prevents compaction from proceeding. If the disk is > 80% full, compaction output files cannot be written, and the engine enters a degraded state.

**Minimum free disk space by compaction strategy:**

| Compaction strategy | Minimum free space | Recommended free space |
|--------------------|-------------------|-----------------------|
| Leveled (RocksDB, LevelDB default) | 30% | 40% |
| Leveled (Cassandra) | 30% | 40% |
| Size-tiered (Cassandra default, HBase) | 50% | 60-70% |
| Size-tiered during peak write burst | 70% | 80% |

Size-tiered compaction needs more headroom because during a compaction cycle, the engine temporarily holds both the input SSTables and the output SSTable on disk simultaneously. If the table being compacted is 30GB, compaction requires 30GB of free space to write the output before deleting the inputs.

---

## Failure Mode: Compaction Cannot Keep Up

**Symptoms:**
- SSTable count grows monotonically over time despite active compaction
- Read latency increases gradually as more SSTables must be checked per query
- `estimate-pending-compaction-bytes` (RocksDB) or pending compaction tasks (Cassandra) grow without decreasing
- Disk usage grows faster than raw write rate (uncompacted duplicates accumulating)

**Diagnosis:**

```bash
# Step 1: Is compaction running at all?
nodetool compactionstats   # Cassandra
grep "Compaction" /path/to/rocksdb/LOG | tail -20  # RocksDB

# Step 2: Is disk I/O saturated?
iostat -x 1    # Linux — watch %util for the disk device; > 90% = saturated

# Step 3: What is the write rate vs compaction throughput?
# If write rate (bytes/sec) > compaction throughput (bytes/sec), lag will grow
```

**Remediation options (in order of preference):**

1. **Reduce write rate** — shed load, batch writes, add rate limiting. Temporary relief.
2. **Increase compaction thread count** — more threads = more compaction throughput. Competes with foreground I/O.
3. **Switch compaction strategy** — size-tiered to leveled reduces space amplification; leveled to size-tiered reduces write amplification temporarily.
4. **Add nodes** — distribute the write load and compaction load across more machines.
5. **Add disk capacity** — buying time; does not fix the underlying throughput imbalance.
6. **Reduce TTL / tombstone accumulation** — if the workload has frequent deletes, tombstones accumulate and must be compacted. Shorter TTLs reduce tombstone buildup.

**What not to do:**
- Do not increase `compaction_throughput_mb_per_sec` beyond disk I/O capacity — it will not help and may make foreground performance worse.
- Do not stop and restart the database hoping compaction will "catch up" — restart does not change the throughput balance.
- Do not ignore growing SSTable counts — the system will eventually stop accepting writes or run out of disk space.
