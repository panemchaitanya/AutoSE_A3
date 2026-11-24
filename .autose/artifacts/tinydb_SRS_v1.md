# SRS: TinyDB Missing Field Operations (v1)

## 1. Purpose and scope
- S-01: "I'm using `tinydb.operations.increment` for a page-view counter. The first time a page is viewed the document has no `count` field yet, and instead of just starting the counter at 1, TinyDB blows up: KeyError: 'count'"
- S-02: "I would expect a counter on a missing field to simply start from 0, i.e. after the call above the document should be `{'page': '/home', 'count': 1}`."
- S-03: "Same goes for `add` and `subtract`: adding 5 to a missing field should give 5, subtracting 3 should give -3."
- S-04: "Right now I have to defensively insert `count: 0` everywhere, which defeats the point."

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | TinyDB User / Developer | STATED | S-01, S-04 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Target Python environment is Python 3.12 with TinyDB 4.9.0 | STATED | S-04 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The increment operation shall initialize a missing field to 0 before incrementing by 1. | STATED | S-01, S-02 | MUST | READY | AC-001-1 |
| FR-002 | The decrement operation shall initialize a missing field to 0 before decrementing by 1. | INFERRED | S-02, S-03 | MUST | READY | AC-002-1 |
| FR-003 | The add operation shall initialize a missing field to 0 before adding the specified value `n`. | STATED | S-03 | MUST | READY | AC-003-1 |
| FR-004 | The subtract operation shall initialize a missing field to 0 before subtracting the specified value `n`. | STATED | S-03 | MUST | READY | AC-004-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Operations on existing fields must retain their current performance without regression. | ASSUMED | Q-1 | SHOULD | CLARIFY | AC-NFR1-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a document without the field 'count', When update(increment('count')) is executed, Then the document shall have 'count' set to 1. |
| AC-002-1 | FR-002 | Given a document without the field 'count', When update(decrement('count')) is executed, Then the document shall have 'count' set to -1. |
| AC-003-1 | FR-003 | Given a document without the field 'score', When update(add('score', 5)) is executed, Then the document shall have 'score' set to 5. |
| AC-004-1 | FR-004 | Given a document without the field 'score', When update(subtract('score', 3)) is executed, Then the document shall have 'score' set to -3. |
| AC-NFR1-1 | NFR-001 | Given existing integration test suite execution, When running benchmarks before and after, Then execution time overhead shall be less than 5 percent. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Changing missing field behavior could break existing client workarounds that rely on KeyError or expect missing fields to remain absent. | ASSUMED | S-04 |

## 8. Traceability
| Source / Evidence ID | Requirement IDs |
|---|---|
| S-01 | FR-001 |
| S-02 | FR-001, FR-002 |
| S-03 | FR-003, FR-004 |
| S-04 | FR-001, CON-1, RSK-1 |
