# Token accounting (brief: "report the total number of tokens you used")

Recomputed 25 Nov 2026, 10:46 IST, through the artifact of run 31 (45551440495, uploaded 05:13:46Z) (post-disclosure, late work) from every retained Actions
artifact of both repositories (196 artifacts: AutoSE_A3 74, AutoSE_A3_Alt 122, none expired).
Script: `results/tools/token_accounting.py`. Provider-reported `usageMetadata.totalTokenCount`
only; each call record counted once by `call_id`; failed calls (429/503/empty) carry no usage.

| Scope | Runs | Call records (unique) | Provider-reported tokens |
|---|---|---|---|
| AutoSE_A3, runs with a call log | 39 | 1,597 (857 failed) | 6,292,067 |
| AutoSE_A3_Alt, runs with a call log | 4 | 290 (201 failed) | 649,307 |
| **Exact, call-logged runs** | 43 | 1,887 | **6,941,374** |
| Runs before the call log existed (A3 15, Alt 14) | 29 | not recorded | not exact; overlapping per-branch cumulative snapshots sum to at most 4,812,201 (A3 528,129, Alt 4,284,072) |

Known disjoint subtotals (provider-reported or recorded in the repo):
- Call-logged Actions runs, exact: 6,941,374 tokens.
- E2 local seeded-review trials (reported in the report, successful-record usage): A 121,609 plus B 475,933 = 597,542 tokens. Disjoint from the Actions logs.
- Actions runs before the call log existed: only overlapping cumulative branch snapshots exist. Their per-run maximum, summed, is 4,812,201. This is a subtotal bound for that defined scope only (those 29 runs' retained usage.json files), not a lifetime bound.

**The exact lifetime total is unavailable and no lifetime upper bound is proven.** Known omissions:
manual probes and smoke calls, runs whose job produced no artifact (for example cancelled or
gate-failed runs), expired or never-uploaded artifacts, usage before artifacts were retained,
the sealed evaluation's own coordinator calls where not in an artifact, and any run after the
cutoff below. Failed calls (429/503/empty) carry no usage and are counted separately above.
Cutoff for the figures: runs through 45551440495 (run 31, the last run before this file). Run 28
(45549371991) was cancelled before any stage and has no artifact. Later runs are not included.
A3 tokens by model in logged runs: gemini-3.5-flash-lite 4,867,803; gemini-3.5-flash 799,450;
gemini-4-hydrogen 241,012; gemini-3-flash-preview 223,853; gemini-3.1-flash-lite 159,949.

Cost: the keys used were Gemini keys with no billing set up by us. Verified: the ORION project showed Free tier with
no billing in the Google console (read-only, 25 Nov 08:08 IST) and the AI Studio key's project
showed Free tier (08:05 IST). That covers those two projects today. It does not prove that every
historical call across every earlier key was free; no billing or paid use was enabled by us and
none was observed.

## Provider-side console evidence (added 25 Nov 2026, 18:21 IST, late work)

Source: Google AI Studio console, Usage, Spend, Billing and Projects pages, read-only, signed in as the
account that owns the "Gemini Project" (gen-lang-client-0742340833). Screenshot of the 7-day view:
`results/probes/ai-studio-usage-7d-2026-11-25-1821IST.png`. Time zone shown by the console: UTC-8.
Usage was read with the console's own windows (1 day, 7 days, 28 days); a custom date range was not available, and the
per-key filter ("All API Keys") showed one key, labelled "Colab ASE Lecture 3".

| Console window (read 25 Nov 18:21 IST) | Input tokens | Output tokens | Requests |
|---|---|---|---|
| 1 day | 4,270,325 | 86,118 | 636 |
| 7 days | 8,535,319 | 188,806 | 1,271 |
| 28 days | 20,803,749 | 889,930 | 2,115 |

What this does and does not show:
- It is provider-reported usage for this one project, all models, all of its traffic in the window. It is not an A3-only
  figure: the same key is the one used for the course activities, so the 7-day and 28-day figures can include non-A3 calls
  (the 28-day chart has an earlier burst around 5 to 7 Nov, before A3 started; in the 7-day chart the first bars are around 22 Nov).
  The 7-day figure (8,724,125 input plus output) is therefore a window total for this project, not a proven A3 total.
- It is not reconciled to the repository logs (6,941,374 exact for call-logged runs, 597,542 E2). The logged runs
  used more than one key (ORION's project was also used as a fallback), so the two numbers are different scopes. The provider
  figure is higher than the logged subtotal, consistent with unlogged calls, failed calls and non-A3 use, but that is a
  consistency check, not a proof.
- The ORION project (orionxai.core, gen-lang-client-0930771108) has its own usage page. See the ORION paragraph below.

Spend cap: the Spend page for this project says there is no billing set up for it, the Billing page says "No billing account",
and the Projects page shows Free tier with no monthly spend. A Gemini API project in that state cannot be charged. This is the
current state. The console does not show whether billing was ever attached earlier, so it does not prove the state
before the first A3 run, and a free tier is not a provider-set "hard spending limit" in the brief's sense. It is reported as
the available evidence, not as a met requirement.

Google Cloud side of the same account (read 25 Nov 18:36 IST): the Cloud console billing page for that Google account shows no
billing accounts, and it still asks to accept the Cloud terms, so no Cloud project or billing account has been set up there.
This supports "no billing was linked to this key's project". It is a current-state reading. Zero charges or no billing account
now cannot show that a limit was installed beforehand, and the console gave no history of billing-link changes.

ORION project (orionxai.core, "Default Gemini Project", used for fallback keys): read on 25 Nov 08:08 IST, Free tier, one key,
no billing linked to the project. The Google account also owns a separate Cloud billing account (not linked to the Gemini
project) that requires prepay and shows no use. Its usage totals were not captured, and a later attempt to read them needed a
sign-in approval that was not completed, so the tokens spent on that key are **not measured** here. The brief's
total-token figure is therefore a measured lower-level set of figures, not a complete count.
