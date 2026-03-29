# Architecture Trade-Off Analysis: Healthcare Appointment Scheduling SaaS

**Date:** 2026-03-25
**Prepared for:** Engineering & Compliance Team
**Context:** Greenfield SaaS product for healthcare appointment scheduling, 3-person dev team, HIPAA compliance required

---

## 1. Executive Summary

This report evaluates two architecture options — microservices and monolith — for a healthcare appointment scheduling SaaS. After analyzing team capacity, compliance requirements, operational complexity, and time-to-market, **the recommendation is to start with a modular monolith** with clear internal boundaries, designed so individual modules can be extracted into services later if and when the need arises.

Neither the CTO nor the lead developer is entirely wrong. The CTO is right that service boundaries matter; the lead dev is right that microservices will overwhelm a 3-person team. The modular monolith gives you both: clean separation without operational explosion.

---

## 2. The Three Positions

| Stakeholder | Position | Underlying Concern |
|---|---|---|
| **CTO** | Microservices | Scalability, modern best practices, independent deployability |
| **Lead Dev** | Simple monolith | Team size, development speed, operational simplicity |
| **Compliance Officer** | HIPAA compliance | PHI protection, audit trails, access controls, breach notification |

---

## 3. Option A: Microservices Architecture

### Proposed Service Decomposition
- Appointment Service
- Patient Service (handles PHI)
- Provider/Schedule Service
- Notification Service
- Auth/Identity Service
- Audit/Logging Service

### Advantages
- Independent scaling of high-traffic services (e.g., appointment search)
- Isolated deployment — one service can be updated without redeploying everything
- Technology flexibility per service
- Fault isolation — one failing service does not necessarily bring down others
- PHI can be isolated in a dedicated service with stricter access controls

### Disadvantages
- **Operational overhead is extreme for 3 developers.** Each service needs its own CI/CD pipeline, monitoring, logging, health checks, and deployment configuration. With 6+ services, you are looking at 6+ deployment targets, service meshes or API gateways, distributed tracing, and container orchestration (Kubernetes or equivalent).
- **Distributed transactions.** Booking an appointment touches patients, providers, schedules, and notifications. Without a saga pattern or similar coordination, you risk data inconsistency. Implementing sagas correctly is non-trivial.
- **Network latency and failure modes.** Every inter-service call is a potential point of failure. Circuit breakers, retries, and timeouts must be implemented and tested.
- **HIPAA complexity multiplies.** Every service that touches PHI needs its own encryption-at-rest, encryption-in-transit, access logging, and BAA coverage. More services = more attack surface = more audit scope.
- **Debugging is significantly harder.** A single request may traverse 3-4 services. Correlating logs across services requires distributed tracing infrastructure (Jaeger, Zipkin, or equivalent).
- **Development velocity will be slow initially.** Service contracts (API schemas), versioning, and integration testing take time that a 3-person team cannot afford in early stages.

### Estimated Additional Infrastructure
- Container orchestration (ECS, EKS, or similar)
- Service mesh or API gateway
- Distributed tracing
- Centralized logging aggregation
- Service discovery
- Secret management per service
- Per-service CI/CD pipelines

### Realistic Timeline Impact
Expect 2-4 months of additional infrastructure work before shipping the first feature, compared to a monolith.

---

## 4. Option B: Simple Monolith

### Structure
Single deployable application handling all domains (appointments, patients, providers, notifications, auth, audit).

### Advantages
- **Fast to build.** One codebase, one deployment, one database. A 3-person team can ship features in weeks, not months.
- **Simple debugging.** Stack traces are local. No distributed tracing needed.
- **Simple transactions.** Database transactions cover multi-table operations naturally.
- **One deployment pipeline.** One CI/CD config, one monitoring dashboard, one log stream.
- **HIPAA compliance is easier to implement and audit** in a single application boundary.

### Disadvantages
- **Risk of becoming a "big ball of mud."** Without discipline, module boundaries blur and the codebase becomes tangled over time.
- **Scaling is all-or-nothing.** You cannot scale the appointment search independently from the notification sender.
- **Deployment coupling.** A bug in the notification module means redeploying everything, including the booking flow.
- **Single point of failure.** If the process crashes, everything is down.
- **Perceived as "not modern"** — this is a political risk, not a technical one, but it is real.

