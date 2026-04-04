# Join Strategy Reference

Detailed decision criteria, size thresholds, and skew handling patterns for batch pipeline joins.

## The Three Join Strategies at a Glance

| Strategy | Also called | Where join logic runs | Input requirements | Best for |
|----------|-------------|----------------------|-------------------|----------|
| Sort-merge join | Reduce-side join | Reducer | No assumptions | Default; both datasets large |
| Broadcast hash join | Map-side join (replicated) | Mapper | One dataset fits in memory | One small + one large dataset |
| Partitioned hash join | Bucketed map join (Hive) | Mapper | Both co-partitioned identically | Both datasets large, same partitioning |

---

## Strategy 1: Sort-Merge Join (Reduce-Side)

### How it works

1. **Map phase:** Both input datasets go through mappers. Each mapper extracts the join key and emits `(join_key, record)` pairs. Records from dataset A and dataset B both emit using the same join key.
2. **Shuffle/sort phase:** The framework partitions mapper output by join key (using hash-of-key to assign to a reducer partition) and sorts within each partition. All records with the same join key — from both datasets — arrive at the same reducer, adjacent in sort order.
3. **Reduce phase:** The reducer iterates over all records with a given key. Using a secondary sort (dataset A records before dataset B records, or vice versa), the reducer can hold one dataset's record in memory while streaming the other, rather than buffering everything. The reducer outputs joined records.

### Secondary sort technique

Secondary sort arranges records so that the "small side" of the join (e.g., one profile record per user) arrives first. The reducer stores this record in a local variable, then iterates through "large side" records (e.g., many activity events per user) emitting a joined output for each. This keeps memory usage constant — only one record from the small side is held at a time.

### Size thresholds

- Both datasets can be arbitrarily large.
- Network and disk I/O scale with total data volume. Budget 2-3x the input data size for shuffle traffic.
- Optimize by filtering and projecting early in the map phase to reduce shuffle volume.

### When to use

- Default choice when dataset sizes are unknown or both are large (> a few GB each).
- When no assumptions can be made about data partitioning.
- When the join key is not known in advance to be uniformly distributed (safe starting point; add skew handling if needed).

### Cost profile

- Expensive: full shuffle of both datasets over the network, full sort.
- Reducer start is delayed until all mappers for both datasets have finished.
- Intermediate data is written to local disk on each mapper, then transferred to reducers.

---

## Strategy 2: Broadcast Hash Join (Map-Side, Small Table)

### How it works

1. Before map tasks start, the small dataset is loaded from the distributed filesystem into each mapper's memory as a hash table (keyed by join key).
2. Each mapper reads one block of the large dataset and, for each record, looks up the join key in the in-memory hash table.
3. The mapper emits joined records directly. No reducer needed. No shuffle.

### Size thresholds

- Small table must fit in memory on each mapper (including other mapper state and JVM overhead).
- Practical limits: 1-4 GB per mapper is typical. Check executor memory configuration.
- If the small table is larger than memory but can fit on local disk, some implementations (Pig "replicated join", Hive "MapJoin") can use a local disk index with OS page cache to achieve near-memory performance.

### Multi-way broadcast joins

If multiple small tables need to be joined with one large table, all small tables can be broadcast simultaneously. Each mapper loads all small tables at startup. This is efficient as long as the total memory footprint of all small tables stays within the mapper's memory budget.

### Supported in

- Pig: "replicated join"
- Hive: "MapJoin" (also auto-detected by Hive optimizer when table is below `hive.mapjoin.smalltable.filesize`)
- Cascading, Crunch: broadcast join operators
- Spark: `broadcast()` hint on small DataFrame; optimizer uses `BroadcastHashJoin`
- Impala: used by default for small tables in analytic queries

### When to use

- One dataset is clearly small (user profile DB, product catalog, lookup table) and the other is large (event log, transaction history).
- When small table is frequently joined with many large datasets (load once, reuse across multiple map tasks).

### When NOT to use

- Small table grows beyond memory budget — switch to sort-merge join.
- Multiple large-large joins — broadcast only one side; the other must be shuffled.

---

## Strategy 3: Partitioned Hash Join (Map-Side, Co-Partitioned)

### How it works

Both datasets must be partitioned using the same key, the same hash function, and the same number of partitions. This is the "co-partitioned" or "bucketed" property.

1. Mapper N reads partition N of the large dataset.
2. Mapper N also loads partition N of the small dataset into memory (only partition N, not the full dataset).
3. Mapper N performs a hash join between the two partitions locally. No shuffle or reducer needed.

