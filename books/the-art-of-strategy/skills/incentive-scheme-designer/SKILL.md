---
name: incentive-scheme-designer
description: "Design and diagnose incentive contracts for situations where effort is unobservable (moral hazard). Use this skill when a user needs to motivate a contractor, employee, co-founder, or agent whose actions cannot be directly monitored; when a user is deciding between a fixed salary, piece-rate, equity share, bonus, or fine structure; when a user needs to set the bonus level so that high-quality effort is in the agent's self-interest; when a user must satisfy both the participation constraint (agent accepts the deal) and the incentive compatibility constraint (agent exerts the desired effort); when a user wants to diagnose why an existing incentive scheme is failing — through sandbagging, gaming, effort diversion, or lack of effort; when a user is deciding between carrots and sticks and needs to understand when each is preferred; when a user suspects financial incentives are crowding out intrinsic motivation (Gneezy/Rustichini effect); when a user manages people performing multiple tasks and needs to know whether to bundle or separate them based on complementarity vs. substitutability; when a user needs to understand efficiency wages and when above-market pay is the cheapest way to deter shirking. This skill covers the full principal-agent problem after a contract is signed. It does NOT cover pre-contract adverse selection (who to hire) — use the information-asymmetry-strategist skill for that."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-art-of-strategy/skills/incentive-scheme-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [13]
tags: [game-theory, incentive-design, moral-hazard, principal-agent, compensation]
depends-on: [information-asymmetry-strategist]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Description of the principal-agent situation: what the agent is hired to do, what outcomes are observable, what effort is unobservable, what the market wage is, the cost of effort to the agent, and the probability that high vs. low effort produces a good outcome"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes the situation in text or structured form"
discovery:
  goal: "Design an incentive contract that induces the desired effort level while satisfying the agent's participation constraint, select the optimal scheme type (linear vs. nonlinear, carrot vs. stick), diagnose multi-task distortions, assess career concern substitutes, and identify when financial incentives will backfire"
  tasks:
    - "Establish the observable outcome, the unobservable effort levels, and the probability that each effort level produces a good outcome"
    - "Compute the minimum bonus needed to make high effort incentive-compatible: B >= cost_of_effort / (p_H - p_L)"
    - "Set base pay to satisfy the participation constraint: base = market_wage - p_H x B (may be negative — a fine)"
    - "Evaluate whether the fine/equity solution is feasible given legal constraints and agent capital"
    - "Compare linear (piece-rate) vs. nonlinear (quota-bonus) schemes: robustness vs. threshold power"
    - "Diagnose carrot vs. stick: equivalent mathematically, but sticks preferred with reliable monitoring; carrots preferred with imperfect monitoring or where punishment destroys participation"
    - "Assess multi-task structure: are tasks complements (bundle, use strong incentives for all) or substitutes (separate, equalize or weaken incentives)"
    - "Check career concern strength: early-career agents may need weaker monetary incentives; near-retirement agents need stronger ones"
    - "Flag intrinsic motivation risk: if the agent currently works for non-monetary reasons, introducing small financial incentives may destroy more motivation than they create"
    - "Design efficiency wage when direct performance measurement is noisy but termination threat is credible"
    - "Deliver structured contract recommendations with explicit numbers wherever inputs allow"
  audience: "Managers, founders, product leads, contract designers, compensation consultants, policy designers, and anyone structuring agreements where effort quality is hard to observe directly"
  when_to_use:
    - "User is designing a contract where they cannot observe how hard or well the other party works"
    - "User suspects an existing incentive scheme is being gamed, sandbagged, or producing effort on the wrong tasks"
    - "User is deciding how large a bonus, equity stake, or penalty to set"
    - "User needs to motivate someone who performs multiple tasks and is worried about effort being diverted away from less-measured tasks"
    - "User is considering whether to add financial incentives to a role currently governed by intrinsic motivation or professional norms"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Incentive Scheme Designer

## When to Use

