---
name: security-testing-strategy
description: |
  Select and implement a layered security testing strategy for a codebase: design unit tests for security properties (boundary conditions, negative inputs, access control invariants), set up integration testing with non-production seed data (avoiding the production data copy anti-pattern), choose and configure dynamic analysis sanitizers (AddressSanitizer for memory corruption, ThreadSanitizer for race conditions, MemorySanitizer for uninitialized reads — with their performance cost tradeoff accounted for in CI/CD scheduling), plan fuzz testing (write effective fuzz drivers using libFuzzer/AFL, apply dictionary inputs for structured formats like HTTP/SQL/JSON, build a seed corpus, integrate continuous fuzzing via ClusterFuzz or OSS-Fuzz), and integrate static analysis at the right depth for each development stage (linters in the IDE commit loop, abstract interpretation nightly, formal methods for safety-critical paths). Use when creating a security testing plan for a new service, setting up fuzz testing for a parser or protocol implementation, integrating static analysis into a CI/CD pipeline, adding sanitizer-enhanced nightly builds, or auditing coverage gaps found during secure-code-review. Produces a security testing strategy document with tool selection rationale, CI/CD integration plan, and coverage priorities derived from code review findings.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/security-testing-strategy
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - secure-code-review
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [13]
tags:
  - security
  - testing
  - fuzzing
  - static-analysis
  - dynamic-analysis
  - ci-cd
execution:
  tier: 3
  mode: full
  inputs:
    - type: document
      description: "Secure code review findings report (output of secure-code-review) — drives testing priorities and tool selection"
    - type: codebase
      description: "Source code directory or architecture description of the system under test — determines applicable sanitizers, fuzz targets, and static analysis tools"
    - type: document
      description: "Existing CI/CD pipeline description (optional) — determines where to integrate each testing layer"
  tools-required: [Read, Grep]
  tools-optional: [Bash, Write]
  mcps-required: []
  environment: "Run inside the repository root or against an architecture description. Grep identifies candidate fuzz targets (parsers, protocol handlers, codec implementations) and existing test infrastructure. Write produces the strategy document."
discovery:
  goal: "Produce a security testing strategy document: layered tool selection (unit → integration → dynamic analysis → fuzzing → static analysis), CI/CD integration plan, seed corpus and fuzz driver guidance, and coverage priorities derived from code review findings"
  tasks:
    - "Map secure-code-review findings to testing gaps — each finding class has a corresponding testing layer that can prevent future regressions"
    - "Identify unit testing priorities: security boundary conditions, negative inputs, access control invariants, capacity overflow scenarios"
    - "Audit integration test environment setup for the production data copy anti-pattern"
    - "Select and configure sanitizers (ASan/UBSan/TSan/MSan/LSan) matched to language and bug classes; schedule in CI/CD accounting for performance cost"
    - "Identify fuzz targets: parsers, decoders, protocol handlers, compression implementations"
    - "Plan fuzz driver design: avoid nondeterminism, slow I/O, intentional crashes, and integrity checks that block fuzzer progress"
    - "Select seed corpus sources and apply dictionary-based input for structured formats"
    - "Select static analysis depth per development stage: linters at commit, abstract interpretation nightly or at code review, formal methods for safety-critical paths"
    - "Integrate ClusterFuzz or OSS-Fuzz for continuous fuzzing if the project is open source or has sustained infrastructure"
  audience:
    roles: ["security-engineer", "software-engineer", "site-reliability-engineer", "tech-lead"]
    experience: "intermediate — assumes familiarity with CI/CD pipelines, basic compiler toolchains, and at least one unit testing framework"
  triggers:
    - "Security testing plan needed for a new service or module"
    - "Set up fuzz testing for a parser, decoder, or protocol implementation"
    - "Integrate static analysis into a CI/CD pipeline"
    - "Add sanitizer-enhanced nightly builds to catch memory corruption"
    - "Coverage gaps identified during secure-code-review need a testing plan to prevent regressions"
    - "Preparing a service for security review before launch"
  not_for:
    - "Threat modeling or adversary profiling — use adversary-profiling-and-threat-modeling"
    - "Reviewing existing code for vulnerabilities — use secure-code-review"
    - "Deployment pipeline security — use secure-deployment-pipeline"
    - "Designing access control policy — use least-privilege-access-design"
