# Architecture Characteristics: Hospital Employee Scheduling Tool

## Step 1: Domain Concerns

Translating stakeholder language into a domain concerns list:

| Concern | Source | Mapped Characteristics |
|---------|--------|----------------------|
| Labor law compliance (mandatory rest periods, max hours) | HR stakeholder | Legal, auditability, reliability |
| "Enterprise-grade and scalable" for 12-hospital expansion | IT Director | Scalability, extensibility, interoperability |
| "Just needs to work for this one hospital first" | Team reality check | Simplicity, feasibility |
| Time and budget constraints (3-person team, tight budget) | Project constraints | Simplicity, feasibility, maintainability |
| Shift swapping between staff | HR / functional requirement | Availability, performance, usability |
| PTO tracking | HR / functional requirement | Reliability, auditability |
| 700 users (500 nurses + 200 doctors) | Organizational scope | Performance (but modest scale — not a driver) |

**Key translation note:** The IT Director says "enterprise-grade and scalable." This needs unpacking. "Enterprise-grade" is not an architecture characteristic — it is vague business language that usually encodes reliability + security + availability. "Scalable for 12 hospitals" encodes scalability + extensibility. However, the team's own assessment ("just need it to work for one hospital") and constraints (3-person team, tight budget) map strongly to simplicity and feasibility. These two perspectives are in tension, and the skill's prioritization step will resolve it.

## Step 2: Extract from Requirements

| Characteristic | Source Requirement | Reasoning |
|---------------|-------------------|-----------|
| **Legal / Compliance** | "Compliance with labor laws (mandatory rest periods, max hours)" | This is the most structurally impactful requirement. The system must ENFORCE legal rules — not just track them. If the system allows an illegal schedule, the hospital faces regulatory penalties. This means compliance rules must be embedded in the scheduling engine's core logic, influencing architecture. |
| **Reliability** | "Shift swapping" + "500 nurses, 200 doctors" | A hospital scheduling system is operationally critical. If the system goes down during a shift swap window, nurses may not show up, creating patient safety risks. "Shift swapping" implies the system must reliably process time-sensitive state transitions (Nurse A off, Nurse B on) without data loss or race conditions. |
| **Auditability** | "Compliance with labor laws" + "PTO tracking" | Labor law compliance doesn't just mean enforcing rules — it means PROVING compliance. If a regulator audits the hospital, the system must produce records showing every scheduling decision respected rest periods and max hours. PTO tracking similarly requires a verifiable trail. This needs structural support (event logs, immutable records). |
| **Scalability** | "What if we expand to all 12 hospitals?" | The IT Director explicitly wants multi-hospital expansion capability. 12x growth from 700 to ~8,400 users, with separate hospital contexts, potentially different labor law jurisdictions, and cross-hospital staff sharing. |
| **Simplicity** | "3-person team, tight budget, just need it to work for one hospital first" | The strongest constraint. A 3-person team cannot build or maintain a complex distributed system. Every unnecessary architectural decision is a tax on a team this small. Simplicity directly influences structure: monolith vs. microservices, simple relational model vs. event-sourced system, etc. |

**Hidden characteristics probed:**

- Shift swapping implies **performance** — but 700 users is modest. No special architectural support needed for this load. Standard web framework handles it. Design concern, not architecture characteristic.
- PTO tracking implies **data integrity** — but this is handled by standard database transactions. Design concern.
- "Expand to 12 hospitals" implies **extensibility** — the system should be structured so multi-tenancy can be added later without a rewrite. This DOES influence structure (e.g., tenant-aware data model from day one vs. retrofitting later).

## Step 3: Identify Implicit Characteristics

| Characteristic | Reasoning |
|---------------|-----------|
| **Availability** | Hospital scheduling is a 24/7 operation. Nurses work night shifts, weekends, holidays. The system must be accessible at all hours for shift swaps and schedule checks. A scheduling outage during shift change could mean understaffed wards. This is implicit because nobody stated it, but a scheduling tool that has frequent downtime is unusable in a hospital context. |
| **Security** | The system handles employee PII (names, schedules, PTO balances), which falls under healthcare-adjacent data handling. While this isn't a clinical system (no HIPAA PHI), employee data still requires protection. However — does security require SPECIAL architectural support here, or is standard security practice sufficient? For an internal tool with 700 users behind a hospital network, standard authentication and authorization patterns suffice. This stays at design level unless the system becomes externally accessible. |
| **Usability** | Nurses and doctors are not power users of software. They need to swap shifts from a phone between rounds. If the system is hard to use, they will revert to paper or WhatsApp groups, defeating the purpose. However, usability is a UX/design concern, not an architecture characteristic — it doesn't require special structural support. |

