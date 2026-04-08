---
name: web-application-hardening-assessment
description: |
  Systematically assess a web application's defensive security posture across input validation, information disclosure, application architecture, and server configuration. Use this skill whenever: evaluating the quality of an application's input handling strategy and whether it correctly applies whitelist vs blacklist vs sanitization approaches; assessing whether boundary validation is implemented at each trust boundary (not only the perimeter); checking whether multistep validation and canonicalization ordering are implemented safely; auditing error handling to determine whether verbose error messages, stack traces, debug output, or database banners are exposed to clients; assessing whether server and service banners are suppressed and whether HTML source comments have been removed; evaluating tiered application architecture for trust-boundary segregation weaknesses, dangerous inter-tier trust relationships, and least-privilege violations; assessing shared hosting or cloud environments for customer isolation deficiencies; auditing application server configuration for default credentials, default content, directory listing exposure, dangerous HTTP methods (WebDAV PUT/DELETE), misconfigured proxy functionality, virtual hosting security gaps, and web application firewall effectiveness; performing a pre-deployment security hardening review; conducting a security architecture review or threat modeling session; reviewing a web application penetration test scope for defensive control gaps. Covers core defense mechanisms (Ch2), information leakage prevention (Ch15), architecture security (Ch17), and application server hardening (Ch18). Maps to CWE-20 (Improper Input Validation), CWE-209 (Information Exposure Through Error Message), CWE-16 (Configuration), CWE-284 (Improper Access Control), CWE-693 (Protection Mechanism Failure).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/web-application-hackers-handbook/skills/web-application-hardening-assessment
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [2, 15, 17, 18]
    pages: "53-72, 651-666, 683-703, 705-735"
tags: [input-validation, boundary-validation, canonicalization, error-handling, information-disclosure, application-architecture, tiered-architecture, shared-hosting, server-hardening, default-credentials, directory-listing, webdav, web-application-firewall, defense-in-depth, owasp, appsec, cwe-20, cwe-209, cwe-16]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application source code — input validation logic, error handlers, framework configuration files — primary for white-box review"
    - type: document
      description: "HTTP traffic captures, Burp Suite logs, server configuration files, architecture diagrams — primary for black-box and config audit modes"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Run inside a project codebase for white-box review, or with HTTP traffic logs and server config for black-box / configuration assessment. Authorized testing context required."
discovery:
  goal: "Assess the application's defensive posture across four domains — input validation strategy, information disclosure controls, application architecture security, and server hardening — and produce a structured findings report with severity, evidence, and countermeasures"
  tasks:
    - "Classify the application's input handling approach for each input type and assess its adequacy"
    - "Verify boundary validation is performed at each trust boundary, not only the perimeter"
    - "Test canonicalization ordering — ensure decode-before-validate is applied and no re-encoding after validation"
    - "Assess error handling for verbose messages, stack traces, debug output, and service banners"
    - "Audit server configuration for default credentials, default content, directory listings, dangerous methods, proxy misconfiguration, and virtual hosting gaps"
    - "Evaluate tiered architecture for trust-boundary weaknesses, inter-tier trust abuse risks, and shared hosting isolation"
    - "Assess web application firewall presence, effectiveness, and bypass susceptibility"
    - "Document all findings with CWE mapping, severity, and specific countermeasures"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-minded-developer", "security-architect", "devops-engineer"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, web proxies (Burp Suite or equivalent), server administration basics, and common vulnerability classes"
  triggers:
    - "Pre-deployment security hardening review of a web application"
    - "Penetration test scope includes defense mechanism quality assessment"
    - "Security architecture review or threat modeling session"
    - "Post-incident assessment to understand why existing defenses failed"
    - "Code review targeting input validation and error handling quality"
    - "Server configuration audit for a newly deployed or migrated application"
  not_for:
    - "Testing specific injection vulnerabilities (SQL injection, command injection) — use the injection assessment skill"
    - "Authentication mechanism testing — use the authentication security assessment skill"
    - "Access control and session management testing — use the dedicated skills for those domains"
    - "Client-side attack surface (XSS, CSRF) — use the client-side attack testing skill"
---

# Web Application Hardening Assessment

## When to Use

You have authorized access to a web application (source code, server configuration, HTTP traffic, or a combination) and need to assess the quality of its defensive security controls — not to find specific exploit payloads, but to evaluate whether the defenses themselves are sound.

This skill applies when:
- A security review requires evaluating input validation strategy, not just testing for a specific injection class
- Error handling is in scope — determining whether the application leaks internal state, stack traces, database structure, or service versions through error responses
- Architecture security is in question — tiered systems, shared hosting, cloud deployments where tier segregation and trust boundaries need assessment
- Application server hardening is required — default credentials, default content, directory listings, WebDAV, proxy behavior, virtual hosting, and web application firewall (WAF) effectiveness

