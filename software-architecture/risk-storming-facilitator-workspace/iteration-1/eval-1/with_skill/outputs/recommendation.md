# Risk Storming Facilitation Package: Microservices Payment System — Availability

## Risk Dimension Selected: Availability

**WHY availability first:** You're about to go live, which means availability is the highest-stakes dimension — if the system goes down in production, it's immediately visible to customers and directly impacts revenue. Performance and security are important but can be addressed post-launch with less disruption. Availability failures at launch are catastrophic.

## Architecture Components

Based on your microservices payment system, the following components will be assessed:

1. **API Gateway** — entry point for all client requests, routes to downstream services
2. **Payment Processor Service** — handles payment transactions, communicates with external payment providers
3. **Order Service** — manages order lifecycle and state
4. **User/Account Service** — authentication, user profiles, account management
5. **Notification Service** — sends emails, SMS, push notifications for payment confirmations
6. **Database(s)** — persistent storage for transactions, orders, user data

> **HANDOFF TO HUMAN:** Validate this component list is complete. Are there load balancers, message queues, caches, or third-party integrations I'm missing?

## Recommended Participants

| Role | Count | Why |
|------|-------|-----|
| Lead architect | 1 | High-level structural perspective on availability design |
| Senior backend developers | 3 | Implementation-level knowledge of failure modes and edge cases |
| Platform/DevOps tech lead | 1 | Operational perspective on deployment, monitoring, and recovery |
| SRE or on-call engineer | 1 | Real-world experience with availability incidents |

**Total: 6 participants**

**WHY include developers and SREs:** Architects design for availability, but developers know where the implementation shortcuts are, and SREs know which components actually fail in production. A developer might rate the database as high risk because they know the connection pool configuration is fragile — a risk the architect would miss.

## Pre-Work Materials

### Session Invitation (send 1-2 days before)

---

**Subject: Risk Storming Session — Payment System Availability**

Team,

We're running a risk storming session to collaboratively identify availability risks in our payment system before launch.

**Risk dimension:** Availability (uptime, resilience to component failures, impact of outages)
**Date:** [DATE]
**Time:** [TIME]
**Location:** [LOCATION/VIRTUAL LINK]

**What to do before the session:**

1. Review the attached architecture diagram
2. For EACH component, individually assess:
   - **Impact** (1-3): How severe if this component goes down?
   - **Likelihood** (1-3): How probable is a failure?
   - **Score** = Impact x Likelihood (1-9)
3. Prepare Post-it notes for each risk you identify:
   - **Green** = Low risk (1-2)
   - **Yellow** = Medium risk (3-4)
   - **Red** = High risk (6-9)
   - Write the score number on the Post-it

**Important rules:**
- Do this assessment INDIVIDUALLY — do not discuss with teammates beforehand
- For any technology you haven't used in production, assign automatic score 9
- Focus ONLY on availability — not performance, security, or other dimensions

See the attached risk matrix reference card for scoring details.

---

### Risk Matrix Reference Card

```
RISK MATRIX — Availability Dimension

                    Likelihood of failure
                    Low (1)    Med (2)    High (3)
Impact    Low (1)  |   1    |    2    |    3    |
         Med (2)   |   2    |    4    |    6    |
        High (3)   |   3    |    6    |    9    |

SCORING KEY:
  1-2 = Low risk (GREEN)  — monitor, no action needed
  3-4 = Medium risk (YELLOW) — plan mitigation
  6-9 = High risk (RED) — requires architectural change

CRITICAL RULE: Unknown/unproven technology = automatic 9
Assess IMPACT first, then LIKELIHOOD.
```

### Individual Assessment Worksheet

```
INDIVIDUAL RISK ASSESSMENT — Availability
Participant: ________________________
Date: ________________________

For each component, assess availability risk:

| Component               | Impact (1-3) | Likelihood (1-3) | Score | Post-it Color |
|------------------------|-------------|-----------------|-------|---------------|
| API Gateway            |             |                 |       |               |
| Payment Processor      |             |                 |       |               |
| Order Service          |             |                 |       |               |
| User/Account Service   |             |                 |       |               |
| Notification Service   |             |                 |       |               |
| Database(s)            |             |                 |       |               |
| [External Payment API] |             |                 |       |               |

Notes / rationale for high-risk ratings:
_____________________________________________
_____________________________________________
```

