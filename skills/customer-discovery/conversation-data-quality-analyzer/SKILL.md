---
name: conversation-data-quality-analyzer
description: Analyze customer conversation notes or transcripts after a meeting to classify every statement as fact, compliment, fluff, or idea — separating real signal from noise. Use this skill whenever the user wants to review interview notes, check whether a customer call produced reliable data, figure out if enthusiastic feedback was genuine interest or polite lies, identify bad data patterns in a transcript, audit whether a conversation that "went great" actually produced usable facts, or suspects they are collecting compliments instead of validated evidence — even if they don't mention "data quality" or "bad data." Do NOT use this skill to write or improve questions before a conversation (use conversation-question-designer) or to evaluate whether a meeting produced real commitment signals like time, reputation, or money (use commitment-signal-evaluator).
version: 1
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [2]
domain: customer-discovery
tags: [customer-discovery, conversation-analysis, bad-data, data-quality, compliments, fluff, false-positives]
depends-on:
  - conversation-question-designer
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Conversation notes, transcript, or meeting summary from a customer conversation"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
---

# Conversation Data Quality Analyzer

## When to Use

You have notes or a transcript from a customer conversation and need to know how much of the data is actually reliable. Typical situations:

- The user just finished a customer conversation and wants the notes reviewed before acting on them
- The user has meeting notes and is about to update their product roadmap or assumptions based on them
- The user says a meeting "went really well" and wants to verify whether it actually produced signal
- The user has a transcript and wants to extract only the validated facts
- The user suspects they are getting false positives from conversations but cannot identify why
- The user has multiple conversation notes and wants a pattern analysis across them

Before starting, verify:
- Does the user have conversation notes, a transcript, or a meeting summary to analyze? (If not, this skill does not apply)
- Does the user know what product or problem area the conversation was about? (Needed to distinguish relevant facts from noise)

**Mode: Hybrid** -- The agent analyzes conversation notes or transcripts after the fact. The human conducted the actual conversation.

## Context & Input Gathering

### Required Context (must have -- ask if missing)

- **Conversation notes or transcript:** The raw material to analyze. This is the core input.
  - Check prompt for: pasted notes, quotes, transcript text, meeting summary
  - Check environment for: `conversation-notes/`, `meeting-*.md`, `transcript-*.md`, `notes-*.md`
  - If still missing, ask: "Please provide the conversation notes or transcript you want analyzed. You can paste them directly or point me to a file."

- **Product idea or problem area:** What the conversation was about. This is needed to distinguish relevant behavioral facts from unrelated statements.
  - Check prompt for: product descriptions, problem statements, startup ideas
  - Check environment for: `product-idea.md`, `README.md`
  - If still missing, ask: "What product or problem area was this conversation about? A sentence is enough."

### Observable Context (gather from environment)

- **Learning goals for the conversation:** What the user wanted to learn. This lets the analysis prioritize which facts matter.
  - Look for: `question-script.md`, `learning-log.md`, learning goals mentioned in the prompt
  - If unavailable: analyze all statements without goal-based prioritization

- **Previous conversation notes:** Past learnings for cross-referencing patterns
  - Look for: `conversation-notes/`, `learning-log.md`
  - If unavailable: analyze standalone

### Default Assumptions

- If no learning goals specified, analyze all customer statements without filtering by relevance
- If no product idea specified, classify data types but skip relevance assessment
- If notes are sparse (fewer than 5 statements), produce a shorter assessment with a note about limited data

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Conversation notes or transcript is available
- Product idea or problem area is known (or defaulted)

PROCEED WITH DEFAULTS when:
- Notes are available but no learning goals
- Product idea is approximate

