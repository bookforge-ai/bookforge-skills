# Symptom Routing Table

Full 19-symptom reference for `legacy-code-symptom-router`.

Each row maps a Part II chapter to a plain-language symptom, the root cause, and the downstream skill(s) to invoke.

---

## Symptom 1 — Ch 6: "I Don't Have Much Time and I Have to Change It"

**Plain-language triggers:** "I have a deadline", "I need to change this fast, no time for tests", "quick fix needed", "production is down", "ship by tomorrow".

**Root cause:** Time pressure. Cannot take on full dependency-breaking and test-writing cycle for the feature.

**Primary route:** `legacy-code-addition-techniques` (Sprout Method, Sprout Class, Wrap Method, Wrap Class)

**Technique preview:** Rather than modifying the existing untestable method, you write new behavior in a separate, testable method (Sprout Method) and call it from the old method. This leaves the old code completely untouched. If the class itself can't be instantiated in a test harness, you create a new Sprout Class instead. Wrap Method and Wrap Class are used when the new behavior must execute around the existing method (temporal coupling).

**Fallback:** If the change is so small that even sprouting is overkill (one-line fix), apply safe-legacy-editing-discipline's Preserve Signatures discipline and document the risk.

---

## Symptom 2 — Ch 7: "It Takes Forever to Make a Change"

**Plain-language triggers:** "Builds take 5 minutes", "I change one file and have to recompile everything", "I can't tell what to change", "takes forever to understand what this does", "feedback loop is too slow", "our builds are awful".

**Root cause:** Two distinct root causes with different routes:
- **Understanding lag** — you don't know WHERE to make the change (comprehension problem)
- **Build lag** — you know WHAT to change but compilation and test cycles are slow (architecture problem)

**Route A (understanding lag):** `scratch-refactoring-for-code-understanding` → understand structure; then `legacy-code-change-algorithm` to proceed

**Route B (build lag):** `dependency-breaking-technique-executor` → break inter-module dependencies to allow fast isolated test compilation (<10 seconds target)

**Key diagnostic question:** "Are you spending time figuring out what to change, or are you waiting for the build after you've already changed it?"

**Note (from df-014):** These two causes are often conflated. Solve them in sequence — comprehension first, then build speed. Trying to speed up builds before you understand the structure is premature optimization.

---

## Symptom 3 — Ch 8: "How Do I Add a Feature?"

**Plain-language triggers:** "I need to add a new feature to this class", "I need to add behavior", "how do I extend this safely", "I want to add a method to this class".

**Root cause:** The code IS (or can be placed) under test, and the developer needs a feature-addition discipline.

**Primary route:** `tdd-and-programming-by-difference`

**Technique preview:** Two approaches. TDD (red-green-refactor) is the default for any language: write a failing test for the new behavior, make it pass with minimal code, refactor. Programming by Difference (OO languages only) uses inheritance: write the feature as a subclass with tests, then normalize the design by pushing behavior up or down as appropriate.

