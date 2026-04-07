# Install building-secure-and-reliable-systems for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/building-secure-and-reliable-systems
mkdir -p ~/.agents/skills
ln -s ~/.codex/building-secure-and-reliable-systems/skills ~/.agents/skills/building-secure-and-reliable-systems
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\building-secure-and-reliable-systems" "%USERPROFILE%\.codex\building-secure-and-reliable-systems\skills"
```

## Update

```
cd ~/.codex/building-secure-and-reliable-systems && git pull
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