Use this skill when you have a principal-agent problem: you are hiring, contracting with, or managing someone whose effort quality matters to you but cannot be directly observed. You can only observe outcomes — and outcomes depend on effort plus luck. The goal is to design a payment scheme that makes the agent's self-interest align with your interests, without paying more than necessary.

The core challenge: **you cannot pay for effort because you cannot see it.** You can only pay for outcomes. But outcomes are imperfect proxies for effort. Tying pay too tightly to outcomes imposes risk on the agent (who may rationally demand a risk premium). Tying pay too loosely means the agent has little reason to work hard. Every incentive scheme is a tradeoff between incentive power and risk imposition.

This skill builds on the information-asymmetry-strategist framework. The difference: adverse selection is about who signs the contract (pre-contract hidden types). Moral hazard is about what they do after signing (post-contract hidden actions). The mechanisms for dealing with them overlap — both use participation constraints and incentive compatibility — but the design logic is different.

This skill does NOT apply to:
- Selecting among candidates of unknown quality (pre-contract adverse selection — use information-asymmetry-strategist)
- Symmetric-information situations where effort is directly verifiable
- Pure negotiation over price without ongoing effort (use the negotiation skill)

---

## Context and Input Gathering

### Required (ask if missing)

- **What is the observable outcome?** What measurable result can you tie pay to?
  -> Ask: "What can you actually observe at the end — revenue, errors found, project success or failure?"

- **What are the effort levels?** What is the difference between routine/low effort and the desired high effort?
  -> Ask: "What does the agent do differently when working hard vs. coasting? What does this cost them — in stress, hours, skill, or discomfort?"

- **What is the probability difference?** How much does high effort raise the chance of a good outcome vs. low effort?
  -> Ask: "If they work hard, what is the probability of success? If they coast, what is the probability?"

- **What is the market wage?** What could the agent earn elsewhere at the same effort level?
  -> Ask: "What is their outside option — what would they earn doing a comparable job?"

- **What is the agent's cost of effort?** The subjective cost in money terms of exerting high rather than low effort.
  -> Ask: "What pay increment would the agent require to voluntarily choose high effort over low effort on their own, with no monitoring?"

### Useful (gather if present)

- Whether fines or negative base pay are legally and practically enforceable
- Whether the agent has capital to invest (enabling equity sharing or fine solutions)
- How many tasks the agent performs simultaneously and whether they are substitutes or complements
- How early or late the agent is in their career (career concern strength)
- Whether the role currently attracts intrinsically motivated people or mercenaries
- Whether the agent will be monitored repeatedly over time (repeated relationship effects)

---

## Execution

### Step 1 — Establish the Probability Structure

**Why:** Everything else in incentive design depends on this. The bonus formula, the base pay, and the efficiency of the scheme all flow from the probability difference (p_H - p_L). If this gap is large, a small bonus can induce high effort. If the gap is small (luck dominates), you need a very large bonus to matter — which imposes high risk on the agent and is expensive.

**Define:**
- p_H = probability of good outcome under high effort
- p_L = probability of good outcome under low effort
- V = value to you of a good outcome (vs. bad outcome)

**Critical check — does effort actually matter?**

If p_H - p_L is small (say, 0.05), outcome is mostly noise. Outcome-based pay will be weakly linked to effort and impose high risk on the agent for little incentive gain. In this case:
- Use fixed salary or efficiency wages instead of performance pay
- Invest in improving monitoring if possible
- Accept that strong incentives may not be feasible

If p_H - p_L is large (say, 0.30 or more), outcome-based pay is powerful and relatively efficient.

---

### Step 2 — Compute the Minimum Incentive Bonus

**Why:** The bonus must be large enough that, in the agent's own calculation, the expected gain from high effort exceeds its cost. Setting it below this threshold gives the agent no rational reason to exert high effort. Setting it far above this threshold overpays for incentive power you do not need — or imposes unnecessary risk.

**The bonus formula:**

```
B >= cost_of_effort / (p_H - p_L)
```

Where B is the bonus paid for a good outcome (beyond the base pay).

