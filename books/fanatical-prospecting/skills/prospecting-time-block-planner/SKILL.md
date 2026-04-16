---
name: prospecting-time-block-planner
description: |
  Build a protected weekly prospecting calendar that separates Golden Hours (when buyers are buying) from Platinum Hours (before/after business hours for research and admin), calculates what each Golden Hour is worth in dollars, and installs a Power Hour protocol that eliminates distractions during focused dial blocks. Use this skill when someone asks "time management for sales", "when should I prospect", "golden hours", "power hour", "prospecting block", "calendar for sales", "how to protect prospecting time", "distractions killing my sales", "time equalizer", "platinum hours", "morning vs afternoon prospecting", "what time should I make cold calls", "how do I structure my sales day", "schedule for SDR", "how to stop email from killing my prospecting", "how to make more calls in less time", "why am I not hitting my dial targets", "how to concentrate my prospecting power", "hourly worth formula", or "sales time allocation framework". This skill gathers the rep's annual quota goal, working hours, current calendar constraints, and top distractors — then produces four artifacts: (1) hourly-worth calculation showing the dollar cost of every non-selling minute during prime time, (2) a Golden Hours and Platinum Hours weekly allocation tuned to the rep's territory and prospect time zones, (3) a 6-rule Power Hour protocol with a named distraction-elimination checklist, and (4) a ready-to-use weekly time-block calendar template. Based on Chapter 8 of Fanatical Prospecting by Jeb Blount.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/prospecting-time-block-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
depends-on: []
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting: The Ultimate Guide to Opening Sales Conversations and Filling the Pipeline by Leveraging Social Selling, Telephone, Email, Text, and Cold Calling"
    authors: ["Jeb Blount"]
    chapters: [8]
tags: [sales, prospecting, time-management, productivity, calendar, sdr, bdr, inside-sales, outside-sales, power-hour, golden-hours, distraction-elimination]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Rep's annual quota or income goal, working weeks per year, available selling hours per day, current calendar commitments, prospect time zones, and top 3–5 distractions that interrupt their prospecting blocks"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document/calendar text directory — reads user situation brief; writes prospecting-time-block-plan-{date}.md to the working directory"
discovery:
  goal: "Calculate the dollar value of each Golden Hour, allocate prime selling time to protected prospecting blocks, and deliver a weekly calendar template with a Power Hour distraction-elimination protocol"
  tasks:
    - "Gather quota goal, working hours, calendar constraints, and distraction inventory from the rep"
    - "Calculate hourly worth using the Annual Goal ÷ Working Weeks ÷ Golden Hours formula"
    - "Identify Golden Hours based on prospect availability window for the rep's territory and time zone"
    - "Assign Platinum Hours (before/after Golden Hours) for research, CRM, proposals, and admin"
    - "Design the Power Hour protocol with specific distraction-elimination rules"
    - "Write a weekly time-block calendar template as the primary output artifact"
  audience:
    roles: [sdr, bdr, ae, inside-sales-rep, outside-sales-rep, founder-self-seller]
    experience: beginner-to-intermediate
  triggers:
    - "Rep is not hitting dial or touch targets despite feeling busy all day"
    - "Rep is spending Golden Hours on admin, CRM, or email instead of prospecting"
    - "Rep wants to know exactly when to prospect vs. when to do everything else"
    - "Rep is setting up a new weekly routine after a quota change or territory reassignment"
    - "Manager is implementing a time-blocking discipline across the team"
  prerequisites: []
  not_for:
    - "Calculating how many total dials or touches are needed to hit quota — use fanatical-prospecting:pipeline-ratio-calculator"
    - "Writing the actual call script for the prospecting block — use fanatical-prospecting:cold-call-opener-builder"
    - "Prioritizing which prospects to call during the block — use fanatical-prospecting:prospect-prioritization-pyramid"
    - "Setting the objective for each prospecting touch — use fanatical-prospecting:prospecting-objective-setter"
  environment: "Document set — reads situation brief from working directory or user input; writes weekly time-block calendar plan"
  quality: placeholder
---

# Prospecting Time Block Planner

