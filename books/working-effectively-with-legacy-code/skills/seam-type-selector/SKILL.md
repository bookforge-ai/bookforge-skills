---
name: seam-type-selector
description: "Select the right seam type (Preprocessor / Link / Object) for breaking a dependency in legacy code. Use whenever a developer needs to substitute behavior for testing without editing in place, is choosing between dependency-injection strategies in an existing codebase, or asks 'how do I intercept this call in a test' / 'how do I fake this library' / 'how do I test around this hard-coded dependency'. Activates for 'seam', 'test seam', 'substitution point', 'dependency injection for legacy code', 'mock this without DI framework', 'C++ testing', 'linker-level fake', 'preprocessor substitution', 'polymorphic substitution', 'enabling point'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/seam-type-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [4]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, dependency-injection]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source file containing the dependency to break + language + description of what needs to be substituted"
  tools-required: [Read, Grep]
  tools-optional: [Edit]
  mcps-required: []
  environment: "A codebase in any language. Seam availability depends on language capabilities."
discovery:
  goal: "Recommend the right seam type for a specific testing or substitution scenario."
  tasks:
    - "Classify the dependency as pervasive or localized"
    - "Identify the target language's seam capabilities"
    - "Recommend Object / Link / Preprocessor seam with rationale"
    - "Identify the enabling point for the chosen seam"
    - "Provide a list of compatible dependency-breaking techniques"
  audience:
    roles: [software-engineer, backend-developer, senior-developer]
    experience: intermediate
  when_to_use:
    triggers:
      - "Developer is trying to substitute behavior in legacy code without direct edit"
      - "Choosing between dependency-injection strategies"
      - "Unable to use DI framework due to legacy constraints"
      - "Need to fake a library/global/static for testing"
    prerequisites: []
    not_for:
      - "Greenfield code where DI framework is available"
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

# Seam Type Selector

## When to Use

Use this skill when a developer needs to substitute or intercept behavior in legacy code for testing, but cannot freely edit the code under test. Specifically:

- The code has a hard-coded dependency (global function, library call, concrete class instantiation) that prevents running it in a test harness.
- The developer asks: "How do I fake this?", "How do I test around this global?", "How do I intercept this call without a DI framework?", or "What's the right way to introduce a test double here?"
- The developer is choosing between approaches (subclass override vs. classpath swap vs. macro replacement) and needs a principled recommendation.

Do not use for greenfield code where a dependency injection framework is already in place — the framework already manages enabling points.

---

## Context and Input Gathering

Before recommending a seam type, gather:

1. **Language** — Is this C or C++ (preprocessor available)? A compiled OO language like Java or C# (link and object seams)? A dynamic OO language like Python or Ruby (object seams, plus text redefinition)?
2. **Dependency type** — What exactly needs to be substituted? Options: global function, static method, constructor call, third-party library, concrete class member.
3. **Pervasiveness** — Is this dependency called in one or two places, or scattered across dozens of files and hundreds of call sites?
4. **Risk tolerance** — Is modifying production class structure (adding a virtual method, adding a constructor parameter) acceptable? Some teams forbid structural changes to classes under test without prior test coverage.

---

## Process

### Step 1: Confirm a seam exists

