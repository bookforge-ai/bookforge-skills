---
name: research-argument-builder
description: Build a complete, structured research argument from a framed problem — assembling all five elements (claim, reasons, evidence, acknowledgment/response, warrant) using the Claim→Reason→Evidence chain. Use this skill when the user has a research problem or framed question and needs to construct the supporting argument that justifies their answer, has a working thesis or claim but does not know how to assemble the reasons and evidence that make it hold, needs to identify which of the five claim types (fact, definition, cause, evaluation, policy) their main claim is and what kind of evidence each type demands, wants to evaluate whether their claim is specific and significant enough to anchor an argument, cannot tell whether a statement is a reason or evidence and keeps treating soft generalizations as hard data, has evidence but cannot determine whether it meets the quality standards (accurate, precise, sufficient, representative, authoritative) their readers will apply, needs to plan their argument visually using a storyboard (claim + reasons + evidence cards) before drafting, or wants to thicken a thin argument by identifying where acknowledgments and warrants are needed. This is the hub skill for research argumentation — use it before counterargument-handler (which handles detailed acknowledgment/response), warrant-tester (which tests whether reasons are genuinely relevant to claims), and research-paper-planner (which turns the completed argument structure into a paper outline).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-craft-of-research/skills/research-argument-builder
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [7, 8, 9]
tags: [research-methodology, academic-writing, argumentation, critical-thinking, evidence-evaluation]
depends-on: [research-problem-framer]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "User's research problem statement, research question, working thesis/claim, or notes describing what they want to argue"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user should have a framed research problem (from research-problem-framer) or be able to state what they want to argue in one or two sentences"
discovery:
  goal: "Construct a complete, reader-ready research argument by assembling the five structural elements — claim, reasons, evidence, acknowledgment/response, warrant — in a logical order that answers every question a skeptical reader can predictably ask"
  tasks:
    - "Identify or sharpen the main claim and classify it by type (fact, definition, cause, evaluation, or policy)"
    - "Evaluate the claim for specificity and significance using the opposite-claim heuristic"
    - "Generate a set of reasons that support the claim, ordered logically"
    - "Distinguish reasons from evidence and identify the evidence needed to ground each reason"
    - "Evaluate available evidence against five quality criteria: accurate, precise, sufficient, representative, authoritative"
    - "Identify where acknowledgments and responses are needed and flag potential warrants"
    - "Produce a storyboard (claim + reason/evidence pairs + acknowledgment slots) ready for drafting"
  audience: "Researchers, graduate students, analysts, and professionals who have a research problem or framed question and need to assemble the argument that justifies their answer"
  triggers:
    - "User has a thesis but does not know how to build the argument around it"
    - "User's draft feels like a data dump with no argumentative structure"
    - "User conflates reasons and evidence, treating generalizations as hard data"
    - "User cannot tell whether their claim is specific or significant enough"
    - "User asks 'what kind of evidence do I need?' without knowing what type of claim they are making"
    - "User needs a logical plan for their argument before they start drafting"
    - "User asks 'is my evidence good enough?' without a quality framework to apply"
---

# Research Argument Builder

## When to Use

You have a research problem — a question plus the stakes of answering it — and you have done enough research to have a working answer. Now you need to assemble the argument that justifies that answer to skeptical readers.

A research argument is not a heated dispute. It is a cooperative inquiry: you and your readers working together to find the best answer to a question you both think matters. Your job is to anticipate every question a careful reader can ask and answer it before they can object.

Those questions reduce to five:

1. **Claim** — What do you want me to believe? What is your point?
2. **Reasons** — Why do you say that? Why should I agree?
3. **Evidence** — How do you know? Can you back it up?
4. **Acknowledgment and Response** — But what about...?
5. **Warrant** — How does that follow? What is your logic?

This skill walks you through all five elements in order, then produces a storyboard you can use as your drafting plan.

**Preconditions to verify:**

