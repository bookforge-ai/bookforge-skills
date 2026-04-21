# Distribution Reasons Checklist

Source: Patterns of Enterprise Application Architecture, Ch 7 (Distribution Strategies) — Fowler

## The First Law

**Don't distribute your objects.**

Any inter-process call is orders of magnitude more expensive than an in-process call — even when both processes are on the same machine. This cost is paid on every call, forever.

## Legitimate Reasons to Distribute

Pass this checklist before committing to a process boundary. Distribute only if one or more applies:

| # | Reason | Question to Ask |
|---|--------|-----------------|
| 1 | **Client-server machine divide** | Do clients run on physically different machines from the server? (e.g., desktop PCs vs shared server, browser vs app server) |
| 2 | **Application server ↔ database** | Is the database in a separate process? (Almost always yes. SQL is designed as a remote interface; this cost is unavoidable but minimizable.) |
| 3 | **Web server and app server separation** | Is a separate web server process required by vendor constraints, security policy, or independent scaling? |
| 4 | **Independent scaling requirements** | Does a hot subsystem need to scale at a dramatically different rate than the rest? (e.g., 50x load differential) |
| 5 | **External vendor / package software** | Does a purchased package run in its own process with a coarse-grained interface? |
| 6 | **Security zone boundary** | Is a firewall or network zone required between subsystems? (e.g., PCI-DSS, DMZ, internal vs external) |
| 7 | **Different hardware or OS requirements** | Does a subsystem require specialized hardware, a different OS, or a different language runtime that cannot coexist in one process? |

## Non-Reasons (Do Not Distribute For These)

| Non-Reason | Why It Is Not Sufficient | Correct Alternative |
|------------|--------------------------|---------------------|
| "We want microservices" (trend) | Distribution costs are real; trend is not a force | Modular monolith with clear package boundaries |
| "Clean architecture / separation of concerns" | SoC is achievable within a process via packages, modules, or bounded contexts | Package-level separation, not process separation |
| "Conway's Law / team size" | Teams can own packages within a monolith; process boundaries are not required for team autonomy | Package ownership per team |
| "Polyglot language preference" | Distribution to use a different language has enormous operational cost | Choose a shared language or isolate via a truly necessary boundary |
| "Independent deployment" (without operational need) | If deploys are cheap (CI/CD), the benefit rarely outweighs the cost | Feature flags, versioned packages, trunk-based development |

## Decision Rule

If NONE of the seven legitimate reasons apply → **Modular monolith**. Structure the application with clear package/module interfaces; defer distribution until a legitimate operational reason emerges.

If one or more apply → Distribute ONLY the subsystem pairs that cross that specific boundary. Every other pair stays in-process.
