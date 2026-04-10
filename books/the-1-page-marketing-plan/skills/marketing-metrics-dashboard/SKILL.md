---
name: marketing-metrics-dashboard
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/marketing-metrics-dashboard
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
quality:
  scores:
    with_skill: 92
    baseline: 31
    delta: 61
  tested_at: "2026-04-09"
  eval_count: 1
  assertion_count: 13
  iterations_needed: 1
description: >
  Build a marketing metrics dashboard tracking the 7 key numbers every small business must measure:
  Leads, Conversion Rate, Average Transaction Value (ATV), Break-Even Point, Gross Margin, Churn Rate,
  and Customer Lifetime Value (CLV) — plus Customer Acquisition Cost (CAC). Use this skill whenever the
  user wants to measure marketing performance, set up a KPI dashboard, track marketing ROI, fill in their
  key numbers, understand which metrics to watch, analyze leads and conversion, calculate CAC, compute CLV,
  identify profit improvement levers, run a marketing analytics review, understand small business metrics,
  build a marketing scorecard, or model what happens when they improve just 3 metrics by 10%. Demonstrates
  the compounding leverage insight: small improvements across multiple metrics multiply — not add — producing
  disproportionate profit gains. Also covers the CAC vs profit-per-sale decision rule for evaluating whether
  a marketing campaign is a winner or loser.
source:
  book: "The 1-Page Marketing Plan: Get New Customers, Make More Money, and Stand Out from the Crowd"
  author: "Allan Dib"
  chapters: ["Chapter 8: Increasing Customer Lifetime Value", "Chapter 3: Reaching Your Prospects"]
  pages: "237-241, 107-110"
tags: [marketing, metrics, analytics, small-business, kpi]
execution-tier: 1
execution-mode: full
density-score: 5
depends-on: []
---

# Marketing Metrics Dashboard

## When to Use

Use this skill when a business owner, solopreneur, or entrepreneur needs to:

- Identify which marketing numbers to track and why
- Build or populate a dashboard with current metric values
- Understand whether their marketing spend is profitable (CAC vs profit decision)
- Model the impact of small improvements across multiple levers
- Set targets and decision rules per metric before the next review cycle

**Preconditions:** The user should have at least rough estimates for their current business numbers. If they have none, the skill walks them through estimation. An existing dashboard can be updated or rebuilt from scratch.

**Before starting, verify:** Do you have current numbers, estimates, or are we starting from zero? Knowing the starting point determines whether this is a measurement session (fill in real numbers) or a planning session (set initial targets with estimates).

---

## Context & Input Gathering

### Required Context (ask if missing)

- **Business type and revenue model:** whether the business is transactional, subscription/recurring, or project-based — this determines which metrics matter most and which update cadence to use.
  → Check prompt for: descriptions of how they charge customers (per-job, monthly, subscription, retail)
  → If missing, ask: "Do customers buy once, come back repeatedly at their own pace, or pay you on a recurring subscription?"

- **Approximate monthly revenue range:** needed to sanity-check metric estimates and select the right dashboard format.
  → Check prompt for: dollar figures, revenue mentions
  → If missing, ask: "Roughly what is your monthly revenue — under $10K, $10K–$100K, or over $100K?"

### Observable Context (gather from environment)

- **Existing financial or marketing files:** look for any spreadsheets, CRM exports, ad spend reports, or revenue summaries in the working directory.
  → Look for: `*.csv`, `*.xlsx`, `revenue*.md`, `marketing*.md`, `dashboard*.md`
  → If unavailable: proceed with user-provided estimates; note all assumptions explicitly.

### Default Assumptions

- Measurement cadence: monthly (suitable for most small businesses; shift to weekly if revenue is high-velocity)
- Dashboard format: markdown document (universal; upgrade to Geckoboard or spreadsheet if user requests)
- CAC calculation: per-campaign basis, not blended average — unless user specifies otherwise

### Sufficiency Threshold

