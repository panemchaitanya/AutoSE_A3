# Spec: Let get() take a default value, like dict.get

## Source
Issue #5: Let get() take a default value, like dict.get
> "`db.get(...)` returns `None` when nothing matches. In most of my code paths `None` is not a usable value... It would be cleaner if `get` accepted a default, the way `dict.get` does: `db.get(doc_id=42, default={})`, `db.get(Query().name == 'x', default={})`. Behavior when the call does match should be exactly what it is today, and omitting `default` should keep returning `None`."

## Requirements
1. FR-1: `Table.get` shall support an optional `default` keyword parameter (or positional default if applicable) when querying single documents by condition or by `doc_id`.
2. FR-2: When no document matches a single-document `Table.get` query and `default` is provided, `Table.get` shall return the provided `default` value.
3. FR-3: When no document matches a single-document `Table.get` query and `default` is omitted, `Table.get` shall return `None`.
4. FR-4: When a document matches a single-document `Table.get` query, `Table.get` shall return the matched document object regardless of whether `default` is specified.
5. FR-5: `Table.get` queries using `doc_ids` shall retain their existing behavior returning a list of matched documents (or an empty list if none match), without modification by single-document `default` handling.

## Acceptance criteria
- Given a table without a document with `doc_id=42`, when calling `db.get(doc_id=42, default={})`, then the returned value is `{}`.
- Given a table without a document matching `Query().name == 'x'`, when calling `db.get(Query().name == 'x', default=[])`, then the returned value is `[]`.
- Given a table without a document with `doc_id=42`, when calling `db.get(doc_id=42)`, then the returned value is `None`.
- Given a table containing document `{'id': 1, 'name': 'test'}` with `doc_id=1`, when calling `db.get(doc_id=1, default={})`, then the returned value is `{'id': 1, 'name': 'test'}`.
- Given a table with documents with `doc_id` 1 and 2, when calling `db.get(doc_ids=[99])`, then the returned value is `[]`.

## Assumptions and open questions
- Question: Should `doc_ids` queries use `default`?
  - Default: No. The issue explicitly specifies: "for `doc_ids`, the default would apply to the list result only in the sense that today's empty-list behavior is already fine - no change needed there; the default matters for the single-document calls".
- Question: What should default to if `default` is not passed?
  - Default: `None`, matching Python `dict.get` standard semantics and current TinyDB behavior.
