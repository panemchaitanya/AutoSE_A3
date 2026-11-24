# Spec: TinyDB Safe Search Retrieval

## Source
GitHub Issue #6: "Sometimes a search returns documents with values that's not what's stored." 
Quotes: 
- "Sometimes a search returns documents with values that are NOT what's stored."
- "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-1: The database retrieval methods (`search` and `all`) shall return unshared copy instances of document dictionaries such that modifying a returned dictionary does not mutate cached database documents.

## Acceptance criteria
- Given a document stored in a TinyDB table, when a user calls `search()` or `all()`, modifies a field of a returned document dictionary in place, and subsequently executes `search()` for the same document, then the newly returned dictionary contains the original stored value and not the modified value.
- Given a document stored in a TinyDB table, when a user retrieves a document via `search()`, modifies a field in place, and subsequently retrieves all documents via `all()`, then the dictionary returned by `all()` contains the original stored value.

## Assumptions and open questions
- ASM-1: Deep-copying dictionaries upon retrieval is the chosen design default to prevent unintended in-place mutation side effects on database storage/caches. (Answers Q-1: How should side effects from modifying returned dicts be prevented?)
