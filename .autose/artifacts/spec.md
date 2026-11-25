# Spec: TinyDB String Document IDs in Update and Remove

## Source
- GitHub issue #35: "`db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged. Passing the int `1` instead of `'1'` works. My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds. Please make these consistent with `get` (which accepts the string form)."

## Requirements
- FR-001: The table `update` method shall accept string representations of document IDs in `doc_ids` (or convert/normalize them consistently with `get`) so that update operations succeed when string IDs are passed.
- FR-002: The table `remove` method shall accept string representations of document IDs in `doc_ids` (or convert/normalize them consistently with `get`) so that remove operations succeed when string IDs are passed.
- NFR-001: Error handling and type conversion for `doc_ids` in `update` and `remove` shall be consistent with `get`.

## Acceptance criteria
- Given a table containing a document inserted with integer ID `1`, When `db.update({'x': 2}, doc_ids=['1'])` is executed, Then the document is successfully updated and the returned list contains the matched ID type/value consistently.
- Given a table containing a document inserted with integer ID `1`, When `db.update({'x': 2}, doc_ids=[1])` is executed, Then the document is successfully updated.
- Given a table containing a document inserted with integer ID `1`, When `db.remove(doc_ids=['1'])` is executed, Then the document is successfully removed and the table length becomes 0.
- Given a table containing a document inserted with integer ID `1`, When `db.remove(doc_ids=[1])` is executed, Then the document is successfully removed.
- Given `get`, `update`, and `remove` methods accepting `doc_ids`, When string IDs are supplied across all three methods, Then all three methods handle string ID normalization identically without silent no-ops.

## Assumptions and open questions
- Assumption (linked to Q-1): Non-existent IDs passed in `doc_ids` to `update` and `remove` continue to be silently ignored, matching existing behavior for integer IDs.
