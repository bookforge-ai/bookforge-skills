# Observer Pattern — Complete Implementation Guide

Source: Design Patterns: Elements of Reusable Object-Oriented Software (GoF), pages 273–282.

---

## The 10 Implementation Concerns

### 1. Mapping Subjects to Their Observers

The simplest approach is for a subject to store references to its observers directly in a `List<Observer*>`. This incurs storage overhead per subject instance regardless of how many observers are registered.

When subjects outnumber observers significantly — for example, many small model objects each observed by one centralized view — the per-instance list wastes memory for the common case of zero or one observer.

**Alternative:** Use an external associative structure (hash table, dictionary) that maps subjects to their observer lists. This trades per-instance storage overhead for a small increase in lookup cost. The hash table approach is global — it centralizes all subject-observer mappings outside the subjects themselves.

```
// Conceptual: external mapping
Map<Subject*, List<Observer*>*> observerMap;

// Attach
observerMap[subject]->Append(observer);

// Notify (subject-side)
observerMap[this]->ForEach(o => o->Update(this));
```

This approach also makes it possible to answer "which subjects does observer O observe?" — the reverse mapping — which the in-subject list approach cannot answer efficiently.

---

### 2. Observing More Than One Subject

An observer may legitimately depend on more than one subject. A spreadsheet cell that aggregates two data streams, or a dashboard panel that shows a composite of price and volume data, is observing multiple subjects.

The basic `Update()` signature does not tell the observer which subject triggered the notification. The observer must be able to discriminate.

**Solution:** Pass the subject itself as a parameter to `Update`. The observer compares the received pointer against its stored subject references:

```cpp
void CompositeObserver::Update(Subject* theChangedSubject) {
    if (theChangedSubject == _priceSubject) {
        // handle price change
    } else if (theChangedSubject == _volumeSubject) {
        // handle volume change
    }
}
```

This is why the GoF base Observer interface uses `Update(Subject*)` rather than a parameterless `Update()`.

---

### 3. Who Triggers the Update

There are exactly two options, and each has a failure mode.

**Option A — Subject triggers automatically (SetState calls Notify)**

```cpp
void Subject::SetState(State s) {
    _state = s;
    Notify();
}
```

- Advantage: Clients never forget to trigger. Observers are always in sync.
- Disadvantage: If a client calls `SetA()`, then `SetB()`, then `SetC()`, three separate notification rounds fire for what is logically one composite change. Each intermediate state triggers observer updates, which may be incorrect or wasteful.

**Option B — Client triggers manually**

```cpp
subject->SetA(...);
subject->SetB(...);
subject->SetC(...);
subject->Notify();  // one round for all three changes
```

- Advantage: Batching is explicit. One notification per logical operation.
- Disadvantage: Every code path that mutates state must remember to call `Notify`. Missing one call silently leaves observers stale. This is a correctness hazard.

**Recommendation:** Default to Option A. Move to Option B only when profiling reveals notification overhead is a measurable cost, or when a use case genuinely requires atomic multi-step state changes (e.g., a transaction commit that sets multiple fields before broadcasting).

---

### 4. Dangling References to Deleted Subjects

When a subject is deleted, observers may still hold pointers to it. On the next notification cycle — or when any observer attempts to call `GetState` — the program accesses freed memory. The crash appears after the deletion, not at it, making the bug hard to locate.

**Wrong approach:** Deleting the observers when the subject is deleted. Observers may be registered with multiple subjects, or referenced by other objects. Deleting them unilaterally is incorrect.

**Correct approach:** The subject notifies its observers of its own deletion so each observer can nullify its stored reference:

```cpp
Subject::~Subject() {
    ListIterator<Observer*> i(_observers);
    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->SubjectDeleted(this);
    }
}

void Observer::SubjectDeleted(Subject* s) {
    // Default: no-op. Subclasses override if they store the subject.
}

void ConcreteObserver::SubjectDeleted(Subject* s) {
    if (s == _subject) {
        _subject = nullptr;  // nullify — observer still exists, subject is gone
    }
}
```

Observers must guard `_subject != nullptr` before using it in `Update`.

---

### 5. Making Sure Subject State Is Self-Consistent Before Notification

Observers call `GetState` on the subject inside `Update`. If `Notify` fires while the subject is partially updated, observers will read a mix of old and new state.

This most commonly occurs in inheritance chains where a subclass operation calls an inherited operation that triggers `Notify`, then continues updating subclass-specific state:

```cpp
// VIOLATION — notification fires at BaseClassSubject::Operation,
// before _myInstVar is updated
void MySubject::Operation(int newValue) {
    BaseClassSubject::Operation(newValue);  // Notify fires here via SetState
    _myInstVar += newValue;                 // already too late
}
```

**Fix using Template Method:** Define an abstract primitive for subclasses to override, and put `Notify` at the end of the template method in the base class:

