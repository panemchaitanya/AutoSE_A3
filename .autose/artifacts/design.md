# Design: Prevent search and query results from retaining in-memory mutations across calls
## Approach
We will update search, all, get, and iteration methods in `tinydb/table.py` to return deep copies (using `copy.deepcopy` or by copying the Document/dict instances) of stored documents. This ensures that mutating returned dictionaries or nested structures does not affect internal cache or storage states.
## Files to change
- `tinydb/table.py`
- `tests/test_tinydb.py` (for tests)
## Functions/classes
- `Table.all`
- `Table.search`
- `Table.get`
- `Table.__iter__`
## Test plan
- Test that modifying a field in a document returned by `search()` or `all()` does not change the result of subsequent calls to `search()` or `all()`.
- Verify general correctness with existing test suite.
## Constraints respected
- ADR 2: Query cache keyed by stable query hash (cache remains valid, but results returned are deep copies so modifications don't mutate cached objects).
- Layering and pure Python constraints.