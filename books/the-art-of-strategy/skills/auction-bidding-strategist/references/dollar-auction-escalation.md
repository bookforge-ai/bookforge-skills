# Dollar Auction and Escalation Traps

Mechanics of escalation auctions, war-of-attrition dynamics, exit criteria, and avoidance strategies.

---

## The Dollar Auction (Shubik's Escalation Game)

**Setup:**
- An auctioneer offers a $1 bill for sale
- Standard ascending-bid rules — highest bidder wins the dollar
- One twist: **both the highest AND second-highest bidder pay their bids**
- The second-highest bidder pays but receives nothing

**Why it escalates:**

Once two bidders are active at bids of, say, $0.50 (second place) and $0.60 (first place):

The second-place bidder calculates: "I am going to lose $0.50 and get nothing. If I bid $0.70, I am the high bidder and will likely win $1.00 for a net gain of $0.30. My alternative is to lose $0.50 for certain."

This logic is locally rational at every step. But:
- If the second-place bidder bids $0.70, the previous leader is now at $0.60 (losing $0.60 for nothing) and faces the same calculation
- Bidding continues past $1.00 because at that point both sides have sunk more than the prize value — they bid to minimize total loss, not to profit

**Classroom result:** Bids regularly exceed $5 for a $1 bill. The auctioneer profits; all active bidders lose.

**Structural cause:** The combination of (1) sunk cost logic creating a trap and (2) no coordination between the two trapped bidders. Neither can unilaterally escape without absorbing a loss, but continuing escalation makes both worse off.

---

## War of Attrition (Business Context)

**Definition:** A competitive situation where both parties spend resources over time, the winner is the last one standing, and both pay their costs regardless of who wins.

**Structure as an auction:**
- Each party "bids" the total financial loss they are willing to absorb
- The party with the higher "bid" (more loss tolerance) wins
- Both parties pay their costs while the contest lasts

**BSB vs. Sky (1989-1990, UK Satellite TV):**

- BSB held the official license; Sky launched without one using a different satellite
- Both firms bid for exclusive content (Hollywood movies, sports rights) at inflated prices
- After 18 months: combined losses of £1.5 billion
- Murdoch understood BSB wouldn't fold easily. BSB's strategy was to outlast Murdoch (who was personally exposed financially)
- Resolution: merger forced by mutual exhaustion and the government's desire to preserve one functioning firm

**Why both continued despite mounting losses:**
1. Sunk costs are irrelevant to future decisions — the £600M already lost was gone either way
2. The prize (monopoly over UK satellite TV with potential £2B/year revenue) justified continued spending at each marginal decision point
3. Each side overestimated their ability to outlast the other — overconfidence plus no coordination mechanism

**Lesson:** The willingness to absorb losses determined the merger split. Murdoch's deeper pockets and higher personal financial exposure (credibly committed him to either win or go bankrupt) gave him leverage.

---

## Exit Criteria for Wars of Attrition

**The decision at each period:**

Stay if: Expected value of winning × probability of winning > Additional cost of staying one more period

Exit if: Additional cost of staying > Expected benefit

**The problem with this calculation:** Both parties may simultaneously believe that the other is "about to fold." There is no consistency check — both sides can hold this belief simultaneously and both be wrong.

**Mathematical formulation (optional depth):**

In the continuous-time war of attrition model, the equilibrium condition for staying in is:

```
p(t) + q(t) ≤ 1
```

Where p(t) is your probability of winning if you stay one more unit of time and q(t) is the rival's probability of winning if they stay one more unit. When p(t) + q(t) > 1, the expected costs exceed benefits and at least one party should exit.

**Practical interpretation:** If your probability of outlasting the rival is less than the fraction of the prize value consumed by one more period of costs, exit immediately.

---

## Decision Framework: Should You Enter?

**Before entering a competitive spending contest:**

1. **Calculate your maximum total loss.** In a dollar auction / war of attrition, the worst case is not "I lose the bid" — it is "I continue to a point where I have spent far more than the prize is worth." What is your hard cap?

2. **Assess credibility of commitment.** Can you credibly pre-commit to a ceiling bid? If your competitor knows you will walk at $X, they may choose not to enter or to stop before $X. Pre-commitment reduces escalation.

3. **Is there a coordinated exit available?** In BSB/Sky, the merger was the coordinated exit. Can you engineer one? Tacit coordination (both sides signaling through bid levels that a certain price is the ceiling) may be possible in multi-round auctions.

4. **Is the prize truly winner-take-all?** Wars of attrition are worst when the prize is indivisible. If the prize can be split (spectrum licenses across geographic areas, as in FCC auctions), there may be an implicit deal available where each side wins something.

---

## Avoidance Strategies

**Strategy 1: Do not enter.** The best outcome in a dollar auction is to not play. If you can observe that the auction structure creates escalation (both top bidders pay), avoid it entirely.

**Strategy 2: Pre-commit publicly to a ceiling.** "We will not spend more than $X to win this." If your ceiling is credible and below the prize value, you can sometimes deter competitors from entering, since they know the auction will be rational (you won't escalate past $X even to "recover" sunk costs).

**Strategy 3: Change the game.** If you are in a competitive spending war, look for ways to change the structure — partnership, merger, exit deal, or third-party arbitration. The BSB/Sky resolution was a merger at the eleventh hour; the ability to absorb losses determined the split.

**Strategy 4: Once in, treat sunk costs as zero.** At every decision point, the question is purely: does the expected future value of continuing exceed the marginal future cost? Prior losses are irrelevant. This is psychologically hard but analytically mandatory.

**The dollar auction trap in disguise:**

Many real business situations have dollar-auction structure without being called auctions:
- Competitive hiring wars (both companies spend on counter-offers; one wins, both pay)
- Patent litigation (both sides pay legal costs; winner gets the patent)
- Price wars to drive out competition (both lose margin; the survivor gets the market)
- Bidding wars for key hires or sports stars (both franchises pay escalating offers; one wins)

Recognize the structure. Once you name it as a dollar auction or war of attrition, the decision framework above applies.
