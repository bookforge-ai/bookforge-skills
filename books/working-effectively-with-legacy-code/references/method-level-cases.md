# Method-Level Test Harness Obstacles (Chapter 10)

Reference for `test-harness-entry-diagnostics`. Full 4-obstacle table with detection rules, technique routing, and worked examples.

Source: *Working Effectively with Legacy Code*, Michael C. Feathers, Chapter 10 — "I Can't Run This Method in a Test Harness"

**Prerequisite:** These obstacles apply only after the class IS instantiable. If the class itself cannot be created, resolve construction obstacles first (see `class-level-cases.md`).

---

## Obstacle 1 — Method Not Accessible

**Detection:** The method to be tested is `private`, `package-private`, or otherwise inaccessible from the test file.

**Decision tree:**

1. **Can you test the behavior through a public method that calls this one?**
   - If yes: do it. Testing through public callers ensures the method is tested as it is actually used. It also prevents you from making the private method overly general.
   - If no, or if the call is deeply buried: proceed to technique below.

2. **Change `private` to `protected`, subclass in the test.**
   ```cpp
   // Production class
   class CCAImage {
   protected:
       void setSnapRegion(int x, int y, int dx, int dy);
   public:
       void snap();
   };

   // Test subclass
   class TestingCCAImage : public CCAImage {
   public:
       using CCAImage::setSnapRegion; // exposes protected method publicly
   };
   ```
   In Java/C#: Change `private` to `protected` (or package-private in Java). Subclass in test package.

3. **Reflection-based access** (Java/C# only)
   - Can be used to call private methods at runtime without code changes.
   - Feathers' position: Use sparingly. Reflection access in tests masks design problems and prevents the team from feeling the pain that would motivate better design.

**Root cause diagnosis:** If a private method is hard to test, the class likely has too many responsibilities. The method belongs on a new, smaller class. Schedule the refactoring; use the subclass approach as a bridge.

**Never for:** Accessing private *variables* (as opposed to methods) via reflection in long-lived test code. This creates invisible coupling to implementation details.

---

## Obstacle 2 — Hard to Construct Parameters

**Detection:** The method signature takes parameters that are expensive, stateful, or impossible to construct in a test (library types with no public constructors, sealed/final classes, types requiring live resources).

**This is structurally identical to class-level Cases 1, 6, and 7.** Apply the same technique routing:

- Parameter has an expensive constructor → **Extract Interface**, create a fake
- Parameter is deeply nested → **Extract Interface on outermost layer** or **Pass Null**
- Parameter is a sealed/final library class (e.g., .NET's `HttpPostedFile`) → **Adapt Parameter**

**Adapt Parameter** (specific to sealed/final library types):
- Extract an interface covering only the methods your code actually uses (e.g., `IHttpPostedFile` with `FileName` and `ContentLength`).
- Write a wrapper for the production type: `HttpPostedFileWrapper implements IHttpPostedFile`.
- Write a fake for tests: `FakeHttpPostedFile implements IHttpPostedFile`.
- Change the method signature to accept the interface type.
- Lean on the compiler to find all callers.

**Why Adapt Parameter is needed for sealed/final:** You cannot subclass these types or extract their interface directly. A wrapper class provides the indirection layer.

---

## Obstacle 3 — Method Has Bad Side Effects

**Detection:** Calling the method sends email, writes to a database, modifies a file, launches a process, or modifies shared state in ways that make the test unreliable, slow, or impossible in CI.

**Technique: Extract and Override Call**

1. Identify the specific statement that causes the side effect.
2. Extract that statement into its own protected method.
3. Override that method in a test subclass to do nothing, or to capture the call for assertion.

```java
// Before
public void performCommand(String source) {
    if (source.equals("project activity")) {
        DetailFrame detailDisplay = new DetailFrame();
        detailDisplay.setDescription(getDetailText());
        detailDisplay.show(); // side effect: opens a window
        ...
    }
}

// After extraction
protected void setDescription(String description) {
    detailDisplay = new DetailFrame();
    detailDisplay.setDescription(description);
    detailDisplay.show();
}

// Test subclass
class TestingAccountDetailFrame extends AccountDetailFrame {
    String capturedDescription = "";
    protected void setDescription(String description) {
        capturedDescription = description; // capture instead of showing
    }
}
```

**Why this works:** The side effect is now at a seam. The test subclass controls whether the side effect fires.

**Command/Query Separation note:** Methods that both produce a result and cause a side effect are the hardest to test. When extracting, try to separate the query (what does the method compute?) from the command (what does it do to the world?). Each extracted method should ideally be one or the other.

---

## Obstacle 4 — Need to Sense Effects Through an Object

**Detection:** The method produces results by mutating an object it holds internally. There is no return value and no output parameter. You need to know what the method *did*, not what it *returned*.

**Example:** `accountDetailFrame.actionPerformed(event)` — sets text on internal GUI components. No return value. No way to check the result without reading internal fields.

**Techniques:**

1. **Subclass and Override Method (Sensing Subclass)**
   - Extract the internal calls that write to objects into protected methods.
   - Override those methods in a test subclass to capture the written values.
   - Assert on the captured values in the test.

   ```java
   // Test subclass captures what would have gone to the display
   class TestingAccountDetailFrame extends AccountDetailFrame {
       String displayText = "";
       void setDisplayText(String text) {
           displayText = text; // capture instead of setting TextField
       }
   }

   // Test
   public void testPerformCommand() {
       TestingAccountDetailFrame frame = new TestingAccountDetailFrame();
       frame.accountSymbol = "SYM";
       frame.performCommand("project activity");
       assertEquals("SYM: basic account", frame.displayText);
   }
   ```

2. **Introduce a Sensing Object at a Seam**
   - If the class collaborates with another object to produce the effect, substitute a sensing fake for that collaborator.
   - The fake records calls made to it; the test asserts on the recorded calls.
   - Use `seam-type-selector` to identify which seam type (object, link, preprocessing) to exploit.

**Root cause diagnosis:** A method that is entirely side effects with no return value mixes command and query concerns. Over time, refactor toward Command/Query Separation. Test subclasses that capture state are acceptable bridge solutions.

---

## Special Cases

### Expose Static Method (alternative for deep logic in non-static context)

When a method uses little or no instance data (no `this` fields), it is a candidate for extraction into a static method or a separate utility class. A static method can be tested directly without constructing the class at all.

Use when: The method under test is long, contains important logic, but all its inputs come through parameters rather than instance fields.

### Break Out Method Object

When a method is very long, takes many parameters, and uses many local variables, it may be better extracted into its own class — a "method object." The method object can be instantiated directly in tests with full control over its inputs.

Use when: Other techniques would require constructing a very complex host object just to test one calculation.

---

*This reference supports `test-harness-entry-diagnostics`. For class-level construction obstacles, see `class-level-cases.md`.*
