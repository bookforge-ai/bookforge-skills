---
name: web-application-penetration-testing-methodology
description: |
  Orchestrate a complete, structured web application penetration test through 13 testing areas during authorized security assessments. Use this skill when you are conducting a full web application security engagement and need a top-level methodology that sequences and delegates all testing phases — from initial reconnaissance through exploitation. Invoke it to plan and coordinate an engagement end-to-end: mapping application content, analyzing the attack surface, testing client-side controls, assessing authentication and session management, verifying access controls, probing all parameters for injection vulnerabilities, testing function-specific input flaws (SMTP, SOAP, LDAP, XPath, XXE), identifying logic flaws, checking shared hosting and server configuration, and conducting miscellaneous browser-security checks. Also invoke it as the master checklist for ensuring no test area has been missed, when delegating specific areas to domain-specific skills, or when producing a complete security assessment report. This is the hub skill — it calls twelve domain skills and provides the connective workflow between them. For white-box complement and source code analysis use alongside source-code-security-review.
version: 1
status: draft
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [21]
    pages: "791-888"
tags:
  - web-security
  - penetration-testing
  - methodology
  - hub-skill
  - appsec
  - owasp
  - burp-suite
  - vulnerability-assessment
  - sql-injection
  - xss
  - authentication
  - session-management
  - access-control
  - logic-flaws
  - server-hardening
  - input-validation
  - injection
  - security-assessment
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Scope definition: target URL(s), authorized domains, excluded paths, testing restrictions, available accounts/privilege levels"
    - type: document
      description: "Prior reconnaissance artifacts: proxy history, site map, Burp exports, source code, API specs — any available pre-engagement material"
    - type: context
      description: "Engagement type: black-box (no source), grey-box (partial source/architecture docs), or white-box (full source code access)"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Run within a project directory containing engagement artifacts. The human operates the browser and proxy; the agent analyzes findings, directs testing, and documents results. A live target is required for most testing phases."
discovery:
  goal: "Produce a complete, reproducible web application security assessment covering all 13 testing areas with findings, evidence, and remediation guidance"
  tasks:
    - "Sequence and coordinate all 13 testing areas in dependency order"
    - "Invoke domain-specific skills for each testing area"
    - "Accumulate findings across testing areas and identify cross-area vulnerability chains"
    - "Track tested vs. untested areas and ensure no area is skipped"
    - "Produce a consolidated findings report with severity ratings and remediation steps"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-consultant", "bug-bounty-hunter", "red-team-operator"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, web application architecture, proxy tools, and common vulnerability classes"
  triggers:
    - "Starting a full web application penetration test engagement"
    - "Conducting an authorized security assessment of a web application"
    - "Performing a structured security review that must cover all OWASP top-10 and beyond"
    - "Building a testing checklist to ensure complete coverage across a web application"
    - "Coordinating multiple domain-specific security assessments into a single engagement"
    - "Producing a deliverable security assessment report for a client or internal stakeholder"
  not_for:
    - "Unauthorized testing — this skill requires explicit written authorization for every target"
    - "Network-layer assessments (port scanning, service enumeration) — scope is the HTTP application layer"
    - "Infrastructure penetration testing — use a dedicated infrastructure assessment methodology"
    - "One-area-only testing — invoke the relevant domain skill directly instead"
---

## When to Use

Use this skill to **plan and execute a complete authorized web application security assessment**. It is the coordinating layer that sequences all 13 testing areas, delegates each area to the appropriate domain skill, and ensures nothing is missed.

Invoke it when:
- You are conducting a full-scope web application penetration test with explicit authorization
- You need a structured methodology to guide a multi-day engagement
- You want a master checklist that covers all standard testing areas
- You are producing a formal security assessment deliverable

Do not invoke it for unauthorized testing. Verify scope — exact hostnames, paths, and restrictions — before beginning. Advise the application owner to back up data before testing commences.

---

## General Guidelines

Apply these cross-cutting rules throughout every testing phase:

**URL Encoding Reference:** When injecting data into HTTP requests through a proxy (not a browser form), URL-encode characters that have special meaning in request syntax:

| Character | Meaning | Encoded Form |
|-----------|---------|--------------|
| `&` | Parameter separator (query string and body) | `%26` |
| `=` | Name/value separator | `%3d` |
| `?` | Query string start | `%3f` |
| ` ` (space) | URL end / cookie delimiter | `%20` or `+` |
| `+` | Encoded space | `%2b` |
| `;` | Cookie separator | `%3b` |
| `#` | Fragment identifier (truncates URL in browser) | `%23` |
| `%` | URL-encoding prefix | `%25` |
| null byte | Nonprinting | `%00` |
| newline | Nonprinting | `%0a` |

