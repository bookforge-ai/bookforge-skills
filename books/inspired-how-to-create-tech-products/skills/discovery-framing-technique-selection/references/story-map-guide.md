# Story Map Guide

## Origin and Purpose

Story maps were created by Jeff Patton (documented in *User Story Mapping*, O'Reilly, 2014) to solve a fundamental problem with flat backlogs: a prioritized list of stories has no context. You cannot tell from a flat backlog how one story relates to another, what a meaningful release looks like, or how the system grows over time.

A story map restores the two dimensions that a flat backlog strips away: the user experience over time (horizontal) and the level of detail/criticality (vertical).

## Construction Reference

### Horizontal Axis: User Activities

User activities are the major things a user does with a product. They are higher-level than user stories. Examples:

- For an e-commerce product: Browse → Search → Select → Configure → Checkout → Track → Return
- For a project management tool: Create project → Add tasks → Assign work → Track progress → Report
- For a finance app: Onboard → Connect accounts → View balances → Categorize transactions → Set budgets → Review reports

Rules:
- Order activities left to right as a user would encounter them
- Use verb + noun format (activity, not feature)
- Aim for 5–12 activities; more than 15 suggests you are operating at task level, not activity level
- Activities are the stable backbone of the map — they change infrequently

### Vertical Axis: Tasks Under Each Activity

Under each activity, list the specific tasks a user performs to accomplish that activity. Tasks are roughly equivalent to user stories in granularity.

Rules:
- Place the most critical tasks near the top (critical = must exist for the product to be functional)
- Place optional, edge-case, or enhancement tasks lower
- There is no required number of tasks per activity
- Tasks can be added as discovery progresses — the map grows as you learn

### The Release Line

Drawing a horizontal line across the map at any vertical position defines a release:
- Everything above the line: in scope for this release
- Everything below the line: explicitly deferred

This is fundamentally better than backlog prioritization because:
- The release is defined by user experience completeness, not arbitrary priority numbers
- Every team member can see at a glance what ships and what does not
- Deferred items are acknowledged, not forgotten

Draw the release line to define the minimum release that delivers meaningful value to the target user — not the minimum to call it "done" internally.

### Keeping the Map Current

Update the story map after every significant discovery finding:
- Prototype testing reveals an activity you did not model → add it
- Customer interviews reveal a task you thought was critical is actually optional → move it below the line
- Engineering feasibility spike reveals a critical task is infeasible in release 1 → move below the line with a note

When discovery transitions to delivery: tasks above the release line move into the product backlog as user stories, with the full map as context.

## When a Story Map Is and Is Not Needed

**Use a story map when:**
- The effort involves 5 or more distinct user activities
- You need to scope discovery into phases or releases
- The team needs a shared visual of the system before prototyping begins
- Multiple team members have different mental models of the user experience

**Skip a story map when:**
- The effort is a single focused feature within one well-understood activity
- The opportunity assessment framing is sufficient and the team is already aligned on scope
- The team has extensive existing context and a story map would duplicate knowledge already shared
