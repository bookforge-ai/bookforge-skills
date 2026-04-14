---
name: message-clinic-runner
description: "Run the full Made-to-Stick Idea Clinic on a draft message — diagnose it against SUCCESs, rewrite the weak dimensions, and ship a before/after pair with a one-sentence punch line explaining why the revision works. This is the end-to-end rework orchestrator for ONE draft at a time. Use this skill whenever the user says 'make this stickier', 'rewrite this message', 'improve this draft', 'run the clinic on this', 'full SUCCESs rework', 'before and after rewrite', 'fix this pitch', 'rework this announcement', 'this copy isn't landing — fix it', 'I need a sticky version of this', 'turn this into a kidney-heist version', 'make my announcement memorable', 'revise this fundraising email', 'rewrite this landing page hero', 'clinic this', 'do the Heath brothers treatment on this', 'rewrite end-to-end', or pastes a draft and asks for both a diagnosis AND a rewritten version. Also triggers when the user has already run a stickiness audit and now wants the rewrite executed, or when they hand over a draft plus audience plus goal and say 'just fix it.' Produces message-clinic-output.md containing SITUATION, MESSAGE 1 (original verbatim), DIAGNOSIS (routed through stickiness-audit), MESSAGE 2 (revised draft that preserves the user's tone and brand constraints), and a one-sentence PUNCH LINE explaining the key change and why it works. Delegates targeted fixes to foundation skills (core-message-extractor, curiosity-gap-architect, concrete-language-rewriter, credibility-evidence-selector, emotional-appeal-selector, story-plot-selector, curse-of-knowledge-detector) based on which dimensions scored weak. Preserves voice, brand, and legal constraints the user provides. Also handles the 'already sticky' case — if the draft passes the audit, returns a no-rework verdict with an explanation of why it already works rather than rewriting for the sake of rewriting. Does NOT process multi-message campaigns (one draft per invocation); does NOT replace stickiness-audit for diagnosis-only use; does NOT invent facts or testimonials the user has not supplied."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/message-clinic-runner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [1, 2, 3, 4, 5, 6]
tags: [communication, messaging, rewriting, clinic, workflow, before-after, orchestrator, copywriting, communications-review, sticky]
depends-on:
  - stickiness-audit
  - curse-of-knowledge-detector
  - core-message-extractor
  - concrete-language-rewriter
  - curiosity-gap-architect
  - credibility-evidence-selector
  - emotional-appeal-selector
  - story-plot-selector
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Draft message to rework — pitch, announcement, landing page hero, email, memo, slide text, tweet, or speech excerpt as markdown or pasted text"
    - type: document
      description: "Audience — role, context, and what they care about"
    - type: document
      description: "Goal — what the reader must remember, feel, or do after reading"
    - type: document
      description: "Tone and brand constraints — voice guidelines, legal language, forbidden claims, character limits (optional but strongly recommended)"
  tools-required: [Read, Write]
  tools-optional: [Grep, TodoWrite]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set working environment: the agent operates on short-form prose drafts supplied by the user."
discovery:
  goal: "Produce a ready-to-ship rewritten draft with a full audit trail — SITUATION, MESSAGE 1 (original), DIAGNOSIS, MESSAGE 2 (revised), PUNCH LINE — that preserves the user's voice and brand constraints while fixing the dimensions the SUCCESs audit flagged."
  tasks:
    - "Take a draft and rewrite it end-to-end into a stickier version with per-change rationale"
    - "Run the book's Idea Clinic template on a real user message"
    - "Decide dimension-by-dimension which foundation skill to invoke and assemble the fixes into a single revised draft"
    - "Handle the 'already sticky' case without forcing a rewrite"
  audience:
    roles: [marketer, founder, communicator, product-manager, teacher, technical-writer, fundraiser, internal-comms, copywriter]
    experience: any
  when_to_use:
    triggers:
      - "User pastes a draft and asks for both a diagnosis and a revised version"
      - "User has an audit result and now wants the rewrite executed end-to-end"
      - "User says 'make this stickier', 'rewrite this', 'fix this pitch'"
    prerequisites:
      - skill: stickiness-audit
        why: "The clinic uses the audit as its DIAGNOSIS stage; weak dimensions drive which foundation skills get invoked."
    not_for:
      - "Diagnosis-only use — invoke stickiness-audit directly"
      - "Multi-message campaigns — run the clinic once per draft"
      - "Writing a message from scratch with no draft — use core-message-extractor first, then compose"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
