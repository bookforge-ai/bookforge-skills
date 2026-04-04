# System Models for Distributed Algorithms

Full reference for Step 6 of the distributed-failure-analyzer skill.

---

## Why System Models Matter

A distributed algorithm is correct only within a specific system model. If the actual system violates the model's assumptions, the algorithm's correctness guarantees no longer hold. Making the model explicit allows:
1. Selecting algorithms that match the system's real behavior.
2. Identifying cases where the implementation may fail even if the algorithm is "correct."
3. Reasoning about safety and liveness properties in the presence of faults.

---

## Timing Models

### Synchronous Model
**Assumptions:** Bounded network delay, bounded process pauses, bounded clock error.

Does not mean perfectly synchronized clocks or zero delay — only that known fixed upper bounds exist.

**Reality fit:** Not realistic for most packet-switched datacenter networks or commodity hardware running general-purpose operating systems. Packet delays are unbounded; GC pauses are unbounded; clock drift has no fixed bound without dedicated hardware (GPS, atomic clocks).

**Use case:** Algorithm analysis baseline. Some embedded and real-time systems (RTOS + dedicated hardware) can approximate this model.

### Partially Synchronous Model
**Assumptions:** The system behaves like a synchronous system *most of the time*, but occasionally exceeds the bounds for network delay, process pauses, and clock drift.

**Reality fit:** Realistic for most production server-side systems. Networks are usually well-behaved; processes usually respond quickly. But any timing assumption may be violated occasionally (load spikes, GC events, VM migrations, network congestion).

**Implication:** Algorithms designed for this model must be correct even when timing bounds are temporarily exceeded. Safety properties must hold always; liveness properties are allowed to wait until the system returns to synchronous behavior.

**Recommended default for most datacenter systems.**

### Asynchronous Model
**Assumptions:** No timing assumptions whatsoever. No clock, no timeouts.

**Reality fit:** Very conservative. Some algorithms (e.g., certain consensus protocols) are designed for this model, making them maximally portable. However, the model is extremely restrictive — without timeouts, failure detection is impossible, and many practical algorithms cannot be expressed.

---

## Node Failure Models

### Crash-Stop Faults
**Assumptions:** A node fails by stopping responding. It never comes back. Once a node is declared dead, it stays dead.

**Notes:** Simplest model. Safe to use as a design assumption even if nodes do recover in practice — algorithms designed for crash-stop remain correct if nodes happen to recover (they just may not take advantage of the recovery).

### Crash-Recovery Faults
**Assumptions:** Nodes may crash at any time. They may start responding again after an unknown amount of time. On crash-recovery: stable storage (non-volatile disk) is preserved across crashes; in-memory state is lost.

**Notes:** Realistic for server-side systems with durable storage (databases, write-ahead logs). Most production distributed databases assume this model.

**Implication:** Algorithms must handle the case where a recovered node has forgotten its in-memory state. This is why distributed databases write decisions to disk before responding — the disk is the source of truth after recovery.

### Byzantine (Arbitrary) Faults
**Assumptions:** Nodes may do anything — crash, respond slowly, send incorrect or conflicting messages, lie about their state.

**Notes:** Covers adversarial behavior and hardware memory corruption. Requires supermajority quorums (>2/3 of nodes functioning correctly). Protocols are significantly more complex and expensive.

**When relevant:**
- Multi-party untrusted environments (blockchain, inter-bank settlement, peer-to-peer networks).
- High-radiation environments (aerospace, space systems) where memory corruption is a realistic concern.
- NOT relevant for typical datacenter systems where your organization controls all nodes.

---

## Safety and Liveness Properties

Every correctness property of a distributed algorithm is classified as either safety or liveness.

### Safety Properties
**Definition:** "Nothing bad happens."

Formally: if a safety property is violated, there exists a specific point in time at which the violation occurred. The violation cannot be undone — the damage is done.

**Examples:**
- Uniqueness (fencing tokens): no two requests for a fencing token return the same value.
- Monotonic sequence: tokens are always increasing.
- Linearizability: reads always see the most recent write.

**Requirement:** Safety properties must hold in *all* situations in the system model — even if all nodes crash or all network delays become infinite. The algorithm must never return a wrong result.

### Liveness Properties
**Definition:** "Something good eventually happens."

Liveness properties often include the word "eventually" in their definition.

**Examples:**
- Availability: a node that requests a fencing token and does not crash eventually receives a response.
- Eventual consistency: if no new writes occur, all replicas eventually converge to the same value.

**Requirement:** Liveness properties may include caveats. For example: "a request receives a response *if* a majority of nodes are functional *and* the network eventually recovers." The partially synchronous model requires that any period of timing violation is finite.

**Note:** Eventual consistency is a liveness property. Linearizability is a safety property. These have fundamentally different guarantees and operational implications.

---

## Recommended System Model for Most Server-Side Data Systems

**Timing model:** Partially synchronous
**Node failure model:** Crash-recovery

This combination is used by most well-known distributed algorithms (Raft, Paxos, ZooKeeper's ZAB, PBFT with crash-recovery modifications).

**Implications for your system:**
1. Timeouts will sometimes fire incorrectly — design for this.
2. A recovered node must re-read its state from stable storage before acting.
3. Safety properties (uniqueness, linearizability) must hold even during timing violations.
4. Liveness properties (eventually getting a response, eventual leader election) are allowed to stall during partitions or excessive delays.

---

## Mapping System Models to Reality

System models are abstractions. Real systems frequently encounter scenarios the model does not cover:

- **Stable storage assumed to survive crashes** — but what if the disk is corrupted by a firmware bug? What if the server fails to recognize its drives on reboot?
- **Crash-recovery assumed** — but what if a node has amnesia and forgets previously stored data (hardware failure wiping the disk)?
- **Non-Byzantine assumed** — but what if a software bug causes a node to send incorrect responses (a bug is effectively a Byzantine fault that a Byzantine-tolerant algorithm cannot save you from, if all nodes run the same buggy code)?

These edge cases do not make system models useless. They mean that:
1. Theoretical algorithm analysis and empirical testing are both required.
2. Real implementations must handle cases the model declares impossible — even if that handling is just an alert + manual intervention.
3. Safety properties in a real system are best-effort, with monitoring as the backstop.
