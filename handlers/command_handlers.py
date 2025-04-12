from telegram import Update
from telegram.ext import CallbackContext
from utils.show_main_menu import show_main_menu

async def start(update: Update, context: CallbackContext):
    """Handle /start command with main menu"""
    await show_main_menu(update, context)

async def handle_text_menu(update: Update, context: CallbackContext):
    """Handle text messages that match menu options"""
    text = update.message.text
    
    if text == "📚 FAQ":
        # Simulate FAQ callback
        from handlers.callback_handlers import button_handler
        # Create a mockup callback query
        class MockQuery:
            def __init__(self, data, message, from_user):
                self.data = data
                self.message = message
                self.from_user = from_user
            async def answer(self):
                pass
                
        mock_query = MockQuery('faq', update.message, update.message.from_user)
        await button_handler(update._replace(callback_query=mock_query), context)
        
    elif text == "🗺️ Мапа доступності":
        # Simulate map callback
        from handlers.callback_handlers import button_handler
        class MockQuery:
            def __init__(self, data, message, from_user):
                self.data = data
                self.message = message
                self.from_user = from_user
            async def answer(self):
                pass
                
        mock_query = MockQuery('map', update.message, update.message.from_user)
        await button_handler(update._replace(callback_query=mock_query), context)
        
    elif text == "➕ Додати об'єкт":
        # Simulate add_object callback
        from handlers.callback_handlers import button_handler
        class MockQuery:
            def __init__(self, data, message, from_user):
                self.data = data
                self.message = message
                self.from_user = from_user
            async def answer(self):
                pass
                
        mock_query = MockQuery('add_object', update.message, update.message.from_user)
        await button_handler(update._replace(callback_query=mock_query), context)

async def handle_text_menu(update: Update, context: CallbackContext):
    """Handle text messages that match menu options"""
    text = update.message.text
    message = update.message
    user = update.message.from_user
    
    if text == "📚 FAQ":
        # Call button handler directly with appropriate data
        from handlers.callback_handlers import button_handler
        
        # Create a simple mock query with needed attributes
        class MockQuery:
            def __init__(self):
                self.data = 'faq'
                self.message = message
                self.from_user = user
                
            async def answer(self):
                pass
        
        # Create a new update with our mock query
        mock_update = Update(update.update_id, callback_query=MockQuery())
        await button_handler(mock_update, context)
        
    elif text == "🗺️ Мапа доступності":
        from handlers.callback_handlers import button_handler
        
        class MockQuery:
            def __init__(self):
                self.data = 'map'
                self.message = message
                self.from_user = user
                
            async def answer(self):
                pass
                
        mock_update = Update(update.update_id, callback_query=MockQuery())
        await button_handler(mock_update, context)
        
    elif text == "➕ Додати об'єкт":
        from handlers.callback_handlers import button_handler
        
        class MockQuery:
            def __init__(self):
                self.data = 'add_object'
                self.message = message
                self.from_user = user
                
            async def answer(self):
                pass
                
        mock_update = Update(update.update_id, callback_query=MockQuery())
        await button_handler(mock_update, context)