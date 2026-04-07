---
name: research-introduction-architect
description: Draft a complete research introduction and matching conclusion using the Context→Problem→Response architecture. Use this skill when the user has a framed research problem (condition + consequence) and needs to write or revise the opening and closing sections of a research paper; when an introduction exists but reads as a flat topic announcement instead of a problem-driven argument; when the user cannot decide whether to state the main point in the introduction (point-first) or withhold it for the conclusion (point-last) and needs to understand the trade-offs; when the first sentence of the introduction is a dictionary definition, a grand universal claim ("Throughout history…"), or a repetition of the assignment prompt; when the conclusion merely restates the introduction without adding new significance or calling for further research; when the user needs guidance on how much context to provide — neither too sketchy nor encyclopedic — based on the audience's prior knowledge; when the pacing of an introduction (fast vs. slow context setup) needs to match audience expertise level; or when the user wants a checked draft that correctly omits the context element (problem well-known) or consequence element (widely understood) rather than including them by default. This skill outputs a draft introduction and conclusion. It does NOT frame the research problem from scratch — use research-problem-framer for that.
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [16]
tags: [research-methodology, academic-writing, introductions, conclusions, argumentation]
depends-on: [research-problem-framer]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "User's research problem statement (condition + consequence), main point or thesis, and a description of the intended audience and field"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user provides problem statement and main point verbally or in a file"
discovery:
  goal: "Draft a complete introduction (Context + Problem + Response) and a matching conclusion (main point + new significance + call for research) that compels the audience to read and leaves them with renewed appreciation of the work's significance"
  tasks:
    - "Gather the research problem statement, main point, audience description, and field"
    - "Decide whether to include or omit each element (context, consequence, main point in intro)"
    - "Determine pace: fast (expert audience) or slow (general/introductory audience)"
    - "Select the opening sentence strategy: striking fact, quotation, or anecdote"
    - "Draft the introduction with correct Context→Problem→Response sequencing"
    - "Draft the conclusion as a mirror reversal: main point → new significance → call for research"
    - "Run structural self-check against anti-patterns and omission rules"
  audience: "Researchers, graduate students, and professionals drafting or revising introductions and conclusions for academic papers, reports, or proposals"
  triggers:
    - "User has a research problem but needs to write the introduction"
    - "Introduction exists but reads as topic announcement, not problem argument"
    - "First sentence is a dictionary definition, grand universal claim, or assignment repetition"
    - "User cannot decide whether to place the main point in the intro or the conclusion"
    - "Conclusion merely repeats the introduction without adding significance or new questions"
    - "Introduction pace (context length) does not match audience expertise"
---

# Research Introduction Architect

## When to Use

You have a framed research problem — a condition (what is not known) and a consequence (what that gap prevents) — and a main point or thesis. Now you need to write the introduction and conclusion that will move readers from curiosity to engagement and leave them with a clear sense of why the work matters.

This skill covers the full drafting cycle:

1. **Introduction:** Context → Problem → Response
2. **Conclusion:** Main point → New significance → Call for further research

**Preconditions to verify:**

- Does the user have a problem statement with both a condition and a consequence? If not: invoke `research-problem-framer` first.
- Does the user have at least a draft main point or thesis? If not: ask them to state in one sentence what their research concludes.
- Do you know the intended audience (field, expertise level, general vs. specialist)?

**This skill does NOT cover:**

- Framing the research problem from scratch (use `research-problem-framer`)
- Building the argument structure of the body (use `research-argument-builder`)
- Editing prose clarity (use `prose-clarity-reviser`)

## Context and Input Gathering

### Required (ask if missing)

- **The problem statement:** A condition + consequence in 2-3 sentences. This is the core of the Problem element.
  -> Check for files like `notes.md`, `outline.md`, `draft-intro.md`, or `proposal.md`
  -> If missing, ask: "What is your research problem — the gap in knowledge and why it matters to readers?"

