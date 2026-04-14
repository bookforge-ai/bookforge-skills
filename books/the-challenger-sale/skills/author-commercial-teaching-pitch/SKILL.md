---
name: author-commercial-teaching-pitch
description: |
  Author a Commercial Teaching pitch using the six-step choreography and polish it with SAFE-BOLD.

  Trigger this skill when you need to:
  - Write a sales pitch using commercial teaching methodology
  - Build a commercial teaching pitch from a validated insight
  - Structure a six-step pitch: warmer reframe rational drowning emotional impact new way solution
  - Author a sales narrative that leads to your solution rather than leading with it
  - Build a sales deck following challenger selling choreography
  - Write a challenger pitch or insight-led pitch for a B2B conversation
  - Draft a pitch script for a sales rep or sales enablement team
  - Differentiate a sales conversation by teaching customers something new about their business
  - Apply SAFE-BOLD to sharpen a teaching pitch before delivery

  NOT for: building the commercial insight itself (use build-commercial-insight first),
  tailoring the pitch to individual stakeholders (use tailor-pitch-by-stakeholder after),
  or diagnosing an existing pitch (use diagnose-pitch-for-commercial-teaching-fit).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/author-commercial-teaching-pitch
metadata:
  openclaw:
    emoji: "🎤"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors:
      - Matthew Dixon
      - Brent Adamson
    chapters:
      - 5
tags:
  - sales
  - b2b-sales
  - challenger-sale
  - commercial-teaching
  - pitch-authoring
  - sales-messaging
depends-on:
  - build-commercial-insight
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "commercial-insight.md (output of build-commercial-insight) containing the validated Reframe and unique strength anchor, plus target customer segment"
  tools-required:
    - Read
    - Write
    - AskUserQuestion
  works-offline: true
discovery:
  goal: "Author a Commercial Teaching pitch using the six-step choreography (Warmer → Reframe → Rational Drowning → Emotional Impact → New Way → Your Solution) and polish it with the SAFE-BOLD framework. Outputs a pitch-script.md artifact ready for delivery."
  triggers:
    - "Write a sales pitch for my product"
    - "Build a commercial teaching pitch from my insight"
    - "I need a six-step challenger pitch"
    - "How do I structure a teaching conversation for my sales team?"
    - "Draft a pitch script for a B2B sales call"
    - "Apply SAFE-BOLD to my teaching pitch"
    - "I want an insight-led pitch, not a product pitch"
  audience:
    - Sales reps and account executives building teaching-led pitches
    - Sales enablement teams creating repeatable pitch assets
    - Product marketing managers turning insights into sales narratives
    - Sales managers coaching reps on commercial teaching delivery
  prerequisites:
    - "Run build-commercial-insight first to produce a validated commercial-insight.md"
  not-for:
    - Auditing or diagnosing an existing pitch — use diagnose-pitch-for-commercial-teaching-fit
    - Building the commercial insight itself — use build-commercial-insight
    - Tailoring the completed pitch to individual stakeholder roles — use tailor-pitch-by-stakeholder
---

# author-commercial-teaching-pitch

Author a Commercial Teaching pitch using the six-step choreography and polish it with SAFE-BOLD. Takes the validated `commercial-insight.md` from `build-commercial-insight` as its primary input and outputs a `pitch-script.md` ready for delivery or enablement packaging.

---

## When to Use

Use this skill after `build-commercial-insight` has produced a validated Reframe and unique strength anchor. This skill structures that insight into a complete, deliverable six-step conversation that engages both the customer's rational and emotional response — because logic alone is rarely enough to overcome the status quo.

The output is not a product presentation. It is a teaching narrative that arrives at your solution as the natural conclusion of a story about the customer's business.

---

## Context and Input Gathering

### Load the prerequisite artifact

If `commercial-insight.md` exists in the working directory, read it now. Extract:
- The validated Reframe statement (the headline insight)
- The unique strength anchor (what only your solution can deliver)
- The target customer segment
- The quantified cost-of-inaction evidence (for Step 3)
- The blocking worldview (what the customer currently believes)

If `commercial-insight.md` does not exist, use `AskUserQuestion` to collect:
1. The Reframe candidate: the unexpected perspective the customer has not considered
2. The unique strength anchor: what your solution delivers that competitors cannot
3. Target customer segment: role, industry, size, common behavior patterns
4. Quantified evidence: data or research showing the cost of the problem or size of the opportunity

Do not proceed without these four inputs. The pitch cannot be constructed from a generic or unvalidated insight.

---

## Process

### Step 1 — Draft the Warmer

Write an opening that names 2-3 challenges you are observing at companies similar to the customer's. Draw from the target segment profile in `commercial-insight.md`.

