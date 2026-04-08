---
name: black-swan-discovery
description: |
  Identify the hidden unknowns that will determine whether your negotiation succeeds or fails before you ever make an offer. Use when someone asks "why is my counterpart acting irrationally?", "why does this deal keep stalling for no apparent reason?", "what am I missing about this negotiation?", "how do I find out what the other side really wants?", or "why won't they just say yes when the deal is clearly good for them?" Also use for: diagnosing a stalled sales cycle where the prospect keeps deflecting, investigating why a candidate rejected an offer that seemed strong, uncovering hidden constraints before entering a high-stakes contract renegotiation, mapping leverage before a complex partnership discussion, or rebuilding a broken negotiation relationship. Produces a black-swan-report.md with a hypothesis map of unknown unknowns in all three categories (worldview mismatches, hidden constraints, hidden agendas), a leverage inventory across all three leverage types, and a prioritized bank of investigation questions to surface what you do not yet know. Pair with counterpart-style-profiler (to refine worldview hypotheses by type) and calibrated-questions-planner (to convert investigation questions into a deployment-ready set).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/black-swan-discovery
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [5, 10]
tags: [negotiation, black-swan, unknown-unknowns, leverage, hidden-constraints, hidden-agendas, worldview, loss-aversion, irrational-behavior, discovery, deal-diagnosis, pre-negotiation]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Deal history — what has been offered, what responses have been received, what has stalled or confused you"
    - type: document
      description: "Counterpart behavior observations — anything that seemed irrational, inconsistent, or unexpectedly emotional"
    - type: document
      description: "Stakeholder map (if available) — who else may be involved in or affected by the decision"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works with pasted deal summaries or document files. Richer context produces more targeted hypotheses."
discovery:
  goal: "Produce a black-swan-report.md that maps hypothesized unknown unknowns across three categories, inventories available leverage, and generates a prioritized question bank to surface the hidden information that is blocking the deal"
  tasks:
    - "Gather deal history, counterpart behavior observations, and stakeholder context"
    - "Diagnose potential unknown unknowns in all three Black Swan categories"
    - "Flag any irrational or contradictory behavior as a diagnostic signal"
    - "Map available leverage across all three leverage types"
    - "Generate 6-10 investigation questions targeting the highest-priority unknowns"
    - "Produce the black-swan-report.md artifact"
  audience: "salespeople, founders, managers, consultants — anyone stuck in a negotiation that is not moving for reasons they cannot explain"
  when_to_use: "When a negotiation is stalling, when counterpart behavior seems irrational, or when preparing for a high-stakes deal where the full picture is unclear"
  environment: "Document set (deal-history.md, counterpart-observations.md) or free-text description"
  quality: placeholder
---

# Black Swan Discovery

## When to Use

You are in a negotiation that is not moving the way it should. The deal looks reasonable on paper, but the counterpart keeps deflecting, delaying, or saying no without a clear explanation. Or you are preparing for a high-stakes negotiation and you suspect there is important information you do not have.

This skill applies when:

- A prospect or counterpart is behaving in ways that seem irrational — rejecting good offers, raising unrelated objections, going silent, or escalating without explanation
- A deal has stalled and you cannot diagnose why
- You are entering a negotiation where the counterpart's real priorities, constraints, or motivations are unclear
- You have received a surprising no after what felt like a strong offer
- You want to map what leverage you actually have before making your next move
- You are rebuilding a previously failed or contentious negotiation

The core principle: **apparent irrationality is almost always a signal, not a fact.** When a counterpart behaves in ways that do not make sense given what you know, they are usually operating on information, constraints, or motivations you do not yet have. The goal of this skill is to surface those unknown unknowns — called "Black Swans" in negotiation practice — so you can address them directly rather than responding to symptoms.

**Black Swans are unknown unknowns — pieces of information whose existence you are not even aware of.** This is different from known unknowns (questions you know you need to answer). A known unknown is "I don't know what their budget is" — you can ask about it directly. An unknown unknown is an undisclosed constraint, hidden relationship, or worldview difference that you do not yet know to ask about. Known unknowns can be resolved with direct questions. Unknown unknowns require a fundamentally different approach: instead of asking about what you know you don't know, you create conditions for unexpected information to surface — through face time, active listening, and watching for behaviors that don't make sense under your current model. These are the deal-killers that blindside experienced negotiators who are otherwise well-prepared.

