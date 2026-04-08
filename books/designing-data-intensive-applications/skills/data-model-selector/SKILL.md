---
name: data-model-selector
description: |
  Choose between relational, document, and graph data models for an application by analyzing data shape, relationship complexity, and query patterns. Use when asked "should I use MongoDB or PostgreSQL?", "when does a graph database make sense?", "how do I choose between SQL and NoSQL?", or "what data model fits my access patterns?" Also use for: evaluating impedance mismatch between data model and application code; deciding schema-on-read vs. schema-on-write for heterogeneous data; diagnosing whether many-to-many relationships call for relational or graph model; choosing between property graphs and triple-stores; deciding when polyglot persistence is appropriate. Produces a concrete recommendation with trade-off analysis — not "it depends." Covers relational (PostgreSQL, MySQL), document (MongoDB, CouchDB), and graph (Neo4j, Datomic) models including schema enforcement strategies and data locality trade-offs.
  For storage engine internals (LSM-tree vs B-tree), use storage-engine-selector instead. For OLTP vs. analytics routing, use oltp-olap-workload-classifier instead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/data-model-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [2]
tags: [data-model, relational, document, graph, nosql, schema-on-read, schema-on-write, data-locality, joins, many-to-many, polyglot-persistence, neo4j, mongodb, postgresql, property-graph, triple-store, cypher, sparql, architecture-decision]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "System description, data relationship description, and expected query patterns — as a written brief, existing schema files (.sql, .json), architecture document, or codebase to analyze"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with pasted descriptions, schema files, docker-compose.yml, or architecture.md documents."
discovery:
  goal: "Produce a concrete data model recommendation with trade-off analysis — not a balanced overview of options"
  tasks:
    - "Classify data shape (tree-structured vs. interconnected graph vs. tabular)"
    - "Score each model against relationship complexity, join requirements, schema flexibility needs, and query patterns"
    - "Identify schema enforcement strategy (schema-on-read vs. schema-on-write)"
    - "Analyze data locality requirements"
    - "Produce a recommendation document with trade-off rationale and implementation guidance"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "tech-lead", "technical-manager"]
    experience: "intermediate-to-advanced — assumes familiarity with relational databases and SQL"
  triggers:
    - "User is designing a new system and needs to choose a database model"
    - "User has an existing system with schema complexity or join explosion symptoms"
    - "User is evaluating document databases (MongoDB, CouchDB, RethinkDB) vs. relational"
    - "User has graph-like data (social networks, recommendation engines, fraud detection, routing)"
    - "User is experiencing object-relational impedance mismatch and wants to know if document model helps"
    - "User needs to decide between schema-on-read and schema-on-write for a heterogeneous data source"
    - "User wants to validate whether their current data model fits their access patterns"
  not_for:
    - "Choosing specific databases within a model (e.g., PostgreSQL vs. MySQL, MongoDB vs. CouchDB) — this skill selects the model, not the product"
    - "Storage engine selection (LSM-tree vs. B-tree) — use storage-engine-selector"
    - "Partitioning strategy for distributed deployments — use partitioning-strategy-advisor"
    - "Replication topology decisions — out of scope for this skill"
---

# Data Model Selector

## When to Use

You are designing a new system or evaluating an existing one and need to decide how to structure your data: relational tables with joins, self-contained documents with nested structure, or a graph of vertices and edges.

This skill applies when:
- You are choosing a data model before picking a specific database product
- Your application code has become complex managing joins or object-relational translation
- You have data with heterogeneous structure or schema requirements that vary per record
- You are seeing many-to-many relationships proliferating and are unsure whether relational or graph is the right solution
- You want to document the trade-off rationale for an architecture decision record

**This skill selects the model, not the product.** Once you have a recommendation, proceed to product selection based on operational requirements (replication, consistency guarantees, operational complexity). For storage engine decisions within your chosen model, see `storage-engine-selector`. For partitioning strategy once you have a model and product, see `partitioning-strategy-advisor`.

---

## Context & Input Gathering

Before running the decision framework, collect:

