---
name: growth-mindset-and-deliberate-practice
description: |
  Diagnose fixed vs growth mindset patterns and design a deliberate practice protocol for expertise development. Use when someone wants to develop expertise in a skill domain, is struggling to improve despite repeated practice, attributes their performance plateau to talent limits, praises or criticizes someone for being a "natural," says "I'm just not good at this," avoids challenges to protect their reputation, or asks how to get to 10000 hours effectively. Applies Dweck's 4-quadrant model (fixed/growth mindset × performance/learning goal orientation) to classify the learner's current stance, identifies fixed-mindset signals and attribution patterns, then designs a deliberate practice plan using Ericsson's 5 characteristics. Growth mindset is the prerequisite — without it, deliberate practice collapses into avoidance. Together they form a complete talent vs effort expertise-building pathway. Produces: mindset diagnostic report + deliberate practice plan with feedback loops, mental model targets, and practice structure.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/growth-mindset-and-deliberate-practice
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - make-it-stick
chapters: [4, 7, 8]
tags:
  - learning-science
  - cognitive-psychology
  - evidence-based-learning
  - growth-mindset
  - deliberate-practice
  - expertise
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: conversation
      description: "Learner's domain, current performance level, and responses to difficulty or failure"
    - type: none
      description: "Skill can run from a brief description of the learner's situation"
  tools-required: [TodoWrite]
  tools-optional: [Read, Grep]
  environment: "Works from any context; richer input produces more specific output"
---

# Growth Mindset and Deliberate Practice

## When to Use

Use this skill when you are working with a learner who:
- Has **plateaued in a skill domain** despite repeated effort — improvement has stalled
- **Attributes failure to fixed ability** — "I'm not talented enough," "some people just have it"
- **Avoids challenging practice** — sticks to tasks they can already perform well
- **Praises or blames innate traits** — calls someone a "natural" or says they "just don't have the gift"
- **Wants to build expertise** — is asking how to reach mastery, or wondering if 10,000 hours is real
- **Shows test anxiety or fear of failure** — avoids difficulty because struggling feels like evidence of inadequacy

Preconditions: you need at minimum:
- The **domain** in which the learner wants to develop expertise (music, coding, writing, athletics, etc.)
- At least one signal about how they **respond to difficulty** (do they persist, retreat, blame themselves?)

**Agent:** Before starting, confirm you have enough to place the learner on the 4-quadrant model. If domain and failure-response are both unknown, ask for them before proceeding.

## Context and Input Gathering

### Input Sufficiency Check

```
User message → Extract domain + difficulty-response signals
                    ↓
Environment → Scan for past performance descriptions, stated goals, praise language
                    ↓
Gap analysis → Can I place the learner on the 4-quadrant model?
                    ↓
     Both domain and response missing? ──YES──→ ASK (one question)
                    │
                    NO
                    ↓
              PROCEED with diagnosis
```

### Required Context

- **Domain:** What skill or field is the learner trying to develop?
  → Check prompt for: named subject, profession, activity, "get better at X"
  → If missing, ask: "What domain or skill are you trying to develop expertise in?"

- **Response to difficulty:** How does the learner react when they fail, struggle, or hit a plateau?
  → Check prompt for: attribution language ("not talented," "just practicing"), avoidance signals, help-seeking
  → If missing, ask: "When you hit a setback in this area — something you tried and failed at — what do you typically do or think?"

### Observable Signals (extract from description)

- **Attribution patterns:** Does failure trigger "I'm not capable" (fixed) or "I need a better strategy" (growth)?
- **Challenge selection:** Does the learner pick tasks at the edge of current ability, or stay in the comfort zone?
- **Praise language used:** Do they praise or admire innate talent in others? Do they describe their own successes as "natural"?
- **Effort theory:** Do they believe that needing to work hard is evidence of lesser ability?

### Default Assumptions

- If no difficulty-response is given: assume the learner has some fixed-mindset patterns (most adults do, especially in domains where they received intelligence-based praise as children).
- If domain is unspecified but expertise-building language is present: treat domain as TBD and note that the practice design will need it.
- If no current level is given: assume early-to-intermediate learner who has some foundation but has not yet invested hundreds of hours in deliberate solo practice.

## Process

Use `TodoWrite` to track all steps before beginning.

