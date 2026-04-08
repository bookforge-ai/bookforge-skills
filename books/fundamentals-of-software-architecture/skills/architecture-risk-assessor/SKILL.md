---
name: architecture-risk-assessor
description: Quantify architecture risk using a 2D risk matrix (impact x likelihood, scored 1-9) and produce structured risk assessment reports. Use this skill whenever the user asks about architecture risks, wants to evaluate risk across services or components, needs a risk matrix, mentions risk assessment, risk analysis, risk heat map, risk scoring, or asks "what are the risks?" for any architecture — even if they don't explicitly say "risk assessment." Also triggers when the user mentions unproven technology risk, scalability risk, availability concerns, security risk, data integrity risk, or wants to prioritize risks for stakeholder meetings.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-risk-assessor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [20]
tags: [software-architecture, architecture, risk, risk-matrix, risk-assessment, governance]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "Architecture context from the user — system description, services, components, and concerns"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can read it for context."
---

# Architecture Risk Assessor

## When to Use

You need to systematically identify and quantify risks in a software architecture. Typical triggers:

- The user describes a system and asks "what are the risks?"
- The user is adopting unproven or unfamiliar technologies
- The user needs to present risk findings to stakeholders or leadership
- The user is planning a migration, new service, or significant architecture change
- The user wants to compare risk profiles across services or domains
- The user is doing sprint/iteration planning and wants to identify high-risk stories

Before starting, verify:
- Is there an architecture to assess? (At minimum, a description of services/components and their responsibilities)
- Is there a specific risk dimension to focus on, or should you cover all standard criteria?

## Context

### Required Context (must have before proceeding)

- **System description:** What services, components, or domains exist in the architecture?
  -> Check prompt for: service names, component descriptions, architecture diagrams, system overviews
  -> Check environment for: docker-compose files, k8s manifests, service directories, README files
  -> If still missing, ask: "Can you describe the services or components in your architecture and their primary responsibilities?"

- **Risk concerns:** What is the user worried about? What prompted this risk assessment?
  -> Check prompt for: mentions of failures, performance issues, security concerns, scaling problems, technology uncertainty
  -> If still missing, proceed with all standard risk criteria (scalability, availability, performance, security, data integrity)

### Observable Context (gather from environment if available)

- **Technology stack:** What technologies are in use?
  -> Look for: package.json, requirements.txt, go.mod, Dockerfile, infrastructure configs
  -> If unavailable: rely on user description
- **Architecture style:** Monolith, microservices, event-driven, etc.
  -> Look for: service count, communication patterns, deployment configs
  -> If unavailable: infer from user description
- **Existing risk documentation:** Previous risk assessments, incident reports, post-mortems
  -> Look for: docs/risks/, incident reports, ADRs mentioning risk
  -> If unavailable: start fresh

### Default Assumptions

- If no risk criteria specified -> use the standard five: scalability, availability, performance, security, data integrity
- If no team context -> assume a team with moderate experience in the primary technology
- If technology maturity unknown -> ask, because unproven tech always gets highest risk (9)
- If no existing risk assessments found -> treat as first assessment (no direction indicators)

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- System description with identifiable services/components is known
- At least one risk concern or dimension is identified
- Technology stack is known or can be inferred

PROCEED WITH DEFAULTS when:
- System description is known
- Risk criteria can use standard defaults
- Technology details are partially available

