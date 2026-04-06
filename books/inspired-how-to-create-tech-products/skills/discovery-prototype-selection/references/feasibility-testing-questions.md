# Feasibility Testing Questions

Source: INSPIRED by Marty Cagan, Chapter 55 (Testing Feasibility)

## The 10 Feasibility Questions Engineers Answer in Discovery

When engineers validate feasibility in discovery, they are trying to answer a set of related questions about whether and how the team can build a proposed solution:

1. **Do we know how to build this?** — Does the technical approach exist and is it understood?
2. **Do we have the skills on the team to build this?** — Are the required engineering capabilities present?
3. **Do we have enough time to build this?** — Within acceptable constraints, can this be delivered?
4. **Do we need any architectural changes to build this?** — Will this require significant platform or infrastructure changes?
5. **Do we have on hand all the components we need to build this?** — Are required libraries, services, and building blocks available?
6. **Do we understand the dependencies involved in building this?** — Are cross-team or cross-system dependencies identified and manageable?
7. **Will the performance be acceptable?** — Will the solution meet latency, throughput, or response time requirements?
8. **Will it scale to the levels we need?** — Can the solution handle the expected load?
9. **Do we have the infrastructure necessary to test and run this?** — Are the required environments and tooling available?
10. **Can we afford the cost to provision this?** — Are the operational costs (compute, storage, API costs, etc.) acceptable?

Most of the time, engineers will review product ideas in discovery and quickly say "No problem" — because most work is not all that new, and engineers have typically built similar things before.

Feasibility investigation is needed when one or more of these questions cannot be answered quickly.

---

## How to Structure Engineer-Led Feasibility Investigation

**The right question to ask:** Not "Can you do this?" but "What is the best way to do this, and how long would it take?" The first question invites a binary yes/no that puts engineers on the spot. The second question opens an investigation and invites engineering judgment.

**Give engineers time to investigate.** Holding a planning meeting and demanding instant estimates on ideas engineers have not had time to consider will produce conservative, inflated answers designed to make the questioner go away. Ambush estimation is a named anti-pattern (see main skill).

**Engineers who have been following discovery will estimate better.** If engineers have been present during discovery — watching users try prototypes, understanding the problems being solved — they will have already been thinking about feasibility for some time. Their estimates will be more accurate because they have context. This is another reason why engineers belong in discovery, not just delivery.

**When engineers say they need a feasibility prototype:** First consider whether the idea is potentially worth the necessary investigation time in discovery. If so, encourage engineers to proceed. The feasibility prototype answers the question; the product manager then decides whether to pursue the approach.

**What engineers produce:** A feasibility prototype — throwaway code that answers the specific feasibility question. No user interface, no error handling, no productization work. Just enough code to demonstrate whether the approach is viable.

---

## Feasibility Anti-Patterns

### Anti-pattern: Ambush Estimation

**What it looks like:** The product manager presents a list of ideas at a weekly planning meeting and asks engineers to estimate them in time or story points on the spot.

**Why it fails:** Engineers put on the spot without investigation time give conservative answers partly designed to make the questioner go away. The estimate is not a real estimate — it is a defensive answer. The team then makes decisions based on inflated numbers, systematically undervaluing complex but high-impact ideas.

**Correct approach:** Ask engineers "What is the best way to do this and how long would it take?" — and give them time to actually investigate before expecting an answer. If investigation requires a feasibility prototype, support that.

### Anti-pattern: Feasibility-Averse Product Management

**What it looks like:** The product manager refuses or avoids any product idea that engineers say requires time to investigate. The product manager treats "needs investigation" as equivalent to "too risky" and filters out these ideas systematically.

**Why it fails:** Many of the best product ideas are based on approaches that are only now possible — which means new technology that engineers need time to learn and evaluate. A product manager who avoids all such ideas systematically kills innovation. The most innovative opportunities are frequently the ones that require investigation because they are genuinely new.

**Three reasons to embrace feasibility investigation:**
1. Many best product ideas are based on newly possible technology — which by definition requires investigation time.
2. Engineers given even one or two days to investigate often return not just with feasibility answers but with better ways to solve the problem.
3. Feasibility investigation is often highly motivating for engineers — it gives them opportunity to learn and shine.

**Correct approach:** When engineers say they need time to investigate, treat it as an opportunity signal, not a risk signal. Evaluate whether the idea is worth the investigation time. If yes, encourage investigation.
