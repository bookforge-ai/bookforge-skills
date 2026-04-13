---
name: bullseye-channel-selection
description: "Guide systematic customer acquisition channel selection using the Bullseye Framework. Use whenever a startup founder, growth marketer, or product leader is deciding which marketing channel to focus on, evaluating customer acquisition options, choosing between viral, SEO, SEM, content, sales, PR, or any other growth channel, struggling with where to invest marketing budget, trying to escape channel bias, asking 'how do we get customers', planning a go-to-market, or needs to narrow 19 possible channels down to one focused bet. Activates on phrases like 'channel selection', 'customer acquisition', 'marketing strategy', 'growth channel', 'traction channel', 'Bullseye Framework', 'which channel should we use', 'how do we grow', 'marketing plan', or any discussion of prioritizing acquisition investments."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/bullseye-channel-selection
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [2, 3]
domain: startup-growth
tags: [startup-growth, customer-acquisition, channel-selection, marketing-strategy, growth-marketing]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Startup context — product description, stage, target customer, traction goal, budget"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for channel evaluation documents and ranked shortlist"
discovery:
  goal: "Select the single customer acquisition channel most likely to produce traction at the current startup stage"
  tasks:
    - "Generate ideas for all 19 traction channels to counteract founder bias"
    - "Rank channels into Inner Circle, Potential, and Long-shot tiers"
    - "Identify exactly 3 inner-circle channels to test in parallel"
    - "Design cheap tests for each inner-circle channel"
    - "Focus resources on the single channel producing best test results"
  audience:
    roles: [startup-founder, growth-marketer, head-of-marketing]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User asks which marketing channel to pursue"
      - "User is stuck in one channel and needs to explore alternatives"
      - "User has a new product and no traction strategy yet"
      - "User's current channel is saturating (rising CAC, falling CTR)"
    prerequisites: []
    not_for:
      - "User has already validated a single working channel and wants to optimize it (use A/B testing skill)"
      - "User is pre-product — no product exists to acquire customers for yet"
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

# Bullseye Channel Selection

## When to Use

You need to choose a customer acquisition channel for a startup, and the answer is not obvious. Before starting, verify:

- The product exists in some usable form (pre-product → product work comes first)
- The user can describe their target customer (even roughly)
- The user is open to considering channels they haven't tried before

If the user is already invested in a channel that's producing results, they likely want to *optimize* that channel, not re-select. Ask before running this skill.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product description:** what it is, who it's for, what stage it's at
  → Check prompt for: product name, category, target user description
  → If missing, ask: "What does your product do, and who is the target customer?"

- **Traction goal:** a specific numeric target (users, revenue, signups) over a specific timeframe
  → Check prompt for: numbers with "users", "customers", "revenue", timeframes
  → If missing, ask: "What's your traction goal? For example: '1,000 paying customers in 6 months' or '10,000 signups by end of quarter'."

- **Budget envelope:** rough dollar range available for channel testing
  → Check prompt for: dollar amounts, "budget", "can spend"
  → If missing, ask: "Roughly what budget do you have for testing acquisition channels? Even $500-$2,000 is enough to start."

### Observable Context (gather from environment)

- **Startup phase:** Phase I (pre-product-market-fit), Phase II (fit established, scaling traction), Phase III (scaling business)
  → Infer from: user count, revenue, team size, product maturity
  → Default: assume Phase I if unclear

- **Current channels tried:** what the user has already attempted
  → Infer from: references to "we tried", "didn't work", "used to"

### Default Assumptions
- Tests should cost $250-$500 each. A four-ad test is enough — forty is over-engineering.
- Inner circle = exactly 3 channels, tested in parallel.
- All 19 channels must be brainstormed, even ones the user dismisses.

### Sufficiency Threshold

```
SUFFICIENT: product description + traction goal + budget known
PROCEED WITH DEFAULTS: product and goal known, budget assumed at $1,500
MUST ASK: product description is missing
```

## Process

Use TodoWrite to track the 5 Bullseye steps:
- [ ] Step 1: Brainstorm (1 idea per all 19 channels)
- [ ] Step 2: Rank into Columns A/B/C
- [ ] Step 3: Prioritize — exactly 3 inner-circle channels
- [ ] Step 4: Test (design cheap parallel tests)
- [ ] Step 5: Focus (direct resources to the winner)

For each step, mark `in_progress` when starting and `completed` when done.

### Step 1: Brainstorm (All 19 Channels)

**ACTION:** Generate at least one concrete channel idea for every one of the 19 channels listed in [references/traction-channels.md](references/traction-channels.md). Write the ideas into a brainstorm table with these columns:

| Channel | Idea | Probability (1-5) | Est. CAC | Est. Volume | Test Timeframe |

Before scoring probability, explicitly note any channels the user dismissed. Ask why. The answer usually reveals one of three biases — see [references/channel-biases.md](references/channel-biases.md).

**WHY:** Founders have blind spots. They reach for channels they know (engineers → Engineering as Marketing; salespeople → Sales) and ignore whole categories. Peter Thiel: "Most businesses actually get zero distribution channels to work. Poor distribution — not product — is the number one cause of failure." Brainstorming every channel, even ones the user considers "not for us", is the systematic counter to this bias. Skipping channels here means skipping the channel that could actually work.