**The foundational insight from Stuttard and Pinto:** Virtually all web applications use the same categories of defense mechanisms. The security difference between applications is not which mechanisms are present, but how well they are implemented. Assessing defensive quality requires understanding what the correct implementation looks like and systematically testing against that standard — not waiting to discover exploitable output.

**Four assessment domains, each targeting a different layer of defense:**
1. **Input handling strategy** — Is the correct approach being applied to each input type? Is boundary validation in place at every trust crossing?
2. **Information disclosure** — What does the application reveal about its internals through errors, headers, comments, and published data?
3. **Application architecture security** — Do tier boundaries enforce their own controls, or do they trust other tiers blindly?
4. **Application server hardening** — Has the server platform been hardened against its default configuration weaknesses?

**Authorized testing only.** This skill is for security professionals with explicit written authorization to assess the target application and server.

---

## Context and Input Gathering

### Required Context (must have — ask if missing)

- **Assessment scope (which domains are in scope):**
  Why: the four domains are largely independent; time-limited engagements may need to prioritize. Input validation and error handling are highest-value in most web app assessments.
  - Check prompt for: "input validation," "error handling," "server config," "architecture review," "full hardening"
  - If missing, ask: "Is this a full hardening assessment across all four domains, or are specific areas prioritized? Do you have access to server configuration and application source?"

- **Testing mode (black-box / white-box / configuration audit):**
  Why: white-box analysis of source code enables detection of input handling class (whitelist vs blacklist) directly. Black-box testing relies on behavioral response analysis. Server configuration audit requires direct access to httpd.conf, web.xml, IIS config, or equivalent.
  - Check environment for: source code files, server config files, HTTP traffic captures
  - If missing, ask: "Do you have access to the application's source code, server configuration files, or only external HTTP access?"

- **Application tier topology (for architecture domain):**
  Why: detecting inter-tier trust abuse requires knowing whether components run on separate hosts, whether a shared database exists, and whether shared hosting or cloud infrastructure is involved.
  - Check environment for: architecture diagrams, deployment scripts, Docker Compose or Kubernetes manifests, hosting provider references
  - If missing, ask: "Does the application use a multi-tier architecture (separate app server and database)? Is it deployed on shared hosting or a cloud platform?"

### Observable Context (gather from environment)

- **Server response headers:**
  Look for: `Server:`, `X-Powered-By:`, `X-AspNet-Version:`, `X-Generator:` headers that reveal technology stack and version; presence of `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`
  If unavailable: note that header analysis requires HTTP access

- **Error responses:**
  Look for: HTTP 500 responses, SQL error text in responses, stack trace output, debug console output embedded in HTML
  If unavailable: proceed with source code analysis of exception handling logic

- **Configuration files:**
  Look for: `web.config`, `httpd.conf`, `nginx.conf`, `web.xml`, `php.ini`, `.htaccess`, `appsettings.json`
  If unavailable: defer to behavioral testing for configuration weaknesses

### Default Assumptions

- Assume **no server hardening has been performed** unless there is direct evidence otherwise — most default server configurations are insecure
- Assume **all input handling is perimeter-only** until boundary validation at each trust crossing is confirmed
- Assume **verbose error messages are enabled** in any environment that has not been explicitly hardened

---

## Process

### Step 1: Classify the Input Handling Strategy for Each Input Type

**ACTION:** For each category of user-supplied input the application processes, determine which of the five input handling approaches is being applied. The five approaches are:

1. **Reject Known Bad (blacklist)** — blocks a list of known-malicious strings or patterns; allows everything else
2. **Accept Known Good (whitelist)** — defines the set of permitted characters, length, format; blocks everything else
3. **Sanitization** — transforms input to a safe form (HTML encoding, escaping metacharacters) before use
4. **Safe Data Handling** — uses inherently safe processing APIs that eliminate the vulnerability class (parameterized queries for SQL, subprocess arrays for OS commands)
5. **Semantic Checks** — validates business logic authorization (does the submitted account ID belong to the authenticated user?)

**WHY:** The choice of approach has a direct bearing on how easily the defense can be bypassed. Blacklists are systematically bypassable through encoding, case variation, comment insertion, and null byte injection — a blacklist of `SELECT` can be bypassed with `SeLeCt`, `SELECT/**/`, or `%00SELECT`. Whitelisting is the strongest defense where feasible. Safe data handling (parameterized queries) eliminates entire vulnerability classes regardless of input content. Understanding which approach is in use for each input type reveals which inputs are inadequately defended and why.

**AGENT: EXECUTES** — Grep source code for input validation logic, regex patterns, filtering functions, and database query construction. Identify the approach applied to each input category.

**For each identified input category, document:**
- Input type (query parameter, form field, cookie, HTTP header, JSON body field)
- Approach currently applied (1-5 from above)
- Adequacy assessment: Is this the right approach for this input type?
- Bypass risk: If approach 1 (blacklist), it is always rated at least Medium risk without compensating controls

