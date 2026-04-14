---
name: diagnose-pitch-for-commercial-teaching-fit
description: Audit an existing sales pitch, deck, or call transcript against the Commercial Teaching rubric. Use this skill when you want to review your deck, diagnose why your pitch isn't working, check whether your pitch leads with solution instead of leading to it, run a commercial teaching check, get a pitch diagnostic, run a sales deck review, figure out why your pitch isn't differentiating, or check whether your pitch opens with your solution before establishing a customer problem. Detects lead-with-vs-lead-to errors, missing Reframes, Rational Drowning misfocus, teaching-into-the-desert traps, buzzword pollution, and sequence violations. Produces a scored per-step rubric with highlighted problem passages and rewrite recommendations.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/diagnose-pitch-for-commercial-teaching-fit
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors: ["Matthew Dixon", "Brent Adamson"]
    chapters: [4, 5]
tags: [sales, b2b-sales, commercial-teaching, pitch-audit, sales-enablement, challenger-sale]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "An existing pitch artifact: markdown export of a slide deck, a call transcript, a sales narrative document, or a written pitch script."
  tools-required: [Read, Write, Grep]
  tools-optional: []
  mcps-required: []
  environment: "Works offline from a provided pitch artifact. No live system access needed. Output: pitch-diagnosis.md with scored rubric, flagged passages, and rewrite recommendations."
discovery:
  goal: "Audit an existing pitch against the Commercial Teaching rubric to surface structural errors, anti-patterns, and missing elements — with specific rewrite guidance."
  tasks:
    - "Map each pitch section or slide to one of the six choreography steps"
    - "Score each step as Pass, Partial, or Fail against its specific criteria"
    - "Detect lead-with-vs-lead-to error: does the pitch open with the seller's solution before establishing customer problem?"
    - "Detect teaching-into-the-desert: does the insight anchor back to the seller's unique capabilities?"
    - "Detect missing or weak Reframe: does the pitch produce curiosity and surprise, or agreement and confirmation?"
    - "Check Rational Drowning focus: is the ROI on the customer's problem or on purchasing the solution?"
    - "Scan for buzzword pollution: leading, unique, innovative, solution, best, top, largest"
    - "Produce pitch-diagnosis.md with scored rubric, specific flagged passages, and rewrite recommendations"
  audience: "sales reps, sales enablement teams, sales operations, revenue leaders, marketing teams building sales collateral"
  when_to_use: "When a pitch exists and you want to improve it before a key meeting, after a lost deal, or as part of a systematic sales content audit"
  environment: "Pitch artifact as a document or text. Works from a deck export, transcript, or narrative script."
  not_for:
    - "Authoring a new pitch from scratch — use author-commercial-teaching-pitch instead"
    - "Evaluating pricing or negotiation tactics — those require different skills"
  quality: placeholder
---

# Diagnose Pitch for Commercial Teaching Fit

## When to Use

You have an existing sales pitch — a deck, a script, a call transcript, or a narrative document — and you want to know whether it is built to teach or built to sell. This skill applies when:

- You lost a deal and suspect the pitch led with your solution before establishing why the customer should care
- Your pitch feels like everyone else's, and you cannot explain why you are not differentiating
- Marketing delivered a deck and you are not sure it follows the right sequence
- You want to run a systematic audit of your sales collateral before a critical meeting
- Someone reviewed your pitch and said "you're just talking about yourself" — and you want to know exactly where

**The diagnostic framework:** Commercial Teaching pitches follow a six-step sequence — Warmer → Reframe → Rational Drowning → Emotional Impact → New Way → Your Solution. The seller's product does not enter the conversation until Step 6. Most pitches violate this by leading with their solution instead of leading to it. This audit locates the violations precisely.

**This skill does not author a new pitch.** It diagnoses an existing one. If you need to build a pitch from scratch, use `author-commercial-teaching-pitch`.

Before starting, confirm you have:
- A pitch artifact (deck export, transcript, or written narrative) to audit
- Enough content to identify sections or slides individually

---

## Context and Input Gathering

### Required Input

- **Pitch artifact:** A document that represents your actual pitch. Acceptable formats: markdown export of a slide deck, call transcript, written sales narrative, or capability brochure. If the pitch only exists as a live presentation, capture a written outline with slide titles and key talking points per slide.

### Observable Context

Before scoring, scan the artifact for these quick signals:

- **First 20% of content:** Does it mention your company name, product name, or offering? If yes, lead-with error is likely.
- **Presence of "About Us" or capability section early:** Almost always a lead-with indicator.
- **Buzzword count:** Search for: leading, unique, innovative, solution, best, top, largest, innovator. More than 3 occurrences in a short pitch is a pollution signal.
- **ROI or data section:** Is the ROI calculated on the customer's problem, or on buying your product?
- **Storytelling section:** Is there a moment where you describe how other companies experienced this problem? If not, Step 4 is likely missing.

