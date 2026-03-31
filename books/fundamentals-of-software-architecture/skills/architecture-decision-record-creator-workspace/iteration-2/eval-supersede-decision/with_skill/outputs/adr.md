## Significance Assessment
| Dimension | Affected? | How |
|-----------|:---------:|-----|
| Structure | Yes | Fundamentally changes the system from a single deployable monolith to a distributed service-based architecture with independently deployable units |
| Nonfunctional characteristics | Yes | Directly impacts deployability (3-hour deployment → per-service deploys), scalability (independent service scaling), security (HIPAA data isolation across service boundaries), and team autonomy |
| Dependencies | Yes | Introduces inter-service communication where none existed; creates new coupling patterns between services and a shared compliance infrastructure layer |
| Interfaces | Yes | Services will expose APIs to each other (REST, messaging, or gRPC); new service contracts must be defined where previously there were in-process method calls |
| Construction techniques | Yes | Requires new deployment tooling (container orchestration, CI/CD per service), distributed tracing, service mesh or API gateway, and HIPAA-compliant logging infrastructure |

**Verdict:** Architecturally significant — affects 5 of 5 dimensions.

---

# ADR 13: Migrate from Monolith to Service-Based Architecture with HIPAA-Compliant Data Isolation

## Status
Proposed (supersedes ADR-12)

## Context

Two years ago, ADR-12 established a monolithic architecture for our healthcare scheduling application. The original architect who authored ADR-12 has since left the company, and **the rationale for choosing a monolith was never documented** — a classic **Groundhog Day anti-pattern** where a past decision is being revisited because nobody can explain WHY it was made. This ADR includes full justification to prevent recurrence.

The forces driving this decision:

- **Deployment bottleneck:** Deployment now takes approximately 3 hours. With 50 developers contributing to a single deployable unit, even small changes require a full deployment cycle. This directly harms time-to-market and developer productivity.
- **Team scaling friction:** 50 developers working in a single codebase creates merge conflicts, long build times, and unclear ownership boundaries. Conway's Law tells us our architecture should mirror our desired team structure — and right now, it cannot.
- **HIPAA compliance concerns:** The compliance team has raised legitimate concerns about distributing Protected Health Information (PHI) across service boundaries. In a monolith, PHI stays within a single process and database. In a distributed architecture, PHI may traverse network boundaries, reside in multiple data stores, and appear in inter-service logs — each creating new vectors for compliance violations.

**Alternatives considered:**

1. **Modular monolith** — Restructure the monolith into well-defined modules with strict boundaries, but keep a single deployable unit. This addresses code ownership but does NOT solve the 3-hour deployment problem, since the entire application still deploys as one artifact.
2. **Service-based architecture with shared database** — Decompose into coarse-grained services (5-12 domain services) that share the existing database. Reduces deployment scope while minimizing data distribution risk. Services own their domain logic but access a shared data layer.
3. **Microservices with per-service databases** — Full decomposition into fine-grained services each owning its data. Maximum independence but maximum HIPAA complexity — PHI would be distributed across many independent data stores, each requiring separate encryption, audit logging, and access controls.
4. **Maintain status quo** — Keep the monolith. This avoids migration risk but does not address the deployment bottleneck or team scaling problems, which will worsen as the team grows.

## Decision

**We will adopt a service-based architecture (Alternative 2) — coarse-grained domain services with a shared HIPAA-compliant database layer — and explicitly reject microservices (Alternative 3) at this time.**

**WHY service-based over microservices:** The compliance team's HIPAA concerns are valid and must be treated as a first-class architectural constraint, not a problem to solve later. A service-based architecture with a shared database keeps PHI in a single, auditable data store with established encryption-at-rest and access controls. This directly addresses the compliance team's concern: PHI does not traverse service boundaries at the data layer. Microservices would require us to solve distributed PHI governance (per-service encryption, cross-service audit trails, distributed access controls) before we could deploy — adding 6-12 months of compliance engineering with no business value beyond what service-based provides.

**WHY service-based over modular monolith:** The modular monolith (Alternative 1) addresses code ownership but does NOT solve the deployment bottleneck. With 50 developers and a 3-hour deployment, we need independent deployability — not just independent development. Service-based architecture gives us both.

**WHY not maintain status quo:** At current growth trajectory (hiring 10-15 developers/year), the deployment bottleneck and merge conflicts will become the primary constraint on product velocity within 6 months. The cost of inaction exceeds the cost of migration.

**Business justification:** Reducing deployment time from 3 hours to 15-30 minutes per service unlocks faster feature delivery, reduces the blast radius of failed deployments (improving system reliability for patients), and removes the primary developer productivity bottleneck — directly impacting time-to-market and operational cost.

**Implementation approach:**

