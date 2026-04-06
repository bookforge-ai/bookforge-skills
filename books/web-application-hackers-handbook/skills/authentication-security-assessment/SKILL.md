---
name: authentication-security-assessment
description: |
  Systematically assess web application authentication mechanisms for design flaws and implementation vulnerabilities. Use this skill whenever: testing the login security of a web application; auditing authentication for unauthorized access risk; evaluating password policy strength or brute-force resistance; checking whether login failure messages leak usernames (user enumeration); testing credential transmission over HTTP vs HTTPS; reviewing password change or forgotten password flows for logic flaws; assessing "remember me" cookie security; testing multistage login mechanisms for stage-skipping or cross-stage credential mixing; reviewing source code or HTTP traffic for fail-open logic or insecure credential storage; performing a penetration test or security code review of any user authentication system. Covers HTML forms-based, HTTP Basic/Digest, and multifactor authentication. Maps to OWASP Testing Guide (OTG-AUTHN-*) and CWE-287 (Improper Authentication), CWE-521 (Weak Password Requirements), CWE-307 (Improper Restriction of Excessive Authentication Attempts), CWE-640 (Weak Password Recovery Mechanism), CWE-312 (Cleartext Storage of Sensitive Information), CWE-522 (Insufficiently Protected Credentials).
version: 1
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [6]
    pages: "159-201"
tags: [authentication, login-security, brute-force, credential-security, password-policy, user-enumeration, session-management, multifactor-authentication, owasp, penetration-testing, appsec, cwe-287, cwe-307, cwe-521, cwe-640]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Application source code containing authentication logic, login handlers, session management — primary for code review mode"
    - type: document
      description: "HTTP traffic captures, Burp Suite logs, or security report — primary for black-box testing mode"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Run inside a project codebase for white-box review, or with HTTP traffic logs for black-box assessment. Authorized testing context required."
discovery:
  goal: "Identify all exploitable weaknesses across design flaws (13 categories) and implementation flaws (3 categories) in the application's authentication mechanism; produce a structured findings report with severity, evidence, and countermeasures"
  tasks:
    - "Map all authentication surfaces: login, password change, account recovery, registration, remember-me, impersonation"
    - "Test each design flaw category systematically using the relevant HACK STEPS"
    - "Test each implementation flaw category using behavioral probing and code analysis"
    - "Document findings with CWE mapping, severity rating, and evidence"
    - "Produce countermeasures aligned with the 'Securing Authentication' framework"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-minded-developer", "security-architect", "bug-bounty-researcher"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, web proxies (Burp Suite or equivalent), and basic authentication concepts"
  triggers:
    - "Penetration test of a web application's authentication mechanism"
    - "Security code review of login, password change, or account recovery logic"
    - "Pre-deployment security audit of authentication functionality"
    - "Post-incident analysis of an authentication bypass or account takeover"
    - "Assessment of brute-force resistance and account lockout behavior"
  not_for:
    - "Authorization or access control testing — use a dedicated access control assessment skill"
    - "Session token analysis — overlaps with session management testing (Chapter 7 scope)"
    - "SQL injection or injection attacks against login forms — use injection assessment skills"
---

# Authentication Security Assessment

## When to Use

You have authorized access to a web application and need to systematically assess its authentication mechanisms for exploitable weaknesses.

This skill applies when:
- A penetration test scope includes login, registration, password change, or account recovery functionality
- A code review targets authentication logic — login handlers, session creation, credential storage
- You need to assess brute-force resistance, account lockout policy, or credential transmission security
- You are evaluating whether a multistage login mechanism provides the security benefit it was designed to deliver

**The foundational insight from Stuttard and Pinto:** Authentication is conceptually simple but practically one of the weakest links in real-world applications. Developers fail to ask "what could an attacker achieve if they targeted our authentication mechanism?" systematically. Even one exploitable flaw is often sufficient to break the entire application — because if authentication fails, session management and access control become irrelevant.

**Two flaw classes exist and require different testing approaches:**
1. **Design flaws** — weaknesses inherent in how the mechanism was conceived (bad passwords, brute-forcible login, verbose errors). Detected by behavioral testing.
2. **Implementation flaws** — mistakes in coding a correctly designed mechanism (fail-open logic, multistage stage-skipping, insecure storage). Detected by code review and malformed-request probing.

