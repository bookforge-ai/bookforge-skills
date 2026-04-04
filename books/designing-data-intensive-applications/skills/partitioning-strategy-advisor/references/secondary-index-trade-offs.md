# Secondary Index Trade-offs: Local vs. Global

This reference covers the detailed trade-off analysis between document-partitioned (local) and term-partitioned (global) secondary indexes in a partitioned database.

---

## The Core Problem

Secondary indexes identify records by attributes that are not the partition key. Because the partition key determines which node holds a record, a secondary index on a different attribute spans all partitions — records with a given attribute value may exist in every partition.

There is no way to partition both the primary data and the secondary index by the same key simultaneously. Every secondary index strategy involves a trade-off between write complexity and read complexity.

---

## Document-Partitioned (Local) Index

### Architecture

Each partition maintains its own secondary index, containing entries only for documents stored in that partition.

```
Partition 0                          Partition 1
PRIMARY DATA                         PRIMARY DATA
 product_id=191  color=red            product_id=515  color=silver
 product_id=214  color=black          product_id=768  color=red
 product_id=306  color=red            product_id=893  color=silver

LOCAL SECONDARY INDEX                LOCAL SECONDARY INDEX
 color:red   → [191, 306]             color:red   → [768]
 color:black → [214]                  color:silver → [515, 893]
```

### Write path
A write to `product_id=191` goes to Partition 0. Only Partition 0 updates its local index. No other partition is involved.

### Read path
A query for `color=red` must be sent to Partition 0 AND Partition 1 (scatter), wait for both to respond, then merge the results (gather). With N partitions, the query fans out to all N partitions.

### Tail latency amplification
Scatter/gather means the query's latency is determined by the slowest partition's response. With 20 partitions, the query is as slow as the slowest of 20 responses. Adding partitions worsens this unless all partitions are identical in performance.

### When to choose local indexes
- Writes are frequent and write latency is critical.
- Secondary index queries are infrequent or can tolerate higher latency.
- Secondary index queries are structured so they can be scoped to a single partition (e.g., always filter by tenant_id first, and data is partitioned by tenant_id — so the secondary index query hits only one partition).
- The database of choice uses local indexes by default and you cannot change it (MongoDB, Cassandra, Elasticsearch, SolrCloud, Riak, VoltDB).

### Mitigation for scatter/gather cost
- Reduce partition count (fewer partitions = less scatter). Over-sharding (e.g., 500 shards for a dataset that fits in 20) amplifies scatter/gather with no benefit.
- Ensure secondary index queries always include the partition key as a filter, so the query can be routed to a single partition.
- Precompute frequently used aggregate queries (materialized views, denormalized rollup tables) instead of relying on secondary index scatter/gather for high-frequency queries.

---

## Term-Partitioned (Global) Index

### Architecture

A single global index covers all partitions, but the index itself is partitioned by the indexed term (or a hash of the term).

```
Global Index Partition 0              Global Index Partition 1
(terms a–r)                           (terms s–z)
 color:black → [191, 515]             color:silver → [515, 893]
 color:red   → [191, 306, 768]        make:Volvo   → [768]
 make:Audi   → [893]
 make:Dodge  → [214]
 make:Ford   → [306, 515]
 make:Honda  → [191]
```

The primary data is still partitioned by `product_id`. The global index is separately partitioned by the indexed attribute value.

### Write path
A write to `product_id=191` (color=red, make=Honda):
- Updates primary data in the `product_id` partition (e.g., Partition 0)
- Must also update `color:red` in Global Index Partition 0
- Must also update `make:Honda` in Global Index Partition 0

A single write now touches multiple partitions (the data partition + all relevant index partitions). In a term-partitioned global index, writes require distributed transactions across partitions — not supported by all databases, so global secondary indexes are often updated **asynchronously**.

### Read path
A query for `color=red` goes to exactly one global index partition (the one covering terms starting with "r"). That partition returns the full list of matching document IDs from all primary partitions. The query can then fetch the actual documents, potentially with targeted lookups to specific primary partitions.

### Asynchronous index updates
Because requiring synchronous updates across multiple index partitions would need distributed transactions, most global secondary index implementations update asynchronously. Amazon DynamoDB's global secondary indexes are normally updated within a fraction of a second, but may lag during infrastructure faults.

**Implication:** If you read the global index immediately after a write, the change may not yet be reflected. Design applications that use global secondary indexes to tolerate brief eventual consistency in index reads.

### Global index partition strategy
- **Range-partitioned term index:** Terms are assigned to partitions by sorted ranges. Supports range queries on the indexed attribute (e.g., price between 100 and 500). Used when the indexed attribute has range-query requirements.
- **Hash-partitioned term index:** Terms are assigned to partitions by hash of the term. More uniform load distribution. No range scan support on the index itself.

### When to choose global indexes
- Secondary index reads are frequent and latency-sensitive.
- Writes are less frequent or can tolerate asynchronous propagation.
- The application can tolerate eventual consistency in secondary index reads.
- The database supports global secondary indexes (DynamoDB, Oracle, Riak search feature).

---

## Comparison Summary

| Dimension | Local (Document-Partitioned) | Global (Term-Partitioned) |
|---|---|---|
| Write cost | Low — single partition update | High — multiple index partitions updated |
| Write consistency | Synchronous, always up-to-date | Often asynchronous — brief eventual consistency |
| Read cost (secondary index query) | High — scatter/gather all partitions | Low — single index partition |
| Read tail latency | Amplified by partition count | Stable — single partition |
| Operational complexity | Low — no separate index management | Higher — global index is a separate partitioned structure |
| Databases | MongoDB, Cassandra, Elasticsearch, Riak, VoltDB | DynamoDB global secondary indexes, Oracle, Riak search |

---

## Hybrid Pattern: Co-location to Avoid Secondary Index

In some cases, secondary index overhead can be eliminated entirely by redesigning the partition key to co-locate records that will be queried together.

**Pattern:** If secondary index queries always filter by a high-cardinality attribute (e.g., `tenant_id`, `store_id`, `user_id`), partition the primary data by that attribute. Secondary index queries within a tenant are now single-partition lookups — no scatter/gather, no global index needed.

**Trade-off:** This works only when secondary index queries are always scoped to the partition key value. If global cross-partition secondary index queries are also needed, co-location does not eliminate the scatter/gather requirement for those queries.
