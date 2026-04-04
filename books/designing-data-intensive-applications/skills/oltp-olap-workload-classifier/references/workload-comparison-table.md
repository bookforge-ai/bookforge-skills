# OLTP vs OLAP Workload Reference

Source: Designing Data-Intensive Applications, Ch. 3 (Table 3-1), Martin Kleppmann

## 6-Dimension Comparison Table

| Property | OLTP (Transaction Processing) | OLAP (Analytic Systems) |
|----------|------------------------------|------------------------|
| **Main read pattern** | Small number of records per query, fetched by key | Aggregate over large number of records |
| **Main write pattern** | Random-access, low-latency writes from user input | Bulk import (ETL) or event stream |
| **Primarily used by** | End user / customer, via web application | Internal analyst, for decision support |
| **What data represents** | Latest state of data (current point in time) | History of events that happened over time |
| **Dataset size** | Gigabytes to terabytes | Terabytes to petabytes |
| **Bottleneck** | Disk seek time (index lookup) | Disk bandwidth (data scanned per query) |

## Bottleneck Explained

**OLTP — disk seek time:** Each user query touches a small number of records. The storage engine uses an index (B-tree or LSM-tree) to find those records. The cost is the seek — how fast the disk can jump to the right location. Optimizing for OLTP means fast index lookups and low per-record I/O.

**OLAP — disk bandwidth:** Each analytic query scans millions or billions of rows, reading a few columns from each. The bottleneck is not seek time (the query is doing a sequential scan, not random access) but total bytes read from disk. Optimizing for OLAP means reducing the volume of data that must be transferred — column-oriented storage is the primary tool.

## Star Schema Components

### Fact Table

| Characteristic | Detail |
|---------------|--------|
| **What it stores** | One row per business event (one row per sale, click, reading) |
| **Row count** | Billions to trillions — very tall |
| **Column count** | 100+ — very wide (all metrics + all dimension foreign keys) |
| **Column types** | Measurable facts (quantities, prices, durations) + surrogate key foreign keys |
| **Mutability** | Append-only — events are immutable once recorded |

### Dimension Tables

| Characteristic | Detail |
|---------------|--------|
| **What they store** | Descriptive attributes of the entities involved in events |
| **Row count** | Thousands to millions — relatively short |
| **Column count** | Wide — all descriptive attributes relevant to analysis |
| **Relationship to fact** | Connected by surrogate keys (integer, not natural business key) |
| **Examples** | `dim_date`, `dim_product`, `dim_store`, `dim_customer`, `dim_promotion` |

### Surrogate Keys

Dimension tables use surrogate keys (auto-increment integers like `product_sk`) rather than natural business keys (like `sku`). Reasons:
- Natural keys can change (product SKUs get reassigned); surrogate keys never change
- Integers join faster than strings
- Allows encoding multiple versions of a dimension record (slowly changing dimensions)

## Star vs Snowflake Schema

| Factor | Star | Snowflake |
|--------|------|-----------|
| **Dimension structure** | Flat, denormalized | Further normalized into sub-dimensions |
| **Join complexity** | Lower — one join per dimension | Higher — multiple joins to traverse sub-dimensions |
| **Query simplicity** | High — analysts prefer | Lower — more complex SQL |
| **Storage efficiency** | Lower — some redundancy in dimension tables | Higher — normalized sub-tables eliminate redundancy |
| **Data integrity** | Lower — updates must touch dimension table rows | Higher — updates propagate through sub-dimensions |
| **Default choice** | Yes — preferred in most warehouses | Only when storage or update frequency justifies it |

## Column-Oriented Storage Decision Criteria

### Apply column-oriented storage when:
- Fact table has 20+ columns and typical queries access fewer than 10
- Dataset exceeds 1TB (compression and I/O reduction pays off at scale)
- Query mix is dominated by aggregations (SUM, COUNT, AVG, GROUP BY)
- Write throughput is manageable (column stores use LSM-tree ingestion internally)

### Defer column-oriented storage when:
- Dataset fits comfortably in RAM (caching eliminates disk I/O bottleneck)
- Most queries need all or most columns (row storage is more efficient here)
- Write-heavy workload with individual row updates (column stores prefer batch writes)

### Column Compression Techniques

| Technique | When it helps | Compression ratio |
|-----------|--------------|-------------------|
| **Run-length encoding** | Low-cardinality columns, sorted data | 10x-100x for sorted low-cardinality |
| **Bitmap encoding** | Low-cardinality columns (< ~100K distinct values) | Very efficient for WHERE IN queries |
| **Dictionary encoding** | String columns with repeated values | Significant for category, status, region columns |
| **Delta encoding** | Monotonically increasing values (timestamps, IDs) | 4-8x for sequential IDs |

Bitmap encoding is particularly powerful for WHERE predicates in data warehouse queries:
```sql
WHERE product_sk IN (30, 68, 69)
```
Load bitmaps for `product_sk = 30`, `product_sk = 68`, `product_sk = 69` and bitwise OR them. Very fast.

```sql
WHERE product_sk = 31 AND store_sk = 3
```
Load bitmaps for both, bitwise AND them. Both columns must be in the same row order — this is preserved by column storage layout.

## Example Star Schema: Grocery Retailer

From Designing Data-Intensive Applications, Figure 3-9.

