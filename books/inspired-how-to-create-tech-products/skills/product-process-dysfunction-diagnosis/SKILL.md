---
name: product-process-dysfunction-diagnosis
description: |
  Diagnose why product efforts fail despite using Scrum, Agile, or roadmaps. Use when a team ships on time but customers don't adopt features, when leadership asks why there's no innovation despite an Agile process, when a new product leader needs to identify root causes quickly, or when someone asks 'are we doing waterfall disguised as Agile?' Also use when someone says 'we follow the process but nothing lands', 'sales keeps driving our roadmap', 'design is always scrambling to catch up', 'our engineers just build what they're told', or 'customers never adopt what we build.' Scores 10 root causes of product failure across startup, growth, and enterprise stages and produces a prioritized dysfunction report. For culture-wide assessment (innovation vs. execution), use product-culture-assessment. For team-level behaviors and velocity, use product-team-health-diagnostic.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/product-process-dysfunction-diagnosis
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
model: sonnet
context: 200k
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of how the team works: how ideas are sourced, how the roadmap is built, PM role, how design and engineering participate, release cadence, and how customer feedback is gathered"
    - type: none
      description: "Skill can work from a verbal description of team processes"
  tools-required: [Read]
  tools-optional: []
  environment: "No codebase access required; works from process descriptions and observations"
source-books:
  - name: inspired-how-to-create-tech-products
    chapters: [3, 4, 5, 6, 7]
depends-on: []
tags: [product-management, process-assessment, agile]
---

# Product Process Dysfunction Diagnostic

## When to Use

Use this skill when you are:
- **Seeing the "shipping but not landing" pattern** — features are delivered on schedule, but customers rarely adopt them or they don't move business metrics
- **Investigating a waterfall-disguised-as-agile process** — the team uses Scrum or Kanban but the upstream process (idea sourcing, roadmaps, business cases) is still waterfall
- **New to a product leadership role** — need to quickly locate which root causes are active before proposing changes
- **Evaluating a team's process** — whether as a coach, consultant, or peer reviewer assessing where dysfunction originates
- **Preparing a process transformation argument** — need to demonstrate to leadership exactly what is broken and why, with specific evidence

Preconditions: you have at least one of:
- A description of how ideas originate and reach the roadmap
- A description of the PM role and how they spend their time
- A description of when design and engineering enter the process
- Information on how and when customers are consulted
- Access to a roadmap, sprint board, or planning artifacts

**Agent:** Before scoring, clarify the company stage — approximately how many engineers are there, and has the company found product/market fit? Stage determines which failure patterns are most likely and which remediations are appropriate.

---

## Diagnostic Framework

The 10 root causes below come directly from Cagan's analysis of the waterfall model (Figure 6.1) practiced by the majority of companies: Ideas → Business Case → Roadmap → Requirements → Design → Build → Test → Deploy. Each root cause is a structural problem in this pipeline, any one of which can derail product efforts.

The two inconvenient truths that make the pipeline especially dangerous:
- **Truth 1 — 50% failure rate:** At least half of all product ideas will not work as expected. The best teams assume at least 75% won't perform like they hope.
- **Truth 2 — Iteration requirement:** Even ideas that do have potential typically require several iterations before they deliver necessary business value ("time to money").

These truths mean the pipeline is not merely inefficient — it is structurally set up to waste the majority of engineering effort.

---

## Step 1 — Identify Company Stage

WHY: The three stages have distinct failure patterns. Applying enterprise remediation to a startup wastes time; applying startup advice to an enterprise ignores real structural constraints.

Classify the company into one of three stages based on engineer count and product/market fit status:

| Stage | Profile | Primary Failure Risk |
|-------|---------|---------------------|
| **Startup** | Fewer than ~25 engineers; pre-product/market fit | Burning runway on wrong product; not doing discovery at all |
| **Growth** | 25 to several hundred engineers; scaling a proven product | Teams don't see the big picture; technical debt accumulates; leadership mechanisms stop scaling |
| **Enterprise** | Hundreds of engineers; established product and brand | Stakeholders protect existing business; innovation atrophies; design by committee; lack of empowerment |

**Stage-specific signals:**

*Startup:*
- The PM role is held by a co-founder with no dedicated product function
- Every pivot is a near-death experience
- "We'll figure it out after we ship" is the standard answer to discovery questions

