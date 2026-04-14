---
name: concrete-language-rewriter
description: Rewrite abstract, theoretical, or jargon-heavy passages into sensory, schema-based language the audience can already picture — using three named techniques (schema tap, high-concept pitch, generative analogy). Use this skill whenever a draft sounds abstract, strategy-level, or theoretical and the user wants it grounded in concrete imagery the reader can see, hear, touch, or do. Activate when the user says "this sounds abstract", "make it more concrete", "feels jargon-y", "how do I explain this", "rewrite this pitch", "too theoretical", "simplify the language", "ground this", "make it tangible", "the reader can't picture it", "I'm stuck at the strategy level", "translate this into plain language", "make this vivid", "needs an analogy", "give me a one-liner pitch", "explain this to a 5-year-old", "we need a metaphor for this", or provides an abstract passage plus an audience and asks to concretize it. Also triggers when a mission statement, value prop, policy memo, product page, cultural value, onboarding doc, or training scenario reads like a thesaurus of abstractions (synergy, excellence, alignment, optimize, empower, leverage, robust, scalable, best-in-class). The skill does NOT invent fake sensory details to ground a claim the user has not actually made, does NOT score the whole SUCCESs rubric (that is the stickiness-audit skill), and does NOT write full narrative stories (that is the story-framing skill) — it produces a side-by-side before/after rewrite of each flagged abstract passage with the technique used and why.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/concrete-language-rewriter
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [3, 13]
tags: [communication, concrete-language, rewriting, analogy, messaging, copywriting, plain-language, metaphor, pitch, clarity]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Draft with abstract passages — a message, pitch, value prop, mission statement, explainer, cultural values doc, or product page"
    - type: document
      description: "Audience reference points — what the audience already knows, does, sees daily, or has experienced (used as the source material for schemas and analogies)"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set environment — the agent operates on short prose artifacts supplied by the user."
discovery:
  goal: "Rewrite abstract passages into concrete, schema-anchored language by applying one of three named techniques chosen to fit the passage and the audience."
  tasks:
    - "Rewrite a jargon-heavy value proposition into something the reader can picture"
    - "Produce a one-sentence high-concept pitch for a new product or idea"
    - "Design a generative analogy that keeps steering behavior after it is stated"
    - "Swap abstract strategy talk for behavior-level language in a cultural values doc"
  audience:
    roles: [marketer, founder, product-manager, communicator, teacher, executive, technical-writer]
    experience: any
  when_to_use:
    triggers:
      - "User says a passage sounds abstract, jargon-y, or theoretical and asks to ground it"
      - "User needs a one-liner pitch for a product or initiative"
      - "Cultural values or strategy doc is full of words like synergy, alignment, empower"
      - "User wants an analogy that non-experts will immediately picture"
    not_for:
      - "Inventing fabricated sensory details to prop up a claim the user has not actually made"
      - "Full SUCCESs rubric scoring (use stickiness-audit)"
      - "Multi-paragraph narrative stories (use story-framing)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: "pending"
    eval_count: 0
---

# Concrete Language Rewriter

## When to Use

You have a draft — a pitch, value prop, mission statement, explainer, internal memo, training doc, or product page — containing passages that sound abstract, theoretical, or jargon-heavy. The user wants those passages rewritten into sensory, schema-based language the audience can already picture. Before starting, confirm: (1) which passages are to be rewritten (user-flagged or agent-flagged), (2) who the audience is and what reference points they already share, (3) whether the user wants a one-shot pitch (high-concept), an idea that keeps producing behavior (generative analogy), or fast comprehension (schema tap).

The core mechanic: abstract ideas only stick when they hook onto concrete things already in the reader's memory (the "Velcro theory of memory" from Chapter 3). The more sensory hooks, the better the retention. "White things" is vague; "white things in your refrigerator" is concrete. This skill turns the first into the second.

## Context & Input Gathering

### Required Context (must have — ask if missing)
- **The draft:** The actual passage(s) to rewrite, verbatim.
  -> Check prompt for: pasted text, a file path, or attached document
  -> If missing, ask: "Paste the passage you want rewritten, or give me the file path."
- **The audience:** Who will read this and what schemas they already have.
  -> Check prompt for: role names, job titles, prior experience mentions
  -> Check environment for: `audience-profile.md`, `brief.md`, `persona.md`
  -> If still missing, ask: "Who is the audience? What do they already know and see every day that I can anchor this to?"

### Observable Context (gather from environment)
- **Related drafts:** Other versions, earlier pitches, or competitor messaging.
  -> Look for: `draft.md`, `existing-copy.md`, `core-message.md`
  -> If unavailable: work from the single passage provided.
