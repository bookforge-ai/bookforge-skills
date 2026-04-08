---
name: secure-code-review
description: |
  Review code for security vulnerabilities and reliability anti-patterns: scan for SQL injection risks (raw string concatenation into queries), XSS exposure (untyped HTML construction), authorization bypass from multilevel nesting, primitive type obsession, YAGNI-inflated attack surface, and missing framework enforcement for authentication/authorization/rate-limiting. Use when conducting a security code review, auditing a codebase for injection vulnerabilities, checking whether auth logic could be bypassed by nesting errors, evaluating whether RPC backends use hardened interceptor frameworks, or assessing whether type-safety patterns (TrustedSqlString, SafeHtml, SafeUrl) are applied to user-controlled inputs. Produces a categorized security findings report with severity, anti-pattern class, affected locations, and fix recommendations grounded in hardened-by-construction design.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/secure-code-review
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [12]
tags:
  - security
  - code-review
  - secure-coding
  - type-safety
  - injection-prevention
  - xss-prevention
  - sql-injection
  - authorization
  - anti-patterns
  - framework-design
  - reliability
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "Source code directory, individual files, or a pull request diff to review for security and reliability anti-patterns"
    - type: document
      description: "Architecture description or code context if no codebase is directly accessible — falls back to structured review of a described design"
  tools-required: [Grep, Read]
  tools-optional: [Bash, Write]
  mcps-required: []
  environment: "Run inside the repository root. Grep searches the working tree for anti-patterns; Read examines flagged files for confirmation and context."
discovery:
  goal: "Produce a categorized security findings report: each finding includes the anti-pattern class, affected file(s) and line(s), severity, and a concrete fix recommendation"
  tasks:
    - "Scan for SQL injection: raw string concatenation into query functions vs. parameterized queries or TrustedSqlString-style typed builders"
    - "Scan for XSS exposure: unescaped user input in HTML rendering, string-typed URLs, absence of SafeHtml/SafeUrl type wrappers"
    - "Scan for authorization bypass from multilevel nesting: auth/error checks nested more than 2 levels deep"
    - "Scan for primitive type obsession: string/int parameters where distinct types would prevent misuse"
    - "Scan for RPC backend structure: direct handler logic vs. interceptor-based framework for auth, logging, rate-limiting"
    - "Scan for YAGNI complexity: unused parameters, abstract base classes with single concrete implementors, dead code paths"
    - "Synthesize findings into a report with severity tiers and fix recommendations"
  audience:
    roles: ["security-engineer", "software-engineer", "site-reliability-engineer", "tech-lead", "code-reviewer"]
    experience: "intermediate — assumes familiarity with web security concepts and a modern typed programming language"
  triggers:
    - "Security code review requested for a service or module"
    - "Auditing a codebase for injection or XSS vulnerabilities"
    - "Checking whether RPC backends enforce auth/logging via a framework or inline ad hoc logic"
    - "Reviewing a pull request that touches database query construction or HTML rendering"
    - "Assessing whether authorization logic could be bypassed due to nesting structure"
    - "Evaluating a new service before launch for common OWASP vulnerability classes"
  not_for:
    - "Threat modeling or adversary profiling — use adversary-profiling-and-threat-modeling"
    - "Access control policy and least-privilege design — use least-privilege-access-design"
    - "Cryptographic primitive selection"
    - "Infrastructure or network security configuration"
---

## When to Use

Use this skill when you need to systematically review source code for the vulnerability classes that account for the majority of security incidents in production systems: injection attacks, XSS, authorization bypass, and type-safety failures.

Invoke it for:
- Any codebase that constructs database queries, renders user input in HTML, or makes authorization decisions inline rather than via a shared framework
- Pull requests touching query construction, template rendering, or RPC handler registration
- Services that implement authentication, authorization, or rate-limiting directly in each handler rather than in a shared interceptor layer
- Assessing technical debt that may carry latent security risk (excessive nesting, primitive types used for security-sensitive data)

Do not invoke it for full threat modeling, infrastructure security review, or cryptographic design — those are separate concerns covered by other skills.

---

## Context and Input Gathering

Before beginning the review, establish:

1. **Language and framework**: What language is the codebase in? Is there a shared RPC framework, ORM, or template system in use? (This determines which scanning patterns are relevant.)
2. **Entry points**: Where does user-controlled input enter the system? (HTTP request parameters, RPC request fields, file uploads, headers.)
3. **Database access pattern**: Does the codebase use an ORM, raw query strings, prepared statements, or a typed query builder?
4. **HTML rendering**: Is HTML rendered server-side? Which template engine? Does it auto-escape by default?
5. **Authorization model**: Is authorization enforced at a framework/interceptor layer or inline in each handler?
6. **Prior review history**: Are there known exemptions, legacy `unsafe` packages, or known TODO/FIXME annotations around security logic?

If no codebase is accessible, conduct a structured interview covering the above before proceeding.

---

## Process

### Step 1 — Scan for SQL Injection Vulnerabilities

**WHY**: SQL injection is the top OWASP vulnerability class. String concatenation into query functions allows attackers to inject arbitrary SQL commands. The only reliable fix is to make mixing user input and SQL structurally impossible — either through parameterized queries enforced by the framework, or a typed query builder (TrustedSqlString pattern) that the compiler enforces.

Search for raw string concatenation into database query calls:

```
Grep pattern: db\.query\(.*\+|db\.exec\(.*\+|execute\(.*\+|query\(["'].*\+
Grep pattern: f"SELECT|f"INSERT|f"UPDATE|f"DELETE   (Python f-strings with SQL keywords)
Grep pattern: "SELECT.*" \+|"INSERT.*" \+|"UPDATE.*" \+   (Java/Go string concat)
```

For each match, Read the flagged file and determine:
- **Confirmed injection risk**: User-controlled input (request parameter, external input) is concatenated directly into the query string. Mark as **Critical**.
- **Developer-controlled concatenation only**: String literals are concatenated but no external input reaches the query. Mark as **Low** but flag for refactoring toward a typed builder.
- **Parameterized / prepared statement**: Input is bound via `?`, `$1`, or named parameters. **Pass** — note the pattern for consistency.

**Fix recommendation for Critical findings**: Replace string concatenation with parameterized queries or a typed query builder. The TrustedSqlString pattern makes injection structurally impossible by construction:

```go
// BEFORE (vulnerable): string concatenation
db.query("UPDATE users SET pw_hash = '" + request["pw_hash"]
    + "' WHERE reset_token = '" + request.params["reset_token"] + "'")

// AFTER (safe): parameterized query
q := db.createQuery("UPDATE users SET pw_hash = @hash WHERE token = @token")
q.setParameter("hash", request.params["hash"])
q.setParameter("token", request.params["token"])
db.exec(q)

// BEST (hardened by construction): TrustedSqlString typed builder
// AppendLiteral only accepts string literal arguments (enforced by the compiler).
// User-supplied strings cannot be passed — the type system prevents it.
q.AppendLiteral("UPDATE users SET pw_hash = ")
q.AppendParam(request.params["hash"])  // param binding, not literal
```

If an `unsafequery` or equivalent escape hatch is found, confirm it routes through a security review workflow. Log its presence as a finding requiring manual sign-off.

### Step 2 — Scan for XSS Vulnerabilities

**WHY**: XSS vulnerabilities occur when user-controlled input is rendered into HTML without sanitization. Because HTML has dozens of contexts (element content, attribute values, URL attributes, JavaScript event handlers) each requiring different escaping semantics, manual escaping is unreliable at scale. The correct fix is a type system where `SafeHtml`, `SafeUrl`, and `TrustedResourceUrl` types are produced only by trusted constructors — making it structurally impossible to pass an unsanitized string where a safe value is required.

Search for patterns where string values reach HTML output:

```
Grep pattern: innerHTML\s*=|document\.write\(|\.html\(.*req\.|\.html\(.*param
Grep pattern: render\(.*request\.|template.*\+.*request\.|%s.*request\.
Grep pattern: href\s*=\s*["']?\s*\+|src\s*=\s*["']?\s*\+   (URL attribute injection)
Grep pattern: SafeHtml|SafeUrl|TrustedResourceUrl   (confirm presence in rendering paths)
```

For each HTML rendering site, Read the surrounding code and determine:
- **Unescaped user input in element content**: String from request inserted directly into HTML. Mark as **Critical**.
- **Untyped URL in href/src attribute**: String variable used as a URL — allows `javascript:` scheme injection. Mark as **High**.
- **Auto-escaping template in use**: Template engine escapes all substitutions by default and the context is correctly classified. **Pass**.
- **SafeHtml/SafeUrl type used**: Constructor-enforced safe type. **Pass** — verify the constructor is from the trusted codebase, not user-supplied.

**Fix recommendation for Critical findings**:

```
// BEFORE (vulnerable): string interpolation into HTML
<div>${userAddress}</div>   // attacker sets userAddress to <script>...</script>

// AFTER (safe): use a SafeHtml type produced by a trusted constructor
// The type system rejects strings where SafeHtml is expected.
// For URLs, use SafeUrl or TrustedResourceUrl — they cannot be constructed
// from arbitrary strings at runtime:
templateRenderer.setMapData(
    ImmutableMap.of("url", TrustedResourceUrl.fromConstant("/script.js"))
).render()
// Passing a plain string variable for "url" is a compile-time error.
```

Flag any template that receives HTML fragments from external (untrusted) sources — these require a sanitizer that parses the HTML, verifies contracts per element, and removes non-conforming content before rendering.

### Step 3 — Scan for Authorization Bypass from Multilevel Nesting

**WHY**: Authorization checks and error handling embedded inside deeply nested conditional blocks are a named reliability and security anti-pattern. When checks occur at nesting level 3 or deeper, the logical relationship between conditions is difficult to follow, and error cases (like "unauthorized") can be silently swapped, bypassed, or reached by an unintended path. Unit tests rarely exercise all combinations of nested conditions.

**Detection criterion**: Flag any code block where an authorization check, permission assertion, or security-relevant error condition appears more than 2 levels of nesting deep (3+ levels of indentation beyond the function body).

Search for deep nesting around auth-related terms:

```
Grep pattern: (if|else|try|catch|for|while).*\n.*\1.*\n.*\2.*auth|permission|unauthorized|forbidden|access_denied
```

Because regex cannot reliably count indentation levels, use Grep to locate function bodies containing both deep nesting keywords and security-relevant terms, then Read the flagged files to manually assess nesting depth.

**Concrete example from the chapter** — the two versions below are logically equivalent, but the left version has a critical bug that is easy to miss:

```python
# BEFORE (vulnerable nesting — bug: 'wrong encoding' and 'unauthorized' are SWAPPED)
response = stub.Call(rpc, request)
if rpc.status.ok():
    if response.GetAuthorizedUser():
        if response.GetEnc() == 'utf-8':
            vals = [ParseRow(r) for r in response.GetRows()]
            avg = sum(vals) / len(vals)
            return avg, vals
        else:
            raise ValueError('no rows')      # BUG: should be 'wrong encoding'
    else:
        raise AuthError('unauthorized')      # BUG: should be 'no rows'
else:
    raise ValueError('wrong encoding')       # BUG: should be RpcError

# AFTER (safe — early exit, each check handled at its own level)
response = stub.Call(request, rpc)
if not rpc.status.ok():
    raise RpcError(rpc.ErrorText())
if not response.GetAuthorizedUser():
    raise ValueError('wrong encoding')
if response.GetEnc() != 'utf-8':
    raise AuthError('unauthorized')
if not response.GetRows():
    raise ValueError('no rows')
vals = [ParseRow(r) for r in response.GetRows()]
avg = sum(vals) / len(vals)
return avg, vals
```

**Fix recommendation**: Refactor using the early-exit (guard clause) pattern — handle each error condition as soon as it can be detected, at the top level of the function. Authorization checks should execute first, before any other logic, and should fail fast with a clear error.

Mark findings as **High** when the mishandled case is an auth/permission check; **Medium** when it is a generic error path.

### Step 4 — Scan for Primitive Type Obsession

**WHY**: Using raw strings or integers for parameters that carry security-sensitive semantic meaning — user IDs, group names, token values, URLs — leads to misuse that the compiler cannot catch. Arguments can be passed in wrong order, values can be truncated or implicitly converted, and security invariants cannot be enforced without runtime checks scattered throughout the codebase. Strong types wrap the primitive and encode the invariant in the type system, enforced at compile time.

Search for functions with multiple adjacent string or int parameters in security-sensitive contexts:

```
Grep pattern: func.*\(.*string,\s*string|def.*\(.*str,\s*str   (adjacent string params)
Grep pattern: AddUser.*string.*string|AddRole.*string.*string   (identity/permission functions)
Grep pattern: query\(.*string\)|execute\(.*string\)   (string-typed query params)
```

For each match, Read the function signature and callers to assess:
- **Security-relevant ambiguity**: Two or more string parameters where transposing them could produce a security failure (e.g., `addUserToGroup(username, groupName)` — which order?). Mark as **Medium**.
- **URL or HTML typed as string**: A `string` parameter used as a URL or HTML fragment that could accept a `javascript:` URI or raw HTML. Mark as **High**.
- **Non-security ambiguity**: Ambiguous parameter ordering but no security consequence. Mark as **Low** / code quality.

