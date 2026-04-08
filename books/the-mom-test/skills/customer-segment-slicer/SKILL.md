---
name: customer-segment-slicer
description: Iteratively narrow broad customer segments into specific, findable sub-segments with who-where pairs. Use this skill whenever the user's target market is too broad, their customer definition is vague or generic ("small businesses," "students," "anyone who..."), they are getting mixed or inconsistent feedback from customer conversations that does not converge, they do not know who to talk to first, everyone seems like a potential customer, they need to decide which customer segment to pursue first, they are overwhelmed by too many potential customer types, they want to know who their ideal early customer is, they cannot figure out who to build for, they ask "who should I talk to" or "how do I narrow down my audience" — even if they don't explicitly say "segmentation" or "customer slicing." Do NOT use for finding or reaching customers (use conversation-sourcing-planner) or designing interview questions (use conversation-question-designer).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-mom-test/skills/customer-segment-slicer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [10]
tags: [customer-discovery, segmentation, targeting, customer-slicing, who-where-pair]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: product-idea
      description: "Description of the business idea and the problem it solves"
    - type: initial-customer-hypothesis
      description: "The user's current best guess at who their customer is"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Operates on text documents describing a product idea and customer hypotheses."
---

# Customer Segment Slicer

## When to Use

You are in a situation where the user has a product idea but their customer definition is too broad to act on. Typical triggers:

- The user describes their customer as a large, generic group ("small businesses," "students," "advertisers," "anyone who...")
- The user is getting mixed or inconsistent feedback from customer conversations and cannot make sense of it
- The user feels overwhelmed by options and does not know where to start talking to people
- The user cannot prove their idea right or wrong because every conversation "sort of" works
- The user is about to begin customer discovery and needs to pick a starting segment
- The user has talked to many people but learnings are not converging

Before starting, verify:

- Does the user have at least a rough product idea or problem hypothesis? (If not, help them articulate one first)
- Is the user's current customer definition genuinely broad? (If they already have a specific who-where pair, they may not need slicing — ask about their conversation results to confirm)

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Product idea or problem hypothesis:** What is the user building or planning to build? What problem does it solve? Ask the user if not stated.
- **Initial customer hypothesis:** Who does the user currently think their customer is? Accept even vague answers — that is the starting point for slicing.

### Helpful Context (gather if available)

- **Conversation history:** Has the user already talked to potential customers? What patterns or inconsistencies emerged?
- **Known customer types:** Does the user already recognize different sub-groups within their broad segment?
- **Existing workarounds:** Are potential customers already solving this problem somehow? How?
- **Business constraints:** Are there markets the user cannot serve (geography, regulation, resources)?

### Default Assumptions

- If no conversation history exists, treat this as pre-conversation segmentation (the user needs a starting segment before beginning customer discovery)
- If the user cannot articulate sub-groups, guide them through the slicing questions to surface them
- If no business constraints are mentioned, assume the user is open to any viable segment

## Process

### Step 1: Diagnose Whether the Current Segment Is Too Broad

**ACTION:** Evaluate the user's current customer definition against three symptoms of a too-broad segment.

**WHY:** Most founders do not realize their segment is too broad until they are already drowning in mixed signals. Startups do not starve from too few options — they drown from too many. Diagnosing this early prevents wasted conversations. If you start too generic, your marketing is watered down, you suffer feature creep, and you cannot prove yourself right or wrong because there is always someone who "sort of" likes each feature.

Check for these three symptoms:

1. **Overwhelm paralysis** — The user is overwhelmed by options and does not know where to start
2. **Unfalsifiability** — The user is not moving forward but cannot prove themselves wrong (everything "sort of" works, every feature has someone who likes it)
3. **Mixed signals** — The user receives inconsistent feedback that does not make sense (20 conversations yielding 20 different must-have features and 20 different problems)

**IF** the user shows none of these symptoms AND has a specific, findable segment → they may not need slicing. Confirm by asking: "Can you tell me exactly where you would go to find 10 of these people this week?"

**IF** the user shows one or more symptoms → proceed to Step 2.