Before starting, confirm you have:
- A description of the negotiation situation and what you want
- At least some observation of counterpart behavior — ideally including something that seemed puzzling or out of proportion
- A rough sense of who else might be involved beyond the person you are talking to

---

## Context & Input Gathering

### Required Context

- **The deal:** What is being negotiated? What have you offered? What has the counterpart said?
- **The gap:** What is preventing agreement? What does the counterpart say when they do not move?
- **The confusion:** What behavior or response surprised or puzzled you?

### Observable Context

If documents are provided, read them for:
- Inconsistencies between what the counterpart says they want and how they respond to offers that give it to them
- Unexpected escalation, emotion, or energy — positive or negative — around specific topics
- Statements that reveal unstated assumptions ("We'd never do that" without explaining why)
- Evidence of other stakeholders or decision-makers referenced but not introduced
- Deadlines, budget cycles, reporting relationships, or organizational constraints mentioned in passing
- Prior failed deals or contentious history that might be shaping the counterpart's current behavior

### Default Assumptions

- If no behavior observations are provided → assume some form of stall or deflection is occurring (most common Black Swan signal)
- If no stakeholder map is provided → assume at least one undisclosed stakeholder exists (boss, board, partner, budget owner)
- If the deal is described as "going well" with no confusion → treat this skill as pre-emptive mapping rather than diagnosis

### Sufficiency Check

Before generating the report, confirm you can answer: "What is the most puzzling or inexplicable thing this counterpart has done?" If there is nothing puzzling, you may still run the skill as a prevention exercise. If there is something puzzling, that specific behavior is your primary entry point for hypothesis generation.

---

## Process

### Step 1: Audit for Irrational Behavior Signals

**ACTION:** Review the deal history and behavior observations. Flag every instance where the counterpart's behavior seems disproportionate, inconsistent, or unexplainable given what you know.

**WHY:** Irrational behavior is not a dead end — it is the most reliable diagnostic signal in negotiation. When a counterpart acts in ways that do not serve their apparent interests, they are almost always responding to information you do not have. The common error is to dismiss unexplained behavior as personality, stubbornness, or bad faith. Skilled negotiators treat every instance of apparent irrationality as a question: "What would they have to believe or be constrained by for this behavior to make sense?" That reframe is what makes Black Swan discovery possible. Without this audit step, the hypotheses generated in Step 2 will be generic rather than targeted.

**Flag as signals:**
- Rejecting an offer that clearly meets their stated criteria
- Sudden escalation or emotional reaction to a neutral proposal
- Agreeing in conversation but not following through with action
- Deflecting or delaying on one specific issue while being cooperative on others
- Introducing new objections after previous objections have been resolved
- Expressing concern about something seemingly unrelated to the stated deal terms

---

### Step 2: Generate Hypotheses Across All Three Black Swan Categories

**ACTION:** For each flagged signal (and proactively if no signals are present), generate at least one hypothesis in each of the three categories below. Write each hypothesis as a testable statement.

**WHY:** Most negotiators mentally default to looking for one type of explanation — usually "they're being difficult" or "their budget is the constraint." The three-category framework forces you to search in places you would not naturally look. Worldview mismatches are invisible to both parties until one of them names them. Hidden constraints are rarely disclosed voluntarily. Hidden agendas are almost never mentioned because they are often embarrassing or politically sensitive. Generating hypotheses in all three categories is what makes the investigation comprehensive rather than confirmation-seeking.

#### Category 1: Worldview Mismatch

The counterpart is operating from fundamentally different assumptions about the situation — its context, norms, or what a "good outcome" looks like. Neither party is necessarily wrong; they are working from different maps of the same territory.

**Diagnostic signals:** Confusion when you state something you consider obvious; strong reactions to framing that seems neutral to you; repeated return to a principle or concern that seems disconnected from the specific deal terms; reluctance to engage with options that are standard in your context.

