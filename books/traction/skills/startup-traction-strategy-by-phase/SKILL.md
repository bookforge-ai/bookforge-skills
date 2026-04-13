---
name: startup-traction-strategy-by-phase
description: "Guide startup growth strategy by diagnosing which phase the startup is in (Phase I: making something people want, Phase II: marketing something people want, Phase III: scaling) and selecting phase-appropriate traction channels. Use whenever a startup founder, growth marketer, or product leader is deciding how to split time between product and traction, asking whether they have product-market fit, choosing which channels fit their current stage, dealing with rising CAC or saturating channels, wondering if they should pivot, applying the 50% Rule, or escaping the Product Trap ('if we build it they will come'). Activates on phrases like 'product-market fit', 'phase I', 'phase II', 'scaling', 'growth strategy', 'should we pivot', '50% rule', 'product trap', 'traction vs product', 'which channels for our stage', 'moving the needle'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/startup-traction-strategy-by-phase
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [4]
domain: startup-growth
tags: [startup-growth, growth-strategy, startup-phases, product-market-fit, marketing-strategy]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Startup state — metrics, team size, product maturity, current traction activities"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for phase diagnosis and channel strategy documents"
discovery:
  goal: "Diagnose the startup's current phase and produce a phase-appropriate traction strategy"
  tasks:
    - "Diagnose current phase (I/II/III) from observable signals"
    - "Audit current time allocation against the 50% Rule"
    - "Map phase-appropriate channels and filter out mismatched ones"
    - "Apply the moving-the-needle filter to proposed activities"
    - "Detect the Product Trap and phase-channel mismatch anti-patterns"
  audience:
    roles: [startup-founder, growth-marketer, head-of-marketing]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User is unsure which phase their startup is in"
      - "User's current channel is producing diminishing returns"
      - "User asks whether to pivot"
      - "User is spending all time on product and wondering about growth"
    prerequisites: []
    not_for:
      - "User has not yet built a product"
      - "User just wants to pick a channel (use bullseye-channel-selection)"
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
    eval_count: 0
    assertion_count: 12
    iterations_needed: 0
---

# Startup Traction Strategy by Phase

## When to Use

The startup is somewhere on the growth curve and needs a phase-appropriate traction strategy. Use this skill when:

- The founder can't tell if they have product-market fit yet
- Growth has plateaued and the channels that worked before aren't working now
- The founder is spending 90%+ of their time on product
- A pivot is being considered
- The user asks "what should we focus on for growth right now?"

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Current metrics:** users, revenue, growth rate (even rough)
  → Check prompt for: numeric counts, percentages, trends
  → If missing, ask: "What are your current metrics? Rough numbers are fine — users, paying customers, monthly growth."

- **Time allocation:** how the founder/team is currently splitting effort
  → Check prompt for: "spending X% on", "we focus on", "most of our time"
  → If missing, ask: "Roughly how is your week split between product work and getting customers?"

- **Current traction activities:** what's actively being tried
  → Check prompt for: "we do X for growth", channel names
  → If missing, ask: "What are you doing right now to get new customers?"

### Observable Context

- **Product maturity:** MVP, v1, v2+
- **Team size and composition**
- **How customers currently describe the product** (satisfaction signals)

### Default Assumptions
- If user count is under 1,000 and no clear growth rate exists → assume Phase I
- If rough product-market fit signals exist (paying customers, word-of-mouth, retention) → Phase II
- If established business model with consistent growth → Phase III

### Sufficiency Threshold

```
SUFFICIENT: metrics + time allocation + current activities known
PROCEED WITH DEFAULTS: metrics known; assume time is 90/10 product/traction (the common failure mode)
MUST ASK: metrics are completely unknown (can't diagnose phase)
```

## Process

Use TodoWrite:
- [ ] Step 1: Diagnose phase
- [ ] Step 2: Audit time allocation against 50% Rule
- [ ] Step 3: Map phase-appropriate channels
- [ ] Step 4: Apply the moving-the-needle filter
- [ ] Step 5: Produce phase strategy document

### Step 1: Diagnose Phase (I / II / III)

**ACTION:** Classify the startup into one of three phases based on observable signals:

- **Phase I — Making something people want.** No product-market fit yet. Signals: low user count, high churn, constant product revision, customers don't obviously stick. The core job is building a product worth marketing.
- **Phase II — Marketing something people want.** Product-market fit established. Signals: customers stick, grow by word of mouth, revenue or engagement climbs. The core job is building a sustainable customer-acquisition engine.
- **Phase III — Scaling the business.** Business model established, market position significant. Signals: consistent growth rate, unit economics work, the question is how to dominate the market. The core job is scaling proven channels.

