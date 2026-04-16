---
name: prospecting-ratio-manager
description: Calculate pipeline ratios and diagnose prospecting health using the Three Laws of Prospecting — use this skill when the user asks about pipeline ratios, close rate math, activity math, sales numbers, the 30-day rule, pipeline slump, feast or famine cycle, how many dials they should make, how much prospecting they need to do, whether they are prospecting enough, quota math, pipeline health, why their pipeline is empty, or why they are in a slump — even if they do not use those exact words. Produces a ratio dashboard (green/yellow/red status per law), a concrete daily activity target, and a fillable daily-tracker worksheet.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/prospecting-ratio-manager
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting"
    authors: ["Jeb Blount"]
    chapters: [5, 6]
tags: [sales, prospecting, pipeline, ratios, metrics, sdr, bdr, sales-ops]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "User's activity counts (dials/connects/conversations/meetings/closed deals), close rate history, quota target, and current pipeline snapshot — provided as a CSV, markdown table, pasted numbers, or verbal description"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "CSV/markdown/spreadsheet directory, or user pastes numbers directly into the prompt"
discovery:
  goal: "Diagnose prospecting health against Three Laws (Need, 30-Day Rule, Replacement) and produce a daily activity target plus daily-tracker worksheet"
  tasks:
    - "Collect activity data and close rate from user"
    - "Calculate the pipeline replacement rate from close-rate math"
    - "Diagnose status against Universal Law of Need, 30-Day Rule, and Law of Replacement"
    - "Compute daily activity target using the E+E=P performance formula"
    - "Produce a ratio dashboard with green/yellow/red status and a daily-tracker worksheet"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner-to-intermediate
  triggers:
    - "pipeline ratios"
    - "close rate"
    - "activity math"
    - "sales numbers"
    - "30-day rule"
    - "pipeline slump"
    - "feast or famine"
    - "how many dials should I make"
    - "how much prospecting do I need"
    - "am I prospecting enough"
    - "quota math"
    - "pipeline health"
    - "my pipeline is empty"
    - "why am I in a slump"
  prerequisites: []
  not_for:
    - "Writing call scripts or email sequences (use prospecting-message-crafter)"
    - "Prioritizing which accounts to call (use prospect-list-tiering)"
    - "Planning time blocks for prospecting sessions (use prospecting-time-block-planner)"
    - "Building a multi-channel prospecting cadence (use balanced-prospecting-cadence-designer)"
  environment: "Any agent environment where the user can provide numerical activity data or a pipeline snapshot"
  quality:
    required_outputs: ["ratio-dashboard", "daily-activity-target", "daily-tracker-worksheet"]
    completeness: "Every law must have an explicit green/yellow/red status with the reasoning shown"
---

# Prospecting Ratio Manager

## When to Use

Your pipeline is empty, shrinking, or unpredictable — and you are not sure whether you have a prospecting volume problem, a consistency problem, or a math problem. Or you are hitting quota but want to know exactly how much prospecting activity is required to maintain that pace as close rates fluctuate.

This skill applies three universal laws from Jeb Blount's *Fanatical Prospecting* to your actual numbers: it tells you whether you are in danger of the Universal Law of Need (desperation territory), whether the 30-Day Rule predicts a future slump from past inactivity, and whether the Law of Replacement math means your pipeline is silently draining faster than you think. It then calculates a concrete daily activity target and produces a worksheet you can fill in every day to stay honest.

**Typical triggers:**
- You feel like you are prospecting "a lot" but quota keeps slipping
- You just closed a big month and want to know if you are safe
- Your pipeline has fewer than 10 live opportunities
- You had a slow December (or any holiday / vacation month) and it is now 60-90 days later
- You are a new SDR / BDR and need a baseline to work from

**This skill does NOT cover:**
- Writing the actual call scripts or email copy (use `prospecting-message-crafter`)
- Deciding which accounts to call first (use `prospect-list-tiering`)
- Building a time-blocked prospecting schedule (use `prospecting-time-block-planner`)

---

## Context and Input Gathering

### Required Context (must have — ask if missing)

**Activity counts (last 30 days):** How many dials, connects, conversations (two-way), meetings/appointments set, and closed deals did you produce?
  -> Check working directory for: `pipeline-ratios.csv`, `activity-tracker.csv`, `activity.md`, or any CSV with columns containing "dials," "connects," "meetings," "closed"
  -> If not found, ask: "Can you share your activity numbers for the past 30 days? I need: dials made, phone conversations (real two-way), meetings/appointments set, and deals closed. Even rough estimates work — I will flag where uncertainty affects the diagnosis."

