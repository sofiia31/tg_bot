from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler
from telegram.ext import filters
import logging
import json

# Ваш токен, отриманий від BotFather
TOKEN = '7777940519:AAGxguct9mmQvi1jOmSTe1GQCAxegZFeEVI'

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для очищення callback_data
def sanitize_callback_data(data: str) -> str:
    sanitized_data = data.replace(" ", "_").replace("'", "").replace("-", "_").replace("/", "_").lower()
    if len(sanitized_data) > 64:
        sanitized_data = sanitized_data[:64]
    logger.info(f"Sanitized callback_data: {sanitized_data}")
    return sanitized_data

# Категорії та об'єкти
categories = {
    "Державні будівлі": [
        ("11"),
        ("12"),
        ("13")
    ],
    "2": [
        ("21"),
        ("22"),
        ("23"),
        ("24")
    ],
    "3": [
        ("31"),
        ("32"),
        ("33"),
        ("34")
    ],
    "4": [
        ("41"),
        ("42"),
        ("43")
    ]
}

# Функція для збереження вибраних даних у JSON
def save_to_json(data, filename='selected_objects.json'):
    try:
  
        with open(filename, 'r+') as file:
            try:
                current_data = json.load(file)  
            except json.JSONDecodeError:
                current_data = []  
            current_data.append(data)  
            file.seek(0)  
            json.dump(current_data, file, indent=4)  
    except FileNotFoundError:
        # Якщо файл не існує, створюємо новий з одним елементом
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)

