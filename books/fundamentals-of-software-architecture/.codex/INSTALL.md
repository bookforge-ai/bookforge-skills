# Install fundamentals-of-software-architecture for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/fundamentals-of-software-architecture
mkdir -p ~/.agents/skills
ln -s ~/.codex/fundamentals-of-software-architecture/skills ~/.agents/skills/fundamentals-of-software-architecture
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\fundamentals-of-software-architecture" "%USERPROFILE%\.codex\fundamentals-of-software-architecture\skills"
```

## Update

```
cd ~/.codex/fundamentals-of-software-architecture && git pull
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
