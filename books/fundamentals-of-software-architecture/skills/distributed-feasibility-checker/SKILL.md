---
name: distributed-feasibility-checker
description: Evaluate whether a system should adopt distributed architecture by systematically checking against the 8 Fallacies of Distributed Computing and assessing team/operational readiness. Use this skill whenever the user is considering microservices, debating monolith vs distributed, hearing "let's use microservices," evaluating operational readiness for distribution, or experiencing growing pains with a monolith — even if they don't mention "distributed computing fallacies."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/distributed-feasibility-checker
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [9, 17, 18]
tags: [software-architecture, architecture, distributed-systems, microservices, monolith, fallacies, feasibility]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "System description and team context — the skill guides the evaluation"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can scan for distribution indicators."
---

# Distributed Architecture Feasibility Checker

## When to Use

Someone is proposing or considering distributed architecture (microservices, service-based, event-driven) and you need to evaluate whether it's actually justified and feasible. Typical situations:

- "Let's move to microservices" — but has anyone checked if the team is ready?
- Growing pains with a monolith — but is distribution the right solution?
- CTO or tech lead pushing for distribution based on industry hype
- Pre-requisite sanity check before `architecture-style-selector`
- Post-quantum-analysis: you've identified multiple quanta, now check if the team can actually operate distributed

Before starting, verify:
- Is there a genuine architectural problem to solve? (If the monolith is working fine, distribution adds cost without benefit)
- Has quantum analysis been done? If not, distribution may not even be needed (use `architecture-quantum-analyzer` first)

## Context & Input Gathering

### Input Sufficiency Check

This skill critically depends on TEAM context, not just technical requirements. A system that technically needs distribution may still fail if the team can't operate it.

### Required Context (must have — ask if missing)

- **System description:** What does the system do? What's the current architecture?
  → Check prompt for: system purpose, current state (monolith/distributed/greenfield)
  → If missing, ask: "What does your system do, and what's your current architecture? (monolith, some services, greenfield?)"

- **Team size and distributed experience:** How many developers? Have they operated distributed systems before?
  → Check prompt for: team size, experience mentions, technology familiarity
  → If missing, ask: "How many developers do you have, and has your team operated distributed systems (microservices, message queues, service mesh) before?"
  → **WHY this is critical:** Team experience is the #1 predictor of distributed architecture success. A team that's never run microservices will struggle regardless of technical merit.

- **Motivation for considering distribution:** Why are they thinking about this?
  → Check prompt for: scaling issues, deployment pain, team autonomy needs, hype
  → If missing, ask: "What specific problem is driving you toward distributed architecture? (a) scaling bottleneck, (b) deployment takes too long, (c) teams stepping on each other, (d) someone said we should, (e) other?"

### Observable Context (gather from environment)

- **Current infrastructure:** What deployment and monitoring tools exist?
  → Look for: docker-compose, k8s manifests, CI/CD configs, monitoring configs
  → Reveals: operational maturity level
- **Service communication:** Are there already distributed calls?
  → Look for: HTTP client imports, message queue configs, gRPC definitions
  → Reveals: whether distribution has already started

### Default Assumptions

- If team experience unknown → assume NO distributed experience (safer to overestimate the challenge)
- If monitoring tools unknown → assume basic logging only (no distributed tracing)
- If motivation unclear → probe before proceeding — distribution without clear motivation is the biggest risk

### Sufficiency Threshold

```
SUFFICIENT: system description + team size + team experience + motivation are known
MUST ASK: team experience is unknown (this is NEVER safe to default)
```

## Process

### Step 1: Understand the Motivation

**ACTION:** Clarify WHY distribution is being considered. Categorize the motivation.

**WHY:** The most dangerous path to distributed architecture is "because everyone else is doing it." Valid motivations have specific, measurable problems. Invalid motivations are based on hype, resume-driven development, or "Netflix does it." Categorizing the motivation early prevents wasted analysis.

| Motivation | Validity | Next step |
|-----------|:---:|----------|
| Specific scaling bottleneck in one part | Valid | Quantify the bottleneck |
| Deployment takes too long (all-or-nothing) | Valid | Check if modular monolith solves it first |
| Teams blocking each other on shared code | Valid | Check if code ownership solves it first |
| "Everyone uses microservices now" | **Invalid** | Push back — this isn't a problem statement |
| "Our CTO read an article" | **Invalid** | Ask what specific problem they're trying to solve |
| Technology exploration / learning | Partially valid | Be honest about the cost of learning in production |

### Step 2: Evaluate Against the 8 Fallacies

**ACTION:** Systematically evaluate the project against each of the 8 Fallacies of Distributed Computing. For each, assess: does the team understand this risk? Do they have mitigations?

**WHY:** The 8 fallacies are assumptions that developers make about distributed systems that are FALSE. Every distributed system must contend with all 8. Teams that haven't thought about them will be surprised — and surprises in distributed systems cause outages. Using these as a checklist transforms abstract knowledge into a concrete readiness assessment.

