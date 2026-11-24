# SRS: tinydb_search_limit (v1)

## 1. Purpose and scope
Add an optional `limit` parameter to `Table.search()` and `TinyDB.search()` so callers can retrieve at most N matching documents in document ID order instead of materializing all matches. (S-01, S-03, S-06, S-07)

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Library Caller | INFERRED | S-01, S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Backward compatibility: existing calls to `search(cond)` without `limit` must remain unchanged. | STATED | S-05, S-06 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The `Table.search` method shall accept an optional `limit` parameter with default value `None`. | STATED | S-03, S-06 | MUST | READY | AC-001-1 |
| FR-002 | When `search` is called with `limit=None` or without `limit`, the system shall return all matching documents in document ID order. | STATED | S-05, S-06 | MUST | READY | AC-002-1 |
| FR-003 | When `search` is called with `limit=N` where N is a non-negative integer, the system shall return at most the first N matching documents in document ID order. | STATED | S-04, S-07 | MUST | READY | AC-003-1 |
| FR-004 | When `search` is called with `limit=N` where N exceeds the count of matching documents, the system shall return all matching documents in document ID order. | STATED | S-08 | MUST | READY | AC-004-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | The search operation with limit parameter shall preserve document ID ordering guarantees of TinyDB queries. | STATED | S-06, S-07 | MUST | READY | AC-005-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a Table instance, when inspecting signature of `search`, then `limit` parameter exists and defaults to `None`. |
| AC-002-1 | FR-002 | Given a table with 5 matching documents, when calling `db.search(cond)` or `db.search(cond, limit=None)`, then a list of all 5 matching documents in ascending document ID order is returned. |
| AC-003-1 | FR-003 | Given a table with 10 matching documents with IDs 1..10, when calling `db.search(cond, limit=3)`, then a list of exactly the first 3 matching documents (IDs 1, 2, 3) is returned. |
| AC-004-1 | FR-004 | Given a table with 3 matching documents, when calling `db.search(cond, limit=10)`, then a list of all 3 matching documents is returned. |
| AC-005-1 | NFR-001 | Given a table with multiple matching documents, when calling `db.search(cond, limit=N)`, then the returned documents match the first N items of `db.search(cond)`. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | `Table.search` implementation in `tinydb/table.py` and forwarder in `tinydb/database.py`. | EVIDENCED | EV-1 |
| RSK-1 | Cached query results might interact with sliced results if cache stores limited results under the same key. | INFERRED | EV-1 |

## 8. Traceability
| Source ID | Requirement IDs |
|---|---|
| S-01 | FR-001 |
| S-02 | FR-001 |
| S-03 | FR-001 |
| S-04 | FR-003 |
| S-05 | FR-002 |
| S-06 | CON-1, FR-001, FR-002, NFR-001 |
| S-07 | FR-003, NFR-001 |
| S-08 | FR-004 |
| EV-1 | DEP-1, RSK-1 |
