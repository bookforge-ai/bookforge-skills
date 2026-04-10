---
name: customer-lifetime-value-growth
description: Grow Customer Lifetime Value (CLV) using five proven levers — raise prices, upsell at point of purchase, move customers up an ascension ladder, increase purchase frequency through reminders and subscriptions, and win back lapsed customers with a reactivation campaign. Use this skill when you want to increase customer lifetime value, grow CLV, grow revenue from existing customers, cross-sell or upsell, raise prices without losing customers, build a subscription model, increase repeat purchases, add recurring revenue, implement an ascension ladder, reactivate customers, win back customers, fill square 8, increase purchase frequency, run a reactivation campaign, grow revenue without new customer acquisition, apply the 20/80 rule to your customer base, or design a return-visit voucher system.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/customer-lifetime-value-growth
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan: Get New Customers, Make More Money, and Stand Out from the Crowd"
    authors: ["Allan Dib"]
    chapters: [8]
tags: [marketing, customer-retention, pricing, upsell, clv, small-business]
depends-on: ["customer-experience-systems-design"]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Business description — what the business sells, approximate average transaction value, rough customer count, and whether a customer list or CRM exists"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document set. Typical files: business-description.md, customer-list.csv or CRM export, current-pricing.md (to be created or referenced). Output: clv-growth-plan.md."
---

# Customer Lifetime Value Growth

## When to Use

You are a small business owner who wants to grow revenue without spending more on new customer acquisition. Typical triggers:

- Revenue is flat despite a healthy customer count
- You have not raised prices in over a year
- You make one sale per customer and then lose contact
- You have a lapsed customer list sitting unused in a CRM or spreadsheet
- You want to add recurring revenue to a currently transactional business
- You want to know what "square 8" of the 1-Page Marketing Plan looks like in practice

Before starting, clarify:
- **Dependency check:** If the customer experience baseline is unknown — what the current delivery process looks like and whether customers are being wowed or merely served — invoke `customer-experience-systems-design` first, or ask the user to describe their current customer experience level. CLV growth built on a broken experience will produce churners, not loyalists.
- **What does the business sell?** (product, service, or both; average transaction value)
- **Does a customer list exist?** (CRM, spreadsheet, email list — any record of past buyers)
- **When did prices last change?**

---

## Context & Input Gathering

Ask the user for the following if not already provided:

1. **Business type** — What is sold, how, and at what price point?
2. **Current average transaction value** — What does a typical customer spend per visit/purchase?
3. **Purchase frequency** — How often does a typical customer buy? Monthly, annually, once?
4. **Customer list status** — Does a list of past customers exist? How far back does it go?
5. **Last price change** — When were prices last raised, and by how much?
6. **Current upsell/add-on offers** — Is anything offered at the point of purchase beyond the primary item?
7. **Product/service ladder** — Are there multiple price tiers, or a single offering?

---

## Process

### Phase 1: Baseline Current CLV

**Step 1 — Calculate the current CLV estimate.**

Use this formula to establish a baseline:

```
CLV = Average Transaction Value × Average Purchases per Year × Average Customer Lifespan (years)
```

If exact numbers are unavailable, use reasonable estimates and note the assumption. The goal is a directional baseline, not accounting-grade precision.

WHY: You cannot measure improvement without a baseline. Even a rough CLV estimate reveals which lever has the most leverage — a business with high transaction value but low frequency should prioritize frequency; a business with high frequency but low transaction value should prioritize price or upsell.

Record the baseline in the output document.

---

### Phase 2: Audit Each of the 5 Levers

For each lever, assess the current state (Active / Partial / Not in use) and identify the single highest-impact action.

**Step 2 — Lever 1: Raise Prices**

Assess: When were prices last raised? By how much? Is inflation being absorbed silently?

The most overlooked lever. Most business owners assume customers will leave if prices rise. In practice, customers are far less price-sensitive than assumed — especially when they are positioned correctly and receiving genuine value. A price increase drops straight to the bottom line with no additional cost attached. By contrast, every dollar of new-customer revenue carries acquisition cost.