MUST ASK when:
- No system description exists (cannot assess risk without knowing what to assess)
- User mentions "unproven technology" but doesn't specify which one
- The architecture is ambiguous (could be interpreted as monolith or distributed)
```

## Process

### Step 1: Identify Architecture Components

**ACTION:** List all services, components, or domain areas that will be assessed for risk. Name each one clearly.

**WHY:** Risk assessment maps criteria AGAINST specific areas of the architecture. Without a clear component list, the assessment becomes vague hand-waving. Each component carries different risk profiles — a payment service has different risk exposure than a notification service. Identifying components first creates the columns of your risk assessment table.

**IF** the user provided a clear service list -> use it directly
**ELSE IF** a codebase is available -> scan for service boundaries (separate deployables, bounded contexts)
**ELSE** -> ask the user to enumerate their primary services or domains

### Step 2: Determine Risk Criteria

**ACTION:** Select the risk criteria (dimensions) to evaluate. Start with the standard five unless the user specifies different ones:

1. **Scalability** — Can each component handle increased load without degradation?
2. **Availability** — What is the impact and likelihood of each component going down?
3. **Performance** — Can each component meet latency and throughput requirements?
4. **Security** — What is the exposure to unauthorized access, data breaches, or compliance violations?
5. **Data Integrity** — What is the risk of data loss, corruption, or inconsistency?

**WHY:** Risk criteria form the rows of your assessment table. Using standardized criteria ensures consistency across assessments and makes them comparable over time. Custom criteria can be added for domain-specific concerns (e.g., "regulatory compliance" for fintech, "patient safety" for healthcare).

**IF** the user mentioned specific concerns -> add those as additional criteria
**IF** the domain has regulatory requirements -> add a compliance criterion

### Step 3: Score Each Cell Using the Risk Matrix

**ACTION:** For each component-criteria pair, assess two dimensions independently:

- **Impact** (1-3): How severe would it be if this risk materializes?
  - 1 = Low: minor inconvenience, easy recovery
  - 2 = Medium: significant disruption, recoverable with effort
  - 3 = High: severe damage, potential data loss, major business impact

- **Likelihood** (1-3): How probable is it that this risk materializes?
  - 1 = Low: unlikely given current architecture and controls
  - 2 = Medium: possible under certain conditions (peak load, specific failures)
  - 3 = High: probable or already occurring

- **Risk Score** = Impact x Likelihood (range: 1-9)

Classify the composite score:
- **1-2: Low risk (green)** — acceptable, monitor only
- **3-4: Medium risk (yellow)** — needs attention, plan mitigation
- **6-9: High risk (red)** — requires immediate action or architectural change

**WHY:** The 2D matrix separates two fundamentally different aspects of risk that people conflate. A risk with high impact but low likelihood (earthquake destroys data center) requires a different response than a risk with low impact but high likelihood (cache miss causing a slightly slower page load). Multiplying them produces a single comparable score, but keeping both dimensions visible enables smarter mitigation — you can reduce impact OR reduce likelihood.

**CRITICAL RULE:** For any unproven or unknown technology, always assign the highest risk score (9 — impact 3 x likelihood 3). Teams consistently underestimate the risk of technologies they haven't used in production. Unknown unknowns are the most dangerous risks.

For detailed matrix layout and visual reference, see [references/risk-matrix-template.md](references/risk-matrix-template.md).

### Step 4: Build the Risk Assessment Table

**ACTION:** Construct a comprehensive risk assessment table mapping all criteria (rows) against all components (columns). Include row totals (accumulated risk per criterion) and column totals (accumulated risk per component).

**WHY:** The table is the primary artifact. Row totals reveal which risk criteria are most concerning across the entire system — a high scalability total means the architecture has a systemic scalability problem, not just one service. Column totals reveal which components carry the most risk — these are the parts that need the most architectural attention. Both views are essential: criteria totals drive architectural strategy, component totals drive prioritization.

Format:
```
| Risk Criteria    | Service A | Service B | Service C | Total |
|------------------|-----------|-----------|-----------|-------|
| Scalability      | 6 (H)    | 2 (L)    | 4 (M)    | 12    |
| Availability     | 3 (M)    | 9 (H)    | 1 (L)    | 13    |
| Performance      | 2 (L)    | 4 (M)    | 6 (H)    | 12    |
| Security         | 9 (H)    | 3 (M)    | 3 (M)    | 15    |
| Data Integrity   | 6 (H)    | 1 (L)    | 9 (H)    | 16    |
| **Total**        | **26**   | **19**   | **23**   |       |
```

### Step 5: Add Risk Direction Indicators

**ACTION:** For each cell, add a direction indicator showing whether the risk is improving (+), worsening (-), or stable (=) compared to the previous assessment or recent trends.

**WHY:** A risk score of 6 that is improving (+) tells a very different story than a risk score of 6 that is worsening (-). Direction matters as much as current state. It shows whether mitigation efforts are working, whether new risks are emerging, and where to focus future attention. For first-time assessments, use observable signals: recent incidents suggest worsening (-), recent infrastructure improvements suggest improving (+).

**IF** this is the first assessment -> use contextual signals (recent incidents, known issues, recent improvements) to infer direction
**IF** previous assessments exist -> compare directly

### Step 6: Create Filtered Views for Stakeholders

**ACTION:** Produce a filtered version of the risk assessment showing ONLY high-risk cells (scores 6-9). Replace low and medium cells with dots or dashes.

**WHY:** Stakeholders and leadership don't need to see every cell. Showing only red (high-risk) areas focuses attention on what matters and prevents "risk fatigue" where everything looks concerning. The filtered view is what you present in meetings. The full table is the reference document for the architecture team.

Format:
```
| Risk Criteria    | Service A | Service B | Service C |
|------------------|-----------|-----------|-----------|
| Scalability      | 6 (H) -  | .         | .         |
| Availability     | .         | 9 (H) -  | .         |
| Security         | 9 (H) =  | .         | .         |
| Data Integrity   | 6 (H) +  | .         | 9 (H) -  |
```

### Step 7: Recommend Mitigations for High-Risk Areas

**ACTION:** For each high-risk cell (6-9), propose a specific mitigation strategy. Include the estimated risk score AFTER mitigation to show the expected improvement.

**WHY:** Risk assessment without mitigation is just worry. The value is in the response plan. Including post-mitigation scores makes the business case concrete — "spending $X on database clustering reduces data integrity risk from 9 to 3." This feeds directly into budget negotiations with stakeholders.

**IF** the user needs Agile story-level risk analysis -> also apply the risk matrix to user stories (Step 8)
**ELSE** -> proceed to output

### Step 8 (Optional): Agile Story Risk Analysis

**ACTION:** Apply the risk matrix to individual user stories during iteration planning:
- **Impact dimension:** Overall impact if this story is NOT completed in the iteration
- **Likelihood dimension:** Probability that this story will NOT be completed (complexity, dependencies, unknowns)
- Identify stories scoring 6-9 as high-risk and flag them for priority attention

**WHY:** The same risk matrix that works for architecture works for sprint planning. High-risk stories — those with high impact if missed AND high likelihood of not completing — should be started early, broken down further, or given to the most experienced developers. This connects architectural risk thinking to daily development practice.

## Inputs

- System description with identifiable services/components (from user or codebase)
- Risk concerns or dimensions to evaluate (from user, or use defaults)
- Optionally: previous risk assessments, incident history, technology stack details

## Outputs

### Architecture Risk Assessment Report

```markdown
# Architecture Risk Assessment: {System Name}

