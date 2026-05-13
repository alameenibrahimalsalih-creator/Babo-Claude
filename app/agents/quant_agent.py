import numpy as np
import ccxt
import logging
from app.agents.base_agent import BaseAgent

class QuantAgent(BaseAgent):
    """
    Quantitative Analysis Agent using real market data from CCXT.
    Performs technical analysis using Moving Averages, RSI, MACD, and Bollinger Bands.
    """
    name = "QuantAgent"
    weight = 1.5

    def __init__(self):
        self.logger = logging.getLogger("BaboClaude.QuantAgent")
        try:
            self.exchange = ccxt.binance()
            self.logger.info("CCXT Binance exchange initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize CCXT: {e}")
            self.exchange = None

    async def analyze(self, symbol: str):
        """
        Perform quantitative analysis on the given symbol.
        Returns a vote with confidence, risk assessment, and trading action.
        """
        try:
            if not self.exchange:
                self.logger.warning("Exchange not available, returning simulated analysis.")
                return self._simulated_analysis(symbol)

            # Fetch OHLCV data (4-hour timeframe)
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe='4h', limit=100)
            closes = np.array([candle[4] for candle in ohlcv])
            
            # Calculate technical indicators
            ma_fast = self._calculate_sma(closes, 50)
            ma_slow = self._calculate_sma(closes, 200)
            rsi = self._calculate_rsi(closes, 14)
            macd_line, signal_line = self._calculate_macd(closes)
            bb_upper, bb_lower, bb_middle = self._calculate_bollinger_bands(closes, 20, 2)
            
            # Determine trading signals
            confidence, risk, action, reason = self._evaluate_signals(
                ma_fast, ma_slow, rsi, macd_line, signal_line, 
                bb_upper, bb_lower, closes[-1]
            )
            
            return {
                "agent": self.name,
                "confidence": confidence,
                "risk": risk,
                "action": action,
                "weight": self.weight,
                "reason": reason,
                "indicators": {
                    "ma_fast": float(ma_fast[-1]) if len(ma_fast) > 0 else None,
                    "ma_slow": float(ma_slow[-1]) if len(ma_slow) > 0 else None,
                    "rsi": float(rsi[-1]) if len(rsi) > 0 else None,
                    "macd": float(macd_line[-1]) if len(macd_line) > 0 else None
                }
            }
        except Exception as e:
            self.logger.error(f"Error during quantitative analysis: {e}")
            return self._simulated_analysis(symbol)

    def _simulated_analysis(self, symbol: str):
        """Fallback simulated analysis when real data is unavailable."""
        return {
            "agent": self.name,
            "confidence": 0.75,
            "risk": 0.15,
            "action": "HOLD",
            "weight": self.weight,
            "reason": "Simulated analysis: Real data unavailable. Awaiting market data."
        }

    def _calculate_sma(self, data, period):
        """Calculate Simple Moving Average."""
        return np.convolve(data, np.ones(period) / period, mode='valid')

    def _calculate_rsi(self, data, period=14):
        """Calculate Relative Strength Index."""
        deltas = np.diff(data)
        seed = deltas[:period + 1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = np.zeros_like(data)
        rsi[:period] = 100. - 100. / (1. + rs)
        
        for i in range(period, len(data)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down if down != 0 else 0
            rsi[i] = 100. - 100. / (1. + rs)
        
        return rsi

    def _calculate_macd(self, data, fast=12, slow=26, signal=9):
        """Calculate MACD (Moving Average Convergence Divergence)."""
        ema_fast = self._calculate_ema(data, fast)
        ema_slow = self._calculate_ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self._calculate_ema(macd_line, signal)
        return macd_line, signal_line

    def _calculate_ema(self, data, period):
        """Calculate Exponential Moving Average."""
        return np.array(data).ewm(span=period, adjust=False).mean()

    def _calculate_bollinger_bands(self, data, period=20, std_dev=2):
        """Calculate Bollinger Bands."""
        sma = self._calculate_sma(data, period)
        # Pad to match original length
        sma_padded = np.concatenate([np.full(period - 1, sma[0]), sma])
        
        std = np.std(data[-period:])
        upper = sma_padded[-1] + (std * std_dev)
        lower = sma_padded[-1] - (std * std_dev)
        middle = sma_padded[-1]
        
        return upper, lower, middle

    def _evaluate_signals(self, ma_fast, ma_slow, rsi, macd_line, signal_line, 
                         bb_upper, bb_lower, current_price):
        """
        Evaluate all technical signals and determine trading action.
        Returns: confidence, risk, action, reason
        """
        signals = []
        
        # Golden Cross / Death Cross
        if len(ma_fast) > 0 and len(ma_slow) > 0:
            if ma_fast[-1] > ma_slow[-1]:
                signals.append(("Golden Cross", 0.9, "BUY"))
            else:
                signals.append(("Death Cross", 0.8, "SELL"))
        
        # RSI Signals
        if len(rsi) > 0:
            if rsi[-1] < 30:
                signals.append(("RSI Oversold", 0.85, "BUY"))
            elif rsi[-1] > 70:
                signals.append(("RSI Overbought", 0.85, "SELL"))
        
        # MACD Signals
        if len(macd_line) > 1 and len(signal_line) > 1:
            if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
                signals.append(("MACD Bullish Crossover", 0.88, "BUY"))
            elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
                signals.append(("MACD Bearish Crossover", 0.88, "SELL"))
        
        # Bollinger Bands
        if current_price < bb_lower:
            signals.append(("Price Below Lower Band", 0.75, "BUY"))
        elif current_price > bb_upper:
            signals.append(("Price Above Upper Band", 0.75, "SELL"))
        
        # Aggregate signals
        if not signals:
            return 0.5, 0.2, "HOLD", "No clear technical signals detected."
        
        # Count BUY vs SELL signals
        buy_signals = sum(1 for _, _, action in signals if action == "BUY")
        sell_signals = sum(1 for _, _, action in signals if action == "SELL")
        
        avg_confidence = np.mean([conf for _, conf, _ in signals])
        
        if buy_signals > sell_signals:
            action = "BUY"
            reason = f"Multiple bullish signals detected: {', '.join([sig[0] for sig in signals if sig[2] == 'BUY'])}"
        elif sell_signals > buy_signals:
            action = "SELL"
            reason = f"Multiple bearish signals detected: {', '.join([sig[0] for sig in signals if sig[2] == 'SELL'])}"
        else:
            action = "HOLD"
            reason = "Mixed signals detected. Awaiting clearer market direction."
        
        risk = 0.1 + (0.1 * abs(buy_signals - sell_signals) / max(len(signals), 1))
        
        return avg_confidence, risk, action, reason
