# 🤖 Babo Claude - Sovereign Financial Trading System

> **Advanced Multi-Agent AI Trading Platform with Swarm Intelligence & Self-Evolution**

Babo Claude is a cutting-edge autonomous trading system that leverages swarm intelligence, consensus algorithms, and self-evolving agents to make sophisticated financial trading decisions. Inspired by Jarvis and powered by Claw-Code architecture, it represents the next generation of AI-driven financial analysis and execution.

## ✨ Key Features

### 🧠 Multi-Agent Swarm Intelligence
- **NewsAgent**: Real-time financial news analysis and sentiment tracking
- **SentimentAgent**: Advanced sentiment analysis using transformer models
- **QuantAgent**: Technical analysis with moving averages, RSI, MACD, and Bollinger Bands
- **RiskAgent**: Comprehensive risk assessment and portfolio protection
- **Sovereign Orchestrator**: Manages agent coordination and consensus

### 🎯 Consensus Protocol
- Weighted voting system based on agent confidence and historical accuracy
- Risk-adjusted decision thresholds
- Critical risk detection and trading halts
- Transparent reasoning for all trading decisions

### 🔄 Self-Evolution System
- Agents learn from historical performance
- Dynamic weight adjustment based on prediction accuracy
- Continuous improvement through feedback loops
- Performance tracking and analytics

### 🚀 Autonomous Execution
- **Paper Trading**: Risk-free simulation mode for testing
- **Live Trading**: Direct exchange integration via CCXT
- Market and limit order support
- Position management and risk controls

### 💬 Jarvis-Inspired Interface
- Interactive Telegram bot for real-time control
- Natural language command support (English & Arabic)
- Detailed swarm analysis reports
- Trade history and performance metrics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Telegram Interface                    │
│              (Jarvis-Inspired User Control)              │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│              Sovereign Orchestrator                      │
│         (Multi-Agent Coordination Engine)                │
└──────────────────────────┬──────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬────────────┐
        │                  │                  │            │
    ┌───▼────┐        ┌───▼────┐        ┌───▼────┐   ┌──▼────┐
    │  News  │        │Sentiment│        │ Quant  │   │ Risk  │
    │ Agent  │        │ Agent   │        │ Agent  │   │ Agent │
    └────────┘        └────────┘        └────────┘   └───────┘
        │                  │                  │            │
        └──────────────────┼──────────────────┴────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│              Consensus Engine                           │
│         (Decision Making & Risk Assessment)             │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│              Trade Executor                             │
│    (Paper Trading & Live Exchange Integration)          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry
- Telegram Bot Token (from @BotFather)
- (Optional) Binance API Keys for live trading

### Installation

```bash
# Clone the repository
git clone https://github.com/alameenibrahimalsalih-creator/Babo-Claude.git
cd Babo-Claude

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Create a `.env` file in the project root:

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Binance Configuration (for live trading)
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET=your_binance_secret

# System Configuration
CONSENSUS_THRESHOLD=0.85
PAPER_TRADING=true
```

### Running the System

#### Telegram Bot Mode (Recommended for beginners)
```bash
python main.py --telegram
```

#### Test Mode (Verify system functionality)
```bash
python main.py --test
```

#### Help
```bash
python main.py --help
```

## 📊 Using the Telegram Bot

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize the bot and show menu | `/start` |
| `/analyze <symbol>` | Analyze a trading symbol | `/analyze BTC/USDT` |
| `/status` | Show current swarm status | `/status` |
| `/history` | View recent trade history | `/history` |
| `/help` | Show help message | `/help` |

### Natural Language Queries

- "Who are you?" → Bot introduces itself
- "عرف نفسك" → Arabic: Bot introduces itself
- "Analyze BTC/USDT" → Triggers analysis
- "حلل BTC/USDT" → Arabic: Triggers analysis

## 🧪 Testing