### Required
- **Data shape description:** What entities exist in your system, and how do they relate to each other? (e.g., "users have many orders, orders have many line items, line items reference products")
- **Relationship type:** Are relationships one-to-many (tree structure), many-to-many (network), or highly interconnected (graph)? Do you know the depth of nesting?
- **Primary query patterns:** How will data most commonly be read? By single entity ID? By traversing relationships? By aggregation across many records? By pattern-matching across connections?
- **Schema stability:** Is your data structure uniform across all records, or does it vary (different fields per record type, externally controlled structure, frequently evolving fields)?

### Important
- **Join frequency expectations:** Will your application routinely query data that spans multiple entity types, or mostly retrieve a single entity and all its associated data at once?
- **Write pattern:** Is data written as complete self-contained units, or updated field-by-field with references to other entities?
- **Team/existing stack:** What models does your team already operate? (Operational familiarity is a legitimate factor in model selection.)

### Optional (improves recommendation precision)
- **Existing schema files:** Provide `.sql`, `.json` schema, or ORM model definitions for analysis
- **Architecture or data flow documents:** Help identify implied relationships not stated explicitly
- **Application code with data access patterns:** ORM queries, aggregation pipelines, or graph traversals reveal actual access patterns vs. assumed ones

If the data shape and relationship description are missing, ask for them before proceeding. A model recommendation without relationship complexity analysis is unreliable.

---

## Process

### Step 1: Classify the Data Shape

**Action:** Determine the primary structure of your data. Every data model has a structural assumption — violate it, and complexity moves into your application code.

**WHY:** The three models evolved to solve different structural problems. The hierarchical model (predecessor to document databases) worked for one-to-many tree structures but broke on many-to-many relationships. The relational model solved many-to-many but introduced a translation layer between objects and tables. Graph databases are the right tool when connections between entities are as important as the entities themselves. Choosing a model that matches your data's natural structure minimizes the impedance mismatch between your application and your storage layer — meaning less translation code, simpler queries, and a data model that evolves naturally with your application.

Identify which category best describes your data:

**Category A — Tree structure (one-to-many, self-contained)**
- Each primary entity has subordinate data that "belongs to" it
- Subordinate data is accessed almost always together with the parent (user + all their profile data; order + all its line items)
- Relationships between different top-level entities are rare or non-existent
- Example: a résumé — one user, many positions, many education records, many contact items; rarely do positions reference other positions

**Category B — Interconnected entities (many-to-many, tabular)**
- Multiple entity types reference each other in both directions
- You need to join across entity types routinely to answer queries
- Normalization matters: you want a single source of truth for shared data (e.g., one record for each city, referenced by many users)
- Example: e-commerce — users place orders, orders contain products, products have categories, users write reviews of products

**Category C — Highly connected graph (many-to-many with traversal)**
- Relationships between entities are as important as the entities themselves
- Queries require following chains of relationships of variable or unknown depth
- Different types of entities and relationship types are mixed in a single data store
- Example: social network — people know people who know people; fraud detection — transactions connect accounts, devices, IP addresses; routing — roads connect junctions across variable-length paths

---

### Step 2: Score Each Model Against Your Data

**Action:** Apply the five-criteria scoring rubric to rate each model's fit. Score each criterion 1–5 per model.

**WHY:** Scoring all three models — even the obvious misfits — forces explicit trade-off reasoning. Practitioners who skip this step often discover later that their "obvious" choice scores poorly on a criterion they hadn't considered (e.g., choosing a document model for "flexibility" without noticing that many-to-many relationships are already present, which will require application-side join emulation). Running the full rubric also produces the rationale needed for an architecture decision record.

**Scoring criteria:**

**1. Data locality fit** — Does the model match how data is naturally retrieved?
- 5 = Data is almost always fetched as a single unit. The model stores it that way.
- 3 = Data is sometimes fetched as a unit, sometimes across entities.
- 1 = Data is routinely fetched by joining many separate entities.