```
TodoWrite([
  { id: "1", content: "Gather learner domain and difficulty-response signals", status: "pending" },
  { id: "2", content: "Classify on the 4-quadrant mindset model", status: "pending" },
  { id: "3", content: "Identify fixed-mindset signals and attribution patterns", status: "pending" },
  { id: "4", content: "Design deliberate practice protocol using 5 characteristics", status: "pending" },
  { id: "5", content: "Set up feedback loops and coach/peer review structure", status: "pending" },
  { id: "6", content: "Produce mindset diagnostic report + deliberate practice plan", status: "pending" }
])
```

---

### Part A: Mindset Diagnostic

---

#### Step 1: Gather Difficulty-Response Signals

**ACTION:** Collect data on how the learner responds to failure, setbacks, challenge selection, and praise — across at least three different contexts if available.

**WHY:** Mindset is not a stable trait — it is a pattern of attributions that shows up most clearly under pressure. A learner who expresses enthusiasm for growth when relaxed may revert to fixed-mindset behavior the moment they fail publicly. The signal that matters is the *response to failure*, not the stated belief about ability. Dweck's research consistently showed that behavior under adversity, not self-report, is the diagnostic indicator.

**Detection signals to look for:**

| Signal | Mindset indicator |
|--------|-------------------|
| "I'm just not a math person" | Fixed — ability is a stable, inherited trait |
| "I wasn't born with musical talent" | Fixed — innate endowment, not accumulated skill |
| "That mistake tells me what to work on next" | Growth — failure is information |
| "He's a natural — it comes easily to him" | Fixed praise frame — attributes success to gift, not effort |
| "I worked hard and it paid off" | Growth attribution — effort caused outcome |
| "I avoided the competition because I might embarrass myself" | Fixed + performance goal — protecting reputation |
| "I picked an easier problem so I'd look competent" | Fixed + performance goal — validation seeking |
| "I stayed up late drilling the hard parts" | Growth + learning goal — effort toward mastery |

**Agent:** Extract these signals explicitly from the learner's description. Note both what the learner *says* about ability and what their *behavior* reveals. These often diverge.

Mark Step 1 complete in TodoWrite.

---

#### Step 2: Classify on the 4-Quadrant Model

**ACTION:** Place the learner in one of four quadrants formed by two axes: **Mindset** (Fixed ↔ Growth) and **Goal Orientation** (Performance goal ↔ Learning goal).

