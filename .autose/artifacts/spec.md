# Spec: Prevent search and query results from retaining in-memory mutations across calls
## Source
"Searches sometimes return data that doesn't match what's in the db?? ... I search for something, tweak the returned dicts a bit for display purposes ..., and later when I run the SAME search again the old tweaked values show up even though I never called update or anything." (Issue #6)

## Requirements
- FR-1: The search and retrieval methods (such as search, all, get) shall return deep copies or freshly constructed dictionary representations of stored documents such that subsequent mutations performed on returned dictionaries do not mutate the internal database cache or storage state.

## Acceptance criteria
- Given a document stored in TinyDB with a field value ``"original"``, when a user queries the document using ``search()`` or ``all()`` and modifies a field in the returned dictionary object to ``"modified"`` without calling any update method, then subsequent calls to ``search()`` or ``all()`` shall return dictionaries where the field value remains ``"original"``.

## Assumptions and open questions
- Assumption: Returning deep copies (or isolating returned dictionaries) will not introduce unacceptable performance degradation, chosen because correctness and prevention of side effects take precedence over raw object reference sharing.