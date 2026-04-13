---
name: viral-growth-loop-design
description: "Design and measure viral growth loops using the viral coefficient (K-factor), viral loop type taxonomy, and cycle time optimization. Use whenever a startup founder, growth marketer, or product lead is designing referral programs, measuring word-of-mouth, building viral features, calculating K-factor, trying to achieve exponential growth, optimizing invite flows, debugging a viral feature that isn't working, or evaluating whether viral is the right channel. Activates on phrases like 'viral marketing', 'viral coefficient', 'K-factor', 'referral program', 'invite flow', 'network effects', 'word of mouth', 'exponential growth', 'viral loop', 'Dropbox referral', 'Hotmail signature', 'inherent virality', 'cycle time', 'should we go viral'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/viral-growth-loop-design
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [7]
domain: startup-growth
tags: [startup-growth, viral-marketing, referral-programs, network-effects, growth-metrics]
depends-on: [bullseye-channel-selection]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Product description, current viral metrics if any, referral mechanics"
  tools-required: [Read, Write]
  tools-optional: [Bash, AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for viral loop designs and K-factor calculations"
discovery:
  goal: "Design or optimize a viral loop using the K-factor formula, loop type taxonomy, and cycle time tactics"
  tasks:
    - "Classify the product's best-fit viral loop type (7 types)"
    - "Measure or estimate the viral coefficient K = i × conversion%"
    - "Decompose K into invite rate, click-through rate, signup rate — find the bottleneck"
    - "Optimize the weakest variable via focused A/B testing"
    - "Shorten the viral cycle time"
    - "Detect and prevent the 4 viral mistakes"
  audience:
    roles: [startup-founder, growth-marketer, product-manager]
    experience: intermediate
  when_to_use:
    triggers:
      - "User wants to add viral mechanics to a product"
      - "User has a viral feature that isn't producing growth"
      - "User is measuring referral program performance"
      - "Bullseye Framework selected viral as an inner-circle channel"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "Viral should be selected via Bullseye first, not default-assumed"
    not_for:
      - "Products without inherent sharing value (viral will not rescue a bad product)"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: 0
    assertion_count: 13
    iterations_needed: 0
---

# Viral Growth Loop Design

## When to Use

The startup has selected viral marketing as a channel (via Bullseye) and needs to design, measure, or optimize a viral growth loop. Before starting, verify:

- The product has at least plausible sharing value (products that aren't inherently viral will not be rescued by viral mechanics — this is viral mistake #1)
- The user has metrics or can instrument metrics for invites and conversions
- Viral was genuinely selected, not defaulted to because "growth hacking"

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product description:** what the product does, who uses it, what makes it share-worthy (or why not)
  → Check prompt for: product name, category, sharing signals
  → If missing, ask: "What does your product do, and why would one user tell another about it?"

- **Current metrics (if any):** signups per period, invites sent, invite-to-signup conversion
  → Check prompt for: numbers, "our K is", "conversion rate"
  → If missing: proceed with hypothetical design, note measurement needs

### Observable Context

- **Existing viral features:** referral program, share buttons, invite flows
- **Product communication patterns:** how users already talk to others about the product

### Default Assumptions
- K > 1 = exponential, K > 0.5 = meaningful contribution, K < 0.5 = not a primary channel
- Optimization focus on the single weakest variable (invite rate OR click-through OR signup)
- 1-2 engineers × 2-3 months minimum to implement viral properly

### Sufficiency Threshold

```
SUFFICIENT: product description + current K measurement or instrumentation plan
PROCEED WITH DEFAULTS: product description known, assume viral is being designed from scratch
MUST ASK: product description is missing, can't recommend loop type
```

## Process

Use TodoWrite:
- [ ] Step 1: Classify viral loop type (7 types)
- [ ] Step 2: Measure baseline K and cycle time
- [ ] Step 3: Decompose K to find the weakest variable
- [ ] Step 4: Design focused optimization (4 viral mistakes check)
- [ ] Step 5: Shorten cycle time

### Step 1: Classify the Viral Loop Type

**ACTION:** Determine which of the 7 viral loop types best fits the product. See [references/viral-loop-types.md](references/viral-loop-types.md) for the full taxonomy.

The 7 types:
1. **Word of Mouth** — organic (nothing engineered). Works when the product is genuinely remarkable.
2. **Inherent Virality** — product requires multiple users (Skype, WhatsApp, Snapchat).
3. **Collaborative Virality** — works alone but better with others (Google Docs, Figma).
4. **Communicative Virality** — product messages carry branding ("Sent from my iPhone", Hotmail signature).
5. **Incentivized Virality** — rewards for referrals (Dropbox extra storage, Uber credits, PayPal cash).
6. **Embedded/Widget Virality** — share buttons, embed codes (YouTube embed, Pinterest pins).
7. **Social Virality** — activity broadcast to social networks (Spotify on Facebook, Strava sharing).

Write the type classification with reasoning to `viral-loop-design.md`.

**WHY:** Loop type determines every downstream decision. An incentivized referral program that would work for a file-storage product would feel spammy on a B2B analytics tool. Getting type wrong is one of the 4 viral mistakes — "bolting on generic sharing mechanics without understanding how users are currently communicating". The type must match the product's actual usage pattern.

**IF** no type fits cleanly → that's a signal viral may not be the right channel. Return to Bullseye with new data.

### Step 2: Measure or Estimate Baseline K and Cycle Time

**ACTION:** Calculate the viral coefficient:

**K = i × conversion_percentage**

- **i** = average number of invites per user (how many people each user invites)
- **conversion_percentage** = percentage of invitees who sign up

Worked example: users send 3 invites each, 2 of 3 invitees convert → K = 3 × (2/3) = 2. Starting with 100 users, next cycle produces 200, next 400, etc. Exponential.

**Thresholds:**
- K > 1: true exponential growth
- K > 0.5: meaningful contribution to growth
- K < 0.5: viral is not a primary channel

Also measure **viral cycle time** — the time between a user joining and their invitees joining. Shorter cycle time = faster compounding. YouTube's cycle time is minutes; slower products can be days or weeks.

Write measurements (or measurement plan if not yet instrumented) to `viral-baseline.md`.

**WHY:** Without baseline K, you're optimizing blind. Every intervention needs a before/after comparison. The K threshold decides whether viral is primary or secondary — K < 0.5 means viral should be a supporting channel, not the main one. Cycle time is often overlooked — two products with the same K but different cycle times have dramatically different growth curves (K=0.9 at 1-day cycle vs K=0.9 at 7-day cycle → very different compounding).

### Step 3: Decompose K to Find the Weakest Variable

**ACTION:** Decompose K further: **K = i × click_through_percentage × signup_percentage**

Measure each component:
- **i** — how many invites are sent per user?
- **click_through_percentage** — how many invite links are clicked?
- **signup_percentage** — of clickers, how many sign up?

Find the weakest variable. That's the optimization target.

**WHY:** Focusing optimization on the wrong variable wastes weeks. If invite rate is healthy (people ARE sharing) but signup conversion is 2%, changing the invite flow doesn't help — the landing page is the problem. Decomposition reveals the actual bottleneck. "Not doing enough A/B tests" is another of the 4 viral mistakes — running tests on the wrong variable is effectively the same failure.

### Step 4: Design Focused Optimization + Check 4 Viral Mistakes

**ACTION:** Run the **4 viral mistakes check** before proposing changes:

1. **Not inherently viral product trying to add viral features** — will the loop work at all? If the product has no plausible sharing hook, stop.
2. **Bad product trying to go viral** — virality accelerates whatever the product is. A bad product + virality = negative reviews spreading faster.
3. **Not enough A/B tests** — assume 1-3 of every 10 tests will yield positive results. Plan accordingly.
4. **Bolting on generic sharing mechanics** — "just add Facebook Like buttons" without understanding user communication is the most common mistake.

If any of the 4 mistakes apply, fix that before optimizing.

Then design focused A/B tests for the weakest variable. Run 2-3 variants for 2-3 weeks at a time. Budget: 1-2 engineers × 2-3 months minimum for serious viral work.

**WHY:** The 4 mistakes prevent wasted optimization cycles. Running 20 A/B tests on the invite flow of a non-viral product produces nothing. Running 20 A/B tests on a healthy invite flow when the bottleneck is signup conversion also produces nothing. The mistakes are named to make them detectable.

### Step 5: Shorten the Viral Cycle Time

**ACTION:** Map the full viral loop — every step between "user takes action" and "new user signs up". Count the steps. Remove any unnecessary step. For each remaining step, ask: "can this be faster?"

Tactics:
- Create urgency (expiring invites, time-limited rewards)
- Remove friction at every funnel step (single-click accept, pre-filled forms, social login)
- Trigger invites at the natural sharing moment (not later)
- Incentivize completion of the next step, not just the final conversion

**WHY:** Cycle time is the most underrated variable. Two products with K = 0.9 but cycle times of 1 day vs 7 days have dramatically different user curves after 30 days. Reducing cycle time by half is equivalent to doubling K for long-term compounding effects. Yet founders obsess over K and ignore cycle time.

## Inputs

- Product description (with sharing hypothesis)
- Current viral metrics (if instrumented)
- Implementation resources (engineers × months)

## Outputs

Four markdown/data files:

1. **`viral-loop-design.md`** — Loop type classification, mechanics, implementation plan
2. **`viral-baseline.md`** — Current K, cycle time, decomposed metrics
3. **`viral-optimization-plan.md`** — Weakest variable, A/B test roadmap, 4 mistakes check
4. **`viral-cycle-time-map.md`** — Full loop steps with friction analysis

## Key Principles

- **K is a formula, not a vibe.** K = i × conversion_percentage. Founders who say "we're going viral" without calculating K are making a category error. WHY: Without numeric K, you can't tell if you're growing virally or just growing. The formula forces clarity.

- **Loop type must match the product's communication pattern.** Generic share buttons on a product users don't naturally discuss is mistake #4. Watch how users ALREADY share the product before designing the loop. WHY: A loop that fights user behavior produces 0% conversion; a loop that amplifies existing behavior compounds.

- **Optimize the weakest link, not the favorite metric.** Founders love to A/B test invite copy. If the bottleneck is signup conversion, invite copy changes nothing. WHY: Decomposition is the only way to find the actual bottleneck. Skipping decomposition is optimization theater.

- **Viral is not a rescue plan for a bad product.** The 4 viral mistakes are explicit: if the product isn't inherently viral, or if the product is bad, virality won't save it — it will accelerate the decline. WHY: This is the most common founder error. Virality is leverage, and leverage works in both directions.

- **Cycle time matters as much as K.** A 7-day cycle and a 1-day cycle with the same K produce radically different growth curves. Shortening cycles is often easier than raising K. WHY: Compounding is about iteration count, not just multiplier. Fast cycles compound more iterations per unit time.

- **Budget 2-3 months for serious viral work.** "Expert teams need 1-2 engineers for 2-3 months minimum to implement and optimize a new viral channel." Viral is not a weekend project. WHY: Shortcuts on viral engineering produce broken loops that look right but don't compound. The time budget is the floor, not the ceiling.

## Examples

**Scenario: File-sharing SaaS adding a referral program**

Trigger: "We're building Dropbox-for-teams. Want to add a referral program. How should it work?"

Process: (1) Loop type: Incentivized Virality fits (Dropbox's original model). Alternative: Collaborative Virality since teams use it together. Decision: combine both — team invites trigger collaborative flow, external referrals get storage credits. (2) Estimate K: assume i=2 (each user invites 2 on average), conversion 30% → K=0.6. Meaningful but not exponential. (3) Decompose: if click-through is 60% and signup is 50%, the weakest variable is signup — optimize that first. (4) 4 mistakes check: product is genuinely collaborative (not mistake 1), product works (not mistake 2), plan weekly A/B tests (not mistake 3), mechanics match how teams actually invite colleagues (not mistake 4). (5) Cycle time: trigger invite moment at "share file with external user" action (natural moment), reward appears at next login (fast).

Output: Clear implementation plan with incentive structure, estimated K baseline, and optimization priority on signup conversion.

**Scenario: Consumer app with K=0.2 — is viral the channel?**

Trigger: "We added a referral feature to our mobile game. Measured K over 30 days: K=0.2. What should we do?"

Process: (1) Loop type: check if current mechanics match the product. If users aren't naturally discussing the game with friends, the incentivized loop was bolted on. (2) K=0.2 is below the 0.5 threshold — viral is not a primary channel. (3) Decompose: low i (users aren't sending invites at all)? Low conversion (invitees click but don't install)? Decomposition reveals the problem. (4) 4 mistakes check: is the product inherently viral? For a mobile game, only if it's multiplayer or has leaderboards. If single-player, viral mechanics are fighting the product's nature. (5) Recommendation: return to Bullseye. Viral as supporting channel only, not primary.

Output: Honest assessment that viral isn't the channel, recommendation to re-run Bullseye with this data.

**Scenario: B2B SaaS considering collaborative virality**

Trigger: "We built a spreadsheet-like analytics tool. Think Figma for data. Should we make it viral?"

Process: (1) Loop type: Collaborative Virality is the clear fit — the product works alone but is 10x more valuable when shared with colleagues. (2) Baseline unknown, but plan the metrics: measure share action rate, external-user signup rate. (3) Decompose from day one: i, click-through, signup separately. (4) 4 mistakes check: product IS inherently collaborative ✓, product quality TBD, budget 2 engineers × 3 months, mechanics match how Figma does it (invite = real seat, not just a link). (5) Cycle time: optimize "share moment" UX so it happens naturally mid-workflow, not as a separate step.

Output: Loop type decision, Figma-inspired mechanics plan, instrumentation requirements for baseline measurement.

## References

- For the full 7-type viral loop taxonomy with examples, see [references/viral-loop-types.md](references/viral-loop-types.md)
- For the 4 viral mistakes in detail, see [references/viral-mistakes.md](references/viral-mistakes.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select viral deliberately, don't default to it
- `clawhub install bookforge-traction-channel-testing` — Baseline K and A/B test discipline
- `clawhub install bookforge-content-and-email-marketing` — Referral emails are part of the viral loop

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
