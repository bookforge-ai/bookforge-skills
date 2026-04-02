# Install influence-psychology-of-persuasion for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/influence-psychology-of-persuasion
mkdir -p ~/.agents/skills
ln -s ~/.codex/influence-psychology-of-persuasion/skills ~/.agents/skills/influence-psychology-of-persuasion
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\influence-psychology-of-persuasion" "%USERPROFILE%\.codex\influence-psychology-of-persuasion\skills"
```

## Update

```
cd ~/.codex/influence-psychology-of-persuasion && git pull
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
