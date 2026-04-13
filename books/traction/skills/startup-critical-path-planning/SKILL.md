---
name: startup-critical-path-planning
description: "Guide a startup to set a single quantified traction goal and define the critical path of milestones to reach it. Use whenever a founder needs to prioritize activities, set growth goals, define milestones, decide what NOT to work on, plan quarterly/yearly execution, cascade goals to teams, escape the 'too many things to do' trap, or apply a binary on-path/off-path filter to proposed work. Activates on phrases like 'traction goal', 'critical path', 'what should we focus on', 'too many priorities', 'prioritization', 'milestones', 'quarterly planning', 'yearly goals', 'OKRs', 'where should I spend my time', 'what NOT to do', 'company planning', 'goal setting', 'DuckDuckGo', 'roadmap'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/startup-critical-path-planning
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [6]
domain: startup-growth
tags: [startup-growth, goal-setting, milestone-planning, startup-execution, prioritization]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Company state, candidate milestones, resource constraints, proposed work items"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for critical path document"
discovery:
  goal: "Produce a written critical path with one traction goal, ordered necessary milestones, and an exclusion log"
  tasks:
    - "Define one specific quantified traction goal"
    - "Enumerate every milestone that might be necessary"
    - "Ruthlessly filter to only truly necessary milestones"
    - "Order milestones by dependency"
    - "Apply binary on-path/off-path filter to proposed work"
    - "Cascade company critical path to department/individual paths"
  audience:
    roles: [startup-founder, growth-marketer, head-of-marketing]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "Founder has too many priorities and can't decide what to cut"
      - "Team is busy but growth isn't happening"
      - "Planning a quarter or year of execution"
      - "Deciding whether a proposed feature/activity is worth doing"
    prerequisites: []
    not_for:
      - "User needs tactical channel advice (use bullseye-channel-selection)"
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
    eval_count: 0
    assertion_count: 11
    iterations_needed: 0
---

# Startup Critical Path Planning

## When to Use

The startup has many possible things to work on and needs a filter for deciding what actually matters. Use this skill when:

- The team is busy but growth isn't moving
- A founder says "we have too many priorities"
- Planning a quarter or year where focus is required
- Evaluating whether a specific proposed feature, hire, or activity is worth doing
- Cascading company-level goals to department or individual work

This is a plan-only skill — the output is a written critical path document, not agent-executed work.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Current company state:** stage, resources, biggest constraint
  → Check prompt for: metrics, team size, runway
  → If missing, ask: "What's your current state? Team size, runway, current metrics (users/revenue), biggest bottleneck?"

- **Candidate list of things being considered:** features, hires, activities the founder is weighing
  → Check prompt for: "we're thinking about", "might do X or Y", lists of activities
  → If missing, ask: "What's on your list of things you're considering doing? Include everything, even things you're not sure about."

### Observable Context

- **Prior goals and progress:** has the founder set goals before? How did they go?
- **Existing roadmap or planning docs:** what already exists

### Default Assumptions
- The user is over-loaded with options (the common case)
- Default goal horizon: 6-12 months
- The critical path will cut 50%+ of candidate items

### Sufficiency Threshold

```
SUFFICIENT: company state + candidate items + rough goal horizon known
PROCEED WITH DEFAULTS: company state known, infer candidates from context
MUST ASK: no company state at all
```

## Process

Use TodoWrite:
- [ ] Step 1: Define the single traction goal
- [ ] Step 2: Enumerate candidate milestones (brainstorm wide)
- [ ] Step 3: Filter to only truly necessary milestones
- [ ] Step 4: Order milestones by dependency
- [ ] Step 5: Apply binary on-path filter to ongoing work
- [ ] Step 6: Cascade to departments and individuals

### Step 1: Define the Single Traction Goal

**ACTION:** Help the user articulate ONE specific, quantified traction goal. It must:
- Be specific and measurable (1,000 paying customers, $50k MRR, 100M searches/month)
- Be time-boxed (by when)
- **Change something significant if achieved** — profitability, fundraisability, market leadership, next-phase unlock

If the user proposes multiple goals, force a choice. Multiple top-level goals is the same as no goal. Write the single goal to `critical-path.md`.

**WHY:** Without a single traction goal, every prioritization decision becomes political or vibes-based. With a single goal, every proposed activity gets a binary check: "does this help reach goal X?" Peter Drucker's version: "If you have more than three priorities, you have none." The single goal is the foundation of the entire skill.

**IF** the user can't pick one goal → ask "which of these, if achieved, would most change the trajectory of the business?" Use that.
**IF** the goal feels too ambitious → keep it. Ambition is fine. The test is whether achievement is significant, not whether it's likely.

### Step 2: Enumerate Candidate Milestones (Brainstorm Wide)