---

## When to Use

Use this skill when you need to select and integrate the right testing layers to make a codebase resilient against the inputs it encounters — including inputs an attacker controls.

Invoke it for:
- New services or modules that lack a security testing plan
- Systems that parse external input (files, network protocols, API requests) and have no fuzz testing in place
- Codebases where secure-code-review found vulnerability classes (injection, memory corruption, race conditions) that need automated test coverage to prevent regression
- CI/CD pipelines that run only unit tests — missing dynamic analysis, sanitizers, and static analysis
- Open source projects eligible for OSS-Fuzz integration

Start by reading the secure-code-review findings report. The anti-patterns found there drive testing priorities: SQL injection findings mean unit tests for parameterized query enforcement; memory corruption patterns mean AddressSanitizer integration; concurrent access patterns mean ThreadSanitizer.

Do not use this skill for threat modeling, access control design, or reviewing existing code for vulnerabilities — those are separate skills.

---

## Context and Input Gathering

Before building the strategy, establish:

1. **Language and runtime**: What language(s) is the codebase in? (Determines available sanitizers and static analysis tools. ASan/TSan/MSan are C/C++ compiler-instrumentation tools; Go has go-fuzz and race detector; Java has Error Prone.)
2. **Input surface**: Where does external input enter the system — HTTP request bodies, file uploads, network packets, deserialized data? These are the fuzz targets.
3. **Existing test infrastructure**: What unit and integration test frameworks are already in use? What CI/CD system? (Determines integration points.)
4. **Secure-code-review findings**: Which vulnerability classes were identified? These determine which sanitizers and test priorities are highest value.
5. **Safety-criticality level**: Is this avionics, medical device, or cryptographic infrastructure? (Determines whether formal methods are warranted.)
6. **Infrastructure budget**: Can the project sustain continuous fuzzing VMs (ClusterFuzz), or is periodic fuzzing more appropriate?

---

## Process

### Step 1 — Map Code Review Findings to Testing Gaps

**WHY**: Testing priorities should be driven by known vulnerability classes, not coverage metrics alone. Each class of finding from secure-code-review has a testing layer that can detect it automatically and prevent future regressions. Without this mapping, teams add tests indiscriminately and miss the highest-risk paths.

For each finding class from the secure-code-review report, map it to a testing layer:

| Finding Class | Primary Testing Layer | Secondary Layer |
|---|---|---|
| SQL injection / parameterized query gaps | Unit tests verifying parameterized query enforcement | Integration tests with a QA database instance |
| XSS / unescaped HTML rendering | Unit tests with malicious input payloads (`<script>`, `javascript:`) | Fuzzing of template rendering paths |
| Memory corruption (buffer overflows, use-after-free) | AddressSanitizer + fuzzing of affected parsers | Nightly sanitizer-enhanced CI builds |
| Race conditions | ThreadSanitizer on concurrent code paths | Integration tests with parallelism stress |
| Uninitialized memory reads | MemorySanitizer | AddressSanitizer (catches many cases) |
| Integer overflow / undefined behavior | UndefinedBehaviorSanitizer | Fuzz testing with edge-case inputs |
| Injection into parsers / decoders | Fuzz testing with a seed corpus + dictionary | ASan + fuzz driver |
| Auth bypass from deep nesting | Unit tests explicitly testing each nested branch | Mutation testing |

Produce a prioritized list of testing gaps to address, ordered by severity of the original finding.

### Step 2 — Design Unit Tests for Security Properties

**WHY**: Unit tests are the fastest feedback loop — they run locally and in every CI commit. For security, they must go beyond happy-path validation to exercise the boundary conditions, malformed inputs, and access control invariants that are most likely to fail under adversarial use. Tests written alongside security reviews capture the cases the engineer checked manually and prevent those cases from regressing as the codebase evolves.

Design unit tests for these security-relevant categories:

**Boundary and overflow conditions**: For any function that accepts a size, quota, or numeric parameter, test values near the limits of the variable's type. A quota management system, for example, should be tested with requests involving negative byte values, values that would overflow the integer type used to represent them, and transfers that bring the total quota to exactly the limit.

