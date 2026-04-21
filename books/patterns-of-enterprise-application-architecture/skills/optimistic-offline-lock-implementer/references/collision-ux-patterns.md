# Collision UX Patterns

When Optimistic Offline Lock detects a conflict (row count = 0), the user must receive actionable information. Three levels of UX quality, from minimum to ideal.

---

## Level 1 — Abort + Inform (Minimum Acceptable)

Re-query for `modified_by` and `modified_at` before throwing. Display:

> **Your changes could not be saved.**
> This record was last modified by **{modifiedBy}** at **{modifiedAt}**.
> Please reload and re-apply your changes.
>
> [Reload Record] [Cancel — Discard My Changes]

**What NOT to say:**
- "A concurrency error occurred." (no context)
- "Please try again." (unhelpful without reload)
- "Error 409." (technical, user-hostile)

**API 409 response schema:**
```json
{
  "error": "Conflict",
  "message": "Record was modified by Alice at 2025-04-20T14:34:00Z",
  "currentVersion": 8,
  "modifiedBy": "alice@example.com",
  "modifiedAt": "2025-04-20T14:34:00Z"
}
```

---

## Level 2 — Show Conflict Diff

After detecting a collision, fetch both versions:
- **Their version** (current DB state, version N)
- **Your proposed changes** (what the user submitted)

Display side-by-side or highlighted diff:

| Field | Current Value (Alice's save) | Your Proposed Value |
|-------|------------------------------|---------------------|
| Name  | Smith Jr.                    | Smythe              |
| Phone | 555-1234 (unchanged)         | 555-1234 (unchanged)|
| Email | smith@new.com                | smith@example.com   |

Actions: [Apply My Changes] [Keep Current] [Pick Per Field] [Cancel]

---

## Level 3 — Merge (Most Powerful, Most Complex)

Auto-merge non-conflicting field changes. Only surface the user for genuinely conflicting fields (both sessions changed the same field to different values).

Logic:
```
For each field:
  if onlyUserChanged(field):   auto-apply user's value
  if onlyTheirChanged(field):  auto-apply their value
  if bothChanged(field):       present conflict to user
  if neitherChanged(field):    keep as-is
```

Fowler on merge: "A quality merge strategy makes Optimistic Offline Lock very powerful … users rarely have to redo any work." Notes that enterprise business objects can merge — it is "a pattern unto its own" and per-entity complexity varies.

Implementation cost: high. Each entity type needs a merge strategy. Reserve for high-value, frequently-edited records.

---

## Force-Save

Allow the user to explicitly overwrite the current DB state with their version. Must be intentional — never the default.

Implementation:
1. User triggers "Save Anyway" action.
2. Client re-sends request with the CURRENT version (fetched after collision, not the original).
3. Server applies user's changes on top of the current version.

```
GET /customers/42  →  version: 8 (current after Alice's save)
PUT /customers/42  →  body: { ...user's fields, version: 8 }
```

The force-save succeeds because the client now holds the latest version. Functionally, the user is saying "I know Alice changed this; overwrite with my values."

---

## Early Conflict Detection: checkCurrent

For long-running workflows, detect conflicts early (before commit):

```java
public boolean checkCurrent(DomainObject obj) {
    int dbVersion = queryVersion(obj.getId());
    return dbVersion == obj.getVersion();  // false = someone changed it
}
```

Call this at natural pause points in the workflow (e.g., between steps of a multi-page wizard). If a conflict is already visible, fail early and save the user from completing 20 more minutes of work that will not commit.

Caveat: `checkCurrent` never guarantees success at commit time. It is an early-warning mechanism, not a guarantee.

---

## License

CC-BY-SA-4.0 — Source: BookForge / Patterns of Enterprise Application Architecture by Fowler et al.