**ACTION:** Work backwards from the goal. List every milestone that might plausibly be necessary to reach it. Be generous — include product features, hires, marketing activities, partnerships, funding events, infrastructure, compliance. At this stage, include more than you need.

**WHY:** The brainstorm is explicitly wide because you can't filter what you haven't considered. A tight filter applied to a short list misses the non-obvious milestones. A tight filter applied to a long list catches what matters and cuts what doesn't.

### Step 3: Filter to Only Truly Necessary Milestones

**ACTION:** For each candidate milestone, apply this filter: **"If we skip this milestone, can we still plausibly hit the traction goal?"**

If the answer is "yes, we'd probably still hit it" → the milestone is NOT on the critical path. Move it to an **exclusion log** with a one-sentence reason.

Be ruthless. Most candidate milestones will be cut. The DuckDuckGo example: product features like images and auto-suggest were *excluded* from the critical path for Goal 2 (100M searches/month) even though users were asking for them — because they weren't strictly necessary for that specific goal. Those features came back onto the path for a later goal.

Write the filtered list to `critical-path.md` and the exclusion log to `critical-path-excluded.md`.

**WHY:** The exclusion is where the power of this framework comes from. "Necessary" is a higher bar than "useful". Many things are useful. Very few are necessary. Cutting the merely-useful is what frees resources to execute the necessary. If the exclusion log is short, you didn't cut hard enough — run the filter again.

**IF** the user resists cutting something → ask specifically: "Can we hit the goal without this?" If the answer isn't a definitive no, cut it.

### Step 4: Order Milestones by Dependency

**ACTION:** For the filtered list, identify which milestones must precede which. Build a dependency chain. The first milestone(s) in the chain are what the team should work on RIGHT NOW. Nothing else.

Prefer shortcuts: if a milestone can be satisfied by using an external provider rather than building in-house, take the shortcut. The goal is to reach the traction goal, not to build everything from scratch.

**WHY:** Dependency ordering reveals what actually has to happen first. It's common for teams to work on Milestone 5 while Milestones 1-4 are unfinished, because 5 is more interesting. Ordering forces the team to confront what's actually blocking progress.

### Step 5: Apply the Binary On-Path Filter

**ACTION:** For any ongoing work or newly proposed activity, apply the filter: **"Is this on the critical path?"** Binary answer — yes or no. If no, don't do it. Period.

This includes activities that feel productive: refactoring, technical debt, new features, exploratory research, speculative hires. If they're not on the path to the traction goal, they wait.

**WHY:** The binary filter is the forcing function. It's easy to rationalize off-path work as "important" or "strategic". The filter asks a narrower question: necessary for *this* goal, *right now*? Everything else is a distraction. DuckDuckGo's Gabriel Weinberg built DDG for 6+ years by maintaining this filter — most search startups died because they worked on everything.

**IF** an ongoing activity fails the filter → stop it. Reassign the resources to the first on-path milestone.
**IF** a proposed activity fails the filter → decline it. Queue it for after the current goal is reached.

### Step 6: Cascade to Departments and Individuals

**ACTION:** If the user has teams or direct reports, cascade the critical path down one level. Each team defines its own sub-critical-path aligned to the company goal. Each individual defines their own critical path aligned to the team goal.

Set a weekly review cadence: 1:1s and team meetings include a standing agenda item — "is the work this week on our critical path?"

**WHY:** Company-level critical paths get diluted at the department and individual level if not explicitly cascaded. The cascade ensures that what the founder calls the critical path is what each engineer, marketer, and salesperson is actually working on day-to-day. Weekly review is the accountability mechanism — if the team can't point to on-path work in a 1:1, the path isn't being followed.

## Inputs

- Current company state (metrics, team, runway, constraints)
- Candidate list of work items being considered
- Rough goal horizon (3, 6, 12 months)

## Outputs

Three markdown files:

1. **`critical-path.md`** — The single traction goal, filtered milestones in dependency order, next immediate steps
2. **`critical-path-excluded.md`** — Exclusion log of items considered but cut, with one-line reasons
3. **`critical-path-cascade.md`** *(if applicable)* — Department and individual sub-paths

## Key Principles

- **One goal, not three.** Multiple top-level goals is the same as no goal. Pick one. The one that, if achieved, changes the business trajectory most. WHY: Prioritization is impossible without a single anchor. Any decision can feel important if you're comparing it to vague multi-goal aspirations.

- **Necessary is a higher bar than useful.** Most candidate milestones are useful. Very few are necessary. The filter cuts the merely-useful. WHY: This is where the leverage is. Resources freed from useful-but-not-necessary work are what enable the necessary work to ship on time.

