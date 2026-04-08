---
name: batch-pipeline-designer
description: |
  Design batch data processing pipelines for large-scale, bounded datasets processed offline. Use when building ETL workflows, processing logs or clickstream data at scale, generating ML feature pipelines or search indexes, or joining two large datasets that cannot fit in memory. Trigger phrases: "design a batch pipeline", "should I use Spark or MapReduce", "how do I join two large datasets", "build an ETL workflow", "process server logs at scale", "how do I handle skewed data in joins", "implement PageRank on a distributed graph", "design an offline processing job". Covers MapReduce vs dataflow engines (Spark, Flink, Tez), three join strategies (sort-merge, broadcast hash, partitioned hash) with selection criteria, graph processing via the Pregel/BSP model, and fault tolerance via materialization vs recomputation. Does not apply to unbounded input streams (see stream-processing-designer) or low-latency OLTP query serving. Produces a pipeline architecture recommendation with engine choice, join strategy, and fault tolerance approach.
model: sonnet
context: 1M
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "System requirements, data flow diagrams, schema definitions, or architecture descriptions"
    - type: codebase
      description: "Existing pipeline code or infrastructure configs to understand current setup"
    - type: none
      description: "Skill can work from a verbal description of the processing requirements"
  tools-required: [Read, TodoWrite]
  tools-optional: [Grep, Bash]
  environment: "Can run from any directory; codebase access enables analysis of existing pipeline code"
depends-on:
  - oltp-olap-workload-classifier
---

# Batch Pipeline Designer

## When to Use

Use this skill when you are designing or evaluating a **batch processing pipeline** — a system that reads a bounded, fixed-size dataset, runs a job over it, and produces output. Batch jobs are scheduled periodically (hourly, daily), tolerate high latency, and are measured by throughput rather than response time.

This skill applies when:
- Processing large datasets offline (logs, clickstream, database snapshots, file dumps)
- Building ETL workflows to move data between systems
- Generating derived datasets: search indexes, ML training features, recommendation model inputs, aggregated reports
- Implementing multi-step data transformations across distributed storage
- Joining two or more large datasets that cannot fit in memory on a single machine
- Processing graph-structured data (social graphs, link graphs, dependency graphs) in bulk

**This skill does NOT apply to:**
- Stream processing where input is unbounded (see `stream-processing-designer`)
- Online query serving where latency < 1 second is required
- Transactional workloads (see `oltp-olap-workload-classifier` to confirm the workload type)

**Dependency check:** If the workload classification is uncertain, invoke `oltp-olap-workload-classifier` first to confirm this is a batch workload before proceeding.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Extract: data sources, transformations required, output destination
                    ↓
Environment → Check: existing pipeline code, schema files, infrastructure configs
                    ↓
Gap analysis → Do I know the input volume, join requirements, latency tolerance?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time)
                    │
                    NO
                    ↓
              PROCEED with pipeline design
