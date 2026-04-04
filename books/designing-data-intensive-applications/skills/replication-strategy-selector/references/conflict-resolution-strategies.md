# Conflict Resolution Strategies

Use this reference when selecting a conflict resolution strategy for multi-leader or leaderless replication. A write conflict occurs when two nodes independently accept writes to the same key without either knowing about the other's write. All replicas must eventually converge to the same value — conflict resolution defines how that convergence happens.

## What Makes a Conflict

Two writes are **concurrent** if neither operation was aware of the other when it was submitted. Version vectors (or vector clocks) track which version each write was based on:
- If client B's write is based on version v2 (which included client A's write), B's write happens-after A's — no conflict.
- If both A and B wrote based on version v1 (neither knew about the other), both writes are concurrent — conflict.

Two writes are **not concurrent** (and therefore not a conflict) if one causally depends on the other.

## Strategy 1: Last Write Wins (LWW)

**How it works:** Attach a timestamp to every write. When two concurrent writes are detected, the write with the higher timestamp "wins" — the other is silently discarded.

**Data loss:** Yes. The losing write is dropped, even though the client received a success acknowledgment.

**When to use:**
- Data loss is acceptable (caches, idempotent operations, analytics events that can be replayed)
- Each key is written at most once and then immutable (use UUID as key to prevent reuse)
- You need the simplest possible convergence with no application code

**When NOT to use:**
- Financial records, inventory counts, reservation systems — any write that cannot be lost
- Counters or aggregates (two increments become one)
- Any write where the client expects their acknowledgment means the write is permanent

**The clock skew problem:** LWW relies on timestamps to pick the "most recent" write. In distributed systems, node clocks cannot be perfectly synchronized. A write with a "later" local timestamp may have actually been submitted before a write with an "earlier" timestamp on another node (due to clock drift, NTP adjustments, or clock skew). LWW will silently pick the wrong winner in these cases.

**Safe use of LWW:** The only safe pattern is to use a globally unique key (UUID) for every write, so two writes to the same key cannot happen. Cassandra documentation recommends this pattern: use a UUID as the primary key, making each write operation a unique key, so concurrent updates cannot occur by construction.

**Implementation:**
- Cassandra: LWW is the default conflict resolution. Timestamp is the write time on the client.
- Riak: LWW is optional; version vectors are the default.
- DynamoDB: Conditional writes (compare-and-set) prevent LWW data loss for critical updates.

---

## Strategy 2: Conflict Avoidance

**How it works:** Design the system so that all writes for a given record always go through the same leader. If one leader "owns" each record, concurrent writes to the same record from two leaders cannot happen — there is no conflict to resolve.

**Data loss:** No.

