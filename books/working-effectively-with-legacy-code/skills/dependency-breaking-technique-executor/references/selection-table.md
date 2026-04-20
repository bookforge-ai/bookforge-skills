# Dependency-Breaking Technique Selection Table

Comprehensive matrix for selecting the right technique from Feathers' catalog of 24. Three lenses:

1. **Primary matrix** — dependency type × language × constraint → technique
2. **Symptom-from-Ch9 cross-reference** — Feathers' 7 "can't get class into test harness" cases → technique
3. **Language applicability quick-ref** — which techniques apply to which languages

---

## Primary Selection Matrix

| Dependency Type | Language | Constraint | Best Technique | Alternative |
|-----------------|----------|------------|----------------|-------------|
| Constructor creates one concrete object | Java / C# | Localized | **Parameterize Constructor** | Extract and Override Factory Method |
| Constructor creates one concrete object | C++ | Localized | **Parameterize Constructor** | Supersede Instance Variable |
| Constructor creates chained objects | Java / C# | Moderate | **Extract and Override Factory Method** | Parameterize Constructor |
| Constructor creates chained objects (C++) | C++ | Moderate | **Extract and Override Getter** | Supersede Instance Variable |
| Constructor has elaborate side-effect chain | OO | Complex | **Extract and Override Factory Method** | Break Out Method Object |
| Method creates concrete object internally | OO | Localized | **Parameterize Method** | Extract and Override Call |
| Parameter is hard-to-fake concrete class | OO | Localized | **Extract Interface** | Adapt Parameter |
| Parameter class cannot be modified | OO | — | **Adapt Parameter** | — |
| Interface name already equals class name | Java / C# | — | **Extract Implementer** | Extract Interface (with rename) |
| Parameter is sealed / final / value type | OO | — | **Subclass and Override Method** | Primitivize Parameter |
| Method calls a static method | OO | Localized | **Extract and Override Call** | Introduce Instance Delegator |
| Method calls static; need instance injection | OO | — | **Introduce Instance Delegator** → Parameterize Method | — |
| Global / static variable — one method | OO | Localized | **Replace Global Reference with Getter** | Extract and Override Call |
| Global / static variable — spread across class | OO / C++ | Pervasive | **Encapsulate Global References** | Replace Global Reference with Getter (×N) |
| Singleton blocking tests | OO | — | **Introduce Static Setter** | Extract Interface + Parameterize Constructor |
| Few bad-dependency methods, rest are fine | OO | Localized | **Subclass and Override Method** | Pull Up Feature |
| Many bad-dependency methods, few good ones | OO | Pervasive | **Push Down Dependency** | — |
| Method too long, uses instance data | OO | — | **Break Out Method Object** | Pull Up Feature |
| Method is short, pure (no instance data) | OO | — | **Expose Static Method** | Parameterize Method |
| Global functions (C procedural) | C | Localized | **Replace Function with Function Pointer** | Link Substitution |
| Whole library / translation unit | C / C++ / Java | Build-level | **Link Substitution** | Definition Completion |
| C++ header chain (`#include` cascade) | C++ | — | **Definition Completion** | Link Substitution |
| Dependency is a template type parameter | C++ | — | **Template Redefinition** | Extract Interface |
| Language is interpreted / dynamic | Python / Ruby / JS | — | **Text Redefinition** | Subclass and Override Method |
| Parameter type too complex to fake | OO | Last resort | **Primitivize Parameter** | Adapt Parameter |

### Pervasive vs. Localized Decision Guide

**Localized** = the dependency appears in one or two places; a per-site technique (Extract and Override Call, Replace Global Reference with Getter) costs less.

**Pervasive** = the same dependency appears across 3+ methods or across multiple classes; a structural technique (Encapsulate Global References, Push Down Dependency) pays back the setup cost.

When in doubt, count call sites before choosing. If 3 or more: structural technique. If 1–2: per-site technique.

---

## Symptom-from-Chapter-9 Cross-Reference

Feathers' Chapter 9 ("I Can't Get This Class into a Test Harness") enumerates 7 named cases. Each maps to one or more techniques from Part III.

