# SRS: issue39 (v1)
## 1. Purpose and scope
- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything. It's like tinydb remembers my display edits."
- S-04: "If I restart the script the data is fine again, so the file itself is OK. It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?). Is this a caching bug?"
- S-05: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer / Script Runner | STATED | S-03 |

## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Documents returned by search and all queries must be safe to edit without side effects on subsequent searches or internal state. | STATED | S-05 | READY |

## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The table query and retrieval methods shall return deep copies of documents so that mutations to returned dictionaries do not affect internal database storage or subsequent search results. | STATED | S-03, S-05 | MUST | READY | AC-001-1 |

## 5. Non-functional reqs
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Search retrieval performance impact from deep copying shall not exceed 10% overhead compared to baseline retrieval time for collections up to 10,000 documents. | ASSUMED | Q-1 | UNSET | CLARIFY | TBD |

## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|---|                     
| AC-001-1 | FR-001 | Given a document is stored in the database, When a user retrieves the document via search or all and modifies the returned dictionary, Then subsequent searches for the document return the original stored values without modification. |

## 7. Dependencies and risks
| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-001 | Deep copying every returned document might impact performance for large query result sets. | INFERRED | S-05 |

## 8. Traceability
| Source / Evidence ID | Requirement IDs |
|---|---|
| S-01 | FR-001 |
| S-02 | FR-001 |
| S-03 | FR-001 |
| S-04 | FR-001 |
| S-05 | FR-001, CON-1 |
