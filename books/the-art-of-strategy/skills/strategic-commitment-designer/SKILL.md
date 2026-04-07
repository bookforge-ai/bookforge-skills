---
name: strategic-commitment-designer
description: "Design credible strategic moves — commitments, threats, and promises — to change the game in your favor before play begins. Use this skill when a user needs to lock in a position and prevent backtracking; deter an adversary from an unwanted action; compel a counterpart to take a desired action; make a negotiation stance, policy, or business pledge actually believable; or structure incentive mechanisms that hold even when renegotiation is tempting. Triggers include: user wants to commit to a course of action in a way that others will believe; user is setting a credible deterrent threat (e.g., retaliation policy, penalty clause, price floor); user must compel action by a deadline and needs the right move type and deadline design; user suspects their threat or promise will be dismissed as a bluff; user needs to choose between issuing a threat vs. a promise for deterrence or compellence; user wants to practice brinkmanship and needs to calibrate the risk level; user is designing a contract or commitment mechanism and needs to close renegotiation loopholes; user is countering an opponent's commitment or threat. This skill covers the full taxonomy of strategic moves (commitment / threat / promise, deterrence / compellence, warnings / assurances) and all eight credibility mechanisms. It does NOT perform the underlying game tree analysis — use backward-reasoning-game-solver for that before applying this skill."
version: 1
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [6, 7]
tags: [game-theory, strategy, negotiation, commitment, credibility]
depends-on: [backward-reasoning-game-solver]
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Description of the strategic situation: the players, the action you want to influence (prevent or compel), your current and desired positions, any existing threats or promises in play, and context about your ability to follow through"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes the situation in text"
discovery:
  goal: "Classify the strategic move needed, determine its purpose (deterrence or compellence), select and design one or more credibility mechanisms, and produce a concrete action plan the user can execute to change the game before play begins"
  tasks:
    - "Classify the move type: unconditional commitment, deterrent threat, compellent threat, deterrent promise, or compellent promise"
    - "Determine whether the goal is deterrence (no deadline needed) or compellence (deadline required)"
    - "Distinguish genuine strategic moves from warnings and assurances to avoid wasted effort on informational-only signals"
    - "Run the renegotiation failure test: check whether both parties would benefit from renegotiating — if so, the proposed commitment is hollow"
    - "Calibrate brinkmanship risk: only invoke if a hard commitment is not credible; size the risk to the minimum needed to compel/deter"
    - "Select and design credibility mechanisms from the Eightfold Path: contracts, reputation, cut communication, burn bridges, leave to chance, small steps, teamwork, mandated agents"
    - "Check for anti-patterns: threat too large, renegotiable commitment, commitment that forecloses a winning position, brinkmanship when you would blink first"
    - "Produce a structured action plan: move type, purpose, credibility mechanism(s), concrete implementation steps, and monitoring criteria"
  audience: "Negotiators, executives, policymakers, managers, lawyers, and anyone designing incentive structures or making strategic pledges"
  when_to_use:
    - "User needs to lock in a position to gain first-mover advantage"
    - "User wants to deter an adversary from taking an unwanted action"
    - "User must compel a counterpart to act by a specific deadline"
    - "User suspects their threat or promise will be treated as a bluff"
    - "User is designing a contract, policy, or incentive mechanism and needs it to be renegotiation-proof"
    - "User is in a brinkmanship situation and needs to calibrate the risk level"
    - "User wants to counter or defuse another player's strategic move"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Strategic Commitment Designer

## When to Use

Use this skill when you want to change the game — not just play it well — by taking a prior action that alters what others expect you to do or what you are capable of doing.

**Prerequisite:** Before designing a commitment, threat, or promise, you need to know the underlying game structure: who moves when, what the payoffs are, and what the current equilibrium looks like without any strategic move. If you have not already done this, run `backward-reasoning-game-solver` first. This skill takes up where backward induction leaves off: once you know what the game predicts, you use strategic moves to change the prediction.

The core principle: **a strategic move must change the game, not just describe your intentions.** Mere words are not strategic moves. The move works only if it alters the other party's rational expectations about your future behavior — and that requires changing either your payoffs or your available actions so that follow-through becomes your dominant choice, not just your stated preference.

---

## Step 1: Classify the Move Type

**WHY:** The taxonomy determines both what needs to be communicated and what credibility problem must be solved. Misclassifying the move type leads to designing the wrong mechanism.

Use the 3x2 taxonomy:

| | Deterrence (prevent action) | Compellence (induce action) |
|---|---|---|
| **Commitment** (unconditional first move) | Occupy a position before others can; create a fait accompli | Announce an irreversible action the other must respond to |
| **Threat** (conditional: punish non-compliance) | "If you do X, I will hurt you" — tripwire, no deadline needed | "Do Y by deadline T, or I will hurt you" — deadline is required |
| **Promise** (conditional: reward compliance) | "If you refrain from X, I will reward you" | "If you do Y by deadline T, I will reward you" |

**Warnings and assurances are not strategic moves.** A warning merely informs the other party what you would naturally do in your own interest anyway — it does not change your response rule. An assurance tells them what cooperative behavior would naturally elicit. Neither changes the game. If your "threat" is already in your interest to carry out, it is a warning. If your "promise" is already in your interest to keep, it is an assurance. Treat these as informational only and skip to credibility design only for the genuine strategic moves.

**Selecting the right move type:**
- If you want to stop something that has not yet started, and timing is open-ended → deterrent threat
- If you want to stop something already happening, or need action by a specific date → compellent threat (must attach a deadline or the opponent can use salami tactics to procrastinate)
- If punishment is too costly or reputation-destroying to be credible → consider a compellent promise instead (reward compliance rather than punish defiance)
- If you can act first without the other player being able to undo it → unconditional commitment; this is the cleanest move because it eliminates the response-rule credibility problem entirely

---

## Step 2: Run the Renegotiation Failure Test

**WHY:** A commitment that both parties would prefer to renegotiate is not a commitment at all — it collapses the moment temptation appears. This is the most common reason well-designed commitments fail in practice.

Apply the test before designing any credibility mechanism:

1. Identify the moment in the future when the commitment would be costly to honor (the "moment of temptation").
2. At that moment, ask: would both parties be better off agreeing to set the commitment aside?
3. If yes → the commitment is vulnerable to renegotiation. You cannot simply add a clause saying "no renegotiation"; you must change who holds the enforcement power so that at least one party at the table has an independent interest in enforcing the original agreement.

