# Install never-split-the-difference for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/never-split-the-difference
mkdir -p ~/.agents/skills
ln -s ~/.codex/never-split-the-difference/skills ~/.agents/skills/never-split-the-difference
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\never-split-the-difference" "%USERPROFILE%\.codex\never-split-the-difference\skills"
```

## Update

```
cd ~/.codex/never-split-the-difference && git pull
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
