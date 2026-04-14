# SUCCESs Dimension Rubric — 0/1/2 per dimension

This is the scoring rubric for the `stickiness-audit` skill. Every dimension uses a **0/1/2** scale. The book is explicit: *"It's a checklist, not an equation."* Do NOT sum the scores. Report per-dimension verdicts only.

Each dimension below gives: the core question, the 0/1/2 criteria, the canonical kidney-heist benchmark (the book's gold-standard 2/2 example), and the canonical weak example (usually the Introduction's "maximize shareholder value" CEO memo).

---

## S — Simple

**Core question:** Does the draft have one identifiable core, expressed with proverb-like compactness?

**Two sub-tests:**
1. **Core test** — Can you state what the draft is *really* about in one sentence that the author would agree with?
2. **Compact test** — Is that sentence short, memorable, and pre-loaded with meaning (like a proverb or Commander's Intent)?

**0** — No identifiable core. The draft makes multiple competing claims, or the core is buried under context, or the "core" is a goal the audience already holds ("we will maximize value"). Fails both sub-tests.

**1** — A core exists but is either buried (reader must read past paragraph 2 to find it) or abstract (reader can recite it but cannot act on it).

**2** — The core is clear, compact, and actionable in a single sentence the reader can repeat.

**Kidney heist = 2.** One core image: "drugged traveler wakes up in bathtub of ice missing a kidney, call 911." The core is the whole story.

**"Maximize shareholder value" = 0.** No core the reader can act on differently tomorrow.

**Handoff when 0 or 1:** `core-message-extractor`.

---

## U — Unexpected

**Core question:** Does the draft break a reader schema and open a curiosity gap?

**Two sub-tests:**
1. **Pattern break** — Does the opening surprise the reader relative to what their mental model predicted?
2. **Curiosity gap** — Does the draft open a question the reader now *wants* answered?

**0** — Every sentence is something the reader would pre-agree with. Common-sense sedation ("customer service is important", "we value our partners").

**1** — Some pattern break exists but it is buried, or the curiosity gap is opened and then not closed (teasing without payoff).

**2** — Opens with a schema violation and either closes the gap satisfyingly or sustains curiosity for a defined payoff.

**Kidney heist = 2.** "Woke up in a bathtub of ice" violates every traveler-safety schema the reader holds.

**"Maximize shareholder value" = 0.** Zero schema violation.

**Handoff when 0 or 1:** `curiosity-gap-architect`.

---

## C — Concrete

**Core question:** Does the draft use sensory, observable language instead of abstractions?

**Two sub-tests:**
1. **Noun audit** — What fraction of the draft's nouns are abstract (strategy, synergy, value, solution, impact) vs sensory/observable (bathtub, 131 passengers, Jared's pants)?
2. **Boeing 727 test** — If you replaced the abstract phrases with measurable constraints, would meaning be lost or gained? If gained, the draft is under-concrete.

**0** — Abstract-only. No sensory nouns, no measurable constraints, no observable behaviors. The Boeing 727 test gains meaning when replacements are applied.

**1** — Some concrete details exist but are surrounded by abstraction. The draft reads concrete in patches but abstract overall.

**2** — Every claim is anchored to a sensory or observable specific. The reader can visualize what the draft is talking about.

**Kidney heist = 2.** Ice, bathtub, phone, note, stitches — every noun is sensory.

**"Maximize shareholder value" = 0.** Not a single sensory noun. Boeing 727 test: "grow revenue 20% in FY26 by winning back 10 lapsed accounts" gains meaning vs the original.

**Handoff when 0 or 1:** `concrete-language-rewriter`.

---

## C — Credible

**Core question:** Does the message vouch for itself without relying on unverifiable adjectives?

**Credibility moves the book catalogues (any ONE of these done well is enough for 2/2):**
- **External authority** — relevant expert or institution.
- **Anti-authority** — a credible first-person skeptic or ex-insider (the ex-smoker argument).
- **Internal vivid details** — specificity that signals first-hand knowledge (the Hyundai cancer-cluster description).
- **Statistics with a human anchor** — a number wired to something relatable (Nukes Stanford distance).
- **Sinatra test** — one overwhelming example that alone makes the case ("if you can make it there…"). Fort Knox security contract, Safexpress + Harry Potter.
- **Testable credentials** — a claim the reader can personally verify ("Where's the beef?" — you can weigh the patty yourself).

