---
name: product-culture-assessment
description: |
  Assess the product culture of a company or team across innovation capacity and execution strength. Use when a leader, founder, or product manager wants to understand where the organization sits on the innovation-execution spectrum and which cultural gaps to address. Also use when someone asks 'do we have a strong innovation culture?', 'why does our team ship fast but feel uncreative?', 'how do we build a culture like Amazon or Netflix?', 'are we a feature factory?', or 'I need to assess our product culture before proposing changes.' Scores 14 culture attributes (7 innovation + 7 execution), places the organization in one of four quadrants (Dreamers, Factories, Elite, Stalled), and produces a prioritized 90-day improvement roadmap. For diagnosing specific team-level dysfunctions (velocity, design integration, behaviors), use product-team-health-diagnostic instead. For waterfall process issues, use product-process-dysfunction-diagnosis instead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/product-culture-assessment
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
model: sonnet
context: 200k
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Observations, notes, interview outputs, or a written description of how the team/company operates"
    - type: none
      description: "Skill can work from a verbal description of what the person observes in their organization"
  tools-required: []
  tools-optional: []
  environment: "No codebase access required; works from observations and descriptions"
source-books:
  - name: inspired-how-to-create-tech-products
    chapters: [67]
depends-on: []
tags: [product-management, organizational-culture, product-culture]
---

# Product Culture Assessment

## When to Use

Use this skill when you are:
- **Diagnosing stagnation** — the company ships reliably but hasn't had a breakthrough product idea in years
- **Diagnosing chaos** — the company has interesting ideas but they rarely make it to customers in a coherent form
- **Leading a culture change** — you need a baseline before setting improvement goals
- **Onboarding into a leadership role** — you want a structured read on what kind of culture you have inherited
- **Preparing for a retrospective** — your team wants to honestly assess what's working and what isn't
- **Evaluating an acquisition or partnership** — you need to understand how their culture will mesh with yours

Do not use this skill to replace qualitative leadership conversations or team surveys. It produces a structured analytical picture; the human layer of trust and context still matters.

---

## Framework: Two Dimensions of Product Culture

Cagan frames strong product culture across two independent dimensions. A company can be strong or weak on each independently.

**Dimension 1 — Innovation Culture:** Can this organization consistently discover and validate valuable solutions?

**Dimension 2 — Execution Culture:** Can this organization reliably ship and deliver on its commitments?

The goal is to be strong on both. Very few companies are.

---

## Step 1: Score the Innovation Culture Attributes

Score each attribute 1–5:
- **1** = This is not present. No evidence.
- **2** = Weak. Some individuals exhibit this, but it is not systemic.
- **3** = Moderate. Present in some teams or contexts but inconsistent.
- **4** = Strong. Most teams exhibit this most of the time.
- **5** = Exceptional. This is a defining organizational trait.

### I1 — Experimentation

**What it means:** Teams know they can run tests. Some experiments will succeed and many will fail, and this is understood and accepted — not punished.

**Diagnostic signals:**
- Teams regularly run A/B tests, prototypes, or spike experiments *before* committing to build
- Failed experiments are discussed openly without blame
- There is a mechanism and time budget for testing ideas quickly and safely
- Leaders reference failed experiments as learning, not waste

**Red flags:** All product work goes directly to engineering. Prototypes are rare or seen as "extra." Leaders ask for results, not learning.

**Score: ___/5**

---

### I2 — Open Minds

**What it means:** Teams know that good ideas can come from anywhere — customers, engineers, data, competitors — and are not always obvious at the outset.

**Diagnostic signals:**
- Ideas from engineers, support, sales, and customers are actively sought and evaluated
- Leaders don't just greenlight ideas that match their own prior beliefs
- The team questions their assumptions rather than defending initial positions
- Counterintuitive ideas get a fair hearing

**Red flags:** All product direction comes top-down. Engineers are told what to build with no opportunity to contribute ideas. Data that contradicts strategy is dismissed.

