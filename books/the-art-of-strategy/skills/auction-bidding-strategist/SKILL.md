---
name: auction-bidding-strategist
description: "Apply the complete game-theoretic auction framework to determine the optimal bid in any auction format. Use this skill when a user is preparing to bid in an English (ascending) auction, a Japanese auction, a Vickrey (second-price sealed-bid) auction, a Dutch (descending-clock) auction, or a standard sealed-bid first-price auction, and wants the game-theoretically correct strategy rather than guesswork. Triggers include: user is deciding how much to bid in a competitive tender, procurement auction, real estate auction, eBay auction, spectrum license auction, or corporate acquisition; user is worried about overbidding and wants to know how to set a ceiling; user suspects they may be falling into the winner's curse — winning but regretting the price paid; user must classify whether the auction involves private values (each bidder's value is independent) or common values (the item has a single underlying value that all bidders are estimating), because the correct strategy differs sharply between the two; user is evaluating whether to participate in a dollar auction, bidding war, or war-of-attrition-style competitive spending contest and wants to know when to stop or avoid; user needs to shade a bid below their true value in a sealed-bid first-price format and wants the formula; user is designing an auction and wants to know which format will yield more seller revenue; user is bidding in multiple simultaneous auctions and needs to think across the games. This skill does NOT cover multi-round negotiation without a defined auction structure (use a negotiation skill instead), combinatorial auctions with complex package bids, or procurement auctions requiring cost estimation."
version: 1
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [10]
tags: [game-theory, auctions, bidding, competitive-strategy, winner-curse]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of the auction situation: format, number of bidders, your estimated value, uncertainty about the item's true value, and any known facts about competitors"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes auction context in text; agent produces bid recommendation and strategy plan"
discovery:
  goal: "Classify the auction format and value type, then apply the correct bidding rule — producing an explicit bid recommendation, the reasoning behind it, and the traps to avoid"
  tasks:
    - "Identify the auction format: English, Japanese, Vickrey, Dutch, or sealed-bid first-price"
    - "Classify value type: private values (independent), common values (shared underlying value with noisy estimates), or mixed"
    - "Determine the bidder's true value (walkaway number) by asking for all value components"
    - "Apply the format-specific optimal bidding rule"
    - "Apply the winner's curse diagnostic in common-value settings: compute the bid conditional on winning (presume-you've-won analysis)"
    - "Identify whether the situation is a dollar auction / war of attrition, and compute the exit threshold"
    - "Flag revenue equivalence implications if the user is on the seller side or comparing formats"
    - "Deliver: recommended bid, bid rationale, traps to avoid, and format-equivalence notes"
  audience: "Business strategists, procurement managers, real estate buyers, corporate development teams, product managers bidding for ad inventory, investors in M&A situations, and anyone entering a structured competitive bidding process"
  when_to_use:
    - "User is preparing a bid and wants the game-theoretically optimal number"
    - "User has won an auction before and regretted it — diagnosing and correcting winner's curse"
    - "User is unsure whether to shade their bid below their value or bid their true value"
    - "User is deciding whether to enter or continue in a bidding war or competitive spending contest"
    - "User is designing an auction mechanism and wants to understand revenue equivalence"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Auction Bidding Strategist

## When to Use

Use this skill whenever a strategic situation has the structure of an auction: one or more items up for bid, a defined rule for who wins, and a defined rule for how much the winner pays. The framework applies far beyond the art auction room — procurement tenders, corporate acquisitions, spectrum licenses, eBay, online ad auctions, and competitive employment offers are all auctions.

**The core discipline of auction strategy: the right bid is not your value. It depends on the format.**

In a second-price (Vickrey) auction, bidding your true value is the dominant strategy. In a first-price sealed-bid auction, bidding your true value guarantees zero profit at best. Getting the format wrong is the single most common and costly bidding error.

**This skill applies when:**

- A defined bidding format governs who wins and how much they pay
- You need an explicit numerical recommendation, not just direction
- The situation involves information asymmetry, common-value uncertainty, or escalation risk

**This skill does NOT apply to:**

