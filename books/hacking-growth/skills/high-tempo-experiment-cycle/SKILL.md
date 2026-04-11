---
name: high-tempo-experiment-cycle
description: "Use this skill to install a disciplined weekly experimentation cadence for a growth team — the 4-stage high-tempo cycle (Analyze, Ideate, Prioritize, Test) with a timeboxed growth review meeting agenda, idea capture template, and cadence benchmarks. Produces an experiment-cycle-runbook the team can follow from Monday morning, a weekly growth review agenda with named roles and materials, and an idea capture template that feeds the prioritization queue. Triggers when a growth PM asks 'how do I run a weekly growth meeting?', 'our experiments are ad-hoc, how do we systematize?', 'growth meeting agenda', 'high-tempo testing', 'experiment cadence', 'how often should we test?', 'how many experiments per week?', 'weekly growth review', 'Sean Ellis growth meeting', 'growth cycle', 'growth rituals', 'how do I install a test rhythm', or 'our growth team has no rhythm'. Also activates for 'we keep running tests but nothing compounds', 'scattershot experiments', 'growth team operating system', or 'idea bank template'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/high-tempo-experiment-cycle
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [4]
tags:
  - growth
  - experimentation
  - team-operations
  - rituals
  - startup-ops
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: >
        Team context (team-context.md) describing team size, current experiment
        cadence (if any), available tools (analytics, A/B platform), and known
        constraints (meeting time, review authority).
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set. Plan-only — produces a runbook, meeting agenda, and idea
    capture template the team can start using the following Monday.
discovery:
  goal: >
    Install a disciplined weekly experimentation operating rhythm so experiments
    compound into learning rather than dissipating as ad-hoc one-offs.
  tasks:
    - "Gather team context"
    - "Tailor the 4-stage cycle (Analyze → Ideate → Prioritize → Test) to the team"
    - "Draft the weekly growth review meeting agenda with timeboxes"
    - "Produce an idea capture template"
    - "Set a cadence target based on team size and stage"
    - "Emit runbook, agenda, and idea capture template"
---

# High-Tempo Experiment Cycle

Install a disciplined weekly experimentation operating rhythm for a growth team. The cycle converts ad-hoc, isolated tests into a compounding learning machine — each week's results directly feed the next week's experiments, producing gains that grow exponentially rather than evaporating.

The core insight: companies that grow fastest are the ones that learn fastest. A 5% monthly improvement in a key metric compounds to an 80% annual gain. But compounding only happens when experiments build on each other, and that requires a repeatable process.

## When to Use

Use this skill when:
- A growth team is running experiments without a disciplined weekly rhythm
- Tests are being run ad hoc, results are reviewed inconsistently, and learning doesn't carry forward
- A growth PM or head of growth wants a concrete operating cadence to install from day one
- A team is debating how many experiments to run per week
- Leadership wants to know what a "growth meeting" should look like
- A team is hitting the scattershot anti-pattern: lots of effort, no compounding insight

Do not use this skill if the product has not yet established must-have status with a meaningful user segment — install the `product-market-fit-readiness-gate` first.

## Context and Input Gathering

Before producing deliverables, read `team-context.md` and extract:

1. **Team size and roles** — who is on the team (growth lead, data analyst, engineer, marketer, designer), which roles are missing or shared
2. **Current cadence** — how many experiments are running per week, whether there is a regular review meeting, how experiment ideas are submitted today
3. **Tool stack** — what analytics platform is in use (Mixpanel, Amplitude, GA4, etc.), whether an A/B testing platform exists, how ideas are tracked (spreadsheet, Notion, Jira, etc.)
4. **Meeting constraints** — what day and time can the team meet weekly for 60 minutes
5. **Blocking throughput today** — is the bottleneck ideation (too few ideas), prioritization (no scoring), test velocity (engineering backlog), or review (no structured debrief)?

If `team-context.md` is not available, ask the user for these five data points before proceeding.

## Process

### Step 1: Gather Team Context
Read the input document and extract the five data points above. Map the current state to one of three maturity stages:
- **No cadence:** No regular meeting, tests run when someone has time, results reviewed informally
- **Partial cadence:** A meeting exists but lacks structure, or experiments are tracked but not scored
- **Broken cadence:** A process was installed but fell apart — identify which stage broke down