**Score: ___/5**

---

### I3 — Empowerment (Innovation)

**What it means:** Individuals and teams feel empowered to pursue and try out an idea — they don't need executive approval for every small experiment.

**Diagnostic signals:**
- Teams have dedicated time and budget to explore ideas
- Individuals can prototype something without a six-week approval cycle
- Leaders set outcomes, not prescribe solutions
- Teams feel ownership over discovery, not just delivery

**Red flags:** Every experiment requires sign-off. Teams wait for leadership to greenlight ideas. Product managers act as ticket-takers rather than problem-solvers.

**Score: ___/5**

---

### I4 — Technology Orientation

**What it means:** Teams recognize that true innovation can be inspired by new technology and data analysis, not just by listening to customers. Engineers are involved early in discovery — not handed specs.

**Diagnostic signals:**
- Engineers participate in customer discovery and problem definition
- Technology possibilities inform product direction (not just customer requests)
- Data analysis generates product hypotheses, not just dashboards
- The organization invests in engineer awareness of emerging technology

**Red flags:** Engineers are brought in only after the product is fully specified. Technology is treated as a cost center rather than a source of ideas. Discovery is solely the product manager's job.

**Score: ___/5**

---

### I5 — Business and Customer Savvy Teams

**What it means:** Teams — including developers — have a deep understanding of both the business context (constraints, revenue model, strategy) and the users and customers they are building for.

**Diagnostic signals:**
- Developers can articulate who the customer is and what problem the product solves
- Teams understand revenue, margins, and business constraints relevant to their work
- Teams have direct access to users and customers (not just through product managers)
- Business strategy is communicated broadly, not held only at leadership level

**Red flags:** Engineering teams don't know the customers. Business goals are hidden from teams. Customer access goes only through a few designated gatekeepers. Teams build features without knowing why they matter.

**Score: ___/5**

---

### I6 — Skill-Set and Staff Diversity

**What it means:** Teams appreciate that different skills and backgrounds — especially the combination of engineering, design, and product — contribute to innovative solutions.

**Diagnostic signals:**
- Product, design, and engineering are treated as equally important contributors
- Design is not a cost center or a finishing layer applied after engineering
- Teams include diverse perspectives and this is seen as a strength, not a management challenge
- Hiring reflects deliberate effort to balance and diversify skill sets

**Red flags:** Design is brought in at the end to "make it look good." All team members share the same background. Product managers are the only ones allowed to have product opinions.

**Score: ___/5**

---

### I7 — Discovery Techniques

**What it means:** The mechanisms are in place for ideas to be tested quickly and safely — protecting the brand, revenue, customers, and colleagues from the risk of unvalidated ideas going straight to production.

**Diagnostic signals:**
- Teams have an established set of discovery techniques (user interviews, prototypes, live-data tests)
- There is a shared vocabulary and practice for de-risking ideas before building
- Teams know how to test value risk, usability risk, feasibility risk, and business viability risk
- Experimentation infrastructure (feature flags, analytics, user research access) exists

**Red flags:** "Discovery" means writing a PRD and getting it approved. No shared toolbox for running quick tests. Every idea goes to a full sprint before getting any validation signal.

**Score: ___/5**

---

**Innovation Culture Score: ___/35**

| Range | Label |
|-------|-------|
| 28–35 | Strong innovation culture |
| 18–27 | Moderate — some capability, significant gaps |
| 7–17 | Weak innovation culture |

---

## Step 2: Score the Execution Culture Attributes

Use the same 1–5 scale.

### E1 — Urgency

**What it means:** People feel like they are operating in a high-stakes environment where slow movement has real consequences. This is not manufactured stress — it is a genuine sense that speed matters.

**Diagnostic signals:**
- Teams default to "what's the fastest way to learn or ship this?" not "what's the safest schedule?"
- Leaders convey why urgency matters without manufacturing false crises
- Blockers are removed fast; people don't wait weeks for decisions
- Teams feel the market and competitive pressure, not just internal process

