# Risk Storming Facilitator — Iteration 1 Grading

## Assertions

### Structural Assertions

| ID | Assertion | Description |
|----|-----------|-------------|
| S1 | has-three-phases | Describes the three phases: Identification (individual), Consensus (collaborative), Mitigation (collaborative) |
| S2 | has-session-agenda | Includes a timed session agenda with specific time allocations |
| S3 | has-pre-work-materials | Includes pre-work materials to send to participants 1-2 days before |
| S4 | has-participant-guidance | Recommends specific participant roles (architects, senior developers, tech leads) |
| S5 | has-risk-dimension-selection | Guides the user to select ONE risk dimension per session |
| S6 | has-mitigation-template | Provides a template for documenting mitigations with cost negotiation fields |

### Value Assertions

| ID | Assertion | Description |
|----|-----------|-------------|
| V1 | phase1-noncollaborative | Explicitly states Phase 1 must be individual/noncollaborative to prevent anchoring bias |
| V2 | focuses-on-disagreements | Directs the facilitator to spend most consensus time on disagreements, not agreements |
| V3 | one-dimension-per-session | Recommends restricting each session to a single risk dimension for focused results |
| V4 | includes-developers | Recommends including senior developers and tech leads, not just architects |
| V5 | cost-negotiation-with-alternatives | Mitigation phase includes cost negotiation with cheaper alternative options |
| V6 | unknown-tech-rule | States unproven/unknown technologies automatically receive highest risk rating (9) |
| V7 | continuous-not-one-time | Frames risk storming as a continuous practice, not a one-time event |
| V8 | color-coded-post-its | Uses color-coded Post-it notes (green/yellow/red) placed on architecture diagrams |

---

## Eval 1: Pre-launch availability risk storming for microservices payment system

**Prompt:** "We're about to go live with a new microservices-based payment system. I want to do a risk assessment with my team before launch. Can you help me plan a risk storming session focused on availability?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|-------|----------|
| S1: has-three-phases | PASS | Describes Phase 1 (individual pre-work), Phase 2 (Consensus, 35min), Phase 3 (Mitigation, 35min) with clear phase transitions |
| S2: has-session-agenda | PASS | Detailed 75-minute timed agenda with minute-by-minute breakdown for both phases |
| S3: has-pre-work-materials | PASS | Complete invitation, risk matrix reference card, individual assessment worksheet — sent 1-2 days before |
| S4: has-participant-guidance | PASS | Specific roles: lead architect (1), senior backend devs (3), platform/DevOps tech lead (1), SRE (1) |
| S5: has-risk-dimension-selection | PASS | Explicitly selects availability with WHY reasoning for why it's the right first dimension pre-launch |
| S6: has-mitigation-template | PASS | Structured template with cost fields, alternative mitigation, owner, deadline, status |
| V1: phase1-noncollaborative | PASS | Pre-work is explicitly individual, instructions say "do not discuss with teammates beforehand" |
| V2: focuses-on-disagreements | PASS | Agenda allocates 15 minutes to "Disagreement Discussion (MOST IMPORTANT)" with specific questions |
| V3: one-dimension-per-session | PASS | Session focuses solely on availability; recommends performance and security as follow-up sessions |
| V4: includes-developers | PASS | Includes 3 senior backend developers and 1 SRE beyond the architect; explains WHY with concrete example |
| V5: cost-negotiation-with-alternatives | PASS | Mitigation template has "Alternative (if cost rejected)" field with alternative cost |
| V6: unknown-tech-rule | PASS | Risk matrix reference card states "Unknown/unproven technology = automatic 9" |
| V7: continuous-not-one-time | PASS | Next Steps recommends follow-up sessions for different dimensions and re-storming after changes |
| V8: color-coded-post-its | PASS | Worksheet and invitation specify green (1-2), yellow (3-4), red (6-9) Post-it notes with score numbers |

**Score: 14/14 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|-------|----------|
| S1: has-three-phases | FAIL | Describes 3 meeting parts (brainstorm, prioritize, plan) but not the specific three-phase protocol; no individual pre-work phase |
| S2: has-session-agenda | PARTIAL | Has a 1-hour agenda with time blocks but lacks minute-level detail and phase structure |
| S3: has-pre-work-materials | FAIL | No pre-work materials; everything happens in the meeting |
| S4: has-participant-guidance | FAIL | Says "invite relevant stakeholders, developers, and architects" — no specific role mix |
| S5: has-risk-dimension-selection | FAIL | Does not mention the concept of focusing on one dimension; discusses availability broadly |
| S6: has-mitigation-template | PARTIAL | Has a basic table but no cost negotiation fields or alternative mitigation |
| V1: phase1-noncollaborative | FAIL | No individual pre-work phase; all assessment happens collaboratively in the meeting |
| V2: focuses-on-disagreements | FAIL | No mention of focusing on disagreements; treats risk identification as open brainstorming |
| V3: one-dimension-per-session | FAIL | No concept of single-dimension sessions |
| V4: includes-developers | FAIL | Generic "invite relevant stakeholders, developers, and architects" without WHY reasoning |
| V5: cost-negotiation-with-alternatives | FAIL | No cost negotiation process or cheaper alternative concept |
| V6: unknown-tech-rule | FAIL | No mention of the unknown-technology rule or automatic risk score 9 |
| V7: continuous-not-one-time | FAIL | No mention of risk storming as continuous practice |
| V8: color-coded-post-its | FAIL | No Post-it notes, no color coding, no placement on architecture diagrams |

