---
name: learning-calibration-audit
description: |
  Diagnose and correct false confidence in learning mastery using cognitive science research. Use when you feel confident about a topic but keep failing tests, want to audit your metacognition for illusions of knowing, are preparing for a high-stakes assessment and need to verify actual mastery, or suspect your study method is producing Dunning-Kruger overconfidence. Also use for: identifying which of 7 specific cognitive distortions — fluency illusion, hindsight bias, Dunning-Kruger overconfidence, curse of knowledge, false consensus, imagination inflation, social memory contamination — is inflating your self-assessment accuracy; distinguishing reliable mastery indicators (delayed recall, novel problem transfer, peer explanation) from unreliable ones (rereading fluency, immediate recall, familiarity warmth); selecting calibration instruments (self-quizzing, cumulative quizzing, peer instruction) matched to the specific distortions detected; designing a dynamic testing cycle (assess → identify gaps → target practice → retest) as an iterative calibration protocol; and producing a calibration report with a retest schedule. Applies across all learning contexts — exam preparation, professional skill development, corporate training, language learning, technical certification. Works on document sets such as study plans, quiz results, self-assessment notes, and course materials.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/learning-calibration-audit
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [5, 6, 8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "metacognition", "self-assessment", "cognitive-bias", "calibration", "overconfidence", "dunning-kruger", "study-skills", "training-design"]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Learning materials, study plans, quiz results, self-assessment notes, or a plain-text description of what you are studying and how you assess your mastery"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with pasted text or document files."
discovery:
  goal: "Identify which cognitive distortions are inflating the learner's confidence, match calibration instruments to the specific distortions found, design a dynamic testing cycle, and produce a calibration report with a retest schedule"
  tasks:
    - "Gather learning context: subject, study methods, and how mastery is currently being assessed"
    - "Diagnose calibration issues by checking for signals of each of the 7 cognitive distortions"
    - "Classify each detected distortion and explain its mechanism"
    - "Recommend calibration instruments matched to the detected distortions"
    - "Design a 3-step dynamic testing cycle as the iterative correction protocol"
    - "Produce a calibration report with detected distortions, selected instruments, and retest schedule"
  audience:
    roles: ["student", "teacher", "corporate-trainer", "instructional-designer", "coach", "lifelong-learner"]
    experience: "any — no prior cognitive science knowledge required"
  triggers:
    - "Learner feels confident but performs poorly on actual tests or transfer tasks"
    - "Learner relies on rereading, highlighting, or recognition-based review as primary study method"
    - "Learner wants to audit their mastery claims before a high-stakes assessment"
    - "Trainer suspects trainees are overestimating skill acquisition from passive instruction"
    - "Learner has studied the same material repeatedly but retention does not seem to improve"
    - "Learner feels they 'know it' when reading notes but blanks when tested without them"
  not_for:
    - "Designing a spaced retrieval practice schedule from scratch — use practice-schedule-designer"
    - "Building interleaved practice sequences — use the interleaving skill"
    - "General study strategy advice without a calibration problem present"
---

# Learning Calibration Audit

## When to Use

You believe you have learned something — but tests, applications, or conversations with others expose gaps you did not know existed. Your self-assessment is miscalibrated: confidence is running ahead of actual mastery.

This skill diagnoses which specific cognitive distortions are inflating your confidence, then prescribes the calibration instruments and testing cycle that will bring self-assessment into alignment with actual performance.

**Do not use this skill if:** You need to design a full spaced-practice schedule. Use `practice-schedule-designer` for that. This skill focuses on the calibration problem — diagnosing and correcting false confidence — not on scheduling practice intervals.

---

## Context and Input Gathering

Before running the audit, collect:

### Required
- **Subject or skill being studied:** What are you trying to master? (e.g., "organic chemistry reaction mechanisms," "Python data structures," "leadership communication")
- **Current study methods:** How are you currently reviewing and assessing your learning? (e.g., rereading, flashcards, practice tests, writing summaries)
- **How you judge mastery right now:** What signal tells you that you know something? (e.g., "it feels familiar," "I can follow along when I reread it," "I got it right on the quiz right after class")

### Important
- **Assessment results, if available:** Any quiz scores, test results, or practice exam feedback
- **Study materials:** Notes, outlines, flashcard decks, or course materials you are working with

