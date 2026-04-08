---
name: learning-practice-auditor
description: |
  Audit any set of study habits, training program, or course design for ineffective learning practices and replace them with evidence-based alternatives. Use this skill when someone wants a study habits audit, suspects they are making learning mistakes, reports that their studying is not working, relies on rereading, highlighting, or cramming, wonders whether their training design actually produces learning, or asks "what am I doing wrong?" Also triggers on: ineffective studying complaints, rereading concerns, learning styles assumptions, cramming before an exam, blocked practice schedules, highlighting as primary review method, "I study for hours but nothing sticks," or any study strategy review. Works for individual learners, teachers, corporate trainers, instructional designers, and coaches. Detects five named anti-patterns — rereading trap, massed practice delusion, illusions of knowing cluster, learning styles myth, errorless learning myth — with mechanism explanations, severity ratings, and direct routing to the corrective skill. Do NOT use this skill to build a study schedule (use retrieval-practice-study-system), to design a practice sequence (use desirable-difficulty-classifier), or to calibrate mastery confidence (use learning-calibration-audit) — this skill diagnoses the problem and routes to those solutions.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/learning-practice-auditor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [1, 2, 3, 5, 6]
tags:
  - learning-science
  - cognitive-psychology
  - evidence-based-learning
  - learning-audit
  - anti-patterns
  - study-habits
depends-on:
  - retrieval-practice-study-system
  - desirable-difficulty-classifier
  - learning-calibration-audit
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: description
      description: "Description of current study habits, training design, or learning approach — can be a verbal description, a course outline, a study schedule, or a list of current practices"
  tools-required: []
  tools-optional: [Read, Write]
  mcps-required: []
  environment: "Any agent environment. Works from a verbal description or a document. No file access required."
discovery:
  goal: "Identify which ineffective learning practices are present, classify each by name and severity, explain the mechanism that makes each feel effective but produces weak retention, and route to the appropriate corrective skill."
  tasks:
    - "Gather the learner's or designer's current practices through targeted intake questions"
    - "Scan for detection signals of each of the five anti-patterns"
    - "Classify each detected anti-pattern by name, severity (critical / moderate / low), and primary mechanism"
    - "Explain why each pattern feels productive — the illusion it creates"
    - "Prescribe a corrective action that names the specific replacement skill to invoke"
    - "Produce a structured audit report with findings ranked by severity"
  audience: ["students", "teachers", "corporate trainers", "instructional designers", "coaches", "lifelong learners"]
  triggers:
    - "Why isn't my studying working?"
    - "I've read this three times and still can't remember it"
    - "Review my study habits"
    - "Is cramming bad for learning?"
    - "I highlight everything but still fail tests"
    - "What am I doing wrong when I study?"
    - "Audit this training program for effectiveness"
    - "I'm a visual learner — should I only use videos?"
    - "My students are studying but not retaining"
    - "Why do I feel confident but fail the exam?"
  not_for:
    - "Building a complete spaced-practice schedule — use retrieval-practice-study-system"
    - "Classifying difficulty levels in a course design — use desirable-difficulty-classifier"
    - "Calibrating mastery confidence and running a dynamic testing cycle — use learning-calibration-audit"
    - "Designing a full curriculum from scratch — this skill diagnoses; other skills redesign"
  quality:
    completeness_score:
    accuracy_score:
    value_delta_score:
---

# Learning Practice Auditor

## When to Use

Something about how you or your learners study is producing less retention than expected. You may be putting in hours that do not convert to durable learning. You may be designing training that graduates confident-feeling but underprepared learners.

This skill is the diagnostic hub: it identifies which of five named ineffective practices are present, explains the mechanism creating the illusion of learning, rates the severity, and routes to the specific corrective skill.

**Typical entry points:**
- Learner: "I study for hours but blank on tests"
- Learner: "I highlight everything but still can't recall it"
- Teacher or trainer: "Why aren't my learners retaining this?"
- Instructional designer: "Is there anything wrong with this training structure?"
- Anyone asking: "Am I studying the wrong way?"

**Mode: Hybrid** — The agent runs the audit and produces the report. The human and/or agent then invokes the recommended corrective skills.

