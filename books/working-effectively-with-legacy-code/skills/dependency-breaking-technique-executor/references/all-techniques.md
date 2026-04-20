# All 24 Dependency-Breaking Techniques

Full step-by-step mechanics for every technique in Chapter 25 of *Working Effectively with Legacy Code* (Feathers, 2004). Techniques are listed alphabetically, as in the book. Each entry includes: purpose, numbered steps, language applicability, cross-references to related techniques, and trade-offs.

---

## 1. Adapt Parameter

**Purpose:** Replace a concrete parameter type with a new interface when the parameter class is difficult to construct or cannot be modified (third-party, sealed, or too tangled).

**When to use:** When a method receives a concrete class you do not own or cannot easily fake, and extracting an interface directly from that class is not feasible. Prefer Extract Interface when you _can_ modify the parameter class.

**Steps:**
1. Create a new interface that exposes only the operations your method actually needs. Name it communicatively (e.g., `Readable`, `Queryable`). Keep it as narrow as possible.
2. Create a production implementation of the new interface that wraps or delegates to the original concrete type.
3. Create a fake implementation of the interface for tests.
4. Write a simple test case passing the fake to the method.
5. Modify the method to use the new interface type as its parameter instead of the concrete class.
6. Run tests to verify the method works via the interface.

**Language applicability:** All OO languages (Java, C#, C++, Python, Ruby). In languages without explicit interfaces, use an abstract base class or duck typing.

**Cross-references:** Extract Interface (simpler when you own the parameter class); Parameterize Method (alternative for factory-method-like creation inside the method body).

**Trade-offs:** Creates an extra wrapper class (production implementer). The interface is narrow and may need expansion if the method's usage of the parameter grows. Prefer over Adapt Parameter when you own the parameter class and can extract an interface directly.

---

## 2. Break Out Method Object

**Purpose:** Move a large method (especially one that uses many instance variables) into its own class, enabling the method to be tested independently without requiring the original class to be instantiated.

**When to use:** When a method is long (50+ lines), uses many instance variables, cannot be extracted as a static method, and the original class is difficult to instantiate. Prefer Expose Static Method for shorter, purer methods that do not need instance data.

**Steps:**
1. Create a new class to house the method. Name it after the method (e.g., method `generateReport()` → class `ReportGenerator`).
2. Create a constructor for the new class. Using Preserve Signatures, give it an exact copy of the original method's argument list. If the method uses instance variables of the original class, add a reference to the original class as the first constructor argument.
3. Declare instance variables for each argument and for the original-class reference (if needed). Assign them in the constructor.
4. Create an empty execution method, often named `run()`.
5. Copy the body of the original method into the `run()` method.
6. Attempt to compile. Lean on the Compiler: error messages identify every remaining reference to original class members. For each, decide whether to:
   - Pass it as an additional constructor argument (adds to the method object's state)
   - Access it via the original-class reference
   - Make it a local variable in `run()` if it does not need to survive multiple calls

**Language applicability:** All OO languages. In C++, take care with memory ownership and the lifetime of the original-class reference.

**Cross-references:** Expose Static Method (simpler for short pure methods); Pull Up Feature (alternative when only some methods need to be separated); monster method decomposition for the follow-on refactoring.

**Trade-offs:** Introduces a new class for every method extracted, which can fragment the design. Best used when the method object reveals a genuine responsibility. The new class starts with a constructor that mirrors the original method's parameter list — this is intentionally ugly; refine once tests exist.

---

## 3. Definition Completion

**Purpose:** Break C++ header-inclusion chains by providing a stub definition for a type in a test-specific file, allowing compilation to proceed without pulling in the full production headers.

**When to use:** C++ codebases only. When a class under test `#include`s headers that transitively pull in platform-specific, hardware, or OS headers that cannot compile in the test environment.

**Steps:**
1. Identify the header that causes the include chain problem.
2. In your test file (or a test-specific `.cpp`), provide a minimal definition of the problematic type — enough for compilation but with empty or stub implementations. Do not `#include` the problematic header.
3. Link the test binary using only the stub definitions. Production code links against the real definitions.

**Language applicability:** C++ only. This technique exploits the C++ One Definition Rule (ODR) in test builds where it is acceptable to provide a different definition for testing.

**Cross-references:** Link Substitution (build-level equivalent for replacing whole translation units); Replace Function with Function Pointer (per-function granularity in C).

**Trade-offs:** Fragile — stub definitions must stay in sync with the real type's interface. Requires careful management of include guards and build targets. Use only when OO techniques are not viable.

---

## 4. Encapsulate Global References

**Purpose:** Wrap free-standing global variables and functions into a class, enabling replacement in tests via subsequent parameterization, getter override, or static setter.

**When to use:** When the same global variable or function appears across multiple methods of a class, making per-method extraction techniques too expensive. For a single-method usage, prefer Replace Global Reference with Getter.

**Steps:**
1. Identify the globals you want to encapsulate. Group logically related globals together (connection state, platform services, etc.).
2. Create a class to hold them. Give it a meaningful name.
3. Copy the global variable declarations as instance variables and the function signatures as method declarations into the class. Copy implementations if the functions are defined in the same translation unit.
4. Comment out the original global declarations. Keep the definitions for now (they will be removed once compilation succeeds).
5. Declare a global instance of the new class (e.g., `extern NetworkGlobals g_network;`).
6. Lean on the Compiler: compile; each error points to a usage of the old global. Navigate to it.
7. Prefix each formerly-global reference with the global instance name (e.g., `g_network.openConnection()`).
8. Now choose a follow-on technique to make the encapsulated globals replaceable in tests:
   - **Introduce Static Setter** — if the global instance should be replaceable as a singleton
   - **Parameterize Constructor** — pass the globals-object into the class that uses it
   - **Parameterize Method** — pass it into a specific method
   - **Replace Global Reference with Getter** — per-method override via subclassing

**Language applicability:** Primarily C/C++ (designed for C-era global variables). Applicable in any language with global mutable state. Less useful in Java/C# where static singletons are the typical global-state pattern (use Introduce Static Setter there).

**Cross-references:** Replace Global Reference with Getter (localized single-method alternative); Introduce Static Setter (singleton-level replacement after encapsulation); Parameterize Constructor (inject the encapsulated object).

**Trade-offs:** 8-step process — most complex technique in the catalog. Rewards effort when globals are pervasive. Creates a new class that may expose previously implicit coupling.

---

## 5. Expose Static Method

**Purpose:** Make a method testable by converting it to a public static method, enabling direct invocation without constructing the problematic class.

**When to use:** When a method does not use instance data (or can be made not to), and the class cannot be instantiated in the test harness. For methods that do use instance data, use Break Out Method Object instead.

**Steps:**
1. Write a test that calls the method as a public static method on the class.
2. Extract the body of the method to a public static method. Apply Preserve Signatures — use parameter names from the original to guide naming (e.g., `validate(Packet p)` → `validatePacket(Packet p)` as a static).
3. Compile.
4. If compilation errors arise from instance variable or method accesses inside the extracted static: examine each and determine if it can be made static. If it can, make it static. If it cannot, the method has instance dependencies and Break Out Method Object is a better fit.

**Language applicability:** All OO languages. In Java, `static` is explicit. In C++, use `static` member function. In Python, use `@staticmethod`. Not applicable to methods with essential instance state that cannot be passed as parameters.

**Cross-references:** Break Out Method Object (for methods with instance data that cannot be made static); Parameterize Method (if the instance data can be passed as a parameter rather than accessed via `this`).

**Trade-offs:** Produces a static method, which can become a design smell if overused. The technique is a temporary testability bridge — once the class is under test, consider whether the method should remain static or be refactored back to an instance method.

---

## 6. Extract and Override Call

**Purpose:** Break a dependency on a specific method call (especially a static call) by extracting the call into a new overridable instance method that a test subclass can override.

**When to use:** When a method contains a specific call to a static method, global function, or hard-coded collaborator, and that call is the only problematic dependency. For global dependencies spread across multiple methods, Encapsulate Global References is more efficient.

**Steps:**
1. Identify the call to extract. Find the declaration of the called method. Copy its signature (Preserve Signatures).
2. Create a new protected method on the current class using the copied signature. The method body is the extracted call expression.
3. Replace the original call site with a call to the new method using `this` (in languages with implicit `this`, this is automatic; in C++, it may be necessary to be explicit).
4. Create a testing subclass that overrides the new method to do nothing, return a safe value, or sense what was passed.

**Language applicability:** All OO languages supporting method override. In C++, the new method must be `virtual`.

**Cross-references:** Extract and Override Factory Method (for constructor-time creation dependencies); Subclass and Override Method (for overriding the method that contains the call, rather than extracting the call out); Encapsulate Global References (when the same call appears in many methods).

**Trade-offs:** Creates one extraction per problematic call. Multiplies quickly if the same global is called in many places. The extracted method is a testing seam, not a production abstraction — name it accordingly and remove it in the next refactoring pass if a cleaner abstraction emerges.

**Case study:** PageLayout.rebindStyles() calling `StyleMaster.formStyles(template, id)` (static). After extraction: `rebindStyles()` calls `this.formStyles(template, id)`; `TestingPageLayout` overrides `formStyles()` to return empty list. (cs-011)

---

## 7. Extract and Override Factory Method

**Purpose:** Replace object creation inside a constructor with a call to an overridable factory method, enabling test subclasses to return fakes without modifying production behavior.

**When to use:** When a constructor creates one or more objects via `new`, and the creation is more complex than a simple `new Type(args)` — it involves multiple steps, configuration, or inter-object initialization. For simple single-object creation, Parameterize Constructor is simpler. Not applicable in C++ (no virtual dispatch in constructors) — use Extract and Override Getter instead.

**Steps:**
1. Identify the object creation inside the constructor.
2. Extract all of the creation logic into a new protected method with a name like `createXxx()`. The method returns the created object. The constructor calls the factory method and assigns the result.
3. Create a testing subclass that overrides the factory method to return a fake or null.

**Language applicability:** Java, C#, Python, Ruby, and any language where virtual dispatch is active during construction. **Not applicable in C++** — virtual table is not fully set up during C++ constructor execution.

**Cross-references:** Extract and Override Getter (C++ alternative using lazy initialization); Supersede Instance Variable (C++ fallback when getter is not viable); Parameterize Constructor (simpler alternative for single-object creation).

**Trade-offs:** Leaves production code with a factory method that is only overridable for testing purposes. The factory method can grow into a proper Abstract Factory if warranted, but do not refactor it during the dependency-breaking step.

---

## 8. Extract and Override Getter

**Purpose:** Replace an object dependency in constructors using lazy initialization: the object is created on first access via a getter that is overridable in a test subclass. Specifically designed for C++ where virtual dispatch is not available in constructors.

**When to use:** C++ primarily. When Extract and Override Factory Method is not viable because the language prohibits virtual calls in constructors. Also useful in Java/C# when lazy initialization is an acceptable design trade-off.

**Steps:**
1. Identify the object you need a getter for.
2. Extract all logic needed to create the object into a getter method (e.g., `getXxx()`). The getter is `virtual` in C++, `virtual` in C#, non-final in Java.
3. Replace all direct accesses to the object inside the class with calls to the getter.
4. Initialize the instance variable to `null` (or `nullptr` in C++) in all constructors. Do not create the object in the constructor.
5. Add first-time (lazy) logic to the getter: if the variable is null, create and assign the object; then return it.
6. In a test subclass, override the getter to return a fake object instead.

**Language applicability:** C++ (primary use case), Java, C#. Not idiomatic in Python/Ruby where late binding makes this unnecessary.

**Cross-references:** Extract and Override Factory Method (Java/C# alternative without lazy initialization); Supersede Instance Variable (alternative when you cannot use a getter); Subclass and Override Method (same overriding pattern applied to methods other than getters).

**Trade-offs:** Introduces lazy initialization, which adds complexity and can cause threading issues in concurrent code (non-atomic lazy init). Not recommended as a permanent design — replace with proper constructor injection once tests are established.

---

## 9. Extract Implementer

**Purpose:** Convert an existing concrete class into an interface by making the class itself the interface and creating a new production implementation class. Use when you want the interface to have the same name as the current class.

**When to use:** When Extract Interface is the right approach but the desired interface name is already the class name (the most common case — `UserRepository` should become an interface named `UserRepository`). Compare to Extract Interface, where the interface gets a new name and the existing class keeps its name.

**Steps:**
1. Make a copy of the source class declaration. Give the copy a different name (convention: prefix with `Production`, e.g., `ProductionUserRepository`, or a more descriptive name).
2. Turn the original source class into an interface: delete all non-public methods, all instance variables, and all method bodies. Make all remaining public methods abstract (in Java: `abstract` on the class; in C++: `= 0` on all methods).
3. Make the production class (the copy from step 1) implement the interface.
4. Lean on the Compiler to find import/include cleanup needed.
5. Compile the production class to verify all method signatures from the interface are implemented.
6. Compile the rest of the system. Find all places where the original class was instantiated (`new UserRepository(...)`). Change each to instantiate the production class (`new ProductionUserRepository(...)`).
7. Recompile and run tests.

**Language applicability:** Java, C#, C++ (as abstract base class). In C++, "interface" means a class with all pure virtual methods.

**Cross-references:** Extract Interface (use when you want a different name for the interface — existing class keeps its name); Adapt Parameter (use when you cannot modify the parameter class at all).

**Trade-offs:** Requires touching every instantiation site. In large codebases, this can be a significant change. Lean on the Compiler makes it systematic. The resulting production class name (e.g., `ProductionUserRepository`) may be permanent or may be renamed once a better name is found.

---

## 10. Extract Interface

**Purpose:** Create a minimal interface from a concrete class so that the class and test fakes can both implement it, breaking the dependency on the concrete type at a usage site.

**When to use:** When a parameter, field, or local variable is typed to a concrete class that you need to substitute in tests. The most widely-used technique in the catalog. Prefer over Extract Implementer when the desired interface name differs from the existing class name.

**Steps:**
1. Create a new interface with the name you want. Add no methods yet. Compile — this is a clean compile since the empty interface does not affect anything.
2. Make the concrete class implement the new interface. Compile and run tests — nothing should break since the interface is empty.
3. Change the target location (parameter type, field type, local variable) to use the interface type instead of the concrete class.
4. Compile. Each method call on the variable that the compiler reports as an error is a method that needs to appear on the interface. Add them one at a time, guided by compiler errors.

**Why compile-guided discovery matters:** Only add methods that the actual usage needs. Do not copy all public methods from the concrete class. A minimal interface is easier to implement with fakes.

**Language applicability:** All OO languages. In C++, an "interface" is an abstract base class with pure virtual methods (`= 0`). In Python/Ruby, duck typing makes formal interfaces optional — but an abstract base class documents intent.

**C++ warning:** Non-virtual methods on the concrete class will not be overridable via the abstract base. If usage sites call non-virtual methods, those must be made virtual or the technique must be combined with Extract Implementer.

**Cross-references:** Extract Implementer (use when the interface name should match the existing class name); Adapt Parameter (use when you cannot modify the parameter class at all); Parameterize Constructor (use when the dependency is in the constructor and an interface alone is not sufficient).

**Trade-offs:** The most universally applicable technique. If one technique should be the default, this is it for OO languages with parameter/field dependencies.

---

## 11. Introduce Instance Delegator

**Purpose:** Make a static method call testable by adding an instance method that delegates to the static, enabling the instance to be substituted via Parameterize Method or similar techniques.

**When to use:** When a class calls a static method on itself or another class, and the static cannot be easily extracted or overridden directly. Converts the static seam problem into an object seam problem.

**Steps:**
1. Identify the static method call that is problematic in tests.
2. Create an instance method on the same class that delegates to the static method. Preserve Signatures — same parameter list and return type.
3. Find every place in the class under test where the static method is called. Use Parameterize Method (or Parameterize Constructor) to supply an instance of the class as a parameter. Replace the static call with an instance method call on the supplied object.

**Language applicability:** All OO languages. Primarily useful in Java/C# where static methods are common on utility classes. In Python, class methods serve a similar function.

**Cross-references:** Parameterize Method (follow-on technique to inject the instance); Extract and Override Call (alternative when the static call is localized and subclassing is easier than parameterization); Replace Function with Function Pointer (procedural C alternative).

**Trade-offs:** Adds a delegation method that exists solely for testability. The method is not design-motivated. Mark it as a testing seam in a comment and plan to refactor.

---

## 12. Introduce Static Setter

**Purpose:** Make a singleton object replaceable in tests by adding a static setter method that allows test code to inject a different instance. Bypasses global mutable state without restructuring the singleton pattern.

**When to use:** When production code accesses a singleton (global instance) and tests need a different behavior from that singleton. Most applicable after Encapsulate Global References has grouped globals into a singleton-like object.

**Steps:**
1. Decrease the protection of the singleton's constructor so that you can create a subclass or a fake (protected access is usually sufficient).
2. Add a static setter method to the singleton class: `static void setTestingInstance(MySingleton* s)`. The setter should assign the new instance to the singleton's static pointer. **Important:** destroy or release the previous instance before setting the new one to prevent memory leaks or dangling pointers.
3. If test code needs to access private or protected members of the singleton to configure it, consider two alternatives:
   - Subclass the singleton and expose needed members via the subclass
   - Extract an interface from the singleton and hold the instance as the interface type; test code provides a clean fake

**Language applicability:** All OO languages with static members. In Java/C#, this is straightforward. In C++, be careful with memory ownership.

**Cross-references:** Encapsulate Global References (step that often precedes this technique by grouping globals into a singleton); Extract Interface (follow-on to enable full substitution); Replace Global Reference with Getter (per-method alternative that avoids modifying the singleton class).

**Trade-offs:** Introduces a writable singleton — a known concurrency hazard. Tests must reset the singleton after use, or tests may interfere with each other. Add teardown cleanup. The pattern is a stepping stone, not a final design.

---

## 13. Link Substitution

**Purpose:** Replace production implementations at the linker/build level with fake ones for testing. The test binary is built with alternative implementations substituted for the production ones, without changing source code.

**When to use:** When whole libraries, translation units, or sets of functions need to be faked, and the codebase is C/C++ or Java (classpath substitution). Most useful for library-level dependencies where per-method techniques are too granular.

**Steps:**
1. Identify the functions or classes you want to fake.
2. Produce alternative definitions: stub implementations that record calls, return safe values, or do nothing. Place them in a separate file that is only included in the test build.
3. Adjust the build system (Makefile, CMakeLists.txt, classpath, IDE settings) so that the test binary links against the alternative definitions instead of the production ones.

**Language applicability:** C/C++ (linker-level), Java (classpath substitution — replace a JAR or individual class files). Not directly applicable in C# (use different approaches for assembly substitution). Not applicable in interpreted languages (use Text Redefinition instead).

**Cross-references:** Definition Completion (C++ header-level alternative for faking type definitions); Replace Function with Function Pointer (more granular — per-function at runtime); Template Redefinition (C++ compile-time alternative for template-based code).

**Trade-offs:** Requires build system modifications that may be opaque to team members unfamiliar with build internals. Alternative definitions must track the interface of the real implementations. Prefer OO techniques for production code; use Link Substitution for tests in legacy C codebases with no OO structure.

---

## 14. Parameterize Constructor

**Purpose:** Externalize object creation from a constructor by making the created object a constructor parameter, allowing tests to pass in a fake.

**When to use:** The most common dependency-breaking technique for constructor-level dependencies. Use when a constructor hard-codes `new ConcreteType(...)` and the goal is to allow a fake to be passed in tests. Prefer over Extract and Override Factory Method when the creation is simple (one object, minimal configuration).

**Steps:**
1. Identify the constructor you want to parameterize. Copy the full constructor signature (Preserve Signatures).
2. Create a new constructor that takes all the original parameters **plus one additional parameter** for the object being replaced. Remove the `new` expression in the new constructor and assign the parameter to the instance variable.
3. Modify the original constructor's body to call the new parameterized constructor, passing `new ConcreteType(...)` as the additional argument. If your language supports constructor delegation (`this(...)` in Java, delegating constructors in C++11), use it. If not, extract shared initialization to a private `initialize()` method.

**Language applicability:** All OO languages. Java supports `this(...)` delegation cleanly. C++11 supports delegating constructors. C++03 requires the `initialize()` method pattern.

**Cross-references:** Parameterize Method (same pattern for methods instead of constructors); Extract and Override Factory Method (use when creation is complex or chained); Supersede Instance Variable (fallback in C++ for post-construction replacement).

**Trade-offs:** Leaves two constructors — one for tests, one for production. The production constructor remains the default; production callers are unchanged. Clean up by removing the no-arg constructor once all callers have been migrated to dependency injection, but only after tests exist.

**Case study:** `mailing_list_dispatcher` C++ constructor allocating `mail_service` with `new` and calling `connect()` on it — untestable without live mail server. After parameterization: tests pass `&fakeMailService`. (cs-005)

---

## 15. Parameterize Method

**Purpose:** Externalize object creation from a method body by making the created object a method parameter, allowing tests to pass a fake. The original method signature is preserved via a delegating wrapper.

**When to use:** When a method (not a constructor) hard-codes `new ConcreteType(...)` and you need to intercept the creation. Mirror of Parameterize Constructor applied to methods.

**Steps:**
1. Identify the method containing the object creation. Copy its signature.
2. Create a new version of the method with all the original parameters **plus one additional parameter** for the object being replaced. Remove the creation expression from the new method.
3. Give the original method a new body: call the parameterized method, passing `new ConcreteType(...)` as the extra argument.

**Language applicability:** All OO languages. Method overloading is the mechanism in Java/C++/C#. In languages without overloading (Python, Ruby), use keyword arguments with a default.

**Cross-references:** Parameterize Constructor (same pattern for constructors); Introduce Instance Delegator (when the dependency is a static method call rather than an object creation); Extract and Override Call (when extracting the call is easier than parameterizing it).

**Trade-offs:** Same two-overload pattern as Parameterize Constructor. The wrapper method delegates to the parameterized version. Clean up by removing the wrapper once dependency injection is established at a higher level.

---

## 16. Primitivize Parameter

**Purpose:** Replace a complex parameter with primitive data (values extracted from it) to test a method without constructing the complex parameter. A last-resort technique when interface extraction is not feasible.

**When to use:** When a method parameter is so difficult to construct or fake that no other technique is applicable, and all you actually need from the parameter is a small number of primitive values. Feathers describes this as "somewhat distasteful" — commit to proper interface extraction later.

**Steps:**
1. Identify which fields or methods of the parameter the target method actually uses.
2. Create a new method that accepts those fields/methods as primitive parameters instead of the complex type.
3. Have the original method call the new method, passing the extracted values.
4. Test the new primitive-parameter method directly.

**Language applicability:** All languages.

**Cross-references:** Adapt Parameter (preferred — creates a proper interface instead of primitives); Extract Interface (preferred when the parameter class can be modified).

**Trade-offs:** Creates a primitive-parameter method that is not representative of the real production interface. The test covers logic but not integration with the real parameter type. Use only as a temporary measure and document the technical debt.

---

## 17. Pull Up Feature

**Purpose:** Move the methods you want to test into a new abstract superclass, leaving bad dependencies in the original class. Test code can instantiate a concrete subclass of the abstract class without pulling in the bad dependencies.

**When to use:** When the methods you want to test do not reference the bad dependencies and can be lifted to a superclass. Contrast with Push Down Dependency, which pushes bad dependencies *down* rather than pulling good methods *up*. Use Pull Up Feature when the good methods are self-contained; use Push Down Dependency when the bad dependencies are concentrated in a few methods.

**Steps:**
1. Identify the methods you want to test (the "good" methods that do not use bad dependencies).
2. Create an abstract superclass for the current class.
3. Copy the identified methods to the superclass and compile.
4. For every missing reference (variable or method) the compiler reports, copy that reference to the superclass (Preserve Signatures). Repeat until compilation succeeds.
5. Create a concrete testing subclass of the abstract superclass. Add whatever helper methods or properties are needed to set it up in tests. Verify that the subclass can be instantiated in the test harness.

**Language applicability:** All OO languages.

**Cross-references:** Push Down Dependency (inverse — push bad dependencies down; use when good methods are numerous or when there are too many dependencies to pull up around); Break Out Method Object (alternative when methods use instance data that cannot be cleanly pulled up).

**Trade-offs:** Introduces inheritance solely for testability. The superclass/subclass relationship may not reflect a genuine domain abstraction. Clean up by evaluating whether the superclass reveals a real responsibility after tests are established.

---

## 18. Push Down Dependency

**Purpose:** Isolate bad dependencies into a concrete subclass, making the original class abstract. Tests can instantiate a test subclass of the abstract class that neutralizes the bad dependencies.

**When to use:** When a few methods in a class have bad dependencies (UI, network, hardware) but most of the logic is fine. Rather than testing around each call site, push all bad dependencies into a dedicated production subclass and create a testing subclass that overrides them away. Contrast with Pull Up Feature (pull good methods up) — use Push Down Dependency when the bad methods are few and concentrated.

**Steps:**
1. Attempt to build the class in your test harness. Note which dependencies create problems.
2. Identify which instance variables and methods contain those problematic dependencies.
3. Create a new subclass with a name that communicates the specific environment (e.g., `WindowsOffMarketTradeValidator` for an MFC-dependent validator).
4. Copy the instance variables and methods containing the bad dependencies to the new subclass. In the original class, make those methods `protected` and `abstract` (or `pure virtual` in C++). Make the original class abstract.
5. Create a testing subclass of the abstract base. Override the now-abstract methods with empty bodies or safe return values.
6. Build and run tests against the testing subclass. The core logic in the abstract base is now exercisable.

**Language applicability:** All OO languages.

**Cross-references:** Pull Up Feature (inverse direction — pull good methods up); Subclass and Override Method (lighter-weight version when you don't want to make the class abstract); Extract and Override Call (for a single localized problematic call).

**Trade-offs:** Makes the class abstract, requiring an instantiable subclass for every usage (production and test). In codebases where the class is already instantiated in many places, this requires touching every instantiation. Lean on the Compiler to find them.

**Case study:** `OffMarketTradeValidator` calling `AfxMessageBox`, `SubmitDialog`, `g_dispatcher` in `showMessage()`. After Push Down Dependency: `showMessage()` is pure virtual in base; `WindowsOffMarketTradeValidator` has real MFC code; `TestingOffMarketTradeValidator` has empty `showMessage()`. (cs-012)

---

## 19. Replace Function with Function Pointer

**Purpose:** Make C functions replaceable at runtime by declaring function pointer variables with the same names, initializing them to the real functions, and allowing tests to reassign them to fakes.

**When to use:** C/procedural codebases where OO techniques (virtual dispatch, subclassing) are not available. More granular than Link Substitution — replaces individual functions rather than whole translation units.

**Steps:**
1. Find the declarations of the functions you want to replace in the header file.
2. Before each function declaration, declare a function pointer variable of the same type but with the same name (e.g., `void (*openConnection)(const char*) = openConnection;`).
3. Rename the original function declarations to avoid name conflicts (e.g., `openConnectionReal`).
4. In a `.c` file, initialize each function pointer to the address of the renamed real function.
5. Run a build — compilation errors from unresolved references to the old function names guide you to the function bodies that need renaming.

**Language applicability:** C. Also applicable in C++ but object seam techniques are preferred.

**Cross-references:** Link Substitution (coarser granularity — whole-file replacement at link time); Definition Completion (header-level stub for type definitions); Introduce Instance Delegator (OO equivalent for static method calls).

**Trade-offs:** Function pointer indirection adds slight runtime overhead. In test builds only, this is acceptable. Function pointer initialization requires careful setup in test teardown to restore originals. Complex in multi-threaded code.

---

## 20. Replace Global Reference with Getter

**Purpose:** Break a global variable dependency in a specific method by introducing a protected getter that can be overridden in a test subclass, enabling the test to provide an alternative value.

**When to use:** When one method accesses a global variable and Subclass and Override Method is already in play (or the class can easily be subclassed for testing). For multiple methods accessing the same global, use Encapsulate Global References instead.

**Steps:**
1. Identify the global reference you want to replace.
2. Write a protected getter method that returns the global's value (e.g., `protected Connection getConnection() { return g_connection; }`). Visibility must be at least `protected` to allow override in a subclass.
3. Replace all references to the global in the target method with calls to the getter.
4. Create a testing subclass that overrides the getter to return a fake value.

**Language applicability:** All OO languages.

**Cross-references:** Encapsulate Global References (use when the same global appears in many methods); Introduce Static Setter (use when a per-subclass override is insufficient and the global needs to be fully replaced as a singleton-level object).

**Trade-offs:** Introduces a getter whose only purpose is testability. Name it clearly. The pattern creates a testable object seam from a global-state seam.

---

## 21. Subclass and Override Method

**Purpose:** The foundational OO dependency-breaking technique. Make overridable methods virtual; create a test subclass that overrides them to neutralize dependencies or sense values. All Extract and Override variants (Call, Factory Method, Getter) are specializations of this technique.

**When to use:** When a class has a few methods that call out to problematic dependencies, those methods can be made overridable, and the problematic behavior can be nullified or replaced by a test subclass. Use Subclass and Override when the problem is localized; use Push Down Dependency when dependencies are pervasive.

**Steps:**
1. Identify the dependencies to separate. Find the smallest set of methods that, if overridden, would eliminate all problematic calls. Aim for one or two methods.
2. Make each method overridable:
   - C++: add `virtual` keyword
   - Java: remove `final` if present (default is non-final)
   - C#: add `virtual` or ensure `override` is in scope
3. Adjust visibility so a subclass can override: Java/C# methods must be at least `protected`. In C++, `virtual` methods can be `protected` or `public`.
4. Create a test subclass (typically in the test file). Override the identified methods. Verify that the subclass can be built in the test harness.

**Language visibility quick-ref:**

| Language | Make overridable | Min visibility for override |
|----------|-----------------|---------------------------|
| C++ | `virtual` | `protected` (convention) |
| Java | remove `final` | `protected` |
| C# | `virtual` | `protected` |
| Python | nothing | nothing (all overridable) |
| Ruby | nothing | nothing (all overridable) |

**Cross-references:** Extract and Override Call (extract a call first, then override — use when the overridable surface is not natural); Extract and Override Factory Method (for constructor-time dependencies in Java/C#); Extract and Override Getter (for constructor-time dependencies in C++); Push Down Dependency (when many methods need to be overridden — make the class abstract instead).

**Trade-offs:** Test subclasses that override too much stop testing the real class. Override as little as possible. The technique creates an object seam at each override point — explicit and maintainable.

---

## 22. Supersede Instance Variable

**Purpose:** Replace an object created in a constructor (after construction is complete) by adding a setter method that safely destroys the old instance and sets a new one. Primarily for C++ where virtual dispatch is unavailable in constructors.

**When to use:** C++ primarily. When Extract and Override Factory Method and Extract and Override Getter are not viable, and you need to substitute an instance variable created in the constructor. Use as a last resort — the technique requires test code to call the setter explicitly after construction.

**Steps:**
1. Identify the instance variable you want to supersede.
2. Create a method named `supersedeXxx` (where `Xxx` is the variable name, e.g., `supersedeConnection`). The method accepts a pointer or reference to the new object.
3. In the method body: check for other references to the old object inside the class (to avoid dangling pointers); release or delete the existing instance; assign the new value.

**Language applicability:** Primarily C++. Can also be used in Java/C# but other techniques are usually simpler there.

**Cross-references:** Extract and Override Factory Method (preferred Java/C# alternative); Extract and Override Getter (preferred C++ alternative using lazy initialization); Parameterize Constructor (preferred when construction can be restructured).

**Trade-offs:** Leaves construction in an intermediate state (real object created in constructor, replaced in test setup). The supersede method is purely a testing artifact. Memory ownership semantics in C++ must be carefully managed to avoid double-free or memory leaks.

---

## 23. Template Redefinition

**Purpose:** Exploit C++ template instantiation to substitute a dependency by providing a different type argument in test builds. The dependency is part of a class template, and tests instantiate the template with a fake type.

**When to use:** C++ codebases with class templates where the dependent type is a template parameter. The production code instantiates the template with the real type; test code instantiates it with a fake type.

**Steps:**
1. Identify the class template and the template parameter that corresponds to the dependency.
2. In the test file, define a fake class that satisfies the template's requirements (duck typing via template specialization — no need for inheritance or a common interface).
3. Instantiate the template with the fake type in the test.

**Language applicability:** C++ (templates). Java generics are erased at compile time and do not support this pattern. Some limited applicability in Rust (trait-based generics).

**Cross-references:** Extract Interface (OO alternative for non-template codebases); Link Substitution (build-level alternative when template redefinition is not practical).

**Trade-offs:** C++ templates can produce long compile-time errors when the fake type does not satisfy all template requirements. The technique is clean when it applies but requires C++ template expertise to apply safely.

---

## 24. Text Redefinition

**Purpose:** In interpreted (dynamic) languages, redefine a method, function, or class at the language level in test code to substitute behavior without any structural changes to production code.

**When to use:** Ruby, Python, JavaScript, Perl, and other interpreted languages where methods can be opened and redefined at runtime. The most powerful technique for dynamic languages — essentially free, with no structural changes required.

**Steps:**
1. In the test file, reopen the class (Ruby: `class Foo; def bar; ... end; end`) or reassign the method (Python: `Foo.bar = lambda self: fake_result`) to replace the production implementation.
2. Write the test using the redefined method.
3. Restore the original method after the test (or use a test framework's stubbing mechanism, e.g., RSpec `allow`, Python `unittest.mock.patch`).

**Language applicability:** Interpreted/dynamic languages only: Ruby, Python, JavaScript (Node.js), Perl, Smalltalk. Not applicable in compiled statically-typed languages (Java, C++, C#).

**Cross-references:** Link Substitution (compiled-language equivalent); Subclass and Override Method (the OO alternative in any language that is less intrusive because it does not modify the class globally).

**Trade-offs:** Extremely powerful but can produce confusing test failures if redefinitions are not properly cleaned up between tests. Use test framework stubbing facilities (mock/patch) rather than manual redefinition whenever available. Text Redefinition bypasses the type system — do not use it to "fix" tests that should be prompting structural changes.

---

*End of technique catalog. For technique selection by dependency type, language, and constraint, see `references/selection-table.md`.*
