---
name: command-pattern-implementor
description: |
  Implement the Command pattern to encapsulate requests as objects, enabling parameterized operations, queuing, logging, and undo/redo. Use when you need to decouple UI elements from operations, implement multi-level undo with command history, support macro recording, queue or schedule requests, or log operations for crash recovery. Includes the complete undo/redo algorithm using a command history list with present-line pointer, MacroCommand for composite operations, and SimpleCommand template for eliminating subclasses.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/command-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - behavioral-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [2, 5]
    pages: [64-69, 219-228]
tags: [design-patterns, behavioral, gof, command, undo, redo, macro, history, transaction, invoker, receiver]
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "A software project needing to encapsulate operations as objects, with or without undo/redo support"
  tools-required: [TodoWrite, Read, Write]
  tools-optional: [Grep, Bash]
  mcps-required: []
  environment: "A codebase with at least one invoker (button, menu, toolbar) and one or more receivers (domain objects that perform the actual work)"
---

# Command Pattern Implementor

## When to Use

You have a behavioral problem where one or more of these is true:

- UI elements (menu items, toolbar buttons, keyboard shortcuts) need to trigger operations without knowing the receiver or the operation's implementation
- The application requires multi-level undo and redo beyond a single "last action"
- Operations need to be queued, scheduled, logged to disk, or replayed after a crash
- Multiple UI surfaces (menu, button, keyboard shortcut) must trigger the same operation without code duplication
- Operations should be combinable into macro sequences that execute as a unit

Before starting, confirm:
- Can you identify at least one **invoker** (the object that triggers the request — e.g., a menu item, button, toolbar) and one **receiver** (the object that knows how to perform the operation — e.g., a document, model, service)?
- Do operations need to be reversible? If so, can each operation store enough state to reverse itself, or does it need an external snapshot (Memento)?

If unsure whether Command is the right pattern, invoke `behavioral-pattern-selector` first and confirm Command is recommended.

---

## Process

### Step 1: Set Up Tracking and Identify Participants

**ACTION:** Use `TodoWrite` to track progress. Identify the four Command pattern participants in your specific system.

**WHY:** Command's power comes from the clean separation of four roles. Confusing the invoker with the receiver — or putting business logic in the wrong place — undermines the pattern's decoupling benefit. Naming these explicitly before writing any code prevents the most common Command implementation mistakes.

```
TodoWrite:
- [ ] Step 1: Identify Command participants (invoker, receiver, command, client)
- [ ] Step 2: Design the Command interface and protocol
- [ ] Step 3: Implement concrete commands with Execute (and Unexecute if needed)
- [ ] Step 4: Implement the undo/redo history if required
- [ ] Step 5: Implement MacroCommand if composite operations are needed
- [ ] Step 6: Wire invoker to commands in client code
- [ ] Step 7: Verify with-skill vs without-skill scenarios
```

Capture these four participants:

| Role | GoF Name | In your system | Responsibility |
|------|----------|----------------|---------------|
| **Command** | Command | The abstract interface | Declares Execute() — and Unexecute()/Reversible() if undoable |
| **ConcreteCommand** | ConcreteCommand | One class per operation | Binds receiver + action; stores state for undo |
| **Invoker** | Invoker | e.g., MenuItem, Button, Toolbar | Calls Execute() on its command; knows nothing about receiver or operation |
| **Receiver** | Receiver | e.g., Document, Model, Service | Has the domain knowledge to actually carry out the request |
| **Client** | Client (Application) | e.g., Application, Controller | Creates ConcreteCommand objects, sets their receivers, gives them to invokers |

If the receiver is not identifiable — i.e., the command does everything itself without delegating — that is a valid design choice for simple operations (see the "How intelligent should a command be?" discussion in the implementation guide).

---

### Step 2: Design the Command Interface and Protocol

**ACTION:** Define the Command interface. Choose the right protocol based on whether undo is required.

**WHY:** The interface design is load-bearing — every invoker, every history list, every macro depends on it. Adding Unexecute later as an afterthought usually means retrofitting all concrete commands. Decide at design time whether undo is in scope; if it is, Unexecute and Reversible belong in the base interface from the start.

**Minimal interface (no undo required):**

```
abstract class Command:
    abstract Execute()
```

**Full undo/redo interface:**

