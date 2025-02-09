# src/bot/handlers/relocation.py
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
from src.data.numbeo.fetcher import fetch_city_data
from datetime import datetime

# Conversation states
CHOOSING_CITY = 0
TYPING_CITY = 1
TYPING_COUNTRY = 2

# Popular cities for quick selection
POPULAR_CITIES = [
    ("New York", "United States"),
    ("London", "United Kingdom"),
    ("Singapore", "Singapore"),
    ("Sydney", "Australia"),
    ("Berlin", "Germany")
]

def format_cost(value: float) -> str:
    """Format cost value with fallback for None"""
    if value is None:
        return "Data not available"
    return f"${value:,.2f}"

def format_city_comparison(city_data: dict) -> str:
    """Format city data for display with safe handling of None values"""
    try:
        costs = {
            'rent_1br_center': city_data.get('rent_1br_center'),
            'cheap_meal_for_one': city_data.get('cheap_meal_for_one'),
            'milk_one_liter': city_data.get('milk_one_liter'),
            'monthly_transit_pass': city_data.get('monthly_transit_pass'),
            'utilities_basic': city_data.get('utilities_basic')
        }
        
        # Check if we have at least some data
        if not any(v is not None for v in costs.values()):
            logger.error(f"No valid cost data found: {costs}")
            return (
                "⚠️ No cost data is currently available for this city.\n\n"
                "Would you like to try another city? Use /relocate again!"
            )

        return (
            f"📊 Cost of Living in {city_data.get('city_name', 'Unknown City')}, "
            f"{city_data.get('country', 'Unknown Country')}:\n\n"
            f"🏠 Housing:\n"
            f"- 1 Bedroom Apartment (City Center): {format_cost(costs['rent_1br_center'])}\n\n"
            f"🍽 Food & Dining:\n"
            f"- Meal (Inexpensive Restaurant): {format_cost(costs['cheap_meal_for_one'])}\n"
            f"- 1L Milk: {format_cost(costs['milk_one_liter'])}\n\n"
            f"🚇 Transportation:\n"
            f"- Monthly Transit Pass: {format_cost(costs['monthly_transit_pass'])}\n\n"
            f"💡 Utilities:\n"
            f"- Basic Utilities: {format_cost(costs['utilities_basic'])}\n\n"
            f"Last Updated: {city_data.get('last_updated', datetime.now()).strftime('%Y-%m-%d')}\n\n"
            f"Would you like to simulate another city? Use /relocate again!"
        )
    except Exception as e:
        logger.error(f"Error formatting city data: {e}")
        return (
            "⚠️ Some data is currently unavailable for this city.\n\n"
            "Would you like to try another city? Use /relocate again!"
        )

async def relocate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /relocate command"""
    logger.info(f"Relocate command received from user {update.effective_user.id}")
    
    keyboard = []
    for city, country in POPULAR_CITIES:
        keyboard.append([
            InlineKeyboardButton(
                f"{city}, {country}", 
                callback_data=f"relocate_{city}_{country}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔍 Other City", callback_data="other_city")])
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌎 Where would you like to relocate to?\n"
        "Choose from popular cities or select 'Other City' to enter a different location:",
        reply_markup=reply_markup
    )
    return CHOOSING_CITY

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button selections"""
    query = update.callback_query
    await query.answer()
    logger.info(f"Relocation callback received: {query.data}")

    if query.data == "cancel":
        await query.edit_message_text("Relocation simulation cancelled.")
        return ConversationHandler.END
        
    if query.data == "other_city":
        await query.edit_message_text(
            "Please enter the name of the city you'd like to move to:"
        )
        return TYPING_CITY
        
    # Handle popular city selection
    try:
        _, city, country = query.data.split('_')
        loading_message = await query.edit_message_text("🔄 Fetching city data...")
        
        city_data = await fetch_city_data(city, country)
        if city_data:
            comparison_text = format_city_comparison(city_data)
            await loading_message.edit_text(comparison_text)
        else:
            await loading_message.edit_text(
                f"Sorry, I couldn't find data for {city}, {country}.\n"
                "The data might be temporarily unavailable. "
                "Please try another city or check back later."
            )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error processing city selection: {e}")
        await query.edit_message_text(
            "Sorry, there was an error processing your selection.\n"
            "The service might be temporarily unavailable.\n"
            "Please try again later or choose another city."
        )
        return ConversationHandler.END

async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle custom city input"""
    city = update.message.text
    context.user_data['target_city'] = city
    
    await update.message.reply_text(
        f"Great! And what country is {city} in?\n"
        "Please enter the country name:"
    )
    return TYPING_COUNTRY

async def handle_country_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle country input and show comparison"""
    country = update.message.text
    city = context.user_data['target_city']
    
    loading_message = await update.message.reply_text("🔄 Fetching city data...")
    
    try:
        city_data = await fetch_city_data(city, country)
        if city_data:
            comparison_text = format_city_comparison(city_data)
            await loading_message.edit_text(comparison_text)
        else:
            await loading_message.edit_text(
                f"Sorry, I couldn't find data for {city}, {country}.\n"
                "The data might be temporarily unavailable. "
                "Please try another city or check back later."
            )
    except Exception as e:
        logger.error(f"Error showing city comparison: {e}")
        await loading_message.edit_text(
            "Sorry, there was an error fetching the data.\n"
            "Please try again later or choose another city."
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation"""
    await update.message.reply_text("Relocation simulation cancelled.")
    return ConversationHandler.END

def get_relocation_handler():
    """Create and return the relocation conversation handler"""
    return ConversationHandler(
        entry_points=[CommandHandler('relocate', relocate)],
        states={
            CHOOSING_CITY: [
                CallbackQueryHandler(button_callback)
            ],
            TYPING_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_input)
            ],
            TYPING_COUNTRY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_country_input)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="relocation_conversation"
    )
