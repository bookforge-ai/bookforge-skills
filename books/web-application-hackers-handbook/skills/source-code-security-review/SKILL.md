---
name: source-code-security-review
description: |
  Perform a systematic white-box security review of web application source code to find exploitable vulnerabilities. Use this skill when: you have authorized access to an application's source code and need to identify security flaws faster or more thoroughly than black-box testing alone; auditing a codebase prior to launch or after a security incident; reviewing open-source or purchased software for embedded vulnerabilities; complementing an active penetration test with source-level analysis. Applies a three-phase methodology: (1) identify all user-input entry points via platform-specific source APIs — Java HttpServletRequest, ASP.NET Request.Params/Form/QueryString, PHP $_GET/$_POST/$_COOKIE/$_REQUEST, Perl CGI param(), JavaScript document.location/URL; (2) trace data flow forward to dangerous sink APIs — Runtime.exec()/Process.Start() for OS command injection, Statement.execute()/mysql_query() for SQL injection, FileInputStream/include() for path traversal, sendRedirect()/header() for open redirect, eval() for script injection; (3) line-by-line close review of authentication, session management, access control, and native code components. Covers 8 vulnerability signature categories: cross-site scripting, SQL injection, path traversal, arbitrary redirection, OS command injection, backdoor passwords, native software bugs (buffer overflow, integer flaw, format string), and incriminating source code comments. Also covers database code components (stored procedures with dynamic SQL) and environment configuration checks (web.xml, Web.config, php.ini). Produces a prioritized findings report with evidence and countermeasures. Maps to CWE-79 (XSS), CWE-89 (SQL Injection), CWE-22 (Path Traversal), CWE-601 (Open Redirect), CWE-78 (OS Command Injection), CWE-798 (Hardcoded Credentials), CWE-120/121/122 (Buffer Overflow), CWE-134 (Format String). For authorized security review engagements, appsec engineers, and security-minded developers.
version: 1
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [19]
    pages: "701-745"
tags: [code-review, white-box-testing, source-code-analysis, xss, sql-injection, path-traversal, open-redirect, command-injection, backdoor, buffer-overflow, java, aspnet, php, perl, javascript, penetration-testing, appsec, cwe-79, cwe-89, cwe-22, cwe-601, cwe-78, cwe-798, cwe-120, cwe-134]
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Web application source code — server-side handlers, data access layer, database stored procedures, configuration files (web.xml, Web.config, php.ini), client-side JavaScript"
    - type: document
      description: "Build manifests, dependency lists, architecture diagrams — optional but useful for scoping"
  tools-required: [Read, Grep]
  tools-optional: [Bash, Write]
  mcps-required: []
  environment: "Run directly against the source code repository. No live application required. Authorized review context required."
discovery:
  goal: "Identify exploitable security vulnerabilities in web application source code using a structured three-phase approach — entry points, dangerous sinks, and line-by-line review of high-risk components — and produce a prioritized findings report"
  tasks:
    - "Establish platform and establish custom wrapper awareness before proceeding"
    - "Map all user-input entry points using platform-specific source APIs"
    - "Trace data flow from sources to dangerous sink APIs for each vulnerability category"
    - "Perform line-by-line review of high-risk components: authentication, session management, access control, native code"
    - "Audit database stored procedures for dynamic SQL construction"
    - "Review environment configuration files for security-relevant settings"
    - "Document findings with CWE mapping, severity, evidence, and countermeasures"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-minded-developer"]
    experience: "intermediate-to-advanced — assumes familiarity with at least one server-side web platform (Java, .NET, PHP, Perl) and common web vulnerability classes"
  triggers:
    - "Penetration test engagement where source code access has been granted"
    - "Security audit of a web application prior to production deployment"
    - "Reviewing an open-source project or purchased component for embedded vulnerabilities"
    - "Root-cause analysis after a security incident — understanding how the vulnerability existed in code"
    - "Supplementing automated SAST tool output with manual verification"
  not_for:
    - "Black-box behavioral testing without source access — use the relevant black-box testing skills"
    - "Infrastructure or network security review — different scope"
    - "Mobile application source review — different platform APIs"
---

# Source Code Security Review

