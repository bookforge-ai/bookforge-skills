# Architecture Quantum Analysis: Django Internal Project Management Tool

## Context

- **System:** Django monolith for internal project management
- **Team:** 3 developers
- **Users:** ~50, all co-located in one office
- **Features:** Task tracking, time logging, simple reporting
- **Infrastructure:** Single server, single PostgreSQL database
- **Proposal under evaluation:** Tech lead wants to split into microservices

---

## What Is an Architecture Quantum?

An architecture quantum is the smallest independently deployable unit of a system that includes all the structural elements required for it to function correctly. It encompasses:

1. **Independently deployable component(s)** — the code that runs
2. **Data store(s)** — the database(s) it depends on
3. **Synchronous connascence** — any runtime coupling to other components needed to fulfill a request

If two parts of a system *must* be deployed together to work, they belong to the same quantum. If they share a database, they are likely in the same quantum. If one makes a synchronous call to another to complete a user request, they are coupled at the quantum level.

---

## Quantum Analysis of Your System

### How Many Quanta Do You Have?

**One. You have a single architecture quantum.**

Here is the breakdown:

| Quantum Element | Your System |
|----------------|-------------|
| Deployable unit | 1 Django application |
| Database | 1 PostgreSQL instance |
| Synchronous dependencies | None external — all features share the same process |
| Independent deployment possible? | No — all features deploy together |
| Independent data ownership? | No — one shared schema, likely with foreign keys across feature areas |

Your task tracking, time logging, and reporting features all:
- Live in the same Django project (likely as apps within one project)
- Share the same database with cross-table relationships
- Deploy as a single unit
- Scale as a single unit

**This is a textbook single-quantum architecture.**

---

## Should You Split Into Microservices?

### The Quantum Perspective Says No

Microservices are justified when you have (or need) **multiple independent quanta** — meaning parts of your system that:

- Need to deploy on different schedules
- Need to scale independently
- Are owned by different teams with different release cadences
- Have genuinely separate data domains with no shared transactions

Let's evaluate your situation against these drivers:

| Driver | Your Reality | Microservices Justified? |
|--------|-------------|------------------------|
| Independent deployment | 3 devs, one team, one release cycle | No |
| Independent scaling | ~50 users on one server — no scaling pressure | No |
| Team autonomy | 3 developers — not enough for even 2 autonomous teams | No |
| Data separation | Tasks, time logs, and reports are tightly coupled (reports query tasks + time logs) | No |
| Technology diversity | No stated need for different tech stacks per feature | No |
| Fault isolation | Single office, single server — if the network is down, everything is down regardless | No |

### What Microservices Would Actually Cost You

Splitting a single quantum into multiple services when the underlying coupling hasn't changed creates **distributed monolith** problems:

1. **Operational overhead:** You now need service discovery, inter-service communication (REST/gRPC/message queues), distributed tracing, health checks, and deployment orchestration for each service. With 3 developers, this infrastructure burden is severe.

2. **Data consistency pain:** Your reporting feature almost certainly joins tasks and time logs. Split them into separate services with separate databases and you must either:
   - Duplicate data across services (eventual consistency, sync logic)
   - Make synchronous cross-service calls (latency, failure modes, distributed transactions)
   - Both options are dramatically more complex than a SQL JOIN

3. **Development velocity drop:** Instead of a simple Django ORM query across related models, developers now write API contracts, handle network failures, manage versioning, and debug across service boundaries. For 3 people, this is crippling.

4. **Testing complexity:** Integration testing across services requires running multiple processes, managing test data across databases, and dealing with timing issues. Currently you just run `python manage.py test`.

5. **Deployment complexity:** One `git push` and a server restart becomes orchestrating multiple deployments with version compatibility checks.

---

## What You Should Do Instead

### Keep the Monolith, But Keep It Clean

Your single-quantum Django monolith is the **correct architecture** for your scale and constraints. Focus on internal quality:

1. **Well-structured Django apps:** Keep `tasks/`, `timelog/`, `reporting/` as separate Django apps with clear boundaries. This gives you logical separation without operational overhead.

2. **Clean interfaces between apps:** Have apps communicate through well-defined service layers or model managers rather than reaching directly into each other's internals. If you ever *do* need to extract a service, this makes it possible.

3. **Database-level separation where sensible:** Use Django's database routing if you want read replicas for reporting, but this is optional at your scale.

4. **Simple deployment:** A single server with PostgreSQL for 50 co-located users is perfectly appropriate. Add basic monitoring (Sentry, simple health checks) and automated backups.

### When to Revisit

Consider splitting only if:
- Your user base grows by 10-100x and specific features have different scaling needs
- Your team grows to 8+ developers and coordination costs increase
- A specific feature genuinely needs different technology (e.g., a real-time component)
- Deployment coupling causes actual problems (it almost certainly doesn't today)

---

## Summary

| Aspect | Assessment |
|--------|-----------|
| Number of architecture quanta | 1 |
| Recommended architecture | Monolith (Django) |
| Microservices recommendation | Not warranted — would increase complexity without benefit |
| Key risk of splitting | Distributed monolith — paying the cost of distribution without gaining independence |
| Key action | Maintain clean internal modularity within the Django project |

**Bottom line:** Your instinct is correct. A well-structured Django monolith is the right architecture for a 3-developer, 50-user, single-office internal tool. Your tech lead's interest in microservices is understandable — they are a popular topic — but applying them here would trade simplicity for complexity with no corresponding benefit. You have one quantum, and one quantum is all you need.
