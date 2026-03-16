"""Retail Trap Scorer
Combines volume spike, price momentum, RSI, and whale flow direction into a 0–100 risk score.
"""
from __future__ import annotations

from typing import Dict, Tuple


def compute_retail_trap_score(
    volume_spike_pct: float,
    price_delta_pct: float,
    rsi: float,
    whale_flow: str = "outflow",  # outflow = selling pressure to CEX, inflow = accumulation
    orderbook_imbalance_pct: float = 0.0,
) -> Dict[str, str]:
    # Normalize inputs
    vol_score = min(max(volume_spike_pct, 0), 300) / 3.0  # cap influence at 100
    price_score = min(max(price_delta_pct, -50), 50) * 0.8  # steep moves near resistance/hype
    rsi_score = 0
    if rsi >= 70:
        rsi_score = 20 + (rsi - 70) * 0.8  # overbought adds pressure
    elif rsi <= 35:
        rsi_score = -10  # oversold reduces trap risk

    whale_bias = 15 if whale_flow.lower() == "outflow" else -10
    ob_bias = min(max(orderbook_imbalance_pct, -50), 50) * 0.3

    raw = vol_score + price_score + rsi_score + whale_bias + ob_bias
    score = max(0, min(100, round(raw, 1)))

    rationale_parts = []
    if volume_spike_pct > 30:
        rationale_parts.append("Massive volume spike")
    if price_delta_pct > 5:
        rationale_parts.append("Price pushing into resistance")
    if rsi >= 70:
        rationale_parts.append("RSI overbought")
    if whale_flow.lower() == "outflow":
        rationale_parts.append("Smart money exiting on-chain")
    if orderbook_imbalance_pct > 15:
        rationale_parts.append("Ask-side orderbook ballooning")

    if not rationale_parts:
        rationale_parts.append("Neutral conditions; monitor only")

    rationale = "; ".join(rationale_parts)
    return {
        "score": score,
        "rationale": f"Score: {score}. {rationale}.",
    }


if __name__ == "__main__":
    demo = compute_retail_trap_score(
        volume_spike_pct=120,
        price_delta_pct=7,
        rsi=74,
        whale_flow="outflow",
        orderbook_imbalance_pct=22,
    )
    print(demo)
