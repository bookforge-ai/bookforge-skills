---
name: dependency-breaking-technique-executor
description: "Select and execute the right dependency-breaking technique from Michael Feathers' catalog of 24 named techniques (Part III of Working Effectively with Legacy Code) for a specific testability obstacle. Use when a class or method cannot be placed under test due to a hard-coded dependency, and you need concrete step-by-step mechanics for breaking it safely — without existing tests protecting you. Activates for 'can't test this class', 'constructor dependency', 'global variable blocking tests', 'static call in method', 'inject a fake', 'break dependency for testing', 'extract interface legacy', 'subclass and override', 'parameterize constructor', 'encapsulate global', 'dependency injection without framework', 'extract and override', 'how to fake this in test', 'legacy code testability refactoring'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/dependency-breaking-technique-executor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [25]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, dependency-injection]
depends-on:
  - legacy-code-change-algorithm
  - seam-type-selector
  - safe-legacy-editing-discipline
  - test-harness-entry-diagnostics
execution:
  tier: 1
  mode: full
  inputs:
    - type: code
      description: "Class or method containing the dependency to break + language + description of the testability obstacle"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any codebase. Language determines which of the 24 techniques are available."
discovery:
  goal: "Select the right technique and execute its full mechanics to break one specific dependency."
  tasks:
    - "Receive diagnostic from test-harness-entry-diagnostics or elicit obstacle directly"
    - "Classify dependency type and constraint"
    - "Select technique via the selection table"
    - "Execute full mechanics with Preserve Signatures discipline"
    - "Run tests; use Lean on the Compiler in statically-typed languages"
    - "Document the break in dependency-break-log.md"
---

# Dependency-Breaking Technique Executor

## When to Use

Use this skill when you have a specific class or method that cannot be placed in a test harness because of a hard dependency — a constructor that allocates live resources, a method that calls a global or static, an interface that is sealed or final, a C++ header chain that pulls in half the system. You have already confirmed the obstacle (ideally via `test-harness-entry-diagnostics`) and need to choose from Feathers' 24 named techniques and execute the mechanics correctly.

**Do not use** this skill for design-level refactoring after tests exist — these techniques are intentionally conservative and produce imperfect intermediate states. The goal is testability, not beauty.

This skill executes **Step 3 (Break Dependencies)** of the Legacy Code Change Algorithm.

---

## Context and Input Gathering

Before selecting a technique, you need four things:

| Item | Source | How to get it |
|------|--------|---------------|
| Dependency type | `test-harness-entry-diagnostics` output or direct inspection | See classification below |
| Language | User or codebase | Determines which techniques apply |
| Constraint scope | Inspection | Localized (one method) vs pervasive (spread across methods/classes) |
| Can modify parameter/class? | Inspection | Affects Adapt Parameter vs Extract Interface choice |

**Dependency type classification:**

- **Constructor dep** — `new ConcreteType()` hard-coded in constructor; no way to inject alternative
- **Method param dep** — method receives a hard-to-construct/fake concrete parameter
- **Global/static var** — method reads or writes a global or static variable
- **Static method call** — method calls `SomeClass.staticMethod()` with no interception point
- **Virtual/overridable call** — method makes a call that could be made virtual/overridable
- **Singleton dep** — class accesses a global singleton instance
- **Header dep** (C++ only) — `#include` chain pulls in platform headers that break compilation
- **Template/generic dep** — dependency baked into a type parameter

If you do not have output from `test-harness-entry-diagnostics`, ask:
1. What is the exact error or obstacle when you try to instantiate the class or run the method in a test?
2. What language and version?
3. Is this one location or does the same dependency appear in many places across the class/codebase?

---

## Process

### Step 1: Receive the Diagnostic

If `test-harness-entry-diagnostics` has already run, use its output directly — it classifies the obstacle and recommends candidate techniques. If not, elicit the three context items above and classify the dependency type yourself.

### Step 2: Consult the Selection Table

Use the compact table below to get to a candidate technique. Full matrix is in `references/selection-table.md`.