### Optional
- **Stakes and timeline:** Is there an upcoming exam, certification, or performance event? When?
- **Prior calibration attempts:** Have you already tried self-quizzing or practice tests? What happened?

If the context is not yet described, ask for it before proceeding.

---

## Process

### Step 1: Identify Unreliable Mastery Signals

**Action:** Review the learner's stated method of judging mastery and check it against the list of unreliable indicators. Flag any that are present.

**WHY:** Unreliable mastery signals produce false confidence because they respond to familiarity and processing ease rather than to retrievable, transferable knowledge. A learner who judges mastery by fluency with their notes has confused ease of reading with depth of encoding. Until unreliable signals are identified, the learner has no reason to change their method — the feeling of knowing is strong and feels valid.

**Unreliable mastery indicators — flag if any are in use:**
- Reading fluency: "When I reread my notes, it all makes sense"
- Familiarity warmth: "It feels familiar when I see it"
- Immediate recall: "I got it right immediately after the lecture"
- Highlighting coverage: "My notes are thoroughly marked up"
- Passive recognition: "I can follow along when the answer is explained"
- Massed repetition: "I reviewed it five times this week"

**Reliable mastery indicators — check which are in use:**
- Delayed free recall: Successfully retrieved from memory after a gap (days, not minutes)
- Novel problem transfer: Applied the concept correctly to an unfamiliar problem type
- Peer explanation: Explained the concept clearly to someone who didn't know it, and they understood
- Error prediction: Accurately anticipated which questions or situations would be difficult before encountering them
- Interleaved performance: Correctly identified which concept or method to use when mixed with similar-looking problems

**Output:** List the unreliable signals in use and note which reliable signals are absent.

---

### Step 2: Diagnose Cognitive Distortions

**Action:** For each unreliable signal flagged in Step 1, identify which cognitive distortion mechanism is producing it. Use the 7-distortion taxonomy in `references/cognitive-distortions.md` for the complete reference. The distortions most likely to appear are described here with their detection signals.

**WHY:** Naming the specific distortion mechanism is what makes the calibration intervention effective. "You are overconfident" gives the learner nothing to act on. "Your confidence is driven by fluency illusion — ease of reading your notes is being mistaken for retrievable knowledge" gives the learner a specific mechanism to interrupt and a specific instrument to replace it with. Each distortion type requires a different correction instrument; a generic "study harder" recommendation will not work.

**Detection checklist — check each distortion:**

**Fluency Illusion**
Detection signal: Learner studies by rereading and reports that material "makes sense" or "is starting to click" during review — but struggles to recall it without the text.
Mechanism: Ease of processing a familiar text is experienced as mastery. The text is doing the cognitive work, not the learner's memory.

**Hindsight Bias (Knew-It-All-Along Effect)**
Detection signal: After seeing the correct answer, learner says "I knew that" or "I almost said that" — but did not produce the answer before seeing it.
Mechanism: Correct answers, once revealed, feel like they were always accessible. The learner retrospectively misremembers their prior uncertainty as near-knowledge.

**Dunning-Kruger Overconfidence**
Detection signal: Learner in early or intermediate stages of learning rates their competence as high relative to peers, but actual performance falls well below this rating. Learner is unaware of the skill dimensions they cannot yet perceive.
Mechanism: Incompetence in a domain also undermines the metacognitive ability to recognize incompetence. The same skill gap that limits performance also limits the ability to judge performance accurately.

**Curse of Knowledge**
Detection signal: Teacher or advanced learner assumes others can follow explanations that feel obvious to the explainer. Or learner who has just mastered a topic believes they could have learned it faster — underestimating past struggle.
Mechanism: Once knowledge is consolidated, the steps required to build it become invisible. The expert cannot reconstruct the novice's perspective.

**False Consensus**
Detection signal: Learner assumes classmates or peers share their level of understanding, and uses the absence of complaints as evidence that the material is clear.
Mechanism: Humans tend to assume others share their beliefs and understanding levels. Silence from peers reads as confirmation rather than as independent uncertainty.

