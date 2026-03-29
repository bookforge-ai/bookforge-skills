# ADR-27: Migrate from Monolith to Domain-Aligned Services for Healthcare Scheduling

## Status

**Accepted** — Supersedes ADR-12 (Monolithic Architecture)

## Date

2026-03-27

## Context

### Current Situation

Two years ago, ADR-12 established a monolithic architecture for our healthcare scheduling application. The original architect who authored ADR-12 has since left the organization, and the specific reasoning behind that decision was not sufficiently documented beyond the ADR itself. Based on available context, the monolith was likely chosen for speed of initial delivery, simplicity of deployment, and a smaller team size at the time.

Since then, the situation has changed significantly:

- **Team growth:** The engineering organization has grown to approximately 50 developers working on the same codebase.
- **Deployment duration:** A full production deployment now takes approximately 3 hours, creating long feedback cycles, delayed hotfixes, and increased risk per release.
- **Merge conflicts and coordination overhead:** Multiple teams frequently collide on shared modules, slowing feature delivery.
- **Blast radius:** A defect in one area (e.g., notification formatting) can block deployment of unrelated changes (e.g., scheduling algorithm improvements).
- **Scaling constraints:** The entire application must be scaled uniformly even when only specific capabilities (e.g., real-time availability checks) experience load spikes.

### Regulatory Constraint

The application processes Protected Health Information (PHI) and must comply with HIPAA (Health Insurance Portability and Accountability Act). The compliance team has raised specific concerns about a distributed architecture:

1. **Data residency and access control:** PHI must not be exposed across service boundaries without proper authorization and audit trails.
2. **Audit logging:** Every access to PHI must be traceable to a specific user, service, and purpose.
3. **Breach notification surface:** More network communication increases the surface area for potential data breaches.
4. **Business Associate Agreements (BAAs):** Any third-party infrastructure component handling PHI requires a BAA.
5. **Data consistency:** HIPAA requires accurate, unaltered records; eventual consistency models must not compromise record integrity.

## Decision

We will incrementally decompose the monolith into domain-aligned services, following a strangler fig migration pattern. We will NOT perform a big-bang rewrite.

### Service Boundaries (Initial Decomposition)

Services are aligned to bounded contexts identified through domain analysis:

| Service | Responsibility | PHI Exposure |
|---------|---------------|--------------|
| **Scheduling Core** | Appointment CRUD, conflict detection, recurring schedules | Yes — patient identifiers, appointment details |
| **Provider Management** | Provider profiles, credentials, availability templates | Minimal — provider data, no patient PHI |
| **Patient Identity** | Patient demographics, insurance, consent records | Yes — high sensitivity, canonical PHI source |
| **Notifications** | Appointment reminders, confirmations, cancellations | Yes — contains patient contact info and appointment references |
| **Reporting & Analytics** | Operational dashboards, utilization metrics | Yes — aggregated but derived from PHI |
| **Auth & Access Control** | Authentication, RBAC, session management | Indirect — controls access to all PHI |

### HIPAA Compliance Architecture

To address the compliance team's concerns directly:

**1. PHI Boundary Enforcement**

- All services that handle PHI are deployed within a single HIPAA-compliant VPC (the "PHI zone"). No PHI leaves this zone except through explicitly audited, encrypted channels.
- Services outside the PHI zone (e.g., a future public-facing landing page) receive only de-identified or tokenized data.

**2. Service-to-Service Communication**

- All inter-service communication uses mutual TLS (mTLS) with short-lived certificates.
- A service mesh (e.g., Istio or Linkerd) enforces encryption in transit, authorization policies, and traffic observability.
- Each service authenticates via service identity tokens. No service can access another's data without explicit policy authorization.

**3. Centralized Audit Logging**

- Every service emits structured audit events to a centralized, append-only audit log (e.g., an immutable event store or a WORM-compliant storage backend).
- Audit events include: timestamp, service identity, user identity (propagated via request context), action performed, resource affected, and outcome.
- The audit log is separate from application logs and has independent access controls.

**4. Data Ownership and Access Patterns**

- Each service owns its data store exclusively. No shared databases.
- Cross-service data access occurs only through well-defined APIs, never through direct database queries.
- The Patient Identity service is the single source of truth for PHI. Other services reference patients by opaque identifiers and request only the minimum necessary data fields (HIPAA Minimum Necessary Rule).

**5. Encryption**

- Data at rest: AES-256 encryption on all data stores within the PHI zone, with keys managed by a dedicated KMS.
- Data in transit: TLS 1.3 for all communication, both internal (mTLS) and external.

**6. BAA Coverage**

- All infrastructure providers (cloud provider, service mesh, logging platform, secrets manager) must have signed BAAs before handling any PHI workload.
- A BAA registry will be maintained and reviewed quarterly.

### Migration Strategy

**Phase 1 — Extract Auth & Access Control (Months 1-3)**
- Lowest PHI risk. Establishes the security foundation (service mesh, mTLS, audit logging) that all subsequent services depend on.
- The monolith delegates authentication/authorization to the new service.

**Phase 2 — Extract Provider Management (Months 3-5)**
- Minimal PHI exposure. Validates the data-separation pattern and inter-service communication without high-risk data.

**Phase 3 — Extract Notifications (Months 5-7)**
- Moderate PHI exposure. Tests the audit-logging pipeline with real PHI flows. Provides an independent deployment win (notification changes no longer block scheduling deployments).

**Phase 4 — Extract Patient Identity (Months 7-10)**
- Highest sensitivity. By this point, the infrastructure patterns, audit logging, and access-control mechanisms are proven. This service becomes the canonical PHI source behind a well-defined API.

