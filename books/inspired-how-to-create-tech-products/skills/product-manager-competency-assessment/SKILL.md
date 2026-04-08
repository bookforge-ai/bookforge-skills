---
name: product-manager-competency-assessment
description: |
  Evaluate product manager competency for hiring, coaching, or self-assessment. Use when interviewing a VP of Product or head of product candidate, assessing an existing product leader, evaluating an individual contributor PM, conducting a PM self-assessment to find development gaps, or debriefing an interview panel. Also use when someone asks 'is this PM candidate strong?', 'am I a good product manager?', 'what does a strong VP of Product look like?', or 'how do I evaluate PM interview performance?' Covers VP assessment (team development, vision and strategy, execution, culture) and IC PM assessment (customer, data, business, market knowledge plus smart/creative/persistent traits). Diagnoses which of 3 PM working modes the person operates in: backlog administrator, roadmap administrator, or empowered PM. Not for team or organizational assessment — use product-team-health-diagnostic or product-culture-assessment for those.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/product-manager-competency-assessment
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
model: sonnet
context: 200k
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Interview notes, performance observations, written self-assessment, or verbal description of the person being assessed"
    - type: none
      description: "Skill can work from a verbal description provided in the prompt"
  tools-required: [Read]
  tools-optional: []
  environment: "No codebase access required; works from descriptions, interview notes, or self-assessment input"
source-books:
  - name: inspired-how-to-create-tech-products
    chapters: [10, 17]
depends-on: []
tags: [product-management, hiring, career-development]
---

# Product Manager Competency Assessment

## When to Use

Use this skill when you are:
- **Hiring a VP of Product** — need a structured evaluation framework beyond gut feel and resume review
- **Assessing an existing head of product** — need to determine if the current leader has the competencies the company needs at this stage
- **Evaluating an individual contributor PM candidate** — need to test whether they have the four knowledge domains and three core traits
- **Coaching a PM** — need to identify specific development gaps and create a targeted improvement plan
- **Running a self-assessment** — a PM wants an honest gap analysis against what the role actually requires
- **Debriefing after interviews** — need a shared framework to align an interview panel on evaluation criteria

Preconditions: you have at least one of:
- Interview notes or transcripts from one or more conversations with the person
- Performance observations over at least several weeks
- A self-written description from the person being assessed
- A verbal description you can provide directly in the prompt

**Agent:** Before beginning, clarify the assessment scope:
1. Is this a VP-level / head of product assessment, an individual contributor PM assessment, or both?
2. Is this a hiring evaluation, a performance review, or a self-assessment for development?
3. What is the company stage and CEO profile (for VP assessments — this changes what vision/strategy profile you need)?

---

## Assessment Processes

---

### Use Case A: VP of Product / Head of Product Assessment

Source: Ch17 (pp.79-83)

#### A-Step 1 — Establish CEO and Company Context First

WHY: The VP of Product must complement the CEO, not mirror them. The right VP profile depends entirely on whether the CEO is a product visionary. Getting this wrong is the single most common cause of VP product failure and short tenure.

Determine:

| Question | Why It Matters |
|----------|---------------|
| Is the CEO a strong product visionary (drives vision, deeply involved in product decisions)? | If yes: the VP role is primarily execution. You need someone who can execute the CEO's vision without ego clash. Hiring a visionary VP into a visionary CEO company causes immediate conflict. |
| Has the founder moved on, or is the CEO not strong at product vision? | If yes: the VP must be the product visionary. The company will stagnate without one. |
| How large is the product organization? | Larger organizations require stronger stakeholder management and internal evangelism skills — weight the execution competency accordingly. |
| Is this a Series A/B (building product culture) or Series C+ (scaling an existing culture)? | Shapes how much you weight product culture competency. |

Document the CEO and company profile before evaluating any candidate.

---

#### A-Step 2 — Evaluate the Four Core Competencies

Score each competency: **Strong** (clear evidence), **Developing** (partial evidence), **Absent** (no evidence or counter-evidence).

