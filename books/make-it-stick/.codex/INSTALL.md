# Install make-it-stick for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/make-it-stick
mkdir -p ~/.agents/skills
ln -s ~/.codex/make-it-stick/skills ~/.agents/skills/make-it-stick
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\make-it-stick" "%USERPROFILE%\.codex\make-it-stick\skills"
```

## Update

```
cd ~/.codex/make-it-stick && git pull
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