## When to Use

You are feeling busy every day but not hitting your prospecting targets. Or you are setting up your week and want to know exactly when to make calls, when to do research, and when to handle email and CRM — and you want that structure to be protected from interruptions.

This skill applies the Golden Hours / Platinum Hours framework from Jeb Blount's Chapter 8 to your specific quota, calendar, and time zone. It calculates what each selling hour is worth in dollars, builds a protected weekly calendar, and installs a Power Hour protocol that eliminates the distractions that are costing you commission.

**Who this skill is for:** SDRs, BDRs, inside sales reps, outside sales reps, and founder-sellers who run outbound prospecting as part of their daily work. Especially valuable for reps who are "always busy" but whose activity numbers are not matching their intentions, and for reps who check email first thing every morning.

**Output:** `prospecting-time-block-plan-{date}.md` — hourly-worth calculation, Golden/Platinum Hours allocation, Power Hour distraction protocol, and a weekly calendar template.

---

## Context & Input Gathering

### Required

To build the calendar accurately, the skill needs:

1. **Annual income goal:** Your quota or on-target earnings for the year (e.g., "$120,000").
2. **Working weeks per year:** How many weeks you are actually selling — subtract vacation, holidays, and expected sick days. Most reps land between 46 and 50 weeks.
3. **Selling hours per day:** How many hours per day are genuinely available for sales activity — not counting lunch, commute, and mandatory non-sales meetings. Typical range is 5–7 hours.
4. **Prospect time zone window:** When are your prospects reachable? A B2B rep in EST calling West Coast companies has a different Golden Hours window than a rep in PST calling the East Coast. If prospects span multiple time zones, note the overlap window.
5. **Current calendar commitments:** Recurring meetings, mandatory team calls, commute blocks, or fixed client commitments that cannot move.
6. **Top 3–5 distractions:** What actually interrupts your prospecting? Email notifications, Slack, mobile phone, colleagues stopping by, CRM rabbit holes, or social media are the most common.

### Useful (read from working directory if available)

- **`pipeline-ratios.csv`** — activity-to-outcome conversion rates (dials per connect, connects per meeting) help size how many Power Hour blocks are needed
- **`prospect-list.csv`** — if prospect geography spans multiple time zones, this calibrates the Golden Hours window

### Defaults

If no documents are provided, the skill asks for the six inputs above in plain conversation. A sentence or two per item is enough to begin. If the rep is uncertain about working weeks or selling hours, the skill applies standard defaults (48 working weeks, 6 selling hours per day) and flags them for adjustment.

---

## Process

### Step 1: Calculate Hourly Worth

**Action:** Apply the hourly-worth formula to the rep's annual income goal:

```
Annual Income Goal
÷ Working Weeks per Year
÷ Golden Hours per Week
= Your Hourly Worth ($)
```

**Example calculation:** Rep with a $75,000 annual goal.
- Working weeks: 48 (52 weeks minus 2 weeks vacation, 1 week holidays, 1 week miscellaneous)
- Selling hours per day: 6 (8-hour day minus 1-hour lunch and 1-hour non-sales overhead)
- Golden Hours per week: 30 (6 hours × 5 days)
- $75,000 ÷ 48 = $1,563/week ÷ 30 = **$52 per Golden Hour**

Once this number is calculated, apply it immediately: if the rep spends 90 minutes on email and CRM during Golden Hours, that is $78 of commission revenue traded for inbox management.

**WHY:** Most reps have never done this math. The abstract idea that "time is money" produces no behavioral change. A specific dollar figure — "$52 per hour" — does. When the rep knows that checking Slack during their morning prospecting block costs $13 in real commission, the distraction has a price tag. This is what converts the CEO mindset from a motivational phrase into an active decision-making tool throughout the day.

**Output:** A single line: "Your Golden Hours are worth **$[X] per hour**."

---

### Step 2: Identify Golden Hours

**Action:** Map the rep's territory against their own working day to identify the window during which buyers are reliably reachable and making purchasing decisions.

