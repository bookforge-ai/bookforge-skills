---
name: negotiation-strategist
description: "Apply the complete game-theoretic bargaining framework to any negotiation. Use this skill when a user needs to structure a negotiation, determine who has leverage, calculate the fair split, or decide whether to make a concession or walk away. Triggers include: user is preparing for a salary negotiation, contract renegotiation, partnership deal, M&A term sheet, or labor negotiation and wants to know what number to open with and why; user wants to determine the 'pie' — the true surplus that is actually at stake between the two parties, not the headline dollar figures; user needs to identify and quantify their Best Alternative to a Negotiated Agreement (BATNA) or the other side's BATNA before entering talks; user wants to know how to improve their bargaining position before the negotiation starts (raise your BATNA, lower theirs); user must decide whether to bundle multiple issues together or separate them; user is weighing whether to actually strike, walk out, or threaten to do so, and wants to understand the cost-benefit calculation; user wants to propose a virtual-strike or escrowed-revenue arrangement to eliminate collateral damage while preserving negotiating pressure; user is in an alternating-offer negotiation and wants to calculate the equilibrium split given relative patience levels; user suspects they are negotiating over the wrong number (confusing total value with incremental value above no-deal); user faces brinkmanship — escalating risk of breakdown — and wants to calibrate how far to push. This skill does NOT cover simultaneous-move games (use nash-equilibrium-analyzer), one-shot ultimatum games without iteration, or multi-party coalition bargaining beyond two principal parties."
version: 1
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [11]
tags: [game-theory, negotiation, bargaining, BATNA, deal-structuring]
depends-on: [backward-reasoning-game-solver]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of the negotiation situation: the parties, what is being negotiated, what each side can do if no deal is reached (their outside options or BATNAs), the timeline, any multi-issue dimensions, and the current state of talks"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes the negotiation context in text; agent produces a structured strategy with explicit numbers, leverage analysis, and recommended moves"
discovery:
  goal: "Measure the pie correctly, identify each party's BATNA, calculate the equilibrium split, diagnose the leverage imbalance, and produce a concrete negotiation strategy with specific opening positions, concession logic, and walk-away thresholds"
  tasks:
    - "Identify both parties and what they are negotiating over"
    - "Establish each party's BATNA: what each gets with zero agreement"
    - "Calculate the pie: total agreement value minus sum of BATNAs"
    - "Apply the equal-split principle: each party gets BATNA plus half the pie"
    - "Assess impatience asymmetry using the delta formula to adjust the split"
    - "Diagnose BATNA improvement opportunities: raise yours, lower theirs"
    - "Evaluate whether to bundle or unbundle multiple issues"
    - "Assess brinkmanship and strike dynamics if talks have or may break down"
    - "Evaluate virtual-strike option if a real disruption would cause collateral damage"
    - "Deliver: pie calculation, each party's fair-split number, BATNA improvement moves, recommended opening position, and walk-away threshold"
  audience: "Business negotiators, HR and labor relations teams, corporate development professionals, lawyers structuring deals, partnership managers, procurement teams, and anyone entering a bilateral negotiation where the stakes are explicit and the goal is an optimal, durable agreement"
  when_to_use:
    - "User needs to calculate what number to open with in a salary or contract negotiation"
    - "User suspects they are being asked to split total value instead of incremental value — the pie-measurement trap"
    - "User wants to know how their BATNA or the other side's BATNA affects who gets what"
    - "User must decide whether to take actions before negotiating that will change the BATNAs"
    - "User is structuring a multi-issue deal and wants to know whether to bundle or separate issues"
    - "User is in or approaching a strike, lockout, or deal-collapse situation and wants a clear cost-benefit view"
    - "User wants to propose a virtual-strike mechanism to preserve negotiating credibility without collateral harm"
---

# Negotiation Strategist

## When to Use

Use this skill any time two parties are negotiating over value that only exists if they reach agreement. The framework applies whether the context is labor-management, commercial contracts, partnership terms, M&A deal points, or international trade negotiations.

The two foundational questions this skill answers:

