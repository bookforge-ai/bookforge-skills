---
name: source-evaluator
description: Evaluate, triage, and actively read a set of research sources — books, articles, and online materials — by applying a dual-axis relevance-and-reliability screen, source-type skim protocols, and a two-pass active reading method that extracts data, arguments to respond to, and generative agreements and disagreements. Use this skill when you have a candidate source list and need to cut it to a workable set, when you need to verify that a source is credible before citing it, when you are reading sources to find a research problem or refine a hypothesis, when you need to take notes that accurately capture what a source argues without misrepresenting it, or when you must identify where sources agree and disagree so you can position your own argument within a field's conversation.
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [5, 6]
tags: [research-methodology, source-evaluation, critical-reading, academic-writing, note-taking, literature-review]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Candidate source list or a single source to evaluate. Can be a bibliography file, a list of titles/URLs, or a document set containing source files."
  tools-required: [Read, Write]
  tools-optional: [WebFetch]
  mcps-required: []
  environment: "Document set preferred. Works from a free-text source list. Output: evaluated-sources.md with relevance/reliability verdicts and reading notes."
discovery:
  goal: "Produce a ranked, evaluated source list with relevance verdicts, reliability assessments, and reading notes that capture arguments, data, and productive agreements/disagreements."
  tasks:
    - "Classify each source as primary, secondary, or tertiary relative to the research question"
    - "Apply the relevance skim protocol appropriate to each source type"
    - "Score each source on the reliability rubric (publisher, peer review, author, currency, apparatus)"
    - "Read high-priority sources using the two-pass active reading protocol"
    - "Identify creative agreements and disagreements to generate or refine the research problem"
    - "Record notes using the quote/paraphrase/summarize decision rule and context-preservation guidelines"
  audience: "researchers, students, academics, professionals conducting any evidence-based inquiry"
  when_to_use: "When you have candidate sources and need to decide which to read, how carefully to read them, and how to take notes that will hold up under scrutiny"
  environment: "Document set (source-list.md, research-question.md) or free-text description of the research question and sources"
  quality: placeholder
---

# Source Evaluator

## When to Use

You have a list of candidate sources — books, journal articles, websites, reports — and must decide which are worth reading, how deeply to read them, and how to capture what they say so you can use them reliably in your own argument. This skill applies when:

- You have search results or a bibliography and need to triage it to a manageable set
- You are unsure whether a source is credible enough to cite in a scholarly or professional context
- You are reading to find or sharpen a research problem, not just collect supporting evidence
- You need to understand where sources agree and disagree to position your own argument
- You have taken notes but worry they may misrepresent what a source actually claims

**The core pattern:** evaluate every source on two axes — relevance to your question, and reliability of its claims — before committing reading time. Then read high-priority sources in two passes: first generously (to understand), then critically (to respond). Record what the source says and what you think about it in clearly separated layers.

Before starting, confirm you have:
- A stated research question or working hypothesis (even a rough one)
- At least one candidate source to evaluate

---

## Context and Input Gathering

### Required Context

- **Research question:** What are you trying to find out? Even a topic ("desegregation in Midwest school boards, 1980s") is workable, but a specific question ("How did school boards in the Midwest respond to federal desegregation mandates?") makes relevance assessment more accurate.
- **Source list:** The sources you want to evaluate. URLs, titles, file paths, or a bibliography.

### Observable Context

If documents are provided, read them for:
- Keywords and named concepts central to the research question
- Source type signals (peer-reviewed journal, book from university press, Wikipedia, industry report, blog)
- Publication date and edition information
- Author credentials and institutional affiliation (if visible)
- Presence or absence of bibliography/references

### Default Assumptions

- If no research question is provided → ask for one before evaluating. Relevance cannot be assessed without it.
- If source type is ambiguous → default to the more skeptical classification (treat a non-peer-reviewed article as tertiary until proven otherwise)
- If currency norms for the field are unknown → use the conservative rule: flag anything older than 10 years for humanities fields, 5 years for social sciences, 2 years for sciences and technology

### Sufficiency Check

Before evaluating, confirm: "Do I know enough about the research question to judge whether a source addresses it?" If the question is still a vague topic, help the user sharpen it first.

---

## Process

### Step 1: Classify Each Source by Type

**ACTION:** For each source, assign it a type — primary, secondary, or tertiary — relative to the specific research question.

