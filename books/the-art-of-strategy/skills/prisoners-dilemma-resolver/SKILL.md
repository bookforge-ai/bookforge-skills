---
name: prisoners-dilemma-resolver
description: |
  Diagnose whether a multi-player conflict is a prisoners' dilemma and design a cooperation mechanism to resolve it. Use when parties are locked in a mutually destructive pattern even though all would benefit from cooperation — price wars, overfishing, arms races, advertising spirals, commons depletion, collective action failures. Distinguishes prisoners' dilemmas (dominant strategy to defect) from coordination problems (no incentive to deviate once aligned) and tailors the remedy accordingly. Produces a structured cooperation design plan: diagnosis, payoff assessment, discount-rate threshold calculation, mechanism selection from a resolution menu (self-enforcement through repeated play, tit-for-two-tats, mutual promises with escrow, linkage, reputation systems, third-party enforcement, Ostrom commons governance), and implementation checklist. Use when someone says 'everyone would be better off if we all cooperated but no one does', 'we keep undercutting each other even though it hurts everyone', 'how do we stop a race to the bottom', 'we need a collective agreement that actually holds', 'our cartel keeps collapsing', 'how do I stop a defection spiral', 'we need to solve a commons problem', or 'is this a coordination problem or a cooperation problem'.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-art-of-strategy/skills/prisoners-dilemma-resolver
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy: A Game Theorist's Guide to Success in Business and Life"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [3, 9]
tags: [game-theory, cooperation, negotiation, collective-action, prisoners-dilemma]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Description of the strategic situation: players, choices available, payoffs or outcomes, interaction history, relationship duration"
    - type: none
      description: "Skill can also work from a verbal description of the conflict"
  tools-required: [Read, TodoWrite]
  tools-optional: []
  environment: "Can run from any directory; operates on situation descriptions provided by the user"
discovery:
  problem-patterns:
    - "everyone cooperating is best but no one does"
    - "race to the bottom / destructive competition"
    - "commons overexploitation"
    - "cartel or collusion arrangement that keeps collapsing"
    - "collective action failure"
    - "arms race or advertising war"
    - "defection spiral that no one can stop unilaterally"
    - "coordination vs cooperation confusion"
  anti-patterns:
    - "zero-sum game: one player's gain is another's loss (no cooperation surplus exists)"
    - "single-shot interaction with no future relationship (may need external enforcement)"
    - "parties have different information about payoffs (screening/signaling skill may be more relevant)"
---

# Prisoners' Dilemma Resolver

## When to Use

Use this skill when you face a situation where:
- **All parties would benefit from mutual cooperation, but each has a private incentive to defect** — this is the defining feature of a prisoners' dilemma. Price wars, overfishing, arms races, and advertising spirals are canonical instances.
- **A collective agreement has been tried and keeps collapsing** — parties promise to cooperate, then someone cheats.
- **A commons is being overexploited** — individuals capture private gains while spreading costs across the group.
- **You need to decide between cooperation and competition** — unsure whether a situation calls for restraint or aggressive play.
- **You need to distinguish a cooperation problem from a coordination problem** — cooperation problems (prisoners' dilemma) have dominant strategies to defect; coordination problems have no incentive to deviate once aligned on a convention. The remedies differ sharply.

Preconditions: you have at least one of:
- A description of the conflict, the parties involved, and what each can choose to do
- A rough sense of who gains and who loses from each combination of choices
- Information about how long the relationship has been ongoing and how long it is expected to continue

**Agent:** Before starting, confirm: (1) how many players are involved, (2) whether this is a one-shot or repeated interaction, and (3) whether the user wants only a diagnosis or a full cooperation mechanism design. The mechanism design is the core deliverable.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Identify: who are the players, what can each choose, what are the rough payoffs?
                    ↓
Environment → Are there documents describing the situation, history, or prior agreements?
                    ↓
Gap analysis → Do I have enough to build a payoff table and assess the discount rate?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time)
                    │
                    NO
                    ↓
              PROCEED with diagnosis and mechanism design