- Does the user have a framed research problem (condition + consequence)? If not, invoke `research-problem-framer` first.
- Does the user have a working answer — even a rough one — to their research question? If not, ask them to state what they think the answer is before continuing. The argument assembles around a claim; without one, there is nothing to build.

**This skill does NOT cover in full:**

- Developing detailed strategies for each objection or alternative view (use `counterargument-handler`)
- Testing whether a reason is genuinely relevant to a claim via warrant analysis (use `warrant-tester`)
- Turning the completed argument structure into a full paper outline with sections and order (use `research-paper-planner`)

## Context and Input Gathering

### Required (ask if missing)

- **The research question or problem:** What the researcher is trying to answer.
  - Check prompt for: a how/why question, a problem statement, or a framing from `research-problem-framer`
  - If missing, ask: "What is your research question — the specific thing you want to find out?"

- **The working claim:** The researcher's current best answer to the question.
  - Check prompt for: thesis statement, main argument, or any sentence that asserts something disputable
  - If missing, ask: "What do you currently think the answer is? Even a rough sentence is enough."

### Useful (gather from environment if available)

- **Notes, draft sections, or annotated sources:** May contain candidate reasons and evidence
  - Look for files like `notes.md`, `draft.md`, `outline.md`, `sources.md`, or any `.txt`/`.md` files in the working directory
  - If found, scan for claims, reasons, and data points before asking the user to supply them from scratch

- **Intended audience or field:** Determines what counts as authoritative evidence and which claim type fits
  - If not specified, ask: "Who are the readers this argument is for — a course, a scholarly field, a professional community?"

## Process

### Step 1 — Identify and Classify the Main Claim

**WHY:** The type of claim determines the type of argument you need to build and the type of evidence readers will demand. Trying to build an argument without knowing your claim type is like trying to construct a building without knowing whether it is a bridge, a house, or a dam. Each type requires different structural support.

State the main claim clearly as a single sentence (or two at most). Then classify it:

| Claim type | Core question answered | Evidence implication |
|---|---|---|
| Fact / existence | Does X exist or occur? | Observations, measurements, documented occurrences |
| Definition / classification | What kind of thing is X? | Criteria, comparison to established category, similarity/difference analysis |
| Cause / consequence | What caused X? What does X cause? | Causal mechanism, correlation + ruling out alternatives, time sequence |
| Evaluation / appraisal | Is X good or bad? Better or worse? | Explicit criteria of judgment, evidence that X meets or fails those criteria |
| Policy / action | What should be done? | Chain of conceptual sub-claims (problem exists → cause identified → solution addresses cause → solution is feasible + cost-effective) |

Most academic research produces **conceptual claims** (fact, definition, cause, or evaluation). Policy claims are **practical claims** — they require a chain of conceptual sub-arguments, not just one.

**Practical claim caution:** If the claim calls for action, it needs four sub-arguments: that the problem exists, what causes it, that the proposed solution addresses the cause, and that it is feasible and cheaper than alternatives. Do not build a policy argument as if it were a single conceptual claim.

See `references/claim-types-and-evidence.md` for worked examples of each claim type with corresponding evidence requirements.

### Step 2 — Evaluate Claim Strength: Specificity and Significance

**WHY:** A vague claim produces a vague argument. A trivial claim produces an argument readers do not think needs making. Both failures waste research. Checking specificity and significance before assembling evidence saves a complete rebuild later.

**Test 1 — Specificity**

Compare:
- Vague: "TV affects people's views of crime."
- Specific: "Graphic violence on local TV news leads regular viewers to overestimate neighborhood crime rates by up to 150 percent."

The specific version gives readers a richer set of concepts to interrogate. It also tells you exactly what evidence you need.

**How to sharpen specificity:** Write a working version of the claim with these two additions:
- An *although* clause acknowledging the main qualification readers might raise: `Although [widely held view you are challenging or limiting condition], [your claim]...`
- A *because* clause forecasting your main reason: `...[your claim] because [key reason].`

