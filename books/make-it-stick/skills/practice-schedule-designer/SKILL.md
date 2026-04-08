---
name: practice-schedule-designer
description: "Design a concrete practice schedule that will actually make learning stick — not just feel productive. Use this skill when the user is preparing for a test, building a new skill, training others, or planning a study program and needs to decide how to structure practice sessions over time. Triggers include: user is relying on marathon study sessions or cramming before a deadline; user practices one topic exhaustively before moving to the next; user feels they know material during practice but forgets it on tests or in real situations; user wants to know how often to review flashcards or revisit past material; user needs to design a training curriculum for a team or class; user is switching between topics during study and wants to know if that is helping or hurting; user is preparing for a performance context (exam, job, sport) and must choose between depth on one skill versus breadth across many. This skill does NOT address memorization technique or recall strategy — use retrieval-practice-study-system for those."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/practice-schedule-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [3, 4, 8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "spaced-repetition", "interleaving", "practice-design"]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "User's learning goal, material list, available time, and current practice approach (if any)"
  tools-required: [Write]
  tools-optional: [Read]
  mcps-required: []
  environment: "Any agent environment; user describes their learning situation in text form or answers guided questions"
discovery:
  goal: "Diagnose the user's current practice approach, classify it against the four practice types, then produce a concrete personalized schedule with spacing intervals, sequencing patterns, and tracking guidance"
  tasks:
    - "Gather learning goal, material type, timeline, and current practice approach"
    - "Diagnose current practice type and identify which anti-patterns are present"
    - "Select optimal practice strategy based on learning goal, material type, and time horizon"
    - "Set spacing intervals calibrated to material difficulty and available time"
    - "Design interleaving and variation patterns appropriate to the content"
    - "Build a concrete schedule document the user can follow immediately"
    - "Warn against the familiarity trap and the blocked-practice illusion"
  audience: "Students, teachers, trainers, coaches, and lifelong learners who need to design or redesign their practice regime"
  triggers:
    - "User is cramming or marathon-studying before a deadline"
    - "User practices one topic exhaustively before moving to the next"
    - "User performs well during practice but forgets material on tests or in real situations"
    - "User wants to know how often to revisit material"
    - "User needs to design a training curriculum for a class or team"
    - "User is alternating topics during study and wants to know if that helps"
    - "User is preparing for a high-stakes performance context"
---

# Practice Schedule Designer

## When to Use

You have material to learn and a timeline to learn it in. What you need now is a practice structure — not just more time studying, but the right pattern of when, how often, and in what order to practice.

This skill is about **schedule design**, not study technique. It tells you how to arrange your practice sessions over time, which types of practice to combine, and how to set spacing intervals for your specific situation.

**Preconditions to verify:**

- Does the user know what they are trying to learn? If the material is completely undefined, ask them to identify it before continuing.
- Does the user have a rough timeline (days, weeks, months)? Interval recommendations depend on it.

**This skill does NOT cover:**

- How to execute retrieval practice within a session (use `retrieval-practice-study-system`)
- How to memorize facts efficiently (flashcard systems, mnemonics)
- How to manage motivation or study environment

---

## The Core Counterintuitive Principle

Before designing any schedule, establish this with the user if they seem unaware of it:

**Feeling productive during practice is not the same as learning durably.**

Massed practice — repeating one thing many times in a row — produces fast visible improvement. That improvement is real but shallow: it rests on short-term memory and fades quickly. Researchers call this "momentary strength." The techniques that build "habit strength" — the kind of learning that is still there weeks later when you need it — feel slower and harder during practice. You sense the effort but not the benefit the effort is creating.

This is why people persist in practicing the wrong way even after they have seen evidence that it does not work. They trust the feeling of progress over the data on retention. The schedule you design here will sometimes feel less productive than the old way. That discomfort is the signal that the learning is durable.

---

## Context and Input Gathering

### Required (ask if missing)

- **What are you learning?** Subject, skill, or material set (e.g., Spanish vocabulary, calculus problem types, sales pitch, guitar chord transitions, medical diagnosis protocols).

- **What is your timeline?** When do you need to perform or be tested? (e.g., exam in 3 weeks, job interview in 10 days, ongoing professional development with no deadline).

- **How much practice time do you have per week?** Total hours available, and how those break into sessions (e.g., 1 hour daily vs. 4 hours on weekends).

- **What does your current practice look like?** Walk through a recent session — what did you do first, second, and for how long? This reveals which practice type they are currently using and which anti-patterns are present.

### Useful (gather if available)

