# Designing Data-Intensive Applications — Agent Skills

14 agent skills extracted from *Designing Data-Intensive Applications* by Martin Kleppmann using the [BookForge](https://bookforgeai.dev) pipeline.

## Install

**Claude Code:**
```bash
claude plugin add https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications
```

**Cursor:** Copy this directory to your Cursor plugins folder.

**Other platforms:** See `.codex/INSTALL.md`, `.aider/INSTALL.md`, or `GEMINI.md`.

## Skills (14)

### Level 0 — Foundation
| Skill | Chapter | Mode |
|-------|:-------:|------|
| data-model-selector | 2 | hybrid |
| storage-engine-selector | 3 | hybrid |
| oltp-olap-workload-classifier | 3 | hybrid |
| encoding-format-advisor | 4 | hybrid |
| replication-strategy-selector | 5 | hybrid |
| transaction-isolation-selector | 7 | hybrid |
| distributed-failure-analyzer | 8 | hybrid |

### Level 1 — Core
| Skill | Chapter | Mode | Depends On |
|-------|:-------:|------|------------|
| replication-failure-analyzer | 5 | full | replication-strategy-selector |
| partitioning-strategy-advisor | 6 | hybrid | data-model-selector |
| concurrency-anomaly-detector | 7 | full | transaction-isolation-selector |
| consistency-model-selector | 9 | hybrid | replication-strategy + distributed-failure |
| batch-pipeline-designer | 10 | hybrid | oltp-olap-workload-classifier |
| stream-processing-designer | 11 | hybrid | encoding-format-advisor |

### Level 2 — Capstone
| Skill | Chapter | Mode | Depends On |
|-------|:-------:|------|------------|
| data-integration-architect | 12 | hybrid | batch + stream + consistency |

## License

Skills: CC-BY-SA-4.0. See [LICENSE](LICENSE).
