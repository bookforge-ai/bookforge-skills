# Qualitative Value Test Protocol

Qualitative value testing is, in Cagan's view, probably the single most important discovery activity for a product team. The goal is rapid learning and big insights — understanding whether customers see real value in your solution, and why or why not.

Quantitative testing tells you what is happening. Qualitative testing tells you why. Both are necessary. Qualitative testing comes first.

**Cadence target:** At minimum two to three qualitative value test sessions per week during active discovery.

**Who must attend:** Product manager, product designer, and at minimum one rotating engineer. The product manager must be present at every session without exception. Do not delegate this. Do not hire a firm to do this for you. The firsthand exposure to user reactions is a core competency of the product manager role.

## The Problem: Politeness Bias

The central challenge in qualitative value testing is that people are generally nice. When sitting face to face with someone who has built something, most people are not willing to tell you what they really think. They give polite, encouraging feedback that does not reflect their actual likelihood to use or pay for the product.

All value tests in this protocol are designed to cut through politeness bias by asking users to make a commitment — not just state an opinion. Commitments (money, time, access, reputation) reveal genuine value perception far more accurately than stated enthusiasm.

## Session Structure

Run each session in four sequential parts. Do not reorder them.

### Part 1: Interview First (5–10 minutes)

Open every session with a short customer interview before showing the prototype.

**Goal:** Confirm that this user actually has the problem you are solving, understand how they currently solve it, and learn what it would take for them to switch.

**Questions to ask:**
- "Tell me about how you currently [handle the problem area]."
- "What's the most frustrating part of that process?"
- "What tools or approaches have you tried?"
- "What would make you consider switching to something new?"

**Why this comes first:** If the user does not actually have the problem, their response to your solution is not useful data. You need to know whether you are talking to a genuine potential customer before interpreting anything they say about the product. This also creates context — after discussing their current approach, users evaluate your solution relative to their actual situation rather than abstractly.

**If the user does not have the problem:** Note this, thank them for their time, and consider whether your recruitment screening criteria need adjustment. Do not proceed with the value test — the data would be invalid.

### Part 2: Usability Test (15–25 minutes)

Before testing value, the user must understand how to use the product. Run a full usability test on the prototype.

**Why usability testing precedes value testing:**

If you attempt value testing without usability testing first, the session becomes a focus group. The user comments hypothetically on something they have never operated — imagining how it might work, asking clarifying questions, making up scenarios. Focus groups provide market insight but do not predict whether your product will work. You need users to have actually operated the product to have a meaningful conversation about value.

After a usability test, the user knows what the product is, how it works, and what it is meant to do. Only then can you have a credible conversation about whether they see value in it.

Follow the usability test protocol in `usability-test-protocol.md`. Use a high-fidelity prototype — value testing requires realism. A live-data prototype or hybrid prototype also works.

**Transition:** After the usability test, the user is in a position to have an informed conversation about the product. Move immediately to specific value tests.

### Part 3: Specific Value Tests (10–15 minutes)

Apply one or more of the four specific value tests. Choose based on what fits the context (consumer vs. business, product type, relationship).

**Value Test 1 — Money**

Ask the user if they would be willing to pay for the product right now.

For consumer products or lower-cost software: "Would you be willing to put in your credit card right now? We don't actually need it, but I'm curious if this is something you'd pay for."

For expensive business products (beyond what an individual would put on a credit card): "Would you be willing to sign a non-binding letter of intent to purchase this if we build it?"

**What the signal means:** You are not collecting the credit card or the letter. You are observing whether the user is willing to make a financial commitment. Willingness to do so — even when told it's not required — reveals genuine perceived value. Refusal or hesitation, even after expressed enthusiasm, reveals politeness bias at work.

**Value Test 2 — Time**

Especially effective for business products:

"Would you be willing to schedule significant time with us — say, a few hours per week over the next month — to work on this with us? We don't necessarily need it, but I'm curious if this is important enough for you to invest that kind of time."

**What the signal means:** Time is the scarcest resource in business. A user's willingness to commit time — even hypothetically — is a strong indicator of how much they value the solution. Businesses that actually have the problem will recognize the value of solving it and will be willing to invest.

**Value Test 3 — Access**

"Would you be willing to give us the login credentials for the product you're currently using for this? We have a migration utility that would help import your data. We don't really need it now, but I'm curious if you'd be ready to switch."

**What the signal means:** Handing over access credentials to a product they are actively using is a significant commitment. It reveals genuine readiness to switch, not just openness to switching someday. Users who are only mildly interested will not do this. Users who genuinely see this as a substantially better solution will.

**Value Test 4 — Referral**

Two variants, use one or both:

Net Promoter Score variant: "On a scale of 0 to 10, how likely would you be to recommend this product to a friend or colleague?"

Commitment variant: "Would you be willing to enter your boss's email address or a colleague's email address so we could tell them about this? We wouldn't actually email them without asking you first — I'm just curious if this is something you'd be willing to put your name behind."

**What the signal means:** Willingness to share on social media, provide a boss's email, or give a high Net Promoter Score indicates that the user is willing to stake their reputation on recommending this product. This cuts through politeness more effectively than asking "Would you use this?" — people are far more careful when their professional reputation is involved.

### Part 4: Iterate the Prototype

After each session (or set of sessions), update the prototype based on what you learned.

**There is no requirement to keep the test identical across all subjects.** The goal is rapid learning, not statistical proof. If session two reveals that users are confused by the navigation, fix the navigation before session three.

**Decision rules:**

- If responses are substantially different across users, investigate why. You may have different customer segments with different problems, or your solution may work for some use cases but not others.
- If you cannot get users interested in the problem or cannot make the solution usable enough that they perceive value, consider stopping and putting the idea on the shelf. This is not failure — it is the discovery process preventing engineering investment in something customers will not value.
- If users consistently show genuine value signals (willingness to pay, invest time, provide access, or recommend), proceed to the next steps: quantitative validation or full build planning.

## Session Notes Template

Use this template to capture findings immediately after each session:

```
Session Date: 
User Profile: [role, company size/type, current solution]
Problem Confirmed: [ ] Yes  [ ] No  [ ] Partial

Usability Issues Observed:
- [Issue 1 — where it occurred, what the user did]
- [Issue 2...]

Value Test Results:
- Money test: [ ] Strong  [ ] Lukewarm  [ ] Declined  [ ] Not administered
- Time test: [ ] Strong  [ ] Lukewarm  [ ] Declined  [ ] Not administered
- Access test: [ ] Strong  [ ] Lukewarm  [ ] Declined  [ ] Not administered
- Referral test: NPS score: __  Willing to provide email: [ ] Yes  [ ] No
  
Verbal Signals: [What did the user say that was most revealing?]
Behavioral Signals: [What did the user do that was most revealing?]
Body Language / Tone: [Did enthusiasm match stated opinion?]
Surprising Observations: 
Prototype Changes Before Next Session:
Overall Value Signal: [ ] Strong  [ ] Mixed  [ ] Weak  [ ] Negative
```

## Email Summary Format

After each session or set of sessions, the product manager or designer sends a brief email to the product team:

**Subject:** Value test learnings — [Feature Name] — [Date]

**Body:**
- What worked (tasks completed, strong value signals)
- What didn't work (friction points, weak value signals)
- What surprised us
- Changes being made to the prototype
- Next session scheduled: [date/time]

Keep it to one page or less. Long reports are obsolete before they are read.
