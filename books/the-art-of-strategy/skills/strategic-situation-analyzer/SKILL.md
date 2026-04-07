---
name: strategic-situation-analyzer
description: "Classify any strategic situation and route to the right game-theory skill. Use this skill whenever a user describes any situation involving multiple decision-makers whose outcomes depend on each other's choices. Triggers include: user says 'I'm not sure how to think about this strategically'; user faces a competitive or cooperative decision and doesn't know where to start; user asks which game theory concept applies to their situation; user describes a negotiation, competition, auction, vote, or incentive design problem and wants to know the right framework; user asks 'is this a prisoners' dilemma?'; user wants to understand whether their situation calls for cooperation or competition; user has a business, political, or personal strategic dilemma and needs a diagnostic before diving into analysis; user says 'what kind of game am I playing?'; user describes any interaction where their best action depends on what others will do; user is unsure whether to look for dominant strategies, equilibria, or use backward reasoning; user needs to decide whether to move first or second; user wonders whether they should cooperate, compete, randomize, commit, signal, or negotiate. This is the ENTRY POINT skill for the entire Art of Strategy skill set. It diagnoses the game type and routes to the specialized skill best suited to the situation. It does NOT replace the specialized skills — it prepares the user to use them effectively."
version: 1
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [1, 4]
tags: [game-theory, strategy, decision-making, strategic-analysis, situation-classifier]
depends-on: [backward-reasoning-game-solver, nash-equilibrium-analyzer]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of the strategic situation: who is involved, what they can do, what they want, and how their choices interact"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes their strategic situation in text"
discovery:
  goal: "Identify the type of strategic game the user is in, classify it along the key structural dimensions (sequential vs. simultaneous, zero-sum vs. non-zero-sum, one-shot vs. repeated), name the game type if it matches a known pattern, and route to the correct specialized skill with targeted guidance"
  tasks:
    - "Elicit the game structure: players, moves, payoffs, information, and timing"
    - "Classify as sequential, simultaneous, or mixed"
    - "Classify as zero-sum or non-zero-sum"
    - "Identify one-shot vs. repeated interaction"
    - "Match to a named game type: prisoners' dilemma, chicken, coordination, battle of sexes, assurance/stag hunt, or other"
    - "Route to the appropriate specialized skill with a specific briefing on what to bring to it"
    - "Flag multiple applicable skills when the situation has more than one relevant dimension"
  audience: "Anyone facing a strategic situation and unsure which analytical tool to apply — managers, negotiators, policy designers, analysts, students, or individuals in personal strategic decisions"
  when_to_use:
    - "User is at the start of a strategic analysis and does not yet know which game-theory framework applies"
    - "User describes a situation and asks 'what kind of game is this?'"
    - "User wants to know whether to cooperate, compete, commit, signal, or negotiate"
    - "User needs a diagnostic before investing time in deeper game-theoretic analysis"
    - "User is unsure whether their situation is sequential, simultaneous, or mixed"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Strategic Situation Analyzer

## When to Use

Use this skill as the **starting point** for any strategic analysis. A game is a situation of strategic interdependence: the outcome of your choices depends on the choices of others acting purposefully. Before applying any specialized technique, you must know which kind of game you are in.

