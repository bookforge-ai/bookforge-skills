# Leitner Box Implementation

## Overview

The Leitner box is a physical or logical system invented by German science journalist Sebastian Leitner for managing spaced retrieval practice of flashcard-style material. Its core principle: the better your mastery of an item, the less frequently you need to practice it — but items you know well never leave the system until the learning goal is fully met.

The system solves two common problems:
1. Learners spend equal time on items they know well and items they struggle with — an inefficient allocation.
2. Learners stop practicing items that feel familiar, triggering the familiarity trap and slow undetected forgetting.

---

## Physical Setup: Four Tiers

### Materials

- 4 physical containers (boxes, folders, file drawer sections, or divided notebook sections)
- Label them Tier 1 through Tier 4
- One card or slip per item to be learned

### Tier Definitions and Review Frequency

| Tier | Mastery Level | Review Frequency |
|---|---|---|
| Tier 1 | Errors frequent; not yet reliable | Every practice session |
| Tier 2 | Mostly correct but not consistent | Every other session |
| Tier 3 | Reliably correct in same-topic blocks | Once per week |
| Tier 4 | Reliably correct in mixed sessions | Once per month |

All new items start in Tier 1.

---

## Movement Rules

### Advancing (Tier 1 → 2 → 3 → 4)

Move an item forward one tier when:
- You answer it correctly in an **interleaved session** (mixed with other topics)
- You do so in two or more consecutive sessions without error

Do not advance based on blocked performance (answering correctly when all cards in the session are from the same topic). Correct recall in massed conditions may reflect short-term memory from recent exposure, not durable learning.

### Demoting (Any tier → Tier 1)

Move an item back to Tier 1 when:
- You answer it incorrectly in any session, regardless of its current tier

This rule is strict for a reason: errors in a system you have been practicing indicate that durable learning has not been achieved for that item. The item needs more frequent retrieval.

---

## Session Structure

### Session Composition

Each session contains:

1. **All Tier 1 items** (reviewed every session)
2. **Tier 2 items** (every other session — check the schedule)
3. **Tier 3 items** (if it is the weekly review day)
4. **Tier 4 items** (if it is the monthly review date)

Shuffle all items from all tiers scheduled for today into a single deck before beginning. Do not separate them into tier-by-tier blocks — the mixing is what makes the session interleaved and what validates advancement decisions.

### Minimum Session Requirements

- Never skip a session that contains Tier 1 items. These are the items most at risk of being forgotten.
- If time is short, prioritize Tier 1 and defer Tier 4 monthly review. The opposite is the familiarity trap in action.

---

## Troubleshooting Stalled Items

### Symptom: An item stays in Tier 1 for more than 3–4 sessions without advancing

This indicates the item is not being learned by repetition alone. Possible causes and remedies:

**Cause 1 — The item requires context, not just recall**
Symptoms: You can recall the item when you see the card, but you cannot generate it from memory in a real situation.
Remedy: Add context to the card. Instead of "Q: What is the capital of Texas? A: Austin" — try "Q: If you are driving from San Antonio to Dallas and stop at the state capital, where do you stop? A: Austin." Force the retrieval to mirror the context where you need the knowledge.

**Cause 2 — The item is being confused with a similar item**
Symptoms: You confuse this item with one or two other items consistently.
Remedy: Create a comparison card that explicitly contrasts the two confusable items. Practice them in consecutive slots (not blocks — just consecutively to highlight the difference), then return to interleaved practice.

**Cause 3 — The item lacks a hook**
Symptoms: The item feels arbitrary; there is no connection to anything you already know.
Remedy: Generate an elaboration — a story, analogy, image, or connection to prior knowledge. Write the hook on the back of the card. The hook does not need to be logical; it needs to be memorable. Even a silly or exaggerated image aids encoding.

**Cause 4 — The item is too big**
Symptoms: The item requires recalling a multi-step process or a long list.
Remedy: Break it into smaller cards. Each card should require a single, specific retrieval act. Multi-step cards often mask partial mastery as failure.

---

## Adapting to Digital Tools

Spaced-repetition software (Anki, RemNote, SuperMemo, etc.) implements equivalent logic with algorithmic precision:

- Individual intervals per item (not tier-based)
- Performance data adjusts intervals automatically
- Retention rate tracking over time

**When to use digital vs. physical:**

| Situation | Recommendation |
|---|---|
| Large material set (> 200 items) | Digital — manual tracking becomes impractical |
| Small material set (< 50 items) | Physical — simpler, no setup overhead, easier to inspect |
| Material requiring images, diagrams | Digital — better display support |
| Study group or shared curriculum | Physical — easier to share and modify collectively |
| Long-term retention (years) | Digital — algorithmic intervals adapt better over very long time horizons |

### Anki Configuration for Leitner-Style Behavior

Default Anki settings are close to Leitner logic. Adjust:
- **New cards per day:** Set low (10–20) to avoid overwhelming Tier 1 with simultaneous new items
- **Review order:** Set to "Random order" within due items — not "Due date" which can cluster items from the same topic
- **Interval modifier:** Default is 100%; increase to 120–130% only if you are reliably hitting 90%+ correct, to extend intervals further

Anki's "Ease" factor automatically reduces intervals for difficult items and extends them for easy items — equivalent to the Leitner tier system but at item-level granularity.

---

## The Familiarity Trap in Leitner Systems

The Leitner box's biggest failure mode is the learner stopping review of Tier 3 and Tier 4 items because they "feel like they know them." This is the familiarity trap: recognition does not equal recall under pressure.

Rules to prevent this:
1. Monthly Tier 4 review is non-negotiable. Schedule it on the calendar, not "when I feel like it."
2. If you skip a Tier 4 review for two or more months, demote those items to Tier 3 automatically.
3. Before any high-stakes performance (exam, presentation, job interview), pull all items from Tier 3 and Tier 4 and quiz yourself under timed, interleaved conditions. The goal is to confirm mastery, not to review — if mastery is there, the session will be short.
