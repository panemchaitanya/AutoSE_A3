# SRS: TinyDB Table.get Default Value Support (v1)

## 1. Purpose and scope
This specification defines requirements for adding a `default` parameter to `Table.get` in TinyDB (S-03). When a document query does not match, `Table.get` returns the default value instead of `None` (S-01, S-03).

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Python Developer / Library User | STATED | S-02 |
| ACT-2 | TinyDB Table Instance | STATED | S-01 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | When `default` is omitted, `Table.get` shall return `None` when no document matches. | STATED | S-05 | READY |
| CON-2 | When a document matches, `Table.get` return value shall remain unchanged. | STATED | S-04 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The `Table.get` method shall accept an optional `default` parameter. | STATED | S-03 | MUST | READY | AC-001-1 |
| FR-002 | The `Table.get` method shall return `default` when querying by `doc_id` or condition if no document matches. | STATED | S-03 | MUST | READY | AC-002-1, AC-002-2 |
| FR-003 | The `Table.get` method shall return `None` when querying by `doc_id` or condition if no document matches and `default` is omitted. | STATED | S-01, S-05 | MUST | READY | AC-003-1 |
| FR-004 | The `Table.get` method shall return the matched document when a document matches regardless of whether `default` is specified. | STATED | S-04 | MUST | READY | AC-004-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Function call performance of `Table.get` shall not degrade by more than 5% when `default` parameter is used. | INFERRED | S-04 | SHOULD | READY | AC-NFR-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a `Table` instance, when calling `table.get(doc_id=1, default={})`, then the call executes without TypeError. |
| AC-002-1 | FR-002 | Given a table with no document for `doc_id=42`, when calling `table.get(doc_id=42, default={})`, then the return value is `{}`. |
| AC-002-2 | FR-002 | Given a table with no document matching `Query().name == 'x'`, when calling `table.get(Query().name == 'x', default=[])`, then the return value is `[]`. |
| AC-003-1 | FR-003 | Given a table with no document for `doc_id=42`, when calling `table.get(doc_id=42)`, then the return value is `None`. |
| AC-004-1 | FR-004 | Given a table containing document `{'a': 1}` with `doc_id=1`, when calling `table.get(doc_id=1, default={})`, then the return value is `{'a': 1}`. |
| AC-NFR-1 | NFR-001 | Given 10000 executions of `table.get(doc_id=999, default=None)` vs `table.get(doc_id=999)`, the mean execution duration ratio shall be within 1.05x. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | `Table.get` implementation in `tinydb/table.py`. | EVIDENCED | EV-1 |
| RSK-1 | Falsy document content (e.g. empty dict or boolean false) could be confused with missing result if falsy check is used instead of identity/sentinel check. | STATED | S-02 |

## 8. Traceability
- S-01 -> FR-003, CON-1
- S-02 -> RSK-1
- S-03 -> FR-001, FR-002
- S-04 -> FR-004, CON-2, NFR-001
- S-05 -> FR-003, CON-1
- S-06 -> FR-002
- S-07 -> FR-002
- EV-1 -> DEP-1
