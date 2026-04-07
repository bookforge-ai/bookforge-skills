---
name: data-visualization-selector
description: "Select the correct graphic type (table, bar chart, line graph) for a dataset and rhetorical goal, then design and frame it to communicate evidence clearly and honestly. Use this skill whenever the user needs to present quantitative data in a research paper, report, thesis, presentation, or professional document and asks: which chart should I use, how should I visualize this data, how do I make this graphic clearer, is my chart misleading, how do I label or title a table or figure, or how do I introduce a graphic in text. Also triggers on: \"my advisor said the table is confusing,\" \"should I use a bar chart or line graph,\" \"how do I make readers see my point in this figure,\" \"is this graph ethical,\" \"my chart looks amateurish,\" \"the scale on my graph looks off,\" or any request to improve the visual communication of numerical evidence. Covers the full workflow: verbal-vs-visual decision → graphic type selection based on rhetorical effect → design simplification → framing with title, intro sentence, and labels → ethical integrity checks."
version: 1
status: draft
source-books:
  - id: the-craft-of-research
    title: "The Craft of Research, 4th Edition"
    authors: ["Wayne C. Booth", "Gregory G. Colomb", "Joseph M. Williams", "Joseph Bizup", "William T. FitzGerald"]
    chapters: [15]
tags: [research-methodology, data-visualization, academic-writing, evidence-presentation, tables, charts, graphs, research-ethics]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: data
      description: "The dataset, table, or graphic the user wants to present or improve — pasted as text, described verbally, or provided as a file"
    - type: claim
      description: "The argument or point the graphic is meant to support — what readers should conclude from it"
  tools-required: []
  tools-optional: [Read, Write]
  mcps-required: []
  environment: "Any agent environment. Works on described data, pasted tables, or referenced files."
---

# Data Visualization Selector

## When to Use

The user has quantitative data and needs to present it visually in a research paper, report, thesis, or presentation. Typical triggers:

- User has a dataset and asks "should I use a table or a chart?"
- User shares an existing graphic and asks why it looks confusing or amateurish
- User asks how to title, label, or introduce a graphic
- An advisor or reviewer said a figure was misleading, hard to read, or poorly framed
- User has multiple data points they are struggling to fit into prose
- User suspects their chart may be exaggerating or misrepresenting their findings

**Scope:** This skill covers the selection, design, and ethical framing of tables, bar charts, and line graphs — the three graphic types essential for basic quantitative research. For scatter plots, heat maps, box plots, or advanced statistical graphics, use this skill's decision logic as a foundation and consult field-specific visualization resources.

**Do not use this skill to select graphics for decorative purposes.** Every graphic must directly support a specific argument or claim.

## Context

### Required (must be present before proceeding)

- **The data:** What values are being presented? How many data points? What variables?
- **The argument:** What claim should readers draw from the graphic? What should they notice?

### Useful but not required

- **Audience and venue:** Specialist readers in your field vs. general audience? Print vs. screen? Black-and-white vs. color?
- **Existing graphic (if revising):** Share it as text, a description, or a file so this skill can diagnose specific problems.

---

## Stage 1 — Verbal or Visual?

Before selecting a graphic type, decide whether visualization is necessary at all.

**Use prose (no graphic) when:**
- You have 3 or fewer numbers to present. Readers can hold a small set of values in a sentence as easily as in a table.
- Example: *"In 2013, men earned $50,033 a year and women $39,157, a difference of $10,876."* This sentence communicates the same information as a 3-row table — and takes less space.

**Use a graphic when:**
- You have more than a few numbers and prose forces readers to track more values than working memory allows.
- The relationships or patterns in the data are the point — readers need to see structure, not just remember numbers.
- The visual comparison is itself the argument (e.g., a dramatic difference in magnitude).

**Why this decision matters:** Graphics carry an implicit claim of complexity. A table with two rows signals to readers that the data required a table — if it did not, the graphic looks inflated and the writer looks like they are padding the paper with visual bulk.

---

## Stage 2 — Select the Graphic Type

The three primary graphic types each produce a distinct rhetorical effect. Choose the effect that matches your argument.

