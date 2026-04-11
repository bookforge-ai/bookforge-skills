---
name: north-star-metric-selector
description: "Use this skill to construct a growth equation for a product and select a defensible North Star Metric that actually reflects core value delivery — rejecting vanity metrics (DAU, total signups, pageviews) that feel like growth but don't compound. Produces the full multiplicative growth equation (acquisition × activation × retention + monetization + referral) and a scored shortlist of NSM candidates with rationale, then recommends one. Triggers when a growth PM or head of growth asks 'what should our north star metric be?', 'help me pick a north star', 'is DAU the right metric?', 'my team is chasing vanity metrics', 'we're orienting around the wrong metric', 'how do I build a growth equation', 'what's our key growth metric', 'OMTM one metric that matters', 'north star framework', or 'growth equation for [product type]'. Also activates for 'WhatsApp messages sent as north star', 'Airbnb nights booked', 'north star vs input metrics', or 'why DAU is misleading'. Use AFTER product/market fit is confirmed — this metric orients every downstream growth experiment."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/north-star-metric-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [3]
tags:
  - growth
  - metrics
  - north-star
  - product-marketing
  - startup-ops
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: >
        Product brief (product-brief.md) describing product, ICP, core value prop,
        current stage, and the user's hypothesis of the aha moment.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set. Plan-only — produces markdown deliverables (north-star-recommendation.md
    and growth-equation.md). No code execution.
discovery:
  goal: >
    Produce a defensible north-star-recommendation.md and growth-equation.md that
    the team can orient around for the next 6-12 months of experimentation.
  tasks:
    - "Read product brief and confirm aha moment"
    - "Construct the multiplicative growth equation with stages"
    - "Enumerate candidate NSM variables"
    - "Apply rejection criteria (vanity, proxy, short-term)"
    - "Score survivors against must-have experience criterion"
    - "Recommend primary NSM + 2-3 input metrics"
    - "Emit deliverables"
---

# North Star Metric Selector

## When to Use

You are a growth PM, head of growth, or founder at a post-PMF startup (Series A–B) and need to answer the question: *what is the one metric that should orient all growth experimentation for the next 6–12 months?*

This skill applies when:

- Your team is debating between several metrics and can't align on which to track
- You suspect the current orienting metric (DAU, total signups, GMV, pageviews) is a vanity metric that can rise while the business stagnates
- You are setting up your growth team and need a North Star before running the first experiment cycle
- You have PMF confirmed (40%+ "very disappointed" on the must-have survey, stable retention curve) and are ready to scale
- Someone on your team challenges whether the current metric captures real value delivery, and you need a structured argument

Do not use this skill before confirming product/market fit. Selecting a North Star before PMF creates false precision — you will orient a team around the wrong signal.

---

## Context and Input Gathering

Before running the process, confirm the following from the product brief:

1. **Product description** — what does the product do, for whom, in what context?
2. **Core value proposition** — what problem is definitively solved for the ideal customer?
3. **Aha moment** — the specific moment a new user first experiences the core value. If the brief does not name it, ask: "At what point does a new user stop wondering whether this is worth it?" Note: the aha moment was identified during PMF validation (see `product-market-fit-readiness-gate`).
4. **Business model** — subscription, marketplace, transactional, freemium, ad-supported? This shapes which equation variables matter.
5. **Current orienting metric** — what metric is the team currently chasing? Why? This is the candidate for rejection.

If the product brief is missing any of these, ask before proceeding. A growth equation built on an assumed aha moment is fragile.

---

## Process

### Step 1: Confirm the Must-Have Experience

Identify and state the aha moment in a single sentence: *"The aha moment is [action] that delivers [core value] to [ICP] at [trigger point]."*

**Why this step:** The North Star must reflect whether users are experiencing this moment — not whether they are merely present. Every downstream selection decision anchors on this sentence. If you skip this confirmation and proceed to equation construction, you risk selecting a metric that measures activity rather than value delivery.

Examples of correctly stated aha moments:
- "Sending a message to a friend in another country for free, immediately" (messaging app)
- "Finding and booking accommodation in a new city within 10 minutes" (marketplace)
- "Seeing my pipeline update automatically without entering data manually" (B2B SaaS)

### Step 2: Construct the Growth Equation

Build the product's fundamental growth equation — a multiplicative formula that expresses all core growth levers.

**Template structure:**
```
[Acquisition input] × [Activation conversion] × [Engagement depth/frequency]
  + Retained [users/subscribers/buyers]
  + Resurrected [lapsed users who returned]
= [Growth output metric]
```

The exact variables depend on the business model. The additive structure (+Retained +Resurrected) is not optional — making retention and resurrection explicit forces the team to treat them as levers, not background assumptions.

**Worked Example A — B2B SaaS (project management tool):**
```
New Trial Signups
  × Trial-to-Seat Activation Rate
  × Seats per Account
  × Weekly Active Seats (depth-of-use)
  + Retained Paying Accounts
  + Resurrected Churned Accounts
= ARR Growth
```

