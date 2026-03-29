# Domain Concern to Architecture Characteristic Mapping

Use this table to translate business/stakeholder language into architecture characteristics. This is the bridge between "what the business cares about" and "what the architect designs for."

## Primary Mapping Table

| Domain Concern | Architecture Characteristics |
|----------------|------------------------------|
| Mergers and acquisitions | Interoperability, scalability, adaptability, extensibility |
| Time to market | Agility, testability, deployability |
| User satisfaction | Performance, availability, fault tolerance, testability, deployability, agility, security |
| Competitive advantage | Agility, testability, deployability, scalability, availability, fault tolerance |
| Time and budget | Simplicity, feasibility |
| Regulatory compliance | Auditability, security, legal, privacy, recoverability |
| Global expansion | Localization, scalability, legal, data residency |
| Cost reduction | Simplicity, feasibility, maintainability |
| Innovation speed | Agility, extensibility, testability, deployability |
| Customer trust | Security, reliability, availability, privacy |
| Operational efficiency | Performance, observability, automation, maintainability |

## Translation Warnings

**"Agility" is NOT "time to market."** Agility = agility + testability + deployability. Focusing on only one ingredient produces an incomplete architecture.

**One concern → many characteristics.** "Complete end-of-day fund pricing on time" implies performance + availability + scalability + reliability + recoverability + auditability. A single business statement can expand to 6+ architecture characteristics.

**Don't transcribe, translate.** The stakeholder's exact words are domain language. Your job is to decode the underlying technical needs, not echo the business terminology back as a characteristic name.

## Probing Questions by Domain

When stakeholders state a concern, use these questions to uncover the full set of characteristics:

| They say... | Ask... | Reveals... |
|------------|--------|-----------|
| "It needs to be fast" | "Fast for whom? Under what load? At what percentile?" | Performance vs scalability vs elasticity |
| "We might get acquired" | "By whom? What systems would need to integrate?" | Interoperability, adaptability, data portability |
| "Security is important" | "Important enough to influence architecture? Or standard best practices?" | Whether security is a design concern or architecture characteristic |
| "We need to scale" | "Scale how? More users (scalability)? Burst traffic (elasticity)? More features (extensibility)?" | The specific type of scaling needed |
| "Budget is tight" | "Tight for build or for operations? Short term or long term?" | Simplicity vs maintainability vs feasibility |
