# Spec: Add a limit parameter to search()

## Source
GitHub issue #37: "Add a limit parameter to search()".
> `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. Could `search` take an optional `limit`?

## Requirements
- FR-1: The database search function shall accept an optional `limit` parameter defaulting to `None` [S-02, S-05].
- FR-2: The database search function shall return all matching documents in document ID order when `limit` is `None` [S-05].
- FR-3: The database search function shall return at most the first N matching documents in document ID order when `limit` is set to an integer N [S-06].
- FR-4: The database search function shall return all matching documents in document ID order when `limit` is greater than the total number of matches [S-07].

## Acceptance criteria
- Given a table with documents, when `db.search(cond)` is called without `limit`, then it executes successfully and returns all matching documents in document ID order.
- Given a table with documents, when `db.search(cond, limit=10)` is called, then it executes successfully.
- Given a query matching 5 documents in a table, when `db.search(cond, limit=2)` is called, then exactly the first 2 matching documents are returned in document ID order.
- Given a query matching 3 documents in a table, when `db.search(cond, limit=10)` is called, then all 3 matching documents are returned in document ID order.
- Given a table where no documents match the query, when `db.search(cond, limit=5)` is called, then an empty list is returned.

## Assumptions and open questions
- Assumption: `limit` must be a non-negative integer or `None` (linked to Q-1, Q-2).
- Open Question: Should negative or non-integer `limit` values raise a `ValueError` or return empty collections? Default chosen for specification scope is standard non-negative integer parameter handling as specified by issue examples.
