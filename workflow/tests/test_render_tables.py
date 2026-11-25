"""ADR-034 offline tests: deterministic table rendering only, no API calls."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent'))
import agent
from a1_checks import table_format_errors


def test_render_basic_and_checks_pass():
    t = [{"name": "reqs", "header": ["ID", "Text", "State"],
          "rows": [["FR-1", "Does a | b", "READY"], ["FR-2", "multi\nline", "OPEN"]]}]
    out, err = agent.render_tables("# X\n\n{{TABLE:reqs}}\n\nafter\n", t)
    assert err is None
    assert "| ID | Text | State |\n|---|---|---|\n| FR-1 | Does a \\| b | READY |" in out
    assert "| FR-2 | multi line | OPEN |" in out
    assert out.endswith("after\n")
    assert table_format_errors("SRS", out) == []


def test_cell_count_mismatch_writes_nothing():
    out, err = agent.render_tables("{{TABLE:a}}", [{"name": "a", "header": ["A", "B"], "rows": [["1"]]}])
    assert out is None and "row 1 has 1 cells, header has 2" in err


def test_placeholder_without_table_and_unused_table_error():
    assert agent.render_tables("{{TABLE:x}}", [{"name": "y", "header": ["A"], "rows": []}])[0] is None
    out, err = agent.render_tables("no placeholder", [{"name": "y", "header": ["A"], "rows": []}])
    assert out is None and "not placed" in err


def test_content_is_never_altered_except_whitespace_in_cells():
    t = [{"name": "a", "header": ["H"], "rows": [["TBD"], ["x  y"]]}]
    out, _ = agent.render_tables("{{TABLE:a}}", t)
    assert "TBD" in out and "| x y |" in out
