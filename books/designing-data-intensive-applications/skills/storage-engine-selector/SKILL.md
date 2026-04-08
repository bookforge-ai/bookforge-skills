---
name: storage-engine-selector
description: |
  Select the right storage engine architecture (LSM-tree, B-tree, or in-memory) for a database workload using a 7-dimensional scored trade-off analysis. Use when evaluating RocksDB vs InnoDB vs LevelDB, diagnosing write amplification in production, choosing between write-optimized vs read-optimized storage, selecting a compaction strategy (size-tiered vs leveled), or deciding whether to skip disk with an in-memory database. Also use for: comparing Cassandra vs PostgreSQL storage internals; justifying an existing engine choice to a team; assessing whether compaction pauses are causing latency spikes. Covers LSM-tree family (LevelDB, RocksDB, Cassandra, HBase), B-tree family (PostgreSQL, MySQL InnoDB, SQLite), and in-memory stores (Redis, Memcached, VoltDB).
  For choosing between relational/document/graph models, use data-model-selector instead. For OLTP vs. analytics routing, use oltp-olap-workload-classifier instead. For replication topology, use replication-strategy-selector instead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/storage-engine-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [3]
tags: [storage-engine, lsm-tree, b-tree, sstable, compaction, write-amplification, rocksdb, leveldb, cassandra, hbase, innodb, postgresql, in-memory-database, write-throughput, read-performance, latency, space-efficiency, transactions, database-selection, workload-analysis]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application codebase, docker-compose, schema files, or architecture description — any artifact that reveals data access patterns"
    - type: document
      description: "Workload description or requirements document if no codebase is available"
  tools-required: [Read, Write, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Run inside a project directory where codebase or configuration files exist. Falls back to document/description input if no codebase."
discovery:
  goal: "Identify the optimal storage engine architecture for a given workload and produce a concrete recommendation backed by a 7-dimensional scored comparison"
  tasks:
    - "Classify the workload (read-heavy, write-heavy, mixed; point lookups vs range scans)"
    - "Score LSM-tree, B-tree, and in-memory across 7 dimensions for this workload"
    - "Select a compaction strategy if LSM-tree is recommended"
    - "Identify concrete database products matching the recommendation"
    - "Flag compaction risk, write amplification risk, or latency predictability issues"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "site-reliability-engineer", "tech-lead"]
    experience: "intermediate-to-advanced — assumes experience with databases and SQL"
  triggers:
    - "User is choosing between database products and wants to understand storage internals"
    - "User has a write-heavy workload and wants to know if RocksDB or Cassandra is appropriate"
    - "User is experiencing write amplification or compaction stalls in production"
    - "User wants to justify switching from B-tree (PostgreSQL) to LSM-tree (RocksDB) storage"
    - "User is evaluating whether to use an in-memory database"
    - "User is comparing Cassandra vs PostgreSQL for a new service"
    - "User is reviewing an architecture decision involving database storage"
  not_for:
    - "Choosing between OLTP and OLAP systems — use oltp-olap-workload-classifier first"
    - "Selecting a data model (relational, document, graph) — use data-model-selector"
    - "Replication or partitioning strategy — use replication-strategy-selector or partitioning-strategy-advisor"
---

# Storage Engine Selector

## When to Use

You have a workload — a new service, an existing system with performance problems, or an architecture decision pending — and need to choose between storage engine architectures: log-structured merge-tree (LSM-tree), B-tree, or in-memory.

This skill applies when the storage engine choice is open, contested, or needs justification. It produces a concrete recommendation (engine family + product + compaction strategy if applicable) backed by a scored 7-dimensional comparison your team can review and challenge.

**Prerequisite check:** If you do not yet know whether the workload is OLTP or OLAP, run `oltp-olap-workload-classifier` first. This skill assumes an OLTP or mixed workload. Column-oriented storage for analytics is out of scope here.

