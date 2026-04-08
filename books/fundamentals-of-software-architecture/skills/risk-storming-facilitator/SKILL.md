---
name: risk-storming-facilitator
description: Plan and facilitate collaborative risk storming sessions for architecture teams. Use this skill whenever the user wants to run a risk identification workshop, organize a risk storming exercise, plan a collaborative risk assessment session, facilitate architecture risk discovery with a team, prepare a risk workshop agenda, coordinate group risk identification, or run a team-based architecture risk review. Also triggers when the user mentions "risk storming," "collaborative risk session," "team risk workshop," "group risk identification," wants to prepare pre-work materials for a risk meeting, or asks "how should I run a risk session with my team?" — even if they don't use the exact term "risk storming."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/risk-storming-facilitator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [20]
tags: [software-architecture, architecture, risk, risk-storming, facilitation, collaboration, governance]
depends-on:
  - architecture-risk-assessor
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: none
      description: "Architecture context from the user — system description, team composition, and risk concerns. Agent produces the facilitation plan; human runs the actual session."
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. Agent produces facilitation artifacts; human executes the session."
---

# Risk Storming Facilitator

## When to Use

You need to prepare and facilitate a collaborative risk identification session with your architecture team. This is a PLAN-ONLY skill — the agent creates all facilitation materials and the human runs the actual session.

Typical triggers:
- The user wants to run a risk storming session with their team before a launch or major milestone
- The user adopted a new technology and wants the team to collaboratively identify risks
- The user needs to assess risks across a specific dimension (availability, performance, security, etc.) with multiple stakeholders
- The user wants to structure a risk workshop and needs an agenda, pre-work materials, and discussion guide
- The user is an architect preparing for a collaborative risk review with senior developers and tech leads

Before starting, verify:
- Is there an architecture diagram or system description available? (Risk storming requires a visual representation of the architecture)
- Has the user identified which risk dimension to focus on? (Sessions work best with ONE dimension at a time)
- Who will participate? (Should include architects, senior developers, AND tech leads — not just architects)

## Context

### Required Context (must have before proceeding)

- **Architecture description or diagram:** What system is being assessed? What are the components, services, and their relationships?
  -> Check prompt for: service names, architecture diagrams, component descriptions, technology stack
  -> Check environment for: architecture docs, C4 diagrams, docker-compose files, README files with system overviews
  -> If still missing, ask: "Can you describe the architecture you want to risk-storm? I need at minimum the major components/services and how they connect."

- **Risk dimension to focus on:** Which area of risk should the session address?
  -> Check prompt for: mentions of availability, performance, scalability, security, data loss, single points of failure, unproven technology
  -> If still missing, ask: "Which risk dimension should this session focus on? Common choices: (a) availability, (b) performance, (c) scalability, (d) security, (e) data loss/integrity, (f) unproven technology, (g) single points of failure. I recommend ONE dimension per session for focused results."

### Observable Context (gather from environment if available)

- **Team composition:** Who will participate?
  -> Check prompt for: team size, role descriptions, mentions of developers, tech leads, architects
  -> If unavailable: default to "the architecture team" and recommend including senior developers and tech leads
- **Technology stack:** What technologies are in use?
  -> Look for: package.json, requirements.txt, Dockerfile, infrastructure configs
  -> If unavailable: rely on user description
- **Previous risk assessments:** Has the system been risk-assessed before?
  -> Look for: risk reports, incident history, post-mortems
  -> If unavailable: treat as first risk storming session

### Default Assumptions

- If no risk dimension specified -> recommend starting with the dimension most relevant to the user's stated concerns
- If no participants listed -> recommend 4-8 participants including at least 1 architect, 2+ senior developers, and 1+ tech lead
- If no architecture diagram exists -> recommend creating one before the session (risk storming requires a visual artifact)
- If session format not specified -> default to in-person with physical Post-it notes; provide virtual alternative

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Architecture description with identifiable components is known
- Risk dimension for the session is selected
- Participant roles are known or can be defaulted

PROCEED WITH DEFAULTS when:
- Architecture description is known
- Risk dimension can be inferred from the user's concerns
- Team details can use reasonable defaults

