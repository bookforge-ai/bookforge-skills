# Command Pattern — Implementation Guide

Deep implementation details for the `command-pattern-implementor` skill.

---

## SimpleCommand Template

For commands that are (1) not undoable and (2) take no extra arguments, a generic/template class can eliminate the need to define a ConcreteCommand subclass for every operation.

**SimpleCommand** is parameterized by the receiver type and stores a pointer-to-member-function (the action). Execute simply calls the stored action on the stored receiver.

**C++ template form (source: GoF p. 225–226):**

```cpp
template <class Receiver>
class SimpleCommand : public Command {
public:
    typedef void (Receiver::* Action)();

    SimpleCommand(Receiver* r, Action a)
        : _receiver(r), _action(a) {}

    virtual void Execute() {
        (_receiver->*_action)();
    }

private:
    Action    _action;
    Receiver* _receiver;
};
```

**Usage:**

```cpp
MyClass* receiver = new MyClass;
Command* aCommand = new SimpleCommand<MyClass>(receiver, &MyClass::Action);
aCommand->Execute();  // calls receiver->Action()
```

**In modern languages:**

In Python, JavaScript, or Java, a lambda or method reference serves the same purpose:

```python
# Python — closure replaces SimpleCommand
def make_command(receiver, action_name):
    def execute():
        getattr(receiver, action_name)()
    return execute

paste_cmd = make_command(document, "paste")
paste_cmd()
```

**Limitations of SimpleCommand / closures:**

- No Unexecute — use only when undo is not required
- No argument storage — use only when the operation takes no extra parameters
- No per-invocation state capture — if the operation depends on runtime state (e.g., current selection), a full ConcreteCommand subclass is required

As soon as any of these three conditions changes, upgrade to a full ConcreteCommand class.

---

## How Intelligent Should a Command Be?

GoF names this a design spectrum:

**Thin command (pure binding):**
The command stores only the receiver reference and delegates everything.

```
class PasteCommand:
    Execute(): this._document.Paste()
```

Use when: a suitable receiver class already exists and has the method you need.

**Fat command (self-contained):**
The command implements the operation entirely without delegating to a receiver at all.

```
class OpenCommand:
    Execute():
        name = AskUser()
        if name:
            doc = new Document(name)
            this._application.Add(doc)
            doc.Open()
```

Use when: no suitable receiver exists, or the command must coordinate across multiple objects (like OpenCommand, which creates a Document, adds it to Application, and opens it — three operations on two objects, with no single "receiver" that knows how to do all three).

**Middle ground:**
The command has enough knowledge to find its receiver dynamically (e.g., asks a registry or uses a service locator inside Execute).

Use when: the receiver is not known at construction time and cannot be passed in.

**Rule of thumb:** Start with thin commands (better testability, clearer separation). Move toward fat commands only when no clean receiver abstraction exists.

---

## State Management in Undoable Commands

### What to capture

Three categories of state may need to be saved for Unexecute:

1. **The receiver object** — which object was affected (reference, not a copy)
2. **The arguments** — what was passed to the receiver (e.g., the new font, the new value)
3. **The original values** — the prior state of the receiver that will be overwritten

For most commands, (3) is the critical one. It must be captured *before* Execute modifies the receiver.

```
class MoveCommand:
    constructor(shape, newX, newY):
        this._shape = shape
        this._newX = newX
        this._newY = newY
        this._oldX = null   # captured at Execute time, not here
        this._oldY = null

    Execute():
        this._oldX = this._shape.X   # save before changing
        this._oldY = this._shape.Y
        this._shape.MoveTo(this._newX, this._newY)

    Unexecute():
        this._shape.MoveTo(this._oldX, this._oldY)
```

### When to copy before placing on history

A command must be *copied* before being placed on the history list when:

- The same ConcreteCommand object is reused across multiple Execute calls
- The command's undo state (captured originals) will be overwritten on the next Execute

**Example:** A single `DeleteCommand` object is wired to the Delete key. Each time the user presses Delete, the same object's Execute runs — overwriting `_deletedObjects` with the new selection. Without copying, the history list holds references to the same object, and all entries point to the most recent invocation's state.

```
# Invoker that copies before tracking
ExecuteCommand(cmd):
    cmd.Execute()
    history.append(cmd.Copy())   # copy captures current undo state
```

If the command's state never varies across invocations (stateless commands), copying is unnecessary — a reference is sufficient.

Commands that must be copied before history placement act as Prototypes (GoF Prototype pattern, p. 117).

---

## MacroCommand: Subcommand Ownership and Lifecycle

### Ownership

MacroCommand owns its subcommands. When the MacroCommand is deleted, it is responsible for deleting its subcommands. This prevents memory leaks in languages without garbage collection:

```cpp
MacroCommand::~MacroCommand() {
    // delete all subcommands
    ListIterator<Command*> i(_cmds);
    for (i.First(); !i.IsDone(); i.Next()) {
        delete i.CurrentItem();
    }
}
```

### Add/Remove at runtime

MacroCommand exposes Add and Remove to allow dynamic macro construction (e.g., macro recording while the user performs actions):

```
macro = new MacroCommand()
// user performs a sequence:
macro.Add(new PasteCommand(doc))
macro.Add(new FontCommand(doc, bold, selection))
// then save the macro for replay
```

### Nested MacroCommands

A MacroCommand can contain other MacroCommands as subcommands. The Execute and Unexecute implementations recurse naturally — each subcommand handles its own children.

---

## History List: Bounding and Persistence

### Bounding history length

For applications where memory or storage is constrained, cap the history list at N commands. When the cap is reached and a new command is pushed:

1. Remove the oldest command from the front of the list
2. Append the new command to the back
3. Adjust the present pointer accordingly

This is a FIFO eviction: you lose the ability to undo the oldest N operations, but the most recent N remain available.

### Persistent history (crash recovery)

Augment Command with Store and Load operations:

```
abstract class Command:
    abstract Execute()
    abstract Unexecute()
    abstract Store(stream: OutputStream)     # serialize command to log
    abstract Load(stream: InputStream)       # deserialize command from log
```

On each Execute, call `cmd.Store(log)` to append the command to a persistent log file. On application startup after a crash, read the log and call `cmd.Execute()` for each logged command to replay the session.

Commands must be serializable — they need to be reconstructed from the log without the original objects in memory. This typically means storing the receiver's identifier (e.g., object ID) rather than a pointer, and resolving the object from a registry during Load.

---

## Error Accumulation in Undo/Redo

GoF names this "hysteresis" — the accumulation of small errors across repeated execute/unexecute/execute cycles.

**Cause:** Computed reversal may lose precision. Example: a rotation command that rotates 90° clockwise; Unexecute rotates 90° counterclockwise. In floating-point arithmetic, these operations may not perfectly cancel, and the object drifts from its original position after many cycles.

**Mitigation: Memento integration**

When exact fidelity is critical, store a Memento (GoF Memento pattern, p. 283) as part of the command's undo data rather than relying on computed reversal:

```
class TransformCommand:
    Execute():
        this._savedState = this._shape.CreateMemento()   # snapshot before
        this._shape.ApplyTransform(this._transform)

    Unexecute():
        this._shape.RestoreMemento(this._savedState)     # exact restoration
```

The Memento gives the command access to the object's private state for restoration without breaking the object's encapsulation — the Memento is the object's own snapshot, returned to it on restore.

Use Memento-based undo when:
- The operation involves floating-point or lossy computation
- The receiver has complex interdependent state where computing the inverse is error-prone
- Exact round-trip fidelity is required (e.g., pixel-perfect graphics undo)

Use computed reversal (Unexecute) when:
- The operation is discrete and exactly invertible (insert → delete, move by delta → move by -delta)
- Storing full state snapshots is too expensive (large objects or frequent operations)

---

## Decoupling Sender from Receiver: The Core Trade-off

The Command pattern's primary cost is class proliferation. Each unique combination of (receiver type, operation) nominally requires its own ConcreteCommand subclass.

Mitigation strategies:

| Strategy | When to use | Mechanism |
|----------|-------------|-----------|
| SimpleCommand / lambda | Operation has no undo, no extra args | Template or closure parameterized by receiver and method |
| Reuse one ConcreteCommand for multiple receivers | The operation is identical across receiver types | Use an interface for the receiver; one command works with any implementing class |
| Fat command | No suitable receiver abstraction exists | Command implements the logic itself |
| MacroCommand | Multiple operations form a logical unit | Composite — delegates to sub-commands |

The class proliferation cost is the pattern's honest trade-off. It is worthwhile when invoker-receiver decoupling, undo/redo, or operation composability are genuine requirements. If none of these are needed, a direct method call is simpler.

---

## Related Patterns

| Pattern | Relationship |
|---------|-------------|
| **Composite (p. 163)** | MacroCommand is Command + Composite |
| **Memento (p. 283)** | Stores state the command needs to undo its effect |
| **Prototype (p. 117)** | Commands that must be copied before history placement act as Prototypes |
| **Strategy** | Both encapsulate behavior; Command encapsulates a *request* (with a receiver binding and potential undo state); Strategy encapsulates an *algorithm* (swappable computation, no intrinsic undo) |
| **Chain of Responsibility** | Both decouple sender from receiver; Command uses a known binding (receiver set at creation), Chain resolves the receiver at runtime by walking a linked list |
