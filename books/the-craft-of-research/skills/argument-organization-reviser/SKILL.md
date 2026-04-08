---
name: argument-organization-reviser
description: "Revise the structural organization of a research paper draft by applying a four-level top-down procedure — Frame (intro/conclusion alignment), Argument (section reasons + evidence ratios), Paper Organization (key-term threading + section signals), and Paragraphs (topic sentence placement + length). Use this skill whenever the user has a complete draft and asks to revise, reorganize, or strengthen its structure — not its prose style. Triggers include: user shares a draft paper and asks for structural feedback; user says sections feel disconnected or the argument is hard to follow; user's introduction and conclusion seem to contradict or not reinforce each other; user suspects their sections lack clear points or bury them in the middle; user cannot tell whether their evidence-to-reasoning ratio is balanced; user's paragraphs open with evidence rather than claims; user is preparing to submit and wants a final organizational pass. Also triggers on: \"revise my structure,\" \"does my argument hold together,\" \"my advisor said the organization is unclear,\" \"do my sections flow,\" \"I need to check the coherence.\" This skill applies structural revision only — it does NOT revise prose style or sentence clarity (use prose-clarity-reviser for that), and does NOT rebuild an argument from scratch (use research-argument-builder for that)."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-craft-of-research/skills/argument-organization-reviser
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [13]
tags: [research-methodology, academic-writing, revision, organization, argumentation]
depends-on: [research-paper-planner]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "A complete or near-complete draft of a research paper, report, or analytical essay — any length, any field"
  tools-required: [Read]
  tools-optional: [Write]
  mcps-required: []
  environment: "Any agent environment. User supplies draft as pasted text or a file path."
discovery:
  goal: "Apply the four-level top-down revision procedure to a draft, producing annotated diagnoses and specific repair prescriptions at each level before moving to the next"
  tasks:
    - "Level 1: Check frame — verify introduction and conclusion boundaries are visible, main point appears at/near end of introduction, conclusion point is specific and contestable"
    - "Level 2: Check argument — verify each major section has its own point, evidence ratio >= 1/3 per section, acknowledgments present, warrants surfaced"
    - "Level 3: Check paper organization — verify key terms thread through sections, section joints are signaled, each section is clearly tied to the whole"
    - "Level 4: Check paragraphs — verify topic sentences open or close paragraphs (not buried), paragraph lengths are appropriate, breaks signal transitions"
    - "Cool-and-paraphrase test — skim structure only and paraphrase; check whether the paraphrase matches the intended argument"
    - "Abstract diagnostic — if field requires one, assess whether the abstract matches the three-component structure"
  audience: "Researchers, students, analysts, and professionals with a complete draft who need structural revision before submission"
  triggers:
    - "User shares a draft paper and asks for structural feedback or revision"
    - "Introduction and conclusion feel disconnected or contradictory"
    - "Sections feel like independent essays rather than parts of one argument"
    - "User cannot locate the main point in the introduction"
    - "Evidence vastly outnumbers reasoning or vice versa"
    - "Paragraphs open with evidence or quotations rather than claims"
    - "User preparing to submit and wants a final structural pass"
---

# Argument Organization Reviser

## When to Use

You have a complete draft — or near-complete draft — of a research paper, report, or analytical essay. The argument is already built. What you need now is structural revision: making the organization of your draft as clear to readers as the argument is to you.

Structural revision is different from prose revision. This skill addresses:
- Whether your introduction and conclusion frame the same argument
- Whether each section carries its own distinct reason
- Whether the evidence-to-reasoning ratio is balanced
- Whether key concepts thread visibly through the paper
- Whether paragraphs are properly anchored

It does **not** address sentence clarity, nominalization, or information flow. For those concerns, use `prose-clarity-reviser` after completing this skill.

**A note on order:** Revise top-down, from large structure to small. Do not fine-tune paragraph sentences before confirming that the sections those paragraphs belong to are correctly placed. Time spent polishing a section that later gets cut or moved is wasted.

**Preconditions:**
- A draft exists. If the user has only a plan or outline, redirect to `research-paper-planner`.
- If the argument itself is missing (no main claim, no reasons), redirect to `research-argument-builder`.

