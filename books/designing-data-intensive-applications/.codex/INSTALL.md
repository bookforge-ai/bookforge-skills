# Install designing-data-intensive-applications for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/designing-data-intensive-applications
mkdir -p ~/.agents/skills
ln -s ~/.codex/designing-data-intensive-applications/skills ~/.agents/skills/designing-data-intensive-applications
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\designing-data-intensive-applications" "%USERPROFILE%\.codex\designing-data-intensive-applications\skills"
```

## Update

```
cd ~/.codex/designing-data-intensive-applications && git pull
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
