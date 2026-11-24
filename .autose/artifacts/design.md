# Design: Add limit parameter to search()
## Approach
Modify `Table.search` and `TinyDB.search` to accept an optional `limit` parameter. When `limit` is specified (not `None`), we adjust cache lookup and storage or iterate with a cap/stop condition, ensuring we return at most `limit` items in document ID order. Specifically, cache keys will be tuple `(cond, limit)` or caching will be handled such that `limit` is respected. Since `search` iterates through table items, we can stop early or slice the results while leveraging the cache appropriately.

## Files to change
`tinydb/database.py`
`tinydb/table.py`

## Functions/classes
- `tinydb.database.TinyDB.search`: add `limit=None` parameter and pass to table search.
- `tinydb.table.Table.search`: add `limit=None` parameter, update query cache keying or retrieval logic to respect `limit`.

## Test plan
- Test `db.search(cond, limit=10)` executes successfully.
- Test `search(cond, limit=None)` returns all matching documents when there are 5 matches.
- Test `search(cond, limit=5)` on a table with 100 matching documents returns exactly 5 documents in document ID order.
- Test `search(cond, limit=10)` on a table with 3 matching documents returns all 3 matching documents.

## Constraints respected
- ADR 2: Query cache keyed by stable query hash (or properly extended/bypassed for `limit`).
- Layering and existing method signatures are preserved for backwards compatibility.