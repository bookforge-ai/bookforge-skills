# Unbundling Patterns: Federated Databases vs. Composed Pipelines

## The Core Analogy

A relational database internally maintains several subsystems:
- **Secondary indexes** — allow efficient lookup by non-primary-key fields
- **Materialized views** — precomputed query results stored for fast read access
- **Replication logs** — propagate changes to follower replicas
- **Full-text indexes** — built into some databases (PostgreSQL tsvector, MySQL FULLTEXT)
- **Query optimizer** — selects efficient execution plans across indexes and joins

When you compose specialized systems — a primary OLTP database, a search index, an analytics warehouse, a feature store — you are implementing these same subsystems outside the database, as independent services connected by an event log. The event log plays the role of the replication log.

This is the "unbundling databases" or "database inside-out" approach: taking features that are built into databases as tightly coupled subsystems and implementing them as loosely coupled independent services.

## Two Approaches to Composition

### Federated Databases (Unified Reads)

A federated database (or polystore) provides a unified query interface over multiple underlying storage engines. Users query a single endpoint; the federated layer routes subqueries to the appropriate backend and merges results.

**Examples:** PostgreSQL Foreign Data Wrappers (FDW), BigQuery federated queries, Presto/Trino.

**Strengths:**
- Single query language for users
- No data movement required for read-only analytical queries
- Applications that need a specialized data model still have direct access to their native storage

**Weaknesses:**
- Query optimization across heterogeneous engines is complex
- No good answer to synchronizing writes across backends — reads are unified, writes are not
- Performance depends on the least-capable backend for cross-store queries

**When to use:** When you need unified read access to existing independent stores and can tolerate the write-synchronization problem being handled separately.

### Composed Pipelines (Unified Writes)

The composed pipeline approach focuses on write synchronization: one system is the source of truth; all others are derived. The event log synchronizes writes deterministically.

**The analogy to Unix pipes:**
```
# Unix: small tools, uniform interface (byte streams), composable
cat access.log | grep "ERROR" | awk '{print $1}' | sort | uniq -c

# Data systems: small tools, uniform interface (event log), composable
PostgreSQL → Debezium CDC → Kafka → Flink → Elasticsearch
                                          → Snowflake
                                          → Redis
```

Each tool does one thing well. The event log is the pipe. Application code is the shell script that wires them together.

**Strengths:**
- Loose coupling: a fault in Elasticsearch does not affect PostgreSQL or Snowflake
- Each store is optimized for its specific access pattern
- Historical reprocessing: replay the event log to rebuild any derived view
- Independent team ownership: each team operates their downstream consumer independently

**Weaknesses:**
- Operational complexity: more systems to deploy, monitor, and upgrade
- Asynchronous propagation: derived views lag behind the source of truth
- No standardized "pipe" yet: unlike Unix pipes, there is no universal protocol for composing storage systems

## Creating an Index as the Template

The `CREATE INDEX` operation in a relational database illustrates the pattern:

1. The database takes a consistent snapshot of the table
2. It scans all rows, extracts the indexed field values, sorts them, and writes the index structure
3. It applies any writes that arrived during the scan from the replication backlog
4. It continues maintaining the index on every subsequent write

This is exactly the bootstrap pattern for setting up a new derived view in a composed pipeline:
1. Take a consistent snapshot of the source of record (initial export)
2. Apply the snapshot to the derived store
3. Switch to consuming the ongoing event log from the point of the snapshot
4. Continue consuming the log indefinitely

The difference is that `CREATE INDEX` is built into the database and runs automatically. In a composed pipeline, you implement this bootstrap manually — but the logic is identical.

## The Missing Piece

Unix has the shell as a high-level language for composing tools via pipes. Data systems do not yet have an equivalent. The vision:

```
# Hypothetical declarative composition
mysql | elasticsearch  # = CREATE INDEX in MySQL, continuously replicated to Elasticsearch
```

This would mean: take all documents in MySQL, index them in Elasticsearch, and continuously apply all future changes. Tools like Debezium + Kafka + a stream processor approximate this, but with significantly more configuration and operational overhead than a pipe operator.

## When a Single System Wins

The goal of unbundling is breadth — serving more access patterns than any single system can. It is not a goal in itself.

**Use a single system when:**
- One technology satisfies all access patterns at the required scale
- The marginal benefit of specialized stores does not justify the operational cost
- The team does not have capacity to operate multiple systems reliably

"If there is a single technology that does everything you need, you're most likely best off simply using that product rather than trying to reimplement it yourself from lower-level components." — Kleppmann, Ch. 12

Premature unbundling — composing systems before the single-system ceiling is reached — adds complexity without benefit and may lock the team into an inflexible design.
