# Spec: Support string document IDs in update() and remove()

## Source
Issue #2: "update() and remove() silently do nothing when I pass the doc id as a string"
- "`db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged."
- "Passing the int `1` instead of `'1'` works. My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds. Please make these consistent with `get` (which accepts the string form)."

## Requirements
- **FR-1**: When `Table.update()` is called with `doc_ids` containing string document IDs (e.g., `doc_ids=['1']`), the method shall update the documents matching those integer IDs and return the list of updated document IDs.
- **FR-2**: When `Table.remove()` is called with `doc_ids` containing string document IDs (e.g., `doc_ids=['1']`), the method shall remove the documents matching those integer IDs and return the list of removed document IDs.

## Acceptance criteria
- Given a database containing a document with ID 1, when `db.update({'x': 2}, doc_ids=['1'])` is executed, then the document with ID 1 is updated to `{'x': 2}` and `[1]` is returned.
- Given a database containing a document with ID 1, when `db.remove(doc_ids=['1'])` is executed, then the document with ID 1 is removed and `[1]` is returned.
- Given a database containing a document with ID 1, when `db.update({'x': 2}, doc_ids=['1'])` is executed, then `db.get(doc_id='1')` returns `{'x': 2}`.

## Assumptions and open questions
- Assumption: Passing string IDs that cannot be converted to integer IDs (or do not match existing integer IDs) should behave consistently with passing non-existent integer IDs (i.e. return an empty list without crashing).
- Default chosen: Rely on standard string-to-int ID handling consistent with `get()` behavior.
