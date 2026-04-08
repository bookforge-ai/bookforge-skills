---
name: structured-reflection-protocol
description: Run a structured reflection or debrief after any learning experience, project, procedure, or performance to turn raw experience into durable skill. Use this skill whenever the user wants to do an after-action review, write a learning journal entry, debrief a session, run a post-mortem, reflect on what went well and what to improve, turn a recent experience into a lesson they will remember, create a reflection document after completing a course chapter or training, or consolidate learning from a recent event — even if they do not use the words "reflection" or "retrieval." Works for students, professionals, coaches, clinicians, writers, teachers, and anyone learning from experience. Do NOT use this skill to build a spaced repetition quiz system (use retrieval-practice-study-system) or to analyze an external document for content (use a different skill).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/structured-reflection-protocol
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [2, 4, 8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "reflection", "experiential-learning"]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Description of a recent experience, session notes, procedure record, or brief summary of what just happened"
  tools-required: [Write]
  tools-optional: [Read]
  mcps-required: []
  environment: "Any agent environment. Write access needed to save the reflection document."
---

# Structured Reflection Protocol

## When to Use

You have just completed something — a surgery, a class session, a project sprint, a difficult conversation, a writing draft, a practice run — and you want to convert that raw experience into durable, retrievable learning before it fades.

Typical entry points:
- Just finished a procedure, class, training session, or performance
- Writing a learning journal and want more than a summary
- Running an after-action review with a team or for yourself
- Noticing a recurring mistake and wanting to break the pattern
- Finishing a course chapter or reading assignment and wanting it to actually stick

