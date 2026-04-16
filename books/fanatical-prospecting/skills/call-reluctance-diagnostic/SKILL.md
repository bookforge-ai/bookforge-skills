---
name: call-reluctance-diagnostic
description: "Diagnose and coach through call reluctance, prospecting avoidance, and sales slumps. Use this skill when you can't make yourself prospect, are procrastinating on cold calls, avoiding the phone, or stuck in a low-activity week. Produces a diagnosis and 1-week intervention plan for: why can't I prospect, prospecting fear, three ps, perfectionism sales, paralysis from analysis, procrastinating on cold calls, slump mindset, mental toughness sales, prospecting motivation, can't pick up the phone."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/call-reluctance-diagnostic
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting: The Ultimate Guide to Opening Sales Conversations and Filling the Pipeline by Leveraging Social Selling, Telephone, Email, Text, and Cold Calling"
    authors: ["Jeb Blount"]
    chapters: [2, 7, 21]
tags: [sales, prospecting, mindset, mental-toughness, call-reluctance, sdr, bdr]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "User's self-report on recent prospecting behavior, activity counts from the last 5 days, what came up instead of prospecting, and how they feel about picking up the phone"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Markdown document for self-reflection. The plan IS the deliverable — the human executes it."
discovery:
  goal: "Diagnose the dominant prospecting performance blocker (one of three named failure modes) and produce a specific 1-week intervention plan keyed to that diagnosis."
  tasks:
    - "Gather symptom inventory from the past 5 days of prospecting behavior"
    - "Run a Seven Mindsets baseline self-score to identify lowest-rated dimensions"
    - "Apply Three Ps differential diagnosis to identify dominant failure mode"
    - "Scan user language for victim-mindset markers"
    - "Produce a diagnosis report and 1-week coaching plan with failure-mode-specific interventions"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner-to-intermediate
  triggers:
    - "call reluctance"
    - "can't make myself prospect"
    - "procrastinating on cold calls"
    - "avoiding the phone"
    - "mental toughness sales"
    - "prospecting fear"
    - "three ps"
    - "perfectionism sales"
    - "why can't I prospect"
    - "prospecting motivation"
    - "slump mindset"
  prerequisites: []
  not_for: "Reps who are not prospecting because they genuinely hate sales and the job is wrong for them — Blount explicitly calls this out: if you cannot will yourself to dial and find this unbearable, this is a career fit problem, not a coaching problem."
  environment: "Markdown self-reflection document. Minimal tooling — no CRM access required."
  quality: placeholder
---

# Call Reluctance Diagnostic

## When to Use

Use this skill at the end of a low-activity week, before a planned prospecting block when you feel resistance, or when you notice you have been consistently avoiding the phone or inbox. Common triggers:

- You had a full day scheduled for prospecting and ended it having made fewer than 10 calls
- You keep telling yourself you'll prospect "after this one thing"
- You spent your prospecting block researching, organizing, or cleaning up the CRM instead of dialing
- You keep asking "but what if they say…" before making your first call of the day
- Your manager has flagged low activity and you cannot explain why

**What this skill produces:** A written diagnosis report that names your dominant failure mode (one of three), rates your mindset baseline across seven dimensions, flags any victim-language patterns in your self-description, and prescribes a specific 1-week intervention. The plan is the deliverable — you execute it.

**This is not for:** Reps who find sales genuinely intolerable and are considering a career change. Blount is direct: if you physically cannot will yourself to dial and dread every moment of prospecting, that is a job-fit problem, not a call-reluctance problem. This skill cannot fix the wrong career.

---

## Context and Input Gathering

Before diagnosis, gather honest data. Ask yourself — or ask the user to provide — answers to these questions:

**Activity data (last 5 business days):**
- How many prospecting calls did you actually make each day? (Write a number, not "some" or "a few")
- How many were planned or expected?
- What was your ratio of dials attempted to decision-makers reached?
- How many prospecting emails or LinkedIn messages did you send?

**Blocker data (what happened instead):**
- When you should have been prospecting, what were you doing instead?
- Did you tell yourself you needed to do more research before calling?
- Did you find reasons to delay starting your calling block?
- Did you replay past rejections or "what-if" scenarios in your head before dialing?

**Emotional data:**
- On a scale of 1–10, how much resistance do you feel right now when you think about picking up the phone?
- Do you find yourself blaming external factors — the territory, the leads, your product, your manager — for your low activity?
- What language do you use when you talk to colleagues about your pipeline and why it is thin?

If the user has provided a written self-report, read it carefully before proceeding. Look for: specific activity numbers, named excuses, and any language that assigns blame to external factors.

