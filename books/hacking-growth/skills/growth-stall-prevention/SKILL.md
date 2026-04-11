---
name: growth-stall-prevention
description: "Use this skill to run a quarterly audit on a growth program to detect and prevent growth stalls — the 18-month plateau that affects 87% of companies (HBR) and destroys 74% of their market cap. Reviews the North Star metric trend, channel concentration, experiment volume/cadence decay, and names the stall pattern (complacency / premature lever exit / channel dependency) with specific recovery actions. Consumes metrics history + experiment log from an existing growth operating system. Triggers when a growth lead or Head of Growth asks 'our growth has plateaued', 'we were growing then stopped', 'growth stall', 'why did our growth slow down', 'growth stall audit', 'are we at risk of stalling', 'our channels are saturating', 'experiments are slowing down', 'we keep running the same tests', 'virtuous growth cycle', 'how do I sustain growth', 'Skype growth stall', 'HBR growth stall research', or 'quarterly growth check-up'. Also activates for 'we're 18 months in and growth is flat', 'channel dependency', 'growth engine breakdown', or 'how do we reinvigorate growth'. Run this skill quarterly — stalls are preventable, but only if detected early."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/growth-stall-prevention
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [9]
tags:
  - growth
  - growth-stalls
  - quarterly-audit
  - virtuous-cycle
  - startup-ops
depends-on:
  - north-star-metric-selector
  - acquisition-channel-selection-scorer
  - growth-experiment-prioritization-scorer
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Growth metrics history (growth-metrics-history.csv) with 3+ months of
        North Star metric, funnel conversion, and channel performance data.
        Optional: experiment-log.md with experiment history for cadence analysis.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set + CSV history. Produces a quarterly growth-stall-risk-audit.md
    with findings and prescribed recovery actions.
discovery:
  goal: >
    Produce a growth-stall-risk-audit.md naming the stall risk pattern (if any),
    the warning signals, and concrete recovery actions — quarterly.
  tasks:
    - "Read growth metrics history"
    - "Compute NSM trend (slope, volatility)"
    - "Compute channel concentration (% growth from top channel)"
    - "Compute experiment cadence trend (tests/week over time)"
    - "Diagnose stall pattern (complacency / channel dependency / cadence decay)"
    - "Check virtuous cycle integrity (are loops feeding each other?)"
    - "Prescribe recovery actions"
    - "Emit growth-stall-risk-audit.md"
---

# Growth Stall Prevention

## When to Use

You are a growth lead or Head of Growth at a Series B–C company. Your growth operating system has been running for 12–18 months. Things were working, then they weren't — or things still look fine but you want to know if a stall is approaching before it arrives.

This skill runs as a **quarterly check-up**. It is not reactive firefighting; it is structured early detection. Research on 87% of companies across HBR's growth-stall study shows that stalls almost always sneak up *after* a period of strong growth, not during a weak patch. The team that feels the least urgency is usually the team most at risk.

Run this skill when any of the following apply:

- Month-over-month North Star metric growth has visibly flattened over the past 6–8 weeks
- Someone on the leadership team has asked "why did growth slow down?" without a clear answer
- The growth team is running fewer experiments this quarter than last quarter, without a deliberate reason
- More than 60% of new acquisition is coming from a single channel
- The growth operating system is 12+ months old and has never been audited for stall risk
- You want to run a scheduled quarterly review (the highest-value use of this skill)

Do not use this skill as a substitute for `north-star-metric-selector` (which selects the metric) or `acquisition-channel-selection-scorer` (which scores and selects channels). This skill assumes those are already in place and audits their health.

---

## Context and Input Gathering

Before running the audit, collect the following:

**Required:**
- `growth-metrics-history.csv` — at minimum 3 months of weekly or monthly data. Preferred: 6+ months. Must include: North Star metric value by period, funnel conversion rates (acquisition → activation → retention → monetization → referral), and channel breakdown (what % of new acquisition came from each channel per period).

