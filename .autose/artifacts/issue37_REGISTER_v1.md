# Register: TinyDB search limit parameter (v1)

## A. Source statements
- S-01: `db.search(cond)` always returns every match.
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
- S-03: Could `search` take an optional `limit`?
- S-04: `db.search(Query().category == 'book', limit=10)` # first 10 matches only
- S-05: `db.search(Query().category == 'book')` # unchanged: all matches
- S-06: `limit=None` (default) keeps today's behavior - all matches, in document id order.
- S-07: `limit=N` returns at most the first N matches, in document id order.
- S-08: A limit larger than the number of matches just returns all matches.

## B. Ambiguous terms
- AMB-1: pagination. Candidate meanings: (1) Offset/limit pagination, (2) Simple limit-based retrieval for top-N or cursor start. Decision forced: Issue states limit parameter for first N matches.

## C. Open questions
- None

## D. Assumptions
- ASM-1: Negative integer limit values are out of scope or treated as 0 / empty result via Python slice semantics, but explicitly tested.

## E. Conflicts
- None

## F. Evidence log
- EV-1: A3 repository-local analysis (no MCP used), inspecting `tinydb/table.py` where `search(self, cond: QueryLike)` is defined.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001, FR-002, FR-003, FR-004)
- Data: COVERED
- Integrations: N/A
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: COVERED (S-02)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: N/A
- Maintainability and extensibility: COVERED
- Success measures: COVERED
- Scope exclusions: COVERED
- Delivery constraints: N/A

## H. Change log
- v1: Initial specification created from issue #37.
