# Quantum Analysis: Healthcare Platform

## Step 1: Components Identified

This is a greenfield design with no codebase. Components are derived from the user's system description.

| Component | Responsibility | Deployment unit |
|-----------|---------------|----------------|
| Patient Scheduling | Appointment booking, nurse-facing 24/7 scheduling for 500 concurrent nurses | TBD (greenfield) |
| Billing Integration | HIPAA-compliant insurance claim processing, payment handling | TBD (greenfield) |
| Patient Portal | Patient-facing portal for viewing test results, medical records | TBD (greenfield) |
| Admin Reporting | Weekly batch reports for administrators, low traffic | TBD (greenfield) |

## Step 2: Communication Map

Based on domain analysis of a typical healthcare platform, the communication patterns between these four components are:

| From | To | Type | Mechanism | Fate-sharing? |
|------|-----|------|-----------|:---:|
| Patient Scheduling | Billing Integration | **Async** | Message queue (event: "appointment.completed") | No |
| Patient Scheduling | Patient Portal | **Async** | Message queue (event: "appointment.scheduled") | No |
| Billing Integration | Patient Portal | **Async** | Message queue (event: "claim.processed", "balance.updated") | No |
| Admin Reporting | Patient Scheduling | **Async** | Read from reporting replica / data warehouse | No |
| Admin Reporting | Billing Integration | **Async** | Read from reporting replica / data warehouse | No |
| Admin Reporting | Patient Portal | **Async** | Read from reporting replica / data warehouse | No |

**Key observation:** None of these four features require synchronous, real-time request-response communication with each other. A nurse scheduling an appointment does not need to wait for billing to confirm insurance in real time. A patient checking test results does not need to call the scheduling service synchronously. Admin reporting runs batch jobs against historical data. These are naturally decoupled domains.

This is significant because **synchronous connascence = shared fate** (the quantum rule). The absence of synchronous cross-component communication means these components do NOT share operational fate — they can have independent characteristics.

## Step 3: Architecture Characteristics Per Component

This is the critical step. The user's description reveals sharply different quality attribute needs:

| Characteristic | Patient Scheduling | Billing Integration | Patient Portal | Admin Reporting |
|---------------|-------------------|--------------------|--------------------|-----------------|
| **Availability** | **Very High** (24/7, 500 nurses, patient care depends on it) | High (claims must process, but not real-time) | High (patients expect access) | **Low** (weekly batch, can tolerate downtime) |
| **Performance** | High (nurses need fast response under load) | Moderate (batch claim processing acceptable) | **Very High** (patients expect instant test results) | **Low** (batch reports can take minutes) |
| **Scalability** | **High** (500 concurrent nurses, peak shift changes) | Moderate (claim volume is predictable) | **High** (patient population can spike, e.g. flu season) | **Low** (single admin or scheduled cron) |
| **Security** | High (PHI data, HIPAA) | **Very High** (financial data + PHI, HIPAA, PCI considerations) | High (PHI data, HIPAA) | Moderate (internal only, aggregated data) |
| **Reliability** | High (missed appointments = care gaps) | **Very High** (lost claims = lost revenue, compliance violations) | Moderate (temporary unavailability is tolerable) | Low (retry next week) |
| **Elasticity** | Moderate (predictable shift patterns) | Low (steady claim flow) | **High** (unpredictable patient access patterns) | None |

**The characteristics are clearly non-uniform.** This is NOT a case where one set of quality attributes serves the whole system. Each component has a distinct profile.

**Caution check (uniform characteristics anti-pattern):** The CTO's suggestion of "microservices for everything" actually hints at an intuition that the system is not uniform — but microservices is a specific implementation choice, not a necessary consequence. What matters is the quantum count.

## Step 4: Quantum Grouping

Applying the three-criteria test (deploy together + high functional cohesion + synchronous connascence):

### Quantum 1: Patient Scheduling
- **Components:** Patient Scheduling service + its database
- **Cohesion:** Unified business purpose — managing appointments
- **Connascence:** No synchronous dependencies on other components
- **Database:** Own database (appointment data, nurse assignments, time slots)

### Quantum 2: Billing Integration
- **Components:** Billing service + its database
- **Cohesion:** Unified business purpose — insurance claims, payments, financial records
- **Connascence:** Receives events asynchronously from Scheduling. No sync calls.
- **Database:** Own database (claims, transactions, insurance records). **Must be isolated** — HIPAA audit trail and financial data integrity demand it.

### Quantum 3: Patient Portal
- **Components:** Patient Portal service + its database (or read replicas)
- **Cohesion:** Unified business purpose — patient-facing access to their health data
- **Connascence:** Reads data asynchronously (materialized views or event-sourced projections from scheduling and billing events). No sync coupling.
- **Database:** Own read-optimized database (patient records, test results, appointment history)

### Quantum 4: Admin Reporting
- **Components:** Reporting service + data warehouse / reporting database
- **Cohesion:** Unified business purpose — generating aggregate reports
- **Connascence:** Reads from data warehouse populated via ETL/CDC. Fully decoupled.
- **Database:** Reporting data warehouse (aggregated, denormalized data)

