# Rewrite Delegation Playbook

This playbook tells the `message-clinic-runner` WHICH foundation skill to invoke for EACH weak dimension flagged by the stickiness audit, in WHICH order, and with WHAT to pass as input. It is the dispatch logic for Step 4 of the clinic workflow.

The core idea: the clinic does not fix drafts itself — it delegates each dimension-specific fix to the Level 0 foundation skill that owns that dimension, then assembles the fragments into MESSAGE 2 in Step 5.

---

## Delegation table

| Audit dimension          | Invoke this skill              | What to pass in                                                                                         | What you get back                                                                                         |
|--------------------------|--------------------------------|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **Simple** (0 or 1)      | `core-message-extractor`       | Draft + audience + goal + tone constraints                                                              | A single-sentence Commander's Intent to anchor MESSAGE 2 around                                           |
| **Curse of Knowledge** (0 or 1) | `curse-of-knowledge-detector` | Draft + audience profile (what the reader does NOT know)                                              | List of flagged insider terms, acronyms, buried assumptions + rewrite guidance                            |
| **Concrete** (0 or 1)    | `concrete-language-rewriter`   | Draft (or the flagged abstract passages) + audience + the Commander's Intent from core-message-extractor | Side-by-side before/after of each abstract passage with the concretizing technique named                  |
| **Unexpected** (0 or 1)  | `curiosity-gap-architect`      | Draft + audience + core message + channel (email subject? tweet? landing hero?)                         | 3 scored hook variants with pattern-break + curiosity-gap structure                                       |
| **Credible** (0 or 1)    | `credibility-evidence-selector`| Draft's claim(s) + audience skepticism profile + available proof (ONLY what the user supplied)         | Ranked evidence list with the Sinatra-test winner picked; weak chains flagged for removal                 |
| **Emotional** (0 or 1)   | `emotional-appeal-selector`    | Draft + audience + goal + forbidden moves (fear appeals? manipulation?)                                 | Chosen lever (Association / Self-Interest / Identity) + named-person framing plan + forbidden-move list   |
| **Stories** (0 or 1)     | `story-plot-selector`          | Draft + audience + goal + available raw story material the user has supplied                           | Plot type (Challenge / Connection / Creativity) + structured story skeleton using real user-supplied facts |

**Rule:** Pass the user's tone and brand constraints to EVERY foundation skill. A fragment that violates voice is useless downstream — it will be dropped in Step 5 and the dimension will remain broken.

---

## Dependency order

Run the invocations in this order. This is not arbitrary — it reflects the dependency graph between dimensions.

1. **Simple → core-message-extractor** (if flagged)
2. **Curse of Knowledge → curse-of-knowledge-detector** (if flagged)
3. **Concrete → concrete-language-rewriter** (if flagged)
4. **Unexpected → curiosity-gap-architect** (if flagged)
5. **Credible → credibility-evidence-selector** (if flagged)
6. **Emotional → emotional-appeal-selector** (if flagged)
7. **Stories → story-plot-selector** (if flagged)

**Why this order:**

- **Simple must be first.** You cannot concretize, hook, or emotionally anchor a message whose core has not yet been decided. Every downstream fix takes the Commander's Intent as input. Running Concrete before Simple produces vivid language around the wrong idea.
- **Curse of Knowledge is second.** Removing buried insider assumptions is a prerequisite for every other fix — a fragment written on top of jargon-corrupted scaffolding inherits the corruption. Also, the Curse fixes are usually cuts (removing terms), which shrinks the draft before the other skills add new material.
- **Concrete is third.** Now that you have a clear core and no insider jargon, you can ground the core in sensory language. Running Concrete before Curse means you re-concretize passages that will then be cut; wasted work.
- **Unexpected is fourth.** The hook (pattern-break + curiosity gap) is built ON TOP of the concrete core. A hook around an abstract core is a gimmick; a hook around a concrete core is the kidney heist.
- **Credible is fifth.** Once the core, the concrete language, and the hook are in place, you can pick the single best proof point. Picking evidence before the core is decided often produces credibility that points at the wrong claim.
- **Emotional is sixth.** The emotional lever wires the (now-decided, now-concrete) claim into an existing reader emotion. Running Emotional first tends to produce sympathy-begging copy that does not connect to a specific claim.
- **Stories is last.** The story wraps everything in a plot — it is the skin, not the skeleton. A story written before the core, hook, and credibility exist is a story about nothing.

**Skip rules:**

- If a dimension scored 2/2 in the audit — do NOT invoke the foundation skill for it. Preserve the existing strength; running the skill anyway risks flattening it.
- If a dimension scored 1/2 and is NOT in the audit's Top 3 — it is optional. Invoke only if the fix is cheap and does not risk breaking other dimensions.
- If a dimension scored 0/2 — ALWAYS invoke the foundation skill, even if it is not in the Top 3. A 0 is always worth fixing.

---

## Passing data between skills

Each skill runs independently and does not see the other skills' outputs. Pass data forward explicitly:

- **core-message-extractor output (Commander's Intent)** → pass to every downstream invocation as `core_message`.
- **curse-of-knowledge-detector output (flagged terms list)** → pass to concrete-language-rewriter so it does not re-use the flagged terms when concretizing.
- **concrete-language-rewriter output (concrete swaps)** → pass to curiosity-gap-architect so the hook builds on the concrete phrasing.
- **credibility-evidence-selector output (Sinatra-test winner)** → pass to emotional-appeal-selector so the emotional framing points at the same proof.
- **emotional-appeal-selector output (chosen lever + named person)** → pass to story-plot-selector so the plot uses the same person.

If a downstream skill would need a fragment from a skill you did NOT invoke (because that dimension scored 2/2), pass the original draft's wording for that dimension instead.

---

## When NOT to delegate

- **Already-sticky branch.** If the audit returns a **Sticky** verdict in Step 3, do not invoke any foundation skill. Skip to the already-sticky output (Step 7 of the main workflow).
- **Single-dimension request.** If the user only asks for one thing ("just make this more concrete"), do not run the full clinic — invoke the single foundation skill directly. The clinic is for end-to-end rework, not single-axis fixes.
- **User provides a locked version.** If the user says "rewrite only the first sentence — leave the rest alone", honor the lock. Delegate fixes only within the unlocked portion and carry the locked text through MESSAGE 2 unchanged.
- **Constraint violation.** If a foundation skill returns a fragment that violates the user's tone, brand, or legal constraints, drop the fragment and use the skill's second-best option. If no option respects the constraints, leave the dimension unchanged and note it in the Rationale ("Emotional dimension unchanged — no lever respected the no-manipulation constraint").

---

## Fix-fragment format

Each foundation skill should return its fix as a structured fragment the clinic can weave into MESSAGE 2:

```
Dimension: {S | U | C | C | E | S | Curse}
Target in MESSAGE 1: "{quoted passage}"
Replacement or addition: "{the new text}"
Technique named: {e.g., "schema tap", "Sinatra Test", "Connection plot"}
Constraint check: {passes / violates — if violates, use second-best}
Needs from user: {list of [NEEDS FROM USER: <what>] placeholders, or "none"}
```

Step 5 of the clinic workflow assembles these fragments by walking MESSAGE 1 and applying the replacements/additions in-place, preserving voice.