**Default assumptions when data is thin:**
- If no activity numbers are provided, assume the issue is real and recent (not hypothetical)
- If the user cannot name a specific blocker, start with the Three Ps diagnostic and let the symptoms surface
- If activity is zero for multiple days, weight paralysis-from-analysis as the most likely primary blocker

---

## Process

### Step 1: Symptom Inventory

**ACTION:** Write out what happened in the last 5 days. Do not estimate — use actual numbers if available. Map each work day against prospecting activity.

**WHY:** Self-delusion about activity is one of the most common and costly patterns in sales. In one coaching session Blount observed, a rep claimed "easily 50 calls" — the CRM log showed 12 in 7 hours. Two early harsh rejections had tripped the rep's confidence and they stopped without realizing it. Putting actual numbers on paper forces an honest baseline and surfaces the gap between what you believed you were doing and what you were actually doing. The gap itself is diagnostic data.

**Output:** A simple 5-day table:

| Day | Planned calls | Actual calls | Decision-makers reached | What I did instead |
|-----|--------------|--------------|------------------------|-------------------|
| Mon | | | | |
| Tue | | | | |
| Wed | | | | |
| Thu | | | | |
| Fri | | | | |

If actual < planned by more than 30%, proceed to Step 2 immediately.

---

### Step 2: Seven Mindsets Baseline Self-Score

**ACTION:** Rate yourself 1–5 on each of the seven mindsets that define high-performing prospectors. Be honest — this is a private self-assessment.

**WHY:** Before diagnosing which blocker is active, you need a baseline of which mindset dimensions are weakest. Low scores consistently cluster around specific failure modes: low Relentless + low Confident tends to predict paralysis-from-analysis; low Systematic + low Optimistic predicts procrastination; low Confident + low Adaptive predicts perfectionism. The self-score is not a performance review — it is a calibration instrument.

**Rating scale:** 1 = this almost never describes me / 5 = this consistently describes me

| # | Mindset | Behavioral marker | Score (1–5) |
|---|---------|------------------|-------------|
| 1 | Optimistic and enthusiastic | I attack each day ready to prospect even after a rough stretch. I don't let yesterday's rejections set the tone for today. | |
| 2 | Competitive | I track my activity vs. peers. I feel driven to outwork my competition at outreach. | |
| 3 | Confident | I expect most conversations to go well. I manage fear and self-doubt when I dial. | |
| 4 | Relentless | I treat rejection as fuel. I never let a "no" stop me from making the next call. | |
| 5 | Thirsty for knowledge | I actively seek coaching and feedback. I invest time in learning prospecting craft. | |
| 6 | Systematic and efficient | I protect my prospecting blocks. I run targeted lists and dial efficiently without over-preparing. | |
| 7 | Adaptive and flexible | I experiment with new approaches. I adjust quickly when a channel or message stops working. | |

**Score interpretation:**
- Any dimension rated 1–2: flag as a development target
- Total score < 21 (average < 3): mindset work is foundational before tactical fixes will hold
- Lowest 1–2 dimensions: these are inputs to the Three Ps diagnosis in Step 3

Full behavioral descriptions for each mindset are in [references/seven-mindsets-rubric.md](references/seven-mindsets-rubric.md).

---

### Step 3: Three Ps Differential Diagnosis

**ACTION:** Identify the dominant failure mode from three named patterns. These have different root causes and require different interventions — lumping them together produces generic advice that fixes none of them.

**WHY:** "Call reluctance" is a catch-all label that obscures what is actually happening. Blount identifies three mechanically distinct blockers. A rep who is procrastinating needs a discipline intervention (small daily commitments). A rep who is perfectionizing needs a research-budget constraint (cap preparation time). A rep who is paralyzed needs a graduated exposure intervention (one call first). Applying the wrong intervention makes the problem worse — telling a paralyzed rep to "just be more disciplined" accelerates anxiety without removing the fear driving inaction.

---

**P1 — Procrastination**

*Root cause:* Failure of daily self-discipline. The rep believes they can make up missed prospecting later ("I'll do a big block on Friday") but the cumulative effect of daily deferrals compounds into an empty pipeline.

*Key behavioral signals:*
- Prospecting is repeatedly deferred to a future date ("tomorrow," "Monday," "end of month")
- Work blocks exist but are consumed by non-prospecting tasks
- Activity patterns show 0–3 call days followed by one burst day (boom-bust)
- The rep can prospect when forced but avoids self-directed starts

*Self-assessment questions:*
- Did you tell yourself at least once this week that you would "catch up" on prospecting later?
- Is there always one more "important" task to clear before starting to dial?
- Do you believe a few heavy calling sessions can compensate for days of low activity?