**Related skills:**
- `data-model-selector` — choose between relational, document, and graph models before choosing a storage engine
- `oltp-olap-workload-classifier` — classify workload type if uncertain

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Write/read ratio:**  Why: The fundamental split. LSM-trees are write-optimized; B-trees are read-optimized. Without the ratio, the primary dimension cannot be scored.
  - Check prompt for: "write-heavy", "read-heavy", "mixed", throughput numbers, writes/sec, reads/sec
  - Check environment for: application code (count DB write vs read calls), docker-compose (any write-intensive services like queues, event logs), schema (append-only tables suggest write-heavy)
  - If still missing, ask: "What is your approximate write-to-read ratio? For example: 80% writes / 20% reads, or mostly reads with occasional bulk imports?"

- **Query patterns:**  Why: Range scans favor B-trees (keys are sorted in-place on disk); point lookups are fine for both but LSM-trees may need Bloom filters. Full-text search requires LSM-tree-backed indexes (e.g., Lucene).
  - Check prompt for: "range queries", "ORDER BY", "BETWEEN", "time-series", "prefix scan", "key lookup", "GET by ID"
  - Check environment for: schema.sql (range indexes, composite indexes), application code (scan vs get patterns)
  - If still missing, ask: "Do your queries primarily look up individual records by key, or do they scan ranges of records (e.g., 'all events between timestamp A and B', 'all users with names starting with X')?"

- **Latency requirements:**  Why: B-trees provide more predictable latency because reads/writes go to a fixed page. LSM-trees have compaction pauses that can spike tail latency unpredictably. SLA-sensitive services need to know this.
  - Check prompt for: SLA numbers (p99 latency), "latency-sensitive", "real-time", "user-facing"
  - Check environment for: requirements.md, architecture.md (SLA definitions), config files (read timeout settings)
  - If still missing, ask: "Do you have a latency SLA? For example, p99 response time under 50ms? Or is this a background/batch service where occasional slowdowns are acceptable?"

- **Durability requirements:**  Why: In-memory databases lose data on restart (unless configured otherwise). If the dataset must survive process failures without replica recovery, disk-based storage is required.
  - Check prompt for: "durable", "ACID", "must not lose data", "crash recovery", or conversely "cache", "ephemeral", "rebuilt on restart"
  - Check environment for: docker-compose restart policies, backup configurations, any mention of replication
  - If still missing, ask: "If the database process crashes, is it acceptable to lose recent writes (rebuilding from a replica or cache), or must every write be durable to disk immediately?"

### Observable Context (gather from environment)

- **Existing database choice:** Look for `docker-compose.yml`, `requirements.txt`, `pom.xml`, or `package.json` for database driver imports. Tells you what is already in use and whether this is a greenfield or migration decision.
- **Data volume:** Look for schema definitions (row counts, partitioning hints), README, or architecture docs. Affects in-memory feasibility.
- **Access pattern code:** Grep the codebase for DB write vs read call ratios; look for bulk insert patterns, streaming writes, or time-series data accumulation.
- **Existing compaction config:** Look for `rocksdb.ini`, `cassandra.yaml`, or similar — signals existing LSM-tree usage and whether compaction is already tuned.

### Default Assumptions

When context cannot be observed and asking would be excessive:
- Write/read ratio unknown → assume mixed (50/50); note this assumption explicitly
- Range query usage unknown → assume point lookups dominate
- Latency SLA unknown → assume best-effort; latency predictability is a "nice to have"
- Data volume unknown → assume larger than available RAM (rules out pure in-memory without further information)

---

## Process

### Step 1: Classify the Workload

**ACTION:** Determine the workload profile across three axes: (a) write intensity, (b) query pattern, (c) latency sensitivity.

**WHY:** The storage engine decision follows directly from these three inputs. Write intensity determines the primary axis (LSM vs B-tree). Query pattern determines whether range scan optimization matters. Latency sensitivity determines whether compaction jitter is acceptable. Getting this classification right avoids the most common mistake: choosing a write-optimized engine (LSM-tree) for a read-heavy workload with range scans, or a read-optimized engine (B-tree) for a write-heavy append-log workload.

Produce a one-line classification:

```
Workload: [write-heavy | read-heavy | mixed]
           [point-lookup-dominant | range-scan-dominant | mixed queries]
           [latency-SLA-strict | best-effort latency]
```