A seam (Feathers' formal definition) is "a place where you can alter behavior in your program without editing in that place." Verify the target call site qualifies:

- You want to substitute the behavior that runs at call site X.
- You can make the substitution without modifying the source text at X itself.
- There is an enabling point — a separate place where you decide which behavior to use.

If no enabling point can be identified, there is no seam. You will need to introduce one first (see `dependency-breaking-technique-executor`).

### Step 2: Classify the dependency

| Classification | Characteristic | Examples |
|---|---|---|
| **Localized** | 1–5 call sites, within one class or module | One `new DatabaseConnection()` in a constructor |
| **Pervasive** | Many call sites, spread across files | 50+ calls to `getenv()` throughout a C codebase; all files import a logging singleton |

Pervasiveness is the primary override condition. If a dependency is pervasive, the cost of introducing object seams at every site may exceed the cost of a single link- or preprocessor-level substitution.

### Step 3: Assess language capabilities

| Language | Preprocessor Seam | Link Seam | Object Seam |
|---|---|---|---|
| C | Yes (`#define`, `#ifdef`) | Yes (object file swap) | No (procedural) |
| C++ | Yes | Yes | Yes |
| Java, Kotlin | No | Yes (classpath) | Yes |
| C# | No | Yes (assembly) | Yes |
| Python, Ruby | No | Limited | Yes (duck typing) |
| Go | No | Limited | Yes (interfaces) |
| TypeScript/JS | No | Limited (module mock) | Yes |

### Step 4: Apply the selection rule

Feathers states: "In general, object seams are the best choice in object-oriented languages. Preprocessing seams and link seams can be useful at times but they are not as explicit as object seams. Tests that depend on them can be hard to maintain. Reserve preprocessing seams and link seams for cases where dependencies are pervasive and there are no better alternatives."

**Decision hierarchy:**

```
1. Is the language OO and the dependency localized?
   → Use Object Seam

2. Is the language OO but the dependency is pervasive (many call sites)?
   → Prefer Link Seam (keeps source changes minimal)
   → Fall back to Preprocessor Seam only in C/C++

3. Is the language procedural C/C++ and the dependency is pervasive?
   → Link Seam first; Preprocessor Seam if link is not feasible

4. Is the language procedural C/C++ and the dependency is localized?
   → Preprocessor Seam (only option available)
```

### Step 5: Identify the enabling point

Every seam has an enabling point — name it explicitly. Future readers (and the developer implementing the seam) must know where to flip the switch.

| Seam Type | Where the Enabling Point Lives |
|---|---|
| **Object Seam** | Where the object is constructed or injected — a constructor, factory method, parameter, or setter |
| **Link Seam** | The build configuration — classpath entry, Makefile rule, linker flag, or IDE project setting |
| **Preprocessor Seam** | A preprocessor define — `#define TESTING`, a `-DTESTING` compiler flag, or an `#include` of a test-override header |

### Step 6: Produce the recommendation artifact

Output a `seam-recommendation.md` (template in Outputs section) with: seam type, enabling point location, rationale, language note, and a list of compatible Part III techniques the developer can apply next.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Source file(s) | Required | The file(s) containing the dependency to break |
| Language | Required | Programming language of the codebase |
| Dependency description | Required | What call/class/library needs to be substituted |
| Pervasiveness assessment | Recommended | Number of call sites; single file vs. codebase-wide |
| Risk constraints | Optional | Whether structural changes to production classes are allowed |

---

## Outputs

### seam-recommendation.md

```markdown
## Seam Recommendation: [dependency name]

**Chosen Seam Type:** [Object / Link / Preprocessor]

**Enabling Point:**
[Exact location — e.g., "The constructor of OrderProcessor (line 42 of OrderProcessor.java)"
or "The classpath entry resolving com.example.PaymentGateway"
or "The TESTING preprocessor define passed via -DTESTING in the Makefile"]

**Rationale:**
[1–3 sentences: why this seam type for this language, dependency type, and pervasiveness level]

**Language Applicability:**
[Confirm the seam is available in the target language; note if a fallback was chosen]

**Compatible Part III Techniques:**
- [Technique name] — [one-line explanation of how it exploits this seam]
- [Technique name] — ...

**Next step:** See `dependency-breaking-technique-executor` to apply the selected technique.
```

---

## Key Principles

1. **Prefer object seams for maintainability.** Object seams are explicit — the substitution is visible in the source code at the enabling point. Link and preprocessor seams substitute behavior invisibly; future readers see nothing unusual at the call site.

2. **Every seam has an enabling point — name it explicitly.** A seam without a named enabling point is incomplete. The enabling point is where the developer acts; without naming it, the recommendation cannot be implemented.

3. **Pervasive dependencies may justify link or preprocessor seams.** When a global function is called in 80 places across 20 files, introducing a virtual dispatch at each site is high-risk surgery. A single build-level substitution is safer than 80 structural edits.

4. **Seams make the substitution point visible to future readers.** The goal is not just to make tests pass today — it is to leave the codebase in a state where the next engineer can understand which behavior is being substituted and why.

---

## Examples

### Example A: Java class with a hard-coded dependency (Object Seam)

**Situation:** A `UserService` class has a constructor that directly instantiates `UserRepository`, which opens a database connection. No DI framework. Need to test `UserService.findActiveUsers()` without a real database.

**Classification:** Localized (one constructor site). Language: Java (OO).

**Recommendation:** Object Seam.

**Enabling point:** The `UserService` constructor. Introduce a second constructor that accepts a `UserRepository` parameter (Parameterize Constructor technique). Tests pass in a fake implementation; production code calls the original constructor.

**Compatible techniques:** Parameterize Constructor, Extract Interface (extract `IUserRepository`), Subclass and Override Method.

---

### Example B: C++ with pervasive global calls (Link Seam)

**Situation:** A legacy C++ codebase has 60+ calls to `log_event()` (a global that writes to a syslog daemon) scattered across 15 files. Running tests triggers syslog writes and slows everything down.

**Classification:** Pervasive. Language: C++ (compiled, OO).

**Recommendation:** Link Seam.

**Enabling point:** The Makefile's link step. Create a `test_log_event.o` object file with a stub `log_event()` that records calls in memory. Swap it in via the Makefile for test builds. Source files are untouched.

**Compatible techniques:** Link-level substitution (Ch 19 procedural pattern), Encapsulate Global References (if later migration to OO is planned).

---

### Example C: Legacy C with pervasive global calls (Preprocessor Seam)

**Situation:** A C codebase calls `db_update(account_no, record)` in 40 places across 8 files. There is no OO structure and no link-time substitution capability in the build environment.

**Classification:** Pervasive. Language: C (procedural — no object seam available).

**Recommendation:** Preprocessor Seam.

**Enabling point:** A `#define TESTING` flag passed to the C compiler (e.g., `gcc -DTESTING`). A `localdefs.h` header, included in each source file, defines a macro replacement for `db_update` under `#ifdef TESTING` that captures arguments without hitting the database.

**Compatible techniques:** Text Redefinition (C/C++ specific), C macro preprocessor pattern (Ch 19).

---

## References

See `references/seam-type-comparison.md` for a full comparison matrix of all three seam types across language families, enabling point locations, and compatible Chapter 25 techniques.

---

## License

[CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) — derived from *Working Effectively with Legacy Code* by Michael C. Feathers (2004).

---

## Related BookForge Skills

- **`dependency-breaking-technique-executor`** — Takes a seam recommendation and applies a specific Chapter 25 technique step-by-step. This skill feeds directly into it.
- **`legacy-code-change-algorithm`** — The outer 6-step procedure. Seam identification is Step 3 of that algorithm; use this skill to complete it.
- **`library-seam-wrapper`** — Applies the link seam pattern specifically to third-party library dependencies, wrapping them in an interface.
