# Risk Storming Facilitation Package: Event-Driven Architecture with Kafka — Unproven Technology

## Risk Dimension Selected: Unproven Technology

**WHY unproven technology:** When nobody on the team has used Kafka in production, this is automatically the highest-priority risk dimension. Per the unknown-technology rule, every Kafka-related component receives an automatic risk score of 9 (impact 3 x likelihood 3). The team cannot meaningfully assess likelihood for technology they've never operated — unknown unknowns are the most dangerous class of risk. All other dimensions (performance, availability, etc.) should be stormed AFTER the team has de-risked the technology through PoC and training.

## Architecture Components

Based on your event-driven architecture with Kafka, the following components will be assessed:

1. **Kafka Broker Cluster** — message storage and delivery infrastructure
2. **Event Producers** — services that publish events to Kafka topics
3. **Event Consumers** — services that subscribe to and process events from topics
4. **Schema Registry** — manages event schemas and compatibility
5. **Dead Letter Queues** — handles failed/unprocessable events
6. **Topic Management** — topic creation, partitioning, retention configuration
7. **Monitoring/Observability** — Kafka metrics, consumer lag, broker health

**CRITICAL:** Since nobody on the team has Kafka production experience, ALL of these components start at risk score 9. The risk storming session will focus on identifying WHICH specific unknowns pose the greatest operational danger and HOW to de-risk them.

> **HANDOFF TO HUMAN:** Validate this component list. Are there additional Kafka-related components in your architecture (e.g., Kafka Connect, Stream Processing, specific consumer groups)?

## Participants

Your stated participants: 4 senior developers + 2 tech leads = 6 people

| Role | Count | Specific Value for This Session |
|------|-------|---------------------------------|
| Senior developers | 4 | Will reveal specific knowledge gaps about Kafka operations |
| Tech leads | 2 | Bridge between architecture intent and operational readiness |

**WHY this mix works:** For an unproven-technology session, developers are the most critical participants. They'll be the ones operating Kafka at 3am when something breaks. Their honest assessment of "I don't know how to handle this" IS the risk identification. Each "I don't know" reveals a specific de-risking action item.

**Consider adding:** If you have any developer on the team (or accessible from other teams) who HAS used Kafka in production, invite them. Even a single experienced voice dramatically changes the risk profile.

## Pre-Work Materials

### Session Invitation

---

**Subject: Risk Storming Session — Kafka Adoption: Unproven Technology Risks**

Team,

We're running a risk storming session to collaboratively identify the risks of adopting Kafka in our event-driven architecture. Since none of us have used Kafka in production, this is an unproven-technology risk session.

**Risk dimension:** Unproven Technology
**Date:** [DATE]
**Time:** [TIME]
**Location:** [LOCATION/VIRTUAL LINK]

**What to do before the session:**

1. Review the attached architecture diagram showing all Kafka-related components
2. For EACH component, honestly assess what you DON'T know:
   - **Impact** (1-3): If this component fails or behaves unexpectedly, how severe?
   - **Likelihood** (1-3): How confident are you in your ability to operate this in production?
   - **Score** = Impact x Likelihood (1-9)
3. Prepare Post-it notes:
   - **Green** = Low risk (1-2) — you're confident about this
   - **Yellow** = Medium risk (3-4) — some uncertainty
   - **Red** = High risk (6-9) — significant unknowns
   - Write the score number on the Post-it

**Critical rule for this session:** If you don't know how something works or have never operated it, that's an automatic score of 9. This isn't a judgment of your skills — it's an honest assessment of operational risk. "I don't know" is the most valuable thing you can say in this session.

**Before the session, consider:**
- What happens when a Kafka broker goes down? Do you know the recovery procedure?
- What happens when a consumer falls behind and can't keep up?
- How do you handle schema evolution without breaking existing consumers?
- What happens when a partition rebalance occurs during a deployment?

---

### Risk Matrix Reference Card

```
RISK MATRIX — Unproven Technology Dimension

                    Likelihood of operational gap
                    Low (1)    Med (2)    High (3)
Impact    Low (1)  |   1    |    2    |    3    |
         Med (2)   |   2    |    4    |    6    |
        High (3)   |   3    |    6    |    9    |

SCORING KEY:
  1-2 = Low risk (GREEN)  — team is confident, documented procedures exist
  3-4 = Medium risk (YELLOW) — some knowledge, gaps need filling
  6-9 = High risk (RED) — significant unknowns, no production experience

CRITICAL RULE: If NOBODY on the team has production experience
with a component/technology, it is AUTOMATICALLY rated 9.
This is not negotiable — unknown unknowns are the most
dangerous class of risk.
```

### Individual Assessment Worksheet

```
INDIVIDUAL RISK ASSESSMENT — Unproven Technology (Kafka)
Participant: ________________________
Role: ________________________
Date: ________________________

For each component, honestly assess your team's operational readiness:

| Component               | Impact (1-3) | Likelihood (1-3) | Score | Post-it Color | "I don't know how to..." |
|------------------------|-------------|-----------------|-------|---------------|--------------------------|
| Kafka Broker Cluster   |             |                 |       |               |                          |
| Event Producers        |             |                 |       |               |                          |
| Event Consumers        |             |                 |       |               |                          |
| Schema Registry        |             |                 |       |               |                          |
| Dead Letter Queues     |             |                 |       |               |                          |
| Topic Management       |             |                 |       |               |                          |
| Monitoring/Observability|            |                 |       |               |                          |

The "I don't know how to..." column is the MOST IMPORTANT.
List specific operational scenarios you cannot handle today.

Examples:
- "I don't know how to recover from a broker failure"
- "I don't know how to handle consumer lag"
- "I don't know what happens during partition rebalancing"
```

