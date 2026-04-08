---
name: mnemonic-device-selector-and-builder
description: Build a complete mnemonic device or memory palace for anything the user needs to memorize, recall, or remember. Use this skill whenever someone wants to memorize a list, sequence, set of terms, vocabulary, historical dates, medical facts, or any body of material they struggle to recall. Activates on requests like "help me remember", "I can't recall", "memorize this", "make a mnemonic", "build a memory palace", "use method of loci", "create a flashcard structure", "remember in order", "recall under pressure", or "stop forgetting." Covers simple devices (acronyms, peg method, chunking, rhyme schemes) and complex devices (memory palace, method of loci, location-based recall). Does NOT teach the underlying subject matter — the learner must understand the content first; this skill organizes it for retrieval.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/make-it-stick/skills/mnemonic-device-selector-and-builder
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: make-it-stick
    title: "Make It Stick: The Science of Successful Learning"
    authors: ["Peter C. Brown", "Henry L. Roediger III", "Mark A. McDaniel"]
    chapters: [7, 8]
tags: ["learning-science", "cognitive-psychology", "evidence-based-learning", "memory-techniques", "mnemonics", "method-of-loci"]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: text
      description: "The material to memorize: a list, sequence, set of terms, body of concepts, or any content the user needs to retrieve reliably"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with conversational output capability."
discovery:
  goal: "Select the right mnemonic type for the material and build a complete, ready-to-use memory device — not a template, but an actual constructed device the user can practice immediately."
  tasks:
    - "Gather what the user needs to memorize: type, volume, order sensitivity, and recall context"
    - "Select mnemonic tier (simple vs. complex) using decision criteria"
    - "For simple material: construct acronym, peg associations, or chunking scheme"
    - "For complex material: build a memory palace with location assignments and vivid image anchors"
    - "Deliver completed device with a 3-session rehearsal schedule"
  audience: ["students", "professionals", "lifelong learners", "educators", "anyone preparing for high-stakes recall"]
  triggers:
    - "Help me memorize this list"
    - "I keep forgetting these terms"
    - "Build a memory palace for this content"
    - "Create a mnemonic for me"
    - "I need to remember this in order"
    - "Use method of loci to help me recall this"
    - "How do I stop forgetting what I study?"
  not_for:
    - "Teaching or explaining the subject matter itself (the user must understand it first)"
    - "Building automated flashcard software"
    - "Creating study schedules (use retrieval-practice-study-system)"
  environment: "Conversational or document-based: lists, notes, vocabulary sets, sequence data, concept outlines"
  quality:
    completeness_score:
    accuracy_score:
    value_delta_score:
---

# Mnemonic Device Selector and Builder

## When to Use

You have material you understand but cannot reliably retrieve when needed. Mnemonic devices are not shortcuts around learning — James Paterson, the Welshman who became a competitive memory athlete, discovered this the hard way: he memorized names and dates for his psychology exams using mnemonics but "didn't have mastery of the concepts, relationships, and underlying principles. He had the mountaintops but not the mountain range." Mnemonics are retrieval infrastructure, not comprehension. Use this skill *after* the user already understands the material.

Typical situations where this skill applies:

- Memorizing a list, sequence, or set of terms under time pressure (exam, presentation, certification)
- Needing to retrieve structured knowledge in a specific order (procedure steps, ranked items, historical sequences)
- Managing high-volume material across multiple topics (medical content, legal codes, multi-part exam essays)
- Preparing to recall knowledge under performance stress (exam hall, job interview, live presentation)

**Mode: Hybrid** — The agent builds the complete mnemonic device. The human practices it through spaced retrieval sessions.

---

## Step 1: Gather What Needs to Be Memorized

**Why:** The mnemonic type must fit the material's structure. The wrong device wastes effort — using a memory palace for five items is overkill; using an acronym for thirty interconnected concepts fails under exam pressure.

Collect:

- **The material itself.** Ask the user to list or paste what must be memorized. If they reference a document, read it.
- **Volume:** How many items, concepts, or sequences? (rough count)
- **Order sensitivity:** Must items be recalled in a specific order, or can they be retrieved in any sequence?
- **Recall context:** Where and when will this be retrieved? (exam hall, live conversation, procedural performance, casual recall)
- **Time to practice:** How many days before the recall event?

If the user has not yet fully understood the material, flag this before proceeding:

> "Mnemonic devices organize what you already know for fast retrieval — they don't replace understanding. If you haven't worked through this material yet, do that first, then come back here to build the retrieval structure."

---

## Step 2: Select Mnemonic Type

**Why:** Simple devices are faster to build and sufficient for small, discrete sets. Complex devices (memory palace) require more construction time but scale to large volumes and high-pressure sequential recall.

### Tier 1 — Simple Devices

Use when **all** of the following are true:
- 10 items or fewer
- Order is not critical, or the sequence is short and linear
- Items are discrete (words, numbers, names, labels) rather than concept-clusters
- Recall context is low-stakes or the device only needs to survive a short time

| Device | Best For | Example |
|--------|----------|---------|
| **Acronym** | Short lists, unordered sets, terms with clear initial letters | ROY G BIV → colors of the rainbow; HOMES → the Great Lakes |
| **Reverse acronym (acrostic)** | Lists where initials don't spell a word | "I Value Xylophones Like Cows Dig Milk" → Roman numeral values (I, V, X, L, C, D, M) |
| **Peg method** | Ordered lists up to 20 items | 1=bun, 2=shoe, 3=tree... each peg holds a vivid image of the item to remember |
| **Chunking** | Long strings of digits or symbols | Phone number 6153926113335 → 615-392-611-3335 (shorter working memory loads) |
| **Rhyme or song structure** | Sequences where rhythm aids recall | Musical phrase → lyrics → encoded image for each segment |

### Tier 2 — Memory Palace (Method of Loci)

Use when **any** of the following are true:
- More than 10 items, or multiple concept-clusters
- Material must be retrieved in a specific order under performance stress
- The recall event is high-stakes (exam, certification, live presentation)
- Items are concept-clusters, not just words (each item has sub-details that must also surface)

**The core mechanism:** Images are easier to recall than words. The brain retrieves a vivid spatial image as a single unit (like "tugging a stringer of fish" — pull one, the whole catch surfaces). Associating content to locations converts abstract material into a mental walkthrough of a familiar space.

**Decision note on the Mark Twain variant:** When the material has inherent quantity or duration (lengths of reigns, timeline spans, measurement-anchored sequences), consider the Twain estate-walk format: stake locations along a physical or imagined path where distance represents a meaningful unit (years, steps, percentages). The path becomes a to-scale diagram that children and adults can literally walk, trot, or revisit.

---

## Step 3: Build the Simple Device

**Why:** A constructed device is ready to practice immediately. A template forces the user to do the hard creative work alone, defeating the purpose of the skill.

### For Acronym / Acrostic

1. List the items. Extract the first letter of each key term.
2. Arrange letters to form a real word (acronym) or create a memorable sentence where each word starts with the extracted letter (acrostic).
3. If no natural word exists, try rearranging the order (if order is not critical) or use a vivid, absurd sentence.
4. Output: the acronym or sentence, plus the mapping (which letter = which item).

**Example — Great Lakes west to east:**  
Ontario, Erie, Huron, Michigan, Superior → HOMES (reordered: Huron, Ontario, Michigan, Erie, Superior)  
Recall cue: "Picture a cluster of HOMES sitting on ice floes."

### For Peg Method (ordered lists up to 20)

1. Confirm the standard peg rhyme: 1=bun, 2=shoe, 3=tree, 4=store, 5=hive, 6=tricks, 7=heaven, 8=gate, 9=twine, 10=pen.
2. For each item to remember, create a vivid, bizarre interaction between the peg image and the target item.
3. Bizarre interactions encode more deeply than mundane ones — the more impossible the scene, the stronger the memory hook.
4. Output: numbered list of (peg image + target item + vivid interaction scene).

**Example — First 3 steps of a procedure:**  
Step 1 (collect data) → bun: "A giant bun rolls down a hill, squashing a pile of spreadsheets and data printouts."  
Step 2 (analyze patterns) → shoe: "A shoe stomps on a magnifying glass that is scanning a graph."  
Step 3 (write report) → tree: "A tree is covered in leaves that are all printed report pages."

### For Chunking

1. Break the full string into groups of 3-4 characters.
2. If groups have natural meaning (phone numbers, zip codes, product codes), use those boundaries.
3. Add rhythm or pronunciation patterns so chunks become speakable units.
4. Output: chunked string with suggested verbal rhythm.

---

## Step 4: Build the Memory Palace (Six-Step Construction)

