---
name: application-logic-flaw-testing
description: |
  Test web application business logic for vulnerabilities that automated scanners cannot detect. Use this skill when: performing a penetration test or security assessment and automated tools have been run but logic-layer coverage is still needed; testing multistage workflows (checkout, account creation, approval flows, insurance applications) for stage-skipping or cross-stage parameter pollution; probing authentication and password-change functions for parameter-removal bypasses (deleting existingPassword to impersonate an admin); testing numeric business limits for negative-number bypass (submitting -$20,000 to avoid approval thresholds); probing discount or pricing logic for timing flaws (add items to qualify, remove before payment); investigating whether shared code components allow session object poisoning across unrelated application flows; hunting for encryption oracles where a low-value crypto context can be used to forge high-value tokens; probing search functions that return match counts as side-channel inference oracles; testing for defense interaction flaws where quote-doubling plus length truncation reconstructs an injection payload; checking whether debug error messages expose session tokens or credentials cross-user via static storage; testing race conditions in authentication that cause cross-user session assignment under concurrent login. Logic flaws arise from violated developer assumptions — assumptions that users will follow intended sequences, supply only requested parameters, omit parameters they were not asked for, and not cross-pollinate state between application flows. Each flaw is unique and application-specific, but the 12 attack patterns documented here provide a reusable taxonomy that transfers across application domains. Maps to OWASP Testing Guide (OTG-BUSLOGIC-*), CWE-840 (Business Logic Errors), CWE-841 (Improper Enforcement of Behavioral Workflow), CWE-362 (Race Condition), and OWASP Top 10 A04:2021 (Insecure Design).
version: 1
status: draft
depends-on: []
source-books:
  - id: web-application-hackers-handbook
    title: "The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws"
    authors: ["Dafydd Stuttard", "Marcus Pinto"]
    edition: 2
    chapters: [11]
    pages: "405-429"
tags: [business-logic, logic-flaws, forced-browsing, parameter-removal, race-condition, encryption-oracle, session-poisoning, negative-numbers, discount-timing, defense-interaction, search-oracle, debug-disclosure, penetration-testing, appsec, owasp, cwe-840, cwe-841, cwe-362]
execution:
  tier: 3
  mode: plan-only
  inputs:
    - type: document
      description: "HTTP traffic captures, Burp Suite proxy logs, or prior application mapping output describing multistage workflows, parameter names, and application behavior"
    - type: codebase
      description: "Application source code or design documentation (white-box) — reveals shared components, session handling, and storage class reuse"
  tools-required: [Read, Write]
  tools-optional: [Grep, WebFetch]
  mcps-required: []
  environment: "Authorized security testing context required. Logic flaw testing requires creative adversarial reasoning and manual interaction with a running application; this skill produces a structured test plan, not automated execution."
discovery:
  goal: "Identify exploitable business logic vulnerabilities by probing the 12 canonical flaw patterns; produce a structured findings report with violated assumption, attack vector, business impact, and remediation recommendation for each finding"
  tasks:
    - "Understand the application's intended workflows, user roles, and the assumptions embedded in each"
    - "Map all multistage processes, shared components, and parameter handling across roles"
    - "Apply each of the 12 flaw patterns as a lens against each relevant application area"
    - "Document each finding: flaw pattern, violated assumption, reproduction steps, business impact"
    - "Produce defensive recommendations aligned with the Avoiding Logic Flaws principles"
  audience:
    roles: ["penetration-tester", "application-security-engineer", "security-minded-developer", "bug-bounty-researcher"]
    experience: "intermediate-to-advanced — assumes familiarity with HTTP, web proxies (Burp Suite or equivalent), and how web application sessions and parameters work"
  triggers:
    - "Penetration test scope requires logic-layer coverage beyond what automated scanners provide"
    - "Application implements multistage workflows (e-commerce checkout, insurance application, loan approval)"
    - "Application has multiple user roles that share underlying code components or session objects"
    - "Security assessment of authentication, password change, or account registration functionality"
    - "Code review of shared components that are reused across different security contexts"
    - "OWASP A04:2021 (Insecure Design) findings need to be enumerated"
---

# Application Logic Flaw Testing

## When to Use

