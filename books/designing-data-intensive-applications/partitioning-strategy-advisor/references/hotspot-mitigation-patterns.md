# Hotspot Mitigation Patterns

Concrete patterns for detecting and relieving the most common partitioning hotspot types.

---

## Pattern 1: Monotonic Key Hotspot (Range Partitioning)

### Symptom
All writes are routed to a single partition — typically the "latest" one. Other partitions are idle. The affected partition's CPU and I/O are saturated while cluster utilization is very low overall.

### Root cause
The partition key is monotonically increasing: `created_at TIMESTAMP`, `id BIGSERIAL`, `event_sequence BIGINT`, `order_id INT AUTO_INCREMENT`. Range partitioning assigns contiguous key ranges to partitions. All new data falls in the highest range, and all current writes go to the partition holding that range.

### Mitigation: Compound prefix key

Prepend a high-cardinality, non-monotonic value to the key before the monotonic component.

**Before (bad):**
```
partition key: timestamp
range: 2024-01-01T00:00:00 → 2024-01-01T23:59:59  →  Partition 0
range: 2024-01-02T00:00:00 → 2024-01-02T23:59:59  →  Partition 1  ← ALL current writes
range: 2024-01-03T00:00:00 → ...                  →  Partition 2  ← empty
```

**After (good):**
```
partition key: (sensor_name, timestamp)
range: sensor_A, 2024-01-01 → sensor_A, 2024-01-03  →  Partition 0  ← sensor A writes
range: sensor_B, 2024-01-01 → sensor_B, 2024-01-03  →  Partition 1  ← sensor B writes
range: sensor_C, 2024-01-01 → sensor_C, 2024-01-03  →  Partition 2  ← sensor C writes
```

**Query impact:** To fetch all sensor readings within a time range (regardless of sensor), you must issue one range query per sensor prefix. This is an accepted trade-off. If you need a global time range query, consider a secondary index on `timestamp` or accept scatter/gather.

**Alternative prefix choices:** User ID, device ID, region code, category ID — any dimension with sufficient cardinality to spread load, which is also available at write time.

---

## Pattern 2: Monotonic Key Hotspot (Hash Partitioning on Sequential IDs)

### Symptom
Hash partitioning is in use, but a new auto-increment ID or UUID-v1 (time-based) is the key. With UUID-v1, the time component is in the high-order bits and produces similar hash values for keys created at the same time, clustering them in the same partition.

### Root cause
UUID-v1 and ULID encode timestamp in a way that may produce sequential values over short intervals, partially defeating hash partitioning.

### Mitigation
- Use UUID-v4 (random) as the partition key — fully random hash distribution.
- Use ULID but reverse the timestamp component to distribute writes: `timestamp_reversed + random_component`.
- Use application-generated random IDs rather than database-generated sequential IDs.
- If you must retain sequential IDs for business reasons, use a hash of the sequential ID as the partition key (not the ID itself), and store the original ID as a separate non-partitioning column.

---

## Pattern 3: Celebrity Key Hotspot (Hash Partitioning)

### Symptom
One or a few specific keys receive orders of magnitude more traffic than all others. Hash partitioning distributes keys evenly in aggregate, but the hot keys are each still concentrated in a single partition. The partition containing the celebrity key is overloaded; others are not.

### Root cause
The partitioning is correct, but the data distribution is inherently skewed: a celebrity user, a viral post, a globally-shared resource (e.g., a global counter, a shared cart, a trending topic ID). Hashing cannot help — `hash(celebrity_key)` is still a single value.

### Mitigation: Write-time key salting

Append a random suffix (00–99) to hot keys at write time, spreading one logical key across 100 physical keys.

**Write:**
```python
import random

def write_celebrity_key(db, key, value):
    # Only apply to known-hot keys
    if is_hot_key(key):
        suffix = random.randint(0, 99)
        physical_key = f"{key}_{suffix:02d}"
    else:
        physical_key = key
    db.write(physical_key, value)
```

**Read:**
```python
def read_celebrity_key(db, key):
    if is_hot_key(key):
        # Must read all 100 suffix variants and merge
        results = []
        for i in range(100):
            physical_key = f"{key}_{i:02d}"
            results.append(db.read(physical_key))
        return merge(results)
    else:
        return db.read(key)
```

**Bookkeeping:** Maintain a lookup table (or application config) of which keys are "hot" so that the salting and merge logic is applied selectively. Applying it to all keys is unnecessary overhead for the vast majority that are not hot.

**Trade-off:** Reads on hot keys now require fetching 100 records and merging. This is acceptable when writes vastly outnumber reads for the hot key, or when the merge is simple (e.g., summing a counter across suffix partitions).

### Alternative: Application-level sharding for celebrity resources

For resources like a global counter or a shared leaderboard that receive extreme write volume, use application-level partitioned counters:

- Maintain N counter shards in the application layer.
- Each write randomly increments one shard.
- To read the total, sum all N shards.
- N can be tuned based on write throughput requirements.

---

## Pattern 4: Write Skew from Unbalanced Partition Boundaries

### Symptom
Some partitions are very large; others are nearly empty. This occurs most often with range partitioning where partition boundaries were chosen based on assumed key distribution that did not match actual data.

### Root cause
In range partitioning, partition boundaries must match the actual data distribution, not an assumed uniform distribution. For example, partitioning a name field alphabetically with equal letter ranges (A–B, C–D, E–F, ...) will produce very unequal partitions because letters do not appear with equal frequency.

### Mitigation
- Use dynamic partitioning (HBase, RethinkDB, MongoDB): boundaries adapt automatically based on actual data volume.
- If using fixed boundaries, analyze actual key distribution before setting boundaries. HBase supports pre-splitting with custom split points derived from a key distribution analysis.
- Use hash partitioning if range queries are not required — hash partitioning produces near-uniform distribution regardless of key distribution.

---

## Detection: How to Identify Hotspots Before They Cause Outages

**Metrics to monitor per partition:**
- Write requests/second per partition (look for orders-of-magnitude differences)
- Storage size per partition (look for one partition growing much faster)
- CPU and I/O utilization per node (hotspot node will be saturated)

**Query to identify hot partition in Cassandra:**
```bash
nodetool tpstats           # Thread pool stats — saturated pools on one node
nodetool cfhistograms      # Per-table latency and request histograms
nodetool tablestats        # Per-table metrics including partition size
```

**Query to identify hot shards in Elasticsearch:**
```bash
GET _cat/shards?v&s=store   # Shards sorted by store size
GET _nodes/stats/indices    # Per-node indexing/search rate
```

**Signal:** If one partition/shard/node shows 10x or more the request rate or storage of others, a hotspot is present.
