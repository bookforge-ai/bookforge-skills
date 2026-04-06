# INSPIRED: How to Create Tech Products Customers Love Skills

12 agent skills distilled from **INSPIRED: How to Create Tech Products Customers Love** by Marty Cagan.

These skills teach AI agents how to apply Cagan's product management framework — from assessing product discovery risks and selecting the right discovery techniques, to diagnosing team health, implementing OKRs, and evaluating PM competency. The hub skill maps any product idea to the 4-risk taxonomy and sequences downstream discovery work.

## Skills

### Hub — Discovery Risk Assessment (1 skill)

| Skill | Description |
|-------|-------------|
| product-discovery-risk-assessment | Assess product risks and decide whether to build. Maps any idea to the 4-risk taxonomy (value, usability, feasibility, business viability) and sequences discovery activities. Hub skill for all downstream discovery technique selection. |

### Foundation Skills (6 skills)

| Skill | Description |
|-------|-------------|
| product-okr-implementation | Design and implement an OKR system for product teams — 12 OKR rules, scoring rubric, functional cascade anti-patterns, and a 6–12 month roadmap-to-outcomes transition plan |
| product-team-health-diagnostic | Diagnose why a product team is slow, not innovative, or delivering poor outcomes — 42 criteria across team behaviors, innovation capacity, velocity killers, and design integration |
| product-culture-assessment | Assess product culture across innovation capacity and execution strength — 14 attributes, 2x2 quadrant placement (Dreamers / Factories / Elite / Stalled) |
| product-process-dysfunction-diagnosis | Diagnose why product efforts fail despite using Scrum or Agile — 10 root causes of waterfall-disguised-as-agile patterns across startup, growth, and enterprise stages |
| product-manager-competency-assessment | Evaluate PM competency for hiring, coaching, or self-assessment — VP 4-competency framework and IC PM 4-domain + 3-trait assessment |
| product-vision-strategy-assessment | Assess or create a product vision and strategy — scores vision against 10 principles and strategy against 5 principles with specific rewrite guidance |

### Discovery Technique Skills (5 skills)

| Skill | Description |
|-------|-------------|
| discovery-framing-technique-selection | Select and execute the right discovery framing technique — opportunity assessment, customer letter, or startup canvas based on effort size |
| discovery-prototype-selection | Select the right prototype type and fidelity for any discovery risk — feasibility, user, live-data, or Wizard of Oz prototype |
| value-testing-technique-selection | Select and execute the right value testing technique — 3-level hierarchy (demand / qualitative / quantitative), usability-then-value session protocol |
| customer-discovery-program | Design a customer discovery program to achieve product-market fit — reference customer recruitment, co-development structure, and PMF definition by product type |
| business-viability-stakeholder-testing | Test whether a product solution is viable for the business — 8 stakeholder domains, 1:1 preview sessions, and viability sign-off document |

## Install

```bash
# Claude Code
claude mcp add bookforge-skills https://github.com/bookforge-ai/bookforge-skills

# Or clone directly
git clone https://github.com/bookforge-ai/bookforge-skills.git
```

## Usage

Start with `product-discovery-risk-assessment` for any product discovery effort. The hub skill maps all risks and tells you which downstream skills to invoke.

## License

CC-BY-SA-4.0 — see [LICENSE](LICENSE)

Skills extracted from *INSPIRED: How to Create Tech Products Customers Love* by Marty Cagan (Wiley, 2018). This is a derivative work — original content copyright Marty Cagan / SVPG.
