---
name: conversation-question-designer
description: Write, rewrite, or audit customer interview questions so they extract honest behavioral data instead of false validation. Use this skill whenever the user needs to prepare a conversation script for customer discovery, draft questions for an upcoming interview, fix questions that keep producing useless or vague answers, rewrite biased or leading questions into past-focused behavior-revealing ones, check whether their interview questions will trigger compliments instead of facts, or build a question list from learning goals — even if they don't mention "question design" or "The Mom Test." Do NOT use this skill to analyze conversation notes after a meeting (use conversation-data-quality-analyzer) or to decide which questions matter most strategically (use question-importance-prioritizer).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-mom-test/skills/conversation-question-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [1]
tags: [customer-discovery, interview-questions, customer-conversations, validation, question-design]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product idea description, draft question list, or conversation topic"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
---

# Conversation Question Designer

## When to Use

You are preparing for a customer conversation and need questions that will produce honest, useful data rather than false validation. Typical situations:

- The user has a list of draft interview questions and wants them reviewed or improved
- The user is about to talk to potential customers and needs a conversation script
- The user wants to validate a product idea but is not sure what to ask
- The user has a conversation topic or learning goal but no specific questions yet
- The user received unhelpful answers from previous conversations and wants to fix their approach

Before starting, verify:
- Does the user have a product idea or problem area to explore? (If not, help them articulate one first)
- Does the user know who they will be talking to? (Customer type affects which questions matter most)

**Mode: Hybrid** — The agent designs the question script and analyzes/rewrites questions. The human conducts the actual conversation.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product idea or problem area:** What is the user building or exploring? This shapes which behaviors and past experiences to ask about.
  → Check prompt for: product descriptions, problem statements, startup ideas, feature concepts
  → Check environment for: `product-idea.md`, `README.md`, pitch documents
  → If still missing, ask: "What product idea or problem area are you exploring? A sentence or two is enough."

- **Learning goals:** What does the user want to learn from these conversations? This determines which questions matter most.
  → Check prompt for: assumptions to validate, unknowns, hypotheses, "I want to find out..."
  → Check environment for: `learning-log.md`, `question-script.md`, previous conversation notes
  → If still missing, ask: "What are the 1-3 most important things you want to learn from these conversations?"

### Observable Context (gather from environment)

- **Existing question drafts:** Check for prepared questions the user wants reviewed
  → Look for: `question-script.md`, question lists in the prompt, bullet-pointed questions
  → If unavailable: generate questions from scratch based on learning goals

- **Customer segment:** Who will the user be talking to?
  → Look for: `customer-segments.md`, persona descriptions, target market references
  → If unavailable: ask "Who will you be talking to? (e.g., small business owners, enterprise CTOs, parents)"

- **Previous conversation notes:** Past learnings that should inform new questions
  → Look for: `conversation-notes/`, `learning-log.md`
  → If unavailable: assume first round of conversations

### Default Assumptions

- If no customer type specified → design questions generic enough for early exploration, note this limitation
- If no stage specified → assume pre-product (learning phase, not selling)
- If no prior conversations → assume this is the first batch and questions should start broad

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Product idea or problem area is known
- At least 1 learning goal is identified
- Customer type is known or defaulted

PROCEED WITH DEFAULTS when:
- Product idea is known but learning goals are vague
- Customer type is approximate ("probably small businesses")