**Why this step cannot be skipped:** The deliverables produced in Steps 3–6 must be calibrated to the team's actual constraints. A 4-person team at 2 tests/week needs a different runbook than a 12-person team targeting 15/week. Producing generic outputs without reading context produces outputs the team will not use.

### Step 2: Install the 4-Stage Cycle

Explain the four stages to the team and define what happens in each. Every stage is required — skipping any one breaks the loop.

**Stage 1 — Analyze (Data Analysis and Insight Gathering)**
Before ideating, the data analyst builds cohort reports and funnel drop-off reports, and the team identifies the most significant gaps or opportunities in the current data. Marketing or research members run any needed user surveys or interviews. All findings are compiled and distributed to the team before the meeting.

*Why this stage cannot be skipped:* Without a structured analysis, the Ideate stage produces guesses rather than data-driven ideas. The cycle's compounding power comes from each round of experiments informing the next — that only happens if results are systematically reviewed before new ideas are generated.

**Stage 2 — Ideate (Idea Generation)**
All team members submit experiment ideas to a shared idea bank using the standardized template (see Step 4). Self-censorship is discouraged. Volume is the goal — most experiments will not produce large wins; finding the few that do is a numbers game. Ideas should eventually flow from colleagues outside the core team and from customers, not only from team members.

*Why this stage cannot be skipped:* Without a formal idea bank that anyone can contribute to at any time, idea generation becomes bottlenecked to whoever shouts loudest in the meeting. The bank decouples contribution from discussion and ensures the team always has a prioritized backlog to draw from.

**Stage 3 — Prioritize (Experiment Prioritization)**
Each idea is scored by its submitter before it enters the pipeline. The ICE framework (Impact, Confidence, Ease — each 1–10, averaged) provides a single comparable score across all ideas. The growth lead reviews scores before the meeting and may suggest modifications. The ranked list is the starting agenda for the selection segment of the growth meeting. ICE score guides but does not dictate — the team can override after discussion.

*Why this stage cannot be skipped:* Without a pre-meeting scoring step, the weekly meeting becomes a debate about which ideas to try rather than a focused decision about the top-ranked options. Prioritization done in the meeting burns the entire meeting's time. Done beforehand, it makes the selection segment crisp and fast.

**Stage 4 — Test (Running Experiments)**
Selected experiments are moved to an "Up Next" queue. Each experiment is assigned an owner responsible for getting it launched. Tests are designed to reach statistical validity (99% confidence level is recommended — at 95%, one in twenty "winning" tests may be a false positive). When results are inconclusive, the default is to stay with the control. Completed test results feed directly back into the next Analyze stage.

*Why this stage cannot be skipped:* The test stage is where the cycle closes. Without it, the analyze and ideate stages produce plans that never ship. Without the 99%-confidence rule and the "control wins ties" rule, the team accumulates false positives that send it down wrong paths.

### Step 3: Draft the Weekly Growth Review Meeting Agenda

The growth meeting runs for 60 minutes, held on a fixed day each week. The book's recommended day is Tuesday, which gives the team Monday to finish prep work. Adapt the day based on the team's constraints, but fix it — a floating meeting day breaks the rhythm.

**Monday prep (growth lead + data analyst):**
- Growth lead reviews experiment velocity from prior week against the team's weekly target
- Data analyst updates the North Star metric and all key metrics being tracked
- Growth lead compiles concluded test data and writes a summary of findings (positive, negative, focus area)
- Combined into a meeting agenda document shared with the team before Tuesday

**60-Minute Tuesday Meeting Agenda:**

| Segment | Duration | Owner | Purpose |
|---|---|---|---|
| Metrics review and update focus area | 15 min | Growth lead | North Star metric status, key positives, key negatives, current focus area (confirm or change) |
| Review last week's testing activity | 10 min | Growth lead | Velocity vs. goal, which tests did not launch and why |
| Key lessons learned from analyzed experiments | 15 min | Growth lead + data analyst + experiment owners | Conclusive results, preliminary results, implications for next steps |
| Select growth tests for current cycle | 15 min | Full team | Discuss nominated experiments, assign owners, set target launch dates |
| Check growth of idea pipeline | 5 min | Growth lead | Pipeline health — number of ideas in queue, call for more ideation if volume is low |