WHY: Submitting unencoded special characters causes them to be interpreted as request structure rather than data values. This produces false negatives — payloads that appear to be sent but are never received by the application in the intended form. Always verify the final request in the proxy before concluding a payload failed.

**False Positive Procedure:** When a crafted input produces a response associated with a vulnerability (error message, behavioral anomaly), always double-check by submitting benign input in the same parameter. If benign input triggers the same response, the finding is a false positive — the behavior exists independently of the attack payload.

WHY: Applications frequently display error messages or unusual behavior for reasons unrelated to the specific payload submitted. Confirming that benign input does not trigger the same response is the minimum verification step before recording a finding.

**State Accumulation and Reset:** Applications accumulate session state from prior requests, which can mask or distort test results. When investigating an anomaly, start a fresh browser session, navigate normally to the relevant location using only benign requests, then resubmit the crafted input. Alternatively, use a proxy replay tool (Burp Repeater) to isolate and resend specific requests.

WHY: If session state from earlier tests has altered the application's behavior — partially authenticated, locked-out account, cart in intermediate state — results from subsequent tests in that session cannot be attributed to the specific payload being tested.

**Load-Balanced Environments:** When the application sits behind a load balancer, consecutive requests may be handled by different back-end servers with slightly different configurations. Successful attacks that create server-side state (files written to disk, database records) may not be reproducible immediately. Repeat the same attack several times in succession to ensure routing to the relevant server before concluding an attack failed.

WHY: State-modifying attacks (command injection writing a file, SQL injection inserting a row) may succeed on one server but the confirmation request hits a different server. Repeating the request increases the probability of routing consistency and prevents missed exploits.

---

## Process

### Phase 1: Reconnaissance and Analysis

Complete reconnaissance before active vulnerability testing. Findings from reconnaissance directly shape how much time to invest in each subsequent testing area.

---

#### Area 1: Map the Application's Content

**Purpose:** Build a complete inventory of all reachable content, hidden directories, debug functionality, and identifier-driven functions. This inventory defines the scope of all subsequent testing.

**Invoke:** `web-application-attack-surface-mapping`

This skill covers:
- Explore visible content (browse entire application with proxy, follow recursive spider results)
- Consult public resources (search engines, web archives, WSDL files, developer forums)
- Discover hidden content (brute-force enumeration of directory and file names, client-side source review for hidden references)
- Discover default server content (Nikto scan, User-Agent variation checks)
- Enumerate identifier-specified functions (parameter-driven function names, common function name wordlists)
- Test for debug parameters (debug=true, test=on, hide=1, source=1 across key functions)

**Output required before proceeding:** Complete URL inventory, list of hidden content discovered, confirmed live debug parameters (if any).

---

#### Area 2: Analyze the Application

**Purpose:** Understand core functionality, all data entry points, server-side technologies, and map behavior to likely vulnerability classes. Produces the prioritized attack plan that directs investment across Areas 3–13.

**Invoke:** `web-application-attack-surface-mapping` (the analysis sub-tasks are included in this skill)

This skill covers:
- Identify core and peripheral functionality, security mechanisms, and administrative/logging functions
- Catalog all data entry points: URL segments, query parameters, POST body, cookies, HTTP headers, out-of-band channels
- Fingerprint server-side technologies: language, framework, database, third-party components
- Map each functional area to its most likely vulnerability classes
- Formulate a prioritized testing plan weighting most interesting functionality and most severe potential vulnerabilities

**Output required before proceeding:** Prioritized test plan with attack surface map. This plan determines how much time to allocate to each subsequent area.

---

### Phase 2: Application Logic Testing

---

#### Area 3: Test Client-Side Controls

**Purpose:** Identify all cases where security enforcement relies on client-side mechanisms (HTML field constraints, JavaScript validation, hidden parameters, browser extension logic) rather than server-side enforcement.

**Invoke:** `client-side-attack-testing`

This skill covers:
- Test transmission of data via client: hidden fields, cookies, preset parameters, ASP.NET ViewState (tamper and decode)
- Test client-side input controls: bypass maxlength restrictions and JavaScript validation; submit disabled form elements
- Test browser extension components (Java applets, Flash, Silverlight, ActiveX): decompile or attach debugger, intercept traffic, modify obfuscated data

