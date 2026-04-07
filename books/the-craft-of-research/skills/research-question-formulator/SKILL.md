---
name: research-question-formulator
description: Transform a broad topic into a focused, answerable research question with built-in significance using the 3-step sentence-completion formula (topic → direct question → So What?). Use this skill when the user has a subject or area of interest but no specific question, has a vague topic like "climate change" or "leadership" and needs to narrow it to something researchable, says they don't know what their paper is really about, is collecting too many notes without a clear direction, wants to know if their research question is worth asking, needs to test whether their topic is too broad (4-5 words = too broad), has a yes/no question that won't drive analysis, is asking a settled-fact question that doesn't open inquiry, wants to move from aimless reading to targeted evidence gathering, has a draft thesis but lost track of what question it answers, or is stuck at the beginning of a research project and doesn't know where to start — even if they never use the phrase "research question formulation." This skill handles question generation and significance testing; it does NOT write the thesis statement (use a separate skill) or plan the full argument structure.
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [3]
tags: [research-methodology, academic-writing, critical-thinking, research-questions]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "User's topic, subject area, draft notes, or early outline — even a single sentence describing what they are interested in"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user needs a text file or can supply topic verbally"
discovery:
  goal: "Turn a broad subject into a focused, significant research question that directs evidence gathering and gives the paper a reason to exist"
  tasks:
    - "Diagnose whether the current topic is too broad, too narrow, or not a question at all"
    - "Apply the 3-step sentence-completion formula to produce a testable research question"
    - "Run the So What? test to confirm the question has significance beyond personal curiosity"
    - "Identify and correct anti-patterns: settled-fact questions, yes/no questions, dead-end questions"
  audience: "Researchers, students, professionals, and analysts starting any evidence-based writing project"
  triggers:
    - "User has a topic but no question"
    - "User is collecting too much information without direction"
    - "User's draft question is too broad, too narrow, or answerable by a single lookup"
    - "User cannot explain why their question matters to anyone else"
    - "User asks 'what should I research about X?'"
    - "User says their paper is about a subject but cannot state what it argues"
---

# Research Question Formulator

## When to Use

You have a subject area, a general interest, or a draft topic, and need to sharpen it into a research question that:

1. Specifies what you do not yet know
2. Directs exactly which evidence you need
3. Answers the "So what?" test — others beyond you care about the answer

Typical triggers:

- "I want to write about [subject] but don't know what my question is"
- Draft notes are accumulating without a focal point
- A question exists but produces only yes/no or looks-it-up answers
- The topic can be stated in four or five words (a sure sign it is too broad)
- Advisor or peer feedback says "I don't know what you're arguing"

**Preconditions to verify:**

- Does the user have at least a rough subject area? (Even "something about climate change" is enough to start)
- Are there any existing notes, outlines, or a draft that might reveal unstated questions?

**This skill does NOT cover:**

- Writing the full thesis statement or claim (topic + question precede the claim)
- Structuring the full argument or paper outline
- Evaluating source quality or research methodology choices

## Context and Input Gathering

### Required (ask if missing)

- **The topic or subject area:** The raw material. A phrase, a sentence, or a paragraph describing what interests the user.
  -> Check prompt for: any subject noun or phrase the user mentions
  -> If missing, ask: "What subject or area are you exploring? Even a rough phrase like 'social media and teenagers' is enough to start."

- **Audience or field context:** Who will read and judge this research? Determines what counts as significant.
  -> Check prompt for: mentions of course, discipline, journal, professional context, or reader type
  -> If missing, ask: "Who is the intended audience — a course instructor, professional colleagues, a journal, or a general reader?"

### Useful (gather from environment if available)

- **Existing notes or draft:** May contain an implicit question the user has not yet named explicitly.
  -> Look for files like `notes.md`, `outline.md`, `draft.md` in the working directory
  -> If found, read them before proceeding — the actual question may already be buried in the material

- **Prior question attempts:** If the user has written a question already, evaluate it rather than starting from scratch.

## Process

### Step 1 — Diagnose the Current Topic

**WHY:** Most researchers begin with a subject, not a question. A subject is static (it can just *be*); only a question creates the obligation to gather evidence and answer something. Diagnosing the topic first prevents building a bad question on a bad foundation.

Check the topic against three diagnostic tests:

**Test A — The Four-Word Test**
If the topic can be stated in four or five words, it is almost certainly too broad to research manageably:

| Too broad (static) | Narrowed (action words added) |
|--------------------|-------------------------------|
| Free will in Tolstoy | The conflict between free will and inevitability in Tolstoy's depiction of three battles in *War and Peace* |
| History of commercial aviation | The military's contribution to developing the DC-3 in the early years of commercial aviation |
| Social media and teenagers | How Instagram's design features affect reported anxiety levels in teenage girls aged 13-17 |

