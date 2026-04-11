---
name: acquisition-channel-selection-scorer
description: "Use this skill to choose acquisition channels for a post-PMF product using the Balfour 6-factor scoring matrix (Cost, Targeting, Control, Input Time, Output Time, Scale — each rated 1–10). First runs two diagnostic prerequisites: language/market fit (does your copy resonate?) and channel/product fit (do your channels match how your audience discovers products?). Then classifies candidate channels into viral/word-of-mouth, organic, and paid categories; scores each on the 6 factors; and recommends 2–3 channels for a Discovery phase with explicit graduation criteria to an Optimization phase. Triggers when a growth PM asks 'which acquisition channels should I test?', 'should I do Facebook ads or SEO?', 'help me pick growth channels', 'acquisition channel prioritization', 'channel/market fit', 'Balfour channel framework', 'our paid ads aren't working', 'which channels for B2B SaaS', 'which channels for e-commerce', 'which channels for consumer app', 'acquisition strategy', or 'how do I pick channels'. Also activates for 'we're spreading too thin across channels', 'single channel focus', 'channel diversification', 'Peter Thiel one channel', 'discovery phase channels', 'channel scoring matrix', or 'six factor channel framework'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/acquisition-channel-selection-scorer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [5]
tags:
  - growth
  - acquisition
  - marketing-channels
  - channel-selection
  - startup-ops
depends-on:
  - north-star-metric-selector
  - growth-experiment-prioritization-scorer
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Product brief (product-brief.md) with business model and target audience.
        Optional: channel-candidates.md listing channels the team is considering.
        Optional: current-acquisition-data.csv with CAC/conversion by channel.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set + optional CSV. Produces channel-selection-matrix.md and
    acquisition-fit-diagnosis.md.
discovery:
  goal: >
    Produce a defensible channel selection matrix and fit diagnosis so the team
    can commit to 2–3 channels for a Discovery phase instead of spreading thin.
  tasks:
    - "Read product brief"
    - "Run language/market fit diagnosis"
    - "Run channel/product fit diagnosis"
    - "Apply first-cut heuristic by business model"
    - "Classify candidate channels (viral / organic / paid)"
    - "Score each on 6-factor Balfour matrix"
    - "Rank and recommend Discovery phase channels"
    - "Define graduation criteria to Optimization phase"
    - "Emit deliverables"
---

# Acquisition Channel Selection Scorer

Structured acquisition channel selection using the Balfour 6-factor matrix. Runs two
prerequisite fit diagnostics, applies a business-model first-cut to filter the channel
space, scores each candidate on six dimensions (Cost, Targeting, Control, Input Time,
Output Time, Scale), and recommends 2–3 channels for a time-boxed Discovery phase with
explicit graduation criteria to Optimization.

---

## When to Use

Use this skill when:

- You need to decide which 2–3 acquisition channels to test next
- Your team is debating paid ads vs. SEO vs. referral and needs a defensible rationale
- You are entering or restarting an acquisition phase after confirming product/market fit
- Your current channels feel expensive, unpredictable, or aren't producing results
- The team is spreading effort across too many channels and not optimizing any

**Prerequisites:**
- Product/market fit confirmed (must-have survey ≥ 40% "very disappointed" or stable
  retention curve). If this is not confirmed, stop — no channel will fix a product
  people don't need. See `north-star-metric-selector` for North Star setup.
- A defined North Star Metric. Channel selection is meaningless without knowing what
  "acquisition success" means in terms of downstream value, not just installs or clicks.

---

## Context and Input Gathering

Before scoring, collect:

1. **Business model** — B2B SaaS, e-commerce, consumer app, marketplace, media/ad-revenue?
   This determines the first-cut heuristic (Step 4).
2. **Target audience** — Who exactly is the ideal customer? What platforms, communities,
   and search behaviors characterize them? Be specific: "developers at Series A startups
   who use Slack daily" is actionable. "SMBs" is not.
3. **Budget and team capacity** — How much can be spent per channel experiment? How many
   engineers and marketers can work on acquisition? High input-time channels need slack
   in the schedule.
