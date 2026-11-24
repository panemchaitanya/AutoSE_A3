# REGISTER: TinyDB limit parameter in search() (v1)

## A. Source statements
| ID | Quote |
|---|---|
| S-01 | `db.search(cond)` always returns every match. When a table has thousands of documents and I only need the first few (a "latest 10" list, a preview, pagination), I have to materialize the whole result list and slice it myself, which is wasteful. |
| S-02 | Could `search` take an optional `limit`? |
| S-03 | `db.search(Query().category == 'book', limit=10)   # first 10 matches only` |
| S-04 | `db.search(Query().category == 'book')             # unchanged: all matches` |
| S-05 | `limit=None` (default) keeps today's behavior - all matches, in document id order. |
| S-06 | `limit=N` returns at most the first N matches, in document id order. |
| S-07 | A limit larger than the number of matches just returns all matches. |

## B. Ambiguous terms
| ID | Term | Candidate meanings | Decision |
|---|---|---|---|
| AMB-1 | "first few" | 1. First by insertion order. 2. First by document ID order. | S-05 and S-06 specify "document id order". |
| AMB-2 | "wasteful" | 1. Memory waste (materializing list). 2. CPU waste (iterating all). | Both are implied; implementation should aim to minimize both. |

## C. Open questions
| ID | Question | Why it matters | Blocks | Score | Default | Owner | Status |
|---|---|---|---|---|---|---|---|
| Q-1 | Should negative `limit` values be allowed? | API robustness. | FR-003 | 1 | Treat as 0 or raise error. Default: raise ValueError or return empty list (to be determined by dev). | Stakeholder | OPEN |
| Q-2 | Should non-integer `limit` (e.g. float) be allowed? | API robustness. | FR-003 | 1 | Only allow int or None. | Stakeholder | OPEN |

## D. Assumptions
| ID | Assumption | Linked Q |
|---|---|---|
| ASM-1 | `limit` must be a non-negative integer or `None`. | Q-1, Q-2 |

## E. Conflicts
*None identified.*

## F. Evidence log
| ID | Source | Detail | Effect |
|---|---|---|---|
| EV-1 | A3 Repository Analysis | Inspected `tinydb/table.py` and `tinydb/database.py`. `search` is defined in `Table` and proxied by `TinyDB`. | Confirmed where the change needs to happen. |

## G. Coverage matrix
| Topic | Status | Details |
|---|---|---|
| Users and roles | COVERED | ACT-1 |
| Core capabilities | COVERED | FR-001, FR-002, FR-003, FR-004 |
| Data | COVERED | Document ID order specified. |
| Integrations | N/A | Internal API change. |
| Deployment | N/A | |
| Security | N/A | |
| Performance | COVERED | NFR-001 |
| Success measures | COVERED | ACs defined. |

## H. Change log
| Version | Date | Description |
|---|---|---|
| v1 | 2023-10-27 | Initial version from issue #37. |