**IF** the user dismisses a channel without evidence → flag the bias type (invisible / negative / schlep) and still generate one idea for it.
**IF** a channel genuinely has no plausible idea → note "no viable idea" with 1-sentence reasoning. Do not skip the row.

### Step 2: Rank Into Columns A / B / C

**ACTION:** Sort each of the 19 channel ideas into three columns:
- **Column A (Inner Circle):** channels that seem most promising right now given the product, audience, and stage
- **Column B (Potential):** channels that could plausibly work but feel less certain
- **Column C (Long-shot):** channels where only stretch ideas exist

Output the ranked three-column table.

**WHY:** Ranking forces explicit prioritization. Without this step, founders treat all channels as equally viable and end up testing whichever is most convenient. The three-column structure creates a visible bar: a channel is in A only if it beats the alternatives on probability, CAC, and volume — not because it's familiar.

**IF** Column A has more than 3 channels → proceed to Step 3 to cut.
**IF** Column A has fewer than 3 channels → promote the strongest Column B entries until you have 3.

### Step 3: Prioritize — Inner Circle Exactly 3

**ACTION:** From Column A, identify exactly 3 channels for the inner circle. If Column A has more than 3, look for the natural drop-off in excitement between candidates — usually around position 3. Eliminate below the drop-off. If fewer than 3, promote from Column B.

Write the inner circle to `channel-inner-circle.md` with one paragraph per channel explaining why it qualified.