**Fix recommendation**:

```
// BEFORE: ambiguous, compiler cannot catch argument transposition
AddUserToGroup(string, string)   // which is user, which is group?

// AFTER: strong types make the call self-documenting and compiler-enforced
Add(User("alice"), Group("root-users"))
// User and Group are distinct types wrapping string — passing them in
// wrong order is a compile-time error.

// For URLs: use SafeUrl or TrustedResourceUrl instead of string
// For HTML content: use SafeHtml instead of string
```

### Step 5 — Evaluate RPC Backend Framework Usage

**WHY**: The most common security and reliability failures in RPC backends — skipped authentication, inconsistent authorization, missing rate limiting, incomplete logging — occur when each handler reimplements these cross-cutting concerns independently. A framework with predefined interceptors (before/after hooks around each RPC) enforces that every call passes through logging, authentication, authorization, and rate limiting in order, regardless of which developer wrote the handler. Centralized framework logic can be fixed once and applied everywhere; ad hoc per-handler logic must be audited and fixed in every handler.

Search for RPC handler implementations:

```
Grep pattern: func.*Handler\(|def.*handler\(|@app\.route|RegisterHandler
Grep pattern: func.*Before\(.*Request|func.*After\(.*Response   (interceptor pattern — positive signal)
```

For each handler file, Read and assess:

**Interceptor pattern present (positive)**:
```go
// Authorization interceptor — framework-enforced
type authzInterceptor struct {
    allowedRoles map[string]bool
}
func (ai *authzInterceptor) Before(ctx context.Context, req *Request) (context.Context, error) {
    callInfo, err := FromContext(ctx)   // callInfo populated by the framework
    if err != nil { return ctx, err }
    if ai.allowedRoles[callInfo.User] { return ctx, nil }
    return ctx, fmt.Errorf("Unauthorized request from %q", callInfo.User)
}
func (*authzInterceptor) After(ctx context.Context, resp *Response) error {
    return nil  // nothing left to do after the RPC is handled
}
```
Mark as **Pass** — the framework handles auth before RPC logic executes. Authorization interceptors that return an error prevent the RPC from executing, but still call the `After` stage of each already-invoked interceptor, ensuring logging completes.

**Ad hoc inline auth (anti-pattern)**:
```
// Each handler manually checks credentials — no guaranteed ordering
func HandleRequest(req *Request) (*Response, error) {
    if req.Token == "" { return nil, ErrUnauthorized }
    // ... business logic with no guaranteed logging ...
}
```
Mark as **High** — auth can be skipped or ordered differently across handlers, logging is not guaranteed, and rate limiting is missing. Recommend migrating to an interceptor-based framework where logging, authentication, authorization, and rate limiting are defined once and applied to every RPC call.

The interceptor execution order that should be enforced: **Logging → Authentication → Authorization → Rate Limiting → RPC Logic**. On error at any stage, the `after` stages of all previously executed interceptors still run (ensuring logs are always written).

### Step 6 — Scan for YAGNI Complexity

**WHY**: Speculative code written "just in case it might be needed" adds surface area that must be secured, tested, and maintained. Unused parameters and abstract interfaces with a single concrete implementor increase the complexity of reasoning about control flow — which is where security bugs hide. Simpler code has fewer paths that can be exploited.

Search for indicators of YAGNI complexity:

```
Grep pattern: virtual.*=\s*0|abstract.*def\b   (abstract methods — check for single implementor)
Grep pattern: TODO|FIXME|HACK                  (debt that may be load-bearing for security logic)
Grep pattern: bool.*=\s*false\b|bool.*=\s*true\b   (boolean flags with suspicious defaults)
```

For each abstract interface or virtual method found, Read the file and search for all implementors. If exactly one concrete implementation exists, flag as **Low** — evaluate whether the abstraction is warranted or whether it adds unnecessary complexity.

For boolean parameters in security-sensitive functions (e.g., `hibernate = false` always passed by callers), Read all call sites. If all callers pass the same value, the parameter is dead weight — the code must handle a case that never occurs, and that handling code introduces reliability risk (error paths never exercised by tests).

**Fix recommendation**: Delete the unused path. Apply the principle of incremental development: implement the abstraction when a second concrete implementation actually exists.

### Step 7 — Synthesize Findings into a Report

