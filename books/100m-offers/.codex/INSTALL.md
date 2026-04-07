# Install 100m-offers for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/100m-offers
mkdir -p ~/.agents/skills
ln -s ~/.codex/100m-offers/skills ~/.agents/skills/100m-offers
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\100m-offers" "%USERPROFILE%\.codex\100m-offers\skills"
```

## Update

```
cd ~/.codex/100m-offers && git pull
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
