---
name: session-management-security-assessment
description: |
  Systematically assess web application session management for security vulnerabilities. Use when testing session token generation quality, cookie security configuration, session fixation susceptibility, cross-site request forgery (CSRF) exposure, or session token handling across a session's full lifecycle. Covers the complete taxonomy of generation weaknesses (meaningful tokens with user data embedded, predictable tokens from concealed sequences or time-dependent algorithms or weak pseudorandom number generators, encrypted tokens vulnerable to ECB block rearrangement or CBC bit-flipping) and handling weaknesses (cleartext transmission, token disclosure in server logs or URLs, vulnerable token-to-session mapping, ineffective logout and expiration, client-side hijacking exposure, overly liberal cookie domain or path scope). Use when someone says 'test our session tokens', 'analyze cookie security', 'check for session fixation', 'verify CSRF protection', 'assess token predictability', 'evaluate our session management', 'can session tokens be guessed', 'review logout implementation', 'check cookie flags', or 'audit session security'. Produces a structured vulnerability report with per-weakness findings and remediation guidance. Framed for authorized security testing, defensive security assessment, and educational contexts.
model: sonnet
context: 1M
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code, HTTP traffic captures, server configuration, security scan reports"
    - type: none
      description: "Can also operate from live application access in an authorized test environment"
  tools-required: [Read, TodoWrite]
  tools-optional: [Grep, Bash, WebFetch]
  environment: "Authorized penetration test or security assessment environment; codebase or HTTP proxy history preferred"
---

# Session Management Security Assessment

## When to Use

Use this skill when you are conducting an **authorized security assessment** of a web application's session management mechanism. Applicable contexts:

- **Penetration testing** — systematically finding exploitable session weaknesses before an attacker does
- **Security code review** — evaluating session token generation logic, cookie configuration, and lifecycle management in source code
- **Security architecture review** — assessing whether the session design meets security requirements before deployment
- **Vulnerability verification** — confirming or ruling out reported session issues with structured test evidence

This skill covers two orthogonal vulnerability classes: weaknesses in how tokens are **generated** (can an attacker predict or derive tokens issued to other users?) and weaknesses in how tokens are **handled** after generation (can an attacker obtain or misuse tokens through network capture, log access, fixation, or client-side attacks?).

**Preconditions:** You have at least one of:
- Source code including session token generation logic
- HTTP proxy history from an authenticated walkthrough of the application
- Live authorized access to a test instance of the application

**Agent:** This assessment requires authorized access. Confirm scope authorization before beginning any active testing steps. Do not perform active token capture or manipulation against systems you are not authorized to test.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Extract: application under test, scope authorization, available artifacts
                    ↓
Environment → Scan for: source files, HTTP logs, config files, cookie headers
                    ↓
Gap analysis → Do I know WHAT to test and DO I have authorized access?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time)
                    │
                    NO
                    ↓
         Confirm authorization → PROCEED with systematic assessment