**WHY**: Raw findings from individual scans need to be prioritized by severity and organized by fix effort so the team can address the most critical issues first without being overwhelmed by the full list.

Produce a report with the following structure:

```
## Security Review Findings: [codebase / PR / module name]
**Date**: [date]
**Reviewer**: [agent or reviewer name]
**Scope**: [files/directories reviewed]

### Critical
[Finding ID] | [Anti-Pattern Class] | [File:Line] | [Description]
Fix: [concrete recommendation]

### High
[same structure]

### Medium
[same structure]

### Low / Code Quality
[same structure]

### Passes (positive patterns noted)
[Interceptor framework present in X, parameterized queries used throughout Y, SafeHtml used in template layer]

### Recommended Next Steps
1. [Highest-priority fix — typically Critical SQL injection or XSS]
2. [Framework migration if ad hoc auth found]
3. [Type hardening for security-sensitive parameters]
```

Severity assignments:
- **Critical**: User-controlled input directly concatenated into SQL or HTML rendering
- **High**: Untyped URLs, inline auth with no framework enforcement, auth check nested >2 levels
- **Medium**: Primitive type obsession in security-sensitive signatures, medium-depth nesting in error paths
- **Low**: YAGNI complexity, developer-controlled SQL concatenation, minor code quality

---

## Key Principles

**Make security invariants impossible to violate by construction.** Guidelines and code review cannot scale. A type system that prevents mixing user input with SQL query strings — or prevents passing a string where `SafeHtml` is required — removes an entire vulnerability class regardless of developer attention. Design APIs so the insecure path is the hard path.

**Security cannot be retrofitted.** Tacking on security after launch is painful and often requires changing fundamental assumptions. The patterns in this skill (interceptors, typed wrappers, early-exit auth) must be applied during implementation, not after the fact.

**Centralize cross-cutting security logic.** Authentication, authorization, logging, and rate limiting belong in a shared framework or interceptor layer — not reimplemented in each handler. When domain experts fix a vulnerability in a centralized framework, it is fixed everywhere simultaneously.

**Nesting is complexity is risk.** Deep conditional nesting makes control flow hard to reason about. Security checks that appear in nested branches are frequently swapped, bypassed, or untested. The early-exit pattern — check preconditions at the top of the function and fail fast — is both simpler and more secure.

**YAGNI applies to attack surface.** Every abstract interface, unused parameter, and speculative code path is surface area that must be secured and maintained. Avoid implementing features that are not currently needed. Add complexity when a second concrete use case actually arrives.

**Frameworks improve developer productivity and security simultaneously.** Developers using a framework only need to specify what is specific to their service (which authorization policy, which data to log). The framework handles the rest. This frees developer attention for business logic and reduces the chance of security-relevant omissions.

---

## Examples

### Example 1 — RPC Backend: Interceptor Framework vs. Ad Hoc Auth

**Scenario**: Reviewing a Go RPC service with 12 handlers. Some handlers check credentials manually; others omit the check entirely.

**Finding**: Ad hoc inline credential check — High severity. No guaranteed ordering. Logging occurs only in some handlers.

**Positive pattern to look for** (interceptor framework):

```go
// Framework interceptor chain: Logging → Auth → Authorization → Rate Limiting → RPC Logic
// Each stage runs Before (pre-RPC) and After (post-RPC, always runs even on error).

// Authorization interceptor:
type authzInterceptor struct{ allowedRoles map[string]bool }

func (ai *authzInterceptor) Before(ctx context.Context, req *Request) (context.Context, error) {
    callInfo, err := FromContext(ctx)  // populated by framework from verified credentials
    if err != nil { return ctx, err }
    if ai.allowedRoles[callInfo.User] { return ctx, nil }
    return ctx, fmt.Errorf("Unauthorized request from %q", callInfo.User)
}

// Logging interceptor (logs every request before, and every failure after):
func (*logInterceptor) Before(ctx context.Context, req *Request) (context.Context, error) {
    callInfo, _ := FromContext(ctx)
    logger.Log(ctx, &pb.LogRequest{
        Timestamp: time.Now().Unix(), User: callInfo.User, Request: req.Payload,
    }, WithAttemptCount(3))
    return ctx, nil
}
func (*logInterceptor) After(ctx context.Context, resp *Response) error {
    if resp.Err == nil { return nil }
    logger.LogError(ctx, &pb.LogErrorRequest{
        Timestamp: time.Now().Unix(), Error: resp.Err.Error(),
    }, WithAttemptCount(3))
    return nil
}
```

