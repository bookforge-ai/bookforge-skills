# Security Policy

BookForge Skills is a library of agent skills distilled from non-fiction books. Skills are static Markdown files that instruct AI agents — they do not execute code in the skill library itself, and the library has no runtime components.

## Reporting a concern

If you discover a concern related to the content of a skill — for example, a skill that instructs an agent to produce harmful output, leak sensitive information, or violate common safety norms — please report it by opening a [GitHub issue](https://github.com/bookforge-ai/bookforge-skills/issues) or emailing the address in [TAKEDOWN.md](TAKEDOWN.md).

For concerns about the BookForge pipeline itself (the code that generates skills), please report them to the [bookforge repository](https://github.com/bookforge-ai/bookforge) instead.

## What to include in a report

- A link to the specific skill file or directory
- A clear description of the concern
- An example of the problematic output, if applicable
- Any suggested remediation

## Response commitment

- We acknowledge reports within 48 hours of receipt.
- We investigate and respond with an action plan within 7 days.
- Critical concerns are addressed as quickly as possible, often within 48 hours of verification.
- We maintain a private compliance log of every report and its resolution.

## Scope

This policy applies to the content and structure of skills in this repository. It does not apply to:

- The underlying AI model you use with the skill (report those to the model provider)
- The agent platform you install the skill into (report those to the platform)
- Third-party tools that BookForge skills reference

## Related documents

- [TAKEDOWN.md](TAKEDOWN.md) — DMCA and rights-holder takedown procedure
- [COPYRIGHT.md](COPYRIGHT.md) — legal framework and attribution practice
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — contributor conduct expectations
