---
name: evidence-based-training-designer
description: "Redesign a corporate training program, employee training curriculum, employee onboarding, or in-service training so that learning actually sticks past the end of the session. Use this skill when a company's training is built on lecture-heavy workshops, single-topic day-long blocks, or passive e-learning modules that employees promptly forget; when an L&D team needs to convert a massed-practice curriculum into an evidence-based architecture; when a trainer or workshop design lead is building a new training program from scratch and wants to apply learning science from the start; when onboarding for a sales, technical, or certification role needs to produce durable competence rather than a test-passing event; when management asks why employees cannot apply training back on the job; when training program design needs to show measurable retention and transfer, not just satisfaction scores. This skill applies the corporate training models from Farmers Insurance (interleaved four-domain curriculum, FORE scaffolding, vision-poster goal anchoring, 5-4-3-2-1 sales system), Jiffy Lube (tell-show-do-review certification cycle, 80% threshold, biennial recertification), and Andersen Windows (2-hour job rotation, worker-led improvement, kaizen events) to redesign any training program. It does NOT design individual practice schedules for individual learners — use practice-schedule-designer for that."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/evidence-based-training-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "corporate-training", "learning-and-development"]
depends-on: [practice-schedule-designer]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Training context: content domains, audience, duration, current program format, and performance gap being addressed"
  tools-required: [Write]
  tools-optional: [Read]
  mcps-required: []
  environment: "Any agent environment; L&D professional or trainer describes their program in text form or answers guided intake questions"
discovery:
  goal: "Audit the current training design for anti-patterns, select a curriculum architecture template (interleaved spiral, certification cycle, or job-rotation model), then produce a redesigned program plan with session structure, spaced retrieval schedule, and evaluation protocol"
  tasks:
    - "Gather training context: content domains, audience profile, duration, and current design"
    - "Audit current design for massed-practice and passive-delivery anti-patterns"
    - "Select the appropriate architecture template based on training type and goal"
    - "Design interleaved curriculum with generation exercises, not lecture-then-drill sequences"
    - "Add spaced retrieval follow-up protocol extending beyond the training event"
    - "Output redesigned program plan with session map, evaluation criteria, and transfer checkpoints"
  audience: "L&D professionals, corporate trainers, instructional designers, operations managers, franchise training coordinators, and HR business partners responsible for employee onboarding or continuing education"
  triggers:
    - "User needs to redesign a training program that is not producing job-transfer"
    - "User is building a corporate training curriculum from scratch"
    - "User's training is structured as full-day single-topic blocks"
    - "Employees pass training assessments but cannot apply skills on the job"
    - "Franchisee or multi-site operation needs a consistent certification model"
    - "L&D team wants to introduce evidence-based learning science into their design process"
    - "In-service or continuing education training is a weekend dump of PowerPoint lectures"
---

# Evidence-Based Training Designer

## When to Use

Your organization runs training. People sit through it. Then they go back to work and do the same things they did before. This is not a motivation problem or a content problem — it is a design problem.

The research is unambiguous: massed instruction (covering one topic exhaustively before moving to the next), passive delivery (lecture and slide), and single-event learning (a workshop with no follow-up) produce fast performance during training and rapid forgetting afterward. The architecture of most corporate training is optimized for the trainer's convenience, not the learner's retention.

This skill redesigns training programs around three mechanisms that the research shows actually produce durable, transferable skill:

1. **Spaced practice** — material is revisited across time with gaps that force retrieval
2. **Interleaving** — multiple content domains are mixed within sessions rather than separated into day-long blocks
3. **Generation** — learners produce answers, solve problems, and practice application before being given the answers, not after

**Preconditions to verify before continuing:**

- Can the user name the content domains the training needs to cover? If not, clarify this before designing.
- Is there a performance gap to address, or is this purely for compliance? Performance-gap training warrants a different intensity of design than compliance box-checking.
- What is the post-training context? Do employees return to a job where they will practice these skills, or is the training a one-time certification event?

**What this skill does NOT cover:**

