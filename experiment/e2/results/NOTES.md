# E2 run notes (local execution, 2026-11-23 IST)

- 10 runs: sp1-sp5 x variants A (isolated) / B (authored pipeline context).
- Model: gemini-3.5-flash-lite, real API key, local sandbox (not hosted runners).
- Token figures are API usage metadata only - no monetary charge; free tier.
- Totals: A 121,609 tokens / B 475,933 tokens (3.9x).
- Failed attempt preserved: first sp2/B run crashed with FileNotFoundError
  (scratch worktree /tmp/e2_sp2 vanished mid-run; cause undiagnosed). No
  artifacts from that attempt; runner patched to record per-variant
  exceptions; sp2/B re-ran once, clean. This note is the failure record.
- summary.json aggregates the 10 completed score.json files.