This is not your final draft claim — it is a working claim that makes your argument's logic explicit.

**Test 2 — Significance (opposite-claim heuristic)**

Flip your claim to its opposite. If the opposite seems obviously false or trivially unimportant, readers will not think your original claim needs arguing.

- Original: "Hamlet is not a superficial character." Opposite: "Hamlet is a superficial character." — Obviously false to anyone who has read the play. This claim does not need an argument.
- Original: "Graphic TV violence distorts viewers' risk perception." Opposite: "Graphic TV violence does not distort viewers' risk perception." — Contestable. Worth arguing.

**Significance proxy:** Ask — if readers accept this claim, how many other beliefs must they change? More belief-revision required = more significant claim.

### Step 3 — Generate Reasons and Order Them

**WHY:** Reasons are the logical spine of the argument. They are the assertions that, when placed between the claim and the evidence, explain *why* the evidence supports the claim. Without well-ordered reasons, an argument is a pile of data — readers cannot follow the logic even if they accept each individual fact.

**Key distinction — reasons vs. evidence:**

- **Reason:** A statement you think up. You use your mind to generate it. It explains *why* the claim follows. "We should leave — *it looks like rain*." (reason)
- **Evidence:** Data that exists in the world. You have to go find it. It anchors a reason in fact. "Barometric pressure has dropped 15 millibars in the past two hours." (evidence)

The direction of dependency is: reasons are *based on* evidence. Evidence does not *follow from* reasons.

**How to generate reasons:**

1. Ask: "Why should readers believe my claim?" Write every answer you can think of.
2. Ask for each answer: "Is this a reason I am asserting, or a piece of data I found?" Sort accordingly.
3. Check whether soft generalizations are reasons masquerading as evidence. "A majority of students leave college with a crushing debt burden" is a reason — it is a general assertion that still needs hard data to support it.

**Ordering reasons:**

Arrange reasons in a logical sequence — not a random list, not chronological unless the argument is about a sequence of events. Read just the reasons, without the evidence, to see if their order makes sense. If not, try other orders until the logical flow is clear.

### Step 4 — Distinguish Evidence from Reports of Evidence

**WHY:** Researchers almost never present the evidence itself — they present reports of it. A data table, a quoted passage, a case study description, a cited statistic: these are representations of evidence, shaped by those who collected and compiled them. Acknowledging this gap is not academic pedantry; it is what allows you to assess how far you are from the original data and how much trust you can ask readers to place in your report. The further you are from the original data, the more you must justify the chain of custody.

**The test:** Can readers plausibly ask "How do you know that?" more than once before reaching unquestionable bedrock? If yes, you have not yet reached evidence — you are still in the chain of reasons.

- Claim: "Higher tuition is harming educational access."
- Reason 1: "College has become unaffordable for low-income families."
- Soft reason 2 (treated as evidence): "Most students graduate with crushing debt." — *readers can still ask "How do you know?"*
- Harder evidence: "In 2013, 70 percent of students borrowed for college, averaging $30,000 in loans." — *harder to question, but still a report of data collected by someone else*

**Practical rule:** Cite as close to the original source as possible. When you use secondary sources, acknowledge it and explain why you could not get closer to the primary data.

### Step 5 — Evaluate Evidence Quality

**WHY:** Evidence that fails any of the five quality criteria will be challenged by careful readers, and even one failed criterion can discredit an otherwise strong argument. Running this checklist before drafting surfaces gaps early, when fixing them is still feasible.

The five criteria:

| Criterion | Question to ask | Common failure |
|---|---|---|
| **Accurate** | Is this data reported correctly and completely? | Misquotation, selective omission, rounding errors |
| **Precise** | Is it specific enough to mean something? | Vague quantities: "a great deal," "high probability," "many" |
| **Sufficient** | Is there enough evidence to support the reason? | One quotation or one number for a broad claim |
| **Representative** | Does it reflect the full range of the relevant data? | Cherry-picking, small unrepresentative samples |
| **Authoritative** | Is the source one readers will accept without question? | Wikipedia, uncited generalizations, non-expert opinion |

