import logging
from typing import List, Dict

class ConsensusEngine:
    """
    Consensus Engine for Babo Claude.
    Evaluates votes from all agents and determines final trading decision.
    Incorporates risk assessment and confidence thresholds.
    """
    
    def __init__(self, threshold: float = 0.85, min_agents: int = 2):
        """
        Initialize Consensus Engine.
        
        Args:
            threshold: Minimum consensus score required for approval (0-1)
            min_agents: Minimum number of agents required for consensus
        """
        self.logger = logging.getLogger("BaboClaude.ConsensusEngine")
        self.threshold = threshold
        self.min_agents = min_agents

    def evaluate(self, votes: List[Dict], threshold: float = None) -> Dict:
        """
        Evaluate votes from agents and determine consensus decision.
        
        Args:
            votes: List of vote dictionaries from agents
            threshold: Optional override for consensus threshold
        
        Returns: Decision dictionary with approval status and reasoning
        """
        if threshold is None:
            threshold = self.threshold
        
        if len(votes) < self.min_agents:
            self.logger.warning(f"Insufficient votes: {len(votes)} < {self.min_agents}")
            return {
                "approved": False,
                "score": 0,
                "reason": f"Insufficient votes: {len(votes)} agents < {self.min_agents} required",
                "action": "HOLD",
                "confidence": 0
            }
        
        # Separate votes by action
        buy_votes = [v for v in votes if v.get('action') == 'BUY']
        sell_votes = [v for v in votes if v.get('action') == 'SELL']
        hold_votes = [v for v in votes if v.get('action') == 'HOLD']
        stop_votes = [v for v in votes if v.get('action') == 'STOP']
        reduce_votes = [v for v in votes if v.get('action') == 'REDUCE']
        
        # Check for critical risk signals
        if stop_votes:
            self.logger.warning("🛑 CRITICAL RISK DETECTED: Risk Agent has issued STOP signal.")
            return {
                "approved": False,
                "score": 0,
                "reason": "Critical risk detected. Trading halted by Risk Agent.",
                "action": "STOP",
                "confidence": 0.95,
                "risk_level": "CRITICAL"
            }
        
        # Calculate weighted consensus score
        weighted_score = self._calculate_weighted_score(votes)
        
        # Determine primary action
        action_counts = {
            'BUY': len(buy_votes),
            'SELL': len(sell_votes),
            'HOLD': len(hold_votes),
            'REDUCE': len(reduce_votes)
        }
        
        primary_action = max(action_counts, key=action_counts.get)
        
        # Calculate average risk
        avg_risk = sum(v.get('risk', 0.5) for v in votes) / len(votes)
        
        # Determine approval based on action and score
        approved, confidence = self._determine_approval(
            primary_action, 
            weighted_score, 
            avg_risk, 
            threshold
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            votes, 
            primary_action, 
            weighted_score, 
            avg_risk
        )
        
        decision = {
            "approved": approved,
            "score": weighted_score,
            "action": primary_action,
            "confidence": confidence,
            "risk_level": self._assess_risk_level(avg_risk),
            "reason": reasoning,
            "vote_breakdown": {
                "buy": len(buy_votes),
                "sell": len(sell_votes),
                "hold": len(hold_votes),
                "reduce": len(reduce_votes),
                "total": len(votes)
            },
            "average_risk": avg_risk
        }
        
        self.logger.info(f"📊 Consensus Decision: {primary_action} (Score: {weighted_score:.4f}, Approved: {approved})")
        
        return decision

    def _calculate_weighted_score(self, votes: List[Dict]) -> float:
        """
        Calculate weighted consensus score based on agent confidence and weights.
        
        Returns: Score between 0 and 1
        """
        if not votes:
            return 0
        
        weighted_sum = 0
        total_weight = 0
        
        for vote in votes:
            confidence = vote.get('confidence', 0.5)
            weight = vote.get('weight', 1.0)
            
            # Normalize confidence to 0-1 range
            confidence = max(0, min(1, confidence))
            
            weighted_sum += confidence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        return weighted_sum / total_weight

    def _determine_approval(self, action: str, score: float, 
                           avg_risk: float, threshold: float) -> tuple:
        """
        Determine if the consensus decision should be approved.
        
        Returns: (approved: bool, confidence: float)
        """
        # Risk-adjusted threshold
        risk_adjustment = avg_risk * 0.2  # Risk reduces approval threshold slightly
        adjusted_threshold = threshold - risk_adjustment
        
        if action == 'BUY':
            approved = score >= adjusted_threshold
            confidence = score if approved else 0.5
        elif action == 'SELL':
            approved = score >= adjusted_threshold
            confidence = score if approved else 0.5
        elif action == 'REDUCE':
            approved = True  # Always approve risk reduction
            confidence = 0.8
        else:  # HOLD
            approved = False  # Don't trade on HOLD
            confidence = 0.5
        
        return approved, confidence

    def _assess_risk_level(self, avg_risk: float) -> str:
        """Assess risk level based on average risk score."""
        if avg_risk > 0.75:
            return "CRITICAL"
        elif avg_risk > 0.6:
            return "HIGH"
        elif avg_risk > 0.4:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_reasoning(self, votes: List[Dict], action: str, 
                           score: float, avg_risk: float) -> str:
        """Generate human-readable reasoning for the decision."""
        vote_breakdown = {
            'BUY': len([v for v in votes if v.get('action') == 'BUY']),
            'SELL': len([v for v in votes if v.get('action') == 'SELL']),
            'HOLD': len([v for v in votes if v.get('action') == 'HOLD']),
            'REDUCE': len([v for v in votes if v.get('action') == 'REDUCE'])
        }
        
        total_votes = len(votes)
        action_percentage = (vote_breakdown[action] / total_votes * 100) if total_votes > 0 else 0
        
        reasons = [
            f"Consensus: {action_percentage:.0f}% of agents voted {action}",
            f"Confidence Score: {score:.2%}",
            f"Average Risk: {avg_risk:.2%}",
            f"Vote Distribution: {vote_breakdown['BUY']} BUY, {vote_breakdown['SELL']} SELL, "
            f"{vote_breakdown['HOLD']} HOLD, {vote_breakdown['REDUCE']} REDUCE"
        ]
        
        return " | ".join(reasons)

    def get_consensus_stats(self, votes: List[Dict]) -> Dict:
        """Get detailed consensus statistics."""
        if not votes:
            return {}
        
        return {
            "total_votes": len(votes),
            "average_confidence": sum(v.get('confidence', 0) for v in votes) / len(votes),
            "average_risk": sum(v.get('risk', 0) for v in votes) / len(votes),
            "vote_distribution": {
                "BUY": len([v for v in votes if v.get('action') == 'BUY']),
                "SELL": len([v for v in votes if v.get('action') == 'SELL']),
                "HOLD": len([v for v in votes if v.get('action') == 'HOLD']),
                "REDUCE": len([v for v in votes if v.get('action') == 'REDUCE']),
                "STOP": len([v for v in votes if v.get('action') == 'STOP'])
            }
        }