**Authorized testing only.** This skill is for security professionals with explicit written authorization to test the target application.

---

## Context and Input Gathering

### Required Context (must have — ask if missing)

- **Testing mode (black-box vs white-box):**
  Why: black-box testing relies on behavioral observation of HTTP responses; white-box testing adds source code analysis which enables detection of implementation flaws that are otherwise invisible.
  - Check prompt for: "source code available," "code review," "codebase," vs "black-box," "external test," "no source"
  - If missing, ask: "Do you have access to the application's source code, or is this a black-box behavioral test?"

- **Authentication technologies in scope:**
  Why: the attack surface differs between HTML forms-based login (>90% of web apps), HTTP Basic/Digest, multifactor, and Windows-integrated authentication. Multistage login requires stage-sequencing analysis that single-stage does not.
  - Check environment for: login form HTML, HTTP headers (`WWW-Authenticate`), multi-step login flows, physical token references
  - If missing, ask: "Does the application use a single username/password form, multistage login (PIN, challenge question, physical token), or something else?"

- **Scope of authentication surfaces:**
  Why: weaknesses are often introduced in secondary functions (password change, account recovery) that developers treat as lower-security than the main login. Missing any surface means missing likely findings.
  - Check environment for: `/forgot-password`, `/change-password`, `/register`, `/impersonate` endpoints
  - If missing, ask: "Besides the main login, are password change, forgotten password, registration, and account recovery in scope?"

### Observable Context (gather from environment)

- **Existing HTTP traffic or Burp Suite session logs:**
  Look for: login POST requests, Set-Cookie headers, redirect chains after login, hidden form fields that carry state between stages
  If unavailable: agent conducts analysis from source code alone; note the limitation

- **Server-side credential storage:**
  Look for: database schema files, ORM model definitions, password field types (VARCHAR vs BINARY/CHAR for hashes), any plaintext password columns
  If unavailable: defer storage analysis to black-box inference (does the app ever return your password to you?)

- **Framework and language:**
  Look for: `package.json`, `requirements.txt`, `pom.xml`, `web.config`, framework config files
  If unavailable: assume no framework-specific protections are in place

### Default Assumptions

- Assume **no account lockout** is in place until tested — lockout is commonly absent or trivially bypassable
- Assume **all authentication surfaces are in scope** unless explicitly excluded
- Assume **HTTP Basic/Digest are not in use** on the primary login if HTML forms are present

---

## Process

### Step 1: Map the Full Authentication Attack Surface

**ACTION:** Identify every function where the application accepts credentials or performs authentication-related processing. Enumerate: main login, password change, forgotten password / account recovery, user registration, "remember me" functionality, administrative impersonation features, any API authentication endpoints.

**WHY:** Vulnerabilities deliberately avoided in the main login function frequently reappear in secondary functions. Password change endpoints are often accessible without authentication. Forgotten password flows commonly reintroduce username enumeration. Missing any surface means missing the most likely source of findings. An attacker examines all surfaces; an assessor must too.

**AGENT: EXECUTES** — Grep for authentication-related URL patterns, form actions, and route handlers. Enumerate all endpoints.

**IF** white-box mode → grep source code for login handler function names, password comparison logic, session creation, credential-related routes
**ELSE** → use application spidering results or manually walk every link on the login, registration, password change, and recovery pages

---

### Step 2: Assess Password Quality Controls (Design Flaw: Bad Passwords)

**ACTION:** Determine what password quality rules, if any, the application enforces. Test by reviewing published FAQ/help text, attempting registration or password change with: blank passwords, single characters, passwords identical to the username, common dictionary words (password, 12345678, qwerty, letmein, monkey), and very short values.

**WHY:** Applications without strong password quality rules will contain a large number of user accounts with weak passwords. An attacker who can guess even a few high-probability passwords against a list of valid usernames will compromise real accounts. Common real-world passwords (documented from breach databases) are a small, well-known set. The absence of enforcement means even amateur attackers succeed.

**HANDOFF TO HUMAN** — Self-registration attempts and password change tests require interactive browser/proxy interaction. Agent interprets results.

**Check for:**
- Minimum length enforcement (target: 8+ characters, ideally 12+)
- Character diversity requirements (uppercase, lowercase, numeric, special characters)
- Rejection of username-as-password
- Rejection of common dictionary passwords
- Server-side vs client-side-only enforcement (client-side-only is a low-severity finding — an attacker can bypass it to set a weak password for themselves, but it does not directly compromise other users)