```cpp
// Base class controls notification timing
void Subject::DoOperation(int newValue) {
    SetInternalState(newValue);     // calls subclass override — all state updated
    Notify();                       // fires only when self-consistent
}

// Subclass — overrides the primitive, not the template method
void MySubject::SetInternalState(int newValue) {
    BaseClassSubject::SetInternalState(newValue);
    _myInstVar += newValue;         // subclass state updated before Notify
}
```

**Rule:** Always document which Subject operations trigger notifications. This is part of the public contract.

---

### 6. Avoiding Observer-Specific Update Protocols — Push and Pull Models

The subject can pass more or less information to observers during notification. The two extremes are:

**Push model:** Subject sends detailed change information as arguments to `Update`.

```cpp
// Subject pushes what it assumes observers need
void Subject::Notify(int changedValue, int oldValue) {
    for each o: o->Update(this, changedValue, oldValue);
}
```

- Advantage: Observer does not need to query the subject — efficient when all observers need the same data.
- Disadvantage: The subject must assume it knows what observers need. If different observers need different data, the push parameters become a lowest-common-denominator compromise. Subjects become less reusable because they're coupled to observer data needs.

**Pull model:** Subject sends only its identity. Observers query what they need.

```cpp
// Subject sends only itself
void Subject::Notify() {
    for each o: o->Update(this);
}

// Observer pulls what it needs
void ConcreteObserver::Update(Subject* s) {
    _cachedValue = ((ConcreteSubject*)s)->GetRelevantState();
    Render();
}
```

- Advantage: Subject remains ignorant of observer needs. Maximum reusability.
- Disadvantage: Observer must know the concrete Subject type to call specific accessors (introduces a cast). Less efficient if determining what changed requires re-reading large state.

**Recommendation:** Pull is the default. It enforces the subject's ignorance of its observers. Add push parameters only when a specific piece of changed data is needed by all observers and the cost of polling for it would be significant.

---

### 7. Specifying Modifications of Interest Explicitly (Aspect-Based Registration)

In the basic pattern, every observer is notified of every change. This is wasteful when a subject produces multiple types of events and a given observer cares about only one.

**Aspect-based registration** lets observers declare which events they care about at subscription time:

```cpp
// Extended Attach — observer registers for a specific aspect
void Subject::Attach(Observer* o, Aspect& interest);

// Extended Update — aspect passed at notification time
void Observer::Update(Subject* s, Aspect& interest);
```

At notification time, the subject supplies the changed aspect and notifies only the observers registered for that aspect:

```cpp
void Subject::Notify(Aspect& changedAspect) {
    for each (observer, registeredAspect) in _observerMap:
        if registeredAspect == changedAspect:
            observer->Update(this, changedAspect);
}
```

This is particularly useful for document-based systems where a single document may produce text changes, layout changes, selection changes, and save-state changes — and different views care about different subsets.

---

### 8 and 9. Encapsulating Complex Update Semantics — the ChangeManager

When the dependency relationships between subjects and observers are complex, the standard direct-Notify approach breaks down in two ways:

1. **Redundant notifications:** An operation changes subjects A and B. Observer O observes both. When A notifies, O runs. When B notifies, O runs again. O has been updated twice for one logical change.

2. **Ordering problems:** If notification order matters (observer C must run before observer D because D reads data that C computes), the simple notification loop cannot express this.

**ChangeManager** addresses both. It is a compound of three patterns:
- **Observer:** subjects and observers still use the standard protocol
- **Mediator:** ChangeManager centralizes the subject-observer communication logic
- **Singleton:** exactly one ChangeManager exists per subsystem; all subjects and observers route through the same instance

**ChangeManager's three responsibilities:**
1. Maintains the subject-to-observer mapping — eliminates per-subject observer storage
2. Defines the update strategy — when and how observers are notified
3. Updates all dependent observers at the request of any subject

**Class structure:**

```
Subject ←────────────── ChangeManager ───────────────→ Observer
Attach(Observer o)       Register(Subject, Observer)     Update(Subject)
Detach(Observer)         Unregister(Subject, Observer)
Notify() ─────────→      Notify()
chman->Notify()               │
                          ┌───┴────────┐
                SimpleChangeManager  DAGChangeManager
```

**SimpleChangeManager:**

```
Notify():
  for each subject s in subjects:
    for each observer o of s:
      o->Update(s)
```

Naive — always notifies all observers. Correct when observers observe exactly one subject.

**DAGChangeManager:**

```
Notify():
  Pass 1 — mark:
    for each subject s in subjects:
      for each observer o of s:
        mark o as pending

  Pass 2 — update once each:
    for each marked observer o:
      o->Update(relevantSubject)
      unmark o
```

Handles directed acyclic graph dependencies. When an observer observes multiple subjects, it receives exactly one `Update` call regardless of how many subjects changed. `DAGChangeManager` is preferable to `SimpleChangeManager` when any observer observes more than one subject.

**Using ChangeManager:**

```cpp
// Subject delegates to ChangeManager instead of maintaining its own list
void Subject::Attach(Observer* o) {
    ChangeManager::Instance()->Register(this, o);
}

void Subject::Notify() {
    ChangeManager::Instance()->Notify();
}
```

