# Adverse Selection: Mechanism, Diagnosis, and Remedies

## What Adverse Selection Is

Adverse selection occurs when information asymmetry causes a transaction to attract the wrong types — systematically drawing in parties whose participation imposes costs on the uninformed counterpart. The term originated in insurance, where policies at a given price attract sicker, riskier, or more claim-prone customers than the average population. It generalizes to any market with private-type information.

**The Groucho Marx effect:** "Any club willing to accept me as a member is not one I would want to join." Applied to markets: any seller willing to sell at the average price is not one whose car (or service, or counterparty) you actually want.

## The Akerlof Lemons Mechanism (Full Walkthrough)

### Setup

Two car types:
- Lemons (bad quality): seller's minimum price = $1,000; buyer's maximum willingness to pay = $1,500
- Peaches (good quality): seller's minimum price = $3,000; buyer's maximum willingness to pay = $4,000
- Proportion: 50% lemons, 50% peaches

### With Symmetric Information (Baseline)

All transactions happen at prices between each type's floor and ceiling. Lemons trade at $1,000–$1,500. Peaches trade at $3,000–$4,000. Both markets function.

### With Asymmetric Information (Sellers Know, Buyers Don't)

**Step 1 — Buyers compute expected value:**
Expected willingness to pay = 1/2 × $1,500 + 1/2 × $4,000 = **$2,750**

**Step 2 — Peach sellers respond:**
A peach seller's floor is $3,000. No peach seller will sell at $2,750. Peaches are withdrawn from the market.

**Step 3 — Buyer inference updates:**
Buyers observe that only lemons remain. Update expected value to $1,500. Offer only $1,500.

**Step 4 — Equilibrium:**
Only lemons trade. Peach market collapses entirely — not because the good product is undesirable or overpriced, but because the buyer cannot distinguish it from lemons.

**The efficiency loss:** Buyers are willing to pay $4,000 for peaches. Sellers are willing to sell for $3,000. There is $1,000 of surplus available that is never realized. Information asymmetry causes a market failure even when all parties are acting rationally.

## Adverse Selection in Insurance

Insurance policies at a fixed premium attract disproportionately high-risk individuals:
- People with mortality rates above the break-even rate find the policy valuable (expected claims > premiums)
- People with mortality rates below the break-even rate may still buy (risk aversion, family protection), but high-risk individuals disproportionately buy larger policies

When the insurer raises premiums to cover losses, lower-risk individuals exit first (for them, the policy is now overpriced). The remaining pool is even riskier. Premiums must rise again. The process continues until only the highest-risk individuals remain — or the market collapses.

**Diagnosis check:** Are you selling an undifferentiated product where willingness to buy is higher for the "bad" type? If yes, adverse selection is active.

## The Credit Card Three-Type Taxonomy

Three customer types for credit cards:
- **Maxpayers:** Pay balance in full each month. Revenue source: merchant fees (~1-2% of transactions). Cost: billing, fraud, and the small risk of job loss/divorce leading to default. Issuers barely break even on these customers.
- **Revolvers:** Carry a balance from month to month and pay interest. Most profitable customer. Interest revenue at 15-25% APR exceeds costs substantially.
- **Deadbeats:** Carry balances but default. Pure cost to issuers.

**Standard offer adverse selection:** At a given APR, deadbeats and maxpayers both apply. Deadbeats apply because they intend to take money and not return it; maxpayers apply because the card is useful for transactions. The most valuable customers (revolvers) may apply but are mixed in with both unprofitable types.

**Capital One's positive selection solution:** The balance transfer offer is structured so that:
- Maxpayers have no balance to transfer → offer is irrelevant to them
- Deadbeats plan to default → a lower interest rate on a balance they will not repay does not change their expected behavior
- Revolvers have real balances, pay interest, and genuinely benefit from a lower rate → offer is attractive

The offer self-selects only the profitable type without requiring the issuer to identify revolvers directly. This is positive selection: designing the offer's attractiveness to be type-specific.

## Remedies for Adverse Selection

### Remedy 1: Signaling (Informed Party Acts)

The high-quality seller credibly communicates their type before the transaction. Requires the cost-difference property (see cost-difference-property.md).

**Examples:**
- Hyundai's 10-year / 100,000-mile warranty (1999): credibly communicated improved quality when reputation had not yet been established
- Financial co-investment (John's classified ad network): offering to co-invest in acquisitions signals genuine confidence in the deal's quality
- Trial periods with performance guarantees: if quality is truly high, the risk of offering a trial is small; if quality is low, the expected cost is high

### Remedy 2: Screening (Uninformed Party Designs Menu)

The uninformed party creates a menu of options designed so that different types self-select into different options. Requires satisfying participation constraints (PCs) and incentive compatibility constraints (ICCs). See screening-menu-design.md.

**Examples:**
- Insurance deductibles: high-deductible plans are chosen by low-risk individuals (they rarely claim, so a lower premium with more exposure is attractive). High-risk individuals prefer low-deductible plans (they claim frequently, so paying a higher premium for full coverage is worth it). Self-selection reveals risk type.
- Airline fare classes: restricted fares require advance purchase, non-refundability, and Saturday-night stay. These restrictions are cheap for leisure travelers (who plan ahead and stay over weekends) and expensive for business travelers (who need flexibility). Self-selection reveals price sensitivity.
- In-kind benefits (wheelchairs, not cash): benefits structured as specific goods that have high value only to genuine claimants are self-screening. The secondary market value is too low for false claimants to make fraud worthwhile.

### Remedy 3: Bureaucratic Friction as Screening Device

Requiring applicants to expend time and effort — filling out forms, waiting in offices, attending multiple appointments — is differentially costly across types:
- Healthy workers who can earn income will find the time too costly to spend
- Genuinely injured workers who cannot work can afford to spend the time

The apparent inefficiency of bureaucratic delay serves a real purpose: it screens false claimants without requiring direct verification of their claimed condition. Cash benefits create fraud incentives; in-kind benefits requiring effort reduce them.

**Important caveat:** This analysis does not justify bureaucratic inefficiency generally. It justifies specifically designed friction that is differentially costly between genuine and fraudulent claimants. Randomly slow processes that impose equal costs on all types are simply wasteful.

### Remedy 4: Positive Selection (Offer Design)

Design the offer so that its attractiveness is higher for the profitable type than for the unprofitable type — ideally making it attractive only to the desired type.

**Design principle:** Identify what the desired type uniquely needs or values. Structure the offer to deliver exactly that. Ensure the offer is unattractive or irrelevant to the undesired types.

**Testing the design:** Ask for each unwanted type: "Why would they NOT accept this offer?" If you cannot answer that question, the offer will attract them and adverse selection remains.

## Diagnosing Adverse Selection in Your Situation

Run through these questions:

1. **Do the transacting counterparts know something material about themselves that you cannot verify?** (Quality, risk, intention, capability)
2. **Does your current offer structure appeal more to the type that is costly to serve?** Check: who self-selects in vs. who you would want.
3. **Is the average quality of counterparts who accept your offer lower than the average quality of all potential counterparts?** Measure: claims rates, default rates, refund rates, churn rates, performance.
4. **Have you tried raising your standards (price, requirements) only to find the pool got worse, not better?** Classic adverse selection response.

If yes to 2 and 3: adverse selection is active. Proceed to remedy design.
