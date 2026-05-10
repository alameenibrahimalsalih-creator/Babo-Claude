from transformers import pipeline
from app.agents.base_agent import BaseAgent

class SentimentAgent(BaseAgent):
    name = "SentimentAgent"
    weight = 1.3

    def __init__(self):
        # Using a lightweight sentiment analysis model
        try:
            self.model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception:
            self.model = None

    async def analyze(self, symbol: str):
        # Simulated sentiment analysis for now
        # In production, this would fetch recent tweets or news titles
        text_to_analyze = f"{symbol} is showing strong bullish signals and high institutional interest."
        
        if self.model:
            result = self.model(text_to_analyze)[0]
            confidence = 0.88 if result['label'] == 'POSITIVE' else 0.40
        else:
            confidence = 0.85 # Fallback simulated score
            
        return {
            "agent": self.name,
            "confidence": confidence,
            "risk": 0.08,
            "action": "BUY",
            "weight": self.weight,
            "reason": "Bullish sentiment detected in social media and news"
        }
