---
name: encoding-format-advisor
description: |
  Select a data encoding format (JSON, Protobuf, Thrift, or Avro) and design a schema evolution strategy that preserves backward and forward compatibility through rolling upgrades. Use when asked "should I use Protobuf or JSON?", "how do I evolve my schema without breaking old clients?", "how does Avro schema evolution work?", "what's the difference between Thrift and Protocol Buffers?", or "how do I add/remove fields without breaking compatibility?" Also use for: choosing text vs. binary encoding for internal services; checking whether a schema change breaks compatibility; diagnosing unknown field loss bugs during rolling upgrades; planning per-dataflow encoding strategy (database storage vs. REST/RPC vs. message broker).
  Covers five encoding families: language-specific, JSON/XML/CSV, binary JSON, Thrift/Protobuf, and Avro — with writer/reader schema reconciliation and per-dataflow-mode analysis.
  For data model selection (relational/document/graph), use data-model-selector instead. For message broker or stream pipeline design, use stream-processing-designer instead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/designing-data-intensive-applications/skills/encoding-format-advisor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: [data-model-selector]
source-books:
  - id: designing-data-intensive-applications
    title: "Designing Data-Intensive Applications"
    authors: ["Martin Kleppmann"]
    chapters: [4]
tags: [encoding, serialization, schema-evolution, protobuf, thrift, avro, json, xml, backward-compatibility, forward-compatibility, rolling-upgrade, binary-encoding, schema-registry, dataflow, message-broker, rpc, grpc, evolvability]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Current data format, schema definition files (.proto, .thrift, .avsc, .json), system topology description, or architecture document describing services and their data exchange"
    - type: code
      description: "Application source files using encoding libraries, or schema files to analyze for compatibility issues"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with pasted schema definitions, .proto/.thrift/.avsc files, docker-compose.yml, architecture.md documents, or codebase analysis."
discovery:
  goal: "Produce a concrete encoding format recommendation with per-format compatibility rules and a schema evolution plan — not a survey of encoding options"
  tasks:
    - "Classify the dataflow mode (database, service calls, async messaging) to constrain format selection"
    - "Score each encoding family against six criteria for the specific system"
    - "Apply compatibility rules for the recommended format to validate each planned schema change"
    - "Produce a schema evolution plan with safe change procedures and prohibited operations"
    - "Document dataflow-specific encoding guidance and watch signals"
  audience:
    roles: ["backend-engineer", "software-architect", "data-engineer", "tech-lead", "site-reliability-engineer"]
    experience: "intermediate-to-advanced — assumes familiarity with building network services and basic serialization concepts"
  triggers:
    - "Team is designing a new internal service API and needs to choose an encoding format"
    - "System uses rolling upgrades and needs a format that supports backward and forward compatibility"
    - "Engineer needs to add/remove/rename a field and is unsure whether it breaks compatibility"
    - "Service uses JSON but is hitting performance or payload size problems at scale"
    - "Team is choosing between gRPC (Protobuf) and REST (JSON) for internal services"
    - "Data pipeline needs a schema evolution strategy for records stored in a message broker or data lake"
    - "Old-code/new-code coexistence is required and unknown fields are being silently dropped"
  not_for:
    - "Choosing specific RPC framework (gRPC vs Thrift RPC vs Avro RPC) beyond encoding format — these inherit their encoding's compatibility properties"
    - "Database replication encoding format — typically database-internal and not configurable"
    - "Encryption or compression decisions — separate from encoding format selection"
    - "Data model shape (relational vs. document vs. graph) — use data-model-selector first"
---

# Encoding Format Advisor

## When to Use

You are designing or evolving a system that passes data between processes — over the network, through a message broker, or persisted to disk — and need to choose how to encode that data and how to evolve the schema over time without breaking running services.

This skill applies when:
- You are choosing an encoding format before building or extending a service API
- Your system uses rolling upgrades: new and old versions of code run simultaneously, reading and writing the same data
- You plan schema changes (add field, remove field, rename field, change type) and need to know whether each change is safe
- You are experiencing performance or payload problems with a text-based format and evaluating binary alternatives
- Different teams or services read the same data and cannot all upgrade simultaneously
- You need to store data durably (database, file, Kafka topic) where records outlive the code that wrote them

**This skill addresses format selection and schema evolution.** For data shape decisions (relational vs. document vs. graph), use `data-model-selector` first. For stream processing pipeline design using encoded data, see `stream-processing-designer`.

---

## Context & Input Gathering

Before running the selection framework, collect:

### Required
- **Dataflow mode:** How does data move? Database writes/reads, synchronous service calls (REST/RPC), or asynchronous message passing (message broker/queue)?
- **System boundaries:** Is this data exchanged within one organization's services, or across organizational boundaries (public API, partner integrations)?
- **Rolling upgrade requirement:** Do you need old code and new code to read the same data simultaneously? Or can you do full-fleet restarts?
- **Schema change plan:** What changes are you planning (or expecting over the system's lifetime)? Add fields? Remove fields? Change field types? Rename fields?

### Important
- **Language and platform:** What programming languages are involved on both the writer and reader side? Are they statically typed (Java, Go, C++) or dynamically typed (Python, JavaScript, Ruby)?
- **Current format (if any):** Provide existing schema files (`.proto`, `.thrift`, `.avsc`, JSON Schema) or representative payload samples for analysis
- **Performance constraints:** Are payload size or parse throughput meaningful concerns (terabyte-scale data, high-frequency messaging)?
- **Team tooling familiarity:** What encoding formats does the team already operate? (Operational familiarity is a legitimate factor.)

### Optional (improves recommendation precision)
- **Architecture or data flow documents:** Help identify all producers and consumers of each data type
- **docker-compose.yml or service topology:** Identifies message brokers, data stores, and service-to-service connections
- **Existing codebase:** Grep for encoding library imports and schema definitions to understand current baseline

If the dataflow mode and rolling upgrade requirement are missing, ask before proceeding. A format recommendation without knowing these two factors is unreliable.

---

## Process

### Step 1: Classify the Dataflow Mode

**Action:** Determine how data flows between the processes you are encoding for. The three dataflow modes impose different constraints on format selection — especially on schema version negotiation and how long compatibility must be maintained.

**WHY:** Encoding format compatibility is a property of a relationship between a writer process and a reader process. That relationship looks fundamentally different in each dataflow mode. In databases, a process writing data today may be read by the same process five years from now using a different schema version — data outlives code. In synchronous service calls (REST/RPC), you can assume servers upgrade before clients, simplifying the compatibility requirement to backward-only on requests. In asynchronous message passing, a consumer may be processing a message written weeks ago by a producer that has since been upgraded or decommissioned. Each mode changes which compatibility properties you need, and therefore which formats are viable.

**Dataflow Mode A — Databases (data-at-rest)**
- One process writes to the database; another (possibly the same process, later) reads it
- Data persists independently of the code that wrote it — data outlives code
- Schema changes may leave old and new records mixed in the same table or collection for years
- Backward compatibility is essential: new code must read data written by old code
- Forward compatibility is also required when multiple application versions run simultaneously (rolling upgrade): old code reads data written by new code
- Archival export or snapshot files also fall here

**Dataflow Mode B — Synchronous service calls (REST, RPC)**
- Client sends a request; server responds; both parties are online simultaneously
- Reasonable assumption: servers upgrade before clients (staged rollout: update servers first, then clients)
- Forward compatibility on requests (old client, new server) and backward compatibility on responses (new client, old server)
- Across organizational boundaries (public APIs): clients you don't control may never upgrade — compatibility must be maintained indefinitely
- Within one organization: API versioning gives you control over the upgrade window

**Dataflow Mode C — Asynchronous message passing (message brokers, event streams)**
- Producer encodes a message; broker holds it temporarily; consumer decodes it later
- Producer and consumer are decoupled — they may be at different schema versions
- If a consumer republishes messages to a downstream topic, it must preserve unknown fields it cannot interpret (or it will silently corrupt the event stream)
- Schema must support backward and forward compatibility: messages written by old producers must be readable by new consumers, and vice versa
- Schema registry (e.g., Confluent Schema Registry for Avro/Kafka) becomes essential at scale

---

### Step 2: Score Each Encoding Family Against Your Requirements

**Action:** Score each of the five encoding families against six criteria relevant to your system. Score 1–5 per criterion per family. Skip "language-specific" family unless evaluating whether to use it (the answer is almost always no).

**WHY:** Engineers frequently default to JSON because it is familiar or default to Protocol Buffers because they "heard it's faster," without evaluating the actual criteria relevant to their system. The scoring forces examination of the criteria that change the decision: whether the schema must be dynamically generated (favors Avro over Protobuf), whether human-readability is required for debugging (favors JSON), whether the data crosses organizational boundaries (favors JSON/REST), whether statically typed code generation is valued (favors Thrift/Protobuf), and whether schema evolution flexibility is the primary constraint (favors Avro). Running all families — even the obvious misfits — produces the rationale needed for a technical decision document.

**Encoding families:**

| Family | Examples | Key characteristic |
|--------|----------|-------------------|
| Language-specific | Java Serializable, Python pickle, Ruby Marshal | Built into the language; no cross-language support |
| Text-based | JSON, XML, CSV | Human-readable; self-describing; no schema required |
| Binary JSON variants | MessagePack, BSON, CBOR | JSON data model; binary encoding; still no schema |
| Schema-driven binary (tag-based) | Apache Thrift (BinaryProtocol, CompactProtocol), Protocol Buffers | Schema required; field tags in encoded data; compact |
| Schema-driven binary (name-based) | Apache Avro | Schema required; no tags in encoded data; writer and reader schemas resolved at decode time |

**Scoring criteria:**

**1. Cross-language support** — Can both writer and reader sides use this format regardless of programming language?
- 5 = Fully cross-language with libraries for all major languages
- 3 = Supported in most major languages; some gaps
- 1 = Tied to a single language or platform (disqualifying for most systems)

**2. Schema evolution safety** — Does the format provide explicit mechanisms for backward and forward compatibility as the schema changes?
- 5 = Explicit rules; format enforces compatibility (field tags / name-based resolution); incompatible changes detected at schema check time
- 3 = Possible with discipline; no automatic detection of incompatible changes
- 1 = No versioning support; any schema change may break readers

**3. Payload compactness** — How large are encoded payloads compared to the logical data?
- 5 = Very compact; field names omitted from encoded data; variable-length integers
- 3 = Moderate; some overhead (binary JSON keeps field names; text has quotes and punctuation)
- 1 = Verbose; full field names plus type metadata in every record (text-based formats at scale)

**4. Human-readability and debuggability** — Can engineers read and debug encoded data without tooling?
- 5 = Directly human-readable; pasteble into browser/curl for debugging
- 3 = Readable with lightweight tooling (e.g., `protoc --decode_raw`, `avro-tools`)
- 1 = Binary; requires schema and decode tool to inspect

**5. Code generation and type safety** — Does the format support generating typed structs or classes from a schema, enabling compile-time type checking?
- 5 = First-class code generation; strong type safety in statically typed languages
- 3 = Optional code generation; usable in both statically and dynamically typed contexts
- 1 = No schema; all types inferred at runtime; no static type checking

**6. Dynamically generated schema support** — Can schemas be generated programmatically (e.g., from a database table definition) without manual field tag assignment?
- 5 = Tag-free schema; generation is trivial; column name → field name directly
- 3 = Schema can be generated but requires careful tag management to avoid conflicts
- 1 = Manual tag assignment required; automation requires bookkeeping infrastructure

**Score each family:**

```
                          JSON/XML  Binary JSON  Thrift/Protobuf  Avro
Cross-language support      [1-5]        [1-5]            [1-5]  [1-5]
Schema evolution safety     [1-5]        [1-5]            [1-5]  [1-5]
Payload compactness         [1-5]        [1-5]            [1-5]  [1-5]
Human-readability           [1-5]        [1-5]            [1-5]  [1-5]
Code generation/type safety [1-5]        [1-5]            [1-5]  [1-5]
Dynamic schema support      [1-5]        [1-5]            [1-5]  [1-5]
Total                      [6-30]       [6-30]           [6-30] [6-30]
```

See `references/format-comparison-table.md` for pre-filled scores with rationale for each criterion, plus byte counts for the same record encoded in all five formats.

---

### Step 3: Apply the Format Selection Decision Rules

**Action:** Apply explicit if/then rules to produce a primary format recommendation. These rules encode the structural logic of the format characteristics — they are not heuristics but direct consequences of how each format handles field identification, schema negotiation, and type encoding.

**WHY:** Scoring produces numbers; decision rules produce a recommendation. The rules encode the non-obvious consequences of format choice: JSON's number ambiguity (integers vs. floats, no precision specification) causes silent data corruption at scale; Thrift/Protobuf's tag-based schema evolution is robust for most cases but breaks when schemas are generated dynamically (because tags must be managed manually); Avro's writer/reader schema resolution is powerful but requires a schema distribution mechanism (file header, schema registry, version negotiation) that must be built or operated. These consequences are expensive to discover after deployment.

**Rule 1 — Use JSON (or REST/JSON) if ANY of the following are true:**
- Data crosses organizational boundaries (public API, partner integrations, browser clients) — JSON is the de facto standard; the difficulty of getting external parties to adopt anything else outweighs efficiency gains
- The primary consumer is a web browser or JavaScript runtime
- Human-readability for debugging and manual API testing is a hard requirement
- The team has no existing schema management infrastructure and schema evolution is low-frequency
- Note: Use JSON with explicit schema validation (JSON Schema) if you need schema documentation; without validation, schema drift into application code is slow and hard to detect

**Rule 2 — Use Protocol Buffers (Protobuf) if ALL of the following are true:**
- Data flows within one organization's services (internal service-to-service)
- Both sides use statically typed languages (Java, Go, C++, Rust) — code generation adds significant value
- Schema changes are infrequent and managed by the team owning the schema (not dynamically generated from another source)
- You need both compact encoding and explicit compatibility rules enforced by a schema checker
- Rolling upgrade compatibility is required (field tags provide this; see Step 4)
- Note: gRPC uses Protocol Buffers and inherits its compatibility properties

**Rule 3 — Use Apache Thrift if ALL of the following are true:**
- Same conditions as Protocol Buffers, AND
- The existing codebase already uses Thrift (e.g., inherited from a Facebook/Twitter-lineage stack)
- Note: Thrift and Protocol Buffers are functionally equivalent for most decisions; the choice between them is primarily ecosystem and existing adoption. CompactProtocol is Thrift's most efficient encoding; use it over BinaryProtocol unless compatibility with older tooling is required.

**Rule 4 — Use Apache Avro if ANY of the following are true:**
- Schemas are dynamically generated from another source (e.g., a relational database schema dump, an Elasticsearch mapping, or code-generated from an ORM) — Avro's tag-free encoding means column names map directly to field names without manual tag assignment
- The data is stored in large file archives where all records share one schema (Hadoop, data lake, archival exports) — Avro object container files embed the schema once per file
- Dynamically typed languages (Python, JavaScript, Ruby) are primary consumers and code generation adds no value — Avro works well without generated code
- You are using Apache Kafka with a schema registry (Confluent Schema Registry natively supports Avro)
- Note: Avro requires a schema distribution mechanism — either embed the writer's schema in the file (object container files), store schema versions in a database (one version number per record), or negotiate schema on connection setup (Avro RPC)

**Rule 5 — Avoid language-specific encodings (Java Serializable, Python pickle, Ruby Marshal) unless:**
- Data is purely transient (in-memory cache within a single process, never written to disk or network)
- Security implications are understood and mitigated: deserializing untrusted bytes can execute arbitrary code
- No cross-language communication is needed now or in the foreseeable future

**Tie-breaker when rules 2 and 4 both apply (schema-driven binary required, but dynamic generation is also needed):**
Choose Avro if schema generation frequency is high (schemas change when the source schema changes, e.g., database column added). Choose Protobuf if schema changes are infrequent and controlled by your team (field tag management overhead is acceptable).

---

### Step 4: Apply Compatibility Rules for the Recommended Format

**Action:** For each planned or expected schema change, check it against the per-format compatibility rules. Classify each change as: safe (backward and forward compatible), backward-only (new code reads old data, but not vice versa), forward-only (old code reads new data, but not vice versa), or breaking (incompatible in at least one direction).

**WHY:** The core problem encoding formats solve is not just efficiency — it is allowing old and new versions of code to coexist while reading the same data. During a rolling upgrade, some nodes run new code and some run old code; they write data to the same database or send messages to the same topic. Forward compatibility (old code reads data written by new code) is the harder direction: it requires old code to safely ignore additions made by new code rather than crashing. Each format handles this differently, and the permitted changes differ significantly.

#### Protocol Buffers and Thrift: Field Tag Rules

Field tags (the numbers `= 1`, `= 2`, `= 3` in Protobuf; `1:`, `2:`, `3:` in Thrift) are the identity of a field in the encoded data — not the field name. The encoded data contains only tags and values; names are only in the schema. This is what enables forward compatibility: a reader that sees an unknown tag number can skip that field using the type annotation to determine how many bytes to skip.

**Safe changes (backward and forward compatible):**
- Add a new field with a new (previously unused) tag number — old code ignores it (forward compatible), new code can read old data that lacks the field (backward compatible, provided the field is optional or has a default)
- Rename a field — names are not in the encoded data; tags are; renaming is invisible to the wire format
- Change a field from `required` to `optional` — safe; `required` is a runtime check, not an encoding property

**Backward compatible only (new code reads old data; old code cannot read new data):**
- Change the field name and keep the tag — backward compatible (old code uses tag, not name); safe

**Breaking changes — never do these:**
- Remove a required field — old code will fail to parse records written by new code that omits it
- Change a field's tag number — all existing encoded data referencing the old tag becomes unreadable
- Reuse a tag number that was previously used for a removed field — new code will misinterpret old data that contains the old field's data under that tag
- Add a new field as `required` — old code that wrote data before the field existed will fail the `required` check when new code reads it; every new field added after initial deployment must be `optional` or have a default value
- Change the datatype of a field in a way the parser cannot convert (e.g., `int32` to `string`) — type mismatch causes a parse error or silent truncation

**Datatype change rules (Protobuf):**
- `int32` → `int64`: safe; new code fills missing high bits with zeros; old code reads 64-bit value into 32-bit variable (truncated if value exceeds 32-bit range)
- `optional` (single-value) → `repeated` (multi-value): safe; new code reading old data sees a list with zero or one elements; old code reading new data sees the last element of the list
- `repeated` → `optional`: safe in the reverse direction only if the new code handles a single-element list

#### Apache Avro: Writer/Reader Schema Rules

Avro does not use field tags. The encoded data contains only values concatenated in schema field order — no type annotations, no tags. The reader must have access to both the writer's schema (which defined the byte layout) and the reader's schema (which defines what the application expects). The Avro library resolves the difference by matching fields by name and filling defaults for missing fields.

**Safe changes (backward and forward compatible):**
- Add a field with a default value — old readers get the default when reading data that lacks the field (backward compatible); new readers ignore the field when reading old data that has it (forward compatible, if the new reader's schema also declares the field)
- Remove a field that has a default value — old readers that still expect the field get the default; new readers that wrote data without the field are fine
- Change field order — Avro matches by name, not position; order changes are transparent

**Backward compatible only:**
- Add a field without a default value — new code can read old data (old code wrote the field, new code reads it); old code cannot read new data (new writer omits the field; old reader has no default to fall back to)

**Forward compatible only:**
- Remove a field without a default value — old readers that expect the field get no value and have no default; this breaks backward compatibility

**Breaking changes:**
- Add a field that has no default value AND remove a field that has no default value simultaneously — breaks in both directions
- Change a field name without adding the old name as an alias in the reader's schema — the Avro resolution algorithm matches by name; a renamed field without an alias is treated as a deleted field plus a new field

**Avro null handling:** Avro does not allow null as a value for a field unless the field's type is a union that includes null (e.g., `union { null, long } favoriteNumber = null`). This is more explicit than Protocol Buffers' optional fields and prevents bugs by forcing you to declare nullability in the schema.

**Avro schema distribution checklist:**
- Large file with many records: embed writer's schema once in the Avro object container file header
- Database with individually written records: store schema version number per record; maintain a schema version registry in the database
- Network connection between two services: negotiate schema version on connection setup (Avro RPC protocol); client and server exchange schemas at handshake time
- Kafka with schema registry: each message includes a schema ID (not the full schema); schema registry stores schemas by ID; producers register schemas; consumers fetch schemas on first encounter

#### JSON/XML: Compatibility Through Convention

JSON and XML have no built-in compatibility mechanism. Compatibility is achieved by convention and application discipline.

**Safe by convention:**
- Add a new field — if all readers ignore unknown fields (the convention is to use lenient parsers), this is forward compatible; backward compatible because new readers handle missing fields with null/default in application code
- Rename a field — breaking; all readers must update simultaneously

**Common failure modes:**
- Removing a field — readers that depend on it crash or silently use a null/zero default
- Changing a field's type — JSON does not distinguish integers from floats; a field that was always an integer may be parsed as a float by some implementations, causing precision loss for integers > 2^53
- Binary strings — JSON has no binary type; binary data requires Base64 encoding, which increases size by 33% and requires encoding/decoding logic on both sides

---

### Step 5: Analyze Dataflow-Mode-Specific Encoding Guidance

**Action:** Apply dataflow-specific guidance for the recommended format. The same format behaves differently in each mode, and there are additional rules and failure modes specific to each.

**WHY:** The encoded format is not used in isolation — it is used within a dataflow mode that imposes additional constraints. Ignoring these constraints produces systems that are correct in isolation but fail in production: a consumer that reprocesses Kafka messages without schema version handling will fail on old messages; a service that decodes a JSON request into a model object and re-encodes it for storage will silently drop unknown fields added by a newer client; a database that stores model objects will lose unknown fields when old code reads and re-writes a record that contains fields it doesn't understand.

**Mode A — Databases:**
- Data outlives code. All schema changes must be backward compatible (or require a full data migration). Plan for records written by version 1 to be readable by version 5.
- Unknown field loss: Decoding a record into a typed model object and re-encoding it will silently drop unknown fields (written by newer schema versions). Protobuf parsers preserve unknown fields in a side-channel; Avro resolution ignores writer-only fields safely. In JSON, use a passthrough "unknown fields" map in the struct, or avoid read-modify-write on fields you don't touch.
- Archival exports: Use Avro object container files — schema embedded once per file; readable years later with only the Avro library.
- Prefer schema-driven binary formats (Thrift/Protobuf/Avro) over JSON for long-lived stored data: explicit schema serves as documentation that cannot drift from reality.

**Mode B — Synchronous service calls (REST, RPC):**
- Reasonable assumption: servers upgrade before clients. Validate: backward compatibility on requests (new server + old client) AND forward compatibility on responses (old client + new server).
- Across organizational boundaries: never break backward compatibility; use URL versioning (`/v1/`, `/v2/`) for breaking changes; maintain deprecated versions with explicit sunset dates.
- REST vs. gRPC: REST with JSON for public APIs (curl-testable, no client tooling required). gRPC (Protobuf) for internal services in statically typed stacks (type safety, compact encoding, HTTP/2 streaming).

**Mode C — Asynchronous message passing (message brokers):**
- Full bidirectional compatibility required simultaneously: producers and consumers deploy independently; messages persist for hours or days.
- Consumer-republish risk: a consumer that republishes messages to a downstream topic must preserve fields it cannot interpret. Failure corrupts the event stream for downstream consumers. Use Protobuf (unknown fields preserved in parser) or Avro (writer-only fields safely ignored during resolution).
- Schema registry: embed writer's schema once per Avro file (archival), or use a schema registry (Confluent Schema Registry with Kafka). Each message carries a 4-byte schema ID; consumer fetches schema on first encounter and caches it.
- Distributed actor defaults: Akka uses Java serialization (no compatibility); Erlang OTP rolling upgrades require careful planning. Replace with Protobuf before assuming rolling upgrades work.

---

### Step 6: Produce the Encoding Decision Document

**Action:** Write a structured recommendation covering format selection, compatibility assessment of planned changes, schema evolution plan, and dataflow-specific guidance. See the full output template in the three examples below.

**WHY:** A recommendation without explicit rationale cannot be reviewed or revised when requirements change. The schema evolution plan is especially important: it must specify not just which format to use, but the exact rules for each type of change the team will make over the system's lifetime, so that engineers making future changes have explicit guidance rather than relying on informal knowledge.

**Required sections:**
1. Recommended format with primary rationale (2 sentences connecting dataflow mode and rolling upgrade requirement)
2. Scoring summary table (six criteria, three to four families)
3. Schema evolution plan (table: each planned change, safe/breaking, compatibility direction, procedure)
4. Dataflow-mode-specific rules and watch signals
5. Ruled-out analysis (one sentence per format explaining the deciding criterion)
6. Implementation checklist with CI tooling and schema version management

**Related decisions:** Data model shape → `data-model-selector`. Stream processing pipeline → `stream-processing-designer`.

---

## What Can Go Wrong

These are the most common failure modes when selecting encoding formats and planning schema evolution. Review each before finalizing a recommendation.

**Adding a required field after initial deployment (Thrift/Protobuf).**
Every new field added after first deployment must be `optional` (or have a default). A `required` field will fail at parse time when reading old records that never wrote it. This is a silent misconfiguration: the schema compiles and tests pass with new test data, but fails at runtime on real old records. Rule: after initial deployment, required fields are permanently forbidden.

**Reusing a field tag number (Thrift/Protobuf).**
A retired field's tag number must be permanently marked `reserved`. Reusing a tag for a new field causes old data with the original field's bytes to be misinterpreted as the new field's type — silent data corruption or a parse error. Use `reserved 3; reserved "old_field_name";` in every `.proto` file when removing a field.

**Avro field without a default value breaks compatibility in one direction.**
Adding a field without a default breaks backward compatibility (old writers didn't include it; readers have no fallback). Removing a field without a default breaks forward compatibility (new writers omit it; old readers have no fallback). Rule: every Avro field that may be added or removed across versions must declare a default value.

**Unknown field loss in read-modify-write cycles (all formats).**
Reading a record into a typed model object, modifying one field, and writing back silently drops any fields the model type doesn't know about. Affects databases (old code reads and rewrites new records, drops new fields) and message brokers (consumer republishes a modified message, drops new producer fields). Protobuf parsers preserve unknown fields in a side-channel; Avro resolution ignores writer-only fields safely. In JSON, the struct must include an explicit "unknown fields" passthrough map.

**Number precision loss with JSON at scale.**
Integers greater than 2^53 cannot be represented exactly in IEEE 754 double-precision float (the JavaScript `Number` type). Twitter returns tweet IDs as both a JSON number and a decimal string because JavaScript clients parse the numeric form incorrectly. Mitigation: string-encode large integers in JSON APIs, or use a format with explicit 64-bit integer types.

**Adopting binary format without schema version management (Avro).**
Avro requires a mechanism for the reader to obtain the writer's schema — file header, schema registry, or connection negotiation. Without this, Avro is unusable. Retrofitting schema version IDs into records after gigabytes of data have been written is expensive. Choose a schema distribution mechanism before writing the first record.

**Switching to binary format to solve a performance problem that isn't encoding.**
For payloads under 1KB at under 10K requests/second, the encoding/decoding difference between JSON and Protobuf is negligible compared to network latency and business logic. Profile first. The operational cost of binary formats (schema management, debugging complexity) is only worth paying when encoding is confirmed as the bottleneck.

---

## Inputs / Outputs

### Inputs
- Dataflow mode description (required)
- Rolling upgrade requirement (required)
- Planned schema changes or data shape description (required)
- Existing schema files or payload samples (optional but strongly improves precision)
- Language and platform of writer and reader services (important)
- Performance constraints (optional)

### Outputs
- Encoding format recommendation with rationale and scored decision matrix
- Per-change compatibility classification (safe / breaking / direction)
- Schema evolution plan with explicit permitted and prohibited operations
- Dataflow-mode-specific encoding guidance
- Implementation checklist with tooling recommendations
- Watch signals for the most likely failure modes

---

## Key Principles

**The compatibility direction that matters depends on the dataflow mode.** In databases, both backward and forward compatibility are required simultaneously (data outlives code). In service calls, you can assume servers upgrade before clients (backward on requests, forward on responses). In async messaging, full bidirectional compatibility is required (decoupled producers and consumers at independent schema versions).

**Field tags are a permanent commitment (Thrift/Protobuf).** A field's tag number is its identity in the encoded data for the lifetime of the schema. It cannot be changed, cannot be reused after removal, and a `required` field cannot be removed. Treat tag assignments as permanent as column IDs in a relational database — they outlive any individual deployment.

**Avro's writer/reader schema resolution requires infrastructure.** Avro achieves the most compact encoding (32 bytes for the example record vs. 59 for Thrift CompactProtocol, 33 for Protobuf, 66 for MessagePack, 81 for JSON) by omitting all field identification from the encoded bytes. The cost is that the reader must have access to the writer's schema. This is not optional — it is a hard requirement that must be designed for before adopting Avro.

**Data outlives code.** A database record written today may be read five years from now by code that uses a schema three versions newer. A Kafka message written by a producer that has since been decommissioned may be replayed by a new consumer. The encoding format you choose today must support reading that data with future schema versions — not just today's.

**Schemas are documentation.** A schema registry of past schema versions is a historical record of every data structure the system has ever used. It serves as documentation that is guaranteed to be accurate (because decoding fails if it is wrong, unlike manually maintained documentation). Build schema versioning infrastructure even if you don't use it for compatibility checking immediately — the documentation value alone is worth it.

---

## Examples

### Example 1: Internal gRPC Service (Statically Typed Stack)

**Scenario:** A platform team is building a new internal recommendation service written in Go, consumed by a Java API gateway and a Python data pipeline. The service will undergo rolling upgrades — no fleet-wide restarts. The team expects to add fields to the recommendation response over time as the ML model evolves (adding score components, confidence intervals, explanation fields). Payload volume is high: ~50K recommendations/second.

**Trigger:** "Should we use JSON REST or gRPC Protobuf for our internal recommendation service? We need rolling upgrades."

**Process:**
- Step 1: Dataflow Mode B — synchronous service calls, internal organization boundary, rolling upgrades required
- Step 2: Protobuf scores high on schema evolution safety (field tags, optional fields), compactness (33 bytes vs. 81 for JSON for equivalent record), and code generation (Go and Java strongly benefit from typed structs). JSON scores high on human-readability but low on schema evolution safety. Avro scores well but dynamic schema generation is not needed here — schemas are hand-authored and evolving incrementally.
- Step 3: Rule 2 applies — internal service, statically typed languages (Go and Java), infrequent schema changes, rolling upgrade required.
- Step 4: Planned changes assessed:
  - Add `confidence_interval` field: safe — new tag, optional, default 0.0
  - Add `explanation` field (list of strings): safe — new tag, repeated field
  - Remove `legacy_score` field: safe if retired tag is marked `reserved`; never reuse tag 3

**Output (abbreviated):**
```
## Encoding Format Decision

**System:** Recommendation Service → API Gateway, Data Pipeline
**Dataflow mode:** B — Synchronous service calls (internal)

### Recommended Format: Protocol Buffers (gRPC)

**Primary rationale:** Internal service with Go and Java consumers undergoing 
rolling upgrades. Protobuf's field tags provide explicit backward/forward 
compatibility; code generation gives typed structs in both languages; 33-byte 
encoding vs 81-byte JSON reduces bandwidth at 50K req/sec by ~60%.

### Schema Evolution Plan

| Change | Safe? | Direction | Procedure |
|--------|-------|-----------|-----------|
| Add confidence_interval (float) | Yes | Both | New tag (e.g., 4), optional, default 0.0 |
| Add explanation (repeated string) | Yes | Both | New tag (e.g., 5), no default needed |
| Remove legacy_score | Yes | Both | Mark tag 3 as reserved; never reuse |
| Rename legacy_score to base_score | Yes | Both | Rename in .proto only; tag unchanged |
| Change score from float to double | Yes (with truncation risk) | Backward | Old readers truncate if value > float range; validate range |

### Ruled Out

**JSON/REST:** No schema-enforced compatibility; number precision issues for 
score floats; human-readability benefit outweighed by 50K req/sec bandwidth 
cost at this scale.
**Avro:** Dynamic schema generation not needed; schema registry adds 
operational overhead not justified by dynamically generated schemas here.

### Implementation Checklist

- [ ] Define .proto schema file; assign initial field tags (never reuse)
- [ ] Add `reserved 3; reserved "legacy_score";` when legacy_score is removed
- [ ] Set up buf lint and buf breaking in CI to catch incompatible changes before merge
- [ ] Python data pipeline: use protobuf Python library (no code gen needed for dynamic language)
- [ ] Watch: if the schema starts being generated from the ML model's feature definition 
      rather than hand-authored, re-evaluate Avro (dynamic generation requires tag management)
```

---

### Example 2: Kafka Event Stream with Independent Producers and Consumers

**Scenario:** An e-commerce platform publishes `OrderPlaced` events to a Kafka topic. Three consumer services (inventory, fulfillment, analytics) subscribe to the topic. Services are deployed independently — the inventory service may be running version 1 of the schema when the order service publishes version 2. Messages are retained for 7 days. The analytics team wants to schema-dump the Kafka topic to Parquet files in a data lake.

**Trigger:** "We're publishing order events to Kafka. How do we handle schema changes when consumers deploy at different times?"

**Process:**
- Step 1: Dataflow Mode C — async message passing, internal organization, multiple independent consumers, 7-day message retention
- Step 2: Avro scores highest — schema registry support native with Kafka; dynamic compatibility from name-based resolution; all records in a topic share a schema per partition making schema ID per record efficient; Hadoop/Parquet interop for data lake export. Protobuf is viable but tag management becomes complex when the analytics team generates Avro schemas from Parquet column definitions.
- Step 3: Rule 4 applies — Kafka ecosystem (Confluent Schema Registry natively supports Avro), data lake export (Avro object container files embed schema for archival), dynamically generated schemas for analytics are a future requirement.
- Step 4: Compatibility rules:
  - All new fields must have default values (backward and forward compatibility required simultaneously)
  - Schema must be registered in schema registry before first producer uses it
  - Consumers must preserve unknown fields before republishing to downstream topics

**Output (abbreviated):**
```
## Encoding Format Decision

**System:** Order events — Kafka topic, 3 consumers, data lake export
**Dataflow mode:** C — Async message passing

### Recommended Format: Apache Avro + Confluent Schema Registry

**Primary rationale:** Kafka with independent producers and consumers at 
different schema versions requires simultaneous backward and forward compatibility. 
Avro's name-based resolution handles field additions and removals with defaults; 
schema registry provides schema distribution without embedding full schema in 
every message; Avro object container files support archival export to data lake.

### Schema Evolution Plan

| Change | Safe? | Direction | Procedure |
|--------|-------|-----------|-----------|
| Add shipping_address field | Yes (if default) | Both | Add with default null; register new schema version first |
| Add discount_codes (array) | Yes (if default) | Both | Add with default [] (empty array) |
| Remove coupon_code (deprecated) | Yes (if had default) | Both | Confirm default exists; remove; add alias for old readers |
| Rename order_id to orderId | Backward only | Backward | Add "orderId" as alias in reader schema; forward breaks |
| Change amount from int to long | Safe | Both | Avro can convert; document range implications |

### Dataflow-Specific Rules

- Register new schema version in registry BEFORE deploying the producer that uses it
- Consumers must implement "preserve unknown fields" pattern when republishing to downstream topics
- Data lake export: use Avro object container files (schema embedded once per file)
- Schema registry: use BACKWARD_TRANSITIVE compatibility mode (new schema must be compatible with ALL previous versions, not just the immediately preceding one)

### Ruled Out

**Protobuf:** Tag management adds friction when analytics team generates schemas 
from Parquet column definitions — Avro's name-based approach maps column names 
directly to field names.
**JSON:** No schema versioning mechanism; unknown field behavior is parser-dependent 
(some parsers drop unknowns, some error); 7-day retention means old records will 
definitely be processed by new consumers.

### Implementation Checklist

- [ ] Set up Confluent Schema Registry; configure BACKWARD_TRANSITIVE compatibility mode
- [ ] Write schema as Avro IDL; define default values for all fields
- [ ] Producer: register schema before first publish; include schema ID in message header
- [ ] Consumer: fetch schema by ID; implement unknown field preservation before republish
- [ ] Data lake export: use Avro object container files; Parquet conversion tool reads embedded schema
- [ ] Watch: if a consumer must republish without a schema registry, embed writer's schema version in message metadata instead
```

---

### Example 3: Public REST API with Long-Lived Clients

**Scenario:** A SaaS company exposes a REST API for third-party integrations. Clients are external developers who cannot be forced to upgrade. The team needs to add `subscription_tier` to `Workspace` and deprecate `plan_name`.

**Trigger:** "How do we evolve our REST API schema without breaking external clients?"

**Process:**
- Step 1: Mode B — service calls across organizational boundaries; clients not controlled; indefinite compatibility required
- Step 2: JSON only — external clients, browser consumers, no client-side code-gen toolchain, human-readability required for developer experience. Rule 1 applies immediately.
- Step 4: Add `subscription_tier` — safe (additive). Deprecate `plan_name` (keep it populated, mark deprecated in docs) — safe. Remove `plan_name` — breaking; requires `/v2/` with a minimum 12-month sunset period for `/v1/`. Change `user_id` int → string — breaking; API version bump required.

**Output (key sections):**

```
Recommended Format: JSON (REST)
Dataflow mode: B — cross-organizational boundary

Schema Evolution Plan:
- Add subscription_tier: Safe — additive; lenient clients ignore unknown fields
- Deprecate plan_name (keep populated): Safe — document as deprecated in OpenAPI spec
- Remove plan_name: Breaking — /v2/ required; 12-month /v1/ sunset window
- Change user_id int → string: Breaking — /v2/ required; document migration guide

Dataflow rules:
- Never remove response fields without a versioned sunset period
- Adding optional request params is safe; adding required params is breaking  
- Watch: if IDs exceed 2^53, return as both JSON number and decimal string (Twitter pattern)

Ruled out — Protobuf/Avro: external clients cannot be required to install code-gen 
toolchains; binary format is not curl-testable.
```

---

## References

| File | Contents |
|------|----------|
| `references/format-comparison-table.md` | Full scoring matrix for all five encoding families; byte counts for the same example record in JSON (81 bytes), MessagePack (66 bytes), Thrift BinaryProtocol (59 bytes), Thrift CompactProtocol (34 bytes), Protocol Buffers (33 bytes), Avro (32 bytes); compatibility matrix comparing each format's handling of add/remove/rename/type-change operations |
| `references/schema-evolution-rules.md` | Complete per-format compatibility rule reference: all Protobuf/Thrift field tag rules, all Avro writer/reader schema resolution rules, JSON convention guidelines, with explicit permitted/prohibited change classification for each change type |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Designing Data-Intensive Applications by Martin Kleppmann.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-model-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
