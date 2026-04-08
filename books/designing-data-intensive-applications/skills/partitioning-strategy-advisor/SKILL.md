---
name: partitioning-strategy-advisor
description: |
  Select the right partitioning (sharding) strategy — range, hash, or compound key — and configure secondary indexes, rebalancing, and request routing for a distributed database. Use when: designing a partition key for a new system; diagnosing write hotspots on monotonically increasing keys (timestamps, auto-increment IDs); evaluating whether an existing sharding scheme supports required query patterns; choosing between document-partitioned (local) vs. term-partitioned (global) secondary indexes and weighing scatter/gather read costs against global index write amplification; or selecting a rebalancing approach (fixed partitions, dynamic partitions, proportional-to-nodes) and routing topology (gossip, ZooKeeper coordination, partition-aware client). Covers Cassandra compound primary key patterns for range queries within hash-distributed partitions, HBase/SSTables range partitioning, Riak consistent hashing, and MongoDB/Elasticsearch index partitioning. Distinct from replication-strategy-selector (topology and consistency) and data-model-selector (schema design). Produces a concrete recommendation: partition key, partitioning method, secondary index approach, rebalancing configuration, and routing topology. Depends on data-model-selector for schema and access pattern context.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/partitioning-strategy-advisor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - data-model-selector
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [6]
tags:
  - partitioning
  - sharding
  - range-partitioning
  - hash-partitioning
  - compound-key
  - hotspot
  - skew
  - secondary-index
  - local-index
  - global-index
  - document-partitioned-index
  - term-partitioned-index
  - scatter-gather
  - rebalancing
  - dynamic-partitioning
  - fixed-partitions
  - proportional-partitioning
  - consistent-hashing
  - request-routing
  - zookeeper
  - gossip-protocol
  - cassandra
  - hbase
  - mongodb
  - riak
  - elasticsearch
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application codebase, docker-compose, database schema files, or architecture description that reveals data access patterns, query patterns, and write volume characteristics"
    - type: document
      description: "System requirements document or architecture description if no codebase is available"
  tools-required: [Read, Write, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Run inside a project directory with codebase or configuration files. Falls back to document/description input."
discovery:
  goal: "Produce a concrete partitioning recommendation: partition key, partitioning method, secondary index approach, rebalancing configuration, and request routing topology"
  tasks:
    - "Identify the primary data entity and its natural access key"
    - "Classify the data distribution risk (monotonic keys, celebrity keys, uniform keys)"
    - "Select partitioning method: range, hash, or compound"
    - "Assess secondary index requirements and select local vs. global indexing"
    - "Select rebalancing approach: fixed, dynamic, or proportional-to-nodes"
    - "Select request routing approach: gossip, coordination service, or partition-aware client"
    - "Document hotspot risks and mitigation strategies"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "site-reliability-engineer", "tech-lead"]
    experience: "intermediate-to-advanced — assumes experience with distributed databases and data modeling"
  triggers:
    - "User is designing a partitioning scheme for a new distributed database deployment"
    - "User is experiencing write hotspots or uneven partition load"
    - "User needs efficient range queries on a hash-partitioned database"
    - "User is choosing between local and global secondary indexes"
    - "User is configuring rebalancing for a growing cluster"
    - "User is evaluating whether their sharding key causes skew"
    - "User is deciding how to route requests to the correct partition"
  not_for:
    - "Choosing a replication topology — use replication-strategy-selector"
    - "Selecting a storage engine or data model — use storage-engine-selector or data-model-selector"
    - "Diagnosing distributed system failures — use distributed-failure-analyzer"
---

# Partitioning Strategy Advisor

## When to Use

You are designing or evaluating a distributed database where data must be spread across multiple nodes (sharding) and need to select a partitioning key, a partitioning method, secondary index approach, rebalancing configuration, and request routing topology.

This skill applies when the partitioning scheme is open (new system), problematic (existing system with hotspots or unsupported query patterns), or needs documented justification (architecture decision record, team alignment). It produces a concrete recommendation covering partition key choice, range vs. hash vs. compound method, secondary index strategy, rebalancing approach, and routing topology.

