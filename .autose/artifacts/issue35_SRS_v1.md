# SRS: issue35 (v1)

## 1. Purpose and scope

- S-01: "update() and remove() silently do nothing when I pass the doc id as a string"
- S-02: "db.get(doc_id='1') finds my document fine, but when I pass the same id as a string to update or remove, nothing happens. No error, no warning, the document is just unchanged."
- S-03: "Passing the int 1 instead of '1' works."
- S-04: "My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds."
- S-05: "Please make these consistent with get (which accepts the string form)."

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / API Client | STATED | S-02, S-04, S-05 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | TinyDB 4.9.0 and Python 3.12 environment compatibility | STATED | Issue Body | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The table update method shall coerce or match string document IDs equivalent to integer keys when updating documents. | STATED | S-02, S-05 | MUST | READY | AC-001-1 |
| FR-002 | The table remove method shall coerce or match string document IDs equivalent to integer keys when removing documents. | STATED | S-02, S-05 | MUST | READY | AC-002-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | The update and remove methods shall not raise an unhandled exception on string document IDs that represent valid integer IDs. | STATED | S-04 | MUST | READY | AC-001-1, AC-002-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a database with a document inserted, when db.update({'x': 2}, doc_ids=['1']) is called with string doc_id, then the document is updated successfully and the return list contains the updated doc id. |
| AC-002-1 | FR-002 | Given a database with a document inserted, when db.remove(doc_ids=['1']) is called with string doc_id, then the document is removed successfully and the return list contains the removed doc id. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Inconsistent ID handling between get() and write operations (update/remove) causes silent data update failures for users passing web form or string identifiers. | STATED | S-02, S-04 |

## 8. Traceability
- S-01 -> FR-001, FR-002
- S-02 -> FR-001, FR-002, RSK-1
- S-03 -> FR-001, FR-002
- S-04 -> NFR-001, RSK-1
- S-05 -> FR-001, FR-002
- FR-001 -> S-01, S-02, S-05, AC-001-1
- FR-002 -> S-01, S-02, S-05, AC-002-1
- NFR-001 -> S-04, AC-001-1, AC-002-1
- CON-1 -> Issue Body
- RSK-1 -> S-02, S-04
