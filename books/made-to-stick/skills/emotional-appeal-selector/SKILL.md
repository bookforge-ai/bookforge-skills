---
name: emotional-appeal-selector
description: Choose the emotional lever that will make an audience actually care about a message — and strip out the analytical priming that kills charity before the emotional ask lands. Use this skill whenever a message is technically correct but emotionally flat, whenever the user asks "how do I make them care", "nobody cares about this", "why won't people act", "why should they care", "make this emotional without being cheesy", "motivate people", "this fundraising email isn't working", "rewrite this pitch so it lands", "our cause is important but donations are dropping", or "this announcement is dry and people are ignoring it". Also triggers when the user has a spreadsheet-heavy pitch, a statistics-first fundraising appeal, a recruiting message that lists benefits nobody responds to, a behavior-change campaign that's being ignored, a change-management memo that reads like a policy document, or a mission statement that employees cannot see themselves inside. Applies three named levers from Made to Stick — Association (tap emotions they already have), Self-Interest (what's in it for you, stated plainly), and Identity (who am I and what do people like me do) — plus the Mother Teresa / identifiable-victim rule (one specific person beats aggregate statistics) plus Maslow's eight needs used as a non-hierarchical palette (warning against "Maslow's basement" — assuming others are motivated only by money and security). Critically detects and removes analytical priming — calculations, spreadsheets, statistics placed before an emotional ask — because the mere act of calculation has been shown to reduce charitable response. This skill does NOT manipulate via fear, exploit vulnerability, or produce sympathy-begging copy. It does NOT write the full message end-to-end (pair with a rewriting skill); it produces an emotional-appeal plan — chosen lever, framing, concrete moves, and forbidden moves — that a writer or another skill can execute.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/emotional-appeal-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [5, 13]
tags: [emotional-appeal, persuasion, messaging, motivation, fundraising, change-management, identity, storytelling, copywriting, communication]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Core message or current draft — the one thing you want the audience to feel, believe, or do"
    - type: document
      description: "Audience profile — who they are, what group they belong to, what they currently care about"
    - type: document
      description: "Type of action sought — donate, join, change behavior, approve a budget, vote, rally around a mission"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set working environment: the agent operates on short-form prose drafts, briefs, and audience notes provided by the user."
discovery:
  goal: "Select the emotional lever most likely to make a specific audience care about a specific ask, and produce a plan the writer can execute without slipping into manipulation or analytical flattening."
  tasks:
    - "Decide between Association, Self-Interest, and Identity as the primary emotional lever for a message"
    - "Detect and remove analytical priming (stats, calculations, spreadsheets) that precedes an emotional ask"
    - "Convert aggregate statistics into an identifiable-individual frame for fundraising or advocacy"
    - "Diagnose whether a motivational appeal is stuck in Maslow's basement and recommend an upper-level reframe"
    - "Produce a forbidden-moves list for a sensitive appeal to prevent manipulation or cheesiness"
  audience:
    roles: [marketer, fundraiser, founder, communicator, manager, change-leader, nonprofit-leader, product-marketer, teacher]
    experience: any
  when_to_use:
    triggers:
      - "Message is technically correct but the audience is not responding"
      - "Fundraising appeal leads with aggregate statistics"
      - "Recruiting or internal memo lists benefits that nobody is acting on"
      - "User explicitly asks how to make an audience care without being manipulative"
      - "Change-management or mission pitch is being ignored or mocked"
    prerequisites: []
    not_for:
      - "Writing the full rewritten message end-to-end — hand off to a rewriting skill after producing the plan"
      - "Running the full six-principle stickiness audit — use a stickiness-audit skill instead"
      - "Producing fear-based, shame-based, or exploitation-based copy — this skill refuses those paths"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
---

# Emotional Appeal Selector

## When to Use

You have a message, pitch, fundraising appeal, recruiting note, change-management memo, or mission statement that is **technically accurate but emotionally inert**. The audience is not moved. The message may be loaded with statistics, benefits, or strategy language, yet the needle on donations, sign-ups, adoption, or morale is not moving. Use this skill to **choose the single emotional lever that will make them care**, diagnose analytical priming that is suppressing charity, and produce a plan that a writer (or a follow-on rewriting skill) can execute.