**Prerequisite check:**
- If you haven't selected a data model (relational, document, graph) for your system, run `data-model-selector` first — partitioning key design depends on the schema and access patterns that the data model determines.
- If you are also designing replication across nodes, run `replication-strategy-selector` after this skill — partitioning and replication are largely independent choices, but the replication factor affects partition sizing.
- If you need to diagnose hotspots or routing failures in a live production system, use `distributed-failure-analyzer` for root-cause analysis after using this skill to select the corrected strategy.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

**1. Primary access pattern — how records are most frequently looked up**

Why: The access pattern determines what the partition key must be. If records are always looked up by a single primary key (user ID, order ID), hashing that key achieves even distribution. If records are frequently fetched in sorted ranges (sensor readings by time, events by date), range partitioning on that key enables efficient range scans. Choosing the wrong key forces scatter/gather reads or hot single partitions on every query.

- Check prompt for: "look up by", "query by", "fetch all records for", "time-series", "range query", "primary key is"
- Check environment for: schema.sql (PRIMARY KEY, index definitions), application code (WHERE clauses, query methods), architecture.md (data access descriptions)
- If still missing, ask: "How does your application most frequently look up records? By a single ID, by a range of values (e.g., date range), or by filtering on secondary attributes (e.g., color, status)?"

**2. Write distribution characteristics — is the natural key monotonically increasing?**

Why: Monotonically increasing keys (timestamps, auto-increment IDs, sequential order numbers) create sequential write patterns that concentrate all writes on the latest partition in range partitioning. This is the most common hotspot source. Even under hash partitioning, extremely popular individual keys (celebrity users, viral content IDs) can overwhelm a single partition. Understanding write distribution is required before selecting a partition key.

- Check prompt for: "timestamp", "created_at", "auto-increment", "sequential ID", "time-series writes", "celebrity", "viral", "high-traffic key"
- Check environment for: schema.sql (SERIAL, AUTO_INCREMENT, TIMESTAMP columns as primary keys), application code (INSERT patterns, event ingestion pipelines)
- If still missing, ask: "Does your most common write operation use a key that increases sequentially (like a timestamp or auto-increment ID)? And are any individual records likely to receive dramatically more writes than others (e.g., a popular user or trending item)?"

**3. Secondary query requirements — does the application filter on non-primary-key attributes?**

Why: Secondary indexes on partitioned data require a choice between document-partitioned (local) and term-partitioned (global) indexes. This choice forces a fundamental trade-off: local indexes are cheap to write (only the local partition is updated) but expensive to read (scatter/gather across all partitions). Global indexes are cheap to read (single partition lookup) but expensive to write (updates span multiple partition index entries, often asynchronously). You must know which queries are required before designing the index strategy.

- Check prompt for: "filter by", "search by color", "find all users where", "full-text search", "secondary index", "non-primary attribute lookup"
- Check environment for: schema.sql (CREATE INDEX, secondary index definitions), application code (multi-attribute WHERE clauses), architecture.md (search or filter requirements)
- If still missing, ask: "Does your application need to query records by attributes other than the primary key — for example, filtering orders by status, searching products by category, or looking up users by email?"

**4. Data volume and growth trajectory**

Why: Affects rebalancing strategy selection. If total data volume is small and known, a fixed number of partitions sized correctly upfront is simplest. If data will grow significantly over time, dynamic partitioning (split/merge) adapts partition count automatically. If the cluster will scale out by adding nodes, proportional-to-nodes partitioning keeps partition size stable. Choosing a fixed partition count that's too small locks out future growth; too large creates excessive overhead.

- Check prompt for: "expected data size", "TB", "GB", "millions of records", "growing fast", "scaling out", "adding nodes"
- Check environment for: docker-compose (volume mounts, sizing comments), requirements.md (capacity planning), architecture.md (growth estimates)
- If still missing, ask: "Roughly how much data will this system store now, and how is it expected to grow over the next 1–2 years? Will you be adding database nodes as it grows?"

