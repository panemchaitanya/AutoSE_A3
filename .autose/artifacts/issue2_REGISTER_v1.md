# Register: issue2 (v1)

## A. Source Statements
| ID | Statement |
|---|---|
| S-01 | `db.get(doc_id='1')` finds my document fine |
| S-02 | when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged. |
| S-03 | Passing the int `1` instead of `'1'` works. |
| S-04 | My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds. |
| S-05 | Please make these consistent with `get` (which accepts the string form). |
| S-06 | TinyDB 4.9.0, Python 3.12. |

## B. Ambiguous Terms
| ID | Term | Candidate Meanings | Decision / Resolution |
|---|---|---|---|
| AMB-1 | string document IDs | 1. Automatically coerced to `document_id_class` integers; 2. Kept as strings | Coerced using `document_id_class` identically to `get()` behavior |

## C. Open Questions
| ID | Question | Why it matters | Blocks | Score | Default | Owner | Status |
|---|---|---|---|---|---|---|---|

## D. Assumptions
| ID | Assumption | Linked Q |
|---|---|---|
| ASM-1 | String `doc_ids` passed to `update` and `remove` should be normalized/coerced using `document_id_class` identically to `get(doc_ids=...)` | None |

## E. Conflicts
None.

## F. Evidence Log
None.

## G. Coverage Matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001, FR-002, FR-003, FR-004)
- Data kinds/volume/retention: COVERED
- Integrations/Environment: COVERED (CON-1)
- Success measures: COVERED

## H. Change Log
- v1 initial version