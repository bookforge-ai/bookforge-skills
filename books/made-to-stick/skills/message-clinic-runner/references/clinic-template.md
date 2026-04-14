# Message Clinic Output Template

This is the fixed template the `message-clinic-runner` skill fills in when producing `message-clinic-output.md`. The structure mirrors the Heath brothers' Idea Clinics from Made to Stick (Chapters 1-6): SITUATION → MESSAGE 1 → DIAGNOSIS → MESSAGE 2 → PUNCH LINE, with a Rationale audit trail and a Constraints-preserved line appended.

Do not reorder sections. Do not drop sections. If a section is inapplicable (e.g., MESSAGE 2 in the already-sticky branch), keep the heading and use the explicit marker "(unchanged — already sticky)".

---

```markdown
# Message Clinic — {draft name or short descriptor}

## THE SITUATION

{2-3 sentences. Name: (a) who is communicating, (b) to whom, (c) the channel, (d) why it matters. Match the compact voice of the book's Clinics — e.g., "Health educators at Ohio State University want to inform the academic community about the risks of sun exposure."}

## MESSAGE 1

> {The user's original draft, verbatim. No typo fixes. No silent polishing. Wrap in blockquote or code fence for visual symmetry with MESSAGE 2.}

## DIAGNOSIS

Audit produced by `stickiness-audit`. 0/1/2 per dimension. No summed score — the book is explicit: it's a checklist, not an equation.

| Dimension            | Score | Verdict (one line)          | Evidence (quoted)        |
|----------------------|-------|-----------------------------|--------------------------|
| Simple               | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |
| Unexpected           | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |
| Concrete             | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |
| Credible             | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |
| Emotional            | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |
| Stories              | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |
| Curse of Knowledge   | 0/1/2 | {one-line verdict}          | "{quoted passage}"       |

**Top 3 rewrite targets** (ranked by severity × fraction of draft poisoned):
1. **{Dimension}** — "{quoted passage from MESSAGE 1}" — Fix: {specific move}. Effort: S/M/L.
2. **{Dimension}** — "{quoted passage}" — Fix: {specific move}. Effort: S/M/L.
3. **{Dimension}** — "{quoted passage}" — Fix: {specific move}. Effort: S/M/L.

## MESSAGE 2

> {The revised draft, in the same medium and voice as MESSAGE 1. Within ±20% of original length unless explicitly requested otherwise. Any unsourced claim replaced with [NEEDS FROM USER: <what>]. If MESSAGE 1 was already sticky, this section reads exactly: "(unchanged — already sticky)".}

## PUNCH LINE

{One sentence (two max). Names at least one SUCCESs dimension explicitly. Explains the central change and why the revision works in terms the user can quote back. Modeled on the book's Clinic punch lines — compact, principle-named, and tied back to the framework.}

## Rationale

Audit trail mapping each change in MESSAGE 2 to the SUCCESs dimension it fixes and the foundation skill that produced the fragment.

- **{Dimension}** — {what changed in one phrase} — produced by `{foundation-skill-name}`
- **{Dimension}** — {what changed} — produced by `{foundation-skill-name}`
- **{Dimension}** — {what changed} — produced by `{foundation-skill-name}`

{If the already-sticky branch fired, this section contains one bullet: "No changes made. Audit verdict retained for the author's records."}

## Constraints preserved

{One line naming which tone, brand, legal, length, or channel constraints the rewrite respected. Example: "Plainspoken voice, no corporate buzzwords, under 150 words, UK fundraising regulator compliance — no graphic imagery."}

{If placeholders exist in MESSAGE 2, add a second line: "Placeholders to fill before shipping: [NEEDS FROM USER: ...], [NEEDS FROM USER: ...]."}
```

---

## Filling notes

- **DIAGNOSIS** is a condensed version of `stickiness-scorecard.md`, not a full copy. The full scorecard can be referenced in the user's working directory; this table is the at-a-glance version.
- **MESSAGE 2** uses the same visual container (code fence or blockquote) as MESSAGE 1 so the user can see the before/after side by side without squinting.
- **PUNCH LINE** is the single highest-value sentence in the entire output. If you can only save one section, save this one — it is the teaching moment.
- **Rationale** bullets are what distinguishes a clinic from a rewrite. Without them the user sees a change but does not learn the principle.
- **Constraints preserved** is the voice-integrity receipt. It lets the user verify you respected their brand before they read the rewrite.

## Branch: already-sticky output

When Step 3's audit returns **Sticky** (no 0s, at most one 1, no structural anti-pattern), the output still uses this template, but:

- DIAGNOSIS table is filled in with the actual scores (most will be 2/2) and quoted evidence from MESSAGE 1.
- **Top 3 rewrite targets** section is replaced with: "**No rework needed.** Draft passes the audit. Below: the two or three dimensions the draft is already winning on."
- MESSAGE 2 reads exactly: `> (unchanged — already sticky)`
- PUNCH LINE explains WHICH dimensions the draft is already winning on, with quoted phrases from MESSAGE 1.
- Rationale contains one bullet: "No changes made. Audit verdict retained for the author's records."
- Constraints preserved line still fires — "already compliant with {constraint}."

This branch is a legitimate output, not a failure mode. The book is explicit: some ideas only need to lose a few pounds; some don't need to lose any.
