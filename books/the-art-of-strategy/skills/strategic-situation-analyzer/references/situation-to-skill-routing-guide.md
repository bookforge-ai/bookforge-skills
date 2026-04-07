# Situation-to-Skill Routing Guide

Extended routing logic for the `strategic-situation-analyzer` hub skill. Covers multi-skill combinations, common situational patterns, and disambiguation between skills with overlapping applicability.

---

## Single-Skill Routes

### Route A: Pure Sequential Game
**Trigger:** Moves alternate; each player observes the previous move; game ends in finite steps.
**Skill:** `backward-reasoning-game-solver`
**Inputs to prepare:**
- The complete sequence of who moves when
- Available actions at each decision point
- Terminal payoffs or preference rankings (ordinal is sufficient)
- Whether any stages involve simultaneous choices embedded in the sequence

**Watch for:** Natural uncertainty (chance nodes like weather, market outcomes) — treat these as probability-weighted branches, not opponent moves.

---

### Route B: Simultaneous Game — Finding Equilibrium
**Trigger:** Players choose without observing each other's current action; need to find the best strategy.
**Skill:** `nash-equilibrium-analyzer`
**Inputs to prepare:**
- List of strategies available to each player
- Payoff matrix: what each player gets for each combination of choices
- Whether the game is zero-sum or non-zero-sum
- Whether the game is one-shot or repeated (repeated changes the equilibrium significantly)

**Watch for:** Multiple equilibria — bring context on any focal points or conventions that might select between them.

---

