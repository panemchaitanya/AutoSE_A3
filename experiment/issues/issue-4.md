# Issue 4 (feature request) - posted to the fork on GitHub

Title: Let get() take a default value, like dict.get

Body:

`db.get(...)` returns `None` when nothing matches. In most of my code paths
`None` is not a usable value, so I end up writing

```python
doc = db.get(doc_id=some_id) or {}
```

which is easy to forget and also wrong for any falsy document content edge
cases I might hit later. It would be cleaner if `get` accepted a default,
the way `dict.get` does:

```python
db.get(doc_id=42, default={})        # {} instead of None when missing
db.get(Query().name == 'x', default={})
```

Behavior when the call does match should be exactly what it is today, and
omitting `default` should keep returning `None`. Ideally this works for all
the ways of calling get: by condition, by `doc_id`, and by `doc_ids` (for
`doc_ids`, the default would apply to the list result only in the sense that
today's empty-list behavior is already fine - no change needed there; the
default matters for the single-document calls).