**Optional but strongly recommended:**
- `experiment-log.md` — a record of experiments run by week or month, ideally including experiment name, hypothesis, result, and status (running / concluded / doubling down). Even a rough count of tests per week is sufficient for cadence analysis.

If experiment-log data is not available, ask the growth lead to estimate: "How many experiments did the team run in the last full quarter? How does that compare to the quarter before?" A single estimate is sufficient to flag cadence decay.

If metrics history covers fewer than 3 months, note this as a data gap in the audit output — insufficient history limits slope confidence — and proceed with what is available.

---

## Process

### Step 1: Read the Metrics History

Read `growth-metrics-history.csv` in full. Parse out:
- North Star metric (NSM) value per period
- Week-over-week or month-over-month growth rate per period
- Channel split per period (what % of acquisition came from each channel)
- Funnel conversion rates per stage: acquisition → activation → retention → monetization → referral

**Why:** The raw data must be read before any diagnosis. A stall can be invisible in a single snapshot but clear in a trend. Reading the full history surfaces the shape of growth: accelerating, flat, or declining, and where in the funnel the weakness lives.

---

### Step 2: Compute the NSM Trend

Calculate two rolling windows:
- **Short window:** average NSM growth rate over the most recent 6 weeks (or 2 months)
- **Long window:** average NSM growth rate over the full history (12+ weeks)

Compare the two. Flag the trend as:
- **Healthy:** short window growth rate ≥ long window rate (growth is at least holding)
- **Decelerating:** short window rate is 20–40% below long window rate (early warning)
- **Stalled:** short window rate is >40% below long window rate, or flat/negative (active stall)

Also compute volatility: if NSM swings more than ±15% week-to-week without a corresponding experiment explanation, flag instability.

**Why:** The NSM is the single number that reflects whether the virtuous cycle is compounding. A declining NSM slope is almost always a lagging indicator — something upstream (cadence, channel health, or a broken funnel link) degraded first. Catching the slope early gives recovery time.

---

### Step 3: Compute Channel Concentration

For each channel, calculate its share of total new acquisition averaged across the most recent full quarter.

Flag if:
- **Any single channel exceeds 60% of acquisition:** high concentration risk
- **Top two channels together exceed 80%:** moderate concentration risk
- **Channel share has shifted >15 percentage points** in either direction quarter-over-quarter: trend change worth investigating

The 60% threshold is the decision criterion from the source research: a single channel carrying more than 60% of acquisition means one platform rule change, one algorithm update, or one cost spike can functionally shut down growth.

**Why:** Channel dependency is the most dangerous stall pattern because it feels like success. A company growing fast on a single paid channel has no warning signal until the channel degrades. Viddy reached a $370M valuation with massive Facebook dependency, then a single News Feed algorithm change collapsed its user base from 50 million to under 500,000 per month. The dependency was structural, not visible in growth metrics until it was too late.

---

### Step 4: Compute Experiment Cadence Trend