### Route C: Cooperation Under Recurring Temptation
**Trigger:** Players face repeated prisoners' dilemma-type structure; each round they are tempted to defect but mutual cooperation would serve both better long-term.
**Skill:** `prisoners-dilemma-resolver`
**Inputs to prepare:**
- The payoff structure of the one-shot game (confirm it has the prisoners' dilemma signature)
- Whether the game is repeated and, if so, for how many rounds (known end vs. indefinite)
- The players' discount rates or patience (how much they value future payoffs vs. current ones)
- Whether communication is possible before each round

---

### Route D: Hidden Information Advantage/Disadvantage
**Trigger:** One party has private information the other lacks; the uninformed party must infer or screen; the informed party may want to signal or conceal.
**Skill:** `information-asymmetry-strategist`
**Inputs to prepare:**
- Who has private information and what kind (quality, intentions, costs)
- What actions the informed party can take that might reveal or conceal their type
- What actions the uninformed party could take to distinguish between types (screening mechanisms)
- Whether signaling is costly (costly signals are more credible)

---

### Route E: Competitive Bidding or Auction
**Trigger:** Multiple parties bid for a prize; the highest bid wins; bidders have private value estimates.
**Skill:** `auction-bidding-strategist`
**Inputs to prepare:**
- Auction format (English/ascending, Dutch/descending, first-price sealed bid, second-price/Vickrey)
- Number of competing bidders (approximately)
- Whether values are private (you know only your own value) or common (the prize has a single true value; everyone has imperfect signals about it)
- Your value estimate for the prize

**Watch for:** Winner's curse in common-value auctions — if winning means all others bid less than you, it likely means you overestimated value.

---

### Route F: Collective Decision or Voting
**Trigger:** A group must reach a collective decision through voting; agenda control or voting rule design is relevant.
**Skill:** `voting-system-strategist`
**Inputs to prepare:**
- The voting rule in use (majority, supermajority, sequential elimination, approval voting)
- The number of voters and key preference rankings
- Whether any player controls the agenda (what gets voted on and in what order)
- Whether the vote is one-shot or part of a multi-round process

---

### Route G: Changing the Structure of the Game
**Trigger:** The user does not want to play the current game optimally — they want to change it. Or they need to make a threat or promise credible before the game begins.
**Skill:** `strategic-commitment-designer`
**Inputs to prepare:**
- The current game structure and its equilibrium outcome
- What commitment, threat, or promise is being considered
- Whether the commitment is reversible (limits credibility) or irreversible (credible but costly)
- What the opponent's anticipated response to the commitment would be

---

### Route H: Negotiation or Bargaining
**Trigger:** Two or more parties are trying to reach a deal that creates joint value; the question is how to get to agreement and how the surplus is divided.
**Skill:** `negotiation-strategist`
**Inputs to prepare:**
- Each party's best alternative to a negotiated agreement (BATNA)
- The range of possible deals (zone of possible agreement)
- What is being divided and what can be traded across issues
- Time pressure: whether delay costs one party more than the other

---

### Route I: Incentive Design or Contract Structure
**Trigger:** A principal wants to induce an agent to take certain actions that the principal cannot directly observe or verify.
**Skill:** `incentive-scheme-designer`
**Inputs to prepare:**
- Who the principal and agent are; what the principal wants the agent to do
- What actions the agent can take that the principal cannot observe (the moral hazard dimension)
- What outcome metrics are observable and contractible
- Whether there is an adverse selection problem (the agent has private information before contracting) as well as a moral hazard problem

---

## Multi-Skill Combinations

### Combination 1: Sequential Commitment + Backward Reasoning
**When:** The user wants to make a first-mover commitment and then predict how the game unfolds from there.
**Order:** Use `strategic-commitment-designer` first to design the credible commitment. Then use `backward-reasoning-game-solver` with the modified game tree (where the commitment changes the first-mover's available actions or the opponent's anticipation).

---

### Combination 2: Negotiation + Information Asymmetry
**When:** A negotiation where one party has private information that affects the deal terms — typical in M&A, hiring, or supply contracts.
**Order:** Use `information-asymmetry-strategist` first to understand the signaling/screening dynamics (should you reveal your information? how do you interpret their signals?). Then use `negotiation-strategist` with the information structure clarified.

---

### Combination 3: Repeated Prisoners' Dilemma + Commitment
**When:** The players are in an ongoing prisoners' dilemma relationship and the user wants to change the equilibrium — either by changing payoffs (commitment) or by establishing a reciprocity norm (repeated game).
**Which to use first:** Depends on the user's goal.
- If the goal is to change the game's structure → `strategic-commitment-designer` (changes payoffs so cooperation becomes dominant)
- If the goal is to sustain cooperation within the existing structure → `prisoners-dilemma-resolver` (tit-for-tat, trigger strategies)

---

### Combination 4: Auction + Information Asymmetry
**When:** The user is bidding in an auction where other bidders may have better information about the true value of the prize (common-value auction with information asymmetry).
**Order:** Use `auction-bidding-strategist` directly — it covers the winner's curse and bid shading for common-value auctions as part of its core content.

---

### Combination 5: Voting + Strategic Commitment
**When:** The user controls the agenda and wants to sequence votes to achieve a preferred outcome.
**Order:** Use `voting-system-strategist` first (it covers agenda manipulation and strategic voting directly). Use `strategic-commitment-designer` if the key issue is pre-committing to a position before the vote to influence other voters' choices.

---

## Disambiguation: When Two Skills Seem Applicable

### Nash Equilibrium Analyzer vs. Backward Reasoning Game Solver
**Distinguishing question:** "By the time you make your decision, will you know what the other party has already chosen?"
- Yes → `backward-reasoning-game-solver` (sequential)
- No → `nash-equilibrium-analyzer` (simultaneous)

**Common confusion:** "I move first, so isn't this sequential?" — Not necessarily. If the second party chooses *without observing your move* (as in sealed-bid auctions), it is simultaneous even though you "moved first" in calendar time.

---

### Prisoners' Dilemma Resolver vs. Nash Equilibrium Analyzer
**Distinguishing question:** "Is the problem fundamentally about mutual defection in a repeated or structured relationship, or about finding the right strategy in a one-shot game?"
- Repeated relationship with cooperation breakdown → `prisoners-dilemma-resolver`
- One-shot equilibrium analysis → `nash-equilibrium-analyzer`

**Overlap:** The one-shot prisoners' dilemma can be solved by `nash-equilibrium-analyzer` (dominant strategy = defect; Nash equilibrium = both defect). Use `prisoners-dilemma-resolver` when the goal is to actually achieve cooperation despite the dominant-strategy trap.

---

### Strategic Commitment Designer vs. Negotiation Strategist
**Distinguishing question:** "Are you trying to change the rules before the game starts, or are you trying to navigate a bargaining process that is already underway?"
- Changing the game → `strategic-commitment-designer`
- Navigating bargaining → `negotiation-strategist`

**Overlap:** Commitment tactics (making threats credible, establishing BATNAs) are part of both skills. If the commitment is purely internal to the negotiation (not a structural change to the game), use `negotiation-strategist`.

---

## Situations That Don't Fit Cleanly

### "I'm not sure if my situation is a game at all"
A game requires **strategic interdependence**: your outcome depends on others' choices, and they know your outcome depends on their choices, and you know that they know, etc. If the other party is passive (a natural environment, a machine with fixed rules, a bureaucracy with no decision-maker), this is a decision problem, not a game. Standard optimization applies.

**Test:** "Does the other party adjust their behavior in response to what I do?" If no, this is not a game theory problem.

---

### "There are more than two players"
Game theory applies to n-player games, but the analysis is more complex. For this skill set:
- Voting and collective decisions → `voting-system-strategist` (designed for multi-player settings)
- Auctions with multiple bidders → `auction-bidding-strategist`
- Multi-player prisoners' dilemma / collective action → `prisoners-dilemma-resolver`
- Multi-player negotiations → `negotiation-strategist` (covers coalition dynamics)
- Multi-player simultaneous games → `nash-equilibrium-analyzer` (handles n players)

---

### "The other party doesn't behave rationally"
Game theory assumes rational players who maximize their payoffs. When players deviate from rationality (due to emotion, pride, status concerns, or cognitive bias), pure game-theoretic analysis may be wrong. Adjustments:
- Model the non-rational payoff directly: if the other party cares about face-saving, include that in their payoff function
- Use behavioral benchmarks: the ultimatum game shows real players reject unfair offers even at personal cost
- Build in slack: if you cannot predict whether the other party will behave rationally, choose strategies that perform reasonably well under both rational and non-rational opponent behavior

**Important note from Tale #10 (the taxi):** Pride, spite, and perceived dishonor can dominate monetary calculations. Always ask: "Is this person optimizing money, or optimizing something else?"