```

### Required Context (must have — ask if missing)

- **Input data characteristics:** What datasets are being processed? What are their approximate sizes?
  → Check prompt for: dataset names, "gigabytes", "terabytes", "millions of records", log file descriptions
  → Check environment for: schema files, data flow docs, existing pipeline configs
  → If still missing, ask: "What are the input datasets, and roughly how large is each one? (e.g., 100 GB user event log + 10 GB user profile database)"

- **Required transformations and joins:** What operations need to happen — filtering, aggregation, joins between datasets?
  → Check prompt for: SQL-like language ("group by", "join on", "aggregate"), descriptions of data enrichment or correlation
  → If still missing, ask: "What does the pipeline need to produce? For example: 'count page views per URL', 'join user events with user profiles', or 'build a feature matrix for ML training'."

- **Output destination:** Where does the processed data go — a database, search index, file system, another pipeline?
  → Check prompt for: destination systems, "load into", "write to", "serve via"
  → If still missing, ask: "Where does the output of this pipeline need to go, and how will it be consumed? (e.g., loaded into Elasticsearch, written to HDFS for downstream jobs, served via a key-value store)"

- **Latency tolerance:** Is this a daily job, hourly, or near-real-time? How long can the job take to complete?
  → Check prompt for: "daily", "hourly", "SLA", "must finish by", scheduling language
  → If still missing, ask: "What is the acceptable job completion time? For example: 'must finish within 6 hours of midnight' or 'runs weekly, no strict deadline'."

### Observable Context (gather from environment)

- **Existing infrastructure:** Look for Hadoop, Spark, Flink, or Airflow configurations that constrain engine choice.
  → Look for: `pom.xml` with spark/hadoop deps, `requirements.txt` with pyspark, `airflow/dags/`, `Dockerfile` with cluster images
  → If unavailable: assume greenfield, no constraint on engine choice

- **Data partitioning:** Check whether input datasets are already partitioned and by what key.
  → Look for: HDFS directory structures, partition specs in Hive metastore configs, dataset metadata files
  → If unavailable: assume unpartitioned, sort-merge join is safe default

- **Skew indicators:** Check whether any join keys are known to have high-cardinality hot keys (e.g., celebrity users in a social graph, viral content IDs).
  → Look for: comments about hot keys, prior skew handling code, "top user" or "trending" concepts in data model
  → If unavailable: assume uniform distribution until data profile reveals otherwise

### Default Assumptions

- If engine is unspecified and infrastructure allows it: recommend a dataflow engine (Spark or Flink) over raw MapReduce — they execute significantly faster for most workloads.
- If join dataset sizes are unspecified: default to sort-merge join (safest for unknown sizes, no memory assumptions).
- If output destination is unspecified: write to distributed filesystem (HDFS, S3) — composable, immutable, safe.
- If fault tolerance requirement is unspecified: use materialization for jobs longer than 30 minutes; use in-memory recomputation for shorter jobs.

### Questioning Guidelines

Ask ONE question at a time, most critical first (input characteristics before transformation details before output). Show what you already know from the environment before asking. State WHY you need the information.

## Process

Use `TodoWrite` to track steps before beginning.

```
TodoWrite([
  { id: "1", content: "Confirm workload is batch; gather input/output characteristics", status: "pending" },
  { id: "2", content: "Select processing engine: MapReduce vs dataflow engine", status: "pending" },
  { id: "3", content: "Design join strategy for any cross-dataset operations", status: "pending" },
  { id: "4", content: "Design multi-step workflow and intermediate state handling", status: "pending" },
  { id: "5", content: "Assess graph processing needs (if applicable)", status: "pending" },
  { id: "6", content: "Design fault tolerance strategy", status: "pending" },
  { id: "7", content: "Specify output destination and loading strategy", status: "pending" },
  { id: "8", content: "Produce pipeline architecture document", status: "pending" }
])
```

---

### Step 1: Confirm Workload Classification

**ACTION:** Verify the workload is genuinely batch before proceeding. Determine input volume, update frequency, and latency tolerance.

**WHY:** The boundary between batch and stream processing determines which design space applies. A pipeline that processes data "every hour" sounds like batch — but if the latency requirement is under 5 minutes, it is stream processing in disguise. Getting this wrong leads to building the wrong system. The key distinguishing property of batch is that the input is **bounded** — it has a known, fixed size at the time the job starts. A job knows when it has finished reading all input, so it can eventually complete.

**Classification signals:**
- **Batch:** Input is a file dump, database snapshot, or accumulated log from a fixed time window. Job runs periodically. Latency measured in minutes to hours. Primary metric is throughput.
- **Stream:** Input arrives continuously and is never "done." Latency measured in milliseconds to seconds. See `stream-processing-designer` instead.

**IF** workload classification is ambiguous → invoke `oltp-olap-workload-classifier` first
**IF** clearly batch → proceed to Step 2

Mark Step 1 complete in TodoWrite.

---

### Step 2: Select the Processing Engine

**ACTION:** Choose between MapReduce and a dataflow engine (Spark, Flink, or Tez) for this pipeline.

**WHY:** MapReduce is simple and robust — it fully materializes intermediate state to disk, tolerates frequent task failures without any data loss, and runs safely on preemptible, low-priority compute. But this robustness has a cost: every intermediate result is written to the distributed filesystem and read back by the next stage. For complex pipelines with many stages, this disk I/O dominates runtime. Dataflow engines (Spark, Flink, Tez) treat the entire workflow as one job, pass data between operators in memory or local disk rather than the distributed filesystem, and skip sorting where it is not required. They execute the same computation significantly faster — often orders of magnitude for multi-stage pipelines — while providing equivalent fault tolerance via lineage tracking (Spark's Resilient Distributed Dataset) or operator checkpointing (Flink).

**Decision framework:**

| Factor | Prefer MapReduce | Prefer Dataflow Engine (Spark/Flink/Tez) |
|--------|-----------------|------------------------------------------|
| Pipeline stages | 1-3 stages | 4+ stages (many intermediate materializations in MR) |
| Task preemption risk | High (shared cluster, MR runs low-priority) | Low to moderate (dedicated cluster) |
| Existing infrastructure | Hadoop-only environment | Any modern cluster |
| Fault tolerance model | Must tolerate very frequent task kills | Standard hardware failure tolerance |
| Processing model | Batch only | Batch + can evolve toward streaming |
| Join complexity | Simple reduce-side joins | Complex multi-way joins, broadcast joins |

**Engine-specific selection within dataflow engines:**
- **Spark:** Batch processing, machine learning (MLlib), iterative algorithms. Rich ecosystem. Best default choice.
- **Flink:** Lowest latency for near-real-time batch; strong streaming integration; best when pipeline must eventually handle stream input.
- **Tez:** Thin optimization layer over YARN; lowest overhead when Pig/Hive workflows already exist and just need faster execution.

**Note on high-level languages:** In most cases, you do not write raw MapReduce or dataflow operator code. Higher-level tools (Hive, Spark SQL, Pig, Cascading, Crunch) compile to the underlying engine and include query optimizers that automatically select the best join algorithm. Declare joins relationally and let the optimizer decide — this is preferred unless fine-grained control is needed.

Mark Step 2 complete in TodoWrite.

---

### Step 3: Design the Join Strategy

**ACTION:** For any operation that correlates records from two or more datasets, select and specify the appropriate join algorithm from the three available strategies.

**WHY:** Joins are the most expensive and failure-prone operation in batch pipelines. The naive approach — querying a remote database for every record — is orders of magnitude slower than the pipeline's normal throughput, and it makes the job nondeterministic (the remote database may change during the job). The correct approach is to bring all the data needed for a join to the same place as a local operation. Three strategies accomplish this, each suited to different data size and partitioning conditions.

**Strategy 1 — Sort-Merge Join (reduce-side join)**

Use when: both datasets are large, sizes are unknown or similar, or datasets have no pre-existing partitioning guarantees.

How it works: Both datasets go through a mapper that emits records keyed by the join key. The shuffle/sort phase collects all records with the same key to the same reducer partition. The reducer sees all records for a given key together and performs the join. A secondary sort ensures that records from one dataset (e.g., a "profile" record) arrive before records from the other dataset (e.g., "activity events"), so the reducer can hold the profile record in memory while iterating through activity events without buffering everything.

Cost: All data is shuffled over the network and sorted. Expensive for large datasets but correct and scalable with no assumptions about data layout.

**Strategy 2 — Broadcast Hash Join (map-side join, small table)**

Use when: one dataset is small enough to fit entirely in memory on each mapper (typically < a few GB).

How it works: Each mapper loads the small dataset into an in-memory hash table at startup (the small dataset is "broadcast" to all mappers). The mapper then scans the large dataset record by record, looking up each record's join key in the hash table. No reducer is needed; no shuffle occurs. This is the fastest possible join when the small table fits in memory.

Cost: Requires the small table to fit in memory. The small table is replicated to every mapper — memory pressure scales with the number of map tasks running concurrently.

**Strategy 3 — Partitioned Hash Join (map-side join, co-partitioned tables)**

Use when: both datasets are large BUT are already partitioned by the same key, using the same hash function, into the same number of partitions (e.g., both output from prior MapReduce jobs with the same partitioning scheme).

How it works: Because both datasets are partitioned identically, mapper N for the large dataset only needs data from partition N of the small dataset. Each mapper loads one partition of the smaller table into memory and scans the corresponding partition of the larger table. No shuffle or reducer needed.

Cost: Requires both datasets to be co-partitioned — a strong prerequisite. This metadata (partitioning key, function, partition count) must be known and consistent between datasets.

**Handling skew in joins:**

If a join key has extreme hot spots (a "celebrity" user ID with millions of events, a viral content ID), a standard sort-merge join will send all records with that key to a single reducer, causing a straggler that blocks the entire pipeline.

Mitigation options:
- **Skewed join (Pig):** Run a sampling job first to identify hot keys. Route hot key records to multiple reducers randomly; replicate the other dataset's records for that key to all those reducers.
- **Sharded join (Crunch):** Specify hot keys explicitly; framework handles replication automatically.
- **Two-stage aggregation:** For GROUP BY on hot keys, first reduce to a partial aggregate per reducer (reducing volume), then combine across reducers.

Mark Step 3 complete in TodoWrite.

---

### Step 4: Design the Multi-Step Workflow

**ACTION:** Decompose the full pipeline into stages, specify the data flow between stages, and decide how intermediate state is managed.

**WHY:** A single MapReduce or dataflow job can only solve a limited range of problems. Complex pipelines require chaining multiple jobs — for example, a recommendation system may use 50-100 MapReduce jobs. The key architectural decision is how intermediate results are passed between stages: full materialization to the distributed filesystem (MapReduce style) vs. streaming through memory/local disk (dataflow engine style). This choice determines both performance and fault recovery behavior.

**Workflow structure decisions:**

1. **Identify job dependencies:** Which jobs produce the input for which other jobs? Draw this as a directed acyclic graph (DAG). A job can only start once all its upstream dependencies have completed successfully — partial output from failed jobs is discarded.

2. **Intermediate state strategy:**
   - **Full materialization (MapReduce):** Each job writes output to a named directory in HDFS; the next job reads from that directory. The intermediate data is durable, replicated, and independently inspectable. Cost: extra I/O, extra network replication, straggler delays (must wait for all tasks in a stage before next stage starts). Benefit: any job can be restarted independently; output can be read by multiple downstream jobs; easy debugging (inspect intermediate files).
   - **Pipelining (Spark/Flink):** Intermediate state between operators is kept in memory or local disk. Operators start as soon as their upstream operator has produced some output — no waiting for the entire stage to complete. Cost: if a node fails, the operator's output must be recomputed from the last checkpoint or original input. Benefit: much lower latency for multi-stage pipelines.

3. **Workflow scheduler:** For MapReduce-based pipelines with many jobs, use a workflow scheduler (Apache Airflow, Luigi, Azkaban, Oozie) to manage job dependencies, retries, backfills, and monitoring. Dataflow engines handle workflow dependencies internally.

4. **Unix philosophy applied:** Design each pipeline stage to do one thing well, read from a well-defined input format, and write to a well-defined output format. Inputs are treated as immutable — a stage never modifies its input. This means any stage can be rerun safely, old outputs can be kept in parallel directories while new outputs are being computed, and rollbacks are possible by switching back to a previous output directory.

Mark Step 4 complete in TodoWrite.

---

### Step 5: Assess Graph Processing Needs (if applicable)

**ACTION:** If the pipeline operates on graph-structured data (social graphs, web link graphs, dependency graphs), determine whether the Pregel/bulk synchronous parallel model is appropriate.

**WHY:** Many graph algorithms are iterative — they traverse edges, propagate information, and repeat until convergence (PageRank, shortest path, connected components, transitive closure). Implementing these in plain MapReduce is inefficient because MapReduce reads the entire input dataset and writes the entire output dataset on every iteration, even if only a small part of the graph changed. The Pregel model (also called bulk synchronous parallel, or BSP) addresses this by keeping vertex state in memory across iterations and only processing vertices that have received new messages.

**How Pregel works:**
- The graph is stored in a distributed filesystem as vertex and edge lists.
- Each iteration (called a "superstep"): the framework calls a function for each vertex, passing it all messages sent to that vertex in the previous superstep. The vertex updates its local state and sends messages to neighboring vertices along graph edges.
- Between supersteps, the framework delivers all messages: every message sent in superstep N is guaranteed to arrive at its destination vertex in superstep N+1.
- A vertex that receives no messages and votes to halt is deactivated. The algorithm completes when all vertices are inactive.
- Vertices communicate only by message passing, not by querying each other directly — this enables batching and provides a clean fault tolerance boundary.

**Fault tolerance in Pregel:** At the end of each superstep, the framework checkpoints the full state of all vertices to durable storage. If a node fails, the computation rolls back to the last checkpoint and resumes. Because operators are deterministic and messages are logged, selective partition recovery is also possible.

**When Pregel is appropriate:**
- Graph is too large to fit in memory on a single machine
- Algorithm requires many iterations over the graph structure
- Examples: PageRank, single-source shortest path, strongly connected components, community detection

**When Pregel is NOT appropriate:**
- Graph fits on a single machine — a single-threaded algorithm will likely outperform a distributed one due to cross-machine communication overhead in distributed graph processing
- Graph fits on a single machine's disks — frameworks like GraphChi enable single-machine processing of graphs larger than RAM
- Algorithm is not naturally expressed as vertex-centric message passing

**Implementations:** Apache Giraph, Spark GraphX, Flink Gelly API.

**SKIP THIS STEP** if the pipeline does not operate on graph-structured data.

Mark Step 5 complete in TodoWrite.

---

### Step 6: Design the Fault Tolerance Strategy

**ACTION:** Specify how the pipeline recovers from task failures, job failures, and node failures.

**WHY:** Batch jobs process large datasets over long runtimes, making failures statistically inevitable. A pipeline that cannot recover from partial failures forces full restarts — wasting hours of compute. The key insight is that fault tolerance in batch processing is much simpler than in online systems because inputs are immutable: a failed task can always be retried on the same input without risk of double-writes or corrupted state. The challenge is minimizing the work lost when a failure occurs.

**Fault tolerance mechanisms:**

1. **Task-level retry (MapReduce and dataflow engines):** If an individual map or reduce task fails, the framework automatically retries it on another machine using the same input. This is safe because inputs are immutable and task outputs from failed attempts are discarded — only the successful attempt's output counts. This handles transient failures (network glitches, temporary disk errors) transparently.

2. **Materialization to durable storage (MapReduce):** Because every job's output is written to HDFS before downstream jobs start, a failed job can be restarted at that job's boundary without recomputing upstream jobs. For a 50-job pipeline, a failure in job 35 requires rerunning only jobs 35-50, not the entire pipeline.

3. **Lineage-based recomputation (Spark):** Spark tracks the lineage of each Resilient Distributed Dataset — which input partitions were used and which operators were applied. If a partition is lost due to node failure, it is recomputed from the lineage graph using the original input data. No intermediate state needs to be persisted to HDFS. Trade-off: recomputation is expensive if the lineage chain is long; checkpoint RDDs periodically for pipelines with many transformation stages.

4. **Operator checkpointing (Flink):** Flink periodically checkpoints operator state, allowing recovery to the last checkpoint without recomputing from original inputs. Particularly important for stateful operators (running aggregations, graph iteration state).

5. **Determinism requirement:** Recomputation is only correct if operators are deterministic — given the same input, they produce the same output. Non-deterministic behaviors to avoid: using system clocks in computations, iterating over hash tables (ordering is not guaranteed in most languages), using random numbers without a fixed seed, reading from external mutable sources during the job.

**Selecting the fault tolerance strategy:**

| Scenario | Recommendation |
|----------|----------------|
| Job runtime < 30 minutes | In-memory recomputation (Spark lineage); full materialization is overkill |
| Job runtime > 1 hour with many stages | Checkpoint intermediate state periodically; full restart from scratch is too expensive |
| Multi-team pipeline (other teams read intermediate outputs) | Full materialization to named HDFS paths; allows independent debugging and reuse |
| High preemption rate (shared cluster, low-priority batch) | MapReduce-style full materialization; task-level retry handles frequent kills efficiently |
| Iterative graph algorithm | Pregel checkpoint at each superstep boundary |

Mark Step 6 complete in TodoWrite.

---

### Step 7: Specify Output Destination and Loading Strategy

**ACTION:** Define where the pipeline writes its final output and how that output is safely loaded for serving.

**WHY:** Writing pipeline output directly to a production database record-by-record is an anti-pattern: it is orders of magnitude slower than batch throughput, it overwhelms the database with parallel writes from hundreds of tasks, and it introduces partial-write visibility (consumers may read incomplete results mid-job). The correct pattern is to build the output as immutable files inside the batch job, then load them atomically.

**Output patterns:**

1. **Distributed filesystem (HDFS, S3, GCS):** Write output to a new directory with an atomic rename at the end. Downstream jobs read the directory by name. This enables rollback (keep the previous directory; switch back if the new output is wrong) and supports multiple consumers. Preferred for intermediate pipeline outputs and for outputs consumed by other batch jobs.

2. **Search index build:** Mappers partition documents by shard, each reducer builds the index for its partition, and index files are written to the distributed filesystem. Index files are then atomically swapped into the search cluster (Lucene/Solr, Elasticsearch). The batch job produces a complete, correct index; the serving layer does a single atomic switch.

3. **Key-value store bulk load:** Build the key-value store files inside the batch job (the mapper extracts keys and sorts by key, which is already most of the work for building an index). Write the database files to the distributed filesystem. Load them into the serving system (Voldemort, HBase, Terrapin, ElephantDB) via bulk load, which copies files and atomically switches the server to query the new files. The old files remain available for rollback.

4. **Anti-pattern — writing to a live database per-record:** Do not use a database client library inside a mapper or reducer to write records one at a time to a production database. Reasons: (a) network round-trip per record kills throughput, (b) parallel tasks overwhelm the database's write capacity, (c) job failure leaves partial results visible to consumers, breaking the all-or-nothing guarantee.

**The all-or-nothing guarantee:** A batch job's output is only visible when the job completes successfully. If the job fails, no output is produced. This property is what makes batch outputs safe to depend on. Preserving it for external outputs requires writing to a temporary location and atomically promoting the output on success.

Mark Step 7 complete in TodoWrite.

---

### Step 8: Produce the Pipeline Architecture Document

**ACTION:** Write a structured pipeline architecture document covering all decisions from Steps 1-7.

**WHY:** The architecture document captures not just what the pipeline does but why each design decision was made. This is essential for future engineers who will modify the pipeline — knowing the reasoning prevents undoing sound decisions. It also serves as the basis for the implementation plan.

**HANDOFF TO HUMAN:** The agent produces the architecture document; the human reviews trade-offs, confirms constraints, and proceeds to implementation.

**Output format:**

```markdown
# Batch Pipeline Architecture: [Pipeline Name]