**0** — Relies on unverifiable adjectives: "world-class", "leading", "proven", "best-in-class". Reader has no way to check any claim.

**1** — Uses one credibility move but weakly (generic stat without human anchor; authority quote without domain match).

**2** — Uses at least one credibility move done well. The reader's response is "yes, that would convince me even if no one said it was true."

**Kidney heist = 2.** Friend-of-a-friend detail + specific operative timing + the "call 911" procedural detail all read like first-hand knowledge.

**"Maximize shareholder value" = 0-1.** Usually leans on adjectives or on a single unanchored statistic.

**Handoff when 0 or 1:** `credibility-evidence-selector`.

---

## E — Emotional

**Core question:** Does the draft make the reader *care*, usually by routing through one specific person or an identity the reader holds?

**Three sub-tests:**
1. **Who specifically?** Is there one identifiable person, not a statistical many? (Rokia, not "Africa's hungry".)
2. **Which identity?** Does the draft connect to an identity the reader already holds? ("Don't mess with Texas" wires into Texas pride.)
3. **Which associations?** Does the draft borrow emotion from associations the reader actually values?

**0** — No named person, no identity hook, emotion manufactured through adjective stacking ("devastating", "heart-wrenching", "unprecedented").

**1** — One of the three sub-tests passes; the other two don't. Emotion is present but thin.

**2** — At least two sub-tests pass. The reader recognizes themselves or someone they care about in the draft.

**Kidney heist = 2.** The traveler is "you" — identity hook is direct; the bathtub is visceral fear wired into body-safety identity.

**"Maximize shareholder value" = 0.** Zero identity hook. Shareholder value is an abstraction most employees cannot identify with.

**Handoff when 0 or 1:** `emotional-appeal-selector`.

---

## S — Stories

**Core question:** Does the draft tell a story, or does it only assert claims?

**A story has:** subject acting (actor + verb), a complication or challenge, and a resolution or lesson.

**Plot types to detect:**
- **Challenge plot** — underdog overcomes obstacle (Jared/Subway).
- **Connection plot** — bridge across a gap between people (Good Samaritan).
- **Creativity plot** — insight solves a puzzle (Apollo 13 CO2 filter).

**0** — No narrative. Bullets, claims, or assertions only. Reader is told what to think, not shown what happened.

**1** — A micro-narrative is present (one sentence of "user did X then Y") but not developed; the reader cannot mentally rehearse the action.

**2** — A full story with identifiable plot type. The reader could summarize what happened to whom and what they should take away.

**Kidney heist = 2.** Complete Challenge-plus-Connection plot: traveler meets stranger, wakes up victimized, must call 911. Full arc.

**"Maximize shareholder value" = 0.** Zero narrative.

**Handoff when 0 or 1:** `story-plot-selector`.

---

## Villain — Curse of Knowledge

**Core question:** Could a non-expert in the audience parse this cold?

**The tapper/listener heuristic:** The author "knows what they mean" — the question is whether the reader can hear it. Re-read the draft from the audience's POV and list every term, acronym, framework reference, named internal tool, or buried assumption that would force a non-expert to pause.

**0** — Visibly corrupted by expertise. Heavy jargon, internal tool names, buried assumptions on every paragraph. A non-expert stops reading in the first 20 seconds.

**1** — Some insider residue. A handful of terms assume reader context; the bulk of the draft is parseable but the residue is enough to lose part of the audience.

**2** — A non-expert could parse it cold. Any domain term is defined on first use or swapped for a common-language equivalent.

**Kidney heist = 2.** Zero jargon. Every noun is a shared-schema household object.

**"Maximize shareholder value" = 0.** Every key phrase assumes MBA-level schema.

**Handoff when 0 or 1:** `curse-of-knowledge-detector` (for deeper per-passage diagnosis) and/or `sticky-message-antipattern-detector` (for related anti-patterns: burying-the-lead, analysis-by-jargon, common-sense-sedation).

---

## Scoring discipline reminders

- **Quote evidence for every score.** A score without a quoted passage is an opinion, not an audit.
- **Do not sum the scores.** The rubric is a checklist, not an equation.
- **Score Curse of Knowledge separately from Simple.** A clear core can still be Curse-corrupted.
- **When uncertain between two scores, pick the lower.** The audit's job is to surface gaps, not to flatter the draft.
- **A single 2/2 dimension does not redeem a 0/2 elsewhere.** Report the full picture.