Use this skill when you need to discover business logic vulnerabilities that no automated scanner will find. Automated tools identify vulnerabilities with recognizable signatures — SQL injection payloads that produce database errors, cross-site scripting payloads that reflect in responses. Logic flaws have no signature. Each instance is a unique one-off tied to the specific assumptions a development team made when building a particular feature.

Logic flaws arise when a developer reasons: "If A happens, then B must be the case, so I will do C" — and fails to ask "But what if X occurs?" The flaw is not in a library or protocol; it is in the developer's mental model of how users will behave. Testing for logic flaws therefore requires getting inside that mental model, understanding what the developers assumed, and then deliberately violating those assumptions.

This skill applies to authorized penetration tests, appsec audits, and security code reviews. It is not a substitute for legal authorization to test a target application.

---

## Core Concepts

### The Nature of Logic Flaws

Logic flaws differ from injection or authentication vulnerabilities in three critical ways:

- **No common signature.** There is no payload or pattern that reliably indicates a logic flaw. Each instance looks different.
- **Not scanner-detectable.** Automated vulnerability scanners cannot model developer intent. They can only recognize known bad outputs, not absent business rules.
- **Lateral thinking required.** Finding logic flaws demands imagination — the tester must think about what the application was built to prevent, and then think about what the developers forgot to consider.

The defining characteristic of every logic flaw is a **violated assumption**: a condition the developer believed could never occur, which the attacker can deliberately engineer.

### The Assumption Framework

For each area of functionality under test, apply this analytical frame:

1. **What is this feature designed to do?** Understand the intended happy path.
2. **What assumptions does the implementation make?** Look for assumed user behavior: assumed parameter presence/absence, assumed request sequence, assumed value ranges, assumed role segregation.
3. **Which assumptions are user-controllable?** Any assumption that depends on client-side behavior can be violated.
4. **What happens when the assumption is violated?** What does the server do? What business rule breaks?

---

## Process

### Phase 1 — Reconnaissance and Assumption Mapping

**Step 1: Map all multistage workflows.**
Identify every process that spans more than one HTTP request or page: checkout flows, account registration, password change, loan/insurance applications, approval chains. Document the intended sequence and the mechanism by which stages are linked (URL parameters, POST fields, session state).

*Why: Logic flaws concentrate in workflows because developers mentally simulate users following the intended path. Every stage transition is a potential assumption violation point.*

**Step 2: Identify all user roles and shared components.**
Determine what roles exist (anonymous, authenticated user, administrator, underwriter, etc.) and whether any server-side code components are shared across roles. Note any functionality that allows one role to trigger server-side state that another role reads.

*Why: Shared components are the most dangerous logic flaw surface. A component designed for Role A that is reused for Role B often carries assumptions that are valid in one context and exploitable in the other.*

**Step 3: Document all parameters in each workflow.**
For each request in a workflow, record every parameter name and value. Note which parameters are hidden, which are read from session vs. the request, and which differ between user roles performing the same operation.

*Why: Parameter names that differ between roles (e.g., `existingPassword` present for users, absent for admins) reveal assumption-based branching in server logic.*

---

### Phase 2 — Apply the 12 Flaw Pattern Library

Work through each pattern below as a lens. For each pattern, identify which application areas are plausible candidates, then design a targeted test.

---

#### Pattern 1: Encryption Oracle

**Violated assumption:** The encryption algorithm and key used to protect a high-value token are not accessible to users through any other mechanism.

**Test approach:** Identify every location where the application encrypts or decrypts data supplied by or returned to the user. Look for low-value encrypted values (screen name cookies, preference tokens) that use the same algorithm/key as high-value tokens (authentication tokens, session identifiers). Submit a high-value encrypted token in a field expecting a low-value encrypted token. Observe whether the application decrypts and processes it.

**Hack steps:**
- Find all locations where encryption (not hashing) is used. Hashing is one-way; encryption implies a key that the application holds.
- Attempt to substitute any encrypted value found in one context into a field expecting an encrypted value in a different context.
- Cause deliberate errors that reveal decrypted values, or find screens that intentionally display decrypted content.
- Test whether user-controlled plaintext input causes the application to return a corresponding encrypted value (oracle-encrypt path).
- Test whether user-controlled encrypted input causes the application to display the corresponding plaintext (oracle-decrypt path).

