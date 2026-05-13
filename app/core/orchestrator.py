import asyncio
import logging
import json
from typing import List, Dict
from datetime import datetime
from app.agents.base_agent import BaseAgent

class SovereignOrchestrator:
    """
    Sovereign Agent Engine inspired by Claw-Code.
    Manages a swarm of specialized financial agents with self-evolution capabilities.
    """
    def __init__(self, history_file: str = "swarm_history.json"):
        self.agents: List[BaseAgent] = []
        self.logger = logging.getLogger("BaboClaude.Orchestrator")
        self.history_file = history_file
        self.performance_history = self._load_history()
        self.agent_performance = {}  # Track each agent's accuracy

    def register_agent(self, agent: BaseAgent):
        """Register a new agent to the swarm."""
        self.agents.append(agent)
        self.agent_performance[agent.name] = {
            "total_votes": 0,
            "correct_votes": 0,
            "accuracy": 0.0,
            "weight_adjustment": 0.0
        }
        self.logger.info(f"Agent {agent.name} registered to the swarm. Current swarm size: {len(self.agents)}")

    async def run_swarm_analysis(self, symbol: str) -> List[Dict]:
        """
        Execute parallel analysis across all agents.
        Returns a list of votes from each agent.
        """
        self.logger.info(f"🔄 Initiating swarm intelligence analysis for {symbol}...")
        self.logger.info(f"📊 Swarm size: {len(self.agents)} agents")
        
        tasks = [agent.analyze(symbol) for agent in self.agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Agent {self.agents[i].name} failed: {result}")
            else:
                valid_results.append(result)
        
        self.logger.info(f"✅ Swarm analysis complete. Received {len(valid_results)}/{len(self.agents)} votes.")
        return valid_results

    async def self_evolve(self, feedback_data: Dict = None):
        """
        Self-evolution protocol: Agents analyze their past performance and adjust weights.
        
        This allows the swarm to learn from historical data and improve accuracy over time.
        """
        self.logger.info("🧬 Initiating self-evolution protocol...")
        
        if not feedback_data:
            self.logger.warning("No feedback data provided for evolution.")
            return
        
        # Analyze each agent's performance
        for agent in self.agents:
            if agent.name in self.agent_performance:
                perf = self.agent_performance[agent.name]
                
                # Calculate accuracy
                if perf["total_votes"] > 0:
                    accuracy = perf["correct_votes"] / perf["total_votes"]
                    perf["accuracy"] = accuracy
                    
                    # Adjust weight based on performance
                    # Agents with higher accuracy get higher weights
                    if accuracy > 0.7:
                        weight_adjustment = 1.2  # Increase weight by 20%
                    elif accuracy > 0.5:
                        weight_adjustment = 1.0  # Keep weight same
                    else:
                        weight_adjustment = 0.8  # Decrease weight by 20%
                    
                    perf["weight_adjustment"] = weight_adjustment
                    agent.weight *= weight_adjustment
                    
                    self.logger.info(
                        f"🔧 {agent.name}: Accuracy={accuracy:.2%}, "
                        f"New Weight={agent.weight:.2f}"
                    )
        
        # Save evolution history
        self._save_history()

    def record_agent_vote(self, agent_name: str, was_correct: bool):
        """
        Record whether an agent's vote was correct for future learning.
        
        Args:
            agent_name: Name of the agent
            was_correct: Whether the agent's prediction was correct
        """
        if agent_name in self.agent_performance:
            perf = self.agent_performance[agent_name]
            perf["total_votes"] += 1
            if was_correct:
                perf["correct_votes"] += 1

    def get_swarm_status(self) -> Dict:
        """Get current status of the swarm."""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(self.agents),
            "agents": [
                {
                    "name": agent.name,
                    "weight": agent.weight,
                    "performance": self.agent_performance.get(agent.name, {})
                }
                for agent in self.agents
            ],
            "performance_history": self.performance_history
        }

    def _load_history(self) -> List[Dict]:
        """Load swarm performance history from file."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.info(f"No history file found. Starting fresh.")
            return []
        except Exception as e:
            self.logger.error(f"Error loading history: {e}")
            return []

    def _save_history(self):
        """Save swarm performance history to file."""
        try:
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "agents": [
                    {
                        "name": agent.name,
                        "weight": agent.weight,
                        "performance": self.agent_performance.get(agent.name, {})
                    }
                    for agent in self.agents
                ]
            }
            self.performance_history.append(history_entry)
            
            with open(self.history_file, 'w') as f:
                json.dump(self.performance_history, f, indent=2)
            
            self.logger.info(f"History saved to {self.history_file}")
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")

    def get_agent_by_name(self, name: str) -> BaseAgent:
        """Get an agent by name."""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def remove_agent(self, name: str) -> bool:
        """Remove an agent from the swarm."""
        for i, agent in enumerate(self.agents):
            if agent.name == name:
                self.agents.pop(i)
                self.logger.info(f"Agent {name} removed from swarm.")
                return True
        return False