**Prerequisite check:** If the class is NOT yet under test, route to Symptom 4 (can't get class in test harness) first, then return here.

---

## Symptom 4 — Ch 9: "I Can't Get This Class into a Test Harness"

**Plain-language triggers:** "The class won't compile in my test", "I can't instantiate this class in a test", "the constructor pulls in too many dependencies", "won't build in test", "I get compile errors when I try to test it".

**Root cause:** One of four class-level obstacles: (1) objects of the class can't be created easily, (2) the test harness won't build with the class, (3) the constructor has side effects, (4) significant work happens in the constructor.

**Primary route:** `test-harness-entry-diagnostics`

**Technique preview:** The 7-case triage from Chapter 9: Irritating Parameter → Extract Interface or Pass Null; Hidden Dependency → Parameterize Constructor; Construction Blob → Extract and Override Factory Method; Irritating Global Dependency → Introduce Static Setter; Horrible Include Dependencies (C++) → Definition Completion; Onion Parameter → Extract Interface on outermost layer; Aliased Parameter → Subclass and Override Method.

---

## Symptom 5 — Ch 10: "I Can't Run This Method in a Test Harness"

**Plain-language triggers:** "I can get the class to compile but this specific method won't run in a test", "the method has side effects I can't control", "I can't see the output of this method", "the method's return value is not visible from outside".

**Root cause:** One of four method-level obstacles: the method is not accessible, the parameters are hard to construct, the method has side effects in production, or you need to sense effects inside the method.

**Primary route:** `test-harness-entry-diagnostics` (same skill handles both class-level Ch9 and method-level Ch10 obstacles)

**Technique preview:** For inaccessible methods: Break Out Method Object (extract to a new class where the method is public). For unobservable side effects: introduce a sensing variable or Extract and Override Call to replace the production call with a fake.

---

## Symptom 6 — Ch 11: "I Need to Make a Change. What Methods Should I Test?"

**Plain-language triggers:** "I know what I need to change but I don't know where to write the tests", "what do I need to test around this change", "which tests should I write", "I don't know the blast radius of my change".

**Root cause:** The developer does not yet know the effect radius of their change — which methods will be affected if they change the target.

**Primary route:** `change-effect-analysis`

**Technique preview:** Trace the change's effects outward via three propagation pathways: return values, parameter mutation, and global/static data modification. Draw an effect sketch (hand-drawn dependency diagram). Place tests at the narrowest interception point that exercises all the affected code. This is where you find the test points to write characterization tests at.

---

## Symptom 7 — Ch 12: "I Need to Make Many Changes in One Area"

**Plain-language triggers:** "I have to touch 5 related classes", "this whole subsystem needs changing", "the changes are spread across a cluster of classes", "I don't want to break all these dependencies individually — is there a faster way?".

**Root cause:** The change spans multiple interrelated classes, and the cost of breaking dependencies in each class individually would be prohibitive.

**Primary route:** `change-effect-analysis` (pinch point variant)

**Technique preview:** Find a pinch point — a single method on a higher-level object where the effects of all changes in the cluster converge. Write a pinch point test there first. This gives temporary coverage to safely restructure the classes below. Then replace pinch point tests with narrower per-class unit tests over time. Warning: do not let pinch point tests become permanent integration tests.

---

## Symptom 8 — Ch 13: "I Need to Make a Change, but I Don't Know What Tests to Write"

**Plain-language triggers:** "I don't know what to test here", "I don't know what this code is supposed to do", "I don't understand the existing behavior well enough to write tests", "I'm afraid the code does something I don't expect".

**Root cause:** The developer does not know the intended behavior of the code being changed — the tests cannot be specification-derived.

**Primary route:** `characterization-test-writing`

**Technique preview:** Write characterization tests that document the ACTUAL behavior (not intended behavior). Use the failure-reveal technique: write an assertion you know is wrong, run the test, let the failure message show you the actual output, update the assertion to match. Do not fix bugs you discover while writing characterization tests — document them for later. Build a behavioral safety net first; improve correctness after.

---

## Symptom 9 — Ch 14: "Dependencies on Libraries Are Killing Me"

**Plain-language triggers:** "We're stuck on this version of the library", "the library is hard to test against", "we can't mock this third-party class", "upgrading the library breaks everything", "this library is all over the codebase".

**Root cause:** Production code depends directly on a third-party library's concrete classes instead of on an abstraction, making the library hard to replace, upgrade, or mock.

**Primary route:** `library-seam-wrapper`

**Technique preview:** Introduce a thin interface that your code depends on, then write a production adapter that delegates to the real library. In tests, use a fake adapter. The library becomes swappable behind the interface. Feathers' key warning: the "we'll never change this library" rationalization is exactly the pattern that makes a library painful to change when you eventually need to.

---

## Symptom 10 — Ch 15: "My Application Is All API Calls"

**Plain-language triggers:** "All we do is call external APIs", "there's no testable logic — it's just API wiring", "we're totally dependent on this external service", "the whole app is SDK calls".

**Root cause:** The application's logic is entangled with the API/SDK call surface, making it impossible to test business logic without live external calls.

**Primary route:** `library-seam-wrapper` (same skill handles Ch 14 and Ch 15 — both are library seam problems)

**Technique preview:** Identify the "skin" of your application (the calls that contact the external service) and the "logic" (what you do with responses). Wrap the skin behind an interface so the logic can be tested in isolation with fake responses. The application's logic becomes testable without any external dependency.

---

## Symptom 11 — Ch 16: "I Don't Understand the Code Well Enough to Change It"

**Plain-language triggers:** "I have no idea what this does", "I can't understand this code", "it's too complex to follow", "I need to understand this before I can touch it", "inherited this mess".

**Root cause:** Comprehension failure — the developer cannot form a mental model of the code from reading it.

**Primary route:** `scratch-refactoring-for-code-understanding`

**Technique preview:** Check out the code, refactor it freely without tests to reveal structure — rename variables to what you think they mean, extract methods to group related logic, simplify conditionals. Then DISCARD the changes (do not commit). The refactoring is for comprehension only. You will repeat the same refactorings properly (with tests) after you understand the structure.

**Critical constraint:** Scratch refactoring code is NEVER committed. It is a throwaway cognitive tool, not a production artifact.

---

## Symptom 12 — Ch 17: "My Application Has No Structure"

**Plain-language triggers:** "We have no architecture", "everything depends on everything", "I don't know where anything lives", "our codebase is a ball of mud", "we never designed this — it just grew".

**Root cause:** The application lacks clear architectural structure — the boundaries between components are invisible or nonexistent.

**Primary routes (two-step):**
1. First: `scratch-refactoring-for-code-understanding` to understand what responsibilities exist
2. Then: `big-class-responsibility-extraction` to extract responsibilities from God classes once you understand the structure; `change-effect-analysis` to identify architectural chokepoints

**Note on Ch 17:** This chapter (Naked CRC / Conversation Scrutiny technique) is primarily architectural discovery. The actual extraction work is covered by the downstream skills above.

---

## Symptom 13 — Ch 18: "My Test Code Is in the Way"

**Plain-language triggers:** "My test doubles are cluttering my production files", "test code is mixed with production code", "my production classes have test-only methods in them", "the test seams are polluting the real classes".

**Root cause:** Test infrastructure (test subclasses, seam-enabling constructors, sensing variables) has accumulated in production code and is creating maintenance confusion.

**Primary route:** Reference `unit-test-quality-checker` for assessing whether the test code is structured correctly. Most solutions are organizational: move test-only constructors to test files, consolidate fake classes into a test/ package, enforce the convention that protected-for-testing methods are documented as such.

**Note:** This chapter is organizational guidance rather than a technique. The resolution is usually applying consistent conventions and moving test artifacts to the right place.

---

## Symptom 14 — Ch 19: "My Project Is Not Object Oriented. How Do I Make Safe Changes?"

**Plain-language triggers:** "We're in C, not C++", "we don't have classes", "procedural codebase", "no OO in this language", "this is a C codebase and I can't do OO seams".

**Root cause:** The OO seam techniques (the primary dependency-breaking strategies) do not apply to procedural or non-OO languages.

**Primary route:** `dependency-breaking-technique-executor` (specifically the Link Seam, Replace Function with Function Pointer, and Definition Completion techniques for non-OO languages)

**Technique preview:** In C/procedural code: Link Seams allow replacing a function's implementation by linking a different object file; Replace Function with Function Pointer makes a function's implementation substitutable at runtime; Definition Completion allows providing a test-only implementation of a header in the test build. These are the non-OO equivalents of object seams.

**Pre-read:** `seam-type-selector` explains the seam type taxonomy (Object, Link, Preprocessor) — read first to understand which seam type applies to your language.

---

## Symptom 15 — Ch 20: "This Class Is Too Big and I Don't Want It to Get Any Bigger"

**Plain-language triggers:** "This class has 80 methods", "this class does everything", "this class has thousands of lines", "God class", "fat class", "I can't understand this class because it's too big".

**Root cause:** A class has accumulated too many responsibilities, violating the Single Responsibility Principle. It is too large to understand, test, or change safely.

**Primary route:** `big-class-responsibility-extraction`

**Technique preview:** Apply 7 heuristics to find hidden responsibilities: group methods by name clusters, look for private methods that signal a hidden class, identify decisions that can change, draw feature sketches to find variable/method clusters, apply the single-sentence description test (multiple clauses = multiple responsibilities). Then extract incrementally — do not binge-refactor; extract a responsibility only when you are already changing it.

---

## Symptom 16 — Ch 21: "I'm Changing the Same Code All Over the Place"

**Plain-language triggers:** "Every time I change this, I have to change 10 other places", "copy-paste everywhere", "duplicated logic in multiple classes", "shotgun surgery", "I keep making the same change over and over".

**Root cause:** The same logic is duplicated across multiple methods or classes, causing changes to require parallel edits.

**Primary route:** `duplication-removal-via-extraction`

**Technique preview:** Start with the smallest shared utility (a single duplicated calculation or validation). Extract it to a shared method. Let the larger structure emerge — a superclass (Template Method pattern) may appear naturally once you've removed small duplications. Do not design the inheritance hierarchy up-front; let duplication removal drive the structure.

**Prerequisites:** Write characterization tests first. Do not remove duplication in code without tests — you need the safety net.

---

## Symptom 17 — Ch 22: "I Need to Change a Monster Method and I Can't Write Tests for It"

**Plain-language triggers:** "This method is 500 lines", "I can't understand this method", "this method does everything", "I can't write tests for this method because it's too complex", "monster method".

**Root cause:** A single method that is too long and complex to understand or test. Often the symptom of years of incremental addition without extraction.

**Primary route:** `monster-method-decomposition`

**Technique preview:** Classify the monster first: Bulleted (sequential chunks, low indentation) → Find Sequences strategy (extract condition + body together to reveal the overarching sequence). Snarled (deep nesting, one dominant block) → Skeletonize strategy (extract condition and body separately, leaving the control structure visible). Always extract to the same class first, use automated refactoring tools only, extract small pieces before large.

---

## Symptom 18 — Ch 23: "How Do I Know That I'm Not Breaking Anything?"

**Plain-language triggers:** "I'm afraid I'll break something", "I don't know if my change is safe", "how can I be sure I'm not introducing a regression", "I don't have tests and I need to make this change now", "I'm making changes without a safety net".

**Root cause:** No tests exist and the developer must make changes without them — a pure safety-discipline problem.

**Primary routes (both apply):**
1. `safe-legacy-editing-discipline` — the 4 behavioral constraints for editing without tests (Hyperaware Editing, Single-Goal Editing, Preserve Signatures, Lean on the Compiler)
2. `characterization-test-writing` — if there is any time to write even a few tests before changing

**Note:** This symptom is the most dangerous state in the algorithm. If there is ANY time to write even one test before changing, do so. If not, apply the editing disciplines mechanically and document all changes for review.

---

## Symptom 19 — Ch 24: "We Feel Overwhelmed. It Isn't Going to Get Any Better"

**Plain-language triggers:** "I don't know where to start", "the codebase is hopeless", "we're never going to fix this", "there's too much legacy code to tackle", "overwhelmed", "demoralized", "we've given up on making this better".

**Root cause:** Motivational and strategic failure, not a technical one. The developer or team cannot see a tractable path through the legacy code problem.

**Primary route:** This is a motivational chapter, not a technique chapter. The resolution is restoring perspective and establishing a starting ritual.

**Entry point:** `legacy-code-change-algorithm` — the 5-step algorithm is the answer to overwhelm. Every legacy code change starts there. Pick ONE change, apply the algorithm, finish it. Build confidence incrementally.

**Feathers' key insight:** "When you come to understand legacy code, you begin to see it differently. It doesn't have to be a mess. You can make changes one step at a time." The algorithm's value is that it makes the next step always clear: identify the change, find a test point, break a dependency, write a test, make the change. Any codebase can be improved one change at a time.

**Reframe:** Overwhelm = team does not have a reliable procedure. Installing `legacy-code-change-algorithm` as a team habit resolves the source of overwhelm.

---

## Quick Symptom Classification Matrix

| Category | Symptoms | Key Question |
|---|---|---|
| **Time pressure** | 1 (Ch 6) | "Do I have time for a full dependency-breaking cycle?" |
| **Build/feedback speed** | 2 (Ch 7) | "Is the delay comprehension or compilation?" |
| **Feature addition** | 3 (Ch 8) | "Is the code currently testable?" |
| **Testability — class** | 4 (Ch 9) | "What error do I get when trying to instantiate in test?" |
| **Testability — method** | 5 (Ch 10) | "Can the class compile but the method won't run?" |
| **Test placement** | 6 (Ch 11), 7 (Ch 12) | "Single change point or a cluster?" |
| **Unknown behavior** | 8 (Ch 13) | "Do I know what the code should do?" |
| **Library/API coupling** | 9 (Ch 14), 10 (Ch 15) | "Direct library calls or all-API logic?" |
| **Comprehension** | 11 (Ch 16), 12 (Ch 17) | "Can't understand one class or the whole system?" |
| **Test organization** | 13 (Ch 18) | "Is the test code polluting production?" |
| **Non-OO language** | 14 (Ch 19) | "Can I use OO seams?" |
| **Design problems** | 15 (Ch 20), 16 (Ch 21), 17 (Ch 22) | "Class too big? Duplication? Monster method?" |
| **Safety without tests** | 18 (Ch 23) | "Can I write any tests before changing?" |
| **Morale / strategy** | 19 (Ch 24) | "Does the team have a reliable starting procedure?" |
