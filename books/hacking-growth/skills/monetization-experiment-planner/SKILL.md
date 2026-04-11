---
name: monetization-experiment-planner
description: "Use this skill to plan monetization experiments for a post-PMF product with stable retention — classify the monetization archetype (subscription / e-commerce / ad-revenue), run cohort revenue analysis to find highest-value customer segments, and propose pricing experiments using pricing relativity (3-tier anchoring), cohort upsell, and penny-gap handling. Produces a monetization-experiment-backlog.md with ordered tests and a revenue-cohort-analysis.md showing where the revenue actually comes from. Triggers when a growth PM asks 'how do I increase revenue per user', 'pricing experiment ideas', 'should I raise my prices', 'how do I structure pricing tiers', 'pricing anchoring', 'cohort revenue analysis', 'freemium to paid conversion', 'penny gap problem', 'our LTV is too low', 'CAC LTV ratio', 'monetization funnel', 'upsell experiments', or 'how do I monetize my free users'. Also activates for 'should we drop the price', 'three tier pricing', 'Qualaroo pricing case', or 'personalization recommendations revenue'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/monetization-experiment-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [8]
tags:
  - growth
  - monetization
  - pricing
  - revenue-optimization
  - startup-ops
depends-on:
  - retention-phase-intervention-selector
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Revenue cohorts CSV (revenue-cohorts.csv) segmenting customers by tier
        or spend. Pricing tiers doc (pricing-tiers.md) with current pricing
        structure. Optional: customer-surveys.md for willingness-to-pay signals.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set + CSV. Produces a monetization experiment backlog and
    revenue cohort analysis as markdown.
discovery:
  goal: >
    Produce an ordered monetization experiment backlog prioritized by impact
    on revenue per retained user, plus a revenue cohort analysis showing
    where the team should focus pricing experiments.
  tasks:
    - "Confirm retention is stable (prerequisite)"
    - "Classify monetization archetype"
    - "Run cohort revenue segmentation"
    - "Identify highest-value customer segments"
    - "Propose pricing experiments appropriate to archetype"
    - "Flag penny-gap and reactive-cut pitfalls"
    - "Emit experiment backlog and cohort analysis"
---

# Monetization Experiment Planner

A structured process for growth teams at post-PMF, Series A–B companies whose
retention is stable but revenue per user is flat or growing too slowly. Applies
the monetization framework from *Hacking Growth* (Ellis & Brown, Chapter 8) to
classify your business model, surface where revenue is actually coming from,
and generate a prioritized backlog of pricing and upsell experiments grounded
in cohort data rather than intuition.

---

## When to Use

Use this skill when:

- Retention is stable (flat or rising retention curve confirmed — see
  `retention-phase-intervention-selector` before proceeding)
- Revenue per user is flat despite user growth
- You need to restructure pricing, add a paid tier, or convert free users
- Leadership is asking "where does our revenue actually come from?"
- You are considering cutting prices and want to test the assumption first
- You want to identify which customer segments to target with upsell experiments

Do not use this skill when retention is still declining. Monetizing users who
are churning produces short-term revenue at the cost of long-term LTV and
compounds CAC-LTV inversion. Stabilize retention first.

---

## Context and Input Gathering

Before beginning, collect:

1. **Revenue cohorts CSV** — at minimum: customer ID, plan/tier or spend
   bracket, acquisition date, acquisition source, revenue in the last 90 days.
   More fields (device, geography, feature usage) improve segmentation quality.

2. **Pricing tiers doc** — current pricing structure including all plan names,
   prices, and feature gates. If pricing is informal or undocumented, write it
   down now before analysis.

3. **Customer surveys (optional)** — any willingness-to-pay or NPS data.
   Useful for generating pricing hypotheses but not required for cohort
   segmentation.

4. **Retention confirmation** — a retention curve showing stabilization (flat
   baseline after the initial drop period). If this does not exist, run
   `retention-phase-intervention-selector` first.