- Individual learner practice schedules (use `practice-schedule-designer`)
- Motivation, engagement, or gamification strategies independent of learning architecture
- Authoring tool selection or e-learning production

---

## The Core Design Failure to Fix

Before any design work, name the pattern being replaced. Most corporate training failures trace to one of three structural defects:

| Anti-Pattern | What It Looks Like | What It Costs |
|---|---|---|
| **Massed-domain blocking** | Day 1: sales skills. Day 2: product knowledge. Day 3: compliance. No return to prior topics. | Topics learned in isolation cannot be integrated or transferred. Employees forget Day 1 material by the time they need to combine it with Day 3 material on the job. |
| **Passive-delivery dependency** | Content delivered via lecture, slides, or video. Practice is an afterthought at the end of a module. | Learners generate no memory retrieval during the training event itself. Recognition in the room does not predict recall on the job. |
| **Training-as-event** | One workshop, one week, one seminar. No scheduled follow-up. | The forgetting curve begins immediately. Without spaced retrieval after the event, 70–80% of content is inaccessible within a week. |

State the diagnosis explicitly before moving to architecture selection.

---

## Step 1 — Gather Training Context

**Why:** Architecture selection and session design depend on the specific combination of content type, audience experience level, training duration, and transfer context. Guessing at these leads to generic recommendations that do not fit the actual situation.

### Required (ask if missing)

- **What are the content domains?** Name each area the training must cover. (Example: Farmers Insurance covers four — sales techniques, marketing systems, business planning, brand advocacy. Jiffy Lube covers service procedures per vehicle position plus management skills.)

- **What is the audience profile?** Are participants new employees, licensed professionals, franchise operators, experienced workers moving to a new role? Experience level determines how much initial orientation is needed before interleaving begins.

- **What is the total training duration?** Hours, days, weeks. Both the initial program and any scheduled follow-up.

- **What is the current program format?** Walk through a recent session — what happens first, second, and for how long? This surfaces the anti-patterns.

- **What does successful transfer look like?** What specific behavior change is expected 30 days after training ends? This defines the evaluation target and shapes the retrieval protocol.

### Useful (gather if available)

- **Is there a certification or compliance requirement?** Jiffy Lube's model requires demonstrated mastery (80% threshold + supervisor sign-off) before employees can work on customers' vehicles. Compliance constraints affect the certification design.

