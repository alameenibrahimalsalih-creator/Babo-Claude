import aiohttp
from app.agents.base_agent import BaseAgent

class NewsAgent(BaseAgent):
    name = "NewsAgent"
    weight = 1.2

    async def analyze(self, symbol: str):
        # Placeholder for real news analysis logic
        score = 0.81
        return {
            "agent": self.name,
            "confidence": score,
            "risk": 0.10,
            "action": "BUY",
            "weight": self.weight,
            "reason": "Positive market news detected"
        }
