---
name: lead-capture-ethical-bribe-design
description: "Use this skill to design a lead-capture ad strategy using an
  ethical bribe — a high-value free offer that self-selects high-probability
  prospects. Triggers when a user wants to capture leads, create a lead magnet,
  design a lead-generation ad, stop selling directly from ads, build a free
  report or free guide offer, set up gated content or a content upgrade, design
  a CRM capture plan, or fill square #4 of the 1-Page Marketing Plan. Also
  activates for 'ethical bribe', 'hunting vs farming', 'I keep running ads but
  nobody buys', 'how do I get people into my database', '3% buyer', 'addressable
  market', '1,233%', 'lead-gen not direct-sell', 'landing page offer', or
  'capture leads from advertising'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/lead-capture-ethical-bribe-design
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan"
    authors: ["Allan Dib"]
    chapters: [4]
tags:
  - marketing
  - lead-generation
  - lead-magnet
  - advertising
  - small-business
depends-on:
  - target-market-selection-pvp-index
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: >
        Business description, the target market (from target-market-selection-pvp-index
        or provided directly), and any existing ad copy or marketing materials.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set — business description, target market profile, and optionally
    existing ads. No code execution required.
discovery:
  goal: >
    Help the user shift from direct-sell advertising (reaching 3% of their
    addressable market) to lead-generation advertising (reaching 40%), by
    designing an ethical bribe concept, a lead-gen ad headline, a minimal capture
    form, and a CRM landing plan. Produces a concrete lead-capture.md document.
  tasks:
    - "Confirm target market (invoke dependency or gather directly)"
    - "Identify the target market's top pain point or burning question"
    - "Brainstorm ethical bribe concepts using the Seven Mistakes formula"
    - "Select the strongest concept and write the lead-gen ad headline"
    - "Design a minimal capture form (name + email or name + address only)"
    - "Plan the CRM landing: what happens after the form is submitted"
    - "Compute the addressable market shift: 3% → 40% = 1,233% improvement"
    - "Write lead-capture.md with all outputs"
  audience:
    roles:
      - small-business-owner
      - solopreneur
      - entrepreneur
      - freelancer
      - startup-founder
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User is running ads that sell directly and getting poor results"
      - "User wants to build a prospect database for follow-up"
      - "User needs a lead magnet or ethical bribe concept"
      - "User is filling square #4 of the 1-Page Marketing Plan"
      - "User wants to shift from hunting to farming"
    prerequisites:
      - "Target market must be known (use target-market-selection-pvp-index first)"
    not_for:
      - "Enterprise demand generation with marketing automation teams"
      - "Businesses that already have a functioning lead-gen funnel and are happy with it"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 92.9
      baseline: 21.4
      delta: 71.4
    tested_at: "2026-04-09"
    eval_count: 1
    assertion_count: 14
    iterations_needed: 1
---

# Lead Capture with Ethical Bribe Design

A structured process for small business owners to stop selling from ads and
start building a database of high-probability prospects. Uses the 3/7/30/30/30
market readiness model to show why lead-gen ads reach 40% of the addressable
market vs 3% for direct-sell ads — a 1,233% improvement in advertising
effectiveness. Produces an ethical bribe concept, lead-gen ad copy, a minimal
capture form, and a CRM landing plan. Required content for square #4 of the
1-Page Marketing Plan canvas.

---

## When to Use

Use this skill after target market selection and before designing a nurture
sequence. It sits in the middle of the marketing funnel: the job of square #4
is to capture interested prospects who are not yet ready to buy, so they can be
nurtured until they are.

Also use it when:
- Ads are running but generating few or no responses
- The business has no prospect database — every month starts from zero
- Marketing feels like feast-or-famine ("hunting" mode)
- The business is about to launch a new advertising campaign

Do NOT use this skill as a substitute for target market selection. If the target
market is not yet defined, invoke `target-market-selection-pvp-index` first, or
ask the user to describe their target market directly before proceeding. Every
step of this skill requires knowing exactly who the ethical bribe is for.

---

## Context & Input Gathering

### Required (must have before proceeding)
- Target market: who the business serves (segment name + key pain points)
- Business description: what the business does, what it sells

### Observable / inferrable
- Top prospect pain points (often apparent from the business description)
- Appropriate ethical bribe format (depends on industry and delivery preference)

### Defaults (apply if not provided)
- If the target market is unknown: invoke `target-market-selection-pvp-index`
  OR ask: "Who is your ideal customer, and what is the biggest problem or
  question they have before they buy from you?"
- If the user has no CRM: default recommendation is to start with a simple
  email service (Mailchimp, ConvertKit, or equivalent) — a spreadsheet is
  better than nothing but is not a system

### Sufficiency check
You have enough to proceed when you can name: (1) the target market segment,
(2) their top pain point or burning question before they buy, and (3) the
business's area of expertise. Everything else is generated in the steps below.

