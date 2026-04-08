---
name: customer-discovery-process
description: Orchestrate the full customer discovery process — before, during, and after customer conversations — to systematically validate a business idea. This is the hub skill that sequences all other customer-discovery skills. Use this skill whenever the user wants to run customer discovery end-to-end, needs a step-by-step process for validating a product idea through customer conversations, wants to start customer discovery from scratch, wants to know what to do before and after customer meetings, needs a discovery status dashboard showing validation progress, suspects their discovery process is broken or unproductive, wants to diagnose whether they are just going through the motions, needs a customer development or lean validation framework, or asks "how do I validate my idea," "what's the full process for talking to customers," or "what should I do next in customer discovery" — even if they don't explicitly mention "discovery process." Do NOT use for writing specific interview questions (use conversation-question-designer), narrowing a customer segment (use customer-segment-slicer), or analyzing a single conversation transcript (use conversation-data-quality-analyzer).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-mom-test/skills/customer-discovery-process
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [12]
tags: [customer-discovery, validation-process, orchestration, discovery-dashboard, before-during-after]
depends-on:
  - conversation-question-designer
  - conversation-data-quality-analyzer
  - commitment-signal-evaluator
  - customer-segment-slicer
  - conversation-learning-process
  - conversation-sourcing-planner
  - conversation-format-selector
  - question-importance-prioritizer
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product idea description, current validation stage, and any existing conversation notes or learning logs"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
---

# Customer Discovery Process

## When to Use

You need to run a structured customer discovery process to validate a business idea through real conversations. This is the hub skill — it orchestrates the full before/during/after workflow and delegates specialized work to sibling skills. Typical situations:

- The user has an idea and wants a systematic plan for validating it through customer conversations
- The user is partway through discovery and needs to assess progress and decide next steps
- The user suspects their discovery process is broken — lots of meetings but no real learning
- The user wants to set up discovery from scratch and does not know where to start
- The user asks "what should I do next?" after a batch of conversations

**Mode: Hybrid** — The agent orchestrates the process, produces the discovery dashboard, and delegates to specialized skills. The human conducts the actual conversations.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product idea or problem hypothesis:** What is the user building or exploring? A sentence is enough.
  -> Check prompt for: product descriptions, problem statements, startup ideas
  -> Check environment for: `product-idea.md`, `README.md`
  -> If still missing, ask: "What product or problem are you exploring? A sentence or two is enough to get started."

- **Current validation stage:** Where is the user in their discovery process?
  -> Check prompt for: "just starting," "have done N conversations," "getting mixed feedback," stage indicators
  -> Check environment for: `learning-log.md`, `conversation-notes/`, `customer-segments.md`
  -> If still missing, ask: "Where are you in customer discovery? (a) Have not started yet, (b) Have done a few conversations, (c) Have done many conversations but feel stuck"

### Observable Context (gather from environment)

- **Existing discovery artifacts:** Check for files that reveal what has already been done.
  -> Look for: `customer-segments.md`, `question-script.md`, `learning-log.md`, `outreach-plan.md`, `commitment-tracker.md`, `conversation-notes/`
  -> If found: assess which process steps are complete and which are pending

- **Team context:** Is this a solo founder or a team?
  -> Look for: mentions of co-founders, team members
  -> If unavailable: assume solo founder

### Default Assumptions

- If no stage specified -> assume the user is starting from scratch
- If no team mentioned -> assume solo founder (but flag the importance of having a review partner)
- If no prior conversations -> begin at the BEFORE phase

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Product idea or problem area is known
- Current validation stage is known or can be inferred from environment

PROCEED WITH DEFAULTS when:
- Product idea is approximate ("something for freelancers")
- Stage is vague ("I've talked to a few people")

