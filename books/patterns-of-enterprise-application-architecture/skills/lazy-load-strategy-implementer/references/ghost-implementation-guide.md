# Ghost Variant: Full Implementation Guide

Source: Patterns of Enterprise Application Architecture, Ch. 11 (Fowler et al., 2002) — C# example

The Ghost is the most infrastructure-heavy Lazy Load variant but has the best identity semantics. Use when:
- Domain objects must participate in sets, maps, or identity comparisons
- Proxy classes per domain class are impractical
- AOP or bytecode manipulation is available

## Core Concept

A ghost is a real domain object initialized with only its primary key. All other fields are null/default. On the first access of any field, the ghost loads its full state from the database. After loading, it behaves identically to an eagerly-loaded object.

Unlike a Virtual Proxy, the ghost IS the domain object — no wrapper. Identity is preserved because the ghost can be placed in the Identity Map immediately upon creation, before it is fully loaded.

## Three Load States

```
GHOST   ──── first field access ────►   LOADING   ──── load complete ────►   LOADED
  │                                                                              │
  └── safe to place in Identity Map                                             └── normal object
      safe to reference cyclically
      NOT safe to access fields
```

The LOADING state prevents re-entrant load calls: when loading Employee triggers loading Department (an association), the Department ghost's `Load()` call is a no-op during its LOADING phase.

## C# Implementation (Fowler's Example)

### Domain Supertype

```csharp
public abstract class DomainObject {
    public long Key { get; private set; }

    private enum LoadStatus { Ghost, Loading, Loaded }
    private LoadStatus _status = LoadStatus.Ghost;

    public bool IsGhost  => _status == LoadStatus.Ghost;
    public bool IsLoaded => _status == LoadStatus.Loaded;

    public DomainObject(long key) { Key = key; }

    public void MarkLoading() {
        Debug.Assert(IsGhost, "Can only start loading from Ghost state");
        _status = LoadStatus.Loading;
    }

    public void MarkLoaded() {
        Debug.Assert(_status == LoadStatus.Loading);
        _status = LoadStatus.Loaded;
    }

    // Every subclass field accessor calls this
    protected void Load() {
        if (IsGhost) DataSource.Load(this);
    }
}
```

### Domain Class (every property must call Load())

```csharp
public class Employee : DomainObject {
    private string _name;
    private Department _department;

    public Employee(long key) : base(key) { }

    // Simple value property
    public string Name {
        get { Load(); return _name; }
        set { Load(); _name = value; }
    }

    // Association property — returns another ghost (triggers that ghost's load on access)
    public Department Department {
        get { Load(); return _department; }
        set { Load(); _department = value; }
    }

    // Collection property — uses DomainList (ghost list)
    public IList TimeRecords { get; private set; } = new DomainList();
}
```

### Registry + Separated Interface (keeps domain ignorant of mappers)

The Load() call in DomainObject cannot directly reference the mapper layer (that would violate layer isolation). Fowler's solution: a Registry with a Separated Interface.

```csharp
// In domain layer — interface only, no mapper reference
public interface IDataSource {
    void Load(DomainObject obj);
}

// In domain layer — Registry (static accessor)
public static class DataSource {
    private static IDataSource _instance;
    public static void SetInstance(IDataSource instance) { _instance = instance; }
    public static void Load(DomainObject obj) { _instance.Load(obj); }
}

// In data source layer — concrete implementation
public class MapperRegistry : IDataSource {
    private readonly IDictionary<Type, Mapper> _mappers = new Dictionary<Type, Mapper>();

    public void Load(DomainObject obj) {
        _mappers[obj.GetType()].Load(obj);
    }
}
// Bootstrap: DataSource.SetInstance(new MapperRegistry(...));
```

### Abstract Mapper Base

