# Install the-craft-of-research for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/the-craft-of-research
mkdir -p ~/.agents/skills
ln -s ~/.codex/the-craft-of-research/skills ~/.agents/skills/the-craft-of-research
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\the-craft-of-research" "%USERPROFILE%\.codex\the-craft-of-research\skills"
```

## Update

```
cd ~/.codex/the-craft-of-research && git pull
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
