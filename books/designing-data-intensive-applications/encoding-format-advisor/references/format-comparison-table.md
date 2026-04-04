# Format Comparison Table

## Byte Counts: Same Record in Five Formats

Reference record (from Kleppmann Chapter 4):

```json
{
  "userName": "Martin",
  "favoriteNumber": 1337,
  "interests": ["daydreaming", "hacking"]
}
```

| Format | Bytes | Notes |
|--------|-------|-------|
| JSON (no whitespace) | 81 | Field names repeated in every record; string quoting; no binary type |
| MessagePack | 66 | Binary JSON; same data model (no schema); field names still embedded |
| Thrift BinaryProtocol | 59 | Field tags + type annotations; no field names in encoded data |
| Protocol Buffers | 33 | Field tags; varint encoding for integers; single encoding format |
| Thrift CompactProtocol | 34 | Field type + tag packed into one byte; varint integers |
| Avro | 32 | No tags, no type annotations; values concatenated in schema field order |

Key observation: The difference between JSON (81 bytes) and Avro (32 bytes) is 60% — not negligible at terabyte scale. The difference between JSON (81 bytes) and MessagePack (66 bytes) is only 19% — often not worth the loss of human-readability for moderate data volumes.

---

## Scoring Matrix: Six Criteria Across Four Encoding Families

Scores are 1–5 per criterion. These represent typical scores for a general case — adjust for your specific system using the notes in each cell.

### Cross-language support (can writer and reader use different programming languages?)

| Format | Score | Notes |
|--------|-------|-------|
| JSON/XML | 5 | Libraries in every language; the default for public APIs |
| Binary JSON (MessagePack, BSON) | 4 | Libraries for major languages; smaller ecosystem than JSON |
| Thrift / Protocol Buffers | 5 | Official libraries for Java, Go, Python, C++, Ruby, C#, JavaScript, Rust, and more; gRPC expands the ecosystem |
| Avro | 4 | Java-native (Hadoop ecosystem); good Python support; thinner in Go and Rust |

### Schema evolution safety (does the format enforce backward/forward compatibility?)

| Format | Score | Notes |
|--------|-------|-------|
| JSON/XML | 2 | No built-in mechanism; relies on convention (lenient parsers, optional fields); no tooling to detect incompatible changes |
| Binary JSON | 2 | Same as JSON — binary encoding but no schema; same compatibility limitations |
| Thrift / Protocol Buffers | 5 | Field tags provide explicit compatibility; `reserved` prevents tag reuse; buf/protoc can detect breaking changes in CI |
| Avro | 5 | Name-based resolution with defaults; schema registry compatibility modes (BACKWARD, FORWARD, FULL, TRANSITIVE variants) enforce rules before a schema is registered |

### Payload compactness (how large is the encoded output relative to the logical data?)

| Format | Score | Notes |
|--------|-------|-------|
| JSON/XML | 1 | Field names repeated in every record; string quoting; no compact integer encoding |
| Binary JSON | 3 | Field names still embedded; varint integers in some implementations; moderate improvement |
| Thrift CompactProtocol / Protocol Buffers | 5 | No field names; varint integers; field type packed with tag |
| Avro | 5 | No field names, no tags, no type annotations; varint integers; most compact of all formats |

### Human-readability and debuggability (can you read encoded data without tooling?)

| Format | Score | Notes |
|--------|-------|-------|
| JSON/XML | 5 | Paste into a browser, cat to terminal, curl directly; debugging is trivial |
| Binary JSON | 3 | Requires `msgpack-tool` or equivalent; not human-readable but decode tools are lightweight |
| Thrift / Protocol Buffers | 2 | Binary; requires `protoc --decode_raw` or `thrift --decode`; schema needed for named field output |
| Avro | 2 | Binary; requires `avro-tools tojson` or `avro-tools getschema`; object container files are self-describing but binary |

### Code generation and type safety (does the format generate typed structs/classes?)