**Golden Hours definition:** Business hours in the prospect's time zone — the window when decision makers are at their desks, answering phones, and taking meetings. Typically 8 AM–5 PM in the prospect's local time.

**Time zone calibration:**
- Rep in EST, prospects in EST: Golden Hours are 8 AM–5 PM local (standard)
- Rep in EST, prospects in PST: Golden Hours shift to 11 AM–8 PM EST (afternoon-heavy)
- Rep in PST, prospects in EST: Golden Hours shift to 8 AM–2 PM PST (morning-heavy)
- Prospects spanning both coasts: 11 AM–2 PM EST / 8 AM–11 AM PST is the reliable overlap window; extend outward from there

**Inside sales note:** Golden Hours are your most protected dial blocks. Outside sales reps add in-person visit windows that should align with the prospect's availability, not drive-time convenience.

**Block the calendar:** Mark Golden Hours as non-negotiable prospecting and selling time. Nothing — email, CRM updates, proposals, colleague requests — happens in these blocks unless it is directly revenue-generating.

**WHY:** The single biggest cause of missed dial targets is not laziness — it is Golden Hours contamination. Non-selling activities feel important and they often are. But proposals, CRM entry, and email management are support functions, not selling functions. Doing them during the window when buyers are available is trading your highest-value hours for your lowest-value tasks. Reps who protect Golden Hours with the same discipline they would apply to a hot prospect meeting consistently outperform those who do not.

**Output:** A labeled time window: "Golden Hours: [START TIME]–[END TIME] [TIME ZONE], Monday–Friday."

---

### Step 3: Assign Platinum Hours

**Action:** Allocate time blocks before and after the Golden Hours window for all non-selling activities that are necessary but should not happen during prime prospecting time.

**Platinum Hours definition:** The 1–2 hours before the Golden Hours window opens (early morning) and the 1–2 hours after it closes (late afternoon or evening). This is when top-earning reps handle:

- Building and updating prospecting lists
- Pre-call research and call objective planning
- Proposal and presentation development
- Contract preparation and approvals
- Social selling activity (LinkedIn connection requests, content engagement)
- Email prospecting (composing outbound sequences, reading and responding to replies)
- CRM data entry and updates
- Reports and administrative tasks
- Calendar management

**The morning Platinum Hour rule:** Do not check email first thing in the morning. Email is "the derailer of all derailers" — opening it before your first prospecting block puts you at the mercy of other people's priorities before you have completed your most important task of the day. Reserve the first morning Platinum Hour for list preparation and pre-call planning; handle email in a scheduled block after your first Power Hour, or in the afternoon Platinum Hours.

**WHY:** Platinum Hours exist to make Golden Hours frictionless. When call lists are prepared, research is done, and objectives are set before the dial block begins, the rep can focus entirely on the call — no context-switching, no stopping mid-block to look up a contact. The preparation done in Platinum Hours directly multiplies the output of the Golden Hours that follow.

**Output:** Labeled morning and afternoon Platinum Hours blocks on the weekly calendar.

---

### Step 4: Design the Power Hour Protocol

**Action:** Install focused dial blocks inside the Golden Hours window. These are the Power Hours — 30–60 minute windows dedicated entirely to a single prospecting activity.

**Power Hour rules (the 6-rule protocol):**

1. **One activity only.** During a phone Power Hour, dial the phone. During an email Power Hour, write and send emails. Do not mix activity types within a single block.
2. **Email off.** Close the email application entirely. Do not have it visible on screen. This is not "I'll just glance at it" — it is closed.
3. **Mobile device in a drawer (or another room).** The average person looks at their phone every 7 minutes. A phone on the desk is a distraction machine even when silent. Physical distance is required.
4. **No CRM research during the block.** All research was completed in Platinum Hours before the block started. During the Power Hour, the rep works from a prepared list with notes already in place.
5. **Notes on paper during the block; log to CRM after.** Take brief notes on a printed list or notepad during calls. Log everything in CRM in a dedicated 20–30 minute block immediately after the Power Hour ends.
6. **Hold interruptions at the door.** Post a visible "Do Not Disturb" signal — a door sign, a status indicator in Slack, or headphones on. Inform colleagues and managers in advance that this time is a protected block.

