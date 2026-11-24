import sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent'))
import agent, gemini

TASK = 'x The specification failed its checks across the requirements artifacts.'
FIN = '{"action":"finish","result":{"summary":"s"}}'
VAL = '.autose/artifacts/issue-1_VALIDATION_v1.md'


def edit(path, content='gate'):
    import json
    return json.dumps({"action": "write_file", "path": path, "content": content})


def run(replies, task=TASK):
    with tempfile.TemporaryDirectory() as d:
        art = Path(d) / '.autose/artifacts'
        art.mkdir(parents=True)
        (art / 'issue-1_VALIDATION_v1.md').write_text('old')
        usage = gemini.Usage()
        with patch.object(agent.gemini, 'generate', side_effect=replies):
            return agent.run_agent('SpecWriter', 'm', 's', task, d, usage)


def test_finish_without_any_change_is_rejected_then_real_edit_accepted():
    result, transcript, err = run([FIN, edit(VAL), FIN])
    assert err is None and result == {'summary': 's'}
    assert len(transcript) == 3


def test_unrelated_file_edit_does_not_count():
    # unrelated write, then finish is rejected; next real edit lets it through
    result, transcript, err = run([edit('notes.txt'), FIN, edit(VAL), FIN])
    assert err is None and len(transcript) == 4


def test_same_content_rewrite_does_not_count():
    result, transcript, err = run([edit(VAL, 'old'), FIN, edit(VAL), FIN])
    assert err is None and len(transcript) == 4


def test_readonly_python_does_not_count():
    cmd = '{"action":"run_shell","command":"python -c \\"print(1)\\""}'
    with patch.object(agent, '_tool_run_shell', return_value='1'):
        result, transcript, err = run([cmd, FIN, edit(VAL), FIN])
    assert err is None and len(transcript) == 4


def test_first_attempt_finish_is_not_affected():
    result, transcript, err = run([FIN], task='write the spec')
    assert result == {'summary': 's'} and len(transcript) == 1
