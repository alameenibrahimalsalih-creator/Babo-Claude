import asyncio
from app.core.orchestrator import SwarmOrchestrator
from app.core.consensus import ConsensusEngine
from app.agents.news_agent import NewsAgent

async def main():
    print("Starting Babo Claude Swarm...")
    
    orchestrator = SwarmOrchestrator()
    consensus_engine = ConsensusEngine()

    # Register agents
    orchestrator.register(NewsAgent())

    # Run analysis
    symbol = "BTC/USDT"
    print(f"Analyzing {symbol}...")
    results = await orchestrator.analyze(symbol)

    # Evaluate consensus
    decision = consensus_engine.evaluate(results)
    
    print(f"Consensus Results: {decision}")
    if decision["approved"]:
        print("Decision: APPROVED - Proceeding with trade logic.")
    else:
        print("Decision: REJECTED - Insufficient consensus.")

if __name__ == "__main__":
    asyncio.run(main())