# Основне меню
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("FAQ", callback_data='faq')],
        [InlineKeyboardButton("Мапа доступності", callback_data='map')],
        [InlineKeyboardButton("Додати об\'єкт", callback_data='add_object')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привіт! Виберіть одну з опцій:', reply_markup=reply_markup)

# Функція для обробки натискання на кнопки
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    logger.info(f"Callback data: {query.data}")  # Логування callback_data

    if query.data == 'faq':
        await query.edit_message_text(text='FAQ ще не налаштовано. Залиште запит, і ми відповімо як тільки зможемо!')
    elif query.data == 'map':
        await query.edit_message_text(text='Мапа доступності ще не налаштована. Скоро вона буде доступна!')
    elif query.data == 'add_object':
        keyboard = [
            [InlineKeyboardButton(category.replace("_", " ").title(), callback_data=f'category_{sanitize_callback_data(category)}')
             for category in categories]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('Оберіть категорію для додавання об\'єкта:', reply_markup=reply_markup)

    elif query.data.startswith('category_'):
        category = query.data[len('category_'):]

        logger.info(f"Selected category: {category}")

        if category in categories:
            objects = categories[category]
            
            object_buttons = [
                InlineKeyboardButton(f"{obj[0]} ({obj[1]} об'єктів)", callback_data=f'object_{category}_{sanitize_callback_data(obj[0])}')
                for obj in objects
            ]
            keyboard = [object_buttons]

            logger.info(f"Generated object buttons: {keyboard}")

            await query.edit_message_text(
                text=f"Оберіть об\'єкт у категорії {category.replace('_', ' ').title()}:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            logger.error(f"Category not found: {category}")
            await query.edit_message_text(text="Помилка: Невідома категорія.")

    elif query.data.startswith('object_'):
        data_parts = query.data.split('_')
        if len(data_parts) == 3:
            _, category, object_name = data_parts
            object_name = object_name.replace("_", " ")
            category = category.replace("_", " ")

            # Зберігаємо вибір об'єкта
            selected_data = {
                'category': category,
                'object': object_name
            }

            # Отримуємо поточний вибір
            try:
                with open('selected_objects.json', 'r') as file:
                    current_data = json.load(file)
            except FileNotFoundError:
                current_data = []

            # Додаємо новий вибір до поточних виборів
            current_data.append(selected_data)

            # Зберігаємо оновлені дані в JSON
            with open('selected_objects.json', 'w') as file:
                json.dump(current_data, file, indent=4)

            await query.edit_message_text(
                text=f"Ви вибрали об'єкт: {object_name} з категорії {category}. Додано успішно!"
            )

            # Тепер запитуємо, чи хоче користувач вказати геолокацію
            keyboard = [
                [InlineKeyboardButton("Вибрати місце на карті", callback_data='choose_location')]
            ]
            await query.edit_message_text(
                text="Тепер оберіть місце розташування для цього об'єкта.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            logger.error(f"Invalid callback data: {query.data}")
            await query.edit_message_text(text="Помилка при обробці вибору об'єкта. Спробуйте ще раз.")

    elif query.data == 'choose_location':
        # Відправляємо кнопку для вибору геолокації
        keyboard = [
            [KeyboardButton("Надіслати свою геолокацію", request_location=True)]
        ]
        await query.message.reply_text(
            text="Виберіть місце на карті, щоб додати геолокацію для цього об'єкта.",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

    elif query.data == 'finish_selection':
        # Завершити вибір
        await query.edit_message_text(text="Вибір завершено. Ваші опції збережені!")

# Функція для продовження вибору після збереження геолокації
async def location_handler(update: Update, context: CallbackContext):
    # Отримуємо геолокацію
    location = update.message.location
    latitude = location.latitude
    longitude = location.longitude

    # Збереження локації в JSON
    save_to_json({
        'latitude': latitude,
        'longitude': longitude
    })

    # Підтвердження користувачу
    await update.message.reply_text(
        f"Ваша локація збережена:\nШирота: {latitude}\nДовгота: {longitude}\n\n"
        "Тепер виберіть, що з доступних опцій вам підходить. Ви можете вибрати кілька:"
    )

    # Кнопки для вибору доступних опцій
    options = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25"
    ]
    # Формуємо кнопки для вибору
    keyboard = [
        [InlineKeyboardButton(option, callback_data=f'option_{sanitize_callback_data(option)}') for option in options[i:i+2]]
        for i in range(0, len(options), 2)
    ]

    # Додаємо кнопку "Завершити вибір"
    keyboard.append([InlineKeyboardButton("Завершити вибір", callback_data='finish_selection')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Запит на вибір опцій
    await update.message.reply_text(
        text="Виберіть опції доступності, які вам підходять:",
        reply_markup=reply_markup
    )

async def option_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Логування вибору
    logger.info(f"Selected option: {query.data}")

    option = query.data[len('option_'):]  # Отримуємо назву вибраної опції
    option = option.replace("_", " ")

    # Отримуємо user_id користувача
    user_id = update.effective_user.id

    # Формуємо дані для збереження
    selected_data = {
        'option': option
    }

    # Отримуємо поточні вибори користувача
    try:
        with open('selected_objects.json', 'r') as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = {}

    # Якщо користувача ще немає, створюємо запис
    if user_id not in current_data:
        current_data[user_id] = {"objects": [], "options": []}

    # Додаємо вибрану опцію до списку опцій користувача
    current_data[user_id]["options"].append(option)

    # Зберігаємо оновлені дані в JSON
    with open('selected_objects.json', 'w') as file:
        json.dump(current_data, file, indent=4)

    # Підтвердження вибору
    await query.edit_message_text(
        text=f"Ви вибрали опцію: {option}. Додано успішно!"
    )
    

# Функція для обробки завершення вибору
# Функція для обробки завершення вибору
async def finish_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Завершення вибору
    await query.edit_message_text(text="✅ Вибір завершено. Ваші опції збережені!")

    # Надсилання окремим повідомленням запиту на фото
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📸 Будь ласка, зробіть фото об'єкта та надішліть його сюди!"
    )
async def photo_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo = update.message.photo[-1]  # Беремо найкращу якість

    file_id = photo.file_id
    file_unique_id = photo.file_unique_id

    logger.info(f"Отримано фото від {user.first_name}, file_id: {file_id}")

    await update.message.reply_text("Дякуємо! Фото отримано та збережено ✅")

    # (Опціонально) Збереження file_id або завантаження фото:
    # file = await context.bot.get_file(file_id)
    # await file.download_to_drive(f"photos/{file_unique_id}.jpg")
    

# Основна функція для запуску бота
def main():
    # Створюємо Application і передаємо токен
    application = Application.builder().token(TOKEN).build()

    # Додаємо обробники для команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))  # Обробка геолокації
    application.add_handler(CallbackQueryHandler(option_handler, pattern='^option_'))  # Обробка вибору опцій
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))  # Обробка фото
    application.add_handler(CallbackQueryHandler(finish_selection, pattern='^finish_selection$'))  # Завершення вибору
    # Запускаємо бота
    application.run_polling()

if __name__ == '__main__':
    main()