WHY: Client-side controls are enforced by code running on a machine the attacker controls. Any security decision made solely by the client is bypassed by sending a crafted request directly via a proxy, bypassing the browser entirely.

**Key output:** List of parameters where client-side validation is not replicated server-side; any decoded ViewState revealing sensitive data or injectable input channels.

---

#### Area 9: Test for Logic Flaws

**Purpose:** Identify flaws in the application's business logic that cannot be detected by automated scanning — step-skipping in multistage processes, trust boundary violations, transaction manipulation.

**Invoke:** `application-logic-flaw-testing`

This skill covers:
- Identify key attack surface: multistage processes, critical security functions, trust boundary transitions, context-dependent functionality, price/quantity adjustment logic
- Test multistage processes: submit steps out of sequence, skip stages, access earlier stages after later ones, submit parameters from one stage at another
- Test handling of incomplete input: remove parameter name/value pairs from security-critical requests
- Test trust boundaries: accumulate state in one context, transition unexpectedly to a higher-trust context
- Test transaction logic: submit negative quantities, exploit successive transactions to achieve unintended states, manipulate price adjustment algorithms

WHY: Logic flaws do not produce anomalous error messages detectable by fuzzing — they produce the wrong valid responses. They require understanding the intended workflow and systematically violating assumptions.

**Key output:** Any step-skip vulnerabilities, trust elevation paths, transaction manipulation vectors.

---

### Phase 3: Access Handling Testing

---

#### Area 4: Test the Authentication Mechanism

**Purpose:** Assess the strength, implementation, and resilience of all authentication functions — login, registration, account recovery, remember-me, and impersonation.

**Invoke:** `authentication-security-assessment`

This skill covers (14 sub-areas):
- Understand the mechanism: authentication technologies in use, all auth-related functionality
- Test password quality rules: minimum requirements, incomplete validation
- Test for username enumeration: response differences between valid and invalid usernames across all auth functions
- Test resilience to password guessing: lockout policy, breadth-first vs depth-first attack strategy
- Test account recovery: challenge question guessability, recovery email predictability, URL reuse
- Test remember-me function: persistent cookie content, predictability, forgery potential
- Test impersonation functions: arbitrary impersonation without authorization, backdoor password indicators
- Test username uniqueness: collision-based enumeration, duplicate-credential registration attacks
- Test predictability of auto-generated credentials: sequence analysis, extrapolation
- Check for unsafe credential transmission: unencrypted channels, query-string exposure, cookie storage
- Check for unsafe credential distribution: predictable activation URLs, reusable activation tokens
- Check for insecure credential storage: shared hash values, rainbow table feasibility
- Test for fail-open authentication logic: empty parameter attacks, type confusion
- Test multistage authentication processes: stage skipping, parameter interception across stages
- Exploit identified vulnerabilities: breadth-first brute-force respecting lockout defenses

WHY: Authentication is the application's primary trust boundary. Weaknesses here often provide direct access to every other vulnerability in the application.

**Key output:** Any enumeration vectors, brute-force feasibility assessment, session fixation risk from account recovery, credential transmission flaws.

---

#### Area 5: Test the Session Management Mechanism

**Purpose:** Assess how the application establishes, maintains, and terminates user sessions — token generation, transmission security, and token handling.

**Invoke:** `session-management-security-assessment`

This skill covers (10 sub-areas):
- Understand the mechanism: session token format, which items actually reidentify users, scope of token validation
- Test tokens for meaning: correlations between token content and user identity, detectable encoding or obfuscation
- Test tokens for predictability: statistical analysis of token sequences (Burp Sequencer), time-dependent content, fixed differences between successive tokens
- Check for insecure token transmission: HTTP vs HTTPS transitions, secure flag on cookies, token exposure in URL
- Check for token disclosure in server-side logs: logging/monitoring functions that reveal tokens
- Check mapping of tokens to sessions: concurrent session support, static persistent tokens
- Test session termination: server-side timeout enforcement, logout actually invalidating the token
- Check for session fixation: whether a new token is issued after login, invented token accepted for authentication
- Check for CSRF: cookie-only session mechanism, predictable request parameters, PoC HTML page test
- Check cookie scope: domain/path attributes, subdomain scope risks, path-based scope that XSS can subvert

WHY: Weak session management allows attackers to hijack authenticated sessions without needing credentials — nullifying authentication entirely.

