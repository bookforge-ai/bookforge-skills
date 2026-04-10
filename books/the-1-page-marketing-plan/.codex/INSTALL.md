# Install the-1-page-marketing-plan for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/the-1-page-marketing-plan
mkdir -p ~/.agents/skills
ln -s ~/.codex/the-1-page-marketing-plan/skills ~/.agents/skills/the-1-page-marketing-plan
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\the-1-page-marketing-plan" "%USERPROFILE%\.codex\the-1-page-marketing-plan\skills"
```

## Update

```
cd ~/.codex/the-1-page-marketing-plan && git pull
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
