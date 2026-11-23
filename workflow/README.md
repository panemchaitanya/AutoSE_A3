# workflow/

This directory holds the agent harness, prompts and a copy of the live
GitHub Actions workflows, as the assignment layout requires.

- `agent/` - the pipeline code. `run_stage.py` is the entry point the
  workflows call; `controller.py` is the deterministic state machine;
  `agent.py` is the ReAct tool loop; `gemini.py` the stdlib API client;
  `checks.py` the mechanical stage checks; `gate.py` the trigger gate;
  `config.py` all budgets and model names; `prompts.py` every role prompt.
- `prompts/requirements-ledger-skill.md` - my A1 skill, fed to the
  SpecWriter.
- `autose.yml`, `autose-review.yml`, `ci.yml` - copies of the live files in
  `../.github/workflows/` (kept in sync; the `.github` copies are the ones
  GitHub runs).
