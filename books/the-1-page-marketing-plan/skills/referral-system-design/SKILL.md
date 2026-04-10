---
name: referral-system-design
description: Design an active referral system for a small business. Use this skill when you want to get more referrals, build a referral system, stop relying on word of mouth, ask for referrals without seeming desperate, write a referral script, create a gift card referral mechanism, apply the bystander effect override to referral asks, set upfront referral expectations with new customers, find joint venture referral partners, write a JV referral outreach email, profile complementary business partners for lead exchange, fill square 9 of the 1-Page Marketing Plan, apply the law of 250, design an orchestrated referral ask cadence, or turn customer satisfaction into a systematic lead source.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/referral-system-design
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan: Get New Customers, Make More Money, and Stand Out from the Crowd"
    authors: ["Allan Dib"]
    chapters: [9]
tags: [marketing, referrals, joint-ventures, word-of-mouth, small-business]
depends-on: ["customer-experience-systems-design"]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Business description — what the business sells, who the ideal customer is, and a rough sense of customer satisfaction level"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document set. Typical files: business-description.md, customer-list.md or CRM export (optional), referral-system.md (to be created)."
---

# Referral System Design

## When to Use

You are a small business owner who wants referrals to be a deliberate, reliable lead source — not an occasional windfall you hope for. Typical triggers:

- You get some referrals but they happen randomly; you have no system driving them
- You feel awkward asking for referrals, as if it makes you seem needy or desperate
- You have satisfied customers who never refer — because no one asked them to
- You attend networking events and ask for "anyone who needs X" without getting results
- You want to set up a joint venture with a complementary business to generate warm leads
- You want to fill square 9 of your 1-Page Marketing Plan canvas

**Dependency check:** This skill assumes customers are genuinely satisfied. If customer experience baseline is unknown, invoke `customer-experience-systems-design` first, or verify that delivered results are strong before running referral scripts. A referral system built on a poor experience accelerates negative word of mouth, not positive.

Before starting, clarify:
- **What is the business?** (product/service, industry, approximate customer base size)
- **What is the typical lifetime value of a customer?** (needed to size gift card and JV incentives)
- **Are there complementary businesses the owner already has relationships with?** (head start for JV partner identification)
- **Is there a current referral practice?** (Audit starting point)

---

## Context & Input Gathering

Ask the user for the following if not already provided:

1. **Business description** — What does the business sell, and to whom?
2. **Satisfaction signal** — Are customers currently happy? Any testimonials, repeat business, or positive feedback?
3. **Customer lifetime value** — Rough estimate. This determines how much to invest in a gift card or JV voucher.
4. **Existing referral practice** — Do you ask for referrals now? How? What happens?
5. **Complementary businesses** — Name any businesses that serve your ideal customer before or after you do.

---

## Process

### Phase 1: Referral Practice Audit

**Step 1 — Classify current referral behavior.**

Determine which pattern describes the current state:

| Pattern | Description | Risk Level |
|---------|-------------|-----------|
| **Passive hope** | Do great work, hope referrals come. No ask, no system. | High — single uncontrollable source |
| **Vague ask** | Sometimes mention "if you know anyone..." to happy customers. No gift, no specifics. | Medium — triggers bystander effect |
| **Active ask, no system** | Ask directly but inconsistently, no cadence, no gift card, no upfront expectation. | Medium — sporadic results |
| **Active system** | Upfront expectation-setting + post-delivery ask + gift card + JV partners + ask cadence. | Low — reliable lead flow |

WHY: Most small businesses are in "passive hope." The goal of this phase is to name the gap honestly before writing scripts. A business that never asks cannot improve its referral rate by changing its ask wording — it must first commit to asking.

---

### Phase 2: Write the Upfront Expectation-Setting Script

**Step 2 — Craft the expectation-setting script for the start of each new customer engagement.**

Use this template, adapted to the business:

> *"[Customer name], I'm going to do an awesome job for you, but I need your help also. Most of our new business comes through referrals. This means that rather than paying for advertising to get new clients, we pass the cost savings directly to you. We typically get about three referrals from each new customer. When we're finished working together and you're 100% satisfied with the work we've done, I'd really appreciate it if you could keep in mind three or more other people who we could also help."*

Four elements this script delivers:
1. **Promise of result** — "I'm going to do an awesome job for you" — power stays with the customer; the referral is conditional on your performance
2. **Their benefit** — referral model = cost savings passed directly to them
3. **Specific number** — "three or more" plants a number without pressure; the customer begins thinking ahead
4. **Future-oriented** — delivered at the START, when the relationship is fresh and expectations are high

