# SRS: TinyDB Search Limit (v1)

## 1. Purpose and scope

- S-01: `db.search(cond)` always returns every match. [Stated in issue body]
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. [Stated in issue body]
- S-03: Could `search` take an optional `limit`? [Stated in issue body]
- S-04: `db.search(Query().category == 'book', limit=10)` -> first 10 matches only. [Stated in issue body]
- S-05: `db.search(Query().category == 'book')` -> unchanged: all matches. [Stated in issue body]
- S-06: `limit=None` (default) keeps today's behavior - all matches, in document id order. [Stated in issue body]
- S-07: `limit=N` returns at most the first N matches, in document id order. [Stated in issue body]
- S-08: A limit larger than the number of matches just returns all matches. [Stated in issue body]

## 2. Actors

| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Client application using TinyDB | STATED | S-02 |

## 3. Constraints

| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The search method must accept an optional `limit` parameter. | STATED | S-03, S-06 | READY |

## 4. Functional requirements

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The search method shall accept an optional `limit` parameter defaulting to `None`. | STATED | S-03, S-06 | MUST | READY | AC-001-1 |
| FR-002 | When `limit` is `None`, search shall return all matching documents in document id order. | STATED | S-06 | MUST | READY | AC-002-1 |
| FR-003 | When `limit` is set to an integer `N`, search shall return at most the first `N` matching documents in document id order. | STATED | S-07 | MUST | READY | AC-003-1 |
| FR-004 | When `limit` is larger than the total number of matches, search shall return all matching documents without error. | STATED | S-08 | MUST | READY | AC-004-1 |

## 5. Non-functional reqs

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | The search method with a limit should avoid materializing/evaluating all matching documents beyond the specified limit where possible for efficiency. | ASSUMED | S-02 | SHOULD | CLARIFY | AC-005-1 |

## 6. Acceptance criteria

| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a Table instance, when calling `search` with no `limit` argument, then it executes successfully using `limit=None`. |
| AC-002-1 | FR-002 | Given a table with multiple matching documents, when calling `search(cond, limit=None)`, then all matching documents are returned in ascending document id order. |
| AC-003-1 | FR-003 | Given a table with matching documents exceeding N, when calling `search(cond, limit=N)` where N is a positive integer, then at most N matching documents are returned in ascending document id order. |
| AC-004-1 | FR-004 | Given a table with fewer than N matching documents, when calling `search(cond, limit=N)`, then all matching documents are returned. |
| AC-005-1 | NFR-001 | Given a table with N matches and a query, when `limit=k` (where k < N) is specified, then the returned list length is exactly k. |

## 7. Dependencies and risks

| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Negative or non-integer limit values passed by callers might cause unexpected slicing behavior if not explicitly handled or validated. | ASSUMED | Q-1 |

## 8. Traceability

- S-01 -> FR-002
- S-02 -> NFR-001
- S-03 -> FR-001, CON-1
- S-04 -> FR-003, AC-003-1
- S-05 -> FR-002
- S-06 -> FR-001, FR-002
- S-07 -> FR-003
- S-08 -> FR-004
