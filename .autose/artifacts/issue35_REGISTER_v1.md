# REGISTER: TinyDB String Document IDs in Update and Remove (v1)

## A. Source statements
- S-01: "`db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged."
- S-02: "Passing the int `1` instead of `'1'` works."
- S-03: "My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds."
- S-04: "Please make these consistent with `get` (which accepts the string form)."

## B. Ambiguous terms
| ID | Term | Candidate meanings | Design decision |
|---|---|---|---|
| AMB-1 | consistent with `get` | 1. Normalize `doc_ids` elements to strings / document ID class just like `get` does. 2. Raise ValueError on string IDs. | Follow candidate 1 to support string IDs consistently with `get`. |

## C. Open questions
| ID | Question | Why it matters | Blocks which IDs | Score | Default if unanswered | Owner | Status |
|---|---|---|---|---|---|---|---|
| Q-1 | Should non-existent string doc IDs continue to be silently skipped during update/remove? | Maintains backwards compatibility with existing batch update/remove behavior where missing IDs are ignored. | FR-001, FR-002 | 2 | Yes, maintain silent skip for non-existent IDs. | Maintainers | CLOSED (Assumed default) |

## D. Assumptions
| ID | Assumption statement | Linked question |
|---|---|---|
| ASM-1 | Non-existent IDs passed in `doc_ids` to `update` and `remove` continue to be silently ignored, matching existing behavior for integer IDs. | Q-1 |

## E. Conflicts
*None*

## F. Evidence log
| ID | Server / Source | Tool / Method | Input args | UTC time | Excerpt / Finding | Effect on spec |
|---|---|---|---|---|---|---|
| EV-1 | Repository-local inspection | `read_file` | `tinydb/table.py` | 2025-02-21 | `get` uses `str(doc_id)` and `set(str(doc_id) for doc_id in doc_ids)`, whereas `update`/`remove` take `Iterable[int]` and use raw int lookup without conversion. | Grounded FR-001, FR-002, NFR-001 |

## G. Coverage matrix
| Coverage topic | Status | Ids |
|---|---|---|
| Users and roles | COVERED | ACT-1, ACT-2 |
| Core capabilities | COVERED | FR-001, FR-002 |
| Data | COVERED | CON-1 |
| Integrations | N/A | Web forms pass strings externally |
| Deployment and hosting | N/A | Library code |
| Security and privacy | N/A | Standard DB operations |
| Legal and compliance | N/A | None |
| Performance and capacity | COVERED | Standard set lookup |
| Availability and recovery | N/A | None |
| Observability and operations | COVERED | NFR-001 |
| Usability and accessibility | COVERED | S-03 |
| Maintainability and extensibility | COVERED | NFR-001 |
| Autonomy and human oversight | N/A | None |
| Success measures | COVERED | AC-001-1 to AC-NFR-1 |
| Scope exclusions | COVERED | Q-1 |
| Delivery constraints | COVERED | CON-1 |

## H. Change log
- v1: Initial register creation from GitHub issue #35.
