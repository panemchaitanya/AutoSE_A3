# Spec: Add limit parameter to search()
## Source
Issue #37: Add a limit parameter to search()
> `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. Could `search` take an optional `limit`?

## Requirements
- FR-1: The `search` method shall accept an optional `limit` parameter.
- FR-2: If `limit` is `None`, the system shall return all matches.
- FR-3: If `limit` is an integer `N`, the system shall return at most the first `N` matches in document ID order.
- FR-4: If `limit` is larger than the number of matches, the system shall return all matches.

## Acceptance criteria
- Given a Table instance, when `search` is called with `limit=10`, then the call executes successfully.
- Given a table with 5 matching documents, when `search(cond, limit=None)` is called, then all 5 documents are returned.
- Given a table with 100 matching documents, when `search(cond, limit=5)` is called, then exactly 5 documents are returned in document ID order.
- Given a table with 3 matching documents, when `search(cond, limit=10)` is called, then all 3 matching documents are returned.

## Assumptions and open questions
- Assumption: Cache key management and query caching must account for the `limit` parameter or be appropriately bypassed/keyed when `limit` is specified. Chosen default: key cache entries by `(cond, limit)` or bypass caching when `limit` is present, to prevent returning truncated cached results for unrestricted searches. Linked to Q-1 (implicit cache invalidation question).