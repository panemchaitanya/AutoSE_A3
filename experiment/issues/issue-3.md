# Issue 3 (feature request) - posted to the fork on GitHub

Title: Add a limit parameter to search()

Body:

`db.search(cond)` always returns every match. When a table has thousands of
documents and I only need the first few (a "latest 10" list, a preview,
pagination), I have to materialize the whole result list and slice it
myself, which is wasteful.

Could `search` take an optional `limit`?

```python
db.search(Query().category == 'book', limit=10)   # first 10 matches only
db.search(Query().category == 'book')             # unchanged: all matches
```

Expected semantics:

- `limit=None` (default) keeps today's behavior - all matches, in document
  id order.
- `limit=N` returns at most the first N matches, in document id order.
- A limit larger than the number of matches just returns all matches.

Thanks!
