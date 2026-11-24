# Design: TinyDB Missing Field Operations

## Approach
We will update `tinydb/operations.py` so that field operations (`increment`, `decrement`, `add`, `subtract`) handle missing fields gracefully by defaulting missing fields to `0` before performing the arithmetic operation. Specifically, we can use `doc.get(field, 0)` or check `if field not in doc: doc[field] = 0` (or similar for add/subtract/increment/decrement).

## Files to change
- `tinydb/operations.py`
- `tests/test_operations.py` (NEW or existing test file)

## Functions/classes
- Modify `add`, `subtract`, `increment`, `decrement` in `tinydb/operations.py` to check for field existence or default to `0` when missing.

## Test plan
- Test `update(increment('count'))` on a document without `'count'`; verify it sets `'count'` to `1`.
- Test `update(decrement('count'))` on a document without `'count'`; verify it sets `'count'` to `-1`.
- Test `update(add('score', 5))` on a document without `'score'`; verify it sets `'score'` to `5`.
- Test `update(subtract('score', 3))` on a document without `'score'`; verify it sets `'score'` to `-3`.

## Constraints respected
- Layering and dependencies (operations do not import tables/databases/queries).