---

## 5. Option C (Recommended): Modular Monolith

### What It Is
A single deployable application with strictly enforced internal module boundaries. Each module owns its domain (Appointments, Patients, Providers, Notifications, Auth, Audit) and communicates with other modules through well-defined internal interfaces — not direct database table access across modules.

### Structure
```
src/
  modules/
    appointments/       # Booking, cancellation, rescheduling
      api/              # Public interface for other modules
      internal/         # Private implementation
      models/           # Domain models
      repository/       # Data access (owns its tables)
    patients/           # Patient records, PHI
      api/
      internal/
      models/
      repository/
    providers/          # Provider schedules, availability
    notifications/      # Email, SMS, push
    auth/               # Authentication, authorization, RBAC
    audit/              # Immutable audit trail
  shared/
    hipaa/              # Cross-cutting HIPAA utilities
    encryption/         # PHI encryption helpers
```

### Key Design Rules
1. **Modules communicate only through their public `api/` layer.** No module directly queries another module's database tables.
2. **Each module owns its tables.** The `patients` module owns `patients`, `patient_contacts`, etc. The `appointments` module references patients by ID only.
3. **PHI access is gated.** The `patients` module exposes minimal PHI through its API. Other modules get only what they need (e.g., patient name for a notification, not the full record).
4. **Internal event bus (in-process).** Modules publish events (e.g., `AppointmentBooked`) that other modules can subscribe to, enabling loose coupling without network overhead.

### Why This Works

| Concern | How the Modular Monolith Addresses It |
|---|---|
| CTO's scalability concern | Module boundaries are designed as future service boundaries. Extraction to microservices is a known, documented path. |
| Lead dev's simplicity concern | One deployment, one database, one CI/CD pipeline. Local debugging. Simple transactions. |
| HIPAA compliance | Single application boundary simplifies encryption, access controls, audit logging, and BAA scope. PHI is isolated in the patients module with strict access rules. |
| Future growth | When you hit 10-15 developers or genuine scaling bottlenecks, you extract the relevant module into a service. The interfaces are already defined. |

---

## 6. HIPAA Compliance: Architecture-Independent Requirements

Regardless of which architecture you choose, these are non-negotiable:

### Technical Safeguards
- **Encryption at rest:** AES-256 for all PHI storage (database, backups, file storage)
- **Encryption in transit:** TLS 1.2+ for all connections (API, database, internal)
- **Access controls:** Role-based access control (RBAC). Minimum necessary access principle. No developer access to production PHI without audit trail.
- **Audit logging:** Immutable, tamper-evident logs of all PHI access (who accessed what, when, from where). Retain for minimum 6 years.
- **Automatic session timeout:** Configurable idle timeout for all user sessions
- **Unique user identification:** Every user action must be traceable to a specific individual

### Administrative Requirements
- **Business Associate Agreements (BAAs):** Required with every vendor that touches PHI — cloud provider (AWS/GCP/Azure all offer BAAs), email service, SMS provider, monitoring tools, etc.
- **Risk assessment:** Document threats and mitigations before launch
- **Incident response plan:** Documented procedure for breach detection, containment, notification (72-hour rule to HHS for breaches affecting 500+ individuals)
- **Workforce training:** All team members must complete HIPAA training

### Architecture Impact on HIPAA
| Aspect | Microservices Impact | Monolith/Modular Monolith Impact |
|---|---|---|
| BAA scope | BAA needed for every infrastructure component per service | Single deployment = fewer infrastructure components |
| Audit trail | Must correlate across services (distributed tracing) | Single log stream, straightforward |
| Access control | Per-service auth or centralized auth gateway | Single RBAC implementation |
| Encryption | Must configure per-service | Single configuration |
| Penetration testing | Larger attack surface (more network endpoints) | Smaller attack surface |
| Compliance audit | Auditor must review each service independently | Single application review |

