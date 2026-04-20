# Four Techniques: Full Step-by-Step Mechanics

Reference file for `legacy-code-addition-techniques` skill. Contains the complete mechanical steps for all four techniques: Sprout Method, Sprout Class, Wrap Method, and Wrap Class.

The primary SKILL.md inlines Sprout Method and Wrap Method (the most common cases). This file documents Sprout Class and Wrap Class in full, plus the complete steps for Sprout Method and Wrap Method for reference completeness.

---

## Sprout Method (Method-Level + Independent)

**When:** New behavior can be formulated as a discrete sequence of statements. Source class CAN be instantiated in a test harness (or you can at minimum compile the class and call the new method statically).

**Steps:**

1. Identify the exact location in the source method where the new code must execute.
2. Write (but comment out) a call to a new method that will do the work. Choose the method name and parameter list now, based on context. The call goes in the source method at the location you identified.
   - *Reason:* Committing to the interface before implementing forces the right abstraction. It also ensures the call site in the source method is only a single line.
3. Determine which local variables from the source method the new method needs. These become its parameters.
   - *Reason:* The sprouted method must have no implicit dependencies on the source method's state — only what you pass in. This is what makes it independently testable.
4. Determine whether the sprouted method must return a value to the source method. If yes, update the commented-out call to assign its return value to a variable.
5. Develop the sprouted method using TDD: write tests against the new method in isolation, implement to make tests pass, refactor.
6. Uncomment the call in the source method to activate the integration. Build and run any available tests.

**Advantages:**
- Clear separation between new code (tested) and old code (untested).
- All variables the new code depends on are explicit as parameters — easy to reason about correctness.
- The source method does not grow; a future developer can see the sprout as a seam for further refactoring.

**Disadvantages:**
- The source method is left in an odd state: its full behavior is split between the original code and the sprout. Someone reading it may not understand why only *that* work happens in a separate method.
- This approach explicitly gives up on getting the source method itself under test *for now*.

---

## Sprout Class (Class-Level + Independent)

**When:** The source class CANNOT be instantiated in a test harness in reasonable time (constructor has too many hard-to-fake dependencies), making even Sprout Method impossible. The new behavior is logically self-contained.

**Steps:**

1. Identify where in the source method the new code must execute.
2. Think of a good name for a class that encapsulates the new work. Write (but comment out) the code that creates an object of that class and calls its method in the source method at the identified location.
   - *Reason:* Committing to the class and method name before implementing forces you to think about the right abstraction. Commenting out ensures zero risk to the source class until the new class is fully tested.
3. Determine what local variables from the source method the new class needs. These become constructor arguments for the new class.
   - *Reason:* The new class has no implicit access to the source method's state — everything it needs must be passed explicitly. This is what makes it independently testable.
4. Determine whether the new class must return values to the source method. If yes, provide a method on the new class that returns those values, and update the commented-out code to capture the return.
5. Develop the new class using TDD: write tests against the new class in isolation (it has clean dependencies — you just defined them), implement to pass, refactor.
6. Uncomment the object creation and method call in the source method. Build and run any available tests.

**Advantages:**
- You can add tested code even when the source class cannot be compiled in a test harness at all.
- The new class is a clean, well-defined unit with no legacy dependency inheritance.
- In C++, you don't need to modify the source class header file — only the implementation file — which reduces compilation dependencies.
- The new class often becomes a natural abstraction that folds into the design over time.

**Disadvantages:**
- Conceptual complexity: a new class appears in the codebase whose only reason for existence (initially) is to avoid testing the legacy class. This can be confusing to future readers.
- The source class's abstraction is fragmenting — work that logically belongs together is split across two classes. This is a design debt that must be resolved when the source class finally gets under test.

**Naming guidance:** Name the sprouted class for what it *does*, not for how it relates to the source class. `QuarterlyReportTableHeaderProducer` is acceptable temporarily; `QuarterlyReportOldStuff` is not. Good names make it easier to eventually see where the new class fits into the broader design.

**Design evolution:** Over time, when you create several sprouted classes near the same source class, you may notice they share an interface or common behavior. This is a signal that the source class is being decomposed — the sprouts are becoming the right design. At that point, consider introducing an explicit interface that both the source class and its sprouts implement.

---

## Wrap Method (Method-Level + Temporally Coupled)

**When:** New behavior must execute every time an existing method is called. The new behavior is logically independent — it should not be intermingled with the original code. Source class can be instantiated in a test harness.

**Form 1 (rename + delegate — use when all existing callers should get the new behavior automatically):**

