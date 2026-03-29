# ADR 1: Adopt Event Sourcing for Financial Audit Trail

## Status
RFC, Deadline 2026-04-02

This ADR is open for team review and comment. The architecture review board will discuss this at the meeting on 2026-04-02 (Thursday). All feedback should be submitted before that date. After the review board meeting, the architect will incorporate feedback and move this ADR to Accepted or Rejected.

## Context

Our financial system requires a complete, tamper-evident audit trail of all transactions and state changes for regulatory compliance and operational traceability. Currently, we maintain an append-only PostgreSQL table that logs each change as a new row. While this approach is simple and well-understood by the team, it has limitations:

- **History replay is not natively supported.** Reconstructing the exact state of an account at a past point in time requires writing custom queries that aggregate rows up to a given timestamp. This is error-prone and slow for complex state reconstructions.
- **The audit log is a secondary artifact.** The append-only table is a side effect of the business logic, not the source of truth. If logging is missed in a code path, the audit trail has gaps — and we have no way to detect the gap.
- **Debugging production issues** requires correlating the audit log with the current state, which is stored separately. There is no single source of truth that contains both the current state and the full history.

Three alternatives have been considered:

1. **Keep the current append-only PostgreSQL table.** Simple, team knows it well, but limited replay capability and the log is secondary to state.
2. **Adopt event sourcing.** All state changes are stored as an immutable sequence of domain events. The current state is derived by replaying events. The event log IS the source of truth.
3. **Implement Change Data Capture (CDC) on the existing database.** Capture row-level changes from the PostgreSQL WAL. Provides an audit trail without changing application architecture, but captures data-level changes, not business-intent events (e.g., "row updated" vs. "payment reversed").

## Decision

We will adopt event sourcing for the financial audit trail, replacing the current append-only PostgreSQL table with an immutable event store where every state change is captured as a named domain event.

**WHY — Technical justification:**

Event sourcing makes the audit trail the source of truth rather than a secondary side effect. Every state transition is recorded as a first-class domain event (e.g., `AccountOpened`, `PaymentReceived`, `AdjustmentApplied`), and the current state is derived by replaying these events. This means:

- Complete history replay is a built-in capability, not a custom query hack. Reconstructing state at any point in time is a matter of replaying events up to that timestamp.
- Audit gaps become structurally impossible — if an event was not emitted, the state change did not happen. The log and the state are one and the same.
- Domain events capture business intent, not just data mutations. "PaymentReversed" carries far more meaning for auditors than "amount column changed from 500 to 0."

**WHY — Business justification:**

Financial regulatory compliance (SOX, PCI-DSS) requires demonstrating a complete, unalterable record of all financial transactions. Our current approach leaves us exposed to audit gaps that could result in compliance findings. Event sourcing provides a structurally complete audit trail that reduces compliance risk and simplifies regulatory reporting. It also provides the temporal query capabilities that the finance team has been requesting for quarter-end reconciliation, which currently takes 2+ days of manual effort.

**Note:** This recommendation is being put forward for team discussion. The architect acknowledges that team expertise is a significant factor (see Consequences) and invites the team to weigh in on the feasibility and timeline before this decision is finalized.

## Consequences

### Positive
- **Complete, structural auditability.** The event log IS the system state. Audit gaps are impossible by design, not by discipline.
- **Native temporal queries.** "What was the account balance at 3:47 PM on March 15?" becomes a straightforward event replay, not a complex aggregate query.
- **Business-intent preservation.** Events like `PaymentReversed` and `FraudHoldPlaced` capture WHY state changed, not just what changed. This is significantly more valuable for auditors and for debugging.
- **Enables future capabilities.** Event sourcing opens the door to event-driven projections (e.g., real-time dashboards), retroactive bug fixes by replaying corrected events, and easier integration with downstream systems via event publishing.

### Negative
- **Steep learning curve.** The team has no prior experience with event sourcing. Concepts like event stores, projections, snapshots, and eventual consistency are non-trivial. This will require training investment and will slow initial development velocity.
- **Increased operational complexity.** An event store requires different operational practices than a relational database — schema evolution becomes event versioning, storage grows unboundedly (requiring snapshot and compaction strategies), and debugging requires event replay tooling.
- **Read model complexity.** Queries that are trivial in a relational model (e.g., "show me all accounts with balance > $10,000") require building and maintaining separate read projections, adding eventual consistency concerns.
- **Tooling and infrastructure.** We will need to select and operate an event store (e.g., EventStoreDB, Axon, or a PostgreSQL-based implementation), adding a new infrastructure component.

### Trade-offs
- We are trading **simplicity and team familiarity** for **structural auditability and temporal query capability**. The current team can maintain the append-only table with minimal effort; event sourcing will require significant upfront learning.
- We are trading **immediate development speed** for **long-term audit compliance confidence**. Initial feature delivery will slow as the team builds expertise, but ongoing compliance effort should decrease.
- We are trading **simple read queries** for **powerful write-side guarantees**. CQRS (Command Query Responsibility Segregation) will likely be needed to maintain query performance, adding architectural complexity.

## Compliance

- **Type:** Manual review (initially), with automated fitness functions once implemented
- **Mechanism:**
  - **During RFC period:** Collect team feedback via comments on this ADR. Architecture review board evaluates on 2026-04-02.
  - **If adopted — manual:** Code reviews must verify that all financial state changes emit domain events through the event store. No direct state mutations bypassing the event log.
  - **If adopted — automated fitness function:** An integration test verifying that every command handler in the financial domain produces at least one event, and that the aggregate state can be fully reconstructed from its event stream. This test should run in CI on every pull request.
  - **If adopted — architectural fitness function:** A static analysis rule (e.g., ArchUnit or custom linter) ensuring no direct database writes occur in the financial domain outside of the event store infrastructure.
- **Frequency:** Code review on every PR. Automated tests on every CI run. Quarterly architecture review to assess event store operational health and team proficiency.

## Notes
- **Author:** [Architect name]
- **Date:** 2026-03-27
- **Approved by:** Pending — under RFC review by architecture review board
- **Last modified:** 2026-03-27
- **RFC deadline:** 2026-04-02 (architecture review board meeting)
- **Supersedes:** N/A
- **Superseded by:** N/A