**Example hypotheses:**
- "They may believe this type of deal normally works differently and our structure looks unusual or suspicious to them."
- "They may have a fundamentally different risk tolerance than we do, shaped by a prior experience we don't know about."
- "They may define success for this negotiation in terms we have not heard — reputation, precedent-setting, relationship signal — not just the financial terms."

#### Category 2: Hidden Constraints

The counterpart cannot agree due to a constraint they have not disclosed — budget, timing, authority, process, or external dependency. They often will not disclose it voluntarily because it feels embarrassing, risky, or irrelevant to them.

**Diagnostic signals:** Stalls that coincide with organizational events (quarter end, budget cycle, leadership change); escalation to someone new in the conversation without explanation; requests for time that seem unrelated to the complexity of the decision; reluctance to commit on a specific dimension (price, timeline, scope) even when others are resolved.

**Example hypotheses:**
- "They may not have approval authority for this deal size and cannot admit it without losing face."
- "They may have a budget constraint that resets at a specific date, making timing the real variable."
- "They may be waiting on an internal decision that is blocking this one — a reorg, a competing priority, a budget freeze."
- "The actual decision-maker may not be the person we are talking to, and that person has not been brought into the conversation."

#### Category 3: Hidden Agenda

The counterpart has a goal, interest, or priority unrelated to (or only partially related to) the stated deal — one they are not disclosing because it is politically sensitive, personally motivated, or awkward to raise directly.

**Diagnostic signals:** Interest in elements of the deal that seem peripheral to their stated goal; unusual energy around non-financial terms; resistance to transparency or documentation that would be neutral in a straightforward deal; behavior that serves their personal position rather than their organization's interest; references to internal relationships or politics without elaboration.

**Example hypotheses:**
- "They may need this deal to succeed for personal career reasons — being seen as the person who closed it — and our current structure does not give them that."
- "They may be in conflict with an internal stakeholder and closing this deal would shift internal power in a way they want or fear."
- "They may need to demonstrate to their organization that they pushed back hard, regardless of the outcome — the negotiation itself is part of their deliverable."
- "There may be a competing relationship they are protecting — a vendor, a partner, a colleague — that this deal would threaten."

---

### Step 3: Map Available Leverage

**ACTION:** For each credible hypothesis from Step 2, identify which type of leverage is most relevant and what form it takes in this specific situation.

**WHY:** Leverage is not a fixed property of the deal — it is relative to what the counterpart values and fears. The same negotiation can contain all three leverage types simultaneously, but they apply to different counterpart concerns. Mapping leverage before deploying it prevents the most common error: using the wrong type of leverage for the counterpart's actual situation. Using negative leverage on a counterpart who is constrained by a hidden agenda (not by fear of loss) is ineffective and damages the relationship. Using normative leverage on a counterpart who has a genuine financial constraint is similarly ineffective.

#### Leverage Type 1: Positive Leverage

The counterpart wants something you can provide that they cannot easily get elsewhere. This is leverage you have when the deal is genuinely attractive to them.

**Activation condition:** The counterpart has demonstrated genuine interest in the outcome, not just in the negotiation process.

**Forms:** Your product/service/offer is differentiated; you have unique access, timing, or relationship value; the deal solves a specific problem they have urgency around.

**Application:** Use positive leverage to reinforce the value of moving forward — frame what they stand to gain if the deal closes. Most effective when combined with a concrete deadline or alternative that makes the opportunity feel limited.

#### Leverage Type 2: Negative Leverage

The counterpart fears what happens if the deal does not close — loss of the opportunity, loss of face, a worse outcome with an alternative. This is leverage based on what they stand to lose.

**Activation condition:** The counterpart has a real and recognized downside from a failed deal — not hypothetical.

**Forms:** A genuine alternative offer or option you can pursue; a time constraint that makes delay costly for them; the cost of the status quo (not closing this deal means the problem continues).

**Application:** Use sparingly and indirectly. Stating negative leverage explicitly often reads as a threat and triggers defensiveness. Instead, frame it as sharing your own constraints: "I need to make a decision by Friday on whether to go in a different direction."