Structure the Warmer as:
- "We've worked with a number of companies in [segment], and we've consistently seen these challenges come up: [challenge 1], [challenge 2], [challenge 3]. Is that what you're seeing, or would you add something else to the list?"

**Emotional target:** Customer feels "they get us" — understood without being interrogated.

**Why:** This establishes credibility through demonstrated domain knowledge (Hypothesis-Based Selling), not through company credentials or product claims. Customers with "solutions fatigue" respond positively because they receive informed perspective rather than having to educate you.

**Self-check:** Does the Warmer lead with hypotheses, not open-ended questions? Does it avoid any mention of your solution or company? Does it invite the customer to confirm or extend the challenge list?

**Anti-pattern:** Asking "What's keeping you up at night?" (discovery framing). Also: transitioning directly from the Warmer to your solution — this is the next step a core-performing rep takes and the one move most likely to waste the goodwill just established.

---

### Step 2 — Draft the Reframe

Write the single headline insight that connects the challenges the customer just confirmed to a problem or opportunity they had not recognized. This is just the headline — not the full explanation.

The Reframe must:
- Introduce an unexpected angle that inverts or expands the customer's current assumption
- Be stated in 1-2 sentences
- Not mention your solution or company

**Emotional target:** "Huh, I never thought of it that way before."

**Why:** The Reframe is the pivot point of the entire conversation. Without a genuine perspective shift, everything that follows is either confirming existing beliefs (no urgency) or promoting your solution prematurely (ignored). The teaching moment lives specifically here — if the customer already believed this, no teaching has occurred.

**Self-check:** Does the customer's hypothetical first reaction suggest curiosity and surprise? Or would they say "I totally agree"? Enthusiastic agreement is a failure signal. Also check: is the Reframe just the headline at this stage, or have you overloaded it with explanation that belongs in steps 3 and 4?

**Anti-pattern:** Getting enthusiastic agreement — this means the insight confirms rather than challenges the customer's worldview, and they have likely already considered solutions (possibly competitor solutions). Timidity is also an anti-pattern: "If you're going to reframe, be sure you really reframe."

---

### Step 3 — Draft Rational Drowning

Write the quantified business case for why the Reframe matters. Use data, benchmarking figures, or research to show the hidden cost of the problem or the size of the missed opportunity.

If an ROI calculator is included, it must calculate the return on solving the problem — not the return on buying your solution.

Structure the Rational Drowning as:
- Here is what this costs most companies like yours (quantified)
- Here is why the cost is larger than it appears (hidden or indirect costs)
- Here is what inaction compounds to over time

**Emotional target:** "This is real, and bigger than I thought." The customer should feel they are "drowning" — not panicked, but acutely aware of a material problem they had underestimated.

**Why:** Rational evidence is necessary to justify action, but it must be framed against the problem the customer now believes they have (from Step 2), not against your solution. The ROI in Step 3 answers: "Is it worth fixing this at all?" Step 6 will answer: "Why buy from you?"

**Self-check:** Is the ROI explicitly about the challenge the Reframe revealed — not about your product? Is the data specific enough to feel credible? Would a skeptical CFO engage with this data?

**Anti-pattern:** Presenting ROI that requires customers to first believe in your product to understand the numbers. Also: staying in Step 3 when the customer is already convinced — move to Step 4 before the emotional urgency dissipates.

---

### Step 4 — Draft Emotional Impact

Write a narrative story that places companies like the customer's in the painful scenario your data just described. The story must feel immediately familiar — the customer should recognize their own organization in it.

