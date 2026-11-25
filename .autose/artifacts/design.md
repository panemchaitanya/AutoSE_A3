# Design: TinyDB Search Result Mutability and Caching Isolation

## Approach
To ensure that in-place mutations of documents returned by `search()`, `all()`, and `get()` do not affect subsequent database operations, internal table storage, or the query cache, we will wrap the returned `Document` instances (or their contents) in deep copies (`copy.deepcopy`). Specifically, `Table.search` will return deep copies of its cached or matched documents, and `Table.__iter__` (which powers `all()`) and `get()` will also ensure deep copies are returned so callers can safely modify returned dictionaries without side effects or leaking state into the query cache/internal storage.

## Files to change
- `tinydb/table.py` (NEW: modified to return deep copies on retrieval methods)
- `tests/test_table.py` (NEW: tests for search/all/get mutability isolation)

## Functions/classes
- Modify `Table.search(self, cond)` in `tinydb/table.py` to return `copy.deepcopy(doc)` for each document.
- Modify `Table.__iter__(self)` or related retrieval paths in `tinydb/table.py` (like `get()`) to ensure deep copies are returned.
- Add tests verifying FR-1, FR-2, CON-1 and acceptance criteria.

## Test plan
- Test that modifying a dictionary returned by `search()` or `all()` or `get()` does not change subsequent query or retrieval results.
- Test nested dictionary/list mutations.
- Test performance characteristics and ensure no regression or memory exceptions.

## Constraints respected
- ADR 2 (Query cache keyed by a stable query hash): Query cache behavior remains consistent, but values stored or returned are safely isolated via deep copying.
- Layering and storage protocols remain unchanged.