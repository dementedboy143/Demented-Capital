"""Master orchestrator wiring Whale Shadow, Retail Trap Scorer, Narrative Engine, and Risk Guardian."""
from __future__ import annotations

import pathlib
import random
import sys
from typing import Callable, Dict, Optional

# Ensure repo root on path when launched from inside core/ (python core/orchestrator.py)
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config_loader import ConfigLoader
from core.risk_guardian import RiskGuardian
from intelligence_nodes.ai_narrative_engine import NarrativeEngine
from intelligence_nodes.retail_trap_scorer import compute_retail_trap_score
from intelligence_nodes.whale_shadow import detect_whale_dumps

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def log(label: str, message: str, color: str = CYAN) -> None:
    print(f"{color}[{label}]{RESET} {message}")

def default_balance_provider() -> Dict[str, Dict[str, float]]:
    # Deterministic demo data; replace with live on-chain fetcher
    return {
        "0xKATANA_TREASURY": {"USDT": 1_000_000 - random.randint(0, 300_000), "ETH": 800},
        "0xSMART_MONEY_ALPHA": {"USDC": 2_000_000 - random.randint(0, 150_000)},
    }

class Orchestrator:
    def __init__(self, balance_provider: Optional[Callable[[], Dict[str, Dict[str, float]]]] = None):
        self.config = ConfigLoader()
        self.guardian = RiskGuardian()
        self.narrative = NarrativeEngine(self.config)
        self.balance_provider = balance_provider or default_balance_provider

    def run_once(self) -> Optional[str]:
        try:
            log("BOOT", f"Model chain -> primary {self.config.pick_model()}")

            balances = self.balance_provider()
            log("DATA", f"Fetched balances for {len(balances)} VIP targets")

            alerts = detect_whale_dumps(
                current_balances=balances,
                percent_threshold=5.0,
                absolute_threshold=150_000.0,
                destination_hint="Binance",
            )

            if not alerts:
                log("STATUS", "No whale deltas above threshold. Standing by.", color=YELLOW)
                return None

            # Simulated market context for scoring
            trap = compute_retail_trap_score(
                volume_spike_pct=120,
                price_delta_pct=7,
                rsi=74,
                whale_flow="outflow",
                orderbook_imbalance_pct=22,
            )
            log("SCORE", trap.get("rationale", ""))

            narrative = self.narrative.generate(alerts, trap)
            log("LLM", "Narrative generated; passing through Risk Guardian", color=GREEN)

            safe_payload = self.guardian.enforce_compliance(narrative, channel="square")
            log("DISPATCH", "Broadcast-ready payload prepared", color=GREEN)
            
            print("\n" + "="*50)
            print(f"{YELLOW}🚀 BROADCAST-READY PAYLOAD:{RESET}")
            print("="*50)
            print(safe_payload)
            print("="*50 + "\n")
            
            return safe_payload

        except Exception as exc: 
            log("ERROR", f"Pipeline failure: {exc}", color=RED)
            return None

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run_once()
