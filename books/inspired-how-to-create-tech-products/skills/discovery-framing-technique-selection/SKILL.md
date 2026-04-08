---
name: discovery-framing-technique-selection
description: "Select and execute the right discovery framing technique before building. Use when value risk is High and the underlying problem is not yet clearly defined, when a team is about to start discovery without a shared problem statement, when someone asks 'how should we frame this discovery effort?', or when starting any non-trivial feature, redesign, or new product effort. Also use for: writing an opportunity assessment, writing a customer letter (press release alternative), completing a startup canvas for a new business, or constructing a story map to scope discovery. Determines effort size (typical/large/new-product), selects the matching technique, and produces the framing document. Best triggered after product-discovery-risk-assessment. For specific testing techniques, use value-testing-technique-selection. For prototype selection, use discovery-prototype-selection."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/discovery-framing-technique-selection
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [35, 36, 37, 38]
tags: [product-management, product-discovery, discovery-framing]
depends-on: [product-discovery-risk-assessment]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Product idea, feature proposal, initiative description, or risk assessment output from product-discovery-risk-assessment"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document-based product management environment"
discovery:
  goal: "Produce a framing document that aligns the full product team on the problem before discovery begins"
  tasks:
    - "Classify the effort by size and type"
    - "Select the appropriate framing technique"
    - "Execute the selected technique step by step"
    - "Produce the framing document using the matching output template"
    - "Optionally construct a story map to scope discovery planning"
  audience:
    roles: [product-manager, product-leader, startup-founder, tech-lead]
    experience: any
  when_to_use:
    triggers:
      - "Starting product discovery and the underlying problem is not clearly defined"
      - "Value risk is High in the risk assessment from product-discovery-risk-assessment"
      - "Team is about to begin discovery work without a shared problem statement"
      - "Beginning any feature, redesign, or new product effort"
      - "Need to align team and stakeholders on what problem we are solving before ideating solutions"
    prerequisites:
      - "product-discovery-risk-assessment completed, or at minimum a product idea / initiative description is available"
    not_for:
      - "Executing prototype, testing, or ideation techniques (use downstream skills)"
      - "Post-build retrospectives or delivery planning"
      - "Efforts where the problem is already well-defined and team is aligned"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: ""
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
---

# Discovery Framing Technique Selection

## When to Use

Apply this skill at the start of any product discovery effort, specifically when:
- Value risk is High and the problem is ambiguous or handed to you as a solution without a clear problem statement
- The team lacks a shared understanding of what problem they are solving
- You are about to assign discovery tasks and need a common frame first

This skill produces a **framing document** — not a solution, not a prototype. Framing clarifies the problem space so all subsequent discovery work is aimed at the right target.

Do NOT skip framing. Teams that skip directly to prototyping or building are, by definition, solving a problem they have not clearly defined.

## Context and Input Gathering

Before selecting a technique, collect:

1. **Initiative description** — What has been proposed? Feature, redesign, or entirely new product/business?
2. **Business objective** — What OKR or company goal does this serve?
3. **Known customer problem** — What pain or job-to-be-done is this addressing?
4. **Target customer** — Which user or buyer persona is primary?
5. **Scope signals** — How many distinct business objectives are involved? Is there an existing product and business model, or is this a new product/business?

If a risk assessment document from `product-discovery-risk-assessment` exists, read it — the "Dependencies for Downstream Skills" section will confirm whether framing is needed and why.

## Process

### Step 1: Classify the Effort by Size

Apply this decision tree to determine effort size:

**Question A: Is this effort aimed at creating an entirely new product or entering a new business?**
- Yes → **New Product / New Business** effort → use **Startup Canvas**

**Question B (if A = No): Does this effort involve multiple business objectives, multiple customer problems, or affect both existing and new customers simultaneously?**
- Yes → **Large Effort** (e.g., redesign, platform shift) → use **Customer Letter**

**Question C (if A and B = No): Is this a typical feature, improvement, or single-objective initiative?**
- Yes → **Typical-to-Medium Effort** → use **Opportunity Assessment**

**WHY:** The framing technique must match the scope of the effort. An opportunity assessment answers four questions in minutes — sufficient for most product work. But a redesign with multiple objectives cannot be adequately framed in four questions; the customer letter forces the team to work through the complexity. A new product requires validating business model risks that don't exist for established products; only the startup canvas covers those dimensions. Using the wrong technique for the scope produces either under-framed (missed objectives) or over-engineered (wasted effort) framing.

