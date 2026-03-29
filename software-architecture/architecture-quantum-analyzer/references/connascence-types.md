# Connascence Types Reference

Connascence defines how components are coupled. Two components are connascent if a change in one requires the other to be modified to maintain correctness. Use this to identify quantum boundaries.

## Static Connascence (discoverable from source code)

| Type | Description | Quantum impact |
|------|-----------|---------------|
| **Name (CoN)** | Components agree on entity names | Weakest. Normal coupling. |
| **Type (CoT)** | Components agree on entity types | Normal coupling. |
| **Meaning (CoM)** | Components agree on meaning of values (e.g., TRUE=1) | Moderate coupling. |
| **Position (CoP)** | Components agree on parameter order | Moderate coupling. |
| **Algorithm (CoA)** | Components agree on an algorithm (e.g., hashing) | Strongest static. Cross-service algorithm agreement = tight coupling. |

Static connascence exists at compile time. It indicates structural coupling but does NOT define quantum boundaries by itself.

## Dynamic Connascence (observable at runtime)

| Type | Description | Quantum impact |
|------|-----------|---------------|
| **Execution (CoE)** | Order of execution matters | Implies synchronous coordination. |
| **Timing (CoT)** | Timing of execution matters (race conditions) | Implies shared fate — same quantum. |
| **Values (CoV)** | Multiple values must change together (distributed transactions) | Strong coupling — same quantum or explicit saga pattern. |
| **Identity (CoI)** | Components reference the same entity | Strongest dynamic. Shared mutable state = same quantum. |

## The Quantum Rule

**Synchronous connascence = same quantum.** If Component A synchronously waits for Component B's response, they share operational fate for the duration of the call. Their availability, scalability, and performance characteristics must be compatible.

**Asynchronous communication breaks quantum boundaries.** Fire-and-forget via message queues means Component A does not wait for Component B. They can have independent operational characteristics.

## Strength Ordering (weakest to strongest)

```
Static: Name → Type → Meaning → Position → Algorithm
Dynamic: Execution → Timing → Values → Identity
```

Stronger connascence = harder to refactor = more likely to be within the same quantum.
