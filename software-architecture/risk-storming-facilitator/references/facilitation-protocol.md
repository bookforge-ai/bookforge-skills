# Risk Storming Facilitation Protocol

> Detailed protocol for running the three-phase risk storming exercise.
> Read this when you need timing details, role assignments, or virtual session adaptations.

## Overview

Risk storming has three phases executed in strict order:

| Phase | Name | Mode | Duration | Purpose |
|-------|------|------|----------|---------|
| 1 | Identification | Individual (noncollaborative) | 1-2 days before session | Each participant independently rates risks |
| 2 | Consensus | Collaborative (all together) | 30-40 minutes | Align on risk ratings through disagreement discussion |
| 3 | Mitigation | Collaborative (all together) | 20-40 minutes | Identify architecture changes and negotiate costs |

**Total session time:** 60-90 minutes (Phases 2 and 3 only; Phase 1 is async pre-work)

## Phase 1: Identification (Pre-Session, Noncollaborative)

### Timing
- Send invitation **1-2 days** before the collaborative session
- Participants complete individual assessment **before** arriving at the session

### What the Facilitator Sends

1. **Architecture diagram** — a clear visual of the system's components and connections. Use the most current version. For in-person sessions, print a large version (A1/A0) for wall posting. For virtual sessions, share a digital version that participants can annotate.

2. **Risk dimension** — the ONE dimension being assessed. State it explicitly:
   - "This session focuses on **availability** risk"
   - NOT "assess all the risks you can think of"

3. **Risk matrix reference:**
   ```
   Likelihood of risk occurring
                    Low(1)  Med(2)  High(3)
   Impact  Low(1)  |  1  |  2  |  3  |
          Med(2)   |  2  |  4  |  6  |
         High(3)   |  3  |  6  |  9  |

   1-2 = Low risk (GREEN Post-it)
   3-4 = Medium risk (YELLOW Post-it)
   6-9 = High risk (RED Post-it)

   RULE: Unknown/unproven technology = automatic 9
   ```

4. **Individual assessment instructions:**
   - Review the architecture diagram
   - For each component, assess impact and likelihood for the given risk dimension
   - Calculate the composite score (impact x likelihood)
   - Prepare Post-it notes: one per risk area identified
   - Write the score on the Post-it and use the matching color (green/yellow/red)
   - If multiple dimensions are being assessed in one session (not recommended), write the dimension name next to the score

### Why Noncollaborative First

The individual phase MUST be noncollaborative to prevent:
- **Anchoring bias** — one vocal person's assessment dominates everyone's thinking
- **Groupthink** — participants converge on "safe" ratings to avoid conflict
- **Knowledge hiding** — junior developers may not speak up in front of senior architects

When each person arrives with their own independent assessment, the differences between assessments become the most valuable data in the session.

## Phase 2: Consensus (Collaborative, 30-40 Minutes)

### Setup (5 minutes)
- Post the architecture diagram on the wall (or display on a large screen)
- Restate the risk dimension: "Today we're focusing on {dimension}"
- Ground rules:
  - Every Post-it goes on the diagram, no matter how "wrong" it might seem
  - We discuss disagreements, not agreements
  - No rank pulls — a developer's risk assessment is as valid as an architect's

### Post-it Placement (10 minutes)
- Each participant places their Post-it notes on the architecture diagram at the location where they identified risk
- For virtual sessions: the facilitator collects each participant's risks and places them on the shared digital diagram
- Do NOT discuss yet — just place

### Reading the Diagram
After placement, the facilitator identifies areas of interest:

| Pattern | What it means | Action |
|---------|---------------|--------|
| Multiple Post-its, same color, same area | Agreement — everyone sees the same risk | Brief confirmation, move on quickly |
| Multiple Post-its, DIFFERENT colors, same area | Disagreement — someone knows something others don't | **This is where you spend time** |
| Single Post-it on an area | One person sees a risk no one else identified | Explore — this person may have unique knowledge |
| No Post-its on an area | Everyone agrees there's no significant risk | Note and move on |

### Disagreement Discussion (15-20 minutes)

This is the highest-value part of the entire exercise. Spend **60% of consensus time** here.

**For each disagreement area, ask:**

1. Start with the outlier: "You rated {component} as {high risk}. The rest of us rated it {low/medium}. What do you see that we're missing?"
2. Probe for experience: "Have you encountered this type of failure before? In what context?"
3. Check for unknown unknowns: "Is there something about {component}'s implementation that changes the risk picture?"
4. Resolve: after discussion, the group agrees on a consolidated rating

**Example from the book (ELB disagreement):**
- Two participants: medium risk (3) for the Elastic Load Balancer
- One participant: high risk (6)
- The outlier explains: "If the ELB goes down, the ENTIRE system is inaccessible"
- Group agrees: yes, impact is high (3), but likelihood is low (1) because ELBs are highly available
- Consolidated rating: medium (3)
- Insight gained: the third participant revealed an availability concern the others hadn't considered

