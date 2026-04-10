---
name: target-market-selection-pvp-index
description: "Use this skill to select the ideal target market or customer
  segment for a small business using the PVP Index (Personal fulfillment,
  Value to marketplace, Profitability). Triggers when a user asks to choose a
  target market, pick a niche, identify their ideal customer, score market
  segments, find the best customers to focus on, decide which customer type to
  target, narrow marketing focus, build a customer avatar, define an ideal
  customer profile, stop trying to serve everyone, or fill square #1 of the
  1-Page Marketing Plan. Also activates for 'who should I market to', 'how do
  I choose a niche', 'which customers are most profitable', 'I serve too many
  segments', or similar market-selection questions."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/target-market-selection-pvp-index
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan"
    authors: ["Allan Dib"]
    chapters: [1]
tags:
  - marketing
  - target-market
  - segmentation
  - small-business
  - niche
  - customer-avatar
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: >
        Business description including current products/services and the
        market segments the business currently serves (or is considering).
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: >
    Document set — business description and market research notes in markdown.
    No code execution required.
discovery:
  goal: >
    Help the user select their ideal target market segment using the PVP Index
    scoring framework, producing a ranked segment table, a selected primary
    target, and a customer avatar.
  tasks:
    - "Score candidate market segments on Personal fulfillment (P), Value to
       marketplace (V), and Profitability (P)"
    - "Rank segments by total PVP score (max 30)"
    - "Select primary target market (highest score)"
    - "Resolve ties using secondary criteria"
    - "Build a customer avatar for the selected segment"
    - "Write target-market.md with full output"
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
      - "User wants to choose a target market or niche"
      - "User serves too many segments and wants to focus"
      - "User needs to define an ideal customer profile"
      - "User is filling square #1 of the 1-Page Marketing Plan"
      - "User asks which customers are most profitable or enjoyable"
    prerequisites: []
    not_for:
      - "Enterprise marketing with large teams and budgets (use rigorous
         market research methodologies instead)"
      - "Businesses that have already validated a clear, focused niche and
         are happy with it"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 86
      baseline: 7
      delta: 79
    tested_at: "2026-04-09"
    eval_count: 1
    assertion_count: 14
    iterations_needed: 1
---

# Target Market Selection with the PVP Index

A structured process for small business owners to stop marketing to everyone
and start marketing to the right customers. Produces a scored segment
comparison table, a primary target market decision, and a customer avatar
— the required content for square #1 of the 1-Page Marketing Plan canvas.

The PVP Index (attributed to Frank Kern, adapted by Allan Dib) scores each
market segment on three dimensions (each 0–10):

- **P** — Personal Fulfillment: How much do you enjoy working with this type?
- **V** — Value to Marketplace: How much does this segment value your work?
- **P** — Profitability: How profitable is the engagement after all costs?

Total out of 30. Highest total = primary target for all marketing.

---

## When to Use

Use this skill at the START of any marketing effort — before writing ads,
choosing media, or crafting offers. It is the foundation because every
downstream marketing decision (message, channel, offer, lead magnet) depends
on knowing exactly who you are speaking to.

Also use it when:
- A business is spreading its marketing budget across too many segments
  and getting mediocre results everywhere
- A business owner feels they serve "everyone" and doesn't know where to
  focus
- Revenue exists but profitability is unclear (some segments may be
  loss-making despite high fees)
- The business is about to launch a new marketing campaign

Do NOT use this skill as a substitute for business strategy or product-market
fit validation. It assumes the business already has services to offer — it
selects *who to market them to*, not whether the business itself is viable.

---

## Context & Input Gathering

### Required (must have before proceeding)
- A description of the business: what it does, what services/products it
  offers
- A list of the current or candidate market segments (at least 2; ideally
  3–5)

### Observable / inferrable
- Industry and service type (often apparent from the description)
- Rough profitability (can be estimated from typical pricing and overhead)

### Defaults (apply if not provided)
- If the user can't name 3+ segments, prompt: "Think about the different
  types of customers you've served or want to serve. What are the main
  categories?"
- If profitability data is unavailable, ask the user to estimate relative
  profitability (high / medium / low) and convert to a 0–10 scale

