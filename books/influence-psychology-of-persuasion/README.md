# Influence: The Psychology of Persuasion

10 agent skills for ethical persuasion strategy, influence defense, and content optimization, extracted from **Influence: The Psychology of Persuasion** by Robert B. Cialdini.

These skills teach AI agents how to apply Cialdini's 6 principles of influence — reciprocity, commitment and consistency, social proof, liking, authority, and scarcity — to marketing, sales, copywriting, and negotiation contexts. They also cover defense: detecting when each principle is being used against you and responding with a principle-specific counter-strategy.

**Average quality delta: +43 points** (95% with-skill vs 52% baseline).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/influence-psychology-of-persuasion
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| influence-principle-selector | Identify which of Cialdini's 6 principles to apply — scoring each against your scenario with rationale and ethical classification | 1 | hybrid | +40 |
| persuasion-content-auditor | Audit any persuasive content against the 6 principles and produce a scored report with per-principle ratings and rewrite recommendations | 1 | full | +48 |
| reciprocity-strategy-designer | Design reciprocity-based persuasion strategies and detect when reciprocity is being used against you | 1 | hybrid | +50 |
| commitment-escalation-architect | Design commitment escalation sequences and detect consistency pressure — covering onboarding flows, foot-in-the-door campaigns, and commitment ladders | 1 | hybrid | +58 |
| social-proof-optimizer | Optimize social proof strategy using uncertainty and similarity conditions — covering testimonials, trust badges, and FOMO messaging | 1 | hybrid | +45 |
| liking-factor-engineer | Analyze and engineer liking to increase rapport and compliance in marketing, sales, and communication contexts | 1 | hybrid | +37 |
| authority-signal-designer | Design and audit authority signals in content, credentials, and landing pages — covering the three authority symbol types and the two-question defense framework | 1 | hybrid | +33 |
| scarcity-framing-strategist | Design and evaluate scarcity framing using psychological research on loss aversion and reactance | 1 | hybrid | +46 |
| influence-defense-analyzer | Detect and counter manipulation attempts using all 6 principles — classifying each tactic as ethical or exploitative with a principle-specific response strategy | 1 | hybrid | +40 |
| multi-principle-stacking-planner | Design a layered persuasion campaign by combining 2–4 principles in the right sequence — covering stacking patterns, interaction rules, and ethical thresholds | 1 | hybrid | +37 |

## Dependency Graph

```
Level 0 (independent):
  influence-principle-selector
  persuasion-content-auditor
  reciprocity-strategy-designer
  commitment-escalation-architect
  social-proof-optimizer
  liking-factor-engineer
  authority-signal-designer
  scarcity-framing-strategist

Level 1 (depends on Level 0):
  influence-defense-analyzer ──> influence-principle-selector
  multi-principle-stacking-planner ──> influence-principle-selector
                                   ──> reciprocity-strategy-designer
                                   ──> commitment-escalation-architect
                                   ──> social-proof-optimizer
                                   ──> liking-factor-engineer
                                   ──> authority-signal-designer
                                   ──> scarcity-framing-strategist
```

## Install Profiles

**Full** (all 10 skills) — Complete persuasion toolkit including defense analysis and multi-principle stacking.

**Core** (8 skills) — All 6 principle skills plus selector and auditor. Full coverage for designing and evaluating persuasion:
- `influence-principle-selector`
- `persuasion-content-auditor`
- `reciprocity-strategy-designer`
- `commitment-escalation-architect`
- `social-proof-optimizer`
- `liking-factor-engineer`
- `authority-signal-designer`
- `scarcity-framing-strategist`

**Minimal** (2 skills) — Entry point for quick persuasion analysis:
- `influence-principle-selector`
- `persuasion-content-auditor`

## Quality Metrics

| Skill | With Skill | Baseline | Delta |
|-------|----------:|--------:|------:|
| influence-principle-selector | 95% | 55% | +40 |
| persuasion-content-auditor | 98% | 50% | +48 |
| reciprocity-strategy-designer | 95% | 45% | +50 |
| commitment-escalation-architect | 98% | 40% | +58 |
| social-proof-optimizer | 95% | 50% | +45 |
| liking-factor-engineer | 92% | 55% | +37 |
| authority-signal-designer | 93% | 60% | +33 |
| scarcity-framing-strategist | 96% | 50% | +46 |
| influence-defense-analyzer | 95% | 55% | +40 |
| multi-principle-stacking-planner | 92% | 55% | +37 |
| **Average** | **95%** | **52%** | **+43** |

All 10 skills passed quality thresholds.

## Attribution

Skills extracted from **Influence: The Psychology of Persuasion** by Robert B. Cialdini (1984). The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, examples, and narrative.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
