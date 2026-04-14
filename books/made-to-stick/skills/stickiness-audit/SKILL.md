---
name: stickiness-audit
description: Run the full SUCCESs stickiness audit on a draft message, pitch, announcement, slide, speech, landing page, or internal memo — the book's capstone diagnostic. Scores the draft across the six SUCCESs principles (Simple, Unexpected, Concrete, Credible, Emotional, Stories) plus the Curse of Knowledge villain axis on a 0/1/2 per-dimension scale (it is a checklist, not an equation), quoting evidence from the draft for every score and producing a top-3 prioritized fix list ranked by impact times effort. Use this skill whenever the user says things like "audit this message", "score this draft", "is this sticky", "run the SUCCESs check", "run the checklist", "will people remember this", "how good is this pitch", "rate this against Made to Stick", "does this pass the kidney heist test", "will this land", "stickiness review", "why is nobody remembering our launch", "I need a communications review", or when any user pastes a draft and asks whether it will resonate, be remembered, or change behavior. Also triggers when a user is about to ship a message and wants a last-mile quality gate, when someone asks for a one-page communications critique, or when a team is choosing between two draft versions and needs a principled scoring method. This skill produces a stickiness scorecard with dimension-level verdicts, evidence, prioritized fixes, and a recommendation for which specialist skill to invoke next (curse-of-knowledge-detector, core-message-extractor, curiosity-gap-architect, concrete-language-rewriter, credibility-evidence-selector, emotional-appeal-selector, story-plot-selector, or sticky-message-antipattern-detector). It does NOT perform the end-to-end rewrite — that is owned by the message-clinic workflow.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/stickiness-audit
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [1, 2, 3, 4, 5, 6, 12, 13]
tags: [communication, messaging, audit, scorecard, diagnostic, rubric, stickiness, success-framework, copywriting, communications-review]
depends-on:
  - curse-of-knowledge-detector
  - core-message-extractor
  - curiosity-gap-architect
  - concrete-language-rewriter
  - credibility-evidence-selector
  - emotional-appeal-selector
  - story-plot-selector
  - sticky-message-antipattern-detector
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Draft to audit — a message, pitch, announcement, slide, landing page, memo, tweet, speech, or email body as markdown or pasted text"
    - type: document
      description: "Audience description — role, context, and what they care about"
    - type: document
      description: "Goal — what the user wants the audience to remember, feel, or do after reading"
  tools-required: [Read, Write]
  tools-optional: [Grep, TodoWrite]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set working environment: the agent operates on short-form prose drafts supplied by the user."
discovery:
  goal: "Produce a rigorous, evidence-quoted SUCCESs + Curse-of-Knowledge scorecard for any draft, plus a top-3 prioritized fix list and a handoff recommendation to the right specialist skill."
  tasks:
    - "Score a draft pitch or announcement against the SUCCESs six-principle rubric"
    - "Decide which Made-to-Stick specialist skill should handle the highest-leverage fix"
    - "Compare two draft versions on a common stickiness scale before choosing one"
    - "Run a last-mile communications review before shipping"
  audience:
    roles: [marketer, founder, communicator, product-manager, teacher, technical-writer, fundraiser, internal-comms]
    experience: any
  when_to_use:
    triggers:
      - "User provides a draft and asks whether it will be remembered, resonate, or land"
      - "User wants a principled comparison between two or more draft versions"
      - "User is about to ship a high-stakes message and wants a pre-flight check"
    prerequisites: []
    not_for:
      - "Rewriting a draft end-to-end — hand off to message-clinic-runner"
      - "Running a single-axis check only — use the specialist skill for that axis directly"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
---

# Stickiness Audit

## When to Use

You have a draft message — a pitch, announcement, slide, landing page, memo, tweet, speech, or email — and you need a rigorous, evidence-grounded verdict on how sticky it is before shipping or choosing between versions. Use this skill when the goal is **diagnosis and prioritization**, not rewriting.