**Close rate (%):** What percentage of qualified opportunities do you typically close?
  -> If the user does not know: use 10% as the default and flag it. A rep with an unknown close rate is already operating blind.
  -> If data file is present, calculate from: `Closed Won / Total Qualified Opportunities Entered`

**Quota target:** What is your monthly or quarterly closed-revenue or closed-deal count target?
  -> If quota is revenue-based, also ask for average deal value so you can translate to deal count.

**Current pipeline size:** How many live, qualified opportunities are currently in your pipeline?
  -> If unknown: flag the data gap and proceed with what is available.

### Observable Context (gather from environment)

- CRM export or activity log files: parse for dials, connects, meetings, closed. Column name variations to check: `Calls Made`, `Outbound Dials`, `Conversations`, `Meetings Booked`, `Demos Set`, `Closed Won`, `Opp Created Date`
- Pipeline snapshot file: parse for count of open opportunities and their ages

### Default Assumptions

| Input | Default if unknown | Flag? |
|-------|-------------------|-------|
| Close rate | 10% | Yes — note it changes targets significantly |
| Working days per month | 21 | No |
| Daily dial capacity | 50 | Note as benchmark |
| Pipeline size | Unknown | Yes — Law of Replacement diagnosis will be partial |

### Sufficiency Threshold

```
SUFFICIENT when:
- At least one of: (a) 30-day activity counts, OR (b) close rate + quota target
- Quota target known (even rough)

NOT sufficient — ask before proceeding:
- No numbers whatsoever AND no files found
  -> Ask: "I need a few numbers to run the diagnosis. What's your monthly quota (as deal count or revenue), your rough close rate, and how many calls or outreach touches you made in the last 30 days?"
```

---

## Process

### Step 1: Collect and normalize activity data

Read any available file. Parse into a standard activity table:

| Metric | Last 30 Days | Notes |
|--------|-------------|-------|
| Dials made | — | Phone outbound attempts |
| Live conversations | — | Two-way exchanges (phone/video) |
| Meetings / appointments set | — | Qualified discovery or demo calls booked |
| Deals closed (won) | — | Closed-won count |
| New prospects added to pipeline | — | Net new opportunities created |
| Current pipeline size | — | Total live, qualified opportunities |

If the user provides raw numbers verbally, structure them into this table before proceeding.

**Why:** Unstructured gut feelings ("I made a lot of calls") are the primary source of self-delusion about prospecting activity. Jeb Blount's "rep who thought he made 50 calls but actually made 12" case is the canonical example. Structuring the numbers before diagnosis prevents the same error.

---

### Step 2: Calculate the pipeline replacement rate

Using the close rate, derive how many new prospects must be added to the pipeline for every deal closed.

**Formula:**

```
Replacement Rate = 1 / Close Rate (as decimal)

Example: Close rate = 10% (0.10)
Replacement Rate = 1 / 0.10 = 10

Interpretation: Every time you close 1 deal, you must add 10 new
prospects to maintain pipeline size — because statistically the other
9 prospects in that cohort will not close.
```

Calculate:
- **Minimum weekly adds** to sustain current pipeline: `(Monthly Closes Target × Replacement Rate) / 4.3`
- **Pipeline floor** (minimum viable live opportunities): `Monthly Closes Target × Replacement Rate`

**Why:** Most salespeople believe closing a deal shrinks the pipeline by 1. The Law of Replacement says it shrinks by the full cohort (at 10% close rate: by 10). This is the mathematical root cause of the feast-or-famine cycle. Without this calculation, a rep who closes 3 deals in a great week and adds 3 new prospects thinks they are even — they are actually 27 prospects underwater.

---

### Step 3: Diagnose against the Three Laws

Evaluate the user's data against each law. Assign a status (green / yellow / red) with explicit criteria.

#### Law 1 — Universal Law of Need

> The more you need a sale, the less likely you are to get it. Desperation magnifies and accelerates failure.

**Diagnosis inputs:** Current pipeline size vs. pipeline floor.

| Status | Condition | Meaning |
|--------|-----------|---------|
| 🟢 Green | Pipeline ≥ 2× pipeline floor | Healthy. You have optionality. No desperation pressure. |
| 🟡 Yellow | Pipeline is 1×–2× pipeline floor | Caution. One bad week removes your cushion. |
| 🔴 Red | Pipeline < pipeline floor | Universal Law of Need is active. Desperation signals are present or imminent. |