**Malicious and malformed inputs**: For every entry point that receives user-controlled data, write tests with inputs that represent known attack patterns:
- SQL injection strings: `' OR username='admin`
- XSS payloads: `<script>alert(1)</script>`, `javascript:void(0)`
- Path traversal: `../../etc/passwd`
- Null bytes, extremely long strings, binary data

**Access control invariants**: For systems with permission models, write parameterized tests that exercise the Cartesian product of roles and actions:

```python
# Parameterized test — run the same test across multiple inputs
# to verify access control without duplicating boilerplate
@parameterize([
    ("billing_admin", "request_quota", True),   # should succeed
    ("standard_user", "request_quota", False),  # should be denied
    ("billing_admin", "delete_cluster", True),
    ("standard_user", "delete_cluster", False),
])
def test_quota_access_control(role, action, expected_allowed):
    assert service.can_perform(role, action) == expected_allowed
```

**Error message safety**: Verify that error responses do not leak internal state, stack traces, or system information that would assist an attacker.

**When to write these tests**: Write them immediately after writing the security-relevant code, so the cases the engineer checked manually are captured. In organizations with code review, a peer reviewer should verify that the tests are robust — checking that new tests can't trivially pass if the security check is removed (mutation testing criterion).

### Step 3 — Audit Integration Test Environment Setup

**WHY**: Integration tests exercise real dependencies — databases, network services, external APIs — and therefore expose real data to anyone who can run the tests. Copying production databases into test environments is a named anti-pattern: production data contains sensitive personal information that will be accessible to all test runners and visible in test logs, violating the principle of least privilege and creating a data breach risk from the test infrastructure itself. Seeded non-production data also makes tests hermetic — the environment starts from a known clean state, which eliminates a major source of flakiness.

**The anti-pattern to identify and eliminate**:

```
# ANTI-PATTERN: production database mirrored to test environment
test_db = copy_production_database(prod_db)  # exposes PII to test runners
integration_test(test_db)
```

**The correct pattern**:

```
# CORRECT: seed the test environment with non-sensitive synthetic data
test_db = create_empty_database()
seed_with_synthetic_data(test_db, [
    {"team": "imaginary_team_1", "quota_bytes": 1024},
    {"team": "imaginary_team_2", "quota_bytes": 512},
])
integration_test(test_db)
```

Audit each integration test setup and look for:
- Direct connections to production databases or services
- Data import scripts that pull from production backups
- Environment variables that point to production credentials

For each such case, replace with synthetic seed data. The seed data should be:
- Representative of the real-world scenarios the tests exercise (enough variety to exercise security boundary conditions)
- Free of any real personal data, credentials, or business-sensitive values
- Checked into the repository alongside the tests, so the environment can always be rebuilt to a known state

### Step 4 — Select and Configure Sanitizers

**WHY**: Memory corruption bugs — buffer overflows, use-after-free, uninitialized reads, race conditions — are the root cause of the most severe security vulnerabilities (including Heartbleed). They are invisible to code review and to unit tests that don't trigger the exact input sequence that causes the corruption. Sanitizers work by instrumenting the compiled binary with additional instructions that detect these conditions at runtime, with precise diagnostic output pointing to the exact line of code responsible. They are the most effective automated tool for finding this class of bug before it reaches production.

**The Google Sanitizers suite** (LLVM/GCC-backed, C/C++ primary but some support other languages):

| Sanitizer | Flag | What It Detects | Use Case |
|---|---|---|---|
| AddressSanitizer (ASan) | `-fsanitize=address` | Out-of-bounds accesses, use-after-free, heap/stack/global buffer overflows | All C/C++ codebases |
| UndefinedBehaviorSanitizer (UBSan) | `-fsanitize=undefined` | Signed integer overflow, null pointer dereference, misaligned access | Combined with ASan |
| ThreadSanitizer (TSan) | `-fsanitize=thread` | Race conditions in concurrent code | Multi-threaded services |
| MemorySanitizer (MSan) | `-fsanitize=memory` | Reads from uninitialized memory | Security-sensitive data handling |
| LeakSanitizer (LSan) | `-fsanitize=leak` | Memory leaks and resource leaks | Long-running services |

