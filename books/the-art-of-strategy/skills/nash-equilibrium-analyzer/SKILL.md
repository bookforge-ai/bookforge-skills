---
name: nash-equilibrium-analyzer
description: Find Nash equilibria in simultaneous-move games by constructing payoff matrices, eliminating dominated strategies (Rules 2-3), mapping best responses (Rule 4), and calculating mixed strategy proportions using the indifference principle (Rule 5). Use this skill when two or more players choose actions simultaneously without seeing each other's moves — pricing decisions, product launches, competitive bids, penalty kicks, resource allocation conflicts — and you need to identify stable strategy configurations, calculate exact mixing proportions for zero-sum conflicts, or select among multiple equilibria using focal-point analysis.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-art-of-strategy/skills/nash-equilibrium-analyzer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy: A Game Theorist's Guide to Success in Business and Life"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [4, 5]
tags: [game-theory, decision-making, equilibrium-analysis, competitive-strategy, mixed-strategy]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of a strategic situation with simultaneous choices: players, available strategies, and payoffs (or enough information to estimate them)."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Works from a strategic situation description. Output: payoff matrix, equilibrium analysis, and strategy recommendation."
discovery:
  goal: "Identify Nash equilibria — strategy combinations where no player can improve by changing course alone — and prescribe which to play, including exact mixing proportions when pure strategies leave you exploitable."
  tasks:
    - "Build or validate the payoff matrix for all strategy combinations"
    - "Check for dominant strategies and eliminate dominated ones (Rules 2-3)"
    - "Map best responses to find cells where both players are simultaneously best-responding (Rule 4)"
    - "Calculate mixed strategy proportions using the indifference principle when no pure equilibrium exists (Rule 5)"
    - "Apply focal-point analysis when multiple equilibria exist"
  audience: "strategists, managers, product managers, negotiators, business professionals facing competitive simultaneous-choice situations"
  when_to_use: "When players choose actions simultaneously without observing each other's moves and you need to predict stable outcomes or prescribe optimal play"
  environment: "Strategic situation description with identifiable players, strategies, and payoffs. The agent constructs the matrix; the user need not supply pre-built tables."
  quality: placeholder
---

# Nash Equilibrium Analyzer

## When to Use

A simultaneous-move game is one where each player chooses without observing the other's choice — there is no first mover, no look-forward-and-reason-backward structure. Both choose at the same moment (or in sealed envelopes, or with mutual concealment). Apply this skill when:

- Players are deciding simultaneously: pricing, product launch timing, bidding, competitive positioning
- You face a repeating conflict where being predictable makes you exploitable: penalty kicks, advertising schedules, audit strategies, military feints
- Multiple outcomes each look like equilibria and you need to select one
- You want to know whether randomizing (mixing) beats committing to one action

**What this skill does not cover:** Games with sequential moves (one player chooses, then the other responds) use backward induction instead. If players observe each other's choices before responding, use the sequential-game framework.

**The four-rule sequence:**
1. Build the payoff matrix
2. Find and use any dominant strategy (Rule 2)
3. Eliminate dominated and never-best-response strategies successively (Rule 3)
4. Search remaining cells for mutual best responses — Nash equilibrium (Rule 4)
5. If no pure-strategy equilibrium, compute mixing proportions using the indifference principle (Rule 5)

---

## Context and Input Gathering

### Required Information

Before building the matrix, gather:

- **Players:** Who are the decision-makers? List each one.
- **Strategies:** What choices does each player have? List all options.
- **Payoffs:** For each combination of choices, what does each player get? Payoffs can be profits, success rates, scores, or any numerical representation of outcomes.

If payoffs are not precisely known, estimate them directionally (High/Medium/Low) or ask the user to rank outcomes — ordinal payoffs often suffice to find equilibria.

### Observable Context

If a situation description is provided, look for:
- Statements about what each player "prefers" or "would choose" — these indicate payoff ranking
- Outcome descriptions that depend on both players' choices simultaneously — confirms simultaneous structure
- Any statement that one strategy "always beats" another regardless of what others do — signals a dominant strategy
- Situations where interests are exactly opposed ("every dollar I gain, you lose") — signals a zero-sum game requiring Rule 5

### Sufficiency Check

You can proceed when:
1. You can name every player
2. You can list every strategy option per player
3. You can estimate payoffs for each combination (even approximate rankings)

If payoff information is missing, ask: "What outcome does Player X get if they choose A while Player Y chooses B?" Repeat until the matrix is complete or estimates are sufficient.

---

## Execution

### Step 1 — Build the Payoff Matrix

Construct a table with rows for one player's strategies and columns for the other's. Each cell contains both players' payoffs.