```
abstract class Command:
    abstract Execute()
    abstract Unexecute()      # Reverses the effect of Execute()
    virtual Reversible() → bool  # Default: true. Override to return false
                                 # when a command has no effect or is non-reversible
                                 # (e.g., SaveCommand — "undo save" is meaningless)
```

**Reversible() rationale:** Sometimes a command's net effect is nothing — e.g., a FontCommand applied to text that already has that font. Calling Unexecute on such a command would do equally meaningless work. `Reversible()` lets the command signal at runtime whether the undo is meaningful. Commands that return `false` are not pushed onto the history list.

**Note on state storage:** Each ConcreteCommand must store whatever state is needed to reverse itself. This typically means capturing the pre-Execute state of the receiver *before* the operation runs. What to capture:
- The receiver object reference
- The arguments that were passed to the receiver
- Any original values in the receiver that will change as a result

---

### Step 3: Implement Concrete Commands

**ACTION:** For each operation in scope, create a ConcreteCommand class that binds the receiver to a specific action.

**WHY:** The ConcreteCommand is the "binding" — it pairs a receiver object with a method call and the state needed to undo that call. This binding is what lets the invoker stay completely decoupled: the MenuItem (invoker) does not need to know about the Document (receiver) at all. The ConcreteCommand holds that reference privately.

**Pattern for each ConcreteCommand:**

```
class PasteCommand : Command:
    constructor(document: Document):
        this._document = document

    Execute():
        this._document.Paste()

    Unexecute():
        this._document.DeleteLastPaste()   # reverse the paste
```

**Pattern for operations requiring saved state (the common case):**

```
class FontCommand : Command:
    constructor(document: Document, newFont: Font, affectedRange: Range):
        this._document = document
        this._newFont = newFont
        this._affectedRange = affectedRange
        this._previousFont = null        # captured at Execute time

    Execute():
        this._previousFont = this._document.GetFont(this._affectedRange)  # save BEFORE
        this._document.SetFont(this._newFont, this._affectedRange)

    Unexecute():
        this._document.SetFont(this._previousFont, this._affectedRange)   # restore
```

**Decisions to make per command:**

| Decision | When | Why |
|----------|------|-----|
| Save state in constructor or Execute? | State that can vary per invocation (e.g., which objects are selected) should be captured at Execute time, not construction time | A MenuItem is configured once at startup; the selection it acts on changes with every user action |
| Copy before history? | If the same ConcreteCommand object is reused across invocations and its state varies, copy the command before placing it on the history list | Without copying, a shared command object would overwrite its undo state on every Execute |
| Does the command know its receiver implicitly? | When no suitable receiver class exists, or the command is self-contained (e.g., OpenCommand prompts the user, creates a Document, adds it to Application) | Self-contained commands are fine; they trade receiver flexibility for simplicity |

For the **SimpleCommand template** (languages that support generic/template types): when a command is simple — not undoable, no arguments, just calls one method on one receiver — a template can eliminate the need for a separate subclass. See `references/command-implementation-guide.md` for the SimpleCommand pattern and usage.

---

### Step 4: Implement the Undo/Redo History

**ACTION:** Implement the command history list with a present-line pointer. Apply the undo and redo algorithms exactly as specified below.

**WHY:** The history list is the mechanism that converts an individual undoable command into multi-level undo. Without the present-line pointer, you cannot distinguish "commands that have been executed" from "commands that have been undone and are available for redo." The pointer is the state machine's cursor: everything to its left is past; everything to its right is future.

**Data structure:**

```
class CommandHistory:
    _commands: List<Command>      # ordered list of executed commands
    _present: int                 # index of the most recently executed command
                                  # (or -1 if nothing has been executed yet)
```

Conceptually:

```
[ cmd1 ]—[ cmd2 ]—[ cmd3 ]—[ cmd4 ] |
 <————————— past ————————>  present
```

**Execute a new command:**

```
ExecuteCommand(cmd: Command):
    IF cmd.Reversible():
        # Discard any redo history to the right of present
        # (a new action invalidates the "future" branch)
        this._commands.truncate_after(this._present)

        cmd.Execute()

        this._commands.append(cmd)
        this._present = this._commands.last_index()
    ELSE:
        cmd.Execute()    # non-reversible commands (e.g., Save) execute but are not tracked
```

