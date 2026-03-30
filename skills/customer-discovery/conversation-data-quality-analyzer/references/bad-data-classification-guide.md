# Bad Data Classification Guide

> Deep reference for the conversation-data-quality-analyzer skill.
> Contains the full taxonomy, detection markers, and recovery techniques.

## The Three Types of Bad Data

Bad data gives false negatives (thinking the idea is dead when it is not) and -- more dangerously -- false positives (convincing yourself you are right when you are not).

### 1. Compliments

**Definition:** Vacuous positive feedback that tricks you into thinking the meeting went well.

**Why they are worthless:** Even if they genuinely like it, that data is still worthless. Venture capitalists (professional judges of the future) are wrong far more often than right. If even a VC's opinion is probably wrong, a random person's opinion has even less weight. The only exception is industry experts who have built very similar businesses.

**Detection markers in statements:**
- "That's cool"
- "I love it"
- "Sounds great"
- "Sounds terrific"
- "Keep me in the loop"
- "That would be awesome"
- Any praise directed at your concept rather than describing their situation

**Detection markers in your own behavior (symptoms):**
- In the meeting: "Thanks!" or "I'm glad you like it"
- Back at the office: "That meeting went really well"
- Back at the office: "We're getting a lot of positive feedback"
- Back at the office: "Everybody I've talked to loves the idea"

**Recovery technique -- DEFLECT:**
- Ignore the compliment entirely
- Redirect to facts: "How are you dealing with this stuff at the moment?"
- Prevention: do not mention your idea at all

### 2. Fluff

**Definition:** Vague, non-specific feedback that sounds like data but lacks concrete grounding.

**Three shapes of fluff:**

| Shape | Trigger Phrases | Example |
|-------|----------------|---------|
| Generic claims | "I usually," "I always," "I never" | "I usually manage my projects pretty well" |
| Future-tense promises | "I would," "I will" | "I would definitely buy that" |
| Hypothetical maybes | "I might," "I could" | "I could see myself using something like that" |

**The world's most deadly fluff:** "I would definitely buy that." It sounds concrete. As a founder, you desperately want to believe it is money in the bank. But people are wildly optimistic about what they would do in the future. They are always more positive, excited, and willing to pay in the imagined future than they are once it arrives.

