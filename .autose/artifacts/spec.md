# Spec: TinyDB Document Mutability and Caching Prevention

## Source
Issue #39: Searches sometimes return data that doesn't match what's in the db??
- Quoted key sentences:
  - "Sometimes a search returns documents with values that are NOT what's stored."
  - "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
  - "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-001: The database search and all retrieval methods shall return independent copies or non-aliased dictionaries of stored documents such that in-memory modifications to returned objects do not mutate internal table cache or subsequent query results.
- CON-1: The underlying storage file must remain unaffected by in-memory edits to returned query/search results unless an explicit update/insert method is called.
- NFR-001: Document retrieval operations shall not introduce latency exceeding TBD relative to current uncopied retrieval performance.

## Acceptance criteria
- Given a document stored in TinyDB, When a user executes a search or retrieves all documents, modifies the returned dictionary object in memory without calling update, and executes the same search again, Then the search results reflect the original stored values rather than the modified display values.
- Given large datasets retrieved via search, When measuring execution time of retrieval methods with copying enabled, Then the execution time per returned document does not exceed TBD milliseconds as defined in Q-01.

## Assumptions and open questions
- Question Q-01: What is the acceptable performance overhead threshold for deep copying returned document dictionaries? Default chosen: negligible overhead (< 5ms per 1000 docs), because standard dict copying in Python is highly efficient and correctness of retrieval isolation takes precedence.