---

# Message Clinic Runner

## When to Use

The user has ONE draft — a pitch, announcement, landing page hero, email, memo, slide, tweet, or speech excerpt — and wants both a diagnosis AND a revised version they can ship. Use this skill when the goal is **end-to-end rework with a full audit trail**, not diagnosis alone.

**Preconditions to verify before starting:**
- The draft exists as text the agent can read.
- The audience is named (even roughly — "mid-market SaaS buyers", "all 400 employees", "first-time $25-$100 donors").
- The goal is stated or can be extracted — what must the reader remember, feel, or do?
- Tone and brand constraints are captured if the user has them. If not, ask ONCE and accept "no explicit constraints, keep my voice."

**The framing restated for the agent:** The Heath brothers' Idea Clinics — inspired by before/after weight-loss photos — follow a fixed five-part template:

1. **THE SITUATION** — 2-3 sentences of context: who is communicating, to whom, and why.
2. **MESSAGE 1** — the draft verbatim, unedited.
3. **DIAGNOSIS** — a principle-by-principle commentary on what is broken, routed through the SUCCESs rubric.
4. **MESSAGE 2** — the revised draft, preserving the user's voice and brand constraints.
5. **PUNCH LINE** — one sentence naming the central change and why the revision works.

The canonical Idea Clinic example, from the book's Introduction, is the CEO who announces "maximize shareholder value" — zero on Simple (no memorable core), zero on Concrete (nothing observable), zero on Emotional (no named person), zero on Stories (pure assertion). The book contrasts it with JFK's "put a man on the moon and return him safely by the end of the decade" — 2/2 on every dimension. Your rewrites aim for the JFK pole.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **The draft:** The actual text — not a summary.
  -> Check prompt for: pasted text, file path, document attachment.
  -> Ask if missing: "Paste the draft you want me to rework, or give me the file path."

- **The audience:** Who the draft is for.
  -> Check prompt for: audience description, persona, reader profile.
  -> Ask if missing: "Who is this for? One sentence: role + context + what they care about."

- **The goal:** What must the reader remember, feel, or do after reading?
  -> Check prompt for: "the ask is…", "I want them to…", "the takeaway is…".
  -> Ask if missing: "If a reader forgets everything except one thing, what must that one thing be? And what do you want them to do next?"

### Observable Context (gather from environment)

- **Tone and brand constraints:** Voice guide, legal language, forbidden claims, character limits.
  -> Look for: `brand.md`, `voice.md`, style guide file, or prior user messages mentioning tone.
  -> If unclear: ask ONCE — "Any tone, brand, or legal constraints I must preserve? Or should I keep your current voice?"

- **Channel and length constraints:** A tweet, a keynote, and an all-hands memo have different rewrite tolerances.
  -> Infer from: file name, draft length, stated character limits.
  -> Default if unclear: keep the revised version within ±20% of the original length.

- **Prior clinic runs or audits:** If a `stickiness-scorecard.md` already exists, reuse it rather than re-auditing.
  -> Look for: `stickiness-scorecard.md` in the working directory.

### Default Assumptions

- **Assumption: voice preservation is ON by default.** Never rewrite in a generic marketing tone. If the draft is casual, the revision is casual. If the draft is clinical, the revision is clinical-but-concrete.
- **Assumption: no invented facts.** The clinic never invents statistics, customer names, testimonials, or credentials the user has not supplied. If a fix requires evidence the user has not given, flag it as `[NEEDS FROM USER: <what>]` in MESSAGE 2.
- **Assumption: one draft per invocation.** If the user pastes three messages, ask which one to clinic first.

### Sufficiency Threshold

- **SUFFICIENT:** Draft + audience + goal + (tone constraints OR explicit "keep my voice").
- **PROCEED WITH DEFAULTS:** Draft + audience + inferred goal. Flag `[assumed goal: X]` in the output.
- **MUST ASK:** No draft, OR audience is "general public" with no narrowing, OR user pastes multiple drafts without indicating which one to rework.

---

## Process