---

**Competency 1 — Team Development**

This is the single most important competency for a VP of Product. The VP's job is to develop a strong team of product managers and designers.

What to look for:
- Track record of identifying and recruiting product talent
- Evidence of actively developing people — addressing weaknesses, exploiting strengths
- Can articulate a framework for what makes a strong PM and how to develop one
- Has successfully promoted people who then performed well
- Has managed out poor performers without letting them linger

Red flag: candidate was an excellent individual contributor PM who has never had to develop others. Strong IC skills and strong people-development skills are different skill sets. Many excellent PMs never progress to leading organizations because they cannot make this transition.

Interview criteria:
- "Tell me about someone on your team who was struggling. What specifically did you do? What was the outcome?"
- "Describe your recruiting process for PMs. What do you look for and how do you find non-obvious talent?"
- "What is your framework for evaluating a PM's strengths and weaknesses?"
- "Tell me about a PM you developed who went on to do something significant."

---

**Competency 2 — Product Vision and Strategy**

The product vision is what drives and inspires the company and sustains it through ups and downs.

What to look for (shape depends on CEO profile — see Step 1):

*If CEO is a product visionary:*
- Candidate is strong at executing and operationalizing vision, not generating it
- Can translate a founder's vision into concrete product strategy and roadmap
- Does not compete with the CEO for the vision; does not need to own it
- Some strong VP candidates will decline this role precisely because their job would be execution — that is self-awareness, not a weakness

*If CEO is not a product visionary:*
- Candidate is a genuine product visionary in their own right
- Has demonstrated ability to define and communicate a compelling product vision that motivates engineers and designers
- Can provide the strategic coherence that the organization currently lacks

Interview criteria:
- "Tell me about a product vision you defined or operationalized. How did you arrive at it and how did you communicate it to the team?"
- "How do you think about the relationship between your vision and the CEO's direction?"
- "Walk me through a strategic decision where you had to say no to a significant stakeholder request."

---

**Competency 3 — Execution**

Vision without execution is worthless. The product leader must have proven ability to get products into customers' hands.

What to look for:
- Expert in modern product planning: customer discovery, product discovery, product development process
- Proven ability to manage stakeholder relationships and internal evangelism
- Can inspire and motivate the company — gets everyone moving in the same direction
- Has worked effectively at the company's scale (or slightly above it)
- Bigger organizations require stronger stakeholder management; weight this accordingly

Interview criteria:
- "Describe your product development process. How do you run discovery? How do you decide what to build?"
- "Tell me about a situation where you had major stakeholder conflict. How did you resolve it?"
- "How do you keep engineering and design motivated when the roadmap is constrained by business needs?"
- "What does your planning process look like at the start of a quarter or half?"

---

**Competency 4 — Product Culture**

Good product organizations have strong teams, solid vision, and consistent execution. Great product organizations add a strong product culture.

What to look for:
- Understands and can articulate why continuous, rapid testing and learning matters
- Treats mistakes as learning — makes them quickly, mitigates risk, moves forward
- Demonstrates genuine respect for designers and engineers as collaborators, not service providers
- Can give concrete examples from their own experience of building product culture
- Has concrete plans for instilling culture in a new company — not vague aspirations

Interview criteria:
- "Tell me about a time your team was wrong about something important. How did you find out? What did you do?"
- "How do you describe your relationship with engineering leadership? Give me a specific example of how you work with your tech lead."
- "What does a strong product culture look like to you? What specifically would I observe if I spent a week in your current team?"
- "What would be your first 90 days focused on, culturally?"

---

#### A-Step 3 — Evaluate Secondary Criteria

**Experience**
- Minimum: strong technology background + understanding of the economics and dynamics of the business and market
- Domain experience (industry-specific knowledge) varies by company — assess fit for your specific industry

