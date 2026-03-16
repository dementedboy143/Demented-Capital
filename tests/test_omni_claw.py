import sys
from pathlib import Path

import pytest

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from intelligence_nodes.retail_trap_scorer import compute_retail_trap_score
from core.risk_guardian import RiskGuardian, MANDATORY_DISCLAIMER


def test_trap_score_bounded_extreme_inputs():
    result = compute_retail_trap_score(
        volume_spike_pct=1_000_000,  # extreme volume
        price_delta_pct=500,         # absurd price move
        rsi=150,                    # invalid RSI
        whale_flow="outflow",
        orderbook_imbalance_pct=999,
    )
    score = result["score"]
    assert 0 <= score <= 100, "Score must be bounded between 0 and 100"


def test_risk_guardian_blocks_promotions_and_appends_disclaimer():
    guardian = RiskGuardian()
    payload = "This is guaranteed 100x upside, buy now!"
    sanitized = guardian.enforce(payload, channel="square")

    assert "[CAUTION]" in sanitized, "Should flag promotional language"
    assert MANDATORY_DISCLAIMER.lower() in sanitized.lower(), "Must append DYOR disclaimer"