**Critical rule:** The meeting is not for brainstorming. All ideas must be submitted before the meeting via the idea capture template. If brainstorming sessions are needed (e.g., when entering a new focus area), run them separately — monthly is a reasonable cadence.

**Attendees:** Growth lead (facilitator), data analyst, engineer(s), marketer, designer. Meeting notes and the agenda document live in shared cloud storage (Google Docs, Notion, Confluence) as a living document updated each week.

### Step 4: Create the Idea Capture Template

The template must be filled out by the idea submitter before the idea enters the pipeline. Standardizing the format eliminates ambiguity and makes the prioritization meeting fast.

**Required fields:**

```
IDEA NAME:
(Max 50 characters — brief and specific)

DESCRIPTION:
(Cover: Who is targeted? What will be built or changed? Where in the product or funnel
does it appear? When does it trigger for users? Why should it improve the metric?
How will it be tested — A/B test, feature flag, new channel, copy change?)

HYPOTHESIS:
(Simple cause-and-effect: "By [doing X], [metric Y] will improve by [estimated amount].")

METRICS TO MEASURE:
(Primary metric. List downstream metrics that may be affected — improvements in one
metric sometimes come at the expense of others.)

ICE SCORE:
  Impact (1–10):
  Confidence (1–10):
  Ease (1–10):
  Average:
```

*Why standardization matters:* Vague submissions ("our sign-up form is too hard, let's simplify it") cannot be prioritized or evaluated. The template forces clarity on what will be tested, how success will be measured, and how much confidence the submitter has. This is what keeps the idea bank usable at scale.

### Step 5: Set the Cadence Benchmark

Match the team's weekly experiment target to its actual size and stage. Do not set an aspirational target that the team cannot deliver — missed targets demoralize faster than any failed experiment.

| Team Stage | Weekly Target | Notes |
|---|---|---|
| Early (2–4 people, first cycle) | 1–2 experiments/week | Build process discipline before building volume |
| Growing (5–8 people, process established) | 3–8 experiments/week | Increase velocity only after the cycle is running cleanly |
| Mature (10+ people, dedicated tooling) | 10–20 experiments/week | Leading teams run 20–30/week at full maturity |

The ramp from 1–2 to 20+ is a multi-month or multi-year journey. Starting at high volume before the process is solid leads to poor test design, invalid results, and team burnout. Set the initial target based on what the team can implement cleanly, not what they aspire to eventually reach.

### Step 6: Define Sprint Length

Default sprint length is one week. Two-week sprints are permitted if meeting time is genuinely constrained, but they carry a cost: the Analyze stage relies on having fresh results from the previous cycle. With two-week sprints, results are four weeks old by the time they influence the next wave of ideas — the compounding effect weakens.

*Why one-week sprints are strongly preferred:* Each week, the team learns something it can act on the following week. Over a 12-week quarter, that is 12 learning cycles. With two-week sprints, it is 6. The asymmetry compounds over time.

If the team cannot run a full weekly cycle, the minimum viable version is: a fixed weekly meeting with at least one experiment launched each week, even if the Ideate and Analyze stages are lighter.

### Step 7: Emit Deliverables

Write three output files tailored to the team's context:

1. **`experiment-cycle-runbook.md`** — The team's operating manual: the 4-stage cycle with stage-by-stage activities, who does what, how prep works, and the sprint schedule. Should be short enough to read in 5 minutes.

2. **`weekly-growth-review-agenda.md`** — The meeting agenda as a reusable template: date field, the five agenda segments with timeboxes, named owners, materials required beforehand, and space for notes per segment.

3. **`idea-capture-template.md`** — The blank template with all required fields and brief guidance for each. Teams copy this for each new idea submission.

## Key Principles

**Rhythm over volume.** A team running 3 disciplined experiments per week, each properly designed and reviewed, generates more compounding insight than a team running 10 chaotic ones that are never properly analyzed. Install the rhythm first; velocity follows. Volume is a byproduct of a well-oiled process, not a starting condition.

