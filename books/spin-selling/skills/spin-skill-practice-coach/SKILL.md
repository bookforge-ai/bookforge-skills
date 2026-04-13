---
name: spin-skill-practice-coach
description: "Build a personalized multi-week SPIN practice plan for a B2B sales rep learning the SPIN methodology. Use this skill when someone is new to SPIN and wants to build the skill systematically, when a rep says 'I read SPIN Selling but can't put it into practice', when someone asks 'how do I actually learn SPIN?', when a seller wants a structured practice curriculum, when a manager wants a rep to develop SPIN questioning skills without blowing key accounts, when someone asks 'how do I actually use Implication Questions in real calls?', when a rep is struggling to apply SPIN because it feels unnatural, when someone wants to build muscle memory for Problem or Need-payoff questions, or when a seller wants to know which accounts are safe to practice on. This skill applies Rackham's Four Golden Rules for skill learning — one behavior at a time, try it 3 times before judging, quantity before quality, safe situations first — plus a 4-step SPIN learning sequence, to build a personalized schedule calibrated to the user's current level and actual account portfolio. The output is a dated multi-week plan that names specific behaviors to practice in specific practice windows, not a feature list. A baseline LLM will produce tips ('read the book', 'practice in real calls', 'get feedback') — this skill produces a practice curriculum."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/spin-skill-practice-coach
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [8]
tags: [sales, b2b-sales, enterprise-sales, spin-methodology, skill-development, practice-plan, learning-curriculum, questioning-techniques]
depends-on:
  - spin-discovery-question-planner
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "account-portfolio.md — list of active accounts with deal stage, size, and relationship strength. If this file does not exist, the skill interviews the user to build it."
    - type: interactive
      description: "SPIN level self-assessment — the skill administers a short diagnostic to determine which question types the user already uses naturally"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set or interactive session. Agent produces spin-practice-plan-{user}.md — a multi-week practice schedule. Human executes the plan in real calls."
