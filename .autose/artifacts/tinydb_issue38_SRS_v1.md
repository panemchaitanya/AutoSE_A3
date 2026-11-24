# SRS: TinyDB db.get() Default Value Support (v1)

## 1. Purpose and scope
- S-01: db.get(...) returns None when nothing matches.
- S-02: db.get(doc_id=some_id) or {} is easy to forget and also wrong for any falsy document content edge cases I might hit later.
- S-03: It would be cleaner if get accepted a default, the way dict.get does.
- S-04: db.get(doc_id=42, default={})
- S-05: db.get(Query().name == 'x', default={})
- S-06: Behavior when the call does match should be exactly what it is today, and omitting default should keep returning None.
- S-07: Ideally this works for all the ways of calling get: by condition, by doc_id, and by doc_ids (for doc_ids, the default would apply to the list result only in the sense that today's empty-list behavior is already fine - no change needed there; the default matters for the single-document calls).

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Client Code | STATED | S-02, S-03, S-04, S-05, S-06, S-07 |
| ACT-2 | TinyDB Database and Table get interface | STATED | S-01, S-03, S-06, S-07 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Behavior when the call matches an existing document must remain exactly what it is today. | STATED | S-06 | READY |
| CON-2 | Omitting default parameter must keep returning None when no match is found. | STATED | S-06 | READY |
| CON-3 | For doc_ids multi-document calls, existing empty-list return behavior is preserved. | STATED | S-07 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The database and table get method shall accept an optional default keyword argument. | STATED | S-03, S-04, S-05, S-07 | UNSET | CLARIFY | AC-001-1, AC-001-2 |
| FR-002 | When get is invoked with a query or doc_id and no matching document is found, it shall return the specified default value instead of None. | STATED | S-03, S-04, S-05 | UNSET | CLARIFY | AC-002-1, AC-002-2 |
| FR-003 | When get is invoked with a query or doc_id and a matching document is found, it shall return the matched document data. | STATED | S-06 | UNSET | CLARIFY | AC-003-1 |
| FR-004 | When get is invoked without the default keyword argument and no matching document is found, it shall return None. | STATED | S-06 | UNSET | CLARIFY | AC-004-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | The get method invocation signature shall maintain backwards compatibility with existing positional and keyword arguments. | STATED | S-06 | UNSET | CLARIFY | AC-NFR1-1 |

## 6. Acceptance criteria
- AC-001-1 | FR-001 | Given a TinyDB database instance db, When db.get(doc_id=42, default={}) is called, Then the method accepts default={} without raising a TypeError.
- AC-001-2 | FR-001 | Given a TinyDB database instance db, When db.get(Query().name == 'x', default=[]) is called, Then the method accepts default=[] without raising a TypeError.
- AC-002-1 | FR-002 | Given a TinyDB table with no matching document for doc_id 999, When db.get(doc_id=999, default="missing") is executed, Then the return value equals "missing".
- AC-002-2 | FR-002 | Given a TinyDB table with no matching document for Query().name == 'nonexistent', When db.get(Query().name == 'nonexistent', default={}) is executed, Then the return value equals {}.
- AC-003-1 | FR-003 | Given a TinyDB table containing document id 42 with data {"name": "test"}, When db.get(doc_id=42, default={}) is executed, Then the return value equals {"name": "test"}.
- AC-004-1 | FR-004 | Given a TinyDB table with no matching document for doc_id 999, When db.get(doc_id=999) is executed, Then the return value is None.
- AC-NFR1-1 | NFR-001 | Given existing code calling db.get(doc_id=42) without default, When executed, Then it functions identically to current behavior.

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | TinyDB table.get and database.get internal implementation structure. | EVIDENCED | tinydb/database.py, tinydb/table.py |
| RSK-1 | Signature changes might affect subclasses or wrapping proxies overriding get(). | INFERRED | S-03, S-07 |

## 8. Traceability
| Source ID | Requirement IDs |
|---|---|
| S-01 | FR-002, FR-004 |
| S-02 | FR-001 |
| S-03 | FR-001, FR-002 |
| S-04 | FR-001, FR-002, AC-001-1 |
| S-05 | FR-001, FR-002, AC-001-2 |
| S-06 | CON-1, CON-2, FR-003, FR-004, NFR-001 |
| S-07 | CON-3, FR-001 |
