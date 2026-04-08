---
name: architecture-style-selector
description: Guide the systematic selection of an architecture style by evaluating domain needs, architecture characteristics, quantum count, data constraints, and organizational factors against all major architecture styles (layered, pipeline, microkernel, service-based, event-driven, space-based, microservices). Use this skill whenever the user is choosing an architecture pattern, deciding between monolith and distributed, comparing architecture styles (e.g., "event-driven vs microservices"), asking "which architecture should we use?", starting a new system and considering options, or reconsidering their current architecture — even if they don't use the phrase "architecture style."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-style-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - architecture-characteristics-identifier
  - architecture-quantum-analyzer
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
tags: [software-architecture, architecture, style-selection, monolith, distributed, microservices, event-driven, decision-making]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "System description, requirements, and organizational context — the skill guides the entire selection process"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can analyze current architecture."
---

# Architecture Style Selector

## When to Use

You need to choose or recommend an architecture style for a system. This is the culminating architecture decision — it integrates characteristics analysis, quantum analysis, and feasibility checking into a concrete style recommendation. Typical situations:

- New system — "we're building X, what architecture should we use?"
- Architecture evaluation — "should we use microservices or event-driven?"
- Migration — "we've outgrown our monolith, what should we move to?"
- Validation — "we chose microservices, was that right?"
- Post-analysis — you've identified characteristics and quanta, now pick the style

Before starting, verify:
- Are architecture characteristics identified? If not, use `architecture-characteristics-identifier` first — you need the top 3 driving characteristics.
- Is quantum analysis done? If components need different quality attributes, use `architecture-quantum-analyzer` first — quantum count determines monolith vs distributed.
- If the user is only asking whether distribution is feasible (not which style), use `distributed-feasibility-checker` instead.

## Context & Input Gathering

### Input Sufficiency Check

This skill synthesizes multiple analysis dimensions. You can proceed with partial information and fill gaps during the process, but certain inputs dramatically improve the recommendation quality.

### Required Context (must have — ask if missing)

- **System purpose and domain:** What does this system do?
  → Check prompt for: domain description, problem statement, business context
  → If missing, ask: "What does your system do? What problem does it solve?"

- **Driving architecture characteristics:** What quality attributes matter most? (Top 3)
  → Check prompt for: scalability, performance, availability, deployability, elasticity, etc.
  → If available from prior `architecture-characteristics-identifier` output, use those
  → If missing, ask: "What are the top 3 quality attributes this system must excel at? For example: (a) scalability, (b) performance, (c) simplicity, (d) deployability, (e) fault tolerance, (f) elasticity, (g) evolutionary/agility, (h) cost"

- **Number of architecture quanta:** Do different parts need different characteristics?
  → Check prompt for: quantum analysis results, mentions of "some parts need X while others need Y"
  → If available from prior `architecture-quantum-analyzer` output, use that
  → If missing, ask: "Do all parts of your system share the same quality attribute needs, or do some parts need different characteristics? For example: 'the order processing needs high scalability but reporting just needs batch processing.'"

### Important Context (strongly recommended — ask if easy to obtain)

- **Team size and experience:** How many developers? What architectures has the team built before?
  → Check prompt for: team mentions, experience level, technology familiarity
  → If missing, ask: "How large is your development team, and what architecture styles has your team worked with before?"

- **Data architecture constraints:** Can data be partitioned? Are ACID transactions required across workflows?
  → Check prompt for: database mentions, transaction requirements, consistency needs
  → If missing and relevant (distributed styles under consideration), ask: "Does your system require strict transactional consistency across different workflows, or can parts tolerate eventual consistency?"

### Observable Context (gather from environment)

- **Existing architecture:** If restructuring, scan for current patterns
  → Look for: package structure (layered? domain?), service folders, docker-compose, k8s manifests
  → Reveals: current style, migration starting point
- **Infrastructure maturity:** What deployment and monitoring tools exist?
  → Look for: CI/CD configs, monitoring configs, container orchestration
  → Reveals: operational readiness for distributed styles

### Default Assumptions

- If characteristics unknown → ask before proceeding (this is critical input)
- If quantum count unknown → assume single quantum (default to monolith evaluation first)
- If team experience unknown → assume moderate experience (can handle service-based but not full microservices)
- If data constraints unknown → assume shared database is acceptable