MUST ASK when:
- No conversation notes, transcript, or meeting summary at all
```

## Process

### Step 1: Parse the Conversation into Individual Statements

**ACTION:** Read through the conversation notes or transcript and extract every distinct customer statement. Number each statement for reference. Separate the interviewer's statements from the customer's.

**WHY:** Bad data hides inside longer passages. A single paragraph of notes might contain one genuine fact, two compliments, and a piece of fluff. By atomizing the conversation into individual statements, each one can be classified independently. Without this step, compliments contaminate nearby facts -- a genuine workflow description followed by "this sounds really useful!" makes the whole passage feel validated when only the workflow part was real data.

**IF** the input is a raw transcript with speaker labels, extract only the customer's statements
**IF** the input is unstructured notes without clear attribution, flag any ambiguous statements where it is unclear whether the customer or the interviewer said it
**IF** the input contains the interviewer's questions, preserve them alongside the customer responses (the question quality affects the response quality)

### Step 2: Classify Each Statement

**ACTION:** Classify every customer statement into one of four categories using the classification rules below.

**WHY:** The four categories represent fundamentally different levels of reliability. Facts are usable data. Compliments, fluff, and ideas feel like data but carry zero validated signal. Misclassifying even one compliment as a fact can send a product team in the wrong direction for months. The classification system catches the specific ways customer conversations produce false positives.

**Classification rules:**

| Category | Definition | Detection Markers | Reliability |
|----------|-----------|-------------------|-------------|
| **FACT** | A concrete, specific statement about past behavior, current workflow, measurable outcome, or observable reality | Past tense, specific details (names, dates, numbers, tools), describes what actually happened, references current process | HIGH -- usable data |
| **COMPLIMENT** | Positive feedback about your idea, product, or pitch that costs the speaker nothing to say | "That's cool," "I love it," "Sounds great," "That would be awesome," any praise directed at your concept rather than describing their situation | ZERO -- entirely worthless |
| **FLUFF** | Vague, non-specific feedback that sounds like data but lacks concrete grounding | Three shapes: (1) Generic claims: "I usually," "I always," "I never"; (2) Future-tense promises: "I would," "I will," "I would definitely buy that"; (3) Hypothetical maybes: "I might," "I could," "I could see myself" | ZERO -- unreliable |
| **IDEA** | Feature requests, suggestions, or solutions proposed by the customer | "You should add...," "It would be great if...," "Can you make it do...," "What about syncing to...," "Have you thought about..." | LOW -- understand motivation, do not obey the request |

**FOR EACH** customer statement:
1. Assign a category: FACT, COMPLIMENT, FLUFF, or IDEA
2. Note which specific markers triggered the classification
3. If FLUFF, identify which of the 3 shapes it matches (generic claim, future-tense promise, hypothetical maybe)
4. If a statement contains mixed types (e.g., a fact followed by a compliment), split and classify each part separately
5. Assess confidence: CLEAR (unambiguous classification) or BORDERLINE (could go either way -- explain why)

### Step 3: Detect Anti-Patterns in the Conversation

**ACTION:** Scan the full conversation for the 6 named anti-patterns that systematically produce bad data. Check both the interviewer's behavior (from questions asked) and the customer's responses.

**WHY:** Individual bad statements are symptoms. Anti-patterns are the disease. A conversation might contain 10 compliments because the interviewer was fishing for them, or 8 pieces of fluff because the interviewer asked fluff-inducing questions. Identifying the root-cause anti-pattern tells the user not just what went wrong in this conversation, but what to fix for the next one.

**Anti-patterns to detect:**

| Anti-Pattern | What It Is | Detection Signals |
|-------------|-----------|-------------------|
| **Compliment Acceptance** | Treating compliments as validation data | Notes say "meeting went really well," "getting positive feedback," "everybody loves it." Compliments recorded as key takeaways. No facts to back up positive assessment. |
| **Fishing for Compliments** | Intentionally seeking approval instead of truth | Interviewer asked opinion-seeking questions: "Do you think it will work?", "Do you like it?" Questions that start with "Do you think my..." or "What do you think of our..." |
| **Ego Exposure Bias** (The Pathos Problem) | Accidentally triggering protective compliments by revealing how much you care | Interviewer shared personal stakes ("I quit my job for this," "This is my passion project"), asked for honest feedback while clearly invested ("I can take it -- tell me what you really think") |
| **Accepting Fluff** | Treating vague generics as concrete evidence | Fluff statements recorded without follow-up anchoring questions. No "when was the last time" or "can you walk me through" questions after generic claims. Fluffy responses accepted at face value. |
| **Being Pitchy** | Talking about the product more than listening | Interviewer talked for extended stretches without asking questions. Multiple product descriptions or feature explanations. Customer responses get shorter as conversation progresses. Symptoms: "No no, I don't think you get it," "Yes, but it also does this!" |
| **Obeying Feature Requests** | Adding feature requests to the roadmap without digging into the motivation behind them | Ideas recorded as action items without "why do you want that?" follow-up. Feature requests listed without underlying motivation. No "how are you coping without it?" questions. |

**IF** the input includes interviewer questions, check each question for fluff-inducing patterns: "Do you ever...", "Would you ever...", "What do you usually...", "Do you think you...", "Might you...", "Could you see yourself..."
**IF** the conversation ended with a compliment and no commitment, flag as potential zombie lead pattern

### Step 4: Assess Overall Conversation Quality

**ACTION:** Calculate a data quality summary and assess whether the conversation produced actionable signal.

**WHY:** A conversation can feel productive while producing zero usable data. By quantifying the ratio of facts to noise, the user gets an objective measure of conversation quality instead of relying on their gut feeling (which is exactly what compliments exploit). This assessment also reveals whether the conversation is worth following up on or whether it needs to be re-run with better questions.

**Calculate:**
- Total customer statements analyzed
- Count and percentage by category (FACT / COMPLIMENT / FLUFF / IDEA)
- Number of anti-patterns detected
- Overall quality rating:
  - **STRONG:** More than 60% facts, zero or one anti-patterns detected, facts include specific past behaviors
  - **MIXED:** 30-60% facts, or facts present but contaminated by significant fluff/compliments
  - **WEAK:** Less than 30% facts, or multiple anti-patterns detected, or no concrete past behaviors
  - **EMPTY:** Mostly compliments and fluff with no usable facts

**IF** quality is WEAK or EMPTY, recommend which questions to ask in a follow-up conversation to recover the missing data (reference the `conversation-question-designer` skill for designing those questions)

### Step 5: Extract the Cleaned Insights Summary

**ACTION:** Produce a cleaned insights document containing only validated facts, with compliments and fluff stripped out. For each idea (feature request), include the underlying motivation if it was uncovered.

**WHY:** The whole point of this analysis is to produce a document the user can trust and act on. The cleaned summary separates what was actually learned from what felt learned. This is the artifact that should inform product decisions -- not the raw notes, which contain a mix of signal and noise.

**Cleaned summary structure:**

```markdown
# Conversation Data Quality Assessment

