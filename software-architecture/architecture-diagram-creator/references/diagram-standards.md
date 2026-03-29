# Diagram Standards Reference

Detailed guide to architecture diagramming standards, element guidelines, and presentation techniques.

## Diagramming Standards

### UML (Unified Modeling Language)

UML was a standard that unified three competing design philosophies in the 1980s. While designed by committee and largely fallen out of widespread use, two diagram types remain valuable:

- **Class diagrams** — Still the most effective way to show object relationships and inheritance hierarchies
- **Sequence diagrams** — Still the best tool for illustrating workflow and interaction timing between components

Most other UML diagram types (use case, activity, state machine, deployment) have been superseded by lighter-weight alternatives.

**When to use UML:** When you need to show class structure or detailed service interaction sequences. When the organization mandates UML.

### C4 (Context, Container, Component, Class)

Developed by Simon Brown to address UML's deficiencies. C4 provides four zoom levels:

| Level | What it shows | Best audience | Example |
|-------|-------------|---------------|---------|
| **Context** | The entire system, including users and external dependencies | Everyone — executives, developers, ops | "Our system talks to these 3 external APIs and serves these 2 user types" |
| **Container** | Physical/logical deployment boundaries within the architecture | Operations, architects | "The web app, API server, and database are in separate containers" |
| **Component** | The internal structure of a container — its modules and their relationships | Architects, senior developers | "The API server has these 5 modules with these internal dependencies" |
| **Class** | Same as UML class diagrams | Developers | "This module has these classes with these relationships" |

**When to use C4:** For monolithic and service-based architectures where the container and component relationships create meaningful zoom levels. C4 is best suited for systems where the container (deployment unit) and component (module) distinction is clear.

**Limitations:** C4 is less suited for distributed architectures like microservices where:
- Each microservice IS a container AND a component simultaneously
- The interesting relationships are between services, not within them
- Container and component levels may be redundant

### ArchiMate

An open source enterprise architecture modeling language from The Open Group. ArchiMate is:
- A technical standard (not just a convention)
- Lighter-weight than UML ("as small as possible")
- Designed for description, analysis, and visualization across business domains

**When to use ArchiMate:** When modeling architecture that spans multiple business domains or when you need a standard that covers business, application, and technology layers in a single view.

## Diagram Element Guidelines

### Titles

- Every element must have a title or be universally known to the audience
- Use rotation and visual effects to make titles "stick" to their shapes
- Make efficient use of space — titles should not dominate the diagram

### Lines

- **Thickness:** Lines must be thick enough to see clearly, especially when projected
- **Direction:** Use arrows to indicate information flow direction. Use bidirectional arrows for two-way traffic
- **Arrowhead style:** Different arrowhead types suggest different semantics — be consistent within a diagram
- **The synchronous/asynchronous convention:**
  - **Solid lines** = synchronous communication (request-response, blocking)
  - **Dotted lines** = asynchronous communication (fire-and-forget, message queues, events)
  - This is one of the few near-universal standards in architecture diagrams

### Shapes

- **3D boxes** — Deployable artifacts (services, applications, servers)
- **Rectangles** — Containment, logical grouping, layers
- **Cylinders** — Databases and data stores (universally recognized)
- **No pervasive standard** — Each architect tends to build their own shape vocabulary
- **Build a stencil** — Create a library of standard shapes for your organization. This creates consistency across all architecture diagrams and speeds up diagram creation

### Labels

- Label every item in the diagram, especially if there is any chance of ambiguity
- When in doubt, add a label — the cost of a redundant label is near zero; the cost of ambiguity is high
- Label relationships (lines) with what is being communicated, not just the protocol

### Color

- Architects historically under-use color due to book printing being black-and-white
- Use color to **distinguish** artifacts from one another (e.g., different services in unique colors)
- Favor monochrome base with selective color over full-color schemes
- Color should carry semantic meaning (e.g., red = high risk, green = healthy)
- Never rely on color alone for meaning — always pair with labels or shapes for accessibility