**Example from the book (Redis cache, unknown technology):**
- One participant: high risk (9) for Redis cache
- All other participants: no risk identified
- The outlier explains: "What is Redis? I've never heard of it."
- Per the unknown-technology rule: automatic 9
- Insight: this reveals a team knowledge gap that IS a risk, regardless of Redis's actual reliability

### Consolidation (5 minutes)
- Remove duplicate Post-its
- Replace disagreement clusters with a single Post-it showing the agreed score
- The final diagram should have one Post-it per risk area with the consensus score

## Phase 3: Mitigation (Collaborative, 20-40 Minutes)

### Mitigation Brainstorm (15-20 minutes)

For each high-risk area (score 6-9), the group identifies architecture changes that would reduce the risk.

**Key questions:**
- "What architecture change would reduce this from {current score} to an acceptable level?"
- "Can we reduce the impact, the likelihood, or both?"
- "Are there proven patterns that address this type of risk?" (e.g., circuit breakers for availability, message queues for throughput)

**Common mitigation patterns by dimension:**

| Dimension | Common mitigations |
|-----------|-------------------|
| Availability | Database clustering, service replication, circuit breakers, fallback services, SLA/SLO verification for external dependencies |
| Performance | Caching layers, async processing, queue-based load leveling, CDN, connection pooling |
| Scalability | Horizontal scaling, event-driven decoupling, database sharding, read replicas |
| Security | API gateway splitting by role, network segmentation, encryption at rest/in transit, authentication/authorization layers |
| Data integrity | Database replication, write-ahead logging, idempotent operations, backup strategies |
| Unproven tech | PoC with production load, team training, vendor support, rollback strategy, parallel run with proven alternative |

### Cost Negotiation (10-15 minutes)

Every mitigation has a cost. The facilitator helps the group negotiate:

1. **Present the full mitigation:** "Database clustering plus splitting into separate physical databases would reduce risk from 6 to 2. Estimated cost: $20,000."

2. **If stakeholder rejects:** "What about splitting the database without clustering? Cost drops to $8,000, and we still mitigate most of the risk (from 6 to 3)."

3. **Document the trade-off:** Record both options, their costs, and the risk reduction each provides.

**Why this matters:** The book's database clustering example shows the real-world negotiation: $20,000 for full mitigation was rejected, but $8,000 for partial mitigation was accepted. Having a cheaper alternative ready is a facilitation skill that prevents "all or nothing" outcomes.

### Action Items (5 minutes)
- Each agreed mitigation gets an owner and a deadline
- Document in the mitigation record template
- Schedule the next risk storming session (different dimension)

## Virtual Session Adaptations

When running risk storming remotely:

| In-Person | Virtual Equivalent |
|-----------|-------------------|
| Large printed architecture diagram on wall | Shared digital diagram (Miro, FigJam, Lucidchart) |
| Physical Post-it notes (green/yellow/red) | Digital sticky notes with color coding |
| Participants walk up and place Post-its | Facilitator collects risks from each participant and places them, OR participants annotate directly |
| Verbal discussion around the diagram | Video call with screen sharing |
| Writing on Post-its during discussion | Updating digital stickies in real-time |

**Critical adaptation:** In virtual sessions, the facilitator must be more active in soliciting input from quiet participants. The "walk up and place Post-its" physical action forces participation; digital sessions need the facilitator to call on each person directly.

## Timing Guide by Team Size

| Team Size | Phase 2 (Consensus) | Phase 3 (Mitigation) | Total |
|-----------|---------------------|----------------------|-------|
| 3-4 people | 25 minutes | 20 minutes | 45 minutes |
| 5-6 people | 35 minutes | 25 minutes | 60 minutes |
| 7-8 people | 40 minutes | 30 minutes | 70 minutes |
| 9+ people | 45 minutes | 35 minutes | 80 minutes |

For teams larger than 8, consider splitting into two parallel sessions with different facilitators, then merging findings.

## Common Facilitation Mistakes

| Mistake | Why it fails | Correction |
|---------|-------------|------------|
| Assessing multiple dimensions in one session | Participants lose focus, conflate risk types | One dimension per session |
| Skipping Phase 1 (individual assessment) | Anchoring bias dominates, fewer risks discovered | Always do individual assessment BEFORE the collaborative session |
| Spending equal time on agreements and disagreements | Agreements don't reveal new information | Spend 60% of time on disagreements |
| Only inviting architects | Misses implementation-level risks | Include senior developers and tech leads |
| Treating it as a one-time event | Architecture risk changes continuously | Schedule recurring sessions, especially after major changes |
| Proposing only one mitigation option | Stakeholders reject expensive options and nothing happens | Always have a cheaper alternative ready |
