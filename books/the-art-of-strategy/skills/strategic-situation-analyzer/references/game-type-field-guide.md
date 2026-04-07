# Game Type Field Guide

Detailed criteria, payoff structures, worked examples, and disambiguation rules for each named game type. Use this reference when the main skill's routing table leaves ambiguity.

---

## Prisoners' Dilemma

### Structure
- Simultaneous moves
- Non-zero-sum
- Each player has a **dominant strategy** (defect/compete) that makes them better off regardless of what the other does
- The dominant-strategy equilibrium is worse for both players than if both had chosen the cooperative option

### Payoff signature (ordinal ranking per player)
Defect while other cooperates > Both cooperate > Both defect > Cooperate while other defects

The key: "Both defect" is the equilibrium even though "both cooperate" is better for both. Individual rationality produces collective irrationality.

### Diagnostic test
Ask: "If you knew for certain the other party would cooperate, would you still be tempted to defect? And if you knew they would defect, would you be forced to defect too?" If yes to both: prisoners' dilemma.

### Examples from the Ten Tales
- Buffett's Dilemma (#7): Campaign finance. Each party's dominant strategy is to support the reform bill, regardless of what the other party does. Both support it → the billionaire's mechanism works for free.
- In Cold Blood (classic illustration): Both suspects defect (confess) even though mutual silence would serve both better.
- Collective action / belling the cat: Each individual free-rides even though collective action would benefit everyone.

### Common real-world instances
- Price wars: each firm cuts prices to gain share; both end up worse
- Arms races: each side builds weapons; both end up less secure at higher cost
- Advertising spending battles: mutually escalating spend with no change in market share
- Environmental non-compliance: each firm pollutes to save costs; industry faces regulation

### Solution routes
- **One-shot:** No escape within the game. Must redesign the game (change payoffs, add enforcement) → `strategic-commitment-designer`
- **Repeated, indefinite horizon:** Tit-for-tat or trigger strategies can sustain cooperation → `prisoners-dilemma-resolver`
- **Many players (collective action):** Coordination mechanisms, selective incentives, threshold dynamics → `prisoners-dilemma-resolver`

---

## Chicken (Hawk-Dove)

### Structure
- Simultaneous moves
- Non-zero-sum
- Two Nash equilibria in pure strategies: (You swerve, They don't) and (You don't, They swerve)
- A third equilibrium in mixed strategies exists
- The worst outcome for both is mutual non-swerving (collision/catastrophe)

### Payoff signature (ordinal ranking per player)
You don't swerve, they do > Both swerve > You swerve, they don't > Neither swerves (catastrophe)

### Diagnostic test
Ask: "Is there an outcome that would be catastrophic for both of us if neither backs down?" If yes: likely chicken. The key feature is mutual catastrophe at the extreme.

### Examples
- Nuclear brinkmanship: mutual destruction is worse than either side backing down
- Labor strike negotiations: protracted dispute damages both sides; one must concede
- Corporate acquisition battles: bidding wars can destroy value for the "winning" acquirer

### Disambiguation from prisoners' dilemma
In prisoners' dilemma, both players have the same dominant strategy (defect). In chicken, there is no dominant strategy — each player's best response depends on what the other does. If you expect the other to swerve, you should hold firm. If you expect the other to hold firm, you should swerve.

### Solution routes
- Creating credible commitment to not swerve forces the other side to swerve → `strategic-commitment-designer`
- Negotiating a coordinated solution before either commits → `negotiation-strategist`

---

## Coordination Game

### Structure
- Simultaneous moves
- Non-zero-sum
- Multiple Nash equilibria; players prefer to coordinate on the same one
- Interests are perfectly aligned once a coordination point is selected

### Payoff signature
Both choose A > Both choose B > Miscoordinate (any combination)
(or: Both choose A = Both choose B > Miscoordinate — pure coordination with indifferent equilibria)

### Diagnostic test
Ask: "Would both of you be happy with any outcome where you both make the same choice, and unhappy whenever you choose differently?" If yes: coordination game.

### Examples
- Driving on the left vs. right side of the road: either convention works; miscoordination is catastrophic
- Technology standards (USB-C, Blu-ray vs. HD DVD): everyone benefits from the same standard
- Meeting a stranger in a city with no pre-arranged location: need a focal point (Schelling point)

### Disambiguation from battle of sexes
In a pure coordination game, both players are indifferent between equilibria, or equally prefer the same one. In battle of sexes, both want to coordinate but each prefers a different coordination point.

### Solution routes
- Focal points (Schelling points): shared cultural or contextual anchors that players naturally coordinate on → `nash-equilibrium-analyzer` (covers focal point selection)
- Communication and pre-play agreements
- Standards-setting institutions

---

## Battle of Sexes

