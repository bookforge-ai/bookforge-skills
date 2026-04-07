---
name: backward-reasoning-game-solver
description: "Solve sequential-move strategic games using backward induction. Use this skill when a user faces a multi-stage decision or negotiation where players alternate moves and each person's best action depends on what others will do later. Triggers include: user needs to determine the optimal opening move in a turn-based game or negotiation; user wants to know whether they can guarantee a win or favorable outcome before the game starts; user must sequence two risky actions and does not know which to attempt first; user is analyzing a multi-stage political, business, or competitive scenario where one party moves, the other responds, and so on; user has a finite-horizon sequential game with known player preferences and needs the game-theoretic solution; user suspects their opponent can anticipate their moves and wants to reason from end-states backward to their first action; user is building a game tree and needs to prune it to find dominant paths; user has a combinatorial takeaway game (like Nim variants) and wants the winning-position formula; user needs to understand why more flexibility or options can paradoxically hurt a player in a sequential game. This skill handles perfect-information, finite, sequential-move games. It does NOT cover simultaneous-move games (use a separate Nash equilibrium skill), incomplete-information games, or infinite-horizon repeated games."
version: 1
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [2]
tags: [game-theory, strategy, decision-making, sequential-games, backward-induction]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of the sequential game: players, sequence of moves, available actions at each decision point, and payoffs or preferences at terminal outcomes"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes the game situation in text or structured form"
discovery:
  goal: "Identify the game-theoretically optimal strategy for any sequential-move game by constructing a game tree and applying backward induction; deliver the opening move, the full contingent strategy, and the predicted outcome"
  tasks:
    - "Classify the interaction as sequential vs. simultaneous and confirm backward induction applies"
    - "Elicit the complete game structure: players, move order, actions at each node, and terminal payoffs or preference rankings"
    - "Construct or describe the game tree with nodes, branches, and terminal payoffs"
    - "Apply the backward induction procedure: start at terminal nodes, fold optimal choices back to the root"
    - "Identify winning positions vs. losing positions for combinatorial games using the k+1 formula where applicable"
    - "Determine risk sequencing: if multiple risky actions are needed, recommend attempting the harder one first while fallback options remain"
    - "Flag applicability limits: check for uncertainty about player motives, hidden information, or simultaneous moves that would require different tools"
    - "Deliver: optimal first move, full contingent strategy, predicted equilibrium outcome, and key reasoning"
  audience: "Strategists, negotiators, managers, game designers, analysts, and decision-makers facing any turn-based strategic interaction"
  when_to_use:
    - "User needs to solve a turn-based game or sequential negotiation"
    - "User must choose between attempting a risky action now vs. later and wants to know which sequence is optimal"
    - "User is designing rules for a competition and wants to predict outcomes before play begins"
    - "User faces a multi-stage business or political scenario where each party observes the other's move before responding"
    - "User wants to know if their current position in a game is a guaranteed win or guaranteed loss"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Backward Reasoning Game Solver

## When to Use

Use this skill for any strategic interaction where players move one at a time, each player can observe what the previous player did, and the game ends in a finite number of moves.

The core principle: **Rule 1 — Look forward and reason backward.** Anticipate where your initial decisions will ultimately lead and use that information to calculate your best current choice. This rule applies whether the game lasts two moves or two hundred.

The key insight backward reasoning delivers: a future action that "lies in the future does not mean it is uncertain." If you can deduce what a rational opponent will choose at a later node — because you know their preferences — you can treat that future action as a known fact today when computing your own best move now.

**This skill applies when all of the following hold:**

- Players move in sequence (not simultaneously)
- Earlier moves are observable before the next player responds
- The game ends in a finite number of moves
- Preferences or payoffs at each terminal outcome are known or can be reasonably estimated

**This skill does NOT apply to:**

- Simultaneous-move games (rock-paper-scissors, sealed-bid auctions, price-setting)
- Games with hidden information or private cards
- Infinite-horizon repeated interactions where reputation effects dominate
- Situations with deep uncertainty about opponents' objectives (estimate preferences first, then apply)

---

## Context and Input Gathering

### Required (ask if missing)

- **Players and move order:** Who moves first, second, etc.? Does the sequence alternate, or does one player move multiple times in a row?
  -> Ask: "Walk me through who acts and in what order."

- **Actions at each decision point:** What choices does the player-to-move have at each node?
  -> Ask: "At each turn, what are the available actions?"

- **Terminal payoffs or preference rankings:** What does each player receive or prefer at each possible end-state?
  -> Ask: "At each possible ending, how do you rank the outcomes? Best to worst is enough if exact numbers are unavailable."

