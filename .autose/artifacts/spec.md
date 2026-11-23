# Spec: Add a limit parameter to search()

## Source
Issue #4: `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. Could `search` take an optional `limit`?

## Requirements
- FR-1: The table search method and database search method shall accept an optional keyword parameter `limit`.
- FR-2: When `limit` is `None`, search shall return all matching documents in document ID order.
- FR-3: When `limit` is an integer `N`, search shall return at most the first `N` matching documents in document ID order.
- FR-4: When `limit` is an integer larger than the total number of matching documents, search shall return all matching documents.

## Acceptance criteria
- Given a table containing multiple documents matching a condition, When `db.search(cond, limit=2)` is invoked, Then exactly the first 2 matching documents in document ID order are returned.
- Given a table containing matching documents, When `db.search(cond, limit=None)` or `db.search(cond)` is invoked, Then all matching documents in document ID order are returned.
- Given a table containing fewer matching documents than the specified limit, When `db.search(cond, limit=100)` is invoked, Then all available matching documents are returned without error.

## Assumptions and open questions
- Assumption: Negative or zero limits are not specified by the issue; standard slicing behavior or returning empty list/all documents is not requested, so we assume standard positive integer limits `N >= 0` or `None`. (Default chosen: standard Python-like or explicit truncation up to N matches).