**This is a plan-only skill.** It outputs a structured decision and brief, not finished copy. The writer still writes.

**Preconditions to verify before starting:**
- There is a clear **core message** (one sentence) — if not, pair with `core-message-extractor` first.
- There is a clear **audience** — who are they, what group do they belong to, what do they already care about?
- There is a clear **action sought** — donate, join, switch behavior, approve, rally. "Raising awareness" is not an action.
- The user wants a recommendation, not a rewrite.

**Do NOT use this skill to:**
- Produce fear-, shame-, or guilt-based manipulation. The skill will refuse and suggest an identity or transcendence reframe instead.
- Replace an honest value proposition with emotional theatre. If the underlying offer is bad, this skill cannot fix it.
- Run the whole SUCCESs audit — emotional is one principle of six.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Core message:** One sentence — the single thing you want the audience to feel, believe, or do.
  -> Check prompt for: a stated ask, a pitch draft, a campaign goal
  -> If missing, ask: "What is the one-sentence message you want to land? (If you don't have one, we should extract it first.)"
- **Audience identity:** Who they are, what group(s) they identify with, what they already care about.
  -> Check prompt for: named audience, segment descriptions, personas
  -> If missing, ask: "Who are you trying to reach? Describe them as a group — not demographics, but shared identity or situation (e.g., 'firefighters in a small-town department' or 'parents of teen soccer players')."
- **Action sought:** The specific behavior you want.
  -> Check prompt for: verbs like donate, subscribe, apply, approve, sign, vote, quit, switch
  -> If missing, ask: "What specific action do you want them to take after reading this?"

### Observable Context (gather from environment)

- **Existing draft:** If a draft exists, read it and scan for analytical priming (numbers, percentages, spreadsheets, ROI language) that appears BEFORE the emotional ask.
  -> Look for: `draft.md`, `brief.md`, pasted copy in the prompt
  -> If unavailable: proceed with the core message + audience only
- **Prior attempts:** Has the user tried a version that failed? Why did they think it failed?
  -> Look for: `previous-version.md`, user's own diagnosis in the prompt
  -> If unavailable: assume no prior signal

### Default Assumptions

- **Tone:** Default to sincere, non-cheesy, non-manipulative. State explicitly in the output brief.
- **Channel:** Default to the channel implied by the draft (email, landing page, speech, memo). If unknown, default to short-form written.
- **Length constraint:** If not stated, assume the writer wants compact — 100-300 words.

### Sufficiency Threshold

- **SUFFICIENT:** Core message + audience identity + action sought are all known.
- **PROCEED WITH DEFAULTS:** Core message + audience known, action sought inferable from context (e.g., fundraising email -> donate).
- **MUST ASK:** Audience is described only demographically ("millennials") with no identity or group context — the three levers need shared-situation context to work.

## Process

### Step 0: Initialize Task Tracking

**ACTION:** Write a lightweight checklist (can be inline markdown) for the steps below: priming scan, lever selection, identifiable-victim check, Maslow check, forbidden-moves list, plan output.

**WHY:** The skill has several independent checks that can be skipped silently if not tracked. Writing the checklist first forces you to run the analytical-priming scan even when the draft "looks fine" — and that scan is the single highest-value step because analytical priming invisibly neutralizes every other move you make.

### Step 1: Scan for Analytical Priming (Before Anything Else)

**ACTION:** Read the existing draft (if any) top to bottom and flag every element that would **prime the reader to think analytically before the emotional ask**. Produce a short list: location + element + why it primes calculation.

Look for:
- Aggregate statistics ("3 million children face hunger", "72% of respondents")
- Dollar figures, percentages, or ROI computations before the ask
- Tables, spreadsheets, comparison charts, "by the numbers" sidebars
- "Let's do the math" / "calculate your savings" / cost-benefit framings
- Dense credentials walls ("PhD, 20 years experience, Harvard-trained")
- Multiple options presented with trade-offs (decision paralysis = analytical mode)
- Forms with required numeric inputs placed before the story