WHY: Setting the referral expectation upfront is far more effective than a surprise ask at the end. The customer has the entire engagement to mentally prepare a short list. It also reframes referrals as the normal operating model of the business — not as begging.

---

### Phase 3: Write the Post-Delivery Direct Ask Script with Gift Card

**Step 3 — Craft the post-delivery direct ask.**

Use this template:

> *"[Customer name], it's been such a pleasure working with you. If you know anyone who's in a similar situation to yourself, we'd love you to give them one of these gift cards which entitles them to $[amount] off their first [consultation/purchase/session] with us. One of the reasons we're able to keep the cost of our service down is because we get a lot of our business through referrals from people like you."*

Three elements this script delivers:
1. **Acknowledgment** — opens by recognizing the customer; people love being acknowledged
2. **Gift, not favor** — you are not asking the customer for something; you are giving them something valuable (a gift card) to pass on to a friend
3. **Reason why** — explaining the referral-based business model makes the ask feel principled, not transactional

**Gift card sizing:** The face value should feel meaningful to the recipient (your prospect) while being affordable relative to your customer lifetime value. If a new customer is worth $5,000 in lifetime revenue, a $100 gift card is a 2% acquisition cost — far cheaper than advertising.

WHY: Framing the ask as offering a gift to the referrer's friend removes the psychological barrier of "begging for a favor." The referrer becomes a value-provider to their network, not a sales agent for your business. This taps the real psychology of referrals: people share because it makes them look and feel good — not as a favor to you.

---

### Phase 4: Apply the Bystander-Effect Override Formula

**Step 4 — Make asks specific, not general.**

Never use: *"If you know anyone who needs [service], please send them my way."*

"Anyone" is "somebody else." Everyone assumes someone else will refer. This is the bystander effect: in a crowd emergency, when everyone assumes someone else will act, no one acts. The same diffusion of responsibility kills generic referral asks.

The fix: be specific. For a referral to occur in a conversation between two people, three things must happen:
1. The referrer notices the conversation is relevant to what you do
2. They think of YOU specifically
3. They introduce you into the conversation

**Formula for a specific ask:**

Instead of "anyone who needs X" → name a specific type of person AND a specific trigger situation.

| Generic (bystander-effect) | Specific (bystander-effect override) |
|---------------------------|-------------------------------------|
| "Anyone who needs a financial planner" | "Someone nearing retirement age who's recently been made redundant" |
| "Anyone who needs a pet food recommendation" | "A new dog owner your vet just prescribed XYZ food for" |
| "Anyone who needs a lawyer" | "A friend who's just started a business and hasn't set up their contracts yet" |

WHY: A specific person + specific trigger creates personal responsibility in the referrer. They think: "Actually, my colleague John just got made redundant last month — this is exactly for him." The abstract "anyone" never triggers that mental shortcut.

---

### Phase 5: Build the JV Partner Profile

**Step 5 — Identify joint venture referral partner types.**

Ask: who serves your ideal customer BEFORE or AFTER they come to you? Those are your JV candidates.

Examples:
- Lawyer → Accountant (same client, different need, non-competing)
- Car detailer → Mechanic (sequential relationship with the same car owner)
- Pet food retailer → Veterinarian (the vet prescribes what the retailer sells)
- Financial planner → Real estate agent (both serve clients with major financial transitions)

**Step 6 — Build a referral profile for each JV partner type.**

For each partner type, answer the five profiling questions:

| Question | What to Determine |
|----------|------------------|
| **Who do they know?** | What types of prospects are in their client or contact base? |
| **What trigger event makes referral timely?** | What happens in the prospect's life that makes your service relevant RIGHT NOW? |
| **What specific problem does the prospect have?** | Not "needs a [professional]" — name the exact problem (redundancy, new puppy, just signed a lease) |
| **How does the referrer look good by referring?** | What value does the referrer provide their client by passing your asset on? |
| **What asset can you give the referrer to pass on?** | A gift card, a lead magnet, a special report, a voucher — something with tangible value |

WHY: A cold request to a JV partner ("send me your clients") fails for the same reason a generic referral ask fails. The partner has no personal responsibility and no tool. A profiled approach gives the partner a specific trigger to watch for and a specific asset to offer — making them a value-provider to their clients, not a salesperson for you.

---

### Phase 6: Write the JV Outreach Email

**Step 7 — Draft the JV outreach email for the primary JV partner type.**

Use this structure (adapted from the Financial Planner → Real Estate Agent example):

