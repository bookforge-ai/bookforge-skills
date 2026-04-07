# Nonlinear Incentive Schemes and Gaming

## Linear vs. Nonlinear: The Core Tradeoff

**Linear (piece-rate) scheme:**
- Payment = base + rate x performance
- Incremental reward is constant at every performance level
- No threshold effects; agent faces the same marginal incentive throughout

**Nonlinear (quota-bonus) scheme:**
- Payment = low_base if performance < quota; high_base if performance >= quota
- Incremental reward is essentially zero everywhere except near the quota threshold
- Near the threshold, the expected gain from a small effort increase is very large (crossing the quota means getting the full bonus)

## Quota-Bonus Incentive Dynamics

**When the quota works:**
The quota is effective when the agent currently sits just below the threshold — a little more effort meaningfully increases the probability of crossing it. The agent faces a binary choice: work hard to make the quota or accept failure. The entire bonus rides on this marginal effort.

**Example:** Salesperson with $1M annual quota in October, currently at $900K. One strong quarter can clear the quota. The agent has maximum incentive to push hard.

**When the quota fails:**

*Case 1 — Too difficult (unreachable quota):*
Salesperson has a bad first half and is at $300K in June with a $1M annual quota. The quota is now mathematically unreachable. Expected gain from any further effort = 0 (cannot hit the quota regardless). Agent stops trying for the rest of the year. The flat-incentive zone below the threshold expands to cover the entire remaining period.

*Case 2 — Already met (no incremental reward):*
Salesperson meets the $1M quota in October. There is no reward for exceeding $1M. Agent stops and coasts through November and December — or deliberately holds orders to get a head start on next year's quota.

*Case 3 — Strategic order timing (sandbagging):*
Salesperson has $950K in sales with a week to go. She has two large orders she could close now, but if she closes them this year, she will start next year at $0. She can close one order now to make quota, and hold the other order for a strong January start. This sandbagging serves the agent's interest (head start on next year's quota) but damages the employer's interest (lost revenue this year, distorted reporting).

## The Enron Pattern

Enron's incentive scheme created massive rewards for reported revenue and profit — without distinguishing genuine revenue from accounting constructs. The quota-like structure (meet earnings targets = large bonus) created incentives to:
- Book speculative future revenues as current income
- Reclassify off-balance-sheet liabilities
- Enter related-party transactions to manufacture apparent revenue

The scheme was powerful near the earnings threshold (as intended) but in a direction opposite to what the employer wanted. The lesson: nonlinear schemes amplify whatever is being measured; if the measurement can be gamed, the gaming will be amplified too.

## Real Estate Commission Analysis

**Setup:**
- Agent earns 6% commission on sale price
- A $20,000 price increase (from negotiating harder, waiting for a better offer, spending more time marketing) generates 6% x $20,000 = $1,200 for the agent
- But the agent's opportunity cost — time not spent on the next listing — may be worth more than $1,200

**Why the agent misaligns:**
The agent's marginal return on negotiating harder is only $1,200 regardless of how much harder they work. The seller's marginal return is $18,800 (their 94% share). The agent's incentive to maximize price is 15.6x weaker than the seller's.

**Why not just increase the commission rate?**
At 6% the misalignment is 15.6:1. At 50% commission it is 1:1 — perfect alignment — but the seller keeps only half the sale price. The agent would need 100% commission to be fully aligned, which makes no sense (the agent would become the effective owner).

**Better nonlinear design:**
Progressive commission that concentrates incentive where the seller wants effort:
- 3% on sale price up to $500,000 (baseline, agent has less incentive to push beyond this)
- 30% on every dollar above $500,000 (agent has strong incentive to negotiate beyond the base)

This gives the agent 30 cents per dollar above the reserve rather than 6 cents — 5x stronger incentive exactly where it matters.

**Failure mode of progressive structure:**
If the $500,000 reserve is set too high and the market won't support it, the agent faces the unreachable-quota problem (Case 1 above). Must calibrate reserve to a realistic market price.

## Hybrid Design (Best Practice)

The most robust approach combines:

1. **Base commission rate (linear):** Provides constant incentive across all performance levels; prevents complete disengagement when circumstances change

2. **Quota bonuses at thresholds:** 100%, 150%, 200% of base quota add concentrated bursts of incentive at realistic achievement targets

3. **No cliff above the top threshold:** Continue the linear commission above 200% to prevent coasting after the top bonus is hit

This preserves the power of threshold bonuses at realistic performance levels while ensuring the agent never faces a period of zero marginal incentive.
