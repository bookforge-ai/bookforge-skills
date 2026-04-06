# Tool Mapping: Claude Code → Codex

Skills use Claude Code tool names. When you encounter these in a skill, use your platform equivalent:

| Skill references | Codex equivalent |
|-----------------|------------------|
| `Read` (file reading) | Native file reading |
| `Write` (file creation) | Native file writing |
| `Edit` (file editing) | Native file editing |
| `Bash` (run commands) | Native shell execution |
| `Grep` (search content) | Native code search |
| `Glob` (search files) | Native file search |
| `WebSearch` | Not available (network restricted in Codex App sandbox) |
| `WebFetch` | Not available (network restricted in Codex App sandbox) |
| `TodoWrite` (task tracking) | `update_plan` |
| `Task` tool (dispatch subagent) | `spawn_agent` (see below) |
| `Skill` tool (invoke a skill) | Skills load natively — just follow the instructions |
| `Agent` (spawn subagent) | `spawn_agent` with worker role |
| `AskUserQuestion` | Direct message to user |

## Subagent dispatch requires multi-agent support

Add to your Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

## Named agent dispatch

BookForge skills may reference named agent types. Codex does not have a named agent registry — `spawn_agent` creates generic agents from built-in roles.

When a skill says to dispatch a named agent type:

1. Find the agent's prompt file or inline prompt in the skill
2. Read the prompt content
3. Fill any template placeholders
4. `spawn_agent(agent_type="worker", message=...)` with the filled content

## Network restrictions

Codex App sandbox blocks internet access. Skills requiring `web_access` capability will degrade — the agent falls back to general knowledge.

## BookForge pipeline notes

- These are document-based product management skills. No subagent dispatch required for individual skills.
- All skills work from user-provided product context, team descriptions, and stakeholder information.
