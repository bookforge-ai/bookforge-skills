---
name: warrant-tester
description: Test the warrants in a research argument — the general principles that connect reasons to claims. Use this skill when a reader might accept a reason as true but still deny it is relevant to the claim, the argument contains a logical leap between a reason and a claim that no stated principle explains, the user needs to decide whether to state a warrant explicitly or leave it implicit, the argument needs to identify which type of warrant is being used (experience-based, authority-based, system/definitional, cultural, methodological) so it can be challenged or defended appropriately, the user is writing for an audience outside their field who will ask "but why does that reason matter to your claim?", a warrant appears to be too broad and needs qualification before it can survive challenge, competing warrants exist and the argument must show why its warrant should prevail, or the user suspects their argument is flawed but cannot identify where — surfacing the implicit warrant often reveals the problem. This skill depends on research-argument-builder (which assembles the full argument structure) and is typically used after reasons and claims have been identified but before final drafting.
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [11]
tags: [research-methodology, academic-writing, argumentation, warrants, logical-reasoning, critical-thinking]
depends-on: [research-argument-builder]
execution:
  tier: 1
  mode: full
  inputs:
    - type: text
      description: "A research argument — at minimum a claim and one or more reasons. The full five-element argument (claim, reasons, evidence, acknowledgment/response, warrant) is ideal but not required."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment; user should have a claim and at least one reason before using this skill"
discovery:
  goal: "Verify that every reason in a research argument is genuinely connected to its claim by an explicit or defensible general principle, and identify where that principle needs to be stated, qualified, or defended"
  tasks:
    - "Surface the implicit warrant connecting each reason to its claim"
    - "Run the five-test validation battery against each warrant"
    - "Classify each warrant by type and identify the appropriate challenge strategy"
    - "Decide whether each warrant must be stated, qualified, or can remain implicit"
    - "Diagnose flawed arguments by revealing the warrant that makes the flaw visible"
  audience: "Researchers, graduate students, analysts, and professionals who have an assembled argument and need to verify that the logical connections between their reasons and claims will survive a careful reader's scrutiny"
  triggers:
    - "User's argument contains a claim and reasons but the connection between them is not obvious"
    - "Reviewer says the reasoning does not follow or the logic is unclear"
    - "User is writing for a general or cross-disciplinary audience who will not share field-specific assumptions"
    - "User needs to challenge someone else's warrant and needs a type-specific strategy"
    - "User suspects their argument is broken but cannot locate the problem"
    - "Argument sounds compelling but a skeptical reader says 'so what?' after hearing the reason"
---

# Warrant Tester

## When to Use

You have a claim and at least one reason. Your reason may be true, well-evidenced, and clearly stated — and a careful reader might still ask: *But how does that follow? Why does that reason matter to your claim?*

That question is asking for a warrant: a general principle that connects the reason to the claim. Warrants are the logical bridges in an argument. They are almost always present, but rarely stated. This skill surfaces them, tests them, and determines what to do with them.

**The core logic of a warrant:**

A warrant has two parts in the form *When X (general circumstance), then Y (general consequence)*. The specific reason must be a valid instance of the general circumstance. The specific claim must be a valid instance of the general consequence. If both fits hold, the argument is logically coherent. If either fit fails, the argument has a structural problem.

Example:

- Claim: "The Russian Federation faces a falling standard of living."
- Reason: "Its birthrate is only 13.2 per 1,000 and life expectancy for men is only about 63 years."
- Implicit warrant: "When a nation's labor force shrinks, its economic future is grim."

A reader who does not share that warrant will accept the reason but deny it is relevant to the claim. Supplying the warrant makes the logic explicit and gives the reader something specific to engage with.

**Preconditions to verify:**

- Does the user have a claim and at least one reason? If not, invoke `research-argument-builder` first to assemble the argument structure.
- Can the user state the claim and each reason in a single sentence? If not, ask them to do so before proceeding — warrant testing requires precise formulations.

**This skill does NOT cover:**

- Assembling the full argument (claim, reasons, evidence, acknowledgment): use `research-argument-builder`
- Generating detailed strategies for each reader objection or counterargument: use `counterargument-handler`

## Context and Input Gathering

### Required (ask if missing)

- **The main claim:** What the argument asserts. A single sentence.
  - Check prompt for: thesis statement, main conclusion, or any disputable assertion
  - If missing, ask: "What is the main claim your argument is trying to establish — the conclusion you want readers to accept?"