**When to use:**
- Each record has a natural "home" (user's home datacenter, record owner, geographic affinity)
- Write locality is predictable (a given user always writes from the same region)
- The system can tolerate routing all writes for a record to a single datacenter

**Limitation:** Conflict avoidance breaks down if the home leader changes. If a user moves to a different region, or if the home datacenter fails and traffic is rerouted, writes may go to a different leader than expected — creating conflicts. Implementing a clean leader-change handoff (lock the record, drain writes, switch leader, unlock) is non-trivial.

**Implementation:** Application-level routing. Configure your load balancer or service layer to send writes for a given key (e.g., user ID, account ID) to the datacenter that "owns" that key. Can be implemented with consistent hashing or explicit key-to-datacenter mappings.

---

## Strategy 3: Merge / Union

**How it works:** When concurrent writes produce multiple versions of the same key, keep all versions and merge them into a single value. For sets and lists, merge = union.

**Data loss:** No — but merge may produce a result that is not exactly what either client intended.

**When to use:**
- The data is a collection (set, list, map) where union is semantically correct
- Collaborative data structures (shopping carts, task lists, tagged content)
- CRDTs (Conflict-free Replicated Data Types) — data structures designed for automatic merge

**Limitation:** Merge only works for additive operations. Deletions are problematic: if client A deletes an item and client B adds an item, and the two writes are concurrent, the union may bring the deleted item back. The solution is tombstones — a special marker indicating "this item was deleted." The merge algorithm must treat tombstones correctly.

**CRDTs (Conflict-free Replicated Data Types):**
CRDTs are data structures designed so that concurrent modifications can always be merged automatically without conflict. Examples:
- **G-counter (grow-only counter):** Each node has its own counter; the global count is the sum of all per-node counts. Concurrent increments never conflict.
- **OR-Set (observed-remove set):** Adds and removes are tracked with unique identifiers; concurrent add+remove is resolved by keeping the add (with a tombstone for the remove).
- **LWW-register:** A single-value register using LWW — safe only when writes to the same key are not truly concurrent (because LWW is used).

Implementations: Riak 2.0 (G-counters, sets, maps, registers, flags), Redis (basic CRDTs), Akka Distributed Data (various CRDTs).

---

## Strategy 4: Application-Level Resolution on Read

**How it works:** When concurrent versions of a key exist, all versions are stored ("siblings" in Riak terminology). On the next read, the database returns all conflicting versions to the application. The application code resolves the conflict and writes back the merged value.

**Data loss:** No — but requires application code to handle multi-version responses correctly.

**When to use:**
- Only the application has the semantic context to merge two concurrent values correctly
- Conflict frequency is low (application complexity of handling multi-version responses is justified)
- The application already handles eventual consistency gracefully

**Limitation:** Every read code path must handle the case of multiple returned values. This is easy to get wrong — a naive implementation that picks the first value, or crashes on multi-value responses, will silently corrupt data.

**Implementation:** CouchDB uses this model. A read returns all conflicting revisions; the application picks or merges them and writes a new revision that resolves the conflict.

---

## Strategy 5: Application-Level Resolution on Write

**How it works:** A conflict handler is registered with the database. When the replication log detects a conflict during synchronization, the handler is called immediately. The handler must run quickly (it executes in the background replication process) and cannot prompt users.

**Data loss:** Depends on handler implementation.

**When to use:**
- Automated conflict resolution is possible without user input
- The conflict resolution logic is deterministic and fast
- The team can implement and test the handler thoroughly

**Limitation:** The handler must not block the replication process. It has no access to the user and cannot make external API calls. Bugs in the handler are difficult to detect because conflicts are infrequent — the handler may go untested in production for months.

**Implementation:** Bucardo (PostgreSQL), Oracle GoldenGate (custom PL/SQL handlers).

---

## Strategy Comparison Matrix

| Strategy | Data loss | Application code changes required | Conflict frequency sensitivity | Best use case |
|----------|----------|----------------------------------|-------------------------------|--------------|
| Last write wins | Yes | No | Low (conflicts infrequent) | Caches, idempotent ops |
| Conflict avoidance | No | Yes (routing) | N/A (no conflicts) | User-owned data with stable home |
| Merge / CRDTs | No | Sometimes (tombstones) | High (designed for concurrent writes) | Collections, collaborative data |
| App-level on read | No | Yes (multi-version handling) | Low-medium | Semantic conflicts only app can resolve |
| App-level on write | Depends | Yes (handler code) | Low-medium | Automated resolution possible |

## Recommendation Decision Tree

```
Can all writes for a given record always route through one leader?
  YES → Conflict avoidance (simplest; no data loss; no application code)
  NO ↓

Is the data a collection (set, list, counter)?
  YES → CRDTs / merge (Riak, or implement a CRDT data structure)
  NO ↓

Can the conflict be resolved automatically without user input?
  YES AND resolution is fast → App-level on write (conflict handler)
  YES AND resolution needs read context → App-level on read
  NO ↓

Is data loss acceptable (cache, analytics, idempotent)?
  YES → Last write wins (with UUID keys if possible)
  NO → Do not use multi-leader or leaderless; use single-leader instead
```
