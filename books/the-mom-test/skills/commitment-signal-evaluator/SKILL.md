---
name: commitment-signal-evaluator
description: Evaluate whether a customer meeting produced real interest or just polite enthusiasm by classifying commitment signals into time, reputation, and money currencies. Use this skill after any customer conversation, product demo, sales call, or pitch where the user wants to know if the meeting actually advanced the deal, asks "was that a good meeting" or "how did it go" or "did that go well," says a meeting "went great" but nothing happened afterward, received enthusiastic feedback and wants to know if it is real, wonders whether someone is actually interested or just being polite, heard "I would definitely buy that" and wants to know if it means anything, wants to distinguish real leads from false-positive prospects (zombie leads), needs to score a pipeline of prospects for conversion likelihood, wants to detect polite rejections disguised as enthusiasm (compliment-stall pattern), or wants to identify early evangelists in their prospect pool — even if they don't explicitly mention "commitment signals" or "meeting evaluation." This skill evaluates meeting OUTCOMES and prospect INTEREST, not conversation data quality (use conversation-data-quality-analyzer) or conversation logistics (use conversation-format-selector).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-mom-test/skills/commitment-signal-evaluator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [5]
tags: [customer-discovery, commitment, sales-signals, meeting-evaluation, zombie-leads, earlyvangelists]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Meeting notes, conversation transcript, or summary of a customer meeting outcome"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with access to meeting notes or transcript files"
---

# Commitment Signal Evaluator

## When to Use

You have just finished (or are reviewing) a customer meeting, product demo, sales call, or investor conversation and need to assess whether the meeting produced real signals of interest or just polite enthusiasm. Typical triggers:

- The user shares meeting notes and asks "how did it go?" or "was that a good meeting?"
- The user has a pipeline of leads and wants to identify which are real vs false-positive prospects (zombie leads)
- The user received enthusiastic feedback but is unsure whether it translates to actual demand
- The user wants to know what commitment to push for at the next meeting
- The user is reviewing a batch of conversations and needs to score signal strength across prospects

**Preconditions to verify:**
- Does the user have meeting notes, a transcript, or at least a summary of what happened?
- Does the user know what product stage they are at? (Pre-product learning vs product demo vs active selling)

**This skill does NOT cover:**
- Evaluating whether the questions asked were good (use `conversation-data-quality-analyzer`)
- Structuring conversation learnings into validated/invalidated assumptions (use `conversation-learning-process`)

## Context & Input Gathering

### Required Context (must have -- ask if missing)

- **Meeting notes or transcript:** The raw material to evaluate. Without this, there is nothing to score.
  -> Check prompt for: pasted text, file path, quotes from the meeting, summary of what happened
  -> Check environment for: files in a `conversation-notes/` or `meetings/` directory
  -> If still missing, ask: "Can you share the meeting notes or paste the key moments from the conversation? I need the actual words and outcomes to evaluate signal strength."

- **Product stage:** Determines which commitment currencies are appropriate to expect. Asking a pre-product prospect for money is premature; not asking a post-demo prospect for a next step is a missed opportunity.
  -> Check prompt for: mentions of "prototype," "MVP," "beta," "launched," "idea stage," "we showed them the product"
  -> If still missing, ask: "What stage is your product at? (a) Still exploring the problem -- no product yet, (b) Have wireframes or prototype, (c) Have working product or beta, (d) Product is live and selling"

### Observable Context (gather from environment)

- **Previous meeting notes:** Past conversations with the same person or segment reveal whether commitment is escalating or stalling.
  -> Look for: files mentioning the same contact name, company, or segment
  -> If unavailable: evaluate this meeting in isolation

- **Commitment tracker:** An existing log of commitments received from various prospects.
  -> Look for: `commitment-tracker.md`, `pipeline.md`, `leads.csv`
  -> If unavailable: create one as part of the output

### Default Assumptions

- If product stage is unclear: assume early-stage (pre-product) and calibrate expectations accordingly. Early-stage meetings should produce time and reputation commitments, not financial ones.
- If only a brief summary is provided (not full notes): evaluate based on available signals but flag that the assessment is partial.

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Meeting notes or transcript with identifiable outcomes/statements are available
- Product stage is known or can be inferred