| Dependency Type | Language | Constraint | Recommended Technique |
|-----------------|----------|------------|-----------------------|
| Constructor creates concrete object | OO | Localized | **Parameterize Constructor** |
| Constructor creates chain of objects | OO | Moderate | **Extract and Override Factory Method** |
| Constructor creates objects (C++, no virtual in ctor) | C++ | — | **Extract and Override Getter** or **Supersede Instance Variable** |
| Method creates concrete object internally | OO | Localized | **Parameterize Method** |
| Method parameter is hard-to-fake concrete | OO | Localized | **Extract Interface** or **Adapt Parameter** |
| Parameter interface name taken by class | OO | — | **Extract Implementer** |
| Parameter is sealed/final, cannot be extracted | OO | — | **Subclass and Override Method** |
| Global/static variable — localized to one method | OO | Localized | **Replace Global Reference with Getter** |
| Global/static variable — spread across class | OO/C++ | Pervasive | **Encapsulate Global References** |
| Static method call | OO | Localized | **Extract and Override Call** |
| Static method call, need instance level | OO | — | **Introduce Instance Delegator** |
| Singleton blocking tests | OO | — | **Introduce Static Setter** |
| Few bad dependency methods, rest are fine | OO | Localized | **Subclass and Override Method** or **Pull Up Feature** |
| Many bad dependency methods, few good ones | OO | Pervasive | **Push Down Dependency** |
| Method too long, uses instance data | OO | — | **Break Out Method Object** |
| Method pure/stateless, no instance data | OO | — | **Expose Static Method** |
| Global functions (C procedural) | C | Localized | **Replace Function with Function Pointer** |
| Whole library/translation unit | C/C++/Java | Build-level | **Link Substitution** |
| C++ header chain | C++ | — | **Definition Completion** |
| Parameter is primitive but hides complex object | OO | Last resort | **Primitivize Parameter** |
| Language has generics/templates | C++/Java | — | **Template Redefinition** |
| Language is interpreted (Ruby, Python, etc.) | Dynamic | — | **Text Redefinition** |

If two techniques appear, prefer the one higher in the list (simpler, fewer structural changes).

### Step 3: Confirm the Choice

Cross-check against `references/selection-table.md` if in doubt, particularly for:
- Whether the language prohibits virtual calls in constructors (C++)
- Whether the name of the desired interface already equals the class name (Extract Interface vs Extract Implementer)
- Whether dependencies are truly localized vs pervasive (affects Subclass and Override vs Push Down Dependency)

### Step 4: Execute the Mechanics

Full mechanics for all 24 techniques are in `references/all-techniques.md`. The 6 most common are inlined here.

---

### Technique A: Parameterize Constructor

**Problem:** Constructor hard-codes `new ConcreteType()` — no way to pass in a fake.

**Steps:**

1. Identify the constructor and the `new` expression creating the problematic object. Copy the full constructor signature (Preserve Signatures).
2. Create a new constructor with all the original parameters **plus one new parameter** for the object being replaced. Inside the new constructor, remove the `new` expression and assign the parameter to the instance variable.
3. Give the original constructor a new body: call the new constructor, passing `new ConcreteType(...)` as the new argument. If your language does not support constructor delegation, extract the shared body to a private `initialize()` method that both constructors call.

**Java example:**
```java
// BEFORE
class PaymentProcessor {
    private DatabaseConnection db;
    PaymentProcessor() {
        this.db = new DatabaseConnection("prod-host", 5432);  // untestable
    }
}

// AFTER
class PaymentProcessor {
    private DatabaseConnection db;

    // New parameterized constructor — use in tests
    PaymentProcessor(DatabaseConnection db) {
        this.db = db;
    }

    // Original constructor — production code unchanged
    PaymentProcessor() {
        this(new DatabaseConnection("prod-host", 5432));
    }
}
// Test: new PaymentProcessor(new FakeDatabase())
```

**Lean on the Compiler:** If the class is used in many places, the compiler will not complain — both constructors are valid. Rely on grep or code review to confirm production callers still use the no-arg constructor.

---

### Technique B: Parameterize Method

**Problem:** A method body hard-codes `new ConcreteType()` — you can instantiate the class fine, but you cannot intercept the object creation inside one specific method.

**Steps:**

1. Identify the method and copy its signature.
2. Create a new version of the method with all original parameters **plus one new parameter** for the created object. Remove the creation expression; use the parameter.
3. Give the original method a new body: call the new parameterized method, passing `new ConcreteType(...)` as the extra argument.

