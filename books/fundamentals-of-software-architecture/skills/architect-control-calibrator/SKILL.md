---
name: architect-control-calibrator
description: Determine the appropriate level of architect control over a development team using a quantitative 5-factor scoring model (-100 to +100 scale). Use this skill whenever the user asks how much they should be involved in a team's decisions, how hands-on or hands-off to be as an architect, how to calibrate their leadership style, whether they are micromanaging developers, whether they should give the team more autonomy, or any question about architect involvement level, team oversight, or technical leadership balance — even if they don't explicitly say "control." Also triggers when the user describes team dysfunction symptoms like merge conflicts increasing, nobody speaking up in meetings, or tasks falling through cracks.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architect-control-calibrator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [22]
tags: [software-architecture, architecture, leadership, team-management, control, elastic-leadership]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "Team and project context from the user — team size, experience, familiarity, project complexity and duration"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. No codebase required."
---

# Architect Control Calibrator

## When to Use

You need to determine how much hands-on control an architect should exercise over a development team. Typical triggers:

- The user is a new architect joining an existing team and wants to know how involved to be
- The user is wondering if they are micromanaging or under-managing their team
- The user describes team problems (merge conflicts, silence in reviews, dropped tasks) and wants guidance
- The user is starting a new project and needs to set the right leadership posture
- The user asks about "elastic leadership" or calibrating their architect involvement

Before starting, verify:
- Is there a team to assess? (At minimum, team size and general experience level)
- Is there a project context? (Complexity and expected duration)

## Context

### Required Context (must have before proceeding)

- **Team size:** How many developers on the team?
  -> Check prompt for: numbers, team descriptions, "my team of N"
  -> If still missing, ask: "How many developers are on the team?"

- **Team experience level:** Are they mostly junior, mid-level, or senior?
  -> Check prompt for: "junior," "senior," "experienced," "fresh out of college," years of experience
  -> If still missing, ask: "What is the overall experience level of the team — mostly junior, mid-level, or senior?"

### Observable Context (gather from environment if available)

- **Team familiarity:** How long has the team worked together?
  -> Check prompt for: "new team," "worked together for X years," "just formed"
  -> If unavailable: assume moderate familiarity (score 0)

- **Project complexity:** How complex is the system being built?
  -> Check prompt for: "distributed," "microservices," "simple CRUD," "complex," architecture descriptions
  -> If unavailable: assume moderate complexity (score 0)

- **Project duration:** How long is the project expected to last?
  -> Check prompt for: months, years, timeline references
  -> If unavailable: assume moderate duration (score 0)

- **Team dysfunction signals:** Are there signs of process loss, pluralistic ignorance, or diffusion of responsibility?
  -> Check prompt for: merge conflicts, silence in meetings, dropped tasks, nobody speaking up
  -> If present: flag and address in output

### Default Assumptions

- If team familiarity unknown -> score 0 (moderate) and note the assumption
- If project complexity unknown -> score 0 (moderate) and note the assumption
- If project duration unknown -> score 0 (moderate) and note the assumption
- If experience level is "mixed" -> score 0 (moderate), but note that mixed teams often need more guidance than the score suggests

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Team size is known
- Team experience level is known or can be inferred
- At least 1 other factor (familiarity, complexity, duration) is known

PROCEED WITH DEFAULTS when:
- Team size and experience are known
- Other factors can use moderate defaults
- Team dysfunction signals can be assessed from context

