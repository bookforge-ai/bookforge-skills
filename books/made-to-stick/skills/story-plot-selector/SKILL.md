---
name: story-plot-selector
description: Pick the right story plot (Challenge / Connection / Creativity) and structure it so it drives the specific action you need — and decide whether to deliver it as a springboard story or a direct argument. Use this skill whenever the user needs to find, pick, or shape a story, anecdote, or case study for a message, talk, pitch, announcement, training session, change effort, or culture push. Activate on "what story should I tell", "find me an anecdote", "how should I open this presentation", "we need a story here", "help me structure a case study", "which of these stories is the right one", "need an inspiring example", "tell a story about", "I have three anecdotes — pick one", "make this talk more human", "how do I open the all-hands", "what's the right case study for this pitch", "story for a keynote", "story to rally the team", "story for onboarding", "change management story", "need a motivating example", "story that shows why this matters", "the talk needs a narrative", or whenever a draft is pure argument/data and the user wants to replace or supplement a claim with a single concrete tale. Also triggers when the user has raw story material (news clipping, customer anecdote, personal experience, historical event) and asks how to frame or structure it. The skill classifies the story need into Challenge (overcoming obstacles — inspires perseverance), Connection (bridging differences — inspires empathy and cooperation), or Creativity (mental breakthrough — inspires experimentation), applies the matching structure, and decides between a springboard story (audience has agency, diverse contexts, you want buy-in) versus a direct argument (single unambiguous action). Also decides whether the story should work as simulation (mental rehearsal of how to act) or inspiration (motivation to act), or both. The skill does NOT fabricate events or invent characters — it works with real stories the user provides or helps them mine from real material. It does NOT write full emotional appeals (use emotional-appeal-selector) and does NOT score the full stickiness rubric (use stickiness-audit).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/story-plot-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [6, 13]
tags: [storytelling, communication, narrative, messaging, case-study, persuasion, change-management, springboard-story, public-speaking, instructional-design]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "The audience response the user wants (what the listener should do, feel, or decide after hearing the story)"
    - type: document
      description: "Raw story material — a draft anecdote, news clipping, customer quote, personal experience, or a shortlist of candidate stories to pick from"
    - type: document
      description: "Occasion and context — where the story will be told (keynote, all-hands, sales pitch, onboarding, memo, training module) and the surrounding argument"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment with file read/write. Document-set environment — the agent operates on short prose artifacts supplied by the user."
discovery:
  goal: "Classify a story need into one of three plots, structure the chosen story to drive the specific action, and decide the delivery mode (springboard vs direct, simulation vs inspiration)."
  tasks:
    - "Pick which of three candidate anecdotes is the right one to open a keynote"
    - "Classify a raw customer story and structure it to inspire a team behavior change"
    - "Decide whether to tell a story or make a direct argument for a change-management ask"
    - "Turn a news article into a structured case study matched to a specific intended action"
  audience:
    roles: [communicator, founder, marketer, manager, trainer, public-speaker, change-leader, product-marketer]
    experience: any
  when_to_use:
    triggers:
      - "User is writing a talk, pitch, memo, or training and needs a story for a specific section"
      - "User has raw anecdotes and wants to pick one and structure it for effect"
      - "User is planning a change effort and wants buy-in across diverse listeners"
      - "User is opening a presentation and needs the right first sixty seconds"
    not_for:
      - "Fabricating characters or events the user cannot verify"
      - "Full emotional-appeal selection (use emotional-appeal-selector)"
      - "Scoring the whole SUCCESs rubric (use stickiness-audit)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: "pending"
    eval_count: 0
---

# Story Plot Selector

## When to Use

You have a specific communication moment — a talk, pitch, memo, all-hands, training module, change announcement, sales deck, fundraising appeal — and you need a *story* (not just an argument) to land one specific action or feeling. You either have candidate story material already (anecdotes, customer quotes, news clippings, personal experience) or you know what action you want and need to pick which kind of story will drive it. Before starting, confirm: (1) what the listener should do/feel/decide after hearing the story, (2) whether you have real story material or need to mine it from real sources, and (3) where the story lives — opening, middle, closing, or standalone.

