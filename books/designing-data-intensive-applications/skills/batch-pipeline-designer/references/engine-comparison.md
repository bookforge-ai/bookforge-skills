# Batch Processing Engine Comparison

Detailed comparison of MapReduce, Spark, Flink, and Tez for batch pipeline selection.

## The Core Distinction: Materialization vs Pipelining

The most important difference between MapReduce and dataflow engines is how they handle data flow between stages.

**MapReduce — full materialization:**
- Every job writes all output to HDFS before the next job starts.
- The next job reads from HDFS.
- Intermediate data is replicated across machines (durability overhead).
- Each stage waits for 100% of the previous stage to complete before starting.
- Straggler tasks (slow tasks in a stage) delay the entire pipeline.

**Dataflow engines (Spark, Flink, Tez) — pipelining:**
- Intermediate state between operators is kept in memory or written to local disk.
- Operators start processing as soon as upstream operators produce output.
- No HDFS replication of intermediate data.
- No waiting for full stage completion before downstream starts.
- Fault recovery requires recomputation (Spark lineage) or checkpoint rollback (Flink).

---

## MapReduce

**Strengths:**
- Extremely robust — designed to run on preemptible, low-priority compute alongside production workloads.
- Task-level fault tolerance: failed tasks are retried on the same input; output from failed attempts is discarded.
- Simple programming model — mapper and reducer callbacks are the entire API.
- Mature tooling, extensive operational experience.
- Correct for any batch workload; no assumptions about data layout or memory.

**Weaknesses:**
- Multi-stage pipelines require full materialization of each stage to HDFS — expensive for complex workflows.
- Sorting is always performed between map and reduce, even when not needed.
- A new JVM process is launched per task — startup overhead adds up for short tasks.
- Cannot express arbitrary operator graphs; only map-then-reduce topology (mitigated by chaining jobs).

**When MapReduce is the right choice:**
- Cluster runs mixed workloads with high task preemption rates (Google-style environment).
- Job must tolerate very frequent task kills without any state loss.
- Simple 1-3 stage pipelines where materialization overhead is not significant.
- Existing Hadoop-only environment with no Spark/Flink infrastructure.
- Compliance/audit requirements demand fully durable intermediate state.

**Typical performance vs Spark:** 2-10x slower for multi-stage pipelines. Comparable for single-stage jobs.

---

## Apache Spark

**Strengths:**
- Significantly faster than MapReduce for multi-stage pipelines — intermediate data stays in memory or local disk.
- Resilient Distributed Dataset (RDD) abstraction tracks data lineage for fault recovery without HDFS materialization.
- Rich API: batch (RDD, DataFrame), SQL (Spark SQL), streaming (Structured Streaming), ML (MLlib), graph (GraphX).
- Spark SQL optimizer (Catalyst) automatically selects join algorithms (broadcast, sort-merge) based on table statistics.
- Strong ecosystem: PySpark, Scala, Java, R APIs; deep integration with Delta Lake, Iceberg, Hudi.

**Weaknesses:**
- Memory-intensive: keeping intermediate state in memory requires careful memory tuning.
- Long lineage chains accumulate recomputation cost on failure — checkpoint RDDs for very long pipelines.
- Non-deterministic operations (system time, Python hash randomization, external reads) make lineage-based recovery unsafe without explicit handling.
- Higher operational complexity than MapReduce.

**When Spark is the right choice:**
- Multi-stage pipelines (4+ stages) where MapReduce would materialize to HDFS between each.
- Machine learning pipelines (MLlib integration).
- Iterative algorithms (graph processing via GraphX, ML training).
- Mixed batch + near-real-time processing (Structured Streaming runs the same code on streams).
- Teams already familiar with Spark; rich Python (PySpark) ecosystem.

**Fault tolerance model:** Lineage tracking. Each RDD/DataFrame partition knows its lineage — which operators and input partitions produced it. On node failure, lost partitions are recomputed from lineage. For very long lineage chains (many transformation stages), periodically call `rdd.checkpoint()` to materialize to HDFS and truncate the lineage.

**Key configuration levers:**
- `spark.executor.memory`: memory per executor — must accommodate working set of intermediate data.
- `spark.sql.autoBroadcastJoinThreshold`: maximum table size for automatic broadcast hash join (default 10 MB; increase if small table fits in memory).
- `spark.default.parallelism`: number of partitions for RDD operations.

---

## Apache Flink

**Strengths:**
- Lowest latency among dataflow engines — pipelined execution (Flink does not wait for a stage to complete before starting the next).
- Strongest streaming integration — same code runs on bounded (batch) and unbounded (stream) input; designed for eventual stream processing migration.
- Stateful operators with exactly-once guarantees via periodic checkpointing.
- Gelly API for graph processing (Pregel/BSP model).
- Lower memory footprint than Spark for many workloads (Flink manages memory outside JVM heap for serialized data).