**Chemistry**
- The VP product must be able to work well on a personal level with the CEO and CTO
- This is non-negotiable: if chemistry is absent, the other competencies do not matter
- Assessment method: include a long dinner (not a formal interview) with at least the CEO and CTO, and ideally the head of marketing and head of design. Make it personal, not a continuation of the interview.

---

#### A-Step 4 — Produce the VP Assessment Report

```
## VP of Product Competency Assessment

**Candidate:** [name / role]
**Evaluator:** [name / role]
**Date:** [date]
**Assessment Type:** [hiring / performance review / promotion]

---

### Company Context
CEO profile: [visionary / not visionary]
Company stage: [Series A / B / C+ / public / other]
Organization size: [# PMs, # designers]
Implication for VP profile: [execution-oriented VP / visionary VP needed]

---

### Competency Scores

| Competency | Score | Summary Evidence |
|------------|-------|-----------------|
| Team Development | Strong / Developing / Absent | [1-2 sentences] |
| Product Vision and Strategy | Strong / Developing / Absent | [1-2 sentences] |
| Execution | Strong / Developing / Absent | [1-2 sentences] |
| Product Culture | Strong / Developing / Absent | [1-2 sentences] |
| Experience (secondary) | Strong / Developing / Absent | [1-2 sentences] |
| Chemistry (secondary) | Strong / Developing / Absent | [1-2 sentences] |

---

### Key Strengths
[2-3 bullet points with specific evidence]

### Key Gaps
[2-3 bullet points with specific evidence]

### Critical Risks
[Any red flags — e.g., no people development track record, CEO/VP vision profile mismatch, chemistry concerns]

---

### Recommendation
[Hire / Do not hire / Conditional hire with specific criteria] — [2-3 sentence rationale]

### If Hiring: First 90-Day Priorities
[2-3 specific areas to watch or support in the first quarter]

### If Not Hiring: Profile Clarification
[What the company should look for differently in the next candidate]
```

---

---

### Use Case B: Individual Contributor PM Assessment

Source: Ch10 (pp.41-48)

#### B-Step 1 — Diagnose the Working Mode

Before assessing competency, diagnose how the PM currently works. This determines whether the competency gaps are individual (can be developed) or structural (require organizational change).

There are three PM working modes. Only one leads to success:

| Mode | How to Identify | Root Cause | Outcome |
|------|----------------|-----------|---------|
| **Backlog Administrator** | Escalates every issue and decision to the CEO or manager; treats the job as managing a Jira backlog; works as a Certified Scrum Product Owner | CEO/manager has not given PM authority and decision-making power | Not scaling; CEO bottleneck |
| **Roadmap Administrator** | Calls stakeholder meetings and lets them fight it out; roadmap is set by committee (sales, support, executives); PM's job is to record decisions and write tickets | Organizational culture of design by committee; no PM empowerment | Mediocrity; rarely yields innovation |
| **Empowered PM** | Synthesizes customer knowledge, data, business constraints, and market context to make and own product decisions; accountable for outcomes | PM has authority and the four knowledge domains | The only mode that produces strong products |

**Diagnostic questions:**
- "Walk me through how the last significant product decision was made. Who was in the room? Who decided?"
- "When you and a key stakeholder disagree on a feature priority, what happens?"
- "How do you typically find out what to put in the backlog?"
- "What happens when engineering raises a concern about scope during sprint planning?"

If the PM is operating in Backlog Administrator or Roadmap Administrator mode, determine whether this is individual weakness or structural disempowerment before evaluating the four knowledge domains. A capable PM in a dysfunctional organization will still look like a weak PM.

---

#### B-Step 2 — Evaluate the Four Knowledge Domains

Score each domain: **Strong** (demonstrated depth), **Developing** (partial), **Absent** (gap).

WHY: These are the four things the PM is responsible for contributing to the team that no one else on the team provides. If the PM cannot bring these, the team will build the wrong things or fail to make good decisions.

---

**Domain 1 — Deep Knowledge of the Customer**

