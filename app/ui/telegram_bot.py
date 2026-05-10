import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.config import settings

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class BaboTelegramBot:
    def __init__(self, orchestrator, consensus_engine):
        self.orchestrator = orchestrator
        self.consensus_engine = consensus_engine
        self.token = settings.TELEGRAM_BOT_TOKEN

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Welcome to Babo Claude! I am your AI Financial Swarm Assistant. Use /analyze <symbol> to start."
        )

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a symbol, e.g., /analyze BTC/USDT")
            return

        symbol = context.args[0].upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Swarm is analyzing {symbol}... Please wait.")

        # Run Swarm Analysis
        results = await self.orchestrator.analyze(symbol)
        decision = self.consensus_engine.evaluate(results)

        # Format response
        response = f"--- Analysis for {symbol} ---\n"
        for res in results:
            response += f"🤖 {res['agent']}: {res['action']} (Conf: {res['confidence']:.2f})\n"
        
        response += f"\n--- Final Decision ---\n"
        response += f"Consensus Score: {decision['score']:.4f}\n"
        response += f"Status: {'✅ APPROVED' if decision['approved'] else '❌ REJECTED'}"

        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def run(self):
        application = ApplicationBuilder().token(self.token).build()
        
        start_handler = CommandHandler('start', self.start)
        analyze_handler = CommandHandler('analyze', self.analyze_command)
        
        application.add_handler(start_handler)
        application.add_handler(analyze_handler)
        
        print("Telegram Bot is starting...")
        application.run_polling()