The core mechanic: stories drive action in two distinct ways — **simulation** (mental rehearsal of how to act in a situation) and **inspiration** (motivation to act). The Jared Subway story, for example, gave listeners both: a vivid picture of how weight loss is done (eat Subway subs daily) *and* the emotional push to try it. Your job as the author is to know which lever the situation needs and pick a plot that pulls it.

Three plots classify more than 80% of the stories in the original *Chicken Soup for the Soul* collection and more than 60% of the non-celebrity stories in *People* magazine:

- **Challenge plot** — protagonist overcomes daunting obstacles. Inspires perseverance, effort, taking on hard things.
- **Connection plot** — people bridge a gap (social, racial, class, generational, functional). Inspires empathy, cooperation, helping across lines.
- **Creativity plot** — someone has a mental breakthrough or solves a problem in a novel way. Inspires experimentation, trying a new approach.

If none of these fit, the story is probably not the one — keep looking or write a direct argument instead.

## Context & Input Gathering

### Required Context (must have — ask if missing)
- **Intended audience response:** What should the listener do, feel, or decide after hearing the story?
  -> Check prompt for: verbs like "inspire", "convince", "rally", "get buy-in", "teach", "motivate", explicit "I want them to ___"
  -> Check environment for: `brief.md`, `talk-outline.md`, `core-message.md`
  -> If still missing, ask: "What do you want the listener to do or feel after hearing this story? One sentence."
- **Raw story material OR a shortlist of candidates:** The actual anecdote, news item, customer quote, personal experience, or list of options.
  -> Check prompt for: pasted story text, a link, a name ("the Jared story"), file paths
  -> If missing, ask: "Do you already have a story or anecdote, or do you need help finding one from a specific pool of material (your customers, your team, the news)?"

### Observable Context (gather from environment)
- **The occasion:** Where the story will be told — talk, memo, slide, pitch, training.
  -> Look for: `draft.md`, `talk.md`, `slides.md`, `pitch.md`
  -> If unavailable: ask for the channel and the time budget (30 seconds? 2 minutes? standalone article?).
- **Audience profile:** Who the listener is and how much agency they have to act.
  -> Look for: `audience-profile.md`, `brief.md`
  -> If unavailable: ask "who is the audience and what action can they actually take?"
- **Sibling draft signals:** Is the surrounding text a direct argument already? Is a story supplementing or replacing it?

### Default Assumptions
- If the occasion is unclear, assume "short-form spoken or written message" (1–3 minutes of time budget).
- If audience agency is unclear, ask — it is the single biggest input to the springboard vs direct decision (Step 4) and should not be defaulted.
- Never invent events, names, numbers, or quotes. If the user's material is thin, say so and ask for more.

### Sufficiency Threshold
SUFFICIENT: intended response + story material (or a clear pool to mine from) + occasion known
PROCEED WITH DEFAULTS: intended response + material known; occasion defaulted to short-form
MUST ASK: intended response unclear OR no real material AND no pool to mine from OR audience agency unknown

## Process

### Step 1: Clarify the intended action
**ACTION:** In one sentence, write down what the listener should do, feel, or decide after hearing the story. Write it as a verb the listener will perform ("apply our tool to a new domain next week", "forgive a teammate they're blaming", "try the new grinder design process"), not as a feeling word ("be inspired", "feel motivated").

**WHY:** Every downstream choice — plot, structure, delivery mode — is determined by this single sentence. A story that is "inspiring" in the abstract but does not drive the specific action is decoration. The whole point of stories in Chapter 6 is that they are tools for generating behavior; without a target behavior, you cannot pick between plots because all three plots are "inspiring" but in different directions. Challenge plots inspire effort, Connection plots inspire empathy, Creativity plots inspire experimentation. You cannot pick one until you know which of those three bowls the action falls into.

**Artifact:** `story-structure.md` — start the file with `## Intended Action:` followed by the one-sentence target behavior.

### Step 2: Classify the story need into one of three plots
**ACTION:** Using the decision rule below, classify the intended action into Challenge, Connection, or Creativity. If two plots seem to fit, pick the one that matches the *dominant* behavior you want — not the richest story. If none fit, go to Step 2b.

