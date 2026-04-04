# Timeliness vs. Integrity: Two Dimensions of Consistency

## The Core Distinction

The term "consistency" in distributed systems conflates two properties that are worth separating:

**Timeliness** — ensuring that users observe the system in an up-to-date state. If data has been written, any subsequent read should return the new value, not a stale version.

**Integrity** — ensuring the absence of corruption; no data loss, no contradictory or false data. If a derived dataset is maintained as a view onto underlying data, the derivation must be correct and complete.

### The Slogan

- Violations of timeliness are **"eventual consistency"** — the system will catch up.
- Violations of integrity are **"perpetual inconsistency"** — the corruption is permanent.

## Why the Distinction Matters for Data Integration

### Traditional Transactions Conflate Both

ACID transactions provide both timeliness (linearizability — a committed write is immediately visible to all subsequent reads) and integrity (atomicity and durability — a write either commits completely or rolls back completely, with no partial effects).

Because transactions provide both together, architects using transactional systems rarely need to distinguish them. This creates a false assumption: that any system providing "consistency" must provide both simultaneously.

### Asynchronous Log-Based Systems Decouple Them

Event-log-based derived data systems (CDC, event sourcing, stream processing) are designed to preserve integrity while accepting weak timeliness.

- **Integrity is central:** Exactly-once semantics, idempotent consumers, and operation identifiers ensure that every event is applied exactly once to every derived view. No data is lost; no event is applied twice.
- **Timeliness is weak:** Derived views lag behind the source of record by the propagation latency (milliseconds to minutes, depending on the system). A read from the derived view may return stale data.

This is not a bug — it is a deliberate design trade-off that enables better performance, availability, and fault isolation than synchronous distributed transactions.

## Practical Implications

### What Integrity Requires in a Composed Pipeline

1. **Exactly-once event delivery to each consumer.** An event that is lost causes the derived view to permanently miss that update. An event that is applied twice may corrupt the derived view (unless the consumer is idempotent).

2. **Correct ordering where ordering matters.** If two events must be applied in a specific order (a delete must not precede the record's creation), the consumer must receive them in that order or detect and handle out-of-order delivery.

3. **Idempotent consumers or deduplication.** Because message delivery may provide at-least-once semantics (duplicates possible), consumers must be idempotent (applying the same event twice produces the same result) or must deduplicate by event ID.

4. **Durable event log.** If the event log is lost, derived views cannot be reconstructed. The log must be replicated and retained for at least as long as any consumer might need to replay it.

### What Timeliness Requires

1. **Low propagation latency.** The gap between a write to the source of record and its visibility in derived views must be small enough for the use case (sub-second for real-time dashboards; minutes may be acceptable for analytics).

2. **Read-your-own-writes consistency** (if required). A user who updates their profile and immediately views the result should see their new profile, not the pre-update version. This requires either routing the user's reads to the system of record (not the derived view) for a period after the write, or using causal consistency mechanisms.

3. **Causal consistency** (if required). If Event B causally depends on Event A (B happened because of A), any user who observes B should also observe A. See the causal ordering section of the main skill.

### The Trade-Off Is Asymmetric

In most applications, integrity violations are far more costly than timeliness violations:

| Scenario | Timeliness violation | Integrity violation |
|----------|---------------------|---------------------|
| E-commerce order | Product shows as available for 30s after selling out | Customer is charged twice for the same order |
| Bank account | Balance shows yesterday's value for 500ms | $11 is debited but only $5.50 is credited |
| Social profile | Updated bio visible to some users 2s before others | Profile update is permanently lost |
| Search index | New document not searchable for 10s | Deleted document remains in search results forever |

Timeliness violations are annoying and recoverable. Integrity violations are catastrophic and may be unrecoverable without manual intervention.

## Coordination-Avoiding Architectures

An important corollary: if integrity is more important than timeliness, and integrity can be maintained without synchronous cross-system coordination, then coordination-avoiding architectures are strictly better for most workloads.

**Coordination-avoiding systems** maintain integrity guarantees on derived data without requiring:
- Atomic commit across multiple stores
- Linearizability (synchronous coordination for recency guarantee)
- Synchronous cross-partition or cross-region coordination

They achieve this through:
- Deterministic derivation functions (same input → same output, always)
- Exactly-once processing (idempotent consumers, operation identifiers)
- Immutable event logs (replay reconstructs any derived view)

A coordination-avoiding system can operate across multiple datacenters in a multi-leader configuration, with weak timeliness guarantees, while still maintaining strong integrity guarantees. This is the sweet spot for most large-scale data integration scenarios.

## Loose Constraint Enforcement

Not every constraint must be enforced synchronously. Many business constraints can be violated temporarily and repaired after the fact ("apologize later").

### Hard Constraints (must be synchronous)
- Double-charging a payment card
- Permanently deleting data that a user wants back
- Any operation that cannot be reversed or compensated

### Soft Constraints (can be eventual or compensating)
- Two users claiming the same username simultaneously — apologize to the loser; ask them to choose another
- Overselling a product — apologize to the excess purchasers; offer a refund or backorder
- Overbooking an airline seat — apologize; offer compensation; bump a passenger

The cost of the apology (money, reputation, customer service effort) determines whether the constraint must be enforced synchronously. If the apology cost is low and the apology workflow must exist anyway (for other reasons like fraud, cancellations, etc.), strict synchronous enforcement may be unnecessary.

**The key question:** "What is the cost of temporarily violating this constraint, and can we detect and repair the violation before it causes irreversible harm?"

If the answer is "low cost, yes we can detect and repair" → soft constraint, coordination-avoiding enforcement is sufficient.
If the answer is "high cost or irreversible" → hard constraint, synchronous enforcement required.

## Applying This in Practice

When designing a data integration architecture, apply this framework to each constraint:

1. Identify the constraint (uniqueness, referential integrity, balance non-negativity, etc.)
2. Classify: hard (synchronous enforcement required) vs. soft (can be eventually enforced with compensation)
3. For hard constraints: design the partition routing to ensure conflicts go to a single partition, enabling a stream processor to enforce the constraint without distributed coordination
4. For soft constraints: design the async detection and compensation workflow; keep the write path fast and coordination-free
5. Ensure integrity (no data loss, no double-application) in all cases, regardless of timeliness classification
