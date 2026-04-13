---
name: sem-performance-optimization
description: "Optimize Search Engine Marketing performance using CTR, CPC, CPA formulas, Quality Score benchmarks, and keyword profitability filtering. Use whenever a founder or marketer is running Google Ads, Bing Ads, or any SEM campaign, measuring CAC on paid search, optimizing ad groups, pruning unprofitable keywords, improving Quality Score, testing SEM as a channel, or comparing SEM vs other acquisition channels. Activates on phrases like 'SEM', 'Google Ads', 'AdWords', 'PPC', 'pay-per-click', 'CPC', 'CPA', 'CTR', 'Quality Score', 'keyword optimization', 'paid search', 'ad groups', 'bid strategy', 'search advertising'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/sem-performance-optimization
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [10]
domain: startup-growth
tags: [startup-growth, sem, google-ads, paid-search, performance-marketing]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product description, target keywords, current SEM metrics"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for SEM analysis and optimization plans"
discovery:
  goal: "Optimize SEM performance using quantitative formulas and Quality Score benchmarks"
  tasks:
    - "Calculate current CTR, CPC, CPA per ad group"
    - "Evaluate Quality Score against benchmarks (avg 2.0%, low 1.5%)"
    - "Apply keyword profitability filter (CPA vs LTV)"
    - "Prune unprofitable keywords"
    - "Design ad group structure for long-tail expansion"
    - "Use Dynamic Keyword Insertion where appropriate"
  audience:
    roles: [startup-founder, growth-marketer, ppc-specialist]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User is running Google Ads and wants to improve performance"
      - "SEM CAC is too high or climbing"
      - "User wants to test SEM as a channel"
      - "Keyword list needs pruning"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "SEM should be selected via Bullseye against existing search demand"
    not_for:
      - "New product categories with no existing search demand"
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

# SEM Performance Optimization

## When to Use

The startup is running SEM and needs to improve performance, or is testing SEM as a new channel. Before starting, verify:

- There is existing search demand for the category (SEM is demand fulfillment, not demand creation)
- The user has or can access basic SEM metrics (spend, clicks, conversions)
- The goal is CAC-positive customer acquisition, not brand awareness

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Current SEM metrics or test hypothesis:** spend, clicks, conversions, CPA
  → Check prompt for: "spending X on ads", CTR numbers, CPC numbers
  → If missing, ask: "What are your current SEM metrics? Spend, clicks, conversions — even rough numbers."

- **Unit economics:** CAC target and LTV
  → Check prompt for: "CAC should be X", "LTV is Y", "customer value"
  → If missing, ask: "What's your approximate customer LTV? And what CAC is acceptable?"

### Observable Context

- **Keyword categories:** category terms (fat-head) vs specific queries (long-tail)
- **Competitor SEM activity:** how crowded the space is

### Default Assumptions
- Average AdWords CTR benchmark: 2.0%
- Low Quality Score threshold: CTR < 1.5% (Google penalizes these)
- Initial test budget: $250-$500 per keyword cluster
- 3:1 LTV:CAC ratio minimum for sustainable channel

### Sufficiency Threshold

```
SUFFICIENT: metrics + unit economics known
PROCEED WITH DEFAULTS: metrics known, use 3:1 LTV:CAC as heuristic
MUST ASK: no SEM metrics or hypothesis at all
```

## Process

Use TodoWrite:
- [ ] Step 1: Calculate current performance (CTR, CPC, CPA)
- [ ] Step 2: Evaluate Quality Score against benchmarks
- [ ] Step 3: Apply profitability filter (CPA vs LTV)
- [ ] Step 4: Prune unprofitable keywords
- [ ] Step 5: Expand to long-tail and restructure ad groups

### Step 1: Calculate Current Performance

**ACTION:** For each ad group, calculate the three core SEM metrics:

- **CTR (Click-Through Rate)** = clicks / impressions × 100
- **CPC (Cost Per Click)** = spend / clicks
- **CPA (Cost Per Acquisition)** = CPC / conversion_percentage, or spend / conversions

Worked example: 100 impressions, 3 clicks → CTR 3%. $1 CPC with 10% conversion → CPA = $1 / 0.10 = $10.

