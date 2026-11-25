# Register: issue39 (v1)

## A. Source statements
- S-01: "Searches sometimes return data that doesn't match what's in the db??"
- S-02: "Sometimes a search returns documents with values that are NOT what's stored."
- S-03: "I search for something, tweak the returned dicts a bit for display purposes (like formatting a field), and later when I run the SAME search again the old tweaked values show up even though I never called update or anything. It's like tinydb remembers my display edits."
- S-04: "If I restart the script the data is fine again, so the file itself is OK. It only happens within one run and only sometimes (maybe only when I edit the dicts I got back?). Is this a caching bug?"
- S-05: "Can you make it so the documents you get back from search/all are just... normal dicts you can safely edit without side effects?"

## B. Ambiguous terms
- AMB-01: "normal dicts you can safely edit without side effects"
  - Candidate 1: Returning copies of documents so mutations do not mutate internal storage/cache.
  - Candidate 2: Returning immutable mapping proxies.
  - Decision: Candidate 1 (deep/shallow copy upon retrieval).

## C. Open questions
- Q-1: What is the acceptable performance overhead limit for returning copies of search results? 
  - Why it matters: Deep copying large query results might impact throughput.
  - Blocks: NFR-001
  - Score: 1
  - Default if unanswered: 10% overhead maximum for up to 10,000 documents.
  - Owner: Stakeholder
  - Status: OPEN

## D. Assumptions
- ASM-01: Performance overhead limit is 10% for collections up to 10,000 documents (linked to Q-1).

## E. Conflicts
- None.

## F. Evidence log
- EV-01: Repository-local analysis (A3 mode). Inspected `tinydb/table.py` and query mechanisms; confirmed search results return direct references to cached/stored document dictionaries.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001)
- Data: COVERED (CON-1)
- Integrations: N/A (library usage)
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: OPEN (NFR-001, Q-1)
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: N/A
- Maintainability and extensibility: N/A
- Autonomy and human oversight: N/A
- Success measures: COVERED (AC-001-1)
- Scope exclusions: N/A
- Delivery constraints: N/A

## H. Change log
- v1 initial draft.
