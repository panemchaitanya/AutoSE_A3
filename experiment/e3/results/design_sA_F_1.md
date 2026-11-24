# Design: Add a limit parameter to search()

## Approach
We will update `Table.search` to accept an optional `limit: Optional[int] = None` parameter. When `limit` is provided and non-negative, we truncate the resulting document list (or optimize iteration/collection) to at most `limit` items. We also update `TinyDB.search` in `tinydb/database.py` to forward `limit` to the default table. The query cache behavior remains correct because caching full search results allows slicing them upon retrieval (or caching based on limit if needed, though caching full results or taking limit into account should be considered carefully; caching full results and returning `docs[:limit]` is extremely clean and avoids cache fragmentation, as standard TinyDB query caching expects the full list of matches). Let's check if caching full results and slicing is correct or if we should slice before/after cache. Slicing after cache retrieval `cached_results[:limit]` (or handling it appropriately) is simple and robust.

## Files to change
- `tinydb/table.py`
- `tinydb/database.py`
- `tests/test_table.py` (NEW or existing test files - let's check existing tests)

## Functions/classes
- `Table.search(self, cond: QueryLike, limit: Optional[int] = None) -> list[Document]`
- `TinyDB.search(self, cond: QueryLike, limit: Optional[int] = None) -> list[Document]`

## Test plan
- Test `table.search(cond, limit=2)` returns at most 2 matching documents in document id order.
- Test `table.search(cond, limit=None)` returns all matching documents.
- Test `table.search(cond, limit=100)` when match count is smaller returns all matching documents.
- Test `db.search(cond, limit=5)` on `TinyDB` instance returns at most 5 matching documents from the default table.

## Constraints respected
- Query objects keep stable hashes (ADR 2).
- Layering rules respected.
