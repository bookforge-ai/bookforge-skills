---
name: prose-clarity-reviser
description: "Revise dense, unclear prose into clear, readable sentences by applying four diagnostic principles — characters-as-subjects, actions-as-verbs, old-before-new information flow, and complexity-last sentence endings. Use this skill whenever the user shares a draft passage, paragraph, or document and asks you to make it clearer, more readable, easier to follow, less dense, less academic-sounding, or better written — even if they don't use those words. Also triggers on: \"can you revise this,\" \"this feels clunky,\" \"my advisor said this is unclear,\" \"make this flow better,\" \"my writing sounds stilted,\" or any request to improve prose style in research papers, reports, essays, grant proposals, or professional documents. Apply all four principles end-to-end; return a revised version with brief annotations showing what changed and why."
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [17]
tags: [research-methodology, prose-revision, writing-style, clarity, academic-writing]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "One or more paragraphs of draft prose to revise — a sentence, paragraph, section, or full document excerpt"
  tools-required: []
  tools-optional: [Read, Write]
  mcps-required: []
  environment: "Any agent environment. Works on pasted text or referenced files."
---

# Prose Clarity Reviser

## When to Use

The user has written prose — in any research, academic, or professional context — and wants it to be clearer or more readable. Typical triggers:

- User pastes a paragraph and says "this is confusing" or "make this clearer"
- User shares a draft section and asks for a style pass or readability revision
- A supervisor, editor, or reviewer has flagged the writing as dense, abstract, or hard to follow
- The user says their writing sounds too "academic," too stiff, or too indirect
- The user asks why their sentences don't "flow" or why readers keep re-reading them

**Do not apply these principles as the user writes new text.** These are revision tools — apply them only after a draft exists. Applying them during drafting causes paralysis.

**Scope:** This skill handles sentence-level and paragraph-level style revision only. It does not restructure arguments, reorganize sections, or evaluate evidence. For those concerns, use a different skill.

## Context

### Required (must be present before proceeding)

- **The text to revise:** One or more sentences or paragraphs. If the user says "revise my paper" without sharing text, ask them to paste the passage.

### Useful but not required

- **Audience:** Who are the intended readers? Specialists, generalists, students, peers? Knowing the audience determines whether field-specific nominalizations can stay as-is (see Principle 2 nuance below).
- **Purpose of the passage:** Is this a methods section, an argument, an introduction? This affects how active vs. passive voice should be used (see Principle 4).

## The Four Principles

Every unclear sentence violates one or more of these four structural rules. Diagnose before revising.

---

### Principle 1: Characters as Subjects

**The rule:** The grammatical subject of every clause should name the main character in that clause's story — the entity doing, experiencing, or driving the action.

**Why it matters:** Readers orient themselves by asking "who or what is this sentence about?" When the subject is an abstraction, a nominalization, or an empty phrase, readers lose the thread. They have to work backward to reconstruct the actual agent.

**Diagnostic — underline the first 6–7 words of every clause.** Then ask:
1. Does the subject name a concrete character (person, organization, organism, system, concept your field treats as an active agent)?
2. If the subject is abstract, is it an abstraction your readers already treat as a familiar actor (e.g., "inflation," "the immune system" in a medical paper)?

**If no to both — revise:**
1. Identify who or what the sentence is really about. If you cannot name a character, invent one (use "we," "researchers," "the study").
2. Make that character the grammatical subject.
3. Keep subjects short, specific, and concrete. Long whole-subjects (e.g., "The standardization of indices for the measurement of mood disorders") signal that the real character has been buried.

**Field-specific note:** In your discipline, the main characters may be abstractions — "monetary policy," "institutionalization," "gene expression." This is acceptable when those abstractions are already familiar to your audience and can be treated as acting entities. The problem occurs when you layer additional abstractions around them as additional nominalizations.

---

### Principle 2: Actions as Verbs (Nominalization Detection)

**The rule:** The key action in every clause should appear as a verb, not as a noun derived from a verb or adjective (a nominalization).

**Why it matters:** When actions become nouns, three things go wrong simultaneously: (1) you lose the specific verb and replace it with a vague one like *make*, *have*, *do*, or *be*; (2) you bury the characters as modifiers or objects of prepositions; (3) you clutter the sentence with articles and prepositions that would not be needed if the action were a verb.

**Nominalization markers to scan for:**
- Suffixes: *-tion, -ness, -ment, -ence, -ity, -ance, -al* (when used as noun)
- Common nominalizations: *analysis, assumption, consideration, development, establishment, examination, implementation, improvement, indication, investigation, provision, requirement, utilization*
- Some nominalizations look identical to their verb: *change, delay, report, plan, review, shift, study* — context determines which they are