The narrowing technique: add nouns derived from action verbs — *conflict*, *contribution*, *effect*, *development*, *influence*, *change*. These imply something is happening, not just existing.

**Caution:** Do not over-narrow. A topic so specific that almost no sources exist (e.g., "the decision to lengthen the wingtips on the DC-3 prototype for military use as a cargo carrier") is also unworkable.

**Test B — The Sentence Test**
Restate the topic as a full sentence. If the result is trivially true, the topic is still a subject, not a research direction:

- "Free will in Tolstoy" → "There is free will in Tolstoy's novels." (trivially true, no inquiry needed)
- "The conflict between free will and inevitability in Tolstoy's depiction of three battles" → "In *War and Peace*, Tolstoy describes three battles in which free will and inevitability conflict." (a claim worth investigating)

**Test C — Question Quality**
Identify which type of problem the current question (if any) represents:

| Problem type | Example | Why it fails |
|---|---|---|
| Settled fact | "Do the Inuit use masks in ceremonies?" | A single source answers it; no analysis needed |
| Dead end | "How many black cats slept in the Alamo the night before the battle?" | Even a correct answer leads nowhere significant |
| Pure speculation | "Would church attendance increase if congregants wore masks?" | No evidence could settle it |
| Yes/No | "Did Lincoln believe in predestination?" | Closes off inquiry the moment you find one source |

Good questions ask *how* and *why* — they invite deeper analysis than *who*, *what*, *when*, or *where*.

### Step 2 — Generate a Question Inventory

**WHY:** Before selecting one question, generating many opens research directions you would otherwise miss. The goal is not to answer yet — it is to map the possibility space so the best question can emerge. Researchers who jump to a single question too early often get stuck when that question dead-ends.

Using the focused topic from Step 1, generate questions across six heuristic categories. Apply each to the user's topic (the masks example from the book illustrates each category):

**History questions**
- How did [topic] come into being? Why? What came before it?
- How has [topic] changed over time? What caused those changes?

**Structure and composition questions**
- How does [topic] fit into a larger system or context?
- How do the parts of [topic] work together? Which parts are most significant?

**Category questions**
- What kinds of [topic] are there? How are they classified?
- How does [topic] compare to or contrast with related phenomena?

**Negative questions** (flip any positive question)
- Why has [topic] *not* changed in a particular way?
- Why does [topic] *not* appear in contexts where you would expect it?

**Speculative "what if" questions**
- What would be different if [topic] never existed, disappeared, or moved to a new context?
- What analogies connect [topic] to other domains?

**Source-suggested questions** (use after initial reading)
- What claim from a source could be extended or tested in a new context?
- Where do sources disagree, and which side has better evidence?
- What questions do sources explicitly leave open at the end?

Record all questions without filtering. The inventory is productive even if most questions are ultimately set aside.

### Step 3 — Select and Elevate the Best Question

**WHY:** Not all questions deserve research. Selecting based on significance — not just personal interest — is what separates research that contributes to a field from research that only satisfies personal curiosity.

**Evaluate each candidate question against these criteria:**

- Would the answer make a reader think about the topic in a new way? (If no: likely a settled fact or dead end)
- Can evidence plausibly exist that could settle it? (If no: purely speculative)
- Does the answer connect to something larger than the question itself? (If no: dead end)

Prefer questions that ask *how* or *why* over those that ask *who*, *what*, *when*, or *where* — the latter are more likely to produce catalog-style reports rather than analysis.

Once you have two or three promising candidate questions, consider combining them into a single broader question that encompasses them all. Multiple related questions often point to one larger organizing question.

Example (from the book): Three Alamo questions — *How have politicians used the story? How have storytellers' motives changed? Whose purposes does each story serve?* — all combine into: *How and why have users of the Alamo story given the event a mythic quality?*

### Step 4 — Apply the 3-Step Significance Formula

**WHY:** A question is not ready for research until you can articulate why someone beyond you cares about its answer. The 3-step formula forces this articulation before you invest significant time gathering evidence. Researchers who skip this step often finish a project and then cannot explain its contribution.

Complete all three parts of this sentence:

```
I am studying/working on [TOPIC]              <- Step 1: Name your topic
because I want to find out [QUESTION]         <- Step 2: State what you don't know
in order to help my reader understand [SO WHAT?]  <- Step 3: Articulate significance
```

**Step 1 — Name the topic** (use action-derived nouns):
```
I am studying the causes of the disappearance of large North American mammals...
I am working on Lincoln's beliefs about predestination and their influence on his reasoning...
```

**Step 2 — Add the direct question** (what you do not know):
```
...because I want to find out whether the earliest peoples hunted them to extinction...
...because I want to find out how his belief in destiny influenced his understanding of the causes of the Civil War...
```

**Step 3 — Answer So What?** (why readers beyond you should care):
```
...in order to help my reader understand whether native peoples lived in harmony with nature or helped destroy it.
...in order to help my reader understand how his religious beliefs may have influenced his military decisions.
```