MUST ASK when:
- No product idea or problem area at all
```

## Process

### Step 1: Assess Current Discovery State

**ACTION:** Determine where the user is in the discovery process by checking for existing artifacts and conversation history. Run the going-through-the-motions diagnostic if they have already started.

**WHY:** The discovery process is not linear — users enter at different points and may need to loop back. Assessing state prevents repeating completed work and identifies the highest-impact next step. Many users who "feel stuck" are actually going through the motions without real learning, and diagnosing this early saves weeks of wasted conversations.

**Going-through-the-motions diagnostic — check for these 9 warning signs:**

1. You are talking more than the customer is
2. They are complimenting you or your idea
3. You told them about your idea and do not know what is happening next
4. You do not have notes from the conversation
5. You have not reviewed your notes with your team
6. You got an unexpected answer and it did not change your idea
7. You were not scared of any of the questions you asked
8. You are not sure which big question you are trying to answer
9. You are not sure why you are having the meeting

**IF** 3 or more warning signs are present -> flag the process as broken. The user needs to fix their approach before having more conversations. Focus on the BEFORE phase regardless of how many conversations they have already done.
**IF** the user has not started -> proceed to Step 2 (BEFORE phase).
**IF** the user has conversation notes to review -> proceed to Step 4 (AFTER phase).

### Step 2: BEFORE — Prepare for Conversations

**ACTION:** Execute the preparation sequence. Each sub-step invokes a specialized skill.

**WHY:** Most bad conversations happen because of bad preparation. Choosing the wrong segment means talking to the wrong people. Unclear learning goals mean the conversation wanders. Bad questions produce bad data. The BEFORE phase is where you set up the conversation to succeed. Skipping it is the primary cause of "going through the motions."

**2a. Segment your customers**
**IF** no customer segment is defined or the current one is too broad -> invoke `customer-segment-slicer` to produce a specific who-where pair.
**WHY:** A conversation without a focused segment produces mixed signals that cannot inform decisions. You are not having 20 conversations with your customers — you are having 1 conversation each with 20 different types of customers.

**2b. Plan conversation sourcing**
**IF** the user knows WHO but not HOW to reach them -> invoke `conversation-sourcing-planner` to create an outreach plan with framing templates.
**WHY:** Most founders default to cold email or formal meetings when casual conversations at natural gathering points would produce better data faster with less overhead.

**2c. Set learning goals and prepare questions**
**ACTION:** Invoke `question-importance-prioritizer` to classify risks and select the 3 most important learning goals. Then invoke `conversation-learning-process` (Step 2: pre-conversation prep) to set those goals with the team. Finally invoke `conversation-question-designer` to produce a question script aligned to those goals.
**WHY:** The minimum viable prep is answering one question: "What do we want to learn from these guys?" Without this, the conversation is aimless. The question script ensures the conversation produces facts instead of compliments.

**2d. Choose conversation format**
**IF** the user is unsure about meeting format -> invoke `conversation-format-selector` to recommend casual vs formal vs phone.
**WHY:** Defaulting to 1-hour formal meetings for every conversation is the Meeting Anti-Pattern. A 5-minute casual chat often produces the same learning with a fraction of the time cost.

**2e. Define target commitments**
**ACTION:** Based on the user's product stage, define what commitment to push for at the end of the meeting.

| Product Stage | Target Commitment |
|---------------|-------------------|
| Problem exploration (no product) | Time: next meeting with specific goals. Reputation: intro to others with the same problem. |
| Wireframes or prototype | Time: sit down to review wireframes. Reputation: intro to decision maker. |
| Working product or beta | Time: non-trivial trial. Reputation: case study. Money: letter of intent. |
| Live product | Money: purchase or deposit. Reputation: public testimonial. |

**OUTPUT:** A completed preparation checklist ready for the human to execute.

### Step 3: DURING — Conversation Execution Guidance

**ACTION:** Provide the human with a field reference card for real-time use during the conversation.

**WHY:** Even with perfect preparation, conversations go off-script. The human needs to recognize danger signals in real-time and recover. This step produces a compact reference, not a rigid script — the human leads the conversation while the card keeps them honest.

**HANDOFF TO HUMAN** — The agent cannot conduct the conversation. Provide this field card:

**Keep it casual.** If it feels like they are doing you a favor by talking to you, it is probably too formal.

**Ask questions that pass 3 rules:**
1. Talk about their life, not your idea
2. Ask about specifics in the past, not generics about the future
3. Talk less and listen more

**Recover from bad data in real-time:**
- If you hear a compliment -> deflect: "Thanks — but how are you currently handling this?"
- If you hear fluff ("I would definitely...") -> anchor: "When was the last time that came up?"
- If you hear a feature request -> dig: "Why do you want that? What would it let you do?"

**Press for commitment and next steps.** Do not leave without a concrete next step. The meeting either advances or it fails — there is no "went well."

**Take notes.** Capture exact quotes. Use signal symbols if possible. Without notes, the conversation might as well not have happened.

### Step 4: AFTER — Review, Synthesize, and Decide Next Steps

**ACTION:** Execute the post-conversation sequence. Each sub-step invokes a specialized skill.

**WHY:** The AFTER phase is where conversations turn into validated learning. Without it, insights stay in one person's head, bad data gets treated as fact, and the team never updates their assumptions. Most teams skip this phase, which is why they feel stuck after dozens of conversations.

**4a. Analyze conversation quality**
**ACTION:** Invoke `conversation-data-quality-analyzer` on the conversation notes to classify every statement as FACT, COMPLIMENT, FLUFF, or IDEA. Get the quality rating (STRONG / MIXED / WEAK / EMPTY).
**WHY:** A conversation that "went well" is a warning sign. Quantifying the ratio of facts to noise gives an objective measure instead of a gut feeling driven by compliments.

**4b. Evaluate commitment signals**
**ACTION:** Invoke `commitment-signal-evaluator` on the meeting outcomes to classify commitment currencies (time, reputation, money) and detect zombie leads.
**WHY:** Compliments cost nothing and are worth nothing. The only reliable measure of interest is what the prospect gave up. This step separates real leads from false-positive prospects.

**4c. Run the team learning review**
**ACTION:** Invoke `conversation-learning-process` (Steps 3-5: categorize notes, run team review, set next learning goals) to transfer learnings to the whole team and update assumptions.
**WHY:** Customer learning is a team sport. When insights stay in one person's head, that person becomes a de-facto dictator wielding "the customer said so" as an unchallengeable trump card. The review is where learning actually transfers.

**4d. Update the discovery dashboard**
**ACTION:** Update the discovery status dashboard (see Step 5) with new data from this conversation batch.

### Step 5: Produce the Customer Discovery Status Dashboard

**ACTION:** Create or update the discovery dashboard — a single document showing the full state of the user's validation progress.

**WHY:** Customer discovery produces many artifacts across many conversations. Without a single status view, the user loses track of what has been validated, what remains unknown, and what to do next. The dashboard is the tangible deliverable of this hub skill — it aggregates output from all sibling skills into one actionable summary.

**Dashboard format:**

```markdown
# Customer Discovery Status Dashboard