**5. Target database**

Why: Different databases implement partitioning in fundamentally different ways — HBase and RethinkDB use dynamic key-range partitioning; Cassandra and Riak use hash partitioning with proportional-to-nodes rebalancing; Elasticsearch uses fixed-partition hash sharding; MongoDB supports both. The recommendation must fit what the target database actually supports. Additionally, Cassandra's compound primary key pattern is only available in Cassandra.

- Check prompt for: database names (Cassandra, HBase, MongoDB, DynamoDB, Riak, Elasticsearch, PostgreSQL with Citus, etc.)
- Check environment for: docker-compose (image names), requirements.md (technology constraints), package files (database drivers)
- If still missing, ask: "Which database are you partitioning? (e.g., Cassandra, HBase, MongoDB, DynamoDB, Elasticsearch, or a custom partitioning layer on top of another store)"

### Optional Context (enriches recommendation)

- **Consistency requirements under rebalancing:** If the system requires zero-downtime rebalancing with continued read/write availability, manual-approval rebalancing (Couchbase, Riak, Voldemort model) is safer than fully automatic.
- **Request routing constraints:** If the system cannot depend on an external coordination service like ZooKeeper, gossip-based routing (Cassandra, Riak) or partition-aware client libraries are required.
- **Read/write ratio:** Heavily read-dominated workloads benefit more from global (term-partitioned) secondary indexes; heavily write-dominated workloads benefit from local (document-partitioned) secondary indexes.

---

## Process

### Step 1 — Classify Data Distribution Risk

Categorize the workload's skew profile before selecting any partitioning method.

**Why:** Partitioning is only useful if load is evenly distributed. A poorly chosen partition key can negate all the benefits of horizontal scaling by concentrating all reads or writes on one node (a hotspot). Identifying skew risk upfront determines whether extra mitigation (key prefixing, salting, compound keys) is needed on top of the base partitioning method.

Classify into one of three profiles:

| Profile | Signal | Risk |
|---|---|---|
| **Monotonic key** | Timestamps, sequential IDs, auto-increment PKs | All writes go to the single "latest" partition under range partitioning |
| **Celebrity key** | A small number of keys receive orders of magnitude more traffic (viral content, celebrity users) | Single partition overloaded even under hash partitioning |
| **Uniform key** | Random UUIDs, user IDs with no natural ordering, hashed values | Low hotspot risk; both range and hash partitioning are viable |

**Mitigation for monotonic keys (range partitioning):** Prefix the timestamp with a high-cardinality dimension (e.g., sensor name + timestamp, or user ID + timestamp). This distributes writes across the key space while preserving range-scan ability within each prefix bucket.

**Mitigation for celebrity keys (hash partitioning):** Append a two-digit random suffix (00–99) to the hot key at write time. This splits writes across 100 partitions. Reads must then query all 100 suffix variants and merge — track which keys are "hot" in a separate lookup table to apply this only where needed.

### Step 2 — Select Partitioning Method

Choose range partitioning, hash partitioning, or compound key (hybrid) based on access patterns and skew profile.

**Why:** This is the central decision. Range partitioning preserves sort order, enabling efficient range scans but requiring careful key design to avoid hotspots. Hash partitioning destroys sort order (making range queries require scatter/gather) but distributes load evenly. Compound keys (Cassandra model) combine both — hashing on the first part distributes across partitions, sorting within the partition on the remaining parts supports range scans within a single partition.

**Decision framework:**

```
PRIMARY ACCESS PATTERN
├── Range queries are critical (fetch records within a time window,
│   scan sorted ranges, support range-based pagination)
│   ├── Key is monotonically increasing → RANGE with prefix mitigation
│   │   Example: (sensor_name, timestamp) compound range key
│   └── Key has natural, non-monotonic distribution → RANGE partitioning
│       Example: alphabetically distributed last names (encyclopedia volumes)
│
├── Point lookups dominate (fetch a single record by ID) AND
│   range queries are not needed
│   → HASH partitioning
│   Example: user profiles by user_id, order records by order_id
│
└── Point lookups on partition key AND range queries within that key
    → COMPOUND KEY (hash partition key + range sort key)
    Example: (user_id [hash], update_timestamp [range]) in Cassandra
    → Efficiently fetch all updates for a user, sorted by time,
       in a single partition lookup
```

