"""CryptoPanic headlines client (public RSS JSON proxy)."""

import json
import urllib.request


class CryptoPanicAPI:
    FEED = "https://cryptopanic.com/api/v1/posts/?kind=news&filter=rising"

    def fetch_headlines(self, limit: int = 5) -> list[dict]:
        raw = urllib.request.urlopen(self.FEED, timeout=10).read()
        posts = json.loads(raw).get("results", [])
        return posts[:limit]