**The Nick Russo failure case:** A dieter offers $25,000 to anyone who catches him eating fattening food. At the moment of temptation, the dieter can offer the restaurant patron a free drink to look the other way. The patron prefers the drink to the slim chance of claiming the $25,000. Both parties benefit from renegotiation. The contract is hollow. **Fix:** enforcement must be held by a party who is not present at the moment of temptation and who has independent reasons to enforce (e.g., StickK.com's third-party charity pledge, or a supplier-producer penalty clause where the producer genuinely needs delivery, not just the fine).

---

## Step 3: Determine Purpose and Deadline Requirements

**WHY:** Deterrence and compellence have different structural requirements. Using deterrence logic for a compellence goal is a common error that allows the opponent to stall indefinitely.

**Deterrence:**
- Goal: prevent the other party from taking an action they otherwise would
- Timing: no deadline required — the threat is standing ("ever do X and I will respond")
- Better achieved with threats than promises (a threat is costless if it succeeds; a promise must be paid if it succeeds)
- Example: Cold War nuclear deterrence, beat-the-competition pricing clauses

**Compellence:**
- Goal: get the other party to take a positive action they would not otherwise take
- Timing: a specific deadline is required — without it, salami tactics defeat the move (the opponent defers action one small step at a time, and each step is too small to trigger the costly response)
- Better achieved with promises than threats for inducing genuine action (promises provide incentive not to procrastinate; threats require the threatener to invoke costs when partial progress has been made)
- Example: "Clean your room before 5 p.m. or lose dessert" vs. "Clean your room" with no deadline

**Threat vs. promise cost tradeoff:**
- A successful threat costs nothing to carry out (the action is never triggered)
- A successful promise must be paid (the reward must be delivered when the other party complies)
- A failed threat requires carrying out a costly action or accepting reputational damage from backing down
- Choose threat when deterrence is the goal and you can size the threat so the opponent complies; choose promise when compellence is the goal and you need to create a positive gradient toward compliance

---

## Step 4: Select Credibility Mechanisms (The Eightfold Path)

**WHY:** Words alone cannot make a strategic move credible. The other party knows that once they have moved, you have the incentive to renege on your threat or promise. You must change the game so that follow-through is in your interest at the moment of execution.

The eight mechanisms fall under three principles. Apply the principle that fits your situation first, then choose the specific mechanism.

### Principle 1 — Change Your Payoffs (Make Follow-Through Profitable)

**Mechanism 1: Write a contract.** Create a legal agreement with penalty clauses that make non-compliance more costly than compliance. Works best in commercial settings where the enforcer (court, arbitration panel) has independent reasons to enforce. Vulnerability: renegotiation by mutual consent. Must ensure enforcer has interests independent of both parties. Practical application: milestone-based payment contracts, performance bonds, penalty clauses for delay.

**Mechanism 2: Establish and use reputation.** Publicly commit your reputation to a position so that backing down destroys future credibility in other games. Works across repeated interactions and multiple audiences. The key is that the public declaration must be specific and visible enough that deviation is clearly observed. Vulnerability: reputation effects require future interactions — in a one-shot game, reputation has no value. Practical application: public speeches committing to a policy, publishing pricing policies in catalogs, establishing industry standing. Caution: a reputation built by public declaration can be demolished by a single visible breach (e.g., "Read my lips: no new taxes").

### Principle 2 — Limit Your Ability to Back Out (Make Retreat Impossible or Costly)

**Mechanism 3: Cut off communication.** Make yourself unavailable for renegotiation after the commitment is announced. If you cannot be reached, you cannot be persuaded to back down. Effective for creating irreversibility. Practical application: wills and trusts (the testator is unavailable after death), publishing a policy before entering negotiations, sending a certified letter. Vulnerability: you also cannot receive confirmation of compliance; you must designate a proxy to monitor.

**Mechanism 4: Burn bridges behind you.** Physically eliminate the retreat option so that advance is your only rational choice. Remove the alternative to following through. Practical application: Cortés burning his ships on arrival in Mexico (soldiers had no choice but to fight); Polaroid concentrating all resources in instant photography (committed to aggressive defense against entrants); announcing a product launch before the product is ready; signing a lease before leaving a job. The goal is to create a situation where your only rational action is the committed action.

**Mechanism 5: Leave the outcome beyond your control, or even to chance.** Delegate the trigger to an automatic mechanism or a probabilistic process that you genuinely cannot stop. Because you no longer control the response, the opponent cannot negotiate with you to avoid it. This is the mechanism underlying brinkmanship. Practical application: automatic penalty clauses triggered by observable metrics (credit ratings, delivery dates), doomsday devices, graduated penalty schedules. The power comes from genuine loss of control — simulated loss of control is transparent and ineffective.

### Principle 3 — Use Others to Help You Maintain the Commitment

**Mechanism 6: Move in small steps.** Break a large commitment into a sequence of small ones, each credible on its own. This solves the credibility problem when the full commitment is too large to be believable, and it reduces the damage if either party defects. Works against salami tactics when you are the compeller (each small step delivered honestly builds credibility for the next). Warning: the step-by-step structure creates an end-game problem — rational players anticipate defection on the last round and unravel the whole sequence. Fix: ensure there is no clearly defined last step (leave continuation open-ended). Practical application: milestone-based contracts, escalating relationship investments, progressive payment schedules.

**Mechanism 7: Develop credibility through teamwork.** Engage a group whose collective payoffs change when any individual defects. Social enforcement mechanisms — honor codes, peer accountability groups, organizational culture — make individual defection costly through shame, ostracism, or retaliation by the group. Practical application: Alcoholics Anonymous (breaking a commitment destroys standing in the group), honor codes at universities (failure to report cheating is itself a violation), labor unions (the leader is accountable to a constituency that will remove him if he backs down). The team structure changes the individual's payoffs without requiring an external enforcer.

**Mechanism 8: Employ mandated negotiating agents.** Delegate authority to an agent whose own incentives prevent flexibility. The agent genuinely cannot concede because doing so would cost them their position, reputation, or legal standing. Two forms: (a) human agents with restrictive mandates (union leaders whose members must ratify any contract; lawyers without settlement authority; real estate agents with published listing prices); (b) mechanical agents (vending machines, automated pricing systems, fixed-rule bureaucracies). The agent's constraint is credible because it is externally visible and costly to override. Vulnerability: the opponent can attempt to go directly to the principal — counter by making the principal unavailable or by ensuring the agent's constraint is itself renegotiation-proof.

---

## Step 5: Calibrate Brinkmanship (If Applicable)

**WHY:** Brinkmanship is a last resort when a hard commitment is impossible and the threat too large to be credible as written. It deliberately creates shared risk to compel compliance. Used incorrectly, it destroys both parties.

Brinkmanship is the **controlled loss of control**: the threatener controls the size of the risk but not the outcome. The risk is genuinely real — this is not a bluff. If the opponent calls the bluff, there is a real chance the catastrophic outcome occurs.

**Apply brinkmanship only when:**
- A hard, credible threat is not available (the action is too costly to be credible as a certain response)
- You need a graduated response mechanism (you do not know the minimum threat size that will work)
- You assess that your opponent's tolerance for risk is lower than yours (if you would blink first, do not start)

**Calibration protocol:**
1. Start with the smallest risk increment that has a reasonable chance of inducing compliance
2. Escalate gradually, observing the opponent's reactions
3. Maintain genuine loss of control — automated or observable mechanisms are more credible than personal discretion
4. Have a de-escalation path ready (face-saving compromise for both parties)
5. Know your own tolerance threshold before starting — if the risk will exceed your own threshold before exceeding the opponent's, do not begin

**Cuban Missile Crisis benchmark:** Kennedy estimated 1/3 to 1/2 odds of nuclear war. This was not a bluff — the risk was real. The strategy worked because Khrushchev's risk tolerance was lower. Before using brinkmanship, honestly estimate both tolerance levels.

---

## Step 6: Check for Anti-Patterns

**WHY:** Strategic moves that are poorly designed can backfire, destroying credibility, locking you into losing positions, or creating outcomes worse than no move at all.

**Anti-pattern 1 — Threat too large.** A threat exceeding what is necessary and proportionate generates terror and is socially unacceptable, making it incredible even if technically feasible. Size threats at the minimum level needed to achieve deterrence or compellence. The escalation cost if the threat fails is too high to ignore.

**Anti-pattern 2 — Renegotiable commitment.** Any commitment both parties would prefer to renegotiate will be renegotiated. Do not rely on legal language alone; ensure enforcement is held by a party with independent interests. Check: if the commitment were tested, would both you and your counterpart benefit from quietly setting it aside?

**Anti-pattern 3 — Commitment that forecloses your winning position.** Before committing, run backward induction on the new game the commitment creates. Some commitments eliminate your own optimal future moves. De Lesseps committed to a sea-level canal at Panama without checking the engineering; the commitment destroyed his ability to adapt when the geology made sea-level construction fatal. First check: does this commitment leave me with a rational path to my goal?

**Anti-pattern 4 — Commitment without a credibility mechanism.** An unconditional announcement is not a commitment; it is just a statement. If you announce a commitment without changing payoffs, eliminating retreat options, or engaging others to enforce it, the announcement will be treated as cheap talk.

**Anti-pattern 5 — Starting brinkmanship when you would blink first.** If your honest assessment is that the shared risk will exceed your own tolerance before the opponent's, brinkmanship is irrational. Your opponent will read your tolerance correctly and call your escalation.

---

## Step 7: Compose the Action Plan

**WHY:** Strategic moves must be implemented as specific prior actions, not future intentions. The plan must be executable before the game begins.

Produce a structured plan covering:

1. **Move type and purpose:** [commitment / deterrent threat / compellent threat / deterrent promise / compellent promise] for [deterrence / compellence]
2. **Deadline (if compellent):** Specific, observable deadline with graduated consequences for partial progress
3. **Credibility mechanism(s):** Which of the eight mechanisms applies, and the concrete prior action that implements it
4. **Renegotiation firewall:** Who holds enforcement authority, and why they have independent interests in enforcing
5. **Opponent's counter-options:** How the opponent might try to undermine your credibility (p. 212-215), and pre-emptive countermeasures
6. **Monitoring criteria:** Observable indicators that the move is working or has been defied
7. **Contingency:** What you will do if the move is tested (having thought this through in advance is itself a credibility signal)

---

## Discovery

This skill surfaces when the user is trying to change what others will do by taking prior action — not just responding optimally to the current game. Key phrases: "make my threat credible," "how do I commit to this," "they won't believe me," "I need them to take action by X date," "how do I deter," "designing an incentive structure," "contract that can't be renegotiated," "burned my bridges," "how do I back this up."

For detailed reference material, see:
- `references/move-taxonomy-reference.md` — full 3x2 taxonomy with examples
- `references/eightfold-path-reference.md` — detailed mechanism descriptions and case studies
- `references/renegotiation-failure-test.md` — test protocol with worked examples
- `references/brinkmanship-calibration.md` — risk calibration guide and anti-patterns