**Database note:** Shared database = shared quantum. If the CTO were to put all four services on one PostgreSQL instance, they would functionally be ONE quantum regardless of separate service binaries — because a schema migration or DB outage affects all services. Each quantum must own its data store to be truly independent.

## Step 5: Quantum Characteristic Comparison

| Characteristic | Q1: Scheduling | Q2: Billing | Q3: Patient Portal | Q4: Admin Reporting | Uniform? |
|---------------|:-:|:-:|:-:|:-:|:---:|
| Availability | Very High | High | High | Low | **No** |
| Performance | High | Moderate | Very High | Low | **No** |
| Scalability | High | Moderate | High | Low | **No** |
| Security | High | Very High | High | Moderate | **No** |
| Reliability | High | Very High | Moderate | Low | **No** |
| Elasticity | Moderate | Low | High | None | **No** |

**Every single characteristic is non-uniform across quanta.** This is a textbook case for distribution.

## Step 6: Architecture Direction

**Quantum count:** 4

**Characteristic uniformity:** Non-uniform (all six measured characteristics differ across quanta)

**Recommendation:** Distributed architecture required

**Reasoning:**

The quantum analysis confirms that 4 independently deployable units are justified — but NOT necessarily 4 microservices in the way the term is commonly used. Here is the precise reasoning:

1. **Four quanta, four different profiles.** Patient Scheduling needs very high availability (24/7 nurse operations). Billing needs very high reliability and security (HIPAA, financial integrity). Patient Portal needs very high performance and elasticity (patient-facing, unpredictable load). Admin Reporting needs almost nothing — it runs weekly batch jobs. A single monolith would force all four to share the same availability, performance, and scalability envelope. You would be over-provisioning for reporting and under-provisioning for scheduling.

2. **No synchronous cross-quantum coupling.** The communication map shows all inter-component communication can be asynchronous. This means the quanta are genuinely independent — one quantum's outage does not cascade to others. This is the ideal case for distribution.

3. **The CTO is directionally right but imprecise.** "Microservices for everything" implies fine-grained services — potentially dozens. The quantum analysis says you need exactly **4 deployment units**, not more. Each quantum could internally be a modular monolith (one well-structured service) rather than a swarm of microservices. The architecture style per quantum could be:
   - **Q1 (Scheduling):** Service-based or modular monolith — straightforward CRUD with availability focus
   - **Q2 (Billing):** Service-based with strong transactional guarantees — pipeline pattern for claim processing
   - **Q3 (Patient Portal):** Could be a lightweight read-optimized service, possibly event-sourced
   - **Q4 (Admin Reporting):** Simple batch service, possibly serverless/scheduled Lambda — minimal infrastructure

4. **You need 4 deployment units, not 40.** The danger of "microservices for everything" is splitting each quantum further without justification. Unless sub-components within a quantum have different characteristics (they don't, based on current analysis), further decomposition adds operational complexity (more deployments, more network calls, more failure modes) without benefit.

## Answering the CTO's Question Directly

> "Our CTO says microservices for everything. Should we?"

**Not microservices for everything. But also not a monolith.** You need exactly 4 independently deployable units — one per quantum. Each unit can be internally simple (a single well-structured service). The quantum analysis shows genuine characteristic divergence that a monolith cannot accommodate, but it does NOT show the kind of fine-grained decomposition that warrants dozens of microservices.

> "How many deployment units do we really need?"

**Four.** One for each quantum identified:

| # | Deployment Unit | Why it's separate |
|---|----------------|-------------------|
| 1 | **Patient Scheduling** | Very high availability (24/7), high scalability (500 nurses, shift peaks) — cannot be dragged down by billing outages or reporting batch loads |
| 2 | **Billing Integration** | Very high reliability + security (HIPAA/financial) — needs its own isolated data store, audit trail, and compliance boundary. Cannot share fate with patient portal traffic spikes |
| 3 | **Patient Portal** | Very high performance + elasticity (patient-facing, unpredictable load) — needs independent scaling without being constrained by billing's transactional overhead |
| 4 | **Admin Reporting** | Low everything — weekly batch. Should NOT be sized, secured, or made highly available like the others. Separate deployment avoids wasting resources and avoids batch jobs competing for resources with real-time services |

Connect them via asynchronous event-driven communication (message queue or event bus). Each quantum owns its database. No shared databases.

## Warnings

- **Shared database anti-pattern:** If anyone proposes "4 services but one shared PostgreSQL," you still have 1 quantum with 4 binaries — all the operational complexity of distribution with none of the benefits. Each quantum MUST own its data store.
- **Over-decomposition risk:** The CTO's "microservices for everything" instinct could lead to splitting Scheduling into "appointment-service," "nurse-availability-service," "time-slot-service," etc. Unless those sub-components have different architecture characteristics (they don't), this adds network hops, partial failure modes, and distributed transaction complexity for zero benefit.
- **HIPAA boundary enforcement:** Billing's data isolation is not just an architecture preference — it is a compliance requirement. The quantum boundary here aligns with a regulatory boundary, which reinforces the separation.
- **Admin Reporting could be even simpler:** Consider serverless/scheduled execution (e.g., AWS Lambda + CloudWatch Events) rather than a persistent service. It only runs weekly — no need for always-on infrastructure.