4. **Current channels** — What is the team already running? What is the current CAC and
   conversion rate per channel? (Provide current-acquisition-data.csv if available.)
5. **Candidate channels** — Does the team already have a list of channels to consider?
   (Provide channel-candidates.md if available.) If not, candidates will be proposed in
   Step 4 based on business model.

If the product brief is missing any of these, surface the gaps as questions before
proceeding. Scoring a channel without knowing the business model is guessing.

---

## Process

### Step 1 — Read the Product Brief

Read `product-brief.md` (and `current-acquisition-data.csv` and `channel-candidates.md`
if provided).

Extract and confirm:
- Core product value proposition (one sentence)
- Business model type
- Target audience definition
- Current acquisition spend and results (if available)
- Team capacity constraints

**Why:** The 6-factor scores are not universal — they are product-specific. A channel
that scores 9 on Targeting for a B2B developer tool may score 4 for a mass-market
consumer app. Grounding in the brief before scoring prevents generic recommendations
that don't survive contact with the team's real constraints.

---

### Step 2 — Language/Market Fit Diagnosis

**Definition:** Language/market fit is how well the language used to describe and market
the product resonates with potential users and motivates them to try it. The term was
coined by growth practitioner James Currier. It covers all marketing copy: landing page
taglines, ad headlines, email subject lines, in-app feature descriptions, value
propositions — every string of text a prospective user encounters.

**Why diagnose this before scoring channels:** With average online attention spans of
roughly 8 seconds, if your copy doesn't immediately connect with a felt need, every
channel will look broken. Low CTR on ads, low landing page conversion, and high bounce
rates are often misdiagnosed as channel failures — they are language failures. Scoring
channels on top of bad copy wastes the scoring effort.

**Diagnosis questions:**
- Do you have conversion rate data from landing page A/B tests, email subject lines, or
  ad copy variants? If yes, which variants won and by what margin?
- Does your current tagline describe the outcome users get, or what the product does?
  (Users care about outcomes, not features.)
- Have you asked 5–10 users to describe the product in their own words? Does their
  language match your copy, or is there a gap?
