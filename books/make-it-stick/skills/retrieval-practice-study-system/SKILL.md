---
name: retrieval-practice-study-system
description: Design a complete self-quizzing study system for any subject, course, or learning goal. Use this skill whenever the user wants to study more effectively, stop wasting time rereading notes, build a study schedule from learning material, prepare for exams, create flashcard decks with a spacing system, design a practice-quiz regimen, or turn any document into a retrieval-based learning plan — even if they don't mention "retrieval practice" or "spaced repetition." Works for students at any level, professionals upskilling, lifelong learners, and coaches designing training programs. Do NOT use this skill to evaluate whether a textbook or course is good (that is a different task), or to build automated quiz software (that requires a coding skill).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/retrieval-practice-study-system
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [2, 8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "study-skills", "self-testing", "active-recall"]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Study material, course outline, textbook chapters, lecture notes, or learning objectives"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
discovery:
  goal: "Design a complete retrieval-based study system — quiz questions, spacing schedule, mastery signals, and anti-pattern guide — so the learner can replace passive rereading with active self-testing."
  tasks:
    - "Analyze study material and extract key concepts, terms, and relationships"
    - "Generate a prioritized set of self-quiz questions (short-answer and concept-connection format)"
    - "Build a spaced repetition schedule calibrated to the content and timeline"
    - "Define mastery signals and a Leitner-style progression system"
    - "Produce a one-page anti-pattern comparison: retrieval practice vs. rereading"
  audience: ["students", "lifelong learners", "teachers", "trainers", "coaches"]
  triggers:
    - "I need to study for an exam"
    - "How do I make this material actually stick?"
    - "Create flashcards for this content"
    - "I keep rereading my notes but nothing is sticking"
    - "Build a study plan for this course"
    - "I want to learn this subject deeply, not just cram"
  not_for:
    - "Evaluating the quality of a course or textbook"
    - "Building quiz software or automated learning platforms"
    - "Summarizing a book (use a summarizer skill)"
  environment: "Document-based: study guides, lecture notes, course outlines, PDF chapters, learning objectives"
  quality:
    completeness_score:
    accuracy_score:
    value_delta_score:
---

# Retrieval Practice Study System

## When to Use

You have a body of material to learn and want to build a structured, science-backed study system. Typical situations:

- The user has a course, textbook, or document they need to master by a deadline
- The user is frustrated that rereading does not produce real retention
- The user wants flashcards but does not know how to space them or signal mastery
- The user needs a study schedule that goes beyond "review the night before"
- A teacher or trainer wants to design a low-stakes quiz regimen for their students

Before starting, verify:
- Is the study material available to read? (If not, ask the user to share it or describe it)
- What is the learning goal and timeline? (Exam date, job start date, presentation deadline)

**Mode: Hybrid** — The agent designs all study materials, question sets, and the schedule. The human executes the daily practice sessions.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Study material:** What must be learned? This is the source for generating questions.
  → Check for: uploaded files, linked documents, pasted notes, chapter summaries in the prompt
  → If missing, ask: "Please share the material you want to study — lecture notes, textbook chapters, or a course outline."

- **Learning goal:** What does mastery look like? This determines question depth.
  → Check for: exam format (multiple-choice, essay, practical), job competency requirements, certification criteria
  → If missing, ask: "What will you be tested on or need to do with this knowledge?"

- **Timeline:** When is the deadline or exam? This sets the spacing schedule.
  → Check for: dates mentioned in prompt, course syllabi, exam announcements
  → If missing, ask: "How much time do you have before you need to know this material?"

### Observable Context (gather from environment)

- **Existing notes or highlights:** Prior study attempts that reveal what the user already knows
  → Look for: annotated files, highlighted PDFs, previous flashcard decks
  → If unavailable: treat all material as new

- **Subject domain:** Affects question type (factual recall vs. concept-application vs. procedure)
  → Look for: course name, subject tags, discipline cues in the material

### Default Assumptions

- If no exam format specified → generate a mix: 60% short-answer, 40% concept-connection
- If no timeline specified → design a 4-week schedule with daily 20-minute sessions
- If no prior knowledge indicated → assume starting from zero

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
  ✓ Study material is available (or described in enough detail to generate questions)
  ✓ Learning goal is clear (what the learner must be able to do)
  ✓ Timeline is known (or default 4-week schedule is acceptable)
