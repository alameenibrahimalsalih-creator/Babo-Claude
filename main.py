import sys
from app.core.orchestrator import SovereignOrchestrator
from app.core.consensus import ConsensusEngine
from app.agents.news_agent import NewsAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.quant_agent import QuantAgent
from app.ui.telegram_bot import BaboJarvisBot

def main():
    print("--- Initializing Babo Claude Sovereign System ---")
    
    orchestrator = SovereignOrchestrator()
    consensus_engine = ConsensusEngine()

    # Registering the Swarm
    orchestrator.register_agent(NewsAgent())
    orchestrator.register_agent(SentimentAgent())
    orchestrator.register_agent(QuantAgent())

    if len(sys.argv) > 1 and sys.argv[1] == "--telegram":
        # Run in Jarvis/Telegram Mode
        bot = BaboJarvisBot(orchestrator, consensus_engine)
        bot.run()
    else:
        print("Please run with --telegram to start the Jarvis interface.")

if __name__ == "__main__":
    main()
