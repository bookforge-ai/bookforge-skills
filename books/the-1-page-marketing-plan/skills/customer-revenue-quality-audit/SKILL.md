---
name: customer-revenue-quality-audit
description: Classify every customer into one of four archetypes — Tribe, Churners, Vampires, or Snow Leopards — score your customer base using Net Promoter Score (NPS), and produce a segmentation report with a concrete fire/grow decision per customer. Use this skill when you want to run a customer audit, audit customer quality, segment customers, identify bad customers, identify draining customers, fire bad customers, clean up polluted revenue, distinguish Tribe from Churners from Vampires from Snow Leopards, classify customers by loyalty, assess NPS score, improve customer loyalty, remove toxic clients, free up team capacity, identify which customers to grow vs which to cut, run a customer quality review, calculate whether you have concentration risk from a single large customer, answer "should I fire this customer", identify your worst customers, stop subsidizing customers who cost more than they generate, or eliminate revenue that is actively making your business sick.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/customer-revenue-quality-audit
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan: Get New Customers, Make More Money, and Stand Out from the Crowd"
    authors: ["Allan Dib"]
    chapters: [8]
tags: [customer-management, segmentation, nps, retention, small-business]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Customer list or description — who your current customers are, how much they pay, how demanding they are, and any known complaints or referrals"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document set. Typical files: customer-list.md or customer-list.csv, support-log.md, revenue-report.md. If no files exist, gather information through conversation."
---

# Customer Revenue Quality Audit

## When to Use

You are a business owner who suspects that not all revenue is equal. Typical triggers:

- Certain customers consume far more staff time than others while paying the same
- You feel drained after dealing with a particular client even though they pay on time
- Your team morale is suffering due to one or two demanding accounts
- You acquired customers through heavy discounting and they are now price-sensitive and disloyal
- One customer makes up a disproportionately large share of total revenue and you worry about losing them
- You are running "eat what you kill" mode and accepting any revenue without evaluating its quality
- A customer complains constantly despite receiving the same service others are happy with
- You want to grow high-value relationships but cannot because problem customers consume all available capacity

Before starting, clarify:
- **Do you have a customer list?** Any format works — spreadsheet, CRM export, a written list.
- **Can you estimate revenue per customer?** Even rough brackets (high/medium/low) are sufficient.
- **Do you have a sense of which customers cause the most friction?** This is the key input for archetype classification.

---

## Context & Input Gathering

Ask the user for the following if not already provided:

1. **Customer inventory** — Name or category of each current customer/account.
2. **Revenue contribution** — Approximate monthly or annual revenue per customer.
3. **Demand level** — How many support requests, calls, or escalations does each customer generate?
4. **Payment behavior** — Do they pay on time, or require constant chasing?
5. **Referral behavior** — Have they referred anyone? Do they speak positively about the business?
6. **Team impact** — Do they deal respectfully with staff, or do they escalate to the owner and cause team stress?
7. **Acquisition method** — Were they acquired through normal marketing, or via heavy discounting or overpromising?

---

## Process

### Phase 1: Archetype Classification

**Step 1 — Apply the four-archetype taxonomy to each customer.**

Every customer in your business falls into one of four categories. Map each customer against the definitions below:

| Archetype | Who They Are | Behavioral Signals | Decision |
|-----------|-------------|-------------------|----------|
| **Tribe** | Raving fans who are actively conspiring for your success | Pay on time, refer others unprompted, respect your team, accept your pricing, treat you as a valued partner | GROW |
| **Churners** | Customers you acquired through overhyping, discounts, or poor fit | Price-sensitive, complain frequently, churn out when the novelty wears off, damage your reputation in the market | FIRE |
| **Vampires** | Customers who can afford you but consume disproportionate resources | Demand access to the owner, terrorize your team, consume 5x average support time while paying average rates, drain morale | FIRE FAST |
| **Snow Leopards** | One large customer who makes up an outsized revenue share | Fun to work with, pay well, but represent concentration risk — rare and almost impossible to replicate | MANAGE (do not build strategy around replicating them) |

WHY: Not all revenue dollars are equal. A dollar from a Churner comes with support costs, churn risk, brand damage, and team morale erosion attached to it. A dollar from a Tribe member comes with referrals, goodwill, and compounding lifetime value attached to it. Treating them the same is what Dib calls "polluted revenue" — revenue that makes your business sick rather than healthy.