**Undo (move backward):**

```
Undo():
    IF this._present >= 0:
        cmd = this._commands[this._present]
        cmd.Unexecute()              # reverse the command
        this._present -= 1          # move present one step to the left
```

**Redo (move forward):**

```
Redo():
    next = this._present + 1
    IF next < this._commands.length:
        cmd = this._commands[next]
        cmd.Execute()                # re-execute the command
        this._present += 1          # move present one step to the right
```

**Visualizing undo then redo:**

```
Initial:
[ c1 ]—[ c2 ]—[ c3 ]—[ c4 ] |
                        present

After Undo:
[ c1 ]—[ c2 ]—[ c3 ]—[ c4 ]
                  |
                present
(c4.Unexecute() was called; c4 stays in list for potential redo)

After Undo again:
[ c1 ]—[ c2 ]—[ c3 ]—[ c4 ]
          |
        present

After Redo:
[ c1 ]—[ c2 ]—[ c3 ]—[ c4 ]
                  |
                present
(c3.Execute() was called again; present advances right)

After new command c5 (while c4 was in "future"):
[ c1 ]—[ c2 ]—[ c3 ]—[ c5 ]
                        present
(c4 is discarded — new action invalidates the old redo branch)
```

**Bounding history length:** Set a maximum length if memory or storage is a concern. When the list is full and a new command arrives, remove the oldest command from the left before appending. This sacrifices the earliest undo levels, which is almost always the correct trade-off.

**Error accumulation warning:** Errors can accumulate when a command is executed, unexecuted, and re-executed repeatedly, and the receiver's state drifts from its original values. If exact fidelity is critical, store a Memento (state snapshot) as part of the command's undo data rather than relying on computed reversal.

---

### Step 5: Implement MacroCommand (if composite operations needed)

**ACTION:** Implement MacroCommand when a single user action must execute a sequence of commands as a unit.

**WHY:** MacroCommand is Command + Composite. It lets you treat a sequence of operations identically to a single operation from the invoker's perspective. This is what enables macro recording: you collect commands into a MacroCommand as the user performs them, then play back the MacroCommand. Critically, Unexecute must iterate in *reverse* order — because applying the sub-commands' undo in original order would leave the receiver in the wrong state.

```
class MacroCommand : Command:
    _commands: List<Command> = []

    Add(cmd: Command):
        this._commands.append(cmd)

    Remove(cmd: Command):
        this._commands.remove(cmd)

    Execute():
        FOR cmd IN this._commands:           # forward order
            cmd.Execute()

    Unexecute():
        FOR cmd IN REVERSE(this._commands):  # reverse order — critical
            cmd.Unexecute()
```

**MacroCommand has no explicit receiver** — the sub-commands already define their own receivers. The MacroCommand simply orchestrates them.

**Undo order matters:** If the macro executes [A, B, C] in that order, undoing it must call [C.Unexecute(), B.Unexecute(), A.Unexecute()]. Undoing in original order (A, B, C) would try to undo A before undoing C and B, which may leave the receiver in an inconsistent intermediate state.

---

### Step 6: Wire Invokers to Commands in Client Code

**ACTION:** In the client (Application or Controller), create ConcreteCommand objects with their receivers and assign them to invokers.

**WHY:** The client is the only place that knows both the invoker and the receiver. This is intentional — the pattern's decoupling only works because this wiring happens once, in one place, at configuration time. The invoker then operates purely through the Command interface.

```
# Client code (Application setup):
document = Document("readme.txt")
history = CommandHistory()

pasteMenuItem = MenuItem()
pasteCommand = PasteCommand(document)        # bind receiver at creation
pasteMenuItem.SetCommand(pasteCommand)

# MenuItem's Clicked() handler (Invoker):
Clicked():
    history.ExecuteCommand(this._command)    # or: this._command.Execute() if no history
```

**Sharing command instances:** A menu item and a toolbar button can share the exact same ConcreteCommand instance — they both call `Execute()` on it. This is what enables "one operation, many surfaces" with zero duplication.

**Context-sensitive commands:** If the receiver changes at runtime (e.g., "paste into whichever document is currently active"), the command can resolve the receiver lazily inside Execute() rather than at construction time. This trades the simplicity of eager binding for runtime flexibility.

---

### Step 7: Verify Implementation

