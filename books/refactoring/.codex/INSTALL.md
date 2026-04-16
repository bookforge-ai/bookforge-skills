# Install refactoring for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/refactoring
mkdir -p ~/.agents/skills
ln -s ~/.codex/refactoring/skills ~/.agents/skills/refactoring
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\refactoring" "%USERPROFILE%\.codex\refactoring\skills"
```

## Update

```
cd ~/.codex/refactoring && git pull
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
