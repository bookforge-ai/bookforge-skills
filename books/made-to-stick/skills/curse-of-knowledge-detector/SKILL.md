---
name: curse-of-knowledge-detector
description: Diagnose a draft for the Curse of Knowledge — the expert blind spot that makes insiders write copy full of unexplained jargon, buried assumptions, strategy-level abstractions, and tacit shared context that lose non-expert audiences. Use this skill whenever reviewing a pitch, announcement, explainer, landing page, onboarding doc, slide, internal memo, or technical write-up for clarity to a non-expert. Activate when the user says things like "why isn't my message landing", "make this clearer", "my audience doesn't get it", "I can't tell if this is too technical", "diagnose this draft", "is this too jargony", "expert blind spot", "tapper listener", "translate for non-experts", "audit this for jargon", "I'm too close to this", or provides a draft plus an audience description and asks for a clarity critique. Also triggers when a user complains that smart readers stare blankly at their copy, when an explainer is full of acronyms, when an announcement leads with context instead of news, or when a strategy deck reads like a mission statement generator. This skill does NOT rewrite the draft end-to-end (that is the message-clinic skill) and does NOT score the full SUCCESs rubric (that is the stickiness-audit skill) — it produces a targeted report of Curse-of-Knowledge violations with locations, reasons, and rewrite guidance.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/curse-of-knowledge-detector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [1, 12, 13]
tags: [communication, clarity, diagnostic, expert-blind-spot, jargon-detection, copywriting, messaging, audit, writing, plain-language]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Draft to audit — a message, pitch, announcement, explainer, slide, memo, or product page as markdown or pasted text"
    - type: document
      description: "Audience description — who the draft is for, what they know, what they do not know"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set working environment: the agent operates on short-form prose drafts provided by the user."
discovery:
  goal: "Surface every passage in a draft where expert blind spots lose a non-expert audience, with concrete rewrite guidance."
  tasks:
    - "Audit a pitch or announcement for jargon, abstractions, and buried assumptions"
    - "Diagnose why an expert-written explainer is not landing with non-expert readers"
    - "Produce a flagged-passage report before running a full rewrite"
  audience:
    roles: [marketer, founder, communicator, product-manager, teacher, technical-writer]
    experience: any
  when_to_use:
    triggers:
      - "User provides a draft and an audience description and asks for a clarity review"
      - "User complains that smart readers are confused by their copy"
      - "Draft is authored by a subject-matter expert for a non-expert audience"
    prerequisites: []
    not_for:
      - "Rewriting the draft end-to-end — use a message-clinic skill instead"
      - "Scoring the full six-principle stickiness rubric — use a stickiness-audit skill"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
---

# Curse of Knowledge Detector

## When to Use

You have a draft (a pitch, announcement, explainer, slide, landing page, memo, or product write-up) authored by someone who knows the subject deeply, and you need to find the specific places where that expertise has corrupted clarity for a non-expert audience. Use this skill when the goal is **diagnosis, not rewriting** — you want a ranked list of Curse-of-Knowledge violations the user can act on (or hand to a rewriting skill).

**Preconditions to verify before starting:**
- The draft exists as text the agent can read (paste, markdown file, or document).
- The audience is named and at least roughly profiled — without a target audience, "too expert" is undefined.
- The user wants a critique, not a full rewrite. If they want a rewrite, hand off to `message-clinic-runner` after producing the report.

