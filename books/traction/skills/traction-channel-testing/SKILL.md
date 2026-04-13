---
name: traction-channel-testing
description: "Design and run cheap validation tests for customer acquisition channels before committing budget. Use whenever a startup founder, growth marketer, or product leader needs to test a marketing channel, validate CAC and LTV assumptions, set up A/B testing, calculate whether a channel can hit growth targets, measure channel performance, detect a saturating channel (Law of Shitty Click-Throughs), decide whether to optimize or abandon a channel, or compare channels quantitatively. Activates on phrases like 'test a channel', 'cheap test', 'CAC', 'customer acquisition cost', 'LTV', 'lifetime value', 'A/B test', 'does this channel work', 'how do I know if this is working', 'conversion rate', 'channel metrics', 'measure marketing', 'channel saturation', 'Law of Shitty Click-Throughs'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/traction-channel-testing
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [5]
domain: startup-growth
tags: [startup-growth, channel-testing, ab-testing, customer-acquisition-cost, growth-metrics]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Channel hypothesis, budget, current tracking setup"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for test plans and results tracking"
discovery:
  goal: "Design and evaluate cheap channel tests that produce actionable CAC, volume, and quality data"
  tasks:
    - "Verify tracking/reporting is in place before testing"
    - "Design the 4-question inner-circle test per channel"
    - "Set up CAC/LTV comparison spreadsheet"
    - "Run the needle-moving volume calculation"
    - "Detect channel saturation via the Law of Shitty Click-Throughs"
    - "Transition from validation to A/B optimization after channel validated"
  audience:
    roles: [startup-founder, growth-marketer, head-of-marketing]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User wants to test a channel before committing"
      - "User is unsure if current channel is still working"
      - "User has proposed A/B tests on unvalidated channel"
    prerequisites: []
    not_for:
      - "User has not yet selected channels to test (use bullseye-channel-selection first)"
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

# Traction Channel Testing

## When to Use

You need to test a customer acquisition channel — either validating a new channel or measuring an existing one. Before starting, verify:

- The user has at least one specific channel hypothesis to test (e.g., "Facebook Ads" not "social media")
- Some minimum budget exists ($250 or more per channel)
- The user is clear on the traction goal the channel should contribute to

If the user hasn't selected channels yet, run `bullseye-channel-selection` first.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Channel to test:** a specific channel, not a category
  → Check prompt for: specific channel names (SEM, SEO, Targeting Blogs, etc.)
  → If vague ("marketing", "ads"), ask: "Which specific channel do you want to test? For example: Google SEM on category keywords, sponsored posts on 3 niche blogs, cold email to 200 enterprise leads?"

- **Test budget:** dollar amount available
  → Check prompt for: "$X", "budget", "can spend"
  → If missing, ask: "What budget is available for the test? Even $250-500 per channel is enough to start."

- **Traction goal the channel must contribute to:** the number the test is trying to validate against
  → Check prompt for: "need X customers", "goal is Y"
  → If missing, ask: "What traction goal does this channel need to help hit? Something like '1,000 signups this quarter' or '$10k MRR in 3 months'."

### Observable Context

- **Tracking system status:** does the user already measure signups, conversions, revenue?
- **Prior channel tests:** what has been tried before, with what results?
- **Unit economics:** rough CAC and LTV if known

### Default Assumptions
- Tests cost $250-$500 each per channel
- First tests are *validation* not *optimization* (4 ads, not 40)
- Conversion rate assumption is 1-5% unless the user has data
- Tracking must exist BEFORE the first test — no exceptions

### Sufficiency Threshold

```
SUFFICIENT: channel + budget + traction goal known, tracking in place
PROCEED WITH DEFAULTS: channel + budget known, assume tracking is a spreadsheet
MUST ASK: no tracking exists (stop and build it first)
```

## Process

Use TodoWrite:
- [ ] Step 1: Verify tracking/reporting infrastructure
- [ ] Step 2: Design the 4-question validation test
- [ ] Step 3: Run needle-moving calculation
- [ ] Step 4: Execute and capture data
- [ ] Step 5: Decide — A/B optimize, abandon, or iterate

### Step 1: Verify Tracking Before Testing

**ACTION:** Confirm the user has a tracking system in place for the metrics the test will produce. At minimum:
- Signups or conversions trackable per source
- Cost per source measurable (ad spend, sponsorship $, etc.)
- A spreadsheet is fine — it does not need to be a fancy analytics platform

If no tracking exists, STOP testing. Help the user build a minimum tracking spreadsheet first: `source | spend | conversions | CAC` as the starting columns.

**WHY:** Sean Ellis: "Don't start testing until your tracking/reporting system has been implemented." A test with no measurement is a waste of budget. Worse, an untracked test gives false confidence — founders assume success or failure based on vibes, not data. Tracking is the non-negotiable prerequisite.

**IF** tracking exists but is inconsistent (e.g., signups tracked but source attribution broken) → fix attribution first. UTM parameters on every link are the minimum.

