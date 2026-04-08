---
name: guarantee-design-and-selection
description: Design, select, and word a risk-reversal guarantee for a product or service offer. Use this skill when the user wants to add a guarantee to an offer, asks "what kind of guarantee should I offer," says prospects are hesitant or objecting to the price or risk, wants to reduce refund fear without killing conversion, asks how to guarantee results, wonders whether to offer a money-back guarantee, wants to switch from a retainer pricing model to a performance model, needs to improve offer conversion rate, asks "what happens if they don't get results," wants to stack multiple guarantees, or is designing a new high-ticket offer and needs a risk-reversal mechanism — even if they don't explicitly mention "guarantee" or "risk reversal." This skill produces a guarantee recommendation with type, wording, and ROI projection. For building the full offer stack see grand-slam-offer-creation. For auditing perceived value before writing the guarantee see value-equation-offer-audit.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/100m-offers/skills/guarantee-design-and-selection
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: 100m-offers
    title: "$100M Offers"
    authors: ["Alex Hormozi"]
    chapters: [15]
tags: [guarantees, risk-reversal, offers, sales, pricing]
depends-on: [value-equation-offer-audit]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: context
      description: "Description of the product or service, current pricing model, target customer, and any known objections"
  tools-required: [Write]
  tools-optional: [Read]
  mcps-required: []
  environment: "Any agent environment"
---

# Guarantee Design and Selection

## When to Use

You are designing or improving an offer and need a guarantee that reverses buyer risk, increases conversion, and protects the business from catastrophic refund exposure. Typical triggers:

- You have an offer but prospects keep hesitating at the risk of not getting results
- You are building a new high-ticket service and need a risk-reversal mechanism
- You want to test whether a stronger guarantee could lift your conversion rate
- You are switching from retainer pricing to a performance or revshare model
- You want to stack multiple guarantees to build an exceptionally compelling offer
- Your current guarantee is weak ("satisfaction guaranteed") and you want to sharpen it

**Preconditions to verify:**
- Is the product or service capable of delivering what it promises? A guarantee on a poor product will backfire into mass refunds.
- Does the user know their approximate current close rate and refund rate? (Needed for ROI math in Step 4)
- Does the user know their fulfillment cost per customer? (Needed for type selection in Step 3)

**This skill does NOT cover:**
- Building the full offer (core deliverable, bonuses, pricing) — use `grand-slam-offer-creation`
- Auditing whether the underlying perceived value is strong enough to sell — use `value-equation-offer-audit`
- Stacking bonuses alongside the guarantee — cross-reference `bonus-stacking-system`

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product or service description:** What is being sold, and what specific outcome does it produce?
  -> Check prompt for: deliverable names, service type, offer description
  -> If missing, ask: "What are you selling and what result does the customer get?"

- **Pricing tier and business model:** Low-ticket B2C product, high-ticket B2B service, coaching program, digital course, agency, SaaS, etc.
  -> Check prompt for: price points, mentions of "retainer," "subscription," "course," "coaching"
  -> If missing, ask: "What is the price and how do customers pay? (one-time, retainer, performance-based)"

- **Fulfillment cost:** Is there significant cost to deliver the service — staff time, ad spend, materials, travel?
  -> If high fulfillment cost: steer toward Conditional or Anti-Guarantee (not Unconditional)
  -> If low fulfillment cost (digital, info product): Unconditional is viable

### Observable Context (gather from environment)

- **Existing offer document or sales page:** Look for a file describing the current offer
  -> If found: read it before recommending a guarantee type
- **Current refund or cancellation data:** Any indication of baseline refund rate
  -> If available: use in ROI projection (Step 4)

### Default Assumptions

- If fulfillment cost is unknown: assume moderate — recommend Conditional as the default safe choice
- If close rate is unknown: use 100 baseline sales for ROI math and note the assumption
- If customer segment is unclear: assume B2C for ticket < $1,000, B2B for ticket > $1,000

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Product/service description is known
- Approximate price point is known
- Fulfillment cost structure is known (high vs low)

PROCEED WITH DEFAULTS when:
- Price and product are known but fulfillment cost is unclear

