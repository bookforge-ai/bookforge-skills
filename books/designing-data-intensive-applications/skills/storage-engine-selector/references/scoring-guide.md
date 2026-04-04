# Scoring Guide: Storage Engine Selector

This reference provides per-dimension scoring rubrics (1–5), a compaction strategy decision tree, and a workload-to-product routing table for use with Step 2 and Step 4 of the `storage-engine-selector` skill.

---

## Per-Dimension Scoring Rubrics

### D1: Write Throughput

Score the engine's suitability for the workload's write volume.

| Score | Meaning | Example condition |
|-------|---------|-------------------|
| 5 | Engine is structurally optimized for this write volume; handles it with commodity hardware | LSM-tree for 100K+ writes/sec sustained |
| 4 | Engine handles this write volume well with standard configuration | B-tree for 10K-50K writes/sec on SSD with WAL tuning |
| 3 | Engine can handle this write volume with tuning or vertical scaling | B-tree for 50K-100K writes/sec; requires fast NVMe + significant RAM |
| 2 | Engine can technically handle this write volume but requires significant sharding/overprovisioning | B-tree for 200K+ writes/sec — expensive and operationally complex |
| 1 | Engine cannot sustain this write volume without architectural workarounds that change the fundamental access model | B-tree for 1M+ writes/sec — not viable without a queue/buffer layer |

**Write volume thresholds (approximate, commodity hardware, 2024 SSD):**

| Volume | LSM-tree fit | B-tree fit |
|--------|-------------|-----------|
| < 5K writes/sec | Both fine | Both fine |
| 5K-50K writes/sec | Both viable | Both viable |
| 50K-500K writes/sec | LSM-tree preferred | B-tree viable with tuning |
| 500K-5M writes/sec | LSM-tree required | B-tree not recommended |
| > 5M writes/sec | Distributed LSM-tree (Cassandra/HBase) | B-tree not viable |

---

### D2: Write Amplification

Score the engine's write amplification relative to the workload's durability requirements and hardware constraints.

| Score | Meaning |
|-------|---------|
| 5 | Minimal write amplification; each logical write causes ≤2 physical writes |
| 4 | Low write amplification (2-4x); typical for well-tuned B-tree with WAL |
| 3 | Moderate write amplification (4-8x); typical for LSM-tree with leveled compaction |
| 2 | High write amplification (8-15x); typical for LSM-tree with leveled compaction under sustained high load |
| 1 | Very high write amplification (>15x); SSD wear concern; B-tree with frequent page splits |

**Notes:**
- In-memory (cache-only): score 5 — no physical disk writes for writes; async persistence only
- In-memory (durable with AOF): score 4 — append-only log; no page-level amplification
- Size-tiered LSM: score 4 during active writes, score 2-3 during compaction bursts
- Leveled LSM: score 3 steady-state; consistent amplification (~10x per level traversal)

---

### D3: Read Performance

Score the engine's suitability for the workload's dominant read pattern.

| Score | Meaning |
|-------|---------|
| 5 | Engine is structurally optimized for this read pattern; predictable O(log n) or better |
| 4 | Good read performance; occasional extra lookups but Bloom filters or caching mitigate |
| 3 | Adequate read performance; requires tuning (Bloom filters, block cache size) |
| 2 | Suboptimal for this read pattern; works but degrades as dataset grows |
| 1 | Structurally poorly suited; each read requires checking many data structures |

**Read pattern to engine fit:**

| Read pattern | LSM-tree | B-tree | In-memory |
|-------------|----------|--------|-----------|
| Point lookup (key exists) | 4 (memtable + 1-2 SSTable levels with Bloom filter) | 5 (O(log n) to leaf) | 5 (O(1) hash) |
| Point lookup (key absent) | 2-4 (Bloom filter critical; without it = all levels) | 4 (O(log n) confirms absence) | 5 |
| Range scan, narrow | 4 (sorted within SSTable; merge across levels) | 5 (contiguous leaf pages) | 3 (no structural range support unless sorted set) |
| Range scan, wide | 3 (must merge multiple SSTable levels) | 5 (sibling page pointers; sequential I/O) | 3 |
| Full table scan | 3 (sequential SSTable reads; good compression) | 3 (sequential page scan; fragmentation affects) | 4 (RAM bandwidth limited) |

---

### D4: Latency Predictability

Score the engine's ability to maintain consistent latency under the workload's conditions.

| Score | Meaning |
|-------|---------|
| 5 | p99 and p999 latency are consistent; no background process interferes with foreground I/O |
| 4 | Mostly consistent; occasional brief spikes during maintenance (VACUUM, checkpoint) that are predictable and schedulable |
| 3 | Periodic latency spikes from background compaction; spikes are measurable but tolerable for non-SLA-critical workloads |
| 2 | Compaction competes with foreground I/O; p99 spikes are frequent at high write rates |
| 1 | Compaction lag causes persistent latency degradation; indistinguishable from a failure state |

**Latency SLA to engine fit:**

| Latency SLA | LSM-tree fit | B-tree fit | In-memory fit |
|------------|-------------|-----------|--------------|
| p99 < 5ms, always | 2 (compaction spikes risk this) | 4 | 5 |
| p99 < 20ms, always | 3 (manageable with compaction tuning) | 5 | 5 |
| p99 < 100ms, mostly | 4 | 5 | 5 |
| Best-effort, no SLA | 5 | 5 | 5 |

---

### D5: Space Efficiency

Score the engine's disk space usage relative to the raw data size.