**2. Relationship complexity fit** — Does the model handle the relationship types present?
- 5 = Model is designed for the relationship types present (tree for document, normalized for relational, graph for traversal).
- 3 = Model can emulate the relationship type but with added application-side complexity.
- 1 = Model is a poor fit; relationships must be emulated awkwardly (e.g., document model for many-to-many, relational for variable-depth traversal).

**3. Schema flexibility** — Does the model handle heterogeneous or evolving record structures?
- 5 = Records naturally have different structures; the model imposes no schema.
- 3 = Records are mostly uniform; occasional variation manageable.
- 1 = All records have the same structure; enforcing a schema is an asset.

**4. Query pattern support** — Does the model's native query language match how you will query?
- 5 = Primary queries are natively supported (SQL joins for relational, document retrieval for document, Cypher traversal for graph).
- 3 = Queries are possible but require workarounds (recursive CTEs in SQL for graph traversal, application-side joins in document databases).
- 1 = Primary queries require the model to be emulated in a way that's significantly slower or more complex.

**5. Normalization requirement** — Does the model support the deduplication level your data needs?
- 5 = Model naturally enforces a single source of truth for shared data.
- 3 = Partial normalization possible with workarounds.
- 1 = Model encourages denormalization, creating update anomalies for shared data.

**Score each model:**

```
                    Relational  Document  Graph
Data locality            [1-5]     [1-5]  [1-5]
Relationship complexity  [1-5]     [1-5]  [1-5]
Schema flexibility       [1-5]     [1-5]  [1-5]
Query pattern support    [1-5]     [1-5]  [1-5]
Normalization            [1-5]     [1-5]  [1-5]
Total                    [5-25]    [5-25] [5-25]
```

See `references/decision-matrix.md` for a pre-filled scoring guide with example systems and their typical scores.

---

### Step 3: Apply the Decision Rules

**Action:** Apply explicit if/then decision rules to produce a primary model recommendation. These rules encode the structural logic of the chapter's analysis — they are not heuristics, but direct consequences of how each model handles relationships.

**WHY:** Scoring produces numbers; decision rules produce a recommendation. The rules encode the non-obvious consequences of model choice that practitioners discover only after the fact: document model users discovering that many-to-many relationships require application-side join emulation; relational model users discovering that object-relational impedance mismatch creates thousands of lines of translation code; graph database adopters discovering that simple one-to-many queries are awkward in Cypher. The rules prevent these surprises.

**Rule 1 — Use the document model if ALL of the following are true:**
- Your data has mostly one-to-many relationships (tree structure, Category A)
- You typically fetch all subordinate data together with the parent entity in one query
- Many-to-many relationships are rare or absent today — and features on your roadmap are unlikely to introduce them
- Records in your collection have heterogeneous structure (different fields per type, or externally controlled structure), making schema enforcement more hindrance than help
- Documents can be kept small (locality advantage degrades sharply for large documents loaded partially)

**Rule 2 — Use the relational model if ANY of the following are true:**
- Many-to-many relationships are already present or expected as features evolve
- You need a single source of truth for shared data (normalization to avoid update anomalies)
- Your query patterns require joining across multiple entity types
- Records have uniform structure and you want the database to enforce schema correctness
- You need full-text search, aggregations, or reporting across many records simultaneously
- Your application is evolving rapidly and you want to add query patterns without restructuring data

**Rule 3 — Use the graph model if ALL of the following are true:**
- Anything is potentially related to everything — connection patterns are as important as the entities
- Queries require following chains of relationships of variable or unknown depth (e.g., "find all friends-of-friends," "shortest path between two nodes," "all transactions connected to this account within 3 hops")
- You have multiple entity types and multiple relationship types coexisting in a single data store
- Relationships themselves carry properties (timestamp, weight, type label) that you need to query

**Rule 4 — Consider polyglot persistence if:**
- Different subsystems of your application clearly fall into different categories (e.g., the user profile is Category A, the recommendation engine is Category C)
- Operational complexity of running multiple datastores is acceptable
- The performance or expressiveness benefit of model specialization outweighs the operational cost

