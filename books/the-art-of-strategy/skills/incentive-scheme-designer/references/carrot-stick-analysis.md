# Carrot vs. Stick Analysis

## Mathematical Equivalence

Any incentive spread can be framed as either a bonus (carrot) or a fine (stick). The two are economically equivalent when:
- The spread (difference between good and bad outcome payments) is the same
- The average payment (weighted by probabilities) is the same

**Example with spread = 50, average = 100, and 2% chance of exceptional event:**

Carrot scheme:
- Normal outcome: 99
- Exceptional good performance: 149 (probability 2%)
- Expected pay: 99 + (0.02 x 50) = 100

Stick scheme:
- Normal outcome: 101
- Exceptionally poor performance: 50 (probability 2%)
- Expected pay: 101 - (0.02 x 51) = 100

Both schemes have identical average payment (100) and identical incentive spread (50). They are mathematically identical from the standpoint of expected value.

## Why They Differ in Practice

**1. Reference point effects**

Behavioral economics shows agents respond differently to losses than gains of equal size. A fine of $10,000 is experienced as more painful than missing a $10,000 bonus, even though the financial outcome is identical. Sticks may therefore provide stronger behavioral incentive per dollar of expected value — but also create stronger resistance, anxiety, and resentment.

**2. Monitoring reliability**

Sticks require reliable detection of bad outcomes. If bad outcomes are sometimes falsely triggered (good workers occasionally punished), the stick:
- Punishes workers who do not deserve it (destroys trust)
- Weakens the link between effort and outcome (reduces incentive value)
- Causes workers to leave rather than accept arbitrary punishment risk

**Stalin's failure:** The Soviet punishment scheme was structurally a stick — work hard or go to Siberia. It would have been powerful if punishment were reliably tied to shirking. It failed because people were punished whether they worked hard or not (arbitrary purges, quota-meeting regardless of effort). When punishment is decoupled from effort, the incentive disappears entirely. Workers asked: "Why work hard if I might get punished anyway?"

**3. Legal and contractual constraints**

Employment law in most jurisdictions prohibits negative base pay and involuntary wage deductions for performance failures. Sticks are therefore frequently infeasible for employees. They are more available for:
- Contractors and vendors (performance bonds, liquidated damages)
- Equity holders (dilution)
- Executives with clawback provisions

**4. Agent wealth and capital**

A fine works only if the agent can pay it. If the agent lacks assets, fines are not credible — a bankrupt agent cannot be fined. This is why the constrained equity-sharing solution (no fine, bonus only) arises when the agent has no capital.

**5. Outside alternatives**

When the agent has strong outside options, the stick may cause them to simply leave rather than accept punishment risk. The effective threat of the stick depends on the gap between current wage and outside option. This is why above-market pay (efficiency wages) is a prerequisite for stick strategies to function.

## CEO Compensation as Carrot Structure

Top executive compensation is structured almost entirely as a carrot:
- Strong performance: very large bonus, stock options, accelerated vesting
- Average performance: moderately large salary plus some bonus
- Poor performance: "golden parachute" — still significant severance

The spread is enormous (billions in difference between great and poor outcomes), but the average is far above what would be needed to meet any reasonable participation constraint. The excess reflects competition for CEO candidates: the participation constraint is not "driving a cab" but "the package at Company X." European companies pay less and still attract capable CEOs because the European alternative is other European packages, not US ones.

## Efficiency Wages: Stick Built on Ongoing Relationship

The efficiency wage is a stick structure where the punishment is job loss rather than a fine. It works as follows:

**Setup:**
- Market wage: $40,000 (dead-end jobs requiring no special effort)
- Job value to employer: $60,000/year
- Cost of effort to worker: $8,000/year
- Probability of detecting shirking in any year: 25%
- Interest rate: 10%

**Efficiency premium calculation:**

The worker gains $8,000 from shirking (effort cost saved). They risk losing the premium X every year thereafter. If detected, lose X annually forever; present value of that loss at 10% interest rate = 10X.

No-shirk condition: $8,000 < 0.25 x 10X → X > $3,200

Minimum efficiency wage: $40,000 (market) + $8,000 (effort premium) + $3,200 (efficiency premium) = $51,200

**Why above $48,000 and not just $48,000?**

$48,000 = market wage + effort cost. At exactly $48,000, the worker is indifferent between the job and the outside option even while working hard. The extra $3,200 is the efficiency premium — it creates a cushion that makes shirking not worth the risk of losing the job.

The threat only works if:
- Detection probability is meaningful (not zero)
- The worker will be fired (not just warned)
- The word will spread (blacklisting is credible)
- The relationship is ongoing (the premium recurs; losing it matters)
