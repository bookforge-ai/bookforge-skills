# Replication Log Formats

Leader-based replication (single-leader and multi-leader) requires the leader to send a stream of data changes to followers. How those changes are encoded determines upgrade flexibility, cross-database compatibility, and the risk of divergence between replicas.

## The Three Formats

### 1. Statement-Based Replication

**How it works:** The leader logs every write SQL statement (INSERT, UPDATE, DELETE) and forwards the statement text to followers. Each follower re-executes the statement.

**Problems:**
- Nondeterministic functions (`NOW()`, `RAND()`, `UUID()`) produce different values on each replica. The leader must replace these with fixed values before logging — a subtle requirement that is easy to miss.
- Statements that depend on existing data (e.g., `UPDATE table WHERE condition`) must execute in the same order on all replicas. Concurrent transactions can cause divergence if statements are re-ordered.
- Statements with side effects (triggers, stored procedures, user-defined functions) may produce different effects on each replica unless side effects are deterministic.

**Used by:** MySQL before version 5.1 (now row-based by default). VoltDB uses statement-based replication but requires all transactions to be deterministic.

**When appropriate:** Only for systems where all statements are guaranteed to be deterministic. Not recommended for general-purpose use.

---

### 2. Write-Ahead Log (WAL) Shipping

**How it works:** The storage engine appends every write to a WAL (write-ahead log) — an append-only sequence of bytes describing every change to every disk block. The leader ships this raw log to followers. Followers apply the log bytes directly to their own storage, building an identical disk structure to the leader.

**Advantages:**
- Byte-for-byte identical disk structure on all replicas. Divergence is structurally impossible.
- Used by PostgreSQL and Oracle (among others).

**Problems:**
- The WAL contains physical details: which bytes changed in which disk blocks. This is tightly coupled to the specific storage engine version and format.
- If the leader and follower run different database software versions, the WAL format may differ — making zero-downtime upgrades impossible. Upgrading requires taking followers offline or using logical replication instead.
- Cannot be used to replicate between different database products (PostgreSQL WAL cannot be consumed by MySQL).

**Used by:** PostgreSQL (`wal_level = replica` or `logical`), Oracle Data Guard.

**When appropriate:** Single-database deployments where version homogeneity is maintained and operational simplicity is valued over upgrade flexibility.

---

### 3. Logical (Row-Based) Log Replication

**How it works:** A separate log format — decoupled from the storage engine's physical format — describes writes at the granularity of database rows:
- **Inserted row:** new values of all columns
- **Deleted row:** enough information to identify the row (primary key, or all column values if no primary key)
- **Updated row:** row identifier + new values of changed columns

**Advantages:**
- Decoupled from the storage engine internals → leader and follower can run different database versions during rolling upgrades.
- Easier to parse by external systems (data warehouses, caches, search indexes via change data capture).
- Can replicate between different database products if both understand the logical format.

**Problems:**
- More data volume than statement-based replication (full row contents vs. one SQL statement).
- Conflict detection in multi-leader setups must operate at the row level (which column changed? was the whole row replaced?).

**Used by:** MySQL binlog (`binlog_format = ROW`), PostgreSQL logical replication (`wal_level = logical`), Debezium (CDC).

**When appropriate:** The recommended default for most production deployments. Required if zero-downtime upgrades are needed. Required if change data capture (CDC) feeds a data warehouse or search index.

---

### 4. Trigger-Based Replication

**How it works:** Application-level replication using database triggers or stored procedures. A trigger fires on every write, logs the change to a separate table, and an external process reads that table and replicates the change.

**Advantages:**
- Maximum flexibility: can replicate a subset of data, apply transformation logic, or replicate between different database systems.
- Does not require changes to the database software itself.

**Problems:**
- Higher overhead than built-in replication (trigger execution + log table writes on every write).
- More bugs and edge cases than built-in replication methods.
- Requires careful design to avoid trigger recursion and partial-write anomalies.

**Used by:** Databus (Oracle to Oracle/MySQL), Bucardo (PostgreSQL), Oracle GoldenGate.

**When appropriate:** When built-in replication does not support the required topology (e.g., cross-database replication, selective replication, custom transformation during replication).

---

## Comparison Table

| Format | Decoupled from storage engine? | Zero-downtime upgrades? | External consumption (CDC)? | Divergence risk |
|--------|-------------------------------|------------------------|----------------------------|----------------|
| Statement-based | Yes | Yes | Difficult (parse SQL) | High (nondeterminism) |
| WAL shipping | No | No | Difficult (binary format) | Very low |
| Logical/row-based | Yes | Yes | Easy (structured rows) | Low |
| Trigger-based | Yes | Yes | Easy (custom table) | Medium (trigger bugs) |

## Recommendation

**Default choice:** Logical (row-based) replication. It provides upgrade flexibility, external CDC compatibility, and low divergence risk without the nondeterminism problems of statement-based replication.

**Use WAL shipping only if:** You want the simplest possible setup and guarantee that the leader and all followers will always run the same database version. Operational teams that can enforce version homogeneity may prefer WAL shipping for its byte-for-byte replica guarantee.

**Avoid statement-based replication** unless you can guarantee all statements are deterministic (VoltDB model) or you are constrained to a legacy MySQL version.