**Imagination Inflation**
Detection signal: Learner has repeatedly rehearsed answering a question mentally (without actually retrieving the answer) and now feels confident they can answer it. Or learner has rehearsed an explanation in their head and treats mental rehearsal as equivalent to demonstrated performance.
Mechanism: Vividly imagining an event increases the likelihood that it will later be remembered as having actually occurred. Imagined retrieval does not build the same memory trace as actual retrieval.

**Social Memory Contamination**
Detection signal: Learner studied in a group and has absorbed peers' explanations, including incorrect ones, as their own understanding. Or learner's recall of material matches a group member's account rather than the source.
Mechanism: Memory conforms to social influence. One person's recalled version of material — including errors — can overwrite another person's memory of the original, especially in collaborative review settings.

**Output:** List each detected distortion with its mechanism and the specific evidence from the learner's context.

---

### Step 3: Select Calibration Instruments

**Action:** For each detected distortion, prescribe the calibration instrument most directly targeted at its mechanism. See `references/calibration-instruments.md` for the full instrument reference.

**WHY:** Calibration instruments work by replacing unreliable feedback (processing fluency, familiarity, social confirmation) with objective performance data that the learner cannot rationalize away. Each instrument is matched to the specific mechanism of a distortion — a self-quiz defeats fluency illusion by forcing retrieval instead of recognition, but it does not help with false consensus, which requires exposure to peer variation. Prescribing the wrong instrument for the distortion type wastes effort without improving calibration.

**Instrument-to-distortion matching:**

| Detected Distortion | Primary Instrument | Why It Works |
|---------------------|-------------------|--------------|
| Fluency Illusion | Self-quizzing (closed-book free recall) | Forces retrieval without text cues; processing difficulty signals actual memory gaps, not text unfamiliarity |
| Hindsight Bias | Pre-answer confidence logging | Recording confidence before seeing the answer makes the prior state of not-knowing concrete and non-revisable |
| Dunning-Kruger Overconfidence | Cumulative quizzing across topic areas | Exposes the full range of what is not yet known; reveals the dimensions of competence the learner cannot currently perceive |
| Curse of Knowledge | Peer teaching (explain to a naive listener) | Forces reconstruction of the knowledge from the novice's baseline; gaps in explanation reveal gaps in transferable knowledge |
| False Consensus | Peer instruction with divergent pairing | Deliberately pairing with peers who gave different answers exposes assumption that consensus already existed |
| Imagination Inflation | Actual practice tests (not mental rehearsal) | Replaces imagined performance with real performance; the difference between imagined and actual recall surfaces immediately |
| Social Memory Contamination | Solo closed-book retrieval before group review | Establishes a clean individual baseline before exposure to peer accounts; deviations from source material are visible |

**Instrument descriptions (summary):**

**Self-quizzing (closed-book free recall):** Set all study materials aside. Write, speak, or type everything you can recall about the topic without looking. Then check against the source. The gaps are your actual gaps.

**Cumulative quizzing:** Quiz that reaches back across all material covered — not just the most recent session — forcing retrieval of earlier material alongside new content. Use at each study session.

**Peer instruction:** Before solving a problem or answering a question, commit to an answer individually. Then discuss with a peer who chose differently. Each person argues their reasoning. The disagreement — not the final answer — is the calibrating event.

**Pre-answer confidence logging:** Before checking any answer, rate your confidence on a simple scale (1-5 or percentage likelihood). After checking, compare prediction to outcome. Patterns of high-confidence errors are the primary diagnostic signal.

**Peer teaching (explain to a naive listener):** Explain the concept to someone who does not know it — without notes. Track where the explanation breaks down, requires hedging, or produces confusion in the listener. These are the knowledge gaps.

**Output:** A prioritized list of instruments assigned to each detected distortion.

---

### Step 4: Design the Dynamic Testing Cycle

**Action:** Structure the learner's calibration correction as an iterative 3-step cycle that continues until predicted performance matches actual performance within an acceptable margin.

**WHY:** A one-time test and a one-time correction do not recalibrate the learner — they only reveal the gap at a single point in time. The dynamic testing cycle treats each test as a calibration instrument rather than a grade: it shows where expertise currently stands, redirects effort to underperforming areas, and then retests to measure whether the gap has closed. Repeating the cycle builds the metacognitive habit of using performance data to guide study, rather than feelings of fluency or familiarity.

**Cycle structure:**