**Block structure:** Schedule 3 Power Hours spread across the Golden Hours day — one in the morning window, one midday, one in the afternoon. A rep making 25–50 teleprospecting calls per Power Hour will complete their daily dial target in 1–2 hours of protected time.

**WHY:** Multitasking is not possible during prospecting. The human brain does not actually run tasks in parallel — it switches rapidly between tasks, creating the illusion of multitasking while accumulating switching overhead. A rep who interrupts calls to log CRM notes, check Slack, and research the next prospect makes roughly one call every 8 minutes. The same rep in a concentrated Power Hour makes 8–10 calls in that same time. This is Horstman's Corollary: work contracts to fill the time available. A 60-minute block with no exit routes forces the rep to move faster and stay focused. Eighty percent of all the appointments a rep needs can be set in 1–2 concentrated hours per day when those hours are properly blocked.

**Output:** A labeled Power Hour protocol embedded in the weekly calendar, with 6 rules printed at the top.

---

### Step 5: Build the Distraction-Elimination Plan

**Action:** Using the rep's self-reported distraction inventory (gathered in Context & Input Gathering), produce a specific countermeasure for each distractor.

**Common distractors and their countermeasures:**

| Distractor | Countermeasure |
|---|---|
| Email notifications | Close email application during Power Hours; schedule 2–3 email blocks per day in Platinum Hours |
| Mobile phone (texts, social, apps) | Phone in desk drawer or a different room; enable Do Not Disturb mode on device during blocks |
| Slack / team chat | Set status to "In a prospecting block — DM me after [TIME]"; close or silence Slack |
| Social media (LinkedIn, X, Facebook) | Block these sites at the browser level during Power Hours using a browser extension or system-level restriction |
| CRM rabbit holes | Complete all prospect research in the pre-block Platinum Hour; commit to "no CRM during calls" as a team norm |
| Colleague drop-ins | Post a physical "Do Not Disturb" sign or schedule the Power Hour in a meeting room |
| Internal meetings | Audit recurring meetings that fall in Golden Hours; request reschedules to Platinum Hours or off-peak windows |

**The email opening rule:** Never check email first thing in the morning before completing the first prospecting block. This is the single highest-leverage rule for protecting morning Golden Hours. If something is genuinely urgent, the sender will call or text — not just send an email.

**WHY:** Each interruption does not just cost the time of the interruption itself. Research on attention recovery shows that returning to deep focus after an interruption takes additional minutes beyond the distraction itself. In Laura's case study from the book, she lost 7 minutes per interruption — not from the interruption alone but from re-orienting, finding her place on the list, and rebuilding mental momentum. Eleven interruptions in a two-hour block cost her far more than 11 × 7 = 77 minutes; they degraded the quality of every call between interruptions as well.

**Output:** A named distraction elimination plan embedded in the weekly calendar artifact, mapped to the rep's specific distractors.

---

## Output Template

