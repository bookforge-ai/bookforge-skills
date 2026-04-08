---
name: negotiation-one-sheet-generator
description: |
  Build a complete Negotiation One Sheet — a five-section preparation document that covers your aspirational goal, a counterpart-validating situation summary, a preemptive accusation audit, a calibrated question bank, and a list of noncash offers — before any negotiation, sales conversation, contract discussion, salary negotiation, or difficult ask. Use when you need to prepare for a high-stakes conversation in a single document, when you want to stop improvising and start with a battle-tested preparation framework, when you keep leaving deals on the table by aiming at your bottom line instead of your aspirational target, when you need to combine emotional preparation with offer strategy into one coherent plan, or when you are coaching someone else through a complex negotiation. Also use before any negotiation where you have 20+ minutes to prepare and want to walk in with every major tool loaded: counterpart profile, labels, questions, offer sequence, and noncash options. Produces negotiation-one-sheet.md — a complete, ready-to-use preparation document with all five sections filled. Works standalone with simplified inline processes or in full-depth mode by invoking the seven supporting Level 0 skills. The hub of the Never Split the Difference skill set.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/negotiation-one-sheet-generator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [23]
tags: [negotiation, preparation, one-sheet, goal-setting, accusation-audit, calibrated-questions, noncash-offers, tactical-empathy, ackerman, bargaining, sales, salary-negotiation, hub-skill]
depends-on:
  - counterpart-style-profiler
  - accusation-audit-generator
  - calibrated-questions-planner
  - empathic-summary-planner
  - ackerman-bargaining-planner
  - black-swan-discovery
  - commitment-verifier
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Situation brief — what the negotiation is about, who the counterpart is, what you want, what you know about their position and constraints"
    - type: document
      description: "Your aspirational goal — the best-case outcome you want. Not your walk-away point. If you don't know, the process will help you set one."
    - type: document
      description: "Any prior artifacts from Level 0 skills (optional) — counterpart-profile.md, accusation-audit.md, calibrated-questions.md, ackerman-plan.md, black-swan-report.md"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works from a free-text situation brief or a full document set from Level 0 skills. Richer context produces a more targeted one sheet."
discovery:
  goal: "Produce negotiation-one-sheet.md — a complete five-section preparation document covering aspirational goal, situation summary, labels/accusation audit, calibrated questions, and noncash offers"
  tasks:
    - "Set an aspirational goal using the four-step process (not BATNA-anchored)"
    - "Write a two-sentence situation summary that will trigger genuine validation from the counterpart"
    - "Prepare 3-5 preemptive labels targeting the counterpart's anticipated emotions"
    - "Prepare 3-5 calibrated How/What questions across three categories"
    - "Identify noncash items the counterpart possesses that would add value"
    - "Optionally invoke Level 0 skills for deep output in each section"
    - "Write negotiation-one-sheet.md"
  audience:
    roles: ["salesperson", "founder", "manager", "consultant", "recruiter", "lawyer", "freelancer", "job-seeker", "anyone-who-negotiates"]
    experience: "beginner to intermediate — no formal negotiation training required"
  triggers:
    - "User is preparing for a negotiation and wants a single comprehensive preparation document"
    - "User wants to combine goal, empathy, questions, and offer strategy in one place"
    - "User has used one or more Level 0 skills and wants to integrate their outputs into a final prep document"
    - "User is coaching someone else through a negotiation and needs a complete framework"
    - "User has 20+ minutes before a negotiation and wants to use that time optimally"
  not_for:
    - "Deep counterpart profiling — use counterpart-style-profiler for a full three-archetype classification"
    - "In-depth accusation audit with delivery scripting — use accusation-audit-generator"
    - "Full calibrated question bank with deployment sequencing — use calibrated-questions-planner"
    - "Detailed Ackerman offer schedule with computed amounts — use ackerman-bargaining-planner"
    - "Black Swan hypothesis mapping — use black-swan-discovery"
    - "Verifying commitment quality after the negotiation — use commitment-verifier"
---

# Negotiation One Sheet Generator

## When to Use

You are preparing for a negotiation — a salary discussion, sales conversation, vendor contract, partnership deal, difficult ask, or any high-stakes conversation where you want more than your bottom line. You have at least 20 minutes to prepare and want to walk in with every major tool loaded.