- Open-ended negotiations without a structured bid mechanism (use a negotiation skill)
- Complex package-bidding combinatorial auctions (these require specialized integer programming)
- Procurement situations where cost uncertainty dominates — you must first estimate your own cost before bidding strategy applies

---

## Context and Input Gathering

### Required (ask if missing)

- **Auction format:** Is this English (ascending bids, open), Japanese (simultaneous hand-raising, clock rises), Vickrey (sealed, winner pays second-highest bid), Dutch (descending clock, first to stop wins), or standard sealed-bid first-price (sealed, winner pays their own bid)?
  -> Ask: "How does the auction work mechanically — is it open or sealed, does price go up or down, and who pays what if they win?"

- **Your true value:** What is the maximum you would pay and still be satisfied? This is your walkaway number — the price at which you are indifferent between winning and losing.
  -> Ask: "At what price would you be completely indifferent between winning and walking away? What components make up that number — resale value, strategic value, avoided cost if rival wins?"

- **Value type:** Does each bidder's value depend only on their own use (private values), or does the item have an underlying worth that everyone will eventually realize (common values)?
  -> Ask: "Is this an item whose value to you is independent of what others think — like a gift for yourself — or is it an item whose true worth is unknown and all bidders are estimating the same underlying reality, like an oil lease or a company?"

- **Number of bidders:** How many competitors are expected? This affects the bid-shading formula in first-price auctions.

### Useful (gather if present)

- Competitor value estimates (even rough ranges)
- Whether bids are observable or secret during the auction
- Whether this is a one-shot bid or a multi-round process
- Whether multiple items are for sale simultaneously
- Whether the auction is structured as a war of attrition (outlasting, not outbidding)

---

## Execution

### Step 1 — Classify the Auction Format

**Why:** The optimal bidding rule differs sharply across formats. Applying the wrong rule — for example, bidding your true value in a first-price sealed-bid auction — produces zero profit even when you win. One minute of format classification prevents systematic overbidding or underbidding.

**The four canonical formats and their strategic equivalences:**

| Format | Mechanism | Strategic twin |
|--------|-----------|---------------|
| English (ascending) | Open bidding; price rises; last bidder wins | Strategically equivalent to Vickrey |
| Japanese (clock rising) | All hands raised; clock rises; drop out by lowering hand; irreversible | Strategically equivalent to English |
| Vickrey (second-price sealed) | Sealed bids; highest wins; pays second-highest bid | Strategically equivalent to English/Japanese |
| Dutch (descending clock) | Price starts high, falls; first bidder to stop clock wins at that price | Strategically equivalent to first-price sealed-bid |
| First-price sealed-bid | Sealed bids; highest wins; pays their own bid | Strategically equivalent to Dutch |

**Key equivalence pair 1 — English ≈ Vickrey ≈ Japanese:**
All three produce the same outcome: the highest-value bidder wins and pays the second-highest valuation. In English/Japanese formats, the auction ends when the second-to-last bidder drops out at their value. In Vickrey, the winner pays the second-highest bid, which equals the second-highest valuation (since everyone bids truthfully).

**Key equivalence pair 2 — Dutch ≈ First-price sealed-bid:**
Both require the bidder to commit to a price before knowing who else has bid and what they offered. The strategic decision is identical: choose a price that maximizes expected profit by balancing the gain from winning against the risk of losing.

---

### Step 2 — Determine Your True Value (Walkaway Number)

**Why:** Every format's optimal bid is anchored to your true value — either you bid it directly (Vickrey/English) or you shade it (first-price). Without an accurate walkaway number, the downstream bid calculation is wrong regardless of how carefully the formula is applied.

**Components of true value (add all that apply):**

- Direct use value: what the item is worth to you in use
- Strategic option value: premium for keeping the item out of a rival's hands
- Resale value: expected liquidation price if you later sell
- Excitement or prestige premium: if present, include it explicitly so you can manage it later

**The walkaway test:** "At this exact price, I am completely indifferent between winning and losing. One dollar more and I would rather not win. One dollar less and I am happy to win." Only one number passes this test. That number is your value.

**Common error:** Treating your value as a ceiling you hope not to reach, rather than the precise indifference point. This leads to soft dropping in English auctions — dropping out before your true value — and forfeiting wins that would have been profitable.

