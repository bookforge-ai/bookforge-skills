# Tool Mapping: Claude Code → Gemini CLI

Skills use Claude Code tool names. When you encounter these in a skill, use your platform equivalent:

| Skill references | Gemini CLI equivalent |
|-----------------|----------------------|
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search content) | `grep_search` |
| `Glob` (search files) | `glob` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `TodoWrite` (task tracking) | `write_todos` |
| `Skill` tool (invoke a skill) | `activate_skill` |
| `Task` tool (dispatch subagent) | **No equivalent** — see below |
| `Agent` (spawn subagent) | **No equivalent** |
| `AskUserQuestion` | `ask_user` |

## No subagent support

Gemini CLI has no equivalent to Claude Code's `Task` tool. These skills do not require subagent dispatch — they are document-based product management skills that run in a single session.

## Additional Gemini CLI tools

These tools are available in Gemini CLI but have no Claude Code equivalent:

| Tool | Purpose |
|------|---------|
| `list_directory` | List files and subdirectories |
| `save_memory` | Persist facts to GEMINI.md across sessions |
| `ask_user` | Request structured input from the user |
| `tracker_create_task` | Rich task management (create, update, list, visualize) |
| `enter_plan_mode` / `exit_plan_mode` | Switch to read-only research mode before making changes |

## BookForge notes

These product management skills work from product context the user provides. No book files or external resources are required.