Write the diagnosis with one paragraph of evidence to `phase-diagnosis.md`.

**WHY:** Every downstream decision depends on phase. A Phase I startup doing Phase III tactics (mass advertising, PR campaigns, full sales teams) wastes money on channels that can't compound without a sticky product. A Phase III startup doing Phase I tactics (personal outreach, hand-holding each customer) underuses scale. Phase mismatch is the most common strategy error.

**IF** signals are mixed between Phase I and II → default to the earlier phase. The cost of over-investing in traction before fit is higher than the cost of under-investing briefly after fit.

### Step 2: Audit Time Allocation Against the 50% Rule

**ACTION:** Calculate how the founder/team is actually splitting time between product work and traction work. Compare to the 50% Rule: **50% of time on product, 50% on traction — at all times, in parallel, regardless of phase.**

If the split is 90/10 product/traction (the common default), name it explicitly. Quote the Product Trap warning: the #1 reason investors pass on otherwise-good founders is focus on product to the exclusion of everything else.

**WHY:** Most founders wildly over-invest in product. Marc Andreessen: "Almost every failed startup has a product. What failed startups don't have are enough customers." The Product Trap is the belief that "if we build it, they will come." Without explicit time-budget accountability, traction work gets crowded out by product work that always feels more urgent. The 50% Rule is a forcing function, not a guideline.

**IF** the user resists 50/50 because "the product isn't ready" → that's exactly when you need traction experiments, because channel feedback shapes the product.
**IF** the user is 50/50 already → excellent, skip to Step 3.

### Step 3: Map Phase-Appropriate Channels

**ACTION:** Based on the diagnosed phase, list which channels typically work and which typically don't. Use the mapping in [references/phase-channel-fit.md](references/phase-channel-fit.md).

Flag any current channel that's mismatched with the phase. Common mismatches:
- Phase I startup running SEM ads without product-market fit → burning budget on churning users
- Phase II startup still relying only on personal outreach → hitting volume ceiling
- Phase III startup ignoring PR → missing biggest growth lever

**WHY:** Channels have phase fit. "Some traction channels will move the needle early on but fail to work later. Others are hard to get working in Phase I but are major sources of traction in the later phases." Running a Phase I playbook in Phase II means growth stalls. Running a Phase III playbook in Phase I means spending on customers you can't retain. Matching phase to channel is the core of the book's strategy advice.

### Step 4: Apply the Moving-the-Needle Filter

**ACTION:** For each proposed or current traction activity, ask: "Can this plausibly deliver enough new customers to meaningfully advance our traction goal at our current scale?"

Do a back-of-envelope calculation: (target new customers) ÷ (realistic conversion rate, 1-5%) = audience you need to reach. Compare that to the channel's realistic reach. If the math doesn't work, the activity is off the needle.

Phase I needle ≠ Phase III needle:
- In Phase I, a tweet from a respected person or a speech to 300 people *can* move the needle.
- In Phase III, if you have 10,000 visitors/day, a blog post that sends 200 visitors is noise.

**WHY:** Founders waste time on activities that feel productive but can't meaningfully affect growth. The moving-the-needle filter is a math check: does the channel even have the volume to matter? Running a Facebook ad with $100 budget in Phase III is not a test — it's rounding error.

**IF** an activity can't pass the needle filter → cut it. Put the time back into the 50% traction budget.

### Step 5: Produce the Phase Strategy Document

**ACTION:** Write `phase-strategy.md` containing:

1. **Phase diagnosis** with evidence
2. **Current time allocation** vs 50% Rule (and the correction needed)
3. **Phase-appropriate channels** — which to pursue, which to cut
4. **Moving-the-needle audit** — activities cut, activities kept
5. **Next 4 weeks of traction experiments**, sized to the phase

**WHY:** A written strategy is a forcing function for accountability. "We're Phase I and the 50% Rule says we need more unscalable outreach" is easier to hold the team to than a verbal agreement. The document also makes phase transitions legible — in 3 months, re-read it and ask "what phase are we in now?"

## Inputs

- Startup metrics (users, revenue, growth rate)
- Current time allocation (product vs traction)
- Current traction activities
- Traction goal (if user has one)

## Outputs

Three markdown files:
1. **`phase-diagnosis.md`** — Phase (I/II/III) with evidence
2. **`phase-strategy.md`** — Complete strategy with time allocation correction and channel map
3. **`weekly-traction-plan.md`** — Next 4 weeks of phase-appropriate experiments

## Key Principles

- **Phase determines everything.** A channel that's a hit in Phase II can be a disaster in Phase I. WHY: The same tactic at the wrong time is a waste. Speed and volume needs change dramatically across phases — Phase I rewards unscalable tactics, Phase III punishes them.

