"""Education engine: generates concise educational snippets."""


class EducationEngine:
    def lesson(self, topic: str) -> str:
        lessons = {
            "liquidity_sweeps": "Liquidity sweeps occur when price runs resting stops before reversing; map where stops cluster above highs and below lows.",
            "funding": "Positive funding means longs pay shorts; extreme funding can precede mean reversion.",
        }
        return lessons.get(topic, "Stay risk-managed: position sizing and clear invalidation protect you more than any indicator.")