**Phase 5 — Extract Scheduling Core (Months 10-14)**
- The largest and most complex extraction. Depends on Patient Identity and Provider Management APIs being stable.

**Phase 6 — Extract Reporting & Analytics (Months 14-16)**
- Consumes data from other services. Can use event-driven projections from domain events published by other services.

### Compliance Validation Gates

Each phase includes a compliance gate before production traffic is routed to the new service:

1. **Threat model review** — Updated threat model for the new service boundary.
2. **Penetration test** — Targeted test on the new service and its communication paths.
3. **Audit log verification** — Confirm all PHI access paths are captured in the audit log with required fields.
4. **Access control review** — Verify least-privilege policies and that the Minimum Necessary Rule is enforced.
5. **Data flow documentation** — Updated data flow diagrams showing PHI paths, submitted to the compliance team.
6. **BAA confirmation** — All new infrastructure components have signed BAAs.

## Consequences

### Positive

- **Independent deployability:** Teams can deploy their services independently, reducing the 3-hour monolith deployment to per-service deployments measured in minutes.
- **Team autonomy:** Clear service ownership enables teams to make decisions independently within their bounded context.
- **Targeted scaling:** High-traffic services (e.g., real-time availability checks in Scheduling Core) can be scaled independently.
- **Reduced blast radius:** A defect in Notifications does not block a Scheduling Core deployment.
- **Improved HIPAA posture:** Explicit PHI boundaries, enforced access policies, and comprehensive audit logging actually strengthen compliance compared to the monolith, where any code path could potentially access any data.

### Negative

- **Operational complexity:** Distributed systems require investment in observability, distributed tracing, and incident response tooling.
- **Data consistency challenges:** Some operations that were previously single-transaction in the monolith will require saga patterns or eventual consistency. For HIPAA-critical records (e.g., appointment creation), we will use synchronous, transactional flows rather than eventual consistency.
- **Migration duration:** The 14-16 month phased migration means the team will operate in a hybrid monolith-plus-services state for an extended period, which increases cognitive load.
- **Infrastructure cost:** Service mesh, per-service data stores, centralized audit logging, and KMS add infrastructure cost. Estimated 30-40% increase in cloud spend, offset by reduced developer time lost to deployment bottlenecks.
- **Testing complexity:** End-to-end testing across service boundaries requires contract testing and integration test environments.

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| PHI leaks across service boundaries | Medium | Critical | mTLS, service mesh policies, audit logging, penetration testing at each phase gate |
| Distributed transaction failures corrupt scheduling data | Medium | High | Saga pattern with compensating transactions; critical paths remain synchronous; idempotency keys on all write APIs |
| Migration stalls in hybrid state | Medium | High | Each phase delivers independent value; the monolith remains functional; no phase depends on completing all phases |
| Compliance team blocks a phase | Low | High | Compliance is involved from Phase 1; gate criteria are defined upfront; no surprises |
| Loss of institutional knowledge about service boundaries | Low | Medium | This ADR, plus per-service ADRs, data flow diagrams, and runbooks are maintained as living documents |

## Alternatives Considered

### 1. Optimize the Monolith

Improve build/deploy pipeline, add modular boundaries within the monolith (e.g., Java modules or Python namespace packages), parallelize CI.

**Rejected because:** While this could reduce deployment time to perhaps 1-1.5 hours, it does not address team coupling, independent scaling, or blast radius. At 50 developers, the coordination overhead is a fundamental constraint, not just a tooling problem.

### 2. Big-Bang Rewrite to Microservices

Rebuild the system from scratch as microservices.

**Rejected because:** High risk of failure for a system handling PHI in production. Extended period with no deliverable value. The original system's implicit business rules (accumulated over two years) would be difficult to replicate without regression. Industry data suggests big-bang rewrites of this scale fail more often than they succeed.

### 3. Modular Monolith (Monolith with Hard Module Boundaries)

Keep a single deployable unit but enforce strict module boundaries with separate data schemas per module.

**Considered seriously.** This would address team coupling and blast radius to some degree while avoiding distributed-systems complexity. **Rejected because:** It does not solve independent deployability (the primary pain point at 3-hour deployments), does not enable independent scaling, and at 50 developers the single deployment pipeline remains a bottleneck. However, we adopt the modular-monolith mindset during migration: each service extraction first establishes clean module boundaries within the monolith before extraction.

### 4. Micro-Frontends with Backend Monolith

Decompose only the frontend; keep the backend monolith.

**Rejected because:** The deployment bottleneck is backend-driven (build, test, database migrations). Frontend decomposition alone does not address the core problem.

## Relationship to ADR-12

ADR-12 chose a monolithic architecture. Based on the team size and product maturity at that time, this was a reasonable decision. The conditions that made it reasonable — small team, rapid iteration needs, simple deployment requirements — no longer hold. This ADR supersedes ADR-12 by establishing a migration path away from the monolith while preserving its operational stability during the transition.

## References

- HIPAA Security Rule (45 CFR Part 160 and Subparts A and C of Part 164)
- HIPAA Minimum Necessary Rule (45 CFR 164.502(b))
- Sam Newman, "Monolith to Microservices" (O'Reilly, 2019)
- Martin Fowler, "StranglerFigApplication" (martinfowler.com)
- Michael Nygard, "Documenting Architecture Decisions" (cognitect.com/blog)

## Signatories

- **Author:** [Your Name], [Role]
- **Reviewers:** [Compliance Lead], [Infrastructure Lead], [Engineering Managers]
- **Approvers:** [CTO], [CISO], [VP Engineering]