Apply this screen to every piece of evidence before adding it to your storyboard. Evidence that fails a criterion is not automatically disqualifying — but you must acknowledge the weakness and either supplement it or qualify the reason it supports.

See `references/evidence-quality-rubric.md` for detailed guidance on each criterion with cross-field examples.

### Step 6 — Identify Where Acknowledgments and Warrants Are Needed

**WHY:** An argument that only presents its own case looks one-sided. Careful readers will question every element, and if you have not anticipated their objections, they conclude you have not thought hard enough. Acknowledging objections before readers raise them, and responding to them, is what distinguishes scholarly argument from advocacy. Warrants — the general principles connecting a reason to a claim — are needed specifically when readers might accept a reason as true but deny it is *relevant* to the claim.

**Acknowledgment slots:** For each reason, ask: "What will readers say against this reason?" Identify the two or three most important objections or alternatives and note where you will acknowledge and respond to them.

**Warrant check:** For each reason→claim connection, ask: "Could a reader accept this reason as true but still deny it supports my claim?" If yes, you need a warrant — a general principle that makes the logical connection explicit.

Example: "We face higher health costs *because* the hard freeze line is moving north." A reader might accept both as true but not see the connection. The warrant: "When an area has fewer hard freezes, diseases carried by subtropical insects become more prevalent, raising medical costs." The warrant states the general principle that makes the specific reason relevant to the specific claim.

**When to state warrants explicitly:** Only when readers in your field might ask how a reason is relevant, or when you are explaining your field's reasoning to a general audience. Do not state warrants that your readers already take for granted — this wastes their time and can seem condescending.

For detailed warrant development and testing, use `warrant-tester`.
For detailed acknowledgment and response strategies, use `counterargument-handler`.

### Step 7 — Build the Storyboard

**WHY:** The storyboard externalizes the logical structure of the argument before you write prose. When the structure is on paper (or screen), you can see whether the reasons are in the right order, whether each reason has enough evidence, and where the acknowledgment gaps are — all without being tangled in the sentence-level decisions of drafting. Fixing the structure at this stage costs minutes; fixing it in a full draft costs hours.

Produce a storyboard with this format:

```
MAIN CLAIM: [one to two sentences]
Claim type: [fact / definition / cause / evaluation / policy]

REASON 1: [one sentence]
  Evidence: [source or data type needed]
  Evidence quality check: [any concerns with accuracy, precision, sufficiency, representativeness, authority]
  Acknowledgment needed: [yes/no — brief description of the objection]

REASON 2: [one sentence]
  Evidence: [source or data type needed]
  Evidence quality check: [any concerns]
  Acknowledgment needed: [yes/no]

[continue for each reason]

WARRANTS NEEDED: [list reason→claim connections that require a stated warrant]
```

Read through the reasons alone, without the evidence, to verify logical order. If the sequence does not make sense, reorder before finalizing.

## Examples

### Example 1 — Undergraduate humanities paper

**Input:** "My paper argues that Shakespeare's *Hamlet* develops the theme that indecision is more destructive than action, even wrong action."

**Step 1 — Claim classification:** Evaluation claim — judging *Hamlet* against a criterion (indecision as a form of destruction).

**Step 2 — Specificity/significance check:**
- *Although* clause: "Although Hamlet is often read as a play about moral paralysis caused by excessive thought..."
- *Because* clause: "...indecision is more destructive than action because every delay Hamlet makes produces a concrete death he could have prevented."
- Opposite: "Indecision in *Hamlet* is not more destructive than action." — Contestable. Worth arguing.