Proceed when: business type is known AND at least 3 of the 7 metrics have a current value or estimate.
Ask before proceeding when: no numbers are available at all — use estimation prompts to unblock.
Proceed with defaults when: some metrics are unknown; mark them as "TBD — estimate by [method]" in the dashboard.

---

## Process

### Step 1: Gather Current Metric Values

**ACTION:** Collect or estimate values for all 7 core metrics plus CAC. Work through each metric below. If the user doesn't know an exact number, ask them to estimate or calculate it from what they do know.

**WHY:** You cannot improve what you don't measure. Many business owners rely on gut feel or total revenue alone, which hides the levers that actually drive profit. Establishing baseline numbers — even rough estimates — is the prerequisite for all improvement.

For each metric, apply these collection questions:

| Metric | What to collect | Estimation fallback |
|--------|----------------|---------------------|
| **Leads** | New contacts entering the business per month | Count website visitors, inquiries, ad clicks, walk-ins |
| **Conversion Rate** | % of leads who become paying customers | (Customers acquired this month) ÷ (Leads this month) × 100 |
| **Average Transaction Value (ATV)** | Average dollar amount per purchase | Total revenue ÷ number of transactions |
| **Break-Even Point** | Monthly fixed cost floor | Sum: rent + staff + utilities + software + insurance + any recurring fixed costs |
| **Gross Margin** | Profit % after cost of goods/services | (Revenue − direct costs) ÷ Revenue × 100 |
| **Churn Rate** | % of recurring customers who cancel or stop buying per period | (Customers lost this period) ÷ (Customers at start of period) × 100 |
| **Customer Lifetime Value (CLV)** | Total revenue expected over a customer's full tenure | ATV × average purchases per year × average years retained |

**CAC (Customer Acquisition Cost):**
- Formula: Total campaign spend ÷ number of new customers acquired from that campaign
- Collect separately per marketing channel when possible

**IF** the user has no recurring customers → skip Churn Rate and CLV; note "not yet applicable — add subscription/repeat element to unlock."

**ELSE** → compute all 7 metrics and CAC.

---

### Step 2: Classify Each Metric by Health Status

**ACTION:** For each metric with a current value, assign a health status: **Healthy**, **Watch**, or **Act Now**. Use the interpretation guide below.

**WHY:** Raw numbers without context are meaningless. Classification converts data into decisions — it tells you where attention is required and where things can run on autopilot.

**Interpretation guide:**

| Metric | Healthy signal | Watch signal | Act Now signal |
|--------|---------------|--------------|----------------|
| Leads | Growing month-over-month | Flat 3+ months | Declining |
| Conversion Rate | >industry benchmark; improving | Flat | Declining or below 1% for transactional |
| ATV | Growing (upsell/pricing working) | Flat | Declining or customer pushback on price |
| Break-Even | Covered with >20% buffer | Covered with <10% buffer | Revenue at or below break-even |
| Gross Margin | >50% for digital/service; >30% for physical | 20–30% | <20% or declining |
| Churn Rate | <2%/month for subscriptions | 2–5%/month | >5%/month (leaky bucket problem) |
| CLV | CLV > 3× CAC | CLV 1–3× CAC | CLV < CAC (losing money per customer) |

---

### Step 3: Compute CAC vs Profit Decision

**ACTION:** For each active marketing campaign or channel, apply the CAC profitability test:

1. Calculate CAC = (campaign total spend) ÷ (customers acquired from campaign)
2. Calculate profit per new customer = ATV × Gross Margin % (front-end profit only)
3. Apply decision rule:
   - **If profit per sale > CAC → winning campaign** (keep, scale, or optimize)
   - **If profit per sale < CAC → losing campaign** (stop, unless CLV justifies front-end loss — see below)
   - **If CLV is high and well-understood → front-end loss may be acceptable** (subscription or high-repeat businesses can "go negative" on acquisition if lifetime value is proven)

**WHY:** Response rates and conversion rates in isolation are vanity metrics. The only number that matters is whether the campaign made money — which requires knowing both what you spent (CAC) and what you earned (profit per customer, optionally adjusted for CLV). A campaign with a 2% conversion rate can be a winner or a loser depending on these numbers.