**WHY:** Source type determines how you use a source, not just how you find it. The same document can be primary for one project and secondary for another. A journal article analyzing Victorian swearing patterns is secondary if your question is about Victorian gender norms, but primary if your question is about how scholars have interpreted Victorian gender norms. Getting this wrong leads to misaligned reading strategies: you read a tertiary source (encyclopedia) as if it were evidence, or you miss that an article is primary data for your project.

**Classification rules:**
- **Primary source:** original materials that provide raw data or evidence for your question. In history: documents, artifacts, letters from the period. In literature/arts: the text or work you are interpreting. In social sciences: survey data, census records, interviews. In sciences: reports of original experiments.
- **Secondary source:** books, articles, or reports based on primary sources, written for scholarly or professional audiences. The best are peer-reviewed or published by university presses. These constitute the field's "literature" — the ongoing scholarly conversation you are entering.
- **Tertiary source:** syntheses of secondary sources for general audiences — textbooks, encyclopedias (including Wikipedia), mass-market publications. Useful for orientation and finding leads to secondary sources. Not appropriate as evidence in scholarly arguments.

**Key rule:** Classifications are relative to your project. If you change your focus, re-classify.

**Output format:**
```
Source: [title/URL]
Type: [primary / secondary / tertiary]
Reason: [one sentence]
```

---

### Step 2: Apply the Relevance Skim Protocol

**ACTION:** Skim each source using the protocol matched to its format. Do not read fully at this stage — the goal is a binary decision: pursue or set aside.

**WHY:** Full reading before relevance assessment wastes time on sources that turn out not to address your question. Skimming forces you to use the structural features that good scholarly sources provide precisely for this purpose — abstracts, indices, opening paragraphs, tables of contents. The skim takes 5-15 minutes per source. A full read takes hours. The investment ratio is decisive.

**See:** [Relevance Skim Protocols](references/relevance-skim-protocols.md) for the full per-format checklists.

**Summary by source format:**

**Book:**
1. Skim the index for your keywords; check the pages on which those words appear
2. Read first and last paragraphs of chapters where your keywords appear most densely
3. Skim prologues, introductions, and summary chapters
4. Read the last chapter's first and last 2-3 pages
5. For edited collections, skim the editor's introduction
6. Check the bibliography for titles relevant to your topic

**Journal article:**
1. Read the abstract if present
2. Skim introduction and conclusion; if headings are absent, read the first 6-7 paragraphs and last 4-5
3. Skim section headings; read first and last paragraphs of each section
4. Check the bibliography for related titles

**Online source:**
1. If it resembles a journal article, apply the article protocol plus keyword search
2. Look for sections labeled "introduction," "overview," "summary," or "about"
3. Check any site map or index for keywords
4. Use the site's search function if available

**Relevance verdict:** After skimming, assign one of three statuses:
- **Read:** clearly relevant; proceed to Step 3 reliability check and then full reading
- **Monitor:** potentially relevant; set aside but note for possible retrieval if other sources prove insufficient
- **Discard:** not relevant to this question

---

### Step 3: Apply the Reliability Rubric

**ACTION:** For each source you marked **Read**, assess reliability using the 5-criterion rubric below. Only proceed to full reading on sources that pass.

**WHY:** Relevance without reliability is dangerous — a source that addresses your question but makes unreliable claims can contaminate your argument. You cannot judge reliability fully until you read, but the rubric identifies red flags before you invest reading time. Importantly, reliability indicators are not guarantees: a peer-reviewed article in a reputable journal can still contain weak arguments or thin data. The rubric tells you where to be cautious, not where to trust uncritically.

**See:** [Reliability Rubric](references/reliability-rubric.md) for the expanded 10-criterion version.

**Core 5-criterion reliability check:**

| Criterion | What to look for | Red flags |
|---|---|---|
| **1. Publication venue** | University press, peer-reviewed journal, established professional publisher | Self-published, vanity press, no publisher listed, sensationalist claims on cover |
| **2. Peer review** | "Peer reviewed" label, journal review process, university press review | Commercial magazines, blogs without editorial process, preprints without review notice |
| **3. Author credentials** | Academic affiliation, track record in the field, cited in other reputable sources | No credentials listed, credentials irrelevant to topic, financial ties to interested parties on contested topics |
| **4. Currency** | Publication date relative to field norms (see below) | Textbooks (assume outdated); sources older than field norms allow; earlier editions when recent editions exist |
| **5. Scholarly apparatus** | Notes, bibliography, citations that can be checked | No bibliography in a book-length argument; website with no attribution, date, or sponsor |

