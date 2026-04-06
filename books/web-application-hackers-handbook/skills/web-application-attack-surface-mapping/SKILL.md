---
name: web-application-attack-surface-mapping
description: |
  Systematically map a web application's content, entry points, technologies, and attack surface during authorized security testing or security-focused code review. Use this skill whenever you are performing reconnaissance on a web application, need to enumerate application functionality and hidden content, want to identify all user-input entry points (URLs, query parameters, POST fields, cookies, HTTP headers), need to fingerprint server-side technologies from HTTP responses, or are building an attack surface inventory before vulnerability testing. Also invoke it when analyzing application behavior to infer server-side structure, looking for undiscovered directories and files through brute-force enumeration, using search engines or web archives to find historical content, probing for hidden debug parameters, mapping functional paths in parameter-driven applications, or producing a behavior-to-vulnerability mapping that prioritizes which areas to probe first. Produces a structured attack surface map: enumerated URLs and functional paths, identified entry points, technology fingerprint, and a prioritized vulnerability-class checklist. Does not perform active exploitation — use this before any active testing phase.
version: 1
status: draft
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [4]
tags:
  - web-security
  - penetration-testing
  - reconnaissance
  - attack-surface
  - web-spidering
  - content-discovery
  - directory-enumeration
  - entry-points
  - server-fingerprinting
  - owasp
  - burp-suite
  - hidden-content
  - http-headers
  - sql-injection
  - xss
  - access-control
  - session-management
  - appsec
  - security-testing
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code, HTTP traffic logs, proxy history, or configuration files for the target application — any of these can substitute for live access"
    - type: document
      description: "Architecture diagrams, API specifications, prior security reports, or a description of the application when live access or a codebase is unavailable"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Run inside a project directory containing source code, HTTP capture files, or application artifacts. For live-target analysis, the agent analyzes intercepted traffic; the human operates the browser and proxy tool."
discovery:
  goal: "Produce a complete attack surface map: content inventory, entry point catalog, technology fingerprint, and behavior-to-vulnerability priority matrix"
  tasks:
    - "Enumerate application content and functional paths through spidering and source analysis"
    - "Discover hidden content using brute-force, inference-based naming, and public sources"
    - "Identify all user-input entry points including non-obvious ones (HTTP headers, out-of-band channels)"
    - "Fingerprint server-side technologies from banners, file extensions, directory names, and session tokens"
    - "Infer server-side functionality and logic from request structure and parameter semantics"
    - "Map application behavior to the most likely vulnerability classes"
    - "Identify anomalous or bolted-on functionality that may escape the application's standard security framework"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-architect", "bug-bounty-hunter", "secure-code-reviewer"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, web application architecture, and proxy tools"
  triggers:
    - "Starting a web application penetration test"
    - "Mapping attack surface before vulnerability scanning or manual testing"
    - "Performing reconnaissance on a web application"
    - "Enumerating hidden content, directories, or undiscovered functionality"
    - "Identifying all user-input entry points in an application"
    - "Fingerprinting server-side technologies from HTTP traffic"
    - "Building a checklist of vulnerability areas to test"
  not_for:
    - "Active exploitation of identified vulnerabilities — this skill maps, it does not exploit"
    - "Network-layer reconnaissance (port scanning, service enumeration) — scope is the HTTP application layer only"
    - "Automated scanning without a human in the loop — use this to direct and interpret automated tools, not replace the analyst"
---

## When to Use

Use this skill at the **start of any authorized web application security engagement** — before any vulnerability probing, scanning, or exploitation. The mapping phase determines which areas of the application are worth investing time in and which vulnerability classes are most likely.

Invoke it when:
- You have explicit authorization to test a web application (bug bounty scope, penetration test contract, internal security review, or own application)
- You are beginning a code review with a security focus and need to understand the application's attack surface before diving into individual functions
- You want to identify all the ways user-controlled data enters the application — not just the obvious form fields
- You have proxy traffic, source code, or application artifacts to analyze and need a structured methodology

Do not invoke it for unauthorized access to systems you do not own or have permission to test.

---

## Context and Input Gathering

### Required Context (must have — ask if missing)

- **Authorization confirmation:** Has explicit authorization for testing been granted?
  - Check prompt for: keywords like "authorized," "bug bounty," "pentest," "internal review," "own application"
  - If missing, ask: "Do you have explicit authorization to perform security testing on this application? If yes, what is the scope?"

