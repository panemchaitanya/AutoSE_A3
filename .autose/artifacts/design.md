# Design: TinyDB increment/add/subtract missing field handling

## Approach
Modify `tinydb/operations.py` so that `increment`, `add`, and `subtract` check if the target field exists in the document (or dictionary). If the field is missing, treat its initial value as 0 before performing the arithmetic operation. This avoids KeyError and correctly fulfills the requirements.

## Files to change
- `tinydb/operations.py`
- `tests/test_operations.py`

## Functions/classes
- `increment`, `add`, `subtract` in `tinydb/operations.py`

## Test plan
- Verify `increment('count')` on a document without 'count' sets it to 1.
- Verify `increment('count', n=5)` on a document without 'count' sets it to 5.
- Verify `add('val', 5)` on a document without 'val' sets it to 5.
- Verify `subtract('val', 3)` on a document without 'val' sets it to -3.
- Ensure existing operations still behave correctly when fields already exist.

## Constraints respected
- Layering: operations.py remains independent of storage/table/database.
- Pure Python implementation with correct typing.