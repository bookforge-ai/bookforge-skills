# Condorcet Cycle Detection

Step-by-step procedure for checking whether a group's majority preferences are transitive or form a cycle.

---

## What a Condorcet Cycle Is

A Condorcet cycle (also called a preference cycle or voting paradox) occurs when majority preferences are intransitive:

- Majority prefers A over B
- Majority prefers B over C
- Majority prefers C over A

This is possible even when every individual voter has perfectly transitive preferences. The paradox arises at the group level through aggregation. It was first formally described by the Marquis de Condorcet in the 18th century.

**Why it matters:** When a cycle exists, there is no option that represents "the will of the people." Any option can be defeated by another in a pairwise vote. The winner is determined entirely by the voting procedure and agenda, not by voter preferences.

---

## Detection Procedure

### Step 1: Construct the preference profile table

List all voter groups as columns. List all options as rows within each column, ranked from most to least preferred.

```
              Group 1 (size)   Group 2 (size)   Group 3 (size)
1st choice       [option]         [option]         [option]
2nd choice       [option]         [option]         [option]
3rd choice       [option]         [option]         [option]
```

### Step 2: Enumerate all pairwise matchups

For n options, there are n(n-1)/2 pairwise matchups.
- 3 options: 3 matchups (A-B, A-C, B-C)
- 4 options: 6 matchups
- 5 options: 10 matchups

### Step 3: For each matchup, count majority preference

For each pair (X vs. Y), add up the voters whose ranking places X above Y. If more than half, X beats Y in the pairwise comparison. Record the winner with an arrow: X → Y means X beats Y.

### Step 4: Build the dominance graph

Draw each option as a node. For each pairwise result, draw an arrow from the winner to the loser.

### Step 5: Check for cycles

Trace paths through the graph. If any path forms a loop (A → B → C → A), a cycle exists.

- No cycle + one node with arrows to all others: Condorcet winner exists. This is the option to elect under the Condorcet method.
- Cycle involving all options: No Condorcet winner. The outcome is entirely procedure-determined.
- Partial cycle (some options in cycle, others not): The options outside the cycle may be stable; options within the cycle have no stable majority ranking among themselves.

---

## Worked Example: The Revolutionary France Case

**Preference profile:**

```
             Left (40)   Middle (25)   Right (35)
1st choice      R            D             L
2nd choice      D            L             R
3rd choice      L            R             D
```

**Pairwise matchups:**

R vs. D:
- Left prefers R (40), Right prefers R (35): total 75 prefer R
- Middle prefers D (25): total 25 prefer D
- R beats D, 75–25

R vs. L:
- Left prefers R (40): 40 prefer R
- Middle prefers L (25), Right prefers L (35): total 60 prefer L
- L beats R, 60–40

D vs. L:
- Left prefers D (40), Middle prefers D (25): total 65 prefer D
- Right prefers L (35): 35 prefer L
- D beats L, 65–35

**Dominance graph:**

```
R → D
D → L
L → R
```

**Result:** Complete cycle. R beats D, D beats L, L beats R. No Condorcet winner exists.

**Implication:** Under any voting procedure, someone will be able to argue their preferred option should win by choosing the right comparison. The agenda-setter decides the winner.

---

## Worked Example: No Cycle (Product Committee)

**Preference profile:**

```
          Engineering (5)   Design (4)   Business (3)
1st           A                B             C
2nd           B                C             A
3rd           C                A             B
```

**Pairwise matchups:**

A vs. B: Engineering (5) prefer A; Design + Business (7) prefer B. B wins 7–5.
B vs. C: Engineering + Design (9) prefer B; Business (3) prefer C. B wins 9–3.
A vs. C: Engineering + Business (8) prefer A; Design (4) prefer C. A wins 8–4.

**Dominance graph:**

```
B → A
B → C
A → C
```

**Result:** No cycle. B beats A and B beats C — B is the Condorcet winner. B would win any head-to-head vote. Recommend B regardless of which voting system is used.

---

## Four-Candidate Cycle Check

With four options (A, B, C, D), run six pairwise matchups: A-B, A-C, A-D, B-C, B-D, C-D.

Possible outcomes:
- One option beats all three others: Condorcet winner, no cycle.
- One option loses to all three others (Condorcet loser): Can still have a Condorcet winner among the remaining three.
- Partial cycle among three: Two options may rank clearly; the third three form a cycle.
- Complete four-way cycle: Very unusual but possible.

For complex profiles, a systematic approach is to build the full dominance matrix: a grid where entry (X, Y) = 1 if X beats Y in pairwise, 0 otherwise. The Condorcet winner is the row with all 1s (except the diagonal).

---

## What To Do When a Cycle Exists

1. **Switch to a cycle-resistant rule:** Condorcet method with a tiebreaker (e.g., elect the option with the smallest maximum pairwise defeat).

2. **Use approval voting:** Approval voting does not depend on transitivity. Each voter simply approves options above their personal quality threshold.

3. **Restrict the agenda:** Identify which option the current vote sequence is engineered to produce. If it does not serve you, propose a different vote order or a system change.

4. **Accept the instability:** Acknowledge that the group's preferences are genuinely cyclical — any outcome requires a procedure-based choice, not a preference-based one. Make the choice transparent rather than pretending the system is neutral.