**Weaknesses:**
- Smaller ecosystem than Spark; fewer pre-built ML libraries.
- More complex operational tuning (checkpoint configuration, state backend selection).
- Less SQL ecosystem maturity than Spark SQL (catching up with Flink SQL).

**When Flink is the right choice:**
- Batch pipeline that will evolve into a stream pipeline — same job graph works for both.
- Lowest latency batch execution is required (minimize time from job submission to output availability).
- Stateful batch computations (running aggregations, sessionization, iterative graph processing).
- Already running Flink for stream processing; use same cluster for batch.

**Fault tolerance model:** Periodic operator checkpointing. Flink snapshots the state of all operators to durable storage at configurable intervals. On node failure, Flink rolls back the entire job to the last checkpoint and resumes execution. Unlike Spark's lineage recomputation, Flink's recovery time is proportional to checkpoint interval, not lineage length.

**Key configuration levers:**
- `execution.checkpointing.interval`: how often to checkpoint (trade-off between recovery time and checkpoint overhead).
- `state.backend`: where checkpoint state is stored (RocksDB for large state, memory for small state).
- `taskmanager.memory.managed.fraction`: fraction of memory managed by Flink outside JVM heap.

---

## Apache Tez

**Strengths:**
- Thin optimization layer over YARN — minimal overhead, leverages existing YARN infrastructure.
- Enables Pig and Hive jobs to execute faster without rewriting job code (swap MapReduce execution engine for Tez via configuration).
- Good for organizations with large existing Pig/Hive codebases that need faster execution without migration.

**Weaknesses:**
- Does not provide its own high-level API — you use Tez through Pig, Hive, or Cascading.
- Relies on YARN shuffle service for data copying between nodes — less control over data transfer than Spark or Flink.
- Smaller community than Spark or Flink.

**When Tez is the right choice:**
- Existing Pig or Hive workflows need faster execution without code changes.
- Team is not ready to migrate to Spark/Flink but needs immediate performance improvement.
- Hadoop cluster with YARN is the only available infrastructure.

---

## High-Level Languages and Query Optimizers

In practice, engineers rarely write raw MapReduce, Spark, or Flink operator code for most batch workloads. High-level languages compile to the underlying engine and include query optimizers that automatically select the best execution plan.

| Language / Tool | Underlying engine | Notes |
|----------------|------------------|-------|
| Hive | MapReduce, Tez, or Spark | SQL-like; Hive query optimizer selects joins automatically |
| Pig | MapReduce or Tez | Dataflow scripting language |
| Spark SQL / DataFrames | Spark | Catalyst optimizer; column pruning, join reordering, predicate pushdown |
| Flink SQL | Flink | Growing SQL support; same optimizer principles |
| Cascading | MapReduce or Tez | Java API |
| Crunch | MapReduce | Java/Scala API |

The advantage of high-level declarative interfaces: you declare WHAT joins you need, and the query optimizer decides HOW to execute them (which join algorithm, in what order). Hive, Spark, and Flink all have cost-based optimizers that can even reorder joins to minimize intermediate state.

**Recommendation:** Use Spark SQL or Hive for most batch workloads unless fine-grained control over join algorithms or operator behavior is required. Reserve raw RDD/operator API for cases the SQL optimizer cannot handle (custom aggregations, iterative algorithms, graph processing).

---

## Performance Comparison Summary

For a representative 10-stage MapReduce pipeline on the same hardware:

| Engine | Relative speed | Primary reason |
|--------|---------------|----------------|
| MapReduce | 1x (baseline) | Full HDFS materialization between all stages |
| Tez | 2-4x | Eliminates unnecessary map stages; reduces HDFS I/O |
| Spark | 5-20x | In-memory intermediate state; pipelined execution; no sort unless needed |
| Flink | 5-20x | Pipelined execution; lower memory overhead than Spark |

Note: actual speedup depends heavily on the pipeline's bottleneck. Disk-bound pipelines see larger Spark/Flink improvements; CPU-bound pipelines see smaller differences. For single-stage jobs with no intermediate state, the difference is minimal.

---

## Engine Selection Decision Tree

```
Is the cluster shared with production workloads and task preemption is frequent?
├── YES → MapReduce (designed for this; tolerates frequent task kills)
└── NO
    └── Does an existing Hive/Pig codebase need faster execution without rewriting?
        ├── YES → Tez (swap execution engine via config)
        └── NO
            └── Will this pipeline eventually process streaming (unbounded) input?
                ├── YES → Flink (same code for batch + stream)
                └── NO
                    └── Is Python ecosystem important? (data science, ML)
                        ├── YES → Spark (PySpark, MLlib, GraphX)
                        └── NO → Spark or Flink (comparable; choose based on team familiarity)
```