| Ch9 Case Name | Symptom | Technique(s) |
|---------------|---------|--------------|
| **Irritating Parameter** | Constructor needs a hard-to-create concrete object | Extract Interface on the parameter type; or Pass Null (when the parameter is not used in the test path) |
| **Hidden Dependency** | Constructor acquires a resource inside itself (file, socket, DB, mail) without the caller knowing | **Parameterize Constructor** |
| **Construction Blob** | Constructor calls a chain of constructors that each create more objects | **Extract and Override Factory Method** (Java/C#); **Extract and Override Getter** (C++) |
| **Irritating Global Dependency** | Constructor or methods access a Singleton or global static | **Introduce Static Setter** + Extract Interface (to allow subclassing the singleton) |
| **Horrible Include Dependencies** | C++ class includes headers that pull in OS/platform code that cannot compile in test | **Definition Completion** |
| **Onion Parameter** | Constructor requires an object that requires another object that requires another object | **Extract Interface** on the outermost layer; or Pass Null for layers not exercised in test |
| **Aliased Parameter** | Parameter is a concrete class you cannot extract an interface from (sealed, final, or third-party without source) | **Subclass and Override Method** on the production class; or **Adapt Parameter** to create a new narrow interface |

**Root cause map (Feathers' 4 root causes → cases):**

| Root Cause | Cases |
|------------|-------|
| Objects cannot be created easily | Irritating Parameter, Onion Parameter, Aliased Parameter |
| Test harness won't build | Horrible Include Dependencies |
| Constructor has bad side effects | Hidden Dependency, Construction Blob |
| Significant work done in constructor | Construction Blob, Irritating Global Dependency |

---

## Language Applicability Quick-Ref

### Techniques Available in ALL OO Languages (Java, C#, C++, Python, Ruby)
- Adapt Parameter
- Break Out Method Object
- Expose Static Method
- Extract and Override Call
- Extract and Override Factory Method *(except C++ — see below)*
- Extract Interface
- Extract Implementer
- Parameterize Constructor
- Parameterize Method
- Pull Up Feature
- Push Down Dependency
- Replace Global Reference with Getter
- Subclass and Override Method

### Techniques with C++ Restrictions or Specializations
| Technique | C++ Status | Note |
|-----------|-----------|------|
| Extract and Override Factory Method | **Not applicable** | Virtual dispatch not active in C++ constructors |
| Extract and Override Getter | **C++ primary** | Lazy-init getter pattern; solves the constructor virtual problem |
| Supersede Instance Variable | **C++ primary** | Post-construction variable replacement; less safe than getter approach |
| Definition Completion | **C++ only** | Exploits header/translation unit separation |
| Template Redefinition | **C++ only** | Exploits template type parameters |
| Replace Function with Function Pointer | **C primary** | Applicable in C++, but OO techniques preferred |
| Encapsulate Global References | **C/C++ primary** | Designed for C-era global variables; applicable anywhere with globals |

### Techniques for Java / C# Only
| Technique | Note |
|-----------|------|
| Introduce Static Setter | Primarily singleton-pattern languages (Java/C#/C++) |
| Extract Implementer | Most natural in Java/C# with formal interfaces |
| Introduce Instance Delegator | Most useful in Java/C# where statics are common utility patterns |

### Techniques for Dynamic / Interpreted Languages Only
| Technique | Languages |
|-----------|-----------|
| Text Redefinition | Ruby, Python, JavaScript, Perl, Smalltalk, Groovy |

### Techniques for Build-Level Substitution (Any Language)
| Technique | Languages |
|-----------|-----------|
| Link Substitution | C, C++, Java (classpath), .NET (assembly-level with care) |
| Definition Completion | C++ only |

---

## Technique Family Summary

For a higher-level mental model, the 24 techniques group into six families:

| Family | Techniques | Core Mechanism |
|--------|-----------|----------------|
| **Interface/Adapter** | Extract Interface, Extract Implementer, Adapt Parameter | Shape a dependency into a testable abstraction |
| **Parameterize** | Parameterize Constructor, Parameterize Method | Pass dependencies in; don't create them internally |
| **Subclass/Override** | Subclass and Override Method, Extract and Override Call, Extract and Override Factory Method, Extract and Override Getter | Use OOP seams for runtime substitution |
| **Encapsulate/Expose** | Encapsulate Global References, Expose Static Method, Replace Global Reference with Getter, Introduce Static Setter, Introduce Instance Delegator | Control access to globals and statics |
| **Language-specific** | Template Redefinition, Text Redefinition, Replace Function with Function Pointer, Definition Completion, Link Substitution | Exploit the build model of C++, C, or dynamic languages |
| **Method/Class Object** | Break Out Method Object, Pull Up Feature, Push Down Dependency, Supersede Instance Variable, Primitivize Parameter | Restructure class or method to isolate dependencies |

---

## Decision Flowchart (Abbreviated)

```
START: What is blocking testability?
│
├─ Constructor hard-codes object creation
│   ├─ Simple (one object)?  →  Parameterize Constructor
│   ├─ Complex chain?  →  Extract and Override Factory Method (Java/C#)
│   │                      Extract and Override Getter (C++)
│   └─ Language = C++, already constructed?  →  Supersede Instance Variable
│
├─ Parameter type is a concrete class
│   ├─ Can I modify the parameter class?  →  Extract Interface
│   ├─ Cannot modify (third-party/sealed)?  →  Adapt Parameter
│   └─ Cannot extract interface at all?  →  Subclass and Override Method
│
├─ Method calls a static or global
│   ├─ One localized call?  →  Extract and Override Call
│   ├─ Same global in many methods?  →  Encapsulate Global References
│   ├─ Global is a Singleton?  →  Introduce Static Setter
│   └─ Need instance-level delegation?  →  Introduce Instance Delegator
│
├─ Bad dependencies in some methods of the class
│   ├─ Bad methods are FEW?  →  Subclass and Override Method or Pull Up Feature
│   └─ Bad methods are MANY?  →  Push Down Dependency
│
├─ C/C++ specific
│   ├─ Header cascade?  →  Definition Completion
│   ├─ C global functions?  →  Replace Function with Function Pointer
│   ├─ Template type?  →  Template Redefinition
│   └─ Whole-library fake?  →  Link Substitution
│
└─ Dynamic language (Ruby/Python)?  →  Text Redefinition
```

---

*For full step-by-step mechanics of each technique, see `all-techniques.md`. For inline mechanics of the 6 most common techniques (Parameterize Constructor, Parameterize Method, Extract Interface, Subclass and Override Method, Encapsulate Global References, Extract and Override Factory Method), see the SKILL.md body.*