---

### Step 4: Identify the 3 Highest-Leverage Metrics

**ACTION:** From the 7 core metrics, select the 3 that are:
(a) currently classified "Act Now" or "Watch", AND
(b) most directly under the business owner's control in the next 90 days

Priority ordering when multiple candidates exist:
1. Conversion Rate — often the highest-leverage single number because it multiplies everything downstream
2. Average Transaction Value — improves with upsells, bundles, or pricing changes; no new leads required
3. Leads — scalable but requires marketing spend or effort; slower to move

**WHY:** Attempting to improve all 7 metrics simultaneously spreads attention too thin and produces no meaningful result in any area. Focusing on 3 creates compounding: improvements multiply across each other rather than adding linearly, generating disproportionate profit impact from the same effort.

---

### Step 5: Model the 10% Compounding Scenario

**ACTION:** For each of the 3 chosen metrics, calculate what a 10% improvement produces — both individually and in combination.

Use this calculation sequence:

```
Current State:
  Total Conversions = Leads × Conversion Rate
  Total Revenue = Total Conversions × ATV
  Gross Profit = Total Revenue × Gross Margin %
  Net Profit = Gross Profit − Break-Even Point

After 10% improvement on all 3 chosen metrics:
  New Leads = Leads × 1.10  (if Leads is a chosen lever)
  New Conversion Rate = Conversion Rate × 1.10  (if Conv Rate is chosen)
  New ATV = ATV × 1.10  (if ATV is chosen)
  Recompute: New Total Conversions → New Revenue → New Gross Profit → New Net Profit

Net Profit Improvement % = (New Net Profit − Current Net Profit) / Current Net Profit × 100
```

**WHY:** The compounding effect is the most important insight in marketing metrics: because improvements multiply together, a 10% gain on 3 levers does not produce a 30% profit gain — it produces something far larger, especially when the break-even point is fixed. The worked example below shows a 431% net profit improvement from exactly this mechanism.

**Show both the "before" and "after" tables** so the magnitude of the leverage is visible.

---

### Step 6: Produce the Dashboard Document

**ACTION:** Write the completed dashboard as a markdown document. Include current values, health status, target values, decision rules, and the compounding scenario output.

**WHY:** A dashboard only works if it is reviewed regularly. A concrete document with clear decision rules and target values transforms the data into a system — something that gets checked weekly or monthly rather than forgotten. Tying metrics to decisions and owners makes it actionable.

Output format: see the **Outputs** section below for the complete dashboard template.

---

## Inputs

- Current business numbers: leads per month, conversion rate, ATV, fixed monthly costs, gross margin, churn rate (if recurring model), CLV estimate
- Marketing spend per campaign or channel (for CAC calculation)
- Business model type (transactional, recurring, project-based)
- Any existing dashboard files or financial summaries in the working directory

---

## Outputs

### Primary Output: `marketing-metrics-dashboard.md`

