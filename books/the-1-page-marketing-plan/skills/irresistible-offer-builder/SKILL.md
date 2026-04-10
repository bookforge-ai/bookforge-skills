---
name: irresistible-offer-builder
description: "Use this skill to construct a complete, irresistible offer using
  an 8-element checklist (Value, Language, Reason Why, Value Stack, Upsells,
  Payment Plan, Outrageous Guarantee, Scarcity). Triggers when a user wants to
  build an offer, design an irresistible offer, stop lazy discounting, fix a
  '10% off' offer, create a value stack, add an outrageous guarantee, design
  scarcity marketing, build a payment plan for a high-ticket product, improve
  offer conversion, write a compelling offer, design upsells, answer
  'why-should-I-buy', or fill square #2 of the 1-Page Marketing Plan. Also
  activates for 'my offers aren't converting', 'I just discount to get
  clients', 'how do I make my offer stand out', 'I keep competing on price',
  or 'what should I include in my offer'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/irresistible-offer-builder
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan"
    authors: ["Allan Dib"]
    chapters: [2]
tags:
  - marketing
  - offer-design
  - pricing
  - conversion
  - small-business
depends-on:
  - target-market-selection-pvp-index
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: >
        Business description including the specific product or service to build
        the offer around, the target market (ideally from target-market-selection-pvp-index),
        and any existing offer or pricing structure to improve.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set — business description and offer inputs in markdown.
    No code execution required.
discovery:
  goal: >
    Help small business owners construct a complete, differentiated offer document
    covering all 8 required elements — escaping the lazy discounting trap and
    producing an offer.md ready to use in marketing campaigns.
  tasks:
    - "Run two diagnostic questions to identify the right product/service"
    - "Define the A-to-B transformation (Value)"
    - "Collect and apply target market jargon (Language)"
    - "Draft reason-why justification"
    - "Design value stack of bonuses"
    - "Identify upsell opportunity"
    - "Structure payment plan if high-ticket"
    - "Draft outrageous guarantee statement"
    - "Design credible scarcity element"
    - "Audit against 10% off anti-pattern"
    - "Write offer.md with all 8 elements filled"
  audience:
    roles:
      - small-business-owner
      - solopreneur
      - entrepreneur
      - freelancer
      - startup-founder
      - consultant
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User wants to build or redesign a marketing offer"
      - "User is relying on price discounts to close sales"
      - "User's current offer blends in with competitors"
      - "User is filling square #2 of the 1-Page Marketing Plan"
      - "User asks how to increase conversion without reducing price"
    prerequisites:
      - "Target market is defined (run target-market-selection-pvp-index first)"
    not_for:
      - "Enterprise product pricing strategy with large teams (use dedicated pricing frameworks)"
      - "Businesses without a defined target market — run target-market-selection-pvp-index first"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 100
      baseline: 7.1
      delta: 92.9
    tested_at: "2026-04-09"
    eval_count: 1
    assertion_count: 14
    iterations_needed: 1
---

# Irresistible Offer Builder

A structured process for small business owners to escape the "10% off" commodity trap
and construct a compelling, differentiated offer that reverses buying risk, creates
urgency, and gives prospects an obvious reason to choose you now. Produces a complete
`offer.md` document covering all 8 required elements — ready to use in ads, landing
pages, and sales conversations.

Filling lazy offers with structure is the single highest-leverage improvement most
small businesses can make. Dib: "Taking the lazy, ill-thought-out road of '10% off'
or similar crappy offers is akin to throwing your marketing dollars in the trash."

---

## When to Use

Use this skill AFTER identifying your target market (see `target-market-selection-pvp-index`)
and BEFORE writing advertising copy, building landing pages, or running campaigns.
The offer is what all marketing points to — it must be irresistible before any media spend.

Also use it when:
- A business's current offer is "a discount" or "competitive pricing" — with nothing
  else differentiating it
- Conversion rates are low despite adequate traffic
- Prospects keep asking "how much?" before any other question (a sign of commodity
  positioning)
- Closing requires excessive persuasion or price negotiation

Do NOT use this skill to replace target market selection. If the target market is
undefined, run `target-market-selection-pvp-index` first — offer language and pain
points depend entirely on knowing exactly who you are talking to.

---

## Context & Input Gathering

### Required (must have before proceeding)
- Target market: who the offer is for (segment + pain points)
- Product or service to build the offer around
- Current pricing or price range

