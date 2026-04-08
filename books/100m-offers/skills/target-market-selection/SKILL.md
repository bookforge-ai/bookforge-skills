---
name: target-market-selection
description: Score and select a target market before building any offer. Use this skill when starting a new business, evaluating a niche, choosing between customer segments, questioning why an existing offer is underperforming despite good execution, or deciding how narrowly to specialize. Activates on phrases like "who should I sell to," "is this a good market," "should I niche down," "I'm not getting traction," "which audience should I focus on," or any request to validate, score, or compare potential target markets.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/100m-offers/skills/target-market-selection
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: 100m-offers
    title: "$100M Offers: How To Make Offers So Good People Feel Stupid Saying No"
    authors: ["Alex Hormozi"]
    chapters: [4]
tags: [market-selection, entrepreneurship, niche-strategy, business-strategy]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Business concept, service description, or target customer hypothesis — the market or niche to evaluate"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Document set preferred: business descriptions, offer drafts, market research notes."
---

# Target Market Selection

## When to Use

You are determining who to sell to — before building an offer, before writing copy, or before spending more effort on a market that may not support success. Typical triggers:

- Starting a new business and need to choose a customer segment
- Evaluating whether your current market is holding you back despite a good product
- Deciding between two or more candidate niches or customer types
- Questioning why a great offer is not gaining traction (bad market may be the cause)
- Deciding how narrowly to specialize within a broader category
- Pivoting away from a declining or saturated market

This skill runs **before** offer design. Market selection is the highest-leverage decision in business. A great offer in the wrong market will fail. A mediocre offer in the right market will still generate revenue.

Priority hierarchy: **Market quality > Offer strength > Sales and persuasion skill**

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Business concept or service description:** What you are selling or intending to sell
  → Check prompt for: service type, product description, expertise area, problem solved
  → Ask if missing: "What product or service are you planning to offer, and what problem does it solve?"

- **Target customer hypothesis:** Who you currently think the customer is (even if uncertain)
  → Check prompt for: industry, role, demographic, company size, life situation
  → Ask if missing: "Who do you currently think your ideal customer is? Be as specific as you can — industry, role, life stage, problem they face."

### Observable Context (gather from environment)

- **Market trend data:** Any existing research, articles, or notes about the market's growth or decline
- **Competitor presence:** Signs of active demand (competitors, advertising, active communities)
- **Existing customer data:** Any past clients that reveal who is already paying

### Default Assumptions

- If no target hypothesis exists → evaluate the three macro-markets (Health, Wealth, Relationships) first to identify which one applies, then narrow from there
- If comparing multiple markets → score each against all four indicators; recommend the highest-scoring market
- If market is already chosen → run as a diagnostic; flag any indicators that score poorly

---

## Process

### Step 1: Anchor to a Macro-Market

**ACTION:** Identify which of the three universal macro-markets the business concept fits into: Health, Wealth, or Relationships.

**WHY:** These three markets exist because the pain of lacking them is universal and permanent — humans will always need to improve their physical condition, earn more money, and improve their relationships. Any business that cannot be placed in one of these buckets is attempting to create demand rather than channel existing demand, which is an order of magnitude harder. Placing yourself inside a macro-market confirms you are working with existing human desire, not against it.

| Macro-Market | Example sub-niches |
|---|---|
| **Health** | Weight loss, fitness, chronic illness, mental health, longevity, sleep, pain relief |
| **Wealth** | Business growth, investing, career advancement, sales skills, real estate, financial planning |
| **Relationships** | Dating, marriage, parenting, leadership, networking, communication, conflict resolution |

**IF the concept does not fit cleanly into one macro-market** → flag this as a structural risk; the business may be attempting to create demand rather than serve it.

**IF the concept fits multiple macro-markets** → identify the primary pain driver and anchor there. A business coach serving executives touches both Wealth and Relationships — anchor to whichever pain is the dominant purchase motivation.

---

### Step 2: Score the Market on Four Indicators

**ACTION:** Rate the candidate market on each of the four market quality indicators using the scoring rubric below. Produce a score from 1 (weak) to 3 (strong) for each indicator. Total score: 4–12.

**WHY:** You need to channel demand, not create it. The four indicators identify whether a market already has the conditions for demand to exist and be converted. Missing even one indicator creates a structural obstacle that no offer quality or sales skill can fully overcome — as the newspaper market example demonstrates: three strong indicators could not save a business from a market shrinking 25% per year.

---

#### Indicator 1: Massive Pain

**Score 1 — Low pain:** The audience experiences minor inconvenience or wants a "nice to have." They are not actively seeking a solution. No urgency.

**Score 2 — Moderate pain:** The audience has a real problem but manages it; they would buy if the offer found them but do not actively search for solutions.