---

## Process

### Step 1 — Confirm Retention Is Stable

**What:** Verify that the retention curve has reached a stable floor before
beginning monetization work.

**Why:** Pricing experiments on a churning user base produce misleading
signals. If users are leaving because they don't find the product valuable,
raising prices will accelerate churn. If the curve is still declining, any
revenue gain from a pricing test will be offset by accelerated loss of the
user base that generates it. A flat retention curve is evidence of genuine
product-market fit — the only soil in which monetization experiments grow.

**Check:** Look at retention by weekly or monthly cohort. A healthy signal is
a curve that drops steeply in the first phase (expected) and then levels off
to a stable floor. If the curve is still declining at month three or later,
halt and address retention first.

---

### Step 2 — Classify the Monetization Archetype

**What:** Assign the product to one of three archetypes:

| Archetype | Revenue mechanism | Primary diagnostic metric |
|-----------|------------------|--------------------------|
| Subscription | Recurring fees; upsell to higher tiers | LTV by plan tier; upgrade rate |
| E-commerce | Transaction fees; repeat purchase | Annual spend bracket; repeat purchase rate |
| Ad-revenue | Impression inventory × CPM | ARPU; engagement depth per session |

Mixed models (e.g., freemium SaaS with an ad-supported tier) should be split
into their dominant revenue stream for this analysis. Pick the archetype that
accounts for more than 50% of current revenue.

**Why:** Each archetype has different pinch points in the monetization funnel,
different cohort segmentation logic, and different experiment types. Running
subscription experiments on an ad-revenue product wastes cycles. The
archetype classification determines everything downstream.

---

### Step 3 — Map the Monetization Funnel

**What:** Overlay revenue touchpoints on the customer journey map (built
during activation work). Mark every page, screen, or event where revenue is
earned or is being lost.

- **Subscription:** pricing/plan comparison page, upgrade modal, annual
  discount offer, add-on upsell surfaces.
- **E-commerce:** item display pages, shopping cart, payment flow,
  post-purchase upsell.
- **Ad-revenue:** every page or screen with potential inventory; pages where
  inventory exists but fill rate is low; engagement entry points that increase
  session depth.

Identify "pinch points" — junctures where conversion to revenue drops sharply.
These become primary experiment targets.

**Why:** Funnel mapping makes the monetization problem geometric rather than
abstract. A team that knows "our pricing page has a 3% upgrade conversion and
our add-on modal has a 0.4% click rate" can prioritize experiments on impact
data. A team guessing in the dark runs experiments on the wrong surfaces.

---

### Step 4 — Run Cohort Revenue Segmentation

**What:** Segment customers by revenue contribution using archetype-appropriate
buckets, then compute revenue per cohort and identify the highest-value
segments.

**Subscription segmentation:**
```
Cohort A: Free tier (if freemium)  → $0/month
Cohort B: Starter plan             → $X/month
Cohort C: Pro plan                 → $Y/month
Cohort D: Enterprise plan          → $Z/month
```

**E-commerce segmentation (by annual spend):**
```
Cohort 1: Low spenders   < $100/year
Cohort 2: Mid spenders   $100–$500/year
Cohort 3: High spenders  > $500/year
```

**Ad-revenue segmentation (by engagement depth):**
```
Cohort I:   Light users   < 5 min/session, 1–2 pages
Cohort II:  Medium users  5–15 min/session, 3–8 pages
Cohort III: Power users   > 15 min/session, 9+ pages
```

Cross-segment by acquisition source, geography, and device to identify which
channels produce high-value cohorts. An acquisition source that delivers 10%
of users but 40% of revenue should get more budget; an acquisition source that
delivers 30% of users but 5% of revenue warrants investigation or reduction.

**Why:** Aggregate revenue statistics hide the structure of who is actually
paying. A product with $50K MRR from 10,000 users has a very different
experiment strategy depending on whether the revenue comes from 50 power users
($1,000 each), from 5,000 mid-tier users ($10 each), or from a flat
distribution. Cohort segmentation makes the distribution visible and forces
experiment strategy to match reality.

