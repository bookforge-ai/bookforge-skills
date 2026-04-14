# Made to Stick Skills

10 agent skills for sticky messaging, extracted from **Made to Stick: Why Some Ideas Survive and Others Die** by Chip Heath and Dan Heath.

These skills encode the SUCCESs framework (Simple, Unexpected, Concrete, Credible, Emotional, Stories) plus the Curse-of-Knowledge diagnostic into agent-executable format. They audit drafts, extract Commander's Intent core messages, build curiosity-gap hooks, rewrite abstract prose into sensory language, pick Sinatra-test credibility evidence, choose identity-based emotional appeals, structure Challenge/Connection/Creativity story plots, and orchestrate end-to-end message clinics that preserve the user's voice and brand constraints.

**Average quality delta: +79 points** (92% with-skill vs 13% baseline across 10 skills).

## Install

### Claude Code (recommended)

```bash
# Add to your Claude Code project
claude mcp add bookforge-skills https://github.com/bookforge-ai/bookforge-skills
```

Or install from the [BookForge marketplace](https://github.com/bookforge-ai/bookforge-skills):

```bash
git clone https://github.com/bookforge-ai/bookforge-skills.git
# Then reference books/made-to-stick/ in your Claude Code settings
```

### Other platforms

- **Cursor:** See `.cursor-plugin/plugin.json`
- **Codex:** See `.codex/INSTALL.md`
- **Gemini CLI:** See `gemini-extension.json` and `GEMINI.md`
- **Aider:** See `.aider/INSTALL.md`
- **OpenCode:** See `.opencode/plugins/made-to-stick.js`

## Skills

### Level 0 — Foundation Diagnostics and Rewriters (independent)

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| curse-of-knowledge-detector | Diagnose expert blind spots — unexplained jargon, buried assumptions, abstract strategy talk — in any draft | hybrid | +90 |
| core-message-extractor | Extract the Commander's Intent — the single sentence that must survive if everything else is lost | hybrid | +62 |
| curiosity-gap-architect | Build Unexpected hooks using schema-break surprise and Gap Theory curiosity, scored against the post-dictable test | hybrid | +89 |
| concrete-language-rewriter | Rewrite abstract/jargon-heavy passages into sensory, schema-based language using three named techniques | hybrid | +50 |
| credibility-evidence-selector | Pick the strongest proof for a claim and kill weak evidence chains via the Sinatra Test | plan-only | +95 |
| emotional-appeal-selector | Choose the right emotional lever (Association, Self-Interest, Identity) and strip out analytical priming | plan-only | +90 |
| story-plot-selector | Pick the right story plot (Challenge, Connection, Creativity) and structure it as springboard or direct | hybrid | +62 |
| sticky-message-antipattern-detector | Scan a draft for named failure modes — buried leads, decision paralysis, stats-without-story, semantic stretch | hybrid | +90 |

### Level 1 — Capstone Diagnostic (depends on all 8 foundations)

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| stickiness-audit | Score a draft across all six SUCCESs principles plus the Curse of Knowledge axis with evidence quotes and a top-3 fix list | hybrid | +90 |

### Level 2 — End-to-End Orchestrator (depends on Level 1 + foundations)

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| message-clinic-runner | Run the full Idea Clinic: audit, delegate fixes to foundation skills, and ship a before/after rewrite with punch line | full | +90 |

## Dependency Graph

```
Level 0 (independent):
  curse-of-knowledge-detector
  core-message-extractor
  curiosity-gap-architect
  concrete-language-rewriter
  credibility-evidence-selector
  emotional-appeal-selector
  story-plot-selector
  sticky-message-antipattern-detector

Level 1 (depends on all 8 foundations):
  stickiness-audit

Level 2 (depends on stickiness-audit + 7 foundations):
  message-clinic-runner
```

Hub skill: `stickiness-audit` (the capstone diagnostic every other level-2 call routes through)

## Install Profiles

**Minimal** (4 skills) — Foundation diagnostics you can use on any draft today:
- `curse-of-knowledge-detector`
- `core-message-extractor`
- `sticky-message-antipattern-detector`
- `concrete-language-rewriter`

**Core** (9 skills) — All 8 foundation skills plus the full SUCCESs stickiness-audit scorecard:
- All minimal skills
- `curiosity-gap-architect`
- `credibility-evidence-selector`
- `emotional-appeal-selector`
- `story-plot-selector`
- `stickiness-audit`

**Full** (all 10 skills) — Complete Made to Stick toolkit including the end-to-end `message-clinic-runner` rewrite orchestrator.

## Quality Summary

| Metric | Score |
|--------|------:|
| Avg with-skill score | 92 / 100 |
| Avg baseline score | 13 / 100 |
| Avg delta | +79 |
| Skills passing | 10 / 10 |

## Attribution

Skills extracted from **Made to Stick: Why Some Ideas Survive and Others Die** by Chip Heath and Dan Heath (2007, ISBN 978-1400064281). The skills encode the book's SUCCESs framework in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full research, case studies, and examples (Commander's Intent, Sinatra Test, the kidney heist, Mother Teresa, Subway's Jared, Saddleback Sam, Boeing 727, Nora Ephron, Loewenstein's gap theory).

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
