# Schema Evolution Rules Reference

## Definitions

**Backward compatibility:** New code can read data written by old code.
- If you deploy new code and it must read records written by old code (e.g., from a database), backward compatibility is required.

**Forward compatibility:** Old code can read data written by new code.
- If old and new code versions run simultaneously (rolling upgrade), old code must be able to read records written by new code without crashing.

**Both directions simultaneously:** Required during rolling upgrades and in message broker scenarios where producers and consumers deploy independently.

---

## Protocol Buffers Rules

### Field Tag Invariants (permanent constraints)

1. **A field's tag number is its permanent identity.** The tag number — not the field name — is what appears in the encoded bytes. It cannot change after any data has been written.

2. **A removed field's tag number is permanently retired.** Mark it with `reserved` in the `.proto` file. Never reuse it for a new field.

3. **A removed field's name is also retired.** Mark it with `reserved "field_name"` as well. This prevents a future developer from accidentally adding a new field with the same name but a different tag.

```protobuf
// Correct way to retire a field:
message Person {
  reserved 3, 4;
  reserved "legacy_score", "old_interests";
  // Fields 3 and 4 existed before; they are gone now.
  // New fields must use tags 5, 6, 7, ...
  string user_name = 1;
  int64 favorite_number = 2;
}
```

### Change Classification Table

| Change | Backward compatible? | Forward compatible? | Notes |
|--------|---------------------|---------------------|-------|
| Add optional field (new tag) | Yes | Yes | New code reads old data: missing field gets default. Old code reads new data: skips unknown tag. |
| Add required field | No | No | Old data didn't write the field; required check fails on read. Never add required after initial deployment. |
| Remove optional field (mark reserved) | Yes | Yes | Old readers: field is absent, gets default or zero. New readers: ignore old data's bytes for retired tag. |
| Remove required field | No | No | Old code that wrote data as required will have the field; new code that has removed it still sees it in the bytes and may error. Mark required → optional first, deploy everywhere, then remove. |
| Rename a field (same tag) | Yes | Yes | Names are not in the encoded bytes. Tag is unchanged. |
| Change tag number | No | No | Breaking permanently. All existing encoded data is now misinterpreted. |
| Reuse a retired tag number | No | No | Old data with that tag now misinterpreted as the new field type. Silent data corruption. |
| Change int32 → int64 | Yes | Partial | New code reads old int32 data: zero-pads to 64 bits (safe). Old code reads new int64 data: truncates if value > 2^31. Risky if values may exceed int32 range. |
| Change optional → repeated | Yes | Yes | New code reading old data: list with 0 or 1 element. Old code reading new data: reads last element of repeated field. |
| Change repeated → optional | Partial | Partial | Risky: new code reading old data sees only last element; data loss if old data had multiple values. |
| Add enum value | Yes | Partial | Old code reading new data: may receive unknown enum value. Depends on implementation (some error, some use 0/default). |
| Remove enum value | Partial | No | Old code that reads data with the removed value may get an error or the default. Risky. |

### Datatype Compatibility (Protobuf wire types)

Fields with the same wire type can be changed to compatible types:
- Varint (wire type 0): `int32`, `int64`, `uint32`, `uint64`, `sint32`, `sint64`, `bool`, `enum` are interchangeable with truncation/extension rules
- 64-bit (wire type 1): `fixed64`, `sfixed64`, `double` are interchangeable
- Length-delimited (wire type 2): `string`, `bytes`, embedded messages, repeated fields are interchangeable
- 32-bit (wire type 5): `fixed32`, `sfixed32`, `float` are interchangeable

Cross-wire-type changes are breaking (the parser cannot skip the bytes correctly).

### Recommended CI Tooling

- `buf breaking --against .git#branch=main` — detects breaking changes against the main branch before merge
- `buf lint` — enforces naming conventions and structural rules in `.proto` files
- Configure as a required CI check on all `.proto` file changes

---

## Apache Thrift Rules

Thrift has the same field-tag-based rules as Protocol Buffers with minor variations.

### BinaryProtocol vs. CompactProtocol

