"""Recompute provider-reported token totals from downloaded Actions artifacts.

Usage: python token_accounting.py <dir with <repo>/<run>-<artifact>-<name>/ folders>
Counts each calls.jsonl record once (by call_id), only status=success records with
provider usageMetadata. Runs that predate the call log are reported separately from
their usage.json (cumulative branch snapshots, which overlap and are NOT summed as exact).
"""
import collections, glob, json, os, sys

root = sys.argv[1]
for repo in sorted(os.listdir(root)):
    seen, tot, models, errs, runs = set(), 0, collections.Counter(), 0, set()
    for f in glob.glob(f"{root}/{repo}/*/calls.jsonl"):
        runs.add(os.path.basename(os.path.dirname(f)).split("-")[0])
        for line in open(f):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r["call_id"] in seen:
                continue
            seen.add(r["call_id"])
            if r.get("status") == "success" and r.get("usage"):
                t = r["usage"].get("totalTokenCount", 0); tot += t
                models[r.get("attempted_model")] += t
            else:
                errs += 1
    pre = {}
    for f in glob.glob(f"{root}/{repo}/*/usage.json"):
        run = os.path.basename(os.path.dirname(f)).split("-")[0]
        if run in runs:
            continue
        u = json.load(open(f))["usage"]
        pre[run] = max(pre.get(run, 0), u["total_tokens"])
    print(repo, "logged runs", len(runs), "unique records", len(seen), "failed-call records", errs,
          "success tokens", tot, dict(models))
    print("  runs without call log:", len(pre), "sum of per-run max cumulative snapshot (overlapping upper bound):", sum(pre.values()))