```

### Required Context (must have — ask if missing)

- **Authorization confirmation:** Is this assessment authorized? Who authorized it and for which systems?
  → Without this, do not proceed with active testing steps.

- **Application identity:** Which application or endpoint is being assessed?
  → Check prompt for: URL, application name, repository path, or system description.

- **Available artifacts:** What artifacts are available — source code, HTTP proxy history, live access?
  → This determines which assessment steps can be performed with full confidence vs inferred.

### Observable Context (gather from environment)

- **Session token location:** How is the session token transmitted? Cookie, URL parameter, hidden form field, custom header?
  → Grep for: `Set-Cookie`, `sessionId`, `jsessionid`, `PHPSESSID`, `ASP.NET_SessionId`, `token=` in URL patterns
  → WHY: The transmission mechanism determines which handling weakness tests apply (e.g., URL transmission exposes to log disclosure; cookies expose to scope and flag issues).

- **Token generation code:** Where and how are tokens generated?
  → Grep for: `Random`, `SecureRandom`, `uuid`, `session_start`, `generateToken`, `Math.random`, `rand()`
  → WHY: Generation code reveals whether the source of entropy is cryptographically secure.

- **Cookie attributes:** What flags are set on session cookies?
  → Grep for: `Secure`, `HttpOnly`, `SameSite`, `domain=`, `path=` in `Set-Cookie` headers or config
  → WHY: Missing `Secure` flag allows cleartext transmission; missing `HttpOnly` enables JavaScript access; overly broad `domain=` widens attack surface.

- **Session lifecycle code:** How are sessions created, refreshed, and destroyed?
  → Grep for: login handlers, logout endpoints, session invalidation calls (`session.invalidate()`, `session_destroy()`, `Session.Abandon()`)
  → WHY: Lifecycle gaps (no token rotation on login, no server-side invalidation on logout) are independent of token strength.

### Default Assumptions

- If transport protocol is not confirmed: assume mixed HTTP/HTTPS until verified — do not assume HTTPS everywhere without checking.
- If cookie flags are not visible: assume absent until confirmed present in `Set-Cookie` response headers.
- If logout implementation is unclear: test server-side invalidation explicitly — client-side cookie deletion is not sufficient.

## Process

Use `TodoWrite` to track assessment steps before beginning.

```
TodoWrite([
  { id: "1", content: "Identify session token(s) and transmission mechanism", status: "pending" },
  { id: "2", content: "Assess token generation: meaningful token analysis", status: "pending" },
  { id: "3", content: "Assess token generation: predictability analysis (concealed sequences, time dependency, weak PRNG)", status: "pending" },
  { id: "4", content: "Assess token generation: encrypted token analysis (ECB block rearrangement, CBC bit-flipping)", status: "pending" },
  { id: "5", content: "Run statistical randomness analysis via Burp Sequencer protocol", status: "pending" },
  { id: "6", content: "Assess token handling: network disclosure (HTTPS coverage, Secure flag, HTTP downgrade paths)", status: "pending" },
  { id: "7", content: "Assess token handling: log disclosure (URL-based tokens, admin monitoring exposure)", status: "pending" },
  { id: "8", content: "Assess token handling: token-to-session mapping (concurrent sessions, static tokens)", status: "pending" },
  { id: "9", content: "Assess token handling: session termination (expiration timeout, logout server-side invalidation)", status: "pending" },
  { id: "10", content: "Assess token handling: session fixation (4 test cases)", status: "pending" },
  { id: "11", content: "Assess token handling: CSRF exposure", status: "pending" },
  { id: "12", content: "Assess token handling: cookie scope (domain and path attributes)", status: "pending" },
  { id: "13", content: "Compile findings report with severity ratings and remediation", status: "pending" }
])
```

---

### Step 1: Identify Session Tokens and Transmission Mechanism

**ACTION:** Identify every item of data that functions as a session token. Do not assume the standard platform cookie is the only token — applications often use multiple items across cookies, URL parameters, and hidden form fields. Confirm which items are actually validated by the server for session state.

**WHY:** Applications may employ several items collectively as a token, using different components for different back-end subsystems. The standard session cookie generated by the web server may be present but not actually used. Additionally, an item that appears to be a session token may be ignored by the server, meaning its modification would go undetected — a finding in itself. Narrowing the actual validated components reduces wasted analysis effort on inert data.

**Detection method:**
1. Walk through the application from the start URL through the login function. Note every new item passed to the browser.
2. Find a page that is definitively session-dependent (e.g., "My Account" or "My Details") — one that returns content specific to the authenticated user.
3. Make repeated requests to that page, systematically removing each suspected token item. If removing an item causes the session-dependent content to disappear or redirect to login, the item is confirmed as a session token.
4. Use Burp Repeater or equivalent to perform this systematically.

**Also check for alternatives to sessions:**
- If token-like items are 100+ bytes, re-issued on every request, and appear encrypted or signed, the application may use sessionless state (transmitting all session data client-side). These require different testing — check for integrity protection and replay resistance rather than token prediction.
- If the application uses HTTP Basic/Digest/NTLM authentication without session cookies, session management attacks may not apply.

Mark Step 1 complete in TodoWrite.

---

### Step 2: Assess Token Generation — Meaningful Tokens

**ACTION:** Determine whether session tokens encode user-identifiable or predictable information (username, email, user ID, role, timestamp, IP address) in raw, encoded, or obfuscated form.

**WHY:** A token that encodes the username — even if hex-encoded or Base64-encoded — allows an attacker to construct valid tokens for any known user without interacting with the server. The apparent complexity of the token string is irrelevant if the underlying data is structured and user-specific.

**Test procedure:**
1. Obtain tokens for multiple different users by logging in with different accounts (use accounts with similar but slightly varying usernames: A, AA, AAA, AAAB, etc., to isolate the username component in the token).
2. Apply progressive decodings to each token and its components: hex decode → Base64 decode → XOR decode. Look for recognizable strings (usernames, email patterns, dates).
3. Look for structural indicators: only hexadecimal characters (possible hex encoding of ASCII), trailing `=` signs or charset `a-z A-Z 0-9 +/` (Base64 signatures), repeated character sequences matching username length.
4. Analyze correlations: do tokens for similar usernames share substrings? Does the token length vary with username length?
5. If tokens appear structured (delimiter-separated components), analyze each component independently. Some components may be random while others are meaningful.

**If meaning is found:**
- Determine whether the meaningful component is actually validated by the server (Step 1 procedure: modify that component and verify rejection).
- If validated: the application is directly vulnerable — an attacker can enumerate valid tokens for known usernames.
- If not validated: the component is decorative padding; remove it from further analysis.

Mark Step 2 complete in TodoWrite.

---

### Step 3: Assess Token Generation — Predictability

**ACTION:** Assess whether token values follow sequences that allow extrapolation to other users' tokens, even when the tokens do not contain meaningful user data. Investigate three predictability sources: concealed sequences, time dependency, and weak pseudorandom number generator (PRNG) output.

**WHY:** A token without meaningful user data can still be predictable if it follows an arithmetic sequence or is derived from observable inputs like the current time. An attacker who obtains a sample of tokens can reverse-engineer the generation algorithm and construct tokens issued to other users — without needing any user-specific information.

**3a. Concealed Sequences**

Tokens may appear random in raw form but reveal arithmetic sequences after decoding. Test:
1. Collect 10–20 consecutive tokens by rapidly triggering new session creation.
2. Apply decodings (Base64, hex) to each token and each structural component.
3. If the decoded output is binary, render as hexadecimal integers and compute differences between successive values.
4. Look for a repeating difference — this reveals the increment constant of the generation algorithm.
5. Once the constant is known, the full token sequence (past and future) is reconstructable.

**3b. Time Dependency**

Some token generation algorithms incorporate the current time (epoch milliseconds, microseconds) as a primary input. Test:
1. Collect two batches of tokens separated by a known time interval (e.g., 5–10 minutes apart).
2. In each batch, identify any component that increases monotonically but in variable increments.
3. Compare the difference between the last value of the first batch and the first value of the second batch. If the jump is consistent with the elapsed time (e.g., ~540,000 units in 9 minutes implies milliseconds), the component is time-based.
4. If source code is available, look for `System.currentTimeMillis()`, `time()`, `microtime()`, `Date.now()`, or similar time sources used in token construction.
5. Time-based components are brute-forceable: the range of valid values for a given user's token is bounded by the window of time around the user's login.

**3c. Weak PRNG**

Linear congruential generators (LCGs), `Math.random()`, `java.util.Random`, PHP's `rand()`, and similar non-cryptographic PRNGs produce sequences that are fully predictable from a small sample of output values. The next value (and all previous values) can be derived algebraically. Test:
1. If source code is available, check what randomness source is used: `SecureRandom`, `os.urandom`, `/dev/urandom`, `CryptGenRandom` are strong. `Random`, `Math.random()`, `rand()`, `mt_rand()` are weak.
2. If source code is unavailable, use Burp Sequencer statistical analysis (see Step 5) to measure effective entropy — weak PRNGs fail at many bit positions even when individual tokens appear visually random.
3. Check whether multiple PRNG outputs are concatenated to form a longer token. This is a common misconception: it does not increase entropy beyond the PRNG's internal state size, and may make state reconstruction easier by providing more sample values.

Mark Step 3 complete in TodoWrite.

---

### Step 4: Assess Token Generation — Encrypted Tokens

**ACTION:** Determine whether tokens are encrypted containers for meaningful data, and if so, test for ECB block rearrangement and CBC bit-flipping vulnerabilities.

**WHY:** Applications that encrypt meaningful session data (user ID, role, username) before issuing it as a token assume that encryption prevents tampering. This assumption fails for ECB ciphers (where ciphertext blocks can be rearranged to produce a different plaintext without knowing the key) and CBC ciphers (where bit-flipping a ciphertext byte produces predictable, controlled changes in the subsequent decrypted block).

**Detection — is a block cipher being used?**
1. Register accounts with usernames of increasing length (e.g., 1 character, 2 characters, etc., up to 20+ characters).
2. Monitor session token length. If the token length jumps by 8 or 16 bytes at a specific username length, a block cipher with 64-bit or 128-bit blocks is likely in use (8 bytes = 64-bit block cipher such as DES, 3DES; 16 bytes = 128-bit block cipher such as AES).
3. Confirm by continuing to add characters and observing the same jump occurring again 8 or 16 characters later.

**ECB mode test:**
1. ECB encrypts identical plaintext blocks into identical ciphertext blocks. Rearranging ciphertext blocks causes the corresponding plaintext blocks to be rearranged.
2. Register usernames specifically crafted so that one block of the username (at a known offset) aligns with a block containing a high-privilege field (e.g., UID or role field) in the token plaintext.
3. Duplicate that ciphertext block and insert it at the position of the target field.
4. Submit the modified token. If the application processes the request in the security context of a different user (or with elevated privileges), the ECB rearrangement attack succeeded.
5. Blind approach (no source code): try duplicating and moving ciphertext blocks, observing whether you remain logged in as yourself, become a different user, or are rejected.

**CBC mode test (bit-flipping):**
1. CBC decryption: flipping a bit in ciphertext block N corrupts block N entirely during decryption (renders it as garbage) but causes a predictable, controlled bit-flip in the corresponding position of block N+1's plaintext.
2. Use Burp Intruder's "bit flipper" payload type on the session token (treating it as ASCII hex). This generates ~8 requests per byte of token data — efficient for coverage.
3. Monitor responses for: (a) continued valid session but with a different user identity displayed (bit-flip hit a UID or role field in the following block), or (b) responses that indicate the application is processing corrupted but accepted token data.
4. When a bit-flip causes user context to change: perform a focused attack on that block position, iterating through a wider range of values to reach a target user ID or role.
5. Note: if the application rejects tokens containing invalid field values (e.g., non-numeric UID), the attack may be impractical. If the application only validates certain fields (e.g., only the UID), the attack targets those fields.

Mark Step 4 complete in TodoWrite.

---

### Step 5: Statistical Randomness Analysis — Burp Sequencer Protocol

**ACTION:** Run a structured statistical randomness test on the session token to quantify effective entropy in bits. This is the authoritative test for token generation quality when visual inspection or manual decoding does not reveal a pattern.

**WHY:** A token that passes visual inspection and manual analysis may still fail formal statistical randomness tests. Conversely, a token that fails statistical tests may not be practically predictable if the failing bits are sparse across many positions. The key metric is effective entropy (bits of the token that pass randomness tests): a 50-bit token with 50 random bits is equivalent to a 1,000-bit token with only 50 random bits.

**Collection protocol:**
1. Identify the request that issues a new session token (typically: `GET /` unauthenticated, or `POST /login` after authentication). Send this request to Burp Sequencer via the context menu.
2. Configure Sequencer: select the cookie name or form field containing the session token; set boundary markers if using manual selection.
3. Enable "auto analyse" to trigger analysis at intervals.
4. **Sample size milestones:**
   - 100 tokens: minimum for any analysis. Collect before reviewing results in detail.
   - 500 tokens: sufficient to detect clear failures. If analysis at this point shows convincing failures, no need to continue.
   - 5,000 tokens: adequate for most assessments; tokens that pass here are unlikely to be practically predictable.
   - 20,000 tokens: required for full FIPS 140-2 compliance testing. Maximum sample size Burp Sequencer supports.
5. If source IP or username influences token generation, repeat token collection from a different IP address and/or username and compare results to isolate IP/username as an entropy source.

**Interpreting Burp Sequencer results:**
- **Effective entropy (bits):** The headline result. Values below 64 bits indicate weakness for most application contexts; below 32 bits is critically weak.
- **FIPS test results:** Six standardized tests (monobit, poker, runs, long runs, serial correlation, spectral). Failing multiple FIPS tests at many bit positions indicates structural non-randomness.
- **Character-level vs bit-level analysis:** Burp tests at both levels. Large structured portions of a token (e.g., a fixed prefix, a user ID field) are not random — this is expected and not a vulnerability in itself. What matters is whether the random portion provides sufficient entropy.

**Important caveats:**
- A token generated by a weak but algorithmically deterministic PRNG (e.g., a linear congruential generator) may pass all statistical tests while being fully predictable from a small sample. Statistical tests measure distribution, not algorithmic predictability.
- A token that fails statistical tests at a few bit positions may not be practically exploitable if the failure involves only a small number of bits that an attacker would need to simultaneously predict correctly.

Mark Step 5 complete in TodoWrite.

---

### Step 6: Assess Token Handling — Network Disclosure

**ACTION:** Verify that session tokens are never transmitted in cleartext over unencrypted HTTP, and that cookie `Secure` flags are correctly set to enforce this.

**WHY:** A network eavesdropper positioned at any point between client and server — the user's local network, corporate network, ISP, hosting provider — can capture cleartext HTTP traffic. A captured session token grants full session access without knowing user credentials. Even applications that use HTTPS for most content frequently have specific paths (static assets, pre-authentication pages, login forms that accept HTTP) that leak the session token.

**Test procedure:**
1. Walk through the complete application lifecycle: unauthenticated access (start URL), login process, all authenticated functionality. Record every URL and every instance in which a new session token is received or existing token is transmitted. Use Burp Proxy HTTP history for this.
2. Check `Set-Cookie` headers for the `Secure` flag. If `Secure` is absent, the browser will transmit the cookie over HTTP to any path/domain match, including unencrypted requests.
3. Verify whether the application switches from HTTP to HTTPS at any point. If it does:
   a. Check whether a session token issued before the HTTPS switch is reused in the authenticated session (pre-authentication token reuse).
   b. Verify whether the application also accepts login over plain HTTP if the login URL is accessed directly with `http://` instead of `https://`.