> **HANDOFF TO HUMAN:** Send these materials to all participants 1-2 days before the session.

## Session Agenda

```
RISK STORMING SESSION — Payment System Availability
Duration: 75 minutes

PHASE 2: CONSENSUS (35 minutes)
[00:00-05:00]  Opening
               - Restate dimension: "We're focused on AVAILABILITY"
               - Ground rules: every Post-it goes on the diagram,
                 we discuss disagreements, rank doesn't matter

[05:00-15:00]  Post-it Placement
               - Each participant places their color-coded Post-its
                 on the architecture diagram
               - No discussion yet — just place

[15:00-30:00]  Disagreement Discussion (MOST IMPORTANT)
               - Identify areas where ratings differ
               - Focus on: where one person sees high risk and
                 another sees low/none
               - Focus on: single-person risks (only one identified it)
               - Use discussion guide questions (see below)

[30:00-35:00]  Consolidation
               - Agree on final ratings for each risk area
               - Replace disagreement clusters with single consensus Post-its

PHASE 3: MITIGATION (35 minutes)
[35:00-50:00]  Mitigation Brainstorm
               - For each high-risk area (6-9): what architecture
                 change would reduce the risk?
               - Consider: redundancy, failover, circuit breakers,
                 database clustering, SLA verification

[50:00-65:00]  Cost Negotiation
               - Estimate cost of each mitigation
               - If too expensive: propose cheaper alternative
                 that partially mitigates
               - Document trade-offs

[65:00-70:00]  Action Items
               - Assign owner and deadline for each agreed mitigation

[70:00-75:00]  Wrap-up
               - Summarize findings
               - Schedule next session (recommend: PERFORMANCE dimension)
```

## Discussion Guide

### For Disagreement Areas

**When ratings differ by 2+ points:**
- "You rated the Payment Processor as high risk (6) for availability, while you rated it low (2). Can each of you explain your reasoning?"
- "What information or experience led you to that score?"
- "Is there something about the deployment or infrastructure that changes the availability picture?"

**When only one person identified a risk:**
- "You're the only one who flagged the Database as an availability risk. What do you see that we might be missing?"
- "Have you experienced database outages in similar systems?"

### For External Dependencies (Payment Providers)

- "What is the SLA for our external payment provider? Has anyone verified it?"
- "If the payment provider goes down, does our entire payment flow stop, or do we have a fallback?"
- "What is the blast radius if this external dependency becomes unavailable?"

### For Single Points of Failure

- "Is the API Gateway a single point of failure? If it goes down, can any traffic reach any service?"
- "Are our databases clustered? If not, what happens if the primary fails?"
- "Do we have health checks and circuit breakers in place between services?"

### For Mitigation Phase

- "What architecture change would reduce this availability risk from {current} to {target}?"
- "What would that cost — in money, development time, and added complexity?"
- "Is there a cheaper option that gets us 80% of the risk reduction?"
- "Can we verify the external payment provider's SLA before launch instead of assuming it's reliable?"

## Mitigation Record Template

```markdown
## Risk Mitigation Record — Payment System Availability

### Risk Area: {Component} — Availability
- **Consensus Risk Score:** {score} ({impact} x {likelihood})
- **Identified by:** {participant names}
- **Rationale:** {why this risk level}

### Proposed Mitigation
- **Change:** {specific architecture change}
- **Expected post-mitigation score:** {new score}
- **Estimated cost:** ${amount} / {dev hours}
- **Alternative (if cost rejected):** {cheaper partial mitigation}
- **Alternative cost:** ${amount} / {dev hours}
- **Owner:** {name}
- **Deadline:** {date — ideally before launch}
- **Status:** Proposed / Approved / Implemented
```

> **HANDOFF TO HUMAN:** Use this template to document each mitigation during the session. The agent cannot facilitate the live discussion — the human runs the session using these materials.

## Next Steps Recommendation

After this availability session:
1. **Next risk storming session:** Performance dimension (especially critical for a payment system under load)
2. **Timing:** 1-2 weeks after implementing availability mitigations
3. **After launch:** Security dimension (payment data protection, PCI compliance considerations)
4. **Ongoing:** Re-storm availability after any major architecture changes or incidents
