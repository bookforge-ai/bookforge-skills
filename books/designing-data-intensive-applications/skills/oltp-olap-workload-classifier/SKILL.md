---
name: oltp-olap-workload-classifier
description: |
  Classify a data workload as OLTP, OLAP, or hybrid, then recommend the appropriate database architecture — transactional database, dedicated data warehouse, or both with an ETL pipeline. Use when asked "should I use a data warehouse?", "why are my analytics queries slow on my production database?", "should I use Redshift/BigQuery/Snowflake?", or "can one database handle both transactions and reporting?" Also use for: designing star or snowflake schemas for analytics; deciding when column-oriented storage is appropriate; planning ETL pipeline structure between operational and analytical systems; evaluating whether HTAP (hybrid) databases fit a workload.
  For choosing between relational/document/graph models, use data-model-selector instead. For storage engine internals (LSM-tree vs B-tree), use storage-engine-selector instead. For batch/stream pipeline design, use batch-pipeline-designer or stream-processing-designer instead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/oltp-olap-workload-classifier
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [3]
    pages: [90-103]
tags: [data-architecture, oltp, olap, data-warehouse, star-schema, column-storage, etl, analytics, database-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: description
      description: "Query patterns, data volume, response time requirements, user count and access patterns — the skill guides gathering via structured questions"
    - type: file
      description: "Schema definitions, architecture docs, or existing query samples if available"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase or schema exists, scan for data access patterns."
---

# OLTP/OLAP Workload Classifier

## When to Use

You need to determine whether a system's data access patterns require a transactional database (OLTP), an analytic data warehouse (OLAP), or both — and then recommend the right architecture for each workload type.

Typical triggers:

- "Our analytic queries are slowing down production"
- "Should we build a data warehouse?"
- "What kind of database should we use for our reporting layer?"
- "Business analysts are running heavy queries on our app database"
- "We need to analyze years of transaction history"
- Designing a new system where both operational and reporting needs exist

Before starting: if the user is asking specifically about which storage engine (B-tree vs LSM-tree) to use for an OLTP system, use `storage-engine-selector` instead. If the user is asking about ETL pipeline architecture in detail, use `batch-pipeline-designer` after this skill.

## Context & Input Gathering

### Input Sufficiency Check

### Required Context (must have — ask if missing)

- **Query patterns:** What do the most important queries do?
  - Check prompt for: SELECT patterns, GROUP BY, aggregations, JOIN count, filter on key vs scan
  - If missing, ask: "Can you describe 2-3 of your most important or frequent queries? Are they looking up specific records by ID, or scanning large ranges of data to compute totals and statistics?"

- **Who runs the queries:** End users/customers or internal analysts?
  - Check prompt for: mentions of "our users", "business analysts", "BI team", "dashboards", "reports"
  - If missing, ask: "Who runs these queries — end users of your application, or internal analysts and data scientists?"

- **Write pattern:** How does data get in?
  - Check prompt for: user-triggered writes, batch imports, event streams, ETL mentions
  - If missing, ask: "How does data get written — individual transactions triggered by user actions, or bulk imports/batch jobs?"

### Important Context (strongly recommended)

- **Data volume:** Current and expected scale
  - Ask: "How much data are we talking about — gigabytes, terabytes, or petabytes? How many rows in the main tables?"

- **Response time requirements:**
  - Ask: "What latency is acceptable? Sub-100ms for user-facing? Seconds for analyst queries? Minutes for nightly reports?"

- **How many columns per query:** Does each query need all columns, or a few at a time?
  - This determines column-oriented storage benefit

- **Historical data need:** Are queries over current state or history?
  - Ask: "Are queries over the current state of data (e.g., 'what is the inventory right now?') or historical trends (e.g., 'how did sales vary across all of last year?')?"

### Observable Context (gather from environment)

- **Existing schema:** Scan for table structures — row count estimates in comments, presence of `fact_` or `dim_` table prefixes, heavy normalization vs wide flat tables
- **Query files:** Look for `.sql` files — presence of `GROUP BY`, `SUM`, `COUNT`, `AVG`, `JOIN` chains, `WHERE year =` predicates is an OLAP signal
- **ORM or application code:** Heavy `find_by_id`, `save`, `update` patterns = OLTP. Analytical query builders = OLAP.
- **Infrastructure config:** Presence of Redshift, BigQuery, Snowflake, dbt, Airflow configs = OLAP already in use or planned

### Default Assumptions

- If query patterns unknown → ask before proceeding (this is the classification's core input)
- If data volume unknown → assume "terabytes or less" (affects column storage urgency, not classification outcome)
- If response time unknown → assume user-facing needs <500ms (OLTP), analyst queries can tolerate seconds to minutes (OLAP)
- If write pattern unknown → assume user-triggered individual writes (OLTP default)

### Sufficiency Threshold

```
SUFFICIENT: query patterns + who runs them + write pattern are known
PROCEED WITH DEFAULTS: query patterns known but volume/latency not quantified
MUST ASK: query patterns are unknown
```

## Process

### Step 1: Score the Workload on 6 Dimensions

**ACTION:** Evaluate the described workload against the 6-dimension comparison table (Table 3-1 from the book). Assign OLTP or OLAP for each dimension. Count the majority.

**WHY:** OLTP and OLAP workloads differ not in degree but in kind. A single database engine is optimized for one or the other — not both. Row-oriented storage excels at OLTP (low-latency point lookups, frequent small writes) but is inefficient for OLAP (must load entire rows even when only 3 of 100 columns are needed). Column-oriented storage compresses well and accelerates aggregate scans but makes individual row inserts expensive. Classifying on all 6 dimensions prevents misclassification from a single misleading signal (e.g., a small analytic workload might have fast query times — that alone doesn't make it OLTP).

| Dimension | OLTP Signal | OLAP Signal |
|-----------|-------------|-------------|
| **Main read pattern** | Small number of records fetched by key (point lookup) | Aggregate over large number of records (scan + compute) |
| **Main write pattern** | Random-access, low-latency writes from user input | Bulk import (ETL) or event stream ingestion |
| **Primarily used by** | End user / customer via web or mobile application | Internal analyst, for business intelligence and decision support |
| **What data represents** | Latest state (current point in time) | History of events that happened over time |
| **Dataset size** | Gigabytes to terabytes | Terabytes to petabytes |
| **Bottleneck** | Disk seek time (index lookup cost) | Disk bandwidth (volume of data scanned) |

**Scoring:**
- Count OLTP vs OLAP signals across the 6 dimensions
- 5-6 OLTP signals → pure OLTP workload
- 5-6 OLAP signals → pure OLAP workload
- 3-4 signals for one type → mixed/hybrid — flag as HTAP candidate (see Step 4)

**Output:** Classification label + dimension-by-dimension score table.

### Step 2: Route to Architecture

**ACTION:** Based on classification, select the recommended architecture path and proceed to the corresponding sub-step.

**WHY:** The routing decision is binary at its core — OLTP and OLAP systems have fundamentally different storage engine designs. Running analytic queries on an OLTP database does not just perform poorly; it actively harms the concurrent transactions by consuming disk I/O and CPU that the storage engine's indexes cannot help with. Enterprises learned this in the late 1980s and began extracting analytic workloads into separate data warehouses specifically to protect OLTP availability. The routing step enforces this architectural boundary.

- **Pure OLTP** → Step 3A (OLTP architecture guidance)
- **Pure OLAP** → Step 3B (data warehouse + schema design)
- **Mixed/hybrid** → Step 4 (HTAP separation strategy), then Step 3A + 3B

### Step 3A: OLTP Architecture Guidance

**ACTION:** For OLTP workloads, confirm the storage engine class and index strategy. This step is a quick check — detailed OLTP guidance lives in `storage-engine-selector`.

**WHY:** OLTP systems are optimized for individual record access: fast point reads (via B-tree or LSM-tree indexes), low-latency writes, and high concurrent user support. The storage engine should be selected to match the write-to-read ratio and durability requirements. Key decisions are: log-structured (LSM-tree) for write-heavy workloads, update-in-place (B-tree) for read-heavy workloads with mixed updates.

Guidance:
- Index on primary key + frequently queried foreign keys
- Normalize schema to minimize update anomalies
- Use transactions with appropriate isolation level (see `transaction-isolation-selector`)
- Do NOT allow ad-hoc analytic queries to run directly — plan for read replicas or export

**If the user also needs analytics** → proceed to Step 3B after this step, and plan ETL from OLTP to OLAP.

### Step 3B: OLAP Architecture — Data Warehouse Design

**ACTION:** Design the data warehouse schema using the star or snowflake schema pattern. Identify the central fact table and its dimension tables.

**WHY:** Data warehouses use a different schema paradigm than operational databases. Operational databases are normalized to minimize write anomalies. But normalization hurts analytic queries — analysts need to join many tables, and every join adds latency at scan scale. The star schema deliberately denormalizes into one wide fact table (every business event as a row) surrounded by dimension tables (the who, what, where, when, why of each event). This layout makes the most common analytic queries simple: filter dimensions, join to fact table, aggregate. Column-oriented storage then further optimizes this by reading only the few columns each query actually touches rather than loading full rows.

**Sub-step 3B-1: Identify the fact table**

The fact table is the center of the star. Each row represents one business event — one sale, one page view, one sensor reading, one log entry. Key characteristics:
- Rows represent events, not entities (events are immutable once they occur)
- Very wide: typically 100+ columns including metrics (quantities, prices, durations) and foreign keys to dimension tables
- Very tall: enterprises may have tens of petabytes of fact table rows
- Columns include measurable facts (quantity sold, net price, response time) plus foreign keys (product_sk, store_sk, customer_sk, date_key)

Ask: "What is the core business event you are tracking? What gets recorded every time that event occurs?"

**Sub-step 3B-2: Identify dimension tables**

Dimension tables answer the "who, what, where, when, how, why" of each event in the fact table. Key characteristics:
- One row per entity (one row per product, per store, per customer, per calendar day)
- Wide but short: many descriptive columns, relatively few rows
- Connected to fact table by surrogate keys (integer foreign keys, not natural business keys)
- Even time gets a dimension table (`dim_date`) — this allows encoding attributes like `is_holiday`, `weekday`, `fiscal_quarter` that enable time-based filtering without date arithmetic

Standard dimension table set for a retail fact table:

| Dimension | Purpose | Example columns |
|-----------|---------|-----------------|
| `dim_date` | Time-based filtering and grouping | `date_key`, `year`, `month`, `day`, `weekday`, `is_holiday` |
| `dim_product` | Product attributes for filtering/grouping | `product_sk`, `sku`, `description`, `brand`, `category` |
| `dim_store` | Store/location attributes | `store_sk`, `state`, `city`, `store_type`, `open_date` |
| `dim_customer` | Customer attributes | `customer_sk`, `name`, `date_of_birth`, `segment` |
| `dim_promotion` | Promotion/campaign attributes | `promotion_sk`, `name`, `ad_type`, `coupon_type` |

**Sub-step 3B-3: Choose star vs snowflake schema**

| Schema | Structure | When to use |
|--------|-----------|-------------|
| **Star schema** | Dimension tables are flat (denormalized) | Preferred for analyst usability — simpler SQL, fewer joins, faster iteration |
| **Snowflake schema** | Dimensions further normalized into sub-dimensions (e.g., `dim_brand` split out from `dim_product`) | When storage is a constraint or dimension data integrity is critical; harder for analysts to query |

Default to **star schema** unless there is a specific normalization requirement. Analysts work with the schema daily — simplicity compounds.

**Sub-step 3B-4: Apply column-oriented storage**

**WHY column-oriented storage matters for OLAP:** A typical analytic query accesses 4-5 columns out of 100+ in the fact table. Row-oriented storage must load every column of every matching row from disk — paying I/O cost for 95+ columns that are immediately discarded. Column-oriented storage keeps each column in a separate file. The query only reads the files for the columns it needs. For a 100-column fact table, this is a 20x reduction in I/O for a 5-column query.

Additional benefits of column storage:
- **Compression:** Column files contain repetitive values (e.g., `product_sk` repeating across millions of purchases). Run-length encoding and bitmap encoding compress these dramatically — often 10x or more.
- **Vectorized processing:** CPU can iterate over compressed column data in tight loops (fits L1 cache), enabling SIMD instruction optimization — faster than row-by-row processing with branch conditions.
- **Sort optimization:** Sorting fact table rows by the most common filter column (e.g., `date_key`) enables range scans that skip large portions of data. Store multiple sort orders across replicas for different query patterns.

**Column storage decision criteria:**

Use column-oriented storage when:
- Fact table has 20+ columns and queries touch fewer than 10 at a time
- Dataset is terabytes or larger
- Queries are read-heavy (analysts, not concurrent transactional writes)
- Aggregate functions (SUM, COUNT, AVG, MAX) dominate query patterns

Defer column storage (use row-oriented) when:
- Dataset fits comfortably in RAM
- Queries regularly need all or most columns per row
- Write throughput is the bottleneck (column storage writes are more complex — use LSM-tree ingestion pattern if column storage is needed)

**Sub-step 3B-5: Plan the ETL pipeline**

**WHY a separate ETL pipeline:** OLTP databases must remain highly available for user-facing transactions. Business analysts running heavy scans on the OLTP database consume disk I/O and table locks that starve concurrent transactions. The solution is to export data on a schedule (periodic dump or continuous stream of change events) from OLTP systems, transform it into the warehouse schema, and load it into a separate read-only warehouse. This is Extract–Transform–Load (ETL).

ETL design decisions:

| Decision | Options | Guidance |
|----------|---------|----------|
| **Extraction method** | Periodic full dump, incremental delta export, change data capture (CDC) stream | CDC is lowest-latency; full dumps are simplest but expensive at scale |
| **Transformation** | In the pipeline (ETL) or in the warehouse after loading (ELT) | ELT preferred for modern cloud warehouses with strong SQL compute (Snowflake, BigQuery, Redshift) |
| **Load frequency** | Nightly batch, hourly micro-batch, near-real-time | Match to analyst freshness requirements — nightly is often sufficient |
| **Schema management** | Separate warehouse schema from OLTP schema | Never query OLTP tables directly from analyst tools |

For detailed ETL/batch pipeline architecture, use `batch-pipeline-designer`.

### Step 4: Hybrid Workload (HTAP) — Separation Strategy

**ACTION:** When the workload shows both OLTP and OLAP signals (typically 3-4 signals on each side), design a two-tier architecture that separates operational and analytical processing.

**WHY:** Hybrid Transactional/Analytical Processing (HTAP) is the most common real-world scenario — an application database that also needs to support reporting. Running both on the same database is the default, and the default fails at scale: analytic queries lock rows, consume disk bandwidth, and compete with user-facing transactions for buffer pool space. The solution is always architectural separation: one system optimized for transactions, one for analytics, with a data pipeline connecting them. The separation can be light (read replica + materialized views for small scale) or full (dedicated warehouse at large scale).

Separation options by scale:

| Scale | Approach | Tooling |
|-------|----------|---------|
| Small (GB, few analysts) | Read replica + materialized views | PostgreSQL read replica, scheduled view refresh |
| Medium (TB, regular reporting) | Lightweight warehouse or columnar extension | DuckDB, ClickHouse, or PostgreSQL + TimescaleDB |
| Large (multi-TB, BI team) | Dedicated data warehouse + ETL pipeline | Snowflake, BigQuery, Redshift, Apache Hive |
| Very large (PB, real-time analytics) | Streaming pipeline + columnar store | Kafka CDC + Apache Pinot, Druid, or Flink + Iceberg |

**Decision rule:** If OLTP system availability is critical (SLA requirements), always separate — even at small scale. Analytic queries running on a production database are an availability risk that compounds as data grows.

### Step 5: Document the Decision

**ACTION:** Write a concise architecture decision document capturing the classification, recommendation, and key trade-offs.

**WHY:** OLTP/OLAP decisions have downstream consequences for schema design, team structure (DBA vs data engineer), tooling procurement, and pipeline work. Documenting the reasoning prevents the decision from being relitigated as systems grow, and gives future engineers the context for why the architecture is the way it is.

Use the output template below.

## Inputs

- Description of query patterns (point lookups vs scans and aggregations)
- Write pattern (user-triggered vs batch)
- Who uses the system (end users vs analysts)
- Data volume (current and projected)
- Response time requirements
- Existing schema or codebase (optional — scan if available)

## Outputs

### Workload Classification Report

```markdown
# Workload Classification: {System Name}

## Classification Result: {OLTP / OLAP / Hybrid}

### 6-Dimension Scorecard

| Dimension | Your Workload | Signal |
|-----------|--------------|--------|
| Main read pattern | {description} | OLTP / OLAP |
| Main write pattern | {description} | OLTP / OLAP |
| Primary users | {description} | OLTP / OLAP |
| What data represents | {description} | OLTP / OLAP |
| Dataset size | {estimate} | OLTP / OLAP |
| Primary bottleneck | {seek time / bandwidth} | OLTP / OLAP |

**Score: {X} OLTP / {Y} OLAP → Classification: {label}**

## Architecture Recommendation

### {OLTP / OLAP / Both}

**Recommended architecture:** {description}

**Key decisions:**
- Storage engine: {row-oriented / column-oriented / both}
- Schema: {normalized / star schema / snowflake schema}
- Data pipeline: {none needed / ETL nightly / CDC streaming}
- Separation strategy: {single DB / read replica / dedicated warehouse}

### Schema Design (if OLAP)

**Fact table:** `fact_{event}` — one row per {event type}
- Metrics: {list measurable columns}
- Foreign keys: {list dimension references}

**Dimension tables:**
- `dim_date` — {key time attributes}
- `dim_{entity}` — {key descriptive attributes}
- {additional dimensions}

**Schema choice:** Star / Snowflake — {reason}

### Column Storage Decision

{Apply / Defer} column-oriented storage — {reasoning}

### ETL Plan (if applicable)

- Extraction: {method}
- Transformation: {ETL in pipeline / ELT in warehouse}
- Load frequency: {schedule}
- Tools: {recommended}

## Trade-offs

**What we gain:** {performance, separation, scalability}
**What we accept:** {operational complexity, pipeline latency, cost}

## Next Steps

1. {First concrete action}
2. {Second action}
3. {If OLAP: use batch-pipeline-designer for ETL pipeline design}
```

## What Can Go Wrong

**Running analytics on the OLTP database.** The most common mistake. Business analysts get direct database credentials "temporarily" and the arrangement becomes permanent. As data grows, analytic queries take longer, table scans compete with user transactions for buffer pool, and OLTP latency degrades. Prevention: enforce separation early, before it becomes a political problem.

**Misclassifying a hybrid workload as pure OLAP.** If a system needs both fresh operational data (OLTP) and historical aggregate analysis (OLAP), designing only a warehouse misses the operational layer. The warehouse will always lag behind the operational system by the ETL interval — if analysts need current-minute data, a warehouse-only design fails.

**Choosing snowflake schema when star schema suffices.** Snowflake schemas are more normalized but require more joins in every analytic query. For most data warehouses, the storage savings don't justify the analyst experience penalty. Default to star schema and only move to snowflake when storage is genuinely constrained or dimension table updates are frequent.

**Not accounting for write complexity of column-oriented storage.** Column storage is optimized for reads. An update-in-place approach requires rewriting all column files for each affected row. Use LSM-tree ingestion (batch writes accumulate in a row-oriented in-memory store, then merge-flush to column files) for any column store that needs ingestion throughput. Systems like Vertica do this natively.

**Building a data cube too early and losing query flexibility.** Materialized aggregates (OLAP cubes) precompute answers to known queries and are very fast. But they can't answer questions their dimensions don't include. Most warehouses keep raw fact table data as the primary store and use cubes only as a performance layer for known high-frequency queries. Don't replace raw data with cubes.

**ETL pipeline latency mismatch.** A nightly ETL batch is inadequate if analysts need same-day data for decisions. Design the freshness requirement into the ETL architecture from the start — nightly batch, hourly micro-batch, or CDC streaming have very different pipeline architectures.

## Key Principles

- **The OLTP/OLAP divide is structural, not a matter of scale.** A small dataset can have an OLAP access pattern. A large dataset can be OLTP. Classification is about query shape and write pattern, not volume alone.

- **Protect OLTP availability.** OLTP systems power user-facing transactions — they must remain highly available. Any analytic access that risks OLTP availability must be separated architecturally, not managed by query limits or time windows.

- **Fact tables capture events, not entities.** The fact table records what happened — each purchase, each click, each sensor reading — as an immutable event row. Dimension tables describe the participants (the who/what/where). This separation is what enables later flexibility in analysis.

- **Star schema prioritizes analyst usability.** Fewer joins = faster iteration for analysts. Most data warehouses use star schema even at the cost of some normalization because the analyst experience pays compound dividends over time.

- **Column storage = query the columns you need, not the rows you have.** The insight is simple: if your query only needs 4 of 100 columns, reading all 100 columns for every row is 25x more I/O than necessary. Column-oriented storage eliminates that waste.

- **ETL separates concerns cleanly.** OLTP systems export data in their format; the ETL pipeline transforms it into the warehouse's format. Neither system needs to know the details of the other. This decoupling is the architectural payoff of the separate warehouse pattern.

## Examples

**Scenario: E-commerce company with slow reporting**
Trigger: "Our monthly sales reports are taking 20 minutes to run, and our DBAs say it's affecting checkout latency."
Process: Step 1 scoring — monthly reports aggregate all sales by region, category, and promotion (OLAP: read pattern, data represents history, disk bandwidth bottleneck); checkout is user-triggered individual record writes (OLTP: write pattern, used by end users, latest state). Score: 3 OLTP / 3 OLAP → Hybrid. Step 4: two-tier separation. OLTP: PostgreSQL for checkout and inventory. OLAP: dedicated warehouse (Redshift or Snowflake). ETL: nightly batch from OLTP to warehouse — analysts run against warehouse, never production DB. Step 3B: star schema with `fact_orders` at center (one row per order line), dimensions: `dim_product`, `dim_store`, `dim_customer`, `dim_date`, `dim_promotion`. Column storage on warehouse — fact table has 85 columns, typical reports use 6-8.
Output: Hybrid architecture. Nightly ETL extracts from PostgreSQL, loads star schema in Snowflake. Checkout latency restored. Analysts get dedicated compute without SLA risk.

**Scenario: SaaS application building its first analytics feature**
Trigger: "We want to add a dashboard showing our customers their usage trends over the past 12 months."
Process: Step 1 scoring — usage trends require scanning all events per customer over a year, aggregating by day/week (OLAP: read pattern, aggregation, history). But users trigger writes (OLAP + OLTP mix on write side). Volume: currently 50GB, projected 500GB in two years. Response time: dashboard can tolerate 2-3 second loads. Step 4: small-scale separation. Read replica with pre-aggregated materialized views is sufficient now; design schema to migrate to a proper warehouse when data exceeds 1TB or query complexity grows. Step 3B: `fact_usage_events` (one row per usage event per user per day), `dim_date`, `dim_user`, `dim_feature`. Star schema. Column-oriented storage deferred until >1TB — current data fits in memory.
Output: Start with PostgreSQL read replica + materialized views refreshed hourly. Schema designed as star schema from day one. Explicit migration trigger: add dedicated warehouse when data exceeds 1TB or query refresh time exceeds 10 seconds.

**Scenario: IoT sensor data platform**
Trigger: "We collect readings from 10,000 sensors every 30 seconds. We need to detect anomalies in real-time but also run monthly trend analysis."
Process: Step 1 scoring — 10,000 sensors × 2 readings/min × 60 min × 24 hr = ~28.8M rows/day. Historical trend analysis scans months of data for aggregation (OLAP: read pattern, dataset size, bandwidth bottleneck, history). Real-time anomaly detection reads the latest N readings per sensor (OLTP: read by key, latest state, low-latency). Score: 3 OLTP / 3 OLAP → Hybrid, but the write pattern (streaming ingestion at high throughput) tilts toward OLAP infrastructure. Step 4: streaming architecture — Kafka for ingestion, Flink or Spark Streaming for real-time anomaly detection (OLTP path), Apache Iceberg or ClickHouse for historical columnar storage (OLAP path). Step 3B: `fact_readings` (one row per sensor reading with timestamp, sensor_id, value, unit), `dim_sensor` (location, type, calibration metadata), `dim_date`. Column storage applied immediately — 30B rows/year, queries scan months of data for trend analysis.
Output: Two-path architecture. Real-time: Kafka → Flink anomaly detection → alert system. Historical: Kafka → ClickHouse (columnar) for trend queries. Shared ingestion pipeline, separate read paths. Cross-reference `batch-pipeline-designer` for ETL scheduling on the historical path.

## References

- For OLTP storage engine selection (B-tree vs LSM-tree), use `storage-engine-selector`
- For ETL and batch pipeline architecture, use `batch-pipeline-designer`
- For detailed comparison table and schema templates, see [references/workload-comparison-table.md](references/workload-comparison-table.md)
- Source: Designing Data-Intensive Applications, Ch. 3, "Transaction Processing or Analytics?" (pp. 90-103), Martin Kleppmann

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