- **Technique preference:** Whether the user wants a pitch, a generative analogy, or a quick explanation.
  -> Look for: words like "pitch", "one-liner", "culture", "values", "explain"
  -> If unavailable: infer from the passage type (see Step 2).

### Default Assumptions
- If no audience is given and one cannot be asked for: assume "intelligent non-expert in the domain" and state this in the output.
- Preserve the user's claim. Do not invent new facts to ground it — find existing audience schemas that match the claim you already have.

### Sufficiency Threshold
SUFFICIENT: passage + audience schemas known
PROCEED WITH DEFAULTS: passage known, audience assumed as "intelligent non-expert" (noted in output)
MUST ASK: no passage provided

## Process

### Step 1: Flag abstract passages
**ACTION:** Read the draft and mark every passage that is (a) a pure abstraction with no sensory anchor, or (b) strategy-level language that does not specify observable behavior. Output a numbered list of flagged passages. If the user already flagged specific passages, use their list and skip scanning.

**WHY:** Rewrites fail when applied to the wrong target. Concrete language is not always better — a correctly concrete sentence should be left alone. Flagging first forces an explicit decision about what actually needs work and produces an auditable list the user can challenge before any rewriting starts.

**Flag tests (any one triggers a flag):**
- Contains an abstract noun with no example: `synergy`, `excellence`, `innovation`, `alignment`, `value`, `quality`, `empowerment`, `transformation`, `optimization`.
- Describes a goal without naming an observable behavior or measurable constraint (e.g., "be the best airline" vs "land a 131-passenger jet on La Guardia Runway 4-22").
- Uses a word the reader cannot picture, touch, or do.
- Is a cultural value or strategy statement that does not name the daily object, phrase, or action the reader should change.

**Artifact:** `flagged-passages.md` — numbered list with the verbatim text of each flagged passage.

### Step 2: Pick the technique for each flagged passage
**ACTION:** For each flagged passage, choose ONE of three techniques based on the decision rule below. Record the choice and the one-sentence reason.

**WHY:** The three techniques are not interchangeable — they solve different problems. Schema tap is for explaining *what a thing is* in under five seconds. High-concept pitch is for positioning a new thing relative to two familiar things. Generative analogy is for seeding a mental model that will keep producing decisions long after the user stops reading. Mixing them up produces rewrites that are clever but do not fit the job.

**Decision rule:**

| If the user needs... | Use | Why |
|---|---|---|
| Quick comprehension ("what IS this thing?") | **Schema tap** | Leverages one existing schema the audience already owns |
| A one-shot positioning pitch ("how is this different?") | **High-concept pitch** | Combines two schemas to place a new idea at their intersection |
| Behavior that keeps aligning after the message is delivered | **Generative analogy** | Seeds a frame that the audience re-uses to make new decisions autonomously |

**IF** the passage is a product tagline, cold-open, or elevator line -> **High-concept pitch**
**ELSE IF** the passage is a cultural value, onboarding frame, or ongoing team norm -> **Generative analogy**
**ELSE** -> **Schema tap**

**Artifact:** Extend `flagged-passages.md` with a `technique:`, `why:`, and `canonical exemplar:` line under each entry.

**MANDATORY — name the lineage.** Every rewrite must cite BOTH (a) the technique used, and (b) the closest canonical exemplar from *Made to Stick* that the rewrite echoes. This is not optional decoration — it is how the user builds the catalog mentally while using the skill, and how a reviewer can trace the rewrite back to the book's proven patterns. Use this map:

| Technique | Canonical exemplars from the book (pick the closest fit) |
|---|---|
| Schema tap | **the pomelo example** (grapefruit crossed with a football); **Aesop's Fox & the Grapes** (parable as packed schema) |
| High-concept pitch | **"Die Hard on a bus"** (the movie *Speed*); other "X meets Y" Hollywood pitches |
| Generative analogy | **Disney "cast members"** (theme park as stage production); **Kris & Sandy** (accounting class reframed as investigative journalism) |
| Behavior-level swap | **Boeing 727 constraint** ("seat 131 passengers, fly Miami–NYC nonstop, land on La Guardia Runway 4-22"); **Jane Elliott's blue-eyes / brown-eyes exercise** (felt experience replaces lecture) |

Every rewrite's output row MUST carry a phrase like *"Schema tap — like the pomelo example"* or *"Generative analogy — like Disney cast members"*.

### Step 3: Rewrite with Technique 1 — Schema tap
**ACTION:** If the chosen technique is schema tap, find one thing the audience already owns in memory that shares the most critical feature of the abstract idea, then describe the abstract idea in terms of that thing plus a minimal delta.