**Red flags:**
- SQL queries built by string concatenation rather than parameterized query APIs
- HTML output produced by string interpolation of user data without encoding
- File paths constructed by appending user input to a base directory without canonicalization
- `exec()`, `system()`, `shell_exec()`, `subprocess.call(shell=True)` receiving user-controlled values
- Any validation logic using `replace()` on attack strings (stripping, not blocking) rather than rejection

---

### Step 2: Verify Boundary Validation at Each Trust Boundary

**ACTION:** Map all trust boundaries in the application — points where data crosses from one component to another where the receiving component applies different security assumptions. Common trust boundaries: browser-to-server, server-to-database, server-to-SOAP/REST back-end service, server-to-OS command execution, server-to-email sending (SMTP), server-to-LDAP, server-to-cache layer. For each boundary, verify that input validation appropriate to the receiving component's vulnerabilities is applied at that boundary.

**WHY:** The simple picture of input validation — clean at the perimeter, trust internally — is fundamentally inadequate. Consider a login flow: the application receives the username, validates basic character set (step 1), performs a SQL query to check credentials (step 2), passes account data to a SOAP service to retrieve profile (step 3), renders the account page in HTML (step 4). Each step is a trust boundary. SQL injection defenses must be applied before step 2. XML metacharacter encoding must be applied before step 3. HTML encoding must be applied before step 4. Perimeter validation alone cannot protect all boundaries simultaneously, because conflicting encoding requirements make a single pass impossible: HTML-encoding prevents XSS but does not prevent SQL injection; SQL escaping does not prevent SMTP header injection.

**AGENT: EXECUTES** — Trace the data flow of key user inputs through the application. For each processing stage, verify that the appropriate validation or encoding for the receiving component is applied immediately before that component receives the data.

**Boundary-specific validation requirements to check:**
| Boundary | Required Defense |
|---|---|
| Server → SQL database | Parameterized queries or stored procedures (not escaping alone) |
| Server → HTML output | HTML entity encoding of all user data in output |
| Server → SOAP/XML service | XML metacharacter encoding of user data before XML construction |
| Server → OS command | Avoid passing user data to OS commands; if unavoidable, use exec array form, not shell string |
| Server → email (SMTP) | Strip or reject CR/LF in any field used in SMTP headers |
| Server → file system path | Canonicalize path, validate against allowed base directory, reject traversal sequences |
| Server → LDAP | Escape LDAP special characters; prefer LDAP API calls over raw filter construction |

**Finding:** Any trust boundary where validation appropriate to the receiving component is absent or insufficient constitutes a boundary validation gap.

---

### Step 3: Assess Multistep Validation and Canonicalization Ordering

**ACTION:** Identify all input validation logic that performs multiple sequential operations on user input (for example: strip `<script>`, then strip `javascript:`, then output). Also identify all points where the application decodes or canonicalizes user input. Verify that the ordering rule is satisfied: **decode/canonicalize first, then validate, never re-encode after validation**.

Test for these specific failure patterns:
- **Stripping without recursive application:** if `<script>` is stripped once, the input `<scr<script>ipt>` will produce `<script>` after one pass
- **Sequential traversal sequence removal:** removing `../` then `..\` — the input `..../` after first pass becomes `../`, bypassing the second check
- **Validation before canonicalization:** blocking `%27` (URL-encoded apostrophe) at the application but then URL-decoding the value before passing it to the database — the decoded `'` reaches the database

**WHY:** Multistep validation introduces ordering dependencies that attackers can exploit. An application that strips a blocked expression once can be fed a nested version that reconstitutes itself after stripping. An application that applies filters before canonicalization can be fed encoded versions of blocked characters. The safe ordering is: perform all decoding and canonicalization first, so that validation sees the final processed form of the input, not an intermediate form that subsequent processing will transform further.

**AGENT: EXECUTES** — Read input validation functions for iterative or sequential sanitization logic. Check whether canonicalization (URL decoding, HTML decoding, Unicode normalization) is applied before or after filter checks.

**Test with (black-box):**
- Nested blocked strings: `<scr<script>ipt>alert(1)</scr</script>ipt>` (tests non-recursive stripping)
- Double URL-encoded characters: `%2527` → after first URL decode → `%27` → after second → `'` (tests validate-before-decode ordering)
- Mixed encoding bypasses: `%3cscript%3e` for `<script>` where only literal form is blocked

---

### Step 4: Assess Error Handling and Information Disclosure via Error Messages

**ACTION:** Systematically probe the application to trigger error conditions and analyze what information is returned. For each functional area, submit: values of the wrong type, values of unexpected length, missing required parameters, values that reference nonexistent resources, and known attack strings for the technologies in use (SQL single-quote for database errors, `../../` for path traversal, `${7*7}` for template injection).

For each error response, check for disclosure of:
- Stack traces with class names, method names, line numbers, and file paths
- Database error messages containing SQL state codes, query fragments, or table/column names
- Internal hostnames, IP addresses, or connection strings visible in error output
- Session token values or other security-sensitive data in debug messages
- Framework or platform version banners embedded in error pages
- Custom debug messages left from development (session variable dumps, environment variable listings)

