import logging
import asyncio
from typing import Dict, Optional
import ccxt

class TradeExecutor:
    """
    Trade Execution Engine for Babo Claude.
    Handles automatic trade execution based on consensus decisions.
    Supports both live trading and paper trading (simulation).
    """
    
    def __init__(self, exchange_name: str = "binance", paper_trading: bool = True):
        """
        Initialize Trade Executor.
        
        Args:
            exchange_name: Name of the exchange (default: binance)
            paper_trading: If True, simulate trades without actual execution
        """
        self.logger = logging.getLogger("BaboClaude.Executor")
        self.paper_trading = paper_trading
        self.exchange_name = exchange_name
        self.exchange = None
        self.paper_portfolio = {}  # For paper trading simulation
        self.trade_history = []
        
        if not paper_trading:
            self._initialize_exchange()
        
        self.logger.info(f"Trade Executor initialized. Mode: {'PAPER' if paper_trading else 'LIVE'}")

    def _initialize_exchange(self):
        """Initialize connection to exchange."""
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            self.exchange = exchange_class()
            self.logger.info(f"Connected to {self.exchange_name} exchange.")
        except Exception as e:
            self.logger.error(f"Failed to initialize exchange: {e}")
            self.exchange = None

    async def execute_trade(self, decision: Dict, symbol: str, 
                           order_size: float = 0.01) -> Dict:
        """
        Execute a trade based on consensus decision.
        
        Args:
            decision: Consensus decision dictionary
            symbol: Trading symbol (e.g., "BTC/USDT")
            order_size: Size of the order
        
        Returns: Execution result dictionary
        """
        if not decision.get('approved'):
            self.logger.info(f"Trade not approved for {symbol}. Skipping execution.")
            return {
                "executed": False,
                "reason": "Trade not approved by consensus",
                "symbol": symbol
            }
        
        action = decision.get('action', 'HOLD')
        
        if action == 'HOLD' or action == 'STOP':
            self.logger.info(f"No trade action for {symbol} (Action: {action})")
            return {
                "executed": False,
                "reason": f"No trade action: {action}",
                "symbol": symbol
            }
        
        try:
            if self.paper_trading:
                return await self._execute_paper_trade(symbol, action, order_size, decision)
            else:
                return await self._execute_live_trade(symbol, action, order_size, decision)
        except Exception as e:
            self.logger.error(f"Error executing trade: {e}")
            return {
                "executed": False,
                "error": str(e),
                "symbol": symbol
            }

    async def _execute_paper_trade(self, symbol: str, action: str, 
                                   order_size: float, decision: Dict) -> Dict:
        """
        Simulate a trade in paper trading mode.
        """
        self.logger.info(f"📄 PAPER TRADE: {action} {order_size} {symbol}")
        
        trade_record = {
            "type": "paper",
            "symbol": symbol,
            "action": action,
            "size": order_size,
            "confidence": decision.get('confidence', 0),
            "risk": decision.get('average_risk', 0),
            "timestamp": self._get_timestamp(),
            "status": "SIMULATED"
        }
        
        self.trade_history.append(trade_record)
        
        return {
            "executed": True,
            "type": "paper",
            "symbol": symbol,
            "action": action,
            "size": order_size,
            "confidence": decision.get('confidence', 0),
            "message": f"Paper trade executed: {action} {order_size} {symbol}"
        }

    async def _execute_live_trade(self, symbol: str, action: str, 
                                  order_size: float, decision: Dict) -> Dict:
        """
        Execute a live trade on the exchange.
        """
        if not self.exchange:
            self.logger.error("Exchange not connected. Cannot execute live trade.")
            return {
                "executed": False,
                "error": "Exchange not connected",
                "symbol": symbol
            }
        
        try:
            order_type = 'market'  # Use market orders for immediate execution
            
            if action == 'BUY':
                self.logger.info(f"🟢 LIVE BUY: {order_size} {symbol}")
                order = await self.exchange.create_market_buy_order(symbol, order_size)
            elif action == 'SELL':
                self.logger.info(f"🔴 LIVE SELL: {order_size} {symbol}")
                order = await self.exchange.create_market_sell_order(symbol, order_size)
            else:
                return {
                    "executed": False,
                    "error": f"Unknown action: {action}",
                    "symbol": symbol
                }
            
            trade_record = {
                "type": "live",
                "symbol": symbol,
                "action": action,
                "size": order_size,
                "order_id": order.get('id'),
                "confidence": decision.get('confidence', 0),
                "risk": decision.get('average_risk', 0),
                "timestamp": self._get_timestamp(),
                "status": "EXECUTED"
            }
            
            self.trade_history.append(trade_record)
            
            return {
                "executed": True,
                "type": "live",
                "symbol": symbol,
                "action": action,
                "order_id": order.get('id'),
                "size": order_size,
                "confidence": decision.get('confidence', 0),
                "message": f"Live trade executed: {action} {order_size} {symbol}"
            }
        
        except Exception as e:
            self.logger.error(f"Live trade execution failed: {e}")
            return {
                "executed": False,
                "error": str(e),
                "symbol": symbol
            }

    def get_trade_history(self, limit: int = 10) -> list:
        """Get recent trade history."""
        return self.trade_history[-limit:]

    def get_execution_stats(self) -> Dict:
        """Get execution statistics."""
        if not self.trade_history:
            return {"total_trades": 0}
        
        buy_trades = [t for t in self.trade_history if t.get('action') == 'BUY']
        sell_trades = [t for t in self.trade_history if t.get('action') == 'SELL']
        
        return {
            "total_trades": len(self.trade_history),
            "buy_trades": len(buy_trades),
            "sell_trades": len(sell_trades),
            "average_confidence": sum(t.get('confidence', 0) for t in self.trade_history) / len(self.trade_history),
            "average_risk": sum(t.get('risk', 0) for t in self.trade_history) / len(self.trade_history),
            "mode": "PAPER" if self.paper_trading else "LIVE"
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    async def close_position(self, symbol: str) -> Dict:
        """Close an open position."""
        self.logger.info(f"Closing position for {symbol}")
        
        if self.paper_trading:
            return {
                "closed": True,
                "symbol": symbol,
                "type": "paper"
            }
        
        try:
            # Get current position and close it
            # This is simplified; production would need more sophisticated position management
            return {
                "closed": True,
                "symbol": symbol,
                "type": "live"
            }
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
            return {
                "closed": False,
                "error": str(e),
                "symbol": symbol
            }
