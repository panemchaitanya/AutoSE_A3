# Register: TinyDB Search Result Mutability and Caching Isolation (v1)

## A. Source Statements
- S-01: "Sometimes a search returns documents with values that are NOT what's stored."
- S-02: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-03: "It's like tinydb remembers my display edits."
- S-04: "If I restart the script the data is fine again, so the file itself is OK."
- S-05: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-06: "Is this a caching bug?"
- S-07: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## B. Ambiguous Terms
- AMB-1: "normal dicts you can safely edit without side effects" (S-07)
  - Candidate meanings: (1) Returning a shallow copy of the Document dict, (2) Returning a deep copy of the Document dict, (3) Returning immutable mapping views.
  - Design decision forced: Must decide whether shallow or deep copies are required to prevent nested dictionary/list mutations from affecting internal cache.

## C. Open Questions
- Q-1: Does returning deep copies on every search/all retrieval introduce measurable performance overhead for large datasets? 
  - Why it matters: Performance impact on large databases.
  - Blocks ids: NFR-001
  - Score: 1
  - Default if unanswered: Accept standard python `copy.deepcopy` semantics as expected for safe isolation.
  - Owner: Maintainer / Issue Reporter
  - Status: OPEN

## D. Assumptions
- ASM-1: Deep copies are necessary to fully isolate nested mutable structures inside document dictionaries (linked to Q-1).

## E. Conflicts
- None identified.

## F. Evidence Log
- EV-1: Repository inspection of `tinydb/table.py` confirms that table caching or stored document references are returned directly without defensive copying.
  - Tool: Repository analysis (A3 repository-local analysis, no MCP used)
  - Effect on spec: Confirms DEP-1 and establishes technical basis for FR-001 and FR-002.

## G. Coverage Matrix
- Users and roles: COVERED (ACT-1, ACT-2)
- Core capabilities: COVERED (FR-001, FR-002)
- Data: COVERED (CON-1, CON-2)
- Integrations: N/A (pure Python embedded library)
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: COVERED (NFR-001)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: N/A
- Maintainability and extensibility: N/A
- Autonomy and human oversight: N/A
- Success measures: COVERED (AC-001-1, AC-001-2, AC-002-1)
- Scope exclusions: COVERED (disk storage correctness preserved per CON-1)
- Delivery constraints: UNSET

## H. Change Log
- v1.0 initial baseline specification from issue #39.