**Derivation logic:** The agent chooses high effort if and only if the expected pay gain from doing so covers the cost. The expected gain from high effort = (p_H - p_L) x B. Setting this equal to cost_of_effort gives the minimum B.

**Worked example (Wizard 1.0 programmer):**
- High effort: p_H = 0.80, cost of effort above market = $20,000
- Low effort: p_L = 0.60
- Minimum bonus: B >= $20,000 / (0.80 - 0.60) = $20,000 / 0.20 = **$100,000**

The bonus for success must be at least $100,000 to make high effort worthwhile.

**Worked example (proofreader):**
- Effort cost: $X (subjective cost of careful reading)
- Probability of finding errors with high effort: p_H
- Probability of finding errors with low effort: p_L
- The piece rate per error found is the continuous analog: the per-error payment must cover the marginal effort cost per marginal error found

---

### Step 3 — Set Base Pay to Satisfy the Participation Constraint

**Why:** The agent must be willing to take the job. If the expected payment under the optimal incentive scheme falls below the market wage, the agent will not accept. You must therefore set base pay so that expected total compensation equals the market wage. This may require negative base pay (a fine) — meaning the agent pays you if the bad outcome occurs.

**The participation constraint:**

```
p_H x (base + B) + (1 - p_H) x base >= market_wage
=> base + p_H x B >= market_wage
=> base >= market_wage - p_H x B
```

Simplified (binding participation constraint at minimum cost to you):

```
base = market_wage - p_H x B
```

Note: base pay can be negative. A negative base pay is a fine paid by the agent in the event of failure. This is mathematically equivalent to equity sharing.

**Worked example (Wizard 1.0):**
- B = $100,000, p_H = 0.80, market wage = $70,000
- base = $70,000 - (0.80 x $100,000) = $70,000 - $80,000 = **-$10,000**

The agent pays a $10,000 fine if the project fails, and receives $90,000 if it succeeds. Expected compensation: (0.80 x $90,000) + (0.20 x -$10,000) = $72,000 - $2,000 = $70,000. Participation satisfied exactly.

**When negative base pay is not feasible:**

If fines are legally unenforceable or the agent lacks capital, the minimum effective bonus is $100,000 on success and $0 on failure. The agent's expected compensation rises to $80,000 (0.80 x $100,000), exceeding the $70,000 market wage. You pay a $10,000 "feasibility premium." This is the cost of moral hazard when the first-best fine solution is unavailable.

---

### Step 4 — Evaluate Scheme Type: Linear vs. Nonlinear

**Why:** The shape of the incentive scheme determines both its power and its vulnerability to gaming. Linear schemes (piece-rate) are robust but apply uniform incentive pressure everywhere on the performance scale. Nonlinear schemes (quota-bonus) concentrate incentive power near the threshold — which is powerful when the threshold is correctly set but creates perverse incentives both below and above it.

**Linear (piece-rate) schemes:**
- Pay proportional to output: every unit of performance earns the same increment
- Strengths: robust to changing circumstances; no inflection points to exploit; agent faces constant marginal incentive
- Weaknesses: may provide insufficient incentive at any particular level; salary cost scales linearly with output
- Best for: ongoing work where effort is continuous and circumstances change (annual sales, error detection)

**Nonlinear (quota-bonus) schemes:**
- Pay a low fixed amount below a threshold; pay a high fixed amount above it
- Strengths: enormous incentive power near the threshold; the spread can be very large without high average cost
- Weaknesses: zero incentive power far from the threshold; invites three failure modes:

| Failure mode | Mechanism | Example |
|---|---|---|
| Below-threshold disengagement | Agent far below quota stops trying; reaching quota is hopeless | Salesperson with bad Q1 coasts through Q2 |
| Above-threshold sandbagging | Agent who hits quota early stops; no reward for exceeding it | Salesperson meets June quota; holds orders until next year |
| Inter-period manipulation | Agent shifts work across periods to hit thresholds optimally | Enron booking false revenues; agent delays customer orders |

