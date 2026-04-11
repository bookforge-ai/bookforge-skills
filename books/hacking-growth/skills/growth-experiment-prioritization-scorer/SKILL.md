---
name: growth-experiment-prioritization-scorer
description: "Use this skill to score and rank a growth experiment backlog using the ICE framework (Impact, Confidence, Ease — each rated 1–10 and averaged) and select the top experiments for the next sprint. Reads an experiment-backlog.md file, applies the ICE rubric with explicit definitions for each dimension, ranks all experiments, separates 'launch now' from 'pipeline with target date' from 'drop', and emits a scored backlog the team can bring to their weekly growth review. Triggers when a growth PM asks 'help me prioritize my experiment ideas', 'which test should I run next', 'ICE score my backlog', 'rank these growth experiments', 'how do I pick experiments for this sprint', 'impact confidence ease', 'ICE framework', 'growth experiment prioritization', or 'I have 40 test ideas, which ones first'. Also activates for 'score this backlog', 'my experiment queue is a mess', 'we keep running low-impact tests', 'growth experiment ranking', or 'how to rank A/B test ideas'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/growth-experiment-prioritization-scorer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [4]
tags:
  - growth
  - experimentation
  - prioritization
  - ICE-scoring
  - startup-ops
depends-on:
  - north-star-metric-selector
  - high-tempo-experiment-cycle
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Experiment backlog (experiment-backlog.md) as a markdown list of ideas
        with hypothesis, metric, and optional effort estimate. North Star metric
        from prior invocation of north-star-metric-selector, or asked from user
        if not available.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set. Reads a backlog file and emits a scored/ranked version.
discovery:
  goal: >
    Produce a ranked experiment-scored-backlog.md with ICE scores and a clear
    recommendation for the next sprint.
  tasks:
    - "Read experiment backlog file"
    - "Confirm or gather the team's North Star metric"
    - "Score each experiment on Impact, Confidence, Ease (1-10)"
    - "Compute average and rank"
    - "Split into 'launch now', 'pipeline with date', and 'drop'"
    - "Emit experiment-scored-backlog.md"
---

# Growth Experiment Prioritization Scorer

Score and rank a growth experiment backlog using the ICE framework, then select the top experiments for the next sprint. The output is a structured scored backlog the team can bring directly to their weekly growth review meeting and begin acting on.

ICE — Impact, Confidence, Ease — was developed at GrowthHackers.com as a way to convert a pile of unordered experiment ideas into a ranked, actionable queue. The scoring is deliberately simple: three dimensions, a 1–10 scale each, averaged to one number. The value is not precision — it is shared calibration. A team that scores ideas against a common rubric before the meeting arrives at a defensible ranking in minutes rather than spending the full meeting debating which idea to try first.

## When to Use

Use this skill when:

- You have a backlog of growth experiment ideas (5–100+) and need to decide which to run in the next 1–2 week sprint
- Your team keeps gravitating toward familiar or easy tests rather than the highest-impact options
- Experiment selection is happening in the weekly meeting by whoever argues most persuasively, rather than by a pre-meeting scoring process
- You are entering a new growth focus area (acquisition, activation, retention, monetization) and need to groom the idea bank for that area
- You have just used `high-tempo-experiment-cycle` to install a weekly cadence and need to score the initial backlog before the first growth meeting

