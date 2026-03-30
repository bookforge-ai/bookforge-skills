---
name: conversation-format-selector
description: Choose the right conversation format — casual chat, scheduled meeting, or phone/video call — for a customer discovery interaction. Use this skill whenever the user is deciding between a formal meeting and a casual conversation, wondering how long customer interviews should be, unsure whether to meet in person or do a phone or video call, preparing to talk to potential customers at a conference or event or meetup, asking how to approach someone at a networking event or industry gathering, spending too much time scheduling formal meetings and not getting enough conversations done (the meeting anti-pattern), defaulting to hour-long Zoom calls for every customer interaction, planning the logistics or setting or duration of a customer conversation, or wondering whether a conversation should be structured or informal — even if they don't explicitly mention "format" or "meeting type." This skill is about HOW to have the conversation (format, duration, setting, formality level), not about finding people to talk to (use conversation-sourcing-planner) or what questions to ask (use conversation-question-designer).
version: 1
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [4, 6]
domain: customer-discovery
tags: [customer-discovery, conversation-format, meeting-planning, casual-conversations, customer-interviews]
depends-on:
  - conversation-sourcing-planner
  - conversation-question-designer
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Description of the conversation context — who the user wants to talk to, what they want to learn, and their current relationship with the target person"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
---

# Conversation Format Selector

## When to Use

You need to decide how to structure an upcoming customer discovery interaction — the format, duration, setting, and approach. Typical situations:

- The user is about to reach out to a potential customer and is deciding whether to request a formal meeting or keep it casual
- The user has an opportunity to talk to someone at an event, conference, or social setting and wants to know how to approach it
- The user is defaulting to scheduling calendar meetings for every conversation and may be falling into the Meeting Anti-Pattern
- The user is considering a phone or video call instead of meeting in person
- The user wants guidance on how long a conversation should be given their learning goals

Before starting, verify:
- Does the user know what they want to learn? (If not, suggest they use the `conversation-question-designer` skill first)
- Does the user have a specific person or type of person in mind? (If not, they need to define their target first)

**Mode: Plan-only** — The agent recommends a conversation format with timing, setting, and approach guidance. The human executes the actual conversation.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Who they want to talk to:** Role, seniority, relationship to the user (stranger, acquaintance, warm intro, existing contact). This determines formality requirements and which formats are available.
  - Check prompt for: person descriptions, titles, "I want to talk to...", event attendee descriptions
  - Check environment for: `customer-segments.md`, `conversation-notes/`, contact lists
  - If still missing, ask: "Who do you want to talk to? What is their role and how do you know them (or don't)?"

- **What they want to learn:** The user's current learning goals. This determines how much time the conversation actually needs.
  - Check prompt for: assumptions to validate, questions to answer, "I want to find out..."
  - Check environment for: `question-script.md`, `learning-log.md`, `product-idea.md`
  - If still missing, ask: "What are the 1-3 most important things you want to learn from this conversation?"

### Observable Context (gather from environment)

- **Product stage:** Pre-product (learning only) vs post-product (learning + demo). This changes duration needs and format constraints.
  - Look for: product descriptions, prototypes mentioned, demo references
  - If unavailable: assume pre-product

- **Conversation setting:** Where the interaction might happen — industry event, office, coffee shop, online, or unplanned encounter.
  - Look for: event mentions, location references, "I'll be at..."
  - If unavailable: assume the user is choosing and needs a recommendation

- **Previous conversations:** Whether the user has talked to this type of person before.
  - Look for: `conversation-notes/`, learning logs, "I've already talked to..."
  - If unavailable: assume first conversations with this segment

### Default Assumptions

- If no product stage specified -> assume pre-product (learning phase)
- If no relationship specified -> assume cold or weak-tie contact
- If no setting specified -> recommend the most effective format for their learning goals

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Target person type is known
- At least 1 learning goal is identified

PROCEED WITH DEFAULTS when:
- Learning goals are approximate ("I want to understand their workflow")
- Person type is general ("marketing managers" without specific individual)

