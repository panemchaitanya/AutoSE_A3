# Register: TinyDB increment/add/subtract missing field handling (v1)

## A. Source statements
- S-01: "I'm using tinydb.operations.increment for a page-view counter. The first time a page is viewed the document has no count field yet, and instead of just starting the counter at 1, TinyDB blows up: KeyError: 'count'"
- S-02: "I would expect a counter on a missing field to simply start from 0, i.e. after the call above the document should be {'page': '/home', 'count': 1}."
- S-03: "Same goes for add and subtract: adding 5 to a missing field should give 5, subtracting 3 should give -3. Right now I have to defensively insert count: 0 everywhere, which defeats the point."
- S-04: "TinyDB 4.9.0, Python 3.12."

## B. Ambiguous terms
| ID | Term | Candidate meanings | Design decision |
|---|---|---|---|
| AMB-001 | missing field | 1) Treated as 0, 2) Ignored, 3) Raised KeyError | Treat as 0 as explicitly requested in S-02 and S-03 |

## C. Open questions
| ID | Question | Why it matters | Blocks which ids | Score | Default if answered | Owner | Status |
|---|---|---|---|---|---|---|---|
| Q-1 | Should performance be benchmarked for missing field fallback? | Ensures no regression in update loops | NFR-001 | 1 | Assume standard dictionary lookup overhead is negligible | Maintainer | ASSUMED |

## D. Assumptions
| ID | Statement | Linked Q-id |
|---|---|---|
| ASM-001 | Missing fields in numeric update operations should behave as if initialized to 0. | Q-1 |

## E. Conflicts
| ID | Statements | Options | Decision owner |
|---|---|---|---|
| None | N/A | N/A | N/A |

## F. Evidence log
| ID | Tool | Input | Result excerpt | Effect on spec |
|---|---|---|---|---|
| EV-001 | Repository inspection | tinydb/operations.py | Current increment/add/subtract implementations access dict keys directly causing KeyError | Confirmed behavior requiring missing key handling |

## G. Coverage matrix
| Coverage topic | Status | IDs |
|---|---|---|
| Users and roles | COVERED | ACT-1 |
| Core capabilities | COVERED | FR-001, FR-002, FR-003 |
| Data | COVERED | S-01, S-02, S-03 |
| Integrations | N/A | Python standard library |
| Deployment and hosting | N/A | Local library |
| Security and privacy | N/A | None |
| Legal and compliance | N/A | None |
| Performance and capacity | COVERED | NFR-001 |
| Availability and recovery | N/A | None |
| Observability and operations | N/A | None |
| Usability and accessibility | COVERED | S-02, S-03 |
| Maintainability and extensibility | COVERED | CON-1 |
| Autonomy and human oversight | N/A | None |
| Success measures | COVERED | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| Scope exclusions | N/A | None |
| Delivery constraints | COVERED | CON-1 |

## H. Change log
- v1: Initial requirements specification derived from issue #36.
