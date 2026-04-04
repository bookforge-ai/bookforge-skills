# Data Model Decision Matrix

Reference for `data-model-selector`. Use this during Step 2 (scoring) and Step 3 (decision rules) of the skill process.

---

## Scoring Rubric — Full Criteria Definitions

### 1. Data Locality Fit

Measures whether the model stores data the way the application retrieves it.

| Score | Meaning |
|-------|---------|
| 5 | Data is almost always retrieved as a single unit; the model stores it that way (document as one JSON blob, graph vertex with inline properties). One query = one retrieval. |
| 4 | Data is usually retrieved as a unit; occasional secondary lookups for referenced data. |
| 3 | Data is retrieved partially as a unit (some subordinate data inline, some via join/reference). |
| 2 | Multiple queries or joins required for most primary reads. |
| 1 | Every primary read requires joining 3+ entity types or following multiple document references. |

**Notes:**
- Document model locality advantage applies only when documents are small and loaded whole. Large documents (>100KB) or partial-access patterns eliminate the advantage.
- Relational databases with row interleaving (Google Spanner, Oracle cluster tables) can match document locality.
- Graph vertex properties are inline; edge traversal requires index lookups — locality varies by query.

---

### 2. Relationship Complexity Fit

Measures whether the model is designed for the relationship types present in the data.

| Score | Meaning |
|-------|---------|
| 5 | Model is designed exactly for the relationship type present: document for one-to-many trees, relational for many-to-many normalized, graph for variable-depth traversal. |
| 4 | Model handles the relationships with minor workarounds (relational for shallow graph traversal with fixed-depth joins, document with occasional cross-document references). |
| 3 | Model can emulate the relationship type, but with application-side complexity (document model emulating many-to-many with application-side joins). |
| 2 | Key relationship types are awkward in this model; significant complexity moves to application layer. |
| 1 | Model is a poor fit; the primary relationship type cannot be expressed without major workarounds. |

**Decision rule trigger:** If document model scores 2 or below on this criterion, Rule 1 (document model) does not apply. Escalate to Rule 2 (relational) or Rule 3 (graph).

---

### 3. Schema Flexibility

Measures whether the model accommodates heterogeneous or frequently evolving record structure.

| Score | Meaning |
|-------|---------|
| 5 | Records naturally have different structures within the same collection; schema-on-read is the natural fit. |
| 4 | Records are mostly similar but with meaningful variation (optional fields, polymorphic types). |
| 3 | Records are mostly uniform; occasional heterogeneity manageable. |
| 2 | Records are uniform; schema enforcement is desirable but adds overhead. |
| 1 | All records have identical structure; schema enforcement is strictly beneficial. |

**Note:** Schema flexibility scoring is independent of model choice. PostgreSQL with JSON columns can score 4–5 on this criterion while still being a relational model.

---

### 4. Query Pattern Support

Measures how naturally the model's native query language handles primary read patterns.

| Score | Meaning |
|-------|---------|
| 5 | Primary queries are expressed directly in the model's native language with no workarounds. |
| 4 | Primary queries are well-supported; secondary queries require minor workarounds. |
| 3 | Primary queries are possible but verbose or require features not universally supported (e.g., JSON path expressions, recursive CTEs). |
| 2 | Primary queries require combining multiple queries or significant application-side processing. |
| 1 | Primary queries cannot be expressed efficiently; require application-level emulation. |

**Signal:** If relational scores 1–2 on this criterion due to graph traversal requirements, this is the canonical signal for graph model. The 29-line recursive CTE is the concrete indicator.

---

### 5. Normalization Requirement

Measures how important it is that shared data has a single source of truth.

| Score | Meaning |
|-------|---------|
| 5 | Shared data is referenced by many records; update anomalies are a serious correctness risk without normalization. |
| 4 | Normalization is important; some shared data across records. |
| 3 | Some duplication is acceptable; data changes rarely enough that update anomalies are manageable. |
| 2 | Most data is entity-specific; normalization adds overhead without major benefit. |
| 1 | All data is unique to each record; denormalization has no downside. |

**Note:** Normalization scores high when: shared reference data exists (regions, categories, organizations), data is updated (not append-only), multiple records reference the same entity.

---

## Pre-filled Scores: 8 Common System Types

### 1. User Profile Service (LinkedIn-style résumé)

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         2 |        5 |     1 |
| Relationship complexity|         4 |        5 |     2 |
| Schema flexibility     |         3 |        4 |     3 |
| Query pattern support  |         3 |        5 |     1 |
| Normalization          |         4 |        3 |     3 |
| **Total**              |        16 |       22 |    10 |

