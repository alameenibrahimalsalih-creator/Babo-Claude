import asyncio
import sys
from app.core.orchestrator import SwarmOrchestrator
from app.core.consensus import ConsensusEngine
from app.agents.news_agent import NewsAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.quant_agent import QuantAgent
from app.ui.telegram_bot import BaboTelegramBot

async def run_cli(orchestrator, consensus_engine):
    symbol = "BTC/USDT"
    print(f"--- CLI Mode: Analyzing {symbol} ---")
    results = await orchestrator.analyze(symbol)
    for res in results:
        print(f"  > {res['agent']}: {res['action']} ({res['confidence']:.2f})")
    decision = consensus_engine.evaluate(results)
    print(f"Final Decision: {decision}")

def main():
    orchestrator = SwarmOrchestrator()
    consensus_engine = ConsensusEngine()

    # Register Agents
    orchestrator.register(NewsAgent())
    orchestrator.register(SentimentAgent())
    orchestrator.register(QuantAgent())

    if len(sys.argv) > 1 and sys.argv[1] == "--telegram":
        # Run in Telegram Mode
        bot = BaboTelegramBot(orchestrator, consensus_engine)
        bot.run()
    else:
        # Run in CLI Mode (Default)
        asyncio.run(run_cli(orchestrator, consensus_engine))

if __name__ == "__main__":
    main()
