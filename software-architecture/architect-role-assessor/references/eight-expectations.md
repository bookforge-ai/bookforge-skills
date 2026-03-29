# Eight Expectations of a Software Architect

Detailed reference for each of the eight core expectations, with self-assessment questions and improvement strategies.

## Expectation 1: Make Architecture Decisions

*An architect is expected to define the architecture decisions and design principles used to guide technology choices within the team, the department, or across the enterprise.*

### Key Distinction: Guide vs Specify

The key operative word is **guide**. An architect should guide technology choices, not specify them.

- **Guiding** (correct): "Use a reactive-based framework for frontend web development" — the team evaluates Angular, React, Vue, Svelte and chooses the best fit
- **Specifying** (overreach): "Use React.js for the frontend" — this is a technical decision, not an architectural one, unless there's a specific architectural reason (e.g., server-side rendering requirements that favor Next.js)

An architect can make specific technology decisions when there is an architectural reason — when the choice affects scalability, performance, availability, or another architecture characteristic. But the default posture should be guidance.

### Self-Assessment Questions
- Do my decisions guide the team or dictate to them?
- Can I articulate the architecture characteristic that justifies each decision?
- Are my decisions documented (ideally in ADRs)?
- Do my decisions form constraints (boundaries) or do they make implementation choices?

### Improvement Strategies
- Review each recent technology decision and ask: "Is this architecture or design?"
- Convert specifications to guidelines where possible
- Start writing ADRs for significant decisions

## Expectation 2: Continually Analyze the Architecture

*An architect is expected to continually analyze the architecture and current technology environment and then recommend solutions for improvement.*

### What This Means

Architecture vitality — assessing how viable the architecture that was designed three or more years ago is today, given changes in both business and technology. Most architects don't focus enough energy on this. As a result, architectures experience structural decay as developers make coding or design changes that impact architecture characteristics.

### Self-Assessment Questions
- When was the last time I evaluated whether our current architecture still meets our needs?
- Am I monitoring architecture characteristics (performance, scalability, availability)?
- Are we tracking architecture fitness functions?
- Have I assessed our testing and release environments for agility?

### Improvement Strategies
- Schedule quarterly architecture health checks
- Implement fitness functions for critical architecture characteristics
- Create a technology radar for the team/organization

## Expectation 3: Keep Current with Latest Trends

*An architect is expected to keep current with the latest technology and industry trends.*

### Why This Matters

Architecture decisions are long-lasting and difficult to change. Understanding key trends helps the architect prepare for the future and make the correct decision. An architect making decisions based on 5-year-old knowledge is building architectures optimized for yesterday's constraints.

### Self-Assessment Questions
- Can I name 3 technology trends from the last 12 months that could affect our architecture?
- Am I reading/watching/attending conferences, tech talks, or community discussions?
- Do I maintain a technology radar or similar tracking mechanism?

### Improvement Strategies
- Dedicate 30 minutes per day to technology trend awareness
- Maintain a personal technology radar
- Attend at least 2 conferences or significant tech community events per year
- Follow thought leaders and industry publications

## Expectation 4: Ensure Compliance with Decisions

*An architect is expected to ensure compliance with architecture decisions and design principles.*

### What This Means

Making decisions is only half the job. The architect must verify that development teams are actually following those decisions. This includes:
- Architecture decisions (e.g., layering rules, service boundaries)
- Design principles (e.g., async messaging between services)

Without compliance checking, architecture violations accumulate until the actual system no longer matches the designed system.

### Self-Assessment Questions
- How do I verify teams follow architecture decisions?
- Do I have automated fitness functions checking structural compliance?
- When was the last time I found and corrected an architecture violation?
- Do developers know which decisions are architectural constraints vs guidelines?

### Improvement Strategies
- Implement automated fitness functions (e.g., ArchUnit, NetArchTest)
- Conduct periodic architecture reviews
- Create an architecture compliance checklist for code reviews

## Expectation 5: Diverse Exposure and Experience

*An architect is expected to have exposure to multiple and diverse technologies, frameworks, platforms, and environments.*

### The Breadth Imperative

This doesn't mean being an expert in everything. It means knowing enough about diverse technologies to:
- Evaluate them against requirements
- Understand their trade-offs
- Recognize when a familiar technology is the wrong choice

An architect who only knows Java/Spring will recommend Java/Spring for everything, even when Go, Python, or Rust would be better fits.

### Self-Assessment Questions
- How many distinct technology stacks have I worked with in the last 3 years?
- Can I evaluate a technology I haven't used against our requirements?
- Do I dismiss technologies I haven't used without investigation?
- When was the last time I recommended something outside my comfort zone?

### Improvement Strategies
- Set a goal of exploring 1-2 new technologies per quarter through lightweight experiments
- Build proof-of-concepts in unfamiliar stacks
- Read about technologies in domains adjacent to yours
- Deliberately sacrifice some depth for breadth in learning time allocation

## Expectation 6: Have Business Domain Knowledge

*An architect is expected to have a certain level of business domain knowledge.*

