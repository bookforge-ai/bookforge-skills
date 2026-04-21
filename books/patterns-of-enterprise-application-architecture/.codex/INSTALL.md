# Install patterns-of-enterprise-application-architecture for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/patterns-of-enterprise-application-architecture
mkdir -p ~/.agents/skills
ln -s ~/.codex/patterns-of-enterprise-application-architecture/skills ~/.agents/skills/patterns-of-enterprise-application-architecture
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\patterns-of-enterprise-application-architecture" "%USERPROFILE%\.codex\patterns-of-enterprise-application-architecture\skills"
```

## Update

```
cd ~/.codex/patterns-of-enterprise-application-architecture && git pull
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