The Negotiation One Sheet is a five-section preparation document. It takes the place of a script (which makes you rigid) and replaces it with prepared tools (which make you adaptive). When pressure hits, you do not rise to the occasion — you fall to your highest level of preparation. This document is that level.

**Use this skill to build the full one sheet.** Use the Level 0 skills listed in `depends-on` when you want deep, standalone output for any individual section. The hub works in two modes:

- **Standalone mode:** Each section uses a simplified inline process. Produces a complete one sheet without invoking any other skill.
- **Integrated mode:** For sections where a Level 0 skill is available and loaded, invoke it to get deeper output, then copy the relevant artifact into the one sheet.

---

## Context & Input Gathering

### Required
- **The situation:** What are you negotiating? What does a good outcome look like? Who is the counterpart?
- **What you want:** Your aspirational target — or enough information to set one in Section I.

### Important
- **What you know about the counterpart:** Their role, what they care about, prior communication history, their likely objections.
- **Available noncash items:** Things you could offer that have high value to them and low cost to you.

### Optional (if Level 0 skills have been run)
- `counterpart-profile.md` — informs Section III (label calibration) and Section II (summary tone)
- `accusation-audit.md` — can replace Section III
- `calibrated-questions.md` — can replace Section IV
- `ackerman-plan.md` — informs Section I (goal feeds Ackerman target)
- `black-swan-report.md` — adds a Bonus Section VI

### Sufficiency Check
You need at minimum: the situation and a rough sense of what you want. Everything else can be inferred. If you have nothing, ask the user to describe the negotiation in 3-5 sentences before proceeding.

---

## Process

Work through the five sections sequentially. For each section, check whether a relevant Level 0 skill artifact is available. If yes, invoke it (or use its output). If no, use the inline process below.

---

### Section I: Goal

**Action:** Set a single aspirational goal — the best-case outcome, written down.

**WHY:** The most common preparation mistake is anchoring preparation to your walk-away point (the minimum acceptable outcome). Decades of goal-setting research confirm that people who set specific, challenging, but realistic goals get better outcomes than those who aim at their minimum. When a walk-away point becomes the focus of preparation, it becomes the psychological ceiling — the negotiator relaxes when they reach it and stops pushing. An aspirational goal does the opposite: it primes you to treat anything short of it as a loss, keeping you psychologically engaged throughout the negotiation. This is the core insight behind refusing to "split the difference" — when you aim at your minimum, splitting gives you something worse than your minimum minus margin.

**Inline four-step process:**

1. **Define the range.** Think through both ends — the absolute worst acceptable outcome AND the best plausible outcome. Write both. The range gives you structure; you need both ends to feel grounded.
2. **Set the aspirational target.** Choose the high end as your goal. Make it specific and concrete (a number, a date, a set of terms). Write it down. Vague goals produce vague negotiations.
3. **Commit it externally.** Write the goal down and share it with a colleague before the negotiation. Externalized commitments are harder to abandon — you psychologically resist lowering a target that another person has witnessed you set. A goal you only think is a goal you will abandon under pressure.
4. **Carry it in.** The written goal goes with you into the negotiation — physically or on screen. It is your anchor when the counterpart puts pressure on your bottom line.

**If `ackerman-plan.md` is available:** The target price in that document is your Section I goal. Paste it here.

**Section I output:**
```
**My Aspirational Goal:** [Specific, concrete best-case outcome]
**Why this is achievable:** [One sentence — what evidence or logic supports this target]
**My absolute floor (not on the one sheet, for mental reference only):** [Walk-away point]
```

---

### Section II: Situation Summary

**Action:** Write a 2-sentence situation summary that describes the facts from the counterpart's perspective — accurate enough that they would respond with "That's right" when they hear it.

**WHY:** The situation summary is not a self-serving description of why you deserve what you want. Its purpose is to demonstrate to the counterpart — at the opening of the conversation — that you understand their situation accurately. This triggers genuine validation ("That's right") rather than polite acknowledgment ("You're right"). The difference matters enormously: "That's right" means the counterpart feels understood; "You're right" means they want to end the conversation. A counterpart who feels understood lowers their emotional guard. A counterpart who feels misunderstood — or believes you are starting from a self-serving interpretation of the facts — immediately activates resistance that no amount of logic will overcome. Emotional preparation precedes rational persuasion. This is not optional: the emotional brain (System 1) evaluates whether you understand the situation before the rational brain (System 2) will engage with your arguments.

