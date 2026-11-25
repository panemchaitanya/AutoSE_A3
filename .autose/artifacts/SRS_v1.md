# SRS: Add default value support to db.get (v1)

## 1. Purpose and scope
This specification defines the addition of a `default` parameter to the `db.get` method, enabling users to return a specified value instead of `None` when no document matches (S-03).

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer | INFERRED | S-01 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The `default` parameter shall not change behavior for `doc_ids` (plural) calls | STATED | S-06 | READY |
| CON-2 | The `default` parameter shall not change behavior for successful matches | STATED | S-05 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-1 | The `db.get` method shall accept an optional `default` parameter | STATED | S-03 | UNSET | READY | AC-1-1 |
| FR-2 | The `db.get` method shall return the `default` value when no document matches | STATED | S-04 | UNSET | READY | AC-2-1 |
| FR-3 | The `db.get` method shall return `None` when no `default` is provided and no match is found | STATED | S-05 | UNSET | READY | AC-3-1 |

## 5. Non-functional reqs
(None)

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-1-1 | FR-1 | Given a `db` instance, when `db.get(doc_id=1, default={})` is called, the method signature accepts the `default` argument. |
| AC-2-1 | FR-2 | Given a `db` instance, when `db.get(doc_id=999, default={'a': 1})` is called and no document exists, the result is `{'a': 1}`. |
| AC-3-1 | FR-3 | Given a `db` instance, when `db.get(doc_id=999)` is called and no document exists, the result is `None`. |

## 7. Dependencies and risks
(None)

## 8. Traceability
| S-id | Requirement ids |
|---|---|
| S-03 | FR-1 |
| S-04 | FR-2 |
| S-05 | FR-3 |
| S-06 | CON-1 |