**Impact:** Complete authentication bypass. Attacker forges a session token for any user, including administrators.

---

#### Pattern 2: Parameter Removal Bypass

**Violated assumption:** The presence or absence of a parameter in a request reliably indicates the user's role or privilege level.

**Test approach:** For every request in a sensitive workflow, remove each parameter entirely (not just blank it — delete the name/value pair). Observe whether the server's behavior changes. Pay special attention to parameters that differ between roles performing the same function.

**Hack steps:**
- Identify parameters submitted in requests and remove them one at a time.
- Delete the parameter name as well as its value. Submitting an empty string is handled differently from omitting the parameter entirely.
- Remove one parameter per request to isolate which code path each parameter controls.
- For multistage processes, follow through to completion after each removal — some effects only manifest in later stages.

**Impact:** Authentication bypass, privilege escalation, or constraint removal depending on which parameter controls which check.

---

#### Pattern 3: Workflow Stage Skip (Forced Browsing)

**Violated assumption:** Users will always access multistage functions in the intended sequence because the browser presents them in that order.

**Test approach:** Map the intended sequence of a multistage workflow. Attempt to access later stages directly without completing earlier stages. Try accessing stage N+2 from stage N (skip one), accessing the final confirmation step from the first step, and re-accessing early stages after completing later ones.

**Hack steps:**
- Determine whether stages are distinguished by URL, POST parameters, a stage index field, or session state.
- Submit requests for each stage out of sequence. Try skipping individual stages and jumping directly to the final stage.
- Observe error conditions when stages are accessed out of order — debug output often reveals application internals.
- Note that incomplete session state from skipped stages may cause unexpected application behavior worth exploring further.

**Impact:** Payment bypass, authorization bypass, approval bypass — any business rule enforced in a skipped stage is evaded.

---

#### Pattern 4: Cross-Stage Parameter Pollution

**Violated assumption:** Users will only submit the parameters that the HTML form at each stage requests; they will not supply parameters from other stages or roles.

**Test approach:** In a multistage workflow, identify parameters submitted at each stage. During a later stage, additionally submit parameters that belong to an earlier stage (or that belong to a different user role). If the server maintains a shared state object that is updated with any parameter supplied at any stage, out-of-sequence parameters will be accepted and processed.

**Hack steps:**
- Walk through the full workflow as each available user role, capturing all parameters submitted at each stage.
- During each stage, additionally submit parameters from other stages or other roles.
- Observe whether the parameters are accepted and whether they affect downstream application state.
- Test whether parameters exclusive to a privileged role (underwriter decision fields, admin approval flags) can be submitted by a lower-privileged role.

**Impact:** Price manipulation, approval bypass, privilege escalation, cross-site scripting stored against privileged reviewers.

---

#### Pattern 5: Session Object Poisoning

**Violated assumption:** A code component reused across multiple features creates independent session objects in each context; using it in one flow does not affect the session state in another.

**Test approach:** Identify features that allow a user to input data that is stored in the session (registration, profile update, account switch). After completing such a flow, navigate to a completely different area of the application and observe whether the session state accumulated in the first flow affects the second flow's behavior or output.

**Hack steps:**
- In complex applications with horizontal or vertical privilege segregation, look for any instance where a user accumulates session state that relates to identity.
- Use one area of functionality (e.g., registration) to write a target user's identity into your session object.
- Switch to a different area of functionality (e.g., account overview) and observe whether the poisoned session state causes the application to act as the target user.
- This is a black-box test; the application behavior must be observed indirectly through output differences.

**Impact:** Full account takeover — attacker accesses another user's financial data, statements, and transactional functionality.

---

#### Pattern 6: Negative Number Bypass

**Violated assumption:** The value supplied for a quantity or amount will always be positive; the approval threshold check (`amount <= threshold`) will always catch large transfers.

**Test approach:** For any numeric input that controls a business limit, pricing calculation, or approval threshold, submit negative values. Observe whether the server accepts them, how it processes them, and what downstream effect occurs.

**Hack steps:**
- Identify all numeric inputs that are bounded by business rules (transfer amounts, order quantities, discount percentages, insurance values).
- Submit negative values and observe whether they pass validation.
- Understand what the negative value means semantically to the application — a negative transfer is often processed as a transfer in the opposite direction.
- Consider multi-step exploits: engineer a balance state via several transfers that enables extraction.