- **The reason(s):** Each statement offered in support of the claim.
  - Check prompt for: because-clauses, support statements, or any assertion offered as grounds for the claim
  - If missing, ask: "What are the reasons you are giving for your claim — the statements you use to justify it?"

### Useful (gather from environment if available)

- **Field or discipline:** Determines which warrants readers will take for granted and which need explicit defense
  - If not stated, ask: "What field or research community are you writing for?"

- **Audience expertise level:** Experts share field warrants; non-experts do not
  - Look for audience description in context; if unclear, ask: "Are your readers specialists in this field, or a more general academic audience?"

- **The full argument (if available):** Evidence, acknowledgments, and existing warrants
  - Check for files like `argument.md`, `outline.md`, `draft.md`, or any document containing the assembled argument

## Process

### Step 1 — Surface the Implicit Warrant for Each Reason

**WHY:** Most arguments rely on unstated warrants. Until the warrant is made explicit, it cannot be examined, tested, or defended. Making it explicit also helps the writer see whether the reason and claim are actually connected — which sometimes reveals that they are not, despite appearing to be.

For each reason→claim pair, surface the implicit warrant by completing this template:

> **When** [general circumstance that the reason is an instance of], **then** [general consequence that the claim is an instance of].

Work backward from the specific argument to find the general principle that would make it valid:

1. Identify what *class of thing* the specific reason belongs to (the general circumstance)
2. Identify what *class of outcome* the specific claim belongs to (the general consequence)
3. State the general principle connecting those two classes

**Example — Gun ownership argument:**

- Reason: "Guns were rarely mentioned in wills in the period 1750–1850."
- Claim: "Gun ownership was probably not widespread in early America."
- Implicit warrant: "When a household object considered valuable is not listed in a will, the household likely did not own one."

**Example — Video game argument (flawed):**

- Reason: "Children aged 12–16 today are significantly more violent than their counterparts from a generation ago."
- Claim: "Violent video games are exerting a destructive influence on today's youth."
- Implicit warrant: "When children are constantly exposed to images of sadistic violence, they are influenced for the worse."
- **Problem:** The reason (rising violence) is not a valid instance of the warrant's general circumstance (constant exposure to sadistic violent imagery). The reason does not cover exposure — it only covers an outcome. The warrant cannot connect this reason to this claim.

Surfacing the warrant reveals that the argument needs a new reason: one about *exposure* to violent imagery, not just *outcomes* in terms of behavior.

### Step 2 — Run the Five-Test Validation Battery

**WHY:** Readers challenge warrants in predictable ways. Running these five tests before readers do lets the writer address weaknesses proactively rather than defensively. A warrant that fails any of the five tests requires either qualification, supporting argument, or replacement.

Apply all five tests to each warrant:

---

**Test 1 — Is the warrant reasonable?**

A warrant is reasonable when readers can accept that its general consequence predictably follows from its general circumstance.

- Ask: "Would my readers, if they considered this general principle on its own, find it acceptable?"
- If no: The warrant needs to be argued for — treat it as a claim in its own sub-argument, supported by its own reasons and evidence.

Example: "When a household object considered valuable is not listed in a will, the household likely did not own one" — readers familiar with wills as legal documents will find this reasonable.

---

**Test 2 — Is the warrant sufficiently limited?**

Most warrants are reasonable only within certain limits. An unlimited version invites easy refutation.

- Ask: "Is this warrant stated so broadly that readers can easily find exceptions that would exclude my own case?"
- If too broad: Add qualifying language (*most*, *usually*, *in conditions where X*), then verify the exceptions do not exclude the specific reason and claim at hand.

Example — too broad: "Valuable objects were listed in wills."
Better: "**Most** household objects **considered valuable by their owners** were **usually** listed in wills."

Caution: Once you add qualifiers, you take on an obligation to show the exceptions do not apply to your case. Be precise about what *most* and *usually* mean, and whether guns counted as valuable.

---

**Test 3 — Is the warrant superior to any competing warrants?**

Other researchers may hold warrants that support the opposite conclusion from the same evidence. A warrant that faces no competition is rare; identifying competition and showing why your warrant prevails is part of building a defensible argument.

- Ask: "Is there a competing general principle that would lead a reasonable person to a different conclusion from the same reason?"
- If yes: Either reconcile the competing warrants by limiting both, or argue explicitly for why your warrant prevails.

