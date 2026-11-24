# SRS: tinydb (v1)
## 1. Purpose and scope
Add a `limit` parameter to the `search()` method of TinyDB tables to improve performance and usability when only a subset of matching documents is needed (S-01, S-02).

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer | STATED | S-02 |
| ACT-2 | TinyDB Table | INFERRED | S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Maintain backward compatibility for `search(cond)` | STATED | S-05 | READY |
| CON-2 | Results must be in document ID order | STATED | S-05, S-06 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-1 | The `search` method shall accept an optional `limit` parameter | STATED | S-03 | MUST | READY | AC-1-1 |
| FR-2 | If `limit` is `None`, the system shall return all matches | STATED | S-05 | MUST | READY | AC-2-1 |
| FR-3 | If `limit` is an integer `N`, the system shall return at most the first `N` matches | STATED | S-06 | MUST | READY | AC-3-1 |
| FR-4 | If `limit` is larger than the number of matches, the system shall return all matches | STATED | S-07 | MUST | READY | AC-4-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-1 | Avoid materializing the full result list when a limit is applied | STATED | S-02 | SHOULD | READY | AC-5-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-1-1 | FR-1 | Given a Table instance, when `search` is called with `limit=10`, then the call succeeds without error. |
| AC-2-1 | FR-2 | Given a table with 5 matches, when `search(cond, limit=None)` is called, then 5 documents are returned. |
| AC-3-1 | FR-3 | Given a table with 100 matches, when `search(cond, limit=5)` is called, then exactly 5 documents are returned in document ID order. |
| AC-4-1 | FR-4 | Given a table with 3 matches, when `search(cond, limit=10)` is called, then exactly 3 documents are returned. |
| AC-5-1 | NFR-1 | Given a table with 10,000 matches, when `search(cond, limit=1)` is called, the execution time is less than a full search (measurable via benchmark). |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Cache interaction: limited results might be cached incorrectly if the cache key doesn't include the limit | INFERRED | S-03, tinydb/table.py:265 |

## 8. Traceability
S-01 -> FR-1
S-02 -> NFR-1
S-03 -> FR-1
S-05 -> FR-2, CON-1
S-06 -> FR-3, CON-2
S-07 -> FR-4