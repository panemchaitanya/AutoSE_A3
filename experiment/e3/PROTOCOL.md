# E3: hand-off to the Designer (ADR-003, decision D3)

Post-disclosure experiment (run after the 18:42 frozen evaluation). Separate identity from E1 (flash vs lite, still unanswered) and E2.

- Arms: F = full spec.md (current pipeline). C = spec title + Acceptance criteria only. Both get ARCHITECTURE.md, same prompt, tools, model (gemini-3.5-flash-lite), budgets.
- Specs: specs/specA.md (search limit), specs/specB.md (increment missing field), both written by the pipeline SpecWriter on frozen branches.
- Trials: 3 per cell, 12 runs. Runner: e3_runner.py (committed before outcomes of trials beyond the first three were known).
- Score (mechanical): checks.check_design pass, identifiers found in named files, AC coverage, tokens, calls.
- Decision rule fixed in advance: adopt C only if its pass rate >= F's and mean tokens are >= 20% lower; otherwise keep F.
- Negative and failed results are reported.

## Attempt log
Scored runs are results/result_*.json. Interruptions are tool-timeout kills, not scored failures, and are re-run with the same inputs:
- 23:01 parallel batch of 4 (sA-C-1, sB-F-1, sB-C-1, sA-F-2) killed by the 105s tool limit: sA-C-1, sB-C-1, sA-F-2 interrupted, no result recorded; sB-F-1 completed.
- 23:03 batch of 3: sA-C-1, sB-C-1 interrupted again (limit); sB-F-1 already complete.
- 23:05 sA-C-1 run alone, completed and scored (check fail).
- 23:07 sB-C-1 completed; sA-F-2 interrupted by the limit, to be re-run.
- 23:18 remaining trials moved to a detached serial job (/tmp/e3_rest.sh, 600s wall cap per trial). sA-C-3 stalled after 3 calls (step 2 to 3 call hung, provider side) and hit the 600s cap at 23:28 with no design written. Recorded as "stalled, cap exceeded", provider-latency cause not confirmed; COUNTED as a timeout outcome (not a pass, no design) in per-arm completion/reliability counts; any replacement trial keeps this original attempt in the table, so no survivor-only pass rates. Same 600s cap and retry policy for both arms.
- 23:29 pipeline run 45449108458 failed Stage 1 (provider 503 after 15-min patience); #37 relabeled for a new run. E3 job continues serially (one call stream).
- 23:43 sandbox restart killed the detached job after sA-F-3 completed; relaunched for sB-C-2, sB-C-3, sB-F-3 (restart interruption is orchestration, not a provider outcome).
- 23:59 sandbox restart again killed the detached job during sB-C-2 (partial, no result; orchestration interruption). Remaining: sB-C-2, sB-C-3, sB-F-3.