**This skill diagnoses. It does not redesign.** After the audit, each corrective action names the skill to invoke next.

---

## Step 1: Intake — Gather Current Practices

**Why this step:** Anti-pattern detection requires knowing what the learner or designer is actually doing, not what they think they are doing. Many learners describe their method as "studying" without specifying what that means. The intake questions force specificity.

Ask the following. If the user has already provided answers in their message, extract the answers without asking again.

### Required
1. **What are you trying to learn, and why?**
   (Subject, course, skill, domain — and the performance event: exam, job task, certification, presentation)

2. **Walk me through a typical study session from start to finish.**
   (What does the learner actually do, in sequence, with the material?)

3. **How do you decide when you know something well enough to move on?**
   (The mastery signal — feeling of familiarity, re-reading smoothly, immediate practice score, etc.)

4. **How is the learning structured over time?**
   (One long session vs. spaced sessions; one topic completed before the next; mixed topics within a session)

### Helpful if available
5. **Do you have a course outline, training schedule, or study plan I can read?**
   → If yes, use Read to scan it for blocked/massed structure signals.

6. **What does assessment look like?** (Multiple-choice, essay, performance demo, on-the-job transfer)

7. **Have you already taken any tests or received feedback on your performance?**

If context is still insufficient after asking, note the gap in the audit report and flag it as a finding ("Unable to assess [pattern] — insufficient information about [X]").

---

## Step 2: Anti-Pattern Detection

**Why this step:** Each anti-pattern has specific detection signals that appear in how the learner describes their practice. This step converts free-form description into a structured finding list.

Check each anti-pattern against the intake answers. Mark each as **Detected**, **Absent**, or **Insufficient information**.

### AP-1: Rereading Trap

**What to look for:**
- "I review my notes / re-read the chapter / highlight the key parts"
- Primary study method is reading or looking at material rather than testing recall
- Mastery signal is "it feels familiar" or "I can follow along when I read it"
- Study sessions described as long reading or annotation sessions

**Mechanism (explain this to the user when detected):**
Each time you reread well-organized text, your processing becomes faster and smoother — a state called *fluency*. That fluency feels like understanding and mastery, but it is really your brain's familiarity with the visual form of the text. It cannot distinguish between "I have encoded this in long-term memory" and "I have seen these words before." On a test, you must retrieve — reconstruct from memory — and fluency does not train that. The 2010 study: students who took a recall test after reading retained **50% more** a week later than those who reread. Crammers in a 1978 study forgot **50% of their initial recall within two days**; retrieval-practice groups forgot only **13%**.

**Corrective action:** Replace rereading sessions with self-testing sessions → invoke **`retrieval-practice-study-system`**

---

### AP-2: Massed Practice Delusion

**What to look for:**
- "I do all the problems for chapter 5 before moving to chapter 6"
- Training sessions run drill repetitions on one skill until it feels solid, then move on
- Study sessions are concentrated blocks on one topic
- Cramming before an exam described as the primary retention strategy

**Sub-pattern — Blocked Practice Trap:**
Problems or practice tasks are grouped by type. This removes the critical "what kind of problem is this?" sorting decision — which is exactly what real performance requires. College students practicing geometry volumes: blocked practice averaged **89% correct** during training but only **20%** on a test one week later. Interleaved practice: **60%** during training, **63%** on the test — a **215% improvement** in transfer. (Ch3)

**Sub-pattern — Familiarity Trap:**
After massed repetition, the material feels familiar (System 1 recognition). But the test requires System 2 retrieval and application. Rapid, blocked practice encodes learning in a cognitively simpler neural representation than spaced, varied practice — less flexible, less transferable.

**Mechanism:**
Rapid repetition draws on short-term working memory. Durable encoding requires a consolidation process that unfolds over hours and days. Massed practice produces fast visible gains that feel like mastery, but the gains are not consolidated. In the surgical microsurgery study: residents who had 4 lessons spaced one week apart outperformed those trained in a single day on *all* measures — elapsed time, movement efficiency, and success rate — one month later. **16%** of the massed-practice group damaged tissue beyond repair.

**Corrective action:** Replace massed and blocked practice with spaced, interleaved, and varied practice → invoke **`desirable-difficulty-classifier`** to classify present and absent difficulty strategies and get redesign recommendations.

