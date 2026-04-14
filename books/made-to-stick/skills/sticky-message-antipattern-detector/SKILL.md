---
name: sticky-message-antipattern-detector
description: Scan a draft, pitch, or copy for the named failure modes that kill stickiness — buried leads, decision paralysis, common-sense sedation, semantic stretch, stats-without-story, abstract strategy talk, scope creep, and the direct-message fallacy. Use this skill whenever a user asks to audit a draft, diagnose why a message is not landing, review a pitch, find the problems in copy, spot issues in an announcement, critique a marketing page, debug a speech, or check an internal memo — even when they do not explicitly use the word "stickiness". Activate on phrases like "audit this draft", "what is wrong with this message", "why is not this landing", "find the problems in this copy", "review my pitch", "spot the issues", "this is not resonating", "my announcement fell flat", "tell me what is broken in this email", "diagnose this speech", "why does not anyone remember what I said", "critique my copy", or any situation where the user supplies a short-form prose artifact and asks for a rigorous problem diagnosis rather than a rewrite. The skill produces a flagged-passage report with each instance located, severity-scored, and paired with a fix strategy — it does NOT rewrite the draft end-to-end and does NOT cover the Curse of Knowledge (that is a separate detector) or score the full six-principle SUCCESs rubric (that is a separate audit skill).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/sticky-message-antipattern-detector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [1, 2, 3, 4, 5, 6, 12]
tags: [communication, diagnostic, anti-pattern, messaging, copywriting, editing, audit, writing, marketing, persuasion]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Draft to audit — a message, pitch, announcement, ad, explainer, speech, slide, memo, or product page as markdown or pasted text"
    - type: document
      description: "Audience profile — who the draft is for, what they care about, what they already believe"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set working environment: the agent operates on short-form prose drafts provided by the user."
discovery:
  goal: "Surface every instance of eight named stickiness failure modes in a draft, with location, severity, and a concrete fix strategy for each."
  tasks:
    - "Audit a pitch, ad, or announcement for named stickiness anti-patterns"
    - "Diagnose why a message is not resonating with an audience"
    - "Produce a prioritized defect list before running a full rewrite"
  audience:
    roles: [marketer, founder, communicator, product-marketer, public-speaker, copywriter, teacher, fundraiser]
    experience: any
  when_to_use:
    triggers:
      - "User pastes a draft and asks what is wrong with it"
      - "User says a message is not landing and wants a diagnosis"
      - "User wants a rigorous defect report before rewriting"
    prerequisites: []
    not_for:
      - "Rewriting the draft end-to-end — use a message-clinic skill"
      - "Scoring the full SUCCESs six-principle rubric — use a stickiness-audit skill"
      - "Diagnosing expert blind spots specifically — use curse-of-knowledge-detector"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
---

# Sticky Message Anti-Pattern Detector

## When to Use

You have a draft — a pitch, ad, announcement, ad copy, speech, memo, slide, or product page — and the user has asked what is wrong with it, why it is not landing, or wants a rigorous defect report before rewriting. Use this skill when the goal is **named-defect diagnosis**, not rewriting. The output is a flagged-passage report that lists every instance of eight specific failure modes, each located, severity-scored, and paired with a fix strategy.

**Preconditions to verify before starting:**
- The draft exists as text the agent can read (pasted, markdown, or file path).
- The target audience is named with at least role + what they already care about. Without audience context, "common sense" and "semantic stretch" cannot be scored.
- The user wants diagnosis, not a rewrite. If they want a rewrite, produce the report first, then hand off.

**The eight anti-patterns this skill detects (each with a book citation):**

