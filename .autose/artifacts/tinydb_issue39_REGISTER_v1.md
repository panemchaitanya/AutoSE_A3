# Register: TinyDB In-Memory Document Mutation Leak Prevention (v1)

## A. Source statements
- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "Example: I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-04: "It's like tinydb remembers my display edits."
- S-05: "If I restart the script the data is fine again, so the file itself is OK."
- S-06: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-07: "Is this a caching bug? Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"
- S-08: "Not sure what exactly is going on, happy to provide more info if you tell me what you need."

## B. Ambiguous terms
- AMB-1: "caching bug" | Candidate meanings: 1. Explicit caching layer returning references; 2. In-memory table representation holding direct references to internal document dicts without copying. | Design decision forced: FR-001 requires returning isolated copies of documents.

## C. Open questions
- Q-001 | What is the acceptable performance overhead threshold for copying documents returned by search and all? | Matters for NFR-001 fit criterion | Blocks: NFR-001 | Score: 1 | Default: Performance overhead shall not exceed TBD percentage over baseline search execution time | Owner: Stakeholder | Status: OPEN

## D. Assumptions
- ASM-001 | Document isolation overhead should be minimal and bounded. Linked to Q-001.

## E. Conflicts
- None.

## F. Evidence log
- EV-001 | Repository inspection | tinydb/table.py returns internal document references directly | Effect: Supports FR-001 and confirms in-memory reference sharing.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1, ACT-2)
- Core capabilities: COVERED (FR-001)
- Data: COVERED (CON-1)
- Performance: OPEN (NFR-001, Q-001)
- All other coverage topics: N/A for this scoped bug report.

## H. Change log
- v1 initial draft.
