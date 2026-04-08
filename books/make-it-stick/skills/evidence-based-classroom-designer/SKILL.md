---
name: evidence-based-classroom-designer
description: |
  Design or redesign any course, class, or training session using evidence-based instructional principles. Use this skill when a teacher, instructor, or instructional designer wants to improve student retention and achievement through classroom design, course design, quiz design, or active learning strategies — even if they don't mention "retrieval practice" or "spaced repetition." Triggers include: instructor wants to reduce failure rates in a gateway course; teacher finds students forget material within days of a lecture; instructor relies on midterm and final exams as the only assessment; teacher wants to move from passive lecturing to active learning without losing content coverage; instructor wants to close the achievement gap between well-prepared and under-prepared students; course designer wants to embed low-stakes quizzing into a curriculum; teacher wants to raise student performance on Bloom's higher-order thinking levels; instructor wants to redesign student engagement without adding complexity. Works for K-12 teachers, university professors, corporate trainers, and instructional designers. Do NOT use this skill to build a personal study system for a single learner (use retrieval-practice-study-system), to create a practice schedule alone (use practice-schedule-designer), or to audit a single learning activity for difficulty structure (use desirable-difficulty-classifier).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/evidence-based-classroom-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "teaching", "classroom-design", "instructional-design", "course-design", "quiz-design", "active-learning", "student-engagement"]
depends-on:
  - retrieval-practice-study-system
  - practice-schedule-designer
  - desirable-difficulty-classifier
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Course syllabus, lesson plan, curriculum outline, or description of the current course structure and assessment approach"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access. Instructor provides course details or uploads a syllabus."
discovery:
  goal: "Audit the current course design against 6 evidence-based criteria, then apply a 4-part teacher protocol to produce a concrete redesigned course plan with an assessment calendar, specific intervention designs, and a transparency script for students."
  tasks:
    - "Gather course details: subject, level, class size, frequency, current assessment structure"
    - "Audit current design against the 6-criteria learning environment checklist"
    - "Apply the 4-part teacher protocol (explain, teach, create difficulties, be transparent)"
    - "Design specific interventions: quiz schedule, reflection exercises, interleaving plan, Bloom's audit"
    - "Produce redesigned course plan with assessment calendar and student transparency script"
  audience: ["K-12 teachers", "university instructors", "corporate trainers", "instructional designers", "curriculum coordinators"]
  triggers:
    - "Students are forgetting material within days of a lecture"
    - "The only assessments are a midterm and a final exam"
    - "Failure rates in a gateway course are too high"
    - "I want to move from lecturing to active learning"
    - "I want to close the achievement gap in my class"
    - "I need to embed low-stakes quizzing into my curriculum"
    - "My students don't retain what they learn"
    - "I want to redesign my course for better student engagement"
  not_for:
    - "Building a personal study system for a single learner (use retrieval-practice-study-system)"
    - "Designing a spacing schedule only (use practice-schedule-designer)"
    - "Auditing a single learning activity (use desirable-difficulty-classifier)"
  environment: "Course-level: syllabus, lesson plan, assessment calendar, or instructor description of current course structure"
  quality:
    completeness_score:
    accuracy_score:
    value_delta_score:
---

# Evidence-Based Classroom Designer

## When to Use

You are an instructor, teacher, or course designer who wants to improve how much students actually learn and retain — not just how much is covered. Typical situations:

- Your gateway course has high failure or withdrawal rates, and you suspect the problem is the assessment structure, not the students
- Students perform adequately on exams but forget the material within days — they're cramming, not learning
- Your course relies on high-stakes midterm and final exams as the only practice and feedback mechanism
- You want to introduce active learning but don't know which specific interventions are worth the effort
- You teach a high-structure discipline (biology, engineering, economics) and want to help under-prepared students succeed without lowering standards