---

### Step 3: Test Brute-Force Resistance (Design Flaw: No Account Lockout)

**ACTION:** Using an account you control, submit approximately 10 failed login attempts with incorrect passwords. Observe whether the application: (a) returns a message about account lockout or suspension, (b) locks the account, (c) continues accepting login attempts without any throttling. If using a proxy, test whether the failed login counter is stored in a client-side cookie (bypass: discard the cookie and start a fresh session).

**WHY:** If the application allows unlimited login attempts, an automated attacker can try thousands of passwords per minute from a standard connection. Even the strongest password eventually falls. Brute-force resistance is a defense that protects all accounts simultaneously — its absence means that any username the attacker knows is eventually compromisable given sufficient time.

**AGENT: EXECUTES** (analysis) — HANDOFF TO HUMAN (actual login attempts via proxy.

**Breadth-first attack strategy (document for the report):** When targeting multiple usernames, iterate through the most common passwords once across all usernames rather than exhausting all passwords against one username. This discovers weak-password accounts faster and avoids triggering per-account lockout thresholds.

**Test session-based lockout bypass:**
- If lockout is triggered, obtain a fresh session token (visit the site without the `Cookie` header) and continue attempting the same account
- If the counter resets, the lockout is stored client-side and trivially bypassed

**Test whether lockout reveals credentials:**
- Submit the correct password against a locked account. If the application returns a different response than for an incorrect password, the lockout can be used to verify a guessed password even without logging in.

---

### Step 4: Test for Username Enumeration (Design Flaw: Verbose Failure Messages)

**ACTION:** Using a known valid username (your test account) and a known invalid username, submit failed login attempts and compare every aspect of the server's response: HTTP status code, response body text, response length, HTML source (including hidden elements and comments), redirect behavior, response timing. Repeat on: the main login, the password change form, the forgotten password form, and self-registration.

**WHY:** When an application distinguishes "username not found" from "wrong password," it enables an attacker to enumerate valid usernames automatically. A confirmed list of valid usernames dramatically accelerates brute-force attacks, targeted password guessing, phishing, and social engineering. The attacker no longer needs to guess both credentials simultaneously — they can confirm usernames first, then target only known-valid accounts.

**AGENT: EXECUTES** — Read and compare response contents when source code is available; analyze HTTP response diffs when traffic logs are provided.

**Subtle enumeration channels to check:**
- Typographical differences in supposedly identical error messages across different code paths
- Response length differences (even a single character difference counts)
- Timing differences — a valid username may trigger slower processing (database lookup, password hash computation) than an invalid one, creating a measurable timing oracle even when messages appear identical
- Self-registration: if the application rejects an already-registered username, registration is an enumeration oracle

---

### Step 5: Test Credential Transmission Security (Design Flaw: Vulnerable Credential Transmission)

**ACTION:** Perform a complete login while intercepting all traffic with a proxy. Verify that: (a) the login page itself is loaded over HTTPS (not just submitted over HTTPS), (b) credentials are submitted only in the POST body — not URL query parameters, not cookies, (c) credentials are not reflected back to the client in any response, (d) credentials are not stored in cookies.

**WHY:** Credentials submitted in URL query strings appear in: browser history, server access logs, and reverse proxy logs — any of which may be accessible to an attacker who compromises a related system. Loading the login form over HTTP allows a man-in-the-middle attacker to modify the form's action URL to HTTP before the user submits credentials, capturing them even when the submission itself is HTTPS. A common developer mistake is to load the page on HTTP "for performance" and only switch to HTTPS at submission — this is insufficient.

**AGENT: EXECUTES** — Grep source code for form action URLs, HTTP vs HTTPS checks, credential parameter names in query strings, cookie-setting on login.

**Check for these common vulnerabilities:**
- Login form loaded via HTTP, submitted via HTTPS (man-in-the-middle attack surface)
- Credentials passed as query string parameters in any redirect after login
- Credentials stored in cookies (even encrypted — replay attacks remain possible)
- Any transmission of a cleartext credential in any direction (including password field pre-population)

---

### Step 6: Assess Password Change Functionality (Design Flaw: Password Change Flaws)

**ACTION:** Locate the password change function (it may not be linked from obvious navigation). Make requests with: invalid usernames, invalid existing passwords, and mismatched "new password"/"confirm password" values. Test whether the function enforces the same brute-force protections as the main login. Check whether a hidden form field or cookie specifies the target username.

**WHY:** Password change functions frequently reintroduce vulnerabilities that were carefully avoided in the main login. Developers apply security rigor to the front door but leave side doors unguarded. A password change function that allows unlimited guesses of the "existing password" field is a second brute-force surface, often with weaker defenses. A function that identifies the user via a hidden form field (rather than the authenticated session) can be exploited to change another user's password.

**AGENT: EXECUTES** (code analysis) — HANDOFF TO HUMAN (interactive testing).

**Specific checks:**
- Is the function accessible without authentication? (It should not be.)
- Does it contain a username field (visible or hidden)? Attempt to supply a different username.
- Does it provide verbose error messages that reveal whether a username exists?
- Does it allow unlimited guesses of the existing password field?
- Does it check that new password and confirm password match before validating the existing password? (If yes, the response to a mismatch reveals whether the existing password was correct — a timing/logic oracle.)

---

### Step 7: Assess Account Recovery Functionality (Design Flaw: Forgotten Password Flaws)

**ACTION:** Walk through the complete forgotten password flow using an account you control. Test: whether the recovery challenge is brute-forcible, whether the recovery URL is predictable, whether the recovery mechanism discloses the existing password, whether the mechanism drops the user into an authenticated session without password verification.

**WHY:** Forgotten password mechanisms are frequently the weakest link in the overall authentication chain. Security questions have a far smaller answer space than passwords — "mother's maiden name" may have thousands of plausible values, not billions. Users set trivially guessable challenges ("Do I own a boat?"). Even well-designed challenge mechanisms are undermined if the account recovery step discloses the existing password or grants immediate authenticated access without credential verification.

**HANDOFF TO HUMAN** — Walkthrough requires interactive browser session with a test account.

**Check for these common weaknesses:**
- Brute-forcible challenge responses (no lockout on the forgotten password form)
- Password "hints" that reveal or heavily suggest the password value
- Recovery URL sent to an attacker-controlled email address (if the email address field is in a hidden form field or cookie, it can be modified)
- Recovery mechanism that discloses the existing forgotten password (attacker can repeat the challenge indefinitely to always know the current password)
- Recovery URL that is predictable from a sequence (analyze multiple recovery URLs using the same techniques as session token analysis)
- Immediate authenticated session granted upon challenge completion, without requiring password reset

---

### Step 8: Test "Remember Me" Functionality (Design Flaw: Remember-Me Flaws)

**ACTION:** Activate any "remember me" feature and inspect all persistent cookies and local storage that are set. Determine whether the cookie stores the username directly, a predictable session identifier, or a securely encrypted/random token. Attempt to modify the cookie value to impersonate another user.

**WHY:** Remember-me cookies that store a plaintext username (e.g., `RememberUser=alice`) authenticate the user based solely on the cookie value — bypassing password verification entirely. An attacker who enumerates valid usernames can construct valid remember-me cookies and log in as any user without knowing their password. Even encoded or encrypted cookies may be reverse-engineerable if the encoding is applied consistently across accounts.

**AGENT: EXECUTES** (cookie analysis in source code or traffic logs) — HANDOFF TO HUMAN (manipulation via proxy).

**Tests to perform:**
1. Does the remember-me cookie fully bypass password entry on return visit, or only pre-fill the username field? (The latter is much lower risk.)
2. Does the cookie contain a recognizable identifier (username, user ID, email)?
3. Does repeated "remembering" of similar usernames reveal a pattern in the cookie value?
4. Can the cookie be modified to contain another user's identifier, gaining access to their account?

---

### Step 9: Test for User Impersonation Functionality (Design Flaw: User Impersonation)

**ACTION:** Search for impersonation functionality that may not be linked from published navigation (e.g., `/admin/impersonate`, `/switch-user`). Test whether: the impersonation endpoint is accessible without administrative authentication, user-supplied parameters control which account is being impersonated, any login "backdoor password" exists that works across all accounts.

**WHY:** Impersonation functionality implemented as a hidden URL without access controls is effectively a complete authentication bypass — anyone who discovers the URL can access any user's account. Backdoor passwords for impersonation are discovered during brute-force attacks (they appear as a second "hit" matching multiple usernames) and expose every account in the application. If administrative accounts can be impersonated, the vulnerability escalates to full application compromise.

**AGENT: EXECUTES** (grep for impersonation routes, admin URLs, backdoor indicators in source) — HANDOFF TO HUMAN (interactive testing).

**Signs of backdoor password:** During password-guessing attacks, the same password successfully logs in to multiple different user accounts, or a brute-force attack produces two separate "hits" for a single account (one for the real password, one for the backdoor password).

---

### Step 10: Test Incomplete Credential Validation (Design Flaw: Incomplete Validation)

**ACTION:** Using an account you control, attempt login with: the password truncated by the last character, the password with a character changed from uppercase to lowercase (or vice versa), the password with special/typographic characters removed. If any of these succeeds, continue experimenting to characterize the exact validation behavior.

**WHY:** Applications that truncate passwords (validating only the first N characters) or perform case-insensitive comparison reduce the effective password space by orders of magnitude. A 12-character password truncated to 8 characters has the same effective strength as an 8-character password. Case-insensitive comparison halves the entropy per character. These limitations massively improve an attacker's chances in an automated attack once discovered, and they can be fed back into the attack to eliminate superfluous test cases.

---

### Step 11: Test for Nonunique and Predictable Usernames (Design Flaw: Username Issues)

**ACTION (Nonunique usernames):** If self-registration is available, attempt to register the same username twice with different passwords. If the second registration succeeds, test the collision behavior. If blocked, the registration form is an enumeration oracle — use it to enumerate existing usernames.

**ACTION (Predictable usernames):** If the application generates usernames automatically, register several accounts in quick succession and analyze the sequence. Extrapolate backward to infer a list of all existing usernames.

**WHY:** Nonunique usernames create a collision attack where an attacker can register a target username with a known password. If the application handles the collision by merging accounts, the attacker gains access to the original account's data. Predictable usernames eliminate the need for enumeration — the attacker already has a complete, high-confidence username list before making a single login attempt, enabling stealth brute-force attacks with minimal application interaction.

---

### Step 12: Test Fail-Open Login Logic (Implementation Flaw)

**ACTION:** Perform a complete valid login, recording every request parameter and cookie in both directions. Then repeat the login numerous times, each time modifying one parameter in unexpected ways: submit an empty string, remove the parameter entirely, submit an unexpectedly long value, submit a string where a number is expected, submit the same parameter multiple times with different values. For each malformed request, carefully compare the server's response against the baseline success and failure responses.

**WHY:** Fail-open logic occurs when an exception during login processing (null pointer, type mismatch, missing parameter) causes the application to bypass the authentication check and grant access. This flaw is invisible to behavioral testing of the happy path — it only manifests when unexpected input causes code to take an error-handling path that skips the credential validation logic. The most dangerous implementations are not obvious fail-opens like an empty catch block — they are complex multi-layered method calls where an exception at any point can propagate in an unexpected way.

**AGENT: EXECUTES** (code analysis for exception handling patterns, fail-open conditions) — HANDOFF TO HUMAN (malformed request submission via proxy).

**In source code, look for:**
- `try { /* login logic */ } catch (Exception e) { }` with subsequent authenticated-state code
- Login functions that return `true` (success) as a default, requiring explicit `false` to deny
- Missing null checks on the user object returned from credential lookup

---

### Step 13: Test Multistage Login Mechanisms (Implementation Flaw)

**ACTION:** Map every distinct stage of the login, documenting what data is collected and validated at each stage and what data is passed between stages (especially hidden form fields, cookies, and URL parameters). Test for: (a) stage skipping — proceeding directly to stage 3 without completing stage 2, (b) cross-user mixing — providing valid credentials for user A at stage 1 and valid credentials for user B at stage 2, (c) state manipulation — modifying hidden fields that encode login progress (e.g., `stage2complete=true`).

**WHY:** Multistage login mechanisms are commonly believed to be more secure than single-stage. In practice, the added complexity creates more opportunities for implementation error. The most dangerous class of flaw: an application validates the username at stage 1 but does not enforce that the same username is submitted at stage 2. An attacker with one user's password and another user's physical token can mix credentials across stages to authenticate as either user — partially defeating the entire multi-factor design at significant cost to the application owner.

**AGENT: EXECUTES** (code analysis for cross-stage data flow, server-side vs client-side state tracking) — HANDOFF TO HUMAN (stage manipulation via proxy).

**Critical check: client-side state tracking.** If login progress (which stages are complete) is tracked in hidden form fields or cookies rather than server-side session variables, an attacker can forge that state and advance directly to any stage.

---

### Step 14: Assess Credential Storage Security (Implementation Flaw)

**ACTION:** In white-box mode: examine the database schema and any ORM model for the users/accounts table. Identify the data type and any hashing configuration for the password field. Check whether salted, slow hashing algorithms are used (bcrypt, scrypt, Argon2, PBKDF2). In black-box mode: look for any authentication-related functionality that ever returns your password to you (password hints, welcome emails with your existing password, password change emails that include new or old passwords) — these behaviors indicate reversible storage.

**WHY:** Insecure credential storage means that a database breach (via SQL injection, access control weakness, or server compromise) produces immediately exploitable credentials. MD5 and SHA-1 hashes of common passwords are precomputed in online databases — cracking them takes milliseconds. Unsalted hashes allow identical passwords to be identified by their shared hash value, enabling mass cracking. Secure hashing (bcrypt, Argon2) with per-user salts means a breach produces hashes that require significant per-hash computation to crack — buying time for users to change passwords.

**AGENT: EXECUTES** — Grep source code for password hashing library usage; inspect schema files for password column definitions.

**Red flags in source code:**
- `MD5(password)`, `SHA1(password)`, or any fast hash without a salt
- Plaintext password comparison: `if (user.password == submitted_password)`
- Password retrieval functions (SELECT password FROM users WHERE ...) used outside administrative contexts

---

### Step 15: Document Findings and Map Countermeasures

**ACTION:** For each confirmed vulnerability, write a finding with: flaw category, CWE identifier, severity (Critical/High/Medium/Low), evidence (request/response or code snippet), and the specific countermeasure from the "Securing Authentication" framework. Produce a structured assessment report.

**WHY:** Findings without mapped countermeasures are incomplete — they tell the development team what is broken but not what to do about it. The countermeasure framework ensures recommendations are specific and actionable, not generic ("use strong passwords"). Linking to CWE identifiers enables teams to cross-reference OWASP testing guides and vendor security advisories.

**AGENT: EXECUTES** — Writes the assessment report to a file.

---

## Inputs

- Application login endpoint and any known authentication-related URLs
- HTTP proxy session / Burp Suite project file (black-box mode)
- Application source code — authentication handlers, session management, user model (white-box mode)
- Database schema or ORM model definitions (white-box mode, for storage analysis)
- Test account credentials with known password (for behavioral testing steps)
- Scope confirmation from the authorizing party

## Outputs

**Authentication Security Assessment Report** containing:

```
# Authentication Security Assessment — [Application Name]
Date: [date]
Assessor: [name/team]
Mode: [black-box | white-box | hybrid]
Scope: [authenticated surfaces tested]

## Executive Summary
[2-3 sentences: overall posture, highest severity finding, recommended priority]

## Findings

### [FINDING-001] [Flaw Name]
- CWE: CWE-XXX
- Severity: [Critical | High | Medium | Low]
- Surface: [main login | password change | account recovery | ...]
- Evidence: [request/response excerpt or code snippet]
- Countermeasure: [specific remediation]

[... repeat for each finding ...]

## Countermeasure Summary
[Table: Finding ID | Severity | Countermeasure | Priority]

## Attack Surface Coverage
[Table: Surface | Tested | Findings Count]
```

---

## Key Principles

- **Authentication is the front line — one break defeats all downstream controls.** Session management and access control depend on authentication to establish identity. An attacker who bypasses authentication bypasses every control built on top of it. This is why a medium-severity finding in authentication often has higher real-world impact than a critical-severity finding in a lower-value function.

- **Secondary functions introduce primary vulnerabilities.** Password change, forgotten password, and registration consistently reintroduce vulnerabilities that were carefully avoided in the main login. Developers apply security review to the main login and assume secondary functions are lower-risk. Assessors must give equal attention to every function that accepts or processes credentials.

- **Behavioral testing reveals design flaws; code analysis reveals implementation flaws.** No amount of happy-path behavioral testing will reveal a fail-open exception handler. No amount of code reading will tell you whether the timing difference between valid and invalid usernames is large enough to exploit. Both modes are necessary for complete coverage.

- **Account lockout bypass is often trivial — test it explicitly.** Client-side lockout counters (in cookies or hidden fields) can be reset by obtaining a fresh session. Session-based counters can sometimes be bypassed by rotating sessions before the threshold. The presence of a lockout UI message does not guarantee the lockout is enforced server-side for automated traffic.

- **Multistage complexity does not equal security.** The common assumption that more authentication stages means stronger security is wrong. Each additional stage adds complexity and introduces new opportunities for implementation error. Multistage mechanisms should be tested more rigorously than single-stage, not less — the design investment makes it especially important that the implementation is correct.

- **Enumerate all authentication surfaces before testing any of them.** An incomplete attack surface map means incomplete findings. Authentication weaknesses cluster in side-door functions (account recovery, impersonation) that are easy to miss during a time-limited assessment.

---

## Examples

**Scenario: Black-box penetration test of a financial services login**
Trigger: "We need a pentest of our banking portal login page before the Q2 launch."
Process:
1. Map authentication surfaces: main login (multistage: username + password + SMS OTP), forgotten password, password change, remember-me, no impersonation found.
2. Step 4 (username enumeration): Login with valid username + wrong password returns "Incorrect password." Login with invalid username returns "User not found." — confirmed username enumeration via verbose failure message (CWE-203). Repeated on forgotten password form: same enumeration exists there.
3. Step 3 (brute-force): 10 failed attempts — no lockout, no CAPTCHA. Counter stored in cookie `failedLogins=10`; deleting the cookie resets to 0. Brute-force fully possible (CWE-307).
4. Step 13 (multistage): Stage 2 (password) accepts the same username from stage 1 — but only from a hidden form field. Modifying the hidden field to a different username while keeping valid stage-1 data results in authentication as the hidden-field username — cross-stage identity substitution confirmed.
5. Step 5 (credential transmission): Login page loaded over HTTP, submitted over HTTPS — man-in-the-middle attack surface for form action modification.
Output: 4 findings (2 High, 1 Critical for stage-skip, 1 Medium), structured report with CWE mapping and countermeasures.

---

**Scenario: White-box security code review of a Node.js Express application**
Trigger: "Review our auth code before it goes to production. We're worried about the login and password reset."
Process:
1. Grep codebase for `password`, `bcrypt`, `hash`, `md5`, `sha1` — finds `crypto.createHash('md5').update(password).digest('hex')` in the user model. MD5 without salt confirmed (CWE-916).
2. Read forgotten password handler: generates a reset token as `Math.random()` — not cryptographically random, predictable token sequence (CWE-340, related to CWE-640).
3. Read login handler: `try { const user = await User.findOne({username, password: md5(password)}); res.json({success: true}); } catch(e) { res.json({success: true}); }` — fail-open: any exception during login returns success (CWE-287).
4. Read password change function: accessible without checking session authentication cookie — unauthenticated password change possible.
Output: 4 findings including 1 Critical (fail-open login), 1 High (unauthenticated password change), 1 High (MD5 unsalted storage), 1 Medium (predictable reset token).

---

**Scenario: Assessment of a forgotten password mechanism**
Trigger: "We're getting reports that users are being locked out of their accounts. Can you check if there's a security issue with our password reset flow?"
Process:
1. Walk through forgotten password flow with a test account: username → secret question → answer → password reset link emailed.
2. Step 7: Challenge brute-force — submit 50 incorrect answers to the security question with no lockout triggered. Security question is "What is your mother's maiden name?" — small answer space, publicly discoverable (CWE-640).
3. Inspect the recovery URL in the email: `https://app.example.com/reset?token=1738241` — sequential numeric token. Register two consecutive accounts, observe tokens 1738239 and 1738241, infer token 1738240 was issued to another user. Confirmed predictable recovery URL (CWE-340).
4. Test token reuse: recovery URL remains valid after use — an attacker who captures a recovery URL can use it repeatedly to take back control of the account.
Output: 3 findings (2 High, 1 Medium), with countermeasures specifying cryptographically random single-use time-limited recovery URLs and challenge brute-force lockout.

---

## References

- For countermeasure implementation details, see [securing-authentication.md](references/securing-authentication.md)
- For CWE and OWASP mapping per flaw category, see [authentication-cwe-mapping.md](references/authentication-cwe-mapping.md)
- Source: Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook* (2nd ed.), Chapter 6: "Attacking Authentication," pp. 159-201. Wiley.
