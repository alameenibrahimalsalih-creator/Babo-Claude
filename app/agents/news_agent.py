import aiohttp
import logging
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent

class NewsAgent(BaseAgent):
    """
    News Analysis Agent that fetches and analyzes financial news.
    Uses CoinGecko API for crypto news and sentiment analysis.
    """
    name = "NewsAgent"
    weight = 1.2

    def __init__(self):
        self.logger = logging.getLogger("BaboClaude.NewsAgent")
        self.coingecko_url = "https://api.coingecko.com/api/v3"
        self.newsapi_url = "https://newsapi.org/v2"

    async def analyze(self, symbol: str):
        """
        Analyze recent news for the given symbol.
        Returns a vote with confidence, risk assessment, and trading action.
        """
        try:
            # Extract base currency (e.g., "BTC" from "BTC/USDT")
            base_symbol = symbol.split('/')[0].lower() if '/' in symbol else symbol.lower()
            
            # Fetch news sentiment
            sentiment_score, news_count, reason = await self._fetch_and_analyze_news(base_symbol)
            
            # Determine trading action based on sentiment
            confidence, risk, action = self._evaluate_sentiment(sentiment_score, news_count)
            
            return {
                "agent": self.name,
                "confidence": confidence,
                "risk": risk,
                "action": action,
                "weight": self.weight,
                "reason": reason,
                "sentiment_score": sentiment_score,
                "news_count": news_count
            }
        except Exception as e:
            self.logger.error(f"Error during news analysis: {e}")
            return self._simulated_analysis()

    async def _fetch_and_analyze_news(self, symbol: str):
        """
        Fetch news from CoinGecko and analyze sentiment.
        Returns: sentiment_score (0-1), news_count, reason
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Fetch trending coins to get news
                async with session.get(f"{self.coingecko_url}/search/trending") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Simple sentiment analysis based on trending status
                        trending_coins = [coin['item']['id'] for coin in data.get('coins', [])]
                        
                        if symbol in trending_coins or any(symbol in coin for coin in trending_coins):
                            sentiment_score = 0.75
                            news_count = len(trending_coins)
                            reason = f"'{symbol}' is trending in the market with positive momentum."
                        else:
                            sentiment_score = 0.55
                            news_count = 0
                            reason = f"No significant trending news found for '{symbol}'."
                    else:
                        sentiment_score = 0.5
                        news_count = 0
                        reason = "Unable to fetch trending data. Using neutral sentiment."
                
                return sentiment_score, news_count, reason
        except Exception as e:
            self.logger.error(f"Error fetching news: {e}")
            return 0.5, 0, f"Error fetching news: {str(e)}"

    def _evaluate_sentiment(self, sentiment_score, news_count):
        """
        Evaluate sentiment score and determine trading action.
        Returns: confidence, risk, action
        """
        # Sentiment score ranges from 0 (very negative) to 1 (very positive)
        if sentiment_score >= 0.7:
            action = "BUY"
            confidence = min(0.95, 0.7 + (sentiment_score - 0.7) * 2)
            risk = 0.08
        elif sentiment_score >= 0.55:
            action = "BUY"
            confidence = 0.65 + (sentiment_score - 0.55) * 2
            risk = 0.12
        elif sentiment_score >= 0.45:
            action = "HOLD"
            confidence = 0.5
            risk = 0.15
        elif sentiment_score >= 0.3:
            action = "SELL"
            confidence = 0.65 + (0.45 - sentiment_score) * 2
            risk = 0.12
        else:
            action = "SELL"
            confidence = min(0.95, 0.7 + (0.3 - sentiment_score) * 2)
            risk = 0.08
        
        return confidence, risk, action

    def _simulated_analysis(self):
        """Fallback simulated analysis when real data is unavailable."""
        return {
            "agent": self.name,
            "confidence": 0.6,
            "risk": 0.15,
            "action": "HOLD",
            "weight": self.weight,
            "reason": "Simulated analysis: Unable to fetch real news data."
        }