**Preconditions to verify before starting:**
- The draft exists as text the agent can read (paste, markdown file, or document).
- The audience is named (even roughly — "mid-market SaaS buyers", "all 400 employees", "first-time donors").
- The user's goal for the message is stated or can be extracted — what must the reader remember, feel, or do?

**The framing restated for the agent:** Sticky ideas — per the kidney heist urban legend used throughout Made to Stick as the gold standard — satisfy six principles and defeat one villain:
- **S**imple — Find the core and make it compact.
- **U**nexpected — Break a pattern; open a curiosity gap.
- **C**oncrete — Use sensory, observable language.
- **C**redible — Let the message vouch for itself (Sinatra test, vivid details, testable credentials).
- **E**motional — Make the reader feel something, usually by way of a specific person, not statistics.
- **S**tories — Use a plot (Challenge, Connection, or Creativity) that teaches or inspires action.
- **Villain: the Curse of Knowledge** — the expert blind spot that tempts the author to tap a tune only they can hear.

The scoring is **0/1/2 per dimension**, not a cumulative score. The book is emphatic: *"It's a checklist, not an equation."* A 2 on Emotional does not cancel a 0 on Simple. The audit surfaces gaps; the user fixes them.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **The draft:** The actual text to audit — not a summary.
  -> Check prompt for: pasted text, file path, document attachment.
  -> Ask if missing: "Paste the draft you want me to audit, or give me the file path."

- **The audience:** Who the draft is for.
  -> Check prompt for: audience description, persona, reader profile.
  -> Ask if missing: "Who is this for? One sentence: role + context + what they care about."

- **The goal:** What must the reader remember, feel, or do after reading?
  -> Check prompt for: phrases like "I want them to…", "the ask is…", "the takeaway should be…".
  -> Ask if missing: "If a reader forgets everything except one thing, what must that one thing be? And what do you want them to do next?"

### Observable Context (gather from environment)

- **Channel and length constraints:** A tweet and a keynote have different stickiness tolerances.
  -> Infer from: file name, format, stated character limits.
  -> Default if unclear: treat as a "short-form written message."

- **Prior versions:** A note like "we've already simplified it twice" tells you the Simple axis is already contested territory.
  -> Look for: user comments about previous drafts.

### Default Assumptions

- **Assumption: the draft's author is closer to the subject than the reader.** The Curse of Knowledge axis defaults to ON; you must actively score it.
- **Assumption: the reader cannot ask follow-up questions.** Most drafts are read asynchronously.
- **Assumption: "sticky enough" means the reader can recall the core message 24 hours later and act on it.** State this in the scorecard.

### Sufficiency Threshold

- **SUFFICIENT:** Draft text + audience description + stated goal.
- **PROCEED WITH DEFAULTS:** Draft + audience with role only. Flag the missing goal as `[assumed goal: X]` in the scorecard so the user can correct.
- **MUST ASK:** No draft, OR audience is "general public" with no narrowing (too vague to detect insider assumptions).

---

## Process

### Step 0: Initialize task tracking
**ACTION:** Create a TodoWrite checklist with one entry per dimension (Simple, Unexpected, Concrete, Credible, Emotional, Stories, Curse of Knowledge) plus "synthesize scorecard" and "structural self-check".
**WHY:** Seven axes in sequence is too many to hold in working memory; fused into one pass the agent defaults to whichever axis is most visible (usually Concrete or Simple) and under-scores the subtler ones (Curse of Knowledge, Emotional). The book's entire methodology is structured axis-by-axis because human authors cannot hold all seven at once. Tracking enforces the discipline.

### Step 1: Establish the audit frame
**ACTION:** Write a short frame at the top of your working notes that captures: (a) the draft's title or first sentence, (b) the audience in one line, (c) the stated goal (what must the reader remember / feel / do), (d) the channel, (e) whether this is a new draft or a comparison against a prior version. This is the lens you will score against.
**WHY:** Stickiness is always relative to an audience and a goal. A pitch that is 2/2 on Emotional for donors may be 0/2 for procurement buyers. Without an explicit frame every dimension score becomes a generic "is this good writing" judgment — which is exactly the failure mode a baseline agent produces.

