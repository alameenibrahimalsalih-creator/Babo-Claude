import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from app.config import settings
from app.core.orchestrator import SovereignOrchestrator
from app.core.consensus import ConsensusEngine

# Jarvis-style Personality
JARVIS_PROMPT = """
I am Babo Claude, your Sovereign Financial Assistant, inspired by Jarvis and powered by the Swarm Intelligence of Claw-Code and Awesome-Finance-Skills.
I monitor global markets, analyze sentiment, and execute trades only when my swarm reaches a sovereign consensus.
"""

class BaboJarvisBot:
    def __init__(self, orchestrator: SovereignOrchestrator, consensus_engine: ConsensusEngine):
        self.orchestrator = orchestrator
        self.consensus_engine = consensus_engine
        self.token = settings.TELEGRAM_BOT_TOKEN

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user.first_name
        await update.message.reply_text(f"Welcome back, {user}. {JARVIS_PROMPT}\n\nHow can I assist you today?")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.lower()
        
        if "who are you" in text or "عرف نفسك" in text:
            await update.message.reply_text(JARVIS_PROMPT)
        elif "analyze" in text or "حلل" in text:
            symbol = "BTC/USDT" # Default or extract from text
            await self.run_analysis(update, symbol)
        else:
            # General AI response placeholder
            await update.message.reply_text("I am processing your request. For financial analysis, please use /analyze <symbol>.")

    async def run_analysis(self, update: Update, symbol: str):
        await update.message.reply_text(f"Initiating sovereign swarm analysis for {symbol}...")
        results = await self.orchestrator.run_swarm_analysis(symbol)
        decision = self.consensus_engine.evaluate(results)

        response = f"--- Sovereign Swarm Report: {symbol} ---\n"
        for res in results:
            response += f"🔹 {res['agent']}: {res['action']} (Confidence: {res['confidence']:.2f})\n"
            response += f"   Reason: {res['reason']}\n"
        
        response += f"\n--- Consensus Protocol ---\n"
        response += f"Score: {decision['score']:.4f}\n"
        response += f"Status: {'✅ SOVEREIGN APPROVED' if decision['approved'] else '❌ REJECTED'}\n"
        
        if decision['approved']:
            response += "\nAction: Executing trade sequence as per protocol."
        else:
            response += "\nAction: Standing by for better market conditions."

        await update.message.reply_text(response)

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        symbol = context.args[0].upper() if context.args else "BTC/USDT"
        await self.run_analysis(update, symbol)

    def run(self):
        application = ApplicationBuilder().token(self.token).build()
        
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('analyze', self.analyze_command))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        
        print("Babo Claude (Jarvis Mode) is online...")
        application.run_polling()
