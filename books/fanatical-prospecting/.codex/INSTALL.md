# Install fanatical-prospecting for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/fanatical-prospecting
mkdir -p ~/.agents/skills
ln -s ~/.codex/fanatical-prospecting/skills ~/.agents/skills/fanatical-prospecting
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\fanatical-prospecting" "%USERPROFILE%\.codex\fanatical-prospecting\skills"
```

## Update

```
cd ~/.codex/fanatical-prospecting && git pull
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
