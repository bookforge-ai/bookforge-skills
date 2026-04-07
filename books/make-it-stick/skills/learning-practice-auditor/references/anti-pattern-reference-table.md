# Anti-Pattern Reference Table

Full evidence profiles for each ineffective learning practice documented in *Make It Stick* (Brown, Roediger, McDaniel). Use this table when you need the complete mechanism, research citations, and severity ratings during an audit.

---

## AP-1: The Rereading Trap

**Core mechanism:** Each pass through the text increases processing fluency — the sensation that the material is easy to understand. Fluency is mistaken for mastery. The learner overestimates how much they will remember on a future test, because the test will require *retrieval*, not recognition.

**Detection signals:**
- Primary review strategy is highlighting, underlining, or annotating text
- Learner says "I've read it three times, I should know this"
- Learner feels confident right after reviewing but blanks on tests
- Study sessions consist of reading notes rather than self-testing

**Sub-pattern — Fluency Illusion:**
When a learner rereads clear, well-organized text, processing becomes faster and easier with each pass. This processing ease (fluency) is a poor proxy for durable retention. The learner confuses *recognition* (can follow the text when it is in front of them) with *recall* (can reconstruct it from memory). Ch5 (p. 115): "Students who study by rereading their texts can mistake their fluency with a text, gained from rereading, for possession of accessible knowledge of the subject and consequently overestimate how well they will do on a test."

**Research evidence:**
- 1978 study: cramming (massed re-study) led to higher scores on an *immediate* test but on a second test two days later, crammers had forgotten **50%** of what they recalled initially; those who practiced retrieval instead forgot only **13%**.
- 2010 study (reported in the New York Times): Students who read a passage and then took a recall test retained **50% more** information a week later than students who only reread the passage.
- Single quiz after a lecture produces better retention than rereading lecture notes (Ch1 claims list, Ch2 passim).

**Consequences of continued use:**
- Systematically overestimates mastery → test performance surprises are common
- Material fades within days; not consolidated into long-term memory
- Time is spent on low-yield re-exposure instead of high-yield retrieval

**Corrective action:** Replace rereading with retrieval practice — invoke `retrieval-practice-study-system`.

---

## AP-2: Massed Practice Delusion

**Core mechanism:** Rapid-fire repetition of a single skill or concept within one session produces visible, rapid improvement. This improvement is real but draws primarily on short-term memory. Because consolidation requires hours to days, the rapid gain is not durably encoded. The learner observes fast progress and concludes the method is superior — but the gains evaporate.

**Detection signals:**
- Training program runs through all examples of one type, then moves to the next type
- Study session = "I'll do 50 of these problems right now"
- Course design: module 1 fully complete → module 2 fully complete → etc.
- Learner feels "on top of it" while doing a session but cannot recall material a week later

**Sub-pattern — Blocked Practice Trap:**
Problems or examples are grouped by type (block 1 = all wedge volumes, block 2 = all spheroid volumes). This eliminates the "what type of problem is this?" decision that is required in real performance. In a study of college students learning volumes of geometric solids: massed/blocked practice averaged **89% correct** during training vs. 60% for interleaved; but on a test one week later, massed practice averaged only **20% correct** vs. **63% for interleaved** — a **215% improvement** for interleaving. (Ch3)

**Sub-pattern — Familiarity Trap:**
After massed repetition, material feels familiar. Familiarity is a System 1 signal (automatic, fast) that is often mistaken for mastery (which requires System 2 verification — delayed recall, transfer, novel problem solving). Ch5 explains Kahneman's System 1/System 2 framework and how fluency-based familiarity hijacks self-assessment.

**Research evidence:**
- Surgical microsurgery study (38 residents): residents with lessons spaced one week apart outperformed those trained in a single day on *all* measures a month later. **16%** of the massed-practice group damaged experimental vessels beyond repair and could not complete their surgeries. (Ch3)
- Beanbag study: 8-year-olds who practiced at 2-foot and 4-foot distances performed best on a 3-foot test, compared to children who only practiced at 3 feet. Variable practice > blocked massed practice. (Ch3)
- Bird classification and painter attribution studies: interleaved study produced superior test scores; massed-study participants *preferred* massed practice and still believed it was superior even after seeing their own test results. (Ch3)

**Consequences of continued use:**
- Training produces confident but incompetent graduates
- Skills fail to transfer to novel situations (poor discrimination ability)
- Fast apparent learning masks slow real consolidation

**Corrective action:** Replace massed practice with spaced, interleaved, and varied practice → invoke `desirable-difficulty-classifier` to identify missing difficulty strategies.

---

## AP-3: Illusions of Knowing Cluster

This is a family of related distortions that inflate perceived mastery. Each has a distinct mechanism. The full taxonomy and calibration instruments are documented in `learning-calibration-audit`.

| Illusion | Mechanism | Signal |
|---|---|---|
| Fluency illusion | Processing ease mistaken for retrieval ability | Feels confident while reading, blanks on test |
| Hindsight bias / Knew-it-all-along | After learning the answer, past ignorance is underestimated | "I knew that" after being shown the correct answer |
| Dunning-Kruger overconfidence | Incompetent people lack the skill to judge their own incompetence | Grossly overestimated test score; bottom quartile students rated themselves 68th percentile when actually at 12th |
| Curse of knowledge | Expert underestimates learning time for a novice | Teacher's explanation misses the foundational steps students actually need |
| False consensus | Assumes others share your understanding | Surprised when teammates do not "obviously" know what you know |
| Imagination inflation | Imagining an event increases belief it occurred | Rehearsed explanations feel like actual competence |
| Social memory contamination | Others' errors infect your memory | Group study partners' incorrect beliefs become your own |

