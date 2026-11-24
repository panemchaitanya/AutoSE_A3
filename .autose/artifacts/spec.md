# Spec: TinyDB search limit parameter

## Source
- GitHub issue #37: "Add a limit parameter to search()"
- Quoted key sentences:
  - `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful.
  - Could `search` take an optional `limit`?
  - `limit=None` (default) keeps today's behavior - all matches, in document id order.
  - `limit=N` returns at most the first N matches, in document id order.
  - A limit larger than the number of matches just returns all matches.

## Requirements
- FR-001: The `search()` method on Table shall accept an optional `limit` parameter defaulting to `None`.
- FR-002: When `limit` is `None`, `search()` shall return all matching documents in document id order.
- FR-003: When `limit` is set to an integer $N \geq 0$, `search()` shall return at most the first $N$ matching documents in document id order.
- NFR-001: Search execution with `limit=N` shall execute correctly and retrieve at most $N$ matching documents without breaking existing search correctness or ordering.

## Acceptance criteria
- Given a table with documents, when `db.search(cond)` is called without `limit`, then it executes successfully without error.
- Given a table with documents, when `db.search(cond, limit=5)` is called with an integer limit, then it executes successfully without error.
- Given a table containing 15 matching documents, when `db.search(cond, limit=None)` is called, then all 15 matching documents are returned in document id order.
- Given a table containing 15 matching documents, when `db.search(cond, limit=5)` is called, then exactly the first 5 matching documents are returned in document id order.
- Given a table containing 3 matching documents, when `db.search(cond, limit=10)` is called, then all 3 matching documents are returned in document id order.
- Given a table containing matching documents, when `db.search(cond, limit=0)` is called, then an empty list is returned.
- Given a table with 10,000 matching documents, when `db.search(cond, limit=10)` is executed, then the execution completes and returns exactly 10 matching documents in document id order.

## Assumptions and open questions
- ASM-1: Negative limits ($N < 0$) are not expected or supported; passing negative limits raises a ValueError or returns empty list per standard Python slicing/limit conventions. (Answers Q-1: How should negative limits be handled? Default chosen as standard behavior since issue specifies $N \geq 0$.)
- Q-1 [OPEN]: Should negative integer limits raise ValueError or return an empty list? Default chosen as standard Python slice/range handling, keeping NFR-001 at CLARIFY.