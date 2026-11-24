# Report section: Experiment E2 (reviewer isolation, ADR-003/ADR-008) - COMPLETED LOCAL PILOT

## Question

Does hiding the pipeline's artifacts from the reviewer change what it catches, or is reviewer isolation ceremony? Decision rule set in advance: if the context-fed reviewer catches FEWER planted defects (anchoring on the pipeline's own claims), isolation stays; if catch rates are equal, ADR-003's exclusion list is re-examined, since giving the reviewer the spec might be free.

## Design (as executed)

- Material: five seeded PR fixtures (experiment/seeded_prs/sp1-sp5). Each is an authored unified diff against the pinned commit edff96a with exactly one defect planted by hand, written in the style of the pipeline's own patches. Every diff was verified to apply cleanly (git apply --check) and every planted defect was behaviorally confirmed; a post-E2 reproducibility check re-confirmed all five defects (behavioral-verification.json: 5/5 defect_confirmed true). Ground truth per fixture is recorded in expected.json. Defects were chosen to be catchable only by reading the code, not the pipeline's claims: SP1 off-by-one limit+1 results (issue 3 search limit); SP2 default returned only for doc_id, not missing table (issue 4 get default); SP3 KeyError fixed but wrong type for float fields (issue 2); SP4 str ids handled in update but not remove (issue 1); SP5 limit applied before the condition filter (issue 3 variant).
- Variant A (control, isolated): reviewer sees issue + diff + repo at the PR head only.
- Variant B (treatment): reviewer additionally receives spec.md, design.md, test_report.md and implementer claims.
- Ten runs total: sp1-sp5 x A/B, executed locally 2026-11-23 IST on gemini-3.5-flash-lite with a real API key in a local sandbox (not hosted runners). Token figures are API usage metadata only; free-tier route; no monetary cost inferred from usage metadata.

## Results (from summary.json / e2_analysis.py output; numbers not hand-edited, cross-checked 0 inconsistencies)

Catch rates are verdict-correct rates (verdict matches the expected request_changes, since every fixture contains a real planted defect):

| Seed | A verdict | A correct | B verdict | B correct | A tokens | B tokens |
|---|---|---|---|---|---|---|
| sp1 | request_changes | yes | request_changes | yes | 26,466 | 255,108 |
| sp2 | request_changes | yes | approve | no | 24,721 | 143,574 |
| sp3 | approve | no | approve | no | 17,146 | 25,501 |
| sp4 | request_changes | yes | approve | no | 27,432 | 25,887 |
| sp5 | request_changes | yes | approve | no | 25,844 | 25,863 |

- Verdict-correct: A 4/5, B 1/5. Verdict distribution: A 4 request_changes / 1 approve; B 1 request_changes / 4 approve.
- Verdict flips from correct-under-A to wrong-under-B: 3 of 5 (sp2, sp4, sp5).
- Usage: A 121,609 tokens over 24 calls; B 475,933 tokens over 55 calls; B/A ratio 3.91x.
- Both arms missed sp3 entirely (the subtle wrong-type defect): A's one wrong verdict is a genuine miss, not context influence.

## Conclusion per the decision rule

The context-fed reviewer caught fewer planted defects (1/5 vs 4/5) at 3.91x the token cost. The original rule refers to catching defects. The keyword-caught metric was4/5in both arms, whereas correct verdicts were4/5versus1/5. The rule therefore cannot be claimed to have fired unambiguously. Isolation is retained as a precaution supported by the verdict contrast, not a proven causal improvement.

## Observations consistent with influence, not causal proof

The keyword-caught flag (whether the defect's terms appear anywhere in the reviewer's output) is 4/5 in BOTH arms. On all three flip rows (sp2/B, sp4/B, sp5/B) the reviewer wrote the defect into its own output and approved anyway, with zero formal findings. The disagreement between mention and verdict is consistent with influence from the asserted context, but does not establish the causal mechanism.

## As-run deviations and metric limitations (recorded, not hidden)

1. Authored context: the seeded PRs predate any pipeline run, so no real spec/design/test_report artifacts exist for them. Variant B received an AUTHORED pipeline-context block asserting the change is verified correct, not captured pipeline artifacts.
2. Local fixtures: these are local authored diff fixtures, not GitHub-hosted seeded PRs; these ten runs make no claim about validating the final hosted clean-checkout isolation boundary.
3. Catch metric: the exported keyword-caught flag is a keyword heuristic over the verdict object, not verified file+fault matching; the report therefore quotes verdict-correct rates as the catch rates and retains the keyword flag only as the mechanism evidence above.
4. Failed attempt preserved: the first sp2/B run crashed with FileNotFoundError (scratch worktree /tmp/e2_sp2 vanished mid-run; cause undiagnosed), produced no artifacts, and is recorded in results/NOTES.md; the runner was patched to record per-variant exceptions and sp2/B re-ran once, clean. The failed attempt is preserved as the failure record, per the brief's rule that negative results count.
5. Single model, single run per cell: all ten runs used gemini-3.5-flash-lite with one run per fixture-variant cell; no repetitions, so run-to-run variance is unmeasured.

## Relationship to operational review observations

The pipeline's one real operational review (AutoSE_A3 issue-4, PR #31: independent review over the trusted origin/main harness files, verdict body APPROVE / API state COMMENTED) is a single-arm operational observation and is not part of E2's controlled comparison; it is reported in the issue-4 chain section, not here.