The Singleton `ChangeManager::Instance()` can be initialized with either strategy at startup, making it possible to change the update strategy without touching Subject or Observer classes.

---

### 10. Combining the Subject and Observer Roles

Languages without multiple inheritance (originally Smalltalk) sometimes define Subject and Observer together in a single root class, making all objects potential subjects and observers without any additional inheritance.

In languages with multiple inheritance (C++), a class can inherit from both `Subject` and `Observer` simultaneously, producing an object that can both publish changes and react to changes from other subjects:

```cpp
class DigitalClock : public Widget, public Observer {
    // Widget provides UI rendering capability
    // Observer provides Update() — reacts to ClockTimer changes
    // DigitalClock itself is not a Subject, but could be if it had dependents
};
```

This also applies to systems where an observer itself is a subject for downstream observers — common in reactive pipelines. In that case, the observer's `Update` method mutates its own state and then calls its own `Notify`, propagating the change downstream.

**Warning:** When an object is both subject and observer and part of a cycle, cascade updates are possible. Use `DAGChangeManager` to prevent redundant updates, or add a change-guard to prevent re-notification while an update is in progress:

```cpp
void ComboSubjectObserver::Update(Subject* s) {
    if (_updating) return;   // prevent re-entrant notification
    _updating = true;
    // update own state based on s
    Notify();                // propagate to own observers
    _updating = false;
}
```

---

## Participants Summary

| Participant | Role | Knows about |
|-------------|------|-------------|
| `Subject` | Maintains observer list; provides Attach/Detach/Notify | Abstract `Observer` only |
| `Observer` | Defines Update interface | Nothing about Subject state |
| `ConcreteSubject` | Stores subject state; calls Notify on change | Its own state and the abstract Observer |
| `ConcreteObserver` | Implements Update; holds reference to ConcreteSubject | ConcreteSubject (for GetState queries) |
| `ChangeManager` | Mediates subject-observer mapping; controls update strategy | Both Subject and Observer interfaces |

---

## Collaborations Sequence

```
aConcreteSubject     aConcreteObserver     anotherConcreteObserver
      │                     │                         │
      │← SetState() ────────│                         │
      │                     │                         │
      │── Notify() ─────────→                         │
      │                     │                         │
      │    ← Update() ──────│                         │
      │    ── GetState() ───→                         │
      │                     │                         │
      │── Update() ─────────────────────────────────→ │
      │                              ← GetState() ────│
      │                                               │
```

Note: the observer that initiates the change (`SetState`) postpones its own update until it receives notification from the subject. `Notify` is not always called by the subject — it can be called by an observer or by an external client (see Implementation Concern 3).

---

## Consequences

### 1. Abstract Coupling Between Subject and Observer

The subject knows only that it has a list of observers conforming to the abstract `Observer` interface. It does not know the concrete class of any observer. The coupling is minimal and abstract. This allows Subject and Observer to belong to different layers of abstraction in a system — a lower-level subject can communicate with a higher-level observer without violating layering. If tightly coupled, the combined object would be forced to exist in one layer, potentially violating the layering abstraction.

### 2. Support for Broadcast Communication

Unlike an ordinary request with one sender and one receiver, a subject's notification is broadcast to all subscribed observers. The subject does not care how many observers exist. Observers can be added and removed at any time without modifying the subject. It is up to each observer whether to handle or ignore a notification.

### 3. Unexpected Updates

Because observers have no knowledge of each other's presence, they cannot predict the ultimate cost of a change to the subject. A seemingly innocuous state change may cause a cascade of updates through multiple observers and their dependent objects. Furthermore, the simple Update protocol provides no information about *what* changed — only that *something* changed. Observers must work to discover what changed (pull model overhead), or the subject must provide that information (push model coupling). Ill-defined dependency criteria lead to spurious updates that are difficult to track down.

---

## Related Patterns

| Pattern | Relationship |
|---------|-------------|
| **Mediator** | ChangeManager acts as a Mediator between subjects and observers. It encapsulates the update communication so neither subject nor observer needs to know the other's full protocol. |
| **Singleton** | ChangeManager is typically a Singleton — there is one per subsystem, and it must be globally accessible to both subjects and observers. |

---

## Known Uses

- **Smalltalk Model/View/Controller (MVC):** The first and best-known application. Model is Subject; View is Observer. Controller mediates input to model changes. View re-renders on model notification.
- **InterViews:** Defines explicit `Observer` and `Observable` (for Subject) classes.
- **Andrew Toolkit:** Calls subjects "data objects" and observers "views."
- **Unidraw:** Splits graphical editor objects into View (observer) and Subject parts.
- **Qt (signals/slots):** A type-safe, language-integrated implementation of Observer with aspect-based registration (signals map to aspects).
- **Java EventListener model:** Observer implemented as interface; aspect-based (event type per listener interface).
- **RxJS / Reactive Extensions:** Observer generalized to streams — an observable (subject) emits values; subscribers (observers) react to each emission.
