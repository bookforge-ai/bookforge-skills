# Spacing Interval Guide

## Core Principles

### The Forgetting Curve and Optimal Spacing

The goal of spacing is not to avoid forgetting — it is to engineer a controlled amount of forgetting that forces effortful retrieval. The retrieval effort re-triggers memory consolidation, making the trace stronger than it was before. This is why "a little forgetting between practice sessions can be a good thing."

The two failure modes:
- **Too little spacing:** Session B occurs before any meaningful forgetting from Session A. Retrieval requires no effort because short-term memory is still active. The session feels highly productive. Little new consolidation occurs.
- **Too much spacing:** So much has been forgotten that retrieving the material is essentially relearning it. Retrieval fails outright. The session requires looking up answers rather than recalling them, reducing the retrieval benefit.

The optimal zone is: "Effort required, but recall is possible."

### Sleep as a Consolidation Amplifier

Memory consolidation is strongly linked to sleep. At minimum, a single sleep period between practice sessions produces meaningfully better long-term retention than two sessions on the same day. Even in compressed schedules, "Monday morning and Monday evening" is inferior to "Monday and Tuesday" when long-term retention matters.

For material that requires deep integration (complex problem-solving, judgment skills, creative skills), multiple sleep periods before re-testing is even better than a single night.

---

## Interval Tables by Material Type

### Names, Faces, and Arbitrary Associations

These associations have a steep forgetting curve — most loss occurs within the first 24 hours.

| Session | Interval After Previous |
|---|---|
| Initial exposure | — |
| First review | Within 10–30 minutes of initial exposure |
| Second review | Same day (4–8 hours later) |
| Third review | Next day |
| Fourth review | 3 days later |
| Fifth review | 1 week later |
| Ongoing maintenance | Monthly |

**Note:** If performance in any review session falls below 60% correct, reset the interval to the previous level.

---

### New Concepts from Text or Lecture

Standard material encountered in academic or professional reading.

| Session | Interval After Previous |
|---|---|
| Initial reading or lecture | — |
| First retrieval (self-quiz without notes) | Same day or within 24 hours |
| Second retrieval | 3–5 days later |
| Third retrieval | 1–2 weeks later |
| Ongoing maintenance | Monthly |

**Key:** The first retrieval should occur without reviewing the source material first. Attempt to recall, then check. The failed retrieval attempts are not wasted — they prepare the mind to encode the corrected information more deeply.

---

### Problem-Solving Skills (Math, Logic, Diagnosis)

Material where the goal is not to recognize a fact but to apply a procedure or select the correct approach.

| Session | Interval After Previous |
|---|---|
| Introduction to problem type | — |
| First solo practice (interleaved with other types) | 1–2 days |
| Second practice (interleaved) | 1 week |
| Third practice (interleaved) | 2–3 weeks |
| Ongoing maintenance | Monthly |

**Note:** Interleaving is especially important here. Do not wait until mastery of one type is complete before introducing others. The point is to build discrimination ability, which requires encountering multiple types together.

---

### Complex Judgment and Transfer Skills

Clinical diagnosis, athletic performance, negotiation, language production, leadership decisions.

| Session | Interval After Previous |
|---|---|
| Initial exposure and structured practice | — |
| First varied practice (changed conditions) | Next session (1–2 days) |
| Second varied practice | 1 week |
| Third varied practice | 3 weeks |
| Real-world application and reflection | As soon as available |
| Ongoing maintenance | Monthly; plus reflection after each real-world encounter |

**Note:** Real-world encounters count as retrieval practice sessions when followed by reflection. A doctor who sees a patient and then reviews the encounter systematically is performing spaced retrieval practice.

---

## Adapting Intervals for Time Constraints

### Compressed Schedule (Exam in < 1 Week)

When the timeline is short, spacing intervals must be compressed. The principle remains the same — some gap between sessions is better than none.

- Minimum gap: One sleep period between sessions covering the same material.
- Use every available gap strategically: morning session + evening session = one sleep period, which is better than two morning sessions back-to-back.
- Prioritize retrieval (self-testing without notes) over re-reading. In compressed timelines, re-reading returns near zero value; retrieval practice returns the highest value per minute.
- If the exam is tomorrow: do a retrieval session tonight (testing yourself without looking), sleep, and do a brief review in the morning. Do not cram through the night — sleep deprivation impairs the consolidation that occurred during the prior week.

### Extended Schedule (3+ Months)

- Start with short intervals and lengthen them as mastery increases.
- Use the Leitner-box principle: items that are reliably retrieved correctly in interleaved conditions get moved to longer intervals (weekly → bi-weekly → monthly).
- Revisit all material at least monthly regardless of apparent mastery. The familiarity trap is most dangerous for well-learned material: it feels unnecessary to review, so review stops, and slow forgetting goes undetected until a performance moment reveals the gap.

### When You Miss Sessions

Missing sessions is unavoidable. The correct response is not to double up (which produces a massed session) but to resume the schedule and accept that some additional forgetting occurred. The forgetting is not catastrophic; it means the next retrieval session will require slightly more effort, which will strengthen the memory trace.

Do not extend the overall schedule proportionally for every missed session — this creates a never-ending plan. Instead, identify the highest-priority material (lowest mastery, most important for performance), concentrate additional retrieval on that, and allow lower-priority material to be reviewed at its scheduled interval even if some sessions were missed.

---

## Leitner Box Implementation

The Leitner box is a mastery-tracking system for flashcard-style material that automatically calibrates review frequency to current mastery level.

### Physical Setup

Use four labeled containers (boxes, folders, or sections of a binder):

- **Box 1:** Review every session (errors frequent)
- **Box 2:** Review every other session (mostly correct)
- **Box 3:** Review once per week (reliably correct in blocked conditions)
- **Box 4:** Review once per month (reliably correct in interleaved conditions)

All new material starts in Box 1.

### Movement Rules

- **Correct answer in interleaved conditions:** Move the item forward one box (toward less-frequent review)
- **Incorrect answer:** Move the item back to Box 1 (most frequent review)
- **Correct answer in blocked conditions (consecutive same-topic):** Do not advance — this may reflect short-term memory, not durable learning. Advance only when correct in a mixed session.

### Why Interleaved Conditions for Advancement

The test for "mastered" must match real performance conditions. If a vocabulary card is answered correctly when all the cards in the session are Spanish vocabulary, that is a weaker signal than answering it correctly when it appears among cards from three different subjects. Only advance when the retrieval is performed in mixed conditions.

### Digital Implementation

Any spaced-repetition software (Anki, RemNote, etc.) implements equivalent logic algorithmically, using performance data to schedule each item's next review. The key difference from a paper Leitner box: digital systems track intervals precisely and account for individual item difficulty separately. Paper boxes use approximate tier-based intervals.

Both work. The paper system is easier to understand and control; the digital system scales better for large material sets.
