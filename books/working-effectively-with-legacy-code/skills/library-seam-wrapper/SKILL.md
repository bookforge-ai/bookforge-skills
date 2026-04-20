---
name: library-seam-wrapper
description: "Isolate third-party library dependencies behind thin wrapper interfaces to break vendor lock-in and enable testing. Use whenever a developer has direct calls to library classes scattered through production code and can't test or swap the library — 'library is killing me', 'vendor lock-in', 'can't mock this library', 'integration tests only for this SDK', 'AWS SDK everywhere', 'Stripe calls in 50 files', 'all API calls', 'wrapping a library', 'adapter for third-party'. Triggers for 'third party', 'SDK', 'library coupling', 'external service', 'API client'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/library-seam-wrapper
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [14, 15]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, third-party-libraries, vendor-lock-in]
depends-on:
  - seam-type-selector
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Codebase with direct library/SDK calls + identification of the library class(es) to wrap"
  tools-required: [Read, Grep, Edit, Bash]
  tools-optional: [Glob]
  mcps-required: []
  environment: "Codebase (any OO language). Link Substitution fallback requires C/C++ build system."
discovery:
  goal: "Replace direct third-party library calls with wrapped abstractions to enable testing and reduce lock-in."
  tasks:
    - "Inventory direct library calls across the codebase"
    - "Design the minimal wrapper interface for the use case"
    - "Create production adapter implementing the interface"
    - "Gradually migrate call sites to use the interface"
    - "Enable test fakes via the interface"
  audience:
    roles: [software-engineer, backend-developer, tech-lead]
    experience: intermediate
  when_to_use:
    triggers:
      - "Vendor lock-in risk identified"
      - "Application is mostly glue between external APIs"
      - "Library calls cannot be faked in tests"
      - "Need to swap library vendor"
    prerequisites:
      - skill: seam-type-selector
        why: "Library wrapping is the object-seam approach; understand the seam model first"
    not_for:
      - "In-house or fully-controlled libraries (modify directly)"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 10
    iterations_needed: null
---

# Library Seam Wrapper

## When to Use

Use this skill when production code calls third-party library or SDK classes directly — and those calls are making testing hard or locking the team into a vendor.

Concrete triggers:
- Tests require the real library (slow, expensive, flaky) because there is no seam to inject a fake.
- A vendor changed pricing, deprecated an API, or introduced licensing terms the team cannot meet, and switching would require touching dozens of files.
- The codebase is "mostly API calls" — every class is a thin shell around external service SDKs with no testable seam.
- A developer says "we'll never need to change this library" — Feathers' warning: that belief can become a self-fulfilling prophecy.

Do not use for in-house or fully-controlled libraries — those can be changed or extended directly without wrapping.

---

## Context and Input Gathering

Before starting, establish:

1. **Library / SDK name and scope** — Which library is being wrapped? One class, one module, or the entire SDK surface?
2. **Call-site inventory** — Where does the library appear in the codebase? Use Grep to find import statements and class-name usages.
3. **Primary goal** — Is the goal to enable test fakes, or to hedge against vendor swap, or both? The goal influences how domain-expressive the wrapper interface needs to be.
4. **Language and OO capability** — OO languages use the object-seam approach (interface + adapter). C/C++ without viable interfaces fall back to Link Substitution.
5. **API complexity** — A small, stable API is a good candidate for full Skin and Wrap. A large, complicated API is a better candidate for Responsibility-Based Extraction.

---

## Process

### Step 1: Inventory direct library calls

Grep the codebase for all import statements and direct usage of the library's class names. Build a call-site map:

```
Grep pattern: import.*<LibraryPackage> OR new <LibraryClass>( OR <LibraryClass>.
```

Record:
- Which files import the library
- Which class or method names from the library appear in production code
- Whether usages cluster in a few classes or are scattered across the codebase

A scattered inventory confirms the anti-pattern Feathers names: the library has become structurally embedded, and every call site is a seam that does not exist.

### Step 2: Classify wrapping scope

Choose between two strategies based on API complexity and migration risk:

**Skin and Wrap** (preferred when feasible):
- Create an interface that mirrors the library's surface you actually use — not its entire API, only the methods your code calls.
- Implement a production adapter that delegates to the real library.
- Production code depends only on the interface; zero library imports outside the adapter.
- Result: complete isolation. The adapter is the only file that touches the library; swapping vendors means writing one new adapter.
- Good when: the API is relatively small, the team wants total isolation, or there are no tests and the only safe path is wrapping first.

**Responsibility-Based Extraction** (when the API is large or tangled):
- Identify the domain responsibility behind each cluster of API calls (e.g., "send a message", "check for mail").
- Extract those responsibilities into methods on a new class, giving them domain-expressive names.
- The new class still calls the library, but the consuming code depends on higher-level behavior, not raw API calls.
- Result: partial isolation. The extracted class is still testable through its interface; some API coupling may remain inside it.
- Good when: the API is complicated, refactoring tools are available, or an all-at-once rewrite is not safe.

Many teams use both: a thin wrapper for test isolation, and a higher-level responsibility wrapper to give the application a domain language. Feathers: "Skin and wrap is more work, but it can be very useful when we want to isolate ourselves from third-party libraries."

### Step 3: Design the wrapper interface

The interface must reflect your use case, not the library's API:

- Name methods by what they do for your domain: `sendTransactionalEmail(recipient, subject, body)` not `postWithSmtpTransport(SmtpSession, InternetAddress[], MimeMessage)`.
- Include only the methods your production code actually calls — do not mirror the whole library.
- Keep the interface stable against library changes; it should be driven by your domain needs.
- One interface per logical service (payment, messaging, storage) keeps fakes small and readable.

If the existing code directly instantiates library objects (e.g., `new Transport()`) that cannot be subclassed — because the library class is `final`, `sealed`, or has non-virtual methods — wrapping is the only viable option. Feathers notes: "Sometimes wrapping the singleton is the only choice available to you."

### Step 4: Implement the production adapter

Create a class that:
- Implements the wrapper interface.
- Holds a reference to the real library object (injected or created internally).
- Delegates each interface method to the library — no business logic inside the adapter.
- Is the only file in the codebase that imports the library package.

The adapter is thin by design. If business logic creeps in, extract it to the calling class instead.

### Step 5: Migrate call sites incrementally

Replace direct library calls with wrapper calls one file at a time, not all at once:

1. Start with the class that has the highest call density or the most urgent test need.
2. Inject the wrapper interface via constructor parameter (preferred) or a setter.
3. Verify tests pass after each migrated file before moving to the next.
4. Leave the remaining call sites temporarily; the build stays green throughout.

Incremental migration avoids the "big bang" refactor that breaks the entire build simultaneously.

### Step 6: Create a fake implementation for tests

With the interface in place, write a `Fake<ServiceName>` class that:
- Implements the wrapper interface.
- Records calls (captures arguments) or returns scripted responses.
- Contains no real I/O or network calls.
- Lives in the test source tree only.

Tests inject the fake; production code uses the real adapter. The interface is the only contract both must satisfy.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Library / SDK name | Required | The third-party library to wrap |
| Codebase access | Required | Source files containing direct library calls |
| Call-site inventory | Required | Grep-generated list of files and usage patterns |
| Primary goal | Required | Test isolation, vendor swap, or both |
| Language | Required | Determines whether object seam or Link Substitution applies |

---

## Outputs

### wrapper-design.md

Documents the wrapping decision for the team:

```markdown
## Wrapper Design: [Library Name]

**Strategy:** [Skin and Wrap | Responsibility-Based Extraction | Both]
**Rationale:** [1–2 sentences on why this strategy for this API]

**Interface:** [InterfaceName]
**Methods:**
- `methodName(params): ReturnType` — [what it does for the domain]

**Production Adapter:** [AdapterClassName]
**Fake Implementation:** [FakeClassName] (test source only)

**Enabling Point:** [Where the adapter is injected — constructor param, factory, etc.]

**Migration plan:** [List of files to migrate, in order of priority]
```

### Production adapter source file

The implementing class, reviewed for zero business logic and single responsibility.

### migration-plan.md

Ordered list of call sites to migrate, one per file, with estimated test coverage gain per step.

---

## Key Principles

1. **"We'll never change this library" is a self-fulfilling prophecy.** Every hard-coded library call is a seam that does not exist. The team cannot fake it, cannot swap the vendor, and eventually cannot change it at all. Wrap before the cost becomes prohibitive.

