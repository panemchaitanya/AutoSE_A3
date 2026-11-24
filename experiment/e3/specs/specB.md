# Spec: TinyDB Missing Field Operations

## Source
Issue #3: increment() crashes with KeyError when the field does not exist yet.
> "I'm using `tinydb.operations.increment` for a page-view counter. The first time a page is viewed the document has no `count` field yet, and instead of just starting the counter at 1, TinyDB blows up... I would expect a counter on a missing field to simply start from 0... Same goes for `add` and `subtract`"

## Requirements
- FR-001: The increment operation shall initialize a missing field to 0 before incrementing by 1.
- FR-002: The decrement operation shall initialize a missing field to 0 before decrementing by 1.
- FR-003: The add operation shall initialize a missing field to 0 before adding the specified value `n`.
- FR-004: The subtract operation shall initialize a missing field to 0 before subtracting the specified value `n`.

## Acceptance criteria
- Given a document without the field 'count', When update(increment('count')) is executed, Then the document shall have 'count' set to 1.
- Given a document without the field 'count', When update(decrement('count')) is executed, Then the document shall have 'count' set to -1.
- Given a document without the field 'score', When update(add('score', 5)) is executed, Then the document shall have 'score' set to 5.
- Given a document without the field 'score', When update(subtract('score', 3)) is executed, Then the document shall have 'score' set to -3.

## Assumptions and open questions
- Assumption: Missing fields for arithmetic update operations default to 0 to align with standard accumulator behavior (Chosen because defensive insertion of 0 defeats the point of built-in operations).