```

### Required Context (must have — ask if missing)

- **The players:** Who are the parties? How many? Are they identifiable individuals, firms, nations, or anonymous members of a group?
  → Check prompt for: named parties, "we vs. they" language, player count
  → If missing, ask: "Who are the parties in this situation? Are they a small identifiable group or a large anonymous one?"

- **The choices:** What are the "cooperate" and "defect" options for each player?
  → Check prompt for: specific behaviors like pricing, output levels, investment, restraint
  → If missing, ask: "What does cooperation look like in practice — what would each party have to do or give up? And what does defection look like — what is the tempting unilateral advantage?"

- **The payoff structure:** Is defection dominant regardless of what others do? Or does the best response depend on what others choose?
  → Check prompt for: "no matter what they do," "everyone is better off if all cooperate but each has an incentive to cheat," outcomes from prior interactions
  → If missing, ask: "When you consider your best move — is it to defect regardless of what the other party does? Or does your best move depend on what they do?"

- **Relationship horizon:** Is this a one-shot interaction or an ongoing relationship? How long is it expected to continue?
  → Check prompt for: contract duration, relationship history, expected future interactions
  → If missing, ask: "Is this a one-time interaction or an ongoing relationship? If ongoing, is there a foreseeable end date?"

### Observable Context (gather from prompt or documents)

- **Prior defection history:** Have parties cheated before? Does each party know it?
  → Relevant for: assessing whether trust has already been destroyed, choosing repair strategies

- **Observability:** Can each party monitor what others actually do, or only infer from outcomes?
  → Relevant for: mechanism design — hidden defection requires different solutions than visible defection

- **Player composition stability:** Is the group of players stable, or do new entrants frequently disrupt existing arrangements?
  → Relevant for: Ostrom principle 1 (clear membership) and end-game defection risk

### Default Assumptions

- If interaction type is unspecified: assume repeated indefinitely with low probability of each period being the last.
- If payoff magnitudes are unspecified: treat the gain from unilateral defection as moderate — sufficient to tempt but not extreme.
- If number of players is unspecified: assume two-player dilemma; flag multiperson extensions where they change the analysis.
- If observability is unspecified: assume imperfect observability (parties can observe outcomes but not always attribute them to a specific defector).

### Questioning Guidelines

Ask ONE question at a time, most critical first. Show what you already know before asking. State why you need the information.

## Process

Use `TodoWrite` to track steps before beginning.

```
TodoWrite([
  { id: "1", content: "Diagnose: confirm prisoners' dilemma vs coordination problem", status: "pending" },
  { id: "2", content: "Map payoffs: build rough payoff table with cooperation surplus", status: "pending" },
  { id: "3", content: "Assess discount rate: calculate cooperation sustainability threshold", status: "pending" },
  { id: "4", content: "Score mechanism prerequisites: detection, clarity, certainty, size, repetition", status: "pending" },
  { id: "5", content: "Select and design cooperation mechanism from resolution menu", status: "pending" },
  { id: "6", content: "For commons/multiperson: apply Ostrom's design principles checklist", status: "pending" },
  { id: "7", content: "Produce cooperation design plan with implementation steps", status: "pending" }
])
```

---

### Step 1: Diagnose the Game Type

**ACTION:** Determine whether the situation is a genuine prisoners' dilemma, a coordination problem, or something else. This diagnosis determines the entire remedy.

**WHY:** The treatments are fundamentally different. A prisoners' dilemma has a dominant strategy to defect — each player is better off defecting regardless of what others do. A coordination problem has multiple equilibria — once aligned on the same convention (QWERTY, driving on the right, common standards), no one wants to deviate unilaterally. Applying cooperation mechanisms to a coordination problem is wasted effort; what's needed is a focal point or a critical mass to tip behavior.

**Two-question diagnostic:**

1. "If the other party cooperates, am I still better off defecting?" (unilateral defection payoff)
2. "If the other party defects, am I still better off defecting?" (defection-regardless test)

If YES to both → prisoners' dilemma. Defection is dominant. Proceed through this skill.

If NO to question 1 (defection hurts me when others cooperate) → coordination problem. The issue is aligning expectations, not suppressing defection. See coordination notes in References.

If YES to question 1 but NO to question 2 → asymmetric game. One party may have a dominant defection strategy while the other's best response depends on context. Requires separate analysis.

**Also check: is this zero-sum?** In a zero-sum game, every gain by one player comes at exactly equal cost to another. Zero-sum games have no cooperation surplus — there is nothing to gain from mutual restraint. The prisoners' dilemma is NOT zero-sum: both players are better off in the mutual cooperation cell than in the mutual defection cell.

**Confirm the cooperation surplus exists:** There must be a combination of choices where all parties are better off than in the mutual-defection equilibrium. If no such combination exists, this is not a prisoners' dilemma.

Mark Step 1 complete in TodoWrite.

---

### Step 2: Map the Payoffs

**ACTION:** Construct a rough payoff table showing the four cells: (Cooperate, Cooperate), (Cooperate, Defect), (Defect, Cooperate), (Defect, Defect). For multiperson dilemmas, show how collective payoff changes as the number of cooperators rises.

**WHY:** The payoff table makes the temptation and its cost concrete. Without it, the mechanism design is abstract. The payoff structure also determines which mechanisms are viable — specifically, the ratio of the one-period defection gain to the ongoing cooperation gain determines the discount-rate threshold (Step 3).

**Standard prisoners' dilemma payoff ordering (for each player):**
- Defect while other cooperates > Mutual cooperation > Mutual defection > Cooperate while other defects
- In shorthand: T > R > P > S (Temptation > Reward > Punishment > Sucker)

**Quantify if possible:**
- One-period defection gain = T − R (what you gain in the short term by cheating)
- Annual cooperation gain loss = R − P (what you lose each year if cooperation collapses)
- Break-even interest rate (see Step 3): (R − P) / (T − R)

**For multiperson / commons situations:** Replace the 2x2 table with a contribution schedule showing how each party's payoff changes as the number of cooperators increases. Key feature: each defector gains a fixed amount regardless of how many others defect, but spreads a cost across all cooperators. This is the "contribution game" structure.

Mark Step 2 complete in TodoWrite.

---

### Step 3: Calculate the Discount-Rate Threshold

**ACTION:** Determine the maximum interest rate (discount rate) at which sustained cooperation is rational. If the actual interest rate or impatience level is below this threshold, cooperation through repeated play is sustainable without external enforcement.

**WHY:** The key insight of repeated-game analysis is that defection gains a short-term advantage but destroys long-term cooperation value. Whether defection is worth it depends on how much you value the future. If you are very impatient (high discount rate), the future is worth little and defection becomes attractive even knowing the relationship will collapse. If you value the future sufficiently (low discount rate), the prospect of losing ongoing cooperation outweighs the temptation to cheat today.

**Formula:**

Cooperation is self-sustaining if the interest rate r satisfies:

```
r < (R − P) / (T − R)
```

Where:
- R = payoff from mutual cooperation (reward)
- P = payoff from mutual defection (punishment)
- T = payoff from defecting while other cooperates (temptation)
- T − R = one-period gain from cheating
- R − P = annual cost of losing the cooperative relationship

**Worked example (from Ch. 3, Rainbow's End / B.B. Lean pricing):**
- Mutual cooperation: $72,000 each per year (R)
- Mutual defection: $70,000 each per year (P)
- One-period defection gain: $110,000 − $72,000 = $38,000 (T − R)
- Annual cost of collapsed cooperation: $72,000 − $70,000 = $2,000 (R − P)
- Break-even rate: $2,000 / $38,000 = 5.26% per year
- If actual interest rate > 5.26%: cooperation collapses; if < 5.26%: self-sustaining

**What raises the sustainability threshold (makes cooperation easier):**
- Longer shadow of the future: indefinite interactions, no known end date
- Growing relationship value: stakes grow over time, making defection increasingly costly
- Stable player composition: no new entrants who don't share the history
- Frequent interactions: each "period" is shorter, making each defection opportunity less rewarding

**What lowers the sustainability threshold (makes cooperation harder):**
- High discount rates: impatience, financial distress, declining industry
- End-game visibility: clear final period triggers backward-induction unraveling
- Low cooperation surplus: R − P is small relative to T − R
- Business booms: temporary windfalls make defection more tempting right now

**End-game problem:** In a finite repeated game with a known final period, backward induction unravels cooperation all the way to round 1. Solution: eliminate the clear end-game — use indefinite time horizons, rolling contracts, or overlapping agreements so there is no obvious "last round."

Mark Step 3 complete in TodoWrite.

---

### Step 4: Score the Punishment Mechanism Prerequisites

**ACTION:** Evaluate the situation against five prerequisites for an effective punishment-based cooperation mechanism. Each gap identifies a specific design problem to solve.

**WHY:** Punishment is the most common mechanism for sustaining cooperation. But punishment only deters defection if it meets specific structural requirements. A gap in any one of the five areas undermines the entire mechanism. Identifying which prerequisite is weak tells you exactly what the mechanism design needs to fix.

**The five prerequisites:**

**1. Detection** — Can defection be observed, attributed to the right party, and detected quickly?
- Fast, accurate detection allows immediate targeted punishment, reducing the gain from cheating.
- Slow or inaccurate detection gives defectors a long free ride before punishment arrives.
- Ambiguous attribution (cannot tell WHO cheated, only that cheating occurred) forces blunt punishments that hurt cooperators too.
- Design tool: make defection observable by structure — arrange for cheating to immediately surface (price-matching clauses put customers in charge of detection; lunar-calendar bid rotation made cheating immediately visible to rivals).

**2. Clarity** — Are the rules of cooperation and the boundaries of acceptable behavior unambiguous?
- If boundaries are complex, parties may cheat by mistake or fail to make a rational calculation. Tit-for-tat's great strength is its clarity: if you cheat, I cut prices immediately next period. No ambiguity.
- Collusion cartels that fail often fail because what counts as cheating is unclear (price cuts vs. quality upgrades vs. extended credit terms).

**3. Certainty** — Is punishment guaranteed when defection occurs? Is cooperation reliably rewarded?
- Uncertain punishment (WTO-style multi-year adjudication where political considerations override facts) provides weak deterrence.
- Design tool: make punishment automatic and mechanical — most-favored-customer clauses, automatic price-matching policies.

**4. Size** — Is the punishment large enough to deter, but not so large that errors cause catastrophic spirals?
- Minimum deterrent punishment is preferable: set punishment at the level required to make defection unprofitable, no larger. Larger punishments amplify errors.
- When errors are possible (as they always are in practice), forgiveness of occasional defections is optimal — punishment should be as low as is compatible with deterrence.

**5. Repetition** — Is there a sufficient "shadow of the future"? (Covered in Step 3 — confirm result applies here.)
- Self-enforcing cooperation requires future value to exceed the one-period defection gain (the threshold from Step 3).

Mark Step 4 complete in TodoWrite.

---

### Step 5: Select and Design the Cooperation Mechanism

**ACTION:** Choose the appropriate mechanism from the resolution menu below. Mechanisms are ordered from lowest to highest external requirement. Select the lowest-level mechanism that is feasible given the prerequisites scored in Step 4.

**WHY:** Not every situation requires the same intervention. Using heavy external enforcement when self-enforcement would work wastes resources and creates regulatory risk (antitrust exposure for firms). Using self-enforcement when the prerequisites are missing produces predictable failure. Matching mechanism to situation is the core design task.

**Resolution Menu (escalating external requirement):**

---

**Level 1 — Self-enforcing repeated play (tit-for-tat or generous variant)**

*Use when:* discount rate is below threshold (Step 3 result), players interact repeatedly, detection is feasible.

*How it works:* Players cooperate initially, then mirror the other's last move. The credible threat of future retaliation deters current defection.

*Standard tit-for-tat:* Cooperate first; replicate opponent's last move every subsequent period.
- Strengths: clear, nice (never initiates defection), provocable (punishment is immediate), forgiving (restores cooperation after one cooperative move).
- Fatal flaw in noisy environments: any error or misperception triggers an alternating defection spiral (Hatfield-McCoy pattern). Each side punishes what it perceived as defection, but the other side is merely responding to the punishment.

*Generous tit-for-tat (preferred in practice):* Cooperate first; punish sustained defection but forgive isolated defections. The tamarin monkey threshold: tolerate up to 1 defection, punish 2 consecutive defections.
- Advantage: breaks punishment spirals caused by noise or misperception.
- Rule: Do not respond to a single defection. If the other party defects twice in a row, switch to defect until they cooperate twice in a row.

*Implementation checklist:*
- [ ] Define what counts as cooperation and defection in operational terms
- [ ] Set the monitoring interval (how quickly is defection detected and responded to?)
- [ ] Choose forgiveness threshold (1 defection? 2 consecutive? context-dependent)
- [ ] Communicate the strategy clearly to the other party — clarity is a prerequisite

---

**Level 2 — Mutual promises with escrow or simultaneous commitments**

*Use when:* Tit-for-tat is viable but trust is currently depleted; players need a credibility boost to restart cooperation.

*How it works:* Both parties make simultaneous promises and deposit promised payments (or penalties for non-performance) in a neutral escrow account. Neither can renege without forfeiting the escrow. Converts soft promises into hard commitments.

*Use cases:* Restart of cooperation after a defection episode; situations where one party is less patient and needs a structural guarantee; situations where the relationship is new and no reputation exists yet.

---

**Level 3 — Reputation and linkage across multiple interactions**

*Use when:* The dyadic interaction has insufficient cooperation surplus to sustain self-enforcement on its own, but the parties interact in multiple dimensions.

*Reputation mechanism:* Public record of each party's cooperation history creates external cost for defection beyond the bilateral relationship. A firm that cheats on a pricing arrangement faces skepticism from future trading partners, lenders, and employees. Works best when: the reputation is observable to third parties who matter, defection is clearly attributable, and the relationship horizon extends far enough to make the reputation investment worthwhile.

*Linkage mechanism:* Bundle multiple interactions so defecting in one dimension risks the entire relationship. Cooperation surplus across all linked interactions must exceed the temptation to defect in any one. Warning: linkage scales both gains and defection gains proportionally if all dimensions have identical payoff structures — benefit comes only from asymmetries across dimensions.

---

**Level 4 — Third-party intervention and external enforcement**

*Use when:* Self-enforcement is not viable (relationship is too short, discount rate too high, detection too imperfect), and parties cannot credibly commit to punishments themselves.

*Options:*
- **Contract enforcement:** Parties write an explicit agreement specifying cooperation terms and penalties for defection. A court or arbitrator enforces it. Requires: clear specification of what counts as defection (not always possible for tacit understandings like pricing).
- **Third-party mediator/arbitrator:** A neutral third party with sufficient authority and interest in cooperation (e.g., Camp David mediator rewarding Egypt and Israel for cooperating). Third party provides both a focal point for what cooperation means and a punishment mechanism for defection.
- **Regulatory prohibition of defection:** Government makes the defect option illegal (antitrust law prevents cartelization, but also prevents the cooperation problem from arising). Note: this works in both directions — antitrust also prevents self-enforcing collusion among competitors, which is why it must be used selectively.

---

**Level 5 — Ostrom commons governance (multiperson dilemmas)**

*Use when:* The dilemma involves a large group managing a shared resource (fishery, groundwater, pasture, shared infrastructure, open-source contribution, common standards).

Apply all eight Ostrom design principles as a checklist. Each principle maps to a specific prerequisite gap:

1. **Defined boundaries** — Clear rules about who has the right to use the resource. Geographic, professional, or membership criteria. Prevents free-rider entry by outsiders.

2. **Rules match local conditions** — Usage rules (time restrictions, location restrictions, technology limits, quantity quotas) must be calibrated to what is actually detectable and enforceable in this specific context. Quantity quotas work well when quantities are easily observable; they fail for fish because catch size is hard to control exactly. Time-based and location-based rules are often more enforceable.

3. **Graduated sanctions** — Punishment starts low (verbal warning, direct approach to the violator) and escalates only for repeat or severe violations. First-offense fines are low; they ratchet up. This principle exists because light initial punishment maintains community relationships while still deterring escalation, and because the first violation might be a misunderstanding rather than deliberate defection.

4. **Automatic detection embedded in operations** — Design the governance system so monitoring happens as a byproduct of normal operations (rotation systems where the person with the good spot automatically notices if someone else is using it; team harvesting that makes solo overharvesting visible). Dedicated guard systems are costly and generate evasion; embedded detection is cheap and hard to game.

5. **Locally designed and adjusted rules** — The group that uses the resource has the information to design rules that are both effective and legitimate. Top-down management consistently fails because it lacks local knowledge of the resource, the technology, and the community norms. The group should design its own rules through a participatory process.

6. **Conflict resolution mechanisms** — Low-cost dispute resolution must be available to address perceived violations without escalating to punishment spirals. The first response to apparent cheating should be inquiry, not punishment.

7. **Recognition by external authority** — External governments must recognize the community's right to organize and enforce its own rules, not override or undermine local governance.

8. **Nested governance for large systems** — For large-scale resources, governance is organized in multiple layers — local groups handle local problems; coordination bodies handle cross-group issues. Monolithic centralized governance fails at scale; purely local governance fails at the system level.

**Ostrom's warning:** "The dilemma never fully disappears, even in the best operating systems. No amount of monitoring or sanctioning reduces the temptation to zero. Effective governance systems cope better than others — they do not eliminate the problem."

Mark Step 5 complete in TodoWrite.

---

### Step 6: For Multiperson Dilemmas — Assess Contribution Game Structure

**ACTION:** If the dilemma involves more than two players and a public good or shared resource, assess the contribution game structure: each party's dominant strategy is to free-ride; collective optimum requires all to contribute.

**WHY:** Multiperson prisoners' dilemmas have a specific feature that bilateral dilemmas lack: each defector's gain is fixed (they free-ride on others' contributions), but each defector imposes a cost spread across ALL cooperators. In the 4-player contribution game: contributing $1 to the pool raises total benefit by $2 (after doubling), but the contributor receives only $0.50 of the gain ($1.50 goes to others). This makes free-riding dominant regardless of what others do.

**Contribution game checklist:**
- [ ] Identify the collective good and who benefits from it regardless of contribution
- [ ] Identify the private gain from free-riding and the collective cost
- [ ] Assess whether the group is small enough for social sanctions to operate (village-scale vs. anonymous urban setting)
- [ ] Assess whether punishment is available: can group members observe who contributed and impose social costs on defectors?
- [ ] Note: experimental evidence shows people will pay a personal cost to punish free-riders (third-party punishment), which activates the dorsal striatum — the biological basis of cooperative norm enforcement

Mark Step 6 complete in TodoWrite.

---

### Step 7: Produce the Cooperation Design Plan

**ACTION:** Write a structured cooperation design plan covering the full analysis from Steps 1-6.

**WHY:** The plan must be specific and actionable. "Use tit-for-tat" is not useful. "Define price cuts of more than 5% as defection, respond with a 10% price cut effective next catalog cycle, forgive single-period deviations, treat two consecutive deviations as intentional" is useful — it specifies the operational terms the parties need to implement.

**HANDOFF TO HUMAN** — the agent produces the plan; the human negotiates, implements, and monitors.

**Plan format:**

```markdown
# Cooperation Design Plan