**WHY:** A new abstraction with zero sensory hooks fails to stick regardless of how accurately it is stated. Tapping an existing schema inherits all of the hooks from the familiar thing for free — the reader does not have to build new memory, only modify existing memory.

**Template:** `{new thing} is like {familiar thing} except {one delta}.`

**Example — pomelo:** Instead of "a large citrus fruit native to Southeast Asia with a thick rind and mild flavor", say "a pomelo is a grapefruit crossed with a football." The reader owns both "grapefruit" and "football" — size, shape, and category arrive in one sentence.

**Checklist for a good schema tap:**
- The familiar thing is visible, touchable, or doable — not another abstraction.
- The delta is ONE thing, not five.
- The reader could draw it after reading it.

### Step 4: Rewrite with Technique 2 — High-concept pitch
**ACTION:** If the chosen technique is a high-concept pitch, find two familiar things from the audience's cultural library whose intersection captures the new idea, and write it as "`{familiar thing A} meets {familiar thing B}`" or equivalent.

**WHY:** High-concept pitches are the Hollywood trick: they let a producer green-light a new project in 30 seconds because both reference points are already fully loaded in the audience's head. The pitch is doing the work of a five-paragraph positioning statement by paying in two words of borrowed context.

**Templates:**
- `{A} meets {B}`
- `{A} for {new domain}`
- `The {A} of {new domain}`
- `{A}, but {B}`

**Example — "Die Hard on a bus":** The movie *Speed* was pitched as "Die Hard on a bus." Both reference points are concrete and already loaded in every producer's head (action-hero hostage thriller + claustrophobic single-location constraint). The audience knew the genre, the pacing, and the stakes immediately.

**Checklist for a good high-concept pitch:**
- Both reference points are genuinely known to the audience (not just to you).
- The combination actually captures the new thing's main feature, not just its vibe.
- It fits in one breath.

### Step 5: Rewrite with Technique 3 — Generative analogy
**ACTION:** If the chosen technique is a generative analogy, choose a source frame whose internal vocabulary, roles, and daily actions will re-apply to the target domain in ways that keep generating decisions after the message is stated. Then rewrite the passage to install the analogy and, optionally, list 2–4 specific objects or actions it renames.

**WHY:** Generative analogies are the highest-leverage concrete technique because the analogy keeps doing work after the user is gone. A good generative analogy lets frontline employees make dozens of small decisions correctly without ever checking back with a manager — the frame tells them what to do.

**Example — Disney "cast members":** Disney reframed the theme park as a stage production. Employees became "cast members", customers became "guests", uniforms became "costumes", walking areas became "onstage" vs "backstage". An 18-year-old hired last week knows — without being told — that you do not step "offstage" in costume, that you perform your role even on a bad day, and that guests are your audience, not your transaction counterparty. The analogy generates the policy for situations no handbook covered.

**Checklist for a good generative analogy:**
- The source frame has a rich internal vocabulary the audience already knows (theater, kitchen, cockpit, newsroom, emergency room, baseball).
- At least 3 daily objects or actions can be renamed without forcing it.
- The new frame steers a behavior the user actually wants (not a behavior that just sounds good).

### Step 6: Swap abstract strategy talk for behavior-level language
**ACTION:** For flagged passages that describe a *strategy* or *goal* rather than a *schema* — e.g., "be the leading provider of X" — do not apply an analogy. Instead, rewrite the passage as a measurable constraint or observable behavior. Replace quality adjectives with numbers, dates, or named actions.

**WHY:** Strategy-level statements ("be the best", "excellence in Y", "world-class Z") do not coordinate behavior because they cannot be pictured, measured, or disputed. A concrete constraint can be shared across teams that never meet — it acts as a self-coordinating reference point. This is why Boeing's 727 design goal was "seat 131 passengers, fly nonstop Miami–NYC, land on La Guardia Runway 4-22" rather than "best passenger plane in the world". Thousands of engineers across specialties could self-coordinate from the constraint; no one could coordinate from the adjective.

**Transform:**
- Quality adjective -> measurable constraint (`best` -> `under 200ms p95`)
- Abstract goal -> observable action (`empower our users` -> `every user can publish without asking support`)
- Strategy noun -> verb the reader performs (`alignment` -> `everyone writes the same one-sentence answer when asked what we are building`)

