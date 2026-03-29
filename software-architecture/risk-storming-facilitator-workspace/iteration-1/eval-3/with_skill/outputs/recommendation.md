# Risk Storming Facilitation Package: API Gateway Performance — 10,000 req/s

## Risk Dimension Selected: Performance

**WHY performance:** The user explicitly identified performance concerns with an API gateway handling 10,000 requests/second. When specific performance numbers are cited, it signals an active concern that needs immediate collaborative analysis. Performance at this scale has non-obvious failure modes that individual architects miss — bottlenecks cascade, and the component that fails first under load is often not the one expected.

## Architecture Components

Based on your API gateway system handling 10,000 req/s, the following components will be assessed for performance risk:

1. **Load Balancer** — distributes incoming traffic across gateway instances
2. **API Gateway Instances** — request routing, protocol translation
3. **Rate Limiter** — throttling and quota enforcement
4. **Authentication/Authorization Middleware** — token validation, permission checks per request
5. **Request Router** — path-based routing to upstream services
6. **Response Cache** — caching layer for frequently requested responses
7. **Logging/Metrics Pipeline** — request logging and observability at high throughput
8. **Upstream Service Connections** — connection pools to backend services

> **HANDOFF TO HUMAN:** Validate this component list. Does your API gateway have additional middleware (e.g., request transformation, schema validation, WAF)? At 10,000 req/s, every component in the request path matters.

## Participants

Your stated team: 8 people from the platform team.

**Recommendation:** All 8 should participate, since they all own or interact with the API gateway. For a performance session, include:

| Role | Value for This Session |
|------|-----------------------|
| Gateway developers | Know where the code-level bottlenecks are |
| Platform/infra engineers | Know the infrastructure limits and scaling behavior |
| Performance/SRE engineers | Have load testing experience and production latency data |
| Tech leads | Understand the end-to-end request path and where latency accumulates |

**WHY full team:** At 10,000 req/s, performance bottlenecks often exist at layer boundaries — between the load balancer and gateway, between auth middleware and the router, between the cache and upstream services. Different team members own different layers and see different bottlenecks. The full team sees the full picture.

## Pre-Work Materials

### Session Invitation

---

**Subject: Risk Storming Session — API Gateway Performance at 10,000 req/s**

Platform Team,

We're running a risk storming session to collaboratively identify performance risks in our API gateway. Current throughput: 10,000 requests/second.

**Risk dimension:** Performance (latency, throughput, response time under load)
**Date:** [DATE]
**Time:** [TIME]
**Location:** [LOCATION/VIRTUAL LINK]

**What to do before the session:**

1. Review the attached architecture diagram of the API gateway request path
2. For EACH component in the request path, individually assess:
   - **Impact** (1-3): How severe if this component becomes a performance bottleneck?
   - **Likelihood** (1-3): How probable is it at 10,000 req/s (or higher)?
   - **Score** = Impact x Likelihood (1-9)
3. Prepare Post-it notes:
   - **Green** = Low risk (1-2) — this component handles the load comfortably
   - **Yellow** = Medium risk (3-4) — might struggle under peak load
   - **Red** = High risk (6-9) — known or likely bottleneck at current/projected load

**Think about these questions as you assess:**
- At 10,000 req/s, which component hits its capacity limit FIRST?
- What happens to p99 latency when the response cache has a miss?
- Is there a synchronous call in the request path that blocks at high concurrency?
- What happens at 2x load (20,000 req/s) — what breaks first?
- Are there any components where performance degrades non-linearly?

If you have load testing data, bring it. Actual measurements beat estimates.

---

### Risk Matrix Reference Card

```
RISK MATRIX — Performance Dimension

                    Likelihood of bottleneck at 10k+ req/s
                    Low (1)    Med (2)    High (3)
Impact    Low (1)  |   1    |    2    |    3    |
         Med (2)   |   2    |    4    |    6    |
        High (3)   |   3    |    6    |    9    |

SCORING KEY:
  1-2 = Low risk (GREEN)  — component handles load, performance is acceptable
  3-4 = Medium risk (YELLOW) — may degrade under peak or growth scenarios
  6-9 = High risk (RED) — known or likely bottleneck, needs architectural change

Think IMPACT first: "If this component becomes a bottleneck, how bad is it?"
Then LIKELIHOOD: "At 10,000 req/s (and growing), how probable?"

CRITICAL RULE: Unknown/unproven technology = automatic 9
```

### Individual Assessment Worksheet

```
INDIVIDUAL RISK ASSESSMENT — Performance (API Gateway, 10k req/s)
Participant: ________________________
Role: ________________________
Date: ________________________

For each component, assess performance risk at 10,000 req/s:

| Component                  | Impact (1-3) | Likelihood (1-3) | Score | Post-it Color | Bottleneck Hypothesis |
|---------------------------|-------------|-----------------|-------|---------------|-----------------------|
| Load Balancer             |             |                 |       |               |                       |
| API Gateway Instances     |             |                 |       |               |                       |
| Rate Limiter              |             |                 |       |               |                       |
| Auth Middleware           |             |                 |       |               |                       |
| Request Router            |             |                 |       |               |                       |
| Response Cache            |             |                 |       |               |                       |
| Logging/Metrics Pipeline  |             |                 |       |               |                       |
| Upstream Connections      |             |                 |       |               |                       |

"Bottleneck Hypothesis" — describe WHERE in this component
performance would degrade and WHY (e.g., "Auth makes a
synchronous DB call per request — at 10k req/s that's 10k
DB queries/second for auth alone").

Current load testing data (if available):
- p50 latency: ______ ms
- p99 latency: ______ ms
- Max throughput tested: ______ req/s
- First component to degrade: ______________________
```

