---
name: sales-call-plan-do-review-coach
description: "Wrap a structured Plan-Do-Review learning loop around any B2B sales call. Use this skill when someone says 'prep me for tomorrow's call with [company]', 'review my call from yesterday', 'help me debrief this meeting', 'what should I learn from this call?', 'build a call brief for next week', 'post-call debrief', 'I just had a discovery call and want to process it', or 'am I actually improving between calls?'. This skill runs in two modes: PRE-CALL — consolidates outputs from spin-discovery-question-planner (SPIN question bank) and commitment-and-advance-planner (Advance objective) into a single call brief you can read 5 minutes before the meeting; POST-CALL — applies Rackham's seven specific review questions to your actual call notes and produces a written debrief that ties directly to the next call's plan. The closed loop is the distinguishing feature: each call's review becomes the next call's plan. Based on Rackham's empirical finding that top performers review every call in detail while average performers say 'it went quite well' — a global conclusion that prevents any learning. Works on call notes, transcripts, or recalled summaries."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/sales-call-plan-do-review-coach
metadata: {"openclaw":{"emoji":"🔄","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [8]
tags: [sales, b2b-sales, enterprise-sales, call-planning, call-review, post-call-analysis, learning-loop, spin-methodology, pre-call-prep, discovery, plan-do-review]
depends-on:
  - spin-discovery-question-planner
  - call-outcome-classifier
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "deal-brief.md — company, contact, deal stage, deal size, what is known so far"
    - type: document
      description: "call-notes-{date}.md or call-transcript-{date}.md — for post-call mode (what actually happened)"
    - type: document
      description: "question-bank-{deal}-{date}.md — output of spin-discovery-question-planner (if already run)"
    - type: document
      description: "commitment-plan-{deal}-{date}.md — output of commitment-and-advance-planner (if already run)"
    - type: document
      description: "call-review-{prior-date}.md — prior review from a previous call on this deal (optional, enables closed-loop iteration)"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "document_set — reads deal-brief.md, call notes/transcripts, and prior dependency outputs; produces call-plan-{date}.md (pre-call) and call-review-{date}.md (post-call)."
discovery:
  goal: "Produce a pre-call brief that consolidates question bank and Advance objective into a single readable artifact, and a post-call review that applies seven specific review questions with evidence from actual call notes, tied to the next call's plan"
  tasks:
    - "Pre-call: consolidate spin-discovery-question-planner output and commitment-and-advance-planner output into a 5-minute call brief"
    - "Post-call: apply all 7 of Rackham's specific review questions to the call notes"
    - "Post-call: cite evidence from actual call notes when answering each review question"
    - "Tie post-call review findings to the next call's planning inputs (closed loop)"
    - "Surface the top-performer distinction: specific detail analysis vs global 'it went well'"
  audience:
    roles: [account-executive, enterprise-sales-rep, solutions-consultant, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "Rep has a call tomorrow and needs a consolidated brief"
      - "Rep just finished a call and wants a structured debrief"
      - "Manager wants to coach a rep using post-call review discipline"
      - "Rep is working a multi-call deal and wants to learn between calls"
    not_for:
      - "Generating SPIN questions from scratch — use spin-discovery-question-planner"
      - "Planning the Advance objective from scratch — use commitment-and-advance-planner"
      - "Classifying the call outcome — use call-outcome-classifier"
      - "SPIN methodology learning curriculum — use spin-skill-practice-coach"
      - "Closing attitude self-assessment — use closing-attitude-self-assessment"
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
      - "Output applies all 7 of Rackham's specific post-call review questions"
      - "Output cites evidence from the user's actual call notes when answering review questions"
      - "Output produces a pre-call brief consolidating question bank and Advance objective"
      - "Output ties post-call review to a specific next-call planning input (closed loop)"
      - "Output does NOT produce vague feedback like 'the call went well'"
    what_baseline_misses:
      - "Produces vague post-call feedback ('looks like the customer was interested, follow up next week')"
      - "Does not apply all 7 specific review questions — generates generic debrief points"
      - "Does not cite specific moments from the call notes as evidence"
      - "Does not connect post-call findings to a next-call plan"
---

# Sales Call Plan-Do-Review Coach

## When to Use

You are working a multi-call B2B deal and you want to learn from each call — not just run them.

**Pre-call mode:** You have a call coming up. You may already have a question bank from `spin-discovery-question-planner` and an Advance objective from `commitment-and-advance-planner`. This skill consolidates both into a single call brief you can read 5 minutes before the meeting.

**Post-call mode:** You just finished a call. You have call notes or a transcript. This skill applies Rackham's seven specific review questions to your actual notes, producing a written debrief with evidence-grounded answers — and ties those findings to what you should do differently on the next call.

**Closed loop:** The post-call review feeds the pre-call plan for the next call. Over a multi-call cycle, each call iteration builds on lessons from the prior one.

**The top-performer distinction:** Rackham's research found two consistent differences in top salespeople: (1) they put great emphasis on reviewing each call — dissecting what they learned and thinking about possible improvement; (2) they understand that success rests on getting behavioral details right, not broad strategy. Average sellers say "it went quite well" and learn nothing. This skill enforces detail-level review.

This skill is out of scope for: generating SPIN questions (use `spin-discovery-question-planner`), planning the Advance objective (use `commitment-and-advance-planner`), classifying call outcomes (use `call-outcome-classifier`), SPIN learning curriculum (use `spin-skill-practice-coach`).

## Context & Input Gathering

### Mode Detection

**Step 0:** Determine which mode to run.

- If the user says "prep me", "plan", "call brief", "before the call" → **PRE-CALL mode** (Steps 1-2)
- If the user says "review", "debrief", "what did I learn", "just had a call" → **POST-CALL mode** (Steps 3-5)
- If unclear → ask: "Are you preparing for an upcoming call or reviewing one that just happened?"

### Required Context (must have — ask if missing)

For **PRE-CALL mode:**
- **Deal context:** Who is the prospect? What stage is the deal?
  -> Check for: `deal-brief.md`
  -> If missing, ask: "Tell me the company, contact, deal stage, and what you know about their situation."
- **Question bank:** SPIN questions for this call.
  -> Check for: `question-bank-{deal}-{date}.md` (output of `spin-discovery-question-planner`)
  -> If missing: "Invoke `spin-discovery-question-planner` first, then return here with the output. Alternatively, paste your planned questions directly."
- **Advance objective:** The specific customer action you're targeting.
  -> Check for: `commitment-plan-{deal}-{date}.md` (output of `commitment-and-advance-planner`)
  -> If missing: "Invoke `commitment-and-advance-planner` first, then return here with the output. Or tell me: what specific action do you want the customer to commit to on this call?"

For **POST-CALL mode:**
- **Call record:** Notes or transcript from the call just completed.
  -> Check for: `call-notes-{date}.md` or `call-transcript-{date}.md`
  -> If missing, ask: "Paste your notes or describe what happened on the call."
- **Prior call brief:** What you planned to do (the pre-call artifact, if available).
  -> Check for: `call-plan-{date}.md`
  -> If missing: ask what the objectives were. Proceed without it if unavailable.

### Observable Context (gather from environment)

- **Prior review:** `call-review-{prior-date}.md` — findings from the previous call on this deal.
  -> If available: read it. Surface any unresolved findings from the prior review in this one.
  -> If unavailable: treat this as the first review in the cycle.

### Sufficiency Threshold

PRE-CALL SUFFICIENT: Deal context + question bank + Advance objective → produce full call brief
PRE-CALL PROCEED WITH DEFAULTS: Deal context only → produce a brief with dep skill prompts clearly marked
POST-CALL SUFFICIENT: Call notes → produce full review (prior brief improves quality but is not required)
MUST ASK: No call notes AND no recalled summary for post-call mode

## Process

### PRE-CALL: Step 1 — Assemble the Call Brief Header

**ACTION:** Produce a one-page header for the call. Include: account name, contact name and role, call date/time, call type (first discovery / follow-up / executive / demo), deal stage, and the primary Advance objective from `commitment-and-advance-planner` (or from the user if the skill has not been run).

**WHY:** The brief's header frames everything that follows. Reading the Advance objective first keeps the seller oriented toward the call's success criterion — the specific customer action to be obtained — rather than a vague sense of "having a good meeting." Without this anchor, sellers drift toward information exchange (a Continuation pattern) instead of driving toward a committed next step.

**Output format:**
```
CALL BRIEF — [Account] — [Date]

Contact: [Name], [Role]
Call type: [Type]
Deal stage: [Stage]

PRIMARY ADVANCE OBJECTIVE:
[Specific customer action — verbatim from commitment-and-advance-planner output or user input]

FALLBACK ADVANCE:
[Secondary commitment target if primary is declined]
```

### PRE-CALL: Step 2 — Consolidate the Question Bank

**ACTION:** From the `spin-discovery-question-planner` output (or user-supplied questions), extract and reformat into a condensed, readable question brief. Structure: Situation Questions (limited), Problem Questions per hypothesis, Implication chains (key questions only — not the full planning artifact), Need-payoff Questions, and the sequence guide. Keep to one page.

**WHY:** The full question bank from `spin-discovery-question-planner` may be 2-3 pages — too long to skim in 5 minutes before a call. This step distills it to the essentials: the questions the seller actually intends to ask, in sequence order, with the branching rules that matter most. Sellers who have to search through a long document during a call lose conversational flow. A condensed brief produces more natural question delivery.

**Output:** Append to the call brief as Section 2: "Question Sequence." Mark each question by type (S/P/I/N). Include: "START HERE →" for the first 1-2 questions, and the sequence-guide decision rules in plain language (1-2 lines max).

**Output file:** `call-plan-{date}.md` — write the complete pre-call brief to this file.

---

### POST-CALL: Step 3 — Read the Call and Extract Evidence

**ACTION:** Read the call notes or transcript. Create an evidence inventory: list every significant customer statement, question response, and behavioral signal observed during the call. Note where questions were asked and what responses they produced. Note any surprises relative to the pre-call plan.

**WHY:** The post-call review requires evidence-grounded answers. Without this extraction step, review answers become based on the seller's overall impression ("I think it went well") rather than specific moments. Evidence prevents rationalization and exposes what was actually said vs. what the seller thought they said. This step is the foundation for all seven review questions that follow.

**Output:** A structured evidence log (internal, not written to a file yet) organized by call stage: opening → discovery questions → customer responses → capability discussion → closing.

### POST-CALL: Step 4 — Apply the Seven Review Questions

**ACTION:** Apply each of Rackham's seven specific post-call review questions to the evidence extracted in Step 3. Answer each with specific, evidence-grounded observations from the call notes. Do not produce vague summaries.

See `references/post-call-review-questions.md` for the verbatim questions and detailed prompts.

**The seven review questions:**

**Q1: Did I achieve my call objectives?**
Check the Advance objective from the pre-call plan (or stated objective). Did the customer commit to the specific action targeted? Apply `call-outcome-classifier` if not already done, or apply the four-outcome framework inline (Order / Advance / Continuation / No-sale). State which outcome was achieved and name the customer action if it was an Advance.

**WHY:** Without a clear objective, every call feels like a success. Checking the specific Advance forces precision — the outcome either happened or it didn't, and a Continuation is not a success regardless of how positive the call felt.

**Q2: If I were making this call again, what would I do differently?**
Name 1-3 specific behavioral changes. Not general improvements ("ask better questions") — specific moments ("In minute 12, when the customer mentioned the procurement delay, I moved to a feature demo instead of asking an Implication Question about the downstream effects of the delay — that was the wrong turn").

**WHY:** Specific behavioral alternatives are actionable in the next call. Generic self-critique ("I could have done better") produces no change in behavior. The behavioral specificity is what transforms review from reflection into a learning signal.

**Q3: What have I learned that will influence future calls on this account?**
Extract 1-2 account-specific insights: new information about the customer's situation, stakeholder dynamics, decision process, or buying criteria that changes how you should approach the next call. Update the deal-brief.md or needs-log.md with these findings.

**WHY:** Each call should advance your model of the account. Sellers who treat calls as isolated events lose cumulative intelligence. This question forces the seller to update their account model rather than starting the next call from the same baseline.

**Q4: What have I learned that I can use elsewhere?**
Extract 1 transferable insight — a question that worked better than expected, an Implication chain structure that moved the conversation, a customer language pattern that surfaced the need more clearly. This insight applies across the portfolio.

**WHY:** Individual learning compounds across the account portfolio. A Implication Question structure that worked in this conversation may be directly applicable to three other accounts with similar problems. Without this question, individual call learning stays siloed.

**Q5: Did some parts of the call go better than others? Why?**
Identify 1-2 high-performing moments and 1-2 low-performing moments from the evidence inventory. For each, state the specific behavior and the customer response it produced. Distinguish luck from skill.

**WHY:** Global assessments ("the call went well" or "the call went poorly") obscure what actually drove the outcome. Understanding which behaviors worked — and which didn't — at the moment level is how behavioral repertoire is built. This is the granular diagnostic that separates learning from experience-accumulation.

**Q6: Which specific questions had the most influence on the customer?**
Identify 2-3 questions that visibly shifted the customer's engagement, language, or position. Note what type they were (S/P/I/N) and what the customer's response revealed about their needs.

**WHY:** Rackham's research found only 1 in 20 questions in an average call is an Implication Question — yet these are the questions most correlated with major-sale success. Tracking which questions actually influenced the customer builds empirical awareness of the seller's question portfolio and corrects systematic imbalances.

**Q7: Which needs changed or emerged during the discussion? Why?**
List any needs that shifted from Implied to Explicit during the call, any new needs that surfaced unexpectedly, and any needs the customer raised that you had not anticipated. Note what prompted the shift.

**WHY:** Need development is the core mechanism of SPIN. If needs changed, something in the conversation caused it — an Implication chain that landed, a question that reframed the problem's cost. If no needs developed, that is the most important finding: the Investigating stage failed to advance the deal. This question diagnoses the core of the call's value.

### POST-CALL: Step 5 — Write the Review Artifact and Next-Call Inputs

**ACTION:** Write `call-review-{date}.md` with the seven review question answers. Then produce a brief "Next Call Inputs" section at the bottom: 2-4 specific observations from this review that should change the pre-call plan for the next call.

**WHY:** The review artifact closes the loop. Without it, the insights exist only in the current conversation and are lost. The "Next Call Inputs" section makes the handoff from review to planning explicit — the seller reads this section when invoking this skill for the next call's pre-call mode. This is the mechanism that converts per-call learning into cumulative skill development.

**Output template:**
```
# Call Review — [Account] — [Date]
Reviewed by: sales-call-plan-do-review-coach

## Call Outcome
[Classification: Order / Advance / Continuation / No-sale]
[Customer action committed, or statement that none was committed]

## Seven Review Questions

### Q1: Did I achieve my call objectives?
[Evidence-grounded answer]

### Q2: If I were making this call again, what would I do differently?
[1-3 specific behavioral alternatives with moment-level context]

### Q3: What have I learned that will influence future calls on this account?
[1-2 account-specific insights — update deal-brief.md or needs-log.md accordingly]

### Q4: What have I learned that I can use elsewhere?
[1 transferable insight]

### Q5: Did some parts of the call go better than others?
[High-performing moments and low-performing moments with evidence]

### Q6: Which specific questions had the most influence on the customer?
[2-3 questions with type label and customer response that followed]

### Q7: Which needs changed or emerged during the discussion?
[Need shifts: Implied → Explicit, new unexpected needs, unopened need paths]

---

## Next Call Inputs (closed loop)

**Changes to the question plan:**
[Specific adjustments to the question bank for the next call]

**Advance objective adjustment:**
[Whether the same Advance applies next call or needs to be revised]

**Account model updates:**
[New information to add to deal-brief.md or needs-log.md before next call]
```

## Key Principles

- **Detail over global judgment.** Rackham's exact words: "Never be content with global conclusions like 'it went quite well.' Ask yourself about the details." Top performers dissect what worked and what didn't at the moment level. Every vague summary is a missed learning opportunity.

- **The review is more valuable than the call itself.** Limited learning comes from planning a call or running it. The most important lessons come from the way you review it. Planning and doing are prerequisites; reviewing is where skill development actually happens.

- **Evidence grounds every answer.** Each of the seven review questions must be answered with a specific moment, quote, or observation from the call notes — not from impression. If the call notes do not support a specific answer, that absence is itself a finding (the seller did not observe carefully enough).

- **Dependency orchestration.** This skill orchestrates two dependency skills. For pre-call mode: invoke `spin-discovery-question-planner` to produce the question bank, and `commitment-and-advance-planner` to produce the Advance objective. For post-call mode: invoke `call-outcome-classifier` (or apply its four-outcome framework inline) to classify the call outcome before answering Q1. This skill consolidates and coaches — it does not replicate the methodology of its dependencies.

- **The closed loop is the output.** A pre-call plan without a post-call review is wasted. A post-call review without a next-call plan is incomplete. The value of this skill is the accumulation: each cycle produces a better-informed plan, which produces a more observable call, which produces a richer review. Without the loop, each call is isolated.

## Examples

**Scenario: Pre-call brief for a second discovery call**

Trigger: AE has a follow-up call in the morning. They've already run `spin-discovery-question-planner` and `commitment-and-advance-planner`. They ask: "Build a call brief for my call tomorrow with Acme."

Process: (1) Read `question-bank-acme-2026-04-14.md` and `commitment-plan-acme-2026-04-14.md` from the working directory. (2) Extract the Advance objective (e.g., "Customer agrees to introduce VP of Operations on the next call") and fallback ("Customer agrees to a product trial"). (3) Distill the question sequence to the 3-4 most important questions per problem, with branching rules in plain language. (4) Write `call-plan-2026-04-15.md` as a single-page brief.

Output: `call-plan-2026-04-15.md` — one page. AE reads it in 5 minutes before the meeting. Advance objective is the first thing visible.

---

**Scenario: Post-call review after a demo that "went well"**

Trigger: AE says "The demo went really well. The VP seemed very interested. Help me review it." Call notes show the VP said "fantastic, we'll be in touch" and no specific next step was set.

Process: (1) Read call notes. Evidence inventory: VP said "this is exactly what we need" (sentiment, not commitment) and "we'll be in touch" (classic Continuation phrase). No customer action committed. (2) Q1: Did I achieve objectives? No — the outcome is a Continuation (apply `call-outcome-classifier` framework: no specific customer action = not an Advance). Flag the Continuation-as-success misread. (3) Q2: What would I do differently? At the call's end, instead of accepting "we'll be in touch," I should have asked "What would make sense as a next step — would it make sense to loop in your procurement lead this week?" (4) Q7: Which needs changed? The VP's strong interest suggests the need shifted toward explicit — but without a Need-payoff question being asked, it was never confirmed as explicit. Plan: ask Need-payoff questions earlier next call. (5) Write `call-review-2026-04-14.md`. Next Call Inputs: adjust Advance objective (VP intro to procurement); add specific Need-payoff questions for the emerging need around reporting automation.

Output: `call-review-2026-04-14.md` — 7-question review with moment-level evidence, a Continuation classification, and 3 specific next-call inputs.

---

**Scenario: Closed-loop iteration — third call in a deal**

Trigger: AE is prepping for call #3. Prior review (`call-review-2026-04-07.md`) identified that Implication Questions about the downstream effects of delayed procurement were skipped on call #2. AE asks: "Build a call brief for my call next week."

Process: (1) Read prior review. Note the unresolved finding: Implication Questions on procurement delay were planned but not asked — insert them explicitly into the brief's question sequence. (2) Read updated `question-bank-acme-2026-04-14.md` (which incorporates the prior review's learnings). (3) Note the Advance objective from the prior review's "Next Call Inputs" section: "Get VP to commit to a product trial date." (4) Write `call-plan-2026-04-21.md` — leading with the Implication chain that was missed last time.

Output: `call-plan-2026-04-21.md` — brief with the specific corrective from the prior review embedded. The loop is closed.

## References

- Seven post-call review questions (verbatim + detailed prompts): [references/post-call-review-questions.md](references/post-call-review-questions.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
```
clawhub install bookforge-spin-discovery-question-planner
clawhub install bookforge-call-outcome-classifier
```

Also useful alongside this skill:
```
clawhub install bookforge-commitment-and-advance-planner
```

This skill orchestrates the full Plan-Do-Review loop. Browse the complete SPIN Selling skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