MUST ASK when:
- Product or service is completely undefined
```

## Process

### Step 1: Understand the Core Guarantee Structure

**ACTION:** Before selecting a type, confirm understanding of what makes a guarantee effective. Every strong guarantee follows this template:

> **"If you do not get [X result] in [Y time period], we will [Z consequence]."**

The Z component — what happens if they fail — is what gives the guarantee power. Without it, you just have a vague claim. Always complete all three parts before moving to type selection.

**Examples of weak vs strong guarantee wording:**

| Weak (incomplete) | Strong (complete) |
|---|---|
| "We guarantee 20 clients." | "You will get 20 clients in your first 30 days, or we give you your money back plus your advertising dollars spent with us." |
| "Satisfaction guaranteed." | "If at any time you don't feel you received $500 in value and service from us, I will write you a check the day you tell me." |
| "Results guaranteed." | "If you don't lose your first 5 pounds in 14 days, we continue your program at no charge until you do." |

**WHY:** The "or we will Z" clause is what triggers the prospect's imagination to picture themselves succeeding. Without a consequence, the guarantee is noise. With it, the prospect mentally simulates the scenario where everything goes well — which is the psychological moment of purchase.

**IF** the user already has guarantee wording that omits the Z clause -> flag this before proceeding. Completing the template alone can lift conversion without changing the guarantee type.

### Step 2: Identify Which of the Four Guarantee Types Applies

**ACTION:** Map the business context to one of the four guarantee types. Read all four descriptions, then score each against the user's situation.

---

#### Type 1: Unconditional Guarantee

**What the customer gets:** A refund with no questions asked and no requirements. They pay, try it, and can get their money back for any reason — full refund, partial refund, or refund plus bonus amount.

**Variants:**
- Full money back ("no questions asked" within X days)
- Partial refund (50%)
- Refund of ancillary costs (ad spend, travel, materials)
- Refund plus competitor's program paid for
- Refund plus additional cash payment ($500, $1,000)
- Named creative guarantee ("Club a Baby Seal Guarantee: after 30 days, if you wouldn't club a baby seal to stay, you don't pay a penny")

**Best for:** Low-ticket consumer products and digital offers where fulfillment cost is low. The more conditions you add to an unconditional guarantee, the weaker it becomes. Works best when you are highly confident in your product and your customers.

**Risk:** You bear full risk of both refund cost AND fulfillment cost. If someone does not achieve results for any reason — including their own lack of effort — you still pay. High consumer-facing volume businesses absorb this well; high-cost-to-deliver services cannot.

**Selection criteria:**
- Ticket price: low to mid (under ~$3,000 for services, any price for digital products)
- Fulfillment cost: low (no significant variable cost per customer)
- Customer behavior: B2C or mass market, where most people won't bother refunding

---

#### Type 2: Conditional Guarantee

**What the customer gets:** A strong outcome guarantee — often better than a money-back — but the customer must satisfy specific conditions (complete key actions that drive success) to qualify.

**Variants:**
- Outsized refund (double or triple money back) if conditions are met
- Service guarantee: you keep working for them free until X is achieved (no time limit)
- Modified service guarantee: you extend service for an additional Y period free of charge
- Credit-based guarantee: refund given as credit toward any service you offer
- Personal service guarantee: you work one-on-one with them free until they reach X (strongest conditional)
- Hotel and airfare guarantee: refund product price plus travel costs if attending an event
- Wage-payment guarantee: pay their hourly rate if they don't find the session valuable
- Release of service guarantee: let them out of their contract with no cancellation fee
- Delayed second payment: don't bill the second installment until they achieve their first outcome
- First outcome guarantee: cover their ancillary costs (ad spend, materials) until they get their first result

**Best for:** High-ticket services, coaching, agencies, and B2B where (1) the customer must take action to succeed, (2) you want to reduce refund risk while still offering a compelling guarantee, and (3) you know the key actions that produce success.

**Key insight:** In the ideal conditional guarantee, 100% of customers qualify for it — because 100% of them followed the conditions — but 100% of them achieved the result and therefore don't want it. This structure also creates better customer outcomes because the conditions ARE the success path.

**Selection criteria:**
- Ticket price: any, but especially high-ticket (> $3,000)
- Fulfillment cost: moderate to high
- Business model: services, coaching, programs, agencies
- You know the key actions that produce results for your customers

**Pro tip (Unconditional vs Conditional by business type):** Bigger, broader guarantees work better with lower-ticket B2C businesses (many people won't bother to claim them). The higher the ticket and the more B2B the context, the more you want specific conditional guarantees. These may or may not include refunds and may or may not have time limits.

---

#### Type 3: Anti-Guarantee

**What the customer gets:** Explicit notice that all sales are final. No refund is possible.

**How to use it:** You must own this position with a compelling "reason why" that the customer can immediately understand and think "Yes, that makes sense." The reason should show your vulnerability — something you expose by working with them that you cannot take back.

**Example framing:** "We are going to show you the proprietary process we use right now to generate leads in our own business — our funnels, ads, and live metrics. Because we're exposing the inner workings of our operation, all sales are final."

**Another example framing:** "If you're the type of customer who needs a guarantee before taking a jump, you are not the type of person we want to work with. We want motivated self-starters who are not looking for a way out before they even begin."

**Best for:** Products or services where value is delivered instantly upon access (code, proprietary data, confidential methodology, information that once seen cannot be unseen). Also works for high-ticket services that require heavy customization, where refunds would mean absorbing full labor cost with nothing to show.

**Selection criteria:**
- Product is consumable or permanently transfers knowledge/access on delivery
- You have a genuine and believable reason why a refund is impossible
- You are targeting serious, committed buyers (anti-guarantee can actually filter out low-quality prospects)

---

#### Type 4: Implied Guarantee (Performance Models)

**What the customer gets:** A pricing structure where you do not get paid unless the customer gets the outcome. No performance, no payment. The guarantee is structural — built into the deal itself.

**Variants:**
- Performance: $X per sale made, $X per pound lost, $X per show
- Revshare: 10–25% of top-line revenue or revenue growth from baseline
- Profit-share: X% of gross or net profit generated
- Ratchets: 10% if over X, 20% if over Y, 30% if over Z (escalating performance fees)
- Bonuses/Triggers: receive X when Y event occurs
- Hybrid floor + performance: "the greater of $1,000/mo or 10% of revenue generated"
- Ramp model: fixed retainer for first 3 months to cover setup, then switch to 100% performance

**What the customer gets:** If you don't perform, they don't pay. If you perform exceptionally, you are very well compensated.

**Best for:** Agencies, consultants, media buyers, and service providers who generate quantifiable outcomes (revenue, leads, weight lost, deals closed). Requires outcome transparency — both parties must be able to measure the result and trust the tracking.

**Why it is powerful:** Creates perfect incentive alignment. You are accountable to results. Low performers are naturally weeded out. The agency/consultant case study (CS-12): agencies switching from retainer models to performance models have gone from $20k/month to $200k+/month in a matter of months because the client has no reason to say no — the risk is entirely on the service provider.

**Selection criteria:**
- Outcome is quantifiable (revenue, leads, conversions, measurable physical result)
- You have a transparent measurement mechanism both parties trust
- You are confident in your ability to deliver — this model rewards the best performers most

---

### Step 3: Select the Best Guarantee Type

**ACTION:** Use this decision framework to pick the type (or combination) that fits:

```
START HERE:
Is your fulfillment cost HIGH (significant labor, ad spend, materials per customer)?
  YES -> Conditional, Anti-Guarantee, or Implied/Performance. NOT Unconditional.
  NO  -> Any type is viable. Start with Unconditional or Conditional.

