# Architecture Style Selection: FreelanceInvoice SaaS

## Decision Context
**System:** SaaS invoicing tool for freelancers — generates PDF invoices, tracks payments, sends reminders, integrates with Stripe.
**Driving characteristics:** (1) Simplicity, (2) Overall cost, (3) Deployability
**Architecture quanta:** 1 — all components (PDF generation, payment tracking, reminders, Stripe integration) share the same quality attribute needs. No part of the system requires a fundamentally different scalability, availability, or performance profile from the rest.
**Team context:** Solo developer, $50/month hosting budget, 3-month launch timeline, no mention of distributed systems experience.

## Step 1: Monolith vs Distributed

**Decision:** Monolith

**Reasoning:**

The quantum count is unambiguously one. PDF generation, payment tracking, reminders, and Stripe integration are all tightly related features of a single invoicing workflow. They share the same users, the same data (invoices, clients, payments), and the same availability/performance profile. There is no scenario where "payment tracking needs to scale independently from PDF generation" at the scale of a freelancer-focused SaaS.

Beyond the quantum analysis, every organizational factor points away from distribution:

- **Solo developer.** The skill's organizational fit table is explicit: team size <10 means avoid microservices. A team of 1 makes this even more definitive. There is nobody to own separate services, nobody to be on-call for independent deployments, nobody to debug distributed tracing at 2 AM.
- **$50/month budget.** Distributed architectures require multiple running processes, container orchestration, service discovery, and potentially multiple databases. This cannot fit in a $50/month budget. A single monolith on a $5-20/month VPS or PaaS instance leaves room for the database.
- **3-month timeline.** Distributed architecture setup (CI/CD per service, inter-service communication, monitoring) would consume a significant portion of this timeline before any business logic is written.

**To directly answer the question: No, you should not use microservices.** Microservices would be the worst possible choice for this project. It would mean higher cost, slower delivery, more operational burden, and zero architectural benefit — since you have a single quantum with no need for independent scaling or deployment of parts.

## Candidate Evaluation

| Criterion | Layered | Microkernel | Pipeline |
|-----------|:-------:|:-----------:|:--------:|
| Simplicity (priority 1) | 5/5 | 4/5 | 5/5 |
| Overall cost (priority 2) | 5/5 | 5/5 | 5/5 |
| Deployability (priority 3) | 1/5 | 3/5 | 2/5 |
| **Characteristic total** | **11** | **12** | **12** |
| Organizational fit | Good | Good | Poor |
| Domain isomorphism | Yes | No | No |
| Anti-pattern risk | Sinkhole (low risk at this scale) | None | Forced — domain is not linear processing |

**Why Pipeline is eliminated:** An invoicing system is not a linear data transformation pipeline. Users interact with invoices (create, edit, view, pay), which involves CRUD operations, UI interactions, and webhook handling — not unidirectional data flow. Pipeline has no domain isomorphism here.

**Why Microkernel is eliminated:** Microkernel excels when the core problem is customizability and plug-in extensibility (e.g., regional tax rules as plug-ins). This invoicing tool has no plug-in requirement. While microkernel scores well on cost and simplicity, the domain does not naturally map to a core-plus-plugins topology. There is no extensibility axis that would benefit from this pattern.

**Why Layered wins:** The invoicing domain is a straightforward business application — UI, business logic, data access. This maps directly to layered architecture's topology. For a solo developer shipping in 3 months, the simplicity advantage is decisive. The deployability weakness (1/5) is a non-issue at this stage: you are deploying a single artifact, and you are the only person deploying it.

## Data Architecture
**Data location:** Single shared database (PostgreSQL recommended — handles invoices, clients, payments, reminders in one place)
**Communication:** Not applicable (monolith — in-process function calls)
**Consistency model:** ACID — critical for financial data. Invoice creation, payment recording, and balance updates must be transactional. A single database gives you this for free.

## Recommendation

**Selected style: Layered Architecture**

**Why this style:**
- Your invoicing domain is a textbook fit for layered architecture. It is a business application with standard CRUD operations, form-based interactions, and integration with an external payment API. The domain/architecture isomorphism is strong.
- A solo developer with a $50/month budget and a 3-month deadline needs maximum simplicity and minimum operational overhead. Layered architecture scores 5/5 on both simplicity and cost — no other style matches this.
- All your features live in a single quantum. Layered architecture handles single-quantum systems cleanly without any structural waste.

**Trade-offs accepted:**
- Scalability (1/5) and elasticity (1/5) are poor. If your freelancer SaaS grows to thousands of concurrent users, you will eventually need to rethink the architecture. But a freelancer invoicing tool is unlikely to hit those limits soon, and if it does, that is a good problem to have — it means you have revenue to fund the migration.
- Deployability (1/5) is limited — the entire application deploys as one unit. For a solo developer, this is actually simpler, not harder.

**Trade-offs rejected (why alternatives were not chosen):**
- **Microservices:** Catastrophic mismatch. Solo developer, one quantum, $50 budget, 3-month timeline — microservices would add massive operational complexity (multiple deployments, inter-service communication, distributed data management, container orchestration) with zero architectural benefit. The book is explicit: team size <10 + no distributed experience + tight budget = do NOT choose microservices. This project fails on every prerequisite.
- **Service-based:** Adds distribution complexity (separate services, network calls, deployment coordination) that provides no benefit for a single-quantum system with one developer. The shared database advantage of service-based is moot when you would not split the database anyway.
- **Event-driven:** Scores 1/5 on simplicity, 3/5 on cost. Designed for high-performance, high-scalability real-time systems — massively over-engineered for an invoicing tool. The asynchronous complexity would slow you down, not speed you up.
- **Microkernel:** Reasonable on paper but the domain has no plug-in or customization axis. You are not building an extensible platform; you are building an invoicing tool.

## Getting Started

1. **Pick a single framework and deploy target.** Choose a full-stack framework that handles routing, ORM, and templating in one package (e.g., Django, Rails, Laravel, or Next.js with a Python/Node backend). Deploy to a single PaaS instance (Railway, Render, Fly.io — all fit within $50/month with a managed Postgres database). This gets you from zero to deployed in days, not weeks.

2. **Structure your layers cleanly from day one.** Even though layered is the simplest style, internal discipline matters. Organize into: (a) Presentation layer — web routes, API endpoints, (b) Business layer — invoice generation, payment logic, reminder scheduling, (c) Integration layer — Stripe SDK calls, PDF library calls, email service calls, (d) Persistence layer — database models and queries. Keep business logic out of route handlers. This structure costs nothing now and makes future migration possible if you outgrow the monolith.

3. **Use background job processing for reminders and PDF generation.** These are not separate services — they are background tasks within your monolith. Use your framework's built-in task queue (e.g., Celery for Django, Sidekiq for Rails, Bull for Node.js). This handles the "send reminders" and "generate PDFs" requirements without any architectural complexity beyond a single worker process alongside your web process.

## Migration Path

You do not need a migration plan today. But if the product succeeds and you need to evolve:

- **First scaling step (hundreds of active users):** Vertically scale your server and add a CDN for static assets. This is a hosting change, not an architecture change.
- **Second scaling step (thousands of active users, multiple developers):** Extract the Stripe integration and PDF generation into separate domain services within a service-based architecture. The clean layer separation from step 2 above makes this straightforward. This is the natural evolution path: layered monolith to service-based.
- **When to reconsider:** Only revisit the architecture decision if (a) you hire 3+ developers who need independent deployment, or (b) specific features need fundamentally different scaling characteristics. Until then, a well-structured monolith will serve you better than a premature distributed system.
