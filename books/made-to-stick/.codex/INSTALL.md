# Install made-to-stick for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/made-to-stick
mkdir -p ~/.agents/skills
ln -s ~/.codex/made-to-stick/skills ~/.agents/skills/made-to-stick
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\made-to-stick" "%USERPROFILE%\.codex\made-to-stick\skills"
```

## Update

```
cd ~/.codex/made-to-stick && git pull
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