1. Identify the method you need to change.
2. Rename the existing method to something that describes its actual function. Apply **Preserve Signatures**: copy the parameter names, types, and return type exactly; do not change them. Make the renamed method `private`.
   - *Reason:* This renames only the internal name; external callers are unaffected because you are about to recreate the original public name. Preserve Signatures is critical here — you are editing an untested method.
3. Create a new method with the **original name and original signature**. This becomes the new public entry point.
4. In the new method: call the renamed original + call a new method you will develop using TDD for the new behavior. Choose whether new behavior runs before or after the original based on the requirement.

**Form 2 (new named method — use when you want both behaviors available separately):**

1. Identify the method you want to extend.
2. Develop the new behavior as a new method using TDD.
3. Create another method (e.g., `makeLoggedPayment()`) that calls both the new behavior method and the original method.

Clients choose which method to call. This form is appropriate when adding behavior is optional or context-dependent.

**Advantages:**
- Makes temporal coupling explicit rather than implicit: the new `pay()` method visibly calls both `logPayment()` and `dispatchPayment()`, signaling that these are two distinct behaviors that happen to co-execute.
- Does not increase the size of the original method (unlike inline addition).
- The new feature is independently testable even though the caller (`pay()`) may not be.

**Disadvantages:**
- You must invent a new name for the original code. Often the new name reveals that the original method was already doing too much (good signal), but it can also produce awkward names like `dispatchPayment()` for code that both calculates *and* dispatches.
- When no refactoring tool is available and the code is brittle, renaming is risky. Apply Preserve Signatures strictly.

---

## Wrap Class (Class-Level + Temporally Coupled — Decorator Pattern)

**When:** New behavior must co-execute with an existing class method, AND one of these is true:
- The new behavior is logically independent and should not pollute the source class
- The source class has grown so large that any addition makes it worse
- The same new behavior needs to be composable across multiple callers

**Steps:**

1. Identify the method where new behavior must co-execute.
2. Create a new class that accepts the source class as a constructor argument (the wrapper). If you cannot instantiate the source class in a test harness, apply Extract Implementer or Extract Interface to the source class first, so that both the source class and the wrapper implement the same interface.
   - *Reason:* The wrapper must be substitutable for the source class at call sites. If no shared interface exists, callers can't use the wrapper without knowing its type.
3. On the wrapper, using TDD: implement the new behavior as one method; implement the co-execution method with the original name that calls the new behavior method AND delegates to the wrapped source class instance.
4. Replace object instantiation in the code path where new behavior is needed: create the wrapper instead of the source class, passing the source class instance to the wrapper's constructor.

**Decorator pattern note:** The full Decorator pattern allows wrapping the wrapper, enabling combinatorial behavior at runtime. For example:
```java
ToolController controller = new StepNotifyingController(
    new AlarmingController(new ACMEController()), notifyees);
```
Use full Decorator when the set of combinable behaviors is open-ended. When you only need to add behavior in one or two places, a simpler (non-combinable) wrapper class is sufficient:
```java
class LoggingPayDispatcher {
    private Employee e;
    public LoggingPayDispatcher(Employee e) { this.e = e; }
    public void pay() {
        e.pay();
        logPayment();
    }
    private void logPayment() { ... }
}
```

**Advantages:**
- Full separation of concerns at the class level: the source class is not modified at all.
- Transparently applies new behavior to all existing callers of the wrapped interface.
- The wrapper class is developed entirely with TDD — it has clean dependencies.
- Enables composable behavior via the Decorator pattern.

**Disadvantages:**
- Higher structural overhead than Sprout Method or Wrap Method for simple additions.
- Navigating decorator-wrapped code ("peeling the onion") can be disorienting. Use sparingly.
- Requires an interface or base class to be substitutable. If no interface exists, Extract Interface adds upfront work.

**Choosing between Decorator and simple wrapper:**
- Many callers need the new behavior → Decorator (transparent substitution at all call sites)
- Only one or two places need it → Simple wrapper (less structure, easier to understand)

---

## Summary: All Four Techniques Leave Old Code in Place

All four techniques are *temporary* solutions. Their purpose is to let you add tested code to the system under time pressure, without requiring you to immediately get the legacy source class fully under test.

When you apply any of these techniques, document the resulting design debt immediately in `refactor-backlog.md`. The techniques buy time; they do not eliminate the need for eventual proper refactoring of the source class.

The signal that it is time to pay down the debt: you keep returning to the same source class to make changes, and each visit requires another sprout or wrap. At that point, the accumulation of sprouts/wrappers *around* the source class is giving you a map of what the source class should actually be refactored into.

Source: Working Effectively with Legacy Code by Michael C. Feathers (2004, Prentice Hall), Chapter 6.