**Score 3 — High pain:** The audience suffers acutely and actively seeks solutions. The problem affects their daily life, income, relationships, or health in a way they cannot ignore. They are already spending money on partial solutions.

**Diagnostic questions:**
- Are people in this market actively complaining about this problem in online communities, forums, or social media?
- Are they already paying for imperfect alternatives because no perfect solution exists?
- Would this audience immediately understand why someone would sell a solution to this problem, without explanation?

**IF pain score is 1** → stop; this market will not support meaningful revenue without extensive (and expensive) demand education.

---

#### Indicator 2: Purchasing Power

**Score 1 — Low purchasing power:** The audience cannot afford to pay what the service is worth. They may want it but lack the money or access to money.

**Score 2 — Moderate purchasing power:** The audience can pay but requires price justification; high-ticket offers will face resistance.

**Score 3 — High purchasing power:** The audience has disposable income, business revenue, or access to financing sufficient to pay premium prices without hardship.

**Diagnostic questions:**
- Can this audience afford what I need to charge to make the business viable?
- Do they already spend money in this category (competitors exist, products are sold)?
- Is the problem tied to income generation or cost reduction — which makes ROI framing easy?

**Anti-pattern — Purchasing Power Trap:** A market can have intense pain, easy targeting, and strong growth, yet still fail commercially if the audience cannot pay. Unemployed job seekers are a classic example: massive pain (joblessness), easy to target (LinkedIn, job boards), growing during recessions — but they cannot pay for resume help at prices that make the business viable. Purchasing power is non-negotiable.

---

#### Indicator 3: Easy to Target (Reachability)

**Score 1 — Hard to target:** The audience is dispersed, not organized into identifiable communities, channels, or associations. Advertising reaches too broad a group to be efficient.

**Score 2 — Moderately targetable:** The audience can be reached but requires significant creative effort or indirect channels.

**Score 3 — Easy to target:** The audience is self-organized. They belong to identifiable associations, follow specific publications or influencers, gather in online communities, attend niche events, or are reachable via narrowly defined ad targeting criteria.

**Diagnostic questions:**
- Is there a specific Facebook group, subreddit, LinkedIn group, or forum where this audience gathers?
- Are there industry associations, trade publications, or conferences serving this niche?
- Can I name 2–3 influencers, podcasts, or media channels that this exact audience consumes?

**WHY this matters beyond marketing:** Easy targeting also makes your messaging more resonant. When you know exactly where your audience gathers, you learn their exact language, fears, and aspirations — which directly improves offer design and copy.

---

#### Indicator 4: Growing Market

**Score 1 — Declining market:** The total number of potential customers is shrinking. Market contraction creates a headwind that no offer can overcome at scale.

**Score 2 — Flat market:** Stable size; the business can grow by capturing share from competitors, but the rising tide will not help.

**Score 3 — Growing market:** The number of potential customers is increasing. External forces (demographics, technology trends, regulatory changes, economic shifts) are creating new entrants into the market. A growing market is a tailwind — it makes everything easier.

**Diagnostic questions:**
- Is the number of people who could potentially become customers increasing or decreasing year over year?
- Are there demographic, technological, or economic trends driving more people into this market?
- Are competitors launching and growing, or consolidating and exiting?

**Anti-pattern — Declining Market Blindness:** Entrepreneurs are problem-solvers by nature. They will try harder, iterate faster, and find new angles when a market resists — often failing to recognize that the market itself is the problem. Lloyd's newspaper software business had a great product, great offer, and strong sales skills; the market was shrinking 25% per year. No amount of effort could overcome that headwind. When a market is declining, pivot the skill set to a growing market rather than fighting the current.

---

#### Scoring Summary

| Indicator | Score (1–3) |
|---|---|
| Massive Pain | |
| Purchasing Power | |
| Easy to Target | |
| Growing Market | |
| **Total** | **/12** |

**Interpretation:**
- **10–12:** Exceptional market. Move to offer design immediately.
- **7–9:** Solid market. Identify the weak indicator(s) and assess whether they are structural or addressable.
- **4–6:** Problematic market. At least one indicator is critically weak. Do not build an offer until the weak indicator is resolved or the market is changed.
- **4 or below:** Bad market. Stop. Redirect to a different niche or macro-market.

**Any single indicator scoring 1 is a potential deal-breaker** — evaluate whether it can be remedied before proceeding.

---

### Step 3: Validate the Niche Depth

**ACTION:** Determine whether to serve the macro-market broadly or niche down to a specific sub-segment. Apply the niche-depth rule.

**WHY:** Niching down increases the perceived relevance of any offer to the audience, which allows dramatically higher pricing for effectively the same core service. The same time management content priced at $19 as a generic course can be repriced at $1,997 when positioned for a highly specific audience (outbound B2B power tools sales reps), because the audience perceives it as built exactly for them. Specificity signals understanding, and understanding signals value. For most businesses under $10M in annual revenue, niching down will generate more profit than serving a broader audience — because conversion rates, pricing, and referral rates all improve with specificity.