**IF** the user describes OLAP, analytics, or columnar access → stop here and recommend `oltp-olap-workload-classifier` + column-oriented storage (out of scope for this skill).

**ELSE** → proceed to Step 2 with the OLTP/mixed classification.

---

### Step 2: Score All Three Engine Families on 7 Dimensions

**ACTION:** Score LSM-tree, B-tree, and in-memory across all 7 dimensions for this specific workload. Use a 1–5 scale per dimension (5 = strong fit, 1 = poor fit or disqualifying).

**WHY:** Scoring all dimensions — not just the obvious one — prevents premature convergence. Engineers often pick "write-heavy → Cassandra" without checking latency predictability (LSM compaction can spike p99 badly for low-latency SLAs). Running the full matrix surfaces disqualifying factors that a shortcut misses. It also produces a reviewable artifact that makes the trade-off explicit for the team.

**The 7 dimensions:**

| Dimension | LSM-tree | B-tree | In-memory |
|-----------|----------|--------|-----------|
| **D1: Write Throughput** | High — sequential SSTable writes; compaction batches rewrites. Typical: 100K-1M+ writes/sec on commodity hardware. | Moderate — must update a page in-place; WAL + page write = 2+ disk writes per record. Random page updates are slow on HDDs. | Highest — writes go directly to RAM; disk persistence (if any) is async append. |
| **D2: Write Amplification** | Moderate-to-high — each write may be rewritten multiple times across compaction levels. Leveled compaction: ~10x typical. Size-tiered: lower initial amplification but larger space use. | High — B-tree index must write every piece of data at least twice (WAL + page); page splits cause additional parent writes. | None (for cache-only). Minimal (for durable in-memory with append log). |
| **D3: Read Performance** | Moderate — reads must check memtable + multiple SSTable levels. Bloom filters help for point lookups; absent key lookups require checking all levels. Range scans are efficient once SSTables are sorted. | High — O(log n) traversal to leaf page; keys are sorted in-place; range scans read contiguous pages. Predictable. | Highest — reads served entirely from RAM with no disk I/O. |
| **D4: Latency Predictability** | Low-to-moderate — compaction runs in background threads and competes for disk bandwidth. At high write throughput, compaction may lag; tail latency spikes (p99/p999). | High — reads and writes go to fixed pages; no background reorganization that spikes latency. Well-established, mature behavior. | High — no disk I/O on the read path; latency is consistent. Network round-trip dominates. |
| **D5: Space Efficiency** | Better than B-tree — no page fragmentation; leveled compaction removes redundant copies; compression across sorted blocks is more effective. | Lower — pages have reserved space for future inserts; page splits leave partially-full pages; fragmentation accumulates over time. | Lowest space-to-cost ratio — RAM is 10-100x more expensive per GB than SSD/HDD. |
| **D6: Transactional Semantics** | Weaker by default — a key may exist in multiple SSTable segments; each segment is a snapshot, not a single source of truth. Row-level locks are complex to implement. Some LSM engines (RocksDB transactions, Cassandra LWT) add transaction support, but it is not native. | Strong — each key exists in exactly one place in the index. Range locks attach directly to B-tree pages. Relational databases (PostgreSQL, MySQL InnoDB) build full ACID transactions on top of B-trees. | Varies — depends on implementation. VoltDB/MemSQL offer full ACID. Redis is single-threaded (atomic per command) but not ACID across commands. |
| **D7: Compaction Risk** | Real — if write throughput exceeds compaction rate, unmerged segment files accumulate; read performance degrades (more segments to check); disk space grows unbounded. Requires active monitoring. Not applicable in size-tiered compaction. | None — no compaction process. Pages are reused in-place. Fragmentation grows slowly but is managed by VACUUM (PostgreSQL) or similar. | None — no disk segments. |

**Scoring template:**