discovery:
  goal: "Produce a personalized multi-week SPIN practice schedule that assigns one new behavior per practice window, names which accounts are safe vs. key, and embeds retry budgets so the user does not abandon new behaviors after one awkward attempt"
  tasks:
    - "Diagnose the user's current SPIN level via short self-assessment"
    - "Classify the user's accounts into safe practice grounds vs. key accounts to protect"
    - "Apply the Four Golden Rules to structure the practice schedule"
    - "Walk through the 4-step SPIN learning sequence: more questions → Problem Qs → Implication Qs → Need-payoff Qs"
    - "Produce a named, dated multi-week plan with one behavior per window and a 3-attempt retry budget"
  audience:
    roles: [account-executive, enterprise-sales-rep, sdr, solutions-consultant, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "Rep is new to SPIN and wants to build the skill methodically"
      - "Rep read SPIN Selling but finds the behaviors feel unnatural in actual calls"
      - "Manager wants a structured learning plan for a rep without risking key accounts"
      - "Seller wants to know which accounts to practice Implication Questions on first"
    prerequisites:
      - "Basic familiarity with SPIN question types (Situation, Problem, Implication, Need-payoff) — either from reading the book or from using spin-discovery-question-planner"
    not_for:
      - "Planning questions for a specific deal call (use spin-discovery-question-planner)"
      - "Diagnosing why a call produced objections (use objection-source-diagnoser)"
      - "Running a Plan-Do-Review cycle on a specific call (use sales-call-plan-do-review-coach)"
      - "Closing-attitude introspection (use closing-attitude-self-assessment)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: ""
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
    what_skill_catches:
      - "Output assigns one new SPIN behavior per practice window, not multiple simultaneously"
      - "Output names which specific accounts are safe practice grounds and which to protect"
      - "Output requires 3 attempts before evaluating a new behavior (Rule 2)"
      - "Output prioritizes quantity over quality in early practice windows (Rule 3)"
      - "Output explicitly forbids practicing new behaviors on top accounts (Rule 4)"
    what_baseline_misses:
      - "Produces a flat list of tips with no structural methodology"
      - "Does not map new behaviors to specific account types"
      - "Does not include a retry budget or protect against abandoning after one awkward attempt"
      - "Does not sequence the four SPIN behaviors — treats them as a flat list"
---

# SPIN Skill Practice Coach

## When to Use

You know what SPIN is. You may have even planned a few question banks with `spin-discovery-question-planner`. But when the call starts, the questions feel clunky. You sound scripted. You go back to old habits. The methodology is in your head — not yet in your hands.

This skill builds the practice infrastructure that converts knowledge into reflexes. It diagnoses where you are in the SPIN learning curve, maps your account portfolio into safe vs. key accounts, and produces a multi-week schedule with one new behavior per practice window and a built-in retry budget.

**Use this skill when:**
- You are new to SPIN and want to learn it without damaging your pipeline
- You have tried SPIN a few times and given up after it felt awkward
- You want to know which accounts are safe to experiment on — and which to protect
- You want a structured plan, not a list of tips

**This skill is NOT for:** individual call execution (use `spin-discovery-question-planner`), post-call objection diagnosis (use `objection-source-diagnoser`), or full Plan-Do-Review cycles (use `sales-call-plan-do-review-coach`).

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Account portfolio:** The user's active accounts, with some indication of size, stage, and relationship strength.
  -> Check environment for: `account-portfolio.md`
  -> If missing, ask: "Tell me about your current account list — roughly how many active accounts do you have, and can you characterize a few as either important/key deals or smaller/exploratory accounts?"

- **Current SPIN level:** Which question types does the user already use naturally?
  -> Check environment for: self-assessment answers or prior call notes
  -> If missing, administer the 5-item diagnostic in Step 1

### Observable Context (gather from environment)

- **Prior call notes or question banks:** Any `question-bank-*.md` files from `spin-discovery-question-planner`
  -> If available: read to calibrate the user's actual SPIN usage, not just self-reported
  -> If unavailable: rely on the Step 1 diagnostic

- **Time horizon:** How many weeks does the user want the plan to cover?
  -> Default to 6 weeks if not specified

### Sufficiency Threshold

SUFFICIENT: Any description of the account portfolio + self-assessment complete
PROCEED WITH DEFAULTS: User describes only 2-3 accounts → extrapolate safe vs. key classification
MUST ASK: No account description at all (the skill cannot assign account-specific practice windows)

## Process

### Step 1: Diagnose Current SPIN Level

**ACTION:** Administer the following 5-item self-assessment. Ask the user to rate each item on a scale of 1 (never) to 5 (always):

1. "In a typical discovery call, I ask open-ended questions to understand the customer's situation." (Situation Questions baseline)
2. "I ask questions specifically about the customer's problems, difficulties, or frustrations." (Problem Questions)
3. "When a customer mentions a problem, I follow up with questions about the downstream effects and costs of that problem." (Implication Questions)
4. "I ask questions that prompt the customer to articulate why solving the problem would be valuable to them." (Need-payoff Questions)
5. "I sequence my questions — building from context to problems to consequences to solutions — rather than asking in whatever order comes to mind." (SPIN sequencing)

**WHY:** Without a baseline, the practice plan cannot know where to start. A seller who scores 1 on all five items needs to start at the very beginning (Step 1 of the SPIN learning sequence: just ask more questions of any type). A seller who scores 4-5 on Situation and Problem but 1-2 on Implication needs a plan that focuses on Implication Questions specifically. Skipping the diagnostic means assigning the wrong starting behavior — the most expensive mistake in a practice plan.

**Output:** A SPIN level summary:
```
SPIN Level Summary
Situation Questions:     [score/5] — [Natural / Developing / Not yet in repertoire]
Problem Questions:       [score/5] — [Natural / Developing / Not yet in repertoire]
Implication Questions:   [score/5] — [Natural / Developing / Not yet in repertoire]
Need-payoff Questions:   [score/5] — [Natural / Developing / Not yet in repertoire]
Sequencing discipline:   [score/5] — [Natural / Developing / Not yet in repertoire]

Starting point: [Step X of the 4-step SPIN learning sequence — see Step 3]
```

### Step 2: Classify Account Portfolio — Safe vs. Key

**ACTION:** Review the user's account list. For each account (or account type), classify it into one of three categories:

- **SAFE — Practice Ground:** Small deal, early stage, strong personal relationship, or an account where a less-than-perfect call has minimal downside. These are where new behaviors get their first 3 attempts.
- **SAFE — Moderate:** Mid-tier accounts, reasonable relationship, some deal risk. New behaviors can be introduced here once they have been tried at least once on a full-safe account.
- **KEY — Protect:** High-value, late-stage, fragile relationship, or strategic deal. No new SPIN behaviors are practiced here until they are fully comfortable.

**Format:**
```
Account Safety Classification

SAFE — Practice Grounds (new behaviors start here):
- [Account name or type]: [Why safe — small deal, strong relationship, etc.]
- [Account name or type]: [...]

SAFE — Moderate (introduce after first attempt):
- [Account name or type]: [...]

KEY — Protect (only use behaviors already comfortable):
- [Account name or type]: [CRITICAL: no new behaviors here]
```

**WHY:** This is Rule 4 in action: practice in safe situations. Research consistently shows that people instinctively try new skills in high-stakes situations — precisely the wrong choice. New SPIN behaviors feel awkward (see Step 3 for why this is normal and temporary). An awkward Implication Question in a $500k deal at closing stage can cost the seller the sale. The same question in a small exploratory call costs nothing and teaches a great deal. The classification step makes Rule 4 concrete rather than abstract.

**Anti-pattern AP-12 — Practicing on Key Accounts:** If the user has no safe accounts in their portfolio (unlikely but possible), do NOT skip account classification — instead, tell the user they need to identify at least one safe practice context before starting the plan. This may mean cold prospecting calls, internal role-plays, or waiting for a new small inbound. Starting on key accounts is worse than not starting.

### Step 3: Apply the Four Golden Rules

**ACTION:** Present the Four Golden Rules to the user before building the schedule. These are the structural constraints that will govern every practice window in the plan.

For verbatim detail and the original analogies, see [references/four-golden-rules-detail.md](references/four-golden-rules-detail.md).

**Summary for plan-building:**

**Rule 1 — One behavior at a time.**
Pick one SPIN behavior. Practice it until it is comfortable. Then, and only then, add the next. Do not simultaneously practice Problem Questions AND Implication Questions AND Need-payoff Questions. That is the fastest path to abandoning all of them.

*Why it matters:* Tom Landry's single coaching principle was "work on one thing at a time, and get it right." Benjamin Franklin's system for learning virtues in his 1771 Autobiography follows the same discipline. The complexity of selling is already high — adding multiple simultaneous behavior changes overwhelms the seller and prevents any individual behavior from becoming automatic.

**Rule 2 — Try the new behavior at least 3 times before judging.**
The first attempt will feel unnatural and probably underperform. This is expected and does not mean the behavior is wrong for you. Out of 200 golfers asked whether their game improved after a professional lesson, 157 said their next round was worse — not because the lesson was bad, but because a new behavior first degrades before it improves. Give every new SPIN behavior a minimum of 3 attempts before deciding whether it works.

*Why it matters:* Abandoning a new behavior after one awkward call is the most common reason SPIN training fails. Anti-pattern AP-11 (judging on first attempt) directly causes the "I tried Implication Questions and they made the call worse" conclusion — which is almost always premature.

**Rule 3 — Quantity before quality.**
When practicing a new behavior, the goal is to use it as many times as possible per call — not to use it perfectly. Ask 8 Problem Questions per call, even if 5 of them are clumsy. Ask many Implication Questions, even if they feel blunt. The quality will improve as a byproduct of volume. Spending time worrying about how to phrase each question is a quality-first trap that slows skill acquisition dramatically.

*Why it matters:* Research on language learning shows that a quantity-first approach produces both more fluency AND better quality than a quality-first approach, in less time. The same principle applies to sales behaviors. A program that required sellers to ask only "high-quality" Problem Questions (with four sub-steps for each question) resulted in students asking an average of 1.6 Problem Questions per call — identical to the pre-training baseline.

**Rule 4 — Practice in safe situations first.**
Never try a new SPIN behavior in a key account or late-stage deal. Start with safe accounts (from Step 2). Move to moderate accounts only after 1-2 successful attempts. Bring new behaviors into key accounts only when they feel completely natural.

*Why it matters:* New behaviors are awkward and may temporarily reduce performance. This is the normal learning curve. The cost of that awkwardness is near-zero in a safe account and potentially catastrophic in a key account. The classification from Step 2 makes this rule concrete.

### Step 4: Build the Practice Plan Using the 4-Step SPIN Learning Sequence

**ACTION:** Using the user's SPIN level from Step 1 and the Four Golden Rules from Step 3, build a multi-week practice schedule. The plan starts at the appropriate step in the SPIN learning sequence and advances one behavior at a time.

**The 4-Step SPIN Learning Sequence:**

For verbatim detail and the full methodology, see [references/spin-learning-sequence.md](references/spin-learning-sequence.md).

**Step A — Ask more questions (any type).**
For sellers who have primarily been "telling" rather than asking. Goal: break the pattern of leading with features and advantages. Use any questions — most will be Situation Questions. Do not worry about quality. Just ask more. Practice windows: 2-3 weeks. Advance when questions feel as natural as telling.

**Step B — Develop Problem Questions.**
For sellers who ask questions but don't consistently probe for customer problems, difficulties, and dissatisfactions. Goal: ask about problems at least 6 times per call in the average call. Focus on quantity — don't worry about whether each question is "good." Practice windows: 2-3 weeks. Advance when 6 Problem Questions per call feels automatic.

**Step C — Plan and ask Implication Questions.**
For sellers who surface problems but don't develop their consequences. Goal: plan Implication chains before each call (using `spin-discovery-question-planner`) and then execute them in-call. This is the hardest step — expect 4-8 weeks of deliberate practice. Plan carefully; execute in volume. Implication Questions must be pre-planned — they cannot be reliably improvised.

**Step D — Ask Need-payoff Questions.**
For sellers who have developed needs through Implication Questions but still present benefits rather than asking the customer to articulate them. Goal: ask questions that get the customer talking about why a solution would be valuable — instead of you telling them. Focus on volume and variety.

**Practice Schedule Format:**

```
SPIN Practice Plan — [User Name] — Starting [Date]

Overall starting point: Step [A/B/C/D] of the SPIN learning sequence

──────────────────────────────────────────
WEEK 1-2: [BEHAVIOR NAME]
Goal: [Specific, measurable goal]
Rule 1: This is the ONLY SPIN behavior being practiced this window
Rule 2: Attempt minimum 3 times before drawing any conclusions
Rule 3: Volume goal: [X] per call — quality does not matter yet
Rule 4: Practice ONLY on these accounts: [names from safe list]
KEY accounts to protect: [names from key list — no new behaviors here]

Practice prompt: [Specific in-call instruction]
Review check: [What to note after each practice call]
──────────────────────────────────────────
WEEK 3-4: [NEXT BEHAVIOR]
[same structure]
──────────────────────────────────────────
WEEK 5-6: [NEXT BEHAVIOR — or advance to next learning step]
[same structure]
──────────────────────────────────────────

Retry budget:
- Feeling awkward is normal. Do NOT conclude a behavior is wrong until 3 attempts.
- If after 3 attempts the behavior still disrupts the call badly, return to Step 1 
  (re-diagnose) and check whether you are applying it in an appropriate context.
- If comfortable ahead of schedule: advance to the next behavior — don't wait.
```

**WHY:** A schedule without account specificity is abstract and does not get followed. Naming the actual safe accounts removes the decision friction at the moment of the call. Naming the protected accounts prevents the instinctive drift toward practicing in high-stakes situations. The retry budget prevents premature abandonment (AP-11).

### Step 5: Embed the Motivation Layer

**ACTION:** Before writing the final plan document, add a brief section that prepares the user for the discomfort of early practice. Use the empirical anchors from the source material.

**Framing to include in the plan:**

> "When you first try a new SPIN behavior, it will feel awkward. You may ask a clumsy Implication Question and see the customer's expression change. You may decide the new behavior is wrong for you. Almost certainly, that conclusion is premature.
>
> Out of 200 people who took golf lessons from a professional, 157 scored worse on their next round — not because the lesson was bad, but because integrating a new technique first disrupts performance before it improves it. The lesson was working. The outcome was temporary.
>
> Tom Landry's single coaching principle was 'work on one thing at a time, and get it right.' He was building a habit, not testing a hypothesis. One awkward call is not a test. Three attempts — with deliberate practice and post-call reflection — is the minimum for a fair evaluation.
>
> This plan gives you the structure to practice without pressure. The safe accounts are your range. The key accounts are the tournament. Practice on the range."

**WHY:** Without this framing, sellers abandon new behaviors after the first awkward attempt — this is anti-pattern AP-11. The golfer analogy provides an evidence-based reason to push through. The Landry and Franklin references elevate the principle from folk wisdom to validated methodology. Motivation scaffolding is not optional — it is the mechanism that keeps the plan in use past the first week.

### Step 6: Write the Practice Plan Document

**ACTION:** Compile all outputs from Steps 1-5 into a single file: `spin-practice-plan-{user}.md`. The document should be readable in under 5 minutes at the start of each practice week.

**Structure:**
1. SPIN Level Summary (from Step 1)
2. Account Safety Classification (from Step 2) — laminate this; refer to it before every call
3. The Four Golden Rules (brief version — link to references/ for depth)
4. Practice Schedule (from Step 4) — one section per practice window
5. Motivation Layer (from Step 5) — read this when it feels awkward

**WHY:** A written, dated document is the difference between a plan and an intention. Without it, the planning conversation evaporates. With it, the user has a reference they can return to each week and annotate with what they observed.

## Key Principles

- **One behavior at a time is not a suggestion — it is the constraint that makes learning possible.** The instinct to practice many things simultaneously is the fastest way to practice nothing effectively. Every practice window in the plan has exactly one target behavior.

- **The awkward phase is not evidence the behavior is wrong.** New skills degrade performance before improving it. 157 of 200 golfers scored worse after a professional lesson. The minimum sample for evaluation is three attempts in appropriate contexts. AP-11 (judging on first attempt) is the single most common cause of failed SPIN adoption.

- **Key accounts are for execution, not experimentation.** Rule 4 is absolute. Practicing a new SPIN behavior on a late-stage six-figure deal is not brave — it is expensive. Safe accounts exist precisely to absorb the awkwardness that is a normal and temporary feature of skill acquisition. AP-12 (practicing on key accounts) destroys both the skill and the deal.

- **Quantity produces quality faster than quality-first approaches do.** Ask many Problem Questions per call, even clumsy ones. The quality will emerge from volume and real-world feedback. A quality-first approach to skill learning consistently underperforms a volume approach by a wide margin — in language acquisition, in sales behavior training, and in other complex skills.

- **The practice plan is a starting point, not a constraint.** If a behavior becomes comfortable ahead of schedule, advance. If after three attempts a behavior is still disrupting calls badly, return to the SPIN level diagnostic and recalibrate. The schedule is a minimum structure, not a maximum commitment.

- **spin-discovery-question-planner is the operational complement.** This skill builds the practice curriculum; `spin-discovery-question-planner` prepares the actual question bank for each practice call. During the Implication Question practice window (Step C of the learning sequence), use `spin-discovery-question-planner` before every call on safe accounts to pre-plan Implication chains. The practice plan tells you which accounts to practice on and which behavior to focus on; the question planner tells you which specific questions to ask.

## Examples

**Scenario: New AE, just finished reading SPIN Selling, has a full pipeline**

Trigger: "I just finished SPIN Selling and want to start using it. I have about 15 accounts, a few of which are big deals. Where do I start?"

Process:
1. Diagnostic: scores 4/5 on Situation Questions (natural asking style), 2/5 on Problem Questions (asks occasionally), 1/5 on Implication Questions (never planned them), 1/5 on Need-payoff (doesn't know how to ask). Starting point: Step B (Problem Questions).
2. Account classification: 3 accounts flagged as key (major deals, late stage). 6 accounts classified as safe (small, early stage, or strong existing relationships). 6 accounts as moderate.
3. Practice schedule: Weeks 1-2: Problem Questions — target 6 per call — safe accounts only. Weeks 3-4: Problem Questions on moderate accounts — add volume not quality. Weeks 5-6: Begin Implication Question planning using spin-discovery-question-planner — safe accounts only, planned chains only, no improvised Implication Questions.
4. Key accounts: no new behaviors until week 7 minimum.

Output: `spin-practice-plan-alex-2026-04-14.md` with classified account list, 6-week schedule, retry budget.

---

**Scenario: Experienced rep, practiced SPIN for 2 weeks, gave up after "Implication Questions made calls worse"**

Trigger: "I tried SPIN for a couple of weeks. The Implication Questions felt really unnatural and I think they actually hurt a few calls. I've gone back to my old style."

Process:
1. Diagnose: this is AP-11 in action. Confirm: did the rep try Implication Questions at least 3 times in safe situations? Almost certainly not — most give up after 1-2 attempts, often on moderate or key accounts.
2. Apply Rule 2 framework: out of 200 golfers, 157 scored worse after a lesson. That doesn't mean the lesson was bad.
3. Rebuild plan from Step C (Implication Questions) — but now with explicit safe account assignment and a 3-attempt minimum before any evaluation.
4. Add the motivation layer as the first section of the plan.

Output: `spin-practice-plan-revised-2026-04-14.md` — same structure but framed as a restart with the AP-11 explanation at the top.

---

**Scenario: Sales manager building a practice plan for a new hire**

Trigger: "I'm onboarding a new AE and want to give them a structured SPIN learning plan. They have a small starter portfolio — 8 accounts, all small-to-mid size. I want them fluent in SPIN in 8 weeks."

Process:
1. Diagnostic administered on behalf of the new hire (or manager answers for them): likely starting at Step A (just ask more questions) given no prior SPIN exposure.
2. Account classification: all 8 accounts are safe by definition (small-to-mid, new rep, no existing key relationships to jeopardize). Flag one or two as "practice-priority" for dense early use.
3. 8-week schedule: Weeks 1-2: quantity questions (any type). Weeks 3-4: Problem Questions (6+ per call). Weeks 5-6: begin Implication Question pre-planning with spin-discovery-question-planner. Weeks 7-8: add Need-payoff Questions.

Output: `spin-practice-plan-new-hire-2026-04-14.md` — includes the manager review checklist (what to listen for in each phase's call recordings).

## References

- Four Golden Rules verbatim text and original analogies (Landry, Franklin, golfer study): [references/four-golden-rules-detail.md](references/four-golden-rules-detail.md)
- 4-step SPIN learning sequence verbatim text and implementation guidance: [references/spin-learning-sequence.md](references/spin-learning-sequence.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
- `clawhub install bookforge-spin-discovery-question-planner` — plan the actual SPIN question bank for each practice call (the operational complement to this skill; use it during the Implication Question and Need-payoff practice windows)

Skills this one builds on:
- `clawhub install bookforge-need-type-classifier` — classify customer responses during practice calls to know whether your Implication Questions developed a need successfully
- `clawhub install bookforge-sales-call-plan-do-review-coach` — wrap a full Plan-Do-Review cycle around individual calls in your practice plan (Level 2)

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