MUST ASK when:
- No architecture description exists (cannot risk-storm without knowing what to assess)
- The user's concern is too vague to select a risk dimension
- The user wants to cover "all risks" in one session (this is an anti-pattern; redirect to single dimension)
```

## Process

### Step 1: Select the Risk Dimension

**ACTION:** Help the user choose ONE risk dimension for the session. Common dimensions:
- **Unproven technology** — new or unfamiliar technologies in the stack
- **Performance** — latency, throughput, response time under load
- **Scalability** — ability to handle increased load (horizontal/vertical)
- **Availability** — uptime, resilience to failures, including transitive dependencies
- **Data loss/integrity** — risk of losing, corrupting, or leaking data
- **Single points of failure** — components whose failure takes down the entire system
- **Security** — unauthorized access, data breaches, compliance violations

**WHY:** Restricting each session to a single dimension produces dramatically better results than trying to assess everything at once. When participants evaluate multiple dimensions simultaneously, they lose focus, conflate different risk types, and produce shallow analysis. A focused session on availability reveals risks that a broad "assess everything" session misses entirely. Run separate sessions for separate dimensions.

**IF** the user already specified a dimension -> confirm and proceed
**IF** the user wants multiple dimensions -> plan separate sessions (one per dimension), prioritize the most urgent first
**IF** the user says "I don't know which" -> ask about recent incidents, upcoming launches, or technology changes to identify the most pressing dimension

### Step 2: Map the Architecture Components

**ACTION:** Enumerate all architecture components that participants will assess. Create a clear component list with brief descriptions.

**WHY:** The component list defines WHAT gets risk-assessed. Missing a component means missing its risks entirely. The list also becomes the basis for the architecture diagram that participants will annotate with Post-it notes during the session.

**IF** an architecture diagram exists -> extract components from it
**IF** a codebase is available -> scan for service boundaries, deployables, infrastructure components
**ELSE** -> ask the user to enumerate components

**HANDOFF TO HUMAN** -- The agent produces the component list; the human validates it is complete and accurate before using it in the session.

### Step 3: Identify Participants

**ACTION:** Build a participant list. The session MUST include people beyond just architects:

- **Architects** (1-2): Provide the high-level structural perspective
- **Senior developers** (2-4): Provide implementation-level risk knowledge that architects miss
- **Tech leads** (1-2): Bridge the gap between architecture vision and implementation reality

**WHY:** No single architect can identify all risks. Senior developers see implementation-level risks that architects overlook — like a developer who rates Redis cache as risk 9 because they've never used it, revealing a critical unknown-technology risk the architect missed. Tech leads understand operational constraints that change risk profiles. The diversity of perspectives IS the point of risk storming.

**IF** the user already has a participant list -> validate it includes developers, not just architects
**IF** the team is small (< 4) -> the session can still work, but note that fewer perspectives means fewer risks discovered

### Step 4: Prepare Pre-Work Materials

**ACTION:** Generate the following materials to send to participants 1-2 days before the collaborative session:

1. **Session invitation** containing:
   - Architecture diagram (or link to where it's stored)
   - The ONE risk dimension being assessed
   - Date, time, and location (physical or virtual)
   - Brief explanation of the risk matrix (impact x likelihood, 1-9 scale)
   - Instructions for individual risk identification (Phase 1)

2. **Risk matrix reference card:**
   - Impact: Low (1), Medium (2), High (3)
   - Likelihood: Low (1), Medium (2), High (3)
   - Score = Impact x Likelihood
   - Color coding: 1-2 green (low), 3-4 yellow (medium), 6-9 red (high)
   - Critical rule: unproven/unknown technology = automatic 9

3. **Individual assessment worksheet** (one per participant):
   - Architecture component list
   - For each component: assess impact and likelihood for the chosen risk dimension
   - Record the composite score (impact x likelihood)
   - Prepare a Post-it note with the color matching the score (green/yellow/red) and the score number written on it

**WHY:** Sending materials 1-2 days ahead gives participants time to individually analyze the architecture without group influence. The noncollaborative nature of Phase 1 is essential — it prevents anchoring bias where one vocal participant's assessment dominates everyone's thinking. Individual assessment first, THEN collaborative discussion, produces the richest set of risks.

**HANDOFF TO HUMAN** -- The agent generates all pre-work documents; the human sends them to participants.

### Step 5: Create the Session Agenda

**ACTION:** Produce a structured agenda for the collaborative session (Phases 2 and 3):

```
RISK STORMING SESSION AGENDA
Dimension: {selected dimension}
Duration: 60-90 minutes

PHASE 2: CONSENSUS (30-40 minutes)
[00:00-05:00] Opening — restate the risk dimension and ground rules
[05:00-15:00] Post-it placement — each participant places their
              color-coded Post-it notes on the architecture diagram
              where they identified risk
[15:00-35:00] Disagreement discussion — focus on areas where
              participants DIFFER in their ratings:
              - Where one person sees high risk and another sees none
              - Where scores differ by 2+ points
              - Single-person risks (only one person identified it)
[35:00-40:00] Consolidation — agree on final ratings for each
              risk area

PHASE 3: MITIGATION (20-40 minutes)
[40:00-55:00] Mitigation brainstorm — for each high-risk area (6-9),
              identify architecture changes that would reduce the risk
