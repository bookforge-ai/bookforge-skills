# Voting Systems Comparison

Detailed rules, fairness criteria, failure modes, and worked examples for the five main voting systems covered in Chapter 12.

---

## Fairness Criteria (Arrow's Framework)

Any voting system can be evaluated against these criteria. Arrow proved no system satisfies all of them simultaneously.

1. **Unanimity (Pareto efficiency):** If every voter prefers A over B, the group result must prefer A over B.
2. **Non-dictatorship:** No single voter's preferences always determine the group outcome regardless of others.
3. **Independence of irrelevant alternatives (IIA):** The group ranking of A vs. B should not change if a third option C is introduced or removed.
4. **Transitivity:** If the group prefers A over B and B over C, it must prefer A over C.
5. **Unrestricted domain:** The system must handle any possible combination of individual preference orderings.

Arrow's impossibility theorem: No voting system with 3+ options can satisfy all five criteria simultaneously. Every system violates at least one.

---

## Plurality (First-Past-the-Post)

**Rule:** Each voter casts one vote for their top choice. The option with the most votes wins.

**Fairness criteria violated:** Independence of irrelevant alternatives (IIA). Adding or removing a third candidate changes the outcome between the two leaders.

**Failure mode — spoiler effect:** A third candidate who cannot win draws votes from a similar candidate, handing victory to the opposing side. The 2000 US election is the textbook case: Nader's 97,488 votes in Florida (most would have gone to Gore) decided a race Bush won by 537.

**Strategic incentive:** Voters abandon sincere first preferences for "viable" candidates. Polls become self-fulfilling: candidates announced as long-shots lose support independent of merit.

**When to use:** Two dominant options with negligible third-candidate risk. Fast decisions where simplicity matters. Internal straw polls.

**When not to use:** Elections with three or more competitive candidates. Any context where the spoiler effect would produce an outcome most voters strongly oppose.

---

## Runoff (Two-Round)

**Rule:** All candidates compete in round one. If no candidate wins an absolute majority (>50%), the top two advance to a runoff election. The runoff winner wins the election.

**Fairness criteria violated:** Independence of irrelevant alternatives. The Condorcet winner can be eliminated in round one if they come third in first-round plurality, even though they would beat both finalists head-to-head.

**Failure mode — first-round naive voting:** Voters who "vote with their hearts" for fringe candidates in round one may accidentally eliminate their second-choice viable candidate. The 2002 French election: left-wing voters split among fringe parties in round one, eliminating Jospin (socialist, second choice for most leftists). The runoff was between Chirac and Le Pen — an outcome no left-winger wanted.

**Strategic incentive:** In round one, supporters of weak candidates should consider whether their sincere vote risks eliminating the viable candidate they prefer. Robespierre supporters in the worked example could vote strategically for Danton in round one to ensure their preferred outcome.

**When to use:** When a majority winner is required for legitimacy. When voter coordination in round one is reliable enough to avoid the Jospin failure mode.

**When not to use:** When the Condorcet winner is likely to poll third in first-round plurality (weak plurality support but strong pairwise performance). Environments where first-round strategic coordination is difficult.

---

## Condorcet Method (Pairwise Majority)

**Rule:** Each option competes against every other in a head-to-head majority vote. The option that beats all others — the Condorcet winner — is elected. In practice, voters submit a complete ranking once; a computer calculates all pairwise matchups from the single ranking.

**Fairness criteria violated:** None of Arrow's five criteria in isolation — but the method fails entirely (produces no result) when a Condorcet cycle exists.

**Advantage:** Selects the option a majority would choose in any direct comparison. No spoiler effect — adding or removing a candidate who is not the Condorcet winner does not change the result. Voters can express true preferences without strategic calculation (in the absence of cycles).

**Failure mode — Condorcet cycle:** When majority preferences are intransitive (A beats B, B beats C, C beats A), no Condorcet winner exists. The method cannot produce a result without supplementary rules (e.g., elect the option with the smallest maximum defeat).

**Practical implementation:** Rank your candidates. The computer derives all pairwise votes from your ranking. In a six-candidate election, this replaces 15 separate binary votes with a single ranked ballot. Used at Yale School of Management for annual teaching awards.

**When to use:** When fairness across all pairwise comparisons is the primary criterion. Committees or organizations willing to submit full rankings. Situations where a spoiler effect would be catastrophic.

**When not to use:** When preference cycles are likely (diverse preferences, many options). When voters are unwilling or unable to rank all options completely.

---

## Borda Count (Point-Scoring)

**Rule:** Each voter ranks all options. Option ranked 1st gets n-1 points, 2nd gets n-2 points, ..., last gets 0 points (where n = number of options). The option with the highest total points wins.

**Fairness criteria violated:** Independence of irrelevant alternatives. Adding a new candidate changes the point allocation for existing candidates.

**Advantage:** Captures intensity of preference across all positions. A candidate widely regarded as second-best by everyone may beat a candidate who is first choice for some and last choice for others — this may better reflect overall support.

**Failure mode — strategic burial:** Voters can improve their preferred candidate's relative standing by ranking a strong opponent last, regardless of their true view. This is both common and effective, making Borda count among the most manipulable systems.

**Strategic incentive:** High. Any voter who knows others' preferences has an incentive to rank their preferred candidate first and their main competitor last.

**When to use:** Sports awards, internal committee rankings where strategic manipulation is unlikely (aligned interests, small groups, social norms against gaming). Academic awards with professional norms.

**When not to use:** Political elections or competitive organizational contexts. Any environment where participants have strong incentives to misrepresent preferences.

---

## Approval Voting

**Rule:** Each voter may vote for (approve of) as many candidates as they wish. Voting for one candidate does not cost votes on any other. The candidate with the most approval votes wins (threshold variant: all candidates above a set percentage are elected).

**Fairness criteria violated:** Independence of irrelevant alternatives in quota/competitive contexts (see failure mode below).

**Core advantage:** Eliminates the spoiler effect in threshold-based elections. Approving a deserving candidate never hurts them — there is no cost to honest expression of support for multiple candidates. Voters need not consider electability when casting approval votes.

**Failure mode — competitive quota context:** When exactly n seats are filled by top-n vote-getters, candidates compete with each other indirectly in voters' minds. A voter who approves both a strong candidate (who will get in anyway) and a borderline candidate inadvertently helps the borderline candidate as much as the strong one. If the voter cares about the composition of the group (e.g., "not two sluggers in the same year"), they may withhold approval from a deserving candidate to affect the slate composition.

**The DiMaggio problem:** In a quota election with Joe DiMaggio (obvious winner), Marv Throneberry, and Bob Uecker, a voter who knows DiMaggio is safe may give both votes to a weaker candidate they prefer — concentrating votes on borderline candidates at the expense of the strongest. If all voters reason this way, DiMaggio is shut out.

**When to use:** Elections where all candidates meeting a quality threshold should be selected (Baseball Hall of Fame model, professional society boards). Elections with many candidates and concern about vote-splitting. Any context where the spoiler effect is the main problem and quota competition is low.

**When not to use:** Competitive fixed-slot elections where voters have strong preferences about the composition of the winning group, not just the quality of individual winners.

---

## System Selection Guide

| Goal | Recommended system |
|------|-------------------|
| Eliminate spoiler effect | Condorcet or Approval |
| Require majority winner | Runoff |
| Capture overall support across ranks | Borda (low-manipulation environment only) |
| Select multiple winners from large field | Approval (threshold rule) |
| Resistance to preference distortion | Condorcet (no cycle) or Approval (threshold) |
| Simplicity | Plurality |
| Strategic robustness for political elections | Condorcet |
