---
name: build-commercial-insight
description: |
  Reverse-engineer a Commercial Insight from seller strengths and validate it against the four-criteria test.

  Trigger this skill when you need to:
  - Build a commercial insight or reframe for a teaching pitch
  - Figure out "what insight should I teach" in a B2B sales conversation
  - Find a unique angle for a commercial teaching pitch
  - Reverse engineer a pitch from your strengths (the "Deb Oler question")
  - Identify which insight to lead with in an insight-led selling approach
  - Differentiate your pitch from competitors who sell the same category
  - Determine whether a proposed reframe qualifies as commercial teaching
  - Start a sales narrative from your solution's unique differentiator rather than customer pain
  - Create an insight that "leads to" your strengths rather than "leading with" them

  NOT for: building the full 6-step pitch choreography (use author-commercial-teaching-pitch), tailoring to specific stakeholders (use tailor-pitch-by-stakeholder), or scoring pitch boldness (use SAFE-BOLD framework).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/build-commercial-insight
metadata:
  openclaw:
    emoji: "💡"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors:
      - Matthew Dixon
      - Brent Adamson
    chapters:
      - 4
      - 5
tags:
  - sales
  - b2b-sales
  - commercial-teaching
  - sales-messaging
  - differentiation
  - challenger-sale
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - solution-capabilities.md — what your solution does, what competitors cannot match
    - target-customer-segment — industry, role, size, shared behaviors of the segment
  tools-required:
    - Read
    - Write
    - AskUserQuestion
  works-offline: true
discovery:
  goal: "Reverse-engineer a Commercial Insight from the seller's unique strengths, express it as a validated Reframe, and output a commercial-insight.md artifact ready to use as the foundation for a Commercial Teaching pitch."
  triggers:
    - "What insight should I teach in my next sales call?"
    - "I need a reframe for my pitch — where do I start?"
    - "How do I build an insight-led pitch from my product's strengths?"
    - "I want to stop leading with features — how do I lead to them instead?"
    - "Deb Oler question: why should customers buy from us?"
    - "Is my teaching insight actually differentiating?"
    - "What's costing my customers money that only we can fix?"
  audience:
    - Sales reps and account executives building teaching-led pitches
    - Sales enablement teams building repeatable insight narratives
    - Product marketing managers creating differentiated messaging
    - Sales managers coaching reps on insight-led conversation design
  prerequisites: none
  not-for:
    - Building the full 6-step teaching pitch — use author-commercial-teaching-pitch
    - Tailoring the pitch to specific stakeholder roles — use tailor-pitch-by-stakeholder
    - Scoring pitch boldness against the SAFE-BOLD continuum
---

# build-commercial-insight

Reverse-engineer a Commercial Insight from the seller's unique strengths and validate it against the four-criteria test. Outputs a `commercial-insight.md` artifact ready to anchor a Commercial Teaching pitch.

---

## When to Use

Use this skill when you need to identify *what to teach* before building a teaching pitch. This is the upstream step: you cannot build a strong teaching conversation without a validated insight that:

1. Routes naturally to what you do better than competitors
2. Genuinely reframes how the customer thinks (vs. confirming what they already know)
3. Creates urgency to act
4. Works across a segment — not just one deal

If you already have a validated insight and want to structure the 6-step delivery, move to `author-commercial-teaching-pitch`.

---

## Context and Input Gathering

Before starting, collect or ask for:

1. **Solution capabilities:** What does your solution do that competitors cannot or do not do at the same level? Be specific — avoid "innovative," "customer-focused," and "solutions-oriented." Those are not differentiators.
2. **Target customer segment:** What type of customer (role, industry, company size, common behavior pattern) is this insight for?
3. **What you already know about this segment's worldview:** What do they believe today about the problem area you operate in? What do they under-value or under-appreciate?

If the user has not provided a `solution-capabilities.md` file, use `AskUserQuestion` to collect the three inputs above before proceeding.

---

## Process

### Step 1 — Inventory Unique Strengths

List the specific capabilities your solution provides that competitors cannot match. For each capability, ask:

- Can a competitor offer this too, even partially?
- Would a customer lose this capability if they chose a competitor?

Keep only capabilities where the honest answer is "no, competitors cannot match this."

**Why:** The Deb Oler Question — "Why should our customers buy from us over anyone else?" — has a specific answer that most companies struggle to state clearly. Before you can identify what insight to teach, you must know where your solution actually outperforms. Without this, any insight you identify risks becoming free consulting for competitors.