PROCEED WITH DEFAULTS when:
- Meeting notes are brief but contain at least one closing statement or outcome
- Product stage can be inferred from context

MUST ASK when:
- No meeting content is available at all
- The user describes a meeting but provides zero specific quotes or outcomes
```

## Process

### Step 1: Extract Meeting Outcomes and Closing Statements

**ACTION:** Read the meeting notes or transcript. Identify all statements, actions, and promises made by the prospect at or near the end of the meeting. Also flag any strong emotional reactions throughout.

**WHY:** The closing moments of a meeting reveal what the prospect is actually willing to do, not just what they said they felt. Enthusiasm during the meeting is cheap -- what they commit to afterward is the real signal. Emotional intensity mid-conversation (pain, frustration, excitement about their problem) also matters because it predicts earlyvangelist potential.

**Extract and list:**
- Direct quotes from the prospect (especially closing statements)
- Any promises made (introductions, follow-ups, purchases, trials)
- Any actions the prospect took during or after the meeting (signed up, scheduled, introduced)
- Emotional intensity markers (frustration with current solutions, excitement about the problem space)
- Anything the prospect gave up (time for next meeting, shared internal docs, made an intro)

### Step 2: Classify Each Signal Using Commitment Currencies

**ACTION:** For each extracted signal, classify it into one of four categories based on what the prospect gave up:

**Commitment Currencies (ranked by signal strength):**

| Currency | What They Give Up | Examples | Signal Strength |
|----------|------------------|----------|----------------|
| **No currency (compliment)** | Nothing | "That's so cool!", "Love it!", "Looks great" | ZERO -- costs them nothing, worth nothing |
| **Time** | Their calendar, attention, effort | Clear next meeting with specific goals, sitting down to review wireframes, using a trial for a non-trivial period | LOW-MEDIUM |
| **Reputation** | Their social capital and credibility | Intro to peers or team, intro to decision maker (boss, spouse, lawyer), public testimonial or case study | MEDIUM-HIGH |
| **Money** | Cash, budget, purchasing authority | Letter of intent, pre-order, deposit, pulling out a credit card | HIGHEST |

**WHY:** A compliment costs the prospect nothing, so it carries zero informational value. The more they give up, the more seriously you can take their words. This is the core insight: words are free, actions cost something. Classifying by currency type immediately separates real signals from noise. Strong commitments often combine multiple currencies -- for example, agreeing to a paid trial with their whole team risks time, money, AND reputation.

**IF** a signal combines multiple currencies -> note it as a compound commitment (strongest type)
**IF** a signal is purely verbal with no cost to the prospect -> classify as compliment (zero signal)

### Step 3: Score Each Signal as Good Meeting / Bad Meeting

**ACTION:** Evaluate each closing statement against the meeting outcome scoring rubric:

| What They Said | Verdict | Why | Fix |
|----------------|---------|-----|-----|
| "That's so cool. I love it!" | BAD | Pure compliment. Zero data. May feel good but contains no actionable information. | Deflect the compliment, ask about their current process or next steps. |
| "Looks great. Let me know when it launches." | BAD | Polite rejection disguised as enthusiasm (compliment-stall). A polite way to say "Don't call me, I'll call you." The big error is mistaking this for a pre-order. | Ask for a commitment available today: intro to their boss, agreement to be a beta tester, or a letter of intent. |
| "There are a couple people I can intro you to when you're ready." | BAD (currently) | Some signal exists but the promise is too vague to act on. "When you're ready" is a deferral. Who specifically? Ready for what? | Convert fuzzy promise to concrete specifics: "Who did you have in mind? Could we set that up this week?" |
| "What are the next steps?" | GOOD | They are actively advancing the deal. But you must know YOUR next steps to benefit -- if you say "let me think about it and get back to you," you have ruined a good meeting. | Have your next steps prepared before the meeting. Always know what commitment you will ask for. |
| "I would definitely buy that." | BAD (dangerous) | This is the most dangerous false positive. Future-tense promises are unreliable. This exact phrase has sunk startups that treated it as validation. | Shift to concrete current commitment: letter of intent, pre-order, deposit, or intros to other decision makers. |
| "When can we start the trial?" | MAYBE GOOD | Depends on what the trial costs them. A free trial of consumer software costs nothing (low signal). A trial that requires training staff and integrating systems costs real time and reputation (high signal). | Evaluate the trial in terms of currency: what are they actually giving up to try it? If too cheap, increase the cost -- ask for a case study commitment after 2 weeks. |
| "Can I buy the prototype?" | GREAT | Strongest possible signal. They want it so badly they will pay for an unfinished version. This is rare and precious. | Take their money. Keep them close. This person is a potential earlyvangelist. |
| "When can you come back to talk to the rest of the team?" | GOOD | Reputation commitment -- they are willing to stake their credibility by bringing you to their colleagues. In enterprise sales, this is a strong advancement signal. If they will not introduce you, it is a dead end. | Schedule the meeting immediately. Prepare for a different audience (technical team vs decision maker). |

**WHY:** Every meeting either succeeds (produces commitment and advancement) or fails (produces only compliments or stalling). There is no such thing as a meeting that "went well" -- that phrase is itself a warning sign. Scoring each outcome forces an honest assessment and prevents the natural human tendency to interpret politeness as progress.

### Step 4: Detect Anti-Patterns

**ACTION:** Scan the meeting outcomes for two critical anti-patterns:

**Anti-Pattern 1: False-Positive Prospects (Zombie Leads)**
Symptoms:
- A pipeline of prospects who keep taking meetings but never convert
- Meetings that end with compliments but no clear next steps
- Meetings described as having "gone well"
- The prospect has not given up anything of value across multiple meetings

**WHY:** Zombie leads are caused by avoiding the scary question -- the one that could get you rejected. By failing to push for commitment, you stay in a comfortable no-man's-land where the prospect keeps being friendly but never moves forward. This is like being friend-zoned by your startup. The fix is to give them a concrete chance to reject you, because rejection is data and no-man's-land is not.

**Anti-Pattern 2: Polite Rejection Disguised as Enthusiasm (Compliment-Stall)**
Symptoms:
- Enthusiastic words with no concrete follow-through
- Future-tense promises: "I would...", "When you launch...", "Eventually..."
- Vague offers: "I know some people...", "We should definitely..."
- The prospect defers all action to an unspecified future date

**WHY:** The compliment-stall is the most common way meetings fail. The prospect is being polite, not committed. Every flavor of "let me know when it's ready" is a polite way to say "Don't call me, I'll call you." The fix is to look for a commitment available today, not in the future.

**IF** zombie lead pattern detected -> flag the entire relationship, not just this meeting
**IF** compliment-stall detected -> recommend specific commitment asks for the next interaction

### Step 5: Evaluate Earlyvangelist Potential

**ACTION:** Check whether the prospect meets the four criteria for an earlyvangelist (early evangelist, a term from Steve Blank's Customer Development methodology) -- the rare person who will become your first real customer:

1. **Have the problem** -- They experience the pain your product addresses
2. **Know they have the problem** -- They are consciously aware of it, not just theoretically affected
3. **Have the budget to solve it** -- They can actually spend money on a solution
4. **Have already cobbled together their own makeshift solution** -- They care enough that they built a workaround

**Emotional intensity signal:** There is a significant difference between "Yeah, that's a problem" and someone who is deeply frustrated, emotional, or excited about the problem space. When you see deep emotion, keep that person close -- they are a rare potential first customer.

**WHY:** First customers are irrational in a good way. They want what you are making so badly they will be the first to try it, knowing the risks. Identifying them early is critical because they will front money on pre-orders, tell friends, give feedback, and become your case studies. Not every interested prospect is an earlyvangelist -- most are just being polite.

**IF** prospect meets all 4 criteria -> flag as HIGH PRIORITY earlyvangelist candidate
**IF** prospect meets 3 of 4 -> flag as POTENTIAL, note which criterion is missing
**IF** prospect shows deep emotion about the problem -> flag regardless of other criteria, investigate further

### Step 6: Determine Overall Meeting Score and Recommend Next Steps

**ACTION:** Produce the final meeting assessment with:

1. **Overall verdict:** GOOD MEETING, BAD MEETING, or MIXED SIGNALS
2. **Signal strength:** Based on highest commitment currency obtained
3. **Commitment level:** What they actually gave up (or did not)
4. **Anti-patterns detected:** Zombie lead risk, compliment-stall instances
5. **Earlyvangelist score:** How many of the 4 criteria are met
6. **Recommended next step:** What specific commitment to push for in the next interaction, calibrated to your product stage

**Stage-appropriate commitment targets:**

| Product Stage | Appropriate Commitment Ask |
|---------------|---------------------------|
| Problem exploration (no product) | Time: next meeting with specific learning goals. Reputation: intro to others with the same problem. |
| Wireframes or prototype | Time: sit down to review wireframes and give feedback. Reputation: intro to decision maker or technical team. |
| Working product or beta | Time: non-trivial trial period. Reputation: case study or testimonial. Money: letter of intent or pre-order. |
| Live product | Money: purchase, deposit, or pre-order. Reputation: public testimonial. Time: team-wide rollout. |

**WHY:** A meeting without a next step was a pointless meeting. Knowing what to ask for -- calibrated to your stage -- prevents two failure modes: asking for too much too early (scares them off) and asking for too little when you should be closing (creates zombie leads). The goal is always advancement: moving the relationship to the next concrete step in your funnel.

**HANDOFF TO HUMAN:** The agent produces the scored assessment and recommended next steps. The human executes the follow-up in the next conversation.

## Outputs

### Meeting Commitment Assessment Report

Write the report to a file the user specifies, or to `meeting-assessment-{date}.md`:

```markdown
# Meeting Commitment Assessment

