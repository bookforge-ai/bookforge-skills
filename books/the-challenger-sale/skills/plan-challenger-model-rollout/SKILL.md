---
name: plan-challenger-model-rollout
description: "Plan a full Challenger model rollout for a sales organization. Use when someone asks: 'implement Challenger model', 'roll out new sales methodology', 'sales transformation plan', 'change management sales', 'pilot Challenger', 'sales methodology adoption', 'implementation roadmap', 'enablement plan', 'sales training rollout', 'sales change management', 'how do I roll out Challenger', 'Challenger implementation plan', 'sales force transformation', 'how to scale Challenger across the team'. Applies Grainger's four-question pilot framework, star/core/laggard adoption sequencing, 80% adoption target, 20–30% attrition planning, and a four-track parallel workstream design (training, tools, coaching, manager enablement). Produces a rollout-plan.md with pilot scope, adoption sequence, 12-month milestone schedule, and attrition/backfill plan."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/plan-challenger-model-rollout
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors: ["Matthew Dixon", "Brent Adamson"]
    chapters: [9]
tags: [sales, sales-enablement, challenger-sale, implementation, change-management, sales-transformation]
depends-on: [classify-rep-profile, diagnose-manager-effectiveness]
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Team composition context: rep-profile distribution from classify-rep-profile + manager effectiveness diagnoses from diagnose-manager-effectiveness + organizational context (team size, current methodology, business unit scope)"
  tools-required: [Read, Write, AskUserQuestion]
  tools-optional: []
  mcps-required: []
  environment: "Any working directory. No codebase required."
discovery:
  goal: "Plan a staged rollout of the Challenger model using Grainger's four-question pilot framework, adoption sequencing, and a parallel-track workstream design"
  tasks:
    - "Gather organizational context: team size, current methodology, rep profile distribution, manager effectiveness baseline"
    - "Run anti-pattern check: verify Challengers were identified by diagnostic, not manager nomination"
    - "Design pilot scope using Grainger's four-question framework"
    - "Sequence adoption waves by star/core/laggard segments"
    - "Set 80% adoption target and 20–30% attrition expectation with backfill plan"
    - "Design four parallel-track workstreams: training, tools, coaching, manager enablement"
    - "Apply training effectiveness triad: pre-training buzz, safe practice, behavioral certification"
    - "Produce rollout-plan.md with 12-month milestones"
  audience:
    roles: ["Sales enablement leaders", "Sales VPs", "Chief Revenue Officers", "Change managers", "Sales operations"]
    experience: senior
  when_to_use:
    triggers:
      - "Sales leader wants to implement or scale the Challenger Selling Model across a team or organization"
      - "Enablement team needs a structured rollout plan after completing rep profile classification"
      - "Organization is designing a sales transformation program and needs a sequenced adoption strategy"
      - "Leadership wants to move beyond ad hoc Challenger training to a systematic implementation"
    prerequisites:
      - "classify-rep-profile run across the rep population to establish baseline profile distribution"
      - "diagnose-manager-effectiveness run across frontline managers to establish coaching baseline"
    not_for:
      - "Hiring plans — Appendix C hiring guide is out of scope; plan backfill headcount but not the hiring process itself"
      - "Individual rep coaching sessions (use coach-rep-with-pause-framework)"
      - "Diagnosing individual rep profiles (use classify-rep-profile)"
      - "Diagnosing individual manager effectiveness (use diagnose-manager-effectiveness)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      density: 4
      tier: 1
      mode: plan-only
---

# plan-challenger-model-rollout

Plan a staged implementation of the Challenger Selling Model using Grainger's four-question pilot framework, star/core/laggard adoption sequencing, and a four-track parallel workstream design. Produces a rollout-plan.md artifact.

## When to Use

Use this skill when a sales leader, enablement team, or CRO needs a structured implementation plan for rolling out the Challenger model at organizational scale. This skill synthesizes inputs from `classify-rep-profile` (team profile distribution) and `diagnose-manager-effectiveness` (manager coaching baseline) into an executable rollout plan.

Do not use this skill for individual rep coaching, individual manager diagnosis, or hiring design.

---

## Step 1 — Gather Organizational Context

Ask the following questions if not already provided in the input document:

1. **Team scope:** How many reps and frontline managers are in scope? Single region, BU, or global?
2. **Current methodology:** What is the current sales methodology (if any)? How long has it been in place?
3. **Rep profile baseline:** Has `classify-rep-profile` been run? What is the current distribution across the five profiles (Challenger, Hard Worker, Relationship Builder, Lone Wolf, Reactive Problem Solver)?
4. **Manager baseline:** Has `diagnose-manager-effectiveness` been run? How many managers are strong on Coaching/Innovating drivers vs. weak?
5. **Existing Challenger content:** Does a Commercial Teaching message library exist? Is it marketing-owned or field-generated?
6. **Timeline pressure:** Is there a board or QBR milestone driving timeline? What is the desired 12-month outcome?
7. **Performance tier distribution:** What share of reps are currently in top 20% / middle 60% / bottom 20% by quota attainment?

**Why:** The rollout plan is calibrated to your actual team composition. A team with 35% existing Challengers needs a different pilot scope than a team with 10%. Managers with weak coaching capacity need enablement before they can sustain behavior change in reps.

---

## Step 2 — Anti-Pattern Check: Verify Challenger Identification Method

Before designing any rollout, confirm how Challengers were identified.

**The anti-pattern:** Asking managers to nominate their best Challengers. Managers reliably nominate their high performers regardless of actual selling profile. Roughly 40% of high performers are true Challengers — the remainder are high-performing Lone Wolves, Hard Workers, or Relationship Builders.

**The consequence:** If the rollout is designed to replicate the behaviors of a high-performing Lone Wolf (or Relationship Builder) rather than a true Challenger, the entire model being scaled is wrong.

**The fix:**
- Confirm that `classify-rep-profile` was run using the Appendix B diagnostic instrument (44-attribute behavioral assessment), not manager nomination
- If manager nomination was used, flag this explicitly in the rollout plan and re-classify before proceeding
- Verify that the Challengers being studied have all three subscale strengths: Teach (high), Tailor (high), Take-Control (high)
- Check for "inactive Challengers" — reps who have the profile but haven't activated it; these are high-leverage early intervention targets

Document this finding in the rollout plan's readiness section.

---

## Step 3 — Design the Pilot Using Grainger's Four-Question Framework

Before launching to the full organization, design a pilot. W. W. Grainger pilots not just to test tools, but specifically to understand adoption dynamics before broad launch.

Apply the four questions to your pilot design:

**Q1: How big is the early adopter group?**
Estimate how many reps will self-select into the pilot. This tells you when adoption will naturally plateau without active intervention. Typically: reps with existing Challenger traits + high performers eager for a new edge.

**Q2: Who are the early adopters, and how are they different from non-adopters?**
Profile the early adopter group: profile distribution, quota performance, tenure, region. This tells you where the initial lift will come from and what characteristics predict adoption success — essential for building the majority-wave case.

**Q3: What metrics will predict tool and methodology impact?**
Define leading indicators before the pilot begins. Options: conversation-quality scores, deal velocity, win rate on complex accounts, customer pushback frequency. These give you a signal before quota impact shows up in lagging data.

**Q4: What can we learn to improve tool impact and push majority adoption?**
Build a structured learning cadence into the pilot: weekly debrief, mid-pilot adjustment gate, post-pilot review before majority wave launch.

**Pilot scope recommendation:**
- Size: 10–20% of total rep population, or one region/segment
- Duration: 60–90 days (enough time for behavior change to show in leading indicators)
- Comparison: Include a control group (comparable reps not in pilot) if feasible — enables delta measurement
- Champion managers: Assign your two or three strongest-coaching managers to the pilot cohort

---

## Step 4 — Sequence Adoption by Wave

Map Grainger's adoption segments to your performance tiers:

| Wave | Adoption Segment | Performance Tier | Strategy |
|------|------------------|------------------|----------|
| 1 (Pilot) | Early adopters | Stars + activated/inactive Challengers | Self-selection + direct invitation; champion managers; generate success stories |
| 2 (Majority) | Majority | Core performers (middle 60%) | Show early adopter success stories; proximity matters — use peer stories not star stories |
| 3 (Laggards) | Laggards | Resistant core / lower performers | Use success stories from peers in their own segment; manager-led individual conversations |
| 4 (Non-adopters) | Naysayers | Quota-beaters who refuse | Apply "live by the sword" policy; monitor quota performance; no active forcing |

