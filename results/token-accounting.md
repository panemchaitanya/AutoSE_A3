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

Known disjoint subtotals (provider-reported or recorded in the repo):
- Call-logged Actions runs, exact: 6,631,297 tokens.
- E2 local seeded-review trials (reported in the report, successful-record usage): A 121,609 plus B 475,933 = 597,542 tokens. Disjoint from the Actions logs.
- Actions runs before the call log existed: only overlapping cumulative branch snapshots exist. Their per-run maximum, summed, is 4,812,201. This is a subtotal bound for that defined scope only (those 29 runs' retained usage.json files), not a lifetime bound.

**The exact lifetime total is unavailable and no lifetime upper bound is proven.** Known omissions:
manual probes and smoke calls, runs whose job produced no artifact (for example cancelled or
gate-failed runs), expired or never-uploaded artifacts, usage before artifacts were retained,
the sealed evaluation's own coordinator calls where not in an artifact, and any run after the
cutoff below. Failed calls (429/503/empty) carry no usage and are counted separately above.
Cutoff for the figures: artifact list read 25 Nov 2026 10:30 IST (Actions run 45550364226 included
where its artifact existed); run 30 onward are not included. A3 tokens by model in logged runs:
gemini-3.5-flash-lite 4,867,803; gemini-3.5-flash 799,450; gemini-3-flash-preview 223,853;
gemini-3.1-flash-lite 90,884.

Cost: every key used was a free-tier Gemini key. Verified: the ORION project showed Free tier with
no billing in the Google console (read-only, 25 Nov 08:08 IST) and the AI Studio key's project
showed Free tier (08:05 IST). That covers those two projects today. It does not prove that every
historical call across every earlier key was free; no billing or paid use was enabled by us and
none was observed.
