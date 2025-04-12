from config import logger

def sanitize_callback_data(data: str) -> str:
    """Clean and format callback data to comply with Telegram API requirements"""
    sanitized_data = data.replace(" ", "_").replace("'", "").replace("-", "_").replace("/", "_").lower()
    if len(sanitized_data) > 64:
        sanitized_data = sanitized_data[:64]
    logger.info(f"Sanitized callback_data: {sanitized_data}")
    return sanitized_data

def get_original_category(sanitized_category, categories):
    """Find original category name from sanitized version"""
    for category in categories:
        if sanitize_callback_data(category) == sanitized_category:
            return category
    return None

def get_original_object(category, sanitized_object, categories):
    """Find original object from sanitized version"""
    for obj_code in categories[category]["objects"]:
        if sanitize_callback_data(obj_code) == sanitized_object:
            return obj_code
    return None