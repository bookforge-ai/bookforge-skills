---
name: persuasion-content-auditor
description: |
  Audit, analyze, review, or score any persuasive content against the 6 principles of influence: reciprocity, commitment and consistency, social proof, liking, authority, and scarcity. Use when someone wants to improve their copy, check their persuasion strategy, evaluate a landing page, review a sales email, audit marketing materials, or find out which influence principles they're using or missing. Triggers on: audit my copy, review my email, is this persuasive, persuasion score, influence check, analyze my landing page, make this more persuasive, improve my conversion rate, CRO review, check my sales page, why isn't this converting, which principles am I using, what's missing from my pitch, evaluate my offer, marketing copy review, persuasion audit, influence framework review, content persuasion analysis. Input: any piece of persuasive content — sales email, landing page, marketing copy, pitch deck, product page, social ad, proposal. Output: scored audit report with per-principle ratings, evidence citations, and specific rewrite recommendations.
model: sonnet
context: 200k
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Marketing content to audit — paste directly or provide as file path"
  tools-required: [Read]
  tools-optional: [Write]
  environment: "Works from any context; content can be pasted inline or read from file"
tags: [persuasion]
---

# Persuasion Content Auditor

## When to Use

Use this skill when you have a specific piece of persuasive content that needs evaluation — a landing page, sales email, marketing copy, pitch, proposal, ad copy, or any text intended to move an audience toward an action.

This skill is appropriate when:
- Someone asks whether their content is persuasive enough
- Someone wants to know which influence principles they're applying and which they're missing
- Someone needs specific, actionable rewrites — not generic advice
- Someone is diagnosing why content isn't converting and wants a principled diagnosis

**What makes this skill valuable:** It applies all 6 scientifically validated influence principles simultaneously and scores each independently. Most content uses only 1-2 principles by accident. Intentionally applying all 6 creates compounding persuasive effect — each principle reinforces the others.

**Agent:** Before starting, confirm you have the content to audit. If the user says "audit my landing page" without providing it, ask them to paste the content or provide the file path. Do not proceed without actual content.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **The content itself:** The actual text or file to audit.
  → Check prompt for: pasted copy, quoted text, file path references
  → Check environment for: .md, .txt, .html files the user may have mentioned
  → If still missing, ask: "Please paste the content you'd like audited, or give me the file path. I'll analyze it against all 6 influence principles."

- **The intended action:** What should the reader do after consuming this content?
  → Check prompt for: CTA mentions, goal statements, "I want them to...", sign up, buy, book, download
  → If still missing, ask: "What action do you want readers to take? (e.g., sign up, buy, schedule a call) — this helps me assess whether the persuasion strategy aligns with the conversion goal."

### Default Assumptions (when context cannot be gathered)

- **Audience:** General adult consumer or B2B professional unless otherwise stated
- **Stage:** Mid-funnel content (audience is aware of the problem, not yet decided on solution)
- **Goal:** Drive a specific conversion action (signup, purchase, inquiry)

### Sufficiency Threshold

PROCEED when: you have the content text AND either the intended action (or a reasonable inference from the content).

## Process

### Step 1: Read and Understand the Content

**ACTION:** Read the entire content in full before beginning any analysis. Note the overall structure, the offer, the audience signals, and the call to action.

**WHY:** Principles interact — a strong reciprocity element early in the piece sets up authority claims later to land harder. Evaluating principles in isolation without understanding the full arc misses compounding effects and sequencing issues.

**IF** content is a file path → use Read to load it
**ELSE** → work directly from the pasted text

### Step 2: Audit Each of the 6 Principles

**ACTION:** For each principle, evaluate: Is it present? How well is it applied? What is the specific evidence from the content?

Work through all 6 in sequence. For each principle, assign a rating and capture the evidence.

**WHY:** Sequential auditing ensures no principle is overlooked. Content creators typically default to whatever persuasion style feels natural to them — often 1-2 principles — and systematically miss the others. A scored checklist surfaces blind spots that intuition misses.

Use the scoring system from [references/audit-rubric.md](references/audit-rubric.md) for detailed criteria. Summary ratings:

| Rating | Meaning |
|--------|---------|
| **Strong (3)** | Principle clearly present and well-executed with amplifiers active |
| **Weak (1)** | Principle present but underexecuted — surface-level, no amplifiers |
| **Missing (0)** | Principle entirely absent |
| **Counterproductive (-1)** | Principle is present but applied in a way that backfires |

