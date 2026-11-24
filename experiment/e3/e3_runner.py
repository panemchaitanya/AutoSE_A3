"""E3 hand-off experiment (ADR-003 / D3), LOCAL execution, post-disclosure.

Question: does the Designer need the whole spec.md, or are the title plus the
acceptance criteria enough? Both arms get ARCHITECTURE.md and the same Designer
prompt, tools, model and budgets (stage 2 contract unchanged).
  F (full):     spec.md as the pipeline hands it today (ADR-003 as written).
  C (condensed): spec title + Acceptance criteria section only.
Specs: two real specs written by the pipeline's SpecWriter (frozen branches).
Scoring is mechanical (no judge): checks.check_design, share of named
functions that exist in the named existing files, number of acceptance criteria
whose key identifier appears in the design, tokens and calls.
Usage: GEMINI_API_KEY=... python3 e3_runner.py <spec: sA|sB> <arm: F|C> <trial>
"""
import json, os, pathlib, re, subprocess, sys, time
REPO = os.environ.get('E3_REPO', '/downloads/a3work/AutoSE_A3')
sys.path.insert(0, REPO + '/workflow/agent')
import agent, checks, config, gemini, prompts
PIN = 'edff96aeb2616402e9489d46e90a592c05565621'
OUT = pathlib.Path(REPO) / 'experiment' / 'e3' / 'results'
SPECS = {'sA': 'specA.md', 'sB': 'specB.md'}

def condensed(spec):
    title = spec.splitlines()[0]
    m = re.search(r'^## Acceptance criteria\n(.*?)(?=^## |\Z)', spec, re.S | re.M)
    return title + '\n\n## Acceptance criteria\n' + m.group(1).strip() + '\n'

def main():
    sp, arm, trial = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = (pathlib.Path(REPO) / 'experiment/e3/specs' / SPECS[sp]).read_text()
    handed = spec if arm == 'F' else condensed(spec)
    wt = f'/tmp/e3_{sp}_{arm}_{trial}'
    subprocess.run(['git', '-C', REPO, 'worktree', 'remove', '--force', wt], capture_output=True)
    subprocess.run(['git', '-C', REPO, 'worktree', 'add', '--detach', wt, PIN], check=True, capture_output=True)
    shutil_arch = subprocess.run(['git', '-C', REPO, 'show', 'HEAD:ARCHITECTURE.md'], capture_output=True, text=True, check=True).stdout
    pathlib.Path(wt, 'ARCHITECTURE.md').write_text(shutil_arch)
    os.makedirs(os.path.join(wt, config.ARTIFACTS_DIR), exist_ok=True)
    task = ("Design the change for this approved specification.\n\n"
            f"--- spec.md ---\n{handed}\n\n"
            f"--- ARCHITECTURE.md ---\n{shutil_arch}\n\n"
            "Explore the repo with list_files/read_file, then write "
            ".autose/artifacts/design.md and finish.")
    usage = gemini.Usage()
    t0 = time.time()
    result, transcript, err = agent.run_agent('Designer', config.MODEL_DESIGN, prompts.DESIGN_SYSTEM, task, wt, usage, stage='design')
    rec = {'spec': sp, 'arm': arm, 'trial': trial, 'model': config.MODEL_DESIGN,
           'handoff_chars': len(handed), 'error': err, 'seconds': round(time.time() - t0),
           'calls': usage.calls, 'total_tokens': usage.total_tokens}
    dp = pathlib.Path(wt, config.ARTIFACTS_DIR, 'design.md')
    if dp.is_file():
        d = dp.read_text()
        ok, problems = checks.check_design(d, wt)
        rec.update(design_written=True, check_pass=ok, problems=problems)
        names = set(re.findall(r'`([A-Za-z_][A-Za-z0-9_]*)\(?', d))
        files = [f for f in set(checks.PATH_RE.findall(d)) if os.path.isfile(os.path.join(wt, f))]
        src = ''.join(pathlib.Path(wt, f).read_text(errors='ignore') for f in files if f.endswith('.py'))
        fn = [n for n in names if re.search(r'^(def|class)\s+' + n + r'\b', d, re.M) is None]
        funcs = [n for n in names if len(n) > 3 and ('_' in n or n.islower())]
        rec['named_identifiers'] = len(funcs)
        rec['identifiers_in_named_files'] = sum(1 for n in funcs if re.search(r'\b' + re.escape(n) + r'\b', src))
        acs = checks.extract_acceptance_criteria(spec)
        rec['ac_total'] = len(acs)
        keys = [set(re.findall(r'(?:limit|increment|decrement|add|subtract|default|search|get)', a)) for a in acs]
        rec['ac_keyword_covered'] = sum(1 for k in keys if k and any(x in d for x in k))
        OUT.joinpath(f'design_{sp}_{arm}_{trial}.md').write_text(d)
    else:
        rec.update(design_written=False, check_pass=False)
    OUT.joinpath(f'result_{sp}_{arm}_{trial}.json').write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec))
    subprocess.run(['git', '-C', REPO, 'worktree', 'remove', '--force', wt], capture_output=True)

main()
