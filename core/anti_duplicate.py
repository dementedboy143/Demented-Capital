"""Anti-duplicate: simple hash guard to avoid reposting same text."""

import hashlib


class AntiDuplicate:
    def __init__(self) -> None:
        self.seen: set[str] = set()

    def is_unique(self, text: str) -> bool:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest in self.seen:
            return False
        self.seen.add(digest)
        return True