```
Dimension                    LSM-tree  B-tree  In-memory
D1: Write Throughput         [1-5]     [1-5]   [1-5]
D2: Write Amplification      [1-5]     [1-5]   [1-5]
D3: Read Performance         [1-5]     [1-5]   [1-5]
D4: Latency Predictability   [1-5]     [1-5]   [1-5]
D5: Space Efficiency         [1-5]     [1-5]   [1-5]
D6: Transactional Semantics  [1-5]     [1-5]   [1-5]
D7: Compaction Risk          [1-5]     [1-5]   [1-5]
                             ------    ------  ---------
Weighted Total               [X/35]    [X/35]  [X/35]
```

Score each dimension relative to the workload classification from Step 1. A write-heavy workload makes D1 and D2 high-weight; a strict-latency workload makes D4 a potential disqualifier.

See `references/scoring-guide.md` for per-dimension scoring rubrics and worked examples.

---

### Step 3: Apply Disqualifying Filters

**ACTION:** Check for hard disqualifiers before ranking by total score. A single disqualifying condition overrides a high total score.

**WHY:** Total score averaging can hide a fatal flaw. A storage engine that scores 4/5 on six dimensions but 1/5 on one critical dimension (e.g., durability for in-memory when data loss is unacceptable) should be eliminated, not ranked second. Disqualifiers must be applied before totaling.

**Disqualifying conditions:**

| Condition | Disqualifies |
|-----------|-------------|
| Data must survive crash without replica recovery | In-memory (cache-only configurations) |
| Strict ACID transactions required (e.g., financial ledger, inventory) | LSM-tree (unless RocksDB transactions or similar explicitly configured) |
| Latency SLA < 10ms p99, write throughput > 100K/sec simultaneously | LSM-tree (compaction stalls cannot be fully eliminated at high write rates) |
| Dataset >> available RAM, no tolerance for cache misses | In-memory |
| Range scans > 50% of queries AND write volume is low | LSM-tree (reads must check multiple SSTable levels; B-tree range scans are O(log n) with contiguous page reads) |
| Compaction monitoring is not feasible (no ops team) | LSM-tree (compaction lag is a production risk that requires active monitoring) |

Apply disqualifiers. If a family is disqualified, remove it from further scoring.

---

### Step 4: Select Compaction Strategy (if LSM-tree survives)

**ACTION:** If LSM-tree is not disqualified, select between size-tiered and leveled compaction based on the workload.

**WHY:** Compaction strategy is the primary tuning lever inside the LSM-tree family and has significant impact on space efficiency, read amplification, and write amplification. Choosing the wrong strategy is a common cause of LSM-tree production problems. LevelDB and RocksDB use leveled compaction by default; Cassandra supports both and defaults to size-tiered. This choice must be explicit.

**Size-tiered compaction:**
- How it works: Newer, smaller SSTables are merged into older, larger SSTables. Tables are organized in tiers by size.
- Best for: Write-heavy workloads where space amplification is acceptable and write throughput is paramount. Lower write amplification during active writes.
- Tradeoff: More space used temporarily (multiple copies of overlapping key ranges exist during compaction). Less suited for read-heavy workloads (more overlap = more segments to check per read).
- Used by: Cassandra (default), HBase.

**Leveled compaction:**
- How it works: The key range is split into smaller SSTables organized into levels. Each level is 10x larger than the previous. A key appears in at most one SSTable per level.
- Best for: Balanced read/write workloads where space efficiency and read performance matter. Better for range scans. Less disk space wasted.
- Tradeoff: Higher write amplification (a key may be rewritten ~10x as it moves through levels).
- Used by: LevelDB, RocksDB (default).

**Decision rule:**
- Write throughput >> read performance AND space is not constrained → size-tiered
- Balanced workload OR space efficiency matters → leveled
- Unsure → leveled (better-known behavior; easier to reason about production issues)

---

### Step 5: Identify Concrete Database Products

**ACTION:** Map the winning engine family and compaction strategy (if LSM-tree) to specific database products available in the ecosystem.

**WHY:** The engine family is the architectural choice; the product is what the team actually installs. Different products within the same family have significantly different operational characteristics, ecosystem support, and cloud availability. The recommendation must be concrete to be actionable.

**LSM-tree family:**

