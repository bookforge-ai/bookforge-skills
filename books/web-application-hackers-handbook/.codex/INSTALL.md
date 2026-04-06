# Install web-application-hackers-handbook for Codex

## Setup

```
git clone https://github.com/bookforge-ai/bookforge-skills.git ~/.codex/web-application-hackers-handbook
mkdir -p ~/.agents/skills
ln -s ~/.codex/web-application-hackers-handbook/skills ~/.agents/skills/web-application-hackers-handbook
```

## Windows

```
cmd /c mklink /J "%USERPROFILE%\.agents\skills\web-application-hackers-handbook" "%USERPROFILE%\.codex\web-application-hackers-handbook\skills"
```

## Update

```
cd ~/.codex/web-application-hackers-handbook && git pull
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
