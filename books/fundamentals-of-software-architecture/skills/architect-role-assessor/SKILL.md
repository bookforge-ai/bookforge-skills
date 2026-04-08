---
name: architect-role-assessor
description: Evaluate whether a software architect is fulfilling the 8 core expectations of the role and assess their technical breadth vs depth balance using the knowledge pyramid. Use this skill whenever the user asks what a software architect should be doing, questions whether they are performing the architect role correctly, wants to assess their own or someone else's architect performance, describes symptoms of role dysfunction (spending too much time coding, not attending stakeholder meetings, only recommending technologies they know, avoiding decisions), asks about transitioning from developer to architect, or encounters the Frozen Caveman anti-pattern where past experiences irrationally drive current decisions — even if they don't explicitly say "architect role" or "expectations."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architect-role-assessor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [1, 2]
tags: [software-architecture, architecture, role-definition, career, leadership, technical-breadth, self-assessment]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: none
      description: "Current architect behavior and concerns from the user — what they spend time on, what challenges they face, how they interact with teams and stakeholders"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. No codebase required."
---

# Architect Role Assessor

## When to Use

You need to evaluate whether an architect (the user or someone they manage) is fulfilling the core expectations of the role. Typical triggers:

- The user just got promoted to architect and wants to know what the role requires
- The user suspects they are spending time on the wrong activities (too much coding, not enough strategy)
- The user's manager says they need to "be more strategic" or "step up as an architect"
- The user only recommends technologies they have personal experience with (Frozen Caveman pattern)
- The user wants to assess another architect's effectiveness
- The user is transitioning from developer to architect and struggles with the shift

Before starting, verify:
- Is the user an architect being assessed, or assessing someone else?
- What specific concerns or symptoms triggered this question?

## Context

### Required Context (must have before proceeding)

- **Current activities:** What does the architect spend their time on?
  -> Check prompt for: coding, meetings, reviews, presentations, stakeholder interactions, technology evaluation
  -> If still missing, ask: "Can you describe how you currently spend your time as an architect — what activities take up most of your day/week?"

- **Specific concern:** What triggered this assessment?
  -> Check prompt for: feedback, frustration, role confusion, promotion, performance review
  -> If still missing, ask: "What prompted this question — is there a specific concern about how the architect role is being performed?"

### Observable Context (gather from environment)

- **Organization type:** What kind of company and team structure?
  -> Check prompt for: startup, enterprise, team size, reporting structure
  -> If unavailable: assume mid-size tech company

- **Career stage:** How long has this person been an architect?
  -> Check prompt for: "just promoted," "been an architect for X years," experience references
  -> If unavailable: assess from behavior descriptions

- **Team interaction patterns:** How does the architect interact with development teams?
  -> Check prompt for: code reviews, pair programming, stand-ups, 1-on-1s, architectural reviews
  -> If unavailable: assess from activity descriptions

### Default Assumptions

- If career stage unknown -> assess all 8 expectations equally
- If organization type unknown -> apply general guidance
- If team interaction patterns unknown -> flag as an area to investigate

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- At least 3-4 current activities are described
- The specific concern or trigger is understood
- The career context provides enough to assess depth vs breadth

PROCEED WITH DEFAULTS when:
- Some activities are described
- A general concern is expressed
- Career stage can be estimated