| Product | Best for | Notes |
|---------|----------|-------|
| **RocksDB** | Embedded key-value store; high write throughput; used as storage engine in other DBs (MySQL MyRocks, CockroachDB, TiKV) | Leveled compaction default; highly configurable; C++ library, not a standalone server |
| **LevelDB** | Embedded key-value, simpler than RocksDB | Leveled compaction; less tunable; good for learning or simple embedded use |
| **Cassandra** | Distributed, multi-datacenter, high write throughput at scale; time-series, IoT, event logs | Size-tiered or leveled compaction; CQL interface; no joins; eventual consistency by default |
| **HBase** | HDFS-backed, Hadoop ecosystem; wide-column, very large datasets | Based on Google Bigtable; size-tiered compaction; strong consistency with ZooKeeper |
| **Elasticsearch / Lucene** | Full-text search; inverted index built on SSTable-like structures | LSM-tree internals for term dictionaries; not a general-purpose key-value store |

**B-tree family:**

| Product | Best for | Notes |
|---------|----------|-------|
| **PostgreSQL** | Full ACID, complex queries, relational model, JSON support | B-tree indexes; MVCC; mature; best general-purpose choice for OLTP |
| **MySQL InnoDB** | ACID OLTP; clustered index (primary key = clustered B-tree); wide deployment | InnoDB is the default engine in MySQL; MyISAM is legacy |
| **SQLite** | Embedded; single-writer; mobile/desktop apps | B-tree storage; full ACID; not for concurrent high-throughput |
| **LMDB** | High-read, embedded; copy-on-write B-tree; used in OpenLDAP | No WAL; crash-safe by design; single-writer model |

**In-memory family:**

| Product | Best for | Notes |
|---------|----------|-------|
| **Redis** | Cache, session store, leaderboards, pub/sub | Weak durability (async AOF/RDB); not ACID; single-threaded per command |
| **Memcached** | Pure LRU cache; no persistence; simpler than Redis | Data loss on restart is expected |
| **VoltDB / MemSQL (SingleStore)** | ACID in-memory OLTP; financial transactions at speed | Full SQL, full ACID; data survives restart via disk snapshots/replication |
| **RAMCloud** | Research prototype; log-structured in-memory + disk | Durable in-memory with log-structured persistence |

---

### Step 6: Produce the Recommendation

**ACTION:** Write a structured recommendation covering the winning engine family, concrete product(s), compaction strategy (if applicable), and the key trade-offs that drove the decision.

**WHY:** A concrete recommendation with explicit rationale enables team alignment and prevents relitigating the decision. The scoring table makes trade-offs transparent. The "what we're giving up" section is essential — it prevents future surprise when the selected engine's weaknesses surface in production.

**Output format:**

```
## Storage Engine Recommendation

### Workload Classification
[One-line workload profile from Step 1]

### Recommendation
**Engine Family:** [LSM-tree | B-tree | In-memory]
**Compaction Strategy:** [Size-tiered | Leveled | N/A]
**Primary Product:** [Specific database product]
**Alternative Product:** [Second option if applicable]

### 7-Dimension Score Summary
| Dimension                 | LSM-tree | B-tree | In-memory | Weight for this workload |
|--------------------------|:--------:|:------:|:---------:|:------------------------:|
| D1: Write Throughput     | [score]  | [score]| [score]   | [High/Medium/Low]        |
| D2: Write Amplification  | [score]  | [score]| [score]   | [High/Medium/Low]        |
| D3: Read Performance     | [score]  | [score]| [score]   | [High/Medium/Low]        |
| D4: Latency Predictability | [score] | [score]| [score]  | [High/Medium/Low]        |
| D5: Space Efficiency     | [score]  | [score]| [score]   | [High/Medium/Low]        |
| D6: Transactional Semantics | [score] | [score]| [score] | [High/Medium/Low]       |
| D7: Compaction Risk      | [score]  | [score]| [score]   | [High/Medium/Low]        |
| **Weighted Total**       | **[X]**  | **[X]**| **[X]**   |                          |

### Why [Winning Engine]
[2-3 sentences connecting the workload classification to the winning dimensions]

### What We're Giving Up
[1-2 sentences on the primary trade-off — what the selected engine does poorly
and how the team should mitigate it]

### Disqualifiers Applied
[If any engine families were disqualified, state why]

### Compaction Risk Flag (LSM-tree only)
[If LSM-tree is selected: what write throughput level risks outpacing compaction,
what metric to monitor, and what the failure mode looks like]

### Operational Notes
[Specific tuning recommendations or gotchas for the selected product]
```

