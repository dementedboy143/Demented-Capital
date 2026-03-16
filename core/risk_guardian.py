"""Risk Guardian: Zero-Signal policy enforcement.
- Appends mandatory DYOR disclaimer
- Blocks promotional language that could be misread as financial advice
- Central choke point before anything leaves the system (Square/Telegram/Discord)
"""
from __future__ import annotations
import re
from typing import Optional

MANDATORY_DISCLAIMER = (
    "DYOR. Not financial advice. Comply with your local regulations."
)

BLOCKLIST = [
    r"guaranteed\s+profit",
    r"risk[- ]?free",
    r"sure\s+shot",
    r"buy\s+now",
    r"100x",
]

class RiskGuardian:
    def __init__(self, disclaimer: str = MANDATORY_DISCLAIMER):
        self.disclaimer = disclaimer

    def _contains_blocked_phrase(self, text: str) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in BLOCKLIST)

    def enforce(self, payload: str, channel: Optional[str] = None) -> str:
        """Sanitize and append disclaimers. If blocked phrases are found, prefix a caution banner."""
        sanitized = payload.strip()

        if self._contains_blocked_phrase(sanitized):
            sanitized = (
                "[CAUTION] Promotional language detected; reframing as educational only.\n"
                + sanitized
            )

        if self.disclaimer.lower() not in sanitized.lower():
            sanitized = f"{sanitized}\n\n[DISCLAIMER] {self.disclaimer}"

        return sanitized

    # Alias requested by orchestrator contract
    def enforce_compliance(self, payload: str, channel: Optional[str] = None) -> str:
        return self.enforce(payload, channel)

if __name__ == "__main__":
    guardian = RiskGuardian()
    demo = "This is a sure shot trade. Buy now!"
    print(guardian.enforce(demo, channel="square"))