**Bottom line:** Microservices roughly multiply your HIPAA compliance effort by the number of services that handle PHI.

---

## 7. Decision Matrix

Scoring: 1 (worst) to 5 (best) for a 3-person team building a healthcare SaaS.

| Criterion | Weight | Microservices | Simple Monolith | Modular Monolith |
|---|---|---|---|---|
| Time to first feature | 20% | 2 | 5 | 4 |
| HIPAA compliance ease | 25% | 2 | 4 | 4 |
| Team capacity fit (3 devs) | 20% | 1 | 5 | 4 |
| Scalability runway | 10% | 5 | 2 | 3 |
| Operational simplicity | 15% | 1 | 5 | 4 |
| Future extractability | 10% | 5 | 1 | 4 |
| **Weighted Total** | **100%** | **2.15** | **3.90** | **3.85** |

The simple monolith and modular monolith score similarly, but the modular monolith provides a significantly better path forward when the team and product grow. The small upfront cost of enforcing module boundaries pays for itself within months.

---

## 8. Migration Path: Modular Monolith to Microservices

When (and only when) you experience concrete scaling problems or team growth beyond 8-10 developers:

1. **Identify the bottleneck module.** Typically the one with the highest load or the one blocking other teams.
2. **Extract its database tables** into a separate database (this is the hardest step — do it first).
3. **Replace in-process API calls** with HTTP/gRPC calls to the new service.
4. **Replace in-process events** with a message broker (SQS, RabbitMQ, Kafka).
5. **Deploy independently.** Set up CI/CD, monitoring, and health checks for the new service.
6. **Repeat** for the next bottleneck module.

This is a gradual, low-risk process because the module boundaries already exist.

---

## 9. Addressing the "Netflix Argument"

Netflix moved to microservices because they had:
- Hundreds of millions of users with extreme traffic variation
- Hundreds of engineering teams that needed to deploy independently
- A monolith that was a deployment bottleneck for 1,000+ engineers

Your situation:
- Zero users (pre-launch)
- 3 developers
- No deployment bottleneck (because nothing is deployed yet)

**Netflix's architecture solves Netflix's problems.** Adopting it before you have those problems means paying the operational tax without receiving the benefits. Many successful companies (Shopify, Stack Overflow, Basecamp) run modular monoliths at significant scale.

The honest question is not "what does Netflix use?" but "what will let 3 developers ship a HIPAA-compliant product fastest while keeping the door open for future growth?"

---

## 10. Recommended Next Steps

1. **Agree on the modular monolith approach** as the starting architecture.
2. **Define module boundaries** based on the domain model (Appointments, Patients, Providers, Notifications, Auth, Audit).
3. **Establish the inter-module communication contract** (internal API interfaces and event types) before writing feature code.
4. **Set up HIPAA infrastructure first:** encryption layer, audit logging, RBAC framework, BAA with cloud provider.
5. **Document the "extraction criteria"** — specific, measurable conditions under which a module should become a service (e.g., "when appointment search needs to handle >1,000 queries/sec independently" or "when the team exceeds 8 developers").
6. **Revisit this decision in 12 months** or when you hit a documented extraction criterion.

---

## 11. Risks of This Recommendation

| Risk | Mitigation |
|---|---|
| Developers don't enforce module boundaries | Enforce via linting rules, architecture tests (e.g., ArchUnit), and code review. Fail CI if a module imports another module's internals. |
| CTO feels the architecture is "not ambitious enough" | Present the extraction path. This is not "we'll never do microservices" — it is "we'll do microservices when we have evidence we need them." |
| Scaling bottleneck hits before extraction is ready | The modular structure makes emergency extraction feasible in 2-4 weeks for a single module. Without modules, extraction from a tangled monolith takes months. |
| HIPAA audit finds gaps | Start the compliance checklist in week 1, not after features are built. Audit logging and encryption are module-zero. |

---

*This analysis prioritizes shipping a compliant product with a 3-person team. The architecture can evolve as the team and product grow. Premature optimization of architecture is as dangerous as premature optimization of code.*
