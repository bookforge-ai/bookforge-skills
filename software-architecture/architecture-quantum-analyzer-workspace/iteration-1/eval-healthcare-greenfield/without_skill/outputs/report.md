# Healthcare Platform Architecture Analysis

## The Question

Should we use microservices for all four features (patient scheduling, billing integration, patient portal, admin reporting)? How many deployment units do we actually need?

## Short Answer

No. Microservices for everything is overkill here. You likely need **2-3 deployment units**, not 4+ microservices.

---

## Analysis of Each Feature

### 1. Patient Scheduling
- **Users:** 500 nurses, 24/7
- **Key requirement:** High availability
- **Traffic pattern:** Steady, constant load
- **Notes:** This is mission-critical. Downtime means nurses can't schedule patients. Needs independent scaling and deployment so that changes to other features don't bring it down.

### 2. Billing Integration
- **Key requirement:** Reliability, security, HIPAA compliance
- **Traffic pattern:** Batch-like (claim submissions), not real-time spikes
- **Notes:** HIPAA means this component needs strict access controls, audit logging, encryption at rest and in transit. It benefits from isolation — not because of scale, but because of **compliance boundaries**. A security audit of billing shouldn't require auditing the entire system.

### 3. Patient Portal
- **Key requirement:** Performance (patients checking test results)
- **Traffic pattern:** Spiky (results released in batches, patients rush to check)
- **Notes:** Read-heavy. Can be optimized with caching. Shares data with scheduling (appointments) and billing (statements). Doesn't necessarily need its own deployment unit if co-located thoughtfully.

### 4. Admin Reporting
- **Key requirement:** None critical — low traffic, weekly batch
- **Traffic pattern:** Periodic, low volume
- **Notes:** This is the clearest case against a dedicated microservice. A weekly batch job does not justify the operational overhead of its own service, CI/CD pipeline, monitoring, on-call rotation, etc.

---

## Recommended Architecture: 2-3 Deployment Units

### Option A: 2 Units (Pragmatic Start)

| Unit | Contains | Rationale |
|------|----------|-----------|
| **Core Clinical Service** | Patient Scheduling + Patient Portal + Admin Reporting | These share patient data, have overlapping domain models, and the portal/reporting don't justify separate deployment overhead. Scheduling drives the availability requirement for this unit. |
| **Billing Service** | Billing Integration | Isolated for HIPAA compliance boundary. Different security posture, audit requirements, and likely different team handling PCI/insurance integrations. |

Admin reporting runs as a scheduled job within the core service — it reads from the same database and produces reports. No need for a separate service.

### Option B: 3 Units (If Growth Is Expected)

| Unit | Contains | Rationale |
|------|----------|-----------|
| **Scheduling Service** | Patient Scheduling | Separated for independent availability and scaling. If scheduling needs 99.99% uptime while the portal can tolerate 99.9%, this separation makes sense. |
| **Patient Experience Service** | Patient Portal + Admin Reporting | Portal is the main component. Reporting is a background job here. |
| **Billing Service** | Billing Integration | Same HIPAA compliance reasoning as above. |

---

## Why Not 4 Microservices?

The CTO's instinct ("microservices for everything") carries real costs:

1. **Operational overhead:** Each service needs its own CI/CD pipeline, monitoring, alerting, log aggregation, health checks, and on-call rotation. With a team that supports 500 nurses, you're probably not Google-sized. Every additional service multiplies ops burden.

2. **Data consistency complexity:** Scheduling, portal, and reporting all operate on patient data. Splitting them into separate services means you need either:
   - A shared database (which defeats much of the microservice benefit), or
   - Event-driven synchronization (which adds eventual consistency problems — a nurse schedules an appointment but the portal doesn't show it for 30 seconds)

3. **Network latency and failure modes:** Every service-to-service call is a network call that can fail, timeout, or slow down. A monolithic or modular approach for tightly coupled features avoids this entirely.

4. **Admin reporting as a microservice is waste:** A weekly batch report does not need its own deployment unit, container orchestration, service mesh entry, API gateway route, etc. It's a cron job.

5. **Team size matters:** Microservices work best when you have independent teams that can own and deploy services independently. If you have 1-2 teams, multiple microservices just mean one team context-switching across many repos and pipelines.

---

## What Actually Matters More Than Service Count

### Modularity Within Each Unit
Even with 2-3 deployment units, you should maintain **clean module boundaries** inside each service:
- Separate packages/modules for scheduling, portal, reporting logic
- Well-defined internal interfaces between modules
- This lets you extract a module into its own service later IF you hit a specific scaling or organizational bottleneck

### HIPAA Compliance Architecture (Applies to ALL Units, Not Just Billing)
Since this is healthcare:
- All units handling PHI (Protected Health Information) need encryption at rest and in transit
- Audit logging everywhere
- Role-based access control
- The billing service has the strictest requirements, but the patient portal also handles PHI (test results)

### Availability Strategy for Scheduling
- Multiple instances behind a load balancer
- Database replication (read replicas for the portal)
- Circuit breakers if calling external systems
- This is achievable without microservices — it's an infrastructure concern, not an architecture style concern

---

## Decision Framework: When to Split a Service Out

Don't split preemptively. Split when you observe one of these:

| Signal | Example | Action |
|--------|---------|--------|
| Different scaling needs are proven, not theoretical | Portal traffic is 100x scheduling | Split portal out |
| Compliance requires hard isolation | Auditor demands billing runs on dedicated infrastructure | Already separated |
| Independent team owns it | A dedicated billing team wants autonomous deploys | Already separated |
| Different tech stack needed | Reporting needs a data warehouse, not the OLTP database | Extract reporting |
| Deploy frequency mismatch is causing pain | Scheduling deploys daily, portal deploys weekly, and coordinating is slowing everyone down | Split them |

---

## Recommended Starting Point

```
┌─────────────────────────────────────────────┐
│           Core Clinical Service             │
│  ┌──────────────┐  ┌───────────────────┐    │
│  │  Scheduling   │  │  Patient Portal   │    │
│  │  Module       │  │  Module           │    │
│  └──────────────┘  └───────────────────┘    │
│  ┌──────────────┐                           │
│  │  Reporting    │  (scheduled job)         │
│  │  Module       │                           │
│  └──────────────┘                           │
│                                              │
│  Shared: Patient DB, Auth, Audit Logging     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│           Billing Service                    │
│  ┌──────────────────────────────────────┐    │
│  │  Claims Processing                    │    │
│  │  Insurance Integration                │    │
│  │  Payment Records                      │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  Isolated: Own DB, Enhanced Encryption,      │
│  Dedicated Audit Trail, HIPAA Hardened       │
└─────────────────────────────────────────────┘

Communication: Async events (patient admitted → billing notified)
```

---

## Summary

| Aspect | Recommendation |
|--------|---------------|
| **Number of deployment units** | Start with 2, grow to 3 if needed |
| **Billing** | Always separate (compliance boundary) |
| **Scheduling + Portal** | Co-deploy initially, split when scaling data proves it necessary |
| **Admin Reporting** | Scheduled job inside the core service, never its own microservice |
| **Microservices for everything?** | No. The costs outweigh the benefits at this scale and team size. Use a well-modularized approach and split only when pain is real. |

The best architecture is the one your team can actually operate. Two well-run services beat four poorly-monitored ones every time.