- **Applicability check:** Is this sequential (players observe each other's moves before responding)?
  -> Ask: "Does each player see what the other did before choosing their own move?"

### Useful (gather if present)

- The number of total moves or stages (needed to apply the k+1 formula for combinatorial games)
- Whether a player needs their opponent to believe a threat is credible (signals a commitment/credibility issue that modifies pure backward reasoning)
- Whether the game is repeated (a one-time game vs. an ongoing relationship changes payoffs)

---

## Execution

### Step 1 — Classify the Game Type

**Why:** Backward induction is the correct tool only for sequential games with observable moves. Applying it to simultaneous games produces wrong answers. Spending thirty seconds on classification prevents wasted analysis.

**1a. Is it sequential or simultaneous?**

- Sequential: players observe previous moves before choosing. Backward induction applies.
- Simultaneous: players choose without seeing each other's current action. Use Nash equilibrium (different skill).
- Mixed: some stages are simultaneous, others sequential. Apply backward induction only to the sequential stages; treat simultaneous sub-games separately.

**1b. Is information perfect?**

- Perfect information: all previous moves are known to all players (chess, 21-flags, most negotiation sequences). Full backward induction works.
- Imperfect information: some moves are hidden (card games). Backward induction must incorporate probabilistic beliefs. Flag this and proceed with stated assumptions.

**1c. Is it finite?**

- Finite: the game ends within a known or bounded number of moves. Backward induction is exact.
- Potentially infinite: note limitations; backward induction gives a partial solution (start from whatever end condition you can identify).

---

### Step 2 — Construct the Game Tree

**Why:** The game tree is the visual logic of the game. It makes the sequence of decisions explicit and prevents the common error of optimizing the first branch without considering what happens downstream. A game tree and a decision tree differ in one critical way: at decision-tree nodes only one person chooses; at game-tree nodes, different players may choose at different nodes, each optimizing for their own preferences.

**Structure of a game tree:**

- **Root node:** The first decision point. Label it with the player who moves.
- **Branch:** Each available action at a node. Label branches with the action name.
- **Internal nodes:** Every subsequent decision point. Label with the player who moves there.
- **Terminal nodes (leaves):** End-states. Attach the payoffs or preference rankings for each player.

**Construction procedure:**

1. Start at the root. Draw one branch per available action.
2. For each branch, identify whether the game ends or another player chooses next. If it ends, attach payoffs. If not, draw a new node labeled with the next player.
3. Repeat until all paths reach terminal nodes.
4. If the tree is too large to draw fully, describe it verbally node by node or use the k+1 formula shortcut for combinatorial games (Step 4).

**Critical rule:** Even if you know that certain branches will never be reached (because a player will not rationally choose them), you must still resolve what each player *would* do at every conceivable node. The reason: a player at an earlier node makes choices based on what the other player would do *if* that branch were taken. Pruning a branch without resolving it first is a mistake.

---

### Step 3 — Apply Backward Induction

**Why:** Forward reasoning — picking the branch that looks best at the first move — fails because it ignores what rational opponents will do in response. The correct procedure is the reverse: start at the end, where outcomes are fully known, and fold optimal decisions back toward the start. This converts every future branch into a known consequence, making the first move's true value calculable.

**Backward induction procedure (step by step):**

1. **Identify all terminal nodes.** These have definite payoffs. No decision is needed here.

2. **Move one step back.** Find every internal node whose branches all lead directly to terminal nodes. These are the "penultimate" nodes — the last decision points in the game.

3. **At each penultimate node, find the optimal action for the player who moves there.** Optimal = the action leading to the terminal node with the best payoff for *that player* (not you, not the other side — the player who moves at that node). Mark this branch as the selected path (thicken it or mark with an arrow).

4. **Replace the penultimate node with its outcome.** Now treat that node as if it were a terminal node whose payoff is whatever the selected branch leads to. The subtree below it is resolved.

5. **Repeat steps 2-4, moving one level back each time,** until you reach the root node.

6. **At the root, the optimal action is determined.** The full path of selected branches from root to terminal is the predicted equilibrium path.

**Worked illustration (Charlie Brown / Fredo Investment):**

The same tree structure covers both cases:
```
Player A
├── Action 1 → Player B
│              ├── B's preferred action → Outcome: [A: bad, B: good]
│              └── B's other action   → Outcome: [A: good, B: okay]
└── Action 2 → Outcome: [A: neutral, B: neutral]
```
Backward induction at B's node: B prefers "B's preferred action." Fold back: if A takes Action 1, the realized outcome is [A: bad, B: good]. Compare to Action 2: [A: neutral]. A prefers neutral to bad → A takes Action 2. Equilibrium: Action 2 without ever reaching B's node.

**Common error to avoid:** Do not prune B's node without resolving it. A must compute what B would do if reached — even if A ends up not taking that branch.

---

### Step 4 — Combinatorial Game Shortcut (Winning-Position Formula)

**Why:** For games where players alternately remove objects from a pile (or similar combinatorial structures), drawing the full tree is impractical for large games. The pattern in the terminal logic propagates backward into a closed-form formula that immediately identifies winning and losing positions.

**The k+1 formula:**

In a game where each player may take 1 to k objects per turn, and the player who takes the last object wins:

- **Losing positions:** multiples of (k + 1). A player facing a multiple of (k+1) cannot win against a perfect opponent.
- **Winning positions:** any other count. The correct move is to take enough objects to leave the opponent at the nearest multiple of (k+1).

**21-flags example (k=3, so k+1=4):**
- Losing positions: 4, 8, 12, 16, 20
- Winning first move: take 1, leaving opponent with 20 (a multiple of 4)
- Opponent takes n (1, 2, or 3); you take 4-n; the count drops to 16, 12, 8, 4, then 0

**The "hot potato" variant (player who takes last loses):**
The same formula applies but the parity flips: losing positions are still multiples of (k+1), but now the positions are interpreted in reverse — check whether facing a multiple means you are forced to take the last item.

**Generalizing:** Any time a combinatorial game has a cycle length derivable from the rules, apply backward induction to the smallest cases (1, 2, 3, ... objects) to identify the pattern, then project it forward.

---

### Step 5 — Risk Sequencing: Attempt Riskier Actions First

**Why:** When a player needs multiple unlikely successes to reach a goal, and can attempt them in any order, the correct sequence is to attempt the *harder or riskier action first while fallback options remain open*. Attempting the easier action first and failing the harder one second results in a forced loss that the reversed sequence would have avoided.

**The Orange Bowl principle (Dixit and Nalebuff):**

Nebraska needed two touchdowns plus net extra points to win. The coach kicked the safe one-point conversion after the first touchdown. When the second touchdown was scored, he was forced to attempt the two-point conversion with no margin. The correct strategy: attempt the two-point conversion first. If it succeeds, the subsequent one-point kick covers the margin. If it fails, there is still a chance to tie via the one-point kick after the second touchdown. Attempting the risky action first keeps more options alive.

**Generalizable rule:** If you need both A (risky, ~50%) and B (safe, ~90%), and either order is feasible:
- Order B→A: if B succeeds but A fails → lose. No recovery.
- Order A→B: if A fails → still alive for the tie/partial win via B. If A succeeds → B is insurance.

Attempt the riskier action first. This applies to: new product launches before marketing commitments are locked in, career pivots before exhausting current options, negotiation concessions where the harder ask should come before the easier one is spent.

---

### Step 6 — Check Applicability Limits

**Why:** Backward induction gives the correct answer only given its assumptions. Violating those assumptions without acknowledging it produces overconfident, wrong predictions. Identifying limits is part of delivering a sound analysis.

**Three conditions that limit backward induction:**

1. **Natural uncertainty (chance nodes):** Some nodes are resolved by probability (a die roll, a market shock), not a player's decision. Incorporate expected values at chance nodes using the same backward induction structure. Note that the result is now a probabilistic expectation, not a guaranteed outcome.

2. **Unknown opponent objectives:** Backward induction requires predicting what the opponent will choose, which requires knowing their preferences. If you are uncertain, you must estimate. The result is a conditional recommendation: "If your opponent values X more than Y, then your best move is Z." If opponent motives are deeply uncertain, behavioral game theory (incorporating altruism, fairness, reputation) supplements the pure analysis.

3. **Strategic uncertainty in simultaneous sub-games:** If any stage involves players choosing simultaneously, that stage requires Nash equilibrium analysis. Solve the simultaneous sub-game first, substitute its equilibrium payoffs into the larger game tree, then continue backward induction.

**Paradox of expanded options:** More choices or greater freedom can hurt a player in a sequential game. Adding options to one player (like a presidential line-item veto) changes what the other player anticipates and may cause the other player to respond in a way that leaves the first player worse off. Backward induction reveals these paradoxes; intuition does not.

---

### Step 7 — Deliver the Solution

Structure your output as:

**Optimal opening move:** [Specific action for the first player, stated plainly]

**Full contingent strategy:** [Complete if-then plan: "If opponent does X, do Y; if opponent does Z, do W"]

**Predicted equilibrium outcome:** [The terminal state that backward induction leads to, and each player's payoff there]

**Key reasoning:** [The one or two backward induction steps that most determine the outcome — the nodes where the game is effectively decided]

**Applicability notes:** [Any assumptions made about opponent preferences or probability estimates, and how violations would change the answer]

---

## Key Principles

**Rule 1 is the foundation.** Look forward and reason backward. All other steps implement this rule.

**Future actions are predictable, not uncertain.** In a sequential game, a rational opponent's future choice follows from their preferences — it is deducible, not random. Treating predictable future actions as "uncertain" is hope over analysis.

**Resolve every node, even unreachable ones.** A player at node A chooses based on what would happen at node B *if* A chose to go there. If node B is unresolved, node A cannot be correctly decided.

**Game trees and decision trees differ in kind.** A decision tree has one optimizer throughout. A game tree has multiple optimizers, each at their own nodes, each optimizing for themselves. Do not collapse a game tree into a single-optimizer problem.

**More options can hurt.** In sequential games, gaining additional choices can signal different intentions to opponents and cause their responses to shift unfavorably. Backward reasoning reveals this paradox; forward intuition misses it.

**Attempt risky actions while fallback options remain.** Risk sequencing is a corollary of backward induction: work backward from what you need to achieve, and structure the order of attempts so that failure of the hardest step leaves the most options open.

**The first-mover advantage is derivable, not assumed.** Whether moving first helps or hurts depends entirely on the structure of the game tree — backward induction tells you which.

---

## Examples

### Example 1: The 21-Flags Game (Survivor: Thailand)

**Setup:** 21 flags; players alternate; each turn take 1, 2, or 3; player who takes the last flag(s) wins.

**Apply k+1 formula (k=3, so k+1=4):**
- Losing positions: 4, 8, 12, 16, 20
- First player wins by taking 1, leaving opponent with 20

**Full contingent strategy for first player:** Take 1. Whatever opponent takes (n), take 4-n. After your turn the count is always a multiple of 4. Opponent is trapped.

**Why Sook Jai lost:** They took 2 on the opening move, leaving 19 — not a multiple of 4. This handed the initiative to Chuay Gahn. The tribe needed to reason all the way back to the opening move; recognizing the 4-flag trap mid-game is too late.

---

### Example 2: The Fredo Investment Game

**Setup:** Charlie considers investing $100K with Fredo. If Charlie invests, Fredo can honor the contract (Charlie nets $150K, Fredo nets $250K) or abscond (Charlie loses $100K, Fredo keeps $500K). If Charlie does not invest, both get $0.

**Game tree:**
```
Charlie
├── Invest → Fredo
│             ├── Abscond → [Charlie: -$100K, Fredo: +$500K]
│             └── Honor   → [Charlie: +$150K, Fredo: +$250K]
└── Don't  → [Charlie: $0, Fredo: $0]
```

**Backward induction at Fredo's node:** Fredo prefers $500K over $250K → will Abscond.

**Fold back:** If Charlie invests, realized outcome is [Charlie: -$100K]. Compare to Don't: [Charlie: $0]. Charlie prefers $0 → Don't invest.

**Equilibrium:** No investment; both get $0. The mutually beneficial outcome ($150K/$250K) is blocked by the inability to commit credibly.

**Caveat:** This changes if the game is repeated or if Fredo has other US-dependent business interests — these create an ongoing game with reputation effects that can sustain cooperation.

---

### Example 3: The Orange Bowl Risk Sequencing

**Setup:** Nebraska needs 2 extra points net across two touchdowns. Option A: two-point conversion attempt (~50% success). Option B: one-point kick (~95% success). Osborne's order: B then A. Alternative: A then B.

**Backward induction on Osborne's order (B first):**
- If B succeeds and A succeeds → win (needed outcome)
- If B succeeds and A fails → lose (no recovery)
- If B fails and A succeeds → tie (acceptable)
- If B fails and A fails → lose

**Backward induction on alternative order (A first):**
- If A succeeds and B succeeds → win
- If A succeeds and B fails → still ahead; other outcomes now favorable
- If A fails → still score second touchdown; one-point kick gives tie (acceptable)
- If A fails and score another: now need exactly 2 points — same situation as Osborne faced but with a remaining chance

**Key insight:** The only scenario where order matters is when exactly one attempt fails. If A fails first, the fallback (B on the second touchdown) still yields a tie. If B fails first (Osborne's plan), the second touchdown forces a must-make two-pointer with no margin. Attempt the risky action first.

---

## References

- `references/game-tree-construction.md` — Detailed node-labeling conventions, tree notation for complex games, handling chance nodes
- `references/combinatorial-game-formulas.md` — k+1 formula derivations, hot-potato variants, multi-pile Nim, worked tables for games up to 100 objects
- `references/applicability-checklist.md` — Diagnostic questions for classifying a game (sequential vs. simultaneous, perfect vs. imperfect information, finite vs. infinite)
- `references/risk-sequencing-patterns.md` — Generalization of the Orange Bowl principle to business, negotiation, and career scenarios; worked examples with probability trees
