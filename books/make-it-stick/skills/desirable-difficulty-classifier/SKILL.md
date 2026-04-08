---
name: desirable-difficulty-classifier
description: Classify any learning activity, practice structure, or instructional design element as a desirable difficulty (strengthens encoding) or undesirable difficulty (creates friction without learning benefit). Use this skill when an instructional designer, trainer, teacher, or learner wants to audit a course design, training session, study method, or practice regimen for evidence-based difficulty management — even if they don't use the phrase "desirable difficulty." Applies to onboarding programs, corporate training, academic course design, self-study plans, coaching sessions, and skill development programs. Identifies which of six proven difficulty strategies are present or absent (spacing, interleaving, variation, retrieval, generation, elaboration) and generates specific redesign recommendations. Do NOT use this skill to build a full study schedule (use retrieval-practice-study-system), to assess learner readiness or aptitude, or to evaluate content quality unrelated to difficulty structure.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/desirable-difficulty-classifier
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [4, 6, 8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "instructional-design", "learning-difficulty"]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: description
      description: "Description of a learning activity, course structure, training program, or study method"
  tools-required: []
  tools-optional: [Read]
  mcps-required: []
  environment: "Any agent environment. No file access required unless the user provides a course document."
discovery:
  goal: "Classify every difficulty element in a learning design as desirable or undesirable, map present and absent strategies from the six-strategy taxonomy, and produce a prioritized set of redesign recommendations."
  tasks:
    - "Gather description of the learning activity and learner context"
    - "Screen each difficulty element against Bjork's two-part classification test"
    - "Map each desirable difficulty to one or more of the six named strategies"
    - "Identify which of the six strategies are absent and represent improvement opportunities"
    - "Generate a difficulty analysis report with bilateral contrast and recommendations"
  audience: ["instructional designers", "teachers", "trainers", "corporate L&D teams", "coaches", "self-directed learners"]
  triggers:
    - "Is this training design effective?"
    - "Why isn't the learning sticking?"
    - "Review this course for evidence-based difficulty"
    - "Are we making it too easy or too hard?"
    - "Help me redesign this practice session"
    - "Audit this onboarding program"
    - "Is this study method actually working?"
  not_for:
    - "Building a complete study schedule (use retrieval-practice-study-system)"
    - "Assessing whether a learner has a learning disability or cognitive limitation"
    - "Evaluating content accuracy or subject-matter quality"
  environment: "Can operate on a verbal description, syllabus document, training outline, or practice schedule"
  quality:
    completeness_score:
    accuracy_score:
    value_delta_score:
---

# Desirable Difficulty Classifier

## When to Use

You are reviewing or designing a learning experience and want to know whether the difficulty it creates strengthens or weakens learning. Typical situations:

- An instructional designer completed a course outline and wants an evidence-based difficulty audit before launch
- A trainer notices participants are not retaining material and suspects the difficulty structure is wrong
- A learner is working through a study method (e.g., rereading, re-watching lectures) and wants to know why nothing is sticking
- A corporate L&D team is redesigning onboarding and wants to know which difficulties to add or remove
- A coach wants to evaluate a practice regimen for an athlete, musician, or professional

Before starting, verify:
- Is a description of the learning activity available? (Enough to understand what the learner does during practice or study)
- What is the learner's background and the intended skill being developed?

**Mode: Hybrid** — The agent runs the classification analysis and generates the report. The human decides which recommendations to implement.

## Context and Input Gathering

### Required Context (must have — ask if missing)

- **Learning activity description:** What does the learner actually do during practice or study?
  → Check for: course syllabi, training outlines, practice schedules, session descriptions, study method descriptions
  → If missing, ask: "Describe the learning activity — what does the learner do, in what order, and for how long?"

- **Target skill or knowledge:** What must the learner be able to do after learning?
  → Check for: learning objectives, job competency requirements, exam descriptions
  → If missing, ask: "What should the learner be able to do after this training? What does success look like?"