*Diagnostic flag:* If the answer to two or more of the above is yes → Procrastination is your primary blocker.

*Core intervention:* You cannot eat the elephant in one bite. Daily minimum commitments — not weekly totals. One non-negotiable calling block of 30–60 minutes at the start of each day before any other task. No exceptions.

---

**P2 — Perfectionism**

*Root cause:* Using preparation as a proxy for prospecting. The rep substitutes the feeling of "getting ready" for the act of calling. Unlike procrastination (deferral), perfectionism produces the illusion of working while producing no prospecting outcomes.

*Key behavioral signals:*
- Calling blocks are consumed by research: Google, LinkedIn, CRM history, company website
- Scripts, lists, or tools must be "just right" before the first dial
- Call volume is extremely low (single digits) despite hours allocated to prospecting
- After each voicemail or rejection, additional preparation is done before the next call

*The Jeremy benchmark (p61–62):* Jeremy spent two hours arranging his desk, scripting, and researching each prospect individually — then made 7 calls in three hours, all to voicemail. Valarie next door ran a CRM list and started dialing immediately. One hour later: 53 calls, 14 decision-makers reached, 2 appointments set, 39 emails sent. Valarie earned approximately $100,000 more in annual commissions and ranked #1 in her division. The performance delta was not skill — it was action vs. preparation. See [references/jeremy-valarie-case.md](references/jeremy-valarie-case.md) for the full breakdown.

*Self-assessment questions:*
- Did you spend more than 15 minutes per prospect on research during your calling block this week?
- Did you reorganize your CRM, desk, or call list before making your first call?
- Have you told yourself "I just need to get the script right" before dialing?

*Diagnostic flag:* If the answer to two or more of the above is yes → Perfectionism is your primary blocker.

*Core intervention:* Cap research at 3 minutes per prospect maximum during calling hours. Research goes in protected time (before 8am or after 5pm) — never inside a calling block. Messy action beats perfect inaction: "Anything worth doing is worth doing poorly" — a targeted list dialed imperfectly produces more revenue than a perfect script never delivered.

---

**P3 — Paralysis from Analysis**

*Root cause:* Fear of rejection expressed as cognitive avoidance. The rep runs "what if" scenarios instead of dialing — "What if they say no?", "What if they say X?", "What should I do if…" — until the imagined scenarios generate enough anxiety to prevent action.

*Key behavioral signals:*
- Hours pass with zero calls despite the phone being in front of the rep
- The rep can articulate many reasons why calling "right now" is not optimal
- "What if" scenarios dominate pre-call thinking
- First call is often delayed to the point of the block ending without a dial

*Note — true job mismatch vs. paralysis:* If you physically cannot will yourself to dial at all and find the act of contacting strangers genuinely intolerable, this may be job-fit rather than analysis paralysis. Blount is direct about this: coaching cannot fix a fundamental mismatch between person and role. If that is your situation, this skill is not the tool you need.

*Self-assessment questions:*
- Did you spend time this week mentally rehearsing "worst case" call scenarios before dialing?
- Did you delay your first call of any day until you felt more "ready" — and then run out of time?
- Is your avoidance tied to a specific fear (rejection, embarrassment, not knowing how to respond)?

*Diagnostic flag:* If the answer to two or more of the above is yes → Paralysis from Analysis is your primary blocker.

*Core intervention:* One call first. Not a plan, not more preparation — a single dial. The purpose of the first call is not to get an appointment; it is to break the paralysis state. After the first call, the brain updates its threat model. Make the second call. Then the third. The anxiety dissipates with action, not with preparation. Graduated exposure: commit to a "one-call block" — a scheduled 5-minute window where the only goal is to complete one prospecting call.

---

### Step 4: Mental Toughness and Victim-Language Audit

**ACTION:** Review the user's self-description (the input document or their answers in this session) for victim-language markers. Then assess the four mental toughness pillars.

**WHY:** Victim-language is the most reliable leading indicator that the Three Ps will return even after tactical interventions. A rep can be coached past this week's procrastination — but if their default attribution pattern is external blame, the blocker will re-emerge next week. Mental toughness is the upstream capability that determines whether the interventions from Step 3 will hold. Diagnosing the weakest pillar guides the recovery prescription.

**Victim-language detection — scan the user's words for these patterns:**

| Pattern type | Example phrases | Signal |
|-------------|----------------|--------|
| External blame | "The leads are bad," "My territory is impossible," "Nobody buys in this economy" | Avoids ownership of prospecting activity |
| Helplessness framing | "Nothing works," "I've tried everything," "It's pointless" | Learned helplessness — often follows repeated rejection without coaching |
| Peer comparison as excuse | "Even the top reps aren't converting," "The whole team is struggling" | Using social proof to justify inaction |
| Manager blame | "They don't give us good tools," "My manager doesn't coach me" | Deflects from self-directed activity |