**WHY:** Mindset and goal orientation are related but distinct. A person can believe their abilities are fixed and still pursue learning goals (they just won't persist when it gets hard). A person can hold a growth mindset but be trapped in performance goals (they know effort builds ability, but social comparison dominates). The combination determines both *what behavior you will see* and *which intervention addresses the root cause*. Treating a performance-goal problem with a mindset intervention alone, or vice versa, produces partial results.

**The 4-Quadrant Model:**

```
                   LEARNING GOAL
                   (build mastery)
                        │
  Fixed Mindset ────────┼──────── Growth Mindset
  (ability fixed)       │         (ability grows)
                        │
                 PERFORMANCE GOAL
                 (validate ability)
```

**Quadrant descriptions:**

| Quadrant | Mindset | Goal | Behavior pattern | Risk |
|----------|---------|------|-----------------|------|
| Q1: Growth + Learning | Growth | Learning | Seeks challenges, interprets failure as data, persists on hard problems | Low — this is the target state |
| Q2: Fixed + Learning | Fixed | Learning | Studies hard but collapses when effort does not produce results; may believe effort is pointless if "not talented" | Moderate — effort theory intervention needed |
| Q3: Fixed + Performance | Fixed | Performance | Avoids challenge, chooses easy tasks, quits when failure threatens self-image | High — most resistant to change |
| Q4: Growth + Performance | Growth | Performance | Persists through difficulty but is driven by comparison and validation; may be demotivated without external feedback | Moderate — goal reframing needed |

**Classify the learner** based on their signals. Note which quadrant and cite the specific signals that placed them there.

**Examples:**

- A fifth-grader praised repeatedly for being "so smart" who now picks easier puzzles to protect their reputation → Q3 (Fixed + Performance). The praise itself caused the shift.
- A musician who says "I'm not naturally talented, but I practice every day and always pick the hardest passages to drill" → Q1 (Growth + Learning). Already in target state; reinforce.
- A developer who knows that "anyone can learn to code with effort" but only takes projects where they already know the answer → Q4 (Growth + Performance). Growth mindset is present; goal reorientation needed.

Mark Step 2 complete in TodoWrite.

---

#### Step 3: Identify Fixed-Mindset Signals and Attribution Patterns

**ACTION:** Surface the specific fixed-mindset traps and errorless-learning myths that are limiting this learner. Name the attribution pattern (what the learner says causes failure) and the intervention it calls for.

**WHY:** Fixed mindset manifests in predictable patterns, but the surface behavior varies. A star athlete who avoids practice because "naturals shouldn't need it" and a student who quits after one bad grade are both showing fixed-mindset behavior — but the intervention differs. Naming the specific pattern matters because growth-mindset interventions work by directly contradicting the attribution: you cannot change a belief you have not identified. Dweck's 7th-grade intervention succeeded precisely because it gave students a *specific reframe* ("effort forms new neural connections") rather than a vague pep talk.

**Fixed-mindset traps to detect:**

1. **Natural talent trap:** "Real experts don't need to work hard. If I have to struggle, I don't have what it takes." This leads to avoidance of the very practice that builds expertise.
   - Intervention: Show that Michelangelo's Sistine Chapel required four torturous years; Mozart's reconstructive memory was the product of acquired skill, not sixth sense.

2. **Errorless learning myth:** "If I'm making mistakes, the practice isn't working." This causes learners to stay in the comfort zone, doing what they can already do — which does not build new capabilities.
   - Intervention: Errors are essential feedback. Deliberate practice requires striving *beyond* current level; mistakes signal you are practicing in the right zone.

3. **Effort-equals-inability belief:** "Smart people don't need to try. My need for effort proves I'm not intelligent."
   - Intervention: Effortful learning changes the brain — myelination of relevant axons, formation of new synaptic connections, hippocampal neurogenesis. Effort is the mechanism, not the evidence of limitation.

4. **Test-anxiety loop:** Fear of failure consumes working memory capacity needed to perform, causing worse outcomes, which confirms the fear. Students with this pattern expend working memory monitoring their performance ("Am I making mistakes?") rather than solving problems.
   - Intervention: Teach that difficulty is expected and productive. A French study found that sixth graders taught "errors are a natural part of learning" showed significantly better working memory use on subsequent tests.

5. **Performance-goal trap:** Choosing challenges calibrated to showcase existing ability, not to build new ability. This delivers short-term validation but zero expertise growth.
   - Intervention: Reframe the measure of success from "did I look competent?" to "did I encounter and resolve something I couldn't do before?"

**Output:** A short list of detected traps with the specific signals that revealed each one, and the reframe each trap calls for. This is the input to the growth-mindset intervention (presented to the learner) and to Step 4 (used to calibrate practice zone).

Mark Step 3 complete in TodoWrite.

---

### Part B: Deliberate Practice Design

---

#### Step 4: Design Practice Protocol Using 5 Characteristics

**ACTION:** Structure a practice plan that satisfies all five characteristics of deliberate practice as defined by Ericsson's research.

**WHY:** Mere repetition is not deliberate practice. Most learners who plateau are repeating what they can already do — reinforcing existing capability without extending it. Ericsson's research on experts across chess, music, sports, medicine, and science found that expert performance is the product not of innate gifts but of the quantity and quality of practice. Crucially, the *quality* dimension is not met by simple repetition; it requires a specific structure. Expertise is built layer by layer, through thousands of hours of this specific structure — not through general experience or logging time.

**The 5 Characteristics of Deliberate Practice:**

1. **Goal-directed:** Each session targets a specific, identified weakness or skill gap — not general improvement.
   - *How to apply:* Before each session, name the one thing being improved. "Today I am working on X" — where X is specific enough that at the end you can say whether you improved it.
   - *Why this matters:* Without a target, practice defaults to what the learner is already good at. The difficulty of identifying specific weaknesses is itself a form of metacognitive work that accelerates learning.

2. **Striving beyond current level:** Practice should be just beyond current competence — difficult enough to produce errors and require effort, not so difficult as to be overwhelming.
   - *How to apply:* Use the "struggle zone" — find the point where the learner succeeds roughly 50-70% of the time. If success rate is above 80%, increase difficulty. If below 40%, reduce it.
   - *Why this matters:* Success at already-mastered tasks produces fluency but not new capability. The neural rewiring, myelination increases, and mental model expansion that characterize expertise development happen in response to striving, failure, and correction — not to smooth performance.

3. **Feedback loops:** Immediate, accurate feedback on each attempt, enabling correction before errors become habits.
   - *How to apply:* Identify the feedback source — a coach, a peer reviewer, a scoring system, audio/video self-review. Define at what granularity feedback will arrive (per attempt, per session, per week). See Step 5 for structure.
   - *Why this matters:* Without feedback, a learner cannot distinguish effective from ineffective technique. Practice without accurate feedback may reinforce the wrong patterns, making expert performance harder to reach, not easier. Deliberate practice usually requires a coach or trainer who can identify performance gaps the learner cannot see from the inside.

4. **Solitary and sustained:** A significant portion of deliberate practice should be individual, focused, and uninterrupted — not social, performance-oriented, or diluted by multitasking.
   - *How to apply:* Reserve dedicated time blocks (minimum 60-90 minutes) for solo deliberate practice sessions, separate from performance contexts. Ericsson found the best experts spent the largest percentage of their total hours in solitary, deliberate practice.
   - *Why this matters:* Social practice contexts introduce performance pressures (avoid looking bad) that conflict with the error-seeking behavior required for skill extension. Solitary practice enables the learner to deliberately put themselves in situations they cannot yet handle.

5. **Mental model accumulation:** Over time, deliberate practice builds a library of complex mental models — patterns for action in a vast vocabulary of situations — that is the substrate of expert judgment.
   - *How to apply:* After each practice session, name the new pattern or case type encountered. Maintain a running catalog of mental models in the domain (e.g., for a chess player: board configurations; for a programmer: algorithm patterns; for a writer: sentence structures). Review and extend this catalog periodically.
   - *Why this matters:* Expert performance is not faster reflexes — it is richer pattern recognition. A chess master can contemplate many alternative moves and their cascading consequences because they have accumulated a vocabulary of board configurations. The goal of deliberate practice is to build this vocabulary, not merely to log hours. Ten thousand hours of low-quality repetition does not produce this; ten thousand hours of deliberate practice does.

**Practice Protocol Template:**

```
Domain: [field]
Current level: [brief description]
Primary weakness being targeted: [specific gap, from Step 3]

Session structure:
- Duration: [minimum 60-90 min uninterrupted]
- Warm-up: [brief review of prior session's patterns]
- Core work: [specific drill or task targeting weakness, at struggle-zone difficulty]
- Error capture: [note every failure and what it revealed]
- Pattern cataloging: [add any new mental model to running catalog]
- Feedback: [when and how, from whom or what — see Step 5]

Weekly cadence:
- [N] solo deliberate practice sessions per week
- [N] performance/application sessions per week (separate — not deliberate practice)
- [N] feedback review sessions per week

Difficulty progression:
- Increase difficulty when: success rate > 70% for two consecutive sessions
- Reduce difficulty when: success rate < 40% for one session
```

Mark Step 4 complete in TodoWrite.

---

#### Step 5: Set Up Feedback Loops and Coach/Peer Review

**ACTION:** Define who provides feedback, at what frequency, at what level of granularity, and how that feedback connects back to practice design revision.

**WHY:** Feedback is not merely motivating — it is *calibrating*. Deliberate practice without accurate feedback can consolidate incorrect technique, build the wrong mental models, and create confident incompetence. Ericsson's research showed that expert performers who reach the highest levels almost universally worked with coaches or trainers who could identify problems the performer could not perceive from within their own practice. The learner's internal model of their own performance is systematically biased — they cannot see what they cannot yet see. External feedback closes this perceptual gap.

**Feedback structure to design:**

| Feedback type | Source | Frequency | Granularity |
|---------------|--------|-----------|-------------|
| Immediate corrective | Coach, scoring system, peer reviewer | Per attempt or per session | Specific technique: "your fingering on bar 12 is incorrect," not "play better" |
| Pattern-level | Self-review (audio/video) + coach | Weekly | Which error types keep recurring — targets for next week's practice |
| Progress tracking | Objective performance metrics | Monthly | Are measurable outcomes improving at a rate consistent with deliberate practice investment? |
| Mental model check | Coach interview or self-quiz | Monthly | Can the learner articulate the pattern they encountered this week in their domain's vocabulary? |

**If a coach is unavailable:**
- Use video or audio self-review with a specific checklist of technique dimensions
- Find a peer at slightly higher skill level who can provide corrective feedback in exchange for reciprocal review
- Use scoring systems with granular breakdowns (not just pass/fail — specific component scores)
- Document every error in writing immediately after it occurs, with a hypothesis about cause

**Feedback-to-practice cycle:**

```
Session → Error capture → Pattern identification → Practice target update
    ↑                                                         │
    └─────────────────────────────────────────────────────────┘
```

The feedback loop is not complete until the feedback *changes the next session's target*. Feedback that is absorbed but not acted on does not improve performance. After each feedback cycle, update the "primary weakness being targeted" in the practice protocol.

Mark Step 5 complete in TodoWrite.

---

#### Step 6: Produce Output — Mindset Diagnostic Report and Deliberate Practice Plan

**ACTION:** Assemble the findings from Steps 1-5 into a two-part output: (A) the mindset diagnostic report, and (B) the deliberate practice plan.

**WHY:** These two outputs serve different purposes and different audiences. The mindset diagnostic report is a mirror — it names what the learner currently believes about their own ability and shows them specifically how those beliefs produce the behaviors limiting their growth. It should be specific enough to be recognizable, not generic. The deliberate practice plan is an operational document — it gives the learner something to do in the next session and a structure to follow over the next 90 days. Together they address both the prerequisite (mindset) and the method (practice design). A practice plan given to a learner in Q3 (Fixed + Performance) without addressing the mindset first will be resisted or abandoned when it produces the discomfort of striving.

**Output Part A — Mindset Diagnostic Report:**

```markdown
# Mindset Diagnostic Report

## Domain
[Field / skill area]

## Quadrant Classification
[Q1-Q4, with the two-axis labels]

## Signals That Placed You Here
- [Signal 1]: [What behavior or attribution revealed this]
- [Signal 2]: ...

## Fixed-Mindset Traps Detected
- [Trap name]: [Specific manifestation in this learner] → [Reframe]

## Growth-Mindset Intervention
[One or two sentences tailored to the learner's specific attributions — not generic motivation,
but a direct reframe of the exact belief pattern identified above]

## What Changes When Mindset Shifts
[Concrete description of how the learner's behavior will look different
once the growth mindset is operative — specific to this domain]
```

**Output Part B — Deliberate Practice Plan:**

```markdown
# Deliberate Practice Plan

## Domain and Current Level
[Field, brief level description]

## Primary Expertise Target (90-day horizon)
[Specific capability that will be meaningfully advanced through this plan]

## Practice Protocol
[Populated template from Step 4]

## Feedback Structure
[Populated table from Step 5, adapted to this learner's access to coaches/tools]

## Mental Model Catalog (starter entries)
[3-5 domain patterns the learner will track and extend through practice]

## Milestones
- 30 days: [Observable indicator of progress]
- 60 days: [Observable indicator]
- 90 days: [Observable indicator]

## What This Will Feel Like
Deliberate practice is usually not enjoyable. It requires striving at the edge of current ability,
which means frequent failure and discomfort. This is not a sign the practice is not working —
it is a sign it is. The discomfort is the myelination happening.
```

Mark Step 6 complete in TodoWrite.

---

## Inputs

- **Domain:** The field or skill in which the learner is developing expertise
- **Difficulty-response signals:** How the learner reacts to failure, setbacks, and challenges (can be brief)
- **Current level:** Optional but useful — helps calibrate the struggle zone

## Outputs

- **Mindset Diagnostic Report** — quadrant classification, detected traps, and tailored growth-mindset reframe
- **Deliberate Practice Plan** — session structure, feedback loops, mental model catalog, and 90-day milestones

## Key Principles

- **Mindset is a prerequisite, not a companion.** A fixed-mindset learner will abandon deliberate practice at the first stretch of discomfort. The mindset diagnosis must happen first and the reframe must be credible to the learner — not a pep talk, but a mechanistic explanation of how effort changes the brain.

- **Effort does not equal ability limitation.** The belief that "needing to work hard proves I'm not talented" is the most corrosive fixed-mindset pattern. It causes learners to avoid precisely the practice that builds expertise. The research finding is the inverse: the best performers invested the *most* hours of deliberate practice, not the fewest.

- **Praise shapes attribution.** Praising a learner for being "smart" or "talented" after a success produces fixed-mindset behavior more reliably than praising effort. In Dweck's study, 90% of students praised for effort chose harder subsequent challenges; the majority praised for intelligence chose easier ones. This has direct implications for how feedback should be framed.

- **The struggle zone is the practice zone.** If a learner is succeeding easily, they are practicing what they already know. The neural adaptations that produce expertise — myelination, new synaptic connections, pattern vocabulary expansion — are driven by striving, failure, and correction. Easy practice produces fluency; it does not produce expertise.

- **Ten thousand hours requires deliberate structure.** Ericsson's finding is not that 10,000 hours of any practice produces expertise. It is that the experts studied had invested approximately that much time in *deliberate* practice — goal-directed, beyond-current-level, feedback-rich, solitary striving. General experience, performance contexts, and low-stakes repetition do not count toward this total.

- **Mental model accumulation is the outcome measure.** The visible product of thousands of hours of deliberate practice is not faster fingers or harder muscles — it is a richer vocabulary of domain patterns. The expert chess player who can contemplate dozens of move sequences has accumulated a pattern library through deliberate practice that a novice cannot access. This is what expertise is. Practice design should target the expansion of this pattern library explicitly, not just the accumulation of hours.

## Examples

**Example 1: Student with performance plateau**

Learner description: "I've been playing guitar for three years but I feel stuck. I'm decent at songs I already know but every new technique I try just sounds bad. I watch other players and they just seem to have natural feel for it."

Diagnosis:
- Step 1: "Natural feel" attribution → fixed-mindset signal. Avoidance of new techniques because they "sound bad" → errorless-learning myth.
- Step 2: Fixed + Performance goal (Q3). Sticks to repertoire where they already sound competent; abandons new techniques quickly.
- Step 3: Traps: natural talent trap ("they just have feel for it"), errorless learning myth ("sounds bad = doing it wrong = stop"), performance goal trap (practice sessions are performance, not striving).

Practice plan:
- Practice domain: Guitar technique
- Primary weakness: New technique acquisition (currently abandoned when imperfect)
- Protocol: 3x/week, 90-min solo sessions. First 15 min: review one technique from last session. Core 60 min: target one specific new technique at 60% success rate (slow, isolated, deliberately imperfect). Error capture: record audio, note what the mistake reveals. Final 15 min: pattern catalog entry.
- Feedback: Weekly audio self-review against a checklist of the technique's components; monthly lesson with a teacher.
- Mindset reframe: "Sounding bad during practice is evidence the practice is working. The discomfort is the learning. A guitarist who only practices what already sounds good is maintaining repertoire, not building technique."

---

**Example 2: Developer who knows growth mindset but stagnates**

Learner description: "I know that anyone can learn to code with effort. But I keep taking projects where I already know the solutions. I'm good but I haven't learned anything new in two years."

Diagnosis:
- Step 1: States growth-mindset belief; behavior contradicts it. Avoids projects with unknown solutions.
- Step 2: Growth + Performance goal (Q4). Growth mindset is genuine; goal orientation is the problem — external validation (competent performance) dominates over skill acquisition.
- Step 3: Trap: performance-goal trap. Effort theory is correct but applied to already-known territory.

Practice plan:
- Practice domain: Software engineering
- Primary weakness: Novel problem-solving under uncertainty
- Protocol: 2x/week, 90-min solo sessions. Target: algorithm or architecture problem type where failure rate is 40-60%. No looking up solutions until 30+ minutes of genuine striving. Error capture: document what the failed attempt revealed about the knowledge gap. Pattern catalog: name the algorithm or design pattern encountered.
- Feedback: Peer code review with explicit focus on "what did you not know before this?" — not quality review, but knowledge-acquisition review.
- Goal reframe: "The measure of a good practice session is not a working solution — it is a specific thing you encountered that you could not do before. That is the unit of progress."

---

**Example 3: Learner already in Q1 (Growth + Learning)**

Learner description: A pianist who deliberately drills the hardest passages at slow tempo, says "I practice what I can't do, not what I can," and keeps a notebook of fingering solutions discovered through practice.

Diagnosis:
- Step 2: Growth + Learning goal (Q1). Already in target state.
- This learner does not need a mindset intervention. The role of this skill is to verify the practice structure satisfies all 5 characteristics (particularly: is feedback granular enough? is the mental model catalog being maintained?) and reinforce what is already working.

Practice guidance: Audit current practice against 5 characteristics. Likely gap: feedback loop may not be closing back into practice target revision. Recommendation: explicitly name the updated practice target at the start of each session based on last session's error capture.

## References

- For detailed evidence on the 4-quadrant model and Dweck's praise research, see [mindset-framework.md](references/mindset-framework.md)
- For Ericsson's deliberate practice research, expert domain examples, and the 10,000-hour finding, see [deliberate-practice-reference.md](references/deliberate-practice-reference.md)
- Source: *Make It Stick* by Brown, Roediger, and McDaniel, Chapters 4, 7, and 8

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
