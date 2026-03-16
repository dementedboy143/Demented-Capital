"""Trending engine: ranks hot tokens from multiple sources."""

from data_sources.binance_api import BinanceAPI
from data_sources.coingecko_api import CoinGeckoAPI


class TrendingEngine:
    def __init__(self, binance: BinanceAPI | None = None, coingecko: CoinGeckoAPI | None = None) -> None:
        self.binance = binance or BinanceAPI()
        self.coingecko = coingecko or CoinGeckoAPI()

    def top_gainers(self, limit: int = 5) -> list[dict]:
        tickers = self.binance.fetch_24h_tickers()
        filtered = [t for t in tickers if not self.binance.is_stable_pair(t["symbol"])]
        sorted_rows = sorted(filtered, key=lambda t: float(t["priceChangePercent"]), reverse=True)
        return sorted_rows[:limit]

    def social_trending(self, limit: int = 5) -> list[dict]:
        return self.coingecko.fetch_trending(limit=limit)

