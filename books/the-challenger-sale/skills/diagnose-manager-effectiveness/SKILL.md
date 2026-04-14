---
name: diagnose-manager-effectiveness
description: "Diagnose a frontline sales manager's effectiveness against the CEB four-driver model. Use when someone asks: 'sales manager effectiveness', 'am I coaching the right reps', 'sales manager diagnostic', 'manager coaching ROI', 'where should I spend coaching time', 'sales manager assessment', 'Challenger sales manager', 'manager drivers', 'front-line manager performance', 'am I a good sales manager', 'sales manager self-assessment', 'coaching time allocation', 'am I spending coaching time correctly', 'democratic coaching', 'why is my team not improving'. Produces a manager-effectiveness-diagnosis.md with weighted driver scores, active anti-patterns, and a concrete time-reallocation plan based on team composition."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/diagnose-manager-effectiveness
metadata: {"openclaw":{"emoji":"🧭","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors: ["Matthew Dixon", "Brent Adamson"]
    chapters: [8]
tags: [sales, sales-management, challenger-sale, manager-diagnostic, coaching-roi]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "coaching-log.md or manager self-description plus team composition (star/core/laggard breakdown)"
  tools-required: [Read, Write, AskUserQuestion]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any working directory. No codebase required."
discovery:
  goal: "Diagnose a sales manager against the CEB four-driver model and identify where coaching time is being wasted"
  tasks:
    - "Gather manager time allocation across four activity types"
    - "Apply Management Fundamentals gate — stop if not cleared"
    - "Score manager against four driver weights (Selling 27%, Coaching 28%, Innovating 29%, Resource Allocation 16%)"
    - "Detect democratic-coaching anti-pattern in coaching time distribution"
    - "Distinguish coaching activity (known behavior development) from innovating activity (deal-level obstacle solving)"
    - "Produce manager-effectiveness-diagnosis.md with reallocation plan"
  audience:
    roles: ["Frontline sales managers", "sales VPs", "sales enablement professionals", "sales operations"]
    experience: intermediate
  when_to_use:
    triggers:
      - "Manager wants to know whether they are spending their time on the highest-impact activities"
      - "Sales VP wants to diagnose which managers need development and in which driver"
      - "Enablement team wants to baseline manager cohort before a Challenger training initiative"
      - "Manager is not seeing rep performance improvement despite active coaching efforts"
    prerequisites: []
    not_for:
      - "Running a coaching session with a rep (use coach-rep-with-pause-framework instead)"
      - "Planning a Challenger rollout across a sales organization (use plan-challenger-model-rollout)"
      - "Assessing individual rep selling profiles (use classify-rep-profile)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 6
    iterations_needed: null
---

# Diagnose Manager Effectiveness

Diagnoses a frontline sales manager against the CEB five-factor effectiveness model (derived from 2,500+ managers, 12,000+ reps). Identifies whether the manager has cleared the Management Fundamentals gate and where their time allocation is misaligned with the four driver weights that predict manager excellence: Sales Innovation (29%), Coaching (28%), Selling (27%), Resource Allocation (16%). Produces a structured diagnosis artifact with anti-pattern flags and a reallocation plan.

The core counterintuitive finding from the CEB data: most managers think sales leadership is about resource allocation and pipeline management. The data says those are the least important activities. The single biggest driver is sales innovation — a skill most sales leaders have never systematically thought about.

Driver weights and the star/core/laggard coaching ROI table are in `references/manager-drivers.md`.

## When to Use

- A manager asks "am I spending my time correctly?" or "why isn't my team improving despite my coaching?"
- A sales VP wants to rank managers by development priority and identify which driver to invest in
- An enablement team wants to baseline the management cohort before a Challenger training program
- A manager feels like they're working hard but the numbers aren't moving

**Not for:** executing a coaching session with a rep (that's coach-rep-with-pause-framework), planning an organization-wide Challenger rollout, or assessing individual rep selling profiles.

## Step 1 — Gather Manager Context

Before scoring, collect the following. If the manager has provided a document (coaching-log.md or self-description), read it first. Then ask for anything missing.

**Time allocation** — Ask the manager to estimate their average week:
- What percentage of time goes to selling or deal support (covering territories, supporting complex deals, modeling behaviors for the team)?
- What percentage goes to coaching reps (1:1s, ride-alongs, call debriefs focused on rep skill development)?
- What percentage goes to deal-level innovation (working with reps to unstick specific stuck deals, finding creative paths through customer obstacles)?
- What percentage goes to resource allocation (pipeline reviews, CRM, territory management, process compliance, activity tracking)?

If percentages don't sum to roughly 100%, ask for clarification. If the manager cannot distinguish coaching from deal innovation, note that — it is a diagnostic signal in itself.

**Team composition** — Ask:
- How many reps on the team?
- Roughly what fraction are stars (consistently above quota), core (at or near quota), or laggards (chronically below, not on a recovery track)?
- Which tier gets the most coaching time currently?

**Management fundamentals check** — Ask the manager to reflect on five binary questions:
1. Do your reps consider you reliable — that you follow through on what you commit to?
2. Do your reps trust that you act with integrity in performance conversations?
3. Do you listen before directing in conversations?
4. Do you recognize rep contributions visibly and specifically?
5. Do you actively build team cohesion and protect psychological safety?

These are pass/fail. A "no" to any one of them triggers the gate in Step 2.

## Step 2 — Management Fundamentals Gate

Management fundamentals are a prerequisite, not a driver to develop alongside the others. They are binary traits — either present or not — and they cannot be coached into existence. CEB found ~4% of managers fail on at least one.

**If the manager fails on any fundamental:**
- Stop the downstream analysis. Flag this clearly in the output.
- The recommendation is not "work on reliability" — it is organizational: this manager should be moved to a non-management role. Investing in their Selling, Coaching, or Innovating skills while management fundamentals are broken produces no return.
- Output a gate-failure diagnosis and end there.

**If the manager passes all five:**
- Proceed to Step 3.

**Why this matters:** Management fundamentals provide the foundation every other driver builds on. A technically skilled manager with an integrity problem creates a fundamentally unsafe environment where coaching cannot land, innovation cannot happen, and rep retention collapses.

## Step 3 — Score Time Allocation Against Driver Weights

The four sales-side drivers and their empirically derived weights:

| Driver | Weight | What It Covers |
|---|---|---|
| Sales Innovation (Innovating) | 29% | Unsticking stuck deals, collaborative deal-level problem solving |
| Coaching | 28% | Developing rep skills toward known behaviors, behavior-focused 1:1s |
| Selling | 27% | Modeling Challenger behaviors, supporting complex deals, covering vacancies |
| Resource Allocation | 16% | Pipeline reviews, CRM compliance, territory management, activity tracking |

For each driver, compare the manager's reported time to the weight. Calculate the gap:

```
Gap = Reported time % − Driver weight %
```

Positive gap = over-indexed. Negative gap = under-indexed.

**Flag as high-priority when:**
- Innovation gap is more negative than −10 points (most common under-investment)
- Coaching gap is more negative than −10 points
- Resource allocation gap is more positive than +15 points (most common over-investment)

**Common mismatch pattern:** Managers over-invest in resource allocation (pipeline reviews, CRM) because it feels like management and is easy to measure. The data says this is the least impactful driver. The most impactful driver — innovation — is rarely tracked, rarely recognized, and rarely developed.

## Step 4 — Detect Democratic Coaching Anti-Pattern

The democratic coaching anti-pattern is one of the most expensive mistakes in sales management: spreading coaching time equally across all reps regardless of performance tier.

**Why it produces near-zero return:**
- Coaching **laggards** (low performers) has near-zero impact. You cannot coach away a poor job fit. These reps need a different role, not better coaching.
- Coaching **stars** (high performers) produces marginal gains. Like a professional golfer shaving one stroke off their average — small incremental improvements on an already high baseline.
- Coaching **core** (median) performers is where all the upside lives. The CEB data shows a significant coaching quality improvement can boost core performer output by up to **19%**. Even moving from bottom-third to top-third coaching quality produces a **6-8% performance gain** for core reps.

**Detection questions:**
- Does the manager spend roughly equal time coaching each rep regardless of tier?
- Does the manager spend disproportionate time on their two most challenging reps (laggards)?
- Does the manager treat star 1:1s as coaching sessions rather than innovation conversations?

**Flag the anti-pattern when:**
- Coaching time is distributed roughly equally across all tiers
- More than 40% of coaching time goes to laggards
- Stars receive structured behavior-development coaching rather than deal-level collaboration

**Correct allocation:** Shift the majority of scheduled coaching time to core/median performers. Reserve time with stars for deal innovation conversations (collaborative problem solving on stuck deals). Move chronic laggards through performance management rather than coaching.

## Step 5 — Distinguish Coaching From Innovating

Many managers confuse these or default entirely to one mode. This is a second diagnostic check independent of time allocation.

**Ask the manager to describe a recent interaction where they helped a rep:**
- If the manager directed the rep toward a specific behavior they knew was missing → that is **coaching**
- If the manager and rep worked through an unknown together to find a path forward on a stuck deal → that is **innovating**

**Red flags indicating confusion:**
- Manager describes all rep interactions as "coaching" including deal problem-solving
- Manager cannot recall any instance of genuine deal-level innovation (suggests innovating is absent)
- Manager describes innovation as "coming up with new value propositions" (that is not what sales innovation means — it is creatively connecting existing capabilities to specific customer obstacles)

**Why the distinction matters:** Coaching builds repeatable rep skills over time. Innovating closes specific stuck deals now. A manager who only coaches leaves revenue on the table. A manager who only innovates never improves rep capability. Both are required — and both count toward the 28%/29% of manager excellence.

## Step 6 — Write manager-effectiveness-diagnosis.md

Write the diagnosis artifact to `manager-effectiveness-diagnosis.md` in the current directory. Structure:

```markdown
# Manager Effectiveness Diagnosis
Generated: [date]

## Management Fundamentals — [PASS / GATE FAILURE]
[If gate failure: stop here with recommendation to redeploy]

## Time Allocation vs. Driver Weights
| Driver | Reported % | Target Weight | Gap | Status |
|---|---|---|---|---|
| Sales Innovation | X% | 29% | ±N | Over/Under/Aligned |
| Coaching | X% | 28% | ±N | Over/Under/Aligned |
| Selling | X% | 27% | ±N | Over/Under/Aligned |
| Resource Allocation | X% | 16% | ±N | Over/Under/Aligned |

## Active Anti-Patterns
[List detected anti-patterns with evidence. If none, say so.]

### Democratic Coaching — [DETECTED / NOT DETECTED]
[Evidence: how coaching time is distributed across tiers]
[Estimated coaching time wasted on low-ROI tiers]

### Coaching/Innovation Confusion — [DETECTED / NOT DETECTED]
[Evidence from manager's description of their interactions]

## Team Composition Analysis
[Star/core/laggard breakdown]
[Where coaching ROI is currently being captured vs. where it should be]

## Time-Reallocation Recommendations
1. [Specific reallocation: e.g., "Shift 15% of time from pipeline review to structured core-rep coaching 1:1s"]
2. [Specific reallocation: e.g., "Replace star coaching sessions with deal-innovation conversations on stuck deals"]
3. [Specific reallocation: e.g., "Reduce resource allocation from 40% to 16% target — delegate CRM reviews"]

## Priority Development Focus
[Single most impactful driver to invest in, with rationale]
[If innovating is the gap: emphasize this is the most overlooked skill in sales management]
```

Keep the artifact factual and specific. Avoid vague recommendations like "coach more." Every recommendation should specify which rep tier, which activity type, and what to reduce to make room.

## Self-Check Before Delivery

Before writing the final artifact, verify:

- Management fundamentals gate was applied — if any fundamental fails, the downstream analysis stops
- All four driver weights are present in the table (27/28/29/16)
- The democratic coaching check is explicit (not just implied)
- Coaching and innovating are assessed separately — not combined
- Recommendations are specific to this manager's team composition and actual time allocation, not generic
- Star/core/laggard ROI is used to justify coaching reallocation recommendations

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

This skill is standalone (no dependencies). To execute a coaching session against the diagnosed gaps, invoke `coach-rep-with-pause-framework`. To plan a team-wide methodology rollout informed by manager diagnoses, invoke `plan-challenger-model-rollout`.
