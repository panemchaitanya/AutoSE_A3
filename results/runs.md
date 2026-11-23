# Runs - links to every Actions run, PR and review

Status: IN PROGRESS. Graded runs land on the submission repository
(https://github.com/panemchaitanya/AutoSE_A3). The development repository
(https://github.com/panemchaitanya/AutoSE_A3_Alt, public after approval) holds the
iteration history below; nothing failed was deleted or hidden.

## Development runs (AutoSE_A3_Alt)

| Run | Trigger | Head | Outcome | What happened and what changed |
| --- | --- | --- | --- | --- |
| [45085110210](https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45085110210) | label `autose` on issue #1 | e541a48 | startup_failure | Caller workflow lacked `actions: write`, so the reusable review workflow was rejected. Fix: 93e453e (permissions + model fallbacks). |
| [45085189588](https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45085189588) | dispatch issue=1 | 93e453e | failure (requirements) | gemini-3.5-flash-lite answered the JSON tool-contract prompt with an empty text part (MALFORMED_FUNCTION_CALL). Fix: 43e102b (`responseMimeType: application/json`). |
| [45085525886](https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45085525886) | dispatch issue=1 | 43e102b | failure (gate) | Fresh-start push rejected (non-fast-forward over the previous attempt's branch). Fix: 8960600, then bfa0919 (qualified force-with-lease). |
| [45085780231](https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45085780231) | dispatch issue=1 | bfa0919 | failure (gate) | Under diagnosis (job log not yet served by GitHub at capture time); also the first run after Alt went private, with included compute exhausted. |

## Submission repository (AutoSE_A3)

| Run | Trigger | Head | Outcome | Note |
| --- | --- | --- | --- | --- |
| [45084718440](https://github.com/panemchaitanya/AutoSE_A3/actions/runs/45084718440) | push (main ref created by branch rename) | edff96a | failure | Upstream tinydb CI fired once when `master` was renamed to `main`; pre-pipeline, before any assignment code. |

## Local validation (not hosted-run evidence)

- 2026-11-23 05:30 IST: requirements stage run locally against the real
  Gemini API (gemini-3.5-flash-lite, JSON mode): PASSED, 5 calls,
  27,874 total tokens, valid spec.md for issue #1.
- 2026-11-23 05:31-05:33 IST: Gemini API returned 503 bursts; harness
  retried only 429s. Fixed locally (ffbb014): transient 5xx and empty
  replies now retry with backoff. Design-stage local completion was NOT
  achieved inside the sandbox's ~120 s command limit (two attempts
  duration-killed; no partial artifacts left behind; stage idempotency
  under mid-stage kills observed but not proven).

## Graded runs

TBD: the five issues run on AutoSE_A3 with links to each run, PR and
review, plus per-stage pass rates and token usage (results.csv).

## 2026-11-23 (post-public, hosted dev runs on Alt)

- Run 45169083482 (issue #1, fresh): gate PASS, requirements PASS
  (spec.md + transcript in artifact 14816202090), design FAILED after 5m15s:
  "rate-limited on all model tiers; last error: Gemini returned an empty
  reply". A small local probe returned text, but did not validate this
  stage's prompt. The client's generic failure label conflates empty
  replies with rate limits, so the root cause is unresolved. Diagnostics
  now retain the finish reason and error class.
  https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45169083482
- Run 45171521123 (issue #1, continuation entry=design): dispatched 17:38 IST.
  https://github.com/panemchaitanya/AutoSE_A3_Alt/actions/runs/45171521123

- Continuation 45171521123 also failed at design with an empty reply.
  Exact-prompt local probes on lite and flash returned
  MALFORMED_FUNCTION_CALL despite JSON mode. Disabling native tool calls
  alone did not fix it; adding an explicit response schema returned STOP
  with a valid JSON action in two probes. Added schema enforcement for
  action agents and a separate judge schema. New runs start fresh so their
  work branches contain the changed client. Earlier run artifacts remain.