```markdown
# Prospecting Time Block Plan
**Date:** [Date]
**Rep:** [Name]
**Prepared by:** fanatical-prospecting:prospecting-time-block-planner

---

## Hourly Worth Calculation

| Input | Value |
|---|---|
| Annual income goal | $[GOAL] |
| Working weeks per year | [WEEKS] |
| Golden Hours per week | [HOURS/DAY × 5] |
| **Your hourly worth** | **$[RESULT]** |

> Every minute you spend on email, CRM entry, or admin during your Golden Hours costs you $[RESULT ÷ 60] in commission. A 30-minute email session during prime selling time costs $[RESULT ÷ 2].

---

## Golden Hours

**Window:** [START TIME] – [END TIME] [TIME ZONE]
**Prospect time zone(s):** [ZONES]
**Days:** Monday – Friday

These hours are your prime selling window. Only revenue-generating activities happen here:
- Outbound prospecting calls (Power Hours)
- Inbound lead follow-up
- Discovery calls and qualification conversations
- Demos, presentations, and closing calls

Non-selling tasks do not belong here — no matter how important they feel.

---

## Platinum Hours

**Morning Platinum Block:** [START TIME] – [END TIME]
**Afternoon Platinum Block:** [START TIME] – [END TIME]

Activities for Platinum Hours:
- [ ] Build and update call lists for today's Power Hours
- [ ] Pre-call research and call objective planning
- [ ] CRM data entry from previous day's blocks
- [ ] Email prospecting (composing sequences, reading replies)
- [ ] Proposals, contracts, and approvals
- [ ] Social selling (LinkedIn connection requests, content engagement)
- [ ] Reports and administrative tasks
- [ ] Calendar management

> **Morning rule:** Do not open email until after your first Power Hour. Your inbox is other people's priorities. Prospect first — then manage inbound.

---

## Weekly Time Block Calendar

| Time | Monday | Tuesday | Wednesday | Thursday | Friday |
|---|---|---|---|---|---|
| [MORNING PLATINUM START]–[END] | Platinum: List prep + research | Platinum: List prep + research | Platinum: List prep + research | Platinum: List prep + research | Platinum: List prep + research |
| [POWER HOUR 1 START]–[END] | **POWER HOUR 1: Dial block** | **POWER HOUR 1: Dial block** | **POWER HOUR 1: Dial block** | **POWER HOUR 1: Dial block** | **POWER HOUR 1: Dial block** |
| [CRM LOG 1 START]–[END] | CRM log + notes | CRM log + notes | CRM log + notes | CRM log + notes | CRM log + notes |
| [EMAIL BLOCK START]–[END] | Email batch | Email batch | Email batch | Email batch | Email batch |
| [POWER HOUR 2 START]–[END] | **POWER HOUR 2: Dial block** | **POWER HOUR 2: Dial block** | **POWER HOUR 2: Dial block** | **POWER HOUR 2: Dial block** | **POWER HOUR 2: Dial block** |
| [MIDDAY]–[END] | Discovery / demo / lunch | Discovery / demo / lunch | Discovery / demo / lunch | Discovery / demo / lunch | Discovery / demo / lunch |
| [POWER HOUR 3 START]–[END] | **POWER HOUR 3: Dial block** | **POWER HOUR 3: Dial block** | **POWER HOUR 3: Dial block** | **POWER HOUR 3: Dial block** | **POWER HOUR 3: Dial block** |
| [CRM LOG 2 START]–[END] | CRM log + proposals | CRM log + proposals | CRM log + proposals | CRM log + proposals | CRM log + proposals |
| [AFTERNOON PLATINUM START]–[END] | Platinum: Proposals + email | Platinum: Proposals + email | Platinum: Proposals + email | Platinum: Proposals + email | Platinum: Proposals + admin |

*Customize start/end times to your Golden Hours window and existing commitments.*

---

## Power Hour Protocol

These 6 rules apply during every Power Hour block:

1. **One activity only** — Dial the phone. Write the email. Do not mix.
2. **Email closed** — Not minimized. Closed. No notifications.
3. **Mobile phone in a drawer** — Physical separation, not just silent mode.
4. **No CRM research** — Research was done in Platinum Hours. Work from your prepared list.
5. **Notes on paper; log after the block** — Take brief notes during calls; block 20–30 min post-block for CRM logging.
6. **Block interruptions** — "Do Not Disturb" sign, Slack status set, colleagues informed.

---

## Distraction Elimination Plan

| Your Distractor | Countermeasure | When It Applies |
|---|---|---|
| [DISTRACTOR 1] | [COUNTERMEASURE] | [POWER HOURS / ALL DAY] |
| [DISTRACTOR 2] | [COUNTERMEASURE] | [POWER HOURS / ALL DAY] |
| [DISTRACTOR 3] | [COUNTERMEASURE] | [POWER HOURS / ALL DAY] |
| Email first-thing habit | First email check happens AFTER Power Hour 1, not before | Every morning |
| Phone checking (avg every 7 min) | Phone in drawer during all Power Hours | Power Hours |
| Colleague drop-ins | "Do Not Disturb" signal posted during Power Hours | Power Hours |

---

## Accountability Check

At the end of each week, answer these three questions:

1. How many of your scheduled Power Hours ran start-to-finish without interruption? (Target: 80%+)
2. Did you check email before your first Power Hour on any morning? (Target: 0 days)
3. How many dials/touches did each Power Hour produce on average? (Benchmark: 25–50 dials/hr for phone blocks)
```