```markdown
# Marketing Metrics Dashboard
**Business:** [Business name]
**Period:** [Month/Quarter]
**Last Updated:** [Date]
**Update Cadence:** [Weekly / Monthly]

---

## Core Metrics Snapshot

| Metric | Current Value | Status | Target | Decision Rule |
|--------|--------------|--------|--------|---------------|
| Leads | [value] | [Healthy / Watch / Act Now] | [target] | If declining 2+ months → audit traffic source; review ad copy |
| Conversion Rate | [value]% | [status] | [target]% | If below [X]% → review sales process, guarantee, and follow-up sequence |
| Avg Transaction Value | [value] | [status] | [target] | If flat → add upsell, bundle, or raise prices on best-sellers |
| Break-Even Point | [value]/mo | [covered/at risk] | Fixed cost floor | If revenue ≤ break-even → freeze discretionary spend immediately |
| Gross Margin | [value]% | [status] | [target]% | If declining → review supplier costs or pricing; never discount without justification |
| Churn Rate | [value]%/mo | [status] | <[X]%/mo | If >5%/mo → prioritize retention over acquisition; diagnose top 3 exit reasons |
| Customer Lifetime Value | [value] | [status] | [target] | If CLV < 3× CAC → optimize retention before scaling acquisition |

---

## Customer Acquisition Cost (CAC) by Channel

| Channel | Spend | New Customers | CAC | Profit/Customer | Decision |
|---------|-------|--------------|-----|----------------|----------|
| [Channel 1] | [spend] | [count] | [CAC] | [profit] | Win / Loss / Front-end loss OK (high CLV) |
| [Channel 2] | | | | | |

**CAC Formula:** Total campaign spend ÷ customers acquired from that campaign
**Win condition:** Profit per sale > CAC
**Loss condition:** Profit per sale < CAC (stop unless CLV justifies it)

---

## 3 Highest-Leverage Metrics (90-Day Focus)

1. **[Metric 1]** — Current: [X], Target: [Y], Owner: [Name/Role]
   Action: [Specific intervention — e.g., "Add outrageous guarantee to checkout page"]

2. **[Metric 2]** — Current: [X], Target: [Y], Owner: [Name/Role]
   Action: [Specific intervention]

3. **[Metric 3]** — Current: [X], Target: [Y], Owner: [Name/Role]
   Action: [Specific intervention]

---

## Compounding Leverage Projection (10% on 3 Levers)

| | Before | After (+10% on 3 levers) |
|-|--------|--------------------------|
| Leads | [value] | [value × 1.10] |
| Conversion Rate | [X]% | [X × 1.10]% |
| Total Conversions | [L × CR] | [new L × new CR] |
| Average Transaction Value | [value] | [value × 1.10] |
| Total Revenue | [value] | [new convs × new ATV] |
| Gross Margin | [X]% | [X]% |
| Total Gross Profit | [rev × margin] | [new rev × margin] |
| Break-Even Point | [fixed] | [fixed] |
| **Net Profit** | **[GP − BE]** | **[new GP − BE]** |
| **Net Profit Improvement** | | **[improvement %]** |

**Key insight:** Fixed costs (break-even) don't increase when you improve these 3 levers.
Every additional dollar of gross profit above break-even flows directly to net profit.
This is why small percentage improvements compound into large net profit gains.

---

## Dashboard Format & Review Schedule

- **Format:** [Whiteboard with manual updates / Spreadsheet / Geckoboard / Internal web page]
- **Review frequency:** [Weekly / Monthly]
- **Review owner:** [Name]
- **Next review date:** [Date]

### Incentive Ties (optional)
- Team dinner if churn rate stays below [X]% this month
- Bonus pool unlocked when net profit exceeds [target]
```

---

## Key Principles

- **Measure 7 specific numbers, not everything** — most businesses track revenue and little else, which hides the levers driving it. The 7 metrics above cover the full revenue equation: how many enter (leads), how many convert, how much they spend, what it costs to run, and how long they stay.

- **Small improvements compound, not add** — a 10% gain on leads, conversion, and ATV produces far more than 30% profit growth because the break-even point is fixed. Every incremental dollar of gross profit above that fixed floor goes straight to net profit. This is the fundamental leverage point of direct-response marketing.

- **CAC is the north star of campaign evaluation** — response rates, click-through rates, and impressions are intermediate signals. The only campaign metric that matters is: did profit per customer exceed cost per customer acquired? If yes, scale it. If no, stop it or fix it.

- **Churn is the master retention metric for recurring businesses** — you cannot fill a leaking bucket. High churn means every new customer simply replaces a lost one, leaving revenue flat regardless of lead volume. Fix churn before scaling acquisition.

- **Front-end loss can be rational if CLV is known** — businesses with high customer lifetime value (subscriptions, repeat-purchase models) can profitably lose money on the first transaction because subsequent purchases more than compensate. This is only safe when CLV is well-understood from actual data, not assumption.

- **Track all 7, focus on 3** — keep the full dashboard current so you have situational awareness. But direct improvement energy at the 3 highest-leverage metrics for the current 90-day period. Attempting to optimize everything simultaneously produces nothing.