**Loss aversion principle (Kahneman & Tversky):** Negative leverage is disproportionately powerful because of loss aversion — the psychological principle that losses are felt roughly twice as intensely as equivalent gains. A $100K loss stings twice as much as a $100K gain satisfies. This means implied negative consequences (what they stand to lose) carry twice the motivational weight of equivalent positive offers (what they stand to gain). "You stand to lose the early pricing" activates more urgency than "You can lock in the lower rate." Frame negative leverage as consequences, not threats: "It seems like if this doesn't work out, the pilot investment would be difficult to justify internally." Use this asymmetry deliberately when the counterpart is not moving on a deal that serves their interests — but only when the counterpart already recognizes the loss as real.

#### Leverage Type 3: Normative Leverage

The counterpart has stated standards, values, or commitments that their proposed behavior contradicts. This leverage uses the gap between their stated principles and their actions.

**Activation condition:** The counterpart has made statements — about fairness, their organization's values, how they treat partners, what their word means — that their current position violates.

**Forms:** Prior commitments ("In our last call you said that X was important to you — how does this decision align with that?"); organizational stated values; professional norms in their industry; precedents they themselves set in prior deals.

**Application:** Frame the discrepancy as a genuine question, not an accusation. "Help me understand how this fits with what you told me about your process" invites reflection without triggering defensiveness. This leverage type often works on hidden agenda situations because it surfaces the gap between the counterpart's public position and their private motivation.

---

### Step 4: Design the Investigation Question Bank

**ACTION:** For each high-priority hypothesis (focus on 3-5), write 1-2 calibrated investigation questions designed to surface that specific unknown without triggering defensiveness.

**WHY:** The purpose of the investigation questions is not to confirm your hypotheses — it is to create space for information you do not have to emerge. Hypotheses are starting points, not conclusions. The questions must be open (How/What, not Why or Yes/No), must convey genuine curiosity rather than accusation, and must be structured so that any answer — including "that's not it" — gives you useful information. Closed questions (Did you have approval? Is budget the issue?) allow the counterpart to shut the inquiry down with a simple denial. Open questions require elaboration that reveals the underlying reality whether or not the specific hypothesis was correct.

**Question design rules:**
- Start with How or What — never Why (reads as accusatory)
- Express genuine curiosity, not challenge: "Help me understand..." or "What would it take for..."
- Target one hypothesis per question
- After asking, use a label to create space: "It seems like there might be more to this."
- Sequence from least sensitive to most sensitive — build trust before surfacing the deepest hypotheses

**Example question bank structure:**

| Hypothesis | Investigation Question | Leverage Type |
|---|---|---|
| Hidden decision authority | "What does the approval process look like from here?" | Constraint |
| Worldview on deal structure | "How does this compare to how you typically structure these arrangements?" | Worldview |
| Personal stake in outcome | "What would success look like for you personally in how this gets resolved?" | Agenda |
| Budget timing constraint | "How does your organization's planning cycle affect timing on decisions like this?" | Constraint |
| Competing internal relationship | "What other considerations are you weighing as you think about this?" | Agenda |

---

### Step 5: Write the Black Swan Report

**ACTION:** Produce the `black-swan-report.md` artifact with the full hypothesis map, leverage inventory, and investigation question bank.

**WHY:** Documenting the hypotheses and leverage map before the next conversation serves two functions. First, it prevents the most dangerous negotiation failure mode: discovering the key unknown unknowns in the middle of the conversation and responding reactively rather than strategically. Second, it forces intellectual honesty — written hypotheses are easier to revise as new information arrives than assumptions held loosely in memory. The report also functions as a brief that can be shared with colleagues or revisited after a conversation to update based on what was learned.

---

## Inputs

| Input | Required | Format |
|---|---|---|
| Deal description | Yes | Any — markdown, plain text, verbal summary |
| What you want from the negotiation | Yes | One sentence minimum |
| Counterpart description | Yes | Role, organization, relationship history |
| Counterpart behavior observations | Yes | What has happened, what has been puzzling |
| Prior offers and responses | Optional | Summary or transcript |
| Stakeholder map | Optional | Who else is involved or affected |
| Counterpart profile | Optional | Output from counterpart-style-profiler |