### Keys

- If any shape is ambiguous, include a key on the diagram
- A diagram that leads to misinterpretation is worse than no diagram
- Keys should be visible without scrolling or paging
- For presentations: show the key on the first slide, then remove it to free space (the audience will remember)

## Tool Features to Look For

1. **Layers** — Link groups of elements together logically. Enable/disable layers to show different levels of detail. Essential for building incremental presentations from a single comprehensive diagram.
2. **Stencils/Templates** — Build reusable shape libraries for organizational consistency. Standard component shapes (microservice, database, queue, load balancer) should look identical across all diagrams.
3. **Magnets** — Automatic connection points on shapes for clean line routing. Create custom magnets for consistent visual style.
4. **Export formats** — Support for multiple output formats (PNG, SVG, PDF) for different contexts (docs, slides, wikis).

## Presentation Techniques

### Incremental Builds

The most powerful presentation technique for architecture diagrams:

1. Start with the complete diagram in your diagramming tool
2. Cover portions with **borderless white boxes** that hide sections
3. Use "build out" animations to remove the covers one at a time
4. Each build step reveals one new part of the architecture
5. Narrate each reveal — explain what it is and why it's there

**Why this works:** When presenting, you have two information channels: visual (slides) and verbal (speaker). Showing everything at once overloads the visual channel while starving the verbal channel. The audience reads ahead and stops listening. Incremental builds keep both channels synchronized.

**Anti-pattern: Bullet-Riddled Corpse** — Slides that are essentially the speaker's notes projected for all to see. If the slides contain everything, just email them as an infodeck instead.

### Manipulating Time

- Use **subtle transitions** (dissolve, fade) to stitch related slides into a continuous story
- Use **distinctly different transitions** (door, cube) to signal topic changes
- Avoid "splashy" transitions (dropping anvils, swirling effects) — they distract from content

### Infodecks vs Presentations

| Aspect | Infodeck | Presentation |
|--------|----------|-------------|
| **Delivery** | Emailed, read individually | Projected, narrated live |
| **Content** | Comprehensive — all information is in the slides | Sparse — slides + speaker = complete story |
| **Animations** | None needed | Essential for pacing |
| **Amount of text** | Full text, standalone | Minimal — keywords and visuals |

**Rule:** If you build comprehensive slides with no animations, you have an infodeck. Email it. Don't stand in front of it and read it aloud.

### Invisibility Pattern

Insert a **blank black slide** when you want to:
- Refocus attention solely on the speaker
- Make a key point that requires eye contact, not screen-staring
- Transition between major topics

When the visual channel goes dark, the verbal channel automatically gets amplified. The speaker becomes the only interesting thing in the room.

### Slides Are Half of the Story

- If the slides are comprehensive, spare everyone and email them
- If you are presenting, the slides should be half the content — you are the other half
- Adding less text to slides makes spoken points land with more impact
- Presenters who put everything on slides make themselves redundant

## The Irrational Artifact Attachment Anti-Pattern

**Definition:** The proportional relationship between time invested in creating an artifact and irrational attachment to it. A four-hour diagram creates more attachment than a two-hour one.

**Why it matters:** Attached architects resist revising designs they should change because they don't want to "waste" the time invested in the diagram. This is classic sunk-cost fallacy applied to architecture.

**Prevention:**
- In early design phases, use low-fidelity tools: whiteboards, tablets, sticky notes, index cards
- Use tablets attached to overhead projectors instead of physical whiteboards (unlimited canvas, easy to save, no glare from cell phone photos)
- Only invest in high-fidelity diagramming tools once the design has stabilized through iteration
- Follow the Agile principle: create just-in-time artifacts with as little ceremony as possible

**Benefits of low-fidelity:**
- Team members throw away what's not working without guilt
- The true nature of the architecture emerges through revision, collaboration, and discussion
- Faster iteration cycles — sketching takes minutes, not hours
