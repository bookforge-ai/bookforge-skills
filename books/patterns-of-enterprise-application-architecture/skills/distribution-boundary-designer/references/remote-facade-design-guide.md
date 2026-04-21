# Remote Facade Design Guide

Source: Patterns of Enterprise Application Architecture, Ch 15 (Remote Facade) — Fowler

## Pattern Intent

A Remote Facade is a **coarse-grained facade over a web of fine-grained objects** that provides efficient remote access to a domain model that would otherwise be chatty.

## Core Rules

1. **No domain logic in the facade.** "Repeat after me three times: Remote Facade has no domain logic." The facade translates coarse → fine. Logic lives in domain objects.
2. **Thin delegation.** Each facade method should be 1-3 lines, delegating to domain objects or a non-remote Service Layer.
3. **Coarse-grained methods.** One call does one unit of useful work. Not one getter per property.
4. **Few facades, many methods.** A moderate application may have one facade; a large application, half a dozen.

## Method Design Heuristics

Good Remote Facade method shapes:
- **Bulk accessor**: `getAddressData(customerId) → AddressDTO` — returns everything the client needs about an address in one call
- **Use-case command**: `submitOrder(orderId, paymentDTO) → OrderConfirmationDTO` — performs a complete business operation
- **Screen loader**: `loadOrderScreen(orderId) → OrderScreenDTO` — loads all data for a specific screen
- **Status command**: `changeOrderStatus(orderId, status)` — a single button-press action

Bad Remote Facade method shapes (distribution-by-class):
- `getCity(addressId)`, `getState(addressId)`, `getZip(addressId)` — three calls for three properties
- `getOrder(orderId)`, `getOrderLines(orderId)`, `getProducts(orderId)` — three calls to display one screen

## Granularity Decision

Fowler prefers very few, very coarse facades. Design facades around **client families** (a group of related screens or operations), not around domain classes.

Example — music domain:
- One `AlbumService` facade handles: `getAlbum`, `createAlbum`, `updateAlbum`, `getArtist`, `addArtist`
- Not: separate `AlbumService`, `ArtistService`, `TrackService` facades

## Remote Facade vs Session Facade (J2EE)

| | Remote Facade (Fowler) | Session Facade (J2EE community) |
|--|------------------------|----------------------------------|
| Contains domain logic? | No — thin skin only | Often yes — workflow coordination |
| Domain objects | Fine-grained POJOs inside | Entity beans or services |
| Correctness | Correct pattern | Anti-pattern per Fowler |

If your "Remote Facade" has conditional logic, workflows, or business rules — it is a Session Facade with leaked domain logic, not a Remote Facade. Move the logic to domain objects.

## Stateful vs Stateless

- **Stateless facade**: Can be pooled; better for high-concurrency B2C scenarios. Requires external session state (Client Session State / Database Session State).
- **Stateful facade**: Holds session state itself; simpler to implement. May become a bottleneck under high user concurrency.

## Security and Transaction Boundaries

The Remote Facade is the correct place for:
- **Access control**: Check permissions at facade method entry
- **Transaction demarcation**: Begin transaction before calling domain objects; commit after

These are infrastructure concerns, not domain logic.

## Testing

Because the facade has no domain logic, you can test domain behavior without deploying the remote shell. Instantiate the facade bean/class directly and test in-process. This is a feature, not a workaround — it confirms the facade has no logic worth testing.

## Modern Equivalents

| Classic | Modern |
|---------|--------|
| EJB Session Bean | gRPC service implementation |
| SOAP Web Service interface | REST controller / OpenAPI endpoint |
| CORBA interface | gRPC .proto service definition |
| RMI interface | Java/Kotlin gRPC stub |