**Tie-breaker when rules conflict:** The relationship complexity criterion is the primary tie-breaker. Many-to-many relationships are the historical dividing line between models — they are why the relational model was invented (to solve the hierarchical model's many-to-many problem) and why graph databases exist (to handle cases where relational joins become impractical). If many-to-many relationships are present or expected, the document model is strongly contraindicated.

---

### Step 4: Analyze Schema Enforcement Strategy

**Action:** Determine whether schema-on-read or schema-on-write is appropriate, independent of the model choice. Note that most relational databases now support document-like JSON columns, and most document databases are adding join-like capabilities — model convergence means this is increasingly a configuration choice, not just a database product choice.

**WHY:** Schema-on-read (structure is implicit, interpreted by application code at read time) vs. schema-on-write (structure is explicit, enforced by the database at write time) is a distinct decision from model selection, but it profoundly affects how easily your data can evolve. Schema-on-write is like static type checking: it catches structural errors at write time, provides documentation, and makes queries predictable. Schema-on-read is like dynamic type checking: it is more flexible, tolerates heterogeneous records, but pushes structural validation into application code. Neither is superior — the right choice depends on whether your records have heterogeneous structure and how rapidly your schema evolves.

**Prefer schema-on-write (relational enforced schema, JSON Schema validation) when:**
- All records are expected to have the same structure
- Multiple applications or services write to the same database (shared schema is the contract)
- You want the database to catch structural errors before bad data enters
- Schema changes are infrequent and go through a migration process

**Prefer schema-on-read (document databases, JSON columns without schema validation) when:**
- Records have different structures within a collection (many types of events, different product attributes, externally-sourced data)
- Structure is controlled by an external system you don't own and that may change
- You need to roll out schema changes incrementally (new fields written by new code, old fields still read by old code simultaneously)

**Schema-on-read migration pattern:** When changing a field format, write new documents with new fields and handle both old and new format at read time in application code — no migration required.

**Schema-on-write migration pattern:** Use `ALTER TABLE` + `UPDATE`. Schema changes have a reputation for downtime that is mostly undeserved — PostgreSQL executes most `ALTER TABLE` in milliseconds; MySQL is the exception (full table copy). See `references/decision-matrix.md` for tooling options.

---

### Step 5: Evaluate Data Locality

**Action:** Determine whether data locality is a meaningful performance factor for your application, and whether it argues for or against the document model.

**WHY:** The document model's storage locality advantage — all related data stored as a single continuous string, fetched in one disk read — is real but conditional. It only matters if you need large parts of the document at the same time. If you access only part of a document (e.g., you only need the user's name, not all their positions and education history), the database still loads the entire document — making locality wasteful. For documents that are large or frequently partially accessed, relational row-level access is more efficient. Furthermore, on writes, modifying a document that grows in size usually requires rewriting the entire document. Keep this in mind: locality is an advantage only when documents are small and accessed whole.

**Locality strongly favors document model when:**
- The entire document is rendered or processed together on most reads (e.g., rendering a profile page, sending a complete order to a fulfillment service)
- Documents are small (kilobytes, not megabytes)
- Write patterns append or replace the whole document rather than updating individual fields

**Locality advantage is diminished when:**
- You routinely access only a small subset of a document's fields
- Documents grow large over time (accumulated history, logs, nested lists)
- High write throughput updates individual fields rather than replacing whole documents

Note: Locality is not unique to document databases. Google Spanner's interleaved tables and Oracle's multi-table index cluster tables bring locality to relational models. Cassandra and HBase use column families for locality. If locality is the primary driver, evaluate whether your target relational database offers nested table features before switching models entirely.

---

### Step 6: Assess Graph Model Subtypes (if applicable)

**Action:** If the graph model scored highest in Steps 2–3, determine which graph subtype is appropriate: property graph or triple-store.

