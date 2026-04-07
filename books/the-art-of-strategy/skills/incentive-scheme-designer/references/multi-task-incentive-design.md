# Multi-Task Incentive Design

## The Multi-Task Problem

Most agents perform multiple tasks simultaneously. When you add a strong financial incentive to one task, it affects effort allocation across all tasks. Whether this is helpful or harmful depends on the relationship between the tasks.

**Core insight (Holmstrom and Milgrom):** An agent with limited effort will direct that effort toward tasks with higher expected marginal payoff. If incentives are unequal across tasks, effort flows to the high-incentive task at the expense of others.

## Substitutes vs. Complements

**Substitute tasks:** More effort on Task A reduces the net productivity of effort on Task B. They compete for a shared resource — time, attention, physical energy, cognitive capacity.

*Diagnostics:*
- Working harder on A makes the agent more tired for B
- Time spent on A is unavailable for B
- Skills required for A crowd out skills for B
- Being very good at A makes being good at B harder (specialization)

*Examples:*
- Corn farming and dairy farming (shared labor hours and physical energy)
- Customer service calls (measured) vs. quality follow-up (not measured)
- Short-term revenue (this quarter) vs. customer satisfaction (long-term)
- Teaching (time-intensive) vs. research (also time-intensive, if not complementary)

**Complement tasks:** More effort on Task A raises the net productivity of effort on Task B. Effort on one makes the other more productive.

*Diagnostics:*
- Success on A makes B easier or more valuable
- Skills built for A transfer to B
- Insights from A generate better outputs in B
- A and B share upstream inputs that benefit both

*Examples:*
- Beekeeping and apple orcharding (bees pollinate apple trees)
- Research and teaching at research universities (research informs lectures; teaching sharpens research questions)
- Prospecting and closing sales (better prospects → easier closes)
- Security and checkout at airports (both part of the same passenger flow process)

## Design Rules

**When tasks are substitutes:**

Strong incentives on Task A divert effort from Task B. If B is important but hard to measure (quality, safety, long-term value), incentivizing only A destroys B performance.

*Rules:*
1. Equalize incentive strength across all tasks you care about
2. Use weaker incentives on each task than you would for a single-task role
3. Consider whether some tasks can be unmeasured entirely — but only if they are genuinely secondary
4. If you cannot avoid unequal measurement, ensure the well-measured task is the most important one

*Example:* Teachers whose pay is tied to standardized test scores (measurable) have incentives to teach to the test at the expense of critical thinking, creativity, and subjects not on the test. The fix: either include the hard-to-measure dimensions in the evaluation or reduce the weight on the easily-measured dimension.

**When tasks are complements:**

Strong incentives on all tasks amplify each other. No tradeoff between tasks; pushing hard on A helps B too.

*Rules:*
1. Use strong incentives on all tasks in the bundle
2. Bundle complementary tasks together under one person (or one team with shared incentives)
3. The complementarity creates a multiplier: incentive investment yields above-proportional returns

*Example:* A research university professor incentivized strongly on both publications and teaching quality performs better on both than one incentivized only on publications. The synergy is real.

## Organizational Design Implications

**Group complementary tasks together; separate substitute tasks:**

- Assign sets of complementary tasks to the same person, team, or division
- Give them strong incentives on all tasks in their bundle
- Assign substitute tasks to different people or divisions with independent incentive schemes
- This way, each person faces a bundle of complements with no internal diversion problem

**The Heathrow Airport failure:**

Airport operations are complementary: check-in, security, shopping, boarding, and ground transport are sequential steps in a single passenger flow. All should be managed by one entity with one aligned incentive: maximize passenger throughput and satisfaction.

UK government structure:
- British Airports Authority (BAA) owns and manages the shopping areas, landing fee setting, and physical terminals
- Police manage security (separate budget, separate incentive)
- Regulators set landing fees (separate mandate: minimize airline costs)

Results:
- BAA profits from leases on shops → allocates too little space to security checks (security reduces shopping time)
- Regulator sets landing fees too low → too many airlines choose Heathrow → congestion
- Police budget not tied to passenger throughput → security staffing often inadequate at peak times

Each entity's incentive partially cancels others'. The complementary tasks are in practice governed like substitutes under an adversarial multi-owner structure.

**Multiple owners / bosses — the incentive dilution formula:**

When one agent answers to N bosses with opposed interests, the total incentive strength is approximately:

```
total_incentive_strength ∝ 1 / N
```

This explains why it is hard to get anything done in international bodies (196 sovereign nations as bosses), large committees, and complex coalition governments. Mathematical models show that in the limit of fully opposed principals with equal power, incentive strength approaches zero — "no man can serve two masters."

**Research vs. teaching as a test case:**

*Substitutes hypothesis:* Research takes time and energy from teaching. Optimize by separating: specialized research institutes (CNRS model in France) and teaching-only universities.

*Complements hypothesis:* Research deepens teaching (researchers bring frontier knowledge to the classroom); teaching sharpens research (student questions reveal gaps; teaching forces clarity). Optimize by combining: research universities (US model).

*Evidence:* The comparative success of US research universities in producing both top research and high-quality graduates relative to the French model suggests complements is the better characterization — at least for top-tier universities. The combination does work better when both tasks genuinely feed each other.

## Competition Between Workers as Relative Performance

When many workers do the same task simultaneously under similar conditions, their luck is correlated (all face the same market, weather, or economic conditions). Comparing performance across workers removes the common luck component and yields a cleaner measure of relative effort.

**Relative performance incentives (tournaments):**

- Investment fund managers ranked by returns relative to peer group benchmark
- Dual-source suppliers evaluated against each other on the same contract
- Two proofreaders assigned overlapping pages — both measure the same "true" number of errors, so relative performance reveals who shirked

*Advantages:*
- Filters out common luck; evaluates effort more accurately
- Does not require knowing the absolute level of effort required
- "Your peers performed much better" is a credible response to bad luck excuses

*Disadvantages:*
- Creates incentive for sabotage of peers (reduce their performance rather than improve your own)
- Requires comparable tasks and correlated conditions
- Agents should not know who their comparison group is (prevents strategic coordination)
- Creates a "rat race" dynamic where all agents work extremely hard but relative rankings are unaffected

*The $2/typo first-finder tournament (Yale proofreading experiment):*
All copies of the book distributed to students; reward $2/typo but only to the first finder. The optimal strategy: start from the back of the book (fewer competitors have read the last chapters). Catherine Pichotta won by thinking ahead about competitor behavior, not just working harder. Strategic behavior in tournaments can be as important as raw effort.