### Observable / inferrable
- Industry terminology and jargon (can be elicited in Step 3)
- Competitive landscape (can be derived from user description)

### Defaults (apply if not provided)
- If no target market is defined: prompt "Run target-market-selection-pvp-index first,
  or describe your ideal buyer — their biggest frustration and what they most want"
- If user has multiple products: run the two diagnostic questions to select one
- If pricing is unknown: estimate from context; refine in Step 6 (Payment Plan)

### Sufficiency check
You have enough to proceed when you know: who the buyer is, what pain they are
experiencing now, and which product/service addresses it. Everything else is built
in-session.

---

## Process

### Step 1: Run the two diagnostic questions

Ask the user:

1. "Of all your products and services, which one do you have the most confidence
   delivering? Which problem are you sure you can solve — to the point where you'd
   stake your reputation on it if you only got paid on results?"
2. "Of all your products and services, which one do you most enjoy delivering?"

Select the product or service that satisfies both. If they conflict, default to
Question 1 (confidence > enjoyment when building a first irresistible offer).

**WHY:** The offer must be built around something you can guarantee with conviction.
Doubt in delivery undermines the guarantee and the claim. Your strongest service
also produces the most credible value stack and guarantee.

---

### Step 2: Define the A-to-B transformation (Value)

For the selected product/service, define:
- **Point A:** Where is the customer now? (the pain, the problem, the frustration)
- **Point B:** Where will they be after? (the specific, concrete outcome)
- **The bridge:** What you provide to move them from A to B

Test: Could you guarantee this transformation? If not, sharpen the outcome until
you could stand behind it.

**WHY:** This is the crux of the entire offer. Dib says this is the "most valuable
thing you can do for your customer." Without a clear A-to-B, everything else in the
offer floats — the language, the guarantee, the scarcity all depend on a specific,
believable transformation. Vague transformations ("we help businesses grow") produce
vague offers that get ignored.

---

### Step 3: Collect target market language (Language)

Ask the user: "What words, phrases, or jargon does your target market use to describe
their problem and desired outcome? Think of how they would describe the situation to
a friend — not how you would describe your service."

If the user is unsure, prompt: "What do your customers complain about most? What words
do they use when they first contact you?"

Translate the offer into that language. Strike feature/spec terminology. Replace with
outcome and pain-relief language.

Examples:
- BMX riders: "endos," "sick wheelies," "bunny hops" — not frame geometry specs
- Golf: "hooks," "slices," "handicaps" — not club shaft flexibility ratings
- IT clients: "computer goes down," "can't access files" — not "network infrastructure"

**WHY:** Customers buy based on recognition — "this is exactly my problem." If your
offer uses your internal product language, it signals that you understand your product
but not your buyer. Jargon-matched language creates immediate resonance and makes the
offer feel tailor-made rather than generic.

---

### Step 4: Draft the reason why

Every strong offer must explain why it is available. Without a stated reason, prospects
assume there is a catch and become skeptical.

Draft a single sentence: "We're able to offer [the offer] because [genuine reason]."

Real reasons that work:
- Clearing old inventory / end-of-season stock
- Launching a new service and need case studies/testimonials
- Moving location or warehouse
- Anniversary / milestone
- Capacity available this month (genuine)
- Cost reduction from a new supplier/process passed on to clients

**WHY:** Dib offered a service at half competitor price and customers kept calling to
ask "what's the catch?" A clear reason why disarms skepticism instantly. Do NOT
fabricate reasons — a false reason destroys trust more than having none.

---

### Step 5: Design the value stack (bonuses)

List complementary bonuses that increase the perceived value of the core offer.
Aim for total perceived value of bonuses to exceed the price of the core offer.

Structure:
- Core offer: [main product/service + outcome]
- Bonus 1: [complementary item — name it, value it]
- Bonus 2: [complementary item — name it, value it]
- Bonus 3: [complementary item — name it, value it]
- Total value: $X | Your price today: $Y

**WHY:** Value stacking makes saying no feel irrational — the buyer gets more than
they pay for. Bonuses do not need to be expensive to produce; they need to be
genuinely useful to the target market.

---

### Step 6: Identify the upsell

At the moment of purchase, when the prospect has said yes, offer one complementary
high-margin product or service.

Upsell formula: "Most of our [offer] clients also add [complementary item] because
[specific reason it solves the next obvious problem]."

Examples: the fries with the burger, the extended warranty, the setup service with
the software, the monthly maintenance contract with the installation.

