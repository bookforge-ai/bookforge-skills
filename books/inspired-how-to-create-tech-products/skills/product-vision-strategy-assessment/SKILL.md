---
name: product-vision-strategy-assessment
description: |
  Assess or create a product vision and product strategy. Use when someone asks 'is our product vision strong enough?', 'does our strategy make sense?', 'we keep pivoting — is that a vision problem or a strategy problem?', or 'how do I write a compelling product vision?' Also use when diagnosing why teams lack direction or feel like mercenaries, stress-testing a strategy for focus and market sequencing, checking whether product principles are resolving design debates, or auditing an existing vision statement for ambition and inspiration gaps. Scores vision against 10 principles and strategy against 5 principles, identifies top gaps with specific rewrite guidance, and evaluates whether product principles exist and are functioning as guardrails. Works on vision documents, strategy decks, product plans, or verbal descriptions. Not for OKR setting — use product-okr-implementation. Not for team health or process issues — use product-team-health-diagnostic or product-process-dysfunction-diagnosis.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/product-vision-strategy-assessment
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
depends-on: []
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [24, 25, 26, 27]
tags: [product-management, product-strategy, product-vision]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Product vision statement, strategy document, product plan, or a verbal description of your current vision and strategy"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works with pasted text or document files."
discovery:
  goal: "Produce a scored, principle-by-principle assessment of a product vision and strategy, with prioritized recommendations for strengthening both"
  tasks:
    - "Score the vision against all 10 vision principles"
    - "Score the strategy against all 5 strategy principles"
    - "Evaluate whether product principles exist and are functioning as design guardrails"
    - "Diagnose whether problems are vision problems, strategy problems, or both"
    - "Produce prioritized recommendations with specific rewrite guidance"
  audience:
    roles: ["product-manager", "head-of-product", "chief-product-officer", "founder", "product-director", "product-lead"]
    experience: "any — no prior framework knowledge required"
  triggers:
    - "User shares a product vision and wants to know if it's strong"
    - "User describes a strategy that seems unfocused or reactive"
    - "User reports teams keep pivoting or losing direction"
    - "User wants to create a vision or strategy from scratch"
    - "User is preparing a product review and wants to stress-test their direction"
    - "User's teams feel like mercenaries rather than missionaries"
  not_for:
    - "Detailed product roadmap planning — this skill evaluates direction, not delivery scheduling"
    - "OKR setting — use product-okr-implementation for objective-key-result implementation"
    - "Team health or process issues — use product-team-health-diagnostic or product-process-dysfunction-diagnosis"
---

# Product Vision and Strategy Assessment

## When to Use

You have a product vision, a strategy (or lack of one), and you need to know whether they are strong, coherent, and aligned — or where they are failing.

This skill covers four interconnected elements:
- **Product vision** — the inspiring future state you are trying to create (2–10 years out)
- **Product strategy** — the sequenced path of product/market bets that get you to that vision
- **Product principles** — the belief statements that resolve design and prioritization conflicts
- **Vision vs. strategy distinction** — diagnosing whether a problem is a direction problem, a focus problem, or both

Use this skill when: you are reviewing an existing vision/strategy for quality; creating a new one; diagnosing why teams are misaligned or reactive; or preparing to evangelize direction to stakeholders, investors, or new hires.

**Do not use this skill if:** You already have a strong vision and strategy and need to write OKRs — use `product-okr-implementation`. If you need to diagnose team dysfunction, use `product-team-health-diagnostic`.

---

## Context and Input Gathering

Before running the assessment, collect:

### Required
- **The vision statement:** What future are you trying to create? How far out? (If none exists, note this — the skill will still run in creation mode.)
- **The strategy:** What is your current plan for getting to that vision? Which markets or customer segments are you targeting, and in what order?
- **The business context:** What stage is the company? Who are the primary customers today?

### Important
- **Team alignment signals:** Do teams know where you are headed? Do they feel motivated by the mission or are they executing a backlog?
- **Recent pivots:** Have you changed vision or strategy in the last 12–18 months? How many times?
- **Competitor pressure:** Is your strategy reactive to competitors or proactively customer-driven?

