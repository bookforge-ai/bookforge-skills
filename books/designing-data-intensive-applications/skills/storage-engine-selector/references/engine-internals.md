# Engine Internals Reference

This reference provides technical depth on LSM-tree, B-tree, and in-memory storage internals. Read this when preparing a team explanation, writing an Architecture Decision Record, or debugging a production storage issue.

Source: Designing Data-Intensive Applications, Chapter 3 (Kleppmann).

---

## LSM-Tree Write Path

LSM-tree (Log-Structured Merge-Tree) storage engines never modify data in place. Every write is an append.

### Write sequence

```
Client write (key=K, value=V)
        │
        ▼
1. Write-Ahead Log (WAL)
   - Append K,V to an append-only disk log
   - WHY: If the process crashes before step 2 completes, the WAL lets
     the engine recover the memtable. Without the WAL, recent writes
     in the memtable would be permanently lost on crash.
        │
        ▼
2. Memtable (in-memory balanced tree)
   - Insert K,V into a red-black tree or AVL tree (keys maintained sorted)
   - WHY: Keeping writes in a sorted in-memory structure allows the engine
     to flush a complete, sorted SSTable to disk in one sequential write.
     If writes went directly to disk unsorted, the engine would need
     random I/O on every write.
        │
   [When memtable exceeds threshold — typically 64MB-256MB]
        │
        ▼
3. SSTable flush to disk
   - Write the sorted key-value pairs from memtable to a new SSTable file
   - SSTable = Sorted String Table: keys in sorted order, one entry per key
   - A sparse in-memory index tracks byte offsets of keys in the file
   - A new memtable begins accepting writes while the flush happens
   - WHY: SSTable flush is a sequential write (fast on HDD; efficient on SSD).
     The sort order comes for free from the memtable's tree structure.
        │
        ▼
4. Compaction (background)
   - Merge multiple SSTable files, removing outdated values for the same key
   - The mergesort algorithm merges sorted files efficiently, even when
     the total size exceeds available RAM
   - After merge, old SSTable files are deleted
   - WHY: Without compaction, the number of SSTable files grows unboundedly.
     Read performance degrades (must check more files per query).
     Disk space grows (old values are never reclaimed).
```

### Read sequence

```
Read request (key=K)
        │
        ▼
1. Check memtable — is K in the current in-memory tree?
   [Found] → return value
        │
        ▼  [Not found]
2. Check Bloom filter for most recent SSTable
   - Bloom filter: probabilistic structure; can say "definitely not in this file"
   - False positives possible (file check triggered even if K is absent)
   - False negatives impossible (if Bloom filter says absent, K is definitely absent)
   - WHY: Without Bloom filters, every absent-key lookup requires reading
     all SSTable levels, causing many unnecessary disk reads.
        │
   [Bloom filter says "maybe present"] → check SSTable file
   [Bloom filter says "absent"] → skip this SSTable, check next level
        │
        ▼
3. Binary search within SSTable file using sparse in-memory index
   - Index stores offsets for some keys; binary search narrows to a block
   - Scan forward within the block to find K
        │
        ▼
4. Repeat for next-older SSTable level if not found
   - Check all SSTable levels from newest to oldest
   - WHY: The most recent SSTable has the most current value for a key.
     Older SSTables may have stale values that have been superseded.
```

### Write amplification in LSM-trees

Write amplification = (physical bytes written to disk) / (logical bytes written by application)

For leveled compaction:
- Level 0 → Level 1: key is rewritten when Level 0 SSTable is compacted into Level 1
- Level 1 → Level 2: rewritten again
- Typical: 10x write amplification for 7 levels of 10x size ratio

For size-tiered compaction:
- Newer SSTables merge into older ones; fewer levels; initial write amplification is lower
- But temporary space usage is higher (multiple full-size SSTable copies exist during merge)

---

## B-Tree Write Path

B-trees organize data into fixed-size pages (blocks), typically 4KB-16KB. Every page has a fixed address on disk. Updates overwrite the page in place.

### Write sequence

```
Client write (key=K, value=V)
        │
        ▼
1. Write-Ahead Log (WAL / redo log)
   - Append the operation to the WAL before modifying the B-tree
   - WHY: Page updates are not atomic at the hardware level. If the process
     crashes mid-page-write, the page is corrupted. The WAL lets the engine
     replay the operation and restore a consistent state on restart.
     (This is the same purpose as the LSM-tree WAL, but the failure mode
     being protected against is different: LSM-tree WAL protects memtable;
     B-tree WAL protects partially-written pages.)
        │
        ▼
2. Find the leaf page containing key K
   - Traverse from root: at each internal node, follow the page reference
     whose key range encompasses K
   - Depth is O(log n): a 4-level tree with 4KB pages and branching factor
     500 stores up to 256TB of data
        │
        ▼
3a. Key K already exists in this leaf page → overwrite value V in place
        │
3b. Key K does not exist in this page
        ├── Page has space → insert K,V into the page (maintain sorted order)
        └── Page is full → page split
              - Split the full page into two half-full pages
              - Update parent page to add a reference to the new page
              - If parent is also full → parent splits too (cascade upward)
              - WHY: Page splits preserve the O(log n) tree depth property.
                Without splitting, the tree would degrade toward O(n) lookup.
        │
        ▼
4. Write modified page(s) to disk
   - Overwrite the page at its fixed disk address
   - WHY: The B-tree design assumes each key exists at exactly one page
     address. Overwriting in place keeps this invariant. Moving pages
     would require updating all parent references — expensive.
```