Before starting, verify:
- Is a course outline, syllabus, or description of the current course structure available? (If not, ask the instructor to describe the course: subject, level, class size, number of meetings, current assessments)
- What is the instructor's primary concern? (Failure rates, retention, engagement, achievement gap, workload?)

**Mode: Hybrid** — The agent designs the course structure, intervention calendar, and transparency materials. The instructor executes and adapts them to their specific classroom.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Course description:** Subject, level (K-12 / university / professional), class size, meeting frequency, total duration
  → Check for: uploaded syllabus, course outline, pasted description
  → If missing, ask: "Please describe your course: what subject, what level, how many students, how often do you meet, and how long does the course run?"

- **Current assessment structure:** What assessments exist? When are they scheduled? What weight do they carry?
  → Check for: exam dates in syllabus, grading breakdown table, assignment list
  → If missing, ask: "How are students currently graded? What assessments exist, and when do they happen?"

- **Primary concern:** What is not working, or what does the instructor want to improve?
  → Check for: explicit problem statement in the prompt ("students forget," "high failure rate," "passive lectures")
  → If missing, ask: "What problem are you trying to solve with this redesign?"

### Observable Context (gather from environment)

- **Subject type:** Affects intervention design (procedural vs. conceptual vs. declarative material)
  → Look for: course name, discipline cues, learning objectives in syllabus

- **Existing active-learning elements:** Prior attempts at quizzing, group work, or reflection exercises
  → Look for: in-class activities section of syllabus, assignment descriptions

### Default Assumptions

- If class size is not specified → design for a class of 25-40 (adjust if instructor clarifies)
- If no assessment structure provided → assume two high-stakes exams (midterm + final), no low-stakes practice
- If no primary concern specified → focus on the most common problem: low-stakes practice is absent and students rely on cramming

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
  ✓ Subject and level are known
  ✓ Current assessment structure is described (or default assumption is acceptable)
  ✓ Primary concern or goal is stated
