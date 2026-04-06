# Web Application Hacker's Handbook Skills

13 agent skills distilled from **The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws** by Dafydd Stuttard and Marcus Pinto.

These skills teach AI coding agents how to conduct structured web application penetration tests — from attack surface mapping and reconnaissance through injection testing, authentication assessment, session management analysis, access control verification, and client-side attack detection. The agent follows the book's complete testing methodology, sequences testing phases, and produces actionable security findings.

## Skills

### Hub — Methodology Orchestrator (1 skill)

| Skill | Description |
|-------|-------------|
| web-application-penetration-testing-methodology | Orchestrate a complete web application penetration test through 13 testing areas, sequencing and delegating all phases from reconnaissance through exploitation |

### Reconnaissance & Mapping (1 skill)

| Skill | Description |
|-------|-------------|
| web-application-attack-surface-mapping | Systematically map application content, entry points, technologies, and attack surface during authorized security testing |

### Authentication & Session Management (2 skills)

| Skill | Description |
|-------|-------------|
| authentication-security-assessment | Assess authentication mechanisms for design and implementation flaws including credential handling, login logic, and multi-factor bypass |
| session-management-security-assessment | Test session management for token predictability, insecure transmission, fixation, and lifecycle weaknesses |

### Access Control (1 skill)

| Skill | Description |
|-------|-------------|
| access-control-vulnerability-testing | Test vertical, horizontal, and context-dependent access controls for privilege escalation and unauthorized resource access |

### Injection Testing (3 skills)

| Skill | Description |
|-------|-------------|
| sql-injection-detection-and-exploitation | Perform complete SQL injection assessment from detection through data extraction, covering UNION-based, blind, and second-order techniques |
| xss-detection-and-exploitation | Detect and exploit reflected, stored, and DOM-based cross-site scripting with filter bypass and context-aware payload construction |
| server-side-injection-testing | Test for OS command injection, path traversal, file inclusion, SMTP/LDAP/XPath/XXE injection, and SSRF |

### Application Logic & Client-Side (2 skills)

| Skill | Description |
|-------|-------------|
| application-logic-flaw-testing | Identify logic flaws that bypass business rules — race conditions, multi-step process manipulation, and trust boundary violations |
| client-side-attack-testing | Test client-side controls including hidden fields, browser extensions, JavaScript validation, and same-origin policy enforcement |

### Automation & Hardening (2 skills)

| Skill | Description |
|-------|-------------|
| web-application-fuzzing-automation | Automate vulnerability discovery through parameter fuzzing, content enumeration, and response analysis |
| web-application-hardening-assessment | Assess server configuration, deployment hardening, error handling, and information disclosure |

### Source Code Review (1 skill)

| Skill | Description |
|-------|-------------|
| source-code-security-review | Perform white-box security review of application source code for unsafe patterns, vulnerable APIs, and injection sinks |

## Dependency Graph

```
Level 0 (hub):
  web-application-penetration-testing-methodology (orchestrates all 12 domain skills)

Level 1 (domain skills, independently usable):
  web-application-attack-surface-mapping
  authentication-security-assessment
  session-management-security-assessment
  access-control-vulnerability-testing
  sql-injection-detection-and-exploitation
  xss-detection-and-exploitation
  server-side-injection-testing
  application-logic-flaw-testing
  client-side-attack-testing
  web-application-fuzzing-automation
  web-application-hardening-assessment
  source-code-security-review
```

## Install Profiles

**Full** (all 13 skills) — Complete web application penetration testing toolkit. Hub methodology plus all 12 domain-specific testing skills.

**Essentials** (7 skills) — Core testing methodology with the highest-impact vulnerability classes:
- `web-application-penetration-testing-methodology`
- `web-application-attack-surface-mapping`
- `authentication-security-assessment`
- `sql-injection-detection-and-exploitation`
- `xss-detection-and-exploitation`
- `server-side-injection-testing`
- `access-control-vulnerability-testing`

**Injection-only** (3 skills) — Focused injection testing:
- `sql-injection-detection-and-exploitation`
- `xss-detection-and-exploitation`
- `server-side-injection-testing`

## Attribution

Skills distilled from **The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws** by Dafydd Stuttard and Marcus Pinto (Wiley, 2nd edition). The skills encode the book's penetration testing methodology and vulnerability assessment techniques in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, diagrams, and discussion.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