---

### Step 3 — Apply the Format-Specific Optimal Bidding Rule

**Why:** Each format has a provably optimal bid derived from game theory. Using the correct rule is not a refinement — it is the difference between a profitable bidding strategy and one that either leaves money on the table or produces regret.

#### English Auction (Ascending, Open)

**Rule:** Stay in the bidding until the current price exceeds your true value. Drop out the moment the price would require you to pay more than your walkaway number.

**Why this is optimal:** Dropping earlier forfeits wins you would have valued. Staying later means you would pay more than the item is worth to you. The optimal exit point is exactly at your value, which is a dominant strategy — no information about competitors changes it.

**Bidding increment issue:** If increments are coarse (bidding goes in units of $10 and your value is $95), be aware that the last bid you make (at $90) means someone else can win at $100. Account for whether strategic endgame matters near your value ceiling.

**In common-value settings, modify this rule with Step 5 (winner's curse correction) before applying.**

#### Japanese Auction (Clock Rising, Simultaneous Drop-Out)

**Rule:** Keep your hand raised until the clock reaches your true value. Lower your hand at that exact price.

**Why this is equivalent to English:** The Japanese format provides more information — you know exactly when each competitor drops out and at what price. In a private-value setting, this extra information is irrelevant to your strategy (your value is independent of what others think). In a common-value setting, seeing where others drop out is useful signal that should update your estimate before the auction ends.

**Common-value modification:** If others drop out unusually early, this signals the true value may be lower. Update your estimate downward before proceeding.

#### Vickrey Auction (Second-Price Sealed-Bid)

**Rule:** Bid your exact true value. Not a penny more, not a penny less.

**Why this is a dominant strategy (proof by dominance):**

Consider two cases where bidding below your true value ($50 instead of $60) matters:

1. Highest rival bid is above $60: You lose either way. No difference.
2. Highest rival bid is below $50: You win and pay that rival bid either way. No difference.
3. Highest rival bid is between $50 and $60 (say, $53): If you bid $60, you win and pay $53 — a profit of $7. If you bid $50, you lose. Since your value is $60, winning at $53 is desirable.

The only case where the two bids differ is case 3 — and in that case, bidding your true value is strictly better. The same argument shows bidding above your value is also dominated. Therefore bidding your true value is the unique dominant strategy. You do not need to know how many competitors there are or what they are bidding.

**eBay proxy bidding:** eBay's proxy system approximates a Vickrey auction. Bid your true value as your proxy. The system will only spend up to what is needed to stay ahead. **Exception:** If early bidding reveals information to other bidders about the item's quality or your willingness to pay, sniping (submitting your proxy at the last moment) prevents competitors from updating their estimates and bidding higher. Snipe when your bid would credibly signal higher value to others who might then raise their own valuations.

#### First-Price Sealed-Bid Auction (and Dutch Auction)

**Rule:** Shade your bid below your true value. **Never bid your true value** — this guarantees zero profit even if you win. Shade the bid to balance expected profit against the risk of losing to another bidder.

**The bid-shading formula (symmetric private values, N bidders, values uniform 0–V):**

```
Optimal Bid = V × (N-1) / N
```

Where V is your value and N is the number of bidders (including yourself).

**Examples:**
- 2 symmetric bidders, value = $100: Bid $50 (bid half your value)
- 3 symmetric bidders, value = $100: Bid $67
- 4 symmetric bidders, value = $100: Bid $75
- 10 symmetric bidders, value = $100: Bid $90

**Intuition:** With more competitors, shading less is optimal because the risk that someone else outbids you rises. With fewer competitors, shade more to capture profit margin.

**The "bid as if you've won" principle (always apply in first-price/Dutch):**

When writing down your bid, assume all other bidders are below you. Then ask: given that I am the highest bidder, what is my best bid? This is equivalent to asking: "If I had a confederate who could only lower my bid after I've won, what amount would I instruct them to lower it to?" The answer to that question is the bid you should write down from the start.

**Why this works:** If your original bid would have lost, the confederate's adjustment doesn't matter — you lose either way. If your original bid wins, the confederate lowers it to the same amount you would have written in the first place. The two approaches produce identical results, so you might as well bid the shaded amount from the start.

---

### Step 4 — Classify Private vs. Common Values and Apply Accordingly

**Why:** The English/Japanese/Vickrey dominant strategy of "bid your value" is only valid in private-value settings. In common-value settings, your naive estimate is systematically biased upward — the winner's curse — and the rules must be modified. Failing to identify the value type leads to predictable losses.

**Private values:** Your value is independent of what others think. Signed memorabilia, items for personal use, branded goods where you care only about your own use. Each bidder's value is their own, unaffected by others' valuations.

**Common values:** The item has a single underlying value that all bidders will eventually realize. Examples: offshore oil lease (the oil quantity is what it is, regardless of who extracts it), corporate acquisition (the company is worth what it will generate, regardless of buyer), real estate in a liquid market, Treasury bills. Each bidder has a private estimate of the same common value.

**Mixed:** Most real situations have both components. An oil company that is better at extraction has private value (the efficiency premium) plus common value (the oil itself).

**In common-value settings, jump to Step 5 before computing any bid.**

---

### Step 5 — Apply the Winner's Curse Diagnostic (Common Values)

**Why:** In a common-value auction, the bidder with the highest private estimate wins. But winning means you estimated higher than everyone else — which means your estimate is systematically above the true value. Ignoring this produces what the book calls the winner's curse: you win, but you pay more than the item is worth. The correction is mandatory, not optional.

**The diagnostic question (presume-you've-won analysis):**

Do not ask: "What do I think this is worth?" Ask instead: "Conditional on my bid winning — meaning everyone else estimated lower — what is the item actually worth?"

**Worked example (ACME acquisition):**

- Your due diligence places ACME's current value uniformly between $2M and $12M (average: $7M)
- Your operational expertise can increase value by 50%
- Naive bid: Average value $7M × 1.5 = $10.5M

**Why $10.5M is wrong:** If you offer $10.5M and they accept, the company is worth between $2M and $10.5M today (average: $6.25M). Your 50% improvement brings it to $9.375M — below what you bid. Accepting your $10.5M offer is bad news, not good news.

**Correct procedure:**
1. Presume your offer will be accepted
2. Conditional on acceptance, recompute the expected value
3. Find the bid B such that: (expected value conditional on acceptance) × (your improvement multiplier) = B

**For ACME:** Bid B. If accepted, current value is between $2M and B (average: (2+B)/2). Your 1.5× improvement: 1.5 × (2+B)/2 = B. Solve: 1.5(2+B)/2 = B → 1.5 + 0.75B = B → 1.5 = 0.25B → B = $6M.

At $6M, if accepted, expected current value = $4M, improved to $6M — exactly breakeven. Bid less than $6M to profit; never bid above $6M without accepting expected losses.

**General rule for common-value auctions:** Your bid must account for the adverse selection implicit in winning. Winning is informative: it tells you that everyone else estimated lower. That information should reduce your bid, not be ignored.

**In English/Japanese auctions with common values:** Observe where competitors drop out — this reveals their private estimates of the common value. Use each dropout as a downward signal. If many competitors drop out early, revise your own estimate down before the auction ends.

---

### Step 6 — Recognize and Escape the Dollar Auction Trap

**Why:** Some competitive bidding contests have a structure where sunk costs create escalation beyond rational stopping points. The dollar auction (Shubik's escalation game) illustrates a situation where both top bidders pay, creating a trap with no natural exit once entered. Recognizing this structure before entering — not after — is the key decision.

**The dollar auction structure:**

An auctioneer sells a dollar bill. Highest bidder wins and pays their bid. But the second-highest bidder also pays their bid and gets nothing. Bids start at pennies. Once two bidders are active, the second-place bidder always has an incentive to bid one increment higher (spend a bit more to win something rather than lose and pay). This logic escalates indefinitely — bidding has reached $5 for a $1 bill in classroom experiments.

**Why escalation is rational at each step but catastrophic in aggregate:** At each moment, the bidder in second place calculates: "I can either lose $X (my current bid) and get nothing, or bid $X+1 and have a chance at the $1 prize." This marginal logic is sound, but the cumulative cost is unbounded.

**War of attrition (BSB vs. Sky UK):** The same structure appears in competitive spending wars. BSB and Murdoch's Sky TV both lost £1.5 billion in their satellite TV competition before merging. Each side rationally stayed in because (a) the prize was enormous and (b) sunk losses were irrelevant to future decisions. But both overestimated their ability to outlast the other.

**Exit threshold for war of attrition:**

The rational time to continue is while the expected value of winning exceeds the cost of staying in one more period. But both sides cannot both rationally believe they will outlast the other — overconfidence is the structural cause of catastrophic losses.

**Decision rules:**
1. **Before entering:** Calculate the maximum total you can lose in a competitive spending contest. If that maximum exceeds your capacity, do not enter regardless of the prize's appeal.
2. **Once entered:** Treat sunk costs as irrelevant (they are). Decide each period based only on: does the additional cost of staying in one more period justify the probability of winning the prize? If no, exit immediately.
3. **The best strategy in a dollar auction:** Do not play. The second-best strategy is to commit credibly before the auction that you will bid only up to a fixed ceiling and communicate this to competitors. A credible ceiling makes the auction unprofitable for both and may deter entry.

---

### Step 7 — Simultaneous Multi-Item Auctions (FCC Spectrum Logic)

**Why:** When multiple items are auctioned simultaneously and bidders value portfolios of items, single-item bidding rules produce systematically wrong results. The value of winning item A depends on whether you also win item B. Bidding on each independently ignores this interdependence and produces overbidding or underbidding.

**The FCC simultaneous auction design:** The FCC solved the sequential auction problem (bidding on NY first, then LA, with budget constraints carrying over) by auctioning all licenses simultaneously with open rounds. Bidders could shift bids across items between rounds. This allows the market to aggregate information about cross-item values.

**Key insight for multi-item strategy (AT&T/MCI example):**

When two bidders compete for two items and both can win both, the dominant bidder should recognize that the true cost of winning both items is higher than the sum of winning prices — because aggressively pursuing both items forces prices up on both. The cost of winning the second item may include the incremental price increase it caused on the first.

**Optimal multi-item strategy:**
- Identify which items form your target portfolio and what portfolio value is
- If the combined cost of winning all items exceeds portfolio value, consider deliberately winning only a subset (even the less-preferred item at a lower price) and let the rival win the remainder at a higher price
- Do not bid your full value on all items simultaneously — calculate the marginal value of each additional item conditional on already winning the others

---

### Step 8 — Deliver the Bid Recommendation

Structure your output:

**Auction format identified:** [Format name and strategic equivalent]

**Value type:** [Private / Common / Mixed, with rationale]

**True value (walkaway number):** [Amount and components]

**Recommended bid:** [Explicit number or formula applied to their stated value]

**Bid rationale:** [Which rule was applied and why; key calculation shown]

**Winner's curse adjustment (if common values):** [Revised estimate conditional on winning, and resulting corrected bid]

**Traps to avoid:** [Top 1-2 risks in this specific situation — overbidding, escalation, value type misclassification]

**Format equivalence note (if relevant):** [If the user is comparing formats or could choose, note revenue equivalence implications]

---

## Key Principles

**Format determines the rule.** The bid that is optimal in a Vickrey auction is catastrophic in a first-price sealed-bid auction. Identify the format before computing anything.

**Revenue equivalence theorem.** Under private values and symmetric bidders, English, Japanese, Vickrey, Dutch, and first-price sealed-bid auctions all yield the same expected seller revenue and the same expected winner — just through different mechanisms. This is why changing the surface rules of a game does not change outcomes: bidders adjust their strategies to offset exactly.

**In Vickrey, bid your value exactly.** This is the only setting where true-value bidding is a dominant strategy. The dominant strategy proof means you do not need to know anything about other bidders to confirm this.

**In first-price, shade your bid.** The formula is V × (N-1)/N under symmetric uniform beliefs. More competitors mean less shading; fewer competitors mean more shading.

**In common-value auctions, winning is bad news.** Winning means everyone else estimated lower. Update your estimate downward conditional on winning. The presume-you've-won diagnostic is the core correction tool.

**In dollar auctions and wars of attrition, the best time to exit was before entering.** Once in, sunk costs are irrelevant. Exit when the marginal continuation cost exceeds the marginal expected benefit — and be honest about the probability that the other side exits first.

**Buyer's premiums are borne by sellers, not buyers.** If an auction house adds a 20% buyer's premium, rational bidders adjust by bidding 1/1.2 of their true value. The hammer price falls enough to leave the winning bidder's total payment unchanged. The auction house's take comes out of the seller's proceeds.

---

## Examples

### Example 1: Vickrey Auction (Corporate Software License)

**Setup:** A government agency is auctioning a multi-year software contract to the lowest bidder. This is a second-price procurement auction (winner pays the second-lowest bid). Your cost to deliver is $800K. You estimate one strong competitor at roughly $700K-$900K.

**Apply the rule:** In a Vickrey (second-price) procurement auction, the dominant strategy is to bid your true cost exactly. Bid $800K.

**Why:** If you win, you pay the second-lowest bid (competitor's bid). If competitor bids $750K, you lose — correct, because they can do it cheaper. If competitor bids $850K, you win and get paid $850K for $800K work: $50K profit. Bidding below $800K (say $750K) might win but you'd be paid $750K or less for $800K work — a guaranteed loss. Bidding above $800K (say $850K) only changes the outcome if the competitor bids between $800K-$850K, in which case you lose wins you would have profited from.

**Recommended bid:** $800K (your true cost).

### Example 2: First-Price Sealed-Bid (Real Estate Offer)

**Setup:** You are in a competitive offer situation on a house. True value to you: $620,000. You believe there are 3 competing bidders, all with values roughly similar to yours.

**Apply the formula:** N = 4 (you plus 3 others). Optimal bid = $620,000 × (4-1)/4 = $620,000 × 0.75 = $465,000.

**Sanity check:** This seems very aggressive shading. In practice, real estate values are not uniformly distributed across [0, V] — they cluster near the asking price. The formula is exact only under symmetric uniform beliefs. Adjust: if you believe competing values cluster around $580K-$620K, the effective range is narrow and shading should be modest (perhaps $595K-$605K). The formula gives a floor on shading; judgment about competitor value concentration adjusts from there.

**Recommended bid:** $600,000 (approximately V × 0.97, given tight competitor value clustering) with a clear ceiling at $620,000.

### Example 3: Winner's Curse Correction (Company Acquisition)

**Setup:** Your team estimates a target company is worth $50M-$90M today. You can improve operations by 40%. You are in a sealed-bid acquisition process.

**Naive calculation:** Average value $70M × 1.4 = $98M. "I can bid up to $98M."

**Winner's curse analysis:** If accepted at $98M, current value is between $50M and $98M — average $74M. Your 40% improvement: $74M × 1.4 = $103.6M. Profit: $103.6M - $98M = $5.6M. Still slightly positive.

**Find the breakeven bid B:** Accepted at B → current value between $50M and B → average (50+B)/2. Your improvement: 1.4 × (50+B)/2 = B. Solve: 70 + 1.4B/2 = B → 70 + 0.7B = B → 70 = 0.3B → B = $233M.

**Wait — this is above the stated range.** This means within the range $50M-$90M, your 40% improvement always generates enough value to justify winning. The winner's curse is not binding here because your operational uplift is large. In this case, bid your full expected-value calculation up to $98M, but confirm your improvement assumptions — they are doing all the work.

**When the winner's curse is binding:** It binds when your improvement multiplier is small (say 1.05×) and the value range is wide. In that case, the accepted-bid calculation reveals expected losses.

---

## References

- `references/auction-format-taxonomy.md` — Full mechanics of all five formats with decision trees
- `references/bid-shading-formula.md` — Derivation of V×(N-1)/N, worked examples across N, and adjustments for non-uniform value distributions
- `references/winners-curse-worksheet.md` — Step-by-step presume-you've-won calculation template with ACME example fully worked
- `references/dollar-auction-escalation.md` — Dollar auction mechanics, war-of-attrition model, BSB/Sky case, exit criteria