---

## Process

### Step 1: Confirm target market and map the top pain point

Review or gather the target market profile. Then identify the single most
pressing pain point, fear, or question a prospect in this market has BEFORE
they make a purchase decision.

**WHY:** The ethical bribe must be irresistibly relevant to the prospect's
current situation, not a generic freebie. The pain point or pre-purchase
question is the hook. A prospect who is about to make a stressful or high-stakes
decision (e.g., hiring a contractor, choosing a photographer, selecting
software) has specific fears and information gaps — the ethical bribe addresses
exactly those.

Ask: "What is the one thing your ideal prospect is most worried about, confused
about, or afraid of making a mistake on — before they buy?"

### Step 2: Apply the 3/7/30/30/30 market readiness model

Explain the model to the user and use it to reframe their advertising goal.

At any given time in a target market:

| Segment | Size | Readiness |
|---------|------|-----------|
| Ready to buy NOW | 3% | Will respond to direct-sell ads |
| Open to buying (not actively searching) | 7% | Will respond to lead-gen ads |
| Interested but not right now | 30% | Will respond to lead-gen ads |
| Not interested | 30% | Cannot be reached profitably |
| Would not buy even if free | 30% | Irrelevant — never target |

Direct-sell ads (ads that say "buy now", "call today", "get a quote") compete
for the 3% only. Lead-gen ads capture the 3% + 7% + 30% = **40%**.

40% ÷ 3% = 13.33x = **1,233% improvement** in advertising effectiveness.

**WHY:** Most business owners have been told that advertising is about making
sales. It is not. Advertising is about finding interested people and getting
them to raise their hand. The 3/7/30/30/30 model makes this concrete and
calculable. Seeing the math — not 10% better, not 50% better, but 1,233% better
— is what creates the mindset shift from hunting to farming.

### Step 3: Brainstorm ethical bribe concepts

Generate 3–5 ethical bribe concepts for the target market. An ethical bribe is
free content of genuine value to the prospect that causes them to self-identify
as a high-probability buyer.

**Formats:** free report, checklist, video series, guide, quiz result, tool,
template, mini-course, or DVD/physical item (where appropriate).

**The Seven Mistakes formula:** The most proven headline structure is:

> "Free [Format] Reveals the [N] Costly Mistakes to Avoid When [Doing the
> thing the prospect is about to do]"

This works because:
1. "Mistakes to avoid" triggers loss-aversion (more powerful than gain-framing)
2. "When [doing the thing]" qualifies the prospect — only people about to do
   this will care
3. The word "free" removes the friction of a purchase decision
4. The number makes it feel specific and bounded (not an overwhelming read)

Generate at least three headline candidates using this formula or close
variations. Evaluate each on: (a) relevance to the target pain point, (b)
specificity of the qualifying phrase, (c) how strongly it self-selects the
right prospect.

**WHY:** The bribe must be high-value to the *prospect*, not impressive to the
*business owner*. A 50-page whitepaper on company history is not a bribe. A
"7 Questions to Ask Any Plumber Before You Let Them Touch Your Pipes" checklist
is a bribe — it solves a real problem the prospect has right now.

### Step 4: Select the strongest concept and write the lead-gen ad

Choose the ethical bribe concept with the highest prospect relevance and
self-selection power. Then write a complete lead-gen ad unit:

**Headline:** The Seven Mistakes formula or equivalent (from Step 3).

**Body copy (3–5 sentences):**
- Name the prospect's pain or fear in their own language
- Introduce the ethical bribe as the solution to that specific worry
- State exactly what they will learn or receive
- Call to action: "Request your free [format] at [URL/phone/address]"

**WHY:** The ad has one job: generate a lead, not make a sale. Every word of
the ad should move the reader toward requesting the bribe — not toward
evaluating the business's credentials, pricing, or features. Those belong in
the nurture sequence, not the ad.

**Anti-pattern to avoid:** Do not include the price, a special offer, or a
"call us now" direct-sell call to action. That collapses back to targeting only
the 3%.

### Step 5: Design the minimal capture form

Specify the fields on the lead capture form. The rule is: capture the minimum
data needed to follow up, and nothing more.

**Default minimum:**
- Name (first name only is fine)
- Email address (for digital follow-up)

**Alternative minimum (for physical delivery):**
- Name + mailing address (if sending a physical bribe like a book or DVD)

**Optional (add only if operationally required):**
- Phone number (adds friction; only include if the follow-up requires calling)
- Business name / company (B2B only, if segmentation requires it)

**WHY:** Every additional field reduces response rate. The goal at this stage is
volume of interested prospects in the database, not completeness of their
profile. Profile can be enriched through the nurture sequence (see
`lead-nurture-sequence-design`). A prospect who gives their name and email is
in your database; a prospect who abandons a long form is lost forever.

