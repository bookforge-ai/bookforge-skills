# Architect Control Calibration

## Team & Project Profile
- **Team size:** 6 junior developers
- **Team familiarity:** Brand new team, never worked together before
- **Overall experience:** All junior, fresh out of college (0-1 years experience)
- **Project complexity:** Simple internal CRUD tool
- **Project duration:** 3 months (short)

## Control Score

| Factor | Score | Rationale |
|--------|-------|-----------|
| Team familiarity | +20 | Brand new team with zero working history together. They have no established norms, communication patterns, or trust. They need help building these from scratch. |
| Team size | -10 | 6 developers is small-to-medium. Small enough to avoid major coordination overhead, but not tiny. Somewhere between the -20 (4 or fewer) and 0 (5-9) range. |
| Overall experience | +20 | All junior developers fresh out of college. Maximum score — they lack professional experience, architecture intuition, and likely haven't worked on production systems. They need significant guidance on practices, patterns, and professional norms. |
| Project complexity | -15 | Simple internal CRUD tool. Well-understood domain with established patterns. Low architectural risk — a wrong decision is easy to correct. |
| Project duration | -15 | 3 months is short. Limited time for architectural drift or major scope changes. The short timeline also limits the damage of any poor decisions. |
| **Total** | **0** | |

## Control Level: Balanced

The total score lands exactly at zero — balanced. But this number hides important nuance. Two factors are at maximum (+20): team familiarity and experience. The team is simultaneously brand new AND entirely junior. The simple project and short duration pull the score down, but the human factors demand attention.

**Critical nuance:** The risk here is not architectural failure — a CRUD tool has limited architectural risk. The risk is team dysfunction. Six people who have never worked together and have never worked professionally need help with process, communication, and professional development far more than they need help with technical decisions.

## Recommended Behaviors

### DO:
1. **Attend daily stand-ups for the first month.** Not to gatekeep — to model how professional communication works. Transition to every-other-day by month 2 if the team is functioning well.
2. **Provide coding standards and code review templates upfront.** Junior developers need guardrails. Don't wait for bad habits to form — establish expectations from day one. Include naming conventions, PR size expectations, and review checklists.
3. **Pair-program on the initial architecture setup.** Set up the project structure, database schema design, and API patterns WITH the team, not FOR them. Walk through WHY each decision is made so they learn the reasoning.
4. **Assign a simple task to each developer in the first week.** New teams with new developers freeze if the first task is too big. Give them something achievable to build confidence and establish working rhythm.
5. **Run a lightweight architecture review at the 1-month mark.** Check whether the initial patterns are being followed or if drift has occurred. Use this as a teaching moment, not a criticism session.
6. **Create explicit ownership for each module or feature area.** With 6 juniors, diffusion of responsibility is a risk. Make sure each person knows exactly what they own.

### DON'T:
1. **Don't dictate implementation details line by line.** Even though they're junior, they need to learn by doing. Over-prescribing robs them of learning opportunities and creates dependency on you. Guide on WHAT patterns to use, not HOW to write every function.
2. **Don't assume silence means understanding.** Junior developers often won't ask questions because they don't know what to ask. Proactively check comprehension: "Can you explain back to me how the data flows through this endpoint?"
3. **Don't over-architect the solution.** A 3-month CRUD tool does not need microservices, event sourcing, or CQRS. Keep the architecture simple and let the team focus on learning professional fundamentals.
4. **Don't treat this like a senior team.** A balanced score of 0 might tempt you to take a hands-off "facilitate" approach. But the +20 on experience and +20 on familiarity mean this team needs active mentoring, not just facilitation.

## Team Health Assessment

**Process Loss: LOW RISK**
With 6 developers on a simple CRUD tool, there are only 15 communication channels. Process loss is unlikely unless work areas overlap significantly. Monitor merge conflicts but don't expect major issues.

**Pluralistic Ignorance: MODERATE RISK**
Junior developers are especially susceptible to pluralistic ignorance. They may agree with your architectural decisions not because they understand them, but because they assume you must be right. Actively solicit questions and disagreement. Create a psychologically safe environment where "I don't understand" is welcomed.

**Diffusion of Responsibility: MODERATE RISK**
With all-junior developers, nobody may feel confident enough to take ownership of difficult tasks. Tasks might languish with "I thought someone more experienced would handle that" — but there IS no one more experienced. Assign explicit owners and check progress frequently.

## Architect Personality Anti-Pattern Check

With a team of all-junior developers, the **Control Freak** anti-pattern is the primary risk. It's tempting to over-prescribe when you see junior developers making mistakes. Remember: they learn more from making and fixing mistakes than from being told the right answer. Your job is to set guardrails wide enough for learning but narrow enough to prevent project-threatening errors.

The **Armchair Architect** anti-pattern is also possible if you dismiss the project as "just a CRUD tool" and disengage. Even simple projects fail when the team has no experience working together or building production software.

## When to Recalibrate

- **After the first 2 weeks:** Re-assess team familiarity. If the team gels quickly, you can reduce involvement sooner.
- **At the 1-month mark:** The team should be settling into patterns. If they're functioning well, shift from daily to weekly check-ins.
- **If any developer is struggling significantly:** May need targeted pairing rather than broad control changes.
- **If scope changes:** A CRUD tool that suddenly needs to integrate with external systems or handle complex workflows changes the complexity factor.
