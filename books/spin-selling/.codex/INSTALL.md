# Install spin-selling for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/spin-selling
mkdir -p ~/.agents/skills
ln -s ~/.codex/spin-selling/skills ~/.agents/skills/spin-selling
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\spin-selling" "%USERPROFILE%\.codex\spin-selling\skills"
```

## Update

```
cd ~/.codex/spin-selling && git pull
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