### Sufficiency Threshold

```
SUFFICIENT: system purpose + top 3 characteristics + quantum count are known
PROCEED WITH DEFAULTS: system purpose + characteristics are known, quantum unclear
MUST ASK: system purpose OR driving characteristics are missing
```

## Process

### Step 1: Determine Monolith vs Distributed

**ACTION:** Based on quantum analysis, make the first and most impactful fork in the decision tree.

**WHY:** This is the single most important architectural decision. Every subsequent choice flows from it. The book is explicit: if a single set of architecture characteristics suffices for the entire system (one quantum), a monolith offers real advantages — simpler deployment, simpler testing, simpler debugging, lower cost. Distribution should only be chosen when different parts genuinely need different quality attributes, requiring multiple independent deployment units. Getting this wrong is expensive: choosing distributed when monolith suffices adds unnecessary operational complexity; choosing monolith when distribution is needed creates a bottleneck that's painful to refactor later.

**Decision logic:**
- **One quantum** (all components share the same characteristic profile) → **Monolith** likely sufficient. Evaluate layered, pipeline, and microkernel.
- **Multiple quanta** (components need different characteristics) → **Distributed** likely needed. Evaluate service-based, event-driven, space-based, and microservices.
- **Uncertain** → Default to monolith evaluation first. It's easier to extract services from a well-structured monolith than to merge poorly separated microservices.

**IF** monolith → proceed to Step 2A.
**IF** distributed → proceed to Step 2B.
**IF** uncertain → evaluate monolith options first (Step 2A), then check if they can support the requirements. If not, proceed to Step 2B.

### Step 2A: Evaluate Monolithic Styles

**ACTION:** Score the three monolithic styles against the driving characteristics using the comparison matrix. Check for domain/architecture isomorphism.

**WHY:** Each monolithic style has a distinct profile. Layered excels at simplicity and cost but scores 1 on nearly everything else. Pipeline is ideal for linear data processing but can't handle complex interactions. Microkernel is the best monolith for extensibility and customization. Choosing between them isn't arbitrary — it's driven by which style's natural strengths align with your driving characteristics, and whether the problem domain's shape naturally maps to the architecture's topology (isomorphism).

Consult the comparison matrix in [references/style-comparison-matrix.md](references/style-comparison-matrix.md) for detailed ratings.

**Evaluation for each candidate:**

| Style | Consider when... | Eliminate when... |
|-------|-----------------|-------------------|
| **Layered** | Simplicity and low cost are primary drivers; requirements still evolving; team is small | Scalability, elasticity, or deployability are driving characteristics |
| **Pipeline** | Data flows linearly through processing stages; ETL, content processing, orchestration | Workflows are not linear; complex user interaction patterns |
| **Microkernel** | High customizability needed; regional/client variations; plug-in extensibility | Need independent scaling of parts; multiple quanta required |

**Isomorphism check:** Does the problem domain naturally match the architecture topology?
- Data transformation pipeline → Pipeline
- Customizable product with rules/variants → Microkernel
- Simple business app, uncertain requirements → Layered (iterate from here)

**Output:** 1-2 candidate monolithic styles with characteristic scores, or a conclusion that monolith cannot meet the requirements (proceed to Step 2B).

### Step 2B: Evaluate Distributed Styles

**ACTION:** Score the four distributed styles against the driving characteristics. Factor in data architecture and communication style.

**WHY:** Distributed styles have dramatically different profiles. Service-based is the pragmatic middle ground — good at most things, extreme at nothing, and preserves ACID transactions through shared database. Event-driven excels at performance and scalability but is the hardest to test. Space-based handles extreme elasticity through in-memory processing but at high cost. Microservices maximize independence but require the most operational maturity. The right choice depends on which characteristics you need to MAXIMIZE, not just "support."

Consult the comparison matrix in [references/style-comparison-matrix.md](references/style-comparison-matrix.md) for detailed ratings.

**Evaluation for each candidate:**

