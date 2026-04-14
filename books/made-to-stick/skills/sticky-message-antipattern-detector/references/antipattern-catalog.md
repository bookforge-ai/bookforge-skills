# Sticky Message Anti-Pattern Catalog

Eight named failure modes that kill stickiness, with detection criteria, book citations, consequences, and fix strategies. Derived from *Made to Stick* (Chip Heath & Dan Heath, 2007). Use this as the deep reference for the `sticky-message-antipattern-detector` skill.

Note: The Curse of Knowledge (the book's "villain") is NOT in this catalog — it is covered by the separate `curse-of-knowledge-detector` skill. This catalog contains the eight secondary named failure modes the Heaths warn against throughout the book.

---

## AP-02 — Burying the Lead

**One-liner:** The most important fact is not in sentence one.

**Detection criteria**
- The first sentence is background, caveats, history, or belief framing — not news.
- The single fact whose loss would gut the piece sits in paragraph 2 or later.
- Test: if forced to delete 90% of the draft, which sentence would you keep? That is the lead. Check if it is currently in position 1.
- Nora Ephron's journalism-teacher test: given "Principal Kenneth Peters announced today that the entire faculty will be attending a seminar on new teaching methods", the real lead is "There will be no school next Thursday".

**Book citation**
- Chapter 1 (Simple) — journalism inverted-pyramid rule, Nora Ephron story, and the Carville "It's the economy, stupid" antidote: Carville had to stop Clinton from burying his own lead when Clinton's instinct was to lead with "balanced budget".
- Epilogue — "The first villain is the natural tendency to bury the lead — to get lost in a sea of information. One of the worst things about knowing a lot, or having access to a lot of information, is that we're tempted to share it all."
- Easy Reference Guide — "Inverted pyramid: Don't bury the lead."

**Consequence**
Readers stop before they reach the lead. Inverted-pyramid violations are silently fatal: the draft looks complete but the audience retains nothing usable.

**Severity rubric**
- High: the lead is in paragraph 3+ or absent entirely; OR the first sentence is pure common-sense framing.
- Medium: the lead is in paragraph 2.
- Low: the lead is in sentence 2–3 of the first paragraph.

**Fix strategy**
Promote the buried sentence to position 1. Demote or delete the prior content. If the lead does not exist in the draft at all, the user must first extract it (Commander's Intent: the single sentence the piece must convey if everything else is lost).

---

## AP-03 — Decision Paralysis

**One-liner:** Multiple co-equal "top priorities" with no hierarchy cause the audience to freeze, defer, or pick nothing.

**Detection criteria**
- Count sentences claiming "the most important", "our top priority", "the key thing", "what matters most". More than one = flag.
- Co-equal lists of 5+ priorities presented without a designated single core.
- Test: ask "if the audience could only act on one of these, which should it be?" If the draft does not answer, it is paralysis.

**Book citation**
- Chapter 1 (Simple) — Decision Paralysis: "Why is prioritizing so difficult? Because what if we can't tell what's 'critical' and what's 'beneficial'? ... people can be driven to irrational decisions by too much complexity and uncertainty."
- Iyengar jam study (Chapter 1 & Notes): 24 flavors produced ~3% purchase; 6 flavors produced ~30% purchase — 10x difference from reducing the option set.
- Redelmeier-Shafir doctor study (Notes): doctors delayed prescribing any treatment when forced to choose among multiple equally good drugs.
- Epilogue — Jeff Hawkins's Palm team freezing on features; "students who missed both a fantastic lecture and a great film because they couldn't decide which one was better".
- Easy Reference Guide — "Beat decision paralysis through relentless prioritization: 'It's the economy, stupid.'"

**Consequence**
Audience takes no action. Worse, they may discount the piece entirely because the lack of priority signals low author confidence.

**Severity rubric**
- High: 3+ co-equal "top" claims, OR the paralysis is in an action-requesting piece (CTA, fundraising, product decision).
- Medium: exactly 2 co-equal "top" claims.
- Low: paralysis is in decorative content (values page, about section).

**Fix strategy**
Force a single core (Commander's Intent). Demote the rest to supporting evidence OR cut them. If the user cannot pick, ask a disambiguating question: "If your audience remembered exactly ONE thing from this, what would it be?"

---

## AP-04 — Common-Sense Trap

**One-liner:** The message says what every reader already believes — so nothing is encoded to memory.

**Detection criteria**
- Scan for claims the audience (per the belief baseline) would nod at BEFORE reading.
- Tell-tale phrases: "customer service is important", "communication is key", "quality matters", "our people are our greatest asset", "we are committed to excellence", "safety first", "innovation matters", "we care about our customers".
- Advice sections whose advice the audience would already give.
- The Nordstrom test (Epilogue): an uncommon-sense claim breaks the reader's schema. "Nordies gift-wrap packages from Macy's" sticks because it breaks the schema of what a store does.

**Book citation**
- Chapter 2 (Unexpected) — "Common sense is the enemy of sticky messages. When messages sound like common sense, they breeze right through the brain." The reader's guessing machine is not broken, so nothing is encoded.
- Chapter 6 (Emotional clinic) — "Notice that there's nothing unexpected here — nothing that is uncommon sense. ... Most of the advice ... is both too abstract and too obvious to stick."
- Chapter 2 — the local-news reporter Adams episode: "Names, names, and names" seems like common sense to reporters, but Adams broke their schema by going radically further.
- Epilogue — "Surprise them by breaking their guessing machines — tell them something that is uncommon sense."

**Consequence**
The reader nods, feels agreement, and forgets. Worse than jargon — jargon at least triggers a "huh?" reaction. Common-sense sedation produces zero friction and therefore zero encoding.

**Severity rubric**
- High: the common-sense sentence IS the lead, or dominates the close.
- Medium: common-sense sentences appear in body paragraphs.
- Low: parenthetical or transitional.

**Fix strategy**
Surface the uncommon claim hiding in the material. Ask: "What is the genuinely non-obvious, counter-intuitive thing you believe about this that your audience does not already believe?" Lead with that. Alternatively, cut the common-sense sentence entirely — the draft usually gets stronger, not weaker, when generic sedation is removed.

---

## AP-05 — Semantic Stretch

**One-liner:** Powerful words have been used so broadly they have lost their original distinctive meaning.

**Detection criteria**
- Scan for the stretched-word list (research-backed from Heath & Gould 2005): *unique*, *strategy*, *strategic*, *awesome*, *amazing*, *fantastic*, *great*, *excellent*, *innovative*, *leverage*, *synergy*, *world-class*, *best-in-class*, *relativity* as "it depends", *revolutionary*, *game-changing*, *disruptive*, *seamless*, *powerful*, *intuitive*.
- For each occurrence, check whether the word is carrying its original distinctive meaning in context or whether it has been diluted into a generic positive vibe.
- "Unique" test: is this genuinely one-of-a-kind, or could you substitute "nice" with no loss? If "nice" works, "unique" has been stretched.
- "Strategy" test: does this name a real strategic choice (doing X and not Y), or is it a fancy word for "plan"?

**Book citation**
- Chapter 5 (Emotional) — "Semantic Stretch and the Power of Association".
- Easy Reference Guide — "USE THE POWER OF ASSOCIATION. The need to fight semantic stretch: the diluted meaning of 'relativity' and why 'unique' isn't unique anymore. Transforming 'sportsmanship' into 'honoring the game.'"
- Notes — "Chip Heath and Roger Gould, 'Semantic Stretch in the Marketplace of Ideas,' working paper, Stanford University, 2005... extreme synonyms for the word good (e.g., fantastic or amazing) are increasing in use faster than synonyms that are less extreme."

**Consequence**
Stretched words fail to impress and silently flatten any sentence they touch. Readers' processing discounts them to near-zero; the writer thinks they have packed the sentence with emphasis but has actually delivered a bland neutral.

**Severity rubric**
- High: 3+ stretched words in one paragraph, OR stretched words in the lead/CTA.
- Medium: 1–2 stretched words in body copy.
- Low: stretched words in navigation, metadata, or decorative footer.

**Fix strategy**
Narrow it to a concrete claim. "Our onboarding is 30 minutes, half the category average" beats "we have an awesome onboarding experience". Alternatively, revive the word's original force via a vivid anchor: "honoring the game" replaced "sportsmanship" in youth sports programming because it carried concrete ritual weight. Or cut the word entirely — most sentences tighten when stretched words are removed.

---

## AP-06 — Stats Without Story

**One-liner:** Claims are defended with statistics alone, which are forgotten almost instantly, instead of human-scale anchors or single-person stories.

**Detection criteria**
- Count statistics, percentages, and quantitative claims. For each, check whether it is paired with (a) a named person, (b) a physical analogy ("5,000 nuclear warheads" → "one BB per thousand people in a bucket"), or (c) a concrete scenario.
- Ratio test: bare stats to anchored stats. Worse than 1:1 = flag.
- Load-bearing test: if a stat is the emotional close or core credibility anchor, it MUST be paired. A bare close is always high severity.

**Book citation**
- Chapter 4 (Credible) — "Since grade school, we've been taught to support our arguments with statistical evidence. But statistics tend to be eye-glazing."
- Chapter 4 — 5,000 nuclear warheads anti-example: "The statistic didn't stick. It couldn't possibly stick. No one who saw the demonstration would remember, a week later, that there were 5,000 nuclear warheads in the world. What did stick was the [BBs in bucket demo]."
- Chapter 5 (Emotional) — Rokia / Save the Children study: a letter with statistics about millions of African children raised less than a letter about a single identified child, Rokia. Identifiable-victim effect.
- Epilogue (student-speech recall study) — "In the average one-minute speech, the typical student uses 2.5 statistics. Only one student in ten tells a story... when students are asked to recall the speeches, 63 percent remember the stories. Only 5 percent remember any individual statistic." 63% vs 5% is the foundational ratio.

**Consequence**
Audience recalls nothing quantitative. Worse, stats without story suppress emotional engagement — the reader's analytic mindset is activated, which dampens caring. This is the Mother Teresa effect in reverse: aggregate suffering moves people less than a single identified person.

**Severity rubric**
- High: the bare stat is load-bearing (in the lead, the close, or the primary evidence block).
- Medium: multiple bare stats in body copy.
- Low: decorative stat in a navigation element, footer, or background paragraph.

**Fix strategy**
Three options: (1) wrap the stat in a physical analogy (Human Scale principle — BBs in a bucket, football fields, houses per city block); (2) pair it with a single named person (Rokia, Jared from Subway); (3) cut it if the story can carry the argument alone. The default recommendation is Option 2 if the audience needs to feel, Option 1 if the audience needs to comprehend magnitude, Option 3 if the argument already has a strong narrative.

---

## AP-07 — Abstract Strategy Talk

**One-liner:** Sentences live at the strategy level (synergies, vision, shareholder value) with no concrete observable behavior — readers cannot name what anyone would DO differently tomorrow.

**Detection criteria**
- Classify each sentence as ACTION-level (actor + verb + observable object) or STRATEGY-level (goals, synergies, visions, alignment).
- Flag every strategy-level sentence without an adjacent action-level translation.
- Tell-tale phrases: "maximize shareholder value", "drive outcomes", "align around", "leverage synergies", "operational excellence", "execute our vision", "deliver value", "transform the business", "best-in-class experience", "our North Star is X" (without naming the number).
- Soccer-team test (from Chapter 3, via Stephen Covey): if you were the coach with this as your message, would your players know what to DO on Monday?
- Boeing 727 test: replace the abstract sentence with a concrete constraint ("seat 131 passengers, land on Runway 4-22 under a mile long"). Does the sentence gain or lose meaning? If concrete GAINS meaning, the abstract original is a hit.

**Book citation**
- Introduction — "Mission statements, synergies, strategies, visions — they are often ambiguous to the point of being meaningless. ... Let's take the CEO who announces... 'maximize shareholder value.' Is this idea simple? ... Is it concrete? Not at all."
- Chapter 3 (Concrete) — "Even the most abstract business strategy must eventually show up in the tangible actions of human beings. It's easier to understand those tangible actions than to understand an abstract strategy statement."
- Chapter 3 — Beth Bechky silicon chip study: engineers and manufacturers could not coordinate because they worked at different levels of abstraction. Coordination only happened when both groups walked the concrete chips on the factory floor.
- Chapter 3 — JFK "man on the moon by the end of the decade" contrasted with "maximize shareholder value".

**Consequence**
Grammatical but un-actionable prose. Audience reads, understands the words, and walks away with no behavior change. Cross-functional teams cannot coordinate because abstract language hides the concrete work each side must do.

**Severity rubric**
- High: entire draft lives at strategy level with no action-level translation.
- Medium: mixed, but the lead and close are strategy-only.
- Low: occasional strategy-level sentences in a mostly concrete draft.

**Fix strategy**
Add an actor-verb-object concretization for every flagged sentence. "Grow revenue" becomes "win back 10 lapsed accounts worth $500K by end of Q2 via personal outreach from the CS team". If the strategy sentence cannot be concretized, the strategy itself is probably incoherent — surface that to the user rather than trying to polish the prose.

---

## AP-08 — Scope Creep (Three Messages Equals No Message)

**One-liner:** The draft tries to make three or more co-equal top points and therefore makes none.

**Detection criteria**
- Count distinct top-level points, themes, or "key takeaways". 3+ with no explicit hierarchy = flag.
- Related to but distinct from AP-03 (Decision Paralysis): paralysis is about conflicting priorities presented as co-equal, scope creep is about a piece trying to communicate too many separate ideas at once.
- High school research-paper pattern: the author feels obligated to include every unearthed fact.

**Book citation**
- Notes p. 175 — "If you say three things, you don't say anything" (attributed comms expert quote).
- Chapter 1 — "If 'it's the economy, stupid' is the lead, then the need for a balanced budget can't also be the lead."
- Epilogue — "High school teachers will tell you that when students write research papers they feel obligated to include every unearthed fact."

**Consequence**
Audience retains zero. Multiple priorities cancel each other out. This is particularly pernicious in long-form copy where the author feels each paragraph is "important" — the sum is less memorable than any single paragraph would have been on its own.

**Severity rubric**
- High: 4+ themes, or the draft is long-form (speech, memo, landing page) with no hierarchy.
- Medium: exactly 3 themes with no designated core.
- Low: 3 themes with a clear primary and two supports.

**Fix strategy**
Name THE one core message (Commander's Intent). Demote the rest to supporting evidence for the core, OR cut them into separate drafts. Hard rule: one core per draft. If the user insists all three matter, split into three separate artifacts rather than combining.

---

## AP-09 — Direct-Message Fallacy

**One-liner:** Raw abstract directives delivered where a springboard story would transfer the idea better.

**Detection criteria**
- Scan for change-management or adoption messages delivered as abstract directives — "we need to be more X", "you should Y", "the key is to Z", "it is important to A".
- No narrative scaffolding: no springboard story, no worked example, no before/after.
- Especially dangerous in change-management contexts (new strategy, culture change, process change) where stories transfer adoption but directives trigger resistance.

**Book citation**
- Chapter 6 (Stories) — Stephen Denning, World Bank: "had always believed in the value of being direct, and he worried that stories were too ambiguous, too peripheral, too anecdotal. He thought, 'Why not spell out the message directly? ... Why not hit the listeners between the eyes?' The problem is that when you hit listeners between the eyes, they fight back."
- Chapter 6 — Velcro theory of memory: "A story is powerful because it provides the context missing from abstract prose. It's back to the Velcro theory of memory, the idea that the more hooks we put into our ideas, the better they'll stick."

**Consequence**
Listeners hear but do not internalize. Abstract directives do not simulate the outcome and so cannot engage the listener's reasoning machinery. Worse, direct directives in change contexts trigger defensive reactions ("fight back") — the opposite of the intended adoption.

**Severity rubric**
- High: the piece is a change-management or adoption message delivered entirely as directive.
- Medium: the piece is informational but relies on assertion where a story would work better.
- Low: the piece is a status update or FAQ where direct delivery is appropriate.

**Fix strategy**
Suggest a springboard-story frame: "tell us one concrete story where this worked, then name the principle". Denning's pattern at the World Bank: a single story of a health worker in Zambia finding CDC information online did more to spark the idea of a knowledge-sharing organization than any directive ever could. If no story is available, suggest an analogy or comparison the user could draft. Acknowledge that direct delivery is sometimes correct (status updates, FAQs) — the flag is only material in change contexts.

---

## Severity Weighting Summary

| Factor | Effect on severity |
|---|---|
| Hit is in the lead sentence | +1 level (Medium → High) |
| Hit is in the close or CTA | +1 level |
| Hit is in a change-management / adoption piece | +1 level for AP-09 specifically |
| Hit is in a decorative / navigation element | -1 level |
| Hit count in same paragraph ≥ 3 | +1 level (compound failure) |

---

## Cross-Pattern Interactions

- **AP-02 (Buried Lead) + AP-04 (Common Sense):** the most common compound failure. The buried lead symptom is usually caused by common-sense sedation in the first sentence. Fix common sense first; the lead often reveals itself.
- **AP-03 (Paralysis) + AP-08 (Scope Creep):** overlapping but distinct. Paralysis is about choosing among competing priorities; scope creep is about failing to choose. A draft can have both (too many themes AND no designated primary).
- **AP-05 (Semantic Stretch) + AP-07 (Abstract Strategy):** stretch words are the atomic units of strategy talk. A draft heavy on "leverage synergies to drive outcomes" is simultaneously a semantic-stretch hit and an abstract-strategy hit. Fix them together.
- **AP-06 (Stats Without Story) + AP-09 (Direct Message):** both are about using the wrong register. Stats without story fails because data does not simulate outcome; direct-message fallacy fails because assertion does not simulate outcome. Story solves both.

---

## What This Catalog Does NOT Cover

- **Curse of Knowledge (AP-001 in hunter findings):** handled by the separate `curse-of-knowledge-detector` skill. That skill covers lexical jargon, tacit shared context, and expert blind spots. This catalog's AP-07 (Abstract Strategy Talk) overlaps slightly, but is scoped to strategy-level abstraction as a stickiness failure rather than as an expert-audience mismatch.
- **The full six-principle SUCCESs scoring rubric:** handled by a separate stickiness-audit skill. This catalog is diagnostic (find defects), not evaluative (score the message).
- **Rewriting the draft:** this catalog and its parent skill produce defect reports. Rewriting is downstream and belongs to a separate message-clinic skill.
