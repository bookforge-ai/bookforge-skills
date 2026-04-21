# Install patterns-of-enterprise-application-architecture for Aider

## Using aider-skills package

```
pip install aider-skills
aider --read $(aider-skills tmpfile ./skills)
```

## Manual configuration

Add to your `.aider.conf.yml`:

```yaml
read: [skills/enterprise-architecture-pattern-stack-selector/SKILL.md]
```

## More information

See https://aider.chat/docs/usage/conventions.html for details on Aider conventions.