**WHY:** Both subtypes model the same underlying graph structure (vertices and edges with properties), but they use different storage formats, query languages, and tooling. The property graph model (Neo4j, Titan, InfiniteGraph) stores structured property key-value pairs on vertices and edges and uses the Cypher query language. The triple-store model (Datomic, AllegroGraph) stores all information as subject-predicate-object triples and uses SPARQL or Datalog. The choice matters because it determines your query language, ecosystem, and how naturally your data maps to the storage format. For most application development use cases, property graphs are the more practical starting point. Triple-stores become more relevant when you need to combine data from multiple external sources (the original motivation for RDF and SPARQL).

**Property graph (Neo4j) is appropriate when:**
- Vertices and edges are well-defined entities with named properties
- You need to query traversals expressively (Cypher reads like ASCII-art of graph patterns)
- Your data is primarily internal to your application
- You need good tooling, visualization, and community support

**Triple-store (RDF/SPARQL) is appropriate when:**
- You need to merge data from multiple external sources with different schemas
- You want to leverage the semantic web ecosystem (linked data, ontologies)
- Your team already uses Datalog-family languages (Datomic)
- You need maximum flexibility in predicate types (RDF treats properties and relationships uniformly as predicates)

**Graph traversal in relational databases:** SQL supports variable-depth traversal via recursive common table expressions (`WITH RECURSIVE`). The same query that takes 4 lines in Cypher typically takes 29 lines in SQL. If graph queries are occasional (not primary), staying in a relational model with `WITH RECURSIVE` is a viable option. If traversal queries are central to your application, a native graph model pays for itself quickly in query expressiveness and performance.

---

### Step 7: Produce the Recommendation Document

**Action:** Write a structured recommendation that covers the primary model, the rationale, key trade-offs, what was ruled out and why, and implementation guidance.

**WHY:** A recommendation without explicit rationale cannot be reviewed, challenged, or revised when requirements change. Stating what was ruled out — and why — is as important as stating what was chosen: it prevents the recommendation from being relitigated by team members who weren't present for the analysis, and it records the assumptions so that if those assumptions change (e.g., a many-to-many relationship is added), the decision can be revisited.

**Output format:**

```
## Data Model Recommendation

**System:** [System name / brief description]
**Date:** [Date]

---

### Recommended Model: [Relational / Document / Graph / Polyglot]

**Primary rationale:** [1–2 sentences connecting the data shape and relationship 
complexity analysis to the model choice]

**Data shape classification:** [Category A (tree) / B (interconnected) / C (graph)]

---

### Scoring Summary

| Criterion             | Relational | Document | Graph |
|-----------------------|-----------|----------|-------|
| Data locality         |     [1-5] |    [1-5] | [1-5] |
| Relationship complexity|    [1-5] |    [1-5] | [1-5] |
| Schema flexibility    |     [1-5] |    [1-5] | [1-5] |
| Query pattern support |     [1-5] |    [1-5] | [1-5] |
| Normalization         |     [1-5] |    [1-5] | [1-5] |
| **Total**             |    [5-25] |   [5-25] | [5-25]|

**Winner:** [Model] with [score]/25

---

### Key Trade-offs of the Recommended Model

**Strengths for this system:**
- [Specific strength tied to your data shape]
- [Specific strength tied to your query patterns]

**Limitations to manage:**
- [Specific limitation and how to mitigate it]
- [Specific limitation and how to mitigate it]

---

### Schema Enforcement Strategy

**Recommendation:** Schema-on-[read/write]
**Rationale:** [Why this fits the data heterogeneity and team workflow]

---

### Ruled Out

**[Model]:** [1–2 sentences on why it scored lower and what specific criterion failed]
**[Model]:** [1–2 sentences on why it scored lower]

---

### Implementation Guidance

**Immediate next steps:**
1. [Concrete first step]
2. [Concrete second step]

**Watch for:**
- [Specific signal that would indicate the model choice needs revisiting]
- [Specific signal]

**Related decisions:**
- Storage engine selection: see storage-engine-selector
- Partitioning strategy: see partitioning-strategy-advisor (if distributing)
```

---

## What Can Go Wrong

These are the most common failure modes when selecting a data model. Review each before finalizing a recommendation.