The five rules that govern all strategic games (from Dixit and Nalebuff's Part I Epilogue):

- **Rule 1:** Sequential games — look forward and reason backward (backward induction)
- **Rule 2:** Simultaneous games — check for dominant strategies first
- **Rule 3:** No dominant strategy — eliminate dominated strategies successively
- **Rule 4:** No dominant or dominated strategies — find Nash equilibrium (mutual best responses)
- **Rule 5:** Zero-sum game with no pure equilibrium — mix strategies randomly

This skill diagnoses which rules apply to your situation, names the game type, and routes you to the specialized skill that implements the right rule. It does NOT perform the deep analysis itself — the specialized skills do that. Think of this as triage: fast, accurate classification that saves the user from applying the wrong framework.

---

## Context and Input Gathering

### Required (ask if missing)

- **Players:** Who are the decision-makers? (Include silent players — a passive institution, a market, or a future version of yourself all count as players)
  -> Ask: "Who are the active decision-makers whose choices affect your outcome?"

- **Moves and timing:** Does each player choose before or after seeing the other's choice?
  -> Ask: "When you make your decision, do you already know what the other party has done — or are you choosing at the same time?"

- **Payoffs and interests:** Does one player's gain require another's loss, or can both benefit?
  -> Ask: "If you get what you want, does that necessarily hurt the other side, or could both of you end up better off?"

- **Time horizon:** Is this a one-time interaction or an ongoing relationship?
  -> Ask: "Will you interact with this person or organization again? How often?"

### Useful (gather if present)

- The specific domain (business negotiation, competitive bidding, collective decision, contract design, information asymmetry)
- Whether the user wants to change the rules of the game rather than play within them
- Whether trust, reputation, or credibility is at stake
- Whether there is a hidden-information component (one party knows something the other doesn't)

---

## Execution

### Step 1 — Identify the Players, Moves, and Payoffs

**Why:** Game theory requires knowing exactly who is playing, what they can do, and what they want. Without these three elements, any analysis is guesswork. The key insight from the Introduction: "The key lesson of game theory is to put yourself in the other player's shoes." You cannot do this without first knowing who the other players are and what motivates them.

**Three questions to answer:**

1. **Players:** List every decision-maker whose choices affect the outcome — including those who may seem passive. A regulator, a future customer, or your own future self (as in commitment problems) may be a player.

2. **Moves:** What actions are available to each player? Are these actions chosen once (one-shot) or repeatedly? Are there actions that change the rules of the game itself (commitments, threats, promises)?

3. **Payoffs:** What does each player ultimately care about? Be precise: a competitor may care about relative standing, not absolute profit. A negotiating counterpart may value fairness or face-saving alongside money.

**Output of this step:** A compact statement of the form: "There are [N] players: [names/roles]. [Player A] can [actions]. [Player B] can [actions]. [Player A] prefers [outcomes ranked]. [Player B] prefers [outcomes ranked]."

---

### Step 2 — Classify: Sequential vs. Simultaneous vs. Mixed

**Why:** This is the single most important structural distinction in game theory. Sequential and simultaneous games require completely different analytical tools. Applying backward induction to a simultaneous game or Nash equilibrium to a purely sequential game yields wrong answers.

**Decision rule:**

| Timing Structure | Definition | Analytical Tool |
|---|---|---|
| **Sequential** | Players move in turns; each player observes previous moves before choosing | Backward induction (Rule 1) |
| **Simultaneous** | Players choose at the same time, or without observing the other's current move | Dominant strategies → dominated strategy elimination → Nash equilibrium (Rules 2-4) |
| **Mixed** | Some stages are sequential, others simultaneous | Combine both tools: solve simultaneous sub-games with Nash equilibrium, substitute results into the sequential tree, then apply backward induction |

**Diagnostic questions:**
- "By the time you make your decision, will you know what the other party has already decided?" → If yes: sequential. If no: simultaneous.
- "Is there a first-mover advantage here?" → Likely sequential.
- "Would you want to go first or second?" → If the answer is obvious and asymmetric, this is likely sequential.
- "Does your best choice depend on what you *think* the other party will do simultaneously?" → Likely simultaneous.

**Football example (mixed game):** The offense and defense choose run/pass simultaneously (neither knows the other's call), but the play call game sits inside a larger sequential game of drive management and clock strategy. Both tools are required.

---

### Step 3 — Classify: Zero-Sum vs. Non-Zero-Sum

**Why:** This classification determines whether cooperation is even theoretically possible. In a zero-sum game, every gain for one player is an exact loss for another — there is no pie to expand, only to divide. In a non-zero-sum game, there are zones of mutual benefit or mutual harm that strategic choices can navigate. Treating a non-zero-sum game as zero-sum leaves value on the table. Treating a zero-sum game as non-zero-sum invites exploitation.

**Decision rule:**

| Payoff Structure | Definition | Implication |
|---|---|---|
| **Zero-sum** | One player's gain = another's loss. Total payoff is constant regardless of outcome. | Pure competition. No cooperative outcome exists. Mix strategies if no pure equilibrium. |
| **Non-zero-sum** | Players' interests partly conflict, partly align. Outcomes exist that are better (or worse) for all. | Cooperation may be possible. Look for jointly beneficial moves, and be alert to coordination failures and collective action problems. |

**Diagnostic questions:**
- "If the other party wins completely, do you lose exactly what they gain?" → Zero-sum.
- "Is there any outcome where both of you are better off than if you simply competed?" → Non-zero-sum.
- "Could you both lose simultaneously?" → Non-zero-sum (mutual loss is only possible when interests are not strictly opposed).

**Common error:** Many real-world situations that feel like competitions are actually non-zero-sum. Arms races, price wars, and litigation are non-zero-sum games where both parties can lose — which means cooperation-based resolutions may be available.

---

### Step 4 — Match to a Named Game Type

**Why:** Named game types are cognitive anchors. Recognizing that you are in a prisoners' dilemma immediately tells you the structure of the problem and the range of solutions. The ten tales in Chapter 1 illustrate that the same structural patterns appear across radically different domains — campaign finance, criminal interrogations, collective action problems, and corporate negotiations are all structurally identical.

**Game type reference:**

| Game Type | Structure | Signature | Example |
|---|---|---|---|
| **Prisoners' Dilemma** | Simultaneous, non-zero-sum. Each player has a dominant strategy that leads to mutual harm. Cooperation is individually irrational but collectively better. | "Both of us defect even though we'd both prefer to cooperate" | Price wars, arms races, campaign spending, confession under interrogation |
| **Chicken** | Simultaneous, non-zero-sum. Two players race toward a collision; the one who swerves loses face but avoids disaster. Both swerving is best collectively; neither swerving is catastrophic. | "Someone has to back down — but who?" | Nuclear brinkmanship, labor negotiations at impasse, road rage |
| **Coordination Game** | Simultaneous, non-zero-sum. Multiple equilibria exist; players just need to coordinate on the same one. Pure alignment of interest — both prefer the same equilibrium once selected. | "We both want to do the same thing, but which thing?" | Driving on the left vs. right, technology standards, meeting-point problems |
| **Battle of Sexes** | Simultaneous, non-zero-sum. Multiple equilibria; players prefer to coordinate but each prefers a different equilibrium. Conflict over which coordination point to reach. | "We both want to meet, but we each prefer our own venue" | Joint ventures with competing HQ preferences, co-authorship credit disputes |
| **Assurance / Stag Hunt** | Simultaneous, non-zero-sum. Cooperation pays off big if both cooperate, but defection is safe if uncertain about the other. Trust is the barrier. | "I'll cooperate if I can trust you will too" | Supply chain partnerships, open-source contributions, international environmental agreements |
| **Pure zero-sum / matching pennies** | Simultaneous, zero-sum. No pure Nash equilibrium; any predictable strategy is exploitable. Must randomize. | "Whatever I do, you have a counter" | Rock-paper-scissors, penalty kicks, IRS audit targeting |
| **Sequential commitment game** | Sequential, non-zero-sum. First mover can lock in advantage by credibly committing to a strategy before the other moves. | "If I can commit first, I win" | Market entry deterrence, collective bargaining postures, international negotiation |

**Matching procedure:**
1. Is it zero-sum? → If yes, skip to mixed-strategy logic or zero-sum sequential analysis.
2. Is it simultaneous? → Check payoff structure against the prisoners' dilemma, chicken, coordination, battle of sexes, and assurance patterns.
3. Is it sequential? → Determine if commitment or credibility is the key issue.
4. Does one party have private information the other lacks? → Flag information asymmetry as a separate dimension.

---

### Step 5 — Route to the Specialized Skill

**Why:** Each specialized skill in this set is optimized for one game type or strategic problem. Sending the user to the wrong skill wastes time and produces misdirected analysis. The routing table below maps the game classification to the correct skill, with specific guidance on what to bring to the skill.

**Routing table:**

| Situation | Primary Skill | What to bring to it |
|---|---|---|
| Sequential game — need the optimal opening move and full strategy | `backward-reasoning-game-solver` | Players, move order, actions at each node, terminal payoffs or preference rankings |
| Simultaneous game — need to find equilibrium or dominant strategies | `nash-equilibrium-analyzer` | Players, strategies available to each, payoff matrix or ranking of outcomes |
| Prisoners' dilemma — cooperation problem, repeated interaction | `prisoners-dilemma-resolver` | Whether the game is one-shot or repeated, who the players are, what defection and cooperation look like in this context |
| Information asymmetry — one party knows something the other doesn't | `information-asymmetry-strategist` | Who has private information, what actions they could take to signal or hide it, what the uninformed party could do to screen |
| Auction or competitive bidding | `auction-bidding-strategist` | Auction format (open/sealed), number of bidders, whether values are private or shared, your value estimate |
| Voting, collective decision, or agenda control | `voting-system-strategist` | Number of voters, voting rule, preference rankings of key voters, who controls the agenda |
| Need to change the game — commitment, threats, promises | `strategic-commitment-designer` | The current game structure, what commitment or threat is being considered, whether it is credible given the mover's incentives |
| Negotiation, bargaining, or deal-making | `negotiation-strategist` | Both parties' alternatives to agreement (BATNAs), the zone of possible agreement, what is being divided and what can be traded |
| Incentive design — principals, agents, moral hazard | `incentive-scheme-designer` | Who the principal and agent are, what actions the agent can take that the principal cannot observe, what the principal wants the agent to do |

**Multiple-skill situations:** Many real situations involve more than one dimension. Common combinations:
- Negotiation with information asymmetry → use `negotiation-strategist` + `information-asymmetry-strategist`
- Sequential game where the first move is a credible commitment → use `strategic-commitment-designer` first, then `backward-reasoning-game-solver`
- Prisoners' dilemma in a repeated relationship → use `prisoners-dilemma-resolver` (it handles both one-shot and repeated cases)
- Auction with information asymmetry (winner's curse) → use `auction-bidding-strategist` (it covers this directly)

---

### Step 6 — Deliver the Diagnosis and Routing

Structure your output as:

**Game classification:**
- Timing: [Sequential / Simultaneous / Mixed]
- Payoff structure: [Zero-sum / Non-zero-sum]
- Time horizon: [One-shot / Repeated]
- Named game type: [Prisoners' dilemma / Chicken / Coordination / Battle of sexes / Assurance / Zero-sum mixing / Sequential commitment / Other]

**Key structural insight:** [The one observation about this game's structure that most shapes the strategic options — e.g., "Both players have dominant strategies that lead to mutual harm, so this is a prisoners' dilemma; the solution must change the payoff structure or introduce repetition"]

**Primary skill to use:** [Skill name] — [One sentence on why this skill is the right one]

**What to bring to it:** [Specific inputs the next skill will need, drawn from what the user has already described]

**Secondary skills (if applicable):** [Any additional skills for dimensions of the situation not covered by the primary skill]

**One thing to watch for:** [The most common error or trap in this type of game, stated concisely]

---

## Key Principles

**Diagnosis before prescription.** Applying a technique before classifying the game type is a common and costly error. The prisoners' dilemma and a coordination game are both simultaneous non-zero-sum games, but their solutions are almost opposite. Classification is not overhead — it is the analysis.

**Put yourself in the other player's shoes.** The core discipline of game theory is modeling the other player accurately: what they know, what they want, and how they will reason. George Bernard Shaw's warning applies: do not treat others as you would want to be treated — their preferences may differ from yours.

**You may be playing a larger game.** The taxi story (Tale #10) illustrates that the immediate transaction may be embedded in a reputation game, a social game, or a future-interaction game. Always ask: what larger game does this interaction sit inside?

**The game type determines the solution, not vice versa.** Do not start with a preferred solution and fit the game type to it. Start with the game type (classification determines what solutions are even theoretically available) and then find the best solution within that type.

**Non-zero-sum games have traps that zero-sum thinking misses.** The prisoners' dilemma is dangerous precisely because it feels like pure competition while actually containing a cooperate-cooperate outcome that both players prefer. Treating it as zero-sum guarantees the bad equilibrium.

**You may not be playing the game you think you are.** Buffett's campaign finance dilemma (Tale #7) looks like a cooperation problem but is actually a clever prisoners' dilemma construction where supporting the bill is a dominant strategy for both parties. Re-examine the payoff structure before committing to any classification.

---

## The Ten Tales: Game Type Reference

Chapter 1 illustrates the breadth of strategic situations. Each tale maps to a game type:

| Tale | Domain | Game Type |
|---|---|---|
| #1: Pick a Number | Adversarial search | Sequential game of expectations; backward induction on predicted opponent behavior |
| #2: Winning by Losing | Survivor | Sequential game; backward reasoning from finale structure |
| #3: The Hot Hand | Sports/defense | Simultaneous mixed-strategy game; zero-sum between offense and defense |
| #4: To Lead or Not | Sailboat racing | Sequential commitment; copying strategy vs. innovation |
| #5: Here I Stand | Negotiation | Sequential commitment; credibility and intransigence as power |
| #6: Thinning Strategically | Self-commitment | Commitment game against your future self; removing options to gain credibility |
| #7: Buffett's Dilemma | Campaign finance | Prisoners' dilemma; dominant strategies leading to mutual harm |
| #8: Mix Your Plays | Rock Paper Scissors | Zero-sum simultaneous; no pure equilibrium, must randomize |
| #9: Never Give a Sucker an Even Bet | Auctions/betting | Information asymmetry; winner's curse |
| #10: Game Theory Can Be Dangerous | Negotiation/taxi | Bargaining; importance of modeling the other player's perspective and payoffs |

---

## References

- `references/game-type-field-guide.md` — Detailed criteria and worked examples for each named game type; disambiguation rules for borderline cases
- `references/five-rules-quick-reference.md` — One-page summary of the five rules from the Part I Epilogue with decision flow and tool mapping
- `references/situation-to-skill-routing-guide.md` — Extended routing logic including multi-skill combinations and common situational patterns