MUST ASK when:
- No product idea or problem area at all
- User provides questions but no context on what they are building
```

## Process

### Step 1: Extract Learning Goals

**ACTION:** Identify the 3 most important things the user needs to learn from upcoming conversations. If the user has provided learning goals, validate them. If not, derive them from their product idea and assumptions.

**WHY:** Questions without clear learning goals produce scattered, unusable data. Every question in the script must connect to a specific learning goal, otherwise the conversation wanders and the user leaves with opinions instead of facts.

**IF** the user has stated learning goals → validate they are about customer behavior/problems (not about validating the solution)
**IF** learning goals are solution-focused (e.g., "Would people use my app?") → reframe toward the underlying behavior: "How are people currently solving this problem?"

**OUTPUT:** A numbered list of 3 learning goals, each framed as a behavior or fact to discover (not an opinion to collect).

### Step 2: Audit Existing Questions (if provided)

**ACTION:** Evaluate each question against the 3 customer conversation quality rules (The Mom Test):

| Rule | Test | Failure Pattern |
|------|------|----------------|
| **Rule 1: Their life, not your idea** | Does this question ask about the customer's actual behavior, problems, or workflow — or does it ask them to evaluate your concept? | Questions containing "my idea," "this product," "would you use," "do you think" |
| **Rule 2: Specifics in the past, not generics about the future** | Does this question ask about concrete events that already happened — or does it ask for predictions, hypotheticals, or generalizations? | Questions containing "would you," "will you," "do you ever," "how much would you pay," future tense |
| **Rule 3: Listen more than talk** | Does this question invite an open-ended response — or does it lead toward a specific answer? | Yes/no questions, questions with the answer embedded, multi-part questions that overwhelm |

**WHY:** Bad questions are the default. Most people naturally ask opinion-seeking, future-hypothetical, or idea-validating questions because those feel productive. But the answers to those questions are worthless — people are overly optimistic about the future and will lie to avoid hurting your feelings. Auditing against these 3 rules catches the specific failure modes before the conversation happens.

**FOR EACH** question in the user's draft list:
1. Rate as PASS, FAIL, or FIXABLE against each of the 3 rules
2. If FAIL or FIXABLE → identify which rule(s) it violates and why
3. Write a rewritten version that passes all 3 rules
4. Note what learning goal this question serves (or flag it as goalless)

**IF** no existing questions are provided → skip to Step 3.

### Step 3: Generate the Question Script

**ACTION:** Build a structured conversation script organized by learning goal. For each learning goal, create 3-5 questions that progress from broad to specific.

**WHY:** Conversations need structure to produce usable data, but rigid scripts kill natural flow. Organizing by learning goal lets the human navigate flexibly — they can follow interesting threads while keeping track of what they still need to learn. Starting broad prevents premature zoom (asking about a specific problem before confirming the person even cares about that area).

**Question design rules — apply to every question:**

1. **Ask about their life, not your idea.** Frame questions around their current behavior, workflows, problems, and goals. Never mention your product concept unless deliberately testing a later-stage hypothesis.

2. **Ask about specifics in the past, not generics about the future.** Replace "Would you..." with "When was the last time..." Replace "Do you usually..." with "Talk me through what happened last time..." Past behavior is the only reliable predictor.

3. **Use open questions that invite stories.** "Talk me through..." and "Tell me about the last time..." produce richer data than "Do you..." or "How often do you..."

4. **Include motivation-revealing questions.** "Why do you bother?" and "What are the implications?" separate must-solve problems from nice-to-haves.

5. **Include commitment-testing questions.** "What have you already tried to solve this?" and "How are you dealing with it now?" reveal whether the problem is painful enough to drive action.

6. **End with network-expanding questions.** "Who else should I talk to?" and "Is there anything else I should have asked?" generate warm introductions and catch blind spots.

**Script structure per learning goal:**

```
## Learning Goal: [goal description]

### Opener (broad, non-leading)
- [Question that explores whether this area matters to them at all]

### Depth questions (specific, past-focused)
- [Question about concrete past behavior]
- [Question about current workflow/workaround]
- [Question about implications/severity]

