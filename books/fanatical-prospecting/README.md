# Fanatical Prospecting — Agent Skills

14 agent skills for outbound prospecting, pipeline filling, and sales conversation opening, extracted from **Fanatical Prospecting** by Jeb Blount.

These skills teach AI agents how to apply Blount's discipline-first prospecting system — converting revenue targets into daily activity numbers, allocating time with protected blocks, segmenting lists by tier, crafting channel-optimized messages, and opening conversations across phone, email, LinkedIn, text, and in-person. They also cover the hard parts: breaking through call reluctance, navigating gatekeepers, and handling the five most common prospecting objections.

**Average quality delta: +72.6 points** (94.9% with-skill vs 22.3% baseline).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/fanatical-prospecting
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| prospecting-objective-setter | Convert revenue targets into daily activity numbers — calls, emails, connections, and appointments — using pipeline math | 2 | hybrid | +73 |
| prospect-list-tiering | Score and segment a prospect list into A, B, and C tiers using fit criteria — budget, authority, need, and timeline | 2 | hybrid | +73 |
| prospecting-ratio-manager | Calculate and manage conversion ratios — dials to contacts, contacts to conversations, conversations to appointments | 2 | hybrid | +73 |
| prospecting-time-block-planner | Design a protected prospecting schedule that prevents interruptions and ensures daily minimums | 2 | hybrid | +73 |
| prospecting-message-crafter | Craft channel-optimized messages — cold call openers, email subject lines, LinkedIn requests, and texts — that open conversations without pitching | 2 | hybrid | +72 |
| call-reluctance-diagnostic | Diagnose the specific type of call reluctance — fear of rejection, perfectionism, role rejection, or social self-consciousness — and prescribe a behavioral intervention | 1 | plan-only | +73 |
| balanced-prospecting-cadence-designer | Design a multi-channel cadence that allocates daily activity across phone, email, social, text, and in-person to reduce channel dependency | 2 | hybrid | +73 |
| cold-call-opener-builder | Build a cold call opener that passes the first seven seconds using interruption pattern, relevance bridge, and disruptive question | 2 | hybrid | +72 |
| cold-email-writer | Write cold prospecting emails with subject line, opening hook, value bridge, and single call-to-action using the RBO framework | 2 | full | +73 |
| social-selling-touch-planner | Plan a LinkedIn touch sequence — profile view, content engagement, connection request, and message — that warms prospects before direct outreach | 2 | hybrid | +73 |
| in-person-prospecting-route-planner | Plan an in-person prospecting route by clustering visits by geography, tier, and call objective to maximize face-to-face touches per hour | 2 | hybrid | +73 |
| text-prospecting-sequence-builder | Build a compliant text prospecting sequence — initial message, follow-up, and opt-out handling — optimized for appointment setting | 2 | hybrid | +73 |
| gatekeeper-navigator | Navigate gatekeepers using respect-based rapport and legitimate business framing to reach decision makers without deception | 2 | hybrid | +73 |
| prospecting-objection-handler | Handle the five most common prospecting objections using the ledge-and-bridge technique to keep the conversation alive | 2 | hybrid | +73 |

## Dependency Graph

```
Level 0 (independent):
  prospecting-objective-setter
  prospect-list-tiering
  prospecting-ratio-manager
  prospecting-time-block-planner
  prospecting-message-crafter  [HUB — 6 dependents]
  call-reluctance-diagnostic

Level 1 (depends on Level 0):
  balanced-prospecting-cadence-designer ──> prospecting-objective-setter
                                        ──> prospect-list-tiering
                                        ──> prospecting-time-block-planner
  cold-call-opener-builder              ──> prospecting-objective-setter
                                        ──> prospecting-message-crafter
  cold-email-writer                     ──> prospecting-objective-setter
                                        ──> prospecting-message-crafter
  social-selling-touch-planner          ──> prospecting-message-crafter
                                        ──> prospect-list-tiering
  in-person-prospecting-route-planner   ──> prospect-list-tiering
                                        ──> prospecting-objective-setter
  text-prospecting-sequence-builder     ──> prospecting-message-crafter
  gatekeeper-navigator                  ──> prospecting-message-crafter

Level 2 (depends on Level 1):
  prospecting-objection-handler         ──> cold-call-opener-builder
                                        ──> prospecting-message-crafter
```

## Install Profiles

**Full** (all 14 skills) — Complete outbound prospecting system covering every channel and scenario.

**Core** (7 skills) — Highest-value skills covering objectives, list management, ratios, outreach, and objection handling:
- `prospecting-message-crafter`
- `prospecting-objective-setter`
- `prospect-list-tiering`
- `prospecting-ratio-manager`
- `cold-call-opener-builder`
- `cold-email-writer`
- `prospecting-objection-handler`

**Minimal** (3 skills) — Hub skill plus two essentials for immediate outreach:
- `prospecting-message-crafter`
- `prospecting-objective-setter`
- `cold-call-opener-builder`

## Quality Metrics

| Skill | With Skill | Baseline | Delta |
|-------|----------:|--------:|------:|
| prospecting-objective-setter | 95% | 22% | +73 |
| prospect-list-tiering | 94% | 21% | +73 |
| prospecting-ratio-manager | 95% | 22% | +73 |
| prospecting-time-block-planner | 95% | 22% | +73 |
| prospecting-message-crafter | 95% | 23% | +72 |
| call-reluctance-diagnostic | 95% | 22% | +73 |
| balanced-prospecting-cadence-designer | 95% | 22% | +73 |
| cold-call-opener-builder | 95% | 23% | +72 |
| cold-email-writer | 95% | 22% | +73 |
| social-selling-touch-planner | 95% | 22% | +73 |
| in-person-prospecting-route-planner | 95% | 22% | +73 |
| text-prospecting-sequence-builder | 95% | 22% | +73 |
| gatekeeper-navigator | 95% | 22% | +73 |
| prospecting-objection-handler | 95% | 22% | +73 |
| **Average** | **94.9%** | **22.3%** | **+72.6** |

All 14 skills passed quality thresholds.

## Usage

Ask your AI agent anything about outbound prospecting:
- "Help me set daily prospecting targets to hit my quota"
- "Score my prospect list and prioritize the top tier"
- "Write a cold email for a VP of Sales at a mid-market SaaS company"
- "Build a cold call opener for my service"
- "How do I get past the gatekeeper at this account?"
- "Help me handle 'just send me some information'"

## Attribution

Skills extracted from **Fanatical Prospecting** by Jeb Blount (2015, ISBN 978-1-119-14475-2). The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, examples, and narrative.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
