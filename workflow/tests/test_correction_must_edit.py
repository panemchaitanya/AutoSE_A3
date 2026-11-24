import sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent'))
import agent, gemini

TASK = 'x The specification failed its checks across the requirements artifacts.'
FIN = '{"action":"finish","result":{"summary":"s"}}'
EDIT = '{"action":"write_file","path":".autose/artifacts/v.md","content":"gate"}'


def run(replies, task=TASK):
    with tempfile.TemporaryDirectory() as d:
        usage = gemini.Usage()
        with patch.object(agent.gemini, 'generate', side_effect=replies):
            return agent.run_agent('SpecWriter', 'm', 's', task, d, usage)


def test_correction_finish_without_edit_is_rejected_then_edit_accepted():
    result, transcript, err = run([FIN, EDIT, FIN])
    assert err is None and result == {'summary': 's'}
    assert [t['reply'] for t in transcript][:2] == [FIN, EDIT]


def test_first_attempt_finish_is_not_affected():
    result, transcript, err = run([FIN], task='write the spec')
    assert result == {'summary': 's'} and len(transcript) == 1
