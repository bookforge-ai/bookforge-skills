# Contributing to BookForge Skills

Thank you for your interest in contributing agent skills to BookForge.

## What This Project Is

BookForge Skills is a library of agent skills distilled from non-fiction books. Each skill is a `SKILL.md` file that gives AI coding agents expert-level knowledge for specific tasks — architecture decisions, design patterns, debugging workflows, and more.

Skills follow the open [Agent Skills specification](https://agentskills.io/specification) and work with Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, and 20+ agent platforms.

## How to Contribute a New Skill

### Option A: Use the BookForge Pipeline (recommended)

1. Pick a non-fiction book with high "skill density" (actionable frameworks, decision trees, checklists)
2. Run the [BookForge pipeline](https://github.com/bookforge-ai/bookforge) to extract and generate skills
3. Submit a PR with the generated skills

### Option B: Write a Skill Manually

1. Create a directory: `<domain>/<skill-name>/SKILL.md`
2. Follow the structure requirements below
3. Submit a PR

## Skill Structure

Every skill must have a `SKILL.md` file with this structure:

```yaml
---
name: skill-name-in-kebab-case
description: >
  One paragraph that describes WHEN to trigger this skill.
  Include specific phrases, symptoms, and situations that should activate it.
  This is the most important field — it determines whether agents find your skill.
---
```

The body contains the instructions the agent follows when the skill is activated.

### Quality Standards

- **Triggering accuracy**: The `description` field must list concrete trigger phrases and situations, not vague summaries
- **WHY reasoning**: Every step includes WHY it matters — this enables agents to handle edge cases
- **Progressive disclosure**: Body under 500 lines. Deep details go in `references/`, scripts in `scripts/`
- **Generalized terminology**: Use domain-standard terms, not author-specific jargon
- **Examples**: Include 2-3 examples with Scenario / Trigger / Process / Output format

### Directory Layout

```
skills/
  <domain>/
    <skill-name>/
      SKILL.md          # Required: the skill itself
      references/       # Optional: deep-dive docs, tables, extended examples
      scripts/          # Optional: reusable shell/Python scripts
    assets/           # Optional: templates, config files
```

## Pull Request Process

1. **One domain per PR** — keep reviews focused
2. **Include test results** if available (with-skill vs without-skill comparison)
3. **Do not include `.meta/` directories** — these are internal pipeline artifacts
4. **Do not include copyrighted book content** — skills must be original, generalized knowledge

## License

All contributions must be licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). By submitting a PR, you agree that your contribution is licensed under this license.

## Questions?

Open an issue in this repo or in the [BookForge pipeline repo](https://github.com/bookforge-ai/bookforge).