- Are your ads generating high impressions but low CTR? (Symptom of language-market
  misfit — people see the ad but don't recognize the value.)

**Output:** Flag as GREEN (language fit established — proceed), YELLOW (partial fit —
note gaps that may skew channel test results), or RED (copy untested or clearly
misaligned — recommend a messaging sprint before scaling any channel).

---

### Step 3 — Channel/Product Fit Diagnosis

**Definition:** Channel/product fit is how well the selected distribution channels match
how the target audience actually discovers products like yours. It is distinct from
language/market fit: you can have perfectly resonant copy delivered through channels
your audience never uses, and see zero results. Both fits must hold.

**Why diagnose this separately:** Teams often default to channels they are familiar with
(Facebook ads, Google Search) regardless of whether their audience uses them. A B2B
developer tool team running Instagram ads is structurally misaligned, regardless of copy
quality. Channel/product fit diagnosis prevents structural errors before scoring.

**Diagnosis questions:**
- Where does your target audience currently discover products like yours? (Communities,
  newsletters, conferences, search queries, social platforms — be specific.)
- Have existing customers told you how they found you? What are the top 3 sources?
- Are there channels where your product is already getting organic traction without
  deliberate effort? (These are strong fit signals worth amplifying.)
- Are there channels you are running that produce impressions/clicks but no retention
  after acquisition? (Symptom of channel/product misfit — reaching the wrong people.)

**Output:** Flag as GREEN (clear channel behaviors visible for audience), YELLOW
(partial data — proceed with caution), or RED (no behavioral data — recommend audience
research before committing to channels).

---

### Step 4 — First-Cut Heuristic by Business Model

Before running the full 6-factor scoring, eliminate channels that are structurally
incompatible with the business model. Scoring a structurally wrong channel wastes time
and pollutes the ranked list.

**Why:** Different business models have fundamentally different acquisition economics.
E-commerce runs on volume; B2B enterprise runs on relationship and trust; consumer apps
run on network effects and virality. A channel that is structurally optimal for one
model can be structurally wrong for another — no amount of optimization fixes a
structural mismatch.

**Apply the following first-cut by model type:**

| Business Model | Priority Channel Space | Rationale |
|---|---|---|
| B2B / Enterprise | Outbound sales, trade shows, content marketing (thought leadership), LinkedIn | Buyers require relationship-building, trust signals, and expertise validation before purchase |
| E-commerce | Paid search (SEM), SEO, retargeting, email/loyalty programs | Model depends on high-volume shopper traffic; search intent is the highest-signal entry point |
| Consumer app (viral potential) | Referral programs, social sharing, word-of-mouth, community | Network effects and instrumented virality lower CAC as user base grows |
| Marketplace (two-sided) | Split strategy: supply-side vs. demand-side channels; treat as two separate channel selection problems | Supply and demand have different acquisition needs |
| Media / ad-revenue | SEO, social content distribution, syndication, email newsletters | Revenue depends on attention volume; organic scale compounds better than paid |

After the first cut, you should have 5–8 candidate channels. If the team provided
`channel-candidates.md`, reconcile the list against this heuristic — add any that were
missed, and flag any that are structurally incompatible.

---

### Step 5 — Classify Candidate Channels

Classify each candidate into one of three mutually exclusive categories. This matters
because the categories have different cost structures, feedback loops, and time horizons
— you want at least one candidate from each category if possible, to avoid a portfolio
that is monolithic in risk profile.

**Why classify before scoring:** Classification reveals structural imbalances. A list
of seven candidates that are all paid channels will score well on Control and Output
Time but will have correlated CAC risk. One viral channel in the mix provides
diversification within the portfolio, not across the portfolio.

**The three categories:**

**Viral / Word-of-Mouth**
Distribution happens through the product itself or through users sharing it without
deliberate paid promotion. Examples: referral programs (Dropbox's free storage exchange,
PayPal's cash referral), product sharing features (Venmo's social feed, Hotmail's email
signature), community building (Slack's viral enterprise spread), instrumented virality
(invite flows, "powered by" attribution links). Key property: marginal cost of an
additional user approaches zero as the base grows.

**Organic**
Distribution happens through earned media, search presence, and content that continues
generating traffic long after creation. Examples: SEO, content marketing (blog posts,
ebooks, case studies, infographics, podcasts, webinars, video), public relations, app
store optimization (ASO), community participation (forums, Reddit, Hacker News). Key
property: high upfront input time, low marginal cost at scale, compounding returns.

**Paid**
Distribution happens through purchased placements. Examples: paid search (Google Ads,
Bing Ads), social ads (Facebook, LinkedIn, Twitter, TikTok), display advertising,
affiliate programs, sponsorships, TV/radio/print. Key property: immediate feedback loop,
precise targeting, linear cost scaling (more spend = more reach, stops when spend stops).

---

### Step 6 — Score Each Channel on the 6-Factor Balfour Matrix

For each candidate channel, assign a score of 1–10 on each of the six factors. Higher
score = more favorable for your situation. Record scores in a table.

**Factors and scoring summary (1 = unfavorable, 10 = highly favorable):**

| Factor | What it measures | Score 10 | Score 1 |
|---|---|---|---|
| **Cost** | Expected spend to run the experiment | Near-zero (email list, organic SEO) | High (TV, trade show, competitive SEM) |
| **Targeting** | Precision of audience reach | Surgical (named-account list, LinkedIn filters) | Broad (display network, national TV/radio) |
| **Control** | Ability to adjust or stop once live | Full real-time (paid ads, A/B test) | None after launch (print, live events) |
| **Input Time** | Time to launch the experiment | Same day (email, existing paid search page) | 4+ weeks (SEO content series, TV production) |
| **Output Time** | Time to get actionable results | 1–3 days (paid search, email click rates) | 2–6 months (SEO ranking, community growth) |
| **Scale** | Maximum reachable audience size | Massive (Google Search, Facebook, viral K>0.5) | Small (outbound sales reps, local community) |

For detailed rubric anchors with scored examples for each factor, see
[`references/balfour-six-factor-rubric.md`](references/balfour-six-factor-rubric.md).

**Scoring table format:**

| Channel | Category | Cost | Targeting | Control | Input Time | Output Time | Scale | Avg | Notes |
|---|---|---|---|---|---|---|---|---|---|
| [Channel A] | [Viral/Organic/Paid] | X | X | X | X | X | X | X.X | |
| [Channel B] | ... | ... | ... | ... | ... | ... | ... | ... | |

Compute the average score across all 6 factors for each channel. Sort descending.

---

### Step 7 — Compute Average and Rank

Sum the 6 factor scores for each channel and divide by 6. Sort the channel list by
average score, descending.

**Why average rather than weighted sum:** The 6 factors are designed to collectively
surface fitness, not to be optimized individually. A channel that scores 10 on Scale but
1 on Cost and 1 on Control is a high-risk bet that should surface as borderline, not
as a winner. Averaging preserves this balance. If the team has specific constraints
(e.g., "we have no engineering bandwidth for 8 weeks"), downweight Input Time manually
and note the adjustment.

**Tie-breaking rule:** When two channels have equal averages, prefer the one with higher
Control — it means you can learn faster and course-correct more cheaply.

---

### Step 8 — Recommend 2–3 Channels for Discovery Phase

Select the top 2–3 channels from the ranked list for the Discovery phase.

**Why 2–3, not more:** The channel diversification fallacy is a well-documented startup
trap. Larry Page's framing is instructive: "more wood behind fewer arrows" — concentrated
effort on fewer channels produces deeper learning faster. Peter Thiel's framing is more
stark: most businesses get zero distribution channels to work; if you try several but
don't nail one, you're finished. Attempting 5–7 channels simultaneously means each gets
shallow testing, no channel reaches statistical confidence, and the team learns nothing
actionable.

**Why not just 1:** A single channel creates brittle dependence. Two or three allows
comparison learning: you discover not just whether a channel works, but *why* one works
better than another — which reveals audience insights that compound across future
experiments.

**Composition guidance:** Ideally select one channel from each category (viral, organic,
paid) if the top 3 allow it. If all top 3 are paid, note the risk and consider adding
the highest-scoring organic or viral channel even if its average is slightly lower.

**For each recommended channel, document:**
- Why it ranked highest (which factors drove the score)
- The specific experiment to run in Discovery (what hypothesis, what creative, what
  audience segment, what landing page)
- The resource commitment required (budget, engineering hours, content creation time)

---

### Step 9 — Define Graduation Criteria to Optimization Phase

For each Discovery phase channel, define explicit, time-bounded graduation criteria.
Without these, Discovery never ends — teams keep tweaking without committing to scale.

**Why explicit criteria:** The Discovery-to-Optimization gate is where most teams get
stuck. They run one experiment, see mixed results, run another variant, see better
results, run another variant — and never make the call to scale. Pre-committing to
graduation criteria removes the decision bias.

**For each channel, define:**
- **CAC target:** What maximum cost per acquired user (or lead, or install) is acceptable
  given LTV? (e.g., "CAC ≤ $25 for a product with $120 expected 12-month LTV")
- **Volume threshold:** Minimum number of acquisitions in the test window to confirm the
  signal is real and not noise (e.g., "100 installs with ≥ 20% Day-7 retention")
- **Confidence window:** Time box for the Discovery experiment (e.g., "3-week test
  window, minimum $3,000 spend on paid channels")
- **Segment specificity:** Does the channel only work for a narrow segment, or broadly?
  (Narrow is fine for Discovery; confirm breadth in Optimization)

**Graduation call:** If a channel meets CAC target AND volume threshold within the
confidence window → promote to Optimization. If it misses either → either redesign the
experiment (different creative, different audience, different landing page) with one
more iteration, or retire the channel and replace with the next-ranked candidate.

---

### Step 10 — Emit Deliverables

Write two files:

**`channel-selection-matrix.md`** — Contains:
- Fit diagnosis summary (language/market fit status, channel/product fit status)
- Business model first-cut rationale
- Channel classification table
- Full 6-factor scoring matrix with scores, averages, and ranking
- Recommended Discovery phase channels (2–3) with rationale
- Experiment brief for each recommended channel
- Graduation criteria table

**`acquisition-fit-diagnosis.md`** — Contains:
- Language/market fit diagnosis (GREEN/YELLOW/RED) with specific gaps identified
- Channel/product fit diagnosis (GREEN/YELLOW/RED) with specific gaps identified
- Audience behavior summary (where the audience actually is)
- Recommendations for resolving any RED flags before scaling

---

## Key Principles

**1. Language/market fit is the prerequisite — without it, every channel looks broken.**
If copy doesn't resonate in 8 seconds, ads generate low CTR, landing pages fail to
convert, and the team misattributes the failure to the channel. Fix the message before
diagnosing the distribution.

**2. Channel diversification is a fallacy for startups — depth beats spread.**
Two or three channels tested deeply produces actionable learning. Seven channels tested
shallowly produces noise. Concentrated effort reaches statistical confidence faster and
cheaper.

**3. Discovery phase ≠ Optimization phase — don't optimize what you haven't validated.**
Running A/B tests on ad creative before confirming that the channel can hit CAC target
at any meaningful volume is premature optimization. Discover first. Optimize second.

**4. The 6 factors capture what is commonly mis-weighted — especially Input Time.**
Teams routinely underestimate Input Time, selecting channels that sound promising but
take 6 weeks to launch, delaying learning. Scoring Input Time forces an honest
conversation about team capacity before committing.

**5. Business model dictates the first cut — don't score channels that are structurally
wrong.**
A B2B enterprise team should not be spending scoring cycles on TikTok ads. The
first-cut heuristic eliminates structural mismatches before they pollute the matrix.

**6. Score channels as a team, not in isolation — calibration matters.**
The 6-factor scores are estimates. Different team members may score the same channel
differently based on different assumptions. Run the scoring exercise together, surface
disagreements explicitly, and document assumptions. A calibrated team score is more
reliable than an individual PM's score.

---

## Examples

### Example A — B2B SaaS (developer tool, $49/mo, targeting senior engineers at Series A–B companies)

**Language/market fit:** YELLOW — landing page copy uses generic "improve your workflow"
framing. Interviews reveal users talk about "stopping context switching between tools."
Recommendation: update copy before scaling.

**Channel/product fit:** GREEN — existing customers found the product through Hacker
News posts, Twitter/X engineering threads, and word-of-mouth from colleagues.

**First-cut:** B2B → prioritize content (thought leadership in developer communities),
outbound (senior engineers on LinkedIn), and paid search on specific query terms.

**Scoring snapshot (illustrative):**

| Channel | Category | Cost | Targeting | Control | Input | Output | Scale | Avg |
|---|---|---|---|---|---|---|---|---|---|
| LinkedIn outbound | Paid | 7 | 9 | 8 | 8 | 8 | 5 | 7.5 |
| Hacker News Show HN | Organic | 9 | 6 | 4 | 8 | 5 | 6 | 6.3 |
| Google Search (long-tail) | Paid | 6 | 8 | 9 | 6 | 9 | 5 | 7.2 |
| Twitter/X engineering content | Organic | 8 | 6 | 7 | 7 | 4 | 6 | 6.3 |
| Content blog (SEO) | Organic | 7 | 5 | 6 | 3 | 2 | 7 | 5.0 |

**Recommended Discovery channels:** LinkedIn outbound (7.5 avg), Google Search long-tail
(7.2 avg), Hacker News Show HN (6.3 avg, plus organic brand signal).

**Graduation criteria:**
- LinkedIn: 30 qualified demo requests within 4 weeks at ≤ $150 CAC
- Google Search: 50 free trial signups within 3 weeks at ≤ $40 CAC
- HN Show HN: 200 signups from one post — repeat with 2nd post to confirm repeatability

---

### Example B — Consumer App (meal planning app, freemium, targeting busy parents)

**Language/market fit:** RED — all ads use "meal planning made easy" which tests poorly.
User interviews reveal the felt need is "stop the 5pm dinner panic." Recommend a
messaging sprint before scaling any channel.

**Channel/product fit:** YELLOW — analytics show organic social referrals and App Store
search drive 70% of current installs. Team wants to add paid Instagram. Need to confirm
audience is on Instagram specifically (vs. Facebook or TikTok).

**First-cut:** Consumer viral potential → referral program and viral sharing first.
E-commerce-adjacent → App Store search (ASO) and paid search on recipe queries.

**Scoring snapshot (illustrative):**

| Channel | Category | Cost | Targeting | Control | Input | Output | Scale | Avg |
|---|---|---|---|---|---|---|---|---|---|
| Referral program | Viral | 8 | 7 | 7 | 5 | 6 | 8 | 6.8 |
| App Store Search (ASO) | Organic | 9 | 7 | 5 | 5 | 4 | 7 | 6.2 |
| Facebook/Instagram ads | Paid | 5 | 7 | 9 | 8 | 9 | 8 | 7.7 |
| Google Search (recipe queries) | Paid | 6 | 6 | 9 | 7 | 9 | 8 | 7.5 |
| TikTok organic content | Organic | 8 | 5 | 5 | 6 | 3 | 8 | 5.8 |

**Recommended Discovery channels:** Facebook/Instagram ads (7.7 — but hold until
language/market RED resolved), Google Search recipe queries (7.5), Referral program
(6.8 — low input cost, compounding upside).

**Graduation criteria:**
- Facebook/Instagram: 500 app installs at ≤ $3.50 CAC with ≥ 25% Day-7 retention within
  3 weeks at $5,000 test budget. Only start after messaging sprint resolves RED flag.
- Google Search: 300 installs at ≤ $4 CAC within 2 weeks
- Referral: K-factor ≥ 0.3 within first 6 weeks of launch (meaning 30% of acquirees
  refer at least one more user)

---

## References

- Brian Balfour, "5 Steps to Choose Your Customer Acquisition Channel," Coelevate, 2013
  (the source of the 6-factor framework, cited directly in Hacking Growth Chapter 5)
- James Currier coined "language/market fit" — discussed in Chapter 5 acquisition intro
- Justin Mares, Gabriel Weinberg, Andrew Chen, James Currier — channel category taxonomy
  (viral/organic/paid) as attributed in the book
- Peter Thiel on single-channel depth — referenced in Chapter 5 footnote 12, originally
  from Blake Masters' notes on Thiel's Stanford CS183 startup course, 2012
- Larry Page on "more wood behind fewer arrows" — Chapter 5

---

## License

Content derived from *Hacking Growth* by Sean Ellis and Morgan Brown, used under fair
use for educational skill generation. This SKILL.md file is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

---

## Related BookForge Skills

**Required dependencies (run these first):**
```
clawhub install bookforge-north-star-metric-selector
clawhub install bookforge-growth-experiment-prioritization-scorer
```

**Useful follow-on skills (run these after channel selection):**
```
clawhub install bookforge-viral-loop-designer
clawhub install bookforge-activation-funnel-diagnostic
```

- `north-star-metric-selector` — Define the metric that determines what "acquisition
  success" means before choosing channels
- `growth-experiment-prioritization-scorer` — Score and sequence experiments within the
  channels you've selected (ICE scoring, growth meeting protocol)
- `viral-loop-designer` — Design the instrumented virality mechanism once viral is your
  top-ranked Discovery channel (K-factor modeling, loop architecture)
- `activation-funnel-diagnostic` — Diagnose and fix activation before scaling acquisition
  spend; channels that acquire well but activate poorly burn budget with no compounding