*Growth:*
- Teams complain they don't understand the big picture or how their work connects to company goals
- Sales and marketing say the go-to-market strategies that worked for the first product don't apply to new ones
- Every engineer mentions "technical debt" unprompted
- Leadership style that worked at 20 people has stopped scaling

*Enterprise:*
- Stakeholders across the business are working hard to protect what the company has already built
- New initiatives get shut down or face so many obstacles that people stop proposing them
- Product teams complain about lack of vision, lack of empowerment, and that getting a decision takes forever
- Leadership resorts to acquisitions or creating separate "innovation centers" when they want new products
- "Design by committee" is how major product decisions are made

---

## Step 2 — Score the 10 Root Causes

For each root cause, score based on the evidence available. WHY: The 10 causes are not equally easy to spot — some are visible in artifacts (roadmaps, sprint boards), others require observing team behavior. Scoring each separately prevents a single visible problem from obscuring others.

**Scoring rubric:**

| Score | Meaning |
|-------|---------|
| **2** | Active dysfunction — the root cause is clearly present and driving poor outcomes |
| **1** | Partial — the root cause is present but partially mitigated |
| **0** | Absent — the team has addressed or does not exhibit this dysfunction |

---

### Root Cause 1 — Sales-Driven and Stakeholder-Driven Idea Sourcing

**Description:** Ideas for new product features originate primarily from sales ("we need this to close a deal"), executives, or internal stakeholders rather than from customer insight, data analysis, or the product team's own discovery work.

**Detection signals:**
- The roadmap looks like a list of feature requests from different parts of the business
- The PM's primary job is to "gather requirements" from stakeholders and translate them into user stories
- Sales specials and one-off customer commitments appear on the engineering backlog
- The quarterly planning meeting is where stakeholders negotiate to get their items prioritized
- Engineers feel like a feature factory — they build what they're told without understanding why

**Why it matters:** This is not the source of best product ideas. It also destroys team empowerment — the team is there to implement, not to solve problems. The team becomes mercenaries rather than missionaries.

**Stage context:**
- *Startup:* Usually surfaces as co-founder or early customer requests driving all decisions without discovery
- *Growth:* Key account management begins dictating product direction; enterprise sales becomes a de facto PM
- *Enterprise:* Full stakeholder negotiation model; roadmap is a political document

---

### Root Cause 2 — Unknowable Business Cases

**Description:** Prioritization is gated on a business case that requires knowing two things that cannot actually be known before building: how much revenue/value the idea will generate, and how much it will cost to build.

**Detection signals:**
- Product ideas require a formal or informal "business case" before getting on the roadmap
- PMs are asked how much revenue a feature will make before any customer validation
- Engineering is asked for estimates before the solution is even defined ("small, medium, large, or extra large")
- Ideas are prioritized by projected ROI that was effectively invented to justify a decision already made
- The business case exercise adds weeks to getting started without actually reducing risk

**Why it matters:** We cannot know either input to the business case at this stage. Revenue depends entirely on how good the solution turns out to be — some ideas generate nothing at all (this is confirmed by A/B testing data). Cost depends on the actual solution, which hasn't been designed. The business case process creates false certainty while adding overhead without reducing the risk of building the wrong thing.

---

### Root Cause 3 — Roadmap as Commitment

**Description:** The product roadmap is treated as a commitment to stakeholders about what will be built and when, rather than as a prioritized hypothesis about how to create value.

**Detection signals:**
- Roadmap items are communicated to sales with specific dates and are used in customer conversations
- Engineers are evaluated on "did we ship what was on the roadmap" rather than "did we achieve the intended outcome"
- Roadmap changes require executive sign-off or cause political conflict
- The PM's primary stress is keeping the roadmap commitments, not solving the underlying customer problem
- Items stay on the roadmap even after evidence emerges that they won't work

**Why it matters:** Most roadmap items are features and projects, not outcomes. The roadmap model predictably leads to teams shipping things that don't meet objectives — orphaned projects that were completed but didn't move the needle. Projects are output; product is about outcome.

---

### Root Cause 4 — Product Manager as Project Manager

**Description:** The PM role is primarily about gathering requirements, writing user stories, and tracking delivery — project coordination — rather than discovering what customers need and finding the best solution.

