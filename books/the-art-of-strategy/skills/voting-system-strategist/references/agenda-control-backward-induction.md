# Agenda Control and Backward Induction in Sequential Votes

How to apply backward induction to sequential voting sequences, construct all-outcomes-by-agenda tables, and identify or counter agenda manipulation.

---

## Why Agenda Order Determines Outcomes

When preferences cycle (a Condorcet cycle exists), there is no option that beats all others. This means:

- For any option X, there exists some option Y that beats X in a pairwise majority vote
- For any option Y, there exists some option Z that beats Y
- And so on, cycling back to X

The agenda-setter exploits this by choosing which pair votes first. The loser of each vote is eliminated; the winner faces the next option. By controlling the sequence, the agenda-setter can engineer any option to be the final winner.

**This is not corruption — it is mathematics.** The agenda-setter is applying backward induction. Any participant who knows preference profiles can do the same analysis to predict or counter the manipulation.

---

## Backward Induction Procedure for Sequential Votes

This is the same backward induction used in sequential game analysis (see backward-reasoning-game-solver), applied to vote sequences.

### Step 1: Map the agenda sequence

Identify the vote order: which two options are voted on first, what the loser is eliminated from, and who the winner faces next.

Example with three options (A, B, C) and agenda "A vs. B first, winner faces C":

```
Round 1: A vs. B → winner
Round 2: [Round 1 winner] vs. C → final winner
```

### Step 2: Resolve the last vote first

Using the preference profile, determine who wins the final matchup (Round 2 in the example). This is known because all pairwise outcomes are determined by majority preference.

### Step 3: Fold backward to the first vote

Now that you know what winning Round 1 leads to (either the Round 1 winner or C in the final), replace Round 2 with its result. Round 1 becomes a choice between: "what happens if A wins Round 1" vs. "what happens if B wins Round 1."

If voters look ahead (as sophisticated decision-makers do), they vote in Round 1 based on which final outcome they prefer — not necessarily based on their honest A-vs-B preference.

### Step 4: Identify the actual winner

The option that emerges from this backward induction analysis is the predicted winner under sophisticated voting. Under naive voting (voters ignore future rounds), use the direct pairwise results.

---

## All-Outcomes-by-Agenda Table

For three options and a cycle, construct this table to show what each agenda produces.

**Three options with cycle:** A beats B, B beats C, C beats A.

| Agenda sequence | Round 1 | Round 2 | Naive winner | Sophisticated winner |
|----------------|---------|---------|-------------|---------------------|
| A vs. B → winner vs. C | A beats B | [A] vs. C → C wins | C | C |
| A vs. C → winner vs. B | C beats A | [C] vs. B → B wins | B | B |
| B vs. C → winner vs. A | B beats C | [B] vs. A → A wins | A | A |

**Reading the table:** The option placed last (facing the round-2 winner) always wins in a complete cycle under naive voting. The "protected" option — the one that doesn't have to win in round 1 — is the ultimate victor.

**For agenda-setters:** If you want option X to win, construct the agenda so X faces the final opponent in the last round, having been protected through the early votes.

**For agenda-challengers:** If you suspect manipulation, identify which option is being "protected" by the proposed agenda. Then propose an alternative agenda that protects your preferred option instead.

---

## Case Study: Three Judicial Procedures

This is the Pliny the Younger problem from Chapter 12. Three judges, three possible outcomes (Death penalty, Life in prison, Acquittal), with a preference cycle.

**Preference profile:**

```
               Judge A          Judge B         Judge C
1st choice   Death penalty   Life in prison    Acquittal
2nd choice   Life in prison  Acquittal         Death penalty
3rd choice   Acquittal       Death penalty     Life in prison
```

**Pairwise results:**
- Death vs. Life: A prefers Death (1), B prefers Life (1), C prefers Death (1). Death wins 2–1.
- Death vs. Acquittal: A prefers Death (1), B prefers Acquittal (1), C prefers Acquittal (1). Acquittal wins 2–1.
- Life vs. Acquittal: A prefers Life (1), B prefers Life (1), C prefers Acquittal (1). Life wins 2–1.

**Cycle:** Death beats Life, Life beats Acquittal, Acquittal beats Death.

**Agenda analysis (sophisticated voters who look forward and reason backward):**

Procedure 1 — Status Quo (guilt/innocence first, then sentencing):
- Stage 2 if guilty: Death vs. Life → Death wins (A+C prefer Death over Life). No wait — check: A prefers Death, C prefers Death over Life? C's ranking: Acquittal > Death > Life. So C prefers Death over Life. Death wins 2–1.
- Stage 1: Guilt (leading to Death) vs. Innocence (Acquittal). A prefers Death > Acquittal → votes Guilty. B prefers Acquittal > Death → votes Innocent. C prefers Acquittal > Death → votes Innocent. Acquittal wins 2–1.
- **Sophisticated winner: Acquittal.**

Procedure 2 — Roman Tradition (most serious first):
- Stage 2 if Death rejected: Life vs. Acquittal → Life wins (A+B prefer Life over Acquittal). A: Life > Acquittal. B: Life > Acquittal. C: Acquittal > Life. Life wins 2–1.
- Stage 1: Death vs. [if rejected → Life]. A prefers Death over Life → votes Death. B prefers Life over Death → votes against Death. C prefers Death over Life → votes Death. Death wins 2–1.
- **Sophisticated winner: Death penalty.**

Procedure 3 — Mandatory Sentencing (sentence first, then guilt):
- Stage 2: Conviction vs. Acquittal, given that conviction means Life (if that's the set sentence). A+B prefer conviction (Life) over acquittal. C prefers acquittal. Conviction wins 2–1.
- Stage 1: Which sentence? Death vs. Life. If Death is the sentence, C votes against conviction in Stage 2, so acquittal wins. If Life is the sentence, conviction wins. Judges look ahead: A prefers Death > Life but knows death sentence leads to acquittal. So A prefers Life sentence (leads to conviction and life) over Death sentence (leads to acquittal). B prefers Life > Acquittal, and Life sentence leads to conviction+life — B votes for Life. C prefers acquittal over both — C votes for Death sentence (knowing it leads to acquittal). Life wins 2–1.
- **Sophisticated winner: Life in prison.**

**Summary:** Same three judges, identical fixed preferences, three different outcomes from three procedures. The choice of judicial system determines the verdict.

---

## The "Love a Loathed Enemy" Pattern

A more subtle form of agenda control: committing resources early to force others to bear costs.

**Mechanism:**
1. Multiple parties share responsibility for a common priority (the "top priority" that all must fund together).
2. One party acts first, committing all their resources to their secondary priority.
3. The remaining parties are forced to bear the full cost of the common priority, leaving nothing for their own secondary priorities.

**Result:** The first mover achieves their secondary priority at the expense of the others' secondary priorities — using the shared top priority as a lever.

**Congressional budget analog (pre-1974 Budget Act):** Congress voted on individual expenditure items first. Unimportant items were approved early; by the time critical items came to a vote, the budget was nearly exhausted, and cutting them was politically impossible. The 1974 Budget Act reformed this by requiring votes on budget totals first.

**Countermeasure:** Require commitment to shared priorities before secondary priorities are addressed. Vote on budget totals before line items. Establish that shared responsibilities must be satisfied proportionally before any party can divert resources to secondary goals.