### Sufficiency check
You have enough to proceed when you can name at least 2 segments and have
enough context to score all three PVP dimensions for each. If unsure about
personal fulfillment or profitability, ask directly — these are the dimensions
most often overlooked and most often decisive.

---

## Process

### Step 1: List candidate segments

Ask the user to name every distinct market segment they currently serve or
are considering. Record them as a simple list.

**WHY:** Without a named list, scoring cannot happen. Segments often blur
together in a business owner's mind; naming them forces clarity. Aim for
3–5 segments — fewer than 2 makes comparison trivial; more than 6 becomes
unwieldy.

### Step 2: Score each segment on Personal Fulfillment (P, 0–10)

For each segment, ask: "How much do you genuinely enjoy working with this
type of customer?" A score of 10 means you look forward to every engagement;
1 means you dread the work or the client relationship.

**WHY:** Most scoring frameworks (like ICE or RICE) omit personal fulfillment
entirely. Dib includes it because a segment you hate serving — even if
lucrative — is unsustainable. You will unconsciously underserve them, burn
out, or avoid marketing to them. Low P scores flag hidden long-term costs
that profit calculations miss.

### Step 3: Score each segment on Value to Marketplace (V, 0–10)

For each segment, ask: "How much does this type of customer value and pay for
your work?" A score of 10 means they actively seek specialists, pay premium
prices without complaint, and perceive high value. A score of 1 means they
price-shop aggressively or view your service as a commodity.

**WHY:** High value perception is what allows premium pricing. Segments that
don't perceive the value of your service will always push back on price,
require excessive justification, and create adversarial relationships. V
scores predict how price-sensitive future negotiations will be.

### Step 4: Score each segment on Profitability (P, 0–10)

For each segment, ask: "After all direct costs — time, materials, overhead
allocated to this segment — how profitable is a typical engagement?" Score
relative to your best-case scenario. High fees do not mean high profit;
account for delivery costs, revisions, support burden, and churn.

**WHY:** It is possible to be busy and broke. Dib's key distinction is
"turnover vs. left over." A segment generating $50K in revenue but $45K in
costs scores very low here. This dimension forces owners to examine actual
margin, not top-line revenue — which is often the insight that changes
everything.

### Step 5: Calculate totals and build the ranking table

Sum P + V + P for each segment. Rank from highest to lowest.

**WHY:** The total makes trade-offs visible. A segment that scores 8/3/9 (20)
versus one that scores 7/7/7 (21) reveals different problems — the first is
personally rewarding and profitable but undersells value; the second is
balanced. Seeing these numbers side by side prevents the most common error:
choosing based on gut feel alone.

### Step 6: Select the primary target market

**IF** one segment has a clearly higher total (3+ points above second place):
  → Select it as primary. Proceed to Step 7.

**IF** two segments are within 2 points of each other (a near-tie):
  → Apply the tie-breaker sequence:
  1. Which segment has the higher V score? (Value perception determines
     long-term pricing power — a critical lever for small businesses)
  2. Which segment has the larger addressable population in your geography?
  3. Which segment is easier to reach via your existing channels?
  → Select the segment that wins 2 of 3 tie-breakers. Document the
     reasoning.

**WHY:** Without an explicit decision rule, owners default to the segment they
are most comfortable with — which is often not the most strategic choice. The
tie-breaker sequence uses objective criteria rather than comfort.

### Step 7: Build the customer avatar

For the selected primary segment, construct a detailed profile. Cover:

**Demographics:**
- Age range, gender (if relevant), geography
- Job title / business type / role
- Income or business revenue range

**Psychographics (the critical layer):**
- What keeps them awake at night, worrying?
- What are they most afraid of?
- What frustrates them daily?
- What do they secretly want most?
- What is the dominant emotion this market lives with?

**Behavioral / contextual:**
- What publications, websites, or social feeds do they consume?
- What is a typical day like?
- Do they use industry-specific jargon?
- Are there built-in decision biases (e.g., highly analytical, risk-averse)?
- Who else is involved in the purchase decision? (If yes, create a second
  avatar for that influencer/gatekeeper)

