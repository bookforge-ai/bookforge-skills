# Rubinstein Bargaining: Mathematical Derivation

Source: The Art of Strategy, Ch. 11 Appendix (pp. 326–330)

## Setup

Two parties alternate making proposals for how to divide a pie of size 1. The pie is described as (X, 1-X) where X is the proposer's share. As soon as one side accepts the other's proposal, the game ends. Delay is costly: a dollar received next period is worth δ times a dollar received today.

δ (delta) is the patience parameter:
- δ close to 1: parties are patient, delay is cheap
- δ close to 0: parties are very impatient, delay destroys most of the value
- δ = 0: ultimatum game (entire pie disappears if offer is not accepted immediately)

## Finding the Equilibrium

Let L = the minimum share you will ever accept (your "lowest acceptable").

**Step 1:** If you turn down today's offer and wait to make a counteroffer tomorrow, the other side knows you will never accept less than L. So the most they can ever hope for is 1 - L. But that is what they get in one period. What they get today is δ(1 - L).

Since the best you can offer them tomorrow is δ(1 - L), they will accept it. That means by rejecting today and countering tomorrow, you can secure 1 - δ(1 - L).

**Step 2:** You should therefore never accept less than 1 - δ(1 - L) today.

Setting L = 1 - δ(1 - L) and solving:

```
L = 1 - δ(1 - L)
L = 1 - δ + δL
L - δL = 1 - δ
L(1 - δ) = 1 - δ
```

Wait — that gives L = 1 regardless of δ, which is wrong. The correct setup is:

The minimum you accept must satisfy: L ≥ δ(1 - δ(1 - L))

Working through the algebra as shown in the text:

```
L ≥ δ(1 - L) [the other side accepts δ(1-L) tomorrow]

Setting L = δ(1 - δ(1 - L)):
L = δ - δ²(1 - L)
L = δ - δ² + δ²L
L - δ²L = δ - δ²
L(1 - δ²) = δ(1 - δ)
L = δ(1 - δ) / (1 - δ²)
L = δ(1 - δ) / [(1 - δ)(1 + δ)]
L = δ / (1 + δ)
```

So L = δ/(1 + δ). This is the least you will ever accept when you are the responder (i.e., the person receiving an offer).

By symmetry, this is also the most you will ever offer the other side (since they will use the same logic). Therefore:

**Proposer's share = 1 - L = 1 - δ/(1 + δ) = 1/(1 + δ)**

**Responder's share = δ/(1 + δ)**

## Numerical Examples

### δ = 0.99 (weekly offers, 1% weekly discount — very patient)

```
Proposer gets: 1 / (1 + 0.99) = 1 / 1.99 ≈ 0.503
Responder gets: 0.99 / 1.99 ≈ 0.497
Split: approximately 50.3 / 49.7
```

Interpretation: With very short intervals between offers, the proposer's first-mover advantage nearly vanishes. The split is almost exactly 50/50.

### δ = 0.5 (each delay loses half the pie — moderately impatient)

```
Proposer gets: 1 / (1 + 0.5) = 1 / 1.5 = 2/3
Responder gets: 0.5 / 1.5 = 1/3
Split: 67 / 33
```

Interpretation: The proposer claims the half that would disappear if the responder said no (since δ = 1/2, half is lost per round), plus half of the remainder. Each round, the proposer collects twice as much as the responder.

### δ = 1/3 (impatient — two-thirds of value lost each delay)

```
Proposer gets: 1 / (1 + 1/3) = 1 / (4/3) = 3/4
Responder gets: (1/3) / (4/3) = 1/4
Split: 75 / 25
```

### δ → 1 (limit case: perfectly patient)

```
Proposer gets: 1/(1+1) = 1/2
Responder gets: 1/(1+1) = 1/2
Split: 50/50
```

### δ → 0 (limit case: ultimatum game)

```
Proposer gets: 1/(1+0) = 1
Responder gets: 0/(1+0) = 0
Split: 100/0
```

This matches the ultimatum game result from Chapter 2: if the pie disappears entirely if the responder says no, the proposer can demand everything.

## Applying to Real BATNAs

The Rubinstein formula applies to the pie (surplus above BATNAs), not to total value. The full split is:

```
Party A (proposer) receives: A_BATNA + Pie × [1/(1+δ)]
Party B (responder) receives: B_BATNA + Pie × [δ/(1+δ)]
```

If both parties have the same δ and alternate making offers, use δ = 1 as the practical approximation (50/50 pie split) unless there is a clear impatience asymmetry.

## Differing Impatience

If the two parties have different discount factors δ_A and δ_B, and the time between offers shrinks to zero, the pie is split in the ratio of their waiting costs. If one party is twice as impatient as the other, it gets one-third of the pie (half as much as the more patient party).

Practical implication: institutional structures that force impatience (electoral cycles, quarterly reporting, public media pressure) systematically reduce bargaining power. The U.S. government's impatience in international negotiations is repeatedly exploited by more patient counterparts.
