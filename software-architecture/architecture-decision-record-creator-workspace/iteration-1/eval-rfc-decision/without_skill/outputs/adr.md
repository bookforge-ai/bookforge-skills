# ADR-XXX: Event Sourcing for Financial Audit Trail

**Status:** Proposed
**Date:** 2026-03-27
**Deciders:** Architecture Review Board
**Review Meeting:** Thursday, 2026-04-02

## Context

Our financial system currently uses an append-only PostgreSQL table to maintain an audit trail of all financial transactions. While this approach has served us adequately, we are evaluating whether adopting event sourcing would better meet our evolving requirements for auditability, history replay, and regulatory compliance.

The append-only table provides a sequential log of changes but does not natively support reconstructing the full state of the system at an arbitrary point in time. As audit and compliance requirements grow more demanding, the ability to replay the complete history of state transitions becomes increasingly valuable.

## Decision Drivers

- **Regulatory requirements** are increasing the need for complete, replayable audit trails.
- **Debugging and incident investigation** would benefit from the ability to reconstruct system state at any point in time.
- **Current append-only table** captures what changed but not necessarily the full context of why or how the state evolved through a sequence of events.
- **Team expertise** in event sourcing is currently limited, which poses adoption risk.
- **Operational complexity** must be weighed against the functional benefits.

## Options Considered

### Option 1: Keep Current Append-Only PostgreSQL Table

Continue using the existing append-only audit table with incremental improvements.

**Pros:**
- Team is already familiar with this approach; no learning curve.
- Simple operational model — standard PostgreSQL tooling, backups, and monitoring.
- Low risk; the system is already in production and working.
- Query patterns are straightforward SQL.

**Cons:**
- Reconstructing system state at a past point in time requires custom logic.
- The table captures individual changes but does not inherently model a stream of domain events.
- Scaling the table over time may require partitioning or archival strategies regardless.

### Option 2: Adopt Event Sourcing

Replace the append-only audit table with an event store where all state changes are captured as a sequence of immutable domain events. Current state is derived by replaying the event stream.

**Pros:**
- Complete history replay: the system state at any point in time can be reconstructed by replaying events up to that moment.
- Events capture domain intent (e.g., "PaymentAuthorized", "RefundIssued") rather than just data diffs, providing richer audit context.
- Enables new capabilities such as temporal queries, retroactive corrections, and event-driven integrations.
- Natural fit for financial domains where every state transition has regulatory significance.

**Cons:**
- Significant increase in architectural complexity (event store, projections, eventual consistency, snapshots).
- The team has limited experience with event sourcing patterns; requires meaningful investment in training and upskilling.
- Debugging can be harder — understanding current state requires reasoning about the event stream.
- Schema evolution of events is non-trivial and must be handled carefully to avoid breaking replay.
- Read-side projections introduce eventual consistency, which may surprise parts of the system that expect immediate consistency.
- Migration from the current system is a non-trivial project in itself.

### Option 3: Hybrid Approach — Enrich Append-Only Table with Event-Like Semantics

Keep PostgreSQL as the storage layer but restructure the append-only table to store typed domain events with metadata, and build lightweight replay and projection capabilities on top.

**Pros:**
- Retains familiar PostgreSQL infrastructure and operational model.
- Captures domain intent in events without requiring a dedicated event store.
- Incremental adoption: the team can learn event-oriented thinking without a full architectural shift.
- Replay capability can be built incrementally as needed.
- Lower migration risk than full event sourcing.

**Cons:**
- Does not provide the full guarantees of a purpose-built event sourcing framework.
- May result in a "neither here nor there" design that is harder to reason about than a clean event sourcing implementation.
- Performance of replay at scale may be limited compared to a dedicated event store.

## Recommendation

**No recommendation at this stage.** This ADR is being presented to the Architecture Review Board for discussion. The author leans toward exploring **Option 3 (Hybrid Approach)** as a pragmatic middle ground that delivers most of the auditability benefits while respecting the team's current expertise level, but wants the board's input before committing to a direction.

## Discussion Points for the Review Board

1. **Team readiness:** What level of investment in training would be acceptable if we go with full event sourcing? Do we have appetite for that?
2. **Regulatory drivers:** Are there specific upcoming compliance requirements that would tip the balance toward full event sourcing?
3. **Scale projections:** How large do we expect the audit trail to grow over the next 2-3 years, and does that affect the choice?
4. **Downstream consumers:** Are there other teams or systems that would benefit from a domain event stream?
5. **Migration risk:** What is our tolerance for a phased migration versus a clean cutover?
6. **Operational burden:** Do we have the infrastructure and on-call expertise to support an event store in production?

## Consequences (to be filled in after decision)

_This section will be completed once the Architecture Review Board reaches a decision._

### Positive

- (pending)

### Negative

- (pending)

### Risks

- (pending)

## Related

- Current audit trail implementation: append-only PostgreSQL table in the financial service
- Relevant patterns: Event Sourcing, CQRS, Domain Events
- References: Martin Fowler's Event Sourcing pattern description; Vaughn Vernon, "Implementing Domain-Driven Design"