**WHY:** The avatar turns an abstract segment into a specific person. All
downstream marketing — ads, offers, headlines, nurture emails — is written
to this person, not to a demographic bracket. Without a vivid avatar, copy
becomes generic and fails to trigger the "hey, that's for me" response that
makes direct-response marketing work.

### Step 8: Write target-market.md

Save the full output (scoring table + selection rationale + avatar) as
`target-market.md` in the user's working directory.

**WHY:** Square #1 of the 1-Page Marketing Plan must be documented to anchor
every subsequent marketing decision. Without a written record, the target
market selection reverts to vague memory and gets overridden under business
pressure ("maybe we should also try to reach X...").

---

## Inputs

| Input | Format | Required |
|-------|--------|----------|
| Business description | text / .md | Yes |
| Current or candidate market segments | list in text | Yes |
| Typical pricing per segment | rough estimate | Recommended |
| Gross cost/overhead per engagement | rough estimate | Recommended |
| Personal fulfillment (owner self-report) | 0–10 per segment | Gathered in Step 2 |

---

## Outputs

Primary output: `target-market.md`

```markdown
# Target Market: [Business Name]

## PVP Index Scoring

| Segment | Personal (P) | Value (V) | Profit (P) | Total /30 |
|---------|:------------:|:---------:|:----------:|----------:|
| [Seg A] | X            | X         | X          | XX        |
| [Seg B] | X            | X         | X          | XX        |
| [Seg C] | X            | X         | X          | XX        |

**Primary Target Market: [Segment Name] — Score: XX/30**

Selection rationale: [1–2 sentences explaining why this segment won,
including any tie-breaker logic applied]

---

## Customer Avatar: [Avatar Name]

**Demographics**
- Age: ...
- Role / business type: ...
- Geography: ...
- Revenue / income: ...

**Psychographics**
- Biggest fear: ...
- Keeps them awake: ...
- Daily frustration: ...
- Secretly desires: ...
- Dominant emotion: ...

**Behavior & Context**
- Reads / watches: ...
- Typical day: ...
- Decision biases: ...
- Jargon they use: ...

**Decision-Making Unit**
- Primary decision-maker: [Avatar Name]
- Influencer / gatekeeper: [Second avatar if applicable]

---

_Square #1 of the 1-Page Marketing Plan canvas: filled._
```

---

## Key Principles

**1. Niching makes price irrelevant.**
A specialist is sought out; a generalist is price-shopped. When you dominate
a specific niche, prospects come to you because you are the obvious expert for
their situation — the way a heart surgeon is not compared to a GP on fees. Do
not fear the narrow niche. Fear the broad, undifferentiated positioning.

**2. An inch wide, a mile deep — then expand.**
Start by dominating one highly specific segment. Once you own that niche,
expand to another. Trying to own multiple niches simultaneously dilutes
budget, message, and credibility. Growth comes from serial dominance, not
parallel mediocrity.

**3. Personal fulfillment is a business metric, not a luxury.**
Most frameworks optimize for revenue or margin and ignore whether you enjoy
the work. Low personal fulfillment is a hidden cost: it produces worse
delivery, higher churn, and owner burnout. A segment that scores 9 on profit
but 2 on fulfillment is not a good long-term bet.

**4. Profitability ≠ revenue.**
High fees from a high-effort, high-overhead segment can result in negative
margins. Always score profitability as "left over," not "turnover." The
segment that appears least lucrative by fee rate may be most profitable in
practice.

**5. Each service category needs its own campaign.**
A photographer who does weddings and corporate work can serve both — but each
requires a completely separate ad targeting a completely separate audience. A
single laundry-list ad speaks to neither. The PVP output tells you which
campaign to build first.

---

## Examples

### Example 1: Photographer (canonical book example)

**Scenario:** A freelance photographer serves four segments — Weddings,
Photojournalism, Corporate, and Family Portraits — and wants to know where
to focus marketing spend.

**Trigger:** "I do photography for four different markets and my marketing
isn't working. Where should I focus?"

**PVP Scoring:**