---

### Step 5 — Identify Highest-Value Segment Characteristics

**What:** Within the highest-value cohorts identified in Step 4, identify
shared characteristics:

- Acquisition source (which channel brought them?)
- Features used (which product capabilities do they rely on?)
- Time-to-first-revenue (how quickly did they convert after signup?)
- Onboarding path (did they complete specific activation steps?)
- Company size or user role (for B2B products)

Build a short profile of the "ideal revenue customer." This profile drives
both the upsell experiments (Step 6) and acquisition channel decisions.

**Why:** The highest-value cohort is the empirical definition of your best
customer. Experiments designed to move lower cohorts toward the behavioral
patterns of the highest cohort are more likely to succeed than experiments
designed from first principles. The profile also surfaces which acquisition
channels to invest in to improve the revenue mix of new users.

---

### Step 6 — Propose Pricing Experiments by Archetype

Generate experiments appropriate to the classified archetype. For each
experiment, state the hypothesis, the primary metric being moved, and whether
it tests the pricing surface or the value delivery.

**Subscription experiments:**

1. **Three-tier anchor restructure** — Introduce or restructure to three named
   tiers where the middle tier's primary function is to make the top tier
   appear to be excellent value (pricing relativity / decoy effect). Dan
   Ariely's Economist experiment: when a middle option at the same price as
   the top option was present, 84% chose the top tier. When it was removed,
   only 32% did. The middle tier does not need to be popular — it needs to
   reframe the top tier.

2. **Annual discount upsell** — Offer a 15–20% annual prepay discount to
   monthly subscribers. Tests whether a meaningful saving converts month-to-
   month users to higher-LTV annual contracts. Confirm that annual LTV exceeds
   monthly LTV × churn rate before offering the discount.

3. **Usage-based add-on** — Introduce a metered component (API calls, seats,
   storage) that allows high-usage customers to expand spend without a plan
   change. Tests whether there is latent willingness to pay above the current
   plan ceiling in the highest-value cohort.

4. **Freemium penny-gap bridge** — If freemium users exist, do not ask them
   to pay the full upgrade price. Instead, offer a time-limited trial of paid
   features at no cost, then convert at the end of trial. The first dollar
   collected after free trial is dramatically easier than asking for the first
   dollar from a free user who has never seen paid features. Reference: 7
   Minute Workout app — switching to free + in-app pro upgrade produced 300%
   revenue increase despite 97% of users paying nothing.

**E-commerce experiments:**

1. **Bundle pricing** — Package two or three complementary items at a price
   lower than the sum of parts. Tests whether perceived value increase drives
   basket size without eroding margin. Start with item combinations most
   frequently purchased together (Jaccard similarity from purchase data).

2. **Free-shipping threshold** — Set a free-shipping minimum just above the
   current average order value. Tests whether customers will add one more item
   to cross the threshold, raising average order value.

3. **Recommendation-driven upsell** — Surface "frequently bought with this"
   recommendations at cart stage. Start with items where co-purchase rate in
   data exceeds 15%. Track revenue-per-session for the recommendation variant
   vs. control.

**Ad-revenue experiments:**

1. **Engagement-driven inventory expansion** — Identify product surfaces with
   high engagement but no current ad inventory. Add inventory and measure
   CPM and user retention impact together (not inventory alone).

2. **Direct-sold vs. programmatic mix shift** — Test whether moving a
   percentage of inventory from programmatic to direct-sold increases effective
   CPM. Start with the highest-engagement pages, where advertiser willingness
   to pay direct premium is highest.

---

### Step 7 — Apply Pricing Relativity and Flag Pitfalls

Before finalizing any pricing experiment, apply three checks:

