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
| 21:59 | #37 | 45437784982 | in progress when written | Retriggered by removing and re-adding the `autose` label. |

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