| Style | Consider when... | Eliminate when... |
|-------|-----------------|-------------------|
| **Service-based** | Need pragmatic distribution without full microservices complexity; ACID transactions needed; team transitioning from monolith | Need extreme scalability or elasticity; need per-service technology diversity |
| **Event-driven** | Performance and scalability are primary drivers; natural event flow in domain; real-time processing | Need request-reply semantics; team lacks async debugging experience; strong consistency required everywhere |
| **Space-based** | Extreme and unpredictable elasticity needs; variable load patterns; cost is secondary | Predictable, steady load; budget-constrained; data consistency is critical |
| **Microservices** | Maximum team autonomy; independent deployability; different tech stacks per service; mature DevOps | Small team; immature DevOps; highly coupled domain; need ACID transactions across services |

**Data architecture sub-decision:** Where should data live?
- **Shared database** → Service-based (simplest, preserves ACID)
- **Logically partitioned** → Service-based with domain-scoped schemas
- **Per-service databases** → Microservices or event-driven (requires eventual consistency)

**Communication sub-decision:** Synchronous or asynchronous?
- **Synchronous** (REST, gRPC) → Convenient but creates runtime coupling; limits scalability
- **Asynchronous** (events, messaging) → Better scalability and decoupling; harder to debug
- **Hybrid** → Most common in practice; synchronous for queries, async for commands/events

### Step 3: Check Organizational Fit

**ACTION:** Validate that the candidate style(s) match the team's capabilities and organizational constraints.

**WHY:** The technically ideal architecture may be operationally infeasible. A team of 5 developers without distributed systems experience choosing microservices is setting up for a distributed monolith — the worst possible outcome. The book is clear: organizational factors (team size, DevOps maturity, deployment process, budget) can and should override purely technical analysis. An architecture the team can't operate is worse than a simpler architecture they can operate well.

| Factor | Impact on style selection |
|--------|-------------------------|
| **Team size <10** | Avoid microservices. Consider service-based or monolith. |
| **Team size 10-30** | Service-based or limited microservices (start with 3-5 services). |
| **Team size 30+** | Microservices viable if DevOps maturity is high. |
| **No distributed experience** | Start with monolith or service-based. Do NOT jump to microservices. |
| **Immature CI/CD** | Avoid any style requiring per-service pipelines. Service-based max. |
| **Tight budget** | Monolithic styles (layered, pipeline, microkernel) strongly favored. |
| **Mergers/acquisitions expected** | Favor integration-friendly styles (service-based, microservices). |
| **Must ship fast** | Service-based or layered. Avoid event-driven and space-based (long setup). |

**IF** organizational constraints eliminate the technically best option → recommend the next-best style that the team CAN operate, with a roadmap to grow into the ideal style.

### Step 4: Check for Anti-Patterns

**ACTION:** Verify the candidate style doesn't match known anti-patterns for this domain.

**WHY:** Each style has specific failure modes that are predictable and preventable. The architecture sinkhole in layered, the reuse-coupling trap in SOA, enforced heterogeneity in microservices — these aren't edge cases, they're the most common mistakes. Checking for anti-patterns before committing to a style prevents choosing a style that will fail in a predictable way. This is the "measure twice, cut once" step.

| Anti-pattern | Style affected | Detection | Resolution |
|-------------|---------------|-----------|------------|
| **Architecture Sinkhole** | Layered | >20% of requests pass through layers with no processing | Switch to open layers or consider a different style |
| **Distributed Monolith** | Microservices | Services share DB, deploy in lockstep, require synchronized changes | Consolidate into service-based, or fix service boundaries |
| **Too-Fine-Grained Services** | Microservices | Services smaller than bounded contexts, excessive inter-service calls | Merge related services; "microservice" is a label, not a description |
| **Enforced Heterogeneity** | Microservices | Mandating different tech per service | Use appropriate tech, not mandatory diversity |
| **Transactions Across Boundaries** | Microservices | Need for ACID across services | Fix granularity — services needing transactions belong together |
| **Broker/Mediator Mismatch** | Event-driven | Using broker for complex error-handling workflows, or mediator for simple fire-and-forget | Match topology to workflow complexity |
| **Reuse Coupling Trap** | SOA-style | Shared services create coupling between all consumers | Prefer duplication over coupling in distributed systems |

### Step 5: Score and Recommend

**ACTION:** Produce a scored comparison of the top 2-3 candidate styles and make a clear recommendation.

**WHY:** Architecture decisions are never binary — they're trade-off decisions where the goal is the "least worst set of trade-offs" (the book's exact words). Presenting scored alternatives with explicit trade-offs enables informed decision-making rather than dogmatic style selection. The recommendation should be specific enough to act on, including not just which style but how to get started with it.