**Detection signals:**
- PMs spend most of their time in stakeholder meetings, backlog grooming, and sprint ceremonies
- PMs describe their job as "translating business needs into requirements for engineering"
- There is no time in the PM's week for customer interaction, data analysis, or prototype testing
- PMs are evaluated on delivery metrics (story points, on-time releases) rather than business outcome metrics
- The PM is the last person to hear about a customer problem — it comes via sales or support

**Why it matters:** This is 180 degrees from the reality of modern product management. Gathering requirements and documenting them for engineers is project management. Product management is discovering what customers need, finding a solution that works for the business, and working collaboratively with design and engineering to bring it to life.

---

### Root Cause 5 — Design Brought In Too Late (Lipstick on the Pig)

**Description:** UX and product design are engaged after requirements are defined, treating design as execution rather than as a discovery and problem-solving function.

**Detection signals:**
- Design receives a set of requirements or a PRD and is asked to "design the solution"
- Designers are brought into the process after the PM has already defined what is being built
- There is no design involvement in customer discovery or prototype testing
- Designers describe their role as "making it look nice" or "improving usability" of already-decided features
- Design is treated as a service team or internal agency rather than an embedded product team member

**Why it matters:** When design enters after requirements are set, the fundamental problem-solution fit has already been locked in. Design can only "put a coat of paint on the mess." The UX designers know this is not good, but they try to make it as nice as possible given the constraints. The real value of design — finding the right solution before anything is built — is lost entirely.

---

### Root Cause 6 — Engineers Excluded from Ideation

**Description:** Engineers only see product work when it arrives at sprint planning as a defined requirement or design spec, excluding them from the discovery and ideation process.

**Detection signals:**
- Engineers describe their role as "implementing what the PM and designer hand off"
- Engineers first see features at sprint planning (or equivalent)
- No mechanism exists for engineers to propose product ideas or surface technical opportunities
- Engineers are consulted only for effort estimates, not for feasibility exploration or solution options
- "Tech debt" is the only engineering-driven item that reaches the roadmap

**Why it matters:** Engineers are typically the best single source of innovation in a product team. By using engineers only for delivery, the organization gets approximately half their value. Engineers are aware of technical capabilities and constraints that enable entirely new product possibilities that neither PMs nor designers would think of — but only if they are in the room when problems are being explored.

---

### Root Cause 7 — Agile Applied Only to Delivery (20% of the Value)

**Description:** Agile methods (Scrum, Kanban) are applied exclusively to the engineering delivery phase, while the upstream process — idea sourcing, business cases, roadmaps, requirements — remains a waterfall pipeline.

**Detection signals:**
- The team "uses Scrum" but all sprint work is pre-defined before engineering is involved
- Sprint retrospectives never surface that the problem is upstream of the sprint
- Agile ceremonies (standups, sprint reviews, retros) are the only visible product process
- The backlog is a queue of pre-decided work, not a list of hypotheses to test
- "We're Agile" is offered as evidence that the team has a modern process, but delivery timelines are still measured in quarters

**Why it matters:** Teams using Agile in this way are getting approximately 20% of the actual value and potential of Agile methods. The core Agile benefit — fast feedback loops to learn and adapt — requires that discovery and definition are also iterative, not just delivery. What you are actually seeing is Agile for delivery, but the rest of the organization and context is waterfall.

---

### Root Cause 8 — Project-Centric Not Product-Centric

**Description:** The organization funds, staffs, and measures projects rather than products — treating product work as a series of discrete initiatives with start and end dates rather than as ongoing discovery and improvement.

**Detection signals:**
- Teams are assembled for a project and then disbanded or reassigned after it ships
- Budget is allocated per project rather than per product area or team
- Success is defined as "project delivered" (on time, on budget) rather than "outcome achieved"
- There is no ownership of a product or feature area after it ships — it becomes "maintenance"
- Teams have no mandate or time to iterate on launched work to improve outcomes

**Why it matters:** Projects are output; product is about outcome. A project-centric model predictably leads to orphaned launches — something was shipped but didn't meet its objectives, and no one owns improving it. There is simply no way to build strong products without the ability to iterate and improve based on real-world data.

---

### Root Cause 9 — Customer Validation at the End

**Description:** Customer feedback and validation only happen after the product is built — during user acceptance testing, beta programs, or post-launch — rather than during discovery before investment is made.