## Meeting Details
- **Date:** {date}
- **Prospect:** {name/company}
- **Product stage:** {stage}
- **Meeting type:** {learning / product demo / sales / follow-up}

## Overall Verdict: {GOOD MEETING / BAD MEETING / MIXED SIGNALS}

## Signal Analysis

| Signal | Quote/Action | Currency | Strength | Verdict |
|--------|-------------|----------|----------|---------|
| {signal 1} | "{exact quote}" | {time/reputation/money/none} | {zero/low/medium/high} | {good/bad/mixed} |
| {signal 2} | ... | ... | ... | ... |

## Commitment Level
- **Highest currency obtained:** {none / time / reputation / money / compound}
- **What they gave up:** {specific description}
- **What they did NOT give up:** {what was expected but missing}

## Anti-Pattern Check
- [ ] Zombie lead risk: {yes/no — with evidence}
- [ ] Compliment-stall detected: {yes/no — with evidence}
- [ ] Future-tense promises without current action: {yes/no — with evidence}

## Earlyvangelist Assessment
- [ ] Has the problem: {yes/no/unknown}
- [ ] Knows they have it: {yes/no/unknown}
- [ ] Has budget to solve it: {yes/no/unknown}
- [ ] Already built makeshift solution: {yes/no/unknown}
- **Emotional intensity:** {low / moderate / high}
- **Earlyvangelist likelihood:** {HIGH PRIORITY / POTENTIAL / UNLIKELY}