MUST ASK when:
- No target person type at all
- No learning goals or topic area
```

## Process

### Step 1: Assess Learning Depth Required

**ACTION:** Categorize the user's learning goals into one of four depth levels. Each level has a natural duration range that should drive format selection.

**WHY:** The biggest mistake in conversation planning is letting the calendar dictate duration instead of letting the learning goal dictate it. A 1-hour formal meeting costs roughly 4 hours when you factor in scheduling, commuting, and review time. If your learning goal only requires 5 minutes of actual conversation, that overhead is a massive waste of the most precious startup resource: founder time and attention.

| Depth Level | Duration | What You Are Learning | Example Goals |
|-------------|----------|----------------------|---------------|
| **Validate existence** | 5 minutes | Whether a problem exists and matters to this person | "Is hiring actually painful for them?", "Do they even care about analytics?" |
| **Understand workflow** | 10-15 minutes | How they currently achieve a goal or handle a problem, what they have tried | "How do they onboard new employees?", "What does their reporting process look like?" |
| **Deep industry dive** | 30-60 minutes | Industry dynamics, complex purchasing processes, organizational politics | "How does budget approval work in their company?", "What is the competitive landscape for their tools?" |
| **Product feedback** | 30 minutes (structured) | Reactions to a prototype or product, purchasing intent, next steps | "Will they try the beta?", "What would they change about the interface?" |

**IF** the user's learning goals span multiple depth levels -> recommend the shallowest level that covers the most critical goal. Additional goals can be addressed in follow-up conversations.

**OUTPUT:** The identified depth level with estimated actual conversation time needed.

### Step 2: Evaluate Format Options

**ACTION:** Score each of three conversation formats against the user's specific context using the trade-off criteria below. Recommend the highest-scoring option.

**WHY:** Each format has structural advantages and disadvantages that affect the quality of learning. Casual conversations produce less biased data because the other person does not feel like they are "doing you a favor." Formal meetings are sometimes necessary but carry overhead and expectation costs. Phone and video calls sacrifice body language, weaken the power dynamic, and eliminate the possibility of warm introductions afterward. Choosing the wrong format means you either waste time on unnecessary formality or miss learning that required deeper engagement.

**Three format options:**

#### Option A: Casual Conversation
- **Best for:** Validate-existence and understand-workflow depth levels. Pre-product stage. Situations where you can encounter the target person organically (events, shared communities, mutual connections).
- **Advantages:** No scheduling overhead, no expectation you will show a product, produces less biased responses because the person does not know they are in a "meeting," allows serendipitous follow-up topics, easy to do many in a single outing.
- **Constraints:** Not appropriate for senior executives you have no relationship with. Hard to take detailed notes in real time. Requires knowing your 3 key questions so you can navigate the conversation without a script.
- **Duration:** 5-15 minutes of actual conversation.
- **Settings:** Industry events, conferences, meetups, coffee shops, coworking spaces, social gatherings, online communities (DMs or forum threads).

#### Option B: Scheduled Meeting
- **Best for:** Deep-industry-dive and product-feedback depth levels. Post-product stage. Senior people outside your network who require a formal ask. Situations where you need a full hour of focused time.
- **Advantages:** Dedicated attention, ability to show a product or prototype, appropriate for decision-makers and enterprise contacts, easier to take structured notes.
- **Constraints:** High overhead (1-hour meeting typically costs 4 hours total with scheduling, travel, and review). Sets expectation you will show something. Creates formal dynamic that can bias responses. Harder to get the meeting in the first place.
- **Duration:** 30-60 minutes of scheduled time.
- **Settings:** Office meetings, video calls, coffee meetings by appointment.

#### Option C: Phone or Video Call
- **Best for:** Geographic constraints where in-person is impossible. Quick follow-ups with people you have already met. Situations where the learning goal is narrow and specific.
- **Advantages:** No travel time, easy to schedule, works across distances.
- **Constraints:** Loses body language and environmental observation. Creates an interview dynamic that feels formal even when the content is casual. Kills the possibility of in-person warm introductions to colleagues. The person feels less engaged and more like they are doing you a favor. Tends to default to 30-minute calendar blocks regardless of actual learning needs.
- **Duration:** Match to actual learning need (often 10-15 minutes is sufficient, not 30).

**Scoring criteria:**

| Criterion | Question to Ask |
|-----------|----------------|
| **Time efficiency** | Does the format match the actual time needed, or does it force unnecessary overhead? |
| **Data quality** | Does the format minimize bias and maximize honest responses? |
| **Relationship building** | Does the format create opportunities for follow-up and warm introductions? |
| **Accessibility** | Can the user actually achieve this format given their relationship with the target person? |

**IF** the user is defaulting to scheduled meetings for every conversation -> flag the Meeting Anti-Pattern (the tendency to relegate every customer conversation opportunity into a formal calendar block). Explain that over-reliance on formal meetings wastes time, sets expectations you will show a product, and causes you to overlook perfectly good chances for serendipitous learning.

**IF** the user is considering a phone call primarily to avoid awkwardness -> flag this as an avoidance pattern, not a strategic choice. Phone calls sacrifice too much signal quality to be used as a comfort mechanism.

### Step 3: Apply the Advisor Evaluation Mindset

**ACTION:** Reframe the user's internal approach to the conversation, regardless of format.

**WHY:** The default mindset for customer conversations is needy: you are asking someone for their time, hoping they will validate your idea, grateful for their attention. This creates a power imbalance where you feel subordinate, which leads to pitching, compliment-seeking, and failure to press for real answers. Reframing the conversation as an advisor evaluation flips the dynamic: instead of seeking customers, you are evaluating whether this person would make a good advisor for your space. The conversation topics stay the same, but you are now in the evaluator's seat, which makes you calmer, more confident, and more likely to ask hard questions.

**Guidance to include in the recommendation:**
- Go into the conversation looking for helpful, knowledgeable people who understand your problem space, not looking for customers or validation
- Evaluate whether this person has genuine insight and experience, which naturally puts you in control of the dynamic
- You do not need to tell them you are evaluating them as an advisor; this is about your internal narrative, not an explicit request
- This mindset works for every format (casual, meeting, or call) but has the biggest impact on formal meetings where the needy dynamic is strongest

**IF** the recommended format is a formal meeting -> emphasize the advisor evaluation mindset especially strongly, because formal meetings are where the needy dynamic is most damaging.

### Step 4: Produce the Format Recommendation

**ACTION:** Write a concrete recommendation document covering format choice, timing, setting, approach, and preparation checklist.

**WHY:** The recommendation must be actionable — not a theoretical comparison. The user should be able to read it once and know exactly what to do, how long it will take, and what mindset to carry into the conversation.

**Output format:**

```markdown
# Conversation Format Recommendation

