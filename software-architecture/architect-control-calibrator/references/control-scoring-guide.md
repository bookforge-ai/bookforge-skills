# Control Scoring Guide

Detailed breakdown of each factor in the 5-factor architect control model, with intermediate values and scoring rationale.

## Factor 1: Team Familiarity

How well does the team know each other? Have they worked together before?

| Score | Description | Rationale |
|-------|-------------|-----------|
| +20 | Brand new team, never worked together | No established norms, communication patterns, or trust. Architect must help set team dynamics and resolve early conflicts. |
| +10 | Partially new — some members know each other, some are new | Mixed familiarity creates subgroups. Architect helps integrate new members and ensure consistent practices. |
| 0 | Team has worked together 6-12 months | Norms are forming but not fully established. Moderate guidance still beneficial. |
| -10 | Established team, 1-2 years together | Strong norms and communication patterns. Team self-organizes effectively on most issues. |
| -20 | Long-standing team, 2+ years together | Deep trust, established conflict resolution, proven collaboration. Architect intervention in team dynamics is unnecessary and counterproductive. |

**Key insight:** Team familiarity is not about individual skill — it's about how well the group functions as a unit. A team of senior engineers who have never worked together still needs more control than a team of mid-level engineers who have been collaborating for years.

## Factor 2: Team Size

How many developers are on the team?

| Score | Description | Rationale |
|-------|-------------|-----------|
| +20 | 12+ developers | Communication paths grow quadratically (n*(n-1)/2). At 12 people, there are 66 communication channels. Process loss is almost guaranteed. |
| +10 | 10-11 developers | Approaching the danger zone. Coordination overhead is significant. Sub-teams may be forming informally. |
| 0 | 7-9 developers | Standard team size. Manageable communication paths. Can function with moderate oversight. |
| -10 | 5-6 developers | Small enough for direct communication. Low coordination overhead. Fewer opportunities for things to fall through cracks. |
| -20 | 4 or fewer developers | Minimal coordination needed. Everyone knows what everyone else is doing. Over-managing this size team is wasteful. |

**Key insight:** Team size is the most reliable predictor of process loss. The communication formula (n*(n-1)/2) means adding just 2 people to a team of 10 increases communication channels from 45 to 66 — a 47% increase. This is why architects should monitor team size as a leading indicator.

**Warning thresholds:**
- At 10+: Actively look for process loss signals
- At 15+: Strongly recommend splitting into sub-teams
- At 20+: Process loss is almost certain without sub-team structure

## Factor 3: Overall Experience

What is the general experience level of team members?

| Score | Description | Rationale |
|-------|-------------|-----------|
| +20 | Mostly junior (0-2 years experience) | Need guidance on patterns, practices, and architectural thinking. Higher risk of implementation decisions that violate architecture principles. |
| +10 | Mix leaning junior (many 1-3 years, few seniors) | Some experience but lack the pattern recognition that comes with years of practice. Need guardrails more than direction. |
| 0 | Balanced mix or mostly mid-level (3-5 years) | Capable of good implementation decisions. Need architecture context and boundaries but not hand-holding. |
| -10 | Mix leaning senior (many 5+ years, few juniors) | Strong individual contributors who can make most technical decisions independently. Over-guidance feels patronizing. |
| -20 | Mostly senior (8+ years) | Deep expertise. Can identify architecture violations themselves. Architect role shifts to facilitator and vision-setter. |

**Key insight:** Experience level determines the GRAIN of control. With junior teams, the architect defines patterns and reviews implementation. With senior teams, the architect sets principles and trusts the team to apply them. The same boundary ("use event-driven communication between these services") means different things to a junior team (needs examples, templates, code reviews) and a senior team (needs the architectural intent, figures out implementation).

## Factor 4: Project Complexity

How architecturally complex is the project?

| Score | Description | Rationale |
|-------|-------------|-----------|
| +20 | Highly complex — distributed systems, novel domain, multiple integration points, real-time requirements | Architectural decisions have far-reaching consequences. Wrong choices are expensive to fix. Architect must be deeply involved in key technical decisions. |
| +10 | Moderately complex — some distributed components, familiar domain with new requirements | Some architectural decisions are critical, others are routine. Architect focuses on high-impact areas. |
| 0 | Standard complexity — well-understood patterns, moderate integration | Architecture is largely settled. Implementation is the main challenge, not design. |
| -10 | Low complexity — straightforward CRUD, single service, well-understood domain | Few architectural decisions to make. Over-architecting is the bigger risk. |
| -20 | Simple — internal tool, prototype, proof-of-concept | Architecture is trivial. Architect involvement beyond initial setup adds no value. |