---

### AP-3: Illusions of Knowing Cluster

**What to look for:**
- Mastery signal is "it feels familiar" or "I recognized the answer when I saw it"
- High confidence before a test, low score after
- "I studied this — I don't know why I blanked"
- Learner or trainer expresses surprise at gaps revealed on assessment
- Anyone relying on "just reading through" as a review method

**Note:** This anti-pattern overlaps with AP-1 and AP-2. Log it separately when the primary problem is *miscalibrated confidence*, not just the study method used.

**Mechanism:**
You rely on System 1 signals — fluency, familiarity, ease of processing — to judge mastery. These signals are unreliable. The Dunning-Kruger research: students at the **12th percentile** in logic ability believed they were at the **68th percentile** on average. Fluency illusion: re-reading a clear text increases the sensation that it is simple and already known. Hindsight bias: after learning the answer, you feel you "knew it all along," which makes you underestimate future study needs.

**Corrective action:** Run a calibration cycle to identify the specific distortion and install reliable mastery signals → invoke **`learning-calibration-audit`**

---

### AP-4: Learning Styles Myth

**What to look for:**
- "I'm a visual learner, so I only use videos"
- Training is segmented by assessed learning style
- Learner or designer says matching style to instruction is important for retention
- Learner avoids certain modalities because they are "not their style"

**The Pashler Validity Test:** For a study to prove learning styles theory, it must: (1) classify learners by style, (2) randomly assign them to style-matched vs. style-mismatched instruction on the same content, (3) show that style-matched learners outperform style-mismatched learners. In the 2008 Pashler et al. review: **no published study meets this design standard**. Those that do flatly contradict the theory. Studies found that matching instruction to the *nature of the content* (visual for geometry, verbal for poetry) benefits *all* learners regardless of their style preference.

**Mechanism:**
Learning preferences are real — but preference does not equal differential effectiveness. A learner's self-reported "style" predicts what they *prefer*, not what produces the best retention. Designing instruction around style matching misses the variance drivers that actually matter: prior knowledge, retrieval practice, spacing, and structure-building ability. More than **70 competing style theories** exist with contradictory dimensions and no cross-validation — itself a strong signal the construct lacks scientific coherence.

**Corrective action:** Drop style-based instructional segmentation; shift to content-nature matching and apply evidence-based strategies to all learners regardless of style preference → invoke **`desirable-difficulty-classifier`**

---

### AP-5: Errorless Learning Myth

**What to look for:**
- Training shows the answer before asking the learner to attempt it
- Flash cards are answer-first or answer-alongside
- Instructor corrects immediately before learner generates a response
- Stated rationale is "we don't want to practice errors"

**Mechanism:**
Generating an answer — even a wrong one — before seeing the correct answer strengthens the subsequent memory of the correct answer more than passive presentation. This is the *generation effect*: word pairs where learners had to fill in a missing letter (foot → s_ _e) produced better later recall than pairs presented intact (foot → shoe). Errors made in *generative attempts* followed by corrective feedback are part of the encoding process, not its enemy. Preventing the attempt removes the cognitive effort that creates durable encoding.

**Key distinction:** Uncorrected misconceptions are harmful. The solution is corrective feedback — not preventing the attempt.

**Corrective action:** Restructure practice to require generation before exposure — pre-tests, cued retrieval, retrieval-first flash cards → invoke **`retrieval-practice-study-system`**

---

## Step 3: Classify Severity

**Why this step:** Not all detected anti-patterns require the same urgency. Severity determines what to fix first and what to route immediately vs. note for later.

For each detected anti-pattern, assign a severity:

| Severity | Criteria | Action |
|---|---|---|
| **Critical** | This is the *primary* study or training method; no evidence-based alternative is in use | Immediate redesign — route to corrective skill now |
| **Moderate** | Anti-pattern coexists with some effective strategies but is undermining them | Targeted replacement of the identified component |
| **Low** | Present but minor; dominant strategy is already evidence-based | Flag for next redesign cycle |

---

## Step 4: Produce the Audit Report

**Why this step:** A written report makes findings actionable. The learner or designer can share it, return to it, and use the corrective routing as a checklist.