**Hybrid approach (in practice):** Combine a base commission rate (linear) with quota bonuses at 100%, 150%, and 200% of target. The linear commission ensures constant baseline incentives; the quota bonuses provide threshold bursts. This captures quota power while limiting the flat-incentive zones.

**Decision rule:**
- Stable task, well-understood probability structure → nonlinear (quota) fine-tuned to the right threshold
- Changing circumstances, multi-period work, or risk of threshold manipulation → linear or hybrid
- Circumstances changed after contract set (making quota unreachable or already met) → linear component prevents incentive collapse

---

### Step 5 — Choose: Carrot or Stick

**Why:** Any incentive spread can be structured as a bonus above the base (carrot) or a fine below the base (stick). The mathematics are identical — what changes is the reference point, the agent's likely behavioral response, and the feasibility constraints. Choosing the wrong framing wastes the incentive power you are paying for.

**Mathematical equivalence:**

Both schemes below have average payment = 100 and spread = 50:
- Carrot: base = 99, bonus = 50 if exceptional performance (2% chance with desired effort) → expected = 99 + (0.02 x 50) = 100
- Stick: base = 101, fine = 51 if exceptionally poor performance (2% chance with desired effort) → expected = 101 - (0.02 x 51) = 100

Same incentive power, same expected cost. The difference is behavioral and practical.

**When to use sticks:**
- Monitoring is reliable: the failure event (shirking coming to light) is observable with reasonable accuracy
- The agent has assets or stakes that can be forfeited
- The agent has outside alternatives that are poor (the threat of job loss plus fine is credible and powerful)
- Example: Stalin's approach would have worked if punishment were reliably tied to effort rather than arbitrary. It failed not because sticks don't work, but because the punishment wasn't tied to actual shirking — people were punished whether they worked hard or not.

**When to use carrots:**
- Monitoring is imperfect: false positives (punishing diligent workers) damage trust and destroy participation willingness
- Legal constraints prohibit negative base pay or fines on employees
- The agent has strong outside options (they will simply leave rather than accept punishment risk)
- Workforce morale is important: being fired or fined publicly destroys motivation for the broader team
- Example: The Dixit proofreading contract — $600 base plus $1/error found. A pure fine structure (pay nothing without errors; fine for missed errors) would cause the student to reject the work.

**Efficiency wages as a special case of the stick:**

When you cannot measure performance well enough to set a bonus formula but can detect gross shirking occasionally, set the wage above market by enough that the threat of losing it deters shirking:

```
X > cost_of_effort / (detection_probability x (1 + 1/interest_rate))
```

The efficiency premium X must exceed the one-time gain from shirking (cost saved) discounted by the probability of detection and the present value of the perpetual wage premium at risk. This works when:
- Shirking is detectable with meaningful probability (even if not always)
- The relationship is ongoing (the premium is valuable precisely because it recurs)
- Firing and blacklisting is credible (word spreads; bad reputation follows the agent)

---

### Step 6 — Handle Multiple Tasks

**Why:** Most real agents perform multiple tasks simultaneously. Adding strong incentives to one task can either help or hurt performance on others, depending on whether the tasks are substitutes or complements. Ignoring this is one of the most common sources of incentive scheme failure.

**Substitutes:** Effort on task A reduces the marginal productivity of effort on task B (because they share a limited effort budget, compete for time, or are cognitively exhausting in the same way).
- Example: A farmhand in corn and dairy. More corn time = more tired = less productive in dairy.
- Example: Teaching and research at a university that keeps them separate by design (French model).
- Example: A customer service rep measured on call speed who also does quality follow-up — strong speed incentives divert effort from quality.

**Complements:** Effort on task A raises the marginal productivity of effort on task B.
- Example: A beekeeper who also tends apple orchards. More bee-keeping makes orchard more productive through pollination.
- Example: Research and teaching at a US research university — research deepens teaching; teaching sharpens research questions.
- Example: A salesperson who does both prospecting and closing — better prospecting leads to better clients who are easier to close.