- **Performance context:** What does success look like in the moment of performance? (e.g., unseen exam questions, real-world patient encounters, live athletic competition, a job interview). This determines whether interleaving and variation are especially critical.
- **Material structure:** Is the content a set of similar items (vocabulary, flashcards), or a set of different problem types that require choosing the right approach?
- **Current mastery level:** Beginner (everything is new) vs. intermediate (some material familiar, some not) vs. advanced (maintaining a high level).

---

## Step 1 — Diagnose Current Practice Type

**Why:** Most learners default to massed practice without knowing it. The diagnosis names the pattern, which makes the problem concrete and motivates the schedule change.

Map what the user described onto one of these four types:

| Type | Definition | Recognition Signal |
|---|---|---|
| **Massed** | Long unbroken sessions on one topic; cramming; re-reading | "I study [topic] for 2 hours then move on" or "I cram the night before" |
| **Spaced** | Same material revisited across sessions with time gaps | "I review it again a few days later" |
| **Interleaved** | Multiple topics or problem types mixed within one session | "I mix different subjects in the same sitting" |
| **Varied** | Same skill practiced in different contexts, formats, or conditions | "I practice [skill] in different scenarios or with different examples" |

**Anti-patterns to flag explicitly:**

- **Cramming:** Massed practice compressed into a single session before a deadline. Effective for next-day recall; ineffective for retention beyond 48 hours.
- **Blocked practice:** Practicing the same drill or problem type in a fixed sequence before switching. Feels like variety because the station changes, but is still massed within each station. Common in sports (always running the same drill from the same position) and math courses (doing 20 problems of type A before moving to type B).
- **Familiarity trap:** Stopping practice on material that feels familiar, mistaking recognition for mastery. Recognized by statements like "I already know this one" or skipping flashcards that seem obvious.

State the diagnosis explicitly:

> "Your current practice is primarily [type]. You are experiencing [anti-pattern if present]. Here is what that costs you: [specific retention or transfer consequence]."

---

## Step 2 — Select the Optimal Practice Strategy

**Why:** The right mix of practice types depends on learning goal, material structure, and time horizon. There is no single correct answer — the decision framework below makes the choice explicit and defensible.

### Decision Framework

**Start with your primary learning goal:**

**Goal A — Memorize a fixed set of items** (vocabulary, dates, formulas, anatomical names, legal definitions)
- Primary strategy: **Spaced practice**
- Add: **Interleaving** if the items are similar enough to be confused with each other
- Do not add variation until items are partially learned

**Goal B — Learn to solve problems of a specific type** (math problems, diagnosis protocols, coding patterns)
- Primary strategy: **Interleaved practice** across problem types
- Add: **Spaced** intervals between sessions
- Warning: blocked practice will make performance during practice look better but test performance will be worse

**Goal C — Build a skill that must transfer to unpredictable real-world conditions** (athletic performance, clinical judgment, language conversation, negotiation)
- Primary strategy: **Varied practice** — deliberately change context, format, and conditions across sessions
- Add: **Interleaving** of related sub-skills
- Add: **Spaced** intervals
- Massed practice of a fixed drill will not transfer; you must practice the skill in conditions that vary from the test conditions

**Goal D — Maintain mastery of material already learned** (ongoing professional skills, language retention, athletic fundamentals)
- Primary strategy: **Spaced practice** with long intervals (monthly)
- Material that is well-mastered needs low-frequency review; the Leitner-box principle applies: the better your mastery, the less frequent the practice, but the material never disappears completely from the rotation

**Time horizon modifier:**

| Horizon | Implication |
|---|---|
| Less than 3 days | Spacing intervals are short (hours); prioritize retrieval practice over rereading |
| 1–4 weeks | Set intervals of 1 day → 3 days → 1 week; interleave topics within sessions |
| 1–3 months | Set intervals of 1 day → 1 week → 2–3 weeks → monthly; build in variation |
| Ongoing (no deadline) | Leitner-box style: frequency tracks mastery level; monthly review of well-mastered material |

---

## Step 3 — Set Spacing Intervals

**Why:** The spacing interval determines how much forgetting occurs between sessions. Some forgetting is desirable — the effort of retrieval after a small gap strengthens the memory. Too little gap and you are resting on short-term memory. Too much gap and retrieval approaches relearning from scratch, which is inefficient.

### Interval Calibration Rules

**Rule 1 — The minimum interval is "enough forgetting."**
If you can recall something effortlessly with no hesitation, you reviewed it too soon. A productive session has some difficulty; some items should require real effort to retrieve.

**Rule 2 — The maximum interval is "not so much forgetting that retrieval becomes relearning."**
If you cannot recall an item at all and must look it up as if encountering it for the first time, the interval was too long.

**Rule 3 — Sleep is a consolidation amplifier.**
At least one sleep period between practice sessions significantly aids memory consolidation. This means even in a compressed timeline, practice on Monday and practice on Tuesday are better than two sessions on Monday.

