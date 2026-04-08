---
name: product-team-health-diagnostic
description: |
  Diagnose why a product team or organization is slow, not innovative, or delivering poor outcomes. Use when a leader or team observes slow velocity, lack of innovation, poor product quality, feature factory behavior, or team dysfunction — and needs root causes and a prioritized fix list. Also use when a new product leader is assessing an organization, when a CEO or board says teams are too slow, or when someone says 'why are we not shipping faster?', 'engineering and design aren't collaborating', 'we ship but nothing moves the needle', or 'I need to assess team health before proposing changes.' Scores 42 diagnostic criteria across team behaviors, innovation capacity, velocity killers, and design integration. Produces a severity-ranked report with a composite health score and remediation priorities. For culture-level issues (innovation vs. execution quadrant), use product-culture-assessment. For process-level waterfall diagnosis, use product-process-dysfunction-diagnosis.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/product-team-health-diagnostic
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
model: sonnet
context: 200k
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Observations, notes, or description of the team/organization being assessed"
    - type: none
      description: "Skill can work from a verbal description of what the assessor observes"
  tools-required: [Read]
  tools-optional: []
  environment: "No codebase access required; works from observations and descriptions"
source-books:
  - name: inspired-how-to-create-tech-products
    chapters: [11, 64, 65, 66]
depends-on: []
tags: [product-management, team-assessment, product-teams]
---

# Product Team Health Diagnostic

## When to Use

Use this skill when you are:
- **New to a leadership role** — need a structured baseline assessment of product team health before making changes
- **Responding to CEO/board concerns** — told teams are "too slow" or "not innovative" and need to diagnose root causes
- **Running an org health review** — periodic check on whether teams are operating in a strong or weak product model
- **Preparing a remediation plan** — need to prioritize which problems to fix first and justify the investment
- **Onboarding a coach or consultant** — need a common diagnostic language to align on what's broken

Preconditions: you have at least one of:
- Direct observations of team behaviors over at least a few weeks
- A written description of how teams operate (processes, rituals, structure)
- Interview notes or survey data from team members
- Access to team artifacts (roadmaps, sprint boards, release logs, design files)

**Agent:** Clarify the scope before beginning — are you assessing one team, a portfolio of teams, or the entire engineering/product organization? The scoring applies per team; an org-level report aggregates across teams.

---

## Assessment Process

### Step 1 — Gather Observations

Collect evidence for each of the 4 diagnostic categories. WHY: each category targets a distinct failure mode — behavioral dysfunction (Ch64), structural innovation blockers (Ch65), process velocity killers (Ch66), and design integration failures (Ch11). Mixing them obscures root cause.

For each category, ask the assessor (or yourself) the following:

**Category A — Team Behaviors (18 criteria)**
Source: Ch64. These contrast what strong teams do vs. what weak teams do. Ask:
- What drives the team's ideas — vision and customer insight, or stakeholder requests and sales?
- How does the team relate to engineers — do they co-discover, or do engineers only see designs at sprint planning?
- Does the team engage real customers weekly, or do they rely on internal assumptions?
- How does the team measure success — business impact achieved, or features shipped?
- See full criteria: `references/diagnostic-criteria.md#category-a`

**Category B — Innovation Capacity (10 criteria)**
Source: Ch65. These are organizational attributes that determine whether consistent innovation is even possible. Ask:
- Is there direct, frequent customer contact at the team level?
- Does the organization have a compelling, current product vision?
- Are product managers strong and capable, or weak and order-takers?
- Are engineers included from the beginning of ideation?
- See full criteria: `references/diagnostic-criteria.md#category-b`

**Category C — Velocity Killers (10 criteria)**
Source: Ch66. These are the structural and process causes of slowness. Ask:
- What is the current release cadence? (Benchmark: minimum every 2 weeks; great teams release multiple times per day)
- Is there significant accumulated technical debt impeding the architecture?
- Is there a delivery manager role actively removing impediments?
- Are priorities stable, or do they shift frequently?
- See full criteria: `references/diagnostic-criteria.md#category-c`

**Category D — Design Integration (4 criteria)**
Source: Ch11. These identify whether design is integrated as a discovery partner or treated as a service. Ask:
- Who produces wireframes or interaction designs — a trained product designer, or the PM?
- Are designers embedded with the product team, or do they operate as an internal agency?
- Is design involved from the inception of each idea, or does it come in after requirements?
- See full criteria: `references/diagnostic-criteria.md#category-d`

---

### Step 2 — Score Each Criterion

WHY: Scoring converts qualitative observations into a comparable signal, making it possible to prioritize and track improvement over time.

For each of the 42 criteria, assign one of three scores:

| Score | Meaning |
|-------|---------|
| **2** | Healthy — the team clearly exhibits the strong behavior |
| **1** | Partial — the behavior is inconsistent or only sometimes present |
| **0** | Absent — the weak behavior is the norm |

