---
name: advertising-media-roi-framework
id: advertising-media-roi-framework
title: Advertising Media & ROI Framework
description: >
  Use when selecting advertising media channels, calculating Customer Acquisition Cost (CAC) per channel,
  deciding whether to stop, measure, or scale each channel, checking for dangerous single-point-of-failure
  lead source dependencies, or building a diversified media plan with per-channel tracking setup and
  ROI decision rules. Triggers: "advertising media", "ROI calculation", "CAC", "customer acquisition cost",
  "where to advertise", "marketing channels", "lead sources", "stop losing money on ads", "scale marketing",
  "single point of failure marketing", "diversify ad channels", "track marketing ROI", "media plan",
  "fill square 3", "which channels should I use", "is my advertising working".
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/advertising-media-roi-framework
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - title: "The 1-Page Marketing Plan"
    author: Allan Dib
    chapters: [3]
source-book: the-1-page-marketing-plan
source-chapters: [3]
quality:
  scores:
    with_skill: 92.9
    baseline: 7.1
    delta: 85.7
  tested_at: "2026-04-09"
  eval_count: 1
  assertion_count: 14
  iterations_needed: 1
depends-on:
  - target-market-selection-pvp-index
  - marketing-message-and-usp-crafting
  - lead-capture-ethical-bribe-design
tags:
  - marketing
  - advertising
  - media-selection
  - roi
  - cac
  - small-business
---

# Advertising Media & ROI Framework

## When to Use

Use this skill when a business owner needs to:
- Decide which advertising channels to use to reach their target market
- Calculate whether current ad spend is generating positive or negative return
- Determine whether to stop, fix measurement on, or aggressively scale a channel
- Audit their lead source portfolio for dangerous single-source dependency
- Build a structured media plan with per-channel budgets, tracking mechanisms, and decision rules

This is square 3 of the 1-Page Marketing Plan canvas: **What media will you use to reach your target market?**

Do not confuse media selection with market selection (square 1) or message crafting (square 2). All three must be right for a campaign to succeed.

---

## Context & Input Gathering

Before building the media plan, confirm these inputs are known. If any are missing, resolve them first.

**Required inputs:**

| Input | Source |
|-------|--------|
| Target market definition | IF unknown → invoke `target-market-selection-pvp-index` OR ask: "Who is your ideal customer — describe them specifically." |
| Marketing message / Unique Selling Proposition (USP) | IF unknown → invoke `marketing-message-and-usp-crafting` OR ask: "What is the core message you send to prospects?" |
| Lead capture offer (ethical bribe) | IF unknown → invoke `lead-capture-ethical-bribe-design` OR ask: "What do you offer prospects in exchange for their contact details?" |
| Profit per sale (front-end) | Ask: "What is your average profit per transaction on the first sale?" |
| Customer Lifetime Value (CLV) estimate | Ask: "What does a typical customer spend with you over their entire relationship? (rough estimate is fine)" |
| Current advertising channels + monthly spend | Ask: "List every channel you currently advertise on and how much you spend per month on each." |
| Tracking currently in place | Ask: "How do you currently track where your leads and customers come from?" |

**Why gather all inputs first:** The CAC calculation requires profit-per-sale and CLV to make stop/scale decisions. Skipping this step leads to decisions based on vanity metrics (response rate, open rate) rather than actual ROI.

---

## Process

### Step 1 — Audit Existing Channels

For each channel the business currently uses:

1. Record: channel name, monthly ad spend, leads generated, customers acquired.
2. Calculate CAC per channel (formula below).
3. Compare CAC to profit-per-sale and CLV.
4. Apply the 3-Scenario Decision Rule.
5. Flag any channel with no tracking in place as Priority Fix.

**Why audit before adding new channels:** Scaling broken channels wastes money. Cutting losers frees budget for winners and new tests.

---

### Step 2 — Calculate Customer Acquisition Cost (CAC)

**The CAC Formula:**

```
CAC = Total Campaign Cost ÷ Number of Customers Acquired
```

