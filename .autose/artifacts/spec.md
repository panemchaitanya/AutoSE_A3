# Spec: TinyDB search limit parameter

## Source
Issue #37: Add a limit parameter to search()
> `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
> Could `search` take an optional `limit`?
> `db.search(Query().category == 'book', limit=10)` # first 10 matches only
> `db.search(Query().category == 'book')` # unchanged: all matches
> Expected semantics: limit=None (default) keeps today's behavior - all matches, in document id order; limit=N returns at most the first N matches, in document id order; A limit larger than the number of matches just returns all matches.

## Requirements
- FR-001: The Table.search method shall accept an optional limit parameter defaulting to None.
- FR-002: When limit is None, Table.search shall return all matching documents in document id order.
- FR-003: When limit is an integer N (where N >= 0), Table.search shall return at most the first N matching documents in document id order.
- FR-004: When limit is larger than the total number of matching documents, Table.search shall return all matching documents.

## Acceptance criteria
- Given a table search method signature, When inspecting arguments, Then an optional limit parameter is accepted and defaults to None.
- Given a call to db.search(cond, limit=5), When executed, Then the limit keyword argument is successfully accepted without error.
- Given a table with matching documents, When calling table.search(cond) without limit, Then all matching documents are returned in document id order.
- Given a table with 20 matching documents, When calling table.search(cond, limit=10), Then exactly the first 10 matching documents in document id order are returned.
- Given a table with matching documents, When calling table.search(cond, limit=0), Then an empty list of documents is returned.
- Given a table with 3 matching documents, When calling table.search(cond, limit=10), Then all 3 matching documents are returned.

## Assumptions and open questions
- Assumption: Negative integer limit values are handled by standard Python slice semantics or treated as empty/zero matches (linked to issue requirement semantics).
