# Post-disclosure rerun series (started 24 November 2026, 21:12 IST)

Late work. After the 18:42 IST freeze and the single sealed evaluation of the ten
earlier branches, the student asked for the assignment to be completed in full.
This series is separate from that evaluation. The ten evaluated heads listed in
`final-autonomous-targets.json` are not touched. Nothing here is unseen
final-test evidence: aggregate hidden results were already disclosed, and no
hidden test content has been read or used for this series.

## Fresh issues (same text as experiment/issues/issue-1..5.md)

| Rerun issue | Source text | Kind |
|---|---|---|
| #35 | issue-1 | bug: string doc id in update()/remove() |
| #36 | issue-2 | bug: increment() KeyError |
| #37 | issue-3 | feature: search(limit=) |
| #38 | issue-4 | feature: get(default=) |
| #39 | issue-5 | vague report |

## Run log (negative and positive runs are all kept)

| Time (IST) | Issue | Run | Outcome | Notes |
|---|---|---|---|---|
| 21:12 | #37 | 45428682833 | FAILED at Stage 1 (requirements) | Gemini API 503, model retries exhausted after 4 SpecWriter steps. Stage checks never ran. Repo secret then held the earlier key. |
| 21:38 | #37 | 45433683809 | FAILED at Stage 1 (requirements) | Same cause: Gemini API 503 after 7 SpecWriter steps, retries exhausted. Repo secret now the student's AI Studio key (free tier). |
| 21:59 | #37 | 45437784982 | FAILED at Stage 1 | Same cause, Gemini 503, retries exhausted. |
| 22:26 | #37 | 45442883647 | FAILED at Stage 1 | flash-lite for all roles; calls.jsonl: 2 successes then four 503 attempts in about 4.5 min, no alternate tier (primary equals fallback). |
| 22:59 | #37 | 45449108458 | FAILED at Stage 1 (27 min) | ADR-021 patience (about 15 min per call). 7 SpecWriter calls, then 503 retries exhausted. AI Studio key. |
| 23:29 | #37 | 45454572048 | FAILED at Stage 1 (16 min) | Same configuration. 2 calls, then 503 retries exhausted. |
| 23:59 | #37 | 45460110589 | FAILED at Stage 1 (24 min) | Same configuration (started before ADR-022 merged). 7 calls, then 503. |
| 00:26 | #37 | 45464842567 | FAILED at Stage 1 (31 min) | ADR-022 fallback tier gemini-3-flash-preview engaged; final error HTTP 429 free-tier quota on the AI Studio project. AI Studio key. |
| 00:59 | #37 | 45470790181 | FAILED at Stage 1 (43 min) | 15 calls: SpecWriter finished attempt 1 (8 calls), strict A1 validation failed (missing topic gate, no explicit PASS/FAIL/N/A for T2...), correction attempt 2 made 7 calls, then 503 on both primary and fallback tiers until retries exhausted (about 31 min). First run past SpecWriter's first full output on the fresh series. Repo secret switched to the student's ORION project key (different project and quota), flash-lite primary, preview fallback. |

## Run environment change (not a harness change)

At 21:38 IST the `GEMINI_API_KEY` secret of AutoSE_A3 was replaced with the
student's AI Studio key, because direct probes showed the previous key hitting
429 (quota) on `gemini-3.5-flash` after one call. Models, budgets, retry
bounds, correction attempts and stage checks are unchanged.

## Provider availability probes, 21:37 to 21:58 IST

Direct calls, not workflow runs: previous key `gemini-3.5-flash` 1 of 4 ok (429
after), `gemini-3.5-flash-lite` 3 of 4 ok; AI Studio key `gemini-3.5-flash` 4 of
4 ok, flash-lite 2 of 4 ok (503 twice). Large-prompt probe at 21:58: flash and
flash-lite 3 of 3 ok. Conclusion: 503 and 429 are bursty provider effects, not a
request-shape fault. This does not measure coding quality.

## Run environment change 2, 00:59 IST (not a harness change)

After the fallback tier returned 429 on the AI Studio project, one probe call per
model showed the ORION project key answering 200 for flash-lite, preview and
gemini-3.5-flash, while the AI Studio key's gemini-3.5-flash is at its 20 per day
free limit until about 13:30 IST. The `GEMINI_API_KEY` secret was set to the ORION
key. Configuration for run 45470790181 and later: ORION key, flash-lite primary,
gemini-3-flash-preview fallback (ADR-022), ADR-021 patience. This is a separate
configuration from the eight earlier runs. No billing is involved.

## Run 45479843730 (#37), 01:50 IST, pre-ADR-023 configuration

Started 20:20:54Z (01:50:54 IST), failed 20:56:39Z (02:26:39 IST), 36 min. No provider
error: SpecWriter wrote its outputs (7 calls), A1 validation rejected attempt 1 and
the self-correction attempt 2 (7 more calls) with the same three errors: VALIDATION
missing required topic "gate"; basis/gate contradiction (NFR-001 INFERRED but READY);
A1 structural checks failed. Stage 1 failed on content after the correction bound,
as designed. Checks and bound unchanged. ADR-023 (merged 01:53 IST, after this run
checked out main) states these validator requirements in the prompt. The next run
is the first with ADR-023.

