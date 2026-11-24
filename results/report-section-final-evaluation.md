# Report section: final acceptance evaluation of the frozen branch targets

## What was evaluated

After the final autonomous boundary (frozen 2026-11-24T13:12:11Z, no active or queued runs in either repository), each of the ten frozen issue-branch tips was evaluated once against a sealed per-issue acceptance file: exactly 4 issue-specific behavioral tests, copied into the repo root of a detached checkout of the exact frozen commit and run alone with pytest (repo pytest.ini overridden via -c /dev/null to avoid the coverage plugin). Environment: Linux sandbox, system python3 in a fresh venv with pytest and pytest-cov, no CI, single pass, no retries, no repo writes. Archive, wrapped key, ciphertext and all five inner file hashes matched their manifests. Acceptance-set mapping is by GitHub issue title: AutoSE_A3 issue N -> set N-1; AutoSE_A3_Alt issue N -> set N. Hidden test content and names are not included here.

## Results (verbatim from the evaluation outcome artifact)

| Repository | Branch | Frozen commit | Set | Passed | Failed | Result |
|---|---|---|---|---|---|---|
| AutoSE_A3 | autose/issue-2 | bc09fa14da71 | 1 | 1 | 3 | FAIL |
| AutoSE_A3 | autose/issue-3 | 17bb34ee8c7f | 2 | 1 | 3 | FAIL |
| AutoSE_A3 | autose/issue-4 | e28b1b5eec8a | 3 | 4 | 0 | PASS |
| AutoSE_A3 | autose/issue-5 | b2a36e4a86b7 | 4 | 1 | 3 | FAIL |
| AutoSE_A3 | autose/issue-6 | ac9916f4509b | 5 | 1 | 3 | FAIL |
| AutoSE_A3_Alt | autose/issue-1 | 5381a9243955 | 1 | 4 | 0 | PASS |
| AutoSE_A3_Alt | autose/issue-2 | 155f5172a69f | 2 | 4 | 0 | PASS |
| AutoSE_A3_Alt | autose/issue-3 | 7382d593cd39 | 3 | 4 | 0 | PASS |
| AutoSE_A3_Alt | autose/issue-4 | 9b560110cb00 | 4 | 1 | 3 | FAIL |
| AutoSE_A3_Alt | autose/issue-5 | f708d999753e | 5 | 1 | 3 | FAIL |

4 of 10 branches fully pass; 6 do not. No checkout or error failures occurred.

## Baseline comparison

Each repository's main (A3 44776fe081..., Alt 426c868309...) was run against the same sets as a baseline, not as an evaluated target: each main fails 3 of 4 tests on four acceptance sets and 4 of 4 on one. Every FAIL branch above sits at exactly that baseline (1 of 4), i.e. shows no measured improvement over main on its issue's checks.

## How to read the passes (required qualifications)

1. Scope: these are only the 4 sealed tests per issue. A PASS does not evidence full test-suite success or general code quality, and none is claimed.
2. AutoSE_A3 issue-4 (e28b1b5eec8a, PR #31 head): the only PASS produced by the recovered single-chain pipeline (requirements -> design -> bounded Developer continuation -> bounded Tester continuation -> mechanical recheck -> release -> independent review, verdict body APPROVE / API state COMMENTED). Its demonstration value carries the single-uninterrupted-run grading caveat stated in the issue-4 report section.
3. AutoSE_A3_Alt issues 1-3: PASS results attach to frozen branch content that predates the corrected pipeline. These branches' code comes from old lineages; their most recent pipeline runs under the corrected harness terminated in failure (issue 1: Developer 40-step cap contract failure; issue 2: provider 503 then exhausted attempt 3; issue 3: provider 503, not retried). The passes are therefore NOT evidence of corrected full-chain success, and the report must not present them as such. They say only that the sealed checks pass on that frozen content.
4. AutoSE_A3_Alt issues 4-5 and AutoSE_A3 issues 2, 3, 5, 6: FAIL at baseline, consistent with their exhausted/interrupted terminal run states; no code reaching these branch tips after their failed runs demonstrated improvement on the sealed checks.

## Summary claim permitted by the evidence

Of the ten final targets, four frozen branch tips pass all four sealed issue-specific checks and six remain at baseline. Exactly one passing target (AutoSE_A3 issue-4) is the product of the corrected end-to-end pipeline. No claim about hidden-test content, full-suite results, or code quality beyond these checks is made.