4. Even if HTTPS is used everywhere for the application itself: verify whether the server also listens on port 80. If so, visit any authenticated page URL using `http://` and check whether the token is transmitted.
5. If any static content (images, scripts, stylesheets) is loaded over HTTP from within an HTTPS-delivered page, the session cookie is transmitted with those HTTP requests (no `Secure` flag) or the browser warns (mixed content). Treat either as a vulnerability.
6. If a token for an authenticated session is transmitted over HTTP: verify whether the server immediately invalidates that token upon detecting the insecure transmission. If not, the token remains valid for hijacking.

Mark Step 6 complete in TodoWrite.

---

### Step 7: Assess Token Handling — Log Disclosure

**ACTION:** Identify whether session tokens can be read from system logs, monitoring interfaces, or referrer headers due to token transmission in URLs.

**WHY:** URL-embedded session tokens appear in: web server access logs, browser history, corporate proxy logs, ISP proxy logs, `Referer` headers sent to third-party servers when the user follows an off-site link from within the authenticated session. Log disclosure differs from network disclosure in that it is often accessible to a much wider range of insiders (helpdesk, IT operations, log aggregation system users) and persists across time.

**Test procedure:**
1. Walk through all application functionality and identify any instances where session tokens appear in URL query strings or path components (e.g., `jsessionid=` in the URL path, `token=` in query parameters). Grep for: `inurl:jsessionid`, `?token=`, `?session=` patterns in captured traffic.
2. Identify any administrative, helpdesk, or diagnostic functionality within the application that allows viewing user sessions. Access that functionality with your test account and check whether the actual session token value is displayed. If it is, verify who can access this functionality — anonymous users, any authenticated user, or only administrators.
3. If tokens appear in URLs: attempt to inject an off-site link (via any user-controlled content feature — message boards, profile fields, feedback forms). Monitor the attacker-controlled server's access logs for incoming `Referer` headers containing session tokens from other users.

