---
name: coach-rep-with-pause-framework
description: "Plan a structured coaching session for a sales rep using the PAUSE framework (Prepare → Affirm → Understand → Specify → Embed). Use when a manager needs to: run a 'sales coaching session', 'coach a sales rep', use 'PAUSE coaching', ask 'pre-call coaching questions', run a 'post-call debrief', do 'challenger rep coaching', follow a 'sales manager coaching guide', 'coach the rep not the deal', answer 'how to coach my rep', or build a '1:1 coaching agenda'. Reads rep-profile-assessment.md from classify-rep-profile to identify the rep's weakest Challenger pillar, selects the Appendix A question set for that pillar, and produces a coaching-session-plan.md with pre-call questions, observation focus, post-call debrief, and an embed homework assignment. Also includes a decision gate: if the issue is deal-specific (stalled deal, unknown obstacle) rather than a rep-behavior gap, routes to the sales innovation mode (Investigate → Create → Share + optional SCAMMPERR) instead of PAUSE coaching."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/coach-rep-with-pause-framework
metadata: {"openclaw":{"emoji":"🎓","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors: ["Matthew Dixon", "Brent Adamson"]
    chapters: [8, "Appendix A"]
tags: [sales, sales-management, challenger-sale, sales-coaching, manager-coaching, rep-development]
depends-on: [classify-rep-profile]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "rep-profile-assessment.md (from classify-rep-profile) + deal-brief.md for the live deal the coaching session will anchor to + optional call-transcript.md from the most recent interaction with that customer"
  tools-required: [Read, Write, AskUserQuestion]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any working directory. No codebase required."
discovery:
  goal: "Plan a PAUSE coaching session tailored to the rep's weakest Challenger pillar, producing a ready-to-run coaching-session-plan.md"
  tasks:
    - "Read rep-profile-assessment.md to identify weakest Challenger pillar"
    - "Apply the coaching vs. innovating decision gate"
    - "If coaching: run PAUSE five-step protocol with pillar-specific Appendix A questions"
    - "If innovating: run Investigate → Create → Share on the stalled deal"
    - "Produce coaching-session-plan.md with pre-call, observation focus, post-call, and embed homework"
  audience:
    roles: ["sales managers", "front-line sales leaders", "sales enablement professionals"]
    experience: intermediate
  when_to_use:
    triggers:
      - "Manager has a rep diagnostic (rep-profile-assessment.md) and wants to run a coaching session"
      - "Manager wants to structure a 1:1 coaching conversation around a specific live deal"
      - "Manager wants pre-call and post-call coaching questions for a specific Challenger pillar"
      - "Manager wants a post-call debrief agenda for a call the rep just completed"
    prerequisites:
      - "rep profile assessment — run classify-rep-profile first to produce rep-profile-assessment.md"
    not_for:
      - "Manager self-diagnosis (use diagnose-manager-effectiveness)"
      - "Hiring or candidate screening"
      - "Rep profile classification (use classify-rep-profile)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 7
    iterations_needed: null
---

# Coach Rep with PAUSE Framework

Plans a complete, pillar-targeted coaching session using CEB's PAUSE framework (Prepare → Affirm → Understand → Specify → Embed) from Chapter 8 of _The Challenger Sale_, anchored to the Appendix A coaching questions per Challenger pillar.

The key prerequisite: run `classify-rep-profile` first. Its output (`rep-profile-assessment.md`) tells you which of the three Challenger subscales — Teaches for Differentiation, Tailors for Resonance, Takes Control — is the rep's weakest. This skill selects the matching Appendix A question set and builds a coaching session around that single pillar.

One session, one pillar, one observable change. That is the design principle.

## When to Use

- You have a rep who has completed the Appendix B self-diagnostic and you want to run their first structured coaching session
- You observed a call or meeting and want to structure specific feedback using a documented coaching protocol
- You want pre-call questions to prime the rep before an important customer meeting, tied to a specific Challenger behavior
- You have a deal you want to use as the coaching anchor and need a structured post-call debrief agenda
- Your rep is executing the right behaviors sometimes but not consistently — you want to embed the change, not just name it

**Not for:** deals that are stalled because neither you nor the rep knows what is blocking progress (that is the innovating mode — see Step 3). Not for manager self-diagnosis (use `diagnose-manager-effectiveness`).

## Context and Input Gathering

Before generating a coaching plan, collect:

1. **rep-profile-assessment.md** — produced by `classify-rep-profile`. Contains three subscale scores and identifies the weakest pillar. Read it before starting.
2. **deal-brief.md** — the specific live deal the coaching session will anchor to. A coaching conversation is most effective when it is grounded in a real deal the rep is actively working.
3. **call-transcript.md** (optional) — the most recent call or meeting with the anchor deal customer. If available, read it to identify specific moments where the target behavior was missing or weak.

If no deal brief is available, ask: "Which customer deal do you want to use as the coaching anchor for this session? Describe the customer, deal stage, and what happened in the most recent interaction."

## Process

### Step 1 — Read rep-profile-assessment.md and identify the target pillar

Read `rep-profile-assessment.md`. Locate the Challenger subscale scores:

| Subscale | Questions | Score | Threshold |
|---|---|---|---|
| Teaches for Differentiation | Q2+Q3 | x/10 | Strong: 8+ / Foundation: 5-7 / New territory: ≤4 |
| Tailors for Resonance | Q5+Q6 | x/10 | Strong: 8+ / Foundation: 5-7 / New territory: ≤4 |
| Takes Control | Q8+Q9 | x/10 | Strong: 8+ / Foundation: 5-7 / New territory: ≤4 |

Identify the single lowest-scoring subscale. That is the target pillar for this coaching session.

WHY: Splitting coaching attention across multiple pillars dilutes the session. CEB's PAUSE framework is designed to land one specific, observable behavior change per session. Trying to address all three pillars at once produces generic feedback that does not change behavior.

If two subscales are tied at the same score, ask the manager: "Between these two areas, which one showed up most clearly as a gap in the rep's most recent customer interaction?" Use the answer to select one.

### Step 2 — Load the deal brief and read the call transcript if available

Read `deal-brief.md`. Note:
- Customer name and deal stage
- What happened in the most recent interaction
- What is blocking progress or causing concern

If `call-transcript.md` is available, read it. Look specifically for moments where the target Challenger behavior (from Step 1) was either absent, weak, or handled differently than the Appendix A standard suggests.

WHY: The PAUSE framework is Hypothesis-Based Coaching. The hypothesis is: "In this specific interaction, the rep was not executing [target behavior]. Here is the specific moment I observed it." Coaching without a specific observed moment becomes abstract and hard for the rep to act on.

### Step 3 — Coaching vs. innovating decision gate

Before running PAUSE, apply this decision gate:

**Is this a rep-behavior gap?**
- The manager can name specifically what "good" looks like for the target behavior
- The rep knows the right behavior in principle but is not executing it consistently
- The gap is about skill, habit, or confidence — not about the deal situation being unusual

→ If yes: **COACH** using PAUSE (Steps 4–8 below)

**Or is this a deal-specific obstacle?**
- The deal is stalled and neither the manager nor the rep knows what is blocking it
- The obstacle is unique to this customer's situation and no standard playbook applies
- The question is "how do we get this deal unstuck?" not "how does the rep sell better?"

→ If yes: **INNOVATE** using Investigate → Create → Share (Step 9 below)

WHY: Coaching and innovating are distinct activities that require different manager modes. Coaching assumes the manager knows the answer and imparts it. Innovating assumes neither party knows the answer and they must collaborate to discover it. Applying coaching when the situation requires innovation means giving prescriptive direction to a problem that has no known solution — which often accelerates a deal loss rather than preventing it.

### Step 4 — PAUSE: Prepare

Before the coaching session begins, the manager completes preparation:

**What to review:**
- The rep's subscale score and the specific threshold it falls into
- Prior coaching notes or action items from the last session (maintain continuity)
- The deal brief and any call transcript for the anchor deal
- The Appendix A pre-call questions for the target pillar (see `references/appendix-a-questions.md`)

**Form the coaching hypothesis:**
Write one sentence that captures what "good" would have looked like in the specific interaction that anchored this session. Example: "In the discovery call with [Customer], good Teach behavior would have been introducing a specific insight about [industry problem] before asking about their situation — instead, the rep led with product features."

WHY: The hypothesis gives the coaching session its direction. Without it, the session becomes a general discussion rather than a targeted development interaction. The hypothesis also prevents the manager from coaching based on outcome (the deal didn't advance) rather than behavior (what the rep did that contributed to that outcome).

**Choose one observation focus:**
Select the specific Challenger behavior to observe in the next live interaction. Keep it narrow: one behavior, not a checklist.

### Step 5 — PAUSE: Affirm

Open the coaching conversation by naming what the rep is doing well — before surfacing the gap.

**How to affirm:**
- Reference a specific recent moment, not a general compliment
- Connect it to a Challenger behavior the rep has shown, even partially
- Keep it brief — one to two sentences

Examples:
- "I noticed in that call that you stayed with the pricing conversation rather than pivoting away from it. That took confidence."
- "Your prep work on the customer's competitive position was thorough — you clearly understood their market pressure."

WHY: If a rep does not feel safe in the coaching session, feedback is wasted. The Affirm step is not a softening technique — it is a precondition for the rep to hear what follows. Separating coaching from performance management requires the rep to experience this interaction as development, not evaluation. Starting with a genuine observation of strength establishes that.

Do not skip Affirm even if the session is urgent or the manager feels the rep needs direct correction. A coaching session where the rep is defensive accomplishes nothing.

### Step 6 — PAUSE: Understand

Invite the rep to self-diagnose before offering the manager's view.

Use the Appendix A pre-call planning questions for the target pillar (from `references/appendix-a-questions.md`) as the structure for this conversation:

**If target pillar is Teach:**
Ask the rep the Teach pre-call questions — but framed as reflection on the past interaction rather than preparation for a future one. Example: "Before that call, what did you think the business problem you were going to surface was? How did you know it was genuinely critical to them?"

**If target pillar is Tailor:**
Ask the Tailor questions as post-interaction reflection. Example: "Going into that meeting, what did you know about the trends hitting their industry right now? What was unique about their competitive position?"

**If target pillar is Take Control:**
Ask the Take Control questions. Example: "What was your intended next step at the end of that call? What do you know about how their organization actually makes this kind of purchase decision?"

WHY: Reps who self-identify a gap own the change. Reps who are told they have a gap may agree verbally but resist behaviorally. The Understand step is not a quiz — it is an opportunity for the rep to arrive at the gap diagnosis through their own reflection, with the manager holding the framework that structures that reflection.

Listen carefully. If the rep's self-diagnosis is accurate, confirm it and move to Specify. If the rep's self-diagnosis misses the actual gap, ask one follow-up question to guide them closer before naming what you observed.

### Step 7 — PAUSE: Specify

Agree on one specific, observable behavior change for the rep's next customer interaction.

**Format of the specification:**
"In your next call with [Customer / account type], when [specific moment], you will [specific observable action] instead of [current pattern]."

Examples by pillar:

**Teach:** "In your next discovery call, you will open with the industry insight about [problem] before asking about their situation — even if it feels like leading with a conclusion. The question to ask yourself afterward: did I teach them something, or did I just ask them questions?"

**Tailor:** "Before your next stakeholder meeting, you will write down one thing that is unique about this company's market position and one place where they are most vulnerable. You will find a way to reference at least one of those observations during the conversation."

**Take Control:** "At the end of your next meeting with this customer, you will name a specific next step with an owner and a date — out loud, in the meeting — rather than leaving it for a follow-up email."

WHY: Generic feedback ("be more assertive," "teach better") cannot be observed, measured, or coached at the next session. A specific observable behavior can be tracked, which gives the Embed step something to anchor to. CEB's PAUSE design requires the Specify step to be concrete enough that both the manager and rep can answer "did they do it or not?" after the next interaction.

Limit to one change per session. A list of behaviors is not a Specify — it is a performance review.

### Step 8 — PAUSE: Embed

Plan how the behavior change will be reinforced beyond this session.

**Three components of the Embed plan:**

**1. Homework before the next call:**
The rep completes a brief preparation task using the Appendix A pre-call questions for the target pillar before their next customer interaction with the anchor deal. Manager reviews it before the call.

**2. Observation checkpoint:**
If the manager can observe the next interaction (live, recorded, or ride-along), schedule it now. If not, agree on when the rep will debrief immediately after the call.

**3. Post-call debrief agenda:**
Use the Appendix A post-call questions for the target pillar (from `references/appendix-a-questions.md`) as the debrief structure. Schedule the debrief for within 24 hours of the interaction.

WHY: A coaching session that ends without continuity into the next interaction creates awareness but not change. The Embed step is what separates a coaching conversation from a one-time event. It ensures that the next coaching session begins with evidence of whether the specific behavior occurred — which gives coaching its cumulative effect over time.

Also: update the coaching log after the session. Note the target pillar, the specific observable change agreed on, and the scheduled debrief date. This creates the continuity that the next session's Prepare step will use.

### Step 9 — Innovating mode (when the gate routes here instead of PAUSE)

When the situation is a deal-specific obstacle — neither the manager nor the rep knows what is blocking progress — use the three-part sales innovation process:

**Investigate:** Work with the rep to map the customer's decision-making process in as much detail as possible. Ask:
- Who is involved in this decision beyond the contacts you have already spoken with?
- What decision criteria is this customer applying — and how do you know?
- What financial, organizational, or political concerns might be blocking progress that the customer has not stated directly?

The goal is to understand what is actually happening, not assume the obstacle is what it appears to be.

**Create:** Co-create options with the rep without immediately evaluating them. This is thought partnership, not deal inspection. Consider:
- Can we reposition our capabilities to better connect to a challenge this customer actually has?
- Can we shift risk from their side to ours in exchange for a longer commitment or expanded scope?
- What has worked in a similar stalled deal elsewhere that we could adapt here?

Use the SCAMMPERR framework (from `references/scammperr-framework.md`) to expand thinking before defaulting to a price concession or standard escalation. The tool generates options — it does not require answering every question.

**Share:** After resolving the deal (or during the next team meeting), document what worked and why. The innovation that unsticks one deal often applies to another.

WHY: Stalled deals fail two ways: the manager gives the rep a prescriptive answer that does not fit the specific situation, or the manager and rep iterate through the same options without generating new ones. Innovating mode is explicitly collaborative because the manager does not know the answer — and pretending otherwise produces bad advice delivered confidently.

### Step 10 — Write coaching-session-plan.md

Produce a written coaching plan the manager can carry into the session.

```markdown
# Coaching Session Plan

**Rep:** [Name]
**Date:** [YYYY-MM-DD]
**Deal anchor:** [Customer name + deal stage]
**Target pillar:** [Teach / Tailor / Take Control]
**Subscale score:** [x/10] — [Strong / Foundation / New territory]

---

## Prepare (manager completes before session)

**Coaching hypothesis:**
[One sentence: what "good" would have looked like in the observed interaction]

**Observation focus for next call:**
[One specific behavior to watch for]

**Prior coaching continuity:**
[What was agreed last session? Did the rep do it?]

---

## Pre-call Questions (Understand step — ask rep to self-diagnose)

[Insert the Appendix A pre-call questions for the target pillar]

---

## Affirm (open the session with)

[One specific genuine observation of a recent strength]

---

## Specify (agreed behavior change)

"In your next call with [Customer], when [moment], you will [action] instead of [current pattern]."

---

## Embed Plan

**Homework before next call:**
[Pre-call planning task using Appendix A questions]

**Observation checkpoint:**
[Date/format: live, recorded, or immediate post-call debrief]

**Post-call debrief agenda:**
[Appendix A post-call questions for the target pillar]

**Next coaching session date:**
[YYYY-MM-DD]

---

## Coaching Log Update

[Note target pillar, specific observable change, debrief date — for next session's Prepare step]
```

## Inputs

| Input | Required | Description |
|---|---|---|
| rep-profile-assessment.md | Yes | From classify-rep-profile — contains subscale scores |
| deal-brief.md | Yes | The live deal used as the coaching anchor |
| call-transcript.md | Optional | Most recent customer interaction for this deal |
| Prior coaching notes | Optional | Continuity from the last PAUSE session |

## Outputs

**Primary artifact:** `coaching-session-plan.md`

Includes: coaching hypothesis, Affirm opener, Appendix A pre-call questions (pillar-specific), Specify statement (one observable change), Embed plan (homework + observation checkpoint + post-call debrief agenda + next session date).

## Key Principles

**1. One pillar per session.** The PAUSE framework produces one observable behavior change. Attempting to address multiple pillars in a single session produces generic coaching and no lasting change. If the rep has two weak pillars, schedule two sessions.

WHY: CEB's research found that coaching effectiveness depends on specificity. The more targeted the feedback, the more likely the rep can act on it in their next interaction. Broad coaching produces awareness without behavior change.

**2. Coaching assumes the manager knows the answer.** If the manager does not know what "good" looks like for the target behavior in the specific deal context, run the innovating mode instead. Coaching from uncertainty produces advice that sounds authoritative but isn't.

WHY: The fundamental distinction between coaching and innovating is epistemic. Coaching is teaching. Innovating is discovering. Using a teaching approach when you are actually discovering together creates false confidence in the wrong direction.

**3. The Specify step must be observable.** "Be more assertive" is not a Specify. "In the meeting, when the customer pushes back on price, stay with the conversation for at least two exchanges before offering an alternative" is a Specify.

WHY: The Embed step cannot work without a concrete behavior to verify. If neither the manager nor the rep can answer "did it happen?" after the next interaction, the coaching session did not produce a Specify.

**4. Affirm is not optional.** The psychological safety created by the Affirm step is a precondition for the rep to hear the Understand and Specify steps without becoming defensive. Skipping it to "save time" destroys the conditions that make the rest of the session work.

WHY: CEB's PAUSE framework separates performance management from coaching development. Performance management creates defensiveness (because there are consequences). Coaching creates openness (because it is safe). Affirm is the mechanism that establishes which mode the rep experiences the session as.

**5. Embed creates the cumulative effect.** A single PAUSE session that ends without a scheduled post-call debrief and the next session date is just a conversation. The behavior change happens across sessions, not within them. Embed is where the ROI of coaching accrues.

WHY: CEB found that the biggest gap in sales manager coaching is not the quality of individual sessions — it is continuity between them. Managers who coach inconsistently produce reps who improve inconsistently. The Embed step institutionalizes continuity.

## Examples

### Example 1 — Teach pillar coaching session (complex SaaS deal)

**Setup:** Rep scored Teach=6, Tailor=8, Take Control=7. Weakest: Teach. Anchor deal: mid-market VP Sales at a SaaS company, discovery call coming up next week for a $180k annual contract.

**Coaching hypothesis (Prepare):** "In the last call, the rep led with product features instead of surfacing a business problem the customer hasn't seen yet. Good Teach behavior would have been opening with the insight that companies at this customer's growth stage typically underinvest in pipeline visibility until it causes a missed quarter — before asking about their current setup."

**Affirm:** "I noticed you came into that last call with detailed knowledge of their competitor's recent pricing move. That preparation shows you were thinking about their world, not just your product."

**Understand (pre-call questions for Teach):**
- What business problem are you planning to surface in the discovery call next week?
- How do you know this is genuinely high-priority for a VP Sales at a company this size?
- Why hasn't this customer solved this problem on their own already?

**Specify:** "In your discovery call next week, you will open with the pipeline visibility problem — before asking a single question about their current setup. If you catch yourself asking questions first, pause and introduce the insight before continuing."

**Embed:** Homework — use the Teach pre-call questions from Appendix A to write a one-page call prep before the discovery call. Debrief within 24 hours using the Teach post-call question: "How provoked or intrigued was the customer when you surfaced the insight? What told you that?"

---

### Example 2 — Innovating mode (stalled deal, unknown obstacle)

**Setup:** Rep's deal with a large enterprise customer has been in legal review for six weeks. No standard objection — the deal just isn't moving. Manager does not know what is blocking it.

**Decision gate:** This is not a rep-behavior gap. Neither the manager nor the rep knows what is stalling the deal. Route to innovating mode.

**Investigate:** Work with the rep to map the customer's internal process. Who is in legal? Who is sponsoring this deal internally at the customer? What does the customer's standard vendor approval process look like — is six weeks normal or abnormal? What did the rep hear most recently from any contact inside the account?

**Create:** Generate options without evaluating them immediately. Could we modify contract terms to reduce the customer's perceived risk? Could we offer a 30-day pilot to get internal momentum before full legal review? Is there an executive sponsor at the customer who could accelerate the legal process — and has the rep engaged them?

**SCAMMPERR prompt:** Under "Adapt" — what have we done to move past a legal stall in a similar deal? Under "Put to other uses" — is there a part of our offering we could scope down to get a faster-path signature while the main contract moves through review?

**Share:** After resolution, document what worked in the internal coaching log for the team.

## References

- [Appendix A Coaching Questions by Challenger Pillar](references/appendix-a-questions.md) — Full pre-call and post-call question sets for Teach, Tailor, and Take Control
- [SCAMMPERR Framework](references/scammperr-framework.md) — Structured deal repositioning tool for the innovating mode

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

- **classify-rep-profile** ← Run this first. Produces rep-profile-assessment.md with the subscale scores this skill reads.
- **diagnose-manager-effectiveness** — For managers who want to assess their own coaching/innovating time allocation before building a coaching practice.
- **diagnose-taking-control-gaps** — Deep-dives into Take Control skill gaps when that subscale is the coaching target.
