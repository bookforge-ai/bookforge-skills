## Significance Assessment
| Dimension | Affected? | How |
|-----------|:---------:|-----|
| Structure | Yes | Introduces the event sourcing pattern, replacing direct state mutation with an append-only event store. This fundamentally changes how the audit trail subsystem models and persists data — from a current-state table to an event log with projection-based reads. |
| Nonfunctional characteristics | Yes | Impacts auditability (complete history replay), performance (read path requires projection/materialization), and data integrity (immutable event log provides a tamper-evident record for financial compliance). |
| Dependencies | Yes | Introduces a dependency on an event store infrastructure component (e.g., EventStoreDB, or a Kafka-backed event log) that does not currently exist in the stack. Other services that consume audit data will need to read from projections rather than querying the PostgreSQL table directly. |
| Interfaces | Yes | Changes how downstream consumers access audit trail data. Current consumers query a PostgreSQL table directly; with event sourcing, they would read from materialized projections or subscribe to event streams. The write interface also changes — producers emit events rather than inserting rows. |
| Construction techniques | Yes | Requires new tooling and expertise the team does not currently possess: event store infrastructure, projection/materialization frameworks, and event versioning strategies. This affects development practices, testing approaches (event-based testing), and operational procedures. |

**Verdict:** Architecturally significant — affects 5 of 5 dimensions.

---

# ADR 1: Adopt Event Sourcing for Financial Audit Trail

## Status
RFC, Deadline 2026-04-03

## Context

Our financial audit trail currently uses an append-only PostgreSQL table that records each transaction event as a new row. This approach has served us well for basic audit queries, but we are encountering limitations:

- **No replay capability:** We can see what happened, but we cannot reconstruct the exact state of the system at any arbitrary point in time. Regulatory inquiries occasionally require this, and today we approximate it with manual analysis.
- **Schema evolution friction:** When we add new fields to the audit record, historical rows lack those fields. Backfilling is expensive and sometimes impossible.
- **Limited temporal queries:** Answering "what was the account balance at 3:47 PM on March 12?" requires complex queries that scan large portions of the table and are not always accurate.

Three alternatives were considered:

1. **Keep the current append-only PostgreSQL table** — Continue with the existing approach, accepting its limitations. Add views or materialized views for temporal queries where needed.
2. **Adopt event sourcing** — Replace the append-only table with an event store pattern where all state changes are captured as immutable events, and current state is derived by replaying those events through projections.
3. **Implement Change Data Capture (CDC)** — Keep PostgreSQL as the system of record but add CDC (e.g., Debezium) to stream changes to a separate audit log. This provides a change history without restructuring the write path.

The team has expressed concern about the expertise gap: nobody on the team has production experience with event sourcing. The current append-only table, while limited, is well-understood and operationally stable.

## Decision

We will adopt event sourcing for the financial audit trail, replacing the current append-only PostgreSQL table with an immutable event store where all financial state changes are recorded as discrete, ordered events. Current state will be derived through event replay and served via materialized projections.

**WHY this approach over the alternatives:**

We choose event sourcing over the status quo because the business requires complete, provable history replay for regulatory compliance. Our current append-only table records facts but cannot reconstruct state at a point in time without expensive and error-prone manual analysis. As our regulatory obligations grow — particularly around SOX compliance and potential audit requests — this gap becomes a business risk, not merely a technical inconvenience.

We choose event sourcing over CDC because CDC solves the observation problem (capturing what changed) but not the reconstruction problem (rebuilding state from history). CDC would give us a change log, but replaying that log to a consistent state requires the same event-replay semantics we would build with event sourcing — without the design benefits of treating events as first-class citizens.

**Business justification:** Regulatory audit response time is projected to decrease from days (manual reconstruction) to minutes (automated replay). This reduces compliance labor costs and mitigates the risk of regulatory penalties from incomplete audit responses. The immutable event log also provides a tamper-evident record, strengthening our position in financial audits.

**Technical justification:** Event sourcing gives us point-in-time state reconstruction as a natural capability rather than an expensive bolt-on. It also enables future capabilities — event-driven analytics, retroactive bug fixes via event replay, and decoupled downstream consumers — that the current architecture cannot support without significant rework.

**This recommendation is presented for team review.** The architect acknowledges the expertise gap and invites the team to evaluate the learning curve, propose a phased migration strategy, and identify whether a proof-of-concept should precede full adoption.

## Consequences

### Positive
- Complete, immutable history of all financial state changes — point-in-time state reconstruction becomes a built-in capability rather than an expensive manual process
- Tamper-evident audit log strengthens regulatory compliance posture (events are immutable and ordered)
- Enables temporal queries natively: "what was the state at time T?" is answered by replaying events up to T
- Decouples read and write models, allowing audit consumers to build purpose-specific projections without affecting the write path
- Future-proofs the architecture for event-driven analytics, retroactive correction (replay with patched logic), and new downstream consumers

### Negative
- **Steep learning curve:** The team has no production event sourcing experience. Training, mistakes, and slower initial velocity are expected.
- **Operational complexity increases:** Event store infrastructure (storage, snapshotting, projection rebuilds) requires new operational knowledge and monitoring
- **Read path latency may increase:** Queries that today hit a single table will now read from materialized projections, which must be kept up to date. Stale projections could serve incorrect data.
- **Event schema versioning is non-trivial:** As event schemas evolve, all historical events must remain deserializable. This requires disciplined versioning (upcasting, schema registry) from day one.
- **Migration risk:** Transitioning from the existing append-only table to an event store requires a careful migration strategy to avoid data loss or audit gaps during the transition period

### Trade-offs
- We accept increased system complexity and a slower initial development pace in exchange for a fundamentally stronger audit capability that meets growing regulatory requirements
- We accept the need for new infrastructure and operational expertise in exchange for a system that provides complete history replay as a first-class capability
- We accept that the read path becomes eventually consistent (projections lag behind events) in exchange for a clean separation of concerns between the write model (events) and read model (projections)

## Compliance

- **Type:** Manual review + Automated fitness function (after adoption)
- **Mechanism:**
  - **During RFC period:** Collect team feedback via comments on this ADR. Review at Architecture Review Board meeting on 2026-04-03. Decision must be finalized by deadline.
  - **If adopted — automated:** Integration test verifying that all financial state mutations produce corresponding events in the event store (no direct state writes bypass the event log). Test name: `test_all_financial_mutations_emit_events`. Runs in CI on every PR.
  - **If adopted — automated:** Projection staleness monitor: alert if any projection falls more than 30 seconds behind the event stream. Runs continuously in production monitoring.
  - **If adopted — manual:** Quarterly review of event schema versioning practices to ensure all historical events remain deserializable. Reviewed during architecture review board meetings.
- **Frequency:** CI pipeline (per PR) for mutation coverage; continuous for projection staleness; quarterly for schema versioning review

## Notes
- **Author:** (requesting architect)
- **Date:** 2026-03-27
- **Approved by:** Pending — under RFC review
- **Last modified:** 2026-03-27
- **RFC Deadline:** 2026-04-03 (Architecture Review Board meeting)
- **Supersedes:** N/A
- **Superseded by:** N/A
- **Review instructions:** Team members should comment on (1) feasibility given current expertise, (2) preferred event store technology, (3) whether a proof-of-concept phase should precede full adoption, and (4) migration strategy from the existing append-only table.
