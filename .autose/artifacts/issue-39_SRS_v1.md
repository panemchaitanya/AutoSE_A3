# SRS: TinyDB Search Result Mutability and Caching Isolation (v1)

## 1. Purpose and scope

This specification addresses GitHub issue #39, where searching or retrieving documents from TinyDB returns references to internal cached or stored dictionary objects rather than independent copies. As a result, when a caller modifies a returned document dictionary in place during a runtime session (e.g. for display formatting), those modifications persist across subsequent searches within the same run without explicit update calls, causing unexpected data state divergence until the script is restarted.

Stated requirements derived directly from the issue description:
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
| ACT-1 | Python Script / Application Developer | STATED | S-02, S-07 |
| ACT-2 | TinyDB Database / Table / Query Engine | STATED | S-03, S-06 |

## 3. Constraints

| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The underlying stored database file itself must remain unaffected and correct on disk when search/all results are mutated in memory. | STATED | S-04 | READY |
| CON-2 | Restarting the script or reloading from storage must restore unmutated database values. | STATED | S-04 | READY |

## 4. Functional requirements

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The database search method (`search`) shall return independent deep copies or unshared copies of documents such that in-place mutations of returned document dictionaries do not affect subsequent searches or internal table storage within the same run. | STATED | S-02, S-07 | UNSET | CLARIFY | AC-001-1, AC-001-2 |
| FR-002 | The database retrieval methods (`all`, `get`, etc. returning documents) shall return independent copies of documents such that in-place mutations do not persist or bleed into subsequent retrievals or internal table state. | STATED | S-02, S-07 | UNSET | CLARIFY | AC-002-1 |

## 5. Non-functional reqs

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Search and retrieval operations returning document copies shall execute efficiently without introducing disproportionate time complexity relative to document payload size. | ASSUMED | Q-1 | UNSET | CLARIFY | AC-NFR1-1 |

## 6. Acceptance criteria

| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-001-1 | FR-001 | Given a table containing a document with field value 'abc', When a user searches for the document, modifies the returned dictionary field in place to 'xyz', and searches for the same document again in the same run, Then the second search returns the document with the original stored value 'abc' rather than the modified value 'xyz'. |
| AC-001-2 | FR-001 | Given a table containing a document, When a search returns a document dictionary, Then modifying nested keys or values of the returned dictionary has no effect on subsequent query results or internal storage cache. |
| AC-002-1 | FR-002 | Given a table containing documents, When `all()` or `get()` is called, Then modifying the returned dictionary objects does not mutate the internal table data or subsequent calls to `all()` or `get()`. |
| AC-NFR1-1 | NFR-001 | Given a table containing a document dictionary with up to 100 nested key-value pairs, When `search()` is executed 1,000 times consecutively, Then the total elapsed execution time overhead introduced by defensive copying remains proportional to O(N * D) where N is result count and D is document depth/size, completing successfully without throwing memory or recursion exceptions. |

## 7. Dependencies and risks

| ID | Statement | Basis | Source |
|---|---|---|---|
| DEP-1 | TinyDB table caching mechanism (`table.py`) caching deserialized or retrieved documents. | EVIDENCED | Repository inspection (`tinydb/table.py`) |
| RSK-1 | Deep copying every returned document may impact performance for applications handling very large numbers of documents or large nested payloads. | INFERRED | S-07, architecture analysis |

## 8. Traceability

- S-01 -> FR-001, FR-002
- S-02 -> FR-001, FR-002, AC-001-1
- S-03 -> FR-001, FR-002
- S-04 -> CON-1, CON-2
- S-05 -> FR-001
- S-06 -> FR-001
- S-07 -> FR-001, FR-002, AC-001-2
- FR-001 -> S-01, S-02, S-03, S-05, S-06, S-07
- FR-002 -> S-02, S-07
- CON-1 -> S-04
- CON-2 -> S-04
- NFR-001 -> Q-1
- DEP-1 -> EV-1
- RSK-1 -> S-07
