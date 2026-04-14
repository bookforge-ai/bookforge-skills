# Abstraction Ladder Examples

Worked before/after pairs for Pass B (Abstraction / Strategy-Level Talk). Each example shows a sentence that sounds clear to an expert but fails the Boeing-727 test, then a concrete rewrite.

## The ladder, briefly

| Level | What lives here | Readability | Coordinates action? |
|-------|-----------------|-------------|--------------------|
| 5. Values | "excellence", "integrity" | feels profound | no |
| 4. Strategy | "maximize shareholder value" | feels important | no |
| 3. Principle | "put the customer first" | feels true | weakly |
| 2. Behavior | "answer every support ticket within 4 hours" | boring | yes |
| 1. Object | "Tracy the flight attendant served complimentary champagne" | vivid | yes |

Made to Stick's central claim: experts drift upward (because they have already internalized the concrete layer). Non-experts can only anchor to levels 1 and 2. Every Pass B flag is a sentence stuck at levels 3–5 that needs a drop to level 1 or 2.

## Example 1 — The canonical contrast (from the book's Introduction)

**Before (level 4):** "Our mission is to maximize shareholder value through synergistic growth and operational excellence."

**After (level 2):** "Ship three new products this year. Double revenue in our European accounts. Cut support-ticket resolution time from 48 hours to 8."

**Why:** The "before" is readable, but after reading it, no employee knows what to do on Monday morning. The "after" specifies observable outcomes. The Heaths contrast this directly with JFK's moon-mission sentence — "put a man on the moon and return him safely to Earth by the end of the decade" — which is a level-1 constraint (man, moon, safely, decade) that coordinated a decade of action without further translation.

## Example 2 — The Boeing 727 test (from Chapter 3 Concrete)

**Before (level 4):** "Design the best single-aisle passenger jet in the world."

**After (level 1):** "Design a plane that seats 131 passengers, flies nonstop from Miami to New York City, and lands on Runway 4-22 at LaGuardia — which is less than a mile long."

**Why:** The "best" phrasing cannot coordinate thousands of engineers across wings, engines, landing gear, and cabin. The "level-1" version constrains every subsystem simultaneously. Wings must produce enough lift at that weight. Landing gear must handle that runway. Engines must reach cruise for that distance. A concrete constraint is a coordination device; an adjective is not.

## Example 3 — Commander's Intent (from Chapter 1 Simple)

**Before (level 3 principle):** "Execute the operational plan with agility and adapt to changing conditions."

**After (level 1 behavior + end state):** "Clear Hill 4305 of enemy remnants so 3rd Brigade can pass through."

**Why:** When the plan doesn't survive contact, the principle ("adapt") gives no guidance. The Commander's Intent sentence — one end state, one named object — lets a subordinate abandon the written plan and still win. If you can't write the one-sentence intent, you don't have a core.

## Example 4 — Southwest Airlines (from Chapter 1 Simple)

**Before (level 4):** "We want to be the best airline experience for value-conscious travelers through operational efficiency."

**After (level 3, but with a delegation test):** "We are THE low-fare airline."

Delegation test: Tracy from marketing wants to add a light chicken Caesar salad on the Houston-Las Vegas flight. Herb Kelleher's answer: "Tracy, is adding the Caesar salad going to make us THE low-fare airline? Because if it isn't, we're not serving it."

**Why this example is subtle:** "THE low-fare airline" sits at level 3, not level 1 — it's still a principle. What makes it work is the exclusion clause ("and nothing else"). A new hire at Southwest can make a contested trade-off from the core alone. "Maximize shareholder value" cannot pass this test. When auditing for Pass B, ask: **can a new hire resolve a contested decision from this sentence alone?** If yes, the sentence passes. If not, it is stranded above the coordination line.

## Example 5 — Nonprofit fundraising (maps to Rokia effect, Chapter 5 Emotional)

**Before (level 5 values):** "We are committed to improving outcomes for vulnerable populations in under-resourced regions."

**After (level 1 object + person):** "We bought mosquito nets for Amina, age 4, and her three siblings in Lilongwe. Last year they had malaria twice. This year: zero."

**Why:** "Vulnerable populations" cannot activate the identifiable-victim effect the Heaths document in the Save the Children Rokia study (donors gave $2.50 to the named child and $1.14 to the statistic). Every abstract population noun in a fundraising letter is a Pass B flag.

## Example 6 — Technical documentation, audience = ops engineers

**Before (level 3):** "The service uses eventual consistency semantics for cross-region replication."

**After (level 2):** "When you write a value in the US region, it appears in the Europe region within 2-5 seconds. During that window, a read from Europe may return the old value. A read from the US returns the new value immediately."

**Why:** "Eventual consistency semantics" is accurate and to an expert it feels precise. To a reader debugging a bug at 2am, it gives no operational prediction. The level-2 rewrite tells the reader what will happen in observable time.

## How to generate the concrete translation

When a Pass B flag fires, apply this template to produce the rewrite:

1. **Who is the actor?** (Not "the team" or "we" — a named role or person.)
2. **What observable verb?** (Not `leverage`, `enable`, `drive` — a verb the actor physically performs.)
3. **What object?** (A physical or digital thing the reader could point at.)
4. **Under what constraint?** (A number, a deadline, a named reference case.)

If any of these four cannot be filled in for the abstract sentence, you have confirmation that the abstract sentence is not actionable — not because you are being pedantic, but because the author has not yet decided what the sentence means in practice. This is a signal to the user: the Curse is covering a decision that has not been made.

## Edge case: when abstraction is intentional

Not every abstract sentence is a Curse-of-Knowledge hit. Values statements, brand voice lines, and aspirational mission text are sometimes supposed to live at levels 4-5. Before flagging, ask: **does the draft have ANY level-1 or level-2 anchor?** If there is at least one vivid concrete scene somewhere in the draft, the abstract sentences around it can stand. If EVERY sentence is at level 3+, the whole draft is Curse-of-Knowledge territory and needs a concretization pass, not a polish pass.
