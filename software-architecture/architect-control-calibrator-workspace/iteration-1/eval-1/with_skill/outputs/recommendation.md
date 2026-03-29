# Architect Control Calibration

## Team & Project Profile
- **Team size:** 20 developers
- **Team familiarity:** Established team, worked together for 3 years
- **Overall experience:** Mostly senior engineers
- **Project complexity:** Complex distributed system
- **Project duration:** 2 more years remaining

## Control Score

| Factor | Score | Rationale |
|--------|-------|-----------|
| Team familiarity | -20 | The team has worked together for 3 years — deeply established norms, trust, and communication patterns. They know how to collaborate without external orchestration. |
| Team size | +20 | 20 developers is well above the 12+ threshold. With 20 people, there are 190 communication channels (n*(n-1)/2 = 20*19/2). This is the single biggest risk factor. |
| Overall experience | -20 | Mostly senior engineers with deep expertise. They can identify architecture violations themselves and make sound technical decisions independently. |
| Project complexity | +20 | Complex distributed system — architectural decisions have far-reaching consequences across service boundaries. Wrong choices are expensive to unwind. |
| Project duration | +15 | 2 more years is a long remaining timeline. Sufficient time for architectural drift, team turnover, and requirement evolution. Active governance needed. |
| **Total** | **+15** | |

## Control Level: Balanced

You are in the "effective architect" zone. The team's seniority and established familiarity pull strongly toward hands-off, but the massive team size and system complexity pull equally toward hands-on. The result is a balanced posture — but one that requires nuance.

**Critical nuance:** Your biggest risk is NOT the architecture. Your biggest risk is the team size. At 20 developers, process loss is almost certain. Even though the team is senior and established, 190 communication channels create coordination overhead that no amount of individual skill can overcome.

## Recommended Behaviors

### DO:
1. **Focus on team structure, not technical direction.** With 20 senior developers, you add more value by optimizing HOW they collaborate than by telling them WHAT to build. Consider proposing sub-team boundaries aligned with service boundaries.
2. **Attend architecture sync meetings weekly.** Not daily stand-ups — the team doesn't need that. But weekly architecture syncs let you monitor cross-team dependencies and prevent architectural drift.
3. **Own the cross-service integration decisions.** Individual services can be delegated to senior leads. But decisions that span services (communication protocols, shared data schemas, API contracts) need your coordination.
4. **Monitor merge conflict frequency.** With 20 developers on a distributed system, this is your leading indicator for process loss. If merge conflicts are rising, the team structure needs adjusting before the architecture does.
5. **Build relationships before making changes.** You are new to this team. They have 3 years of established norms. Spend the first 2-4 weeks listening and understanding their architecture decisions before suggesting changes.
6. **Establish quarterly re-calibration.** With a 2-year remaining timeline, recalculate this score every quarter as you learn the team dynamics.

### DON'T:
1. **Don't dictate implementation details.** These are senior engineers. Telling them which design patterns to use or how to structure their classes will frustrate them and undermine your credibility as a new member.
2. **Don't ignore the team size problem.** A score of +15 might tempt you to take a hands-off approach. But the +20 on team size is a red flag. 20 developers almost always need sub-team restructuring.
3. **Don't assume silence means agreement.** With 20 people in a meeting, pluralistic ignorance is a real risk. If nobody pushes back on your architecture proposals, it doesn't mean they agree — it means the group is too large for honest dissent.
4. **Don't try to review every decision.** You will become a bottleneck. Focus on architecture-impacting decisions only.

## Team Health Assessment

**Process Loss: HIGH RISK**
With 20 developers, process loss is almost certain. Key indicators to monitor immediately:
- Merge conflict frequency across the codebase
- Whether adding recent team members improved or decreased velocity
- Whether developers are stepping on each other's code in the same service areas

**Recommended action:** Investigate whether the 20 developers are already informally organized into sub-teams. If not, propose formal sub-teams of 4-6 aligned with service boundaries. Each sub-team gets a senior tech lead who handles implementation decisions within that service.

**Pluralistic Ignorance: MODERATE RISK**
With 20 people in meetings, individuals are less likely to speak up. Watch for:
- Silence during architecture reviews (especially from developers you know have opinions)
- Team members complaining privately about decisions they agreed to publicly
- "Emperor's new clothes" dynamics where obvious problems go unmentioned

**Recommended action:** Use smaller breakout groups for architecture discussions. 1-on-1s with key senior engineers will surface honest opinions that group settings suppress.

**Diffusion of Responsibility: MODERATE RISK**
At 20 developers, ownership boundaries can blur. Watch for:
- Tasks falling through cracks with "I thought someone else was handling that"
- Unclear ownership of cross-cutting concerns (logging, monitoring, error handling)
- Junior-level tasks not getting done because everyone assumes a more junior person will do them (but the team is mostly senior)

**Recommended action:** Ensure every service, every cross-cutting concern, and every architectural initiative has a named owner — not a team, a person.

## Architect Personality Anti-Pattern Check

As a new architect joining an established senior team, you are at risk of the **Armchair Architect** anti-pattern — being too hands-off because the team is senior and "doesn't need you." They don't need you for implementation decisions, but they DO need you for:
- Cross-service coordination (which gets harder with 20 people)
- Architectural governance over a 2-year timeline
- Team structure optimization to combat process loss

Don't mistake "senior team" for "team that doesn't need an architect."

## When to Recalibrate

- **After your first month:** Once you understand the team dynamics, re-score familiarity and complexity based on reality rather than description
- **If the team is restructured into sub-teams:** This changes the effective team size factor dramatically
- **If team members leave or join:** Changes familiarity and experience mix
- **Every quarter:** On a 2-year timeline, factors will shift as the project matures
- **If warning signs escalate:** Process loss or pluralistic ignorance becoming visible should trigger an immediate re-scoring with more control