### Why Technical Skills Aren't Enough

An architect who doesn't understand the business domain will build technically elegant solutions that don't solve the actual business problem. Without business domain knowledge:
- Architecture characteristics can't be properly identified (which -ilities matter depends on the business)
- Trade-off decisions lack business context
- Communication with stakeholders breaks down

### Self-Assessment Questions
- Can I explain our business model without using any technical terms?
- Do I understand the competitive landscape we operate in?
- Can I identify which business processes are most critical to revenue/success?
- Do I attend stakeholder meetings regularly?

### Improvement Strategies
- Attend product/business meetings regularly
- Schedule 1-on-1s with product managers and business stakeholders
- Read industry publications (not just tech blogs)
- Frame architecture decisions in business terms

## Expectation 7: Possess Interpersonal Skills

*An architect is expected to possess exceptional interpersonal skills, including teamwork, facilitation, and leadership.*

### The Soft Skills Are Not Optional

Technical brilliance without interpersonal skills produces architects who:
- Cannot facilitate productive meetings
- Alienate team members with abrasive communication
- Fail to build consensus around architectural direction
- Lose influence because people avoid working with them

### Self-Assessment Questions
- Can I facilitate a productive meeting with 10 people who disagree?
- Do people seek out my input or avoid it?
- Can I give constructive feedback without creating defensiveness?
- Do I listen as much as I speak in technical discussions?

### Improvement Strategies
- Practice active listening — summarize others' points before responding
- Facilitate (not dominate) architecture review meetings
- Seek feedback on communication style from trusted colleagues
- Invest in leadership training

## Expectation 8: Understand and Navigate Politics

*An architect is expected to understand the political climate of the enterprise and be able to navigate the politics.*

### The Uncomfortable Truth

Almost every architecture decision is also a political decision. Budget allocation, team structure, technology standards, vendor selection — all involve stakeholders with competing interests. An architect who ignores politics will:
- Propose technically excellent solutions that never get funded
- Make enemies by disrupting established power structures without coalition-building
- Be outmaneuvered by less technically skilled but more politically savvy colleagues

### Self-Assessment Questions
- Do I understand who the key decision-makers are and what motivates them?
- Can I anticipate which stakeholders will support or oppose my recommendations?
- Do I build coalitions before proposing significant changes?
- Am I surprised when good ideas get blocked for "non-technical reasons"?

### Improvement Strategies
- Map the stakeholder landscape: who has power, what they care about, who influences whom
- Build relationships with key stakeholders before you need something from them
- Learn to frame proposals in terms that align with stakeholder priorities
- Practice the negotiation techniques from the stakeholder-negotiation-planner skill

## The Knowledge Pyramid

### Three Zones of Knowledge

```
          /\
         /  \
        / S  \       "Stuff you don't know you don't know"
       / T  U \       (Unknown unknowns — the dangerous zone)
      / U  F  \       Expanding breadth shrinks this zone
     / F  F   \
    / F        \
   /____________\
  /   Stuff you  \    "Stuff you know you don't know"
 /   know you     \    (Known unknowns — ARCHITECT's key zone)
/   don't know     \   This is technical BREADTH
/___________________\
|                     |
|   Stuff you know    |   "Stuff you know"
|                     |   (Known knowns — DEVELOPER's key zone)
|   (Technical DEPTH) |   This is technical DEPTH
|_____________________|
```

### The Transition from Developer to Architect

As a developer, your value comes from **depth** — being the expert in your technology stack.

As an architect, your value shifts to **breadth** — being able to evaluate many technologies against requirements and select the right one for each problem.

This transition requires a **deliberate sacrifice**: you must give up some depth to build breadth. This feels uncomfortable because depth is how you built your career. But an architect who maintains developer-level depth in one stack at the expense of breadth across many stacks will make poor architecture decisions.

**Practical guidance:**
- Maintain depth in 1-2 technologies (enough to stay credible and build POCs)
- Build breadth across 10-20 technologies (enough to evaluate and compare)
- Invest 70% of learning time in breadth, 30% in depth maintenance

## The Frozen Caveman Anti-Pattern

A Frozen Caveman Architect always reverts to their past experience, regardless of whether it applies to the current situation.

**Example:** An architect who experienced a system failure in 1997 due to scalability issues now insists every system must handle extreme scale, even when the current application is an internal tool with 50 users.

**How to differentiate learning from experience vs Frozen Caveman:**

| Learning from experience (good) | Frozen Caveman (anti-pattern) |
|------|------|
| "We should consider scalability because our user base is growing 200% yearly" | "We MUST build for massive scale because my system crashed in 2018" |
| Decision grounded in current data | Decision grounded in past trauma |
| Can articulate current risk factors | Can only reference historical incidents |
| Considers probability in current context | Ignores probability differences |
| Open to evidence that the risk is different now | Refuses to reconsider |

**Correction:** For every decision driven by past experience, ask: "What is the probability of this specific failure in THIS system, with TODAY's technology, given our CURRENT requirements?" If the answer is "low," the past experience is informing a bias, not a decision.