### Optional (improves scoring precision)
- **Product principles:** Do you have any explicit statements about what you believe is important when building your product?
- **Go-to-market motion:** How do you sell and deliver the product? Is the strategy aligned with your sales and marketing channels?
- **A specific decision or debate:** Is there a current strategic choice you are trying to resolve? Name it — the principles assessment may resolve it directly.

If the required inputs are absent, ask for them before scoring. A vision assessment without the actual vision statement will produce generic, low-value output.

---

## Process

### Step 1: Establish the Vision vs. Strategy Distinction

**Action:** Before scoring, confirm which layer each problem lives in. Separate vision issues from strategy issues explicitly.

**WHY:** Vision and strategy are often confused, which causes the wrong intervention. Vision is inspiring leadership — it sets the 2–10 year direction that motivates missionaries. Strategy is focused management — it identifies which markets or products to pursue in sequence to reach that vision. Confusing them leads to either: (a) over-pivoting the vision when the real problem is an unfocused strategy, or (b) obsessing over execution details when the team fundamentally lacks inspiring direction. The difference, as Cagan states, is analogous to the difference between leadership and management: leadership inspires and sets direction; management helps get there.

**Output:** Write two sentences:
1. "The vision layer concern is: [identified or 'no vision exists']"
2. "The strategy layer concern is: [identified or 'no coherent strategy exists']"

---

### Step 2: Score the Vision Against the 10 Vision Principles

**Action:** Evaluate the vision statement (or its absence) against each of the 10 principles. Score each 1–5. Produce a one-sentence rationale for each score.

**WHY:** Running all 10 prevents selective evaluation. The principles are cumulative — a vision that scores well on ambition (principle 3) but fails on inspiration (principle 5) will still fail to attract missionaries. A vision that articulates the right problem (principle 2) but does not embrace trends (principle 6) will be outdated before it is realized. Scoring all 10 surfaces the specific weaknesses that need addressing rather than vague "the vision needs work" feedback.

**Score scale:**
- **5** — Principle fully satisfied; no meaningful gaps
- **4** — Principle largely satisfied with minor gaps
- **3** — Partial satisfaction; could be meaningfully strengthened
- **2** — Principle largely missing or weakly present
- **1** — Principle absent or actively violated

**Vision scoring template:**

```
1. Starts with why (purpose-led):         [1-5] — [rationale]
2. Problem-oriented (not solution-locked): [1-5] — [rationale]
3. Sufficiently ambitious (2-10 year scope): [1-5] — [rationale]
4. Willing to disrupt self:               [1-5] — [rationale]
5. Genuinely inspiring (missionary fuel): [1-5] — [rationale]
6. Embraces relevant trends:              [1-5] — [rationale]
7. Anticipates where the world is heading: [1-5] — [rationale]
8. Stubborn on direction, flexible on details: [1-5] — [rationale]
9. Accepted as a leap of faith (ambitious enough): [1-5] — [rationale]
10. Actively evangelized:                 [1-5] — [rationale]

Vision total: [X/50]
```

See `references/vision-principles-detail.md` for full activation criteria per principle, including the vision pivot vs. discovery pivot distinction, the missionary vs. mercenary diagnostic, and the over-optimism vs. over-conservatism failure modes for principle 7.

---

### Step 3: Identify the Top Vision Gaps

**Action:** From the scoring, identify the 2–3 lowest-scoring principles. For each, write a specific rewrite suggestion or structural fix.

**WHY:** A ranked gap list converts a score into an action. Without it, the user has numbers but no clear next move. The suggestion should be concrete enough that the user can apply it immediately — not just "make it more inspiring" but "reframe the vision around the customer problem you are solving, removing the product/feature language in sentences 1 and 3."

**Gap output format:**
```
Gap 1: [Principle name] (Score: X/5)
Problem: [What is wrong or missing]
Fix: [Specific rewrite guidance or structural change]

Gap 2: [Principle name] (Score: X/5)
Problem: [What is wrong or missing]
Fix: [Specific rewrite guidance or structural change]
```

