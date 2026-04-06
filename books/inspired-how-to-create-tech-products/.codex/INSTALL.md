# Install inspired-how-to-create-tech-products for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/inspired-how-to-create-tech-products
mkdir -p ~/.agents/skills
ln -s ~/.codex/inspired-how-to-create-tech-products/skills ~/.agents/skills/inspired-how-to-create-tech-products
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\inspired-how-to-create-tech-products" "%USERPROFILE%\.codex\inspired-how-to-create-tech-products\skills"
```

## Update

```
cd ~/.codex/inspired-how-to-create-tech-products && git pull
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
