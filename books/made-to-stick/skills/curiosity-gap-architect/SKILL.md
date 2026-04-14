---
name: curiosity-gap-architect
description: "Build an Unexpected hook for a message, pitch, essay, ad, talk, or email — first break the audience's expected pattern to CAPTURE attention, then open a curiosity gap (a knowledge gap they didn't know existed) to HOLD attention all the way to the core message. Use this skill whenever the user says 'how do I hook them', 'what's my opening line', 'I need to get attention', 'this is boring how do I make it interesting', 'what's my angle', 'stop losing the audience', 'hook for my post', 'cold-open', 'lead paragraph', 'ad headline', 'landing page hero', 'intro for my talk', 'title that makes people click', 'my opening is flat', 'people tune out in the first 10 seconds', 'how do I make this dry topic interesting', 'email subject line', 'tweet hook', 'YouTube intro', 'TED-style opener', 'how Nora Ephron taught leads', 'Cialdini mystery opening', 'how to use surprise without being gimmicky'. Applies the two Unexpected mechanisms from Made to Stick Chapter 2: (1) SURPRISE via schema-break for short-term attention capture, (2) CURIOSITY GAP via Gap Theory of Curiosity (Loewenstein) for long-term attention hold. Every surprise option is scored against the POST-DICTABLE TEST — a good surprise feels inevitable in hindsight and drives home the core message; a gimmicky surprise gets a laugh but the audience can't remember the point. Produces 3 scored hook variants the user can drop into their draft. Does NOT rewrite the body of the message — only the hook and the gap structure. Does NOT manufacture shock or clickbait for its own sake. Relevant for: copywriters, marketers, product marketers, founders pitching, teachers, trainers, public speakers, content writers, journalists, fundraisers, PR, messaging, narrative design, persuasion, attention, Heath brothers, SUCCESs, Unexpected, Gap Theory, Loewenstein, schema break, postdictable, Ephron lead, Nordstrom Nordies, Cialdini Saturn rings, popcorn Silverman."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/curiosity-gap-architect
metadata: {"openclaw":{"emoji":"🪝","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [2, 7]
tags: [communication, messaging, copywriting, marketing, persuasion, attention, curiosity-gap, unexpected-principle, hook-writing, public-speaking, made-to-stick, success-framework]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "draft.md — the current version of the message, pitch, ad, post, or talk that needs a better hook"
    - type: document
      description: "core-message.md (optional) — the one-sentence thing that must survive if the audience remembers nothing else. If missing, the skill extracts a working core from the draft and asks the user to confirm it."
    - type: document
      description: "audience-beliefs.md (optional) — what the audience currently believes, expects, or takes for granted about the topic. Used to decide which schema to break. If missing, the skill asks 3 targeted questions."
  tools-required: [Read, Write]
  tools-optional: [TodoWrite, Grep]
  mcps-required: []
  environment: "Document set. Agent reads draft + optional brief, writes hook-options.md with 3 scored variants."
discovery:
  goal: "Produce 3 hook variants that break the audience's expected pattern and open a curiosity gap leading directly to the core message, each scored against the post-dictable test."
  tasks:
    - "Extract or confirm the core message the hook must deliver the audience to"
    - "Surface the audience's current schema — the pattern the hook will break"
    - "Draft 3 hook variants across 3 mechanisms (schema-break lead, mystery opener, news-teaser gap)"
    - "Score each variant against the post-dictable test: does the surprise land the core, or just make noise?"
    - "Output hook-options.md ranked with rationale, rejected variants, and drop-in placement notes"
  audience:
    roles: [marketer, copywriter, founder, product-marketer, content-writer, public-speaker, teacher, fundraiser]
    experience: beginner-to-intermediate
---

# Curiosity Gap Architect

Build the opening of a message that captures attention by breaking a pattern, then holds attention by opening a gap the audience needs to close — without falling into shock, clickbait, or gimmick.

## When to Use

Use this skill when:

- **You have a draft but the opening is flat.** The body is solid; the audience would love it — if they got past the first sentence. They don't.
- **Your topic is technically important but feels dry.** You have a statistic, a policy, a feature, a lesson, a cause — and every attempt to open with it sounds like homework.
- **You're competing with infinite scroll.** Email subject, tweet, YouTube intro, landing hero, ad headline, talk opener — anywhere the first 3 seconds decide whether the next 30 happen.
- **You need to HOLD attention across a longer piece.** Not just a one-shot surprise. An essay, a whitepaper, a 20-minute talk, a sales page. You need a gap the reader carries through to the end.
- **Someone tried to be surprising and it backfired.** The shock worked but the message didn't. The audience remembered the stunt, not the point. You need the post-dictable test.

Do NOT use this skill when:

- The draft has no core message yet (the hook has nothing to deliver the audience to). Use `core-message-extractor` or `simple-core-message-distiller` first, or extract a working core inside this skill and confirm it with the user.
- The goal is to rewrite the body of the message for clarity, concreteness, credibility, or emotion. Those belong to the other SUCCESs skills. This skill changes only the hook and the gap architecture that spans the piece.
- The medium forbids a hook entirely (legal disclosures, regulated compliance copy, SLAs). The Unexpected principle does not apply to contracts.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Draft:** Current version of the opening you want to rewrite (email, ad, post, talk script, lead paragraph, landing hero).
  - Look for: `draft.md`, `copy.md`, `post.md`, `hook.md`, pasted text in the prompt.
  - If missing: "Paste the current opening — just the first 1–5 sentences, plus one line of what comes after."

- **Core message:** The one thing the audience must walk away remembering. (Commander's Intent.)
  - Look for: `core-message.md`, `brief.md`, or a labeled line in the draft.
  - If missing: extract a candidate from the draft, show it to the user, and ask "Is this the thing you want to land? If not, correct it in one sentence."
  - WHY blocking: a hook without a destination is clickbait. The post-dictable test is impossible to apply without knowing what the surprise is supposed to make inevitable.

### Observable Context (gather, do not block on)

- **Audience beliefs / schema:** What does the audience currently assume about the topic? What's the default pattern the hook will break?
  - Look for: `audience-profile.md`, `audience-beliefs.md`, a section in `brief.md`.
  - If missing, ask up to 3 short questions:
    1. "Who is the audience in one line?"
    2. "If the audience had to finish the sentence '[topic] is usually ___,' what would they write?"
    3. "What would make them say 'huh, I didn't expect that'?"

- **Medium and length budget:** one-line subject? 280 char tweet? 90-second cold open? 3-paragraph lead?
  - Affects the mechanism choice (see Step 3).

- **Prior attempts that failed:** If the user has tried hooks before, what was rejected and why ("too gimmicky", "too slow", "off-brand")?
  - Look for: `rejected-hooks.md`, inline comments in the draft.
  - Use to avoid re-suggesting the same failure mode.

### Sufficiency Threshold

- **SUFFICIENT:** Draft opening + confirmed core message + at least one sentence on audience schema.
- **PROCEED WITH DEFAULTS:** Draft + core message, no explicit audience schema (infer from the draft, flag assumption in output).
- **MUST ASK:** No draft OR no recoverable core message.

## Process

### Step 0: Initialize Task Tracking

**ACTION:** Create a TodoWrite list with the 5 process steps below.
**WHY:** This skill's failure mode is skipping the post-dictable test and shipping a clever-but-empty hook. Tracking forces you to hit Step 4 before declaring the artifact ready.

### Step 1: Confirm the Core Message

**ACTION:** Find or extract the one sentence the hook must deliver the audience to. If you had to extract it, write it back to the user in the form `"Core message I'm building the hook for: <sentence>. Confirm or correct."` Wait for confirmation only if the extraction is ambiguous.

**Artifact:** One-sentence core message logged at the top of `hook-options.md`.

**WHY:** The Unexpected principle only works in service of a core. Heath brothers' rule: surprise must be *postdictable* — in hindsight it must feel like the inevitable setup for this specific core. If the core is vague, every hook will feel gimmicky because nothing can make it feel inevitable. Garbage core in, gimmick out.

### Step 2: Surface the Audience Schema

**ACTION:** Write down, in 1–3 bullets, the expectations the audience brings to this topic right before they hit the hook. Specifically:
- What category do they file this topic under?
- What's the standard opening for a message in this category?
- What's the predictable next sentence after the draft's current first line?

**Artifact:** `## Schema to break` section in `hook-options.md`.

**WHY:** You cannot break a pattern you have not named. The Enclave minivan ad (Ch2) works because the writer first identified the minivan-commercial schema (cup holders, sky-view roof, suburban dad) and then violated it at a sharp moment (T-bone collision). Without naming the schema, the "surprise" is just a random swerve — the audience has nothing to be surprised *from*. Most failed hooks skip this step and jump straight to "be punchy."

### Step 3: Draft 3 Hook Variants Across 3 Mechanisms

**ACTION:** Produce exactly three variants, each using a different mechanism. Drafting fewer than three hides the tradeoff; drafting more wastes tokens and dilutes the post-dictable test.

**Mechanism A — Schema-Break Lead (capture, short-form):**
- Set up the default category for a half-beat, then violate it in the next beat.
- Use when the medium is short (headline, subject line, ad, cold open, first paragraph).
- Target: an instant "wait, what?" that resolves immediately into the core.
- Exemplar: **Nora Ephron's journalism teacher.** The class wrote leads like "Principal Kenneth L. Peters announced this morning that the entire high school faculty will travel to Sacramento for a colloquium." The teacher's flip: *"The lead is — there will be no school Thursday."* The schema ("announcements are about who announced what") is violated by the real lead ("what does this mean for me").

**Mechanism B — Schema-Break Dramatization (capture, mid-form):**
- Build up the expected pattern deliberately, then collapse it at a single sharp moment that the core message then explains.
- Use when you have 3–10 sentences, a short video, a landing hero section, or a cold-open scene.
- Target: a vivid image the audience can replay in their head that *already contains* the core.
- Exemplar: **CSPI's Art Silverman on movie popcorn.** A medium popcorn has 37g of saturated fat. Instead of quoting the number, Silverman staged a table: a bacon-and-eggs breakfast, a Big Mac lunch, a steak dinner — and the bag of popcorn, which equalled all three combined. The schema ("popcorn is a snack") breaks the moment the camera pans. Rule of thumb: if your statistic won't stick, find a familiar reference object that makes the magnitude visceral.
- Exemplar: **Nordstrom Nordies.** To teach "outstanding service" the company doesn't post a values poster; it tells the story of the Nordie who refunded snow tires Nordstrom never sold, or gift-wrapped goods bought at Macy's. The schema ("retail workers follow rules") is broken by a specific, repeatable incident. Use this pattern when the core is a cultural norm or behavior.

**Mechanism C — Curiosity Gap Opener (hold, long-form):**
- Open with a genuine knowledge gap the reader didn't know existed, then make the rest of the piece the resolution.
- Use when the medium is long: whitepaper, essay, sales page, 20-minute talk, feature announcement you want people to finish.
- Target: a gap painful enough that the reader commits to staying until it closes.
- Exemplar: **Cialdini's Saturn-rings opener.** Cialdini found the most memorable science writing started with a genuine mystery — *"three top labs disagree on what the rings of Saturn are made of"* — and used the essay to resolve it. The reader didn't know there was a disagreement; now they need to.
- Exemplar: **News-teaser pattern** ("Which local restaurant has slime in its ice machine? Details at 11."). A pointed, specific question whose answer is exactly the core message.
- Exemplar: **Priming a gap in a boring domain** (Roone Arledge's NCAA football broadcasts). When the topic is dry, front-load questions the novice now realizes they can't answer, then pay them off one by one.

**For each variant, write:**
```
### Variant [A|B|C]: <mechanism name>
Hook (drop-in text): <1–5 sentences, exact copy the user can paste>
Pattern broken: <the schema or expectation the hook violates>
Gap opened: <the specific knowledge gap — only for Mechanism C; for A/B, write "N/A — capture only">
Bridges to core via: <one sentence showing how this hook makes the core message feel inevitable>
```

**WHY three:** The Heath brothers distinguish SURPRISE (short-term capture) from INTEREST (long-term hold) as two different problems. Drafting only capture variants solves the first problem and loses the second; drafting only curiosity-gap variants solves the second and fails at the door. Forcing one of each makes the mechanism choice visible to the user rather than hidden behind the writer's instinct.

**Artifact:** `## Variants` section with three subsections.

### Step 4: Score Each Variant Against the Post-Dictable Test

**ACTION:** For every variant, answer four questions in writing. No variant ships without all four answered.

1. **Post-dictable?** *After the audience reads the full message, does the surprise feel inevitable — like of course the piece had to open that way?* If yes, 1 point. If the surprise is an unrelated stunt the audience would have to forgive, 0.
2. **Delivers the core?** *Is the specific core message the thing the surprise makes inevitable?* If yes, 1. If the surprise lands some core but not the one you confirmed in Step 1, 0.
3. **Schema actually present?** *Is the pattern being broken a pattern the audience actually holds?* If the schema is only in the writer's head, the surprise will land as "weird" rather than "unexpected." 1 or 0.
4. **Gap resolvable by this specific piece?** *(Mechanism C only)* The gap must be payable off by the body the user already has. A gap this piece can't close is clickbait. 1 or 0 for C; N/A for A and B.

**Reject any variant that scores 0 on question 1 or 2.** Those are the gimmick-trap failures. Rewrite the variant or mark it as rejected with a note.

**Rank the surviving variants.** Tiebreaker goes to the variant whose pattern-break is tightest (fewest words between setup and violation) for short-form, or whose gap is narrowest (most specific unanswered question) for long-form.

**Artifact:** `## Post-dictable scorecard` table in `hook-options.md` with one row per variant, plus a `## Ranking` section.

**WHY:** This is the skill's core defense against the single failure mode the Heaths call out repeatedly: surprise used as decoration. The test is written explicitly because even experienced writers skip it — if the hook *feels clever*, they ship it. The question "would this feel inevitable in hindsight?" is the only reliable filter between sticky Unexpected and forgettable gimmick.

### Step 5: Write the Hook-Options Artifact

**ACTION:** Assemble `hook-options.md` with the sections produced above, in this order:
1. `# Hook options for: <short title>`
2. `## Core message (confirmed)` — one sentence.
3. `## Schema to break` — 1–3 bullets.
4. `## Variants` — Variant A, B, C with drop-in text.
5. `## Post-dictable scorecard` — 4-column table.
6. `## Ranking` — numbered list with one-line rationale per variant, rejected variants flagged.
7. `## Placement notes` — where in the draft each ranked variant should be dropped and what line of the current draft it replaces.
8. `## What this skill did NOT change` — explicit note that the body of the message is untouched; point to the appropriate SUCCESs skills if further rewriting is needed (concrete-language swapper, credibility anchor, emotional pathway, story frame).

**WHY a physical artifact:** The user ships copy, not understanding. An explanation of "how to write a better hook" is worth nothing at 11pm before the launch; three variants and a ranking with drop-in text are immediately usable. Every BookForge skill ends with an artifact the user can ship or paste.

## Key Principles

- **Surprise is a tool, not a goal.** The Heath brothers repeat this with the word *postdictable*: the surprise must make the core feel inevitable. If your hook could sit on top of any message, it's decoration. Kill it.
- **Capture and hold are two jobs.** Short-form media only needs capture (Mechanism A). Long-form media dies without hold (Mechanism C). Mid-form usually needs both in sequence. Decide which job you're doing before you draft.
- **You can only break a named schema.** Spend a minute writing down the audience's default pattern. Every failed "surprising" hook in the wild violates a schema that existed only in the writer's head.
- **A gap is a promise, and the body must pay it.** Curiosity gap openers fail when the piece cannot resolve the gap they opened. A whitepaper that opens "why is X true?" and never answers X teaches the audience the source lies. Open only gaps this piece can close.
- **Gimmick vs Unexpected is a single question.** "After the audience has read the core, does the surprise feel inevitable?" No other test matters. Feels clever, makes them laugh, gets retweets — all irrelevant if the answer is no.
- **Specific always beats abstract in a hook.** Slime in the ice machine beats "contamination in restaurants." Three labs disagreeing on Saturn's rings beats "open questions in astronomy." Tire chains Nordstrom never sold beats "outstanding service." Concrete nouns are what let the schema break land.

## Examples

### Example 1: Dry product announcement needs a hook (short-form)

**Scenario:** A SaaS company is launching a new feature: their database migration tool now validates row counts before cutover. The PM writes: "We're excited to announce a new pre-cutover validation step in our migration tool, providing additional safety for enterprise customers."

**Trigger:** "Help me, this is boring, nobody's going to read past the first line."

**Process:**
1. Core message confirmed: *"Our migration tool now catches silent data loss before cutover, not after."*
2. Schema to break: audience (platform engineers) assumes feature-launch posts open with "we are excited to announce…" and are safe to skim.
3. Variants:
   - **A (Schema-break lead):** *"The worst kind of migration bug is the one that succeeds."* Pattern: launch posts open with a feature; this opens with a fear the reader has lived.
   - **B (Schema-break dramatization):** *"Imagine: the migration finishes green. Every monitor is calm. Three days later, support tickets start arriving from customers whose orders have vanished. Nobody knows when it happened."* Pattern: launch posts are about what the tool does; this is about what you'll never notice it doing until now.
   - **C (Curiosity gap opener):** *"Why did 7 of the last 10 silent-data-loss incidents we investigated look green in the migration console? Three answers, and the fix we shipped last week."* Pattern: promises a count and a fix.
4. Post-dictable scorecard: A scores 3/3, B scores 3/3, C scores 4/4. All three ship. Ranking: C first (long-form post, best hold), A second (best drop-in for subject line), B third.

**Output (`hook-options.md`):** Three drop-in variants, scorecard, placement notes. The PM picks C for the blog post, A for the email subject line.

### Example 2: Fundraiser for a research nonprofit (mid-form)

**Scenario:** A nonprofit studying rare pediatric kidney disease has a donation letter. Current opening: "Our team has been working tirelessly to advance research into pediatric nephrotic syndrome."

**Trigger:** "This reads like every other nonprofit letter. How do I make it actually land?"

**Process:**
1. Core message confirmed: *"A single researcher, funded by people like you, is the only person in the world studying the subtype that killed Emily."*
2. Schema to break: nonprofit letters open with "our team" / mission-speak / statistics.
3. Variants:
   - **A (Schema-break lead):** *"There is one doctor in the world studying what killed Emily. Her name is Dr. Martinez. Her lab has three people. You fund two of them."* Pattern broken: fundraising letters are about the cause; this is about a count — one, three, two.
   - **B (Dramatization):** Silverman-style — *"Pediatric nephrotic syndrome has more research dollars than you'd think — roughly the cost of one Super Bowl ad per year. Spread across the whole field. Now subtract the subtypes that already have funding. Now subtract the ones with fewer than 200 known cases. What's left is Dr. Martinez's lab."* A bagged-popcorn-next-to-a-steak-dinner staging in words.
   - **C (Gap opener):** *"Why does the rarest kidney disease in children have exactly three researchers worldwide? The answer isn't money. Keep reading."*
4. Post-dictable scorecard: A 3/3, B 3/3, C rejected — the letter cannot pay off "the answer isn't money" because the body's ask IS money. Fails test 4. Rewrite C as: *"Three people in the world are trying to save children like Emily. Here is what each of them does on Monday morning."* This version opens a gap the letter can close (specific work). Rescored 4/4.

**Output:** Two surviving variants plus the rewritten C, with a note that the original C was rejected because the curiosity gap did not match what the body of the letter was capable of resolving.

### Example 3: Conference talk cold-open (mid-form)

**Scenario:** A senior SRE is giving a 20-minute talk on post-incident reviews. Opening slide currently says "Learning from Production Incidents: A Practitioner's Guide."

**Trigger:** "Give me a cold open that isn't 'hi my name is.'"

**Process:**
1. Core message confirmed: *"The post-incident review you write in the first 48 hours is almost always wrong about the cause, and that's fine — write it anyway."*
2. Schema to break: SRE talks open with a definition of reliability or a fancy outage graph.
3. Variants:
   - **A (Schema-break lead):** *"Every post-incident review I've ever written has been wrong. So has every one you've written. Let's talk about why that's the right outcome."*
   - **B (Dramatization):** *Slide 1: an incident timeline. Slide 2: the same timeline six months later, with three of the 'root causes' struck through. 'This is the same incident. The middle version is what we told leadership. The bottom version is what actually happened. I want to talk about the gap between them.'*
   - **C (Gap opener):** *"Why do the best post-incident reviews tend to be the ones that contradict themselves six months later? I'll tell you what I found after reviewing 40 of ours."* (Nordie-style specific count.)
4. Post-dictable scorecard: A 3/3, B 4/4 (strongest because the schema-break is built into the visual), C 4/4. Ranking: B first, A second, C third.

**Output:** Three cold-open variants with exact speaker lines and slide cues. The SRE opens with B.

## References

- Source: *Made to Stick* Chapter 2 "Unexpected" and the "Easy Reference Guide" — Gap Theory of Curiosity (Loewenstein), postdictable surprise, schema-break, movie-popcorn/Silverman, Nordstrom Nordies, Nora Ephron lead, Buick Enclave ad, Cialdini Saturn-rings mystery.
- Related SUCCESs skills in this book (forthcoming in the same skill set): `core-message-extractor`, `curse-of-knowledge-detector`, `velcro-theory-concretizer`, `compact-message-pattern-picker`, `stickiness-audit`.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Made to Stick: Why Some Ideas Survive and Others Die* by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is part of the forthcoming `bookforge-made-to-stick` skill set covering the full SUCCESs framework. It is designed to be used standalone, but composes naturally with `core-message-extractor` (to confirm the core before drafting the hook) and `stickiness-audit` (to score the whole message after the hook is in place). Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills).