---

## What Can Go Wrong

**Compaction cannot keep up with write rate.** If write throughput exceeds the compaction thread's ability to merge SSTable files, the number of unmerged segments on disk grows unboundedly. Read performance degrades (each read must check more segments), disk space grows, and eventually the system runs out of space. LSM-tree-based engines like Cassandra do not throttle incoming writes when compaction lags — they rely on the operator to monitor this. Monitor: number of SSTables per partition (Cassandra), compaction pending tasks, disk space growth rate.

**Write amplification degrades SSD lifespan.** B-tree and LSM-tree engines both cause write amplification — each logical write results in multiple physical writes. On SSDs, which have a limited number of program/erase cycles per block, sustained write amplification accelerates wear. Leveled compaction in LSM-trees has ~10x write amplification; B-trees typically have 2-4x. For write-heavy workloads on SSDs, track disk write bytes vs application write bytes to measure actual amplification.

**LSM-tree read amplification for absent keys.** If many reads query keys that do not exist in the database, LSM-tree engines must check the memtable and then each SSTable level before confirming the key is absent. Without Bloom filters, this causes multiple disk reads per absent-key lookup. Bloom filters (used by LevelDB, RocksDB, Cassandra) eliminate most absent-key disk reads but require additional memory.

**B-tree fragmentation and VACUUM costs.** B-trees leave partially-full pages after page splits and row deletions. In PostgreSQL, dead row versions accumulate until VACUUM reclaims them. A system that never runs VACUUM (or runs it too infrequently) will see table bloat, degraded scan performance, and transaction ID wraparound issues. VACUUM competes with production queries for I/O.

**In-memory data loss on restart.** Products like Redis (without persistent configuration) and Memcached lose all data on process restart. This is expected behavior for caches, but is a catastrophic failure mode for systems that stored durable state. Verify durability configuration before using any in-memory product for non-ephemeral data.

**Choosing B-tree for write-heavy append workloads on HDDs.** On magnetic hard drives, random writes to B-tree pages are dramatically slower than sequential writes. A write-heavy workload that uses a B-tree engine on HDD may see 10-100x worse write throughput than the same workload on an LSM-tree engine, because each page update requires a disk head seek. LSM-trees write sequentially by design, which aligns with HDD hardware characteristics.

---

## Key Principles

**The engine-workload match is the primary decision axis — not the database brand.** Choosing PostgreSQL vs Cassandra is often framed as a "SQL vs NoSQL" decision, but the real driver is B-tree vs LSM-tree storage internals. Many teams pick a database for API familiarity and suffer performance problems because the storage engine is mismatched to the workload. Map workload characteristics first, then identify products that match.

**Write amplification is a system-level concern, not just a performance metric.** Both B-trees (WAL + page write) and LSM-trees (compaction rewrites) amplify writes. On SSDs, write amplification directly affects hardware lifespan and effective I/O bandwidth. On HDDs, the pattern (random vs sequential) matters more than the amplification factor. Quantify write amplification before concluding that "SSD makes the difference negligible."

**LSM-tree compaction strategy is not a one-time decision — it requires ongoing operations.** Selecting leveled vs size-tiered compaction sets the default behavior, but production workloads change. A write rate that doubled over 6 months may outpace a compaction configuration that worked at launch. LSM-tree engines require operators who monitor compaction health and tune it as load evolves. If the team lacks this capacity, prefer B-tree or a managed cloud service (Amazon DynamoDB, Google Bigtable) that handles compaction operationally.

**In-memory is not just "cache." It is a storage architecture choice with trade-offs.** The performance advantage of in-memory databases is not primarily that they avoid disk reads — the OS page cache already caches hot data in memory for disk-based engines. In-memory databases are faster because they avoid the overhead of encoding in-memory data structures into on-disk formats. They also enable richer in-memory data structures (priority queues, sets, sorted sets in Redis) that are expensive to implement on disk. Choose in-memory for the data structure capabilities, not only for read speed.