**Detection signals:**
- "Customer validation" means a beta test of the finished product
- Usability testing, if it happens at all, occurs on production-ready or near-production builds
- The first time real users interact with the idea is after engineering has invested weeks or months
- Discovering that customers don't want the feature is treated as a launch problem, not a discovery failure
- The risk of building the wrong thing is not managed — it is accepted

**Why it matters:** This is the biggest flaw of the waterfall process. All the risk is at the end. The key principle in Lean methods is to reduce waste, and one of the biggest forms of waste is to design, build, test, and deploy a feature or product only to find out it is not what was needed. Many teams believe they are applying Lean principles while following exactly this pattern — trying out ideas in one of the most expensive, slowest ways possible.

---

### Root Cause 10 — Opportunity Cost Ignored

**Description:** The cost of not doing alternative work — the opportunity cost — is never accounted for when evaluating the work the team is currently doing.

**Detection signals:**
- No mechanism exists to evaluate what the team is NOT building while building the current roadmap
- The roadmap is evaluated on "are these good ideas?" not "are these better than the alternatives?"
- When a project fails or delivers no value, the conversation is about what went wrong, not about what the team should have been doing instead
- Leadership evaluates the roadmap against stakeholder requests, not against market opportunities
- "We got it done" is the success criterion, even when the outcome was negligible

**Why it matters:** While the team is busy executing a process that generates a high rate of waste, the biggest loss is usually not the wasted effort itself — it is the opportunity cost of what the organization could have and should have been doing instead. That time and money cannot be recovered. The value of discovering what not to build — and redirecting to higher-value work — is invisible until it is calculated.

---

## Step 3 — Calculate the Dysfunction Score

Sum the scores across all 10 root causes:

```
Total dysfunction score = sum of scores (0–20 scale)
```

| Total Score | Severity | Interpretation |
|-------------|----------|----------------|
| 16–20 | Critical | Fundamental process transformation required; systemic waterfall in a non-waterfall costume |
| 11–15 | High | Multiple serious dysfunctions; significant innovation and adoption risk |
| 6–10 | Moderate | Several isolated dysfunctions; targeted fixes will produce meaningful improvement |
| 1–5 | Low | Minor process gaps; incremental tuning sufficient |
| 0 | Healthy | Process is largely sound |

**Automatic escalation:** Root causes 5 (late design), 6 (engineers excluded), and 9 (late customer validation) each represent structural risks that can independently invalidate an entire product process. If any of these three score 2, escalate the overall severity by one level regardless of total score.

WHY: These three are the core of what distinguishes product discovery from project execution. A team that scores well on the other seven but has all three of these active is still fundamentally not doing product development — they are doing project delivery.

---

## Step 4 — Map Findings to Company Stage Remediations

WHY: The same root cause has different remediation paths depending on company stage. A startup cannot adopt enterprise-scale discovery rituals; an enterprise cannot simply "empower the team" without structural change.

**Startup remediations (pre-product/market fit):**
- Focus entirely on getting to product/market fit — nothing else matters until you have a product that meets the needs of an initial market
- Root causes 1, 4, 9 are the most dangerous: any of them can cause a startup to burn runway building what stakeholders want instead of what the market needs
- Remediation is direct: the founding team must talk to real customers weekly, run low-fidelity experiments before building, and treat the roadmap as a hypothesis list

