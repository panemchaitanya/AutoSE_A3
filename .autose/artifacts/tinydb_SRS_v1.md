# SRS: TinyDB Limit Parameter (v1)

## 1. Purpose and scope
- S-1: `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
- S-2: Could `search` take an optional `limit`?
- S-3: `db.search(Query().category == 'book', limit=10)` # first 10 matches only; `db.search(Query().category == 'book')` # unchanged: all matches.
- S-4: `limit=None` (default) keeps today's behavior - all matches, in document id order.
- S-5: `limit=N` returns at most the first N matches, in document id order.
- S-6: A limit larger than the number of matches just returns all matches.

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer | STATED | S-1 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | None | - | - | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-1 | The `Table.search` method shall accept an optional `limit` parameter of type `Optional[int]`. | STATED | S-2 | UNSET | READY | AC-001-1, AC-002-1, AC-003-1 |
| FR-2 | When `limit` is `None`, `Table.search` shall return all matching documents in document id order. | STATED | S-4 | UNSET | READY | AC-002-1 |
| FR-3 | When `limit` is a non-negative integer `N`, `Table.search` shall return at most the first `N` matching documents in document id order. | STATED | S-5 | UNSET | READY | AC-001-1 |
| FR-4 | When `limit` is larger than the number of matching documents, `Table.search` shall return all matching documents. | STATED | S-6 | UNSET | READY | AC-003-1 |
| FR-5 | The `TinyDB` database class shall forward the `limit` parameter in `search()` calls to the default table. | STATED | S-1, S-3 | UNSET | READY | AC-004-1 |

## 5. Non-functional reqs
None.

## 6. Acceptance criteria
| AC-id | Requirement | Criterion | TINYDB-SPEC-AC |
|---|---|---|---|
| AC-001-1 | FR-1, FR-3 | Given a table with multiple matching documents, When calling `table.search(cond, limit=2)`, Then at most 2 matching documents are returned in document id order. | Measurable threshold |
| AC-002-1 | FR-2 | Given a table with matching documents, When calling `table.search(cond, limit=None)`, Then all matching documents are returned in document id order. | Measurable threshold |
| AC-003-1 | FR-4 | Given a table with matching documents, When calling `table.search(cond, limit=100)` where 100 exceeds match count, Then all matching documents are returned. | Measurable threshold |
| AC-004-1 | FR-5 | Given a database instance `db`, When calling `db.search(cond, limit=5)`, Then at most 5 matching documents from the default table are returned. | Measurable threshold |

## 7. Dependencies and risks
None.

## 8. Traceability
- S-1 -> FR-5
- S-2 -> FR-1
- S-3 -> FR-5
- S-4 -> FR-2
- S-5 -> FR-3
- S-6 -> FR-4
