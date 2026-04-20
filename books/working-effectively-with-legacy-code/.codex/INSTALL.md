# Install working-effectively-with-legacy-code for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/working-effectively-with-legacy-code
mkdir -p ~/.agents/skills
ln -s ~/.codex/working-effectively-with-legacy-code/books/working-effectively-with-legacy-code/skills ~/.agents/skills/working-effectively-with-legacy-code
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\working-effectively-with-legacy-code" "%USERPROFILE%\.codex\working-effectively-with-legacy-code\books\working-effectively-with-legacy-code\skills"
```

## Update

```
cd ~/.codex/working-effectively-with-legacy-code && git pull
```

## Configuration

Enable multi-agent support for skills that dispatch subagents:

```toml
# ~/.codex/config.toml
[features]
multi_agent = true
```

## Tool Mapping

See references/codex-tools.md for how Claude Code tool names map to Codex equivalents.