## Step 4: Three-Criteria Validation

| Characteristic | Nondomain? | Influences Structure? | Critical? | Verdict |
|---------------|:---:|:---:|:---:|---------|
| **Legal / Compliance** | Yes | Yes — compliance rules engine must be a first-class architectural component, not sprinkled through business logic. Rules change by jurisdiction and over time. | Yes — regulatory violations carry fines and endanger hospital licensing. | **Include** |
| **Reliability** | Yes | Yes — requires careful state management for shift swaps (no double-bookings, no lost swaps), transaction design, and error handling strategy. | Yes — unreliable scheduling in a hospital creates patient safety risks. | **Include** |
| **Auditability** | Yes | Yes — requires immutable audit logs, event tracking, and potentially an append-only data pattern. Cannot be bolted on after the fact. | Yes — regulatory audits demand proof of compliance. | **Include** |
| **Simplicity** | Yes | Yes — directly determines architectural style (monolith vs distributed), technology choices, deployment model. THE most structural characteristic for a 3-person team. | Yes — a system too complex for the team to build and maintain will fail regardless of other qualities. | **Include** |
| **Availability** | Yes | Partially — standard cloud deployment with redundancy handles hospital-grade availability. No exotic architecture needed. | Important but not critical at architecture level — a managed database + load balancer provides sufficient availability. | **Include (low priority)** |
| **Scalability** | Yes | Yes — multi-tenancy, data isolation, tenant-aware routing all influence structure. BUT only if the system actually expands to 12 hospitals. | Not critical NOW. The system serves 700 users at one hospital. Premature optimization for 12x growth conflicts with simplicity for a 3-person team. | **Design-only for now** |
| **Extensibility** | Yes | Yes — plugin points, modular rule engines, clean boundaries. | Important but overlaps with simplicity — a well-structured simple system is inherently more extensible than a complex one. | **Design-only** |
| **Security** | Yes | No — standard authentication/authorization patterns. Internal hospital tool, not internet-facing. No special structural support needed beyond standard practices. | Important but handled at design level. | **Design-only** |
| **Performance** | Yes | No — 700 users is well within standard web app territory. No caching layers, no read replicas, no special optimization needed. | Not critical. | **Exclude** |
| **Usability** | No (it IS domain-adjacent) | No — UX concern, not structural. | Important for adoption but not architecture. | **Exclude (UX concern)** |

## Step 5: Categorization

| Category | Characteristics |
|----------|----------------|
| **Operational** | Reliability, availability |
| **Structural** | Simplicity, auditability |
| **Cross-Cutting** | Legal / compliance |

**Blind spot check:** The list skews toward operational and cross-cutting, which makes sense for a compliance-driven scheduling tool. Simplicity covers the structural side — for a 3-person team, maintainability and extensibility are downstream benefits of keeping things simple, not separate drivers.

## Step 6: Top 3 Driving Characteristics

### Elimination exercise applied:

Starting candidates: Legal/Compliance, Reliability, Auditability, Simplicity, Availability.

- Can we drop availability? Yes — standard cloud hosting provides sufficient availability. Not a special driver.
- Can we drop auditability? Tempting, but no — without audit trails, compliance is unverifiable. However, auditability is closely tied to legal/compliance. They can be treated as a package.
- Can we drop reliability? For a hospital scheduling system? No — patient safety is downstream.
- Can we drop simplicity? For a 3-person team with a tight budget? No — this is the existential constraint.
- Can we drop legal/compliance? For a system whose primary purpose includes labor law enforcement? No.

**Top 3:**

1. **Legal / Compliance** — This is the reason the system exists. A scheduling tool that doesn't enforce mandatory rest periods and max hours is worse than a spreadsheet because it creates a false sense of compliance. This must be a first-class architectural concern with a dedicated rules engine that can be updated as laws change across jurisdictions. Auditability is bundled here — compliance without provability is meaningless.