### Commitment signal (reveals real vs stated priority)
- [Question about what they have tried or are spending]
```

### Step 4: Add Anti-Bias Safeguards

**ACTION:** Review the complete script for common bias traps and add inline warnings where the human might accidentally slip into bad patterns during the conversation.

**WHY:** Even with good prepared questions, conversations go off-script. The human needs to recognize danger signals in real-time. Adding warnings at specific points in the script acts as a field guide during the conversation.

**Bias traps to flag:**

| Trap | Signal | Recovery |
|------|--------|----------|
| **Compliment fishing** | You just described your idea and they said "That sounds great!" | Deflect: "Thanks — but tell me, how are you currently handling this?" |
| **Accepting vague enthusiasm** | They say "I would definitely use that" or "That is exactly what I need" | Anchor: "When was the last time this problem came up? Walk me through what happened." |
| **Pitching instead of asking** | You have been talking for more than 30 seconds without asking a question | Stop and ask: "Sorry, I got excited. Can I ask — how are you dealing with this right now?" |
| **Leading toward your solution** | Your question contains your product's features or approach | Reframe around their problem, not your solution |
| **Accepting generic claims** | They say "I usually..." or "I always..." or "I never..." | Anchor: "Can you tell me about the most recent specific time?" |

### Step 5: Produce the Deliverable

**ACTION:** Write the final question script as a structured document the user can reference during their conversation.

**WHY:** The deliverable must be usable in the field — not a theoretical analysis. It should fit on a single page, be scannable during a live conversation, and clearly connect each question to what the user is trying to learn.

**Output format:**

```markdown
# Conversation Question Script

## Context
- **Product/Problem Area:** [from input]
- **Target Customer:** [from input]
- **Date Prepared:** [today]

## Learning Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Question Script

### Learning Goal 1: [description]

**Opener:** [broad question]

**Depth:**
- [specific past-focused question]
- [workflow/workaround question]
- [implication/severity question]

**Commitment signal:** [what-have-you-tried question]

> WATCH OUT: [relevant bias trap warning]

### Learning Goal 2: [description]
[same structure]

### Learning Goal 3: [description]
[same structure]

## Closing Questions (use for every conversation)
- "Who else should I talk to?" — generates warm intros
- "Is there anything else I should have asked?" — catches blind spots

## Quick Reference: Bias Recovery
| If you hear... | Do this... |
|----------------|-----------|
| "That sounds great!" | Deflect → ask about their current process |
| "I would definitely..." | Anchor → ask about most recent specific instance |
| "I usually/always/never..." | Anchor → "Tell me about the last time" |
| Feature requests | Dig → "Why do you want that? What would it let you do?" |

## Questions Rewritten (if audit was performed)
| # | Original (FAIL) | Rewritten (PASS) | Rule Violated |
|---|-----------------|------------------|---------------|
| 1 | [original] | [rewritten] | [rule 1/2/3] |
```

**IF** the user provided a file path or working directory → write the output to `question-script.md`
**ELSE** → present the output directly in the conversation

## Examples

**Scenario: Founder with draft questions about a project management tool**

Trigger: "I'm building a project management tool for freelancers. Here are my interview questions: 1) Do you think a simpler project management tool would be useful? 2) Would you pay $10/month for it? 3) How do you manage your projects?"

Process:
1. Extract learning goals: (a) Do freelancers have project management pain? (b) What do they currently use? (c) Would they pay for a solution?
2. Audit existing questions:
   - Q1 FAIL (Rule 1: asks them to evaluate your idea; Rule 2: hypothetical)
   - Q2 FAIL (Rule 1: about your product; Rule 2: hypothetical pricing)
   - Q3 FIXABLE (Rule 2: too generic, needs past-tense anchoring)
3. Generate rewritten script with depth questions

Output (abbreviated):
```
## Questions Rewritten
| # | Original (FAIL) | Rewritten (PASS) | Rule Violated |
|---|-----------------|------------------|---------------|
| 1 | "Do you think a simpler PM tool would be useful?" | "Tell me about the last project you managed. What went well and what was frustrating?" | Rule 1, Rule 2 |
| 2 | "Would you pay $10/month for it?" | "How much time do you spend on project admin each week? What tools are you paying for right now?" | Rule 1, Rule 2 |
| 3 | "How do you manage your projects?" | "Walk me through how you managed your most recent client project from start to finish." | Rule 2 |