**Choosing document model for "flexibility," then adding many-to-many relationships later.**
The document model's join support is weak by design. When many-to-many relationships appear (as they almost always do as applications evolve — organizations become entities, recommendations reference users, tags cross-reference content), the join work moves into application code. Application-side joins are slower than database joins (multiple round trips vs. optimized index lookups inside the database) and create significant complexity. If your roadmap includes any features that create cross-entity references, score the relational model at least as a baseline.

**Treating "schemaless" as "no schema."**
Document databases don't eliminate schema — they move it from the database into the application code that reads data. This is sometimes called the implicit schema problem. Every piece of code that reads a document assumes something about its structure. When that structure changes, all reading code must be updated. The difference from schema-on-write is that the database cannot help you find all the places where the assumption was made. Budget for the discipline required to manage implicit schemas.

**Using graph query syntax for simple data.**
Graph databases excel at traversal queries (variable-depth path following). For simple one-to-many reads, Cypher is more verbose than SQL, and a graph database adds operational complexity without benefit. Do not choose a graph model because your data "could" be a graph — choose it because your primary queries require graph traversal.

**Underestimating the impedance mismatch tax.**
If your application code uses objects, and your data store uses tables with rows, every read and write passes through a translation layer (ORM). ORMs reduce boilerplate but cannot eliminate the impedance mismatch. When this translation layer becomes a bottleneck (complex join queries expressed as object graphs, N+1 query problems, schema migrations that require coordinating application and database changes simultaneously), it is a signal that the data shape mismatches the model — not that the ORM is inadequate.

**Choosing model based on write throughput alone, ignoring read patterns.**
NoSQL databases were partly adopted for write scalability. But the data model decision (relational vs. document vs. graph) is a separate concern from the scalability decision. A relational database can scale writes with appropriate partitioning. A document database with many-to-many relationships will have read complexity problems regardless of how fast it writes. Separate the model-fit question from the scalability question.

**Locking in on a model before the data shape is understood.**
Starting with a document database because JSON is "natural for web applications" without first analyzing relationship complexity is a common path to regret. Run Step 1 (data shape classification) before any other discussion. If the shape is not yet clear because the product is early-stage, prefer relational: it can be refactored to document or graph more easily than the reverse, because it enforces the normalization that makes data portable.

---

## Inputs / Outputs

### Inputs
- System description or data entity list (required)
- Relationship description between entities (required)
- Primary query patterns (required)
- Schema stability assessment (required)
- Existing schema files or architecture documents (optional)
- Application code with data access patterns (optional)

### Outputs
- Data shape classification (Category A / B / C)
- Scored decision matrix (three models, five criteria)
- Primary model recommendation with rationale
- Schema enforcement strategy recommendation
- Graph subtype recommendation (if graph model selected)
- Ruled-out analysis for the other models
- Implementation guidance and watch signals

---

## Key Principles

**Data relationships are the primary decision axis.** The three models evolved to solve different relationship problems: the hierarchical model handled one-to-many, the relational model solved many-to-many, graph databases handle variable-depth traversal where relational joins become impractical. Map your data's relationship type to the model designed for it.

**Many-to-many relationships are the historical dividing line.** When many-to-many relationships appear, the document model loses its advantage — joins move into application code. The entire history of database systems (IMS → relational/network model debate of the 1970s) is the history of solving this problem. Do not repeat it by choosing a model that doesn't handle the relationships you have.

**Schema-on-read is not schemaless — it is implicit schema.** Every piece of code that reads a document assumes a structure. That assumption is your schema; the question is only whether the database enforces it (schema-on-write) or the application enforces it (schema-on-read). Use schema-on-read for heterogeneous records; schema-on-write when records are uniform and correctness must be enforced at write time.

**Document and relational databases are converging.** PostgreSQL 9.3+ supports JSON, MySQL 5.7+ supports JSON, RethinkDB supports joins, MongoDB reinvented SQL as an aggregation pipeline. The practical choice is increasingly about which model fits your data as primary — secondary capabilities are often available in either system.

---

## Examples

### Example 1: User Profile Service (SaaS Application)