Structure the report as follows:

```
## Learning Practice Audit — [Subject / Program Name]

### Summary
[1-3 sentence overview: how many anti-patterns found, dominant severity level, top recommendation]

### Findings

#### [Anti-Pattern Name] — Severity: [Critical / Moderate / Low]
**Detected signals:** [What in their description triggered this finding]
**Mechanism:** [Why it feels effective but produces weak retention — in plain language]
**Evidence:** [1-2 specific research findings with numbers]
**Corrective action:** [Named replacement practice] → invoke `[skill-name]`

[Repeat for each detected anti-pattern]

### What to Do Next
[Prioritized list of corrective skills to invoke, in order of severity]
1. [Corrective skill] — addresses [anti-pattern(s)]
2. ...

### What Is Already Working
[Any detected evidence-based practices — note and reinforce these]
```

---

## Examples

### Example 1 — Individual Student (Critical: Rereading + Massed Practice)

**User description:** "I study organic chemistry by reading the chapter twice, then doing all the practice problems for each reaction type before moving on. I feel pretty solid during my sessions but I've failed two midterms."

**Audit findings:**
- **AP-1: Rereading Trap — Critical.** Primary review method is re-reading. The fluency gained from reading the chapter twice is not producing retrievable memory. The learner is using feeling-solid as the mastery signal, which tracks fluency not recall.
- **AP-2: Massed Practice Delusion (Blocked Practice) — Critical.** All practice problems for one reaction type before moving to the next = blocked massed practice. This eliminates the "which type of problem is this?" discrimination skill that the exam actually tests. The 20% vs. 63% result on blocked vs. interleaved geometry test is directly applicable.
- **AP-3: Illusions of Knowing — Moderate.** "I feel pretty solid during sessions but failed two midterms" = textbook miscalibration. The mastery signal is unreliable.

**Corrective routing:**
1. `retrieval-practice-study-system` — replace re-reading with self-quizzing and build spacing schedule
2. `desirable-difficulty-classifier` — redesign the problem practice to interleave reaction types
3. `learning-calibration-audit` — install reliable mastery signals to replace the fluency-feeling

---

### Example 2 — Corporate Trainer (Moderate: Learning Styles Design)

**User description:** "We have our training team assess employees' learning styles before onboarding. Visual learners get diagrams-first modules; auditory learners get voice-over walkthroughs. We invested in this system two years ago."

**Audit findings:**
- **AP-4: Learning Styles Myth — Critical.** The entire curriculum segmentation is organized around a theory with no empirical validation (Pashler et al., 2008). Investment in assessment tools and differentiated modules is producing no learning benefit relative to matched instruction. The content-nature matching finding is relevant: geometry-style content (spatial workflows, process maps) should be visual for *all* learners, regardless of assessed style.

**Corrective routing:**
1. `desirable-difficulty-classifier` — audit the onboarding modules for evidence-based difficulty strategies that will benefit all learners regardless of style
2. Redirect the investment in style assessment toward spaced-practice scheduling and retrieval-based knowledge checks

---

### Example 3 — Teacher (Low: Partial Massed Practice)

**User description:** "I do a mixed review at the end of each unit. I mostly teach one topic per day but sometimes bring in earlier material. Students self-quiz once a week using flashcards."

**Audit findings:**
- **AP-2: Massed Practice — Low.** One topic per day is still somewhat blocked, but the weekly mixed review and flashcard self-quizzing are evidence-based practices that partially offset this. The dominant strategy is already better than pure massed practice.
- No other anti-patterns detected from this description.

**Recommendation:** This practice is already above average. The flashcard self-quizzing is the highest-value element — reinforce and expand it. For the next redesign cycle: consider interleaving topics within sessions, not just end-of-unit reviews.

---

## Reference

Full evidence profiles, all research citations, and detailed sub-pattern descriptions for each anti-pattern:
→ `references/anti-pattern-reference-table.md`

For mechanism details on illusions of knowing, see also:
→ `learning-calibration-audit` references

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-retrieval-practice-study-system`
- `clawhub install bookforge-desirable-difficulty-classifier`
- `clawhub install bookforge-learning-calibration-audit`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