### Table

**Rhetorical effect:** Precise, objective, neutral. Presents discrete numbers and lets readers draw their own comparisons.

**Use when:**
- Exact values matter and readers will need to look up or compare specific numbers
- You have many variables across multiple categories and readers may need to extract different values depending on their question
- The argument requires readers to see all the data, not just a highlighted trend

**Example trigger:** "Here are the unemployment rates for nine countries across two time periods" — readers may want to check any specific country, so exact numbers in a table serve them better than a simplified visual.

**Trade-off:** A table requires readers to infer relationships themselves (unless you state them in an introductory sentence). A table makes your data available; it does not automatically make your argument visible.

---

### Bar Chart

**Rhetorical effect:** Visual contrast. Emphasizes differences in magnitude among discrete items.

**Use when:**
- The argument is a comparison — one group or item is larger, smaller, or different from others
- Bars arranged to match your point (e.g., sorted by size, grouped by category) directly support the claim
- You want readers to see relative sizes at a glance rather than read exact numbers

**Example trigger:** "Most of the world's deserts are concentrated in North Africa and the Middle East." A bar chart with deserts grouped by region (rather than listed alphabetically) makes that geographic concentration visible as a visual pattern — readers do not have to read and calculate. An alphabetical listing of the same values produces no coherent image.

**Trade-off:** Bar charts communicate less precisely than tables. Readers see approximate magnitudes, not exact values. Add numbers to bars when exact values also matter.

**Variants:**
- *Stacked bars:* Use only when you want readers to compare total bar heights across groups; do not use when the argument depends on comparing individual segment sizes (readers cannot judge segment proportions accurately by eye).
- *Clustered bars:* Use when segment sizes are as important as totals. Group and order logically; label group totals.
- *Pie charts:* Avoid for quantitative data — readers cannot accurately judge proportional areas. Acceptable only for qualitative impressions (e.g., "one segment is disproportionately larger than all others combined"). Use bar charts instead for quantitative comparisons.

---

### Line Graph

**Rhetorical effect:** Continuous change over time. Suggests trend, trajectory, and movement.

**Use when:**
- Time is one axis and you want to argue that something changed, increased, or declined
- The argument is about direction and rate of change, not specific values at points in time
- Multiple trends need to be compared visually over the same period

**Example trigger:** "Two-parent households declined steadily from 1970 to 2010 while mother-headed households rose." The line graph conveys this crossing trajectory in a single image; a table of the same values requires readers to read across rows and do arithmetic to see the trend.

**Trade-off:** A line graph implies continuous change between plotted points. If your data are categorical, intermittent, or collected at uneven intervals, a line graph misleads by implying smooth progression. Use a bar chart for discrete items, even if time is involved.

**Variable direction note:** Choose the variable that makes the line travel in the direction that supports your argument. If a reduction is good news, you may represent the same data as an increase in the opposing variable (e.g., retention rate instead of dropout rate) to produce a rising line that carries positive visual force.

---

## Stage 3 — Design the Graphic

Once the type is selected, apply these design principles to produce a clear, readable graphic. Resist default software settings — most produce graphics that look complex without communicating clearly.

### 3.1 Keep It Simple

**Include only data relevant to your argument.** If you have additional data to report for completeness, label it separately and move it to an appendix.

**Why:** Readers assume every element of a graphic is there to support your point. Irrelevant data confuses them about what they should conclude.

**For tables:**
- Use horizontal lines only (top border, bottom border, header separator). Do not use a grid of horizontal and vertical dark lines — it creates visual noise.
- For long tables, shade every fifth row lightly to help readers track rows across columns.
- Do not add background color or shading.

**For charts and graphs:**
- Box a graphic only if you are grouping two or more figures together.
- Do not color or shade the background.
- Use background grid lines only if the graphic is complex or readers need to read precise values from it. Make grid lines light gray.
- Use color or shading only to show a contrast. Verify the graphic is still readable in black-and-white (avoid distinguishing elements by color alone if the document may be photocopied).
- Never use iconic bars (e.g., images of cars to represent automobile production) — they distort how readers judge values and look amateurish.
- Do not add a third dimension (3D effect) for visual appeal. Three-dimensional bars and pie charts make proportions harder to judge, not easier.