### Step 0: Initialize task tracking
**ACTION:** Create a TodoWrite checklist with entries: "gather inputs", "run stickiness-audit (DIAGNOSIS)", "invoke foundation skills for weak dimensions", "assemble MESSAGE 2", "write PUNCH LINE", "assemble clinic output", "structural self-check".
**WHY:** The clinic has seven phases and the middle one fans out to multiple foundation skills. Without a checklist the agent tends to collapse DIAGNOSIS and MESSAGE 2 into a single vague "improved version" — losing the audit trail that is the clinic's entire differentiator. Tracking enforces the book's before/DIAGNOSIS/after discipline.

### Step 1: Gather inputs and establish the SITUATION
**ACTION:** Ask the user (or infer from prompt) for: draft text, audience, goal, tone/brand constraints. Then write the SITUATION paragraph: 2-3 sentences naming (a) who is communicating, (b) to whom, (c) why it matters, (d) channel. Match the compact voice of the book's Clinics ("Health educators at Ohio State University want to inform the academic community about the risks of sun exposure.").
**WHY:** The SITUATION is the lens the rest of the clinic uses. A rewrite without an explicit situation drifts toward generic "better writing" advice — because without audience and goal, "sticky" collapses into "good prose." The book's Clinics always start here, and for the same reason: stickiness is relative to an audience.

**Save:** SITUATION draft to the working scorecard.

### Step 2: Record MESSAGE 1 verbatim
**ACTION:** Copy the user's original draft unedited into the MESSAGE 1 section. Do not fix typos, do not soften tone, do not "lightly improve" anything. Wrap the draft in a code fence or blockquote so it is visually distinct.
**WHY:** The "before" photo only has value if it is the actual before. Any silent improvement to MESSAGE 1 destroys the clinic's entire credibility contract — the user cannot verify the delta if the baseline was already pre-polished. The book's Clinics reproduce Message 1 verbatim even when it is painful to read.

### Step 3: Run the stickiness audit (DIAGNOSIS stage)
**ACTION:** Invoke the `stickiness-audit` skill on the draft with the same audience and goal. Capture the scorecard: seven 0/1/2 scores (Simple, Unexpected, Concrete, Credible, Emotional, Stories, Curse of Knowledge), the kidney-heist comparison, the Top 3 rewrite targets, and the Handoff Recommendations. If a scorecard already exists in the working directory from a prior audit, read and reuse it rather than re-auditing.

**IF** the audit returns **Sticky** (no 0s, at most one 1, no structural anti-pattern) -> skip to Step 7 (already-sticky branch).
**ELSE** -> proceed to Step 4.

**WHY:** The DIAGNOSIS is not "what do I think is wrong" — it is the structured output of the SUCCESs rubric with quoted evidence. The book's Clinics always diagnose principle-by-principle before rewriting, because a rewrite without a diagnosis produces stylistic variation rather than targeted fixes. Delegating to stickiness-audit guarantees the diagnosis is dimension-labeled, evidence-quoted, and ranked — which is exactly what MESSAGE 2 needs as input.

**Save:** DIAGNOSIS section = condensed scorecard + Top 3 targets + handoff list.

### Step 4: Delegate targeted rewrites to foundation skills
**ACTION:** For each dimension that scored 0 or 1, invoke the matching foundation skill with the draft, the audience, the goal, and the tone constraints. Use the delegation table in [references/rewrite-delegation-playbook.md](references/rewrite-delegation-playbook.md). Collect each skill's output as a "fix fragment" — a targeted replacement, addition, or restructuring move. Do NOT run every foundation skill; run only the ones flagged by the audit's Top 3 plus any dimension that scored 0.

**Order matters.** Run the fixes in this priority:
1. **Simple (core-message-extractor)** — must happen first; every other fix is downstream of the core.
2. **Curse of Knowledge (curse-of-knowledge-detector)** — run second; removes blockers that would otherwise survive other rewrites.
3. **Concrete (concrete-language-rewriter)** — third; grounds the core in sensory language.
4. **Unexpected (curiosity-gap-architect)** — fourth; builds the hook on top of the now-concrete core.
5. **Credible (credibility-evidence-selector)** — fifth; picks the one proof point that best anchors the claim.
6. **Emotional (emotional-appeal-selector)** — sixth; wires the core into an existing reader emotion.
7. **Stories (story-plot-selector)** — seventh; wraps the fixes in a plot if the channel allows it.

**IF** a foundation skill asks for information the user has not supplied (customer name, statistic, testimonial) -> do NOT invent it. Insert `[NEEDS FROM USER: <what>]` as a placeholder in the fix fragment and flag it in the PUNCH LINE.