**WHY:** Verbose error messages give an attacker a detailed map of the application's internals at no cost. A stack trace identifies the exact framework version (enabling known-CVE attacks), the database technology (enabling SQL injection tuning), the file system layout (enabling path traversal), and which component generated the error (enabling targeted exploitation). A database error message containing the partial SQL query allows an attacker to reconstruct the full query and craft a precise injection. This information gathering step is a standard part of every targeted attack, not a vulnerability in isolation — but it dramatically accelerates every other attack that follows.

**AGENT: EXECUTES** (response analysis and source code review of exception handling) — HANDOFF TO HUMAN for interactive error triggering via proxy.

**In source code, look for:**
- Unhandled exceptions that propagate to the framework's default error page
- Catch blocks that log and rethrow exceptions to the HTTP response
- Debug-mode flags still enabled in production configuration (`DEBUG=True`, `customErrors mode="Off"`, `display_errors=On`)
- `phpinfo()` pages or equivalent diagnostic endpoints left accessible

**Scan raw HTTP responses for error keywords:** `error`, `exception`, `illegal`, `invalid`, `fail`, `stack`, `access`, `directory`, `file`, `not found`, `varchar`, `ODBC`, `SQL`, `SELECT` — matches in responses that are not expected to contain these words indicate information disclosure.

---

### Step 5: Assess Information Disclosure in Published Content and Headers

**ACTION:** Examine the following disclosure surfaces in the live application:

**HTTP response headers:**
- `Server:` header — reveals web server product and version
- `X-Powered-By:` — reveals framework, language, version
- `X-AspNet-Version:`, `X-Generator:`, `X-Runtime:` — framework specifics
- Record all technology disclosures; map each to known CVEs for the disclosed version

**HTML source of all application pages:**
- Developer comments containing: URL paths, database structure hints, TODO/FIXME notes, commented-out code, internal hostnames, or user credential references
- Hidden form fields that carry internal values (user IDs, privilege flags, session state) visible to the client

