# Jargon Detection Playbook

Detailed guidance for Pass A (Unexplained Jargon, Acronyms, and Named Frameworks). Use alongside the main SKILL.md Process → Step 2.

## What counts as jargon for this skill

A term is "jargon" relative to a listener baseline if ANY of these are true:

1. **Lexical opacity.** The reader cannot reasonably parse the term from its parts (e.g., `blast radius`, `eventual consistency`, `BATNA`).
2. **Semantic drift.** The term is a common English word used in a specialist sense the reader does not hold (e.g., `commit` for code, `surface` as a verb meaning "reveal", `ship` for release).
3. **Acronym opacity.** The reader may know ONE expansion but not YOURS (e.g., `CDP` = Customer Data Platform vs Continuous Delivery Pipeline vs Clean Development Mechanism).
4. **Named-framework shorthand.** The draft references a framework by name (`SUCCESs framework`, `Sinatra Test`, `STAR format`, `RICE scoring`) without a one-line gloss.
5. **Proper-noun opacity.** References to internal projects, tools, teams, or people the reader does not work with (`the Apollo migration`, `the Foundry team`, `what Sarah said last quarter`).
6. **Borrowed metaphor.** A metaphor taken from a sub-field the reader does not live in (`the chess strategy`, `the orchestration layer`, `the spine of the product`).

## Fast-scan heuristics

When auditing a draft, apply these in order. Each is cheap and catches a distinct failure mode.

### Heuristic 1: Capital-letter density
Count capitalized nouns per 100 words. Above ~6 per 100 is a strong signal of named-framework / proper-noun overload.

### Heuristic 2: Acronym expand-on-first-use test
For every acronym, check: is it expanded on first use in the draft? If no, flag. If yes, is the expansion itself parseable to the listener baseline? (Expanding `API` to `Application Programming Interface` is not parseable to a non-engineer — you need one more hop.)

### Heuristic 3: The "pause test"
Read each sentence aloud. If you have to pause to decide how to pronounce a term, the reader's eye will stutter there too. Flag it.

### Heuristic 4: The "swap test"
For each suspect term, mentally substitute a generic placeholder (`[thing]`, `[process]`). If the sentence still makes sense to the listener, the term was load-bearing jargon and needs a gloss. If the sentence loses nothing, the term was decorative and should be cut.

## Rewrite options (in order of preference)

For each flagged term, offer one of these four fixes. Prefer the earliest option that preserves meaning.

1. **Remove.** The term is decorative. Cut it.
2. **Substitute.** Replace with a common-language equivalent. (`leverage` -> `use`, `bandwidth` -> `time`, `surface` -> `show`.)
3. **Gloss inline.** Keep the term but add a short parenthetical definition on first use. (`We use feature flags (on/off switches that let us turn a new feature on for some users without redeploying)`.)
4. **Gloss in a footnote or sidebar.** Use only for terms the reader will see repeatedly and should learn.

Only keep a term unchanged if the listener baseline explicitly shows the reader knows it.

## Worked examples

### Example 1 — SaaS product announcement, audience = business buyers

Draft: "We are GA on the new idempotent retry handler with exponential backoff."

Flags:
- `GA` — acronym, not expanded. Substitute: "generally available" or just "launched".
- `idempotent` — lexical opacity for business buyers. Substitute: "safe-to-retry".
- `retry handler` — borrowed technical metaphor. Substitute: "automatic retry system".
- `exponential backoff` — named technique. Remove (buyers don't need the algorithm) or gloss: "waits longer between each retry".

Rewrite: "We launched a safe-to-retry system that automatically tries failed requests again with growing wait times between attempts."

### Example 2 — Internal HR memo, audience = all employees

Draft: "Per our new L&D OKR, all ICs should complete the DE&I module by EOQ."

Flags: `L&D`, `OKR`, `ICs`, `DE&I`, `EOQ`. All acronyms, none expanded, reader is "all employees" including facilities and operations staff who do not live in HR shorthand.

Rewrite: "Everyone except managers (we call these 'individual contributors' or ICs) should finish the new diversity, equity, and inclusion training by the end of September."

### Example 3 — Academic grant abstract, audience = program officers from another field

Draft: "We propose a mixed-methods investigation of non-cognitive skill formation using IRT-scaled assessments."

Flags: `mixed-methods` (known in some social sciences, unknown in STEM program offices), `non-cognitive skill formation` (opaque compound), `IRT-scaled` (named technique).

Rewrite options: define each on first use, OR reframe the abstract in plain language and move the technical terms to the methods section.

## Anti-patterns the playbook catches that a generic grammar pass misses

- **"Consultant stack" sentences.** Chains of four+ abstract business nouns: `strategic alignment`, `value creation`, `core competency`, `operational excellence`. Each term is technically English, but together they are pure tapping.
- **Hollow verbs.** `Leverage`, `enable`, `drive`, `facilitate`, `orchestrate`. These verbs carry no sensory information. Flag them as Pass B (abstraction) but note them in Pass A if they let a named framework hide.
- **Framework-name inflation.** Using `SUCCESs framework` in a draft for an audience that has not read the book is a dead giveaway. Same for `BATNA`, `NPS`, `PMF`.
