from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from handlers.command_handlers import start, handle_text_menu
from handlers.callback_handlers import button_handler
from handlers.message_handlers import location_handler, photo_handler, text_handler

def main():
    """Main function to start the bot"""
    # Initialize the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    
    # Add handlers for text menu and coordinates input
    menu_filter = filters.TEXT & (
        filters.Regex(r'^📚 FAQ$') | 
        filters.Regex(r'^🗺️ Мапа доступності$') | 
        filters.Regex(r'^➕ Додати об\'єкт$')
    )
    application.add_handler(MessageHandler(menu_filter, handle_text_menu))
    
    # This should be the last handler to catch all other text messages
    application.add_handler(MessageHandler(filters.TEXT & ~menu_filter, text_handler))

    # Start the bot
    print("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()