## When to Use

You have authorized access to a web application's source code and need to find security vulnerabilities systematically.

This skill applies when:
- A penetration test or security audit includes source code access, and you want to find more vulnerabilities faster than black-box alone
- You need to identify backdoor passwords, hardcoded credentials, or logic flaws that are invisible to behavioral testing
- A black-box test revealed anomalous behavior and you want to trace its root cause in code
- You are reviewing an open-source component before integrating it into production

**The foundational insight:** Black-box testing is powerful but incomplete. Automated fuzzing can send hundreds of test cases per minute, but it cannot identify a backdoor password that only activates for a specific hardcoded value, a condition-guarded XSS that only triggers when a secondary parameter equals `"3"`, or a buffer overflow buried in a native helper library. Source code review finds a different population of vulnerabilities than black-box testing. The two approaches are strongest when combined — code review guides where to probe interactively; interactive testing confirms whether code-level findings are actually exploitable.

**Before starting:** Establish the extent of any custom wrappers, library extensions, or application-specific abstractions around standard APIs. Applications may implement their own session storage, input sanitization utilities, or database access layers. Understanding these customizations is essential — a call to a custom `safeQuery()` wrapper may or may not prevent SQL injection depending on its implementation.

**Authorized review only.** This skill is for security professionals with explicit written authorization.

---

## Context and Input Gathering

### Required Context

- **Platform(s) in use (Java, ASP.NET, PHP, Perl, JavaScript, or mix):**
  Why: each platform has distinct source APIs for reading user input and distinct dangerous sink APIs. The Grep patterns and review focus differ entirely between a Java servlet application and a PHP script.
  - Check for: `pom.xml` / `build.gradle` (Java), `*.csproj` / `Web.config` (ASP.NET), `*.php` files, `*.pl` files, `package.json` (Node.js/JS)

- **Scope of review (full codebase, specific modules, authentication only):**
  Why: a large enterprise application may have hundreds of thousands of lines. Time-boxed reviews require prioritizing the highest-risk components. Without a defined scope, coverage is uneven.
  - If unspecified, start with authentication, session management, access control, and any component that processes user file access or external command execution

- **Any existing SAST tool output:**
  Why: avoids duplicating what automated analysis already found and focuses manual effort on classes of issues that tools reliably miss (logic flaws, race conditions, backdoors).

### Observable Context (gather from codebase)

- Platform-specific configuration files: `web.xml`, `Web.config`, `php.ini`, `.htaccess`
- Framework identification: Spring, Struts, Django, Laravel, Rails annotations and imports
- Database access layer: ORM vs raw SQL, presence of prepared statement APIs
- Custom security utilities: classes or functions named `sanitize`, `validate`, `encode`, `escape`, `filter`
- Native code integration: JNI calls, P/Invoke, C extension includes, `Runtime.exec` / `Process.Start`

---

## Process

### Phase 1 — Map User-Input Entry Points

**ACTION:** Grep the codebase for platform-specific source APIs. Every location where user-controlled data enters the application is a potential source of tainted data. Build a catalog of entry points before tracing data flows.

**WHY:** Vulnerabilities arise when user-controlled data reaches a dangerous operation without proper validation or encoding. You cannot trace data flow without first knowing all the places data enters. Applications frequently receive input through less-obvious channels — HTTP headers, cookies, session-derived data from user registration, even the URL path itself. Missing an entry point means missing all vulnerabilities that originate from it.

**AGENT: EXECUTES** — Grep for platform-specific source APIs:

**Java (HttpServletRequest / ServletRequest):**
```
getParameter|getParameterNames|getParameterValues|getParameterMap
getQueryString|getHeader|getHeaders|getHeaderNames
getRequestURI|getRequestURL|getCookies|getRequestedSessionId
getInputStream|getReader|getRemoteUser|getUserPrincipal
```

**ASP.NET (System.Web.HttpRequest):**
```
Request\.Params|Request\.Item|Request\.Form|Request\.QueryString
Request\.ServerVariables|Request\.Headers|Request\.Url|Request\.RawUrl
Request\.UrlReferrer|Request\.Cookies|Request\.BinaryRead
Request\.Browser|Request\.UserAgent|Request\.AcceptTypes
```

