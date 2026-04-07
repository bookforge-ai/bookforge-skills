---
name: source-incorporator
description: Incorporate quoted, paraphrased, and summarized sources into research writing by applying a 3-branch selection decision tree, 3 integration methods for quotations, and a 5-mechanism inadvertent plagiarism prevention checklist. Use this skill when drafting or revising a paper that uses sources and you need to decide whether to quote, paraphrase, or summarize a passage; when you need to weave quotations into your prose grammatically and meaningfully; when you need to make explicit to readers why evidence is relevant; when you must choose a citation style; or when you want to audit a draft for the five most common forms of inadvertent plagiarism before submitting.
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [14]
tags: [research-methodology, academic-writing, citation, source-incorporation, plagiarism-prevention]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Draft text containing source material to incorporate, or a set of source notes (quotations, paraphrases, summaries) to be woven into a paper."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Works from a draft document or a list of source passages. Output: revised draft with properly integrated sources and a plagiarism audit report."
discovery:
  goal: "Produce writing that integrates sources in the form best suited to each passage, integrates quotations grammatically, makes evidence relevant through framing sentences, and is clean of all five forms of inadvertent plagiarism."
  tasks:
    - "Apply the quote/paraphrase/summarize decision tree to each source passage"
    - "Select one of three integration methods appropriate to each quotation"
    - "Add a framing sentence before complex evidence to establish its relevance"
    - "Run the five-mechanism plagiarism audit on every incorporated passage"
    - "Apply or verify the correct citation style for every in-text reference"
  audience: "researchers, students, academics, professionals writing any evidence-based document"
  when_to_use: "When drafting or revising research writing that draws on external sources and must show credibility, accuracy, and respect for intellectual ownership"
  environment: "Draft document or source notes. Research question and target citation style should be known."
  quality: placeholder
---

# Source Incorporator

## When to Use

You are writing a research paper, report, or any evidence-based document and must bring in material from external sources. This skill applies when:

- You have collected source passages and must choose whether to quote, paraphrase, or summarize each one
- You have quoted a source but the quotation is not integrating smoothly into your prose
- You have placed evidence in your paper but readers may not see why it supports your claim
- You want to audit a near-final draft for inadvertent plagiarism before submitting
- You are unsure which citation style to use or how to format in-text references

**The core pattern:** source incorporation is a three-stage decision — (1) choose the right form (quote, paraphrase, or summarize), (2) integrate that form grammatically and meaningfully into your sentence, (3) make the relevance of the evidence explicit with a framing sentence. Then audit every incorporated passage for the five inadvertent plagiarism mechanisms.

Before starting, confirm you have:
- A draft or source notes you want to incorporate
- A working research question or thesis
- Knowledge of your required citation style, or permission to choose one

---

## Context and Input Gathering

### Required Context

- **Draft or source passages:** The text to be incorporated — direct quotations, paraphrases already drafted, or summaries.
- **Target citation style:** Chicago author-title, MLA, Chicago author-date, or APA. If unknown, ask.

### Observable Context

If a draft document is provided, scan for:
- Passages surrounded by quotation marks — check for integration method and framing
- Passages attributed to a source name without quotation marks — check if paraphrase or summary
- Parenthetical references or footnotes — check format against the declared citation style
- Long quoted passages (5+ lines) — check if set as block quotations
- Claims supported by evidence with no explanatory sentence — candidates for framing

### Default Assumptions

- If citation style is unspecified → ask before proceeding; applying the wrong style wastes revision effort
- If source passage length is borderline (4 vs. 5 lines) → use the block format when in doubt; it signals care
- If a passage combines the writer's words with source words invisibly → treat as plagiarism risk regardless of intent
- If source type is legal or statutory text → quotation marks may be omitted per field convention; confirm before flagging

### Sufficiency Check

You have enough to proceed when:
1. You know which passages are the writer's own words and which come from sources
2. You know the required citation style
3. You have at least one source passage to work with

If you cannot distinguish source text from writer text, stop and ask the writer to mark source passages before continuing.

---

## Execution

### Step 1 — Apply the Quote / Paraphrase / Summarize Decision Tree

For each source passage, choose the right form using these three branches. Use only one form per passage; mixing forms on the same passage is a common error.

**Branch 1 — Summarize** when:
- The details in the passage are not essential to your argument
- The source is a background reference, not a central exhibit
- The source is not important enough to warrant close analysis

*Why:* Readers only need what serves your argument. Unnecessary detail weakens focus and suggests you are padding rather than arguing.

**Branch 2 — Paraphrase** when:
- Your argument depends on the details in the passage, but not on the specific words
- You can restate the idea more clearly or concisely than the original
- The original language is technical and your audience needs a plain-language equivalent