**Inline process:**

1. Write 1 sentence describing the situation from the counterpart's perspective: what are the facts as they see them, and what is at stake for them?
2. Write 1 sentence describing what they are likely trying to achieve: what does a good outcome look like from their side?
3. Check: would your counterpart respond "That's right" if they heard this? If they would respond "Well, not exactly..." — revise until they would agree.
4. Keep it to 2 sentences maximum. A longer summary signals you are making an argument, not demonstrating understanding.

**If `empathic-summary-planner` is available:** The "That's right" trigger statement in that skill's output is your Section II summary. Paste it here.

**Section II output:**
```
**Situation Summary (2 sentences):**
[Sentence 1 — facts from their perspective]
[Sentence 2 — what they are trying to accomplish]

**"That's right" test:** [Would they agree? If not, what needs to change?]
```

---

### Section III: Labels / Accusation Audit

**Action:** Prepare 3-5 preemptive labels that name the counterpart's anticipated negative feelings before they surface.

**WHY:** Emotional objections voiced by a counterpart have more force than the same objections that stay unspoken — because the counterpart has now committed to them publicly. Naming them first, before the counterpart does, drains the charge. When you say "It seems like you might be concerned this isn't going to be worth your time" before the counterpart thinks it, they cannot use that concern as a weapon. If the label is right, they feel understood. If it is wrong, they correct you — which still advances the conversation. The mechanism is neurological: naming a negative emotion engages the prefrontal cortex and reduces amygdala activation. The counterpart's emotional brain calms down. Their rational brain comes online. This is what makes emotional preparation more valuable than rational scripting.

**Inline process:**

1. List every accusation the counterpart might make — stated in their voice, uncensored. Include the extreme ones.
2. Convert each into a label using the formula: "It seems like \_\_\_\_" / "It sounds like \_\_\_\_" / "It looks like \_\_\_\_". Never "I feel" or "I think you feel."
3. Select the 3-5 most emotionally charged labels. Sequence from strongest to lightest.
4. Add the fill-in-the-blank templates below for any gaps:

**Universal label templates (fill in the blank):**
- "It seems like \_\_\_\_\_\_\_\_\_ is valuable to you."
- "It seems like you don't like \_\_\_\_\_\_\_\_\_."
- "It seems like you value \_\_\_\_\_\_\_\_\_."
- "It seems like \_\_\_\_\_\_\_\_\_ makes it easier."
- "It seems like you're reluctant to \_\_\_\_\_\_\_\_\_."

**If `counterpart-style-profiler` is available:** The counterpart's type (Analyst/Accommodator/Assertive) tells you which category of concerns to weight most heavily. Analysts fear surprises and insufficient data. Accommodators fear relationship damage and conflict. Assertives fear being ignored or not heard.

**If `accusation-audit-generator` is available:** The label bank in that skill's output replaces this section. Paste the 3-5 sequenced labels here.

**Section III output:**
```
**Anticipated Accusations (raw):**
1. [Their voice — worst-case thought]
2. [Their voice]
3. [Their voice]

**Labels (3-5, sequenced strongest to lightest):**
Label 1: "It seems like ___________." [Pause 3-5 seconds]
Label 2: "It sounds like ___________." [Pause 3-5 seconds]
Label 3: "It seems like ___________." [Pause 3-5 seconds]
[Label 4 if applicable]
[Label 5 if applicable]
```

---

### Section IV: Calibrated Questions

**Action:** Prepare 3-5 How/What questions across three categories: value-revealing, behind-the-table stakeholder discovery, and deal-killing issue identification.

**WHY:** A negotiator who only talks about their own position never finds out what the counterpart actually needs — which means they can never offer something that genuinely satisfies both sides. Calibrated questions shift the problem-solving burden to the counterpart, generate information, and give the counterpart a sense of control (because they are the one providing answers). "How" and "What" questions do this cleanly. "Why" questions — even well-intentioned ones — sound like accusations ("Why is that a concern for you?" implies their concern is unjustified) and produce defensiveness, not information. The three-category structure ensures you are not just asking about stated positions: you are also surfacing the stakeholders who can kill the deal from off-screen, and diagnosing problems that will derail implementation after a handshake.