**Save:** The audit frame as the first section of the scorecard.

### Step 2: Score dimension S — Simple
**ACTION:** Apply two tests. **Core test:** Can you state what the draft is *really* about in one sentence? If the draft makes more than one core claim, or the core is buried under context, it fails the core test. **Compact test:** Is the core expressed with a proverb-like compactness (short, memorable, pre-loaded with meaning)? Use the rubric in `references/success-dimension-rubric.md` for 0/1/2 criteria. Quote one passage as evidence for the score.
**WHY:** Chapter 1's central claim is that stickiness begins with Find the Core + Commander's Intent + proverb-compact expression. A draft that is missing a core is not "almost sticky" — it is structurally un-sticky, because there is nothing for the other principles to amplify. The Introduction's "maximize shareholder value" worked example is the canonical 0/2 on Simple: it states a vague goal the whole company could already agree with, which is the opposite of a core.

**If Simple scores 0 or 1** -> flag "core-message-extractor" as the recommended next step.

### Step 3: Score dimension U — Unexpected
**ACTION:** Ask two questions. **Pattern break:** Does the opening violate a schema the reader holds? Does it surprise them with something their mental model did not predict? **Curiosity gap:** Does the draft open a question in the reader's mind that the draft (or a follow-up) then closes? A draft that answers a question the reader was not yet asking cannot build curiosity. Score 0/1/2 per the rubric; quote evidence.
**WHY:** Chapter 2's mechanism is the gap theory of curiosity: readers only pay attention when they notice a gap between what they know and what they want to know. Drafts that lead with common-sense framing ("customer service is important") pre-fill the gap and lose attention in the first sentence. The kidney-heist story scores 2/2 here because "woke up in a bathtub of ice" violates every schema the reader holds.

**If Unexpected scores 0 or 1** -> flag "curiosity-gap-architect" as the recommended next step.