## Context
- **Target:** [who they are talking to]
- **Learning Goals:** [what they want to learn]
- **Product Stage:** [pre-product / post-product]
- **Date Prepared:** [today]

## Recommended Format
**[Casual Conversation / Scheduled Meeting / Phone Call]**

### Why This Format
[2-3 sentences explaining why this format fits their specific context,
referencing the depth level and trade-off analysis]

### Timing
- **Actual conversation time needed:** [X minutes]
- **Total time investment:** [Y minutes, including overhead]
- **Duration guidance:** [specific advice on when to wrap up or extend]

### Setting
- **Where:** [specific setting recommendation]
- **Alternative:** [backup option if primary is not available]

### Approach
- **Mindset:** [advisor evaluation framing specific to their situation]
- **Opening:** [how to start the conversation naturally given the format]
- **Formality check:** [how to tell if the conversation is too formal]

### Preparation Checklist
- [ ] Know your 3 key questions (use `conversation-question-designer` if needed)
- [ ] [Format-specific prep item]
- [ ] [Format-specific prep item]

### Formality Warning Signs
Watch for these signals that the conversation has become too formal:
- You open with "Thanks for agreeing to this interview..."
- You are using rating scales ("On a scale of 1 to 5...")
- It feels like they are doing you a favor by talking to you
- You are following a rigid script instead of having a natural conversation

