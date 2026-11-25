# SRS: db.get default value (v1)
## 1. Purpose and scope
Add a `default` parameter to `db.get()` to return a user-provided value when no document matches, matching `dict.get` behavior. Source: S-01, S-02.
## 2. Actors
| ID | Actor | Basis | Source |
|---|---|---|---|
| ACT-1 | Developer | INFERRED | S-01 |
## 3. Constraints
| ID | Statement | Basis | Source | Gate |
|---|---|---|---|---|
| CON-1 | Behavior when the call does match should be exactly what it is today | STATED | S-03 | READY |
| CON-2 | Omitting `default` should keep returning `None` | STATED | S-03 | READY |
## 4. Functional requirements
| ID | Statement | Basis | Source | Priority | Gate | AC |
|---|---|---|---|---|---|---|
| FR-1 | The system shall accept a `default` parameter in `db.get` | STATED | S-02 | UNSET | READY | AC-1-1 |
## 5. Non-functional reqs
(None)
## 6. Acceptance criteria
| AC-id | Requirement | Criterion (given/when/then or measurable) |
|---|---|---|
| AC-1-1 | FR-1 | Given a `db.get` call with no matching document, when `default` is provided, then the method returns the `default` value. |
## 7. Dependencies and risks
(None)
## 8. Traceability
S-01 -> FR-1; S-02 -> FR-1; S-03 -> CON-1, CON-2