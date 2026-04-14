# Forced Prioritization Worksheet

Use this worksheet when the user has multiple candidate points and cannot pick one. It operationalizes the "if you say three things, you say nothing" rule from Carville's 1992 Clinton war room.

## The Four Questions

For each candidate point in the inventory, answer:

### Q1 — The Removal Test
"If I delete this point, can the message still achieve its goal for this audience?"
- **Yes** -> CUT. This point is decorative, not load-bearing.
- **No** -> KEEP. This point is structural.

### Q2 — The Delegation Test (Southwest)
"Could a new hire make a contested trade-off decision from this point alone?"
- **Yes** -> this point is actionable for frontline decisions. Strong candidate for #1.
- **No** -> this point describes atmosphere, not action. Weak candidate.

### Q3 — The Outsider-Judgeable Test (JFK)
"Could an outsider verify success or failure against this point in a fixed timeframe?"
- **Yes** -> the point has a falsifiable end state. Strong candidate.
- **No** -> the point is corporate atmosphere. Weak candidate.

### Q4 — The Six-Month Recall Test
"If the audience remembers only one thing six months from now, would I rather they remember this point or another?"
- This is the tiebreaker when Q1-Q3 leave multiple survivors. Force the choice. Ties are not permitted.

## Cut List Format

When writing the cut list in `core-message.md`, use this format for each cut point:

```
- <cut point> — FAILED <Q1|Q2|Q3|Q4>: <one-sentence rationale>
```

Example:

```
- "Our platform is enterprise-grade" — FAILED Q1: removing this does not change whether a buyer acts.
- "We have 99.9% uptime" — FAILED Q2: not something a sales rep uses to close a deal.
- "We're the fastest-growing in our category" — FAILED Q3: "fastest-growing" is not outsider-verifiable without comparative data.
- "We save customers time AND money" — FAILED Q4: "time" survived the other tests; "money" is the weaker co-claim and gets cut in the tiebreaker.
```

## Anti-Patterns to Flag During Prioritization

- **"Everything is #1"** — the author refuses to rank. Push back: "If the audience can only remember one, which one?"
- **Burying the lead** — the #1 point appears after paragraph 2. Inverted-pyramid journalism exists because readers quit; the most important fact must come first.
- **Compound #1** — "We are fast, affordable, and reliable" — three #1s in a coat. Force the split; pick one.
- **Process as message** — "We use AI to..." is not an end state, it is a method. Ask: "What does the audience *get* because of the method?" That is the #1.
