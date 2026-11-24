# REGISTER: TinyDB String Document ID Support (v1)

## A. Source Statements
- S-01: "I spent an hour debugging this. `db.get(doc_id='1')` finds my document fine, but when I pass the same id as a string to `update` or `remove`, nothing happens. No error, no warning, the document is just unchanged."
- S-02: "Passing the int `1` instead of `'1'` works. My ids come from a web form so they are always strings, and I really do not want to crash on every bad input either - but a silent no-op on a write is the worst of both worlds."
- S-03: "Please make these consistent with `get` (which accepts the string form)."

## B. Ambiguous Terms
None.

## C. Open Questions
None.

## D. Assumptions
- ASM-1: String IDs matching integer document IDs should be coerced consistently across `update()` and `remove()` methods just like `get()` does. (Linked to S-03)

## E. Conflicts
None.

## F. Evidence Log
None.

## G. Coverage Matrix
- Users and roles: COVERED (ACT-1)
- Core capabilities: COVERED (FR-001, FR-002)
- Data: COVERED
- Integrations: N/A
- Security and privacy: N/A
- Performance and capacity: N/A
- Success measures: COVERED

## H. Change Log
- v1: Initial extraction from issue #2.
