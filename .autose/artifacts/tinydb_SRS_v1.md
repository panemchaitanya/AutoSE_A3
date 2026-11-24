# SRS: TinyDB Safe Search Retrieval (v1)

## 1. Purpose and scope
- S-01: "Sometimes a search returns documents with values that are NOT what's stored."
- S-02: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything. It's like tinydb remembers my display edits."
- S-03: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Script Runner | STATED | S-01, S-02, S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | In-place modifications to dictionaries returned by database retrieval methods must not mutate internal database caches or affect subsequent query results within the same script run. | STATED | S-02, S-03 | CLARIFY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-1 | The database retrieval methods (`search` and `all`) shall return unshared copy instances of document dictionaries such that modifying a returned dictionary does not mutate cached database documents. | STATED | S-01, S-02, S-03 | UNSET | CLARIFY | AC-001-1, AC-001-2 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-1 | Document retrieval methods shall complete execution without memory leakage across repeated queries within a single process run. | INFERRED | S-02 | UNSET | CLARIFY | AC-NFR-1-1 |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|----|
| AC-001-1 | FR-1 | Given a document stored in a TinyDB table, when a user calls `search()` or `all()`, modifies a field of a returned document dictionary in place, and subsequently executes `search()` for the same document, then the newly returned dictionary contains the original stored value and not the modified value. |
| AC-001-2 | FR-1 | Given a document stored in a TinyDB table, when a user retrieves a document via `search()`, modifies a field in place, and subsequently retrieves all documents via `all()`, then the dictionary returned by `all()` contains the original stored value. |
| AC-NFR-1-1 | NFR-1 | Given 1000 consecutive `search()` queries on a table, when returned dictionaries are modified in place after each query, then memory consumption does not exceed 100MB above baseline. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-1 | Deep copying or copying document dictionaries on every retrieval could introduce mild computational overhead for very large result sets. | INFERRED | S-03 |

## 8. Traceability
- S-01 -> FR-1
- S-02 -> FR-1, CON-1, NFR-1
- S-03 -> FR-1, CON-1
- FR-1 -> S-01, S-02, S-03
- CON-1 -> S-02, S-03
- NFR-1 -> S-02
