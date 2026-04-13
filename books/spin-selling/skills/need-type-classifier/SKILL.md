---
name: need-type-classifier
description: "Classify customer statements from sales calls as Implied Needs (problems, difficulties, dissatisfactions) or Explicit Needs (wants, desires, intentions to act). Use this skill whenever a sales rep shares something a prospect said and asks what to do next, when reviewing call notes or transcripts to identify which customer statements represent buying signals, when diagnosing whether discovery went deep enough before a demo or proposal, when building a needs log from call notes, or when a colleague says 'the prospect sounded interested — they mentioned several problems.' This skill applies Rackham's empirically-validated SPIN methodology to prevent the most common large-sale mistake: treating Implied Needs (problems) as buying signals. In large B2B sales, Explicit Needs — not Implied Needs — predict deal success. Invoke whenever any customer statement needs to be categorized, developed, or acted on in a B2B or enterprise sales context."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/need-type-classifier
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [3]
domain: b2b-sales
tags: [sales, b2b-sales, enterprise-sales, discovery, customer-needs, spin-methodology, need-development, buying-signals]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Customer statement(s) — pasted text, call-notes file, transcript excerpt, or a single verbal quote from a prospect"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set: deal-brief.md, call-notes-{date}.md, call-transcript-{date}.md, or plain text input. Agent classifies and writes output; human acts on the recommendations."
discovery:
  goal: "Determine whether each customer statement represents an Implied Need (problem/dissatisfaction) or an Explicit Need (want/desire/intention), and know exactly what to do next"
  tasks:
    - "Classify individual customer statements from a call as Implied Need, Explicit Need, or Neither"
    - "Review call notes or transcript to build a categorized needs log"
    - "Diagnose whether discovery surfaced enough Explicit Needs before moving to presentation"
    - "Determine the next recommended move for each statement (develop, convert, or capitalize)"
    - "Flag misreading of Implied Needs as buying signals in large-sale contexts"
  audience:
    roles: [account-executive, enterprise-sales-rep, sdr, solutions-consultant, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "Prospect said something in a call and the rep wants to know what it means and what to do"
      - "Post-call review of notes or transcript to log what needs were expressed"
      - "Pre-demo check: 'Do we have enough Explicit Needs to present our solution?'"
      - "Coaching: manager wants to show a rep why a call stalled despite the prospect 'agreeing to problems'"
    prerequisites: []
    not_for:
      - "Generating the actual SPIN questions (use spin-discovery-question-planner)"
      - "Drafting Benefit statements from confirmed Explicit Needs (use benefit-statement-drafter)"
      - "Negotiation tactics or pricing objections (out of SPIN scope)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: ""
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
    what_skill_catches:
      - "Correct distinction between problem statements (Implied) and desire/action statements (Explicit)"
      - "Explicit warning when reps treat Implied Needs as buying signals in large sales"
      - "Correct next-move recommendation: develop vs convert vs capitalize"
    what_baseline_misses:
      - "Conflates 'the customer agreed they have a problem' with 'the customer wants to buy'"
      - "Recommends presenting solutions immediately after hearing Implied Needs"
      - "Fails to surface the large-sale vs small-sale distinction in interpretation"
---

# Need Type Classifier

## When to Use

A customer said something on a call — or you have a batch of statements from call notes — and you need to know: is this a buying signal, a starting point, or something else?

This skill applies specifically to B2B discovery calls and enterprise sales contexts where the distinction between a customer's expressed problems (Implied Needs) and expressed desires (Explicit Needs) determines what happens next. If you are in a large-sale context (high value, multiple stakeholders, long cycle), this distinction is load-bearing: treating an Implied Need as a buying signal is the primary cause of premature solution presentations and stalled deals.

Use this skill:
- During or after a discovery call, to classify what the prospect actually expressed
- When building or updating a needs log from call notes
- Before moving to demo or proposal stage, to verify you have Explicit Needs to link capabilities to
- When coaching a rep who thinks a call went well because "the customer agreed to problems"

Do NOT use this skill to generate follow-up questions (use `spin-discovery-question-planner`) or to draft capability presentations (use `benefit-statement-drafter`).

## Context & Input Gathering

### Input Sufficiency Check

Before classifying, determine: "Do I have the customer statement(s) and enough context to apply the large-sale gate?"

### Required Context (must have — ask if missing)

- **Customer statement(s):** The actual words the customer used, not a paraphrase
  -> Check prompt for: quoted text, call-notes file, transcript excerpt
  -> Check environment for: `call-notes-{date}.md`, `call-transcript-{date}.md`, `needs-log.md`
  -> If still missing, ask: "Paste the customer statement(s) you want me to classify, or point me to the call-notes file."

- **Sale context (large vs small):** Determines whether Implied Needs count as buying signals
  -> Check prompt for: deal size, enterprise/SMB label, multi-stakeholder mention
  -> Check environment for: `deal-brief.md` (look for deal size, stakeholder count, sales cycle length)
  -> If still missing, ask: "Is this a large sale (high value, multiple decision-makers, weeks or months to close) or a small/transactional sale?"

### Observable Context (gather from environment)

- **Deal brief:** Look for `deal-brief.md` — provides company context, deal stage, stakeholder count
  -> If unavailable: proceed without company context; note the assumption
- **Prior needs log:** Look for `needs-log.md` — prior Implied/Explicit needs from previous calls
  -> If available: cross-reference to detect progression (Implied → Explicit across calls = positive signal)
  -> If unavailable: treat each statement independently

### Default Assumptions

- **Default to large-sale context** if deal size or cycle length is unspecified. This is the conservative assumption — it prevents premature solution presentation, which is the more costly error.
- **Classify based on exact words, not inferred intent.** A customer who says "our system has limitations" is expressing an Implied Need even if they seem eager. Only "we need a better system" counts as Explicit.

### Sufficiency Threshold

SUFFICIENT: Customer statement(s) + sale context (large vs small)
PROCEED WITH DEFAULTS: Statement(s) present but sale context unknown (apply large-sale gate with a note)
MUST ASK: No customer statements provided

## Process

### Step 1: Confirm the Classification Framework

**ACTION:** Before classifying, establish the two categories and their strict definitions. Apply these as written — the distinction is load-bearing.

**WHY:** The most common error is conflating these two types. A general agent (without this methodology) will treat "our current vendor is unreliable" as a buying signal. It is not — not in a large sale. The definitions must be applied with precision.

**Definitions:**

**Implied Need** — A customer statement expressing a problem, difficulty, or dissatisfaction with the current situation. The customer is describing something that is wrong, painful, or suboptimal. They are NOT expressing desire for change or intention to act.
- Structural markers: "can't cope with," "struggling with," "not happy about," "limitations," "problem with," "we're finding it difficult," "the current X is inadequate"
- Examples: "Our present system can't cope with the throughput." / "I'm unhappy about wastage rates." / "We're not satisfied with the speed of our existing process."

**Explicit Need** — A customer statement expressing a specific want, desire, or intention to act. The customer is describing something they WANT or are PLANNING TO DO, not just a problem they have.
- Structural markers: "we need," "we're looking for," "I'd like," "we want," "our goal is," "we're planning to," "we'd require"
- Examples: "We need a faster system." / "What we're looking for is a more reliable machine." / "I'd like to have a backup capability." / "We're going to overhaul our data network next year."

**Neither** — Factual statements, background information, or neutral observations that don't express a problem or a want.
- Examples: "We have 200 users." / "We've been using this vendor for three years." / "Our IT team handles procurement."

**Step 1 output:** Confirm the framework is understood before proceeding to classification.

### Step 2: Classify Each Statement

**ACTION:** For each customer statement provided, apply the definitions from Step 1. Produce a classification with supporting evidence and rationale.

**WHY:** Showing the evidence (the exact words that triggered the classification) makes the output auditable and teachable. Reps need to understand WHY a statement is Implied vs Explicit so they can hear this distinction in real time on future calls.

**For each statement, output:**
1. The statement (quoted verbatim)
2. Classification: Implied Need / Explicit Need / Neither
3. Evidence: the specific words that indicate the type
4. Rationale: one sentence explaining why

**Example classification:**

> "Our approval workflow takes forever — we lose deals because contracts sit in queue."
> - Classification: **Implied Need**
> - Evidence: "takes forever," "lose deals," "sit in queue" — describes a problem and its consequences, not a desire for a solution
> - Rationale: The customer expresses dissatisfaction and a negative outcome, but does not state a want or intention to act on it.

> "We're looking for a contract automation tool that integrates with Salesforce."
> - Classification: **Explicit Need**
> - Evidence: "We're looking for" — direct expression of a desired capability
> - Rationale: Specific want expressed; matches the structural pattern of an Explicit Need.

### Step 3: Apply the Large-Sale Gate

**ACTION:** After classifying each statement, apply the large-sale gate: if the context is a large B2B sale, check whether any Implied Needs have been mistakenly treated as buying signals or used to justify moving to presentation/demo.

**WHY:** In small sales (low value, single decision-maker, short cycle), Implied Needs ARE reliable buying signals. In large sales (high value, multiple stakeholders, long cycle), they are not. The empirical basis for this is stark: analysis of 1,406 larger sales found no relationship between Implied Needs and call success, but Explicit Needs were twice as high in successful calls. This distinction is counterintuitive — most reps and most sales training conflate the two. An agent without this methodology will incorrectly validate "the customer agreed to problems = positive signal."

**Gate logic:**

IF large-sale context:
- Flag any Implied Need where the rep seems to be treating it as a buying signal
- Include this explicit warning: "Implied Needs in large sales are a starting point, not a buying signal. A prospect agreeing to problems does not indicate readiness to buy. The number of Implied Needs you surface has no statistical relationship to success in large deals. What matters is whether you develop them into Explicit Needs."
- Identify which statements are Explicit Needs — these ARE the buying signals in large sales

IF small/transactional sale:
- Implied Needs do predict success; surfacing more problems helps
- Note this context difference explicitly

IF sale context is unknown (defaulted to large):
- Apply the large-sale warning, note the assumption

### Step 4: Generate Next-Move Recommendations

**ACTION:** For each classified statement, recommend the specific next move in the SPIN methodology.

**WHY:** Classification without a next action is an observation, not a tool. The rep needs to know what to DO — and the correct action depends entirely on which type of need they're working with. Prescribing the wrong next move (e.g., presenting a solution to an Implied Need in a large sale) is one of the most common and costly errors in enterprise selling.

**Next-move logic:**

| Classification | Large Sale | Small Sale |
|---|---|---|
| Implied Need | Develop with Implication Questions (explore consequences of the problem) | Present a solution or ask Need-payoff Questions |
| Explicit Need | Capitalize with a Benefit statement (link capability to this specific want) | Capitalize with a Benefit statement |
| Neither | No action required; gather more context | No action required |

**Develop with Implication Questions:** When a customer expresses an Implied Need, the next move is to ask questions that help the customer feel the full weight of the problem — its consequences, its ripple effects, its cost to the business. This is not about creating artificial urgency; it is about helping the customer understand the full scale of the problem so that the cost of solving it feels justified. Do not yet present solutions.

**Convert with Need-payoff Questions:** When an Implied Need has been sufficiently developed (the customer has expressed its consequences and is clearly feeling the weight of the problem), ask questions that prompt the customer to articulate what a solution would mean for them. "If you could eliminate that bottleneck, what would that mean for your team?" This converts Implied into Explicit.

**Capitalize with a Benefit:** When the customer expresses an Explicit Need and your product or service can meet it, link your capability directly to their expressed want. This is a Benefit in the SPIN sense — it is tied to a specific, customer-expressed desire, not a feature you want to highlight.

### Step 5: Produce the Classification Report

**ACTION:** Compile all classifications, large-sale gate findings, and next-move recommendations into a single structured report. Write it to `needs-log.md` (update if it exists; create if it does not).

**WHY:** A written report creates a persistent record that carries forward to question planning, benefit drafting, and call review. Without a written artifact, the classification exists only in the conversation and cannot be referenced by other skills (`spin-discovery-question-planner` reads `needs-log.md`).

**Report format:**

```markdown
# Needs Classification — {Account Name} — {Date}

## Sale Context
{Large / Small / Unknown — defaulted to large}

## Classification Results

| # | Statement (verbatim) | Type | Evidence | Next Move |
|---|---|---|---|---|
| 1 | "{statement}" | Implied Need | "{trigger words}" | Develop with Implication Qs |
| 2 | "{statement}" | Explicit Need | "{trigger words}" | Capitalize with a Benefit |
| 3 | "{statement}" | Neither | — | No action |

## Summary
- Implied Needs identified: {N}
- Explicit Needs identified: {N}
- Neither: {N}

## Large-Sale Gate Assessment
{If large sale: note whether the call has sufficient Explicit Needs to justify moving to solution presentation, or whether more development is needed.}

## Recommended Next Move
{One-paragraph narrative: what should the rep do next given this classification?}
```

## Key Principles

- **Explicit Needs, not Implied Needs, are the buying signals in large sales.** This is the single most important and counterintuitive insight in the SPIN methodology — backed by analysis of 1,406 large-sale calls. A customer agreeing to problems says nothing about whether they will buy. A customer expressing a want, desire, or intention to act is a meaningful signal. When a rep says "the call went great — they agreed they had X, Y, and Z problems," that tells you only that the call surfaced raw material, not that it advanced the deal.

- **Classify on words, not inferred intent.** "Our system is slow" is Implied even if the customer seems highly motivated. "We need a faster system" is Explicit even if the customer sounds calm. The classification depends on the grammatical and semantic form of the statement, not on the rep's gut feeling about the customer's readiness.

- **Implied Needs are raw material, not failure.** Surfacing Implied Needs is necessary — you can't develop what hasn't been uncovered. The error isn't finding Implied Needs; it's stopping there. In large sales, Implied Needs are the starting point for a development strategy, not a signal to present solutions.

- **The value equation explains the large/small split.** In small sales, the cost of the solution is low, so even a mild problem can justify a purchase. In large sales, the cost (financial, risk, disruption) is high, so a mild problem never justifies action alone. The customer must perceive the problem as large enough to outweigh the cost — and that requires development, not just identification.

- **Stay in scope.** This skill classifies and recommends. It does not generate the actual Implication Questions (that is `spin-discovery-question-planner`) or draft the Benefit statements (that is `benefit-statement-drafter`). When the classification output points to a next move, the rep or the relevant skill executes it.

## Examples

**Scenario: Post-call classification of transcript excerpt (large enterprise deal)**

Trigger: Rep shares: "Here are four things our prospect said on the call today. Did the call go well?"
Statements:
1. "Our current reporting is really painful — it takes the team 2 days to pull together the board deck."
2. "We've had compliance issues with our current data process."
3. "We're actively evaluating vendors for a new reporting platform."
4. "We have about 50 analysts who use the system."

Process:
- Statement 1: Implied Need — "really painful," "takes 2 days" = dissatisfaction with current situation. Next move: Develop with Implication Questions (what does the 2-day delay cost? who is affected?).
- Statement 2: Implied Need — "compliance issues" = problem statement. Next move: Develop with Implication Questions (what are the consequences of non-compliance?).
- Statement 3: Explicit Need — "actively evaluating vendors" = stated intention to act. Next move: Capitalize with a Benefit — this is a buying signal.
- Statement 4: Neither — factual background. No action.
- Large-sale gate: 2 Implied Needs, 1 Explicit Need. The call surfaced good raw material but is NOT ready for solution presentation yet — Statement 3 is the only Explicit Need. The rep should develop Statements 1 and 2 further before presenting capabilities.

Output: Needs classification report written to `needs-log.md`. Rep advised to plan Implication Questions for the next call and NOT lead with a product demo.

---

**Scenario: Single statement quick-check (large sale)**

Trigger: "My prospect said 'we're not happy with our current platform.' Is that a buying signal?"
Process: Classify the single statement. "Not happy with" = dissatisfaction = Implied Need. Apply large-sale gate: no, this is NOT a buying signal in a large sale. The customer has expressed a problem, not a desire for change. Next move: develop with Implication Questions.
Output: Classification report (short form). Clear warning that treating this as a buying signal would be premature — this is the error that cost the inexperienced telecom rep the deal in the book (CS-07).

---

**Scenario: Pre-demo sufficiency check**

Trigger: Rep asks: "We have a demo tomorrow. Here's our needs log from the last two calls — are we ready?"
Process: Read `needs-log.md`. Count Implied vs Explicit Needs. Apply large-sale gate: if the needs log contains only Implied Needs and no Explicit Needs, the customer has not yet expressed a want or desire that can be linked to a Benefit. A demo at this stage risks presenting Features and Advantages to a customer who has not confirmed any Explicit Need — which predicts objections and value challenges, not advancement.
Output: Pre-demo sufficiency report. If Explicit Needs are present: ready to proceed, list which capabilities can be linked to which Explicit Needs. If no Explicit Needs: recommend one more discovery call to develop the strongest Implied Need into an Explicit Need before presenting.

## References

For a quick-reference card of Implied vs Explicit Need markers with 20+ examples by selling context, see [references/need-type-reference-card.md](references/need-type-reference-card.md).

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill is standalone (no dependencies). Skills that build on it:

- `clawhub install bookforge-spin-discovery-question-planner` — Plan the Situation, Problem, Implication, and Need-payoff questions for a specific deal call (reads `needs-log.md` from this skill)
- `clawhub install bookforge-fab-statement-classifier` — Classify whether seller statements are Features, Advantages, or true Benefits (requires distinguishing Explicit Needs)
- `clawhub install bookforge-benefit-statement-drafter` — Draft Benefit statements that link product capabilities to customer-expressed Explicit Needs

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