**Inline process:**

**Category A — Value-revealing questions** (what matters to them, what success looks like):
- "What are we trying to accomplish?"
- "How is that worthwhile?"
- "What's the core issue here?"
- "How does that affect things?"
- "What's the biggest challenge you face?"
- "How does this fit into what the objective is?"

**Category B — Behind-the-table stakeholder questions** (who else has veto power):
- "How does this affect the rest of your team?"
- "How on board are the people not in this conversation?"
- "What do your colleagues see as their main challenges in this area?"

**Category C — Deal-killing issue questions** (what could prevent implementation):
- "What are we up against here?"
- "What happens if you do nothing?"
- "What does doing nothing cost you?"
- "How does making a deal with us affect things?"
- "How does this resonate with what your organization values?"

**Selection guidance:** Choose 1-2 questions from each category. Ask them in groups of 2-3 — similar questions from the same category help the counterpart think about the same issue from multiple angles without feeling interrogated. Prepare a follow-up label template for each question.

**Follow-up label templates (for after their answers):**
- "It seems like \_\_\_\_\_\_\_\_\_ is important."
- "It seems like you feel my organization is in a unique position to \_\_\_\_\_\_\_\_\_."
- "It seems like you're worried that \_\_\_\_\_\_\_\_\_."

**If `calibrated-questions-planner` is available:** The deployment groups in that skill's output replace this section. Paste the question bank here, selecting your 3-5 highest-priority questions.

**Section IV output:**
```
**Selected Questions:**

[Category A — Value-Revealing]
Q1: [How/What question]
→ Follow-up label: "It seems like ___________."

Q2: [How/What question]
→ Follow-up label: "It sounds like ___________."

[Category B — Behind-the-Table]
Q3: [How/What question about stakeholders]
→ Follow-up label: "It seems like ___________ has a stake in this."

[Category C — Deal-Killing Issues]
Q4: [How/What question about obstacles]
→ Follow-up label: "It seems like ___________ could be the real challenge."

[Q5 optional]
```

---

### Section V: Noncash Offers

**Action:** List noncash items your counterpart possesses — or that you possess — that could be traded to reach agreement when money alone has stalled.

**WHY:** A surprisingly high percentage of negotiations hinge on something other than price. Counterparts often have constraints, status needs, or interest in non-monetary outcomes that are far cheaper for the other side to provide than the gap in the cash number. The negotiator who only thinks about price leaves these trades on the table. Asking "what could they give that would almost make us do this for free?" forces creativity about value beyond money. It also produces your strongest noncash closing move: offering something of genuine value to the counterpart alongside your final price — especially when that price is a precise, non-round number — signals that you have exhausted your financial flexibility and are finding other ways to make the deal work. This makes your final number feel more credible and final.

**Inline process:**

1. Ask: "What could they give me that would almost make me do this for free?" List 3 candidates.
2. Ask: "What could I give them that costs me little but would be genuinely valuable to them?" List 3 candidates.
3. Select the 1-2 most viable options from each list.
4. Identify which item is most appropriate as a final-stage sweetener alongside your last offer.

**Examples by situation type:**
- Salary negotiation: Additional vacation days, remote flexibility, earlier performance review, professional development budget, equity acceleration
- Vendor/service purchase: Longer contract term, public testimonial, case study rights, referral to other buyers, priority support access
- Real estate: Flexible closing date, furniture items included, quick pre-approval, waived contingencies
- B2B sales: Speaking opportunity, advisory board seat, co-marketing, logo placement, named reference

**If `ackerman-bargaining-planner` is available:** The noncash item selected in that skill's output is your primary Section V item for the final offer stage. Add it here and expand the list.

**Section V output:**
```
**Noncash Items They Could Offer Me:**
1. [Item — why it's valuable to me, why it costs them little]
2. [Item]
3. [Item]

**Noncash Items I Could Offer Them:**
1. [Item — why it's valuable to them, why it costs me little]
2. [Item]
3. [Item]

**Best final-stage sweetener:** [The single most valuable noncash item to include with the last offer]
```

