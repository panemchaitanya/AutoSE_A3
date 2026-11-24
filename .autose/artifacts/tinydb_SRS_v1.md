# SRS: TinyDB limit parameter in search (v1)

## 1. Purpose and scope

- S-01: "`db.search(cond)` always returns every match."
- S-02: "When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful."
- S-03: "Could `search` take an optional `limit`?"
- S-04: "`db.search(Query().category == 'book', limit=10)` # first 10 matches only"
- S-05: "`db.search(Query().category == 'book')` # unchanged: all matches"
- S-06: "`- limit=None` (default) keeps today's behavior - all matches, in document id order."
- S-07: "`- limit=N` returns at most the first N matches, in document id order."
- S-08: "`- A limit larger than the number of matches just returns all matches."

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Client code calling `db.search()` or `table.search()` | STATED | S-02 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The search method signature and behavior must remain backwards compatible (default `limit=None`). | STATED | S-05, S-06 | READY |
| CON-2 | Matches must be returned in document id order. | STATED | S-06, S-07 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The database search and table search methods shall accept an optional `limit` parameter defaulting to `None`. | STATED | S-03, S-06 | UNSET | READY | AC-001-1 |
| FR-002 | When `limit` is `None`, search shall return all matching documents in document id order. | STATED | S-06 | UNSET | READY | AC-002-1 |
| FR-003 | When `limit` is set to an integer $N$, search shall return at most the first $N$ matching documents in document id order. | STATED | S-04, S-07 | UNSET | READY | AC-003-1 |
| FR-004 | When `limit` is larger than the total number of matching documents, search shall return all matching documents. | STATED | S-08 | UNSET | READY | AC-004-1 |

## 5. Non-functional reqs
*(None stated)*

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|-
| AC-001-1 | FR-001 | Given a call to `db.search(cond)` without `limit`, When executed, Then it accepts the call without errors and behaves according to default parameters. |
| AC-002-1 | FR-002 | Given a table with documents matching a condition, When `db.search(cond, limit=None)` is called, Then all matching documents are returned in document id order. |
| AC-003-1 | FR-003 | Given a table with multiple matching documents, When `db.search(cond, limit=3)` is called, Then at most the first 3 matching documents are returned in document id order. |
| AC-004-1 | FR-004 | Given a table with 2 matching documents, When `db.search(cond, limit=10)` is called, Then both matching documents are returned. |

## 7. Dependencies and risks
*(None)*

## 8. Traceability
- S-01 -> FR-002
- S-02 -> FR-001
- S-03 -> FR-001
- S-04 -> FR-003
- S-05 -> FR-002
- S-06 -> FR-002, CON-1, CON-2
- S-07 -> FR-003, CON-2
- S-08 -> FR-004
