# REGISTER: db.get default value (v1)
## A. Source Statements
S-01: "db.get(...) returns None when nothing matches."
S-02: "It would be cleaner if get accepted a default, the way dict.get does"
S-03: "Behavior when the call does match should be exactly what it is today, and omitting default should keep returning None."
## B. Ambiguous Terms
(None)
## C. Open Questions
(None)
## D. Assumptions
(None)
## E. Conflicts
(None)
## F. Evidence Log
EV-1: A3 repository-local analysis, no MCP used.
## G. Coverage Matrix
- Actors: COVERED (ACT-1)
- Core capabilities: COVERED (FR-1)
- Data: COVERED (S-01)
- Integrations: N/A
- Deployment: N/A
- Security: N/A
- Performance: N/A
- Usability: COVERED (S-02)
## H. Change Log
- v1: Initial creation.