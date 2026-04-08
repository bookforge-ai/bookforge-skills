---
name: research-paper-planner
description: "Build a storyboard-based plan for a research paper and turn it into a first draft. Use this skill when the user has assembled a research argument — a main claim with supporting reasons, evidence, and acknowledgments — and now needs to organize it into a coherent, reader-ready structure before writing. Triggers include: user has a thesis and evidence but does not know how to order the sections; user suspects their draft is organized as a research narrative (what they found first) rather than as an argument (what readers need); user's draft summary-hops across sources without asserting their own claim (patchwork writing); user wants a working introduction sketch to start drafting; user is staring at a blank page and cannot begin; user needs to decide where to state their main point — end of introduction or end of paper; user wants to know whether to order reasons by importance, complexity, familiarity, or contestability. This skill does NOT build the underlying argument from scratch — use research-argument-builder for claim, reason, evidence, acknowledgment, and warrant assembly before using this skill."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-craft-of-research/skills/research-paper-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [12]
tags: [research-methodology, academic-writing, paper-planning, drafting, organization]
depends-on: [research-argument-builder]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "User's assembled argument: main claim (point), supporting reasons, evidence per reason, and any acknowledgments of objections"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user supplies their argument in text form or answers guided questions"
discovery:
  goal: "Translate a research argument into a sequenced storyboard — one page per section — that the user can draft from; detect and correct the three structural anti-patterns before drafting begins"
  tasks:
    - "Verify the argument is assembled (claim + reasons + evidence); redirect to research-argument-builder if not"
    - "Sketch a working introduction: context summary, gap statement, So what? consequence, and tentative main point"
    - "Identify 4-6 key concepts that must run through every section"
    - "Plan the body: background page, one storyboard page per major reason, suitable ordering heuristic"
    - "Plan each section: section point at top, evidence placement, acknowledgments, warrants, and section summaries if needed"
    - "Sketch the conclusion: restate point, articulate significance"
    - "Diagnose the three flawed-plan anti-patterns: Research Journey Narrative, Source Patchwork, Assignment-Prompt Order"
    - "Produce a draft protocol: quick vs. careful drafting guidance, keyword tracking, heading strategy"
  audience: "Researchers, students, analysts, and professionals who have a completed argument and need to build a reader-oriented structure before writing"
  triggers:
    - "User has a claim and reasons but does not know how to sequence sections"
    - "Draft organizes events in the order they occurred to the researcher, not by reader need"
    - "Draft reads as a tour of sources rather than an assertion of the researcher's own view"
    - "User copied assignment-prompt language into the opening paragraph"
    - "User cannot decide whether to state the main point early or late"
    - "User is stuck at the blank page and cannot begin drafting"
---

# Research Paper Planner

## When to Use

You have a research argument — a main claim supported by reasons, with evidence for each reason and responses to likely objections. The argument exists; what you need now is a reader-oriented plan for presenting it.

A plan is not the same as an argument. Your argument captures what you know. Your plan arranges that knowledge into the order that helps *readers* follow, evaluate, and accept it.

This skill guides you through five planning moves, then helps you turn the plan into a draft.

**Preconditions to verify:**

- Does the user have a main claim (point/thesis) and at least two supporting reasons? If not, invoke `research-argument-builder` first, or ask the user to state their claim and reasons before continuing.
- Does the user know their intended audience? Ordering decisions depend on what readers already know and believe.

**This skill does NOT cover:**

- Building the claim, reasons, evidence, or acknowledgments from scratch (use `research-argument-builder`)
- Writing the final polished introduction or conclusion (see chapter 16 of the source)
- Incorporating and citing sources (separate skill)

---

## Context and Input Gathering

### Required (ask if missing)

- **Main claim (point):** The thesis sentence — what the whole paper asserts.
  -> Ask: "In one or two sentences, what is the main claim your paper will defend?"

