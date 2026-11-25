# SRS: TinyDB In-Memory Document Mutation Leak Prevention (v1)

## 1. Purpose and scope

- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "Example: I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-04: "It's like tinydb remembers my display edits."
- S-05: "If I restart the script the data is fine again, so the file itself is OK."
- S-06: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-07: "Is this a caching bug? Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"
- S-08: "Not sure what exactly is going on, happy to provide more info if you tell me what you need."

## 2. Actors

| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | TinyDB User / Python Script | STATED | S-03, S-06 |
| ACT-2 | TinyDB Database / Table search mechanism | STATED | S-02, S-07 |

## 3. Constraints

| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | The persisted file storage remains correct across script restarts without manual file correction. | STATED | S-05 | READY |

## 4. Functional requirements

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-001 | The search and all methods on Table shall return documents that are isolated copies so subsequent in-place modifications to returned dictionaries do not affect stored or subsequently retrieved documents within the same run. | STATED | S-07 | UNSET | CLARIFY | AC-001-1 |

## 5. Non-functional reqs

| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| NFR-001 | Document isolation overhead shall not introduce execution time degradation exceeding TBD percentage over baseline search execution time. | ASSUMED | Q-001 | UNSET | CLARIFY | AC-001-NFR1 |

## 6. Acceptance criteria

| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|---|
| AC-001-1 | FR-001 | Given a document stored in TinyDB, When a user performs a search or gets all documents, mutates the returned dictionary object in-place, and performs the same search again, Then the newly retrieved search results reflect the original stored database state rather than the in-place mutated dictionary. |
| AC-001-NFR1 | NFR-001 | Given a benchmark suite measuring search performance, When deep copying is enabled for returned documents, Then the execution time overhead remains within TBD threshold. |

## 7. Dependencies and risks

| ID | Statement | Basis | Source |
|---|---|---|---|
| RSK-001 | Deep copying every returned document on search or all operations may impact performance for large collections or nested dictionaries. | INFERRED | S-07, Q-001 |

## 8. Traceability

| Source ID / EV ID | Corresponding Requirement IDs |
|---|---|
| S-01 | FR-001 |
| S-02 | FR-001 |
| S-03 | FR-001 |
| S-04 | FR-001 |
| S-05 | CON-1 |
| S-06 | FR-001 |
| S-07 | FR-001 |
| S-08 | None |
