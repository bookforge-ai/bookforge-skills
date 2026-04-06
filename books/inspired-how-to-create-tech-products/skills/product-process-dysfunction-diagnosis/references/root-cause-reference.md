# Root Cause Reference

Extended detection signals and remediation patterns for each of the 10 root causes of failed product efforts.

Source: INSPIRED by Marty Cagan, Chapters 3–7.

---

## Root Cause 1 — Sales/Stakeholder-Driven Idea Sourcing

**Source chapter:** Ch6 (pp. 17–18)

**Extended signals:**
- Roadmap items can each be traced to a specific stakeholder who requested them
- The PM attends stakeholder "requirements sessions" as a standard part of their week
- Feature descriptions reference a specific customer, deal, or internal sponsor rather than a customer segment or problem
- Engineers describe the product as "Sales' product" or "Marketing's product"

**What this is not:**
- Stakeholder input is not inherently wrong. The problem is when stakeholders are the primary or dominant source, replacing customer insight and discovery.
- Sales feedback can surface real customer problems. The dysfunction is when it bypasses discovery and becomes a direct feature request.

**Remediation by stage:**
- *Startup:* Co-founders must separate "customer request for this feature" from "customer has this problem." Commit to the problem, not the proposed solution.
- *Growth:* Establish a product strategy that gives the team criteria for what goes on the roadmap. Stakeholder requests must be evaluated against strategy.
- *Enterprise:* Requires formal intake process with explicit criteria. Sales specials must be limited and time-boxed; they cannot be the default mechanism.

---

## Root Cause 2 — Unknowable Business Cases

**Source chapter:** Ch6 (pp. 18)

**The two inputs that cannot be known:**
1. How much money/value will the idea make? — Depends entirely on quality of the solution, which hasn't been created yet. Many product ideas generate literally nothing (confirmed by A/B testing data).
2. How much will it cost to build? — Cannot be estimated without knowing the actual solution. Experienced engineers refuse to estimate at this stage; others provide "t-shirt sizes" (S/M/L/XL) that are essentially meaningless.

**Extended signals:**
- The phrase "we need a business case before we prioritize this" is common
- ROI projections are reverse-engineered to justify decisions already made
- Engineering estimates exist on the roadmap next to items that haven't been designed
- Business case effort adds 2–6 weeks to getting started

**Why business cases themselves are not wrong:**
Cagan is in favor of business cases for ideas that need a larger investment. The problem is the sequence — creating business cases before solution discovery produces false precision and bureaucratic overhead without reducing actual risk.

**Remediation:**
Move the business case to after a prototype has been validated with customers. The inputs become real: you have evidence for potential value, and engineering can estimate against a defined solution.

---

## Root Cause 3 — Roadmap as Commitment

**Source chapter:** Ch6 (pp. 18–19)

**Extended signals:**
- Sales references roadmap dates in customer conversations
- When items are removed from the roadmap, it is treated as breaking a promise
- The PM's performance review includes "roadmap delivery" as a metric
- The roadmap is a Gantt chart or dated list, not a prioritized hypothesis backlog

**The output vs. outcome distinction:**
Projects are output. Product is about outcome. The roadmap-as-commitment model focuses entirely on output (features shipped) and has no mechanism for tracking whether those features achieved the intended outcome. This is why teams can ship 100% of their roadmap and still be failing.

**What a healthy roadmap looks like:**
A prioritized list of the most important problems to solve, with success metrics defined, but without commitment to specific solutions or dates until discovery is complete.

---

## Root Cause 4 — Product Manager as Project Manager

**Source chapter:** Ch6 (p. 19)

**The 180-degree problem:**
Gathering requirements and documenting them for engineers is the opposite of what product management should be. Requirements-gathering assumes the solution is known and just needs to be described. Product management starts from the problem and discovers the solution.

**Extended signals:**
- PM job description uses words like "gather," "document," "translate," "coordinate," "track"
- PMs have no time in their calendar marked for customer interviews or prototype testing
- When asked "what problem are we solving with this feature?" the PM quotes the stakeholder's request
- The PM is evaluated on delivery (sprint velocity, milestone completion) not on outcomes (revenue, retention, adoption)

**The "mercenary" vs. "missionary" distinction:**
In the requirements-gathering model, the team is mercenary — they implement what they are told. In product management, the team is missionary — they are given a problem and have the authority and responsibility to find the best solution.

---

## Root Cause 5 — Design Brought In Too Late

**Source chapter:** Ch6 (pp. 19–20)

**The "lipstick on the pig" pattern:**
When design enters after requirements are set, the fundamental problem-solution fit has been locked in by non-designers. Design can only optimize the presentation of a solution that may be fundamentally wrong. The UX designers are aware of this — they are doing their best within structural constraints that prevent them from doing real design work.

**Extended signals:**
- Designers receive wireframes or written requirements as design inputs
- There is no "design studio" or collaborative ideation session early in the process
- Designers are allocated per feature (assigned when a feature starts, done when it ships)
- User research, if it exists, is conducted by a separate research team whose findings are reported out rather than experienced directly by the designers