**Field-specific currency norms:**
- Sciences and technology: 2 years is the outer limit for findings; foundational theory may be older
- Social sciences: 10 years is often cited as the outer limit; check recent literature for updates
- Humanities (literary criticism, history, philosophy): articles and books can remain relevant for decades; foundational works cited regardless of age
- **Rule of thumb:** Look at the citations in 2-3 recent articles in your target field. The oldest sources cited regularly establish the floor for acceptable age.

**Advanced criteria** (for experienced researchers or high-stakes projects):
- Has the book been reviewed favorably in field-specific review journals?
- Has the source been frequently cited by others? (High citation count = high impact factor; use forward citation search)

**Reliability verdict:**
- **Reliable:** passes all 5 criteria or has minor issues on 1 criterion with strengths on the others
- **Use with caution:** issues on 2 criteria; flag the specific concerns in your notes
- **Exclude:** fails 3 or more criteria, or fails on peer review and author credentials simultaneously

---

### Step 4: Two-Pass Active Reading

**ACTION:** Read each **Read + Reliable** source twice using the protocol below. Record bibliographic information completely before reading anything else.

**WHY:** Passive reading — absorbing what a source says without responding to it — produces notes that are dead data. You remember the source's argument but not your reactions to it, and your reactions are where your own research problem lives. Two-pass reading forces the separation: the first pass builds understanding on the source's own terms (so you do not misrepresent it later); the second pass builds your critical response (so you do not accept it uncritically). Experienced researchers do this naturally; the protocol makes it explicit for those building the habit.

**Step 4a: Record complete bibliographic information first**

Before reading a single page, record all bibliographic data for the source. (See [Bibliographic Recording Checklist](references/bibliographic-recording-checklist.md) for field-specific lists.) Record it in whatever format you choose for your own notes, but record it completely — incomplete bibliographic records have killed publications.

**Step 4b: First pass — read generously**

Read to understand. Pay attention to what sparks interest. Reread passages that puzzle or confuse you. Do not look for disagreements yet. Read in ways that help the source make sense. Resist the temptation to criticize while you are still learning what the source actually argues.

**During first pass, mark or note:**
- The source's main claim (thesis)
- The evidence it relies on most heavily
- Passages that are central versus qualifications or concessions the author makes in passing
- Passages you find compelling or surprising

**Understand before you respond:** If you cannot summarize the source's argument in 2-3 sentences, you do not yet understand it well enough to respond to it.

**Step 4c: Second pass — read critically**

Read slowly and with your own research question in mind. Think about how you would respond to each claim. Record your responses in your notes — clearly separated from what the source says (see Step 5).

During the second pass, look for productive responses in two directions:

**Creative agreements** (sources you believe — extend them):
1. **Offer additional support:** The source makes a claim; you can support it with better or newer evidence
2. **Confirm unsupported claims:** The source speculates or assumes something; you can prove it
3. **Apply more widely:** The source correctly applies a principle to one case; you can show it applies more broadly

**Creative disagreements** (sources you doubt — challenge them):
1. **Contradiction of kind:** The source categorizes something incorrectly (e.g., graffiti is vandalism; you argue it is public art)
2. **Part-whole contradiction:** The source mistakes how the parts of something relate to each other
3. **Developmental contradiction:** The source mistakes the origin or trajectory of something (e.g., a trend the source says is rising is actually falling)
4. **Causal contradiction:** The source mistakes a causal relationship (e.g., claims X causes Y; you show they are both caused by Z)
5. **Contradiction of perspective:** The source analyzes something from one framework; a different framework reveals a new truth

**See:** [Active Reading Response Taxonomy](references/active-reading-response-taxonomy.md) for templates and examples for each type.

---

### Step 5: Take Notes That Hold Up

**ACTION:** Record your notes using the four-layer structure below. Always separate what the source says from what you think about it.