---

## Outputs

Produce `black-swan-report.md` with the following structure:

```markdown
# Black Swan Report

**Deal:** [One-sentence description of what is being negotiated]
**Counterpart:** [Who they are, role, organization]
**Status:** [Current state — stalled, progressing, first contact, etc.]
**Primary Signal:** [The most puzzling or inexplicable behavior observed]

---

## Irrational Behavior Signals

| Behavior | Why It Seems Irrational | What It Might Signal |
|---|---|---|
| [Specific observed behavior] | [Why it doesn't fit their stated interests] | [Category — worldview / constraint / agenda] |

---

## Black Swan Hypotheses

### Category 1: Worldview Mismatches

- **Hypothesis 1a:** [What assumption mismatch might explain the observed behavior?]
  - *Signal it would explain:* [Which behavior]
  - *How to test:* [Observation or question that would confirm/disconfirm]

- **Hypothesis 1b:** [Alternative worldview hypothesis]

### Category 2: Hidden Constraints

- **Hypothesis 2a:** [What constraint might they not be disclosing?]
  - *Signal it would explain:* [Which behavior]
  - *How to test:* [Question or timing observation]

- **Hypothesis 2b:** [Alternative constraint hypothesis]

### Category 3: Hidden Agendas

- **Hypothesis 3a:** [What personal or political motivation might be at play?]
  - *Signal it would explain:* [Which behavior]
  - *How to test:* [Observation or indirect question]

---

## Leverage Inventory

| Leverage Type | What You Have | Activation Condition | Risk |
|---|---|---|---|
| Positive | [What they want that you can provide] | [When it applies] | [What could undermine it] |
| Negative | [What they stand to lose if this fails] | [When it's real, not hypothetical] | [Overuse = threat = defensiveness] |
| Normative | [What they've said that their current behavior contradicts] | [Specific prior statements or values] | [Must be framed as question, not accusation] |

---

## Investigation Question Bank

**Priority questions (next conversation):**

1. [Most important — targets highest-priority hypothesis]
   *WHY this question:* [What unknown it surfaces]
   *Follow with:* [Label to create space for elaboration]

2. [Second priority question]
   *WHY this question:* [What unknown it surfaces]

3. [Third priority question]
   *WHY this question:* [What unknown it surfaces]

**Secondary questions (if time or if primary questions open new threads):**

4. [Question targeting secondary hypothesis]
5. [Question targeting normative leverage opportunity]

---

## Discovery Strategy

**What to do before the next conversation:**
- [Specific preparation step — research, stakeholder outreach, leverage validation]

**What to observe in the next conversation:**
- [Specific signal that would confirm or disconfirm a key hypothesis]

**If the primary hypothesis is confirmed:**
- [How to address it — acknowledge the constraint, reframe the offer, introduce normative leverage]

**If the primary hypothesis is wrong:**
- [What to look for next — which secondary hypothesis becomes more likely]
```

---

## Key Principles

- **Irrational behavior is always a signal, never a conclusion.** When your counterpart acts in ways that do not serve their stated interests, the correct response is "What am I missing?" not "They're being unreasonable." Almost every instance of apparent irrationality is a window into information you do not yet have.

  *WHY:* People do not generally act against their own interests. When behavior looks irrational from your perspective, the most likely explanation is that you are missing context — a constraint, a belief, a relationship, a fear — that makes the behavior internally consistent. Dismissing the behavior as "crazy" closes off the inquiry. Treating it as a signal keeps it open.

- **Unknown unknowns are not the same as known unknowns.** A known unknown is something you know you don't know ("I don't know their budget"). An unknown unknown is something you don't know you don't know. Black Swans are the second type — which is why they require active hypothesizing, not just direct questions about the things you already know to ask about.

  *WHY:* Known unknowns can be addressed with direct questions. Unknown unknowns cannot be directly asked about because you do not yet know they exist. This is why the three-category hypothesis framework exists: it forces you to search in categories (worldview, constraints, agendas) where information is systematically undisclosed rather than merely unknown.

