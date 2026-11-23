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

- Runs 45173689343 (issue 1) and 45173693188 (issue 2) failed requirements
  checks: the first schema allowed write_file without content, and the
  model emitted summaries instead of file text, creating empty specs.
  Fixed with action-specific anyOf schemas requiring each action's fields,
  plus runtime rejection of missing write content. A real API write probe
  returned STOP and a complete Markdown spec with the corrected schema.

- Run 45175070006 (issue 2): requirements passed; design failed its
  semantic check for generic function names. Inspection found retry prompts
  dropped the original spec/architecture when starting a fresh agent.
  Self-correction now preserves the original task plus concrete feedback.
- Run 45175065687 (issue 1): requirements and design passed; development
  was in progress at this checkpoint.

- Implementation transport failures: issue 1 run 45175065687 and issue 5
  run 45175520241 raised TimeoutError; issue 2 run 45175508632 raised
  RemoteDisconnected. These escaped retries. Added transport-error retry
  handling and shorter per-call timeouts; primary flash latency is a real
  E1 completion/availability failure, not a successful code-quality result.

- Flash Developer runs for issue 3 (45175512084) and issue 4 (45175516167)
  also timed out. Lite run issue 2 (45177093956) hit a real HTTP 429:
  the provider reported 15 free requests/minute. Parallel issue runs shared
  that bucket. Changed future workflows to a serial provider queue, paced
  client requests at least five seconds apart, and lengthened 429 backoff.

- Serial continuation 45177637212 passed implementation and testing;
  release CI passed but release failed because shallow checkout had no
  merge base for origin/main...HEAD. Posting ci/pytest also lacked
  statuses:write. Fixed full-history checkout and explicit status permission.
  No PR existed at this point. Passed implementation/testing are retained.

- Recovery 45178255762 stopped because operational continuations incorrectly
  consumed review rounds despite no reviewer verdict. Added entry=resume to
  retain stages without spending review rounds; operational recovery repairs
  counts only when no reviewer verdict exists, with an explicit state event.

- Run 45178413455 passed through release CI; PR creation was denied because
  repository Actions permissions disabled PR creation/approval. Enabled
  that setting (keeping default workflow permission read; explicit workflow
  grants still apply). Run 45179045717 retries release through resume.

- Issue 1 PR https://github.com/panemchaitanya/AutoSE_A3_Alt/pull/6 opened
  in 45179045717 after release CI passed. Reusable review did not instantiate;
  separate review 45180126544 ran but failed verdict schema (findings absent).
  Fixed Reviewer result schema to require verdict/findings/classification/
  summary; no missing finding is silently converted into an approval.

- Review 45181202664 produced a valid approve verdict, but GitHub rejected
  formal approval by the same Actions app that authored the PR. Publish
  the agent's explicit verdict as a COMMENT review instead; it is not a
  human approval or an approving GitHub review. Human merge remains required.

- Issue 1 review completed successfully in 45182313423. Posted COMMENT
  review with explicit approve verdict (not formal/human approval):
  https://github.com/panemchaitanya/AutoSE_A3_Alt/pull/6#pullrequestreview-6022345553
  Pipeline stages passed across recovery runs; no single uninterrupted
  end-to-end success is claimed. Issue 2 operational resume launched next.

- Issue 2 resume 45182917832 failed design after exhausted HTTP 503 retries.
  Kept the run and moved to issue 3 operational resume 45183839092 rather
  than immediately repeating the same unavailable call.

- Issue 3 resume 45183839092 failed implementation after HTTP503 retries.
  Issue 4 resume 45184875593 launched next. Changed the automatic review
  hand-off to explicit workflow_dispatch, the same separate-workflow path
  already verified for issue 1, rather than the unresolved reusable-call path.

- Issue 4 resume 45184875593 failed implementation HTTP503. Verified
  gemini-3.1-flash-lite with a real Developer-contract probe and switched
  current role overrides without changing the free/no-billing project.
  Issue 2 resume 45185960683 passed design and reached development.
- Earlier state lacked a release-passed update despite PR creation; fixed
  future release state writes. API usage now records actual responding
  models per cumulative run, not just requested role defaults. Older logs
  remain the model evidence where this field did not exist.
