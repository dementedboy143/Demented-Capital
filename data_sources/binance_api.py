"""Minimal Binance public-data client (public endpoints only)."""

import json
import os
import urllib.request


class BinanceAPI:
    BASE = "https://api1.binance.com"
    STABLES = {"USDT", "BUSD", "USDC", "FDUSD", "TUSD", "USDP", "DAI", "EUR", "GBP", "TRY", "BRL", "AUD", "CAD", "JPY", "CHF"}

    def fetch_24h_tickers(self, symbols: list[str] | None = None) -> list[dict]:
        url = f"{self.BASE}/api/v3/ticker/24hr"
        raw = urllib.request.urlopen(url, timeout=15).read()
        data = json.loads(raw)
        if symbols:
            wanted = set(symbols)
            data = [t for t in data if t.get("symbol") in wanted]
        return data

    def fetch_ticker(self, symbol: str) -> dict:
        url = f"{self.BASE}/api/v3/ticker/24hr?symbol={symbol}"
        raw = urllib.request.urlopen(url, timeout=10).read()
        return json.loads(raw)

    def is_stable_pair(self, symbol: str) -> bool:
        return any(symbol.endswith(stable) for stable in self.STABLES)