**WHY:** Three is a deliberate number. Testing 1 channel sequentially wastes time — you learn nothing about alternatives. Testing 5+ channels in parallel fractures focus and produces noisy results ("kitchen sink distribution" — Thiel's named failure mode). Three channels tested in parallel takes the same clock time as one and produces comparative data. The correct channel is unpredictable before testing, so parallel is how you discover it.

**IF** the user insists on more than 3 → explain the focus cost. If they still want more, note the deviation in the output and proceed with 3 for the formal Bullseye cycle.

### Step 4: Design Cheap Parallel Tests

**ACTION:** For each of the 3 inner-circle channels, design a cheap test that answers these four questions:
1. Roughly how much will it cost to acquire customers through this channel?
2. How many customers are available through this channel at that cost?
3. Are these the customers you want right now?
4. How long does it take to acquire a customer through this channel?

Target test budget: $250-$500 per channel. Use 4 ads, not 40. Speed to data matters more than test sophistication. Write `channel-test-plan.md` with hypothesis, budget, success metrics, and timeline per channel.

**WHY:** Inner-circle tests are validation experiments, not optimization. Founders confuse these and spend weeks A/B-testing a channel before knowing it works at all. Cheap tests ($250 on AdWords) give enough signal to rule a channel in or out — rule *out* is the primary goal. A/B testing to wring out an extra 15% conversion matters only after you've proven the channel can work at all.

**IF** tracking/reporting is not in place yet → stop and build it first. Sean Ellis: "Don't start testing until your tracking/reporting system has been implemented." A test with no measurement is a waste of budget.

### Step 5: Focus on the Winner

**ACTION:** After tests complete, compare results across the four questions. Direct all channel resources to the single channel with the strongest signal. Write `channel-focus-strategy.md` with the chosen channel, the evidence from testing, and the optimization plan (A/B testing cadence, budget scaling, team allocation).

If no channel showed promise, document what you learned and repeat Steps 1-4. Use the test data to refine the next brainstorm — which assumptions were wrong?

**WHY:** Focus is where traction actually happens. Spreading resources across multiple channels after testing is the kitchen sink failure mode again, just later in the cycle. If Channel A showed a clear signal and Channel B showed a weaker one, doubling down on A produces more traction than hedging across both. Compound returns come from depth, not breadth.

**IF** two channels tied → pick based on strategic fit with the next growth phase, not the current test alone. A channel that works now but doesn't scale (personal outreach in Phase II) is worse than a channel that works now and scales (content marketing).

## Inputs

- Product description and stage
- Traction goal (specific, numeric, time-bound)
- Budget for channel testing
- Current channels tried (if any)

## Outputs

Produces four deliverables in the working directory:

1. **`channel-brainstorm.md`** — 19-row table with ideas, probability scores, CAC/volume estimates, test timeframes
2. **`channel-rankings.md`** — Three-column A/B/C table with all 19 channels sorted
3. **`channel-inner-circle.md`** — The 3 selected channels with qualification reasoning
4. **`channel-test-plan.md`** — Cheap test design per channel (hypothesis, budget, metrics, timeline)
5. **`channel-focus-strategy.md`** *(after tests complete)* — Chosen channel + optimization plan

## Key Principles

- **Don't dismiss any channel in the brainstorm.** The channel you skip because it "obviously won't work" is the one a competitor will use to beat you. WHY: Founder bias is the single biggest failure mode in channel selection. Every channel gets one idea — this is non-negotiable.

- **Three in parallel, not one at a time.** Sequential testing wastes calendar time. Five in parallel fractures focus. Three is the Goldilocks number — enough parallelism to compare, not so much that you lose discipline. WHY: The correct channel is unpredictable before testing, so you can't just "pick the right one first". Parallel comparison is how you discover it.

- **Cheap validation before expensive optimization.** Inner-circle tests rule channels *out*, not in. Spend $250 to learn if a channel has any signal, not $25,000 to optimize a channel you haven't validated. WHY: Premature optimization is the most common testing failure. A/B testing is valuable only after the channel itself is proven.

- **Repeat Bullseye at every growth-stage transition.** A channel that worked in Phase I will often saturate in Phase II. When your current channel's CAC starts climbing or CTR starts falling (Law of Shitty Click-Throughs), run Bullseye again with the data you've accumulated. WHY: Channels have a lifecycle. Treating Bullseye as a one-time decision locks you into a channel past its useful life.

- **Focus after the test, not during.** Once a winner emerges, all resources go to that channel — not hedged across the top two. Compound returns come from depth. WHY: The startup's biggest asset is focused attention. Diluting it across channels is the kitchen sink failure at a different scale.

## Examples

**Scenario: B2B SaaS founder with no traction strategy**

Trigger: "We built a project management tool for construction teams. Launched 3 months ago. Have 40 paying customers from personal outreach. Need to get to 500 in 6 months. Budget: $3,000/month for marketing. What should we do?"

Process: (1) Brainstorm all 19 channels — note the founder dismissed Trade Shows as "not for us" (flagged as schlep bias; construction expos are where this audience lives). (2) Rank: Column A = Sales (SDR outreach), Trade Shows (construction expos), Targeting Blogs (construction-industry blogs). Column B = BD (integration partnerships), Content Marketing, SEM. Column C = Viral, Affiliate, Community. (3) Inner circle: Sales, Trade Shows, Targeting Blogs. (4) Tests: SDR with 100 cold emails ($500), booth sponsorship at one small construction meetup ($800), paid sponsorship on top 2 construction blogs ($700). (5) Two weeks later: sponsored blog posts had clear winner — $40 CAC, 25 signups. Focus: double down on Targeting Blogs, expand to 5 more blogs, build library of 3 guest posts per month.

Output: 4 markdown files in working directory, clear channel winner with evidence, next-4-weeks plan.

**Scenario: Consumer app stuck in Engineering as Marketing tunnel**

Trigger: "We built a free calculator tool that ranks on Google for 'loan calculator'. Drives 50k visits/month but only 200 signups. Engineering team keeps building more calculators. Growth has plateaued. What now?"

Process: (1) Brainstorm forces the founder to consider channels beyond Engineering as Marketing. Notes: "Viral Marketing — we haven't even thought about this; our calculators could include share hooks." (2) Rank: Column A = Viral Marketing (embed calculators as widgets on finance blogs), Content Marketing (loan advice articles with calculator CTAs), Email Marketing (nurture the 200 signups). Column B = PR, SEM, Targeting Blogs. Column C = Sales, Trade Shows, Offline Events. (3) Inner circle: Viral (widgets), Content, Email. (4) Tests: 3 widgets on blogs ($0 — engineering time), 5 long-form articles ($1,500 freelance), email drip sequence (existing 200 contacts). (5) Content articles converted 4x better than widgets — focus on content, commission 2 articles/week.

Output: Founder breaks out of "just build more calculators" loop. Discovers Content Marketing is the real channel; Engineering as Marketing was actually serving SEO, not acquisition.

**Scenario: Repeating Bullseye after saturation**

Trigger: "Targeting blogs worked great for us for 18 months — got 40k users. But now CAC is climbing and new blog partnerships aren't producing the same volume. Growth is flattening."

Process: Recognize this as the Law of Shitty Click-Throughs — the channel is saturating. Run Bullseye again, this time weighted by the test data already accumulated. (1) Brainstorm with the history in mind: "We know blog-style content works — which channels amplify that?" (2) Rank: Column A = PR (media coverage amplifies existing content), Content Marketing (owned publication), Community Building (turning blog readers into evangelists). (3) Inner circle: PR, Content, Community. (4) Tests: 1 HARO pitch per day for 30 days, launch own publication with 8 articles, seed community in Slack. (5) PR produced biggest lift — TechCrunch feature = 8,000 new users in 48 hours.

Output: Channel rotation handoff from Targeting Blogs → PR, with Content Marketing as supporting channel for PR amplification.

## References

- For the complete list of 19 traction channels with descriptions, see [references/traction-channels.md](references/traction-channels.md)
- For detection and counter-tactics for the three founder bias types, see [references/channel-biases.md](references/channel-biases.md)
- For the Mint case study showing Bullseye in action from 0 → 1M users, see [references/mint-case-study.md](references/mint-case-study.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

This skill is the entry point for the Traction methodology. Install related skills from ClawhHub:

- `clawhub install bookforge-startup-traction-strategy-by-phase` — Matches channels to your current growth phase (I/II/III)
- `clawhub install bookforge-traction-channel-testing` — Designs cheap tests for inner-circle channels
- `clawhub install bookforge-startup-critical-path-planning` — Integrates channel selection into startup milestone planning

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