Both protocols encode the same schema and have the same compatibility rules. CompactProtocol is preferred for production use:
- BinaryProtocol: type (1 byte) + tag (2 bytes) + value = 59 bytes for the example record
- CompactProtocol: type + tag packed into 1 byte + varint value = 34 bytes for the same record

Switch between BinaryProtocol and CompactProtocol only at a fleet-wide migration point — mixing protocols within the same stream requires all readers and writers to switch simultaneously.

### Differences from Protocol Buffers

1. **List datatype:** Thrift has a dedicated `list<T>` datatype (parameterized by element type). This does not support the `optional` → `list` promotion that Protobuf's `repeated` supports.

2. **`required` vs. `optional`:** Thrift enforces `required` strictly. Same rule as Protobuf: never add a required field after initial deployment.

3. **Nested lists:** Thrift's dedicated list type supports nested lists (e.g., `list<list<string>>`). Protobuf's repeated fields do not directly support nesting — nested lists require wrapping in a message type.

### Change Classification Table

Same as Protocol Buffers table above, with the addition:

| Change | Backward compatible? | Forward compatible? | Notes |
|--------|---------------------|---------------------|-------|
| Change optional field to list | No | No | Thrift's list type is distinct from optional; no automatic promotion |

---

## Apache Avro Rules

### Core Mechanism: Writer/Reader Schema Resolution