Key implementation guidance:
- Give customers a reason why: quality improvements, input cost increases, or an expansion of what they receive.
- Customers won on price will be lost on price — losing price-sensitive customers during a price rise is often net-positive.
- Grandfathering option: apply the increase only to new customers; tell existing customers they are locked in at the current rate. This reinforces their loyalty and makes them feel valued rather than penalized.

Action: Identify the last price change date and draft a 10–20% increase with a rationale statement.

**Step 3 — Lever 2: Upsell**

Assess: Is anything offered at the moment of purchase beyond the primary item?

Upselling is the bundling of add-ons with the primary product or service at the point of sale. It works because of the contrast principle: after a customer commits to a primary "expensive" purchase, add-ons feel comparatively cheap. A $5 accessory feels trivial next to a $100 main purchase. A customer who has just bought a suit will add shirts, ties, and belts without resistance — the contrast makes them seem reasonably priced.

"Would you like fries with that?" is responsible for hundreds of millions of dollars in McDonald's revenue. It is a single question asked at one moment.

Customers are at peak receptivity immediately after buying — they are in a buying state of mind. Waiting to approach them again later is a missed opportunity.

Framing: "Most customers who bought X also bought Y" — social norm framing taps the human desire to fit in with normal buying behavior.

Action: Identify the top 2–3 add-on candidates that complement the primary offering at high margin. Draft the upsell offer and the moment it will be presented.

**Step 4 — Lever 3: Ascension**

Assess: Does the business have a standard and a premium tier? Is there a product/service ladder?

Ascension is the process of moving existing customers from lower-tier to higher-priced, higher-margin products and services over time. It must be a constant part of the marketing process — not a one-time pitch. Customers stay on existing products due to inertia. When their current option no longer meets their needs, they shop competitors rather than asking you for an upgrade.

Having only a single pricing option leaves enormous revenue on the table. Rule of thumb: approximately 10% of existing customers would pay ten times more; approximately 1% would pay one hundred times more. A single-option business never finds out.

Product ladder example:
- Entry level: self-paced course ($300)
- Standard: group coaching program ($1,500)
- Premium: one-to-one engagement ($5,000)
- Ultra-high-ticket: private intensive or retainer ($25,000+)

Ultra-high-ticket items also activate the contrast principle — standard products appear more reasonably priced by comparison.

Action: Map the current product/service ladder. Identify the missing tier (most commonly: the premium or ultra-high-ticket option). Draft what that tier would offer and at what price.

**Step 5 — Lever 4: Increase Frequency**

Assess: How often do customers return? Is there any systematic mechanism to bring them back?

Two proven tactics:

**Reminders:** Products and services with a natural expiry or renewal cycle (car servicing, dental checkups, ink cartridges, pet vaccinations) can be re-purchased on autopilot if the business sends a timely reminder by email, SMS, or post. Fully automatable. Sending reminders is not pushy if the product genuinely benefits the customer — not sending reminders is a disservice.

**Vouchers / forced return visits:** Issue a voucher at checkout valid only from the following day onward (not redeemable on the day of issue) with an expiry date. This forces a return visit and attaches loss aversion to not returning — the customer will "waste" the voucher if they do not come back. Completely distinct from discounting: the current transaction is not discounted; a future visit is incentivized.

**Subscriptions:** Convert a one-time purchase into a recurring delivery. The Dollar Shave Club model — cheap disposable razor blades converted to a monthly subscription — is the archetype. Subscription turns off the customer's price-shopping radar; when the need is automatically handled, they stop comparison-shopping. Any consumable or regularly-used service is a candidate.

Action: Identify which frequency tactic best fits the business model. For reminder-eligible businesses: define the reminder interval and channel. For transactional businesses: design the voucher mechanic or assess whether a subscription tier is feasible.

**Step 6 — Lever 5: Win Back Lapsed Customers (Reactivation)**

Assess: Does a lapsed customer list exist? When was it last contacted?

Past customers have already crossed the trust chasm between prospect and customer. They are 21 times more likely to buy again than a cold prospect. The list of past buyers is a gold mine — most of the hard work of establishing trust is already done. Reactivation campaigns produce fast cash from a warm audience.

**3-Step Reactivation Procedure:**