**WHY:** The Rokia / Save the Children experiment showed donors gave **$2.38** after reading about one named girl, but only **$1.14** after reading statistics about millions of hungry children. Worse — people who read BOTH the story AND the statistics gave only **$1.43**, almost a dollar LESS than those who got the story alone. A second study primed half the participants with a calculation problem ("If an object travels at 5 ft/min, how many feet in 360 seconds?") before the Rokia letter. The primed group gave $1.26; the unprimed group gave $2.34. **The mere act of calculation cut charity almost in half.** If you leave analytical priming in front of the emotional ask, the emotional ask cannot do its job. This step is non-negotiable — skip it and the rest of the plan is neutralized.

**IF** analytical priming is found before the emotional ask -> mark every instance with a [REMOVE-OR-MOVE-AFTER-ASK] tag in the plan.
**ELSE** -> note "no analytical priming detected" explicitly in the plan. Absence is a finding, not silence.

### Step 2: Profile the Audience's Current Emotional Tags

**ACTION:** Write a short "what they already care about" note for the audience. What emotions, values, group memberships, and aspirations are ALREADY active in their life — without you putting them there?

Answer four questions:
1. What group(s) do they identify with? (role, profession, region, fandom, cause, family structure)
2. What do they brag about? (what would they post on social media proudly?)
3. What do they resent or mock? (what group do they define themselves against?)
4. What upper-level Maslow need is currently most under-served in their environment? (see `references/maslow-eight-levels.md`)

**WHY:** The book's strongest move in the Emotional chapter is that you usually do not need to **create** emotion — you piggyback on emotion the audience is already feeling. The "Association" lever only works if you know which existing emotional tags to connect to. Skipping this step forces you to manufacture emotion, which is where cheesiness and manipulation come from. The fourth question specifically guards against Maslow's basement: you will default to Security/Esteem appeals unless you explicitly ask what upper need is under-served.

### Step 3: Choose the Primary Lever

**ACTION:** Pick ONE of the three levers as primary. You can add a secondary, but lead with one. Use the decision rules below; they are ordered by priority — use the first one that applies.

**Lever 1 — IDENTITY** ("Who am I? What do people like me do?")
- **Use when:** The audience has a strong shared identity (profession, region, fandom, cause, demographic group), and the action you want is something they would do *because of who they are*, not because of what they get.
- **Decision test:** Can you finish the sentence "A real ___ would ___"? If yes, Identity is your lever.
- **Canonical example:** "Don't Mess With Texas" worked on a littering problem where a self-interest appeal ("fines", "environmental damage") had failed — because the target ("Bubba", a pickup-driving Texan) responded to *identity-as-Texan* much more strongly than to incentives. The appeal's message: *real Texans do not litter.*
- **Counter-example:** The firehouse popcorn-popper incident — an educational film for firefighters was being pitched to chiefs with a free popcorn popper as incentive. One chief exploded: *"You think we need a #*$@! popcorn popper to run a fire-safety program?"* The free-gift appeal insulted the firefighters' identity (we are professionals, not consumers). Any incentive-based move was going to fail; only an identity-appeal could work.

**Lever 2 — SELF-INTEREST** ("WIIFY — What's in it for you")
- **Use when:** The benefit is concrete, personal, and the audience does not have a conflicting identity that makes incentives feel insulting.
- **Decision test:** Can you name a specific, tangible, personal outcome — and is the audience the kind of person who can say "yes, I want that" without feeling embarrassed?
- **Canonical moves:**
  - Say "you", not "people". *"You enjoy a sense of security when you use Goodyear tires"* — not *"people will enjoy a sense of security..."*.
  - **Help them visualize the benefit already happening.** The Tempe cable TV study found that a subtle "imagine coming home and finding your show on cable" pitch outperformed an abstract benefits list. Visualization > enumeration.
  - **Do not bury the self-interest.** Caples: *"First and foremost, try to get self-interest into every headline you write."*