## Run 45486818027 (#37), 02:31 IST, ADR-023 prompt

Started 21:01:35Z (02:31:35 IST), failed 21:15:25Z (02:45:25 IST), 14 min, 28 model
calls, no provider error. First run where the structural A1 checks passed after
correction: attempt 1 failed only on "NFR-001 INFERRED but READY"; after the
correction attempt the structural checks passed. Attempt 2 failed the model-based
A1 semantic validation with three findings: NFR-001 ASSUMED with gate CLARIFY said
to violate E2 (the finding itself notes CLARIFY is not READY, so this one reads as a
judge inconsistency), NFR-001 ASSUMED yet linked to source S-02, and Q-1 blocks
FR-003 while FR-003 is READY (rule C4, plausibly a real defect). Stage failed after the
correction bound, as designed. Checks and bound unchanged. This run carried ADR-023
but not ADR-024 (merged after it checked out main). Artifact: autose-issue-37-requirements.

## Run 45490367204 (#37), 02:51 IST, ADR-022 + ADR-023 + ADR-024

First fresh-series run past Stage 1. gate success; requirements success first attempt
(02:52 to 03:11 IST, 8 calls); design success (03:11 to 03:28 IST, two attempts, 18
calls in total); develop FAILED 03:28 to 03:32 IST: "step cap 40 reached" with no
posted PR. Transcript: the same edit_file on tinydb/database.py three times (steps 8,
12, 29) between read_file loops and no edit to tinydb/table.py. Cause analysis and the
fix are in ADR-025 (merged after this run). Release and the independent review did not
run. Run id 45490367204, https://github.com/panemchaitanya/AutoSE_A3/actions/runs/45490367204

## Run 45497498216 (#37), 03:34 IST, ADR-022 to ADR-025

