# Spec: Fix update and remove silent no-op when doc_ids are passed as strings

## Source
Issue #2: update() and remove() silently do nothing when I pass the doc id as a string.
> `db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged.

## Requirements
- FR-001: The `Table.update` method shall successfully match and update documents when `doc_ids` contains string representations of valid document IDs.
- FR-002: The `Table.remove` method shall successfully match and remove documents when `doc_ids` contains string representations of valid document IDs.
- FR-003: The `Table.update` and `Table.remove` methods shall return the list of modified/removed document IDs correctly when string-form IDs are provided.
- FR-004: The `Table.update` and `Table.remove` methods shall continue to silently skip non-existent document IDs without raising exceptions when invalid or missing IDs are passed.
- NFR-001: ID coercion and lookup behavior in `update` and `remove` with `doc_ids` shall be consistent with `get(doc_ids=...)` by converting supplied IDs using `self.document_id_class` or `str` normalization.

## Acceptance criteria
- Given a TinyDB table containing a document with ID `1`, when `table.update({'x': 2}, doc_ids=['1'])` is executed, then the document with ID `1` is updated to have `{'x': 2}` and `['1']` or `[1]` is returned (depending on document_id_class).
- Given a TinyDB table containing a document with ID `1`, when `table.remove(doc_ids=['1'])` is executed, then the document with ID `1` is removed from the table and the ID is returned in the removed list.
- Given an empty TinyDB table, when `table.update({'x': 2}, doc_ids=['999'])` or `table.remove(doc_ids=['999'])` is executed, then `[]` is returned and no exception is raised.

## Assumptions and open questions
- Assumption: Document IDs passed as strings should be coerced using `self.document_id_class` (or normalized to strings matching table keys, identically to `get(doc_ids=...)`), because TinyDB's internal storage keys are strings and `get()` already coerces/normalizes them.