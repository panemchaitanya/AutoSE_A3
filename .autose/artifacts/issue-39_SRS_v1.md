# SRS: TinyDB Document Mutability and Caching Prevention (v1)

## 1. Purpose and scope

- S-01: "Sometimes a search returns documents with values that are NOT what's stored."
- S-02: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-03: "It's like tinydb remembers my display edits."
- S-04: "If I restart the script the data is fine again, so the file itself is OK."
- S-05: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-06: "Is this a caching bug?"
- S-07: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## 2. Actors

| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | TinyDB User / Python Script | STATED | S-02 |

## 3. Constraints

| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The underlying storage file must remain unaffected by in-memory edits to returned query/search results unless an explicit update/insert method is called. | STATED | S-04, S-07 | READY |

## 4. Functional requirements

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The database search and all retrieval methods shall return independent copies or non-aliased dictionaries of stored documents such that in-memory modifications to returned objects do not mutate internal table cache or subsequent query results. | INFERRED | S-02, S-05, S-07 | UNSET | CLARIFY | AC-001-1 |

## 5. Non-functional reqs

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Document retrieval operations shall not introduce latency exceeding TBD relative to current uncopied retrieval performance. | ASSUMED | Q-01 | UNSET | CLARIFY | AC-001-2 |

## 6. Acceptance criteria

| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a document stored in TinyDB, When a user executes a search or retrieves all documents, modifies the returned dictionary object in memory without calling update, and executes the same search again, Then the search results reflect the original stored values rather than the modified display values. |
| AC-001-2 | NFR-001 | Given large datasets retrieved via search, When measuring execution time of retrieval methods with copying enabled, Then the execution time per returned document does not exceed TBD milliseconds as defined in Q-01. |

## 7. Dependencies and risks

| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-001 | Copying every returned document could impact performance for applications retrieving large collections. | INFERRED | S-07 |

## 8. Traceability

- S-01 -> FR-001
- S-02 -> FR-001
- S-03 -> FR-001
- S-04 -> CON-1
- S-05 -> FR-001
- S-06 -> FR-001
- S-07 -> FR-001, CON-1
- FR-001 -> S-01, S-02, S-03, S-05, S-07, AC-001-1
- CON-1 -> S-04, S-07
- NFR-001 -> Q-01, AC-001-2
- AC-001-1 -> FR-001
- AC-001-2 -> NFR-001
- RSK-001 -> FR-001