**Design rules by task relationship:**

| Relationship | Rule | Reason |
|---|---|---|
| Substitutes | Equalize incentive strength across tasks; use weaker incentives for both | Strong incentive on A diverts effort from B; net effect may be negative |
| Complements | Use strong incentives for all tasks | Effort on A amplifies B; synergies compound; no diversion problem |
| Unknown | Start with equal moderate incentives; observe for diversion patterns | Asymmetric incentives are risky when relationship is unclear |

**Organizational design implication:** Group complementary tasks together under one person (or division) and use strong incentives. Separate substitute tasks into different people or divisions with independent incentive schemes. The failure to follow this — mixing substitute tasks with shared incentives — is a structural source of incentive weakness.

**Heathrow Airport example:** Check-in, security, shopping, and boarding are all complements — they form one end-to-end process. Splitting them across BAA, police, and a regulator with opposing incentives (BAA profits from shops; regulator prices landing fees to reduce congestion) created predictable dysfunction. Each owner's incentives partially cancel the others'.

**Multiple owners / bosses:** The incentive strength is inversely proportional to the number of owners with conflicting objectives. When agent answers to N bosses with opposed interests, each boss's incentive partially cancels the others'. In the extreme (fully opposed principals), incentive strength approaches zero. This explains incentive weakness in public sector agencies, international bodies, and joint ventures with misaligned partners.

---

### Step 7 — Account for Career Concerns and Repeated Relationships

**Why:** Financial incentives are not the only incentive mechanism. Early-career agents are often powerfully motivated by reputation, promotion prospects, and future earnings — mechanisms that substitute for or supplement direct monetary incentives. Ignoring career concerns leads to over-paying for monetary incentives early in a career and under-paying for them late.

**Career concerns:**
- Strong when: agent is early-career, relationship is ongoing, agent has future earning potential in this or related fields
- Weak when: agent is near retirement, agent plans to leave the field, relationship is one-shot
- Effect: career concerns substitute for monetary incentives early in career. A junior employee working on a visible project has strong incentive to perform because the outcome is part of their professional record, even with a modest salary bonus.
- Implication: reduce monetary incentive intensity for early-career employees in visible roles; increase it near retirement or for contractors with no ongoing relationship

**Repeated relationships:**
- When the same agent works on multiple projects over time, each outcome gives you more information about their underlying effort level
- By the law of large numbers, average output over many projects is a more accurate indicator of average effort than any single outcome
- This allows stronger incentives over time: persistent poor outcomes become attributable to effort rather than luck
- Also: the employer can credibly threaten to "believe the bad luck story once" but not repeatedly — this itself disciplines the agent

**Design implication:** An incentive scheme that looks too weak for a one-shot interaction may be adequate for a long-term relationship where career concerns and repeated-game reputation effects provide supplementary discipline.

---

### Step 8 — Check for Intrinsic Motivation Risk

**Why:** Adding financial incentives to a role currently governed by intrinsic motivation can backfire. When money enters the picture, it becomes the primary frame for evaluating the task. A small payment that is insulting relative to effort converts a volunteer activity into a poorly-paid job. The result can be performance worse than no incentive at all (the Gneezy/Rustichini finding).

**The Gneezy/Rustichini experiment:**
- Group 1: no payment → 28 correct answers on average (intrinsic motivation intact)
- Group 2: 3 cents per correct answer → 23 correct answers (worst performance — money frame introduced, amount too small)
- Group 3: 30 cents per correct answer → 34 correct answers (incentive large enough to dominate)
- Group 4: 90 cents per correct answer → 34 correct answers (same)

**Key finding:** Small payments destroy intrinsic motivation and produce the worst outcome. The prescription: pay significantly or do not pay at all. There is no safe small-payment middle ground when intrinsic motivation is present.

