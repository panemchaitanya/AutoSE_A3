# AutoSE A3 - Architecting an Agentic SDLC Workflow

AutoSE course, Assignment 3. A GitHub Actions workflow that turns an issue
into a tested, independently reviewed pull request.

- **Fork of:** https://github.com/msiemens/tinydb
- **Pinned commit:** `edff96aeb2616402e9489d46e90a592c05565621`
  (`edff96a`, 2026-10-15). All issues, runs and PRs are against this commit's
  code as it stands in this fork.
- **Models (free-tier Gemini API key, repo secret `GEMINI_API_KEY`):**
  gemini-3.5-flash-lite for SpecWriter / Designer / Tester / judge,
  gemini-3.5-flash for Developer / Reviewer (ADR-006). Total tokens per run are
  recorded from the API's usage metadata and reported in
  `results/results.csv`. The key sits on a free-tier project with no billing
  attached, so spend is hard-capped at the free quota.

## How to trigger the workflow

1. Open an issue (see `experiment/issues/` for the five used in the
   experiments).
2. Add the label `autose` to it, or comment `/autose` on it.
3. Watch `.autose/artifacts/` on the branch `autose/issue-<N>`: every stage
   commits its artifact there (`spec.md`, `design.md`, `diff.patch`,
   `test_report.md`, `pr.md`, `review.md`) plus a transcript; the same files
   are attached to the Actions run. `state.json` on the branch shows the
   pipeline's decisions.
4. The run ends with a PR reviewed by the independent reviewer. Only a human
   merges or closes - the workflow never merges.

Only the repository owner can trigger runs (ADR-010). `main` is protected:
changes land through pull requests.

## Layout

```
README.md            # this file
report.pdf           # the report (max 8 pages + appendices)
demo.mp4             # demo video link (see results/runs.md)
ARCHITECTURE.md      # my A2 architecture document, feeds the Designer
architecture/
  views/             # component view, sequence view, stage map
  decisions/         # ADR-001.md ... ADR-010.md (Nygard format)
workflow/            # copy of .github/workflows/ + all agent code + prompts
experiment/
  issues/            # the 5 issue texts
  hidden_tests/      # hidden acceptance tests (kept out of the repo during runs)
  seeded_prs/        # the 5 reviewer-check PRs (diffs + labels)
  variants.md        # what each decision-experiment variant changes
results/
  results.csv
  runs.md            # links to every Actions run, PR and review
```

The live workflows are in `.github/workflows/` (`autose.yml`,
`autose-review.yml`, `ci.yml`); `workflow/` holds a copy plus the agent
harness and prompts, as the brief asks.

## AI use (course policy)

I used an AI coding assistant substantially while building the workflow code
and scaffolding. I reviewed everything it generated; the architecture
decisions, the ADRs and the reasoning in the report are my own.

## Notes for maintainers

- `.autose/` on a PR branch is pipeline metadata; drop it when merging.
- Generated tests live in `tests_autose/` and are part of the reviewed diff.
