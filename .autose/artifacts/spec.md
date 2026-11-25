# Spec: Untrusted Data / Query Result Side Effects in Search
## Source
Issue #39: "Searches sometimes return data that doesn't match what's in the db??"
- Quoted key sentences: "Sometimes a search returns documents with values that are NOT what's stored." / "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything. It's like tinydb remembers my display edits." / "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-001: The table query and retrieval methods shall return deep copies of documents so that mutations to returned dictionaries do not affect internal database storage or subsequent search results.

## Acceptance criteria
- Given a document is stored in the database, When a user retrieves the document via search or all and modifies the returned dictionary, Then subsequent searches for the document return the original stored values without modification.

## Assumptions and open questions
- Question Q-1: What is the acceptable performance overhead limit for returning copies of search results? 
  - Default chosen: 10% overhead maximum for up to 10,000 documents.
  - Why: Necessary to establish a non-functional performance baseline for copying overhead without stakeholder feedback.
