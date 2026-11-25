# Spec: Prevent Mutation of Stored Documents via Returned Search Results

## Source
Issue #39: "Searches sometimes return data that doesn't match what's in the db??"
- "Sometimes a search returns documents with values that are NOT what's stored."
- "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-1: The system shall return copies of documents from search and retrieval methods so that in-place modification of the returned objects does not affect the internal database state or subsequent queries.
- FR-2: The system shall ensure that the file-on-disk remains unmodified by in-memory edits to search results unless an explicit update operation is called.

## Acceptance criteria
- Given a table with one document `{'key': 'original'}`, When `table.search()` is called and the resulting dictionary is modified to `{'key': 'edited'}`, Then a subsequent `table.search()` call returns `{'key': 'original'}`.
- Given a document retrieved from `table.all()`, When comparing the object identity of the result to the internal storage reference, Then the result must be a distinct object instance (e.g., `id(result) != id(internal_doc)`).

## Assumptions and open questions
- **Assumption (ASM-1):** The user's request for "normal dicts" implies standard Python dictionary objects that do not maintain a live link to the database's internal cache. This is chosen as the default to resolve the reported "caching bug" (S-07).
- **Open Question:** Does this requirement apply to nested objects within the document? **Default:** Yes, deep copies are assumed to be required to prevent side effects in nested structures.
