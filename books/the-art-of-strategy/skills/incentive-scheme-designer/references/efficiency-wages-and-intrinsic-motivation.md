# Efficiency Wages and Intrinsic Motivation

## Efficiency Wages

### The Problem They Solve

Sometimes performance is not measurable continuously, but gross failure (shirking being discovered) occurs with a detectable probability. In this context, a performance-based bonus formula is not available — you cannot set B because there is no continuous outcome metric. But you can still deter shirking through the threat of job loss.

An efficiency wage is above-market pay that creates a valuable job worth keeping, combined with a credible threat to fire (and blacklist) any worker caught shirking. The worker shirks only if the one-time gain from shirking outweighs the expected present value of losing the wage premium.

### The Efficiency Wage Formula

**Variables:**
- W_eff = efficiency wage
- W_m = market wage (outside option)
- C = cost of effort (one-time gain from shirking = C saved)
- q = probability of detecting shirking in any period
- r = interest rate (for discounting future income streams)

**No-shirk condition:**

The worker shirks if:
```
C (gain from shirking) > q x PV(W_eff - W_m) (risk of losing premium)
```

Present value of losing the premium forever at interest rate r:
```
PV(W_eff - W_m) = (W_eff - W_m) / r
```

Wait — but the worker faces detection risk each year. Annual premium at risk: W_eff - W_m.
Present value of permanent stream: (W_eff - W_m) / r

No-shirk condition:
```
C < q x (W_eff - W_m) / r
=> W_eff - W_m > C x r / q
=> W_eff > W_m + C x r / q
```

**Worked example (text):**
- W_m = $40,000, C = $8,000, q = 0.25, r = 0.10
- Required efficiency premium: $8,000 x 0.10 / 0.25 = $3,200
- Efficiency wage: $40,000 (market) + $8,000 (effort cost premium) + $3,200 = $51,200

Verification: One-time gain from shirking = $8,000. Risk = 0.25 chance of losing $3,200/year forever; PV = $3,200/0.10 = $32,000; expected loss = 0.25 x $32,000 = $8,000. Exactly indifferent at $51,200. Any higher efficiency wage makes shirking strictly worse.

### When Efficiency Wages Work

**Required conditions:**

1. **Detectable failure:** Shirking must come to light with meaningful probability. If q ≈ 0, the premium required becomes infinite (no finite wage deters shirking when detection is impossible).

2. **Credible termination:** You must actually fire workers caught shirking. If workers know termination is unlikely (political protection, union rules, social norms), the threat loses credibility.

3. **Credible blacklisting:** The premium is only valuable if the fired worker cannot immediately get an equally good job elsewhere. "Spreading the word" among employers makes the blacklist credible.

4. **Ongoing relationship:** The premium is valuable because it recurs. A one-shot contract cannot use this mechanism effectively.

### Efficiency Wages in Daily Life

The principle extends beyond formal employment:
- **Regular mechanic:** Paying slightly more than the lowest rate makes the relationship worth preserving for the mechanic. Cheating (overcharging, doing unnecessary work) risks losing a steady client. The premium is for honesty, not efficiency.
- **Long-term contractors:** Vendors who depend significantly on your business have strong incentive to maintain quality — losing the account is costly.
- **Author-publisher relationships:** Publishers who pay higher advances have more to lose from a book's failure and are more invested in its success — and authors are more motivated to deliver.

## Intrinsic Motivation and Crowding Out

### The Gneezy/Rustichini Experiment

Subjects were given 50 questions from an IQ test. Four groups:

| Group | Incentive | Average correct |
|---|---|---|
| 1 | None — "do your best" | 28 |
| 2 | 3 cents per correct answer | 23 |
| 3 | 30 cents per correct answer | 34 |
| 4 | 90 cents per correct answer | 34 |

**Key findings:**
- Groups 3 and 4 outperformed the no-incentive group (financial incentive works when large enough)
- Group 2 performed worst of all — worse than no incentive
- Small payments destroyed intrinsic motivation without replacing it with sufficient extrinsic motivation

**Mechanism:** Introducing money changes the frame from "I am doing this because it matters / is interesting" to "I am doing this for pay." At 3 cents, the "pay" frame is active but the pay itself is insulting — it signals the task is not worth real money. At 30 cents, the pay frame is active and the pay is large enough to be motivating. The transition from intrinsic to extrinsic motivation is discontinuous: once money is introduced, intrinsic motivation is partially displaced.

**Secondary effect:** Small payments may also signal that the task itself has low value or low importance. "They are only paying me 3 cents per answer — this must not matter much."

### Practical Conclusion

Gneezy and Rustichini conclude: **pay significantly or do not pay at all.** There is no safe small-payment strategy when intrinsic motivation is present.

### Identifying Intrinsic Motivation

| Signal | Implication |
|---|---|
| Agent works below market rate voluntarily | Mission, reputation, or identity motivation likely present |
| Quality is highest when financial monitoring is lowest | Intrinsic standards drive performance, not fear of penalty |
| Agent describes work in mission/impact terms, not compensation terms | Strong non-monetary motivation |
| Agent is in a profession with strong ethical norms (medicine, teaching, law) | Professional identity substitutes for financial incentive |
| Agent seeks the work out proactively rather than being recruited | Genuine interest, not just market labor supply |

### Career Concerns as Intrinsic Substitute

Career concerns are not intrinsic in the same sense as mission motivation, but they function similarly — they provide strong incentive for effort without requiring direct financial incentive tied to performance.

**Career concerns are strongest when:**
- Agent is early in career with many years of future earnings at stake
- Agent is in a field where reputation and track record are persistent (academia, law, finance)
- Current work is visible — results will be known to future employers or clients
- Agent expects to stay in the field long-term

**Career concerns are weakest when:**
- Agent is near retirement
- Agent is planning to leave the field
- Work is confidential and cannot signal reputation
- Agent has already established peak career position

**Design implication for managers:**

For early-career employees in visible roles with strong career concerns:
- Reduce direct monetary incentive intensity (career concerns substitute)
- Invest in visibility (prominent projects, external speaking, bylines)
- Provide honest feedback and development — career concern is only useful if performance actually signals ability

For late-career employees or contractors without ongoing relationships:
- Increase direct monetary incentive intensity
- Career concerns are weaker; financial incentives must do more of the work

### The Double-Burden of Risk and Incentive

When an agent is both risk-averse and must be given financial incentives, the employer faces a double cost:
1. **Effort cost compensation:** Expected bonus must cover cost of effort (participation constraint)
2. **Risk premium:** Agent must be compensated for bearing outcome risk (beyond expected value)

The risk premium grows with:
- The size of the bonus (larger gamble → larger risk premium)
- The level of noise in the outcome (higher p_H - p_L means less noise; risk premium is smaller)
- The agent's degree of risk aversion

This is why high-noise environments (where p_H - p_L is small) naturally tend toward fixed salaries or efficiency wages rather than performance pay: the risk premium required to impose large incentives in noisy environments is prohibitively expensive.