**Diagnostic — for each nominalization you find, ask:**
1. Is this the subject of a verb? If so, and if it derives from a verb, that verb has been buried.
2. Is this from my field's standard vocabulary — a term readers recognize as a concept, not just a buried verb? (e.g., "hospitalization," "measurement" in a clinical paper) If yes, it may stay.

**To revise:**
1. Find the buried verb inside the nominalization (e.g., *consideration* → *consider*, *establishment* → *establish*, *utilization* → *use*).
2. Make that verb the main verb of the clause.
3. Move the character (now freed from modifier position) back to subject position.

**The exception:** Do not convert every nominalization into a verb. When a nominalization refers to a concept that your readers treat as familiar and established — especially if you introduced it earlier in the passage — leave it as a noun. Abstract nouns used to echo earlier content serve the old-before-new principle (Principle 3). Revise unnecessary nominalizations; keep necessary ones.

---

### Principle 3: Old Before New (Information Flow)

**The rule:** Begin each sentence with information readers already know (old) — either from the previous sentence or from shared context — and place new information at the end.

**Why it matters:** Readers build meaning incrementally. When each sentence opens with something familiar, readers have an anchor. They can attach the new information at the end to something they already hold in mind. When sentences open unpredictably, readers cannot connect them; the passage feels disjointed even if every individual sentence is well-formed.

**This principle overrides Principle 1 when they conflict.** If you must choose between starting with a character or starting with familiar information, always choose the familiar information.

**Diagnostic — underline the first 6–7 words of every sentence (skip short introductory phrases like "At first," "For the most part").** Then run your eye down the page and ask:
1. Do the sentence-opening words form a consistent, related set? They do not need to be identical, but they should name people or concepts that your readers will see as clearly related.
2. Does each sentence begin with a word or phrase that echoes something from the previous sentence or from shared context?

**If no — revise:**
1. Reorder: move the familiar information to the front of the sentence.
2. Use pronouns, synonyms, or summary nouns to refer back to what was just mentioned.
3. Move new, complex, or technical information to the end of the sentence. This often requires using the passive voice (see Principle 4).

**Active vs. passive and information flow:** The passive voice is not a flaw. Its primary function is to flip old and new information — to move older, familiar information from the end of one sentence to the beginning of the next. When familiar information would naturally be the object of an active verb, use the passive to promote it to subject position. Do not use passive or active based on a blanket rule; use whichever puts the right information at the beginning.

---

### Principle 4: Complexity Last (Sentence Endings)

**The rule:** Place the newest, most complex, most technically demanding information at the end of a sentence, never at the beginning.

**Why it matters:** Readers can handle complexity better when they arrive at it from stable ground. If a sentence opens with a long, complex subject or an unfamiliar technical phrase, readers must decode it before they even know what the sentence is doing. Placing complexity last lets readers approach it with context already built.

**Three contexts where this principle is especially important:**
1. **Introducing a new technical term** — the term should appear in the last few words of the sentence, not the first.
2. **Presenting a long, complex bundle of information** — if a clause requires a long phrase or subordinate clause, push it to the sentence's end.
3. **Opening a paragraph** — the last few words of the paragraph's opening sentence should name the key terms that the rest of the paragraph will develop.

**Diagnostic — underline the last 5–6 words of every sentence.** Ask:
1. Are those words the most important, complex, or emphatic in the sentence?
2. Are they technical terms being introduced for the first time?
3. Are they concepts that the next several sentences will develop?

**If no — revise:** Move the most important, newest content to the sentence's end. This may require splitting the sentence, using a passive verb, or reordering clauses.

---

## Active vs. Passive: The Decision Criterion

Use active voice when:
- The writer/researcher is performing an action that only they can perform: *argue, conclude, suggest, claim, design, prove*
- The action you want to emphasize is something only the authors did (rhetorical or intellectual ownership)

Use passive voice when:
- Describing a process that any qualified person could repeat (standard in methods sections of scientific writing)
- You need to move familiar information to the front of a sentence (information flow rule)

Do not use active or passive based on a blanket stylistic rule. The passive is not a sign of weak writing — it is a structural tool for managing information flow.

---

## Revision Protocol

Apply in this order. Do not try to apply all four principles simultaneously.