**Assert:** You have classified the effort as one of: Typical-to-Medium, Large, or New Product / New Business.

### Step 2: Execute the Selected Technique

Follow the section below that matches your effort classification. Skip the other two sections.

---

#### Technique A: Opportunity Assessment (Typical-to-Medium Efforts)

**Use when:** Single feature, improvement, or single-objective initiative. Most product work falls here.

**Time required:** Minutes to one hour. This is intentionally lightweight.

**Execution:**

Answer these four questions precisely. Do not write essays — each answer should be one to three sentences.

**Question 1 — Business Objective (Objective)**
What business objective does this work address? Your answer must map to at least one of your team's assigned OKRs or top-level company objectives. If the work cannot be tied to any assigned objective, stop: clarify with leadership before proceeding.

*WHY:* Product work that cannot be connected to an assigned business objective is not prioritized work — it is speculative. Framing forces this connection explicitly before any discovery time is spent.

**Question 2 — Key Results (Key Results)**
How will you know if you have succeeded? State at least one measurable outcome. Example: "Reduce 30-day churn by 15%" or "Increase trial-to-paid conversion by 10 percentage points." A 1% improvement and a 20% improvement are very different success thresholds — define this now so the team knows what discovery evidence they are looking for.

*WHY:* Without a stated measure of success, the team cannot evaluate discovery findings or know when the problem is solved. Key results set the bar that discovery work must clear.

**Question 3 — Customer Problem (Customer Problem)**
What problem will this solve for customers? State the customer pain, not the product feature. If this addresses internal users, note that — but still tie it back to end-customer benefit where possible.

*WHY:* Teams default to feature enumeration. This question forces the pivot from output thinking ("we will build X") to outcome thinking ("customers currently struggle with Y"). The customer problem statement is the anchor for all downstream prototype and testing work.

**Question 4 — Target Market (Target Market)**
Which type of customer or user is the primary beneficiary? Be specific: a user persona, a customer segment, or a job-to-be-done context. "Everyone" is not an acceptable answer — products that try to please everyone please no one.

*WHY:* Target market definition determines who you recruit for discovery testing and which customer insights are signal versus noise. Lack of specificity causes teams to collect contradictory feedback and prototype for multiple incompatible mental models simultaneously.

**After answering all four questions:** Share the completed opportunity assessment with the full product team (product manager, designer, engineer) and key stakeholders before beginning discovery. Every team member must understand the answers before discovery work starts.

**Output:** Use the Opportunity Assessment template in the Outputs section.

---

#### Technique B: Customer Letter (Large Efforts)

**Use when:** Multiple business objectives, multiple customer problems, redesigns, or efforts that must serve both existing and new customers.

**Time required:** Several hours to one day. This is a more demanding technique.

**Execution:**

Write two imagined documents — a customer letter and a CEO response — set in the future after the product or redesign has launched successfully.

**Part 1 — The Customer Letter**

Write a letter from a specific, well-defined customer persona (use a real persona if one exists, or name a hypothetical representative customer) to the company's CEO. The letter must:

- Be written in the voice of the customer — their language, their problems, their frame of reference
- Explain what the customer's life or work was like before the product/redesign (the pain)
- Explain how the new product/redesign changed or improved their life (the benefit)
- Be specific about what changed — not vague praise ("it's so much better!") but concrete outcomes ("I used to spend two hours reconciling invoices each week; now it takes ten minutes")
- Address the primary customer benefit, not a list of features

*WHY:* Writing in the customer's voice prevents the team from defaulting to feature enumeration. The customer does not care about your architecture decisions or your internal roadmap; they care about whether their problem is solved. The letter format creates empathy — when the team reads a letter from a real-seeming customer describing real pain, they understand the problem viscerally, not abstractly. This is qualitatively different from a bullet-point list of requirements.

**Part 2 — The CEO Response**

Write an imagined congratulatory response from the CEO to the product team, explaining:

- How this product/redesign has helped the business (in business terms: revenue, retention, market position, customer satisfaction)
- Why the company's investment in this effort was worthwhile
- What the business outcome has been

*WHY:* The CEO response makes the business case explicit. It forces the product manager to think through what "success" looks like from the company's perspective — not just the customer's. This surfaces business viability considerations early: if you cannot write a plausible CEO response, the business case is not yet clear.

**After writing both documents:** Review with the product team and key stakeholders. If colleagues cannot get excited about the customer letter, the framing has more work to do, or the effort should be reconsidered.

