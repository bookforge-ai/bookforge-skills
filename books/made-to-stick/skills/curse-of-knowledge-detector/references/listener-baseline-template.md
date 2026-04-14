# Listener Baseline Template

A filled-in template for Step 1 of the skill. The listener baseline is the single most important artifact in the audit — every subsequent flag is scored against it — so this reference gives you a reliable shape and an interview script to fill in missing information.

## Why this template exists

The Curse of Knowledge experiment works because the listener's state of mind is knowable: they literally cannot hear the tune the tapper is hearing. For prose, we have to manufacture that knowability. The listener baseline is the manufactured listener — a written profile that the rest of the audit treats as ground truth.

Without a written baseline, the agent defaults to "generic reasonable reader" and produces generic feedback. The book is explicit: the Curse cannot be cured, only routed around, and the routing requires a specific listener.

## Template

```markdown
## Listener Baseline: {audience short name}

### Role and context
- **Role:** {e.g., "VP of Engineering at a 200-person B2B SaaS company"}
- **Reading context:** {async email / deck in meeting / landing page / onboarding doc}
- **Can they ask follow-up questions?** {yes / no / partial}
- **Time budget for this draft:** {how long they will realistically read before bouncing}

### Vocabulary they KNOW
- {term 1}: {why — e.g., "used daily in their role"}
- {term 2}: {why}
- {term 3}: {why}
...

### Vocabulary they do NOT know
- {term 1}: {why — e.g., "engineering-internal"}
- {term 2}: {why}
- {term 3}: {why}
...

### Processes they understand
- {process 1}: {depth — surface / working / deep}
- {process 2}: {depth}
...

### Processes they do NOT understand
- {process 1}: {why}
- {process 2}: {why}
...

### Prior context they hold
- {thing 1}: {source — e.g., "from previous email in thread"}
- {thing 2}: {source}
...

### Prior context they LACK
- {thing 1}: {what they do not know}
- {thing 2}: {what they do not know}
...

### Emotional/identity stakes
- **What they care about in this decision:** {the reader's actual motivation}
- **What they do NOT care about:** {items authors often assume the reader cares about but does not}
- **Identity frame:** {who they see themselves as when reading — "pragmatic operator", "strategic thinker", "worried parent", etc.}

### What would make this reader stop reading
- {reason 1 — e.g., "any sentence longer than 30 words in paragraph 1"}
- {reason 2}
...
```

## Interview script (when the user provides a thin audience description)

If the user's audience description is too vague to fill out the template, ask THESE questions — one at a time. Do not batch.

1. **"What is this reader's role and seniority?"** (You need the role to infer vocabulary and processes.)

2. **"Pick one: is this reader (a) a subject-matter expert in the same field as the author, (b) an adjacent expert from a related field, (c) an informed non-expert, or (d) a general reader?"** (This single multiple-choice question does most of the work — the four categories have very different jargon tolerances.)

3. **"Name three things the author knows that you are SURE this reader does not know."** (This is the most valuable question. Authors often know the answer immediately and it anchors the whole baseline.)

4. **"Name three things the author thinks this reader cares about that they actually might not."** (Catches the identity / motivation gap that Pass C will use.)

5. **"What decision do you want this reader to make after reading?"** (If the user cannot answer this in one sentence, flag it — the draft has no core, which is a bigger problem than the Curse.)

6. **"Will this reader see the draft in isolation or inside a thread / deck / conversation?"** (Changes what "prior context they hold" can include.)

Stop after question 6 — even if incomplete, you have enough to begin. Note remaining gaps at the top of the report as "assumptions the audit depends on."

## Worked baseline — Example 1

**Draft:** SaaS product announcement for a developer-tools company.
**User's audience description:** "VP of Engineering buyers at mid-market SaaS companies."

### Filled baseline

- **Role:** VP Eng, mid-market B2B SaaS, budget authority, manages 20-80 engineers
- **Reading context:** async email from their AE, probably on phone
- **Can they ask follow-up questions?** Yes but they will not — they will forward or delete
- **Time budget:** 60 seconds for paragraph 1, another 60 if hooked

**Knows:**
- `feature flag` (they have used LaunchDarkly or similar)
- `staging` and `production` environments
- `incident`, `outage`, `postmortem` (from their ops-review meetings)
- `SLA`, `uptime` (from their vendor contracts)

**Does NOT know:**
- `canary` (knows the concept of gradual rollout but not this word)
- `blast radius` (metaphor, not used outside of SRE subculture)
- `idempotent`, `eventual consistency` (they have not coded in 5 years)
- internal product names of the tool vendor

**Processes they understand:** vendor evaluation, budget cycles, incident-response escalation (at a management level, not at the keyboard level).

**Processes they do NOT understand:** the actual rollout mechanism at the code level. They know that engineers "turn features on for some users first" but not how.

**Prior context they hold:** they have heard of the vendor (probably), they know feature-flag tools exist as a category.

**Prior context they LACK:** what `v1` of this product did, what changed in `v2`, who else is using it.

**Cares about:** reducing incidents, team productivity, budget predictability, CVs for their engineers.
**Does NOT care about:** the algorithmic details of the rollout engine, the vendor's engineering-team size.

**Identity frame:** "pragmatic operator" — does not want to look foolish in front of their engineers by buying a toy, but also does not want to debug vendor pitches.

**Would stop reading if:** first paragraph is full of SRE jargon, or if the first sentence is organizational news ("We're excited to announce...").

## Worked baseline — Example 2

**Draft:** Grant application abstract from a social-science research group.
**User's audience description:** "Program officer at an interdisciplinary foundation — probably trained in a different field."

### Filled baseline

- **Role:** Program officer, PhD in some field (probably not this one), reviews ~200 abstracts per cycle
- **Reading context:** batch review, 3-5 minutes per abstract max
- **Can they ask follow-up questions?** No — the abstract is the decision
- **Time budget:** 90 seconds per abstract at the filter stage

**Knows:**
- general academic vocabulary (`hypothesis`, `sample`, `controls`, `significance`)
- how grants work, budget ranges, review criteria
- the foundation's own program areas

**Does NOT know:**
- field-specific named methods (`IRT scaling`, `difference-in-differences`, `fixed effects`)
- field-specific jargon compounds (`non-cognitive skill formation`)
- which researchers in the field are famous

**Cares about:** does this fit our funding priorities, is the team credible, is the method sound enough that our board won't embarrass us.
**Does NOT care about:** methodological novelty for its own sake.

**Identity frame:** gatekeeper who wants to say yes to good work but has to triage hard.

**Would stop reading if:** the first two sentences are pure methods jargon, or if the problem statement does not connect to a human-visible outcome.

## How to use the baseline

Once filled out, the baseline is the left-hand column of every subsequent flag. For each sentence in the draft, the agent asks:

- Pass A: Is every term in this sentence in the "knows vocabulary" list?
- Pass B: Does this sentence reach down to a process or object the reader understands?
- Pass C: Does this sentence depend on prior context the reader holds?
- Pass D: Does this sentence match what the reader actually cares about and identifies with?

If any answer is no, the sentence is a flag, and the rewrite guidance uses the baseline's vocabulary and context to produce a specific fix.