- **Learner background:** Prior knowledge and skill level of the learner
  → Check for: prerequisite statements, audience profile, experience level
  → If missing, assume intermediate (some prior exposure to the domain, not expert)

### Observable Context (gather without asking)

- **Practice structure signals:** Any mention of blocked practice, random ordering, massed sessions, or spaced reviews
- **Assessment signals:** Whether the design includes tests, quizzes, or performance checks
- **Feedback signals:** Whether corrective feedback is provided and when

### Default Assumptions

- If no prior knowledge is specified → assume intermediate learner
- If no timeline is specified → assume multi-week program (not single-session)
- If the description mentions "lecture + notes" with no practice → flag as massed-passive baseline

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
  ✓ Learning activity is described clearly enough to identify practice structure
  ✓ Target skill or knowledge is known
  ✓ Learner background is known or acceptably assumed
BLOCK if: the description is so vague (e.g., "we do training") that no structural elements can be identified
```

## Process

### Step 1 — Map the Learning Activity Structure

Read the description and identify all structural elements of the learning design. Extract:

- **Practice format:** How content is delivered (lecture, demonstration, reading, video, simulation)
- **Practice timing:** How sessions are spaced or compressed (single block, daily, weekly, on-demand)
- **Practice order:** Whether topics are blocked (one type at a time) or mixed (interleaved)
- **Practice variation:** Whether the same scenario is repeated identically or varied
- **Assessment method:** Whether learners are tested, self-quizzed, or never formally assessed
- **Learner generation:** Whether learners are asked to produce answers, solve problems, or only receive information
- **Elaboration prompts:** Whether learners are asked to connect new knowledge to prior knowledge or to explain in their own words

**WHY:** Classification requires knowing the actual structure of what the learner does, not just the topic. A lecture on retrieval practice can be a passive event (low desirable difficulty) or an active one (high desirable difficulty) depending on whether learners are quizzed, asked to generate examples, or simply read slides. The same content can be either desirable or undesirable depending on the surrounding practice structure.

Output: A structured list of 5-10 design elements extracted from the description.

---

### Step 2 — Apply Bjork's Two-Part Classification Test

For each difficulty element identified in Step 1, apply both tests:

**Test A — Does the effort strengthen encoding?**
Ask: Does this difficulty require the learner to actively reconstruct knowledge from long-term memory, generate a response, or make discriminations? If yes → potentially desirable. If the effort is purely about overcoming an obstacle unrelated to the skill being learned → undesirable.

**Test B — Can the learner overcome this difficulty?**
Ask: Does the learner have the prerequisite background knowledge and skills to respond to this difficulty successfully? If yes → desirable. If the difficulty exceeds the learner's current capacity to respond → undesirable.

**The critical distinction:** A difficulty is desirable when it triggers encoding and retrieval processes. It becomes undesirable when the learner cannot overcome it, when it does not strengthen the specific target skill, or when it creates anxiety that consumes working memory capacity instead of directing it toward learning.

**Undesirable difficulty markers — flag these for removal or redesign:**
- Difficulty caused by missing prerequisite knowledge (learner cannot engage because the gap is too large)
- Difficulty caused by poor presentation quality (confusing language, broken technology, inaccessible format) that is unrelated to the target skill
- Difficulty that induces test anxiety sufficient to disrupt performance (working memory consumed by self-monitoring)
- Difficulty that matches learning style preference but has no empirical support (e.g., requiring visual-only delivery for self-identified "visual learners")
- Difficulty that requires overcoming a physical or cognitive limitation unrelated to the skill (e.g., requiring dyslexic learners to decode complex text when the target skill is mathematical reasoning)

**WHY:** The Bjork framework distinguishes between difficulties that slow apparent progress while strengthening durable learning (desirable) and difficulties that simply impede without cognitive benefit (undesirable). The test of "does the effort succeed?" is the pivotal discriminator: unsuccessful effort in the face of an insurmountable obstacle does not produce learning. Both conditions must hold for a difficulty to qualify as desirable.

Output: A classification table: each difficulty element labeled DESIRABLE, UNDESIRABLE, or AMBIGUOUS with the specific test that determined the classification.

---

### Step 3 — Map to the Six-Strategy Taxonomy

For each difficulty classified as desirable in Step 2, identify which of the six named strategies it represents. For each strategy, note whether it is PRESENT, ABSENT, or PARTIAL in the current design.

See `references/six-strategy-taxonomy.md` for the full bilateral contrast table. Summary:

| Strategy | Core mechanism | Counterpart (ineffective) |
|----------|---------------|--------------------------|
| **Spacing** | Practice sessions separated by time, forcing reconstruction from long-term memory | Massed practice (cramming): draws on short-term memory, rapid improvement, rapid forgetting |
| **Interleaving** | Different topics or problem types mixed within a session, requiring discrimination | Blocked practice: one type at a time, feels productive, produces narrow skill that fails to transfer |
| **Variation** | Problems, scenarios, and contexts varied across practice sessions | Identical repetition: builds narrow pattern-matching, fails in novel contexts |
| **Retrieval practice** | Learner produces answers from memory before checking (testing effect) | Rereading / re-watching: creates familiarity illusion, not actual retrievability |
| **Generation** | Learner must produce a response, attempt a solution, or formulate an explanation before being given the answer | Passive reception: information presented without learner output requirement |
| **Elaboration** | Learner connects new knowledge to prior knowledge, gives examples, or explains why it is true | Isolated encoding: material presented in isolation without connection to existing knowledge structures |

**Presence scoring:**
- PRESENT: The design explicitly includes this strategy (e.g., quizzes before feedback = retrieval; randomized problem order = interleaving)
- PARTIAL: Some elements exist but inconsistently (e.g., end-of-module quiz but no spacing across sessions)
- ABSENT: No elements of this strategy appear in the design

**WHY:** Naming which strategy is present or absent converts a subjective critique ("this training seems passive") into a specific, actionable gap. Each absent strategy represents a concrete redesign opportunity. Partial presence is often more actionable than complete absence — it means the design already has the right structural idea but applies it narrowly.

Output: A 6-row strategy presence table.

---

### Step 4 — Identify Redesign Priorities

Rank the gaps from Step 3 by expected learning impact. Prioritize:

1. **Absent retrieval practice** — highest single-strategy impact on long-term retention. If learners never produce answers from memory, all other strategies are less effective.
2. **Absent spacing** — without time between sessions, retrieval cannot draw from long-term memory, undermining the mechanisms of all other strategies.
3. **Absent generation** — learners who only receive information without producing responses show weak transfer.
4. **Blocked practice / absent interleaving** — blocking creates narrow skill that fails to transfer to real-world variation.
5. **Absent variation** — produces rigid pattern-matching, especially problematic for professional and applied skills.
6. **Absent elaboration** — reduces integration with prior knowledge; new learning remains isolated and less retrievable.

For each priority gap, generate a specific redesign suggestion that fits the existing design format. Do not recommend radical structural changes when a small addition achieves the goal.

**Redesign suggestion format:**
> **Gap:** [Strategy absent or partial]
> **Current design element:** [What currently exists]
> **Redesign:** [Specific change to add the strategy]
> **Effort:** [Low / Medium / High — how much design work is required]
> **Expected impact:** [What improves and why]

**WHY:** Prioritization prevents the instructional designer from feeling overwhelmed. The redesign suggestions are ordered so that the highest-impact changes are addressed first. Adding retrieval practice to a passive lecture (e.g., three quiz questions at the end of each session) is a low-effort change with disproportionately high impact. The effort estimate helps designers triage.

Output: 3-6 prioritized redesign recommendations.

---

### Step 5 — Produce the Difficulty Analysis Report

Compile the outputs of Steps 1-4 into a structured report:

**Report sections:**
1. **Learning activity summary** — 2-3 sentence description of what was analyzed
2. **Classification table** — all difficulty elements with DESIRABLE / UNDESIRABLE / AMBIGUOUS labels
3. **Strategy presence table** — all six strategies with PRESENT / PARTIAL / ABSENT status
4. **Undesirable difficulty list** — specific elements to remove or redesign
5. **Prioritized recommendations** — 3-6 redesign suggestions in ranked order
6. **Screening questions for ongoing design** — 6 questions the designer can ask about any future learning element (see Step 6)

**WHY:** A structured report makes the analysis actionable and shareable. The classification table gives evidence for each finding. The strategy presence table shows the overall difficulty profile at a glance. The screening questions equip the designer to self-assess future designs without re-running the full analysis.

---

### Step 6 — Provide Screening Questions for Ongoing Design

Deliver these six questions to the instructional designer for use in future design reviews. They are derived from Bjork's classification framework and the six-strategy taxonomy:

1. **Does the learner produce a response from memory before receiving feedback?** (Tests retrieval practice — if no, add low-stakes quizzing or recall prompts)
2. **Is practice distributed across multiple sessions with gaps of at least one day?** (Tests spacing — if no, redesign the schedule to prevent massed practice)
3. **Are different topics or problem types mixed within sessions rather than blocked?** (Tests interleaving — if no, randomize problem order or alternate topic blocks)
4. **Does the learner encounter varied scenarios, examples, or problem formats across sessions?** (Tests variation — if no, diversify the practice set)
5. **Are learners asked to attempt a solution or generate an answer before the solution is revealed?** (Tests generation — if no, add pre-solution attempts, even for material not yet taught)
6. **Does the design ask learners to connect new material to what they already know or to explain it in their own words?** (Tests elaboration — if no, add reflection prompts or explanation exercises)

**Bonus undesirable difficulty screening question:**
7. **Does this difficulty require prerequisites the learner does not yet have?** (If yes → it is undesirable; address the prerequisite gap first)

**WHY:** Providing screening questions converts the classification framework into a self-service tool. A designer who has the questions does not need to re-engage the skill for every design decision — they can self-audit in minutes. The questions are written to produce a binary yes/no answer because ambiguous criteria are not used in practice.

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Learning activity description | Yes | What the learner does during practice or study |
| Target skill or knowledge | Yes | What success looks like after learning |
| Learner background | No (defaults to intermediate) | Prior knowledge and experience level |
| Course document or syllabus | No | File containing the full design structure |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Classification table | Inline markdown | All difficulty elements labeled DESIRABLE / UNDESIRABLE / AMBIGUOUS |
| Strategy presence table | Inline markdown | Six strategies with PRESENT / PARTIAL / ABSENT status |
| Redesign recommendations | Inline markdown | 3-6 prioritized, specific recommendations |
| Screening questions | Inline markdown | 7 questions for ongoing design self-audit |

---

## Key Principles

**1. Difficulty is not inherently good or bad — mechanism determines value**
The same activity can be a desirable or undesirable difficulty depending on whether it strengthens encoding and whether the learner can overcome it. A hard test given before the learner has any relevant knowledge is an undesirable obstacle. The same test given after initial instruction is a desirable retrieval event. The mechanism — not the felt difficulty — is what matters.

**2. Fluency is the enemy of durability**
Learning that feels easy, smooth, and productive is often the least durable. Rereading produces fluency (the text feels familiar) without retrievability (the learner cannot recall it without the text in hand). Massed practice produces performance gains (rapid improvement in the session) without long-term retention. Instructional designs that prioritize participant comfort consistently produce poor retention outcomes.

**3. The effort that succeeds is the effort that teaches**
Effortful retrieval that results in correct recall (with or without struggle) strengthens the memory trace. Effortful retrieval that fails because the difficulty is unsurmountable does not. The key is to calibrate difficulty to the learner's current level: enough to require reconstruction from long-term memory, not so much that the reconstruction fails entirely.

**4. All six strategies are additive**
The six desirable difficulty strategies are not mutually exclusive — they stack. A practice session that includes retrieval (quizzing from memory), spacing (scheduled one week after initial learning), interleaving (mixing problem types), and elaboration (explaining answers in own words) is dramatically more effective than any single strategy alone. Instructional designs should aim to incorporate multiple strategies rather than optimizing for one.

**5. Structure building requires difficulty**
Learners who are given information passively develop superficial familiarity. Learners who are required to generate, retrieve, and elaborate develop mental models — connected knowledge structures that enable transfer to new problems. The difficulty of constructing meaning cannot be shortcut; it is the mechanism of learning.

---

## Examples

### Example 1 — Corporate Onboarding Audit

**Input:** A new-employee onboarding program: Day 1 is a full-day lecture with slides covering company history, culture, and processes. Employees are given a manual to read. No assessment. Employees shadow a senior colleague for Day 2 and Day 3. Week 2 is independent work.

**Classification results:**
- Full-day lecture: UNDESIRABLE — passive reception with no retrieval requirement; massed (one day), no spacing
- Read-only manual: UNDESIRABLE — rereading analog; creates familiarity, not retrievability
- Shadowing: PARTIAL — observational, not generative; no retrieval or elaboration required
- Independent work (Week 2): DESIRABLE — real-world variation; generation required; implicit spacing from Day 1

**Strategy presence:**
- Retrieval practice: ABSENT
- Spacing: ABSENT (Day 1 lecture never revisited before independent work)
- Interleaving: ABSENT
- Variation: PARTIAL (Week 2 provides it)
- Generation: PARTIAL (Week 2 only)
- Elaboration: ABSENT

**Top recommendation:** Add three retrieval prompts at the end of Day 1: "Without looking at your notes, write down the three things from today that you'll need to do in your first solo task." Low effort, high impact.

---

### Example 2 — Medical Training Workshop

**Input:** A one-day continuing education workshop for physicians: Morning session is two hours of case presentations (attending presents, residents watch). Afternoon is small-group discussion of cases. Participants complete a satisfaction survey at the end.

**Classification results:**
- Case presentations (passive): UNDESIRABLE — observation only; no retrieval, no generation
- Small-group discussion: DESIRABLE — elaboration present (connecting to prior cases); generation partial (if participants must propose diagnoses before attending reveals it)
- Satisfaction survey: UNDESIRABLE difficulty marker (not a learning assessment)

**Strategy presence:**
- Retrieval practice: ABSENT
- Spacing: ABSENT (single-day event, no follow-up)
- Interleaving: PARTIAL (cases are varied topics)
- Variation: PRESENT (diverse cases)
- Generation: PARTIAL (discussion may require it, but not consistently)
- Elaboration: PARTIAL (discussion context encourages it)

**Top recommendation:** Restructure case presentations as retrieval events: present the case with findings, pause, ask participants to write their diagnosis before the attending reveals it. Same content, same time — but changes passive observation to active retrieval.

---

### Example 3 — Self-Study Method Audit

**Input:** A software developer studying for a certification exam: studies by watching tutorial videos twice through, then reads the official guide once. Exam is in four weeks.

**Classification results:**
- Re-watching videos: UNDESIRABLE — rereading analog; repeated exposure creates familiarity, not retrieval strength
- Reading official guide: UNDESIRABLE alone — passive encoding with no retrieval requirement

**Strategy presence:**
- Retrieval practice: ABSENT
- Spacing: ABSENT (all material consumed in a compressed initial period)
- Interleaving: ABSENT (one topic fully before moving to next)
- Variation: ABSENT (single source format)
- Generation: ABSENT
- Elaboration: ABSENT

**Assessment:** This method has zero desirable difficulty strategies. High effort with low expected retention. The learner will feel prepared (familiarity illusion) and underperform on the exam.

**Top recommendation:** Replace re-watching with self-quizzing. After watching each video once, close it and write down the five most important concepts from memory. Check against the video. Repeat for missed items only. This single change introduces retrieval practice, generation, and implicit spacing — three strategies at once.

---

## References

- `references/six-strategy-taxonomy.md` — Full bilateral contrast table for all six strategies with definitions, mechanisms, evidence summary, and counterpart descriptions
- `references/bjork-classification-criteria.md` — Detailed source notes on the Bjork framework for desirable vs. undesirable difficulty, with direct chapter citations

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