---

## Input Gathering

### Required

- **The draft:** Full text, pasted or provided as a file path. If only a section is provided, note that the diagnosis will be partial.
  -> Ask: "Please share the draft you want to revise structurally — paste it here or give me the file path."

### Useful

- **Field and genre:** Knowing whether this is a lab report, a humanities seminar paper, a policy brief, or a thesis chapter affects what conventions govern heading use, abstract format, and where the main point should appear.
- **Target audience:** Expert readers vs. generalists affects how much background and how many key-term definitions are needed.
- **Submission deadline and purpose:** If submission is imminent, prioritize Levels 1 and 2 only.

---

## Execution

Work strictly top-down. Complete each level's diagnosis and repair before descending to the next. This order matters because: a repositioned section changes every paragraph in it; a repositioned main point changes the meaning of both introduction and conclusion. Fixing sentences before fixing structure is like painting walls before fixing the foundation.

---

### Level 1 — Revise the Frame

**What this level checks:** Do readers know instantly where your introduction ends, where your conclusion begins, and where your main point is stated?

Readers need to recognize three things instantly and unambiguously:
1. Where the introduction ends
2. Where the conclusion begins
3. Which sentence in one or both states the main point

**Why this matters:** Readers do not read word by word, adding up detail. They begin with a sense of the whole — where the paper is going and why. If the frame is not visible, readers spend cognitive effort searching for orientation instead of engaging with the argument.

**Diagnosis — check these three things:**

**1a. Are the introduction and conclusion boundaries visible?**

Look for one of these markers:
- An extra blank line (white space) separating the introduction from the body
- A heading marking where the body or first major section begins
- A heading marking the conclusion

If neither exists, readers may not know when your introduction ends.

-> If boundaries are missing: add white space or headings at those joints. (Check whether your field permits or expects headings — if not, use extra space.)

**1b. Is your main point stated at or near the end of your introduction?**

Find the last two or three sentences of your introduction. Does one of them state a specific, contestable claim — what the whole paper argues?

Watch for the weak form: an introduction that ends with a topic announcement ("In this paper I will discuss...") rather than a claim ("This paper argues that..."). A topic announcement tells readers what you will write about; a claim tells them what you are arguing. Readers need the claim.

> Example of a topic announcement (weak): "In this paper I will discuss the reasons for the Crusades."
> Example of a claim (strong): "The Crusades were driven not only by religious zeal but by shrewd political moves to unify the Roman and Greek churches in the face of internal forces threatening to tear them apart."

-> If the main point is absent from the introduction: draft a point sentence (one or two sentences, specific and contestable) and place it at the end of the introduction. It should name the key concepts the body will develop.

-> If you are writing in a field where the convention is to reserve the main point for the conclusion (some humanities traditions): your introduction still needs a "launching point" — a sentence that introduces the key concepts the paper will explore, even if it does not state the full conclusion.

**1c. Do your introduction point and conclusion point align?**

Read the point sentence in your introduction and the point sentence in your conclusion side by side.

They should:
- Not contradict each other
- Not be identical — the conclusion's version should be more specific, more developed, and more directly address the "so what?" question

> Good alignment example: Introduction claims "political concerns drove the Crusades as much as religious ones." Conclusion claims "the political calculations of Urban II and Gregory VII — specifically their need to prevent Byzantine schism — shaped the Crusades more decisively than theological unity arguments did."

-> If they contradict: one of the two is wrong; decide which version of the argument you actually made in the body, then revise the other to match.
-> If they are identical word for word: develop the conclusion's version; it should add something the introduction could not say before the argument was made.

---

### Level 2 — Revise the Argument

**What this level checks:** Does the structure of your paper match the structure of your argument? Is the evidence-to-reasoning ratio sound?

Do this only after Level 1 is resolved. A frame you cannot trust will mislead your assessment of the argument.

**Why this matters:** Your argument consists of a main claim supported by reasons, each backed by evidence. If your sections do not map onto that structure — if sections mix multiple reasons, or contain only evidence with no stated reason, or contain stated reasons with no evidence — readers cannot follow the argument even if the frame is clear.

