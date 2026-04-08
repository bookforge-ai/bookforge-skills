---
name: conversation-learning-process
description: Structure the before-and-after process around customer conversations so learning actually reaches the whole team. Use this skill when the user needs to prepare a team for a batch of customer conversations, set up pre-conversation learning goals, create a note-taking system for customer interviews, review and categorize conversation notes using signal symbols, run a post-conversation team review, share customer insights across the team, diagnose whether conversations are producing real learning or just going through the motions, fix a learning bottleneck where one person hoards all customer insights, their team keeps having conversations but nothing changes or plans never update, or a co-founder or teammate is out of the loop on customer feedback — even if they don't explicitly say "learning process" or "team review." Do NOT use for analyzing a specific transcript for data quality (use conversation-data-quality-analyzer) or evaluating whether a prospect gave a real commitment (use commitment-signal-evaluator).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-mom-test/skills/conversation-learning-process
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [8]
tags: [customer-discovery, conversation-process, note-taking, team-learning, learning-goals, post-mortem, meeting-prep]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Team context, conversation notes, existing assumptions, or learning log"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
---

# Conversation Learning Process

## When to Use

Your team is about to start, is in the middle of, or has just finished a batch of customer conversations, and you need a structured process to extract maximum learning. Typical situations:

- The team is preparing for upcoming customer conversations and needs to agree on learning goals and roles
- Someone just finished a conversation and needs to categorize their notes and extract learnings
- The team has accumulated conversation notes but has not reviewed them together or updated their assumptions
- One person is doing all the customer conversations and the rest of the team is out of the loop
- Conversations feel unproductive -- the team suspects they are going through the motions without real learning
- The user wants to set up a repeatable learning process for their founding team

Before starting, verify:
- Does the team have a product idea or problem area they are exploring? (If not, they need to clarify this first)
- Has the team chosen a customer segment to focus on? (If not, consider using the `customer-segment-slicer` skill first)

**Mode: Hybrid** -- The agent structures the learning process, categorizes notes, and produces the learning review document. The humans conduct the actual conversations and participate in team review discussions.

## Context & Input Gathering

### Required Context (must have -- ask if missing)

- **Product idea or problem area:** What is the team building or exploring? This shapes which assumptions matter and what learning goals to set.
  -> Check prompt for: product descriptions, problem statements, startup ideas, business concepts
  -> Check environment for: `product-idea.md`, `README.md`, pitch documents
  -> If still missing, ask: "What product or problem area is your team exploring?"

- **Phase indicator:** Is this pre-conversation (preparing), mid-batch (reviewing notes), or post-batch (synthesizing learnings)?
  -> Check prompt for: mentions of "preparing," "just had a meeting," "reviewing notes," "planning conversations"
  -> If ambiguous, ask: "Are you preparing for upcoming conversations, reviewing notes from recent ones, or both?"

### Observable Context (gather from environment)

- **Team composition:** Who is on the team and who is attending conversations?
  -> Look for: team descriptions, org context, co-founder mentions
  -> If unavailable: assume a small founding team (2-3 people) and note the assumption

- **Existing conversation notes:** Raw notes from previous or recent conversations
  -> Look for: `conversation-notes/`, files with meeting dates, notes containing quotes
  -> If unavailable: assume first batch of conversations

- **Current assumptions or learning log:** What the team currently believes and what they have already validated or invalidated
  -> Look for: `learning-log.md`, `assumptions.md`, hypothesis documents
  -> If unavailable: help the team articulate their current assumptions as part of the process

- **Previous learning goals:** What the team was trying to learn in prior conversation batches
  -> Look for: prior question scripts, learning goal lists, `question-script.md`
  -> If unavailable: treat as first batch

### Default Assumptions

- If no team size specified -> assume 2-3 person founding team
- If no conversation history -> assume this is the first batch
- If no assumptions document -> help build one during the process
- If phase is unclear -> run the full before/after cycle

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Product idea or problem area is known
- Phase (before, during review, or after) is clear
- At least some team context exists (even approximate)