## Recommended Next Steps
1. **Immediate action:** {what to do within 48 hours}
2. **Next meeting commitment ask:** {specific commitment to request, calibrated to stage}
3. **If they decline:** {what that tells you and how to respond}

## Key Quote
> "{the single most informative quote from the meeting}"
```

## Examples

**Scenario: SaaS founder reviews demo meeting notes**
Trigger: "I just demoed our project management tool to a mid-size agency. They said 'This looks amazing, we'd definitely use this! Let me know when you have the team plan ready.' How did it go?"
Process: Extracted closing statement. Classified "This looks amazing" as compliment (zero currency). Classified "we'd definitely use this" as future-tense promise (zero currency -- most dangerous false positive). Classified "let me know when you have the team plan ready" as compliment-stall (deferring action to unspecified future). No currency exchanged. Detected compliment-stall anti-pattern. Product stage is working product (beta). Checked earlyvangelist criteria: they have the problem (project management pain) and know it, but no evidence of budget or existing workaround.
Output: BAD MEETING. Zero commitment currencies exchanged. Compliment-stall detected. Recommended next step: "Go back and ask for a specific commitment available today. Since you have a working beta, ask them to trial it with one project team for 2 weeks, and to write a brief case study afterward. If they say yes, it's a real lead. If they hesitate, you know where you stand. Do not wait for them to contact you."

**Scenario: Founder evaluates a pipeline of 5 prospects**
Trigger: "I've had meetings with 5 potential customers over the past month. Here are my notes. Which ones are real leads?"
Process: Read all 5 meeting note files. For each prospect, extracted closing statements and classified commitment currencies. Prospect A: gave an intro to their CTO (reputation currency -- GOOD). Prospect B: said "love it, keep me posted" across 3 meetings (compliment-stall, zombie lead -- BAD). Prospect C: asked to buy early access (money currency -- GREAT, earlyvangelist candidate). Prospect D: scheduled a follow-up with specific agenda (time currency -- GOOD). Prospect E: enthusiastic but cancelled the follow-up twice (zombie lead -- BAD).
Output: Pipeline assessment ranking all 5 prospects by commitment strength. Prospect C flagged as earlyvangelist (met all 4 criteria). Prospects B and E flagged as zombie leads with recommendation to force a decision (ask for commitment or accept the rejection). Prospects A and D rated as advancing with recommended next commitment asks.

**Scenario: Pre-product founder assessing problem interviews**
Trigger: "I've been doing problem interviews for my HR analytics idea. One person said 'Oh my god, I spend 3 hours every week manually pulling data from our HRIS into spreadsheets. I even wrote a janky Python script to automate part of it.' Is this a good signal?"
Process: Extracted signal. No commitment currency exchanged yet (this is a learning conversation, not a product meeting). However, identified strong earlyvangelist indicators: has the problem (manual data pulling), knows they have it (quantified at 3 hours/week), and has already cobbled together a makeshift solution (Python script). Budget unknown. Emotional intensity is high (the "Oh my god" opener indicates genuine frustration). No compliment-stall -- this is concrete past behavior, not future promises.
Output: STRONG SIGNAL (even though no commitment was asked for -- this is pre-product stage). This person meets 3 of 4 earlyvangelist criteria. Recommended next step: "In your next conversation with this person, verify budget authority and ask for a time commitment: 'Would you be willing to spend 30 minutes reviewing wireframes when we have a prototype? And could you introduce me to others on your team who deal with this data problem?' These are stage-appropriate asks that test real interest."

## Key Principles

- **Compliments cost nothing, so they are worth nothing** -- A prospect saying "I love it" has given up zero currency. It feels validating but contains no data. The natural human desire to hear praise makes compliments actively dangerous because they feel like progress. Train yourself to hear compliments as warning flags that the prospect may be trying to end the conversation politely.

- **It is not a real lead until you have given them a concrete chance to reject you** -- Zombie leads persist because founders avoid the scary moment of asking for commitment. Rejection is a valid and useful outcome -- it tells you where you stand. No-man's-land (friendly but non-committal) tells you nothing. Always push for a next step or a clear "no."

- **The more they give up, the more seriously you can take their words** -- This is the fundamental measurement principle. Evaluate every signal by asking: what did it cost them to say or do this? A pre-order costs money. An intro to their boss costs reputation. A scheduled follow-up with a specific agenda costs time. "That's cool" costs nothing. Rank signals by cost, not by enthusiasm.

- **Calibrate your ask to your product stage** -- Asking for money when you have no product is premature and counterproductive. Not asking for money when you have a live product is wasteful. Match commitment requests to what is appropriate for your current stage, and escalate as you progress.

- **Meetings either succeed or fail -- there is no "went well"** -- The phrase "the meeting went well" is itself a red flag. Every meeting either produces advancement (a concrete next step with commitment) or it does not. If you leave with only compliments and vague promises, the meeting failed. Acknowledging this honestly is the first step to fixing it.

## References

- For cross-referencing data quality in the same conversation, see the `conversation-data-quality-analyzer` skill
- For synthesizing learnings across multiple meetings into validated/invalidated assumptions, see the `conversation-learning-process` skill
- For the commitment currency taxonomy and meeting outcome scoring rubric, see [references/commitment-currencies.md](references/commitment-currencies.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The Mom Test by Rob Fitzpatrick.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
