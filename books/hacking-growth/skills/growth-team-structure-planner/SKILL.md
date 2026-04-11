---
name: growth-team-structure-planner
description: "Use this skill to design a cross-functional growth team for a Series A–B scaling startup and produce a concrete proposal the growth lead can bring to their executive team. Recommends product-led (growth team embedded in product) vs independent (standalone growth team reporting to CEO or VP Growth) based on org context, assigns named roles (growth lead, PM, engineer, designer, data analyst, marketer), defines executive sponsorship requirements, and drafts a kickoff meeting agenda. Triggers when user asks 'how do I structure a growth team?', 'should growth be under product or standalone?', 'who should be on my growth team?', 'what roles does a growth team need?', 'how do I pitch a growth team to my CEO?', 'growth team kickoff', 'first growth hire', 'growth team model', or 'building a growth team from scratch'. Also activates for 'our marketing and product aren't aligned on growth', 'we need a growth function but don't know how to structure it', 'growth team charter', or 'growth team proposal'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/growth-team-structure-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [1]
tags:
  - growth
  - team-structure
  - startup-ops
  - organizational-design
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: >
        Org context describing company stage (Series A–B), existing functions
        (product, engineering, marketing, data), reporting lines, known political
        constraints, and the CEO/exec team's appetite for growth investment.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set. Plan-only — produces a proposal document and kickoff agenda
    for human review and exec presentation. No code execution.
discovery:
  goal: >
    Produce a defensible growth team proposal (team model, roles, sponsorship,
    kickoff agenda) that a growth lead can take to their CEO.
  tasks:
    - "Gather org context from user"
    - "Recommend product-led vs independent model with rationale"
    - "List named roles with job description stubs"
    - "Define executive sponsorship requirements"
    - "Draft kickoff meeting agenda"
    - "Produce growth-team-proposal.md and kickoff-agenda.md"
---

# Growth Team Structure Planner

Design a cross-functional growth team proposal that a Growth PM or Head of Growth
can bring to their executive team. Produces two ready-to-present documents:
`growth-team-proposal.md` (model rationale, roles, sponsorship plan) and
`kickoff-agenda.md` (first team meeting, structured to align on North Star,
growth levers, and velocity commitment).

## When to Use

Use this skill when you are tasked with building or proposing a growth team and
need to make an org design decision (product-led vs independent), staff it with
the right cross-functional roles, secure executive buy-in, and run a first meeting
that sets the team up to experiment immediately.

This skill is appropriate before running any growth experiments. It precedes
`north-star-metric-selector` (metric alignment) and `high-tempo-experiment-cycle`
(weekly experimentation cadence). Use it when you have product-market fit signals
but no structured growth function yet.

Not appropriate for: teams already operating with a defined growth process, or
companies pre-product-market fit (growth investment at that stage is premature).

---

## Context and Input Gathering

Before producing the proposal, collect this information from the user. Ask for
it directly if org-context.md has not been provided.

**7 questions to ask:**

1. **Company stage and headcount:** Series A or B? How many people total, and
   roughly how many in product, engineering, marketing, and data?

2. **Existing growth ownership:** Who currently owns metrics like activation rate,
   retention, and revenue? Is it distributed across departments or does someone
   own it end-to-end?

3. **Reporting lines:** Does the CEO have direct involvement in growth decisions?
   Is there a VP Product, VP Marketing, or VP Engineering who would be the natural
   exec sponsor?

4. **Political constraints:** Are there known turf tensions between product and
   marketing? Has a previous cross-functional initiative failed? Who would resist
   a growth team and why?

5. **Budget and hiring authority:** Is this team assembled from existing staff,
   new hires, or a mix? Does the growth lead have a headcount budget?

6. **Product complexity:** Single product or multiple? One audience or several?
   This determines whether scope should be narrow (one product area) or broad
   (all growth levers).

7. **Exec alignment:** Has the CEO or a C-level executive explicitly endorsed
   a growth investment? Or does this proposal need to make the case from scratch?

---

## Process

### Step 1 — Classify the org (WHY: the two structural models have opposite tradeoffs; choosing wrong costs months of political friction)