1. **How much value is actually at stake?** (The pie — not the headline number)
2. **Who gets how much, and why?** (BATNA-based equal split, adjusted for patience and leverage)

## Core Framework

### Step 1: Establish the BATNAs

Before calculating anything, identify what each party gets with no deal.

**BATNA = Best Alternative to a Negotiated Agreement.** It is the best outcome each side can secure on its own without the other party's cooperation.

- Ask: "If talks break down completely, what does each side do and what does that earn them?"
- BATNAs are not aspirations. They are concrete fallback outcomes. If a union can earn $300/day in outside work during a strike, that is their BATNA. If management can operate with replacement workers at $500/day profit, that is theirs.
- BATNAs can be improved strategically (see Step 5).

### Step 2: Calculate the Pie

**The pie is not the total value of the agreement. It is the additional value created by agreement above what both parties would get anyway.**

Formula:
```
Pie = (Agreement Value) - (Party A BATNA) - (Party B BATNA)
```

Example: Hotel earns $1,000/day when open. Union BATNA = $300/day (outside work). Management BATNA = $500/day (scab operation).
```
Pie = $1,000 - $300 - $500 = $200/day
```

The parties are not negotiating over $1,000. They are negotiating over $200. This matters enormously — anchoring on the wrong number leads to systematically wrong expectations.

**The Talmud principle traces this insight to ancient fairness norms:** when two parties dispute a garment each claims, the portion each concedes to the other is split evenly. The logic is exactly the BATNA-based pie calculation applied to physical division of cloth.

### Step 3: Calculate the Equal Split

With equal patience and equal bargaining position:

```
Party A receives: A's BATNA + Pie/2
Party B receives: B's BATNA + Pie/2
```

From the hotel example:
```
Union receives: $300 + $100 = $400/day
Management receives: $500 + $100 = $600/day
```

The equal split of the pie is the baseline. It is "equal" not in the sense of equal total receipts, but in the sense that each party gains the same increment above their no-deal fallback.

**Why this is the right number:** Both parties contribute equally to the existence of the pie. Neither can claim a larger share of the surplus simply because their outside option happens to be higher. The BATNA is already theirs — it is not a bargaining chip to be divided.

### Step 4: Adjust for Impatience (Rubinstein Equilibrium)

When the two parties alternate making offers and delays are costly, impatience breaks the 50/50 split of the pie in favor of the more patient party.

**Impatience factor δ (delta):** The fraction of value that remains after one round of delay. If a dollar next week is worth $0.99 today, then δ = 0.99 (patient). If a dollar next week is worth $0.33 today, then δ = 1/3 (very impatient).

**Rubinstein equilibrium split of the pie:**
```
Proposer's share of pie = 1 / (1 + δ)
Responder's share of pie = δ / (1 + δ)
```

Key cases:
- δ = 1 (no cost to waiting): split is 1/2 and 1/2. Pure 50/50.
- δ = 1/2 (each delay loses half the pie): proposer gets 2/3, responder gets 1/3.
- δ → 0 (extreme impatience, like ultimatum game): proposer gets essentially everything.

**Backward induction logic (from the backward-reasoning-game-solver framework):** The proposer's advantage arises because each round the proposer can claim the portion of pie that would be lost if the responder said no. The responder only gets the δ-discounted value of their next turn. Working backward from the terminal condition produces the δ/(1+δ) formula for the responder's share.

**Practical implication:** If your counterpart is under more time pressure than you are (public media coverage, quarterly earnings, expiring option, cash crunch), you are effectively the more patient party and should capture more than 50% of the pie. Conversely, if your organization faces political pressure to settle quickly, expect to concede more.

### Step 5: Improve the BATNAs — "This Will Hurt You More Than It Hurts Me"

BATNAs are often not fixed. Before or during negotiations, both parties can take actions that shift the BATNA landscape.

**General rule:** You will do better in the negotiation if your BATNA improves relative to your counterpart's BATNA — even if both BATNAs get worse in absolute terms, as long as theirs gets worse by more.

**Calculation:** If an action costs you X but costs the other party Y, and Y > X, the action is worth taking even though it hurts you, because it improves your relative bargaining position by (Y - X)/2 after the pie is re-split.