**Convention:** Row player's payoff in the southwest corner of each cell; column player's payoff in the northeast corner. (In zero-sum games, show only the row player's payoff since the column player's is always the complement.)

**Why build it explicitly:** The matrix makes all 2n combinations visible at once. Without it, players reason about their options in sequence, miss interactions, and reach wrong conclusions. The matrix converts circular "what if they..." thinking into simultaneous inspection.

For games with many strategies (more than 4-5 per player), build the matrix in a spreadsheet and note that software can compute equilibria directly. The manual method below applies to small games; the concepts transfer to large ones.

**Example — Pricing game (2 firms, 2 prices):**

|  | Rival: Low | Rival: High |
|---|---|---|
| **You: Low** | 40, 40 | 60, 20 |
| **You: High** | 20, 60 | 80, 80 |

---

### Step 2 — Check for Dominant Strategies (Rule 2)

A **dominant strategy** is one that gives you a higher payoff than every other option you have, regardless of what your opponent does.

**How to check:** For each of your strategies, compare its payoff across every column (every opponent strategy). If one row always produces a higher payoff than all other rows, it is dominant.

**If a dominant strategy exists:** Play it. No further analysis is needed for that player. Also expect rational opponents to play their dominant strategies.

**Why dominance matters:** A dominant strategy is your best choice no matter what — it eliminates the need to guess what the other player will do. If both players have dominant strategies, the Nash equilibrium is simply the cell where both dominant strategies intersect.

**Anti-pattern — ignoring dominance:** Players who do not check for dominance first waste effort reasoning about contingencies that do not apply. Always check dominance before best-response mapping.

---

### Step 3 — Eliminate Dominated and Never-Best-Response Strategies (Rule 3)

When no strategy is globally dominant, look for strategies to eliminate:

**Type A — Dominated strategy:** Strategy A is dominated by strategy B if B gives a higher payoff than A regardless of what the opponent does. A dominated strategy will never be played by a rational player; eliminate it.

**Type B — Never-best-response strategy:** A strategy that is never the best response to any opponent strategy — even if it is not dominated. Eliminate it; no rational player will use a strategy that is never the best they can do.

**Successive elimination:** After eliminating a strategy, re-examine the reduced game. Strategies that were not dominated in the original game may become dominated once other strategies are removed. Repeat until no further elimination is possible.

**Why this helps:** Successive elimination reduces a large, complex matrix to a smaller, tractable one. In some games it narrows the outcome to a single cell — finding the Nash equilibrium without explicitly checking all mutual best responses.

**Example — 5x5 pricing game reduced to 3x3:**
If prices of $42 and $38 are never best responses to any rival price, eliminate them. In the remaining 3x3 game, a dominant strategy of $40 may emerge for both firms, identifying the Nash equilibrium directly.

**Stopping rule:** If successive elimination produces a unique outcome, that is the Nash equilibrium. If it produces a smaller game but not a unique outcome, proceed to Step 4.

---

### Step 4 — Map Best Responses and Find Nash Equilibria (Rule 4)

A **best response** is the strategy that maximizes your payoff given a specific belief about what your opponent will do.

**How to find best responses:**
1. Fix one player's strategy (e.g., assume Rival plays Low).
2. For the other player, find which strategy produces the highest payoff given that assumption. Mark it (bold, underline, or highlight).
3. Repeat for every possible fixed strategy of the opponent.
4. Swap roles and repeat for the other player.

**Identify Nash equilibria:** A Nash equilibrium is any cell where **both** players' payoffs are marked as best responses. In such a cell, each player is already doing the best they can given the other's choice — neither has any incentive to deviate unilaterally.

**Definition check:** A configuration of strategies is a Nash equilibrium if and only if:
- Each player is choosing a best response to what they believe the other players are doing, AND
- Those beliefs are correct (each player is actually doing what the other expects)

**Why Nash equilibrium is the right solution concept:** Any outcome that is not a Nash equilibrium has at least one player who could improve by switching. That player has an incentive to deviate, making the outcome unstable. Nash equilibrium is the resting point of rational strategic reasoning.

**Multiple equilibria:** Games often have more than one Nash equilibrium. When this occurs, proceed to Step 5 (if zero-sum, compute mixing) or Step 6 (coordination games, use focal-point analysis).

---

### Step 5 — Calculate Mixed Strategy Proportions (Rule 5)

When there is no Nash equilibrium in pure strategies — that is, when best-response arrows cycle (L beats R, R beats L, L beats R...) — the equilibrium exists in **mixed strategies**: deliberate randomization over pure strategies.

