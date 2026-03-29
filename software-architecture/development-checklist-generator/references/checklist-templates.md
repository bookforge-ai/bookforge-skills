# Checklist Templates Reference

Ready-to-use templates for each checklist type, with customization instructions.

## Template 1: Developer Code Completion Checklist

Use this checklist when a developer declares code is "done." It defines the definition of done for code completion.

### Base Template

```markdown
# Code Completion Checklist

> Complete this checklist before marking your PR/MR as ready for review.
> Every unchecked item needs a comment explaining why it doesn't apply.

- [ ] **No hardcoded configuration values** — All environment-specific values (URLs, ports, keys, connection strings) are externalized to config files or environment variables. WHY: Hardcoded values cause deployment failures when promoting to staging/production.

- [ ] **Input validation on external boundaries** — All inputs from users, APIs, queues, and file uploads are validated. Null checks, type checks, and range checks are present. WHY: Most security vulnerabilities and runtime crashes originate from unvalidated external input.

- [ ] **Error handling produces actionable information** — Catch blocks log the context needed to diagnose the issue (what was attempted, what input caused the failure, what the system state was). WHY: "NullPointerException at line 42" wastes hours of debugging time. "Failed to process order #12345 for customer ABC because payment service returned null" saves hours.

- [ ] **No absorbed exceptions** — No empty catch blocks. No catch-and-ignore patterns. Every exception is either handled, logged, or re-thrown. WHY: Absorbed exceptions create silent failures that are nearly impossible to diagnose. The system appears to work but data is inconsistent or incomplete.

- [ ] **Sensitive data excluded from logs** — Passwords, tokens, API keys, PII, and credit card numbers are NOT written to log files. WHY: Log files are often less protected than databases. Logging sensitive data creates an unmonitored data leak.

- [ ] **New configuration keys present in all environment configs** — If you added a new config key, it exists in dev, staging, and production config files (even if the value differs). WHY: Missing config keys cause startup failures in environments that weren't tested.

- [ ] **Code changes are covered by tests** — New logic has unit tests. Changed logic has updated tests. Edge cases identified during development are tested. WHY: Untested code changes are the primary source of regression bugs.
```

### Customization Instructions

1. **Remove items your tooling handles** — If your linter catches formatting issues, don't add a formatting item. If your CI pipeline validates configuration, remove the config item.
2. **Add team-specific items** — What recurring bugs does YOUR team ship? Add items that target those specific patterns.
3. **Add project-specific items** — Does your project have unique requirements (HIPAA compliance, PCI, accessibility)? Add verification items for those.
4. **Keep it under 10 items** — If you exceed 10, split into "Code Quality" and "Security" checklists used at different stages.

## Template 2: Unit and Functional Testing Checklist

Use this checklist when reviewing test coverage for a feature or component.

### Base Template

```markdown
# Testing Checklist

> Complete this checklist before marking tests as complete.
> Focus on scenarios that are commonly missed, not scenarios your test framework handles automatically.

- [ ] **Happy path tested** — The primary use case works as expected with valid inputs. WHY: Baseline verification that the feature does what it's supposed to do.

- [ ] **Empty/null inputs handled** — Tests cover: null values, empty strings, empty collections, zero values, and missing optional parameters. WHY: Boundary conditions are the most common source of production bugs because developers test with realistic data, not edge cases.

- [ ] **Error paths tested** — Tests verify behavior when dependencies fail: database timeouts, external API errors, network failures, invalid responses. WHY: Error handling code is the least-tested and most-executed code in production. Systems spend more time handling errors than processing happy paths.

- [ ] **Concurrent access scenarios considered** — If the code modifies shared state, tests cover concurrent writes, race conditions, and transaction isolation. WHY: Concurrency bugs are the hardest to reproduce and the most damaging in production.

- [ ] **Boundary values tested** — Tests cover: maximum allowed values, minimum allowed values, values just above/below limits, and values at pagination boundaries. WHY: Boundary errors (off-by-one, overflow, truncation) are systematic — they affect every record at the boundary, not just occasional ones.

- [ ] **Integration points tested with failure simulation** — External service calls are tested with: slow responses, error responses, malformed responses, and complete unavailability. WHY: External services WILL fail. The question is whether your system degrades gracefully or crashes.

- [ ] **Test data is realistic** — Tests use data that resembles production: international characters, long strings, special characters in names, realistic date ranges. WHY: Tests with "test123" and "John Doe" pass but fail in production with "O'Brien" or "Muller" or "Yamamoto Takeshi."
```

### Customization Instructions