Example:
- Baseline: Union BATNA $300, Management BATNA $500. Pie = $200. Union share = $400.
- Union intensifies picketing: costs union $100/day in outside income, reduces management's scab profit by $200/day.
- New BATNAs: Union = $200, Management = $300. Pie = $500. New union share = $200 + $250 = $450.
- Net gain to union: +$50/day despite the self-imposed cost.

**MLB 1980 case study:** Players struck during the exhibition season (players received no salary, but owners collected gate revenue from vacationers). Players returned for the regular season but threatened another strike on Memorial Day weekend — when owner revenues spike sharply. The players had no salary at stake during the exhibition season, so their cost was low. Owner revenue loss was highest precisely when the strike threat loomed. The players identified the timing that maximized the asymmetry between their cost and the owners' cost.

**BATNA improvement tactics:**
- **Raise your BATNA:** Develop credible outside alternatives before negotiating. Competing offers, alternative suppliers, internal capability development, coalition formation.
- **Lower their BATNA:** Actions that reduce the other side's ability to walk away or operate without you. Intensified competition for their customers, public commitments that make their fallback position more visible or more costly.
- **Both simultaneously:** If both BATNAs drop but theirs drops more, you gain.

### Step 6: Multi-Issue Bundling

When multiple issues are on the table, the choice to bundle or unbundle them strategically affects outcomes.

**Bundle when:**
- You value different issues differently than your counterpart does.
- Bundling allows a package trade where you concede on issues you care less about in exchange for wins on issues you care more about.
- Example: A company values group health coverage at $1,000/worker while an individual worker would pay $2,000 for the same coverage. The company can offer health coverage instead of an equivalent wage increase — both parties prefer the bundle.
- Broad negotiations (like GATT/WTO trade rounds) succeed more than narrow sector-by-sector talks for exactly this reason: the larger the bundled package, the more room for issue-swapping.

**Unbundle when:**
- Your counterpart is trying to use strength on one issue to extract concessions on an issue where you are strong.
- Bundling a security alliance with a trade dispute allows one party to threaten the security arrangement to extract economic concessions. The weaker party on one dimension should insist on separating the games.
- Example: Japan insisted the U.S.-Japan military alliance and trade disputes be negotiated separately to prevent the U.S. from leveraging security threats to extract trade concessions.

### Step 7: Brinkmanship and Strikes

Strikes and breakdowns happen even when both parties would prefer agreement, because:

1. **Asymmetric information:** Each side must guess the other's cost of waiting. Since a lower cost of waiting is advantageous, each side has incentive to claim its costs are low. Claims without proof are not credible. The only credible proof is actually incurring the cost.

2. **Signaling through pain:** A strike is a costly signal. By actually striking, the union demonstrates that its cost of striking is lower than management believed. The signal is credible precisely because it hurts.

3. **Brinkmanship mechanics:** Rather than an all-or-nothing strike threat (not credible when much time remains), the effective form is gradual escalation — tempers rising, talks souring, increasing probability of breakdown each day. The party that fears breakdown less has the stronger position. Brinkmanship is a weapon for the stronger party.

**When strikes occur despite the theory predicting they should not:** Both sides must have a common view of the eventual outcome for agreement to happen immediately. Disagreement about who will concede — caused by private information or genuine strategic ambiguity — causes both sides to hold out, incurring real costs. The strike ends when one side's resolve is tested enough that the other side's belief updates.

**Implication for preparation:** Before talks begin, invest in understanding the other side's true cost of delay — their cash position, external pressures, political constraints. The better your model of their impatience, the less likely you are to miscalibrate and accidentally trigger a breakdown.

### Step 8: Virtual Strikes

When a real strike or lockout would cause large collateral damage — to customers, third parties, public reputation, or the long-term enterprise — consider proposing a virtual strike arrangement.

**Mechanism:**
- Workers continue working as normal.
- The employer continues producing as normal.
- During the virtual strike period, neither side gets paid: workers forfeit wages; employer forfeits all revenue (paid to a third party — government, charity, or customers as free product).
- The BATNAs are unchanged: both sides feel the same financial pain as in a real strike.
- No third parties are harmed.