**2a. Does each major section carry exactly one reason supporting the main claim?**

Go through each major section. For each one, ask: *What is the one reason this section asserts?* Write it in a sentence at the top of a blank page.

- If you cannot state a reason for a section, the section may be context, background, or evidence — not a structural section of the argument. Determine whether it belongs as a subsection inside another section or as background before the argument begins.
- If a section contains two distinct reasons, split it into two sections.
- If two sections contain the same reason expressed differently, merge them.

> Example: A section titled "Evidence from Historical Documents" contains both the reason "documentary evidence shows political motivation" and separate evidence for a second reason about ecclesiastical authority. These need to be separated.

**2b. Does each section strike a sound balance between reasons and evidence?**

In each section, identify every item that counts as evidence: summaries, paraphrases, quotations, facts, figures, graphs, tables, reported cases — anything you took from a source.

Apply this test: **If evidence and its explanation account for less than roughly one-third of a section, you probably do not have enough evidence for that reason.** If you have extensive evidence but few or no stated reasons, you may have a data dump — information without analytical claim.

-> Too little evidence: find additional data, or narrow the section's claim to match what your evidence actually supports.
-> Data dump (evidence without reasoning): write a sentence stating what all this evidence adds up to — the reason it supports. Place that sentence at the top of the section.

**2c. Is your evidence reliable? Have you acknowledged objections and expressed warrants?**

- Check data and quotations against your notes. Errors of fact undermine even a structurally sound argument.
- Make sure every quotation or data item is explicitly connected to the reason it supports. Do not assume the connection is obvious.
- For each section, identify the most likely objection a skeptical but fair reader would raise. Have you acknowledged it? Have you responded to it?
  -> Ask yourself: *Why do I believe this? Am I really making as strong a point as I think? What about...?* Answer the objections that matter.
- For each section, identify the unstated warrant — the principle that connects the evidence to the reason. Ask: would a reader in this field accept this warrant without argument? If not, state it and support it before the reason.

---

### Level 3 — Revise the Organization of the Paper

**What this level checks:** Does the paper cohere? Do readers see it as one argument rather than separate sections that happen to share a cover page?

Do this only after Levels 1 and 2 are resolved.

**Why this matters:** Coherence is not a feeling — it has a structural cause. Readers experience a paper as coherent when key terms from the main claim recur visibly throughout the paper, when section beginnings signal how each section relates to what came before, and when each section clearly contributes to the whole.

**3a. Do key terms thread through the whole paper?**

Locate your main point sentence in the introduction. Circle the words that name the central concepts your argument depends on — the terms that define your specific question, not the general vocabulary of your field.

> Example from a paper on the Crusades: circle *political concerns*, *unity*, *internal forces*, *dividing*. These are not general medieval history terms — they are the specific concepts your argument turns on.

Now go through the body:
- Circle those same terms wherever they appear in the body.
- Underline related words — synonyms, associated concepts, terms in the same semantic family.

**Test:** Does at least one of these key terms appear in most paragraphs? If a passage goes several paragraphs without any key term, readers may conclude the paper has wandered.

-> If a passage lacks key terms entirely: try adding a few. If that feels forced, the passage may be off-topic — consider cutting or rewriting it so it connects to the argument.

**3b. Is the beginning of each major section clearly marked?**

Read through the paper and ask: could you quickly and confidently insert section headings to mark where each major section begins?

- If yes: your organization is probably visible to readers. (Insert the headings, or confirm existing ones are accurate.)
- If you struggle to identify where one section ends and another begins: readers will struggle too. Consider adding white space, transition sentences, or headings.

-> If your field prohibits headings: add an extra blank line at the major joints and open each new section with a transition sentence that signals the shift.

**3c. Does each section signal how it relates to the preceding section?**

The first words of each major section should tell readers why it comes where it does. Readers need to understand not just where sections begin but why they appear in this order.

Useful signal phrases:
- "More important..." (escalation)
- "The other side of this issue is..." (counterargument or contrast)
- "Some have objected that..." (acknowledgment)
- "One complication is..." (qualification)
- "First... Second..." (explicit enumeration)
- "As a result..." (consequence)

