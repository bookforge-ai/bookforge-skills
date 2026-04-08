---
name: information-asymmetry-strategist
description: "Diagnose and resolve information asymmetry in strategic interactions using four mechanisms: signaling, screening, signal jamming, and countersignaling. Use this skill when a user needs to credibly communicate private information to an uninformed counterpart; when a user needs to elicit honest information from a better-informed counterpart without being able to verify their claims; when a user suspects they are on the receiving end of signal jamming or adverse selection and wants to see through it; when a user is designing a pricing scheme, contract structure, hiring process, or product menu and needs to induce self-selection among different customer or candidate types; when a user wants to know whether to signal their quality, countersignal by staying silent, or jam an opponent's signals; when a user needs to apply Bayes' rule to update beliefs after observing an opponent's action in a mixed-strategy game; when a user faces Akerlof-style market collapse risk and wants to identify signaling or screening remedies; when a user is designing a menu of options (e.g., airline fare classes, insurance deductibles, product tiers) and needs to check participation constraints and incentive compatibility constraints. This skill handles both directions of information asymmetry: the informed party communicating outward (signaling, countersignaling, jamming) and the uninformed party extracting information inward (screening, adverse selection management). It does NOT cover moral hazard or principal-agent problems after a contract is signed, nor does it handle simultaneous-move games without information asymmetry (use the Nash equilibrium skill for those)."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-art-of-strategy/skills/information-asymmetry-strategist
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [8]
tags: [game-theory, information-economics, signaling, screening, adverse-selection]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of the strategic situation: who holds private information, what they want the other side to believe or infer, what actions are available, and the cost structure for each type of player"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes the situation in text or structured form"
discovery:
  goal: "Identify which information asymmetry mechanism applies to the user's situation, design credible signals or effective screening menus, diagnose adverse selection and prescribe remedies, apply Bayes' rule to update beliefs from observed actions"
  tasks:
    - "Classify the information structure: who knows what, who benefits from revealing vs. concealing it"
    - "Identify the active mechanism: signaling, screening, signal jamming, or countersignaling"
    - "For signaling: verify the cost-difference property holds (signal is credible only if cost to the wrong type exceeds cost to the right type by more than the informational value)"
    - "For screening: design a menu that satisfies both the participation constraint (target type remains willing to transact) and the incentive compatibility constraint (wrong type prefers their intended option)"
    - "For adverse selection: diagnose whether bad types are being systematically attracted and prescribe a remedy (signal, screen, or positive selection)"
    - "Apply Bayes' rule to update beliefs from observed actions in mixed-strategy or semi-separating equilibria"
    - "Identify the equilibrium type: separating, pooling, or semi-separating"
    - "Check for countersignaling conditions: determine whether top types should refrain from signaling entirely"
    - "Deliver structured recommendations: which mechanism to use, specific design of the signal or menu, predicted equilibrium, and informational externality costs"
  audience: "Business strategists, product managers, hiring managers, marketers, negotiators, policy designers, and anyone who must communicate credibly or elicit honest information from strategic counterparts"
  when_to_use:
    - "User needs to convince a skeptical counterpart of their quality, commitment, or type without being able to simply say so"
    - "User is designing a contract, pricing tier, or application process to attract a specific customer or candidate type while discouraging others"
    - "User suspects they are in an adverse selection situation where bad types are systematically attracted to their offer"
    - "User wants to interpret an opponent's action probabilistically using Bayes' rule after observing a signal in a game with mixed strategies"
    - "User is unsure whether to signal their ability/quality or stay silent and countersignal"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Information Asymmetry Strategist

## When to Use

Use this skill when one player in a strategic interaction knows something important that another player does not — and both sides are trying to act strategically given this imbalance.

The core principle: **actions speak louder than words.** When interests are not fully aligned, claims cannot be trusted. But actions — especially costly ones — carry information precisely because they are not free to fake. The framework maps four ways to exploit or manage this: signaling, screening, signal jamming, and countersignaling.

This skill applies when:
- One party has private information (about quality, type, intentions, or capability) that affects both parties' payoffs
- That party has an incentive to reveal, conceal, or manipulate what the other infers
- The uninformed party wants to extract honest information or protect itself from strategic misrepresentation

This skill does NOT apply to:
- Post-contract moral hazard (hidden actions after agreement — different problem)
- Simultaneous-move games with symmetric information (use the Nash equilibrium skill)
- Pure negotiation where information is symmetric (use the negotiation BATNA framework)