## Metadata
- **Date:** [conversation date if known]
- **Customer/Interviewee:** [name or identifier]
- **Product/Problem Area:** [from context]
- **Conversation Quality:** [STRONG / MIXED / WEAK / EMPTY]

## Quality Breakdown
| Category | Count | Percentage |
|----------|-------|------------|
| Facts | X | X% |
| Compliments | X | X% |
| Fluff | X | X% |
| Ideas | X | X% |

## Validated Facts (usable data)
1. [Fact statement] — *[why this is reliable: specific past behavior, named tool, concrete number]*
2. [Fact statement] — *[why this is reliable]*
...

## Ideas with Motivations (understand, do not obey)
1. **Request:** [what they asked for]
   **Underlying motivation:** [why they want it, if uncovered]
   **Currently coping by:** [their workaround, if mentioned]
   *If motivation was NOT explored:* Flag for follow-up — ask "Why do you want that?" and "How are you coping without it?"

## Discarded Data (compliments and fluff)
| # | Statement | Category | Why Discarded |
|---|-----------|----------|---------------|
| 1 | [statement] | COMPLIMENT | [explanation] |
| 2 | [statement] | FLUFF (generic claim) | [explanation] |
...

## Anti-Patterns Detected
- **[Pattern name]:** [evidence from conversation] → [what to fix next time]