**Key output:** Predictability rating for session tokens, any insecure transmission paths, CSRF susceptibility, session fixation feasibility.

---

#### Area 6: Test Access Controls

**Purpose:** Verify that all privilege segregation — vertical (role-based) and horizontal (data ownership) — is enforced server-side on every request, at every stage of multistage functions.

**Invoke:** `access-control-vulnerability-testing`

This skill covers (4 sub-areas):
- Understand access control requirements: vertical and horizontal segregation model, identify the most valuable targets for privilege escalation
- Test with multiple accounts: use a high-privilege account to map all functionality, then attempt to access each item from a low-privilege account using Burp's compare site maps; test horizontal segregation by substituting resource identifiers between two same-privilege accounts
- Test with limited access: enumerate admin paths discovered during mapping, decompile clients for references, predict identifiers from observed patterns
- Test for insecure access control methods: parameter-based access control flags (edit=false), Referer-based controls, HTTP method-based container controls (HEAD method bypass)

WHY: Access controls are the most commonly broken class of web application control. Server-side enforcement must be present for every protected request — not only the first request in a sequence.

**Key output:** Any vertical privilege escalation paths, horizontal data isolation failures, insecure access control method bypasses.

---

### Phase 4: Input Handling Testing

---

#### Area 7: Test for Input-Based Vulnerabilities

**Purpose:** Fuzz every request parameter across the application for the full range of injection vulnerability classes, then follow up each positive signal with targeted exploitation testing.

**Invoke (fuzzing phase):** `web-application-fuzzing-automation`
**Invoke (SQL injection follow-up):** `sql-injection-detection-and-exploitation`
**Invoke (XSS follow-up):** `xss-detection-and-exploitation`
**Invoke (server-side injection follow-up):** `server-side-injection-testing`

**Fuzzing procedure (Area 7.1):** For every distinct request that submits parameters server-side, load into an automated fuzzer and submit the following payload sets across all parameter values simultaneously:

- SQL injection: `'`, `'--`, `'; waitfor delay '0:30:0'--`, `1; waitfor delay '0:30:0'--`
- XSS and header injection: `xsstest`, `*"><script>alert('xss')</script>`
- OS command injection: `|| ping -i 30 127.0.0.1 ; x`, `| ping -n 30 127.0.0.1 |`, `` ` ping 127.0.0.1 ` ``
- Path traversal: `../../../../../../../../etc/passwd`, `..\..\..\..\..\boot.ini`
- Script injection: `;echo 111111`, `response.write 111111`
- File inclusion: `http://<your-server-name>/`, `http://<nonexistent-IP>/`

Configure response grep terms: `error`, `exception`, `illegal`, `invalid`, `fail`, `stack`, `access`, `directory`, `file`, `not found`, `varchar`, `ODBC`, `SQL`, `SELECT`, `111111`. Also grep for payload echo (XSS/header injection indicator). Set up a listener to detect file inclusion callbacks.

WHY: Fuzzing all parameters simultaneously with a broad payload set surfaces anomalies that indicate where to investigate further. The goal is not to confirm exploitability from fuzzing alone, but to quickly identify which of hundreds of parameters warrant manual follow-up.

**Follow-up by vulnerability type after fuzzing:**

- **SQL injection signals** (error messages, time delays, string concatenation behavior) → invoke `sql-injection-detection-and-exploitation` to confirm, fingerprint database, and exploit for data extraction or authentication bypass
- **XSS signals** (payload reflected in response body, HTTP header context, stored and later displayed) → invoke `xss-detection-and-exploitation` for reflected XSS, stored XSS, header injection, and open redirection follow-up
- **OS command injection** (time delay correlated with ping count) → invoke `server-side-injection-testing` for command retrieval, out-of-band channel establishment, and privilege escalation
- **Path traversal** (anomalous response length, file content indicators) → invoke `server-side-injection-testing` for filter bypass sequences and file content escalation
- **Script injection** (111111 in response without echo marker) → invoke `server-side-injection-testing` for platform-specific command execution verification
- **File inclusion** (incoming HTTP connection to your listener, response time anomaly) → invoke `server-side-injection-testing` for remote file inclusion exploitation

Also fuzz out-of-band input channels (email content processed by the application, data fetched from external URLs). Run an automated vulnerability scanner alongside manual fuzzing to provide independent findings for comparison.

**Key output:** Complete list of anomalous responses per parameter, confirmed vulnerability type per positive signal, follow-up findings from domain skills.

---

