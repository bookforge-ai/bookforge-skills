# Bid Shading Formula

Derivation of the optimal bid in first-price sealed-bid (and Dutch) auctions, with worked examples.

---

## Setup

**Assumptions for the symmetric baseline:**
- N bidders total (including yourself)
- Each bidder's value is drawn independently from a uniform distribution [0, 100] (or equivalently [0, V])
- All bidders know N and the distribution; each knows only their own value
- Symmetric equilibrium: all bidders use the same bidding function

---

## Deriving the Formula

**Step 1 — Expected payment in Vickrey equals bid in first-price (Revenue Equivalence)**

Revenue equivalence theorem guarantees that in equilibrium, both auctions yield the same expected payment from the winner. In a Vickrey auction with N symmetric bidders and uniform [0, V] values, the winner (highest-value bidder) pays the expected value of the second-highest valuation given that they have the highest.

**Step 2 — Compute the expected second-highest value conditional on having the highest**

If your value is v (and you have the highest value), the other N-1 bidders all have values below v. Their values are i.i.d. uniform [0, v]. The expected maximum of N-1 uniform [0, v] draws is:

```
E[max of N-1 uniform(0,v)] = v × (N-1)/N
```

**Step 3 — By revenue equivalence, your optimal first-price bid equals your expected payment in Vickrey**

```
Optimal bid = v × (N-1)/N
```

This is the optimal symmetric bid. Every bidder using this function produces a Nash equilibrium in the first-price auction.

---

## The Formula in Practice

**Formula:**
```
Bid = V × (N - 1) / N
```

Where:
- V = your true value (walkaway number)
- N = total number of bidders (including you)

**Worked examples:**

| Your Value | Bidders | Formula | Optimal Bid | Shading Amount |
|-----------|---------|---------|-------------|---------------|
| $100 | 2 | 100 × 1/2 | $50 | $50 |
| $100 | 3 | 100 × 2/3 | $66.67 | $33.33 |
| $100 | 4 | 100 × 3/4 | $75 | $25 |
| $100 | 5 | 100 × 4/5 | $80 | $20 |
| $100 | 10 | 100 × 9/10 | $90 | $10 |
| $60 | 2 | 60 × 1/2 | $30 | $30 |
| $60 | 4 | 60 × 3/4 | $45 | $15 |
| $200K | 3 | 200K × 2/3 | $133K | $67K |
| $1M | 5 | 1M × 4/5 | $800K | $200K |

---

## Adjustments for Non-Uniform Distributions

The formula V × (N-1)/N is exact only when competitor values are uniform [0, V]. In practice:

**When competitor values cluster near your value (competitive setting):**
- True optimal bid is closer to V than the formula suggests
- Shade conservatively (perhaps 5-10% off V rather than the formula's amount)
- Example: real estate competitive offers where all bidders are serious buyers cluster near market price

**When competitor values are sparse / few strong bidders:**
- Formula may understate how much to shade
- With only 1-2 serious competitors in a wide value range, shade more aggressively

**Rule of thumb for non-uniform settings:**
Use the formula as a floor — never bid above V × (N-1)/N in a first-price auction. Adjust upward toward V only when the distribution of competitor values is highly concentrated near your own.

---

## Why Bidding Your True Value Is Always Wrong in First-Price

**Algebraic proof:**

Suppose you bid exactly your value V. If you win, you pay V and profit = V - V = $0.

Now consider bidding B = V - ε for small ε > 0. You still win whenever your value is the highest (which is all that matters, since V is still your value). But now you pay B = V - ε and profit = V - (V - ε) = ε > $0.

Therefore bidding V is strictly dominated by bidding V - ε. QED.

**Bidding above V is even worse:** If you win, you pay more than V and profit < 0. This is dominated by not bidding at all.

---

## Revenue Equivalence Theorem

**Statement:** Under private values, symmetric bidders, and risk-neutrality, all four canonical auction formats (English, Japanese, Vickrey, Dutch/first-price) yield the same expected revenue to the seller and the same expected payment from the winner.

**Why it holds:** Bidders' strategies adjust to perfectly offset changes in format rules. If the seller imposes a buyer's premium, bidders shade down their bids proportionally. If the seller switches from second-price to first-price, bidders shade their bids down by exactly the right amount. The expected payment stays constant.

**Practical implication for sellers:** You cannot systematically increase revenue by choosing a different standard auction format. You can increase revenue by:
- Setting a binding reserve price (excludes low-value bidders, raises payment from the winner)
- Attracting more bidders (increases N, which by the formula tightens bid shading)
- Designing formats that reduce common-value uncertainty (reducing the winner's curse discount)

**Practical implication for bidders:** If you are in a format-equivalent auction, focus on getting your value estimate right, not on outguessing the format. The format doesn't change your expected payment.