From `experiment-log.md` (or the growth lead's estimate), compute:
- Average experiments per week in the most recent full quarter
- Average experiments per week in the prior quarter
- Direction of change: up, flat, or down

Flag if:
- Experiment volume declined more than 30% quarter-over-quarter without a documented strategic reason (e.g., deliberate sprint pause)
- Fewer than 1 experiment per week on average in the most recent quarter for a team of 3+ people
- The backlog of untested ideas has fewer than 20 items

**Why:** Cadence decay is the leading indicator that precedes NSM decline. In the GrowthHackers.com case, the team ran fewer than 10 experiments in an entire quarter while traffic plateaued — the drop in experiment volume preceded and caused the growth stall. By the time the NSM shows a problem, cadence has usually been declining for weeks or months. Tracking volume directly short-circuits the lag.

---

### Step 5: Diagnose the Stall Pattern

Using the outputs of Steps 2–4, assign a diagnosis. A program can carry multiple patterns simultaneously.

**Pattern A — Complacency (premature deceleration)**
Indicators: NSM trend decelerating or stalled; experiment cadence declining; no channel concentration issue. Root cause: the team achieved strong growth and allowed administrative routine to crowd out growth work. The false confidence that "growth is assured" replaced the urgency to keep experimenting. Recovery: reset the minimum cadence floor, rebuild the idea backlog, and explicitly re-prioritize growth work over administrative tasks in the weekly meeting.

**Pattern B — Premature Lever Exit (failure to double down)**
Indicators: NSM trend decelerating; experiment volume may be normal, but experiments are exploring new territory instead of fully exploiting proven wins. Diagnostic question: "When did the team last run a follow-on experiment on the highest-performing lever from last quarter?" If the answer is "we moved on," this is Pattern B. Recovery: apply the Battleship rule — when you get a hit, pursue it until the ship sinks. Identify the top 3 proven levers and assign explicit follow-on experiments before exploring new ground.

**Pattern C — Channel Dependency**
Indicators: channel concentration flag triggered (>60% from one source); NSM may still be healthy but the risk is structural. Recovery: immediately begin parallel channel development. Re-invoke `acquisition-channel-selection-scorer` to score and prioritize 2–3 new channel candidates. Begin at Discovery phase with small budget; do not wait until the dominant channel degrades.

**If no pattern is flagged:** NSM trend healthy, no concentration risk, cadence flat or growing. Output a clean bill of health with the recommendation to re-run in one quarter.

---

### Step 6: Virtuous Cycle Integrity Check

Review the funnel conversion rates collected in Step 1. Map them to the four links:
- **Acquisition → Activation:** is the aha moment conversion rate stable or improving?
- **Activation → Retention:** are retained users returning at the expected frequency?
- **Retention → Monetization:** are retained users converting to paid at the expected rate?
- **Monetization → Referral:** are paying users generating referrals or organic word of mouth?

Flag any link where the conversion rate has declined more than 10% over the past quarter.

**Why:** The virtuous cycle is the structural protection against long-term stalls. Facebook's growth team sustained compounding growth for a decade by continuously reinforcing every link in the loop. A stall in acquisition can be caused by a broken referral link — the feedback loop depends on every stage functioning. If a single link is broken, the compounding effect degrades even if the team is running experiments at high tempo. The virtuous cycle check catches funnel decay that channel metrics and NSM trend may not surface immediately.

---

### Step 7: Prescribe Recovery Actions

Based on the diagnosis, prescribe concrete actions matched to the pattern(s). Each action must include who owns it and when it should show measurable progress.

**For Pattern A (Complacency):**
- Set a minimum weekly experiment floor (e.g., 2–3 experiments/week for a team of 3–5; adjust for team size)
- Schedule a backlog rebuild session within the next two weeks; target 50+ ideas in the backlog
- Add "current experiment count vs. floor" as a standing agenda item in the weekly growth meeting
- Expected signal: cadence should recover within 2 weeks; NSM slope should show improvement within 6–8 weeks

**For Pattern B (Premature Lever Exit):**
- Identify the top 3 performing levers from the prior two quarters
- For each, generate at least 3 follow-on experiment ideas (deeper optimization, new contexts, larger scope)
- Slot these into the experiment backlog before any new-territory explorations
- Add a "doubling down check" to experiment prioritization: before testing a new idea, confirm the best prior wins have been fully exploited
- Expected signal: winning lever experiments should show continued lift within 4–6 weeks

**For Pattern C (Channel Dependency):**
- Immediately begin parallel channel experimentation (do not wait for the dominant channel to degrade)
- Re-invoke `acquisition-channel-selection-scorer` with the current channel mix as the baseline
- Allocate a defined discovery budget (10–15% of acquisition spend) to 2 new channel candidates
- Set a 90-day milestone: reduce single-channel concentration below 60%
- Expected signal: new channel experiments running within 2 weeks; concentration ratio improving by next quarterly audit

**For broken virtuous cycle links:**
- Flag the degraded link to the relevant functional owner (product for activation/retention, monetization lead for conversion, referral loop owner)
- Schedule a focused experiment sprint on the degraded link within 30 days
- Reference `retention-phase-intervention-selector` for retention link failures; `monetization-experiment-planner` for monetization link failures

---

### Step 8: Emit the Audit Report

Write `growth-stall-risk-audit.md` with the following structure:

```
# Growth Stall Risk Audit — [Quarter] [Year]

## Risk Score
[Low / Medium / High] — [one sentence summary]

## NSM Trend
[Healthy / Decelerating / Stalled] — [slope data]

## Channel Concentration
[Flag: Yes/No] — [top channel %, quarter-over-quarter shift]

## Experiment Cadence
[Healthy / Declining / Critical] — [tests/week, quarter-over-quarter change]

## Virtuous Cycle Integrity
[All links healthy / Degraded links: X, Y] — [conversion rates]

## Diagnosed Pattern(s)
[None / Pattern A / Pattern B / Pattern C / Combination]

## Evidence
[Specific data points supporting the diagnosis]

## Recovery Actions
[Numbered list, owner, timeline, expected signal]

## Next Audit
[Date — one quarter out]
```

---

## Key Principles

**Stalls are preventable but hard to reverse once established.** The HBR study showed that 74% of market cap is lost in the decade surrounding a stall — not just the year of. The asymmetry between early detection and late-stage recovery is extreme. A quarterly audit costs hours; a full stall recovery costs months and organizational trust.

**87% of companies experience a stall — yours is statistically likely.** The question is not whether a stall will happen but whether it will be caught early. Companies that treat stalls as an "other companies" problem are the most vulnerable.

**Channel dependency feels like success until it doesn't.** Viddy's collapse from 50 million to under 500,000 users in a single quarter was not a surprise in hindsight — the dependency was visible in the metrics. The team just wasn't auditing for it.

**Cadence decay is a leading indicator.** Experiment volume drops before the NSM drops. Tracking cadence directly is the earliest available signal. If the team ran fewer than 10 experiments last quarter without a deliberate reason, the stall has already begun structurally even if growth still looks healthy on the dashboard.

**The virtuous cycle is the protection — feed every loop.** Acquisition-only focus creates a leaky bucket. The companies that sustain growth for 10+ years (Facebook is the book's primary case) reinforce every link: activation, retention, monetization, and referral, continuously and in parallel. A broken referral link is a broken acquisition multiplier.

**Run this skill quarterly even when growth looks healthy.** The most dangerous stalls follow periods of strong growth. The team with the least urgency is usually closest to a plateau. Schedule the audit before it feels necessary.

---

## Examples

### Example 1: Channel Dependency Stall (Viddy Pattern)

A mobile productivity startup grew from 100K to 2M monthly actives over 18 months, primarily through Facebook paid acquisition. NSM trend was healthy — the team was proud of their growth rate. Quarterly audit revealed: 72% of new acquisition from Facebook ads, 15% from App Store organic, 13% from all other sources combined. The team had never run experiments on organic channels because paid was working so well.

The audit diagnosed Pattern C (Channel Dependency). Recovery actions: (1) allocated 15% of paid budget to Apple Search Ads experiments; (2) re-ran `acquisition-channel-selection-scorer` to score SEO, content partnerships, and referral; (3) set a 90-day target to reduce Facebook concentration below 60%. Six months later, Facebook share was 51%, App Store organic was 28%, and referral had grown to 12% — a structurally healthier distribution, and the startup survived a subsequent Facebook algorithm change that dropped similar competitors' acquisition by 40%.

### Example 2: Cadence Decay Stall (GrowthHackers Pattern)

A B2B SaaS company had strong product-market fit and had grown ARR 3x in its first year. The growth team of four people slowed their experiment pace after the initial push — Q1 had 24 experiments; Q2 had 11; Q3 had 6. NSM (weekly active teams) was still growing slightly, but the slope had decelerated from 12% month-over-month to 4%. No one on the team had noticed the cadence drop.

The quarterly audit flagged Pattern A (Complacency) and Pattern B (Premature Lever Exit). The email onboarding sequence had been the highest-performing lever in Q1 but had received no follow-on experiments in six months. Recovery: (1) set a cadence floor of 2 experiments/week; (2) rebuilt the backlog from 15 to 80 ideas in a single team session; (3) ran 4 follow-on experiments on the email onboarding sequence in the next 6 weeks, producing a 31% lift in 30-day retention. NSM growth rate returned to 9% month-over-month by end of quarter.

---

## Audit Limitations and Edge Cases

**Fewer than 3 months of data:** The NSM slope calculation requires at least 3 months (12 weeks) to be meaningful. With less data, report the NSM trend as "insufficient history" and focus the audit on channel concentration and cadence, which are assessable with a single quarter of data.

**Deliberate cadence pauses:** A team that intentionally paused experiments for a product rebuild or major launch is not experiencing cadence decay — it is making a strategic trade-off. Audit output should note the pause reason and confirm a resumption date rather than diagnosing Pattern A.

**Pre-revenue or pre-retention programs:** This audit assumes all four virtuous cycle links are active. If monetization or referral loops have not yet been built, limit the virtuous cycle check to the available links and note the gap as a planned future audit scope.

**Multiple patterns simultaneously:** The most common finding at 18+ months is a combination of Patterns A and B — the team slowed down *and* failed to double down on proven levers. Prescribe recovery actions for both; do not force a single-pattern diagnosis.

**No experiment log available:** If the team has no experiment log, the cadence analysis relies on self-report. Accept the estimate but recommend that the team begin maintaining a simple experiment log (experiment name, date, result) as a prerequisite for the next quarterly audit. Without it, cadence is blind.

---

## References

- `references/growth-stall-statistics.md` — HBR study: Olson, Van Bever, Verry (CEB); 87% stall rate; 74% market cap loss; Levi Strauss case ($7B → $4.6B); additional named brands (3M, Apple, Caterpillar, Toys "R" Us, Volvo)
- `references/virtuous-growth-cycle.md` — The acquisition → activation → retention → monetization → referral compounding loop; Facebook 10-year case as the primary sustained-growth exemplar
- `references/channel-concentration-thresholds.md` — The >60% single-channel concentration decision rule; Viddy case (50M → <500K after Facebook algorithm change); Upworthy/BuzzFeed News Feed dependency; Google ranking algorithm as analogous SEO risk
- `references/experiment-cadence-baselines.md` — GrowthHackers.com recovery case: <10 tests/quarter → 3/week floor → 76% traffic increase in one quarter; cadence floor calibration by team size

---

## License

[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — Skills from the BookForge library. Share alike with attribution.

---

## Related BookForge Skills

This skill sits on top of the growth operating system and audits its health. For recovery actions, reinvoke the relevant operating skills:

```bash
# NSM trend analysis — provides the north star metric this skill audits
clawhub install bookforge-north-star-metric-selector

# Channel recovery — re-score and prioritize new acquisition channels
clawhub install bookforge-acquisition-channel-selection-scorer

# Cadence recovery — re-prioritize experiments and rebuild the backlog
clawhub install bookforge-growth-experiment-prioritization-scorer

# Cadence floor — reset the experiment cycle to a minimum weekly tempo
clawhub install bookforge-high-tempo-experiment-cycle

# Retention link failures — diagnose and intervene on broken retention
clawhub install bookforge-retention-phase-intervention-selector

# Monetization link failures — experiment on the monetization funnel link
clawhub install bookforge-monetization-experiment-planner
```