Mark Step 7 complete in TodoWrite.

---

### Step 8: Assess Token Handling — Vulnerable Token-to-Session Mapping

**ACTION:** Test whether the application correctly maps tokens to sessions, preventing concurrent session abuse and static token reuse.

**WHY:** Even a cryptographically strong token is useless as a security control if the application accepts multiple concurrent valid tokens for the same user, or issues the same token on every login ("static tokens"). Concurrent sessions allow an attacker who has obtained credentials to use a captured token undetected while the legitimate user is also logged in. Static tokens are permanent access credentials, not sessions — compromising them compromises the account permanently.

**Test procedure:**
1. **Concurrent session test:** Log in to the application twice simultaneously using the same user account, from different browser processes or machines. Determine whether both sessions remain active concurrently. If yes: concurrent sessions are permitted. An attacker who has compromised credentials can use them without triggering a conflict.
2. **Static token test:** Log in and log out of the same account multiple times, from different browser processes or machines. Record the session token issued on each login. If the same token is issued on every login: the application is using static tokens. These are not sessions in the security sense — they function as permanent credentials.
3. **Segmented token test (structured tokens only):** If tokens contain both user-identifying components and apparently random components, modify the user-identifying component to refer to a different known user while submitting any valid random component. If the server accepts the modified token and processes the request in the context of the different user: the application has a fundamental token-to-session mapping vulnerability (the user context is determined by user-supplied data outside the session).