**C++ example:**
```cpp
// BEFORE
void TradeRecorder::record(Trade* trade) {
    AuditLog* log = new AuditLog("/var/log/trades");  // ties to filesystem
    log->write(trade->toXml());
    delete log;
}

// AFTER
void TradeRecorder::record(Trade* trade, AuditLog* log) {
    log->write(trade->toXml());
}

void TradeRecorder::record(Trade* trade) {
    AuditLog* log = new AuditLog("/var/log/trades");
    record(trade, log);
    delete log;
}
// Test: recorder.record(trade, &fakeLog)
```

---

### Technique C: Extract Interface

**Problem:** A parameter, instance variable, or return type is a concrete class — you cannot pass a fake without changing the production signature.

**Steps:**

1. Create a new interface with the name you want. Add **no methods yet**. Make the existing concrete class implement it. Compile and run tests to verify nothing broke.
2. Change the declaration of the target (parameter, field, local variable) to use the new interface type instead of the concrete class.
3. Compile the system. Every method call on the variable that the compiler now rejects needs to become a method declaration on the interface. Add them one by one, guided by compiler errors — this is Lean on the Compiler doing method discovery.
4. Create a fake implementation of the interface for use in tests.

**Why compiler-driven discovery matters:** Never extract a maximal interface (copying all public methods). Only add methods that the actual usage site needs. The compiler tells you exactly which methods those are.

**Java example:**
```java
// BEFORE: UserNotifier depends on concrete UserRepository
class UserNotifier {
    private UserRepository repo;
    UserNotifier(UserRepository repo) { this.repo = repo; }
    void notify(int userId) {
        User user = repo.findById(userId);
        sendEmail(user.getEmail());
    }
}

// AFTER: Extract IUserRepository
interface IUserRepository {
    User findById(int id);  // compiler told us this is needed
}
class UserRepository implements IUserRepository { ... }
class FakeUserRepository implements IUserRepository {
    public User findById(int id) { return new User("test@test.com"); }
}
class UserNotifier {
    private IUserRepository repo;
    UserNotifier(IUserRepository repo) { this.repo = repo; }
    ...
}
```

**C++ note:** In C++, non-virtual methods are resolved at compile time. If the concrete class has non-virtual methods you rely on, Extract Interface (creating a pure-virtual abstract base) is the correct approach. Do not try to extract an interface from a class with only non-virtual methods you need — use Subclass and Override Method instead.

---

### Technique D: Subclass and Override Method

**Problem:** A few methods inside a class call out to problematic dependencies (UI, network, filesystem). You cannot easily parameterize because the method uses `this` directly.

**Steps:**

1. Identify the smallest set of methods that, if overridden, would eliminate all the problematic dependencies. Try to find one or two methods rather than a large set.
2. Make each method overridable: in C++, add `virtual`; in Java, confirm it is not `final` (remove `final` if needed); in C#, add `virtual` or `override`.
3. Adjust visibility so that a subclass can override: in Java/C#, methods must be at least `protected` (not `private`). In C++, `virtual` methods can have any access but `protected` is conventional for testing seams.
4. Create a testing subclass in your test file. Override the methods to do nothing or return safe values. Verify that you can instantiate this subclass in your test harness and that the problematic calls are neutralized.

**Language visibility quick-ref:**

| Language | Make overridable | Visibility minimum |
|----------|-----------------|-------------------|
| C++ | add `virtual` | `protected` conventional |
| Java | remove `final` (default non-final) | `protected` |
| C# | add `virtual` | `protected` |
| Python/Ruby | nothing required | nothing required |

**Key risk:** Test subclasses that override too many methods may stop testing the real class logic. Override only the methods that reach problematic external dependencies — not the logic you actually want to test.

---

### Technique E: Encapsulate Global References

**Problem:** Free-standing global variables or functions are used throughout a class or multiple methods. The globals cannot be intercepted per-call without restructuring every call site.

**Steps:**

1. Identify all the globals you want to encapsulate. Group logically-related globals together.
2. Create a new class to hold them. Name it for its responsibility (e.g., `ApplicationContext`, `PlatformServices`).
3. Copy the global variable declarations and function signatures into the new class as instance variables and methods.
4. Comment out (do not delete yet) the original global declarations. Keep the definitions.
5. Declare a **global instance** of the new class with the original names or a conventional name (e.g., `g_context`).
6. **Lean on the Compiler** — attempt to compile. Every unresolved reference to an original global is now a compiler error. Navigate to each error.
7. Prefix each formerly-global reference with the global instance name (e.g., `g_context.openConnection()`).
8. Now you have an object you can replace. Use one or more follow-on techniques to enable substitution in tests: **Introduce Static Setter** (for singletons), **Parameterize Constructor** (pass the instance in), **Parameterize Method**, or **Replace Global Reference with Getter** (per-method override via subclass).

