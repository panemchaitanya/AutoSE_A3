# SRS: tinydb-issue-39 (v1)

## 1. Purpose and scope
- S-01: "Sometimes a search returns documents with values that are NOT what's stored."
- S-02: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-03: "It's like tinydb remembers my display edits."
- S-04: "If I restart the script the data is fine again, so the file itself is OK."
- S-05: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-06: "Is this a caching bug? Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Python Script Developer / User | STATED | S-02, S-06 |
| ACT-2 | TinyDB Database / Table search mechanism | STATED | S-01, S-03, S-05 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The database storage file itself must remain unaffected by in-memory modifications made to returned search documents unless an explicit update/insert method is called. | STATED | S-04 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The Table.search method shall return documents that are safe to mutate without causing side effects on subsequent searches or cached internal state within the same run. | STATED | S-06 | MUST | READY | AC-001-1 |
| FR-002 | The query cache or document retrieval mechanism shall return deep copies or independent copies of documents so that external modifications to returned dictionary structures do not corrupt cached query results. | INFERRED | S-02, S-03, S-06, tinydb/table.py:249-297 | MUST | CLARIFY | AC-002-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Search execution time shall not regress by more than TBD when returning independent document copies. | ASSUMED | Q-1 | UNSET | CLARIFY | AC-NFR1-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|>
| AC-001-1 | FR-001 | Given a table containing documents, When a user performs a search, modifies a field in the returned document dictionaries, and then performs the identical search again during the same runtime, Then the returned documents reflect the original stored database values rather than the modified display values. |
| AC-002-1 | FR-002 | Given a table with cached search results, When a returned document from search is mutated in place, Then the internal cache retains unmodified data and subsequent search calls return uncorrupted data. |
| AC-NFR1-1 | NFR-001 | Given search performance benchmarks, When deep copying documents, Then execution overhead remains within TBD milliseconds. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-001 | Returning deep copies of documents on every search may introduce a performance overhead for tables with large numbers of matching documents or nested structures. | INFERRED | tinydb/table.py:249-297 |

## 8. Traceability
- S-01 -> FR-001, CON-1
- S-02 -> FR-001, FR-002
- S-03 -> FR-001, FR-002
- S-04 -> CON-1
- S-05 -> FR-001
- S-06 -> FR-001, FR-002