BLOCK if: no subject and no description — cannot design interventions without knowing what students are learning
```

---

## Process

### Step 1 — Gather Course Profile

Collect and record:
1. **Course basics:** Subject, level, class size, meeting frequency (e.g., 3x/week × 15 weeks), total seat time
2. **Learning objectives:** What must students be able to do by the end? At what cognitive level (recall, application, analysis, synthesis)?
3. **Current assessment calendar:** When do assessments occur? What types? What percentage of grade?
4. **Current in-class structure:** Lecture-only? Group work? Discussion? Problem sets?
5. **Student population:** Are they primarily well-prepared, mixed, or under-prepared? Are there equity concerns?

**WHY:** Intervention design must be calibrated to the specific constraints of the course. A 25-person seminar meeting twice a week calls for different mechanics than a 200-person lecture hall meeting three times a week. Gathering specifics first prevents generic recommendations that cannot be implemented.

Output: A course profile summary (3-5 sentences) confirmed with the instructor before continuing.

---

### Step 2 — Audit Current Design Against 6 Criteria

Evaluate the current course against each criterion. Rate each: **Present / Partial / Absent.**

| Criterion | What to look for | Research basis |
|-----------|-----------------|----------------|
| **C1. Low-stakes retrieval practice** | Frequent quizzes, self-tests, or recall exercises that occur during the course (not only at midterm/final) | Testing effect: retrieval consolidates learning and arrests forgetting. Quizzed material retained at 92% vs 79% for non-quizzed in Columbia IL study |
| **C2. Spaced and cumulative review** | Assessments or exercises that reach back to prior material — not only the most recent unit | Spacing forces reconstruction from long-term memory, strengthening the neural pathway. Cumulative quizzing builds complex mental models |
| **C3. Interleaving across topics** | Topics or problem types mixed across sessions rather than blocked by unit | Interleaving requires students to "reload" prior knowledge and identify which approach applies, building discrimination and transfer |
| **C4. Consequences (low-stakes)** | Practice exercises count toward the course grade, even at very low weight | Students in graded low-stakes practice classes outperform students in classes where the same exercises are ungraded |
| **C5. Transparency about how learning works** | Instructor explicitly explains why desirable difficulties are used and what the research shows | Students who understand the mechanism tolerate the discomfort of effortful practice and persist longer |
| **C6. Calibration feedback** | Students receive timely feedback that reveals what they know vs. what they think they know | Without calibration, students rely on fluency illusions and study the wrong material. The "illusion of knowing" is the primary cause of exam failure despite adequate study time |

For each criterion rated **Partial** or **Absent**, note the specific gap (e.g., "C1 absent: only two exams, no in-class quizzing").

**WHY:** Most course designs fail on C1 and C2 — they schedule high-stakes practice too infrequently and too late. Students in low-structure courses (lecture + two exams) have no mechanism to discover gaps before the exam, no incentive to practice distributed retrieval, and no feedback on whether their self-assessed confidence matches actual mastery. The audit makes the specific gaps visible before designing interventions.

For detailed difficulty classification across all six strategies (including generation, elaboration, variation), invoke `desirable-difficulty-classifier` OR apply the 6-criteria audit above directly.

Output: A filled audit table with Present/Partial/Absent ratings and gap notes.

---

### Step 3 — Apply the 4-Part Teacher Protocol

Apply each of the four protocol elements to the specific course. For each, produce a concrete implementation plan — not just a principle.

#### Protocol Part 1: Explain How Learning Works

Design a brief transparency module to deliver at the start of the course (or first class). Include:

- **The testing effect:** Explain that retrieval practice — not rereading — produces durable learning. Students who quiz themselves retain far more than students who reread the same content.
- **Desirable difficulties:** Explain that the discomfort of struggling to recall something is not a signal of failure — it is the mechanism of learning. If quizzing feels easy, the interval is too short.
- **Growth mindset tie-in:** Explain that intellectual ability is not fixed. Effortful learning changes the brain. Setbacks are information, not verdicts.
- **Course-specific preview:** Tell students exactly which practices in this course are intentionally difficult and why (e.g., "The daily quizzes in this course are harder than you might expect. That difficulty is the point.").

*Example — Wenderoth's framing:* "The whole idea of the testing effect is that you learn more by testing yourself than by rereading. I know this contradicts how most of you study. So I'm going to model it in class, and I'm going to show you your results over the semester so you can see it working."

**WHY:** Students who understand the mechanism tolerate the discomfort of effortful practice and persist longer. Students who don't understand it interpret quiz difficulty as unfairness and disengage. Wenderoth's research shows that students who are told they "have the illusion of knowing" and understand what that means come to her with solvable problems rather than complaints about trick questions.

#### Protocol Part 2: Teach Students How to Study

Design at least two study strategies to explicitly teach (not just recommend):

- **Free recall exercise:** Assign students to spend 10 minutes at the end of each class writing everything they remember from that session — without notes. Then check their notes and identify gaps. *Wenderoth assigns this daily; it guides what students bring to the next class.*
- **Testing groups (not study groups):** Restructure any group work so the group wrestles with a question together — books closed — rather than having the most knowledgeable person explain to the others. *Wenderoth finds that testing groups build exploration and understanding; study groups build dependency.*
- **Summary sheets:** Assign a weekly synthesis artifact — a single page illustrating the week's material with connections, arrows, and key ideas. This forces synthesis across a week of content before it fragments. *Wenderoth uses cartoon-style physiology sheets; the format can be adapted to any discipline.*

For detailed retrieval practice implementation for individual students, invoke `retrieval-practice-study-system` OR apply the free recall and self-quizzing pattern above directly.

**WHY:** Students are not taught how to study effectively and tend toward the least effective strategies (rereading, highlighting). Explicitly modeling correct study technique — rather than assuming students know it — is a prerequisite for the active-learning interventions in the course to work. Students who don't know how to retrieve cannot benefit from a high-structure course.

#### Protocol Part 3: Create Desirable Difficulties in the Classroom

Design 3-5 specific interventions drawn from the following menu. Select based on the audit gaps (Step 2) and the course constraints.

**Intervention A — Daily or bi-weekly low-stakes quizzes**
- Format: 3-5 questions at the start or end of class; closed notes; short-answer preferred over multiple-choice
- Timing: Every class, or every other class — not only at exam time
- Content: Mix current material with material from 2-3 sessions ago (cumulative reach-back)
- Grading: Count toward course grade at very low weight (e.g., 15-20% total, drop 3-4 lowest)
- Ground rules (critical): Set clear rules at the start of term — e.g., 4 free absences, no makeups; students either take it or they don't. This prevents negotiation overhead that makes quiz systems unsustainable.

*Example — McDermott (Washington University):* 4-question quiz in the last 3-5 minutes of every class meeting (28 meetings, 2×/week). Anything covered to date is fair game. Students drop 4 quizzes; no makeups. Quizzes = 20% of grade. By end of semester, students report quizzes helped them keep up and discover gaps early.

*Example — Sobel (political economics):* Cumulative low-stakes quizzing throughout the term. Each quiz can draw from any material covered so far. Students build incrementally complex mental models rather than cramming disconnected units.

**Intervention B — Pre-class generation exercises**
- Before the class where a new concept is taught, assign a brief problem or question the students cannot yet fully solve
- Students wrestle with the problem before seeing the solution; they arrive primed to receive instruction
- This "generation effect" produces stronger encoding than reading the explanation first

*Example — Matthews/West Point Thayer method:* Students read for specific learning objectives before each class; class opens with a quiz on those objectives; then students "take to the boards" — higher-order questions requiring integration, worked at the board in groups; one student per group gives a recitation to the class. Zero lecture. The grade rests on consistent daily participation.

**Intervention C — Board work and active recitation**
- Assign student groups to work through higher-order questions at the board (or equivalent: whiteboard apps, shared documents)
- One student per group explains the group's answer to the class — recitation, not just written output
- Keep questions at analysis/synthesis level (Bloom's level 4-6), not just recall

**Intervention D — Bloom's taxonomy answer keys**
- For each major exam or assessment, provide a Bloom's-level answer key: one answer for knowledge-level recall, a more complete answer for comprehension, a deeper answer for analysis, and the strongest answer for synthesis/evaluation
- Ask students to locate where their answer fell on the taxonomy and identify what they would need to know to reach the next level

*Example — Wenderoth:* Students receive the Bloom's key with their graded tests. They identify their level for each answer. The exercise shifts the question from "did I get it right?" to "at what level did I understand this?" and produces a specific, actionable study target.

**Intervention E — Learning paragraphs (periodic writing)**
- Once or twice a month, pose a synthesis question at the end of class ("How is X like Y?", "You just got your test back — what would you do differently?")
- Students write a 5-6 sentence response. Low stakes. Collect and read; comment in the next class so students know they were read.
- Purpose: stimulate retrieval and reflection before the week's learning is lost; give science or technical students deliberate writing practice.

**Designing the spacing and interleaving structure:**

For detailed spacing and interleaving schedule design across topics, invoke `practice-schedule-designer` OR apply this pattern directly:
- Map topics across the course timeline; identify where topics are currently blocked (all of Topic A, then all of Topic B)
- Restructure to alternate: introduce Topic A, introduce Topic B, return to Topic A at a higher complexity level, return to Topic B, etc.
- In physical or life sciences: align this with the vertical curriculum structure (e.g., Columbia IL: six simple machines in middle school → underlying physics in high school → applied engineering problem solving later)

**WHY:** Research consistently shows that students in high-structure classes (daily/weekly low-stakes practice) outperform students in low-structure classes (lecture + two exams) — and the gap is largest for under-prepared students. The key finding from Wenderoth's biology experiments: high-structure classes significantly reduced failure rates in gateway biology while simultaneously raising performance on Bloom's higher-order levels. The mechanism is that low-structure courses leave students to self-regulate their study, and most students self-regulate poorly until they have been taught otherwise.

#### Protocol Part 4: Be Transparent Throughout

Ongoing transparency (not just at the start of the course):

- After each quiz, briefly explain why you designed the question the way you did
- When students struggle with a difficult question, name the difficulty: "This question is designed to be hard to recall — that difficulty is producing stronger encoding right now"
- When quiz grades disappoint, redirect from blame to calibration: "This tells you something accurate about what you know. That's the point of doing this now rather than at the final exam."
- Reference student language: if a student says "that was a trick question," use it as a teaching moment about the illusion of knowing. *Wenderoth's observation: students who understand the illusion of knowing come to office hours with solvable problems, not complaints.*

**WHY:** Transparency is not a one-time orientation. The discomfort of effortful practice recurs throughout the semester, and students need a recurring framework for interpreting that discomfort as signal rather than failure. Without ongoing explanation, students who struggle will attribute difficulty to bad teaching rather than effective learning design.

---

### Step 4 — Design Specific Interventions

Based on the audit results and the 4-part protocol, produce:

**4a. Quiz schedule design**
- How many quizzes, at what frequency, on what content reach-back window
- Ground rules (free misses policy, no-makeup rule, weighting)
- Sample questions for the first 3 quizzes that demonstrate the cumulative reach-back pattern

**4b. Reflection exercise plan**
- Which reflection exercises to use (free recall, learning paragraphs, summary sheets)
- When in the class period they occur and how long they take
- How they are collected or reported (written, verbal, whiteboard)

**4c. Interleaving plan**
- A revised topic sequence showing where topics are interleaved rather than blocked
- Identification of which topics have natural conceptual connections that make interleaving high-value

**4d. Bloom's level design**
- For at least one major assessment: a Bloom's-level answer key template showing what a knowledge-level, comprehension-level, and analysis-level answer looks like for one representative question
- Instructions for distributing this key to students post-assessment

**WHY:** Without concrete artifacts — a quiz schedule, a sample question set, an interleaving map — instructors revert to their existing structure because it is familiar and low-effort. The interventions must be specifiable enough to execute in the first week of class.

---

### Step 5 — Produce Redesigned Course Plan and Assessment Calendar

Produce a complete redesigned course plan including:

1. **Transparency module** (first class): 10-15 minute script or outline explaining the testing effect, desirable difficulties, and how learning works
2. **Assessment calendar** (full course): When each type of assessment occurs (quiz, exam, reflection exercise, summary sheet), what it covers, and its grade weight
3. **Intervention calendar** (weekly): For each week of the course, which specific interventions occur (e.g., Week 3: 2 quizzes with reach-back to Week 1; board exercise on Topic B; summary sheet due Monday)
4. **Ground rules document**: The course-level policies for low-stakes practice (free misses, no-makeup rules, weighting)
5. **Student-facing explanation**: A 1-paragraph explanation for the syllabus or first-day handout that tells students why the course is designed the way it is

**WHY:** The goal is a course design that can be handed to another instructor and implemented without additional planning. Generality disappears at the level of execution; specificity is what makes redesign actionable.

Output: Write the redesigned course plan to `redesigned-course-plan.md`.

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Course description | Yes | Subject, level, class size, meeting frequency, duration |
| Current assessment structure | Yes (or default assumed) | What assessments exist, when, what weight |
| Primary concern or redesign goal | Yes | What is not working or what the instructor wants to improve |
| Course syllabus or outline | Preferred | The document to audit and redesign |
| Student population description | No | Mix of prepared/under-prepared; equity concerns |

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `redesigned-course-plan.md` | Markdown | Full redesigned course plan with all 5 components from Step 5 |

### Output Template: redesigned-course-plan.md

```markdown
# Redesigned Course Plan: [Course Name]

