# Register: TinyDB search limit parameter (v1)

## A. Source statements
- S-01: `db.search(cond)` always returns every match.
- S-02: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
- S-03: Could `search` take an optional `limit`?
- S-04: `db.search(Query().category == 'book', limit=10)   # first 10 matches only`
- S-05: `db.search(Query().category == 'book')             # unchanged: all matches`
- S-06: `limit=None` (default) keeps today's behavior - all matches, in document id order.
- S-07: `limit=N` returns at most the first N matches, in document id order.
- S-08: A limit larger than the number of matches just returns all matches.

## B. Ambiguous terms
- AMB-1: "pagination" (Issue #37 body)
  - Candidate meanings: (1) Offset/limit pagination; (2) Simple item capping/limiting (top-N).
  - Design decision forced: The issue explicitly specifies `limit=N` without an offset parameter, focusing on top-N / preview / latest 10. Offset support is out of scope unless separately requested.

## C. Open questions
- None. All requirements and semantics are explicitly defined in the issue description.

## D. Assumptions
- ASM-1: Negative limits ($N < 0$) are not expected or supported; passing negative limits should either raise ValueError or return empty list per standard Python slicing/limit conventions. (Default chosen: standard python slice/comparison behavior; linked to FR-003).

## E. Conflicts
- None.

## F. Evidence log
- EV-1: Repository code inspection (`tinydb/table.py`) confirms `search()` returns `[doc for doc in self if condition(doc)]` in document id order. Evidence mode: A3 repository-local analysis, no MCP used.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001, FR-002, FR-003)
- Data (kinds, volume, retention, ownership): COVERED (NFR-001)
- Integrations: N/A (Internal API change)
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: COVERED (NFR-001)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: COVERED (S-03, CON-1)
- Maintainability and extensibility: COVERED (RSK-1)
- Autonomy and human oversight: N/A
- Success measures: COVERED (AC-001-1 to AC-NFR-1)
- Scope exclusions: COVERED (AMB-1)
- Delivery constraints: N/A

## H. Change log
- v1: Initial version derived from GitHub issue #37.