**Range partitioning:** Used by Bigtable, HBase, RethinkDB, MongoDB (pre-2.4). Partition boundaries must adapt to data distribution — automatic boundary management (dynamic partitioning) is strongly preferred over manually configured boundaries to avoid under/over-filled partitions.

**Hash partitioning:** Used by Cassandra, Riak, Voldemort, MongoDB (hash mode). The hash function must be stable across processes — language-native hash functions (Java's `Object.hashCode()`, Ruby's `Object#hash`) are not safe for this purpose because they can return different values in different processes. Use a purpose-built stable function: Cassandra and MongoDB use MD5, Voldemort uses Fowler-Noll-Vo. Assign each partition a range of hash values (not `hash mod N` — see rebalancing step).

**Compound key (Cassandra):** The partition key (first component) is hashed to determine the partition. The clustering columns (remaining components) determine sort order within the partition. A query that fixes the partition key can perform an efficient range scan over the clustering columns without touching other partitions. This is the primary pattern for one-to-many relationships in Cassandra: `(user_id, post_timestamp)` stores all posts for a user in one partition, sorted by time.

### Step 3 — Design the Secondary Index Strategy

If the application requires queries on non-primary-key attributes, choose between document-partitioned (local) and term-partitioned (global) secondary indexes.

**Why:** Secondary indexes do not map cleanly to partitions. The choice of local vs. global index makes a fundamental trade-off between write cost and read cost that cannot be undone without a full reindex. Making this decision explicitly — and documenting it — prevents later surprises when a secondary index query turns out to require scatter/gather across every partition in the cluster.

**Document-partitioned (local) index:**
- Each partition maintains its own secondary index covering only the documents in that partition.
- Write: only the partition being written must be updated. Fast, local, no cross-partition coordination.
- Read: a secondary index query must be sent to all partitions and results merged (scatter/gather). Tail latency amplification — the query takes as long as the slowest partition.
- Used by: MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud, VoltDB.
- Choose when: writes are frequent and latency-sensitive; read queries on secondary indexes are acceptable to be slower; secondary index queries usually target a single partition (structured such that the secondary query attribute correlates with the partition key).

**Term-partitioned (global) index:**
- A single global index covers all partitions, but is itself partitioned (by the indexed term or a hash of the term).
- Read: a secondary index query hits a single index partition — fast, no scatter/gather.
- Write: a single document write may need to update index entries spread across multiple index partitions. Updates are typically asynchronous (DynamoDB global secondary indexes update within a fraction of a second normally, but with potential delays under faults).
- Used by: Amazon DynamoDB (global secondary indexes), Riak's search feature, Oracle data warehouse.
- Choose when: secondary index read frequency and latency are critical; writes are less frequent or can tolerate asynchronous index propagation; consistency requirements can accept eventually-consistent secondary indexes.

**Index partition boundary choice (for global indexes):**
- Range-partitioned term index: supports range scans on the indexed attribute (e.g., price ranges).
- Hash-partitioned term index: more uniform load distribution, no range scan support on the index.

### Step 4 — Select Rebalancing Approach

Choose fixed-partition, dynamic, or proportional-to-nodes rebalancing.

**Why:** As data grows and nodes are added or removed, partitions must be redistributed. The rebalancing strategy determines how disruptive this is, how much data moves, and how much operational overhead it requires. Using `hash mod N` — the naive approach — is explicitly wrong: it causes the vast majority of keys to move when N changes, making rebalancing catastrophically expensive.