**Score: 1/14 (7%) — counting 2 PARTIALs as 0.5 each**

---

## Eval 2: Unproven technology risk storming for Kafka adoption

**Prompt:** "Our team just adopted a new event-driven architecture using Kafka. Nobody on the team has used Kafka in production before. I want to facilitate a risk discussion with the 4 senior developers and 2 tech leads. How should I structure this?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|-------|----------|
| S1: has-three-phases | PASS | Phase 1 (individual pre-work), Phase 2 (Consensus, 45min extended), Phase 3 (Mitigation/de-risking, 40min) |
| S2: has-session-agenda | PASS | 90-minute timed agenda with extended disagreement discussion time for unproven-tech sessions |
| S3: has-pre-work-materials | PASS | Invitation, risk matrix card, individual worksheet with "I don't know how to..." column |
| S4: has-participant-guidance | PASS | Validates the 4 devs + 2 tech leads; recommends adding anyone with Kafka production experience |
| S5: has-risk-dimension-selection | PASS | Explicitly selects "Unproven Technology" with WHY (nobody has production experience = highest priority) |
| S6: has-mitigation-template | PASS | De-risking focused template with production readiness gate checklist |
| V1: phase1-noncollaborative | PASS | Pre-work states "I don't know is the most valuable statement"; individual honest assessment |
| V2: focuses-on-disagreements | PASS | 25 minutes for disagreement discussion; probes when someone rates LOW despite no experience |
| V3: one-dimension-per-session | PASS | Focuses solely on unproven technology; recommends performance and availability as follow-ups |
| V4: includes-developers | PASS | Developers are "the most critical participants" — they'll operate Kafka at 3am |
| V5: cost-negotiation-with-alternatives | PASS | De-risking actions include alternatives and production readiness gates |
| V6: unknown-tech-rule | PASS | Central theme: ALL Kafka components start at risk 9; "not negotiable" |
| V7: continuous-not-one-time | PASS | Recommends re-storming AFTER de-risking to verify scores dropped; schedules follow-up sessions |
| V8: color-coded-post-its | PASS | Post-it instructions in invitation with green/yellow/red and score numbers |

**Score: 14/14 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|-------|----------|
| S1: has-three-phases | FAIL | Has 4 agenda items (intro, overview, brainstorm, action planning) — not the three-phase protocol |
| S2: has-session-agenda | PARTIAL | 60-minute agenda with time blocks, but generic meeting structure |
| S3: has-pre-work-materials | FAIL | Preparation asks participants to "come prepared with concerns" but no structured pre-work |
| S4: has-participant-guidance | FAIL | Accepts the given team without validating roles or explaining WHY the mix matters |
| S5: has-risk-dimension-selection | FAIL | No concept of focusing on one dimension; covers operational, technical, and organizational risks |
| S6: has-mitigation-template | PARTIAL | Has a basic table but no cost negotiation fields or alternatives |
| V1: phase1-noncollaborative | FAIL | No individual assessment phase; starts with a group Technology Overview |
| V2: focuses-on-disagreements | FAIL | No mention of disagreements as a source of insight |
| V3: one-dimension-per-session | FAIL | Covers multiple risk categories (operational, technical, organizational) in one session |
| V4: includes-developers | FAIL | No guidance on why developers are critical for this type of session |
| V5: cost-negotiation-with-alternatives | FAIL | No cost negotiation process |
| V6: unknown-tech-rule | FAIL | Mentions "no production experience" as a risk but doesn't apply automatic 9 rule |
| V7: continuous-not-one-time | PARTIAL | Mentions "follow-up in 2-4 weeks" but doesn't frame as continuous practice |
| V8: color-coded-post-its | FAIL | No Post-it notes, no color coding |

**Score: 1.5/14 (11%) — counting 3 PARTIALs as 0.5 each**

---

## Eval 3: Performance risk storming for high-throughput API gateway

**Prompt:** "We've identified some performance concerns in our API gateway that handles 10,000 requests/second. I need to run a collaborative risk session with the platform team (8 people) to identify and prioritize the risks. Can you create a facilitation plan?"

### With Skill

