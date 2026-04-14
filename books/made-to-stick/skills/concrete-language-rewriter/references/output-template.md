# Concrete Rewrite — Output Template

Use this structure for `concrete-rewrite.md` deliverables.

```markdown
# Concrete Rewrite

**Audience:** {role, domain familiarity, what they see/do daily}
**Source draft:** {file path or "pasted in chat"}
**Date:** {YYYY-MM-DD}

---

## Summary

{N} passages flagged. Techniques used: {schema tap: X, high-concept pitch: Y, generative analogy: Z, behavior-level swap: W}.

## Side-by-side table (REQUIRED)

Every rewrite must appear in this four-column table. The `Canonical Exemplar` column is non-optional — it names the *Made to Stick* pattern the rewrite echoes, so the user builds the catalog mentally as they use the skill.

| Original | Rewrite | Technique | Canonical Exemplar |
|---|---|---|---|
| {verbatim original} | {rewrite} | {schema tap / high-concept pitch / generative analogy / behavior-level swap} | like {pomelo example / Disney cast members / Die Hard on a bus / Boeing 727 runway constraint / Jane Elliott blue-eyes exercise / Kris & Sandy / Aesop's Fox & the Grapes} |

Canonical exemplar map:
- **Schema tap** — like the **pomelo** example ("grapefruit crossed with a football"); or **Aesop's Fox & the Grapes** (parable as packed schema)
- **High-concept pitch** — like **"Die Hard on a bus"** (the *Speed* pitch); other X-meets-Y Hollywood pitches
- **Generative analogy** — like **Disney "cast members"** (theme park as stage production); or **Kris & Sandy** (accounting reframed as investigative journalism)
- **Behavior-level swap** — like **Boeing's 727 runway constraint** ("seat 131 passengers, fly Miami-NYC, land on La Guardia Runway 4-22"); or **Jane Elliott's blue-eyes / brown-eyes exercise** (felt experience replaces lecture)

---

## Passage 1 — {short label}

**Technique:** {schema tap | high-concept pitch | generative analogy | behavior-level swap}
**Canonical exemplar:** like {pomelo example | Disney cast members | Die Hard on a bus | Boeing 727 runway constraint | Jane Elliott blue-eyes exercise | Kris & Sandy | Aesop's Fox & the Grapes}

**Before:**
> {verbatim original text}

**After:**
> {rewrite}

**Why this works:**
{One line — which hook(s) in the audience's existing memory the rewrite taps, how it echoes the canonical exemplar's pattern, and what the original was missing.}

**Generated vocabulary (generative analogy only):**
- {old term} -> {new term}
- {old term} -> {new term}

**Caveats:**
- {Any `[assumption — verify]` flags, e.g., "rewrite implies a performance claim the source did not state — confirm before shipping"}
- {Or: "none — rewrite uses only audience-known schemas"}

---

## Passage 2 — {short label}

...

---

## Notes for the user

- Reject any rewrite whose `[assumption — verify]` flag cannot be substantiated.
- For cultural-values rewrites, the generative analogy is only useful if at least 3 daily objects or actions can be renamed without forcing it — if fewer, downgrade to schema tap.
- For one-shot pitches (tagline, cold open), prefer high-concept pitch; verify both reference points are genuinely known to the audience, not just to you.
```
