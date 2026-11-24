# Design: TinyDB Missing Field Operations

## Approach
Modify the arithmetic update operations (`increment`, `decrement`, `add`, and `subtract`) in `tinydb/operations.py` so that if the target field does not exist in the document (`field not in doc`), it is initialized to `0` before applying the operation. This prevents `KeyError` exceptions when operating on missing fields, fulfilling the user requirements and aligning with standard accumulator behavior.

## Files to change
- `tinydb/operations.py`
- `tests/test_operations.py` (NEW or modified existing test file for operations)

## Functions/classes
- `add(field, n)`: modify `transform` to check `if field not in doc: doc[field] = 0` before `doc[field] += n`.
- `subtract(field, n)`: modify `transform` to check `if field not in doc: doc[field] = 0` before `doc[field] -= n`.
- `increment(field)`: modify `transform` to check `if field not in doc: doc[field] = 0` before `doc[field] += 1`.
- `decrement(field)`: modify `transform` to check `if field not in doc: doc[field] = 0` before `doc[field] -= 1`.

## Test plan
- Test `update(increment('count'))` on a document without 'count', verifying it results in `count` = 1.
- Test `update(decrement('count'))` on a document without 'count', verifying it results in `count` = -1.
- Test `update(add('score', 5))` on a document without 'score', verifying it results in `score` = 5.
- Test `update(subtract('score', 3))` on a document without 'score', verifying it results in `score` = -3.

## Constraints respected
- Layering and separation of concerns: operations remain pure functions acting on dict-like documents without touching storage/table machinery directly.