### Default Assumptions

- If the pitch is a slide deck without speaker notes → audit the slide titles and visible content only; note that full scoring requires speaker notes
- If the pitch is a call transcript → treat each topic shift as a potential step boundary
- If sections are unlabeled → assign provisional step labels based on content, then flag uncertainty in the output
- If the pitch is a single paragraph → still apply the sequence test; the error pattern will be obvious

### Sufficiency Check

You have enough to proceed when:
1. You have a pitch artifact with enough content to identify what happens in the opening, middle, and close
2. You can tell what the seller is selling (at least at a category level)
3. You can tell who the customer is (at least at a role or industry level)

If the pitch is fewer than 5 sentences, ask the user to expand it or provide the full deck before continuing.

---

## Execution

### Step 1 — Load and Structure the Pitch Artifact

Read the pitch artifact in full. As you read, do not score yet — just parse.

Create a working map of the artifact's sections. For a slide deck: list each slide title. For a transcript: identify each topic shift. For a narrative: identify paragraph clusters by theme.

For each section, write a one-line summary of what that section is claiming or doing.

**Why this matters:** You cannot score choreography violations without first knowing what sequence the pitch actually follows. Most reps are not aware their pitch is out of sequence — they need the map made explicit.

---

### Step 2 — Map Sections to Choreography Steps

For each section in your working map, assign it to one of the six choreography steps, or mark it as Unclassified if it does not fit any step.

The six steps and their content signatures:

| Step | What the Content Does |
|------|-----------------------|
| 1 — Warmer | Discusses customer challenges, benchmarks, peer anecdotes. No product. Ends with a question. |
| 2 — Reframe | Introduces unexpected angle that connects challenge to a hidden problem or overlooked opportunity. Delivers surprise. |
| 3 — Rational Drowning | Quantifies the cost or size of the problem using data, charts, ROI models. |
| 4 — Emotional Impact | Tells a story about how similar companies experienced this problem. Makes it personal and recognizable. |
| 5 — New Way | Defines the capability or behavior change needed — without naming your company as the answer. |
| 6 — Your Solution | Introduces your specific offering as uniquely able to deliver what Step 5 described. |

Mark any content that is about your company (history, team, awards, logo wall, locations) as Unclassified — it does not belong in the sequence.

**Why this matters:** The mapping exposes sequence violations. A pitch may technically contain a Reframe — but if it appears after Your Solution, the choreography is broken.

---

### Step 3 — Score Each Step Against Its Criteria

For each step that appears in the pitch, assign a score: **Pass**, **Partial**, or **Fail**. For steps that are absent, mark **Missing**.

Use the detailed per-step criteria from `references/six-step-rubric.md`. The summary criteria are:

**Step 1 — Warmer**
- Pass: hypothesis-based, uses benchmarks or peer anecdotes, ends with reaction question
- Fail: opens with "what's keeping you up at night?" or company overview instead
- Fail: no customer context at all — pitch jumps to data or product

**Step 2 — Reframe**
- Pass: presents an insight the customer has not already considered; produces surprise
- Fail: customer's likely response is "I totally agree" rather than "I never thought of it that way"
- Fail: missing entirely — pitch goes from challenges directly to data or product
- Partial: mild reframe that challenges at the margins without genuine surprise

**Step 3 — Rational Drowning**
- Pass: ROI is on the customer's problem (cost of the reframe issue), not on buying your product
- Fail: ROI calculator shows "you'll save X% with our platform" — product ROI, not problem ROI
- Fail: missing or too thin — data does not disturb, only informs

**Step 4 — Emotional Impact**
- Pass: tells a story about similar companies that triggers recognition; customer sees themselves
- Fail: missing — pitch goes from data to product with no narrative bridge
- Fail: story is about your customer success cases, not about the customer's own behavior pattern

**Step 5 — New Way**
- Pass: describes solution capabilities without naming your company; customer agrees to the concept
- Fail: describes generic best practices available from any vendor (teaching-into-the-desert risk)
- Fail: accidentally names your product (premature reveal)
- Fail: missing — pitch jumps from emotional story directly to product

**Step 6 — Your Solution**
- Pass: connects your specific capabilities back to the New Way requirements; differentiation is earned
- Fail: product presentation leads the pitch (lead-with error — your solution appears in Step 1 position)
- Partial: solution is presented but connection to Step 5 is loose

---

### Step 4 — Detect Lead-With vs. Lead-To Error

Run a focused check on the opening of the pitch (first 20% of content).