**PHP:**
```
\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SERVER
\$HTTP_GET_VARS|\$HTTP_POST_VARS|\$HTTP_COOKIE_VARS
\$GLOBALS
```
Note: if `register_globals` is enabled in `php.ini`, any variable name may receive request parameter values. Line-by-line review is then required to track all uses of uninitialized variables.

**Perl (CGI.pm):**
```
->param\(|->param_fetch\(|->Vars\b|->cookie\(|->raw_cookie\(
->query_string\b|->referer\b|->self_url\b|->url\b
ReadParse
```

**JavaScript (DOM sources):**
```
document\.location|document\.URL|document\.URLUnencoded|document\.referrer
window\.location|location\.search|location\.hash|location\.href
```

**NOTE:** Also search for `$GLOBALS` (PHP), any class names ending in `Request`, `HttpContext`, `HttpInput`, or equivalent — applications commonly abstract input access behind wrapper classes.

---

### Phase 2 — Trace Data Flow to Dangerous Sinks (Signature Scanning)

**ACTION:** For each vulnerability category below, grep for the dangerous sink APIs. For each hit, trace backward to determine whether user-controlled data from Phase 1 sources flows into that sink without adequate validation or encoding. Confirm or dismiss each candidate finding.

**WHY:** Signature scanning targets the highest-density locations of potential vulnerabilities first. A hard-coded SQL query fragment like `"SELECT` appearing in application code is almost always part of a SQL injection–vulnerable pattern. An `eval()` call receiving user input is almost always dangerous. This approach finds low-hanging fruit quickly, leaving remaining time for the subtler line-by-line review in Phase 3.

---

#### 2.1 — Cross-Site Scripting (XSS)

**Grep for output APIs that write user data to responses:**

**Java:** `response.getWriter().print|println|write`, `out.print|println`, `.InnerHtml`, `response.setHeader`

**ASP.NET:** `Response.Write|Response.Output.Write`, `\.InnerHtml\s*=`, `\.InnerText\s*=`

**PHP:** `echo\b|print\b|printf\b|vprintf\b`, `<?=`

**JavaScript (DOM sinks):**
```
document\.write\(|document\.writeln\(|\.innerHTML\s*=
eval\(|window\.execScript\(|window\.setInterval\(|window\.setTimeout\(
```

**Pattern to find:** User input from a Phase 1 source is incorporated into HTML output without HTML-encoding. Example:
```java
// Vulnerable: m_pageTitle set from request.getParameter("title") and
// later written into a <title> element without encoding
m_pageTitle = request.getParameter("title");
```
Trace `m_pageTitle` forward — if it is written to a response element or used to construct a link/HTML fragment without `HtmlEncode()` / `escapeHtml()` / `HtmlUtils.htmlEscape()`, this is a confirmed XSS.

**Grep for SQL fragment strings to find XSS in query-string construction:**
```
"SELECT |"INSERT |"DELETE |" WHERE |" AND |" OR |" ORDER BY
```
These patterns are case-insensitive; also search lowercase. The surrounding whitespace and quote distinguish SQL keyword strings from ordinary concatenated strings.

**NOTE on filter-based mitigations:** If a filter exists that blocks certain XSS payloads in the query string, trace it carefully. Filters applied to the wrong parameter, or applied before the vulnerable parameter is read, provide no protection.

---

#### 2.2 — SQL Injection

**Grep for raw SQL execution APIs:**

**Java:** `createStatement|Statement\.execute|Statement\.executeQuery|Statement\.executeUpdate`

**ASP.NET:** `SqlCommand|OleDbCommand|OdbcCommand|SqlDataAdapter|\.CommandText\s*=`

**PHP:** `mysql_query|mssql_query|pg_query|mysqli_query`

**Perl:** `->selectall_arrayref|->do\b`

For each hit, check whether the SQL string is constructed by concatenating user-controlled data. The presence of string fragments like `" WHERE ` + variable or `"SELECT * FROM ` + variable adjacent to a `createStatement` / `execute` call is a strong indicator.

