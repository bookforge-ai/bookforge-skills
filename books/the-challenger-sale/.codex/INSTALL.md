# Install the-challenger-sale for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/the-challenger-sale
mkdir -p ~/.agents/skills
ln -s ~/.codex/the-challenger-sale/skills ~/.agents/skills/the-challenger-sale
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\the-challenger-sale" "%USERPROFILE%\.codex\the-challenger-sale\skills"
```

## Update

```
cd ~/.codex/the-challenger-sale && git pull
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
