# Register: TinyDB Table.get Default Value Support (v1)

## Section A: Source Statements
- S-01: "`db.get(...)` returns `None` when nothing matches."
- S-02: "In most of my code paths `None` is not a usable value, so I end up writing `doc = db.get(doc_id=some_id) or {}` which is easy to forget and also wrong for any falsy document content edge cases I might hit later."
- S-03: "It would be cleaner if `get` accepted a default, the way `dict.get` does: `db.get(doc_id=42, default={}) # {} instead of None when missing`, `db.get(Query().name == 'x', default={})`."
- S-04: "Behavior when the call does match should be exactly what it is today"
- S-05: "omitting `default` should keep returning `None`."
- S-06: "Ideally this works for all the ways of calling get: by condition, by `doc_id`"
- S-07: "and by `doc_ids` (for `doc_ids`, the default would apply to the list result only in the sense that today's empty-list behavior is already fine - no change needed there; the default matters for the single-document calls)."

## Section B: Ambiguous Terms
- AMB-1: None identified; behavior matches Python `dict.get` standard semantics.

## Section C: Open Questions
- Q-1: Does `doc_ids` need a default argument? Options: No change needed as empty list is already returned (S-07). Default: No change for `doc_ids`.

## Section D: Assumptions
- ASM-1: `doc_ids` lookup behavior remains unchanged (linked to Q-1).

## Section E: Conflicts
- None.

## Section F: Evidence Log
- EV-1: A3 repository-local analysis (no MCP used). Examined `tinydb/table.py` for `Table.get` implementation.

## Section G: Coverage Matrix
- Core capabilities: COVERED (FR-001, FR-002, FR-003, FR-004)
- Backward compatibility: COVERED (CON-1, CON-2)
- Performance: COVERED (NFR-001)

## Section H: Change Log
- v1: Initial creation.
