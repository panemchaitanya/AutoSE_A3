# Spec: Fix Query Cache Document Mutation Side Effects (Issue #39)

## Source
Issue #39: Searches sometimes return documents with values that don't match what's stored in the database due to in-place mutation of search results within a single run.
- Quote: "Sometimes a search returns documents with values that are NOT what's stored."
- Quote: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- Quote: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-001: The Table.search method shall return documents that are safe to mutate without causing side effects on subsequent searches or cached internal state within the same run.
- FR-002: The query cache or document retrieval mechanism shall return deep copies or independent copies of documents so that external modifications to returned dictionary structures do not corrupt cached query results.

## Acceptance criteria
- Given a table containing documents, When a user performs a search, modifies a field in the returned document dictionaries, and then performs the identical search again during the same runtime, Then the returned documents reflect the original stored database values rather than the modified display values.
- Given a table with cached search results, When a returned document from search is mutated in place, Then the internal cache retains unmodified data and subsequent search calls return uncorrupted data.

## Assumptions and open questions
- Assumption: Performance overhead of deep copying search results is negligible for typical TinyDB usage or acceptable relative to correctness (Default chosen to prioritize data correctness and prevent silent cache corruption, linked to Q-1).
- Open Question: What is the acceptable performance threshold for deep copying search results? (Blocks NFR-001).