**Scoring rules:**
- Score what you observe, not what the team says they do. WHY: teams frequently describe aspirational practices.
- When evidence is ambiguous, default to 1 (partial), not 2. WHY: over-scoring masks real problems.
- For Category C, Item 4 (release cadence): score 2 if releases happen at least every 2 weeks, 0 if monthly or less, 1 if inconsistent.

---

### Step 3 — Calculate Category and Composite Scores

For each category, calculate:

```
Category score = (sum of item scores) / (max possible score) × 100
```

| Category | Items | Max Score |
|----------|-------|-----------|
| A — Team Behaviors | 18 | 36 |
| B — Innovation Capacity | 10 | 20 |
| C — Velocity Killers | 10 | 20 |
| D — Design Integration | 4 | 8 |
| **Composite** | **42** | **84** |

WHY: Keeping categories separate prevents a strong score in one area from masking a critical failure in another. A team can be fast (good C score) but consistently build the wrong things (low A score).

---

### Step 4 — Classify Severity

WHY: Not all scores below 100% require equal urgency. This classification focuses remediation effort.

**Per-category thresholds:**

| Score | Severity | Interpretation |
|-------|----------|----------------|
| 80–100% | Healthy | Maintain; minor tuning only |
| 60–79% | Caution | Targeted improvements needed |
| 40–59% | Degraded | Structural issues present; prioritize fixes |
| 0–39% | Critical | Fundamental dysfunction; urgent intervention required |

**Red flags — any single criterion scoring 0 in these areas triggers automatic Critical classification for that dimension, regardless of category average:**
- Team behaviors: engineers excluded from discovery (criterion A9)
- Innovation: no customer-centric culture (criterion B1), no compelling vision (criterion B2)
- Velocity: infrequent releases — monthly or less (criterion C4)
- Design: design not involved in discovery (criterion D4)

WHY: These specific items represent systemic dysfunctions that a higher average cannot compensate for.

---

### Step 5 — Produce the Diagnostic Report

Structure the output as follows:

```
## Product Team Health Diagnostic Report

**Organization/Team:** [name]
**Assessment Date:** [date]
**Assessor:** [role]

---

### Composite Score: [X/84] — [XX%] — [SEVERITY]

| Category | Score | % | Severity |
|----------|-------|---|----------|
| A — Team Behaviors | X/36 | XX% | [label] |
| B — Innovation Capacity | X/20 | XX% | [label] |
| C — Velocity Killers | X/20 | XX% | [label] |
| D — Design Integration | X/8 | XX% | [label] |

---

### Red Flags (Criteria scoring 0 that require immediate attention)
[List each, with one sentence describing the observed symptom]

---

### Category Findings

#### A — Team Behaviors
**Strengths:** [criteria scoring 2]
**Gaps:** [criteria scoring 0 or 1, with observed evidence]

#### B — Innovation Capacity
[same format]

#### C — Velocity Killers
[same format]
Note: Release cadence benchmark — minimum every 2 weeks; great teams release multiple times per day.

#### D — Design Integration
[same format]

---

### Prioritized Remediation Plan

Ordered by: (1) Critical severity first, (2) within severity by cross-category impact

| Priority | Issue | Category | Current State | Target State | Estimated Effort |
|----------|-------|----------|---------------|--------------|-----------------|
| 1 | ... | ... | ... | ... | ... |

---

### Summary Narrative
[3–5 sentences: what is working, what is broken, and the single most important thing to fix first and why]
```

---

### Step 6 — Validate the Assessment

Before delivering the report, verify:
- [ ] Every scored criterion has supporting evidence, not assumption
- [ ] Red flags are confirmed, not inferred
- [ ] The prioritized remediation plan addresses root causes, not symptoms
- [ ] The summary narrative is actionable — it tells the reader what to do, not just what is wrong

WHY: Diagnostic reports are only useful if they drive decisions. Vague findings ("culture needs improvement") create no action. Specific findings ("engineers first see features at sprint planning — exclude from discovery") point to a concrete fix.

---

## Interpreting Results

**Common misread — high velocity, low innovation:** A team can score well on Category C (velocity) while scoring poorly on Category B (innovation). This is the "feature factory" pattern — teams ship fast but build the wrong things. The fix is upstream (discovery and vision), not downstream (process acceleration).

**Common misread — blaming individuals:** Low PM capability scores (B4, C2) often reflect structural issues — PMs who are order-takers because leadership treats them as such. Diagnose whether the PM is weak, or whether the PM has been structurally prevented from being strong.

**Common misread — design as optional:** Category D scores are frequently rationalized ("we're a B2B company, design matters less"). The book is explicit: strong design is a competitive differentiator in B2B, and companies that treat it as optional are being displaced.

**The innovation/velocity relationship:** Chapters 65 and 66 share several root causes (weak PMs, engineers excluded, no vision). Fixes to these shared causes yield compound improvements across both dimensions.

---

## Reference

Full 42-criterion reference table with good/bad behavior descriptions:
`references/diagnostic-criteria.md`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Inspired How To Create Tech Products by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
