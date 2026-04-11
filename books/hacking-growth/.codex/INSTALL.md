# Install hacking-growth for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/hacking-growth
mkdir -p ~/.agents/skills
ln -s ~/.codex/hacking-growth/skills ~/.agents/skills/hacking-growth
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\hacking-growth" "%USERPROFILE%\.codex\hacking-growth\skills"
```

## Update

```
cd ~/.codex/hacking-growth && git pull
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