## Workload Classification
- Type: Batch (bounded input, periodic execution)
- Input: [datasets, sizes, formats]
- Output: [destination, format, consumers]
- Latency tolerance: [acceptable job duration]

## Processing Engine
- Selected: [MapReduce / Spark / Flink / Tez]
- Rationale: [key factors from decision framework]

## Pipeline Stages (DAG)
[Stage 1] → [Stage 2] → [Stage 3] → [Output]

### Stage N: [Name]
- Input: [source dataset or upstream stage output]
- Transformation: [what this stage does]
- Output: [format, partitioning key]
- WHY this is a separate stage: [reason]

## Join Strategy
- Join type: [sort-merge / broadcast hash / partitioned hash]
- Datasets joined: [A (size) × B (size)]
- Selection rationale: [why this strategy fits the data characteristics]
- Skew handling: [if applicable]

## Intermediate State Management
- Strategy: [full materialization / pipelining / hybrid]
- Checkpoint points: [where state is durably saved]

## Graph Processing (if applicable)
- Model: [Pregel/BSP, implementation]
- Algorithm: [what graph computation is being performed]
- Iteration convergence: [how the algorithm knows when to stop]

## Fault Tolerance
- Task failure: [retry policy]
- Job failure: [restart boundary — which stages must rerun]
- Determinism: [operator determinism guarantees]

