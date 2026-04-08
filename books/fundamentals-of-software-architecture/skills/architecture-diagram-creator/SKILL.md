---
name: architecture-diagram-creator
description: Create effective architecture diagrams following established diagramming standards (UML, C4, ArchiMate) with proper visual elements and presentation techniques. Use this skill whenever the user needs to create, review, or improve architecture diagrams, wants guidance on which diagramming standard to use, needs help with diagram elements (titles, lines, shapes, labels, color, keys), is preparing architecture presentations with slides, wants to use incremental builds for presenting complex diagrams, is struggling with inconsistent notation across diagrams, or needs to maintain representational consistency across different zoom levels of their architecture — even if they don't explicitly say "diagram."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-diagram-creator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [21]
tags: [software-architecture, architecture, diagrams, presentation, UML, C4, ArchiMate, communication, visual]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "Architecture context from the user — system components, relationships, communication patterns, and target audience"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. No codebase required."
---

# Architecture Diagram Creator

## When to Use

You need to create or improve architecture diagrams that effectively communicate system design. Typical triggers:

- The user needs to create a new architecture diagram and wants guidance on standards and best practices
- The user has existing diagrams with inconsistent notation and wants to standardize them
- The user is preparing a presentation of their architecture and wants advice on visual communication
- The user is choosing between diagramming standards (UML, C4, ArchiMate)
- The user has diagrams at different zoom levels that don't connect visually
- The user is spending too much time perfecting diagrams early in the design process (Irrational Artifact Attachment)

Before starting, verify:
- What system or architecture needs to be diagrammed?
- Who is the audience (developers, executives, operations, mixed)?

## Context

### Required Context (must have before proceeding)

- **System to diagram:** What system, service, or architecture needs visual representation?
  -> Check prompt for: system names, service descriptions, component lists, technology mentions
  -> If still missing, ask: "What system or architecture do you need to diagram? Can you describe its main components and how they communicate?"

- **Target audience:** Who will view these diagrams?
  -> Check prompt for: "developers," "CTO," "stakeholders," "team," presentation context
  -> If still missing, ask: "Who is the primary audience for this diagram — developers, executives, operations, or a mix?"

### Observable Context (gather from environment)

- **Existing diagrams:** Are there existing diagrams that need improvement or consistency fixes?
  -> Check prompt for: references to current diagrams, notation complaints, inconsistency mentions
  -> If unavailable: assume creating from scratch

- **Diagramming tool:** What tool is being used?
  -> Check prompt for: tool names (Mermaid, PlantUML, draw.io, Lucidchart, OmniGraffle, Visio)
  -> If unavailable: provide tool-agnostic guidance

- **Architecture style:** What architecture pattern is the system using?
  -> Check prompt for: microservices, monolith, event-driven, layered, service-based
  -> If unavailable: infer from component descriptions

### Default Assumptions

- If audience unknown -> assume mixed technical audience (developers + architects)
- If tool unknown -> provide text-based diagram descriptions and general guidelines
- If zoom level unknown -> start with the Container level (C4 terminology) as the most commonly useful view

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- System components and relationships are known or described
- Target audience is known or can be inferred
- Communication patterns (sync/async) are understood

PROCEED WITH DEFAULTS when:
- System is described at a high level
- Audience can be assumed as technical
- Standard architecture pattern is used

