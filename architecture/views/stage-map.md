# Stage map

| # | Stage | Agent (model) | Inputs the agent sees | Artifact | Check before moving on | Who decides pass/fail |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Requirements | SpecWriter (gemini-3.5-flash-lite) | Issue title + body only | `spec.md` | AC lint: every acceptance criterion is given/when/then or measurable, no vague words; LLM judge agrees all criteria are testable | Mechanical lint + judge, recorded in `state.json` |
| 2 | Design | Designer (gemini-3.5-flash-lite) | `spec.md`, `ARCHITECTURE.md`, repo file tree (paths only) | `design.md` | Every file the plan names exists in the repo or is explicitly marked NEW; plan names files and functions | Mechanical path check + judge |
| 3 | Implementation | Developer (gemini-3.5-flash) | `design.md`, acceptance criteria, full repo read/write tools | `diff.patch` | `python -m compileall` on changed files + package imports | Mechanical (exit codes) |
| 4 | Testing | Tester (gemini-3.5-flash-lite) | `spec.md` criteria, `diff.patch`, repo; writes tests, runs pytest | `test_report.md` | New tests and full suite pass (`pytest` exit 0); on failure back to stage 3, max 3 cycles | Mechanical (pytest exit code) |
| 5 | Release | none (scripted `gh` CLI) | `diff.patch` applied on branch, all prior artifacts | `pr.md` + PR link | PR is open and CI (`ci.yml`) is green on the branch | Mechanical (gh + check runs) |
| 6 | Review | Reviewer (gemini-3.5-flash) | Issue text, `diff.patch`, repo at PR head. Never the pipeline artifacts or agent logs | `review.md` + PR review | Approve, or changes requested classified as approach/code; max 2 rounds | Reviewer verdict JSON with mandatory evidence; human merges |

## Deliberate exclusions (what each agent does NOT see)

- SpecWriter: the repository. The spec must come from the issue, not from what
  happens to be easy to change.
- Designer: the issue's raw wording. It works from the checked spec, so
  ambiguity resolved in stage 1 cannot leak back in.
- Developer and Tester: the hidden acceptance tests. Those live outside the
  repository until grading.
- Tester: nothing extra; it writes its own tests from the spec's criteria, so
  "tests pass" means the spec was met, not that the developer's own tests pass.
- Reviewer: `spec.md`, `design.md`, `test_report.md`, all agent conversations
  and all reasoning. It judges the issue, the diff and the code as it stands.
