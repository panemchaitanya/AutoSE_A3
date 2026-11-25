# SRS: TinyDB String Document IDs in Update and Remove (v1)

## 1. Purpose and scope
- S-01: "`db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged."
- S-02: "Passing the int `1` instead of `'1'` works."
- S-03: "My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds."
- S-04: "Please make these consistent with `get` (which accepts the string form)."

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / User | STATED | S-01, S-03 |
| ACT-2 | Web Form Client | STATED | S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | TinyDB version 4.9.0 and Python 3.12 environment | STATED | Issue Body | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The table `update` method shall accept string representations of document IDs in `doc_ids` (or convert/normalize them consistently with `get`) so that update operations succeed when string IDs are passed. | STATED | S-01, S-04 | MUST | READY | AC-001-1, AC-001-2 |
| FR-002 | The table `remove` method shall accept string representations of document IDs in `doc_ids` (or convert/normalize them consistently with `get`) so that remove operations succeed when string IDs are passed. | STATED | S-01, S-04 | MUST | READY | AC-002-1, AC-002-2 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Error handling and type conversion for `doc_ids` in `update` and `remove` shall be consistent with `get`. | STATED | S-04 | MUST | READY | AC-NFR-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a table containing a document inserted with integer ID `1`, When `db.update({'x': 2}, doc_ids=['1'])` is executed, Then the document is successfully updated and the returned list contains the matched ID type/value consistently. |
|---|---|---|
| AC-001-2 | FR-001 | Given a table containing a document inserted with integer ID `1`, When `db.update({'x': 2}, doc_ids=[1])` is executed, Then the document is successfully updated. |
| AC-002-1 | FR-002 | Given a table containing a document inserted with integer ID `1`, When `db.remove(doc_ids=['1'])` is executed, Then the document is successfully removed and the table length becomes 0. |
| AC-002-2 | FR-002 | Given a table containing a document inserted with integer ID `1`, When `db.remove(doc_ids=[1])` is executed, Then the document is successfully removed. |
| AC-NFR-1 | NFR-001 | Given `get`, `update`, and `remove` methods accepting `doc_ids`, When string IDs are supplied across all three methods, Then all three methods handle string ID normalization identically without silent no-ops. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | TinyDB table storage backend (`MemoryStorage` / JSON storage) | STATED | Issue Body |
| RSK-1 | Breaking backward compatibility for callers expecting strict int-only type matching in `doc_ids` if not handled carefully | INFERRED | S-02, S-04 |

## 8. Traceability
| Source / Evidence ID | Requirement / Artifact ID |
|---|---|
| S-01 | FR-001, FR-002, AC-001-1, AC-002-1 |
| S-02 | RSK-1 |
| S-03 | ACT-2, CON-1 |
| S-04 | FR-001, FR-002, NFR-001, AC-NFR-1 |