**Instructor:** [Name or role]
**Course:** [Subject, level, class size, meeting frequency]
**Primary concern addressed:** [e.g., "High failure rate in gateway biology"]
**Redesign date:** [Date]

## Design Audit Results

| Criterion | Rating | Gap |
|-----------|--------|-----|
| C1. Low-stakes retrieval practice | Present / Partial / Absent | [gap note] |
| C2. Spaced and cumulative review | Present / Partial / Absent | [gap note] |
| C3. Interleaving across topics | Present / Partial / Absent | [gap note] |
| C4. Consequences (low-stakes) | Present / Partial / Absent | [gap note] |
| C5. Transparency about learning | Present / Partial / Absent | [gap note] |
| C6. Calibration feedback | Present / Partial / Absent | [gap note] |

## Interventions Selected

[List of 3-5 interventions from Step 3, with brief rationale for each]

## Transparency Module (First Class)

[10-15 minute outline or script]

## Assessment Calendar

| Week | Assessment | Type | Covers | Grade weight |
|------|-----------|------|--------|-------------|
| 1 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

## Weekly Intervention Calendar

| Week | Quizzes | Reflection exercises | Board work | Other |
|------|---------|---------------------|------------|-------|
| 1 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

## Ground Rules Document

[Policies for low-stakes practice: free misses, no-makeup rule, weighting]

