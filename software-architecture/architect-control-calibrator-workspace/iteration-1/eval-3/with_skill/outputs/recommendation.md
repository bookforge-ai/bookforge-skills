# Architect Control Calibration

## Team & Project Profile
- **Team size:** 12 mid-level developers
- **Team familiarity:** Not explicitly stated — assumed moderate (6+ months into the project together)
- **Overall experience:** Mid-level developers
- **Project complexity:** Complex microservices migration
- **Project duration:** Estimated 12-18 months total for a migration of this nature (currently 6 months in)

## Control Score

| Factor | Score | Rationale |
|--------|-------|-----------|
| Team familiarity | -5 | The team has been working together for at least 6 months on this project. Some familiarity has developed, but a migration project often involves shifting responsibilities as services are carved out, which disrupts established patterns. Slightly below moderate. |
| Team size | +15 | 12 developers is above the 10-12 threshold where process loss becomes highly probable. With 12 people, there are 66 communication channels (12*11/2). This is large enough to cause significant coordination overhead, especially during a migration where boundaries are shifting. |
| Overall experience | 0 | Mid-level developers — they have professional experience and can work independently, but may lack the architectural judgment to navigate complex trade-offs in a migration without guidance. |
| Project complexity | +20 | Complex microservices migration is near the maximum complexity. Migrating from a monolith (or different architecture) to microservices involves service boundary decisions, data ownership splits, inter-service communication patterns, and the risk of creating a distributed monolith. Every decision has cascading consequences. |
| Project duration | +10 | Estimated 12-18 months total. At 6 months in, there's still a significant runway where architectural drift can compound. Migration projects often extend beyond initial estimates. |
| **Total** | **+40** | |

## Control Level: Moderate-High

You should be exercising significant architectural control. Attend key meetings, review all architecture-impacting decisions, provide templates and patterns for service decomposition, and check in regularly. You are NOT in a "sit back and observe" zone — the team needs your active guidance.

**Critical nuance:** The score says +40, but the warning signs you described push this even higher. The tripled merge conflicts and silence in architecture reviews are not normal — they indicate active dysfunction that requires immediate intervention beyond what the score alone suggests.

## Recommended Behaviors

### DO:
1. **Immediately investigate the merge conflict explosion.** Tripled merge conflicts in one month is a process loss signal. Identify which files and services are seeing the conflicts. You will likely find that multiple developers are working in overlapping areas without clear ownership boundaries. Map out who is working on what and create explicit service ownership assignments.
2. **Switch architecture reviews from group to small-group or 1-on-1 format.** With 12 people in a room, pluralistic ignorance is expected. Nobody speaks up because everyone assumes everyone else agrees. Pull aside 2-3 developers you trust and ask them directly: "What concerns do you have about the migration that you haven't raised?" You will almost certainly hear issues that were invisible in group settings.
3. **Create and enforce a service ownership map.** Each microservice (existing and planned) should have exactly one owner and one backup. No shared ownership. This directly combats both process loss (reduces overlap) and diffusion of responsibility (creates accountability).
4. **Review all service boundary decisions personally.** In a microservices migration, the most expensive mistakes are wrong service boundaries. These are almost impossible to fix later. This is the architect's #1 job right now.
5. **Establish a weekly "migration health" check.** Track: merge conflict count, number of services in flight, deployment frequency, and inter-service dependency count. These metrics will tell you if the migration is going well before subjective opinions do.
6. **Create anonymous feedback channels.** If people aren't speaking up in reviews, give them a safe way to raise concerns. A simple anonymous form asking "What is the biggest risk in our migration right now?" will surface honest answers.

