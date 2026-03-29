# Quantum Analysis: Internal Project Management Tool (Django Monolith)

## System Overview

A Django monolith serving as an internal project management tool for a single office. 3 developers, ~50 users. Features: task tracking, time logging, simple reporting. Deployed on one server with one PostgreSQL database.

---

## Step 1: Components Identified

No codebase was provided, so components are derived from the user's system description.

| Component | Responsibility | Deployment unit |
|-----------|---------------|----------------|
| Task Tracking | Create, assign, update, and manage tasks | Django monolith (single server) |
| Time Logging | Record time entries against tasks | Django monolith (single server) |
| Reporting | Generate simple reports from task/time data | Django monolith (single server) |
| User/Auth | Authentication, user profiles, permissions | Django monolith (single server) |
| PostgreSQL DB | Single shared database for all data | Same server |

All components are Django apps (or modules) within a single Django project, deployed as one unit on one server.

---

## Step 2: Communication Map

| From | To | Type | Mechanism | Fate-sharing? |
|------|-----|------|-----------|:---:|
| Task Tracking | PostgreSQL DB | Sync | Django ORM (direct DB read/write) | Yes |
| Time Logging | PostgreSQL DB | Sync | Django ORM (direct DB read/write) | Yes |
| Time Logging | Task Tracking | Sync | Django ORM foreign keys / direct model imports | Yes |
| Reporting | PostgreSQL DB | Sync | Django ORM queries (read-only) | Yes |
| Reporting | Task Tracking | Sync | Django ORM queries across models | Yes |
| Reporting | Time Logging | Sync | Django ORM queries across models | Yes |
| User/Auth | PostgreSQL DB | Sync | Django ORM (direct DB read/write) | Yes |
| All components | User/Auth | Sync | Django middleware / decorators | Yes |

**Key observation:** Every single communication path is synchronous. All components talk through the Django ORM to the same PostgreSQL database. There are no message queues, no HTTP calls between services, no async event buses. This is textbook synchronous connascence — all components share fate.

The shared database is the strongest coupling signal. Per the quantum rule: "A shared database means shared deployment. You cannot independently deploy services that share a database without risk of schema conflicts."

---

## Step 3: Architecture Characteristics Per Component

Since this is a small internal tool (50 users, single office), the characteristics are straightforward. The critical question from the skill: *"Does the task tracking part need the same scalability/reliability/performance as the reporting part?"*

| Characteristic | Task Tracking | Time Logging | Reporting | User/Auth | Uniform? |
|---------------|:---:|:---:|:---:|:---:|:---:|
| **Scalability** | Low (50 users) | Low (50 users) | Low (50 users) | Low (50 users) | **Yes** |
| **Availability** | Moderate (business hours only, single office) | Moderate | Moderate | Moderate | **Yes** |
| **Performance** | Low-Moderate (simple CRUD) | Low-Moderate (simple CRUD) | Low-Moderate (simple queries) | Low (login/auth) | **Yes** |
| **Reliability** | Moderate (internal tool, not revenue-critical) | Moderate | Moderate | Moderate | **Yes** |
| **Security** | Low-Moderate (internal network only) | Low-Moderate | Low-Moderate | Low-Moderate | **Yes** |
| **Simplicity** | High (3-dev team) | High | High | High | **Yes** |
| **Deployability** | Simple (one server) | Simple | Simple | Simple | **Yes** |

**Every characteristic is uniform across all components.** No component has a meaningfully different quality attribute need from any other. This is exactly what the skill warns about checking: "If everything needs the same scalability, reliability, and performance — it's one quantum, and a monolith is fine."

With 50 users in one office, there are no burst traffic patterns, no components that need independent scaling, no parts requiring different SLAs. The dominant architecture characteristic for this system is **simplicity** — and all components share that need equally.

---

## Step 4: Quantum Grouping

Applying the three-criteria test to group components into quanta:

1. **Deploy together?** Yes — all components are Django apps in one project, deployed as one artifact to one server.
2. **High functional cohesion?** Yes — all components serve the unified purpose of "internal project management."
3. **Synchronous connascence?** Yes — all communication is synchronous via Django ORM and a shared PostgreSQL database.

All three criteria are met for ALL components together.

| Quantum | Components | Driving Characteristics | Communication type |
|---------|-----------|------------------------|:---:|
| **Quantum 1 (the only one)** | Task Tracking, Time Logging, Reporting, User/Auth, PostgreSQL DB | Simplicity, Moderate Availability, Low-Moderate Performance | Internal: all synchronous (ORM + shared DB) |