Capture the result as a short list: **[Capability] → [Why competitors cannot match it]**.

### Step 2 — Focus on Under-Appreciated Capabilities

From your capability list, identify the ones customers *currently under-value* — not the ones they already know and appreciate.

Ask: "If a customer already values this capability, do they need to be taught anything about it?" If no, that capability is not the right anchor. The teaching opportunity lives specifically at the gap between the value you could deliver and the value customers currently perceive.

**Why:** Teaching is only necessary where perception lags reality. If customers already value a capability, they will buy on it without teaching. The Commercial Insight lives in the gap — the hidden value customers are missing because their worldview prevents them from seeing it.

### Step 3 — Apply the Reverse-Engineering Diagnostic

For each under-appreciated capability identified in Step 2, work backward using this diagnostic sequence:

```
Your Solution (unique capability)
    ↓
New Way (what the customer would need to do differently to capture that value)
    ↓
Emotional Impact (a peer company story where the customer sees themselves)
    ↓
Rational Drowning (quantified cost of NOT doing the New Way — in customer's own metrics)
    ↓
Reframe Candidate (the altered perspective that makes the cost suddenly visible)
```

The core diagnostic question at each step:
> "Why don't my customers value this capability already?"

That question uncovers the worldview or assumption blocking appreciation. The Reframe is the correction to that worldview.

