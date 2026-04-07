# Five Rules Quick Reference

The five rules from the Part I Epilogue of *The Art of Strategy* (Dixit and Nalebuff). These rules are the complete decision procedure for any strategic game — sequential or simultaneous, zero-sum or non-zero-sum. Use this reference as a one-page lookup.

---

## The Five Rules

### Rule 1: Sequential games — Look forward and reason backward

**When it applies:** Players move in turns; each player observes previous moves before choosing; game ends in a finite number of moves.

**Mechanism:** Construct a game tree. Starting at the terminal nodes (where outcomes are known), fold backward by replacing each node with the optimal choice of the player who moves there. Continue until you reach the first move.

**Key insight:** Future actions by rational players are predictable, not uncertain. "Look forward" means identify what the game ultimately leads to. "Reason backward" means calculate what choice at the first move leads to that desired outcome.

**Tool:** `backward-reasoning-game-solver`

**Failure mode:** Forward reasoning — choosing the action that looks best immediately without tracing the full chain of consequences.

---

### Rule 2: Simultaneous games — Check for dominant strategies

**When it applies:** Players choose without observing the other's current move. Applied first in any simultaneous game analysis.

**Mechanism:** For each player, check whether any one strategy outperforms all other strategies regardless of what the opponent does. If a dominant strategy exists, use it. If your opponent has a dominant strategy, predict they will use it and respond accordingly.

**Key insight:** A dominant strategy eliminates the "what will they do?" problem. You don't need to predict the opponent's action — the strategy is best no matter what they do.

**Tool:** `nash-equilibrium-analyzer` (handles dominant strategy detection)

**Failure mode:** Searching for a "clever" response to anticipated opponent moves when a dominant strategy already makes that search unnecessary.

---

### Rule 3: No dominant strategy — Eliminate dominated strategies successively

**When it applies:** No player has a dominant strategy (or after dominant strategies have been identified and played, the residual game still has multiple strategies per player).

**Mechanism:** A dominated strategy is one that is uniformly worse than some other strategy, regardless of opponent choices. Remove it. After removal, re-examine the smaller game — new dominant or dominated strategies may now appear. Repeat until the game resolves or cannot be further reduced.

**Key insight:** Dominated strategies will never be played by rational players. Knowing this shrinks the game and may reveal solutions that were hidden in the full game.

**Tool:** `nash-equilibrium-analyzer` (covers iterated elimination)

**Failure mode:** Analyzing all combinations in a large game matrix without first eliminating dominated strategies, wasting effort on branches that rational players would never reach.

---

### Rule 4: No dominant or dominated strategies — Find Nash equilibrium

**When it applies:** After Rules 2 and 3 have been applied (or found not to apply), the game still has no clear solution.

**Mechanism:** A Nash equilibrium is a combination of strategies such that each player's strategy is their best response to the other players' strategies. Neither player can benefit by unilaterally deviating. Find the equilibrium by checking all remaining strategy combinations for mutual best-response.

**Key insight:** Nash equilibrium is the logical resting point of strategic reasoning — the only combination of strategies where all players are simultaneously satisfied with their choices given what the others are doing. Multiple equilibria may exist; in that case, a focal point or coordination mechanism is needed.

**Tool:** `nash-equilibrium-analyzer`

**Failure mode:** Stopping at a strategy combination without verifying it is a mutual best response — finding "a good strategy" rather than "an equilibrium strategy."

---

### Rule 5: Zero-sum game with no pure equilibrium — Mix strategies

**When it applies:** The game is zero-sum (one player's gain is exactly the other's loss) and there is no pure-strategy Nash equilibrium (which is always the case in zero-sum games like Rock-Paper-Scissors and penalty kicks where any predictable choice can be exploited).

**Mechanism:** Calculate mixed-strategy probabilities such that the opponent is indifferent between their available strategies. At a mixed-strategy equilibrium, randomizing in the right proportions makes you unpredictable and exploitable-proof.

**Key insight:** In zero-sum games with no pure equilibrium, predictability is exploitability. The goal of mixing is not to confuse — it is to make the opponent indifferent, which is the only state where neither player can improve by deviating from the mix.

**Tool:** `nash-equilibrium-analyzer` (covers mixed strategies)

**Failure mode:** Rotating strategies in a predictable pattern (thinking that "changing it up" is the same as mixing). Any detectable pattern — even a rotation — can be exploited. True mixing requires randomization.

---

## Decision Flow

```
Start: Describe the game (players, moves, payoffs)
         |
         v
Is the game SEQUENTIAL?
(players observe moves before choosing)
  |
  Yes --> Apply Rule 1: Look forward, reason backward
          --> backward-reasoning-game-solver
  |
  No  --> Game is SIMULTANEOUS
          |
          v
       Does any player have a DOMINANT STRATEGY?
         |
         Yes --> Apply Rule 2: Use it (and predict opponent uses theirs)
                 --> nash-equilibrium-analyzer
         |
         No  --> Can any strategy be ELIMINATED as dominated?
                 |
                 Yes --> Apply Rule 3: Eliminate successively
                         --> nash-equilibrium-analyzer
                 |
                 No  --> Look for NASH EQUILIBRIUM (mutual best responses)
                         |
                         Found: unique --> Apply Rule 4: Use it
                         Found: multiple --> Need focal point/coordination
                         Not found (zero-sum game) --> Apply Rule 5: Mix
                         --> nash-equilibrium-analyzer
```

---

## Combined Game Note

In practice, many games have both sequential and simultaneous stages (football, auctions with rounds, multi-stage negotiations). The approach:

1. Identify all simultaneous sub-games and solve them using Rules 2-5
2. Substitute the equilibrium payoffs from each simultaneous sub-game back into the larger sequential game tree
3. Apply Rule 1 to the full sequential structure with these substituted payoffs

This combination is why `strategic-situation-analyzer` is the entry point: it identifies the structure so the right tools are applied in the right order.

---

## What the Rules Do NOT Cover

These five rules address how to find optimal strategies within a given game. They do not address:

- **Changing the game itself** — modifying payoffs, timing, or information structure before the game is played → `strategic-commitment-designer`
- **Repeated game dynamics** — how cooperation can be sustained over time through reciprocity and reputation → `prisoners-dilemma-resolver`
- **Hidden information** — when one player knows something the other doesn't → `information-asymmetry-strategist`
- **Institutional design** — designing rules, incentives, or mechanisms for others to play within → `incentive-scheme-designer`, `auction-bidding-strategist`, `voting-system-strategist`
- **Bargaining over the surplus** — when the game produces joint value and the question is how to divide it → `negotiation-strategist`
