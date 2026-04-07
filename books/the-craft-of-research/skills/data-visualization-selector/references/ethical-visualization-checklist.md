# Ethical Visualization Checklist

Use this checklist before finalizing any graphic in a research paper, report, or thesis. A graphic can contain accurate data and still mislead through design choices. These checks catch the most common forms of visual misrepresentation.

Source: The Craft of Research, 4th Ed., §15.5 — Communicating Data Ethically.

---

## The Four Rules

1. Do not manipulate a scale to magnify or reduce a contrast.
2. Do not use a figure whose image distorts values.
3. Do not make a table or figure unnecessarily complex or misleadingly simple.
4. If the table or figure supports a point, state it.

---

## Check 1 — Axis Scale (Truncation)

**Question:** Does the vertical (value) axis begin at zero?

- [ ] If yes: proceed.
- [ ] If no: is there a legitimate field convention for starting at a non-zero value (e.g., temperature scales, index benchmarks)? If yes, label the truncation explicitly.
- [ ] If no legitimate reason: reset axis to zero. Recheck whether the argument still holds. If the argument depended on the compressed visual, state the actual magnitude of change in the introductory sentence.

**The problem:** A bar chart with a y-axis starting at 85 instead of 0 can make a drop from 101 to 90 appear to represent a 50% reduction. The data are accurate; the visual impression is false.

---

## Check 2 — Dual-Axis Lines (False Correlation)

**Question:** Does your graph use two different vertical scales — one on the left axis, one on the right — for two different variables?

- [ ] If no dual axis: proceed.
- [ ] If dual axis present: have you established the relationship between these two variables through analysis (regression, correlation coefficient, causal mechanism)? If yes, label both axes clearly and note the relationship in the text.
- [ ] If no established relationship: do not use dual-axis display. Two variables that merely "trend together" on a dual-axis graph imply causation by visual proximity, not by evidence.

**The problem:** A dual-axis graph showing union membership (left axis, 13–17%) and unemployment rate (right axis, 4–8%) over the same period can be calibrated so both lines trace nearly identical paths. This implies they move together causally. But the scales are different — any two variables that decline over the same period will appear to correlate on a dual-axis graph if you calibrate the axes to match.

---

## Check 3 — Figure Geometry Distorting Values

**Questions to check:**

- [ ] **3D graphics:** Are you using a three-dimensional rendering of a bar, pie, or area chart? 3D rendering creates depth illusions that make front bars appear larger than back bars of equal value. Remove the 3D effect.
- [ ] **Stacked area chart ordering:** In a stacked area chart, have you placed the most volatile band at the bottom? If a bottom band rises sharply, all bands above it will appear to rise as well, even if their individual values are stable. Place the most stable bands at the bottom.
- [ ] **Iconic bars:** Are bars replaced with images (e.g., stacked coins, car icons)? Iconic bars distort magnitude perception. Replace with plain bars.
- [ ] **Pie chart precision:** Are you using a pie chart to communicate precise proportions between segments of similar size? Switch to a bar chart.

---

## Check 4 — Missing Argument Statement

**Question:** For every table and figure in the document, is there an introductory sentence that states the claim the graphic supports?

- [ ] Every graphic has an introductory sentence before it.
- [ ] The introductory sentence states the argument — what readers should conclude — not just "Table 3 shows..."
- [ ] The introductory sentence highlights the specific values or relationships readers should look for.

**Why silence misleads:** A graphic without an introductory argument statement invites readers to draw any conclusion the data could support — including incorrect ones. The author's silence does not signal neutrality; it signals that the point was too obvious to state, or that there is no point, or (worst) that the author does not know what the data mean.

---

## Check 5 — Complexity and Simplicity Balance

**Question:** Is the graphic as simple as its content allows, but not simpler?

- [ ] Does the graphic include only data relevant to the argument? (Extraneous data: label separately and move to appendix.)
- [ ] Does the graphic display enough data that readers can verify the claim? (A graphic with only two data points selected to support a trend claim that exists across twenty data points is misleadingly simple.)
- [ ] Are all labels, axes, and titles present and specific? (Missing labels force readers to guess what they are looking at.)

---

## Quick Self-Test

Before submitting, ask:

1. If a hostile reader examined only my graphic — not my text — could they use a design choice in it to argue I was exaggerating or suppressing the contrast? If yes, fix the design choice and explain the actual magnitude in text.

2. If I described what this graphic looks like to someone who cannot see it, would my description match what the data actually say? If not, the figure's image is distorting the values.

3. Have I stated in prose what I want readers to conclude from this graphic? If not, add an introductory sentence.