**Analyze first, or experiments don't compound.** The analyze stage is not optional prep — it is what makes the cycle a learning machine rather than a test-running machine. Skipping it means each experiment starts from zero instead of building on the last. The compounding effect that drives exponential growth (a 5% monthly improvement compounds to 80% annually) only activates when each cycle learns from the previous one.

**The meeting is a forcing function, not a status update.** The weekly growth meeting has one purpose: agree on what to test next. Metrics are reviewed so the team knows what to optimize. Results are reviewed so the team learns what worked. The selection segment is the meeting's payoff. If the meeting drifts into status reporting, refocus it. Keep the meeting to 60 minutes — if it regularly runs over, segments are not being respected.

**One-week sprints keep errors from ossifying.** A two-week cycle means a bad experiment runs for two weeks before the team recalibrates. A one-week cycle means the team corrects course every seven days. The faster the feedback loop, the smaller the mistakes. Over a quarter, a one-week cadence produces 12 learning cycles; a two-week cadence produces 6.

**Anti-pattern — scattershot experimentation.** Running tests without the cycle — ad hoc, without scoring, without structured review — burns team effort and produces no compounding insight. Each test is an island. Teams in this pattern often conclude that systematic testing does not work for their company when the actual problem is the absence of the cycle, not the absence of good ideas. The cycle is the antidote.

**The idea bank is the team's most valuable asset.** A deep, well-scored pipeline means the team never wastes meeting time debating what to try. It also means that a failed experiment is never a dead end — the next ranked idea is already ready. Protect the pipeline: if ideation volume drops, the whole cycle slows.

**Statistical discipline protects the learning.** Each experiment run comes at the cost of another candidate not being tested. A poorly designed test — one that reaches false-positive results due to insufficient confidence thresholds — sends the team down a wrong path and wastes future cycles. Set a 99% confidence threshold on A/B tests. When results are genuinely inconclusive, the control version wins.

## Examples

### Example 1: Series A Team of 4, Starting from Zero

**Scenario:** A SaaS startup with 4 people on the growth team — a growth PM (also the growth lead), a data analyst, a full-stack engineer, and a marketer. No current cadence. Experiments have been run ad hoc when one of the founders had an idea. Results are rarely reviewed. The team has Mixpanel for analytics and uses Google Sheets for experiment tracking.

**Trigger:** The growth PM says: "We're running tests but nothing compounds. We need a system."

**Process:**
1. Growth PM reads `team-context.md` and identifies: no meeting cadence, no idea scoring, analytics in place but no formal funnel reporting.
2. The 4-stage cycle is installed with a one-week sprint. The data analyst is tasked with building a weekly funnel report to distribute every Monday.
3. Meeting scheduled for Tuesdays at 10am. Monday prep: growth lead + analyst prepare the metrics brief and compile any concluded test results.
4. A Google Sheet is set up as the idea pipeline with the idea capture template as each row's structure.
5. Cadence target: 2 experiments per week. This is achievable given the engineer's bandwidth.
6. First deliverable: a 2-page runbook the team reads before the first meeting.

**Output:** `experiment-cycle-runbook.md` (tailored to a 4-person team with Google Sheets pipeline), `weekly-growth-review-agenda.md` (Tuesday, 10am, 60 min, 5 segments), `idea-capture-template.md` (Google Sheet row template).

**Expected outcome at 4 weeks:** Team has run 6–8 experiments. At least one conclusive result is in the bank. The meeting runs to time consistently. Ideas are flowing into the pipeline between meetings rather than only surfacing in the meeting itself.

### Example 2: Series B Team of 12, Shifting from Chaos to Discipline

**Scenario:** A marketplace startup with 12 people across two growth squads — one focused on acquisition, one on retention. Each squad runs 5–6 experiments per week but without a shared scoring system or a consistent review meeting. Experiments from the acquisition squad often conflict with retention squad tests because there is no shared pipeline. The team uses Amplitude and Optimizely.

**Trigger:** The head of growth says: "We're running 10 tests a week but I have no idea which ones are actually working or why. We need a shared operating system."