**For each principle, document:**
1. Rating (Strong / Weak / Missing / Counterproductive)
2. Evidence — quote specific phrases or elements from the content
3. What amplifiers are present or absent (see rubric)

**Principle 1 — Reciprocity**
Look for: Does the content give something before asking? Free value (content, tools, samples, useful information), a concession structure (large ask reduced to smaller ask), or a favor that creates felt obligation.
- Amplifier check: Is the gift uninvited (stronger) or expected/requested (weaker)? Does it arrive before the ask?
- Counterproductive signal: Taking without giving, leading with demands, making the reader feel extraction is happening

**Principle 2 — Commitment and Consistency**
Look for: Does the content invite small commitments that escalate? Does it ask readers to take a stance, identify with a value, or make a micro-decision that leads naturally to the main ask?
- Amplifier check: Are commitments active (user does something) rather than passive? Written rather than verbal? Public rather than private? Self-attributed ("because you care about X") rather than externally pressured?
- Counterproductive signal: Contradicting earlier commitments, asking for large commitment before small, or implying the reader's past behavior was wrong

**Principle 3 — Social Proof**
Look for: Testimonials, user counts, case studies, ratings, logos, mentions of others using the product. Are they specific (named, detailed, with results) rather than generic?
- Amplifier check: Do the proof examples match the target reader's situation (similarity condition)? Are they deployed where readers feel most uncertain about the decision?
- Counterproductive signal: Vague testimonials, testimonials from dissimilar audiences, manufactured-feeling proof, highlighting others' success in a way that makes the reader feel behind

**Principle 4 — Liking**
Look for: Does the content build rapport? Does it demonstrate shared values, shared identity, familiarity, or compliments to the reader? Does the brand/person behind the content feel warm and relatable?
- 5 factors to check: physical attractiveness/professional polish (visuals), similarity to the reader (shared struggles/values/background), compliments or acknowledgment of the reader's intelligence/good taste, repeated familiar touchpoints, positive associations (aspirational imagery, pleasant scenarios)
- Counterproductive signal: Cold, corporate tone; condescension; overly formal language that creates distance; negative associations (imagery of failure, threat, shame)

**Principle 5 — Authority**
Look for: Credentials, expertise signals, data citations, institutional affiliations, track record evidence, visual markers of professionalism. Does the content establish WHY the source should be trusted on this specific topic?
- 3 symbol types: Titles (credentials, certifications, professional roles), visual/clothes signals (design quality, photography professionalism, brand marks), trappings (media features, client logos, scale signals)
- Amplifier check: Is authority relevant to the domain? Is there a "strategic self-deprecation" move — acknowledging a minor flaw to increase credibility on the major claim?
- Counterproductive signal: Overclaiming credentials, authority from irrelevant domain, boastfulness that triggers skepticism

**Principle 6 — Scarcity**
Look for: Limited quantity language, deadline language, exclusive access framing, or information-scarcity ("only available to X group"). Does the content create urgency that is credible rather than manufactured?
- 3 types: Limited number ("only 12 spots left"), Deadline ("offer ends Friday"), Exclusive information ("only our subscribers know this")
- Amplifier check: Is the scarcity newly introduced (more powerful than constant scarcity)? Is it demand-driven ("because demand is high...") rather than arbitrary? Is there an information-scarcity layer on top of product scarcity (the "double whammy" — 6x effect)?
- Counterproductive signal: Fake urgency the reader can see through, permanent "limited time" offers, scarcity claims that contradict other signals in the content

### Step 3: Calculate Coverage Score

**ACTION:** Sum the 6 principle ratings. Identify how many principles are "Strong" (rating of 3).

**WHY:** Coverage score reveals the overall persuasive architecture at a glance. A piece with 2 strong principles and 4 missing ones is systematically under-persuasive regardless of how well-written the copy is. The goal is not necessarily to maximize all 6 simultaneously — some audiences and contexts call for restraint on certain principles — but missing 4-5 is almost always a problem.

**Coverage Score:**

| Coverage (principles ≥ Weak) | Assessment |
|------------------------------|------------|
| 5-6 principles present | Full-spectrum persuasion — evaluate depth next |
| 3-4 principles present | Partial strategy — identify high-value gaps |
| 1-2 principles present | Thin strategy — significant opportunity |
| 0 principles present | Unpersuasive content — structural rebuild needed |

### Step 4: Identify Top 3 Improvement Opportunities

**ACTION:** Among missing or weak principles, identify the 3 that would create the most impact if added or strengthened. Prioritize based on: (a) ease of implementation, (b) fit with the content type, (c) stage of the funnel.