If two or more of these patterns appear in the user's self-description, flag victim-language as active and include a language-change prescription in the output plan.

**Four Pillars of Mental Toughness — rate each (Weak / Moderate / Strong):**

1. **Desire** — Can you answer clearly: What do you want? How will you get it? How badly do you want it? A rep without written goals has nothing to draw on when prospecting gets hard. If desire is weak, the intervention is goal-writing before any tactical changes.

2. **Mental Resilience** — Do you bounce back from rejection within the same calling block, or does a single harsh "no" shut down your activity for the rest of the day? Resilience is built through investment in self-development: 15 minutes of professional reading per day, audio programs during commute, coaching intake.

3. **Physical Resilience** — Sleep, exercise, and nutrition directly constrain mental toughness. Sleep deprivation specifically degrades the cognitive control needed to push past avoidance. If sleep is under 7 hours or exercise is absent, flag this as a contributor.

4. **Attitude** — Are you feeding your belief system or starving it? Inputs matter: the people you spend time with, what you read and watch, whether you practice gratitude or dwell on setbacks. "When your attitude loses altitude — you lose your winning edge."

---

### Step 5: Produce the Diagnosis Report and 1-Week Intervention Plan

**ACTION:** Write a structured output document — `call-reluctance-diagnosis.md` — that names the dominant failure mode, summarizes the evidence, and prescribes specific daily actions for the next 7 days.

**WHY:** A diagnosis without a plan produces insight without behavior change. The plan must be specific (named actions, named times) and keyed to the dominant failure mode identified in Step 3. Generic "prospect more" advice fails because it does not address the root cause. The written plan functions as a commitment device — ink on paper creates accountability that a verbal intention does not.

---

## Inputs

| Input | Required | Format |
|-------|----------|--------|
| 5-day activity data (calls planned vs. actual) | Yes | Numbers or estimates |
| Description of what happened instead of prospecting | Yes | Free text |
| Self-score on Seven Mindsets (Step 2) | Yes | 1–5 ratings |
| Three Ps self-assessment answers (Step 3) | Yes | Yes/No answers |
| User's own words describing their situation | Recommended | Verbatim — needed for victim-language scan |
| Mental toughness pillar self-rating (Step 4) | Recommended | Weak/Moderate/Strong |

---

## Outputs

Produce `call-reluctance-diagnosis.md` with the following sections:

```markdown
# Call Reluctance Diagnosis

**Date:** [Today's date]
**Diagnosis session covers:** [Date range of the behavior being reviewed]

---

## Activity Summary (Last 5 Days)

[5-day table from Step 1]

**Activity gap:** [Planned calls] planned vs [Actual calls] completed — [gap %] shortfall

---

## Seven Mindsets Baseline

[Scores table from Step 2]

**Lowest-rated dimensions:** [Names and scores of bottom 1–2]
**Interpretation:** [1–2 sentence read of what the pattern suggests]

---

## Primary Diagnosis: [Name the dominant P]

**Evidence:**
- [3–5 specific behavioral signals that confirm this as the primary blocker]

**Why this matters:**
- [1–2 sentences on the financial or pipeline cost if unaddressed]

---

## Victim-Language Findings

[Either: "No victim-language patterns detected" OR a list of flagged phrases and a brief note on what pattern they represent]

---

## Mental Toughness Pillar Assessment

| Pillar | Rating | Notes |
|--------|--------|-------|
| Desire | | |
| Mental Resilience | | |
| Physical Resilience | | |
| Attitude | | |

**Weakest pillar:** [Name] — [1 sentence on why this matters now]

---

## 1-Week Intervention Plan

[Specific daily actions, keyed to dominant failure mode. See examples below.]

**Day 1–2 (Foundation):** [Immediate structural change]
**Day 3–5 (Habit build):** [Daily practice with specific time/volume commitment]
**Day 6–7 (Audit):** [Review against activity data from Step 1 baseline]

---

## Self-Talk Scripts

[2–3 specific reframes for the most active negative self-talk pattern identified]
```

---

## Key Principles

- **The Three Ps are distinct failure modes, not synonyms.** Procrastination is a discipline failure. Perfectionism is action-substitution. Paralysis is fear-driven cognitive avoidance. They overlap but have different roots and different cures. Applying the wrong intervention to the wrong P produces frustration — and often reinforces the original blocker.