- **50/50 is non-negotiable.** Not 80/20 in favor of product "because we're early". Not 20/80 "because we need customers fast". Always 50/50. WHY: Product and traction co-evolve. Traction experiments reveal what customers actually want. Product changes shape what traction channels work. Decoupling them is how startups die with "a great product nobody wanted."

- **The Product Trap has a specific detection signal.** If the founder says "the product isn't ready for marketing yet", that's the trap. WHY: The product is never "ready." Marc Andreessen: "The number one reason we pass on entrepreneurs is focusing on product to the exclusion of everything else." Ready for marketing means ready for feedback, not ready for perfection.

- **Re-diagnose phase quarterly.** Phases aren't permanent. What was Phase I six months ago might be Phase II now. WHY: Phase transitions are easy to miss from the inside. The channels that served you in Phase I will saturate as you enter Phase II. If you don't re-diagnose, you'll keep running Phase I tactics and watch growth flatten.

- **Unscalable tactics are a Phase I *strategy*, not a failure mode.** Paul Graham's "do things that don't scale" is phase-specific advice. In Phase I, it's correct. In Phase III, it's a trap. WHY: The same advice applied in the wrong phase produces opposite outcomes. Don't let "unscalable = bad" reflexes push you to premature scaling in Phase I.

## Examples

**Scenario: "We're 3 months in, 200 users, growth has stalled"**

Trigger: "Built a note-taking app for lawyers. 200 users in 3 months, mostly from Twitter. Growth has stalled the last 4 weeks. Only I'm doing marketing; 2 engineers on product."

Process: (1) Diagnose Phase I — low user count, no repeat customer signals, team still iterating product. (2) Time audit: founder estimates 70% product, 30% traction → flag the gap. Apply 50% Rule → founder needs to reclaim 20% of product time for traction. (3) Phase-appropriate channels: unscalable tactics work best here — targeting blogs (legal industry blogs), speaking at small legal conferences, direct outreach to named lawyers. Cut: any paid ads (wrong phase), no SEO (too slow for Phase I). (4) Moving-the-needle filter: founder was about to run $500 Facebook ads — kill that. $500 goes to sponsoring a legal-industry newsletter instead. (5) Produce 4-week plan: 10 cold emails/week to named lawyers, 1 guest post on a legal blog, outreach to 2 legal podcast hosts.

Output: Clear Phase I diagnosis, Product Trap flagged (70/30 instead of 50/50), and a concrete unscalable-first plan.

**Scenario: "Great growth for 18 months, now slowing"**

Trigger: "B2B SaaS, $200k MRR, 30% YoY growth. Content marketing drove most of our growth. Last 3 months growth has flattened to 5%. What's happening?"

Process: (1) Diagnose: likely Phase II → Phase III transition. Product-market fit clearly there. Content marketing is saturating (the Law of Shitty Click-Throughs). (2) Time audit: 50/50 seems maintained — that's good. (3) Phase-appropriate channels: Phase III should leverage channels with bigger volume ceilings. Consider PR (first big feature), paid ads at scale, BD with integration partners. (4) Moving-the-needle filter: a new blog post that sends 500 visitors no longer moves the needle at this scale. (5) Produce plan: kick off PR push (3 pitches to industry media), add SEM for bottom-funnel keywords, negotiate 2 integration partnerships.

Output: Phase II→III transition identified; next-phase channels selected; content remains but isn't the growth engine anymore.

**Scenario: The classic Product Trap**

Trigger: "We've been building for 8 months, launching soon, want to plan a big marketing push for launch day."

Process: (1) Diagnose Phase I — not launched, no customers. (2) Time audit: user says "we haven't done marketing yet because the product isn't ready" → Product Trap diagnosis, quote Andreessen. (3) 50% Rule applied retroactively — what traction experiments should have been running for the last 8 months? At minimum: building an email list, talking to 20 prospective customers weekly, finding 10 blogs where the audience lives. (4) Moving-the-needle: a "big launch day push" without a list or audience is a guaranteed flop. (5) Strategy: delay launch by 4 weeks, spend those weeks building traction groundwork (email list, blog relationships, 20 customer conversations), so launch lands on an audience that already cares.

Output: Product Trap named and corrected; launch plan now has traction preamble; founder understands the rule going forward.

## References

- For the full phase-channel fit mapping, see [references/phase-channel-fit.md](references/phase-channel-fit.md)
- For signs of each phase and transition signals, see [references/phase-signals.md](references/phase-signals.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select specific channels within your phase strategy
- `clawhub install bookforge-traction-channel-testing` — Run cheap tests on the channels you pick
- `clawhub install bookforge-startup-critical-path-planning` — Set quantified traction goals by phase

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