---

### Bonus Section VI: Black Swan Hypotheses (optional)

**If `black-swan-discovery` is available:** Paste the top 2-3 Black Swan hypotheses from that skill's `black-swan-report.md` here. These are the unknown unknowns that could explain surprising behavior or break the deal entirely. Carry them as live hypotheses — watch for signals during the conversation.

**If the skill is not available:** Skip this section or list 1-2 things that feel unexplained about the counterpart's behavior so far.

---

### Final Step: Write the One Sheet

**Action:** Produce `negotiation-one-sheet.md` by assembling all five (or six) sections into a single document. The one sheet must be short enough to review in 2 minutes before walking into the conversation. If any section exceeds one short paragraph or 5 bullet points, summarize it. Each section should contain 3-5 items maximum.

**WHY:** The one sheet fails if it becomes a binder. Its purpose is to be a live reference document — reviewed immediately before the conversation, carried into the room, consulted if the conversation stalls. It must be fast to read under pressure. Length is the enemy of use.

---

## Inputs

| Input | Required | Format |
|---|---|---|
| Situation brief | Yes | Any — markdown, plain text, verbal description |
| Aspirational goal (or enough to set one) | Yes | A number, term, or outcome |
| Counterpart description | Yes | Role, what they care about, prior history |
| Level 0 skill artifacts | Optional | counterpart-profile.md, accusation-audit.md, calibrated-questions.md, ackerman-plan.md, black-swan-report.md |
| Noncash items | Optional | Anything of value beyond money |

---

## Outputs

**Primary output:** `negotiation-one-sheet.md`

```markdown
# Negotiation One Sheet: [Deal / Conversation Name]

**Prepared by:** [Name / role]
**Counterpart:** [Name / organization / role]
**Date:** [Date of negotiation]

---

## Section I: Goal

**My Aspirational Goal:** [Specific, concrete best-case outcome — a number, a set of terms, a deadline]

**Why achievable:** [One sentence — the evidence or logic that makes this goal realistic, not just wishful]

*(Walk-away floor is known but not written here — it is not the target.)*

---

## Section II: Situation Summary

**Summary (2 sentences):**
[Sentence 1 — facts from their perspective]
[Sentence 2 — what they are trying to accomplish]

**"That's right" test:** [Would they agree? Note any uncertainty.]

---

## Section III: Labels / Accusation Audit

**Labels (3-5, sequenced strongest to lightest):**

Label 1: "It seems like ___________."
*[Pause 3-5 seconds after delivery.]*

Label 2: "It sounds like ___________."
*[Pause 3-5 seconds.]*

Label 3: "It seems like ___________."
*[Pause 3-5 seconds.]*

[Label 4 if applicable]
[Label 5 if applicable]

**Delivery note:** Open with the labels before any ask. Downward inflection — statement, not question. Do not fill the silence after each label.

---

## Section IV: Calibrated Questions

**Value-Revealing:**
- [How/What question] → Follow-up label: "It seems like ___________."
- [How/What question] → Follow-up label: "It sounds like ___________."

**Behind-the-Table Stakeholders:**
- [How/What question] → Follow-up label: "It seems like ___________ has a stake in this."

**Deal-Killing Issues:**
- [How/What question] → Follow-up label: "It seems like ___________ could be the real challenge."

[Optional 5th question]

**Deployment note:** Ask questions in groups of 2-3. Pause and label after each answer before asking the next.

---

## Section V: Noncash Offers

**Items I could offer them (high value to them / low cost to me):**
1. [Item]
2. [Item]

**Items they could offer me (high value to me / potentially low cost to them):**
1. [Item]
2. [Item]

**Final-stage sweetener:** [The single noncash item to pair with the last offer]

---

## Section VI: Black Swan Hypotheses (if applicable)

- [Hypothesis 1 — unknown unknown that could explain their behavior or constraints]
- [Hypothesis 2]
*(Watch for signals during the conversation. If a hypothesis confirms, pivot.)*

---

## Post-Negotiation Follow-Up

- [ ] Was a genuine "That's right" obtained on the situation summary?
- [ ] Were all labels delivered before the first ask?
- [ ] Were the calibrated questions asked, or did you skip to position-trading?
- [ ] Was the final offer accompanied by a noncash item?
- [ ] Any verbal commitments that need `commitment-verifier` analysis?
```