- **The main point or thesis:** The conclusion the research reaches.
  -> If missing, ask: "What does your research conclude? Even a rough one-sentence answer is enough to start."

- **The intended audience:** Determines pace (how much context to build before disrupting it) and whether consequences need to be spelled out.
  -> If missing, ask: "Who are your readers — specialists in a field, a general educated audience, or a specific professional community?"

### Useful (gather from environment if available)

- **Existing draft introduction or outline:** Diagnose which elements are present and which are missing before rewriting.
- **Field or discipline conventions:** Sciences and social sciences typically allow faster context setup and explicit road-maps; humanities introductions often open more slowly and withhold the main point until the conclusion.

## Architecture: The Three-Element Introduction

Every introduction, regardless of field, follows the same underlying grammar:

**Context → Problem → Response**

| Element | Function | When to omit |
|---|---|---|
| Context | Establish common ground — the stable, unproblematic state of knowledge — so that the Problem can disrupt it | Omit when the problem is so well-known that readers already share the disruption |
| Problem | State the condition (gap in knowledge) and consequence (what the gap prevents) | Never omit — this is the engine of the introduction |
| Response | State the main point directly (point-first) or promise a main point to come (point-last) | Never omit entirely — at minimum, provide a launching point |

The conclusion reverses this order: **Response (main point) → new significance → call for further research**.

## Process

### Step 1 — Gather and Confirm the Problem Statement

**WHY:** Everything in the introduction grows from the research problem. A problem statement that lacks a consequence, or that is still framed as a topic rather than a gap, will produce a flat introduction no matter how well the surrounding elements are written. Confirming the problem statement before drafting prevents rewriting the introduction after fixing the problem.

Confirm the problem statement has two parts:

- **Condition sentence:** Names the gap. Uses formulations like "We do not yet know…," "X remains poorly understood…," or "The ways Y has changed remain unclear…"
- **Consequence sentence:** Names what that gap prevents. Uses formulations like "Without that understanding, we cannot…" or "Until we do, readers cannot address…"

If the consequence is missing, run the So What? cascade (see `research-problem-framer`) before continuing.

### Step 2 — Decide the Structural Configuration

**WHY:** Choosing the wrong structural configuration — omitting context the audience needs, or laboriously establishing context the audience already knows — damages credibility. Experts who see two paragraphs of background they already know may conclude the writer underestimates them. Novices who see no context may not understand why the problem is a problem.

Work through three decisions:

**Decision A — Include or omit the Context element?**

Include context when:
- The audience may not immediately recognize why the existing state of knowledge is insufficient
- The problem requires a stable baseline to make the disruption legible

Omit context (open directly with the Problem) when:
- The problem is already widely familiar in the field (e.g., a well-known open question in mathematics or physics)
- Opening with context would be condescending to specialist readers

**Decision B — Spell out consequences or omit them?**

Spell out consequences when:
- The audience works in a field where the problem is new or unfamiliar
- The connection between the condition and the larger gap is not self-evident

Omit consequences (or state them briefly) when:
- The audience knows the field well and would find explicit consequence-statements redundant
- The consequence is genuinely obvious once the condition is named

**Decision C — Point-first or point-last?**

| Choice | What it does | When to use |
|---|---|---|
| **Point-first** (state main point in intro) | Reader knows the destination from the start; controls their own reading | Sciences, social sciences, professional reports; readers who skim for answers |
| **Point-last** (launch point in intro, main point in conclusion) | Writer controls revelation; suspense builds through the argument | Humanities, complex arguments where the conclusion requires the full argument to be persuasive |

The minimum for point-last is a **launching point**: a concrete plan or outline of the argument, not just "This paper will discuss X." Vague topic announcements ("This study investigates processes leading to ozone depletion") give readers no reason to trust the journey.

### Step 3 — Determine the Pace