BLOCK if: no material and no description — cannot generate meaningful questions without content
```

## Process

### Step 1 — Analyze the Material and Extract Learning Targets

Read the study material and identify:
- **Key concepts:** Core ideas the learner must understand (not just recognize)
- **Critical terms:** Vocabulary with precise meanings that affect application
- **Relationships:** How concepts connect, cause each other, or contrast
- **Procedures:** Step-by-step processes or decision rules

**WHY:** Retrieval practice is most effective when questions target the deep structure of the material — the underlying principles — not just surface facts. Identifying learning targets first ensures the question set is prioritized, not exhaustive.

Output: A numbered list of 10-20 learning targets, ranked by importance to the learning goal.

---

### Step 2 — Generate the Self-Quiz Question Set

For each learning target, write 1-3 questions. Prefer:
- **Short-answer questions** that require the learner to produce the answer (not recognize it): "What happens to memory retention when retrieval is delayed by one week?"
- **Concept-connection questions** that require relating ideas: "How does spacing interact with retrieval practice to strengthen long-term memory?"
- **Application questions** that transfer learning to a new scenario: "A colleague is preparing a presentation. Which study strategy would you recommend and why?"

Avoid:
- True/false questions (recognition is weaker than recall)
- Questions answerable by a single memorized word

**WHY:** Research demonstrates that questions requiring the learner to produce an answer (short-answer, essay) yield significantly stronger long-term retention than recognition-based formats (multiple choice, true/false). The cognitive effort of generating an answer strengthens the neural pathway to that memory. When multiple-choice is necessary (e.g., matching a certification exam format), write questions with plausible distractors that require discrimination, not guessing.

**IF** the material is primarily procedural (e.g., a clinical protocol, a coding pattern):
→ Write sequence-recall questions: "List the steps of X in order" and error-identification questions: "What is wrong with this approach?"

**IF** the material is primarily conceptual (e.g., economic theory, learning science):
→ Weight toward explanation questions: "Explain why X happens" and comparison questions: "How does X differ from Y?"

Output: A question bank file (`quiz-questions.md`) with questions grouped by learning target.

---

### Step 3 — Build the Spacing Schedule

Construct a tiered review schedule based on the timeline and confidence level:

**Tier schedule (adjust for your timeline):**
- **Session 0 (Day 1):** Initial study of material + immediate self-quiz (all questions, no peeking)
- **Session 1 (Day 2-3):** Review all missed questions from Session 0 + skim correct ones
- **Session 2 (Day 5-7):** Quiz all questions again; retire cards answered correctly twice in a row to the "monthly" pile
- **Session 3 (Day 10-14):** Quiz remaining active questions; add any new material
- **Monthly review:** Pull the "retired" pile once a month and re-quiz — anything missed re-enters the active deck

**For short timelines (exam in under 2 weeks):**
- Compress to every-other-day quizzing
- Prioritize the highest-weight learning targets
- Do not retire cards until after the exam

**WHY:** Spacing practice — leaving time between retrieval sessions — forces the brain to reconstruct the memory from long-term storage rather than working memory. This reconstruction process, which feels effortful and even frustrating, is precisely what strengthens long-term retention. Research shows cramming produces 50% forgetting within two days; spaced practice reduces forgetting to 10% over the same period.

Output: A study calendar file (`study-schedule.md`) with specific dates, session content, and time estimates.

---

### Step 4 — Set Up the Leitner Box Progression

Organize flashcards (physical or digital) into 3-5 boxes with escalating review intervals:

| Box | Review frequency | Entry rule | Exit rule |
|-----|-----------------|------------|-----------|
| Box 1 (Active) | Every session | All new cards start here | Answered correctly once → Box 2 |
| Box 2 | Every other session | From Box 1 | Correct again → Box 3 |
| Box 3 | Once a week | From Box 2 | Correct again → Box 4 |
| Box 4 | Once a month | From Box 3 | Correct again → Box 5 |
| Box 5 (Mastered) | Once a semester / before high-stakes events | From Box 4 | Stays here unless missed → back to Box 1 |

**Critical rule:** If a card is answered incorrectly at any box level, it returns immediately to Box 1.

**WHY:** The Leitner system (a physical implementation of spaced repetition) ensures that difficult material receives more practice and easy material is not wasted on. The "any miss → Box 1" rule prevents the learner from self-deceiving about mastery — the moment a card is missed, it is treated as unlearned.

Output: Instructions for setting up the Leitner system in `study-schedule.md`, including the starting box assignment for all cards.

---

### Step 5 — Define Mastery Signals

Mastery for a given concept is declared when ALL of these are true:
1. The learner answers the question correctly **without hesitation** on 3 consecutive sessions
2. The learner can explain the concept **in their own words** (not by reciting the source text)
3. The learner can connect the concept to at least one other concept in the course
4. The concept has been in Box 4 or Box 5 for at least one review cycle

**Warning signals** (study is not working — change approach):
- Answering correctly immediately after reading but unable to recall 24 hours later → increase spacing interval
- Feeling confident but scoring below 70% on a practice test → the fluency illusion is active; reduce rereading and increase self-quizzing
- Unable to answer any question after a session → material is too complex; break learning targets into smaller sub-concepts

**WHY:** Without explicit mastery criteria, learners commonly experience the "fluency illusion" — the feeling of knowing that arises from familiarity with the text, not from actual command of the material. Familiarity is not retrievability. Defining mastery signals forces the learner to test their knowledge against objective criteria rather than subjective feeling.

Output: A mastery checklist section at the bottom of `study-schedule.md`.

---

### Step 6 — Produce the Anti-Pattern Comparison

Write a one-page summary contrasting retrieval practice with rereading, specific to the learner's material:

**Rereading (what feels productive but is not):**
- Highlights and color-coded notes create visual familiarity
- Fluency with the text mimics the feeling of understanding
- Results in 50-70% forgetting within one week
- Produces overconfidence: learners believe they know material they cannot recall

**Retrieval practice (what feels harder but works):**
- Self-quizzing feels awkward and slow — this discomfort is a signal it is working
- Effort during recall strengthens the memory pathway
- A single retrieval session boosts one-week retention by ~11%; three sessions "immunize" against forgetting
- Correcting wrong answers after a retrieval attempt produces better learning than never having tried

**WHY:** Learners who understand the mechanism are more likely to tolerate the discomfort of self-quizzing. The awkward feeling of struggling to recall is cognitively identical to the process that makes memories durable. Naming this feeling in advance reduces the temptation to abandon the system.

Output: Anti-pattern guide appended to `quiz-questions.md`.

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Study material | Yes | Text, notes, chapters, or course outline to learn |
| Learning goal | Yes | What the learner must be able to do with this knowledge |
| Timeline | Yes (or accept default 4-week) | Days until exam or competency is needed |
| Existing flashcards / notes | No | Prior study artifacts that can seed the question bank |
| Exam format | No | Affects question type weighting |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `quiz-questions.md` | Markdown | Full question bank grouped by learning target, with anti-pattern guide |
| `study-schedule.md` | Markdown | Day-by-day schedule, Leitner box setup, mastery checklist |

### Output Template: study-schedule.md

```markdown
# Study Schedule: [Subject]