---

## Key Principles

**Preparation is the multiplier.** Every hour spent on a Negotiation One Sheet yields at least a 7:1 return on time saved from renegotiating deals and clarifying implementation. The investment is not in the document — it is in the mental simulation the preparation forces. Negotiators who prepare a one sheet have already imagined the hard moments before they arrive.

**The aspirational goal is the engine; the walk-away point is just the guardrail.** BATNA (Best Alternative to a Negotiated Agreement) anchors negotiators to their minimum because the human brain, under the cognitive load of a live negotiation, gravitates toward the most psychologically significant number it has prepared. Preparing an aspirational target puts that number front-and-center instead. The walk-away point exists to prevent catastrophic outcomes — not to aim at.

**The One Sheet is a toolkit, not a script.** The One Sheet is a toolkit of prepared tools (labels, questions, offers), NOT a predetermined script. Scripts make you rigid and exploitable — they break the moment the counterpart says something you did not anticipate. Tools give you prepared responses that adapt to whatever direction the conversation takes.

**Emotional preparation (labels, accusation audit) must precede rational preparation (goals, numbers).** The counterpart's System 1 (fast, emotional brain) processes social signals before System 2 (slow, rational brain) can engage with facts. Calming System 1 with empathic labels opens the door for System 2 to evaluate your proposal rationally. This is why the section ordering of the one sheet is not arbitrary: a summary that triggers genuine validation (Section II) and labels that defuse anticipated hostility (Section III) are prerequisites to productive engagement with questions (Section IV) and offers (Sections I and V).

**The five sections are interdependent.** Goal (I) feeds the Ackerman offer sequence. The situation summary (II) uses the counterpart profile. Labels (III) are calibrated to the counterpart's emotional state. Questions (IV) surface deal-killers before they surface on their own. Noncash items (V) are the creative exit from purely positional bargaining. Prepare all five — they compound.

**The one sheet is a live reference document.** It must be reviewable in 2 minutes. Long preparation documents are not consulted under pressure. One page — two at most — that you can glance at when the conversation stalls or when you are tempted to split the difference.

---

## Examples

### Example 1: Salary Negotiation

**Scenario:** A senior engineer preparing to negotiate a 25% raise with their current employer. They know budget constraints exist but also know their work has driven significant retention impact. They have 30 minutes before the conversation.

**Trigger:** "Help me build a complete one sheet for my salary negotiation this afternoon."