MUST ASK when:
- No current activities are described at all
- The concern is completely unclear
```

## Process

### Step 1: Assess Against the 8 Core Expectations

**ACTION:** Evaluate the architect against each of the eight core expectations. Score each as Strong, Adequate, Needs Improvement, or Missing. For detailed descriptions of each expectation, see [references/eight-expectations.md](references/eight-expectations.md).

**WHY:** These eight expectations define what an architect should be doing regardless of their title, organization, or seniority level. An architect who excels at 3 of 8 is failing the role even if those 3 are done brilliantly. The expectations are intentionally broad — they encompass technical, interpersonal, and organizational dimensions because the architect role sits at the intersection of all three.

| # | Expectation | What it means | Common failure mode |
|---|------------|---------------|---------------------|
| 1 | **Make architecture decisions** | Define architecture decisions and design principles to GUIDE (not specify) technology choices | Specifying "use React.js" instead of guiding "use a reactive-based framework" |
| 2 | **Continually analyze the architecture** | Assess how viable the architecture is given today's business and technology landscape, recommend improvements | Designing once and never revisiting; architecture decay goes unnoticed |
| 3 | **Keep current with latest trends** | Stay up to date on technology and industry trends | Falling behind on technologies, making decisions based on outdated knowledge |
| 4 | **Ensure compliance with decisions** | Verify teams are following architecture decisions and design principles | Making rules but never checking if they're followed; architecture violations go uncaught |
| 5 | **Diverse exposure and experience** | Know multiple technologies, frameworks, and platforms — not just one stack | Only knowing Java/Spring and recommending it for every problem |
| 6 | **Have business domain knowledge** | Understand the business side, not just technology | Building technically elegant solutions that don't solve the actual business problem |
| 7 | **Possess interpersonal skills** | Teamwork, facilitation, leadership | Being technically brilliant but unable to collaborate, facilitate meetings, or lead teams |
| 8 | **Understand and navigate politics** | Navigate corporate politics effectively | Ignoring organizational dynamics and being surprised when good ideas get blocked |

**IF** the user describes their activities -> map each activity to one or more expectations and identify gaps
**IF** the user describes problems -> trace each problem to a failing expectation

### Step 2: Evaluate Technical Breadth vs Depth

**ACTION:** Assess whether the architect has the right balance of technical breadth (knowing many technologies at a surface level) vs technical depth (knowing a few technologies deeply).

**WHY:** The knowledge pyramid has three zones: "stuff you know" (depth), "stuff you know you don't know" (breadth), and "stuff you don't know you don't know" (unknown unknowns). Developers should maximize depth. Architects should maximize breadth. When a developer becomes an architect, they must deliberately shift their learning investment: sacrifice some depth to expand breadth. An architect who only has depth makes poor decisions because they can only see solutions through the lens of technologies they know deeply.

**The Knowledge Pyramid:**
- **Stuff you know** (technical depth) — Your core expertise. As a developer, this is your strength. As an architect, this narrows your solution space.
- **Stuff you know you don't know** (technical breadth) — Technologies you're aware of and could evaluate but haven't used deeply. As an architect, THIS is your most valuable zone. It lets you identify the right technology for each problem, even if you need to dive deeper to implement it.
- **Stuff you don't know you don't know** (unknown unknowns) — The dangerous zone. Everything here is a potential blind spot. Expanding breadth shrinks this zone.

**Assessment criteria:**
- Does the architect recommend the same technology stack for every problem? -> Too much depth, not enough breadth
- Can the architect evaluate unfamiliar technologies against requirements? -> Good breadth
- Does the architect dismiss technologies they haven't used without evaluation? -> Depth bias
- Does the architect maintain awareness of the broader technology landscape? -> Good breadth practice

### Step 3: Check for the Frozen Caveman Anti-Pattern

**ACTION:** Determine whether the architect exhibits the Frozen Caveman pattern — irrationally reverting to past experience regardless of current context.

**WHY:** The Frozen Caveman Architect had a traumatic experience years or decades ago (a system failure due to scalability, a data breach, a vendor lock-in disaster) and now insists every new system must guard against that specific problem, even when it's irrelevant to the current context. This is not the same as learning from experience — it's the inability to objectively assess whether past lessons apply to the current situation.

**Warning signs:**
- Constantly references a specific past failure ("In 2018, our message queue crashed, so I never use message queues")
- Over-engineers for scenarios that are extremely unlikely in the current context
- Dismisses entire technology categories based on a single bad experience
- Cannot articulate current, evidence-based reasons for their position — only historical anecdotes
- Fear-driven decisions that don't match current requirements

**IF** Frozen Caveman pattern detected -> flag it explicitly with specific correction:
- Evaluate each architecture decision based on CURRENT context, requirements, and constraints
- Past experience should INFORM decisions but not DICTATE them
- Use risk assessment techniques to objectively evaluate whether historical concerns apply
- Ask: "What is the probability of that specific failure in THIS system, with TODAY's technology?"

### Step 4: Identify the Architecture vs Design Boundary

**ACTION:** Assess whether the architect is operating at the right level — making architecture decisions vs design decisions.

**WHY:** Architecture decisions affect the structure of the system and constrain or guide development teams. Design decisions affect implementation within those constraints. An architect who makes design decisions (choosing class structures, selecting design patterns, writing pseudocode) is micromanaging. An architect who doesn't make architecture decisions (letting the team decide service boundaries, communication protocols, data partitioning) is abdicating the role.

**The boundary test:** Does this decision affect the overall structure of the system?
- If YES -> architecture decision (architect's responsibility)
- If NO -> design decision (developer's responsibility)
- If UNCLEAR -> architecture decision, but the architect should guide rather than specify

### Step 5: Generate the Assessment Report
**AGENT: EXECUTES** — produces the assessment

**ACTION:** Compile the findings into a structured assessment with specific recommendations for improvement.

**HANDOFF TO HUMAN** — the user implements the changes in their daily work

## Inputs

- Description of current architect activities and time allocation
- Specific concerns or symptoms
- Optionally: career history, team structure, organization type, manager feedback

## Outputs

### Architect Role Assessment

```markdown
# Architect Role Assessment

