# Spec: Add default value support to db.get
## Source
"It would be cleaner if get accepted a default, the way dict.get does" (S-02)
## Requirements
1. FR-1: The system shall accept an optional `default` parameter in `db.get`.
## Acceptance criteria
- Given a `db.get` call with no matching document, when `default` is provided, then the method returns the `default` value.
- Given a `db.get` call with a matching document, when `default` is provided, then the method returns the matching document.
- Given a `db.get` call with no matching document, when `default` is omitted, then the method returns `None`.
## Assumptions and open questions
- None.