The PM must be an acknowledged expert on the actual users and customers: their issues, pains, desires, how they think, how they work (for business products), and how they decide to buy.

This is not optional — without this knowledge, every product decision is guessing.

Requires both:
- Qualitative learning: understanding *why* users and customers behave the way they do
- Quantitative learning: understanding *what* they are doing (usage data, conversion data, behavioral analytics)

The PM must also be an undisputed expert on the product itself.

Evidence to look for:
- Spends time regularly with actual users (not just internal proxies like sales or customer success)
- Can describe specific users by name with detailed empathy for their situation
- Has a systematic practice for staying current on customer behavior
- Their team trusts them as the definitive source of customer truth

---

**Domain 2 — Deep Knowledge of Data**

Product managers are expected to be comfortable with data and analytics: both quantitative and qualitative skills.

Evidence to look for:
- Starts the day reviewing analytics: sales data, usage data, A/B test results
- Can form and test hypotheses using product analytics without delegating the interpretation
- Uses data to challenge assumptions, including their own
- Understands the difference between correlation and causation in product data

Critical: analysis and understanding of data cannot be delegated. Having a data analyst help with queries is fine; having the analyst interpret what the data means for the product is not.

---

**Domain 3 — Deep Knowledge of Business**

Successful products are not only loved by customers — they also work for the business.

This is often the hardest domain for PMs, because it requires understanding:
- Who the key stakeholders are: general management, sales, marketing, finance, legal, business development, customer service
- What constraints each stakeholder operates under
- How the product creates and captures value in the business model

Evidence to look for:
- Can articulate the business constraints they are working within
- Has established trust with key stakeholders by demonstrating they understand and respect their constraints
- Has declined to build features that customers wanted but that would not work within business constraints
- Does not treat stakeholder management as a political obstacle; treats it as part of the job

---

**Domain 4 — Deep Knowledge of Market and Industry**

The PM must know the competitive landscape and the market trajectory — not just where the market is today, but where it will be tomorrow.

Evidence to look for:
- Monitors competitors regularly and understands their strengths, weaknesses, and strategy
- Tracks key technology trends relevant to their market
- Follows relevant industry analysts and understands the role of social media in their market
- Can articulate why feature parity with competitors is not sufficient (switching costs mean users need to be *substantially* better off to switch)
- Thinks about ecosystem fit — how the product fits into a broader ecosystem of tools and workflows

---

#### B-Step 3 — Evaluate the Three Core Traits

These are not skills that can be taught — they are characteristics the person either has or does not have. Passion for the product and for solving customer problems is the prerequisite; these traits determine whether that passion produces results.

| Trait | What It Means | How to Identify |
|-------|--------------|----------------|
| **Smart** | Intellectually curious; quickly learns and applies new technologies to solve problems, reach new audiences, or enable new business models. Not just raw intelligence — learning velocity. | Ask about a recent technology trend they explored. How deeply did they go? Did they connect it to a product opportunity? |
| **Creative** | Thinks outside the normal product feature box to solve business problems. Does not default to "add a feature" as the solution. | Ask about a problem they solved in a non-obvious way. How did they arrive at the solution? |
| **Persistent** | Pushes the company way beyond its comfort zone with compelling evidence, constant communication, and building bridges across functions in the face of stubborn resistance. | Ask about a time they were told no and kept going. What was the evidence they used? How did they communicate? Did they succeed? |

---

#### B-Step 4 — Assess Preparation and Development Readiness

A new PM needs approximately 2-3 months to get up to speed — but only if they have the right access:
- Regular access to customers (qualitative and quantitative)
- Access to data and the tools to access it
- Access to key stakeholders
- Time to learn the product and industry

If this access is not available, the onboarding timeline is meaningless. A PM cannot develop deep knowledge in isolation.

**Preparation roadmap for a developing PM (or self-assessment action plan):**