> **HANDOFF TO HUMAN:** Send these materials to all 8 platform team members 1-2 days before the session.

## Session Agenda

```
RISK STORMING SESSION — API Gateway Performance (10k req/s)
Duration: 90 minutes (full duration for technical depth at scale)

PHASE 2: CONSENSUS (40 minutes)

[00:00-05:00]  Opening
               - "We're focused on PERFORMANCE at 10,000 req/s"
               - Share any load testing data available
               - Ground rules: every Post-it goes up, disagree openly,
                 bring data when you have it

[05:00-15:00]  Post-it Placement
               - All 8 participants place their Post-its on the
                 request path diagram
               - At this scale, expect Post-its clustered around
                 auth, caching, and upstream connections

[15:00-35:00]  Disagreement Discussion (20 minutes)
               - Where ratings differ: "You think auth is the
                 bottleneck, you think it's the cache — let's dig in"
               - Where only one person sees risk: unique bottleneck
                 knowledge
               - Use load testing data to resolve disputes where possible
               - Use discussion guide questions below

[35:00-40:00]  Consolidation
               - Agree on final ratings
               - Rank the bottleneck chain: which component fails FIRST?

PHASE 3: MITIGATION (40 minutes)

[40:00-55:00]  Mitigation Brainstorm
               - For each high-risk component: what change reduces
                 the performance risk?
               - Consider: caching, async processing, connection pooling,
                 horizontal scaling, protocol optimization

[55:00-70:00]  Cost-Benefit Analysis
               - Estimate effort for each mitigation
               - Estimate performance improvement (e.g., "connection
                 pooling could reduce upstream latency by 40%")
               - Prioritize: highest performance gain per effort

[70:00-80:00]  Validation Plan
               - For each mitigation: how do we VERIFY it worked?
               - Load testing requirements, target metrics
               - Define performance SLOs

[80:00-85:00]  Action Items
               - Assign owners and deadlines
               - Schedule load testing sessions

[85:00-90:00]  Wrap-up
               - Summarize bottleneck chain and mitigation plan
               - Schedule next session: recommend SCALABILITY dimension
                 (what happens at 2x-5x growth?)
```

## Discussion Guide

### For Bottleneck Identification

**When participants disagree on WHERE the bottleneck is:**
- "You rated Auth Middleware as high risk (9) and you rated it as low (2). Do we have latency data for auth at peak load?"
- "What happens to auth latency when you have 10,000 concurrent token validations? Is there a database call, an in-memory check, or a remote auth service call?"
- "Let's trace a request through the full path — where does the most time accumulate?"

**When exploring non-obvious bottlenecks:**
- "What about the Logging Pipeline — at 10,000 req/s, that's 10,000 log entries per second. Is logging synchronous or async?"
- "How big is the connection pool to upstream services? At 10,000 req/s, are we exhausting connections?"
- "What happens when the Response Cache has a miss? Does p99 spike because cache misses hit the backend synchronously?"

### For Load Testing Gaps

- "What's the highest throughput we've actually tested? If it's 5,000 req/s, we're extrapolating for the remaining 5,000."
- "Do we have p99 latency data, not just p50? The tail latency is where performance risks hide."
- "Have we tested with realistic traffic patterns, or just uniform load? Real traffic has bursts."

### For Mitigation Phase

- "What architecture change would reduce this bottleneck? Can we quantify the improvement?"
- "Is this a 'throw more hardware at it' fix, or does it require a design change?"
- "What is the cost: development time, complexity, operational burden?"
- "How do we verify the mitigation worked? What load test proves it?"
- "What performance SLO should we set for this component? p99 < X ms at 10k req/s?"

## Mitigation Record Template (Performance-Specific)

```markdown
## Performance Risk Mitigation Record — API Gateway

### Bottleneck: {component}
- **Consensus Risk Score:** {score} ({impact} x {likelihood})
- **Current performance:** p50 = {X}ms, p99 = {Y}ms at {Z} req/s
- **Bottleneck type:** {CPU-bound / IO-bound / connection-limited / memory-limited}

### Proposed Mitigation
- **Change:** {specific architecture/config change}
- **Expected improvement:** {e.g., "p99 from 200ms to 50ms" or "throughput from 10k to 25k req/s"}
- **Expected post-mitigation risk score:** {new score}
- **Estimated effort:** {dev days/hours}
- **Alternative (if effort too high):** {simpler partial fix}
- **Owner:** {name}
- **Deadline:** {date}
- **Validation:** {how to verify — load test, metrics, etc.}

### Performance SLO
- p99 latency target: {X}ms at {Y} req/s
- Throughput target: {X} req/s sustained
- Error rate target: < {X}% at target throughput
```

> **HANDOFF TO HUMAN:** Use this template during the session. The performance-specific fields (current metrics, expected improvement, SLOs) make the mitigation discussions concrete and measurable.

## Next Steps Recommendation

1. **After this session:** Execute load tests to validate current baselines and verify any assumptions made during risk storming
2. **Next risk storming session:** Scalability dimension — "What happens at 20,000 req/s? 50,000? Where does the architecture fundamentally break?"
3. **Then:** Availability dimension — "What happens if the gateway itself goes down? What about upstream service failures?"
4. **Ongoing:** Re-storm performance after implementing mitigations to verify improvements and check for new bottlenecks
5. **Performance gate:** Define SLOs before going live and use them as fitness functions for continuous monitoring