**Process:**
1. Context review reveals: dual squad structure, no shared idea pipeline, no unified meeting, high test volume but low review discipline.
2. The skill recommends a unified weekly meeting with both squad leads presenting their results, plus a shared idea pipeline in Optimizely's project management feature.
3. ICE scoring is introduced as a required pre-submission step. Squads' ideas compete for prioritization in a shared queue filtered by focus area.
4. Cadence target raised from 10/week to 15/week — but with a new quality gate: each experiment must have a pre-written hypothesis and a designated metrics owner before it launches.
5. Meeting agenda adapted: the "lessons learned" segment expands to 20 minutes to cover both squads, the "select tests" segment includes a focus-area filter to ensure squads aren't running conflicting tests on the same funnel stage.

**Output:** `experiment-cycle-runbook.md` (dual-squad variant with shared pipeline protocol), `weekly-growth-review-agenda.md` (adapted 60-min agenda with dual squad coverage), `idea-capture-template.md` (with squad field and focus-area tag added).

**Expected outcome at 4 weeks:** Both squads have a shared idea bank with 30+ ideas scored and ranked. Experiment conflicts across squads have been eliminated via the shared focus-area tag. Velocity has increased from ~10/week to 13–15/week while average test quality has improved.

## Common Failure Modes to Diagnose

When the cycle is installed but is not producing results, check these failure modes first:

| Symptom | Root cause | Fix |
|---|---|---|
| Meeting runs over 60 minutes | Brainstorming happening in the meeting | Move ideation to async; enforce the "no brainstorming in the meeting" rule |
| Idea pipeline is always empty before the meeting | Team is submitting ideas only in the meeting | Make idea submission a daily habit; growth lead primes the pipeline between meetings |
| ICE scores are inflated (everything is 8+) | Submitters are not calibrating against past experiments | Growth lead reviews and challenges scores before the meeting |
| Tests are never concluded | Insufficient sample size, or no one owns the conclusion | Assign each test a target conclusion date and a metrics owner at launch |
| Results are never acted on | Analyze stage skipped; conclusions not fed back into ideation | Make Monday prep mandatory; growth lead writes a summary of implications, not just results |

## Calibration Questions

Before finalizing the runbook, ask the growth lead these calibration questions to ensure the deliverables fit the team's reality:

1. **Who has authority to launch an experiment without additional approval?** If every experiment requires sign-off from a VP or CTO, the cycle will slow to a crawl. Identify what can be shipped autonomously and what requires a fast-track approval path.

2. **What is the team's current statistical tooling?** Teams without an A/B testing platform (Optimizely, VWO, split.io, LaunchDarkly, etc.) will need to route experiments through engineering feature flags or run sequential rather than concurrent tests. Adjust the cadence target accordingly.

3. **Is there an existing experiment backlog?** If ideas already exist (in Slack threads, docs, or a PM's notebook), start by formalizing them into the idea capture template before the first meeting. A seeded pipeline makes the first meeting's selection segment immediately productive.

4. **Who will own the Monday prep?** If the growth lead and data analyst are the same person, or if the analyst is part-time, Monday prep will be the bottleneck. Plan for it explicitly in the runbook.

## References

- ICE scoring details and worked examples: `../../references/ice-scoring-guide.md` *(if built)*
- Meeting facilitation best practices: `../../references/meeting-facilitation.md` *(if built)*
- Statistical validity for A/B tests: 99% confidence level rule and "control wins ties" rule come from Chapter 4.
- Source chapter: *Hacking Growth* Chapter Four, "Testing at High Tempo" — full cycle, meeting agenda, and cadence benchmarks.

## License

CC-BY-SA-4.0. Derived from *Hacking Growth* by Sean Ellis and Morgan Brown. You are free to share and adapt this skill with attribution and under the same license.

## Related BookForge Skills

This skill works within a system. Install these companion skills for the full operating foundation:

```
# The metric the cycle orients around
clawhub install bookforge-north-star-metric-selector

# The ICE scoring step of the cycle, as a standalone tool
clawhub install bookforge-growth-experiment-prioritization-scorer

# Install a team before installing a cadence
clawhub install bookforge-growth-team-structure-planner

# Verify PMF before starting the cycle
clawhub install bookforge-product-market-fit-readiness-gate
```