- **Target definition:** What is the application being mapped?
  - Check prompt for: a URL, domain name, application name, or codebase path
  - Check environment for: source code directory, HTTP capture files (`.har`, Burp export), or API spec files
  - If still missing, ask: "What is the target application? (URL, codebase path, or description)"

### Observable Context (gather from environment)

- **Source code available:** Look for web framework files (`routes.py`, `urls.py`, `web.xml`, `routes.rb`, `*.controller.ts`), config files (`application.properties`, `.env`), and template directories.
- **HTTP traffic available:** Look for `.har` files, Burp Suite exports, or traffic captures in the working directory.
- **Existing security artifacts:** Look for prior pentest reports, OpenAPI/Swagger specs, or architecture diagrams.
- **Technology indicators:** Look for `package.json`, `pom.xml`, `Gemfile`, `requirements.txt`, `composer.json` to infer the stack without HTTP traffic.

### Default Assumptions

- If no proxy tool is specified, Burp Suite Community/Professional is assumed as the primary interception proxy.
- If authorization is unclear from a codebase-only review context, assume the user owns or has authorization to review the application.
- If no scope boundary is stated, treat the entire domain (and its subdomains if mentioned) as in-scope.

---

## Process

### Step 1: Establish the Spidering Baseline

**ACTION:** Walk through the application manually using a browser proxied through an interception tool (Burp Suite, OWASP ZAP, or equivalent), visiting every linked page and submitting every form. Simultaneously, run an automated spider against the already-visited content.

**WHY:** Automated spiders miss content hidden behind JavaScript navigation, Flash/Java applets, forms with validation, and authentication-protected areas. User-directed spidering with a proxy captures everything the human can see — including JavaScript-triggered navigation — while the proxy parses all server responses for additional content automatically. The combination is more thorough than either technique alone.

**Procedure:**
1. Configure the browser to route all traffic through the proxy
2. Browse the entire application normally: click every link, submit every form with valid-looking data, complete all multi-step workflows (registration, checkout, password reset)
3. Try browsing with JavaScript enabled, then disabled — some applications serve different content in each mode
4. Try browsing with cookies enabled, then disabled — some content paths are reachable only in the cookieless state
5. After completing the manual walk-through, review the proxy's site map for any content identified by parsing server responses that you did not visit directly
6. For any such content, access it manually through the browser so that the proxy can parse the server's response for further links
7. Repeat Step 6 recursively until no new content appears
8. Check `robots.txt` — it frequently lists directories the application owner does not want indexed, which are often the most sensitive areas worth testing

**AGENT: EXECUTES** (when source code is available) — grep for all route definitions, template links, and form `action` attributes to produce a complete URL list without live access.

**HANDOFF TO HUMAN** (when live access is required) — the human browses while the proxy captures traffic; the agent analyzes the captured site map.

**WARNING:** Never run an automated spider against an application without first identifying and excluding dangerous endpoints (admin delete functions, data-erasure operations, logout URLs). An automated spider that follows all links can cause real damage — defacing content, deleting users, or breaking sessions.

---

### Step 2: Discover Hidden Content

**ACTION:** Enumerate content not linked from the visible application using three complementary techniques: brute-force enumeration, inference from naming patterns, and mining public sources.

**WHY:** Applications routinely contain unlinked content — debug pages left from development, old versions not removed from the server, functionality visible only to higher-privilege users, configuration files with credentials, and backup copies of live pages. None of these appear in a spider's site map. Finding them can reveal critical vulnerabilities that the main application surface does not expose.

**2a. Brute-Force Enumeration**

Use a tool with a wordlist (Burp Intruder, DirBuster, ffuf, gobuster, or a custom script) to request common directory names and file names within every known directory:

1. Make test requests for known-valid and known-invalid resources first to establish how the server signals a missing resource. Many applications return `200 OK` with a custom "not found" page rather than `404`. Record the response fingerprint for genuinely missing resources so you can filter it from results.
2. Start at the web root and enumerate common directory names
3. For each discovered directory, enumerate common file names within it
4. Capture the full response (not just status code) and review manually — a `302` redirect to the login page indicates an authenticated-only resource that exists; a `401`/`403` indicates an existing but access-restricted resource; a `500` often indicates a resource that exists and expects specific parameters
5. Perform each exercise recursively as new directories are found