> *"Hey [Partner name],*
>
> *If you have anyone who [specific trigger situation — e.g., wants to buy or sell a property, or who's about retirement age and has recently been made redundant], I've got something that I think would really help them out. I've put together a [asset — e.g., special report, gift card, voucher] titled "[Asset name]." If you have anyone who would benefit from this, please call or text me, and I'll [send you a copy to pass on / give you gift cards to hand out]."*

Key design principles:
- **Trigger-specific** — name the exact situation that makes your service relevant now
- **Warm, not cold** — the referrer passes on an asset; they do not give out the prospect's contact details
- **Referrer looks good** — they provide genuine value to their client, not a sales pitch
- **Low friction** — the partner just has to forward something; no explanation, no selling

WHY: Not asking for a cold referral is critical. A cold referral requires the referrer to convince their client to call you — a significant social cost. A warm pass-through (share this report/voucher) requires almost no effort and creates goodwill between the referrer and their client.

---

### Phase 7: Design the Orchestrated Ask Cadence

**Step 8 — Schedule the referral ask touchpoints.**

Document the full referral ask cadence as a repeatable process:

```
REFERRAL ASK CADENCE

Touchpoint 1 — Onboarding (Day 1 of engagement):
  Deliver: upfront expectation-setting script
  Goal: plant the referral expectation early; let the customer begin thinking

Touchpoint 2 — Mid-engagement check-in (if engagement > 2 weeks):
  Deliver: satisfaction check ("How are things going so far?")
  Goal: confirm experience is positive before post-delivery ask

Touchpoint 3 — Completion / Delivery (Day of handoff):
  Deliver: post-delivery direct ask script + gift cards
  Goal: capture referral commitment when satisfaction is highest

Touchpoint 4 — Follow-up (14–21 days post-delivery):
  Deliver: brief follow-up call/email checking in on results + gentle ask
  ("We'd love to help someone else in your network — do you still have
  that gift card? Happy to send more if you'd like.")
  Goal: capture referrals from customers who forgot or were busy at delivery

JV Outreach Cadence (independent of individual customer cadence):
  Quarterly: review JV partner list; identify new trigger events (legislation
  changes, local business news, seasonal patterns); send fresh JV outreach email
  to each partner type with an updated asset or gift card batch
```

WHY: Most referral asks happen once, at delivery, if at all. A cadence spreads the ask across four touchpoints and catches customers at different stages of post-purchase satisfaction. The JV cadence treats partner relationships as a recurring asset to be actively maintained — not a one-time deal struck and forgotten.

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Business description (industry, product/service) | Yes | Needed to write specific scripts |
| Approximate customer lifetime value | Yes | Needed to size gift card amount |
| Current referral practice | Yes | Needed for audit in Phase 1 |
| Complementary businesses (JV candidates) | Recommended | Can be identified from scratch if absent |
| Customer list or CRM export | Optional | Helps segment referrer profiles |

---

## Outputs

This skill produces a single document: **referral-system.md**

Contents:

1. **Referral practice audit** — current state classification (passive hope / vague ask / active ask / active system)
2. **Upfront expectation-setting script** — adapted to the business, ready to use at onboarding
3. **Post-delivery direct ask script** — adapted to the business, with gift card amount determined
4. **Gift card mechanism** — face value, redemption condition, delivery method (physical card, digital code, voucher)
5. **Bystander-effect override** — specific person type + trigger situation table for use in direct and JV asks
6. **JV partner list** — two to four partner types profiled using the five-question framework
7. **JV outreach email template** — one per primary partner type, ready to send
8. **Orchestrated ask cadence** — four-touchpoint customer cadence + quarterly JV cadence, formatted as a checklist

---

## Key Principles

**Active over passive.** Passive word-of-mouth is a free lunch — nice, but not a strategy. A referral system requires deliberate orchestration: scripts, gifts, timelines, and JV partnerships. Hope is not a plan.

**They refer because it benefits them, not you.** People share recommendations to look good and to help their friends. Every referral script and JV mechanism must be designed around what's in it for the referrer and their contact — not around your need for new business.

**Specific over general.** "Anyone who needs X" is the perfect ingredient for the bystander effect. Name a specific person type and a specific trigger event. Personal responsibility and mental specificity collapse the gap between "I should refer someone" and actually making the introduction.

**Reward referrers — give them something to offer.** A gift card or voucher transforms the referrer from a salesperson into a value-provider. They are not asking their friend to call you; they are handing their friend $50.

**Set the expectation upfront.** Asking at delivery lands as a surprise. Setting the expectation at onboarding gives the customer the entire engagement to identify three names. It also frames referrals as the normal operating model of the business.

**The tribe is a prerequisite.** Referral systems accelerate what is already happening — a positive customer experience. Building a referral system on top of a mediocre experience produces negative word of mouth at scale. Verify satisfaction before running scripts.

**Law of 250.** Every customer has about 250 people in their life who are important enough to invite to a wedding or funeral. Treat every customer relationship as a node in a network of 250 potential referrals. One bad experience loses 250 prospects.

---

## Examples

### Example 1: Mike's Pet World — JV Gift Card Mechanism (verbatim case)

Mike's Pet World is a pet food retailer. Their JV partner: a local veterinarian who recommends XYZ dog food to clients.

The arrangement: the vet receives a supply of $50 gift cards redeemable at Mike's Pet World. After a consultation where the vet recommends XYZ food, the vet hands the client a card:

*"I recommend XYZ dog food. You can buy it at most pet food retailers but you're a good customer so here's a $50 voucher that you can redeem at Mike's Pet World, which is just down the road. They always carry plenty of stock of XYZ dog food."*

The outcome:
- Vet creates massive goodwill — handing a client $50 for free
- Client receives an unexpected discount; no sales pressure
- Mike's Pet World acquires a new customer whose lifetime value is approximately $5,000
- Mike's cost: a $50 voucher (wholesale cost even less)
- Mike's also acquires the trust the client has with their vet — the referral carries that goodwill

Most customers redeem the card because throwing out a voucher with a monetary value attached feels wasteful. The conversion rate on gift card referrals far exceeds cold advertising.

### Example 2: Financial Planner → Real Estate Agent — JV Outreach Email (verbatim case)

A financial planner wants referrals from real estate agent clients. JV profiling:
- Trigger event: clients of the real estate agent who are nearing retirement age and have recently been made redundant
- Problem: how to leverage a redundancy package to fund a comfortable retirement
- Referrer looks good by: giving their client a free special report with practical guidance
- Asset to pass on: a free report titled "The 7 Keys to Leveraging Your Redundancy Package and Ensuring a Fully Funded Retirement"

The JV outreach email sent to six real estate agent clients:

> *"Hey Bob,*
>
> *If you have anyone who wants to buy or sell a property or who's about retirement age and has recently been made redundant, I've got something that I think would really help them out. I've put together a special report titled, "The 7 Keys to Leveraging Your Redundancy Package and Ensuring a Fully Funded Retirement." If you have anyone who would benefit from this, please call or text me, and I'll send you a copy of the report to pass on."*

This email is:
- Specific about the trigger (redundancy + retirement age)
- Not asking for cold contact details — the agent just forwards the report
- Designed so the agent looks good to their client (providing genuine value)
- Low friction — the call to action is "call or text me"

### Example 3: Home Renovation Contractor — Full System Applied

A home renovation contractor with 40 completed projects and good reviews but zero referral system.

**Upfront expectation-setting (delivered at contract signing):**
> "Mrs. Johnson, I'm going to do a great job on your kitchen. Most of our new projects come through referrals from happy clients — it keeps our overhead low and we pass those savings on. When we're done and you love the result, I'd really appreciate it if you could think of three neighbors or friends who might be planning something similar."

**Post-delivery ask (delivered on final walkthrough):**
> "Mrs. Johnson, it's been a real pleasure working with you. Here are three gift cards — each one gives a friend $500 off a kitchen or bathroom project with us. If you know anyone planning a renovation, we'd love you to pass these on."

**Gift card sizing:** Customer lifetime value = $20,000 (repeat renovations + referrals). Gift card face value = $500. Acquisition cost = 2.5%.

**JV partner profile:** Interior designers (serve homeowners before renovation begins). Trigger event: client has just signed a lease or purchased a new home. Asset: $500 gift card toward renovation. The designer hands the client the card as a gesture of added value.

**Bystander-effect override in the post-delivery ask:** "Do you have a neighbor who mentioned they've been thinking about redoing their kitchen? Anyone who's just bought a new place nearby?"

---

## References

- Dib, A. (2016). *The 1-Page Marketing Plan*, Chapter 9: Orchestrating and Stimulating Referrals (pp. 250–266).
- Law of 250: Joe Girard — developed while observing attendance at Catholic funerals and wedding guest counts. Average person has ~250 people important enough to invite to either. Each customer represents 250 potential referrals (or 250 potential enemies).
- Bystander effect: first documented by Darley and Latané (1968) following the Kitty Genovese case. Diffusion of responsibility in crowds — the same mechanism that kills generic referral asks at networking events.
- `customer-experience-systems-design` — prerequisite skill. Referral systems accelerate the existing customer experience trajectory. Run this skill first if customer satisfaction is unverified.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-customer-experience-systems-design`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