**Recommended starting intervals by material type:**

| Material | First review | Second review | Third review | Ongoing |
|---|---|---|---|---|
| Names and faces, arbitrary associations | Within minutes (high forgetting rate) | Same day | Next day | Weekly, then monthly |
| New concepts from a text or lecture | Within 24 hours | 3–5 days later | 1–2 weeks later | Monthly |
| Problem-solving skills | 1–2 days | 1 week | 2–3 weeks | Monthly |
| Complex judgment skills (clinical, athletic) | Next session | 1 week | 3 weeks | Monthly; plus real-world practice |

**Leitner-box logic for flashcard-style material:**

Divide material into difficulty tiers based on current mastery:

- **Tier 1 (errors frequent):** Review every session
- **Tier 2 (mostly correct):** Review every other session
- **Tier 3 (reliably correct):** Review weekly
- **Tier 4 (mastered):** Review monthly — but never remove from rotation until the learning goal is fully met

When you answer incorrectly, move the item back up one tier (more frequent review). When you answer correctly in consecutive sessions, move it down one tier (less frequent review).

---

## Step 4 — Design the Interleaving and Variation Pattern

**Why:** Interleaving and variation do the work that spacing cannot do alone. Spacing builds retention of individual items. Interleaving builds discrimination — the ability to recognize which type of problem you are facing and select the right approach. Variation builds transfer — the ability to apply a skill in conditions different from where you practiced it.

### Interleaving Design Rules

**When to interleave:** When the material contains two or more distinct problem types, subject areas, or skill categories that the learner must eventually distinguish between. Do not interleave before the learner has a basic grasp of each type — a small amount of initial blocked practice to introduce a new problem type is acceptable.

**How to interleave:** Within a single session, rotate through topics or problem types without completing a full block of any one type. The switch should happen before the learner feels fully on top of the current topic. That feeling of incompleteness is the point: the interruption forces the learner to start fresh retrieval on return, which builds the discrimination ability needed for tests and real situations.

**Do not confuse blocked practice with interleaving:** If your session has 20 minutes on topic A, then 20 minutes on topic B, then 20 minutes on topic C — that is blocked practice across the session, not interleaving. True interleaving mixes A, B, and C within each segment.

> Example: A student preparing for a statistics exam should not work 30 problems of hypothesis testing, then 30 problems of regression, then 30 problems of ANOVA. Instead: do 5 problems, switch types, do 5 more of a different type, switch again. The session will feel slower and less satisfying. The exam results will be better.

### Variation Design Rules

**When to vary:** When the learning goal requires transfer to unpredictable real-world conditions — athletic performance, clinical encounters, language conversation, professional problem-solving. If the test conditions will differ from practice conditions, practice must differ internally too.

**How to vary:** Change one or more of the following across sessions: context (location, sequence, trigger conditions), format (problem presentation, question phrasing), conditions (speed, materials available, teammate or patient involved), or level of challenge (harder examples, more ambiguous cases).

**Blocked practice warning for motor and procedural skills:** Always practicing a drill from the same position, in the same sequence, at the same speed locks the skill to those conditions and prevents transfer. Vary the starting position, the sequence, the speed, and the context systematically.

> Example: A professional learning a sales pitch should not practice it the same way from the same prompt every time. Vary the opener, the objection presented, the simulated client's emotional state, and the medium (phone vs. in-person vs. video call). This is uncomfortable — it will feel like the learning is not taking hold. That discomfort is producing a more robust skill.

---

## Step 5 — Build the Practice Schedule Document

**Why:** An abstract plan does not change behavior. A concrete schedule the user can open on Monday morning and follow without re-reading instructions does.

Produce a schedule document with the following components:

**Header block:**
- Learning goal
- Timeline (start date and performance date)
- Material list (what is being practiced)
- Total sessions planned
- Session length

**Session-by-session plan** (for schedules 4 weeks or shorter, list every session; for longer schedules, provide a repeating weekly template plus interval triggers):

For each session:
- Date or week number
- Duration
- Topics to cover and rotation sequence (for interleaved sessions)
- What to retrieve (specific problem types, flashcard tiers, or skill variants)
- What to check (which mastery tier items are due for review)

**Interval trigger rules** (so the user can adapt if they miss a session):
- "If you miss a session, do not double up the next day. Resume the schedule; the gap is not wasted — some forgetting during the gap is acceptable."
- "If an item in Tier 1 is still in Tier 1 after 3 sessions, flag it for deeper investigation or alternate explanation — repetition alone will not fix a conceptual gap."

