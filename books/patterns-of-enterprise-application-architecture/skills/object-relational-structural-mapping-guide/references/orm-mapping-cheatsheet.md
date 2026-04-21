# ORM Mapping Cheatsheet

Per-pattern ORM configuration for six major stacks.

## Identity Field

| Stack | Configuration |
|-------|--------------|
| Hibernate/JPA | `@Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;` |
| EF Core | `public long Id { get; set; }` (convention) or `[Key]` attribute |
| SQLAlchemy | `id = Column(BigInteger, primary_key=True, autoincrement=True)` |
| Django | `id = models.BigAutoField(primary_key=True)` (default since Django 3.2) |
| Rails | Auto-generated `id :bigint` on `create_table` |
| TypeORM | `@PrimaryGeneratedColumn('increment') id: number;` or `@PrimaryGeneratedColumn('uuid')` |

**UUID variant:**
- Hibernate: `@GeneratedValue(strategy = GenerationType.UUID)` (JPA 3.1+) or `@GenericGenerator(name="uuid", strategy="uuid2")`
- EF Core: `public Guid Id { get; set; }` + `ValueGeneratedOnAdd()`
- SQLAlchemy: `id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)`
- Django: `id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`

---

## Foreign Key Mapping

### Single-valued reference (N:1, Album → Artist)

| Stack | Owner side (FK column) | Referenced side |
|-------|------------------------|-----------------|
| Hibernate/JPA | `@ManyToOne @JoinColumn(name="artist_id") Artist artist;` | `@OneToMany(mappedBy="artist") List<Album> albums;` |
| EF Core | `public long ArtistId { get; set; }` + `public Artist Artist { get; set; }` | `public ICollection<Album> Albums { get; set; }` |
| SQLAlchemy | `artist_id = Column(BigInteger, ForeignKey('artists.id'))` + `artist = relationship('Artist', back_populates='albums')` | `albums = relationship('Album', back_populates='artist')` |
| Django | `artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='albums')` | (reverse available as `artist.albums.all()`) |
| Rails | `belongs_to :artist` in Album; `has_many :albums` in Artist | |
| TypeORM | `@ManyToOne(() => Artist) @JoinColumn() artist: Artist;` | `@OneToMany(() => Album, a => a.artist) albums: Album[];` |

---

## Association Table Mapping (N:M)

### Employee ↔ Skill example

| Stack | Configuration |
|-------|--------------|
| Hibernate/JPA | `@ManyToMany @JoinTable(name="employee_skills", joinColumns=@JoinColumn(name="emp_id"), inverseJoinColumns=@JoinColumn(name="skill_id")) Set<Skill> skills;` |
| EF Core | Explicit join entity: `modelBuilder.Entity<EmployeeSkill>().HasKey(es => new { es.EmployeeId, es.SkillId });` |
| SQLAlchemy | `Table('employee_skills', Base.metadata, Column('emp_id', ForeignKey('employees.id')), Column('skill_id', ForeignKey('skills.id')))` then `skills = relationship('Skill', secondary=employee_skills)` |
| Django | `skills = models.ManyToManyField(Skill)` (auto join table) or `skills = models.ManyToManyField(Skill, through='EmployeeSkill')` |
| Rails | `has_many :employee_skills` + `has_many :skills, through: :employee_skills` |
| TypeORM | `@ManyToMany(() => Skill) @JoinTable() skills: Skill[];` |

**When join table needs attributes:** Always use an explicit through/join entity and give it an Identity Field.

---

## Dependent Mapping

### Album → Tracks (Album mapper owns Track persistence)

| Stack | Configuration |
|-------|--------------|
| Hibernate/JPA | `@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true) @JoinColumn(name="album_id") List<Track> tracks;` |
| EF Core | `HasMany(a => a.Tracks).WithOne().HasForeignKey("AlbumId").OnDelete(DeleteBehavior.Cascade)` |
| SQLAlchemy | `tracks = relationship('Track', cascade='all, delete-orphan', passive_deletes=True)` |
| Django | `class Track(models.Model): album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')` |
| Rails | `has_many :tracks, dependent: :destroy` |
| TypeORM | `@OneToMany(() => Track, t => t.album, { cascade: true, eager: true }) tracks: Track[];` |

**Note:** The Track model should not have a reverse `album` reference that is independently navigable by other domain services — enforce access only through Album.

---

## Embedded Value

### Employment → Money + DateRange

| Stack | Configuration |
|-------|--------------|
| Hibernate/JPA | `@Embeddable class Money { BigDecimal amount; String currency; }` + `@Embedded Money salary;` (columns: `salary_amount`, `salary_currency` on `employment` table) |
| EF Core | `[Owned] class Address { string Street; string City; }` + `modelBuilder.Entity<Customer>().OwnsOne(c => c.Address)` |
| SQLAlchemy | `composite(Address, employment.c.addr_street, employment.c.addr_city, employment.c.addr_zip)` or just inline columns |
| Django | Direct fields on the model: `salary_amount = models.DecimalField(...)`, `salary_currency = models.CharField(...)` |
| Rails | `store_accessor :address_data, :street, :city, :zip` or plain columns |
| TypeORM | `@Column() salaryAmount: number; @Column() salaryCurrency: string;` or `@Embedded(() => Money) salary: Money;` |

---

## Serialized LOB

### Department hierarchy as CLOB (use with caution)

| Stack | Configuration |
|-------|--------------|
| Hibernate/JPA | `@Lob @Column(name="dept_hierarchy") String deptHierarchyXml;` |
| EF Core | `public string DeptHierarchyJson { get; set; }` + `HasConversion<string>()` or custom value converter |
| SQLAlchemy | `dept_hierarchy = Column(Text)` or `Column(JSONB)` (PostgreSQL) |
| Django | `dept_hierarchy = models.JSONField()` (Django 3.1+) or `models.TextField()` |
| Rails | `store :dept_hierarchy, coder: JSON` or just `text :dept_hierarchy` |
| TypeORM | `@Column({ type: 'jsonb' }) deptHierarchy: DeptNode;` |

**PostgreSQL JSONB query example (limited use):**
```sql
SELECT * FROM customers WHERE preferences @> '{"channel": "email"}';
-- Only acceptable if: (1) PostgreSQL-only deployment, (2) GIN index on preferences column,
-- (3) query patterns are bounded and known at schema design time
```