### Step 2: Run the Slicing Questions (Iterative)

**ACTION:** Take the user's broad segment and repeatedly apply the six slicing questions to break it into specific sub-segments. This is a recursive process — keep slicing until you reach groups that are concrete enough to find and talk to.

**WHY:** A broad segment like "students" hides enormous diversity. A PhD researcher, a prep school teenager, a homeschooling parent, a child in a rural Indian village, and a student in Africa using a cellphone are all "students" — but they have completely different needs, budgets, and behaviors. You are not having 20 conversations with your customers when your segment is too broad. You are having one conversation each with 20 different types of customers. That is why feedback is inconsistent.

Apply these six questions to the current segment, one at a time:

1. **"Within this group, which type of person would want this most?"** — Identifies the highest-urgency sub-group
2. **"Would everyone in this group buy or use it, or only some of them?"** — Forces the user to acknowledge internal diversity
3. **"Why do they want it? What is their specific problem or goal?"** — Surfaces the underlying motivation
4. **"Does everyone in the group have that motivation, or only some?"** — Tests whether the motivation is universal or segment-specific
5. **"What additional motivations exist?"** — Uncovers parallel reasons different sub-groups might want the product
6. **"Which other types of people have these motivations?"** — Expands the candidate list beyond the original demographic framing

**OUTPUT from this step:** Two lists emerge:
- A list of **specific demographic sub-groups** (e.g., "non-native-speaking PhD students with upcoming conference talks")
- A list of **motivations** (e.g., "nervous about a specific upcoming event," "want to improve as a long-term skill," "need to fix accent issues")

**IF** any sub-groups are still generic → go back through them and repeat the slicing questions. Keep asking "within THAT sub-group, who wants it most?" until you reach people you can picture concretely.

### Step 3: Map Behaviors and Workarounds

**ACTION:** For each sliced sub-group, identify what they are already doing to solve the problem and where they congregate.

**WHY:** Demographics tell you WHO someone is. Behaviors tell you WHERE to find them and HOW serious they are about the problem. Someone who is already spending time and money on workarounds is a far stronger prospect than someone who merely has the problem. Behaviors also reveal natural gathering points where you can find these people efficiently.

Ask these three questions for each sub-group:

1. **"What are these people already doing to achieve their goal or cope with their problem?"** — Reveals existing workarounds and competing solutions
2. **"Where can we find people in this demographic group?"** — Identifies physical and online gathering points
3. **"Where can we find people doing these workaround behaviors?"** — Often different from demographic gathering points and frequently more valuable (someone actively searching for solutions is higher-intent than someone who merely fits a demographic)

**IF** a sub-group is un-findable (you cannot articulate where to find them) → that segment is not actionable. Go back and slice further until you can answer the "where" question.

### Step 4: Construct Who-Where Pairs

**ACTION:** Combine each viable sub-group with its best finding location to create who-where pairs.

**WHY:** A customer segment is only useful if it is both specific (who) and findable (where). "Moms who want healthy alternatives for kids" is a who without a where. "Moms shopping at independent health food stores" is a who-where pair you can act on today. If you do not know where to find your customers, keep slicing your segment into smaller pieces until you do.

Format each pair as:

```
WHO: [specific demographic + motivation]
WHERE: [concrete location, community, channel, or behavior-based finding method]
```

Generate 3-5 who-where pairs from the slicing analysis. Include both demographic-based locations and behavior-based locations where possible.

### Step 5: Check for Wrong-Audience Traps

**ACTION:** Review the who-where pairs for three common targeting failures before scoring.

**WHY:** Even with good slicing, founders can still talk to the wrong people. Catching these traps before you invest in conversations prevents wasted effort and misleading data.

Check for:

1. **Too-broad segment surviving** — Did any who-where pair remain vaguely defined? Test: "If I talked to 5 random people from this group, would they have the same core problem and goal?" If not, slice further.
2. **Missing customer segments** — Does the product involve multiple sides (marketplace, platform) or require buy-in from someone other than the end user? If you are building an app for children, you must also understand parents. If you are building for public schools, you could be affected by teachers, students, administration, parent-teacher associations, and taxpayers. List ALL segments that need validation.
3. **Overlooked stakeholders in complex buying** — In B2B or institutional sales, the user is rarely the buyer. Identify manufacturing partners, distribution partners, IT decision-makers, procurement, or other influencers who could block the sale. Also consider: are you talking to representative customers, or just impressive-sounding ones? Talking to senior executives when your actual user is a frontline worker will give you misleading data.

### Step 6: Score and Select the Starting Segment

**ACTION:** Evaluate each who-where pair against three selection criteria and recommend where to start.

**WHY:** You cannot pursue all segments simultaneously — that is how you end up drowning again. Choosing one starting segment lets you run focused conversations where learnings compound. You can always broaden later. The goal is to quickly get to a specific, best-possible customer so you can grab a few conversations and start making real progress.

Score each who-where pair on three criteria:

| Criteria | Question to Answer | Scoring Guidance |
|----------|-------------------|------------------|
| **Profitable** | Can this group pay? Is the problem painful enough that they would spend money to solve it? | HIGH = already spending money on workarounds. MEDIUM = have budget, problem is real but not urgent. LOW = no budget or problem is a nice-to-have. |
| **Reachable** | Can you actually get to these people within the next 2 weeks? | HIGH = you know exactly where to find them and can reach 5+ this week. MEDIUM = you can find them but it requires effort or introductions. LOW = you have no clear path to reaching them. |
| **Rewarding** | Would you enjoy building a business around these people? | HIGH = you find this group interesting and would enjoy spending years in their world. MEDIUM = neutral. LOW = you would dread working with them daily. |

**WHY these three criteria matter:**
- **Profitable** ensures you are not building for people who will never pay
- **Reachable** ensures you can actually run conversations (a perfect segment you cannot reach is useless)
- **Rewarding** ensures sustainability — customer discovery is hard work and can be a real grind if you are cynical about the people or the industry you are trying to understand and serve

**RECOMMEND** the who-where pair with the strongest combination across all three criteria. If there is a tie, favor reachability — you need conversations before you can learn anything else.

### Step 7: Produce the Segment Analysis Document

**ACTION:** Write the complete analysis to a file the user can reference and update.

**WHY:** This document becomes the foundation for all subsequent customer discovery activities — it determines who to talk to, where to find them, and what to learn. It should be a living document that gets updated as conversations reveal new information.

Write the output file with this structure:

```markdown
# Customer Segment Analysis: {Product/Idea Name}

## Product Hypothesis
{Brief description of the product idea and the problem it solves}

## Initial Segment (Before Slicing)
{The user's original broad customer definition}

## Too-Broad Diagnosis
{Which symptoms were present and evidence for each}

## Slicing Results

### Sub-Groups Identified
{Numbered list of specific demographic sub-groups discovered through slicing}

### Motivations Identified
{Numbered list of distinct motivations/problems/goals surfaced}

### Behaviors and Workarounds
{For each sub-group: what they currently do to solve the problem}

## Who-Where Pairs

### Pair 1: {Name}
- **WHO:** {specific demographic + motivation}
- **WHERE:** {concrete finding location}
- **Workaround behavior:** {what they currently do}
- **Profitable:** {HIGH/MEDIUM/LOW} — {reasoning}
- **Reachable:** {HIGH/MEDIUM/LOW} — {reasoning}
- **Rewarding:** {HIGH/MEDIUM/LOW} — {reasoning}

### Pair 2: {Name}
{Same format}

### Pair 3: {Name}
{Same format}

## Wrong-Audience Check
- [ ] No surviving too-broad segments
- [ ] All customer sides identified (if multi-sided)
- [ ] All stakeholders in buying process identified (if B2B/institutional)
- [ ] Talking to representative customers, not just impressive ones

## Recommended Starting Segment
**{Who-where pair name}** — chosen because {justification referencing the three criteria}

## Next Steps
1. Find 3-5 people from this segment within the next {timeframe}
2. Prepare 3 learning goals for initial conversations (see `conversation-sourcing-planner` for finding approaches, `question-importance-prioritizer` for choosing what to learn)
3. After 3-5 conversations, check: are problems and goals consistent? If yes, continue. If mixed, slice further.

## Revision Log
| Date | Change | Trigger |
|------|--------|---------|
| {today} | Initial analysis | First segmentation exercise |
```