#### Area 8: Test for Function-Specific Input Vulnerabilities

**Purpose:** Test vulnerability classes that are triggered only by specific application functionality types, not by generic fuzzing — these require understanding what the function does before testing it.

**Invoke:** `server-side-injection-testing`

This skill covers 7 function-specific injection types. Apply each only where the corresponding functionality is present:

- **SMTP injection (Area 8.1):** In email-related functions (contact forms, notification triggers), inject SMTP header sequences (`%0aCc:`, `%0d%0aBcc:`, full DATA command injection). WHY: applications that concatenate user input directly into SMTP commands allow sending arbitrary email through the server — spam relay and phishing delivery.

- **Native software vulnerabilities (Area 8.2):** For native code components, submit overlong strings (1100, 4200, 33000 bytes) for buffer overflow detection; submit integer boundary values (0x7f/0x80, 0xff/0x100, 0x7fff/0x8000, 0x7fffffff/0x80000000) for integer overflow; submit long format specifier strings (`%n%n%n%n...`, `%s%s%s%s...`) for format string vulnerabilities.

- **SOAP injection (Area 8.3):** In SOAP-enabled functions, submit a rogue XML closing tag (`</foo>`), then balanced open/close pairs. Submit XML comment open/close characters across adjacent parameters to comment out portions of the SOAP message.

- **LDAP injection (Area 8.4):** In directory-query functions, submit `*` (wildcard returns many results), `)))))))))` (syntax error), and expression pairs that produce differential behavior (`) (cn=*`). Try appending LDAP attributes (cn, mail, uid, objectclass) as comma-separated additions.

- **XPath injection (Area 8.5):** In XML data retrieval functions, submit `' or count(parent::*[position()=1])=0 or 'a'='b` (false condition) vs. `' or count(parent::*[position()=1])>0 or 'a'='b` (true condition). Differential behavior without error indicates XPath injection; extract the XML tree one byte at a time using substring conditions.

- **Back-end HTTP request injection (Area 8.6):** Where parameters specify server names or IP addresses, submit arbitrary server/port combinations and monitor for timeouts; submit `localhost` and your own IP for incoming connection callbacks. Inject URL-encoded additional parameters (`%26foo%3dbar`) to test HTTP parameter injection.

- **XML external entity (XXE) injection (Area 8.7):** Where XML is submitted to the server, inject a DOCTYPE entity declaration referencing a known local file or an internal URL. Monitor for file content disclosure in the response or time-based detection via internal network probing.

**Key output:** Any confirmed function-specific injection vulnerabilities with exploitation evidence.

---

### Phase 5: Hosting and Infrastructure

---

#### Area 10: Test for Shared Hosting Vulnerabilities

**Purpose:** Assess whether isolation between tenants in a shared hosting environment is effective, and whether compromise of one application enables lateral movement.

**Covered inline** (no dedicated domain skill required):

- **Shared infrastructure segregation (Area 10.1):** Examine whether remote access mechanisms (FTP, SSH, control panel) use secure protocols; determine whether one tenant can read or write files belonging to other tenants; test whether interactive shell access enables cross-tenant resource access. If command execution, SQL injection, or file access is achieved in any application, investigate whether it enables escalation to other co-hosted applications.

- **ASP-hosted application segregation (Area 10.2):** Identify shared components (logging mechanisms, admin functions, database code components) across multiple customer applications in an ASP model. Attempt to leverage these shared components to compromise the shared infrastructure. Audit database configuration and permissions using a database scanning tool if a common database is present.

WHY: Shared hosting converts an application-layer vulnerability into a host-layer vulnerability. SQL injection that reads one customer's data may read all customers' data if the database is shared.

**Key output:** Any cross-tenant access capability, shared component abuse vectors.

---

#### Area 11: Test for Application Server Vulnerabilities

**Purpose:** Assess the security posture of the web server and application container independently of the application logic — default credentials, dangerous HTTP methods, misconfigurations, and known software vulnerabilities.

**Invoke:** `web-application-hardening-assessment`