**Performance cost — the core tradeoff**:

Sanitizer-instrumented binaries can be orders of magnitude slower than native binaries. ASan typically adds 2x overhead; MSan can add 3x. This makes it impractical to run sanitizer builds on every commit in the same pipeline as fast unit tests. The established practice is:

- **Fast unit and integration tests**: Run on every commit, no sanitizers — native build speed
- **Sanitizer-enhanced pipelines**: Run nightly (or on a separate slower CI tier), with ASan + UBSan as the baseline combination
- **Fuzz testing**: Always pair with ASan — the fuzzer generates inputs, ASan detects the memory corruption they trigger

**CI/CD integration**:

```bash
# Bazel example — build ASan variant
build:asan --copt -fsanitize=address
build:asan --linkopt -fsanitize=address
build:asan --copt -fno-omit-frame-pointer
build:asan --copt -O1 --copt -g

# Run nightly in CI
$ CC=clang CXX=clang++ bazel build --config=asan //...
$ bazel test --config=asan //...
```

For Go: use `-race` flag for race condition detection (equivalent to TSan). Python: use Valgrind for C extensions, or memory profilers for Python-native code.

**ASan example output** (shows precisely where the violation occurred and where the memory was originally allocated and freed):

```
ERROR: AddressSanitizer: heap-use-after-free on address 0x...
READ of size 1 at ...
    #0 in main use-after-free.c:5:10
SUMMARY: AddressSanitizer: heap-use-after-free use-after-free.c:5:10 in main
```

When a sanitizer flags a "known safe" function (for example, a signed integer overflow that is intentionally discarded and has no security consequence), annotate it explicitly: `__attribute__((no_sanitize("undefined")))`. Add annotations only after careful review — they suppress real detections and can create false negatives. Document the reason in a comment.

### Step 5 — Plan Fuzz Testing

**WHY**: Fuzz testing finds bugs that no human would think to test for — unexpected input combinations that trigger crashes, memory corruption, or denial-of-service conditions. File parsers, network protocol handlers, compression codecs, and audio/video decoders are the highest-value fuzz targets because they process complex, adversary-controlled inputs that can reach many code paths. Heartbleed (CVE-2014-0160) — the OpenSSL vulnerability that caused web servers to leak TLS certificates and session cookies — was reproducible through fuzzing with the right driver and ASan enabled.

**How fuzz engines work**:

A fuzz engine (fuzzer) generates large numbers of candidate inputs and passes them through a fuzz driver to the fuzz target (the code under test). Modern fuzz engines use compiler instrumentation to observe which code paths each input exercises. When an input triggers a new code path, the engine preserves it in a seed corpus and uses it to generate future mutations. This coverage-guided approach is far more effective than "dumb fuzzing" (random bytes from a random number generator), which is unlikely to pass input validation and reach the interesting code.

**Identify fuzz targets**: Search the codebase for:

```bash
# Grep for common fuzz target signatures
Grep pattern: ReadJpeg|ParsePng|DecodeAudio|ParseHttp|ReadXml|ParseJson
Grep pattern: Unmarshal|Deserialize|Decode|ParseProto
Grep pattern: compress|decompress|inflate|deflate
```

Each function that accepts a byte sequence from an external source and interprets it as a structured format is a candidate fuzz target.

**Writing effective fuzz drivers** (libFuzzer/AFL compatible):

The libFuzzer entry point is a single function:

```cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Pass data to the fuzz target. Return 0 always.
    MyLibrary::ParseInput(data, size);
    return 0;
}
```

Avoid these patterns in fuzz drivers — they prevent the fuzzer from running quickly and reproducing crashes:

- **Nondeterministic behavior**: Random number generators, timestamp-dependent logic, thread scheduling dependencies. The fuzzer cannot reproduce crashes if the same input produces different execution paths.
- **Slow operations**: Console logging, disk I/O, network calls. Use a memory-based filesystem or a "fuzzer-friendly" build flag (`-DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION`) to disable slow paths.
- **Intentional crashes**: The fuzzer cannot distinguish an intentional crash from a bug.
- **Integrity checks (CRCs, message digests)**: A fuzzer is unlikely to generate a valid checksum. Skip integrity checks in fuzzer builds, or the fuzzer will never reach the parsing code past the checksum verification.