**WHY:** Pace signals how much the writer assumes the reader already knows. A fast opening (one or two sentences of context before the disruption) implies a peer audience. A slow opening (extended context built over several sentences or paragraphs) implies a less expert audience. Mismatched pace is a credibility signal: too slow for experts reads as patronizing; too fast for novices reads as inconsiderate.

**Fast pace (expert audience):**
- One sentence naming the established consensus or current practice
- Immediately disrupt with the condition of the problem
- State the consequence in one sentence if needed

**Slow pace (general or introductory audience):**
- Multiple sentences building the background, defining terms, and establishing the stakes
- Disrupt only after the reader has enough grounding to feel the disruption

**Diagnostic question:** If you read the first sentence to someone in your target audience, would they immediately recognize it as describing their world? If yes: fast pace is safe. If no: build more context first.

### Step 4 — Select the Opening Sentence Strategy

**WHY:** The first sentence establishes tone, signals audience, and creates the first impression of the writer's authority. Three patterns work; three common substitutes do not.

**Patterns that work:**

1. **Striking fact relevant to the problem**
   > "Those who think that tax cuts for the rich stimulate the economy should contemplate the fact that the top 1 percent of Americans control one-third of America's total wealth."
   — Works because the fact is specific, surprising, and directly anticipates the problem

2. **Striking quotation** (only if key terms recur through the introduction)
   > "From the sheer sensuous beauty of a genuine Jan van Eyck there emanates a strange fascination not unlike that which we experience when permitting ourselves to be hypnotized by precious stones." — Edwin Panofsky
   — Works because specific language from the quotation ("fascination," "strange") drives the rest of the introduction

3. **Relevant anecdote** (only if its language vividly illustrates the problem)
   > "On a park bench in July 1996, Cynthia, Laurie, and other senior officers of the Black Sisters United — Chicago's largest federation of 'girl gangs' — reflected on their efforts…"
   — Works because the scene concretizes the problem before any abstract statement

**Anti-patterns to avoid:**

| Anti-pattern | Why it fails |
|---|---|
| Dictionary definition ("Webster's defines ethics as…") | Signals the writer does not yet know what the word means in their field; too generic for any audience |
| Grand universal claim ("Throughout history, philosophers have…") | Wrong community: tries to speak to all of humanity rather than the specific audience who cares about this problem |
| Assignment repetition ("This paper will analyze…") | Signals the audience is a single teacher, not a research community; treats the paper as a task, not an argument |

### Step 5 — Draft the Introduction

**WHY:** Writing the full draft — rather than an outline — forces every element to be resolved. Gaps that seem small in outline form (a missing consequence, a vague launching point) become visible as structural problems in a full draft.

Assemble the elements in order:

```
[Opening sentence: striking fact, quotation, or anecdote]
[Context: 1-4 sentences establishing the stable, unproblematic state of knowledge]
    — OR omit if problem is well-known —
[Condition: the gap in knowledge, stated as "We do not yet know…" or equivalent]
[Consequence: what the gap prevents, stated as "Without that…, we cannot…"]
    — OR omit if consequence is self-evident to the audience —
[Response: main point stated directly (point-first) OR launching point with plan (point-last)]
```

Target length: 150–350 words for most academic and professional introductions. Longer for book chapters or proposals; shorter for short reports.

### Step 6 — Draft the Conclusion

**WHY:** A conclusion that merely restates the introduction tells readers nothing they do not already know. The conclusion earns its place by doing two things the introduction cannot: it states the main point in full (rather than promising it), and it extends the conversation — naming new significance, implications, or open questions that the research has made visible.

Structure the conclusion as a mirror reversal of the introduction:

```
[Main point, stated more fully than in the introduction — not word-for-word repeated]
[New significance or application: a new answer to "So what?" that was not in the introduction]
    — e.g., an additional implication, a practical consequence, or a broader theoretical connection —
[Call for further research: what questions remain open; what studies would follow naturally]
    — frame as keeping the conversation alive, not admitting defeat —
```