---

## Key Principles

**Golden Hours and Platinum Hours are not the same.** Golden Hours are when buyers are available — they are irreplaceable. If you miss them, the revenue opportunity is gone. Platinum Hours are flexible support time that can expand or contract. Every minute of Golden Hours spent on admin is a minute that cannot be recovered; every minute of Platinum Hours spent on admin is exactly where that work belongs.

**WHY:** The failure mode is treating all working hours as interchangeable. A rep who "works hard" for 10 hours but spends 4 of those hours doing CRM and email during prime selling time has not worked 10 hard hours of selling — they have worked 6 hard hours of selling and 4 hours of support activity billed at the wrong rate. The Golden/Platinum distinction ends this confusion by assigning each type of work its correct window.

**A Power Hour is an appointment with yourself.** Cancel a scheduled meeting with a hot prospect at 9 AM because a colleague wants to grab coffee and you look irresponsible. Cancel a Power Hour for the same reason and there are no immediate consequences — which is exactly why most reps cancel their Power Hours and no one else does. Treat the block as a hard commitment, not a preference.

**WHY:** Without this mindset, every interruption seems justified in isolation. The prospect research that could be done in Platinum Hours, the quick email that could wait two hours, the colleague conversation that could happen after the block — each one individually seems minor. Collectively they eliminate the block entirely. The only defense is the same rule applied to every external appointment: the block is on the calendar, it is sacred, and it does not move.