### Step 2: Design the 4-Question Validation Test

**ACTION:** For the channel being tested, design an experiment that answers these four questions:

1. **How much does it cost to acquire customers through this channel?** (CAC)
2. **How many customers are available through this channel?** (Volume)
3. **Are these the customers you want right now?** (Quality/fit)
4. **How long does it take to acquire a customer through this channel?** (Time-to-acquire)

Set the test budget to $250-$500 per channel. Keep it small on purpose. Write hypothesis, setup, duration, and success thresholds to `channel-test-plan.md`.

Critically: this is a **validation** test, not an **optimization** test. Four ads, not forty. One landing page, not ten. Goal: determine whether the channel can work at all, not whether it's perfectly tuned.

**WHY:** Founders confuse validation and optimization. They A/B test forty ad variants on a channel they haven't proved works, wasting weeks and thousands of dollars to discover the channel was fundamentally wrong. Validation tests cost $250 and answer a binary question: signal or no signal. Only after signal appears should A/B optimization begin.

**IF** the channel is SEM → a $250 AdWords buy is enough to get a rough CAC estimate.
**IF** the channel is Targeting Blogs → sponsor 1-2 mid-tier blogs, measure clicks and signups.
**IF** the channel is Cold Sales → 100 personalized cold emails, measure reply and qualified-lead rates.

### Step 3: Run the Needle-Moving Volume Calculation

**ACTION:** Before launching, do a back-of-envelope calculation: **can this channel plausibly hit the traction goal?**

Formula: (target new customers) ÷ (assumed conversion rate 1-5%) = audience you need to reach

Example: need 100,000 new customers → at 1-5% conversion, you need to reach 2-10 million people. Does the channel even have that audience?

If the channel's maximum reach can't support the math, there's no point testing it for this goal. Move on.

**WHY:** This is the math check that prevents wasted tests. Running a $500 targeted blog test for a Phase III company that needs 100,000 new users is a waste — even at 5% conversion, no single blog reaches the audience required. Filtering by volume before testing saves budget for channels that could actually matter.

**IF** math doesn't work → either downsize the goal, or pick a different channel. Don't run the test.
**IF** math works with headroom → proceed to the test.

### Step 4: Execute and Capture Data

**ACTION:** Run the test for the timeframe set in the plan. During the test:
- Do NOT change variables mid-test
- Do NOT add more budget if early results look bad
- Do NOT start optimizing before the validation phase completes

After the test, record results in `channel-test-results.md` with:
- CAC (actual cost ÷ actual conversions)
- Volume (conversions in the test period)
- Customer quality (engagement, activation, fit signals)
- Time-to-acquire (days from first touch to conversion)

Add the channel as a new row in the master `channel-comparison.csv` with columns: channel, CAC, LTV (estimated), volume, quality_score, status.

**WHY:** Mid-test tampering destroys the signal. Extending budgets inflates the baseline. Optimizing before validating confuses two separate questions. Discipline during execution is what produces trustworthy data. The `channel-comparison.csv` is the universal spreadsheet the book recommends — CAC vs LTV per channel is how you compare channels at a glance.

### Step 5: Decide — Optimize, Abandon, or Iterate

**ACTION:** Based on test results, make one of three decisions:

1. **Optimize (A/B test):** Signal is clear (CAC < LTV, volume sufficient, customer quality good). Start A/B testing to improve the channel. Target cadence: 1 A/B test per week → 2-3x improvement over time.