MUST ASK when:
- Team size is completely unknown (cannot calibrate without it)
- Experience level is unknown AND cannot be inferred from context
```

## Process

### Step 1: Score Each Factor

**ACTION:** Score each of the five control factors on a scale from -20 to +20. Use the scoring guide below. For detailed breakdowns with intermediate values, see [references/control-scoring-guide.md](references/control-scoring-guide.md).

**WHY:** Each factor independently influences how much architect control is appropriate. Scoring them separately prevents one dominant factor from masking others. A senior team working on a complex project needs different handling than a junior team on a simple one — the individual factor scores reveal this nuance.

| Factor | -20 (less control) | 0 (moderate) | +20 (more control) |
|--------|-------------------|--------------|-------------------|
| **Team familiarity** | Established team, worked together 2+ years | Some familiarity, 6-12 months | Brand new team, never worked together |
| **Team size** | Small (4 or fewer) | Medium (5-9) | Large (12+) |
| **Overall experience** | Mostly senior (8+ years) | Mixed or mid-level | Mostly junior (0-2 years) |
| **Project complexity** | Simple (CRUD, well-understood domain) | Moderate | Highly complex (distributed, novel domain) |
| **Project duration** | Short (< 3 months) | Medium (3-12 months) | Long (> 18 months) |

**IF** a factor is unknown -> score 0 and note the assumption
**IF** a factor falls between values -> interpolate (e.g., team of 10 is between medium and large, score +10)

### Step 2: Calculate Total Score

**ACTION:** Sum all five factor scores to get the total control score (range: -100 to +100).

**WHY:** The total determines the overall control posture. Individual scores matter for understanding WHY the total is what it is, but the total drives the primary recommendation. The scale is intentionally symmetrical — neither extreme is inherently better. The right level depends entirely on context.

Interpret the total:
- **+60 to +100:** High control — Be very hands-on. Attend stand-ups, review all major technical decisions, pair-program on critical paths, create detailed technical guidance. This is NOT micromanaging — the team needs this level of support.
- **+20 to +59:** Moderate-high control — Attend key meetings, review architecture-impacting decisions, provide templates and patterns, check in regularly but don't dictate implementation details.
- **-19 to +19:** Balanced — Facilitate rather than direct. Set architecture boundaries, let the team decide implementation. Be available for guidance. This is the "effective architect" zone.
- **-59 to -20:** Moderate-low control — Focus on high-level guardrails only. Trust the team to make most technical decisions. Intervene only when architecture principles are at risk.
- **-100 to -60:** Low control — Be a strategic advisor. Set vision and principles, then step back. The team is capable and cohesive. Over-involvement will frustrate them and slow them down.

### Step 3: Check for Architect Personality Anti-Patterns

**ACTION:** Based on the total score and the user's described behavior, check whether the architect is falling into a personality anti-pattern.

**WHY:** The two extremes of the control spectrum represent well-known anti-patterns. An architect at +80 who is also over-controlling on a team that doesn't need it is a Control Freak. An architect at -80 who is also absent from a team that needs guidance is an Armchair Architect. The score tells you what SHOULD be, but the user's described behavior might not match.

**Control Freak Architect** (too much control for the context):
- Dictates class designs and design patterns to developers
- Restricts use of any external libraries without approval
- Writes pseudocode for the development team
- Makes implementation-level decisions that should belong to developers
- **Root cause:** Steals the art of programming, causes frustration and turnover
- **Correction:** Focus on component-level architecture, not implementation details

**Armchair Architect** (too little control for the context):
- Architecture diagrams are too high-level to be actionable
- Doesn't understand the technology stack the team is using
- Moves between projects without staying for implementation
- No regular time spent with the development team
- **Root cause:** Disconnected from reality, team left to figure things out alone
- **Correction:** Stay involved through implementation, spend time with the team

**IF** the user describes behavior matching a personality anti-pattern AND the score supports it -> flag the anti-pattern and provide specific correction steps
**IF** the behavior doesn't match the score -> the score may indicate they should adjust

### Step 4: Scan for Team Warning Signs

**ACTION:** Check the user's description for three critical team dysfunction signals. These indicate the team may be too large or that control needs recalibration regardless of the score.

**WHY:** These warning signs override the numerical score. A team scoring -40 (experienced, established) can still exhibit dysfunction that requires immediate architect intervention. Detecting these signs early prevents project failure.

**Process Loss (Brook's Law):**
- **Signal:** Merge conflicts have increased, developers stepping on each other's code, adding people hasn't improved velocity
- **Root cause:** Too many people working in overlapping areas
- **Response:** Look for areas of parallelism. Move developers to parallel tracks where they won't conflict. Consider splitting the team.

**Pluralistic Ignorance:**
- **Signal:** Team agrees publicly with decisions but complains privately. Nobody raises concerns in architecture reviews. Silence during design discussions.
- **Root cause:** Social pressure to conform. Team members privately disagree but assume everyone else agrees.
- **Response:** Observe body language during meetings. Directly ask quieter members for their opinion. Create anonymous feedback channels. As the architect, act as a facilitator who draws out dissent.

**Diffusion of Responsibility:**
- **Signal:** Tasks get dropped because everyone assumes someone else will do it. Unclear ownership. "I thought you were handling that."
- **Root cause:** Accountability gaps that grow with team size. The larger the team, the easier it is for individuals to assume someone else is responsible.
- **Response:** Assign explicit owners to every task and architecture concern. Question whether new team members are actually needed. Reduce team size if possible.

**IF** warning signs are detected -> include them in the output with specific remediation steps
**IF** no warning signs mentioned -> note that the architect should monitor for these throughout the project

### Step 5: Generate Recommendations

**ACTION:** Produce a calibrated recommendation with specific behaviors the architect should adopt at the determined control level. Include what to do, what NOT to do, and when to recalibrate.

**WHY:** A number alone isn't actionable. The architect needs specific guidance on behaviors: which meetings to attend, what decisions to own vs delegate, how to provide guidance without over-controlling. The recommendation must be concrete enough to change behavior on Monday morning.

Include:
1. **Control posture summary** — one-sentence description of the recommended level
2. **Specific behaviors to adopt** — 4-6 concrete actions at this control level
3. **Specific behaviors to avoid** — 3-4 things NOT to do (the anti-pattern behaviors for this level)
4. **Recalibration triggers** — when to re-score (team membership changes, project phase shifts, complexity changes)
5. **Warning sign monitoring** — which dysfunction signals to watch for given the team profile

## Inputs

- Team description (size, experience, familiarity)
- Project description (complexity, duration, technology)
- Optionally: current architect behavior, team dynamics observations, specific concerns

## Outputs

### Architect Control Calibration Report

```markdown
# Architect Control Calibration

