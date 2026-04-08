---
name: voting-system-strategist
description: "Analyze, design, or defend against voting system manipulation. Use this skill when a user needs to evaluate how a voting or election procedure will behave strategically — including which candidate or option will actually win under a given system, how an agenda-setter can engineer an outcome, whether a preference cycle makes the 'true will' of the group unknowable, how to choose the voting rule best suited to a group's goals, or when a voter should vote strategically rather than sincerely. Triggers include: user is designing a committee, board, or organizational voting process and wants to know which system is fairest or hardest to manipulate; user suspects the order of votes or the choice of voting method is being used against them; user needs to predict who wins under plurality, runoff, Condorcet pairwise, Borda count, or approval voting; user wants to know whether their group's preferences form a cycle that makes any outcome unstable; user is a voter or participant wondering whether to vote sincerely or strategically; user is analyzing a legislative, judicial, or board vote where agenda control may be shaping the outcome; user needs to apply the median voter theorem to predict where competing positions will converge; user wants to evaluate the pivotal-voter principle to understand when a single vote actually changes outcomes. This skill covers social choice theory, Arrow's impossibility theorem, the Condorcet paradox, agenda control via sequential voting, strategic (insincere) voting, comparison of voting rules, the median voter theorem, approval voting, and pivotal voter analysis. It does NOT cover simultaneous-move strategic games (use nash-equilibrium-analyzer), sequential multi-player negotiation (use other negotiation skills), or auction design."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-art-of-strategy/skills/voting-system-strategist
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-art-of-strategy
    title: "The Art of Strategy"
    authors: ["Avinash K. Dixit", "Barry J. Nalebuff"]
    chapters: [12]
tags: [game-theory, voting, social-choice, decision-making, group-decisions]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Description of the voting situation: participants, options or candidates, known preference orderings or rankings, voting procedure in use or under consideration, and any agenda-setting information"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user describes the voting situation in text or structured form"
discovery:
  goal: "Identify who wins under the current or proposed voting system, flag strategic manipulation risks, detect preference cycles, recommend a voting rule aligned with the group's fairness goals, and — for voters — determine whether sincere or strategic voting is optimal"
  tasks:
    - "Classify the voting situation: election, committee vote, sequential judicial/board decision, resource allocation, or candidate positioning problem"
    - "Elicit the complete preference profile: how many voters, how many options, and each group's preference ranking from best to worst"
    - "Identify the voting rule in use: plurality, runoff, Condorcet pairwise, Borda count, approval, or quota-based"
    - "Apply the Condorcet cycle check: conduct all pairwise comparisons to detect whether majority preferences are intransitive"
    - "Analyze agenda control: if votes are sequential, apply backward induction to reveal which outcome the vote sequence produces and whether it can be engineered"
    - "Assess strategic voting incentives: identify who is a pivotal voter and whether any voter gains by misrepresenting preferences"
    - "Apply the median voter theorem where applicable: find the median preference position and assess whether it is a stable equilibrium"
    - "Recommend or evaluate the voting rule: compare plurality, runoff, Condorcet, Borda, and approval voting on fairness, manipulability, and practicality for the situation"
    - "Deliver: predicted winner under each relevant rule, identified manipulation risks, Condorcet cycle diagnosis, and a recommended design or strategy"
  audience: "Organizational leaders, committee chairs, policy designers, negotiators, board members, political analysts, voters, and anyone designing or participating in group decision-making"
  when_to_use:
    - "User is choosing or evaluating a voting system for a committee, board, election, or organization"
    - "User suspects the agenda or vote order is being manipulated against their interests"
    - "User wants to know who would actually win under different voting rules given known preferences"
    - "User is a voter wondering whether to vote sincerely or strategically when a preferred candidate is unlikely to win"
    - "User is designing rules for a process (judicial, legislative, board) and needs to understand how procedure affects outcome"
    - "User wants to predict where competing candidates or proposals will converge when positioning is strategic"
  quality:
    correctness: null
    depth: null
    actionability: null
    specificity: null
---

# Voting System Strategist

## When to Use

Use this skill whenever a group must aggregate individual preferences into a collective decision and the choice of procedure — or individual voter behavior — is itself strategic.

The foundational insight: **the outcome of a vote is determined by the voting system just as much as by the voters' preferences.** The same set of preferences can produce different winners depending on whether you use plurality voting, runoff, Condorcet pairwise comparison, Borda count, or approval voting. Anyone who controls the procedure controls significant power over the result.