This skill covers (7 sub-areas):
- Default credentials: identify accessible administrative interfaces, test default and common credentials, assess functionality available after gaining access
- Default content: use Nikto scan results to identify default or known content present on the server; search exploit-db.com and osvdb.org for vulnerability details specific to identified technologies
- Dangerous HTTP methods: use OPTIONS to enumerate allowed methods; test each manually; investigate WebDAV methods if enabled
- Proxy functionality: attempt to use the server as an HTTP proxy via GET and CONNECT requests to external hosts, internal hosts, and localhost
- Virtual hosting misconfiguration: request root directory with correct Host header, bogus Host header, IP address as Host header, and no Host header; compare responses for directory listing differences or divergent content
- Web server software bugs: run Nessus or equivalent against identified server software; review Security Focus and Full Disclosure for recent vulnerabilities; consider local installation for novel bug discovery
- Web application firewalling: detect firewall presence via parameter-name attack payloads; identify blocked vs. permitted request locations (query string vs. POST body vs. cookies); use WAF bypass encoding techniques where a firewall is detected

WHY: Application server vulnerabilities are independent of the application code and frequently overlooked in application-focused reviews. Default credentials on a management interface can bypass all application-layer security controls.

**Key output:** Any accessible administrative interfaces, dangerous methods enabled, proxy functionality, virtual host leakage, known CVEs applicable to identified server software.

---

### Phase 6: Final Checks

---

#### Area 12: Miscellaneous Checks

**Purpose:** Cover browser-client security issues that do not fit into the preceding categories: DOM-based attacks, local privacy vulnerabilities, weak transport security, and cross-origin policy misconfigurations.

**Covered inline:**

- **DOM-based attacks (Area 12.1):** Review every JavaScript file received from the application. Identify where DOM-controllable sources (`document.location`, `document.URL`, `document.referrer`, `window.location`) flow into dangerous sinks (`document.write()`, `eval()`, `document.body.innerHTML`, `window.location`, `document.open()`). Test for DOM XSS and DOM-based open redirection by crafting URLs with payloads in the fragment or query string.

- **Local privacy vulnerabilities (Area 12.2):** Review all Set-Cookie headers for persistent cookies (future `expires` attribute); inspect their contents for sensitive data. Check whether pages containing sensitive data are served with `Cache-control: no-store`, `Pragma: no-cache`, and `Expires: past-date` headers. Check whether sensitive form fields use `autocomplete=off`.

- **Weak SSL/TLS configuration (Area 12.3):** Enumerate supported cipher suites and protocol versions. Identify weak ciphers (DES, RC4, export-grade), outdated protocols (SSLv2, SSLv3, TLS 1.0), and missing certificate validation requirements. Test for mixed-content issues (HTTPS page loading HTTP resources).

- **Same-origin policy configuration (Area 12.4):** Check `Access-Control-Allow-Origin` response headers for overly permissive cross-origin resource sharing (CORS) configuration — particularly `*` or reflection of the request's `Origin` header. Review `crossdomain.xml` (Flash) and `clientaccesspolicy.xml` (Silverlight) for overly permissive cross-domain access grants.

**Key output:** Any DOM XSS vectors, sensitive data in persistent cookies, missing cache headers on sensitive pages, weak ciphers, permissive CORS or cross-domain policy.

---

#### Area 13: Follow Up Any Information Leakage

**Purpose:** Investigate all cases where the application has disclosed information about its internal structure, technology stack, credentials, or error handling that could enable or refine attacks.

**Invoke:** `web-application-hardening-assessment`

Review and investigate:
- Verbose error messages containing stack traces, SQL queries, file paths, or component version information discovered during any prior testing phase
- HTTP response headers revealing internal server names, framework versions, or back-end topology
- HTML comments containing developer notes, disabled code, or internal endpoint references
- Debug output left visible in responses
- Information accessible via server default content identified in Area 11

WHY: Information leakage findings rarely produce direct impact but consistently enable more effective exploitation of other findings. A stack trace revealing the database query structure makes SQL injection exploitation dramatically more efficient.

---

### White-Box Complement

For grey-box or white-box engagements where source code is available, run alongside all testing phases:

**Invoke:** `source-code-security-review`

Source code review finds vulnerabilities that black-box testing cannot detect — insecure cryptography, hardcoded credentials, business logic flaws invisible from the outside, and dangerous function calls in code paths not reached by testing. It also confirms exploitability of suspected vulnerabilities and extends testing coverage beyond what the running application reveals.

---

### Findings Consolidation

After completing all applicable areas, consolidate findings across testing phases:

1. Group findings by vulnerability class (authentication, injection, access control, etc.)
2. Identify vulnerability chains — findings from one area that enable or amplify findings from another (e.g., XSS + CSRF = account takeover; information leakage + SQL injection = faster extraction)
3. Assign severity ratings using standard criteria: Critical (unauthenticated RCE, authentication bypass, SQL injection on sensitive data), High (authenticated privilege escalation, stored XSS, CSRF on sensitive functions), Medium (reflected XSS, information leakage of sensitive data, missing security headers), Low (information disclosure of non-sensitive data, weak cipher support without other risk factors)
4. For each finding, document: description, affected URL/parameter, evidence (request/response), severity rating, and remediation steps
5. Identify any areas that were scoped out or not testable, and note them explicitly in the report

---

## Inputs

- Written authorization to test the target application
- Scope definition: target URLs, allowed domains/paths, excluded functionality, any testing restrictions
- Available accounts: number of accounts at each privilege level available for testing
- Engagement type: black-box, grey-box, or white-box

## Outputs

- **Attack surface map:** Content inventory, entry points, technology fingerprint (from Area 1-2)
- **Testing log:** Per-area testing notes with payloads sent and responses observed
- **Findings register:** All confirmed vulnerabilities with severity, evidence, and remediation guidance
- **Untested areas log:** Any areas not tested and why
- **Consolidated assessment report:** Executive summary, findings narrative, severity ratings, remediation roadmap

---

## Key Principles

- **Follow the methodology, not the order** — The 13 areas have a logical sequence but information from any area may send you back to an earlier area. An access control finding may reveal URLs that need re-testing in Area 7. A file inclusion vulnerability may enable source code access that turns a grey-box engagement into white-box. Adapt continuously.

- **Accumulate state carefully** — Session state from earlier tests affects later tests in the same browser session. When testing a specific parameter or flow, start from a clean session state to ensure the behavior you observe is attributable to the current payload. Use Burp Repeater to isolate individual requests.

- **Confirm before recording** — A single anomalous response is not a confirmed vulnerability. Reproduce it. Apply the false-positive check (benign input in the same parameter). Verify that behavior difference is systematic and attributable to the payload. Only then record it as a finding.

- **Respect lockout defenses** — Password guessing, username enumeration, and brute-force attacks can lock out real users or generate alerts. Before launching automated attacks, identify lockout policies (threshold, lockout duration, lockout scope). Use breadth-first approaches — one password per username across all usernames — rather than depth-first per-username attacks.

- **Load-balanced targets require persistence** — In load-balanced environments, repeat exploits several times in succession. A successful attack that creates server-side state (a written file, a database row) may not be confirmable on the first follow-up request. Issue enough requests to be statistically likely to hit the same back-end server.

- **Source code access changes what is testable** — When source code is available, use `source-code-security-review` alongside all black-box testing phases. Source access enables confirmation of false positives, discovery of non-reachable code paths, and identification of cryptographic and business logic flaws invisible from the outside.

---

## Examples

### Example 1: Full Black-Box Penetration Test (E-Commerce Application)

**Scenario:** A client has contracted a penetration test of their retail web application. Authorization is confirmed. A staging environment is available.

**Trigger:** "Conduct a full penetration test of shop.example.com per the signed scope document. We have admin, seller, and buyer accounts."

**Process:**
1. Areas 1-2: Invoke `web-application-attack-surface-mapping`. Discover 340 URLs, 3 hidden admin endpoints, debug parameter `test=true` active on `/checkout/`. Technology: Java/Spring, PostgreSQL, Nginx. Prioritized plan: admin endpoints (highest), checkout debug parameter, search sort parameter, file upload.
2. Area 3: Invoke `client-side-attack-testing`. Find price field enforced only by JavaScript maxlength — server accepts arbitrary decimal values. Find ViewState on admin pages not MAC-protected.
3. Area 4: Invoke `authentication-security-assessment`. Find username enumeration via timing difference on login. Account recovery sends predictable sequential tokens. No lockout policy.
4. Area 5: Invoke `session-management-security-assessment`. Session tokens pass Sequencer entropy test. Session does not expire server-side — 14-day-old token accepted. CSRF on fund-transfer function — no anti-CSRF token.
5. Area 6: Invoke `access-control-vulnerability-testing`. Buyer account can access `/admin/users/export` (IDOR). Seller can modify other sellers' product prices by changing `seller_id` parameter.
6. Area 7: Invoke `web-application-fuzzing-automation` across all 340 parameterized requests. SQL injection signal in product search `sort` parameter (time delay). XSS signal in product review `name` parameter (payload reflected). Invoke `sql-injection-detection-and-exploitation` — confirm SQL injection, extract user table. Invoke `xss-detection-and-exploitation` — confirm stored XSS, demonstrate session hijacking.
7. Areas 8-13: No SOAP/LDAP functionality. Server running Nginx 1.14.2 — check CVE list, two known vulnerabilities. CORS configured with `*` on `/api/` endpoints.

