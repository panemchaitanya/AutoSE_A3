"""ADR-028: unique execution branch per run; propagation through the gate."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))
import gate  # noqa: E402


def test_default_branch_unchanged():
    assert gate.branch_for(39) == "autose/issue-39"


def test_suffix_gives_unique_branch():
    assert gate.branch_for(39, suffix="r2") == "autose/issue-39-r2"
    assert gate.branch_for(35, suffix="x7") == "autose/issue-35-x7"


def test_explicit_branch_wins_for_continuation():
    assert gate.branch_for(39, explicit="autose/issue-39-r2",
                           suffix="r9") == "autose/issue-39-r2"
    assert gate.branch_for(39, explicit="autose/issue-39") == "autose/issue-39"


@pytest.mark.parametrize("bad", ["autose/issue-3", "autose/issue-390",
                                 "autose/issue-39-", "main",
                                 "autose/issue-39/../x", "autose/issue-38-r2"])
def test_explicit_branch_must_belong_to_issue(bad):
    with pytest.raises(ValueError):
        gate.branch_for(39, explicit=bad)


@pytest.mark.parametrize("bad", ["r 2", "r/2", "../x", "r-2", "r;rm"])
def test_bad_suffix_rejected(bad):
    with pytest.raises(ValueError):
        gate.branch_for(39, suffix=bad)


def test_workflows_propagate_branch():
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    wf = open(os.path.join(root, ".github/workflows/autose.yml")).read()
    rv = open(os.path.join(root, ".github/workflows/autose-review.yml")).read()
    assert "AUTOSE_BRANCH_SUFFIX" in wf and "INPUT_BRANCH" in wf
    assert '-f branch="$BRANCH"' in wf
    assert 'BRANCH="${INPUT_BRANCH:-autose/issue-$ISSUE}"' in rv
    assert '-f branch="$BRANCH"' in rv
