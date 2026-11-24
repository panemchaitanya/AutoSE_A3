# Spec: TinyDB db.get() Default Value Support

## Source
GitHub issue #38 requesting default value support for `db.get()`:
> `db.get(...)` returns `None` when nothing matches. In most of my code paths `None` is not a usable value, so I end up writing `doc = db.get(doc_id=some_id) or {}` ... It would be cleaner if `get` accepted a default, the way `dict.get` does: `db.get(doc_id=42, default={})`. Behavior when the call does match should be exactly what it is today, and omitting `default` should keep returning `None`.

## Requirements
- FR-001: The database and table `get()` method shall accept an optional `default` keyword argument.
- FR-002: When `get()` is invoked with a query or `doc_id` and no matching document is found, it shall return the specified `default` value instead of `None`.
- FR-003: When `get()` is invoked with a query or `doc_id` and a matching document is found, it shall return the matched document data.
- FR-004: When `get()` is invoked without the `default` keyword argument and no matching document is found, it shall return `None`.

## Acceptance criteria
- Given a TinyDB database instance `db`, When `db.get(doc_id=42, default={})` is called, Then the method accepts `default={}` without raising a TypeError.
- Given a TinyDB table with no matching document for `doc_id` 999, When `db.get(doc_id=999, default="missing")` is executed, Then the return value equals `"missing"`.
- Given a TinyDB table with no matching document for `Query().name == 'nonexistent'`, When `db.get(Query().name == 'nonexistent', default={})` is executed, Then the return value equals `{}`.
- Given a TinyDB table containing document id 42 with data `{"name": "test"}`, When `db.get(doc_id=42, default={})` is executed, Then the return value equals `{"name": "test"}`.
- Given a TinyDB table with no matching document for `doc_id` 999, When `db.get(doc_id=999)` is executed, Then the return value is `None`.
- Given existing code calling `db.get(doc_id=42)` without default, When executed, Then it functions identically to current behavior.

## Assumptions and open questions
- Assumption: The `default` parameter applies only to single-document retrieval calls (`doc_id` and query matching) and does not alter multi-document `doc_ids` list-returning behavior. Chosen because the issue explicitly states that `doc_ids` empty-list behavior is already fine and requires no change.