- **Supporting reasons:** The major reasons why the claim is true — these become sections.
  -> Ask: "What are the two to four main reasons a skeptical reader should accept your claim?"

- **Evidence per reason:** Data, examples, cases, or quotations that support each reason.
  -> Ask: "For each reason, what is your strongest evidence?"

### Useful (gather if present)

- Acknowledgments of objections and responses to them
- The field or discipline (affects ordering conventions and heading norms)
- Deadline and draft length constraints (affects depth of storyboard)

---

## Execution

### Step 1 — Sketch a Working Introduction

**Why:** You need a starting place that orients both you and your readers. A working introduction is not polished writing — it is a map of your opening move. Most writers revise it substantially; that is expected. Writing it now prevents you from drifting during drafting.

The working introduction has four parts, sketched in this order on the first storyboard page:

**1a. Context: summarize only the most relevant prior work**

Write a brief summary (even just bullet notes) of the sources you intend to challenge, modify, or build on. Order them in a way that is useful to readers — chronologically, by significance, by point of view — not in the order you read them and not exhaustively.

> Example: For a paper on concussion risk in youth sports, note the three major epidemiological studies, ordered from earliest population-level finding to most recent biomechanical evidence.

Omit marginal sources. An account of sources that are only loosely related wastes reader attention and dilutes your framing.

**1b. Gap statement: rephrase your question as a flaw or gap in that prior work**

Transform your research question into a statement of what the existing literature fails to explain.

Pattern: "Few of these researchers, however, have explained [your question restated as an absence]."

> Example question: "Why do female athletes under eighteen sustain concussions at nearly twice the rate of male athletes in the same sports?"
> Gap statement: "That research reveals little about the *causes* of this discrepancy."

**1c. Consequence (So what?): sketch why readers cannot afford to ignore this gap**

Even a rough answer is enough to start. Ask: "Until we understand [your gap], we cannot know [more important thing]."

> Example: "Until we understand why female athletes suffer proportionally more concussions, we cannot know the most effective ways to protect them."

If you cannot articulate a consequence at all, pause here. A gap with no consequence is a private curiosity, not a research problem. (If this is the sticking point, consult `research-argument-builder` for the So What? cascade.)

**1d. Main point placement — choose one:**

- **State your claim at the end of your introduction.** This puts readers in charge: they know the problem and the answer, so they can read selectively, challenge you earlier, and remember your argument longer. This is the default preference for most readers and most fields.
- **Reserve your claim for the conclusion.** Use this if building suspense is a disciplinary convention or if your argument only makes sense after the reader has moved through all the evidence. You still need a "launching sentence" at the end of your introduction that previews the key concepts.

> Note: Stating the claim early does not bore readers. If the question is interesting, readers want to see how well you can answer it.

Place your tentative main point at the bottom of the introduction page. You can move it later.

---

### Step 2 — Identify Key Concepts That Will Run Through Your Paper

**Why:** Readers experience a paper as coherent when a small set of concepts recurs across all sections. Without shared key terms, sections feel disconnected even if each section is internally sound.

From your main claim and gap statement, circle four to six words or phrases that name the central concepts your paper depends on.

> Example (immigration and employment paper): employment, job satisfaction, recent Southeast Asian immigrants, cross-cultural, length of residence, prior economic level.

These are not your topic's general vocabulary. They are the specific terms tied to your particular question.

- Write these key concepts at the top of every storyboard page. They are your coherence anchor.
- If you cannot find four to six distinct terms, your claim may be too general. Review your question.
- Check after drafting: does each section use most of these terms? Sections that do not may belong elsewhere or not at all.

---

### Step 3 — Plan the Body

**Why:** The order you assembled your argument follows your research logic. The order your draft follows must serve your readers' cognitive needs. These are rarely the same.

**3a. Sketch a background page (if needed)**

After the introduction page, add a storyboard page for necessary background: definitions of key terms, delimitation of scope, review of a major prior position, historical or social context. Keep it short. Background that exceeds what readers need to follow your argument is delay, not context.

