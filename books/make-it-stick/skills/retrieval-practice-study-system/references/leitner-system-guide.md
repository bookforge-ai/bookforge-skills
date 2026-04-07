# Leitner Box System: Implementation Guide

## What It Is
The Leitner box is a physical implementation of spaced repetition invented by German science journalist Sebastian Leitner. It organizes flashcards into boxes with escalating review intervals, so difficult material gets more practice and easy material is not wasted on.

## Physical Setup (Index Cards)
Use 5 dividers or physical boxes labeled 1-5. Write one question on the front of each card, the answer on the back.

## Review Intervals (Default)
| Box | Review Frequency | Cards Start Here |
|-----|-----------------|-----------------|
| 1 | Every study session | All new cards |
| 2 | Every other session | Promoted from Box 1 |
| 3 | Once per week | Promoted from Box 2 |
| 4 | Once per month | Promoted from Box 3 |
| 5 | Once per semester | Promoted from Box 4 |

## The Golden Rule
**Any card answered incorrectly at any box level returns immediately to Box 1.**
This is not punitive — it is the mechanism that prevents the fluency illusion.

## Promotion Rule
- Answered correctly once → promote to next box
- Answered incorrectly → return to Box 1 regardless of current box

## Digital Equivalents
- **Anki** (free, cross-platform): implements the SM-2 algorithm, which is mathematically equivalent to Leitner with adaptive intervals
- **Quizlet** (freemium): supports basic spaced repetition
- **Remnote** (freemium): combines notes and flashcards with spaced repetition
- **Physical cards** remain effective and have the advantage of requiring the learner to produce cards manually, which is itself a form of retrieval practice

## Adapting for Short Timelines
- Compress to 3 boxes: Active (daily), Practice (every other day), Mastered (weekly)
- Do not retire cards to Box 5 until after the exam or deadline
- Treat any Box 3 card as "nearly mastered" and revisit weekly

## Common Mistakes
- **Stopping at Box 2 and feeling done:** Mastery requires reaching Box 4+ with at least one correct review cycle
- **Not returning missed cards to Box 1:** Allowing incorrect cards to stay in higher boxes creates a false sense of progress
- **Never reviewing Box 5:** Mastered material still requires periodic retrieval; quarterly review of Box 5 prevents long-term forgetting