**Worked Example B — Consumer Marketplace (short-term rentals):**
```
New Host Listings
  × Listing Quality Rate (photos, description completeness)
  × Guest Search Sessions
  × Booking Conversion Rate
  + Retained Repeat Guests
  + Resurrected Dormant Guests
= Nights Booked
```

**Worked Example C — Subscription Media:**
```
Monthly Website Traffic
  × Email Capture Rate
  × Active Reader Rate (opens content ≥ 2x/week)
  × Paid Subscriber Conversion Rate
  + Retained Paid Subscribers
  + Resurrected Lapsed Subscribers
= Subscriber Revenue Growth
```

**Why this step:** The growth equation makes growth levers explicit and countable. Without it, "grow the business" is the strategy. With it, the team can see exactly which stage is the weakest link and focus experimentation there. The equation also produces the candidate pool for NSM selection in Step 3.

### Step 3: Enumerate NSM Candidates

Extract the key variables from the equation. These are the candidate North Star metrics. Every variable in the equation is a candidate — including the output metric itself, the conversion rates, the depth-of-use variables, and the retained/resurrected terms.

List each candidate explicitly. For the B2B SaaS example above, candidates include: trial signups, weekly active seats, seats per account, booking conversion rate, retained paying accounts, ARR.

**Why this step:** Teams often skip straight to the output metric (ARR, GMV) and miss that an intermediate variable — one that more precisely captures the aha moment — is the better North Star. You cannot make that judgment without seeing all candidates in one view.

### Step 4: Apply Rejection Criteria

Run each candidate through four rejection filters. A metric that fails any filter is disqualified from North Star selection. It may survive as an input metric.

**Filter 1 — Vanity metric check:**
*Can this metric rise while core value delivery to users stays flat or declines?*
If yes, reject. Total signups can rise via an aggressive acquisition campaign even if zero users reach the aha moment. Pageviews can increase via SEO while user engagement craters. Daily active users can be inflated by notification spam.

**Filter 2 — Proxy check:**
*Is this metric measuring the activity that produces value, or the value itself?*
If it measures activity only, reject as a standalone NSM (it becomes an input metric). New trial signups measures acquisition activity, not value delivery. The variable that captures value delivery is the one closest to the aha moment in the equation.

**Filter 3 — Frequency mismatch check:**
*Does the natural frequency of the metric match how often users actually experience the core value?*
If not, reject. A short-term rental platform cannot use daily active users as its North Star — even loyal users book stays only a few times per year. A review platform cannot use daily visits — genuine users search weekly at most. Forcing a daily metric onto a low-frequency product makes the metric impossible to move and misaligned with actual usage patterns.

**Filter 4 — Short-term inflation check:**
*Can the metric be moved quickly through tactics that don't improve the underlying product?*
If yes, reject as the primary NSM. A metric vulnerable to gaming (login streaks, notification-driven opens, discount-triggered purchases) should be monitored as an input metric, not the orientation point for the team.