| Score | Meaning |
|-------|---------|
| 5 | Space overhead < 10% of raw data size; excellent compression |
| 4 | Space overhead 10-30%; minor fragmentation or redundancy |
| 3 | Space overhead 30-60%; some fragmentation or compaction-in-progress redundancy |
| 2 | Space overhead 60-100%; significant fragmentation or size-tiered compaction temp space |
| 1 | Space overhead > 100%; multiple full copies of data exist simultaneously |

**Rule of thumb disk headroom requirements:**
- B-tree: maintain 20-30% free for page splits and VACUUM
- LSM-tree leveled: maintain 30-40% free for compaction output staging
- LSM-tree size-tiered: maintain 50-100% free to avoid compaction being unable to proceed
- In-memory: RAM cost is 10-100x SSD/HDD per GB; factor into cost analysis

---

### D6: Transactional Semantics

Score the engine's native support for the workload's transaction requirements.

| Score | Meaning |
|-------|---------|
| 5 | Full ACID transactions (atomicity, consistency, isolation, durability) natively supported; serializable isolation available |
| 4 | Read committed or snapshot isolation available; most OLTP workloads covered |
| 3 | Basic atomicity per key (single-row atomic); multi-row transactions require application-level coordination |
| 2 | Eventual consistency by default; lightweight transactions (CAS operations) available but expensive |
| 1 | No transaction support; all consistency is application-level |

**Engine to transaction support:**

| Engine family | Native transaction support |
|--------------|---------------------------|
| B-tree (PostgreSQL, InnoDB) | 5 — full ACID, serializable isolation, row-level locks |
| LSM-tree (RocksDB with transactions) | 4 — optimistic and pessimistic transactions available |
| LSM-tree (Cassandra, HBase) | 2 — eventual consistency default; CAS (Lightweight Transactions in Cassandra) |
| In-memory (VoltDB, MemSQL) | 5 — full ACID in-memory |
| In-memory (Redis) | 3 — single-command atomic; MULTI/EXEC for multi-command atomicity; no isolation |
| In-memory (Memcached) | 1 — no transactions |

---

### D7: Compaction Risk

Score the operational risk introduced by the engine's background maintenance process.

| Score | Meaning |
|-------|---------|
| 5 | No compaction process; background maintenance is lightweight and schedulable |
| 4 | Background maintenance (VACUUM, checkpoint) is predictable and easily scheduled during off-peak hours |
| 3 | Compaction runs continuously; risk is low with proper monitoring and headroom |
| 2 | Compaction can lag at high write rates; requires active monitoring and capacity planning |
| 1 | Compaction lag is a known production issue at this write volume; requires dedicated ops attention |

**When to flag compaction risk as a disqualifier:**
- Team has no dedicated database operations capacity (< 2 engineers with DB expertise)
- Write rate is expected to grow 3x+ in 12 months without a corresponding ops team scaling plan
- Budget for disk capacity headroom is constrained (< 50% free disk; size-tiered compaction needs more)

---

## Compaction Strategy Decision Tree

```
Is LSM-tree the selected engine family?
├── NO → Compaction strategy N/A
└── YES
    ├── Is write throughput the primary optimization target?
    │   (sustained writes > 500K/sec; insert-dominant; batch ingest)
    │   ├── YES → Size-tiered compaction
    │   │   └── Ensure 50-100% disk headroom for compaction temp space
    │   └── NO (balanced or read-leaning)
    │       ├── Are range queries > 20% of reads?
    │       │   ├── YES → Leveled compaction (better range scan; key per level)
    │       │   └── NO
    │       │       ├── Is disk space constrained (< 50% headroom)?
    │       │       │   ├── YES → Leveled compaction (less space waste)
    │       │       │   └── NO → Either; default to leveled (better-known behavior)
    │       └── Default → Leveled compaction
```

---

## Workload-to-Product Routing Table

| Workload | Recommended engine | Recommended product | Key consideration |
|----------|-------------------|--------------------|--------------------|
| High-volume event ingestion (IoT, clickstream, logs) | LSM-tree, size-tiered | Cassandra, Kafka + RocksDB | Monitor compaction lag at peak write rates |
| Time-series metrics | LSM-tree, leveled | InfluxDB (internal TSM = LSM variant), RocksDB, TimescaleDB (on PostgreSQL) | Retention policies drive compaction cadence |
| Financial ledger, inventory | B-tree, ACID | PostgreSQL, MySQL InnoDB | Serializable isolation required; horizontal scale via Citus or CockroachDB |
| Key-value cache, session store | In-memory | Redis, Memcached | Decide on persistence requirement before choosing |
| General-purpose OLTP (e-commerce, SaaS) | B-tree | PostgreSQL | Default choice; only deviate with evidence of write bottleneck |
| Full-text search | LSM-tree (inverted index) | Elasticsearch, OpenSearch, Meilisearch | Not a general-purpose storage choice; use alongside a primary DB |
| Embedded key-value (application-internal) | LSM-tree | RocksDB, LevelDB | Not a standalone server; embedded in the application process |
| Wide-column, Hadoop ecosystem | LSM-tree | HBase | Requires ZooKeeper, HDFS operational knowledge |
| Read-heavy product catalog | In-memory + B-tree | Redis (cache) + PostgreSQL (source of truth) | Write-through or write-behind cache pattern |
| Distributed SQL (multi-region ACID) | B-tree (distributed) | CockroachDB, Google Spanner, YugabyteDB | Higher latency than single-region B-tree; consensus protocol adds overhead |