## Product
- **Idea:** [product description]
- **Stage:** [problem exploration / prototype / beta / live]
- **Date Updated:** [today]

## Active Segment
- **WHO:** [specific customer segment]
- **WHERE:** [finding location]
- **Source:** customer-segment-slicer output or user-defined
- **Segment Status:** [needs slicing / defined / validated]

## Learning Goals (Current Batch)
| # | Learning Goal | Status | Evidence |
|---|--------------|--------|----------|

## Conversation Log
| # | Date | Person | Quality | Commitment | Key Insight |
|---|------|--------|---------|------------|-------------|
| 1 | [date] | [who] | [STRONG/MIXED/WEAK] | [currency type] | [one-line insight] |

## Assumption Tracker
| # | Assumption | Status | Evidence | Source |
|---|-----------|--------|----------|--------|

## Commitment Pipeline
| Prospect | Highest Currency | Earlyvangelist Score | Next Step | Status |
|----------|-----------------|---------------------|-----------|--------|
| [name] | [time/reputation/money/none] | [0-4 criteria met] | [action] | [active/zombie/closed] |

## Process Health
- **Conversations this batch:** [N]
- **Going-through-the-motions signs:** [count of 9] — [list any present]
- **Good meeting results:** [count of meetings producing Facts + Commitment + Advancement]
- **Learning bottleneck risk:** [yes/no — is one person hoarding insights?]

## Results of a Good Meeting (Checklist)
For each conversation, verify it produced at least one of:
- [ ] **Facts** — concrete, specific facts about what they do and why (not compliments, fluff, or opinions)
- [ ] **Commitment** — they gave up something of value: time, reputation, or money
- [ ] **Advancement** — they moved to the next step of your real-world funnel, closer to a sale

