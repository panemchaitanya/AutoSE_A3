# Design: TinyDB Missing Field Operations

## Approach
Modify the `add`, `subtract`, `increment`, and `decrement` operations in `tinydb/operations.py` so that if the specified field does not exist in the document (`field not in doc`), it is initialized to `0` before performing the arithmetic operation. This matches standard accumulator behavior and prevents `KeyError` exceptions when operating on missing fields.

## Files to change
- `tinydb/operations.py`
- `tests/test_operations.py` (NEW or modify existing test files - let's check existing tests first or write tests via test plan)

## Functions/classes
- `add(field, n)`: modify `transform` to check `if field not in doc: doc[field] = 0`
- `subtract(field, n)`: modify `transform` to check `if field not in doc: doc[field] = 0`
- `increment(field)`: modify `transform` to check `if field not in doc: doc[field] = 0`
- `decrement(field)`: modify `transform` to check `if field not in doc: doc[field] = 0`

## Test plan
- Test `increment` on a document without the field (verifies field is initialized to 0 and becomes 1).
- Test `decrement` on a document without the field (verifies field is initialized to 0 and becomes -1).
- Test `add` on a document without the field (verifies field is initialized to 0 and becomes `n`).
- Test `subtract` on a document without the field (verifies field is initialized to 0 and becomes `-n`).

## Constraints respected
- Pure Python implementation, layer rules respected (operations does not depend on database/table/queries/storage).
