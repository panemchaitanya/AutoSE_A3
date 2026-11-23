# Decision experiments - what each variant changes

The report's section 3. Two ADRs were tested with real runs. Negative results
count as much as positive ones (brief's rule) and are reported as found.

## E1 - tests ADR-006 (model tiers): Developer on flash-lite vs flash

- **Question:** does the Developer's model tier actually matter, or is the
  cheaper tier good enough when the stage is mechanically checked?
- **Variant A (control):** Developer = gemini-3.5-flash (the ADR's choice).
- **Variant B (treatment):** Developer = gemini-3.5-flash-lite, everything
  else identical (same issues, prompts, checks, budgets).
- **Issues used:** #3 (search limit) and #4 (get default) - the two feature
  issues, comparable in size.
- **Measurements:** build-pass on first implementation, tests-pass within
  fix cycle 1, fix cycles used, total tokens, wall time, and whether the run
  completed at all.
- **Decision rule:** if flash-lite matches flash on pass outcomes, ADR-006 is
  amended to move the Developer down a tier (cost win); if it does not, the
  ADR stands with measured evidence.

## E2 - tests ADR-003/ADR-008 (reviewer isolation): with vs without pipeline context

- **Question:** does hiding the pipeline's artifacts from the reviewer
  actually change what it catches - or is isolation ceremony?
- **Material:** the five seeded PRs in `experiment/seeded_prs/` - authored diffs
  against the pinned repository, each with one defect planted by hand (see the label
  file per seeded PR).
- **Variant A (control, my design):** reviewer sees issue + diff + repo at
  the PR head only.
- **Variant B (treatment):** reviewer additionally receives spec.md,
  design.md and test_report.md from the pipeline that produced the PR.
- **Measurements:** planted-defect catch rate (out of 5) per variant, false
  positives raised, verdict distribution.
- **Decision rule:** if the context-fed reviewer catches fewer planted
  defects (anchoring on the pipeline's own claims), isolation stays. If the
  catch rate is equal, ADR-003's exclusion list is re-examined - giving the
  reviewer the spec might be free.

### As-run deviation (recorded, not hidden)

The seeded PRs predate any pipeline run, so no real spec/design/test_report
artifacts exist for them. Variant B therefore received an AUTHORED
pipeline-context block (spec/design/test-report/developer summary all
asserting the change is verified correct) instead of captured artifacts.
Run locally on gemini-3.5-flash-lite. Both deviations are carried into the
report's limitations. Result: correct verdicts A 4/5, B 1/5; three verdict
flips to approve under context; isolation stays (see report section 3).
