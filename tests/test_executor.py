import pytest
from app.execution.executor import TradeExecutor

def test_executor_initialization():
    """Test TradeExecutor initialization."""
    executor = TradeExecutor(paper_trading=True)
    
    assert executor.paper_trading == True
    assert executor.exchange_name == "binance"
    assert len(executor.trade_history) == 0

def test_executor_paper_trading_mode():
    """Test executor in paper trading mode."""
    executor = TradeExecutor(paper_trading=True)
    
    assert executor.paper_trading == True
    assert executor.exchange is None  # No real exchange connection

@pytest.mark.asyncio
async def test_executor_buy_trade():
    """Test executing a BUY trade."""
    executor = TradeExecutor(paper_trading=True)
    
    decision = {
        "approved": True,
        "action": "BUY",
        "confidence": 0.9,
        "average_risk": 0.1
    }
    
    result = await executor.execute_trade(decision, "BTC/USDT", order_size=0.01)
    
    assert result["executed"] == True
    assert result["type"] == "paper"
    assert result["action"] == "BUY"
    assert result["symbol"] == "BTC/USDT"

@pytest.mark.asyncio
async def test_executor_sell_trade():
    """Test executing a SELL trade."""
    executor = TradeExecutor(paper_trading=True)
    
    decision = {
        "approved": True,
        "action": "SELL",
        "confidence": 0.85,
        "average_risk": 0.15
    }
    
    result = await executor.execute_trade(decision, "ETH/USDT", order_size=0.5)
    
    assert result["executed"] == True
    assert result["action"] == "SELL"

@pytest.mark.asyncio
async def test_executor_rejected_trade():
    """Test that rejected trades are not executed."""
    executor = TradeExecutor(paper_trading=True)
    
    decision = {
        "approved": False,
        "action": "BUY",
        "confidence": 0.5,
        "average_risk": 0.5
    }
    
    result = await executor.execute_trade(decision, "BTC/USDT")
    
    assert result["executed"] == False
    assert "not approved" in result["reason"]

@pytest.mark.asyncio
async def test_executor_hold_action():
    """Test that HOLD actions don't execute trades."""
    executor = TradeExecutor(paper_trading=True)
    
    decision = {
        "approved": True,
        "action": "HOLD",
        "confidence": 0.5,
        "average_risk": 0.3
    }
    
    result = await executor.execute_trade(decision, "BTC/USDT")
    
    assert result["executed"] == False

@pytest.mark.asyncio
async def test_executor_trade_history():
    """Test trade history tracking."""
    executor = TradeExecutor(paper_trading=True)
    
    decision = {
        "approved": True,
        "action": "BUY",
        "confidence": 0.9,
        "average_risk": 0.1
    }
    
    await executor.execute_trade(decision, "BTC/USDT", order_size=0.01)
    await executor.execute_trade(decision, "ETH/USDT", order_size=0.1)
    
    history = executor.get_trade_history()
    
    assert len(history) == 2
    assert history[0]["symbol"] == "BTC/USDT"
    assert history[1]["symbol"] == "ETH/USDT"

def test_executor_statistics():
    """Test execution statistics."""
    executor = TradeExecutor(paper_trading=True)
    
    stats = executor.get_execution_stats()
    
    assert stats["total_trades"] == 0
    assert stats["mode"] == "PAPER"

@pytest.mark.asyncio
async def test_executor_multiple_trades():
    """Test executing multiple trades."""
    executor = TradeExecutor(paper_trading=True)
    
    symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    
    for symbol in symbols:
        decision = {
            "approved": True,
            "action": "BUY",
            "confidence": 0.85,
            "average_risk": 0.15
        }
        
        result = await executor.execute_trade(decision, symbol)
        assert result["executed"] == True
    
    stats = executor.get_execution_stats()
    assert stats["total_trades"] == 3
    assert stats["buy_trades"] == 3