**Work contracts to fill the time available (Horstman's Corollary).** Give yourself all day to make 50 calls and it will take all day. Give yourself 60 minutes and a prepared list and it will take 60 minutes. This is not motivational — it is how attention and urgency work. The boundary forces efficiency.

**WHY:** In Blount's coaching example, an inside sales team that had been making fewer than half their required daily dials made 22 dials in 30 minutes during a forced block exercise — more than they averaged in a full day. The mechanism was time pressure combined with single-task focus: they could not check email, research prospects, or socialize. The time constraint did not add effort; it removed escape routes, which produced the same output in 4% of the time.

---

## Examples

### Example 1: B2B Enterprise SDR (Inside Sales, East Coast prospects)

**Situation:** SDR at a SaaS company. Quota: $180,000 in sourced pipeline per quarter. Annual on-target earnings: $65,000. Working weeks: 48. Prospects are primarily East Coast, 9 AM–5 PM EST reachable.

**Hourly-worth calculation:**
- $65,000 ÷ 48 weeks = $1,354/week
- 6 selling hours/day × 5 days = 30 Golden Hours/week
- $1,354 ÷ 30 = **$45 per Golden Hour**

**Calendar design:**
- Golden Hours: 9 AM–5 PM EST
- Morning Platinum: 7:30–9 AM (list prep, LinkedIn prospecting, pre-call research)
- Power Hour 1: 9–10 AM (phone block — 35–45 dials)
- CRM + email: 10–10:30 AM
- Power Hour 2: 10:30–11:30 AM (phone block)
- Midday: 12–1 PM (demos, discovery calls, lunch)
- Power Hour 3: 1:30–2:30 PM (phone block)
- Balance of afternoon: CRM, email, follow-up calls, social prospecting
- Afternoon Platinum: 4:30–5:30 PM (proposals, pipeline admin, next-day prep)

**Distraction profile:** Email notifications (every 5 min), Slack (constant), phone on desk.
- Email: Closed during all three Power Hours; checked at 10 AM, 1 PM, and 4:30 PM only
- Slack: Status set to "Prospecting — DM for urgent only" during Power Hours
- Phone: In desk drawer from 9–10 AM, 10:30–11:30 AM, and 1:30–2:30 PM

**Result target:** 3 Power Hours × 40 dials = 120 dials/day, 600/week — consistent with Sales Gravy's inside team benchmark.

---

### Example 2: Outside Rep with Mixed In-Person and Phone Prospecting

**Situation:** Outside B2B rep covering a regional territory. Annual target: $95,000 OTE. Prospects span Central and Mountain time zones. Mix of phone-based days (Mon/Fri) and field days (Tue–Thu).

**Hourly-worth calculation:**
- $95,000 ÷ 47 weeks = $2,021/week
- 5.5 selling hours/day × 5 days = 27.5 Golden Hours/week
- $2,021 ÷ 27.5 = **$73 per Golden Hour**

**Calendar design (phone days — Mon/Fri):**
- Golden Hours: 8 AM–4 PM CT (prospects are CT/MT, so this covers both)
- Morning Platinum: 7–8 AM (prepare call list, review account notes, plan call objectives)
- Power Hour 1: 8–9 AM (phone block — 25–35 dials)
- Power Hour 2: 10–11 AM (phone block — follow-up calls from field days)
- Midday: 11 AM–1 PM (proposals, pipeline review, lunch)
- Power Hour 3: 1:30–2:30 PM (phone block)
- Afternoon Platinum: 4–5 PM (next-day prep, CRM clean-up, route planning for field days)

**Calendar design (field days — Tue–Thu):**
- Golden Hours: 8 AM–4 PM local to territory
- In-person prospecting and appointments fill the Golden Hours window
- Route planned in advance (Platinum Hours) to minimize drive time within prospect time zones
- 30-min Platinum buffer before first appointment for same-day prep

---

### Example 3: Founder-Seller (Self-Managed, No Support Staff)

**Situation:** Founder doing all sales personally. Annual revenue goal: $240,000 (B2B services). Works roughly 50 hours/week but self-manages all admin, operations, and prospecting. Prospects are primarily US West Coast.

**Hourly-worth calculation:**
- $240,000 ÷ 46 weeks = $5,217/week
- 4 focused selling hours/day × 5 days = 20 Golden Hours/week (lower because more wearing all hats)
- $5,217 ÷ 20 = **$261 per Golden Hour**

**Calendar design:**
- Golden Hours: 10 AM–2 PM PST (peak B2B phone window, post-standup hour for prospects)
- Morning Platinum: 7–10 AM (email, admin, proposals, operations — all non-selling work done here before phones open)
- Power Hour 1: 10–11 AM (phone block — 20–30 dials + LinkedIn DMs)
- CRM log: 11–11:30 AM
- Power Hour 2: 11:30 AM–12:30 PM (follow-up calls + email prospecting)
- Lunch: 12:30–1 PM
- Power Hour 3 (optional, 2× week): 1–2 PM (if pipeline pressure is high)
- Afternoon: Client delivery, operations, product work
- Evening Platinum (optional): 8–9 PM (catch-up on proposals/contracts if Golden Hours ran short)

**Key principle for founder:** At $261/hour, every 15 minutes spent on admin during the 10 AM–2 PM window costs $65. Delegating $30/hour Upwork tasks that free 2 hours of Golden Hours daily generates a 4× return on that $60/day spend.

---

## References

| File | Contents |
|---|---|
| `references/golden-platinum-hours-calendar-templates.md` | Extended weekly calendar templates for inside sales, outside sales, and founder-seller configurations; copy-paste blocks for common calendar tools |
| `references/hourly-worth-worked-examples.md` | Worked hourly-worth calculations across six income levels ($45K–$300K) with time-zone calibration notes |

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fanatical Prospecting by Jeb Blount (Ch. 8).

## Related BookForge Skills

For calculating how many dials per day you need to hit quota:
```
clawhub install bookforge-pipeline-ratio-calculator
```

For setting the right objective (appointment vs. qualify vs. close) for each touch in the block:
```
clawhub install bookforge-prospecting-objective-setter
```

For writing the phone opener used during Power Hours:
```
clawhub install bookforge-cold-call-opener-builder
```

For deciding which prospects to call first when the block starts:
```
clawhub install bookforge-prospect-prioritization-pyramid
```

Browse the full Fanatical Prospecting skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
