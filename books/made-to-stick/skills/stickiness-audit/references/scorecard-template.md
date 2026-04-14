# Stickiness Scorecard Template

Copy this template when producing the audit output file. Every section is required. Every score needs a quoted passage as evidence. Do NOT add a "total score" row — the rubric is a checklist, not an equation.

---

```markdown
# Stickiness Scorecard — {draft name or first-line title}

## Audit Frame

- **Draft:** {title or opening line}
- **Audience:** {role + context + what they care about — one sentence}
- **Goal:** {what the reader must remember, feel, or do}
- **Channel:** {email / tweet / landing page / slide / memo / speech / other}
- **Compared against:** {prior version filename if applicable, else "first draft"}
- **Assumed default(s):** {any assumption filled in for missing context, e.g., "[assumed goal: sign up for trial]"}

---

## Scorecard

| Dimension            | Score | Verdict (one line)                              | Evidence (quoted from draft)             |
|----------------------|-------|-------------------------------------------------|------------------------------------------|
| Simple               | 0/1/2 | {e.g., "no identifiable core"}                  | "{quoted passage}"                       |
| Unexpected           | 0/1/2 | {...}                                           | "{...}"                                  |
| Concrete             | 0/1/2 | {...}                                           | "{...}"                                  |
| Credible             | 0/1/2 | {...}                                           | "{...}"                                  |
| Emotional            | 0/1/2 | {...}                                           | "{...}"                                  |
| Stories              | 0/1/2 | {...}                                           | "{...}"                                  |
| Curse of Knowledge   | 0/1/2 | {...}                                           | "{...}"                                  |

**Rubric reminder:** 0 = fails the dimension, 1 = partial, 2 = kidney-heist level. Do not sum the scores.

---

## Kidney-Heist Comparison

{One sentence: which dimensions the draft hits at 2/2 kidney-heist level and which it misses. Example: "Credibility is kidney-heist-level; Emotional and Stories axes are inverted — the draft leads with statistics where the kidney heist would lead with one person in one bathtub."}

---

## Anti-Pattern Findings (Step 9 cross-cutting pass)

- [ ] **Burying the lead** — {present / not present; if present, where}
- [ ] **Decision paralysis** — {present / not present; if present, which competing asks}
- [ ] **Common-sense sedation** — {present / not present; if present, which sentences}
- [ ] **Analysis by jargon** — {present / not present; if present, which terms}

(If any fire, these explain why a draft can score 1s across dimensions and still fail to land.)

---

## Top 3 Rewrite Targets

Ranked by (severity × how much of the draft they poison). Each target names the dimension, quotes the passage, prescribes a specific fix, and estimates effort.

1. **{Dimension}** — "{quoted passage}"
   - **Why it hurts:** {one sentence}
   - **Fix:** {specific rewrite direction, not "make it better"}
   - **Effort:** S / M / L

2. **{Dimension}** — "{quoted passage}"
   - **Why it hurts:** {...}
   - **Fix:** {...}
   - **Effort:** S / M / L

3. **{Dimension}** — "{quoted passage}"
   - **Why it hurts:** {...}
   - **Fix:** {...}
   - **Effort:** S / M / L

---

## Handoff Recommendations

For each dimension that scored 0 or 1, name the specialist skill to invoke next and say why that skill (not another) is the right move.

- **Simple 0/1** -> invoke `core-message-extractor` because {reason}.
- **Unexpected 0/1** -> invoke `curiosity-gap-architect` because {reason}.
- **Concrete 0/1** -> invoke `concrete-language-rewriter` because {reason}.
- **Credible 0/1** -> invoke `credibility-evidence-selector` because {reason}.
- **Emotional 0/1** -> invoke `emotional-appeal-selector` because {reason}.
- **Stories 0/1** -> invoke `story-plot-selector` because {reason}.
- **Curse of Knowledge 0/1** -> invoke `curse-of-knowledge-detector` because {reason}.
- **Anti-pattern hits** -> invoke `sticky-message-antipattern-detector` for deeper diagnosis of {specific anti-pattern}.

**First move:** {name the ONE skill to invoke first, and why it is upstream of the others.}

---

## Final Verdict

**{Sticky (ready to ship) | At risk (fix top 2 before shipping) | Not sticky (structural rework required)}**

{One-sentence rationale that matches the dimension scores above. Example: "Not sticky — Simple and Concrete both score 0/2 and those are structural; fixing downstream dimensions without a core would paper over the real gap."}

**Threshold rules used:**
- **Sticky** = no dimension scored 0; at most one scored 1; no anti-pattern hits.
- **At risk** = at most one dimension scored 0 AND no anti-pattern hits on burying-the-lead or common-sense sedation.
- **Not sticky** = two or more dimensions scored 0, OR Simple scored 0, OR a structural anti-pattern fired.
```

---

## Template usage notes

- The quoted-evidence column is mandatory. Scores without quotes are rejected by the Step 11 self-check.
- The kidney-heist comparison line is mandatory — it is the book's own calibration anchor and the audit's main anti-generic-advice defense.
- The "First move" line under Handoff Recommendations is the single most important handoff output — it answers the user's real question ("what do I do first?") and prevents the decision-paralysis anti-pattern inside the audit itself.
- Use the exact heading names in this template. Downstream skills (message-clinic-runner) parse these sections by header.