Is the outcome quantifiable and trackable?
  YES -> Implied/Performance is worth serious consideration.
  NO  -> Conditional or Unconditional.

Is the product delivered upon access (knowledge, code, methodology)?
  YES -> Anti-Guarantee with compelling reason why.
  NO  -> Continue.

Is this high-ticket B2B (> $3,000 and business buyer)?
  YES -> Conditional with specific conditions tied to success behaviors.
  NO (low-ticket consumer) -> Unconditional or named creative guarantee.

Do you want maximum conversion and are confident in delivery?
  YES -> Unconditional (or stacked: unconditional short-window + conditional long-window).
  UNCERTAIN -> Conditional with conditions that mirror the success path.
```

**Pro tip on naming:** Give your guarantee a compelling name. Avoid "satisfaction guarantee" or "money-back guarantee." Use vivid, specific language. Example: instead of "30 Day Money Back Satisfaction Guarantee," use "In 30 days, if you wouldn't jump into shark-infested waters to get our product back, we'll return every dollar you paid."

### Step 4: Run the ROI Math

**ACTION:** Calculate whether the stronger guarantee is financially worth it. Do not skip this step — the math is what separates emotion from business logic.

**The formula:**

```
Net Sales (baseline)    = Total Sales × (1 - Refund Rate)
Net Sales (with guarantee) = New Total Sales × (1 - New Refund Rate)
ROI Multiple            = Net Sales (with guarantee) ÷ Net Sales (baseline)
```

**Working example from the source material:**

```
Baseline:          100 sales × (1 - 5% refund) = 95 net sales
With guarantee:    130 sales × (1 - 10% refund) = 117 net sales
ROI multiple:      117 ÷ 95 = 1.23x (23% net revenue increase)
```

The conversion lifted 30% and the refund rate doubled — yet net revenue still grew 23%.

**Rule of thumb:** For a stronger guarantee to NOT be worth it, the increase in refund rate would have to completely offset every additional sale. A 5% absolute increase in sales would need to be completely wiped out by a 5% absolute increase in refunds (which would be an implausible doubling of refunds). In practice, the stronger guarantee almost always wins on net.

**For high-cost fulfillment services:** Adjust the formula to include fulfillment cost:

```
Net Revenue (baseline)       = (Sales × Price) - (Sales × Fulfillment Cost) - (Refunds × Price)
Net Revenue (with guarantee) = (New Sales × Price) - (New Sales × Fulfillment Cost) - (New Refunds × Price + Guarantee Cost)
```

**ACTION:** Plug in the user's numbers. If current close rate and refund rate are unknown, use these conservative defaults: 100 baseline sales, 5% baseline refund rate, 20% conversion lift from guarantee, refund rate doubles. Present the calculation explicitly so the user can adjust assumptions.

### Step 5: Consider Stacking

**ACTION:** Evaluate whether the offer would benefit from stacking two guarantees.

Stacking means layering guarantees for different time windows or different conditions. Examples:

- **Unconditional short + Conditional long:** "No questions asked, full refund within 30 days. OR: complete all modules and implement the framework within 90 days and don't double your leads — we'll give you triple your money back."
- **Two conditional outcomes sequenced:** "You'll generate $10,000 by day 60, and $30,000 by day 90, as long as you complete steps 1, 2, and 3."
- **Implied + Conditional hybrid:** Fixed base fee for setup month, then 100% performance after that.

**WHY stacking works:** Multiple guarantees future-pace the prospect through a timeline of outcomes. It makes the seller appear deeply convinced the customer will succeed. It shifts risk further from buyer to seller at each stage, which increases the perceived "unfairness" of not buying.

**When to stack:** When a single guarantee feels insufficient for the price point, or when the sales conversation reveals the prospect has multiple distinct fears (immediate risk AND long-term outcome risk).

### Step 6: Write the Final Guarantee

**ACTION:** Produce the complete guarantee recommendation with these components:

1. **Type selected** and rationale (1-2 sentences)
2. **Wording** — complete "If you do not get X in Y, we will Z" sentence
3. **Name** — a compelling, memorable name for the guarantee
4. **Conditions** (if Conditional) — specific customer actions required to qualify
5. **ROI projection** — calculated using Step 4 formula with stated assumptions
6. **Delivery script** — a 2-3 sentence way to present the guarantee during the sales conversation

## Examples

**Scenario A: Online fitness coaching program, $497, B2C**

Context: 100 current sales/month, 4% refund rate, digital delivery, low fulfillment cost.

Process: Low ticket, B2C, low fulfillment cost. Unconditional viable. ROI check: baseline 100 × 96% = 96 net sales. With guarantee: projected 135 × 8% = 124.2 net sales. Multiple = 1.29x (29% net revenue gain). Stack: unconditional 30-day + conditional 90-day for those who follow the program.

Output:
- **Type:** Stacked (Unconditional 30-day + Conditional 90-day)
- **Name:** "The No-Excuse Guarantee"
- **Wording:** "Try the program for 30 days, no questions asked — if it's not for you, you pay nothing. OR: follow the program exactly as outlined for 90 days. If you don't lose at least 12 pounds, I will refund every dollar AND pay for your next program."
- **ROI:** 96 baseline net sales → ~124 projected net sales = 1.29x improvement (assumes 35% conversion lift, refund rate doubling)

---

**Scenario B: Marketing agency, $10,000/month retainer, B2B**

Context: Agency currently on retainer model. Clients often hesitate due to "what if it doesn't work." High fulfillment cost (staff time).

Process: High ticket B2B, high fulfillment cost. Unconditional too risky. Performance/Implied model ideal because outcomes (leads, revenue) are trackable. This is the CS-12 case study scenario.

Output:
- **Type:** Implied/Performance (retainer-to-performance transition)
- **Name:** "We Only Win When You Win"
- **Wording:** "We charge $1,000/month for the first 3 months to cover setup. After that, we take 15% of the revenue we generate for you — nothing if we generate nothing."
- **Transition pitch:** "We've helped agencies like ours go from $20k/month to $200k+/month by making this switch. The reason clients agree immediately is simple: if we don't perform, they owe us nothing."
- **ROI:** Baseline at $10k/mo flat. If agency generates $100k/mo in results: performance fee = $15k/mo, a 50% revenue increase, with zero client objection to the price.

---

**Scenario C: Business consultant selling proprietary methodology, $25,000 one-time**

Context: Methodology includes confidential internal playbook and live financial models from the consultant's own business.

Process: High ticket, knowledge instantly transferred on delivery, consultant has genuine "reason why" for no refunds. Anti-Guarantee is appropriate and actually strengthens perceived exclusivity.

Output:
- **Type:** Anti-Guarantee
- **Name:** "All Access, All Final"
- **Wording:** "This engagement gives you full access to the live playbooks, ad accounts, and financial models from our own operating businesses. Because you're seeing exactly how we run our company, all sales are final — we can't un-show you what you've seen."
- **Delivery script:** "I want to be upfront about one thing: this is all-sales-final. The reason is that within the first session, you'll have access to our actual numbers, our actual funnels, and our proprietary frameworks. Once you have that, you have it. That's also why this works."

## Key Principles

- **Risk reversal is the single greatest objection handler** — The number one reason people don't buy is fear that the product won't do what it says. A guarantee directly addresses that fear. Changing the quality of a guarantee alone can lift conversions 2–4x.

- **Always say the guarantee boldly — even if you don't have one** — State your position clearly and give the reason why. Vague, hedged guarantee language performs worse than an explicit anti-guarantee with a strong rationale.

- **Guarantees are enhancers, not foundations** — A guarantee on a poor product or weak sales process will accelerate refunds, not conversions. Confirm the offer delivers real results before strengthening the guarantee.

- **The "or what" clause is what gives a guarantee teeth** — Without a specified consequence, a guarantee is just a claim. "We guarantee results" is meaningless. "If you don't get results in 30 days, we refund you in full plus pay for a competitor's program" is a guarantee.

- **The stronger the guarantee, the higher the net increase in purchases — even if refunds increase** — Do the math. A guarantee that doubles your refund rate but lifts sales by 30% still wins by 23% on net. Don't be afraid of the refund number in isolation.

- **Conditions should mirror the success path** — The best conditional guarantee has conditions that are the exact actions a customer must take to succeed. In a perfect world, 100% qualify and 100% achieve the result — meaning nobody claims it. This also improves customer outcomes.

- **AP-7 Warning — Wrong-customer magnet:** Guarantees can attract the wrong type of customer. A person who buys primarily because of the guarantee — not because they want the outcome — is likely uncommitted to doing the work. This leads to: high refund rates, difficult customer relationships, poor case studies, and burnout. Use conditional guarantees to filter for customers willing to act. Use anti-guarantees for high-commitment, self-selecting audiences. Never use a strong unconditional guarantee to prop up a weak product or to compensate for poor targeting.

## References

- For building the full offer before designing the guarantee: `grand-slam-offer-creation`
- For auditing perceived value and the value equation (Dream Outcome × Perceived Likelihood ÷ Time Delay × Effort): `value-equation-offer-audit`
- For stacking bonuses alongside the guarantee to complete the offer: `bonus-stacking-system`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — $100M Offers by Alex Hormozi.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-value-equation-offer-audit`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
