import pytest
from app.core.consensus import ConsensusEngine

def test_consensus_engine_initialization():
    """Test ConsensusEngine initialization."""
    engine = ConsensusEngine(threshold=0.85, min_agents=2)
    
    assert engine.threshold == 0.85
    assert engine.min_agents == 2

def test_consensus_with_insufficient_votes():
    """Test consensus with insufficient votes."""
    engine = ConsensusEngine(min_agents=3)
    votes = [
        {"agent": "Agent1", "confidence": 0.9, "action": "BUY", "weight": 1.0}
    ]
    
    decision = engine.evaluate(votes)
    
    assert decision["approved"] == False
    assert decision["score"] == 0
    assert "Insufficient votes" in decision["reason"]

def test_consensus_with_critical_risk():
    """Test consensus with critical risk signal."""
    engine = ConsensusEngine()
    votes = [
        {"agent": "Agent1", "confidence": 0.9, "action": "BUY", "weight": 1.0, "risk": 0.1},
        {"agent": "RiskAgent", "confidence": 0.95, "action": "STOP", "weight": 1.8, "risk": 0.95}
    ]
    
    decision = engine.evaluate(votes)
    
    assert decision["approved"] == False
    assert decision["action"] == "STOP"
    assert "Critical risk" in decision["reason"]

def test_consensus_buy_decision():
    """Test consensus for BUY decision."""
    engine = ConsensusEngine(threshold=0.7)
    votes = [
        {"agent": "Agent1", "confidence": 0.9, "action": "BUY", "weight": 1.5, "risk": 0.1},
        {"agent": "Agent2", "confidence": 0.85, "action": "BUY", "weight": 1.2, "risk": 0.15},
        {"agent": "Agent3", "confidence": 0.8, "action": "HOLD", "weight": 1.0, "risk": 0.2}
    ]
    
    decision = engine.evaluate(votes)
    
    assert decision["action"] == "BUY"
    assert decision["approved"] == True
    assert decision["score"] > 0.7

def test_consensus_sell_decision():
    """Test consensus for SELL decision."""
    engine = ConsensusEngine(threshold=0.7)
    votes = [
        {"agent": "Agent1", "confidence": 0.88, "action": "SELL", "weight": 1.5, "risk": 0.2},
        {"agent": "Agent2", "confidence": 0.82, "action": "SELL", "weight": 1.2, "risk": 0.25},
        {"agent": "Agent3", "confidence": 0.75, "action": "HOLD", "weight": 1.0, "risk": 0.15}
    ]
    
    decision = engine.evaluate(votes)
    
    assert decision["action"] == "SELL"
    assert decision["approved"] == True

def test_consensus_hold_decision():
    """Test consensus for HOLD decision."""
    engine = ConsensusEngine()
    votes = [
        {"agent": "Agent1", "confidence": 0.6, "action": "HOLD", "weight": 1.0, "risk": 0.3},
        {"agent": "Agent2", "confidence": 0.55, "action": "HOLD", "weight": 1.0, "risk": 0.35},
        {"agent": "Agent3", "confidence": 0.5, "action": "HOLD", "weight": 1.0, "risk": 0.4}
    ]
    
    decision = engine.evaluate(votes)
    
    assert decision["action"] == "HOLD"
    assert decision["approved"] == False

def test_consensus_weighted_scoring():
    """Test weighted consensus scoring."""
    engine = ConsensusEngine()
    votes = [
        {"agent": "Agent1", "confidence": 1.0, "action": "BUY", "weight": 2.0, "risk": 0.1},
        {"agent": "Agent2", "confidence": 0.5, "action": "BUY", "weight": 1.0, "risk": 0.2}
    ]
    
    decision = engine.evaluate(votes)
    
    # With weights, Agent1's vote should have more influence
    expected_score = (1.0 * 2.0 + 0.5 * 1.0) / (2.0 + 1.0)
    assert abs(decision["score"] - expected_score) < 0.01

def test_consensus_risk_assessment():
    """Test risk assessment in consensus."""
    engine = ConsensusEngine()
    votes = [
        {"agent": "Agent1", "confidence": 0.9, "action": "BUY", "weight": 1.0, "risk": 0.8},
        {"agent": "Agent2", "confidence": 0.85, "action": "BUY", "weight": 1.0, "risk": 0.75}
    ]
    
    decision = engine.evaluate(votes)
    
    assert decision["risk_level"] == "HIGH"
    assert decision["average_risk"] > 0.7

def test_consensus_stats():
    """Test consensus statistics generation."""
    engine = ConsensusEngine()
    votes = [
        {"agent": "Agent1", "confidence": 0.9, "action": "BUY", "weight": 1.0, "risk": 0.1},
        {"agent": "Agent2", "confidence": 0.85, "action": "BUY", "weight": 1.0, "risk": 0.15},
        {"agent": "Agent3", "confidence": 0.75, "action": "SELL", "weight": 1.0, "risk": 0.2}
    ]
    
    stats = engine.get_consensus_stats(votes)
    
    assert stats["total_votes"] == 3
    assert stats["vote_distribution"]["BUY"] == 2
    assert stats["vote_distribution"]["SELL"] == 1
    assert stats["average_confidence"] > 0.75