1. **Add domain-specific edge cases** — Financial: rounding errors, currency conversion. Healthcare: HIPAA data handling. E-commerce: inventory race conditions.
2. **Remove items your test framework covers** — If you use property-based testing that auto-generates edge cases, you may not need the boundary values item.
3. **Add performance thresholds** — If performance matters, add: "Response time under expected load stays below {threshold}."

## Template 3: Software Release Checklist

Use this checklist before every production deployment.

### Base Template

```markdown
# Software Release Checklist

> Complete this checklist before initiating production deployment.
> Every unchecked item requires sign-off from the release lead explaining why it's acceptable.

- [ ] **Configuration verified for target environment** — Config files for the target environment have been reviewed. New configuration keys are present. Values are appropriate for production (not dev/staging values). WHY: Configuration mismatches are the #1 cause of deployment failures that pass all automated tests.

- [ ] **Database migrations verified** — All pending migrations have been run in staging successfully. Migration is idempotent (running twice doesn't cause errors). Rollback migration exists and has been tested. WHY: Failed migrations can corrupt production data and are the hardest deployment failures to recover from.

- [ ] **Cache state addressed** — Caches that hold data affected by this release have been identified. Invalidation strategy is defined (manual flush, TTL expiry, versioned keys). WHY: Stale cache data causes users to see old behavior after deployment, creating confusion and bug reports for "bugs" that are actually cache issues.

- [ ] **Feature flags configured correctly** — New features behind feature flags are set to the correct state (enabled/disabled) for this release. Kill switches are verified. WHY: Features accidentally enabled in production before they're ready cause user-facing incidents.

- [ ] **Rollback plan documented** — A specific rollback procedure exists for this release. The rollback has been tested in staging. The team knows who is authorized to trigger rollback and under what conditions. WHY: When a production deployment fails at 2 AM, there's no time to figure out rollback procedures. They must be pre-defined and pre-tested.

- [ ] **Monitoring and alerting updated** — Dashboards include metrics for new components. Alert thresholds are set for new services. On-call team has been notified of the release. WHY: Deploying new components without monitoring means failures are discovered by users, not by engineers.
```

### Customization Instructions

1. **Add security items if relevant** — "Security scan passed" or "Penetration test results reviewed."
2. **Add compliance items** — SOC2, HIPAA, PCI requirements for releases.
3. **Add communication items** — "Release notes published" or "Customer success team notified."
4. **Adapt to deployment model** — Blue/green deployments may need different items than rolling deployments.

## Checklist Design Rules Summary

| Rule | Good Example | Bad Example |
|------|-------------|-------------|
| **Independent items** | "No hardcoded config values" (can check anytime) | "Submit config form, then verify table" (dependent) |
| **Not automatable** | "Error messages provide diagnostic context" (needs judgment) | "Code passes linting" (automate this) |
| **Specific** | "Null checks on all external API response fields" | "Good error handling" |
| **States the obvious** | "No credentials in code" | (omitted because "everyone knows") |
| **Small** | 7 items per checklist | 50 items in one mega-checklist |
| **Has WHY** | "WHY: Silent failures are impossible to diagnose" | (no explanation, item seems arbitrary) |

## Compliance Strategy: The Hawthorne Effect

### What It Is

The Hawthorne Effect: when people know they are being observed or monitored, their behavior changes and they generally do the right thing.

### How to Apply It

1. **Announce spot-checks** — Tell the team that completed checklists will be randomly verified for accuracy. The announcement matters more than the frequency.
2. **Actually spot-check occasionally** — The tech lead or architect reviews 1-2 completed checklists per week, verifying that checked items were actually done.
3. **Discuss findings constructively** — When a spot-check reveals rubber-stamping, treat it as a coaching moment, not a punishment. "I noticed the config check was marked done but the staging config is missing the new REDIS_URL key. Let's talk about how to make this check easier."
4. **Use visible monitoring** — Website monitoring software, build dashboards, code quality dashboards — all serve as visible "cameras" that remind the team their work is observed.

### What NOT to Do

- Don't create a surveillance culture — the goal is awareness, not fear
- Don't punish people for honest mistakes — the checklist exists to catch mistakes
- Don't spot-check every checklist — that defeats the purpose and creates resentment
- Do make the spot-check process transparent and collaborative

## When NOT to Use Checklists

Not everything needs a checklist. Avoid checklists for:

1. **Simple, well-known processes** — If the team does it correctly every time without thinking, a checklist adds friction without value.
2. **Purely procedural workflows** — Step-by-step procedures belong in runbooks, not checklists.
3. **Fully automatable checks** — If a CI pipeline can verify it, automate it instead of putting it on a human checklist.
4. **Things that change frequently** — Items that change every sprint create maintenance burden. If the checklist needs weekly updates, the items are too specific.
