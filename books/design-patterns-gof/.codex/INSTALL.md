# Install design-patterns-gof for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/design-patterns-gof
mkdir -p ~/.agents/skills
ln -s ~/.codex/design-patterns-gof/skills ~/.agents/skills/design-patterns-gof
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\design-patterns-gof" "%USERPROFILE%\.codex\design-patterns-gof\skills"
```

## Update

```
cd ~/.codex/design-patterns-gof && git pull
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