**Impact:** Financial fraud, approval bypass, inventory manipulation.

---

#### Pattern 7: Discount Timing Flaw

**Violated assumption:** A user who qualifies for a discount at the time of adding items to a cart will purchase all the qualifying items; discount adjustments applied at add-time are final.

**Test approach:** In any application that applies discounts, pricing adjustments, or promotions based on the composition of a user's cart or order, add items to qualify for the adjustment, then remove some qualifying items after the discount has been applied. Observe whether the discount persists on remaining items.

**Hack steps:**
- Understand the algorithm the application uses to determine discount eligibility and the point in the workflow where adjustments are made.
- Determine whether adjustments are made once at add-time or recalculated on every cart change.
- Add qualifying items to trigger a discount, verify the discount is applied, then remove the items you do not want.
- Observe whether the discount persists on the items you retain.

**Impact:** Unauthorized price reductions, financial loss to the application owner.

---

#### Pattern 8: Escape-from-Escaping

**Violated assumption:** Escaping all potentially dangerous metacharacters in user input provides complete protection against injection; the escape character itself is not dangerous.

**Test approach:** When probing for command injection or other metacharacter-sensitive injection points where escaping is applied, prefix each dangerous character with a backslash. If the application escapes the semicolon in `foo;ls` to produce `foo\;ls` but does not also escape the backslash, then input `foo\;ls` will be transformed to `foo\\;ls` — where the shell interpreter treats the first backslash as escaping the second, leaving the semicolon unescaped.

**Hack steps:**
- When testing any input that is sanitized by escaping metacharacters, always try placing a backslash immediately before each metacharacter in your payload.
- Input: `foo\;ls` → after escaping: `foo\\;ls` → shell sees: literal backslash + unescaped semicolon = command injection.
- This same pattern applies to JavaScript string contexts where backslash-escaping of quotes is used as an cross-site scripting defense.

**Impact:** Command injection, cross-site scripting — complete bypass of the escaping defense.

---

#### Pattern 9: Defense Interaction Flaw (Quote-Doubling + Truncation)

**Violated assumption:** Two independently sound defense mechanisms (quote-escaping and length truncation) are still sound when applied in sequence.

**Test approach:** When an application doubles single quotes to prevent SQL injection and also truncates input to a maximum length, the two defenses interact destructively. A payload of 127 a's followed by a single quote: the doubling adds one character (making it 129), then truncation to 128 removes the doubled second quote, leaving a single unescaped quote that breaks query syntax.

**Hack steps:**
- Note all instances where the application modifies user input: truncation, stripping, encoding, escaping.
- Test for defense interaction by submitting two long strings: one consisting entirely of single quotes, one of `a` characters followed by a single quote. Observe whether an error occurs after either even or odd numbers of characters are submitted.
- If data is stripped non-recursively (e.g., SQL keywords removed once), try nested payloads: `SELSELECTECT` — removing the inner `SELECT` leaves `SELECT`.
- If URL decoding occurs before stripping, try double-encoded payloads.

**Impact:** SQL injection bypass, authentication bypass despite defense-in-depth measures.

---

#### Pattern 10: Search Function Inference Oracle

**Violated assumption:** A search function that returns only document titles (not content) provides no meaningful access to the documents' protected content.

**Test approach:** When a search function returns the count of matching documents (or a binary match/no-match indication) rather than full document content, it can be exploited as an oracle. Issue a large number of targeted queries, narrowing down the content of protected documents through binary search — similar to blind SQL injection inference.

**Hack steps:**
- Identify search functions that return counts or match indicators for content the user is not authorized to view in full.
- For a target document, construct queries with progressively more specific terms and observe match counts.
- Use the binary search approach: if `[topic] [subtopic]` returns 1 match and `[topic] [subtopic] [candidate phrase]` returns 0, the document does not contain that phrase.
- Apply letter-by-letter brute force when the search function matches substrings rather than whole words (effective against passwords stored in wikis and document management systems).

**Impact:** Unauthorized disclosure of protected content, credential leakage, competitive intelligence exposure.

---

