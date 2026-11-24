# Register: TinyDB Search Limit (v1)

## A. Source statements
- S-01: `db.search(cond)` always returns every match.
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
- S-03: Could `search` take an optional `limit`?
- S-04: `db.search(Query().category == 'book', limit=10)` -> first 10 matches only.
- S-05: `db.search(Query().category == 'book')` -> unchanged: all matches.
- S-06: `limit=None` (default) keeps today's behavior - all matches, in document id order.
- S-07: `limit=N` returns at most the first N matches, in document id order.
- S-08: A limit larger than the number of matches just returns all matches.

## B. Ambiguous terms
- AMB-1: `limit` (int vs None vs negative/zero values). Candidate meanings: (1) positive integer N caps return length; (2) None means no limit; (3) 0 or negative values return empty list or raise ValueError. Resolution: default to None for unlimited, positive integer for max count, handled per standard slicing/iteration.

## C. Open questions
- Q-1: What should happen if a negative integer or zero is passed as `limit`? Blocks: FR-003. Score: 1. Default: negative/zero limit returns an empty list or behaves as standard slice `[:0]` / `[:N]`. Owner: maintainer. Status: ASSUMED.

## D. Assumptions
- ASM-1: Negative or zero limit values follow Python slicing semantics (e.g. `[:0]` returns empty list). Linked to Q-1.

## E. Conflicts
- None.

## F. Evidence log
- EV-1: A3 repository-local analysis of `tinydb/table.py` confirms `search()` iterates over documents and returns a list of matching documents.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001 through FR-004)
- Data: COVERED
- Integrations: N/A
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: COVERED (NFR-001)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: COVERED
- Maintainability and extensibility: COVERED
- Success measures: COVERED
- Scope exclusions: N/A
- Delivery constraints: N/A

## H. Change log
- v1.0 initial baseline specification from issue #37.