**On the new significance:** State it in the conclusion, not the introduction, because it suggests further questions the paper does not take up. Introducing it in the introduction would create an obligation to answer it in the body.

**On the call for research:** Imagine a reader fascinated by your work who wants to follow up. What would you tell them to investigate? This frames the call as generative, not as an admission of incompleteness.

### Step 7 — Structural Self-Check

**WHY:** Small structural errors in introductions and conclusions — missing consequences, vague launching points, word-for-word repeated conclusions — are easy to miss in the flow of drafting. A brief checklist catches them before the draft is shared.

Run through each item:

- [ ] Does the introduction open with a specific first sentence (fact, quotation, or anecdote) — not a dictionary definition, universal claim, or assignment repetition?
- [ ] Is the Context calibrated to audience expertise (not too thin, not encyclopedic)?
- [ ] Is the Problem stated with both a condition AND a consequence — or is the omission of the consequence justified by audience familiarity?
- [ ] Is the Response either a direct main point (point-first) or a concrete launching point with a plan (point-last) — not merely a vague topic announcement?
- [ ] Does the conclusion state the main point more fully than the introduction — not word-for-word repeated?
- [ ] Does the conclusion add new significance (a new answer to "So what?") not present in the introduction?
- [ ] Does the conclusion call for further research that extends rather than merely closes the argument?

If any item fails, revise before delivering the draft.

## Examples

### Example 1 — Humanities paper (point-last, full context)

**Input:**
- Condition: We do not know why the quasi-persons in American science fiction (androids, half-aliens, cyborgs) are almost invariably depicted as white and male.
- Consequence: Without understanding this pattern, we cannot fully analyze how popular culture defines personhood against non-Western, non-male norms.
- Main point: These figures implicitly define the "model person" by Western, male criteria — a definition that excludes most of humanity.
- Audience: Cultural studies readers, familiar with Star Trek and Frankenstein but not necessarily with critical race theory.
- Pace: Moderate (lay out examples before disrupting).

**Introduction draft:**

> In almost every episode of *Star Trek: The Next Generation*, the android Data wonders what makes a person a person. In the original *Star Trek*, similar questions were raised by the half-Vulcan Mr. Spock, whose status as a person was undermined by his machine-like logic and lack of emotion. Data and Spock are only the most recent "quasi-persons" in American popular fiction who have explored the nature of humanity — a lineage that runs from Frankenstein's monster to the Terminator. But the real question is not whether these characters achieve personhood. It is why these quasi-persons who struggle to be persons are almost always white and male. As cultural interpreters, do they tacitly reinforce destructive stereotypes about what it means to be "normal"? This article argues that the model person in American science fiction is consistently defined by Western, male criteria — a definition that, taken seriously, excludes most of the people in the world.

**Why this works:**
- Opening anecdote (Data wondering) anchors the problem concretely before naming it abstractly
- Context builds two paragraphs of examples, then the "But" disrupts them
- Consequence is embedded in the rhetorical question ("do they reinforce destructive stereotypes?")
- Response states the main point directly (for a short article); an essay version might end with a launching point instead

---

### Example 2 — Professional report (point-first, fast pace, no explicit consequence)

**Input:**
- Condition: Motodyne has no data showing which of its online help icons are self-explanatory to users.
- Consequence: Without such data, the design team cannot determine which icons to redesign.
- Main point: Five of eleven icons tested are not self-explanatory; those five should be priority redesigns.
- Audience: Engineering and UX team at Motodyne — knows the product, unfamiliar with the specific test data.
- Pace: Fast (one sentence of context, then directly to the problem).

**Introduction draft:**

> As part of its Continuous Quality Improvement program, Motodyne plans to redesign the user interface for its Unidyne online help system — specifically, the icons that should be self-explanatory without verbal labels. Motodyne has three years of experience with its current icon set, but it has no data showing which icons users actually understand without labels. Lacking such data, we cannot determine which icons to redesign. This report provides data for eleven icons and shows that five of them are not self-explanatory.

