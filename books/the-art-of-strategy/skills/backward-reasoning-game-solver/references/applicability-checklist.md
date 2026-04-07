# Applicability Checklist for Backward Induction

Use this checklist to determine whether backward induction is the correct tool, and if not, what adjustment or alternative to use.

---

## Step 1: Sequential vs. Simultaneous

**Question:** Do players observe each other's moves before choosing their own?

| Answer | Implication |
|---|---|
| Yes, all moves are observed before the next player responds | Fully sequential. Backward induction applies directly. |
| No, players choose simultaneously without observing the current action | Simultaneous game. Use Nash equilibrium analysis instead. |
| Mixed: some stages are sequential, some simultaneous | Apply backward induction to sequential stages. Solve simultaneous sub-games using Nash equilibrium and substitute equilibrium payoffs into the tree. |

---

## Step 2: Perfect vs. Imperfect Information

**Question:** Do players know all previous moves and the full state of the game at their decision point?

| Answer | Implication |
|---|---|
| Yes: all history is observable (chess, negotiation sequences, flag games) | Perfect information. Backward induction is exact. |
| No: some prior moves or private information is hidden (card games, some auctions) | Imperfect information. Backward induction requires probability estimates at hidden-information nodes. Results are conditional on beliefs. |
| Partially: some information is public, some private | Model public history as the tree structure; treat hidden information as opponent-type uncertainty. Use stated assumptions and sensitivity analysis. |

---

## Step 3: Finite vs. Potentially Infinite

**Question:** Does the game end within a bounded number of moves?

| Answer | Implication |
|---|---|
| Yes: game ends in a finite, known number of moves | Finite. Backward induction is exact and terminates. |
| Yes, but very large (chess-scale): finite in principle, infeasible in practice | Apply backward induction to the endgame (few pieces / final stages). Use heuristic evaluation for midgame positions. Combine game theory with domain expertise. |
| No: the game can repeat indefinitely | Backward induction does not directly apply. Consider: discounted payoffs, trigger strategies, reputation models for infinite-horizon games. |

---

## Step 4: Known vs. Unknown Preferences

**Question:** Do you know (or can you reasonably estimate) what each player prefers at each terminal outcome?

| Answer | Implication |
|---|---|
| Yes: preferences are clearly known (win > tie > loss; higher payoff > lower) | Full backward induction. |
| Approximately known: preferences can be ranked but not precisely measured | Backward induction with ordinal payoffs. Results are robust to small changes in rankings. |
| Uncertain: you do not know whether your opponent values outcome A over B | You cannot run backward induction without an assumption. Options: (1) try both preference orderings and deliver conditional recommendations; (2) ask for more context on opponent motives; (3) acknowledge uncertainty in the deliverable. |
| Opponent has non-standard preferences (altruism, fairness, spite) | Behavioral game theory adjustment. Incorporate fairness concerns as an additional payoff component (e.g., opponent prefers equal split over maximizing own take). |

---

## Step 5: One-Shot vs. Repeated

**Question:** Is this game played once or repeatedly between the same players?

| Answer | Implication |
|---|---|
| One-shot: single play with no future interaction | Pure backward induction. No reputation effects. Fredo-type defection is rational; Charlie should not invest. |
| Repeated with known end: finite repetitions | Backward induction applies to the repeated game. In many cases (e.g., finite prisoner's dilemma), cooperation unravels back to the one-shot outcome. |
| Repeated indefinitely or with unknown end | Reputation and reciprocity become relevant. The "shadow of the future" can sustain cooperation. Pure backward induction understates the range of sustainable outcomes. |

---

## Quick Classification Card

Run through this five-question sequence. The first "No" determines the tool.

1. Sequential moves? → If No: use Nash equilibrium
2. Observable history? → If No: use beliefs + backward induction (Bayesian)
3. Finite game? → If No: use repeated-game / reputation models
4. Known preferences? → If No: run conditional analysis or gather more information
5. One-shot? → If No: consider reputation effects as payoff additions

If all five answers are Yes: proceed with standard backward induction (Steps 2-7 of the main skill).

---

## The Paradox of More Options

A recurring finding from backward induction analysis: **giving a player more choices can make them worse off**.

This occurs when expanded options change the other player's anticipated responses. The example from Chapter 2: a presidential line-item veto appears to increase presidential power. But backward induction shows that Congress, anticipating the veto, changes the bills it passes in ways that leave both players worse off than under the no-veto regime.

Check for this paradox whenever:
- A player gains a new action or capability
- You are modeling how that change affects both players' strategies
- The outcome for the "empowered" player seems counterintuitively worse

The mechanism: more options at your node can signal or enable different things to opponents at earlier nodes, shifting their behavior before you even act.
