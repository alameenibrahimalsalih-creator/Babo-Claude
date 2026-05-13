import logging
from app.agents.base_agent import BaseAgent

class RiskAgent(BaseAgent):
    """
    Risk Assessment Agent that evaluates market conditions and portfolio risk.
    Prevents over-leveraging and ensures risk management protocols are followed.
    """
    name = "RiskAgent"
    weight = 1.8  # High weight due to critical risk management role

    def __init__(self, max_position_size: float = 0.05, max_daily_loss: float = 0.02):
        """
        Initialize Risk Agent with risk parameters.
        
        Args:
            max_position_size: Maximum position size as % of portfolio (default 5%)
            max_daily_loss: Maximum daily loss tolerance as % of portfolio (default 2%)
        """
        self.logger = logging.getLogger("BaboClaude.RiskAgent")
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss
        self.portfolio_value = 10000  # Default starting portfolio
        self.daily_loss = 0  # Track daily loss

    async def analyze(self, symbol: str, other_votes: list = None):
        """
        Analyze risk based on current market conditions and portfolio state.
        
        Args:
            symbol: Trading symbol
            other_votes: Votes from other agents (for risk aggregation)
        
        Returns: Risk assessment vote
        """
        try:
            # Calculate risk metrics
            position_size_risk = self._evaluate_position_size_risk(symbol)
            volatility_risk = self._evaluate_volatility_risk(symbol)
            portfolio_risk = self._evaluate_portfolio_risk()
            correlation_risk = self._evaluate_correlation_risk(symbol, other_votes)
            
            # Aggregate risk scores
            total_risk_score = (position_size_risk + volatility_risk + portfolio_risk + correlation_risk) / 4
            
            # Determine action based on risk
            confidence, action, reason = self._determine_risk_action(
                total_risk_score, 
                position_size_risk, 
                portfolio_risk
            )
            
            return {
                "agent": self.name,
                "confidence": confidence,
                "risk": total_risk_score,
                "action": action,
                "weight": self.weight,
                "reason": reason,
                "risk_breakdown": {
                    "position_size": position_size_risk,
                    "volatility": volatility_risk,
                    "portfolio": portfolio_risk,
                    "correlation": correlation_risk
                }
            }
        except Exception as e:
            self.logger.error(f"Error during risk assessment: {e}")
            return self._simulated_analysis()

    def _evaluate_position_size_risk(self, symbol: str) -> float:
        """
        Evaluate risk based on position size.
        Returns a risk score from 0 (low risk) to 1 (high risk).
        """
        # Simulated position sizing logic
        # In production, this would check actual open positions
        current_position_size = 0.03  # Assume 3% of portfolio
        
        if current_position_size > self.max_position_size:
            return 0.9  # High risk
        elif current_position_size > self.max_position_size * 0.75:
            return 0.6  # Medium-high risk
        else:
            return 0.3  # Low risk

    def _evaluate_volatility_risk(self, symbol: str) -> float:
        """
        Evaluate risk based on market volatility.
        Returns a risk score from 0 (low volatility) to 1 (high volatility).
        """
        # Simulated volatility assessment
        # In production, this would calculate actual volatility from price data
        # Using ATR (Average True Range) or standard deviation
        
        # For now, assume moderate volatility
        volatility_score = 0.45
        
        return volatility_score

    def _evaluate_portfolio_risk(self) -> float:
        """
        Evaluate overall portfolio risk.
        Returns a risk score from 0 (low portfolio risk) to 1 (high portfolio risk).
        """
        # Check daily loss against threshold
        if self.daily_loss > self.max_daily_loss * self.portfolio_value:
            return 0.95  # Critical risk - stop trading
        elif self.daily_loss > self.max_daily_loss * self.portfolio_value * 0.5:
            return 0.7  # High risk - reduce position size
        else:
            return 0.3  # Acceptable risk

    def _evaluate_correlation_risk(self, symbol: str, other_votes: list = None) -> float:
        """
        Evaluate risk of correlated positions.
        Returns a risk score from 0 (low correlation risk) to 1 (high correlation risk).
        """
        if not other_votes:
            return 0.2  # Low correlation risk if no other positions
        
        # Count how many agents are voting BUY/SELL on the same symbol
        buy_votes = sum(1 for vote in other_votes if vote.get('action') == 'BUY')
        total_votes = len(other_votes)
        
        # High consensus = higher correlation risk
        if total_votes == 0:
            return 0.2
        
        consensus_ratio = buy_votes / total_votes
        
        if consensus_ratio > 0.8 or consensus_ratio < 0.2:
            return 0.7  # High correlation risk - too much consensus
        else:
            return 0.3  # Moderate correlation risk

    def _determine_risk_action(self, total_risk_score: float, 
                               position_risk: float, 
                               portfolio_risk: float) -> tuple:
        """
        Determine trading action based on risk assessment.
        Returns: confidence, action, reason
        """
        if portfolio_risk > 0.8:
            return 0.95, "STOP", "CRITICAL: Portfolio risk threshold exceeded. Halting all trades."
        
        if total_risk_score > 0.75:
            return 0.85, "HOLD", "High risk detected. Recommend waiting for better entry conditions."
        
        if total_risk_score > 0.6:
            return 0.7, "REDUCE", "Moderate-high risk. Recommend reducing position size."
        
        if total_risk_score > 0.4:
            return 0.6, "PROCEED", "Acceptable risk level. Proceed with caution."
        
        return 0.5, "PROCEED", "Low risk detected. Safe to proceed with standard position sizing."

    def _simulated_analysis(self):
        """Fallback simulated analysis when real data is unavailable."""
        return {
            "agent": self.name,
            "confidence": 0.7,
            "risk": 0.4,
            "action": "PROCEED",
            "weight": self.weight,
            "reason": "Simulated analysis: Risk assessment in progress."
        }

    def update_daily_loss(self, loss_amount: float):
        """Update daily loss tracking."""
        self.daily_loss += loss_amount
        self.logger.info(f"Daily loss updated: {self.daily_loss}")

    def reset_daily_loss(self):
        """Reset daily loss counter (typically at market close)."""
        self.daily_loss = 0
        self.logger.info("Daily loss counter reset.")
