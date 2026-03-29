# Architecture Characteristics for Hospital Employee Scheduling Tool

## Context Summary

- **Team size:** 3 developers
- **Scope:** Internal scheduling tool for one mid-size hospital (500 nurses, 200 doctors)
- **Core features:** Shift swapping, PTO tracking, labor law compliance (rest periods, max hours)
- **Stakeholder tension:** IT director wants "enterprise-grade and scalable" for potential 12-hospital expansion; immediate need is just one working hospital
- **Budget:** Tight

---

## Recommended Architecture Characteristics (Prioritized)

### 1. Correctness / Data Integrity (Top Priority)

This is a healthcare scheduling system where mistakes have real consequences. If the system allows a nurse to be double-booked, or permits a shift assignment that violates mandatory rest periods, you're looking at labor law violations, patient safety risks, and potential legal liability. The scheduling rules — max consecutive hours, minimum rest between shifts, overtime caps — must be enforced consistently and without exception. This is the one thing the system absolutely cannot get wrong.

**What this means practically:**
- Strong validation layer that checks every schedule change against labor law constraints before committing it
- Transactional consistency — a shift swap must either fully complete or fully roll back
- Solid test coverage on the compliance rule engine

### 2. Reliability / Availability

Nurses and doctors need to check and swap shifts around the clock. A hospital runs 24/7 and scheduling decisions happen at all hours. If the system goes down during a shift change window, you get chaos — people showing up to shifts that were supposed to be swapped, gaps in coverage. It doesn't need five-nines uptime, but it needs to be dependably available during normal use and degrade gracefully if something goes wrong.

**What this means practically:**
- Straightforward deployment on reliable infrastructure (a managed database, a well-monitored app server)
- Basic health checks and alerting so someone knows when something breaks
- Reasonable error handling — don't lose data if a request fails mid-process

### 3. Usability / Accessibility

Your users are nurses and doctors, not software engineers. They're checking schedules on their phones between patients. The interface needs to be dead simple. If adoption is poor because the tool is confusing, the whole project fails regardless of how elegant the backend is. With 700 users, even a small usability problem becomes a big support burden for a 3-person team.

**What this means practically:**
- Mobile-friendly (probably mobile-first) design
- Minimal clicks to perform common actions (view my schedule, request a swap, submit PTO)
- Clear feedback when compliance rules block an action ("This swap would violate the 11-hour rest requirement between shifts")

### 4. Security

You're dealing with employee personal information, work schedules, and PTO balances inside a hospital environment. Healthcare organizations face regulatory scrutiny (even for non-clinical systems, because they sit on the same network and involve employee PII). Role-based access matters — a nurse shouldn't be able to edit a doctor's schedule or approve their own PTO.

**What this means practically:**
- Authentication tied to the hospital's existing identity system (Active Directory / SSO)
- Role-based access control (nurse, charge nurse, department manager, HR admin)
- Audit logging for compliance-sensitive actions (who approved what, when)
- Standard security hygiene (encryption in transit, parameterized queries, etc.)

### 5. Maintainability

With only 3 developers and a tight budget, you cannot afford a system that's painful to change. Labor laws vary by jurisdiction and change over time. Hospital policies evolve. New shift patterns get introduced. The compliance rules engine will need frequent updates, and those updates need to be safe and easy to make. A tangled codebase will grind your small team to a halt.

**What this means practically:**
- Clean separation between scheduling logic, compliance rules, and presentation
- Compliance rules should be configurable or at least isolated in a module that's easy to update without touching the rest of the system
- Good test coverage so changes can be made with confidence
- Simple, well-understood tech stack — nothing exotic

### 6. Performance (Adequate, Not Extreme)

700 users is not a high-scale problem. Even if everyone checks their schedule at shift change, you're looking at maybe a few hundred concurrent requests at peak. The system needs to feel responsive — schedule views load fast, shift swaps confirm quickly — but you don't need distributed caching or microservices. A well-built monolith with a properly indexed database will handle this comfortably.

**What this means practically:**
- Response times under 1-2 seconds for common operations
- Database queries optimized with appropriate indexes on schedule lookups
- Don't over-engineer — a single application server with a PostgreSQL database is probably sufficient

---

## Characteristics to Deliberately Deprioritize

### Scalability (For Now)

The IT director's concern about expanding to 12 hospitals is valid as a future consideration but dangerous as a current design driver. Building for 12 hospitals when you have 3 developers and a tight budget is a recipe for never shipping anything. 700 users at one hospital and 8,400 users across 12 hospitals are different problems, but not as different as people think — a well-built monolith can often handle both.

**The pragmatic approach:** Build a clean, well-structured system for one hospital. Use configuration (not hard-coding) for hospital-specific rules. If expansion happens, you'll likely need multi-tenancy, which is easier to add to a clean codebase than to a prematurely distributed one. The "scalability" that matters now is *code-level modularity*, not infrastructure-level horizontal scaling.

### Elasticity

You don't have unpredictable traffic spikes. Hospital scheduling is predictable — peak usage is at shift changes, and the load is modest. Don't spend money or complexity on auto-scaling infrastructure.

### Fault Tolerance / High Availability

A few minutes of downtime won't endanger patients (the existing paper/whiteboard process is the fallback). Simple redundancy (database backups, a restart policy) is sufficient. You don't need multi-region failover.

---

## Architecture Recommendation

Given the constraints (3 developers, tight budget, one hospital, compliance-heavy domain):

**Start with a modular monolith.** One deployable unit, but with clear internal boundaries:

- **Scheduling module** — shift assignments, calendar views, swap workflow
- **Compliance engine** — labor law rules, rest period checks, max hours validation (isolated so rules can be updated independently)
- **PTO module** — requests, approvals, balance tracking
- **User/auth module** — SSO integration, roles, permissions
- **Notification module** — shift change alerts, swap requests, PTO approvals

This gives you the maintainability and correctness benefits of good structure without the operational overhead of microservices. A 3-person team running Kubernetes and 8 microservices is a team that never ships features.

**When the 12-hospital conversation becomes real** (budget approved, timeline set, actual requirements gathered), you can extract modules into services where needed. A clean monolith is far easier to decompose later than a premature microservice architecture is to operate today.

---

## Summary Table

| Characteristic | Priority | Rationale |
|---------------|----------|-----------|
| Correctness / Data Integrity | Critical | Labor law violations have legal and safety consequences |
| Reliability | High | 24/7 hospital operations depend on schedule accuracy |
| Usability | High | 700 non-technical users; adoption determines success |
| Security | High | Employee PII, healthcare environment, audit requirements |
| Maintainability | High | 3-person team, evolving compliance rules, tight budget |
| Performance | Moderate | 700 users is manageable; just needs to feel responsive |
| Scalability | Low (for now) | One hospital first; clean code enables future scaling |
| Elasticity | Low | Predictable, modest load |
| Fault Tolerance | Low | Brief downtime is acceptable; manual fallback exists |
