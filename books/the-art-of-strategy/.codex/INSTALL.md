# Install the-art-of-strategy for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/the-art-of-strategy
mkdir -p ~/.agents/skills
ln -s ~/.codex/the-art-of-strategy/skills ~/.agents/skills/the-art-of-strategy
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\the-art-of-strategy" "%USERPROFILE%\.codex\the-art-of-strategy\skills"
```

## Update

```
cd ~/.codex/the-art-of-strategy && git pull
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
