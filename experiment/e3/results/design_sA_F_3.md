# Design: Add a limit parameter to search()

## Approach
We will add an optional `limit: Optional[int] = None` parameter to `Table.search()` and forward it from `TinyDB.search()` in `tinydb/database.py`. When `limit` is specified and is a non-negative integer, `search` will return at most `limit` matching documents. Caching behavior is preserved or adjusted carefully (e.g. caching full search results or handling slices appropriately, or since query cache caches all matching docs, we slice the cached list or apply limit after fetching from cache). Slicing the cached list (`cached_results[:limit]` if `limit is not None` else `cached_results[:]`) is extremely clean, efficient, and preserves query cache validity and correct semantics.

## Files to change
- `tinydb/table.py`
- `tinydb/database.py`
- `tests/test_tables.py` (NEW or modified)
- `tests/test_tinydb.py` (modified)

## Functions/classes
- Modify `Table.search(self, cond: QueryLike, limit: Optional[int] = None) -> list[Document]`
- Modify `TinyDB.search(self, cond: QueryLike, limit: Optional[int] = None, **kwargs) -> list[Document]` (or forwarding via `**kwargs` or explicit parameter)

## Test plan
- Test `table.search(cond, limit=2)` returns at most 2 documents in doc_id order.
- Test `table.search(cond, limit=None)` returns all matching documents.
- Test `table.search(cond, limit=100)` where 100 exceeds match count returns all matching documents.
- Test `db.search(cond, limit=5)` on the `TinyDB` instance returns at most 5 matching documents from the default table.

## Constraints respected
- ADR 2 (Query cache keyed by stable query hash remains intact, slicing cached/uncached results respects order and limit).
- Layering and type safety (typing annotations with `Optional[int]`).