Because the co-partitioning guarantee means that any record in partition N of dataset A can only match records in partition N of dataset B, each mapper handles a fully independent subset of the join problem.

### Size thresholds

- Neither dataset needs to fit entirely in memory — only one partition at a time.
- Memory requirement: (total small dataset size) / (number of partitions).
- With 1000 partitions and a 100 GB small dataset: each mapper loads 100 MB. Very manageable.
- Large dataset can be arbitrarily large as long as one partition fits in local disk.

### Prerequisites

Co-partitioning is a strong prerequisite. The datasets must:
- Be partitioned by the same join key (e.g., both partitioned by `user_id`)
- Use the same hash function
- Have the same number of partitions

This is most naturally satisfied when both datasets were produced by prior MapReduce jobs with the same output partitioning scheme. The partitioning metadata (key, function, partition count) must be tracked — Hadoop ecosystem uses HCatalog / Hive metastore for this.

### Known as

- Hive: "bucketed map join"
- General: "co-partitioned hash join", "partition hash join"

### When to use

- Both datasets are large, but one is smaller than the other.
- Both datasets were produced by prior pipeline stages that happen to partition by the join key.
- The join key is the same as the partitioning key already in use.

### When NOT to use

- Datasets are partitioned by different keys, different hash functions, or different partition counts — co-partitioning guarantee does not hold.
- One dataset is small enough for broadcast hash join (strategy 2 is simpler and faster).

---

## Map-Side Merge Join (Bonus Variant)

If both datasets are not only co-partitioned but also **sorted by the join key within each partition**, a mapper can perform a merge join by reading both partition files incrementally in ascending key order and matching records with the same key — exactly like the merge step of a merge sort.

This requires no in-memory hash table, making it suitable for very large partitions. It works like the reduce phase of a sort-merge join but runs in a mapper (no shuffle required).

This situation often arises naturally if the datasets were produced by prior sort-merge join outputs (which are partitioned and sorted by definition).

---

## Skew Handling Patterns

### When to suspect skew

- A social network with celebrity accounts
- Content platforms with viral items (a single video_id with 10x the events of the average)
- Natural language data (stop words like "the", "a" as join keys)
- Time-partitioned data where some time windows have disproportionate traffic

### Detecting skew

Run a preliminary sampling job (or query the dataset statistics if available) to estimate the top-N key frequencies. If the top key has 10x the frequency of the median key, skew handling is warranted.

### Pattern 1: Skewed Join (Pig)

1. **Sampling job:** Scan a sample of the large dataset to identify hot keys.
2. **Hot key handling:** Records with hot keys are sent to a randomly chosen subset of reducers (spreading the load). Records from the other dataset for those hot keys must be replicated to all reducers handling that key.
3. **Cold key handling:** Standard sort-merge join.

Cost: data for hot-key matching side is replicated (increases network volume). Benefit: the hot-key reducer becomes a set of reducers, eliminating the straggler.

### Pattern 2: Sharded Join (Crunch)

Same approach as skewed join but hot keys are specified explicitly by the developer rather than discovered by sampling. Requires domain knowledge of which keys are hot.

### Pattern 3: Two-Stage Aggregation for GROUP BY Skew

When grouping by a hot key (not joining), a two-stage approach avoids the straggler reducer:

1. **Stage 1:** Each mapper sends records to a randomly chosen reducer (not the canonical hash-of-key reducer). Each reducer computes a partial aggregate for its subset of records.
2. **Stage 2:** The partial aggregates for each key (now much smaller in volume) are sent to the canonical reducer for final aggregation.

This is only correct for commutative, associative aggregations (sum, count, min, max). It is not correct for median or other order-dependent aggregations.

### Hive skewed join optimization

Hive's approach: hot keys are declared in the table metadata. Records for hot keys are stored in separate files. At join time, the hot-key records are processed using a broadcast hash join (map-side) while cold-key records use a standard sort-merge join. The join strategy is automatically selected per-key based on the metadata.

---

## Join Output and Downstream Partitioning

The join strategy affects the output's partitioning, which matters for downstream pipeline stages:

- **Sort-merge join output:** Partitioned and sorted by the join key (reducer output). Downstream stages that need the data sorted by join key can skip re-sorting.
- **Broadcast hash join output:** Partitioned the same way as the large input dataset (since one map task per block of the large input). Not sorted by join key.
- **Partitioned hash join output:** Partitioned the same way as both input datasets.

Knowing the output partitioning of each stage enables downstream stages to choose faster join strategies (e.g., if the sort-merge output is already sorted, the next join on the same key can use a map-side merge join).