**Range queries are inherently easier for B-trees.** In an LSM-tree, sorted key ranges exist within each SSTable, but range scans that span multiple SSTables and levels require merging results from multiple files. In a B-tree, keys at the same level are stored on contiguous pages; a range scan follows sibling pointers across leaf pages. For range-scan-dominant workloads (time-series ranges, alphabetical ranges, geospatial ranges), B-tree provides structurally lower read amplification.

**B-tree transaction semantics are a genuine advantage, not just a feature.** B-tree engines store each key in exactly one location. This makes it straightforward to attach range locks to tree nodes, implement MVCC (multi-version concurrency control), and guarantee snapshot isolation. LSM-tree engines may have multiple copies of the same key across SSTable segments; enforcing single-writer semantics or range locks requires coordination layers on top of the storage engine. For workloads that require serializable isolation or complex multi-key transactions, B-tree is the structurally simpler choice.

---

## Examples

### Example 1: Time-Series IoT Event Log (Write-Heavy, Eventual Consistency Acceptable)

**Scenario:** A device telemetry platform ingests sensor readings from 500K devices at 5 events/device/second (2.5M events/sec peak). Queries are mostly recent-window reads ("last 24 hours per device") and aggregate dashboards. There is no requirement for multi-row transactions. The team runs on AWS with a 4-person platform engineering team.

**Trigger:** "We're choosing between Cassandra and PostgreSQL for our IoT ingestion layer. Write volume is the primary constraint."

**Process:**
- Step 1: Write-heavy (99% writes at peak), mixed queries (mostly recent-range, some point lookups), best-effort latency (dashboards tolerate 1-2 second delays)
- Step 2: D1 write throughput → LSM-tree=5, B-tree=2; D4 latency predictability → not a disqualifier; D6 transactions → not required (score equally)
- Step 3: No disqualifiers for LSM-tree; B-tree disqualified by write throughput at this scale without extreme horizontal sharding
- Step 4: Size-tiered compaction — write rate is sustained and high; space amplification is acceptable; Cassandra size-tiered is default and well-tested at this scale
- Step 5: Cassandra (distributed, multi-region, proven at IoT scale); DynamoDB as managed alternative

**Output summary:**
```
## Storage Engine Recommendation

### Recommendation
Engine Family: LSM-tree
Compaction Strategy: Size-tiered (Cassandra default)
Primary Product: Apache Cassandra
Alternative Product: Amazon DynamoDB (managed LSM-tree; removes compaction ops burden)

### Why LSM-tree
2.5M events/sec sustained writes require sequential SSTable appends, not random
B-tree page updates. At this write volume, B-tree random I/O would require 50+
nodes to achieve parity. LSM-tree sequential writes scale linearly with nodes.

### What We're Giving Up
Complex multi-row transactions and ad-hoc joins are not available in Cassandra.
Design data models around denormalized, query-first schemas.

### Compaction Risk Flag
Monitor: nodetool tpstats (Cassandra) — CompactionExecutor pending tasks > 100
is a warning sign. At 2.5M events/sec, size-tiered compaction requires at least
2 dedicated compaction threads per node and ≥50% free disk space headroom.
```

---

### Example 2: Financial Ledger Service (Read-Balanced, ACID Required)

**Scenario:** A fintech startup is building a transaction ledger. Every debit/credit must be ACID-compliant (no partial writes, no duplicate entries). The read/write ratio is approximately 60% reads / 40% writes. The business has a strict p99 < 20ms latency SLA for balance lookups. The dataset is expected to be 500GB after 2 years — fits comfortably in a well-provisioned RDS instance.

**Trigger:** "We need a database for our ledger. Someone suggested Cassandra because it's 'scalable.' Does that make sense?"

