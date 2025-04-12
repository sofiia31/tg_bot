from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from config import user_selections, STATE_WAITING_FOR_LOCATION, STATE_SELECTING_OPTIONS, STATE_WAITING_FOR_PHOTO, logger
from utils.show_main_menu import show_main_menu
from data.storage import save_to_json
from data.categories import options
import re

async def location_handler(update: Update, context: CallbackContext):
    """Handle location messages"""
    user_id = update.message.from_user.id
    
    if user_id in user_selections and user_selections[user_id]['state'] == STATE_WAITING_FOR_LOCATION:
        location = update.message.location
        latitude = location.latitude
        longitude = location.longitude
        
        await process_location(update, context, user_id, latitude, longitude)
    else:
        await update.message.reply_text("❌ Будь ласка, спочатку виберіть об'єкт.")

async def text_handler(update: Update, context: CallbackContext):
    """Handle text messages that might contain coordinates"""
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    # Check if user is waiting for text location input
    if (user_id in user_selections and 
        user_selections[user_id]['state'] == STATE_WAITING_FOR_LOCATION and 
        user_selections[user_id].get('waiting_for_text_location')):
        
        # Parse coordinates from text using regex
        # Looking for patterns like "50.4501, 30.5234" or "50.4501,30.5234"
        coordinates_pattern = r'(\d+\.\d+)\s*,\s*(\d+\.\d+)'
        match = re.search(coordinates_pattern, message_text)
        
        if match:
            try:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                
                # Basic validation of coordinates
                if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                    # Remove the waiting flag
                    user_selections[user_id].pop('waiting_for_text_location', None)
                    
                    await process_location(update, context, user_id, latitude, longitude)
                else:
                    await update.message.reply_text(
                        "❌ Невірні координати. Широта повинна бути від -90 до 90, довгота від -180 до 180.\n"
                        "Спробуйте ще раз або поверніться в меню командою /start"
                    )
            except ValueError:
                await update.message.reply_text(
                    "❌ Не вдалося розпізнати координати. Будь ласка, введіть у форматі:\n"
                    "50.4501, 30.5234"
                )
        else:
            await update.message.reply_text(
                "❌ Не вдалося розпізнати координати. Будь ласка, введіть у форматі:\n"
                "50.4501, 30.5234"
            )

async def process_location(update, context, user_id, latitude, longitude):
    """Process location data (common for both location types)"""
    user_selections[user_id]['location'] = {'latitude': latitude, 'longitude': longitude}
    user_selections[user_id]['state'] = STATE_SELECTING_OPTIONS
    
    # Remove keyboard if present
    await update.message.reply_text(
        f"📍 Локація збережена успішно\n\n"
        f"Координати:\n"
        f"Широта: {latitude}\n"
        f"Довгота: {longitude}",
        reply_markup=ReplyKeyboardRemove()
    )

    # Create keyboard with options
    options_list = list(options.keys())
    keyboard = []
    for i in range(0, len(options_list), 5):
        row = []
        for option_code in options_list[i:i+5]:
            row.append(InlineKeyboardButton(
                option_code, 
                callback_data=f'option_{option_code}'
            ))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("✅ Завершити вибір", callback_data='finish_selection')])
    
    # Send options descriptions first
    options_description = "\n".join([f"{code}: {desc}" for code, desc in options.items()])
    await update.message.reply_text(
        f"🔍 Опції доступності\n\n"
        f"{options_description}"
    )
    
    # Send options selection message and save its ID
    message = await update.message.reply_text(
        "Виберіть всі підходящі опції:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    user_selections[user_id]['options_message_id'] = message.message_id

async def photo_handler(update: Update, context: CallbackContext):
    """Handle photo messages"""
    user_id = update.message.from_user.id
    
    if user_id in user_selections and user_selections[user_id]['state'] == STATE_WAITING_FOR_PHOTO:
        photo = update.message.photo[-1]  # Get the highest resolution photo
        file_id = photo.file_id
        user_selections[user_id]['photo'] = file_id

        # Save all application data to JSON
        selection = user_selections[user_id]
        saved = save_to_json(user_id, {
            'category': selection['category'],
            'object_code': selection['object_code'],
            'object_name': selection['object_name'],
            'location': selection['location'],
            'options': selection['options'],
            'photo': selection['photo'],
            'date': update.message.date.isoformat()
        })

        if saved:
            # Create summary text
            if selection['options']:
                selected_options_text = "\n".join([
                    f"✅ {opt}: {options[opt]}" 
                    for opt in selection['options']
                ])
            else:
                selected_options_text = "Жодної опції не вибрано"
                
            await update.message.reply_text(
                f"✅ Дякуємо! Ваша заявка збережена успішно\n\n"
                f"Дані про об'єкт:\n"
                f"Категорія: {selection['category']}\n"
                f"Об'єкт: {selection['object_code']} - {selection['object_name']}\n"
                f"Координати: {selection['location']['latitude']}, {selection['location']['longitude']}\n\n"
                f"Вибрані опції доступності:\n{selected_options_text}\n\n"
                "Ваш внесок допоможе зробити місто доступнішим! 🌟"
            )
            
            # Clear current selection
            del user_selections[user_id]
            
            # Show main menu with custom message
            custom_message = (
                "Ваша заявка успішно надіслана! 🎉 "
                "Ви можете додати ще один об'єкт або вибрати іншу опцію:"
            )
            await show_main_menu(update, context, custom_message=custom_message)
        else:
            await update.message.reply_text(
                "❌ Сталася помилка при збереженні даних. Будь ласка, спробуйте ще раз."
            )
    else:
        await update.message.reply_text("❌ Будь ласка, спочатку завершіть вибір опцій.")