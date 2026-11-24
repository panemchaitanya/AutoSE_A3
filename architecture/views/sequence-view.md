# Final corrected recovered sequence

![Actual A3issue4 recovered chain](sequence.png)

The final corrected chain spans45313024154,45331022168,45338808975,45346906399and separate45347087697. No single uninterrupted execution is claimed. PR31is open. Historical Alt sequence remains below for failure provenance, not final corrected evidence.

# Sequence view: one run from label to review

This is the path of one issue through the system. The concrete instance of
this view, with links to the real Actions runs, PRs and reviews, is in
`results/runs.md`.

```mermaid
sequenceDiagram
    actor M as Maintainer (human)
    participant GH as GitHub (issue/PR)
    participant W as autose.yml
    participant AG as Agents (SpecWriter, Designer, Developer, Tester)
    participant R as Release (scripted)
    participant CI as ci.yml
    participant V as autose-review.yml (Reviewer)
    actor H as Human

    M->>GH: adds label "autose" to issue #N
    GH->>W: trigger (issues: labeled)
    W->>W: gate: check sender is repo owner,<br/>create branch autose/issue-N,<br/>init state.json
    W->>AG: Stage 1 Requirements (SpecWriter, issue text only)
    AG-->>W: spec.md
    W->>W: check: AC lint + LLM judge (testable criteria)
    W->>AG: Stage 2 Design (Designer, spec + ARCHITECTURE.md + file tree)
    AG-->>W: design.md
    W->>W: check: every named file exists or is marked NEW
    loop up to 3 fix cycles
        W->>AG: Stage 3 Implementation (Developer, design + repo)
        AG-->>W: diff.patch
        W->>W: check: code builds (compileall + import)
        W->>AG: Stage 4 Testing (Tester, one test per AC + full suite)
        AG-->>W: test_report.md
        W->>W: check: pytest exit code 0
    end
    W->>R: Stage 5 Release
    R->>GH: push branch, open PR, write pr.md
    GH->>CI: pull_request opened
    CI->>CI: run pytest suite
    W->>V: workflow_dispatch after release
    V->>V: Stage 6 Review: fresh context,<br/>sees issue + diff + repo @ PR head only
    alt changes requested, round <= 2
        V-->>GH: COMMENT review: request_changes verdict<br/>classified: approach issue or code issue<br/>+ human-readable comment
        V->>W: gh workflow run autose.yml<br/>(workflow_dispatch: issue, entry stage)
        W->>W: gate: continue mode, entry stage from classification,<br/>review_rounds + 1
    else approve, or rounds used up
        V-->>GH: COMMENT review: approve verdict (or rounds exhausted note)
        V->>H: human decides merge or close
    end
```

## Reading the loop

- Tests failing inside stage 4 loop back to implementation **within the same
  job** (cheap, no new run) up to 3 cycles; after that the run stops and
  `test_report.md` says why.
- Reviewer feedback loops back **across workflows**: the review lives in a
  different workflow with different permissions (source read-only, review/comment and dispatch writes), so it cannot
  push state; it dispatches a continuation run of the main workflow instead
  (workflow_dispatch is exempt from GitHub's recursion guard; a bot's PR
  comment would not re-trigger anything) and leaves a comment for humans.
  An approach issue re-enters at design; a code issue re-enters at
  implementation; at most 2 review rounds, then the human decides.
- Every stage boundary is a checkpoint: artifacts and `state.json` are
  committed to the branch, so a restarted run resumes instead of repeating
  work (and repeating cost).

## Observed run, not one uninterrupted execution

Issue 2 reached release in run 45185960683, opening PR 7. Independent
review run 45188199175 posted COMMENT approve review 6022889438. Earlier
failed attempts are retained in results/runs.md. The COMMENT verdict is
not formal GitHub approval: GitHub rejected self-approval for an
Actions-created PR. No merge occurred.