> **HANDOFF TO HUMAN:** Send these materials to all 6 participants 1-2 days before the session.

## Session Agenda

```
RISK STORMING SESSION — Kafka Unproven Technology Risks
Duration: 90 minutes (extended for unproven-tech depth)

PHASE 2: CONSENSUS (45 minutes — extended because disagreements
         will center on "what we don't know we don't know")

[00:00-05:00]  Opening
               - "We're focused on UNPROVEN TECHNOLOGY risk"
               - Ground rule: "I don't know" is the most valuable
                 statement. This session is about honest assessment,
                 not demonstrating expertise.
               - Reminder: anything nobody has production experience
                 with = automatic 9

[05:00-15:00]  Post-it Placement
               - Each participant places their Post-its on the diagram
               - Expect lots of red (9) — that's correct and expected
               - No discussion yet

[15:00-40:00]  Disagreement Discussion (25 minutes)
               - Focus on areas where someone rates LOW while others
                 rate HIGH — does that person have genuine experience,
                 or are they being optimistic?
               - Focus on "I don't know how to..." items from worksheets
               - Use discussion guide questions below
               - Catalog every specific operational unknown

[40:00-45:00]  Consolidation
               - Agree on final ratings
               - The list of "I don't know" items becomes the
                 de-risking action plan

PHASE 3: MITIGATION (40 minutes — de-risking focus)

[45:00-60:00]  De-Risking Strategies
               - For each high-risk area: what would REDUCE the
                 unknowns? (PoC, training, vendor support, etc.)
               - NOT architecture changes — technology readiness actions

[60:00-75:00]  Operational Readiness Checklist
               - What must be true BEFORE going to production?
               - Runbook requirements for each Kafka component
               - Monitoring/alerting requirements

[75:00-85:00]  Action Items
               - Assign de-risking actions with owners and deadlines
               - Define decision gate: "We can go to production when..."

[85:00-90:00]  Wrap-up
               - Summarize unknowns and de-risking plan
               - Schedule follow-up risk storming AFTER de-risking
                 (expect scores to drop from 9 to 3-4 if actions complete)
```

## Discussion Guide

### For Knowledge Gap Assessment

**When exploring what the team doesn't know:**
- "Let's go component by component. For Kafka Broker Cluster: who can describe what happens when a broker goes down and how to recover? If nobody can, that's a 9."
- "For Event Consumers: what happens when a consumer falls behind by millions of messages? Who knows the procedure?"
- "For Schema Registry: how do we evolve event schemas without breaking existing consumers? Has anyone done this?"

**When someone rates a component LOW despite no production experience:**
- "You rated Topic Management as low risk (2). Have you managed Kafka topics in production before?"
- "What's your basis for that confidence? Is it from reading docs, a tutorial, or production experience?"
- "Keep in mind: knowing HOW something works conceptually is different from having OPERATED it under failure conditions."

**When identifying the most dangerous unknowns:**
- "Of all the 'I don't know' items we've listed, which ONE would cause the most damage if it happened at 3am on a Saturday?"
- "What happens during a Kafka partition rebalance while we're deploying a new version of a consumer?"
- "If Kafka loses messages, how do we detect it? How do we recover?"

### For De-Risking (Mitigation Phase)

- "What is the minimum PoC that would validate we can operate Kafka in production?"
- "Should we run a parallel system (Kafka + existing messaging) during the transition?"
- "Does our Kafka vendor or managed service provide an SLA? What support options exist?"
- "What training does the team need before we're production-ready?"
- "What runbooks must exist before we go live?"
- "What is our rollback strategy if Kafka proves unworkable?"

## Mitigation Record Template (De-Risking Focus)

```markdown
## De-Risking Record — Kafka Adoption

### Unknown: {specific operational gap}
- **Component:** {which Kafka component}
- **Consensus Risk Score:** {score} (likely 9 for most items)
- **Identified by:** {participant names}
- **"I don't know how to...":** {specific operational scenario}

### De-Risking Actions
- **Action 1:** {PoC / training / vendor engagement / etc.}
  - Owner: {name}
  - Deadline: {date}
  - Success criteria: {how we know this risk is reduced}
  - Expected post-action score: {target — aim for 3-4}

- **Action 2 (if needed):** {additional de-risking}

### Production Readiness Gate
- [ ] Runbook exists for this scenario
- [ ] Monitoring/alerting covers this failure mode
- [ ] At least one team member has hands-on experience
- [ ] Rollback procedure documented and tested
```

> **HANDOFF TO HUMAN:** Use this template during the session. The "I don't know how to..." column is the most important input — it directly generates the de-risking action plan.

## Next Steps Recommendation

1. **Immediate:** Execute de-risking actions from this session (PoCs, training, vendor support)
2. **After de-risking complete:** Re-storm the same dimension (unproven technology) to verify scores dropped from 9 to acceptable levels (3-4)
3. **Then:** Storm performance dimension — Kafka throughput and latency under your specific load patterns
4. **Then:** Storm availability dimension — Kafka cluster resilience, consumer group failover
5. **Decision gate:** Do NOT go to production until re-storm scores are below 6 for all Kafka components