**This system is a single architecture quantum.**

---

## Step 5: Quantum Characteristic Analysis

With only one quantum, there is nothing to compare. The single quantum has these driving characteristics (top 3):

| # | Characteristic | Level | Rationale |
|---|---------------|-------|-----------|
| 1 | **Simplicity** | High | 3-developer team, internal tool — simplicity is the dominant driver. Complexity has direct cost with a small team. |
| 2 | **Availability** | Moderate | Needs to be up during business hours. Not mission-critical (if it's down for 30 min, people use sticky notes). |
| 3 | **Deployability** | Simple | Single server, single artifact. No need for complex deployment orchestration. |

There are **no characteristic differences** between components because there is only one quantum.

---

## Step 6: Architecture Direction

**Quantum count:** 1

**Characteristic uniformity:** Uniform (all components need the same characteristics)

**Recommendation: Monolith**

**Reasoning:**

The quantum analysis conclusively shows this system is a single architecture quantum. Here's why:

1. **Single quantum = monolith.** With one quantum, there is no architectural justification for distribution. The entire system has one set of quality attribute needs, and a monolith can optimize for all of them simultaneously.

2. **Shared database = shared quantum.** Even if you split the Django apps into separate services, they would all still need the same PostgreSQL database. Per the quantum rule, services sharing a database are in the same quantum regardless. You'd have the complexity of distributed architecture (network calls, service discovery, deployment orchestration) with none of the benefits (independent scaling, independent deployment, independent characteristics).

3. **Uniform characteristics = no reason to distribute.** The ONLY valid reason to accept distributed architecture complexity is that different parts of the system need genuinely different quality attributes. Your task tracking, time logging, and reporting all need the same low-moderate characteristics. There is nothing to optimize differently.

4. **Team size makes distribution actively harmful.** With 3 developers, the operational overhead of microservices (service mesh, distributed tracing, container orchestration, inter-service communication, network failure handling, distributed transactions, deployment pipelines per service) would consume more engineering effort than the application logic itself. A 3-person team maintaining multiple services is a well-documented anti-pattern.

5. **Scale doesn't justify it.** 50 users in one office is orders of magnitude below the threshold where a Django monolith would face scaling issues. Django can handle thousands of concurrent users on a single server with proper configuration.

---

## Characteristic Comparison

| Characteristic | Quantum 1 (entire system) | Uniform? |
|---------------|:---:|:---:|
| Scalability | Low | N/A (single quantum) |
| Availability | Moderate | N/A (single quantum) |
| Performance | Low-Moderate | N/A (single quantum) |
| Simplicity | High | N/A (single quantum) |
| Deployability | Simple | N/A (single quantum) |

---

## Warnings

- **Microservices enthusiasm without quantum justification detected.** The tech lead's desire to split into microservices is not supported by quantum analysis. Microservices solve the problem of *multiple quanta with different characteristics* — this system has one quantum with uniform characteristics. Introducing microservices here would add complexity without corresponding benefit.

- **Premature distribution anti-pattern.** Splitting a single-quantum system into services creates "distributed monolith" — you get all the operational complexity of distributed systems (network latency, partial failures, data consistency challenges) while still having all the coupling of a monolith (shared database, synchronous communication, lockstep deployment). This is strictly worse than a well-structured monolith.

- **Conway's Law consideration.** With 3 developers in one office, the team structure already matches a monolith. Microservices work best when independent teams own independent services. Splitting services across a 3-person team means everyone works on everything anyway, but with more infrastructure overhead.

---

## Recommendation Summary

**Keep the monolith.** Your instinct is correct — splitting this system into microservices is overkill.

The quantum analysis provides objective backing for this position: you have one quantum, uniform characteristics, a shared database, 50 users, and 3 developers. None of the conditions that justify distributed architecture are present.

If the tech lead is concerned about code quality, the right approach is a **well-structured modular monolith** — clean separation between Django apps (task tracking, time logging, reporting) with well-defined interfaces, but deployed as one unit. This gives you the organizational benefits of service thinking without the operational cost of actual distribution.

**Revisit this analysis when/if:**
- User count grows to thousands with different usage patterns (e.g., reporting becomes CPU-heavy at month-end while task tracking needs to stay snappy)
- Different components need different scaling (e.g., you add a real-time notification system)
- The team grows large enough that independent deployment becomes valuable (typically 15+ developers)
- Different components need different technology stacks