Mark Step 8 complete in TodoWrite.

---

### Step 9: Assess Token Handling — Session Termination

**ACTION:** Verify that sessions expire after an appropriate inactivity timeout and that logout actually invalidates the session on the server side.

**WHY:** A long-lived session token extends the attack window — if a token is captured or guessed, it remains valid for use. A logout function that only deletes the browser cookie without invalidating the server-side session is functionally equivalent to no logout: anyone who captured the token before logout can still use it indefinitely. Client-side cookie blanking is not server-side invalidation.

**Test procedure:**
1. **Inactivity timeout test:**
   a. Log in and obtain a valid session token.
   b. Wait for the intended inactivity period without making any requests (e.g., 10–30 minutes, depending on the application's stated policy).
   c. Submit a request for a protected page using the token.
   d. If the page renders normally: the inactivity timeout is not enforced or is longer than expected.
   e. Use Burp Intruder to automate: configure increasing time intervals between successive requests using the same token to find the timeout boundary.
2. **Logout invalidation test:**
   a. Log in and record a session-dependent request (e.g., GET to "My Account") in Burp Proxy history.
   b. Perform the logout action in the application.
   c. Send the recorded session-dependent request again using the pre-logout token (via Burp Repeater).
   d. If the session-dependent page renders successfully: the logout did not invalidate the server-side session.
3. **Client-side vs server-side test:** Examine what the logout response actually does: does it issue a `Set-Cookie` with a blank or expired token value (client-side only), or does it call a server-side invalidation function? Source code review is definitive. If no source code: the Repeater test in step 2 is authoritative.

Mark Step 9 complete in TodoWrite.

---

### Step 10: Assess Token Handling — Session Fixation

**ACTION:** Test four specific scenarios that determine whether an attacker can fix a known token value for a victim, then escalate to authenticated access after the victim logs in.

**WHY:** Session fixation attacks are possible when an application accepts tokens that it did not itself issue, or when it reuses pre-authentication tokens as post-authentication tokens. The attacker supplies a token to the victim (via URL parameter, cookie injection, or simply knowing the format), the victim logs in, and the attacker then uses the known token to access the victim's authenticated session.

**Test procedure — four test cases:**

1. **Pre-authentication token reuse:** If the application issues session tokens to unauthenticated users (e.g., to track anonymous shopping carts), obtain an unauthenticated token and perform a login. If the application does not issue a new token after successful authentication: it is vulnerable. An attacker can obtain an anonymous token, force the victim to use it (URL fixation), and after the victim logs in, use the same token.

2. **Return-to-login token reuse:** Log in to obtain an authenticated token. Return to the login page. If the application serves the login page without issuing a new token (the existing authenticated token is still active): log in again as a different user using the same token. If the application does not issue a new token on the second login: it is vulnerable to fixation between accounts.

3. **Attacker-supplied token acceptance:** Identify the format of valid tokens (from Step 1). Construct a token that conforms to the format (correct length, character set) but is an invented value the application did not issue. Attempt to log in while submitting this invented token in the expected location. If the application creates an authenticated session tied to the invented token: the application accepts attacker-supplied tokens, enabling fixation.

4. **Sensitive data fixation (non-login applications):** If the application does not use authentication but processes sensitive user data (e.g., payment forms, personal details), apply test cases 1 and 3 in relation to the pages that display submitted sensitive data. If a token set during anonymous usage can be used by another party to retrieve that user's sensitive data: the application is vulnerable to fixation against non-authenticated sensitive operations.

**Cross-site request forgery (CSRF) check:**
If the application transmits session tokens via cookies: confirm whether it is protected against CSRF.
1. Log in to the application and identify state-changing operations whose parameters an attacker could determine in advance (fund transfers, password changes, data deletions).
2. From a different browser tab or window in the same browser process, construct a request to that operation (via a crafted form or link) that would originate from a page on a different domain.
3. If the application processes the cross-origin request and executes the state change: it is vulnerable to CSRF. The browser submits the cookie automatically regardless of the request origin.
4. Check for CSRF tokens: does the application include a per-request unpredictable token in a hidden form field or custom header that the server validates? If the application relies solely on cookies and has no CSRF token: assume vulnerable.

Mark Step 10 complete in TodoWrite.

---

### Step 11: Assess Token Handling — Cookie Scope

**ACTION:** Review all `Set-Cookie` response headers for `domain` and `path` attributes. Determine whether cookie scope is more permissive than necessary, exposing session tokens to other applications or subdomains.

**WHY:** A cookie scoped to `wahh-organization.com` is submitted to every subdomain of that organization — including test environments, staging systems, and other applications that may have lower security standards or be accessible to different personnel. A cross-site scripting vulnerability in any application within the cookie's scope can steal tokens from the main application. Cookie scope is often configured at the platform level (web server defaults) rather than by application developers, so it may be unnecessarily broad.

**Test procedure:**
1. Review all `Set-Cookie` headers issued by the application across the full application walkthrough. Note the `domain` and `path` values for session token cookies.
2. If `domain` is set: it is more permissive than the default (which scopes cookies to the exact hostname). Identify all subdomains and applications within the specified domain. Any of these can receive the session cookie.
3. If no `domain` is set: by default, the browser scopes the cookie to the exact hostname. However, subdomains still receive the cookie (e.g., a cookie set by `app.example.com` with no domain attribute is still sent to `app.example.com`, not to `other.example.com`, but default behavior differs by browser implementation — verify).
4. If `path` is set to `/` or a broad path: path-based scope restriction provides no meaningful security separation between applications at different URL paths on the same hostname. Client-side JavaScript at any path on the same origin can read cookies regardless of `path` attribute.
5. Identify all web applications accessible via the domains that will receive the session cookie. Assess their security posture — a stored cross-site scripting vulnerability in any of them could steal tokens from the primary application.

Mark Step 11 complete in TodoWrite.

---

### Step 12: Compile Findings Report

**ACTION:** Consolidate all findings from Steps 2–11 into a structured vulnerability report with severity ratings and remediation guidance.

**WHY:** A finding without remediation guidance is incomplete. Each vulnerability class has a corresponding countermeasure; mapping findings to remediations allows the development team to act without additional research.

**HANDOFF TO HUMAN** — the agent produces the report; the security team or development team prioritizes and implements remediations.

**Report format:**

```markdown
# Session Management Security Assessment Report

## Assessment Scope
[Application name, test date, authorization basis, artifacts reviewed]

## Session Token Identification
[Which items function as session tokens, transmission mechanism, alternatives-to-sessions assessment]

## Part 1: Token Generation Weaknesses

### G1: Meaningful Token Content
**Finding:** [Present / Not detected]
**Evidence:** [Decoded token values, correlation with user data]
**Severity:** [Critical if exploitable | Informational if not validated by server]
**Remediation:** Tokens should be opaque server-generated identifiers. Move all session data to server-side session storage. Never encode user-identifiable data in tokens.

### G2: Predictable Token Sequences
**Finding:** [Present / Not detected — specify: concealed sequence / time dependency / weak PRNG]
**Evidence:** [Sample tokens, decoded sequences, difference analysis, PRNG identification]
**Severity:** [Critical if directly exploitable | High if requires timing correlation]
**Remediation:** Use a cryptographically secure PRNG (CSPRNG) seeded from a high-entropy source (e.g., `SecureRandom`, `os.urandom`, `CryptGenRandom`). Do not use time as a primary entropy source. Do not use linear congruential generators.

### G3: Encrypted Token Vulnerabilities
**Finding:** [ECB block rearrangement / CBC bit-flipping / Not detected]
**Evidence:** [Block cipher detection evidence, manipulation results]
**Severity:** [High — privilege escalation or cross-user access]
**Remediation:** Tokens should not encode sensitive data at all. If encrypted tokens are required, use authenticated encryption (AES-GCM, ChaCha20-Poly1305) to detect any ciphertext modification. Do not use ECB mode. Verify that the entire ciphertext is authenticated before processing any field.

### G4: Statistical Entropy Assessment (Burp Sequencer)
**Finding:** [Effective entropy: X bits. FIPS tests: passed/failed. Notable failures: ...]
**Severity:** [Critical if < 32 bits effective | High if < 64 bits | Low if >= 128 bits]
**Remediation:** Target >= 128 bits of effective entropy. Use platform-provided session management (mature frameworks implement this correctly) rather than custom token generation.

## Part 2: Token Handling Weaknesses

### H1: Network Disclosure
**Finding:** [Cleartext transmission detected / Secure flag absent / HTTP downgrade path found / Not detected]
**Remediation:** Transmit tokens exclusively over HTTPS. Set `Secure` flag on all session cookies. Use HSTS. Redirect HTTP to HTTPS and invalidate any token transmitted over HTTP. Issue a fresh token after the HTTP-to-HTTPS transition.

### H2: Log Disclosure
**Finding:** [Token in URL / Admin monitoring exposes token / Not detected]
**Remediation:** Never transmit session tokens in URL query strings or path components. Use POST for token submission or store in cookies. Administrative monitoring functions should display session metadata (user ID, IP, login time) without exposing the token value itself.

### H3: Vulnerable Token-to-Session Mapping
**Finding:** [Concurrent sessions permitted / Static tokens / Segmented token vulnerability / Not detected]
**Remediation:** Issue a unique token per session. Invalidate all existing sessions when a new login occurs (or alert the user of concurrent access). Never reissue the same token to the same user across separate login events.

### H4: Vulnerable Session Termination
**Finding:** [No inactivity timeout / Logout does not invalidate server-side / Client-side-only cookie deletion / Not detected]
**Remediation:** Implement server-side session invalidation on logout that disposes of all session resources and marks the token as invalid. Implement server-side inactivity timeout (10–30 minutes is typical; match business requirements). Do not rely on client-side cookie deletion as the primary termination mechanism.

### H5: Session Fixation
**Finding:** [Pre-authentication token reused / Return-to-login reuse / Attacker-supplied token accepted / Sensitive data fixation / Not detected]
**Remediation:** Issue a fresh session token immediately after successful authentication. Reject tokens that the server did not itself generate. For non-authenticated sensitive data flows, create a new session at the start of the sensitive data sequence.

### H6: Cross-Site Request Forgery
**Finding:** [Vulnerable — state-changing operations accept cross-origin requests without CSRF token / Not detected]
**Remediation:** Implement per-request CSRF tokens in hidden form fields. Validate the CSRF token on every state-changing request. Consider using the `SameSite=Strict` or `SameSite=Lax` cookie attribute. Require re-authentication before critical operations (fund transfers, password changes).

### H7: Overly Liberal Cookie Scope
**Finding:** [Domain attribute broadens scope to: [list domains] / Path attribute is ineffective for security isolation / Not detected]
**Remediation:** Do not set `domain` attribute unless required — the default (exact hostname) is more restrictive. If subdomains must receive the cookie, audit every subdomain for cross-site scripting and other vulnerabilities. Set cookie scope as restrictively as feasible. Prefer `HttpOnly` to reduce JavaScript access.

## Summary

| # | Weakness | Severity | Status |
|---|----------|----------|--------|
| G1 | Meaningful token content | | |
| G2 | Predictable sequences | | |
| G3 | Encrypted token vulnerability | | |
| G4 | Insufficient entropy | | |
| H1 | Network disclosure | | |
| H2 | Log disclosure | | |
| H3 | Token-to-session mapping | | |
| H4 | Session termination | | |
| H5 | Session fixation | | |
| H6 | CSRF | | |
| H7 | Cookie scope | | |

**Priority remediations:**
1. [Most critical — typically: token generation or network disclosure]
2. [Second priority]
3. [Third priority]

**Positive findings:** [Aspects confirmed secure]
```

Mark Step 12 complete in TodoWrite.

## Key Principles

- **Token generation and token handling are independent failure dimensions.** A cryptographically strong token can still be stolen via network interception, log exposure, or session fixation. A token that is never disclosed can still be useless as a security control if the session lifecycle is broken. Assess both dimensions fully, not just whichever is easier.

- **Statistical randomness tests do not prove cryptographic security.** A deterministic algorithm (linear congruential generator, hash of sequential counter) can produce output that passes all FIPS statistical tests while being perfectly predictable by an attacker who knows the algorithm. Effective entropy is a necessary condition, not a sufficient one. Always investigate the generation algorithm in source code when available.

- **Passing visual inspection is not passing a security test.** Session tokens that "look random" to the eye have repeatedly proven predictable under analysis. Structured statistical analysis (Burp Sequencer at 500+ tokens) and algorithmic analysis (source code review) are required for a defensible assessment.

- **The Secure flag and HTTPS coverage must both be confirmed.** An application that uses HTTPS for all its own pages but loads a single static resource over HTTP exposes the session cookie to network capture on that one HTTP request. Coverage must be total, not partial.

- **Server-side invalidation is the only valid form of logout.** Any logout implementation that relies solely on the client deleting its cookie provides no security against an attacker who has already captured the token. Test logout by replaying a captured pre-logout request after the logout action.

- **Cookie scope is often set at the platform level, not the application level.** Platform defaults may scope cookies to a parent domain across all subdomains. The developer may be unaware. Always check `domain` and `path` attributes explicitly in the `Set-Cookie` response headers, not in application code.

- **Encrypted tokens are not safe from tampering without authentication.** ECB mode allows block rearrangement without decryption. CBC mode allows controlled plaintext modification without decryption. Only authenticated encryption (AEAD) prevents ciphertext manipulation. If tokens must encrypt meaningful data, AES-GCM with verification of the authentication tag before any field is processed is the minimum acceptable approach.

## Examples

**Scenario: E-commerce application — suspected meaningful token**
Trigger: "Our session tokens look like random hex strings but I want to verify they don't encode user data."
Process:
1. Collect tokens for 5 test accounts: usernames `a`, `aa`, `aaa`, `b`, `testuser@example.com`.
2. Hex-decode each token. Token for `testuser@example.com` decodes to a semicolon-delimited string: `user=testuser@example.com;app=shop;date=2026-04-06`. This is a meaningful token.
3. Verify: modify the `user=` component to a different registered email. Submit to a session-dependent page. Application responds with the other user's account data.
4. Confirmed: meaningful token content, directly exploitable for horizontal privilege escalation across all registered accounts.
Output: Critical G1 finding. Remediation: move to opaque server-generated session identifiers; store all session data server-side.

---

**Scenario: Banking application — logout verification**
Trigger: "Verify whether our logout actually terminates sessions."
Process:
1. Log in, navigate to "My Account" page. Record the GET request in Burp Proxy.
2. Send that GET request to Burp Repeater. Confirm it returns account data.
3. Perform logout action via the application UI.
4. In Burp Repeater, re-send the same GET request with the pre-logout session cookie.
5. Application returns: HTTP 200 with full account data. The session token is still valid after logout.
6. Examine logout response: server issues `Set-Cookie: sessionId=; expires=Thu, 01 Jan 1970 00:00:00 GMT` — a client-side cookie deletion only. No server-side invalidation call occurs.
Output: High H4 finding. Remediation: implement server-side session invalidation on logout; store session state on server with explicit invalidation on logout request.

---

**Scenario: Internal application — Burp Sequencer entropy assessment**
Trigger: "Custom session token generation was built in-house using Java. Assess token quality."
Process:
1. Identify the login POST endpoint as the token issuance point. Send to Burp Sequencer, configure for the `sessionId` cookie.
2. Collect 100 tokens: preliminary analysis shows effective entropy ~32 bits. Several FIPS tests fail at low bit positions.
3. Collect 500 tokens: entropy estimate stabilizes at 28 bits. FIPS monobit and runs tests fail at positions 0–6.
4. Source code review (available): `String sessId = Integer.toString(s_SessionIndex++) + "-" + System.currentTimeMillis();` — a sequential counter concatenated with epoch milliseconds. The counter is the primary failure cause; milliseconds provide only limited additional entropy during busy periods.
5. Confirmed: time-dependent sequential generation with low effective entropy. G2 and G4 findings.
Output: Critical G2 (time dependency + sequential counter) and Critical G4 (28-bit effective entropy) findings. Remediation: replace with `java.security.SecureRandom` generating 128-bit random tokens; store all session data in a server-side session store keyed by this token.

## References

- For token generation countermeasure implementation details, see [references/securing-session-management.md](references/securing-session-management.md)
- For cookie attribute reference and browser behavior matrix, see [references/cookie-security-attributes.md](references/cookie-security-attributes.md)
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- CWE-330: Use of Insufficiently Random Values; CWE-384: Session Fixation; CWE-352: Cross-Site Request Forgery
- Source: *The Web Application Hacker's Handbook*, 2nd ed., Stuttard & Pinto, Chapter 7, pp. 205–255

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Web Application Hackers Handbook by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