### Step 7: Produce the side-by-side deliverable
**ACTION:** Write the final artifact as a side-by-side before/after table (or structured markdown), with technique, canonical exemplar, rationale, and any caveats. For each flagged passage, include:
1. The original text (verbatim).
2. The technique chosen.
3. The **canonical exemplar** from *Made to Stick* whose pattern this rewrite echoes (e.g., "like the pomelo example", "like Disney cast members", "like Die Hard on a bus", "like Boeing's 727 runway constraint", "like Jane Elliott's blue-eyes exercise", "like Kris & Sandy", "like Aesop's Fox & the Grapes"). REQUIRED — not optional.
4. The rewrite.
5. One line explaining why the rewrite uses concrete hooks the original lacked.
6. (If applicable) A "caveat" line noting any claim the rewrite intentionally did not invent support for.

**Table form (REQUIRED columns):** Every side-by-side table must have four columns:

| Original | Rewrite | Technique | Canonical Exemplar |
|---|---|---|---|

The `Canonical Exemplar` column is non-optional — a row missing it is an incomplete deliverable and must be rejected during Step 8.

**WHY:** A rewrite without the reasoning is a magic trick — the user cannot apply it to the next passage, and cannot tell whether to accept or reject it. Showing the technique and its rationale turns the deliverable from a one-shot fix into a teachable artifact.

**Artifact:** `concrete-rewrite.md` — see template in `references/output-template.md`.

### Step 8: Self-check for fabricated detail
**ACTION:** Re-read each rewrite and verify that no sensory detail was invented to prop up a claim the original did not make. If a rewrite added a number, a name, a physical feature, or a specific example that is not in the source material or the user's knowledge, either flag it as `[assumption — verify]` or remove it.

**WHY:** Concrete language can become a lie if it invents specifics the user cannot defend. "We serve 10,000 customers daily" is concrete and sticky — and catastrophic if the user only has 400 customers. This skill is explicitly out-of-scope for fabricating details; Step 8 is the enforcement step. A rewrite that needs invented detail means the user must supply the detail or the technique was wrong.

**IF** any rewrite contains fabricated specifics -> mark `[assumption — verify]` inline or replace with a schema tap that uses only the audience's existing knowledge
**ELSE** -> mark the artifact complete.

## Inputs
- **Draft:** prose passage(s) to rewrite.
- **Audience schemas:** what the audience already knows, sees, or does (roles, domain, prior experience).
- **Optional:** technique preference (schema / pitch / generative), channel (tagline / memo / slide), tone constraints.

## Outputs
- **`flagged-passages.md`** — numbered list of abstract passages with assigned technique and reason.
- **`concrete-rewrite.md`** — the side-by-side deliverable. Template:

```markdown
# Concrete Rewrite

Audience: {audience description}

## Summary table

| Original | Rewrite | Technique | Canonical Exemplar |
|---|---|---|---|
| {verbatim original} | {rewrite} | {schema tap / high-concept pitch / generative analogy / behavior-level swap} | like {pomelo / Disney cast members / Die Hard on a bus / Boeing 727 runway constraint / Jane Elliott blue-eyes / Kris & Sandy / Aesop's Fox & the Grapes} |

## Passage 1
**Technique:** {schema tap | high-concept pitch | generative analogy | behavior-level swap}
**Canonical exemplar:** like {pomelo example | Disney cast members | Die Hard on a bus | Boeing 727 runway constraint | Jane Elliott blue-eyes exercise | Kris & Sandy | Aesop's Fox & the Grapes}

**Before:**
> {verbatim original}

**After:**
> {rewrite}

**Why this works:** {one line — which existing hook(s) the rewrite taps, and how it echoes the exemplar's pattern}

**Caveats:** {any `[assumption — verify]` flags, or "none"}

## Passage 2
...
```

## Key Principles

