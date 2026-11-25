# REGISTER: Add default value support to db.get (v1)

## A. Source statements
- S-01: "`db.get(...)` returns `None` when nothing matches."
- S-02: "In most of my code paths `None` is not a usable value"
- S-03: "It would be cleaner if `get` accepted a default, the way `dict.get` does"
- S-04: "`db.get(doc_id=42, default={})` # {} instead of None when missing"
- S-05: "Behavior when the call does match should be exactly what it is today, and omitting `default` should keep returning `None`."
- S-06: "Ideally this works for all the ways of calling get: by condition, by `doc_id`, and by `doc_ids` (for `doc_ids`, the default would apply to the list result only in the sense that today's empty-list behavior is already fine - no change needed there)"

## B. Ambiguous terms
(None)

## C. Open questions
(None)

## D. Assumptions
- ASM-1: The `default` parameter applies only to single-document retrieval methods (by `doc_id` or query condition) as requested in the issue (S-06).

## E. Conflicts
(None)

## F. Evidence log
- EV-1: A3 repository-local analysis, no MCP used.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-1, FR-2, FR-3)
- Data: COVERED (S-06)
- Integrations: N/A
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: N/A
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: COVERED (S-03)
- Maintainability and extensibility: COVERED (S-02)
- Autonomy and human oversight: N/A
- Success measures: COVERED (AC-1-1, AC-2-1, AC-3-1)
- Scope exclusions: COVERED (CON-1)
- Delivery constraints: N/A

## H. Change log
- v1: Initial creation.