**3b. Create one storyboard page per major reason**

At the top of each page, write the point that the section supports, develops, or explains. This point is almost always one of your supporting reasons. Label it explicitly — "This section argues that..." — even if you delete that label from the final draft.

**3c. Choose a body-ordering heuristic**

When you are unsure how to sequence your reasons, choose from the following eight options. The first two are based on your topic; the remaining six are based on your readers' knowledge and understanding:

| Heuristic | Use when |
|---|---|
| **Part-by-part** | Your topic divides naturally into components; deal with each component in an order that reflects their functional relationships or hierarchy. |
| **Chronological** | Earlier to later, or cause to effect — the simplest option when sequence is intrinsic to the subject. |
| **Short to long, simple to complex** | Readers prefer to settle simple issues before working through complex ones. |
| **More familiar to less familiar** | Readers prefer to read about known territory before venturing into new ideas. |
| **Less contestable to more contestable** | Start with what readers already accept; move toward claims they are more likely to resist. |
| **More important to less important** | Readers prefer important reasons first, but those reasons may have more impact if they come last — weigh both. |
| **Earlier understanding to prepare for later understanding** | Some concepts, definitions, or events must be understood before other sections make sense. |
| **General analysis to specific applications** | Readers need the overall position before they can evaluate how it applies to particular cases, texts, or situations. |

These principles often cooperate. A familiar reason is usually also short and simple. But they can conflict: a crucial reason may be the least familiar. When they conflict, prioritize the principle that most directly serves your readers' ability to follow your core argument.

Mark your chosen principle at the top of each section page with a word that signals the ordering: *First ... Second ... Later ... More important ... A more complex issue ... As a result ...* These markers are for your benefit during drafting; revise or remove them in the final draft.

---

### Step 4 — Plan Each Section and Subsection

**Why:** A section point at the top of a storyboard page is a claim. Like all claims, it needs support. Planning section internals before you draft prevents you from filling a section with whatever material you happened to find, rather than with evidence organized around the section's specific assertion.

For each section page, add:

**4a. Key terms for this section**

From your global key concepts, circle the two or three that uniquely distinguish *this* section from all others. They should appear in the sentence stating the section point. If you cannot find terms that distinguish this section, the section may not contribute independently to your argument.

**4b. Evidence placement**

List the evidence that supports this section's point. If you have multiple evidence items:
- Group items of the same kind together
- Order groups in a way that is logical for readers (not the order you found them)
- Note where you must explain the evidence — its source, reliability, or exact connection to the section's point

**4c. Acknowledgments and responses**

Anticipate the objection most likely to arise in this section. Sketch a response. Responses can be sub-arguments with their own claims, reasons, and evidence.

**4d. Warrants (when needed)**

If readers might not see why a reason supports your claim, add a warrant before the reason. A warrant makes explicit the principle that connects evidence to claim.

> Without warrant: "Most Oxford University students in 1580 signed documents with only their first and last names, so most were commoners."
> With warrant: "In late sixteenth-century England, when someone was not a gentleman but a commoner, he did not add 'Mr.' or 'Esq.' to his signature. Most Oxford University students in 1580 signed documents with only their first and last names, so most must have been commoners."

State the warrant *before* the reason and claim — not after. If readers might question the warrant itself, add a brief argument supporting it.

**4e. Section summaries (long or fact-heavy papers)**

If your paper is long and dense with dates, names, or numbers, end each major section with a one- or two-sentence summary: "This section has established [X]. The argument so far supports [Y]." Cut these from the final draft if they feel clunky; they serve drafting more than reading.

---

### Step 5 — Sketch a Working Conclusion

**Why:** Knowing where you are heading before you start keeps you from discovering your conclusion only after you have written 5,000 words pointing somewhere else.

On the final storyboard page:

1. **Restate your main point.** Not word for word — restate it in light of everything the body has established.
2. **Articulate significance.** Return to the "So what?" question from your introduction. Now that you have argued the point, what does the reader understand about a larger issue that they could not before? What should they do or think differently?

If you still cannot articulate significance, leave a placeholder and return to it after drafting. The act of drafting often surfaces the answer.

---

## Diagnosing the Three Flawed-Plan Anti-Patterns

Before you begin drafting, run these three diagnostic checks. First drafts organized around any of these three patterns require significant reorganization — catching them now costs far less than catching them after drafting.

### Anti-Pattern 1: Research Journey Narrative

**What it is:** The paper follows the order in which you conducted the research — what you found first, the dead ends you hit, the problems you overcame — rather than the order that serves readers.

**Diagnostic signals:** Scan your storyboard for language that refers to *how you did the research* rather than *what the research shows*:
- "The first issue I investigated was..."
- "Then I compared..."
- "Finally, I concluded..."
- Sections labeled by research activity ("Literature Review," "Data Collection") rather than by the argument being made

**Correction:** Reorganize around the elements of your argument: your claim and the reasons that support it. Readers do not need to know how you found the answer; they need to be persuaded by the answer itself.

---

### Anti-Pattern 2: Source Patchwork

**What it is:** The paper strings together quotations, summaries, and paraphrases of sources without asserting your own analysis. Structure follows the sources; your voice is absent.

**Diagnostic signals:**
- Section points at the top of storyboard pages name what a source says rather than what *you* claim
- Key terms running through the paper are the same as those in one or more major sources — you may be mimicking their organization rather than building your own
- Paragraphs begin with a source name rather than your claim
- You could swap two sections without changing the argument because no section has a distinct, necessary contribution

**Correction:** Rewrite each section point in your own analytical language. Your sources are evidence *for* your reasons; they do not *constitute* your reasons. If the key terms in your plan match a source's key terms, ask: am I making my own argument or summarizing theirs?

Note: Patchwork writing is especially common when most research is done online and cutting-and-pasting is easy. Readers recognize it, and it invites charges of plagiarism.

---

### Anti-Pattern 3: Assignment-Prompt Order

**What it is:** The paper's structure echoes the language or sequence of the assignment prompt, substituting the instructor's framing for your own argument.

**Diagnostic signals:**
- Opening paragraph contains phrases lifted from the assignment
- Sections follow the order of items listed in the prompt
- The paper compares Subject A and Subject B in two sequential halves (one half on A, one half on B) — a structure imposed by the assignment's compare-and-contrast framing rather than by conceptual logic

> Example: An assignment asks you to "compare Freud and Jung on the imagination and the unconscious." The flawed response organizes into Part 1 (Freud) and Part 2 (Jung), producing two disconnected summaries. The corrected response breaks the topic into conceptual parts — definitions of the unconscious, mechanisms of imagination, therapeutic implications — and orders those parts by reader need.

**Correction:** Break the prompt's topics into their conceptual elements. Order those elements in the way that best serves your readers' understanding of your argument.

---

## Turning the Storyboard into a Draft

### Draft in the mode that works for you

- **Quick drafting:** Let words flow. Skip quotations and data you will plug in later. When you cannot remember a detail, insert `[?]` and keep writing. Do not stop to perfect a sentence. Start early enough to leave time for revision.
- **Careful drafting:** Get each sentence right before writing the next. Requires a detailed storyboard or outline. If this is your mode, invest more time in Steps 3 and 4 above before you begin.

Most writers draft quickly and revise carefully. But either mode works — the important thing is that you draft *now*, not after conditions are perfect. The perfect paper has never been written and never will be.

### Use keywords to stay on track

Keep your four to six key concepts visible as you draft. Check periodically: does each section use most of them? If a section wanders, return to the key terms and the section point at the top of its storyboard page.

