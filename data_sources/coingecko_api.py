"""CoinGecko lightweight client for trending endpoints."""

import json
import urllib.request


class CoinGeckoAPI:
    BASE = "https://api.coingecko.com/api/v3"

    def fetch_trending(self, limit: int = 5) -> list[dict]:
        url = f"{self.BASE}/search/trending"
        raw = urllib.request.urlopen(url, timeout=10).read()
        data = json.loads(raw).get("coins", [])
        return data[:limit]

