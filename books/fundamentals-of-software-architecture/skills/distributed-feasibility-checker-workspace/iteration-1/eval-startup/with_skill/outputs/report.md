# Feasibility Assessment: B2B Invoice Management SaaS

## Motivation Analysis
**Stated motivation:** CTO attended a conference and came back saying the team needs to move to microservices.
**Validated motivation:** Invalid
**Underlying problem:** No specific problem was identified. The motivation is conference-driven hype, not a response to a measurable pain point. There is no mention of scaling bottlenecks, deployment friction, team coordination issues, or any concrete symptom that distribution would address. This is the "our CTO read an article" anti-pattern — the most dangerous path to distributed architecture because there is no success criterion to measure against.

## 8 Fallacies Evaluation

| # | Fallacy | Team awareness | Mitigations in place | Risk level |
|---|---------|:---:|:---:|:---:|
| 1 | Network Is Reliable | No | None — current monolith on Heroku makes all calls in-process; no timeouts, retry logic, or circuit breakers for inter-service communication exist | High |
| 2 | Latency Is Zero | No | None — team has no experience measuring or managing inter-service latency; moving from in-process method calls to network calls will add latency to every decomposed interaction | High |
| 3 | Bandwidth Is Infinite | No | None — no API design discipline for distributed payloads; risk of stamp coupling (sending entire invoice objects between services when only IDs are needed) | Medium |
| 4 | Network Is Secure | No | None — Heroku provides basic platform security, but splitting into services multiplies the attack surface; no service-to-service authentication or mTLS | High |
| 5 | Topology Never Changes | No | None — Heroku abstracts some topology concerns, but service discovery across multiple dynos/services would need explicit handling | Medium |
| 6 | Only One Administrator | No | None — with 5 people, there is effectively one administrator today, which is fine for a monolith; distribution would require coordination across service boundaries that the team has no practice with | Low |
| 7 | Transport Cost Is Zero | No | None — moving from a single Heroku dyno to multiple services means multiple dynos, potentially a message broker, API gateway, and load balancers; real infrastructure cost increase for a small team | High |
| 8 | Network Is Homogeneous | No | None — currently homogeneous (single Heroku stack), but distribution often introduces heterogeneity over time | Low |

**Fallacy readiness score:** 0/8 mitigated

The team has zero mitigations in place for any of the 8 fallacies. This is expected — they are running a monolith, so these problems don't exist yet. But it means adopting distribution would require simultaneously learning and solving all 8 fallacies in production.

## Operational Readiness

| Capability | Status | Gap |
|-----------|:---:|-----|
| Distributed logging | Not ready | Papertrail provides centralized log aggregation, but no correlation IDs, no structured logging for cross-service request tracing. Papertrail is a log viewer, not a distributed observability platform. |
| Distributed tracing | Not ready | No tracing infrastructure whatsoever. No Jaeger, Zipkin, Datadog APM, or equivalent. Cannot trace a request across service boundaries. |
| CI/CD per service | Not ready | Single CI/CD pipeline. Cannot deploy one service independently. Moving to per-service pipelines requires pipeline redesign, independent versioning, and independent deployment orchestration. |
| Service discovery | Not ready | No service discovery mechanism. Heroku provides basic DNS for a single app, but multi-service discovery would need explicit implementation (e.g., Consul, service mesh, or at minimum environment-based config). |
| Contract management | Not ready | No API versioning strategy, no consumer-driven contract tests, no schema registry. Services would be tightly coupled from day one. |
| Monitoring & alerting | Not ready | Papertrail provides basic log search and alerts on log patterns, but no per-service health checks, no SLO dashboards, no latency percentile tracking, no dependency health mapping. |

**Operational readiness score:** 0/6 capabilities in place

The team's current operational tooling (single Heroku app + Papertrail) is appropriate for a monolith but provides essentially none of the capabilities required to operate a distributed system safely.

## Simpler Alternatives Considered

| Alternative | Solves the problem? | Why/why not |
|------------|:---:|-------------|
| Modular monolith | Yes | Since no specific problem was stated, there is no problem that distribution uniquely solves. A modular monolith with clean domain boundaries (e.g., invoicing, payments, users, notifications as separate Rails engines or modules) gives the team code organization, independent development within modules, and a clear path to future extraction if real scaling needs emerge — all without operational overhead. |
| Single service extraction | N/A | There is no identified bottleneck to extract. Extracting a service without a reason creates a distributed monolith — the worst of both worlds. |
| Better code boundaries | Yes | If the underlying concern is code organization or "the monolith feels messy," enforcing module boundaries, introducing domain-driven design within Rails (service objects, bounded contexts via namespaces), and improving test coverage addresses the root cause directly. |

## Recommendation

**No-Go.**

- **No valid motivation exists.** The stated driver is conference hype, not a specific, measurable problem. Distribution without a clear problem to solve means there is no way to measure success and no way to know when you're done.
- **The team has zero distributed systems experience.** A 5-person team learning microservices, distributed tracing, circuit breakers, service discovery, contract management, and per-service CI/CD — all simultaneously, in production, on a B2B SaaS with paying customers — is a recipe for prolonged instability.
- **Operational readiness is 0/6.** The current infrastructure (single Heroku app, Papertrail, one CI/CD pipeline) would need to be almost entirely rebuilt before distributed architecture is viable.
- **Fallacy readiness is 0/8.** The team has not yet encountered or mitigated any of the fundamental challenges of distributed computing.
- **The monolith is working.** No scaling problems, no deployment pain, no team coordination issues were mentioned. A working monolith is an asset, not a liability.
- **A 5-person team cannot absorb the operational tax.** Microservices require dedicated investment in infrastructure, observability, and operational tooling. For a 5-person team, this overhead would consume a significant fraction of total engineering capacity, directly competing with feature development for a B2B product that needs to grow.

## Instead: Recommended Path Forward

1. **Ask the CTO the real question:** "What specific problem are we trying to solve?" If there is a real pain point (slow deploys, scaling concern, code complexity), address that directly. If the answer is "best practice" or "future-proofing," the answer is: the best practice for a 5-person team is a well-structured monolith.

2. **Invest in a modular monolith now.** Organize the Rails app into clear domain modules (invoicing, payments, users, notifications, reporting). Use Rails engines or strict namespace conventions. This gives you 80% of the organizational benefits of microservices at 20% of the cost.

3. **Establish good boundaries that enable future extraction.** If the product succeeds and the team grows to 15-20+ engineers, or specific modules hit measurable scaling limits, those clean module boundaries become natural service extraction points.

4. **Revisit distribution when you have data.** The right time to consider microservices is when you can point to specific, measured problems: "the payment module needs to scale 10x independently," "deploys take 45 minutes and we deploy 10 times a day," or "three teams of 8 are constantly blocked by shared code." Numbers, not conferences, should drive this decision.

5. **If the CTO wants to learn microservices:** Build a non-critical internal tool or side project as a learning exercise. Do not learn distributed systems on your revenue-generating production system.
