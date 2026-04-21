# Interface Style Selector

Source: Patterns of Enterprise Application Architecture, Ch 7 (Interfaces for Distribution) — Fowler, extended with modern options

## Fowler's Original Guidance (2002)

- **RPC-style** (CORBA, RMI): Both sides same platform → use native binary mechanism. Avoid XML overhead.
- **XML over HTTP** (SOAP): Cross-platform communication, firewall traversal, public APIs. More interoperable, more overhead.
- Principle: "Use XML Web services only when a more direct approach isn't possible."

The principle holds today. Substitute gRPC for RMI/CORBA and REST/JSON for SOAP/XML.

## Modern Decision Matrix

| Style | Coupling | Latency | Async? | Browser-native? | Best for |
|-------|----------|---------|--------|-----------------|----------|
| **gRPC** (binary, proto) | Tight (schema-first) | Low | Streaming (not fire-and-forget) | No (needs grpc-web proxy) | Internal service-to-service, high throughput, same-platform |
| **REST / JSON** | Loose (URL + JSON) | Medium | No (HTTP/2 streams possible) | Yes | External APIs, browser clients, public/partner APIs, cross-platform |
| **Message queue** (Kafka, SQS, RabbitMQ) | Very loose (event schema) | High tolerance | Yes — async only | No | Fire-and-forget, event-driven, decoupled producers/consumers, high-volume ingest |
| **GraphQL** | Medium (schema-typed) | Medium | Subscriptions | Yes | Multi-client (mobile + web) with varying field needs, avoiding over-fetch, developer experience |

## Selection Heuristics

**Use gRPC when:**
- Both sides are controlled by your team and share the same platform or can consume proto-generated clients
- Low latency and high throughput are required (e.g., internal order processing, payment authorization)
- You want schema-first API contracts with strong typing

**Use REST/JSON when:**
- External clients (browsers, mobile apps, third parties) consume the API
- Cross-platform interoperability matters
- Developer experience / debuggability > raw performance
- The API is public or exposed to partners

**Use message queue when:**
- The call is fire-and-forget (no immediate response needed)
- The producer should not be blocked by consumer availability or speed
- High latency tolerance (seconds, not milliseconds)
- Event-driven architecture or data pipeline
- Examples: order placed → fulfillment service picks up from queue; audit log events; notification dispatch

**Use GraphQL when:**
- Multiple client types with different field subsets (mobile shows 3 fields; desktop shows 20)
- You want to avoid REST over-fetching / under-fetching
- Schema introspection and developer tooling matter
- Consider the N+1 risk: server-side resolvers must batch (DataLoader pattern) to avoid per-field DB queries

## Combining Styles

It is common and correct to use different styles at different boundaries:
- Internal services → gRPC
- External / public API → REST/JSON (possibly generated from proto schemas via gRPC-gateway)
- Async event flows → message queue
- Mobile-specific → GraphQL over REST

The Remote Facade pattern applies to all of these: design the interface as a coarse-grained use-case-shaped contract, implement it with whichever transport style is appropriate.
