# The Challenger Sale Skills

10 agent skills for B2B sales execution, extracted from **The Challenger Sale** by Matthew Dixon and Brent Adamson.

These skills encode the Challenger methodology — derived from CEB's empirical study of 6,000+ sales reps across 44 behavioral attributes. They teach AI agents how to classify rep profiles, build and author Commercial Teaching pitches, tailor by stakeholder, diagnose taking-control gaps, plan negotiations with constructive tension, and coach reps for behavior change. The agent handles preparation, classification, diagnosis, and planning while the human conducts the actual sales activities.

**Average quality delta: +65.4 points** (99.3% with-skill vs 33.9% baseline).

## Install

### Claude Code (recommended)

```bash
# Add to your Claude Code project
claude mcp add bookforge-skills https://github.com/bookforge-ai/bookforge-skills
```

Or install from the [BookForge marketplace](https://github.com/bookforge-ai/bookforge-skills):

```bash
# Clone and link
git clone https://github.com/bookforge-ai/bookforge-skills.git
# Then reference skills/the-challenger-sale/ in your Claude Code settings
```

### Other platforms

- **Cursor:** See `.cursor-plugin/plugin.json`
- **Codex:** See `.codex/INSTALL.md`
- **Gemini CLI:** See `gemini-extension.json` and `GEMINI.md`
- **Aider:** See `.aider/INSTALL.md`
- **OpenCode:** See `.opencode/plugins/the-challenger-sale.js`

## Skills

### Level 0 — Foundation Skills (independent)

| Skill | Description | Mode |
|-------|-------------|------|
| classify-rep-profile | Classify a sales rep against the five CEB selling profiles and score Teach/Tailor/Take-Control subscales using the Appendix B self-diagnostic | hybrid |
| build-commercial-insight | Reverse-engineer a Commercial Insight from seller strengths and validate it against the four-criteria test | hybrid |
| diagnose-pitch-for-commercial-teaching-fit | Audit an existing sales pitch, deck, or call transcript against the Commercial Teaching rubric — detects lead-with vs lead-to errors, missing Reframes, and sequence violations | full |
| diagnose-taking-control-gaps | Diagnose a deal's taking-control posture: foil-RFP detection, passive/assertive/aggressive positioning, and misconception analysis | hybrid |
| diagnose-manager-effectiveness | Diagnose a frontline sales manager's effectiveness against the CEB four-driver model, with weighted driver scores and a time-reallocation plan | hybrid |

### Level 1 — Core Challenger Skills (depend on Level 0)

| Skill | Description | Mode |
|-------|-------------|------|
| author-commercial-teaching-pitch | Author a Commercial Teaching pitch using the six-step choreography and polish it with SAFE-BOLD | hybrid |
| plan-negotiation-with-constructive-tension | Build a pre-call negotiation plan using DuPont's four-step framework and sequence concessions to avoid the proactive-discount and ultimatum traps | hybrid |
| coach-rep-with-pause-framework | Plan a structured coaching session for a sales rep using the PAUSE framework, routing to PAUSE coaching or sales innovation mode based on issue type | hybrid |

### Level 2 — Advanced Skills (depend on Level 1)

| Skill | Description | Mode |
|-------|-------------|------|
| tailor-pitch-by-stakeholder | Tailor a Commercial Teaching pitch to each stakeholder role using Functional Bias Cards and route the pitch to avoid the C-suite elevation trap | hybrid |
| plan-challenger-model-rollout | Plan a full Challenger model rollout using Grainger's four-question pilot framework, star/core/laggard adoption sequencing, and a four-track parallel workstream design | plan-only |

## Dependency Graph

```
Level 0 (independent):
  classify-rep-profile               [HUB — 2 dependents]
  build-commercial-insight
  diagnose-pitch-for-commercial-teaching-fit
  diagnose-taking-control-gaps
  diagnose-manager-effectiveness

Level 1 (depends on Level 0):
  author-commercial-teaching-pitch ──> build-commercial-insight
  plan-negotiation-with-constructive-tension ──> diagnose-taking-control-gaps
  coach-rep-with-pause-framework ──> classify-rep-profile

Level 2 (depends on Level 1):
  tailor-pitch-by-stakeholder ──> author-commercial-teaching-pitch
  plan-challenger-model-rollout ──> classify-rep-profile
                                ──> diagnose-manager-effectiveness
```

Hub skill: `classify-rep-profile` (depended on by `coach-rep-with-pause-framework` and `plan-challenger-model-rollout`)

## Install Profiles

**Full** (all 10 skills) — Complete Challenger Sale methodology toolkit, including rep profiling, commercial insight construction, pitch authoring, stakeholder tailoring, negotiation planning, rep coaching, and rollout planning.

## Quality Summary

| Metric | Score |
|--------|------:|
| Avg with-skill score | 99.3 / 100 |
| Avg baseline score | 33.9 / 100 |
| Avg delta | +65.4 |
| Skills passing | 10 / 10 |

## Attribution

Skills extracted from **The Challenger Sale: Taking Control of the Customer Conversation** by Matthew Dixon and Brent Adamson (2011, Portfolio / Penguin). The skills encode the book's empirically-validated methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full research, case studies, and examples.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