For each fallacy, evaluate:

| # | Fallacy | The false assumption | Reality check question |
|---|---------|---------------------|----------------------|
| 1 | **The Network Is Reliable** | Network calls always succeed | Do you have timeouts and circuit breakers? What happens when Service B is unreachable? |
| 2 | **Latency Is Zero** | Remote calls are as fast as local | What's your average and 95th-percentile latency? How many chained service calls per request? |
| 3 | **Bandwidth Is Infinite** | Send as much data as you want | Are you sending entire objects when you only need a few fields? (Stamp coupling) |
| 4 | **The Network Is Secure** | Internal network is safe | Does distribution multiply your attack surface? How many new network endpoints? |
| 5 | **The Topology Never Changes** | Network layout is fixed | What happens when ops upgrades routers on the weekend? Do your services use hardcoded IPs? |
| 6 | **There Is Only One Administrator** | One team controls everything | How many teams manage infrastructure? Who coordinates deployments? |
| 7 | **Transport Cost Is Zero** | Network calls are free | What's the actual infrastructure cost of service mesh, load balancers, API gateways? |
| 8 | **The Network Is Homogeneous** | All network equipment is the same | Do you run multi-cloud? Different hardware vendors? |

### Step 3: Assess Operational Readiness

**ACTION:** Evaluate whether the team has the operational maturity to run distributed systems.

**WHY:** Distribution doesn't just change how you code — it fundamentally changes how you operate. Distributed logging, distributed tracing, distributed transactions, independent deployments, service discovery, contract versioning — these are operational capabilities that don't exist in monolith-land. A team without these capabilities will build a distributed system they can't debug, can't deploy safely, and can't monitor.

| Capability | Question | Ready if... | Not ready if... |
|-----------|---------|-------------|-----------------|
| **Distributed logging** | Can you correlate logs across services? | Have ELK/Datadog with correlation IDs | Console.log to stdout per service |
| **Distributed tracing** | Can you trace a request across service boundaries? | Have Jaeger/Zipkin/Datadog APM | No tracing infrastructure |
| **CI/CD per service** | Can you deploy one service without deploying all? | Per-service pipelines with independent versioning | Single pipeline deploying everything |
| **Service discovery** | How do services find each other? | Service mesh, DNS-based, or registry | Hardcoded URLs in config |
| **Contract management** | How do you handle API changes between services? | Versioned APIs, consumer-driven contract tests | No versioning strategy |
| **Monitoring & alerting** | Can you detect when one service is degrading? | Per-service health checks, SLO dashboards | Aggregate-only monitoring |

### Step 4: Check for Simpler Alternatives

**ACTION:** Before recommending distribution, verify that simpler solutions don't solve the problem.

**WHY:** Distribution is the most expensive solution to almost any problem. A modular monolith with good code boundaries solves many of the same problems (team autonomy, code organization, independent development) without the operational overhead. The book explicitly states that monolith advantages are REAL — simpler deployment, simpler testing, simpler debugging, lower cost. Distribution should be the LAST option, not the first.

| Problem | Simpler alternative | When it's NOT enough |
|---------|-------------------|---------------------|
| Deployment takes too long | Modular monolith with independent module builds | Different modules need different deployment frequencies |
| Teams stepping on each other | Code ownership + branch-by-abstraction | Teams need different technology stacks |
| One part needs to scale | Separate the hot path only (strangler fig) | 3+ parts need independent scaling |
| "It's too complex" | Better module boundaries, cleaner interfaces | Genuine bounded contexts with different data models |

### Step 5: Produce the Feasibility Assessment

**ACTION:** Compile a structured go/no-go assessment with specific recommendations.

**WHY:** The value of this skill is the structured, honest assessment — not a blanket "yes" or "no" to microservices. Some teams are ready. Some aren't. Some should start with a single service extraction, not full distribution. The assessment should be specific enough to act on.

## Inputs

- System description and current architecture
- Team size, experience, and operational capabilities
- Motivation for considering distribution

## Outputs

### Distributed Architecture Feasibility Assessment

