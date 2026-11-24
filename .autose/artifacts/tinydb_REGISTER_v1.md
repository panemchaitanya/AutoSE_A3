# Register: TinyDB Missing Field Operations (v1)

## A. Source Statements
- S-01: I'm using tinydb.operations.increment for a page-view counter. The first time a page is viewed the document has no count field yet, and instead of just starting the counter at 1, TinyDB blows up: KeyError: 'count'
- S-02: I would expect a counter on a missing field to simply start from 0, i.e. after the call above the document should be {'page': '/home', 'count': 1}.
- S-03: Same goes for add and subtract: adding 5 to a missing field should give 5, subtracting 3 should give -3.
- S-04: Right now I have to defensively insert count: 0 everywhere, which defeats the point.

## B. Ambiguous Terms
- AMB-1: Missing field treatment. Candidate meanings: (1) Treat as 0, (2) Raise KeyError, (3) Ignore update. Decision: Treat as 0 for arithmetic operations increment, decrement, add, subtract.

## C. Open Questions
- Q-1: Should performance of existing operations be maintained? Blocks: NFR-1. Score: 1. Default: Yes, zero performance regression. Owner: Maintainer. Status: ASSUMED.

## D. Assumptions
- ASM-1: Missing fields for increment/decrement/add/subtract default to 0. Linked to Q-1.

## E. Conflicts
- None.

## F. Evidence Log
- None.

## G. Coverage Matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001, FR-002, FR-003, FR-004)
- Performance: COVERED (NFR-001)

## H. Change Log
- v1: Initial specification created from GitHub issue #3.