### Step 4: Score dimension C — Concrete
**ACTION:** Mark every noun in the draft that is either abstract (strategy, synergy, value, platform, solution, impact) or sensory/observable (ice, bathtub, runway, 131 passengers, Jared's pants). Compute rough ratio. **Boeing 727 test:** If you replaced the draft's abstract phrases with measurable constraints ("seat 131 passengers, land on a mile-long runway"), would meaning be lost or gained? If gained, the draft is under-concrete. Score 0/1/2 per the rubric; quote evidence.
**WHY:** Chapter 3 argues concreteness is the Velcro principle — more sensory hooks means more places for memory to stick. Abstract-only writing reads fine but leaves no residue. Non-experts can only anchor to concrete objects ("bishops moving diagonally", not "chess strategy"). JFK's "man on the moon this decade" is 2/2 Concrete; a modern CEO's "maximize shareholder value" is 0/2.

**If Concrete scores 0 or 1** -> flag "concrete-language-rewriter" as the recommended next step.

### Step 5: Score dimension C — Credible
**ACTION:** Identify every credibility move in the draft and classify it: **external authority** (expert quote, institutional citation), **anti-authority** (a credible first-person skeptic or ex-smoker type), **internal vivid details** (Hyundai cancer-cluster specificity), **statistics with a human anchor** (Nukes Stanford distance example), **Sinatra test** (one overwhelming example that alone makes the case — "if you can make it there…"), **testable credentials** (Wendy's "Where's the beef?" — a claim the reader can personally verify). A draft can score 2/2 with only one of these, done well. Drafts that lean on unverified adjectives ("world-class", "proven", "leading") score 0. Quote evidence.
**WHY:** Chapter 4's insight is that credibility is not the same as citations. The Heaths argue a single vivid detail (sweater color at the hospital visit) often out-credits a paragraph of statistics, because the reader's brain registers specificity as evidence of first-hand knowledge. Drafts that bury their credibility behind unverifiable adjectives fail here even if everything they say is technically true.

**If Credible scores 0 or 1** -> flag "credibility-evidence-selector" as the recommended next step.

### Step 6: Score dimension E — Emotional
**ACTION:** Ask three questions. **Who specifically?** Does the draft point to one identifiable person (Rokia, not "Africa's hungry")? **Which identity?** Does the draft connect to an identity the reader already holds ("Don't mess with Texas" triggers Texas-pride identity)? **Which associations?** Is the draft pulling emotional weight from associations the reader actually values (the reader's own kids vs. the author's abstract concern for "the community")? The Mother Teresa effect: a single identified victim beats a statistical many, every time. Score 0/1/2 per the rubric; quote evidence.
**WHY:** Chapter 5's claim is that emotion is not about making readers sad — it is about making them care, which requires wiring the message into an existing emotional circuit the reader already has. Statistics bypass emotion; specific people route through it. Drafts that try to manufacture emotion through adjective stacking ("devastating", "heart-wrenching") score lower than drafts with a named person and one concrete detail.

**If Emotional scores 0 or 1** -> flag "emotional-appeal-selector" as the recommended next step.

### Step 7: Score dimension S — Stories
**ACTION:** Determine whether the draft tells a story or merely asserts claims. A story has a **subject acting** (actor + verb), a **complication or challenge**, and a **resolution or lesson**. Identify the plot type if present: **Challenge plot** (underdog overcomes obstacle — Jared/Subway), **Connection plot** (bridge across a gap — Good Samaritan), **Creativity plot** (insight solves a puzzle — Apollo 13). A bullet list of features is not a story; a narrative about one user's specific day is. Score 0/1/2 per the rubric; quote evidence.
**WHY:** Chapter 6 argues stories are mental flight simulators — they rehearse behavior in a way assertions cannot. The kidney heist is a story; "the security of your body is at risk when traveling" is an assertion. The same idea, one sticks. Drafts that have strong Concrete and Emotional scores but 0 on Stories usually fail to change behavior because the reader never got to rehearse the action mentally.

**If Stories scores 0 or 1** -> flag "story-plot-selector" as the recommended next step.

### Step 8: Score the villain axis — Curse of Knowledge
**ACTION:** Re-read the draft from the audience's point of view. List every term, acronym, framework reference, named internal tool, or buried assumption that would force a non-expert reader to pause. Apply the tapper/listener heuristic: if the author "knows what they mean" but the reader would not, the draft is tapping. Score 0/1/2 per the rubric (0 = visibly corrupted by expertise, 1 = some insider residue, 2 = a non-expert could parse it cold). Quote evidence.
**WHY:** The Curse of Knowledge is the book's named villain, and the Epilogue treats it as the root cause of most stickiness failures. It is scored separately from Simple because a draft can have a clear core and still be Curse-corrupted (the core is clear to insiders and opaque to outsiders). Scoring it as a seventh dimension prevents the agent from collapsing it into Simple and under-counting its impact.

**If Curse of Knowledge scores 0 or 1** -> flag "curse-of-knowledge-detector" as the recommended next step for deeper diagnosis.

### Step 9: Anti-pattern sanity pass
**ACTION:** Before synthesizing, run a quick check for the three named anti-patterns the book warns about: **burying the lead** (is the actual news in paragraph 4?), **decision paralysis** (does the draft offer too many options so the reader picks none?), and **analysis by jargon / common-sense sedation** (sentences any reader would already nod along to before reading). If any fire, add them as cross-cutting findings to the scorecard — they usually explain why a draft can score 1s across the board but still fail.
**WHY:** These anti-patterns are not captured cleanly by any single dimension. A draft can be Concrete, Credible, and Emotional while still burying the lead in paragraph 4 — at which point no one reads far enough to hit the good stuff. For deeper diagnosis of these patterns, delegate to `sticky-message-antipattern-detector`.

### Step 10: Synthesize the scorecard
**ACTION:** Produce a single markdown file, `stickiness-scorecard.md`, using the template at `references/scorecard-template.md`. It must include:
1. **Audit frame** — draft title, audience, goal, channel.
2. **Scorecard table** — seven rows (S, U, C, C, E, S, Curse), each with: score (0/1/2), one-sentence verdict, quoted evidence.
3. **Kidney-heist comparison line** — one sentence naming which dimensions the draft hits at 2/2 kidney-heist level and which it misses.
4. **Top 3 rewrite targets** — ranked by (severity × how much of the draft they poison). Each target gets: dimension, quoted passage, specific fix, estimated effort (S/M/L).
5. **Handoff recommendations** — for each dimension that scored 0 or 1, the name of the specialist skill to invoke next and why that skill (not another) is the right next step.
6. **Final verdict** — one of: **Sticky (ready to ship)**, **At risk (fix top 2 before shipping)**, **Not sticky (structural rework required)**. State which thresholds triggered the verdict.

**WHY:** The user is not here for a long table — they are here for a decision. The scorecard's value is the top-3 + handoff + verdict. Without those three artifacts the audit produces decision paralysis, which is the exact anti-pattern Chapter 1 warns about. The kidney-heist comparison is the book's own gold-standard calibration — it forces the audit to be concrete about *how much better* the draft could be.

**Save:** `stickiness-scorecard.md` in the user's working directory.

### Step 11: Structural self-check
**ACTION:** Before returning, verify: (a) every dimension has a score, a verdict, AND quoted evidence — not just a number; (b) the kidney-heist comparison line is present; (c) the top-3 are actually ranked (not just listed) and each names an effort estimate; (d) the handoff recommendations name specific specialist skills from the dependency list, not generic advice; (e) the final verdict matches the dimension scores (cannot say "Sticky" with two 0s on the card); (f) no dimension was collapsed into "it's fine" without evidence.
**WHY:** The audit's value is specificity + decisiveness. A scorecard that says "could be improved" on every axis is indistinguishable from baseline agent output. Quoted evidence, ranked top-3, and named handoffs are what make this skill book-derived rather than generic writing feedback.

---

## Inputs

- `draft` — the text to audit (markdown, pasted text, or file path).
- `audience` — one sentence: role + context + what they care about.
- `goal` — what the reader must remember, feel, or do after reading.
- Optional: `prior_version` — a previous draft for comparative scoring.

## Outputs

A single file, `stickiness-scorecard.md`, following the template at [references/scorecard-template.md](references/scorecard-template.md). At a glance:

```markdown
# Stickiness Scorecard — {draft name}

## Audit Frame
- Audience: {...}
- Goal: {...}
- Channel: {...}

## Scorecard
| Dimension            | Score | Verdict (one line)       | Evidence (quoted)    |
|----------------------|-------|--------------------------|----------------------|
| Simple               | 0/1/2 | {...}                    | "..."                |
| Unexpected           | 0/1/2 | {...}                    | "..."                |
| Concrete             | 0/1/2 | {...}                    | "..."                |
| Credible             | 0/1/2 | {...}                    | "..."                |
| Emotional            | 0/1/2 | {...}                    | "..."                |
| Stories              | 0/1/2 | {...}                    | "..."                |
| Curse of Knowledge   | 0/1/2 | {...}                    | "..."                |

## Kidney-Heist Comparison
{One sentence: which dimensions match the gold-standard kidney-heist 2/2 and which miss.}

## Top 3 Rewrite Targets
1. **{Dimension}** — "{quoted passage}" — Fix: {specific}. Effort: S/M/L.
2. ...
3. ...

## Handoff Recommendations
- {Dimension that scored 0-1} -> invoke `{specialist-skill}` because {reason}.
- ...

## Final Verdict
**{Sticky | At risk | Not sticky}** — {one-sentence rationale matching the scores above.}
```

---

## Key Principles

- **It is a checklist, not an equation.** The Heaths are emphatic: summing scores misses the point. A 2/2 on five dimensions does not redeem a 0 on Simple, because a draft without a clear core has nothing for the other principles to amplify. Report per-dimension scores only; refuse to produce a "total".

- **Every score carries a quoted passage.** The audit's value is evidence. A score without a quote is just an opinion — and opinions are exactly what a baseline agent produces. Quoting the specific sentence that earned the score makes the audit auditable by the user, which is the skill's credibility test (see Chapter 4: "let the details vouch for the claim").

- **The kidney heist is the calibration point.** Every audit compares the draft to the kidney-heist urban legend as the 2/2-on-everything reference. This is not theatrical — it is the book's own gold standard. When a dimension scores 0 or 1, the audit must be able to say "here is how the kidney heist does this and here is what the draft is missing."

- **Dimension weakness dictates the handoff.** The audit does not fix drafts — it diagnoses them and routes the user to the right specialist skill. A 0 on Concrete means `concrete-language-rewriter`. A 0 on Simple means `core-message-extractor`. A 0 on Curse of Knowledge means `curse-of-knowledge-detector`. Never recommend "go make it better" — that is baseline advice and destroys the skill's delta.

- **Curse of Knowledge is scored separately.** A draft can have a crystal-clear core and still be Curse-corrupted. Collapsing the Curse into Simple under-counts its impact, which is the single most common audit error. Score it seventh, always, even if every other dimension looks fine.

- **Prioritize ruthlessly; report faithfully.** The top-3 is the action surface; the full scorecard is the audit trail. Without the top-3 the user drowns in findings (the decision-paralysis anti-pattern the book explicitly warns against). Without the full scorecard the user cannot trust the top-3. Both are required.

- **Deeper diagnosis belongs to specialists.** The audit runs a quick inline check per dimension. When a dimension scores 0 or 1 AND the user wants to act, invoke the specialist skill rather than attempting a deeper audit inline — that is what the depends-on graph exists for. The audit's job is routing, not forensic detail.

---

## Examples

**Scenario: "Maximize shareholder value" CEO memo (the book's canonical weak baseline)**

Trigger: User pastes a 300-word all-hands memo titled "Our North Star for FY26" containing phrases like "maximize shareholder value", "synergies across business units", and "best-in-class operational excellence." Audience: "all 400 employees, mixed roles, most have never attended strategy meetings." Goal: "get everyone rowing in the same direction."

Process: (1) Audit frame captures audience + goal. (2) Simple = 0/2: no identifiable core; "shareholder value" is a goal the whole company already knew. Evidence quoted. (3) Unexpected = 0/2: every sentence is something the reader would pre-agree with (common-sense sedation). (4) Concrete = 0/2: every noun is abstract; Boeing 727 test confirms measurable constraints would gain meaning. (5) Credible = 1/2: one internal statistic is cited but without a vivid anchor. (6) Emotional = 0/2: no named person, no identity hook. (7) Stories = 0/2: zero narrative — pure assertion. (8) Curse of Knowledge = 0/2: "North Star metric" and three internal initiative names assume reader context they don't have. (9) Anti-pattern pass flags burying the lead and common-sense sedation. (10) Synthesize: final verdict **Not sticky — structural rework required**.

Output: `stickiness-scorecard.md` with Top 3 = (1) extract a concrete core using `core-message-extractor`, (2) replace "North Star metric" with the actual metric and its target number using `concrete-language-rewriter`, (3) add a "what changes for you on Monday" paragraph per role group. Kidney-heist comparison: "Kidney heist scores 2/2 on all six; this memo scores 0/2 on five of seven dimensions — the Made-to-Stick canonical worked example of a structurally un-sticky message." Handoff: invoke `core-message-extractor` first because every other fix is downstream of it.

**Scenario: Nonprofit email blast ahead of giving day**

Trigger: User pastes a 400-word email opening "Our 2026 impact report shows 14 programs reached 47,000 beneficiaries across sub-Saharan maternal health." Audience: "first-time $25-$100 donors." Goal: "convert to a first gift."

Process: (1) Frame captured. (2) Simple = 1/2: there is a core ("your gift saves mothers") but it's buried in statistics. Evidence quoted. (3) Unexpected = 0/2: opens with a report finding, which is exactly what the reader expected. (4) Concrete = 1/2: the number 47,000 is concrete but not sensory; no named person. (5) Credible = 2/2: the program data itself is specific and testable. (6) Emotional = 0/2: pure statistics, Mother Teresa effect inverted — no named beneficiary. (7) Stories = 0/2: no narrative, only claims. (8) Curse of Knowledge = 1/2: "catchment area" and "M&E framework" leak through once each. (9) Anti-pattern pass flags burying the lead (the actual ask is in paragraph 4). (10) Final verdict **At risk — fix top 2 before shipping**.

Output: Top 3 = (1) open with a named beneficiary (one mother, one specific birth) via `emotional-appeal-selector`, (2) restructure to a Connection-plot story via `story-plot-selector`, (3) move the ask to the top via anti-pattern fix. Kidney-heist comparison: "credibility is kidney-heist-level; emotional and story axes are inverted — the draft leads with numbers where kidney heist would lead with one person in one bathtub." Handoff: `emotional-appeal-selector` first because it unlocks both the Emotional and the Stories axes.

**Scenario: Developer-tool landing page hero — comparing two versions**

Trigger: User pastes two versions of a landing page hero. V1: "Unified observability platform for cloud-native workloads." V2: "Know which of your 400 microservices broke in the last deploy before your customers do." Audience: "backend engineers at mid-size SaaS companies." Goal: "sign up for a 14-day trial."

Process: (1) Run the full audit on both versions. (2) V1 scorecard: Simple 1/2 (core exists but generic), Unexpected 0/2, Concrete 0/2, Credible 0/2 ("platform" is an adjective-of-assertion), Emotional 0/2, Stories 0/2, Curse 0/2 ("unified observability" is pure insider jargon). V2 scorecard: Simple 2/2 (core is "catch bad deploys before customers do"), Unexpected 1/2, Concrete 2/2 ("400 microservices", "last deploy"), Credible 1/2 (testable by the reader's own memory of past incidents), Emotional 1/2 (wires into the fear of a customer-reported incident), Stories 1/2 (implicit micro-narrative), Curse 2/2. (3) Kidney-heist comparison favors V2 across six of seven dimensions. (4) Final verdict: ship V2; V1 is "Not sticky — structural rework required".

Output: A scorecard for each version plus a one-line recommendation: "Ship V2. V1 loses to V2 on six of seven dimensions including the structural Simple and Concrete axes — this is not a stylistic preference, it is the SUCCESs rubric reporting a clean dominance." No specialist handoff needed — V2 is ready.

---

## References

- For the full 0/1/2 rubric per dimension with book-sourced pass/fail criteria, see [success-dimension-rubric.md](references/success-dimension-rubric.md)
- For the exact markdown template the scorecard must fill in, see [scorecard-template.md](references/scorecard-template.md)

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Made to Stick: Why Some Ideas Survive and Others Die by Chip Heath and Dan Heath.

## Related BookForge Skills

This is a Level 1 hub skill — it delegates specialized diagnoses to the Level 0 foundation skills. Install from ClawhHub:

- `clawhub install bookforge-curse-of-knowledge-detector` — deeper diagnosis when the Curse axis scores low
- `clawhub install bookforge-core-message-extractor` — invoked when Simple scores low
- `clawhub install bookforge-curiosity-gap-architect` — invoked when Unexpected scores low
- `clawhub install bookforge-concrete-language-rewriter` — invoked when Concrete scores low
- `clawhub install bookforge-credibility-evidence-selector` — invoked when Credible scores low
- `clawhub install bookforge-emotional-appeal-selector` — invoked when Emotional scores low
- `clawhub install bookforge-story-plot-selector` — invoked when Stories scores low
- `clawhub install bookforge-sticky-message-antipattern-detector` — invoked when Step 9 flags burying-the-lead, decision-paralysis, or common-sense sedation

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