**WHY:** The order reflects dependency: you cannot concretize an abstract sentence until you know what the core actually is; you cannot build a curiosity gap around a hidden core; you cannot pick the right credibility anchor until the core claim is decided. Running fixes out of order produces fragments that contradict each other. The book's Clinics apply principles in roughly this order for the same reason — Simple first, Stories last.

**Save:** One fix fragment per invoked skill, labeled with the dimension.

### Step 5: Assemble MESSAGE 2
**ACTION:** Produce the revised draft by weaving the fix fragments into a single coherent message. Rules:
- **Preserve the user's voice.** Cadence, register, and brand vocabulary stay. If the original is casual, MESSAGE 2 is casual-but-concrete.
- **Respect stated constraints.** Character limits, legal language, forbidden claims, tone rules. If a fix would violate a constraint, drop the fix and use the second-best option from the foundation skill's output.
- **Keep it within ±20% of original length** unless the user explicitly asks for a different length or the channel demands it.
- **Never introduce facts, customer names, statistics, or testimonials the user did not supply.** Use `[NEEDS FROM USER: <what>]` placeholders.
- **Do not ship a rewrite that scores worse than the original on any dimension.** Re-check mentally: did any of my fixes flatten a strength?

Write MESSAGE 2 in the same format and medium as MESSAGE 1 (if the original was an email, MESSAGE 2 is an email; if a landing page hero, MESSAGE 2 is a hero). Wrap it in the same visual container (code fence or blockquote) for visual symmetry with MESSAGE 1.

**WHY:** MESSAGE 2 is the artifact the user actually ships. Voice preservation is non-negotiable because a rewrite in a generic "sticky" tone is functionally useless — the user cannot send it without re-editing, which defeats the clinic. The ±20% length rule prevents the common failure mode where the rewrite balloons into a 3x-longer paragraph because every SUCCESs fix adds a sentence. The no-invented-facts rule is the clinic's integrity contract: the user's trust in the output depends on knowing that every proof point is one they gave you.

**Save:** MESSAGE 2 to the working scorecard.

### Step 6: Write the PUNCH LINE
**ACTION:** Write a single sentence (two sentences maximum) naming (a) the central change between MESSAGE 1 and MESSAGE 2 and (b) why the revision works. The punch line is a teaching sentence — it should answer "what did I learn from this rework?" in words the user can quote back. Model it on the book's Clinic punch lines: compact, principle-named, and connected back to the SUCCESs framework.