**Why this matters:** Red status means you are mathematically forced to close deals you cannot afford to lose. Prospects can sense that pressure. The fix is not better closing technique — it is rebuilding the pipeline volume.

#### Law 2 — 30-Day Rule (activity-to-pipeline lag effect)

> Prospecting done in any 30-day window pays off in the next 90 days. A prospecting gap now bites you 90 days later.

**Diagnosis inputs:** Monthly new prospects added (Step 1) vs. minimum monthly adds (Step 2).

Calculate a **prospecting coverage ratio:**
```
Coverage Ratio = New Prospects Added (Last 30 Days) / Minimum Monthly Adds Required
```

| Status | Coverage Ratio | Meaning |
|--------|---------------|---------|
| 🟢 Green | ≥ 1.2 | Prospecting is ahead of pace. 90-day outlook is healthy. |
| 🟡 Yellow | 0.8–1.19 | Roughly on pace. Minor gaps will appear in ~60-90 days. |
| 🔴 Red | < 0.8 | Prospecting deficit. Expect a pipeline slump in 60-90 days if not corrected now. |

If the user is currently in a slump: ask what their prospecting activity looked like 60-90 days ago. A December holiday gap causing a March slump is the Greg pattern — misdiagnosed as a closing problem, actually a lag effect from stopped prospecting.

**Why this matters:** The 30-Day Rule creates a dangerous illusion — prospecting gaps feel painless in the moment (you are busy closing) but manifest 90 days later when the pipeline is already empty and recovery takes another 30 days of daily prospecting. By then, the hole is 4 months deep.

#### Law 3 — Law of Replacement

> When you close 1 deal, you must replace the whole closing cohort — not just 1 prospect.

**Diagnosis inputs:** New prospects added (Step 1) vs. deals closed × replacement rate.

```
Replacement Deficit = (Deals Closed × Replacement Rate) - New Prospects Added

If Replacement Deficit > 0: pipeline is shrinking even if it looks "full"
```

| Status | Condition | Meaning |
|--------|-----------|---------|
| 🟢 Green | Replacement Deficit ≤ 0 | Pipeline is being replenished at or above close rate. |
| 🟡 Yellow | Deficit = 1–5 prospects | Minor lag. Catch up this week. |
| 🔴 Red | Deficit > 5 prospects | Pipeline is draining. Prospecting intensity must increase immediately. |

**Why this matters:** This is the most common invisible leak. A rep who closed 5 deals last month and added 5 new prospects thinks they are even. At 10% close rate, they are actually 45 prospects behind. The pipeline will look healthy for another 30 days, then collapse.

---

### Step 4: Calculate daily activity target

Using the quota target and close rate, work backward to a required daily activity level.

**Formula chain:**

```
Monthly Closes Needed         = Quota Target / Average Deal Value  (if revenue-based)
Monthly New Prospects Needed  = Monthly Closes Needed / Close Rate
Weekly New Prospects Needed   = Monthly New Prospects Needed / 4.3
Daily New Prospects Needed    = Weekly / 5

Conversations Needed per Day  = Daily New Prospects Needed / Meeting-Set Rate
  (use Meeting-Set Rate from Step 1 data: Meetings Set / Conversations)
  (default if unknown: 1 meeting per 5-10 conversations = 10-20% set rate)

Dials Needed per Day          = Conversations Needed / Connect Rate
  (use Connect Rate from Step 1: Conversations / Dials)
  (default if unknown: 1 conversation per 7-10 dials = 10-14% connect rate)
```

**Hourly worth check (optional but valuable):**
```
Worth per Hour = Annual Income Goal / (Working Weeks × Golden Hours per Week)
Default: $75,000 goal / (48 weeks × 30 hours/week) = $52/hour

Use this to evaluate whether non-prospecting tasks should be deferred or delegated.
```

**Why:** Without a number, "prospect more" is not an actionable directive. The daily dial target is what converts a diagnosis into a behavior. The backward calculation from quota ensures the target is anchored to revenue reality, not arbitrary benchmarks.

---

### Step 5: Produce the ratio dashboard and daily tracker

**Output 1: Ratio Dashboard** (`ratio-dashboard.md`)