**Recommendation:** Document  
**Key reason:** One-to-many tree (user → positions, education, contact_info); whole profile fetched together  
**Watch for:** When organizations become entities (many-to-many) — migrate toward relational or polyglot

---

### 2. E-commerce Platform

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         3 |        2 |     2 |
| Relationship complexity|         5 |        1 |     3 |
| Schema flexibility     |         3 |        4 |     2 |
| Query pattern support  |         5 |        2 |     2 |
| Normalization          |         5 |        1 |     3 |
| **Total**              |        21 |       10 |    12 |

**Recommendation:** Relational  
**Key reason:** Products, categories, orders, reviews form many-to-many; normalization prevents product name update anomalies across thousands of orders  
**Watch for:** Product attribute heterogeneity (electronics vs. clothing attributes) — use JSON columns in PostgreSQL for this specific case while keeping relational model overall

---

### 3. Social Network / Friend Graph

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         2 |        2 |     5 |
| Relationship complexity|         2 |        1 |     5 |
| Schema flexibility     |         3 |        4 |     5 |
| Query pattern support  |         2 |        1 |     5 |
| Normalization          |         4 |        2 |     4 |
| **Total**              |        13 |       10 |    24 |

**Recommendation:** Graph  
**Key reason:** Variable-depth traversal (friends-of-friends, 6 degrees), multiple entity types (people, posts, events, groups) connected by multiple relationship types  
**Subtype:** Property graph (Neo4j) — connection properties (when friended, interaction weight) matter; Cypher patterns match social queries naturally

---

### 4. IoT Time-Series (Sensor Data)

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         3 |        5 |     1 |
| Relationship complexity|         4 |        4 |     1 |
| Schema flexibility     |         2 |        4 |     3 |
| Query pattern support  |         3 |        4 |     1 |
| Normalization          |         4 |        3 |     2 |
| **Total**              |        16 |       20 |     8 |

**Recommendation:** Document (or time-series database)  
**Key reason:** Each event is a self-contained record (device_id, timestamp, readings); events are never joined to other events; schema varies by sensor type  
**Note:** For very high ingest rates, a purpose-built time-series database (InfluxDB, TimescaleDB) may outperform a general document store — but the data model is document-like in either case

---

### 5. Content Management System (CMS)

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         2 |        5 |     2 |
| Relationship complexity|         4 |        3 |     3 |
| Schema flexibility     |         2 |        5 |     4 |
| Query pattern support  |         4 |        4 |     2 |
| Normalization          |         4 |        3 |     3 |
| **Total**              |        16 |       20 |    14 |

**Recommendation:** Document (with relational for structured metadata)  
**Key reason:** Content is heterogeneous (articles have different fields from products, events, etc.); each content item is a self-contained unit fetched whole  
**Polyglot note:** User accounts, permissions, and structured metadata often fit relational; content bodies and rich media fit document — CMS is a classic polyglot use case

---

### 6. Fraud Detection / Anti-Money Laundering

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         2 |        1 |     4 |
| Relationship complexity|         2 |        1 |     5 |
| Schema flexibility     |         3 |        3 |     5 |
| Query pattern support  |         1 |        1 |     5 |
| Normalization          |         4 |        2 |     4 |
| **Total**              |        12 |        8 |    23 |

**Recommendation:** Graph  
**Key reason:** Fraud queries are path-finding and cluster-detection by nature (shared device, IP rings, mule account networks); variable-depth traversal is the primary operation  
**Subtype:** Property graph — edge properties (transaction amounts, timestamps) are queried; Cypher pattern matching maps directly to fraud pattern expressions  
**Polyglot note:** Keep relational for the transaction ledger (compliance reporting, aggregation); use graph for traversal and pattern matching only

---

### 7. ERP / Enterprise Business Application

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         3 |        2 |     2 |
| Relationship complexity|         5 |        1 |     3 |
| Schema flexibility     |         2 |        3 |     3 |
| Query pattern support  |         5 |        2 |     2 |
| Normalization          |         5 |        1 |     3 |
| **Total**              |        20 |        9 |    13 |

**Recommendation:** Relational  
**Key reason:** ERP data is the canonical many-to-many, normalized use case — customers reference orders reference products reference vendors reference accounts. Normalization is not optional; update anomalies in billing or inventory data are business-critical failures  
**Note:** ERP is why the relational model was invented and where it remains the strongest choice