1. Pull the lapsed customer list from the CRM or spreadsheet. Define "lapsed" for this business (no purchase in 6 months? 12 months?). Filter out bad-fit customers you do not want back.
2. Create a strong offer: a gift card, coupon, or free offer with a clear call to action. The offer must be compelling enough to overcome inertia.
3. Contact them. Acknowledge the gap — they haven't heard from you in a while. Ask why they haven't returned. If the reason is a business error: apologize and describe the corrective action taken. If they reactivate: follow up after the next purchase to make them feel valued.

Campaign headline options: "We Miss You" / "Have We Done Something Wrong?"

Run reactivation campaigns on a quarterly cadence as a standing item in the marketing calendar.

---

### Phase 3: Prioritize and Sequence

**Step 7 — Identify the highest-leverage lever for this business.**

Score each lever on two dimensions:
- **Impact** (H/M/L): How much could this realistically move CLV given the business model?
- **Effort** (H/M/L): How much work is required to implement the first version?

Prioritize levers with High Impact and Low-to-Medium Effort. For most small businesses: Raise Prices and Reactivation deliver the fastest bottom-line impact with the lowest effort. Upsell and Frequency systems take slightly longer to design but compound over time. Ascension is the highest-ceiling lever but requires building new products.

WHY: Trying to implement all five levers simultaneously produces none of them well. A sequenced 90-day plan with one lever per month is more likely to produce results than a five-lever launch that stalls at week two.

**Step 8 — Draft the 90-day implementation sequence.**

Assign each prioritized lever to a 30-day window. Include:
- Lever name
- Specific tactic to implement
- Who is responsible
- What "done" looks like
- How success will be measured

---

### Phase 4: Draft the CLV Growth Plan Document

**Step 9 — Write clv-growth-plan.md.**

Structure:

```
# CLV Growth Plan — [Business Name]
Generated: [date]

## Baseline
- Average transaction value: $[X]
- Average purchase frequency: [X] per year
- Average customer lifespan: [X] years
- Estimated current CLV: $[X]

## Lever Audit

| Lever | Current State | Priority | First Action |
|-------|--------------|----------|-------------|
| 1. Raise Prices | [Active/Partial/Not in use] | [H/M/L] | [action] |
| 2. Upsell | [Active/Partial/Not in use] | [H/M/L] | [action] |
| 3. Ascension | [Active/Partial/Not in use] | [H/M/L] | [action] |
| 4. Increase Frequency | [Active/Partial/Not in use] | [H/M/L] | [action] |
| 5. Reactivation | [Active/Partial/Not in use] | [H/M/L] | [action] |

## 90-Day Implementation Sequence

### Month 1: [Top-priority lever]
- Tactic: [specific action]
- Owner: [role]
- Done when: [completion signal]
- Measure: [metric]

### Month 2: [Second lever]
...

### Month 3: [Third lever]
...

## Reactivation Campaign
- Lapsed customer definition: no purchase in [X] months
- List size: [X] contacts
- Offer: [gift card / coupon / free offer]
- Headline: ["We Miss You" / "Have We Done Something Wrong?" / custom]
- Contact channel: [email / SMS / post]
- Follow-up: [post-reactivation action]

## CLV Target
- Target CLV after 12 months: $[X]
- Primary driver: [lever]
```

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Business description (product/service, price point) | Yes | Short paragraph if no file exists |
| Average transaction value and purchase frequency | Yes | Estimates acceptable for baseline |
| Customer list or CRM export (lapsed customers) | Yes for reactivation | If absent, note reactivation as deferred |
| Current pricing and last price change date | Yes for Lever 1 | |
| Current product/service ladder | Yes for Lever 3 | Can be inferred from conversation |

---

## Outputs

This skill produces one primary document:

1. **clv-growth-plan.md** — CLV baseline, lever-by-lever audit table, 90-day priority sequence, specific tactics per lever, reactivation campaign template, and 12-month CLV target

---

## Key Principles

**The diamond mine is under your feet.** Most businesses leave their existing customer base largely untapped while spending marketing budget on new acquisition. Past customers have already crossed the trust chasm — they are 21 times more likely to buy again. The existing and lapsed customer base is the richest source of profit available.

