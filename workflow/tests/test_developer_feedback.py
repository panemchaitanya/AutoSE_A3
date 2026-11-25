import json, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent'))
import agent, gemini


def repo(d):
    sh = lambda *a: subprocess.run(a, cwd=d, check=True, capture_output=True)
    sh('git', 'init', '-q', '-b', 'main')
    Path(d, 'tinydb').mkdir()
    Path(d, 'tinydb/t.py').write_text('import copy\n')
    sh('git', 'add', '.')
    sh('git', '-c', 'user.name=a', '-c', 'user.email=a@a', 'commit', '-qm', 'x')
    sh('git', 'update-ref', 'refs/remotes/origin/main', 'HEAD')


def test_noop_edit_reports_no_change_not_applied():
    noop = json.dumps({"action": "edit_file", "path": "tinydb/t.py",
                       "old_text": "import copy", "new_text": "import copy"})
    seen = []

    def gen(model, system, contents, usage, context=None):
        seen.append(json.dumps(contents))
        return noop if len(seen) == 1 else '{"action":"finish","result":{"blocked":true}}'
    with tempfile.TemporaryDirectory() as d:
        repo(d)
        with patch.object(agent.gemini, 'generate', side_effect=gen):
            agent.run_agent('Developer', 'm', 's', 't', d, gemini.Usage())
        assert Path(d, 'tinydb/t.py').read_text() == 'import copy\n'
    assert 'edit_file made no change' in seen[1]


def test_no_diff_nudge_appears_after_step_12_only_for_developer():
    read = json.dumps({"action": "read_file", "path": "tinydb/t.py"})
    seen = []

    def gen(model, system, contents, usage, context=None):
        seen.append(json.dumps(contents))
        return read if len(seen) < 15 else '{"action":"finish","result":{"blocked":true}}'
    with tempfile.TemporaryDirectory() as d:
        repo(d)
        with patch.object(agent.gemini, 'generate', side_effect=gen):
            agent.run_agent('Developer', 'm', 's', 't', d, gemini.Usage())
    assert 'no source change exists yet' not in seen[5]
    assert 'no source change exists yet' in seen[13]
    # a real edit removes the nudge
    seen.clear()
    write = json.dumps({"action": "write_file", "path": "tinydb/t.py", "content": "import copy\nx = 1\n"})
    script = [read] * 12 + [write, read, '{"action":"finish","result":{"blocked":true}}']

    def gen2(model, system, contents, usage, context=None):
        seen.append(json.dumps(contents))
        return script[len(seen) - 1]
    with tempfile.TemporaryDirectory() as d:
        repo(d)
        with patch.object(agent.gemini, 'generate', side_effect=gen2):
            agent.run_agent('Developer', 'm', 's', 't', d, gemini.Usage())
    assert 'no source change exists yet' not in seen[14]


def test_profile_reminds_of_frequent_spec_defects():
    import prompts
    p = prompts.A3_REUSE_PROFILE
    assert "end with a pipe" in p and "E3:" in p and "E4:" in p
    assert "not new rules" in p
