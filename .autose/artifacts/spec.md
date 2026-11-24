# Spec: TinyDB Search Limit
## Source
- GitHub Issue #37: Add a limit parameter to search()
- "Could search take an optional limit?"
- "db.search(Query().category == 'book', limit=10) # first 10 matches only"

## Requirements
- FR-1: The search method shall accept an optional limit parameter defaulting to None.
- FR-2: When limit is None, search shall return all matching documents in document id order.
- FR-3: When limit is set to an integer N, search shall return at most the first N matching documents in document id order.
- FR-4: When limit is larger than the total number of matches, search shall return all matching documents without error.

## Acceptance criteria
- Given a Table instance, when calling search with no limit argument, then it executes successfully using limit=None.
- Given a table with multiple matching documents, when calling search(cond, limit=None), then all matching documents are returned in ascending document id order.
- Given a table with matching documents exceeding N, when calling search(cond, limit=N) where N is a positive integer, then at most N matching documents are returned in ascending document id order.
- Given a table with fewer than N matching documents, when calling search(cond, limit=N), then all matching documents are returned.

## Assumptions and open questions
- Question (Q-1): What should happen if a negative integer or zero is passed as limit? Default assumed: negative/zero limit follows standard slicing behavior or returns an empty list, linked to ASM-1.