**Fluff-inducing questions (the interviewer's fault):**
- "Do you ever..."
- "Would you ever..."
- "What do you usually..."
- "Do you think you..."
- "Might you..."
- "Could you see yourself..."

These questions are not toxic in themselves -- they can transition into concrete questioning. The mistake is in valuing the answers, not asking the questions.

**Recovery technique -- ANCHOR:**
- Ask: "When's the last time that happened?"
- Ask: "Can you talk me through that?"
- Ask: "Can you walk me through a specific example?"
- Transition sequence: fluffy question -> fluffy answer -> anchor to past -> concrete details

**Anchoring example:**
- Them: "I'm an Inbox Zero zealot. It's totally changed my life." (generic claim)
- You: "What's your inbox at right now?" (anchor to present)
- Them: "Looks like about ten that have come in since this morning." (fact)
- You: "When's the last time it totally fell apart for you?" (anchor to past)
- Them: "Three weeks ago, I was travelling and the internet at the hotel totally didn't work. It took me like ten days to get back on track." (concrete fact)

### 3. Ideas (Feature Requests)

**Definition:** Feature requests, suggestions, or solutions proposed by the customer once they get excited about your concept.

**Why they are dangerous:** Startups are about focusing and executing on a single, scalable idea rather than jumping on every good one which crosses your desk. When you accept feature requests at face value, you get feature creep. The author built three months of unnecessary analytics features for MTV because he accepted "we need analytics" without asking why they wanted it. The real need was automated weekly emails to clients, not a self-serve analytics dashboard.

**Detection markers:**
- "You should add..."
- "Can you make it do..."
- "Are you going to be able to sync to..."
- "What about adding..."
- "It would be great if it could..."
- "Have you thought about..."

**Recovery technique -- DIG:**

Questions to dig into feature requests:
1. "Why do you want that?"
2. "What would that let you do?"
3. "How are you coping without it?"
4. "Do you think we should push back the launch to add that feature, or is it something we could add later?"
5. "How would that fit into your day?"

Questions to dig into emotional signals:
1. "Tell me more about that."
2. "That seems to really bug you -- I bet there's a story here."
3. "What makes it so awful?"
4. "Why haven't you been able to fix this already?"
5. "You seem pretty excited about that -- it's a big deal?"
6. "Why so happy?"
7. "Go on."

## The Six Anti-Patterns

### 1. Compliment Acceptance

**What it is:** Treating compliments as validation data.

**Symptoms:**
- Your meeting notes list compliments as positive signals
- You tell your team the meeting "went well" without citing specific facts
- Your pipeline is full of people who "loved it" but have not committed anything

**Root cause:** Compliments feel like data because we desperately want them to be.

**Fix:** Strip all compliments from your notes. If the remaining facts do not support your conclusion, the meeting did not actually go well.

### 2. Fishing for Compliments

**What it is:** Intentionally seeking approval instead of truth. You have already made up your mind and need someone's blessing to take the leap.

**Symptom phrases from the interviewer:**
- "I'm thinking of starting a business... so, do you think it will work?"
- "I had an awesome idea for an app -- do you like it?"

**Fix:** Do not mention your idea. Ask about their life instead.

### 3. Ego Exposure Bias (The Pathos Problem)

**What it is:** Accidentally triggering protective compliments by exposing how much you care about the idea. Once someone detects that your ego is on the line, they will give you fluffy half-truths and extra compliments. Even asking for honest criticism does not fix it -- people still pull their punches.

**Symptom phrases from the interviewer:**
- "So here's that top-secret project I quit my job for... what do you think?"
- "I can take it -- be honest and tell me what you really think!"

**Fix:** Keep the conversation focused on the other person. Ask about specific, concrete cases and examples. People rarely lie about specific stuff that has already happened, regardless of your ego.

### 4. Accepting Fluff

**What it is:** Treating generic claims, hypothetical future promises, and "I would definitely buy that" statements as meaningful signal.

**Detection:** Fluff statements in notes without corresponding anchoring follow-ups. No "when was the last time" or "can you walk me through" questions visible.

**Fix:** Anchor every generic claim to a specific past instance. If they cannot provide one, the claim is not data.

### 5. Being Pitchy

**What it is:** Holding someone hostage until they say they like your idea. The dark side of approval-seeking -- instead of being vulnerable, you are being annoying.

**Symptom phrases from the interviewer:**
- "No no, I don't think you get it..."
- "Yes, but it also does this!"

**Fix:** Apologize and redirect. "Whoops -- I just slipped into pitch mode. I'm really sorry about that. Can we jump back to what you were saying?"

### 6. Obeying Feature Requests

**What it is:** Adding feature requests to the roadmap without digging into the motivation behind them.

**Detection:** Ideas listed as action items or roadmap entries. No "why do you want that?" follow-up visible in the notes.

**Fix:** For every feature request, ask the digging questions (see Ideas section above). The request is a surface symptom. The underlying motivation is the real data.

## The Complainer vs Customer Distinction

When anchoring fluff, you may discover the person is a complainer, not a customer. The pattern looks like this:

- "Someone should definitely make an X!" -> Have you looked for an X? -> "No, why?" -> They are not your customer.
- "I would definitely use that!" -> Have you tried any existing solutions? -> "I downloaded a couple but they were annoying" -> "Why didn't you keep using them?" -> "I'll do it next time. Not a real problem." -> They are a complainer, not a customer.

Long story short, if someone is not willing to try solving the problem themselves, they are not going to care about your solution either. Complainers live in the la-la-land of imagining they are the sort of person who finds clever ways to solve the petty annoyances of their day.

## Quick Reference: The Deflect-Anchor-Dig Workflow

```
HEAR a compliment?     → DEFLECT: Ignore it. Ask about their current process.
HEAR fluff?            → ANCHOR: "When was the last time that happened?"
HEAR a feature request → DIG: "Why do you want that? What would that let you do?"
HEAR an emotion?       → DIG: "Tell me more about that. What makes it so [awful/exciting]?"
```
