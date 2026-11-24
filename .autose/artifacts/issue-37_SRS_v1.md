# SRS: TinyDB search limit parameter (v1)

## 1. Purpose and scope
- S-01: `db.search(cond)` always returns every match. [Stated: Issue #37 body]
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. [Stated: Issue #37 body]
- S-03: Could `search` take an optional `limit`? [Stated: Issue #37 body]
- S-04: `db.search(Query().category == 'book', limit=10)   # first 10 matches only` [Stated: Issue #37 body]
- S-05: `db.search(Query().category == 'book')             # unchanged: all matches` [Stated: Issue #37 body]
- S-06: `limit=None` (default) keeps today's behavior - all matches, in document id order. [Stated: Issue #37 body]
- S-07: `limit=N` returns at most the first N matches, in document id order. [Stated: Issue #37 body]
- S-08: A limit larger than the number of matches just returns all matches. [Stated: Issue #37 body]

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | TinyDB Database / Table User | STATED | S-02, S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The search method signature and behavior must remain backward compatible when limit is omitted or None. | STATED | S-05, S-06 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The `search()` method on Table (and Database wrapper if applicable) shall accept an optional `limit` parameter defaulting to `None`. | STATED | S-03, S-06 | MUST | READY | AC-001-1, AC-001-2 |
| FR-002 | When `limit` is `None`, `search()` shall return all matching documents in document id order. | STATED | S-06 | MUST | READY | AC-002-1 |
| FR-003 | When `limit` is set to an integer $N ≥ 0$, `search()` shall return at most the first $N$ matching documents in document id order. | STATED | S-07, S-08 | MUST | READY | AC-003-1, AC-003-2, AC-003-3 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Search execution with `limit=N` shall avoid full materialization of results when iterating/evaluating matches if possible, or execute correctly without breaking existing search performance profiles. | INFERRED | S-02 | SHOULD | READY | AC-NFR-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|-
| AC-001-1 | FR-001 | Given a table with documents, when `db.search(cond)` is called without `limit`, then it executes successfully without error. |
| AC-001-2 | FR-001 | Given a table with documents, when `db.search(cond, limit=5)` is called with an integer limit, then it executes successfully without error. |
| AC-002-1 | FR-002 | Given a table containing 15 matching documents, when `db.search(cond, limit=None)` is called, then all 15 matching documents are returned in document id order. |
| AC-003-1 | FR-003 | Given a table containing 15 matching documents, when `db.search(cond, limit=5)` is called, then exactly the first 5 matching documents are returned in document id order. |
| AC-003-2 | FR-003 | Given a table containing 3 matching documents, when `db.search(cond, limit=10)` is called, then all 3 matching documents are returned in document id order. |
| AC-003-3 | FR-003 | Given a table containing matching documents, when `db.search(cond, limit=0)` is called, then an empty list is returned. |
| AC-NFR-1 | NFR-001 | Given a table with 10,000 documents, when `db.search(cond, limit=10)` is executed, then the execution time completes successfully and correctly retrieves at most 10 documents. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Subclassing or custom table implementations overriding `search()` might need signature updates or might ignore `limit` if not updated. | INFERRED | Codebase inspection of `tinydb/table.py` |

## 8. Traceability
- S-01 -> FR-002
- S-02 -> NFR-001
- S-03 -> FR-001
- S-04 -> FR-003, AC-003-1
- S-05 -> CON-1, AC-001-1
- S-06 -> FR-001, FR-002, AC-002-1
- S-07 -> FR-003, AC-003-1
- S-08 -> FR-003, AC-003-2
- FR-001 -> S-03, S-06
- FR-002 -> S-06
- FR-003 -> S-07, S-08
- NFR-001 -> S-02
- CON-1 -> S-05, S-06
- RSK-1 -> Codebase inspection
