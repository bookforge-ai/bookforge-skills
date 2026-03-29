# Online Auction System — Mock Codebase

Mock environment for testing the `architecture-quantum-analyzer` skill.

## Scenario

An online auction platform ("Going Going Gone") with four services that form
three distinct architecture quanta based on their deployment boundaries,
communication styles, and architecture characteristics.

## Services

| Service | Port | Purpose |
|---------|------|---------|
| Bidder Service | 8001 | Bid placement — burst traffic during live auctions |
| Auction Service | 8002 | Auction lifecycle management |
| Payment Service | 8003 | Post-auction payment processing |
| Notification Service | 8004 | Email/SMS delivery |

## Expected Quanta

1. **Bidding Quantum** (Bidder + Auction) — synchronous REST coupling,
   shared scalability needs. Deploys together. Key characteristics:
   elasticity, performance.

2. **Payment Quantum** (Payment alone) — asynchronous consumer of auction
   events. Independent deploy cadence. Key characteristics: reliability,
   security.

3. **Notification Quantum** (Notification alone) — asynchronous consumer
   of auction events. Independent deploy cadence. Key characteristics:
   availability.

## Communication Map

```
Bidder ──REST──► Auction ──MQ──► Payment
                    │
                    └──MQ──► Notification
```

## Running

```bash
docker-compose up --build
```