---

### Step 4: Score the Strategy Against the 5 Strategy Principles

**Action:** Evaluate the strategy against each of the 5 principles. Score each 1–5. Produce a one-sentence rationale.

**WHY:** Strategy fails in characteristic ways. The most common is serving multiple customer segments simultaneously, which pleases no one well. The second most common is drifting from business strategy when the business model shifts (new monetization, new sales motion). The third is competitor-reactive behavior — abandoning the customer focus when a serious competitor appears. Scoring all 5 surfaces which failure mode is active rather than leaving the diagnosis vague.

**Strategy scoring template:**

```
1. Single target market focus per release:    [1-5] — [rationale]
2. Aligned with business strategy:            [1-5] — [rationale]
3. Aligned with go-to-market strategy:        [1-5] — [rationale]
4. Customer-obsessed (not competitor-driven): [1-5] — [rationale]
5. Communicated across the organization:      [1-5] — [rationale]

Strategy total: [X/25]
```

**Prioritization context:** When the strategy has not yet identified which markets to tackle first, the three factors to evaluate are: total addressable market size, go-to-market fit (can existing channels serve this market?), and time to market. These three factors, balanced together, should drive sequencing decisions.

---

### Step 5: Identify the Top Strategy Gaps

**Action:** From the strategy scoring, identify the 1–2 most critical gaps with specific interventions.

**WHY:** Strategy gaps are frequently more actionable than vision gaps — a team can decide to focus on one market segment this quarter even if the vision needs months to refine. Naming the specific intervention (e.g., "choose one of your three identified customer segments and defer the other two for at least 6 months") gives the team something to act on immediately.

**Gap output format:**
```
Strategy Gap 1: [Principle name] (Score: X/5)
Problem: [What is wrong or missing]
Intervention: [Specific action or decision required]

Strategy Gap 2: [Principle name] (Score: X/5) — if applicable
Problem: [What is wrong or missing]
Intervention: [Specific action or decision required]
```

---

### Step 6: Assess Product Principles

**Action:** Determine whether the team has explicit product principles. If yes, evaluate whether they are (a) tied to real beliefs rather than aspirational platitudes, and (b) actually resolving design and prioritization debates. If no, recommend creating them.

**WHY:** Product principles are the least-known of the three layers but often the most immediately useful. Where vision describes where you are going and strategy describes how to get there, principles describe the nature of what you are building — specifically, how to resolve conflicts when two valid priorities compete. The eBay example is instructive: sellers generate most of eBay's revenue, yet eBay's principle stated "in cases where buyers and sellers conflict, prioritize the buyer — because that's what makes sellers successful." Without that principle, every design debate about buyer vs. seller experience would require escalation or arbitrary resolution. With it, hundreds of product decisions make themselves. A team without principles is navigating without a decision framework.

**Principles assessment output:**
```
Do explicit product principles exist? [Yes / No / Partially]

If yes:
- Are they belief statements (not feature lists)? [Yes / No]
- Are they specific enough to resolve real conflicts? [Yes / No]
- Have they actually resolved recent design debates? [Yes / No / Unknown]
- Rating: [Strong / Adequate / Weak / Missing]

If no or weak:
- Conflict symptom: [What design or prioritization debate keeps recurring?]
- Principle recommendation: [A draft principle that would resolve it]
  Example format: "In cases where [X] and [Y] conflict, we prioritize [X],
  because [reason that connects to vision]."
```

---

### Step 7: Produce the Overall Assessment

**Action:** Write a structured summary covering: overall diagnosis, top 3 prioritized recommendations, and a corrected or improved vision statement (if the scoring surfaces significant gaps).

**WHY:** The summary synthesizes the scoring into a prioritized action list. The overall diagnosis names whether the core problem is a vision problem, a strategy problem, a principles problem, or some combination. The prioritization ensures the team tackles the highest-leverage fix first rather than spreading effort across all gaps simultaneously.