*Why:* Paraphrase shows you have genuinely understood the source; quotation can sometimes hide that you have not. Reserve the source's exact words for when they do work a paraphrase cannot.

**Branch 3 — Quote** when one or more of these conditions holds:
- The words themselves are evidence (e.g., a historical document, a legal statute, a primary source statement)
- The words come from an authority whose exact phrasing endorses your claim
- The phrasing is strikingly original or conceptually precise in a way that would be diluted by paraphrase
- You are quoting to disagree and fairness requires stating the view exactly

*Why:* Direct quotation carries the highest evidentiary weight but also the highest reader cost. Every quoted passage asks readers to pause and read carefully. Use that cost purposefully.

**Example application:**

| Passage type | Decision | Reasoning |
|---|---|---|
| Broad historical background on a topic you mention once | Summarize | Details not central to your argument |
| A researcher's four-step method you will explain and apply | Paraphrase | Details matter, but your own clearer phrasing serves readers better |
| An economist's coinage of "creative destruction" as the precise term your argument turns on | Quote | Strikingly original phrase; paraphrase would lose precision |
| A critic's statement of a position you are refuting | Quote | Fairness requires exact language |

---

### Step 2 — Choose an Integration Method for Each Quotation

Once you decide to quote, you must integrate the quotation into your prose. There are two format decisions and three integration methods.

**Format decision — run-in or block:**
- **Run-in quotation:** 4 or fewer quoted lines — integrate directly into your paragraph, surrounded by quotation marks.
- **Block quotation:** 5 or more quoted lines — indent as a separate block, no quotation marks around the block.

*Why the threshold matters:* Long run-in quotations fragment your prose rhythm and are harder to read. Block format signals to readers that a substantial passage follows and they should read it as a unit. Using block format for short passages wastes space and looks evasive.

**Integration method — choose one of three:**

**Method A — Drop in:** Introduce the quotation with a brief identifying phrase (*Author says*, *According to Author*, *As Author puts it*). Use when the quotation is self-explanatory in context.

> Diamond says, "The histories of the Fertile Crescent and China . . . hold a salutary lesson for the modern world: circumstances change, and past primacy is no guarantee of future primacy" (417).

**Method B — Introduce:** Precede the quotation with a sentence that interprets or characterizes what the quotation will show. Use when the quotation needs framing to be understood at all.

> Diamond suggests what we can learn from the past: "The histories of the Fertile Crescent and China . . . hold a salutary lesson for the modern world . . ." (417).

**Method C — Weave:** Grammatically merge the quotation into your own sentence structure. Use when only part of the source sentence is needed or when seamless flow is important.

> Diamond suggests that the chief "lesson for the modern world" in the history of the Fertile Crescent and China is that "circumstances change, and past primacy is no guarantee of future primacy" (417).

*Why three methods:* Drop-in is fastest but can leave readers wondering why the quotation matters. Introduce provides the most interpretive control. Weave demonstrates mastery but risks distorting grammar if done carelessly. Match the method to the complexity of the evidence and the density of argument around it.

**Modifying quotations (permitted):**
- Use ellipsis `. . .` to mark deleted words within a quotation
- Use square brackets `[word]` to change a word so the quotation fits your grammar or to add a clarifying word
- Never change the meaning of the quotation while modifying it — this is a form of dishonesty

---

### Step 3 — Frame Complex Evidence Before Presenting It

Evidence never speaks for itself, especially long quotations or data tables. Readers who encounter unframed evidence must guess why it is relevant.

**The framing pattern:**
1. State your claim
2. Add a framing sentence that explains what the evidence will show and why it is relevant (the reason)
3. Report the evidence

*Without framing (ineffective):*
> When Hamlet comes upon his stepfather, Claudius, at prayer, he demonstrates cool rationality: [long quotation from Hamlet 3.3]

The connection between the claim ("cool rationality") and the quotation is not visible in the text.

*With framing (effective):*
> When Hamlet comes upon his stepfather at prayer, he demonstrates cool rationality. He impulsively wants to kill Claudius but pauses to reflect: if he kills Claudius while praying, Claudius will go to heaven, but Hamlet wants him damned to hell, so he coolly decides to kill him later: [quotation]

Now the evidence and claim are linked. Readers see exactly which aspect of the quotation matters.

*Rule:* Introduce complex evidence with a sentence explaining what you want readers to get out of it. This applies equally to long quotations, data tables, and figures.

---

### Step 4 — Run the Five-Mechanism Inadvertent Plagiarism Audit

For every source passage you have incorporated — quotation, paraphrase, or summary — check each of the five mechanisms. A single failure on any mechanism is a plagiarism risk regardless of intent.

**Mechanism 1 — Uncited paraphrase or summary**
*Check:* Does every paraphrase and summary have a citation? Even if you never quoted a single word, using someone's ideas without attribution is plagiarism.
*Action:* Add the citation immediately when you write the paraphrase; do not wait until a later revision pass — you may not remember the source originated with someone else.

