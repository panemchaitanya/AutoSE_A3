# E3 results (post-disclosure, gemini-3.5-flash-lite, Designer stage, 600s cap per trial)

All 12 attempts are listed. A timeout is a measured outcome (provider call stalled past the cap), not a pass. Runs: local (first 9) and GitHub Actions run 45460176153 (sB-C-2, sB-C-3, sB-F-3). Same runner, model, retry policy and cap for both arms.

| spec | arm | trial | outcome | check_design | tokens | calls | seconds |
|---|---|---|---|---|---|---|---|
| sA | F | 1 | done | pass | 18447 | 4 | 47 |
| sA | F | 2 | done | pass | 30571 | 5 | 56 |
| sA | F | 3 | done | pass | 19716 | 4 | 48 |
| sB | F | 1 | done | pass | 18985 | 5 | 22 |
| sB | F | 2 | done | pass | 18894 | 5 | 52 |
| sB | F | 3 | TIMEOUT 600s | n/a | n/a | n/a | 600 |
| sA | C | 1 | done | FAIL (names no functions or classes) | 28184 | 6 | 89 |
| sA | C | 2 | done | pass | 28854 | 5 | 21 |
| sA | C | 3 | TIMEOUT 600s | n/a | n/a | n/a | 600 |
| sB | C | 1 | done | pass | 17483 | 5 | 54 |
| sB | C | 2 | done | pass | 17526 | 5 | 432 |
| sB | C | 3 | TIMEOUT 600s | n/a | n/a | n/a | 600 |

## Per-arm counts (6 attempts each)
- F (full spec): 5 pass, 0 check fail, 1 timeout. Mean tokens of completed trials 21323.
- C (criteria only): 3 pass, 1 check fail, 2 timeouts. Mean tokens of completed trials 23012 (8% more than F). sB-C-2 passed but took 432 s.

## Decision (rule fixed before the outcomes: adopt C only if pass rate >= F and mean tokens >= 20% lower)
Neither condition is met. Keep ADR-003 as written: the Designer gets the full spec. This is a negative result for the condensed hand-off.
Caveats: 6 attempts per arm, one model, mechanical scoring only (check_design plus identifier counts, no human or hidden-test judgment). Pass means check_design passed, not that the design is correct. Timeouts are provider stalls at the same step in both arms, not attributed to an arm.
