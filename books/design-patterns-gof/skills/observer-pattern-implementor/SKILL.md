---
name: observer-pattern-implementor
description: |
  Implement the Observer pattern to establish one-to-many dependencies where changing one object automatically notifies and updates all dependents. Use when a spreadsheet model needs to update multiple chart views, when UI components must react to data changes, when event systems need publish-subscribe, or when you need to decouple a subject from an unknown number of observers. Handles 10 implementation concerns including push vs pull models, dangling reference prevention, update cascade avoidance, and the ChangeManager compound pattern.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/observer-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - design-pattern-selector
  - behavioral-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [5]
    pages: [273, 282]
tags: [design-patterns, behavioral, gof, observer, publish-subscribe, event-system, mvc, change-manager, mediator, singleton]
execution:
  tier: 2
  mode: full
  inputs:
    - type: code
      description: "Existing code where one object's state changes need to propagate to dependents — tightly coupled notification logic, direct method calls between model and views, or a missing event/callback system"
  tools-required: [TodoWrite, Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Requires a codebase or a sufficiently detailed design description. Code reading tools required to inspect existing structure before refactoring."
---

# Observer Pattern Implementor

## When to Use

A data source is directly calling update methods on its consumers, making it impossible to add or remove consumers without modifying the source. Apply this skill when:

- An abstraction has two separable aspects — a subject (data) and observers (views/reactions) — and tightly coupling them limits reuse of each independently
- A change to one object requires notifying an unknown or variable number of other objects, and you don't want to hard-code who those are
- Objects should be able to notify others without making assumptions about who those objects are — you want zero coupling from subject to observer

Do not apply if:
- Only one consumer will ever exist and that is certain by design (direct call is simpler)
- Observers trigger further changes that trigger more observers — cascade control is complex; use ChangeManager (Step 9)
- The language/framework already provides this mechanism natively (e.g., React state, RxJS, Qt signals) — use those instead

Before starting, verify you can answer: What is the subject (the thing that changes)? What are the observers (the things that react)? What state do observers need from the subject after a change?

---

## Process

### Step 1: Set Up Tracking and Audit Existing Coupling

**ACTION:** Use `TodoWrite` to track progress, then read the codebase to map current subject-observer coupling.

**WHY:** Observer refactoring touches at least three participants (Subject, ConcreteSubject, ConcreteObserver) and requires consistent interface changes across all of them. Without tracking, it is easy to partially refactor — adding the Observer interface while leaving direct calls in the subject — which produces a hybrid that is worse than either approach. The audit reveals whether existing coupling is simple (one direct call) or complex (multiple consumers with different update logic), which determines whether ChangeManager is needed.

```
TodoWrite:
- [ ] Step 1: Audit existing coupling — map subjects and consumers
- [ ] Step 2: Define Subject and Observer interfaces
- [ ] Step 3: Implement ConcreteSubject with Attach/Detach/Notify
- [ ] Step 4: Resolve trigger strategy (who calls Notify)
- [ ] Step 5: Ensure state consistency before Notify
- [ ] Step 6: Choose push vs pull model and implement Update
- [ ] Step 7: Apply aspect-based registration if multiple event types
- [ ] Step 8: Evaluate whether ChangeManager is needed
- [ ] Step 9: Implement ChangeManager if warranted
- [ ] Step 10: Wire up and verify — no dangling references
```

Use `Read` and `Grep` to answer:
- Which class(es) change state and need to broadcast changes? (Subject candidates)
- Which class(es) react to those changes? (Observer candidates)
- How many consumers are there? Are they stable or do they change at runtime?
- Are there multiple types of events, or one general "something changed" notification?

---

### Step 2: Define the Subject and Observer Interfaces

**ACTION:** Create abstract `Subject` and `Observer` base classes (or interfaces). Do not write any concrete logic yet — define only the contracts.

**WHY:** The power of Observer comes from the subject knowing only the abstract `Observer` interface — not any concrete observer type. If you skip this and call concrete methods directly, you recreate the coupling you're trying to eliminate. Defining the interfaces first forces you to commit to the notification contract before any implementation details leak in.

**Subject interface** — three responsibilities:

```cpp
class Subject {
public:
    virtual ~Subject();
    virtual void Attach(Observer*);   // register a new observer
    virtual void Detach(Observer*);   // deregister an observer
    virtual void Notify();            // broadcast change to all observers
protected:
    Subject();
private:
    List<Observer*> _observers;       // or a hash map — see Step 3
};
```

**Observer interface** — one responsibility:

```cpp
class Observer {
public:
    virtual ~Observer();
    virtual void Update(Subject* theChangedSubject) = 0;
protected:
    Observer();
};
```

Note: `Update` receives the subject pointer (not state data). This is the **pull model** default — observers call back on the subject for what they need. See Step 6 for the push vs pull decision.

---

### Step 3: Implement ConcreteSubject and the Observer List

**ACTION:** Implement the concrete subject with state, state accessors (`GetState`/`SetState`), and a working `Notify`. Choose the storage strategy for the observer list.

**WHY:** The naive approach — storing observers directly in every subject instance — works when subjects are few and observers are many per subject. When subjects are many and observers are few (e.g., many small model objects each observed by one dashboard), the per-subject list wastes memory. The hash map trade-off is real: choose based on the ratio of subjects to observers in your system.

**Storage decision:**

| Situation | Storage | Trade-off |
|-----------|---------|-----------|
| Few subjects, many observers each | `List<Observer*>` in Subject | Simple; O(1) attach; O(n) notify |
| Many subjects, few observers each | External hash map (subject → observer list) | Eliminates per-subject overhead; increases access cost |

**Standard Subject implementation:**

```cpp
void Subject::Attach(Observer* o) { _observers->Append(o); }
void Subject::Detach(Observer* o) { _observers->Remove(o); }

void Subject::Notify() {
    ListIterator<Observer*> i(_observers);
    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->Update(this);
    }
}
```

**ConcreteSubject** adds only state and accessors:

```cpp
class ConcreteSubject : public Subject {
public:
    SubjectState GetState() const;
    void SetState(SubjectState s);
private:
    SubjectState _subjectState;
};
```

---

### Step 4: Decide Who Triggers Notify

**ACTION:** Choose and implement one of two trigger strategies: automatic (subject triggers) or manual (client triggers).

**WHY:** This is the most common source of Observer bugs. Automatic triggering ensures observers are never out of sync but fires notifications on every state mutation — including intermediate states in a multi-step update. Manual triggering gives the client control to batch multiple mutations before broadcasting, but adds an obligation: every code path that mutates state must remember to call `Notify`. Forgetting one call produces stale observers that are hard to debug.

**Option A — Automatic trigger (subject calls Notify in SetState):**

```cpp
void ConcreteSubject::SetState(SubjectState s) {
    _subjectState = s;
    Notify();              // automatic — client never calls Notify
}
```

Use when: mutations are typically single-step, or missing a notification is worse than extra notifications.

**Option B — Manual trigger (client calls Notify):**

```cpp
// Client code
subject->SetState(s1);
subject->SetBoundary(b);  // multiple mutations
subject->Notify();         // one notification for both changes
```

Use when: performance matters and multiple state changes should batch into one notification round.

**Recommendation:** Default to Option A. Switch to Option B only if profiling shows notification overhead is significant, or if the use case explicitly requires batching (e.g., multi-step transaction commit).

---

### Step 5: Ensure Subject State Is Self-Consistent Before Notify

**ACTION:** Audit every operation that calls `Notify` (directly or via `SetState`) and verify that all subject state is fully updated before `Notify` fires.

**WHY:** Observers call `GetState` on the subject inside their `Update` method to synchronize. If `Notify` fires while the subject is in a partially-updated state — for example, after a base class operation but before a subclass operation completes — observers will read inconsistent data and enter an inconsistent state of their own. This is a silent bug: observers receive a valid-looking notification but pull stale or partial data.

**Common violation in inheritance:**

```cpp
// WRONG — notification fires before subclass state is updated
void MySubject::Operation(int newValue) {
    BaseClassSubject::Operation(newValue);  // triggers Notify here
    _myInstVar += newValue;                 // too late — observers already ran
}
```

**Fix — use Template Method to control notification timing:**

```cpp
// In abstract Subject — Notify is last
void Text::Cut(TextRange r) {
    ReplaceRange(r);   // redefined in subclasses — all state updated here
    Notify();          // fires only after the complete operation
}
```

Always ensure `Notify` is the **last operation** in any state-mutating method. Document which operations trigger notifications in the class interface comment.

---

### Step 6: Choose and Implement the Push or Pull Model

**ACTION:** Decide whether the subject sends state data to observers (push) or observers query the subject (pull). Implement `Update` accordingly.

**WHY:** This is the core design trade-off for observer usability versus coupling. The pull model makes the subject maximally ignorant of its observers (it sends no assumptions about what they need), but can be inefficient — each observer must figure out what changed on its own. The push model is efficient for observers with narrow needs but makes the subject assume it knows what observers care about, reducing reusability when different observers need different data.

**Pull model** — subject sends only its identity; observers pull what they need:

```cpp
void DigitalClock::Update(Subject* theChangedSubject) {
    if (theChangedSubject == _subject) {  // guard: verify it's the right subject
        int hour = _subject->GetHour();
        int minute = _subject->GetMinute();
        Draw();  // re-render with pulled values
    }
}
```

**Push model** — subject sends relevant state as Update arguments:

```cpp
// Subject
void Subject::Notify(int newValue) {
    for each observer: observer->Update(this, newValue);
}

// Observer
virtual void Update(Subject*, int newValue) = 0;
```

**Decision:**

| Prefer pull when... | Prefer push when... |
|--------------------|---------------------|
| Different observers need different parts of subject state | All observers need the same data |
| Subject does not know what observers care about | The changed data is cheap to pass and expensive to re-query |
| Maximum observer reusability is important | Observer should not need to hold a reference to the subject |

Pull is the default. Push reduces reusability because it encodes assumptions about observer needs into the Subject interface.

---

### Step 7: Apply Aspect-Based Registration for Multiple Event Types

**ACTION:** If the subject produces multiple distinct event types and observers care about only some, extend `Attach` to accept an "aspect" (event category) parameter.

**WHY:** Without aspect filtering, every observer is notified of every change — even changes it does not care about. This wastes cycles and can cause incorrect behavior if an observer's `Update` logic assumes it is only called for its relevant event. Aspect-based registration lets observers declare their interest at subscription time, so `Notify` only calls the relevant observers.

**Extended interfaces:**

```cpp
// Subject registration with aspect
void Subject::Attach(Observer* o, Aspect& interest);

// Observer Update with aspect parameter
void Observer::Update(Subject* s, Aspect& interest);
```

**Notify implementation with aspect filtering:**

```cpp
void Subject::Notify(Aspect& changedAspect) {
    // only notify observers registered for this aspect
    for each (observer, registeredAspect) in _observerMap:
        if registeredAspect == changedAspect:
            observer->Update(this, changedAspect);
}
```

Use when: subjects produce heterogeneous events (e.g., a document that can have text changes, layout changes, and selection changes), and observers specialize in only one type.

---

### Step 8: Evaluate Whether ChangeManager Is Needed

**ACTION:** Assess whether the subject-observer dependency graph is simple or complex. If complex, implement ChangeManager (Step 9). If simple, skip Step 9.

**WHY:** The standard Notify-loop works well when subjects and observers are independent. It breaks down in two scenarios: (1) a single operation modifies multiple interdependent subjects, causing observers to be notified multiple times for what is logically one change; (2) observers themselves observe multiple subjects, creating diamond-shaped dependency graphs where redundant updates proliferate. ChangeManager exists to handle these cases — it absorbs the complexity so subjects and observers don't have to.

**Use ChangeManager if any of the following are true:**

- One high-level operation modifies two or more subjects whose observers overlap
- Any observer observes more than one subject (creating potential for redundant updates)
- Notification order matters and must be controlled globally
- You need a specific update strategy (e.g., "update all after all subjects have changed")

**If none of the above apply:** ChangeManager adds complexity for no benefit. Keep the simple direct Notify loop from Step 3.

---

### Step 9: Implement ChangeManager (Observer + Mediator + Singleton)

**ACTION:** If Step 8 determined ChangeManager is needed, implement it as a mediator that owns the subject-observer mapping, controls update strategy, and exists as a singleton.

**WHY:** ChangeManager combines three patterns with a specific purpose: it acts as a **Mediator** (centralizing the subject-observer communication logic), uses the **Observer** protocol (subjects and observers still implement the same interfaces), and is a **Singleton** (there is exactly one ChangeManager per subsystem — subjects and observers both need to find the same instance). This combination eliminates redundant updates when multiple subjects change in one operation, and allows the update strategy to be changed without touching Subject or Observer classes.

**ChangeManager responsibilities:**
1. Maintains the subject-to-observer mapping (replaces per-subject observer lists)
2. Defines the update strategy — when and in what order observers are notified
3. Updates all dependent observers when a subject requests it

**Two built-in strategies:**

| Strategy | Behavior | Use when |
|----------|----------|----------|
| `SimpleChangeManager` | For each subject, notify all its observers immediately | Observers observe only one subject; no redundant update risk |
| `DAGChangeManager` | Mark all affected observers; update each marked observer exactly once | Observers observe multiple subjects (directed acyclic graph dependencies) |

**ChangeManager interface:**

```cpp
class ChangeManager {
public:
    static ChangeManager* Instance();   // Singleton access
    virtual void Register(Subject*, Observer*);
    virtual void Unregister(Subject*, Observer*);
    virtual void Notify() = 0;          // strategy-defined update dispatch
protected:
    ChangeManager();
private:
    static ChangeManager* _instance;
};
```

**Subject delegates to ChangeManager:**

```cpp
// Subject no longer stores observer list — delegates to ChangeManager
void Subject::Attach(Observer* o) {
    ChangeManager::Instance()->Register(this, o);
}
void Subject::Notify() {
    ChangeManager::Instance()->Notify();
}
```

**DAGChangeManager Notify — prevents redundant updates:**

```cpp
void DAGChangeManager::Notify() {
    // Pass 1: mark all observers that need updating
    for each subject s in _subjects:
        for each observer o of s:
            mark o as pending

    // Pass 2: update each marked observer exactly once
    for each marked observer o:
        o->Update(relevantSubject);
        unmark o;
}
```

---

### Step 10: Wire Up and Prevent Dangling References

**ACTION:** Wire all observers to their subjects via `Attach`. Add lifecycle management to prevent dangling references when subjects are deleted. Verify the full notification chain manually or with a test.

**WHY:** Deleting a subject that observers still hold a reference to produces dangling pointers — observers will attempt to call `GetState` on freed memory. Simply deleting the observers is not a valid solution because they may be observing other subjects or be referenced by other objects. The subject must notify observers of its own deletion so they can nullify their references.

**Deletion protocol in subject destructor:**

```cpp
Subject::~Subject() {
    // Notify observers that this subject is going away
    // so they can reset their stored reference
    ListIterator<Observer*> i(_observers);
    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->SubjectDeleted(this);
    }
}

// Observer handles deletion
void ConcreteObserver::SubjectDeleted(Subject* s) {
    if (s == _subject) {
        _subject = nullptr;  // nullify — do not delete
    }
}
```

**Wiring example:**

```cpp
ClockTimer* timer = new ClockTimer;
DigitalClock* digitalClock = new DigitalClock(timer);  // Attach in constructor
AnalogClock* analogClock = new AnalogClock(timer);     // Attach in constructor
// When timer ticks, both clocks update automatically
```

**Verification checklist:**
- [ ] Attach is called before any state changes that should be observed
- [ ] Detach is called in every observer destructor
- [ ] Deleting a subject does not crash observers
- [ ] Adding a new observer at runtime receives subsequent updates correctly
- [ ] Notifications fire only when subject state is fully consistent (Step 5)

---

## Pitfalls

**1. Cascade updates.** Observer A's `Update` changes subject B, which notifies observer C, which changes subject D... This is the most serious Observer failure mode, and it is difficult to detect because it appears during runtime. Prevention: avoid state changes inside `Update` that would notify other observers. If cascade is unavoidable, use `DAGChangeManager` to ensure each observer updates exactly once per logical change.

**2. Dangling references to deleted subjects.** Deleting a subject without notifying observers leaves them with stale pointers. The crash appears on the next notification cycle, not at the point of deletion, making it hard to locate. Prevention: always implement the deletion-notification protocol in Step 10.

**3. Inconsistent state notification.** Calling `Notify` before all subject state is updated (typically in inherited operations — see Step 5). Observers run during `Update` and pull stale data. Prevention: always use Template Method to put `Notify` last, and audit inheritance chains for calls to `super.Operation()` that trigger notifications mid-update.

**4. Trigger ambiguity.** Mixing automatic and manual trigger strategies across different subjects in the same system. Developers expect one behavior and get the other; observers are sometimes notified twice, sometimes not at all. Prevention: pick one strategy and apply it uniformly across the system. Document it in the Subject class comment.

**5. Push overspecification.** The push model embeds assumptions about what observers need directly into the Subject's `Notify` signature. When observer needs diverge (one needs the full new state, another only needs a delta, a third only needs to know that *something* changed), the push signature becomes a compromise that serves none of them well. Prevention: default to pull. Only add push parameters that are universally needed by all observers, and only after profiling shows that the extra pull calls are a measurable cost.

---

## Examples

### Example 1: Spreadsheet Model with Multiple Chart Views

**Scenario:** A spreadsheet has a data model that three chart widgets (bar chart, pie chart, line chart) read directly. Currently the model calls `barChart.refresh()`, `pieChart.refresh()`, and `lineChart.refresh()` in its `SetCell` method. Adding a fourth chart requires modifying the model.

**Trigger:** "Every new chart type requires touching the spreadsheet model."

**Process:**
- Step 1: Audit reveals `SpreadsheetModel` directly references three concrete chart classes
- Step 2: `SpreadsheetModel` becomes `ConcreteSubject`; each chart implements `Observer`
- Step 3: `List<Observer*>` in Subject (few subjects, multiple observers)
- Step 4: Automatic trigger — `SetCell` calls `Notify()` after updating data
- Step 5: `Notify` is last in `SetCell` — state is fully updated first
- Step 6: Pull model — charts call `GetCellValue(row, col)` in their `Update`
- Step 8: No complex dependencies — skip ChangeManager

**Output:** `SpreadsheetModel` has no reference to any chart class. New charts attach themselves; model never changes.

---

### Example 2: Clock with Multiple Display Observers

**Scenario:** A `ClockTimer` (concrete subject) notifies time displays. A `DigitalClock` and `AnalogClock` both observe the same timer. This is the canonical sample from the GoF text.

**Trigger:** "Both clock displays must always show the same time, but neither should know about the other."

**Key implementation details:**
- `DigitalClock` inherits from both `Widget` (UI toolkit) and `Observer` (combining concern 10 — Subject/Observer in one class hierarchy via multiple inheritance)
- Constructor calls `_subject->Attach(this)`; destructor calls `_subject->Detach(this)` — full lifecycle management
- `Update` guards on subject identity: `if (theChangedSubject == _subject)` — handles potential future case of observing multiple subjects

```cpp
void DigitalClock::Update(Subject* theChangedSubject) {
    if (theChangedSubject == _subject) {
        Draw();
    }
}

void DigitalClock::Draw() {
    int hour   = _subject->GetHour();
    int minute = _subject->GetMinute();
    // render digital display
}
```

**Output:** `ClockTimer::Tick()` calls `Notify()`; both displays update independently without knowing each other exist.

---

### Example 3: Multi-Subject Dashboard with ChangeManager

**Scenario:** A financial dashboard has three data subjects: `PriceSubject`, `VolumeSubject`, and `PositionSubject`. A `RiskSummaryObserver` observes all three. When a trade executes, all three subjects change in one operation. Without ChangeManager, `RiskSummaryObserver.Update` fires three times for one logical event.

**Trigger:** "Our risk view recalculates three times per trade because it observes three subjects."

**Process:**
- Step 8: Observer observes multiple subjects — DAG dependency. ChangeManager required.
- Step 9: Implement `DAGChangeManager`. Each subject calls `ChangeManager::Instance()->Notify()`. DAGChangeManager marks `RiskSummaryObserver` when `PriceSubject` changes, marks it again when `VolumeSubject` changes (already marked — no-op), then updates it once.

**Output:** One trade → three subject changes → `RiskSummaryObserver.Update` called exactly once.

---

## Reference Files

| File | Contents |
|------|----------|
| `references/observer-implementation-guide.md` | All 10 implementation concerns in full detail, ChangeManager class diagrams, push/pull protocol variants, aspect-based registration patterns, and language-specific notes |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-design-pattern-selector`
- `clawhub install bookforge-behavioral-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