**Scenario:** A SaaS application needs to store user profiles. Each profile contains basic info (name, email), job history (multiple positions with title and organization), education history (multiple schools with dates), and contact info (multiple URLs by type). The primary read pattern is: load the complete profile for display on a page. Cross-profile queries are rare — mostly search by email or user ID.

**Trigger:** "Should we use MongoDB or PostgreSQL for our user profiles?"

**Process:**
- Step 1: Category A — tree structure. Each user is the root; positions, education, contact_info are subordinate. Rarely queried across users.
- Step 2: Document scores high on locality (whole profile loaded together), relationship complexity (one-to-many tree is native), schema flexibility (profiles may have different contact types). Relational scores high on normalization but the normalization benefit is minimal here — organizations and schools are just strings, not shared entities referenced by multiple users.
- Step 3: Rule 1 applies — mostly one-to-many, fetch whole profile together, no many-to-many present.
- Watch for: If "organizations" become full entities (with their own pages, logos, employee counts — as LinkedIn did), the model needs to shift. Organization references become many-to-many (each résumé links to an organization entity, each organization is referenced by many résumés). At that point, document model requires application-side joins.

**Output:**
```
## Data Model Recommendation

**System:** User Profile Service

### Recommended Model: Document

**Primary rationale:** Profile data forms a self-contained tree — one user with 
many subordinate records that are always fetched together. The document model's 
locality advantage applies directly: one query returns the complete profile.

**Data shape classification:** Category A (tree, one-to-many)

### Scoring Summary

| Criterion              | Relational | Document | Graph |
|------------------------|-----------|----------|-------|
| Data locality          |         2 |        5 |     1 |
| Relationship complexity|         4 |        5 |     2 |
| Schema flexibility     |         3 |        4 |     4 |
| Query pattern support  |         3 |        5 |     1 |
| Normalization          |         5 |        3 |     3 |
| **Total**              |        17 |       22 |    11 |

**Winner:** Document with 22/25

### Key Trade-offs

**Strengths:**
- One query fetches a complete profile; no joins
- Flexible contact_info types (blog, twitter, phone) without schema changes

**Limitations to manage:**
- If organizations become shared entities, many-to-many appears — reassess model
- Application must manage implicit schema (validate structure at write time in code)

### Schema Enforcement Strategy

**Recommendation:** Schema-on-read
**Rationale:** Contact info types vary per user; new contact types can be added 
without migration. Application validates structure at write time.

### Ruled Out

**Relational:** Normalized representation requires multi-table joins on every 
profile read; locality benefit is lost. Normalization benefit is minimal since 
organizations and schools are not shared entities needing deduplication.
**Graph:** No traversal queries; no many-to-many relationship patterns present.

### Implementation Guidance

1. Store each profile as a single document; keep documents under ~16KB
2. Index on user_id and email for primary lookup patterns
3. Monitor for feature requests that add cross-profile references (organization entities, recommendations from other users) — these signal relational migration

**Watch for:** Any feature where one user's data references another user's data 
(recommendations, shared organization entities) — this introduces many-to-many 
and breaks the document model's join-free assumption.
```

---

### Example 2: E-commerce Platform

**Scenario:** An e-commerce platform has: users, orders, order line items, products, product categories, and reviews. Users write reviews of products. Products belong to multiple categories. Orders reference products. The team needs analytics queries (top products by category, revenue by user segment). The team currently uses MongoDB and is experiencing complex application-side join code.

**Trigger:** "Our MongoDB queries are getting complex and we're doing a lot of application-side joining. Should we migrate to PostgreSQL?"

**Process:**
- Step 1: Category B — interconnected entities. Products are referenced by orders, categories, and reviews. Users are referenced by orders and reviews. Queries span multiple entity types.
- Step 2: Many-to-many relationships are present throughout (products ↔ categories, users ↔ products via reviews). Relational model's join support is exactly what's missing. Document model's weakness (application-side joins) is the stated pain point.
- Step 3: Rule 2 applies — many-to-many relationships present, normalization needed (single source of truth for product data referenced by many orders and reviews), query patterns span entity types.
- Schema: Uniform structure per entity type; schema-on-write appropriate.