**WHY:** Not all missing principles have equal value. Scarcity on a thought leadership article would feel manipulative. Reciprocity on a sales email is both easy to add and highly effective. The right improvement recommendations are context-specific, not a generic checklist.

**Selection criteria:**
- For cold/awareness content: Liking and Reciprocity usually have highest ROI (lower commitment ask)
- For decision/conversion content: Social Proof, Scarcity, and Authority usually have highest ROI (reduce friction at decision point)
- For retention/re-engagement: Commitment and Consistency usually has highest ROI (leverages prior investment)

### Step 5: Generate Specific Rewrite Recommendations

**ACTION:** For each of the top 3 opportunities, produce a concrete rewrite. Do not describe what to do — show it.

**WHY:** Generic advice ("add social proof") is useless. Specific rewrites ("Add a testimonial from a [role similar to target audience] who achieved [specific result] in [specific timeframe], placed immediately before the CTA") give the content creator an actionable, near-final version they can implement immediately. Specific examples also demonstrate that you understand their content deeply, not just the framework.

**Format for each rewrite recommendation:**
- **Principle:** which principle this addresses
- **Current state:** what exists now (quote from the content or "absent")
- **Why it matters:** the mechanism — WHY adding this will increase compliance
- **Recommended addition/change:** the actual new copy or structural change
- **Placement:** where in the content this element should appear

### Step 6: Produce the Audit Report

**ACTION:** Compile findings into a structured report following the template below.

**WHY:** A structured report makes findings actionable and shareable. The content creator should be able to hand this to a copywriter or implement it themselves without needing to re-read the analysis.

---

## Output: Persuasion Audit Report

```
## Persuasion Audit Report
**Content:** [title or description of audited piece]
**Date:** [today's date]
**Intended action:** [what the content asks readers to do]

---

### Principle Scores

| Principle | Rating | Score |
|-----------|--------|-------|
| Reciprocity | [Strong/Weak/Missing/Counterproductive] | [3/1/0/-1] |
| Commitment & Consistency | [Strong/Weak/Missing/Counterproductive] | [3/1/0/-1] |
| Social Proof | [Strong/Weak/Missing/Counterproductive] | [3/1/0/-1] |
| Liking | [Strong/Weak/Missing/Counterproductive] | [3/1/0/-1] |
| Authority | [Strong/Weak/Missing/Counterproductive] | [3/1/0/-1] |
| Scarcity | [Strong/Weak/Missing/Counterproductive] | [3/1/0/-1] |
| **Total** | | **/18** |

**Overall Assessment:** [Full-spectrum / Partial / Thin / Unpersuasive]

---

### Per-Principle Analysis

#### 1. Reciprocity — [Rating]
**Evidence:** [specific quotes or elements from the content]
**Amplifiers active:** [list which amplifiers apply]
**Gap:** [what's missing or could be stronger]

#### 2. Commitment & Consistency — [Rating]
**Evidence:** [specific quotes or elements from the content]
**Amplifiers active:** [list which amplifiers apply]
**Gap:** [what's missing or could be stronger]

#### 3. Social Proof — [Rating]
**Evidence:** [specific quotes or elements from the content]
**Amplifiers active:** [list which amplifiers apply]
**Gap:** [what's missing or could be stronger]

#### 4. Liking — [Rating]
**Evidence:** [specific quotes or elements from the content]
**Amplifiers active:** [list which amplifiers apply]
**Gap:** [what's missing or could be stronger]

#### 5. Authority — [Rating]
**Evidence:** [specific quotes or elements from the content]
**Amplifiers active:** [list which amplifiers apply]
**Gap:** [what's missing or could be stronger]

#### 6. Scarcity — [Rating]
**Evidence:** [specific quotes or elements from the content]
**Amplifiers active:** [list which amplifiers apply]
**Gap:** [what's missing or could be stronger]

---

### Top 3 Improvement Opportunities

#### Opportunity 1: [Principle Name]
**Why this has high impact:** [mechanism explanation]
**Current state:** [quote or "absent"]
**Recommended change:**
> [exact copy to add or replace]
**Placement:** [where in the content]

#### Opportunity 2: [Principle Name]
**Why this has high impact:** [mechanism explanation]
**Current state:** [quote or "absent"]
**Recommended change:**
> [exact copy to add or replace]
**Placement:** [where in the content]

#### Opportunity 3: [Principle Name]
**Why this has high impact:** [mechanism explanation]
**Current state:** [quote or "absent"]
**Recommended change:**
> [exact copy to add or replace]
**Placement:** [where in the content]

---

### Summary
[2-3 sentence overall assessment: what's working, what's the biggest gap, what to do first]
```

