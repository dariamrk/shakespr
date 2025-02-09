# src/bot/handlers/profile.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, 
    ConversationHandler, 
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from src.utils.logging import logger

# States
CHOOSING = 0
TYPING_NAME = 1
TYPING_CITY = 2
TYPING_COUNTRY = 3

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for profile management"""
    logger.info(f"Profile command received from user {update.effective_user.id}")
    
    keyboard = [
        [InlineKeyboardButton("Start Profile Setup", callback_data='setup')],
        [InlineKeyboardButton("Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to profile setup! Would you like to continue?",
        reply_markup=reply_markup
    )
    return CHOOSING

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button presses"""
    query = update.callback_query
    logger.info(f"Callback received: {query.data}")
    
    await query.answer()
    
    if query.data == 'cancel':
        await query.edit_message_text("Profile setup cancelled.")
        return ConversationHandler.END
    
    await query.edit_message_text("Please enter your name:")
    return TYPING_NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle name input"""
    name = update.message.text
    context.user_data['name'] = name
    logger.info(f"Name received: {name}")
    
    await update.message.reply_text(
        f"Nice to meet you, {name}! Now, please enter your current city:"
    )
    return TYPING_CITY

async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle city input"""
    city = update.message.text
    context.user_data['city'] = city
    logger.info(f"City received: {city}")
    
    await update.message.reply_text(
        f"Great! And what country is {city} in?"
    )
    return TYPING_COUNTRY

async def handle_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle country input and complete profile"""
    country = update.message.text
    context.user_data['country'] = country
    logger.info(f"Country received: {country}")
    
    # Here you would typically save to database
    await update.message.reply_text(
        f"Perfect! I've saved your profile:\n\n"
        f"Name: {context.user_data['name']}\n"
        f"City: {context.user_data['city']}\n"
        f"Country: {country}\n\n"
        f"You can now use /relocate to explore other cities!"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation"""
    await update.message.reply_text("Profile setup cancelled.")
    return ConversationHandler.END

def get_profile_handler():
    """Return the conversation handler"""
    logger.info("Creating profile conversation handler")
    
    return ConversationHandler(
        entry_points=[CommandHandler('profile', profile)],
        states={
            CHOOSING: [
                CallbackQueryHandler(button_callback)
            ],
            TYPING_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)
            ],
            TYPING_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city)
            ],
            TYPING_COUNTRY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_country)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="profile_conversation"
    )