Examples of punch-line shape (paraphrased from the book's Clinics):
- "Message 2 works because it replaces an abstract strategy statement with a single concrete constraint — the Boeing 727 move — which the reader can actually picture."
- "Message 2 wins on the Mother Teresa principle: one named person creates emotional traction that 47,000 statistical beneficiaries destroy."
- "Message 2 opens a curiosity gap in the first sentence rather than answering a question the reader was not yet asking — the Gap Theory fix."

**IF** MESSAGE 2 contains `[NEEDS FROM USER: <what>]` placeholders -> name them in the punch line so the user knows what to fill in before shipping.

**WHY:** The punch line is the clinic's teaching surface. Without it, the user sees a before/after but does not learn the principle — which means they will make the same mistake on the next draft. The book's Clinics end with a punch line because the rework is meant to be a worked example, not a one-off fix. A clinic without a punch line is a haircut; a clinic with a punch line is a lesson.

**Save:** PUNCH LINE to the working scorecard.

### Step 7: Handle the already-sticky branch (early exit)
**ACTION:** If Step 3's audit returned a **Sticky** verdict, do NOT rewrite. Instead, produce a clinic output where:
- SITUATION is written normally.
- MESSAGE 1 is recorded verbatim.
- DIAGNOSIS explicitly states: "Draft passes the audit — no rework needed."
- MESSAGE 2 section says: "(unchanged — MESSAGE 1 is already sticky)" and does NOT duplicate the draft.
- PUNCH LINE explains which two or three dimensions the draft is already winning on, quoting specific phrases from MESSAGE 1 as evidence.

**WHY:** Rewriting for the sake of rewriting is the single worst failure mode for this skill — it erodes user trust and often flattens strengths. The Heaths warn against this directly ("some ideas only need to lose a few pounds; some don't need to lose any"). An honest "this is already good and here's why" output is more valuable than a cosmetic rework that damages a working draft.

### Step 8: Assemble the clinic output file
**ACTION:** Write `message-clinic-output.md` using the template at [references/clinic-template.md](references/clinic-template.md). The file contains exactly these sections in this order:
1. **THE SITUATION** — 2-3 sentences.
2. **MESSAGE 1** — original verbatim, in a visual container.
3. **DIAGNOSIS** — per-dimension scorecard (score + one-line verdict + quoted evidence) from Step 3, plus the Top 3 rewrite targets. This is the condensed audit — not the full `stickiness-scorecard.md`.
4. **MESSAGE 2** — revised draft, in the same visual container as MESSAGE 1 (or "unchanged" if already sticky).
5. **PUNCH LINE** — one sentence (two max), principle-named.
6. **Rationale** — a short bulleted list mapping each change in MESSAGE 2 to the SUCCESs dimension it fixes and the foundation skill that produced the fragment. This is the audit trail.
7. **Constraints preserved** — a one-line statement of which tone/brand/legal constraints the rewrite respected.

**Save:** `message-clinic-output.md` in the user's working directory.

### Step 9: Structural self-check
**ACTION:** Before returning, verify:
- [ ] SITUATION names audience, goal, and channel.
- [ ] MESSAGE 1 is verbatim — no silent edits.
- [ ] DIAGNOSIS is dimension-labeled (all seven axes listed, even if some scored 2) with quoted evidence.
- [ ] MESSAGE 2 is either a rewritten draft in the user's voice OR explicitly marked "unchanged — already sticky."
- [ ] MESSAGE 2 contains no invented facts — any fabricated claim must be a `[NEEDS FROM USER: ...]` placeholder.
- [ ] MESSAGE 2 length is within ±20% of MESSAGE 1 unless explicitly requested otherwise.
- [ ] PUNCH LINE names at least one SUCCESs dimension by name ("Concrete", "Emotional", "Curse of Knowledge", etc.).
- [ ] Rationale section maps each change to a dimension AND a foundation skill.
- [ ] Constraints-preserved line exists and is accurate.
- [ ] No dimension was collapsed — Curse of Knowledge is addressed separately from Simple.

**IF** any check fails -> fix before returning the output.
**WHY:** Each of these checks defends against a specific baseline failure mode (silent polishing, invented testimonials, missing punch line, collapsed Curse axis). Skipping the self-check lets the clinic degrade into "an LLM rewrote your copy" — which is exactly what the skill exists to out-perform.

---

## Inputs

- `draft` — the text to rework (markdown, pasted text, or file path).
- `audience` — one sentence: role + context + what they care about.
- `goal` — what the reader must remember, feel, or do.
- `constraints` — tone, brand, legal, length, channel rules (optional but recommended).
- `prior_scorecard` — path to an existing `stickiness-scorecard.md` if one exists.

## Outputs

A single file, `message-clinic-output.md`, structured as:

```markdown
# Message Clinic — {draft name}

## THE SITUATION
{2-3 sentences: who, to whom, channel, why it matters.}

## MESSAGE 1
> {the original draft, verbatim}

## DIAGNOSIS
| Dimension            | Score | Verdict              | Evidence              |
|----------------------|-------|----------------------|-----------------------|
| Simple               | 0/1/2 | {...}                | "..."                 |
| Unexpected           | 0/1/2 | {...}                | "..."                 |
| Concrete             | 0/1/2 | {...}                | "..."                 |
| Credible             | 0/1/2 | {...}                | "..."                 |
| Emotional            | 0/1/2 | {...}                | "..."                 |
| Stories              | 0/1/2 | {...}                | "..."                 |
| Curse of Knowledge   | 0/1/2 | {...}                | "..."                 |

**Top 3 rewrite targets:** {dimension → fix → effort}

## MESSAGE 2
> {the revised draft, same medium and voice as MESSAGE 1}

## PUNCH LINE
{One sentence (two max) naming the central change and which SUCCESs principle it lands.}

## Rationale
- **{Dimension}** — {what changed} — produced by `{foundation-skill}`
- ...

## Constraints preserved
{One line: voice, brand, legal, length — what the rewrite respected.}
```

---

## Key Principles

- **Preserve voice, always.** A rewrite in generic marketing tone is functionally useless — the user cannot ship it. Cadence, register, and brand vocabulary stay; only the SUCCESs-failing moves change. If the original is clinical, the revision is clinical-but-concrete. If the original is casual, the revision is casual-but-emotional. This is the difference between "a clinic" and "an LLM smoothed my copy."

- **Never invent facts.** The clinic never introduces customer names, statistics, testimonials, or credentials the user has not supplied. Every fix that needs evidence becomes a `[NEEDS FROM USER: <what>]` placeholder. This is the skill's integrity contract — users can only trust the before/after if they know the "after" contains nothing fabricated. A clinic that invents a testimonial is worse than no clinic at all.

- **The diagnosis is delegated, not improvised.** The DIAGNOSIS stage runs `stickiness-audit` — the rubric-based hub skill — rather than guessing. Without a structured audit the rewrite drifts toward stylistic variation, which is the baseline agent failure mode. The audit's Top 3 + handoff list is the work order for Step 4.

- **Fix order follows the dependency graph.** Simple first (nothing else works without a clear core), then Curse of Knowledge (removes blockers), then Concrete, Unexpected, Credible, Emotional, Stories. Running fixes out of order produces fragments that contradict each other — e.g., concretizing a sentence whose core has not yet been decided.

- **The already-sticky case is a legitimate output.** If the draft passes the audit, returning "no rework needed — here's why it already works" is the right answer. The book is explicit: some ideas only need to lose a few pounds; some don't need to lose any. A cosmetic rework that damages a working draft is the worst possible outcome.

- **The punch line is a teaching sentence, not a summary.** It names a SUCCESs principle, quotes the central change, and explains why the revision works in terms the user can apply to the next draft. A clinic without a punch line is a haircut; a clinic with a punch line is a lesson.

- **Voice preservation beats rubric optimization.** If a fix would win a dimension but break the user's voice or brand, drop the fix and use the second-best option. The goal is not a 14/14 scorecard; it is a ship-ready draft. Rubric-chasing at the cost of voice is the "robot-wrote-this" smell.

- **One draft per clinic.** Multi-message campaigns fan out into contradictory fixes. If the user pastes three drafts, run the clinic three times in sequence — not fused into one output.

---

## Examples

**Scenario: The "maximize shareholder value" CEO memo (canonical weak baseline)**

Trigger: User pastes a short all-hands announcement: "Team — as we enter FY26 we will maximize shareholder value through synergies across business units and a best-in-class North Star metric. Our goal is operational excellence." Audience: "all 400 employees across mixed roles, most have never been in strategy meetings." Goal: "get everyone rowing in the same direction on Monday morning." Constraints: "keep my plainspoken voice — I don't use corporate buzzwords in person."

Process: (1) SITUATION: "The CEO is addressing 400 employees across mixed roles in an all-hands memo ahead of FY26 kickoff; the goal is to give everyone a shared direction they can act on Monday morning." (2) MESSAGE 1 captured verbatim. (3) Audit returns: Simple 0/2, Unexpected 0/2, Concrete 0/2, Credible 1/2, Emotional 0/2, Stories 0/2, Curse of Knowledge 0/2. Top 3 = (a) extract a concrete core, (b) replace "North Star metric" with the actual metric and target number, (c) add a "what changes for you on Monday" paragraph. Verdict: Not sticky — structural rework required. (4) Delegation: core-message-extractor → curse-of-knowledge-detector → concrete-language-rewriter → emotional-appeal-selector. Each returns a fix fragment. (5) MESSAGE 2: "Team — this year we want one thing: every customer keeps their service working during our platform migration. We're moving 400 services to the new stack between now and December. For you on Monday: if you own a service on the list below, your sprint changes — talk to your manager. If you don't, nothing changes yet. [NEEDS FROM USER: the actual service-count number and the migration deadline]." (6) PUNCH LINE: "Message 2 works because it replaces an abstract strategy statement ('maximize shareholder value') with one concrete Commander's Intent the reader can act on Monday — the Simple + Concrete combination the book calls the core of stickiness." (7) Rationale lists each change and its source skill. (8) Constraints preserved: "plainspoken voice, no corporate buzzwords — FY26 is the only business term retained."

Output: `message-clinic-output.md` with the above sections. The placeholder flags what the CEO must fill in before shipping.

**Scenario: Nonprofit giving-day email (the Mother Teresa inversion)**

Trigger: User pastes a 120-word email: "Our 2026 impact report shows 14 programs reached 47,000 beneficiaries across sub-Saharan maternal health. Every dollar donated supports our work. Donate today to continue our mission." Audience: "first-time $25-$100 donors, no prior engagement." Goal: "convert to a first gift." Constraints: "keep under 150 words, compliant with UK fundraising regulator — no emotional manipulation or graphic imagery."

Process: (1) SITUATION captured. (2) MESSAGE 1 verbatim. (3) Audit: Credible 2/2 (numbers are testable), Simple 1/2, Emotional 0/2 (Mother Teresa inverted — no named person), Stories 0/2 (no narrative), Unexpected 0/2, Concrete 1/2, Curse 1/2 ("impact report" leaks through). Top 3 = emotional-appeal-selector, story-plot-selector, fix burying-the-lead. (4) Delegation: emotional-appeal-selector returns "lead with one named mother + one specific detail"; story-plot-selector returns a Connection-plot micro-narrative. Both respect the regulator constraint — no graphic imagery, no manipulation. (5) MESSAGE 2: "Last March, Amina walked 11 km to our clinic in Kebri Dehar. She was in her eighth month. The clinic was open because a donor like you had paid for the month's supplies. Your £25 today keeps one clinic open for a day. Donate here. [NEEDS FROM USER: confirmation that Amina is a real case you have permission to cite, or substitute a permitted story]." (6) PUNCH LINE: "Message 2 inverts the Mother Teresa effect — one named mother and one specific walk creates emotional traction that 47,000 aggregate beneficiaries flatten; the regulator constraint is respected because the detail is factual, not graphic." (7) Rationale. (8) Constraints preserved: "under 150 words, no graphic imagery, no manipulation."

Output: `message-clinic-output.md` with placeholder flagging the consent check before shipping.

**Scenario: Already-sticky landing page hero (no rework needed)**

Trigger: User pastes a landing page hero: "Know which of your 400 microservices broke in the last deploy before your customers do." Audience: "backend engineers at mid-size SaaS companies." Goal: "sign up for a 14-day trial." Constraints: "engineering-tone, no hype."

Process: (1) SITUATION captured. (2) MESSAGE 1 verbatim. (3) Audit: Simple 2/2, Unexpected 1/2, Concrete 2/2 ("400 microservices", "last deploy"), Credible 1/2 (reader can verify from memory), Emotional 1/2 (wires into fear of a customer-reported incident), Stories 1/2 (implicit micro-narrative), Curse 2/2. Verdict: Sticky. (4) Early exit — skip rewrite. (5) MESSAGE 2: "(unchanged — already sticky)". (6) PUNCH LINE: "Ship it. The hero is winning on Simple (a single Commander's Intent — catch bad deploys), Concrete (the 400-microservice number the reader can picture), and Curse of Knowledge (zero insider jargon); a rewrite would flatten at least one of those strengths." (7) Rationale: "no changes made; audit verdict and reasoning retained for the author's records." (8) Constraints preserved: "engineering-tone, no hype — already compliant."

Output: `message-clinic-output.md` with an unchanged MESSAGE 2 and an honest punch line explaining why the draft already works.

---

## References

- For the exact markdown template `message-clinic-output.md` must fill in, see [clinic-template.md](references/clinic-template.md)
- For the decision table mapping audit dimensions to foundation skills and the dependency-ordered fix priority, see [rewrite-delegation-playbook.md](references/rewrite-delegation-playbook.md)

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Made to Stick: Why Some Ideas Survive and Others Die by Chip Heath and Dan Heath.

## Related BookForge Skills

This is a Level 2 orchestrator — it delegates diagnosis to the Level 1 hub and targeted rewrites to the Level 0 foundation skills. Install from ClawhHub:

- `clawhub install bookforge-stickiness-audit` — the DIAGNOSIS stage (required)
- `clawhub install bookforge-core-message-extractor` — invoked when Simple scores low
- `clawhub install bookforge-curse-of-knowledge-detector` — invoked when the Curse axis scores low
- `clawhub install bookforge-concrete-language-rewriter` — invoked when Concrete scores low
- `clawhub install bookforge-curiosity-gap-architect` — invoked when Unexpected scores low
- `clawhub install bookforge-credibility-evidence-selector` — invoked when Credible scores low
- `clawhub install bookforge-emotional-appeal-selector` — invoked when Emotional scores low
- `clawhub install bookforge-story-plot-selector` — invoked when Stories scores low

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