---

### 8. Recommendation Engine

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         2 |        3 |     4 |
| Relationship complexity|         2 |        2 |     5 |
| Schema flexibility     |         3 |        4 |     5 |
| Query pattern support  |         2 |        2 |     5 |
| Normalization          |         3 |        2 |     4 |
| **Total**              |        12 |       13 |    23 |

**Recommendation:** Graph  
**Key reason:** Recommendation queries are "users who bought X also bought Y" or "find items similar to Z via shared attributes" — these are graph traversal queries (user → item → user → item chains)  
**Subtype:** Property graph — similarity weights, interaction types (viewed, purchased, rated), and timestamps on edges matter for ranking  
**Alternative:** Collaborative filtering at scale often uses matrix factorization (not a graph query), which can run on top of any model. Graph is optimal for neighborhood-based recommendations; matrix factorization can use document or relational storage.

---

## Query Pattern to Model Fit Mapping

| Query pattern | Natural model | Workaround cost in alternatives |
|--------------|--------------|--------------------------------|
| Fetch entire entity with all subordinate data | Document | Relational: multi-table join (medium). Graph: vertex + edge traversal (medium). |
| Join multiple entity types | Relational | Document: application-side join (high). Graph: pattern match (low-medium). |
| Find all X connected to Y within N hops | Graph | Relational: recursive CTE (high). Document: not feasible without graph-like indexing. |
| Aggregate across all records (GROUP BY, SUM) | Relational | Document: aggregation pipeline (medium). Graph: awkward (high). |
| Full-text search within records | Relational (with FTS extensions) or dedicated search index | All models benefit from a dedicated search index (Elasticsearch) regardless of primary model. |
| Retrieve record by ID | All models (similar cost) | No meaningful difference for simple key lookups. |
| Heterogeneous records with different fields | Document | Relational: JSON columns (low). Graph: schema-free (low). |
| Variable-depth path traversal | Graph | Relational: WITH RECURSIVE (high — verbose, slow for deep paths). Document: not supported. |
| Pattern matching across connections | Graph | Relational: self-joins or recursive CTEs (high). Document: not supported. |

---

## Relationship Type Quick Reference

| Relationship type | Definition | Natural model | Example |
|-------------------|-----------|--------------|---------|
| One-to-one | Each A has exactly one B | Relational or Document | User ↔ UserProfile |
| One-to-many | Each A has many B; B belongs to one A | Document (if B is always fetched with A) or Relational | User → Orders |
| Many-to-one | Many A reference one B (normalization) | Relational | Many Users → one Region |
| Many-to-many | A references many B; B referenced by many A | Relational | Products ↔ Categories |
| Variable-depth traversal | Follow relationship chains of unknown length | Graph | Friends-of-friends, shortest path, cluster detection |
| Heterogeneous graph | Multiple entity types and relationship types in one store | Graph | Social graph (people, posts, events, groups, comments) |

---

## Schema Strategy Decision Tree

```
Is data structure uniform across all records?
├── Yes → Are multiple services writing to the same database?
│         ├── Yes → Schema-on-write (enforced)
│         └── No → Schema-on-write preferred; schema-on-read acceptable
└── No → Why is it heterogeneous?
          ├── Different object types (event types, product categories) → Schema-on-read
          ├── Externally controlled structure (third-party API, webhook payload) → Schema-on-read
          └── Evolving fields (rolling out new fields incrementally) → Schema-on-read
```

---

## Convergence: What Modern Databases Support Across Model Lines

| Capability | Relational | Document | Graph |
|-----------|-----------|----------|-------|
| JSON document storage | PostgreSQL 9.3+, MySQL 5.7+, SQL Server | Native | Via vertex properties |
| Joins | Native (SQL) | RethinkDB native; MongoDB limited | Via traversal |
| Schema enforcement | Native (DDL) | Optional (JSON Schema) | Optional (constraints) |
| Graph traversal | WITH RECURSIVE (SQL:1999) | Not supported | Native (Cypher, SPARQL) |
| Full-text search | Native (FTS) or via extension | Via text index | Via external index |
| Aggregation | Native (GROUP BY, window functions) | Aggregation pipeline | Limited |
| ACID transactions | Native | Varies by product | Varies by product |

**Implication:** If your primary model is relational, JSON columns cover most document flexibility needs. If your primary model is document, RethinkDB covers most join needs. The models are converging — optimize for data shape fit first, then check whether your target product covers secondary needs.