**Signals that intrinsic motivation may be present:**
- Agents voluntarily seek out the work (academics, doctors, nonprofit workers, open-source contributors)
- Current compensation is below market wage, yet quality is high
- Workers describe their role in mission-oriented rather than transactional terms
- Quality is highest when financial monitoring is lowest

**Decision rule:**
- Strong intrinsic motivation + you cannot offer a substantial financial incentive → do not introduce financial incentives; use non-monetary recognition, career concerns, and mission framing
- Strong intrinsic motivation + you can offer a substantial financial incentive → proceed, but monitor for crowding out (e.g., quality may fall on less-measured dimensions)
- Weak or absent intrinsic motivation → financial incentives are the primary tool; calibrate using the bonus formula in Step 2

---

### Step 9 — Deliver Structured Contract Recommendations

Structure your output as:

**Scheme type:** [Fixed salary / Linear piece-rate / Quota-bonus / Equity share / Efficiency wage — and why given the situation]

**Bonus calculation:**
- p_H = [value], p_L = [value], cost_of_effort = [value]
- Minimum bonus: B = cost_of_effort / (p_H - p_L) = [value]

**Base pay calculation:**
- market_wage = [value]
- base = market_wage - p_H x B = [value]
- If negative and infeasible: constrained solution = [0 base + B on success only]; feasibility premium = [value]

**Carrot vs. stick recommendation:** [With rationale: monitoring reliability, legal constraints, agent alternatives]

**Multi-task assessment:** [Are tasks substitutes or complements? Are incentives equalized or differentiated? Should tasks be bundled or separated?]

**Career concern adjustment:** [Is the agent early-career? Should monetary incentive be reduced accordingly?]

**Intrinsic motivation check:** [Is there risk of crowding out? Is the payment level above the threshold to avoid the Gneezy/Rustichini trap?]

**Failure modes to watch for:** [Sandbagging, gaming, effort diversion, threshold exploitation — specific to this scheme]

**Your expected profit:** [Revenue - average compensation, with and without moral hazard constraint]

---

## Key Principles

**Pay for outcomes, not effort — because you can only observe outcomes.** The fundamental constraint is observability. Build incentive schemes around what you can actually measure. Do not assume you will be able to infer effort from outcomes when noise is high.

**The bonus formula is the anchor.** B = cost_of_effort / (p_H - p_L) is the minimum bonus to induce high effort. Everything else — base pay, scheme shape, carrot vs. stick — is calibration around this anchor. Compute it first.

**Participation and incentive compatibility are both binding.** A scheme that induces effort but pays below market wage will be rejected. A scheme that pays market wage but provides no effort incentive will lead to shirking. Both constraints must be satisfied simultaneously.

**Carrots and sticks are mathematically equivalent; choose based on monitoring reliability and legal context.** Stalin's economy failed not because sticks cannot work, but because punishment was not reliably tied to shirking. With arbitrary punishment, the incentive disappears — workers are penalized whether they work hard or not.

**Multiple tasks destroy incentives unless tasks are complements.** Any time you measure one task well and another poorly, effort flows to the measured task. Fix this by grouping complementary tasks together, giving substitute tasks to different people, and equalizing incentive strength across tasks you cannot avoid bundling.

**Small payments are worse than no payments when intrinsic motivation is present.** Introduce financial incentives only if you can make them substantial. The threshold is not zero — it is large enough that the monetary frame dominates rather than merely corrupts the intrinsic one.

**Efficiency wages work when termination is credible and the relationship is ongoing.** The wage premium deters shirking by making the job worth keeping. The threat is only credible if you will actually fire; the deterrence is only valuable if the relationship is long-term.

---

## Examples

### Example 1: Real Estate Agent Commission Problem

**Situation:** A real estate agent earns a 6% commission on house sales. The seller is asking $500,000.

**The alignment problem:** On a $20,000 price increase (e.g., negotiating harder or waiting for a better offer), the agent gains only 6% x $20,000 = $1,200. But the agent's opportunity cost — the time spent on this house rather than moving to the next listing — is far higher. The agent's optimal strategy is to close quickly at a good-enough price, not maximize price for the seller.

