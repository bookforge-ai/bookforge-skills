# Game Type Classifier

Identifies the type of simultaneous-move game to ensure the correct analysis method is applied.

---

## Why Classification Matters

The correct strategy depends on the game type:

| Game Type | Interests | Pure Equilibria? | Mixing? |
|---|---|---|---|
| Zero-sum / pure conflict | Exactly opposed | Sometimes | Yes — Rule 5 applies |
| Coordination | Aligned | Usually multiple | No — focal point instead |
| Mixed-motive | Partly aligned, partly opposed | Often multiple | Possible but fragile |
| Prisoners' dilemma | Individually rational, collectively bad | One (bad) | No |

---

## Zero-Sum (Pure Conflict) Games

**Signature:** What one player gains, the other loses exactly. Payoffs in each cell sum to a constant (often 0 or 100).

**Examples:** Penalty kicks, military feints, inspection/evasion, competitive espionage, zero-sum market share battles.

**Identifying test:** In each cell of the payoff matrix, check if the two payoffs sum to the same number (or to 0 if negative payoffs are used). If yes, zero-sum.

**Analysis approach:**
1. Show only row player's payoffs (column player's = constant minus row's)
2. Check for dominant strategies first
3. If no pure equilibrium, use Rule 5 (indifference principle)
4. Mixing is optimal and necessary if the game has no pure Nash equilibrium

---

## Coordination Games

**Signature:** Players benefit from matching each other's choices. Miscoordination produces the worst outcomes. Both players prefer any coordination to no coordination.

**Examples:** Meeting point selection, platform adoption, technology standards, project methodology alignment, driving on the same side of the road.

**Identifying test:** The best cells are on the diagonal (where players match), and these are all better than off-diagonal cells for both players.

**Classic structures:**
- **Pure coordination:** Players have identical preferences over the equilibria (stag hunt, meeting game)
- **Battle of sexes:** Players agree that coordinating beats mismatching, but disagree about which coordinated outcome is better

**Analysis approach:**
1. Find all Nash equilibria (typically multiple)
2. Do NOT apply Rule 5 (mixing) — uncoordinated mixing leads to miscoordination
3. Apply focal-point analysis to select an equilibrium
4. If repeated interaction, consider alternation or explicit agreement

**Anti-pattern warning:** Applying the indifference principle to a coordination game produces a mixed strategy equilibrium, but this equilibrium has lower expected payoff than either pure equilibrium. Players who independently follow this mixed strategy will end up miscoordinated more than the pure equilibria would predict.

---

## Mixed-Motive Games (Non-Zero-Sum with Conflict)

**Signature:** Players have some aligned interests (prefer coordination to chaos) but different preferences about which outcome to coordinate on.

**Examples:** Chicken game, competitive promotions (Coke/Pepsi), labor negotiations, technology format wars.

**Identifying test:** There are multiple Nash equilibria, and different players prefer different equilibria.

**Analysis approach:**
1. Find all pure Nash equilibria
2. A mixed Nash equilibrium exists but typically has lower expected payoffs than the pure equilibria
3. Consider commitment devices to secure the preferred equilibrium (see commitment-strategy-designer skill)
4. If the game is repeated, cooperation solutions may dominate

---

## Prisoners' Dilemma Structure

**Signature:** Each player has a dominant strategy that leads to a collectively bad outcome. The Nash equilibrium is worse for both than a coordinated alternative.

**Identifying test:** One strategy strictly dominates all others for each player, and the resulting Nash equilibrium is Pareto-dominated (both players would prefer a different outcome if they could coordinate).

**Analysis approach:**
1. Apply Rule 2 (dominant strategy) — the equilibrium is determined
2. Note that the equilibrium is stable even though both parties would prefer mutual cooperation
3. In repeated interactions, cooperation may be sustained (separate repeated-games skill)

---

## Quick Classification Protocol

1. Do payoffs in each cell sum to a constant? → **Zero-sum** → use Rule 5 if no pure equilibrium
2. Are all on-diagonal outcomes better for both players than off-diagonal? → **Coordination game** → focal-point analysis, no mixing
3. Does one strategy dominate for each player, but the result is worse than mutual cooperation? → **Prisoners' dilemma** → dominant strategy equilibrium, note the trap
4. None of the above → **Mixed-motive** → find all equilibria, consider commitment or repetition