**WHY:** The prospect has already agreed to spend — this is the highest-conversion
moment for an additional offer. A $200 add-on feels small after a $2,000 core
agreement (contrast principle). Upsells increase revenue per transaction without
acquiring a new customer.

---

### Step 7: Structure the payment plan (if high-ticket)

If the offer price is $500 or higher, present an installment option.

Payment plan formula: [N] easy payments of $[installment amount]
- Set installments so that N × installment > full price (covers financing cost)
- Full-pay option: "Or save $X by paying in full today"

Example: $5,000 → "12 easy payments of $497" (total: $5,964). Lump-sum payers
receive a "$964 savings" framing.

**WHY:** People budget monthly. A $5,000 ask feels like a major decision;
$497/month feels like a line item. The same purchase is psychologically smaller
when expressed as an installment. Making lump-sum payment the "savings" option
also incentivizes full-pay without removing the installment path for those who
need it. For genuinely low-ticket items (under $100), payment plans add friction
without benefit — skip this element.

---

### Step 8: Draft the outrageous guarantee

Write a guarantee that totally reverses the risk of doing business with you.
"Satisfaction guaranteed" is the floor — it is weak and ineffective. The guarantee
must be specific and stakes-based.

Guarantee structure:
"If [specific deliverable outcome] does not happen by [specific timeframe], we will
[specific consequence — refund, redo, pay penalty]."

For deep guarantee mechanics and verbatim scripts: see `sales-conversion-trust-system`.

**WHY:** Prospects have been disappointed before. They do not trust claims by default.
An outrageous guarantee signals that you are willing to bear the risk of your own
delivery — which only someone who is confident in their results can honestly offer.
Risk reversal converts fence-sitters by removing the downside. "Satisfaction
guaranteed" fails because it is vague, expected, and easily disputed.

---

### Step 9: Design the scarcity element

Every offer needs a credible reason why the prospect must respond now. Scarcity
must be genuine — never fabricated.

Credible scarcity types:
- **Limited supply:** "Only 3 slots available at this price"
- **Limited time:** "Offer closes [specific date]"
- **Limited resources:** "We can only take 10 new clients this quarter to maintain
  service quality"
- **Running countdown:** Countdown timer on landing page, or deadline in email

**WHY:** People respond more strongly to fear of loss than to prospect of gain.
Without a reason to act now, prospects defer — and deferral is a lost sale. The
key constraint is credibility: scarcity must have its own reason why (genuine
capacity, genuine deadline, genuine stock limit). Fake scarcity is obvious to
prospects and destroys trust. Genuine scarcity creates urgency without manipulation.

---

### Step 10: Audit against the 10% off anti-pattern

Before writing offer.md, check each element against this failure-mode list:

| Anti-pattern | Failure sign | Fix |
|---|---|---|
| Lazy discount | Offer is "X% off" with nothing else | Add 7 remaining elements |
| Competitor copy | Offer is structurally identical to nearest competitor | Differentiate on Value Stack + Guarantee |
| No reason why | No explanation for why the offer is available | Draft Step 4 reason |
| Weak guarantee | "Satisfaction guaranteed" only | Rewrite with specific outcome + timeframe |
| No scarcity | No deadline, no limit, no urgency trigger | Add Step 9 scarcity element |
| Product language | Offer uses specs, features, technical terms | Rewrite in Step 3 jargon |
| Prevention pitch | Offer sells future benefit, not present pain | Reframe around existing pain (Step 2) |

**WHY:** Most offers fail 3–5 of these checks. Finding them here costs nothing;
discovering them after a campaign launch costs budget and momentum.

---

### Step 11: Write offer.md

Compile all 8 elements into the final offer document (see Outputs section for template).

**WHY:** Without a written offer, the message degrades as it passes through ads,
landing pages, and sales scripts. The document is the source of truth that keeps
all channels saying the same thing.

---

## Inputs

| Input | Format | Required |
|---|---|---|
| Target market (segment + pain points) | text / from target-market.md | Yes |
| Product or service to build the offer around | text | Yes |
| Current price or price range | rough estimate | Yes |
| Existing offer or marketing copy (if any) | text | Recommended |
| Known customer objections | text | Recommended |
| Existing testimonials or results | text | Recommended |

---

## Outputs

Primary output: `offer.md`