PROCEED WITH DEFAULTS when:
- Team composition is vague ("me and my co-founder")
- No prior conversation notes exist (first batch)

MUST ASK when:
- No product idea or problem area at all
- Cannot determine whether they need prep, review, or both
```

## Process

### Step 1: Diagnose the Current Learning Process

**ACTION:** Assess whether the team has a working learning process or is falling into common traps. Check for the learning bottleneck anti-pattern and going-through-the-motions symptoms.

**WHY:** Most teams default to a broken process where one person goes to all the meetings, takes poor notes, and becomes the sole repository of customer truth. This creates a de-facto dictatorship where "the customer said so" becomes an unchallengeable trump card. Even if the learning is accurate, it does not matter if it has not been communicated to the whole team. One founder's CTO quit over exactly this pattern, saying "We're never going to succeed if you keep changing what we're doing." The learning was true -- but it had not been shared.

**Learning bottleneck symptoms** -- flag if any are present:
- One person attends all customer meetings alone
- The team hears about customer insights secondhand ("I talked to customers and they said...")
- Product decisions are justified with "Because the customers told me so!" without shared evidence
- Technical co-founders say "I don't have time to talk to people -- I need to be coding!"
- Notes are not taken or not shared

**Going-through-the-motions symptoms** -- flag if any are present:
1. You are talking more than the customer is
2. The customer is complimenting you or your idea
3. You told them about your idea and do not know what is happening next
4. You do not have notes from the conversation
5. You have not reviewed your notes with your team
6. You got an unexpected answer and it did not change your idea or plans
7. You were not scared of any of the questions you asked
8. You are not sure which big question you are trying to answer by doing this

**IF** learning bottleneck symptoms are present -> flag this explicitly and recommend the team fixes it before continuing. The fix has three parts: prepping together, reviewing together, and taking good notes.
**IF** going-through-the-motions symptoms are present -> note which ones apply and address them in subsequent steps.
**IF** neither pattern is detected -> proceed to the appropriate phase.

**OUTPUT:** A brief diagnostic with any flags raised, plus a recommendation for which steps to focus on.

### Step 2: Set Pre-Conversation Learning Goals (Before Phase)

**ACTION:** Help the team define their 3 most important learning goals for the upcoming batch of conversations. Then identify conversation roles, write down assumptions, and do desk research triage.

**WHY:** If you do not know what you are trying to learn, you should not bother having the conversation. The minimum prep is answering "What do we want to learn from these guys?" Learning goals must be decided with the whole founding team -- both business and product should be represented -- because if you leave part of the company out of the prep, you end up missing their concerns in the conversations.

**Sub-steps:**

**2a. Define the 3 Big Learning Goals**

Work with the team to identify the 3 murkiest or most important unknowns right now. These should be framed as facts or behaviors to discover, not opinions to collect.

**IF** the team has prior conversation data -> review what was learned and what remains unknown. Pick up where you left off.
**IF** this is the first batch -> derive goals from the team's riskiest assumptions about the business.

To surface hidden risks, ask these two prep questions:
- "If this company were to fail, why would it have happened?"
- "What would have to be true for this to be a huge success?"

These are not long strategy discussions -- gut reactions are enough. They reveal which assumptions are load-bearing and should be tested first.

**2b. Assign Conversation Roles**

Meetings go best with two people:
- **Lead:** Focuses on talking, asking questions, and guiding the conversation
- **Note-taker:** Focuses on writing down exact quotes and signal annotations. Also watches for bad question patterns or missed signals -- jump in and fix them when noticed.

Do not send more than two people unless it is group-on-group. Three people interviewing someone can feel overwhelming. Going solo is fine once you are good at taking concise notes, but the main risk is that it is harder to catch yourself going off-track.

**IF** the team member doing conversations is shy -> suggest bringing a friend or co-founder to the first few conversations to play note-taker until they are comfortable leading.

**2c. Write Down Best Guesses**

Spend up to an hour writing down best guesses about what the person they are about to talk to cares about and wants. These guesses will probably be wrong, but having a skeleton makes it easier to stay on track and hit important points during the conversation.

**2d. Desk Research Triage**

For any question that could be answered with desk research (company background, industry trends, publicly available information), do that first. Do basic due diligence on LinkedIn and the company website. This takes 5 minutes and prevents wasting conversation time on questions the internet could answer.

**2e. Decide Target Commitments**

If the team has already learned the facts of their customer and industry, they should also know what commitment and next steps to push for at the end of the meeting. Define the ideal outcome.

**OUTPUT:** A prep document with:
- 3 numbered learning goals
- Conversation roles (lead + note-taker)
- Key assumptions to test
- Desk research notes (if applicable)
- Target commitment or next step to push for

### Step 3: Categorize Conversation Notes (During/After Phase)

**ACTION:** Take raw conversation notes and categorize each entry using the 12 signal symbols system. Tag each note with the appropriate symbol(s) and extract exact quotes.

**WHY:** Unstructured notes are almost as bad as no notes. Signal symbols turn raw conversation data into sortable, filterable intelligence. When the team reviews, they can pull all pain points across multiple conversations, find patterns in workarounds, and prioritize based on emotional weight. Without categorization, notes become an unsearchable pile that nobody looks at -- and notes are useless if you do not look at them.

**The 12 Signal Symbols** — see [references/note-taking-signal-symbols.md](references/note-taking-signal-symbols.md) for the complete symbol table (3 categories: Emotions, Their Life, Specifics).

**Processing rules:**

1. **Preserve exact quotes.** Wrap verbatim customer words in quotation marks. These can be used later in marketing language, fundraising decks, and to resolve arguments with skeptical teammates.
2. **One learning per entry.** Each note should capture a single insight, quote, or observation -- not a paragraph of mixed signals.
3. **Combine emotion + life symbols.** A pain point mentioned with anger `:( [pain]` carries far more weight than one mentioned casually `[pain]`. Flag these high-weight combinations.
4. **Tag follow-ups prominently.** Especially next steps promised as a condition of commitment -- these must be actioned promptly.

**IF** raw notes are provided -> categorize each entry with appropriate symbols
**IF** a transcript is provided -> extract key moments and categorize them
**IF** notes are missing or sparse -> flag this as a process problem and reconstruct what can be remembered (but acknowledge the data loss)

**OUTPUT:** Categorized notes with signal symbols applied to each entry.

### Step 4: Run the Post-Conversation Team Review

**ACTION:** Structure a team review session that covers three levels: content review (what was learned), meta-review (how the conversation went), and assumption updates.

**WHY:** The review is where learning actually transfers from one person's head to the whole team's shared understanding. It is tempting to skip because it sounds like a non-step, but skipping it creates the learning bottleneck. Disseminate learnings to your team as quickly and directly as possible, using notes and exact quotes. This keeps the team in sync, leads to better decisions, prevents arguments, and allows your whole team to benefit from the learning you have worked hard to acquire.

**4a. Content Review -- What Did We Learn?**

Walk through the categorized notes with the team. Focus on:
- Key quotes and what they reveal
- Main takeaways from each conversation
- Surprising or unexpected data points
- Patterns across multiple conversations (if reviewing a batch)

**4b. Meta-Review -- How Did the Conversation Go?**

Discuss the conversation process itself:
- Which questions worked well and which fell flat?
- Were there important signals or questions we missed?
- Did we slip into any bad patterns (pitching, accepting compliments, premature zoom)?
- How can we do better next time?

**WHY meta-review matters:** Customer conversation quality is more craft than science. You have to actively practice it to get better. Spending a few minutes on meta-level reflection after each conversation is a valuable skill for your team to develop. It will get less scary as you improve.

**4c. Assumption Update -- What Changed?**

For each of the team's current assumptions:
- Mark as VALIDATED if conversation evidence supports it (cite the specific evidence)
- Mark as INVALIDATED if conversation evidence contradicts it (cite the specific evidence)
- Mark as UNCERTAIN if evidence is mixed or insufficient
- Note any NEW assumptions that emerged from the conversations

**IF** an unexpected answer did not change the team's idea or plans -> flag this as a going-through-the-motions symptom. An unexpected answer that does not change anything means the team is either not listening or not asking important enough questions.

**OUTPUT:** Updated assumption list with evidence citations.

### Step 5: Set Next 3 Learning Goals

**ACTION:** Based on the review, decide the next 3 big questions for the next batch of conversations.

**WHY:** Learning goals evolve as you gather data. Questions that were murky last week may now be clear, while new questions have emerged. The team should always know their current list of 3 -- this lets them take advantage of serendipitous encounters (chance meetings, casual conversations) because they know exactly what they need to learn.

**IF** key assumptions were invalidated -> the next learning goals should explore the implications and potential pivots
**IF** assumptions were validated -> the next goals should push deeper or move to adjacent unknowns
**IF** the team is getting mixed signals across conversations -> consider whether the customer segment is too broad (use `customer-segment-slicer` to narrow)

**OUTPUT:** Updated list of 3 learning goals for the next conversation batch.

### Step 6: Produce the Learning Review Document

**ACTION:** Compile everything into a structured learning review document that serves as the permanent record of this conversation batch.

**WHY:** Notes must be transferred to permanent storage that is sortable, combinable with team notes, and retrievable. This document is the team's shared source of truth for what was learned, preventing any single person from becoming the bottleneck.

**Output format:**

```markdown
# Conversation Learning Review

## Batch Context
- **Date:** [date range of conversations]
- **Product/Problem Area:** [from input]
- **Customer Segment:** [who was talked to]
- **Team Members:** [who attended, with roles]
- **Conversations Conducted:** [count]

## Learning Goals (This Batch)
1. [Goal 1] -- STATUS: [validated/invalidated/uncertain]
2. [Goal 2] -- STATUS: [validated/invalidated/uncertain]
3. [Goal 3] -- STATUS: [validated/invalidated/uncertain]

## Categorized Notes

### Conversation: [person/company, date]

| # | Signal | Quote / Observation |
|---|--------|-------------------|
| 1 | :( [pain] | "We spend two full days every month reconciling invoices" |
| 2 | [workaround] | Built a spreadsheet macro but it breaks when format changes |
| 3 | $ [money] | Currently paying $2K/month for legacy system |
| 4 | [person] | Mentioned Sarah Chen at Acme -- same problem, bigger team |
| 5 | [follow-up] | Send API documentation they requested |

[Repeat for each conversation]

## Assumption Updates
| # | Assumption | Prior Status | New Status | Evidence |
|---|-----------|-------------|-----------|----------|
| 1 | [assumption] | untested | validated | "exact quote" -- [person, date] |
| 2 | [assumption] | untested | invalidated | [observation] -- [person, date] |

## Meta-Review
- **What worked:** [questions or techniques that produced good data]
- **What to improve:** [patterns to fix, questions to rephrase]
- **Process issues:** [any going-through-the-motions symptoms detected]

## Next 3 Learning Goals
1. [Next goal 1]
2. [Next goal 2]
3. [Next goal 3]

## Follow-Up Actions
- [ ] [action item 1 -- owner, deadline]
- [ ] [action item 2 -- owner, deadline]
```

**IF** the user provided a file path or working directory -> write the output to `learning-review-[date].md`
**ELSE** -> present the output directly in the conversation

## Examples

**Scenario: Founding team preparing for first customer conversations about a B2B invoicing tool**

Trigger: "We're building an automated invoicing tool for small accounting firms. My co-founder and I are about to start talking to potential customers. We've never done this before. How should we prepare?"

Process:
1. Diagnose: No prior conversations, no notes, no learning process yet. No bottleneck symptoms (they have not started). Flag the importance of both founders attending.
2. Set learning goals using the risk-identification questions:
   - "If this company fails, why?" -> Maybe nobody wants to switch from their current system, or the integration work is too painful.
   - "What would have to be true for huge success?" -> Accounting firms must hate their current invoicing workflow enough to pay for a new tool and endure switching costs.
3. Derive 3 learning goals: (a) How painful is the current invoicing process? (b) What workarounds do firms use today? (c) What would make them switch?

Output (abbreviated):
```
## Learning Goals (Batch 1)
1. How painful is the current invoicing workflow for small accounting firms?
   -> Test assumption: "Manual invoicing takes significant staff time"
2. What workarounds and tools do they currently use?
   -> Test assumption: "Most firms use spreadsheets or legacy software"
3. What would trigger a switch to a new invoicing tool?
   -> Test assumption: "Time savings alone would justify switching cost"

## Conversation Roles
- Lead: [Founder A] -- ask questions, guide conversation
- Note-taker: [Founder B] -- capture quotes, annotate with signal symbols

## Key Assumptions to Test
- Small firms spend >5 hours/week on invoicing
- Current tools are frustrating but firms have not actively looked for alternatives
- Price sensitivity is moderate ($50-200/month range)

## Prep Questions (Hidden Risks)
- If we fail, it is probably because: switching cost is too high,
  or the problem is not painful enough to justify change
- For huge success: firms must actively hate their current process
  AND be willing to endure 2-4 weeks of migration
```

---

**Scenario: Solo founder reviewing messy notes after three customer conversations**

Trigger: "I had three conversations this week about my meal planning app. Here are my notes: 'Sarah - busy mom, hates grocery shopping, tried Blue Apron but too expensive, husband won't eat weird food. Mike - personal trainer, tracks macros obsessively, uses MyFitnessPal but says it sucks for meal planning, spends 2 hours Sunday on meal prep. Lisa - college student, eats out constantly, knows it's unhealthy, has a budget of maybe $50/week for food, never cooks.'"

Process:
1. Diagnose: Solo founder, no team review, no signal categorization. Flag going-through-the-motions risk: are these conversations producing learning that changes plans?
2. Skip prep (conversations already happened).
3. Categorize each note with signal symbols.
4. Identify patterns and assumption updates.
5. Set next 3 learning goals.

Output (abbreviated):
```
## Categorized Notes

### Sarah (busy mom)
| # | Signal | Quote / Observation |
|---|--------|-------------------|
| 1 | :( [pain] | Hates grocery shopping |
| 2 | [workaround] | Tried Blue Apron |
| 3 | $ [money] | Blue Apron was too expensive (price sensitivity signal) |
| 4 | [obstacle] | Husband won't eat unfamiliar food (household constraint) |

### Mike (personal trainer)
| # | Signal | Quote / Observation |
|---|--------|-------------------|
| 1 | [goal] | Tracks macros obsessively (nutrition is a priority) |
| 2 | :( [workaround] | Uses MyFitnessPal but "says it sucks for meal planning" |
| 3 | [context] | Spends 2 hours Sunday on meal prep (significant time investment) |

### Lisa (college student)
| # | Signal | Quote / Observation |
|---|--------|-------------------|
| 1 | [context] | Eats out constantly, knows it is unhealthy |
| 2 | $ [money] | Budget ~$50/week for food |
| 3 | [obstacle] | Never cooks (skill/motivation barrier) |

## Pattern Analysis
- Mike is the strongest signal: has the problem, knows he has it, already
  spends significant time on a workaround, uses competing tools. Closest
  to an early adopter.
- Sarah has the problem but the household constraint (husband's food
  preferences) may be a dealbreaker for your solution.
- Lisa has awareness but no urgency -- has not tried to solve the problem.
  Unlikely early customer.

## Process Warning
You are reviewing notes alone. This is a learning bottleneck risk --
these insights need to reach your whole team (if you have one). If you
are a solo founder, consider finding an advisor to review with.

Also: these notes lack exact quotes. In future conversations, write
down verbatim customer words in quotation marks.

## Next 3 Learning Goals
1. How much would someone like Mike pay to eliminate Sunday meal prep?
   (anchor to his current time investment, not a hypothetical price)
2. What specific part of meal planning is hardest -- recipe selection,
   macro calculation, grocery list creation, or something else?
3. Have people like Mike actively searched for meal planning solutions
   beyond MyFitnessPal? (tests whether the problem is important enough
   to drive action)
```

---

**Scenario: Team diagnosing why their conversations feel unproductive**

Trigger: "We've done about 15 customer conversations over the past month for our HR analytics platform, but I feel like we're not making progress. We keep hearing positive things but nothing concrete is changing in our product plans."

Process:
1. Diagnose: Classic going-through-the-motions pattern. Positive feedback without plan changes = receiving compliments instead of learning. Check for all 8 symptoms.
2. Run diagnostic checklist against their described situation.
3. Recommend specific fixes.

Output (abbreviated):
```
## Diagnostic Results

Going-through-the-motions symptoms detected:
- [YES] They are complimenting you or your idea
  -> "We keep hearing positive things" -- compliments are the fool's gold
  of customer learning. They are shiny, distracting, and worthless.
- [YES] You got unexpected answers and they did not change your idea
  -> "Nothing concrete is changing in our product plans" -- if 15
  conversations have not changed anything, either you already know
  everything (unlikely) or you are not asking important enough questions.
- [LIKELY] You were not scared of any questions you asked
  -> Positive-only feedback across 15 conversations suggests the team
  is avoiding the hard questions that could disprove their assumptions.
- [CHECK] You have not reviewed notes with your team
  -> Ask: Are notes from all 15 conversations in a shared, reviewed
  location? Or are they in one person's notebook?

## Recommended Fixes
1. For each of your next 3 conversations, identify one question that
   terrifies you -- one where a bad answer would mean rethinking
   your product. If no question scares you, you are not asking about
   things that matter.
2. After each conversation, ask: "Did anything surprise us? Did
   anything change what we believe?" If the answer is always no,
   your questions are too safe.
3. Push for concrete commitments at the end of product meetings.
   "That sounds great" is not a commitment. "Can I buy the prototype?"
   is. See the `commitment-signal-evaluator` skill to evaluate your
   meeting outcomes.
4. Review all 15 sets of notes with your full team. Categorize using
   signal symbols. Look for patterns you missed individually.
```

## Key Principles

- **Customer learning is a team sport, not a solo mission** -- When all customer learning is stuck in one person's head, that person becomes a de-facto dictator wielding "the customer said so" as an unchallengeable trump card. Even if their interpretation is correct, learning that has not been shared cannot inform the team's decisions. Both business and product people need to participate in prep, attend at least some conversations, and review all notes together. The whole founding team must be represented.

- **The minimum viable prep is one question: "What do we want to learn?"** -- If you do not know what you are trying to learn, you should not bother having the conversation. Everything else in prep (desk research, role assignment, assumption mapping) is valuable but optional. This one question is not. It takes 5 minutes and transforms an aimless meeting into a focused learning opportunity.

- **Notes without review are worthless** -- Taking notes is necessary but not sufficient. The review is where learning actually transfers from paper to the team's shared understanding. It is tempting to skip because it feels like a non-step, but skipping it is how learning bottlenecks form. Disseminate learnings as quickly and directly as possible, using exact quotes wherever you can.

- **Unexpected answers that do not change plans are the clearest warning sign** -- If a customer tells you something surprising and your product plans remain unchanged, one of two things is true: either the information was not important (meaning you asked the wrong question), or the team is filtering out inconvenient truths. Either way, something in the process is broken.

- **Conversations are a tool, not an obligation** -- Talking to customers is a tool for de-risking your business. If it is not going to help or you do not want to do it, skip it. The alternative is worse: going through the motions, ticking the "learn from customers" checkbox, and wasting everyone's time. This process should make your business move faster, not slower. Spend an hour prepping, go talk to people. Do not spend a week on preparation -- anything more is stalling.

## References

- For the complete 12-symbol note-taking system with usage examples, see [note-taking-signal-symbols.md](references/note-taking-signal-symbols.md)
- For analyzing whether conversation questions are producing good data, use the `conversation-data-quality-analyzer` skill
- For evaluating whether meeting outcomes include real commitment signals, use the `commitment-signal-evaluator` skill

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Mom Test by Rob Fitzpatrick.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