**WHY:** The three plots are not interchangeable — they trigger different downstream behaviors in the listener. Picking the wrong plot means the listener is motivated toward the wrong action. Jared's story (Challenge) works because it inspires *personal effort* to match Jared's perseverance; if Subway had told the same facts as a Creativity story ("Jared solved a nutrition puzzle"), listeners would have felt intellectual admiration rather than "maybe I could try this too."

**Decision rule:**

| If you want the listener to... | Pick | Core engine |
|---|---|---|
| Work harder, persevere, take on a daunting goal, push through an obstacle | **Challenge** | Protagonist vs daunting odds → success |
| Bridge a gap (help a stranger, trust a teammate, work across lines of difference, reach across conflict) | **Connection** | Protagonist crosses a social/relational gulf |
| Try a new approach, experiment, break a process pattern, solve a problem differently | **Creativity** | Protagonist makes a mental breakthrough |

**Test for daunting-ness (Challenge plot specifically):** The obstacles must seem daunting *relative to the protagonist*. Jared losing 245 pounds is a Challenge plot. Jared's neighbor shaving an inch off his waist is not. If your story's protagonist is only mildly challenged, it will not inspire listeners to take on their own hard things — the bar is too low to be motivating.

**IF** no plot fits cleanly -> go to Step 2b.
**ELSE** -> record `plot: {Challenge|Connection|Creativity}` in the artifact and proceed.

### Step 2b: No plot fits — decide story-or-not
**ACTION:** If none of the three plots match the intended action, the situation may not be a story problem at all. Before forcing a plot, ask: "Would a direct argument, a concrete constraint, or a data point do this job better?" If yes, stop and tell the user. If the user still wants a story, pick the plot closest to the action and flag the mismatch in the artifact.

**WHY:** Stories are not free. They take time, they carry emotional weight, and a mismatched story actively fights your message. The three plots cover ~80% of inspirational story cases — the remaining ~20% are usually better served by a concrete example, a direct claim, a statistic, or a one-sentence core message. Forcing a story into a plot it doesn't fit is how people end up with anecdotes that feel tacked on.

### Step 3: Decide the simulation / inspiration mix
**ACTION:** Mark the story as providing simulation (S), inspiration (I), or both (S+I). Use the test below.

**WHY:** Stories work as *mental simulators* and/or *motivators* — these are distinct effects. The Xerox copier-repair story (lunchroom shop talk about an E053 error) is pure simulation: no emotional uplift, but listeners learn a diagnostic pattern they can apply next week to a real broken machine. The Jared story is both — listeners learn that daily Subway sandwiches correlate with dramatic weight loss (simulation) *and* feel moved to try it (inspiration). Knowing which lever the occasion needs controls how you write the story in Step 5.

**Tests:**
- **Simulation needed (S)** if: the listener needs to know *how* to act in a specific kind of situation; the value is transferable pattern recognition; the story will be used in training, onboarding, or a how-to context; the listener will need to handle a similar case next week.
- **Inspiration needed (I)** if: the listener needs *motivation* to act on something they already know how to do; the value is emotional momentum; the story will be used in a rally, pitch, keynote open/close, fundraising moment, or change-kickoff.
- **Both (S+I)** if: the listener needs both a picture of the behavior *and* the push to start — typical of culture-change, behavior-change campaigns, and case studies used to drive adoption.

Record `mode: S | I | S+I` in the artifact.

### Step 4: Decide springboard story vs direct argument
**ACTION:** Decide whether the story should be delivered as a **springboard story** (tell a seed story, let each listener generate their own application) or as a **direct argument with illustrative story** (make the claim explicitly, use the story as proof). Use the rule below.

**WHY:** Stephen Denning's work at the World Bank showed that when you *hit listeners between the eyes* with a direct argument, they fight back — they evaluate it, criticize it, argue with the "little voice inside the head." A springboard story bypasses that by engaging the little voice: it gives the listener a tiny seed of possibility and lets them generate their own second story about how it applies to *their* context. This is why Denning could introduce a whole knowledge-management strategy at the World Bank in 10 minutes using one short story about a health-care worker in Zambia finding CDC data about malaria online — each executive in the room could mentally substitute their own project for "Zambia" and generate a version of knowledge management that fit their world. A direct argument could never have produced that breadth of buy-in in 10 minutes, because each executive would have argued with it from their own specific context.