## Assessment Scope
- **Date:** {date}
- **Assessed by:** {who}
- **Architecture style:** {monolith/microservices/event-driven/etc.}
- **Components assessed:** {count}
- **Risk criteria:** {list}

## Architecture Components
1. **{Component A}** — {responsibility}
2. **{Component B}** — {responsibility}
3. **{Component C}** — {responsibility}

## Full Risk Assessment

| Risk Criteria    | Component A      | Component B      | Component C      | Total |
|------------------|------------------|------------------|------------------|-------|
| Scalability      | {score} ({L/M/H}) {dir} | ... | ... | {sum} |
| Availability     | ... | ... | ... | {sum} |
| Performance      | ... | ... | ... | {sum} |
| Security         | ... | ... | ... | {sum} |
| Data Integrity   | ... | ... | ... | {sum} |
| **Total**        | **{sum}**        | **{sum}**        | **{sum}**        |       |

### Scoring Key
- Score = Impact (1-3) x Likelihood (1-3)
- Low (L): 1-2 | Medium (M): 3-4 | High (H): 6-9
- Direction: + improving, - worsening, = stable

## High-Risk Summary (Filtered View)

{Filtered table showing only 6-9 scores}

## Risk Details and Mitigations

### {Component A} — {Risk Criteria} (Score: {N})
- **Impact ({1-3}):** {why this impact level}
- **Likelihood ({1-3}):** {why this likelihood level}
- **Direction:** {+/-/=} {reason}
- **Mitigation:** {specific recommendation}
- **Post-mitigation estimate:** {expected new score}

{Repeat for each high-risk cell}

## Systemic Risk Observations
- {Pattern observed across multiple components}
- {Risk criteria with highest total — indicates systemic issue}
- {Components with highest totals — indicates architectural attention needed}