2. **Abandon:** Signal is absent (CAC > LTV, or volume can't scale, or customer quality poor). Cut the channel. Write what you learned in `channel-postmortem.md` — the data is still valuable for the next Bullseye cycle.

3. **Iterate validation:** Signal is ambiguous. Run a second validation test with a refined hypothesis (different audience, different creative, different offer). Budget: another $250-$500.

Apply the **Law of Shitty Click-Throughs** check: even on channels that look good, ask "is this a channel about to saturate?" Plan continuous small experiments even in working channels.

**WHY:** The transition from validation to optimization is where most discipline breaks down. Founders who see early promising signal jump to full-scale investment before validating at the right scale. Founders who see weak signal keep pouring money in hoping to see improvement. The three-way decision is a forcing function. The Shitty CTR check is important because every channel degrades over time — a channel that's great today is saturating tomorrow.

**IF** optimizing → set up a weekly A/B test cadence. Focus variables: subject lines, ad copy, landing page headlines, call-to-action, imagery.
**IF** abandoning → make sure the learning is captured. The book: "Consistently running cheap tests will allow you to stay ahead of competitors pursuing the same channels."

## Inputs

- Channel hypothesis (specific channel + tactic)
- Test budget ($250-500 per channel minimum)
- Traction goal
- Tracking/reporting system status

## Outputs

Four markdown/csv files:

1. **`channel-test-plan.md`** — hypothesis, budget, 4-question test design, timeline
2. **`channel-test-results.md`** — CAC, volume, quality, time-to-acquire per tested channel
3. **`channel-comparison.csv`** — universal spreadsheet with CAC/LTV per channel
4. **`channel-decision.md`** — Optimize / Abandon / Iterate decision with reasoning

## Key Principles

- **Validation before optimization.** Cheap tests answer "does this channel work at all?" A/B testing answers "how do I make this channel work better?" Mixing them wastes weeks. WHY: 80% of channel failure shows up at validation. Optimizing something that will fail validation is pure waste.

- **Four questions, not forty metrics.** CAC, volume, quality, time-to-acquire. Extra metrics are noise at the validation stage. WHY: Limiting metrics keeps the test interpretable. A pass/fail answer from four numbers is better than an ambiguous answer from twenty.

- **Tracking is the prerequisite, not an afterthought.** No tracking = no test. Sean Ellis explicitly warns against running tests before instrumentation. WHY: Untracked tests give false confidence. Worse, they destroy the signal for the next test — you learn nothing, but your budget is gone.

- **The Law of Shitty Click-Throughs is always in effect.** Every channel degrades over time. Even working channels need continuous small experiments to detect saturation early. WHY: The moment you stop testing a working channel, a competitor or a shift in the platform can make it unproductive before you notice. Continuous validation is cheaper than catching saturation late.

- **$250 is enough for an initial signal on SEM.** Scale the budget to the channel — $250 on AdWords, $500 on a blog sponsorship, 100 emails for cold sales — but keep the validation budget small by design. WHY: Cheap forces you to ask "can this work at scale?" Expensive forces you to justify the spend, which biases interpretation.

## Examples

**Scenario: B2B SaaS founder wants to test SEM**

Trigger: "I want to run Google Ads to test SEM as a channel. We sell a $99/month project management tool. Budget: $500 for the test. Goal: 200 paying customers in 90 days."

Process: (1) Tracking check — founder has a CRM with source attribution, good. (2) Needle calc: 200 customers / 3% assumed conversion = 6,667 clicks needed. At $2/click = $13,334 budget at full scale. $500 test can produce ~250 clicks = maybe 5-8 customers. That's enough signal. (3) 4-question test designed: 4 ads, 1 landing page, 5 keyword groups, 2 weeks duration. (4) Run: $487 spent, 243 clicks, 9 signups, 4 paying. CAC = $122 vs $99 price × 12-month average retention = $1,188 LTV. Healthy ratio. (5) Decision: Optimize. Weekly A/B tests on ad copy and landing page headline. Scale budget to $3k/month.

Output: Clear validation → optimization decision with CAC vs LTV math.

**Scenario: Consumer app considering Targeting Blogs**

Trigger: "We want to try sponsored posts on fitness blogs. We have $800 to test. Our mobile fitness app needs to hit 10,000 new users this quarter."

Process: (1) Tracking — in-app attribution via source-tagged download links, OK. (2) Needle calc: 10,000 users / 2% conversion = 500k reach needed. Top 3 fitness blogs reach ~800k/month combined. Math works. (3) Test: 2 sponsored posts on 2 mid-tier blogs, $400 each, 1 week duration. Measure click-throughs and downloads. (4) Run: Blog A = 1,240 clicks → 31 downloads (CAC $13). Blog B = 340 clicks → 6 downloads (CAC $67). (5) Decision: Blog A clearly works, Blog B doesn't. Optimize on Blog A (sponsor monthly), explore similar fitness blogs.

Output: Clear winner, clear loser, next-stage plan.

**Scenario: Detecting a saturating channel**

Trigger: "Our Facebook ads have been great for 18 months. CAC was $15. Now it's $28 and climbing. Should we panic?"

Process: (1) This is the Law of Shitty Click-Throughs in action. Don't panic but don't ignore it. (2) Re-run the 4 questions: CAC up ($28), volume flat, quality similar, time-to-acquire same. (3) Check LTV — is $28 still profitable? If LTV is $300, $28 is fine but trajectory matters. (4) Decision: Run 2-3 small tests on adjacent channels NOW while Facebook still works. Don't wait until Facebook is unprofitable. (5) Parallel experiments: $250 on TikTok ads, $250 on YouTube preroll, $250 on 1 niche influencer. See which has signal.

Output: Recognition of saturation, parallel discovery of next channel before the primary fails.

## References

- For the universal CAC/LTV comparison spreadsheet template, see [references/channel-comparison-template.md](references/channel-comparison-template.md)
- For the Law of Shitty Click-Throughs in detail, see [references/law-of-shitty-clickthroughs.md](references/law-of-shitty-clickthroughs.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Choose which channels to test in the first place
- `clawhub install bookforge-startup-traction-strategy-by-phase` — Ensure the channel matches your startup phase
- `clawhub install bookforge-sem-performance-optimization` — Deep-dive into SEM-specific metrics and optimization

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
