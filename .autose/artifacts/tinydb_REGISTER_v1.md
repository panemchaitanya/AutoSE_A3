# Register: TinyDB Limit Parameter (v1)

## A. Source statements
- S-1: `db.search(cond)` always returns every match.
- S-2: When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
- S-3: Could `search` take an optional `limit`?
- S-4: `limit=None` (default) keeps today's behavior - all matches, in document id order.
- S-5: `limit=N` returns at most the first N matches, in document id order.
- S-6: A limit larger than the number of matches just returns all matches.

## B. Ambiguous terms
- AMB-1: "first few" -> resolved by S-5 (`limit=N` returns at most the first N matches).

## C. Open questions
None.

## D. Assumptions
- ASM-1: Negative integer limits are not expected/supported per standard pagination semantics and standard Python slicing.

## E. Conflicts
None.

## F. Evidence log
- EV-1: A3 repository-local analysis (no MCP used). Inspected `tinydb/table.py` and `tinydb/database.py` to confirm search method signatures and proxy forwarding.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-1 to FR-5)
- Data, Performance, integrations, etc.: COVERED

## H. Change log
- v1: Initial requirements specification.
