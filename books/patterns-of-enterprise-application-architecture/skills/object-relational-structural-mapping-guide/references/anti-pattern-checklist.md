# Anti-Pattern Checklist: O/R Structural Mapping

Five structural anti-patterns flagged in PEAA Chapter 3 and 12.

## 1. Meaningful Key Leakage

**Signal:** The primary key of a table is a business identifier (SSN, email, order-number, product-code, username).

**Why it fails:**
- Real-world identifiers are assigned by humans or external systems — both uniqueness and immutability depend on actors outside your control.
- A mistyped SSN creates a row that is neither unique nor correctable without a key migration.
- Business rules change: email addresses change, product codes get reused, order numbering schemes change.

**Detection in codebase:**
```
Grep for: @Id.*email | @Id.*username | @Id.*name | primary_key=True.*CharField
Schema: PRIMARY KEY (email), PRIMARY KEY (username), PRIMARY KEY (sku)
```

**Fix:** Introduce a surrogate `BIGINT` or UUID PK. Retain the meaningful value as a unique-constrained non-key column (`UNIQUE INDEX`).

---

## 2. Association Table Mapping Bypass (N:M via Repeated FKs)

**Signal:** A many-to-many relationship is modeled as an array/JSON column of IDs, or by adding multiple FK columns (`skill_1_id`, `skill_2_id`, `skill_3_id`).

**Why it fails:**
- Arrays in a column violate first normal form — you cannot join, filter, or count on them reliably with SQL.
- Fixed FK columns have a hard-coded upper bound on the number of associations.
- Neither approach is scalable when relationships grow.

**Detection:**
```
Schema: columns named *_1_id, *_2_id, *_3_id
Code: storing JSON array of IDs in a VARCHAR/TEXT column
```

**Fix:** Create a proper join table: `entity_a_entity_b(entity_a_id FK, entity_b_id FK, PRIMARY KEY(entity_a_id, entity_b_id))`.

---

## 3. Dependent with External FK Reference

**Signal:** A class that is treated as a dependent (no Identity Field, saved by owner) is also referenced by a FK from another table.

**Why it fails:**
- Dependent Mapping's safe delete-and-reinsert strategy breaks when other rows reference the dependent — cascade delete would orphan them or fail the FK constraint.
- Identity ambiguity: if the same dependent row is referenced from two places, which owner is responsible for it?

**Detection:**
```sql
-- FK pointing at what should be a dependent table
REFERENCES tracks(track_id) -- from a playlist_tracks table, while Track is treated as Album dependent
```

**Fix:** Give the child class an Identity Field and change all owner references to Foreign Key Mapping. Establish explicit cascade rules per relationship.

---

## 4. Embedded Value for Shared or Variable Data

**Signal:**
- A value object's columns appear in multiple tables (sharing violation), OR
- The owner table has a variable number of embedded value instances (e.g., `phone_1_number`, `phone_2_number`, `phone_3_number`).

**Why it fails:**
- Shared embedded data becomes inconsistent when one owner's copy is updated but not the others.
- Variable-count embedded values create nullable column sprawl and make "find all customers with a fax number" impossible without checking all numbered columns.

**Detection:**
```
Schema: columns like phone_1_type, phone_1_number, phone_2_type, phone_2_number
Code: same Address class embedded in both Customer and Order tables (duplicated)
```

**Fix for shared data:** Normalize the value into its own table; use Foreign Key Mapping.
**Fix for variable count:** Use a one-to-many child table (Foreign Key Mapping or Dependent Mapping depending on identity needs).

---

## 5. Serialized LOB for Queryable Data

**Signal:** Data stored as XML, JSON blob, or binary BLOB in a column that SQL queries need to filter, sort, or join on.

**Why it fails:**
- SQL cannot efficiently filter or sort on data buried in a LOB without full deserialization at the application layer.
- PostgreSQL JSONB operators (`@>`, `#>>`) can query JSON fields, but this is not portable, and JSONB GIN indexes do not scale as well as normalized table indexes for high-cardinality filtering.
- Reporting tools, BI systems, and data warehouses expect normalized columns.

**Detection:**
```sql
-- Filtering on a CLOB/JSON column with application-side parsing
SELECT * FROM orders WHERE preferences_xml LIKE '%email%'
-- Or: Application code deserializes LOB to filter in memory
customers.filter { deserialize(it.prefs_blob).channel == 'email' }
```

**Fix:** Normalize the queryable fields into columns or a child table. If the LOB is large and only some fields are queried, consider a hybrid: store the full LOB for display but project the queried fields into regular indexed columns.

**Legitimate Serialized LOB uses:**
- Storing a snapshot of an order's line-item state at the time of checkout (immutable, never queried by content).
- Storing user-defined form responses where the schema varies per form and reports run against a separate reporting DB.
- Configuration or settings that are always loaded and deserialized as a whole object, never partially queried.