**Mechanism 2 — Unclosed quotation**
*Check:* If you cite a source and include its words, are those words surrounded by quotation marks (or set as a block quotation)? Even a single borrowed line without quotation marks is plagiarism even if you cited the source.
*Action:* For strikingly original or technically precise phrases, always enclose in quotation marks the first time you use them, even if the phrase is brief. Once you have introduced and cited a phrase, you may use it subsequently without marks.

**Mechanism 3 — Too-close paraphrase**
*Check:* Can you run your finger along your paraphrase sentence and find synonyms for the same ideas in the same order as in the source? If yes, the paraphrase is too close.
*Action:* Read the original, look away, think about it, then write the paraphrase without looking back. Check that the resulting sentence cannot be matched word-for-word-synonym against the original. If it can, revise again.

*Too close (plagiarism):*
> Success seems to depend on a combination of talent and preparation. However, when psychologists closely examine the gifted and their careers, they discover that innate talent plays a much smaller role than preparation (Gladwell 38).

*Acceptable paraphrase:*
> As Gladwell observes, summarizing studies on the highly successful, we tend to overestimate the role of talent and underestimate that of preparation (38).

**Mechanism 4 — Uncited non-common-knowledge idea**
*Check:* For every idea that is not your own, is it either common knowledge in your field or cited? The test: is this idea (a) associated with a specific person AND (b) new enough not to be part of the field's common knowledge? If both, it must be cited.
*Action:* When in doubt, cite. Citing when unnecessary makes you look careful; not citing when necessary makes you look dishonest.

**Mechanism 5 — Free-content fallacy**
*Check:* Did you use any content from freely available online sources without citing? Free and publicly available does not mean unattributed. Website text, Wikipedia, open-access articles — all require citation.
*Action:* Apply the source-recognition test: if the person you borrowed from read your writing, would they recognize their words or ideas? If yes, cite and enclose any exact words.

---

### Step 5 — Apply the Correct Citation Style

Choose and consistently apply one style. There are two structural patterns:

**Author-title pattern** (humanities): bibliography entry begins Author → Title → publication data
**Author-date pattern** (sciences, social sciences): bibliography entry begins Author → Date → title → publication data

The date-first pattern serves fields where recency matters most — readers can immediately spot how old a source is.

**Four common styles:**

| Style | Pattern | In-text format | List name |
|---|---|---|---|
| Chicago author-title | Author-title | Superscript footnote/endnote | Bibliography |
| MLA | Author-title | (Author page) — no comma | Works Cited |
| Chicago author-date | Author-date | (Author date, page) | Bibliography |
| APA | Author-date | (Author, date, p. page) | References |

**Key in-text mechanics:**
- If you name the author in your sentence, drop the name from the parenthetical: *Smith argues that prices rise (1999, 45)* → not *(Smith 1999, 45)*
- If citing multiple works by the same author, add a short title: *(Kay, A Life, 220)*
- If a paraphrase or summary extends across multiple paragraphs, cite only once at the end
- Cite each passage that comes from a different page individually

*Why citation style details matter:* Readers use citations to locate sources. Every deviation from style convention — a missing comma, a wrong order of elements — potentially breaks the bibliographic trail and signals careless work. Experienced readers judge a writer's reliability partly by citation precision.

---

## Output

Deliver the revised text with:

1. **Integrated source passages** — each passage in the correct form (quote, paraphrase, or summary) with the integration method applied
2. **Framing sentences** — added before any complex or long evidence
3. **Plagiarism audit log** — a brief checklist confirming each of the five mechanisms was checked, with notes on any passages that required remediation
4. **Citation style consistency check** — confirmation that in-text references follow the declared style

If working on a full draft, deliver the audit log as an appendix to the revised draft. If working on individual passages, deliver the audit log inline after each passage.

---

## Quick Reference

**Decision tree (one choice per passage):**
- Source not central → **summarize**
- Details matter, not words → **paraphrase**
- Words are evidence / authority / unforgettable / fair-to-quote-to-disagree → **quote**

**Integration methods (for quotations):**
- Self-explanatory in context → **drop in** (*Author says, . . .*)
- Needs setup → **introduce** (sentence + colon + quotation)
- Partial quotation needed → **weave** (grammatically merge)

**Five plagiarism risks:**
1. Paraphrase/summary without citation
2. Source words without quotation marks (even with citation)
3. Too-close paraphrase — same synonyms, same order
4. Non-common-knowledge idea without citation
5. Free/online content treated as unattributable

**Citation style selector:**
- Humanities → Chicago author-title or MLA
- Sciences / social sciences → Chicago author-date or APA
- When unsure → ask your target venue