## Learning Goal 1: Do freelancers have project management pain?
Opener: "What does a typical work week look like for you?"
Depth:
- "Tell me about the last time a project got disorganized. What happened?"
- "What are the implications when project details fall through the cracks?"
- "How seriously do you take project organization compared to, say, finding new clients?"
Commitment signal: "Have you looked into any tools or systems to help with this?"
```

---

**Scenario: Product manager preparing for first customer discovery conversations**

Trigger: "We're exploring a new feature for our analytics platform that would auto-generate executive reports. I need to prepare questions for talking to marketing directors. No existing questions yet."

Process:
1. Identify learning goals: (a) How do marketing directors currently create executive reports? (b) How painful is the current process? (c) Who else is involved in reporting?
2. Skip audit (no existing questions)
3. Generate full question script from scratch
4. Add anti-bias safeguards (flag the risk of pitching the auto-generate feature)

Output (abbreviated):
```
## Learning Goal 1: Current reporting workflow
Opener: "Tell me about the last executive report you put together."
Depth:
- "Walk me through the steps — where did the data come from, who was involved, how long did it take?"
- "What was the most annoying part of that process?"
- "What happened after you delivered it? Any follow-up requests or revisions?"
Commitment signal: "Have you tried any tools or shortcuts to speed this up?"

> WATCH OUT: Do NOT mention "auto-generated reports" during this section.
> If they mention reporting pain, resist the urge to pitch — instead ask
> "What have you tried to make it faster?"
```

---

**Scenario: Rewriting a single biased question**

Trigger: "Is this a good question to ask potential customers: 'Would you buy an app that helps you track your calories more easily?'"

Process:
1. Identify the single question violates Rule 1 (about your app) and Rule 2 (hypothetical future)
2. Rewrite to pass all 3 rules
3. Provide the rewritten version with explanation

Output:
```
FAIL — violates Rule 1 (asks about your idea, not their life) and Rule 2 (hypothetical future).

The answer will almost always be "yes" because people are optimistic about
hypotheticals and want to be supportive. This tells you nothing.

Rewritten:
- "How are you tracking what you eat right now?" (their current behavior)
- "Walk me through what you did for food tracking yesterday." (specific past)
- "What else have you tried? What did you like and hate about it?" (commitment signal)
- "How much are you spending on health/nutrition apps right now?" (price anchor from reality)

These questions reveal whether they actually care enough to have tried
solving this — which is far more predictive than whether they say "yes"
to a hypothetical.
```

## Key Principles

- **Opinions are worthless; behavior is everything** — People will tell you your idea is great to avoid hurting your feelings. But they cannot fake what they have actually done in the past. Always ask about concrete past actions, never about future intentions or abstract opinions. A question like "Would you use X?" is answered with optimism. "When did you last try to solve X?" is answered with facts.

- **The best questions make your idea invisible** — If the person you are talking to does not even know you have a product idea, they cannot lie to you about it. The moment you reveal your concept, every response becomes contaminated by their desire to be supportive (or contrarian). Keep the conversation about their life, their problems, their workflow.

- **Generic claims need anchoring to specifics** — When someone says "I always" or "I usually" or "I would," that is a generic claim (vague, non-specific feedback). It sounds like data but it is noise. Anchor it to reality by asking "When was the last time that happened?" or "Can you walk me through a specific example?" The specific story either confirms the generic claim or contradicts it.

- **Every question must serve a learning goal** — Questions without a clear purpose produce interesting but useless conversations. Before adding any question to the script, verify: "If they answer this, which of my 3 learning goals does it advance?" Goalless questions waste scarce conversation time.

- **Premature specificity kills discovery** — If you zoom into your specific problem area before confirming the person even cares about that area, you get false validation. Start broad ("What are the biggest challenges in your role?") and only zoom in when they independently raise the topic you care about. If they do not mention it unprompted, it is probably not a top priority for them.

## References

- For the complete 14-question good/bad rubric with fix patterns, see [question-quality-rubric.md](references/question-quality-rubric.md)
- For analyzing conversation quality after conversations happen, use the `conversation-data-quality-analyzer` skill
- For prioritizing which questions matter most given business risk, use the `question-importance-prioritizer` skill

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Mom Test by Rob Fitzpatrick.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