**Dictionary-based input for structured formats**:

When the fuzz target processes a well-specified format — HTTP, SQL, JSON, XML, a binary protocol — provide a dictionary of keywords from the format's grammar. Without a dictionary, the fuzzer generates inputs that are rejected at the token-recognition stage, never reaching the parsing logic where bugs live:

```
# HTTP dictionary example (http.dict)
"GET "
"POST "
"HTTP/1.1\r\n"
"Content-Length: "
"Transfer-Encoding: chunked"
```

Fuzz engines like Peach Fuzzer can also accept a formal grammar definition of the input format, generating structurally valid inputs that violate specific field relationships — more targeted than a keyword dictionary.

**Seed corpus**: Start with real-world representative inputs. For an image library, use a small JPEG file. For a JSON parser, use a representative JSON document. A single real-world seed can increase code coverage by 10% or more compared to starting from an empty corpus, because the fuzzer begins exploring mutations from valid inputs rather than building structure from scratch. Sources for seed corpora:
- Existing test suite sample files
- OSS-Fuzz and The Fuzzing Project published corpora for common formats
- Hand-curated inputs covering edge cases identified in the code review

**Input splitting for multi-mode targets**: If the fuzz target's behavior depends on a configuration mode, split the input: use the first N bytes to select the mode, and the remaining bytes as the payload. This allows a single driver to explore all modes without the fuzzer having to independently discover the mode-selection encoding.

**Comparing implementations**: When migrating from library A to library B, a fuzz driver can pass the same input to both and report any output difference as a crash. This differential fuzzing approach finds subtle behavioral changes that standard tests miss.

### Step 6 — Set Up Continuous Fuzzing

**WHY**: Fuzzing cannot run to completion — fuzz engines generate inputs indefinitely. A one-time local fuzzing session finds some bugs but misses regressions introduced by later changes. Continuous fuzzing integrates the fuzz engine with the CI/CD build pipeline, so fuzzers automatically run against the latest code, accumulate a growing corpus of interesting inputs, and file bugs when crashes are detected — without manual intervention. OSS-Fuzz found over 1,000 bugs within 5 months of its December 2016 launch and has since found tens of thousands more.

**ClusterFuzz** (open source, Google):
- Manages pools of virtual machines running fuzzing tasks
- Corpus management, crash deduplication, lifecycle management
- Web interface for fuzzer metrics (executions per second, code coverage, crash rate)
- Supports libFuzzer and AFL
- Does not build fuzzers — expects the project to push fuzz driver binaries via a continuous build pipeline

**OSS-Fuzz**:
- Combines ClusterFuzz infrastructure with distributed Google Cloud execution
- Open to open source projects — integration requires writing fuzz drivers and a Dockerfile
- Reports vulnerabilities directly to developers within hours of detecting them
- Projects already integrated benefit from both Google's internal fuzzing tools and external fuzzing tools reviewing the same code

**Integration checklist**:
- [ ] Fuzz driver builds cleanly with ASan + libFuzzer flags
- [ ] Seed corpus committed to repository or uploaded to cloud storage bucket
- [ ] Build pipeline pushes fuzzer binary to ClusterFuzz/OSS-Fuzz bucket on every main branch commit
- [ ] Crash alerts route to the team's bug tracker
- [ ] Saved crash samples are checked into the test suite as unit test cases after fixes, to prevent regression

### Step 7 — Integrate Static Analysis at the Right Depth

**WHY**: Static analysis can detect potential bugs before code is executed — ideally before it is checked in. But different static analysis techniques operate at different depths and costs, and the right tool depends on where in the development cycle it runs. Running a slow, deep analyzer on every keystroke creates friction and developer fatigue; running only a fast linter nightly misses the window when the developer still understands the code they just wrote.

**The depth-vs-cost spectrum**:

| Technique | Depth | Cost | Integration Point | Examples |
|---|---|---|---|---|
| Linters / AST pattern matching | Shallow — syntactic patterns, usage rules | Very fast (~compile time) | IDE, pre-commit hook, every commit | Clang-Tidy (C/C++), Error Prone (Java), GoVet (Go), Pylint (Python) |
| Abstract interpretation (deep static analysis) | Semantic — control flow, data flow, cross-function | Slow (minutes to hours) | Nightly, code review on changed code only | Frama-C (C), Infer (Java/C/Go), AbsInt |
| Formal methods | Proof — mathematically rigorous property verification | Very high up-front cost | Safety-critical paths only; pre-deployment release analysis | TLA+, Coq, specialized domain tools |

Statically verifying any program is an undecidable problem — no algorithm can determine whether an arbitrary program will execute without violating an arbitrary property. All static analyzers therefore make tradeoffs between false positives (warnings about code that is actually safe) and false negatives (missing real bugs). Tool selection and integration point determine which tradeoff is acceptable.

**Linters at the commit loop**:

Linters perform syntactic analysis and AST pattern matching. They run fast (roughly compile time), catch common bug patterns and style violations, and integrate well into IDEs and code review systems. Target a false-positive rate of 10% or lower — developers learn to ignore higher-noise tools.

Key linters by language:
- **C/C++**: Clang-Tidy (custom checks, auto-fix capability), Error Prone-style checks via compiler warnings
- **Java**: Error Prone (type-safe bug patterns, auto-fix; 162 authors had submitted 733 checks as of 2018)
- **Go**: GoVet (suspicious constructs), staticcheck
- **Python**: Pylint, Bandit (security-focused)

Google's Tricorder platform runs ~146 analyzers covering 30+ languages during code review, surfacing results inline in the review diff. The platform measures user-perceived false-positive rate by tracking "Not useful" clicks and disables individual checks that exceed 10% noise. Adopt a similar feedback loop: track which findings developers dismiss and tune the ruleset accordingly.

**Abstract interpretation nightly (deep static analysis)**:

Abstract interpretation tools reason about program semantics — data flow, control flow, heap shape — often across function call boundaries. They can find buffer overflows, null pointer dereferences, division by zero, and dangling pointers that linters miss. The cost is analysis time measured in minutes to hours for large codebases.

Integration pattern:
- Run nightly against the full codebase (not on every commit)
- At code review: run in differential mode — analyze only the changed code, reusing previously computed analysis facts for unchanged code
- Route results to the code author during review, not as blocking CI failures (the analysis takes too long to block a commit)

Tools:
- **Frama-C**: C programs — buffer overflows, segmentation faults, dangling pointers, division by zero
- **Infer**: Java, C, Go — memory and pointer bugs, dangling pointers
- **App Security Improvement (ASI)** program: Google Play Store — performs interprocedural analysis on every Android app upload; had led to over 1 million app fixes as of early 2019

**Formal methods for safety-critical paths**:

Formal methods require specifying system properties in a mathematically rigorous way and then verifying them. The upfront cost is high — engineers must learn specification languages and the approach requires a priori description of system requirements. Reserve formal methods for:
- Safety-critical code where a defect has physical consequences (flight control, medical devices)
- Cryptographic protocol implementations (continuous formal verification of TLS protocols)
- Hardware design (standard practice via EDA vendor tools)

**Developer workflow integration**:

The key principle from Google's experience: surface findings at the moment the developer is most able to act on them — when they are writing or reviewing the code, not days later. A developer who gets a null-pointer warning during a code review can fix it immediately. The same warning in a weekly report competes with other priorities.

Practical integration:
1. Add linters to pre-commit hooks and IDE plugins (zero friction for developers who already run the linter)
2. Surface linter results inline in code review diffs (Tricorder pattern — present findings alongside the changed lines)
3. Run deep analysis (Infer, Frama-C) nightly and route findings to a team dashboard — not as commit blockers
4. For security-critical paths identified in threat modeling, evaluate formal methods on a case-by-case basis

### Step 8 — Produce the Security Testing Strategy Document

**WHY**: A strategy document makes the testing plan explicit, reviewable, and executable by the team. It prevents the common failure mode where each engineer adds tests independently without a shared understanding of which vulnerability classes need coverage or how the testing layers interact.

Produce a document with the following sections:

```
## Security Testing Strategy: [service/codebase name]
**Date**: [date]
**Based on**: secure-code-review findings for [scope], [date]

### Coverage Priorities (from code review findings)
[Priority 1]: [Finding class] → [Testing layer] → [Specific tool/test design]
[Priority 2]: ...

### Unit Testing Plan
- Security boundary tests: [list specific functions/modules and input classes to test]
- Access control invariants: [parameterized test design for role/action matrix]
- Malformed input tests: [entry points and attack payloads to exercise]

### Integration Testing Environment
- Seed data plan: [what synthetic data to create, who creates it]
- Production data locations to remediate: [list any current production data copies]

### Dynamic Analysis (Sanitizers)
- Language: [language]
- Baseline sanitizers: [ASan + UBSan / -race / Valgrind — per language]
- CI/CD integration: [nightly build config, runtime estimate]
- Additional sanitizers for specific findings: [TSan if race conditions found, MSan if uninitialized reads found]

### Fuzz Testing Plan
- Fuzz targets identified: [list: function name, input format, codebase location]
- Fuzz engine: [libFuzzer / AFL / Honggfuzz — or combination]
- Seed corpus sources: [existing test files, OSS-Fuzz corpora, hand-curated]
- Dictionary files needed: [list formats requiring dictionary input]
- Continuous fuzzing: [ClusterFuzz / OSS-Fuzz / periodic local — with rationale]

### Static Analysis Plan
- Commit/PR: [linter(s) and configuration]
- Nightly: [deep analysis tool if applicable]
- Safety-critical paths: [formal methods evaluation — yes/no with rationale]

### Integration Timeline
[Week 1]: [Immediate actions — highest-priority unit tests, linter setup]
[Week 2-3]: [Sanitizer nightly builds, integration test remediation]
[Month 2]: [Fuzz drivers written and integrated, continuous fuzzing started]
[Ongoing]: [OSS-Fuzz / ClusterFuzz monitoring, static analysis tuning]
```

---

## Key Principles

**Testing strategies have different cost-benefit profiles — use all layers.** Unit tests provide fast feedback but cannot find memory corruption or unexpected input combinations. Sanitizers catch memory bugs that unit tests miss. Fuzzing finds edge cases no human would consider. Static analysis catches bugs before execution. Each layer is complementary, not a substitute for the others.

**Fuzz testing is most effective when paired with sanitizers.** A fuzzer that generates inputs without ASan enabled can only detect bugs that cause the program to crash or exit. With ASan, the fuzzer detects invalid memory accesses that would otherwise be silent — allowing it to find vulnerabilities like Heartbleed that don't immediately crash the process.

**Never copy production data to test environments.** Production databases contain sensitive personal information that becomes accessible to all test runners and visible in test logs. Seed test environments with synthetic, non-sensitive data. This also eliminates a major source of test flakiness — the environment always starts from a known clean state.

**Performance cost of sanitizers requires scheduling discipline.** Sanitizer-instrumented binaries run orders of magnitude slower than native builds. Run sanitizer pipelines nightly (not on every commit) to catch bugs without blocking developer velocity. Bugs found nightly are still caught far earlier than bugs found in production.

**Code review findings drive testing priorities.** Security testing should not be designed in isolation. Anti-patterns identified during code review — memory corruption patterns, injection risks, concurrency issues — directly determine which sanitizers to enable, which fuzz targets to prioritize, and which unit tests to write first.

**Static analysis should surface findings when developers can act on them.** Findings surfaced during code review — when the engineer understands the code they just wrote — have high fix rates. Findings in a weekly report compete with other priorities. Integrate linters into the commit loop and code review diff; run deeper analysis nightly and route results to the author.

**Fuzzer crashes become regression tests.** When a fuzzer finds a crash, save the crashing input and add it as a unit test case after fixing the bug. This prevents the same vulnerability from being reintroduced in future refactoring.

---

## Examples

### Example 1 — Fuzz Driver for a JPEG Decoder (C++, libFuzzer + ASan)

**Scenario**: A service processes JPEG images uploaded by users. The decoder library handles arbitrary user input. The secure-code-review found no injection issues, but the library is written in C++ and processes complex binary input — a strong candidate for fuzzing.

**Build configuration** (Bazel `.bazelrc`):
```
build:asan --copt -fsanitize=address --linkopt -fsanitize=address
build:asan --copt -fno-omit-frame-pointer --copt -O1 --copt -g dbg
```