Evaluate the org context against two models identified from Silicon Valley growth
team research (McInnes and Miyoshi):

**Product-Led (Functional) Model:**
- Growth team reports to a product management executive
- Scope limited to one product or one area of the product
- Works within existing hierarchy — minimal reorganization required
- Appropriate when: company has an established product org, multiple products with
  distinct PMs, or when political resistance to a standalone function is high
- Examples: Pinterest (four growth subteams under product), LinkedIn, Twitter, Dropbox

**Independent (Stand-Alone) Model:**
- Growth team is separate from product; growth lead reports to VP Growth or CEO
- Authority spans all products and functional areas
- Requires reorganization or new reporting lines
- Appropriate when: single product company, CEO is the sponsor, growth must cut
  across all silos without permission overhead, or company is early enough that
  org structure is still fluid
- Examples: Facebook, Uber

**Decision matrix:**

| Signal | Product-Led | Independent |
|--------|-------------|-------------|
| CEO actively involved in growth decisions | Either | Prefer Independent |
| Multiple products, established PM org | Prefer Product-Led | — |
| Single product, one core metric | — | Prefer Independent |
| High cross-functional friction expected | Prefer Product-Led (less disruption) | — |
| Growth must span marketing + product + data | — | Prefer Independent |
| Series A, <50 people | — | Prefer Independent |
| Series B, 50–200 people | Prefer Product-Led | Either |

Document the recommended model and the two or three org-context signals that drove
the recommendation. This becomes Section 1 of `growth-team-proposal.md`.

### Step 2 — Define the team roster (WHY: under-specifying roles is how growth teams become everyone's side project and no one's responsibility)

List each role with name, function source (which existing team they come from or
whether they are a new hire), time commitment, and key responsibilities.

**Core six roles:**

| Role | Source | Minimum commitment | Core responsibility |
|------|--------|--------------------|---------------------|
| Growth Lead | New hire or internal promotion | Full-time | Sets focus area and objectives, runs weekly growth meeting, monitors experiment velocity, owns North Star metric |
| Data Analyst | Data/BI team | Full-time or 80% | Builds cohort reports and funnel reports, compiles experiment results, identifies metric drop-off points, prepares weekly analytics brief |
| Engineer | Engineering team | Full-time (dedicated, not on loan) | Implements experiment code, builds A/B test infrastructure, runs technical variants |
| Marketer | Marketing team | Full-time or 60% | Runs promotional channel experiments (paid, email, content), implements channel-level tests |
| Designer | Design/UX team | 50% minimum | Designs experiment variants, collects qualitative user feedback, evaluates feature usability |
| Product Manager | Product team | 50% minimum (optional at Series A) | Coordinates experiment dependencies with product roadmap, manages stakeholder alignment |

**Minimum viable team (Series A, <30 people):** Growth Lead + Data Analyst +
Engineer + Marketer. Designer and PM fold into existing roles.

**Growth team sizing examples:**
- IBM Bluemix growth team: 5 engineers + 5 operations/marketing staff
- Inman News: data scientist + 3 marketers + web developer + COO (growth lead)
- Series A typical: 4–6 people, mostly reallocated from existing departments

Document each role as a one-paragraph job description stub. This becomes
Section 2 of `growth-team-proposal.md`.

### Step 3 — Specify executive sponsorship (WHY: growth without executive sponsorship dies within six months — teams hit departmental resistance on their first cross-functional experiment and have no one to clear the path)

Growth teams need authority to cross established departmental boundaries. Without
a named exec sponsor who can resolve turf conflicts at the C-suite level, teams
get blocked by brand guidelines, product roadmap locks, and budget gatekeeping.

**Sponsorship requirements by company stage:**

- **Series A / founder-led:** CEO or founder is the sponsor. Non-negotiable.
  If the CEO won't sponsor it, growth investment is premature. The sponsor
  attends the kickoff meeting and the first four weekly growth meetings to
  signal organizational commitment.

- **Series B / professional management team:** VP Growth, VP Product, or COO
  is the sponsor. The sponsor has cross-suite authority — meaning they can
  authorize the growth team to run experiments that touch marketing assets,
  product features, and pricing without needing separate approvals from each
  department head.