**Worked example (direct mail):**
- Send 100 letters at a total print + postage cost of $300
- 10 people respond (10% response rate)
- 2 of those 10 become customers (20% closure rate)
- Customers acquired = 2
- **CAC = $300 ÷ 2 = $150**

**Decision:**
- If profit per sale = $600 → net gain = $600 − $150 = **+$450 per customer** → WINNING
- If profit per sale = $100 → net loss = $100 − $150 = **−$50 per customer** → LOSING

**Important:** Response rate and conversion rate are intermediate metrics only. They help calculate CAC but are not the goal. The only numbers that matter are **CAC** and **CLV**.

**The CLV exception:** If front-end profit is less than CAC but CLV is confirmed high (e.g., subscription businesses, repeat-purchase businesses), accepting a front-end loss is a deliberate strategy — not a failure. Do not apply this exception until CLV is measured, not estimated.

---

### Step 3 — Apply the 3-Scenario Decision Rule

For every channel, exactly one of three situations is true:

| Scenario | Condition | Action |
|----------|-----------|--------|
| **FAIL** | Profit per sale < CAC (negative ROI), consistently | **STOP.** Change the channel, the message, or the offer. Do not continue spending on a confirmed loser. |
| **UNMEASURED** | No tracking in place; ROI unknown | **FIX MEASUREMENT IMMEDIATELY.** With tools readily available (toll-free numbers, UTM codes, coupon codes, dedicated landing pages, call tracking), not measuring is inexcusable. Treat this as urgent. |
| **WIN** | Profit per sale > CAC (positive ROI), consistently | **SCALE AGGRESSIVELY. No budget cap.** Winning marketing is not an expense — it is a legal money printing press. Capping spend on a winner is like refusing to buy $100 bills at $80. |

**Why no budget cap on winners:** Setting a fixed "marketing budget" implies either (a) marketing is not working or (b) you do not know if it is working. If it works, the only sensible limit is operational capacity — and even that signals it is time to raise prices.

**Testing phase exception:** During initial testing, spend conservatively. Fail fast and fail cheap. Test headline, offer, positioning, and channel variables one at a time. Once a winner emerges, remove the cap.

---

### Step 4 — Check 5-Source Diversification

Count the number of distinct, active lead sources generating customers.

**Rule: Minimum 5 different lead sources.**

**Why 5 is the floor:** One is the most dangerous number in any business. Single-source dependency creates fragility:

- **Google Slap** (2000s–2010s): Google increased pay-per-click costs 4–10x overnight for certain categories, halting campaigns immediately.
- **SEO algorithm change**: Businesses that relied entirely on organic search rankings lost their lead flow overnight when Google updated its algorithm.
- **Fax broadcasting**: Outlawed in the United States. Every business relying solely on this channel went broke.
- **Single large customer departing**: Revenue collapses with no pipeline to replace it.

If fewer than 5 sources exist, identify candidates for new channels to test (see Step 5).

**Prefer paid media for most sources.** Paid media is reliable (if you pay, the ad runs) and forces ROI discipline (if it does not work, you cut it). Free or "organic" methods such as word of mouth have no measurement pressure — time wasted on ineffective free channels carries an opportunity cost that translates to real money.

**Own your marketing assets.** Social media platforms can change their rules at any time. An email subscriber list you own is more valuable than 10x the followers on a platform you do not own.

---

### Step 5 — Identify New Channel Candidates

Match candidate channels to the target market profile:

1. **Where does the target market spend time?** (Online communities, industry publications, local venues, social platforms, physical locations)
2. **What media do they trust?** (Peer referrals, trade publications, search, direct mail, radio)
3. **What channels are competitors NOT using?** (Under-competition means lower cost and higher attention)
4. **What channels allow direct response measurement?** (Prefer channels where you can attach a unique phone number, URL, or code)

Rank candidates by: (a) target market reach, (b) trackability, (c) estimated cost per lead, (d) time to first result.

Select the top 2–3 to test. Do not test more than 3 new channels simultaneously — it obscures what is working.

