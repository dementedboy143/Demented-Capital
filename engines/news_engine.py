"""News engine: pulls curated crypto headlines."""

from data_sources.cryptopanic_api import CryptoPanicAPI


class NewsEngine:
    def __init__(self, source: CryptoPanicAPI | None = None) -> None:
        self.source = source or CryptoPanicAPI()

    def latest(self, limit: int = 5) -> list[dict]:
        return self.source.fetch_headlines(limit=limit)