## Recommendations
- [Specific actions: follow-up questions to ask, questions to redesign, anti-patterns to watch for]
```

**IF** the user provided a file path or working directory, write the output to `data-quality-assessment.md`
**ELSE** present the output directly in the conversation

## Examples

### Example 1: Founder reviews notes from a "great" meeting about a project management tool

**Scenario:** A founder building a project management tool for freelancers says: "I had a great conversation with a freelance designer yesterday. Here are my notes."

**Trigger:** User provides meeting notes containing a mix of facts, compliments, and fluff.

**Process:**
1. Parse notes into individual statements
2. Classify each statement:
   - "I usually manage projects with sticky notes and email" -> FLUFF (generic claim: "I usually")
   - "Last month I lost a client because I sent the wrong version of a file" -> FACT (specific past event with consequence)
   - "Your tool sounds amazing, I would totally use it" -> COMPLIMENT + FLUFF ("sounds amazing" = compliment, "I would totally use it" = future-tense promise)
   - "I have 6 active clients right now and track them in a spreadsheet" -> FACT (specific current state with number)
   - "You should add a Figma integration" -> IDEA (feature request)
   - "It would save me so much time" -> FLUFF (hypothetical future)
3. Detect anti-patterns: Ego Exposure Bias (founder mentioned "my tool" triggering compliments), Obeying Feature Requests (Figma integration noted without asking why)
4. Quality: MIXED -- 2 facts (33%), 1 compliment, 2 fluff, 1 idea

**Output (abbreviated):**
```
Conversation Quality: MIXED

Validated Facts:
1. Lost a client last month due to sending wrong file version — specific past event with real consequence
2. Has 6 active clients tracked in a spreadsheet — concrete current workflow with number

Ideas with Motivations:
1. Request: Figma integration
   Underlying motivation: NOT EXPLORED — follow up with "Why do you want that?" and "What would that let you do?"

