# results/

- `results.csv` - one row per graded issue run on the submission repo:
  per-stage pass/fail, fix cycles and review rounds used, reviewer verdict,
  hidden acceptance tests passed, total tokens (measured from the API's
  usageMetadata), wall time. Filled from real runs only.
- `runs.md` - links to every Actions run, PR and review, including failed
  development runs and what each failure changed.