Run the comprehensive test suite to verify system functionality:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app
```

### Test Coverage
- **test_agents.py**: Individual agent functionality
- **test_consensus.py**: Consensus engine logic
- **test_executor.py**: Trade execution system

## 📈 Performance Metrics

The system tracks and displays:
- **Agent Accuracy**: Percentage of correct predictions
- **Consensus Score**: Weighted average confidence
- **Risk Assessment**: Current portfolio risk level
- **Trade Statistics**: Win rate, average confidence, execution count

## 🔐 Risk Management

### Built-in Protections
- Position size limits (default 5% of portfolio)
- Daily loss thresholds (default 2%)
- Volatility assessment
- Correlation risk detection
- Critical risk halts (STOP signals)

### Risk Levels
- **LOW**: Safe to proceed with standard sizing
- **MEDIUM**: Proceed with caution
- **HIGH**: Reduce position sizes
- **CRITICAL**: Halt all trading

## 🔄 Self-Evolution Protocol

The system continuously improves through:

1. **Performance Tracking**: Records accuracy of each agent's predictions
2. **Weight Adjustment**: Agents with higher accuracy get higher weights
3. **History Logging**: Maintains detailed performance history
4. **Feedback Integration**: Learns from market outcomes

## 🛠️ Advanced Configuration

### Adjusting Consensus Threshold
```python
# In main.py
consensus_engine = ConsensusEngine(threshold=0.90)  # More conservative
```

### Enabling Live Trading
```python
# In main.py
executor = TradeExecutor(paper_trading=False)  # CAUTION: Real money!
```

### Adding Custom Agents
```python
from app.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    name = "CustomAgent"
    weight = 1.0
    
    async def analyze(self, symbol: str):
        # Your analysis logic here
        return {
            "agent": self.name,
            "confidence": 0.75,
            "action": "BUY",
            "weight": self.weight,
            "reason": "Custom analysis result"
        }

# Register in main.py
orchestrator.register_agent(CustomAgent())
```

## 📚 API Reference

### SovereignOrchestrator
```python
orchestrator = SovereignOrchestrator()

# Register an agent
orchestrator.register_agent(agent)

# Run swarm analysis
results = await orchestrator.run_swarm_analysis("BTC/USDT")

# Trigger self-evolution
await orchestrator.self_evolve()

# Get swarm status
status = orchestrator.get_swarm_status()
```

### ConsensusEngine
```python
consensus = ConsensusEngine(threshold=0.85)

# Evaluate votes
decision = consensus.evaluate(votes)

# Get statistics
stats = consensus.get_consensus_stats(votes)
```

### TradeExecutor
```python
executor = TradeExecutor(paper_trading=True)

# Execute a trade
result = await executor.execute_trade(decision, "BTC/USDT")

# Get trade history
history = executor.get_trade_history()

# Get statistics
stats = executor.get_execution_stats()
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This system is provided for educational and research purposes. Trading cryptocurrencies and financial instruments involves significant risk. Past performance does not guarantee future results. 

**Before using this system for live trading:**
- Start with paper trading to understand how it works
- Use small position sizes
- Monitor the system regularly
- Never invest money you cannot afford to lose
- Consult with financial advisors if needed

## 🚀 Roadmap

- [ ] Multi-timeframe analysis support
- [ ] Advanced portfolio optimization
- [ ] Machine learning model integration
- [ ] Real-time market microstructure analysis
- [ ] Advanced risk hedging strategies
- [ ] Web dashboard for monitoring
- [ ] Mobile app integration
- [ ] Multi-exchange support

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review test cases for usage examples

## 🙏 Acknowledgments

- Inspired by Jarvis (Iron Man's AI assistant)
- Architecture based on Claw-Code multi-agent framework
- Financial analysis powered by community tools and libraries

---

**Made with ❤️ by the Babo Claude Team**

*"Intelligence is not just about being smart. It's about being wise enough to know when to act and when to wait."* - Babo Claude