**ACTION:** Test the implementation against two scenarios: with-skill (using Command pattern) vs. without-skill (baseline).

**WHY:** Functional verification catches the most common implementation bugs — most often: undo restoring to the wrong state (forgot to capture pre-Execute state), redo failing (present-line pointer not advanced after redo), or MacroCommand unexecuting in wrong order.

**Verification checklist:**

- [ ] Invoker has no import or reference to the Receiver class
- [ ] Execute and Unexecute restore exact round-trip state (execute → unexecute → state matches original)
- [ ] Multiple sequential undos each restore one step correctly
- [ ] Redo after undo re-executes the correct command and advances the pointer
- [ ] New command after undo discards the redo branch (old future commands are gone)
- [ ] MacroCommand's Unexecute iterates sub-commands in reverse
- [ ] Non-reversible commands (Reversible() = false) are not placed on the history list
- [ ] Copying behavior is correct: if a command's state varies per invocation, it is copied before history placement

---

## Inputs

- Description of the operations to encapsulate (what actions, which receivers)
- Whether undo/redo is required, and if so, at what depth
- Whether macro recording or composite operations are needed
- Programming language (to apply the SimpleCommand template pattern correctly)

## Outputs

- **Command interface** (abstract class with Execute, and optionally Unexecute and Reversible)
- **ConcreteCommand classes** — one per operation in scope
- **CommandHistory** — present-line pointer implementation for unlimited undo/redo (if applicable)
- **MacroCommand** — composite command with correct forward/reverse Execute/Unexecute (if applicable)
- **Client wiring** — invoker-command-receiver binding in application setup

---

## Key Principles

- **The invoker must not know the receiver** — if the invoker imports, references, or casts to the receiver type, the decoupling is broken. The ConcreteCommand is the only place that knows both. WHY: decoupling is what allows the same Command to be triggered by a menu item, a toolbar button, and a keyboard shortcut without any of those invokers knowing about Document, Model, or Service.

- **Capture undo state at Execute time, not construction time** — a command is often constructed once (at application setup) but invoked many times. The selection, cursor position, or affected range may change between construction and invocation. WHY: capturing state at construction time would save the wrong state, making Unexecute restore to the wrong point.

- **Reversible() is a runtime predicate, not a class-level distinction** — the same class can return true or false based on execution context. WHY: a FontCommand applied to text already in that font has no effect; its Unexecute would do equal meaningless work. Reversible() prevents these no-ops from polluting the history list.

- **New command execution truncates the redo branch** — when the user undoes two steps and then performs a new action, the two undone commands are gone. WHY: the new action creates a divergent history. Preserving the old "future" would require a branching history tree, which is rarely worth the complexity. Most applications implement linear history.

- **MacroCommand unexecute must iterate in reverse** — the sub-commands of a macro may have dependencies (B assumes A has happened; undoing B before A may corrupt state). Reverse-order unexecution guarantees that each command is undone in the context where it was originally executed. WHY: forward-order undo unravels the causal chain backwards, leaving the receiver in intermediate states that were never valid program states.

- **SimpleCommand eliminates subclasses only for simple cases** — the template approach works when a command has no undo requirement and takes no extra arguments. The moment you need undo state or per-invocation arguments, a full ConcreteCommand subclass is required. WHY: trying to stretch SimpleCommand beyond its design envelope produces parameterized callbacks that are harder to read than a dedicated subclass.

---

## Examples

### Example 1: Document Editor with Multi-Level Undo

**Scenario:** A text editor with menus for Cut, Copy, Paste, and Bold. Users expect unlimited undo/redo accessible from Edit > Undo and Edit > Redo, and from Ctrl+Z / Ctrl+Y. The same Cut command should be triggerable from the menu, the toolbar, and the keyboard shortcut.

**Trigger:** "We need multi-level undo for edit operations and the same command needs to work from three different places in the UI."

**Process:**
- Step 1: Invoker = MenuItem + ToolbarButton + KeyboardHandler. Receiver = Document. Client = Application.
- Step 2: Full undo protocol — Command interface includes Execute, Unexecute, Reversible.
- Step 3: CutCommand captures the cut selection and clipboard content at Execute time. BoldCommand captures the affected range and original font at Execute time.
- Step 4: CommandHistory with present-line pointer. Edit > Undo calls `history.Undo()`. Edit > Redo calls `history.Redo()`.
- Step 6: Application creates one `CutCommand(document)`, assigns it to the menu item, toolbar button, and keyboard handler. All three share the same instance.