**Why mixing is necessary:** In zero-sum (pure conflict) games, any predictable pure strategy can be exploited. A penalty kicker who always shoots left will face a goalie who always covers left. Randomization removes exploitability by making the opponent indifferent between their choices.

**The indifference principle (Rule 5):** Choose your mixing proportions so that your opponent gets the same expected payoff from any of their pure strategies. When your opponent is indifferent, they cannot exploit you by choosing one strategy over another.

**Two-strategy formula:**

For a 2x2 game where row player mixes strategy A (probability p) and strategy B (probability 1-p):

Set the column player's expected payoff from their Left strategy equal to their expected payoff from their Right strategy:

```
payoff(column Left | row A) × p + payoff(column Left | row B) × (1-p)
= payoff(column Right | row A) × p + payoff(column Right | row B) × (1-p)
```

Solve for p. This is the row player's equilibrium mixing proportion.

**Worked example — Penalty kick (kicker payoffs, goalie minimizes):**

|  | Goalie: Left | Goalie: Right |
|---|---|---|
| **Kicker: Left** | 58 | 95 |
| **Kicker: Right** | 93 | 70 |

To find the kicker's equilibrium mix (proportion p = Left):
- Against goalie's Left: 58p + 93(1-p) = 93 - 35p
- Against goalie's Right: 95p + 70(1-p) = 70 + 25p
- Set equal: 93 - 35p = 70 + 25p → 23 = 60p → p = 23/60 ≈ 0.383

Kicker should kick Left 38.3% of the time, Right 61.7%.

To find the goalie's equilibrium mix (proportion y = Left):
- Against kicker's Left: 58y + 95(1-y) = 95 - 37y
- Against kicker's Right: 93y + 70(1-y) = 70 + 23y
- Set equal: 95 - 37y = 70 + 23y → 25 = 60y → y = 25/60 ≈ 0.417

Goalie should cover Left 41.7% of the time, Right 58.3%.

**Three-strategy system of equations:**

For a 3-strategy zero-sum game, let player mix with probabilities p (strategy 1), q (strategy 2), (1-p-q) (strategy 3). Compute the opponent's expected payoff for each of their three strategies. Set all three equal (indifference across all three). Solve the system of two equations (the third is redundant since probabilities sum to 1).

**Graphical method (minimax V-shape):** Plot the row player's mixture proportion (x) on the horizontal axis. For each column player pure strategy, draw a line showing the row player's payoff against that pure strategy. The upper envelope (the maximum of these lines) forms an inverted-V shape. The kicker's best mixture is at the apex — the proportion that maximizes the minimum payoff. This is the maximin point, equal to the minimax by von Neumann's theorem.

**Critical constraint — only for zero-sum games:** Rule 5 (mix to make opponent indifferent) applies to zero-sum or pure-conflict games. In coordination games (where interests overlap), mixing produces the worst expected outcome — players get trapped in miscoordinated outcomes more often than the pure strategy equilibria. Never randomize independently in coordination games.

**Why your mix is determined by opponent's payoffs:** In a non-zero-sum game with a mixed equilibrium, your equilibrium mixture is calculated to keep your opponent indifferent — so it depends on your opponent's payoffs, not your own. Counterintuitively, if your own payoffs change, your equilibrium mixture is unaffected; only your opponent's equilibrium mixture changes.

---

### Step 6 — Handle Multiple Equilibria with Focal-Point Analysis

When a game has multiple Nash equilibria (common in coordination games), Nash equilibrium theory alone does not select among them. Use focal-point analysis.

**Definition:** A focal point (Schelling point) is an equilibrium that is "obvious" to all players without communication — because of mathematical salience, cultural convention, symmetry, precedent, or shared experience.

**Focal-point sources — check in order:**
1. **Mathematical salience:** Is one equilibrium uniquely simple? (Equal split = focal. Round numbers = focal. First in a ranked list = focal.)
2. **Cultural or historical convention:** Do the players share a background that makes one option stand out? (Geographic division, industry norms, social customs.)
3. **Symmetry or fairness:** Does one equilibrium treat players symmetrically? Equal splits are focal partly because of their fairness appearance.
4. **Prior interaction:** Have these players coordinated before? The outcome of past play is often the focal point for future play.
5. **Communication:** If players can talk before choosing, use that channel — any agreement, even a vague one, can create a focal point.

**When no focal point exists:** If players lack shared context to converge expectations, equilibrium selection may fail. This is a genuine limitation — Nash equilibrium predicts what will happen only when beliefs converge. Multiple equilibria without a focal point is a coordination failure risk, not an analytic error.