```
=== PROSPECTING RATIO DASHBOARD ===
Generated: [Date]

INPUTS USED
-----------
Close Rate:             [X]%
Monthly Quota Target:   [N] deals (or $X at $Y avg deal)
30-Day Activity Data:   [provided / estimated]

KEY RATIOS
----------
Pipeline Replacement Rate:    [X] prospects per close
Pipeline Floor (minimum):     [N] live opportunities
Coverage Ratio (30-Day):      [X.X] ([Green/Yellow/Red])

THREE-LAW STATUS
----------------
Universal Law of Need:    [🟢/🟡/🔴] — Pipeline: [N] / Floor: [N]
30-Day Rule:              [🟢/🟡/🔴] — Coverage: [X.X] — [interpretation]
Law of Replacement:       [🟢/🟡/🔴] — Deficit: [N] prospects

DAILY ACTIVITY TARGET
---------------------
Deals to close per month:         [N]
New prospects needed per month:   [N]
Daily new prospects needed:       [N]
Conversations needed per day:     [N]  (at [X]% set rate)
Dials needed per day:             [N]  (at [X]% connect rate)

DIAGNOSIS SUMMARY
-----------------
[Narrative: Which laws are active, what caused it, what to do first]
```

**Output 2: Daily Tracker Worksheet** (`daily-tracker.md`)

```
=== DAILY PROSPECTING TRACKER ===
Rep: _______________    Date: _______________

DAILY TARGETS (from ratio dashboard)
  Dials:            [target]  |  Actual: _____
  Conversations:    [target]  |  Actual: _____
  Meetings Set:     [target]  |  Actual: _____
  New Prospects:    [target]  |  Actual: _____

PIPELINE STATUS
  Current Pipeline Size:      _____
  New Prospects Added Today:  _____
  Deals Closed Today:         _____
  Running Replacement Deficit: _____

LAW OF NEED CHECK  (circle one)
  Pipeline vs Floor:   ABOVE   /   AT   /   BELOW

NOTES / BLOCKERS
___________________________________________________

END-OF-DAY SELF-CHECK
  [ ] Did I hit my dial target?
  [ ] Did I add at least [N] new prospects today?
  [ ] Is my replacement deficit ≤ 0 for the week?
  [ ] If below floor: am I prospecting FIRST tomorrow, before anything else?
```

**Why:** Externalized tracking prevents the self-delusion problem. Blount's rep who "felt like" he made 50 calls but actually made 12 had no tracking sheet. The daily worksheet creates accountability by forcing a visual reckoning with the numbers at end of day, not at end of quarter when recovery options have narrowed.

---

## Inputs

| Input | Required | Format | Notes |
|-------|----------|--------|-------|
| 30-day activity counts | Recommended | CSV, markdown table, or pasted numbers | Dials, conversations, meetings, closes, new prospects added |
| Close rate | Recommended | Percentage or decimal | Default 10% if unknown |
| Monthly quota target | Required | Deal count or revenue | Revenue → also need avg deal value |
| Current pipeline size | Recommended | Integer | Needed for Law of Need diagnosis |

---

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `ratio-dashboard.md` | Markdown | Three-law status (green/yellow/red), key ratios, daily activity target, diagnosis narrative |
| `daily-tracker.md` | Markdown | Fillable daily worksheet with targets populated from dashboard |

---

## Key Principles

**The pipeline replacement rate is the most underused number in sales.** Every rep knows their close rate but almost none do the math on what that close rate means for required daily activity. A 10% close rate does not mean 10% of your time prospecting — it means for every deal you close, you must find 10 new qualified prospects.

**The 30-Day Rule makes slumps invisible until they are severe.** The gap and the pain are separated by 60-90 days. By the time you feel the slump, the prospecting failure that caused it was 3 months ago. The only protection is daily tracking and weekly coverage ratio checks.

**Consistency beats intensity.** One week of 200 dials followed by three weeks of none does not average out. The 30-Day Rule requires steady input across the full window — the payoff comes from consistency, not bursts.

**Desperation is a symptom of a math failure, not a mindset failure.** When the Universal Law of Need is active, no closing technique will fix it. The fix is pipeline volume. Applying closing pressure when you are red on the Law of Need makes the problem worse by signaling desperation to prospects.

**Tracking must be visual and manual.** Relying on CRM auto-logging creates a false sense of productivity. Manual counting — even tick marks on a sheet — keeps you grounded in what actually happened today.

---

## Examples

### Example 1 — Jerry's end-of-quarter collapse (Universal Law of Need + Replacement)

**Situation:** SDR, mid-October. Had a strong August. Stopped prospecting heavily in September to service newly closed accounts. Now has 4 live opportunities, needs 2 closes by end of quarter. Close rate: 10%. Monthly quota: 3 deals.

**Data provided:**
- Dials last 30 days: 120 (well below their usual 300)
- New prospects added: 2
- Deals closed last 30 days: 3
- Current pipeline: 4 opportunities

