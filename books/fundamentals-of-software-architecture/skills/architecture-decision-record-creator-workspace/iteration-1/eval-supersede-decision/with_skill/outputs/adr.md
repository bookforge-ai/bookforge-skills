# ADR 47: Decompose Healthcare Scheduling Monolith into Domain-Aligned Services with HIPAA-Compliant Data Isolation

## Status
Proposed (supersedes ADR-12)

*This ADR requires approval from: Chief Architect, Compliance Officer, HIPAA Security Officer, and Engineering Leadership before implementation begins.*

## Context

Two years ago, ADR-12 established a monolithic architecture for our healthcare scheduling application. The original rationale for that decision is no longer available — the authoring architect has left the organization and ADR-12 lacks sufficient justification in its Decision section (a cautionary example of why the WHY matters more than the HOW in architecture decision records).

Since ADR-12 was written, the following forces have fundamentally changed the operating context:

- **Team scale:** The engineering team has grown from a small team to **50 developers** working in the same codebase. Merge conflicts, ownership ambiguity, and coordination overhead have become daily friction.
- **Deployment velocity:** A full production deployment now takes **3 hours**, creating a bottleneck that limits our ability to ship urgent fixes — including security patches required for HIPAA compliance. In a regulated healthcare environment, the inability to rapidly deploy a security fix is itself a compliance risk.
- **Release coupling:** A bug in scheduling logic blocks deployment of unrelated payment or notification features. Every release is an all-or-nothing event, increasing blast radius and rollback complexity.
- **Scalability constraints:** The scheduling engine, patient notifications, and billing modules have vastly different load profiles but cannot be scaled independently.
- **Regulatory pressure:** HIPAA requires that Protected Health Information (PHI) be subject to access controls, audit logging, and breach containment. The compliance team has raised concerns that distributing data across services could widen the attack surface and complicate audit trails.

**Alternatives considered:**

1. **Maintain the monolith (status quo):** Keep the existing architecture and invest in build/deployment optimization. This addresses the symptom (slow deployment) but not the root causes (team coupling, independent scalability, blast radius).
2. **Modular monolith:** Enforce strict module boundaries within the monolith using internal APIs and separate data schemas, but deploy as a single unit. This reduces code coupling but does not solve deployment coupling or independent scalability.
3. **Domain-aligned services with HIPAA-compliant data isolation (recommended):** Decompose into services aligned to bounded contexts, with PHI concentrated in a dedicated, hardened data service behind a strict API boundary. Each service owns its data and can be deployed independently.
4. **Microservices (fine-grained):** Decompose into many small services per function. This maximizes independence but introduces excessive operational complexity for a 50-person team and dramatically increases the HIPAA compliance surface area.

## Decision

We will decompose the monolith into **domain-aligned services** organized around bounded contexts, with a dedicated **PHI Data Service** that centralizes all Protected Health Information behind a single, hardened API boundary. We will NOT adopt fine-grained microservices.

**WHY this approach, and WHY now:**

1. **Developer productivity is a business-critical constraint.** With 50 developers, the monolith has become a coordination bottleneck. Independent service ownership enables teams to deploy on their own cadence. Reducing deployment time from 3 hours to minutes directly translates to faster feature delivery and faster time-to-market for new scheduling capabilities — a competitive differentiator in healthcare SaaS.

2. **HIPAA compliance is strengthened, not weakened, by this design.** The compliance team's concern about distributed data is valid for naive service decomposition. Our approach deliberately addresses this: PHI is NOT distributed across services. Instead, all PHI resides in a single, purpose-built PHI Data Service with:
   - Dedicated encryption at rest and in transit (AES-256, TLS 1.3)
   - Row-level access control enforced at the API layer
   - Comprehensive audit logging of every PHI access (who, what, when, why)
   - A minimized blast radius — a breach in the Scheduling Service or Notification Service does NOT expose PHI because those services hold only opaque patient identifiers, never raw PHI
   - Separate infrastructure isolation (dedicated VPC subnet, dedicated database instance)

3. **The monolith's deployment coupling is a compliance liability.** A 3-hour deployment window means security patches take 3 hours to reach production. In a HIPAA-regulated environment, the inability to rapidly remediate a known vulnerability is an audit finding. Independent deployability directly supports our obligation to maintain timely security patching.

4. **Domain-aligned (not fine-grained microservices) because operational complexity must be proportional to team capacity.** A 50-person team can effectively own 5-8 services. Fine-grained microservices (20+) would require platform engineering investment we are not yet prepared to make, and each additional service boundary that touches PHI adds compliance overhead.

**Proposed service boundaries (initial decomposition):**

| Service | Domain | Owns PHI? |
|---------|--------|-----------|
| **PHI Data Service** | Patient identity, demographics, medical record references | YES — the single source of truth for all PHI |
| **Scheduling Service** | Appointment booking, availability, calendar management | No — references patients by opaque ID only |
| **Billing Service** | Claims, payments, insurance verification | Limited — holds billing-specific PHI (delegated from PHI Data Service with explicit scope) |
| **Notification Service** | Reminders, alerts, communication preferences | No — receives only delivery addresses, no clinical data |
| **Provider Service** | Provider profiles, credentials, schedules | No |
| **API Gateway** | Authentication, authorization, rate limiting, request routing | No — passes through tokens, does not store PHI |

