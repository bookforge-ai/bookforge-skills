---
name: core-message-extractor
description: "Extract the single-sentence core of any message — the one thing that must survive if everything else is lost. Use this skill whenever the user asks 'what's my one sentence?', 'simplify this pitch', 'find the core', 'one-liner for this', 'elevator pitch', 'boil this down', 'what's the headline?', 'TL;DR this', 'what's the one thing?', or has a draft, announcement, pitch, product description, speech, or strategy memo that says too many things at once. Also invoke when the user struggles with 'my message isn't landing', 'I have 30 seconds to explain this', 'we can't agree on messaging', 'nobody remembers our pitch', or wants a Commander's Intent, high-concept pitch, tagline, mission statement, or forced prioritization of candidate points. This is the foundation skill for all sticky messaging — run it BEFORE any unexpected/concrete/credible/emotional/story framing work."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/core-message-extractor
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [1, 13]
tags: [messaging, communication, copywriting, pitching, prioritization, commanders-intent, bookforge]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Draft, idea brief, or raw message the user wants compressed"
    - type: document
      description: "Audience description and communication goal"
  tools-required: [Read, Write]
  tools-optional: [Edit]
  mcps-required: []
  environment: "Operates on short-form prose — pitches, drafts, announcements, briefs, product copy."
discovery:
  goal: "Produce a single-sentence core message that captures the one thing that must survive if everything else is lost."
  tasks:
    - "Distill a verbose draft into one sentence"
    - "Force-rank candidate messaging points and cut to one"
    - "Write a Commander's Intent for a team, project, or launch"
    - "Compress a complex idea into a high-concept pitch ('X for Y')"
    - "Diagnose a 'nothing-sticks' draft as having no core"
  audience:
    roles: [marketer, founder, product-manager, communicator, teacher, manager]
    experience: any
  when_to_use:
    triggers:
      - "User has a draft, pitch, or announcement that says too many things"
      - "User asks for a one-liner, tagline, elevator pitch, or TL;DR"
      - "Team cannot agree on what the message 'really is'"
    prerequisites: []
    not_for:
      - "Emotional framing or story wrapping — use sibling Emotional/Story skills"
      - "Adding sensory detail to an already-focused message — use a Concrete skill"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores: {}
    tested_at: null
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
---

# Core Message Extractor

## When to Use

You have been handed a draft, a brief, or a rambling idea, and the user wants it compressed into a single sentence — the one sentence that must survive if everything else is lost. This is the Commander's Intent: the plain-language statement of end-state that lets a subordinate abandon the written plan and still accomplish the mission.

Run this skill BEFORE any downstream sticky-messaging work (unexpected hooks, concrete sensory detail, credibility anchors, emotional framing, story wrapping). Without a core, those techniques decorate the wrong message.

**Preconditions to verify before starting:**
- You have the draft text (or raw idea). If missing, ask the user to paste it.
- You know who the audience is. If missing, ask: "Who specifically is this for?"
- You know the communication goal — what the audience should *do* or *decide* after reading. If missing, ask: "If one person acts on this message, what do they do?"

**Do NOT use this skill for:**
- Emotional framing (use an Emotional/pathways skill).
- Story structure (use a Story/narrative skill).
- Adding sensory detail (use a Concrete skill) — unless you find the core first, then return.

## Context & Input Gathering

### Required Context (must have — ask if missing)
- **Draft or idea brief:** the raw material being compressed.
  -> Check prompt for: pasted text, attached draft, a document the user references.
  -> Check environment for: `draft.md`, `brief.md`, `pitch.md`, `announcement.md` in the working directory.
  -> If still missing, ask: "Can you paste the current draft (or a bullet list of the points you want to include)?"
- **Audience:** who specifically will read or hear this.
  -> Check prompt for: role, title, segment, familiarity level.
  -> If missing, ask: "Who is the specific audience — a role, not a company?"
- **Goal (what the audience should do or decide):** the behavioral outcome.
  -> Check prompt for: CTA, action verb, decision to be made.
  -> If missing, ask: "If the audience remembers only one thing and acts on it, what do they do?"

### Observable Context (gather from environment)
- **Existing core statements:** prior taglines, mission statements, internal one-liners.
  -> Look for: `core-message.md`, `about.md`, `README.md`, brand docs.
  -> If present: treat as candidates, not constraints.