**Fixed number of partitions:**
- Create many more partitions than nodes at setup (e.g., 1,000 partitions for a 10-node cluster = ~100 partitions/node).
- When a node is added, it steals a few partitions from every existing node. Only entire partitions move; no keys are remapped.
- Partition count is fixed at creation time. Choose it high enough to accommodate maximum expected cluster size.
- Operationally simple. Used by Riak, Elasticsearch, Couchbase, Voldemort.
- Risk: if data size is highly variable, partition size grows proportionally to total data, making very large partitions expensive to rebalance and recover from failure.

**Dynamic partitioning:**
- Partitions split when they exceed a configured size threshold (HBase default: 10 GB); partitions merge when they shrink below a lower threshold.
- Partition count adapts to data volume: small datasets use few partitions (low overhead), large datasets use many.
- Requires pre-splitting on an empty database (pre-splitting) — without it, all writes initially hit a single partition until the first split.
- Used by HBase, RethinkDB. MongoDB supports both dynamic and fixed partitioning.
- Choose when: data volume is highly variable or expected to grow significantly; range-partitioned databases where fixed boundaries would be very wrong.

**Proportional to nodes:**
- Fixed number of partitions per node (Cassandra default: 256 per node).
- When a node is added, it randomly splits existing partitions and takes half of each split.
- Partition size remains stable as the cluster grows because adding nodes also increases partition count.
- Used by Cassandra and Ketama. Requires hash-based partitioning (partition boundaries are drawn from the hash space).
- Choose when: using Cassandra or a gossip-based hash-partitioned system; cluster will scale out by adding nodes.

**Automatic vs. manual rebalancing:**
- Fully automatic: the system decides when and how to move partitions, without operator intervention. More convenient but unpredictable — a node that is temporarily slow may be misidentified as dead, triggering rebalancing that adds load to the already-overloaded node, potentially causing cascading failure.
- Semi-automatic (recommended for production): the system generates a suggested rebalancing plan, but an operator must approve it before it executes. Used by Couchbase, Riak, Voldemort.
- Fully manual: an administrator configures partition assignment explicitly.
- **Recommendation:** Use semi-automatic rebalancing in production. The human-in-the-loop prevents rebalancing storms triggered by false-positive failure detection.

### Step 5 — Select Request Routing Approach

Choose how clients discover which node owns a given partition.

**Why:** As partitions rebalance, the mapping from partition to node changes. Clients or proxies must track these changes to route requests to the correct node. Using stale routing metadata results in forwarded requests (extra latency), re-tried requests, or errors. The routing approach must match the database's coordination model.

Three options:

**Option 1 — Any-node with forwarding (gossip-based):**
- Clients send requests to any node. If that node owns the partition, it handles the request; otherwise it forwards to the correct node.
- Nodes disseminate routing metadata via gossip protocol — no external coordination service required.
- Used by Cassandra and Riak.
- Trade-off: adds complexity to database nodes; routing metadata may be slightly stale (eventual convergence). Good for systems that must avoid a single-point-of-failure coordination service.

**Option 2 — Routing tier (coordination service):**
- A dedicated routing layer (partition-aware load balancer) receives all requests, consults a coordination service (ZooKeeper, etcd), and forwards to the correct node.
- ZooKeeper maintains the authoritative partition-to-node mapping. Nodes register themselves; the routing tier subscribes to changes.
- Used by HBase, SolrCloud, Kafka (ZooKeeper), LinkedIn Espresso (Helix+ZooKeeper).
- Trade-off: introduces ZooKeeper as an operational dependency; provides strong consistency for routing metadata. Best for systems with complex multi-partition query routing.

**Option 3 — Partition-aware client:**
- The client library maintains a local copy of the partition-to-node mapping and connects directly to the correct node.
- Requires a mechanism to learn about partition changes — usually subscribing to ZooKeeper, or refreshing from a config server.
- Used by MongoDB (mongos daemon), some Cassandra drivers in "token-aware" mode.
- Trade-off: pushes routing logic into each client; reduces hop count for simple key lookups.

---

## What Can Go Wrong

