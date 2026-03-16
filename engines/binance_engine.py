"""Binance engine: thin wrapper over Binance data source for reuse."""

from data_sources.binance_api import BinanceAPI


class BinanceEngine:
    def __init__(self, client: BinanceAPI | None = None) -> None:
        self.client = client or BinanceAPI()

    def top_gainers(self, limit: int = 10) -> list[dict]:
        tickers = self.client.fetch_24h_tickers()
        filtered = [t for t in tickers if not self.client.is_stable_pair(t["symbol"])]
        return sorted(filtered, key=lambda t: float(t["priceChangePercent"]), reverse=True)[:limit]

    def ticker(self, symbol: str) -> dict:
        return self.client.fetch_ticker(symbol)