**Output:** Use the Customer Letter template in the Outputs section.

---

#### Technique C: Startup Canvas (New Product / New Business)

**Use when:** Entirely new product, early-stage startup, or enterprise initiative to enter a new business that does not share the existing product's distribution, monetization, or customer base.

**Time required:** One to several days. This is the most comprehensive framing technique.

**Execution:**

Complete all nine cells of the canvas. Do not skip cells — each represents a risk that must be surfaced, not deferred.

**Critical warning:** The most common failure mode when using a canvas is spending disproportionate time on business model risks (monetization, channels, cost structure) while leaving solution risk underspecified. Solution risk — discovering a compelling solution that customers will choose to buy — is the primary risk for most new products. It must be addressed directly in discovery, not delegated to engineers after the canvas is complete.

Complete each cell:

**1. Problem**
State the top one to three customer problems you are solving. Be specific about who experiences them and how painful they are. Do not describe your solution here.

**2. Customer Segments**
Who are the target customers? Which segment is the most important early adopter? Distinguish between users (who interact with the product) and buyers (who pay for it) if different.

**3. Unique Value Proposition**
What is the single, clear, compelling reason a customer will choose your product over all alternatives (including doing nothing)? This is a headline, not a feature list. Note: to get someone to switch to a new product, it must be demonstrably and substantially better than existing alternatives — comparable is not sufficient.

**4. Solution**
Describe the solution at the concept level — enough to validate against the problem, not enough to specify engineering. This cell is intentionally lightweight: the solution will be refined through discovery. The startup canvas is not the place to lock in a solution.

**5. Channels**
How will you reach customers and deliver the product to them? Specify distribution and go-to-market channels. If these are unknown, that is a risk to flag.

**6. Revenue Streams**
How will this product make money? Pricing model, transaction type, and revenue expectations. If monetization is uncertain, note it — this is a risk to validate.

**7. Cost Structure**
What are the major costs to build, deliver, and support this product? Are there cost thresholds that would make the business unviable?

**8. Key Metrics**
What numbers will you track to know if the product is succeeding? Select metrics that reflect actual customer value, not just usage volume.

**9. Unfair Advantage**
What does your team or company have that competitors cannot easily replicate? This is honest — if you have no unfair advantage at this stage, leave it blank and note this as a strategic risk.

**After completing the canvas:** Share with the product team, relevant stakeholders, and advisors. Use it as a living document — update it as discovery progresses. The canvas is a starting map, not a contract.

**Output:** Use the Startup Canvas template in the Outputs section.

---

### Step 3: Construct a Story Map (Optional — Planning Complement)

A story map is a two-dimensional visualization of a product's user experience. Use it alongside any framing technique when the effort involves multiple user activities or when you need to scope discovery work across a complex system. It is especially useful for large efforts and new product discovery.

**When to build a story map:**
- The framing involves multiple distinct user activities
- You need to scope discovery into releases or phases
- The team needs a shared visual of what the system does before prototyping begins

**How to construct:**

**Horizontal axis — User Activities (left to right, time-ordered)**
List the major activities a user performs with the product. Order them as a user would encounter them, left to right. For a checkout system: browse → select → configure → pay → confirm → track. These are the column headers.

*WHY:* Horizontal ordering reflects the user's experience over time, not a product feature taxonomy. This prevents organizing the map around engineering modules (which have no inherent temporal order) and keeps the team anchored to user journeys.

**Vertical axis — Tasks (top to bottom, critical to optional)**
Under each activity, list the specific user tasks that make up that activity. Place critical tasks near the top, optional or edge-case tasks lower. There is no fixed number — add as many tasks as are relevant.

*WHY:* Vertical ordering enables release planning. Drawing a horizontal "release line" across the map at any vertical position defines a release: everything above the line is in; everything below is deferred. This is fundamentally better than a flat backlog, where there is no natural release boundary and prioritization requires arbitrary judgment.

**Draw the release line**
After populating the map, draw a release line that defines the minimum viable release — the row that, if delivered, provides meaningful value to the target user. Everything above that line is in scope for the first release. Everything below is deferred.

**Keep it current**
As discovery progresses and you receive feedback from prototype testing, update the story map to reflect what you learn. When discovery transitions to delivery, the tasks above the release line move directly into the product backlog with full context intact.

**Assert:** If a story map was built, it includes: at least three user activities on the horizontal axis, tasks ranked by criticality on the vertical axis, and a visible release line.

### Step 4: Share and Validate Alignment

Regardless of which technique was used:

1. Share the framing document with the full product team (product manager, designer, engineer) before any discovery work begins.
2. Confirm every team member can answer: What problem are we solving? For whom? How will we know we succeeded?
3. Share with key stakeholders to confirm the business objective and success measures are correct.
4. If stakeholders or team members cannot get aligned around the framing document after one revision, escalate — this is a signal of a deeper organizational misalignment that discovery cannot resolve.

**Assert:** Framing document has been reviewed by the product team and at least one key stakeholder before discovery activities begin.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Initiative description | Yes | What is being proposed — feature, redesign, or new product |
| Risk assessment output | Recommended | Output from product-discovery-risk-assessment, confirms framing is needed |
| Business objectives / OKRs | Yes | The team's assigned objectives for this period |
| Customer personas | Recommended | Existing persona definitions for the target customer |
| Existing business model context | For Technique C | Revenue model, channels, cost structure if it exists |

## Outputs

### Output Template A: Opportunity Assessment

```
# Opportunity Assessment: [Initiative Name]

Date: [YYYY-MM-DD]
Author: [Product Manager Name]
Status: Draft / Reviewed / Approved

## Business Objective
[Which assigned OKR or company objective does this address? One to two sentences.]

## Key Results
[How will we measure success? State at least one specific, measurable outcome.]
Example: Reduce 30-day churn rate from X% to Y% / Increase trial-to-paid conversion by Z points

## Customer Problem
[What problem does this solve for customers? State the pain, not the feature.]

## Target Market
[Which specific user or customer segment is the primary beneficiary?]

## Distribution
Share with: [Names of product team members + key stakeholders]
Reviewed by: [ ]
```

### Output Template B: Customer Letter

```
# Customer Letter: [Initiative Name]

Date: [YYYY-MM-DD]
Author: [Product Manager Name]
Customer Persona: [Name of persona or representative customer archetype]

---

## Letter from Customer to CEO

Dear [CEO Name],

I wanted to write and tell you how much [product/redesign name] has changed [my work / my life].

Before [product/redesign], I used to [describe the pain — specific, concrete, in the customer's voice].
This meant [consequence of the pain — time lost, money wasted, frustration, etc.].

Now, [describe what changed — specific outcomes, not feature lists].
[Optional: specific time/money/effort saved, or qualitative change in experience.]

I [recommend this / have told my colleagues / renewed our subscription] because [specific reason].

Thank you,
[Customer Name]
[Customer Title / Context]

---

## CEO Response to Product Team

Team,

I wanted to share this letter we received from [customer name / customer segment].

This is exactly what we were aiming for with [initiative name]. The work you did has [business outcome: improved retention / driven X new customers / expanded into Y market / improved NPS by Z points].

[One to two sentences on why this mattered to the business — revenue, competitive position, mission.]

Well done.
[CEO Name]

---

## Internal Notes
Business objectives addressed: [list]
Success measures: [list — what we will track to know this worked]
Target market: [specific segment this letter represents]
Share with: [product team + key stakeholders]
Reviewed by: [ ]
```

### Output Template C: Startup Canvas

```
# Startup Canvas: [Product / Business Name]

Date: [YYYY-MM-DD]
Author: [Product Manager / Founder]
Status: Draft / Version N

| Cell | Content |
|------|---------|
| Problem | [Top 1-3 customer problems. Who has them. How painful.] |
| Customer Segments | [Primary target segment. Early adopter profile. User vs. buyer distinction.] |
| Unique Value Proposition | [Single clear reason customers will choose this over all alternatives, including inaction.] |
| Solution | [Concept-level description. Not an engineering spec. Subject to change through discovery.] |
| Channels | [How you reach and deliver to customers.] |
| Revenue Streams | [Pricing model, transaction type, revenue expectations.] |
| Cost Structure | [Major costs to build, deliver, support.] |
| Key Metrics | [What you will track to know the product is succeeding.] |
| Unfair Advantage | [What competitors cannot easily replicate. Honest — blank if none yet.] |

## Primary Risk: Solution Risk
[Describe what a compelling solution looks like. How will you discover it? What does
"demonstrably and substantially better than alternatives" mean in this specific context?]

## Discovery Priority
1. Solution risk (value risk) — must be resolved first
2. [Next risk in priority order]
3. ...

## Living Document Log
| Version | Date | What Changed | Why |
|---------|------|-------------|-----|

Share with: [product team + stakeholders + advisors]
Reviewed by: [ ]
```