- **Velcro, not paint.** Concrete language is not about making prose prettier — it is about attaching the idea to hooks already in the reader's memory. More hooks = better retention. If a rewrite adds adjectives but no new hooks, it has not concretized anything.
- **Borrow schemas, do not manufacture facts.** The sensory detail must come from what the audience already owns (pomelo leans on grapefruit + football) or from what the user can honestly claim (Boeing's actual runway constraint). Never invent specifics to make an abstract claim feel more real — that is lying, not concretizing.
- **Three techniques, three jobs.** Schema tap = comprehension speed. High-concept pitch = one-shot positioning. Generative analogy = ongoing behavior steering. Picking the wrong technique wastes the rewrite: a high-concept pitch cannot run a culture, and a generative analogy cannot fit on a billboard.
- **Constraints coordinate, adjectives do not.** When a passage describes a goal or strategy, the fix is not an analogy — it is a measurable constraint. "Best" cannot coordinate 500 engineers; "fits in under a mile of runway" can. Replace quality adjectives with numbers, dates, or named actions whenever the passage is a goal.
- **Rewriting is audit-able or it is arbitrary.** Always show the technique and the reason next to the rewrite. The user needs to be able to reject a rewrite and know why it is wrong, or apply the same move to the next passage tomorrow.
- **Name the lineage.** Every rewrite declares which of the 3 techniques it used AND which canonical book exemplar it echoes — "like the pomelo", "like Disney cast members", "like Die Hard on a bus", "like Boeing's 727 runway constraint", "like Jane Elliott's blue-eyes exercise", "like Kris & Sandy", "like Aesop's Fox & the Grapes". This is how users build the catalog mentally while using the skill, not just the technique abstraction. An unlabeled rewrite is an incomplete rewrite.
- **More hooks = more memory.** "White things" is vague. "White things in your refrigerator" is concrete. Every additional hook (color, container, location, use) multiplies retention — but only if each hook is real to the audience.

## Examples

**Scenario: abstract value proposition for a developer tool**
Trigger: User says "our landing page hero feels too abstract — it says 'unified observability platform for cloud-native workloads' and nobody gets it. Audience: backend engineers at mid-size startups."
Process: (1) Flag the passage — "unified observability platform for cloud-native workloads" is three stacked abstractions. (2) Choose high-concept pitch — it is a product tagline. (3) Rewrite: "Datadog for teams that can't afford Datadog" — two familiar reference points (known product + known pain), instant positioning. (4) Self-check: "can't afford Datadog" is a claim about audience economics, not about our product — safe.
Output: `concrete-rewrite.md` row — **Technique:** high-concept pitch; **Canonical exemplar:** like "Die Hard on a bus" (the *Speed* pitch); **Rationale:** "leverages the audience's existing schema of Datadog and its known price-point pain, placing the new product at a specific intersection in one breath — the same two-schema collision trick that let a Hollywood producer green-light *Speed* in 30 seconds."

**Scenario: mission statement for customer support reorg**
Trigger: User shares a draft values doc: "We aim to empower partnership-oriented interactions that drive mutual long-term value with our customer community." Audience: customer support agents.
Process: (1) Flag — entire sentence is strategy-level abstraction with zero behavior. (2) Choose generative analogy — it is meant to shape ongoing behavior, not a one-shot pitch. (3) Rewrite: reframe support agents as "co-pilots, not gate agents." List renames: tickets -> "missions", SLAs -> "flight plans", escalations -> "hand-offs to the captain". (4) Self-check — no invented facts; all renames are metaphor, not claim.
Output: `concrete-rewrite.md` row — **Technique:** generative analogy; **Canonical exemplar:** like Disney "cast members" (theme park as stage production); **Rationale:** "the co-pilot frame keeps generating decisions the way Disney's cast-member frame tells a brand-new hire they do not step offstage in costume — a co-pilot does not close a mission before the captain lands safely, which maps to 'do not close a ticket until the customer confirms resolution.' Daily vocabulary (tickets -> missions, SLAs -> flight plans, escalations -> hand-offs) renames at least 3 objects, clearing the Disney-style test from Step 5."

**Scenario: training material for new product managers**
Trigger: User asks, "How do I teach new PMs what it feels like when another team blocks their work? It keeps coming out as a lecture about stakeholder alignment."
Process: (1) Flag — "stakeholder alignment" is the core abstraction. (2) Choose schema tap — the goal is comprehension, not positioning. (3) Rewrite: design a short in-class simulation modeled on Jane Elliott's blue-eyes/brown-eyes exercise (Chapter 3) — split the PMs into two teams, give team A the tooling and team B the deadline, force team B to request every build from team A for 20 minutes. (4) Self-check — simulation rules are concrete and can be run with no invented facts about the PMs.
Output: `concrete-rewrite.md` row — **Technique:** schema tap (delivered as a felt experience); **Canonical exemplar:** like Jane Elliott's blue-eyes / brown-eyes exercise (Chapter 3); **Rationale:** "a felt experience (being blocked by another team's schedule) builds direct memory the way Elliott's blue-eyes / brown-eyes exercise made discrimination concrete for a classroom of 8-year-olds — lecturing about 'alignment' does not. The PMs now own a 20-minute schema they can tap when the abstract word 'stakeholder' resurfaces."

## References
- For a reusable output template, see [references/output-template.md](references/output-template.md)
- For an expanded catalog of schema-tap, high-concept-pitch, and generative-analogy patterns with more worked examples (Aesop's Fox and Grapes parable compression, Disney cast-member system, Kris & Sandy accounting case, Boeing 727 runway constraint, Jane Elliott blue-eyes exercise), see [references/technique-catalog.md](references/technique-catalog.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Made to Stick: Why Some Ideas Survive and Others Die* by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