**Step 2 — Classify every customer.**

For each customer on your list, assign one archetype. Where ambiguous, use this decision tree:

```
Does this customer consume significantly more time/energy than average?
  YES → Are they pleasant and respectful?
          YES → Snow Leopard (large + nice but probably outsized revenue share)
          NO  → Vampire (affordable but consuming; fire fast)
  NO  → Do they refer others and pay on time?
          YES → Tribe (grow these)
          NO  → Churner (acquired via bad fit; fire)
```

Document each classification in the segmentation table (see Outputs).

---

### Phase 2: NPS Scoring

**Step 3 — Send the NPS survey to all active customers.**

The Net Promoter Score is a formal measurement of customer loyalty. Send every customer a two-question survey:

**Primary question (scored 0–10):**
> "How likely is it that you would recommend our company/product/service to a friend or colleague?"

**Follow-up open-ended question:**
> "What is the main reason for your score?"

Record each response. The open-ended reason is critical — it tells you *why* a customer is a Promoter or Detractor, which informs both firing decisions and Tribe growth strategy.

WHY: The NPS survey gives you a defensible, quantified basis for decisions that might otherwise feel personal or arbitrary. It also surfaces issues you did not know existed from customers who were quietly unhappy but never complained — they simply stopped buying.

**Step 4 — Apply NPS thresholds to segment customers.**

| NPS Score | Label | Archetype Mapping |
|-----------|-------|------------------|
| 9–10 | Promoter | Tribe |
| 7–8 | Passive | Potential Snow Leopard zone; monitor |
| 0–6 | Detractor | Churner or Vampire; prioritize for review |

WHY: The thresholds are not arbitrary. Passives (7–8) are satisfied but not loyal — they will switch providers if given a better offer. Only Promoters (9–10) actively recruit new customers for you. Detractors (0–6) are actively damaging your reputation in the market even if they remain paying customers.

**Step 5 — Calculate your NPS.**

```
NPS = % of Promoters − % of Detractors

Range: −100 (all detractors) to +100 (all promoters)
Benchmark: >0 = good; ≥50 = excellent
```

Example: 60% Promoters, 10% Detractors, 30% Passives → NPS = 60 − 10 = **+50** (excellent)

Record this number. It is your revenue quality baseline. Repeat the NPS survey quarterly to track whether firing Detractors and investing in Tribe members is improving the score over time.

---

### Phase 3: Revenue Quality Analysis

**Step 6 — Estimate true profitability per customer.**

For each Detractor/Churner/Vampire customer, calculate a rough adjusted profit:

```
Adjusted Profit = Revenue − (Direct Costs + Time Cost + Morale Cost)

Time Cost = (Hours per month spent on this customer) × (Owner/staff hourly rate)
Morale Cost = qualitative flag (Low / Medium / High)
```

WHY: Most business owners track gross revenue per customer but ignore the time cost of managing them. A customer paying $3,000/month who requires 20 hours of escalations per month at an effective rate of $200/hour is generating $3,000 − $4,000 = **net loss** before other costs. Running an honest profit and loss per customer is often the moment a business owner realizes they have been subsidizing problem customers.

**Step 7 — Flag Snow Leopard concentration risk.**

If any single customer represents more than 20–25% of total revenue, flag them as a Snow Leopard. Document:
- Their revenue as a percentage of total
- What would happen to the business if they left tomorrow
- The dependency risk this creates

WHY: Snow Leopards are wonderful customers — they are often pleasant, pay well, and are fun to work with. The risk is not in the relationship; it is in the strategy error of treating them as a template for growth. They are exquisite and rare, like the actual animal. Chasing more Snow Leopards is a bad growth strategy. Instead, invest in replicating the Tribe.

---

### Phase 4: Decisions and Actions

**Step 8 — Apply firing rules and produce the action plan.**

For each customer, assign one of four actions:

| Action | Applies To | What It Means |
|--------|-----------|--------------|
| **GROW** | Tribe members | Invest in deepening the relationship — referral programs, exclusive access, appreciation outreach, loyalty rewards |
| **MONITOR** | Passives + Snow Leopards | No immediate action; survey again next quarter; for Snow Leopards, diversify revenue exposure |
| **FIRE (scheduled)** | Churners | Give appropriate notice; refer them elsewhere professionally; do not renew |
| **FIRE (urgent)** | Vampires | Move quickly — every day they remain costs morale and capacity; use the firing script below |