If you find yourself following a trail that diverges from your plan, follow it for a while — you may be discovering something. But return to the storyboard afterward and decide whether the discovery belongs in this paper.

### Use headings during drafting

Even if your field does not use headings in the final paper, use them while drafting. Headings built from section-specific key terms (e.g., "Sam Houston as a Hero in Newspapers Outside of Texas") show the structure at a glance and keep each section anchored to its point. Delete them before final submission if convention requires.

### On procrastination and writer's block

If you cannot start at all, the cause is usually one of three things:

- **Intimidation by the whole:** The task feels too large to begin. Solution: divide the storyboard into the smallest possible steps — one page, one section point. Work only on that step.
- **Goals set too high:** You are trying to draft a polished sentence when a rough one will do. Solution: lower the bar explicitly. Tell yourself you are writing notes to think with, not sentences for readers. Every researcher compromises perfection to get the job done.
- **Perfectionism sentence by sentence:** You cannot move to the next sentence until the current one is perfect. Solution: write informally, remind yourself the draft is for your benefit, and accept that revision is where polishing happens.

If you are stuck but have time, set the draft aside for a day or two. Some writer's block is the subconscious integrating material. Return to find the path clearer.

---

## Worked Examples

### Example A: Sports Science Paper

**Claim:** The higher concussion rate among female youth athletes is due primarily to differences in protective equipment standards and monitoring protocols, not to physiological factors alone.

**Working introduction sketch:**
- Context: Three epidemiological studies (ordered chronologically) establishing the rate disparity
- Gap: "That research reveals little about the causes of this disparity"
- Consequence: "Until we understand the causes, we cannot design effective protective interventions"
- Main point: stated at end of introduction

**Key concepts:** concussion rate, female youth athletes, protective equipment, monitoring protocols, physiological factors

**Body ordering chosen:** Less contestable to more contestable — the equipment-standards argument is more data-supported; the monitoring-protocols argument is more contested among practitioners.

**Conclusion sketch:** Restate claim. Significance: policy recommendations for equipment standards and mandatory monitoring protocols in youth sports governing bodies.

---

### Example B: History Seminar Paper

**Claim:** The Alamo story became a national legend not because of its military significance but because of how Texas boosters and Eastern journalists co-constructed it in print media between 1840 and 1880.

**Working introduction sketch:**
- Context: Historians who have documented the Alamo narrative (ordered by significance to the argument)
- Gap: "Few of these historians, however, have explained *why* the story became so important in national mythology"
- Consequence: "Until we understand how such stories become national legends, we cannot understand what values a culture selects to represent itself"
- Main point: reserved for conclusion (disciplinary convention in narrative history)

**Body ordering chosen:** Chronological (1840s newspaper coverage → 1860s dime novels → 1880s monumental histories) because sequence is intrinsic to how the narrative evolved.

---

## Quick Reference: Storyboard Page Structure

```
PAGE: [Section name]
Key concepts active here: [2-3 from your global list]
Section point: [One sentence asserting what this section claims]
Ordering signal: [First / More important / Earlier understanding needed / etc.]

Evidence:
  - [Item 1 — note source and what it proves]
  - [Item 2 — note source and what it proves]
  (group by kind; order by reader logic)

Warrant needed? [Yes/No — if yes, state it before reason]
Acknowledgment: [Likely objection]
  Response: [Sub-claim + reason + evidence]
Section summary (if long paper): [One sentence — what has this section established?]
```

For deeper detail on the final polished introduction and conclusion structure, see references/working-introduction-conclusion.md.

---

## References

- `references/working-introduction-conclusion.md` — Full structure for final (not working) introductions and conclusions
- `references/body-ordering-heuristics.md` — Extended guidance on each of the eight ordering principles with field-specific examples
- `references/storyboard-anti-patterns.md` — Diagnostic checklist and correction exercises for all three flawed-plan patterns

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Craft of Research, 4th Edition by Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, William T. FitzGerald.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-research-argument-builder`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