**Sponsorship operating model:** The exec sponsor is not a day-to-day manager.
Their role is: (a) clear political blockers when the growth team's experiments
conflict with other departments, (b) attend growth meeting reviews quarterly
to assess progress against North Star, and (c) protect growth team headcount
and budget from reorganizations.

Document sponsor name (or title if not yet identified), their authority scope,
their attendance commitment for the first 90 days, and the escalation path when
experiments hit departmental resistance. This becomes Section 3 of
`growth-team-proposal.md`.

### Step 4 — Define scope and operating parameters (WHY: an unbounded growth mandate paralyzes new teams — a narrow first scope builds credibility before expanding)

For the first 90 days:

1. **Scope:** Choose one area — one product, one funnel stage (e.g., activation),
   or one metric (e.g., D7 retention). Do not attempt to cover all growth levers
   in the first quarter.

2. **Permanence:** Propose the team as permanent, not project-based. Project-based
   growth teams lose institutional knowledge when disbanded and restart from zero.
   Document the intended permanence.

3. **Experiment velocity target:** Start with 1–2 experiments per week. Scale to
   10–20 as team builds confidence. Document the week-1 velocity commitment.

4. **Reporting cadence:** Weekly growth meeting (all team members). Monthly
   North Star review with exec sponsor. Quarterly scope reassessment.

This becomes Section 4 of `growth-team-proposal.md`.

### Step 5 — Draft the kickoff meeting agenda (WHY: the kickoff is the team's first shared contract — it aligns everyone on process, metric, and velocity before the first experiment, preventing the chaos of undirected early experiments)

The kickoff is the first growth team meeting. It should run 90–120 minutes and
produce four shared commitments.

**Kickoff agenda structure:**

**Opening (15 min)**
- Growth lead explains the growth hacking methodology: continuous cycle of
  Analyze → Ideate → Prioritize → Test
- Growth lead clarifies each team member's role and what they own

**Charter review (20 min)**
- Review the recommended team model and why it was chosen
- Review scope boundaries: what is in scope for the first 90 days, what is not
- Review exec sponsorship: who the sponsor is, how escalation works

**North Star commitment (20 min)**
- Data analyst presents initial analysis: current state of the primary metric,
  known drop-off points, baseline cohort data
- Team discusses and commits to the North Star metric
  (if not yet selected, flag that `north-star-metric-selector` runs first)
- Growth lead documents the agreed North Star in writing during the meeting

**First experiment discussion (30 min)**
- Data analyst presents two or three high-priority areas surfaced by initial analysis
- Team generates ideas for first experiments using brainstorm format
  (no filtering yet — quantity over quality)
- Team agrees on a velocity goal: how many experiments to run in week 1–2

**Cadence agreement (15 min)**
- Confirm weekly growth meeting day and time
- Confirm monthly exec sponsor review date
- Assign owner for first experiment submission

This becomes `kickoff-agenda.md`, formatted as a shareable meeting doc with
blank sections for participants to fill in during the meeting.

### Step 6 — Produce output documents (WHY: a verbal proposal evaporates — a written document survives the exec review cycle and serves as the team's founding charter)

Write two files:

**growth-team-proposal.md** containing:
- Section 1: Recommended team model with decision rationale (2–3 signals)
- Section 2: Role roster with one-paragraph stubs per role
- Section 3: Executive sponsorship — named sponsor, authority scope, 90-day attendance
- Section 4: Scope, permanence, velocity target, reporting cadence
- Section 5: What success looks like in 30 / 60 / 90 days

**kickoff-agenda.md** containing:
- Meeting details: date, attendees, facilitator
- All five agenda blocks with time allocations
- Blank fields for team to complete during the meeting:
  - Agreed North Star metric: ___
  - Week-1 velocity goal: ___ experiments
  - First experiment owner: ___
  - Weekly meeting cadence: ___

---

## Key Principles

1. **Growth without executive sponsorship dies in six months.** The first cross-
   functional experiment will hit departmental resistance. Without a named sponsor
   who can clear the path at the C-suite level, the team burns its credibility
   on internal politics instead of experiments.