MUST ASK when:
- No system description is provided at all
- The request is ambiguous between creating vs reviewing diagrams
```

## Process

### Step 1: Select the Appropriate Diagramming Standard

**ACTION:** Based on the system type, audience, and organizational context, recommend a diagramming standard.

**WHY:** Different standards serve different purposes. UML is universally understood for class and sequence diagrams but most other diagram types have fallen into disuse. C4 provides four natural zoom levels ideal for monolithic architectures where container and component relationships matter. ArchiMate serves enterprise-level modeling across business domains. Choosing the wrong standard wastes time and confuses the audience.

| Standard | Best For | Limitations |
|----------|----------|-------------|
| **UML** | Class diagrams, sequence diagrams, workflow | Most diagram types are disused; overly formal for architecture overviews |
| **C4** | Systems with clear container and component boundaries; monolithic and service-based | Less suited for distributed architectures like microservices where container/component relationships differ |
| **ArchiMate** | Enterprise architecture spanning business domains | Heavier; overkill for single-system diagrams |
| **Custom notation** | When no standard fits perfectly | Requires a key; risk of misinterpretation without one |

**IF** the user's organization mandates a standard -> use that standard
**IF** the system is a monolith or service-based -> recommend C4 for its four zoom levels (Context, Container, Component, Class)
**IF** the system spans multiple business domains -> recommend ArchiMate
**IF** the need is class structure or workflow -> recommend UML (class/sequence diagrams only)
**ELSE** -> recommend custom notation with a clear key

### Step 2: Check for Irrational Artifact Attachment Risk

**ACTION:** Assess whether the user is at risk of the Irrational Artifact Attachment anti-pattern — spending disproportionate time creating beautiful diagrams before the design is stable.

**WHY:** There is a proportional relationship between how long it takes to produce an artifact and how irrationally attached a person becomes to it. A four-hour diagram creates more attachment than a two-hour one. This attachment prevents architects from revising designs when they should, because they don't want to "waste" the time invested. Early in design, use low-fidelity tools (whiteboards, tablets, sticky notes) so the team feels free to throw away and iterate.

**IF** the user is in early design phase -> recommend low-fidelity tools first (whiteboard, tablet, index cards)
**IF** the user has a stable, finalized architecture -> recommend investing in high-fidelity diagrams
**IF** the user mentions spending hours perfecting diagrams -> flag Irrational Artifact Attachment and recommend reducing tool investment until the design stabilizes

### Step 3: Apply Diagram Element Guidelines

**ACTION:** For each diagram, ensure all six core visual elements are properly used. For detailed standards and examples, see [references/diagram-standards.md](references/diagram-standards.md).

**WHY:** Each element serves a specific communication purpose. Missing or misused elements create ambiguity, and a diagram that leads to misinterpretation is worse than no diagram at all.

**Elements to verify:**
1. **Titles** — Every element must have a title or be well-known to the audience. Use rotation and visual effects to make titles "sticky" to their shapes.
2. **Lines** — Must be thick enough to see clearly. Solid lines = synchronous communication. Dotted lines = asynchronous communication. Use arrows for directional flow. Be consistent with arrowhead styles.
3. **Shapes** — Use 3D boxes for deployable artifacts, rectangles for containment. Build a stencil of standard shapes for organizational consistency.
4. **Labels** — Label every item, especially if there is any ambiguity. When in doubt, label.
5. **Color** — Use sparingly to distinguish artifacts from one another (e.g., different services in different colors). Favor monochrome with selective color over full-color chaos.
6. **Keys** — If shapes are ambiguous, include a key explaining what each shape represents. A misinterpreted diagram is worse than no diagram.

### Step 4: Ensure Representational Consistency

**ACTION:** If producing multiple diagrams at different zoom levels, ensure each maintains visual context showing where it fits in the larger architecture.

**WHY:** When an architect shows a portion of the architecture without indicating where it fits in the overall system, viewers lose context and become confused. Representational consistency means always showing the relationship between parts and the whole, either in diagrams or presentations, before changing views. For example, when drilling from a system overview into a specific service, first show the overview with the target service highlighted, then zoom into it.

**IF** creating multiple views -> include a small context indicator showing which part of the larger system is being detailed
**IF** presenting to an audience -> use the overview-then-zoom pattern: show the full system, highlight the area of focus, then drill in

### Step 5: Apply Presentation Techniques (if presenting)

**ACTION:** If the diagrams will be presented (not just shared as documents), apply presentation-specific techniques.

**WHY:** Presentations and documents are fundamentally different media. In a presentation, the presenter controls how quickly an idea unfolds (manipulating time). In a document, the reader controls the pace. Treating a presentation as a document (Bullet-Riddled Corpse anti-pattern) wastes the presenter's most powerful tool: controlling the narrative flow.

**Techniques:**
- **Incremental Builds:** Never show a complex diagram all at once. Build it piece by piece using animations. Cover parts of the diagram with borderless white boxes, then use "build out" animations to reveal sections as you narrate. This maintains suspense and keeps the audience engaged.
- **Manipulating Time:** Use subtle transitions and dissolves to stitch slides into a continuous story. Use distinctly different transitions (door, cube) to signal topic changes.
- **Infodecks vs Presentations:** If the slides will be emailed, not presented, they are an "infodeck" — include all information, skip animations. If they will be presented live, slides should be half the story (the other half is the speaker).
- **Slides Are Half of the Story:** Don't put everything on the slide. The presenter is the other information channel. Adding less text to slides gives more punch to spoken points.
- **Invisibility:** Insert blank black slides when you want to refocus attention on the speaker. Turning off the visual channel automatically amplifies the verbal channel.

### Step 6: Generate the Diagram Specification

**ACTION:** Produce a complete diagram specification including all components, relationships, communication types, labels, and visual guidelines.

**WHY:** A specification serves as both the blueprint for creating the diagram in any tool and as documentation of what the diagram should contain. It prevents the "I drew it from memory" syndrome where critical elements get omitted.

## Inputs

- System description (components, services, data stores, external systems)
- Communication patterns (synchronous REST, asynchronous messaging, etc.)
- Target audience and purpose
- Optionally: existing diagrams to review, organizational standards, preferred tools

## Outputs

### Architecture Diagram Specification

```markdown
# Architecture Diagram: {System Name}

