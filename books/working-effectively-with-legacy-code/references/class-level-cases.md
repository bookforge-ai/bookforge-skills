# Class-Level Test Harness Cases (Chapter 9)

Reference for `test-harness-entry-diagnostics`. Full 7-case table with detection rules, technique routing, and trade-off notes.

Source: *Working Effectively with Legacy Code*, Michael C. Feathers, Chapter 9 — "I Can't Get This Class into a Test Harness"

---

## Root Cause Map

| Root Cause | Cases |
|-----------|-------|
| Objects can't be created easily | Case 1 (Irritating Parameter), Case 6 (Onion Parameter), Case 7 (Aliased Parameter) |
| Harness won't build with the class | Case 5 (Horrible Include Dependencies — C++ only) |
| Constructor has bad side effects | Case 2 (Hidden Dependency), Case 3 (Construction Blob) |
| Significant work in constructor; need to sense | Case 3 (Construction Blob with sensing), Case 4 (Irritating Global Dependency) |

---

## Case 1 — Irritating Parameter

**Detection:** A constructor parameter type has a constructor of its own that causes side effects (network connection, file I/O, process launch). The parameter IS passed in explicitly. The class under test does not create it — the caller does. The problem is that creating the parameter is painful.

**Example:** `CreditValidator(RGHConnection connection, CreditMaster master, String id)` — `RGHConnection` connects to a server on construction.

**Techniques (in preference order):**

1. **Extract Interface** on the problematic parameter type. Create a fake implementation for tests.
   - When to use: You need some behavior from the parameter during the test.
   - Trade-off: Requires modifying production code to use the interface type.