**Pricing relativity check (three-tier anchor):**
Does the current pricing structure present options in a way that makes the
target tier appear to be good value? If there are only two tiers (free and
paid), add a middle or high tier to anchor perception before running the
conversion experiment. The middle tier creates contrast; contrast creates
perceived value.

**Penny gap check:**
Is the experiment asking free users to pay a first dollar? If yes, the
primary experiment lever should be a time-limited paid feature trial, not a
direct price offer. The resistance between $0 and $0.01 is disproportionately
high relative to any subsequent price increase. Convert free users to paid
trials; convert trial users to subscribers.

**Reactive price cut warning:**
If the instinct is to lower prices to increase volume, require a test first.
The Qualaroo case is the canonical counter-example: the hypothesis that lower
prices would drive more upgrades failed. The hypothesis that higher prices
would attract better customers succeeded three times in sequence. In B2B and
professional services markets, price functions as a quality signal. Lowering
price can actively suppress demand from the target segment. Always test; never
assume elasticity.

**Personalization backfire check:**
If any experiment uses behavioral data to deliver personalized pricing or
recommendations, apply the Target test: would a reasonable user find this
recommendation intrusive if they discovered how it was generated? Personalized
recommendations that feel natural increase revenue; recommendations that feel
like surveillance can permanently damage trust and revenue. Test personalization
experiments with explicit user consent framing where the data source is
sensitive.

---

### Step 8 — Rank and Emit Outputs

**What:** Rank all proposed experiments by expected impact on revenue per
retained user. Emit two output documents.

**Ranking criteria (in order):**
1. Size of the cohort affected (larger cohorts = higher potential impact)
2. Proximity to a confirmed pinch point in the funnel (known leakage = higher
   confidence)
3. Speed of signal (experiments that produce a clean revenue signal in 2–4
   weeks rank above experiments requiring 8+ weeks of accumulation)
4. Reversibility (experiments where the control can be fully restored rank
   above permanent pricing changes)

**Output 1: `monetization-experiment-backlog.md`**
One row per experiment with: experiment name, hypothesis, primary metric,
cohort affected, estimated signal timeline, ranking, and pitfall flags (penny
gap / reactive cut / personalization).

**Output 2: `revenue-cohort-analysis.md`**
One section per archetype cohort with: cohort definition, current revenue
contribution, characteristics of the segment (acquisition source, feature
usage, time-to-revenue), and the specific experiments from the backlog that
target this cohort.

---

## Key Principles

1. **Monetize retained users, not churning ones.** Pricing experiments on
   a churning base produce short-term revenue at the cost of permanent LTV
   damage. Confirm the retention curve is stable before any pricing work.

2. **Cohort revenue beats aggregate revenue for diagnosis.** A single ARPU
   number hides the distribution. The distribution reveals where experiments
   should focus.

3. **Pricing relativity — three tiers make the middle look reasonable and the
   top look like a bargain.** The decoy tier's job is not to sell; its job is
   to reframe. Never run a freemium-to-paid conversion experiment without a
   three-tier structure already in place.

4. **Lower price does not always mean more volume.** In technology and
   professional services, price functions as a quality signal. Test the
   elasticity assumption before cutting. The Qualaroo pattern (raise prices,
   get better customers) is more common than teams expect.

5. **Penny gap is real — free-to-paid friction is disproportionate.** The
   distance between $0 and $0.01 is not $0.01 psychologically. Bridge it with
   a paid feature trial, not a direct price ask.

6. **Personalization drives revenue until it feels invasive.** Amazon's
   recommendation engine increases revenue. Target's pregnancy model destroyed
   trust. The line is whether the user perceives the recommendation as helpful
   or surveillance. Test personalization experiments on segments where the
   data source is non-sensitive first.

---

## Examples

### Example 1 — SaaS Three-Tier Restructure

**Situation:** A B2B SaaS product has two plans: Free (0) and Pro ($49/month).
Free-to-Pro upgrade rate is 2.1%. The team's instinct is to lower Pro to $29.