```markdown
# Offer: [Business Name] — [One-line offer headline]

## Diagnostic

**Product/service selected:** [Name]
**Confidence basis:** [Why you'd stake your reputation on this]
**Point A (current state):** [Specific pain/problem the buyer is in NOW]
**Point B (desired state):** [Specific, concrete outcome after delivery]

---

## The 8-Element Offer

### 1. Value Statement
[One to two sentences: what transformation is being delivered, expressed as
Point A → Point B in concrete terms]

### 2. Offer Headline (in target market's language)
[A headline using the buyer's own jargon — not product terminology]

Supporting copy: [2–3 sentences using emotionally resonant, pain-targeted language]

### 3. Reason Why
[One sentence explaining why this offer is available at this price/terms right now]

### 4. Value Stack
| What you get | Estimated value |
|---|---|
| [Core offer: name the outcome, not the service] | $[value] |
| [Bonus 1 name + what it does for them] | $[value] |
| [Bonus 2 name + what it does for them] | $[value] |
| [Bonus 3 name + what it does for them] | $[value] |
| **Total value** | **$[total]** |

**Your investment today:** $[offer price] (or see payment plan below)

### 5. Upsell
"When you [core offer], most clients also add [upsell name] because [specific
next-pain it solves]. Add it today for $[price]."

### 6. Payment Plan
**Option A:** [N] easy payments of $[installment] — total $[installment × N]
**Option B:** Pay in full today — $[full price] (save $[difference])

_[Skip this section if under $500 total]_

### 7. Outrageous Guarantee
"If [specific outcome] does not [happen / be delivered] by [specific timeframe],
we will [specific consequence: full refund / redo at no charge / pay penalty of $X].
No questions asked."

_For deeper guarantee scripting: see sales-conversion-trust-system_

### 8. Scarcity
[State the limit and the genuine reason for it]

Example: "We are only taking [N] new clients this [month/quarter] because
[genuine capacity reason]. [Deadline or counter if applicable.]"

---

## Offer Summary (one paragraph for ads/sales scripts)

[Combine all 8 elements into a single paragraph that could be read aloud in
30 seconds or used as a Facebook ad body. Should contain: transformation,
headline language, reason why, value stack summary, guarantee, and deadline.]

---

_Square #2 of the 1-Page Marketing Plan canvas: filled._
```

---

## Key Principles

**1. Pain over prevention — always.**
People do not buy prevention; they buy cure. Targeting a prospect already in pain
eliminates price sensitivity, shortens the sales cycle, and produces better
customer satisfaction (the pain was real, the relief is appreciated). Always
identify the pain the prospect is in NOW, not a future risk they might want to
avoid.