**Output:**
- `CutCommand.Execute()` saves selected text to clipboard, deletes from document, records deleted range + content
- `CutCommand.Unexecute()` re-inserts recorded content at recorded range, updates clipboard
- History state after three edits: `[CutCmd | BoldCmd | PasteCmd] |` (present at end)
- After two undos: `[CutCmd | BoldCmd | PasteCmd]` (present points at CutCmd)
- After typing a new character: `[CutCmd | TypeCmd]` (BoldCmd and PasteCmd discarded)

---

### Example 2: Database Transaction System

**Scenario:** A database management system needs to support atomic transactions as a sequence of insertions, updates, and deletions. The whole transaction must be undoable as a unit if it fails partway through. Operations need to be logged to disk so they can be replayed after a crash.

**Trigger:** "We need to group database operations into a transaction and undo the whole thing if any step fails."

**Process:**
- Step 1: Invoker = TransactionManager. Receiver = Database. Client = Application.
- Step 2: Full undo interface. Each operation also implements `Store()` / `Load()` for crash-recovery logging.
- Step 3: `InsertCommand` captures the inserted row's primary key for Unexecute (DELETE by key). `UpdateCommand` captures the original row values. `DeleteCommand` captures the full deleted row.
- Step 5: Transaction = MacroCommand. On success, the MacroCommand is placed on history as one unit. On failure midway, `MacroCommand.Unexecute()` reverses completed sub-commands in reverse order.
- Log persistence: after Execute, each sub-command is serialized to a log file. On crash recovery, the log is read and each command's Execute is re-applied.

**Output:**
- Transaction of [InsertCmd, UpdateCmd, DeleteCmd] executes forward; on failure after UpdateCmd, reverse unexecution: [UpdateCmd.Unexecute(), InsertCmd.Unexecute()] — DeleteCmd was never executed so it is not reversed
- History after commit: one MacroCommand on the history list, undoable as a unit
- Crash recovery: replay log by re-calling Execute on each logged command

---

### Example 3: Lexi MenuItem-Command Case Study (from GoF)

**Scenario:** The Lexi document editor (GoF chapter 2) has dozens of user operations accessible via pull-down menus and keyboard shortcuts. Operations include paste, change font, open document, quit, and save. Some are undoable (paste, font change), some are not (quit, save). MenuItems must not be subclassed per operation — one MenuItem class must serve all cases.

**Trigger:** "We have too many menu item subclasses — one per operation. Adding a new operation requires a new subclass."

**Process:**
- Step 1: Invoker = MenuItem. Receivers = Document (paste, font), Application (open, quit). Client = Application (configures menus at startup).
- Step 2: Command interface has Execute. Undo interface has Unexecute + Reversible.
- Step 3:
  - `PasteCommand(document)`: Execute calls `document.Paste()`. Undoable — stores clipboard content.
  - `FontCommand(document, font, range)`: Execute saves original font, applies new font. Undoable.
  - `OpenCommand(application)`: Execute prompts user for filename, creates Document, calls `application.Add(document)`, opens it. Not the typical receiver-delegation pattern — the command does all the work itself because there is no pre-existing receiver.
  - `QuitCommand(application)`: Execute checks if document is modified; if so, calls `save.Execute()`, then quits. Reversible() = false — not placed on history.
- Step 6: Application creates all ConcreteCommand instances at startup, assigns each to the appropriate MenuItem. MenuItem.Clicked() calls `history.ExecuteCommand(this._command)`.

**Output:**
- One MenuItem class handles all operations — the operation is entirely in the Command
- Edit menu's Undo item calls `history.Undo()` — which calls `Unexecute()` on the last reversible command
- QuitCommand does not appear in undo history
- Font change on text already in that font: `FontCommand.Reversible()` checks if font actually changed; returns false if not, preventing a no-op undo entry

---

## References

| File | When to read |
|------|-------------|
| `references/command-implementation-guide.md` | For SimpleCommand template pattern, deep state management guidance, MacroCommand subcommand ownership, and language-specific implementation notes |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-behavioral-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
