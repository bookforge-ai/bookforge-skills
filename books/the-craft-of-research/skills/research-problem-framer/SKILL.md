---
name: research-problem-framer
description: Transform a research question into a fully framed research problem that readers recognize as worth solving, using the condition+consequence structure and the So What? cascade test. Use this skill when the user has a research question but cannot explain why readers should care about the answer, has completed the 3-step significance formula but the Step 3 consequence still feels abstract or weak, is writing an introduction and the reader's "So what?" objection keeps coming back, cannot tell whether their project is pure or applied research and whether that matters for their introduction, wants to verify that solving their conceptual problem actually serves a practical one, has a research question that feels personally interesting but lacks community relevance, is being asked by an advisor or reviewer "why does this matter?", needs to state a research problem in formal proposal or introduction language, wants to understand the difference between a research question (condition) and a research problem (condition + consequence) and why the problem frame is what goes in the introduction, or is building a research argument but keeps getting feedback that readers don't feel the stakes. This skill handles problem framing and consequence articulation; it does NOT formulate the initial research question (use research-question-formulator for that) or write the claim/thesis statement.
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [4]
tags: [research-methodology, academic-writing, research-problems, critical-thinking]
depends-on: [research-question-formulator]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "User's research question, 3-step formula sentence, or partial introduction describing what they are studying and why"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user needs a text file or can supply context verbally"
discovery:
  goal: "Elevate a research question into a problem statement that readers recognize as worth solving — by naming the condition (what you do not know) and its consequence (what that gap prevents readers from understanding)"
  tasks:
    - "Classify the problem as practical or conceptual and identify the type of gap"
    - "Name the condition (the knowledge gap stated as the research question)"
    - "Identify the consequence (what more important question remains unanswerable until this one is solved)"
    - "Run the So What? cascade to test whether the consequence is specific enough and audience-grounded"
    - "Determine whether the project is pure or applied research and adjust the consequence framing"
    - "Compose a 2-3 sentence problem statement ready for a paper introduction"
  audience: "Researchers, graduate students, professionals, and analysts who have a focused question but need to articulate its community significance"
  triggers:
    - "User has a question but cannot explain why readers should care about the answer"
    - "User's Step 3 significance statement reads as 'interesting to me' rather than 'urgent to my readers'"
    - "Reviewer or advisor asks 'so what?' after hearing the research question"
    - "User cannot distinguish their question (condition) from their problem (condition + consequence)"
    - "Introduction does not create stakes that make readers want to keep reading"
    - "User asks 'is this pure or applied research?' or 'how do I justify this to a practical audience?'"
---

# Research Problem Framer

## When to Use

You have a focused research question (or can formulate one quickly) and need to complete the move from question to problem — the move that tells readers not just what you do not know, but why they should care whether you find out.

A research problem has two parts:

1. **Condition:** A gap in knowledge or understanding (stated as your research question)
2. **Consequence:** What more important question cannot be answered until this gap is closed

Without the consequence, your question is a private curiosity. With it, you enter a community conversation.

Typical triggers:

- "I have a good question but my advisor keeps asking 'so what?'"
- Your introduction describes what you will study but does not create a reason for readers to keep reading
- You finished the 3-step formula and Step 3 still feels thin or forced
- You are not sure whether your consequence is strong enough for your field
- You need to write an introduction that opens with stakes, not just a topic

**Preconditions to verify:**

- Does the user have a focused research question (a how/why question, not a topic)? If not: invoke `research-question-formulator` first, OR ask the user to state what they want to find out in one sentence.
- Does the user know their intended audience? (The consequence must land from the reader's point of view, not the researcher's.)

**This skill does NOT cover:**

- Formulating the research question from scratch (use `research-question-formulator`)
- Writing the full thesis, claim, or argument structure
- Evaluating source quality or selecting a methodology

## Context and Input Gathering

### Required (ask if missing)

- **The research question:** The condition of the problem — what the researcher does not yet know.
  -> Check prompt for: a direct how/why question, or the middle term of the 3-step formula
  -> If missing, ask: "What is your research question — the specific thing you want to find out? Even a rough sentence is enough to start."

- **The intended audience or field:** Who will judge whether the consequence is significant.
  -> Check prompt for: mentions of discipline, course, journal, professional setting, or reader type
  -> If missing, ask: "Who are the readers this research is for — a course, a scholarly field, a professional community, or a general audience?"

