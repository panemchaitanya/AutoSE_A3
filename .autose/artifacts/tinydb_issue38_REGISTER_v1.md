# Register: TinyDB db.get() Default Value Support (v1)

## A. Source Statements
- S-01: `db.get(...)` returns `None` when nothing matches.
- S-02: `db.get(doc_id=some_id) or {}` is easy to forget and also wrong for any falsy document content edge cases I might hit later.
- S-03: It would be cleaner if `get` accepted a default, the way `dict.get` does:
- S-04: `db.get(doc_id=42, default={})`
- S-05: `db.get(Query().name == 'x', default={})`
- S-06: Behavior when the call does match should be exactly what it is today, and omitting `default` should keep returning `None`.
- S-07: Ideally this works for all the ways of calling get: by condition, by `doc_id`, and by `doc_ids` (for `doc_ids`, the default would apply to the list result only in the sense that today's empty-list behavior is already fine - no change needed there; the default matters for the single-document calls).

## B. Ambiguous Terms
- AMB-1: "default" (Candidate meanings: default value returned as-is; default factory callable evaluated when missing. Decision: support direct default value matching dict.get).

## C. Open Questions
- None. All requirements are fully specified by direct stakeholder statements.

## D. Assumptions
- ASM-1: (None required as all requests are explicitly stated).

## E. Conflicts
- None.

## F. Evidence Log
- EV-1: Repository analysis of `tinydb/table.py` and `tinydb/database.py` showing `get()` signature and implementation returning `None` when query/doc_id yields no match.

## G. Coverage Matrix
| Topic | Status | IDs |
|---|---|---|
| Users and roles | COVERED | ACT-1, ACT-2 |
| Core capabilities | COVERED | FR-001, FR-002, FR-003, FR-004 |
| Data / persistence | COVERED | CON-1, CON-2, CON-3 |
| Integrations | N/A | No external integrations affected |
| Deployment and hosting | N/A | Pure library change |
| Security and privacy | N/A | No security boundaries affected |
| Legal and compliance | N/A | MIT licensed codebase |
| Performance and capacity | COVERED | NFR-001 |
| Availability and recovery | N/A | N/A |
| Observability and operations | N/A | N/A |
| Usability and accessibility | COVERED | S-02, S-03 |
| Maintainability and extensibility | COVERED | NFR-001 |
| Autonomy and human oversight | N/A | N/A |
| Success measures | COVERED | AC-001-1 to AC-004-1 |
| Scope exclusions | COVERED | CON-3 |
| Delivery constraints | COVERED | S-07 |

## H. Change Log
- v1.0 initial specification extracted from GitHub issue #38.