Save to `customer-segments.md` in the user's working directory (or the path they specify).

## Examples

### Example 1: Powdered Superfood Condiment

**Scenario:** A founder has developed an all-natural powdered condiment — sweet like cinnamon brown sugar but packed with multivitamin nutrition. She says "it has countless uses" and her customer segment is "health-conscious people."

**Trigger:** The founder cannot make progress because bodybuilders want it for protein shakes, restaurants want it as a healthy sugar alternative on tables, and moms want to trick kids into eating healthy. Every group wants different things. She does not know where to start.

**Process:**
1. Diagnosed too-broad: all three symptoms present (overwhelmed by conflicting needs, cannot prove any direction right or wrong, each group wants different packaging/marketing/pricing)
2. Slicing questions surfaced three sub-groups with distinct motivations: bodybuilders (performance nutrition), restaurant owners (menu differentiation), moms (stealth nutrition for children)
3. Behavior mapping: moms already shop at health food stores, already buy organic alternatives, already read nutrition labels. Bodybuilders already buy supplements online. Restaurant owners already source specialty ingredients from distributors.
4. Who-where pairs: (a) Moms at independent health food stores, (b) Bodybuilders in supplement forums, (c) Restaurant owners via food distributor reps
5. Scoring: Moms at health food stores scored highest — profitable (already spending on healthy alternatives), reachable (the stores ARE the finding location AND a distribution partner), rewarding (founder is a mom herself)

**Output:** Recommended starting with moms at independent health food stores. The stores serve double duty — they are where you find the customers AND a potential distribution channel. Proposed commitment test: ask store owners to place a few bottles beside breakfast foods, return in one week to check results. This cuts through opinions by asking for a concrete commitment (shelf space) rather than collecting compliments.

### Example 2: Public Speaking Practice App

**Scenario:** A team has built a product for "students who want to become more confident speakers." After 20 conversations, they have 20 different must-have features and cannot figure out what to build first.

**Trigger:** Feedback is absurdly inconsistent. One user wants formal citations, another wants practice questions, a third needs iPad support, a fourth needs 80 students on one computer, another needs offline mode. The team's soul feels like it is being forced through a colander.

**Process:**
1. Diagnosed too-broad: primary symptom is mixed signals. "Students" hides at least five completely different customer types — PhD researchers, prep school teens, homeschooling parents, children in Indian rural villages sharing one computer, African students on cellphones. The team was having one conversation each with 20 different types of customers, not 20 conversations with their customers.
2. Slicing on motivation: "nervous about a specific upcoming high-stakes event" vs "want to improve speaking as a long-term skill" vs "need to fix language/accent issues." The first motivation is the most urgent — people with a specific event have a deadline and high emotional stakes.
3. Further slicing within "nervous about upcoming event": graduating students (first job interview), first-time TV/radio guests, wedding speakers, new authors on book tour, non-native-speaking PhD students with a conference talk.
4. Behavior mapping: people scared of speaking who are actively trying to improve — they Google for tips, attend workshops, go to Toastmasters meetups, listen to speaking podcasts. Those who just feel anxious and avoid it are NOT the customer (no active solution-seeking behavior).
5. Who-where pairs: (a) Non-native PhD students at university admissions offices and department advisors, (b) Nervous wedding speakers Googling "great wedding speech examples," (c) New authors on book tour found via Amazon upcoming release lists, (d) Active Toastmasters members at local meetups
6. Scoring: Toastmasters members scored highest on reachability (can attend a meetup this week and have a dozen conversations in one evening). PhD students scored highest on profitability (institutional budgets, high stakes). Team chose Toastmasters as starting point for accessibility — a single evening could yield enough conversations to validate the core problem.