- **Face time surfaces what documents do not.** The most important Black Swans are rarely discoverable through written communication. They emerge in body language, pauses, inconsistencies between tone and content, and the emotional energy around specific topics. This is why high-stakes negotiations require in-person or video time — not just more email.

  *WHY:* Written communication is filtered. People edit their words before sending. In real-time conversation, especially face-to-face, the emotional and nonverbal signals that reveal hidden constraints and agendas are much harder to suppress. The counterpart who writes a completely neutral email often reveals in the first thirty seconds of a call that something else is going on.

- **Loss aversion is approximately 2x as powerful as equivalent gain.** When designing leverage or framing choices for your counterpart, a potential loss activates approximately twice the urgency of an equivalent potential gain. Use this asymmetry deliberately, not manipulatively — frame the real cost of inaction rather than fabricating artificial urgency.

  *WHY:* Prospect theory (Kahneman and Tversky) demonstrates that the psychological pain of losing something is roughly twice the pleasure of gaining the equivalent. In negotiation, this means "you might lose the early pricing by waiting" is approximately twice as motivating as "you can save money by deciding now." Both statements can be true simultaneously — the framing determines which motivational system you are activating.

- **All three leverage types apply simultaneously.** Most negotiators think in terms of one dominant leverage type. In reality, most negotiations contain all three, applying to different counterpart concerns. Mapping all three before the conversation lets you choose the right tool for the specific hypothesis you are investigating.

  *WHY:* Using negative leverage on a counterpart who has a hidden agenda (not a fear of loss) is ineffective and often damages the relationship. The right leverage type for each situation depends on what the counterpart actually cares about — which is only discoverable through the hypothesis and investigation process.

- **Normative leverage is almost always available.** Every counterpart has stated values, prior commitments, and professional standards. Surfacing a gap between those statements and their current behavior — framed as a genuine question — is one of the most powerful and least adversarial ways to create movement. It requires the counterpart to reconcile their stated principles with their actions.

  *WHY:* People are strongly motivated to maintain consistency between their stated values and their behavior (consistency bias). When a counterpart's behavior contradicts something they have said — about fairness, process, their organization's standards — gently surfacing that discrepancy creates internal pressure to resolve it. This does not require any threat or external pressure; the inconsistency itself creates the leverage.

---

## Examples

### Example 1: The Korean MBA Student and the Ex-Boss

**Scenario:** A Korean MBA student needs a letter of recommendation from a former employer who has become distant and difficult to reach. The student cannot understand why the ex-boss is unresponsive. The relationship had been positive during employment.

**Trigger:** "My former boss agreed to write a recommendation but keeps delaying. We haven't worked together in two years. I can't figure out what's going on."

**Process:**
- Signal audit: Agreement followed by prolonged inaction despite reminders. Behavior is inconsistent with a simple yes.
- Category 1 hypothesis: The ex-boss may assume that helping a former employee makes sense only if the relationship has ongoing value — a networking norm the student has not activated.
- Category 2 hypothesis: The ex-boss may have a time constraint (travel, project deadline) that they are too embarrassed to name after already agreeing.
- Category 3 hypothesis (discovered via investigation): The ex-boss may need something in return — specifically, a connection to the MBA program's network or a way to be associated with the student's future success. The letter is not just a favor; it is an implicit exchange the student has not acknowledged.

**Black Swans discovered:** (1) Worldview mismatch — the ex-boss operates on implicit reciprocity norms the student has not addressed; (2) Hidden agenda — the ex-boss wants to be positioned as a champion in the MBA community, not just a reference provider. When the student acknowledged both (offered to introduce the ex-boss to program contacts and framed the letter as a mutual professional visibility opportunity), the letter arrived within a week.

**Key leverage deployed:** Normative (the ex-boss had agreed and his professional reputation as a mentor was at stake) and Positive (access to MBA network contacts).

---

### Example 2: Stalled Enterprise Sales Deal