**Niche-depth decision rule:**

- **Under $10M in annual revenue:** Default to niching down. Stay narrow. Serve fewer people more completely.
- **At or above $10M in annual revenue:** Evaluate whether the total addressable market (TAM) of the current niche can support further growth, or whether expansion up-market, down-market, or into adjacent niches is warranted. Do not expand prematurely — many businesses at $1M–$3M believe they have hit their ceiling when they have not.

**How to niche:**

Start with the macro-market category, then apply one or more of these specificity dimensions:

1. **Who specifically** (role, demographic, life stage): not "business owners" → "microgym owners with 50–200 members"
2. **What specific problem** (pain sub-type): not "marketing help" → "acquiring first 100 paying customers"
3. **What specific context** (industry, platform, geography): not "outbound sales training" → "outbound B2B sales training for power tools distributors"

**IF the niche feels "too small"** → challenge that assumption. Companies regularly scale to $30M+ serving a single narrow niche (chiropractors, gyms, plumbers, solar installers, roofers, salon owners). Narrowness is a feature, not a limitation, up to $10M.

---

### Step 4: Test Market Commitment Readiness

**ACTION:** Before finalizing market selection, assess whether you can commit to this market through the natural failure-and-iteration cycle.

**WHY:** The primary cause of market selection failure is not choosing the wrong market — it is abandoning a workable market before making 100 genuine offer attempts. Both dentists and chiropractors represent multi-billion dollar markets; either would work. The fatal error is switching between them before exhausting the offer iteration space. Every market switch resets positioning, reputation, referral networks, and customer feedback cycles — compounding the time cost of failure. Commit to one market. Iterate the offer, not the audience.

**Commitment readiness checklist:**

- [ ] I can articulate the specific pain of this audience without guessing
- [ ] I have access to this audience (through existing network, community, or paid channels)
- [ ] I am willing to make at least 50–100 genuine offers to this market before concluding it does not work
- [ ] I understand that if my first offer fails, the offer needs to change — not necessarily the market
- [ ] I am not currently serving a different market simultaneously (divided focus produces divided results)

**IF checklist has multiple unchecked items** → resolve access and commitment gaps before proceeding to offer design.

**Anti-pattern — Niche Hopping:** Switching markets at the first sign of resistance is the single most common cause of entrepreneurial stagnation. The impulse to hop niches (from dentists to chiropractors, from e-commerce to coaches) is driven by the false belief that the market is the problem when the offer has not been sufficiently tested. All markets have friction. The grass is not greener in the new niche — it is just unfamiliar, which temporarily masks its own friction. Stay. Iterate the offer.

---

### Step 5: Produce the Market Selection Report

**ACTION:** Synthesize Steps 1–4 into a structured market assessment. Produce a go/no-go recommendation with supporting rationale.

**WHY:** A written assessment forces explicit scoring and prevents post-hoc rationalization. It also creates a reference point for future iterations — if the market underperforms, you can return to the assessment and identify which indicator was the actual weak point.

**Output template:**

```
## Market Assessment: [Market Name / Niche Description]

**Macro-market:** [Health / Wealth / Relationships]
**Specific niche:** [Exact customer segment being evaluated]

### Four-Indicator Scorecard
| Indicator         | Score (1–3) | Rationale                        |
|-------------------|-------------|----------------------------------|
| Massive Pain      |             |                                  |
| Purchasing Power  |             |                                  |
| Easy to Target    |             |                                  |
| Growing Market    |             |                                  |
| **Total**         | **/12**     |                                  |

### Niche Depth Assessment
- Current revenue stage: [Under / Over $10M]
- Recommended niche level: [Broad / Narrow / Hyper-specific]
- Suggested niche formulation: [Who + What problem + What context]

### Risk Flags
- [Any indicator scoring 1, with explanation]
- [Any structural risk: declining market, targeting difficulty, purchasing power gap]

### Go / No-Go Recommendation
**[GO / NO-GO / CONDITIONAL GO]**

Rationale: [2–4 sentences explaining the recommendation]

Next step: [If GO → proceed to premium-pricing-strategy or grand-slam-offer-creation] 
           [If NO-GO → identify alternative markets to evaluate]
           [If CONDITIONAL GO → specify what must change before proceeding]
```

---

## Examples

### Example 1: Strong market, clear niche (GO)

**Input:** "I want to help restaurant owners increase their revenue. Is this a good market?"

