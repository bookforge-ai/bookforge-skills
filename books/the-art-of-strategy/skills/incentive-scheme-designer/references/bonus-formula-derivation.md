# Bonus Formula Derivation

## Setup

A principal (employer) hires an agent (worker) to perform a task. The agent can exert high effort or low effort. The principal cannot observe effort; only the outcome is observable.

**Variables:**
- p_H = probability of good outcome under high effort
- p_L = probability of good outcome under low effort
- p_H > p_L (high effort genuinely improves the probability)
- C = agent's cost of high effort (in monetary equivalent)
- W = market wage (agent's outside option)
- B = bonus paid for good outcome (payment increment above base)
- base = base pay (paid regardless of outcome)

## Incentive Compatibility Constraint

The agent chooses high effort if and only if expected pay from high effort >= expected pay from low effort:

```
p_H x (base + B) + (1 - p_H) x base >= p_L x (base + B) + (1 - p_L) x base + C

=> p_H x B >= p_L x B + C

=> (p_H - p_L) x B >= C

=> B >= C / (p_H - p_L)
```

The minimum bonus to induce high effort is: **B* = C / (p_H - p_L)**

**Intuition:** The expected bonus gain from switching to high effort is (p_H - p_L) x B. This must exceed the cost C of doing so. The smaller the probability gap, the larger B must be to compensate.

## Participation Constraint

The agent accepts the contract only if expected pay >= market wage:

Under high effort (which we want to induce):

```
p_H x (base + B) + (1 - p_H) x base >= W

=> base + p_H x B >= W

=> base >= W - p_H x B
```

The minimum base pay (binding participation constraint):

**base* = W - p_H x B**

With B = B* = C / (p_H - p_L):

```
base* = W - p_H x C / (p_H - p_L)
```

## When Base Pay Is Negative

base* is negative when p_H x B > W, i.e., when the expected bonus payment already exceeds the market wage. The agent must pay the principal a fine in the bad outcome. This is a fine structure.

**Example (Wizard 1.0):**
- p_H = 0.80, p_L = 0.60, C = $20,000, W = $70,000
- B* = $20,000 / 0.20 = $100,000
- base* = $70,000 - 0.80 x $100,000 = $70,000 - $80,000 = -$10,000

Payment structure: +$90,000 on success, -$10,000 on failure.

Expected pay = (0.80 x $90,000) + (0.20 x -$10,000) = $72,000 - $2,000 = $70,000 = W. Exactly satisfies participation.

## Equity-Share Equivalence

In the fine/bonus scheme, the programmer effectively owns a fraction of the firm:
- Pay $10,000 to acquire 50% stake (firm value: $200,000 on success, $0 on failure)
- Her net: -$10,000 + 50% x $200,000 = $90,000 on success; -$10,000 on failure

Equity share s that induces high effort:

```
(p_H - p_L) x s x V >= C

=> s >= C / [(p_H - p_L) x V]
```

In this example: s >= $20,000 / (0.20 x $200,000) = 0.50 = 50%

Both formulations are equivalent. Fine/bonus = equity sharing at the right fraction.

## Constrained Solution (No Fines)

If fine is unenforceable (legal constraint) or agent has no capital:

- base = 0, B = $100,000 (only paid on success)
- Expected pay = 0.80 x $100,000 = $80,000 > W = $70,000

Agent earns a $10,000 feasibility premium. Principal's average profit = $160,000 - $80,000 = $80,000 vs. $90,000 with fine solution. The $10,000 gap is the cost of moral hazard under the capital constraint.

## Risk Premium Complication

If the agent is risk-averse, they value the $100,000 bonus at less than its expected value ($80,000). They require additional compensation for bearing risk. The optimal solution is a compromise:
- Lower B (below $100,000) to reduce risk imposed on agent
- Higher base to compensate, accepting that this weakens effort incentive
- Result: effort somewhere between low and high; principal accepts some incentive loss to reduce risk premium cost

The more noise in the outcome (smaller p_H - p_L), the larger B must be to incentivize effort, and the more risk is imposed on a risk-averse agent. This is why high-noise environments tend toward fixed salaries.