[55:00-70:00] Cost negotiation — estimate the cost of each mitigation
              and determine if the risk reduction justifies the cost
[70:00-80:00] Action items — assign owners and deadlines for
              agreed mitigations
[80:00-90:00] Wrap-up — summarize findings, schedule next risk
              storming session (different dimension)
```

**WHY:** The agenda front-loads disagreement discussion because that is where the highest-value insights emerge. When two participants rate the same component differently, the ensuing discussion reveals knowledge that neither participant had alone — like the developer who rates Redis as risk 9 because they've never used it, while the architect rated it as risk 1 assuming everyone knew Redis. The disagreement IS the insight.

### Step 6: Create the Discussion Guide

**ACTION:** Produce a facilitation guide with specific questions to drive productive disagreement discussion:

**For areas where ratings differ:**
- "You rated this as {high} while you rated it as {low}. Can each of you explain your reasoning?"
- "What information or experience led you to that score?"
- "Is there something about the implementation that changes the risk assessment?"

**For areas where only one person identified risk:**
- "You're the only one who flagged this. What do you see that the rest of us might be missing?"
- "Have you had direct experience with this type of risk?"

**For unproven technology:**
- "Has anyone on the team used {technology} in a production system before?"
- "If no one has production experience, this is automatically rated 9 per the unknown-technology rule."

**For the mitigation phase:**
- "What architecture change would reduce this risk score from {current} to {target}?"
- "What would that change cost in terms of money, time, or complexity?"
- "Is the risk reduction worth the cost? If not, what is a cheaper alternative that partially mitigates the risk?"

**WHY:** Facilitators often struggle to drive productive discussion. These prepared questions prevent the session from becoming either a silent agreement fest or an unfocused debate. The questions are designed to surface the knowledge gaps between participants — which is exactly where undiscovered risks hide.

**HANDOFF TO HUMAN** -- The agent produces the discussion guide; the human uses it to facilitate the actual session.

### Step 7: Create the Mitigation Template

**ACTION:** Produce a template for documenting mitigations discovered during Phase 3:

```markdown
## Risk Mitigation Record

### Risk Area: {component} - {dimension}
- **Consensus Risk Score:** {score} ({impact} x {likelihood})
- **Identified by:** {participant names}
- **Rationale:** {why this risk level}

