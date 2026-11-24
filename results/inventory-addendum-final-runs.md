# Final-runs addendum: runs after the issue-4 chain, and the final autonomous boundary

Addendum to attempt-inventory/1 (v4) and the issue-4 chain addendum. Covers the five runs between the issue-4 chain and the final boundary, and records the frozen final targets. Provenance: coordinator live terminal-log/state inspections (labeled per row), reconciled against the coordinator-frozen target table verified live 2026-11-24T18:42:11-22 IST (`final-autonomous-targets.json`): NO active or queued runs in either repo at freeze time. Counters are cumulative branch-lineage state with the labels shown; no sum or difference of snapshots is a billing figure.

## Run 45357125865 (AutoSE_A3, issue 6) - completed/failure (terminal)

- https://github.com/panemchaitanya/AutoSE_A3/actions/runs/45357125865 | workflow_dispatch, created 2026-11-24T08:33:14Z (coordinator dispatch record)
- harness: [44776fe081](https://github.com/panemchaitanya/AutoSE_A3/tree/44776fe0815d6ca563549e4ef3b0a6e1435d690b) (post-PR33, first run with the bundle-naming correction prompt) on branch `autose/issue-6`
- requirements FAILED 2026-11-24T09:25:00Z after two attempts; correction checkpoint attempt 3, exhausted=true. The improved correction fixed the missing structural checks; the semantic gate then caught inconsistent readiness counts (FR1 CLARIFY/UNSET vs validation READY) and an ASSUMED default-source citation defect. No coding or downstream stages
- Known cumulative usage: 214577 tokens / 36 calls, fix/review cycles 0 (coordinator state inspection)
- Frozen branch tip: [ac9916f450](https://github.com/panemchaitanya/AutoSE_A3/commit/ac9916f4509bc0d9ce18d2ba7434e61d3e9b0417)

## Run 45365882908 (AutoSE_A3_Alt, issue 1) - completed/failure (terminal)

- https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45365882908 | workflow_dispatch, created 2026-11-24T09:30:39Z (coordinator dispatch record)
- harness: [426c868309](https://github.com/panemchaitanya/AutoSE_A3_Alt/tree/426c86830903adb0334bb6fda908e5389f53eb01) (Alt parity main) on branch `autose/issue-1`
- requirements SUCCESS and design SUCCESS (corrected A1 verification passed; old lineage usage 363904/41 carried); develop FAILED 2026-11-24T11:05:55Z at the Developer 40-step cap: repeated finish replies omitted the required files_changed field and were not accepted. No Tester, release or review
- Known cumulative usage: 845491 tokens / 108 calls, fix/review cycles 0 (coordinator full terminal logs + state + 40-step transcript)
- LIMIT: this is a real bounded Developer contract failure, not a recoverable timeout; the exhausted attempt is preserved, not reset
- Frozen branch tip: [5381a92439](https://github.com/panemchaitanya/AutoSE_A3_Alt/commit/5381a924395537b0e5bd470bfa9c6551918dbfe6); generated PR #6 open at this head, unmerged

## Run 45382088367 (AutoSE_A3_Alt, issue 2) - completed/failure (terminal, provider error)

- https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45382088367 | workflow_dispatch, created 2026-11-24T11:12:45Z (coordinator dispatch record)
- harness: [426c868309](https://github.com/panemchaitanya/AutoSE_A3_Alt/tree/426c86830903adb0334bb6fda908e5389f53eb01) on branch `autose/issue-2`
- FAILED 2026-11-24T12:14:37Z by provider 503 during SpecWriter correction attempt 2; checkpoint attempt 2 PENDING (not exhausted), conversation saved after 8 correction steps
- Known cumulative usage: 289843 tokens / 47 calls (coordinator terminal inspection; old lineage 160553/31 carried)

## Run 45393236349 (AutoSE_A3_Alt, issue 2) - completed/failure (terminal, bounded resume then exhausted)

- https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45393236349 | workflow_dispatch, created 2026-11-24T12:24:39Z (coordinator dispatch record)
- harness: [426c868309](https://github.com/panemchaitanya/AutoSE_A3_Alt/tree/426c86830903adb0334bb6fda908e5389f53eb01) on branch `autose/issue-2`
- Resumed the EXACT saved correction step 8 (full-log confirmed, no replay/reset); SpecWriter finished and requirements FAILED 2026-11-24T12:40:16Z: structural validation still missing gate/human topics and R1-R3/T2/T3/E2-E4 explicit results. Checkpoint attempt 3, exhausted=true
- Known cumulative usage: 299758 tokens / 49 calls, fix/review cycles 0
- Frozen branch tip: [155f5172a6](https://github.com/panemchaitanya/AutoSE_A3_Alt/commit/155f5172a69feddfb8a92c5ddb6de03e3dd33f26); generated PR #7 open at this head, unmerged

## Run 45396629779 (AutoSE_A3_Alt, issue 3) - completed/failure (terminal, provider error; LAST autonomous run)

- https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45396629779 | workflow_dispatch, created 2026-11-24T12:45:34Z (coordinator dispatch record)
- harness: [426c868309](https://github.com/panemchaitanya/AutoSE_A3_Alt/tree/426c86830903adb0334bb6fda908e5389f53eb01) on branch `autose/issue-3`
- FAILED ~2026-11-24T13:10Z by provider 503 during requirements; no corrected requirements pass, no correction record yet; old lineage usage 132445/21 carried
- Known cumulative usage: 160960 tokens / 25 calls (coordinator terminal inspection)
- Frozen branch tip: [7382d593cd](https://github.com/panemchaitanya/AutoSE_A3_Alt/commit/7382d593cd39118b72b6fb8c7de4d899fa99678c); generated PR #8 open at this head, unmerged
- LIMIT: this failure is a provider interruption with remaining budget, preserved as-is at the final boundary; it was NOT retried

## Final autonomous boundary (frozen 2026-11-24T13:12:11Z)

- No further implementation changes or autonomous runs; artifact-only completion after the sealed hidden evaluation. Verified live at freeze: no active or queued runs in either repository
- Final evaluated heads: AutoSE_A3 main 44776fe0815d6ca563549e4ef3b0a6e1435d690b; AutoSE_A3_Alt main 426c86830903adb0334bb6fda908e5389f53eb01
- All ten issue-branch frozen tips and open generated PRs (A3 #31; Alt #6, #7, #8 - all open, none merged) are listed verbatim in branch-targets-final.csv, transcribed from the coordinator-frozen table
- A3 issue 5 tip [b2a36e4a86](https://github.com/panemchaitanya/AutoSE_A3/commit/b2a36e4a86b76f56f98d2b583190bc299e9af652) and Alt issues 4/5 tips ([9b560110cb](https://github.com/panemchaitanya/AutoSE_A3_Alt/commit/9b560110cb007fd60c53d558669ebb9033207594), [f708d99975](https://github.com/panemchaitanya/AutoSE_A3_Alt/commit/f708d999753e82da8b11816ab5bd96d8c86bcd41)) had no new runs in this window; their earlier exhausted/old-lineage states stand as previously recorded

## Post-boundary acceptance evaluation (results integration)

Sealed per-issue acceptance evaluation (4 tests per issue, single pass, detached checkout of each frozen tip, integrity-verified archive) ran after the boundary; outcome artifact evaluated_at 2026-11-24T18:43+05:30. Results: PASS 4/4 - A3 issue-4 (e28b1b5eec8a, set 3), Alt issue-1 (5381a9243955, set 1), Alt issue-2 (155f5172a69f, set 2), Alt issue-3 (7382d593cd39, set 3). FAIL at baseline 1/4 - A3 issues 2/3/5/6 (sets 1/2/4/5) and Alt issues 4/5 (sets 4/5). Mains are baselines only (each fails 3 of 4 on four sets, 4 of 4 on one). Provenance caveat: the Alt 1-3 passes attach to pre-correction lineage content, not corrected-chain output; A3 issue-4 is the only corrected-chain product among the passes. Full framing in report-section-final-evaluation.md. No hidden test content accessed or included.

## Scope correction (coordinator, applied)

The 16-row runs-final.csv is the recent corrected/recovery subset, not the exhaustive run history; older runs remain in each repo's runs.md. See runs-final-scope.md. E1 tooling is local/unmerged infrastructure, not a delivered repository experiment; the E1 report section now states this.