Example — vaccination mandate debate:
- Warrant A: "When parents believe a medical procedure may harm their children, they have a right to refuse it."
- Warrant B: "When medical decisions concern matters of public health, the state has a right to regulate them."
- Both are reasonable. Reconciliation requires limiting both: Warrant A holds *so long as that does not jeopardize the health of others*; Warrant B holds *so long as the state encroaches as little as possible on parental medical decisions*.

---

**Test 4 — Is the warrant appropriate to this field?**

A warrant that seems reasonable in general may be inadmissible in a specific research community. Field-specific reasoning standards can override common-sense warrants.

- Ask: "Would researchers and reviewers in my field accept this principle as a valid basis for inference, or does my field require a different kind of reasoning?"
- If no: Either find the field-appropriate warrant, or explicitly argue that the field's standard warrant should be updated or supplemented.

Example: Common sense says "When a person is wronged, the law should correct it." In legal reasoning, this warrant has no standing — legal warrants based on precedent and procedure may override it entirely. Law students learn this at their cost.

---

**Test 5 — Does the warrant cover this specific reason and claim?**

Even a reasonable, limited, superior, and field-appropriate warrant fails if the specific reason is not a valid instance of the warrant's general circumstance, or the specific claim is not a valid instance of the warrant's general consequence.

- Ask (circumstance side): "Is my specific reason genuinely an instance of what the warrant's general circumstance describes?"
- Ask (consequence side): "Is my specific claim genuinely an instance of what the warrant's general consequence predicts?"

Example:
- Warrant: "When you are not safe, you should protect yourself."
- Reason: "You live alone."
- Claim: "You should buy a gun."
- Circumstance check: "Living alone" is not obviously an instance of "being unsafe" — this is the gap.
- Consequence check: Even if unsafe, "buying a gun" may not be the only or best instance of "protecting yourself."

If the reason does not fit the circumstance: Revise the reason (or find new evidence) so it becomes a valid instance of the warrant's general circumstance.
If the claim does not fit the consequence: Revise the claim, or find a different warrant whose consequence does cover the claim.

### Step 3 — Classify Each Warrant by Type

**WHY:** The type of warrant determines how it can be challenged and how it should be defended. Applying a challenge strategy designed for one type to a different type wastes effort and often backfires. Knowing the type also helps identify whether the challenge is even winnable — some warrant types are unchallengeable in principle.

| Warrant type | Basis | Examples | Challenge strategy |
|---|---|---|---|
| **Experience-based** | Individual or reported observations | "When people habitually lie, we don't trust them." "When insecticides leach into ecosystems, bird populations fall." | (1) Challenge reliability of the experience or report — difficult; (2) Find counterexamples that cannot be dismissed as special cases |
| **Authority-based** | Expertise, position, or credibility of a source | "When authority X says Y, Y must be so." | Friendly: show the authority lacked full information or exceeds their expertise in this case. Aggressive: argue the source is not a genuine authority at all. |
| **System/definitional** | Formal definitions, principles, or theories (mathematics, biology, law) | "When we add two odd numbers, we get an even one." "When we drive without a license, we commit a misdemeanor." | Facts are largely irrelevant. Either challenge the system itself (very difficult) or show the case does not fall under the warrant's definition. |
| **Cultural** | Common experience of an entire community | "Out of sight, out of mind." "An insult justifies retaliation." | Possible but high resistance — readers experience this as a challenge to their heritage. These warrants change slowly. |
| **Methodological** | Abstract patterns of reasoning | Generalization, analogy, sign | Challenge the application or identify limiting conditions: "Yes, we can analogize X to Y, but not in this respect because..." |

**Methodological warrants in detail:**

- *Generalization:* When every known case of X has quality Y, then all Xs probably have quality Y. Challenge: find a known case that does not have quality Y, or show the sample was not representative.
- *Analogy:* When X is like Y in most respects, then X will be like Y in other respects. Challenge: identify a relevant difference that breaks the analogy.
- *Sign:* When Y regularly occurs before, during, or after X, then Y is a sign of X. Challenge: show that Y and X are correlated but one does not reliably indicate the other.

**Note on warrants based on articles of faith:** Some warrants are beyond rational challenge — they are backed by the certainty of those who espouse them, not by evidence or argument. Do not build a research argument that depends on others accepting such a warrant; and when you encounter them while gathering data, do not treat them as warrants to test. They operate outside the logic of academic argument.