- **The exclusion log matters as much as the path.** Writing down what you're NOT doing, with reasons, is what prevents the cut items from creeping back in. WHY: Without the written exclusion, team members will re-propose cut items every few weeks. The log is a reference point: "we explicitly cut this for this reason."

- **Binary, not gradient.** Work is on the path or off the path. There is no "kind of on the path." Gradient evaluation produces wishy-washy prioritization. WHY: Binary forces a decision. Gradient lets people rationalize anything as "somewhat important."

- **Reassess after every milestone.** Completing a milestone changes what you know. The path that made sense at the start may not be the path from here. WHY: The critical path is not a one-time document. It's a living plan that updates with learning. Static paths become wrong as the world changes.

- **Take the shortcut.** If a milestone can be reached via an external provider, partnership, or existing tool, use that instead of building. WHY: The goal is the traction goal, not the pride of building everything yourself. Shortcuts compress time-to-goal, which is the whole point.

## Examples

**Scenario: Founder with 15 priorities**

Trigger: "We're a 6-person B2B SaaS startup, 3 months from running out of runway. Need to raise a Series A. We're working on: the new dashboard redesign, hiring a VP Marketing, a big feature release, onboarding automation, enterprise SSO, the blog we've been meaning to launch, getting on the Salesforce marketplace, rebuilding our pricing page, and a bunch of other things."

Process: (1) Goal: $30k MRR by month-end — the minimum to make an A story credible. (2) Brainstorm: all the items above plus ~8 more. (3) Filter — for each item ask "does this get us to $30k MRR this month?" Results: onboarding automation YES (converts trials faster), Salesforce marketplace MAYBE (takes too long to ship, move to exclusion), dashboard redesign NO (doesn't acquire customers), VP Marketing hire NO (won't ship this month), blog NO (too slow), pricing page NO, SSO NO (enterprise deals don't close this month). Of 15 items, only 3 survive: onboarding automation, closing 4 active trials that are on the edge, and accelerating one enterprise deal already in flight. (4) Order: close the enterprise deal first (biggest lever), accelerate trial closures, ship onboarding automation last. (5) Filter ongoing work: team was spending 40% of time on dashboard redesign — stop. Reallocate to closing the enterprise deal.

Output: `critical-path.md` with the 3 surviving items, `critical-path-excluded.md` with 12 items and reasons, immediate reallocation plan.

**Scenario: Startup 18 months in, still no focus**

Trigger: "Consumer mobile app, 18 months in, $0 revenue, $400k raised. We have a free app with 20k users. Founders disagree on whether to focus on ads, in-app purchases, or a B2B licensing deal."

Process: (1) Force one goal. Ask: "Which of these, if achieved in 6 months, would most change the trajectory?" — founders agree: first $10k MRR. (2) Brainstorm milestones for each of the 3 paths: ad-supported model, IAP, B2B licensing. (3) Filter: ad-supported model requires 500k+ users (can't hit in 6 months) → excluded. IAP requires product changes + payment infrastructure + marketing test → viable. B2B licensing requires 1 deal closure → viable and fastest. (4) Order: pursue B2B first (single deal = goal), IAP as parallel fallback. (5) Filter ongoing work: team was building ad infrastructure — stop, reassign to B2B outreach.

Output: Clear single goal, decisive cut of ad strategy, parallel B2B+IAP path with B2B as primary.

**Scenario: DuckDuckGo-style long-arc planning**

Trigger: "Privacy-focused product competing with incumbents. We have 10k users. Where do I even start with goals?"

Process: (1) Goal: specific user count that unlocks next phase — "100k monthly active users" as first goal (DDG-style cascade: product/messaging stable → break-even threshold → mainstream adoption). (2) Brainstorm all milestones that might contribute: mobile app, improved messaging, 1 piece of viral PR, API integration with a power user tool, SEO on "privacy" keywords, etc. (3) Filter: mobile app YES (retention driver), SEO on privacy keywords YES (aligned with cause), viral PR YES (one good story could 10x users), API integration MAYBE — moved to exclusion for this phase. (4) Order: SEO foundation first (slowest to compound), then PR preparation, then mobile app launch. (5) Filter proposed features: product team wants to add a new browser extension → apply filter → does this contribute to 100k MAU? Only if it ships in 3 weeks. Otherwise, exclude.

Output: Multi-goal cascade pattern inspired by DuckDuckGo's approach. One current goal with clear milestones. Features that don't serve it are explicitly excluded, reviewable at next goal transition.

## References

- For the DuckDuckGo three-goal cascade case study, see [references/duckduckgo-cascade.md](references/duckduckgo-cascade.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — The critical path's traction milestones often include channel selection
- `clawhub install bookforge-startup-traction-strategy-by-phase` — The critical path goal should match the startup's current phase
- `clawhub install bookforge-business-development-pipeline` — BD deals are frequently critical path milestones

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