## Recommendations Priority
1. {Highest priority mitigation} — addresses {risk}
2. {Second priority} — addresses {risk}
3. {Third priority} — addresses {risk}
```

## Key Principles

- **Separate impact from likelihood** — These are fundamentally different dimensions that require different mitigation strategies. High-impact/low-likelihood risks need contingency plans. Low-impact/high-likelihood risks need engineering fixes. Conflating them into a single "risk level" hides the appropriate response.

- **Unknown technology = maximum risk** — For any unproven or unfamiliar technology, always assign the highest risk score (9). Teams systematically underestimate the danger of technologies they haven't used in production. Unknown unknowns are the most dangerous class of risk. This isn't pessimism — it's calibration against a well-documented bias.

- **Direction matters as much as magnitude** — A risk score of 6 that is improving tells a completely different story than a score of 4 that is worsening. Track direction with every assessment. It reveals whether mitigation efforts are working and where new risks are emerging.

- **Filter for your audience** — Show the full risk assessment to the architecture team. Show only high-risk areas (6-9) to stakeholders and leadership. Risk fatigue is real — if everything looks red, nothing gets attention. Filtering focuses the conversation on what actually needs action.

- **Risk assessment is continuous, not one-time** — Architecture risk changes as the system evolves, new technologies are adopted, team composition shifts, and business requirements change. A risk assessment is a living document. Treat it like a fitness function — measure regularly, compare to previous results, act on trends.

- **Mitigation has a cost** — Every mitigation strategy costs something: money, complexity, development time, or operational burden. Present mitigations alongside their costs so stakeholders can make informed decisions. Sometimes accepting a medium risk is better than the cost of eliminating it.

## Examples

**Scenario: E-commerce platform risk assessment**
Trigger: "We have 4 services: customer registration, catalog checkout, order fulfillment, and order shipment. Can you assess the architecture risks?"
Process: Listed 4 components. Applied standard 5 risk criteria. Scored each cell using the impact x likelihood matrix. Customer registration scored low across the board. Catalog checkout scored high on performance (6) due to peak-hour load. Order fulfillment scored high on availability (9) and data integrity (6) because lost orders mean lost revenue. Order shipment scored medium across most criteria. Created filtered view showing only the 3 high-risk cells. Recommended: message queue between checkout and fulfillment (reduces availability risk from 9 to 3), database replication for order data (reduces data integrity risk from 6 to 2), auto-scaling for catalog during peak hours (reduces performance risk from 6 to 2).
Output: Full risk assessment report with filtered stakeholder view and 3 prioritized mitigations with cost estimates.

**Scenario: Unproven technology risk flag**
Trigger: "We're evaluating using CockroachDB for our new service. Nobody on the team has used it before."
Process: Immediately flagged CockroachDB as unproven technology — assigned risk score 9 (impact 3 x likelihood 3) per the unknown-technology rule. Assessed the service across standard criteria. Data integrity risk automatically high (9) due to unfamiliar database behavior under edge cases. Availability risk elevated (6) because the team can't troubleshoot production issues quickly. Recommended mitigations: proof-of-concept with production-like load before committing, dedicated learning sprint, identify rollback strategy to known database, engage vendor support.
Output: Risk assessment highlighting the technology risk with specific de-risking steps and a decision gate (proceed only if PoC succeeds).

**Scenario: Agile story risk analysis for sprint planning**
Trigger: "We have 12 stories for the next sprint. Some feel risky. How do we figure out which ones to prioritize?"
Process: Applied the risk matrix to each story. Impact = business impact if story not completed this sprint. Likelihood = probability of non-completion (based on complexity, dependencies, unknowns). Identified 3 stories scoring 6-9: a payment integration story (impact 3 x likelihood 2 = 6, depends on external API), a data migration story (impact 3 x likelihood 3 = 9, unknown data quality), and a performance optimization story (impact 2 x likelihood 3 = 6, requires load testing infrastructure). Recommended: start data migration story on day 1 with senior developer, spike the payment integration dependency immediately, defer performance story to next sprint if load testing infra isn't ready.
Output: Story risk matrix with all 12 stories scored, 3 flagged as high-risk with specific handling recommendations.

## References

- For the detailed risk matrix layout with visual scoring guide, see [references/risk-matrix-template.md](references/risk-matrix-template.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