### Structure
- Simultaneous moves
- Non-zero-sum
- Two Nash equilibria in pure strategies; players prefer to coordinate but each prefers a different equilibrium
- Conflict over which coordination point to reach

### Payoff signature (per player)
Your preferred outcome > Other's preferred outcome > Miscoordinate

Both players prefer either coordination point over miscoordination, but they rank the two coordination points differently.

### Diagnostic test
Ask: "Would both of you prefer to be doing the same thing, but you each prefer a different 'same thing'?" If yes: battle of sexes.

### Examples
- Opera vs. football: partners want to be together; each prefers their own venue
- Joint venture HQ location: both firms prefer to co-locate, but each prefers its own city
- API standards negotiations: both parties want compatibility, but each prefers their own protocol as the standard

### Solution routes
- Alternating coordination (trade off between preferred outcomes over time)
- Pre-commitment to your preferred equilibrium to force the other to follow → `strategic-commitment-designer`
- Negotiation with side payments → `negotiation-strategist`

---

## Assurance Game (Stag Hunt)

### Structure
- Simultaneous moves
- Non-zero-sum
- Two Nash equilibria: mutual cooperation (payoff-dominant) and mutual defection (risk-dominant)
- Unlike prisoners' dilemma, cooperation is individually rational IF the other party cooperates
- The barrier is trust and mutual assurance, not individual incentive to defect

### Payoff signature
Both cooperate > You defect, they cooperate > Both defect > You cooperate, they defect

The key distinction from prisoners' dilemma: cooperating while the other defects is the *worst* outcome for you (not just bad), which means you should only cooperate if you are confident the other will too.

### Diagnostic test
Ask: "If you were confident the other party would cooperate, would you definitely cooperate? And if you were uncertain, would you fall back to the safe, individual option?" If yes to both: assurance game.

### Examples
- International environmental agreements: cooperating on emissions cuts is good if all do it; unilateral cuts while others don't is the worst outcome
- Open-source contributions: valuable if many contribute; contributing alone while others free-ride is wasteful
- Supply chain partnerships: sharing proprietary information benefits both if both share; exposing information while the other doesn't is catastrophic

### Solution routes
- Building mutual trust through repeated interaction and observable signals
- Transparency and verification mechanisms that make cooperation observable
- Upfront commitments and credible signals of cooperative intent → `strategic-commitment-designer`
- Sequencing to reveal cooperative intent early → `prisoners-dilemma-resolver`

---

## Zero-Sum Simultaneous Game (Matching Pennies / Rock-Paper-Scissors)

### Structure
- Simultaneous moves
- Zero-sum: what one player gains, the other loses exactly
- No pure Nash equilibrium: any predictable strategy is exploitable
- Mixed-strategy Nash equilibrium exists: randomize to become unpredictable

### Diagnostic test
Ask: "Does my opponent benefit from knowing in advance what I will do?" If yes, and if one player's gain is exactly the other's loss: this is a zero-sum simultaneous game requiring mixing.

### Examples
- Rock Paper Scissors (Christie's vs. Sotheby's)
- Penalty kicks in soccer: kicker and goalkeeper choose simultaneously
- IRS audit targeting: if the formula is known, only compliant taxpayers get audited
- Bluffing in poker: if you only raise with strong hands, opponents fold every time

### Solution routes
- Calculate the mixed-strategy equilibrium probabilities from the payoff matrix → `nash-equilibrium-analyzer`
- Use randomization devices to achieve unpredictability
- Consider whether the game can be restructured to avoid the zero-sum dynamic

---

## Borderline Cases and Disambiguation

### "Is this a prisoners' dilemma or chicken?"
The test: what happens if both players choose the "hard" option (both defect vs. neither swerves)?
- Prisoners' dilemma: both defect is a **Nash equilibrium** (bad but stable)
- Chicken: both don't swerve is a **catastrophe** (not a Nash equilibrium — both would want to deviate)

### "Is this a coordination game or assurance game?"
The test: what happens if you cooperate and the other doesn't?
- Coordination game: you are unhappy (miscoordination), but not catastrophically so
- Assurance game: cooperating while the other defects is the **worst possible outcome** for you (zero payoff or negative — you shared information / resources and got nothing back)

### "Is this sequential or just asymmetric simultaneous?"
A game is sequential if Player B *observes* Player A's choice before making their own — not just if Player A happens to go first in calendar time. If B must commit without observing A's actual choice, it is simultaneous even if the decisions happen at different calendar times.

### "Is this zero-sum or just competitive?"
A competitive game is not necessarily zero-sum. A market where firms compete for share is competitive but non-zero-sum — both can grow or both can shrink together. Zero-sum means the total payoff is fixed regardless of outcome; every unit transferred is a gain for one and an equal loss for the other.
