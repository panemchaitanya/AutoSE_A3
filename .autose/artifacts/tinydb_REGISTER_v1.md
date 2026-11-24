# Register: tinydb (v1)

## A. Source statements
- S-01: db.search(cond) always returns every match.
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
- S-03: Could search take an optional limit?
- S-04: db.search(Query().category == 'book', limit=10) # first 10 matches only
- S-05: limit=None (default) keeps today's behavior - all matches, in document id order.
- S-06: limit=N returns at most the first N matches, in document id order.
- S-07: A limit larger than the number of matches just returns all matches.

## B. Ambiguous terms
- AMB-1: first N matches. Candidate meanings: first N matching documents encountered during iteration over table dict in document ID order. Resolution: document ID order.

## C. Open questions
None.

## D. Assumptions
- ASM-1: Cache behavior needs to account for limit (e.g. caching per limit or disabling cache when limit is provided). Linked to RSK-1.

## E. Conflicts
None.

## F. Evidence log
- EV-1: A3 repository-local analysis of tinydb/table.py search method implementation.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-1, FR-2, FR-3, FR-4)
- Performance: COVERED (NFR-1)
- Compatibility: COVERED (CON-1)

## H. Change log
- v1: Initial version from issue #37.