| Priority | Action | Target |
|----------|--------|--------|
| 1 | Become the customer expert | Share customer learnings openly with the team — become the company's go-to person for anything about the customer, quantitative and qualitative |
| 2 | Build stakeholder relationships | Convince each key stakeholder of two things: (1) you understand their constraints; (2) you will only bring solutions consistent with those constraints |
| 3 | Become the product and industry expert | Share knowledge openly and generously; be the person others ask about competitors and market trends |
| 4 | Build collaborative relationship with the team | Nurture the working relationship with design and engineering; make them want to work with you |

---

#### B-Step 5 — Produce the IC PM Assessment Report

```
## Individual Contributor PM Competency Assessment

**Person:** [name / role]
**Evaluator / Context:** [name / hiring / self-assessment / coaching]
**Date:** [date]

---

### Working Mode Diagnosis

Current mode: [Backlog Administrator / Roadmap Administrator / Empowered PM]
Evidence: [2-3 specific observations that indicate the mode]
Root cause: [individual gap / structural disempowerment / both]
Implication: [whether competency gaps are fixable through individual development or require organizational change first]

---

### Knowledge Domain Scores

| Domain | Score | Key Evidence | Primary Gap |
|--------|-------|-------------|-------------|
| Deep Knowledge of Customer | Strong / Developing / Absent | [observation] | [specific gap if any] |
| Deep Knowledge of Data | Strong / Developing / Absent | [observation] | [specific gap if any] |
| Deep Knowledge of Business | Strong / Developing / Absent | [observation] | [specific gap if any] |
| Deep Knowledge of Market and Industry | Strong / Developing / Absent | [observation] | [specific gap if any] |

---

### Core Traits Assessment

| Trait | Present / Partial / Absent | Evidence |
|-------|---------------------------|---------|
| Smart (learning velocity, technology curiosity) | | |
| Creative (non-obvious problem solving) | | |
| Persistent (pushes through resistance with evidence) | | |

---

### Strengths
[2-3 bullet points with specific evidence]

### Development Gaps
[2-3 bullet points with specific evidence and root cause]

---

### Recommendation
[Hire / Do not hire / Continue with development plan] — [2-3 sentence rationale]

### Development Plan (if applicable)
Ordered by priority:

| Priority | Domain/Trait | Current State | Target State | Actions | Timeline |
|----------|-------------|---------------|--------------|---------|----------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### Onboarding Requirements (if new hire)
Access needed: [customers / data tools / stakeholders / product time]
Expected ramp time: 2-3 months with full access
Manager commitment required: [specific]
```

---

## Interpreting Results

**Working mode vs. individual competency:** A PM in Backlog Administrator mode may actually have strong knowledge domains — they are simply not permitted to apply them. Do not equate the working mode diagnosis with individual capability. An empowered PM in a dysfunctional organization looks weak; a weak PM in a supportive organization can look stronger than they are.

**The vision/execution mismatch for VP assessments:** The most common VP hiring failure is not evaluating the CEO's profile first. A visionary VP hired into a visionary CEO company will clash. An execution VP hired into a company with no product vision will leave a dangerous vacuum. The CEO profile assessment in A-Step 1 is not optional.

**Team development is the hardest competency to assess:** VP candidates often have strong individual contributor track records and poor people-development track records. Ask specifically about people they have developed — not just teams they have led. Look for concrete examples of someone struggling and the specific interventions used, not just successful team outcomes.

**Product culture is about concrete plans, not values:** Many VP candidates will say the right things about product culture. Press for concrete evidence: examples of how they instilled culture in a previous company, specific rituals or practices they used, what went wrong and how they corrected it. Vague values ("I believe in data-driven decisions") are not evidence.

**The chemistry criterion for VP assessments:** This is assessed last but is a veto. Strong competencies cannot compensate for a fundamental lack of personal rapport with the CEO and CTO. Build the dinner into the process.

---

## Reference

Detailed interview question banks and scoring rubrics:
`references/competency-interview-guide.md`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Inspired How To Create Tech Products by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