- **Counter-test (Maslow's basement check):** If your self-interest appeal is purely Security/Esteem/Physical (money, bonus, comfort), stop. Re-read `references/maslow-eight-levels.md` and ask whether you could rewrite the appeal from Learning, Aesthetic, Self-actualization, or Transcendence. *"Math is mental weight training"* beats *"you'll need it for your job"* because it moves up out of the basement.

**Lever 3 — ASSOCIATION** ("Tap emotions they already have")
- **Use when:** The audience has strong existing feelings about some adjacent concept, and you can hook your idea onto that concept without semantic stretch.
- **Decision test:** Is there a word, image, or idea they already respond to emotionally that your message is genuinely (not coincidentally) connected to?
- **Canonical example:** Positive Coaching Alliance could not use "sportsmanship" — the word had been stretched thin by overuse. Jim Thompson reframed the concept as **"Honoring the Game"**, a phrase that had not been worn out, and coaches, parents, and kids immediately understood the ask. Same underlying concept, fresh association.
- **Warning — semantic stretch:** Any word that has been overused until it means nothing (unique, passionate, innovative, empowered, next-generation) has lost its emotional voltage. Do not associate your message with words in the stretched zone; either find a fresh word (Honoring the Game) or pick a different lever entirely.

**WHY the ordering matters:** Identity-based appeals are the most under-used and the most motivating when they fit — they recruit the audience's sense of self as an unpaid copywriter on your behalf. Self-interest is the default most people reach for; test whether identity would beat it before committing. Association is the most creative lever and the easiest to get wrong via semantic stretch, so it goes last.

**IF** two levers tie -> run the stronger one as primary and add the second as a supporting line at the end.
**ELSE** -> lock the primary lever and proceed.

### Step 4: Apply the Mother Teresa / Identifiable-Victim Rule

**ACTION:** If the message involves suffering, harm, need, or any collective beneficiary group, convert the collective to **one named individual with concrete details**. Discard aggregate statistics from the emotional section of the message entirely.

**WHY:** Mother Teresa: *"If I look at the mass, I will never act. If I look at the one, I will."* The Rokia study proved the effect is not metaphor — $2.38 vs $1.14 for the same underlying cause, differing only in whether the reader saw one child or a statistic. The theory: individuals produce empathy; masses produce the "drop in the bucket" feeling of futility, which collapses motivation. Worse, combining both modes *lowered* giving below the individual-only version because statistics drag the reader into analytical mode (Step 1's concern, but reinforced here).

**Implementation:**
- Pick ONE real or representative individual the message is ultimately about.
- Give them a name, an age, a place, and one concrete sensory detail (Rokia: *seven years old, from Mali, loves to play soccer, gets annoyed by her little brother*).
- If you have statistics you cannot bear to remove, move them to a **post-ask** context section (e.g., "About this cause" footer), never before the ask.

**IF** the ask has no beneficiary (e.g., a recruiting message for a job, a behavior change with no specific victim) -> skip this step and note "not applicable: no beneficiary frame".
**ELSE** -> produce the one-named-individual frame.

### Step 5: Maslow's Basement Check

**ACTION:** Read the draft (or your working plan) and categorize which of the eight Maslow needs each motivational appeal is targeting. Then ask: "Am I stuck in the basement?"

The eight needs, as a palette not a ladder: Transcendence, Self-actualization, Aesthetic, Learning, Esteem, Belonging, Security, Physical. (See `references/maslow-eight-levels.md` for definitions and the company-bonus experiment that demonstrates the bias.)

**WHY:** Most message designers unconsciously assume the audience is motivated only by Security, Esteem, and Physical needs while themselves pursuing Transcendence and Self-actualization. This projection-in-reverse is Maslow's basement. The Pegasus dining hall in Baghdad is the book's best counter-example: Army cook Floyd Lee ran a mess hall on identical rations and identical Army recipes as every other mess hall, but reframed his mission as *"I am not in charge of food service, I am in charge of morale"* — appealing to Transcendence, Aesthetic, and Learning needs in his staff. Soldiers drove through IED zones for his meals. The same appeal pitched as "we need to hit our meal-service KPI" would have produced nothing. If you are stuck in the basement, the upper-level rewrite is almost always available — you just have to look for it.

**Decision:** If every motivational line in the draft targets only Security/Esteem/Physical, rewrite at least ONE line to target an upper level (Transcendence, Self-actualization, Aesthetic, or Learning). Prefer Transcendence if a shared mission exists; prefer Learning or Self-actualization for professional audiences.

### Step 6: Write the Forbidden-Moves List

**ACTION:** Produce an explicit list of moves the writer MUST NOT use in executing this plan. This is a guardrail against manipulation, cheesiness, and fear-based persuasion.

Include by default:
- No fear appeals that catastrophize beyond the honest stakes.
- No guilt or shame framing ("if you don't donate, you're responsible for…").
- No semantic-stretch words (list the specific stretched words to avoid for this audience).
- No stacking statistics before the ask.
- No cost-benefit tables before the ask.
- No dense credentials walls before the emotional hook.
- No self-interest appeal that would insult the audience's identity (popcorn-popper trap).
- No invented or fictional individual presented as real (use "representative" or "composite" labels if using a constructed person).

**WHY:** The Emotional chapter's main warning is that emotional levers are powerful enough to be abused — and that abuse is what makes audiences defensive and mocking of sincere appeals. Writing the forbidden list before the writer starts forces the writer to stay inside the honest envelope. Skipping this step is how plan-only skills end up producing slick copy that reads as manipulative.

### Step 7: Output the Emotional Appeal Plan

**ACTION:** Write `emotional-appeal-plan.md` with the structure below. Do NOT write the finished copy — that is the writer's job (or a follow-on rewriting skill's job).

```markdown
# Emotional Appeal Plan: {message title}

## Core message
{one-sentence ask, carried from input}

## Audience identity profile
- Group: {who they identify as}
- What they already care about: {list}
- Under-served upper-level need: {Transcendence / Self-actualization / Aesthetic / Learning}

## Primary lever: {Identity | Self-Interest | Association}
**Why this lever:** {reasoning from Step 3 decision rules}
**How to frame it:** {2-3 sentences on the framing}
**Example opening line (for the writer to adapt):** {one line, illustrative only}

## Secondary lever (optional): {lever | none}
**How it supports:** {one sentence}

## Identifiable individual frame
{one named person with concrete details, OR "not applicable: no beneficiary frame"}

## Analytical priming to remove
- {item}: {location in draft} -> move to post-ask section or delete
- {item}: {location in draft} -> ...
OR: "No analytical priming detected."

## Maslow level(s) being targeted
{list of levels, with a note if any upper-level rewrites were applied}

## Forbidden moves
- {specific move to avoid}
- {specific stretched word to avoid}
- ...

## Rationale notes for the writer
{1-2 paragraphs explaining the core strategic choice so the writer can adapt under pressure}
```

**WHY:** The plan is the handoff artifact. A writer (human or agent) executing this plan can produce compliant copy without re-running the analysis. Without the structured output, the recommendation lives in chat and gets lost as soon as the draft needs a revision.

## Inputs

- **Core message:** one-sentence ask
- **Audience profile:** group identity, what they currently care about
- **Action sought:** specific verb — donate, join, switch, approve, rally
- **Optional — existing draft:** for analytical-priming scan and before/after comparison

## Outputs

- **`emotional-appeal-plan.md`** — structured plan (template above) covering lever choice, framing, identifiable-individual frame, analytical priming to remove, Maslow targeting, and forbidden moves. This is a plan, not finished copy.

## Key Principles

- **The mere act of calculation reduces charity.** — This is the most counter-intuitive and the most enforced rule in this skill. Do not put numbers in front of an emotional ask. WHY: Measured in a controlled experiment, analytical priming cut donations nearly in half; the reader's cognitive mode shifts from empathy to evaluation, and evaluation is fatal to charity.
- **One identifiable person beats the aggregate, always.** — WHY: Empathy is a mechanism tuned to individuals. Collective suffering produces the "drop in the bucket" feeling and collapses agency; a single named person produces the felt responsibility that drives action.
- **Identity > self-interest > association, as a default ordering.** — WHY: Identity appeals recruit the audience's self-concept as an unpaid advocate; self-interest is the workhorse default; association is powerful but fragile because stretched words kill it. When in doubt, test identity first.
- **Get out of Maslow's basement.** — WHY: Message designers systematically project a Security/Esteem motivation onto audiences that would respond more strongly to Transcendence, Learning, or Self-actualization. The upper-level rewrite is almost always available; you just have to look for it.
- **Do not manufacture emotion — piggyback on emotion already present.** — WHY: Manufactured emotion is where cheesiness and manipulation come from. Finding what the audience already feels and hooking your message onto that existing feeling is honest, sustainable, and cannot be detected as a trick.
- **Semantic stretch is real and silent.** — WHY: Words like "unique", "passionate", "innovative", "sportsmanship" have been overused until they produce no emotional response at all. The audience does not tell you the word is dead — they just stop reacting. Find a fresh synonym (Honoring the Game) or change levers.
- **Plan-only discipline prevents slick manipulation.** — WHY: If this skill wrote the finished copy, it would be tempted to optimize for punch instead of honesty. Producing a plan + forbidden-moves list forces the writer to execute inside an honest envelope.

## Examples

**Scenario: fundraising email full of statistics**
Trigger: User shares `draft.md` — a wildfire relief email that opens with *"Over 12,000 families have lost their homes in the past 30 days. Donations are down 40% year-over-year. For every $100 we raise, 15 families receive emergency shelter."* The user says: "Donations are flat. Help."
Process: (1) Analytical-priming scan flags three items (12K families, 40% YoY, $100 -> 15 families) all before the ask — [REMOVE-OR-MOVE-AFTER-ASK]. (2) Audience profile: general donors who recently saw wildfire news, already feel concerned but overwhelmed; under-served need is Transcendence (feeling they matter). (3) Primary lever = Association (tap the concern they already feel) + identifiable-individual frame. (4) Identifiable individual: "Marta, 47, a nurse from Paradise, CA, walked out of her home on Thursday with her seven-year-old's asthma inhaler and nothing else." (5) Maslow targeting: Transcendence (you can be the person who made the difference in Marta's week). (6) Forbidden moves: no statistics before ask, no catastrophizing the fire, no "if you don't donate" guilt, no stretched word "devastating". (7) Plan written.
Output: `emotional-appeal-plan.md` recommending an Association-led rewrite opening with Marta, statistics moved to a post-ask "About the crisis" footer, Transcendence framing for the donation, forbidden-moves list appended. Writer (or rewriting skill) executes.

**Scenario: recruiting memo to firefighters ignored**
Trigger: User shares a recruiting memo for a volunteer fire-safety training program. The pitch leads with "free training materials, a $50 gift card per participant, and certificates". Chiefs are ignoring it.
Process: (1) No statistics to flag, but the incentives-first framing is itself an analytical move (cost-benefit calculation). (2) Audience profile: firefighters — strong professional identity, define themselves AGAINST being consumers who need gifts. The popcorn-popper trap is live. (3) Primary lever = Identity. "A real fire chief runs a department where every rookie has had the latest burn-pattern training by week 4." (4) No beneficiary frame needed (not a charitable appeal). (5) Maslow: reframe from Esteem/Security basement to Self-actualization (mastery) and Transcendence (protecting the community). (6) Forbidden moves: do not offer the gift card in the lead, do not lead with "free" anything, do not use "participants" (frames them as consumers), do not use "incentive". (7) Plan written.
Output: `emotional-appeal-plan.md` recommending identity-led reframe ("A real fire chief…"), gift card moved to a practical footer or removed entirely, forbidden-moves list emphasizing the popcorn-popper trap.

**Scenario: change-management memo about a new internal tool**
Trigger: User shares a rollout memo for a new internal reporting tool. Current draft: *"The new dashboard consolidates 7 data sources and saves an estimated 4.2 hours per week per analyst. ROI projected at $480K annually."*
Process: (1) Analytical priming everywhere — every sentence is numbers. (2) Audience profile: analysts, professional identity as craftspeople of insight; under-served upper need is Self-actualization (doing work they're proud of). (3) Primary lever = Self-Interest at the Self-actualization level (not Esteem level) — "spend your hours on the analysis you actually want to do, not the hours you spend hunting for the data". (4) No identifiable individual (not a beneficiary situation). (5) Maslow: explicitly rewritten from Esteem/Security basement ("save time", "ROI") to Self-actualization ("spend your hours on the work you came here for"). (6) Forbidden moves: no $ figures, no % figures, no hour-counting before the ask; no generic "productivity" language (stretched); no "empowered" or "streamlined" (stretched). (7) Plan written.
Output: `emotional-appeal-plan.md` recommending a Self-interest (upper-level) lead, all ROI numbers moved to an appendix, forbidden-moves list flagging the stretched words, Self-actualization reframing noted as the primary strategic move.

## References

- For Maslow's eight needs as a non-hierarchical palette and the Maslow's-basement experiment, see [maslow-eight-levels.md](references/maslow-eight-levels.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Made to Stick: Why Some Ideas Survive and Others Die by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