**Research evidence:** Dunning-Kruger: students at 12th percentile believed they were at **68th percentile** in logical reasoning. After training in logic, the bottom-quartile students could accurately estimate their own performance. Without training, they held their inflated estimates despite seeing peers' superior performance. (Ch5)

**Corrective action:** → invoke `learning-calibration-audit` to run the full distortion diagnosis and calibration cycle.

---

## AP-4: Learning Styles Myth

**Core mechanism:** The theory proposes that each learner has a preferred modality (visual, auditory, reading/writing, kinesthetic — "VARK") and learns best when instruction matches that style. The myth is appealing because learner preferences are real. The research failure is: preferences ≠ differential effectiveness. No published evidence validates the critical claim — that matching instruction to style *improves outcomes* relative to mismatched instruction.

**Detection signals:**
- Training program segments learners by "learning style" assessment
- Instructor provides visual-only materials for "visual learners" and skips written materials
- Learner says "I'm a visual learner, so slides work better for me than reading"
- Curriculum design driven by style matching rather than content-nature matching

**The Pashler Validity Test (2008):**
Pashler, McDaniel, Rohrer, and Bjork established the evidence standard a study must meet to validate learning styles:
1. Classify learners by their assessed learning style
2. Randomly assign learners to different instructional modes teaching the same content
3. Give all learners the same test afterward
4. Show that style-matched learners outperform style-mismatched learners, AND that different styles yield different optimal modalities

**Finding:** Virtually no published study meets this design requirement. Those that do *flatly contradict* the theory. Moreover: when instructional mode matches the *nature of the content* (visual for geometry, verbal for poetry), *all* learners do better, regardless of their style preferences. Content-nature matching > style matching. (Ch6)

**Additional context:** A 2004 survey for Britain's Learning and Skills Research Centre identified **more than 70 distinct learning styles theories** in the marketplace. The report's authors called the field a "bedlam of contradictory claims." An attendee at a learning conference who had completed a style assessment reported: "I learned that I was a low auditory, kinesthetic learner. So there's no point in me reading a book or listening to anyone for more than a few minutes." This exemplifies the corrosive effect: learners artificially limit themselves. (Ch6)

**Consequences of continued use:**
- Students pigeonhole themselves and avoid effective modalities outside their "style"
- Organizations waste resources on style-matched training with no evidence of benefit
- Misses the actual variance driver: differences in prior knowledge, structure-building ability, and use of retrieval practice

**Corrective action:** Shift from style-based design to content-nature matching and apply proven strategies (retrieval, spacing, interleaving) regardless of style preferences → invoke `desirable-difficulty-classifier`.

---

## AP-5: Errorless Learning Myth

**Core mechanism:** The myth holds that presenting learners with immediate, correct answers before they attempt retrieval prevents the formation of incorrect memories and maximizes confidence. The research shows the opposite: attempting to generate an answer, even when wrong, strengthens memory of the correct answer more than passive presentation does.

**Detection signals:**
- Flash cards show the answer on the same side as the prompt
- Training materials show the solution before asking the learner to attempt it
- Instructor corrects students immediately before they have attempted an answer
- "We don't want them to practice errors" as the stated rationale

**Research evidence:**
- The "generation effect": word pairs studied with a cue (foot → s_ _e) produced higher later recall than pairs studied intact (foot → shoe). The effort of generating the answer from a partial cue strengthens the memory trace. (Ch2)
- Pre-testing: trying to solve a problem *before being taught the solution* leads to better learning, even when the attempt produces errors. (Ch1 claims list)
- Delayed practice retrieval: when a recall attempt was delayed by 20 intervening word pairs rather than immediate, later recall was stronger, because the greater effort required consolidated the memory further. (Ch2)

**Key distinction:** Errors made during *learning attempts* (generative errors, before feedback) strengthen encoding. Errors made due to *misconceptions left uncorrected* are harmful. The corrective is feedback, not preventing the attempt.

**Consequences of continued use:**
- Learners receive information passively, which produces weak encoding
- Confidence may feel high (material was always presented correctly) but retrieval on tests fails
- The difficulty of attempting retrieval — which is the mechanism of durable learning — is eliminated

**Corrective action:** Build in pre-testing, retrieval attempts, and generative cues before presenting answers → invoke `retrieval-practice-study-system`.

---

## Severity Classification

| Severity | Definition | Appropriate Response |
|---|---|---|
| **Critical** | Anti-pattern is the primary study or training method; no evidence-based alternative is in use | Immediate redesign; route to corrective skill now |
| **Moderate** | Anti-pattern coexists with some effective strategies; it is undercut the effective ones | Targeted replacement; redesign the identified component |
| **Low** | Anti-pattern present but minor; dominant strategy is already evidence-based | Note and flag for next redesign cycle |

---

*Source: Make It Stick (Brown, Roediger, McDaniel). Chapters 1, 2, 3, 5, 6.*
