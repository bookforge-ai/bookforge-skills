# Facilitation Plan: API Gateway Performance Risk Session

## Overview

With 10,000 requests/second going through your API gateway, it's critical to identify performance risks collaboratively with your platform team. Here's a plan for running this session.

## Session Details

- **Team:** 8 platform team members
- **Duration:** 60 minutes
- **Format:** Workshop/discussion

## Agenda

### 1. Current State Review (10 minutes)
- Share current performance metrics (latency, throughput, error rates)
- Show the API gateway architecture diagram
- Identify which components are in the critical request path

### 2. Risk Identification (20 minutes)
- Go around the table — each person shares their top performance concern
- Capture all risks on a whiteboard or shared document
- Group similar concerns together

### 3. Risk Prioritization (15 minutes)
- For each risk, vote on severity: Critical, High, Medium, Low
- Use dot voting (each person gets 3 dots to place on their top concerns)
- Focus discussion on the top 5 risks

### 4. Mitigation Planning (15 minutes)
- For the top 3 risks, discuss potential solutions
- Assign investigation tasks
- Set follow-up meeting date

## Key Performance Risks to Explore

1. **Latency at scale** — What's the p99 latency at 10k req/s? Is it acceptable?
2. **Connection pooling** — Are connections to upstream services properly pooled?
3. **Authentication overhead** — Is auth adding significant latency per request?
4. **Caching effectiveness** — What's the cache hit rate? What happens on misses?
5. **Logging overhead** — Is synchronous logging slowing down requests?
6. **Thread/goroutine limits** — Can the gateway handle 10k concurrent connections?
7. **Memory pressure** — Is the gateway running out of memory under load?

## Preparation Steps

1. Collect current performance metrics (p50, p95, p99 latency)
2. Run a load test at current production levels to establish baseline
3. Create an architecture diagram showing the request flow
4. Identify any recent performance incidents or degradation

## Output

After the session, produce:
- Prioritized list of performance risks
- Top 3 mitigation actions with owners
- Load testing plan to validate assumptions
- Performance SLOs for the API gateway

## Tips for Facilitation

- Start with data — share actual metrics before opinions
- Use timeboxing to keep discussions focused
- Encourage quieter team members to share their observations
- Capture action items in real-time
- Schedule a follow-up session in 2 weeks to review progress
