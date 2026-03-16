"""AI Narrative Engine powered by Anthropic Claude Opus 4.6 (with fallbacks).
Takes structured intel (whale alerts + retail trap score) and produces a 90s educational explainer.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    import anthropic
except ImportError:  # pragma: no cover - offline environments
    anthropic = None

from core.config_loader import ConfigLoader

SYSTEM_PROMPT = (
    "You are an Institutional Coach for crypto risk management. "
    "Tone: concise, data-first, no hype. "
    "Never give financial advice; always remind users to DYOR and comply with regulations. "
    "Explain what happened, why it matters, and a neutral action framework (observe/prepare/avoid)."
)


class NarrativeEngine:
    def __init__(self, config: Optional[ConfigLoader] = None):
        self.config = config or ConfigLoader()
        self.model = self.config.pick_model()
        self.api_key = self.config.get_secret("ANTHROPIC_API_KEY", "")

    def _build_user_prompt(self, whale_alerts: List[Dict[str, Any]], trap_score: Dict[str, Any]) -> str:
        whale_text = "No whale movement detected." if not whale_alerts else "\n".join(
            [
                f"- {w['label']} moved {w['delta']:.0f} {w['asset']} ({w['delta_pct']}% drop) toward {w.get('destination','unknown')}"
                for w in whale_alerts
            ]
        )
        trap_line = trap_score.get("rationale", "No trap score computed.")
        return (
            "Context:\n"
            f"Whale flows:\n{whale_text}\n\n"
            f"Retail Trap Score: {trap_line}\n\n"
            "Write a ~120-150 word explainer (˜90 seconds reading aloud) in plain English."
            " Include: what happened, why it matters, and a neutral action framework with risk caveats."
        )

    def generate(self, whale_alerts: List[Dict[str, Any]], trap_score: Dict[str, Any]) -> str:
        prompt = self._build_user_prompt(whale_alerts, trap_score)

        if not anthropic or not self.api_key:
            # Fallback deterministic text for offline/demo
            return (
                "Educational Explainer (offline fallback):\n"
                f"Whales: {prompt.split('Whale flows:')[1].strip()}\n"
                f"Trap: {trap_score.get('rationale','N/A')}\n"
                "Framework: Observe orderbook liquidity, avoid market chasing, set alerts for secondary prints; always DYOR."
            )

        client = anthropic.Anthropic(api_key=self.api_key)
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            # Anthropics returns content as list of blocks
            if hasattr(response, "content") and response.content:
                return "".join([block.text for block in response.content])
            if hasattr(response, "completion"):
                return response.completion  # legacy field
        except Exception as exc:  # pragma: no cover
            return f"Educational Explainer (fallback due to error: {exc})\n{prompt}"

        return "Educational Explainer: unable to generate content."


if __name__ == "__main__":
    engine = NarrativeEngine()
    whale = [{
        "label": "Katana CoL Treasury",
        "delta": 2750000,
        "delta_pct": 18.5,
        "asset": "USDT",
        "destination": "Binance",
    }]
    trap = {"score": 88, "rationale": "Score: 88. Massive volume spike; Smart money exiting."}
    print(engine.generate(whale, trap))