The third step is the hardest and the most important. It is your ticket into the conversation of your research community. Advanced researchers are judged not by whether their question interests them, but by whether the answer to Step 3 matters to their field.

**If you cannot complete Step 3:** The question may be valid but you are not yet far enough into the topic to see its significance. Write "TBD — research in progress" and return to it after initial reading. Do not abandon the question; begin research, then revisit.

**Peer feedback prompt:** Ask a colleague, roommate, or friend to listen to your three-step sentence. If they respond "So what?" after Step 2, you have not yet answered Step 3 convincingly.

### Step 5 — Deliver the Formulated Question

**WHY:** The user needs three distinct outputs — not one blended answer — because topic, question, and significance serve different downstream functions. The topic goes into the introduction; the question guides source selection; the significance statement becomes the motivation section. Separating them explicitly prevents the common error of conflating topic with question or question with thesis.

Present the output in three parts:

1. **The focused topic** (narrowed from the original subject using action-derived nouns)
2. **The research question** (direct question form, asking how or why, not answerable by a single lookup)
3. **The significance statement** (Step 3 of the formula — why the answer matters to a reader)

Optionally include:
- The full 3-step sentence in one block for easy reference
- A brief note on what type of evidence would be needed to answer the question
- 1-2 anti-pattern warnings if the original topic exhibited them (e.g., "Your original topic 'Social media and teens' was too broad — the action-derived noun 'effect' is what focused it")

## Examples

### Example 1 — Undergraduate research paper

**Input topic:** "Climate change and agriculture"

**Step 1 diagnosis:** Four-word test fails (too broad). Sentence test: "Climate change affects agriculture" — trivially true.

**Narrowed topic:** The effect of shifting precipitation patterns on smallholder wheat yields in sub-Saharan Africa, 2000-2020.

**Research question:** How have changes in seasonal rainfall timing altered crop yields for smallholder wheat farmers in sub-Saharan Africa over the past two decades?

**3-step formula:**
```
I am studying the effect of shifting precipitation patterns on smallholder wheat yields in sub-Saharan Africa
because I want to find out whether yield losses are driven more by total rainfall reduction or by changes in seasonal timing
in order to help my reader understand whether climate adaptation programs should prioritize irrigation infrastructure or planting calendar adjustments.
```

---

### Example 2 — Graduate thesis (from the book)

**Input topic:** "Lincoln and religion"

**Step 1 diagnosis:** Can be stated in three words. Sentence: "Lincoln was religious" — settled fact, no inquiry.

**Narrowed topic:** Lincoln's beliefs about predestination and their influence on his Civil War reasoning.

**Research question:** How did Lincoln's belief in predestination and divine destiny influence his interpretation of the causes and meaning of the Civil War?

**3-step formula:**
```
I am working on Lincoln's beliefs about predestination and their influence on his reasoning
because I want to find out how his belief in destiny and God's will influenced his understanding of the causes of the Civil War
in order to help my reader understand how his religious beliefs may have influenced his military decisions.
```

---

### Example 3 — Professional report context

**Input topic:** "Remote work productivity"

**Step 1 diagnosis:** Yes/no question risk: "Is remote work more productive?" — answerable by a single meta-analysis citation.

**Narrowed topic:** The relationship between remote work policy design (flexibility vs. structure) and knowledge worker output quality in software teams.

**Research question:** How does the degree of schedule flexibility in remote work policies affect code quality and defect rates in software development teams?

**3-step formula:**
```
I am studying the relationship between remote work policy design and software team output quality
because I want to find out whether higher schedule flexibility is associated with better or worse code quality metrics
in order to help my reader understand which remote work policy features organizations should prioritize to maintain engineering quality.
```

---

## Anti-Pattern Quick Reference

| Anti-pattern | Diagnosis signal | Fix |
|---|---|---|
| Topic too broad | Stateable in 4-5 words; sentence version is trivially true | Add action-derived nouns: *effect*, *conflict*, *development*, *influence* |
| Settled-fact question | A single source can answer it | Reframe as *how* or *why* it happened, not *whether* it happened |
| Yes/No question | Question begins with "Does," "Is," "Did," "Are" | Replace with "How," "Why," "In what ways," "To what extent" |
| Dead-end question | Correct answer doesn't connect to anything larger | Add the Step 3 significance test — if you can't complete it, the question is a dead end |
| Pure speculation | No evidence could plausibly settle it | Ask: can I imagine finding data, documents, or observations that would answer this? If no, drop it |
| Over-narrowed | No sources exist; question is hyper-specific trivia | Broaden by one level; the topic should be researchable by a non-specialist |

## References

- See `references/question-inventory-heuristics.md` for the full six-category question generation framework with worked examples across multiple disciplines
- See `references/3-step-formula-templates.md` for fill-in-the-blank templates and discipline-specific variants of the significance formula