---

### Step 6 — Set Up Tracking Mechanisms Per Channel

For each channel (existing and new), assign at least one tracking mechanism before spending:

| Tracking Method | Best For |
|-----------------|----------|
| Unique toll-free number per campaign | Direct mail, print, radio, TV |
| UTM parameters on URLs | Online ads, email, social |
| Dedicated landing page per source | Online ads, QR codes in print |
| Coupon or promo codes | Any channel |
| Call tracking software | Phone-heavy businesses |
| "How did you hear about us?" (at point of sale) | Backup for all channels |

**Why tracking is non-negotiable:** Without tracking, Scenario 2 (UNMEASURED) applies to every channel. You cannot cut losers or scale winners. The technology exists and is inexpensive. Not using it is a choice to operate blind.

---

### Step 7 — Draft the Media Plan Document

Produce `media-plan.md` using the structure below.

---

## Inputs

- Target market profile (from `target-market-selection-pvp-index`)
- Marketing message / USP (from `marketing-message-and-usp-crafting`)
- Lead capture offer (from `lead-capture-ethical-bribe-design`)
- Profit per sale (front-end)
- Customer Lifetime Value (CLV)
- Current channel list with spend data
- Current tracking status per channel

---

## Outputs

### Primary: `media-plan.md`

```markdown
# Media Plan — [Business Name]
**Date:** [Date]
**Target Market:** [From square 1]
**Core Message:** [From square 2]
**Lead Capture Offer:** [From square 4]
**Profit Per Sale (Front-End):** $[X]
**Customer Lifetime Value (CLV):** $[X]

---

## Channel Decision Table

| Channel | Monthly Spend | Customers/Mo | CAC | Profit/Sale | Decision | Tracking Method |
|---------|--------------|-------------|-----|-------------|----------|-----------------|
| [e.g. Google Ads] | $[X] | [X] | $[X] | $[X] | SCALE / STOP / MEASURE | UTM + landing page |
| [e.g. Direct Mail] | $[X] | [X] | $[X] | $[X] | SCALE / STOP / MEASURE | Unique phone # |
| [e.g. Email List]  | $[X] | [X] | $[X] | $[X] | SCALE / STOP / MEASURE | Tracked links |
| ... | | | | | | |

**Total active channels:** [X] / 5 minimum required
**Diversification status:** [ADEQUATE / AT RISK — add [X] more sources]

---

## New Channel Tests (next 90 days)

| Channel | Rationale | Test Budget | Tracking Setup | Success Threshold (CAC) |
|---------|-----------|-------------|----------------|-------------------------|
| [Channel] | [Why this market is there] | $[X] | [Method] | CAC < $[X] |

---

## Decision Rules Summary

- Any channel with CAC < profit/sale for 3+ consecutive months → **Scale, no cap**
- Any channel with CAC > profit/sale for 2+ consecutive months → **Stop. Reallocate.**
- Any channel with no tracking → **Fix tracking within 2 weeks or pause spend**
- Total lead sources < 5 → **Add one new test channel per quarter until threshold met**
```

---

## Key Principles

**cac-vs-profit-decision:** The only question that matters for any advertising channel is: does CAC exceed or fall below profit per sale (adjusted for CLV)? Response rates, open rates, click-through rates are intermediate metrics — useful only for diagnosing why CAC is high or low.

**no-budget-cap-on-winning-channels:** Setting a marketing budget on a channel with confirmed positive ROI is equivalent to refusing discounted money. The only legitimate budget limit during active campaigns is operational capacity to fulfill demand — which itself signals an opportunity to raise prices.

**5-source-diversification:** Relying on fewer than 5 lead sources makes the business brittle. Any external change — algorithm updates, regulatory changes, platform policy shifts, cost spikes — can eliminate a single-source business's lead flow overnight.

**paid-over-free-media:** Paid media is preferred for most of the 5 sources because (a) it is reliable — paying for placement means the ad runs, and (b) it forces ROI accountability — when money is at stake, measurement follows. Free channels such as word of mouth carry hidden time costs and no inherent measurement pressure.

