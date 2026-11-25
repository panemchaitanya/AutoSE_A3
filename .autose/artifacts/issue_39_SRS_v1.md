# SRS: issue_39 (v1)
## 1. Purpose and scope
- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "Example: I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-04: "It's like tinydb remembers my display edits."
- S-05: "If I restart the script the data is fine again, so the file itself is OK."
- S-06: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-07: "Is this a caching bug? Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / User | STATED | S-03, S-07 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | File storage must remain intact across script restarts (file itself is OK) | STATED | S-05 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The search and retrieval methods shall return documents such that modifying the returned dictionary objects does not mutate internal database cache or stored table documents. | STATED | S-03, S-07 | UNSET | READY | AC-001-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Document retrieval shall return independent dictionary copies. | STATED | S-07 | UNSET | READY | AC-NFR1-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a table containing a document, When a search or retrieval (e.g. search, all) is executed and the returned dictionary is modified in place, Then subsequent searches or retrievals return the original unmodified document values without side effects from the previous edits. |
| AC-NFR1-1 | NFR-001 | Given a document retrieved from table.search() or table.all(), When inspecting object identity (e.g. id(result) != id(stored)), Then the returned dictionary is a distinct copy instance. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-001 | Returning deep copies may affect performance for very large datasets or large nested documents. | INFERRED | S-03, S-07 |

## 8. Traceability
- S-01 -> FR-001
- S-02 -> FR-001
- S-03 -> FR-001
- S-04 -> FR-001
- S-05 -> CON-1
- S-06 -> FR-001
- S-07 -> FR-001, NFR-001