## Student-Facing Explanation (for Syllabus)

[1 paragraph]
```

---

## Key Principles

**1. Low-stakes retrieval practice is the highest-leverage classroom intervention**
The single most impactful change a teacher can make is to add frequent, low-stakes retrieval practice — quizzes that happen during the course rather than only at the end. The Columbia, Illinois middle school study found 92% retention on quizzed material vs. 79% on non-quizzed material in the same class. McDermott's university course achieves this with 4 questions in the last 5 minutes of every class meeting. The investment is minimal; the learning gain is substantial.

**2. High-structure courses close achievement gaps**
Wenderoth's biology experiments show that high-structure classes (daily and weekly low-stakes exercises) significantly reduce failure rates in gateway biology courses while simultaneously raising Bloom's-level performance. The gap narrows most for under-prepared students — those without a prior history of effective learning habits. High-structure is not remediation; it is structure that helps all students and helps struggling students most.

**3. Consequences matter, even at very low stakes**
Students in courses where practice exercises count toward the grade — even at minimal weight — outperform students in the same course where the exercises carry no consequences. The exercises being identical means the difference is purely in motivation to engage. Low-stakes grading is not coercive; it is the signal that the exercises are real, not optional.

**4. Transparency is a design element, not a nice-to-have**
When students understand why effortful retrieval feels uncomfortable and why that discomfort signals learning, they tolerate it and persist. When they don't understand it, they interpret difficulty as unfairness and disengage. Transparency is not soft pedagogy — it changes the behavioral response to difficulty and determines whether the rest of the course design can work.

**5. The Thayer method proves high-structure scales across disciplines**
West Point's Thayer method — specific learning objectives before every class, daily quizzing at the start, board work on higher-order questions, student recitation — has been sustained across almost 200 years and multiple disciplines. Matthews's courses run with essentially zero lecturing. The method works best for students who need structure to develop study discipline, and it scales from elite academies to Riverside Military Academy's more varied student population.

**6. Cumulative reach-back builds the mental model, not just the fact list**
Sobel's cumulative quizzing approach allows any quiz to draw from any material covered to date. This is not review for review's sake — it is the design mechanism that forces students to build connections between concepts over the course of the term, producing complex mental models rather than isolated fact recall. The final exam is never a shock because the student has been practicing toward it all semester.

---

## Examples

### Example 1: University Gateway Biology Course (High Failure Rate)

**Scenario:** A biology professor teaches a 150-student introductory biology lecture course that serves as a gateway requirement. Failure and withdrawal rates are around 30%. The course currently has 2 midterms and a final exam, weekly readings, and a lab section. Most students rely on cramming.

**Audit result:** C1 absent (no low-stakes quizzing), C2 absent (exams are not cumulative), C3 partial (topics are sequential, not interleaved), C4 absent (no graded practice), C5 absent (no explanation of learning principles), C6 partial (exams provide calibration, but too infrequently).

**Redesign interventions selected:**
- Weekly 5-question quiz (cumulative, 20% of grade, 3 lowest dropped)
- Daily free recall exercise: 10 minutes at end of lecture, written, no notes
- Bloom's answer keys distributed with each graded exam
- Transparency module in week 1 (testing effect + growth mindset)
- Summary sheets due every Monday (illustrate prior week's material)

**Expected outcome (based on Wenderoth's results):** Statistically significant reduction in failure rates; higher-order thinking scores on exams improve; under-prepared students show the largest gains.

---

### Example 2: High School History (Passive Lecture Problem)

**Scenario:** A high school history teacher with 28 students finds that students are disengaged during lectures and score poorly on unit tests despite apparently paying attention. The course has 8 unit tests across the year, plus a final. No quizzing between tests.

**Audit result:** C1 absent, C2 absent (unit tests are not cumulative), C3 absent (one unit at a time, fully blocked), C4 absent, C5 absent, C6 partial.

**Redesign interventions selected:**
- Bi-weekly 3-question quiz (reach back 2 units, 15% of grade, 2 lowest dropped)
- Board exercise: students assigned to groups, each answers a synthesis question on whiteboards ("How did the economic causes of WWI compare to those of WWII?") — one student explains to the class
- Vertical topic curriculum: re-expose earlier units at greater complexity as year progresses
- First-class transparency module with student-friendly language

**Assessment calendar shift:** From 8 disconnected unit tests to 8 unit tests + 14 bi-weekly quizzes with cumulative reach-back + 4 synthesis writing exercises.

---

### Example 3: Corporate Professional Training (Post-Workshop Forgetting)

**Scenario:** A corporate L&D team runs a two-day sales training workshop for 40 new agents. Participants rate the sessions highly, but sales managers report that skills and knowledge are not visible in behavior 30 days later. The team suspects the workshop format — intensive lecture + role play, then nothing — is the problem.

**Audit result:** C1 absent (no retrieval practice after the workshop), C2 absent (no spaced review), C3 partial (topics covered across 2 days but not interleaved), C4 absent (no consequences for post-workshop engagement), C5 absent, C6 absent.

**Redesign interventions selected:**
- Replace the final half-day of the workshop with a generation exercise: participants work on a real case before the solution is presented
- Schedule 3 follow-up quiz modules at 1 week, 3 weeks, and 6 weeks post-workshop (mobile-delivered, 5 questions each, draws from workshop + prior quiz content)
- Brief transparency segment on day 1 of the workshop: explain why the difficult generation exercise is the point, not an obstacle
- Interleave the four training topics (sales, marketing systems, business planning, brand advocacy) across both days rather than covering each in sequence — adapted from Farmers Insurance's new-agent training model

**Expected outcome:** Knowledge and skills are visible in behavior at 30 and 60 days because the design includes distributed retrieval practice after encoding, not only during it.

---

## References

- `references/case-studies.md` — Detailed case studies: Wenderoth (University of Washington biology), Matthews/Thayer method (West Point), McDermott (Washington University), Sobel (political economics), Columbia IL school district results
- `references/bloom-taxonomy-implementation.md` — Bloom's taxonomy levels with classroom examples, Wenderoth's answer key template, question classification guide for creating higher-order quiz items
- `references/design-checklist.md` — Printable 6-criteria course design checklist with rating scale and redesign prompt for each criterion
- `references/transparency-scripts.md` — Sample first-class transparency scripts for university (biology/sciences), high school (humanities), and corporate training contexts; student-facing language for syllabi

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-retrieval-practice-study-system`
- `clawhub install bookforge-practice-schedule-designer`
- `clawhub install bookforge-desirable-difficulty-classifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
