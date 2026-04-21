# Pattern Decision Table

Full routing table for PEAA structural mapping patterns, including edge cases.

## Primary Routing Table

| Domain Structure | Default Pattern | Edge Case / Override |
|-----------------|-----------------|----------------------|
| Persistable entity with independent lifecycle | Identity Field (surrogate) | Existing DB with meaningful key: map it but document the risk |
| Single-valued reference to another entity (1:1) | Foreign Key Mapping | If the referenced entity is private and never shared → consider Dependent Mapping |
| One-to-many collection (parent owns children) | Foreign Key Mapping (FK on child side) | If children have no identity and no external FK references → Dependent Mapping |
| Many-to-many relationship | Association Table Mapping | Always; no alternative in relational DBs |
| Many-to-many with attributes | Association Table Mapping → promote to entity | The link table entity gets its own Identity Field |
| Child object with no independent identity | Dependent Mapping | If another entity needs a direct FK to the child → give child an Identity Field |
| DDD Value Object (Money, Address, DateRange) | Embedded Value | If value is shared across owners → normalize to its own table with FK |
| Complex non-queryable subgraph | Serialized LOB | Only when zero SQL query need on internals; prefer JSON over BLOB |
| Self-referential hierarchy (parent/child same type) | Foreign Key Mapping (`parent_id` self-referencing FK) | If unbounded depth + complex traversal → consider Serialized LOB with tree path |

## Identity Field — Key Type Decision

| Criterion | Choice |
|-----------|--------|
| New schema, no legacy constraints | Surrogate `BIGINT` auto-increment |
| Distributed system, no central sequence | UUID v4 or v7 (ordered) |
| Existing natural key that IS truly immutable and unique | Keep it, but add a surrogate for O/R mapping |
| Class Table or Concrete Table Inheritance hierarchy | Keys must be unique across the hierarchy, not just per-table |

## Association Table Mapping — When to Add Attributes

| Signal | Action |
|--------|--------|
| Join table needs start_date / end_date | Add columns to join table; consider promoting to entity |
| Join table needs role, weight, or type | Promote to a first-class entity with Identity Field |
| Join table rows must be individually updateable | Promote to entity (need Identity Field for row identity) |
| Join table is append-only (immutable history) | Can keep as plain Association Table; add created_at timestamp |

## Dependent Mapping — Qualification Checklist

A child qualifies for Dependent Mapping only if ALL of the following are true:

- [ ] Has exactly one owner
- [ ] No other table holds a FK pointing to the child's table
- [ ] No in-memory entity other than the owner (or its other dependents) holds a persisted reference to the child
- [ ] Child cannot be loaded independently (no finder method)
- [ ] Child's lifecycle is fully controlled by the owner (created/deleted when owner is)

If ANY check fails, the child needs an Identity Field and Foreign Key Mapping.

## Embedded Value — Qualification Checklist

An object qualifies for Embedded Value only if ALL of the following are true:

- [ ] It is a Value Object (no identity — two instances with same values are equal)
- [ ] It belongs to exactly one owning entity
- [ ] The cardinality is 1:1 (or a small fixed set)
- [ ] Its fields will never be the sole target of SQL filtering, sorting, or joining outside the owner
- [ ] It is not shared across multiple owners

## Serialized LOB — Anti-Pattern Detection

Stop and reconsider if any of these signals are present:

| Signal | Problem |
|--------|---------|
| A SQL query filters on a field inside the LOB | The data is queryable — normalize it |
| A report joins to data inside the LOB | Same as above; normalize or replicate to a reporting table |
| The LOB class definition changes frequently | Binary BLOBs will break; JSON CLOBs need migration scripts |
| Multiple objects reference data inside the LOB | LOB identity hazard — the data will be duplicated or become inconsistent |
| The LOB column is on a table with many rows and high read frequency | Deserializing LOBs at scale has significant CPU cost |

## Modern Stack Notes

| ORM | Identity Field | Foreign Key Mapping | Association Table | Dependent Mapping | Embedded Value | Serialized LOB |
|-----|---------------|---------------------|-------------------|-------------------|----------------|----------------|
| Hibernate/JPA | `@Id @GeneratedValue` | `@ManyToOne @JoinColumn` | `@ManyToMany @JoinTable` | `cascade=ALL, orphanRemoval=true` | `@Embedded @Embeddable` | `@Lob String` / `@Column(columnDefinition="jsonb")` |
| EF Core | `[Key]` / convention `Id` | `public int FkId` + navigation | explicit join entity | `HasMany.WithOne.OnDelete(Cascade)` | `[Owned]` / `OwnsOne` | `string JsonField` mapped to JSON column |
| SQLAlchemy | `Column(Integer, primary_key=True)` | `ForeignKey` + `relationship` | association Table + secondary | `cascade="all, delete-orphan"` | `composite()` | `Column(JSON)` or `Column(Text)` |
| Django | auto `id` field | `ForeignKey(on_delete=CASCADE)` | `ManyToManyField` or `through` | `related_name='+'` + cascade | inline fields on model | `JSONField` |
| Rails ActiveRecord | auto `id` | `belongs_to` / `has_many` | `has_many :through` | `has_many dependent: :destroy` | virtual attrs / `store_accessor` | `store :data, accessors: [...]` |
| TypeORM | `@PrimaryGeneratedColumn` | `@ManyToOne @JoinColumn` | `@ManyToMany @JoinTable` | `cascade: true` | `@Column` on embedded | `@Column('jsonb')` |