- **Is there a multi-location or franchise context?** Distributed training requires written standards (like Andersen Windows' step-by-step written job guides) to ensure consistency across sites without a permanent trainer present.

- **What is the post-training work environment?** Andersen Windows workers rotate every two hours by design; their training architecture mimics this by building cross-training into the job itself. If the post-training environment is inherently varied, this reduces the burden on the training program to create variation artificially.

---

## Step 2 — Audit Current Design for Anti-Patterns

**Why:** A redesign proposal lands better when it names what is wrong specifically, not generically. The audit also surfaces which anti-patterns are present so the architecture selection in Step 3 can correct them directly.

Work through the user's description of their current program and score each dimension:

**Domain structure:**
- Are all sessions on one domain completed before moving to the next? → Massed-domain blocking present
- Are multiple domains touched within each session? → Interleaving present (assess quality)

**Delivery method:**
- Is content delivered primarily via lecture, video, or slides? → Passive-delivery dependency present
- Are learners generating answers (solving problems, role-playing, predicting outcomes) before being told correct answers? → Generation present (assess frequency)

**Follow-up structure:**
- Does the training have a scheduled follow-up protocol (quizzes, check-ins, return practice sessions) after the initial event? → If no, training-as-event anti-pattern present

**Output a brief audit summary** before making architecture recommendations:

> "Your current program has the following anti-patterns: [list]. The most costly pattern for your transfer goal is [name the primary one] because [specific consequence for their context]."

---

## Step 3 — Select the Architecture Template

**Why:** Three corporate training models from the research map to three different training contexts. Selecting the right one (rather than applying a generic interleaving prescription) produces a design that fits the actual constraints of time, certification need, and workforce structure.

### Template A — Interleaved Spiral Curriculum (Farmers Insurance Model)

**Best for:** New-hire programs covering 3–6 distinct but related content domains over several days to weeks. Contexts where domains are mutually reinforcing (sales technique, product knowledge, business planning, and brand advocacy each add meaning to the others). High-trust, high-engagement contexts where learner buy-in matters.

**Core mechanics:**
1. **Vision anchor (Day 1, ~30 minutes):** Before any content, learners create a concrete representation of what success looks like for them personally at a meaningful future horizon (Farmers used a poster exercise with magazines and scissors). The image on the poster becomes the anchor to which all subsequent learning is connected. This is not a warm-up exercise — it is a generation activity that activates prior knowledge and establishes a motivational frame that the trainer can return to throughout the program.
2. **Interleaved session design:** No session is devoted exclusively to one domain. Every session touches all domains, returning to each with increasing complexity. The Farmers model cycles through all four domains multiple times per day, not once per day.
3. **FORE scaffolding:** Build a client/customer discovery framework early (in the Farmers case, asking about Family, Occupation, Recreation, and Enjoyment). Introduce it as an icebreaker in Day 1, reuse it as a sales discovery tool in Day 2, deepen it as a needs-analysis framework in Day 3. The same structure gains new meaning at each return — this is the mechanism of interleaved learning.
4. **Concrete metrics embedded in the content:** The Farmers 5-4-3-2-1 system (5 new marketing initiatives per month, 4 cross-marketing programs, 3 appointments scheduled daily, 2 kept, 1 new customer per day averaging 2 policies) turns abstract sales goals into a traceable system. Metrics are not presented as a slide — they emerge from a session where participants calculate backwards from their vision poster to derive what their weekly targets must be.
5. **Role-reversal practice:** Participants alternate between practitioner and client roles. Being the client is not a rest — it is a retrieval exercise that exposes gaps in understanding you did not know you had.

**Session design rule:** Divide each session into segments of no more than 25–30 minutes on any single domain. After that segment, pivot to a different domain. Return to the first domain later in the same day with a new application of the same concept.

### Template B — Certification Cycle (Jiffy Lube Model)

**Best for:** Procedural skills with safety, quality, or regulatory requirements. Franchises, service operations, healthcare, technical trades. Contexts where a minimum competency threshold must be demonstrated before the employee can work unsupervised.

**Core mechanics:**
1. **E-learning with embedded retrieval:** Pre-work is not passive video. It is interactive modules with frequent embedded quizzes — not summative tests at the end, but retrieval questions interspersed throughout. Learners must score 80% or better before proceeding to on-job training. This threshold forces mastery before hands-on work begins.
2. **Tell-show-do-review cycle:** For each procedural skill —
   - **Tell:** Explain what the step is and why it exists (not just what to do, but the reasoning that enables error recovery)
   - **Show:** Demonstrate the step with the learner observing
   - **Do:** Learner performs the step with the trainer present; the written standard is on-hand as the reference, not in the trainer's head
   - **Review:** Supervisor evaluates performance against the written standard and certifies competency in the permanent record
3. **Written standards as the invariant:** Every job is performed to a documented standard that specifies each step and its execution criteria. Without written standards, consistency across shifts and locations degrades; four workers produce four variants of the same product. The written standard also enables self-directed practice — a learner can rehearse against the checklist independently.
4. **Biennial recertification:** Certification is not permanent. Every two years, employees recertify to keep skills current and adapt to procedural and technical changes. This builds spaced retrieval into the organizational system, not just the individual's behavior.
5. **Progressive certification path:** As a technician completes certification in one position, they begin training for the next, until they have trained in all positions including management. The training is the career path, not a one-time event.

### Template C — Job Rotation and Worker-Led Improvement (Andersen Windows Model)

**Best for:** Manufacturing, operations, production environments where cross-training, quality consistency, and continuous improvement are all active goals. Contexts where workers have tacit knowledge about the production process that managers do not have.

**Core mechanics:**
1. **2-hour job rotation:** Workers rotate between positions on a fixed cycle (Andersen uses 2 hours). This is not a staffing convenience — it is an interleaved learning mechanism. Each rotation forces the worker to retrieve procedural knowledge from a different position, builds understanding of the integrated process, and broadens the worker's capacity to respond to unexpected events.
2. **Written standards at every station:** As in the certification model, every station has a written standard. Rotation without standards produces variability; rotation with standards produces cross-trained workers who all meet the same quality bar.
3. **Tell-show-do-review for onboarding:** New workers are paired with experienced workers; training is entirely on-job. The sequence is identical to Template B: tell, show, do, review — with feedback referenced to the written standard.
4. **Worker-led improvement (Kaizen events):** The key reversal in this model is that workers, not managers, are the subject-matter experts on the production process. When a production target is not being met, workers are asked to identify the problem and redesign the process to solve it. This is a structured generation activity: by articulating the problem, proposing changes, and teaching the redesign to others, workers deepen their own understanding of the process far beyond what passive training produces. The Andersen Cottage Grove plant reduced space requirements by 40%, doubled production, and cut costs in half over five months using this model.
5. **Stretch goals as learning catalysts:** Incremental improvement targets require incremental change. Stretch goals (that cannot be reached through incremental methods) require workers to fundamentally rethink the process — which is a high-quality generation task that produces durable, systemic understanding.

---

## Step 4 — Design the Interleaved Curriculum

**Why:** The architecture template tells you what shape the program has. This step converts that shape into a concrete session map the trainer can execute.

### For Template A (Interleaved Spiral)

Build a session-by-session map with the following structure:

- **Session opening (10–15 min):** Retrieve prior learning. Ask participants to recall what they learned in the previous session without notes — not as a test but as a warm-up that reactivates prior knowledge before new content is introduced. Correct gaps immediately.
- **Domain rotation (blocks of 20–25 min each):** Cycle through all content domains within the session. Each block should end with a brief generation task (a question to answer, a scenario to respond to, a metric to calculate) before moving on. Do not complete a domain block before pivoting.
- **Integration pivot:** Once all domains have been touched, run a scenario or exercise that requires participants to use knowledge from multiple domains simultaneously. This is the payoff of interleaving — cross-domain integration that blocked instruction cannot produce.
- **Session close (10 min):** Participants write down three things they learned and one question they still have. This is a generation and retrieval activity, not a satisfaction survey.

### For Template B (Certification Cycle)

Map each job certification as a unit:

- Pre-work (e-learning with embedded quizzing) → scored to 80% threshold
- On-job tell-show-do-review → supervisor-evaluated against written standard
- Certification recorded in permanent file
- Begin next certification unit
- Biennial recertification scheduled automatically

Track all progress on a visible dashboard (the Jiffy Lube "virtual dashboard" model) that shows each employee where they are in the certification path. Visibility motivates completion and allows managers to spot bottlenecks.

### For Template C (Job Rotation / Continuous Improvement)

Map the rotation schedule:

- Rotation frequency (Andersen: 2 hours)
- Written standard location for each station (physical or digital)
- Crew leader assignment and coaching responsibilities
- Improvement cycle trigger: when a production target is missed, convene a worker-led problem-solving session rather than issuing a directive
- Kaizen event protocol for major restructuring: cross-functional team (engineer + maintenance + crew leader + production workers), dedicated time (1 week), defined stretch goals, structured review process

---

## Step 5 — Add Spaced Retrieval Follow-Up Protocol

**Why:** The training event is where learning begins, not where it ends. Without a structured follow-up protocol, the forgetting curve reclaims most of what was learned within a week. The follow-up protocol is not optional — it is the mechanism that converts short-term training performance into long-term job competence.

The follow-up protocol has three components:

**1. Scheduled retrieval quizzes (post-training)**

For programs using Template A or B, schedule quizzes at:
- 48 hours after training ends (first retrieval while some memory remains — strengthens consolidation)
- 1 week after training (second retrieval — requires more effort, produces more durable trace)
- 1 month after training (third retrieval — the point at which most organizations declare "done"; this is actually when the most important retention work happens)

Quizzes should be low-stakes (not graded punitively) and delivered in the work context (mobile device, email, brief team meeting). The Qstream platform model — short spaced retrieval questions delivered via mobile — is a direct implementation of this protocol at scale.

**2. Transfer check-ins (manager-led)**

At 30, 60, and 90 days post-training, a manager or team lead conducts a brief structured conversation:
- "Walk me through how you handled [situation the training addressed] this week."
- "What part of the training has been hardest to apply? What's getting in the way?"
- "Show me [specific skill] using the written standard."

This is not a performance review — it is a coaching conversation that also functions as a retrieval event. Narrating what you did and why deepens encoding.

**3. Recertification trigger (for Template B)**

Set a calendar-based recertification schedule (Jiffy Lube uses 2 years). Recertification is not a formality — it is the organizational mechanism for spaced practice at scale. Build it into HR systems so that it happens automatically, not when someone remembers to schedule it.

---

## Step 6 — Output: Redesigned Training Program Plan

**Why:** An abstract recommendation does not change what trainers do on Monday. A concrete program plan does.

Produce a program plan document with the following sections:

**Program overview:**
- Training goal and transfer target (what behavior change, measurable within 90 days)
- Content domains (named and scoped)
- Architecture template selected and rationale
- Total duration (initial event + follow-up protocol)

**Session map:**
- For each session: date/number, duration, domain sequence, exercises, generation tasks, and closing retrieval activity
- Anti-pattern warnings embedded at each session: "Resist the urge to complete this domain block before moving to the next — the discomfort of switching is the mechanism of learning"

**Written standards checklist:**
- For Templates B and C: list each job/procedure that requires a written standard; flag which ones exist and which need to be created before training begins

**Follow-up protocol:**
- Exact dates for post-training retrieval quizzes
- Transfer check-in questions for 30/60/90-day conversations
- Recertification calendar trigger (if applicable)

**Evaluation criteria:**
- Leading indicators: quiz scores at 48 hours, 1 week, 1 month
- Lagging indicators: on-job performance metrics at 30/60/90 days
- Anti-pattern check: is anyone reverting to passive review or single-session cramming as a supplement to the program? Flag and correct.

---

## Worked Examples

### Example A: Sales Onboarding Redesign (Template A)

**Situation:** A regional insurance agency brings on 15 new agents per quarter. Current program: 3-day bootcamp with Day 1 on sales, Day 2 on products, Day 3 on compliance. No follow-up after day 3. Agents report forgetting most of what they learned within 2 weeks.

**Audit:** Massed-domain blocking (one domain per day), passive delivery (primarily slide lectures), training-as-event (no follow-up). Primary cost: domains learned in isolation cannot be integrated when a real customer conversation requires combining sales technique with product knowledge and compliance awareness simultaneously.

**Architecture:** Template A — Interleaved Spiral Curriculum.

**Redesign:**
- Day 1 opens with a vision exercise (not a slide deck): agents build a concrete picture of what a successful agency looks like for them in 3 years, deriving the revenue and policy targets backward from that vision.
- Each day cycles through all three content domains in 25-minute segments. Day 1 introduces a client discovery framework (FORE equivalent) as an icebreaker; Day 2 returns to it as a product-needs tool; Day 3 applies it in a compliance conversation.
- Every session includes role-reversal practice: one agent plays prospect, one plays agent. The "prospect" role is as instructive as the "agent" role because gaps in understanding become visible when you have to respond spontaneously to questions.
- Post-training: retrieval quizzes delivered by email at 48 hours, 1 week, and 1 month. Manager check-in at 30 days: "Walk me through a recent prospect conversation — what did you ask first, and why?"

---

### Example B: Technical Certification Rollout (Template B)

**Situation:** A multi-site automotive service franchise (8 locations, 65 employees) has no consistent certification process. New hires shadow an experienced worker for a few days, then work unsupervised. Service quality varies significantly by location.

**Audit:** No written standards (four workers, four variants), no threshold-gated certification, no recertification schedule. Training is apprenticeship by observation — modeling without structured retrieval or documented criteria.

**Architecture:** Template B — Certification Cycle.

**Redesign:**
- Create written standards for each of the 8 service positions. Each standard lists every step and the acceptable quality criteria for each step.
- Pre-work: interactive e-learning for each position, with retrieval questions every 3–5 minutes of content. Threshold: 80% before on-job training begins.
- On-job training follows tell-show-do-review for each step in the written standard. Supervisor certifies each step; certification is recorded in a shared file.
- New employees begin certification in one position, complete it, then begin the next position. All employees eventually certified in all 8 positions.
- Recertification calendar: every 2 years, all employees recertify in their primary positions; flag any procedural changes requiring immediate recertification.

---

### Example C: Production Floor Cross-Training (Template C)

**Situation:** A manufacturing facility has high variability in output quality across shifts. Workers are specialized in their station and cannot cover for absent colleagues. Management issues directives when targets are missed but does not see improvement.

**Audit:** No job rotation (workers locked to single stations — equivalent to massed practice), no written standards at each station, problem-solving directed by management rather than generated by workers.

**Architecture:** Template C — Job Rotation and Worker-Led Improvement.

**Redesign:**
- Implement 2-hour rotation across all stations within each cell. Pair rotation with written standards at each station so rotation produces cross-trained competence, not confusion.
- Onboard new workers via tell-show-do-review, with an experienced worker as the trainer at each station.
- When a production target is missed, convene the production team (not a manager meeting) to identify the problem: "What is causing this, and what would make it better?" Document and implement worker proposals.
- For a major productivity problem: run a 1-week Kaizen event with a cross-functional team (engineer + maintenance + crew leader + workers). Define a stretch goal that requires fundamental redesign. The team teaches each other the constraints of the process and redesigns it collaboratively. The teaching and problem-solving process is itself the learning.

---

## Quick Reference: Architecture Selection

```
TRAINING TYPE                          → TEMPLATE
------------------------------------------------------------
New-hire onboarding, 3–6 domains       → A: Interleaved Spiral Curriculum
Procedural/technical certification     → B: Certification Cycle
Production/operations cross-training   → C: Job Rotation + Worker-Led Improvement
Compliance/in-service (single event)   → B: Certification Cycle + spaced retrieval follow-up

ANTI-PATTERN DETECTED                  → FIX
------------------------------------------------------------
One domain per day                     → Interleave: cycle through all domains each session
Lecture-dominant delivery              → Replace with generation: role-play, calculate, produce
No post-training follow-up             → Add retrieval quizzes at 48h, 1 week, 1 month
No written standards                   → Document each step before on-job training begins
No recertification                     → Schedule biennial recertification in HR system

GENERATION EXERCISE TYPES              → WHEN TO USE
------------------------------------------------------------
Vision poster / future-state image     → Day 1 anchor; activates motivation and prior knowledge
FORE / discovery framework             → Build early, reuse in new contexts across sessions
Role reversal (be the customer)        → Every session; surfaces gaps recognition cannot reveal
Calculate-backward (metrics to vision) → Business/sales training; makes metrics personally meaningful
Worker-led problem diagnosis           → When performance targets are missed; generates understanding
Kaizen / redesign event                → When stretch goals require fundamental process change
```

---

## References

- `references/three-architecture-templates.md` — Full specifications for each template including session timing tables, written standard format, and certification record design
- `references/generation-exercise-library.md` — 12 generation exercise types (vision poster, FORE, role-reversal, calculate-backward, scenario simulation, etc.) with facilitation instructions and domain applicability
- `references/spaced-retrieval-follow-up-protocol.md` — Exact quiz cadences by training duration, sample question formats, Qstream and mobile delivery options, and 30/60/90-day check-in question banks

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-practice-schedule-designer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
