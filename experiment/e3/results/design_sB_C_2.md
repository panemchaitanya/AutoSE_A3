# Design: TinyDB Missing Field Operations

## Approach
Modify the update operations in `tinydb/operations.py` (`add`, `subtract`, `increment`, `decrement`) so that if the field does not exist in the document (`field not in doc`), it defaults to a sensible initial value (0 for numeric/addition/subtraction/increment/decrement operations). Specifically, for `increment`/`decrement`/`add`/`subtract`, if `field not in doc`, `doc[field]` is initialized to `0` before applying the operation (`+=` or `-=`).

## Files to change
- `tinydb/operations.py`
- `tests/test_operations.py` (NEW or existing test file)

## Functions/classes
- `add(field, n)` in `tinydb/operations.py`
- `subtract(field, n)` in `tinydb/operations.py`
- `increment(field)` in `tinydb/operations.py`
- `decrement(field)` in `tinydb/operations.py`

## Test plan
- Test `update(increment('count'))` on a document without 'count' results in 'count' set to 1.
- Test `update(decrement('count'))` on a document without 'count' results in 'count' set to -1.
- Test `update(add('score', 5))` on a document without 'score' results in 'score' set to 5.
- Test `update(subtract('score', 3))` on a document without 'score' results in 'score' set to -3.

## Constraints respected
- Layering and pure Python design
- Standard TinyDB operation interface unchanged
