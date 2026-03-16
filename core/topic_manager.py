"""Topic manager: keeps rotation of themes to avoid repetition."""

from collections import deque


class TopicManager:
    def __init__(self) -> None:
        self.queue = deque(["liquidity", "funding", "momentum", "risk"])

    def next_topic(self) -> str:
        topic = self.queue[0]
        self.queue.rotate(-1)
        return topic