**Diagnosis:**
- Pipeline floor: 3 closes needed × 10 = 30 minimum live opportunities
- Current pipeline: 4 — **Law of Need is Red**
- Replacement deficit: (3 closes × 10) − 2 added = **28 prospects underwater**
- Law of Replacement: **Red**
- Coverage ratio: 2 added / 30 needed = 0.07 — **30-Day Rule: Red**

**Dashboard output:** All three laws red. Diagnosis: Jerry did not prospect during his September close cycle. He is now 28 prospects underwater with only 4 live deals and needs 2 closes from that pool. Desperation signals are mathematically inevitable. The fix is not closing technique — it is 4-6 weeks of aggressive daily prospecting to rebuild the floor.

**Daily target:** 30 new prospects needed per month → 7 per week → 1.4 per day. At 10% meeting-set rate: 14 conversations/day. At 14% connect rate: 100 dials/day.

---

### Example 2 — Sandra's steady-state check (all laws green)

**Situation:** AE, wants to verify she is on track for Q3. Uses the skill as a monthly sanity check. Close rate: 20%. Monthly quota: 5 deals. Average deal value: $12,000.

**Data provided:**
- Dials last 30 days: 650
- New prospects added: 35
- Deals closed: 5
- Current pipeline: 38 opportunities

**Diagnosis:**
- Replacement rate: 1 / 0.20 = 5
- Pipeline floor: 5 × 5 = 25 minimum
- Current pipeline: 38 — **Law of Need: Green** (38 / 25 = 1.52×)
- Monthly adds needed: 5 × 5 = 25. Added: 35. Coverage ratio: 1.4 — **30-Day Rule: Green**
- Replacement deficit: (5 closes × 5) − 35 = −10 (surplus) — **Law of Replacement: Green**

**Dashboard output:** All three laws green. Sandra has a 10-prospect surplus, pipeline 52% above the floor, and prospecting pace 40% ahead of minimum. No action required except maintaining the current pace.

---

### Example 3 — Greg's mid-quarter course correction (30-Day Rule lag)

**Situation:** Sales rep, early March. December was slow (holiday breaks). January and February were busy with admin and onboarding new Q4 clients. Now nothing is closing. Rep thinks he has a closing problem.

**Data provided:**
- Deals closed in March so far: 0
- Meetings happening in March: 2 (both pushing to Q2)
- New prospects added last 30 days: 8
- Last full prospecting month: November (estimated 45 new prospects added)
- Close rate: 15%. Monthly quota: 3 deals.

**Diagnosis:**
- Replacement rate: 1 / 0.15 = 6.7 (round to 7)
- Monthly adds needed: 3 × 7 = 21. Added in Feb: ~8. Coverage ratio: 0.38 — **30-Day Rule: Red**
- Root cause diagnosis: December and January prospecting gaps are hitting in March. This is a prospecting problem, not a closing problem. The March stalls are prospects that were marginally viable — the cohort is stale. Calling them again for closing techniques will not help.
- Law of Need: pipeline details not provided — flag as partial diagnosis.

**Recommended action:** Stop calling the same 8 prospects. Start 30 days of daily prospecting from today. Expect the payoff in late April / May. Quota for March is likely unrecoverable — focus energy on April-May recovery.

---

## References

Full ratio-math proofs and worked examples with variable close rates (5%, 10%, 15%, 20%, 25%): see `references/ratio-math-reference.md`

Slump anatomy and recovery checklist (9-step sequence): see `references/slump-anatomy-and-recovery.md`

Source chapters: Blount, Jeb. *Fanatical Prospecting.* Wiley, 2015.
- Chapter 5: "The More You Prospect, the Luckier You Get" (pp. 43–53)
- Chapter 6: "Know Your Numbers: Managing Your Ratios" (pp. 54–58)

---

## Related BookForge Skills

- **prospecting-time-block-planner** — Once you have your daily dial target, use this skill to schedule protected prospecting blocks (Golden Hours) in your calendar.
- **balanced-prospecting-cadence-designer** — Design a multi-channel (phone, email, LinkedIn, text) cadence that reaches your daily new-prospect target across channels.
- **prospect-list-tiering** — Ensure the prospects you are adding to refill your pipeline are tiered by qualification state so you work the highest-probability accounts first.
- **call-reluctance-diagnostic** — If you know your targets but are not hitting them, use this skill to diagnose which of the Three Ps (procrastination, perfectionism, paralysis) is blocking activity.

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills. Source framework: *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). Chapters 5–6.
