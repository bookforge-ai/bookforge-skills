# Rebalancing Strategies

Detailed comparison of the three main rebalancing approaches, with configuration guidance and known failure modes.

---

## Why Not hash mod N

The naive approach to rebalancing is `partition = hash(key) mod N` where N is the number of nodes.

**The problem:** When N changes (a node is added or removed), the modulo result changes for nearly every key. If you had 10 nodes and add one (N = 11), `hash(key) mod 10` ≠ `hash(key) mod 11` for most keys — they all need to move. This makes rebalancing catastrophically expensive: adding a single node triggers a full data shuffle.

**The fix:** Assign each partition a fixed range of hash values (not a modulo). When a node is added, it takes over some partitions' hash ranges from existing nodes. Keys within a given hash range always map to the same partition; only the partition-to-node assignment changes, not the key-to-partition mapping.

---

## Strategy 1: Fixed Number of Partitions

**How it works:**
- Create many more partitions than nodes at initial setup. Common ratio: 10:1 to 100:1 (e.g., 1,000 partitions for a 10-node cluster).
- When a node is added: it steals a few complete partitions from every existing node until load is balanced.
- When a node is removed: its partitions are distributed to remaining nodes.
- Key-to-partition mapping never changes. Only partition-to-node assignment changes.
- Used by: Riak, Elasticsearch, Couchbase, Voldemort.

**Configuration:**
- Initial partition count: set at cluster creation, cannot be changed later in most fixed-partition databases.
- Rule of thumb: `initial_partitions = max_expected_nodes × 10`
- Elasticsearch: `number_of_shards` per index (set at index creation, immutable without reindex)
- Riak: `ring_size` (power of 2, set at cluster creation)

**When to choose:**
- Total data size is known and bounded — partition count can be sized correctly upfront.
- Operational simplicity is preferred — no dynamic splitting/merging to manage.
- Database supports it natively (Riak, Elasticsearch, Couchbase, Voldemort).

**Failure modes:**
- Too few partitions: limits maximum cluster size. A 10-partition cluster can never have more than 10 nodes effectively.
- Too many partitions: each partition has per-partition overhead (metadata, connections, background processes). Very high partition counts degrade performance.
- Data grows much larger than expected: partition size grows proportionally, making each partition very large and recovery from node failure very slow.

---

## Strategy 2: Dynamic Partitioning

**How it works:**
- Partitions split when they exceed a size threshold; they merge when they fall below a lower threshold.
- Partition count adapts to total data volume automatically.
- After a large partition splits, one of the two halves can be transferred to another node to balance load.
- Used by: HBase (default 10 GB threshold), RethinkDB, MongoDB (both hash and range modes).

**Configuration (HBase example):**
```
hbase.regionserver.region.split.policy = IncreasingToUpperBoundRegionSplitPolicy
hbase.hregion.max.filesize = 10737418240   # 10 GB — split threshold
```

**Pre-splitting (required for empty databases):**
An empty database starts with a single partition. All writes hit one node until the first split. For key-range partitioning, pre-splits require knowing the key distribution in advance.

```
# HBase: create a table with 10 pre-splits for known key prefixes
create 'sensor_data', 'readings', SPLITS => ['sensor01', 'sensor02', ..., 'sensor09']
```

For hash partitioning, MongoDB supports pre-splitting by hash value ranges.

**When to choose:**
- Data volume is highly variable or will grow significantly and unpredictably.
- Key-range partitioning is used (dynamic partitioning is the natural complement).
- The database natively supports it (HBase, RethinkDB, MongoDB).

**Failure modes:**
- Cold-start bottleneck: without pre-splitting, all early writes go to one partition/node.
- Split storms: a sudden data ingestion spike can trigger many rapid splits simultaneously, creating high I/O load on the splitting nodes.
- Pre-split key guessing: key-range pre-splits require knowing key distribution upfront, which may not be available for new systems.

---

## Strategy 3: Proportional to Nodes

**How it works:**
- Fixed number of partitions per node (Cassandra default: 256 vnodes per node).
- Total partition count = nodes × partitions_per_node.
- When a new node joins: it randomly selects existing partitions, splits them, and takes ownership of half of each split partition.
- Partition size stays roughly constant as nodes are added (more nodes = more partitions = same data per partition).
- Used by: Cassandra (virtual nodes / vnodes), Ketama.

**Configuration (Cassandra):**
```yaml
# cassandra.yaml
num_tokens: 256          # vnodes per node (partitions per node)
                         # Cassandra 3.0+: use vnodes for automatic load balancing
                         # Lower values (16, 32) reduce overhead but decrease balance quality
```

**Virtual nodes (vnodes):** Rather than assigning each node a single contiguous range of the hash space, each node owns many small non-contiguous ranges. This improves load distribution when nodes have heterogeneous capacity (a stronger node gets more vnodes). It also reduces the data movement needed when a node fails (failure load is spread across all other nodes, not just neighbors in the ring).

**When to choose:**
- Using Cassandra, Ketama, or a gossip-based ring system.
- Cluster will grow by adding nodes — partition size stays stable automatically.
- Hash partitioning is in use (proportional rebalancing requires hash-based boundary selection).

**Failure modes:**
- Unfair splits from randomization: with few partitions per node, random split selection can create unbalanced partition sizes. Cassandra 3.0 introduced a deterministic allocation algorithm to address this.
- New node join overhead: a new node must stream data from all nodes it takes partitions from, generating simultaneous I/O on multiple existing nodes.

---

## Automatic vs. Manual Rebalancing Decision

| Approach | Operational burden | Predictability | Risk |
|---|---|---|---|
| Fully automatic | Low — system handles all moves | Low — unpredictable timing | Rebalancing storm from false-positive failure detection |
| Semi-automatic (recommended) | Medium — operator approves proposed plan | High — operator sees full plan before execution | Delayed response to cluster changes |
| Fully manual | High — DBA configures partition assignment | High | Human error in assignment |

**Recommendation for production:** Use semi-automatic. The operator-approval step costs minutes but prevents the failure mode where a temporarily slow node triggers a rebalancing cascade that makes the situation worse.

Systems that support semi-automatic rebalancing: Couchbase, Riak, Voldemort (generate plan → operator commits → execution begins).
