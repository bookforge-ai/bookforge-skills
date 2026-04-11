# Hacking Growth — Agent Skills

11 agent skills for growth PMs at Series A–B scaling startups, distilled from
*Hacking Growth* by Sean Ellis and Morgan Brown (Crown Business, 2017). The skills
cover the full growth stack: PMF gating, North Star metric selection, team structure,
high-tempo experimentation, ICE prioritization, acquisition channel scoring, activation
funnel diagnosis, retention phase intervention, monetization experiments, viral loop
design, and quarterly stall prevention. Each skill encodes the reasoning — not just the
steps — so your agent can handle edge cases, not just textbook scenarios.

**Quality baseline:** avg 88 with-skill vs 53 baseline (+35 delta). 11/11 passed.

---

## Install

### Install individual skills via ClawhHub

```bash
clawhub install bookforge/north-star-metric-selector
clawhub install bookforge/product-market-fit-readiness-gate
clawhub install bookforge/growth-experiment-prioritization-scorer
```

### Install the full skill set via Claude Code plugin

```bash
claude plugin install https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth
```

### Clone the repo

```bash
git clone https://github.com/bookforge-ai/bookforge-skills.git
cd bookforge-skills/books/hacking-growth
```

---

## Skills

### Level 0 — Foundation (no prerequisites)

| Skill | Description |
|---|---|
| `product-market-fit-readiness-gate` | Run the Sean Ellis must-have survey (40% threshold) and retention curve analysis to get a binary go/no-go verdict before scaling growth. |
| `growth-team-structure-planner` | Design a cross-functional growth team — product-led vs independent model — and produce an exec-ready proposal with role assignments and kickoff agenda. |
| `north-star-metric-selector` | Construct a multiplicative growth equation and select a defensible North Star Metric that reflects core value delivery, rejecting vanity metrics. |
| `high-tempo-experiment-cycle` | Install the 4-stage weekly experiment cadence (Analyze, Ideate, Prioritize, Test) with meeting agenda, idea capture template, and cadence benchmarks. |

### Level 1 — Growth Levers (depends on Level 0)

| Skill | Description |
|---|---|
| `growth-experiment-prioritization-scorer` | Score and rank a growth experiment backlog using the ICE framework (Impact, Confidence, Ease) to select the top tests for the next sprint. |
| `acquisition-channel-selection-scorer` | Score acquisition channels on Balfour's 6-factor matrix (Cost, Targeting, Control, Input Time, Output Time, Scale) and recommend 2–3 Discovery-phase channels. |
| `activation-funnel-diagnostic` | Map the signup-to-aha-moment funnel, identify the highest-drop-off step, diagnose friction vs positive-friction tradeoffs, and produce ranked experiment candidates. |
| `retention-phase-intervention-selector` | Diagnose which retention phase (initial / medium / long-term) is broken and prescribe phase-appropriate interventions — because week-1 tactics fail for month-6 users. |
| `monetization-experiment-planner` | Classify monetization archetype, run cohort revenue analysis, and propose pricing experiments including 3-tier anchoring, cohort upsell, and penny-gap handling. |
| `viral-loop-designer` | Extract the viral/referral loop pattern from canonical case studies (Dropbox, Hotmail, Airbnb, LinkedIn) and adapt it to your product, modeling K-factor and cycle time. |

### Level 2 — Sustainability (depends on Level 1)

| Skill | Description |
|---|---|
| `growth-stall-prevention` | Run a quarterly audit to detect growth stalls before they compound — review North Star trend, channel concentration, and experiment cadence decay with named recovery actions. |

---

## Quick Start

For a Series A startup asking "are we ready to scale?":

1. Run `product-market-fit-readiness-gate` — get the go/no-go verdict
2. If go: run `north-star-metric-selector` — align the team on what to optimize
3. Run `growth-team-structure-planner` — set up the team structure
4. Run `high-tempo-experiment-cycle` — install the experiment rhythm
5. Run `growth-experiment-prioritization-scorer` with your backlog — pick the first tests
6. Run `acquisition-channel-selection-scorer` — focus channel spend
7. Run `activation-funnel-diagnostic` — fix where users drop off
8. Run `retention-phase-intervention-selector` — fix the retention phase that's broken
9. Once retention is stable: `monetization-experiment-planner` and `viral-loop-designer`
10. Every quarter: `growth-stall-prevention`

### Example prompt

```
Use the north-star-metric-selector skill. My product is a B2B SaaS project
management tool. We have 500 active teams, 80% retain past month 1, and the
core value is helping teams ship projects on time. Help me select a North Star
Metric and build the growth equation.
```

---

## Dependency Graph

```
Level 0:  product-market-fit-readiness-gate   growth-team-structure-planner
          north-star-metric-selector           high-tempo-experiment-cycle
                      |                                    |
Level 1:  acquisition-channel-selection-scorer  growth-experiment-prioritization-scorer
          activation-funnel-diagnostic          retention-phase-intervention-selector
          monetization-experiment-planner       viral-loop-designer
                                  |
Level 2:              growth-stall-prevention
```

Hub: `north-star-metric-selector` (6 dependents)

---

## Source Book

**Hacking Growth: How Today's Fastest-Growing Companies Drive Breakout Success**
Sean Ellis and Morgan Brown — Crown Business, 2017 — ISBN 9780451497215

---

## License

[CC-BY-SA-4.0](LICENSE) — BookForge, 2026.
Skills are derivative works under fair use / transformative commentary.
Source pipeline: https://github.com/bookforge-ai/bookforge