### Write amplification in B-trees

- Minimum: 2 writes per logical write (WAL + page)
- On page split: 3+ writes (WAL + split pages + parent page update)
- If the engine avoids partial writes (writes full page even for 1-byte change): additional overhead proportional to page size
- Some engines (e.g., PostgreSQL) write pages twice to avoid partial write corruption (double buffering)

### Crash recovery

B-tree crash recovery uses the WAL to replay uncommitted operations. The WAL is an append-only log; replaying it after a crash brings the B-tree pages to a consistent state. This is why the WAL must be written (and fsync'd) before the page write — the WAL is the source of truth for recovery.

---

## In-Memory Database Durability Patterns

In-memory databases serve reads entirely from RAM. Writes may or may not persist to disk, depending on configuration.

### No persistence (cache-only)
- Example: Memcached, Redis without AOF/RDB
- All data lost on process restart
- Acceptable for: session caches, computed view caches, leaderboards where rebuild is fast
- Not acceptable for: any data that cannot be reconstructed from another source

### Append-only file persistence (AOF)
- Example: Redis with AOF enabled
- Every write command is appended to a log file on disk (like a WAL)
- On restart: replay the log to reconstruct state
- Tradeoff: AOF can grow very large; requires periodic compaction (AOF rewrite)
- Durability: configurable — fsync every write (durable, slower) or fsync every second (fast, up to 1 second of data loss possible)

### Periodic snapshot (RDB)
- Example: Redis with RDB enabled
- Full in-memory dataset is serialized to disk periodically (e.g., every 5 minutes or every 1000 writes)
- On restart: load the most recent snapshot; recent writes (since last snapshot) are lost
- Tradeoff: faster restarts than AOF replay; more data loss risk

### Replication-based durability
- Example: Redis Sentinel, Redis Cluster
- Writes are replicated to one or more replicas synchronously or asynchronously
- A failed primary can be replaced by a replica with minimal data loss
- Tradeoff: depends on replica availability; not a substitute for disk persistence in single-node deployments

### Full ACID in-memory (VoltDB, MemSQL/SingleStore)
- Write path: WAL written to disk + write applied to in-memory tables
- On restart: WAL replayed to rebuild in-memory state
- Full ACID semantics: serializable isolation, multi-table transactions
- Tradeoff: WAL write is on critical path; recovery time proportional to WAL size since last checkpoint

---

## Bloom Filter Mechanics

Bloom filters are used by LSM-tree engines (LevelDB, RocksDB, Cassandra, HBase) to avoid unnecessary SSTable file reads when looking up absent keys.

### How it works

A Bloom filter is a bit array of size m, with k hash functions.

**Insert key K:**
1. Hash K with all k hash functions → k bit positions
2. Set those k bits to 1

**Query "is K in the set?":**
1. Hash K with all k hash functions → k bit positions
2. If any bit is 0 → K is definitely NOT in the set (no false negatives)
3. If all bits are 1 → K is probably in the set (false positives possible)

False positive rate decreases as the bit array grows (more bits per key = fewer false positives). A well-tuned Bloom filter with 10 bits per key achieves ~1% false positive rate.

### Why it matters for LSM-trees

Without Bloom filters, a lookup for an absent key requires:
- Checking the memtable (1 in-memory lookup)
- Reading each SSTable level from disk (multiple disk reads)

With Bloom filters:
- Check the Bloom filter (in-memory, fast)
- If the filter says "absent" → skip this SSTable entirely (0 disk reads for absent keys)
- If the filter says "maybe present" → read the SSTable (only ~1% false positive overhead)

This is the primary optimization that makes LSM-tree read performance for point lookups competitive with B-trees.

---

## Write Amplification: Calculation Method

To measure write amplification in production:

```bash
# Linux: monitor disk write throughput
iostat -x 1 | grep <disk_device>

# Compare disk writes (bytes/sec) to application write rate (bytes/sec)
write_amplification = disk_write_bytes_per_sec / application_write_bytes_per_sec
```

Expected ranges:
| Engine | Expected write amplification |
|--------|------------------------------|
| B-tree, stable (no splits) | 2-4x |
| B-tree, high insert rate (frequent splits) | 4-8x |
| LSM-tree, size-tiered, low write rate | 3-5x |
| LSM-tree, leveled, steady state | 8-12x |
| LSM-tree, leveled, high write rate | 10-20x |

If measured write amplification significantly exceeds these ranges, investigate:
- B-tree: high page split rate (index fragmentation; consider FILLFACTOR tuning)
- LSM-tree: compaction not keeping up with writes; size-tiered compaction merging frequently