**Step 3 — Reasons:**
1. Each time Hamlet delays, the direct result is a preventable death (Polonius, Ophelia, Laertes, Gertrude, himself).
2. The characters who act decisively — Fortinbras, Laertes, even Claudius — achieve their immediate objectives.
3. Hamlet explicitly diagnoses his own problem as over-thinking, not lack of moral clarity.

**Step 4/5 — Evidence check:**
- Reason 1 needs: textual evidence from specific scenes (Acts 3–5), showing causal chain from delay to death.
- Reason 2 needs: textual examples of decisive action and its outcomes; must be *representative* (not cherry-picked scenes).
- Reason 3 needs: direct quotations from Hamlet's soliloquies; accuracy check — quote completely, not out of context.

**Storyboard fragment:**

```
MAIN CLAIM: In Hamlet, indecision is more destructive than action because
every delay produces a preventable death while decisive action — however
morally compromised — consistently achieves its objective.
Claim type: evaluation

REASON 1: Each of Hamlet's delays directly precedes a death he could have prevented.
  Evidence: Scene-by-scene textual analysis (Acts 3–5)
  Quality: Sufficient only if all major deaths are covered; representative
  Acknowledgment needed: Yes — "Hamlet could not have acted without more information earlier"
```

---

### Example 2 — Policy research

**Input:** "I want to argue that universities should require a one-semester research methods course for all undergraduates."

**Step 1 — Claim classification:** Policy claim — requires a chain of sub-arguments.

**Step 2 — Sub-claims needed:**
1. Most undergraduates currently lack basic research skills (fact)
2. The lack is caused by no structured instruction in research methodology (cause)
3. A required methods course would close that gap (cause/consequence)
4. The course is feasible and its benefits outweigh its costs (evaluation)

**Step 3 — Reasons for sub-claim 1:**
- Surveys show graduates cannot evaluate source credibility (fact sub-claim)
- Employers report new hires struggle to conduct independent research (fact sub-claim)

**Step 4/5 — Evidence:**
- Employer survey data: check *authoritativeness* (peer-reviewed or institutional?) and *representativeness* (industry range, not one sector)
- Graduate skills assessments: check *precision* (what exactly was measured, not just "critical thinking")

---

## Output

Produce a written storyboard following the format in Step 7, then provide:

1. **Claim diagnosis:** type, specificity assessment, significance check result
2. **Reasons list:** ordered sequence, with reason/evidence distinction confirmed for each
3. **Evidence inventory:** what you have, what you still need, quality concerns flagged
4. **Acknowledgment map:** where objections are anticipated and what the responses will cover
5. **Warrant flags:** any reason→claim connections that need a stated principle

If critical evidence is missing: name exactly what data type would fill the gap and where the researcher might find it. Do not recommend building the argument on soft reasons in place of unlocated evidence.

## Anti-Pattern Quick Reference

| Anti-pattern | Signal | Fix |
|---|---|---|
| Soft reason treated as evidence | "Most students..." "Many researchers..." — no source, no data | Ask "How do you know?" until you reach unquestionable data; cite the source |
| Policy claim without sub-argument chain | Single claim: "We should do X" | Break into 4 sub-claims: problem exists, cause identified, solution addresses cause, feasible + cheaper |
| Vague claim | "Technology affects education" | Apply *although/because* template to force specificity |
| Evidence fails opposite-claim test | Opposite claim is obviously false | The original claim is not worth arguing; sharpen or change the claim |
| Representative failure | One or two examples for a broad claim | Either narrow the claim to match the evidence or gather a representative sample |
| Warrant gap | Reason is true but readers say "so what?" | State the general principle that makes the specific reason relevant to the specific claim |

## References

- `references/claim-types-and-evidence.md` — Five claim types with worked examples and corresponding evidence requirements per type
- `references/evidence-quality-rubric.md` — Detailed guidance on all five evidence quality criteria with cross-field examples and failure modes

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Craft of Research, 4th Edition by Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, William T. FitzGerald.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-research-problem-framer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