1. **Burying the Lead** — the most important fact is not in sentence one. (Ch 1 — Nora Ephron's journalism-teacher story; Carville's "It's the economy, stupid" was an antidote to Clinton burying his own lead.)
2. **Decision Paralysis** — multiple co-equal "top priorities" with no hierarchy. (Ch 1, Epilogue — Iyengar jam study 24→6, Redelmeier-Shafir doctor study, Jeff Hawkins's Palm team.)
3. **Common-Sense Trap** — the message says what every reader already believes. (Ch 2, Ch 6, Epilogue — "customer service is important" fails; Nordstrom "gift-wrap from Macy's" sticks.)
4. **Semantic Stretch** — words like *unique*, *strategy*, *awesome*, *great*, *amazing* are used so broadly they have lost meaning. (Ch 5 — Heath & Gould 2005 Stanford working paper; "unique" is no longer unique, "relativity" now means "it depends".)
5. **Stats Without Story** — claims are defended with numbers alone, not human-scale anchors. (Ch 4, Ch 5, Epilogue — 63% of students remember stories vs 5% remember individual statistics; Rokia/Save the Children identifiable-victim study; nuclear warheads demonstrated as BBs in a bucket.)
6. **Abstract Strategy Talk** — sentences live at the strategy level (synergies, vision, shareholder value) with no concrete observable behavior. (Intro, Ch 3 — Beth Bechky silicon chip engineers vs manufacturers; "maximize shareholder value" vs JFK moon mission.)
7. **Scope Creep** — the message tries to make three or more co-equal top points and therefore makes none. (Notes p.175 — "If you say three things, you don't say anything"; related to but distinct from decision paralysis.)
8. **Direct-Message Fallacy** — raw abstract directives delivered where a springboard story would transfer the idea better. (Ch 6 — Stephen Denning at the World Bank: "hit the listeners between the eyes, they fight back"; Velcro theory of memory.)

For detailed detection criteria, consequences, and fix recipes for each pattern, see [references/antipattern-catalog.md](references/antipattern-catalog.md).

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **The draft:** The actual text to audit — not a summary.
  -> Check prompt for: pasted text, file path, document attachment.
  -> Ask if missing: "Paste the draft you want audited, or give me the file path."

- **The audience profile:** Who the draft is for, and what they already believe.
  -> Check prompt for: audience description, target persona, reader role.
  -> Ask if missing: "Who is this draft for? One sentence on (a) their role, (b) what they already care about, (c) what they already believe is obvious about this topic."

### Observable Context (gather from environment)

- **Channel and constraint:** Is this an ad (character limit), a speech (time limit), an email (subject-line constraint), a slide (visual), or long-form prose? Affects severity scoring.
  -> Infer from: length, formatting, user framing.
  -> If unclear: ask one question — "What format and where will this run?"

- **Tone constraints:** Brand or legal tone limits change which fixes are legal.
  -> Look for: user comments like "it has to stay on-brand" or "legal signed off on this phrasing".

### Default Assumptions

- **Assumption: audience cannot ask follow-up questions.** Drafts are read asynchronously. If the user corrects this, raise severity of buried-lead and scope-creep flags (readers cannot re-ask for the core).
- **Assumption: the author is an insider.** Make the author a secondary stickiness risk: the common-sense trap and abstract-strategy talk are more likely when the author is deep in the domain.

### Sufficiency Threshold

- **SUFFICIENT:** Draft text + audience with role and "what they already believe" + known channel.
- **PROCEED WITH DEFAULTS:** Draft + role-only audience. Flag the missing beliefs list in the report so the user can confirm.
- **MUST ASK:** No draft, OR audience is "general public" with no narrowing (too vague to score common-sense or semantic-stretch hits).

---

## Process

### Step 0: Initialize task tracking
**ACTION:** Create a TodoWrite checklist with one item per detection pass (Steps 2–9) plus Step 1 and Step 10.
**WHY:** Each anti-pattern targets a different axis (structural, lexical, narrative, prioritization). Fusing passes into a single scan defaults to the most visible axis (usually jargon-ish word problems) and silently drops the subtler ones — buried assumptions about common sense, semantic stretch in background phrases, scope creep across sections. The checklist enforces that every axis gets its own independent pass.

### Step 1: Establish the audience belief baseline
**ACTION:** Write a short profile of the audience: (a) role, (b) what they already believe is true / obvious about this topic, (c) what would genuinely surprise them, (d) what they actually care about (outcomes, pains, wins), (e) what counts as credible to them (data, peer stories, authority, personal anecdote). Use the user's supplied profile plus your reasoning.
**WHY:** Three of the eight anti-patterns — common-sense trap, semantic stretch, stats-without-story — can only be scored relative to a specific audience. "Customer service is important" is common sense to customer-service managers and news to a junior engineer. "Unique" is semantic stretch to a marketing buyer and fresh to a child. Skip this and the report becomes generic clarity advice.

**Save:** The audience belief baseline as Section 1 of the output report.

### Step 2: Pass AP-02 — Burying the lead
**ACTION:** Read the draft's first sentence (and for long pieces, the first paragraph). Ask: "Is this the single most important thing the reader must walk away with?" Then scan the whole draft for the sentence that SHOULD be the lead — the single fact, offer, news, or claim whose loss would gut the piece. If that sentence is not in position 1, flag `AP-02: Buried Lead`.
**WHY:** Journalism's inverted-pyramid rule exists because readers stop reading. The Heaths' Epilogue names this as the first villain for speakers: "we're tempted to share it all." If the actual news is buried in paragraph four, the audience never reaches it. Detection is mechanical — compare sentence 1 to the sentence you would keep if forced to delete 90% of the piece.

**For each hit record:** the actual first sentence (quote), the sentence that should be the lead (quote + location), severity (High if the lead is in paragraph 3+ or absent; Medium if in paragraph 2), and a fix strategy — usually "promote sentence X to position 1" with any needed connective tweaks.

### Step 3: Pass AP-03 — Decision paralysis
**ACTION:** Count the number of sentences that claim to be "the most important", "our top priority", "the key thing", or equivalent. Also count the number of top-level bullet lists with 5+ items framed as co-equal. Flag `AP-03: Decision Paralysis` if there is more than one "top" or if a co-equal list of five or more priorities is presented without a designated single core.
**WHY:** Iyengar's jam study (24 flavors → 3% bought; 6 flavors → 30% bought) and the Redelmeier-Shafir doctor study (doctors delay treatment when forced to choose among multiple good options) show that audiences freeze when confronted with multiple equally-weighted "bests". The Heaths explicitly prescribe "relentless prioritization: 'It's the economy, stupid.'" Detection is a simple count.

**For each hit record:** the conflicting "top" claims (quotes), severity (High if 3+ top claims; Medium if 2), and a fix strategy naming a single recommended core (or asking the user to pick one).

### Step 4: Pass AP-04 — Common-sense trap
**ACTION:** For each standalone claim sentence, ask: "Would a member of the audience, based on the belief baseline, nod in agreement BEFORE reading?" If yes — flag `AP-04: Common Sense`. Especially target sentences like "customer service is important", "communication is key", "quality matters", "our people are our greatest asset", "we are committed to excellence", "safety first", and any variant. Also flag any "advice" section whose advice the audience would already give.
**WHY:** Chapter 2 names this explicitly: "common sense is the enemy of sticky messages." The reader's guessing machine is not broken, so nothing is encoded to memory. The test in Epilogue: Nordstrom's "gift-wraps packages from Macy's" sticks because it breaks the schema of what a store does. Detection: any sentence the audience would have written themselves fails.

**For each hit record:** the flagged sentence, why it is common sense relative to the audience baseline, severity (High if it is the lead, Medium elsewhere), and a fix strategy — either the counter-intuitive reframe (surface the uncommon claim hiding in the material) or deletion.

### Step 5: Pass AP-05 — Semantic stretch
**ACTION:** Scan for stretched words. The book-named list (Heath & Gould 2005 working paper, Stanford): *unique*, *strategy*, *strategic*, *awesome*, *amazing*, *fantastic*, *great*, *excellent*, *innovative*, *leverage*, *synergy*, *world-class*, *best-in-class*, *relativity* as "it depends", *revolutionary*, *game-changing*. For each occurrence, check whether the word is carrying its original distinctive meaning in context (a genuine one-of-a-kind claim for "unique"; a real strategic choice for "strategy") or whether it has been diluted into a generic positive vibe.
**WHY:** Heath and Gould documented that extreme synonyms for "good" (fantastic, amazing) are increasing in use faster than less-extreme synonyms — i.e., the vocabulary is inflating. Overused words do not just fail to impress; they flatten any sentence they touch because the reader's processing discounts them to zero. Detection is a fixed-list scan with a context check.

**For each hit record:** the stretched word (with surrounding phrase), whether the original meaning is intact or diluted, severity (High if 3+ stretched words in one paragraph or in the lead; Medium if 1–2), and a fix strategy — narrow it to a concrete claim ("our onboarding is 30 minutes, half the category average" beats "we have an awesome onboarding experience") or revive the word's original force via a vivid anchor.

### Step 6: Pass AP-06 — Stats without story
**ACTION:** Count every statistic, percentage, or quantitative claim in the draft. For each, check whether it is paired with a human-scale anchor, a named person, or a concrete analogy ("5,000 nuclear warheads" → "one BB per thousand people in a bucket"; "400,000 children in need" → "one child, Rokia"). Compute the ratio of bare stats to anchored stats. Flag `AP-06: Stats Without Story` if any high-stakes stat is bare, or if the ratio of bare-to-anchored is worse than 1:1.
**WHY:** The Heaths cite a student-speech recall study directly: 63% of listeners remember stories; 5% remember any individual statistic. The Rokia/Save the Children study showed that a single identified child raised more than statistics about millions. Statistics do not engage the machinery that produces caring. Detection is mechanical — count and check for pairing.

**For each hit record:** the bare statistic (quote), why a human-scale anchor is needed, severity (High if the stat is load-bearing for the argument, Medium if decorative), and a fix strategy — either wrap the stat in a physical analogy (Human Scale principle), pair it with a single named person, or cut it if the story does the job alone.

### Step 7: Pass AP-07 — Abstract strategy talk
**ACTION:** Re-read each sentence and classify it as ACTION-level (names a concrete actor doing a concrete verb on a concrete object) or STRATEGY-level (goals, synergies, visions, competencies, alignment). Flag every sentence that sits at strategy level without an adjacent action-level translation. Especially target: "maximize shareholder value", "drive outcomes", "align around", "leverage synergies", "operational excellence", "execute our vision", "deliver value", "transform the business", "our North Star is X" (without naming the number and the specific target). Apply the "soccer team test": if you were the coach with this as your message, would your players know what to DO on Monday?
**WHY:** Chapter 3 uses the Beth Bechky silicon chip study: designers and manufacturers could not coordinate because they worked at different levels of abstraction. The Heaths contrast JFK's "man on the moon" (concrete, sensory, time-bound) with a modern CEO's "maximize shareholder value" (unbounded, opaque, unactionable). Abstract-only prose is grammatical but un-actionable. Detection: look for sentences without an actor-verb-object.

**For each hit record:** the abstract sentence, whether there is ANY concrete translation in the draft, severity (High if the whole draft lives at strategy level, Medium if mixed), and a fix strategy — either add an actor-verb-object concretization ("grow revenue 20% this year by winning back 10 lapsed accounts") or replace the sentence entirely with the behavior it implies.

### Step 8: Pass AP-08 — Scope creep
**ACTION:** Count the number of distinct top-level points, themes, or "key takeaways" in the draft. If there are 3 or more with no explicit hierarchy, flag `AP-08: Scope Creep`. This is related to but distinct from decision paralysis: paralysis is about competing priorities presented as co-equal, scope creep is about a piece trying to communicate too many separate ideas at once.
**WHY:** The Heaths cite the "If you say three things, you don't say anything" principle from a named comms expert (Notes p. 175). Mechanism: multiple priorities cancel each other out and the audience retains none. Common trigger: high school research papers where students feel obligated to include every unearthed fact. Detection is a section / theme count.

**For each hit record:** the enumeration of top points (quotes or summaries), severity (High if 4+ themes or the draft is long-form; Medium if exactly 3), and a fix strategy — name THE one core message (Commander's Intent) and demote the rest to supporting evidence or cut them.

### Step 9: Pass AP-09 — Direct-message fallacy
**ACTION:** Scan for passages that deliver abstract directives ("we need to be more X", "you should Y", "the key is to Z", "it is important to A") without any narrative scaffolding — no springboard story, no worked example, no before/after. Flag `AP-09: Direct Message Fallacy` where the piece is making an argument or prescribing a change and relies entirely on assertion rather than story.
**WHY:** Chapter 6 tells the Stephen Denning World Bank story: Denning initially believed in being direct and thought stories were "too ambiguous, too peripheral, too anecdotal". He found that when you "hit the listeners between the eyes, they fight back" — abstract directives do not simulate the outcome, so they cannot engage the listener's reasoning machinery. The Velcro theory: more hooks = more stickiness. Direct assertion has few hooks.

**For each hit record:** the directive passage, the change it is trying to cause, severity (High if this is a change-management or adoption message; Low-Medium if a status update), and a fix strategy — suggest a springboard-story frame ("tell us one concrete story where this worked, then name the principle") or identify an analogy / comparison the user could draft.

### Step 10: Synthesize the report
**ACTION:** Combine the nine passes into a single prioritized report. Structure:
1. **Audience belief baseline** (from Step 1).
2. **Scorecard** — a table with each anti-pattern, hit count, and max severity.
3. **Top 3 fix targets** — the three highest-impact hits across all passes, ranked by (severity × how much of the draft they poison). Each gets: quote, anti-pattern ID, why it hurts, specific fix.
4. **Full flagged-passage table** — every hit with columns: anti-pattern ID, location, passage, severity, fix strategy.
5. **Handoff note** — one decisive sentence: "cosmetic fixes" (stretch + stats only) vs "structural rework" (lead + scope + paralysis) vs "rewrite from core message" (common-sense + strategy-talk dominate).

**WHY:** The report's value is in ranked, actionable specificity. An unranked dump causes decision paralysis — the exact failure mode named in AP-03. The top-3 is the action surface; the full table is the audit trail; the handoff note tells the user what to DO with the report.

**Save:** The full report to `antipattern-report.md` in the user's working directory.

### Step 11: Structural self-check
**ACTION:** Before returning, verify: (a) every flagged passage has a location, a severity, and a fix — not just "this is bad"; (b) the top-3 are ranked, not listed; (c) the scorecard counts match the flagged-passage table; (d) the handoff note is one decisive sentence, not a hedge; (e) AP-01 (Curse of Knowledge) is NOT included — that is a separate skill.
**WHY:** Specificity is what makes this skill outperform generic critique. A report that says "the tone could be punchier" is indistinguishable from baseline advice. Location + severity + fix strategy is what gives the user something to act on. Missing the hedge-note check is the most common late-stage failure.

---

## Inputs

- `draft` — the text to audit (markdown, pasted text, or file path).
- `audience_profile` — role, what they already believe, what they care about, what counts as credible to them.
- Optional: `channel` — ad / email / slide / speech / memo / long-form (affects severity weighting).

## Outputs

A single file, `antipattern-report.md`, with this shape:

```markdown
# Sticky Message Anti-Pattern Report — {draft name}

## Audience Belief Baseline
{role, pre-read beliefs, what would surprise, what they care about, what is credible to them}

## Scorecard
| Anti-Pattern | Hits | Max Severity |
|---|---|---|
| AP-02 Buried Lead | ... | ... |
| AP-03 Decision Paralysis | ... | ... |
| AP-04 Common Sense | ... | ... |
| AP-05 Semantic Stretch | ... | ... |
| AP-06 Stats Without Story | ... | ... |
| AP-07 Abstract Strategy | ... | ... |
| AP-08 Scope Creep | ... | ... |
| AP-09 Direct Message | ... | ... |

## Top 3 Fix Targets
1. **{quote}** — {AP-ID}. Why: {reason}. Fix: {specific}.
2. ...
3. ...

## Flagged Passages
| AP-ID | Location | Passage | Severity | Fix |

## Handoff Note
{one decisive sentence: cosmetic | structural | rewrite-from-core}
```

---

## Key Principles

- **Named defects beat vibes.** "This feels vague" is a stylistic reaction. "AP-07 Abstract Strategy Talk — sentence lives at the strategy level with no actor-verb-object; needs concretization" is a diagnosis. Every flag MUST carry an anti-pattern ID and a fix strategy, or it is noise.

- **Scoring requires a baseline.** Three of the eight patterns (common sense, semantic stretch, stats without story) cannot be scored without a specific audience. The belief baseline (Step 1) is not decoration — it is the denominator for the scoring function. Skip it and you produce generic critique.

- **Mechanical passes beat impression passes.** The book's methodology is six independent principles, not one fused heuristic, precisely because humans and agents cannot hold all axes at once. This skill enforces the same structure: one pass per pattern, independent, in order. Fusing passes silently drops the subtler ones.

- **Rank ruthlessly, report faithfully.** The top-3 is the action surface; the full table is the audit trail. Both are required — top-3 alone lacks justification, full-table alone causes the exact decision paralysis (AP-03) this skill detects. The report structure is load-bearing.

- **The skill diagnoses; it does not rewrite.** The book distinguishes the Answer stage from the Telling Others stage. This skill operates at the Telling Others diagnostic layer — it flags and suggests fixes but does not produce the new prose. Crossing that boundary erodes the per-passage specificity that makes the audit valuable and hands off cleanly to a rewriting skill.

- **Severity is a function of position and stake.** A common-sense sentence in the lead is fatal; the same sentence in a parenthetical is a minor hit. A buried statistic in a decorative list is low-stakes; the same bare statistic in the close of a fundraising letter is a flameout. Always weight by where the flaw sits in the reader's attention path.

---

## Examples

**Scenario: SaaS product announcement email**

Trigger: User pastes a 400-word product email that opens "At Acme, we believe that communication is the key to great teams. That is why we are incredibly excited to announce our amazing new unified platform, which represents our strategic commitment to driving better outcomes. Our customers — over 5,000 of them — have been asking for integrations, a better inbox, and smarter notifications. We think you will love it." Audience: "Product managers at mid-market SaaS companies who already use our product."

Process: (1) Audience baseline notes PMs already believe "communication matters" and already use the product. (2) AP-02: buried lead — the actual news (unified platform) is in sentence 2 but buried under belief framing; the real "what changed" is unspecified. (3) AP-03: three co-equal "asks" (integrations, inbox, notifications) with no hierarchy. (4) AP-04: "communication is the key to great teams" is pure common-sense sedation for this audience. (5) AP-05: "incredibly excited", "amazing", "strategic commitment", "better outcomes" — four stretched words in two sentences. (6) AP-06: "over 5,000 customers" is a bare stat with no human scale. (7) AP-07: "driving better outcomes", "strategic commitment" are strategy-level with no behavioral anchor. (8) AP-08: three themes crammed into one email.

Output: `antipattern-report.md` with scorecard showing 8 hits. Top 3: (1) cut the opening "we believe" sentence and lead with the single biggest user-visible change; (2) pick ONE of the three features as the core of this email and demote the other two to a "also shipping" line; (3) replace "amazing", "strategic commitment", "better outcomes" with a concrete behavioral claim. Handoff note: "Structural rework — lead repositioning plus scope reduction to one feature."

**Scenario: Nonprofit fundraising letter**

Trigger: User pastes a 600-word letter that leads with organizational history, cites "We reached 1.2 million children across 14 countries", and closes with "We are committed to lasting impact." Audience: "First-time donors, $25–$100 range."

Process: (1) Baseline notes first-time donors do not know the org, care about individual impact, are moved by specific stories. (2) AP-02: buried lead — the "why you should give" is absent from sentence 1. (3) AP-06: 1.2M children / 14 countries is a bare stat with no Rokia-style anchor; high severity because this is the emotional close. (4) AP-04: "committed to lasting impact" is common-sense sedation. (5) AP-07: "lasting impact", "sustainable outcomes" are strategy-talk. (6) AP-09: entire letter is direct assertion with no springboard story.

Output: Scorecard shows 5 hits. Top 3: (1) open with a single named beneficiary (Rokia effect); (2) replace the 1.2M stat with a one-child story or an analogy that scales to a donor's $50 gift; (3) cut the commitment-to-impact sentence. Handoff note: "Rewrite from core message — this letter is architected around the org, not the donor's decision."

**Scenario: Internal strategy memo**

Trigger: CEO pastes a 500-word memo: "Team, our North Star is net revenue retention. We will drive synergies across BUs, maximize shareholder value, and align around operational excellence. Quality is non-negotiable, our people are our greatest asset, and I am confident we will achieve excellence together." Audience: "All 400 employees, roles from engineering to facilities."

Process: (1) Baseline: most employees do not know NRR, BUs, or what "shareholder value" means for their week. (2) AP-04: "quality is non-negotiable", "our people are our greatest asset", "I am confident" — three consecutive common-sense sentences. (3) AP-05: "synergies", "operational excellence", "excellence together" — three stretched words. (4) AP-07: entire memo is at strategy level with zero action-level sentences; invokes the Boeing 727 / JFK test and fails. (5) AP-08: NRR, synergies, shareholder value, quality, people, excellence — six co-equal themes.

Output: Scorecard shows all-strategy, all-common-sense, heavy stretch. Top 3: (1) add a "what changes for you on Monday" paragraph per role category; (2) cut the entire "quality / people / excellence" paragraph (common-sense sedation); (3) replace "North Star is NRR" with the actual number and the behavior change needed to hit it. Handoff note: "Rewrite from core message — this is the canonical 'maximize shareholder value' failure at scale."

---

## References

- For the full eight-entry catalog with detection criteria, book citations, consequences, and fix recipes, see [references/antipattern-catalog.md](references/antipattern-catalog.md)

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Made to Stick: Why Some Ideas Survive and Others Die by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone (Level 0 foundation). Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
