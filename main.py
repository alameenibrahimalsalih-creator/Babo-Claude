import asyncio
from app.core.orchestrator import SwarmOrchestrator
from app.core.consensus import ConsensusEngine
from app.agents.news_agent import NewsAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.quant_agent import QuantAgent

async def main():
    print("--- Starting Babo Claude Advanced Swarm ---")
    
    orchestrator = SwarmOrchestrator()
    consensus_engine = ConsensusEngine()

    # Registering the Swarm of Agents
    print("Registering agents...")
    orchestrator.register(NewsAgent())
    orchestrator.register(SentimentAgent())
    orchestrator.register(QuantAgent())

    # Run Multi-Agent Analysis
    symbol = "BTC/USDT"
    print(f"Swarm is analyzing {symbol}...")
    results = await orchestrator.analyze(symbol)

    # Display individual agent findings
    for res in results:
        print(f"  > {res['agent']}: Action={res['action']}, Confidence={res['confidence']:.2f}, Reason={res['reason']}")

    # Evaluate Global Consensus
    decision = consensus_engine.evaluate(results, threshold=0.85)
    
    print("\n--- Final Decision ---")
    print(f"Consensus Score: {decision['score']:.4f}")
    if decision["approved"]:
        print("Status: APPROVED - The swarm has reached a consensus to execute the trade.")
        print("Action: Executing BUY order via Broker API...")
    else:
        print("Status: REJECTED - The swarm could not reach the required 85% consensus.")
        print("Action: Monitoring markets for better entry points.")

if __name__ == "__main__":
    asyncio.run(main())