### Step 4 — Decide Whether to State Each Warrant Explicitly

**WHY:** Stating a warrant your readers already accept wastes their time and can appear condescending. Failing to state a warrant your readers need to understand your reasoning — or are likely to challenge — leaves a logical gap that careful readers will exploit. The decision is an audience judgment, not a structural one.

State a warrant explicitly when any of the following apply:

1. **Readers are outside your field.** If you are writing as a specialist for non-specialists, explain how experts in your field draw conclusions — especially if that reasoning is unusual by general standards.

2. **The principle is new or controversial in your field.** If you rely on an unconventional reasoning principle, state and defend it proactively. Cite others in your field who use it. If you cannot, build the argument for it yourself.

3. **Readers will resist the claim because they do not want it to be true.** Lead with a warrant readers can accept *before* laying out the reason and claim they may resist. This does not guarantee acceptance, but it obliges readers to engage rationally rather than emotionally.

Do not state a warrant when:
- Readers are specialists in your field who already take it for granted (stating it appears condescending)
- The warrant is so general and uncontested that every adult accepts it without prompting
- Stating it would slow the argument without adding logical protection

**Ethos implication:** Stating a warrant when your readers need it signals intellectual care and respect. Keeping a warrant implicit when you know readers will ask for it signals overconfidence or evasion. Both choices communicate something about your credibility as a researcher.

### Step 5 — Diagnose and Repair Flawed Arguments Using Warrants

**WHY:** The most common cause of an argument that "feels wrong" but is hard to locate is a reason that does not genuinely connect to the claim. Surfacing the implicit warrant makes the problem visible: the reason is not a valid instance of the warrant's general circumstance, or the claim is not a valid instance of the warrant's general consequence.

**Diagnosis procedure:**

1. State the claim and the reason in one sentence each.
2. Surface the implicit warrant (Step 1).
3. Check whether the reason fits the warrant's circumstance (Step 2, Test 5, circumstance side).
4. Check whether the claim fits the warrant's consequence (Step 2, Test 5, consequence side).
5. Identify which fit fails.

**Repair options:**

| Failure | Repair |
|---|---|
| Reason does not fit warrant's circumstance | Revise the reason to be a valid instance of the circumstance; gather new evidence to support the revised reason |
| Claim does not fit warrant's consequence | Narrow or restate the claim so it is a valid instance of the consequence; or find a different warrant whose consequence does cover the claim |
| Warrant does not survive the five-test battery | Qualify the warrant, argue for it as a sub-claim, replace it, or abandon the reason it was meant to support |
| No warrant can connect this reason to this claim | Discard the reason; find a reason that a defensible warrant can cover |

**Worked example — Video game argument:**

Flawed:
- Reason: "Children 12–16 are significantly more violent than a generation ago."
- Claim: "Violent video games are exerting a destructive influence on today's youth."
- Implicit warrant: "When children are constantly exposed to images of sadistic violence, they are influenced for the worse."
- Failure: The reason (observed rising violence) is not an instance of the warrant's circumstance (exposure to violent imagery). Rising violence is an outcome, not an exposure.

Repaired:
- New reason: "Over the past decade, video games have become a major source of children's exposure to violent imagery."
- Same warrant applies: the new reason is now a valid instance of the warrant's circumstance (exposure to sadistic violent imagery).
- New evidence needed: data showing the proportion of children's screen time spent on violent video games and the nature of that violence.

## Examples

### Example 1 — Historical argument

**Argument:**
- Claim: "Gun ownership was probably not widespread in early America before 1850."
- Reason: "Guns were rarely mentioned in wills filed in seven states between 1750 and 1850."

**Step 1 — Surfaced warrant:** "When valuable household objects were not listed in a will, the household did not own them."

**Five-test battery:**
1. Reasonable? Plausible — wills were legal inventories of valuables. But readers who believe widespread gun ownership was common will resist. Needs supporting argument: Watson (1989) confirmed this practice in Cumberland County wills. [sub-argument needed]
2. Sufficiently limited? The original version allows no exceptions. Qualified: "Most household objects *considered valuable by their owners* were *usually* listed in wills." Now must address: Were guns always considered valuable? What is "usually"?
3. Superior to competing warrants? A competing warrant: "When war was common, most households owned weapons as a matter of survival." This competes. Must argue why the will-listing warrant prevails for this time and place.
4. Field-appropriate? For historical demography — yes. Document-based inference from legal records is standard in this field.
5. Covers this reason and claim? Check: "Guns rarely mentioned in wills" is an instance of "valuable object not listed" only if guns were valuable. Check: "Gun ownership not widespread" is an instance of "household did not own them" at the aggregate level. Both fits hold, but the "valuable" condition is the vulnerability.