#### Pattern 11: Debug Message Harvesting

**Violated assumption:** Debug information returned to a user only contains data about that user's own session and request; it is harmless to display because the user already has access to this information.

**Test approach:** Identify any conditions that cause verbose error messages, debug dumps, or diagnostic responses containing user-specific information (session tokens, usernames, request parameters). Determine whether the storage mechanism for this information is session-scoped or stored in a static (application-global) container. If static, poll the error message endpoint repeatedly across time — it will intermittently expose other users' session data.

**Hack steps:**
- Catalog all anomalous conditions that produce verbose error responses containing user-identifying information.
- Test the error message endpoint using two accounts simultaneously. Engineer an error condition for one account, then immediately access the error endpoint from the second account. If both see the same debug data, the storage is static, not session-scoped.
- Poll the error URL repeatedly over a period of time, logging each response. Even without concurrent testing, a static container will eventually expose another user's data if the application has meaningful traffic.

**Impact:** Mass credential harvesting — session tokens, usernames, and user-supplied input (possibly passwords) exposed across the entire user base.

---

#### Pattern 12: Race Condition (Static Variable Login)

**Violated assumption:** The login process, which has been reviewed and tested, is thread-safe; it cannot produce cross-user session assignment.

**Test approach:** Race conditions in authentication arise when a key identifier (user ID, session object) is briefly written to a static (non-session) variable during the login flow. If two login requests execute concurrently, one thread may overwrite the static variable before the other thread reads it, causing the earlier thread's session to be established with the second user's identity. Testing requires generating high volumes of concurrent requests against security-critical functions.

**Hack steps:**
- Target security-critical functions: login mechanisms, password change functions, funds transfer processes.
- For each function under test, identify the minimal request set required to perform the action and the simplest means of confirming the result (e.g., verify that a login resulted in access to the expected account).
- From multiple machines at different network locations, script simultaneous execution of the same action on behalf of multiple different user accounts.
- Run a large number of iterations. Confirm that each action produced the expected result for the expected user. Anomalies indicate a race condition.
- Be prepared for a high volume of false positives from load effects unrelated to thread safety.

**Caution:** Remote black-box race condition testing is a specialized undertaking appropriate only for the most security-critical applications. It generates high request volumes that may resemble a load test.

**Impact:** Complete authentication bypass, cross-user account access, financial fraud.

---

### Phase 3 — Document and Report

**Step 1: Classify each finding by flaw pattern.**
For each confirmed vulnerability, identify which of the 12 patterns it instantiates (or describe a new pattern if none applies). State the violated developer assumption explicitly.

**Step 2: Document reproduction steps.**
Capture the exact HTTP requests needed to reproduce the flaw. For multistage exploits, number each step.

**Step 3: Rate business impact.**
Logic flaws often have severe business impact (payment bypass, account takeover, financial fraud) even when the technical complexity of exploitation is low. Rate impact in business terms, not just technical severity.

**Step 4: Produce remediation recommendations.**
Map each finding to the relevant defensive principle from the Avoiding Logic Flaws section below.

---

## Avoiding Logic Flaws — Defensive Principles

These principles apply to developers building secure applications and to testers verifying that defenses are adequate.

- **Document all assumptions explicitly.** Every assumption a designer makes should appear in design documentation. An outsider reading the document should be able to understand every assumption and why it holds.
- **Comment source code with component purpose, assumptions, and consumer list.** Every code component should state what it assumes about its inputs, what it assumes about the context in which it is called, and which other components depend on it.
- **During design review, enumerate assumptions and imagine violations.** For each assumption, ask: "Is this condition actually within the control of application users?" If yes, it must be enforced server-side, not assumed.
- **During code review, think laterally about unexpected user behavior and component side effects.** Consider how shared components behave when called from unexpected contexts.
- **Drive all identity and privilege decisions from server-side session state.** Never infer role or privilege from parameter presence/absence, HTTP Referer, or other client-controlled signals.
- **Treat user input as user-controlled in every dimension.** Users control parameter names (not just values), request sequence, which parameters they include or omit, and which features they access in which order.
- **Validate numeric input canonicalization before applying business limits.** If negative values are not semantically valid, reject them explicitly before applying threshold checks.
- **Apply discounts only at order finalization, not at add-to-cart time.**
- **Escape the escape character.** Any escaping mechanism must also escape the escape character itself.
- **Compose defenses with awareness of interaction effects.** If two defenses are applied in sequence, reason about what happens when both transform the same input.
- **Use session-scoped (not static) storage for all per-user data.** Any component that writes user-identifying data must write it into the user's session, not a shared static container.
- **When search functions index protected content, enforce authorization at the inference level.** Returning match counts to unauthorized users is equivalent to returning the content.