**Step A — Assess (Baseline Test)**
Administer a performance test using the calibration instrument matched to the primary detected distortion. The test must be:
- Closed-book
- Conducted after a time gap from the last study session (minimum 24 hours for most material)
- Scored with a pre-answer confidence log if hindsight bias was detected

What to record: raw score, confidence-versus-accuracy pattern, and which specific items or sub-areas were missed.

**Step B — Identify Gaps and Redirect**
For each missed item, classify the gap type:
- Encoding gap: Information was never well encoded (did not understand it at study time)
- Retrieval gap: Information was encoded but cannot be retrieved (knew it once, lost it)
- Transfer gap: Information can be retrieved in isolation but cannot be applied to novel problems

Each gap type requires different practice:
- Encoding gap: Return to the source, study the concept more carefully, then re-encode using elaborative questioning ("why does this work?" "how does this connect to X?")
- Retrieval gap: More retrieval practice, with greater spacing between attempts
- Transfer gap: Practice on varied and unfamiliar problem types that use the same underlying concept

**Step C — Retest**
After targeted practice on the identified gaps, retest on the same topics — preferably using different question formats or novel problem instances to distinguish retrieval from memorization of specific items. Compare the pre-answer confidence log across test and retest.

**Retest calibration criterion:** Continue cycling until one of these conditions is met:
- Predicted confidence and actual scores differ by less than 10 percentage points on average
- Three consecutive retests show no new gap areas emerging
- Peer teaching attempt produces no listener confusion or unanswered questions

**Cycle schedule guidance:**
- Space retest at least 48-72 hours after targeted practice (not immediately after)
- For high-stakes preparation: run the full cycle at least 3 times across the study period
- Do not drop material from the cycle after one correct answer — review it at least one more time at a longer interval

---

### Step 5: Produce the Calibration Report

**Action:** Write a structured calibration report that consolidates the audit findings and serves as the learner's working document.

**WHY:** The report externalizes the calibration data — moving it from subjective feeling to an objective, reviewable record. Learners who have a written account of their distortions, their instruments, and their retest schedule are far less likely to drift back to unreliable study habits than those who receive only verbal advice. The report also creates accountability: at the next retest, the learner can compare predicted versus actual and update the record.

**Report structure:**

```
## Calibration Report: [Subject / Skill]

### Current Mastery Assessment
[Estimated actual mastery level based on reliable indicators: what the learner can do without study materials]

### Detected Distortions
For each distortion detected:
- Distortion: [Name]
- Evidence: [What the learner is doing that signals this distortion]
- Mechanism: [Brief explanation of why this produces false confidence]

### Prescribed Calibration Instruments
For each instrument assigned:
- Instrument: [Name]
- Targets: [Which distortion(s) it corrects]
- Instructions: [How to use it — what to do, when to do it]

### Dynamic Testing Cycle Plan
- Cycle 1 Baseline Test: [Date, instrument, scope]
- Gap Analysis: [How to classify and record gaps]
- Cycle 1 Retest: [Target date — minimum 48h after targeted practice]
- Cycle 2 Baseline Test: [Date]
- [Continue for 3+ cycles if high-stakes]

### Calibration Criterion
[Which criterion defines successful recalibration for this learner and subject]

### Red Flags to Watch For
[Conditions that would indicate calibration is not working — e.g., consistently high confidence despite low scores, dropping practice tests after apparent success]
```

---

## Inputs / Outputs

### Inputs
- Description of the subject or skill being studied (required)
- Description of current study methods and mastery-judging criteria (required)
- Quiz results, test scores, or self-assessment data (optional but valuable)
- Study materials or course outline (optional)

### Outputs
- List of unreliable mastery signals in use
- Detected cognitive distortions with mechanisms and evidence
- Prioritized calibration instrument recommendations matched to distortions
- Dynamic testing cycle schedule (3-step iterative protocol)
- Written calibration report with retest schedule

---

## Key Principles

**Feeling of knowing is not knowing.** The subjective sense that material is familiar or "making sense" during review reflects processing ease, not retrievable, transferable knowledge. The gap between what feels known and what can be retrieved without cues is where false confidence lives.