**Fuzz driver** (libFuzzer entry point compatible with Honggfuzz and AFL):
```cpp
#include <cstddef>
#include <cstdint>
#include "jpeg_data_decoder.h"
#include "jpeg_data_reader.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t sz) {
    knusperli::JPEGData jpg;
    knusperli::ReadJpeg(data, sz, knusperli::JPEG_READ_HEADER, &jpg);
    return 0;
}
```

**Running the fuzzer** (5-minute session, empty starting corpus):
```bash
$ mkdir synthetic_corpus
$ ASAN_SYMBOLIZER_PATH=/usr/lib/llvm-6.0/bin/llvm-symbolizer \
  bazel-bin/fuzzer \
  -max_total_time=300 -print_final_stats synthetic_corpus/
```

**Improving coverage**: Add a real JPEG file to the seed corpus. A single representative seed can improve code coverage by 10%+ because the fuzzer begins mutating valid inputs rather than building JPEG structure from scratch.

**Input splitting for multi-mode targets**: If the decoder has multiple read modes (header-only, tables, full), use the first 64 bytes of input to select the mode rather than hardcoding one mode per driver — a single driver then exercises all code paths.

### Example 2 — Sanitizer Nightly Build Integration

**Scenario**: A Go gRPC service processes concurrent requests. ThreadSanitizer was not previously enabled. The secure-code-review identified shared state accessed by multiple goroutines.

**CI configuration** (GitHub Actions nightly):
```yaml
nightly-sanitizer:
  schedule:
    - cron: '0 2 * * *'
  steps:
    - name: Build and test with race detector
      run: go test -race ./...
    - name: Run integration tests with race detector
      run: go test -race -tags=integration ./...
```

**What TSan catches that tests miss**: A race condition where two goroutines concurrently read and write a shared token store without synchronization. The race is timing-dependent — unit tests pass 99% of the time. TSan instruments the binary to detect the unsynchronized access deterministically, regardless of thread scheduling.

### Example 3 — Static Analysis Integration at Code Review

**Scenario**: A Java service performs string comparisons incorrectly. Error Prone is integrated into the Bazel build.

**Error Prone detection** (compile-time, no runtime overhead):
```java
// Buggy code — Error Prone catches this at build time:
public boolean foo() {
    return getString() == "foo";  // reference equality, not value equality
}
```

**Error Prone output during build** (surfaces in code review diff):
```
ERROR: String comparison using reference equality instead of value equality
  return getString() == "foo";
         ^
[StringEquality] see http://errorprone.info/bugpattern/StringEquality
Suggested fix: return getString().equals("foo");
```

The developer sees the finding inline in their code review and can apply the one-click fix. This is faster and more reliable than a weekly static analysis report.

---

## References

- [sanitizer-configuration-guide.md](../../references/sanitizer-configuration-guide.md) — ASan, TSan, MSan, UBSan, LSan: compiler flags, Bazel/CMake integration, shadow memory mechanics, performance overhead tables, "known safe" annotation governance
- [fuzz-driver-patterns.md](../../references/fuzz-driver-patterns.md) — libFuzzer/AFL/Honggfuzz entry points, seed corpus curation, dictionary format, FuzzedDataProvider for input splitting, fuzzer-friendly build flags, differential fuzzing pattern
- [continuous-fuzzing-setup.md](../../references/continuous-fuzzing-setup.md) — ClusterFuzz and OSS-Fuzz integration: Dockerfile requirements, build pipeline configuration, corpus management, crash deduplication, bug tracker routing
- [static-analysis-depth-spectrum.md](../../references/static-analysis-depth-spectrum.md) — Full depth-vs-cost spectrum: linters (Clang-Tidy, Error Prone, GoVet, Pylint) → abstract interpretation (Frama-C, Infer, ASI) → formal methods. Developer workflow integration patterns from Google Tricorder.

Cross-references:
- `secure-code-review` — findings from code review drive the testing priorities in Step 1; anti-patterns found there determine which sanitizers and fuzz targets are highest value
- `secure-deployment-pipeline` — testing strategy outputs (sanitizer builds, fuzz driver binaries) integrate with the deployment pipeline

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-secure-code-review`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