```markdown
# Feasibility Assessment: {System Name}

## Motivation Analysis
**Stated motivation:** {what the team says}
**Validated motivation:** {Valid / Invalid / Partially valid}
**Underlying problem:** {the real problem, which may differ from stated motivation}

## 8 Fallacies Evaluation

| # | Fallacy | Team awareness | Mitigations in place | Risk level |
|---|---------|:---:|:---:|:---:|
| 1 | Network Is Reliable | Yes/No | {specific mitigations or "none"} | Low/Med/High |
| 2 | Latency Is Zero | Yes/No | {mitigations} | Low/Med/High |
| 3 | Bandwidth Is Infinite | Yes/No | {mitigations} | Low/Med/High |
| 4 | Network Is Secure | Yes/No | {mitigations} | Low/Med/High |
| 5 | Topology Never Changes | Yes/No | {mitigations} | Low/Med/High |
| 6 | Only One Administrator | Yes/No | {mitigations} | Low/Med/High |
| 7 | Transport Cost Is Zero | Yes/No | {mitigations} | Low/Med/High |
| 8 | Network Is Homogeneous | Yes/No | {mitigations} | Low/Med/High |

**Fallacy readiness score:** {X}/8 mitigated

## Operational Readiness

| Capability | Status | Gap |
|-----------|:---:|-----|
| Distributed logging | Ready/Not ready | {what's missing} |
| Distributed tracing | Ready/Not ready | {what's missing} |
| CI/CD per service | Ready/Not ready | {what's missing} |
| Service discovery | Ready/Not ready | {what's missing} |
| Contract management | Ready/Not ready | {what's missing} |
| Monitoring & alerting | Ready/Not ready | {what's missing} |

**Operational readiness score:** {X}/6 capabilities in place

## Simpler Alternatives Considered
| Alternative | Solves the problem? | Why/why not |
|------------|:---:|-------------|
| Modular monolith | Yes/No/Partially | {reasoning} |
| Single service extraction | Yes/No/Partially | {reasoning} |
| Better code boundaries | Yes/No/Partially | {reasoning} |

## Recommendation
**{Go / No-Go / Conditional Go}**
- {Primary reasoning}
- {If conditional: what must be done first}

## If Proceeding: Readiness Roadmap
1. {First capability to build before distributing}
2. {Second capability}
3. {Suggested first service to extract}
```

## Key Principles

- **Distribution is a trade-off, not an upgrade** — Distributed architecture gains scalability and team autonomy but pays with operational complexity, debugging difficulty, and infrastructure cost. It's not inherently better than monolith — it's different, with different trade-offs. The 8 fallacies are the price of admission.

- **Team readiness trumps technical need** — A technically justified distributed architecture operated by an unprepared team produces worse outcomes than a monolith. Team experience with distributed operations, monitoring, and debugging is the #1 success predictor.

- **Check for simpler solutions first** — A modular monolith with clean boundaries solves 80% of the problems people think require microservices, at 20% of the operational cost. Distribution should be the LAST option, not the first.

- **Monolith is not a dirty word** — The book explicitly defends monolith advantages: simpler deployment, simpler testing, simpler debugging, lower operational cost. Many successful systems run as monoliths. Don't recommend distribution to be "modern."

- **The distributed monolith is the worst outcome** — Adopting microservices but keeping all the coupling of a monolith gives you the operational overhead of distribution with none of the benefits. This is the most common result of premature distribution.

- **Latency is the deal-breaker** — Fallacy #2 is the primary factor in whether distribution is feasible. If your request chains 10 service calls at 100ms each, you've added 1 second of latency. Know your numbers before committing.

## Examples

**Scenario: Startup wanting microservices**
Trigger: "We're 5 developers building a SaaS. Should we start with microservices?"
Process: Asked about motivation — "our CTO says it's best practice." Invalid motivation — no specific problem. Evaluated: team has no distributed experience, no monitoring beyond basic logging, single CI pipeline. Checked simpler alternatives: modular monolith solves all current needs. Fallacy check: 0/8 mitigated. Operational readiness: 0/6.
Output: **No-Go.** Recommended modular monolith with clean domain boundaries. Distribution adds operational cost the 5-person team can't absorb. Revisit when: team hits 15+ developers, or specific parts need independent scaling proven by data.

**Scenario: Growing monolith with real pain**
Trigger: "We have 40 developers, deployments take 2 hours, and the payment module keeps bringing down the whole site during Black Friday."
Process: Valid motivation — specific scaling bottleneck + deployment pain. Team has 3 years of monolith experience, basic CI/CD, Datadog for monitoring but no distributed tracing. Fallacy evaluation: aware of #1 and #2, unaware of #3-#8. Operational readiness: 2/6 (monitoring, basic CI/CD). Simpler alternatives: modular monolith partially solves deployment but not the Black Friday scaling.
Output: **Conditional Go.** Extract payment module as first service (strangler fig pattern). Before extracting: implement distributed tracing, per-service CI/CD pipeline, and circuit breakers. Don't attempt full microservices — start with 2-3 services maximum.

**Scenario: Already distributed but struggling**
Trigger: "We went microservices 6 months ago and everything is on fire. Can't trace bugs, deployments are a nightmare, and our latency tripled."
Process: Diagnosed against fallacies: Fallacy #2 (latency) — chaining 8 synchronous calls, 95th percentile at 2 seconds. Fallacy #1 — no circuit breakers, cascading failures. Operational readiness: 1/6 (only basic logging). The team fell into the distributed monolith anti-pattern — services share a database and deploy in lockstep.
Output: Feasibility assessment showing the team wasn't ready. Recommended: consolidate back to 3-4 larger services (from 12), implement distributed tracing and circuit breakers, establish per-service databases before attempting fine-grained services again.

## References

- For the full 8 Fallacies with detailed mitigations, see [references/eight-fallacies.md](references/eight-fallacies.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
