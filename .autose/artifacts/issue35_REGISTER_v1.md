# Register: issue35 (v1)

## A. Source statements
- S-01: "update() and remove() silently do nothing when I pass the doc id as a string"
- S-02: "db.get(doc_id='1') finds my document fine, but when I pass the same id as a string to update or remove, nothing happens. No error, no warning, the document is just unchanged."
- S-03: "Passing the int 1 instead of '1' works."
- S-04: "My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds."
- S-05: "Please make these consistent with get (which accepts the string form)."

## B. Ambiguous terms
- AMB-1: "silently do nothing" -> Candidate meanings: (a) return empty list without modifying records, (b) raise ValueError for type mismatch. Decision: match `get()` behavior by accepting string representation of integer IDs and performing the operation.

## C. Open questions
- None. The issue requirements are fully specified by stakeholder comparison with `get()`.

## D. Assumptions
- None. All requirements are directly stated.

## E. Conflicts
- None.

## F. Evidence log
- EV-1: Mode: A3 repository-local analysis (no MCP used). Inspected `tinydb/table.py` and `tinydb/database.py` showing `get()` coerces/handles doc_id lookup while `update()` and `remove()` filter `doc_ids` directly against integer keys without string coercion.

## G. Coverage matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001, FR-002)
- Data: COVERED
- Integrations: N/A
- Deployment and hosting: N/A
- Security and privacy: N/A
- Legal and compliance: N/A
- Performance and capacity: N/A
- Availability and recovery: N/A
- Observability and operations: N/A
- Usability and accessibility: COVERED
- Maintainability and extensibility: COVERED
- Autonomy and human oversight: N/A
- Success measures: COVERED (AC-001-1, AC-002-1)
- Scope exclusions: N/A
- Delivery constraints: COVERED (CON-1)

## H. Change log
- v1: Initial register creation from issue #35.
