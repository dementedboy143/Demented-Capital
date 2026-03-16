"""Post generator: orchestrates engines to craft outbound Square posts."""

from engines.market_engine import MarketEngine
from engines.trending_engine import TrendingEngine
from engines.news_engine import NewsEngine
from engines.education_engine import EducationEngine
from engines.sentiment_engine import SentimentEngine
from core.topic_manager import TopicManager
from core.anti_duplicate import AntiDuplicate


class PostGenerator:
    def __init__(
        self,
        market: MarketEngine | None = None,
        trending: TrendingEngine | None = None,
        news: NewsEngine | None = None,
        education: EducationEngine | None = None,
        sentiment: SentimentEngine | None = None,
        topics: TopicManager | None = None,
        anti_dup: AntiDuplicate | None = None,
    ) -> None:
        self.market = market or MarketEngine()
        self.trending = trending or TrendingEngine()
        self.news = news or NewsEngine()
        self.education = education or EducationEngine()
        self.sentiment = sentiment or SentimentEngine()
        self.topics = topics or TopicManager()
        self.anti_dup = anti_dup or AntiDuplicate()

    def build_trending_post(self) -> str:
        gainers = self.trending.top_gainers(limit=3)
        headline = self.news.latest(limit=1)[0]["title"] if self.news.latest(limit=1) else "Market moving fast."
        lines = [f"Top gainers right now:"]
        for g in gainers:
            lines.append(f"- {g['symbol']}: {g['priceChangePercent']}% (last {g['lastPrice']})")
        lines.append(f"News: {headline}")
        lesson = self.education.lesson("liquidity_sweeps")
        lines.append(f"Lesson: {lesson}")
        post = "\n".join(lines)
        return post if self.anti_dup.is_unique(post) else ""

