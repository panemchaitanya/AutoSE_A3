# Token accounting (brief: "report the total number of tokens you used")

Recomputed 25 Nov 2026, 10:34 IST (post-disclosure, late work) from every retained Actions
artifact of both repositories (194 artifacts: AutoSE_A3 72, AutoSE_A3_Alt 122, none expired).
Script: `results/tools/token_accounting.py`. Provider-reported `usageMetadata.totalTokenCount`
only; each call record counted once by `call_id`; failed calls (429/503/empty) carry no usage.

| Scope | Runs | Call records (unique) | Provider-reported tokens |
|---|---|---|---|
| AutoSE_A3, runs with a call log | 37 | 1,565 (852 failed) | 5,981,990 |
| AutoSE_A3_Alt, runs with a call log | 4 | 290 (201 failed) | 649,307 |
| **Exact, call-logged runs** | 41 | 1,855 | **6,631,297** |
| Runs before the call log existed (A3 15, Alt 14) | 29 | not recorded | not exact; overlapping per-branch cumulative snapshots sum to at most 4,812,201 (A3 528,129, Alt 4,284,072) |

Lifetime reading: at least 6,631,297 tokens (exact, logged) and at most about 11.44 million if
every snapshot-only run is added in full (the snapshots overlap on shared branches, so this is an
upper bound, not a measurement). A3 tokens by model in logged runs: gemini-3.5-flash-lite
4,867,803; gemini-3.5-flash 799,450; gemini-3-flash-preview 223,853; gemini-3.1-flash-lite 90,884.

Not included: E2 local seeded-review trials (reported separately in the report: A 121,609, B
475,933 tokens), manual probes, runs whose job produced no artifact, and any later runs.
Cost: every call used a free-tier key; the Google console showed the project on the Free tier
(read-only check, 25 Nov 08:08 IST). No billing or paid tier was enabled.