**Sensitive data published to authorized users:**
- Credit card numbers in full (should be truncated to last 4 digits)
- Password fields pre-populated with existing password (reveals password to anyone with access to the user's session)
- User role and privilege data that is more detailed than necessary
- Account enumeration through user profile pages or search results

**WHY:** Server banners enable automated and manual fingerprinting of the exact product version, directly mapping to the CVE database. Developers frequently leave HTML comments containing information gathered during development — database schema notes, access control bypass hints, environment variable names, or even temporary hardcoded credentials. Pre-populating password fields means the existing password is transmitted in cleartext to the browser on every page load, even if the user never interacts with it — it is visible in the page source and in any browser extension or corporate proxy that logs traffic.

**AGENT: EXECUTES** — Read all page source files and response captures. Grep for comment markers (`<!--`, `//`, `#`), hidden input fields, and sensitive data patterns.

---

### Step 6: Assess Application Server Configuration — Default Credentials and Default Content

**ACTION:** Identify the web server and application server products in use (from banner analysis, file extensions, URL patterns, error pages). For each identified product:

**Default credentials:**
- Identify any administrative interfaces at non-standard ports (8080, 8443, 8888, 9090) or well-known admin paths (`/manager/`, `/admin/`, `/jmx-console/`, `/phpmyadmin/`)
- Test default credentials for the identified products (Apache Tomcat: `admin/(none)`, `tomcat/tomcat`, `root/root`; JBoss: JMX console unauthenticated by default; Oracle Application Server: PL/SQL gateway accessible without authentication)
- If default credentials do not work, attempt common weak credentials before concluding

**Default content:**
- Test for accessible debug and diagnostic pages: `phpinfo.php`, `/test/jsp/dump.jsp` (Jetty), Tomcat Sessions Example servlet, JBoss JMX console
- Test for sample applications shipped with the server: these frequently contain exploitable vulnerabilities or provide information useful to attackers
- Use tools such as Nikto to identify remaining default content

**WHY:** Default credentials are the most commonly exploited configuration weakness in application server deployments. Many servers ship with known-credential administrative interfaces that are never changed during installation. The Apache Tomcat manager application at `/manager/html` with credentials `tomcat/tomcat` allows arbitrary WAR file deployment — an attacker who finds this can upload a backdoor and achieve remote code execution in minutes. JBoss JMX console is accessible without authentication by default and provides the same capability. Default content (phpinfo, sample servlets) provides attackers with precise version information, installed module lists, and runtime configuration — the exact intelligence needed to select exploits.

**AGENT: EXECUTES** (technology fingerprinting from source and config) — HANDOFF TO HUMAN (credential testing, Nikto scan, port scan for admin interfaces).

**Assessment checklist for this step:**
- [ ] All default credentials changed or accounts disabled
- [ ] Administrative interfaces not publicly accessible (ACL or firewall on admin paths/ports)
- [ ] All default content removed or confirmed intentionally retained and hardened
- [ ] phpinfo.php, server-info, server-status, and equivalent diagnostic endpoints removed or access-controlled
- [ ] Sample applications and example servlets removed

---

### Step 7: Assess Application Server Configuration — Directory Listings, Dangerous HTTP Methods, and Proxy Behavior

**ACTION:**

**Directory listings:**
- For each directory path discovered during application mapping, issue a GET request to the directory URL (without a filename). If the server returns a directory index instead of an error or default document, this is a directory listing finding.
- Check whether any listed directories expose sensitive content: log files, backup files, old script versions, configuration files, or documents not intended for public access.

**Dangerous HTTP methods:**
- Issue an `OPTIONS` request to the application root and to each subdirectory. Record all advertised methods.
- Methods of concern: `PUT` (file upload), `DELETE` (file deletion), `COPY`, `MOVE`, `SEARCH`, `PROPFIND`, `TRACE`, `CONNECT`
- Attempt to use the `PUT` method against a writable directory: `PUT /test.txt HTTP/1.1` with a test payload. If a `201 Created` response is returned, arbitrary file upload is possible — test whether executable scripts can be uploaded directly or via `PUT` followed by `MOVE` to a script extension.
- Test `TRACE` method: if it reflects request headers back (including `Cookie` and `Authorization`), this enables cross-site tracing attacks in some browser configurations.

**Proxy behavior:**
- Issue a GET request containing a full URL with a foreign hostname: `GET http://external-host.example.com/ HTTP/1.0`. If the server returns content from the external host, it is configured as a forward proxy — an attacker can use it to attack third-party systems, reach internal hosts not directly accessible from the Internet, or bypass firewall rules.
- Issue a `CONNECT` request: `CONNECT external-host.example.com:443 HTTP/1.0`. If the server returns `200 Connection established`, it is proxying arbitrary TCP connections.

**WHY:** Directory listings reveal the complete file inventory of server directories, allowing attackers to discover files that depend on obscurity for access control — log files, backup copies of scripts, old versions of files, and configuration files containing credentials. Directory listings are the most common path to discovering sensitive content that has no access control at all. Dangerous HTTP methods (particularly `PUT`) allow an attacker to upload backdoor scripts into the web root and execute arbitrary code with the server process's privileges. A misconfigured open proxy allows an attacker to use the target server as a launch platform for attacks against internal infrastructure.

**AGENT: EXECUTES** (configuration analysis) — HANDOFF TO HUMAN (OPTIONS requests, PUT test, proxy test via proxy tool).

**Assessment checklist for this step:**
- [ ] Directory listings disabled server-wide (Apache: `Options -Indexes`; IIS: disable directory browsing; Nginx: `autoindex off`)
- [ ] Each directory contains a default document (`index.html`) as a fallback
- [ ] Only `GET` and `POST` enabled for application directories; all other methods explicitly disabled
- [ ] Server is not configured as an open forward proxy
- [ ] `TRACE` method disabled

---

### Step 8: Assess Misconfigured Virtual Hosting

**ACTION:** If the server hosts multiple virtual hosts (confirmed by DNS, server banner, or configuration review), test whether security hardening applied to named virtual hosts also applies to the default (unnamed) host:

1. Issue a GET request to the root with the expected `Host:` header — record the response
2. Issue the same GET request with an arbitrary `Host:` header value (e.g., `Host: attacker.example.com`)
3. Issue the same GET request with the server's IP address in the `Host:` header
4. Issue the same GET request with no `Host:` header

Compare responses. Differences in content, status codes, or directory listing behavior indicate that the default virtual host is handled differently — potentially bypassing hardening that was applied only to named virtual hosts.

**WHY:** A common configuration error in virtual hosting is to apply security hardening (access controls, authentication requirements, directory listing suppression) only to the named virtual host containers, not to the default host. When a request arrives with an IP address in the `Host:` header or with no `Host:` header, it is handled by the default host configuration — which may have no hardening applied. This allows an attacker to access content or functionality that is supposedly protected by bypassing the Host-based routing.

**AGENT: EXECUTES** (configuration analysis) — HANDOFF TO HUMAN (Host header manipulation via proxy).

---

### Step 9: Assess Application Architecture Security — Tiered Architecture Trust Boundaries

**ACTION:** For multi-tier architectures, assess the inter-tier trust model:

**Identify the trust model in use:**
- Does the application tier perform all access control checks, with the database tier trusting all commands from the application tier?
- Does the database use a single high-privilege account for all operations, or role-based accounts aligned to user privilege levels?
- Do application components run as OS accounts with more privilege than strictly required for their function?

**Assess tier segregation:**
- Can the application tier directly read or write the database's physical data files (LAMP architecture vulnerability: MySQL data stored as readable files, accessible via path traversal in the application tier)?
- Are application tier components co-located on the same physical host as the data tier? (Compromise of any tier on a co-located host = compromise of all tiers)
- Are network-level controls in place to restrict which ports and protocols the application tier can use to reach the data tier?

**Assess least-privilege implementation:**
- Application server tier: runs as a dedicated low-privilege OS account (not `root`, not `SYSTEM`, not `nobody` shared with other applications)
- Database tier: application uses separate accounts for read-only operations (anonymous user queries), authenticated user operations, and administrative operations — each with only the access required
- Sensitive data (credentials, payment card data) stored encrypted in the database even if the application tier is compromised

**WHY:** The most dangerous architectural weakness is the implicit trust relationship where the database tier honors all commands from the application tier as if they were legitimate. When a SQL injection flaw exists, the attacker does not need to crack database credentials — they directly control the database through the high-privilege application account. An attacker who exploits a file disclosure vulnerability on a co-located LAMP stack can read MySQL's raw data files directly from the filesystem, bypassing all database-level access controls entirely. Least-privilege containment means a successful attack against one tier does not automatically give full access to all tiers.

**AGENT: EXECUTES** — Grep configuration files for database connection strings, database user names, privilege grants. Review deployment architecture for co-location and shared accounts.

---

### Step 10: Assess Shared Hosting and Application Service Provider Security

**ACTION:** For applications deployed on shared hosting or Application Service Provider infrastructure, assess:

**Customer isolation:**
- Can the current customer's application code access the filesystem paths of other customers' applications? (Test by attempting to read paths one level above the current application's web root)
- Does the database access model use a shared database instance with per-customer tables, or fully isolated database instances? (Shared instances with deficient access control allow cross-customer data access)
- Does the operating system account used by the application have permissions restricted to the application's own file paths?

**Shared management infrastructure:**
- Identify how customers administer their hosted applications (FTP, SFTP, web-based admin panel, VPN)
- Is the administration protocol encrypted? (FTP transmits credentials in cleartext)
- Does the management interface have its own security vulnerabilities that could allow one customer to interfere with another's application or data?

**Deliberate and unintentional cross-application attacks:**
- If the application executes customer-supplied code (customizations, plugins, scripts), verify that execution occurs in a sandboxed context with restricted OS privileges and no network access to other customers' resources
- Verify that database stored procedures shared across customers run with definer privileges that cannot be leveraged to access other customers' data

**WHY:** Shared hosting multiplies the blast radius of any single vulnerability. A command injection flaw in one customer's application can expose the data of every other customer hosted on the same server — the attacking code runs with the web server process's credentials, which typically have read access to all other customers' web roots. A SQL injection against a shared database can access all tables in the database regardless of which customer's tables they belong to. The 2011 wave of mass defacements targeted shared hosting environments specifically because a single exploit gives access to hundreds of sites simultaneously.

**AGENT: EXECUTES** (configuration and filesystem permission analysis) — HANDOFF TO HUMAN (cross-customer isolation testing requires dedicated test accounts in the shared environment).

---

### Step 11: Assess Web Application Firewall Effectiveness and Bypass Susceptibility

**ACTION:** Determine whether a web application firewall (WAF) or intrusion detection system (IDS) is present. If present, assess its effectiveness boundaries and susceptibility to bypass.

**Detect WAF presence:**
- Submit a GET request with an obvious attack payload in a parameter that the application reflects in the response (e.g., `?foo=<script>alert(1)</script>`). If the application blocks the request with a generic error page or returns a WAF-specific response, an external defense is likely present.
- Look for WAF-specific response headers or cookies (e.g., `X-CDN:`, specific Set-Cookie names associated with commercial WAF products)

**Assess effectiveness boundaries:**
WAFs effectively block:
- Known attack signatures submitted in obvious locations (URL parameters in GET requests)
- Standard, well-known attack payloads (`/etc/passwd`, `<script>alert(1)`, `' OR 1=1--`)

WAFs do not protect against:
- Business logic flaws, access control weaknesses, and authentication vulnerabilities (no signature possible)
- DOM-based XSS (processed entirely client-side, never passes through the WAF)
- Attacks submitted through unconventional input channels (HTTP headers, cookies, JSON body fields, multipart form fields)
- Custom application-specific attack vectors with no matching signature

**Test bypass techniques (document, do not exploit):**
- Submit the same payload through an unprotected input channel (cookie instead of query parameter, POST body instead of GET)
- Submit the payload in a non-standard encoding: double URL-encoding, HTML entity encoding, Unicode alternative representations
- Concatenate the attack string across multiple parameters (HTTP Parameter Pollution on ASP.NET: `?id=SELECT&id=*+FROM+users` → server-side concatenation reconstructs the attack)
- Use benign-looking payloads that avoid common signatures: `/var/log/syslog` instead of `/etc/passwd`, `prompt('xss')` instead of `alert('xss')`

**WHY:** A WAF can stop commodity automated attacks and slow down less-skilled attackers, but it creates a false sense of security if the organization believes it substitutes for fixing underlying vulnerabilities. Every WAF deployed has a boundary — the effective defense is the intersection of the WAF's signature coverage and the attacker's payload awareness. A determined attacker familiar with WAF bypass techniques will circumvent generic rules. The WAF does not reduce the severity of the underlying vulnerability; it only increases the cost of exploitation for certain attack classes.

**AGENT: EXECUTES** (response analysis, header review) — HANDOFF TO HUMAN (WAF bypass testing via proxy).

---

### Step 12: Document Findings and Produce the Hardening Assessment Report

**ACTION:** For each confirmed weakness, write a structured finding entry. Produce the full assessment report using the output template.

**WHY:** Findings without countermeasures leave remediation ambiguous — developers cannot prioritize or plan remediations without understanding what specific change addresses each finding. Linking findings to CWE identifiers enables cross-referencing with OWASP testing guides, NIST guidelines, and vendor security advisories, and allows tracking against industry-standard frameworks.

**AGENT: EXECUTES** — Writes the assessment report to a file.

---

## Inputs

- Application source code — input validation logic, error handlers, framework and server configuration files (white-box mode)
- HTTP proxy session / Burp Suite project file with application responses including error pages (black-box mode)
- Server configuration files: `httpd.conf`, `nginx.conf`, `web.xml`, `web.config`, `.htaccess`, `php.ini`
- Application architecture documentation: deployment diagrams, infrastructure topology, database access model
- List of technologies in use (web server product, application framework, database, hosted environment)
- Scope confirmation from the authorizing party

## Outputs

**Web Application Hardening Assessment Report** containing:

```
# Web Application Hardening Assessment — [Application Name]
Date: [date]
Assessor: [name/team]
Mode: [black-box | white-box | hybrid | config-audit]
Scope: [domains assessed]

## Executive Summary
[2-3 sentences: overall posture, highest-severity finding category, recommended priority]

## Domain 1: Input Handling Strategy
### [H-001] [Finding name]
- CWE: CWE-XX
- Severity: [Critical | High | Medium | Low]
- Input type/location: [specific parameter or code location]
- Current approach: [Blacklist | No validation | Sanitization with gap | ...]
- Evidence: [code snippet or HTTP request/response]
- Countermeasure: [specific remediation]

## Domain 2: Information Disclosure
[Findings in same format]

## Domain 3: Application Architecture Security
[Findings in same format]

## Domain 4: Application Server Hardening
[Findings in same format]

## Countermeasure Priority Matrix
[Table: Finding ID | Domain | Severity | Effort | Priority]

## Coverage Summary
[Table: Domain | Steps Completed | Findings Count | Highest Severity]
```

---

## Key Principles

- **Blacklists are systematically bypassable — document as at-least-Medium risk without compensating controls.** Case variation (`SeLeCt`), comment insertion (`SELECT/**/`), double encoding (`%2527`), and null byte injection (`%00`) all defeat naive keyword filtering. A blacklist may catch automated scanners but will not stop a targeted attacker. Use this as a finding, not merely an observation.

- **Perimeter validation is necessary but insufficient.** A single validation step at the input boundary cannot simultaneously satisfy the encoding requirements of SQL, HTML, XML, OS commands, and LDAP. Boundary validation at each trust crossing allows each component to enforce its own protection requirements without conflicting with others. Absence of boundary validation is a structural weakness, not a one-off finding.

- **Decode before validate — never validate before decode.** The correct canonicalization ordering is: receive input, apply all expected decoding, then apply validation logic. An application that blocks `%27` but processes it through a second URL decode will silently pass the apostrophe to the database. This is the root cause of the majority of encoding bypass vulnerabilities.

- **Error messages are an attacker's reconnaissance tool.** Stack traces, database error text, and service banners accelerate every other attack: they reveal the exact technology stack, the database schema, the file layout, and the framework version. Suppressing error messages does not fix the underlying vulnerability — it raises the cost of finding and exploiting it.

- **Architecture security determines blast radius.** A SQL injection in an application using a DBA-privilege database account is a full database compromise. The same SQL injection in an application using a read-only account against non-sensitive tables may be a low-severity finding. The architectural countermeasures (least-privilege database accounts, tier segregation, encrypted data at rest) determine what a successful attack against one vulnerability can actually achieve.

- **Default server configurations are insecure by design — hardening is always a deliberate act.** Servers ship with defaults optimized for ease of use: default credentials, sample applications, directory listings enabled, all HTTP methods active, verbose errors. A server that has not been explicitly hardened retains all of these. Assessing hardening requires verifying that each default has been deliberately addressed, not merely that the application seems to function correctly.

- **WAFs are a supplement, not a substitute, for fixing vulnerabilities.** A WAF correctly deployed stops commodity attacks and provides detection coverage. It does not protect business logic, DOM-based attacks, or any vulnerability class for which no generic signature exists. The presence of a WAF should not reduce the severity rating of underlying findings — it should reduce the likelihood of exploitation, which affects risk prioritization, not the severity of the control gap.

---

## Examples

**Scenario: Pre-deployment hardening review of a financial services portal**
Trigger: "Before we go live next month, we need a security review of the server configuration and input handling across the application."
Process:
1. Step 1 (input handling classification): Review database query construction — 3 of 12 query-building functions use string concatenation with user parameters rather than parameterized queries. Classified as Approach 1 (Reject Known Bad) in two cases (blacklisting single-quote) and no validation in the third. Findings: 2 High (blacklist-only SQL), 1 Critical (no validation on admin query).
2. Step 2 (boundary validation): Trace username from login form through: (a) HTML login page rendering — username HTML-encoded before output, compliant; (b) SQL query for credential check — parameterized, compliant; (c) SOAP service call for profile data — username interpolated directly into XML payload, no XML metacharacter encoding, finding: XML injection risk at SOAP boundary.
3. Step 4 (error handling): Trigger a database error by submitting a type-mismatch value. Response contains full stack trace including Oracle JDBC connection string with hostname and credentials: `jdbc:oracle:thin:apps/appspassword@db-prod-01.internal:1521/PROD`. Critical finding: credential disclosure in error message.
4. Step 6 (server config): Apache Tomcat detected. Access `/manager/html` — returns 401 with authentication prompt. Test credentials `tomcat/tomcat` — authentication succeeds. WAR file deployment interface accessible with default credentials. Critical finding.
5. Step 7 (directory listings): 4 of 11 directories return Apache directory indexes. One exposed directory contains `backup_2023-11-01.sql.gz` — database backup file downloadable without authentication.
Output: 2 Critical, 4 High, 3 Medium findings across all four domains.

---

**Scenario: Architecture security review of a multi-tenant SaaS application**
Trigger: "We host multiple enterprise clients on the same platform. A security consultant flagged concerns about tenant isolation. Can you do a full architecture review?"
Process:
1. Step 9 (tiered architecture): Review database connection configuration — a single database account `app_user` with GRANT ALL PRIVILEGES is used for all operations. All tenants' data in the same schema with tenant_id discrimination in queries. SQL injection in any query can access any tenant's data. Finding: High — insufficient database-level tenant isolation.
2. Step 10 (shared hosting): Review OS account configuration — all tenant application containers run as `www-data`. Path traversal in any tenant application could read other tenants' uploaded files, which are all accessible to `www-data`. Finding: High — insufficient OS-level filesystem isolation.
3. Step 11 (WAF): WAF is present (detected via custom cookie `X-WAF-Token`). Test: submitting `' OR 1=1--` in query string is blocked. Same payload in JSON POST body passes through. Finding: Medium — WAF does not inspect JSON request bodies.
4. Step 2 (boundary validation): Multi-tenant SOAP endpoint receives tenant-supplied data that is interpolated into XML without encoding. One tenant could inject XML to interfere with another tenant's SOAP requests.
Output: Architecture recommendations include separate database accounts per tenant with row-level security, per-tenant OS accounts with restricted filesystem access, and WAF configuration update for JSON body inspection.

---

**Scenario: Error handling and information disclosure audit of an e-commerce application**
Trigger: "We're getting strange error pages appearing on our site during our pen test engagement. Can you review our error handling posture?"
Process:
1. Step 4 (error handling): Systematically inject type-mismatch values into each parameter category. Three findings: (a) product ID parameter returns Oracle SQL state and partial query text on invalid input; (b) order search by date returns ASP.NET stack trace revealing .NET version 4.5.2 and full file path; (c) admin user endpoint triggers custom debug message dumping session variables including `SessionKey` value.
2. Step 5 (header/comment disclosure): Server header reveals `Microsoft-IIS/8.5`. HTML source of checkout page contains commented-out block: `<!-- TODO: remove test card 4111111111111111 / 12/25 / 456 before launch -->`. Finding: test payment card data embedded in production HTML comment.
3. Countermeasures: Configure `customErrors mode="On"` in `web.config` with generic error page redirect; suppress `Server:` header via URLScan/IIS Lockdown; remove all HTML comments from production deployment pipeline.
Output: 5 information disclosure findings (1 Critical for session key exposure, 2 High for stack trace + SQL error, 2 Medium for version banners and payment card in comment).

---

## References

- For input validation countermeasure implementation details, see [input-validation-countermeasures.md](references/input-validation-countermeasures.md)
- For server hardening checklists per platform (Apache, IIS, Tomcat, Nginx), see [server-hardening-checklists.md](references/server-hardening-checklists.md)
- For architecture security countermeasures (tier segregation, least-privilege, defense-in-depth), see [architecture-security-countermeasures.md](references/architecture-security-countermeasures.md)
- Source: Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook* (2nd ed.), Chapters 2, 15, 17, 18, pp. 53-72, 615-630, 647-666, 669-699. Wiley.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws by Dafydd Stuttard, Marcus Pinto.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