## Key Principles

- **Score each principle independently before forming an overall view** — WHY: Overall impressions are contaminated by the strongest elements. Systematic per-principle scoring reveals blind spots that impressionistic review misses. A piece can feel polished while being structurally missing 4 principles.

- **Look for counterproductive application, not just presence/absence** — WHY: A poorly applied authority signal (overclaiming, irrelevant credentials) is worse than no authority signal at all. It triggers skepticism that undermines otherwise good elements. Detecting counterproductive usage is as valuable as detecting gaps.

- **Match amplifier conditions to context** — WHY: Amplifiers multiply the effect of each principle, but only when conditions are right. Scarcity from new shortage is more powerful than constant scarcity. Social proof from similar people outperforms proof from dissimilar audiences. Simply "adding" a principle without its amplifiers often underdelivers.

- **Specificity in rewrites beats generic advice** — WHY: "Add social proof" is not actionable. "Add a testimonial from a [specific role] achieving [specific result] in [timeframe], placed before the CTA" can be implemented in 30 minutes. Specific recommendations are the product of this skill, not general observations.

- **Sequencing matters — principles interact** — WHY: Reciprocity given early in a piece makes authority claims land harder later (the reader is already obligated and predisposed to trust). Social proof placed at the decision point reduces cognitive friction precisely when commitment anxiety peaks. The position of each principle within the content arc affects its impact.

## Examples

**Scenario: SaaS signup page audit**
Trigger: "Here's our landing page — why isn't it converting better?"
Process: Agent reads the full page copy. Reciprocity: Missing — page leads immediately with pricing and features, no value-first gift. Commitment: Weak — has a CTA but no micro-commitments (no quiz, no "see if you qualify" step). Social Proof: Strong — has customer logos, testimonials with results, user counts. Liking: Weak — corporate tone, no shared struggles, no warmth. Authority: Strong — founders cited in press, credentials listed. Scarcity: Missing — no deadline or limited access signal.
Output: Score 8/18. Top 3 opportunities: (1) Add a free tool or resource offer above the fold for reciprocity — include specific copy for a "free audit" widget. (2) Add a micro-commitment step before the main CTA — "See if [Product] is right for you" quiz. (3) Add a "beta cohort closing Friday" deadline with demand-driven explanation.

**Scenario: Cold outreach email audit**
Trigger: "My open rates are fine but replies are terrible — can you audit this email?"
Process: Agent reads the email. Reciprocity: Weak — mentions a case study but doesn't lead with it as a gift. Commitment: Missing — no small ask, jumps straight to "schedule a call." Social Proof: Missing — no evidence of results, no similar clients. Liking: Weak — template-feeling language, no demonstrated research into recipient. Authority: Strong — mentions publications and company size. Scarcity: Missing.
Output: Score 5/18. The email establishes authority (who they are) but fails to give value first, build connection, or reduce the friction of a large first ask. Top opportunity: Lead with a specific insight about the recipient's business (liking through demonstrated attention), offer it as a free observation (reciprocity), then ask for a smaller commitment than a call — "Would it be useful if I sent you the full analysis?" builds commitment before scheduling.

**Scenario: B2B proposal document audit**
Trigger: "I keep losing deals at proposal stage — audit this proposal."
Process: Agent reads the proposal. Reciprocity: Strong — includes a free discovery findings section. Commitment: Strong — proposal references agreements made in discovery call ("As you said you needed..."). Social Proof: Weak — includes two testimonials but from different industries. Liking: Strong — personalized language, references shared goals. Authority: Strong — case studies with detailed results. Scarcity: Counterproductive — says "this offer expires in 30 days" but the timeline feels arbitrary and manufactured.
Output: Score 13/18. Strongest proposal areas are authority, liking, and commitment. The scarcity claim is backfiring — it reads as a pressure tactic rather than a genuine constraint, which undermines the trust built elsewhere. Fix: Replace arbitrary deadline with demand-driven scarcity ("We can only take on 2 new clients this quarter due to onboarding capacity") and fix social proof by adding a case study from the prospect's industry.

## References

- For detailed per-principle scoring rubric with amplifier conditions, counterproductive patterns, and evidence checklist, see [references/audit-rubric.md](references/audit-rubric.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Influence Psychology Of Persuasion by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
