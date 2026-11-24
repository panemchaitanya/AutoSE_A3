# Design: Add a limit parameter to search()

## Approach
We will update `Table.search` in `tinydb/table.py` to accept an optional `limit: Optional[int] = None` parameter. When `limit` is provided, we can either apply a slice on the cached results list (if retrieved from the cache) or apply `itertools.islice` or slicing during the matching loop (or slice the resulting list before caching/returning). Note that caching the full search results allows queries with different limits or subsequent unlimited queries to benefit from the cache (or we can slice the cached list when returning). Specifically, if we cache the full list of matches for a query, then `table.search(cond, limit=N)` can simply return `cached_results[:limit]` (handling `limit=None` correctly as returning all). For the non-cached case, we can collect the matching documents and apply `[:limit]` before caching the full list and returning the sliced list. Also, `TinyDB.search` in `tinydb/database.py` will be updated to accept `limit: Optional[int] = None` and forward it to the default table's `search` method.

## Files to change
- `tinydb/table.py`
- `tinydb/database.py`
- `tests/test_tables.py` (NEW or modify existing)
- `tests/test_tinydb.py` (modify existing)

## Functions/classes
- `Table.search(self, cond: QueryLike, limit: Optional[int] = None) -> list[Document]` in `tinydb/table.py`
- `TinyDB.search(self, cond: QueryLike, limit: Optional[int] = None) -> list[Document]` in `tinydb/database.py`

## Test plan
- Test `table.search(cond, limit=2)` returns at most 2 matching documents in doc ID order.
- Test `table.search(cond, limit=None)` returns all matching documents in doc ID order.
- Test `table.search(cond, limit=100)` where 100 exceeds match count returns all matching documents.
- Test `db.search(cond, limit=5)` returns at most 5 matching documents from the default table.

## Constraints respected
- ADR 2: Query cache remains valid and properly keyed by the query hash; cached results can be sliced by `limit` on return, while caching the full match set.
- Layering and typing conventions in TinyDB are strictly followed.