**Response code interpretation guide:**
- `200 OK` — Resource exists and is accessible (verify it is not a custom "not found" page)
- `302` to login page — Resource exists, authentication required
- `302` to error page — May indicate a different condition; investigate further
- `401 Unauthorized` / `403 Forbidden` — Resource exists but access is restricted regardless of privilege level
- `400 Bad Request` — May indicate nonstandard naming conventions or invalid wordlist entries
- `500 Internal Server Error` — Resource likely exists and expects specific parameters

**2b. Inference from Naming Patterns**

1. Review all enumerated resources to identify naming conventions (capitalization style, abbreviation patterns, verb prefixes like `Add`, `Edit`, `View`, `Delete`)
2. Infer sibling resources: if `ForgotPassword` exists in `/auth`, look for `ResetPassword`, `ChangePassword`, `UpdatePassword`
3. For numeric identifiers in URLs (e.g., `/pub/media/117`), probe adjacent values in the observed range
4. Add common backup and temporary extensions to known file stems: `.bak`, `.src`, `.inc`, `.old`, `.tmp`, `.php-1`, `.DS_Store`
5. For source files compiled into live pages (`.java`, `.cs`), request the source extension — misconfigured servers may serve raw source code

**2c. Mine Public Sources**

1. Query search engines using advanced operators against the target domain:
   - `site:target.com` — all indexed pages
   - `site:target.com admin` — pages containing specific keywords (administrative areas, login functions)
   - `link:target.com` — pages on other sites that link to the target (may reveal partner-only URLs)
2. Check web archives (Wayback Machine at `archive.org`) for historical content that may no longer be linked but is still live on the server
3. Search developer forums and issue trackers for the names of known developers — technical questions they posted may reveal functionality, technology choices, or known bugs
4. View cached versions of pages to find content that requires authentication or payment on the live site

**AGENT: EXECUTES** — analyzes source code for hardcoded paths, commented-out links, disabled form fields, and server-side include references. Produces a candidate URL list.

**HANDOFF TO HUMAN** — wordlist-based brute-force and live HTTP probing require tool execution against a live target.

---

### Step 3: Identify All User-Input Entry Points

**ACTION:** Catalog every location where user-controlled data enters the application — including non-obvious channels that are frequently overlooked.

**WHY:** Vulnerability testing is only as comprehensive as the entry point catalog. Missed entry points mean missed vulnerabilities. Many critical flaws (SQL injection, cross-site scripting, path traversal) are discovered at entry points that automated scanners miss because they do not appear in HTML forms — they appear in HTTP headers, URL path segments, or out-of-band channels.

**Entry point categories to enumerate:**

| Category | What to collect |
|---|---|
| URL path segments | Every segment in REST-style URLs (e.g., `electronics` and `iPhone3G` in `/shop/browse/electronics/iPhone3G/`) |
| URL query string parameters | Every `name=value` pair, including non-standard separators (`;`, `$`, `%3d`) |
| POST body parameters | Every field in every form, including hidden fields |
| Cookies | Every cookie name and value |
| Standard HTTP request headers | `User-Agent`, `Referer`, `Accept`, `Accept-Language`, `Host` — all may be logged or processed |
| Custom HTTP headers | `X-Forwarded-For`, `X-Real-IP`, and any application-specific headers — often processed for IP-based access control or geolocation |
| Out-of-band channels | Email content processed by a mail-parsing function, HTTP content fetched by server-side URL retrievers, data from APIs consumed by the application |

**Special attention — HTTP headers:** Many applications trust the `X-Forwarded-For` header for the client's IP address when running behind a proxy. If this header is processed without validation, injecting SQL or scripting content into it can trigger injection vulnerabilities. Similarly, spoofing `User-Agent` to a mobile device string often reveals a separate mobile-optimized code path that has received less security review.

**Special attention — non-standard parameter formats:** If the application does not use the standard `name=value&name2=value2` format, understand the actual encoding before testing. Treating a URL like `/dir/file?data=%3cfoo%3e%3c%2ffoo%3e%3cbar%3e%3c%2ffoo2%3e%3e` as a single parameter called `data` will miss injection points inside the embedded XML.

---

### Step 4: Fingerprint Server-Side Technologies

**ACTION:** Determine the technology stack — web server software and version, application framework, programming language, database, and third-party components — from the available indicators.