**2. Reason why is non-negotiable.**
A strong offer without a stated reason why creates suspicion, not desire. Prospects
think: "If this is such a great deal, what's the catch?" The reason why disarms
this immediately and allows the value to land. Even a simple, obvious reason ("we
have capacity this month") is better than none.

**3. Value stack beats discount every time.**
Discounting trains buyers to wait for sales and positions you as a commodity. A
value stack keeps the price intact and makes the offer feel like a windfall.
Zero-cost bonuses (a checklist, a guide, a consult call) that are genuinely useful
can convert a hesitant prospect without touching the margin.

**4. Contrast principle amplifies upsells.**
A $300 upsell added to a $3,000 core sale feels negligible by comparison. Present
the upsell at the moment of purchase — not before, not after — to maximize the
contrast effect.

**5. Installment pricing reframes affordability.**
The same $5,000 purchase presented as 12 × $497 closes more often because people
think in monthly budgets. Price is rarely the actual objection — cashflow is.
Payment plans solve cashflow without reducing price.

**6. Scarcity must be credible to work.**
Fake countdowns and fabricated limits are transparent and destroy trust. Genuine
scarcity (real capacity limits, real deadlines, real stock) creates urgency without
manipulation. If you have no genuine scarcity, create it by design: limit intake,
set enrollment windows, cap cohort sizes.

**7. "Satisfaction guaranteed" is the floor, not the ceiling.**
Generic guarantees do nothing because everyone offers them. A specific, stakes-based
guarantee differentiates you and converts fence-sitters. If you can't make an
outrageous guarantee, sharpen the offer until you can.

---

## Examples

### Example 1: Business coach selling a $2,000 coaching program

**Diagnostic:**
- Confident delivering: 90-day revenue growth program for freelancers
- Pain (Point A): Freelancer earning $3K–$4K/month, inconsistent, working weekends
- Outcome (Point B): $7K+/month consistent income, with systems to maintain it without weekends

**The 8 elements:**

1. **Value:** "Go from $3K months to $7K months — with a system you can repeat without
   burning yourself out."
2. **Language:** "Stop chasing invoices. Stop discounting to close. Stop working
   weekends on projects you hate."
3. **Reason why:** "I'm opening 5 new spots this quarter while I test a new group
   format — at 40% below what I'll charge when it's proven."
4. **Value stack:** 90-day coaching ($2,000 value) + Pricing Script Library ($400
   value) + Client Qualification Toolkit ($300 value) + Weekly group Q&A calls
   ($600 value) = $3,300 total value. Price: $2,000.
5. **Upsell:** "Most clients add a done-with-you proposal template package at checkout
   — $300, saves 10+ hours on your first new client pitch."
6. **Payment plan:** 3 payments of $740 (total $2,220) or $2,000 paid in full (save $220).
7. **Guarantee:** "If you follow the program and don't hit $6,000 in a single month
   within 90 days, I'll continue coaching you at no charge until you do."
8. **Scarcity:** "5 spots only — I cap intake to protect the group's quality. 3 already
   filled as of this week."

---

### Example 2: Physical product — ergonomic keyboard ($149)

**Diagnostic:**
- Product: Ergonomic split keyboard
- Pain (Point A): Developer with wrist pain after 6+ hour coding sessions
- Outcome (Point B): Code for 8 hours without wrist pain, without changing workflow

**The 8 elements:**

1. **Value:** "Type all day without wrist pain — without relearning how to type."
2. **Language:** "Built for engineers who live in their terminal. Zero adjustment
   period. Plug in. Code."
3. **Reason why:** "We overproduced the Q1 batch and are clearing stock before
   the updated model ships in 60 days."
4. **Value stack:** Keyboard ($149 value) + Carrying case ($29 value) + Wrist
   placement guide PDF ($15 value) + 90-day adjustment support via email ($30 value)
   = $223 value. Price: $149.
5. **Upsell:** "Add the matching wrist rest set for $29 — used by 68% of our buyers
   and the #1 thing people wish they'd ordered at the same time."
6. **Payment plan:** [Not applicable — under $500]
7. **Guarantee:** "If your wrists still hurt after 30 days of daily use, return it
   for a full refund. We pay return shipping. No questions."
8. **Scarcity:** "84 units remaining from this batch. No restock until August."

---

### Example 3: SaaS — project management tool with free trial (fixing lazy offer)

**Before (lazy offer):** "14-day free trial. No credit card required."

**Diagnostic:**
- Pain (Point A): Agency owner whose team misses deadlines and loses client trust
- Outcome (Point B): Every project delivered on time, client trust restored, repeat business

**The 8 elements applied:**

1. **Value:** "Never miss a client deadline again — or give one painful status update
   call explaining why."
2. **Language:** "Built for agencies running 5+ client projects at once, where one
   slipped deadline costs a retainer."
3. **Reason why:** "We're proving this with new agencies this quarter — so you get
   free onboarding support that won't exist at full price."
4. **Value stack:** 14-day trial ($0) + 1:1 setup call with our team ($200 value)
   + Deadline recovery playbook PDF ($75 value) + 30-day price lock guarantee
   ($X value) = included free.
5. **Upsell:** "Most agencies add client reporting automation at signup — $29/month,
   saves 3 hours per client per month on status reports."
6. **Payment plan:** Annual plan: $59/month billed yearly (vs $79/month monthly).
7. **Guarantee:** "If you use the tool for 14 days and your team still misses a
   deadline, we'll give you 3 months free to fix it — or refund your first paid
   month, no questions."
8. **Scarcity:** "Free onboarding call is available for the next 11 signups only —
   our onboarding team has limited capacity this month."

**Result:** Same free trial — now differentiated by outcome, pain-targeted language, a specific guarantee, genuine value-adds, and credible scarcity.

---

## References

- `hunter-report.md` — sk-04 entry: 8-element offer checklist, density 4
- `.meta/research/irresistible-offer-builder.md` — full research summary with
  all source quotes and anti-pattern list
- `sales-conversion-trust-system` — deep mechanics for guarantee scripting
  (verbatim IT and pest control guarantee scripts, risk-reversal psychology)
- `target-market-selection-pvp-index` — prerequisite: defines who the offer is for
- `book-profile.json` — full book metadata

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-target-market-selection-pvp-index`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