### Useful (gather from environment if available)

- **Existing 3-step formula sentence:** May already contain a draft consequence in Step 3 that just needs strengthening.
  -> Look for files like `notes.md`, `outline.md`, `draft-intro.md`, or `proposal.md` in the working directory
  -> If found, extract the Step 3 statement and evaluate it against the So What? cascade before rebuilding from scratch

- **Whether the project has a practical application:** Determines whether to frame the consequence as pure (understanding) or applied (doing).

## Process

### Step 1 — Confirm the Research Question Is Problem-Ready

**WHY:** A research problem cannot be framed until the question is genuinely focused. Too-broad questions produce consequences that are correspondingly vague ("helps readers understand a lot of things"), which fails the So What? cascade. A quick diagnostic here saves a wasted framing cycle.

Check the question against two fast tests:

**Test A — Is it a how/why question?**
Questions beginning with "Does," "Is," "Did," or "Are" invite yes/no answers that close inquiry. Problem framing requires an open question.

| Closes inquiry (not ready) | Opens inquiry (ready) |
|---|---|
| Did the Alamo story influence Texas voters? | How and why did nineteenth-century politicians use Alamo stories to shape public opinion? |
| Is remote work less productive? | How does schedule flexibility in remote work policies affect code quality in software teams? |

**Test B — Is it a single focused question (not a topic)?**
If the question can be answered by listing facts without analysis, it is still a topic masquerading as a question.

If either test fails: invoke `research-question-formulator` first, or work with the user to sharpen the question before continuing.

### Step 2 — Classify the Problem Type

**WHY:** The type of problem determines the type of consequence. Practical problems have tangible costs (money, health, safety, opportunity). Conceptual problems have epistemic consequences — what else we cannot understand because of this gap. Misclassifying the problem type leads to mismatched consequences: attaching a thin practical justification to a conceptual question reads as a stretch and weakens the problem statement.

**Practical problem:** A condition in the world that imposes tangible costs (time, money, safety, respect, opportunity). Solving it requires doing something.

Example:
- Condition: Costs are rising at the Omaha plant.
- Cost: The company is losing money.
- Research problem: What changed? (to find out so management can act)

**Conceptual (research) problem:** A condition of not knowing or not understanding something. Solving it requires answering a question.

Example:
- Condition: We do not know how politicians used Alamo stories to shape public opinion.
- Consequence: We cannot understand how regional self-images influence national politics.

Most academic, journalistic, and professional research projects are conceptual problems. Practical problems motivate the research but the conceptual problem is what the paper actually solves.

**Relationship:** Practical problems motivate conceptual ones. Research answers the conceptual question, which in turn helps solve the practical one. When they are linked, both should appear in the problem statement — the practical problem as motivation, the conceptual problem as what the research actually does.

### Step 3 — Name the Condition

**WHY:** The condition is simply the research question restated as a gap. Making it explicit in the problem statement — rather than leaving it implicit in the question alone — is what lets readers recognize that you are not just curious but investigating something that has not yet been understood. Naming the gap signals that the research is filling something, not just adding to an already-full pile.

Restate the research question as a gap in one of two forms:

**Direct form (question):**
> "How have romantic movies changed in the last fifty years?"

**Indirect form (noun clause, for use in the problem statement):**
> "We do not yet know how romantic movies have changed in the last fifty years."
> or
> "The ways romantic movies have changed in the last fifty years remain poorly understood."

The indirect form integrates more naturally into the introduction prose. Use it when composing the final problem statement.

### Step 4 — Identify the Consequence Using the So What? Cascade

**WHY:** The consequence is what makes the research matter to someone other than the researcher. Without a named consequence, readers have no reason to care whether you answer your question. The So What? cascade is a pressure test: you keep answering "So what if we can't answer this?" until you reach a question that your audience clearly thinks needs answering. If you can answer the cascade in one step, the consequence is probably strong. If you run out of answers before reaching something your audience cares about, the problem needs reconfiguration.

**Run the cascade:**

Start with the condition, then ask: "So what if we can't answer that question?"

> Condition: We do not know how romantic movies have changed in the last fifty years.
> So what? → We can't answer: How have our cultural depictions of romantic love changed?
> So what? → We can't answer: How does our culture shape young people's expectations about marriage and family?

