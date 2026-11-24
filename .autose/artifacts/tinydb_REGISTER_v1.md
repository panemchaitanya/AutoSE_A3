# Register: TinyDB limit parameter in search (v1)

## A. Source statements
- S-01: "`db.search(cond)` always returns every match."
- S-02: "When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful."
- S-03: "Could `search` take an optional `limit`?"
- S-04: "`db.search(Query().category == 'book', limit=10)` # first 10 matches only"
- S-05: "`db.search(Query().category == 'book')` # unchanged: all matches"
- S-06: "`- limit=None` (default) keeps today's behavior - all matches, in document id order."
- S-07: "`- limit=N` returns at most the first N matches, in document id order."
- S-08: "`- A limit larger than the number of matches just returns all matches."

## B. Ambiguous terms
*(None)*

## C. Open questions
*(None)*

## D. Assumptions
*(None)*

## E. Conflicts
*(None)*

## F. Evidence log
- EV-01: A3 repository-local analysis. Inspected `tinydb/table.py` and `tinydb/database.py` to confirm search signature and implementation. No MCP used.

## G. Coverage matrix
| Topic | Status | Ids |
|---|---|---|
| Core capabilities | COVERED | FR-001, FR-002, FR-003, FR-004 |
| Data | COVERED | CON-2 |
| Success measures | N/A | -

## H. Change log
- v1: Initial specification from issue #37.
