# Spec: Add default value parameter to db.get()

## Source
GitHub Issue #5: "Let get() take a default value, like dict.get"
> db.get(...) returns None when nothing matches. In most of my code paths None is not a usable value... It would be cleaner if get accepted a default, the way dict.get does: db.get(doc_id=42, default={}) # {} instead of None when missing

## Requirements
- FR-1: The database `get` method shall accept an optional `default` parameter across all query invocation methods (by `doc_id`, by query condition, and by `doc_ids`). (Stated)
- FR-2: When a single-document `get` call (via `doc_id` or query condition) finds no matching record, the method shall return the value provided to the `default` parameter instead of `None`. (Stated)
- FR-3: When the `default` parameter is omitted in single-document `get` calls and no record matches, the method shall continue to return `None`. (Stated)
- FR-4: When a single-document `get` call successfully matches a record, the method shall return the matched document regardless of whether a `default` parameter was provided. (Stated)
- FR-5: When multi-document `get` calls (`doc_ids`) are used, the presence or absence of the `default` parameter shall not alter the existing empty-list or multi-result behavior for missing matches. (Stated)

## Acceptance criteria
- Given a database containing no document with `doc_id=42`, When calling `db.get(doc_id=42, default={})`, Then the return value equals `{}`.
- Given a database containing no document matching `Query().name == 'x'`, When calling `db.get(Query().name == 'x', default=[])`, Then the return value equals `[]`.
- Given a database containing a document with `doc_id=42` containing `{'a': 1}`, When calling `db.get(doc_id=42, default={})`, Then the return value equals `{'a': 1}`.
- Given a database containing no document with `doc_id=42`, When calling `db.get(doc_id=42)`, Then the return value is `None`.
- Given a database containing no documents for a list of IDs `[1, 2]`, When calling `db.get(doc_ids=[1, 2], default={})`, Then the return value equals `[]`.

## Assumptions and open questions
- ASM-1: The parameter name for the default fallback value is strictly `default` matching `dict.get` conventions (Assumed based on issue text).