## Next Actions
1. [Highest-priority next step]
2. [Second priority]
3. [Third priority]
```

**IF** the user provided a working directory -> write to `discovery-dashboard.md`
**ELSE** -> present directly in the conversation

## Examples

**Scenario: Founder starting from scratch with a SaaS idea**

Trigger: "I have an idea for a tool that helps freelance designers manage client feedback. How do I validate this?"
Process: Assess state (starting from scratch). BEFORE phase: invoke `customer-segment-slicer` ("freelance designers" too broad, slice to "freelance UI/UX designers on Dribbble with 3+ simultaneous projects"). Invoke `conversation-learning-process` for prep (3 goals: feedback loop pain, current tools, past fix attempts). Invoke `conversation-question-designer` for script. Define target commitments (pre-product: time + reputation).
Output: Discovery dashboard with BEFORE phase complete, segment defined, question script ready, zero conversations logged. Action plan: "Talk to 3-5 freelance UI/UX designers this week."

---

**Scenario: Founder stuck after 12 conversations**

Trigger: "I've done 12 customer interviews for my restaurant inventory tool but everyone says it sounds great and nobody has signed up for the beta."
Process: Run going-through-the-motions diagnostic — detected 3 of 9 signs (compliments without commitments, no scary questions, nothing changed). Invoke `conversation-data-quality-analyzer` on notes (likely WEAK — mostly compliments and fluff). Invoke `commitment-signal-evaluator` (zero currencies across 12 meetings, zombie lead pattern). Diagnosis: collecting compliments instead of facts.
Output: Dashboard showing 12 conversations, zero validated assumptions, zero commitments. Restart plan: re-slice segment, set scary learning goals, redesign questions to hide the product, define concrete commitment asks.

---

**Scenario: Team reviewing after a productive conversation batch**

Trigger: "My co-founder and I finished 5 conversations this week about our invoicing tool. Here are our notes. What next?"
Process: Enter AFTER phase. Invoke `conversation-data-quality-analyzer` on each set of notes. Invoke `commitment-signal-evaluator` on outcomes. Invoke `conversation-learning-process` for team review, assumption updates, and next learning goals.
Output: Updated dashboard with 5 conversations logged, quality ratings, strongest lead flagged, assumptions updated, next 3 learning goals set.

## Key Principles

- **This skill orchestrates, it does not duplicate** — Every specialized task (segmenting, questioning, analyzing, evaluating commitments, reviewing learnings) is handled by a sibling skill. This skill sequences them in the right order and maintains the overall discovery state. If you find yourself doing detailed question design or data classification here, you are in the wrong skill.

- **The process is before/during/after, not plan/execute** — Customer discovery is not a project plan you execute once. It is a loop: prepare, talk, review, update, repeat. Each cycle through the loop should produce validated or invalidated assumptions. If you have been through the loop multiple times and nothing has changed, the process itself is broken.

- **A meeting that "went well" is a warning sign** — Good meetings produce facts, commitment, and advancement. Bad meetings produce compliments and warm feelings. The phrase "it went well" almost always means the latter. Every meeting must be scored against the three results criteria (facts, commitment, advancement), not against how it felt.

- **Conversations are a tool, not an obligation** — Having a process does not mean having more meetings. The goal is to learn what you need as quickly as possible and get back to building. Three focused conversations with the right segment can produce more learning than thirty scattered ones with the wrong people. If conversations are not producing learning, fix the process or stop having them.

- **Process without action is worse than no process at all** — Having a process is valuable, but do not get stuck in it. Sometimes you can just pick up the phone and hack through the knot. The personal trainer who called the police station instead of agonizing over customer segmentation got a trial session in twenty minutes. Process exists to serve learning, not the other way around.

## References

- Segment customers into who-where pairs -> `customer-segment-slicer`
- Create outreach plans and framing templates -> `conversation-sourcing-planner`
- Design questions that pass the 3 quality rules -> `conversation-question-designer`
- Choose conversation format (casual/formal/phone) -> `conversation-format-selector`
- Prioritize which learning goals matter most -> `question-importance-prioritizer`
- Analyze conversation notes for bad data -> `conversation-data-quality-analyzer`
- Evaluate commitment signals and detect zombie leads -> `commitment-signal-evaluator`
- Run team learning review and set next goals -> `conversation-learning-process`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Mom Test by Rob Fitzpatrick.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-conversation-question-designer`
- `clawhub install bookforge-conversation-data-quality-analyzer`
- `clawhub install bookforge-commitment-signal-evaluator`
- `clawhub install bookforge-customer-segment-slicer`
- `clawhub install bookforge-conversation-learning-process`
- `clawhub install bookforge-conversation-sourcing-planner`
- `clawhub install bookforge-conversation-format-selector`
- `clawhub install bookforge-question-importance-prioritizer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