**Why it works:** The bargaining-theoretic logic of a strike is purely about pain imposition — demonstrating that your cost of not having a deal is lower than the other side believes. A virtual strike replicates this exactly without the collateral harm of service disruption, consumer inconvenience, or reputational damage.

**Historical precedent:** WWII-era Jenkins valve plant (Bridgeport, CT); 1960 Miami bus strike (customers rode free); 1999 Meridiana Airlines pilot strike (Italy's first virtual strike — flights operated, Meridiana donated all ticket revenue to charities). In all cases management forfeited gross revenue, not just profits, because profit measurement is too easy to manipulate.

**When to propose it:** Propose before the real strike becomes imminent — ideally as a contingency clause in the contract: "If negotiations fail at the next renewal, the default dispute mechanism is a virtual strike." Agreeing in advance avoids the game-theoretic problem of appearing weak by proposing it in the heat of a breakdown.

**Limitation:** Public relations benefit of virtual strikes may paradoxically make them harder to implement — some employers prefer the reputational damage of a real strike over the reputational windfall a virtual strike gives workers.

## Worked Example: The Triangle Airfare Negotiation

Two companies (Houston and San Francisco) share a New York lawyer. The lawyer flies a triangle route NY-Houston-SF-NY ($2,818) instead of two round trips ($3,818). The savings = $1,000.

**Wrong approaches:**
- Split the triangle fare 50/50 → Houston pays $1,409. But Houston's standalone round-trip is $1,332. Houston would refuse.
- Allocate by leg or mileage → leads to ad hoc results that depend on route geometry, not fairness.

**Right approach — measure the pie:**
- Houston BATNA: $1,332 (its own round-trip).
- SF BATNA: $2,486 (its own round-trip).
- Total BATNA sum: $3,818.
- Agreement value: $2,818.
- Pie = $3,818 - $2,818 = $1,000.
- Equal split: each saves $500 above their BATNA.
- Houston pays: $1,332 - $500 = **$832**
- SF pays: $2,486 - $500 = **$1,986**

This is the uniquely fair and stable outcome: each party gets an equal share of the value they jointly created by cooperating.

## Quick Reference

| Concept | Formula |
|---|---|
| Pie | Agreement value - Party A BATNA - Party B BATNA |
| Equal split (Party A) | A BATNA + Pie/2 |
| Equal split (Party B) | B BATNA + Pie/2 |
| Proposer share (Rubinstein) | 1 / (1 + δ) |
| Responder share (Rubinstein) | δ / (1 + δ) |
| Patient limit (δ → 1) | 50/50 |
| Ultimatum limit (δ → 0) | 100/0 |

## Structural Self-Check

Before finalizing any negotiation strategy, verify:

- [ ] Have I identified each party's BATNA concretely, not aspirationally?
- [ ] Have I calculated the pie as the increment above BATNAs, not the total headline figure?
- [ ] Have I accounted for asymmetric patience and used the δ/(1+δ) formula if one party is more impatient?
- [ ] Have I considered pre-negotiation BATNA improvement moves (raise mine, lower theirs)?
- [ ] Have I identified all issues on the table and decided whether bundling benefits me?
- [ ] If a strike or breakdown is possible, have I calculated who bears more relative cost?
- [ ] If collateral damage is large, have I considered proposing a virtual strike mechanism?
- [ ] Is my opening position anchored to the correct number (my BATNA + half the pie), not a naive split of total value?

## References

- `references/rubinstein-bargaining-math.md` — Full derivation of the δ/(1+δ) split from backward induction, with worked numerical examples for δ = 0.99, 0.5, and 1/3
- `references/batna-improvement-case-studies.md` — MLB 1980 exhibition season strike, hotel union/management 101-day season, detailed numbers
- `references/virtual-strike-mechanics.md` — Meridiana 1999 case, Jenkins valve plant, Miami bus strike, proposal language for contingency clauses
- `references/multi-issue-bundling-guide.md` — GATT/WTO bundling logic, Japan-US security/trade separation, health benefits vs. wages example