```csharp
public abstract class Mapper {
    protected IDictionary<long, DomainObject> _identityMap = new Dictionary<long, DomainObject>();

    // Returns a ghost immediately — places it in Identity Map before loading
    public DomainObject AbstractFind(long key) {
        if (_identityMap.TryGetValue(key, out var cached)) return cached;
        var ghost = CreateGhost(key);
        _identityMap[key] = ghost;
        return ghost;
    }

    protected abstract DomainObject CreateGhost(long key);

    // Called by DataSource.Load() when a ghost field is first accessed
    public void Load(DomainObject obj) {
        if (!obj.IsGhost) return;
        using var cmd = new OleDbCommand(FindStatement, DB.Connection);
        cmd.Parameters.AddWithValue("key", obj.Key);
        using var reader = cmd.ExecuteReader();
        reader.Read();
        LoadLine(reader, obj);
    }

    public void LoadLine(IDataReader reader, DomainObject obj) {
        if (obj.IsGhost) {
            obj.MarkLoading();
            DoLoadLine(reader, obj);
            obj.MarkLoaded();
        }
    }

    protected abstract string FindStatement { get; }
    protected abstract void DoLoadLine(IDataReader reader, DomainObject obj);
}
```

### Concrete Mapper

```csharp
public class EmployeeMapper : Mapper {
    protected override DomainObject CreateGhost(long key) => new Employee(key);

    protected override string FindStatement =>
        "SELECT name, departmentId FROM employees WHERE id = @key";

    protected override void DoLoadLine(IDataReader reader, DomainObject obj) {
        var employee = (Employee) obj;
        employee.Name = (string) reader["name"];

        var deptMapper = (DepartmentMapper) MapperRegistry.Mapper(typeof(Department));
        employee.Department = (Department) deptMapper.AbstractFind((long) reader["departmentId"]);
        // ^ Returns a Department ghost — placed in Identity Map immediately
        // ^ Department data loads on first access to Department.Name etc.

        LoadTimeRecords(employee);
    }

    private void LoadTimeRecords(Employee employee) {
        var listLoader = new ListLoader {
            Sql = "SELECT * FROM time_records WHERE employee_id = @key",
            Mapper = MapperRegistry.Mapper(typeof(TimeRecord))
        };
        listLoader.SqlParams.Add(employee.Key);
        listLoader.Attach((DomainList) employee.TimeRecords);
        // TimeRecords collection stays ghost until first access
    }
}
```

### Ghost List (collection lazy unit)

```csharp
// Ghost list: the collection itself is the lazy unit
public class DomainList : IList {
    private IList _data;
    private bool _isLoaded = false;

    public delegate void Loader(DomainList list);
    public Loader RunLoader;

    private IList Data {
        get {
            if (!_isLoaded) {
                _isLoaded = true;
                RunLoader(this);
            }
            return _data ?? (_data = new ArrayList());
        }
    }

    // Delegate all IList members to Data
    public int Count => Data.Count;
    public object this[int index] { get => Data[index]; set => Data[index] = value; }
    public void Add(object item) => Data.Add(item);
    // ... other IList members
}
```

## Python Equivalent (using descriptors)

Python can implement Ghost via descriptors — a more Pythonic alternative to bytecode manipulation.

```python
class LazyField:
    """Descriptor that triggers ghost load on first access."""
    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        obj._load_if_ghost()
        return getattr(obj, self._name, None)

    def __set__(self, obj, value):
        setattr(obj, self._name, value)


class DomainObject:
    GHOST = "ghost"
    LOADING = "loading"
    LOADED = "loaded"

    def __init__(self, key):
        self.key = key
        self._status = self.GHOST

    def _load_if_ghost(self):
        if self._status == self.GHOST:
            DataSource.load(self)

    def mark_loading(self): self._status = self.LOADING
    def mark_loaded(self):  self._status = self.LOADED
    @property
    def is_ghost(self): return self._status == self.GHOST


class Employee(DomainObject):
    name = LazyField()
    department = LazyField()
```

## When Ghost Is the Right Choice

- You need domain objects usable in sets/dicts by identity without proxy confusion
- Your stack has AOP or descriptor support to instrument field access transparently
- You are building a framework layer that many domain classes will inherit
- You want the ghost in the Identity Map *before* load (prevents circular-load bugs)

## When Ghost Is NOT Worth the Complexity

- An ORM already ships Virtual Proxy and handles identity via its session cache — use that
- The domain model is simple with few associations — Lazy Initialization is sufficient
- The team is unfamiliar with AOP/bytecode instrumentation — the tooling cost is too high
