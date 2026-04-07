# Combinatorial Game Formulas Reference

## The k+1 Winning-Position Formula

### Setup
- A pile of N objects
- Players alternate turns
- On each turn, a player must take between 1 and k objects (inclusive)
- The player who takes the **last** object(s) **wins**

### Formula

**Losing positions:** Any count that is a **multiple of (k+1)**

If you face a multiple of (k+1) and your opponent plays perfectly, you cannot win.

**Winning positions:** Any count that is **not** a multiple of (k+1)

Your winning move: take enough objects to leave your opponent with the nearest multiple of (k+1).
- Winning move = (current count) mod (k+1)
- This leaves opponent with count = current - [(current mod (k+1))], which is a multiple of (k+1)

### 21-Flags Example (k=3)

k+1 = 4. Losing positions: 4, 8, 12, 16, 20.

| Count facing you | Your status | Correct move |
|---|---|---|
| 21 | Winning | Take 1 (leave 20) |
| 20 | Losing | No winning move |
| 19 | Winning | Take 3 (leave 16) |
| 18 | Winning | Take 2 (leave 16) |
| 17 | Winning | Take 1 (leave 16) |
| 16 | Losing | No winning move |
| 13 | Winning | Take 1 (leave 12) |
| 12 | Losing | No winning move |
| 9 | Winning | Take 1 (leave 8) |
| 8 | Losing | No winning move |
| 5 | Winning | Take 1 (leave 4) |
| 4 | Losing | No winning move |
| 3 | Winning | Take 3 (take last, win) |
| 2 | Winning | Take 2 (take last, win) |
| 1 | Winning | Take 1 (take last, win) |

### Verification by Backward Induction

From the terminal nodes backward:
- 1, 2, 3 objects → Winning (take them all)
- 4 objects → Losing (whatever you take — 1, 2, or 3 — opponent takes the rest)
- 5, 6, 7 objects → Winning (take 1, 2, or 3 to leave opponent with 4)
- 8 objects → Losing
- Pattern: every multiple of 4 is a losing position

This is why the formula is derivable from first principles rather than memorized: run backward induction on small cases, observe the pattern, project it forward.

---

## Hot Potato Variant (Last Taker Loses)

Same setup, but the player who takes the last object **loses**.

The losing positions shift by one: a player facing exactly **1** object loses (must take it). Back-propagate:
- 1 → Lose
- 2, 3, 4 → Win (take enough to leave opponent with 1)
- 5 → Lose (any move leaves opponent with 1, 2, 3, 4 — all winning for opponent)

**Revised formula:** Losing positions are counts of the form (k+1)·m + 1 for integer m ≥ 0.

For k=3: losing positions are 1, 5, 9, 13, 17, 21.

If starting count is 21 (a losing position in hot potato), the second player wins, not the first.

---

## Multi-Pile (Nim) Generalization

When there are multiple piles and a player takes any number from one pile per turn, the solution involves XOR (exclusive or) of pile sizes in binary representation. This is standard Nim theory.

For a quick heuristic (exact for two piles):
- Two piles of equal size → the player who faces them loses (second-mover wins by mirroring)
- Two piles of unequal size → first player wins by equalizing the piles

For three or more piles, use the XOR rule: if XOR of all pile sizes = 0, it is a losing position; otherwise it is a winning position. The winning move is to take from any pile such that XOR of remaining piles = 0.

---

## Worked Tables for Common Starting Counts

### k=2 (take 1 or 2), last taker wins

k+1 = 3. Losing positions: 3, 6, 9, 12, ...

| Starting count | First player status | Winning first move |
|---|---|---|
| 10 | Win | Take 1 (leave 9) |
| 9 | Lose | No winning move |
| 7 | Win | Take 1 (leave 6) |
| 6 | Lose | No winning move |

### k=4 (take 1, 2, 3, or 4), last taker wins

k+1 = 5. Losing positions: 5, 10, 15, 20, 25, ...

| Starting count | First player status | Winning first move |
|---|---|---|
| 21 | Win | Take 1 (leave 20) |
| 20 | Lose | No winning move |
| 17 | Win | Take 2 (leave 15) |
| 15 | Lose | No winning move |

---

## Deriving the Formula for a New Game

If you encounter a combinatorial game not matching these patterns, derive from scratch:

1. Solve the terminal cases (1, 2, 3, ... objects) by inspection.
2. Label each as W (winning) or L (losing).
3. A position is L if and only if all moves from it lead to W positions.
4. A position is W if and only if at least one move leads to an L position.
5. List the L positions: 1, ?, ?, ...
6. Identify the gap between consecutive L positions — that gap is (k+1) for standard takeaway games.
7. Project the pattern forward.