Structure the Emotional Impact as:
- "I understand you're a little bit different, but let me show you how we've seen this play out at similar companies..."
- [Specific scenario that maps to the customer's role, industry, and common behavior pattern]
- The scenario ends at the moment of maximum pain — the unplanned cost, the scramble, the workaround — and pauses there

**Emotional target:** "This is MY problem, not just the company's." The customer stops seeing the data as applying to others and starts replaying the scenario in their own context.

**Why:** Customers often respond to strong rational arguments with "I see what you're saying, but we're different." More data never defeats this response — because it is not a logic problem, it is an emotional connection failure. The story creates the link between the abstract problem and the customer's lived experience.

**Self-check:** Can the customer immediately place themselves in the story? Does the scenario end at the pain moment — not at the solution? Does the narrative feel specific and credible rather than generic?

**Anti-pattern:** Responding to "we're different" with more charts. More charts intensify the same failed approach. Also: making the story too polished or corporate — the roughness of a real customer situation is what makes it land.

---

### Step 5 — Draft the New Way

Write a point-by-point description of the capabilities the customer would need to adopt in order to address the opportunity or solve the problem. Frame this as what the customer needs to do differently — not what your solution does.

Structure the New Way as:
- "Here is the type of organization you would need to become to capture this opportunity / eliminate this cost..."
- [Specific capability categories: what they would track, how they would operate, what relationships they would manage differently]

**Emotional target:** "We need to change how we operate." The customer agrees conceptually to the direction of change before being introduced to any specific vendor.

**Why:** Customers must buy the concept before they buy the product. Step 5 creates the buy-in to change that makes Step 6 feel like the natural answer rather than a sales pitch. If the customer agrees "that's what we need to do" in Step 5, Step 6 becomes a question of which supplier, not whether to act.

**Self-check:** Is Step 5 still about the customer's organizational capabilities — not about your product's features? Does it describe a world-class solution abstractly before naming your company? Does it feel like aspirational vision, not a product spec sheet?

**Anti-pattern:** Rushing to name your product in Step 5. This is the most common premature close in commercial teaching. The customer must first agree to the direction of change; then they are ready to hear who can deliver it.

---

### Step 6 — Draft Your Solution

Write the specific demonstration of how your solution is better positioned than any alternative to equip the customer to act on the New Way they agreed to in Step 5. This is the first time you name your company.

Structure Your Solution as:
- "Given everything we've talked about, here's how [your solution] delivers exactly what we described..."
- Map each capability in the New Way to a specific, unique feature or differentiator of your solution
- Close by pointing to the natural next step (diagnostic, pilot, or proposal)

**Emotional target:** "And you can deliver it." Customer sees the direct line from the New Way to your specific offer.

**Why:** The hard work of Steps 1-5 creates the context in which your capabilities feel like the natural answer rather than a sales pitch. If you have correctly identified unique capabilities that were not legible before the teaching, competitors cannot easily follow. The solution is legible only to a customer who has been taught to value it.

**Self-check:** Is every capability mentioned in Step 6 mapped directly to a point from the New Way (Step 5)? Is competition still potentially viable at this stage — if yes, the earlier steps may not have sufficiently differentiated the path. Does the close feel like a logical next step, not a closing technique?

**Anti-pattern:** Introducing new capabilities in Step 6 that were not set up in Step 5. Also: presenting your full product portfolio — Step 6 should only present capabilities that map to the specific New Way from this pitch.

---

### Step 7 — Per-Step Self-Check

Before the SAFE-BOLD pass, verify the sequence:

| Step | Emotional target met? | Success signal present? | Anti-patterns avoided? |
|------|----------------------|------------------------|----------------------|
| 1 Warmer | Customer would feel understood | Engagement + reaction invited | No discovery questions, no solution preview |
| 2 Reframe | Surprise + curiosity, not agreement | "I hadn't thought of it that way" | Not timid, not explained too early |
| 3 Rational Drowning | Problem feels large and material | Quantified, CFO-credible | ROI on problem, not on product |
| 4 Emotional Impact | Customer sees themselves in story | Rueful recognition, not generic | Story ends at pain, not solution |
| 5 New Way | Customer agrees to direction of change | "That's what we need to do" | No product name, no vendor mention |
| 6 Your Solution | Natural fit between need and offer | Clear next step proposed | Only capabilities set up in Step 5 |

If any row fails, return to that step and revise before continuing.

---

### Step 8 — SAFE-BOLD Polish Pass

Score the draft pitch against the four SAFE-BOLD dimensions (developed by Neil Rackham and KPMG). Each dimension is scored on a continuum: SAFE is weak, BOLD is strong.

| Dimension | SAFE (1) | BOLD (5) | Your score | Evidence from draft |
|-----------|----------|----------|------------|-------------------|
| **Big** | Small, narrow scope | Expansive, far-reaching | | |
| **Innovative** | Follower idea, common | Leading-edge, untested | | |
| **Risky** | Easily achievable | Asks significant change | | |
| **Difficult** | Easy to implement | Hard because of scale, uncertainty, or politics | | |

**Why Difficult matters:** If the problem is easy for the customer to solve without help, there is no reason to hire you. The difficulty of the problem is what creates the need for a capable partner.

For any dimension scoring below 3:
- **Big below threshold:** Broaden the scope of the Reframe or the Rational Drowning data — show a larger pattern, a longer time horizon, or a cross-functional impact
- **Innovative below threshold:** Sharpen the Reframe — if the customer could have thought of this themselves, it is not yet a teaching insight
- **Risky below threshold:** Ensure the New Way requires meaningful organizational change — if customers can adopt the direction casually, there is no urgency to act now
- **Difficult below threshold:** Strengthen the Rational Drowning and New Way — the problem should feel genuinely hard to solve at scale, which is exactly why your solution matters

Document SAFE-BOLD scores and any targeted rewrites in the `pitch-script.md` output.

---

### Step 9 — Write pitch-script.md

Create `pitch-script.md` with this structure:

```markdown
# [Pitch Title]

**Customer segment:** [Segment from commercial-insight.md]
**Unique strength anchor:** [From commercial-insight.md]
**SAFE-BOLD scores:** Big: [X/5] | Innovative: [X/5] | Risky: [X/5] | Difficult: [X/5]

---

## Step 1: Warmer
**Emotional target:** Customer feels understood
**Script:** [Draft language]
**Success signal:** [What the rep listens for]

## Step 2: Reframe
**Emotional target:** "Huh, I hadn't thought of it that way"
**Script:** [Draft language]
**Success signal:** [What the rep listens for]

## Step 3: Rational Drowning
**Emotional target:** "This is real and bigger than I thought"
**Script:** [Draft language with quantified evidence]
**Success signal:** [What the rep listens for]

## Step 4: Emotional Impact
**Emotional target:** "This is MY problem, not just the company's"
**Script:** [Narrative story]
**Success signal:** [What the rep listens for]

## Step 5: A New Way
**Emotional target:** "We need to change how we operate"
**Script:** [Draft language]
**Success signal:** [What the rep listens for]

## Step 6: Your Solution
**Emotional target:** "And you can deliver it"
**Script:** [Draft language]
**Success signal / Next step:** [What the rep proposes]
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `commercial-insight.md` | Yes | Output of build-commercial-insight — validated Reframe, unique strength anchor, quantified cost evidence, target segment |
| Target customer segment | Yes | Role, industry, company size, common behavior patterns |
| Benchmarking or spend data | Optional | Quantified evidence for Rational Drowning — if not in commercial-insight.md, ask the user |

---

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| `pitch-script.md` | `./pitch-script.md` | Six-step pitch with per-step language, emotional targets, success signals, and SAFE-BOLD scores |

---

## Key Principles

**The supplier appears last, not first.** Steps 1-5 contain no mention of your company or product. Your solution appears only in Step 6, as the natural answer to a problem the customer now believes is urgent. "Lead to, not with."

**Emotional and rational engagement are both required.** "No one ever sold anything off a spreadsheet alone." The six-step arc is designed to take the customer to a dark place (Steps 3-4) before showing them the way forward (Steps 5-6). If either the rational or the emotional layer is missing, the pitch is incomplete.

**The ROI belongs to the problem, not to the purchase.** In Step 3, if your ROI calculator explicitly references your product, you are answering the wrong question. The customer must first believe the problem is worth solving before they will listen to why your solution is the best way to solve it.

**Step 5 is the most commonly skipped.** Reps are trained to close at the moment of maximum customer agreement. After Step 4 emotional resonance, jumping to Step 6 feels natural but is wrong — it collapses the gap between the New Way and your specific product. Let the customer agree to the concept of change before introducing who should deliver it.

**SAFE-BOLD prevents organizational watering-down.** Teaching pitches that pass through multiple internal reviewers reliably lose their edge. SAFE-BOLD exists to measure and prevent this. A pitch that produces no discomfort internally has almost certainly lost the sharpness that makes it work with customers.

---

## Examples

See `references/worked-examples.md` for two detailed worked examples:
- W.W. Grainger "Power of Planning the Unplanned" — full six-step walkthrough with Pain Chain and Parts Orphanage emotional impact techniques
- ADP Dealer Services Profit Clinics — six-step walkthrough showing how commercial teaching delivered results during a 40% market contraction

Both examples trace the full sequence from Warmer through Solution, including how each step was operationalized and what customer reactions were targeted.

---

## References

- `references/worked-examples.md` — Full walkthrough of Grainger and ADP examples

**Source:** *The Challenger Sale* by Matthew Dixon and Brent Adamson. Chapter 5 (Teaching for Differentiation, Part 2). SAFE-BOLD Framework developed by Neil Rackham and KPMG.

---

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to use, adapt, and redistribute with attribution.

Source book content is copyrighted by the authors. This skill contains no verbatim passages — all content is paraphrased, structured, and extended for agent execution.

---

## Related BookForge Skills

| Skill | Relationship |
|-------|-------------|
| `build-commercial-insight` | Run before this skill — validates the Reframe and unique strength anchor that anchors the pitch |
| `tailor-pitch-by-stakeholder` | Run after this skill — adapts the completed pitch to individual stakeholder roles and priorities |
| `diagnose-pitch-for-commercial-teaching-fit` | Alternative entry point — use to audit an existing pitch before rebuilding with this skill |
| `classify-rep-profile` | Use independently — confirms whether the rep is equipped to deliver a Challenger-style teaching pitch |
