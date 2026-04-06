# Usability Test Protocol

This document provides the complete four-phase protocol for running usability tests as part of product discovery. In the value testing context, usability testing is always a prerequisite to qualitative value testing — users must understand how to operate the product before their value reactions are meaningful.

## Why Usability Testing in Discovery

Traditional usability testing happened at the end of development, after the product was built. By then, correcting serious issues required significant waste or produced a permanently flawed product.

Modern discovery practice runs usability testing on prototypes — before anything is built — so that issues are corrected at near-zero cost. The main difference is the timing: discovery usability testing uses prototypes, not products.

## Phase 1 — Recruit

You need at minimum 5 test subjects. Research consistently shows that 5 users reveal the majority of serious usability issues.

**Recruitment channels (in order of preference):**

1. **Customer discovery program members** — Pre-qualified, already opted in, best for business products. Use this if you have one.
2. **Email list selection** — If you have a user email list, work with your product marketing manager to select a screened subset matching your target customer profile.
3. **Company website volunteer form** — Solicit test subject volunteers. Screen all volunteers with a phone call to confirm they are in your target market.
4. **Craigslist or search engine marketing campaign** — Especially effective for reaching users who are actively in the moment of experiencing the problem your product solves (for example, a Google AdWords campaign targeting people searching for your problem category).
5. **Intercept at locations where target users congregate** — Trade shows for business software, shopping centers for e-commerce, sports bars for fantasy sports. Bring thank-you gifts.

**Compensation:** If asking users to come to your location, compensate them for their time. A common approach is to meet at a mutually convenient location — a coffee shop works well. This is so common it is called Starbucks testing.

**Screening requirement:** Always screen volunteers by phone before the session. Confirm they match your target customer profile. Volume is less important than quality — five well-matched users are more valuable than fifteen mismatched ones.

## Phase 2 — Prepare

**Prototype:** Use a high-fidelity user prototype for both usability testing and value testing. You can get useful usability feedback from lower-fidelity prototypes, but the value testing that follows requires realism. Build to the fidelity level that the downstream value test demands.

**Attendees:** Product manager, product designer, and at minimum one engineer (rotating among team members). All three must be present. The product manager and designer must attend every session without exception. Engineer attendance is strongly encouraged — the direct exposure to customer behavior produces learning that written summaries cannot replicate.

**Role division:**
- One person administers the test (interacts with the user)
- One person takes notes
- After the session, both debrief to confirm they observed the same things and reached the same conclusions

**Task definition:** Define in advance the specific tasks you want to test. Focus on the primary tasks — the ones users will do most of the time. There may also be less-frequent but important tasks; include those if they are risky. Do not try to test everything in one session.

**Example task list for a report generation feature:**
- Generate a report for last quarter's sales
- Change the date range on a report
- Share a report with a colleague
- Export a report to a spreadsheet

**Venue:**
- Coffee shop table — informal, user feels less like a lab rat, works well for most situations
- Customer's office — excellent for business products; environmental cues (monitor size, desk setup, coworker interruptions) reveal additional context
- Formal testing lab with two-way mirror — useful when available, but not required
- Remote tools — acceptable supplement for usability testing, but less suitable for the value testing that follows (value testing benefits from in-person presence)

## Phase 3 — Test

### Opening the Session

Before presenting any tasks:

1. **Set expectations:** Tell the user this is a prototype, it is a very early product idea, and it is not real. Explain that you are testing the ideas in the prototype, not testing them. They cannot pass or fail — only the prototype can. You want candid feedback, good or bad.

2. **Landing page cold read:** Before jumping into tasks, ask the user to look at the landing page or home screen of your prototype and tell you what they think it does and what might be valuable or appealing to them. Do this before they start interacting with tasks — once they are in task mode, you lose the first-time visitor perspective. Landing pages are critical for bridging the gap between user expectations and what the product actually does.

### During the Test

**Keep users in use mode, not critique mode.**

The goal is to observe what users can and cannot do. It does not matter whether the user thinks something is ugly or that a button is in the wrong place. What matters is whether they can complete the tasks they need to do.

Avoid asking questions like "What three things would you change about this page?" Unless the user is a product designer, their answer to that question is not useful. Watch what they do more than what they say.

**Stay quiet.**

The hardest skill in usability testing is silence. When a user struggles, the natural instinct is to help. Suppress that instinct. Get comfortable with silence — it is your most important tool. Struggle reveals friction; helping the user removes the signal.

**The three outcomes for each task:**
1. User completed the task with no problem and no help — good
2. User struggled but eventually completed the task — friction detected
3. User gave up — failure; note whether they truly abandoned or were about to leave the product entirely

**The parrot technique:**

When you feel compelled to say something (either because the silence is uncomfortable or because you want to prompt the user), parroting is the tool:

- If the user is scrolling and looking confused, say: "I see you're looking at the list on the right." This prompts them to tell you what they are trying to find without leading them toward an answer.
- If the user asks "Will clicking this create a new entry?", respond: "You're wondering if clicking this will create a new entry?" The user will typically answer their own question. This avoids leading the witness.
- Use parroting instead of value judgments. Instead of "Great!" when the user completes a task, say "You created a new entry." This avoids leading value judgments while still acknowledging their action.
- Parroting gives the note-taker more time to write down observations.

**Avoid leading the witness:**

Do not give hints. Do not redirect attention. If you see the user scrolling past the right answer, do not help. What you are observing is exactly the information you need — that the affordance is not discoverable.

**Reading non-verbal signals:**

Users communicate through body language and tone. Genuine enthusiasm is visible — they lean forward, ask follow-up questions, and often ask when the product will be available. Lack of genuine enthusiasm is also visible even when users say polite things. Watch for the gap between what users say and what their body language and engagement level communicate.

## Phase 4 — Summarize

**Immediately fix issues you identify.**

There is no rule that says you must keep the test identical across all subjects. Qualitative usability testing is about rapid learning, not proving anything statistically. As soon as you identify an issue, fix it in the prototype before the next session. This is the power of discovery usability testing — fast iteration at low cost.

**The email summary:**

After each test session (or after each set of sessions if running multiple in a day), the product manager or designer writes a short email summary of key learnings and sends it to the product team. Keep it brief — one page or less. Long reports that take hours to write and days to read are obsolete by the time they are delivered. The prototype will have moved past what was tested.

The email summary should include:
- What tasks users completed successfully
- Where users struggled or failed
- What surprised you
- What changes are being made to the prototype before the next session

**What you are looking for:**

The goal is to identify places in the prototype where the model the software presents is inconsistent or incompatible with how the user is thinking about the problem. When you find this mismatch, the fix is often straightforward — nomenclature, flow, or visual hierarchy — and fixing it can be a significant win.

## Common Mistakes

| Mistake | Why It Fails | Correction |
|---------|-------------|------------|
| Running usability test at the end of development | Issues found too late to fix without significant waste | Run on prototypes during discovery |
| Product manager or designer not attending | Secondhand summaries miss critical nuance; learning must be firsthand | Attend every session — non-negotiable |
| Asking for design opinions ("What would you change?") | Users cannot specify what to build; their opinions predict their own behavior poorly | Watch what they do, not what they say |
| Helping users when they struggle | Removes the friction signal | Stay silent; use the parrot technique |
| Writing long formal reports | Reports are obsolete before they are read | Write brief email summaries immediately after each session |
| Testing too few users | Missing major issues | Target minimum 5 users per round of testing |
| Using internal employees as test subjects | Employees know the product, think like the team, and are not target customers | Always use actual target customers |
