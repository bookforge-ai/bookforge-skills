# Virtual Strike Mechanics

Source: The Art of Strategy, Ch. 11 (pp. 321–323)

## The Problem with Real Strikes

A traditional strike (or lockout) imposes costs on:
1. Workers (lost wages)
2. Management (lost profits)
3. Customers (lost service)
4. Third parties (supply chain disruption, economic spillover)

The dock-worker lockout of 2002: the dispute involved ~$20 million in productivity enhancements. The lockout disrupted the U.S. economy by more than $10 billion. Collateral damage was 500 times the size of the dispute.

**The strike's logic is purely signaling:** each party needs to prove its cost of not having a deal is lower than the other believes. The collateral damage to third parties is pure waste — it serves no bargaining purpose.

## The Virtual Strike Mechanism

**Mechanism:**
- Workers continue working as normal (no service disruption).
- Employer continues producing as normal (no lost output for customers).
- All revenue during the virtual strike period is forfeited by the employer to a third party: government, charity, or customers (as free product/service).
- Workers receive no wages during the virtual strike period.

**Result:**
- Workers feel the same financial pain as in a real strike (no pay).
- Employer feels the same financial pain as in a real strike (no revenue — in practice, gross revenue is used rather than profit because profit is too easy to manipulate).
- Customers are unharmed.
- The BATNAs are unchanged relative to a real strike.
- The bargaining incentives are unchanged.

## Historical Precedents

### Jenkins Company Valve Plant — Bridgeport, CT (World War II)
- The U.S. Navy used a virtual strike to settle a labor dispute.
- Workers continued working; management forfeited profits.
- First documented industrial use of the mechanism.

### Miami Bus Strike (1960)
- Bus drivers staged a virtual strike.
- Buses ran on their normal schedule.
- Passengers rode for free — the revenue that would normally go to the transit authority was effectively given to riders.
- "Customers got a free ride, literally."

### Meridiana Airlines — Italy (1999)
- Italy's first virtual strike in aviation.
- Pilots and flight attendants worked their normal flights, unpaid.
- Meridiana donated all ticket revenue from virtually-struck flights to charities.
- Flights were not disrupted. No stranded passengers.
- The virtual strike worked as predicted — the threat was credible and management settled.

### Italy Transport Union (2000)
- 300 pilots participated in a virtual strike.
- The union forfeited 100 million lire (strike payments to charity).
- The union chose a medical device for a children's hospital as the recipient.
- Public relations benefit: instead of destroying consumer goodwill (as in NHL 2004-5), the virtual strike generated a positive story.

### NHL Lockout (2004–5)
- Management imposed a lockout rather than accepting virtual strike terms.
- The entire season was cancelled. No Stanley Cup awarded.
- Arena attendance took years to recover.
- This is the counterfactual: real disruption permanently destroys consumer demand and enterprise value. Virtual strikes avoid this.

## Implementation Design

### Revenue vs. Profit Forfeiture

In all four documented cases, management agreed to forfeit gross revenue, not profit. The reason: profit is a residual after costs, and management can shift costs or accounting choices to minimize reported profit during the dispute period. Gross revenue is harder to manipulate.

Workers forfeit wages. Employer forfeits gross revenue. The escrowed funds go to the third party.

### Third-Party Recipient Options
- **Government (tax authority):** Neutral, accepted by both parties, legally clean.
- **Charity:** Creates positive public relations; may be preferred by labor as a signal of strength.
- **Customers (free product/service):** Most consumer-visible option; aligns customer interests with quick resolution.

### Timing of Agreement

The right time to agree to a virtual strike mechanism is **before the real strike becomes imminent** — ideally as a contingency clause in the labor contract:

> "If contract negotiations fail to reach agreement by [date], both parties agree to enter a virtual strike arrangement beginning [date+n], under which [revenue escrow terms], until agreement is reached."

Agreeing in advance avoids the game-theoretic problem where proposing a virtual strike during a real dispute signals weakness or loss of resolve.

## Limitations and Complications

1. **Public relations benefit may backfire:** If a virtual strike generates positive PR for workers (charity donations, customer goodwill), management may prefer the reputational damage of a real strike — it is a known threat rather than an unknown one.

2. **Customer inconvenience as a strategic weapon:** Some real strikes are deliberately designed to inconvenience customers so they pressure management to settle. A virtual strike removes this pressure. Workers who rely on customer pressure as part of their strategy may not want to go virtual.

3. **Revenue measurement disputes:** Even gross revenue can be contested in industries with complex pricing, barter, intercompany transactions, or subscription models. The escrow mechanism must specify exactly what counts.

4. **Worker motivation during virtual strike:** Workers who work for nothing during a virtual strike must believe settlement is imminent and that the sacrifice is worth it. If the dispute drags on, worker participation may erode.

## Decision Rule: When to Propose a Virtual Strike

Propose a virtual strike mechanism when:
- The collateral damage to customers or third parties is large relative to the size of the dispute.
- The enterprise's long-term customer relationships or brand value are at risk from disruption.
- Both parties genuinely want to settle but need a credible signaling mechanism.
- You are the party whose BATNAs are better protected under a virtual arrangement than a real one.

Do not propose a virtual strike when:
- Customer pressure is a key part of your negotiating strategy.
- Management will use the virtual strike's PR benefit to undercut your leverage.
- The dispute is so bitter that neither party wants to cooperate even on the mechanism.