**Red flags:** Teams estimate generous timelines with large buffers by default. Slow velocity is normalized. Urgency is manufactured as pressure rather than genuinely felt. No one feels consequences of delay.

**Score: ___/5**

---

### E2 — High-Integrity Commitments

**What it means:** Teams understand the value of commitments and insist on making them with integrity — meaning they commit to outcomes they genuinely believe are achievable, and they flag risk early rather than hiding it.

**Diagnostic signals:**
- Teams push back on unrealistic timelines and negotiate rather than just accept
- When teams commit, they mean it — commitments are not routinely broken
- Teams surface risks and blockers proactively, not on the day of the deadline
- Commitments are tracked and treated as genuine obligations, not aspirational goals

**Red flags:** Teams agree to everything asked of them, then miss most of it. Leadership sets dates without team input. Slipped commitments are consistently explained away. There is no culture of accountability for missing what was promised.

**Score: ___/5**

---

### E3 — Empowerment (Execution)

**What it means:** Teams feel they have the tools, resources, and permission to do whatever is necessary to meet their commitments — they are not blocked by bureaucracy when trying to deliver.

**Diagnostic signals:**
- Teams can make architectural decisions without committee approval
- Necessary tools, environments, and infrastructure are available
- Teams can resolve cross-team dependencies without escalating to leadership
- Blockers are cleared quickly; people don't feel like they need permission to act

**Red flags:** Teams routinely blocked waiting for approvals. Engineers can't deploy without a week-long release process. Simple decisions require escalation. Teams feel helpless in the face of cross-team dependencies.

**Score: ___/5**

---

### E4 — Accountability

**What it means:** People and teams feel a deep responsibility to meet their commitments. Accountability has consequences — not necessarily being fired, but consequences to reputation among peers when commitments are broken or avoided.

**Diagnostic signals:**
- Missed commitments are discussed honestly in retrospectives, not minimized
- There is peer pressure (constructive) to follow through on what was promised
- Leaders model accountability — they own failures as well as successes
- Repeated misses have real consequences for reputation and trust

**Red flags:** Missed commitments are consistently blamed on external factors. No one is ever held responsible. Poor performers are tolerated indefinitely. Accountability is treated as a management concept, not a team value.

**Score: ___/5**

---

### E5 — Collaboration

**What it means:** While team autonomy and empowerment are important, teams understand they must work together to accomplish the biggest and most meaningful objectives.

**Diagnostic signals:**
- Teams proactively share dependencies and coordinate across team boundaries
- There is a spirit of helping other teams unblock — not hoarding resources
- Leaders model cross-functional collaboration at the top
- Teams celebrate joint wins, not just individual team outcomes

**Red flags:** Teams optimize only for their own roadmap. Cross-team work is seen as a burden. Dependencies are discovered late. There is strong "silo" behavior. Teams blame each other for failures.

**Score: ___/5**

---

### E6 — Results Orientation

**What it means:** The focus is on outcomes — did this work actually move the needle for the customer and the business? — not outputs (did we ship the feature on time?).

**Diagnostic signals:**
- Teams track and review the actual impact of shipped work
- Product success is measured by business and customer outcomes, not delivery metrics
- Leaders ask "did it work?" not just "did it ship?"
- Teams feel embarrassed by features that shipped but had no impact

**Red flags:** Sprint velocity is the primary productivity metric. Teams are praised for shipping regardless of whether it worked. No post-launch reviews or outcome measurement. Features are never removed even when they clearly don't work.

**Score: ___/5**

---

### E7 — Recognition

**What it means:** Teams take their cues from what is rewarded and what is accepted. Recognition should reinforce both innovation (trying and learning) and execution (delivering on commitments) — not just one at the expense of the other.

**Diagnostic signals:**
- Teams that ship hard commitments are recognized and celebrated
- Teams that run smart experiments and learn — even when the result is "no" — are also recognized
- Missing commitments is not casually excused in ways that normalize it
- Recognition is consistent with the stated values of the organization