**Hotspot from monotonically increasing write key**
The most common partitioning failure. A table keyed on `created_at`, `id SERIAL`, or any auto-increment column with range partitioning sends 100% of writes to the partition covering the current moment. The newest partition is overloaded while all others sit idle.
Fix: Switch to compound key with a high-cardinality prefix, or switch to hash partitioning if range queries are not needed. For time-series with range-query requirements, use `(source_id, timestamp)` compound range key.

**Scatter/gather latency on secondary index queries**
Document-partitioned (local) secondary indexes require querying all partitions. With 100 partitions, the query waits for the slowest of 100 responses (tail latency amplification). Secondary index queries that were fast in a single-node database become 10–100x slower after partitioning.
Fix: If secondary index reads are frequent and latency-sensitive, switch to a global (term-partitioned) index and accept asynchronous write propagation. Alternatively, structure the primary partition key to co-locate records that will be queried together (e.g., partition by tenant_id if secondary queries are always within a tenant).

**Rebalancing storm from automatic rebalancing + false-positive failure detection**
A temporarily overloaded node responds slowly. Other nodes declare it dead. Automatic rebalancing begins moving its partitions to other nodes. The extra rebalancing traffic overloads the already-struggling node further. The added load on other nodes triggers further detection false-positives.
Fix: Use semi-automatic (operator-approved) rebalancing in production. Tune failure detection timeouts conservatively. Set rebalancing rate limits to bound the bandwidth consumed during rebalancing.

**Wrong partition count with fixed-partition scheme**
Fixed partitions chosen at setup cannot be changed later (in databases that do not support dynamic partitioning). Too few partitions caps how many nodes can be added. Too many creates excessive per-partition overhead. Choosing 10 partitions for a system that grows to 100 nodes means 10 nodes must carry the entire load.
Fix: For fixed-partition systems, choose initial partition count 10–20x the expected maximum node count. For variable-growth scenarios, prefer dynamic partitioning.

**Language-native hash functions used for partitioning**
Java's `Object.hashCode()` and Ruby's `Object#hash` return different values for the same string in different JVM processes (randomization is intentional for security). Using these for partitioning produces incorrect routing — the partition computed at write time differs from the partition computed at read time.
Fix: Use a purpose-built stable hash function: MD5 (Cassandra, MongoDB), Fowler-Noll-Vo (Voldemort), MurmurHash, or similar. Verify hash stability across process restarts before deploying.

**Stale routing metadata causes misrouted requests**
If routing metadata is cached client-side and not refreshed after rebalancing, requests are sent to nodes that no longer own the target partition. The node either returns an error or silently returns stale data.
Fix: Use a routing approach that subscribes to partition assignment changes (ZooKeeper watches, gossip convergence). Test routing after every rebalancing event. Implement retry-with-redirect at the client layer.

---

## Examples

### Example 1 — IoT sensor time-series platform

**Scenario:** Storing sensor readings where each reading has `(sensor_id, timestamp, value)`. Queries: fetch all readings for a sensor within a date range; write throughput is high and continuous.

**Trigger:** "We're building a sensor data platform on HBase. Our current key is just the timestamp, and we're seeing one region server getting all the writes."

**Process:**
1. Skew classification: Monotonic key — `timestamp` as the sole partition key causes all writes to go to the "now" partition.
2. Method selection: Range partitioning is required (range scans by date are the primary read pattern). Apply compound range key with sensor name as prefix: key = `(sensor_name, timestamp)`.
3. Secondary index: None required — all queries fix `sensor_name` (partition prefix) and scan a `timestamp` range within the partition.
4. Rebalancing: Dynamic partitioning (HBase default). Pre-split with known sensor names to avoid cold-start single-partition writes.
5. Routing: ZooKeeper-based routing tier (HBase default via HMaster).

**Output:** Compound range key `(sensor_name, timestamp)`. All writes for a sensor go to the same partition, distributed across sensors. Range queries within a sensor are efficient single-partition scans. Dynamic rebalancing handles data growth.

---

### Example 2 — Social media post feed (Cassandra)

**Scenario:** Storing user posts where queries are: "fetch all posts by user X sorted by time" (dominant) and "fetch a single post by post_id" (secondary). Write pattern: each user writes to their own posts; no cross-user write conflicts.

