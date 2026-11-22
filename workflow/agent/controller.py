"""The deterministic state machine (ADR-002).

state.json on the work branch is the single source of truth for where a run
is. Only this module and the workflow steps write it; agents never touch it.

State shape:
{
  "issue": 3,
  "branch": "autose/issue-3",
  "stages": {
    "requirements": {"status": "passed", "artifact": ".autose/artifacts/spec.md", ...},
    "design": {"status": "pending"},
    "implementation": {"status": "pending"},
    "testing": {"status": "pending"},
    "release": {"status": "pending"},
    "review": {"status": "pending"}
  },
  "fix_cycles": 0,
  "review_rounds": 0,
  "usage": {...},
  "history": [{"ts": ..., "event": ...}]
}

statuses: pending | running | passed | failed | stopped
"""

import datetime
import json
import os

import config

STAGES = ["requirements", "design", "implementation", "testing",
          "release", "review"]


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def init_state(issue, branch):
    return {
        "issue": issue,
        "branch": branch,
        "stages": {s: {"status": "pending"} for s in STAGES},
        "fix_cycles": 0,
        "review_rounds": 0,
        "usage": {},
        "history": [{"ts": _now(), "event": "run created"}],
    }


def load_state(repo_root):
    path = os.path.join(repo_root, config.STATE_PATH)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_state(repo_root, state):
    path = os.path.join(repo_root, config.STATE_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


def record(state, event):
    state["history"].append({"ts": _now(), "event": event})


def set_stage(state, stage, status, **extra):
    st = state["stages"].setdefault(stage, {})
    st["status"] = status
    st.update(extra)
    record(state, f"{stage} -> {status}" + (f" ({extra.get('reason')})" if extra.get("reason") else ""))


def first_unpassed(state):
    for s in STAGES:
        if state["stages"][s]["status"] not in ("passed",):
            return s
    return None


def entry_stage_for_continue(state, classification):
    """Review feedback: approach issues go back to design, code issues to
    implementation (ADR-002). Everything downstream is re-opened."""
    entry = "design" if classification == "approach" else "implementation"
    order = STAGES.index(entry)
    for s in STAGES[order:]:
        if s != "review":
            state["stages"][s]["status"] = "pending"
    state["stages"]["review"]["status"] = "pending"
    state["fix_cycles"] = 0
    record(state, f"continue requested -> re-enter at {entry}")
    return entry


def budgets_exhausted(state):
    """Return a reason string if any hard budget is spent, else None."""
    if state.get("fix_cycles", 0) >= config.MAX_FIX_CYCLES:
        return (f"fix-cycle budget exhausted ({config.MAX_FIX_CYCLES}); "
                f"stopping for a human (ADR-009)")
    if state.get("review_rounds", 0) >= config.MAX_REVIEW_ROUNDS:
        return (f"review-round budget exhausted ({config.MAX_REVIEW_ROUNDS}); "
                f"stopping for a human (ADR-009)")
    total = state.get("usage", {}).get("total_tokens", 0)
    if total >= config.MAX_TOKENS_PER_RUN:
        return f"token budget exhausted ({total} >= {config.MAX_TOKENS_PER_RUN})"
    return None
