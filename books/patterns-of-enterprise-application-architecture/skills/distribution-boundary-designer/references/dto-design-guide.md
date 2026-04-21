# DTO Design Guide

Source: Patterns of Enterprise Application Architecture, Ch 15 (Data Transfer Object) — Fowler

## Pattern Intent

A Data Transfer Object carries data between processes in a single method call, reducing call count. It is a serializable data holder with no domain behavior.

## Core Rules

1. **No behavior** — only data fields and serialization logic
2. **Serializable independently** of the domain model
3. **Fields are primitives, strings, dates, or nested DTOs** — not domain object references
4. **Designed around client interaction needs**, not domain class structure
5. **Separated from domain objects by an Assembler** — neither the DTO nor the domain object depends on the other

## Assembler Pattern

The Assembler is a Mapper that lives on the server side:
- Populates DTOs from domain objects (for responses)
- Updates domain objects from DTOs (for commands/updates)

The Assembler is separate because:
- DTOs may need to be deployed on both sides of the wire without domain classes
- Domain model must not depend on wire format (wire format changes more often than domain invariants)
- Auto-generating DTOs is easy; auto-generating assemblers is hard — keeping them separate allows manual control of the translation

## DTO Structural Guidelines

**Collapse related objects:** If the client always needs the artist name when viewing an album, embed `artistName: string` in `AlbumDTO` rather than requiring a separate `ArtistDTO` call.

**Hierarchical, not graph:** DTOs should form a tree (album → tracks → performers), not a graph with back-references. Domain models often have complex bidirectional references; DTOs flatten or simplify these.

**Aggregation scope:** A single DTO typically carries data from multiple domain objects. If a screen needs order + customer + line items + delivery info, that's one DTO with nested sub-DTOs.

**Err toward over-sending:** Include related data the client might need in the near future. The cost of a second call exceeds the cost of modest over-fetching.

## Request vs Response DTOs

- If request and response shapes are similar → single DTO (mutable, populated differently)
- If they diverge significantly → separate `OrderRequestDTO` and `OrderResponseDTO`
- Fowler prefers mutable DTOs (easier to populate incrementally)

## Serialization Format Trade-offs

| Format | Pros | Cons | Use when |
|--------|------|------|----------|
| Binary (Java serialization, .NET binary) | Fast, compact | Fragile — any schema change breaks old clients | Both sides fully controlled and versioned together |
| JSON | Human-readable, widely supported, tolerant of adding optional fields | Larger payload, slower parsing | REST APIs, browser clients, cross-platform |
| XML / SOAP | Maximum interoperability, tooling support | Verbose, slower | Legacy integration, SOAP contracts |
| gRPC / protobuf | Fast, strongly typed, schema-first | Requires proto compiler, not browser-native | Internal service-to-service, high throughput |
| Dictionary/Map (binary) | Tolerant of field additions — old clients skip unknown keys | Loses strong typing, no explicit interface | When tolerance matters more than type safety |

## Modern Parallels

| Fowler DTO concept | Modern equivalent |
|--------------------|-------------------|
| DTO class with getters/setters | Java record, Kotlin data class, Python dataclass, TypeScript interface |
| XML serialization | JSON (Jackson, Gson, System.Text.Json) |
| Binary serialization | gRPC proto message, Avro record, Thrift struct |
| Assembler | MapStruct (Java), AutoMapper (.NET), manual mapper function |
| DTO designed per screen | GraphQL fragment, OpenAPI response schema, REST response body |

## DTO vs Value Object (Naming Clarification)

- **Fowler's DTO**: a data carrier for the wire — no behavior, serializable, designed per use case
- **Fowler's Value Object**: an immutable object whose identity is defined by its values (e.g., Money, DateRange, Address) — NOT for wire transfer
- **J2EE community "Value Object"**: what Fowler calls DTO — this naming collision caused significant confusion

## Common Anti-Patterns

| Anti-Pattern | Description | Remedy |
|--------------|-------------|--------|
| DTO mirrors domain class 1:1 | Auto-generated DTOs for every entity; one DTO per domain class | Design DTOs around use-case interactions, collapse related data |
| Domain object in DTO field | DTO references a domain class directly | Replace with primitive fields or nested DTO |
| Behavior in DTO | Business logic or validation in DTO methods | Move to domain objects or validators; DTO = data only |
| Over-split DTOs | Separate DTO per property group, requiring multiple calls to populate a screen | Consolidate into one use-case-shaped DTO |
