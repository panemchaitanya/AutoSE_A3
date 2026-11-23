# Seeded PRs for experiment E2 (reviewer isolation)

Each seeded PR is a unified diff against the pinned commit (edff96a) with
exactly one defect planted by hand, written in the style of the pipeline's
own patches. Every diff is verified to apply cleanly with `git apply
--check` and its planted defect is verified behaviorally (a short probe
script per seed; see expected.json). `expected.json` records the ground
truth the reviewer is scored against. The planted defects are chosen to be the
kind a reviewer can only catch by reading the code, not the pipeline's
claims:

| # | Base diff | Planted defect | Catchable from diff alone? |
| --- | --- | --- | --- |
| SP1 | issue 3 (search limit) | off-by-one: `limit + 1` results returned | yes, with care |
| SP2 | issue 4 (get default) | default returned only for `doc_id`, not for missing table | yes |
| SP3 | issue 2 (increment KeyError) | fix catches KeyError but returns wrong type for float fields | yes, subtle |
| SP4 | issue 1 (string doc_ids) | fix handles str ids in `update` but not in `remove` | yes, partial-fix |
| SP5 | issue 3 variant | limit applied before the condition filter, not after | yes, semantic |

Protocol per seeded PR: two independent reviewer runs (isolated =
issue + diff + repo head only; with-context = same plus spec.md, design.md,
test_report.md, implementer claims). Record verdict, findings, and whether
the planted defect's file + fault appear in the findings. Catch rate per
variant goes into results.csv; disagreements are quoted in the report.
