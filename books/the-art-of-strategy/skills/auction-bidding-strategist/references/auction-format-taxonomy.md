# Auction Format Taxonomy

Full mechanics and decision flows for the five canonical auction formats.

---

## English Auction (Ascending, Open)

**Mechanics:**
- Auctioneer calls out successively higher prices
- Bidders signal participation (raise paddle, call out bid)
- Anyone can drop out at any time; once dropped, can re-enter in some implementations but typically cannot
- Auction ends when only one bidder remains
- Winner pays the price at which the last competitor dropped out (approximately the second-highest valuation)

**Strategic optimal:** Bid (stay in) until price reaches your true value; drop at that price.

**Information revealed:** Partial. In an English auction, you see others' bids but not their private valuations — a bidder might be silent and then make a surprise late bid. You know what others bid, but not how high they would have gone.

**Common value relevance:** High. In English auctions with common values, each dropout reveals a signal about the common value. Update your estimate as bidders leave.

---

## Japanese Auction (Clock Rising, Simultaneous Commitment)

**Mechanics:**
- All bidders begin with hands raised (or button pressed)
- A clock rises from a starting price; all active bidders remain "in" while their hand is raised
- A bidder drops out by lowering their hand; this is irreversible
- Auction ends when only one bidder remains
- Winner pays the price at which the last other bidder dropped out

**Strategic optimal:** Keep hand raised until clock reaches your true value; lower hand at exactly that price.

**Difference from English:** Full transparency. In a Japanese auction, you know exactly how many competitors remain at every price point and the exact prices at which each drops out. There are no hidden bids or surprise late entrants.

**Information revealed:** Complete. Everyone knows exactly when every bidder dropped out and at what price. This is the most information-rich ascending auction format.

**Strategic equivalence with English:** Under private values, the extra information is irrelevant — your value is independent of what others think. Both auctions produce the same outcome: winner with highest value pays the second-highest valuation.

---

## Vickrey Auction (Second-Price Sealed-Bid)

**Mechanics:**
- All bidders submit a sealed bid simultaneously
- Bids are revealed; highest bid wins
- Winner pays the second-highest bid (not their own)
- Other bidders pay nothing

**Strategic optimal:** Bid your exact true value. This is the unique dominant strategy — it is best regardless of what others bid and regardless of how many others are bidding.

**Dominant strategy proof:**

Let your value = V. Consider any alternative bid B ≠ V.

Case 1: Highest rival bid H > V. You lose with bid V; you also lose with bid B unless B > H, in which case you "win" but pay H > V — a loss. Bidding V weakly dominates.

Case 2: Highest rival bid H < V. You win with bid V and pay H < V (profit). If B > H you also win and pay H (same outcome). If B < H you lose (forfeited profit). Bidding V weakly dominates in this case too.

Case 3 (the decisive case): V < H < V... wait, this is impossible if H < V is case 2. The case that makes B ≠ V strictly worse: B < V and B < H < V → you lose with B, win with V (paying H < V), profit = V - H > 0. Bidding V strictly dominates B.

Symmetric argument shows bidding above V is also dominated. Therefore V is the unique dominant strategy.

**Real-world applications:** Treasury bills (uniform price variant), Google AdWords second-price variant, some procurement auctions.

---

## Dutch Auction (Descending Clock)

**Mechanics:**
- Clock starts at a high price and descends
- First bidder to stop the clock wins at that price
- All other bidders pay nothing and receive nothing
- (Aalsmeer Flower Auction: 14 million flowers/day, 160-acre facility, descending clock)

**Strategic optimal:** Determine your bid before the auction begins (as if writing a sealed bid). When the clock descends to that price, stop it immediately.

**Why strategic equivalence with sealed-bid first-price:**
- Your "bid" in a Dutch auction is the price at which you plan to stop the clock
- This plan is made in advance, without seeing others' bids
- The person who plans to stop at the highest price (has the highest sealed bid) wins
- The winner pays the price at which they stopped (their "bid")
- Identical to first-price sealed-bid in every strategically relevant sense

**The one difference:** In a Dutch auction, you know you've won when the clock stops. In a first-price sealed-bid auction, you find out later. But per the "bid as if you've won" principle, in a sealed-bid auction you should already be assuming you've won when computing your bid. This removes the only apparent difference.

---

## First-Price Sealed-Bid Auction

**Mechanics:**
- All bidders submit a sealed bid simultaneously
- Bids revealed; highest bid wins
- Winner pays their own bid
- Others pay nothing

**Strategic optimal:** Shade your bid below your true value. The amount of shading depends on how many competitors you expect.

**Bid-shading formula (symmetric private values, uniform distribution [0, V]):**

```
Optimal Bid = V × (N-1) / N
```

N = total number of bidders (including yourself).

| N (bidders) | Formula | Fraction of V to bid |
|-------------|---------|---------------------|
| 2 | V × 1/2 | 50% |
| 3 | V × 2/3 | 67% |
| 4 | V × 3/4 | 75% |
| 5 | V × 4/5 | 80% |
| 10 | V × 9/10 | 90% |
| 20 | V × 19/20 | 95% |

**Intuition:** With more competitors, the probability that you have the highest value is lower, so you must bid closer to your value to avoid being outbid. With fewer competitors, you can shade more aggressively because the next-highest bidder is likely to have a lower value than yours.

**Why never bid your true value in first-price:** If you win by bidding V, you pay V and profit exactly $0. You can always do better by bidding slightly less — you still win (since others bid even less), but you pay less. Bidding V is weakly dominated by V - ε for any ε > 0.

---

## Buyer's Premium (Rule Modification)

**What it is:** Auction houses (Sotheby's, Christie's) add a percentage premium to the winning bid. The buyer pays their bid plus, say, 20% on top. A $1,000 winning bid becomes a $1,200 payment.

**Who actually bears the cost:** The seller, not the buyer.

**Why:** Rational bidders know the premium exists. If your true value is $1,200 (the total amount you're willing to spend), you will bid $1,000 (knowing that $1,000 × 1.2 = $1,200). The hammer price falls in proportion to the premium. The winner's total payment stays the same. The auction house's cut comes from what would otherwise be the seller's proceeds.

**Generalizable principle (Revenue Equivalence):** Any change to the payment rule that bidders can anticipate and incorporate will be perfectly offset by corresponding changes in bidding behavior. The seller's expected revenue remains unchanged. Players adapt their strategies to undo rule changes.