## Current Profile
- **Role tenure:** {how long as architect}
- **Organization context:** {company type, team size}
- **Primary concern:** {what triggered the assessment}

## Eight Expectations Scorecard

| # | Expectation | Rating | Evidence | Recommendation |
|---|------------|--------|----------|----------------|
| 1 | Make architecture decisions | {Strong/Adequate/Needs Improvement/Missing} | {what was observed} | {specific action} |
| 2 | Continually analyze | ... | ... | ... |
| 3 | Keep current with trends | ... | ... | ... |
| 4 | Ensure compliance | ... | ... | ... |
| 5 | Diverse exposure | ... | ... | ... |
| 6 | Business domain knowledge | ... | ... | ... |
| 7 | Interpersonal skills | ... | ... | ... |
| 8 | Navigate politics | ... | ... | ... |

## Technical Breadth vs Depth Assessment
- **Current balance:** {depth-heavy / balanced / breadth-heavy}
- **Knowledge pyramid status:** {description of current state}
- **Recommendation:** {specific actions to adjust balance}

## Anti-Pattern Check
- **Frozen Caveman:** {detected / not detected} — {evidence}
- **Other patterns:** {any other role anti-patterns observed}

## Architecture vs Design Boundary
- **Current boundary:** {operating too low / appropriate / too high}
- **Evidence:** {examples of boundary violations}