**Pass 1 — Diagnosis (mark up the text)**
1. Highlight the first 6–7 words of every clause. Skip short introductory phrases.
2. Scan for nominalizations: look for words ending in *-tion, -ness, -ment, -ence, -ity*. Mark each one.
3. Ask of each highlighted opening: Is this a character? Is this familiar information?
4. Highlight the last 5–6 words of every sentence. Ask: Is this the most important content?

**Pass 2 — Character and verb revision (Principles 1 and 2)**
5. Find sentences where the subject is not a character. Identify the real character.
6. Find nominalizations. Determine which are field-standard (keep) and which bury a verb (convert).
7. Rewrite: make real characters the subjects of specific, concrete verbs.

**Pass 3 — Information flow revision (Principle 3)**
8. Reorder sentence openings to begin with familiar information.
9. Shift new, complex, or technical content to sentence ends.
10. Adjust active/passive as needed to serve information flow — not as a separate stylistic choice.

**Pass 4 — Sentence endings (Principle 4)**
11. Check sentence endings. If the most important content is buried mid-sentence, reorder.
12. Check paragraph-opening sentences. Confirm that the last few words introduce the paragraph's key term.

**Pass 5 — Output**
13. Produce the revised text.
14. For each paragraph, add a brief annotation listing: what changed and which principle was applied. Format:
    - `[P1]` — character moved to subject
    - `[P2]` — nominalization converted to verb
    - `[P3]` — old-before-new reordering
    - `[P4]` — complexity moved to sentence end
    - `[P3+voice]` — passive/active adjusted for information flow

---

## Examples

### Example 1: Heavy Nominalization + Abstract Subject

**Before:**
> The standardization of indices for the measurement of mood disorders has now made possible the quantification of patient response as a function of treatment differences.

**After:**
> Having standardized indices for measuring mood disorders, we now can quantify patients' responses to different treatments.

**Annotations:**
- `[P2]` *standardization* → *standardized*, *measurement* → *measuring*, *quantification* → *quantify*, *response* → *responses*
- `[P1]` Subject changed from the abstract nominalized phrase to *we*
- `[P2]` Vague verb *made possible* replaced by specific verb *can quantify*

---

### Example 2: Information Flow Broken Across Sentences

**Before:**
> Locke frequently repeated himself because he did not trust the power of words to name things accurately. Seventeenth-century theories of language, especially Wilkins's scheme for a universal language involving the creation of countless symbols for countless meanings, had centered on this naming power. A new era in the study of language that focused on the ambiguous relationship between sense and reference begins with Locke's distrust.

**After:**
> Locke often repeated himself because he distrusted the naming power of words. This naming power had been central to seventeenth-century theories of language, especially Wilkins's scheme for a universal language involving the creation of countless symbols for countless meanings. Locke's distrust begins a new era in the study of language, one that focused on the ambiguous relationship between sense and reference.

**Annotations:**
- `[P3]` Sentence 2 rewritten to open with *This naming power* — picks up the phrase from sentence 1's end
- `[P3]` Sentence 3 rewritten to open with *Locke's distrust* — picks up the concept from sentence 2's end
- `[P2]` *distrust of* → *distrusted* (minor nominalization)
- `[P4]` New technical concept (*ambiguous relationship between sense and reference*) moved to sentence 3's end

---

### Example 3: Complexity at the Front, Technical Term Placement

**Before:**
> The monoamine hypothesis has been the leading biological account of depression for over three decades.

**After:**
> For over three decades, the leading biological account of depression has been the monoamine hypothesis.

**Annotation:**
- `[P4]` Technical term *monoamine hypothesis* moved to sentence end, where new technical terms belong when first introduced. The familiar framing (*for over three decades*) now anchors the sentence's opening.

---

## Field-Specific Notes

**Sciences (natural, social, clinical):** Use passive in methods sections to describe repeatable processes. Use active and first person (*we conclude*, *we argue*, *we designed*) when describing intellectual contributions unique to the authors. Do not use passive to appear "objective" — it only changes whose story is being told.

**Humanities:** Main characters are often real people or abstract concepts (*democracy*, *modernity*, *the text*). These abstractions can stay as subjects if they are familiar to your audience and you are not layering additional nominalizations around them.

**Technical and policy writing:** Characters are often institutions, systems, or policies. Keep them as subjects. Avoid nominalizing verbs that describe what those institutions actually do (*implement* vs. *implementation of*, *regulate* vs. *regulation of*).

---

See `references/before-after-sentence-pairs.md` for 15+ additional before/after sentence pairs illustrating all four principles across different academic disciplines.