### Output Template D: Story Map (Complement to Any Technique)

```
# Story Map: [Initiative Name]

Date: [YYYY-MM-DD]
Version: [N]

## User Activities (horizontal — left to right, time-ordered)
| Activity 1 | Activity 2 | Activity 3 | Activity 4 | ... |
|-----------|-----------|-----------|-----------|-----|

## Tasks by Activity (vertical — critical at top, optional below)

### [Activity 1]
- [Critical task 1]
- [Critical task 2]
---- RELEASE LINE ----
- [Optional task 1]
- [Optional task 2]

### [Activity 2]
- [Critical task 1]
- [Critical task 2]
---- RELEASE LINE ----
- [Optional task 1]

[Continue for each activity]

## Release Scope
**Release 1 (above line):** [Summary of what ships in first release]
**Deferred (below line):** [Summary of what is explicitly deferred]

## Change Log
| Date | What Changed | Discovery Signal That Prompted It |
|------|-------------|----------------------------------|
```

## Key Principles

1. **Framing is not optional.** Every product effort, regardless of size, must be framed before discovery begins. The technique scales — the need does not disappear.
2. **Effort size determines technique.** Opportunity assessment for typical work. Customer letter for large multi-objective work. Startup canvas for new products. Applying the wrong technique produces either under-framing or wasted effort.
3. **The framing document defines what discovery must prove.** Key results and customer problem statements set the success threshold. Discovery evidence either clears this bar or it does not.
4. **Framing is a team activity, not a PM artifact.** The product manager authors the document, but every team member must understand and be aligned with the answers before discovery begins.
5. **Solution risk is primary.** For startup canvas use: do not spend most of your time on business model risks while leaving solution risk underspecified. A compelling solution unlocks all other risks; an elegant business model with no compelling solution is worthless.
6. **Customer letter beats press release.** Writing in the customer's voice creates empathy the team can feel, not just understand. If the team cannot get excited about the customer letter, the framing has more work to do.
7. **Story maps are living documents.** Update them as discovery produces learning. When discovery transitions to delivery, the story map becomes the backlog source of truth.

## Examples

### Example 1: Opportunity Assessment for a B2B Feature

**Initiative:** Add bulk export functionality to a project management tool.

**Effort classification:** Typical — single feature, single objective.

**Opportunity Assessment:**
- Business Objective: Reduce trial-to-paid churn (maps to OKR: "Improve 30-day retention from 42% to 55%")
- Key Results: Reduce cancellation reason "missing export" from 18% of churn responses to below 5%
- Customer Problem: Enterprise users cannot extract project data for executive reporting without manually copying rows — a two-hour-per-month task that creates frustration and support tickets
- Target Market: Enterprise trial users managing 10+ projects with executive reporting obligations

### Example 2: Customer Letter for a Redesign

**Initiative:** Redesign mobile onboarding for a consumer finance app (multiple objectives: reduce drop-off, improve feature discovery, differentiate from competitors).

**Effort classification:** Large — multiple objectives, both existing and new customers affected.

**Customer letter written from persona:** "Maria, a 28-year-old first-time investor, writing six months after the redesign launched."

The letter describes: confusion with the original seven-step onboarding, almost deleting the app, then returning after a friend recommended it post-redesign. Now completes onboarding in under three minutes, discovered portfolio tracking on day one, has referred two friends.

CEO response acknowledges: 41% improvement in onboarding completion, 23% increase in feature discovery within first week, highest App Store rating in company history.

### Example 3: Startup Canvas for a New Product

**Initiative:** A B2B startup building an AI-powered contract review tool for small law firms.

**Effort classification:** New product / new business.

**Canvas note on solution risk:** "We have filled in all nine cells, but the most important work is discovering whether we can build a contract review experience that is demonstrably faster and more accurate than a junior associate. That is the solution risk that all other canvas cells depend on. We will spend the first four weeks of discovery exclusively on this."

## References

- `references/framing-technique-comparison.md` — Side-by-side comparison of all three framing techniques with selection criteria and tradeoffs
- `references/opportunity-assessment-examples.md` — Worked examples of opportunity assessments across different product types
- `references/customer-letter-guide.md` — Detailed guidance on writing the customer letter and CEO response, including common failure modes
- `references/startup-canvas-guide.md` — Full startup canvas guidance with risk prioritization and the "biggest risk" warning
- `references/story-map-guide.md` — Step-by-step story map construction, release line drawing, and backlog transition guidance

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-product-discovery-risk-assessment`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