**Decision on stating the warrant:** State explicitly — the argument's expected readers (general readers who believe widespread gun ownership was historically common) will not share this principle and will challenge relevance.

---

### Example 2 — Interdisciplinary argument with competing warrants

**Argument:**
- Claim: "The state can require vaccination of children against measles."
- Reason: "When most children are vaccinated, everyone is safer."

**Step 1 — Surfaced warrant:** "When medical decisions concern matters of public health, the state has a right to regulate them."

**Competing warrant:** "When parents believe a medical procedure may harm their children, they have a right to refuse it."

**Test 3 — Competing warrant analysis:** Both are reasonable and backed by defensible principles. Neither can simply be dismissed. Reconciliation: limit both.

- Warrant A limited: "Parents may refuse a medical procedure *so long as that refusal does not jeopardize the health of others.*"
- Warrant B limited: "The state may regulate medical decisions concerning public health *so long as it encroaches as little as possible on parental medical decisions.*"

**Decision on stating:** State the warrant and explicitly acknowledge the competing one — this argument is inherently about competing principles. Stating the reconciliation shows intellectual honesty and invites rational engagement.

---

### Example 3 — Self-diagnosis of a broken argument

**Input from user:** "My argument feels wrong but I cannot find the problem. I'm arguing that social media should be regulated, because teenagers are anxious today."

**Step 1 — Surfaced warrant:** "When teenagers are anxious, social media is harming them."

**Test 5 — Coverage check:**
- Circumstance side: "Teenagers are anxious today" — is this an instance of "social media is harming them"? No. Anxiety is an outcome, not an instance of harm *by social media*. The reason does not fit the warrant's circumstance.
- This is the flaw: rising anxiety does not logically implicate social media without a reason that specifically connects the two.

**Repair:** Revise the reason to: "Teenagers who spend more than three hours daily on social media report significantly higher anxiety rates than those who spend less than one hour." This reason is now an instance of the warrant's circumstance (harm from social media use). Gather evidence: longitudinal survey data showing the correlation with exposure to social media specifically, not screens in general.

## Output

For each reason→claim pair, produce:

1. **Warrant statement:** The general principle in *When X, then Y* form
2. **Five-test results:** Pass/fail for each test, with the specific issue named if it fails
3. **Warrant type:** Classified from the taxonomy in Step 3
4. **Challenge strategy:** The type-specific approach a skeptical reader would use
5. **State or leave implicit?** Decision based on Step 4, with the reasoning stated
6. **Repair instructions (if needed):** Specific changes to the reason, claim, or warrant, with what new evidence is required

If the argument has multiple reasons: process each separately, then note whether the warranted reasons together constitute a sufficient case for the claim.

## Anti-Pattern Quick Reference

| Anti-pattern | Signal | Fix |
|---|---|---|
| Reason stated but not connected | Reader says "so what?" or "why does that matter?" | Surface and state the implicit warrant |
| Warrant too broad | A single obvious exception invalidates the entire argument | Add qualifiers (*most*, *usually*, *in cases where X*) and address whether exceptions exclude your case |
| Reason does not fit warrant's circumstance | Reason describes an outcome but warrant requires an exposure or condition | Revise the reason to be a valid instance of the warrant's circumstance |
| Competing warrant ignored | Opponent uses same evidence to reach opposite conclusion | Limit both warrants explicitly; argue for why yours prevails in this context |
| Field-inappropriate warrant | Reviewer rejects the reasoning principle, not the data | Identify the field's accepted warrant and use it; or explicitly argue for updating the field's reasoning standard |
| Faith-based warrant in a research argument | Warrant cannot be challenged because it rests on certainty, not evidence | Do not build a research argument on such a warrant; find an evidence-based principle or revise the argument |
| Unstated warrant for a skeptical audience | Argument sounds valid to the writer but not to the reader | Identify the audience's knowledge level and state the warrant that bridges the gap |

## References

- `references/warrant-types-and-challenge-strategies.md` — Full taxonomy of warrant types with worked examples and type-specific challenge strategies
- `references/five-test-battery-guide.md` — Detailed guidance on each of the five validation tests with cross-field examples and common failure modes
