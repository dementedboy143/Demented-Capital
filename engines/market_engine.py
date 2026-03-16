"""Market engine: aggregates core market metrics for downstream bots."""

from data_sources.binance_api import BinanceAPI


class MarketEngine:
    def __init__(self, binance: BinanceAPI | None = None) -> None:
        self.binance = binance or BinanceAPI()

    def snapshot(self, symbols: list[str] | None = None) -> list[dict]:
        """Return lightweight 24h ticker snapshots."""
        return self.binance.fetch_24h_tickers(symbols)