| Segment          | Personal (P) | Value (V) | Profit (P) | Total |
|------------------|:------------:|:---------:|:----------:|------:|
| Weddings         | 5            | 7         | 9          | 21    |
| Photojournalism  | 9            | 7         | 2          | 18    |
| Corporate        | 3            | 6         | 9          | 18    |
| Family Portraits | 9            | 8         | 9          | **26** |

**Output:** Family Portraits wins decisively — the only segment that scores
high on all three dimensions. Photojournalism scores high on fulfillment but
is barely profitable (equipment, time, low publication fees). Weddings are
profitable but the photographer finds them stressful. Corporate pays well but
the work is joyless.

**Avatar:** Sarah, 34, married with one toddler. Feels this is a once-in-a-
decade moment that will be on the walls of her home for decades. Her dominant
emotion is anticipation mixed with anxiety about capturing the moment
perfectly. She reads parenting blogs and Pinterest. She wants an emotional
story, not a technical portfolio.

---

### Example 2: Independent Management Consultant

**Scenario:** A consultant serves startups (project-based, $5K–$15K
engagements), mid-market companies ($20K–$60K retainers), and non-profits
(grants-funded, $8K–$20K). She finds startup work energizing but chaotic;
non-profit work fulfilling but underpaid; mid-market work steady but
bureaucratic.

**Trigger:** "I'm spread thin across three client types. Which should I focus
my marketing on?"

**PVP Scoring:**

| Segment         | Personal (P) | Value (V) | Profit (P) | Total |
|-----------------|:------------:|:---------:|:----------:|------:|
| Startups        | 8            | 5         | 4          | 17    |
| Mid-Market      | 4            | 8         | 9          | 21    |
| Non-Profits     | 7            | 3         | 3          | 13    |

**Output:** Mid-Market wins (21). Startups are energizing but score low on
both value perception and profitability — startups are budget-constrained,
slow to pay, and often require extensive scope-creep management. Non-profits
are personally rewarding but chronically undervalue consulting fees. Mid-
market companies have budget authority, respect expertise, and generate
reliable margins.

**Tie note (if Startups had scored 20):** The tie-breaker would favor
Mid-Market on V score (8 vs 5) — mid-market clients have higher value
perception and are less likely to push back on fees, which is the more
sustainable long-term lever.

**Avatar:** Marcus, 48, VP of Operations at a 200-person manufacturing
company. His dominant frustration: processes that worked at 50 people are
breaking at 200. He reads Harvard Business Review. His biggest fear is being
seen as the bottleneck that's holding the company back. He wants a consultant
who has "seen this exact problem before."

---

### Example 3: Quick-turn (user provides segment list)

**Scenario:** A web design agency owner says: "I serve real estate agents,
restaurants, law firms, and e-commerce brands. Real estate pays $2K–$5K but
I find it boring. Restaurants pay $1K and churn fast. Law firms pay $5K–$15K
but are very demanding and slow to approve work. E-commerce pays $3K–$8K
and I enjoy the work."

**Trigger:** "Which should I focus on?"

**Process:** Translate owner statements to scores:
- Real estate: P=3 (boring), V=6 (pay okay, not premium), P=6 (decent margin)
  → 15
- Restaurants: P=5 (neutral), V=3 (low price, high churn), P=2 (thin margin)
  → 10
- Law firms: P=4 (demanding = friction), V=8 (high fees, respect expertise),
  P=7 (good margin despite slow pace) → 19
- E-commerce: P=8 (enjoyable), V=6 (pay well, value speed), P=7 (good margin)
  → 21

**Output:** E-commerce wins (21). Law firms are a strong second and worth
targeting once e-commerce is established. Restaurants should be deprioritized
or dropped from marketing entirely.

---

## References

- `book-profile.json` — Full book metadata and terminology mappings
- `hunter-report.md` — sk-01 entry: PVP Index found by 5 hunters, density 5
- Research summary: `.meta/research/target-market-selection-pvp-index.md`
  (complete scoring tables, avatar questions, anti-patterns, Max Cash and
  Angela Assistant avatar examples)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

No direct dependencies. Install the full book set from GitHub.

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