2. **The wrapper interface names the use case, not the library API.** `PaymentGateway.charge(amount, currency, token)` is a domain concept. `StripeClient.createPaymentIntent(PaymentIntentCreateParams)` is a library detail. The interface protects consuming code from library churn.

3. **Full wrap is better than skin-and-wrap, but skin-and-wrap beats no wrap.** Even a thin pass-through interface that mirrors the library API provides the test-injection seam. Improve the domain naming later.

4. **A library-using class can wrap itself.** If a class uses a library for a single responsibility, extract that responsibility into an interface on the class itself. The class becomes its own adapter; no new file required.

5. **The adapter is the only file that imports the library.** Enforcing this as a convention (via linting or package visibility) prevents the anti-pattern from re-emerging after migration.

---

## Examples

### Example A: Stripe SDK scattered across 40 Java files

**Situation:** A payment service has `StripeClient`, `Charge`, and `PaymentIntent` imports in 40 files. Unit tests hit the real Stripe API with test keys — they are slow and occasionally fail due to network timeouts.

**Strategy:** Skin and Wrap. The Stripe API surface actually used is small: create a charge, retrieve a charge, refund.

**Interface:**
```java
interface PaymentGateway {
    ChargeResult charge(Money amount, String token);
    ChargeResult retrieve(String chargeId);
    RefundResult refund(String chargeId, Money amount);
}
```

**Production adapter:** `StripePaymentGateway implements PaymentGateway` — delegates to `StripeClient`, zero business logic.

**Fake:** `FakePaymentGateway implements PaymentGateway` — stores charges in a `List`, returns scripted responses.

**Migration:** Inject `PaymentGateway` via constructor into each service class, replacing direct `StripeClient` usages one class at a time.

**Outcome:** 40 files see the interface only. Switching to Braintree means writing one new adapter.

---

### Example C: C codebase with curl calls (Link Substitution fallback)

**Situation:** A C codebase makes HTTP calls via `curl_easy_perform()` in 30 files. No OO structure exists; an interface cannot be defined. The team needs to test HTTP-dependent functions without real network calls.

**Strategy:** Link Substitution (Ch 25 fallback for procedural languages when interface wrapping is not feasible).

**Steps:**
1. Identify all calls to `curl_easy_perform`, `curl_easy_setopt`, and `curl_easy_init`.
2. Write a `fake_curl.c` that provides stub implementations recording calls in memory.
3. Adjust the test build (Makefile) to link `fake_curl.o` instead of the real libcurl.

The production Makefile links the real libcurl. The test Makefile links the fake. Source files are untouched.

**Limitation:** Link Substitution provides fake isolation but not vendor-swap isolation. A full wrapper in OO code is preferable when feasible.

---

### Example C: iOS app that is 90% CRM API calls

**Situation:** An iOS CRM client has view controllers calling the vendor SDK directly. 90% of the code is mapping API responses to UI. A product manager wants to evaluate switching vendors.

**Strategy:** Responsibility-Based Extraction with per-service wrappers.

**Decomposition:**
1. Identify the domain responsibilities behind the API calls: contact lookup, activity logging, pipeline management.
2. Create one protocol (Swift) per responsibility: `ContactRepository`, `ActivityLogger`, `PipelineService`.
3. Implement production adapters that delegate to the CRM SDK.
4. View controllers depend only on the protocols.

**Outcome:** Evaluating a new vendor requires writing three new adapters, not auditing 200 view controller methods. The app's logic is now testable without the CRM SDK.

---

## References

See `references/wrapper-design-template.md` for a blank `wrapper-design.md` template and a decision checklist for choosing between Skin and Wrap and Responsibility-Based Extraction.

---

## License

[CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) — derived from *Working Effectively with Legacy Code* by Michael C. Feathers (2004).

---

## Related BookForge Skills

- **`seam-type-selector`** — Prerequisite. Library wrapping is the object-seam approach; this skill helps you confirm it before investing in wrapper design.
- **`dependency-breaking-technique-executor`** — Extract Interface is the primary mechanic behind Step 3 and Step 4 of this skill. Use it when executing the interface extraction in a specific language.
- **`legacy-code-symptom-router`** — Routes legacy code problems to the right skill. If the symptom is "can't test because of a library", it should direct here.