**Key insight:** Complexity determines the STAKES of control. On a simple project, a bad architectural decision has limited blast radius. On a complex distributed system, a bad decision can take months to unwind. The architect's role scales with the cost of getting architecture wrong.

## Factor 5: Project Duration

How long is the project expected to last?

| Score | Description | Rationale |
|-------|-------------|-----------|
| +20 | Long (18+ months) | More time for architectural drift, team turnover, requirement changes. Architecture must be actively governed to prevent erosion. |
| +10 | Medium-long (12-18 months) | Sufficient time for problems to accumulate. Periodic architecture reviews needed. |
| 0 | Medium (6-12 months) | Standard project lifecycle. Regular check-ins sufficient. |
| -10 | Short (3-6 months) | Limited time for architecture to drift. Initial decisions carry through to completion. |
| -20 | Very short (< 3 months) | Sprint-like intensity. Architecture is set once and executed. Extended governance adds overhead without value. |

**Key insight:** Duration determines the FREQUENCY of recalibration. Long projects need quarterly re-scoring because factors change: team members leave and join, complexity becomes better understood, the team becomes more familiar. Short projects need one calibration at the start.

## Worked Scoring Examples

### Example 1: Scores +35 (Moderate-High Control)

A fintech company is building a new payment processing platform.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Team familiarity | +10 | Team of 8 pulled from different departments. 3 know each other, 5 are new to the group. |
| Team size | 0 | 8 developers — standard size. |
| Overall experience | +10 | Mix of 3 seniors and 5 mid-levels, skewing toward less experienced for a complex domain. |
| Project complexity | +20 | Payment processing with PCI compliance, multiple external integrations, real-time reconciliation. |
| Project duration | -5 | 9 months — medium with slight short lean. |
| **Total** | **+35** | Moderate-high control. Complex domain with partially new team. |

**Recommended posture:** Attend architecture syncs and key stand-ups. Define service boundaries and integration patterns. Review all external API integration decisions. Create architecture fitness functions for PCI compliance. Trust seniors for implementation but guide the mid-level developers on patterns.

### Example 2: Scores -55 (Moderate-Low Control)

A mature DevOps team is building a new internal deployment dashboard.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Team familiarity | -20 | Team has worked together for 4 years on various internal tools. |
| Team size | -15 | 5 developers. |
| Overall experience | -15 | 4 seniors (10+ years each), 1 mid-level (4 years). |
| Project complexity | -10 | Standard web dashboard with APIs they've built before. Some new charting requirements. |
| Project duration | +5 | 15 months — longer than typical for this type of project due to phased rollout. |
| **Total** | **-55** | Moderate-low control. Experienced, established team on familiar ground. |

**Recommended posture:** Set high-level architecture direction (tech stack, deployment model, data schema approach), then step back. Monthly architecture review is sufficient. Be available for questions but don't attend daily stand-ups. Focus architect time on the phased rollout strategy, which is the one area of complexity.

## Score Interpretation Zones

```
-100 -------- -60 -------- -20 -------- +20 -------- +60 -------- +100
  |     Low     |  Mod-Low   |  Balanced  | Mod-High   |    High    |
  |             |            |            |            |            |
  | Advisor     | Guardrails | Facilitate | Guide      | Direct     |
  | Set vision  | Set bounds | Collaborate| Attend key | Attend all |
  | Step back   | Check in   | Be present | Review     | Review all |
  |             | monthly    | weekly     | decisions  | daily      |
```

## Re-scoring Triggers

Recalculate the score when any of these events occur:

1. **Team membership changes** — New members reduce familiarity; departures change experience mix
2. **Project phase transition** — Moving from design to implementation, or from implementation to maintenance
3. **Complexity revelation** — The project turns out to be more or less complex than initially estimated
4. **Warning signs appear** — Process loss, pluralistic ignorance, or diffusion of responsibility emerge
5. **Quarterly cadence** — Even without specific triggers, re-score every 3 months on long projects
