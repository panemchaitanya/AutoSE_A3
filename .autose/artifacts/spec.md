# Spec: TinyDB In-Memory Document Mutation Leak Prevention

## Source
GitHub Issue #39: "Searches sometimes return data that doesn't match what's in the db??"
> "Example: I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything. It's like tinydb remembers my display edits."
> "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## Requirements
- FR-001: The search and all methods on Table shall return isolated copies of documents so subsequent in-place modifications to returned dictionaries do not affect stored or subsequently retrieved documents within the same run.

## Acceptance criteria
- Given a document stored in TinyDB, When a user performs a search or gets all documents, mutates the returned dictionary object in-place, and performs the same search again, Then the newly retrieved search results reflect the original stored database state rather than the in-place mutated dictionary.

## Assumptions and open questions
- Question (Q-001): What is the acceptable performance overhead threshold for copying documents returned by search and all?
- Assumption (ASM-001): Document isolation overhead should be minimal and bounded. Default: Performance overhead shall not exceed TBD percentage over baseline search execution time.
