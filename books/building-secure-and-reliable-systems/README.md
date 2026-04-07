# Building Secure and Reliable Systems — Agent Skills

14 agent skills extracted from *Building Secure and Reliable Systems* by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield using the [BookForge](https://bookforgeai.dev) pipeline.

## Install

**Claude Code:**
```bash
claude plugin add https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems
```

**Cursor:** Copy this directory to your Cursor plugins folder.

**Other platforms:** See `.codex/INSTALL.md`, `.aider/INSTALL.md`, or `GEMINI.md`.

## Skills (14)

### Level 0 — Foundation
| Skill | Mode | Tier |
|-------|------|:----:|
| adversary-profiling-and-threat-modeling | hybrid | 1 |
| security-reliability-design-review | full | 2 |
| least-privilege-access-design | full | 2 |
| resilience-and-blast-radius-design | full | 2 |
| disaster-risk-assessment | hybrid | 1 |
| secure-code-review | full | 2 |
| security-change-rollout-planning | hybrid | 1 |

### Level 1 — Core
| Skill | Mode | Tier | Depends On |
|-------|------|:----:|------------|
| recovery-mechanism-design | full | 2 | resilience-and-blast-radius-design |
| dos-defense-and-mitigation | full | 2 | resilience-and-blast-radius-design |
| security-testing-strategy | full | 3 | secure-code-review |
| secure-deployment-pipeline | full | 3 | secure-code-review |
| incident-response-team-setup | plan-only | 1 | disaster-risk-assessment |

### Level 2 — Capstone
| Skill | Mode | Tier | Depends On |
|-------|------|:----:|------------|
| security-incident-command | hybrid | 1 | incident-response-team-setup |
| security-incident-recovery | hybrid | 2 | security-incident-command |

## Quality

- 14/14 skills pass verification
- Average with-skill score: 95
- Average baseline score: 42
- Average delta: +49

## License

Skills: CC-BY-SA-4.0. See [LICENSE](LICENSE).
