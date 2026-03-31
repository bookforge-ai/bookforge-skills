# Install the-mom-test for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/the-mom-test
mkdir -p ~/.agents/skills
ln -s ~/.codex/the-mom-test/skills ~/.agents/skills/the-mom-test
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\the-mom-test" "%USERPROFILE%\.codex\the-mom-test\skills"
```

## Update

```
cd ~/.codex/the-mom-test && git pull
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