**This skill applies when:**

- Three or more candidates, options, or proposals are under consideration (two-option majority vote is strategically trivial)
- You need to predict who wins, or design a system that produces fair or manipulation-resistant outcomes
- You suspect a cycle in group preferences (majority prefers A over B, B over C, but also C over A)
- Vote order, agenda setting, or sequential decisions may be shaping outcomes
- A voter is considering whether to misrepresent preferences to get a better outcome

**This skill does NOT apply to:**

- Two-option majority votes (vote sincerely; no manipulation is possible)
- Simultaneous-move strategic games among competitors (use the Nash equilibrium skill)
- Price-setting, bidding, or auction design (use auction strategy skills)
- Infinite-horizon political games where reputation and coalition dynamics dominate

---

## Context and Input Gathering

### Required (ask if missing)

- **Options and participants:** How many candidates or proposals are there? How many voters or decision-makers?
  -> Ask: "List every option being considered and every voter or voter-group with a significant block of votes."

- **Preference profile:** What is each voter or voter-group's ranking of the options from most to least preferred?
  -> Ask: "For each distinct group of voters, rank the options from best to worst. Approximate sizes are sufficient."

- **Voting rule in use:** What procedure is being used — plurality (most first-place votes wins), runoff (top two advance), sequential pairwise votes, Borda count (points by rank), approval (vote for as many as you like), or something else?
  -> Ask: "How is the winner actually determined?"

- **Agenda information (if sequential):** If votes are taken in sequence, what is the order?
  -> Ask: "What gets voted on first, and what does the loser of that vote face next?"

### Useful (gather if present)

- Whether voters have accurate information about each other's preferences (affects whether strategic voting is feasible)
- Whether any voter or group controls agenda-setting (order of votes, which options are paired)
- Whether the group is positioned on a single ideological dimension or multiple dimensions (affects median voter applicability)
- Whether the goal is designing a new system or diagnosing an existing one

---

## Execution

### Step 1 — Classify the Voting Situation

**Why:** Different voting situations call for different analytical tools. Misclassifying a sequential agenda-control problem as a simple election leads to wrong predictions. Spending one minute on classification prevents wasted analysis.

**Classification questions:**

**1a. How many options?**
- Two options: simple majority applies; no manipulation possible. This skill is not needed.
- Three or more: proceed — all the interesting strategic dynamics arise here.

**1b. Are votes simultaneous or sequential?**
- Simultaneous: all voters express preferences at once (standard elections). Analyze rule first, then strategic voting.
- Sequential: issues voted in a specified order (legislative votes, judicial panels, board approval sequences). Apply backward induction to identify how agenda order determines the outcome (Step 4).

**1c. What is the goal?**
- Predict who wins under the current system
- Diagnose a manipulation or cycle problem
- Design or recommend a better voting system
- Advise a specific voter on sincere vs. strategic voting

---

### Step 2 — Build the Preference Profile

**Why:** All voting analysis depends on knowing how voters rank options. A preference profile that seems obvious often conceals cycles or surprises when laid out systematically. Constructing it explicitly prevents errors.

**Format:** Build a table with voter groups as columns and options ranked top-to-bottom in each column. Record group sizes (as vote shares or raw counts).