If you notice these → loosen up, drop the script, and ask about
something genuinely interesting about their work.
```

**IF** the user provided a file path or working directory -> write the output to `format-recommendation.md`
**ELSE** -> present the output directly in the conversation

## Examples

### Example 1: Founder Planning Customer Conversations at an Industry Conference

**Scenario:** A founder building a tool for restaurant inventory management is attending a food industry trade show next week. They want to talk to restaurant owners about how they manage ingredient ordering.

**Trigger:** "I'm going to a food industry conference next week. I want to learn how restaurant owners handle inventory and ordering. Should I try to set up meetings beforehand, or just wing it at the event?"

**Process:**
1. Depth assessment: Understand-workflow level (10-15 minutes needed per conversation)
2. Format scoring: Casual conversation scores highest — organic access to target customers at an event, no scheduling overhead, can do 6-10 conversations in a single day
3. Advisor evaluation: Reframe from "trying to get meetings with busy restaurant owners" to "evaluating which restaurant operators really understand the inventory challenge"

**Output (abbreviated):**
```
## Recommended Format
**Casual Conversation**

### Why This Format
You are attending an event where your target customers are already present
and open to talking. Scheduling formal meetings in advance would cost you
4 hours of overhead per conversation for learning that takes 10-15 minutes.
At an event, you can have 6-10 of these conversations in a single day by
simply being curious and interested.

### Timing
- Actual conversation time needed: 10-15 minutes
- Total time investment: 10-15 minutes (no overhead)
- Duration guidance: You can usually get what you need in 10 minutes.
  If the conversation is going well and they are engaged, let it run.
  People love talking about the annoying parts of their work.

### Approach
- Mindset: You are evaluating whether these restaurant operators have
  real insight into the inventory problem. Not everyone will. Some will
  have it solved. That is useful data too.
- Opening: "How do you handle ordering for a place this size? I imagine
  that gets complicated."
- Formality check: If you catch yourself saying "Can I ask you a few
  questions about your business?" you have made it too formal. Just be
  interested.
```

---

### Example 2: Product Manager Deciding Between Phone Call and In-Person Meeting

**Scenario:** A product manager at a B2B analytics company wants to understand how marketing directors at mid-sized companies create executive reports. They have a warm introduction to a specific marketing director at a company across town.

**Trigger:** "I have a warm intro to a marketing director. Should I suggest a phone call or go meet them in person? I don't want to waste their time with a full meeting."

**Process:**
1. Depth assessment: Understand-workflow level (10-15 minutes), but could tip into deep-industry-dive if the reporting process is complex (30 minutes)
2. Format scoring: Scheduled meeting slightly edges out casual because this is a warm intro to a specific senior person. Phone call scores lowest — loses body language, creates interview feel, and eliminates the warm-intro pipeline (the marketing director might introduce you to their team or peers if you are there in person).
3. Advisor evaluation: Reframe from "I don't want to waste their time" (needy framing) to "I want to find out if this person really understands the reporting challenge well enough to be a useful advisor"

**Output (abbreviated):**
```
## Recommended Format
**Scheduled Meeting (30 minutes)**

### Why This Format
You have a warm introduction to a senior person, which makes a meeting
request natural and appropriate. A phone call would work logistically
but costs you two things: body language observation (you will see their
reaction when they describe report-building pain) and the opportunity
for them to introduce you to peers on the spot. Those in-person warm
intros are extremely valuable and impossible over the phone.

### Timing
- Actual conversation time needed: 15-20 minutes of questions
- Total time investment: ~2 hours (travel + meeting + review)
- Duration guidance: Request 30 minutes. Spend the first 5 on greetings,
  15-20 on your questions, and the last 5 asking who else you should
  talk to.

### Approach
- Mindset: You are evaluating whether this marketing director
  has deep enough reporting pain to be a useful advisor for your space.
  You are not asking for a favor — you are seeing if they qualify.
- Formality check: If you open with "Thanks for taking the time..."
  you are signaling that they are doing you a favor. Instead, open
  with genuine curiosity about their work.
