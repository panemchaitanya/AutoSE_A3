# SRS: TinyDB search limit parameter (v2)

## 1. Purpose and scope
- S-01: db.search(cond) always returns every match. [Stated, Issue Body]
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. [Stated, Issue Body]
- S-03: Could search take an optional limit? [Stated, Issue Body]
- S-04: db.search(Query().category == 'book', limit=10) # first 10 matches only [Stated, Issue Body]
- S-05: db.search(Query().category == 'book') # unchanged: all matches [Stated, Issue Body]
- S-06: limit=None (default) keeps today's behavior - all matches, in document id order. [Stated, Issue Body]
- S-07: limit=N returns at most the first N matches, in document id order. [Stated, Issue Body]
- S-08: A limit larger than the number of matches just returns all matches. [Stated, Issue Body]

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Python API Consumer | STATED | S-02 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The search method must accept an optional limit parameter defaulting to None. | STATED | S-03, S-06 | CLARIFY |
| CON-2 | Results must be returned in document id order. | STATED | S-06, S-07 | CLARIFY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The Table.search method shall accept an optional limit parameter defaulting to None. | STATED | S-03, S-06 | UNSET | CLARIFY | AC-001-1, AC-001-2 |
| FR-002 | When limit is None, Table.search shall return all matching documents in document id order. | STATED | S-05, S-06 | UNSET | CLARIFY | AC-002-1 |
| FR-003 | When limit is an integer N (where N >= 0), Table.search shall return at most the first N matching documents in document id order. | STATED | S-04, S-07 | UNSET | CLARIFY | AC-003-1, AC-003-2 |
| FR-004 | When limit is larger than the total number of matching documents, Table.search shall return all matching documents. | STATED | S-08 | UNSET | CLARIFY | AC-004-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a table search method signature, When inspecting arguments, Then an optional limit parameter is accepted and defaults to None. |
| AC-001-2 | FR-001 | Given a call to db.search(cond, limit=5), When executed, Then the limit keyword argument is successfully accepted without error. |
| AC-002-1 | FR-002 | Given a table with matching documents, When calling table.search(cond) without limit, Then all matching documents are returned in document id order. |
| AC-003-1 | FR-003 | Given a table with 20 matching documents, When calling table.search(cond, limit=10), Then exactly the first 10 matching documents in document id order are returned. |
| AC-003-2 | FR-003 | Given a table with matching documents, When calling table.search(cond, limit=0), Then an empty list of documents is returned. |
| AC-004-1 | FR-004 | Given a table with 3 matching documents, When calling table.search(cond, limit=10), Then all 3 matching documents are returned. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Negative integer passed as limit might cause unexpected slice behavior unless explicitly handled or constrained. | INFERRED | S-07 |

## 8. Traceability
| Source ID | Requirement / Item ID |
|---|---|
| S-01 | FR-002 |
| S-02 | ACT-1 |
| S-03 | CON-1, FR-001 |
| S-04 | FR-003, AC-003-1 |
| S-05 | FR-002 |
| S-06 | CON-1, CON-2, FR-002 |
| S-07 | CON-2, FR-003, RSK-1 |
| S-08 | FR-004 |
