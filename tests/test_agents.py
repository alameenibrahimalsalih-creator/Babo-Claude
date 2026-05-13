import pytest
import asyncio
from app.agents.news_agent import NewsAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.quant_agent import QuantAgent
from app.agents.risk_agent import RiskAgent

@pytest.mark.asyncio
async def test_news_agent():
    """Test NewsAgent functionality."""
    agent = NewsAgent()
    result = await agent.analyze("BTC/USDT")
    
    assert result is not None
    assert "agent" in result
    assert result["agent"] == "NewsAgent"
    assert "confidence" in result
    assert "action" in result
    assert result["action"] in ["BUY", "SELL", "HOLD"]
    assert 0 <= result["confidence"] <= 1

@pytest.mark.asyncio
async def test_sentiment_agent():
    """Test SentimentAgent functionality."""
    agent = SentimentAgent()
    result = await agent.analyze("BTC/USDT")
    
    assert result is not None
    assert "agent" in result
    assert result["agent"] == "SentimentAgent"
    assert "confidence" in result
    assert "action" in result
    assert result["action"] in ["BUY", "SELL", "HOLD"]
    assert 0 <= result["confidence"] <= 1

@pytest.mark.asyncio
async def test_quant_agent():
    """Test QuantAgent functionality."""
    agent = QuantAgent()
    result = await agent.analyze("BTC/USDT")
    
    assert result is not None
    assert "agent" in result
    assert result["agent"] == "QuantAgent"
    assert "confidence" in result
    assert "action" in result
    assert result["action"] in ["BUY", "SELL", "HOLD"]
    assert 0 <= result["confidence"] <= 1

@pytest.mark.asyncio
async def test_risk_agent():
    """Test RiskAgent functionality."""
    agent = RiskAgent()
    result = await agent.analyze("BTC/USDT")
    
    assert result is not None
    assert "agent" in result
    assert result["agent"] == "RiskAgent"
    assert "action" in result
    assert result["action"] in ["BUY", "SELL", "HOLD", "STOP", "REDUCE", "PROCEED"]

def test_agent_weights():
    """Test that agents have proper weights."""
    agents = [
        NewsAgent(),
        SentimentAgent(),
        QuantAgent(),
        RiskAgent()
    ]
    
    for agent in agents:
        assert agent.weight > 0
        assert isinstance(agent.weight, (int, float))

@pytest.mark.asyncio
async def test_agent_consistency():
    """Test that agents return consistent data structures."""
    agents = [
        NewsAgent(),
        SentimentAgent(),
        QuantAgent(),
        RiskAgent()
    ]
    
    required_fields = ["agent", "confidence", "action", "weight", "reason"]
    
    for agent in agents:
        result = await agent.analyze("BTC/USDT")
        for field in required_fields:
            assert field in result, f"Missing field '{field}' in {agent.name}"
