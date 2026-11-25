# Register: tinydb-issue-39 (v1)

## A. Source statements
- S-01: "Sometimes a search returns documents with values that are NOT what's stored."
- S-02: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-03: "It's like tinydb remembers my display edits."
- S-04: "If I restart the script the data is fine again, so the file itself is OK."
- S-05: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-06: "Is this a caching bug? Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## B. Ambiguous terms
| ID | Term | Candidate meanings | Decision force |
|---|---|---|---|
| AMB-1 | "normal dicts you can safely edit without side effects" | 1. Deep copies returned on search so mutations don't affect cache/storage. 2. Immutable wrappers. | Determines whether search returns deep-copied standard dictionaries or wrappers. |

## C. Open questions
| ID | Question | Why it matters | Blocks which ids | Score | Default if unanswered | Owner | Status |
|---|---|---|---|---|---|---|---|
| Q-1 | What is the acceptable performance threshold for deep copying search results? | NFR measurement | NFR-001 | 1 | No strict latency limit; correctness takes precedence | Stakeholder | OPEN |

## D. Assumptions
| ID | Statement | Linked Q-id |
|---|---|---|---
| ASM-1 | Performance overhead of deepcopy on search results is negligible for typical TinyDB usage or acceptable relative to correctness. | Q-1 |

## E. Conflicts
None.

## F. Evidence log
| ID | Tool | Input | Result excerpt | Effect on spec |
|---|---|---|---|---|
| EV-1 | A3 repository-local analysis | tinydb/table.py search method (lines 249-297) | Caches query results and returns cached document references directly or via list slicing (`cached_results[:]`), where individual document dict objects are shared with the cache. | Confirmed root cause: query cache stores and returns shared references to Document instances. |

## G. Coverage matrix
- Users and roles: COVERED (ACT-1, ACT-2)
- Core capabilities: COVERED (FR-001, FR-002)
- Data: COVERED (CON-1)
- Integrations: N/A (in-memory/file database)
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: OPEN (NFR-001, Q-1)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: COVERED
- Maintainability and extensibility: COVERED
- Autonomy and human oversight: N/A
- Success measures: COVERED
- Scope exclusions: N/A
- Delivery constraints: N/A

## H. Change log
- v1: Initial specification generated from GitHub issue #39.