**Learning goal:** [What you will be able to do]
**Exam / deadline:** [Date]
**Total sessions:** [N]

## Leitner Box Setup
- Box 1 (Active): [N] cards — review every session
- Box 2: [N] cards — review every other session
- Box 3: [N] cards — review weekly
- Box 4: [N] cards — review monthly
- Box 5 (Mastered): empty at start

## Session Calendar
| Date | Box(es) to quiz | Time estimate | Notes |
|------|----------------|---------------|-------|
| [Day 1] | All (Box 1) | 30 min | First pass — expect to miss most |
| [Day 2-3] | Box 1 (misses only) | 20 min | Focus on gaps |
| ... | ... | ... | ... |

## Mastery Checklist
For each learning target, check off when:
- [ ] Correct 3 consecutive sessions without hesitation
- [ ] Can explain in own words
- [ ] Can connect to at least one other concept
- [ ] In Box 4 or Box 5 for one full cycle
```

## Key Principles

**1. Retrieval, not review, is the learning event**
Reading creates familiarity; retrieval creates memory. After the first reading, every additional hour spent rereading yields far less retention than the same hour spent self-quizzing. The act of pulling a memory from storage — not the act of encoding it — is what makes it durable.

**2. Desirable difficulty: effortful = effective**
The discomfort of struggling to recall something is not a sign of failure; it is the mechanism of learning. Research consistently shows that more effortful retrieval produces stronger retention than easy retrieval. If self-quizzing feels smooth and easy, the spacing interval is probably too short.

**3. Spacing beats massing**
Distributing practice across days produces dramatically better long-term retention than the same amount of practice compressed into one session. The reason: spaced sessions require the brain to reconstruct the memory from long-term storage, reinforcing the neural pathway each time. Cramming draws from short-term memory and fades quickly.

**4. Errors are learning events, not failures**
Getting a question wrong, then checking the correct answer and trying again, produces better learning than never having made the error. Wrong answers followed by corrective feedback are more effective than rereading alone. Do not avoid questions you expect to miss — seek them out.

**5. Calibration beats confidence**
The fluency illusion (feeling like you know material because you can read it fluently) is one of the most reliable predictors of exam failure. Self-quizzing provides an objective measure of what you actually know, not what you feel you know. Use quiz scores, not reading speed or highlighting volume, to guide study decisions.

**6. Interleaving deepens discrimination**
Mixing study of different topics or problem types — rather than blocking one topic at a time — helps the brain learn to identify which approach applies to which situation. This is harder and slower than blocked practice but produces superior transfer to new problems.

## Examples

### Example 1: Medical Student Preparing for a Physiology Exam

**Scenario:** A first-year medical student has four weeks before a comprehensive physiology exam. The course covers twelve organ systems. After two weeks of rereading notes and highlighting textbooks, they scored 65 on a practice exam. They need to change their approach.

**Trigger:** "I have a physiology exam in four weeks. I've been rereading my notes but not retaining anything. Help me study."

**Process:**
1. Agent reads the student's notes and identifies 60 learning targets across the twelve systems
2. Agent generates a 90-question bank weighted toward concept-connection and mechanism questions (e.g., "Trace the pathway by which decreased blood pressure triggers aldosterone release")
3. Agent builds a 4-week spaced schedule: daily 25-minute sessions in weeks 1-2, 30-minute sessions in weeks 3-4 with backward-reaching review
4. Agent sets up a 4-box Leitner system and designates mastery criteria for each organ system
5. Agent writes an anti-pattern guide specific to physiology: why reading the textbook description of the cardiac cycle is not the same as being able to describe it

**Output:** `quiz-questions.md` (90 questions, grouped by system) and `study-schedule.md` (28-day calendar, Leitner assignments, mastery checklist)

---

### Example 2: Professional Upskilling in Data Systems

**Scenario:** An engineer wants to deeply learn distributed systems concepts from a technical book. They have 6 weeks, no fixed exam, but a system design interview in 42 days. They've been reading chapters but feel like concepts slip away within a day.

**Trigger:** "I'm reading a technical book on distributed systems for a system design interview. Nothing is sticking. Can you build me a study system?"

**Process:**
1. Agent reads the chapter summaries and identifies 35 learning targets (replication strategies, consensus protocols, storage engines, etc.)
2. Agent generates a 50-question bank mixing definition recall ("What is the difference between strong and eventual consistency?") and application questions ("You are designing a leaderboard for a global gaming platform. Which consistency model would you choose and why?")
3. Agent builds a 6-week schedule with interleaving across topic areas (storage + replication + consistency alternated, not blocked)
4. Agent sets up a 3-box Leitner system (simpler, given the timeline) and defines mastery as "able to explain the concept whiteboard-style without notes"

**Output:** `quiz-questions.md` and `study-schedule.md` optimized for interview preparation

---

### Example 3: Teacher Designing a Classroom Retrieval System

**Scenario:** A middle school social studies teacher wants to integrate low-stakes quizzing into their unit on ancient civilizations. They have 8 weeks of unit material and want a system that does not feel punitive to students.

**Trigger:** "I'm a teacher. Help me design a quiz system for my ancient civilizations unit that helps students retain information without stressing them out."

**Process:**
1. Agent reads the unit outline and identifies 40 learning targets across Egypt, Mesopotamia, India, and China
2. Agent generates a bank of 80 short-answer questions suitable for classroom use, with 3 quiz sets of approximately 5 questions each (pre-lesson, post-lesson, pre-exam)
3. Agent builds an 8-week schedule with three quiz points per unit chapter: beginning of class (prior reading), end of class (today's lesson), and 24 hours before the chapter test
4. Agent writes teacher notes explaining the 79%-vs-92% research result (Columbia Middle School science study) and how to frame quizzes to students as "practice, not a grade"
5. Agent produces a student-facing anti-pattern card explaining why rereading notes feels productive but is not

**Output:** `quiz-questions.md` (80 questions in three quiz sets) and `study-schedule.md` (8-week calendar with classroom timing)

---

## References

- `references/research-evidence.md` — Key empirical studies: testing effect research (1917, 1939, 1978, 2005 Columbia Middle School, 2007 eighth-grade science), forgetting curve data, cramming vs. spacing retention comparisons
- `references/leitner-system-guide.md` — Full Leitner box implementation guide including physical card setup and digital app equivalents
- `references/mastery-signals.md` — Extended mastery criteria for different subject types (procedural, conceptual, declarative)
- `references/anti-patterns.md` — Full comparison of 6 ineffective study strategies vs. retrieval practice alternatives

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