WHY: Firing is not abandonment — it is capacity creation. When you remove a Vampire or Churner from your customer base, you free the time and energy that was being consumed to serve your Tribe better. This creates scarcity (you are selective about who you work with), which increases your perceived value in the market and allows you to attract more Tribe-type customers. Firing problem customers and referring them to competitors is the most elegant strategy available: you solve your problem while gifting competitors with it.

**Step 9 — Write the firing conversation script for each customer being fired.**

Use the template below. Adjust the reason for each customer (Churner vs Vampire may require different framing):

```
CUSTOMER FIRING SCRIPT — [Customer Name]
Date: [date]
Method: [email / phone call / in-person meeting]

---

Opening (acknowledge the relationship):
"[Customer name], I want to thank you for your business over the past [time period].
We have genuinely valued the relationship."

Reason (clear but non-accusatory):
"After reviewing our current capacity and focus, we have made the decision to work
exclusively with [describe your ideal customer type — e.g., 'clients in the enterprise
segment / clients who have been with us for more than 12 months / clients whose projects
align with our core specialty'].

This means we will not be able to continue serving [their company] beyond [date]."

Transition (professional referral):
"We want to make sure you are well taken care of. We recommend [competitor or alternative
provider] as a strong fit for your needs. I am happy to make an introduction if that
would be helpful."

Close (firm and warm):
"Thank you again for the time we have worked together. I wish you and your team every
success."

---
Note: Do NOT negotiate. Do NOT offer a discount to stay. A customer won on price will
be lost on price. The decision is final.
```

WHY: A professional, gracious exit protects your reputation. Fired customers talk. A gracious exit turns a Churner into a neutral — they cannot reasonably complain. A botched firing turns a Churner into an active Detractor who damages your brand in the market.

**Step 10 — Build the Tribe growth plan.**

For each Tribe member identified, document at least one growth action:

| Tribe Member | Current Revenue | Referral Potential | Next Growth Action |
|-------------|----------------|-------------------|-------------------|
| [Name] | [amount] | [High/Med] | [e.g., invite to referral program, offer exclusive early access, send handwritten thank-you, provide additional service bundle] |

WHY: Your Tribe members keep the lights on and promote your business for free. They are the customers who will survive you focusing on firing problem customers — and they are the ones who will notice when you have more time and attention to give them.

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Customer list with names/accounts | Yes | Spreadsheet, CRM export, or written list |
| Revenue per customer (approximate) | Yes | Even rough brackets work |
| Support/demand level per customer | Yes | Can be estimated if not logged |
| NPS survey results | Recommended | Can be run as part of this skill; requires email access to customers |
| Payment history | Optional | Strengthens Churner classification |

---

## Outputs

This skill produces four documents:

1. **customer-segmentation-report.md** — Full table of all customers with archetype, NPS score, estimated true profit, and action (GROW / MONITOR / FIRE scheduled / FIRE urgent)
2. **firing-scripts/[customer-name]-firing-script.md** — One firing script per customer being exited
3. **tribe-growth-plan.md** — Action plan for each Tribe member with specific next steps
4. **nps-baseline.md** — NPS calculation, Promoter/Passive/Detractor breakdown, and quarterly review schedule

---

### Output Template: Customer Segmentation Report

```markdown
# Customer Segmentation Report
Date: [date]
Business: [business name]
Total active customers: [N]
NPS baseline: [score]

## Segmentation Table

| Customer | Revenue/mo | Archetype | NPS Score | True Profit Est. | Action |
|----------|-----------|-----------|-----------|-----------------|--------|
| [Name]   | $[X]      | Tribe     | 10        | Positive        | GROW   |
| [Name]   | $[X]      | Vampire   | 2         | Net loss        | FIRE (urgent) |
| [Name]   | $[X]      | Churner   | 4         | Marginal        | FIRE (scheduled) |
| [Name]   | $[X]      | Snow Leopard | 8     | Positive but concentrated | MONITOR |

## Revenue Quality Summary
- Tribe revenue: $[X] ([X]% of total)
- Polluted revenue (Churners + Vampires): $[X] ([X]% of total)
- Snow Leopard concentration: $[X] ([X]% of total)
- Adjusted NPS after planned exits: [projected score]

## Actions This Quarter
1. Fire [N] Vampires by [date]
2. Fire [N] Churners by [date]
3. Grow [N] Tribe members with [specific action]
4. Re-survey all Passives in [month]
```

