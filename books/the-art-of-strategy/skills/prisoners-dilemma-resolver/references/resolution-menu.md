# Resolution Menu: Cooperation Mechanism Levels

Each level assumes the prerequisites of levels below it are insufficient or unavailable.
Select the lowest level that is feasible given the situation's prerequisites.

---

## Level 1: Self-Enforcing Repeated Play

**Prerequisite check:**
- [ ] Interest rate / discount rate is below the break-even threshold: r < (R−P)/(T−R)
- [ ] Interaction is expected to continue indefinitely (or at least without a known final period)
- [ ] Detection is feasible (defection can be observed within a reasonable timeframe)
- [ ] Players are identifiable (defection can be attributed to the correct party)

**Mechanism: Tit-for-tat (two variants)**

### Standard Tit-for-Tat
Rule: Cooperate in period 1. In every subsequent period, do what the other player did in the previous period.

Properties (Axelrod's four principles):
- **Clear:** The rule is simple. The opponent does not have to guess what you will do; the link between their behavior and your response is unambiguous.
- **Nice:** Never initiates defection. No first-mover defection advantage.
- **Provocable:** Defection is punished immediately — no free rides.
- **Forgiving:** After one cooperative move by the other party, cooperation is immediately restored. No grudges.

Fatal flaw in noisy environments: Any misperception or error produces an alternating defection spiral. Party A defects by mistake in round 11. Party B retaliates in round 12. Party A (who cooperated in round 11) retaliates against B's retaliation in round 13. Round 14: B retaliates again. The pattern alternates indefinitely until another error accidentally restores cooperation or both defect permanently. Real-world example: Hatfield-McCoy feud — no one remembers what started it, but retaliation is perpetual. Middle East cycles of reprisal follow the same structure.

**Do not use** standard tit-for-tat when:
- Observability is imperfect (outcomes observable but attribution uncertain)
- Communication between parties is limited
- There is a history of prior misperceptions
- The relationship has experienced recent turbulence

### Generous Tit-for-Tat (recommended for most real-world applications)

Rule: Cooperate in period 1. Tolerate up to 1 isolated defection. Punish if the other party defects twice consecutively. Resume cooperation when the other party cooperates twice consecutively.

Source: Cotton-top tamarin monkey experiments — stable cooperation emerged with this exact rule. Consistent with subsequent Axelrod tournament results when error/noise was introduced.

Why 2-consecutive threshold works:
- Single defection may be noise (error, misperception, emergency). Punishing it starts a spiral.
- Two consecutive defections are highly unlikely to both be noise. This is deliberate defection.
- The threshold is clear and simple enough to be mutually understood.

**Operational implementation steps:**
1. Define "cooperate" and "defect" in specific, observable, operational terms (e.g., "cooperate" = maintain price at or above $X; "defect" = undercut by more than $Y)
2. Set monitoring interval (how frequently are outcomes observed?)
3. Establish response lag (how quickly can punishment be implemented?)
4. Communicate the rule explicitly (or create structural clarity through most-favored-customer clauses, price-matching policies, etc.)
5. Document forgiveness rule in advance — both parties must know cooperation will be restored

**Anti-patterns:**
- Defining defection too loosely (ambiguous trigger → false positives → unnecessary spirals)
- Setting punishment too harshly (catastrophic punishment → not credible when errors occur)
- Using tit-for-tat in a market with hidden price cuts (undetectable defection makes the strategy impossible)

---

## Level 2: Mutual Promises with Escrow or Simultaneous Commitments

**When Level 1 fails because:** Discount rate is acceptable but trust has been depleted by prior defection; parties believe the other will defect; no mechanism to make future cooperation credible.

**Mechanism:**
Both parties simultaneously commit to cooperative action AND deposit a performance bond (or penalty payment) in a neutral escrow account. If either party defects, the escrow funds are paid to the other party or forfeited to a third party.

**Design elements:**
- Escrow holder: neutral third party with no stake in the outcome (law firm, bank, arbitration service)
- Trigger definition: what counts as defection must be clearly specified and verifiable by the escrow holder
- Bond size: must exceed the one-period defection gain (T−R); otherwise defection plus forfeiting the bond is still profitable
- Duration: escrow is maintained for the agreed cooperation period; released upon successful completion
- Amendment process: how do the parties modify the agreement if circumstances change?

**Limitation:** Requires explicit agreement on what constitutes defection. Works for discrete, observable commitments. Does not work for tacit cooperation arrangements where defection is continuous and ambiguous.

**Example:** Camp David Accords — US provided explicit economic rewards (external escrow, essentially) to both Egypt and Israel conditional on maintaining the peace agreement. The third party with an interest in cooperation funded the escrow.

---

## Level 3: Reputation and Linkage

### Reputation Mechanism

**When to use:** The direct bilateral relationship has insufficient cooperation value, but the parties care about their reputation with third parties (customers, future partners, lenders, regulators, employees).

**How it works:** Defection in the current relationship damages the party's reputation with observers who will matter in future relationships. This creates an indirect future cost beyond the bilateral punishment.

**Reputation effectiveness conditions:**
- Defection must be observable to relevant third parties (not just the bilateral partner)
- Defection must be clearly attributable (cannot hide behind noise or ambiguity)
- The reputational audience must be substantial — the parties must have future interactions with people who will care
- Reputation recovery is slow — the damaged party must continue in the market long enough for reputation to have positive value

**Design question:** "Who observes this interaction besides the two parties? Do those observers affect the defector's future?" If the answer is no one significant, reputation alone will not sustain cooperation.

### Linkage Mechanism

**When to use:** Multiple dimensions of interaction between the same parties; defection in one dimension can be punished across multiple dimensions; the total cooperation surplus across all linked dimensions exceeds the temptation to defect in any one.

**How it works:** Bundle multiple interactions into a single relationship. "If you defect on pricing, we will also defect on delivery terms, quality standards, and the three other dimensions of our relationship."

**Critical limitation:** If all dimensions have identical payoff structures (same T, R, P, S), then linking them scales both the cooperation gain AND the defection gain proportionally, leaving the break-even interest rate unchanged. The ratio (R−P)/(T−R) is the same for the bundle as for any individual dimension.

Linkage only helps when dimensions are asymmetric — some dimensions have low defection temptation (high R−P relative to T−R) while others have high temptation. Bundling transfers sustainability from the low-temptation dimension to the high-temptation one.

**Multiproduct interaction warning (from Ch. 3):** Cheating on a multiproduct relationship brings the prospect of multiproduct retaliation, but also the temptation of multiproduct cheating simultaneously. These forces cancel if payoff structures are identical across products. Do not assume multiproduct relationships automatically sustain cooperation better than single-product relationships.

---

## Level 4: Third-Party Intervention and External Enforcement

### Explicit Contract Enforcement

**When to use:** Self-enforcement is not viable; parties cannot write credible unilateral punishment threats.

**Requirements:**
- Clear, verifiable specification of what cooperation and defection mean (cannot leave this ambiguous)
- Enforcement authority with jurisdiction and willingness to act
- Evidence mechanism: how will defection be proven?
- Proportionate remedy: what is the contracted consequence for defection?

**Limitation:** Many cooperation arrangements cannot be fully specified in a contract. "Do not undercut on price" is straightforward. "Maintain service quality at the level expected by our customers" is not. Contracts work for discrete, observable, attributable defections.

**Antitrust risk for firms:** Explicit agreements among competitors to cooperate on pricing or output are illegal in most jurisdictions. External enforcement through contract is not available for cartel arrangements — this is precisely why tacit self-enforcement mechanisms (Levels 1-3) are commercially important.

### Third-Party Mediator or Arbitrator

**When to use:** Parties cannot credibly commit to punishments themselves; a neutral third party has both authority and interest in the cooperative outcome.

**What the mediator provides:**
1. Focal point: the mediator defines what cooperation means (resolves the "clarity" prerequisite gap)
2. Verification: the mediator monitors compliance (resolves the "detection" gap)
3. Punishment: the mediator imposes consequences that neither party could credibly threaten unilaterally

**Mediator requirement:** The mediator must have either direct authority to impose consequences OR enough leverage over both parties (economic rewards, reputational influence, legal authority) that their judgment matters.

**Example:** US role at Camp David — neither Egypt nor Israel could credibly reward each other's cooperation. The US, with economic and military assistance to offer both, could.

### Regulatory Prohibition of the Defect Option

**When to use:** The defection option itself can be made illegal or structurally unavailable, eliminating the dominant strategy.

**How it works:** Rather than punishing defection after the fact, the regulation removes the defection choice from the game. Cigarette advertising ban (1968): TV advertising was a prisoners' dilemma for cigarette companies — each had to advertise because others did, even though collective advertising budgets were pure waste. The ban eliminated the defection option and actually benefited the firms by removing the arms race.

**Considerations:**
- Regulatory prohibition that benefits the regulated parties (the firms) may face regulatory capture concerns
- Prohibition must be designed to prevent new forms of defection from emerging (if TV advertising is banned, does billboard advertising become the new defection option?)
- Prohibition works best when the defection option has a clear legal definition

---

## Level 5: Ostrom Commons Governance

See [ostrom-commons-governance.md](ostrom-commons-governance.md) for full treatment.

**When to use:** Multiperson dilemma involving a shared resource; group is identifiable and can be organized; resource is local enough for community governance to be credible.

**Summary of when NOT to use Level 5 alone:**
- Completely anonymous large group (no community relationships)
- Resource spans jurisdictions in ways that prevent coherent local governance
- External authority will not recognize community governance rights (Principle 7 gap)
- Group is too heterogeneous for shared norms to develop

In these cases, Level 4 (external enforcement) may need to be the primary mechanism, with Level 5 principles used where possible to reduce enforcement costs.

---

## Mechanism Selection Matrix

| Situation | Recommended Level | Key reason |
|---|---|---|
| Ongoing bilateral relationship, observable, discount rate low | 1 (generous tit-for-tat) | Self-enforcing, no external requirement |
| Bilateral, trust depleted by prior defection, otherwise viable | 2 (escrow/promises) | Restart credibility |
| Bilateral, low direct cooperation value, strong reputational stakes | 3 (reputation/linkage) | Indirect enforcement |
| One-shot or short relationship, observable, specifiable defection | 4 (contract) | No shadow of future |
| Competitor coordination (antitrust-constrained) | 1 or 3 only (tacit) | Explicit agreements illegal |
| Shared resource, identifiable community, local resource | 5 (Ostrom) | Scale and community fit |
| Large anonymous group, no community structure | 4 (regulation) | Cannot self-govern |
