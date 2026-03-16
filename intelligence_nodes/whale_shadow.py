"""Whale Shadow: On-chain treasury/whale delta tracker.
- Tracks VIP target addresses and compares against historical SQLite snapshots
- Flags large outflows/inflows (potential dumps to CEX)
- Returns structured alert dict for downstream pipelines
"""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Dict, List, Optional

DB_PATH = Path("data_pipeline/memory_vault/whale_snapshots.db")

# VIP targets can be extended; key = address, value = metadata
VIP_TARGETS = {
    "0xKATANA_TREASURY": {"label": "Katana CoL Treasury", "assets": ["USDT", "ETH"]},
    "0xSMART_MONEY_ALPHA": {"label": "Smart Money Alpha", "assets": ["USDC", "BTC"]},
}


def _ensure_db(path: Path = DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
                address TEXT NOT NULL,
                asset   TEXT NOT NULL,
                balance REAL NOT NULL,
                updated_at INTEGER NOT NULL,
                PRIMARY KEY(address, asset)
            )
            """
        )
        conn.commit()


def _get_previous_balances(path: Path = DB_PATH) -> Dict[str, Dict[str, float]]:
    with sqlite3.connect(path) as conn:
        rows = conn.execute(
            "SELECT address, asset, balance FROM snapshots"
        ).fetchall()
    result: Dict[str, Dict[str, float]] = {}
    for address, asset, balance in rows:
        result.setdefault(address, {})[asset] = float(balance)
    return result


def _save_balances(current: Dict[str, Dict[str, float]], path: Path = DB_PATH) -> None:
    ts = int(time.time())
    with sqlite3.connect(path) as conn:
        for addr, assets in current.items():
            for asset, bal in assets.items():
                conn.execute(
                    "REPLACE INTO snapshots(address, asset, balance, updated_at) VALUES (?, ?, ?, ?)",
                    (addr, asset, float(bal), ts),
                )
        conn.commit()


def detect_whale_dumps(
    current_balances: Dict[str, Dict[str, float]],
    percent_threshold: float = 10.0,
    absolute_threshold: float = 250_000.0,
    destination_hint: Optional[str] = None,
) -> List[Dict]:
    """Compare current balances vs previous snapshot and flag large outflows.

    Args:
        current_balances: {address: {asset: balance}}
        percent_threshold: percentage drop to trigger
        absolute_threshold: absolute USD (or unit) drop to trigger
        destination_hint: e.g., "binance" if we know transfers hit a CEX

    Returns: list of alert dicts
    """
    _ensure_db()
    previous = _get_previous_balances()
    alerts: List[Dict] = []

    for address, assets in current_balances.items():
        meta = VIP_TARGETS.get(address, {"label": address})
        for asset, current in assets.items():
            prev = previous.get(address, {}).get(asset, current)
            delta = prev - current
            if delta <= 0:
                continue
            pct = (delta / prev * 100) if prev > 0 else 0
            if delta >= absolute_threshold or pct >= percent_threshold:
                alerts.append(
                    {
                        "address": address,
                        "label": meta.get("label", address),
                        "asset": asset,
                        "previous_balance": prev,
                        "current_balance": current,
                        "delta": delta,
                        "delta_pct": round(pct, 2),
                        "destination": destination_hint or "unknown",
                        "reason": f"{meta.get('label', address)} moved {delta:,.0f} {asset} ({pct:.2f}% drop) towards {destination_hint or 'unknown destination'}",
                    }
                )

    # Persist the new snapshot after evaluation
    _save_balances(current_balances)
    return alerts


if __name__ == "__main__":
    sample_balances = {
        "0xKATANA_TREASURY": {"USDT": 1_000_000, "ETH": 800},
        "0xSMART_MONEY_ALPHA": {"USDC": 2_000_000},
    }
    print(detect_whale_dumps(sample_balances, percent_threshold=5, absolute_threshold=100_000, destination_hint="Binance"))