**WHY:** Technology identification directly predicts which vulnerability classes to prioritize. A PHP application on Apache has a different vulnerability profile than a Java application on WebSphere. Known third-party components may have published Common Vulnerabilities and Exposures (CVEs) that are directly exploitable. Version information enables precise vulnerability lookup.

**Fingerprinting sources:**

| Indicator | Where to look | What it reveals |
|---|---|---|
| `Server` HTTP header | Every HTTP response | Web server software and version |
| `X-Powered-By` header | Application responses | Framework (e.g., `PHP/7.4`, `ASP.NET`) |
| Custom headers | Non-standard headers in responses | Application-specific platform details |
| HTML source comments | Page source, especially error pages | Developer notes, framework version, build info |
| File extensions | URLs across the site map | Programming language (`.jsp`=Java, `.aspx`=ASP.NET, `.php`=PHP, `.py`=Python, `.rb`=Ruby, `.cfm`=ColdFusion) |
| Directory names | URL structure | Servlet containers (`/servlet/`), ColdFusion (`/cfdocs/`, `/cfide/`), Rails (`/rails/`) |
| Session token names | Cookie names in HTTP responses | Platform (`JSESSIONID`=Java, `ASPSESSIONID`=IIS, `PHPSESSID`=PHP, `CFID/CFTOKEN`=ColdFusion) |
| Error page format | 404, 500 responses | Framework-generated error pages are distinctive |
| URL patterns with comma-separated numbers | URL structure | Vignette content management platform |

**HTTP fingerprinting:** Even when the `Server` header is suppressed or falsified, behavior differences in how the server handles invalid requests, the ordering of response headers, and the exact formatting of error messages can identify the underlying software. Run a behavioral fingerprinting tool (httprecon, WhatWeb) against the target when banner-based identification is inconclusive.

**Third-party component identification:** Search for the names of unusual cookies, custom HTTP headers, or distinctive JavaScript library calls. Locate other applications using the same component to understand its full feature set and known vulnerabilities. Check CVE databases for the identified component and version.

---

### Step 5: Infer Server-Side Functionality and Structure

**ACTION:** Reason about the server-side implementation by analyzing request structure, parameter names, and application behavior — treat every observable artifact as a clue about how the server processes requests.

**WHY:** Understanding what the server is doing enables identification of vulnerability classes that are not yet visible from the application's surface. Parameters named `OrderBy` suggest database queries where the value may be used directly in an SQL `ORDER BY` clause. Parameters named `template` or `loc` suggest file retrieval that may be vulnerable to path traversal. Boolean parameters set to `false` may control functionality that attackers benefit from setting to `true`.

**Analysis approach:**

1. For each request, review every parameter name and value in context of the function being performed. Ask: "What server-side mechanism is most likely handling this?" Common patterns:
   - `OrderBy`, `sort`, `sortField` parameters → SQL `ORDER BY` injection candidates
   - `template`, `page`, `include`, `file`, `path` parameters → path traversal or server-side include candidates
   - `redirect`, `url`, `next`, `returnUrl` parameters → open redirect candidates
   - `to`, `from`, `subject` parameters in mail-sending functions → email header injection candidates
   - `isExpired`, `isAdmin`, `edit`, `debug` Boolean parameters → access control bypass candidates by toggling the value

2. Look for consistent patterns across functions — if input sanitization is applied in one area, it may be uniformly applied (or uniformly absent) across the application. A function that visibly echoes user input to the page reveals the sanitization logic, which you can then test against other entry points.

3. Identify areas where behavior diverges from the application's norm — different visual style, different parameter naming conventions, commented-out code referencing a different framework. These "bolted-on" areas are frequently missing from the application's standard security controls (authentication checks, CSRF tokens, input validation middleware).

---

### Step 6: Map Behavior to Vulnerability Classes

**ACTION:** For each functional area identified, assign the most likely vulnerability classes based on the behavior and technology patterns observed.

**WHY:** Attack surface mapping is only actionable when it produces a prioritized test plan. A behavior-to-vulnerability matrix translates the reconnaissance findings into specific things to test, preventing both the unfocused "test everything" approach and the risk of missing high-probability vulnerability areas.

Apply this mapping:

| Observed Behavior or Functionality | Primary Vulnerability Classes to Investigate |
|---|---|
| Client-side input validation in forms | Server-side validation bypass (checks may not be replicated on server) |
| Database interaction (search, filtering, ordering) | SQL injection (CWE-89) |
| File upload or download functionality | Path traversal (CWE-22), stored cross-site scripting |
| Display of user-supplied data | Cross-site scripting (CWE-79, reflected and stored) |
| Dynamic redirects (`redirect`, `next`, `returnUrl` parameters) | Open redirect (CWE-601), header injection |
| Social features (user profiles, messaging) | Username enumeration, stored cross-site scripting |
| Login functionality | Username enumeration, weak credential policies, brute-force susceptibility |
| Multi-step login or checkout workflows | Business logic flaws, step-skipping |
| Session tokens issued by server | Predictable token generation, insecure token handling |
| Access control (privilege levels, roles) | Horizontal privilege escalation (CWE-639), vertical privilege escalation (CWE-269) |
| User impersonation or "act as" functionality | Privilege escalation |
| HTTP-only communication (no TLS) | Session hijacking, credential interception |
| Off-site links (third-party resources in page) | Query string parameter leakage via `Referer` header |
| Integration with external systems (payment processors, APIs) | Session shortcutting, access control bypass at integration boundaries |
| Verbose error messages | Information leakage (CWE-209) — internal structure, stack traces, SQL errors |
| Email interaction (contact forms, notification triggers) | Email injection (CWE-93), command injection |
| Native code components or plugins | Buffer overflow (CWE-121) |
| Third-party application components | Known CVEs for identified component and version |
| Identifiable web server software | Configuration weaknesses, known software bugs for identified version |

**Prioritize the map** by combining two factors: likelihood (how often this vulnerability class appears in this technology) and impact (what an attacker gains if it is present). Authentication bypass, SQL injection, and access control flaws are typically highest priority.

---

## Inputs

- Application access (live target via browser + proxy, OR source code directory, OR HTTP traffic captures)
- Scope definition (which domains, paths, user roles are in-scope)
- Authorization confirmation for the target

## Outputs

- **Content inventory:** Enumerated URLs, directories, and functional paths discovered through spidering and content discovery
- **Entry point catalog:** Table of all user-input locations — URL segments, parameters, cookies, HTTP headers, out-of-band channels
- **Technology fingerprint:** Web server, application framework, programming language, database, third-party components with version information where available
- **Functional path map:** For parameter-driven applications, a map showing which parameters control which functions and their logical dependencies
- **Behavior-to-vulnerability matrix:** Prioritized list of functionality areas mapped to vulnerability classes, ordered by estimated risk

---

## Key Principles

- **Coverage before depth** — The mapping phase is about breadth. Resist the urge to probe a promising entry point in depth until the full surface is enumerated. A vulnerability found in the first 10 minutes may be less significant than one hiding in content discovered in the last 10 minutes of mapping. WHY: skilled assessments are always time-boxed; investing testing time against the complete surface produces better risk coverage than deep-diving the first interesting thing found.

- **User-directed spidering beats automated spidering** — Automated spiders miss JavaScript navigation, form validation requirements, and authenticated content. A human browsing with a proxy captures all of these while the tool handles the mechanical parsing work. WHY: modern applications increasingly rely on client-side navigation mechanisms that do not appear in static HTML — a conventional spider that only follows `<a href>` links will miss large portions of the application.

- **Naming patterns are reconnaissance** — The naming conventions a developer uses (verbose vs. abbreviated, verb-first vs. noun-first, CamelCase vs. snake\_case) are consistent and predictable within an application. Mining these patterns dramatically improves brute-force effectiveness. WHY: developers typically write all their code in a consistent personal style; inferring that style from observed names allows you to generate a far more targeted wordlist than a generic dictionary.

- **HTTP headers are entry points** — The `Referer`, `User-Agent`, `X-Forwarded-For`, and `Host` headers are processed by many applications for logging, analytics, access control, and content personalization. Treating them as read-only is a testing oversight. WHY: headers that are logged are often concatenated into queries or log entries without sanitization — the same classes of injection that affect form fields apply to header values that are processed server-side.

- **Bolted-on functionality escapes standard defenses** — In mature applications with centralized security frameworks, the highest-yield areas are not the core functions but the features added after the framework was established. Debug functions, CAPTCHA implementations, third-party integrations, and recently added features often bypass the application's middleware-level input validation and authentication checks. WHY: these additions are frequently built by different developers, under time pressure, and without full awareness of the application's security conventions — they are structurally more likely to contain vulnerabilities.

