import sys
import logging
from app.core.orchestrator import SovereignOrchestrator
from app.core.consensus import ConsensusEngine
from app.agents.news_agent import NewsAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.quant_agent import QuantAgent
from app.agents.risk_agent import RiskAgent
from app.ui.telegram_bot import BaboJarvisBot
from app.execution.executor import TradeExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def print_banner():
    """Print system initialization banner."""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         🤖 BABO CLAUDE - SOVEREIGN TRADING SYSTEM 🤖      ║
    ║                                                            ║
    ║    Multi-Agent Financial Intelligence Platform            ║
    ║    Powered by Jarvis-inspired AI & Swarm Intelligence     ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    print("--- Initializing Babo Claude Sovereign System ---\n")
    
    # Initialize core components
    orchestrator = SovereignOrchestrator()
    consensus_engine = ConsensusEngine(threshold=0.85)
    executor = TradeExecutor(paper_trading=True)  # Start with paper trading
    
    # Register the Swarm of Agents
    print("📊 Registering Swarm Agents...")
    
    agents = [
        NewsAgent(),
        SentimentAgent(),
        QuantAgent(),
        RiskAgent()
    ]
    
    for agent in agents:
        orchestrator.register_agent(agent)
        print(f"  ✅ {agent.name} registered (Weight: {agent.weight})")
    
    print(f"\n✨ Swarm initialized with {len(orchestrator.agents)} agents\n")
    
    # Print swarm status
    status = orchestrator.get_swarm_status()
    print("🤖 Swarm Configuration:")
    for agent_info in status.get('agents', []):
        print(f"  • {agent_info.get('name')}: Weight={agent_info.get('weight'):.2f}")
    
    print("\n" + "="*60)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--telegram":
            print("\n🚀 Starting Telegram Bot Interface...\n")
            bot = BaboJarvisBot(orchestrator, consensus_engine, executor)
            bot.run()
        elif sys.argv[1] == "--test":
            print("\n🧪 Running Test Mode...\n")
            asyncio.run(test_swarm(orchestrator, consensus_engine, executor))
        else:
            print(f"\n❌ Unknown argument: {sys.argv[1]}")
            print_help()
    else:
        print_help()

def print_help():
    """Print help message."""
    help_text = """
    Usage: python main.py [OPTIONS]
    
    Options:
      --telegram    Start the Telegram Bot interface for trading
      --test        Run in test mode with sample analysis
      --help        Show this help message
    
    Example:
      python main.py --telegram
    
    Environment Variables:
      TELEGRAM_BOT_TOKEN    Your Telegram bot token
      BINANCE_API_KEY       Your Binance API key (for live trading)
      BINANCE_SECRET        Your Binance API secret (for live trading)
    
    For more information, visit: https://github.com/alameenibrahimalsalih-creator/Babo-Claude
    """
    print(help_text)

async def test_swarm(orchestrator, consensus_engine, executor):
    """Test the swarm with sample analysis."""
    import asyncio
    
    print("Testing Babo Claude Swarm Intelligence...\n")
    
    test_symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    
    for symbol in test_symbols:
        print(f"\n{'='*60}")
        print(f"Analyzing: {symbol}")
        print(f"{'='*60}\n")
        
        # Run swarm analysis
        results = await orchestrator.run_swarm_analysis(symbol)
        
        # Get consensus decision
        decision = consensus_engine.evaluate(results)
        
        # Print results
        print("Agent Votes:")
        for res in results:
            print(f"  • {res.get('agent')}: {res.get('action')} (Confidence: {res.get('confidence'):.1%})")
        
        print(f"\nConsensus Decision:")
        print(f"  Action: {decision.get('action')}")
        print(f"  Score: {decision.get('score'):.2%}")
        print(f"  Approved: {decision.get('approved')}")
        print(f"  Risk Level: {decision.get('risk_level')}")
        
        # Execute trade if approved
        if decision.get('approved'):
            execution = await executor.execute_trade(decision, symbol)
            print(f"\nExecution Result:")
            print(f"  Executed: {execution.get('executed')}")
            if execution.get('executed'):
                print(f"  Type: {execution.get('type')}")
                print(f"  Message: {execution.get('message')}")
    
    print(f"\n{'='*60}")
    print("Test Complete!")
    print(f"{'='*60}\n")
    
    # Print execution statistics
    stats = executor.get_execution_stats()
    print("Execution Statistics:")
    print(f"  Total Trades: {stats.get('total_trades')}")
    print(f"  Buy Trades: {stats.get('buy_trades')}")
    print(f"  Sell Trades: {stats.get('sell_trades')}")
    print(f"  Average Confidence: {stats.get('average_confidence'):.1%}")
    print(f"  Average Risk: {stats.get('average_risk'):.1%}")

if __name__ == "__main__":
    import asyncio
    main()
