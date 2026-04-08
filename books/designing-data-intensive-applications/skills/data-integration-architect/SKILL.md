---
name: data-integration-architect
description: |
  Design the integration architecture for systems with multiple specialized data stores (Postgres, Elasticsearch, Redis, data warehouses) that must stay in sync. Use when deciding how data flows between components, avoiding dual writes, reasoning about correctness across system boundaries (idempotency, end-to-end operation identifiers), choosing between Lambda and Kappa architecture, or applying the "unbundling databases" pattern to compose specialized tools instead of relying on a single monolith. Trigger phrases: "how do I keep Postgres and Elasticsearch in sync?", "should I use CDC or event sourcing to propagate data?", "how do I avoid dual writes across microservices?", "my downstream systems are going out of sync — how do I fix the architecture?", "how do I design derived data pipelines?", "what is the system of record pattern?", "how do I integrate OLTP with a search index and an analytics warehouse?", "how do I design for end-to-end idempotency?". This is the capstone skill for data systems design — it synthesizes batch pipelines, stream integration, consistency, and replication into a single architecture recommendation. Produces a component map (systems of record vs derived views), data flow diagram, and correctness analysis. Does not replace batch-pipeline-designer or stream-processing-designer — delegates to them for pipeline internals.
model: sonnet
context: 1M
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Current architecture description, data flow diagram, or system design document (architecture.md, data-flow.md)"
    - type: codebase
      description: "docker-compose.yml, schema.sql, config files showing current infrastructure and database choices"
    - type: none
      description: "Skill can work from a verbal description of the system and its data stores"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep, Bash]
  environment: "Any agent environment. Codebase access enables concrete analysis of existing infrastructure. Works equally well from a written system description."
depends-on:
  - batch-pipeline-designer
  - stream-processing-designer
  - consistency-model-selector
  - replication-strategy-selector
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [12]
tags:
  - data-integration
  - derived-data
  - system-of-record
  - unbundling-databases
  - lambda-architecture
  - kappa-architecture
  - change-data-capture
  - event-sourcing
  - total-order-broadcast
  - idempotency
  - end-to-end-correctness
  - dataflow
  - federated-database
  - write-path
  - read-path
  - dual-writes
  - multi-system-consistency
  - operation-identifiers
  - coordination-avoiding
  - timeliness
  - integrity
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/data-integration-architect
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
---

# Data Integration Architect

## When to Use

Use this skill when you are designing or evaluating an architecture where **multiple specialized data stores need to work together** and you must reason about how data flows between them, stays consistent, and remains correct in the face of faults.

Concrete preconditions:

- You have (or are planning) more than one data store: for example, a primary relational database plus a search index, an analytics warehouse, a cache, or a machine learning feature store.
- You need to decide the **integration strategy**: should writes go to all stores directly, or should one store be the source of truth with others derived from it?
- You need to choose the **propagation mechanism**: synchronous distributed transactions, change data capture, event sourcing, or batch ETL.
- You need to evaluate a **processing architecture**: Lambda (separate batch and stream layers), Kappa (unified stream layer), or a single integrated system.
- You have a correctness problem: downstream systems are drifting, duplicate events are being applied, or a system boundary is leaking bugs.

**Do not use this skill** if you have a single-database workload with no integration requirements — use `oltp-olap-workload-classifier` and `storage-engine-selector` instead.

---

## Context and Input Gathering

Before proceeding, gather the following. If any are unknown, ask the user.

**Required:**
1. **Current data stores** — list every database, index, cache, or data warehouse in the system (e.g., PostgreSQL, Elasticsearch, Redis, Snowflake, Kafka).
2. **Data sources** — what writes new data into the system, and at what volume/rate?
3. **Data consumers** — who reads from each store, and what access patterns do they require (full-text search, OLAP aggregation, low-latency lookup, ML training)?
4. **Consistency requirements** — which parts of the system require linearizability (user-facing correctness), and which can tolerate eventual consistency (derived views)?
5. **Growth trajectory** — current data volume, expected growth rate, and peak write throughput.

**Optional but valuable:**
- Existing architecture diagram or `architecture.md` / `docker-compose.yml`
- Current integration mechanism (if any: ETL scripts, dual writes, triggers, CDC)
- Known pain points: lag, drift, data loss, duplicate processing, schema migration friction