- **The site map is a prioritization tool, not just a record** — The goal of mapping is not to have a complete list of URLs but to understand which areas deserve the most testing attention and what vulnerability classes are most likely present. A complete map with no prioritization is less useful than a partial map with clear next steps. WHY: testing time is always finite; the attack surface map must translate directly into a test plan.

---

## Examples

**Scenario: External penetration test of an e-commerce platform**

Trigger: "I'm starting a pentest on a client's shopping site. I have authorization and they've given me a staging environment URL."

Process:
1. Configure Burp Suite as proxy; browse the full application — browse product catalog, register an account, complete checkout, test password reset
2. Review Burp's site map; note `robots.txt` discloses `/admin/` and `/staging-api/` — both unlinked from the visible application
3. Run Burp's content discovery against `/admin/` — finds `Admin`, `AdminLogin`, `Dashboard`, `ExportUsers`, `BulkDelete`; `ExportUsers` returns `302` to login, `BulkDelete` returns `200` directly
4. Fingerprint: `Server: Apache/2.4.41`, `X-Powered-By: PHP/7.3`, session cookie named `PHPSESSID`, `/shop/` uses REST-style URLs
5. Entry points catalog: 47 URL parameters, 12 POST fields, 8 cookies, `X-Forwarded-For` header processed for free-shipping threshold check
6. Map `/admin/BulkDelete` (no auth required, `200` response) → access control bypass; REST URL product IDs → path traversal; `X-Forwarded-For` processed → injection; checkout `discount_code` parameter → business logic; search `sort` parameter → SQL injection candidate

Output: Prioritized test plan with `BulkDelete` access control bypass as P0, SQL injection in `sort` parameter as P1, `X-Forwarded-For` injection as P2.

---

**Scenario: Security review of an internal HR application source code**

Trigger: "Can you review our internal HR application for security issues? Here's the repo."

Process:
1. Grep route definitions in `routes.py` and `urls.py` — identifies 84 endpoints including `/api/admin/export-all-employees` not referenced in the frontend
2. Search for all form inputs and API parameters; identify `manager_id` parameter that accepts arbitrary integers and appears in a raw string format SQL query
3. Check `requirements.txt` for outdated dependencies; find `django==2.2.0` (end-of-life, multiple known CVEs)
4. Grep HTTP header processing: `X-Employee-Level` header used in authorization logic without validation
5. Search for commented-out code: finds `# TODO: add auth check` comment above three API endpoints
6. Map: direct SQL injection in `manager_id`, missing authentication on three endpoints, authorization bypass via `X-Employee-Level` spoofing, Django version vulnerabilities

Output: Written security assessment with four critical/high findings and remediation guidance.

---

**Scenario: Bug bounty reconnaissance on a SaaS product**

Trigger: "I want to map the attack surface of this SaaS product before I start testing — it's in my bug bounty scope."

Process:
1. Check scope definition — confirm allowed subdomains and excluded paths
2. Browse application across three privilege levels (unauthenticated, regular user, admin)
3. Run content discovery on each subdomain with a targeted wordlist inferred from observed naming patterns
4. Query `site:target.com` in Google; Wayback Machine reveals `/v1/api/` endpoints from 3 years ago — test whether they still respond
5. Search GitHub for developer names found in HTML comments — find a developer's Stack Overflow post containing a full database schema
6. Identify mobile `User-Agent` triggers a different code path with less aggressive rate limiting on the login endpoint

Output: Attack surface map covering 6 subdomains, 312 endpoints, 4 distinct user roles, legacy API still live, and login brute-force vector on mobile code path.

---

## References

- For the behavior-to-vulnerability matrix with deeper detail per vulnerability class, see [attack-surface-vulnerability-matrix.md](references/attack-surface-vulnerability-matrix.md)
- For technology fingerprinting indicators (file extensions, directory names, session token names, HTTP header signatures), see [technology-fingerprinting-reference.md](references/technology-fingerprinting-reference.md)
- For wordlist generation strategies and inference-based naming approaches, see [content-discovery-strategies.md](references/content-discovery-strategies.md)
- For HTTP response code interpretation during brute-force enumeration, see [response-code-interpretation.md](references/response-code-interpretation.md)