-> Review the opening sentence of each section. Does it signal the logical relationship to the previous section? If not, add a brief transition phrase or sentence.

**3d. Is the point of each section clearly stated?**

For each section, locate the sentence that states the section's point — what it argues, not merely what it discusses.

- Prefer stating the section point at the end of the section's introductory paragraph, not buried mid-section. Readers need to know early what a section is arguing.
- For sections longer than four to five pages, consider also restating the point and summarizing the argument at the section's close.

**3e. Do the key terms of each section uniquely distinguish it from the others?**

For each section, repeat the key-term exercise: circle the terms in that section's point sentence (not the whole-paper terms, but the terms unique to this section). Check whether those terms run through the section.

- If you find no unique key terms, the section may not be contributing a new idea — it may be repeating another section. Consider merging them.
- If the same unique key terms run through two sections, those sections may overlap. Consider merging or sharpening the distinction.

---

### Level 4 — Check the Paragraphs

**What this level checks:** Are paragraphs properly anchored by topic sentences? Are they the right length?

Do this only after Levels 1–3 are resolved. Moving sections in Level 3 changes which paragraphs exist and where they sit.

**Why this matters:** Paragraphs are the unit at which readers test whether they understand what they are reading. Each paragraph must signal its key concept at or near its opening — otherwise readers cannot connect what they are reading to the section's point.

**4a. Does each paragraph signal its key concept near the opening?**

Open each paragraph with one or two sentences that name its key concept and orient readers to what follows. This is not the same as stating a formal "topic sentence" — the goal is to give readers an anchor before they encounter the detail.

- If the paragraph's point is not stated in the opening, it should appear in the paragraph's final sentence. Never bury the point in the middle.
- If neither the first nor the last sentence states the point, revise: move the point sentence to the opening or the close.

> Example: A paragraph opening with "In 1095, Urban II gave a speech at the Council of Clermont..." buries the analytical point. Better: "Urban II's Council of Clermont speech reveals more political calculation than religious urgency. In 1095..."

**4b. Are paragraphs the right length?**

There is no universal rule, but:
- Short paragraphs of two or three sentences suggest underdeveloped points. If a series of paragraphs are this short, either merge the ones making related points or develop each point further.
- Long paragraphs exceeding one page may mean the point is not sharply focused, or that the paragraph is doing the work of two. Consider splitting: give each idea its own paragraph.
- Use short paragraphs deliberately to emphasize a transition or highlight a key point — the visual pause draws attention.

**4c. Do paragraph breaks signal transitions effectively?**

Paragraph breaks function like pauses in a conversation: they give readers a moment to process a point before moving on. Use a break:
- After making a strong or complex point (let it land)
- When transitioning to a new but related idea
- When you shift from evidence to analysis or vice versa

---

### Level 5 — Cool-and-Paraphrase Test

**What this test does:** Checks whether the structure you have revised is legible at the skimming level — the level at which readers first encounter a paper and decide whether to engage with it.

**Why this matters:** You know your argument too well to test it as your readers will encounter it. This test forces you to read like a stranger.

**How to run it:**

1. Set the draft aside. Do not read it for at least a day if possible. (If time is short, skip directly to step 2.)
2. Return to the draft and skim only its structure: the introduction, the first paragraph of each major section, and the conclusion. Do not re-read the full body.
3. Based only on what you skimmed, paraphrase the paper to yourself (or to someone else): What is the problem this paper addresses? What does it argue? What are the main reasons? What is the significance?
4. Does the paraphrase match the argument you intended? If yes, the structure is working. If not — if parts are missing, confused, or inverted — the gaps are where the structure fails.

-> If you can find someone else to do the skimming and paraphrasing: their paraphrase will predict with reasonable accuracy how well your final readers will understand the argument. Consider their version seriously, even if you disagree with specific suggestions.

---

## Abstract Diagnostic (if applicable)

If your field requires an abstract, use the abstract as an additional diagnostic after the cool-and-paraphrase test.

**Why:** An abstract must compress the whole paper's argument into a paragraph. If you cannot write a coherent abstract, the paper's structure is probably not coherent.

