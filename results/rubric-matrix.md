# Requirements matrix against assignment-3.md

Checked 25 Nov 2026 10:35 IST against the live repo (main f76cbc8 plus branch token-acct). Late work,
post-disclosure. Three classes: R = required deliverable, O = required outcome (what the brief says a
run must achieve), X = experiment result the brief lets us report as found ("Experiments that give
negative results earn as many marks as those that give positive results").

| Brief clause | Class | Evidence | Status |
|---|---|---|---|
| Six stages with a check each; stage stops and explains on failure | R | workflow/, ADR-013, stage-map.md; failed stages write *_FAILED.md | present |
| Independent reviewer, no push rights, final merge by a person | R | autose-review workflow, ADR-013; PR #31 and #57 open, not merged | present |
| 8 or more ADRs, Nygard format, superseded kept | R | 33 in architecture/decisions (ADR-034 proposed in PR #71), ADR-005/006/009 marked Superseded | present |
| Component, sequence and stage-map views | R | architecture/views (png, dot, md) | present |
| Fork pinned to a commit; hash in README | R | README line 35: edff96aeb2616402e9489d46e90a592c05565621; verified today as a commit and an ancestor of main | present |
| 5 issues (2 bug, 2 feature, 1 vague) with 2 to 4 hidden tests each, outside the repo | R | experiment/issues 1 to 5; hidden totals of 4 per issue in results.csv; tests are not in the repo, as the brief says | present |
| 5 seeded PRs for reviewer checks | R | experiment/seeded_prs sp1 to sp5, verify_seeds.py | present |
| Keys as repo secrets; main protected | R | GEMINI_API_KEY secret; main requires a PR (0 required approvals), enforce-admins on | present; 0 approvals is a choice, not a brief requirement |
| Design committed before agent code | R | ADR/views commit 08a94af is the parent of workflow commit e541a48 (ancestry verified today). Both carry the identical timestamp 2026-11-23 05:16:28 +05:30, so timestamps alone do not show the order; ancestry does | present, with that caveat |
| Two tested ADR experiments | X | E2 (ten local reviews) and E3 (6 attempts per arm, negative result) complete. E1 (ADR-006 model tiers) is incomplete and confounded, and is labelled so; the brief asks for two tested ADRs, not three, so E1 supports no separate required comparison | met by E2 + E3. E1 is an unanswered ADR-006 question, reported as a limitation, not an unmet requirement |
| Layout: README, architecture/, workflow/, experiment/, results/ (results.csv, runs.md) | R | all present; experiment/hidden_tests absent by design (hidden tests stay outside the repo) | present |
| report.pdf at most 8 pages plus appendices, six sections | R | 8 pages; sections incl. hidden results 4 of 10 frozen targets (1/4, 1/4, 4/4, 1/4, 1/4) | present; needs a post-disclosure paragraph (page limit) |
| Pass rate per stage, hidden-test results, what the reviewer caught and missed | R | report section Results and Final hidden acceptance evaluation | present |
| At least three limitations | R | report section 6 | present |
| Total tokens used | R | results/token-accounting.md: 6,941,374 exact for call-logged runs (through run 31), E2 597,542, pre-log snapshot subtotal at most 4,812,201 (that scope only). Exact lifetime total unavailable; no lifetime upper bound proven; omissions listed | **partly unmet: exact total not recoverable**; measured parts reported |
| Cost: hard spending limit with the provider | R | free-tier keys only; two projects shown as Free tier today; not proven for every historical call; no provider-set hard limit exists for a free tier | **not verifiably met for all history**; no billing enabled by us |
| Demo of ONE complete run, issue page to posted review, at most 5 min | R | demo.mp4 3:47 (issue 4, disclosed time cuts and a recheck continuation); demo_run16.mp4 2:30 (run 16, one uninterrupted run). I viewed frames: issue page, run, design artifact, tests, PR, review. Silent, captioned | present; frame check done |
| roll_number_a3_AutoSE.txt with only the repo link | R | 2025204023_a3_AutoSE.txt holds the repo URL only | present |
| AI-use disclosure in README | R | README line 171 | present |
| Honesty: real, linkable runs | R | results/runs.md; post-disclosure CSV; failed and cancelled runs kept | present |
| Public fork, TA-openable links | R | repo public, fork true | present |
| Workflow runs on the five issues | O | the brief states no number of successful runs and the recovered user messages ask for the full assignment, not a chain count. Observed: one uninterrupted full chain (run 16, #36, to a posted automated approve, PR #57 open); frozen evaluation 4 of 10 targets passed all four hidden checks; later runs failed as logged. Reported as found | reported as observed; not claimed as five successes |

## Gate/basis check (answer to main)
The brief's stage-1 check is "All acceptance criteria are testable" and says to reuse the A1 skill. The
A1 skill (workflow/prompts/requirements-ledger-skill.md) defines the VALIDATION summary as: overall verdict,
counts per gate and basis, the result of every section-7 check, tool calls made, and what a human must do.
Our harness (workflow/agent/a1_checks.py) enforces this with a substring test for the words verdict, gate,
basis, tool and human, plus PASS/FAIL/N/A lines for 21 check ids. So the words come from the A1 skill's
required content, not from the assignment, and the test is a wording proxy for that content, not a test of
substantive correctness. The substantive checks (testable acceptance criteria, E2 no READY item with an
INFERRED basis, T3 banned adjectives, the judge) remain. I have not changed any of it. Changing the brittle
proxy would be an ADR plus PR with later runs labelled as a different configuration; it would not by itself
lower the requirement, but I have not done it.
