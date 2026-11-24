# SRS: TinyDB increment/add/subtract missing field handling (v1)

## 1. Purpose and scope
- S-01: "I'm using tinydb.operations.increment for a page-view counter. The first time a page is viewed the document has no count field yet, and instead of just starting the counter at 1, TinyDB blows up: KeyError: 'count'"
- S-02: "I would expect a counter on a missing field to simply start from 0, i.e. after the call above the document should be {'page': '/home', 'count': 1}."
- S-03: "Same goes for add and subtract: adding 5 to a missing field should give 5, subtracting 3 should give -3. Right now I have to defensively insert count: 0 everywhere, which defeats the point."
- S-04: "TinyDB 4.9.0, Python 3.12."

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | TinyDB Database User / Developer | STATED | S-01, S-02, S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Compatible with TinyDB 4.9.0 and Python 3.12 environment | STATED | S-04 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The increment operation shall treat a missing field as having an initial numeric value of 0 when applied to a document, resulting in a value of n (where increment default is 1 or specified amount) | STATED | S-01, S-02, S-03 | MUST | READY | AC-001-1, AC-001-2 |
| FR-002 | The add operation shall treat a missing field as having an initial numeric value of 0 when applied to a document, resulting in the added amount | STATED | S-03 | MUST | READY | AC-002-1 |
| FR-003 | The subtract operation shall treat a missing field as having an initial numeric value of 0 when applied to a document, resulting in the negative of the subtracted amount | STATED | S-03 | MUST | READY | AC-003-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | The operation update execution time for documents with missing fields shall not introduce regressions compared to existing field updates | ASSUMED | Q-1 | UNSET | CLARIFY | AC-NFR-001 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|--|
| AC-001-1 | FR-001 | Given a document without a 'count' field, when db.update(increment('count'), doc_ids=[1]) is executed, then the document shall be updated to include 'count': 1. |
| AC-001-2 | FR-001 | Given a document without a 'count' field, when db.update(increment('count', n=5), doc_ids=[1]) is executed, then the document shall be updated to include 'count': 5. |
| AC-002-1 | FR-002 | Given a document without a 'val' field, when db.update(add('val', 5), doc_ids=[1]) is executed, then the document shall be updated to include 'val': 5. |
| AC-003-1 | FR-003 | Given a document without a 'val' field, when db.update(subtract('val', 3), doc_ids=[1]) is executed, then the document shall be updated to include 'val': -3. |
| AC-NFR-001 | NFR-001 | Given 10,000 update operations on documents lacking the target field, when executed, then execution completes successfully without performance degradation errors. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-001 | Modifying increment/add/subtract behavior on missing fields might affect users relying on KeyError for validation | INFERRED | S-01, S-03 |

## 8. Traceability
| Source ID | Requirement / Item IDs |
|---|---|
| S-01 | FR-001, RSK-001 |
| S-02 | FR-001, AC-001-1 |
| S-03 | FR-001, FR-002, FR-003, AC-001-2, AC-002-1, AC-003-1, RSK-001 |
| S-04 | CON-1 |