## Top 3 Priority Actions
1. {most impactful change}
2. {second priority}
3. {third priority}
```

## Key Principles

- **The 8 expectations are non-negotiable** — WHY: They define the role. An architect who excels at 3 expectations but ignores the other 5 is not an effective architect — they're a specialist with the wrong title. Every expectation matters because the role sits at the intersection of technology, business, and people.

- **Breadth over depth for architects** — WHY: An architect who only knows Java/Spring recommends Java/Spring for everything, even when Go, Rust, or Python would be better fits. Technical breadth enables pattern recognition across technologies: "This problem looks like an event-sourcing problem regardless of the implementation language." Depth can always be re-acquired when needed for a specific implementation.

- **The Frozen Caveman is one of the most damaging anti-patterns** — WHY: Unlike other anti-patterns that produce bad output, the Frozen Caveman produces fear-based decisions that LOOK prudent. "We must plan for extreme scale" sounds responsible. But over-engineering for a scenario from 2018 that doesn't apply to the current 50-user internal tool wastes budget, time, and team morale. The Frozen Caveman confuses caution with wisdom.

- **Guide, don't specify** — WHY: The first expectation says architects should GUIDE technology decisions, not SPECIFY them. "Use a reactive-based framework for the frontend" guides the team to evaluate Angular, React, Vue, and Svelte. "Use React.js" takes that evaluation away from the team, depriving them of learning and depriving the project of potentially better alternatives.

- **Architecture decisions have structural scope** — WHY: If a decision doesn't affect the system's structure, it's a design decision and belongs to the developer. Architects who make design decisions become bottlenecks and steal the art of programming from their teams. Architects who don't make architecture decisions leave structural voids that the team fills inconsistently.

## Examples

**Scenario: New architect spending 80% of time coding**
Trigger: "I just got promoted to architect from senior developer. I'm still spending 80% of my time coding. My team says I'm a bottleneck on code reviews."
Process: Assessed against the 8 expectations. Found Expectation 1 (architecture decisions) as Needs Improvement — the user is making design decisions via code reviews instead of architecture decisions. Expectations 2-4 likely Missing since coding leaves no time for architecture analysis, trend-following, or compliance verification. Expectations 6-8 (business domain, interpersonal, politics) at risk due to time allocation. Diagnosed the architecture-vs-design boundary violation: the architect is operating at the design level, which is the developer's domain. Technical breadth assessment: likely depth-heavy since coding maintains depth at the expense of breadth. Recommended: reduce coding to 20-30%, shift to proof-of-concepts and fitness functions rather than production code, delegate code review responsibility to senior developers, and invest freed time in Expectations 2-8.
Output: Assessment showing 2 of 8 expectations met, depth-heavy knowledge profile, design-level boundary violation, and a 90-day transition plan.

**Scenario: Architect who only recommends familiar technologies**
Trigger: "I've been an architect for 5 years but I only recommend technologies I've used before — Java/Spring for everything. My team wants to try Go and Kafka but I keep saying no because I had a bad experience with message queues in 2018."
Process: Identified two issues: (1) Frozen Caveman anti-pattern — a 2018 message queue failure is driving current technology decisions without evaluating whether the same risk applies to today's context with today's tools. (2) Expectation 5 (diverse exposure) failure — recommending Java/Spring for everything indicates depth without breadth. Assessed knowledge pyramid: "stuff you know" (Java/Spring) is deep, "stuff you know you don't know" (Go, Kafka, modern event streaming) is being actively suppressed rather than explored. Correction: objectively evaluate whether the 2018 failure conditions exist in the current system; explore Go and Kafka through a proof-of-concept rather than dismissing them; set a goal of evaluating 2 unfamiliar technologies per quarter through lightweight experiments.
Output: Assessment flagging Frozen Caveman anti-pattern and Expectation 5 failure, with a structured technology exploration plan.

**Scenario: Architect who avoids stakeholder work**
Trigger: "I'm an architect but I never attend stakeholder meetings. I design systems, write ADRs, and review code. My manager says I need to 'be more strategic.'"
Process: Assessed against 8 expectations. Strong on Expectation 1 (architecture decisions via ADRs), Adequate on Expectation 4 (compliance via code reviews). Missing on Expectations 6 (business domain knowledge — can't learn the business without attending stakeholder meetings), 7 (interpersonal skills — not being exercised), and 8 (navigate politics — completely absent). The manager's feedback ("be more strategic") translates to: "you're fulfilling the technical expectations but ignoring the organizational expectations." Architecture doesn't happen in a vacuum — it must align with business goals, and that requires understanding the business. Recommended: attend 2 stakeholder meetings per week, schedule 1-on-1s with product managers to understand business priorities, and frame all ADRs with a "Business Context" section.
Output: Assessment showing 3 of 8 expectations met, organizational-expectation gap analysis, and specific stakeholder engagement plan.

## References

- For detailed descriptions of each of the 8 expectations with self-assessment questions and improvement strategies, see [references/eight-expectations.md](references/eight-expectations.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