- **Prior drafts and rejected versions:** useful as negative signal.
  -> Look for: `*-v1.md`, `*-draft*.md`, git history on a message file.

### Default Assumptions
- Medium: short-form text (email, slide headline, landing hero, 30-second pitch). State this assumption if used.
- Tone: neutral-professional unless brand voice docs say otherwise.

### Sufficiency Threshold
- SUFFICIENT: draft + audience + goal are all known.
- PROCEED WITH DEFAULTS: draft + audience known, goal inferable from draft content (state the inference explicitly and ask the user to confirm in the output).
- MUST ASK: draft text missing, OR audience completely unspecified.

## Process

### Step 1: Inventory the Candidate Points
**ACTION:** Read the draft. List every distinct message point as a bullet — one claim, benefit, feature, fact, or call-to-action per bullet. Do not edit, merge, or rank yet. Write this as `core-message.md` under a `## Candidate Points` heading.

**WHY:** You cannot force-prioritize what you have not enumerated. Drafts hide their own over-stuffing — a single paragraph can contain five distinct points fused by connective tissue. Making them visible as a flat list is the move that enables ranking. Skipping this step and jumping to "what's the core?" usually yields the *most emotionally loaded* point, not the most important one.

**Output artifact:** `core-message.md` with a `Candidate Points` section listing 3-15 bullets.

### Step 2: Apply Forced Prioritization (The "If You Say Three Things, You Say Nothing" Rule)
**ACTION:** For each candidate point, perform the Removal Test: imagine the point is deleted and ask, "Can the message still achieve its goal for this audience?" If yes -> mark as CUT. If no -> mark as KEEP. When multiple points survive, rank them and force a single #1. Write results as a `## Ranked Candidates` section with KEEP/CUT markers and rationale.

**WHY:** Forced prioritization is uncomfortable because every point feels important to the author — that is the Curse of Knowledge talking. The rule from Carville's 1992 Clinton war room applies: three priorities posted on the wall ("Change vs. more of the same / The economy, stupid / Don't forget health care") with Carville's rule "if you say three things, you don't say anything." Audiences remember the #1 and lose everything below it. If you refuse to rank, the audience will rank for you — badly, and probably on whatever sounded most familiar, not most important.

**IF** two points tie for #1 -> ask the user: "Which of these would you rather your audience remember in six months?" Force the choice.
**ELSE** -> proceed with the clear #1.

**Anti-pattern to flag:** *burying the lead* — the #1 point appears in paragraph 3 of the draft instead of paragraph 1. Inverted-pyramid journalism exists because readers stop reading; the most important fact must come first.

### Step 3: Draft the Commander's Intent (First Pass)
**ACTION:** Write the #1 point as a single plain-language sentence describing the end state the audience should reach. Format: plain English, no jargon, no internal acronyms, no hedging ("might," "could," "in some cases"). State it as if briefing someone who will execute on it after you leave the room. Write it as a `## Commander's Intent (draft)` section.

**WHY:** The US Army adopted Commander's Intent because elaborate plans "don't survive contact with the enemy" — the plan decays the moment reality intervenes. A single end-state sentence lets subordinates improvise when the written plan breaks. The same is true for messages: your audience will not read every word, will forget most of what they read, and will paraphrase what remains. The sentence you write here is the paraphrase you are willing to let survive.

**Anti-patterns to check:**
- Abstract adjectives ("world-class," "innovative," "best-in-class") — these fail the Boeing 727 test (see Step 4).
- Metrics without subject ("grow 10%") — who grows, toward what end?
- Process descriptions ("we use AI to...") — the process is not the end state.

### Step 4: Run the Three Tests
**ACTION:** Test the draft Commander's Intent against three named tests. If any test fails, revise and re-test.

**Test A — The Delegation Test (Southwest Test):**
Could a new hire use this sentence alone to make a contested trade-off decision without asking a manager? Herb Kelleher's 30-second orientation at Southwest was "We are THE low-fare airline." When a marketer proposed adding a light entree on a flight, Kelleher could answer without a meeting: would a light entree help Southwest be THE low-fare airline? No. Cut. "Maximize shareholder value" fails this test; "THE low-fare airline" passes.