**WHY:** The most common failure in research note-taking is blending the source's words with your paraphrase of them, or blending both with your own interpretation. This causes two problems: (1) you may later cite your paraphrase as a direct quotation, undermining your credibility; (2) you may attribute your own ideas to the source or the source's ideas to yourself, which is a form of inadvertent plagiarism. Keeping the layers separate is not just scholarly caution — it is how you maintain the distinction between what you know and what you think, which is the foundation of honest argument.

**Four-layer note structure:**

```
SOURCE: [Author, short title, page]
TOPIC TAGS: [keywords for sorting and retrieval]

SUMMARY: [2-4 sentences capturing the source's main argument in your own words]

QUOTATION(S): [exact words, in quotation marks, with page numbers]
"..." (p. XX)

PARAPHRASE(S): [source's meaning in your words; replace most words, not just a few]
[Paraphrase of p. XX]: ...

MY RESPONSE: [your reactions, agreements, disagreements, questions — clearly marked as yours]
[Response]: ...
```

**Quote, paraphrase, or summarize — when to use each:**
- **Summarize** when you need only the point of a passage, section, or whole source. Summary is useful for context or for sources only loosely relevant to your argument. A summary alone is never evidence.
- **Paraphrase** when the specific words matter less than the meaning. Replace most of the words and phrasing — not just a word or two. A paraphrase is weaker evidence than a direct quotation.
- **Quote exactly** when: (a) the words themselves are evidence (e.g., exact language in a historical document); (b) the source is an authority you will directly challenge or rely on; (c) the phrasing is so precise or striking that your paraphrase would lose it; (d) you are disagreeing with a specific claim and must represent it fairly.

**Never abbreviate a quotation expecting to reconstruct it later. You cannot.**

**Context-preservation rules (prevent misrepresentation):**
1. Record not just what a passage says but the line of reasoning it serves in the source. Note the pages before and after.
2. When you record a claim, note its role: main point, minor point, qualification, or concession. A concession reported as a main point is a misrepresentation — even if accidental.
3. Record the scope and confidence of claims precisely. "Chemicals in french fries cause cancer" and "some chemicals in french fries correlate with a higher incidence of some cancers" are not the same claim.
4. Note when a source is summarizing someone else's view rather than stating its own. Misattributing a summary as the source's own position is a common error.
5. Note why sources agree or disagree when you spot convergence or conflict — the basis of agreement matters as much as the fact of it.

---

## Output

Produce an `evaluated-sources.md` file with the following sections:

**1. Source Inventory**
For each candidate source: type classification, relevance verdict (Read / Monitor / Discard), reliability verdict (Reliable / Use with Caution / Exclude), and a one-line rationale.

**2. Reading Notes**
For each source you read fully: the four-layer note structure (summary, quotations, paraphrases, your response).

**3. Productive Tensions**
A brief section listing the most significant creative agreements and disagreements you identified across sources — these are the seeds of your own argument.

---

## Examples

**Example 1: Triaging a bibliography**

Research question: "How did social media use during the 2020 US election affect political polarization?"

Given 12 sources, the evaluator would:
- Classify Wikipedia and a Pew Research explainer as tertiary (useful for orientation, not citation)
- Mark a 2019 peer-reviewed article on social media and polarization as secondary + Read
- Flag a 2016 book on political communication as secondary + Reliable but flag for currency (pre-2020)
- Mark a personal blog post with no author or date as Exclude

**Example 2: Reading for a research problem**

A student reading a secondary source on urban desegregation finds the source argues that federal mandates uniformly increased white flight. The student applies creative disagreement type 3 (developmental contradiction): data from three Midwestern cities suggest the pattern peaked and then reversed after 5 years. That disagreement is the research problem.

**Example 3: Context-preserving note**

Poor note: "Jones (p. 123): The war was caused by Z."
Better note: "Jones argues the war was caused by X, Y, and Z (p. 123); he considers Z the most important cause (p. 123), for reasons on pp. 124-28. Note: X and Y are introduced as background context, not as Jones's main causal argument."

---

## References

- [Relevance Skim Protocols](references/relevance-skim-protocols.md) — full per-format checklists for books, articles, and online sources
- [Reliability Rubric](references/reliability-rubric.md) — expanded 10-criterion rubric with field-specific guidance
- [Active Reading Response Taxonomy](references/active-reading-response-taxonomy.md) — templates for 3 creative agreement types and 5 creative disagreement types
- [Bibliographic Recording Checklist](references/bibliographic-recording-checklist.md) — field-specific bibliographic data requirements