## Diagram Metadata
- **Standard:** {UML / C4 / ArchiMate / Custom}
- **C4 Level:** {Context / Container / Component / Class} (if C4)
- **Audience:** {who will view this}
- **Purpose:** {what decision or understanding this supports}

## Components

| ID | Name | Type | Description |
|----|------|------|-------------|
| 1  | {name} | {service/database/queue/external} | {what it does} |

## Relationships

| From | To | Type | Protocol | Label |
|------|----|------|----------|-------|
| {source} | {target} | sync/async | {REST/gRPC/AMQP/etc.} | {what is communicated} |

## Visual Guidelines
- **Line styles:** Solid = synchronous, Dotted = asynchronous
- **Colors:** {color scheme with rationale}
- **Shapes:** {shape conventions}
- **Key:** {if custom shapes are used}

## Presentation Notes (if applicable)
- **Build order:** {sequence for incremental reveals}
- **Narration points:** {what to say at each build step}
```

## Key Principles

- **Representational consistency is non-negotiable** — WHY: Viewers who see a zoomed-in diagram without context for where it fits in the overall architecture will misunderstand the scope and boundaries. Always show the relationship between parts and the whole before changing zoom levels.

- **Solid lines = synchronous, dotted lines = asynchronous is a universal standard** — WHY: This is one of the few diagram conventions that exists across the software industry. Violating it confuses everyone who has learned this convention, and most architects have. If you must deviate, include a key.

- **Low-fidelity early, high-fidelity late** — WHY: The Irrational Artifact Attachment anti-pattern causes architects to defend designs they should revise, simply because they invested hours in the diagram. Using whiteboards and sticky notes early frees the team to iterate without sunk-cost bias.

- **A misinterpreted diagram is worse than no diagram** — WHY: Diagrams carry authority. If a diagram is ambiguous and someone interprets it wrong, they will build or operate the system based on that wrong interpretation with high confidence. When in doubt, add labels and keys.

- **Incremental builds make presentations compelling** — WHY: The human brain cannot resist reading text that appears on screen. Showing a complex diagram all at once forces the audience to read ahead of the presenter, splitting their attention. Building the diagram piece by piece keeps narrator and visual in sync.

- **The presenter is half the presentation** — WHY: Slides have two information channels: visual (slides) and verbal (speaker). Overloading the visual channel by putting everything on slides starves the verbal channel and makes the presenter redundant. The best presentations have sparse slides and a compelling narrator.

## Examples

**Scenario: Creating a microservices architecture diagram**
Trigger: "I need to create an architecture diagram for our microservices system with 6 services, an API gateway, message queue, and 3 databases."
Process: Selected custom notation over C4 (C4 is less suited for distributed microservices where container/component relationships differ). Applied the six element guidelines: assigned each service a distinct color, used solid lines for synchronous REST calls and dotted lines for asynchronous message queue communication, labeled every relationship with the protocol and data exchanged. Included a key explaining shapes (3D boxes = deployable services, cylinders = databases, hexagon = API gateway). Recommended incremental build order for presentation: start with the API gateway, build out to the services one by one, then show the async communication layer.
Output: Complete diagram specification with component table, relationship matrix, visual guidelines, and presentation build order.

**Scenario: Standardizing inconsistent team diagrams**
Trigger: "Our team has different diagrams at different zoom levels using inconsistent notation."
Process: Recommended adopting C4 as the standard since the system has clear context, container, and component boundaries. Created a notation guide: specific shapes for each component type, consistent color palette, solid/dotted line convention. For each existing diagram, identified which C4 level it corresponds to and added representational consistency indicators (small overview diagram in the corner showing which part is detailed). Created a shared stencil template for the team's diagramming tool.
Output: Notation standard document, C4 level mapping for existing diagrams, shared stencil template, and diagram review checklist.

**Scenario: Preparing architecture presentation for executives**
Trigger: "I'm presenting our new event-driven architecture to the CTO next week. I have 15 slides full of bullet points."
Process: Flagged the Bullet-Riddled Corpse anti-pattern — slides full of text that the presenter reads aloud. Redesigned the presentation using incremental builds: replaced bullet point slides with a single architecture diagram revealed in 6 build steps, each narrated by the presenter. Added invisibility slides (blank black slides) before key decision points to refocus attention on the speaker. Converted detailed technical content to an infodeck appendix for email distribution after the meeting. Advised: "slides are half the story — you are the other half."
Output: Restructured 15-slide deck into 8 slides with incremental builds, 3 invisibility slides, and a 12-page infodeck appendix.

## References

- For detailed diagramming standards, element guidelines, C4 level descriptions, and notation conventions, see [references/diagram-standards.md](references/diagram-standards.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