**Test B — The Outsider-Judgeable Test (Kennedy Test):**
Could an outsider tell in five years whether you succeeded? JFK's 1961 goal — "put a man on the moon and return him safely to Earth by the end of the decade" — is pass/fail judgeable by anyone. A hypothetical modern rewrite — "become the leading space-faring nation through teamwork and strategic innovation" — is un-judgeable. If your sentence cannot be falsified, it is not a core message; it is corporate atmosphere.

**Test C — The Constraint Test (Boeing 727 Test):**
Does the sentence contain measurable constraints that could coordinate work across teams without meetings? Boeing's 1960s design goal for the 727 was "seat 131 passengers, fly nonstop Miami-NYC, land on La Guardia Runway 4-22" — the runway was under a mile long, impossible for then-current jets. Thousands of engineers self-coordinated against that sentence. Compare: "best passenger plane in the world." Constraints coordinate; adjectives don't.

**WHY:** Each test catches a different failure mode. The Delegation Test catches messages that are too abstract to guide action. The Outsider-Judgeable Test catches messages that cannot be verified (and therefore cannot be trusted or tracked). The Constraint Test catches adjective-stuffed corporate voice that no cross-functional team can align on. A sentence that passes all three is a Commander's Intent; one that passes fewer needs revision.

**IF** the sentence fails any test -> return to Step 3 and revise with the failed test's corrective in mind.
**ELSE** -> proceed to Step 5.

### Step 5: Compact the Core Using One of Three Packing Techniques
**ACTION:** Choose ONE of three named techniques to compact the core further. Apply it. Write the result as a `## Compacted Core` section.

Selection rule:
- **IF** the audience shares a clear existing mental model with you -> use Technique 1.
- **ELSE IF** you can borrow a widely known reference point -> use Technique 2.
- **ELSE IF** the message must generate many downstream decisions over time -> use Technique 3.
- **ELSE** -> keep the Step 4 sentence unchanged.

**Technique 1 — Tap Existing Schema:**
Describe the new thing in terms the audience already has. The classic example: explaining a pomelo as "a grapefruit-like citrus" — one phrase, the audience's existing "grapefruit" schema does the heavy lifting. Use when audience familiarity with an adjacent concept is high.

**Technique 2 — High-Concept Pitch:**
Hollywood greenlights $100M films on one-sentence "known-movie + twist" pitches. *Speed* = "Die Hard on a bus." *Alien* = "Jaws on a spaceship." *13 Going on 30* = "Big for girls." Formula: `[Famous reference] + [specific twist]` or `X for Y` / `X but Z`. Use when a widely-known reference is available and your twist is clean.

**Technique 3 — Generative Analogy:**
Pick an analogy that keeps producing new decisions. Disney's "cast members" (instead of "employees") generates uniform rules, break vocabulary ("backstage"), and audition norms — all without a policy manual. Use when the core must propagate decisions across many future unknown situations.

**WHY:** The Step 4 sentence is defensible but may still be long or abstract. These three techniques compact further by offloading semantic work onto the audience's existing brain — schema-tapping reuses their concepts, high-concept reuses their media memory, generative analogy reuses their inferential machinery. Compaction is not decoration; it is how you fit the same meaning into fewer tokens of audience attention.

### Step 6: Write the Output Artifact
**ACTION:** Assemble the final `core-message.md` with the following sections, in order:

```
# Core Message

## The One Sentence
<final compacted core message — one sentence>

## Why This Is The Core (Justification)
- Audience: <who>
- Goal: <what they should do or decide>
- Passed Delegation Test: <how>
- Passed Outsider-Judgeable Test: <how>
- Passed Constraint Test: <how>
- Packing technique used: <Schema | High-Concept | Generative Analogy | None>

## Cut List (what was removed and why)
- <cut point 1> — <one-line rationale>
- <cut point 2> — <one-line rationale>
...

## Assumptions
- <any inferred audience/goal/medium assumption the user should confirm>
```

**WHY:** The cut list is as important as the kept sentence. Users resist cuts; seeing the cut list lets them challenge specific removals rather than the whole compression. The three-test justification converts "the agent picked this" into "the sentence passed three named, checkable criteria" — which is what makes the output defensible in a team meeting.

## Inputs

- The raw draft text (or a bullet list of candidate points).
- The target audience (role, not company).
- The communication goal (what the audience should do or decide).
- Optional: medium constraints (character limit, time limit), brand tone constraints.

## Outputs

