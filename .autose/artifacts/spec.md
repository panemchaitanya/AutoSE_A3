# Spec: Consistent string ID handling in update and remove

## Source
Issue #35: "update() and remove() silently do nothing when I pass the doc id as a string"
> "Please make these consistent with get (which accepts the string form)."

## Requirements
1. FR-1: The `update()` method shall accept string representations of document IDs and perform the update if the ID matches an existing record (consistent with `get()`).
2. FR-2: The `remove()` method shall accept string representations of document IDs and perform the removal if the ID matches an existing record (consistent with `get()`).
3. FR-3: The system shall not raise an exception when a string ID is passed to `update()` or `remove()` that does not match any record; it should return an empty list as per existing behavior for non-matching IDs.

## Acceptance criteria
- Given a TinyDB instance with one document (ID 1), when `db.update({'x': 2}, doc_ids=['1'])` is called, then the document with ID 1 is updated and the method returns `[1]`.
- Given a TinyDB instance with one document (ID 1), when `db.remove(doc_ids=['1'])` is called, then the document with ID 1 is removed and the method returns `[1]`.
- Given a TinyDB instance with one document (ID 1), when `db.get(doc_id='1')` is called, it returns the document (existing behavior to be preserved).

## Assumptions and open questions
- **Assumption (ASM-1):** The stakeholder's request for consistency with `get()` implies that string IDs should be coerced to integers if the underlying storage uses integer keys. This answers the question of how to handle type mismatch between the input string and the internal integer ID.
- **Assumption (ASM-2):** Non-numeric strings (e.g., `doc_ids=['abc']`) should continue to return an empty list silently rather than crashing, as the stakeholder stated they "do not want to crash on every bad input".