2. **Simplicity** — A 3-person team with a tight budget building for one hospital. This constraint dominates every architectural decision. Monolith over microservices. Single database over distributed data. Server-rendered pages over SPA + API. Convention over configuration. The IT Director's "enterprise-grade" aspiration must be tempered by reality: the best architecture is the one that gets built and maintained by the team you have. A simple, well-structured monolith can later be decomposed if multi-hospital expansion actually happens.

3. **Reliability** — Hospital scheduling directly affects patient care. A shift swap that silently fails, a double-booked nurse, or a schedule that loses changes means understaffed wards. The system must handle concurrent shift swaps without data corruption, survive server restarts without losing state, and clearly communicate failures rather than silently swallowing them. This requires careful transaction design and error handling strategy at the architectural level.

### Acknowledged but not driving

- **Auditability:** Critical for compliance but treated as part of the legal/compliance package rather than a separate driver. Structurally, this means immutable event logs for all scheduling decisions — implemented as part of the compliance architecture.
- **Availability:** Important (hospital is 24/7) but standard cloud deployment patterns (managed database, health checks, basic redundancy) provide sufficient availability without special architectural support. Not a driver.
- **Scalability:** The IT Director's concern about 12-hospital expansion is valid but premature as an architecture DRIVER. Recommendation: design a clean data model with a tenant identifier from day one (cheap to add, expensive to retrofit), but do NOT build multi-tenancy infrastructure now. When expansion actually happens, the simple monolith can be evolved. The Vasa warship sank trying to be everything at once — build the one-hospital tool first.
- **Security:** Standard authentication and authorization practices are sufficient. Implement role-based access (doctors vs nurses vs HR vs admin) at the design level. No special architectural support needed unless the system becomes internet-facing.
- **Extensibility:** A well-structured simple monolith with a clean compliance rules engine is inherently extensible. Don't add plugin architectures or extension points speculatively.

## Characteristics NOT Included (and why)

- **Performance:** 700 users is trivial load. Any standard web framework handles this without architectural consideration. Failed criterion 3 (not critical).
- **Usability:** Important for adoption but this is a UX/design concern. Doesn't influence system structure. Failed criterion 1 (it's a domain design consideration) and criterion 2 (doesn't influence structure).
- **Elasticity:** No burst traffic patterns. Hospital scheduling is steady-state, not Black Friday. Failed criterion 3.
- **Scalability (as a driver):** Premature for a 3-person team building for one hospital. 12-hospital expansion is speculative. Would conflict with the simplicity driver. Noted as a design consideration (tenant ID in data model) but not an architecture driver.
- **Interoperability:** No mention of integrating with existing hospital systems (EHR, payroll, time clocks) in requirements. If integration needs emerge, revisit. Failed criterion 3 (not established as critical).
- **Extensibility (as a driver):** Overlaps with simplicity. A simple, well-structured system is extensible by default. Adding explicit extension points adds complexity that conflicts with the #2 driver. Failed the "don't over-specify" principle.

---

## Summary for the Team

Your architecture should be driven by **legal compliance, simplicity, and reliability** — in that order. Concretely, this means:

- **Start with a monolith.** Single deployable, single database. Your 3-person team cannot afford the operational overhead of distributed systems.
- **Build a dedicated compliance rules engine** as a distinct module within the monolith. Labor law rules (rest periods, max hours) should be configurable and testable in isolation, not scattered through scheduling logic. When you expand to hospitals in different jurisdictions, you update rules — not architecture.
- **Log every scheduling decision immutably.** Every shift assignment, swap, and PTO approval gets an audit trail entry. This is your compliance proof.
- **Design transactions carefully for shift swaps.** Two nurses swapping shifts is a concurrent state mutation. Use database-level transactions and optimistic locking to prevent double-bookings and lost updates.
- **Add a tenant ID column now, build multi-tenancy later.** This is the one concession to future scalability that costs almost nothing today but would be very expensive to retrofit.

Tell your IT Director: "We're building it right for one hospital first, with a clean structure that can grow. Enterprise-grade doesn't mean enterprise-complex — it means enterprise-reliable." The architecture that ships and works beats the architecture that's still being designed.