**The diagnostic instrument must bypass the unreliable signal.** Closed-book retrieval defeats fluency illusion because processing ease is no longer available as a signal. Peer teaching defeats curse of knowledge because the listener's confusion is not subject to rationalization. Match the instrument to the mechanism of the distortion.

**Dynamic testing is iterative by design.** A single calibration test is not sufficient. Each cycle of assess → identify gaps → targeted practice → retest updates the calibration. Three cycles across a study period is a minimum for high-stakes preparation.

**Incompetence impairs metacognition too.** The Dunning-Kruger effect means that the largest calibration gaps often occur at low competence levels, precisely where the learner is least equipped to detect them. External feedback — peer instruction, practice test scores, peer review — is most critical here.

**Reliable indicators require a time gap.** Immediate recall after a lecture or study session is not a reliable mastery indicator — the material is still in working memory. The meaningful test is whether it can be retrieved after a delay of at least 24 hours, when working memory has cleared.

---

## Examples

### Example 1: Law Student Before Bar Exam

**Context:** A law student feels confident about contract law — they have read the chapter three times and their notes are thoroughly highlighted. But a practice bar question on contracts leaves them unable to identify the correct legal standard.

**Step 1:** Unreliable signals: rereading fluency, highlighting coverage. Reliable signals absent: no delayed free recall, no novel problem practice.

**Step 2:** Fluency illusion (primary — rereading fluency mistaken for retrievable doctrine); Imagination inflation (studying by mentally rehearsing answers without actually producing them in writing).

**Step 3:** Self-quizzing (closed-book): Write out the elements of each contract doctrine from memory before opening notes. Pre-answer confidence logging: before each practice question, rate confidence 1-5 and record. Compare to actual score.

**Step 4:** Cycle 1 baseline — 15-question practice exam on contracts, closed-book, confidence logged. Gap analysis — which doctrine elements are encoding gaps vs. retrieval gaps. Cycle 1 retest — 48 hours later, different question set, same doctrines. Continue until confidence ratings and scores align within 10 points.

---

### Example 2: Corporate Training Cohort

**Context:** A trainer observes that trainees perform well during the training day (completing exercises correctly with the reference guide available) but report confusion when applying procedures in the field.

**Step 1:** Unreliable signals in use: passive recognition (exercises done with reference guide open), immediate recall (end-of-day quiz administered right after instruction). No delayed free recall, no novel application, no peer teaching.

**Step 2:** Fluency illusion (guide availability masks retrieval difficulty); Dunning-Kruger overconfidence (trainees in early learning stage overrate competence); False consensus (trainees assume peers' silence means shared understanding).

**Step 3:** Cumulative quizzing — weekly quiz reaching back across all procedures covered. Peer instruction — before demonstrations, trainees write their expected procedure independently, then compare with a partner who differed. Peer teaching — in pairs, trainees teach a procedure without the guide; the partner signals confusion points.

**Step 4:** Cycle 1 — closed-book procedural quiz one week post-training. Gap analysis — which procedures have encoding vs. retrieval vs. transfer gaps. Targeted practice — additional drills on gap procedures. Retest — same procedures in a novel scenario context two weeks later.

---

### Example 3: Self-Study Language Learner

**Context:** A language learner reports that vocabulary "feels solid" — recognition from flashcard reviews is high and they can follow podcasts well. But speaking and writing attempts reveal many words are not available for production.

**Step 1:** Unreliable signals: familiarity warmth (flashcard recognition), passive recognition (following podcasts). Reliable signals absent: no production-side practice, no delayed free recall, no peer teaching in the target language.

**Step 2:** Fluency illusion (recognition mistaken for production-ready knowledge); Social memory contamination (if studying in groups, may have absorbed peer corrections as own knowledge without independent consolidation).

**Step 3:** Closed-book production quizzing — cover the target word; write or speak only from the definition cue. Peer instruction — set a conversation exchange where neither participant can revert to their native language for a defined vocabulary set; communication breakdowns are calibration data.

---

## References

| File | Contents |
|------|----------|
| `references/cognitive-distortions.md` | Complete 7-distortion taxonomy with detection criteria, mechanisms, real-world examples, and false positive guards |
| `references/calibration-instruments.md` | Full instrument reference: self-quizzing, cumulative quizzing, peer instruction, peer teaching, confidence logging — with implementation steps and distortion coverage |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