**Contrast with safe patterns:** Presence of `prepareStatement` (Java), `.Parameters.Add` (ASP.NET), `mysqli->prepare` / `stmt->bind_param` (PHP), or `->prepare` / `->execute` (Perl) indicates parameterized queries — confirm that the prepared statement is actually used with bound parameters, not that the SQL string itself still incorporates concatenated user input before being prepared.

**Database stored procedures:** Extend this search to stored procedure definitions (`.sql` files, embedded SQL strings). A web application calling a parameterized stored procedure is safe only if the procedure itself does not construct dynamic SQL from its parameters. Search stored procedure code for dynamic SQL execution keywords: `EXEC` (MS-SQL, Sybase), `EXECUTE IMMEDIATE` (Oracle), `EXEC SQL` (DB2). If user-supplied procedure parameters are concatenated into these dynamic SQL strings, SQL injection exists in the database tier even when the application tier uses parameterized calls.

---

#### 2.3 — Path Traversal

**Grep for filesystem APIs:**

**Java:** `new File\(|FileInputStream|FileOutputStream|FileReader|FileWriter`

**ASP.NET:** `System\.IO\.File\.|FileStream\(|StreamReader\(|StreamWriter\(`

**PHP:** `fopen\(|readfile\(|file\(|fpassthru\(|include\(|require\(|include_once\(|require_once\(`

**Perl:** `open\s*\(|sysopen\s*\(`

For each hit, determine whether the filename parameter incorporates user-controlled data. The most common pattern is user data appended to a hard-coded base directory:
```csharp
FileStream fs = new FileStream("C:\\temp\\" + userInput, FileMode.Open);
```
This is vulnerable if `userInput` is not canonicalized and verified to not contain `..` sequences.

**For PHP `include()` / `require()`:** Also check whether the included file path can resolve to a remote URL (if `allow_url_include` is enabled in `php.ini`). Remote File Inclusion (RFI) produces arbitrary code execution.

**Grep for filename-related parameter names** as a quick surface finder:
```
AttachName|filename|filepath|file=|path=|template=|page=|include=
```

---

#### 2.4 — Arbitrary Redirection

**Grep for redirect APIs:**

**Java:** `sendRedirect\(|setStatus\(|addHeader\(`

**ASP.NET:** `HttpResponse\.Redirect\(|Response\.Status|Response\.StatusCode|Response\.AddHeader|Server\.Transfer`
Note: `Server.Transfer` changes the page processed server-side without issuing an HTTP redirect, so it cannot be exploited for external redirects — but it can still be used for internal access control bypass.

**PHP:** `http_redirect\(|header\s*\(.*Location|HttpMessage::setResponseCode|HttpMessage::setHeaders`

**Perl:** `->redirect\(`

For each hit, check whether the redirect URL string is constructed from user-controllable data (e.g., a `refURL` query string parameter, a `ReturnUrl` form field). Also check client-side JavaScript for redirect patterns:
```javascript
document.location = target;
window.location.href = url;
```
Trace whether the URL value originates from a DOM source (`document.URL`, `document.referrer`, `location.search`). After-validation canonicalization is a common bypass path — if the code calls `unescape()` after checking for `//`, the check can be bypassed with double-encoded slashes (`%25252f%25252f`).

---

#### 2.5 — OS Command Injection

**Grep for OS command execution APIs:**

**Java:** `Runtime\.getRuntime\(\)\.exec|Runtime\.exec\(`

**ASP.NET:** `Process\.Start\(|ProcessStartInfo`

**PHP:** `\bexec\s*\(|passthru\(|popen\(|proc_open\(|shell_exec\(|system\(`, and the backtick operator `` `command` ``

**Perl:** `system\s*\(|\bexec\s*\(|qx/|qx\(`, and the backtick operator

**C/C++ (native components):** `system\(|popen\(|execve\(|execl\(`

For each hit, determine whether user-controlled data forms part of the command string. In Java, `Runtime.exec(string)` interprets shell metacharacters if the argument is a single string — but `Runtime.exec(String[])` with arguments passed as separate array elements does not. Partial control of the command string may still be exploitable via argument injection (injecting command-line flags rather than shell metacharacters).

---

