from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

async def show_main_menu(update: Update, context: CallbackContext, custom_message: str = None):
    """Display the main menu with optional custom message"""
    # Inline keyboard for menu options
    inline_keyboard = [
        [InlineKeyboardButton("📚 FAQ", callback_data='faq')],
        [InlineKeyboardButton("🗺️ Мапа доступності", callback_data='map')],
        [InlineKeyboardButton("➕ Додати об'єкт", callback_data='add_object')]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    
    # Regular keyboard with the same options
    regular_keyboard = [
        ["📚 FAQ", "🗺️ Мапа доступності"],
        ["➕ Додати об'єкт"]
    ]
    regular_markup = ReplyKeyboardMarkup(regular_keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    # Default message if none provided
    default_message = (
        "Привіт! Я бот для допомоги зі збором інформації про доступність об'єктів. "
        "Виберіть одну з опцій:"
    )
    
    # Send message with inline buttons
    await update.message.reply_text(
        custom_message or default_message,
        reply_markup=inline_markup
    )
    
    # Send message with persistent keyboard
    await update.message.reply_text(
        "Використовуйте кнопки нижче для швидкого доступу:",
        reply_markup=regular_markup
    )