# Winner's Curse Worksheet

Step-by-step presume-you've-won calculation for common-value auctions.

---

## When to Use This Worksheet

Use whenever:
- The item has a single underlying value that all bidders will eventually realize (oil leases, company acquisitions, rights auctions, Treasury bills)
- Your estimate of that value is uncertain and potentially noisy
- Winning would reveal that you estimated higher than all competitors

Signs you are in a common-value setting:
- The item's value depends on facts that will eventually be known to everyone (oil quantity underground, future cash flows of a company)
- Other bidders are professional market participants who have done similar analysis
- You are estimating the same reality as your competitors, not valuing something according to personal taste

---

## The Presume-You've-Won Diagnostic

**The core reframing:**

Do NOT ask: "What do I think this item is worth?"

DO ask: "If my bid is accepted / if I win this auction, what does that tell me about the item's actual worth?"

Winning is informative. In a competitive common-value auction, winning means you estimated higher than everyone else. That is systematic, not random. The winner's estimate is biased upward relative to the true value.

---

## Worksheet: Step-by-Step Calculation

### Step 1 — Establish Your Prior Range

What is your estimated range for the item's current value?

- Low estimate: $______
- High estimate: $______
- Distribution assumption: __________ (uniform is simplest; use if no reason to weight one end)
- Prior average value: $________ (for uniform: (low + high) / 2)

### Step 2 — Identify Your Value Multiplier

What improvement or extraction advantage do you bring over the baseline?

- Your multiplier: ________ (e.g., 1.5 = you can improve value by 50%)
- Naive maximum bid: Prior average × multiplier = $________

*This is what most people bid. It is usually wrong.*

### Step 3 — Apply the Presume-You've-Won Correction

Assume your bid B is accepted. Conditional on acceptance, the item's current value is somewhere between [Low, B], not [Low, High].

For uniform distribution: expected current value conditional on acceptance = (Low + B) / 2

The value you will realize from the item: Multiplier × (Low + B) / 2

For the deal to be at least breakeven, the value you realize must equal your bid:

```
Multiplier × (Low + B) / 2 = B
```

Solve for B:

```
Multiplier × Low / 2 + Multiplier × B / 2 = B
Multiplier × Low / 2 = B - Multiplier × B / 2
Multiplier × Low / 2 = B × (1 - Multiplier/2)
B = (Multiplier × Low / 2) / (1 - Multiplier/2)
```

Or equivalently:

```
B = (Multiplier × Low) / (2 - Multiplier)
```

*This is your maximum breakeven bid. Bid less than this to expect a profit.*

---

## Worked Example: ACME Acquisition

**Given:**
- Value range: $2M to $12M (uniform)
- Your multiplier: 1.5 (50% improvement)
- Low = $2M

**Naive bid:** Average ($7M) × 1.5 = $10.5M

**Why $10.5M is wrong:**
If accepted at $10.5M, current value is $2M to $10.5M (average $6.25M). Your improvement: 1.5 × $6.25M = $9.375M < $10.5M. Expected loss: $1.125M.

**Correct calculation using the formula:**

```
B = (1.5 × 2) / (2 - 1.5) = 3.0 / 0.5 = $6M
```

**Verify:** Bid $6M. If accepted, current value is $2M to $6M (average $4M). Improvement: 1.5 × $4M = $6M = bid. Exactly breakeven. ✓

**Practical bid:** Bid less than $6M to expect profit (e.g., $5M to expect $500K profit on average).

---

## Worked Example: Oil Lease Auction

**Given:**
- Your seismic survey estimates 1M to 5M barrels at $20/barrel net value
- Range: $20M to $100M
- Your drilling efficiency advantage: 1.1× (10% better than average)
- Low = $20M

**Naive bid:** Average ($60M) × 1.1 = $66M

**Winner's curse check:**

```
B = (1.1 × 20) / (2 - 1.1) = 22 / 0.9 = $24.4M
```

**Why this is so low:** The 10% improvement multiplier is barely above 1.0. In this case the winner's curse is severe — your advantage is too small to overcome the adverse selection from winning. You would need to bid below $24.4M to expect any profit.

**At $66M (naive bid):** If accepted, current value is $20M to $66M (average $43M). Your value: 1.1 × $43M = $47.3M << $66M. Expected loss: ~$18.7M.

**Lesson:** When your improvement multiplier is close to 1.0 (little differentiation from rivals), the winner's curse can make common-value auctions unprofitable at any reasonable bid. Consider whether to participate at all.

---

## The "Conditional on Acceptance" Intuition

Think of the seller as having private information about the true value. They accept your bid only when you are paying more than the item is worth to them. The act of acceptance is bad news.

This is the same structure as:
- A used car seller accepting your offer (they know more about the car's condition than you)
- A counterparty accepting your M&A price (they know more about the company's liabilities)
- A homeowner accepting your offer in a falling market (they know more about structural issues)

In every case: if they said yes, ask yourself why. The presume-you've-won analysis forces you to answer that question before, not after, committing.

---

## Common-Value Adjustments in English/Japanese Auctions

In ascending auctions with common values:

1. **Each dropout is a signal.** When a competitor lowers their hand at price P, they are revealing that their private estimate is approximately P (or they updated their estimate downward to P). This is information you did not have before.

2. **Update continuously.** As more bidders drop out at prices lower than you expected, revise your estimate of the common value downward. Early mass dropouts are stronger signals than gradual ones.

3. **The last surviving competitor's dropout price is the strongest single signal.** The price at which the second-to-last bidder drops out tells you the second-highest private estimate. This is valuable: if you had estimated $100K but the second-to-last competitor drops at $70K, your estimate should move toward $70K-$80K range.

4. **In a Japanese auction, this information is more complete.** You know every dropout price, not just the final one. Use all of them as a Bayesian update on the common value.