Write current metrics per ad group to `sem-baseline.md`.

**WHY:** Optimization without baseline metrics is guessing. The three formulas are the universal measurement framework — every SEM decision ultimately traces back to one of these numbers. Founders who skip the baseline and jump to "optimize my ads" produce random changes with random results.

### Step 2: Evaluate Quality Score Against Benchmarks

**ACTION:** Check CTR against Google's Quality Score benchmarks:

- **Average CTR benchmark: 2.0%** — this is the rough AdWords average
- **Low threshold: 1.5%** — below this, Google assigns low Quality Score → worse ad placements AND higher CPC

For each ad group with CTR < 1.5%, flag it. You're in a Quality Score penalty spiral: low CTR → low Quality Score → higher CPC → worse ROI.

**WHY:** Quality Score is a multiplicative effect. An ad with CTR of 1% doesn't just get worse performance — Google charges more per click AND shows the ad less often. This is a doom loop that only gets worse unless fixed. The 1.5% threshold is where the penalty kicks in hard.

**IF** CTR is 1.5-2.0% → rewrite ad copy for relevance, use Dynamic Keyword Insertion.
**IF** CTR is below 1.5% → consider pausing the ad group entirely while you rewrite.

### Step 3: Apply Keyword Profitability Filter

**ACTION:** For each keyword, calculate: **Is CPA less than LTV × profit margin?**

Formula: profitable keyword = CPA < LTV_margin

Example: LTV = $300, 30% margin = $90 profit per customer. If CPA > $90, the keyword is losing money.

Keywords are profitable in three bands:
- **Highly profitable** (CPA < 30% of LTV margin) — scale spend
- **Marginally profitable** (CPA 30-100% of LTV margin) — optimize or maintain
- **Unprofitable** (CPA > LTV margin) — pause or kill

**WHY:** Founders often compare CPA to product price, not to profit margin. At $99/month product price, a $95 CPA looks fine — until you remember you only make $30 profit per month and the customer churns in 8 months. True profitability needs margin and retention in the calculation, not just price.

**IF** you don't have retention data → assume 12-month average and adjust as data comes in.

### Step 4: Prune Unprofitable Keywords

**ACTION:** Pause or delete unprofitable keywords identified in Step 3. Be ruthless — a portfolio of 100,000 keywords is not inherently better than 10,000 profitable ones.

Archives.com case study: started with 100,000 keywords, pruned to 50,000 profitable ones. The pruning itself improved average CPA by removing drag from unprofitable keywords that were consuming budget.

Write the pruning list to `sem-pruning.md` with reasons per keyword.

**WHY:** Unprofitable keywords consume budget that could go to profitable ones. Even if you don't scale spend, removing bad keywords redirects the same budget to good keywords, improving overall CPA. The pruning is often the fastest win in an SEM optimization project.

### Step 5: Expand to Long-Tail and Restructure Ad Groups

**ACTION:** For profitable category keywords, expand to long-tail variants:

- Category keyword: "project management software"
- Long-tail variants: "project management software for construction", "cheap project management software", "project management software vs Asana"

Long-tail keywords are less competitive → lower CPC → often higher conversion (more specific intent).

Restructure ad groups by keyword cluster — each tight cluster gets its own ad group with relevant ad copy and landing page. Use Dynamic Keyword Insertion to personalize ads by query.

**WHY:** Broad ad groups mean one ad tries to match 50 different queries — Quality Score suffers because the ad isn't specific enough. Tight ad groups (5-10 related keywords) with custom ad copy produce dramatically higher CTR and lower CPC. This is the single biggest structural win in mature SEM accounts.

## Inputs

- Current SEM metrics (spend, clicks, conversions, per ad group)
- Unit economics (LTV, margin)
- Target keywords or existing keyword list

## Outputs

Four markdown/data files:

1. **`sem-baseline.md`** — CTR, CPC, CPA per ad group
2. **`sem-quality-score-audit.md`** — Ad groups flagged by Quality Score threshold
3. **`sem-pruning.md`** — Unprofitable keywords to pause with reasons
4. **`sem-optimization-plan.md`** — Ad group restructure, long-tail expansion, A/B test queue