**Recommendation**: Migrate all handlers to register with the interceptor framework. Remove inline credential checks. The framework guarantees every call is logged before and after, authenticated, authorized against the allowed-roles policy, and rate-limited — regardless of which developer wrote the handler.

### Example 2 — SQL Injection: TrustedSqlString Pattern

**Scenario**: Reviewing a password reset endpoint. The query is constructed by string concatenation.

**Finding**: Critical SQL injection — user-controlled `reset_token` concatenated directly into the query string.

```python
# Vulnerable (real code pattern from the chapter):
db.query("UPDATE users SET pw_hash = '" + request["pw_hash"]
    + "' WHERE reset_token = '" + request.params["reset_token"] + "'")
# An attacker sets reset_token = "' OR username='admin" to reset admin's password.
```

**Fix**: Parameterized query eliminates injection. Typed builder (TrustedSqlString) makes it impossible by construction — `AppendLiteral` only accepts compile-time string constants; user input cannot be passed:

```go
// TrustedSqlString typed builder — Go example:
struct Query { sql strings.Builder }
type stringLiteral string  // package-private; outside code cannot construct it
func (q *Query) AppendLiteral(literal stringLiteral) { q.sql.WriteString(string(literal)) }
// q.AppendLiteral("foo")  -- compiles (string literal implicitly converts)
// q.AppendLiteral(foo)    -- does NOT compile (variable cannot convert to stringLiteral)
```

If a legacy `unsafequery` escape hatch is found in the codebase, gate all new uses behind a security review approval workflow (visibility allow-listing). Each new use must be individually reviewed; the review load is manageable precisely because the typed API prevents most cases.

### Example 3 — XSS: SafeHtml and SafeUrl Type Enforcement

**Scenario**: A web application renders user-provided profile data into HTML templates.

**Finding**: High severity — `userAddress` is a string interpolated directly into an HTML element:

```html
<!-- Vulnerable: attacker sets userAddress to <script>exfiltrate_user_data();</script> -->
<div>${userAddress}</div>
```

**Fix**: The rendering layer must require `SafeHtml` for element content and `SafeUrl` / `TrustedResourceUrl` for URL attributes. The types are immutable wrappers — their constructors are the only trusted codebase that can produce them:

```java
// Template substitution with SafeHtml enforcement:
// Passing a plain String where SafeHtml is expected is a compile-time error.
templateRenderer.setMapData(
    ImmutableMap.of("address", SafeHtml.fromConstant("..."))  // only from trusted constructors
).render();

// For URL attributes — TrustedResourceUrl rejects javascript: scheme at construction:
templateRenderer.setMapData(
    ImmutableMap.of("url", TrustedResourceUrl.fromConstant("/script.js"))
).render();
// templateRenderer.setMapData(ImmutableMap.of("url", some_string_variable)) -- compile error
```

If the application receives HTML fragments from an external (untrusted) source, use a sanitizer that parses the HTML, verifies type contracts per element, and removes elements or attributes that do not meet their contract — rather than rendering the fragment directly.

---

## References

- [security-anti-pattern-catalog.md](../../references/security-anti-pattern-catalog.md) — Full catalog of named anti-patterns from Chapter 12: multilevel nesting, primitive type obsession, YAGNI smells, ad hoc framework reimplementation
- [owasp-top10-framework-mitigations.md](../../references/owasp-top10-framework-mitigations.md) — OWASP Top 10 vulnerability classes mapped to framework-level hardening measures (Table 12-1)
- [trusted-sql-string-pattern.md](../../references/trusted-sql-string-pattern.md) — TrustedSqlString implementation guide: Go (package-private type alias), Java (@CompileTimeConstant), C++ (template constructor); incremental rollout strategy; unsafequery escape hatch governance
- [safe-html-safe-url-pattern.md](../../references/safe-html-safe-url-pattern.md) — SafeHtml and SafeUrl type system: constructor trust model, Closure Templates integration, HTML sanitizer usage, TrustedResourceUrl for script/stylesheet URLs
- [rpc-interceptor-framework.md](../../references/rpc-interceptor-framework.md) — Interceptor framework design for RPC backends: context object, before/after execution model, dependency registration, exponential backoff, cascading failure prevention

Cross-references:
- `adversary-profiling-and-threat-modeling` — identify which threat actors make injection and XSS vulnerabilities most consequential
- `least-privilege-access-design` — authorization framework design and access control policy complement the inline auth review in Step 5

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
