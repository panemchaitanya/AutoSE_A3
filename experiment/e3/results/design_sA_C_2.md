# Design: Add a limit parameter to search()

## Approach
We will add an optional `limit` parameter (defaulting to `None`) to `Table.search()` in `tinydb/table.py`. When `limit` is provided and is an integer, `Table.search()` will collect and return at most `limit` matching documents in document id order. Since TinyDB's `Table.search()` iterates through `self._read_table().items()` (which are already in document ID order), we can either slice or short-circuit collection once `limit` items are found. Note that query caching should correctly handle the presence of `limit` (or we can include `limit` in cache lookup/storage, or bypass/incorporate `limit` in the cache or query representation). Wait, if a query is cached without a limit, or with a different limit, caching needs to respect `limit`. But wait, does `QueryInstance` or cache keying need to include `limit`? Let's check how `Table.search` uses the query cache: it uses `cond` as the cache key (`self._query_cache[cond]`). If `limit` is specified, caching the full result or caching per-limit or disabling caching when `limit` is not None (or including `limit` in cache handling) should be considered. Let's see: if `limit` is `None`, we can use the existing cache. If `limit` is not `None`, we can either slice the cached full result if available, or skip caching / handle caching appropriately. Slicing the cached full result if `cached_results` is present is extremely efficient and clean! Alternatively, if `limit` is specified, we can retrieve `cached_results` (if cached for `cond`), slice it up to `limit`, and return it. If not cached, we compute full docs matching `cond`, cache the full list of matching docs for `cond`, and return a slice of up to `limit`! That preserves the query cache for `cond` entirely while correctly supporting `limit`.

## Files to change
- `tinydb/table.py` (MODIFY)
- `tests/test_tables.py` (MODIFY)
- `tests/test_tinydb.py` (MODIFY)

## Functions/classes
- `Table.search(self, cond: QueryLike, limit: Optional[int] = None) -> list[Document]` in `tinydb/table.py`
- `TinyDB` forwarding / search methods if necessary (since `TinyDB` inherits from `Table` via `TableBase` and uses `__getattr__` or `search` directly from `Table`, `db.search(cond, limit=5)` is automatically forwarded/supported).

## Test plan
- Test `table.search(cond, limit=2)` returns at most 2 matching documents in document ID order.
- Test `table.search(cond, limit=None)` returns all matching documents.
- Test `table.search(cond, limit=100)` where 100 exceeds match count returns all matching documents.
- Test `db.search(cond, limit=5)` on a database instance returns at most 5 matching documents from the default table.

## Constraints respected
- Constraint 3: Query objects keep stable hashes (query cache mechanism remains intact and robust).
- Constraint 4: Table mutation methods clear the query cache.
- No changes to storage or middleware layers, adhering to ADR 1 & 3.
