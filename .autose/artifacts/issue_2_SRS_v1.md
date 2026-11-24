# SRS: TinyDB String Document ID Support for Update and Remove (v1)

## 1. Purpose and scope
- S-01: "I spent an hour debugging this. `db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged."
- S-02: "Passing the int `1` instead of `'1'` works. My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds."
- S-03: "Please make these consistent with `get` (which accepts the string form)."

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | TinyDB User / Application Developer | STATED | S-01, S-02, S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Compatible with TinyDB 4.9.0 and Python 3.12 | STATED | Issue description | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The `Table.update()` method shall accept document IDs passed as string representations of integers (e.g. `'1'`) and successfully update the matching document(s), behaving consistently with `Table.get()`. | STATED | S-01, S-03 | MUST | READY | AC-001-1 |
| FR-002 | The `Table.remove()` method shall accept document IDs passed as string representations of integers (e.g. `'1'`) and successfully remove the matching document(s), behaving consistently with `Table.get()`. | STATED | S-01, S-03 | MUST | READY | AC-002-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Operations utilizing string-form document IDs shall not silently no-op when a corresponding integer ID document exists. | STATED | S-01, S-02 | MUST | READY | AC-001-1, AC-002-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|----|
| AC-001-1 | FR-001 | Given a database containing a document with integer ID 1, when `db.update({'x': 2}, doc_ids=['1'])` is executed, then the document with ID 1 is updated to `{'x': 2}` and the list of updated document IDs `[1]` is returned. |
| AC-002-1 | FR-002 | Given a database containing a document with integer ID 1, when `db.remove(doc_ids=['1'])` is executed, then the document with ID 1 is removed and the list of removed document IDs `[1]` is returned. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | Depends on TinyDB internal table query/doc_ids coercion mechanisms. | INFERRED | Codebase structure |

## 8. Traceability
| Source ID | Requirement ID(s) |
|---|---|
| S-01 | FR-001, FR-002, NFR-001 |
| S-02 | NFR-001 |
| S-03 | FR-001, FR-002 |