**Red flags:** Only the team with the most exciting new idea gets recognized. Execution teams feel invisible. Or conversely: only on-time delivery is celebrated and no one is recognized for discovery work. Recognition is random and disconnected from what the company says it values.

**Score: ___/5**

> **Fast-acting lever:** E7 (Recognition) is the highest-leverage culture attribute to change quickly. Leaders control recognition directly and immediately — no organizational restructuring required. If the assessment reveals a gap between stated values and what is actually celebrated, adjusting recognition patterns (in all-hands meetings, team updates, manager behavior) produces a visible cultural signal within weeks. Other attributes (E4 Accountability, I3 Empowerment) take quarters to shift. Start with E7 if you need early momentum.

---

**Execution Culture Score: ___/35**

| Range | Label |
|-------|-------|
| 28–35 | Strong execution culture |
| 18–27 | Moderate — some capability, significant gaps |
| 7–17 | Weak execution culture |

---

## Step 3: Plot the 2x2 Diagnostic Grid

Use the two dimension scores to place the organization in one of four quadrants.

```
                    EXECUTION CULTURE
                 Weak (7–17)    Strong (28–35)
               ┌──────────────┬──────────────┐
  Strong       │              │              │
  (28–35)      │  DREAMERS    │  ELITE       │
               │              │              │
INNOVATION     │ High idea    │ Amazon,      │
CULTURE        │ volume, low  │ Google,      │
               │ delivery.    │ Netflix.     │
               │ Chaos risk.  │ Rare.        │
               ├──────────────┼──────────────┤
  Weak         │              │              │
  (7–17)       │  STALLED     │  FACTORIES   │
               │              │              │
               │ Weak both.   │ Ship fast,   │
               │ Usually      │ wrong things.│
               │ legacy cos.  │ Feature      │
               │              │ factory risk.│
               └──────────────┴──────────────┘
```

### Quadrant Profiles

**ELITE (also: PIONEERS) — Strong Innovation + Strong Execution**
The rarest quadrant. These organizations have cracked both discovery and delivery. They innovate consistently and ship reliably. Examples: Amazon, Google (historically), Netflix. Behavioral signature: teams simultaneously run discovery experiments AND ship reliable commitments without tension between the two. Post-mortems happen for both failed experiments and missed deliveries. Note: these are often intense work environments. The combination of urgency, accountability, and experimentation creates pressure. Not everyone thrives here.

**DREAMERS — Strong Innovation + Weak Execution**
Strong ideation, weak delivery. The organization has good instincts and can generate interesting ideas, but struggles to ship them in a coherent and timely way. Common in early-stage startups and creative agencies. Behavioral signature: the backlog is full of half-validated ideas; commitments slip regularly; teams celebrate the idea more than the outcome. The risk: good ideas die in the delivery bottleneck, or ship so late the market has moved on.

**FACTORIES — Weak Innovation + Strong Execution**
The most common trap for established companies. Efficient at delivering what is asked of them, but the wrong things are being asked. Feature factories. Velocity is high, but the roadmap is driven by the loudest stakeholders rather than validated customer problems. Teams feel like order-takers. Behavioral signature: engineers are handed specs, not problems; discovery means writing a PRD; teams are evaluated on delivery metrics, not customer outcomes. Innovation capacity has atrophied.

**STALLED (also: DECLINING) — Weak Innovation + Weak Execution**
Often older companies that lost their product instincts long ago but have a strong brand or customer base to lean on. Behavioral signature: low urgency, low curiosity, low accountability — teams ship slowly AND the shipped work doesn't move metrics. The hardest to turn around because neither capability is present. Requires significant leadership change and culture investment.

---

## Step 4: Identify the Highest-Leverage Gaps

From the 14 individual attribute scores, identify the three lowest scores. These are the highest-leverage improvement opportunities.

### Prioritization Logic