**Growth-stage remediations (scaling a proven product):**
- The organizational stress symptoms (teams don't see the big picture, technical debt, leadership mechanisms not scaling) require structural fixes, not just process changes
- Root causes 1, 3, 7, 8 are the most common at this stage
- Remediation requires: product vision that teams can connect their work to, defined product strategy, team charters that create clear ownership, and technical investment to address debt that is now blocking velocity

**Enterprise remediations (consistent innovation challenge):**
- The challenge is not capability — it is organizational will and structure
- Root causes 1, 3, 4, 7, 8, 10 all tend to be active simultaneously at enterprise scale
- Stakeholder dynamics actively resist the changes needed
- Remediation requires executive sponsorship of a new operating model; incremental process tweaks will not overcome the structural incentives
- Reference organizations: Adobe, Amazon, Apple, Google, Netflix have solved this — it requires making "pretty big changes"

---

## Step 5 — Identify the Waterfall-Disguised-as-Agile Pattern

WHY: This is the most common process misdiagnosis. Teams believe they are Agile because they use Scrum, but the upstream process that feeds the sprint is waterfall. Naming this explicitly is essential for any remediation conversation.

The pattern is present if ALL of the following are true:
- The team uses sprints or Kanban boards (delivery is Agile)
- Ideas arrive at sprint planning as defined requirements or designs (Agile starts downstream of discovery)
- Root causes 1, 3, 4, or 9 score 2 (the upstream pipeline is waterfall)

**Diagnostic test — ask these three questions:**
1. How does a brand-new idea go from "someone has this idea" to "an engineer starts coding"? If the answer involves roadmap, requirements document, or design handoff before any customer interaction, the upstream is waterfall.
2. When do engineers first see a feature? If the answer is sprint planning, standup, or ticket assignment, engineering is in delivery-only mode.
3. When do customers first interact with the idea? If the answer is beta, user acceptance testing, or post-launch, validation is at the end — waterfall.

**Report label:** If the pattern is detected, explicitly state: "This process is waterfall-disguised-as-agile. The Agile practices in use (sprints, standups, retrospectives) apply to approximately 20% of the product lifecycle — the delivery phase. The upstream process remains sequential and output-focused."

---

## Step 6 — Produce the Dysfunction Report

Structure the output as:

```
## Product Process Dysfunction Report

**Organization/Team:** [name]
**Company Stage:** [startup / growth / enterprise]
**Assessment Date:** [date]

---

### Overall Dysfunction Score: [X/20] — [SEVERITY]

**Waterfall-Disguised-as-Agile:** [Yes / No / Partial]

| Root Cause | Score | Severity | Key Signal Observed |
|------------|-------|----------|---------------------|
| 1. Sales/stakeholder-driven ideas | X | [label] | [1-sentence evidence] |
| 2. Unknowable business cases | X | [label] | [1-sentence evidence] |
| 3. Roadmap as commitment | X | [label] | [1-sentence evidence] |
| 4. PM as project manager | X | [label] | [1-sentence evidence] |
| 5. Design brought in too late | X | [label] | [1-sentence evidence] |
| 6. Engineers excluded from ideation | X | [label] | [1-sentence evidence] |
| 7. Agile delivery only (20% value) | X | [label] | [1-sentence evidence] |
| 8. Project-centric not product-centric | X | [label] | [1-sentence evidence] |
| 9. Customer validation at the end | X | [label] | [1-sentence evidence] |
| 10. Opportunity cost ignored | X | [label] | [1-sentence evidence] |

---

### Two Inconvenient Truths Assessment

| Truth | Impact Given Current Process |
|-------|------------------------------|
| At least 50% of ideas won't work | [How many ideas are being built without pre-validation? What is the estimated waste?] |
| Good ideas need several iterations | [Does the process allow for post-launch iteration? Is there team ownership that enables it?] |

---

### Automatic Escalation Triggers
[List any of causes 5, 6, 9 scoring 2 and their escalation impact]

---

### Waterfall-Disguised-as-Agile Analysis
[Result of the three diagnostic questions. If pattern detected, state it explicitly.]

---

### Stage-Appropriate Remediation Plan

**Company Stage:** [startup / growth / enterprise]

Ordered by: (1) escalation triggers first, (2) highest score, (3) cross-cause impact

| Priority | Root Cause | Current State | Target State | Stage-Specific Action |
|----------|-----------|---------------|--------------|----------------------|
| 1 | ... | ... | ... | ... |

---

### Summary

[3–5 sentences: what the process looks like from the outside, what is actually broken, the primary waste being generated, and the single most important change to make first]
```

---

## Step 7 — Validate Before Delivering

Before delivering the report:
- [ ] Every score of 2 has a specific, observable signal — not an assumption
- [ ] The waterfall-disguised-as-agile determination is based on answering all three diagnostic questions
- [ ] Stage classification is confirmed (do not default to "growth" — ask explicitly)
- [ ] The inconvenient truths section quantifies actual waste exposure, not generic risk
- [ ] The remediation plan is stage-appropriate — startup actions are not the same as enterprise actions
- [ ] The summary names the single most important change, not a list of everything that is wrong

WHY: The most common failure of a dysfunction diagnosis is that it becomes a laundry list that overwhelms rather than a prioritized argument for change. The report must end with a clear "start here."

---

## Reference

Full root cause detail with extended detection signals and remediation patterns:
`references/root-cause-reference.md`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Inspired How To Create Tech Products by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
