# Game Tree Construction Reference

## Node Labeling Conventions

### Standard Notation

- **Decision node:** Circle or labeled box with the player's name or identifier (P1, P2, etc.)
- **Chance node:** Diamond or circle marked "Nature" or "N" — used when probability resolves the branch rather than a player
- **Terminal node:** Rectangle or square with payoffs listed for each player in the order they entered the game (P1 payoff, P2 payoff, ...)
- **Branch:** Arrow from node to next node or terminal, labeled with the action name
- **Selected branch (backward induction result):** Thickened line or arrowhead added after solving

### Payoff Representation

Two formats work equally well:

**Ordinal (rankings):** Use when exact utilities are unknown but preference ordering is clear.
- "4 = best, 1 = worst" for each player listed separately
- Example terminal node: `[Congress: 3, President: 3]`

**Cardinal (utilities or money):** Use when magnitudes matter (expected value calculations require cardinal payoffs).
- Example terminal node: `[Charlie: -$100,000, Fredo: +$500,000]`

When preferences are mixed (one player's ranking is clear, another's is ambiguous), estimate and state assumptions explicitly.

---

## Tree Structure for Common Game Types

### Two-Player Alternating Game (Most Common)

```
P1 (root)
├── Action A → P2
│              ├── Response 1 → Terminal [P1: x, P2: y]
│              └── Response 2 → Terminal [P1: x', P2: y']
└── Action B → P2
               ├── Response 1 → Terminal [P1: a, P2: b]
               └── Response 2 → Terminal [P1: a', P2: b']
```

### Three-Stage Game

```
P1 (root)
├── A1 → P2
│         ├── B1 → P1
│         │        ├── C1 → Terminal
│         │        └── C2 → Terminal
│         └── B2 → P1
│                  ├── C3 → Terminal
│                  └── C4 → Terminal
└── A2 → Terminal
```

Note: P1 appears at both the root and at Stage 3. At Stage 3, P1 optimizes for their own payoff given what has already happened — they do not undo the prior move. The game is still solved by backward induction starting from the Stage 3 nodes.

### Game with Chance Node

```
P1 (root)
└── Risky Action → Nature (N)
                    ├── Success (prob p) → P2
                    │                       ├── ...
                    └── Failure (prob 1-p) → Terminal [P1: 0, P2: 0]
```

At a chance node, do not pick the "best" branch — compute the expected payoff (probability × payoff) and fold that expected value back to the previous decision node.

---

## Handling Very Large Trees

When the game has many players, many stages, or many actions per node, drawing the full tree is impractical. Two approaches:

### Approach 1: Logical Description by Layer

Instead of drawing, describe the tree layer by layer:

- Layer 0 (root): P1 chooses from {A, B, C}
- Layer 1: If A, P2 chooses from {D, E}; if B, P2 chooses from {F}; if C, game ends
- Layer 2: If D, P1 chooses from {G, H}; if E, game ends; if F, P1 chooses from {I, J}
- Terminal payoffs: G → [P1: 3, P2: 1]; H → [P1: 1, P2: 4]; E → [P1: 2, P2: 2]; I → [P1: 4, P2: 0]; J → [P1: 0, P2: 3]

Then apply backward induction layer by layer from the terminals.

### Approach 2: Pattern Recognition + Formula

For combinatorial games where the structure is regular (same choices available regardless of history, only the state size changes), derive the winning-position pattern from small cases and generalize. See `combinatorial-game-formulas.md`.

---

## The Critical Rule: Resolve All Nodes Including Counterfactual Ones

A node is "counterfactual" if the backward induction solution predicts it will never be reached. It must still be resolved.

**Why:** Player at node X makes decisions based on what would happen at node Y if X chose the branch leading there. If Y is unresolved, X's calculation is incomplete.

**Example:** In the Congress/President line-item veto game (p. 53-54 of source), Congress's optimal move depends on what the President would do if Congress passed each possible bill. Even if Congress ends up passing "neither" (and thus the President's nodes for "U only" and "M only" are never reached), Congress must reason through what the President would do there to know that passing neither is optimal.

Mark unresolved counterfactual nodes with dashed lines to distinguish them from the predicted equilibrium path.

---

## Common Construction Errors

| Error | Consequence | Fix |
|---|---|---|
| Pruning a branch before resolving it | Incorrect backward induction at parent node | Resolve all branches before pruning |
| Using your own payoffs at opponent's nodes | Wrong prediction of opponent's choice | At each node, use the payoffs of the player who moves there |
| Merging sequential and simultaneous stages | Invalid tree structure | Model simultaneous stages as a sub-game payoff matrix; substitute equilibrium payoffs into the tree |
| Omitting chance nodes | Overstated certainty | Insert Nature nodes wherever probability (not choice) determines outcomes |
| Stopping the tree before all paths terminate | Cannot apply backward induction | Extend every path until payoffs are reachable (add "game continues" node if truly unbounded) |