**This skill's process:**
- Cohort segmentation shows that 80% of Pro revenue comes from teams using 3+
  seats. Single-seat users churn at 2× the rate of multi-seat users.
- Pricing relativity check: two tiers provide no anchor. The jump from $0 to
  $49 feels uncalibrated.
- Proposed restructure: Starter ($29/mo, 1 seat, limited features), Pro
  ($49/mo, 5 seats, full features), Team ($99/mo, 15 seats + admin + API).
  The Team tier anchors Pro as the obvious middle choice.
- Penny gap bridge: add a 14-day full-feature trial before asking for payment.
- Experiment 1: A/B test three-tier page vs. two-tier page. Primary metric:
  upgrade rate from free. Expected signal: 3 weeks.
- Reactive cut warning applied: Do not lower Pro to $29 until the restructure
  test runs. Qualaroo's experience suggests price sensitivity may be lower
  than assumed.

**Expected outcome:** The three-tier structure increases Pro upgrade rate. The
Team tier qualifies enterprise conversations the two-tier structure was not
having.

---

### Example 2 — E-commerce Bundle Optimization

**Situation:** An e-commerce app sells meal-prep ingredients. Average order
value is $38. Free shipping is offered at $50. Cohort analysis shows that mid-
spenders ($100–$300/year) make up 60% of customers but only 28% of revenue.
High-spenders (>$300/year) make up 12% of customers and 54% of revenue.

**This skill's process:**
- High-spender profile: acquired via recipe content channel, purchase 3+
  items per order, use the "meal plan" feature, first purchase within 7 days
  of signup.
- Funnel pinch point: 45% of carts are abandoned at payment. Average
  abandoned cart value is $33 — just below the free-shipping threshold.
- Experiment 1: Surface a "add $12 more for free shipping" prompt in cart for
  carts between $30–$48. Tests whether the threshold drives upsell without
  requiring a price change. Primary metric: average order value for carts in
  that range.
- Experiment 2: Bundle top-3 co-purchased items (Jaccard co-purchase rate
  >20%) as a "starter kit" at $42 — above free-shipping threshold. Tests
  whether bundle reduces decision friction and drives first purchase above
  threshold.
- Personalization check: recommendations based on purchase history are low-
  risk. Recommendations based on demographic inference (age, household
  composition) require explicit data disclosure.

**Expected outcome:** Free-shipping threshold prompt increases average order
value for the $30–$48 cart bracket by 15–25%. Bundle reduces decision time
and improves conversion for new users.

---

## References

- Ellis, Sean and Brown, Morgan. *Hacking Growth.* Chapter 8: Monetization.
  Crown Business, 2017.
- Ariely, Dan. *Predictably Irrational.* The Economist subscription pricing
  experiment (decoy/anchor effect).
- Kopelman, Josh. "The Penny Gap." (Venture capital blog post; referenced in
  Ellis & Brown Chapter 8.)
- Cialdini, Robert. *Influence.* Price-as-quality-signal principle (referenced
  in Ellis & Brown Chapter 8).
- Reichheld, Fred. "Prescription for Cutting Costs." Bain & Company (5%
  retention = 25–95% profit uplift formula, Chapter 7 context).

---

## License

Content derived from *Hacking Growth* (Ellis & Brown) under fair use for
educational commentary. Skill text licensed CC-BY-SA 4.0. Pipeline code MIT.

---

## Related BookForge Skills

Install the prerequisite and companion skills:

```
clawhub install bookforge-retention-phase-intervention-selector
```
Prerequisite — retention must be stable before monetization experiments begin.

```
clawhub install bookforge-growth-experiment-prioritization-scorer
```
Score the monetization experiment backlog using ICE (Impact, Confidence, Ease)
to sequence the backlog across sprint cycles.

```
clawhub install bookforge-north-star-metric-selector
```
The monetization North Star (revenue per retained user) may differ from the
growth North Star (new user acquisition). Confirm alignment before running
experiments.