**Process:**
- Section I: Aspirational goal set at 25% raise (above market mid-range for the role). Walk-away at 15%. Written and stated to a friend.
- Section II: Summary written from manager's perspective — acknowledges budget cycle pressure and that raises are being evaluated against team-wide equity, not just individual performance.
- Section III: Three labels prepared — strongest first: "It seems like any raise right now creates a precedent problem with the rest of the team." Second: "It sounds like the timing isn't great given what the budget situation looks like." Third: "It seems like you want to reward good work but you're constrained by what's possible."
- Section IV: Two value-revealing questions (What does retention of high performers cost us relative to a raise?), one stakeholder question (How are decisions like this usually made — is it just you or does HR need to sign off?), one deal-killer question (What happens if this conversation doesn't go anywhere today?).
- Section V: Noncash items identified — earlier performance review cycle in exchange for lower raise increment now; remote work flexibility; professional development budget for conference attendance.

**Output:** `negotiation-one-sheet.md` with all five sections filled, goal set at 25%, two-sentence summary written from manager's perspective, three sequenced labels, four calibrated questions with follow-up labels, and two noncash alternatives as final-stage creative options.

---

### Example 2: Vendor Contract Renewal

**Scenario:** A procurement manager renewing a SaaS contract. The vendor has sent a 30% price increase. The procurement manager wants to hold price flat and secure a 2-year term.

**Trigger:** "I have a contract renewal meeting tomorrow. The vendor wants 30% more. Build me a one sheet."

**Process:**
- Section I: Goal — hold price flat or max 5% increase, lock in 2-year term with price protection. Walk-away at 15% increase maximum.
- `counterpart-style-profiler` invoked — vendor account manager classified as Assertive. Adaptation: lead with label before counter-position. Get to the point quickly. Do not over-explain rationale.
- Section II: Summary from vendor's perspective — they need to justify pricing to their own leadership and have been under margin pressure. The account relationship has been stable but the procurement manager has not been vocal about value internally.
- `accusation-audit-generator` invoked — three labels prepared: strongest first: "It seems like you're in a position where you can't bring a flat renewal back to your team and have it look like a win." Second: "It sounds like the pricing increase is tied to something that happened at the platform cost level, not just a negotiating position." Third: "It seems like locking in a longer term creates some of its own complications for you internally."
- Section IV: Three questions — What would a 2-year commitment change about how you think about the pricing? How does this account fit into your team's goals for retention this year? What happens to the pricing structure if we decide to go to market?
- Section V: Noncash items — offer a public case study, agree to introductory reference calls for two new prospects, offer a multi-year term with annual increases capped at CPI.

**Output:** Complete `negotiation-one-sheet.md` integrating counterpart-profile and accusation-audit outputs, with Assertive-adapted delivery notes and a noncash offer structured around reference value rather than cash.

---

### Example 3: Partnership Deal with a Larger Company

**Scenario:** A startup founder negotiating a distribution partnership with a much larger company. Power asymmetry is significant. The larger company's champion is enthusiastic but internal approval is uncertain.

**Trigger:** "I'm meeting their VP next week. There's a real deal here but I don't know who else needs to approve this. Build me a one sheet."

**Process:**
- `black-swan-discovery` invoked — key hypothesis: the champion does not have final authority and there is an internal stakeholder (legal or procurement) who has not been surfaced. A second hypothesis: the larger company is evaluating two alternatives simultaneously and is using the meeting to gather competitive information.
- Section I: Goal — signed letter of intent with exclusivity clause, revenue share above 20%, and implementation timeline under 90 days. Walk-away: any deal without exclusivity protection.
- Section II: Summary from VP's perspective — their team needs a credible distribution solution before the end of the quarter. This partnership solves a problem they have already identified internally. The risk for them is picking a partner who underdelivers and creating an embarrassment.
- Section III: Three labels — strongest: "It seems like the real concern is what happens if this partnership doesn't work and your team has publicly backed it." Second: "It sounds like there are people not in this meeting whose buy-in you need before anything can move." Third: "It seems like the timeline is being driven by something on your side that we haven't fully talked about yet."
- Section IV: Value-revealing (What does success look like for your team 12 months from now?), stakeholder (How on board are the people who would actually implement this?), deal-killer (What would have to be true for this not to move forward?).
- `commitment-verifier` noted for post-meeting use — any "yes" from the VP in this meeting should be analyzed before treating as a commitment.

**Output:** `negotiation-one-sheet.md` with Black Swan hypotheses in Section VI, stakeholder-focused questions dominating Section IV, labels targeting the political risk of public backing, and a post-meeting action item to run commitment-verifier on the VP's responses.

---

## References

| File | Contents |
|------|----------|
| `references/one-sheet-framework.md` | Extended one sheet guidelines: when to use standalone vs. integrated mode, how to time-box preparation, how to adapt the one sheet for remote vs. in-person conversations, one sheet anti-patterns |
| `references/level0-skill-integration.md` | How to pass context between Level 0 skill artifacts and the one sheet: file naming conventions, copy-paste workflows, which sections each artifact feeds |
| `references/system1-system2-prep.md` | Why emotional preparation beats rational scripting: the influence arc (Active Listening → Empathy → Rapport → Influence → Behavioral Change), System 1 / System 2 neuroscience, and the ordering logic behind the one sheet's five sections |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-counterpart-style-profiler`
- `clawhub install bookforge-accusation-audit-generator`
- `clawhub install bookforge-calibrated-questions-planner`
- `clawhub install bookforge-empathic-summary-planner`
- `clawhub install bookforge-ackerman-bargaining-planner`
- `clawhub install bookforge-black-swan-discovery`
- `clawhub install bookforge-commitment-verifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