The Avro library takes the writer's schema and the reader's schema and translates the data:
- Field present in writer, absent in reader: ignored (the bytes are skipped correctly because the writer's schema gives the type needed to skip)
- Field present in reader, absent in writer: filled with the default value declared in the reader's schema
- Field present in both: value is translated from writer's type to reader's type (if compatible)
- Fields are matched by name, not position (order in the schema does not matter for compatibility)

### Schema Distribution Mechanisms (required — choose one)

| Context | Mechanism | Implementation |
|---------|-----------|----------------|
| Large file, all records same schema | Embed writer's schema in file header | Avro object container file format; reader gets schema from file header |
| Database with per-record writes | Version number per record + schema registry DB | Store schema version as integer at start of every record; reader fetches schema by version from a schema table in the database |
| Network connection (two services) | Negotiate on connection setup | Avro RPC protocol: client and server exchange schemas at handshake; use same schema for connection lifetime |
| Kafka topics | Schema ID per message + schema registry service | 4-byte schema ID in message header; Confluent Schema Registry stores schemas by ID; consumer fetches on first encounter |

### Change Classification Table

| Change | Backward compatible? | Forward compatible? | Notes |
|--------|---------------------|---------------------|-------|
| Add field with default value | Yes | Yes | Old readers: get default for missing field. New readers: ignore field if writer didn't include it. |
| Add field without default value | No | Yes | Old readers: no default to supply; parsing fails or produces incorrect data. |
| Remove field that had default | Yes | Yes | Old readers: field is absent in new writer's data; default is used. New readers: field not present in new schema; old writer's data has it; ignored. |
| Remove field without default | Yes | No | New readers reading old writer's data: field is present in writer's schema but not reader's; ignored (safe). Old readers reading new writer's data: expected field not present; no default; fails. |
| Rename field | Backward only | No | Add old name as alias in reader's schema to restore forward compat. Example: reader schema has `"name": "userId", "aliases": ["user_id"]`. |
| Reorder fields | Yes | Yes | Resolution is by name; field order is irrelevant. |
| Change type (Avro-compatible) | Yes | Yes | Avro spec defines compatible type promotions: int→long, int→float, int→double, long→float, long→double, float→double, string→bytes, bytes→string. |
| Change type (incompatible) | No | No | Any other type change is breaking. |
| Add branch to union type | Backward only | No | Old readers don't know the new branch. |
| Remove branch from union type | No | Backward only | New readers don't handle the old branch. |
| Add null to union (make nullable) | Yes | Yes | `union { null, long }` — can add null as default branch. |

### Avro Null and Default Values

Avro's default value must be of the type of the first branch in a union:

```json
// Correct: null is first branch; default is null
{"name": "favoriteNumber", "type": ["null", "long"], "default": null}

// Correct: long is first branch; default is a long
{"name": "favoriteNumber", "type": ["long", "null"], "default": 0}

// WRONG: default null but null is not first branch — Avro schema parse error
{"name": "favoriteNumber", "type": ["long", "null"], "default": null}
```

### Schema Registry Compatibility Modes (Confluent Schema Registry)

| Mode | Meaning | Recommended for |
|------|---------|-----------------|
| BACKWARD | New schema is backward compatible with the immediately previous version | Most common; simple use cases |
| BACKWARD_TRANSITIVE | New schema is backward compatible with ALL previous versions | Recommended for Kafka topics with long retention (messages from old versions may be replayed) |
| FORWARD | New schema is forward compatible with the immediately previous version | Rare; use when consumers upgrade before producers |
| FORWARD_TRANSITIVE | Forward compatible with ALL previous versions | Rare |
| FULL | Both BACKWARD and FULL with immediately previous | Use when producers and consumers upgrade independently at any time |
| FULL_TRANSITIVE | Both BACKWARD_TRANSITIVE and FORWARD_TRANSITIVE | Strictest; use for long-lived event streams with independent deployments |
| NONE | No compatibility checking | Only for development/experimentation |

---

## JSON / XML Rules (Convention-Based)

JSON has no built-in compatibility mechanism. These are conventions:

### Safe by convention (if all consumers follow lenient parsing)

| Change | Notes |
|--------|-------|
| Add new field to response | Consumers must ignore unknown fields (lenient parsing). This is the JSON convention but not enforced by the format. |
| Add optional query parameter to request | Servers must ignore unknown parameters or return a helpful error. |
| Add optional body field to request | Server reads known fields; unknown fields ignored. |

### Breaking changes (require API version bump)

| Change | Why it's breaking |
|--------|------------------|
| Remove a field from response | Consumers that read the field get null/undefined and may crash or produce wrong results |
| Rename a field | Same as remove + add; old name becomes null |
| Add a required field to request | Old clients that don't send it will fail validation |
| Change field type | JSON does not enforce types; consumers parse to their expected type; mismatch produces silent corruption or parse error |
| Change number precision | Integers > 2^53 are not representable in IEEE 754 double; JavaScript consumers silently corrupt them |

### API Versioning Patterns

| Pattern | Example | When to use |
|---------|---------|-------------|
| URL versioning | `/v1/users`, `/v2/users` | Recommended for breaking changes; easy to route in reverse proxy |
| Accept header versioning | `Accept: application/vnd.myapi.v2+json` | RESTful purists prefer this; harder to test with browser |
| Query parameter | `?version=2` | Simplest; not RESTful; fine for internal APIs |
| Feature flags | `?include=newField` | For optional capabilities; not for breaking changes |

---

## Dataflow-Specific Compatibility Checklists

### Database (Mode A)

- [ ] Every schema change is backward compatible (data may be years old)
- [ ] New code handles missing fields from old records (null, zero, or explicit default)
- [ ] Read-modify-write operations preserve unknown fields (test this explicitly)
- [ ] Schema migration scripts do not rewrite data unnecessarily (expensive and introduces risk)
- [ ] Archival dumps use a self-describing format (Avro object container files or JSON with schema snapshot)

### Service Calls (Mode B)

- [ ] Server-side schema changes are backward compatible with the current client version
- [ ] Client-side schema changes are forward compatible with the current server version
- [ ] For public APIs: changes are backward compatible with ALL deployed client versions
- [ ] API versioning strategy is defined before first breaking change is needed
- [ ] Compatibility is tested with both old-client → new-server and new-client → old-server scenarios

### Message Passing (Mode C)

- [ ] Schema changes are both backward and forward compatible simultaneously
- [ ] All new fields have default values (Avro) or are optional (Protobuf)
- [ ] Consumers that republish messages preserve unknown fields
- [ ] Schema registry or equivalent schema distribution mechanism is operational before producers use new schema
- [ ] Consumer handles messages written by schema versions older than the current version
- [ ] Schema registry compatibility mode is set to BACKWARD_TRANSITIVE or FULL_TRANSITIVE for long-retention topics
