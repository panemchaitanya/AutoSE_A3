# Spec: Add a limit parameter to search()

## Source
Issue #37: `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. Could `search` take an optional `limit`?

## Requirements
- FR-1: The database search and table search methods shall accept an optional `limit` parameter defaulting to `None`.
- FR-2: When `limit` is `None`, search shall return all matching documents in document id order.
- FR-3: When `limit` is set to an integer N, search shall return at most the first N matching documents in document id order.
- FR-4: When `limit` is larger than the total number of matching documents, search shall return all matching documents.

## Acceptance criteria
- Given a call to `db.search(cond)` without `limit`, When executed, Then it accepts the call without errors and behaves according to default parameters.
- Given a table with documents matching a condition, When `db.search(cond, limit=None)` is called, Then all matching documents are returned in document id order.
- Given a table with multiple matching documents, When `db.search(cond, limit=3)` is called, Then at most the first 3 matching documents are returned in document id order.
- Given a table with 2 matching documents, When `db.search(cond, limit=10)` is called, Then both matching documents are returned.

## Assumptions and open questions
- None. All requirements are fully specified by the issue description.