**Output:** Recommended shifting segment from "students" to "people scared of public speaking who are actively trying to get better." Starting point: attend a Toastmasters meetup. One evening provides understanding of motivations, worldview, and needs of a large group of ideal customers who are already spending time and money to improve.

### Example 3: B2B Advertising Platform

**Scenario:** A founder's customer segment is "advertisers." He has talked to mom-and-pop shops, e-tailers, big brands, creative agencies, SMEs, and music labels. Everything sort of works. Some talk about paying $10,000 per month, others scoff at $10.

**Trigger:** The team cannot cut any features because every feature is someone's favorite. Every debate over a new feature can be won by claiming "well, those guys would love it." The reverse argument prevents removing any feature. They can prove themselves neither right nor wrong.

**Process:**
1. Diagnosed too-broad: classic unfalsifiability symptom — making a so-so product for a bunch of audiences instead of an incredible product for one
2. Slicing revealed that "advertisers" contains sub-groups with fundamentally different budgets ($10 vs $10,000/month), different needs (self-serve vs managed), different constraints (brand safety vs scrappiness), and different goals (awareness vs direct response)
3. Reviewed existing conversation data for signal strength: noticed unusually strong enthusiasm from creative agencies who wanted to be edgy — they leaned forward, asked detailed follow-up questions, and offered to connect the team with other agencies
4. Who-where pairs: (a) Creative agencies at advertising industry meetups, (b) E-commerce stores in Shopify app marketplace, (c) SMEs through local business associations
5. Scoring: Creative agencies scored highest — profitable (agency budgets), reachable (clustered in industry events and online communities), rewarding (the team found their energy exciting)

**Output:** Recommended narrowing from "advertisers" to "creative agencies who want to be edgy." Cut features that only served other segment types. Finally able to get clear signal on what worked and what did not, because all feedback came from a consistent customer type.

## Key Principles

- **Good customer segments are a who-where pair** — A segment definition is incomplete until you can name both WHO the customer is AND WHERE to find them. If you cannot answer "where would I go this week to find 5 of these people?", keep slicing into smaller pieces until you can. A customer segment you cannot find is a customer segment you cannot learn from.

- **Before you can serve everyone, you have to serve someone** — Google started with PhD students finding obscure code. eBay started with Pez dispenser collectors. Evernote started with moms saving recipes. These companies serve the whole world now, but they did not start there. Starting broad waters down everything — your marketing, your features, your conversations. Get specific first, then broaden from a position of strength.

- **Inconsistent feedback is a segmentation problem, not a product problem** — When 20 conversations yield 20 different must-have features, the instinct is to think the product is wrong. Usually, the segment is wrong. You are not having 20 conversations with your customers — you are having one conversation each with 20 different types of customers. Slice the segment until feedback converges.

- **Behaviors reveal more than demographics** — Demographics tell you who someone is on paper. Behaviors tell you how serious they are about the problem. Someone who is already spending time and money on workarounds (attending workshops, buying tools, cobbling together spreadsheets) is a vastly stronger prospect than someone who merely fits the demographic profile but ignores the problem. Target behaviors, then trace back to demographics.

- **Choose your starting segment, not your forever segment** — Picking a segment to start with is not a permanent commitment. It is the fastest way to stop drowning and start learning. You can always broaden later once you have validated the core problem and built momentum. The three criteria (profitable, reachable, rewarding) optimize for learning speed and founder sustainability, not total addressable market.

## References

- **Cross-skill dependencies:** After slicing produces a starting segment, use `conversation-sourcing-planner` to find conversations with that segment, and `question-importance-prioritizer` to decide what to learn from them.
- **Segment validation signal:** If after 3-5 focused conversations you are still getting inconsistent problems and goals, your segment is not specific enough yet — return to this skill and slice further. If feedback converges within 3-5 conversations, your segment is well-defined.
- **Slicing questions quick reference:** See [references/slicing-questions.md](references/slicing-questions.md) for the complete question set formatted as a standalone reference card.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Mom Test by Rob Fitzpatrick.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
