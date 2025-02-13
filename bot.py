import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from database import Database
from handlers import BotHandlers
from utils import setup_logging

async def main() -> None:
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Initialize database
    db = Database("crypto_mining_bot.db")

    # Initialize bot handlers
    handlers = BotHandlers(db)

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CallbackQueryHandler(handlers.mine, pattern="^mine$"))
    application.add_handler(CallbackQueryHandler(handlers.balance, pattern="^balance$"))
    application.add_handler(CallbackQueryHandler(handlers.settings, pattern="^settings$"))
    application.add_handler(CallbackQueryHandler(handlers.tasks, pattern="^tasks$"))
    application.add_handler(CallbackQueryHandler(handlers.referral, pattern="^referral$"))

    # Start bot
    logger.info("Bot started")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())