# Install traction for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/traction
mkdir -p ~/.agents/skills
ln -s ~/.codex/traction/skills ~/.agents/skills/traction
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\traction" "%USERPROFILE%\.codex\traction\skills"
```

## Update

```
cd ~/.codex/traction && git pull
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