An abstract should do three things (the same three things an introduction does, compressed):
1. State the research problem or context
2. Announce the key themes or approach
3. State the main point or a launching point that anticipates it

Three common patterns:

| Pattern | Structure | When to use |
|---|---|---|
| **Context + Problem + Main Point** | 1–2 sentences of context, 1–2 sentences of problem, 1 sentence of result | When you have a specific result to state upfront |
| **Context + Problem + Launching Point** | Same, but states the nature of the investigation rather than the result | When the result is complex or when disciplinary convention defers the conclusion |
| **Summary** | Context + problem + compressed argument (methods, evidence, and procedures) + main point | Required in many scientific and social-scientific journals |

-> If you cannot state your main point in one sentence for the abstract, return to Level 1 and revise the introduction's point sentence first.

-> For discoverability: put your most important search keywords in both the title and the first sentence of the abstract. A future researcher searching for your work will find it through those terms.

---

## Distinguishing This Skill from Adjacent Skills

| Concern | Use this skill | Use another skill |
|---|---|---|
| Sentences are dense or unclear | No | `prose-clarity-reviser` |
| Main claim and reasons need to be built | No | `research-argument-builder` |
| Draft does not exist yet; planning a structure | No | `research-paper-planner` |
| Introduction and conclusion need full writing | No | See references/introduction-conclusion-revision.md |
| Objections and counterarguments need developing | Partially (Level 2) | `counterargument-handler` |

---

## Examples

### Example A: Introduction/Conclusion Misalignment (Level 1)

**Introduction point (end of intro):** "This paper will explore the political and religious motivations behind the First Crusade."

**Conclusion point:** "The efforts of Urban II and Gregory VII were shrewd political moves to unify the Roman and Greek churches and prevent the breakup of the empire from internal forces threatening to tear it apart."

**Diagnosis:** The introduction states a topic ("will explore motivations") while the conclusion states a specific, contestable claim. These do not align — the introduction promises an exploration, the conclusion delivers an argument.

**Repair:** Replace the introduction's final sentence with a claim that introduces the paper's key concepts: "In a series of documents, the popes proposed their Crusades to restore Jerusalem to Christendom, but their words suggest other issues involving political concerns about European and Christian unity in the face of internal forces that were dividing them."

---

### Example B: Data Dump (Level 2)

A section titled "Economic Conditions" contains three pages of statistics, tables, and historical data about medieval European trade, population, and agricultural output, with no sentence stating what these data collectively prove.

**Diagnosis:** Evidence < 1/3 of section is not the problem here — evidence > 2/3 is. There is no stated reason. This is a data dump.

**Repair:** Write the section's reason statement and place it at the top: "The economic instability of late eleventh-century Europe gave feudal lords strong incentives to redirect their restless knight class outward — the Crusades offered an outlet that a stable economy would not have required."

---

### Example C: Paragraph Point Buried in Middle (Level 4)

**Before:**
> "In 1095, Pope Urban II gave a speech at the Council of Clermont in which he appealed to knights to join a Crusade. He described the suffering of Eastern Christians and the loss of Jerusalem. His words, however, reveal something more calculated: Urban framed the Crusade as a solution to the growing threat of Byzantine schism and the erosion of papal authority in the West. By 1096 the First Crusade had been launched."

**After (point moved to opening):**
> "Urban II's Council of Clermont speech reveals more political calculation than religious urgency. In 1095, Urban appealed to knights to join a Crusade, describing the suffering of Eastern Christians and the loss of Jerusalem. But his words frame the expedition as a solution to a more urgent problem: the growing threat of Byzantine schism and the erosion of papal authority in the West. By 1096 the First Crusade had launched."

---

## References

- `references/introduction-conclusion-revision.md` — Full procedure for revising the introduction and conclusion as polished final text (not just structural diagnosis)
- `references/key-term-threading.md` — Step-by-step guide to identifying key concepts and tracing them through a multi-section paper
- `references/abstract-patterns.md` — Annotated examples of all three abstract patterns across disciplines

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Craft of Research, 4th Edition by Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, William T. FitzGerald.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-research-paper-planner`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
