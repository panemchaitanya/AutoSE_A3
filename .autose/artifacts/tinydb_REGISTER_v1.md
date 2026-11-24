# Register: TinyDB Safe Search Retrieval (v1)

## A. Source Statements
- S-01: "Sometimes a search returns documents with values that are NOT what's stored."
- S-02: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-03: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## B. Ambiguous Terms
- AMB-1: "tweak the returned dicts a bit for display purposes" -> Candidate meanings: 1. In-place dictionary mutation; 2. Returning wrapped objects. Resolution: Handled by ensuring retrieved dicts are deep copies.

## C. Open Questions
*(None)*

D. Assumptions
- ASM-1 (links to S-03): Deep-copying dictionaries upon retrieval is the intended mechanism to prevent side effects.

## E. Conflicts
*(None)*

F. Evidence Log
- EV-1: A3 repository-local analysis (no MCP used). TinyDB stores documents in an in-memory table cache/list referenced directly by search and retrieval methods.

G. Coverage Matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-1)
- Data/Caching: COVERED (CON-1, FR-1)

H. Change Log
- v1 initial draft.