2. **Product-led vs independent is not about quality — it's about org physics.**
   Neither model is better. The right model is the one that generates the least
   political friction given the company's existing reporting lines and the CEO's
   appetite for disruption.

3. **The engineer must be dedicated, not on loan.** Growth teams that share
   engineers with product squads will lose those engineers to roadmap emergencies
   within weeks. Experiment velocity requires a committed engineer who can push
   code on the growth team's schedule, not product's.

4. **Start narrow, expand after wins.** The first scope should be one product
   area or one funnel stage. A single, visible win in a narrow area converts
   skeptical department heads into advocates faster than a broad mandate with
   diffuse results.

5. **The kickoff meeting is the team's founding contract.** Every team member
   must leave the kickoff with a shared understanding of: the North Star metric,
   the velocity target, and who owns what. An unstructured kickoff produces
   an unstructured team.

6. **Resist the urge to outsource the core.** External consultants can add
   specialist expertise (e.g., a paid acquisition specialist), but internal
   product knowledge cannot be hired in. The growth lead must be deeply familiar
   with the product and the customer.

---

## Examples

### Example 1 — Series A SaaS, Product-Led Model

**Scenario:** 35-person Series A SaaS company. Product team (5 engineers, 2 PMs),
marketing team (3 people), one data analyst. CEO is focused on fundraising.
VP Product has strong exec presence and wants to own growth.

**Trigger:** Head of Growth (newly hired) asked to propose a team structure before
their first 30-day review.

**Process:** Org context signals point to product-led model — established PM org,
VP Product as natural sponsor, CEO bandwidth is limited, and realigning reporting
lines would require board approval. Growth lead reports to VP Product. Team roster:
growth lead (new hire) + one dedicated engineer (from product team) + marketer
(from marketing, 80% allocation) + data analyst (full-time, from existing team).
Designer is shared at 50%. Scope: activation funnel only (D7 retention is the
North Star). Velocity target: 2 experiments per week.

**Output:** `growth-team-proposal.md` with VP Product named as sponsor and
authority to approve experiments touching onboarding flow and email without
separate product team sign-off. `kickoff-agenda.md` with first experiment
discussion focused on onboarding drop-off points surfaced by data analyst.

---

### Example 2 — Series B B2C, Independent Model

**Scenario:** 90-person Series B consumer app. Four product squads (acquisition,
activation, retention, monetization), large marketing team, CEO actively engaged
in growth decisions. Marketing and product have friction over campaign attribution.

**Trigger:** CEO asks Head of Growth to propose a standalone growth function that
can run cross-funnel experiments without requiring approvals from each squad PM.

**Process:** Independent model is the clear fit — growth must span four existing
squads, CEO is the sponsor and has expressed willingness to create a new reporting
line, and the cross-departmental friction is exactly what the independent model
is designed to break through. Growth lead reports to CEO directly. Team: growth
lead + two dedicated engineers + data analyst + marketer + UX designer, all
full-time. Scope: North Star metric is weekly active engagements (WAE); first
90-day focus is top-of-funnel acquisition conversion. Velocity target: 5
experiments per week by end of month 1.

**Output:** `growth-team-proposal.md` establishing the growth team as a permanent
standalone unit with CEO sponsorship letter attached. `kickoff-agenda.md` including
all four squad PMs as observers for the first meeting to signal that the growth
team has cross-functional authority, not just advisory status.

---

## References

- `references/growth-team-model-comparison.md` — Side-by-side comparison of
  product-led vs independent models with full criteria table
- `references/role-definitions.md` — Expanded job description templates for all
  six growth team roles
- `references/kickoff-facilitation-guide.md` — Facilitator notes for running
  the kickoff meeting including common objections and how to handle them

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Hacking Growth* by Sean Ellis and Morgan Brown.

---

## Related BookForge Skills

After structuring your team, install the operating system:

- `clawhub install bookforge-north-star-metric-selector` — pick the metric the team will orient around
- `clawhub install bookforge-high-tempo-experiment-cycle` — install the weekly experimentation cadence
- `clawhub install bookforge-product-market-fit-readiness-gate` — confirm PMF before investing in team

Browse more: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