---

## Examples

### Example 1: E-Commerce Checkout Skip

**Scenario:** Authorized penetration test of an online retail platform.

**Trigger:** Application implements a four-stage checkout: browse, basket review, payment, delivery. Tester has mapped the workflow and confirmed each stage is served from a distinct URL.

**Process:**
1. Complete stages 1 and 2 normally. Capture all HTTP requests.
2. Apply Pattern 3 (Workflow Stage Skip): from stage 2, construct a direct HTTP request to the stage 4 delivery URL, bypassing stage 3 (payment entry).
3. Submit the stage 4 request. Observe whether the application accepts it and generates an order.
4. Check the order management backend to confirm whether a real order was created without payment.

**Output:** Finding: "Checkout Stage Skip — Payment Bypass." Violated assumption: users always access checkout stages in sequence. Business impact: attackers can generate fulfilled orders without paying. Remediation: enforce that payment stage has been completed server-side (session flag set only after successful payment processing) before accepting the delivery stage request.

---

### Example 2: Insurance Application Cross-Stage Parameter Pollution

**Scenario:** Security assessment of a financial services insurance web application with applicant and underwriter roles.

**Trigger:** Application processes a multi-dozen-stage insurance application. Tester notices that the application uses a shared server-side component that updates application state with any name/value pair received in a POST request.

**Process:**
1. Walk through the full applicant flow, capturing all POST parameters at each stage.
2. Walk through the underwriter review flow as a valid underwriter account, capturing all POST parameters — especially the acceptance decision field (e.g., `underwriterDecision=accept`).
3. Apply Pattern 4 (Cross-Stage Parameter Pollution): during the applicant's final submission stage, additionally submit the underwriter acceptance parameter identified in step 2.
4. Observe whether the application's state records the application as accepted without actual underwriter review.

**Output:** Finding: "Cross-Stage Parameter Pollution — Applicant Self-Underwriting." Violated assumption: only underwriters submit underwriter parameters. Business impact: applicants can accept their own insurance applications at arbitrary premium values. Remediation: enforce role-based access control at the parameter level; the server must validate that each parameter is appropriate for the authenticated user's role before updating application state.

---

### Example 3: Debug Message Polling for Session Tokens

**Scenario:** Penetration test of a recently deployed financial services web application that exhibits intermittent errors.

**Trigger:** During normal testing, an error page appears containing the current user's username, session token, and request parameters. The tester notes this is returned as a redirect to a static URL (`/app/error?id=last`).

**Process:**
1. Apply Pattern 11 (Debug Message Harvesting): engineer an error condition from Account A and immediately access `/app/error?id=last` from Account B.
2. Observe whether Account B's browser displays Account A's debug information (confirming static storage).
3. Write a script to poll `/app/error?id=last` every few seconds over a 30-minute window, logging all responses.
4. Review the log for session tokens and usernames belonging to other users.

**Output:** Finding: "Static Debug Storage — Cross-User Session Token Disclosure." Violated assumption: each user sees only their own debug information because they follow the redirect to their own error. Business impact: an attacker who polls the error endpoint over time accumulates session tokens for other users and can hijack those sessions. Remediation: store debug information in session-scoped storage, not a static global container; or disable verbose debug messages in production entirely.

---

## References

- Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook*, 2nd ed. Wiley. Chapter 11: "Attacking Application Logic," pp. 405–429.
- OWASP Testing Guide: OTG-BUSLOGIC-001 through OTG-BUSLOGIC-009
- CWE-840: Business Logic Errors
- CWE-841: Improper Enforcement of Behavioral Workflow
- CWE-362: Concurrent Execution Using Shared Resource with Improper Synchronization (Race Condition)
- OWASP Top 10 A04:2021: Insecure Design
