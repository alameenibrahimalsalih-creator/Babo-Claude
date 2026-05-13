import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from app.config import settings
from app.core.orchestrator import SovereignOrchestrator
from app.core.consensus import ConsensusEngine
from app.execution.executor import TradeExecutor

# Jarvis-style Personality
JARVIS_PROMPT = """
🤖 **Babo Claude - Sovereign Financial Assistant**
Powered by Jarvis-inspired AI and Swarm Intelligence

I am your autonomous trading companion, equipped with:
✨ Multi-agent consensus system
📊 Real-time technical analysis
🔐 Advanced risk management
🚀 Self-evolving intelligence

Status: ONLINE & READY
"""

class BaboJarvisBot:
    def __init__(self, orchestrator: SovereignOrchestrator, 
                 consensus_engine: ConsensusEngine,
                 executor: TradeExecutor = None):
        self.orchestrator = orchestrator
        self.consensus_engine = consensus_engine
        self.executor = executor or TradeExecutor(paper_trading=True)
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.logger = logging.getLogger("BaboClaude.TelegramBot")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user.first_name
        keyboard = [
            [InlineKeyboardButton("📊 Analyze Symbol", callback_data='analyze')],
            [InlineKeyboardButton("🤖 Swarm Status", callback_data='status')],
            [InlineKeyboardButton("📈 Trade History", callback_data='history')],
            [InlineKeyboardButton("ℹ️ About Me", callback_data='about')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Welcome back, {user}!\n\n{JARVIS_PROMPT}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        text = update.message.text.lower()
        
        if "who are you" in text or "عرف نفسك" in text:
            await update.message.reply_text(JARVIS_PROMPT, parse_mode='Markdown')
        elif "analyze" in text or "حلل" in text:
            # Extract symbol from message if provided
            parts = update.message.text.split()
            symbol = parts[-1].upper() if len(parts) > 1 else "BTC/USDT"
            await self.run_analysis(update, symbol)
        elif "status" in text or "حالة" in text:
            await self.show_swarm_status(update)
        elif "history" in text or "السجل" in text:
            await self.show_trade_history(update)
        else:
            await update.message.reply_text(
                "I didn't understand that command.\n\n"
                "Try:\n"
                "• /analyze BTC/USDT\n"
                "• /status\n"
                "• /history\n"
                "• /help"
            )

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command."""
        symbol = context.args[0].upper() if context.args else "BTC/USDT"
        await self.run_analysis(update, symbol)

    async def run_analysis(self, update: Update, symbol: str):
        """Execute swarm analysis and consensus."""
        try:
            await update.message.reply_text(
                f"🔄 Initiating sovereign swarm analysis for **{symbol}**...\n"
                f"📊 Swarm size: {len(self.orchestrator.agents)} agents",
                parse_mode='Markdown'
            )
            
            # Run swarm analysis
            results = await self.orchestrator.run_swarm_analysis(symbol)
            
            # Get consensus decision
            decision = self.consensus_engine.evaluate(results)
            
            # Build response
            response = f"**--- Sovereign Swarm Report: {symbol} ---**\n\n"
            response += "**Agent Votes:**\n"
            
            for res in results:
                emoji = "🟢" if res.get('action') == 'BUY' else "🔴" if res.get('action') == 'SELL' else "⚪"
                response += (
                    f"{emoji} **{res.get('agent')}**: {res.get('action')} "
                    f"(Confidence: {res.get('confidence', 0):.1%})\n"
                    f"   └─ {res.get('reason', 'N/A')}\n"
                )
            
            response += f"\n**--- Consensus Protocol ---**\n"
            response += f"📊 Final Score: {decision.get('score', 0):.2%}\n"
            response += f"🎯 Action: **{decision.get('action', 'HOLD')}**\n"
            response += f"⚠️ Risk Level: {decision.get('risk_level', 'UNKNOWN')}\n"
            response += f"✅ Approved: {'YES' if decision.get('approved') else 'NO'}\n"
            response += f"\n📝 Reasoning:\n{decision.get('reason', 'N/A')}\n"
            
            # Execute trade if approved
            if decision.get('approved') and decision.get('action') in ['BUY', 'SELL']:
                execution_result = await self.executor.execute_trade(decision, symbol)
                response += f"\n**--- Trade Execution ---**\n"
                if execution_result.get('executed'):
                    response += f"✅ Trade Executed!\n"
                    response += f"Type: {execution_result.get('type', 'N/A').upper()}\n"
                    response += f"Action: {execution_result.get('action')}\n"
                    response += f"Size: {execution_result.get('size')}\n"
                else:
                    response += f"❌ Trade Execution Failed\n"
                    response += f"Reason: {execution_result.get('error', 'Unknown')}\n"
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {e}")
            await update.message.reply_text(
                f"❌ Error during analysis: {str(e)}",
                parse_mode='Markdown'
            )

    async def show_swarm_status(self, update: Update):
        """Show current swarm status."""
        try:
            status = self.orchestrator.get_swarm_status()
            
            response = "**--- Swarm Status ---**\n\n"
            response += f"🤖 Total Agents: {status.get('total_agents', 0)}\n"
            response += f"⏰ Timestamp: {status.get('timestamp', 'N/A')}\n\n"
            
            response += "**Agent Details:**\n"
            for agent_info in status.get('agents', []):
                perf = agent_info.get('performance', {})
                accuracy = perf.get('accuracy', 0)
                response += (
                    f"• {agent_info.get('name')}\n"
                    f"  └─ Weight: {agent_info.get('weight', 0):.2f} | "
                    f"Accuracy: {accuracy:.1%}\n"
                )
            
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            self.logger.error(f"Error showing swarm status: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def show_trade_history(self, update: Update):
        """Show recent trade history."""
        try:
            history = self.executor.get_trade_history(limit=5)
            stats = self.executor.get_execution_stats()
            
            response = "**--- Trade History & Statistics ---**\n\n"
            response += f"📊 Total Trades: {stats.get('total_trades', 0)}\n"
            response += f"🟢 Buy Trades: {stats.get('buy_trades', 0)}\n"
            response += f"🔴 Sell Trades: {stats.get('sell_trades', 0)}\n"
            response += f"📈 Avg Confidence: {stats.get('average_confidence', 0):.1%}\n"
            response += f"⚠️ Avg Risk: {stats.get('average_risk', 0):.1%}\n"
            response += f"🔧 Mode: {stats.get('mode', 'UNKNOWN')}\n\n"
            
            if history:
                response += "**Recent Trades:**\n"
                for trade in history:
                    emoji = "🟢" if trade.get('action') == 'BUY' else "🔴"
                    response += (
                        f"{emoji} {trade.get('action')} {trade.get('size')} "
                        f"{trade.get('symbol')} @ {trade.get('timestamp', 'N/A')}\n"
                    )
            else:
                response += "No trades yet."
            
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            self.logger.error(f"Error showing trade history: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'analyze':
            await query.edit_message_text(
                "Please send a symbol to analyze (e.g., BTC/USDT):"
            )
        elif query.data == 'status':
            await self.show_swarm_status(query)
        elif query.data == 'history':
            await self.show_trade_history(query)
        elif query.data == 'about':
            await query.edit_message_text(JARVIS_PROMPT, parse_mode='Markdown')

    def run(self):
        """Start the Telegram bot."""
        application = ApplicationBuilder().token(self.token).build()
        
        # Add handlers
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('analyze', self.analyze_command))
        application.add_handler(CommandHandler('status', lambda u, c: self.show_swarm_status(u)))
        application.add_handler(CommandHandler('history', lambda u, c: self.show_trade_history(u)))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        self.logger.info("🚀 Babo Claude (Jarvis Mode) is online and ready for trading!")
        print("\n" + "="*60)
        print("🤖 BABO CLAUDE - SOVEREIGN TRADING SYSTEM")
        print("="*60)
        print("✅ Telegram Bot is ONLINE")
        print("📊 Swarm Intelligence: ACTIVE")
        print("🔐 Risk Management: ENABLED")
        print("="*60 + "\n")
        
        application.run_polling()