**Proximity rule (critical):** Do not use star performer success to persuade average performers. People adopt when they see people *like themselves* succeeding. Document average-performer transition stories — reps who moved from non-Challenger to Challenger and improved quota attainment — specifically for majority and laggard wave communication.

**Target:** 80% adoption across the full rep population. Do not target 100%. The final 20% is disproportionately costly to attain. Non-adopters who beat quota are treated as new Lone Wolves: acceptable while above goal, required to adopt or transition if performance slips.

---

## Step 5 — Set Attrition Expectation and Backfill Plan

Expect 20–30% of reps to not complete the transition to the Challenger model. This is not a failure of the program — it reflects genuine profile incompatibility with a teaching-and-control-oriented approach.

**Redeployment options (not termination by default):**
- Customer success or account management roles (relationships, not complex selling)
- Marketing or product specialist roles (deep domain knowledge without quota pressure)
- Internal sales or smaller-account segments with lower complexity requirements

**Backfill plan:**
- Estimate headcount gap: if team is 100 reps, plan for 20–30 eventual departures over 18–24 months
- Note: The Challenger Hiring Guide (Appendix C) is the recommended hiring instrument for replacements, but is out of scope for this skill
- Plan headcount addition to start 6–9 months into the rollout as attrition pattern becomes clear
- Inform HR and recruiting of the incoming volume before the majority wave launches

Document the attrition expectation explicitly in the rollout plan — surprises here create panic; expectation-setting creates confidence.

---

## Step 6 — Design the Four Parallel-Track Workstreams

Do not sequence these tracks. All four must run concurrently, with explicit coordination checkpoints.

**Track 1 — Training:** Build Challenger behaviors (teach, tailor, take control) across the rep population. Use experiential safe practice on real accounts. Source facilitators with frontline sales credibility.

**Track 2 — Tools:** Build or source the Commercial Teaching message library. Pull from existing field Challengers first — they are already delivering insights to customers. Pilot tools with the early adopter wave before broad launch.

**Track 3 — Coaching:** Establish behavioral certification (not attendance certification). Managers must observe and certify rep behavior change. Coaching is the primary lever for training stickiness — 87% of training content is forgotten within 30 days without reinforcement.

**Track 4 — Manager Enablement:** Train managers before they are expected to coach. Diagnose the democratic coaching anti-pattern (managers who spread time equally miss high-leverage opportunities). Assign managers to waves based on their coaching driver strength.

Full workstream detail, milestone templates, and adoption-wave mapping: see [references/parallel-track-workstreams.md](references/parallel-track-workstreams.md).

---

## Step 7 — Apply the Training Effectiveness Triad

Training-only programs fail. Three phases are required:

**Pre-training — Generate demand:**
- Create internal buzz before rollout (not a top-down announcement)
- Share early research findings, compelling data on core performer lift (19% average improvement)
- Identify rep champions who can create peer pull-through demand
- Hold preview sessions framed as "here's what some of your peers are already doing"

**During training — Safe practice on real accounts:**
- Use real accounts, real deals, real customer challenges — not fabricated scenarios
- Require reps to apply Challenger behaviors during training to an actual live opportunity
- Design around experiential learning, not presentation delivery

**Post-training — Behavioral certification:**
- Replace "did you attend?" with "can you demonstrate the behavior?"
- Define certification criteria for each subscale: Teach, Tailor, Take-Control
- Build ongoing manager coaching cadence into the certification cycle
- Track leading behavior indicators (not just lagging quota results)

---

## Step 8 — Write rollout-plan.md

Produce the following artifact:

```markdown
# Challenger Model Rollout Plan
## Organization: [Name]
## Scope: [Teams/BUs in scope]
## Date: [Plan date]

## Readiness Assessment
- Rep profile baseline: [distribution from classify-rep-profile]
- Manager baseline: [distribution from diagnose-manager-effectiveness]
- Challenger identification method: [diagnostic / nomination — flag if nomination]
- Inactive Challengers identified: [count and names]
- Lone Wolf risk: [count of Lone Wolves — do not scale these behaviors]

## Pilot Design (Grainger Framework)
- Q1 — Early adopter group size: [estimate]
- Q2 — Early adopter characteristics vs. non-adopters: [profile]
- Q3 — Leading indicator metrics: [3–5 specific metrics]
- Q4 — Learning capture plan: [weekly debrief structure, adjustment gate timing]
- Pilot cohort: [rep count, region/segment, assigned managers]
- Control group: [yes/no, description]
- Pilot duration: [60 / 90 days]

## Adoption Sequence
- Wave 1 Pilot: [dates, cohort, champion managers]
- Wave 2 Majority: [dates, cohort, peer success stories from Wave 1]
- Wave 3 Laggards: [dates, cohort, segment-proximity stories]
- Wave 4 Non-adopters: [monitoring policy — "live by the sword"]

## Adoption Targets
- 80% adoption target by: [date]
- Non-adopter policy: [quota-beating = tolerated; performance slip = adopt or transition]

## Attrition Plan
- Expected attrition: 20–30% of [N] reps = [low estimate]–[high estimate] reps
- Timeline: over [18–24 months]
- Redeployment options: [customer success / marketing specialist / smaller accounts]
- Backfill start: [6–9 months into rollout]
- HR notification: [date]

## Four-Track Workstream Timeline (12 months)
| Month | Training | Tools | Coaching | Manager Enablement |
|-------|----------|-------|----------|--------------------|
| 1–2   | Demand generation; facilitator selection | Challenger ID and field message inventory | Manager diagnostic complete | Manager training begins |
| 3–4   | Pilot cohort trained | Pilot tool set v1 ready | Certification rubric defined | Champion managers briefed |
| 5–6   | Pilot debrief; majority wave prep | Tool improvements from pilot | Pilot cohort certification cycle | All managers trained |
| 7–8   | Majority wave trained | Improved tool set deployed | Majority wave certification | Coaching cadence running |
| 9–10  | Laggard wave prep | Full tool library | Laggard wave support | Anti-pattern corrections |
| 11–12 | Laggard wave trained | Tool adoption at 80% | 80% certified | Manager performance reviews updated |

## 12-Month Milestones
- Month 2: Readiness audit complete; pilot cohort defined
- Month 4: Pilot wave trained and certified; leading metrics baselined
- Month 6: Pilot post-mortem; majority wave launch decision
- Month 8: Majority wave certified; adoption plateau analysis
- Month 10: Laggard wave active; attrition pattern clear; backfill in progress
- Month 12: 80% adoption achieved; non-adopter policy enforced; program review
```

---

## Self-Check Before Delivering

Verify the rollout plan includes:

- [ ] Challenger identification was diagnostic-based, not manager nomination
- [ ] Pilot uses all four Grainger questions with specific answers
- [ ] Adoption waves are sequenced early adopters → majority → laggards → naysayers
- [ ] 80% adoption target is explicit (not 100%)
- [ ] 20–30% attrition expectation is documented with redeployment options and backfill timeline
- [ ] All four workstreams run in parallel (no sequential ordering)
- [ ] Training effectiveness triad is addressed: pre-training buzz, safe practice, behavioral certification
- [ ] Proximity rule applied: peer success stories, not star stories, for majority and laggard waves
- [ ] Lone Wolf warning is addressed: verify the model being scaled is Challenger-profile behaviors, not Lone Wolf behaviors

---

## References

- [Parallel-Track Workstream Detail + Training Effectiveness Triad](references/parallel-track-workstreams.md)
- Prerequisite: `classify-rep-profile` — produces team rep-profile distribution required for Step 1
- Prerequisite: `diagnose-manager-effectiveness` — produces manager coaching baseline required for Track 4
- Related: `coach-rep-with-pause-framework` — for individual rep coaching sessions during the rollout

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

This skill depends on:

- `classify-rep-profile` — produces the rep-profile distribution this skill consumes
- `diagnose-manager-effectiveness` — produces manager diagnoses this skill uses to plan the manager-enablement workstream

Related skill for individual coaching during the rollout: `coach-rep-with-pause-framework`.