**C++ example (abbreviated):**
```cpp
// BEFORE: globals spread everywhere
extern int g_activeConnections;
bool openConnection(const std::string& host);

// Encapsulated:
struct NetworkGlobals {
    int activeConnections;
    bool openConnection(const std::string& host);
};
extern NetworkGlobals g_network;  // replaces originals

// After Lean on the Compiler, every site becomes:
g_network.openConnection(host);
g_network.activeConnections++;

// In tests (using Parameterize Constructor afterward):
FakeNetworkGlobals fakeNet;
MyClass obj(&fakeNet);  // injected
```

**When to use vs Replace Global Reference with Getter:** Use Encapsulate Global References when the same global is accessed in multiple methods of the class. Use Replace Global Reference with Getter when only one method uses it and Subclass and Override is already in play.

---

### Technique F: Extract and Override Factory Method

**Problem:** A constructor creates one or more objects internally via `new`, and the creation cannot simply be parameterized because it involves multiple steps or inter-object initialization.

**Steps:**

1. Identify the object creation in the constructor (the `new SomeType(...)` expression and surrounding initialization logic).
2. Extract all of that creation logic into a new protected method, e.g., `createXxx()`. The method returns the created object. The constructor calls the factory method and assigns the result.
3. Create a testing subclass that overrides `createXxx()` to return a fake or null object.

**Java example:**
```java
// BEFORE
class OrderProcessor {
    private ShippingService shipping;
    OrderProcessor() {
        this.shipping = new FedExShippingService(loadConfig());  // pulls config file
    }
}

// AFTER
class OrderProcessor {
    private ShippingService shipping;
    OrderProcessor() {
        this.shipping = createShippingService();
    }
    protected ShippingService createShippingService() {
        return new FedExShippingService(loadConfig());
    }
}

// In tests:
class TestOrderProcessor extends OrderProcessor {
    protected ShippingService createShippingService() {
        return new FakeShippingService();
    }
}
```

**C++ warning:** Do **not** call virtual methods from a C++ constructor. Virtual dispatch is not in effect during construction. If you need this pattern in C++, use Extract and Override Getter (lazy initialization via a getter that is only called after construction) or Supersede Instance Variable.

---

### Step 5: Run Tests and Adjust

After executing the mechanics:

1. Attempt to compile. If there are errors, use Lean on the Compiler to navigate them — do not guess at call sites; let the compiler find them.
2. Run the tests. If a test fails because you missed an override or the fake is not wired in correctly, adjust the test subclass or fake implementation.
3. If the change introduced a regression in existing tests, check whether you violated Preserve Signatures. The most common mistake is accidentally changing a method signature during the extraction.
4. If compilation fails persistently, verify that you have not introduced circular dependencies (common in C++ header extraction).

### Step 6: Document the Break

Create or update `dependency-break-log.md` in the book or module directory. Record:

```markdown
## [Date] Break: [TechniqueName] on [ClassName.methodName]

**Obstacle:** [What prevented testing before]
**Technique chosen:** [Name from catalog]
**Why this technique:** [One sentence justification]
**Changes made:**
- [File and what changed]
**Remaining design debt:** [What this left imperfect — be honest]
**Next step:** [What to refactor once tests are in place]
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Source code file | Yes | The class or method containing the dependency |
| Language | Yes | Determines which techniques apply |
| Testability obstacle | Yes | From `test-harness-entry-diagnostics` or direct description |
| Constraint scope | Yes | Localized vs pervasive |
| `test-harness-entry-diagnostics` output | Optional but recommended | Pre-classifies obstacle; speeds selection |

---

## Outputs

| Output | Description |
|--------|-------------|
| Refactored source code | The class after dependency breaking — compilable and testable |
| `chosen-technique.md` | Short record of which technique was used and why |
| `dependency-break-log.md` | Running log of all breaks for the module |
| Test file stub | If applicable, the testing subclass or fake used to verify the break |

---

## Key Principles

**Prefer object seam techniques in OO languages.** Extract Interface, Parameterize Constructor, Subclass and Override Method, and Extract and Override Factory Method all create explicit, maintainable object seams. Reserve Link Substitution, Preprocessor Seams, and procedural techniques (Replace Function with Function Pointer) for C/C++ codebases where OO techniques are unavailable or the dependencies are at the build level.

**Use Preserve Signatures during step execution.** When extracting a method or copying a constructor, copy the parameter list exactly as written — do not rename parameters, collapse overloads, or add convenience arguments. Introduce those improvements after tests are in place. Signature drift during dependency breaking is a leading cause of introducing bugs while trying to enable testing.

**Lean on the Compiler in statically-typed languages.** When you move a declaration (comment out a global, rename a class, change a field type), let compile errors guide you to every affected call site. This is more reliable than grep. Be aware of the inheritance trap: removing a method from a class will not produce a compiler error if a superclass has the same method — check the class hierarchy.

**For pervasive dependencies, prefer Encapsulate Global References over per-site rewrites.** If the same global or static appears in five methods of a class, encapsulating it once and replacing with a parameterized or getter-based approach costs less than applying Extract and Override Call five times separately.

**Each technique is a refactoring done without tests — that is the point.** The conservative step-by-step mechanics protect you in the absence of a safety net. Resist the temptation to clean up design simultaneously. "First, make it testable. Then, make it good."

---

## Examples

### Example 1: Parameterize Constructor (Java)

`PaymentProcessor` creates `new DatabaseConnection("prod", 5432)` in its constructor. Tests cannot run without a live database.

**Technique:** Parameterize Constructor. Add `PaymentProcessor(DatabaseConnection db)` constructor; original becomes `this(new DatabaseConnection(...))`. Tests inject `new FakeDatabaseConnection()`. Production callers unchanged.

---

### Example 2: Extract Interface (Java)

`UserNotifier` holds a `UserRepository` field. Repository opens a database on construction; no way to substitute.

**Technique:** Extract Interface. Create empty `IUserRepository`; make `UserRepository implements IUserRepository`; change `UserNotifier`'s field type. Compile — errors identify every method that must appear on the interface. Create `FakeUserRepository` for tests. Production unchanged.

---

### Example 3: Push Down Dependency (C++)

`OffMarketTradeValidator.showMessage()` calls `AfxMessageBox` (Windows MFC) and `g_dispatcher`. Cannot test validation logic without the Windows GUI framework.

**Technique:** Push Down Dependency. Make `showMessage()` pure virtual in the base class. `WindowsOffMarketTradeValidator` holds real MFC code. `TestingOffMarketTradeValidator` overrides `showMessage()` with an empty body. Tests instantiate the testing subclass — validation logic is now testable without any UI framework. (See case study cs-012 in `references/all-techniques.md`.)

---

## References

- `references/all-techniques.md` — Full step-by-step mechanics for all 24 techniques, including language-specific ones (Template Redefinition, Text Redefinition, Link Substitution, Definition Completion, Replace Function with Function Pointer) and less common ones (Primitivize Parameter, Introduce Instance Delegator, Break Out Method Object, Expose Static Method, Pull Up Feature, Introduce Static Setter, Supersede Instance Variable)
- `references/selection-table.md` — Comprehensive dependency-type × language × technique matrix; symptom-from-Ch9 → technique cross-reference; language applicability quick-ref

---

## License

This skill is derived from *Working Effectively with Legacy Code* by Michael C. Feathers (Prentice Hall, 2004). Skill content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

---

## Related BookForge Skills

**Direct dependencies (invoke before this skill):**
- `legacy-code-change-algorithm` — outer procedure; this skill executes Step 3
- `seam-type-selector` — determines seam family (object/link/preprocessor) before technique selection
- `safe-legacy-editing-discipline` — Preserve Signatures, Lean on the Compiler, Single-Goal Editing disciplines used during execution
- `test-harness-entry-diagnostics` — classifies the testability obstacle; feeds directly into Step 1 of this skill

**Cross-references (related skills):**
- `characterization-test-writing` — what to do in Step 4 (write tests) after this skill completes
- `library-seam-wrapper` — specialized wrapper skill for third-party library dependencies
- `legacy-code-symptom-router` — routes from symptom to this skill and other Part II techniques
- `legacy-code-addition-techniques` — Sprout/Wrap techniques for when you need to add code before getting under test
