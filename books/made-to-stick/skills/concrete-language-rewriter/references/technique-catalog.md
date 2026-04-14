# Technique Catalog — Concrete Language Rewriter

Expanded reference for the three concrete-rewrite techniques plus the behavior-level swap. Each entry includes the mechanic, worked examples from *Made to Stick*, adaptation patterns, and failure modes.

---

## Technique 1: Schema Tap

**Mechanic.** Find one thing the audience already owns in memory that shares the most critical feature of the abstract idea, then describe the new idea as `{familiar thing} + {one delta}`. The audience inherits every existing hook of the familiar thing for free.

**Why it works.** Memory is a network. A brand-new abstraction with zero connections to the existing network decays fast; a new node connected to a well-known node gets pulled along every time the known node is activated. The Velcro theory of memory: more hooks to existing knowledge = stickier retention.

**Template.** `{new thing} is like {familiar thing}, except {one delta}.`

**Worked example — pomelo.** Instead of "a large citrus fruit native to Southeast Asia, pale yellow to pink flesh, thick rind, mild sweet flavor," say: "a pomelo is a grapefruit crossed with a football." Two schemas the audience already owns (grapefruit: citrus taste, segmented flesh; football: size, oval shape) convey category, size, shape, and texture in one sentence.

**Worked example — Jane Elliott blue-eyes/brown-eyes exercise.** To teach the abstract concept of *discrimination* to third-graders who had never experienced it, Elliott did not lecture. She split the class by eye color, gave blue-eyed children privileges and brown-eyed children restrictions, then flipped the arrangement the next day. Students recalled the lesson vividly 20 years later. The abstract concept inherited the concrete sensory memory of being favored or shunned. (This is a schema tap at the classroom-experience level — the simulation *becomes* the audience's new schema.)

**Adaptation patterns.**
- Physical product descriptions -> compare to an existing product with one visible delta.
- Org concepts (e.g., "squad", "guild") -> compare to a non-work group the reader already belongs to.
- Technical processes -> compare to a domestic or mechanical process the reader has done themselves.

**Failure modes.**
- The "familiar thing" is only familiar to the writer, not the audience.
- The delta is several things at once — the reader cannot tell which feature matters.
- The schema is too close to the new thing, so there is no actual delta to learn ("it is like email, but for messages").

---

## Technique 2: High-Concept Pitch

**Mechanic.** Position a new idea as the intersection of two things the audience already understands. Both reference points must be rich enough that naming them loads their entire context into the reader's head.

**Why it works.** A new concept takes seconds to positioning-test if both reference points are already loaded. This is why Hollywood green-lights movies on a one-line pitch: the producer's mental model of "Die Hard" (action-hero hostage, ticking-clock stakes, confined space) plus "on a bus" (single location, constant motion) instantly builds the movie concept for Speed. No further explanation needed.

**Templates.**
- `{A} meets {B}`
- `{A} for {new audience or new domain}`
- `The {A} of {new domain}`
- `{A}, but {B}`
- `It is like {A}, except {B}`

**Worked examples.**
- *Speed* = "Die Hard on a bus" — action thriller in a confined moving vehicle.
- Airbnb early pitch = "eBay for space" — peer-to-peer marketplace, but for rooms.
- Uber = "push a button, get a ride" — not a pitch per se, but a high-concept description by action.

**Adaptation patterns for product marketing.**
- `{Known product} for {underserved segment}` — "Slack for construction crews"
- `{Consumer behavior} for {enterprise use case}` — "Tinder for warehouse shift swapping"
- `{A} without {pain of A}` — "Datadog without the enterprise contract"

**Failure modes.**
- One or both reference points are known only to the writer ("It is Substack for Roon users").
- The combination captures a *vibe* but not the actual job to be done.
- Used for a situation that needs generative steering, not a one-shot pitch — the analogy does not carry further into decisions.

---

## Technique 3: Generative Analogy

**Mechanic.** Choose a source frame whose internal vocabulary, roles, and daily actions will keep re-applying to the target domain to generate new decisions long after the analogy is stated. The analogy is not a description — it is an operating system that runs in the audience's head for months.

**Why it works.** A generative analogy preloads an entire decision framework. An employee who is told "you are a cast member on a stage" inherits rules about costumes, audience, breaks, and performance that the handbook could never enumerate. The analogy does the work of policy documents because humans are very good at transferring rules between analogous domains.

**Worked example — Disney cast members.** Disney reframed the theme park as a stage production. Employees -> "cast members"; customers -> "guests"; uniforms -> "costumes"; public areas -> "onstage"; staff areas -> "backstage". The frame generates decisions: you stay in character while onstage, you do not eat lunch in costume in the guest area, you treat guests as an audience not a transaction counterparty. None of these rules had to be written; the analogy generates them.

**Worked example — Kris & Sandy accounting case.** Instead of teaching accounting concepts with disconnected textbook problems, one instructor anchored an entire semester's worth of abstract accounting topics (leasing, working capital, profitability vs cash flow) around a single evolving fictional business: Kris and Sandy's SNO device company. Every lesson extended the same story. The characters and prior decisions carried context that disconnected examples could not, and the class retained abstract principles because they were always attached to one concrete, growing business.

**Worked example — Aesop's Fox and the Grapes.** A 2,500-year-old story encoding the psychological principle of rationalization. The one-scene parable is generative: "sour grapes" now serves as a two-word frame the audience applies to new situations they encounter (a person dismissing what they cannot have). The frame keeps producing interpretations long after the story is told.

**Adaptation patterns.**
- Pick a source frame with rich internal vocabulary: theater, kitchen, cockpit, newsroom, baseball team, emergency room, orchestra.
- List 3–5 daily objects/actions from the current domain that the frame will rename.
- Test: does the frame generate at least one new behavior you had not written into policy?

**Failure modes.**
- The source frame is picked for style, not for the behaviors it generates.
- The analogy renames things but does not actually change any behavior (cosmetic relabeling).
- Fewer than 3 daily terms fit the frame — the analogy peters out.
- The generated behaviors are the wrong ones (the analogy pulls users toward outcomes you did not intend).

---

## Technique 4 (out of the three, but essential): Behavior-Level Swap

**Mechanic.** When the flagged passage is a *goal* or *strategy* rather than an explanation, do not apply an analogy — replace quality adjectives with measurable constraints or named behaviors.

**Why it works.** Adjectives do not coordinate action. A 500-person engineering org cannot self-organize around "the best user experience", but it can self-organize around "the page loads in under 200ms on a 3G connection." Constraints are shareable across teams that never meet; adjectives are not.

**Worked example — Boeing 727.** Boeing's 1960s design brief for the 727 was not "build the best passenger plane." It was: "Seat 131 passengers, fly nonstop from Miami to New York, and land on La Guardia Runway 4-22." That runway was under a mile — impossible for then-current jets. Thousands of engineers across dozens of specialties self-coordinated from that single constraint. The runway defined the airframe.

**Transforms.**
- `best` -> specific measurable threshold (`p95 < 200ms`, `bounce rate < 30%`)
- `delightful` -> observable user action (`new users publish their first post without opening the help docs`)
- `aligned` -> specific verbal behavior (`every PM writes the same one-sentence answer to "what are we building this quarter"`)
- `empower` -> specific unblocked action (`every support agent can issue refunds up to $500 without approval`)
- `world-class` -> benchmark against a named competitor's named metric

**Failure modes.**
- Swapping an adjective for a number that is not actually measurable day-to-day.
- Choosing a metric that is measurable but not the metric that matters (Goodhart's law).
- Over-constraining — leaving no room for the creativity the goal was trying to invite.

---

## When to use each technique

| Situation | Technique |
|---|---|
| "What is this thing?" (new product, new term, new concept) | Schema tap |
| "How is this different from X?" (positioning, tagline, one-shot pitch) | High-concept pitch |
| "How should our team behave over time?" (culture, values, long-running frame) | Generative analogy |
| "What does success look like?" (goal, strategy, mission) | Behavior-level swap |

---

## Self-check against fabrication

For every rewrite, verify:
1. Every sensory detail either already exists in the audience's shared knowledge OR corresponds to a fact the user actually supplied.
2. No new numbers, names, or physical features have been introduced that the user cannot defend.
3. If the rewrite *needed* invented detail to work, the technique was wrong — re-pick from the table.

Concrete language is a multiplier on truth, not a substitute for it. A concrete lie is just a sticky lie.