**Why this works:**
- Fast pace: one sentence of organizational context, then immediately to the gap
- Consequence is explicit ("cannot determine which icons to redesign") because the team is not a specialist research audience
- Response states the main point directly — appropriate for a technical report where readers skim for findings

---

### Example 3 — Academic paper with conclusion (legal history)

**Input:**
- Condition: It is unclear whether Supreme Court decisions rejecting mandatory death sentences in civilian cases apply to the military, creating ambiguity in the Uniform Code of Military Justice.
- Consequence: Until resolved, Congress cannot know whether it must revise military law.
- Main point: The Supreme Court's decisions do apply, and Congress must revise the Uniform Code.
- New significance (for conclusion): Revising the Code will challenge a foundational value of military culture — that ultimate betrayal requires ultimate penalty — which will force Congress to adjudicate military values, not just legal rules.
- Audience: Legal scholars and policy readers, familiar with the Uniform Code but not necessarily with the specific Supreme Court cases.

**Introduction draft:**

> In today's society, would Major John André — a British spy captured behind American lines in 1780 — be hanged? Though considered a noble patriot by the British, he suffered the punishment mandated by military law. Over time our traditions of punishment have changed, but the punishment for spying has not: it is the only offense that still mandates death. Recently, however, the Supreme Court has rejected mandatory death sentences in civilian cases, creating an ambiguity in their application to military law. If those decisions apply to the military, Congress may have to revise the Uniform Code of Military Justice. This article concludes that it will.

**Conclusion draft:**

> In light of recent Supreme Court decisions rejecting mandatory capital punishment, the mandatory death penalty for espionage is apparently unconstitutional and must be revised by Congress. More significantly, if the Uniform Code of Military Justice is changed, it will challenge the fundamental value of military culture that ultimate betrayal requires the ultimate penalty. Congress will then have to deal not just with a legal inconsistency, but with the military's deeply held sense of what justice demands — a question that extends well beyond the narrow issue of one penalty's constitutionality. Future research should examine how military culture has historically adapted its core values when external legal constraints required change, and whether those adaptations were perceived as legitimate by the communities they governed.

**Why this works:**
- Conclusion restates the main point ("must be revised") more fully than the introduction's one-sentence prediction
- New significance (the cultural challenge to military values) was not in the introduction — introducing it there would have created an unanswered obligation
- Call for research ("how military culture has historically adapted…") keeps the conversation alive without implying the article failed to answer its own question

## Anti-Pattern Quick Reference

| Anti-pattern | Diagnosis signal | Fix |
|---|---|---|
| Dictionary opening | "Webster's defines X as…" in sentence 1 | Replace with a striking fact, quotation, or anecdote specific to the problem |
| Grand universal opening | "Throughout history…" or "Since the dawn of civilization…" | Narrow to the specific community of readers; open with a fact or example from their field |
| Assignment repetition | "In this paper, I will discuss…" mirrors the prompt language | Rewrite for a reader who has not seen the assignment; treat the introduction as an argument, not a task report |
| Context-only introduction | Background runs for several paragraphs with no disruption | Add the condition (gap) and consequence before the response; the introduction must contain a problem |
| Missing consequence | Condition stated, then immediately jumps to response | Ask So what? after the condition; state what remains unresolvable if the gap is not closed |
| Vague launching point | "This paper will investigate X" with no plan | Replace with a concrete outline of the argument: what the paper evaluates, compares, or demonstrates |
| Word-for-word repeated conclusion | Conclusion uses same sentences as introduction | Restate the main point more fully; add new significance not previewed in the introduction |
| Conclusion as summary only | Conclusion lists findings without adding significance | Add a new answer to "So what?" — an implication, application, or further question the research has opened |

## References

- See `references/introduction-configurations.md` for full worked examples of all structural configurations (omit context, omit consequence, point-first vs. point-last) across three disciplines
- See `references/conclusion-patterns.md` for worked conclusion drafts with and without calls for further research