**Named failure modes:**
- DAU for WhatsApp: fails Filter 3. A user can be daily-active but send only one message. DAU doesn't capture whether WhatsApp is actually the user's primary messaging channel.
- Total registrations for a marketplace: fails Filter 1. Registrations rise whenever an acquisition campaign runs, regardless of whether any transaction occurs.
- GMV without repeat purchases: fails Filter 2 if the aha moment is repeat value (a user who buys once and never returns didn't fully experience the core value).

### Step 5: Score Surviving Candidates

For candidates that pass all four rejection filters, score each on a 1–5 scale across four criteria:

| Criterion | Score 5 | Score 1 |
|-----------|---------|---------|
| Reflects must-have experience | Directly measures the aha moment | Measures a downstream proxy |
| Actionable by the team | Team has clear levers to move it | Driven by factors outside team control |
| Survives 6-12 months | Relevant at 2x current scale | Likely to become obsolete within 3 months |
| Honest signal | Hard to inflate without real value delivery | Easy to game with tactics |

Sum the scores. The highest scorer is the primary NSM recommendation.

**Why this step:** When two candidates both pass the rejection filters, subjective debate replaces rigor. A scored comparison makes the selection defensible to the executive team and creates a record of why candidates were accepted or rejected.

### Step 6: Recommend Primary NSM and Input Metrics

Produce:

1. **Primary NSM:** the highest-scoring survivor from Step 5, stated as a specific, measurable quantity with a time dimension. Example: "Messages sent per active user per week" rather than "messages sent."

2. **2-3 Input metrics:** the upstream variables in the growth equation that the team's experiments will directly manipulate to move the NSM. Input metrics are the levers; the NSM is the outcome. They are not the same. Experiments target input metrics; success is confirmed by movement in the NSM.

3. **Explicit rejects:** list the 1-2 most tempting metrics that were rejected and why. This is as important as the recommendation — it prevents the team from reverting to vanity metrics when the NSM is hard to move.

**Why this step:** Teams that select only the NSM without naming input metrics have no operational plan. Teams that confuse input metrics for the NSM lose the north-star property — the metric becomes gameable. The distinction is critical.

### Step 7: Emit Deliverables

Write two output files:

**`north-star-recommendation.md`**
- Product name and aha moment (confirmed in Step 1)
- Primary NSM: name, definition, measurement method, current baseline
- Rationale: why this metric, why not the top 2 rejected candidates
- Input metrics: 2-3 with measurement method and team ownership
- Review cadence: recommend quarterly NSM review at minimum (the right metric may change as the company matures)

**`growth-equation.md`**
- Full equation in the multiplicative + additive template format
- Variable definitions: one sentence per variable explaining what it measures and how to instrument it
- Current values where known, gaps where not yet instrumented
- Stage diagnosis: which stage of the equation currently has the weakest conversion? This is the starting point for the first experiment cycle.

---

## Key Principles

1. **The guiding question is singular:** "Which variable in the growth equation most accurately represents the delivery of the must-have experience?" Everything else is a supporting question.

2. **Input metrics are levers; the NSM is the outcome.** The growth team pulls input metrics (trial conversion rate, onboarding completion, feature adoption). The NSM tells them whether pulling those levers is working. Conflating the two — treating an input metric as the North Star — makes the metric gameable and disconnects it from real value delivery.

3. **The right NSM changes at different company stages.** A metric that captures core value delivery for a 10,000-user product may become irrelevant at 10 million users. Early-stage Facebook correctly oriented around MAU to prove reach; later-stage Facebook correctly shifted to DAU as engagement became the constraint. Build a quarterly review into the process.

4. **If your NSM can go up while your business goes down, it's wrong.** This is the litmus test for vanity metrics. Run the test on your current metric before the process — it will confirm whether the problem is worth solving.

5. **The growth equation forces retention and resurrection into view.** The additive structure (+ Retained + Resurrected) is not decorative. Without it, teams treat retention as a passive background condition and allocate all experiments to acquisition. Seeing retained and resurrected users as explicit equation variables changes the allocation decision.

6. **The North Star creates the right disagreements.** A well-chosen NSM generates productive debates: "Why didn't this experiment move the NSM even though the input metric improved?" That disagreement surfaces disconnects between levers and outcomes. A vanity metric generates false confidence: "The number went up" — end of discussion.

---

## Examples

### Consumer Marketplace — Accommodation Platform

A short-term rental platform with strong early adopter retention asked: "Should we orient around DAU, total listings, or something else?"

The aha moment: a guest successfully books unique accommodation in their destination city within a single session. The growth equation revealed the core stages: listings (supply) × search sessions (demand) × booking conversion × guest satisfaction → repeat bookings. Nights booked was the only variable that captured both supply and demand satisfaction simultaneously — a night booked means a host listed a quality property AND a guest found and committed to it. Orienting around nights booked also surfaced a non-obvious lever: professional photography increased listing quality, which increased booking conversion in lagging markets. DAU would never have revealed this lever — the metric couldn't distinguish between users who browsed and abandoned from users who completed bookings.

Input metrics: listing completion rate, search-to-booking conversion rate, average listings per active market.

### B2B SaaS — Team Collaboration Tool

A project management SaaS with a freemium model was orienting around monthly active users (MAU). The growth team suspected this was the wrong metric because MAU was rising while paid conversion was flat.

The aha moment: a team lead sees their entire team's tasks update in real time without anyone logging data manually. The growth equation exposed the gap: trial signups × team activation rate (≥3 members completing setup) × weekly collaborative sessions × conversion to paid. MAU failed the vanity metric check — a single user opening the app weekly counted as "active" even if they never invited their team, which meant they never experienced the aha moment. The better North Star: weekly collaborative sessions per team (defined as ≥2 members using a shared project in a 7-day window). This metric could not rise without teams actually collaborating, which is precisely the must-have experience.

Input metrics: team invite completion rate, shared project creation rate, integration setup completion.

---

## References

- `research/north-star-metric-selector.md` — source passages and company-specific examples from Chapter 3
- `references/growth-equation-examples.md` — additional worked growth equations by business model
- `orchestration/specs/skill-spec.md` — BookForge skill authoring standards

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Hacking Growth* by Sean Ellis and Morgan Brown.

---

## Related BookForge Skills

This skill is the foundation of the Hacking Growth operating system — most downstream skills consume the North Star metric it produces:

- `clawhub install bookforge-growth-experiment-prioritization-scorer` — score experiments by predicted impact on this NSM using the ICE framework before committing any team time
- `clawhub install bookforge-activation-funnel-diagnostic` — diagnose which stage of the growth equation is leaking most, starting from the NSM signal
- `clawhub install bookforge-retention-phase-intervention-selector` — select the right retention intervention for each retention phase, with success measured against the NSM
- `clawhub install bookforge-growth-stall-prevention` — audit the NSM trend for plateau signals and select the right counter-measure before momentum is lost

Browse more: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