## Key Principles

- **CTR below 1.5% is a doom loop.** Fix or pause immediately. WHY: Google penalizes low Quality Score with higher CPC AND lower impressions. Letting a low-CTR ad group run is actively worse than pausing it.

- **Profitable keyword = CPA < LTV margin, not CPA < product price.** WHY: Product price is revenue, not profit. Unit economics depend on margin and retention, not list price. Comparing CPA to price produces keywords that "look profitable" but lose money over the customer lifetime.

- **Prune aggressively.** 10,000 profitable keywords beats 100,000 mixed. WHY: Unprofitable keywords consume the budget that could go to profitable ones. Pruning redirects spend without growing it.

- **Tight ad groups beat broad ad groups.** 5-10 closely-related keywords per ad group with custom copy. WHY: Google's Quality Score rewards relevance. Broad ad groups where one ad tries to match 50 queries tank CTR and raise CPC.

- **Long-tail is where profit lives.** Category terms are competitive and expensive. Long-tail is less competitive AND has higher intent. WHY: "Project management software" has 50 advertisers bidding; "construction project management software for contractors" has 3. Lower competition + higher specificity = better unit economics.

- **Use SEM to validate SEO potential.** If a keyword converts well on paid search, it's worth pursuing on organic search. If it doesn't convert on paid, SEO won't save it. WHY: SEM is fast keyword validation. SEO takes months to rank. Using SEM to test before committing to SEO saves months.

## Examples

**Scenario: SaaS founder with rising CAC**

Trigger: "Our Google Ads CAC was $80 six months ago. Now it's $140. Product price $79/month. What's going on?"

Process: (1) Calculate current metrics by ad group. Find 3 groups with CTR < 1.5% — Quality Score penalty spiral. (2) Unit economics check: $79 × 30% margin × 12 months = $284 LTV profit. $140 CAC is still profitable (LTV:CAC 2:1) but trajectory is wrong. (3) Prune: 15 keywords have CPA > $200 — kill them. (4) Restructure: 3 broad ad groups → 12 tight ad groups with specific copy. (5) Long-tail expansion: add 40 specific variants targeting buyer intent phrases.

Output: Clear diagnosis (Quality Score + bad ad group structure), pruning list, restructuring plan.

**Scenario: Testing SEM as a new channel**

Trigger: "We want to try Google Ads for our B2B analytics tool. $1k test budget. Never run ads before."

Process: (1) Research existing search volume on category terms via Keyword Planner. (2) Check competitor CPCs — if top-of-page bid is $8, $1k gives 125 clicks. (3) Design test: 5 keyword clusters, tight ad groups, 2 ads per group, 1 landing page per cluster. (4) Profitability filter: target CPA < $200 (assuming $50/month × 30% × 12 = $180 LTV profit = need CPA < $180). (5) Test for 2 weeks, measure. If profitable → scale. If not → prune and try long-tail.

Output: Structured first test with clear profitability criteria and scale/abandon decision rule.

**Scenario: Inherited a messy 100k-keyword account**

Trigger: "Took over SEM for a company that has 100,000 keywords across 200 ad groups. CAC is all over the place. Where do I start?"

Process: (1) Export current data — spend, conversions, CPA per keyword/ad group. (2) Apply profitability filter to every row. Identify the 20% of keywords producing 80% of conversions. (3) Quality Score audit — find ad groups in the penalty spiral. (4) Aggressive prune: pause everything unprofitable (expect to cut 30-60% of keywords). (5) Restructure remaining into tight ad groups. (6) Re-test over 2 weeks and compare.

Output: Prioritized cleanup plan, pruning list, restructuring roadmap — the Archives.com pattern of 100k → 50k.

## References

- For ad group structure patterns and Dynamic Keyword Insertion examples, see [references/sem-structure.md](references/sem-structure.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select SEM via Bullseye before deep optimization
- `clawhub install bookforge-seo-channel-strategy` — SEO complements SEM for category terms
- `clawhub install bookforge-traction-channel-testing` — CAC/LTV framework applies here

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