**WHY we supersede ADR-12 rather than amend it:** ADR-12's monolithic architecture was appropriate for a small team shipping an MVP. The forces that justified it (simplicity, speed of initial development, small team coordination) no longer apply. Amending it would obscure the decision history. This new ADR creates a clear, traceable record: ADR-12 represented the right choice for its time; ADR-47 represents the right choice for current scale.

## Consequences

### Positive
- **Deployment time drops from 3 hours to 15-30 minutes per service**, unblocking rapid iteration and security patching
- **Team autonomy increases** — each team owns a service end-to-end, reducing cross-team coordination overhead and merge conflicts
- **HIPAA compliance posture improves** — PHI is concentrated in one hardened service with dedicated access controls, audit logging, and encryption, rather than spread across an entire monolithic codebase where any developer can access it
- **Blast radius is contained** — a failure in Notification Service does not affect Scheduling; a breach in Scheduling does not expose PHI
- **Independent scalability** — the Scheduling Service (high read volume) can scale separately from Billing (high write volume during claims processing)
- **Security patching speed improves** — critical patches to the PHI Data Service can be deployed in minutes without redeploying unrelated services

### Negative
- **Distributed system complexity** — network failures, partial outages, and eventual consistency scenarios that did not exist in the monolith
- **Operational overhead increases** — requires investment in service mesh or API gateway, centralized logging, distributed tracing, and container orchestration
- **Migration risk** — the decomposition itself is a multi-quarter effort with risk of data inconsistency during the transition period
- **Testing complexity** — integration testing across service boundaries is harder than testing within a monolith; contract testing must be established
- **Team skill gap** — the team has monolith experience; distributed systems debugging and service ownership patterns require training
- **Billing Service PHI delegation** — even with scoped access, the Billing Service touching any PHI creates a second compliance surface that must be audited separately

### Trade-offs
- We accept increased operational complexity in exchange for deployment independence and team autonomy
- We accept the cost of building and maintaining a dedicated PHI Data Service in exchange for a stronger, more auditable HIPAA compliance posture
- We accept a multi-quarter migration timeline in exchange for a sustainable architecture that supports the next phase of growth
- We accept the need for new infrastructure (service mesh, distributed tracing, container orchestration) in exchange for independent scalability and fault isolation
- We accept that the Billing Service will hold scoped PHI (a pragmatic compromise) rather than forcing all billing operations through the PHI Data Service (which would create a performance bottleneck and tight coupling)

## Compliance

### Architectural Compliance
- **Type:** Automated fitness function + Manual review
- **Mechanism:**
  - **Automated — PHI boundary enforcement:** A CI pipeline test scans every service's codebase and database schema to verify that only the PHI Data Service (and the explicitly scoped Billing Service) contain PHI fields. Any service introducing a PHI column or field fails the build. Implementation: a custom linter or Open Policy Agent (OPA) policy that checks database migration files and API schemas against a PHI field registry.
  - **Automated — Service dependency direction:** An architecture fitness function (e.g., ArchUnit equivalent or dependency analysis in CI) verifies that no service directly accesses the PHI Data Service's database — all access must go through its API. Direct database connections from other services fail the build.
  - **Automated — Contract testing:** Consumer-driven contract tests (Pact or similar) run in CI to ensure service interface compatibility and prevent breaking changes.
  - **Manual — Quarterly architecture review:** Review service boundaries, PHI access patterns, and any proposed new services against HIPAA requirements. Any new service that needs PHI access requires a compliance review before approval.
- **Frequency:** Automated checks run on every pull request and merge to main. Manual review quarterly and on any proposed new service boundary.

### HIPAA Compliance
- **Type:** Automated audit + Manual review
- **Mechanism:**
  - **Automated — PHI access audit logging:** The PHI Data Service logs every access (read, write, delete) with requestor identity, timestamp, patient ID, fields accessed, and business justification. Logs are immutable (append-only, shipped to a separate audit store).
  - **Automated — Access anomaly detection:** Alerting on unusual PHI access patterns (bulk reads, access outside business hours, access by service accounts not on the allowlist).
  - **Manual — Annual HIPAA risk assessment:** Include the service architecture in the annual risk assessment, specifically evaluating the PHI Data Service's access controls and the Billing Service's scoped PHI access.
- **Frequency:** Audit logging is continuous. Anomaly alerting is real-time. Risk assessment is annual (or triggered by significant architecture changes).

## Notes
- **Author:** [Requesting architect — to be filled by the proposer]
- **Date:** 2026-03-27
- **Approved by:** Pending — requires sign-off from Chief Architect, Compliance Officer, HIPAA Security Officer, and Engineering Leadership
- **Last modified:** 2026-03-27
- **Supersedes:** ADR-12 (Monolithic Architecture for Healthcare Scheduling Application)
- **Superseded by:** N/A
- **Related decisions:** Upon acceptance, ADR-12 must be updated to status "Superseded by ADR-47"
- **Migration plan:** A separate ADR (ADR-48) should document the phased migration strategy, including the sequence of service extractions, data migration approach, and rollback procedures. This ADR documents the target architecture; ADR-48 will document how we get there.
- **Context on ADR-12:** The original architect who authored ADR-12 has left the organization. ADR-12's Decision section lacked sufficient justification (the WHY). This is documented here as institutional learning: every ADR must capture the full reasoning, because personnel change but decisions persist. Future architects reading this ADR should find complete justification for every aspect of this decision.