**Scenario:** A SaaS company's sales rep has been in a six-month sales cycle with a VP of Operations at a mid-size logistics company. The deal has gone through legal review, the technical evaluation was positive, and the VP has expressed enthusiasm in every conversation. But the final approval keeps getting pushed.

**Trigger:** "This deal should have closed three months ago. The champion loves the product, legal is done, pricing is agreed. Every time I ask about timing, she says 'soon' but nothing happens."

**Process:**
- Signal audit: Sustained enthusiasm combined with inability to execute. Gap between stated support and ability to close. Timing questions deflected with vague answers.
- Category 2 hypothesis (highest priority): Hidden budget constraint — the VP may not have authorization for this deal size and has been hoping to resolve that internally without disclosing it.
- Category 2 secondary hypothesis: There is a competing internal priority consuming the executive sponsor's attention and political capital.
- Category 3 hypothesis: The VP needs visible executive buy-in from her own boss before committing — either for political protection or because the actual decision-maker is above her.

**Investigation questions designed:**
1. "What does the approval process look like from here on your end?" (surfaces authority constraint without accusation)
2. "What would need to be true for this to move in the next thirty days?" (opens space for constraint disclosure)
3. "Who else in your organization would want to weigh in on a decision like this?" (surfaces undisclosed stakeholder)

**Outcome:** Question 3 revealed a CFO who had budget veto authority and had not been introduced into the process. The VP had been trying to shield the deal from CFO scrutiny but could not close without his approval. Once the sales rep offered to support the VP in presenting the ROI case to the CFO directly, the deal closed within three weeks.

---

### Example 3: Partnership Negotiation Breakdown

**Scenario:** A startup founder is negotiating a distribution partnership with a larger company. Initial conversations were extremely positive, but after a terms sheet was sent, communication became formal and slow. The other party's lead negotiator has been replaced by someone the founder has never met.

**Trigger:** "Everything was going great, then we sent the terms and it all went cold. Now there's a new person involved who seems hostile for no reason. I don't understand what changed."

**Process:**
- Signal audit: Sudden shift from warmth to formality after terms were sent; personnel change; new representative displays hostility without stated cause.
- Category 1 hypothesis: The terms sheet may have violated an unstated norm in how the other company handles formal proposals — perhaps they expected a different structure, or the founder went around the appropriate channel.
- Category 3 hypothesis (highest priority): The original champion may have been moved off the deal for internal reasons, and the new representative has a mandate or a personal motivation to renegotiate from a lower position.
- Category 3 secondary: The new representative may have been assigned specifically because the deal was seen internally as unfavorable, and the warmth in early conversations was not accurately representing the other organization's actual position.

**Leverage mapped:**
- Positive: Limited — the deal terms are now under review and the new representative has not expressed the same enthusiasm.
- Normative: High — the prior representative made specific positive statements about deal structure that are on record. The new representative is bound by what was discussed.
- Negative: Moderate — the startup has alternative distribution options that can be made more visible.

**Investigation questions designed:**
1. "Help me understand how this differs from what you typically look for in a partnership arrangement." (tests worldview mismatch)
2. "What are the most important factors for your team in how this is structured?" (resets the conversation to their priorities without the previous framing)
3. "What would make this work better from your perspective?" (opens space for the new representative to state their actual mandate)

---

## References

- [references/black-swan-categories.md](references/black-swan-categories.md) — Extended diagnostic signals per category, with real-world examples across sales, employment, and partnership negotiations
- [references/leverage-types-guide.md](references/leverage-types-guide.md) — Detailed activation conditions, risk profiles, and combination strategies for all three leverage types
- [references/loss-aversion-framing.md](references/loss-aversion-framing.md) — Prospect theory background, framing formulas, the 2x rule application in negotiation contexts
- [references/face-time-tactics.md](references/face-time-tactics.md) — How to extract Black Swan information in live conversation: observation checklist, contradiction signals, emotional energy mapping
- [references/investigation-question-templates.md](references/investigation-question-templates.md) — 20 ready-to-use investigation questions across all three categories with situation-specific variants

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
