import json, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent'))
import agent, gemini


def edit(old, new):
    return json.dumps({"action": "edit_file", "path": "m.py", "old_text": old, "new_text": new})


FIN = '{"action":"finish","result":{"files_changed":["m.py"],"blocked":true}}'


def run(replies):
    seen = []
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / 'm.py').write_text('a = 1\n')
        def gen(model, system, sent, usage, context=None):
            seen.append(sent)
            return replies.pop(0)
        with patch.object(agent.gemini, 'generate', side_effect=gen):
            agent.run_agent('Developer', 'm', 's', 't', d, gemini.Usage())
        return seen, (Path(d) / 'm.py').read_text()


def text(sent):
    return json.dumps(sent)


def test_repeated_edit_is_told_it_was_already_applied_and_ledger_records_outcome():
    seen, final = run([edit('a = 1', 'a = 2'), edit('a = 1', 'a = 2'), FIN])
    assert final == 'a = 2\n'
    assert 'already applied' in text(seen[2])
    assert '\\"result\\": \\"applied\\"' in text(seen[2])


def test_failed_edit_recorded_in_ledger_with_error():
    seen, final = run([edit('zzz', 'y'), FIN])
    assert final == 'a = 1\n'
    assert 'old_text must match exactly once' in text(seen[1])