- `core-message.md` — the artifact defined in Step 6, containing:
  - One final sentence (the core).
  - A justification block naming the three tests it passed.
  - A cut list of removed points with rationale.
  - An assumptions block for anything inferred.

## Key Principles

- **If you say three things, you say nothing.** — Carville's war-room rule. Audiences remember the #1 and lose everything below it. Ranking is not optional; the only question is whether you rank or your audience ranks for you.
- **Commander's Intent is a survival sentence, not a summary.** — The sentence must still be useful after the written plan collapses. Summaries preserve content; Commander's Intent preserves end state. These are different outputs.
- **Constraints coordinate; adjectives don't.** — "Best" and "world-class" do not tell a cross-functional team what to build. "Land on a runway under a mile long" does. When in doubt between an adjective and a measurable constraint, take the constraint.
- **Compaction offloads work onto the audience's existing brain.** — Schema-tapping, high-concept pitches, and generative analogies are not literary flourishes; they are compression techniques that reuse the audience's prior knowledge so you do not have to carry it in your token budget.
- **The Curse of Knowledge hides the core from the author.** — The author knows everything and finds it all important. Forced prioritization is painful precisely because the author has already mentally integrated the full message. If the Removal Test feels easy, you probably did it wrong.

## Examples

**Scenario: Product launch announcement, too many features**
Trigger: User pastes a 6-paragraph launch email listing 8 features and says "help me find the core."
Process: (1) Inventory produces 8 candidate points. (2) Removal Test cuts 5 feature points that don't change the purchase decision; 3 survive. (3) Forced rank picks one: "the app now works offline." (4) First-pass draft: "our app now works offline." (5) Delegation Test: could a support rep prioritize roadmap bugs from this? Yes — "does this make offline better?" Passes. Outsider Test: Can you verify offline works? Yes. Constraint Test: measurable. Passes all three. (6) High-concept packing: "Notion that works on a plane." Final core.
Output: `core-message.md` with one sentence ("Notion that works on a plane"), justification block, cut list of 7 features that got demoted to "feature table in the appendix."

**Scenario: Internal strategy memo, nobody remembers it**
Trigger: Founder says "we sent a 4-page strategy memo and a week later my leads are each describing a different strategy."
Process: (1) Inventory of the memo finds 11 distinct claims, including "focus on enterprise," "ship faster," "improve onboarding," "raise ARPU." (2) Removal Test — "focus on enterprise" is the only point that changes every downstream decision; the rest are second-order. (3) First-pass: "we are moving upmarket to enterprise customers." (4) Delegation Test: can a PM decide between two backlog items with just this sentence? Yes — "which serves a 5000-seat customer better?" Passes. (5) Generative analogy chosen (decisions will propagate over a year): "We are the Salesforce of X, not the Notion of X." Final core.
Output: `core-message.md` with the one sentence, tests passed, cut list (10 demoted points), and an assumption flag: "Assuming 'enterprise' = 1000+ seats — please confirm."

**Scenario: Government mission statement audit**
Trigger: User shares "Our mission is to empower citizens through innovative, data-driven, inclusive, transparent services."
Process: (1) Inventory — 5 adjectives, zero end state. (2) Removal Test — you can remove any one adjective and the sentence has the same meaning (or the same meaninglessness), which means none of them are load-bearing. (3) Ask user: "What is the one outcome a citizen should get?" User answers: "Renew any permit in under 10 minutes online, on any device." (4) This passes all three tests directly — Southwest-style delegation ("does this help renew faster?"), Kennedy-style outsider-judgeable ("10 minutes, measurable"), Boeing-style constraint ("any device"). No packing technique needed. (5) Final core: "Renew any permit in under 10 minutes, on any device."
Output: `core-message.md` with the JFK-style final sentence, justification, and a cut list explicitly naming the original 5 adjectives as the removed material.

## References

- For the long-form breakdown of the three packing techniques with worked examples, see [packing-techniques.md](references/packing-techniques.md)
- For the four-question forced-prioritization worksheet, see [forced-prioritization-worksheet.md](references/forced-prioritization-worksheet.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Made to Stick: Why Some Ideas Survive and Others Die* by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone (a Level 0 foundation for the Made to Stick skill set). It is the prerequisite for all sibling sticky-messaging skills — run this first, then layer Unexpected, Concrete, Credible, Emotional, and Story techniques on top of the extracted core.

Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