**Process:**
- Step 1: Mixed workload (60/40), point-lookup-dominant (balance queries by account ID), latency-SLA-strict (p99 < 20ms)
- Step 2: D6 transactions → critical; D4 latency predictability → critical; D1 write throughput → moderate importance
- Step 3: LSM-tree disqualified — ACID multi-row transactions required (debit + credit must be atomic); compaction jitter risks p99 latency SLA. In-memory disqualified — durability required without replica dependency.
- Step 5: PostgreSQL (full ACID, B-tree, mature, proven for financial workloads)

**Output summary:**
```
## Storage Engine Recommendation

### Recommendation
Engine Family: B-tree
Compaction Strategy: N/A
Primary Product: PostgreSQL
Alternative Product: MySQL InnoDB (same storage family; more familiar to some teams)

### Why B-tree
ACID transactional semantics (debit + credit as atomic operation) require B-tree's
single-key-location model. LSM-tree's multi-segment structure makes range locking
and snapshot isolation operationally complex. PostgreSQL provides serializable
isolation, mature VACUUM tooling, and predictable p99 latency without compaction
stalls.

### What We're Giving Up
Write throughput ceiling is lower than LSM-tree at extreme scale. If the ledger
exceeds ~50K writes/sec, horizontal sharding or CockroachDB (distributed B-tree)
should be evaluated.
```

---

### Example 3: Product Catalog with In-Memory Consideration (Read-Heavy, Small Dataset)

**Scenario:** An e-commerce platform serves a product catalog of 2 million SKUs (approx. 8GB uncompressed). Reads are 95% of traffic (product page loads); writes are batch updates (nightly price refresh from suppliers). The dataset is small enough to fit in RAM on a 32GB server. The team wants sub-millisecond reads.

**Trigger:** "Should we put our product catalog in Redis for speed? Or keep it in PostgreSQL?"

**Process:**
- Step 1: Read-heavy (95% reads), point-lookup-dominant (product by SKU), latency-SLA-strict (sub-millisecond)
- Step 2: D3 read performance → in-memory=5; D1 write throughput → not important (nightly batch); D6 transactions → not required; D7 compaction risk → not a concern for in-memory
- Step 3: No disqualifiers for in-memory if nightly refresh process handles data loss on restart via rebuild. B-tree (PostgreSQL) is viable but slower for sub-ms reads.
- Step 4: N/A (in-memory selected)
- Step 5: Redis (with RDB snapshot for nightly rebuild on restart); PostgreSQL retained as source of truth for writes

**Output summary:**
```
## Storage Engine Recommendation

### Recommendation
Engine Family: In-memory (cache layer)
Primary Product: Redis
Architecture Pattern: Write-through cache — PostgreSQL is source of truth; Redis
serves reads; nightly batch job refreshes Redis from PostgreSQL.

### Why In-memory
8GB dataset fits in RAM. Sub-millisecond read SLA is achievable with Redis
(PostgreSQL with OS page cache typically serves at 1-5ms, not sub-millisecond).
Nightly batch writes are low-frequency and do not stress any storage engine.

### What We're Giving Up
Redis is not the source of truth. A Redis failure requires rebuilding from
PostgreSQL (nightly batch or on-demand rebuild, ~5-10 minute recovery time).
Do not store writes in Redis alone — all mutations go to PostgreSQL first.

### Durability Note
Configure Redis with RDB snapshots or AOF persistence if the 2-million-SKU
rebuild time on restart is unacceptable. Without persistence, a Redis restart
means serving reads from PostgreSQL until the cache warms.
```

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/scoring-guide.md` | Per-dimension scoring rubrics (1-5 scale) with worked examples for write-heavy, read-heavy, and mixed workloads; compaction strategy selection decision tree; workload-to-product routing table | When scoring Step 2 or selecting compaction in Step 4 |
| `references/engine-internals.md` | LSM-tree write path (memtable → WAL → SSTable → compaction), B-tree write path (WAL → page update → page split), in-memory durability patterns; Bloom filter mechanics; write amplification calculation method | When a deeper technical explanation is needed for a team discussion or ADR |
| `references/compaction-monitoring.md` | Cassandra compaction metrics (nodetool tpstats, cfstats), RocksDB compaction stats, write stall conditions, disk space headroom rules, alert thresholds | When LSM-tree is selected and operational guidance is needed |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
