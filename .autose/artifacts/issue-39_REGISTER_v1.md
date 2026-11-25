# Register: TinyDB Document Mutability and Caching Prevention (v1)

## A. Source statements
- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything."
- S-04: "It's like tinydb remembers my display edits."
- S-05: "If I restart the script the data is fine again, so the file itself is OK."
- S-06: "It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?)."
- S-07: "Is this a caching bug?"
- S-08: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## B. Ambiguous terms
- AMB-1: "caching bug" -> Candidate meanings: (1) In-memory reference caching storing retrieved documents directly; (2) Persistent query result cache. Decision forced: determines whether fixing table-level retrieval references or query caching is needed.

## C. Open questions
- Q-01: What is the acceptable performance overhead threshold for deep copying returned document dictionaries? | Why it matters: Impacts large dataset retrieval performance | Blocks: NFR-001 | Score: 1 | Default: negligible overhead (< 5ms per 1000 docs) | Owner: Maintainer | Status: OPEN

## D. Assumptions
- ASM-01: The performance overhead of copying returned documents is acceptable for normal usage. | Linked Q: Q-01

## E. Conflicts
- None

## F. Evidence log
- EV-01: A3 repository-local analysis of tinydb/table.py shows documents are returned by reference from internal cache/storage lists without defensive copying.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001)
- Data: COVERED (CON-1)
- Integrations: N/A (pure library)
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: OPEN (NFR-001, Q-01)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: N/A
- Maintainability and extensibility: COVERED
- Autonomy and human oversight: N/A
- Success measures: COVERED
- Scope exclusions: N/A
- Delivery constraints: N/A

## H. Change log
- v1 initial draft