**Example (Condorcet's original three-group setup):**

```
             Group L (40%)   Group M (25%)   Group R (35%)
1st choice       A               B               C
2nd choice       B               C               A
3rd choice       C               A               B
```

**Key rule:** Even if you only care about who wins under one system, complete the full ranking. Incomplete rankings hide cycles and make agenda-control analysis impossible.

---

### Step 3 — Diagnose the Preference Cycle (Condorcet Paradox Check)

**Why:** Majority preferences can be intransitive even when every individual's preferences are perfectly rational and transitive. This is the Condorcet paradox: Group prefers A over B (majority), B over C (majority), and C over A (majority). No option beats all others in pairwise comparison. When a cycle exists, there is no stable "will of the people" — any outcome can be justified, and the voting system or agenda-setter chooses who wins.

**Procedure:**

1. For every pair of options (A vs. B, A vs. C, B vs. C, etc.), count which option is preferred by a majority.
2. Construct a directed graph: draw an arrow from the winner to the loser in each pairwise matchup.
3. Check for cycles: if you can trace a loop (A beats B, B beats C, C beats A), a Condorcet cycle exists.

**Interpreting the result:**

- **No cycle, one option beats all others:** That option is the Condorcet winner. It is the most defensible choice — it would win a head-to-head election against any alternative.
- **Cycle exists:** No option is unambiguously "best." The winner will be determined by the voting system and agenda, not by voter preferences alone. Flag this prominently.

**Worked example (Condorcet's Revolutionary France case):**
- R vs. D: Left (40) + Right (35) = 75 prefer R; Middle (25) prefer D. R wins 75–25.
- R vs. L: Left (40) prefer R; Middle (25) + Right (35) = 60 prefer L. L wins 60–40.
- L vs. D: Left (40) + Middle (25) = 65 prefer D; Right (35) prefers L. D wins 65–35.
- Cycle: R beats D, D beats L, L beats R. No stable winner.

---

### Step 4 — Analyze Agenda Control and Sequential Votes

**Why:** When preferences cycle, the agenda-setter — the person who decides which option gets voted on first and who the loser faces next — effectively chooses the winner. This is not a minor procedural detail; it is the most powerful unrecognized form of strategic influence in committees, legislatures, and judicial panels.

**Backward induction procedure for sequential votes:**

Apply the same backward induction logic used for sequential games (see backward-reasoning-game-solver if needed):

1. Identify the last vote in the sequence. Determine which option wins that final matchup based on majority preferences.
2. Replace the final vote with its outcome. Now the penultimate vote is between the option that lost the previous step and whatever just became the "resolved" outcome.
3. Repeat — move one step back at a time — until you reach the first vote.

**Case study: Three judicial procedures, same preferences**

Three judges with this preference profile (a cycle):

```
               Judge A         Judge B         Judge C
1st choice   Death penalty    Life in prison   Acquittal
2nd choice   Life in prison   Acquittal        Death penalty
3rd choice   Acquittal        Death penalty    Life in prison
```

Three agenda sequences produce three different outcomes:

| Procedure | Vote 1 | If loses → Vote 2 | Winner |
|-----------|--------|-------------------|--------|
| Status quo (innocence/guilt first) | Guilt vs. Innocence → Guilty wins (A+B). Then: Death vs. Life → Life wins (B+C votes for life/acquittal). | Acquittal tied → | **Acquittal** (B tips) |
| Roman tradition (most serious first) | Death vs. not-Death → Death wins (A+C). Then Life vs. Acquittal → Life wins (A+B). | | **Death penalty** |
| Mandatory sentencing (sentence first) | Life vs. Death as required sentence → Life wins (A+B prefer conviction). Then: Convict vs. Acquit → Convict (A+B). | | **Life in prison** |

The same three judges with identical fixed preferences produce death, acquittal, or life in prison depending solely on vote order. **Whoever sets the agenda chooses the outcome.**

**Practical implication:** When you cannot change the preferences, change the agenda. When someone else controls the agenda, predict their preferred outcome and work backward to see what vote order would produce it.

---

### Step 5 — Compare Voting Systems

**Why:** Arrow's impossibility theorem proves no voting system can satisfy all fairness criteria simultaneously. Every system is flawed — but they are not equally flawed. The choice of system is a real design decision with real consequences.

**The five main systems:**

**Plurality (first-past-the-post)**
- Rule: The option with the most first-place votes wins.
- Problem: Spoiler effect. A third candidate drawing votes from a similar alternative can hand victory to the most opposed option. The 2000 US election: Nader's 97,488 Florida votes (majority would have chosen Gore) handed the state to Bush by 537 votes.
- Strategic incentive: Voters abandon sincere first choices for viable alternatives ("wasting a vote").
- Use when: Fast, low-stakes decisions with two dominant options and no third-candidate risk.

**Runoff (two-round)**
- Rule: If no candidate wins an absolute majority in round one, top two advance to a runoff.
- Problem: Eliminates the Condorcet winner if they come third in round one (Danton example: comes third with 25% but would beat both in pairwise). Creates strategic first-round voting by supporters of front-runners who fear the runoff.
- Example: 2002 French election — left-wing voters "naively" voted for fringe candidates in round one, eliminating Jospin (their real preference) and forcing a choice between Chirac and Le Pen in round two.
- Use when: Legitimacy requires a majority winner; strategic coordination risk is low.

**Condorcet method (pairwise)**
- Rule: Each option faces every other in a head-to-head majority vote. The option that beats all others (the Condorcet winner) is elected. Voters submit a full ranking; a computer calculates all matchups.
- Advantage: Selects the option most voters would choose in any direct comparison. Resistant to spoiler effects.
- Problem: When a cycle exists, no Condorcet winner exists — the method fails to produce a result.
- Practical implementation: Voters rank candidates once; software derives all pairwise votes from the ranking. Used successfully at Yale School of Management for teaching prizes.
- Use when: Fairness across all pairwise comparisons is the priority; group is willing to provide full rankings.

**Borda count (point-scoring)**
- Rule: Each voter ranks all options. An option gets n-1 points for each first-place vote, n-2 for second-place, etc. Highest total points wins.
- Advantage: Incorporates intensity of preference across all positions.
- Problem: Highly manipulable — strategic voters can bury a strong opponent by ranking them last, regardless of their true view.
- Use when: Selecting among many options where overall support matters and strategic manipulation risk is low (e.g., sports awards, internal committees with aligned interests).

**Approval voting**
- Rule: Each voter may vote for as many candidates as they approve of. No exclusion — voting for one person does not cost votes on others. The option with the most approval votes wins (or all above a threshold are selected).
- Advantage: Eliminates the spoiler effect entirely. Voters can express true preferences without strategic calculation in threshold-based systems. Proposed by Steven Brams and Peter Fishburn; used by many professional societies.
- Residual problem: When candidates compete for a fixed number of slots, strategic misrepresentation reappears — a voter may withhold approval from a strong candidate to help a weaker favorite.
- Use when: Multiple winners are selected, or a minimum-threshold rule applies. Especially valuable for elections with many candidates and concern about vote-splitting.

**Comparison summary:**

| System | Spoiler risk | Cycle risk | Manipulation ease | Complexity |
|--------|-------------|------------|-------------------|------------|
| Plurality | High | N/A | Low-medium | Minimal |
| Runoff | Medium | N/A | Medium | Low |
| Condorcet | None | Fails if cycle | Low | Medium |
| Borda | Low | N/A | High | Medium |
| Approval | None (threshold) | N/A | Low (threshold) | Low |

---

### Step 6 — Assess Strategic Voting Incentives

**Why:** Sincere voting — voting for your true first preference — is not always rational. When your vote may be pivotal (deciding the outcome), the strategic question is: which vote produces the best outcome for you, given what others will do? Arrow's impossibility theorem guarantees that in any voting system, some voter in some situation will have an incentive to misrepresent their preferences.

**The pivotal voter principle:**

A vote matters only when it breaks or creates a tie. If the outcome is already decided (by a large margin), your vote is a "voice" — it affects margins but not outcomes. Think about your vote as if you are the pivotal voter:

- If you are not pivotal (outcome is decided either way): vote sincerely. Express your true preference.
- If you are potentially pivotal: compare what happens if you vote sincerely vs. strategically, and choose the action that produces your preferred outcome.

**Strategic voting procedure:**

1. Identify your true preference ranking (best to worst).
2. Identify the realistic candidates (options with a realistic chance of being pivotal).
3. Determine which realistic candidate you most prefer.
4. If your most-preferred realistic candidate differs from your sincere first choice, strategic voting means supporting the realistic candidate.

**Case study: The 2000 Nader dilemma**
- Nader supporters' true ranking: Nader > Gore > Bush
- Realistic options: Gore or Bush (Nader cannot win)
- Strategic analysis: If you are in Florida (a swing state), your vote is potentially pivotal in the Gore/Bush decision. Voting for Nader means voting for the option that cannot be pivotal — throwing away influence over the Gore/Bush outcome.
- Strategic vote: Gore

**The paradox:** You can afford to vote sincerely only when your vote does not matter. When your vote does matter, you must vote strategically. Truthful expression is ethical only when it is costless.

**First-mover preference distortion:**

When voting is sequential and your stated preference influences others (foundation funding example, pre-1974 Congressional budgets), there is an incentive to overstate or distort preferences strategically:
- Acting early and committing your resources to one option forces others to cover the alternatives.
- Small actors can exercise disproportionate influence by committing first to secondary priorities, knowing large actors will cover primary needs.

---

### Step 7 — Apply the Median Voter Theorem (Where Applicable)

**Why:** When voters' preferences can be ordered along a single dimension (e.g., liberal to conservative, low-tax to high-tax, lenient to strict policy), the median voter theorem predicts where competing candidates or proposals will converge. The median position is a Nash equilibrium — any candidate who deviates loses votes.

**Conditions for applicability:**

- Preferences must be one-dimensional (can be placed on a single spectrum)
- Each voter has a single "ideal point" on that spectrum and prefers options closer to it
- At least two competing candidates or proposals are adjusting their positions to win

**The median voter theorem:**

The platform that beats all others in majority voting is the one at the median voter's ideal point — the position where exactly half the voters prefer a shift in each direction.

**Why the median is stable:**

- A voter to the left of the median: exaggerating leftward does not move the median position; only rightward pressure affects the median, which works against this voter.
- A voter at the median: their position is adopted; no incentive to distort.
- A voter to the right of the median: symmetric to left-voter case.

**Critical advantage:** The median rule is the unique voting rule (for one-dimensional preferences) where no voter has an incentive to misrepresent their position. Truthful voting is a dominant strategy for everyone.

**Limits:**
- Fails for multi-dimensional preference spaces (taxes AND social issues simultaneously). In two dimensions, no stable equilibrium may exist — preferences cycle across the plane.
- Fails when voters can strategically claim extreme positions to shift the computed average (mean-based rules invite this; median-based rules do not).

**The constitutional stability insight:**

In multi-dimensional preference spaces, simple majority rule (50% threshold) creates cyclical instability — any outcome can be overturned by a new majority coalition. The U.S. Constitution's two-thirds amendment requirement reflects a key finding: a supermajority threshold of approximately 64% or higher creates a stable position at the average of all voter preferences that cannot be beaten. This explains why constitutions require supermajorities to amend: not rigidity, but calibrated stability.

---

### Step 8 — Deliver the Analysis

Structure your output as:

**Voting system diagnosis:** [Which rule is in use; what it produces given the stated preferences]

**Condorcet check result:** [Does a Condorcet winner exist? If so, who? If a cycle exists, what does that mean for stability?]

**Predicted winner(s) by rule:** [For each relevant voting system, who wins and why]

**Agenda control risk:** [If sequential, what does backward induction reveal about the agenda's effect?]

**Strategic voting assessment:** [Who has incentive to vote strategically, and what should they do?]

**Recommendation:** [If designing a system: which voting rule best fits this group's goals and manipulation-resistance needs. If advising a voter: sincere or strategic, and how.]

**Limits:** [Where the analysis depends on preference estimates, single-dimensionality assumptions, or information about others' votes that may not hold]

---

## Key Principles

**Arrow's impossibility theorem: no perfect system exists.** No voting rule simultaneously satisfies all fairness criteria (unanimity, non-dictatorship, independence of irrelevant alternatives, transitivity of group preferences). Every system will be gamed in some scenario. The design question is which failures are least harmful for your context.

**The Condorcet paradox: group irrationality from individual rationality.** Even when every voter is perfectly rational and has transitive preferences, the group's majority preferences can cycle. A cycle means there is no objectively correct winner — only the system or agenda determines the outcome.

**Agenda control is the hidden lever.** Whoever controls the order of sequential votes controls the outcome. This is not corruption — it is mathematics. Backward induction reveals exactly how the agenda maps to the result.

**Strategic voting is rational, not cynical.** When your vote is pivotal, voting sincerely for an unwinnable option is equivalent to not voting at all on the choice that matters. The ethical case for sincere voting holds only when your vote is not pivotal.

**The median voter theorem works for one dimension, fails for two.** On a single axis (liberal/conservative), candidates converge to the median. Add a second axis and convergence disappears — no stable center exists, and any position can be attacked from a direction that assembles a winning coalition.

**Supermajority rules create stability, not just barriers.** A 64%+ threshold can prevent preference cycles in multi-dimensional spaces by making some positions unbeatable. Constitutional supermajority requirements are not mere tradition — they are an engineered solution to the instability of simple majority rule.

**A vote matters only when it creates or breaks a tie.** The vice president's tie-breaking vote is equal in power to any senator's vote, because it decides exactly the same set of outcomes — those decided by a 50–50 split. A vote's impact is not its frequency but the leverage it applies when decisive.

---

## Examples

### Example 1: Diagnosing a Condorcet Cycle (Committee Vote)

**Setup:** A product committee of 12 must choose between Feature A (performance), Feature B (usability), Feature C (integration). Preference profile:

```
          Engineering (5)   Design (4)   Business (3)
1st           A                B             C
2nd           B                C             A
3rd           C                A             B
```

**Pairwise check:**
- A vs. B: Engineering (5) prefer A; Design + Business (7) prefer B. B wins 7–5.
- B vs. C: Engineering + Design (9) prefer B; Business (3) prefer C. B wins 9–3.
- A vs. C: Engineering + Business (8) prefer A; Design (4) prefer C. A wins 8–4.

**Result:** B beats A and C. No cycle. B is the Condorcet winner — the option that would win any head-to-head vote. Recommend Feature B regardless of voting system.

---

### Example 2: Agenda Control in a Board Vote

**Setup:** A board of 7 must choose among Status Quo (S), Proposal A, and Proposal B. The board chair can set the vote order. Preference cycle: A beats S, S beats B, B beats A.

**Backward induction by agenda:**

- Agenda 1: A vs. B first → A wins. Then A vs. S → S wins. **Winner: S**
- Agenda 2: A vs. S first → A wins. Then A vs. B → B wins. **Winner: B**
- Agenda 3: S vs. B first → S wins. Then S vs. A → A wins. **Winner: A**

**Diagnosis:** The chair can produce any of the three outcomes by choosing the agenda. If the chair prefers A, use Agenda 3. If the chair prefers B, use Agenda 2.

**Countermeasure:** If you are not the agenda-setter and you see a cycle, identify which option the agenda is designed to produce by tracing backward induction on the proposed vote order. If it does not serve you, propose a different vote order — or propose a voting system change (Condorcet pairwise) that eliminates agenda sensitivity.

---

### Example 3: Strategic Voting Decision

**Setup:** A primary election with three candidates: your preferred candidate X (progressive, 15% polling), candidate Y (moderate, 45%), and candidate Z (conservative, 40%). You prefer X > Y > Z.

**Analysis:**
- Is X viable? No — 15% cannot win.
- Are you potentially pivotal in Y vs. Z? Yes — this is close.
- What is your pivotal choice? Y vs. Z, and you strongly prefer Y.
- Strategic vote: Y.

**Why sincere voting hurts you:** Voting for X means your vote does not participate in the Y vs. Z decision. If Y loses to Z by a small margin, your sincere vote contributed to your worst outcome.

**The paradox stated plainly:** It is only okay to vote sincerely (for X) when the election is not close — when your vote will not matter anyway. The moment your vote matters, strategic voting for your best viable option is the rational choice.

---

### Example 4: Choosing a Voting System for an Organization

**Setup:** A professional society with 200 members needs to elect 3 people to an advisory board from 12 nominees. Currently uses plurality with each voter casting 3 votes.

**Problem diagnosis:** With 12 candidates and 3 votes each, coordinated blocs can dominate — a minority with focused votes can sweep all three seats. The Joe DiMaggio effect: the obvious strongest candidate gets abandoned by strategic voters who "know they're safe" and redirect votes to favorites who need help. Result: strongest candidate sometimes fails to be elected.

**System options:**

- Plurality (current): High manipulation risk from vote concentration. Weakest option.
- Approval voting: Each voter approves as many of the 12 as desired; top 3 by approval votes win. Eliminates strategic vote-rationing — no cost to approving a strong candidate. Best fit for threshold-based selection with many candidates.
- Condorcet pairwise: Elects the option that beats all others head-to-head. Not well-defined for selecting 3 of 12 simultaneously; complex to implement.
- Borda count: Full ranking of all 12; points assigned by rank. More expressive but highly manipulable — voters can bury strong opponents.

**Recommendation:** Approval voting. Approving a deserving candidate never hurts them. Strategic misrepresentation requires complex reasoning about competitors' mutual approval rates — unlikely to be widespread. Implement with a threshold (e.g., elected if approved by >50% of voters) or seat-limit (top 3 by approval count).

---

## References

- `references/voting-systems-comparison.md` — Detailed rules, examples, fairness criteria, and failure modes for plurality, runoff, Condorcet, Borda, and approval voting
- `references/condorcet-cycle-detection.md` — Step-by-step pairwise comparison procedure, cycle diagnosis, worked examples with three and four candidates
- `references/agenda-control-backward-induction.md` — Applying backward induction to sequential vote sequences; all-outcomes-by-agenda table construction; legislative and judicial examples
- `references/arrows-impossibility-theorem.md` — The five fairness criteria, formal statement of impossibility, and practical implications for voting system design
- `references/median-voter-theorem.md` — One-dimensional convergence proof, strategic preference exaggeration under mean-based rules, multi-dimensional failure, constitutional supermajority insight

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Art of Strategy by Avinash K. Dixit, Barry J. Nalebuff.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