## Game Diagnosis
**Type:** [Prisoners' Dilemma / Coordination Problem / Asymmetric / Not applicable]
**Cooperation surplus exists:** [Yes/No — the mutual cooperation cell vs. mutual defection cell]
**Payoff structure:**
| | Other: Cooperate | Other: Defect |
|---|---|---|
| You: Cooperate | R = [value] | S = [value] |
| You: Defect | T = [value] | P = [value] |

**Dominant strategy:** [Defect / Cooperate / Context-dependent]

## Discount-Rate Assessment
**One-period defection gain (T − R):** [value]
**Annual cooperation value at stake (R − P):** [value]
**Break-even interest rate:** [calculation and result]
**Self-enforcement viable?** [Yes if actual rate < break-even / No if above]

## Prerequisite Gaps
| Prerequisite | Status | Gap Description |
|---|---|---|
| Detection | [Strong/Weak/Missing] | [specific gap] |
| Clarity | [Strong/Weak/Missing] | [specific gap] |
| Certainty | [Strong/Weak/Missing] | [specific gap] |
| Size (minimum deterrent) | [Strong/Weak/Missing] | [specific gap] |
| Repetition / shadow of future | [Strong/Weak/Missing] | [specific gap] |

## Recommended Mechanism
**Level selected:** [1–5 from resolution menu]
**Mechanism:** [Name and brief description]
**Rationale:** [Why this level fits the situation]

## Implementation Steps
1. [Operational definition of cooperation and defection in this context]
2. [Monitoring arrangement: how, by whom, with what frequency]
3. [Response rule: specific trigger and specific response]
4. [Forgiveness threshold: when to restore cooperation]
5. [Communication plan: how to make the strategy clear to all parties]
6. [Escalation path: if self-enforcement fails, what is the next level?]

## Risks and Anti-Patterns
- **End-game defection risk:** [Is there a visible final period? How to address?]
- **Punishment spiral risk:** [Is generous tit-for-tat needed? What forgiveness threshold?]
- **Player composition risk:** [Are new entrants expected? How does the mechanism handle them?]
- **Boom/bust defection timing:** [When is defection temptation highest? Special provisions needed?]

## For Commons/Multiperson Situations
Ostrom principle compliance:
- [ ] Defined boundaries
- [ ] Rules match local conditions
- [ ] Graduated sanctions
- [ ] Automatic detection embedded in operations
- [ ] Locally designed rules
- [ ] Conflict resolution mechanisms
- [ ] External recognition
- [ ] Nested governance (for large systems)
```

Mark Step 7 complete in TodoWrite.

## Inputs

- **Situation description:** Who are the players? What choices do they have? What happens to each player under each combination of choices?
- **Relationship context:** How long has the relationship been ongoing? Is it expected to continue indefinitely or does it have a clear end date?
- **Observability:** Can each party monitor what others actually do, or only observe outcomes?
- **Prior cooperation history:** Have parties cooperated or defected in the past? What happened?

## Outputs

- **Cooperation Design Plan** (Markdown) — complete structured plan with diagnosis, payoff table, discount-rate threshold, prerequisite gap assessment, mechanism selection and implementation steps, risk register, and Ostrom compliance checklist where applicable
- **Decision rationale** — for each recommendation, the WHY (which prerequisite is met or missing, why this mechanism level was chosen)

## Key Principles

- **Diagnosis before mechanism** — the correct remedy depends entirely on the game type. Applying cooperation tools to a coordination problem (or vice versa) is worse than doing nothing because it misidentifies the problem and wastes resources. Always confirm whether defection is dominant regardless of others' choices.

- **The cooperation surplus is the prize** — the difference between mutual cooperation and mutual defection payoffs is what parties are fighting over. If this surplus is small relative to the temptation to defect, self-enforcement requires either an extremely low discount rate or an external mechanism. The surplus size determines the viable mechanism space.

- **The future must be sufficiently valuable** — cooperation is self-enforcing only when the prospect of losing ongoing cooperation outweighs the one-period temptation gain. This is not a moral claim; it is an arithmetic one. Calculate the break-even discount rate explicitly. Fuzzy talk about "long-term relationships" is insufficient.

- **Punishment must be targeted, certain, and proportionate — not maximal** — the temptation to set catastrophic punishments ("nuke any country that breaks the tariff agreement") is wrong because errors will occur. When errors occur, catastrophic punishments are either not credible or produce catastrophic outcomes. Set punishment at the minimum level that makes defection unprofitable.

- **Standard tit-for-tat is fragile in noisy environments** — the real world has errors and misperceptions. Tit-for-tat cannot distinguish intentional defection from noise, and its perfect responsiveness creates punishment spirals. Generous tit-for-tat (2-consecutive-defections threshold) preserves punishment credibility while tolerating noise.

- **Cooperation and coordination are different problems** — cooperation problems (prisoners' dilemma) have dominant strategies to defect; the challenge is suppressing that incentive. Coordination problems have no incentive to deviate from the prevailing convention once everyone is on it; the challenge is getting to the right convention and escaping a bad one. Cigarette advertising bans, QWERTY entrenchment, and racial tipping are coordination problems. Arms races, price wars, and overfishing are cooperation problems.

- **Ostrom: no governance system eliminates the dilemma** — the goal is a governance system that manages the dilemma better than alternatives, not one that eliminates it. Perfection is not the standard. Practical improvement — fewer defections, faster detection, lower cost of enforcement — is.

## Examples

**Example 1: Pricing cartel between two mail-order retailers**

Situation: Rainbow's End (RE) and B.B. Lean (BB) both price shirts at $70 when both could price at $80 and each earn $72,000 vs. $70,000 per year. Each firm cuts to $70 because it's the dominant strategy: cutting while the other holds at $80 yields $110,000; holding at $80 while the other cuts yields only $24,000.

Diagnosis: Classic 2-player prisoners' dilemma. T=$110k, R=$72k, P=$70k, S=$24k. Defection dominant for both.

Discount-rate calculation: (R−P)/(T−R) = ($72k−$70k)/($110k−$72k) = $2k/$38k = 5.26%. If prevailing interest rate < 5.26%, tacit cooperation at $80 is self-sustaining.

Mechanism: Level 1 (self-enforcing repeated play). Detection: price lists are publicly observable. Clarity: define "defect" as cutting below $80. Response: immediately match any price cut in next catalog. Forgiveness: if other party restores $80 pricing, match that too. Communication: a "most-favored-customer" clause makes the automatic response policy public, removing ambiguity. Anti-pattern avoided: no explicit agreement is reached (antitrust risk); cooperation is purely tacit.

---

**Example 2: Fishery commons overexploitation**

Situation: New England fishing fleet: each captain has incentive to catch as much as possible before others do; result is collapse of species after species (Atlantic halibut, ocean perch, haddock).

Diagnosis: Multiperson prisoners' dilemma (contribution game). Each additional catch by one captain reduces the stock for all others. Dominant strategy: fish aggressively regardless of what others do.

Discount-rate calculation: Not determinative on its own — relationship continues indefinitely but individual boats can't unilaterally enforce rules against strangers.

Mechanism: Level 5 (Ostrom commons governance). Apply 8-principle checklist:
1. Boundaries: issue licenses to fish specific species in specific zones — clear membership
2. Rules match conditions: seasonal closures and gear restrictions (net size) — more observable than quantity quotas
3. Graduated sanctions: first violation = warning + education; second = fine; third = license suspension
4. Automatic detection: rotating assignment to prime fishing zones creates natural monitoring — the assigned captain notices unauthorized use immediately
5. Local design: fishing community designs the quota and rotation rules with knowledge of local conditions, not federal agency
6. Conflict resolution: fishing association mediation before formal sanction
7. External recognition: state and federal agencies recognize community fishing governance authority
8. Nested governance: local associations handle local waters; interstate compact handles migratory species

---

**Example 3: Coordination problem misdiagnosed as cooperation problem**

Situation: Ivy League colleges keep overspending on athletics even though the relative standings stay the same. "Each school would be better off if we all limited spring training to one day."

Diagnosis check: "If other schools limit training, should I limit training?" → Yes, my performance improves no more than theirs, but I save costs. "If other schools don't limit training, should I limit training?" → No, I'd be at a disadvantage. This is NOT a prisoners' dilemma. Defection is NOT dominant regardless of others' choices. The best response to "others cooperate" is to cooperate; the best response to "others defect" is to defect. This is a coordination problem.

Mechanism: Not Level 1-5 from the resolution menu. Instead: establish a focal point for the cooperative equilibrium through a collective agreement with clear enforcement (the Ivy League agreement limiting spring training to one day). Once the convention is established and everyone expects everyone else to comply, compliance becomes self-sustaining without punishment — because no one wants to be the only school overdoing training when no one else is.

Key distinction that matters: if this were a genuine prisoners' dilemma, the agreement would keep collapsing despite everyone's stated preference for cooperation. In coordination problems, a credible agreement is usually sufficient because there is no dominant strategy to defect — just a fear that others won't cooperate.

## References

- For the Ostrom 8-principle checklist with detailed examples and design notes, see [ostrom-commons-governance.md](references/ostrom-commons-governance.md)
- For the resolution menu with full specification of each mechanism level, see [resolution-menu.md](references/resolution-menu.md)
- For the cooperation vs. coordination distinction with examples, see [cooperation-vs-coordination.md](references/cooperation-vs-coordination.md)
- Source: *The Art of Strategy*, Dixit & Nalebuff, Chapter 3 (pp. 74–105) and Chapter 9 (pp. 254–280)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Art of Strategy: A Game Theorist's Guide to Success in Business and Life by Avinash K. Dixit, Barry J. Nalebuff.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
