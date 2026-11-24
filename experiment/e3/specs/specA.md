# Spec: Add a limit parameter to search()

## Source
Issue #4: `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. Could `search` take an optional `limit`?

## Requirements
- FR-1: The `Table.search` method shall accept an optional `limit` parameter of type `Optional[int]`.
- FR-2: When `limit` is `None`, `Table.search` shall return all matching documents in document id order.
- FR-3: When `limit` is a non-negative integer `N`, `Table.search` shall return at most the first `N` matching documents in document id order.
- FR-4: When `limit` is larger than the number of matching documents, `Table.search` shall return all matching documents.
- FR-5: The `TinyDB` database class shall forward the `limit` parameter in `search()` calls to the default table.

## Acceptance criteria
- Given a table with multiple matching documents, When calling `table.search(cond, limit=2)`, Then at most 2 matching documents are returned in document id order.
- Given a table with matching documents, When calling `table.search(cond, limit=None)`, Then all matching documents are returned in document id order.
- Given a table with matching documents, When calling `table.search(cond, limit=100)` where 100 exceeds match count, Then all matching documents are returned.
- Given a database instance `db`, When calling `db.search(cond, limit=5)`, Then at most 5 matching documents from the default table are returned.

## Assumptions and open questions
- ASM-1: Negative integer limits are not expected/standard and follow default Python slicing or exception handling if unsupported. (Linked to standard pagination usage).