2. **Pass Null** for the parameter.
   - When to use: The code path under test never actually uses the parameter. Confirm by running — a NullPointerException means the parameter IS used.
   - Trade-off: Only valid in garbage-collected languages (Java, C#). Not safe in C/C++ without null-checking runtime support.
   - Rule: Never pass null in production code.

3. **Subclass and Override Method** on the parameter type.
   - When to use: The side effect is isolated to a specific method on the parameter type (e.g., `connect()`), and the constructor of that type calls it.
   - Trade-off: Only works if the method in question is overridable (not final/sealed).

---

## Case 2 — Hidden Dependency

**Detection:** The constructor uses `new SomeService()` or a static call internally — the dependency is not in the parameter list. There is no way to substitute the dependency from outside the class.

**Example:** `mailing_list_dispatcher()` constructor calls `new mail_service` in its initializer list.

**Primary technique: Parameterize Constructor**
- Extract the `new` expression outside the constructor.
- Add a constructor overload accepting the dependency as a parameter.
- Preserve the original constructor (for production callers) as a delegating constructor: `MyClass() { this(new RealService()); }`.
- In C++, extract the constructor body into an `initialize(service*)` method, then provide both constructors.

**Secondary techniques (when Parameterize Constructor is inconvenient):**
- **Extract and Override Getter** — add a protected getter that returns the dependency; override in test subclass.
- **Extract and Override Factory Method** — extract the `new` call into a protected factory method; override in test subclass.
- **Supersede Instance Variable** — add a setter that replaces the instance after construction (C++ only, with care).

**Trade-off:** Parameterize Constructor exposes the dependency in the API. If many callers exist, the no-arg delegating constructor shields them.

---

## Case 3 — Construction Blob

**Detection:** The constructor creates several objects in sequence, often where one created object is passed into the next. You need to sense through or substitute one of the internally-created objects. Parameterizing the constructor would require passing too many parameters.

**Example:** `WatercolorPane(Form, WashBrush, Pattern)` creates `anteriorPanel`, `backgroundPanel`, and `cursor` internally.

**Techniques:**

1. **Extract and Override Factory Method** (Java and C# only)
   - Extract the object-creation code for the object you need to sense into a `protected` factory method.
   - Override in a test subclass to return a fake or testing implementation.
   - Why C++/C++ cannot use this: C++ constructors do not dispatch virtual calls to derived-class overrides. The override will not be called during base-class construction.

2. **Supersede Instance Variable**
   - Add a setter (e.g., `void supersedeCursor(FocusWidget* newCursor)`) that replaces the internally-created object.
   - Call the constructor normally, then call the setter to substitute the test double.
   - C++ warning: The setter must delete the old object to avoid memory leaks. Understand what the destructor does before using this technique.
   - Java/C#: No cleanup needed (garbage collector handles the replaced reference).
   - Rule: Never call superseding methods in production code.

---

## Case 4 — Irritating Global Dependency (Singleton)

**Detection:** The constructor calls `SomeClass.getInstance()` or accesses a static variable. The singleton enforces a single instance via a private constructor, preventing substitution.

**Example:** `Facility` constructor calls `PermitRepository.getInstance().findAssociatedPermit(notice)`.

**Techniques:**

1. **Introduce Static Setter**
   - Add `public static void setTestingInstance(T instance)` to the singleton class.
   - In test setUp: create a real or fake instance, call the setter before each test.
   - In test tearDown: reset to null or to the production singleton.
   - Change the constructor visibility from private to protected to allow subclassing.

2. **Extract Interface on the singleton**
   - Change the static field type from the concrete class to an interface.
   - In tests, pass a fake implementation through the static setter.
   - Required when: the singleton performs side effects (DB, network) that must not run in tests.

3. **Add `resetForTesting()` method**
   - Alternative to static setter. Sets the static instance to null so the singleton re-initializes itself on next `getInstance()` call.
   - Use when: the singleton's public methods are sufficient to set up test state directly.

**Trade-off:** The static setter "relaxes" the singleton property. Protect against production use with a build rule or runtime assertion (check call stack or environment flag).

---

## Case 5 — Horrible Include Dependencies (C++ only)

**Detection:** Adding `#include "TargetClass.h"` in the test file triggers a cascade of transitively included headers. The test binary fails to compile, takes excessively long to compile, or requires linking against libraries unavailable in the test environment.

**Example:** `Scheduler` includes `Meeting.h`, `MailDaemon.h`, `SchedulerDisplay.h`, etc.

**Technique: Definition Completion**
- Identify the specific included class that causes the problem (e.g., `SchedulerDisplay`).
- In the test file (or a `Fakes.h` file), provide stub definitions for just the methods that are actually called:
  ```cpp
  void SchedulerDisplay::displayEntry(const std::string& description) { }
  ```
- Place the test binary in a separate build target — you can have only one definition per method per program.
- Reuse stubs across test files by placing them in `Fakes.h`.

**Trade-off:** Stub definitions must be maintained as long as the tests exist. Reserve for severe dependency cases. This technique does not improve the production design — it is a test-only workaround.

---

## Case 6 — Onion Parameter

**Detection:** The constructor needs Object A. Object A's constructor needs Object B. Object B's constructor needs Object C. The creation chain is nested several levels deep. No single "extract interface" handles it without working through every layer.

**Example:** `SchedulingTaskPane(SchedulingTask task)` → `SchedulingTask(Scheduler, MeetingResolver)` → further dependencies.

**Techniques (in preference order):**

1. **Extract Interface on the outermost layer**
   - The outermost parameter is `SchedulingTask`. Create `ISchedulingTask`.
   - Write a `FakeSchedulingTask implements ISchedulingTask` that is trivial to construct.
   - You do not need to descend deeper into the chain.
   - C++ note: If the outermost class inherits from a base class with pure virtual methods, you may need to add delegation methods to satisfy the compiler.

2. **Pass Null**
   - If the outermost parameter is not used in the code path under test, pass null.
   - Confirm safety by running — NullPointerException means the parameter is used.

---

## Case 7 — Aliased Parameter

**Detection:** A parameter type inherits from a base class. That same base class is used as the type of an instance variable. You cannot extract an interface for the parameter without also making the instance variable use the interface — requiring a cascading redesign of the class hierarchy.

**Example:** `IndustrialFacility(int, String, OriginationPermit permit)` — `OriginationPermit extends FacilityPermit extends Permit`. The `basePermit` field is typed as `Permit`. Assigning an `IOriginationPermit` to `Permit` would not compile.

**Technique: Subclass and Override Method**
- Identify the specific method on the parameter type that causes the problem (e.g., `validate()` which hits the database).
- Create a test subclass of the parameter type.
- Override only the problematic method.
- In the test, pass an instance of the test subclass.

```java
public void testHasPermits() {
    class AlwaysValidPermit extends FakeOriginationPermit {
        public void validate() { becomeValid(); }
    };
    Facility facility = new IndustrialFacility(
        Facility.HT_1, "b", new AlwaysValidPermit());
    assertTrue(facility.hasPermits());
}
```

**Trade-off:** Requires the problematic behavior to be isolated in a single, overridable method. If the dependency is intermingled with logic you need, extract methods first (potentially using a refactoring tool) to isolate the side effect before subclassing.

---

*This reference supports `test-harness-entry-diagnostics`. For method-level obstacles, see `method-level-cases.md`.*