**tracking-is-non-negotiable:** Not measuring where leads and sales come from is the mark of an amateur. Modern tracking tools (toll-free numbers, UTM codes, call tracking, dedicated landing pages) are inexpensive and readily available. Running any campaign without tracking is a deliberate choice to waste money.

**reject-arbitrary-marketing-budget:** Treating marketing as a fixed expense category implies it either does not work or is not being measured. Marketing that works is an investment with measurable return, not an expense with a ceiling.

**front-end-back-end-distinction:** Profit per sale on first purchase (front-end) may be lower than CAC in high-CLV businesses. Accepting a front-end loss is only valid when CLV is confirmed through actual measurement — not assumption.

---

## Examples

### Example 1: Direct Mail CAC Calculation (Verbatim)

A plumbing company sends a direct mail campaign:
- 100 letters sent; print + postage cost = $300
- 10 recipients respond (10% response rate)
- 2 of the 10 responders become customers (20% closure rate)
- **CAC = $300 ÷ 2 = $150**

If the profit per job is $600: net per customer = $600 − $150 = **+$450. Scale.**
If the profit per job is $100: net per customer = $100 − $150 = **−$50. Stop and rethink.**

The response rate (10%) is irrelevant in isolation. A 0.5% response rate that yields a CAC of $80 against $600 profit per sale is far better than a 15% response rate that yields a CAC of $200.

---

### Example 2: Google Slap — Single-Source Failure

A software reseller built its entire lead flow on Google pay-per-click (PPC) ads. Monthly spend: $5,000. CAC was positive, business growing.

Google changed its ad classification rules. Overnight, the cost per click increased 5x. Monthly spend to maintain the same lead volume jumped to $25,000 — above the business's operating capacity.

The business had no alternative lead sources. It halted its Google campaign while investigating, and lead flow dropped to zero for 6 weeks. Revenue collapsed.

**Prevention:** Had the business maintained 5 lead sources (e.g., Google PPC + email list + direct mail + SEO content + referral program), one source failing would have reduced lead flow by roughly 20%, not 100%.

---

### Example 3: Multi-Channel Plan for a Local Accounting Firm

**Target market:** Small business owners (1–10 employees) in a single metro area.
**Profit per engagement:** $1,200/year average
**CLV:** $4,800 (4-year average tenure)
**CAC threshold for front-end:** $1,200 (break even on first year)
**CAC threshold with CLV:** $2,000 (still profitable over tenure)

| Channel | Monthly Spend | CAC | Decision | Tracking |
|---------|--------------|-----|----------|----------|
| Google Ads (local) | $800 | $900 | SCALE | UTM + dedicated landing page |
| Direct mail (local biz list) | $400 | $1,100 | MEASURE (3 months) | Unique phone # |
| LinkedIn outreach | $0 (time) | Unknown | MEASURE | CRM tagging |
| Referral program | $200 | $400 | SCALE | Referral codes |
| Email newsletter | $50 | $600 | SCALE | Tracked links |

Total sources: 5. Diversification: ADEQUATE.

Next test: local radio (30-day test, $600 budget, unique phone number, CAC threshold $1,200).

---

## References

- Source: "The 1-Page Marketing Plan" by Allan Dib, Chapter 3 "Reaching Prospects with Advertising Media," pp. 103–126
- Related skills: `target-market-selection-pvp-index` (square 1), `marketing-message-and-usp-crafting` (square 2), `lead-capture-ethical-bribe-design` (square 4), `customer-lifetime-value-growth` (CLV expansion), `marketing-metrics-dashboard` (ongoing measurement)
- The 3M framework: Market (Ch. 1) + Message (Ch. 2) + Media (Ch. 3) must all be correct for a campaign to succeed. Failure on any one causes campaign failure regardless of the other two.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-target-market-selection-pvp-index`
- `clawhub install bookforge-marketing-message-and-usp-crafting`
- `clawhub install bookforge-lead-capture-ethical-bribe-design`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
