# REGISTER: issue_39 (v1)
## A. Source statements
- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "Example: I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-04: "It's like tinydb remembers my display edits."
- S-05: "If I restart the script the data is fine again, so the file itself is OK."
- S-06: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-07: "Is this a caching bug? Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## B. Ambiguous terms
- AMB-1: "caching bug" - Candidate meanings: 1) Query cache returning cached references without copying; 2) Storage layer caching mechanism. Decision forced: FR-001 needs to ensure returned documents are isolated copies.

## C. Open questions
- None.

## D. Assumptions
- None.

## E. Conflicts
- None.

## F. Evidence log
- EV-01: A3 repository-local analysis (no MCP used): Inspected `tinydb/table.py` around lines 235-265 showing `table.all()` and `table.search()` return document dict references directly without copying.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001)
- Data: COVERED (CON-1)
- Performance: COVERED (NFR-001)

## H. Change log
- v1: Initial extraction from issue #39.