**Price increases go straight to the bottom line.** Every dollar of new customer revenue carries acquisition cost. A price increase on existing customers does not. Most customers are less price-sensitive than business owners assume. Holding prices constant while inflation rises is a silent pay cut.

**The contrast principle makes upsells work.** After committing to the primary purchase, add-ons feel cheap by comparison. The moment of purchase is peak buying receptivity — waiting to offer more later is a structural missed opportunity.

**A single price option is money left on the table.** Approximately 10% of customers would pay 10x more; approximately 1% would pay 100x more. Without a premium and ultra-high-ticket tier, the business never discovers who they are.

**Subscriptions turn off the price-shopping radar.** When a recurring need is automatically handled, customers stop comparison-shopping. Convenience has a price — most customers accept it.

**Reactivation is fast cash.** Past customers are a warm audience. A simple three-step campaign — pull list, create offer, make contact — produces results from people who already trust the business.

**Focus on the existing base, not just new acquisition.** Two ways to grow a business: get new customers, or make more from existing and past ones. The second path is higher-margin, faster, and requires no new positioning or advertising spend.

---

## Examples

### Example 1: Shoe Store — Voucher Forcing Return Visits (Lever 4)

A specialty shoe store about an hour's drive from the customer's home issued a voucher worth $30 for every $100 spent at checkout. A $300 purchase produced a $90 voucher. The voucher carried an expiry date approximately six months out, but critically: it was only valid from the day after issue — it could not be redeemed immediately.

The customer came home, told her husband about the voucher, and he was dragged back the next day. They spent $200 more. A new $60 voucher was issued at that checkout. The wife — tired of the drive — nearly pleaded with the cashier not to give it to her. The cashier apologised and said it was store policy.

With one tactic, the store had nearly doubled the initial transaction value and created psychological loss aversion around not returning. The voucher is not a discount — it does not reduce the current transaction. It creates a future asset the customer will "waste" by not returning.

**Application for a service business:** A massage clinic issues a "pre-loaded session credit" voucher valid from the following week with a 90-day expiry. The customer has already paid for the session in their mind — not booking forfeits it.

### Example 2: SaaS Tool — Ascension Ladder (Lever 3)

A solo developer sells a productivity tool at a single flat rate of $29/month. The product is profitable but growth is flat. Applying the ascension lever reveals the missing tiers:

- Solo plan: $29/month (existing)
- Team plan: $99/month — 5 seats + team admin features
- Business plan: $249/month — unlimited seats + priority support + API access
- Agency/white-label: $999/month — client workspaces + custom branding

Within 6 months, 12% of existing customers upgraded to Team, and 2% moved to Business. Monthly recurring revenue increased 38% with no new customer acquisition.

WHY this works: customers on the solo plan had expanded use cases that were not being served. They were not being asked to move up — inertia kept them at the entry tier. The ascension campaign surfaced those customers and gave them a path.

### Example 3: Trades Business — Reactivation Campaign (Lever 5)

A residential plumbing company had 847 customers in their CRM who had not booked in over 18 months. They ran a 3-step reactivation:

1. Pulled the list; filtered out 23 addresses flagged as problematic. Remaining list: 824.
2. Offer: "$50 off any service call booked in the next 30 days."
3. Sent an email with the subject line "Have We Done Something Wrong?" — acknowledged the gap and asked for feedback.

Result: 67 customers booked (8.1% conversion). Average service call value $280. Revenue: ~$18,760 from a single email to a dormant list. Cost: one afternoon of setup and a $50 discount per job. Follow-up email sent to all 67 after the job was completed.

---

## References

- Dib, A. (2016). *The 1-Page Marketing Plan*, Chapter 8: Increasing Customer Lifetime Value (pp. 222–247). Growth levers section: pp. 222–236.
- Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion* — Contrast principle referenced on pp. 228–230 of source text. The contrast principle explains why add-ons feel cheap after the primary purchase and why ultra-high-ticket items make standard products appear reasonably priced.
- Dollar Shave Club subscription model referenced p. 233 as the archetype for converting consumable products into recurring revenue subscriptions.
- Dependency: `customer-experience-systems-design` — CLV growth levers built on a poor customer experience accelerate churn rather than retention. Establish experience baseline before implementing growth campaigns.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-customer-experience-systems-design`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