---

## Context and Input Gathering

### Required (ask if missing)

- **Who holds the private information?** Is it the seller, candidate, counterpart, or the user themselves?
  -> Ask: "Who knows something relevant that the other side cannot directly observe?"

- **What is the private information?** Quality of a product, level of risk, genuine intention, capability, or type?
  -> Ask: "What exactly does the informed party know that the uninformed party wants to know?"

- **What is the direction of benefit?** Does the informed party want to reveal this information (to get a better deal) or conceal it (to avoid disadvantage)?
  -> Ask: "Does the informed party benefit from the other side knowing the truth, or from keeping it hidden?"

- **What actions are available?** What can the informed party do that the uninformed party can observe?
  -> Ask: "What observable actions can the informed party take? What can they offer, invest, display, or commit to?"

- **Cost asymmetry between types:** Does the potential signal cost more for one type than another?
  -> Ask: "Would this action cost more — in money, time, risk, or inconvenience — for someone who does NOT have the private information?"

### Useful (gather if present)

- Base rates: what proportion of the population are the "good" vs. "bad" type?
- The magnitude of payoff differences between types (needed for Bayes' rule calculations)
- Whether the interaction is one-shot or repeated (reputation effects change signaling economics)
- What screening options the uninformed party controls (contract terms, product versions, timing constraints)

---

## Execution

### Step 1 — Classify the Information Structure

**Why:** The four mechanisms work in opposite directions — applying the wrong one wastes effort and may backfire. A credible signal requires cost differences that may not exist. Screening requires control over the menu that the uninformed party may not have. Getting the classification right in thirty seconds prevents misdirected analysis.

**1a. Who holds private information?**

- Informed party = seller, applicant, counterpart → they have private knowledge about themselves
- Uninformed party = buyer, employer, user → they want to elicit or infer that knowledge

**1b. Who acts first?**

- Informed party acts first to reveal information → **Signaling** (seller offers warranty; applicant gets MBA)
- Uninformed party designs menu to force self-selection → **Screening** (employer requires MBA; insurer offers deductible tiers)
- Informed party acts to suppress or obscure information → **Signal Jamming** (poker bluffing; corporate obfuscation)
- Informed party refrains from signaling to communicate top status → **Countersignaling** (old money doesn't flaunt; top mathematicians don't follow convention)

Note: signaling and screening often produce similar equilibria via different initiative paths. The same credential (MBA) can be a screening device (firm requires it) or a signaling device (candidate volunteers it). The key principle — cost difference between types — is the same either way.

---

### Step 2 — Apply the Cost-Difference Property (For Signaling and Screening)

**Why:** This is the decisive test for whether any signal or screen will actually work. A signal that is equally cheap for the wrong type to mimic provides no information — it will be mimicked, and the equilibrium collapses. Every credible signal in every domain — warranties, education, tattoos, gang initiation rites — works because it satisfies this property.

**The cost-difference property:** A signal is credible if and only if it costs more for the wrong type to send than for the right type. The cost difference must exceed the informational value of the signal.

**Formally:** For a signal to separate types in equilibrium:
- Cost of signal for the "false" type > Cost of signal for the "true" type
- The gap must be large enough that the false type's expected gain from mimicking (the price premium or employment benefit from being mistaken for the true type) does not outweigh the cost

**Worked diagnostic:**

| Claimed signal | True type cost | False type cost | Cost difference | Signal credible? |
|---|---|---|---|---|
| Warranty | Low (cheap to honor good car) | High (costly repairs on bad car) | Large | Yes |
| Mechanic inspection offer | Zero (no commitment) | Zero (can walk away if bad) | None | No |
| MBA degree (talented) | $200K, certain pass | $200K, 50% fail risk | Extra $100K expected | Yes (if wage premium > $40K/yr) |
| Clean car for sale | Minimal | Minimal | None | No (pooling equilibrium) |
| Tattoo with partner's name | Low (committed person) | High (non-committed person) | Large | Yes |

**When to use each type of signal:**

- **Financial guarantees / warranties:** Credible when repair/fulfillment cost differs sharply by quality
- **Costly credentials / degrees:** Credible when completion rate or opportunity cost differs sharply by underlying ability
- **Irreversible commitments:** Credible when the commitment destroys future options that only a non-serious party would value
- **In-kind benefits (not cash):** Credible for self-selection when secondary value (resale of a wheelchair) differs sharply between true and false claimants

---

### Step 3 — Identify the Equilibrium Type

**Why:** The outcome of a signaling game depends on the mix of types in the population and the size of cost differences. Knowing which equilibrium type you are in determines both how to interpret the other side's actions and which interventions will shift the equilibrium.

**Separating equilibrium:** Different types take different observable actions. The action reliably identifies the type. This is the desired outcome for signaling and screening. Requires: the cost-difference property holds strongly enough that the wrong type will not mimic.

**Pooling equilibrium:** All types take the same action. The action conveys no information. This occurs when: cost differences are small, the proportion of wrong types is small (so even wrong types benefit from mimicking), or the signal is free to imitate. A clean car at sale time is a pooling signal when everyone cleans their car before selling.

**Semi-separating equilibrium:** Some of the wrong type mimic, some do not. The action is informative but not perfectly so. Occurs when cost differences are modest relative to the gain from mimicking. Requires Bayes' rule to interpret the resulting probabilistic signal. A dirty car would be a sure indicator of carelessness; a clean car is likely (but not certain) to indicate care.

**Diagnostic for equilibrium type:**

1. Is the cost difference large relative to the gain from mimicking? → Separating
2. Is the proportion of wrong types small? → Pooling (everyone mimics; signal is uninformative)
3. Is the cost difference small but positive? → Semi-separating (mixed-strategy mimicking, use Bayes' rule)

---

### Step 4 — Apply Bayes' Rule to Update Beliefs from Observed Actions

**Why:** In semi-separating equilibria (and when opponents play mixed strategies), observed actions are informative but not decisive. Bayes' rule is the correct tool for updating from "what I believed before" to "what I should believe now given what I observed." Applying it prevents both overconfidence (acting as if a signal is perfectly revealing) and underconfidence (ignoring a signal entirely).

**Bayes' Rule for type inference:**

P(true type | observed action) = P(action | true type) × P(true type) / P(action)

Where: P(action) = P(action | true type) × P(true type) + P(action | false type) × P(false type)

**Worked example (poker bluffing):** A rival raises 2/3 of the time with a good hand and 1/3 of the time with a poor hand. Prior probability of good hand = 1/2.

- P(raise | good hand) = 2/3
- P(raise | poor hand) = 1/3
- P(raise) = (1/2)(2/3) + (1/2)(1/3) = 1/3 + 1/6 = 1/2
- P(good hand | raise) = (1/3) / (1/2) = **2/3**

After observing a raise, update from 1/2 prior to 2/3 posterior. The raise is informative but not conclusive — there is still a 1/3 chance of a bluff. Decisions after the raise should incorporate this updated probability, not the original 50/50.

**Using Bayes' rule diagnostically:**

- If P(action | true type) >> P(action | false type): the action is highly informative; posterior shifts strongly toward true type
- If P(action | true type) ≈ P(action | false type): the action is barely informative; posterior barely moves from prior
- If you observe "fold" or another action unique to one type: posterior collapses to certainty (P = 0 or 1)

---

### Step 5 — Design or Evaluate a Screening Menu

**Why:** When the uninformed party controls the transaction structure (employer, insurer, seller offering product tiers), they can design a menu that induces each type to self-select into the option designed for them. This is more powerful than waiting to receive signals. But a menu that ignores the two constraints below will fail: either the target type opts out entirely, or the wrong type defects to the other option.

**Two binding constraints in screening design:**

**Participation constraint (PC):** The option designed for type T must offer that type at least as much value as opting out entirely. If the price exceeds the type's maximum willingness to pay (reservation price), they do not participate.

- For a screen to work: price ≤ reservation price of the target type
- Binding PC = you are extracting the maximum surplus from that type consistent with their participation

**Incentive compatibility constraint (ICC):** The option designed for type T must give type T at least as much surplus as the option designed for the other type.

- For a screen to work: surplus in own option ≥ surplus in the other option
- Binding ICC = the other type would be exactly indifferent; any worse and they defect

**Screening design procedure:**

1. Identify the two (or more) types and their reservation prices for each product/service version
2. Set the price for the low type at or below their reservation price (binding PC)
3. Calculate the consumer surplus the low-type option gives to the high type
4. Set the price for the high-type option so the high type's surplus equals or exceeds what they get from the low-type option (binding ICC)
5. Verify the resulting profit structure; compare against the alternative of serving only the high type at their full reservation price
6. If the proportion of low types is very small, consider whether it is more profitable to ignore them entirely (violate their PC) and charge high types their full reservation price

**Airline pricing illustration (PITS example):**

| Service | Cost | Tourist reservation price | Business reservation price |
|---|---|---|---|
| Economy | 100 | 140 | 225 |
| First | 150 | 175 | 300 |

- Tourist PC: Economy price ≤ 140 → set at 140 (binding)
- Business ICC: surplus from First class ≥ surplus from Economy at 140 → 300 − First price ≥ 225 − 140 = 85 → First price ≤ 215
- Set First class at 215; business travelers' surplus = 300 − 215 = 85 = their surplus from Economy at 140 (225 − 140 = 85) → they are indifferent, but choose First if there is any tiebreaker
- Profit per 100 passengers: (140−100)×70 + (215−150)×30 = 2800 + 1950 = 4750 vs. 7300 with perfect discrimination → informational externality cost = 2550

**The informational externality:** The cost of screening vs. perfect price discrimination equals the ICC rent multiplied by the number of high-type customers (85 × 30 = 2550). This cost exists because the low types, by existing, force the seller to give the high types a surplus to keep them from defecting.

---

### Step 6 — Diagnose and Remedy Adverse Selection

**Why:** Adverse selection — the systematic over-representation of bad types in a transaction — is the most common and damaging consequence of information asymmetry. It can cause entire markets to collapse (Akerlof's lemons). Correctly diagnosing adverse selection is the first step; the remedies are specific to the mechanism.

**Adverse selection diagnosis checklist:**

1. Is there information asymmetry where the transacting party knows their own type but the counterpart does not?
2. Does the current price or offer structure attract bad types more than good types (or exclusively bad types)?
3. Has the good type's willingness to transact fallen as the price has been adjusted to reflect the increasing proportion of bad types?
4. Has the market thinned, collapsed, or settled at a "lemons" price?

**If yes to 2-4: adverse selection is active.**

**Akerlof lemons mechanism (used car market):**
- If sellers know quality but buyers do not, and half the cars are lemons ($1K seller min, $1.5K buyer max) and half are peaches ($3K seller min, $4K buyer max):
- Buyers bid the expected value = (1/2)(1.5K) + (1/2)(4K) = $2.75K
- Peach owners will not sell at $2.75K (below their $3K floor) → only lemons offered
- Buyers, inferring this, bid only $1.5K → market for peaches collapses entirely
- The Groucho Marx effect: "Any car willing to sell at this price is not a car you would want to buy"

**Remedies by mechanism:**

| Situation | Remedy | Mechanism |
|---|---|---|
| Seller has quality information | Seller offers warranty, money-back guarantee, or long-term service contract | Signaling |
| Buyer has access to screening levers | Buyer requires certification, trial period, or deductible structure | Screening |
| Insurer cannot identify risk types | Offer deductible tiers: low-risk types prefer high deductible (lower premium); high-risk types prefer low deductible (higher premium) | Screening |
| Employer cannot observe talent | Require costly credential differentially costly to untalented | Screening |
| Bad types attracted to standard offer | Redesign offer to be unattractive to bad types (Capital One balance transfer: unattractive to maxpayers and deadbeats, attractive only to revolvers) | Positive selection |

**Positive selection (Capital One example):** Adverse selection can be reversed by designing offers that are attractive only to the profitable type. A balance transfer offer attracts revolvers (who have balances to transfer and intend to repay) while being irrelevant to maxpayers (no balance to transfer) and unattractive to deadbeats (who plan to default regardless). Any customer who accepts the offer is one you want.

---

### Step 7 — Evaluate Countersignaling (Should You Stay Silent?)

**Why:** The intuition that "you should always signal if you can" is wrong in some conditions. When there are three or more types (e.g., gold digger, question mark, and true love; or weak, average, and expert), and the uninformed party can distinguish the top type from others through alternative signals or background knowledge, the top type may benefit from NOT signaling. Signaling in this context reveals that you feel the need to distinguish yourself from the middle type — which is exactly what only the middle type needs to do.

**Countersignaling conditions (all three required):**

1. There are at least three types (bottom, middle, top), not just two
2. The top type is distinguishable from the bottom type even without the signal (through other observable attributes or base rate knowledge)
3. The middle type, by signaling, reveals that they are not the top type (because top types do not need to signal)

**Equilibrium with countersignaling:**
- Bottom type: does not signal (cannot afford it, or chooses not to play)
- Middle type: signals (to distinguish from the bottom type)
- Top type: does not signal (to distinguish from the middle type)

**Result:** Signaling is a signal of being middle-tier. The top type signals by the very absence of signaling.

**Examples:**
- Old money does not flaunt wealth; the nouveau riche does. Old money is identifiable through other means; flaunting reveals one is new money trying to be distinguished from those with no money.
- Highly accomplished faculty at top PhD programs use first names only in voicemails; faculty at lesser institutions use their title "Professor Dr." to distinguish themselves from those without doctorates.
- Expert negotiators do not demonstrate expertise through elaborate terminology; novices who have just learned the jargon use it constantly.

**Decision rule for countersignaling:**

- Are you clearly distinguishable from the bottom type even without the signal? → If yes, weigh countersignaling
- Would signaling group you with the middle type in the observer's inference? → If yes, countersignaling is better
- Is the observer sophisticated enough to run this three-way inference? → If no, you may need to signal anyway

---

### Step 8 — Signal Jamming (Obscuring Your Type)

**Why:** Sometimes your optimal strategy is not to communicate your type but to prevent the other side from inferring it. Mixed strategies in poker serve this purpose. Jamming preserves strategic uncertainty — keeping the opponent guessing maintains option value and prevents exploitation.

**When signal jamming applies:**
- Your interests are opposed to the other party (zero-sum or strongly competitive context)
- The other party would benefit from knowing your type and change their strategy accordingly
- You can randomize your actions credibly (or the cost of randomization is low)

**Signal jamming mechanics:**
- The "tight" poker player who never bluffs is exploitable: opponents know large bets mean good hands and fold accordingly, keeping pots small
- The "loose" player who always bluffs is also exploitable: opponents always call
- Optimal play mixes bluffing and legitimate raises at an equilibrium frequency derived from payoffs

**Key rule:** When interests are fully opposed, ignore what the other side says entirely. Do not assume their statement is true; do not assume its opposite is true. Play the equilibrium strategy as if no statement were made. The statement carries zero information content when interests are completely opposed.

**Signal jamming in business contexts:**
- Randomizing project launch timing to prevent competitors from inferring R&D readiness
- Mixing price promotions irregularly to prevent customers from timing purchases around predictable discounts
- Providing employees with information that is accurate in aggregate but not attributable to specific decisions, obscuring the decision rule

---

### Step 9 — Deliver Structured Recommendations

Structure your output as:

**Information asymmetry type:** [Who knows what; which direction it cuts]

**Active mechanism:** [Signaling / Screening / Signal Jamming / Countersignaling — and why]

**Cost-difference assessment:** [Does the cost-difference property hold? What is the cost to the true type vs. false type of the recommended signal or screen?]

**Equilibrium prediction:** [Separating / Pooling / Semi-separating — and why given cost differences and population proportions]

**Recommended action:**
- For signaling: specific action to take, why it satisfies the cost-difference property, and how the other party will update their beliefs
- For screening: specific menu design with prices/conditions, participation constraint check, incentive compatibility constraint check
- For adverse selection: diagnosis of which type is being over-attracted and which remedy (signal, screen, or positive selection redesign) applies
- For countersignaling: whether you are in a three-type situation, whether staying silent signals top-tier status

**Informational externality cost:** [What does correcting the asymmetry cost in total, and who bears it?]

**Failure modes:** [Under what conditions will this signal be mimicked, this screen be gamed, or this equilibrium collapse to pooling?]

---

## Key Principles

**Actions speak louder than words.** Verbal claims are cheap and will be made regardless of truth when interests diverge. Only costly, observable actions carry information — and only when the cost differs between types.

**The cost-difference property is the universal test.** A signal is credible if and only if the cost to the wrong type exceeds the cost to the right type by at least the value of the information conveyed. No other test is needed; no other test is sufficient.

**The informed party and uninformed party can both initiate.** The warranty can be offered (signaling) or demanded (screening). The MBA can be volunteered (signaling) or required (screening). The underlying equilibrium is similar; which party initiates depends on institutional context.

**Adverse selection is the systematic consequence of information asymmetry.** Without remediation, bad types crowd out good types until markets thin or collapse. The lemons market is not a special case — it is the generic outcome when information asymmetry is left unmanaged.

**Informational externalities are unavoidable.** The cost of signaling (the extra wages paid to talented workers to distinguish them from the untalented) is paid by the untalented's mere existence. This cost cannot be eliminated by any one party; it is the price of the information asymmetry.

**Countersignaling is rational for the top type in a three-tier world.** When you are clearly distinguishable from the bottom tier, signaling reveals you as middle-tier. The absence of a signal — for a top type — is itself the strongest signal.

**In purely opposed interactions, ignore the other side's statements.** When interests are fully opposed, verbal statements are strategically determined to mislead. Play the equilibrium strategy; update beliefs only from actions observed, using Bayes' rule.

---

## Examples

### Example 1: Hyundai Warranty (Signaling)

**Situation:** In 1999, Hyundai had improved quality but U.S. consumers did not believe it. Verbal claims of quality were worthless — any manufacturer can claim quality.

**Mechanism:** Signaling. Hyundai is the informed party (knows its own quality). Consumers are uninformed.

**Cost-difference analysis:** A 10-year / 100,000-mile warranty is cheap to offer if you genuinely build reliable cars (few claims). It is catastrophically expensive if your cars break down (massive warranty repair bills). The cost difference between a truly improved Hyundai and a still-defective manufacturer is large.

**Equilibrium:** Separating. A manufacturer who knew its cars were still defective would not offer this warranty — the expected repair costs would exceed the price premium gained. The signal works because only a confident manufacturer can afford to make it.

**Outcome:** Consumers rationally updated their quality beliefs. Hyundai's U.S. market share grew substantially.

---

### Example 2: Capital One Balance Transfer (Positive Selection)

**Situation:** Standard credit card offers suffer adverse selection — they attract maxpayers (no profit: merchant fees barely cover billing costs) and deadbeats (loss: default) while revolvers (most profitable: pay interest over time) are indistinguishable from the others.

**Mechanism:** Positive selection via targeted screening. The balance transfer offer is the screening device.

**Why it works:** Maxpayers have no outstanding balance — the offer is irrelevant to them. Deadbeats have no intention of repaying — bringing a balance they plan to default on provides no benefit. Revolvers, who have real outstanding balances and plan to repay, find a lower interest rate genuinely attractive. The offer self-selects only the profitable type.

**Key insight:** Capital One did not need to identify who the revolvers were. The nature of the offer caused them to identify themselves. This is the reversal of Groucho Marx: any customer who accepts this offer is exactly one you want.

---

### Example 3: Airline Fare Classes (Screening for Price Discrimination)

**Situation:** PITS airline serves 30 business travelers (reservation price: $300 first, $225 economy) and 70 tourists (reservation price: $175 first, $140 economy). PITS cannot tell them apart.

**Mechanism:** Screening. PITS designs two service tiers to induce self-selection.

**Constraint analysis:**
- Tourist PC: economy price ≤ 140 (tourists' max)
- Business ICC: first-class surplus ≥ economy surplus for business travelers
  → 300 − p_first ≥ 225 − 140 = 85 → p_first ≤ 215

**Optimal prices:** Economy = $140, First = $215
**Profit:** (140−100)×70 + (215−150)×30 = 2800 + 1950 = $4,750 per 100 passengers

**vs. perfect discrimination:** $7,300 — the $2,550 gap is the informational externality cost paid to business travelers as ICC rent (85 × 30).

**Failure mode:** If business travelers represent 50% of passengers, it may be more profitable to exclude tourists entirely and charge $300 to business travelers only (profit = (300−150)×50 = $7,500).

---

## References

- `references/cost-difference-property.md` — Formal derivation of the credibility condition, worked examples across domains, common failure cases
- `references/screening-menu-design.md` — Detailed procedure for designing participation-compatible, incentive-compatible menus with two and three types; algebraic examples
- `references/bayes-rule-inference.md` — Bayes' rule applied to type inference: worked poker example, generalized formula, updating in semi-separating equilibria
- `references/adverse-selection-remedies.md` — Akerlof lemons mechanism, insurer adverse selection, Capital One case, bureaucratic delay as screening, in-kind benefits
- `references/countersignaling-conditions.md` — Feltovich/Harbaugh/To three-type model, prenuptial example, voicemail study data, decision rule for when to countersignal

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Art of Strategy by Avinash K. Dixit, Barry J. Nalebuff.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
