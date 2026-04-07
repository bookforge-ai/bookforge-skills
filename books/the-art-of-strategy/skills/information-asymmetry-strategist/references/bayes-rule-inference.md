# Bayes' Rule for Type Inference in Strategic Games

## Purpose

When a player observes an action taken by an opponent who is playing a mixed strategy (or in a semi-separating equilibrium), that action is informative but not conclusive. Bayes' rule is the mathematically correct procedure for updating your probability estimate of the opponent's type given what you observed.

## The Formula

**P(type T | action A) = P(A | type T) × P(type T) / P(A)**

Where:

**P(A)** = total probability of observing action A
= P(A | type T) × P(type T) + P(A | type not-T) × P(type not-T)

In words: the probability that the opponent is type T, given you observed action A, equals the fraction of all cases where action A occurs that are attributable to type T.

## Worked Example: Poker Bluffing

### Setup

Your rival plays as follows:
- With a **good hand**: raises 2/3 of the time, calls 1/3 of the time, folds never
- With a **poor hand**: raises 1/3 of the time, calls never, folds 2/3 of the time

Prior: you believe good and poor hands are equally likely (P(good) = 1/2, P(poor) = 1/2).

### Probability Table

| Action | P(action \| good hand) | P(action \| poor hand) |
|--------|----------------------|----------------------|
| Raise  | 2/3                  | 1/3                  |
| Call   | 1/3                  | 0                    |
| Fold   | 0                    | 2/3                  |

### Applying Bayes' Rule to "Raise"

**P(raise)** = P(raise | good) × P(good) + P(raise | poor) × P(poor)
= (2/3)(1/2) + (1/3)(1/2)
= 1/3 + 1/6 = **1/2**

**P(good | raise)** = P(raise | good) × P(good) / P(raise)
= (2/3 × 1/2) / (1/2)
= (1/3) / (1/2) = **2/3**

**Interpretation:** After observing a raise, update from 50% prior to 67% posterior. The raise is informative — it shifts the probability of a good hand upward — but it is not conclusive. There is still a 1 in 3 chance the raise is a bluff.

### Applying Bayes' Rule to "Fold" and "Call"

**Fold:**
P(fold) = (0)(1/2) + (2/3)(1/2) = 1/3
P(good | fold) = (0 × 1/2) / (1/3) = 0

Observing a fold gives certainty of a poor hand. Posterior = 0% good.

**Call:**
P(call) = (1/3)(1/2) + (0)(1/2) = 1/6
P(good | call) = (1/3 × 1/2) / (1/6) = (1/6) / (1/6) = 1

Observing a call gives certainty of a good hand. Posterior = 100% good.

### Summary Table

| Observed action | P(good hand) before | P(good hand) after | Inference |
|---|---|---|---|
| Raise | 50% | 67% | Informative but inconclusive |
| Call | 50% | 100% | Conclusive — good hand |
| Fold | 50% | 0% | Conclusive — poor hand |

## Semi-Separating Equilibrium and Bayes' Rule

In a semi-separating equilibrium, some wrong-type players mimic the signal and some do not. The signal is informative but not perfectly separating. Bayes' rule determines how much posterior belief should shift.

**Key inputs needed:**
1. Prior probability of each type (base rates)
2. Probability each type takes the observed action (the mixing probabilities)

**When cost differences are small:** Wrong-type players mix between signaling and not signaling. The equilibrium mixing probabilities are determined by the condition that the wrong type is indifferent between mimicking and not mimicking. The posterior belief after observing the signal is determined by Bayes' rule given those mixing probabilities.

## Practical Guidance

**When to apply Bayes' rule:**
- You observe an opponent's action and want to update your belief about their type
- The opponent is known to play mixed strategies (not a pure type-revealing signal)
- You are in a pooling equilibrium and want to know how much information you can extract despite the pool

**When Bayes' rule gives extreme results:**
- If only one type ever takes a particular action (P(action | wrong type) = 0), observing that action gives certainty about type. No calculation needed — the posterior collapses to 1.
- If both types take an action with equal probability, observing it gives no information. The posterior equals the prior.

**Common error:** Ignoring base rates. If 90% of the population are the wrong type and only 10% are the right type, even a highly informative signal (P(action | right type) = 0.9 vs. P(action | wrong type) = 0.1) still leaves substantial uncertainty. With equal base rates (50/50), the same signal likelihoods yield a strong posterior update.

## Business Applications

**Interpreting a competitor's price cut:** If competitors with high-cost structures cut price rarely (1/10 of the time) and low-cost competitors cut price frequently (7/10 of the time), and you have a 50/50 prior about which type of competitor you face:
P(low-cost | price cut) = (0.7 × 0.5) / [(0.7 × 0.5) + (0.1 × 0.5)] = 0.35 / 0.40 = **87.5%**

A price cut is strong evidence of a low-cost competitor. Adjust your response accordingly.

**Interpreting a candidate's salary history:** If candidates with strong outside options disclose salary 80% of the time and candidates with weak outside options disclose 20% of the time, observing disclosure raises the probability of a strong outside option significantly. Non-disclosure has the opposite implication (Sherlock Holmes: the dog that did not bark).