**Output:** 12 findings (2 Critical, 4 High, 4 Medium, 2 Low). Critical: SQL injection on search (full database read), CSRF on fund transfer. Report delivered with reproduction steps and remediation guidance.

---

### Example 2: Grey-Box Security Review (Internal HR Portal)

**Scenario:** An internal security team is reviewing the company HR portal before a compliance audit. Source code and credentials for all role levels are available.

**Trigger:** "Security review of our HR portal — full access including source code. Findings needed for the compliance audit."

**Process:**
1. Areas 1-2: Invoke `web-application-attack-surface-mapping` against both source code and live application. Source grep reveals 6 API endpoints not linked from the frontend, including `/api/payroll/export-all`. Technology fingerprint: Python/Django, PostgreSQL.
2. Area 3: Invoke `client-side-attack-testing`. Employee ID field client-validated but server accepts any integer. Hidden `role` parameter in profile update endpoint.
3. Areas 4-5: Invoke `authentication-security-assessment` and `session-management-security-assessment`. Multi-factor authentication bypass: second factor not verified if `step` parameter is posted directly to final stage endpoint. Session fixation: pre-login session token retained after authentication.
4. Area 6: Invoke `access-control-vulnerability-testing`. Employee can access other employees' pay stubs by incrementing document ID. Manager-level API endpoints accessible with employee token.
5. Area 7: Invoke `web-application-fuzzing-automation`. Source code confirms `manager_id` parameter builds raw SQL string — confirmed injection. `name` field in search uses parameterized queries — no injection.
6. Invoke `source-code-security-review` across all phases: finds hardcoded database credentials in `settings.py`, insecure deserialization in session handling, timing-safe comparison missing from password verification.

**Output:** 9 findings. Critical: MFA bypass, SQL injection. High: broken access control (pay stubs), session fixation. Report formatted for compliance audit with GDPR and SOC 2 control mapping.

---

### Example 3: Targeted Re-Test After Remediation

**Scenario:** A client has applied fixes to findings from a prior engagement. They need a re-test of the remediated items plus any newly introduced surface.

**Trigger:** "Re-test the 8 findings from last quarter's report. They say everything is fixed. Also check the new API they launched."

**Process:**
1. Area 1-2: Run `web-application-attack-surface-mapping` focused on changed areas. New `/api/v2/` endpoints identified — not present in prior engagement.
2. Targeted re-test of prior findings per applicable domain skills: invoke each relevant domain skill with specific focus on the previously vulnerable parameter/function. Confirm or deny remediation for each.
3. Areas 7-8 on new API: Invoke `web-application-fuzzing-automation` against all `/api/v2/` endpoints. XXE vulnerability found in new XML upload endpoint (Area 8.7). SQL injection in one new search parameter.
4. Area 6 on new API: Invoke `access-control-vulnerability-testing` — new API endpoints accessible without authentication.

**Output:** 5 of 8 prior findings confirmed remediated; 3 inadequately fixed with bypass demonstrated. 3 new findings (Critical: unauthenticated API access; High: SQL injection in new endpoint; Medium: XXE). Differential report delivered showing remediation status per prior finding plus new findings.

---

## References

- Area 1-2 full procedures: `web-application-attack-surface-mapping` SKILL.md
- Area 3 full procedures: `client-side-attack-testing` SKILL.md
- Area 4 full procedures: `authentication-security-assessment` SKILL.md
- Area 5 full procedures: `session-management-security-assessment` SKILL.md
- Area 6 full procedures: `access-control-vulnerability-testing` SKILL.md
- Area 7 fuzzing procedures: `web-application-fuzzing-automation` SKILL.md
- Area 7 SQL injection follow-up: `sql-injection-detection-and-exploitation` SKILL.md
- Area 7 XSS follow-up: `xss-detection-and-exploitation` SKILL.md
- Area 7-8 server-side injection follow-up: `server-side-injection-testing` SKILL.md
- Area 9 full procedures: `application-logic-flaw-testing` SKILL.md
- Area 11 and 13 full procedures: `web-application-hardening-assessment` SKILL.md
- White-box complement: `source-code-security-review` SKILL.md
- URL encoding quick reference: `references/url-encoding-reference.md`
- Severity rating criteria and finding templates: `references/findings-templates.md`