**Check A — Solution-first opening:**
Does the pitch open with any of the following?
- The seller's product or platform name
- A product feature or capability statement
- A company overview or "About Us" section
- A value proposition or tagline referencing what the seller does

If yes, mark: **Lead-With Error Detected**. The pitch opens with the seller's story before establishing why the customer should care.

**Check B — First-slide diagnosis:**
For deck audits — what is on slides 1–3? If the answer is any combination of: company values, team credentials, solution capabilities, partner logos, or customer logo walls — those slides are all lead-with signals. They have no place in the opening of a Commercial Teaching pitch.

**Check C — Buzzword pollution scan:**
Search the full artifact for these terms (from Ch9 analysis of top overused pitch language): leading, unique, innovative, solution, best, top, largest, innovator, world-class, cutting-edge, state-of-the-art.

Count occurrences. More than 3 in a short pitch is a pollution signal. More than 6 means the pitch is indistinguishable from competitor materials.

Flag each occurrence with location and surrounding sentence.

**Why this matters:** Buzzwords do not differentiate — they signal sameness. Every competitor also claims to be "the leading solution." These words invite a price discussion rather than a conceptual sale. They also indicate that the pitch is leading with product identity rather than customer insight.

---

### Step 5 — Detect Teaching Into the Desert

This check addresses a subtler failure: the pitch has a real Reframe (Step 2), but the insight does not route back to capabilities that only this seller can deliver.

**The test:** For each insight or Reframe identified in Step 2, ask:

1. Does the New Way (Step 5) describe capabilities that are genuinely differentiating for this seller?
2. Can any of the seller's three largest competitors equally satisfy the Step 5 capability requirements?
3. If the customer takes this insight to bid, does the seller win — or does any qualified competitor win?

If competitors can equally satisfy the New Way requirements, mark: **Teaching-Into-the-Desert Risk Detected**.

**Manifestations to look for:**
- Step 5 describes generic technology adoption, process improvement, or organizational change that any consultant could recommend
- The insight is industry-available (customer has heard it before, just not from this rep)
- Step 6 (Your Solution) does not map cleanly to Step 5 (New Way) — there is a gap between what was described as needed and what the seller actually offers

**Why this matters:** Free consulting that benefits your competitors is the worst possible outcome of a teaching pitch. The four rules of Commercial Teaching require that every insight lead to a capability where you outperform the competition — otherwise you are educating the market on behalf of your rivals.

---

### Step 6 — Detect Missing or Weak Reframe

A separate targeted check on Step 2.

**Presence check:** Is there any moment in the pitch that introduces an unexpected angle — something the customer has not already considered? If no — the Reframe is missing. This is the most consequential single failure in the choreography.

**Quality check for present Reframes:**
- Would a customer's first reaction be "I never thought of it that way" — or "yes, exactly, that's what we're all dealing with"?
- Does the Reframe connect challenges from Step 1 to a larger problem the customer did not know they had?
- Is it delivered as a headline (creating curiosity) or as a full explanation (killing the tension)?
- Does it create mild dissonance — or does it feel like validation?

**Common Reframe failure modes:**
- Reframe describes a well-known industry problem (everyone has already heard it) → teaching at the margins
- Reframe is so gently framed it reads as agreement rather than challenge
- Reframe makes a claim the customer immediately agrees with → they already have a solution in mind → commoditization risk

Mark as: **Reframe Missing**, **Reframe Weak**, or **Reframe Effective**.

---

### Step 7 — Write the Pitch Diagnosis Report

Write the output to `pitch-diagnosis.md` in the same directory as the input artifact, or in the working directory if no artifact path is specified.

The report contains four sections:

**Section 1 — Sequence Map**

A table showing how the pitch sections map to choreography steps, with any sequence violations called out.

```
| Pitch Section | Assigned Step | Sequence Position | Notes |
|---|---|---|---|
| Slide 1: About Our Company | Unclassified | 1st | Lead-with signal — company content in opening |
| Slide 2: Our Leading Platform | Step 6 | 2nd | Solution appears at position 2 of 8 — severe lead-with |
| Slide 3: Industry Challenges | Step 1 (Warmer) | 3rd | Correct step, wrong position |
...
```

**Section 2 — Per-Step Scorecard**

```
Step 1 — Warmer:           [ Pass / Partial / Fail / Missing ]
Step 2 — Reframe:          [ Pass / Partial / Fail / Missing ]
Step 3 — Rational Drowning: [ Pass / Partial / Fail / Missing ]
Step 4 — Emotional Impact:  [ Pass / Partial / Fail / Missing ]
Step 5 — New Way:           [ Pass / Partial / Fail / Missing ]
Step 6 — Your Solution:     [ Pass / Partial / Fail / Missing ]

Lead-with error:            [ Detected / Not detected ]
Buzzword pollution:         [ N occurrences / None ]
Teaching-into-the-desert:   [ Risk detected / Safe ]
Reframe quality:            [ Missing / Weak / Effective ]
```

