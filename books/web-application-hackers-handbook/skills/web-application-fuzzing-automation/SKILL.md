---
name: web-application-fuzzing-automation
description: |
  Build and execute customized automated attacks against web applications. Use this skill when: systematically enumerating valid identifiers (userids, document IDs, session tokens) by iterating through a parameter range and detecting hits via HTTP status code, response length, response time, Location header, Set-Cookie header, or grep expression; harvesting sensitive data at scale from access-control-flawed endpoints; fuzzing every request parameter with a universal payload kit covering SQL injection (`'`, `'--`, `'; waitfor delay '0:30:0'--`), XSS (`xsstest`, `"><script>alert('xss')</script>`), OS command injection (`|| ping -i 30 127.0.0.1 ; x || ping -n 30 127.0.0.1 &` and separator variants), path traversal (`../../../../../../etc/passwd`, `../../../../../../boot.ini`), script injection (`;echo 111111`, `response.write 111111`), and remote file inclusion (`http://<your-server>/`); selecting the correct Burp Intruder attack type: Sniper (one position cycled through all payloads), Battering Ram (same payload into all positions simultaneously), Pitchfork (parallel payload sets, one per position, advanced in lockstep), or Cluster Bomb (Cartesian product of multiple payload sets across multiple positions); maintaining valid sessions across automated runs using Burp Suite cookie jar, request macros (login, token fetch, multistep pre-requests), and session-handling rules (check session validity, run re-login macro, update token per request); bypassing automation barriers including per-request anti-CSRF tokens (macro extracts token from prior response, session-handling rule injects it), session expiry (validate-and-re-login rule), and CAPTCHA (solution exposed in source, solution replay, OCR, or human-solver integration); triaging results by clicking column headings to sort by status/length/time and Shift-clicking to reverse-sort. Covers JAttack custom Java scripting framework as a reference model for payload source design and response parsing. For authorized penetration testing and application security assessment only.
version: 1
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [14]
    pages: "571-613"
tags: [fuzzing, burp-intruder, automation, identifier-enumeration, data-harvesting, sql-injection, xss, os-command-injection, path-traversal, session-handling, csrf-token, captcha-bypass, payload-generation, penetration-testing, appsec]
execution:
  tier: 2
  mode: interactive
  inputs:
    - type: document
      description: "HTTP traffic / Burp Suite project file — request/response pairs to target"
    - type: text
      description: "Target URL, parameter names, scope confirmation from authorizing party"
  tools-required: [Read, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Authorized penetration test engagement. Burp Suite Professional (or equivalent) required for Intruder attack types and session-handling features. JAttack source available at companion site for custom scripting."
discovery:
  goal: "Enumerate valid identifiers, harvest data from vulnerable endpoints, or identify input-based vulnerabilities across all request parameters via automated fuzzing — producing a triage-ready results table and prioritized follow-up list"
  tasks:
    - "Select the correct automation mode (enumeration, harvesting, or fuzzing) and configure the matching attack type and payload source"
    - "Configure hit detection criteria appropriate to the target's response behavior"
    - "Address session-handling barriers before launching to prevent false negatives from expired sessions or missing tokens"
    - "Launch the attack, triage results by sorting on status/length/time/grep columns, and escalate anomalies to manual verification"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "bug-bounty-researcher"]
    experience: "intermediate-to-advanced — assumes working knowledge of HTTP, Burp Suite proxy/Intruder, and web vulnerability classes"
  triggers:
    - "Authorized pentest of an application with predictable identifiers, access-control findings worth harvesting, or large parameter surface needing fuzzing"
    - "Coverage of dozens of dynamic pages where manual per-parameter testing is not feasible"
    - "Session token analysis has revealed a pattern amenable to enumeration"
    - "Burp Scanner found a potential injection but coverage of remaining parameters is needed"
  not_for:
    - "Unauthenticated or unauthorized testing — written authorization required"
    - "Fully automated scanning without human triage — customized automation surpasses scanners only when a human reviews results"
    - "Deep exploitation of confirmed vulnerabilities — use dedicated exploit skills after fuzzing identifies the candidate"
---

# Web Application Fuzzing Automation

## When to Use

You have authorized access to a web application and need to go beyond manual, one-request-at-a-time testing. Customized automation is appropriate when:

- A parameter holds identifiers (document IDs, account numbers, session tokens) that need iterating to find all valid values
- An access-control flaw lets you access other users' data, and you want to harvest it at scale
- A large application has dozens of dynamic pages, each with multiple parameters — manual fuzzing is not feasible
- Initial manual probing has revealed promising indicators (error messages, status code variation) that need systematic confirmation across the full parameter space

**The core insight:** Every web application is different. Off-the-shelf scanners apply generic signatures. A skilled tester using customized automation combines human intelligence (selecting the right request, interpreting subtle response differences, thinking like the application's designer) with computerized brute force to achieve results neither can deliver alone.

**Authorized testing only.** Never apply these techniques without explicit written authorization from the application owner.

---

## Context and Input Gathering

### Required Context

- **Scope and authorization:** Which hosts, URLs, and parameters are in scope. Why: automation amplifies impact — an out-of-scope mistake at scale causes disproportionate harm.
- **A valid session:** An authenticated account to carry through the attack. Why: most interesting functionality and identifiers are behind authentication; testing unauthenticated surfaces only misses the majority of findings.
- **Target request/response pair:** The specific request to automate against, identified during manual recon. Why: automation needs a stable baseline — a request where the parameter of interest clearly affects the response.

### Observable Context (gather from environment)

- Parameters with sequential or guessable values: `uid=198`, `docId=10069`, `pageid=32010039`
- HTTP status code variation in response to different values (200 vs. 302 vs. 500)
- Response length variation — template pages return fixed length for misses, variable length for hits
- Session management mechanisms: anti-CSRF tokens in forms (field named `__csrftoken`, `nonce`, `_token`), session expiry behavior, multistage processes

---

## Process

### Step 1: Choose the Automation Mode

Three distinct uses for customized automation, each requiring different configuration:

**Identifier Enumeration** — Iterate through a range of values for a single parameter to determine which are valid. Hit detection is binary (valid vs. invalid). Payload source: numeric range or custom list.

**Data Harvesting** — Extend enumeration to extract content from each hit (page titles, names, credentials). Requires adding Extract Grep patterns to pull specific strings from each response. Hit detection is still used but you also capture response content.

**Vulnerability Fuzzing** — Submit a universal set of attack strings to every parameter in every request, regardless of normal function. You do not know in advance what a hit looks like; you capture as much response detail as possible and review manually for anomalies.

**WHY distinct modes matter:** Enumeration and harvesting require a focused request with a known-good baseline. Fuzzing is deliberately broad — you sacrifice focus for coverage. Mixing the two produces poor results: fuzzing an already-exploited endpoint wastes requests; applying a focused enumeration payload to a fuzz target misses everything else.

---

### Step 2: Configure Attack Type (Burp Intruder)

Select the attack type based on how many payload positions and payload sets your attack requires:

| Attack Type | Positions | Payload Sets | Behavior | Best For |
|---|---|---|---|---|
| **Sniper** | One at a time | 1 | Cycles each position through all payloads; other positions hold their baseline value | Fuzzing each parameter independently; most common choice |
| **Battering Ram** | All simultaneously | 1 | Same payload inserted into every position at once | Testing username-equals-password login, or inserting a single attack string everywhere |
| **Pitchfork** | Multiple, in lockstep | One per position | Advances all payload lists simultaneously (position 1 gets payload 1 from list A, position 2 gets payload 1 from list B, etc.) | Testing credential pairs from a known username/password list |
| **Cluster Bomb** | Multiple | One per position | Cartesian product — every combination of all payload sets | Brute-forcing debug parameter name + value pairs; credential stuffing from independent lists |

**WHY Sniper is the default for fuzzing:** When fuzzing for input-based vulnerabilities, you need to test each parameter in isolation. If you inject into all parameters simultaneously, an anomalous response becomes ambiguous — you cannot determine which payload in which parameter triggered it. Sniper eliminates this ambiguity. Each payload appears in exactly one parameter per request; all others remain at their baseline values.

**Set payload positions:** Use the "Auto" button in Intruder's Positions tab to mark all URL, cookie, and body parameter values automatically. Manually adjust to add or remove positions as needed.

---

### Step 3: Configure Payload Source

**For enumeration/harvesting:** Use the Numbers payload type. Configure sequential hexadecimal or decimal range, step size, and minimum digit count to match the application's identifier format. Example: tokens ending in 3 hex digits → range 0x000 to 0xfff, hex format, minimum 3 digits.

**For fuzzing:** Use the universal payload kit below. These are literal strings — Burp URL-encodes special characters by default; do not disable this.

```
# SQL Injection
'
'--
'; waitfor delay '0:30:0'--
1; waitfor delay '0:30:0'--

# XSS and Header Injection
xsstest
"><script>alert('xss')</script>

# OS Command Injection
|| ping -i 30 127.0.0.1 ; x || ping -n 30 127.0.0.1 &
| ping -i 30 127.0.0.1 |
| ping -n 30 127.0.0.1 |
& ping -i 30 127.0.0.1 &
& ping -n 30 127.0.0.1 &
; ping 127.0.0.1 ;
%0a ping -i 30 127.0.0.1 %0a
` ping 127.0.0.1 `

# Path Traversal
../../../../../../../../../../etc/passwd
../../../../../../../../../../boot.ini
..\..\..\..\..\..\..\..\..\..\etc\passwd
..\..\..\..\..\..\..\..\..\..\boot.ini

# Script Injection
;echo 111111
echo 111111
response.write 111111
;response.write 111111

# File Inclusion (point at a server you control and monitor for incoming connections)
http://<your-server>/
http://<nonexistent-ip>/
```

**WHY this kit:** Each string is the minimal probe for its class. The SQL `'` triggers syntax errors. The `waitfor` variants detect blind time-based SQL injection. The OS command strings use `ping` with a controlled delay — a 30-second response confirms blind injection regardless of whether output is visible. Script injection uses the literal value `111111` — if it appears alone in the response, the input was executed. Path traversal strings use redundant `../` sequences so they work regardless of how deep the web root is. File inclusion strings require monitoring for out-of-band connections, not response content.

---

### Step 4: Configure Hit Detection and Response Analysis

In Burp Intruder's Options tab, configure the attributes to capture from each response:

**Baseline columns (always captured):**
- HTTP status code
- Response length
- Response time

**Grep – Match:** Configure strings to flag in responses. For fuzzing, use:

```
error
exception
illegal
invalid
fail
stack
access
directory
file
not found
varchar
ODBC
SQL
SELECT
111111
quotation
syntax
```

**Grep – Extract:** For data harvesting, configure strings that precede the data you want to capture. Example: `<title>` captures page titles; `<td>Name: </td><td>` captures user names from HTML tables.

**Grep – Payload:** Enable "flag responses that reflect the payload" to detect potential XSS — any response that echoes back the `xsstest` string or the full XSS payload unmodified is a candidate.

**WHY response length is critical even when you have a reliable status code indicator:** Response length frequently surfaces anomalies you did not anticipate when designing the attack. In a session token enumeration, all HTTP 200 hits return roughly the same page — but noticeably longer responses indicate more-privileged user sessions. Always sort length even when status provides the primary signal.

---

### Step 5: Handle Session Barriers Before Launching

Identify which barriers apply to the target, then configure Burp's session-handling stack in the order below. Each layer operates on every outgoing Intruder request automatically.

**Cookie Jar (always enable):**
Burp maintains a cookie jar tracking all application cookies seen in proxied traffic. Enable "add cookies from cookie jar" as the first session-handling rule action for the target domain. This ensures the most recent session token is always included.

**Request Macros:**
A macro is a predefined sequence of one or more requests replayed before (or instead of) the attack request. Define macros for each barrier:

- *Validate session:* A GET to an authenticated page. Configure the macro item to read its session cookie from the cookie jar and update the jar with the response cookie. Used to check whether the current session is still valid.
- *Re-login:* POST to the login endpoint with preset credentials. Updates the cookie jar with the new session token. Triggered when session validation fails.
- *Obtain token/nonce:* GET or POST to the form page that contains the anti-CSRF token. Configure the macro item to extract the token from the response (Burp auto-detects derivable parameter relationships; manually confirm). The extracted value is injected into the target request.

**Session-Handling Rules (apply in this order):**

1. **All requests to target domain:** Add cookies from cookie jar.
2. **All requests to target domain:** Check whether session is valid by running the validate-session macro. If session is invalid, run the re-login macro and update the cookie jar.
3. **Requests containing the anti-CSRF token parameter:** Run the obtain-token macro and set the token parameter to the extracted value from the macro's final response.

**Scope each rule** to the correct Burp tools (Spider, Scanner, Intruder, Repeater as appropriate) and to the target host/URL pattern. Use the session-handling tracer to verify each rule fires correctly before launching the full attack.

**WHY this ordering matters:** Adding the cookie jar before the session-validity check ensures the check uses the current token, not a stale one. Validating before every request (rather than on failure) prevents a wave of failed requests from triggering account lockout or defensive session termination. Obtaining the token last ensures it is always fresh — anti-CSRF tokens are typically invalidated after a single use.

---

### Step 6: Launch the Attack and Triage Results

Launch the attack in Burp Intruder. Results appear in a table with one row per request.

**Triage workflow:**

1. Click the **Status** column heading to sort by HTTP status code. Anomalous status codes (200 among mostly 302, or 500 among mostly 200) surface immediately.
2. Click the **Length** column heading to sort by response length. Responses that are meaningfully longer or shorter than the majority are candidates for further review.
3. Click the **Time** column heading to sort by response time. Significant delays (≥25 seconds) against OS command injection payloads confirm blind time-based injection.
4. Click each **Grep column** heading to surface responses that matched the error/exception strings.
5. **Shift-click any column** to reverse-sort — useful to move both extremes into view without re-sorting by hand.
6. Double-click any row to view the full request and response. Right-click and "Send to Repeater" to manually investigate and refine the finding.

**What to look for:**

- **Enumeration:** Status code 200 (or a Set-Cookie with a session token) among predominantly 302/404/500 responses = valid identifier found.
- **Harvesting:** Extracted column values populated for hits; empty for misses.
- **Fuzzing — SQL injection:** Single `'` produces a response containing `quotation`, `syntax`, or `ODBC` that differs from the `'--` response (which may restore normal behavior); `waitfor` payload produces ~30-second delay.
- **Fuzzing — XSS:** Payload Grep column shows the `xsstest` string was reflected unmodified.
- **Fuzzing — OS command injection:** Response time for ping-based payloads is ~30 seconds; other payloads respond immediately.
- **Fuzzing — Script injection:** Response contains `111111` alone, not as part of the submitted string.

For each confirmed or suspected finding, refer to the dedicated vulnerability skill for detailed exploitation and verification steps.

---

## Inputs

- Burp Suite project file or proxy history with the target application's traffic
- At least one valid authenticated session (credentials or an active session token)
- Confirmed scope and authorization from the authorizing party
- (For harvesting) Knowledge of the HTML structure around the data to extract
- (For enumeration) Known baseline response for a valid identifier value

## Outputs

**Attack Results Table** with one row per request, columns: request number, parameter, payload, HTTP status, response length, response time, grep matches, extracted data (if configured). Sorted to surface anomalies.

**Follow-up Findings List** — for each anomalous row:
```
Parameter: [name]
Payload: [string]
Anomaly: [status/length/time/grep observation]
Suspected class: [SQL injection | XSS | OS command | path traversal | script injection | access control]
Next step: [manual verification approach]
```

---

## Key Principles

- **Isolation over coverage in fuzzing.** Test one parameter at a time (Sniper). If you inject into all positions simultaneously, you cannot attribute which payload triggered an anomaly. Isolation costs more requests but produces actionable results.

- **Response length is always informative.** Even when status code provides a reliable hit signal, sort the length column anyway. The most interesting results are often the ones you didn't design the attack to find.

- **Configure session handling before launching, not after failures appear.** A wave of unauthenticated requests from a failed session produces misleading uniform responses that look like no findings. The session-handling tracer is the only way to confirm your rules fire correctly before the full run.

- **Automation amplifies human intelligence, not replaces it.** The goal is to reduce the mechanical load — submitting hundreds of requests, recording status and length — so you can spend your time on what automation cannot do: reasoning about why a response is different, recognizing a pattern that doesn't fit the expected schema, and deciding which anomaly is a real finding versus noise.

- **10% accuracy is still useful.** For CAPTCHA bypass via automated solving, perfect accuracy is not required. An attack that solves only 1 in 10 puzzles correctly still completes the task in roughly 10x the time of a human — which is still orders of magnitude faster than manual testing at scale.

---

## Examples

**Scenario: Session token enumeration on an application with weak token generation**

Trigger: "The session tokens look partially sequential — I want to enumerate valid sessions for privilege escalation testing."

Process:
1. Analyze token structure from Burp Sequencer output: `000000-fb2200-16cb12-172ba72551`. The final 3 hex digits increment predictably; the middle segment is static; the second segment partially increments.
2. Capture a request to an authenticated page (`GET /auth/502/Home.ashx`) that returns HTTP 200 for a valid session and HTTP 302 to login for an invalid one.
3. Configure Intruder Sniper: one payload position on the last 3 hex digits of the session cookie value. Payload type: Numbers, range 0x000–0xfff, hex format, 3-digit minimum. No custom grep needed — status code is the hit signal.
4. Launch. Sort results by Status. HTTP 200 rows = valid hijackable sessions.
5. Sort results by Length. Two HTTP 200 responses are significantly longer than the rest — these are more-privileged user sessions. Double-click to confirm admin content.

Output: List of valid session tokens. Two confirmed as administrative. Escalate to manual session hijacking verification via Burp Repeater.

---

**Scenario: Data harvesting via access-control flaw on a user-details endpoint**

Trigger: "We found that `GET /auth/498/YourDetails.ashx?uid=198` returns any user's full profile — we need to harvest all accounts."

Process:
1. Inspect the response HTML: user data appears in table cells as `<td>Name: </td><td>Phill Bellend</td>`, `<td>Username: </td><td>phillb</td>`, `<td>Password: </td><td>b3ll3nd</td>`.
2. Configure Intruder Sniper: one payload position on `uid`. Payload type: Numbers, range 190–250 (start from known-good range, widen later). Session cookie as a fixed non-attack parameter.
3. Add three Extract Grep entries for `<td>Name: </td><td>`, `<td>Username: </td><td>`, `<td>Password: </td><td>` — each configured to capture text until the next `<`.
4. Launch. Sort by Status. HTTP 200 rows with populated extract columns = valid users.
5. Export tab-delimited results into a spreadsheet. Widen the UID range to capture all accounts.

Output: Complete user directory with credentials. Feed into privilege escalation and password reuse testing.

---

**Scenario: Baseline vulnerability fuzzing of a login form and authenticated function**

Trigger: "We need to fuzz every parameter in the login and in the user-detail page before concluding the assessment."

Process:
1. Send the login POST and the user-details GET from Burp Proxy history to Intruder using "Send to Intruder." Intruder auto-marks all parameter values as payload positions.
2. Configure Sniper attack type. Load the universal fuzzing payload kit (SQL, XSS, OS command, path traversal, script injection, file inclusion strings). Configure Grep-Match with the standard error-string list (`error`, `exception`, `quotation`, `syntax`, `ODBC`, `111111`, `xsstest`). Enable Payload Grep to flag reflected payloads.
3. For the user-details page, configure a session-handling rule: validate session before each request; re-login macro runs if session is invalid. This prevents the expired-cookie false-negative problem.
4. Launch both attacks. Sort each by Status, then Length, then Time.
5. Login form results: `'` in `username` produces status 200, length 2941, with `exception` and `quotation` in grep — different from all other payloads which produce length ~1600. Confirmed SQL injection candidate.
6. User-details results: `xsstest` in `uid` is reflected in the response body (Payload Grep column shows match). Confirmed reflected input — escalate to manual XSS exploitation check.

Output: Two candidates (SQL injection in login username, reflected input in uid parameter). Escalate each to the dedicated vulnerability skill for confirmation and exploitation.

---

## References

- Attack type decision guide: [references/intruder-attack-type-selection.md](references/intruder-attack-type-selection.md)
- Universal fuzzing payload kit (extended): [references/fuzzing-payload-kit.md](references/fuzzing-payload-kit.md)
- Session-handling rule templates: [references/session-handling-rule-templates.md](references/session-handling-rule-templates.md)
- Source: Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook* (2nd ed.), Chapter 14: "Automating Customized Attacks," pp. 571–613. Wiley.