- If you are in the **FACTORIES** quadrant: Innovation gaps are the priority. Look at I1 (Experimentation), I3 (Empowerment), I7 (Discovery Techniques) first.
- If you are in the **DREAMERS** quadrant: Execution gaps are the priority. Look at E2 (High-Integrity Commitments), E4 (Accountability), E6 (Results Orientation) first.
- If you are in the **STALLED** quadrant: Start with E3 (Execution Empowerment) and I3 (Innovation Empowerment) — both depend on teams feeling like they can actually act.
- If you are in the **ELITE** quadrant: Focus on sustaining. Look at which attributes dropped since last assessment and investigate root causes before they compound.

---

## Step 5: Produce the Assessment Output

Deliver a structured report with the following sections:

### 1. Culture Scores Summary

| Attribute | Score |
|-----------|-------|
| I1 — Experimentation | /5 |
| I2 — Open Minds | /5 |
| I3 — Empowerment (Innovation) | /5 |
| I4 — Technology Orientation | /5 |
| I5 — Business & Customer Savvy | /5 |
| I6 — Skill-Set Diversity | /5 |
| I7 — Discovery Techniques | /5 |
| **Innovation Total** | **/35** |
| E1 — Urgency | /5 |
| E2 — High-Integrity Commitments | /5 |
| E3 — Empowerment (Execution) | /5 |
| E4 — Accountability | /5 |
| E5 — Collaboration | /5 |
| E6 — Results Orientation | /5 |
| E7 — Recognition | /5 |
| **Execution Total** | **/35** |

### 2. Quadrant Placement

State clearly which quadrant the organization is in and what that means for the improvement agenda.

### 3. Top Three Gaps

For each of the three lowest-scoring attributes:
- What is missing (specific behavioral evidence)
- Why it matters for the organization's goals
- One concrete first action to start closing the gap

### 4. Strengths to Protect

Identify 2–3 attributes that scored highest. These represent existing cultural assets that improvement efforts should not inadvertently erode.

### 5. Recommended Focus for the Next 90 Days

A single-sentence framing of the most important cultural shift to make, given quadrant position and the specific gap pattern identified.

---

## Anti-Patterns: Culture Change Theater

When organizations attempt to improve product culture, they frequently adopt surface-level practices that mimic the behaviors of high-performing cultures without addressing the underlying conditions. These anti-patterns produce the appearance of change while the actual culture stays the same. Flag them when assessing improvement plans.

**Cargo cult innovation** — Running hackathons, design sprints, or "innovation days" without actually empowering teams to pursue validated ideas afterward. The hallmark: ideas generated in innovation events are never resourced or followed up. Teams learn quickly that the event is theater; it doesn't change what gets built. A team that can run an experiment every quarter but cannot greenlight any result scores low on I3 (Empowerment) regardless of how many hackathons it hosts.

**Process theater** — Adopting Agile ceremonies (stand-ups, retrospectives, sprint planning) without product discovery. Teams run two-week sprints and hold retrospectives, but the work going into the sprints was handed to them as a feature list. Discovery — the work of figuring out what to build — never happens. The ceremonies create the appearance of an empowered, modern team. The actual work model is waterfall with shorter release cycles. Scores low on I7 (Discovery Techniques) and I3 (Empowerment) despite high ceremony adoption.

**Values-recognition gap** — The company posts its values on the wall ("customer obsession," "move fast," "own the outcome") but recognizes and rewards the opposite (shipping on time, avoiding visible failure, deferring to leadership). This is the most reliable diagnostic signal that E7 (Recognition) is broken: ask teams what behaviors actually get people promoted or praised, then compare to stated values.

---

## Reference

See `references/culture-attribute-definitions.md` for the full definitions of all 14 attributes as described by Cagan.

---

## References

- Cagan, Marty. *INSPIRED: How to Create Tech Products Customers Love*, 2nd ed. Wiley, 2018. Chapter 67.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Inspired How To Create Tech Products by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