**Process:**
- Macro-market: Wealth (business revenue growth)
- Pain: High (3) — restaurant margins are notoriously thin; owners are in constant pain about revenue, labor costs, and slow nights
- Purchasing power: Moderate (2) — small restaurant owners have limited cash but are willing to pay when ROI is clear
- Easy to target: High (3) — restaurant owners have associations (National Restaurant Association), industry-specific Facebook groups, trade publications (Nation's Restaurant News), and events
- Growing market: Moderate (2) — the restaurant industry is stable but competitive; growth depends on sub-niche (fast casual growing, fine dining flat)
- **Total: 10/12**

**Niche recommendation:** Narrow further. "Restaurant owners" is too broad. Recommend: "Fast casual restaurant owners with 1–3 locations wanting to increase repeat customer visits" — higher pain specificity, clearer ROI framing, tighter targeting.

**Recommendation: GO** — solid market with room to niche for premium pricing. Proceed to offer design.

---

### Example 2: Declining market, correct diagnosis (NO-GO)

**Input:** "I'm selling software services to print media companies — newspapers and magazines. I've been at it for 3 years and can't seem to grow."

**Process:**
- Macro-market: Wealth (B2B software)
- Pain: Moderate (2) — print media companies have operational problems but are more focused on survival than growth
- Purchasing power: Low (1) — print media ad revenue has collapsed; discretionary technology spend is minimal
- Easy to target: High (3) — industry is well-organized with associations and publications
- Growing market: Low (1) — print media circulation is declining 15–25% per year across the sector
- **Total: 7/12** with two indicators at 1

**Diagnosis:** Two critical weak indicators. Purchasing power is structurally constrained by declining ad revenue. Market growth is negative. These are not fixable through offer iteration. The market itself is the problem.

**Recommendation: NO-GO** — pivot the existing skill set to a growing market. The same software capabilities that served print media could serve digital media companies, local news startups, or content marketing agencies — all growing, all with purchasing power. Run a new market assessment on the pivot target before building a new offer.

---

### Example 3: Good macro-market, needs niching (CONDITIONAL GO)

**Input:** "I'm a relationship coach. Who should I target?"

**Process:**
- Macro-market: Relationships — confirmed universal demand
- Broad "relationship coaching" scores: Pain 2, Purchasing Power 2, Easy to Target 1, Growing 2 → **Total: 7/12**
- The weak point is targeting: "relationship coaching" is too diffuse to reach efficiently via any channel

**Niche candidates evaluated:**

| Niche | Pain | Purchasing Power | Easy to Target | Growing | Total |
|---|---|---|---|---|---|
| College students (relationships) | 2 | 1 | 2 | 2 | 7 |
| Newly divorced professionals (40–55) | 3 | 3 | 3 | 3 | 12 |
| Couples in early marriage (1–5 years) | 2 | 2 | 2 | 2 | 8 |

**Recommended niche:** Newly divorced professionals aged 40–55. Higher pain (life disruption), higher purchasing power (mid-career income), easy to target (divorce attorney referral networks, specific Facebook groups, therapist partnerships), and demographically growing (large boomer cohort entering this life stage).

**Recommendation: CONDITIONAL GO** — proceed only after narrowing to a specific sub-segment. Do not launch as a generic relationship coach.

---

## Key Principles

- **Market quality trumps all other factors.** Offer strength and sales skill only matter if the market has the capacity to respond. A great offer in a dying market still dies. Assess market quality before investing in offer design.

- **You are channeling demand, not creating it.** Look for markets where people are already spending money, already complaining, already seeking solutions. Demand creation is an order of magnitude more expensive and slow than demand channeling. The three macro-markets (Health, Wealth, Relationships) always have demand.

- **Specificity enables premium pricing.** The same core service priced at $19 for a generic audience can command $1,997 when positioned for a specific avatar with a specific problem in a specific context. Niching down is not limiting — it is a pricing strategy. Do not broaden until revenue warrants it (typically $10M+).

- **Commit to one market; iterate the offer, not the audience.** The failure that feels like a bad market is usually an untested offer. Make 50–100 genuine attempts before concluding the market is wrong. Every market switch resets your positioning, network, and learning — compounding the cost of starting over.

- **A single weak indicator can sink a business.** Four strong indicators produce a great market. But one indicator scoring 1 — especially purchasing power or market growth — can block revenue no matter how well the other three perform. Score honestly. Do not rationalize weak indicators away.

---

## References

- **Next step after market selection:** Use `premium-pricing-strategy` to set price points and avoid the commodity trap; use `grand-slam-offer-creation` to build an offer tailored to the selected niche.
- **Offer evaluation:** Use `value-equation-offer-audit` to assess whether the offer delivers enough perceived value for the chosen market's price sensitivity.
- For extended niche-depth examples and the full niche-pricing multiplier framework, see `references/niche-pricing-examples.md` (when available).

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — $100M Offers: How To Make Offers So Good People Feel Stupid Saying No by Alex Hormozi.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