**Scoring method:**
1. List the top 3 driving characteristics
2. For each candidate style, look up the star rating for each characteristic
3. Sum the scores (max possible = 15 for 3 characteristics at 5 stars each)
4. Apply organizational fit modifier: -1 per significant organizational gap
5. Apply isomorphism bonus: +1 if domain naturally maps to the style's topology

## Inputs

- System description and domain
- Driving architecture characteristics (top 3, prioritized)
- Architecture quantum count (from quantum analysis or estimation)
- Team size, experience, and organizational constraints
- Data architecture constraints (ACID needs, partitioning feasibility)

## Outputs

### Architecture Style Recommendation

```markdown
# Architecture Style Selection: {System Name}

## Decision Context
**System:** {what it does}
**Driving characteristics:** {top 3, in priority order}
**Architecture quanta:** {count and reasoning}
**Team context:** {size, experience, constraints}

## Step 1: Monolith vs Distributed
**Decision:** {Monolith / Distributed / Hybrid}
**Reasoning:** {quantum count, characteristic variance, organizational factors}

## Candidate Evaluation

| Criterion | {Style A} | {Style B} | {Style C} |
|-----------|:---------:|:---------:|:---------:|
| {Characteristic 1} (priority) | {score}/5 | {score}/5 | {score}/5 |
| {Characteristic 2} | {score}/5 | {score}/5 | {score}/5 |
| {Characteristic 3} | {score}/5 | {score}/5 | {score}/5 |
| **Characteristic total** | **{sum}** | **{sum}** | **{sum}** |
| Organizational fit | {Good/Fair/Poor} | {Good/Fair/Poor} | {Good/Fair/Poor} |
| Domain isomorphism | {Yes/No} | {Yes/No} | {Yes/No} |
| Anti-pattern risk | {risk or "none"} | {risk or "none"} | {risk or "none"} |

## Data Architecture
**Data location:** {shared DB / partitioned / per-service}
**Communication:** {sync / async / hybrid}
**Consistency model:** {ACID / eventual / mixed}

## Recommendation
**Selected style: {Style Name}**

**Why this style:**
- {Primary reason — how it matches driving characteristics}
- {Secondary reason — organizational fit, isomorphism}

**Trade-offs accepted:**
- {What you give up by choosing this style}
- {What you gain}

**Trade-offs rejected (why alternatives were not chosen):**
- {Style B}: {why it was eliminated}
- {Style C}: {why it was eliminated}

## Getting Started
1. {First concrete step to implement this style}
2. {Second step}
3. {Key pattern or practice to adopt}

## Migration Path (if applicable)
{If current system exists, how to get from here to there}
```

## Key Principles

- **Everything is a trade-off** — The First Law of Software Architecture. There is no "best" architecture style — only the one with the least worst set of trade-offs for your specific context. Every style gains something by sacrificing something else. Anyone claiming one style is universally superior hasn't understood the problem.

- **Quantum count drives the first fork** — The monolith vs distributed decision is not a matter of preference. One quantum = monolith is architecturally sufficient. Multiple quanta with different characteristic needs = distribution is architecturally required. This is a structural determination, not a philosophical one.

- **Organizational fit trumps technical optimality** — The best architecture is one the team can actually build and operate. A technically perfect microservices design operated by a team without distributed experience produces worse outcomes than a "suboptimal" service-based architecture they can run well. Factor in team size, DevOps maturity, and operational capability.

- **Domain/architecture isomorphism matters** — Some problem domains naturally match certain architecture topologies. Customization-heavy systems map to microkernel. Linear data processing maps to pipeline. High-scale event processing maps to event-driven. Fighting isomorphism creates friction; embracing it creates natural solutions.

- **Start simple, evolve up** — When uncertain, start with the simplest style that could work. It's far easier to extract services from a well-structured monolith than to merge poorly separated microservices. Service-based architecture is often the best "starting distributed" option because it offers distribution benefits at moderate complexity.

- **Monolith is not a dirty word** — The book explicitly lists monolith advantages: simpler deployment, simpler testing, simpler debugging, lower cost. Many successful systems run as monoliths. Choosing monolith when it fits is a sign of architectural maturity, not backwardness. Don't recommend distribution to be "modern."