- **The dashboard must be visible and reviewed on a schedule** — a metrics document that no one checks is worthless. Tie a review meeting, team incentive, or personal habit to the cadence. The dashboard is an early-warning system, not a historical record.

---

## Examples

### Example 1: The Compounding Leverage Worked Case (Online Electronics Store)

**Scenario:** Small online consumer electronics store importing from China. Healthy 50% margin. Owner wants to improve profitability without increasing fixed costs.

**Starting metrics:**
- Leads: 8,000/month
- Conversion Rate: 5%
- Total Conversions: 400
- Average Transaction Value: $500
- Total Revenue: $200,000
- Gross Margin: 50%
- Total Gross Profit: $100,000
- Break-Even Point: $90,000/month (warehouse, staff, hosting)
- Net Profit: $10,000/month ($120,000/year)

**Three interventions applied:**
1. More compelling ad copy → Leads increase from 8,000 to 8,800 (+10%)
2. Outrageous risk-reversal guarantee → Conversion Rate increases from 5% to 5.5% (+10%)
3. Checkout upsell offer → ATV increases from $500 to $550 (+10%)

**After metrics:**
- Leads: 8,800
- Conversion Rate: 5.5%
- Total Conversions: 484
- ATV: $550
- Total Revenue: $266,200
- Gross Margin: 50%
- Total Gross Profit: $133,100
- Break-Even Point: $90,000 (unchanged)
- Net Profit: $43,100/month ($517,200/year)

**Result:** Net profit improved from $10,000 to $43,100 — a **431% improvement** — from only 10% gains across 3 levers. Owner income increased from $120,000 to $517,200 annually. Fixed costs did not change.

**Why the leverage is so large:** Each intervention multiplied the others. More leads × higher conversion = more customers. More customers × higher ATV = more revenue. Fixed break-even point meant all incremental gross profit became net profit. The math compounds; it does not add.

---

### Example 2: Local Fitness Studio (Subscription Model)

**Scenario:** A fitness studio with 200 active members at $80/month. Owner notices revenue is flat despite steady new member sign-ups.

**Dashboard reveals:**
- Leads: 40 free-trial bookings/month
- Conversion Rate: 50% (20 new members/month)
- ATV: $80/month
- Break-Even: $12,000/month
- Gross Margin: 70%
- Churn Rate: 10%/month ← Act Now flag
- CLV: $80 × 12 months average = $960

**CAC analysis:**
- Google Ads spend: $1,000/month → 10 new members → CAC = $100
- Profit per new member front-end: $80 × 70% = $56 (front-end loss of $44)
- CLV-adjusted: $960 × 70% = $672 gross profit over tenure → campaign is a strong winner on CLV basis

**Problem identified:** Churn at 10%/month means losing 20 members/month — exactly equal to new acquisition. Revenue stays flat. Filling the bucket but it leaks as fast as it fills.

**3 highest-leverage focus (90 days):**
1. Churn Rate: target <4%/month — introduce member check-ins at week 3, 6, 10 (high-cancellation risk windows)
2. ATV: target $90/month — introduce premium membership tier with one-on-one coaching add-on
3. Conversion Rate: target 60% — improve free-trial experience with structured onboarding session

**Compounding projection (if all 3 improve 10%):**
- Churn improvement alone: 10% → 9% = 2 fewer lost members/month = net positive growth begins
- Combined effect: revenue trajectory turns from flat to growing; no increase in marketing spend required

---

## References

- For calculating Customer Lifetime Value in detail and the 5 levers to increase it (raise prices, upsell, ascension, frequency, win-back): see Chapter 8 of the source book
- For campaign-level CAC analysis and the 3-scenario decision framework (stop / measure / scale): see Chapter 3 of the source book
- For tools to pull metrics automatically: Geckoboard integrates with common small business platforms (Stripe, Shopify, Google Analytics, QuickBooks)
- For dashboard cadence guidance: weekly works well for high-velocity businesses (e-commerce); monthly is appropriate for service, consulting, or project-based businesses

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

No direct dependencies. Install the full book set from GitHub.

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