---

## Key Principles

**Not all revenue is equal.** A dollar from a Tribe member and a dollar from a Vampire look identical on a revenue report. They are not. The Vampire dollar comes with hidden costs: staff time, morale erosion, owner distraction, and opportunity cost. Track revenue quality, not just revenue volume.

**A customer won on price will be lost on price.** Churners are almost always acquired through discounting or overpromising. They never become Tribe members. The acquisition method predicts the customer type.

**Firing creates scarcity, and scarcity creates value.** When you fire problem customers and become selective about who you work with, the market perceives you as premium. Selectivity is a positioning signal.

**The right customer is always right.** The cliché "the customer is always right" is dangerous when applied to Vampires and Churners. Reframe it: the *right* customer is always right. Problem customers are not always right — they are always wrong for your business.

**Genuine complaints are different from problem customers.** A customer who raises a legitimate service failure is a valuable intelligence asset — they reveal a gap others experienced silently. Do not confuse a customer with a real grievance (fix them) with a Vampire or Churner (exit them).

**Give the squeaky wheel's oil to the quiet good customer.** Low-value, price-sensitive customers complain the most and demand the most attention. High-value Tribe customers are often silent — they are getting good service and do not need to escalate. Firing problem customers redirects time and energy to the customers who actually deserve it.

---

## Examples

### Example 1: Accounting Firm Fires a Vampire

A small accounting firm had one client — a medium-sized retailer — who paid $4,500/month. However, the client's owner called the firm's principal directly at least twice a week, demanded same-day turnarounds, questioned every bill, and once yelled at a junior accountant. NPS score: 3.

True profit calculation:
- Revenue: $4,500/month
- Direct service cost: $1,200/month
- Time cost: 18 hours/month × $220/hr effective rate = $3,960
- **Adjusted profit: $4,500 − $1,200 − $3,960 = −$660/month (net loss)**

The firm sent the firing script (email, 2 weeks notice, competitor referral included). The next month, the principal reclaimed 18 hours, used them to onboard two new Tribe-type clients at $2,500/month each with minimal ongoing support needs. Net monthly improvement: +$5,160.

### Example 2: E-Commerce Brand Identifies Churners Through Acquisition Audit

An e-commerce brand ran a 50%-off launch promotion to acquire their first 200 customers. Twelve months later, 80% of those customers had never reordered. NPS survey results for the promo cohort: average score of 5.2 (Detractor territory). NPS for customers acquired at full price: 8.6 (Passive/Promoter territory).

Decision: Stop discounting. Segment the promo cohort as Churners. Run a reactivation email sequence — customers who respond with a purchase move to Monitor; those who do not are removed from active marketing budget. This freed 30% of the email marketing budget previously wasted on a Churner cohort.

Lesson: The acquisition method predicted the customer quality. Discounting to acquire customers is a Churner factory.

### Example 3: Consulting Practice Manages a Snow Leopard

A strategy consultant had one client — a large financial services firm — that represented 65% of annual revenue. The client was pleasant, paid promptly, and gave positive feedback (NPS: 9). The consultant loved working with them.

The Snow Leopard risk: if that client's internal champion left the firm or the budget was cut, the consultant's practice would face a 65% revenue cliff overnight.

Decision: Do not fire. Do not over-invest in chasing similar clients (they are rare). Instead: cap hours devoted to this account, diversify by actively marketing to new clients, and set a target of reducing this client's revenue share to below 35% within 18 months — without reducing the relationship quality.

Lesson: Snow Leopards are not problems to solve — they are risks to manage. The risk is strategic concentration, not the client themselves.

---

## References

- Dib, A. (2016). *The 1-Page Marketing Plan*, Chapter 8: Increasing Customer Lifetime Value — "Polluted Revenue and the Unequal Dollar" (pp. 242–247) and "Fire Problem Customers" (pp. 243–247).
- Net Promoter Score methodology: Reichheld, F. (2003). "The One Number You Need to Grow." *Harvard Business Review*. The NPS survey question and scoring thresholds (9–10 Promoters, 7–8 Passives, 0–6 Detractors) are the standard implementation.
- The four-archetype taxonomy (Tribe, Churners, Vampires, Snow Leopards) is Dib's original framework from the book. The "polluted revenue" and "unequal dollar" concepts are core to Chapter 8.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

No direct dependencies. Install the full book set from GitHub.

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