## Output Loading
- Pattern: [filesystem / search index build / key-value bulk load]
- Atomicity mechanism: [how partial output is prevented from being visible]
- Rollback strategy: [how to revert to previous output if new output is wrong]

## Trade-offs and Risks
- [Key trade-off 1]: [why this decision was made, what is given up]
- [Risk 1]: [failure mode and mitigation]
```

Mark Step 8 complete in TodoWrite.

## Inputs

- **Data source descriptions:** Dataset names, sizes, formats, update frequency
- **Required transformations:** Join conditions, aggregations, filters, enrichment steps
- **Output destination:** Where results go, how they will be consumed
- **Latency tolerance:** Acceptable job completion time
- **Infrastructure constraints:** Existing cluster type, available tools, team expertise

## Outputs

- **Pipeline architecture document** — engine choice, DAG of stages, join strategies, fault tolerance, output loading pattern
- **Join strategy selection** — which of the three join algorithms applies and why
- **Engine recommendation** — MapReduce vs Spark/Flink/Tez with decision rationale
- **Fault tolerance design** — materialization vs recomputation checkpointing strategy

## Key Principles

- **Bring data to the computation, not computation to the data** — the reason for co-locating datasets in a distributed filesystem before joining is that random remote lookups (querying a database per record) cost orders of magnitude more than local reads. MapReduce handles all network communication; the application code only sees local data. This separation also shields application code from partial failures.

- **Treat inputs as immutable and outputs as complete-or-nothing** — immutable inputs make retries safe (a failed task reruns on the same input, cannot corrupt it). Complete-or-nothing outputs make pipelines composable and debuggable (a job either produced a correct output or produced no output; there is no third state). These two properties together enable fault tolerance without distributed transactions.

- **Materialization is the trade-off between durability and performance** — fully materializing intermediate state to HDFS maximizes durability and restartability at the cost of extra I/O. Keeping state in memory maximizes performance at the cost of recomputation on failure. The right balance depends on job duration, cluster reliability, and whether intermediate outputs have other consumers.

- **Join strategy depends on data layout, not just data size** — the fastest join is not always the one that handles the largest data; it is the one that matches the data's existing partitioning. A broadcast hash join is fastest when one table is small. A partitioned hash join is fastest when both tables are co-partitioned. A sort-merge join is always correct but always pays the shuffle cost. Knowing what assumptions you can make about data layout unlocks faster strategies.

- **Skew breaks the "work is evenly distributed" assumption** — most batch processing performance analysis assumes uniform key distribution. Hot keys (celebrities, viral content, common stop words) concentrate work on a single reducer, making that reducer the bottleneck for the entire job. Identify potential hot keys during design and plan skew handling explicitly.

- **Graph algorithms on distributed systems pay a high communication cost** — distributed graph processing sends messages across the network for every edge crossing a machine boundary. If a graph fits on one machine, a single-machine algorithm almost always outperforms a distributed one. Use distributed graph processing (Pregel) only when the graph genuinely cannot fit on a single machine or disk.

- **Write output as files, bulk-load atomically into serving systems** — building the serving database inside the batch job (as sorted, indexed files on the distributed filesystem) and loading it atomically produces correct, rollback-able results. Writing per-record to a live database during the job trades away the all-or-nothing guarantee for implementation convenience, which is a bad trade.

## Examples

**Scenario: Web server log analysis — top URLs by traffic**

Trigger: "We have 500 GB of daily nginx access logs in S3. We need a daily report of the top 1000 most-requested URLs."

Process:
1. Workload: batch — daily job, logs are a bounded daily dump, 24-hour latency acceptable.
2. Engine: Spark — single-stage job, but team already has Spark infrastructure; no reason to use raw MapReduce.
3. Stage 1 (map): Parse log lines, extract URL field. Emit (url, 1) pairs.
4. Stage 2 (reduce): Group by URL, sum counts. Emit (url, count).
5. Stage 3 (sort): Sort by count descending, take top 1000.
6. No joins required — single dataset.
7. Output: Write top-1000 list to S3 as a JSON file. Atomic rename prevents partial reads.
8. Fault tolerance: Spark lineage — job is short enough (< 30 min) that full recomputation from S3 is acceptable if a task fails.

Output: Architecture doc specifying a 3-operator Spark pipeline with no joins, output to S3 JSON, daily schedule via Airflow.

---

**Scenario: User activity enrichment — joining events with profile database**

Trigger: "We have 2 TB of daily clickstream events (user_id, timestamp, url) and a 50 GB user profile database snapshot (user_id, age, country). We need to produce a dataset of (url, viewer_age, viewer_country) for analytics."

Process:
1. Workload: batch — daily job, both datasets are fixed snapshots, latency up to 6 hours acceptable.
2. Engine: Spark — multi-stage workflow benefits from dataflow execution.
3. Join strategy: broadcast hash join — user profile database (50 GB) is small enough to broadcast to each executor; 2 TB clickstream is the large dataset. Each executor loads profile hash table at startup, scans clickstream records, looks up profile by user_id. No shuffle required.
4. Skew check: if any user_id has pathologically many events (bot traffic), filter or handle separately — but for typical users, assume uniform distribution.
5. Stage 1: Load both datasets. Broadcast profile table.
6. Stage 2 (map-side join): For each clickstream record, look up user profile by user_id. Emit (url, age, country).
7. Stage 3: Write output partitioned by date to HDFS.
8. Output: HDFS directory, Parquet format, read by Hive/Spark SQL for analytics queries.
9. Fault tolerance: Spark lineage; profile table is fully in memory per executor so recomputation is fast.

Output: Architecture doc specifying broadcast hash join, Spark execution, Parquet output to HDFS, with note that if profile table grows beyond 200 GB, re-evaluate to sort-merge join.

---

**Scenario: PageRank computation on a web link graph**

Trigger: "We have a 10 TB graph of web pages and hyperlinks (300 billion edges). We need to compute PageRank scores for all pages to power search result ranking."

Process:
1. Workload: batch — graph is a periodic snapshot, computation may take hours to days, latency not critical.
2. Engine: Spark GraphX (implements Pregel/BSP model) — algorithm is iterative and graph-structured; plain MapReduce would re-read 10 TB per iteration.
3. Graph processing: Pregel model. Each vertex holds its current PageRank score. Each superstep: vertex sends its score divided by out-degree to all neighbors. Vertex receives scores from all incoming neighbors and updates its own score as weighted sum. Repeat until convergence (change in scores below threshold, typically 0.001).
4. Fault tolerance: Checkpoint vertex state to HDFS every 5 supersteps (configurable). On node failure, roll back to last checkpoint and resume. Algorithm is deterministic, so checkpointing + rollback is safe.
5. Skew: PageRank is a "pull" algorithm — vertices pull scores from neighbors. High-degree "celebrity" pages receive many messages; this is handled by the framework's partitioning, not by skew join handling.
6. Single-machine feasibility check: 10 TB graph — does not fit on a single machine. Distributed processing is required.
7. Output: Write (page_id, pagerank_score) to HDFS. Bulk-load into serving key-value store for search ranking lookups.

Output: Architecture doc specifying GraphX Pregel implementation, 5-superstep checkpoint interval, bulk load to serving store, with note to evaluate GraphChi if graph shrinks to single-machine scale.

## References

- For detailed join algorithm decision criteria and size thresholds, see [join-strategy-reference.md](references/join-strategy-reference.md)
- For MapReduce vs dataflow engine comparison with benchmark data, see [engine-comparison.md](references/engine-comparison.md)
- For skew handling patterns (skewed join, sharded join, two-stage aggregation), see [join-strategy-reference.md](references/join-strategy-reference.md)
- Cross-reference: for stream processing (unbounded input), see `stream-processing-designer`
- Cross-reference: for workload classification (batch vs OLTP vs OLAP), see `oltp-olap-workload-classifier`
- Source: *Designing Data-Intensive Applications*, Martin Kleppmann, Chapter 10 (pages 389-430)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data Intensive Applications by Unknown.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-oltp-olap-workload-classifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
