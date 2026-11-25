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
| Fork pinned to a commit; hash in README | R | README | present (not re-verified today) |
| 5 issues (2 bug, 2 feature, 1 vague) with 2 to 4 hidden tests each, outside the repo | R | experiment/issues 1 to 5; hidden totals of 4 per issue in results.csv; tests are not in the repo, as the brief says | present |
| 5 seeded PRs for reviewer checks | R | experiment/seeded_prs sp1 to sp5, verify_seeds.py | present |
| Keys as repo secrets; main protected | R | GEMINI_API_KEY secret; main requires a PR (0 required approvals), enforce-admins on | present; 0 approvals is a choice, not a brief requirement |
| Design committed before agent code | R | git history | present (not re-verified today) |
| Two tested ADR experiments | X | E2 (ten local reviews) and E3 (6 attempts per arm, negative result) complete; E1 incomplete and confounded, labelled | met by E2 + E3; E1 stays labelled incomplete |
| Layout: README, architecture/, workflow/, experiment/, results/ (results.csv, runs.md) | R | all present; experiment/hidden_tests absent by design (hidden tests stay outside the repo) | present |
| report.pdf at most 8 pages plus appendices, six sections | R | 8 pages; sections incl. hidden results 4 of 10 frozen targets (1/4, 1/4, 4/4, 1/4, 1/4) | present; needs a post-disclosure paragraph (page limit) |
| Pass rate per stage, hidden-test results, what the reviewer caught and missed | R | report section Results and Final hidden acceptance evaluation | present |
| At least three limitations | R | report section 6 | present |
| Total tokens used | R | results/token-accounting.md: 6,631,297 exact (call-logged runs, failed calls carry no usage), pre-log runs at most 4,812,201 more, overlapping; lifetime is a bounded range | measured part exact, rest bounded |
| Cost: hard spending limit with the provider | R | free-tier keys only, no billing; the Google project was shown as Free tier (08:08 IST); a provider-set hard limit is not applicable to a free tier | stated, not a paid limit |
| Demo of ONE complete run, issue page to posted review, at most 5 min | R | demo.mp4 3:47 (issue 4, disclosed time cuts and a recheck continuation); demo_run16.mp4 2:30 (run 16, one uninterrupted run). I viewed frames: issue page, run, design artifact, tests, PR, review. Silent, captioned | present; frame check done |
| roll_number_a3_AutoSE.txt with only the repo link | R | 2025204023_a3_AutoSE.txt holds the repo URL only | present |
| AI-use disclosure in README | R | README line 171 | present |
| Honesty: real, linkable runs | R | results/runs.md; post-disclosure CSV; failed and cancelled runs kept | present |
| Public fork, TA-openable links | R | repo public, fork true | present |
| Workflow works on the five issues | O | the brief states no number of successful runs. One uninterrupted full chain exists (run 16, #36, to a posted automated approve). Frozen evaluation: 4 of 10 targets passed all four hidden checks | outcome is reported as found; more chains are the user's ask, not a stated brief clause |

## Gate/basis check (answer to main)
The brief's stage-1 check is "All acceptance criteria are testable" and says to reuse the A1 skill. The
literal words "gate" and "basis" in VALIDATION come from our own A1-reuse check in
workflow/agent/a1_checks.py (a substring test, plus 21 PASS/FAIL lines C1 to E5). It tests wording,
not whether a requirement is correct. It is our harness, not the assignment. I have not weakened it. A
change would be an ADR and a PR between runs, with later runs labelled as a different configuration.