**Assessment output format:**

```
## Product Vision and Strategy Assessment

### Overall Scores
Vision: [X/50] — [one-line diagnosis]
Strategy: [X/25] — [one-line diagnosis]
Principles: [Strong / Adequate / Weak / Missing]

### Primary Diagnosis
[2–3 sentences: What is the core problem? Is it a vision problem,
a strategy problem, a principles problem, or all three? What is
the highest-leverage fix?]

### Top Recommendations (prioritized)

1. [Highest-leverage fix — most likely a vision or focus issue]
   Action: [Specific, concrete]
   Why first: [Why this has the highest impact]

2. [Second recommendation]
   Action: [Specific, concrete]

3. [Third recommendation]
   Action: [Specific, concrete]

### Vision Rewrite (if vision scored below 30/50)
Current: "[original vision statement]"
Issues: [2–3 specific problems]
Suggested rewrite: "[revised vision statement]"
Note: This is a starting point — refine with your team.

### Strategy Adjustment (if strategy scored below 15/25)
[Specific recommendation for market focus or sequencing]

### Product Principles (if missing or weak)
[Draft 1–2 principles based on recurring conflicts identified]
```

---

## Inputs and Outputs

### Inputs
- Vision statement or description (required — or note that none exists)
- Strategy description or plan (required — or note that none exists)
- Business context: stage, customer type, markets served (required)
- Team alignment signals (important)
- Product principles, if any (optional)
- A specific strategic decision to resolve (optional)

### Outputs
- Vision scored against 10 principles (X/50 with rationale per principle)
- Strategy scored against 5 principles (X/25 with rationale per principle)
- Product principles assessment with draft principles if missing
- Top 2–3 vision gaps with specific rewrite guidance
- Top 1–2 strategy gaps with specific interventions
- Prioritized recommendation list
- Vision rewrite suggestion (if vision scored below 30/50)
- Overall diagnosis statement

---

## Key Principles

**Vision inspires; strategy focuses.** These are distinct jobs. A vision that doubles as a strategy (e.g., "win the SMB accounting market in 3 years") is neither inspiring nor focused — it is an objective. A strategy that is also a vision ("we will build the best product for everyone") is neither inspiring nor actionable. Hold the distinction firmly when diagnosing.

**The leap-of-faith test.** If a vision can be fully validated before committing to it, the vision is not ambitious enough. Vision requires several years to discover whether the solutions exist. If you already know how to deliver it, it is a roadmap, not a vision.

**Vision pivot vs. discovery pivot.** Changing the vision itself (vision pivot) is usually a sign of a weak product organization — the equivalent of a company losing its mission. Changing the approach to reach a stable vision (discovery pivot) is healthy product work. Teams should be stubborn about the destination and flexible about the route.

**Single target market is the most important strategy decision.** There is no single ideal approach to market sequencing, but the decision that matters most is simply committing to one target market at a time. Once that commitment exists, the whole organization — sales, marketing, engineering — can align behind it.

**Customers leave because you stop taking care of them.** When a serious competitor appears, the temptation is to match their features. This is always the wrong move. Customers rarely leave for a competitor's product; they leave because the current product stopped serving them well. Strategy should remain customer-obsessed through competitive pressure, not competitor-obsessed.

**Product principles are a conflict resolution tool, not a values document.** A principle like "we are committed to quality" is a platitude — it resolves nothing. A principle like "when speed of delivery and quality of experience conflict, we choose quality" resolves hundreds of decisions. The test of a good principle: does it tell a team how to decide when two good things are in tension?

---

## Examples

### Example: "Leading Platform for Small Business Accounting" Assessment

**Input provided:** "Our product vision is: 'Be the leading platform for small business accounting.' Our strategy is to add features that our top 10 enterprise customers request. We serve both freelancers and mid-market companies."

