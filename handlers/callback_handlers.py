from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils.helpers import sanitize_callback_data, get_original_category, get_original_object
from data.categories import categories, options
from config import user_selections, STATE_WAITING_FOR_LOCATION, STATE_SELECTING_OPTIONS, STATE_WAITING_FOR_PHOTO

async def button_handler(update: Update, context: CallbackContext) -> None:
    """Handle callback button presses"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Main menu options
    if query.data == 'faq':
        await query.message.reply_text(
            "📚 Часті питання\n\n"
            "1. Що таке доступність?\n"
            "   Доступність - це можливість безперешкодного використання об'єктів людьми з інвалідністю\n\n"
            "2. Як я можу допомогти?\n"
            "   Ви можете додавати інформацію про доступність об'єктів у вашому місті\n\n"
            "3. Де я можу побачити карту доступності?\n"
            "   Вибравши опцію 'Мапа доступності' в головному меню"
        )
        
    elif query.data == 'map':
        await query.message.reply_text(
            "🗺️ Мапа доступності\n\n"
            "Переглянути інтерактивну карту доступності можна за посиланням: https://example.com/map\n\n"
            "На карті відображені всі об'єкти, які були додані користувачами з відміткою про їх доступність",
            disable_web_page_preview=True
        )
        
    elif query.data == 'add_object':
        keyboard = []
        for category in categories:
            keyboard.append([
                InlineKeyboardButton(
                    category, 
                    callback_data=f'category|{sanitize_callback_data(category)}'
                )
            ])
        
        await query.message.reply_text(
            "🏢 Додавання об'єкта\n\n"
            "Оберіть категорію об'єкта, який ви хочете додати:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Category selection
    elif query.data.startswith('category|'):
        parts = query.data.split('|')
        if len(parts) == 2:
            sanitized_category = parts[1]
            category = get_original_category(sanitized_category, categories)
            
            if category:
                keyboard = []
                for obj_code, obj_name in categories[category]["objects"].items():
                    keyboard.append([
                        InlineKeyboardButton(
                            f"{obj_code}: {obj_name}", 
                            callback_data=f'object|{sanitize_callback_data(category)}|{sanitize_callback_data(obj_code)}'
                        )
                    ])
                
                await query.message.reply_text(
                    f"📋 {category}\n\n"
                    f"{categories[category]['description']}\n\n"
                    "Оберіть об'єкт у цій категорії:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await query.message.reply_text("❌ Помилка: Невідома категорія.")
        else:
            await query.message.reply_text("❌ Помилка при обробці вибору категорії.")

    # Object selection
    elif query.data.startswith('object|'):
        parts = query.data.split('|')
        if len(parts) == 3:
            sanitized_category = parts[1]
            sanitized_object = parts[2]
            
            category = get_original_category(sanitized_category, categories)
            if category:
                object_code = get_original_object(category, sanitized_object, categories)
                
                if object_code:
                    object_name = categories[category]["objects"][object_code]
                    
                    user_selections[user_id] = {
                        'state': STATE_WAITING_FOR_LOCATION,
                        'category': category,
                        'object_code': object_code,
                        'object_name': object_name,
                        'location': None,
                        'options': [],
                        'photo': None,
                        'options_message_id': None
                    }
                    
                    await query.message.reply_text(
                        f"✅ Об'єкт обрано успішно\n\n"
                        f"Категорія: {category}\n"
                        f"Об'єкт: {object_code} - {object_name}\n\n"
                        "Тепер нам потрібно дізнатися розташування цього об'єкта."
                    )
                    
                    # Allow custom location input
                    keyboard = [
                        [InlineKeyboardButton("📍 Моя поточна локація", callback_data='current_location')],
                        [InlineKeyboardButton("📌 Вказати іншу локацію", callback_data='custom_location')]
                    ]
                    await query.message.reply_text(
                        "Виберіть, як ви хочете вказати розташування об'єкта:",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                else:
                    await query.message.reply_text("❌ Помилка: Невідомий об'єкт.")
            else:
                await query.message.reply_text("❌ Помилка: Невідома категорія.")
        else:
            await query.message.reply_text("❌ Помилка при обробці вибору об'єкта.")

    # Location selection methods
    elif query.data == 'current_location':
        if user_id in user_selections and user_selections[user_id]['state'] == STATE_WAITING_FOR_LOCATION:
            keyboard = [
                [KeyboardButton("📍 Надіслати свою геолокацію", request_location=True)]
            ]
            await query.message.reply_text(
                "📌 Надсилання геолокації\n\n"
                "Натисніть на кнопку нижче, щоб надіслати своє поточне місцезнаходження.\n"
                "Переконайтеся, що ви знаходитеся біля об'єкта, який хочете додати.",
                reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            )
        else:
            await query.message.reply_text("❌ Будь ласка, спочатку виберіть об'єкт.")
            
    elif query.data == 'custom_location':
        if user_id in user_selections and user_selections[user_id]['state'] == STATE_WAITING_FOR_LOCATION:
            await query.message.reply_text(
                "📌 Вказання локації\n\n"
                "Будь ласка, поділіться геолокацією або введіть координати об'єкта у форматі:\n"
                "latitude, longitude\n\n"
                "Наприклад: 50.4501, 30.5234\n\n"
                "Або знайдіть об'єкт на Google Maps і надішліть координати."
            )
            # Set state to handle text input of coordinates
            user_selections[user_id]['state'] = STATE_WAITING_FOR_LOCATION
            # Store a flag to indicate waiting for text coordinates
            user_selections[user_id]['waiting_for_text_location'] = True
        else:
            await query.message.reply_text("❌ Будь ласка, спочатку виберіть об'єкт.")

    # Option selection
    elif query.data.startswith('option_'):
        if user_id in user_selections and user_selections[user_id]['state'] == STATE_SELECTING_OPTIONS:
            option = query.data[len('option_'):]
            
            # Toggle option selection
            if option in user_selections[user_id]['options']:
                user_selections[user_id]['options'].remove(option)
            else:
                user_selections[user_id]['options'].append(option)
            
            # Build keyboard with all options, highlighting selected ones
            options_list = list(options.keys())
            keyboard = []
            for i in range(0, len(options_list), 5):
                row = []
                for option_code in options_list[i:i+5]:
                    option_text = option_code
                    if option_code in user_selections[user_id]['options']:
                        option_text = f"✅ {option_code}"
                    row.append(InlineKeyboardButton(
                        option_text, 
                        callback_data=f'option_{option_code}'
                    ))
                keyboard.append(row)
            
            keyboard.append([InlineKeyboardButton("✅ Завершити вибір", callback_data='finish_selection')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Create options info text
            if user_selections[user_id]['options']:
                selected_options_text = "\n".join([
                    f"✅ {opt}: {options[opt]}" 
                    for opt in user_selections[user_id]['options']
                ])
                options_message = f"🔍 Вибрані опції доступності:\n\n{selected_options_text}"
            else:
                options_message = "🔍 Поки що не вибрано жодної опції доступності"
            
            # Edit the existing message if we have its ID, otherwise send a new one
            if user_selections[user_id].get('options_message_id'):
                try:
                    await context.bot.edit_message_text(
                        chat_id=query.message.chat_id,
                        message_id=user_selections[user_id]['options_message_id'],
                        text=f"{options_message}\n\nВиберіть опції або натисніть 'Завершити вибір':",
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    # If editing fails, send a new message
                    message = await query.message.reply_text(
                        f"{options_message}\n\nВиберіть опції або натисніть 'Завершити вибір':",
                        reply_markup=reply_markup
                    )
                    user_selections[user_id]['options_message_id'] = message.message_id
            else:
                # Send a new message and save its ID
                message = await query.message.reply_text(
                    f"{options_message}\n\nВиберіть опції або натисніть 'Завершити вибір':",
                    reply_markup=reply_markup
                )
                user_selections[user_id]['options_message_id'] = message.message_id
        else:
            await query.message.reply_text("❌ Будь ласка, спочатку виберіть об'єкт і локацію.")

    # Finish option selection
    elif query.data == 'finish_selection':
        if user_id in user_selections and user_selections[user_id]['state'] == STATE_SELECTING_OPTIONS:
            user_selections[user_id]['state'] = STATE_WAITING_FOR_PHOTO
            
            if user_selections[user_id]['options']:
                selected_options_text = "\n".join([
                    f"✅ {opt}: {options[opt]}" 
                    for opt in user_selections[user_id]['options']
                ])
            else:
                selected_options_text = "Жодної опції не вибрано"
            
            await query.message.reply_text(
                f"✅ Вибір опцій завершено\n\n"
                f"Вибрані опції:\n{selected_options_text}\n\n"
                "Тепер, будь ласка, надішліть фото об'єкта."
            )
        else:
            await query.message.reply_text("❌ Будь ласка, спочатку виберіть об'єкт і локацію.")