**Anti-pattern warning reminders** (embed in the schedule):
- At the start of every session: "Resist the urge to review items you feel you already know. Quiz yourself before checking. The familiarity trap is the most common reason well-prepared learners underperform."
- At the midpoint of any block: "If this is starting to feel effortless, switch topics or problem types now — not when you have finished the block."

---

## Worked Examples

### Example A: Exam Preparation — 3-Week Timeline

**Situation:** University student, organic chemistry final exam in 21 days. Currently: reads lecture notes for 2 hours then attempts a few problems at the end of each session. Covers one reaction type per session.

**Diagnosis:** Massed practice with blocked problem-solving. The reading-then-practice pattern means retrieval happens only after review, so short-term memory is carrying the work. One reaction type per session = blocked practice.

**Selected strategy:** Interleaved practice across reaction types, spaced across sessions.

**Spacing intervals:** Sessions 6 days per week, 90 minutes each.

**Week 1:** Introduce all 6 reaction types across 2 sessions each (brief blocked intro, ~15 min per type). By end of week, all types have been seen.

**Weeks 2–3:** Every session mixes problem types. 6 problems per sitting, each from a different reaction type in random order. Also retrieve prior lecture concepts: at the start of each session, answer 3 questions from Week 1 material before working new problems.

**Interval triggers:** Any reaction type answered incorrectly moves to "daily review" status. Any answered correctly 3 times in a row in interleaved conditions moves to "every-other-session" status.

---

### Example B: Professional Skill — Ongoing Sales Training

**Situation:** A team of 8 new sales agents needs to learn 4 skill areas over 6 months: prospecting, product knowledge, objection handling, and business planning. Current approach: one full day of training on each skill area before moving to the next.

**Diagnosis:** Massed curriculum design. Full-day blocks on single topics will produce rapid performance during training but weak retention and poor transfer when agents face real customers who mix topics spontaneously.

**Selected strategy:** Spiraling interleaved curriculum with spaced return to all 4 skill areas.

**Design:** Weekly sessions cycle through all 4 areas, returning to each with new examples and more complex scenarios that require applying earlier learning in a new context. No single session devotes more than 25% of time to one skill area.

**Variation:** Role-play scenarios in each session change the client profile, objection type, and product involved. After month 2, agents practice with no script, varying the opener.

**Tracking:** Weekly 5-question quiz covering one item from each of the 4 areas plus one item from a randomly selected prior week. Agents track their own error rate per area. Any area below 70% correct triggers additional retrieval practice in the next session.

---

### Example C: Athletic Skill — Learning a Technical Movement

**Situation:** Tennis player improving their second serve. Currently practices 50 serves in a row at the end of every session.

**Diagnosis:** Massed practice (blocked repetition from the same position). Will encode a serve that works in practice conditions but deteriorates under match pressure and varied court position.

**Selected strategy:** Varied practice with spacing.

**Design:** Second serve practice is distributed within each session (not saved for the end). Each serve set uses a different starting court position, a different target zone, and a different immediately preceding shot (serve after a baseline rally, serve cold at the start, serve under a 30-second time limit). No more than 10 consecutive serves from the same position.

**Spacing:** Serve technique reviewed every session but never as a marathon block. Maintenance once per session (15 minutes), interleaved with other technical elements.

---

## Quick Reference: Practice Type Selection

```
LEARNING GOAL                   → PRIMARY STRATEGY
------------------------------------------------------
Memorize fixed items             → Spaced (+ interleave if confusable)
Solve typed problems             → Interleaved (+ spaced sessions)
Transfer to unpredictable use    → Varied (+ interleaved + spaced)
Maintain existing mastery        → Spaced (long intervals, Leitner logic)

TIME HORIZON                    → STARTING INTERVAL
------------------------------------------------------
< 3 days                         → Hours between sessions; prioritize retrieval
1–4 weeks                        → 1 day → 3 days → 1 week
1–3 months                       → 1 day → 1 week → 2–3 weeks → monthly
Ongoing                          → Mastery-based (Leitner tiers)

ANTI-PATTERN CHECK              → CORRECTION
------------------------------------------------------
Cramming                         → Break into sessions with gaps
Blocked practice                 → Interleave within sessions
Familiarity trap                 → Quiz before reviewing; never skip "known" items
```

---

## References

- `references/practice-type-comparison.md` — Full research evidence for each of the four practice types, including the geometry study (89% blocked vs. 63% interleaved during practice; 20% blocked vs. 63% interleaved on delayed test), the surgical resident spaced training study, and the beanbag motor learning experiment
- `references/spacing-interval-guide.md` — Detailed interval tables by material type, cognitive load, and learner experience level; guidance for compressing or expanding schedules when time constraints change
- `references/leitner-box-implementation.md` — Step-by-step Leitner box setup for flashcard-style material; digital and physical implementations; troubleshooting stalled items

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
