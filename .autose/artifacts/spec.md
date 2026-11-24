# Spec: TinyDB increment/add/subtract missing field handling

## Source
Issue #36: "increment() crashes with KeyError when the field does not exist yet"
"I'm using tinydb.operations.increment for a page-view counter. The first time a page is viewed the document has no count field yet, and instead of just starting the counter at 1, TinyDB blows up: KeyError: 'count'"

## Requirements
- FR-001: The increment operation shall treat a missing field as having an initial numeric value of 0 when applied to a document, resulting in a value of n.
- FR-002: The add operation shall treat a missing field as having an initial numeric value of 0 when applied to a document, resulting in the added amount.
- FR-003: The subtract operation shall treat a missing field as having an initial numeric value of 0 when applied to a document, resulting in the negative of the subtracted amount.

## Acceptance criteria
- Given a document without a 'count' field, when db.update(increment('count'), doc_ids=[1]) is executed, then the document shall be updated to include 'count': 1.
- Given a document without a 'count' field, when db.update(increment('count', n=5), doc_ids=[1]) is executed, then the document shall be updated to include 'count': 5.
- Given a document without a 'val' field, when db.update(add('val', 5), doc_ids=[1]) is executed, then the document shall be updated to include 'val': 5.
- Given a document without a 'val' field, when db.update(subtract('val', 3), doc_ids=[1]) is executed, then the document shall be updated to include 'val': -3.

## Assumptions and open questions
- Assumption (ASM-001, answering Q-1): Missing fields in numeric update operations should behave as if initialized to 0 to provide intuitive counter behaviors without requiring defensive insertions.
