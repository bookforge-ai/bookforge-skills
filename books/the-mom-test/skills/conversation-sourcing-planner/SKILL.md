---
name: conversation-sourcing-planner
description: Create a plan for finding and reaching people to have customer discovery conversations with, including channel selection, outreach messages, and warm intro strategies. Use this skill whenever the user does not know how to find people to talk to, does not know anyone in their target market, needs to reach potential customers but has no connections, wants to write a cold outreach email or LinkedIn message for customer conversations, needs help with warm introductions or getting introduced to prospects, is struggling to get meetings or conversations with target customers, wants to build a conversation pipeline or outreach cadence, asks "where do I find people to interview" or "how do I get customer meetings," needs to figure out the best channels to reach a specific customer segment, wants to plan cold or warm outreach for customer interviews, or wants to leverage events or communities or online forums to find conversation targets — even if they don't explicitly say "sourcing" or "outreach." This skill is about FINDING and REACHING people, not about who your target customer is (use customer-segment-slicer) or whether meetings should be casual or formal (use conversation-format-selector).
version: 1
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [9]
tags: [customer-discovery, outreach, conversation-sourcing, cold-outreach, warm-intros, meeting-framing, advisory-flip]
depends-on:
  - customer-segment-slicer
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Target customer segment description (ideally a who-where pair from customer-segment-slicer)"
    - type: document
      description: "Product stage and vision description"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Operates on text documents describing target segments and product context. Agent creates the outreach plan; human executes the actual conversations."
---

# Conversation Sourcing Planner

## When to Use

You are in a situation where the user has a defined customer segment (ideally a who-where pair) and needs a concrete plan to reach those people and start conversations. Typical triggers:

- The user has completed customer segmentation but does not know how to actually reach their target segment
- The user is stuck at zero conversations and needs a way to get started
- The user has tried one channel (usually cold email) and it is not working — they need alternatives
- The user wants to write outreach messages but does not know how to frame them without triggering sales-meeting dynamics
- The user needs to plan how many conversations to have and over what timeline
- The user feels awkward or needy about asking strangers for meetings

Before starting, verify:

- Does the user have a specific customer segment defined? (If not, they need `customer-segment-slicer` first — a sourcing plan without a defined segment will produce unfocused outreach that wastes everyone's time)
- Does the user know their product vision, even roughly? (Needed for framing outreach messages)
- Is the user clear on what they want to learn? (If not, note this gap in the plan — they should define learning goals before having conversations)

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Target customer segment:** Who is the user trying to reach? Must be specific enough to identify concrete finding locations. A who-where pair is ideal.
  - Check prompt for: customer descriptions, segment names, who-where pairs, references to a customer-segments.md file
  - Check environment for: `customer-segments.md` in the working directory
  - If still missing, ask: "Who specifically are you trying to have conversations with? If you have a customer segment document, point me to it. If not, describe your target customer as specifically as you can — who they are and where you might find them."

- **Product stage and vision:** What is the user building and how far along are they? This determines whether outreach should emphasize "nothing to sell" (pre-product) or "early version to show" (post-product).
  - Check prompt for: product descriptions, stage indicators (idea, prototype, MVP, launched)
  - Check environment for: `product-idea.md` or similar product brief
  - If still missing, ask: "What is your product or business idea, and what stage are you at? (idea stage, prototype, MVP, or launched product)"

### Helpful Context (gather if available)

- **Existing network:** Does the user already know anyone in their target segment? Do they have warm connections, advisors, or investors who could make introductions?
- **Previous outreach attempts:** Has the user already tried reaching out? What worked and what did not?
- **Available platforms:** Does the user have a blog, social media presence, email list, or landing page? These affect which "bring them to you" channels are viable.
- **Geographic constraints:** Is the user limited to a specific location, or can they reach people remotely?
- **Team composition:** Is anyone on the team embedded in the target industry? Do they have a PhD student (built-in excuse for research conversations)?

### Default Assumptions

- If no network information is provided, assume the user is starting cold with no existing connections in the target segment
- If no platform presence is mentioned, assume the user has no blog, list, or social following to leverage
- If product stage is unclear, default to pre-product (nothing to sell yet) — this is the safer framing for outreach
- If geographic constraints are not mentioned, assume the user can do both in-person and remote outreach

## Process

### Step 1: Assess the Starting Position

**ACTION:** Evaluate the user's current assets and constraints to determine which conversation channels are viable.

**WHY:** Different founders start from radically different positions. Someone embedded in their target industry already has warm connections and credibility. Someone entering a new industry starts cold and needs different tactics. Matching channels to the user's actual starting position prevents wasted effort on channels that require assets they do not have.

Assess these four dimensions:

1. **Network proximity** — How many degrees of separation from the target segment? (0 = they ARE the target, 1 = know people directly, 2 = know people who know people, 3+ = no connection)
2. **Platform presence** — Do they have any audience, content, or online presence relevant to this segment? (blog, social following, email list, landing page)
3. **Industry credibility** — Would the target segment recognize the user as someone worth talking to? (industry experience, relevant expertise, academic credentials)
4. **Time and geography** — Can the user attend in-person events? How many hours per week can they dedicate to outreach?

**IF** network proximity is 0-1 → prioritize warm intro channels (advisors, existing contacts, network asks)
**IF** network proximity is 2+ → start with cold channels and immersion, plan to convert cold contacts into warm intros over time
**IF** the user has platform presence → include "bring them to you" channels (blogging, teaching, landing pages)
**IF** the user has no platform → skip those channels for now and focus on "going to them" and warm intro strategies

### Step 2: Score and Rank Available Channels

**ACTION:** Evaluate each of the 7 conversation channels against the user's specific situation and rank them by expected yield.

**WHY:** Not every channel works for every founder. Cold calls work when you only need a 2% response rate to start the snowball. Organizing meetups works when you have time and a findable community. The right channel depends on the user's assets, segment, and constraints. Scoring prevents the user from defaulting to whatever feels most comfortable (usually cold email) when a higher-yield channel is available.

Evaluate these 7 channels:

| Channel | How It Works | Best When |
|---------|-------------|-----------|
| **Cold outreach** | Email, LinkedIn, or cold calls to target contacts. Expect 2% response rate — but you only need one or two to start the intro snowball. | You have no connections at all and need to bootstrap from zero. The rejection rate is irrelevant — you are not selling, you are starting a snowball. |
| **Seize serendipity** | Use casual encounters (parties, conferences, co-working spaces) to start conversations when you hear relevant signals. Keep your learning goals in your head so you are ready. | You are around people socially and can recognize target customers in the wild. Works best when conversations are casual and you know your top 3 questions. |
| **Immerse yourself** | Join the communities and spaces where your target segment already gathers. Attend their events, join their forums, volunteer, give free talks. | You are entering a new industry and need to build connections from scratch. Time-intensive but produces deep understanding and organic relationships. |
| **Landing pages** | Put up a page describing your value proposition, collect emails, then personally email every person who signs up. The value is not the conversion metrics — it is the conversations from reaching out to signups. | You can describe your value proposition clearly enough to attract interest. Use the signups as qualified leads for personal outreach, not as quantitative validation. |
| **Organize events** | Host a meetup, happy hour, workshop, or knowledge exchange call for your target segment. You absorb the credibility of being the organizer. | You have a findable segment that would attend topic-specific events. Marginally more effort than attending events but dramatically more effective — you are the center of attention. |
| **Speak and teach** | Give talks, workshops, free consulting, or create educational content for your target segment. Teaching forces you to clarify your thinking and puts you in front of a self-selected audience. | You have domain expertise and opinions about how things could be better. The audience self-selects as people who take the topic seriously. |
| **Industry blogging** | Write about your target industry's problems and solutions. Even without readers, the blog serves as a credibility signal when cold emailing. People check your domain and see you are serious. | You want a long-term credibility asset. Even with zero audience, a blog makes cold emails more effective because recipients check your site. |

For each channel, score:
- **Viable?** (YES/NO — does the user have what they need to use this channel?)
- **Expected yield** (HIGH/MEDIUM/LOW — how many conversations per unit of effort?)
- **Time to first conversation** (DAYS/WEEKS/MONTHS)
- **Recommended?** (YES/NO — should this channel be in the plan?)

**Rank** the recommended channels from highest to lowest priority.

### Step 3: Identify Warm Intro Paths

**ACTION:** Map all potential paths to warm introductions for the user's target segment.

**WHY:** Warm introductions are dramatically more effective than cold outreach. When someone credible introduces you, the target contact already trusts that you are worth their time. The goal of all cold outreach is to stop having cold conversations — you hustle together the first one or two from wherever you can, treat people's time respectfully, and those cold contacts start turning into warm intros. The snowball starts rolling.

Map these warm intro sources:

1. **Existing network** — Who does the user already know who might know someone in the target segment? Apply the "7 degrees of separation" principle — the world is small, and you can find anyone you need if you ask around a few times.
2. **Industry advisors** — Would it make sense to recruit 2-5 industry advisors? Each advisor gets approximately 0.5% equity, meets monthly, and provides a steady stream of introductions. You can sometimes identify strong advisor candidates from your early customer conversations.
3. **Investors** — If the user has investors, their portfolio rolodex and industry connections are a powerful intro source, especially for B2B.
4. **Universities** — If the user is a student or recently graduated, professors are a goldmine. They get grant funding from industry contacts and those contacts are self-selected as people excited about new projects. Professors post their emails publicly and you can walk into their office.
5. **Cashing in old favors** — Anyone who previously said "sounds great, keep me in the loop and let me know how I can help" can be contacted now. Reply to that old email and ask for a specific introduction using the framing formula from Step 4.

**OUTPUT:** A list of specific warm intro paths with names or categories of people to contact, ordered by likelihood of success.

### Step 4: Draft Outreach Messages Using the Framing Formula

**ACTION:** Write 2-3 outreach message templates customized to the user's situation, using the 5-element framing formula.

**WHY:** Most outreach fails because it triggers sales-meeting dynamics. Asking "Can I interview you?" sets off alarm bells that the meeting will be boring. Asking "Can I get your opinion on what we're doing?" signals neediness and desire for approval. Asking "Do you have time for a quick coffee?" provides no context, suggesting the requester will waste time. The 5-element framing formula prevents all of these failures by establishing credibility, showing vulnerability, and making the request feel like an opportunity to help rather than a sales pitch.

The 5-element framing formula (mnemonic: "Very Few Wizards Properly Ask [for help]"):

1. **Vision** — One half-sentence of how you are trying to make the world better. Do NOT mention your idea or product. Frame it as a mission.
2. **Framing** — Mention what stage you are at. If true, say you have nothing to sell. This disarms sales defenses.
3. **Weakness** — Show vulnerability by mentioning your specific problem or knowledge gap. Give them a chance to help. This also clarifies you are not a time-waster — you have a specific need.
4. **Pedestal** — Show how much THEY in particular can help. Make it clear why you are reaching out to them specifically, not mass-emailing a list.
5. **Ask** — Ask for help. Be specific about what you need (a 15-minute chat, a coffee, an email exchange).

**IMPORTANT:** The 5 elements can be reordered based on context. If the standard order might look like a sales pitch, move Weakness earlier so the reader sees vulnerability before they delete it as spam.

Draft at least 2 templates:
- **Template A: Cold email** (for reaching people you have never met)
- **Template B: Warm intro request** (for asking someone to introduce you to a contact)
- **Template C (if applicable): Meeting opening** (for when someone else made the introduction — use them as a voice of authority, repeat your framing, then immediately drop into the first question)

**IF** the user is pre-product → emphasize "we don't have anything to sell" in the Framing element
**IF** the user is post-product → adjust Framing to "we have an early version and want to make sure we're building the right thing"

### Step 5: Apply the Advisor Evaluation Mindset

**ACTION:** Reframe the user's internal narrative from "finding customers" to "finding advisors."

**WHY:** Going into conversations looking for customers creates a needy vibe and forfeits the position of power. Instead, the user should go in search of industry and customer advisors — helpful, knowledgeable people who are excited about the space. With this mindset switch, the user knows why they are there, the meeting feels like "let me find out if you are a good advisor" instead of a needy sales meeting, and the user is now evaluating them rather than being evaluated. The topics of discussion are basically the same, but the power dynamic changes completely. This is not about explicitly telling people you are looking for advisors — it is about orienting your internal narrative to give yourself a helpful and consistent front. Willpower is finite. Changing the context of the meeting is easier than willing yourself to not be needy.

Add to the outreach plan:
- A brief reminder of the advisor evaluation mindset
- The reframe: "You are not asking for favors. You are evaluating whether this person could be a valuable advisor for your space."
- Note that strong advisor candidates may emerge from early conversations — keep an eye out for people who are genuinely knowledgeable, excited, and well-connected

### Step 6: Set Target Conversation Count and Timeline

**ACTION:** Recommend a specific number of conversations and a timeline based on the user's segment focus and product stage.

**WHY:** Every conversation has an opportunity cost — while you are in a meeting, you are not building. The goal is not a thousand meetings. It is about quickly learning what you need and getting back to building. The right number depends on segment focus: 3-5 conversations may be enough for a well-defined segment in a simple industry. If you have run 10+ conversations and results are still inconsistent, the customer segment is probably too broad and needs to be tightened up (go back to `customer-segment-slicer`). The stopping rule is: keep having conversations until you stop hearing new information.

Guidelines:
- **Focused segment, simple industry:** Target 3-5 conversations in the first 2 weeks
- **Broad segment or complex industry:** Target 5-10 conversations in the first 3 weeks
- **Sales-driven business (especially enterprise):** More conversations is fine — the opportunity cost is low because many early conversations become sales leads
- **Diminishing returns signal:** If conversations start repeating the same patterns and no new information emerges, you have enough
- **Divergence signal:** If after 10+ conversations results are all over the map, your segment is too fuzzy — return to `customer-segment-slicer`

**IF** the user is building a sales-driven business → recommend higher volume (10-15 conversations) since early conversations double as learning AND dealflow
**IF** the user is building a product-led business → recommend lower volume (3-5 conversations) and emphasize getting back to building quickly

### Step 7: Produce the Outreach Plan Document

**ACTION:** Write the complete outreach plan to a file the user can execute against and track progress.

**WHY:** A written plan with specific channels, messages, and targets transforms "I should talk to some customers" from a vague intention into an executable checklist. The plan should be a living document — channels that produce results get doubled down on, channels that do not produce results get dropped.

**HANDOFF TO HUMAN** — The agent produces the plan document. The human executes the outreach, has the conversations, and updates the plan with results.

Write the output file with this structure:

```markdown
# Conversation Sourcing Plan: {Product/Idea Name}

## Target Segment
**WHO:** {specific customer segment description}
**WHERE:** {where to find them — from who-where pair}
**Source:** {reference to customer-segments.md if available}

## Starting Position Assessment
- **Network proximity:** {0-3 score with explanation}
- **Platform presence:** {description of existing assets}
- **Industry credibility:** {current standing}
- **Available time:** {hours/week for outreach}

## Channel Plan (Ranked)

### Priority 1: {Channel Name}
- **Why this channel:** {reasoning for this segment}
- **Specific actions:** {concrete steps to take this week}
- **Expected yield:** {conversations per unit of effort}
- **Time to first conversation:** {days/weeks}

### Priority 2: {Channel Name}
{Same format}

### Priority 3: {Channel Name}
{Same format}

## Warm Intro Map
{List of specific warm intro paths with people/categories to contact}

## Outreach Templates

### Template A: Cold Email
Subject: {subject line}

{Full email using VFWPA formula with elements annotated}

### Template B: Warm Intro Request
{Full message for asking someone to make an introduction}

### Template C: Meeting Opening
{Script for when someone else introduced you}

## Mindset Reminder
{Brief advisor evaluation mindset reminder}

## Conversation Targets
- **Target count:** {N} conversations
- **Timeline:** {weeks}
- **Stopping rule:** Stop when you stop hearing new information
- **Divergence signal:** If 10+ conversations yield inconsistent results, re-slice your segment

## Progress Tracker
| # | Date | Person | Channel | Key Insight | Follow-up |
|---|------|--------|---------|-------------|-----------|
| 1 |      |        |         |             |           |
| 2 |      |        |         |             |           |
| 3 |      |        |         |             |           |

## Channel Results (update weekly)
| Channel | Attempts | Conversations | Conversion | Keep/Drop |
|---------|----------|---------------|------------|-----------|
|         |          |               |            |           |

## Revision Log
| Date | Change | Trigger |
|------|--------|---------|
| {today} | Initial plan | First outreach planning session |
```

Save to `outreach-plan.md` in the user's working directory (or the path they specify).

## Examples

### Example 1: Developer Tools Startup Entering a New Industry

**Scenario:** A two-person team has built a prototype debugging tool for embedded systems engineers. They completed customer segmentation and their starting segment is "embedded systems engineers at automotive companies who are frustrated with proprietary debugging tools." They know nobody in the automotive industry.

**Trigger:** The team says "We know who we want to talk to but we have no idea how to reach embedded systems engineers at automotive companies. We've never worked in that industry."

**Process:**
1. Starting position: network proximity 3+ (no connections in automotive), no platform presence, some technical credibility from embedded systems background but no automotive industry recognition, available 10 hours/week for outreach
2. Channel ranking: (1) Immerse yourself — attend Embedded Systems Conference and local automotive engineering meetups; (2) Cold outreach via LinkedIn — target engineers with "embedded" and "automotive" in their profiles; (3) Industry blogging — start writing about embedded debugging challenges to build credibility; (4) Organize — host a virtual "Embedded Debugging War Stories" meetup
3. Warm intro map: no direct paths, but suggested asking their university professors (both are recent graduates) and checking if their university has automotive industry partnerships
4. Outreach templates: cold LinkedIn message using VFWPA — Vision: "trying to make embedded debugging less painful"; Framing: "we're engineers ourselves, just starting out, nothing to sell"; Weakness: "we've only worked with consumer electronics and don't understand automotive constraints"; Pedestal: "your experience with [specific tool] at [company] is exactly the perspective we need"; Ask: "15 minutes to understand your debugging workflow?"
5. Advisor mindset: framed as "we're evaluating whether automotive is the right space for us and looking for people who can help us understand the landscape"
6. Target: 5 conversations in 3 weeks (new industry needs more discovery)

**Output:** Outreach plan with LinkedIn cold outreach as the immediate action (start this week, target 20 messages for 1-2 conversations), Embedded Systems Conference attendance as medium-term (next month), and a "debugging war stories" blog as a long-term credibility asset.

### Example 2: Consumer App Founder With Industry Connections

**Scenario:** A founder is building a meal planning app. She completed segmentation and is targeting "busy working parents who already meal-prep on Sundays, found in meal-prep subreddits and local meal-prep Facebook groups." She is a working parent herself and knows many others.

**Trigger:** The founder says "I'm one of my own customers and I know lots of parents who meal-prep, but I feel weird asking my friends for 'interviews.' How do I do this without being awkward?"

**Process:**
1. Starting position: network proximity 0 (she IS the target customer), strong existing network, no formal platform but active in relevant Facebook groups, high credibility as a fellow meal-prepping parent, 5 hours/week
2. Channel ranking: (1) Seize serendipity — she is already around her target customers every day at school pickup, in parent groups, at meal-prep activities; (2) Warm intros from existing network — ask parent friends "who is the most obsessive meal-prepper you know?"; (3) Immerse in online communities — engage genuinely in meal-prep subreddits and Facebook groups before starting conversations; (4) Organize — host a "Sunday meal-prep session" at her home
3. Warm intro map: 8-10 parent friends who meal-prep, 3 active meal-prep Facebook groups she is already in
4. Outreach templates: for this founder, formal outreach templates are actually WRONG. Her best conversations will happen casually — at school pickup, at the park, during playdates. The plan emphasized: do NOT frame these as interviews. Just have conversations. Ask about their meal-prep routine, what frustrates them, how they decide what to cook. Her top 3 learning goals should always be in her head so she can use any casual encounter.
5. Advisor mindset: reframed from "I need to interview parents" to "I'm curious about how other parents handle meal prep differently from me"
6. Target: 5 conversations in 2 weeks (focused segment she is already embedded in)

**Output:** Outreach plan with serendipity as primary channel (no outreach messages needed — just prepare learning goals and use casual encounters), a list of 8 specific parent friends to have meal-prep conversations with this week, and a note to keep conversations casual per `conversation-format-selector` guidance.

### Example 3: B2B SaaS With Advisory Board Strategy

**Scenario:** A funded startup is building compliance automation software for fintech companies. Their target segment is "compliance officers at Series A-C fintech startups who currently manage compliance with spreadsheets." They have two investors with fintech portfolios.

**Trigger:** The team says "We need to talk to compliance officers but they're hard to reach. They're busy, skeptical of vendors, and don't hang out in obvious communities."

**Process:**
1. Starting position: network proximity 2 (investors know fintech founders who know compliance officers), no platform but have funding credibility, moderate industry credibility (team includes an ex-compliance analyst), 15 hours/week
2. Channel ranking: (1) Investor intros — both investors have fintech portfolio companies with compliance officers; (2) Industry advisors — recruit 3-5 compliance professionals as advisors at 0.5% equity each for monthly intro flow; (3) Organize — host a "Fintech Compliance Roundtable" quarterly call for compliance officers to share challenges; (4) Speaking and teaching — offer free compliance workshops at fintech accelerators; (5) Cold outreach via LinkedIn — target compliance officers at specific fintech companies
3. Warm intro map: Investor A has 12 fintech portfolio companies, Investor B has 8. Ex-compliance analyst team member has 5 former colleagues. Combined: 25+ potential paths to compliance officers through warm introductions.
4. Outreach templates: warm intro request to investors — Vision: "making compliance automated so fintech companies can focus on building products"; Framing: "we've just raised our seed and are in discovery mode — not selling anything yet"; Weakness: "we built compliance tools internally but don't know if our approach generalizes across different fintech types"; Pedestal: "your portfolio company [X] is exactly the stage where compliance gets painful — their compliance team's perspective would be incredibly valuable"; Ask: "could you connect us with their compliance lead for a 20-minute chat?"
5. Advisor mindset: "We are building an advisory board of the smartest compliance people in fintech. Each conversation is an audition — we're evaluating whether they have the depth to help guide our direction."
6. Target: 10-15 conversations in 4 weeks (enterprise/B2B = higher volume because conversations become dealflow)

**Output:** Outreach plan with investor intros as immediate action (send 4 intro requests this week), advisory board recruitment as parallel track (identify 5 candidates from early conversations), and a quarterly compliance roundtable as a medium-term credibility play. Included email templates for investor intro requests and a separate cold LinkedIn template for direct outreach.

## Key Principles

- **The goal of cold outreach is to stop having cold outreach** — You hustle together the first one or two conversations from wherever you can. If you treat people's time respectfully and are genuinely trying to solve their problem, those cold contacts start turning into warm introductions. The snowball starts rolling. Do not try to optimize your cold outreach conversion rate — try to convert cold contacts into warm intro sources as fast as possible.

- **Rejection rate is irrelevant when you are learning, not selling** — If you reach out to 100 people and 98 hang up, you now have 2 conversations. Unless your plan is to sell via cold calls, the rejection rate does not matter. You only need one "yes" to start the intro chain. People don't like getting cold calls. No surprise there. But you only need a tiny response rate to begin.

- **Frame for help, not for sales** — When you do not know why you are in a meeting, it becomes a sales meeting by default, which is bad for three reasons: the customer closes up about pricing, attention shifts to you instead of them, and it will be the worst sales meeting ever because you are not ready. The 5-element framing formula (Vision/Framing/Weakness/Pedestal/Ask) prevents this by establishing you as someone worth helping, not someone trying to sell.

- **Bring them to you when possible** — When you are going to people, you are on the back foot. You made the approach, so they are suspicious and trying to figure out if you are wasting their time. When they come to you (through a meetup you organized, a blog post they read, a talk you gave), the dynamic flips — they take you more seriously and want to help you more. Any channel that brings customers to you saves time and changes the power dynamic.

- **The advisor evaluation mindset changes the power dynamic** — Do not go into conversations looking for customers. Go in search of industry and customer advisors. You are evaluating whether they are helpful, knowledgeable, and excited about your space. The topics of discussion are basically the same but the dynamic changes completely. You change your circumstances to require less willpower, like throwing out chocolate when you start a diet.

- **Match conversation count to segment focus, not to anxiety** — 3-5 conversations can be enough for a focused segment. 10+ conversations with inconsistent results means the segment is too broad, not that you need more conversations. The stopping rule is simple: keep talking to people until you stop hearing new information. Then get back to building.

## References

- For the complete 7-channel breakdown with tactical details and additional examples, see [references/channel-guide.md](references/channel-guide.md)
- For outreach message templates adapted to different contexts, see [references/outreach-templates.md](references/outreach-templates.md)
- **Cross-skill dependencies:** This skill requires a defined customer segment from `customer-segment-slicer` as input. After creating the outreach plan, use `conversation-format-selector` to decide whether conversations should be casual or formal.
