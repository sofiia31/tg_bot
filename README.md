# Accessibility Mapping Telegram Bot

A Telegram bot designed to collect and share information about building accessibility features. The bot allows users to add new locations, specify their accessibility features, and view a map of accessible buildings.

## Features

- 📚 FAQ section with information about accessibility
- 🗺️ Interactive map of accessible locations
- ➕ Add new accessible buildings with detailed information
- 📍 Share location data via GPS or manual coordinates
- 📸 Upload photos of accessibility features
- ✅ Select from multiple accessibility options for comprehensive mapping

## Getting Started

### Prerequisites

- Python 3.7+
- Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))

### Installation

1. Set up a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

5. Run the bot:
   ```
   python bot.py
   ```

## Project Structure

```
accessibility-telegram-bot/
├── bot.py                 # Main entry point
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not in repository)
├── data/
│   ├── categories.py      # Building categories and accessibility options
│   └── storage.py         # Functions for data persistence
├── handlers/
│   ├── callback_handlers.py  # Handle inline button callbacks
│   ├── command_handlers.py   # Handle bot commands
│   └── message_handlers.py   # Handle text, photo, and location messages
└── utils/
    └── helpers.py         # Utility functions
```

## Usage

1. Start the bot by sending `/start` command
2. Use the main menu to navigate:
   - 📚 FAQ - Read about accessibility features and the bot
   - 🗺️ Accessibility Map - View an interactive map of accessible buildings
   - ➕ Add Object - Submit information about a new accessible building

3. When adding a new object:
   - Select the building category
   - Choose a specific object type
   - Share the location (via GPS or manual coordinates)
   - Select accessibility features present at the location
   - Upload a photo of the building or its accessibility features

## Data Storage

The bot stores submitted data in a JSON file (`selected_objects.json`). Each entry includes:
- Building category and type
- Location coordinates
- Selected accessibility options
- Photo file ID
- Submission date

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the python-telegram-bot team for their excellent library
- Inspired by accessibility mapping initiatives worldwide