**Trigger:** "We're modeling user posts in Cassandra. We need to efficiently retrieve all posts by a user, sorted from newest to oldest, but we also need to look up individual posts by ID."

**Process:**
1. Skew classification: User ID as partition key is approximately uniform (assuming large user base). No celebrity-user mitigation needed unless specific users are known to be viral.
2. Method selection: Compound key pattern — `user_id` as hash partition key (evenly distributes users across nodes), `post_timestamp DESC` as clustering column (sorts posts within the partition, newest first).
3. Secondary index: Post-by-ID lookup can be handled by a separate table keyed on `post_id` (denormalization, Cassandra idiom) rather than a secondary index, avoiding scatter/gather entirely.
4. Rebalancing: Proportional-to-nodes (Cassandra default, 256 vnodes/node). Automatic with gossip-based partition assignment.
5. Routing: Gossip protocol with token-aware driver (Cassandra default). No ZooKeeper dependency.

**Output:** Compound primary key `(user_id, post_timestamp DESC)`. Fetching all posts by user is a single-partition range scan. Individual post lookup uses a separate `posts_by_id` table. Scales horizontally by adding Cassandra nodes.

---

### Example 3 — E-commerce product catalog with multi-attribute search

**Scenario:** Product records with attributes `(product_id, category, color, price)`. Queries: look up by `product_id` (dominant write target), filter by `category + color` (secondary index query), filter by `price` range (secondary index query).

**Trigger:** "We have 50 million products partitioned by product_id hash across 20 Elasticsearch shards. Our 'filter by category and color' queries are slow and getting slower as we add shards."

**Process:**
1. Skew classification: `product_id` hash partitioning is uniform — no hotspot risk on writes.
2. Method selection: Hash partitioning on `product_id` is correct for primary key lookups. Do not change this.
3. Secondary index analysis: Elasticsearch uses document-partitioned (local) indexes by default. The `category + color` filter query is scatter/gathered across all 20 shards. Query latency scales with shard count.
4. Secondary index strategy: Two options:
   - If `category` queries are always within a tenant/store, consider routing documents by `(store_id, product_id)` compound key to co-locate products from the same store, reducing scatter/gather to intra-store shards.
   - If global catalog search is required, accept scatter/gather and optimize by reducing shard count (fewer, larger shards perform better for scatter/gather than many small shards) or pre-aggregate category+color facets.
5. Rebalancing: Fixed partitions (Elasticsearch uses fixed shard count). Choose initial shard count = projected node count × 2–3. Do not over-shard.
6. Routing: Elasticsearch coordinator node (partition-aware proxy, equivalent to routing tier option).

**Output:** Keep hash partitioning on `product_id`. Accept scatter/gather for secondary index queries — this is the Elasticsearch design. Reduce total shard count to the minimum needed; over-sharding amplifies scatter/gather cost. Add replica shards for read scaling on hot index queries.

---

## Cross-References

- **replication-strategy-selector** — Select replication topology (single-leader, multi-leader, leaderless) after partitioning is configured. Replication factor affects partition sizing.
- **data-model-selector** — Must be run before this skill. The schema and access pattern decisions made there determine viable partition keys and secondary index requirements.
- **storage-engine-selector** — The storage engine (LSM-tree vs. B-tree) affects how range scans perform within a partition. Relevant when range partitioning is selected.

---

## References

See `references/` for:
- `partitioning-decision-matrix.md` — Scoring rubric comparing range, hash, and compound strategies across 6 workload dimensions
- `rebalancing-strategies.md` — Detailed comparison of fixed, dynamic, and proportional rebalancing with configuration guidance
- `secondary-index-trade-offs.md` — Local vs. global index trade-off analysis with cost model
- `hotspot-mitigation-patterns.md` — Patterns for monotonic key hotspots, celebrity key hotspots, and write skew mitigation
- `request-routing-comparison.md` — Gossip vs. ZooKeeper vs. partition-aware client with operational trade-offs per database

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-model-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