**Step 1 — Vision vs. Strategy distinction:**
- Vision layer concern: Vision is solution-locked ("platform for accounting") and market-locked ("small business"), not problem-oriented. It does not articulate why this matters or what future it creates for customers.
- Strategy layer concern: Strategy is driven by enterprise customer requests rather than a target segment, and serves two distinct customer types (freelancers and mid-market) simultaneously without sequencing.

**Step 2 — Vision scoring (selected):**
```
1. Starts with why: 1 — No purpose expressed; "leading platform" is a market position, not a why
2. Problem-oriented: 2 — Mentions accounting (a domain) not the underlying problem customers face
3. Sufficiently ambitious: 2 — "Leading platform" is achievable in 1–2 years; not 5-10 year scope
5. Genuinely inspiring: 1 — No missionary fuel; describes a market position, not a cause
9. Leap of faith: 1 — "Leading platform" is an execution target, not a leap

Vision total: 18/50 — significantly weak
```

**Step 4 — Strategy scoring (selected):**
```
1. Single target market focus: 1 — Serves freelancers AND mid-market simultaneously; no sequencing
2. Aligned with business strategy: 3 — Enterprise feature requests may align but is unclear
4. Customer-obsessed: 2 — Top 10 enterprise customers drive requests; rest of market underserved

Strategy total: 11/25 — focus and customer-obsession are the critical failures
```

**Step 7 — Output:**
```
## Product Vision and Strategy Assessment

### Overall Scores
Vision: 18/50 — solution-locked, uninspiring market position statement
Strategy: 11/25 — no market focus, reactive to loudest customers

### Primary Diagnosis
The vision describes a market position rather than a future worth creating.
It gives product teams no reason to be missionaries. The strategy compounds
this by serving two incompatible segments simultaneously and being driven by
top enterprise customer requests rather than target-market needs. The team
is operating without either inspiring direction or focused strategy.

### Top Recommendations

1. Rewrite the vision around the customer problem
   Action: Identify the specific pain that small business owners face
   (cash flow anxiety? time lost on manual reconciliation? tax season dread?)
   and write a vision that describes a world where that problem is solved.
   Why first: Everything else — strategy, principles, team motivation —
   flows from a vision grounded in the customer problem.

2. Choose one customer segment and defer the other
   Action: Decide whether to pursue freelancers or mid-market companies
   first. Build the smallest product that makes that segment successful.
   Ideas for the deferred segment are saved for future consideration.
   Why second: No strategy can produce a beloved product while serving
   two incompatible customer profiles simultaneously.

3. Replace enterprise-request-driven strategy with target-segment needs
   Action: Identify the job-to-be-done for the chosen primary segment
   (not the top 10 enterprise accounts) and build strategy around it.

### Vision Rewrite (vision scored 18/50 — below threshold)
Current: "Be the leading platform for small business accounting."
Issues: Solution-locked, market-position framing, no why, not inspiring
Suggested rewrite: "Make financial confidence accessible to every
independent professional — so running a business feels less like
surviving tax season and more like understanding your own success."
Note: This is a starting point — validate the specific pain with customers
and refine with your leadership team.

### Product Principles (if missing)
Conflict symptom: Enterprise customers vs. freelancer needs will
constantly compete for product attention.
Draft principle: "When enterprise feature requests and freelancer
workflow needs conflict, we prioritize the freelancer experience —
because delighting freelancers at scale is what builds the network
that makes enterprise customers successful."
```

---

## References

| File | Contents |
|------|----------|
| `references/vision-principles-detail.md` | Full activation criteria for all 10 vision principles; vision pivot vs. discovery pivot definition; missionary vs. mercenary diagnostic; common failure modes per principle; example visions scored against each principle |
| `references/strategy-principles-detail.md` | Full activation criteria for all 5 strategy principles; market prioritization framework (total addressable market, go-to-market fit, time to market); competitor-reactive vs. customer-obsessed strategy patterns; product/market fit sequencing approaches |
| `references/product-principles-guide.md` | What product principles are and are not; eBay buyer/seller case study; how to draft principles that resolve real conflicts; principles as public vs. internal tools; how principles complement vision and strategy |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