## Examples

**Scenario: Nationwide sandwich shop ordering system (Silicon Sandwiches)**
Trigger: "We're building an online ordering system for a sandwich franchise. Need web/mobile ordering, regional customization, promotions, and POS integration."
Process: Identified characteristics — scalability (lunch rush traffic), customizability (regional recipes), availability (ordering must work). Quantum analysis: single quantum — all features share the same scalability/availability profile. Monolith is sufficient. Evaluated monolithic styles: Layered (simplicity fits, but customizability scores 1), Microkernel (customizability is built-in, regional variations as plug-ins, scores well). Isomorphism check: the customization requirement naturally maps to microkernel's plug-in topology. Organizational fit: small team, low budget — microkernel's simplicity (4) and cost (5) work well.
Output: **Microkernel** recommended. Core system handles ordering workflow; plug-in components handle regional customization (recipes, prices, promotions). Layered was backup option but doesn't structurally support customization. Trade-off accepted: limited to single quantum scaling. Trade-off rejected: microservices would add operational cost without solving the core customization problem.

**Scenario: Online auction with real-time bidding (Going, Going, Gone)**
Trigger: "Building an online auction platform. Need real-time bidding, live video streaming, bid tracking, and payment processing. Expecting thousands of concurrent bidders."
Process: Identified characteristics — elasticity (bursty bidder traffic), performance (sub-second bids), reliability (bids cannot be lost), availability (auctioneer feed can't drop). Quantum analysis: MULTIPLE quanta — bidder-facing components need different characteristics (high elasticity) than auctioneer-facing components (high reliability). Different quanta → distributed. Evaluated distributed styles: Service-based (pragmatic but scores 2 on elasticity — insufficient for burst traffic), Event-driven (performance 5, scalability 5 — matches real-time event flow), Microservices (scalability 5 but adds complexity beyond what's needed), Space-based (elasticity 5 but massive cost for this scale). Isomorphism: real-time bid events naturally flow as events — event-driven topology matches the domain. Data: per-component databases (bidding needs strong consistency, tracking can be eventual). Communication: async for bid streams, sync for payment.
Output: **Event-driven architecture** with microservices topology for service boundaries. Bid processing uses broker topology for real-time event flow. Payment uses mediator topology for workflow orchestration with error handling. Trade-off accepted: harder to test, eventual consistency for non-critical paths. Trade-off rejected: service-based can't handle the elasticity requirements; pure microservices without event-driven doesn't match the domain's natural event flow.

**Scenario: Internal business application for insurance company**
Trigger: "We're building an insurance claim processing system. Multi-page forms where each page depends on context from previous pages. Team of 8 developers, no distributed experience. Budget is tight."
Process: Identified characteristics — reliability (claims can't be lost), simplicity (team is small), cost (budget-constrained). Quantum analysis: single quantum — the multi-page form workflow is HIGHLY semantically coupled (each page depends on previous context). This is a textbook example where distribution would create pain. Monolith is clearly appropriate. Organizational fit: 8 developers, no distributed experience, tight budget — this eliminates all distributed styles. Evaluated monolithic styles: Layered (high simplicity and low cost, handles the coupled workflow well), Pipeline (doesn't fit — forms aren't linear data transformations), Microkernel (doesn't fit — no plug-in/customization requirement). Anti-pattern check: watch for sinkhole anti-pattern as the app grows.
Output: **Layered architecture** recommended. The high semantic coupling of multi-page forms naturally fits a single deployment unit. Team size and experience align perfectly. Trade-off accepted: limited scalability and deployability — but these aren't driving characteristics. Trade-off rejected: Service-based was considered but adds unnecessary distribution complexity for a system with one quantum and a team without distributed experience. Explicit note: "highly coupled problem domain matches poorly with highly decoupled distributed architectures."

## References

- For detailed style ratings and profiles, see [references/style-comparison-matrix.md](references/style-comparison-matrix.md)
- For architecture characteristics identification, use `architecture-characteristics-identifier`
- For quantum analysis, use `architecture-quantum-analyzer`
- For distributed feasibility checking, use `distributed-feasibility-checker`
- For documenting the final decision, use `architecture-decision-record-creator`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-characteristics-identifier`
- `clawhub install bookforge-architecture-quantum-analyzer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