| Format | Score | Notes |
|--------|-------|-------|
| JSON/XML | 1 | No schema; types inferred at runtime; JSON Schema validation is optional and rarely enforced at compile time |
| Binary JSON | 1 | No schema; same as JSON |
| Thrift / Protocol Buffers | 5 | First-class code generation for all supported languages; IDE autocompletion; compile-time type checking in statically typed languages |
| Avro | 3 | Optional code generation; fully usable without it (especially in dynamic languages); self-describing object container files enable schema-free consumption |

### Dynamically generated schema support (can schemas be generated programmatically without manual work?)

| Format | Score | Notes |
|--------|-------|-------|
| JSON/XML | 5 | No schema required; any JSON is valid; trivial to generate |
| Binary JSON | 5 | No schema; same as JSON |
| Thrift / Protocol Buffers | 2 | Field tags must be assigned and managed; generating schemas from a database table requires careful tag assignment and bookkeeping to avoid reuse of old tag numbers |
| Avro | 5 | Field names map directly to column names; no tag management; generating a new Avro schema from an updated database table is mechanical (no bookkeeping) |

### Typical total scores (general case)

| Format | Cross-lang | Evolution | Compact | Readable | Code-gen | Dynamic | Total |
|--------|-----------|-----------|---------|----------|----------|---------|-------|
| JSON/XML | 5 | 2 | 1 | 5 | 1 | 5 | 19 |
| Binary JSON | 4 | 2 | 3 | 3 | 1 | 5 | 18 |
| Thrift/Protobuf | 5 | 5 | 5 | 2 | 5 | 2 | 24 |
| Avro | 4 | 5 | 5 | 2 | 3 | 5 | 24 |

Thrift/Protobuf and Avro tie on typical totals. The deciding criteria are: dynamic schema generation (Avro wins), code generation in statically typed languages (Protobuf/Thrift win), and Kafka ecosystem fit (Avro wins via schema registry).

---

## Compatibility Matrix: Change Types vs. Format

For each type of schema change, whether it is safe for each encoding family.

| Change type | JSON convention | Protobuf/Thrift | Avro |
|-------------|-----------------|-----------------|------|
| Add optional field | Safe (lenient parsers) | Safe (new tag, optional/default) | Safe (requires default value) |
| Add required field | Breaking | Breaking — never do post-deployment | N/A (no required concept; use union without null default) |
| Remove field (had default) | Breaking for dependents | Safe (mark tag reserved) | Safe (old readers get default) |
| Remove field (no default) | Breaking | Safe (mark tag reserved) | Breaks backward compatibility |
| Rename field | Breaking | Safe (name not in encoded data) | Backward-only (add alias in reader schema) |
| Change field type (compatible) | Risky (no type safety) | Limited (see type rules) | Possible (Avro converts compatible types) |
| Change field type (incompatible) | Breaking | Breaking | Breaking |
| Reorder fields | Safe | Safe (tags not position-based) | Safe (resolution by name, not position) |
| Add enum value | Risky (old code may error) | Safe (forward: old code ignores) | Safe (forward: old code ignores) |
| Remove enum value | Breaking for users of that value | Breaking | Breaking |

---

## Format Selection Summary by Scenario

| Scenario | Recommended format | Key reason |
|----------|--------------------|-----------|
| Public REST API | JSON | Cross-org boundary; external clients; browser-testable |
| Internal gRPC service, statically typed | Protocol Buffers | Code generation; explicit compatibility; compact encoding |
| Internal service, Facebook/Twitter stack | Apache Thrift | Same as Protobuf; existing ecosystem |
| Kafka event stream with schema registry | Apache Avro | Schema registry native integration; name-based evolution |
| Data lake archival (Hadoop, Parquet pipeline) | Apache Avro | Object container files embed schema; analytics tools native support |
| Database-to-file export with changing schema | Apache Avro | Dynamic schema generation from DB table; no tag management |
| Lightweight in-process cache | Language-specific (cautiously) | Only if truly transient; never persisted or sent over network |
| Dynamic language stack (Python/JS only) | Avro or JSON | Code generation adds no value; name-based resolution works without generated classes |