### Step 6: Plan the CRM landing

Map what happens after the form is submitted:

1. **Confirmation page:** Thank the prospect. Tell them when and how to expect
   the ethical bribe (e.g., "Check your email — your free report arrives in
   the next 5 minutes").
2. **Bribe delivery:** Automated email sends the ethical bribe immediately
   (PDF attachment, download link, or shipping confirmation for physical items).
3. **CRM entry:** Prospect's name + email is logged to the CRM with a source
   tag (which campaign/ad generated this lead) and a timestamp.
4. **Nurture trigger:** The CRM starts the prospect on a follow-up sequence
   (to be designed with `lead-nurture-sequence-design`).

If no CRM exists yet: capture name + email to a spreadsheet or basic email
service as a starting point. The database is the marketing asset — even a
simple list is better than no list.

**WHY:** The CRM is the goldmine. The ethical bribe is the mining tool. Without
a system that captures and stores lead information, every ad campaign is
one-shot: prospects who respond but don't buy today are lost. With a database,
the prospect who was not ready in January might convert in June — and you still
have them.

### Step 7: Compute the addressable market shift

For the user's specific context, make the 1,233% improvement tangible:

```
Current ad budget: $[X]
Prospects reached by ad: [N]
Direct-sell addressable market: 3% of N = [0.03 × N] high-probability prospects
Lead-gen addressable market:   40% of N = [0.40 × N] high-probability prospects
Marketing spend per valid prospect (direct-sell): $[X] ÷ [0.03N] = $[Y1]
Marketing spend per valid prospect (lead-gen):    $[X] ÷ [0.40N] = $[Y2]
Improvement: [Y1] ÷ [Y2] = 13.33x = 1,233%
```

**WHY:** Abstract percentages are easy to dismiss. Plugging in real numbers
makes the opportunity cost of direct-sell advertising undeniable. A business
spending $2,000/month on direct-sell ads that reach 2,000 people is spending
$33.33 per valid prospect (60 prospects). The same $2,000 in lead-gen reaches
800 valid prospects at $2.50 each — with 13x more firepower per prospect.

### Step 8: Write lead-capture.md

Save the full output as `lead-capture.md` in the user's working directory.

**WHY:** Square #4 of the 1-Page Marketing Plan must be documented. Without a
written ethical bribe concept and ad copy, execution reverts to "we'll do it
later" — the most common reason small businesses never build a prospect database.

---

## Inputs

| Input | Format | Required |
|-------|--------|----------|
| Target market profile | text / .md (from PVP skill) | Yes |
| Business description | text | Yes |
| Existing ad copy or campaigns | text / image | Optional |
| Ad budget (for Step 7 calculation) | dollar amount | Recommended |
| CRM or email platform in use | tool name | Recommended |

---

## Outputs

Primary output: `lead-capture.md`

```markdown
# Lead Capture Plan: [Business Name]

## Target Market
[One paragraph: who they are, their top pain point]

## Ethical Bribe
**Concept:** [Name of the bribe — e.g., "Free Guide: 7 Costly Mistakes..."]
**Format:** [Report / Checklist / Video series / etc.]
**Delivery:** [Email PDF / Physical mail / Download link]

## Lead-Gen Ad Copy
**Headline:** [Full headline using Seven Mistakes formula or equivalent]
**Body:** [3–5 sentence ad copy]
**Call to action:** [Exact CTA text and response mechanism]

## Capture Form Fields
- [ ] First name
- [ ] Email address
- [ ] [Optional: phone / company if justified]

## CRM Landing Plan
1. Confirmation page message: [text]
2. Bribe delivery: [automated email / physical ship / instant download]
3. CRM tag: [campaign source + date]
4. Nurture trigger: [name of sequence or "to be designed"]

## Market Readiness Calculation
| Segment | % | Count (of [N] reached) |
|---------|---|------------------------|
| Ready to buy NOW | 3% | [0.03N] |
| Open to buying | 7% | [0.07N] |
| Interested, not now | 30% | [0.30N] |
| **Lead-gen total** | **40%** | **[0.40N]** |
| Direct-sell total | 3% | [0.03N] |
| **Improvement** | | **1,233%** |

_Square #4 of the 1-Page Marketing Plan canvas: filled._
```

---

## Key Principles

**1. The goal of your ad is to generate a lead, not make a sale.**
Conflating these two goals is the most costly mistake in small business
advertising. The ad exists to cause interested people to raise their hand.
The sale happens later, through the nurture sequence, when the prospect is
ready. Trying to close from the ad collapses the 40% addressable market back
to 3%.

**2. The ethical bribe must be genuinely valuable, not a gimmick.**
A weak bribe (a discount coupon, a brochure dressed as a "free report") does
not self-select high-probability prospects — it attracts bargain hunters. The
bribe must deliver real information the prospect wants: what to look out for,
what mistakes to avoid, what questions to ask. Its value positions the business
as an educator and expert before any sales conversation begins.

**3. Minimal capture fields preserve response rate.**
The database is built one name at a time. Every extra form field loses
prospects. Capture name and email. Build the rest of the profile through
follow-up. A long form is a conversion killer.

**4. Authority positioning over salesperson positioning.**
When a business educates its prospects through free content, it is no longer
questioned — it is trusted. The prospect who reads a free guide arrives at the
sales conversation already believing the business is the expert. A salesperson
has to earn trust through the pitch; an educator has already earned it before
the pitch begins.

**5. The database is the asset, not the ad.**
An ad campaign is temporary. The prospect database is permanent. Every name
captured today is a future sale — not just the next sale. Businesses that
treat the database as their primary asset run marketing infrastructure; everyone
else runs "random acts of marketing" that cost more than they produce.

---

## Examples

### Example 1: Wedding Photographer (canonical book example)

**Target market:** Engaged couples planning a wedding.

**Top pain point:** Fear of making an expensive, irreversible mistake when
choosing a photographer for the most important day of their life.

**Ethical bribe:** A free DVD showcasing the photographer's work AND educating
couples on what to look for.

**Headline (verbatim from the book):**
> "Free DVD Reveals the Seven Costly Mistakes to Avoid When Choosing a
> Photographer for Your Wedding Day."

**Why it works:** Anyone requesting this DVD has self-identified as someone
planning a wedding and evaluating photographers. The list of requesters is
a database of high-probability prospects — every single one is a potential
customer, unlike a general ad audience where 97% will never buy.

**Capture form:** Name + mailing address (for DVD delivery).

**CRM landing:** DVD ships within 48 hours. Lead enters CRM tagged
"wedding-dvd-[campaign]". Follow-up sequence starts day of delivery.

---

### Example 2: Independent IT Services Firm (B2B service)

**Target market:** Small business owners (10–50 employees) who manage their
own IT and are worried about data security and downtime.

**Top pain point:** Fear of a ransomware attack or data loss that could shut
down the business, combined with uncertainty about whether their current setup
is actually protected.

**Ethical bribe:** A free security checklist that lets business owners audit
their own IT setup in 15 minutes.

**Headline:**
> "Free Checklist: The 9 Critical Security Gaps Most Small Businesses
> Have — and How to Spot Them Before Hackers Do."

**Ad body:**
> "Most small business owners assume their IT is 'good enough' — until
> the day a ransomware attack proves otherwise. This free 9-point
> checklist takes 15 minutes and shows you exactly where your biggest
> vulnerabilities are. No tech jargon. No sales pitch. Just a clear,
> honest audit you can do yourself. Download it free at [URL]."

**Capture form:** First name + work email.

**CRM landing:** Instant PDF download. Lead tagged "security-checklist-[ad]".
Follow-up email Day 1: "Did you find any gaps?" opens the conversation without
selling.

**Market shift:** If the ad reaches 500 local businesses: direct-sell would
reach 15 ready buyers; lead-gen reaches 200 interested prospects (1,233%
improvement). At $500/month ad spend: $33/prospect vs $2.50/prospect.

---

### Example 3: Local Kitchen Renovation Showroom (retail/trades)

**Target market:** Homeowners planning a kitchen renovation in the next 6–18
months.

**Top pain point:** Anxiety about cost blow-outs, contractor reliability, and
making design decisions they will regret in an expensive project.

**Ethical bribe:** A free planning guide that walks homeowners through the
renovation process before they speak to any contractor.

**Headline:**
> "Free Guide: 6 Mistakes Homeowners Make That Turn a $20,000 Kitchen
> Renovation Into a $35,000 Nightmare — and How to Avoid Every One."

**Ad body:**
> "Planning a kitchen renovation? Before you call a single contractor,
> read this. Our free 12-page guide reveals the six budget-blowout
> mistakes we see homeowners make every week — and the exact questions
> to ask any contractor before you sign anything. Request your free
> copy at [URL] or call [number]."

**Capture form:** First name + email (or first name + address if mailed).

**CRM landing:** PDF emailed immediately. Lead tagged "kitchen-guide-[month]".
Follow-up sequence: 3 educational emails over 14 days, then invitation to visit
the showroom.

---

## References

- Research summary: `.meta/research/lead-capture-ethical-bribe-design.md`
- Hunter report: `.meta/research/hunter-report.md` (sk-06 entry)
- Dependency: `skills/target-market-selection-pvp-index/SKILL.md`
- Next skill in sequence: `lead-nurture-sequence-design` (square #5)
- Canvas meta-skill: `marketing-plan-canvas` (square #4 slot)
- Book profile: `.meta/book-profile.json`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-target-market-selection-pvp-index`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