**Why:** Building a teaching pitch forward (starting from the customer's pain) often produces generic insights that competitors can copy. Building backward from your unique capability ensures the insight naturally leads back to what only you can deliver. This is "leading to" your strengths rather than "leading with" them.

### Step 4 — Write the Reframe Candidate

Draft a one-to-two sentence Reframe statement that:
- Describes a problem or opportunity the customer has not fully seen
- Connects to a cost, risk, or missed revenue expressible in their own business metrics
- Does not mention your solution or company name

Target reaction from the customer: **"Huh, I never thought of it that way before."**

Disqualifying reaction: "I totally agree!" — enthusiastic agreement means the customer already believed this. It is not a Reframe; it is confirmation of existing beliefs.

**Why:** A Reframe that produces enthusiastic agreement is not a teaching insight — it is validation of the customer's current worldview. The commercial teaching model is built on the premise that the insight must genuinely shift perspective, not reinforce it.

### Step 5 — Validate Against the Four-Criteria Test

Score the Reframe Candidate against each rule. All four must pass before proceeding.

**Rule 1 — Leads to Unique Strengths**
Gate question: After teaching this insight, can you say: "Let me show you why we're better able to help you act on this than anyone else"?

- PASS: The insight naturally requires a capability only your solution provides.
- FAIL (Teaching into the Desert): The insight is compelling but does not require your unique capabilities. Customers can fix the problem with a generic solution or a competitor's product. If you teach this insight and the customer goes to bid, a competitor can win using your free consulting.

**Rule 2 — Challenges Assumptions**
Gate question: Does this insight tell customers something they did not already believe?

- PASS: The insight contradicts or significantly extends the customer's current worldview.
- FAIL: The customer already has this belief on their radar. Enthusiastic agreement is a failure signal, not a success signal.

**Rule 3 — Catalyzes Action**
Gate question: Does this insight create sufficient urgency that the customer will feel compelled to act, not just agree?

- PASS: The insight quantifies a cost, risk, or missed revenue large enough to make inaction uncomfortable.
- FAIL: The customer finds the insight interesting but not urgent enough to change behavior.

**Rule 4 — Scales Across Customers**
Gate question: Is this insight applicable across a recognizable segment (by role, industry, or behavioral pattern) — or does it require full customization for each individual deal?

- PASS: The insight can be pre-built by marketing and delivered consistently across multiple customers with similar characteristics.
- FAIL: The insight requires bespoke research for each customer. One-off insights do not justify the construction investment and create a free consulting risk.

If any rule fails, return to Step 3 and adjust the Reframe candidate. Common fixes:
- Rule 1 failure → check if insight is too generic; narrow to a problem only your specific capability can resolve
- Rule 2 failure → the insight is already common knowledge; go deeper or find a less obvious angle
- Rule 3 failure → the Rational Drowning data layer is missing or weak; find the quantified cost
- Rule 4 failure → the insight is too deal-specific; abstract to the pattern that holds across the segment

### Step 6 — Write the Commercial Insight Statement

Once the Reframe passes all four rules, synthesize a Commercial Insight statement in this format:

> "Most [customer segment] are unknowingly [cost/risk/missed revenue description] because of [flawed assumption or behavior]. [Your solution type] can address this in a way [alternative approaches] cannot."

This becomes the anchor for the teaching pitch. The full Reframe, Rational Drowning data, and Emotional Impact narrative are built around it.

### Step 7 — Write the commercial-insight.md Artifact

Create `commercial-insight.md` with the following structure:

```markdown
# Commercial Insight: [Working Title]

## The Deb Oler Answer
[One paragraph: what your solution does that competitors cannot. The honest, specific answer to "why should customers buy from us over anyone else?"]

## Under-Appreciated Capability
[Which specific capability is currently under-valued, and why customers do not currently value it]

## The Blocking Worldview
[What assumption or belief prevents customers from appreciating this capability today]

## The Reframe
[The corrected perspective — 1-2 sentences. Target reaction: "I never thought of it that way."]

## Four-Criteria Validation
- Rule 1 (Leads to unique strength): [PASS/FAIL + evidence]
- Rule 2 (Challenges assumptions): [PASS/FAIL + evidence]
- Rule 3 (Catalyzes action): [PASS/FAIL + quantified cost/risk]
- Rule 4 (Scales across customers): [PASS/FAIL + segment definition]

## Commercial Insight Statement
[The synthesized 1-3 sentence insight statement ready to anchor the teaching pitch]

## Target Segment
[Role, industry, size, and behavioral characteristics of the customer segment this insight is built for]

## Next Step
Build the 6-step teaching pitch using: author-commercial-teaching-pitch
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `solution-capabilities.md` | Yes | Your solution's specific capabilities and how they compare to competitors |
| Target customer segment | Yes | Industry, role, company size, common behaviors or challenges |
| Existing customer research or purchase data | Optional | Accelerates Step 3 by providing quantified cost/risk evidence |
| Draft pitch or messaging | Optional | Existing materials to audit against the four-criteria test |

---

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| `commercial-insight.md` | `./commercial-insight.md` | The validated Reframe and insight statement ready for pitch construction |

---

## Key Principles

**Start from strength, not pain.** Discovery-led selling starts from the customer's stated pain and maps to your capabilities. Commercial Teaching reverses this: start from your unique capabilities and work backward to the insight that makes customers value them. This ensures the insight is differentiating, not generic.

**Teach what customers do not know, not what they want to hear.** The target reaction is thoughtful pause and curiosity — not enthusiastic agreement. If the customer already believed the insight, no teaching occurred.

**"Leading to" vs. "leading with."** Your solution should appear at the end of the teaching conversation as the natural answer to a problem the customer now believes is urgent — not at the beginning as the subject of the pitch. Your company is mentioned last, not first.

**Only 14% of claimed unique benefits are perceived as both unique and relevant by customers.** Most differentiation claims are not actually differentiating. The four-criteria test exists to verify — not assume — that an insight is genuinely differentiated.

**Teaching into the desert is worse than not teaching at all.** A compelling insight that does not lead to your unique capabilities creates urgency without a solution. The customer goes to bid. Competitors win using your free consulting investment.

---

## Examples

See `references/worked-examples.md` for two detailed worked examples:
- Industrial distributor reverse-engineering a "hidden MRO spend" insight from their catalog breadth advantage
- Enterprise software provider reverse-engineering a "fragmentation cost" insight from their integration advantage

Both examples trace the full reverse-engineering sequence from unique capability through validated Reframe, including four-criteria validation and emotional impact narrative construction.

---

## References

- `references/worked-examples.md` — Two full reverse-engineering walkthroughs

**Source:** *The Challenger Sale* by Matthew Dixon and Brent Adamson. Chapters 4 and 5 (Teaching for Differentiation, Parts 1 and 2).

---

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to use, adapt, and redistribute with attribution.

Source book content is copyrighted by the authors. This skill contains no verbatim passages — all content is paraphrased, structured, and extended for agent execution.

---

## Related BookForge Skills

| Skill | Relationship |
|-------|-------------|
| `author-commercial-teaching-pitch` | Use after this skill — builds the 6-step delivery choreography around the validated Commercial Insight |
| `tailor-pitch-by-stakeholder` | Use after `author-commercial-teaching-pitch` — tailors the pitch to individual stakeholder roles |
| `classify-rep-profile` | Use before this skill — confirms whether the rep is operating in Challenger mode |