Prerequisites before using this skill:
- You have a confirmed North Star metric (from `north-star-metric-selector` or from the team's existing documentation). Impact scoring is meaningless without a shared reference metric.
- The backlog exists as a document with at least a name and hypothesis per idea. Vague ideas ("improve onboarding") cannot be scored — they must be made specific first.

---

## Context and Input Gathering

Before scoring, collect two inputs.

**Input 1 — Experiment backlog file**

Ask the user: "Please share the path to your `experiment-backlog.md` file, or paste the backlog content directly." Read the file. Each idea in the backlog should have:
- A name (max 50 characters is the book's recommendation — force brevity)
- A hypothesis: "By doing X, metric Y will change by Z"
- A target metric (which metric this experiment directly affects)
- An optional effort estimate (days / team members required)

If ideas are missing a hypothesis, flag them. You can score ideas without an effort estimate (Ease will be estimated), but you cannot score ideas without a hypothesis — without knowing what the experiment is supposed to change, Impact and Confidence scores are fabricated.

**Input 2 — North Star metric**

Ask: "What is your team's current North Star metric and focus area (e.g., 'weekly revenue per active user, focused on activation this sprint')?" If the user ran `north-star-metric-selector`, pull the NSM from `north-star-recommendation.md`. If unavailable, ask directly. Do not proceed to scoring without this — Impact scores are defined relative to the NSM.

---

## Process

### Step 1: Read the Backlog

Read `experiment-backlog.md` in full. Count the ideas. Note:
- Which ideas have a complete hypothesis (name + cause-and-effect hypothesis + target metric)
- Which ideas are vague or missing a hypothesis — flag these as "needs clarification before scoring"
- Which ideas target the current focus area vs. other growth levers (e.g., retention ideas in an activation sprint)

**Why this step:** Scoring a vague idea produces a fake ICE score. An idea named "improve checkout" with no hypothesis could mean anything — a copy tweak (days of work) or a full redesign (weeks). Flagging incomplete ideas before scoring forces the submitter to sharpen the idea, which is itself valuable and usually surfaces the key assumption the experiment is testing.

### Step 2: Confirm the North Star Metric

State the confirmed NSM explicitly: "NSM for this sprint: [metric name], defined as [precise definition with time dimension]."

**Why this step:** Impact scores are always relative to the NSM. "10" means "expected to move the NSM meaningfully in the next sprint." Without this anchor, a "9" from one team member means something completely different from a "9" from another — the scores are not comparable, and the ranking is not useful.

### Step 3: Score Impact (1–10)

For each idea, assign an Impact score using this rubric:

| Score | Meaning |
|-------|---------|
| 9–10 | Expected to produce a large, direct movement in the NSM. The mechanism is clear and well-grounded. |
| 7–8 | Expected to produce a meaningful, measurable improvement in an NSM input metric. Direct NSM effect is plausible but not certain. |
| 5–6 | Expected to improve a metric adjacent to the NSM. Effect may be indirect or conditional. |
| 3–4 | Narrow improvement — affects a small user segment or a metric weakly connected to the NSM. |
| 1–2 | No credible mechanism to move the NSM or any meaningful input metric. May produce a local improvement that does not compound. |

Key calibration rule: a low-impact score is not a reason to discard an idea — it is a reason to pair it with high Ease or reconsider what it is actually testing. A quick, low-cost idea with modest impact still belongs in the queue; it just runs after the high-impact work.

**Why this step:** Impact calibration is the most common ICE failure mode. Teams inflate impact scores ("everything is an 8!") because they want their ideas to win, not because they have a clear mechanism for NSM movement. Anchoring to the NSM rubric forces the question: "What specifically will change in the NSM if this test wins?"

### Step 4: Score Confidence (1–10)

For each idea, assign a Confidence score using this evidence ladder:

| Score | Evidence Base |
|-------|--------------|
| 9–10 | Strong prior evidence: internal data showing user behavior consistent with the hypothesis, plus a published case study or industry benchmark from a comparable company. Direct iteration of a past winning experiment at this company ("doubling down"). |
| 7–8 | Solid evidence: internal behavioral data supports the hypothesis, or a well-documented case study from a comparable product type. Team has run a related (not identical) experiment with positive results. |
| 5–6 | Moderate evidence: user survey data or interview data suggests the problem exists. No direct experimental evidence, but logic is sound and the mechanism is plausible. |
| 3–4 | Weak evidence: hypothesis is based primarily on team intuition or general industry patterns. No internal data support. May be correct, but the submitter is guessing. |
| 1–2 | Pure conjecture: no data, no precedent, no user evidence. The idea is speculative. May still be worth testing if Ease is high. |

**Why this step:** Confidence rewards epistemic honesty. A submitter who scores their own idea at 9 on confidence is claiming they have strong evidence — that is a testable claim the growth lead can check. Teams that cannot differentiate a data-backed hypothesis from a gut feeling are systematically over-investing in weak ideas. The evidence ladder gives submitters a shared vocabulary for calibrating uncertainty.

### Step 5: Score Ease (1–10)

For each idea, assign an Ease score using this rubric:

| Score | Effort Level |
|-------|-------------|
| 9–10 | Less than 1 day, single person, no dependencies. Copy change, image swap, minor UI adjustment. Can be shipped and measured within the current sprint. |
| 7–8 | 1–3 days, one or two people, minimal coordination. Small feature flag, minor backend change, email copy variant. |
| 5–6 | 3–7 days, involves a second function (e.g., engineering + design). Can probably be launched in the current sprint if started immediately. |
| 3–4 | 1–2 weeks, cross-team coordination required (e.g., engineering + product + legal review). Target the sprint after this one. |
| 1–2 | More than 2 weeks, significant product investment or cross-functional coordination. Requires a scheduled target date, not a sprint slot. |

Penalty rule for cross-team dependencies: if an experiment requires sign-off or execution from a team that is not on the growth team (e.g., a feature that requires a full product sprint, or an email campaign that requires legal review), reduce the Ease score by at least 2 points. Cross-team dependencies predictably slow experiments beyond the initial estimate.

**Why this step:** Ease provides the cycle's pacing mechanism. Without it, teams fill the sprint with high-impact, low-ease experiments that never finish and crowd out the learning the cycle needs to compound. Ease also surfaces low-hanging fruit — quick tests that might surprise the team, the way a newsletter form relocation at GrowthHackers produced a 700% lift despite a low initial impact estimate.

### Step 6: Compute Average and Rank

For each idea: ICE Score = (Impact + Confidence + Ease) / 3. Round to one decimal place.

Sort all ideas by ICE score, highest to lowest. This is the ranked backlog.

**Why this step:** Averaging — not summing — means the three dimensions are equally weighted and no single dimension can dominate. A 10/10/1 idea scores 7.0; a 7/7/7 idea also scores 7.0. The parity is intentional: an extremely high-impact idea that is nearly impossible to ship should not outrank a solid, executable idea just because the impact score is higher.

Produce a table in this format:

```
| Rank | Experiment Name | Impact | Confidence | Ease | ICE Avg | Status |
|------|-----------------|--------|------------|------|---------|--------|
| 1    | [Name]          | 8      | 7          | 9    | 8.0     | Launch now |
| 2    | [Name]          | 9      | 8          | 4    | 7.0     | Pipeline: [date] |
| ...  | ...             | ...    | ...        | ...  | ...     | ...    |
```

### Step 7: Split into Launch / Pipeline / Drop

After ranking, apply the triage:

**Launch now** — Ideas the team should select for the current sprint. Criteria: ICE average high enough to justify the team's time relative to other ideas in the queue, and Ease score high enough to be completable within one sprint (Ease ≥ 5 as a default threshold, adjustable by the growth lead). The number of "launch now" ideas should match team capacity — a 4-person team running 2 experiments per week selects 2–4 ideas; a 12-person team running 8 per week selects 8–12.

**Pipeline with target date** — Ideas that are worth running but cannot launch in the current sprint. This includes:
- High-ICE ideas with low Ease (≤ 4) that require engineering scope estimation before a sprint slot can be assigned
- Ideas that are solid but ranked below the sprint capacity cutoff
- Ideas that target a different focus area than this sprint's priority

For each pipeline idea, assign a target sprint date using input from the relevant team (engineers estimate product work; marketers estimate channel experiments). Record the date in the scored backlog.

**Drop** — Ideas with ICE average below a threshold (default: ≤ 3.5) that lack a clear mechanism for NSM movement and have no strong evidence base. Before dropping, verify: is the low score due to a poorly written hypothesis that could be improved? If so, return it to the submitter with feedback. If the idea is genuinely low-value, mark it as dropped with a one-sentence reason.

**Why this step:** The pipeline is the team's most important asset. An empty pipeline means the weekly meeting runs out of candidates. But a pipeline filled with vague, undifferentiated ideas is equally useless — it creates the illusion of a full queue while the real work is selecting from noise. The three-bucket split forces explicit decisions rather than allowing ideas to accumulate indefinitely without a commitment.

### Step 8: Emit experiment-scored-backlog.md

Write `experiment-scored-backlog.md` with the following structure:

1. **Header** — sprint date, North Star metric, focus area, total ideas scored
2. **Launch now** — ranked table for the current sprint, with owner field (blank, to be assigned in the growth meeting)
3. **Pipeline** — ranked table with target sprint dates
4. **Dropped** — list with reason per idea
5. **Flagged for clarification** — ideas that could not be scored because they lack a hypothesis, with specific question to ask the submitter

---

## Key Principles

1. **Impact is always relative to the North Star metric.** There is no such thing as an impact score without a reference metric. An idea that scores 9 on impact for a retention-focused sprint would score 4 in an acquisition-focused sprint. Before scoring, confirm the NSM and the current focus area — every Impact score is anchored there.

2. **Confidence rewards evidence over enthusiasm.** Submitters naturally overestimate confidence in their own ideas. The evidence ladder exists to make the claim testable: "You scored this a 9 — show me the internal data and the case study you're referencing." If the submitter cannot produce evidence matching the ladder, the score should come down.

3. **Ease penalizes cross-team dependencies because they predictably slow the cycle.** An experiment that requires sign-off from a team outside the growth team almost always takes longer than estimated. The 2-point penalty is a calibration correction for the team's natural optimism about coordination costs.

4. **ICE is deliberately blunt — the goal is a relative ranking, not an absolute forecast.** A score of 7.3 vs. 7.1 is not meaningful. A score of 8.5 vs. 5.2 is. The system's value is in separating the top tier from the middle tier from the bottom tier, not in creating a precise numerical ranking. When two ideas are close, the growth lead uses judgment — the score is the starting point for the selection conversation, not the final word.

5. **Run the scoring before the meeting, not in it.** ICE scoring done synchronously in the weekly growth meeting burns the entire meeting on a task that can be done asynchronously. The scored backlog is prep work. The meeting uses the ranked list to make the selection decision in 15 minutes.

6. **The lowest-scoring ideas can still be the biggest winners.** The 700% newsletter lift came from a form relocation that scored 4 on Impact. Score informs selection order, not selection cutoff. If an idea is quick to run and the downside of being wrong is minimal, run it — the cost of not learning is real.

---

## Examples

### Example 1: Series A — 20-Idea Backlog, Activation Sprint

A B2B SaaS team of 5 (growth PM, engineer, designer, marketer, data analyst) has 20 experiment ideas targeting activation — getting new trial users to the "aha moment" (≥3 team members using a shared project within 7 days). North Star: weekly collaborative sessions per team.

The scored backlog (abbreviated) looks like:

| Rank | Experiment | Impact | Confidence | Ease | ICE | Status |
|------|------------|--------|------------|------|-----|--------|
| 1 | Add progress bar to team setup wizard | 8 | 7 | 9 | 8.0 | Launch now |
| 2 | In-app prompt to invite 2nd team member at step 3 | 8 | 8 | 7 | 7.7 | Launch now |
| 3 | Email sequence: days 1, 3, 7 post-signup | 7 | 8 | 6 | 7.0 | Launch now |
| 4 | Rebuild onboarding checklist UI | 9 | 6 | 3 | 6.0 | Pipeline: next sprint |
| 5 | Integration with Slack for task notifications | 8 | 5 | 2 | 5.0 | Pipeline: 3 weeks (eng scoping) |
| ... | ... | ... | ... | ... | ... | ... |
| 19 | Add mascot to empty state screens | 3 | 4 | 8 | 5.0 | Drop |
| 20 | Redesign marketing site hero | 4 | 3 | 2 | 3.0 | Drop |

**Sprint selection:** The growth PM selects experiments 1, 2, and 3 for the sprint (matching the team's capacity of 2–3 tests per week). Experiment 4 is slotted for the following sprint pending design mockups. Experiment 5 goes to engineering for a scope estimate. Experiments 19 and 20 are dropped — neither has a clear mechanism to increase collaborative sessions, which is the current NSM.

### Example 2: Series B — 50-Idea Backlog, Retention Sprint

A marketplace team of 12 (two growth squads: acquisition + retention) needs to groom 50 ideas for a retention sprint targeting 90-day repeat purchase rate. North Star: orders per buyer per quarter.

**Scoring challenge:** The retention squad notices that 15 of the 50 ideas are acquisition ideas submitted by the other squad — they score well on Impact but target a different focus area. The growth lead moves all 15 to a separate acquisition backlog without scoring them in the retention sprint.

The remaining 35 retention ideas are scored. The top 8 (ICE ≥ 6.5) are selected for the sprint — 4 per squad per week. Ideas ranked 9–20 (ICE 4.5–6.4) are pipelined with dates. Ideas 21–35 (ICE ≤ 4.4) are reviewed for hypothesis quality: 5 are returned to submitters for clarification; 10 are dropped.

**Key finding from the scoring:** Three ideas that the retention squad assumed were quick (scoring themselves 8 on Ease) were recalibrated to Ease 4 by the growth lead after consulting the engineering team — all three required A/B test infrastructure that was not yet in place. Moving them to the pipeline freed up sprint slots for two mid-ranked ideas (ICE 6.2) that were genuinely fast to ship. The sprint launched on schedule.

---

## References

- `research/growth-experiment-prioritization-scorer.md` — source passages from Chapter 4 on ICE scoring, evidence definitions, and pipeline management
- `references/ice-scoring-guide.md` — worked scoring examples by experiment type
- `orchestration/specs/skill-spec.md` — BookForge skill authoring standards

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Hacking Growth* by Sean Ellis and Morgan Brown.

---

## Related BookForge Skills

This skill is the Prioritize stage of the high-tempo experiment cycle and consumes the North Star metric produced upstream:

```
# Required upstream — NSM must be confirmed before scoring
clawhub install bookforge-north-star-metric-selector

# The cycle this skill plugs into — Prioritize is Stage 3
clawhub install bookforge-high-tempo-experiment-cycle

# Feeds activation experiment ideas into the backlog
clawhub install bookforge-activation-funnel-diagnostic

# Feeds retention experiment ideas into the backlog
clawhub install bookforge-retention-phase-intervention-selector
```

Browse more: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