**Why 6% linear commission fails:** The agent's stake in the marginal price improvement ($1,200) is far smaller than the seller's stake ($20,000 - $1,200 = $18,800 net). The incentives are structurally misaligned. More commission rate helps, but the agent would need nearly 100% commission to fully align interests.

**Better scheme:** Progressive commission that increases sharply above a reserve price (e.g., 6% up to $500K, then 30% on every dollar above $500K). This concentrates the agent's incentive exactly where the seller wants effort — on maximizing the price above the baseline.

**Failure mode to avoid:** A poorly set reserve price creates the same quota problem as any nonlinear scheme — if $500K is too high and the market won't support it, the agent disengages.

---

### Example 2: Software Programmer Equity Sharing (Wizard 1.0)

**Situation:** You want to develop a chess game (Wizard 1.0). Value = $200,000 if successful. p_H = 0.80, p_L = 0.60. Market wage for routine effort: $50,000. You want high-quality effort (cost = $20,000 above market).

**Step 2 — Minimum bonus:** B >= $20,000 / (0.80 - 0.60) = **$100,000**

**Step 3 — Base pay:** base = $70,000 - (0.80 x $100,000) = **-$10,000** (fine if project fails)

**Fine/equity scheme:** Pay $90,000 on success, -$10,000 (fine) on failure. Average pay = $70,000. Your average profit = $160,000 - $70,000 = $90,000.

**Constrained equity scheme (if fine is unenforceable):** Give programmer 50% equity (worth $100,000 on success, $0 on failure) in exchange for labor only. Average pay = $80,000. Your average profit = $80,000. You pay a $10,000 feasibility premium for moral hazard.

**Risk premium issue:** If the programmer is risk-averse, she values the $100,000 gamble at less than its $80,000 expected value. She needs additional compensation for bearing risk. The optimal solution is a compromise: less than full incentive, some fixed base to absorb risk — but this reduces incentive power and requires accepting some effort below the ideal.

---

### Example 3: Multi-Task Failure — Teaching vs. Research

**Situation:** A professor teaches and conducts research. University wants high effort on both.

**Tasks:** Teaching and research are complements in US research universities — better research informs better teaching; regular teaching keeps researchers grounded. They share time and attention but each makes the other more productive.

**Correct incentive design:** Use strong incentives for both: tenure and promotion contingent on both teaching evaluations and publication record. Bundle the tasks; apply strong incentives across the bundle.

**Incorrect design (French model):** Separate research into specialized institutes, teaching into pure teaching universities. Treats them as substitutes. Results in weaker incentives (research institutes have no teaching to cross-pollinate; teaching universities have no research to inform). US model comparatively succeeds because the complement structure is respected.

**Test:** If you observe a professor excelling at research and neglecting teaching, the tasks may actually be substitutes for that individual (research crowds out teaching energy). The fix is equalization: weight both dimensions more equally in the incentive scheme rather than rewarding only research publications.

---

## References

- `references/bonus-formula-derivation.md` — Full derivation of B >= cost / (p_H - p_L), participation constraint algebra, worked numerical examples, equity-share equivalence
- `references/carrot-stick-analysis.md` — Mathematical equivalence proof, behavioral differences, Stalin case study, CEO compensation analysis, monitoring reliability as the selection criterion
- `references/nonlinear-schemes-and-gaming.md` — Quota-bonus mechanics, sandbagging patterns, Enron-style manipulation, hybrid linear-nonlinear design, real estate commission analysis
- `references/multi-task-incentive-design.md` — Substitute vs. complement taxonomy, Heathrow Airport organizational failure, research-teaching complementarity, multiple-owners incentive dilution formula
- `references/efficiency-wages-and-intrinsic-motivation.md` — Efficiency wage formula derivation, Gneezy/Rustichini experiment results, intrinsic motivation crowding out, career concern substitution table

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Art of Strategy by Avinash K. Dixit, Barry J. Nalebuff.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-information-asymmetry-strategist`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
