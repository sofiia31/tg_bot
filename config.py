import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token obtained from BotFather via environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Optional fallback if environment variable isn't set (for development)
if not TOKEN:
    # Only use this during development, never commit actual tokens
    TOKEN = ''
    logging.warning("No bot token found in environment variables! Using empty token.")

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# States for managing selection process
STATE_WAITING_FOR_LOCATION = 1
STATE_SELECTING_OPTIONS = 2
STATE_WAITING_FOR_PHOTO = 3

# Dictionary to store current selection state for each user
user_selections = {}