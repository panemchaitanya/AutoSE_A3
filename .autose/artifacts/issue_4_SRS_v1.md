# SRS: Add a limit parameter to search() (v1)

## 1. Purpose and scope
- S-1: `db.search(cond)` always returns every match.
- S-2: When a table has thousands of documents and I only need the first few, I have to materialize the whole result list and slice it myself, which is wasteful.
- S-3: Could `search` take an optional `limit`?
- S-4: `limit=None` (default) keeps today's behavior - all matches, in document id order.
- S-5: `limit=N` returns at most the first N matches, in document id order.
- S-6: A limit larger than the number of matches just returns all matches.

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Client code | STATED | Issue #4 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Must maintain backwards compatibility with existing `search()` calls without `limit`. | STATED | S-4 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-1 | The table search method and database search method shall accept an optional keyword parameter `limit`. | STATED | S-3, S-4 | MUST | READY | AC-1, AC-2, AC-3 |
| FR-2 | When `limit` is `None`, search shall return all matching documents in document ID order. | STATED | S-4 | MUST | READY | AC-2 |
| FR-3 | When `limit` is an integer `N`, search shall return at most the first `N` matching documents in document ID order. | STATED | S-5 | MUST | READY | AC-1 |
| FR-4 | When `limit` is an integer larger than the total number of matching documents, search shall return all matching documents. | STATED | S-6 | MUST | READY | AC-3 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-1 | Searching with `limit=N` shall avoid materializing or evaluating documents beyond the limit where possible to improve efficiency. | INFERRED | S-2 | SHOULD | READY | AC-4 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-1-1 | FR-3 | Given a table containing multiple matching documents, When `db.search(cond, limit=2)` is invoked, Then exactly the first 2 matching documents in document ID order are returned. |
| AC-2-1 | FR-2 | Given a table containing matching documents, When `db.search(cond, limit=None)` or `db.search(cond)` is invoked, Then all matching documents in document ID order are returned. |
| AC-3-1 | FR-4 | Given a table containing fewer matching documents than the specified limit, When `db.search(cond, limit=100)` is invoked, Then all available matching documents are returned without error. |
| AC-4-1 | NFR-1 | Given a large table, When `db.search(cond, limit=10)` is invoked, Then internal iteration halts or avoids fetching unnecessary trailing documents. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | Depends on Table.search implementation. | STATED | S-3 |

## 8. Traceability
- S-1 -> FR-2
- S-2 -> NFR-1
- S-3 -> FR-1
- S-4 -> FR-2
- S-5 -> FR-3
- S-6 -> FR-4