Discarded:
- "I usually manage projects with sticky notes" — FLUFF (generic claim, ask "walk me through your last project")
- "Your tool sounds amazing" — COMPLIMENT (zero data)
- "I would totally use it" — FLUFF (future-tense promise, the world's most deadly fluff)

Anti-Patterns:
- Ego Exposure Bias: Mentioned "my tool" which triggered protective compliments
- Obeying Feature Requests: Figma integration recorded without motivation digging

Recommendations:
- Follow up to anchor the "sticky notes and email" claim: "Walk me through how you managed your most recent client project from start to finish"
- Dig into Figma integration request: "Why do you want that? How are you coping without it?"
- Use conversation-question-designer to redesign questions that avoid mentioning the product
```

---

### Example 2: Product manager analyzes a transcript full of enthusiastic but empty responses

**Scenario:** A product manager shares a transcript from a call about an automated reporting feature. The customer was very enthusiastic throughout.

**Trigger:** User provides a transcript where the customer gave many positive responses but few concrete details.

**Process:**
1. Parse transcript into 15 customer statements
2. Classify: 2 FACTS, 7 COMPLIMENTS, 4 FLUFF, 2 IDEAS
3. Detect anti-patterns: Being Pitchy (PM talked for 60% of the conversation), Compliment Acceptance (PM noted "great call" at the end), Fishing for Compliments ("Don't you think automated reports would save time?")
4. Quality: WEAK -- 13% facts, 3 anti-patterns

**Output (abbreviated):**
```
Conversation Quality: WEAK

Validated Facts:
1. Team spends "nearly a week at the end of each month" pulling reports together — specific time cost
2. Currently using Excel and email to coordinate — specific current tools

Discarded (13 statements):
- "That's exactly what we need!" — COMPLIMENT
- "I would definitely buy that" — FLUFF (future-tense promise; the deadliest fluff)
- "We'd probably use it every day" — FLUFF (hypothetical maybe + future-tense)
- "You should integrate with Salesforce" — IDEA (motivation not explored)
...

Anti-Patterns:
- Being Pitchy: PM described the product for 4 consecutive exchanges without asking a question
- Fishing for Compliments: Asked "Don't you think automated reports would save time?" (opinion + hypothetical)
- Compliment Acceptance: PM wrote "great call" in notes — the 2 facts do not justify this assessment

Recommendations:
- This conversation needs a complete redo with the conversation-question-designer skill
- The 2 facts are valuable — dig deeper with: "Walk me through the last time you pulled the monthly report together"
- Do NOT put "Salesforce integration" on the roadmap until you ask: "Why Salesforce specifically? What would that let you do that you can't do now?"
```

---

### Example 3: Analyzing sparse notes from a casual conversation

**Scenario:** A founder jotted down quick notes from a casual coffee chat: "Met Sarah, runs a bakery. Says inventory is a nightmare. Would love an app for it. Gave me her card."

**Trigger:** User provides minimal notes from an informal conversation.

**Process:**
1. Parse into 3 statements: "inventory is a nightmare" (borderline -- emotional but vague), "would love an app for it" (FLUFF), "gave me her card" (FACT -- concrete action)
2. Quality: WEAK -- too few data points, one fact is a social gesture not a commitment

**Output (abbreviated):**
```
Conversation Quality: WEAK (insufficient data)

Validated Facts:
1. Gave business card — concrete action, but this is a social gesture, not a commitment signal. A card costs nothing.

Borderline (needs anchoring):
- "Inventory is a nightmare" — emotional signal worth digging into, but currently vague. Follow up: "Tell me about the last time inventory caused a problem. What happened?"

Discarded:
- "Would love an app for it" — FLUFF (future-tense promise)

Note: This conversation produced too little data to draw conclusions. The emotional signal about inventory is promising but unvalidated. Recommended follow-up questions:
- "When was the last time inventory went wrong? Walk me through what happened."
- "What are you using to track inventory right now?"
- "How much time do you spend on inventory management each week?"
- "What have you tried to fix this?"
```

## Key Principles

- **Compliments are the fool's gold of customer learning: shiny, distracting, and entirely worthless** -- Even genuine compliments contain zero usable data. A venture capitalist (a professional judge of the future) is wrong far more often than right. A random person's opinion has even less weight. The only exception is industry experts who have built very similar businesses. Everyone else's approval is noise.

- **The deadliest fluff sounds the most concrete** -- "I would definitely buy that" feels like a commitment because it uses decisive language. But it is a future-tense promise about a hypothetical, which means it is pure fluff. The first startup the author worked at fell for this trap and lost ten million dollars. Always check: did they describe something that already happened, or something they imagine happening?

- **Ideas and feature requests should be understood, but not obeyed** -- When a customer says "you should add Excel sync," the wrong response is to write "Excel sync" on the roadmap. The right response is "Why do you want that? What would that let you do?" The request is a surface symptom. The underlying motivation is the real data. The author built three months of unnecessary analytics features for MTV because he accepted the feature request at face value instead of asking why.

- **Anti-patterns are the disease; bad data is the symptom** -- A conversation full of compliments usually means the interviewer was fishing for them or exposed their ego. A conversation full of fluff usually means the interviewer asked fluff-inducing questions. Fixing individual data points is pointless if the underlying conversational behavior remains. This skill diagnoses both.

- **A conversation that "went well" is a warning sign, not a positive signal** -- When you leave a meeting feeling great about it, that feeling is almost always driven by compliments. Genuine learning conversations often feel uncomfortable because you are hearing things you did not want to hear. The best conversations produce facts and commitments, not warm feelings.

## References

- For the complete bad data taxonomy with all fluff shapes, anti-pattern symptoms, and detection markers, see [bad-data-classification-guide.md](references/bad-data-classification-guide.md)
- For designing better questions before the next conversation, use the `conversation-question-designer` skill
- For evaluating whether a meeting produced real commitment signals (time, reputation, money), use the `commitment-signal-evaluator` skill
