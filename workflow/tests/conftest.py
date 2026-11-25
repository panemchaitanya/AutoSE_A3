import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))

@pytest.fixture(autouse=True)
def _clear_tier_cooldown():
    import gemini
    gemini._TIER_COOLDOWN_UNTIL.clear()
    yield
    gemini._TIER_COOLDOWN_UNTIL.clear()
