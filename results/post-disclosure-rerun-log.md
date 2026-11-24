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