### 3.2 Use Clear Labels

**Label everything:** All rows and columns in tables; both axes in charts and graphs; all lines in line graphs.

**For graphs and charts:**
- Use tick marks and labels to indicate intervals on the vertical axis.
- Label lines and bar segments directly on the graphic image when possible. Use a legend only when direct labeling would make the graphic too cluttered to read.
- When exact values matter, add them to bars (above or inside) or to dots on line graphs.

**Why:** A graphic that requires readers to scan between image and legend interrupts reading and increases the chance of misidentifying elements. Direct labeling keeps interpretation in the image.

### 3.3 Order Data to Match Your Argument

**Tables:** Order rows and columns by the principle that lets readers quickly find the comparison you want them to make. Do not default to alphabetical order unless the argument has no inherent ordering.

**Bar charts:** Arrange bars to create a visual image that matches your claim. Bars in no particular order imply no particular point.

**Example:** A bar chart of desert sizes listed alphabetically makes no argument. The same data sorted by region (North Africa, Middle East, Australia, South Africa, North America) immediately supports the claim that deserts cluster in certain geographic zones.

**Tables — rounding:** Round to the precision that makes differences visible. If differences smaller than 1,000 do not matter to your argument, then 2,123,499 is misleadingly precise — use 2,123,000 or 2.1 million. Place totals at the bottom of columns or the end of rows, not at the top.

---

## Stage 4 — Frame the Graphic in Text

A graphic does not speak for itself. You must frame it with three elements that tell readers what to see and why it matters.

### 4.1 Provide a Descriptive Title

**Tables:** Title goes above the table, flush left.
**Figures (charts, graphs):** Legend goes below the figure, flush left.

**Rules for titles and legends:**
- Describe the data specifically enough to distinguish this graphic from every other in the document.
- Do not use a general topic as a title: **Not** *Heads of households* — **Use** *Changes in one- and two-parent heads of households, 1970–2010*
- Do not editorialize in the title — do not characterize what the data imply: **Not** *Weaker effects of counseling on depressed children before professionalization of staff, 1995–2004* — **Use** *Effect of counseling on depressed children, 1995–2004*
- Make the title descriptive, not argumentative. The argument belongs in your introductory sentence (see 4.2).

**Why:** Titles serve as identifiers when readers scan, search for, or cite a specific figure. An argumentative title permanently embeds your interpretation into the graphic's identity and prevents a reader from drawing an independent conclusion from the data.

### 4.2 Write an Introductory Sentence

Before every graphic, write one sentence that tells readers what to see in it and how it supports your argument. Do not assume readers will draw the right conclusion.

**Structure:** State the claim you want the graphic to support, then refer readers to the figure.

**Without framing:** *Table 15.3. Gasoline consumption.* (Readers must figure out why it is here.)

**With framing:** *Gasoline consumption has not grown as predicted. Though Americans drove 23 percent more miles in 2000 than in 1970, they used 32 percent less fuel. [See Table 15.3.]*

**Why:** Readers approach a graphic already looking for whatever the preceding text suggested they would find. Without a framing sentence, readers do not know which relationship in the graphic to focus on — they look everywhere and conclude nothing specific. A good framing sentence makes the reader's eye go directly to the key number, trend, or relationship.

### 4.3 Add Internal Emphasis When the Data Is Dense

If a graphic contains many values but only a few are directly relevant to your argument, highlight those values internally — for tables, shade the relevant rows or columns; for graphs, annotate key inflection points.

**Example:** A table showing per-capita mileage and fuel consumption across four decades becomes readable when the percentage-change column is shaded and labeled, directing attention to the relevant comparison. Without shading, readers scan all 16 cells equally.

---

## Stage 5 — Check for Ethical Integrity

A graphic that is technically accurate can still mislead. Before finalizing, run these four checks:

**Check 1 — Scale manipulation.** Does the vertical axis begin at zero? A truncated scale (starting at a non-zero value) compresses the visible range and exaggerates contrasts. A bar chart where bars appear to show a 50% reduction may actually represent a drop from 94 to 90 on a scale starting at 80. The data are accurate; the visual impression is not.

- Rule: Do not manipulate scale to magnify or reduce a contrast beyond what the data warrant.

**Check 2 — Dual-axis false correlation.** Does your line graph use two different vertical scales on left and right axes? Two independent variables measured on different scales will appear to move together if their scales are calibrated to overlap visually. This creates the impression of correlation or causation where neither has been established.

- Rule: Do not use dual-axis graphs to suggest a relationship between variables unless you have established the relationship through analysis, not visual calibration.

**Check 3 — Figure type distorting values.** Does the figure's geometry accurately represent the data? Stacked area charts, 3D graphics, and certain pie chart configurations can make the same data appear to show different patterns depending on which elements are placed at the top or bottom.

- Rule: Do not use a figure whose image distorts the values it displays.

**Check 4 — Missing argument statement.** If the graphic supports a specific point, have you stated that point? Presenting data without a claim allows readers to draw unintended conclusions.

- Rule: If the table or figure supports a point, state it. Silence is not neutrality — it is an invitation to misinterpret.

---

## Examples

### Example 1: Verbal vs. Visual Decision

**Data:** Average annual salaries for men ($50,033) and women ($39,157) in 2013, with a difference of $10,876.

**Decision:** Three numbers. Prose handles this without a graphic — *"In 2013, men earned $50,033 a year on average and women $39,157, a difference of $10,876."* A table here adds visual bulk without adding comprehension.

**But:** Add four time periods and two additional family types across 40 years (the family structure data), and the same logic flips — 20+ numbers exceeds what readers can hold in working memory from prose. A table or chart is now necessary.

---

### Example 2: Bar Chart vs. Line Graph for the Same Data

**Data:** Percentages of U.S. families by type (two-parent, mother-headed, father-headed, no-adult-headed) across five decades (1970–2010).

**If the argument is:** "Family structure changed dramatically over 40 years, with two-parent households declining steadily while mother-headed households tripled."
- Use a **line graph**: it visualizes continuous directional change and allows all four trends to be compared over time on a single image.

**If the argument is:** "In any given year, different family types had dramatically different prevalence rates."
- Use a **bar chart**: it emphasizes magnitude contrasts at a given point in time (contrast among discrete items within each year's cluster).

**Design note (bar chart):** Do not sort bars alphabetically or by family-type name. Group them by year, then order the bars within each group by size — largest first — to make the dominant category immediately visible.

---

### Example 3: Detecting and Correcting an Ethical Violation

**Scenario:** A bar chart shows a city's pollution index declining from 101 to 90 over twelve years, presented as evidence of significant environmental improvement.

**The problem:** The vertical axis starts at 80 (not 0). The resulting bars appear to shrink by roughly half their height, creating the visual impression of a ~50% reduction. The actual decline is 101 to 90 — about 11% on the full scale.

**Correction:** Start the vertical axis at 0. The bars will now show a modest, accurate decline. If the decline is real and meaningful, state it in the introductory sentence: *"Pollution fell 11 percent over twelve years, from 101 to 90."* Do not rely on a distorted visual to inflate the apparent magnitude.

---

## Quick-Reference: Graphic Type Selection

| Your argument | Data characteristics | Best type |
|---|---|---|
| Present all values for reference or lookup | Many exact numbers | Table |
| Show difference in magnitude between discrete items | Categories, no time axis | Bar chart |
| Show trend or change over time | Continuous time axis | Line graph |
| Show parts of a whole (totals matter most) | Whole + proportional parts | Stacked bar |
| Show proportion is disproportionately large/small | One segment dominates | Pie (qualitative only) |

---

See `references/graphic-type-rhetorical-effects.md` for an extended table of rhetorical uses for additional graphic types (scatter plots, frequency distributions, box plots) used in advanced research contexts.

See `references/ethical-visualization-checklist.md` for a printable checklist of all five ethical integrity checks.