**Conflict games with multiple equilibria (Battle of Sexes, Chicken):** When players have different preferences over the multiple equilibria (unlike pure coordination games), the equilibrium selection problem is harder. Options:
- Pre-commitment: one player credibly binds themselves to their preferred equilibrium (covered in commitment skills)
- Alternation over repeated plays: agree to rotate between equilibria
- Third-party coordination: use an external signal both players observe to coordinate

---

## Output

Deliver the following in writing:

1. **Payoff matrix** — formatted table showing all strategy combinations and payoffs
2. **Equilibrium identification** — which cells are Nash equilibria, with the best-response markings shown
3. **Analysis path taken** — which rules applied (dominance, elimination, best-response, mixing)
4. **Mixing proportions** (if applicable) — exact fractions/percentages with the indifference calculation shown
5. **Strategy recommendation** — which equilibrium to target and why, including focal-point reasoning if multiple equilibria exist
6. **Anti-patterns flagged** — if the situation is a coordination game, warn against uncoordinated mixing

---

## Key Principles

**Nash equilibrium is a self-consistent belief system:** Each player chooses the best action given correct beliefs about others. Any outcome where at least one player could improve by switching is unstable.

**Every finite game has at least one Nash equilibrium** — possibly in mixed strategies. The only games without equilibria are exotic theoretical constructs.

**Mixing purpose:** Mix to prevent exploitation, not to be unpredictable for its own sake. The correct mix is the one that makes your opponent indifferent — calculated from their payoffs, not your preferences.

**Do not mix in coordination games:** When interests overlap and there are multiple pure-strategy equilibria, mixing independently leads to miscoordination. Use focal points or explicit coordination instead.

**Improving your weakness changes the equilibrium mix:** In a zero-sum game, if you improve your performance in one option, your opponent uses that option less in their mix — and you use it less too. The value of improving a weakness is that you do not have to use it as often; the opponent can no longer exploit it as easily.

---

## Examples

### Example 1 — Pricing game (unique pure equilibrium via successive elimination)

**Situation:** Two retailers are setting prices simultaneously in a range of $38–$42.

**Analysis:**
1. Build 5×5 payoff matrix
2. $42 is dominated by $41 for both firms (higher profit regardless of rival's price); eliminate
3. $38 is dominated by $39; eliminate
4. In the resulting 3×3 game, $40 is dominant for both firms
5. **Nash equilibrium:** Both price at $40 (40,000 profit each)

**Insight:** The $40 equilibrium is less profitable than the collusion price ($80 = 72,000 each), but neither firm can unilaterally raise price without losing customers. The equilibrium is stable even if both wish for a different outcome.

### Example 2 — Penalty kick (no pure equilibrium, mixed strategy required)

**Situation:** Kicker vs. goalie, simultaneous choice of Left/Right. Payoffs (kicker success %):

|  | Goalie: Left | Goalie: Right |
|---|---|---|
| **Kicker: Left** | 58 | 95 |
| **Kicker: Right** | 93 | 70 |

**Analysis:**
1. No pure equilibrium — best-response arrows cycle
2. Rule 5 applies (zero-sum game)
3. Kicker indifference equation → p = 38.3% Left, 61.7% Right
4. Goalie indifference equation → y = 41.7% Left, 58.3% Right
5. Equilibrium success rate: 79.6% (minimax = maximin by von Neumann's theorem)

**Recommendation:** Kicker randomizes Left 38.3% using an objective device (page numbers, watch second hand). Goalie randomizes Left 41.7%. Any predictable pattern invites exploitation.

### Example 3 — Coordination game with multiple equilibria (focal-point selection)

**Situation:** Two division managers must independently choose which cloud platform to deploy on (AWS or Azure). Payoffs: both benefit equally from coordinating (3 each), neither benefits from mismatching (0 each). Two Nash equilibria: (AWS, AWS) and (Azure, Azure).

**Analysis:**
1. Both equilibria are Nash — each is a mutual best response
2. No dominant strategy; game is pure coordination
3. **Do not mix** — independent randomization at 50/50 produces miscoordination 50% of the time, yielding expected payoff 1.5 < 3
4. Focal-point check: Does the company already use one platform? Is there an industry default? Is one option mathematically simpler? → Use whichever has the strongest salience as the focal point
5. If no focal point exists, establish one through explicit pre-game communication

---

## References

Detailed worked calculations and additional examples are in:
- `references/mixed-strategy-calculation.md` — Full algebraic and graphical walkthrough of 2×2 and 3×3 mixed strategy problems
- `references/game-type-classifier.md` — How to distinguish zero-sum, coordination, and mixed-motive games
- `references/focal-point-examples.md` — Schelling's classic examples and modern applications

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Art of Strategy: A Game Theorist's Guide to Success in Business and Life by Avinash K. Dixit, Barry J. Nalebuff.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