Stop when you reach a question your audience clearly cares about. That is your consequence.

**Rules for a strong consequence:**

1. **The answer to Q1 (condition) must genuinely help answer Q2 (consequence).** The link must be logical, not merely thematic.
2. **Q2 must be more important than Q1 to your readers.** If Q2 is equally obscure or equally unimportant, keep cascading.
3. **The consequence must be stated from the reader's point of view** — it is a cost they pay if the condition is not resolved, not a reward you receive for answering your question.
4. **Stop the cascade before the question becomes so large it swamps the research.** "How does culture work?" is too broad to function as a consequence.

**If the cascade stalls:** You have not yet spent enough time in the field to see what depends on your answer. Provisional remedy: state "The significance of this question will emerge during research" and return to this step after initial reading.

### Step 5 — Determine Pure or Applied Framing

**WHY:** Pure and applied research have the same structure (condition + consequence) but different consequence types. Pure research consequences refer to understanding; applied research consequences refer to doing. Using the wrong consequence type misrepresents the project's goals and can create a mismatch between what the research delivers (knowledge) and what the introduction promises (action). Getting this right also determines whether to include a practical application as a fourth step.

**Test:** Look at your consequence (Step 3 of the 3-step formula). Does it refer to knowing/understanding, or to doing?

**Pure research:** Consequence refers to understanding a larger question.
> "...in order to help readers understand how regional self-images influence national politics."

**Applied research:** Consequence refers to doing something differently.
> "...in order to help astronomers use data from earthbound telescopes to measure electromagnetic radiation more accurately."

**Hybrid (add a fourth step):** If the project is fundamentally conceptual but has a plausible practical application, frame it as pure research and add a fourth step naming the potential practical consequence. The practical application goes in the conclusion, not the introduction.

> Step 3 (conceptual): "...in order to help readers understand how politicians use popular culture to advance political goals."
> Step 4 (practical, in conclusion only): "...so that readers might better recognize and resist manipulation by political narratives."

**Caution:** Do not attach a practical consequence to a conceptual question unless the link is genuine and specific. If readers must take a conceptual leap to see how the knowledge leads to action, the link is a stretch. A thin practical consequence weakens the problem, it does not strengthen it.

### Step 6 — Compose the Problem Statement

**WHY:** The problem statement is the payoff of this entire process — a 2-3 sentence formulation that goes into the introduction and creates the stakes that make readers want to keep reading. It must state both the condition (the gap) and the consequence (what the gap prevents) clearly enough that readers can recognize the problem as one that belongs to them, not just to the researcher.

**Template:**

```
[Condition sentence: name the gap]
[Consequence sentence: name what cannot be understood/done without closing that gap]
[Optional: name the practical application if the project is applied]
```

**Examples:**

Pure research (Alamo):
> We do not yet understand how nineteenth-century politicians used stories of the Alamo to shape public opinion. Without that understanding, we cannot fully explain how regional self-images become instruments of national political persuasion.

Applied research (Hubble telescope):
> We do not know how much the atmosphere distorts electromagnetic measurements taken by earthbound telescopes. Until we do, astronomers cannot use earthbound data to measure the density of electromagnetic radiation with confidence.

Hybrid (four-step):
> We do not understand how politicians used stories of great historical events to shape public opinion in the nineteenth century. Until we do, we cannot understand how popular culture functions as a tool of political goals — a gap that, once closed, may help readers recognize similar moves in contemporary politics.

**Composition rules:**

- Lead with the condition (the gap), not with background or context
- State the consequence before offering any solution
- Use "we do not know," "we do not yet understand," or "the X of Y remains unclear" for the condition
- Use "until we do, we cannot" or "without understanding X, we cannot address Y" for the consequence
- Keep the statement to two or three sentences; longer statements bury the stakes

## Examples

### Example 1 — Undergraduate humanities paper

**Input question:** How have cultural depictions of romantic love in American movies changed since 1970?

**Step 2 — Problem type:** Conceptual. The condition is not knowing how depictions have changed; there is no immediate practical cost, but there is an epistemic consequence.

**Step 3 — Condition:** We do not yet know how romantic movies have changed their depictions of love and relationships over the past fifty years.