### DON'T:
1. **Don't assume the silence means things are fine.** This is the most dangerous interpretation. The silence IS the problem. Twelve mid-level developers on a complex migration WILL have concerns. If they're not voicing them, the communication channel is broken, not the team's satisfaction.
2. **Don't respond to merge conflicts by adding process (more reviews, more approvals).** The root cause is overlapping work areas, not insufficient review. Adding process will slow the team down without fixing the underlying structural issue.
3. **Don't try to solve this by adding more developers.** Brook's Law applies directly here. More people = more communication channels = more coordination overhead. If anything, consider whether 12 is already too many for this phase of the migration.
4. **Don't wait to see if it resolves itself.** Tripled merge conflicts and silent reviews are escalating symptoms. They will get worse, not better, without intervention. Act this week.

## Team Health Assessment

### Process Loss: ACTIVE (URGENT)

**Evidence:** Merge conflicts have tripled in the last month.

This is a textbook process loss signal. With 12 developers and 66 communication channels, developers are stepping on each other's code. In a microservices migration, this often happens when:
- Multiple developers are modifying the monolith's shared code as they extract services
- Service boundaries aren't clearly defined, so developers are working in the same areas
- The "seam" between old and new architecture is a high-contention zone

**Immediate remediation:**
1. Map every active work stream to a specific developer or pair
2. Identify the 3-5 files/areas with the most merge conflicts
3. Assign exclusive ownership of those areas — only the owner modifies them
4. Consider splitting extraction work so that only one service is being carved out at a time from any given code area
5. If parallel extraction is necessary, define explicit interfaces between the extraction teams BEFORE they start coding

### Pluralistic Ignorance: ACTIVE (URGENT)

**Evidence:** Nobody raised concerns in the last architecture review despite known issues.

This means the team is making decisions without genuine consensus. Developers privately disagree but publicly go along with it. This is especially dangerous in a migration because:
- Wrong service boundaries get locked in without pushback
- Technical debt accumulates as developers silently implement workarounds for architecture decisions they disagree with
- The architect (you) gets a false sense that the migration is on track

**Immediate remediation:**
1. Cancel the next large-group architecture review. Replace it with 3-4 small-group sessions (3-4 people each)
2. In each session, explicitly ask: "What would you change about our current migration approach if you could?"
3. Implement an anonymous concern channel (Google Form, Slack bot, whatever is lowest-friction)
4. In future reviews, use a "pre-mortem" exercise: "Imagine this migration has failed in 6 months. What went wrong?" This reframes criticism as helpful foresight rather than dissent

### Diffusion of Responsibility: MODERATE RISK

**Evidence:** Not directly observed, but with 12 developers and the above two signals active, diffusion of responsibility is likely present.

**Monitoring:** Watch for:
- Cross-cutting concerns (logging, monitoring, authentication) that nobody owns
- Integration testing gaps ("I thought the other team was testing that")
- Documentation of service contracts falling behind

## Architect Personality Anti-Pattern Check

You should be worried — and the fact that you're asking the question suggests you're paying attention. The risk for your situation is NOT being too hands-on (Control Freak) — it's being too reactive. The warning signs have been building, and a moderate-high control posture means you should have been actively monitoring for exactly these signals.

Going forward, lean into the role. At +40 with active warning signs, you should be one of the most visible people on this team. Not dictating code — but owning architecture decisions, facilitating honest discussion, and restructuring work to eliminate the overlap causing merge conflicts.

## When to Recalibrate

- **After implementing the remediation steps above (2-3 weeks):** Check if merge conflicts have decreased and if team members are speaking up in smaller sessions. If yes, you may be able to ease back slightly.
- **When the migration passes the 50% mark:** The nature of the work changes. Early migration is about decomposition (high complexity). Later migration is about optimization and stabilization (lower complexity). Re-score project complexity.
- **If the team loses or gains members:** Any team membership change at this size disrupts familiarity and ownership. Re-score immediately.
- **If the merge conflict trend reverses:** A sustained drop in merge conflicts means your structural changes are working. Consider reducing involvement in day-to-day coordination.
- **Quarterly regardless:** Set a recurring calendar event.
