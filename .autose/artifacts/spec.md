# Spec: TinyDB Search Result Mutability and Caching Isolation

## Source
Issue #39: Searches sometimes return data that doesn't match what's in the db??
- Quoted key sentences: 
  - "Sometimes a search returns documents with values that are NOT what's stored."
  - "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
  - "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-1: The database search method (`search`) shall return independent copies of documents such that in-place mutations of returned document dictionaries do not affect subsequent searches or internal table storage within the same run.
- FR-2: The database retrieval methods (`all`, `get`) shall return independent copies of documents such that in-place mutations do not persist or bleed into subsequent retrievals or internal table state.
- CON-1: The underlying stored database file itself must remain unaffected and correct on disk when search/all results are mutated in memory.

## Acceptance criteria
- Given a table containing a document with field value 'abc', When a user searches for the document, modifies the returned dictionary field in place to 'xyz', and searches for the same document again in the same run, Then the second search returns the document with the original stored value 'abc' rather than the modified value 'xyz'.
- Given a table containing a document, When a search returns a document dictionary, Then modifying nested keys or values of the returned dictionary has no effect on subsequent query results or internal storage cache.
- Given a table containing documents, When `all()` or `get()` is called, Then modifying the returned dictionary objects does not mutate the internal table data or subsequent calls to `all()` or `get()`.
- Given a table containing a document dictionary with up to 100 nested key-value pairs, When `search()` is executed 1,000 times consecutively, Then the total elapsed execution time overhead introduced by defensive copying remains proportional to O(N * D) where N is result count and D is document depth/size, completing successfully without throwing memory or recursion exceptions.

## Assumptions and open questions
- Q-1: Does returning deep copies on every search/all retrieval introduce measurable performance overhead for large datasets? Default chosen: Accept standard python `copy.deepcopy` semantics as expected for safe isolation, with performance impact assumed negligible or acceptable until benchmarked.
- ASM-1: Deep copies are necessary to fully isolate nested mutable structures inside document dictionaries (linked to Q-1).
