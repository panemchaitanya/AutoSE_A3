# Design: Add a limit parameter to search()

## Approach
Modify `Table.search` to accept an optional `limit: Optional[int] = None`. When `limit` is specified (an integer >= 0), iterate through documents matching the condition and stop once `limit` items have been accumulated. Also update `TinyDB.search` in `tinydb/database.py` to accept and forward the `limit` parameter to the default table's `search` method.

## Files to change
- `tinydb/table.py`
- `tinydb/database.py`
- Tests (e.g. `tests/test_tinydb.py` or a new test or existing test files)

## Functions/classes
- `Table.search(self, cond: QueryInstance, limit: Optional[int] = None)`
- `TinyDB.search(self, cond: QueryInstance, limit: Optional[int] = None)`

## Test plan
- Test `table.search(cond, limit=N)` returns at most N matching documents in document ID order.
- Test `table.search(cond, limit=None)` returns all matching documents.
- Test `table.search(cond, limit=100)` when match count is smaller than 100 returns all matching documents.
- Test `db.search(cond, limit=N)` forwards `limit` from `TinyDB` to the default table.

## Constraints respected
- Query hashes / caching (cached results in `Table` are stored by query instance/hash; note whether limit affects caching or if search without limit vs with limit uses separate cache entries or if limit is part of search cache key / bypassed. Wait, let's look at how `Table.search` uses cache).
