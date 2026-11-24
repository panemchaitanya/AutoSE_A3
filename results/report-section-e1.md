# Report section: Experiment E1 (Developer model tier, ADR-006) - UNANSWERED

## Question

E1 asked whether moving the Developer role down one model tier (gemini-3.5-flash-lite instead of gemini-3.5-flash) preserves pass outcomes, which would amend ADR-006 as a cost win. The decision rule: if lite matches flash on pass outcomes across completed controlled trials, amend the ADR; otherwise the ADR stands with measured evidence.

## Result: the quality question is UNANSWERED

No controlled E1 trial comparison was executed. This must be reported as an unanswered question with delivered, validated infrastructure - not as a negative result about the models and never as an implied equivalence.

What exists, honestly classified:

1. Control tooling implemented LOCALLY and validated (offline, no provider execution). This tooling is local and unmerged - it is not landed in either repository and is therefore not a delivered repository experiment: a trial recorder (schema e1-trial/3) binding each trial to its repository, actual GitHub issue (4 = search-limit, 5 = getdefault), feature task and declared issue file, with review proof only from API-fetched reviews bound to the branch tip; an upstream-input freezer (schema e1-freeze/1) capturing the spec, design, issue file, ARCHITECTURE, harness config and digest, the full initial source tree and the fixed harness as immutable, byte-verified copies with a clean zero-start lineage proof; a clean trial-copy preparation utility producing runnable, provenance-recorded, zero-counter trial repos; and a fail-closed analyzer that requires the frozen manifest, binds every trial to its lineage ORIGIN commit (never its run-modified tip), and refuses a quality conclusion on any identity, input, provenance, contamination or repetition violation. Validation: 65 tooling tests (54 analyzer controls + 6 freezer + 5 trial-copy) plus the execution owner's independent 350-test full pytest and an end-to-end offline chain test (freeze -> prepare -> record -> analyze, zero violations).
2. Operational observations only: the issue-4 chain ran the Developer on gemini-3.5-flash (harness default). That is a single-arm operational outcome, not a comparison, and says nothing about lite.
3. Earlier ad-hoc attempts were confounded and are excluded: provider availability probes mistaken for experiments, comparisons attempted across two forks, branch labels treated as model evidence, and cumulative usage snapshots mislabeled as per-trial usage. The analyzer's fail-closed controls exist precisely because these failure modes were observed.

## Why no trials ran

A controlled E1 pair requires a frozen matched upstream per issue: corrected-A1-verified requirements+design passed, clean zero-start lineage, frozen before any Developer work. Within the assignment window, only issue 4 reached that state (2026-11-24, after the recovered chain), and no fixture was frozen from its pre-Developer boundary (commit e73d1acd0a6e3869b5a91e82c913c6363467522f is the intended source boundary; the PR tip already implements the feature and was correctly never frozen). Issue 5 has no passed upstream (exhausted terminal series). The eight controlled trials were improvement work beyond the minimum honest submission and are not claimed.

## Grading limitation (state plainly)

E1's infrastructure exists and is tested locally, but E1 produced no experimental evidence about the model-tier question. On quality, ADR-006 stands unmeasured either way; per the project's own experiment record, ADR-006 is superseded only PROVISIONALLY by ADR-012 for availability reasons (bounded backoff under provider 503 incidents), which is an availability decision, not quality evidence. A single exploratory matched availability probe pair (E1b, 2026-11-23 22:12 IST: identical Developer prompt/schema/task, one serial call per requested model, no fallback; both requested models returned actual HTTP 503 UNAVAILABLE in under a second) supports that bounded-backoff availability handling and is not a model-quality result.

## Scope correction

The tooling described here (recorder, freezer, trial-copy preparation, analyzer, and their tests) exists in a local working state only. It is unmerged and not part of either repository's delivered state; this section reports it as validated local infrastructure with an unanswered experiment, never as a completed repository experiment.