Started 22:05:18Z, requirements FAILED 22:25:02Z (03:55 IST), 21 calls, no provider
error. The relabel reran Stage 1 on branch autose/issue-37, which already held the
passing v1 requirements bundle from run 45490367204. The SpecWriter wrote a v2 bundle
without a REGISTER v2 and without result lines in VALIDATION, so the A1 bundle check
(components are never mixed across versions) and 21 VALIDATION-line checks failed
after both correction attempts. Checks unchanged. ADR-025 was in force but is a
Developer-stage change, so no effect on it is tested. Lesson recorded: relabeling an
issue whose branch already has a passing bundle starts a versioned revision cycle
that has its own failure mode; the next run uses a clean issue (#38) instead of
relabeling #37 again.

## Run 45501304497 (#38), 03:58 IST, ADR-022 to ADR-025

Requirements FAILED at 22:30Z (04:00 IST) after the SpecWriter finished in 8 calls and
committed the bundle: `git push` was rejected by GitHub with Internal Server Error.
Infrastructure failure, no check involved. Retried on the same issue (next run).

## Run 45501659488 (#38 retry), 04:01 IST, ADR-022 to ADR-025

Requirements FAILED 22:35Z (04:05 IST). Attempt 1 failed the semantic check (priority
UNSET on all requirements yet gate READY). The correction attempt wrote a new partial
v2 bundle instead of fixing v1 because the correction text said to preserve version
history; the bundle check rejected it. Same root cause as run 45497498216. Fixed by
ADR-026 (PR #56): correction edits the current version in place. Branch autose/issue-38
now holds this residue and needs a clean branch for a later rerun.

## Run 45504039498 (#36), 04:16 IST, ADR-022 to ADR-026 (main e88f489)

FULL CHAIN PASSED. gate 22:46:32Z; requirements 22:51:17Z (04:21 IST); design
22:52:43Z; develop 23:39:55Z (05:09 IST); release 23:40:27Z, PR #57 opened and left
open (no auto-merge); independent review run 45511951611 posted a review on PR #57 at
23:40:52Z (05:10 IST), verdict approve. Post-disclosure work, not frozen-evaluation
evidence; hidden tests were not run against it. ADR-026's effect is one pass.

## Run 45512804566 (#39), 05:16 IST, ADR-022 to ADR-026 (main e88f489)

Requirements CANCELLED by the 90-minute job timeout at 01:17:15Z (06:47 IST). Attempt 1
finished by 23:53Z (05:23 IST) but failed the semantic check (FR-001 marked STATED
while the statement was paraphrased). The correction attempt then took four
consecutive single model calls of about 15 minutes each (00:06Z to 01:10Z, ADR-021
patience), finished at 01:11:19Z and was cancelled during validation. A first-attempt
semantic failure followed by a slow correction, not pure provider latency. No limits or
checks were changed. No PR, no later stage.

## Run 45526034077 (#35), 06:58 IST, ADR-022 to ADR-026

Requirements CANCELLED by the 90-minute job timeout at 02:59:11Z (08:29 IST). Attempt 1
failed the semantic check (judge: an acceptance criterion tested existing behaviour and
FR-3 non-matching ids were not covered). The correction then ran into rate limits.
Artifact calls.jsonl has 59 call records (each retry is its own record, not a distinct
logical call): 10 flash-lite ok, 4 gemini-3-flash-preview ok, 44 flash-lite rate_limited,
1 flash-lite transient. The 429 body names the free-tier daily quota (500 requests/day for
flash-lite), exhausted; the full backoff ladder was spent before the fallback each time.
Billing check (read-only, 08:08 IST): the ORION project "Default Gemini Project" shows
Free tier, no billing attached. The exact key-to-project tail match was not done.
No checks or limits were changed during the run. Fix: ADR-027 (PR #62, merged 2d671e6
at about 08:34 IST) switches to the fallback after 2 consecutive 429s; later runs use a
new harness identity and are a different configuration. Run 19 (#39) started 03:04:43Z
(08:34 IST).

## Run 45537422704 (#39), 08:34 IST, ADR-022 to ADR-027

Failed at the gate in 27 s: the git push with force-with-lease to the residue branch
autose/issue-39 (run 17 commit 6938e90) was rejected. Branch state, not a model or
harness result. Residue preserved as tag evidence/issue-39-run-17 (no PR had used the
branch); the branch was removed and recreated by run 20.

## Run 45538092589 (#39), 08:40 IST, ADR-022 to ADR-027 (main 2d671e6)

Requirements FAILED at 03:29:24Z (08:59 IST), 19 min after start. 20 call records:
gemini-3-flash-preview 7 ok + 9 rate_limited; gemini-3.5-flash-lite 1 ok + 2 rate_limited
+ 1 transient. ADR-027 worked as designed: after two consecutive 429s on flash-lite
(03:11:08Z, 03:12:08Z) the fallback answered at 03:12:16Z, about 2 minutes after the first
429, instead of after the 15.5 minute ladder. The fallback then also hit its free-tier
daily quota (limit 20 per day for gemini-3-flash) and its ladder ran 03:14Z to 03:29Z
before failing. Both approved models are daily-quota exhausted on this key until the
reset (flash-lite reset about 13:30 IST per the 08:00 probe; preview reset not verified).
No checks or limits were changed. Account tier: Free (AI Studio console, 08:08 IST).

## Execution configuration change (09:02 IST, before run 21)

Both approved models were daily-quota exhausted on the ORION key (run 20 evidence). At
03:32:48Z (09:02 IST) the repository secret GEMINI_API_KEY was replaced with the user's
existing AI Studio key (Free tier project, no billing, no new account, no code change).
Tiny probe with that key: gemini-3.5-flash-lite 200; gemini-3-flash-preview 429 (20 per day,
retry about 4h27m, about 13:30 IST). Runs from run 21 (45540758298, #39, 03:33:06Z) are a
distinct execution configuration (key provenance) from runs 14 to 20, same harness code
(main 2d671e6). The preview fallback has no quota on either key until about 13:30 IST.
Residue notes: the harness gate archives a superseded branch tip under
refs/autose-archive/<branch>-<sha12> before any lease push (6938e90 is archived for #39);
tags evidence/issue-39-run-17 (6938e90) and evidence/issue-39-run-20 (1115060) also exist.
Run 19's lease push failure cause is undiagnosed (the gate swallows git stderr).

## Runs 21 to 28 (09:03 to 10:19 IST), AI Studio key, ADR-028 to ADR-033

Every run below is post-disclosure and a different configuration from the frozen evaluation.
Harness changes, each an ADR plus a PR merged between runs, no check weakened:
- ADR-028 (PR #65): branch suffix variable AUTOSE_BRANCH_SUFFIX, so each retry uses a new
  branch (autose/issue-N-rNN) instead of deleting or force-updating residue.
- ADR-029 (PR #65): deterministic malformed-table-row check; the judge must quote text.
- ADR-030, ADR-031 (PR #66): no-op edit returns an error; reminder text for table separators.
- ADR-032 (PR #67): table column-count checks. Scanned bundles of runs 17 to 24, zero false positives.
- ADR-033 (PR #68, main d24fc6a): 429 quota id and retry delay logged; a per-minute 429
  stays on the primary model. Run 27 is the first run with it.

Transport finding: the malformed separator rows (for example `|---|---|---| p`) are in the
raw model reply itself (run 24 transcript); the write tool stores content unchanged. It is
model generation, not truncation.

Outcome so far: 0 full chains in runs 21 to 28. Run 22 passed requirements and design and
failed at develop (step cap). Run 27 showed the daily free quota on both approved models
is spent on the AI Studio key (retry delay says reset at 08:00:00Z, 13:30 IST). Run 28 was
cancelled by us before any stage ran. Only run 16 (#36, PR #57, automated approve, not
merged) is a full chain in the post-disclosure series. No billing or paid tier was used.