## Team & Project Profile
- **Team size:** {N developers}
- **Team familiarity:** {description}
- **Overall experience:** {description}
- **Project complexity:** {description}
- **Project duration:** {description}

## Control Score

| Factor | Score | Rationale |
|--------|-------|-----------|
| Team familiarity | {-20 to +20} | {why this score} |
| Team size | {-20 to +20} | {why this score} |
| Overall experience | {-20 to +20} | {why this score} |
| Project complexity | {-20 to +20} | {why this score} |
| Project duration | {-20 to +20} | {why this score} |
| **Total** | **{-100 to +100}** | |

## Control Level: {High/Moderate-High/Balanced/Moderate-Low/Low}

{One-sentence summary of recommended posture}

## Recommended Behaviors

### DO:
1. {specific action}
2. {specific action}
...

### DON'T:
1. {specific anti-pattern to avoid}
2. {specific anti-pattern to avoid}
...

## Team Health Assessment

{Warning signs detected or "No warning signs detected — monitor for: ..."}

## When to Recalibrate

- {trigger 1}
- {trigger 2}
- {trigger 3}
```

## Key Principles

- **Control is not inherently good or bad** — Too much control on a senior, established team suffocates them. Too little control on a junior, new team leaves them floundering. The right level is determined by context, not by ideology. An architect who always defaults to high control or always defaults to low control is failing to read the room.

- **The score is a starting point, not a verdict** — The 5-factor model provides an objective baseline, but real teams are messier than any model. Use the score to check your instincts. If your gut says "more control" but the score says "less," one of you is wrong — investigate which.

- **Re-evaluate throughout the project lifecycle** — A team that starts at +60 (new team, complex project) may shift to -20 six months later as familiarity grows and complexity becomes understood. The factors are not static. Set a calendar reminder to re-score quarterly.

- **Watch for warning signs regardless of score** — Process loss, pluralistic ignorance, and diffusion of responsibility can appear at any control level. A score of -60 doesn't mean "ignore the team." It means "facilitate rather than direct" — but still observe, still engage, still monitor.

- **Architect personality anti-patterns are the real danger** — The biggest risk is not getting the score wrong. It's letting your natural personality override the score. Control Freaks will over-control even when the score says back off. Armchair Architects will under-engage even when the score says step up. Know your tendency and actively counter it.

- **Team size is a leading indicator** — When a team exceeds 10-12 developers, warning signs almost always appear. Process loss scales non-linearly with team size. If the team is large and there are no warning signs, either you're not looking hard enough or the team is exceptionally well-organized.

## Examples

**Scenario: New architect joining an established senior team**
Trigger: "I'm a new architect joining a team of 20 developers. They've been working together for 3 years on a complex distributed system. Most are senior engineers. The project is expected to last 2 more years."
Process: Scored factors: team familiarity -20 (established 3+ years), team size +20 (20 developers, very large), overall experience -20 (mostly senior), project complexity +20 (complex distributed), project duration +15 (2 more years, long). Total: +15 (balanced). However, flagged team size as a major concern — 20 developers is well above the threshold where process loss appears. Checked for warning signs: with 20 developers on a distributed system, process loss is almost certain. Recommended balanced approach with strong emphasis on monitoring warning signs and potentially recommending team splits. Anti-pattern check: the new architect may be tempted toward Armchair Architect with such a senior team, but the large size and complexity demand active presence.
Output: Control calibration report showing +15 (balanced) with warning about team size and specific monitoring plan for process loss.

**Scenario: Leading a junior team on a simple project**
Trigger: "I'm leading a team of 6 junior developers fresh out of college. We're building a simple internal CRUD tool that should take about 3 months. They've never worked together before."
Process: Scored factors: team familiarity +20 (brand new team), team size -10 (6 is small-to-medium), overall experience +20 (all junior), project complexity -15 (simple CRUD), project duration -15 (3 months). Total: 0 (balanced). Despite the balanced score, noted that two factors are at maximum (+20): familiarity and experience. This means the architect should lean toward more guidance on team process and technical mentoring, even though the simple project and short duration pull the score down. Recommended attending daily stand-ups for the first month, providing coding standards and review templates, but NOT dictating implementation details.
Output: Control calibration report showing 0 (balanced) with nuance that mentoring is critical for this team profile.

**Scenario: Team showing dysfunction warning signs**
Trigger: "I'm the architect for a team of 12 mid-level developers. We're 6 months into a complex microservices migration. Merge conflicts have tripled in the last month, and in our last architecture review, nobody raised any concerns even though I know there are issues."
Process: Scored factors: team familiarity 0 (assumed moderate, not specified), team size +15 (12 is large), overall experience 0 (mid-level), project complexity +20 (complex microservices migration), project duration +10 (assumed 12-18 months for migration). Total: +45 (moderate-high control). But the critical finding was two warning signs: process loss (tripled merge conflicts = developers stepping on each other's code) and pluralistic ignorance (silence in architecture reviews = false consensus). Recommended immediate interventions: for process loss, identify overlapping work areas and assign clear service ownership boundaries; for pluralistic ignorance, switch to 1-on-1 architecture discussions and create anonymous concern channels. Score says moderate-high control, and the warning signs confirm the team needs MORE architect involvement, not less.
Output: Control calibration report showing +45 (moderate-high) with urgent team health alerts for process loss and pluralistic ignorance, including specific remediation steps.

## References

- For detailed factor scoring with intermediate values and worked examples, see [references/control-scoring-guide.md](references/control-scoring-guide.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