**Step 4 — So What? cascade:**
- So what if we don't know this? → We can't understand how Hollywood storytelling shapes cultural expectations about romantic partnerships.
- So what? → We can't understand how mass media influences what young people expect from marriage and long-term relationships.
- *(Audience cares. Stop here.)*

**Step 5 — Pure or applied:** Pure. The consequence is about understanding cultural influence, not about making better movies or fixing relationship expectations. No practical fourth step needed.

**Problem statement:**
> We do not yet know how American romantic movies have changed their depictions of love and partnership over the past fifty years. Without that knowledge, we cannot fully understand how Hollywood storytelling shapes the expectations young people bring to romantic relationships — a question central to cultural psychology and media studies.

---

### Example 2 — Graduate policy research

**Input question (from 3-step formula):** How did the loss of NASA's Hubble instruments change the agency's approach to telescope design and redundancy planning?

**Step 2 — Problem type:** Hybrid. There is a conceptual problem (what we do not know about how institutional learning works after a major failure) linked to a practical one (how NASA and similar agencies should design future systems).

**Step 3 — Condition:** We do not know how the Hubble failure changed NASA's internal design review and redundancy protocols.

**Step 4 — So What? cascade:**
- So what? → We can't understand how large engineering organizations update institutional practices after high-profile failures.
- So what? → We can't explain what conditions cause those updates to stick versus fade within a decade.
- *(Applied consequence within reach: agencies cannot design reliable failure-response protocols.)*

**Step 5 — Framing:** Applied. The consequence refers to doing (designing better protocols), so the project is applied research.

**Problem statement:**
> We do not know how the Hubble Space Telescope's optical failure changed NASA's internal design review and redundancy planning processes. Without that understanding, large engineering agencies lack a documented model for how institutional learning after catastrophic failure translates — or fails to translate — into lasting procedural change.

---

### Example 3 — Professional context

**Input:** "I'm writing a report on why our engineering team's velocity dropped after switching to remote work. My manager wants to know if we should go back to in-office or just change our remote policies."

**Step 2 — Problem type:** Practical problem (velocity drop costs delivery time and morale) → motivates a conceptual problem (we don't know which aspect of remote work caused the drop).

**Step 3 — Condition:** We do not know whether the velocity drop is caused by collaboration friction, tooling gaps, scheduling misalignment, or some combination.

**Step 4 — So What? cascade:**
- So what? → Without knowing the cause, management cannot fix the right variable.
- So what? → The organization risks reverting to in-office work to solve a problem that actually requires policy redesign, not location change.
- *(Manager cares. Stop here.)*

**Step 5 — Framing:** Applied. Consequence refers to doing (making the right policy decision).

**Problem statement:**
> We do not yet know whether our team's velocity decline after the remote transition stems from collaboration friction, scheduling misalignment, tooling inadequacy, or a combination of factors. Without that diagnosis, any intervention — including a return to in-office work — risks fixing the wrong variable and leaving the actual cause unaddressed.

---

## Anti-Pattern Quick Reference

| Anti-pattern | Diagnosis signal | Fix |
|---|---|---|
| Researcher-centric consequence | Step 3 reads "to satisfy my curiosity about X" or "to complete my degree" | Reframe from reader's point of view: what does the reader gain or lose depending on your answer? |
| Artificial practical significance | Practical consequence requires a leap of logic from the conceptual question | Frame as pure research; add practical application as an optional fourth step in the conclusion only |
| Consequence equals condition | "We don't know X because we don't know X" — circular restatement | Run the cascade: ask "So what if we can't answer this?" to find a genuinely distinct, larger question |
| Consequence too large | "Until we answer this, we can't understand how culture works" | Narrow: stop the cascade one step earlier; link to a specific sub-question your audience already cares about |
| Mixed pure/applied framing | Introduction promises practical change but research only delivers understanding | Choose one: either frame as pure + optional practical fourth step, or redesign the project as genuinely applied |
| No audience grounding | Consequence is significant to the researcher but not named from reader's perspective | Imagine the reader asking "So what does that mean for me?" — the answer to that question is the consequence |

## References

- See `references/condition-consequence-structures.md` for worked condition+consequence pairs across disciplines (humanities, social sciences, natural sciences, professional research)
- See `references/pure-vs-applied-framing.md` for the four-step hybrid formula and guidance on when to add a practical application step