1. Identify 5-8 domain boundaries (scheduling, patient management, provider management, billing, notifications, reporting, authentication/authorization, compliance/audit).
2. Extract services incrementally using the Strangler Fig pattern — new features are built as services, existing features are migrated one domain at a time.
3. PHI access is mediated through the shared database with a dedicated HIPAA data access layer that enforces row-level security, audit logging, and encryption.
4. Inter-service communication for non-PHI data uses asynchronous messaging; any communication involving PHI references uses the shared database as the integration point (no PHI in message payloads).

## Consequences

### Positive
- **Deployment time reduced from 3 hours to 15-30 minutes per service**, unblocking 50 developers from waiting on a single deployment pipeline
- **Independent team ownership** — each domain service is owned by a specific team (6-8 developers), reducing merge conflicts and enabling autonomous feature delivery
- **Blast radius containment** — a failed deployment in the notification service does not bring down scheduling or patient management
- **HIPAA compliance preserved** — PHI remains in a single database with existing encryption, access controls, and audit logging intact; no new compliance vectors introduced at the data layer
- **Incremental migration via Strangler Fig** — no big-bang rewrite; the monolith continues to serve traffic while services are extracted one domain at a time, reducing migration risk
- **Decision rationale documented** — unlike ADR-12, this ADR explicitly captures WHY this architecture was chosen, preventing future Groundhog Day revisitation

### Negative
- **Operational complexity increases** — we now operate 5-8 services instead of 1; this requires investment in container orchestration, service monitoring, distributed tracing, and on-call runbooks per service
- **Network latency introduced** — what were in-process method calls become network calls; some workflows (e.g., scheduling + billing) will experience added latency
- **Shared database becomes a coupling point** — while it solves the HIPAA problem, it creates a coordination bottleneck for schema changes; a migration in the shared database can affect all services
- **Testing complexity** — integration testing across service boundaries requires new tooling (contract tests, staging environments per service)
- **Team skill gap** — the team has operated a monolith for 2 years; distributed systems debugging, service orchestration, and container management are new skills that require training

### Trade-offs
- **We accept shared database coupling in exchange for HIPAA simplicity.** This is a deliberate, temporary constraint. Once the compliance team is confident in distributed PHI governance (encryption per service, cross-service audit trails), we can migrate to per-service databases — but that is a future ADR, not this one.
- **We accept higher operational overhead in exchange for deployment independence.** The 3-hour deployment bottleneck is a concrete, measurable cost today. The operational overhead is real but manageable with proper investment in observability tooling.
- **We accept incremental migration duration (estimated 12-18 months for full extraction) in exchange for reduced migration risk.** A big-bang rewrite would be faster in theory but carries catastrophic failure risk for a healthcare system where downtime directly impacts patient care.

## Compliance

### Architectural Compliance
- **Type:** Automated fitness function
- **Mechanism:** CI pipeline test that verifies no service directly accesses another service's database tables. All cross-domain data access must go through the HIPAA data access layer. Implemented as a static analysis check on database query patterns per service.
- **Frequency:** Every pull request and nightly build

### HIPAA Compliance
- **Type:** Automated fitness function + Manual review
- **Mechanism (automated):**
  - Fitness function verifying that no inter-service message payloads contain PHI fields (patient name, SSN, DOB, medical record number). Scans message schema definitions in CI.
  - Audit log completeness check: automated test verifying that every PHI database access generates an audit log entry (required by HIPAA §164.312(b)).
  - Encryption verification: automated check that database connections use TLS and data-at-rest encryption is enabled on all PHI tables.
- **Mechanism (manual):** Quarterly compliance review with the compliance team to assess whether the service boundaries maintain PHI isolation guarantees. Review covers: new services added, any changes to the data access layer, and audit log sampling.
- **Frequency:** Automated checks on every PR; manual review quarterly

### Service Boundary Compliance
- **Type:** Manual review
- **Mechanism:** Architecture review for any new service extraction. Before a domain is extracted from the monolith, the proposal must be reviewed against this ADR's principles: shared database for PHI, no PHI in messages, Strangler Fig migration pattern.
- **Frequency:** Per extraction event (estimated 5-8 times over 12-18 months)

## Notes
- **Author:** [Requesting architect — name to be filled]
- **Date:** 2026-03-27
- **Approved by:** Pending — requires approval from: (1) Engineering Director, (2) HIPAA Compliance Officer, (3) VP of Product
- **Last modified:** 2026-03-27
- **Supersedes:** ADR-12 (Monolithic Architecture for Healthcare Scheduling App)
- **Superseded by:** N/A
- **Migration to ADR-12:** Upon acceptance of this ADR, update ADR-12 status to "Superseded by ADR-13"