**The real value of design:**
Design's actual contribution is discovering the right solution before anything is built — prototyping, testing, iterating on interaction patterns and information architecture until a solution is found that customers can actually use and value. This requires design to be a discovery partner from day one, not a delivery service at the end.

---

## Root Cause 6 — Engineers Excluded from Ideation

**Source chapter:** Ch6 (p. 20)

**The "best single source of innovation" problem:**
Engineers are typically the best single source of innovation in a product organization. They have direct knowledge of what is technically possible, what is becoming possible (new APIs, new capabilities, falling costs), and how existing technical investments could be leveraged for new product purposes. Excluding them from ideation means this knowledge is never applied to product decisions.

**Extended signals:**
- Engineers describe their role as "implementing designs"
- Engineering input into product direction is limited to effort estimates
- "Feasibility" is only checked after a feature is spec'd, not explored during ideation
- Engineers propose technical improvements (infrastructure, tooling) but not product ideas
- The phrase "the engineers just build what they're told" is used without irony

**The "half their value" calculation:**
If engineers are used only for implementation, the organization is getting approximately half their value — the labor of building, but not the intellectual contribution to what gets built.

---

## Root Cause 7 — Agile Applied Only to Delivery

**Source chapter:** Ch6 (p. 20), Ch7 (pp. 23–24)

**The 20% value problem:**
Agile methods applied only to the delivery phase capture approximately 20% of the potential value. The core Agile benefit — rapid learning through fast feedback loops — requires that discovery and definition are also iterative. Applying Agile only to engineering delivery turns it into a faster waterfall.

**Extended signals:**
- "We're Agile" is demonstrated by sprint ceremonies, not by discovery practices
- Retrospectives only address delivery issues, not upstream process problems
- The backlog contains no discovery tasks, only implementation tasks
- "Definition of done" is code-complete and QA-passed, not "did it solve the problem?"
- Teams that were told to "be Agile" implemented Scrum and stopped there

**Lean principles also frequently misapplied:**
Teams claim to be applying Lean while working for months on what they call a minimum viable product (MVP) without knowing whether it will sell. Teams also over-apply Lean by testing and validating everything, going nowhere fast. Neither reflects the actual principle: reduce waste through fast, cheap learning before committing to expensive build effort.

---

## Root Cause 8 — Project-Centric Not Product-Centric

**Source chapter:** Ch6 (p. 20)

**The orphaned project pattern:**
A project-centric model produces a predictable failure mode: something was shipped, it didn't meet its objectives, but the team has already been disbanded or reassigned to the next project. No one owns improving it. The organization ships features into a void and moves on.

**Extended signals:**
- The product team changes with each major initiative
- "Maintenance mode" is where products go after their initial launch
- Metrics are checked at launch and then rarely revisited
- There is no defined owner for a given product area who is accountable for its long-term performance
- Budget cycles are project-based, not product-team-based

**The iteration requirement:**
Even ideas that have real potential typically require several iterations to deliver the necessary business value. This is the second inconvenient truth. A project-centric model structurally prevents these iterations from happening, because the project ends at launch.

---

## Root Cause 9 — Customer Validation at the End

**Source chapter:** Ch6 (p. 20)

**The biggest flaw of waterfall:**
Cagan identifies this as the biggest flaw of the waterfall process: all the risk is at the end. The entire engineering investment is committed before the first real customer interaction. By that point, it is too expensive to change direction — so teams either ship something that doesn't work or spend months in rework that could have been avoided with a two-day prototype test at the beginning.

**Extended signals:**
- "User acceptance testing" is the primary customer validation mechanism
- Usability testing happens on production builds or release candidates
- Customer pilots or betas are the first time real users see the product
- Discovery is not a defined phase — it happens implicitly as requirements are gathered from stakeholders
- "We'll see what customers think when we ship" is a common planning assumption

**The cost calculation:**
If a prototype test takes two days and costs essentially nothing, but a full engineering build takes 8 weeks, and 50–75% of ideas won't work as expected, validating before building has an expected value that is straightforward to calculate. Teams that do late validation are trying out ideas in one of the most expensive, slowest ways possible.

---

## Root Cause 10 — Opportunity Cost Ignored

**Source chapter:** Ch6 (p. 20)

**The invisible cost:**
Opportunity cost is invisible because it represents the value of work not done, not the cost of work that was done and failed. This makes it systematically under-weighted in all planning processes — you can see the cost of a failed project, but you cannot see the revenue from a product that was never built because the team was busy on something else.

**Extended signals:**
- Roadmap reviews only ask "are these good ideas?" not "are these better than alternatives?"
- No mechanism exists for surfacing and comparing alternative uses of engineering time
- When a project delivers negligible value, the post-mortem focuses on execution, not on whether the opportunity was worth pursuing
- The team has no visibility into what is being deferred and the cumulative cost of those deferrals
- Leadership evaluates the roadmap against stakeholder requests rather than against market opportunities

**The compounding problem:**
Opportunity cost compounds with the 50% failure rate (Truth 1) and the iteration requirement (Truth 2). If half of all ideas fail, and good ideas need multiple iterations, and the team is executing a process that can't validate ideas cheaply before building them — the opportunity cost of alternative work (correctly prioritized, quickly validated ideas) grows with every sprint.