**Section 3 — Flagged Passages**

For each issue detected, quote the specific passage and label the problem:

```
[LEAD-WITH] Slide 1, sentence 2:
"Our platform is the leading solution for enterprise supply chain optimization."
Problem: Solution claim in opening position. Customer has not yet been given a reason to care.
Rewrite direction: Replace with a hypothesis about supply chain challenges at companies like theirs.

[BUZZWORD] Slide 3:
"Our innovative, world-class team delivers unique value."
Problem: 4 buzzwords in one sentence. These terms appear in every competitor's deck.
Rewrite direction: Replace with a specific, measurable capability or a customer outcome.

[TEACHING-INTO-THE-DESERT] Slide 6 (New Way):
"Companies need to adopt AI-powered analytics to reduce decision latency."
Problem: Any vendor with an analytics product can satisfy this requirement.
Rewrite direction: Specify a unique capability only this seller delivers — or revise Step 2 to teach an insight that naturally leads to a more differentiated capability.
```

**Section 4 — Priority Rewrite Recommendations**

Rank the top 3 changes the rep or enablement team should make, ordered by impact:

1. **Highest impact first** — typically: remove solution-first content from opening positions
2. **Second:** install or strengthen the Reframe
3. **Third:** correct the Rational Drowning focus from product ROI to problem ROI

For each recommendation, provide one concrete rewrite direction (not a full rewrite — that is `author-commercial-teaching-pitch`).

---

## Output

The primary output is `pitch-diagnosis.md` containing all four report sections.

Secondary outputs (inline in the conversation):
- A one-paragraph summary of the pitch's overall Commercial Teaching fitness
- The three highest-priority issues in plain language

The diagnosis report is not a rewrite. It is a precise diagnostic that the rep or enablement team uses to understand exactly what to fix — and why each fix matters to the customer experience.

---

## Examples

### Example 1 — Lead-With Opening

**Pitch opening:** "At Acme Corp, we are the leading provider of enterprise workflow automation. Our award-winning platform serves over 500 enterprise customers across 40 countries."

**Diagnosis:**
- Step 1 (Warmer): Fail. This is a company overview, not a hypothesis about customer challenges.
- Lead-with error: Detected. The pitch opens with the seller's identity and solution before the customer has any reason to care.
- Buzzword pollution: "leading" (1 occurrence in 2 sentences).
- Rewrite direction: Open with: "We've worked with companies similar to yours and consistently see three challenges in workflow adoption — [specific hypothesis]. Is that what you're experiencing, or would you add something?"

### Example 2 — Teaching Into the Desert

**Reframe:** "Most companies don't realize that 40% of approval bottlenecks happen outside their workflow tool — in email threads and Slack conversations. That's where decisions actually get made."

**Step 5 (New Way):** "You need a system that captures decisions wherever they happen and integrates them back into the workflow record."

**Diagnosis:**
- Reframe quality: Effective. "I never thought of it that way" is the likely reaction.
- Teaching-into-the-desert risk: Detected. The New Way describes a capability available from at least four major workflow vendors with inbox integrations. The insight does not route to a unique capability.
- Rewrite direction: Either specify what this seller does uniquely in the capture-and-integrate space, or revise the Reframe to lead to an insight where the seller's differentiation is genuinely unmatched.

### Example 3 — Missing Reframe

**Pitch structure:** Slide 1: About Us → Slide 2: Industry Challenges → Slide 3: Market Data → Slide 4: Our Solution → Slide 5: ROI Calculator → Slide 6: Next Steps

**Diagnosis:**
- Sequence map: No Reframe (Step 2) present. No New Way (Step 5) present. Pitch is: opener → warmer → Rational Drowning → solution. Three steps are missing.
- Reframe: Missing. The pitch presents challenges and data, but never introduces an unexpected angle.
- Emotional Impact: Missing. No storytelling bridge between the data and the solution.
- Impact: Without the Reframe, the customer has no reason to think this pitch differs from every competitor pitch they've seen this quarter.
- Rewrite direction: After Slide 2 (challenges), insert a Reframe slide that presents one unexpected angle the customer has not already considered. This is the single highest-impact addition.

---

## Reference Files

- `references/six-step-rubric.md` — Detailed per-step scoring criteria with pass/partial/fail indicators, failure mode examples, and the full anti-pattern quick-reference table

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

This skill is standalone (no dependencies). It diagnoses an existing pitch. To author a new pitch from scratch, use `build-commercial-insight` followed by `author-commercial-teaching-pitch`.