```sql
-- Fact table: one row per customer purchase (line item)
CREATE TABLE fact_sales (
    date_key        INTEGER REFERENCES dim_date(date_key),
    product_sk      INTEGER REFERENCES dim_product(product_sk),
    store_sk        INTEGER REFERENCES dim_store(store_sk),
    promotion_sk    INTEGER REFERENCES dim_promotion(promotion_sk),  -- NULL if no promotion
    customer_sk     INTEGER REFERENCES dim_customer(customer_sk),    -- NULL if unknown
    quantity        INTEGER,
    net_price       DECIMAL(10,2),
    discount_price  DECIMAL(10,2)
);

-- Date dimension: encodes time attributes useful for analysis
CREATE TABLE dim_date (
    date_key    INTEGER PRIMARY KEY,
    year        INTEGER,
    month       VARCHAR(3),
    day         INTEGER,
    weekday     VARCHAR(3),
    is_holiday  BOOLEAN
);

-- Product dimension: all attributes relevant to product analysis
CREATE TABLE dim_product (
    product_sk  INTEGER PRIMARY KEY,
    sku         VARCHAR(20),
    description VARCHAR(200),
    brand       VARCHAR(100),
    category    VARCHAR(100)
);

-- Store dimension: all attributes relevant to store analysis
CREATE TABLE dim_store (
    store_sk  INTEGER PRIMARY KEY,
    state     VARCHAR(2),
    city      VARCHAR(100)
);

-- Customer dimension
CREATE TABLE dim_customer (
    customer_sk   INTEGER PRIMARY KEY,
    name          VARCHAR(200),
    date_of_birth DATE
);

-- Promotion dimension (NULL promotion_sk in fact table = no promotion applied)
CREATE TABLE dim_promotion (
    promotion_sk  INTEGER PRIMARY KEY,
    name          VARCHAR(200),
    ad_type       VARCHAR(50),
    coupon_type   VARCHAR(50)
);
```

### Example Analytic Query (from the book)

```sql
-- Analyzing whether people are more inclined to buy fresh fruit or candy
-- depending on the day of the week (2013 calendar year)
SELECT
    dim_date.weekday,
    dim_product.category,
    SUM(fact_sales.quantity) AS quantity_sold
FROM fact_sales
    JOIN dim_date    ON fact_sales.date_key    = dim_date.date_key
    JOIN dim_product ON fact_sales.product_sk  = dim_product.product_sk
WHERE
    dim_date.year = 2013
    AND dim_product.category IN ('Fresh fruit', 'Candy')
GROUP BY
    dim_date.weekday,
    dim_product.category;
```

This query only accesses 3 columns from `fact_sales` (`date_key`, `product_sk`, `quantity`). In a 100-column fact table with row-oriented storage, the engine must load the full row for every matching row. With column-oriented storage, it reads only those 3 column files — a ~33x I/O reduction for this example.

## ETL Pipeline Overview

```
OLTP Systems                 Pipeline                  OLAP Warehouse
─────────────────────────────────────────────────────────────────────
┌─────────────┐  extract   ┌──────────┐  transform  ┌─────────────┐
│ Sales DB    │ ─────────► │          │ ──────────► │             │
├─────────────┤            │  ETL     │             │  Data       │
│ Inventory   │ ─────────► │  Process │ ──────────► │  Warehouse  │◄── Business
│ DB          │            │          │             │             │    Analysts
├─────────────┤  extract   └──────────┘    load     └─────────────┘
│ Geo DB      │ ─────────────────────────────────►
└─────────────┘
```

**Extract:** Periodic full dump, incremental delta, or CDC stream from OLTP
**Transform:** Apply business rules, clean data, map to warehouse schema, resolve surrogate keys
**Load:** Bulk insert into fact and dimension tables

### ELT vs ETL

| Approach | Description | When to use |
|----------|-------------|-------------|
| **ETL** | Transform before loading into warehouse | Legacy warehouses with limited compute; transformation logic is complex |
| **ELT** | Load raw data, transform inside warehouse using SQL | Modern cloud warehouses (Snowflake, BigQuery, Redshift) — warehouse compute is cheap and powerful |

## Materialized Views and OLAP Cubes

**Materialized view:** An actual copy of query results stored on disk, updated when underlying data changes. Unlike a regular view (which is just a saved query), a materialized view is precomputed. Reads are fast; writes are more expensive (must update the view).

**OLAP cube (data cube):** A special case of materialized view. A multi-dimensional grid of precomputed aggregates. For example, `SUM(net_price)` grouped by every combination of `(date_key × product_sk)` — a 2D cube. With 5 dimensions, a 5-dimensional hypercube.

**Trade-off:** Cubes are very fast for queries that match the cube's dimensions, but cannot answer queries involving attributes not included in the cube. Raw fact table data is more flexible. Most warehouses keep raw data as the primary store and layer cubes as a performance optimization for known high-frequency queries.

## Common OLAP Database Technologies

| Scale | Technology | Type | Notes |
|-------|-----------|------|-------|
| Small | DuckDB, SQLite | Embedded columnar | Excellent for <100GB, local analysis |
| Medium | ClickHouse, TimescaleDB | Columnar OLAP | Self-hosted, high performance |
| Large (cloud) | Snowflake, BigQuery, Redshift | Managed cloud warehouse | Fully managed, scales to PB |
| Large (open source) | Apache Hive, Spark SQL, Presto | SQL-on-Hadoop | Open source equivalents |
| Very large | Apache Druid, Apache Pinot | Real-time OLAP | Sub-second queries on streaming data |
| Columnar format | Apache Parquet, ORC | Storage format | Used with Spark, Flink, Presto |