**The Curse of Knowledge, restated for the agent:** Once someone knows something, they cannot imagine not knowing it. Experts "tap" a tune they can hear in their own head (Elizabeth Newton's 1990 Stanford study: tappers predicted listeners would guess 50% of tunes; listeners got 2.5% — a 20x gap). The same expertise that produced the Answer backfires during the Telling Others stage. This skill catches the tapping.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **The draft:** The actual text to audit — not a summary.
  -> Check prompt for: pasted text, file path, document attachment.
  -> Ask if missing: "Paste the draft you want me to audit, or give me the file path."

- **The target audience:** Who the draft is for, and — critically — what they do NOT already know.
  -> Check prompt for: audience description, persona, reader profile.
  -> Ask if missing: "Who is this draft for? Tell me (a) their role, (b) what they already know about the subject, and (c) what you think they do not know. One sentence each is fine."

### Observable Context (gather from environment)

- **Author expertise domain:** Often visible in the prose (heavy acronyms, named frameworks, implied processes).
  -> Infer from: density of jargon, tone, structural choices.
  -> If unclear: ask one question — "Is the author a subject-matter expert in [X]?"

- **Prior attempts:** A note like "I already tried simplifying it" changes the rewrite guidance — you push for more radical reframing, not another smoothing pass.
  -> Look for: user comments about previous drafts.

### Default Assumptions

- **Assumption: the author is closer to the subject than the reader.** State this in the report. The Curse is a one-way disease — detection assumes the author is the "tapper," not the "listener."
- **Assumption: the audience cannot ask follow-up questions.** Drafts are typically read asynchronously. If the audience can ask, note the change in severity (Q&A recovers some clarity; it does not cure the Curse).

### Sufficiency Threshold

- **SUFFICIENT:** Draft text + audience description with at least role and "what they do not know."
- **PROCEED WITH DEFAULTS:** Draft + role-only audience. Flag the missing "does not know" list in the report so the user can supply it later.
- **MUST ASK:** No draft, OR audience is "general public" with no narrowing (too vague — every reader is different and the skill cannot detect insider assumptions without a contrast point).

---

## Process

### Step 0: Initialize task tracking
**ACTION:** Create a TodoWrite checklist with the steps below.
**WHY:** This is a multi-pass audit. Tracking prevents the agent from fusing passes into a single shallow scan, which is the failure mode that produces "looks fine to me" false negatives. Each pass has a different target and must run independently.

### Step 1: Establish the "listener baseline"
**ACTION:** Write a one-paragraph profile of the audience in plain terms. List explicitly: (a) vocabulary they know, (b) vocabulary they do NOT know, (c) processes/workflows they understand, (d) processes they do NOT understand, (e) prior context they have, (f) prior context they lack. Use the audience description supplied by the user and your own reasoning.
**WHY:** You cannot detect Curse-of-Knowledge violations without a contrast point. The tapper/listener experiment works because the listener's state of mind is knowable (they literally cannot hear the tune). For a draft, you simulate the listener by writing down, up front, what the listener can and cannot hear. Every subsequent flag is scored against THIS baseline, not a generic "average reader."

**Save:** The listener baseline as the first section of the output report.

### Step 2: Pass A — Unexplained jargon, acronyms, and named frameworks
**ACTION:** Scan the draft and flag every term that appears in the draft but not in the listener baseline's "vocabulary they know" list. Include: acronyms (including common-in-industry ones the audience may not share), proper nouns referring to internal tools/products/projects, named frameworks (e.g., "SUCCESs framework", "Sinatra Test"), technical verbs used as nouns ("a retro", "a standup"), and metaphors borrowed from a sub-field the audience does not live in.
**WHY:** Jargon is the most visible Curse-of-Knowledge symptom. It is also the easiest to miss in self-review because the author reads every term as transparent. A mechanical pass catches what an "impression pass" glosses over.

**For each hit record:** location (quote or line reference), the term, why a listener would not parse it, and a rewrite option (define on first use, swap for a common-language equivalent, or remove if not load-bearing).

### Step 3: Pass B — Abstraction ladder (strategy-level talk)
**ACTION:** Re-read each paragraph and ask: "Is the sentence operating at the level of STRATEGY (goals, visions, synergies, principles) or the level of ACTION (observable behavior, physical object, named person, concrete step)?" Flag sentences that live at the strategy level without ever dropping to the action level. Apply the Boeing 727 test: "If this were replaced by a concrete constraint ('seat 131 passengers, land on Runway 4-22, one mile long'), would the sentence lose meaning or gain it?" If concrete constraints GAIN meaning, the abstract original is a Curse-of-Knowledge hit.
**WHY:** Experts prefer the strategy level because they have internalized the concrete layer and find it tedious. Non-experts can only anchor to concrete objects, people, and behaviors ("bishops moving diagonally," not "chess strategy"). Abstract-only copy is readable but un-actionable — the reader finishes the paragraph and cannot say what anyone would DO differently tomorrow. This is exactly what the JFK "man on the moon" example contrasts with the modern-CEO "maximize shareholder value" failure mode.

**For each hit record:** location, the abstract phrase, a specific concrete translation (actor + verb + observable object), and whether the fix is "add a concrete example" or "replace the abstraction entirely."

### Step 4: Pass C — Buried assumptions and tacit shared context
**ACTION:** For each claim in the draft, ask: "What does the reader have to ALREADY believe or know for this sentence to land?" Write the implicit premise. Then check it against the listener baseline. If the premise is not on the listener's "known" list, the sentence is a Curse-of-Knowledge hit even if every word is plain English.
**WHY:** This is the subtlest axis and the one where "it sounds clear" audits miss the most. A sentence like "we're deprecating the legacy pipeline" has no jargon to the author — but assumes the reader knows (a) there is a pipeline, (b) there is a legacy version and a new version, (c) "deprecate" is a soft word for "turning off," and (d) the reader is a stakeholder in the decision. Each of those assumptions is a tapper tapping a tune. Surfacing the buried premises IS the diagnosis.

**For each hit record:** location, the explicit premise the reader must hold, whether the listener baseline shows they hold it, and a rewrite option (state the premise, link to a primer, or restructure).

### Step 5: Pass D — Buried lead and common-sense sedation
**ACTION:** Read the first sentence of the draft. Ask: "Is this the single most important thing the reader must walk away with?" If not, flag "buried lead" (the Nora Ephron journalism-teacher test: the lead is `there will be no school Thursday`, not `principal announces faculty retreat`). Then scan the draft for sentences every member of the audience would nod and agree with before reading — "customer service is important," "communication is key." Flag these as "common sense sedation." Both failure modes are Curse-of-Knowledge symptoms: the author is leading with context they already know, or stating positions so internalized they feel like news to the author but are invisible to the reader.
**WHY:** The Heaths frame "burying the lead" as the first villain named after the Curse in the Epilogue — "we're tempted to share it all" because we know it all. Common-sense statements are a second-order Curse effect: the author forgot what it was like not to already agree. Both pass the plain-English test but fail the stickiness test.

**For each hit record:** location, the failure mode (buried-lead OR common-sense), and one concrete replacement sentence.

### Step 6: Synthesize the report
**ACTION:** Combine the four pass outputs into a single prioritized report with this structure:
1. **Listener baseline** (from Step 1).
2. **Tapper/listener gap estimate** — your one-sentence summary of the delta between what the draft assumes and what the listener baseline actually holds. Be specific. ("Author assumes reader knows what a feature flag is, what rollout means, and why staged rollouts reduce risk. Listener baseline shows none of these are held.")
3. **Top 3 rewrite targets** — the three highest-impact hits across all four passes, ranked by (severity × how much of the draft they poison). Each gets: quote, pass it came from, why it hurts, specific rewrite.
4. **Full flagged-passage table** — every hit from Passes A–D with columns: location, passage, pass (A/B/C/D), why, rewrite guidance.
5. **Listener simulation test** — three to five questions the listener baseline-reader would plausibly ask the author after reading the draft. These are the gaps the rewrite must close.
6. **Handoff note** — one sentence saying whether the draft needs jargon substitution (lightweight), structural rework (lead repositioning + abstraction concretization), or a full rewrite from the core message up.

**WHY:** The user asked for diagnosis, not a pile of annotations. The top-3 ranking and the handoff note tell them what to DO with the report. Without prioritization, a long flagged-passage table produces analysis paralysis — the exact anti-pattern Made to Stick warns against in Chapter 1.

**Save:** The full report to `curse-of-knowledge-report.md` in the user's working directory.

### Step 7: Structural self-check
**ACTION:** Before returning, verify: (a) every flagged passage has a location, a reason, and a rewrite option — not just "unclear"; (b) the listener baseline is specific enough that someone else could re-run the audit and reach similar conclusions; (c) the top-3 are actually ranked, not just listed; (d) the handoff note is one decisive sentence, not a hedge.
**WHY:** The audit's value is in its specificity. A report that says "some parts could be clearer" is indistinguishable from generic AI advice — it produces no delta over a baseline agent. Specificity (location + reason + rewrite) is what makes the skill book-derived rather than generic.

---

## Inputs

- `draft` — the text to audit (markdown, pasted text, or file path).
- `audience` — a description of the target reader, minimum role + "what they do not know."
- Optional: `mode_note` — "lightweight pass" or "full four-pass audit" (default: full).

## Outputs

A single file, `curse-of-knowledge-report.md`, with this shape:

```markdown
# Curse of Knowledge Report — {draft name}

## Listener Baseline
{audience role, known vocabulary, unknown vocabulary, known processes, unknown processes, held context, missing context}

## Tapper/Listener Gap Estimate
{one-sentence delta}

## Top 3 Rewrite Targets
1. **{quote}** — Pass {X}. Why: {reason}. Rewrite: {concrete fix}.
2. ...
3. ...

## Flagged Passages (Pass A: Jargon)
| Location | Passage | Why a listener cannot parse it | Rewrite |

## Flagged Passages (Pass B: Abstraction)
| Location | Passage | Abstract level | Concrete translation |

## Flagged Passages (Pass C: Buried Assumptions)
| Location | Passage | Implicit premise | Present in listener baseline? | Rewrite |

## Flagged Passages (Pass D: Buried Lead / Common Sense)
| Location | Passage | Failure mode | Replacement sentence |

## Listener Simulation Questions
- Q1: {a question the listener baseline-reader would ask after reading}
- ...

## Handoff Note
{one decisive sentence: jargon substitution | structural rework | full rewrite}
```

---

## Key Principles

- **You cannot cure the Curse, only route around it.** The Heaths are explicit: "There are only two ways to beat the Curse of Knowledge reliably. The first is not to learn anything. The second is to take your ideas and transform them." Detection means finding what must be transformed — not guilting the author into "trying harder to be clear."

- **The listener baseline is the only ground truth.** Every flag is relative to a specific listener profile. A term that is "jargon" to a recruit is "common language" to an engineer on the same team. If you skip the baseline and audit against a generic reader, you produce generic feedback — which is exactly the delta gap the skill is supposed to close.

- **Multi-pass beats single-pass.** Each pass targets a different axis (lexical, structural, tacit, prioritization). Fused into one pass, the agent defaults to the most visible axis (jargon) and misses the subtler ones (buried assumptions, common-sense sedation). The book's entire methodology is structured this way — six principles, each addressed on its own — because human authors cannot hold all axes at once.

- **Specificity is the value.** "This paragraph is too abstract" is free advice. "Replace `maximize shareholder value` with `grow revenue by 20% this year by winning back 10 lapsed accounts` (actor + verb + measurable object)" is the skill. Every flag must include a concrete rewrite option or it is noise.

- **Prioritize ruthlessly; report faithfully.** The top-3 is the action surface. The full table is the audit trail. Without the top-3, the user drowns in findings (decision paralysis — a named Made to Stick failure mode). Without the full table, the user cannot trust the top-3. Both are required.

- **The author is not the villain.** Curse-of-Knowledge is a natural psychological tendency, not a skill deficit. Frame the report so the author can see the failure mode as structural — "here is where your expertise created a gap" — not as criticism.

---

## Examples

**Scenario: Product announcement for a developer tool, audience is non-technical buyers**

Trigger: User pastes a 400-word announcement that opens "We're shipping v2 of our feature-flag rollout engine with staged canaries and blast-radius controls." Audience: "VP of Engineering buyers at mid-market SaaS companies — they manage engineers but haven't written code in five years."

Process: (1) Listener baseline notes "feature flag" = probably known, "canary", "blast radius" = probably not known, "staged rollout" = known in principle, "rollout engine" = ambiguous. (2) Pass A flags `canaries`, `blast-radius`, `rollout engine`. (3) Pass B flags the abstract noun "controls" with no concrete behavior. (4) Pass C flags the buried assumption that the reader already wanted v2. (5) Pass D flags the buried lead — the actual news ("our tool now prevents the top three rollout-caused outages buyers told us about") is in paragraph 4.

Output: `curse-of-knowledge-report.md` with Top 3 = (1) move the paragraph-4 news to sentence 1, (2) define `canary` on first use as "a small slice of users who see the change first", (3) replace "blast-radius controls" with "automatic rollback if error rate crosses a threshold you set." Handoff note: "Structural rework — lead repositioning plus three jargon substitutions."

**Scenario: Nonprofit fundraising letter, audience is first-time donors**

Trigger: User pastes a 600-word letter from a global-health nonprofit that leads with program architecture, regional coverage statistics, and the M&E framework. Audience: "First-time individual donors, $25–$100 range, no prior engagement with global health."

Process: (1) Listener baseline: knows what a nonprofit is, does not know `M&E`, `catchment area`, `DALY`, does not know the named regions, does not know the organization's history. (2) Pass A flags four acronyms. (3) Pass B flags "program architecture" and "regional coverage" as strategy-level. (4) Pass C flags the assumption that the reader already cares about sub-Saharan maternal health statistics. (5) Pass D flags the buried lead (there is no Rokia-style individual named person) and flags "we are committed to lasting impact" as common-sense sedation.

Output: Top 3 = (1) open with a named beneficiary (the Mother Teresa / Rokia effect — identifiable victim beats statistics), (2) replace `M&E`, `DALY`, and `catchment area` with plain equivalents or cut them, (3) cut the "committed to lasting impact" sentence entirely. Handoff note: "Full rewrite from the core message — the current draft is architected around the organization's self-description, not the donor's decision."

**Scenario: Internal all-hands memo about a strategy pivot, audience is all employees**

Trigger: CEO pastes a memo that mentions "shareholder value," "synergies across business units," and "our North Star metric." Audience: "All 400 employees — roles range from engineers to facilities staff. Most have not attended exec strategy meetings."

Process: (1) Listener baseline: broadly varied — assume the lowest-context reader does not know `North Star metric`, does not know which business units exist, does not know what "shareholder value" means for their day-to-day. (2) Pass A flags `North Star`, `synergies`. (3) Pass B flags the entire memo as strategy-level with no concrete behavior change. (4) Pass C flags the assumption that readers know why the pivot is happening. (5) Pass D flags severe common-sense sedation across three paragraphs that any reader would already agree with.

Output: Top 3 = (1) add a concrete "what changes for you on Monday" paragraph per role category, (2) replace `North Star` with the actual metric and its target number, (3) cut the two paragraphs of values-language that add no news. Handoff note: "Full rewrite — this is the Made to Stick-canonical 'maximize shareholder value' failure at scale."

---

## References

- For the full jargon-substitution decision tree and worked word-swap tables, see [jargon-detection-playbook.md](references/jargon-detection-playbook.md)
- For the abstraction-ladder worked examples (Boeing 727, JFK moon mission, Commander's Intent, maximize shareholder value), see [abstraction-ladder-examples.md](references/abstraction-ladder-examples.md)
- For the full listener-baseline template and audience-profile interview script, see [listener-baseline-template.md](references/listener-baseline-template.md)

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Made to Stick: Why Some Ideas Survive and Others Die by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone (Level 0 foundation). Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
