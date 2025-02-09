# src/main.py
import os
from pathlib import Path
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from src.utils.logging import setup_logging, logger
from src.bot.handlers.profile import get_profile_handler
from src.bot.handlers.relocation import get_relocation_handler

# Load environment variables
env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

# Setup logging
logger = setup_logging()

async def start(update, context):
    """Handle the /start command"""
    logger.info(f"Start command received from user {update.effective_user.id}")
    await update.message.reply_text(
        "👋 Welcome to Shakespr - Your AI-Empowered Life Path Simulator!\n\n"
        "I can help you simulate life decisions like:\n"
        "🌎 Relocating to a new city\n"
        "💼 Switching careers\n\n"
        "To get started, use /profile to set up your profile."
    )

async def help(update, context):
    """Handle the /help command"""
    logger.info(f"Help command received from user {update.effective_user.id}")
    await update.message.reply_text(
        "🤖 Shakespr Bot Commands:\n\n"
        "/start - Start the bot\n"
        "/profile - Set up or update your profile\n"
        "/relocate - Simulate relocating to a new city\n"
        "/career - Explore career transitions\n"
        "/help - Show this help message"
    )

def main():
    """Start the bot"""
    # Get bot token from environment variables
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No bot token provided!")
        return

    try:
        # Create application
        application = ApplicationBuilder().token(token).build()

        # Add handlers
        logger.info("Registering command handlers")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help))
        
        # Add profile handler
        logger.info("Registering profile conversation handler")
        application.add_handler(get_profile_handler())
        
        # Add relocation handler
        logger.info("Registering relocation conversation handler")
        application.add_handler(get_relocation_handler())

        # Start the bot
        logger.info("Starting bot...")
        application.run_polling(allowed_updates=["message", "callback_query"])

    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)

if __name__ == '__main__':
    main()