**Why:** A memory palace's power comes from specificity — a vague imagined space gives vague retrieval cues. Each of the six steps transforms abstract material into concrete, location-anchored imagery that survives exam-hall stress.

**Pre-condition:** The user must understand the material before building. James Paterson's students at Bellerbys College only visited cafés to build memory palaces after "thoroughly covering the material in class." The palace organizes knowledge; it does not create it.

### Step 1: Consolidate and Reduce the Material

Gather all sources (notes, slides, reading). Reduce to **key ideas in phrase form, not full sentences**. These are the items each location will anchor.

- Wrong: "Restraint theory, proposed by Herman and Mack, suggests that the attempt to not overeat paradoxically increases the probability of overeating because disinhibition causes loss of dietary control."
- Right: "Restraint → disinhibition → overeating"

**Why:** Full sentences cannot be imaged. A short phrase collapses into a single vivid scene. A long sentence requires multiple scenes and breaks the location-one-to-one-idea contract.

### Step 2: Select the Palace Location

Choose a real physical space the user knows extremely well — well enough to mentally walk through it in detail with eyes closed.

Good choices:
- A frequently visited café, restaurant, or library
- Your home (room by room, or a single room with many fixtures)
- A commute route with distinctive landmarks
- A childhood street or school

For **the Mark Twain variant (quantity-anchored sequences):** Use a path (driveway, road, hallway) where physical distance represents a meaningful unit. Twain staked 817 feet of his estate driveway — one foot per year of English history — so the monarchs' reigns became walkable, measurable segments. Use this format when your material has duration, quantity, or timeline structure.

**Why the space must be familiar:** The memory palace works because spatial memory is ancient and robust. You already know how your home is laid out without conscious effort. The palace hijacks that effortless spatial recall to carry new, effortful content.

### Step 3: Identify Locations Within the Palace

Walk through the space mentally. Identify 8-15 distinct, fixed features in a logical traversal order.

- For a café: door → host stand → first booth → bar counter → espresso machine → window seat → back table → exit
- For a room: door → left wall bookshelf → armchair → lamp → desk → right wall window → closet door → ceiling fan

Write the sequence. These are your "loci" — the location anchors.

**Why ordered traversal matters:** If order is important (essay structure, procedural steps, historical sequence), the walk direction encodes the order. Marlys, preparing for her A-level psychology exam, moved through Pret-a-Manger clockwise — each station cued the next paragraph in sequence, so she could not skip ahead or lose her place.

### Step 4: Assign One Key Idea to Each Location

Map each reduced key idea (from Step 1) to a specific location (from Step 3), one-to-one.

- Door → Restraint theory (Herman and Mack)
- First booth → Boundary model of hunger and satiety
- Bar counter → Cultural biases in obesity data
- ...and so on

**Why one idea per location:** Assigning two ideas to one location collapses them — retrieval cues blur. If there are more ideas than locations, either expand the palace (add a second room or building) or group closely related sub-ideas under a single phrase.

### Step 5: Populate Each Location With a Vivid, Bizarre Character or Scene

For each location, invent an absurd, memorable scene that encodes the key idea. The scene must:

- Feature a recognizable character or object (a movie character, a celebrity, an animal, a specific person)
- Show that character doing something impossible or extreme — action creates stronger recall than static images
- Directly embody the concept, not just label it

**Marlys's example:** At Pret-a-Manger, the "restraint theory" location showed La Fern (the man-eating plant from *Little Shop of Horrors*) restraining her friend Herman from a plate of mac and cheese just out of reach. When Marlys mentally entered the café and saw La Fern, she immediately wrote: *"Herman and Mack's restraint theory suggests that attempting not to overeat may actually increase the probability of overeating."* The scene encoded the author names, the theory name, and its counterintuitive direction.

**Why bizarre and active:** Humans remember pictures more easily than words, and impossible or extreme scenes encode more durably than plausible ones. A seated person reading a book at the counter is forgettable. A yak riding a unicycle while eating an encyclopedia is not.

### Step 6: Rehearse the Walk — Three Sessions

The palace is built. Now practice retrieval, not review.

**Session 1 (same day, within 2 hours of building):** Walk the palace from beginning to end without looking at notes. At each location, reconstruct the scene and state the key idea aloud or in writing. If a location is blank, skip it, finish the walk, then return to fill gaps.