**Output (abbreviated — full format shown in Example 1):**
```
## Data Model Recommendation: E-commerce Platform

### Recommended Model: Relational (Score: 21/25 vs Document 9/25 vs Graph 13/25)

Primary rationale: Many-to-many relationships are pervasive (products ↔ categories,
users ↔ products via reviews, orders ↔ products). Application-side join complexity
is the document model failing at exactly what it was not designed for.

Schema strategy: Schema-on-write — entity types are uniform; multiple services 
write to the same database; schema is the contract.

Ruled out — Document: Application-side joins are the current pain point; migrating 
to another document store does not solve it.
Ruled out — Graph: Many-to-many but not variable-depth; SQL joins are sufficient.

Next steps:
1. Migrate one entity type at a time; start with products (most referenced)
2. Use PostgreSQL JSON columns for product attributes that vary by category

Related: See storage-engine-selector for covering index strategy on category + 
price range queries.
```

---

### Example 3: Fraud Detection System

**Scenario:** A financial services company needs to detect fraud by finding connections between transactions, accounts, devices, IP addresses, and known fraudsters. Queries include: "find all accounts connected to this device within 3 hops," "identify clusters of accounts that share IP addresses," "shortest path between a flagged account and any account in this transaction."

**Trigger:** "We're trying to build fraud detection. Our PostgreSQL queries for finding connected accounts are very slow — 29-table recursive CTEs. Would a graph database help?"

**Process:**
- Step 1: Category C — highly connected graph. Queries require variable-depth traversal. Connections between entities are as important as the entities. Multiple entity types (accounts, devices, IPs, transactions) coexist.
- Step 2: Graph model is native for traversal queries; relational requires `WITH RECURSIVE` which the team has already found unwieldy. The 29-line recursive CTE is the canonical signal that graph traversal in relational has exceeded its practical limit.
- Step 3: Rule 3 applies — variable-depth traversal is the primary query, multiple entity types and relationship types coexist, relationships carry properties (timestamp, amount).
- Subtype: Property graph (Neo4j) — data is internal, relationships carry properties (amounts, timestamps), Cypher is expressive for pattern-matching fraud queries.

**Output (abbreviated — full format shown in Example 1):**
```
## Data Model Recommendation: Fraud Detection System

### Recommended Model: Graph — Property Graph subtype (Score: 23/25)
Relational: 12/25. Document: 9/25.

Primary rationale: The 29-line recursive CTE is the canonical signal that graph 
traversal in relational has exceeded its practical limit. Variable-depth traversal 
(account → device → account → IP → account within N hops) is exactly what the 
property graph model is designed for.

Subtype rationale: Property graph (Neo4j) — data is application-internal, edge 
properties (amount, timestamp) must be queryable, Cypher pattern-matching maps 
directly to ring detection and shared-device cluster queries.

Schema strategy: Schema-on-read — fraud patterns require different vertex/edge 
property sets; heterogeneous structure is expected.

Ruled out — Relational: WITH RECURSIVE is syntactically clumsy and cannot use 
graph-optimized index structures; query expressiveness gap is the deciding factor.
Ruled out — Document: No traversal capability; relationship chain following is 
the entire problem.

Next steps:
1. Model as labeled vertices (Account, Device, IPAddress, Transaction) + labeled 
   edges (USES_DEVICE, SHARES_IP, TRANSFERS_TO) with amount/timestamp properties
2. Start with shared-device cluster detection as the first migrated query
3. Polyglot: keep relational for transaction ledger and compliance reporting

Watch for: If queries simplify to fixed-depth lookups (always 2 hops), 
re-evaluate whether SQL joins are sufficient.
```

---

## References

| File | Contents |
|------|----------|
| `references/decision-matrix.md` | Pre-filled scoring guide with 8 common system types (e-commerce, social network, IoT time-series, CMS, fraud detection, recommendation engine, ERP, analytics pipeline) showing typical scores per model and decision rationale; cross-reference table mapping query patterns to model fit |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
