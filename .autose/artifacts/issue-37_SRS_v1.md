# SRS: TinyDB limit parameter in search() (v1)

## 1. Purpose and scope
[S-01] `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
[S-02] Could `search` take an optional `limit`?
[S-03] `db.search(Query().category == 'book', limit=10)   # first 10 matches only`
[S-04] `db.search(Query().category == 'book')             # unchanged: all matches`
[S-05] `limit=None` (default) keeps today's behavior - all matches, in document id order.
[S-06] `limit=N` returns at most the first N matches, in document id order.
[S-07] A limit larger than the number of matches just returns all matches.

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Client Code | STATED | S-01, S-02 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | `search()` method must accept an optional `limit` parameter | STATED | S-02, S-03, S-04 | READY |
| CON-2 | Default value for `limit` must be `None` | STATED | S-05 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The database search function shall accept an optional `limit` parameter defaulting to `None`. | STATED | S-02, S-05 | UNSET | READY | AC-001-1, AC-001-2 |
| FR-002 | The database search function shall return all matching documents in document ID order when `limit` is `None`. | STATED | S-05 | UNSET | READY | AC-002-1 |
| FR-003 | The database search function shall return at most the first N matching documents in document ID order when `limit` is set to an integer N. | STATED | S-06 | UNSET | READY | AC-003-1, AC-003-2 |
| FR-004 | The database search function shall return all matching documents in document ID order when `limit` is greater than the total number of matches. | STATED | S-07 | UNSET | READY | AC-004-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Searching with a limit of N should avoid materializing/processing all subsequent matches once N matches are found when possible. | INFERRED | S-01 | UNSET | READY | AC-005-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a table with documents, When `db.search(cond)` is called without `limit`, Then it executes successfully. |
| AC-001-2 | FR-001 | Given a table with documents, When `db.search(cond, limit=10)` is called, Then it executes successfully. |
| AC-002-1 | FR-002 | Given a query matching 5 documents in a table, When `db.search(cond, limit=None)` is called, Then all 5 matching documents are returned in document ID order. |
| AC-003-1 | FR-003 | Given a query matching 5 documents in a table, When `db.search(cond, limit=2)` is called, Then exactly the first 2 matching documents are returned in document ID order. |
| AC-003-2 | FR-003 | Given a table where no documents match the query, When `db.search(cond, limit=5)` is called, Then an empty list is returned. |
| AC-004-1 | FR-004 | Given a query matching 3 documents in a table, When `db.search(cond, limit=10)` is called, Then all 3 matching documents are returned in document ID order. |
| AC-005-1 | NFR-001 | Given a table with 10,000 matching documents, When `db.search(cond, limit=1)` is executed, Then the execution time is measurably less than executing `db.search(cond)` without limit. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Performance improvement assumes search iteration can terminate early or limit slice is applied efficiently. | INFERRED | S-01 |

## 8. Traceability
| Source / Evidence ID | Requirement IDs |
|---|---|
| S-01 | FR-001, NFR-001, RSK-1 |
| S-02 | CON-1, FR-001 |
| S-03 | CON-1 |
| S-04 | CON-1 |
| S-05 | CON-2, FR-001, FR-002 |
| S-06 | FR-003 |
| S-07 | FR-004 |