| Assertion | Pass? | Evidence |
|-----------|-------|----------|
| S1: has-three-phases | PASS | Phase 1 (individual pre-work with bottleneck hypotheses), Phase 2 (Consensus, 40min), Phase 3 (Mitigation, 40min) |
| S2: has-session-agenda | PASS | 90-minute timed agenda with bottleneck-chain ranking and validation plan sections |
| S3: has-pre-work-materials | PASS | Invitation with specific performance questions, risk matrix, worksheet with "Bottleneck Hypothesis" column and current metrics fields |
| S4: has-participant-guidance | PASS | Full 8-person team with role-specific value (gateway devs, infra engineers, SREs, tech leads) |
| S5: has-risk-dimension-selection | PASS | Explicitly selects performance with WHY; recommends scalability and availability as follow-ups |
| S6: has-mitigation-template | PASS | Performance-specific template with current metrics, expected improvement, and performance SLO fields |
| V1: phase1-noncollaborative | PASS | Individual pre-work with data-gathering; "Think about these questions as you assess" |
| V2: focuses-on-disagreements | PASS | 20 minutes for disagreement discussion; resolves disputes using load testing data where possible |
| V3: one-dimension-per-session | PASS | Focuses solely on performance; recommends scalability and availability as follow-ups |
| V4: includes-developers | PASS | Full team inclusion with specific reasoning: "different team members own different layers and see different bottlenecks" |
| V5: cost-negotiation-with-alternatives | PASS | Cost-benefit analysis section in agenda; template has effort estimate and cheaper alternative fields |
| V6: unknown-tech-rule | PASS | Risk matrix reference card includes the automatic 9 rule |
| V7: continuous-not-one-time | PASS | Recommends re-storming after mitigations; defines performance gates and SLOs for continuous monitoring |
| V8: color-coded-post-its | PASS | Post-it instructions with green/yellow/red and component-by-component placement |

**Score: 14/14 (100%)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|-------|----------|
| S1: has-three-phases | FAIL | Has 4 agenda items (review, identify, prioritize, plan) — not the three-phase protocol |
| S2: has-session-agenda | PARTIAL | 60-minute agenda with broad time blocks |
| S3: has-pre-work-materials | PARTIAL | Preparation steps include collecting metrics, but no individual assessment worksheets or materials to send |
| S4: has-participant-guidance | FAIL | Accepts "8 people" without role-specific guidance or WHY reasoning |
| S5: has-risk-dimension-selection | FAIL | No concept of single-dimension focus |
| S6: has-mitigation-template | FAIL | No mitigation template |
| V1: phase1-noncollaborative | FAIL | No individual pre-work phase; all identification happens collaboratively |
| V2: focuses-on-disagreements | FAIL | Uses "dot voting" for prioritization — consensus by voting, not disagreement discussion |
| V3: one-dimension-per-session | PARTIAL | Implicitly focused on performance but doesn't state the principle |
| V4: includes-developers | FAIL | No guidance on participant roles or why different perspectives matter |
| V5: cost-negotiation-with-alternatives | FAIL | No cost negotiation process |
| V6: unknown-tech-rule | FAIL | No mention of the unknown-technology rule |
| V7: continuous-not-one-time | PARTIAL | Mentions "follow-up in 2 weeks" but not as a continuous practice |
| V8: color-coded-post-its | FAIL | No Post-it notes, no color coding, no diagram annotation |

**Score: 2/14 (14%) — counting 4 PARTIALs as 0.5 each**

---

## Summary

| Eval | Prompt | With Skill | Without Skill | Gap |
|------|--------|-----------|--------------|-----|
| 1 | Payment system availability | 14/14 (100%) | 1/14 (7%) | +93 pts |
| 2 | Kafka unproven technology | 14/14 (100%) | 1.5/14 (11%) | +89 pts |
| 3 | API gateway performance | 14/14 (100%) | 2/14 (14%) | +86 pts |
| **Average** | | **100%** | **11%** | **+89 pts** |

### Key Observations

**What the skill adds that general agents miss:**

1. **Three-phase protocol with noncollaborative Phase 1** — General agents default to "brainstorm in a meeting." The skill enforces individual assessment BEFORE collaboration to prevent anchoring bias.

2. **Focus on disagreements** — General agents use consensus techniques (dot voting, severity ratings). The skill focuses facilitator attention on WHERE participants disagree, because that's where undiscovered risks hide.

3. **One dimension per session** — General agents try to cover all risks in one meeting. The skill restricts to a single dimension for depth over breadth.

4. **Unknown technology = automatic 9** — General agents mention unfamiliar technology as a risk but don't apply a specific scoring rule. The skill enforces automatic maximum risk.

5. **Color-coded Post-its on architecture diagrams** — General agents use tables and lists. The skill uses a visual spatial technique that maps risks directly to architecture components.

6. **Cost negotiation with alternatives** — General agents list mitigations. The skill includes the cost negotiation process with cheaper backup options.

7. **Complete facilitation package** — General agents produce an agenda. The skill produces a full package: invitation, reference cards, worksheets, agenda, discussion guide, mitigation template, and next steps.