**Session 2 (24-48 hours later):** Repeat the walk from memory. Check against source material. Repair any broken scenes — strengthen weak images by making them more bizarre or adding sensory detail (smell, sound, movement).

**Session 3 (3-5 days later, or 24 hours before the recall event):** Full walk plus a "random access" test: name a location out of order and retrieve the idea without tracing the full route. This tests whether the location truly anchors the concept or whether you are just remembering a list.

**Why three sessions?** Spaced retrieval practice (not passive re-reading of the palace) is what converts the device into durable long-term memory. One review immediately after construction captures working memory, not long-term storage.

---

## Step 5: Output — Deliver the Completed Device

**Why:** Handing the user a blank framework defeats the skill's purpose. Deliver a complete, specific, ready-to-practice device.

### For Simple Devices

Deliver:
- The full acronym/acrostic/peg list/chunked string — written out completely
- The mapping: each letter/peg/chunk → what it encodes
- One recall cue (a vivid summary sentence or image to start the device)
- The 3-session rehearsal schedule: when to practice and what counts as success

### For Memory Palace

Deliver:
- The palace location and traversal route (in order)
- For each location: [Location name] → [Key idea] → [Scene description]
- A "walk summary" — the full sequence in a single compact list for reference
- The 3-session rehearsal schedule

**Success signal:** The user can walk the palace (or recite the acronym) from memory with zero reference material and retrieve every anchored idea with enough detail to write a paragraph or perform a task — within Session 2.

---

## Examples

### Example 1: Simple — Acronym for Roman Numeral Values

**Material:** I=1, V=5, X=10, L=50, C=100, D=500, M=1000 (ascending order)  
**Device:** Acrostic — *"I Value Xylophones Like Cows Dig Milk"*  
**Mapping:** I=I(1), V=V(5), X=X(10), L=L(50), C=C(100), D=D(500), M=M(1000)  
**Recall cue:** Picture a xylophone-playing cow digging in a milk bath.  
**Rehearsal:** Say the sentence, then state each value without looking. Repeat 24h later.

### Example 2: Complex — Memory Palace for a 5-Topic Exam

**Context:** Three essay topics for a psychology exam, each with 12 key points.  
**Palace 1 (Topic: Dieting):** Pret-a-Manger café, clockwise traversal, 12 locations  
- Door → Restraint theory (La Fern restraining Herman from mac and cheese)  
- Window → Boundary model (a bright neon boundary line dividing the table)  
- Counter → Cultural bias (customer in national costume arguing with the server)  
*(... 9 more locations ...)*

**Palace 2 (Topic: Aggression):** Krispy Kreme shop, 12 locations  
**Palace 3 (Topic: Schizophrenia):** Starbucks, 12 locations  

**Walk rehearsal:** Marlys spent 10 minutes before her exam mentally walking all three cafés, listing the 12 key ideas per topic. She then wrote her essays from her structured notes — without anxiety about forgetting what she had learned.

### Example 3: Twain Estate-Walk Variant — Ordered Sequence With Quantity

**Material:** English monarchs' reigns, William the Conqueror through Victoria (817 years total)  
**Palace:** A driveway or hallway, 817 units long — each unit represents one year  
**Stake placement:** At each reign boundary, place a distinct image-stake (whale = William the Conqueror, because both start with W and both are "the biggest of their kind")  
**Recall:** Walk the path, call out monarch and dates at each stake. Children can physically walk the estate road, or adults can mentally traverse a hallway where each floor tile equals one year.  
**Why this works:** Duration is physically embodied in distance. A 46-year reign is visibly longer than a 2-year reign — proportional memory rather than arbitrary list order.

---

## Critical Warning: Mnemonics Come After Learning

Mnemonic devices are *retrieval infrastructure*, not *learning infrastructure*. James Paterson learned this through competitive failure: he memorized facts for exams without mastering the underlying relationships, and his knowledge collapsed under conceptual questions. The memory palace at Bellerbys College worked for Marlys because Paterson had *already thoroughly covered the material in class* before taking students to construct palaces in cafés.

If the user does not yet understand the material:
1. Flag this clearly.
2. Recommend they work through the content first (retrieval practice, concept mapping, or active study).
3. Return to this skill when they can explain the ideas in their own words.

Mnemonics organize what you know. They cannot substitute for knowing it.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Make It Stick: The Science of Successful Learning by Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