### Proposed Mitigation
- **Change:** {specific architecture change}
- **Expected post-mitigation score:** {new score}
- **Estimated cost:** {money, time, complexity}
- **Alternative (if cost rejected):** {cheaper partial mitigation}
- **Alternative cost:** {reduced cost}
- **Owner:** {who will implement}
- **Deadline:** {when}
- **Status:** Proposed / Approved / Implemented
```

**WHY:** Mitigations without documentation become forgotten promises. The template captures not just the mitigation but the cost negotiation — which is critical because stakeholders often reject the first proposed mitigation as too expensive. Having a documented alternative at a lower cost point (like splitting a database without clustering, reducing cost from $20,000 to $8,000) gives the architect negotiating flexibility.

**HANDOFF TO HUMAN** -- The agent produces the template; the human fills it in during the session.

### Step 8: Compile the Complete Facilitation Package

**ACTION:** Assemble all artifacts into a single facilitation package:
1. Session invitation with architecture diagram and risk dimension
2. Risk matrix reference card
3. Individual assessment worksheets
4. Session agenda
5. Discussion guide with prepared questions
6. Mitigation record template
7. Recommendation for the NEXT session (different risk dimension)

**WHY:** A complete package lets the facilitator focus on running the session rather than scrambling for materials. The recommendation for the next session reinforces that risk storming is continuous — not a one-time event. Each dimension reveals different risks, and the architecture should be re-stormed after major changes or at regular intervals.

For the detailed facilitation protocol with timing and role assignments, see [references/facilitation-protocol.md](references/facilitation-protocol.md).

## Inputs

- Architecture description or diagram with identifiable components
- Risk dimension to focus on (or user concerns to derive one from)
- Participant list or team description (roles and approximate size)
- Optionally: previous risk assessments, incident history, technology stack details

## Outputs

### Risk Storming Facilitation Package

The agent produces all of the following artifacts; the human uses them to run the actual session:

1. **Pre-work materials** — invitation, risk matrix card, individual worksheets
2. **Session agenda** — timed agenda for the 60-90 minute collaborative session
3. **Discussion guide** — prepared questions for driving productive disagreement discussion
4. **Mitigation template** — structured template for documenting mitigations and cost negotiations
5. **Next steps recommendation** — which dimension to storm next, when to re-storm

## Key Principles

- **One dimension per session** -- Assessing multiple risk dimensions in a single session dilutes focus and produces shallow results. A dedicated availability session reveals risks that a broad "assess all risks" session misses entirely. If the user wants to cover multiple dimensions, plan separate sessions and prioritize the most urgent first.

- **Disagreements are the insight, not the problem** -- When participants rate the same component differently, that disagreement reveals knowledge asymmetry — one person knows something the others don't. The facilitator's job is to mine these disagreements, not to resolve them quickly. Spend 60% of consensus time on areas where ratings differ.

- **Include developers, not just architects** -- Senior developers see implementation-level risks that architects miss. A developer who rates an unfamiliar technology as risk 9 reveals a critical unknown that the architect assumed everyone knew. Tech leads bridge the gap between design intent and operational reality. The diversity of perspectives is the entire point.

- **Unknown technology = automatic risk 9** -- For any technology that the team hasn't used in production, always assign the highest risk score (9). The risk matrix cannot be applied meaningfully because the team cannot assess likelihood for something they've never operated. This rule prevents the systematic underestimation of unfamiliar technology risk.

- **Mitigation requires cost negotiation** -- Every mitigation costs something. When stakeholders reject the first proposal as too expensive, have a cheaper alternative ready that partially mitigates the risk. The goal is risk reduction the business can afford, not perfect risk elimination at any cost.

- **Risk storming is continuous** -- A single session assesses one dimension. The architecture should be re-stormed after major changes, technology adoptions, or at regular intervals (e.g., quarterly). Each session reveals different risks and progressively improves the architecture.

## Examples

**Scenario: Pre-launch availability risk storming for microservices payment system**
Trigger: "We're about to launch a new microservices payment system. I want to do a risk assessment with my team focused on availability."
Process: Selected availability as the risk dimension. Mapped 6 services (API gateway, payment processor, notification service, user service, audit logger, database cluster). Recommended participants: lead architect, 3 senior backend developers, platform tech lead, SRE lead. Generated pre-work package with architecture diagram, risk matrix reference, and individual worksheets. Created 75-minute agenda with 35 minutes for consensus (focusing on where ratings diverge) and 30 minutes for mitigation planning. Prepared discussion questions targeting single points of failure, database availability, and third-party payment provider SLAs. Created mitigation template with cost negotiation section.
Output: Complete facilitation package with 7 artifacts. Recommended follow-up sessions for performance and security dimensions.

**Scenario: Unproven technology risk storming for Kafka adoption**
Trigger: "Our team just adopted Kafka for event-driven architecture. Nobody has used Kafka in production before. I need to facilitate a risk session with 4 senior devs and 2 tech leads."
Process: Selected unproven technology as the risk dimension (automatically the highest priority when the team has zero production experience). Mapped architecture components that interact with Kafka (event producers, consumers, topic management, schema registry, dead letter queues). Noted that per the unknown-technology rule, ALL Kafka-related components receive automatic risk score 9. Generated pre-work emphasizing that participants should identify specific areas where Kafka's behavior is unknown to them. Created agenda with extended discussion time (45 minutes) since disagreements will center on "what we don't know we don't know." Prepared questions focused on production operation gaps: "Who will handle partition rebalancing at 3am?" and "What happens when a consumer falls behind?" Created mitigation template emphasizing de-risking steps: PoC with production load, vendor support contracts, team training.
Output: Complete facilitation package tuned for unproven-technology sessions. Flagged that every Kafka component starts at risk 9 and mitigations focus on de-risking through knowledge and operational readiness.

**Scenario: Performance risk storming for high-throughput API gateway**
Trigger: "We have performance concerns with our API gateway handling 10,000 req/s. I need to run a risk session with the platform team of 8 people."
Process: Selected performance as the risk dimension. Mapped API gateway subcomponents (load balancer, rate limiter, auth middleware, request router, response cache, logging pipeline, upstream service connections). Recommended splitting the 8-person team into the full session since all are relevant. Generated pre-work with current performance baselines (if available) alongside the architecture diagram. Created 90-minute agenda with 40 minutes for consensus and 40 minutes for mitigation, given the technical depth needed. Prepared discussion questions targeting bottleneck identification: "At 10,000 req/s, which component hits its limit first?" and "What happens to latency when the response cache misses?" Created mitigation template with performance-specific fields: current throughput, target throughput, expected improvement per mitigation.
Output: Complete facilitation package for performance-focused session. Recommended load testing validation after implementing mitigations.

## References

- For the detailed three-phase facilitation protocol with timing, role assignments, and virtual session adaptations, see [references/facilitation-protocol.md](references/facilitation-protocol.md)
- For risk matrix scoring details, invoke the `architecture-risk-assessor` skill

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-risk-assessor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