```

---

### Example 3: Early-Stage Founder Defaulting to Formal Meetings

**Scenario:** A solo founder is exploring a productivity app idea and has been scheduling 1-hour Zoom calls with anyone who will talk to them. After 3 weeks, they have completed only 4 conversations and are feeling overwhelmed by the time investment.

**Trigger:** "I've been doing hour-long Zoom interviews but I've only managed 4 in three weeks. This is taking forever. Am I doing something wrong?"

**Process:**
1. Depth assessment: Validate-existence level (5 minutes needed) — the founder is still in early exploration and does not yet know if the problem is real
2. Format scoring: Flag the Meeting Anti-Pattern immediately — the founder is relegating every conversation to a 1-hour calendar block when they need 5-minute casual chats. Four conversations in three weeks is a symptom of format mismatch, not a scheduling problem.
3. Advisor evaluation: The founder's frustration comes from the needy dynamic — each call feels like a big ask, which makes scheduling emotionally draining

**Output (abbreviated):**
```
## Recommended Format
**Casual Conversation**

### Why This Format
You are falling into the Meeting Anti-Pattern — relegating every
conversation to a formal calendar block. At your current stage (early
exploration, pre-product), you need to learn whether the problem you
are exploring actually exists and matters to people. That takes about
5 minutes of conversation, not 60.

Your current setup costs roughly 4 hours per conversation (scheduling,
prep, the call itself, review). At that rate, 4 conversations in 3
weeks is actually the expected throughput — the problem is the format,
not your hustle.

Switch to casual conversations. Go where your target users already are
(coworking spaces, meetups, online communities). Strike up conversations
about their work. You should be able to have 5-10 of these in a single
outing, each taking 5-10 minutes.

### Formality Warning Signs
You mentioned "hour-long Zoom interviews" — the word "interview" itself
is a red flag. Learning from customers does not require wearing a suit
and drinking boardroom coffee. If you are using rating scales, structured
interview guides, or opening with "Thanks for agreeing to this," you
have made it too formal.

### Preparation Checklist
- [ ] Know your 3 key questions (the 3 most important things you want
      to learn — use `conversation-question-designer` if needed)
- [ ] Identify 2-3 places where your target users gather (online or
      in person) — use `conversation-sourcing-planner` for ideas
- [ ] Practice your opening: a casual question about their work, not
      a request for an interview
```

## Key Principles

- **Format should match learning depth, not social convention** — A 1-hour formal meeting is appropriate when you need a deep industry dive or product feedback session. For validating whether a problem exists, 5 minutes of casual conversation produces the same learning with a fraction of the time cost. Let what you need to learn determine how you have the conversation, not the arbitrary conventions of calendar software.

- **Formality biases responses** — When a conversation feels like an interview, people give interview answers: polished, diplomatic, and unhelpful. When it feels like a chat between peers, they tell you what actually happens. If it feels like they are doing you a favor by talking to you, the conversation is probably too formal. The best customer conversations happen when the other person does not even realize it was a "meeting."

- **The Meeting Anti-Pattern is the most common format mistake** — First-time founders default to scheduling formal meetings for every customer interaction because it feels structured and professional. But the overhead (scheduling, commuting, prep, review) means a 1-hour meeting actually costs 4 hours. At that rate, you will never talk to enough people. Casual conversations at events and in communities let you compress a dozen learnings into a single outing.

- **Evaluate advisors, do not seek validation** — The default mindset going into customer conversations is needy: you want their approval, their time, their enthusiasm. Flip this by going in to evaluate whether they would make a good advisor for your space. You are looking for helpful, knowledgeable people. This reframe changes the power dynamic without changing the conversation topics, and it works regardless of format.

- **Phone calls are a considered trade-off, not a default** — Phone and video calls are convenient but sacrifice body language observation, weaken the power dynamic, and eliminate the possibility of in-person warm introductions. Use them when geography makes in-person impossible or when following up with someone you have already met, not as a way to avoid the awkwardness of face-to-face conversation.

## References

- For sourcing conversation opportunities and outreach framing, use the `conversation-sourcing-planner` skill
- For designing specific questions to ask during the conversation, use the `conversation-question-designer` skill
- For evaluating commitment signals after the conversation, use the `commitment-signal-evaluator` skill