- **Messy action beats perfect inaction.** Valarie's 53 imperfect calls outperformed Jeremy's 7 researched calls by every metric that matters: contacts reached, appointments set, and annual commissions earned. The gap between them was not skill, product knowledge, or territory — it was the decision to act before conditions were perfect.

- **Victim language is a leading indicator, not a trailing one.** If a rep's natural language pattern assigns blame externally, tactical interventions will not hold. The belief that performance is controlled by external factors (leads, territory, economy) prevents the rep from taking the ownership actions that would actually change outcomes. Detecting and naming this pattern is as important as diagnosing the dominant P.

- **The three controllables in sales are: your actions, your reactions, and your mindset.** Everything else — prospect behavior, market conditions, product gaps — is outside your control. Losing is a choice. Mediocrity is a choice. This is not motivational language; it is a diagnostic frame. If a rep is not prospecting, it is because they have chosen a behavior that produces inaction. Naming that choice is the first step toward changing it.

- **Mental toughness can be developed — unlike talent, it is not fixed.** The formula is: change your mindset, change your game. The four pillars (Desire, Mental Resilience, Physical Resilience, Attitude) are all developable. The rep who builds them systematically outperforms the talented rep who does not over any sustained period.

---

## Examples

### Example 1: The Procrastinator ("I'll have a big Friday")

**Scenario:** An SDR reports that she made 12 calls this week total. She had four "prospecting days" planned. On each of those days, she spent the first 90 minutes on admin, email, and CRM cleanup, telling herself she would "get to calls in the afternoon." By afternoon, other things came up.

**Dominant P identified:** Procrastination — deferral pattern with boom-bust intent ("I'll make up for it Friday").

**1-Week Plan:**
- Daily non-negotiable: 30-minute calling block starting at 8:30am, before email is opened
- Target: 15 calls per day minimum, regardless of outcomes
- Remove admin from mornings entirely — move it to end of day
- Self-talk reframe: "I cannot prospect Monday's calls on Friday. Prospecting is like eating — it has to happen every day."
- Day 7 audit: compare 5-day call log vs. prior week baseline

---

### Example 2: The Perfectionist ("I just need to research one more thing")

**Scenario:** A BDR has been allocating two hours each morning to a "prospecting block." His average daily calls: 6. He describes his process: "I check LinkedIn for each prospect, look at the company website, review their recent news, check our CRM history, then think about what angle to use." He adds: "I don't want to go in blind."

**Dominant P identified:** Perfectionism — research-as-avoidance, classic Jeremy pattern.

**1-Week Plan:**
- Research budget: 3 minutes per prospect maximum. Set a timer.
- All research happens before 8am or after 5pm — never inside a calling block
- During calling hours: run the CRM list and dial in sequence. No pre-call research.
- Target: 30+ calls per 2-hour block (Valarie's benchmark: 53 calls + 39 emails in one hour)
- Self-talk reframe: "Imperfect information on a live call beats perfect information never delivered."
- Week review: track calls made vs. calls researched — if research time exceeds call time, the block was a research block, not a prospecting block

---

### Example 3: The Paralyzed Rep ("What if they hang up on me?")

**Scenario:** An AE doing self-directed outbound describes spending 45 minutes at his desk before making his first call on a Monday morning. He has written notes about "what to say if they ask about pricing," "what if their current vendor is cheaper," and "what if they already saw our email." He made 4 calls before deciding "it wasn't a good time to call."

**Dominant P identified:** Paralysis from Analysis — "what-if binge" pattern, decision-freeze from rejection anticipation.

**1-Week Plan:**
- One-call block: Schedule a 5-minute slot every morning at 9am with a single goal: complete one call. Just one. The outcome does not matter — the completion does.
- After the first call, immediately make a second. Then a third. Do not pause to debrief between calls.
- Ban pre-call scenario planning: notes, scripts, and objection prep happen the evening before, not in the calling block. Once the block starts, the only action is dialing.
- Self-talk reframe: "The call I have not made cannot go well. The call I make — even if it goes badly — gives me real data. I will learn more from one bad call than from one hour of imagining it."
- Graduated exposure target: Week 1 goal = 10 completed calls per day. Not answered calls. Not productive calls. Completed dials.

---

## References

- [references/seven-mindsets-rubric.md](references/seven-mindsets-rubric.md) — Full behavioral descriptions and scoring guidance for all 7 mindsets (Ch 2, p27–30)
- [references/jeremy-valarie-case.md](references/jeremy-valarie-case.md) — Full case study: Jeremy vs. Valarie, call counts, appointment outcomes, $100K commission delta (Ch 7, p61–62)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fanatical Prospecting by Jeb Blount.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