Before starting, verify:
- Is there a specific, bounded experience to reflect on? (If the user wants to reflect on "everything lately," narrow to one recent event first.)
- Is this for individual use or a team debrief? (Team debriefs need all participants contributing; flag if only one person's perspective is available.)

**Mode: Hybrid** — The agent structures the reflection, asks the four questions, and produces the output document. The human supplies the experience content. The agent connects dots, surfaces patterns, and generates the "strategies for next time" section.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **What just happened:** A description of the experience being reflected on. Even a rough sentence works: "I taught my first class session today" or "We just finished the sprint review."
  -> Check prompt for: descriptions of recent events, project completions, session summaries, procedure notes
  -> If missing, ask: "What experience do you want to reflect on? Give me a brief description of what happened."

- **Domain or role:** What kind of practitioner is this person? (student, surgeon, coach, writer, etc.)
  -> Shapes which reflection format to use and the vocabulary of the output
  -> If missing, infer from context; note the assumption

### Observable Context (gather from environment)

- **Prior reflection documents:** Any previous reflection files or learning journals
  -> Look for: `reflection-*.md`, `learning-journal.md`, `after-action-*.md`
  -> If found: reference them for pattern recognition ("this is the third time you've noted X")

- **Goals or intentions set before the experience:** What the person was trying to accomplish
  -> Look for: planning documents, session outlines, stated objectives
  -> If unavailable: derive from the experience description

### Default Assumptions

- If no domain specified -> use domain-neutral language; adapt examples to match whatever domain the user mentions
- If no prior reflections available -> treat as first reflection in a series
- If the experience was negative or difficult -> reflect without judgment; the protocol works regardless of outcome
- If the user is in a hurry -> offer the short-form output (four answers + three action items) rather than the full document

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- At least one experience is described (even briefly)
- The time frame is clear (this happened recently, not months ago)

PROCEED WITH DEFAULTS when:
- Domain or role is vague
- No prior reflections exist

MUST ASK when:
- No experience at all has been described
- The event is so old that memory is likely unreliable (use a note: "recall may be approximate")
```

## Process

### Step 1: Gather the Experience

**ACTION:** Ask the user to describe what just happened, or read the input they have already provided. Establish the bounded event to reflect on.

**WHY:** Reflection requires a specific target. Vague, open-ended reflection ("I've been learning a lot lately") rarely produces retrievable insights because the mind cannot reconstruct specific episodes. The neurosurgeon Mike Ebersold described his reflection practice as always starting from a specific surgery: "Something would come up in surgery that I had difficulty with, and then I'd go home that night thinking about what happened." The bounded experience is the anchor.

**IF** the user provides a file or notes -> read them and summarize the key events in 3-5 bullet points before proceeding. Show this summary to the user and ask if anything important is missing.

**IF** the user describes the experience verbally in the prompt -> paraphrase it back in 2-3 sentences to confirm understanding before asking the reflection questions.

**OUTPUT:** A 2-5 sentence statement of what the experience was, who was involved, and what the intended outcome had been.

---

### Step 2: Run the Four Reflection Questions

**ACTION:** Work through each of the four questions in order. For each question, prompt the user for their answer, then elaborate and deepen it before moving to the next.

**WHY:** These four questions are not arbitrary. Each one activates a different cognitive mechanism that strengthens learning:
- Question 1 (what went well) consolidates the memory of successful strategies, making them easier to retrieve and repeat.
- Question 2 (what could go better) forces retrieval of what was difficult — the effortful retrieval itself strengthens the memory trace.
- Question 3 (what does this remind me of) is elaboration: connecting new experience to prior knowledge creates multiple retrieval paths and deepens understanding.
- Question 4 (strategies for next time) is mental rehearsal: visualizing the corrected action consolidates it before the next performance, the same mechanism Ebersold used to pre-solve surgical problems the night before returning to the OR.

**The four questions:**

#### Q1: What went well?

Prompt to the user: "What worked in this experience? What did you do that you would do exactly the same way next time?"

**Agent role:**
- Affirm specific behaviors, not vague positives ("your pacing was effective" not "it went well")
- If the user says "nothing," push gently: "What was the outcome? Did you complete the task? What enabled that?"
- Identify 1-3 concrete behaviors or decisions that contributed to success

**WHY this question first:** Starting with success is not merely motivational. It retrieves the memory in a positive state, reducing the defensiveness that causes people to shut down before they reach the harder questions. It also identifies what to protect — the strategies worth preserving.

#### Q2: What could have gone better?

Prompt to the user: "Where did you struggle? What would you change if you could do it again right now?"

**Agent role:**
- Press for specificity: "At which exact moment did things feel difficult?"
- Distinguish between knowledge gaps (didn't know what to do) and execution gaps (knew what to do but couldn't execute under pressure)
- If the user blames external factors entirely, acknowledge them but redirect: "Granted the conditions were difficult — what could you have done differently within those conditions?"

**WHY this question matters:** Difficulty is where the most durable learning lives. The brain assigns higher priority to encoding surprising, effortful, or failed attempts because they signal situations that need future preparation. Surfacing what went wrong is not self-criticism — it is the specific mechanism by which expert practitioners build the dense situational awareness that novices lack.

#### Q3: What does this remind you of? What earlier experience or knowledge does it connect to?

Prompt to the user: "Have you encountered something like this before — in this domain or a different one? What principles or frameworks does this experience illuminate or challenge?"

**Agent role:**
- Offer connections the user may not have seen: "This sounds similar to [X pattern] — does that resonance feel right?"
- Surface both same-domain analogies ("this is like the time you...") and cross-domain analogies ("this has the structure of...")
- If the user draws a blank, offer a prompt: "What does this remind you of from a book, a past job, a different field?"

**WHY this question is the multiplier:** Elaboration — connecting new learning to prior knowledge — is one of the most powerful learning mechanisms available. Every connection created is an additional retrieval path. A piece of learning with many connections is far more durable and accessible than isolated information. This is why expert practitioners can solve problems that novices cannot: their knowledge is richly interconnected, not just voluminous.

#### Q4: What strategies will you use next time?

Prompt to the user: "If you faced the exact same situation tomorrow, what would you do differently? What specific technique, preparation step, or adjustment would you make?"

**Agent role:**
- Push for concrete, executable strategies, not vague intentions ("I will prepare a list of three fallback questions before entering any difficult conversation" not "I will be better prepared")
- Include mental rehearsal: "Walk me through the moment where things got hard. Now describe what the corrected version looks like."
- If the user identifies multiple strategies, help prioritize to the 2-3 most impactful

**WHY mental rehearsal matters:** Visualization and mental rehearsal activate many of the same neural pathways as physical practice. Ebersold's reflection practice was not just verbal — he would mentally walk through the corrected surgical technique, seeing his hands working, before attempting it in the OR. This pre-consolidates the improved pattern. Football coaches Vince Dooley used reflection and mental rehearsal with his players to lock in playbook adjustments before the next game.

**OUTPUT after Step 2:** Four completed, elaborated answers — specific behaviors, honest analysis of difficulty, at least two connections to prior knowledge, and 2-3 concrete strategies for next time.

---

### Step 3: Select and Apply the Reflection Format

**ACTION:** Based on the domain, time available, and what was learned in Steps 1-2, select the most appropriate output format and produce the reflection document.

**WHY:** Different contexts benefit from different reflection structures. A 10-minute free-recall session serves a student differently than a structured after-action review serves a surgical team. The format should fit the practitioner's context, not the other way around.

**Format A: Free Recall (10 minutes, blank page)**

Best for: Students, individual learners, anyone with < 15 minutes, first reflection in a new domain.

Instructions to the user:
1. Close all notes, books, and references.
2. Set a timer for 10 minutes.
3. Write everything you can remember from the experience (or, for a course session, from the material just covered) — facts, sequences, confusing parts, surprising moments, anything.
4. Do not worry about organization. The retrieval effort is the point.
5. After 10 minutes, review what you wrote. Note what was easy to recall and what was absent.

**Agent role:** After the user completes free recall, read their output and identify:
- What they recalled easily (well-consolidated)
- What they recalled with uncertainty (needs one more retrieval session)
- What was absent entirely (likely needs re-encoding from the source)

This calibration is the most accurate feedback mechanism available — it shows the learner exactly where their memory is reliable versus where it only feels reliable.

**Format B: Learning Paragraph (Wenderoth Method)**

Best for: Students in courses, practitioners in training programs, weekly reflection practice.

Biology professor Mary Pat Wenderoth assigns weekly "learning paragraphs" in which students reflect on what they learned the previous week and characterize how their class learning connects to life outside class. This is a structured elaboration exercise, not a summary.

Structure:
1. In 1-2 sentences: What was the most important thing you learned this week/in this session?
2. In 2-3 sentences: How does it connect to what you already knew before this course/experience?
3. In 1-2 sentences: Where else does this appear — in your work, your life, another field?
4. In 1-2 sentences: What question does this raise that you have not yet answered?

**Agent role:** Read the completed paragraph and flag weak elaborations ("this connects to things I already know" is not an elaboration — ask the user to name what specifically).

**Format C: Structured Debrief (Ebersold Post-Procedure Method)**

Best for: Clinical procedures, high-stakes performances, team after-action reviews, any complex multi-step event.

This is the format Mike Ebersold used after difficult surgeries. It is structured around the gap between planned and actual performance.

Structure:
```
DEBRIEF RECORD
Experience: [procedure, project, session name]
Date: [date]
Participants: [if team]

WHAT WAS PLANNED
- Intended approach:
- Expected difficulties:
- Preparation steps taken:

WHAT ACTUALLY HAPPENED
- Where the plan held:
- Where the plan broke down:
- Unexpected events:

TECHNICAL ANALYSIS
- Root cause of any gap between plan and execution:
- Knowledge gap vs. execution gap:
- Environmental factors beyond control:

IMPROVEMENTS FOR NEXT TIME
- Technique adjustment:
- Preparation adjustment:
- Mental rehearsal target (what to visualize before next attempt):

WHAT TO TEACH OR SHARE
- What would be useful for a colleague or student to know?
```

**Agent role:** Complete the non-human fields from the experience description. Fill in analysis sections with the outputs from Step 2. Present the completed document for review.

---

### Step 4: Produce and Save the Reflection Output

**ACTION:** Compile the four-question answers and the selected format into a single, dated reflection document. If a file path or working directory is available, write it to disk.

**WHY:** Reflection documents are only as useful as their retrievability. Notes that exist only in conversation history become inaccessible within days. Writing the document to a file preserves it for future pattern recognition — noticing, for example, that "rushed preparation" appears in four consecutive after-action reviews signals a systemic habit to change, not just an isolated incident.

**Output document structure:**

```markdown
# Reflection: [Experience Name]
**Date:** [date]
**Domain/Role:** [domain]
**Duration of experience:** [approximate]

## What Happened
[2-5 sentence description]

## Four Questions

### What went well?
[Specific behaviors and decisions that worked — not vague positives]

### What could have gone better?
[Specific difficulty moments, honest analysis — knowledge gap vs. execution gap]

### What does this remind me of?
[Connections to prior experiences, frameworks, cross-domain analogies]

### Strategies for next time
1. [Concrete, executable strategy]
2. [Concrete, executable strategy]
3. [Optional third strategy]

## Mental Rehearsal Target
[A one-paragraph description of the corrected action, written in present tense as if performing it correctly right now]

## Action Items
- [ ] [Specific follow-up action — study, practice, consult, prepare]
- [ ] [If applicable: share this learning with whom, by when]
```

**IF** a working directory is available -> write to `reflection-[YYYY-MM-DD]-[slug].md`
**ELSE** -> present the completed document directly in the conversation

---

## Examples

**Scenario: Medical student after a difficult patient case presentation**

Trigger: "I just finished presenting a complex case in rounds. It went okay but I know I fumbled the differential diagnosis section. I want to make sure I learn from this."

Process:
1. Experience: Case presentation in medical rounds, differential diagnosis section was weak.
2. Four questions:
   - Q1: "I stayed calm and presented the history clearly. Attendings noted my physical exam findings were thorough."
   - Q2: "When asked why I hadn't included X in the differential, I blanked. I hadn't thought through the less common causes."
   - Q3: "This reminds me of how I studied anatomy — I memorized structures but not their clinical implications. Same pattern: knowing facts but not knowing what to do with them."
   - Q4: "Next time, before any presentation, I'll generate my differential by ruling out the dangerous diagnoses first, not just listing the common ones."
3. Format: Learning Paragraph (student context, moderate time available).

Output (abbreviated):
```
## Four Questions

### What went well?
Presented the history in a clear chronological sequence. Physical exam findings
were complete and well-organized. Remained composed under direct questioning.

### What could have gone better?
The differential diagnosis was shallow — I listed common causes but had not
systematically worked through the high-acuity diagnoses to exclude first.
When challenged on a rare diagnosis, I had no reasoning to offer. This is
an execution gap: I know the framework (dangerous diagnoses first) but
did not apply it under pressure.

### What does this remind me of?
This is the same pattern as my anatomy studying: I memorized structures but
missed their clinical relevance. Isolated facts without clinical reasoning
frameworks. Also reminds me of debugging code — you have to exclude the
catastrophic failures first before assuming it's a minor issue.

### Strategies for next time
1. For every presentation, explicitly work through the "must not miss" diagnoses
   before listing common ones. Write them down even if I'm confident they're excluded.
2. Practice presenting differentials out loud to a study partner twice per week —
   the retrieval pressure of a live audience surfaces blanks that solo review misses.

## Mental Rehearsal Target
Standing at the whiteboard, I've just presented the history. Before listing
my differential, I pause, say "Let me start with the diagnoses we need to rule
out," and work through the dangerous possibilities with brief reasoning for why
each is or isn't supported by the data. I finish with the likely common cause.
The attending asks about the rare diagnosis. I cite the two findings that made
me downgrade its probability.
```

---

**Scenario: Writing teacher after a workshop session that lost the room**

Trigger: "I ran a 90-minute writing workshop today and lost the group around the 45-minute mark. They were engaged at the start but then checked out. I need to figure out what happened."

Process:
1. Experience: 90-minute writing workshop, engagement dropped at midpoint.
2. Four questions:
   - Q1: "The opening exercise worked — everyone participated and the energy was high."
   - Q2: "Around 45 minutes I shifted from exercises to explanation. Too much theory at once. I can see now that I talked for 20 minutes straight."
   - Q3: "This reminds me of the generation effect from learning science — learners retain more when they attempt a task before being shown the solution. I did the opposite: I explained the concept then had them practice."
   - Q4: "Flip the sequence every 15 minutes: attempt first, explain second. Keep explanations under 5 minutes."
3. Format: Structured Debrief (teaching context, identifying a repeatable technique error).

---

**Scenario: Undercover police detective after a difficult surveillance operation**

Trigger: "Just finished a long undercover operation. We got what we needed but I made a cover story mistake at the 3-hour mark that almost burned me. I want to do a proper debrief before I forget the details."

Process:
1. Experience: Multi-hour undercover surveillance, cover story error at hour 3.
2. Four questions:
   - Q1: "Initial contact and rapport-building went well. The target accepted my presence without suspicion."
   - Q2: "At hour 3, fatigue caused a factual inconsistency in my cover story — I cited a location I had not visited yet in the timeline. The target noticed the hesitation."
   - Q3: "Reminds me of the 'seven-thousand-and-one' rule from jump school training: the moment you stop counting, you're in trouble. Sustained performance under stress requires explicit cuing, not willpower."
   - Q4: "Build in a 2-hour check: step away, review cover story facts, reset. Do not rely on memory under sustained stress without a structured refresh point."
3. Format: Structured Debrief (high-stakes procedure context, team operational record).

---

## Key Principles

- **Reflection is retrieval practice, not journaling** — The difference between a reflection that builds skill and a reflection that just feels good is effortful retrieval. The questions must surface specific memories, not vague impressions. "It went okay" is not a retrievable insight. "I used this specific technique at this moment and it produced this result" is.

- **Difficulty is data, not failure** — The questions are designed to surface struggle because that is where the most durable learning lives. A reflection that only records what went well is incomplete. What went wrong — and specifically why — is the material the brain will prioritize encoding for future use.

- **Mental rehearsal is not optional decoration** — Visualizing the corrected action before the next performance is a distinct cognitive step, not a summary of what was learned. The surgeon who thinks through the technique that night returns to the OR the next day with a pre-practiced neural pathway, not just an intention to do better.

- **Written beats remembered** — Reflection documents compound in value over time. A single reflection is useful. A month of reflections lets you see whether the same difficulty appears repeatedly, which tells you something very different than any single event could. Write it down.

- **Free recall first, then review sources** — When possible, attempt to write down everything you can remember before consulting notes or references. The retrieval attempt — even imperfect — strengthens the memory more than rereading ever will. The gaps you discover during free recall are your exact study targets.

## References

- For spaced retrieval practice as a study system (recurring self-quizzing schedule), see the `retrieval-practice-study-system` skill
- For the science behind retrieval, spacing, interleaving, and generation effects, see [references/cognitive-mechanisms.md](references/cognitive-mechanisms.md)
- For domain-specific reflection templates (clinical, writing, coaching, law enforcement), see [references/domain-reflection-templates.md](references/domain-reflection-templates.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