#### 2.6 — Backdoor Passwords and Hidden Debug Functions

**Grep for hardcoded credential patterns in authentication logic:**
```
equals\(".*"\)|\.equals\('.*'\)|==\s*["']
password.*==|password.*equals|"admin"|"password"|"secret"
```

**Grep for incriminating source code comments:**
```
// bug|// problem|// bad|// hope|// todo|// fix|// overflow
// crash|// inject|// xss|// trust|# bug|# hack|# fixme
# todo|# xxx
```

These comment searches often surface developer-acknowledged vulnerabilities that were never resolved, temporary workarounds that became permanent, or security test code that was never removed. Example from production code:
```c
char buf[200]; // I hope this is big enough
strcpy(buf, userinput);
```

**Also look for:** Unreferenced functions accessible via hidden URL parameters, `debug=1` style logic branches, IP address allowlists that bypass authentication.

---

#### 2.7 — Native Software Bugs (C/C++ components)

**Buffer overflow — grep for unchecked buffer manipulation APIs:**
```
\bstrcpy\b|\bstrcat\b|\bmemcpy\b|\bsprintf\b|\bgets\b|\bscanf\b
```
Also: their wide-character variants (`wcscpy`, `wcscat`, `swprintf`). For each hit, verify whether the destination buffer is large enough to accommodate the source data, and whether the source length is bounded. Even `strncpy` can be misused — check whether the size argument is `strlen(src)` rather than `sizeof(dst)` (the former still overflows if `src` exceeds `dst`'s size).

**Integer vulnerabilities — grep for signed/unsigned comparisons:**
```
len\s*<\s*sizeof|size\s*<\s*sizeof|length\s*<\s*sizeof
```
If `len` is a signed integer compared to `sizeof()` (which returns an unsigned `size_t`), a user-supplied negative value for `len` passes the check and causes the subsequent unchecked copy to overwrite memory.

**Format string vulnerabilities — grep for uncontrolled format strings:**
```
\bprintf\s*(\s*[^"]\|fprintf\s*(\s*[^"][^,]\|syslog\s*(\s*[^,]*,\s*[^"]
```
The dangerous pattern is `printf(userInput)` instead of `printf("%s", userInput)`. If the format string parameter is user-controllable, the attacker controls format specifiers — `%n` writes to arbitrary memory addresses, enabling code execution.

---

### Phase 3 — Line-by-Line Review of High-Risk Components

**ACTION:** Select the components listed below for close sequential reading. The goal is not to find every vulnerability via signatures, but to understand the security logic and find flaws in its design or implementation — race conditions, time-of-check/time-of-use issues, bypasses enabled by edge cases, incorrect trust assumptions.

**WHY:** Many serious vulnerabilities are not detectable by grep — they require understanding the surrounding logic. An authentication bypass may exist because a conditional check that should be `&&` is `||`. A session fixation vulnerability requires reading the session initialization flow end-to-end. These subtler issues are common in precisely the most security-critical code.

**Components to read line-by-line:**

1. **Authentication mechanisms** — login logic, password comparison, account lockout, password reset flow, multi-factor verification. Look for: timing-based username enumeration, bypass conditions (OR instead of AND in credential checks), hardcoded fallback credentials, insecure token generation for password reset.

2. **Session management** — session token generation, storage, validation, and invalidation. Look for: use of `java.util.Random` (predictable) instead of `SecureRandom`, session tokens derived from user-controllable data, session fixation (token not rotated after login), logout that does not invalidate the server-side session.

3. **Access control** — per-resource authorization checks, role validation. Look for: missing checks on sensitive endpoints, checks that rely on client-supplied role data, checks placed after the sensitive operation rather than before.

4. **Application-wide input validation utilities** — any class or function named `sanitize`, `validate`, `encode`, `escape`. Look for: allowlist vs denylist (denylists are almost always bypassable), post-validation canonicalization (decoding after checking), validation applied to the wrong parameter.

5. **Interfaces to external components** — database connections, OS command helpers, file access wrappers, LDAP queries. Confirm that parameterization is consistently applied and that no code path bypasses the wrapper.

6. **Native code (C/C++) integration points** — any JNI, P/Invoke, or C extension boundary where Java/.NET managed data crosses into unmanaged memory. Data length and character set assumptions made in managed code may not hold in native code.

---

### Phase 4 — Environment Configuration Review

**ACTION:** Read the platform configuration files and check the security-relevant settings below.

**WHY:** A perfectly written application can be made insecure by a misconfigured environment. Debug mode enabled in production exposes stack traces that reveal internal paths, class names, and database credentials. Permissive PHP `register_globals` creates uninitialized variable injection vectors that do not appear in the application source. Insecure cookie flags allow session token theft.

**Java — `web.xml`:**
- `login-config`: verify authentication method; if forms-based, check action is `j_security_check` with correct parameter names (`j_username`, `j_password`)
- `security-constraint` with `url-pattern`: verify all sensitive paths are covered; gaps mean unauthenticated access
- `session-config session-timeout`: overly long or zero timeout increases session hijacking window
- `error-page`: verify error codes map to custom pages (not stack traces)
- `init-param`: check `listings` is `false` and `debug` is `0`

**ASP.NET — `Web.config`:**
- `httpCookies httpOnlyCookies="true"`: prevents JavaScript cookie theft; `requireSSL="true"` prevents cookie transmission over HTTP
- `sessionState timeout`: session lifetime
- `compilation debug="false"`: debug symbols expose internals
- `customErrors mode="On"` or `"RemoteOnly"`: prevents detailed error disclosure to users
- `httpRuntime enableHeaderChecking="true"` (default): request header injection defense; `enableVersionHeader="false"`: prevents version disclosure

**PHP — `php.ini`:**
- `register_globals = Off`: if On, all request parameters become global variables — mandatory Off for any application not specifically designed for it
- `display_errors = Off`: prevents PHP errors from leaking to users; use `log_errors` + `error_log` instead
- `allow_url_fopen` and `allow_url_include`: if On, `include()` can load remote URLs — Remote File Inclusion vector
- `magic_quotes_gpc`: if On, single quotes in request parameters are auto-escaped — affects SQL injection testability; however magic quotes do not prevent numeric injection or second-order injection (data read from DB is unescaped); **removed in PHP 6**
- `safe_mode`: if On, restricts `shell_exec`, `exec` execution paths — but bypassable; not a security panacea; **removed in PHP 6**
- `file_uploads` and `upload_tmp_dir`: confirm uploaded files are stored in a non-web-accessible temporary path

**Perl:** Check for taint mode (`-T` flag in shebang `#!/usr/bin/perl -T`). Taint mode marks all user input as tainted and prevents tainted data from reaching dangerous functions (`eval`, `system`, `exec`, `open`) without explicit pattern-match untainting. If taint mode is not enabled, no framework-level protection exists against injection. If it is enabled, verify the untainting regexes are sufficiently restrictive — overly broad patterns (e.g., `(.*)`) that extract arbitrary content defeat the protection.

---

### Phase 5 — Document Findings

**ACTION:** For each confirmed vulnerability, record: vulnerability class, CWE identifier, severity, file path and line number(s), evidence (code snippet showing source → sink flow), and countermeasure.

**Severity guidance:**
- **Critical:** OS command injection with code execution, SQL injection with data access or authentication bypass, Remote File Inclusion, backdoor credentials
- **High:** Arbitrary file read via path traversal, XSS in authenticated context or on sensitive page, SQL injection limited to read-only data, stored XSS
- **Medium:** Reflected XSS in unauthenticated context, open redirect, Local File Inclusion, insecure direct object reference
- **Low:** Incriminating comments, configuration weaknesses without direct exploitability, verbose error disclosure

**Output format:**
```
## Source Code Security Review — [Application Name]
Date: [date]  |  Reviewer: [name]  |  Platform: [Java/PHP/etc]
Scope: [files or modules reviewed]

### FINDING-001 — [Vulnerability Class] — [File:Line]
- CWE: CWE-XX
- Severity: [Critical | High | Medium | Low]
- Location: [path/to/file.java:42]
- Evidence: [2-5 line code snippet showing the vulnerable pattern]
- Root cause: [1-2 sentences]
- Countermeasure: [specific fix]

## Coverage Summary
[Table: Phase | Files Reviewed | Findings]
```

---

## Inputs

- Web application source code (all server-side files, client-side JavaScript, database scripts)
- Platform configuration files (`web.xml`, `Web.config`, `php.ini`)
- Any existing SAST tool output (to focus manual effort on what tools miss)
- Scope definition: modules in scope, time budget

## Outputs

A **Source Code Security Review Report** with:
- Per-finding entries (class, CWE, severity, location, evidence, countermeasure)
- Coverage summary (phases completed, files reviewed, findings count by severity)
- Prioritized remediation list

---

## Key Principles

- **White-box finds a different population of bugs than black-box.** Backdoor passwords, condition-guarded logic flaws, and vulnerabilities that only activate for specific secondary parameter values are nearly impossible to find by fuzzing. Code review is not a replacement for behavioral testing — it is a complement that finds what fuzzing cannot.

- **Trace the full data flow — source to sink.** A dangerous API call is only a vulnerability if user-controlled data reaches it without adequate sanitization. Conversely, a piece of code that stores user data in a class field and later passes that field to a dangerous API is vulnerable even if the dangerous API call looks harmless in isolation. Never confirm or dismiss a finding without tracing the full path.

- **Denylists fail; allowlists don't.** Filters that block known-bad patterns (`../`, `<script>`, single quote) are routinely bypassed via URL encoding, Unicode encoding, case variation, or application-specific decoding. An application that validates input by allowlisting known-safe characters and rejecting everything else is structurally more robust. When you see a denylist filter protecting a dangerous API, treat it as a weak mitigant — look for bypasses.

- **Post-validation canonicalization is always a bug.** Any decoding, unescaping, or canonicalization performed after validation defeats the validation. If an application validates a redirect URL by checking for `//`, then calls `unescape()` on the value before using it, an attacker can encode the slashes as `%252f%252f` (percent-encoding the percent sign), pass validation, then have `unescape()` decode to `//`.

- **Configuration is part of the attack surface.** PHP `register_globals`, ASP.NET debug mode, and Java `listings=true` each create vulnerabilities that are not visible anywhere in the application source files. Always read the configuration files as part of the review scope.

- **Database stored procedures are not automatically safe.** Using parameterized calls from application code to invoke a stored procedure prevents SQL injection in the application tier — but if the stored procedure itself constructs dynamic SQL by concatenating its parameters, the vulnerability simply moves one layer deeper. Include stored procedure and trigger code in the review scope.

---

## Examples

**Scenario: Penetration test with source access — Java banking application**
Trigger: "We're granting you source access for this pentest. The application handles fund transfers and user account management."
Process:
1. Phase 1: Grep for `getParameter` — finds 47 call sites. Note `request.getParameter("title")` stored in `m_pageTitle` field in `PageController.java:88`.
2. Phase 2.1 (XSS): Grep for `InnerHtml` — finds `objCell.InnerHtml = link` in `ReportView.java:204`. Trace `link` backward — constructed by string concatenation from `HttpUtility.UrlDecode(Request.QueryString["refURL"])` without HTML-encoding. Confirmed reflected XSS (CWE-79, High). Also trace `m_pageTitle` forward — finds it written into `<title>` element in template renderer without encoding. Second XSS confirmed, conditionally triggerable (requires `type=3`).
3. Phase 2.2 (SQL injection): Grep for `createStatement` — finds `s.executeQuery("SELECT name, accno FROM TblCustomers WHERE " + SqlWhere)` in `CustomerSearch.java:156`. `SqlWhere` is built from `Request.QueryString["CID"]`. Confirmed SQL injection (CWE-89, Critical).
4. Phase 2.6 (Backdoor): Line-by-line review of `AuthService.java` — finds `if (checkCredentials(up, password) || "oculiomnium".equals(password)) return up;`. Hardcoded backdoor password grants access to any account (CWE-798, Critical).
Output: 3 findings — Critical SQL injection, Critical backdoor password, High XSS (x2). Countermeasures: replace `createStatement` with `prepareStatement`; remove hardcoded password; HTML-encode all output via `HtmlUtils.htmlEscape()`.

---

**Scenario: Pre-launch PHP e-commerce application review**
Trigger: "We're launching next month. Please review our PHP codebase for security issues before we go live."
Process:
1. Phase 1: Grep for PHP input sources — finds `$_GET`, `$_POST`, `$_COOKIE` in 23 files. Check `php.ini` — `register_globals = On` on their dev server; flag immediately.
2. Phase 2.3 (Path traversal + RFI): Grep for `include(` — finds `include($_GET['page'] . '.php')` in `main.php:12`. No `allow_url_include` check in code. Check `php.ini` — `allow_url_include = 1`. Confirmed Remote File Inclusion (CWE-98, Critical). Also: `allow_url_fopen = 1` and `display_errors = On` in production config.
3. Phase 2.2 (SQL injection): Grep for `mysql_query(` — finds `mysql_query("SELECT * FROM users WHERE username = '$username' AND password = '$password'")` in `login.php:34`. Variables from `$_POST` without escaping. Confirmed SQL injection (CWE-89, Critical). `magic_quotes_gpc = Off` confirms no runtime escaping active.
4. Phase 2.5 (OS command injection): Grep for `exec(` — finds `exec("convert " . $_POST['filename'] . " -resize 100x100 output.jpg")` in `image.php:67`. Confirmed OS command injection via shell metacharacters (CWE-78, Critical).
5. Phase 4 (Config): `display_errors = On` in `php.ini` — leaks stack traces and DB credentials to users (Low). `register_globals = On` — creates uninitialized variable injection vectors (High).
Output: 3 Critical findings, 1 High, 1 Low. Countermeasures: disable `allow_url_include` and `allow_url_fopen`; replace `mysql_query` with `mysqli->prepare`; replace shell `exec` with ImageMagick PHP extension API; set `display_errors = Off` + `log_errors = On`; set `register_globals = Off`.

---

**Scenario: Security audit of a PHP/JavaScript SPA — focus on client-side and database tier**
Trigger: "Our application is a single-page app with a PHP API backend. We've had a report of potential DOM-based XSS and we want to understand our stored procedure security posture."
Process:
1. Phase 2.1 (DOM XSS): Grep JavaScript for DOM sources and sinks — finds `url = document.URL; index = url.indexOf('?redir='); target = unescape(url.substring(index + 7, url.length)); document.location = target;` in `redirect.js:22`. Script checks for `//` to block absolute URLs but calls `unescape()` afterward. Confirmed DOM-based open redirect and XSS via `?redir=%2500javascript:alert(1)` (CWE-601 + CWE-79, High). Post-validation canonicalization bypass.
2. Phase 2.2 (Stored procedure SQL injection): Review `.sql` migration files — finds `CREATE PROCEDURE show_current_orders (@name varchar(400) = NULL) AS DECLARE @sql nvarchar(4000) SELECT @sql = 'SELECT id_num, searchstring FROM searchorders WHERE ' + 'searchstring = ''' + @name + ''''; EXEC (@sql) GO`. Even if the application calls this procedure with a parameterized API, the procedure itself constructs dynamic SQL from `@name` — confirmed stored procedure SQL injection (CWE-89, High).
3. Phase 3 (Session management): Line-by-line review of `TokenGenerator.java` — uses `java.util.Random` (not cryptographically secure) to generate session tokens. Session tokens are predictable given sufficient samples (CWE-338, High).
Output: 3 High findings — DOM-based XSS/redirect, stored procedure SQL injection, predictable session tokens. Countermeasures: remove `unescape()` call from redirect script; rewrite stored procedure using `sp_executesql` with parameterized query; replace `java.util.Random` with `java.security.SecureRandom`.

---

## References

- Per-platform source and sink API tables: [platform-api-reference.md](references/platform-api-reference.md)
- Environment configuration security settings: [environment-config-reference.md](references/environment-config-reference.md)
- CWE and OWASP mapping for findings: [vuln-cwe-owasp-mapping.md](references/vuln-cwe-owasp-mapping.md)
- Source: Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook* (2nd ed.), Chapter 19: "Finding Vulnerabilities in Source Code," pp. 701-745. Wiley.