**Rule — use a springboard story when ALL of these are true:**
- The audience has meaningful agency to act in *diverse contexts* (each person's application will look different).
- You want buy-in across skeptics, not compliance from subordinates.
- A seed of possibility is enough — you do not need to specify exact behavior.
- The audience is likely to argue back if you make a direct claim ("little voice" is loud).

**Use a direct argument with illustrative story when:**
- You need one specific, unambiguous action from everyone.
- The audience is friendly and the claim is not contested.
- The action has a fixed procedure (training / how-to / compliance).
- You have very limited time AND the story is carrying proof, not persuasion.

**IF** springboard -> keep the seed story lean, end with an unstated "could this work here?" implicit question, do NOT hand the listener the conclusion.
**ELSE** -> make the claim explicitly first, then use the story as a *single overwhelming example* (Sinatra-style).

Record `delivery: springboard | direct` in the artifact.

### Step 5: Structure the story using the matching arc
**ACTION:** Write the structured story using the arc template for the chosen plot. Keep it short (time-budget aware — 30 seconds / 2 minutes / 5 minutes). Include only details that pull the intended action lever. Cut everything that is just "interesting."

**WHY:** Each plot has a structural spine that makes the inspiration mechanism fire. A Challenge plot that buries the obstacle under biographical setup does not inspire perseverance — the reader forgets what was at stake. A Connection plot that skips the "gulf" between protagonist and other does not inspire crossing gulfs. A Creativity plot that omits the old approach does not inspire breaking patterns. The arc is the mechanism.

**Challenge arc:**
1. Protagonist + stakes (who, what they have to lose, who else is affected).
2. The obstacle is named and made to feel daunting *relative to the protagonist*.
3. Attempt and setback (shows the obstacle is real, not trivial).
4. Perseverance or clever effort.
5. Resolution + specific change in protagonist's world.
6. Implicit invitation: "you could take on your thing too."

**Connection arc:**
1. Protagonist and the "other" — name the gulf explicitly (social, racial, class, functional, generational). Modern audiences often miss the gulf in old stories (the Good Samaritan needs the "atheist-biker-gang-member" reframe to land today).
2. The moment of encounter — the protagonist could walk past.
3. The cost of crossing the gulf (time, money, status, comfort).
4. The act of connection, in concrete terms.
5. What the "other" received that the priest/Levite walked past.
6. Implicit invitation: "cross the gulf near you."

**Creativity arc:**
1. The old approach — named, and visibly slow, expensive, or stuck.
2. The frustration ("it was taking us longer to build a new grinder than it took to fight World War II").
3. The breakthrough moment — a concrete, unexpected act (tying plastic and metal samples to a car bumper and driving them around a parking lot).
4. The result (enough to show the new approach works).
5. Implicit invitation: "what test could you run this week, without permission?"

**Shackleton note:** Stories can combine plots — Shackleton's Antarctic expedition is a Challenge plot (survival odds) wrapped around a Creativity plot (assigning the complainers to sleep in his own tent to contain their influence). If your story is legitimately dual, lead with the plot that matches your intended action.

**Artifact:** Add `story:` (the structured draft) to `story-structure.md`.

### Step 6: Write the opening line
**ACTION:** Write the first sentence of the story. It must do one thing: make the listener want to hear the second sentence. Drop the reader mid-scene or mid-question; do not start with context, a thesis statement, or a summary of the point.

**WHY:** Stories compete with the listener's attention budget. An opening line that explains the point before telling the story kills the mechanism — listeners evaluate the thesis instead of entering the scene. "In the late 1990s, Subway launched a campaign based on a statistic: Seven subs under six grams of fat. It didn't stick." is a better opener than "Today I want to talk about how stories are more memorable than statistics" because it pulls the listener into a concrete moment that has not yet revealed its point.

**Rules:**
- Opening line names one concrete thing (a place, a person, a weight, a date, an object).
- Opening line does not summarize the moral.
- For springboard stories, the opening line is also the hook — the rest must earn the listener's continued "little voice" engagement.

**Artifact:** Add `opening_line:` to `story-structure.md`.

### Step 7: Self-check against fabrication and fit
**ACTION:** Re-read the structured story and verify four things. Fix any failures or flag for the user.

**WHY:** The skill is worth nothing if it fabricates or if it produces a beautifully structured story that drives the wrong action. These four checks cover the common failure modes.

**Checks:**
1. **No fabrication.** Every fact, name, number, quote, and event traces back to the source material the user provided. If any detail is invented, mark it `[invented — verify or remove]`.
2. **Plot matches the intended action.** Re-read Step 1 and Step 2 — does the plot still line up? If the story drifted into inspiration for the wrong action during structuring, re-pick the plot.
3. **Daunting enough (Challenge only).** If it is a Challenge plot, the obstacle must feel daunting relative to the protagonist. If it doesn't, the story won't inspire effort — either find a stronger version or switch to a different story.
4. **Delivery mode honored.** If springboard: the conclusion is unstated. If direct: the claim is explicit and the story follows it as proof.

**IF** any check fails -> fix and re-run Step 5–7.
**ELSE** -> mark the artifact complete.

## Inputs
- **Intended audience response:** one-sentence target behavior.
- **Raw story material:** real anecdotes, news, customer stories, personal experience (OR a pool to mine from).
- **Occasion:** channel, time budget, where in the draft the story lives.
- **Audience profile:** who the listener is and what agency they have.

## Outputs
- **`story-structure.md`** — the single deliverable. Template:

```markdown
# Story Structure

## Intended Action
{one-sentence target behavior the listener should perform}

## Plot Classification
**Plot:** {Challenge | Connection | Creativity | none-fit}
**Why this plot:** {one line tying the intended action to the plot's inspiration mechanism}

## Mode
**Simulation / Inspiration:** {S | I | S+I}
**Why:** {one line}

## Delivery
**Mode:** {springboard | direct}
**Why:** {one line referencing audience agency and context diversity}

## Opening Line
> {the first sentence}

## Structured Story
{the story, arc-aligned, within the time budget}

## Caveats
- {any [invented — verify] flags}
- {any dual-plot notes}
- {whether a direct argument would actually fit better}
```

## Key Principles

- **Pick the plot by the action, not by the story you love.** A beautiful Creativity story used to inspire perseverance will teach listeners to look for clever shortcuts instead of working harder. The plot-to-action mapping is not negotiable: Challenge drives effort, Connection drives empathy, Creativity drives experimentation.
- **Simulation and inspiration are separate levers.** Ask which (or both) the occasion needs before you write. Xerox lunchroom shop talk is pure simulation (no uplift, just transferable diagnostic patterns). Jared Subway is both. Most keynote openers are pure inspiration. Get the mix right and the story carries the right weight.
- **Springboard beats direct when the audience has diverse contexts.** If every listener will apply the idea in a different setting (executive committee, cross-functional reorg, distributed teams), a springboard story lets each one generate their own application — you get breadth of buy-in in minutes. A direct argument in the same slot triggers the "little voice" to argue back and you lose the room.
- **Name the gulf explicitly (Connection plots only).** Modern audiences miss the social distance in old stories. "Good Samaritan" lands for Bible-literate audiences; "atheist biker gang member helping a stranded priest" lands for everyone else. If the gulf is invisible, the cross is invisible, and the story inspires nothing.
- **Daunting is relative, not absolute.** A Challenge plot is defined by whether the obstacle feels daunting *to the protagonist*, not by the absolute scale. Rose Blumkin postponing her 100th birthday to keep her store running is a Challenge plot. A 210-pound neighbor losing an inch of waist is not. If the story's stakes are low, it will not inspire listeners to take on their own hard things.
- **You do not invent stories — you spot them.** The Heaths' core claim in Chapter 6 is that life keeps handing you usable material; the skill is recognition, not fabrication. If the source material will not support the plot you want, find a different story — do not add details.
- **The opening line drops you into a scene.** First sentences that name a concrete thing (a place, a weight, a date, a person) beat first sentences that announce the thesis. A thesis-first opener lets the listener evaluate the claim instead of entering the story.

## Examples

**Scenario: keynote opener for a health-product launch**
Trigger: Founder says: "I have 90 seconds to open the keynote. I want the audience to believe a single person's daily choice can produce a huge outcome. I have three candidate stories: a Subway customer named Jared, a Harvard nutrition study, and my own cousin's weight-loss journey."
Process: (1) Intended action: "start a daily habit this week." (2) Plot: Challenge — protagonist overcomes daunting obstacle through perseverance. (3) Mode: S+I — listeners need both the pattern (how weight loss was done) and the emotional push. (4) Delivery: direct — one specific action requested, friendly launch audience, 90-second budget. Skip the Harvard study (no plot, no protagonist) and the founder's cousin (not public, audience cannot verify). Pick Jared. (5) Structure the Challenge arc: 425-pound college junior, size XXXXXXL shirts, swollen ankles and edema diagnosis, father's warning about dying before 35, 245-pound loss on daily Subway subs. (6) Opening line: "In the spring of 1998, a college junior named Jared Fogle wore size XXXXXXL shirts and a 60-inch waist." (7) Self-check: all facts verifiable from Subway campaign, daunting obstacle clear, plot matches action.
Output: `story-structure.md` with Challenge-plot Jared story, S+I mode, direct delivery, and a scene-drop opener.

**Scenario: change-management kickoff for a knowledge-management initiative**
Trigger: Program lead says: "I have 10 minutes at the next leadership offsite to introduce a new knowledge-management strategy. The 15 execs in the room run wildly different parts of the business. I need all of them to champion this back in their units. I have one anecdote about a colleague who found malaria-treatment data on the CDC website from a remote office in Zambia."
Process: (1) Intended action: "champion a knowledge-management initiative inside your own unit this quarter." (2) Plot: Creativity — the health-care worker's breakthrough was finding data on the internet in 1996. (3) Mode: S+I. (4) Delivery: springboard — diverse contexts (15 different business units), meaningful agency, buy-in required, not compliance. Each exec must generate their own version of "what would knowledge management look like in my unit?" A direct argument would be fought. (5) Structure: lean Creativity arc — name the old approach (siloed project knowledge, no sharing across countries), the frustration (a water-treatment guru in Zambia never meets a highway-construction guru in Bangladesh), the breakthrough moment (the worker in Kamana logging on and finding CDC data), the result (acted more effectively against malaria), implicit invitation left unstated. (6) Opening line: "In June 1995, a health-care worker in Kamana, Zambia — 360 miles from the capital — logged onto the internet and tried to find out how to fight malaria." (7) Self-check: no fabrication, plot matches action, delivery mode honored (conclusion stays implicit).
Output: `story-structure.md` with Creativity-plot Zambia springboard story, S+I mode, unstated conclusion that lets each exec project themselves in.

**Scenario: sales-training story for a new customer-success team**
Trigger: Training lead: "I need a story for the onboarding session. New CSMs tend to escalate every tricky ticket to engineering instead of troubleshooting. I want them to pattern-match on complex error states and try one or two hypotheses first. I have a transcript of a Xerox copier repairman explaining how he chased a misleading E053 error."
Process: (1) Intended action: "try two hypotheses on a tricky ticket before escalating." (2) Plot: Creativity — troubleshooting is mental breakthrough. (3) Mode: Simulation only — this is training, not motivation; the listener needs a transferable diagnostic pattern, not emotional lift. (4) Delivery: direct — onboarding, single unambiguous behavior requested, friendly audience, no "little voice" resistance. (5) Structure: lean Creativity arc — old approach (escalate on misleading error codes), the E053 error showing up and being genuinely misleading, the hypothesis-testing that led to the bad dicorotron diagnosis, the payoff (running long enough to confirm). (6) Opening line: "A copier salesperson at lunch said: 'The new XER board won't cook itself anymore — instead it trips the 24-volt interlock and crashes with an E053.'" (7) Self-check: all facts in user's transcript, plot matches action, simulation mode honored (no inspirational flourish).
Output: `story-structure.md` with Creativity-plot Xerox story, Simulation-only mode, direct delivery, and a mid-scene opener that teaches the shop-talk pattern.

## References
- For an extended catalog of worked examples (Jared Subway / Rose Blumkin / Shackleton Antarctic / Xerox lunchroom / Denning Zambia / Ingersoll-Rand grinder "drag test" / Good Samaritan modern reframe) with full source attribution and plot-arc markup, see [references/plot-example-catalog.md](references/plot-example-catalog.md)
- For the output template and worked filled-in example, see [references/output-template.md](references/output-template.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Made to Stick: Why Some Ideas Survive and Others Die* by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