**If dependencies are installed**, invoke them to fill gaps:
- `consistency-model-selector` → determine per-operation consistency requirements
- `replication-strategy-selector` → determine replication topology for the primary store
- `batch-pipeline-designer` → design the batch processing layer if historical reprocessing is needed
- `stream-processing-designer` → design the stream processing layer if low-latency propagation is needed

---

## Process

### Step 1: Map the Current Dataflow

**ACTION:** Identify every system that stores data and every transformation that moves data between systems.

Draw (or describe) the current state:
```
[Write source] → [Store A] → ??? → [Store B]
                           → ??? → [Store C]
```

For each data path, classify the current integration mechanism:
- **Dual writes** (application writes to A and B directly) — flag as anti-pattern
- **Distributed transactions** (2PC across stores) — note heterogeneity constraints
- **Change data capture** (CDC from A's replication log to B)
- **Event sourcing** (events written to a log; A and B derived independently)
- **Batch ETL** (periodic full or incremental extract from A to B)

**WHY:** You cannot improve what you cannot see. Dual writes are the most common source of drift between systems — if the write to Store B fails after the write to Store A succeeds, the stores diverge permanently. Making the dataflow explicit immediately surfaces where this risk exists.

---

### Step 2: Identify the System of Record

**ACTION:** For each logical data entity (user, order, product, event), determine which single store is the **system of record** — the authoritative source of truth that other representations are derived from.

Apply this test: if Store A and Store B disagree about the value of an entity, which one is correct by definition?

- If the answer is "A" → A is the system of record; B is a derived view.
- If the answer is "it depends" or "neither" → you have a multi-master problem that must be resolved by architecture (see Step 4).

Document the result as a table:

| Entity | System of Record | Derived Views |
|--------|-----------------|---------------|
| User profile | PostgreSQL users table | Elasticsearch user index, Redis session cache |
| Order | PostgreSQL orders table | Kafka order-events log, Snowflake orders_fact |
| Search index | (none — fully derived) | Elasticsearch ← PostgreSQL via CDC |

**WHY:** The system of record designation is not just documentation — it determines write authority. Only the system of record should accept writes for its entities. All other stores are read-optimized derived views that are populated by processing the source of truth. This is what prevents split-brain inconsistency between stores.

---

### Step 3: Choose the Integration Mechanism

**ACTION:** For each system of record → derived view pair, select the integration mechanism from this decision framework:

**Decision tree:**

```
Is the derived view latency requirement < 1 minute?
├─ YES → Use stream-based propagation (CDC or event sourcing)
│        → invoke stream-processing-designer for details
└─ NO  → Can you afford to reprocess all historical data?
         ├─ YES → Consider batch ETL (simpler, replayable)
         │        → invoke batch-pipeline-designer for details
         └─ NO  → Use incremental batch or hybrid (CDC + periodic batch)
```

**For the propagation mechanism, choose:**

| Mechanism | Use when | Trade-off |
|-----------|----------|-----------|
| **Change data capture (CDC)** | Existing database cannot be changed; need low-latency propagation | Requires access to replication log; schema changes need care |
| **Event sourcing** | New system or greenfield; want full audit log; need replayability | Application must be redesigned around immutable events |
| **Batch ETL** | High latency acceptable; historical reprocessing needed regularly | Simple but creates lag windows; schema evolution is manual |
| **Log-based messaging (Kafka)** | High throughput; multiple consumers; need replay; decoupled teams | Operational complexity; ordering only within partition |

**Key principle — prefer the event log over distributed transactions:**
Distributed transactions (2PC) across heterogeneous stores are fragile: they have poor fault tolerance (coordinator failure leaves participants in-doubt), poor performance (blocking protocol), and require all participating systems to speak the same transaction protocol. An ordered log of events with idempotent consumers achieves the same correctness properties with better fault isolation and looser coupling. A fault in one consumer is contained locally; it does not abort the writes to all other systems.

**WHY:** The integration mechanism determines whether failures in one part of the system cascade to other parts. Synchronous coupling (dual writes, distributed transactions) amplifies failures across system boundaries. Asynchronous event logs contain failures: a slow or failed consumer falls behind, but the producer and other consumers continue unaffected.

---

### Step 4: Decide — Single System vs. Composed Pipeline

**ACTION:** Evaluate whether the requirements can be satisfied by a single integrated system or require a composed pipeline of specialized tools.

Apply this test:

**Use a single system if:**
- One technology satisfies all access patterns with adequate performance (e.g., PostgreSQL with full-text search is sufficient for the scale)
- The team lacks operational capacity to run multiple systems
- The workload fits within the throughput and latency envelope of a single product

**Use a composed pipeline if:**
- No single technology satisfies all access patterns (OLTP + full-text + analytics + ML feature serving)
- Scale requirements exceed what a single system can handle
- Different teams own different parts of the data, requiring independent deployment

**The unbundling principle:** A database internally implements secondary indexes, materialized views, replication logs, and caching. When you compose specialized systems — a primary database plus a search index plus an analytics warehouse plus a feature store — you are "unbundling" those features into separate, independently deployable components. The event log plays the role of the replication log that connects them.

The goal of unbundling is **breadth**: achieving good performance across a wider range of workloads than any single system supports. It is not to maximize the number of moving parts.

**WHY:** Many teams reach for multi-system architectures prematurely and add operational complexity without proportionate benefit. The decision must be grounded in actual access pattern requirements that cannot be satisfied by a simpler alternative.

---

### Step 5: Choose the Processing Architecture

**ACTION:** If a composed pipeline is warranted, select the processing architecture:

**Lambda Architecture:**
- Two parallel layers: a batch layer (reprocesses all historical data; produces accurate views) and a speed layer (processes recent events; produces approximate views)
- Reads merge results from both layers
- **Use when:** Batch processing is significantly simpler and less bug-prone than the stream processor you can operate, AND the latency of batch processing alone is unacceptable
- **Problems:** Maintaining the same logic in two frameworks doubles complexity; merging batch and stream outputs is non-trivial for operations beyond simple aggregations; batch layer often ends up doing incremental processing anyway, negating its simplicity advantage

**Kappa Architecture:**
- Single stream processing layer that handles both historical reprocessing (by replaying the log) and recent events
- **Use when:** A stream processor with replay capability (e.g., Apache Flink reading from Kafka with historical retention, or Apache Beam on Google Cloud Dataflow) can match the correctness guarantees of batch processing
- **Required capabilities:** Log-based broker with configurable retention (replay); exactly-once semantics in the stream processor; event-time windowing (not processing-time windowing, which is meaningless during replay)
- **Preferred** when these capabilities are available — eliminates the dual-system burden of Lambda

**Single unified system:**
- Modern stream processors (Flink, Beam) unify batch and stream by treating batch as a bounded stream
- **Use when** the team can operate one such system well; eliminates the architecture choice entirely

**WHY:** Lambda architecture was an important idea that made event reprocessing central to data system design. But the practical problems — dual codebases, merged outputs, incremental batch complexity — are significant. The Kappa architecture achieves the same benefits (replayability, correctness, low latency) without the dual-system burden, provided the stream processor supports replay and exactly-once semantics.

---

### Step 6: Design for Total Ordering

**ACTION:** Identify which data flows require a total order and evaluate whether total order is achievable given your deployment constraints.

**Total ordering is required when:**
- Multiple systems derive state from the same events and must remain consistent with each other (they must process events in the same order)
- A uniqueness constraint must be enforced (who claimed the username first?)
- Causal dependencies exist between events in different partitions or services (the "unfriend before message" example: a message notification system must not deliver a message to a user who was unfriended before the message was sent)

**Constraints on total ordering:**

| Constraint | Effect |
|------------|--------|
| Single leader | Total order is feasible; the leader serializes all writes |
| Multiple partitions | Order within a partition is guaranteed; across partitions is not |
| Multiple datacenters | Total order requires synchronous cross-datacenter coordination (high cost) |
| Independent microservices | Events originating in different services have no defined order |

**For causal ordering without total order, consider:**
- **Logical timestamps** (Lamport clocks, vector clocks): provide causal ordering without a single leader; see `consistency-model-selector`
- **Causal event identifiers**: log the state the user saw before making a decision (the event identifier); downstream consumers can reference this to reconstruct the causal dependency
- **Partition routing by entity**: route all events for a given entity (user ID, order ID) to the same partition, ensuring per-entity ordering

**WHY:** Total order broadcast is equivalent to consensus — it requires a single node (or Raft/Paxos cluster) to serialize all events. This scales well on a single machine but becomes a bottleneck at very high throughput or across geographically distributed systems. Understanding exactly which parts of your data flow require total ordering — versus which can tolerate partial ordering — lets you apply the strong guarantee only where it is necessary.

---

### Step 7: Enforce End-to-End Correctness

**ACTION:** Apply the end-to-end argument to the integration architecture. Verify that correctness guarantees are not assumed from any single layer.

**The end-to-end argument:** TCP suppresses duplicate packets within a connection. Databases provide transactional atomicity. Stream processors provide exactly-once semantics within the processing framework. But none of these individually prevent a user from submitting a duplicate request after a network timeout. Solving the problem requires passing a unique operation identifier all the way from the end-user client to the final data store.

**Correctness checklist — apply to every data flow:**

1. **Idempotency at the consumer:** Can the consumer safely process the same event twice? If not, implement idempotency using a deduplication table keyed by operation ID.

   ```sql
   -- Pattern: unique constraint on request_id suppresses duplicates
   ALTER TABLE requests ADD UNIQUE (request_id);
   INSERT INTO requests (request_id, ...) VALUES ('uuid-here', ...);
   -- Second identical insert fails at the constraint level — safe to retry
   ```

2. **Operation identifier propagation:** Is a unique operation ID generated by the client (UUID or hash of request fields) and passed through every hop — HTTP request → message broker → stream processor → database write?

3. **Single-message atomicity for multi-partition operations:** When an operation must affect multiple partitions (e.g., debit account A and credit account B), do not use distributed atomic commit. Instead:
   - Write the entire request as a single message to a log partition (by request ID)
   - A stream processor reads the request and emits individual instructions to each partition's stream (with the request ID included)
   - Downstream processors for each partition deduplicate by request ID
   - This achieves equivalent correctness to atomic commit without cross-partition coordination

4. **Timeliness vs. integrity separation:** Distinguish what must be linearizable (users must see their own writes immediately) from what requires only integrity (data must not be lost or corrupted). Violations of timeliness are eventually consistent; violations of integrity are permanent corruption.
   - **Timeliness failures:** the user sees stale data temporarily → recover by waiting
   - **Integrity failures:** data is lost, double-charged, or corrupted → cannot self-heal

   Design the architecture so integrity is maintained in all cases, even if timeliness guarantees are weak.

5. **Loose constraint enforcement:** Not every uniqueness constraint requires synchronous linearizable enforcement. Evaluate whether the business cost of a constraint violation is recoverable:
   - If two users claim the same username concurrently and one succeeds, the other gets a rejection — recoverable
   - If a financial transaction is applied twice to an account — not recoverable
   
   For recoverable constraints, asynchronous detection and compensation (apology workflow) may be sufficient, enabling coordination-avoiding architectures with better availability and performance.

**WHY:** This is the most critical step and the most commonly skipped. Engineers assume that because their database provides transactions and their message broker provides exactly-once delivery, their system is correct. The end-to-end argument shows this is false: each layer handles its own scope, but correctness across the entire request path — from client to database — requires an explicit end-to-end mechanism. The operation identifier is the minimal such mechanism.

---

### Step 8: Produce the Integration Architecture Document

**ACTION:** Write an `integration-architecture.md` with three sections:

**Section 1: Component Map**
List every data store with its role (system of record vs. derived view), the entity types it owns or serves, and the access patterns it satisfies.

```
[System of Record]
  PostgreSQL — users, orders, products
    Access: OLTP reads/writes, foreign key enforcement

[Derived Views — propagated via Kafka CDC]
  Elasticsearch — full-text search on products and orders
  Snowflake — orders_fact, products_fact for OLAP analytics
  Redis — user session cache, hot product cache

[Processing Layer]
  Kafka — event log (ordered message delivery, 7-day retention)
  Debezium — CDC from PostgreSQL to Kafka
  Apache Flink — stream processor (CDC → Elasticsearch, Snowflake)
```

**Section 2: Data Flow Diagram**
For each entity type, show the write path (how new data enters) and the read path (how consumers access the derived view).

```
Write Path:
  User action → Application server → PostgreSQL (system of record)
              → Debezium reads WAL → Kafka topic (ordered)
              → Flink consumer → Elasticsearch (search index)
              → Flink consumer → Snowflake (analytics)

Read Path:
  Full-text search → Elasticsearch
  OLAP query       → Snowflake
  OLTP query       → PostgreSQL
  Session lookup   → Redis (populated from PostgreSQL on login)
```

**Section 3: Correctness Analysis**
Document the ordering guarantees, idempotency mechanisms, and constraint enforcement strategy for each critical data flow.

---

## Examples

### Example 1: E-commerce Platform — OLTP + Search + Analytics

**Scenario:** Online retailer with PostgreSQL for orders/products, Elasticsearch for product search, Snowflake for business analytics. Current architecture uses dual writes from application code. Products sometimes appear in search before inventory is updated; analytics dashboards occasionally show orders that do not exist in PostgreSQL.

**Trigger:** "Our Elasticsearch and PostgreSQL are drifting. Products show in search that are out of stock. How do we fix the architecture?"

**Process:**
- Step 1 identifies dual writes as the anti-pattern causing drift
- Step 2 designates PostgreSQL as system of record for products, orders, inventory
- Step 3 selects CDC (Debezium) from PostgreSQL WAL → Kafka → Elasticsearch/Snowflake consumers
- Step 6 confirms that per-product ordering (route by product_id partition) is sufficient; total ordering across all products is not required
- Step 7 verifies Flink consumers are idempotent (upsert by product_id handles redelivery)

**Output:** Replace dual writes with Debezium CDC pipeline. Elasticsearch and Snowflake become read-only derived views, populated exclusively from the Kafka event log. Drift is eliminated because both stores process the same ordered event sequence from the same source.

---

### Example 2: Financial Services — Multi-Partition Transfer with End-to-End Correctness

**Scenario:** Payment processing system where transferring money requires debiting one account (partition A) and crediting another (partition B). Current implementation uses two-phase commit across partitions; this causes availability problems when the coordinator fails.

**Trigger:** "We're using 2PC for cross-account transfers and it's killing our availability. How do we redesign this?"

**Process:**
- Step 3 selects event sourcing: log the transfer request as a single message
- Step 6 identifies that per-request ordering (route by request_id) is needed to prevent duplicate application
- Step 7 applies the multi-partition correctness pattern:
  1. Client generates UUID request_id; application appends transfer request to Kafka (keyed by request_id)
  2. Stream processor reads request; emits debit instruction to partition A's stream (with request_id) and credit instruction to partition B's stream (with request_id)
  3. Account processors for A and B each deduplicate by request_id using a unique constraint on a requests table
- If the stream processor crashes and reprocesses the request, it produces identical debit/credit instructions; the unique constraint suppresses the duplicates

**Output:** Remove 2PC. Achieve equivalent correctness (every transfer applied exactly once to both accounts) without cross-partition coordination. Availability improves because no coordinator failure mode exists.

---

### Example 3: Social Platform — Causal Ordering Across Services

**Scenario:** Social network with friendship status stored in service A, notification delivery in service B. Users report receiving notifications from people they have unfriended — the unfriend event and the message-send event are processed in the wrong order.

**Trigger:** "Users are getting messages from people they unfriended. The unfriend event seems to arrive after the message sometimes."

**Process:**
- Step 1 identifies that friendship and messaging are independent event streams; no total order exists between them
- Step 6 identifies a causal dependency: the message-send event causally depends on the friendship status the sender observed
- Fix: When the sender sends a message, log the event identifier of the most recent friendship-status read (the state the sender saw). The notification service checks this event ID; if it has not yet processed past that event in the friendship log, it defers the notification.
- Alternative: Route all friendship and messaging events through a single Kafka topic partitioned by the pair of user IDs, imposing a per-pair total order

**Output:** Causal dependency captured via event identifiers. Notification service becomes causally consistent without requiring total ordering across all users.

---

## References

- [Architecture patterns: federated databases vs. unbundled databases](references/unbundling-patterns.md)
- [Lambda vs. Kappa architecture decision guide](references/lambda-kappa-decision.md)
- [End-to-end correctness and operation identifier implementation](references/end-to-end-correctness.md)
- [Timeliness vs. integrity: distinguishing the two dimensions of consistency](references/timeliness-integrity.md)

**Cross-skill references:**
- `batch-pipeline-designer` — design the batch reprocessing layer (historical data, schema migrations)
- `stream-processing-designer` — design the stream propagation layer (CDC, event sourcing, window types, join types)
- `consistency-model-selector` — determine per-operation consistency requirements; distinguish linearizability from serializability; select consensus mechanisms where needed
- `replication-strategy-selector` — determine the replication topology of the primary system of record
- `transaction-isolation-selector` — evaluate isolation requirements for the system of record's OLTP workload
- `distributed-failure-analyzer` — diagnose correctness failures in the existing integration

**Source:** Designing Data-Intensive Applications, Martin Kleppmann (O'Reilly, 2017), Chapter 12: The Future of Data Systems, pp. 489–544.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-batch-pipeline-designer`
- `clawhub install bookforge-stream-processing-designer`
- `clawhub install bookforge-consistency-model-selector`
- `clawhub install bookforge-replication-strategy-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
